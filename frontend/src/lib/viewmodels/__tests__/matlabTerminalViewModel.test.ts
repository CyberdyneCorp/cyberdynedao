import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	createMatlabTerminalVM,
	looksLikePlot,
	withSaveas
} from '../matlabTerminalViewModel.svelte';
import * as matlabApi from '$lib/api/matlabApi';

beforeEach(() => {
	// Override jsdom's nodedata: implementation so we can assert on
	// the revoke calls deterministically.
	URL.createObjectURL = vi.fn(() => 'blob:mock://abc') as typeof URL.createObjectURL;
	URL.revokeObjectURL = vi.fn() as typeof URL.revokeObjectURL;
});

afterEach(() => {
	vi.restoreAllMocks();
});

describe('matlabTerminalViewModel', () => {
	it('starts with no cells and a stable session id', () => {
		const vm = createMatlabTerminalVM();
		expect(vm.cells).toEqual([]);
		expect(vm.input).toBe('');
		expect(vm.running).toBe(false);
		expect(vm.sessionId).toMatch(/^web-/);
	});

	it('submitRepl is a no-op when input is empty', async () => {
		const replSpy = vi.spyOn(matlabApi, 'repl');
		const vm = createMatlabTerminalVM();
		vm.setInput('   ');
		await vm.submitRepl();
		expect(replSpy).not.toHaveBeenCalled();
		expect(vm.cells).toEqual([]);
	});

	it('submitRepl pushes a cell and records stdout on success', async () => {
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: 'hello\n',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		const vm = createMatlabTerminalVM();
		vm.setInput("disp('hello')");
		await vm.submitRepl();
		expect(vm.cells).toHaveLength(1);
		expect(vm.cells[0].status).toBe('ok');
		expect(vm.cells[0].mode).toBe('repl');
		expect(vm.cells[0].stdout).toBe('hello\n');
		expect(vm.cells[0].source).toBe("disp('hello')");
		expect(vm.input).toBe(''); // cleared on submit
	});

	it('passes session_id + stateful=true to the API', async () => {
		const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		const vm = createMatlabTerminalVM();
		vm.setInput('x = 1');
		await vm.submitRepl();
		expect(replSpy).toHaveBeenCalledWith({
			source: 'x = 1',
			session_id: vm.sessionId,
			stateful: true
		});
	});

	it('submitPlot routes through /v1/repl with appended saveas', async () => {
		const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: ['cd_plot_x_abcdef.png']
		});
		const dlSpy = vi
			.spyOn(matlabApi, 'downloadArtifact')
			.mockResolvedValue({ url: 'blob:figs', contentType: 'image/png', bytes: 1024 });
		const vm = createMatlabTerminalVM();
		vm.setInput('plot(rand(10,1))');
		await vm.submitPlot();
		expect(replSpy).toHaveBeenCalledTimes(1);
		// The source got augmented with our saveas call.
		const payload = replSpy.mock.calls[0][0];
		expect(payload.source).toMatch(/saveas\(gcf, 'cd_plot_/);
		expect(payload.source).toMatch(/^plot\(rand\(10,1\)\);/);
		expect(dlSpy).toHaveBeenCalled();
		expect(vm.cells[0].plots).toHaveLength(1);
		expect(vm.cells[0].mode).toBe('plot');
	});

	it('surfaces 401 with a "Sign in required" prefix', async () => {
		vi.spyOn(matlabApi, 'repl').mockRejectedValue(
			new matlabApi.MatlabApiError(401, 'missing bearer token')
		);
		const vm = createMatlabTerminalVM();
		vm.setInput('x');
		await vm.submitRepl();
		expect(vm.cells[0].status).toBe('error');
		expect(vm.cells[0].error).toMatch(/Sign in required/);
		expect(vm.cells[0].error).toMatch(/missing bearer token/);
	});

	it('surfaces generic errors verbatim', async () => {
		vi.spyOn(matlabApi, 'repl').mockRejectedValue(new Error('network down'));
		const vm = createMatlabTerminalVM();
		vm.setInput('x');
		await vm.submitRepl();
		expect(vm.cells[0].status).toBe('error');
		expect(vm.cells[0].error).toBe('network down');
	});

	it('flags timed_out and truncated in the cell', async () => {
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: false,
			stdout: '',
			stderr: 'killed',
			timed_out: true,
			truncated: true,
			stateful: true,
			artifacts: []
		});
		const vm = createMatlabTerminalVM();
		vm.setInput('while true; end');
		await vm.submitRepl();
		expect(vm.cells[0].timedOut).toBe(true);
		expect(vm.cells[0].truncated).toBe(true);
		expect(vm.cells[0].status).toBe('error');
	});

	it('refuses to start a second cell while one is running', async () => {
		let resolveFirst!: (v: matlabApi.ReplResponse) => void;
		vi.spyOn(matlabApi, 'repl').mockImplementationOnce(
			() => new Promise((res) => (resolveFirst = res))
		);
		const vm = createMatlabTerminalVM();
		vm.setInput('first');
		const inflight = vm.submitRepl();
		expect(vm.running).toBe(true);
		// While inflight, this is a no-op (running guard).
		vm.setInput('second');
		await vm.submitRepl();
		expect(vm.cells).toHaveLength(1);
		resolveFirst({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		await inflight;
		expect(vm.running).toBe(false);
	});

	it('clearCells drops history and revokes plot URLs', async () => {
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: ['cd_plot_a.png']
		});
		vi.spyOn(matlabApi, 'downloadArtifact').mockResolvedValue({
			url: 'blob:to-revoke',
			contentType: 'image/png',
			bytes: 10
		});
		const vm = createMatlabTerminalVM();
		vm.setInput('plot(1)');
		await vm.submitPlot();
		expect(vm.cells).toHaveLength(1);
		vm.clearCells();
		expect(vm.cells).toEqual([]);
		expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:to-revoke');
	});

	it('resetSession bumps the session id', async () => {
		const vm = createMatlabTerminalVM();
		const first = vm.sessionId;
		vm.resetSession();
		expect(vm.sessionId).not.toBe(first);
		expect(vm.cells).toEqual([]);
	});

	// ── Auto Run → Plot fallback ────────────────────────────────────

	describe('plot auto-fallback', () => {
		it('looksLikePlot matches common plotting verbs', () => {
			expect(looksLikePlot('plot(x, y)')).toBe(true);
			expect(looksLikePlot('  figure; plot(x, y)')).toBe(true);
			expect(looksLikePlot('imshow(img)')).toBe(true);
			expect(looksLikePlot('surf(Z)')).toBe(true);
			expect(looksLikePlot('histogram(rand(100,1))')).toBe(true);
			expect(looksLikePlot('a = 1; bar([1 2 3])')).toBe(true);
		});

		it('looksLikePlot rejects non-plot code', () => {
			expect(looksLikePlot('disp(1+1)')).toBe(false);
			expect(looksLikePlot("x = 'plot a chart'")).toBe(false);
			expect(looksLikePlot('A = magic(5)')).toBe(false);
		});

		it('withSaveas appends saveas + strips trailing punctuation', () => {
			expect(withSaveas('plot(x)', 'p.png')).toMatch(/^plot\(x\);\nsaveas\(gcf, 'p\.png'\);\n$/);
			// Trailing semicolon + whitespace is collapsed.
			expect(withSaveas('plot(x);   ', 'p.png')).toMatch(/^plot\(x\);\nsaveas/);
		});

		it('Run with a plotting source + empty artifacts → re-invokes /v1/repl with saveas', async () => {
			const replSpy = vi
				.spyOn(matlabApi, 'repl')
				.mockResolvedValueOnce({
					ok: true,
					stdout: '',
					stderr: '',
					timed_out: false,
					truncated: false,
					stateful: true,
					artifacts: []
				})
				.mockResolvedValueOnce({
					ok: true,
					stdout: '',
					stderr: '',
					timed_out: false,
					truncated: false,
					stateful: true,
					artifacts: ['cd_plot_x_abcdef.png']
				});
			vi.spyOn(matlabApi, 'downloadArtifact').mockResolvedValue({
				url: 'blob:figure',
				contentType: 'image/png',
				bytes: 1024
			});
			const vm = createMatlabTerminalVM();
			vm.setInput('plot(rand(10))');
			await vm.submitRepl();

			expect(replSpy).toHaveBeenCalledTimes(2);
			// Second call has saveas appended.
			expect(replSpy.mock.calls[1][0].source).toMatch(/saveas\(gcf, 'cd_plot_/);
			const cell = vm.cells[0];
			expect(cell.mode).toBe('repl');
			expect(cell.plotFallback).toBe(true);
			expect(cell.plots).toHaveLength(1);
			expect(cell.status).toBe('ok');
		});

		it('Run with non-plot source never fires the fallback', async () => {
			const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: 'hi\n',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			const vm = createMatlabTerminalVM();
			vm.setInput("disp('hi')");
			await vm.submitRepl();
			expect(replSpy).toHaveBeenCalledTimes(1);
			expect(vm.cells[0].plotFallback).toBe(false);
		});

		it('Run that already returned artifacts does not fire the fallback', async () => {
			const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: '',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: ['cd_pre.png']
			});
			vi.spyOn(matlabApi, 'downloadArtifact').mockResolvedValue({
				url: 'blob:1',
				contentType: 'image/png',
				bytes: 100
			});
			const vm = createMatlabTerminalVM();
			vm.setInput('plot(1)');
			await vm.submitRepl();
			expect(replSpy).toHaveBeenCalledTimes(1);
			expect(vm.cells[0].plotFallback).toBe(false);
		});

		it('Fallback failure leaves a note in artifactErrors but keeps the cell OK', async () => {
			vi.spyOn(matlabApi, 'repl')
				.mockResolvedValueOnce({
					ok: true,
					stdout: '',
					stderr: '',
					timed_out: false,
					truncated: false,
					stateful: true,
					artifacts: []
				})
				.mockRejectedValueOnce(new Error('boom'));
			const vm = createMatlabTerminalVM();
			vm.setInput('plot(rand(10))');
			await vm.submitRepl();
			expect(vm.cells[0].status).toBe('ok');
			expect(vm.cells[0].plotFallback).toBe(false);
			expect(vm.cells[0].artifactErrors[0]).toMatch(/plot fallback failed: boom/);
		});
	});

	// ── Artifact download error surfacing ───────────────────────────

	it('reports failed artifact downloads in artifactErrors', async () => {
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: ['cd_plot_ok.png', 'cd_plot_missing.png']
		});
		vi.spyOn(matlabApi, 'downloadArtifact').mockImplementation(async (path) => {
			if (path.endsWith('missing.png')) {
				throw new matlabApi.MatlabApiError(404, 'not found');
			}
			return { url: 'blob:ok', contentType: 'image/png', bytes: 100 };
		});
		const vm = createMatlabTerminalVM();
		vm.setInput('plot(1)');
		await vm.submitPlot();
		expect(vm.cells[0].plots).toHaveLength(1);
		expect(vm.cells[0].artifactErrors).toHaveLength(1);
		expect(vm.cells[0].artifactErrors[0]).toMatch(/missing.png.*not found/);
	});
});
