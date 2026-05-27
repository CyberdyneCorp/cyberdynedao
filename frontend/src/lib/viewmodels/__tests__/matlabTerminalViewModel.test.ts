import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	createMatlabTerminalVM,
	looksLikePlot,
	parseWhos
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

	it('submitPlot routes through /v1/plot with the raw source', async () => {
		const plotSpy = vi.spyOn(matlabApi, 'plot').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			artifacts: ['plot_abc123.png']
		});
		// /v1/repl is only called for the post-turn `whos` refresh.
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
		const dlSpy = vi
			.spyOn(matlabApi, 'downloadArtifact')
			.mockResolvedValue({ url: 'blob:figs', contentType: 'image/png', bytes: 1024 });
		const vm = createMatlabTerminalVM();
		vm.setInput('plot(rand(10,1))');
		await vm.submitPlot();
		expect(plotSpy).toHaveBeenCalledWith({
			source: 'plot(rand(10,1))',
			session_id: vm.sessionId,
			format: 'png'
		});
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
		vi.spyOn(matlabApi, 'plot').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			artifacts: ['plot_a.png']
		});
		// post-turn `whos` refresh
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
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

	// ── Auto Run → /v1/plot routing ─────────────────────────────────

	describe('plot auto-routing', () => {
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

		it('Run with a plot-y source routes straight to /v1/plot', async () => {
			const plotSpy = vi.spyOn(matlabApi, 'plot').mockResolvedValue({
				ok: true,
				stdout: '',
				stderr: '',
				timed_out: false,
				truncated: false,
				artifacts: ['plot_xyz.png']
			});
			// /v1/repl is only hit for the post-turn `whos` refresh.
			const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: '',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			vi.spyOn(matlabApi, 'downloadArtifact').mockResolvedValue({
				url: 'blob:figure',
				contentType: 'image/png',
				bytes: 1024
			});
			const vm = createMatlabTerminalVM();
			vm.setInput('plot(rand(10))');
			await vm.submitRepl();

			expect(plotSpy).toHaveBeenCalledTimes(1);
			expect(plotSpy.mock.calls[0][0].source).toBe('plot(rand(10))');
			// One repl call total — just the auto-refresh whos.
			expect(replSpy.mock.calls).toHaveLength(1);
			expect(replSpy.mock.calls[0][0].source).toBe('whos');
			const cell = vm.cells[0];
			expect(cell.mode).toBe('repl');
			expect(cell.plotFallback).toBe(true); // Run that got auto-routed
			expect(cell.plots).toHaveLength(1);
			expect(cell.status).toBe('ok');
		});

		it('Run with non-plot source stays on /v1/repl', async () => {
			const plotSpy = vi.spyOn(matlabApi, 'plot');
			const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: 'hi\n',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			const vm = createMatlabTerminalVM();
			vm.setInput("disp('hi')");
			await vm.submitRepl();
			expect(plotSpy).not.toHaveBeenCalled();
			// Call 0: user's Run. Call 1: auto-refresh `whos`.
			expect(replSpy.mock.calls).toHaveLength(2);
			expect(replSpy.mock.calls[1][0].source).toBe('whos');
			expect(vm.cells[0].plotFallback).toBe(false);
		});

		it('failed /v1/plot call surfaces in the cell as an error', async () => {
			vi.spyOn(matlabApi, 'plot').mockRejectedValue(new Error('boom'));
			// `whos` refresh still fires from the finally block.
			vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: '',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			const vm = createMatlabTerminalVM();
			vm.setInput('plot(rand(10))');
			await vm.submitRepl();
			expect(vm.cells[0].status).toBe('error');
			expect(vm.cells[0].error).toMatch(/boom/);
		});
	});

	// ── Artifact download error surfacing ───────────────────────────

	it('reports failed artifact downloads in artifactErrors', async () => {
		vi.spyOn(matlabApi, 'plot').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			artifacts: ['plot_ok.png', 'plot_missing.png']
		});
		// post-turn whos refresh
		vi.spyOn(matlabApi, 'repl').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: []
		});
		vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
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

	// ── Workspace state ──────────────────────────────────────────────

	describe('parseWhos', () => {
		it('parses a 3-column matlab-llvm output', () => {
			const stdout = `  Name             Size             Class\n` +
				`  A                5x5              double\n` +
				`  b                1x1              double\n`;
			const vars = parseWhos(stdout);
			expect(vars).toEqual([
				{ name: 'A', size: '5x5', klass: 'double' },
				{ name: 'b', size: '1x1', klass: 'double' }
			]);
		});

		it('returns empty for header-only output', () => {
			expect(parseWhos('  Name  Size  Class\n')).toEqual([]);
		});

		it('returns empty for completely empty input', () => {
			expect(parseWhos('')).toEqual([]);
		});

		it('skips noise lines that do not start with a valid identifier', () => {
			const stdout = `Warning: workspace state lost\n` +
				`  A    5x5    double\n` +
				`>>>\n`;
			expect(parseWhos(stdout)).toEqual([
				{ name: 'A', size: '5x5', klass: 'double' }
			]);
		});

		it('keeps trailing class attributes joined', () => {
			const stdout = `  Name  Size  Class\n  x  3x3  double sparse\n`;
			expect(parseWhos(stdout)).toEqual([
				{ name: 'x', size: '3x3', klass: 'double sparse' }
			]);
		});
	});

	describe('workspace refresh', () => {
		it('refreshWorkspace populates variables (from whos) + files', async () => {
			vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: '  Name  Size  Class\n  A  5x5  double\n',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([
				{ path: 'note.txt', size: 12, modified: 1700000000 }
			]);
			const vm = createMatlabTerminalVM();
			await vm.refreshWorkspace();
			expect(vm.workspaceVariables).toHaveLength(1);
			expect(vm.workspaceVariables[0]).toEqual({
				name: 'A',
				size: '5x5',
				klass: 'double'
			});
			expect(vm.workspaceFiles).toHaveLength(1);
			expect(vm.workspaceError).toBe(null);
		});

		it('passes the VM sessionId to whos + listFiles', async () => {
			const replSpy = vi.spyOn(matlabApi, 'repl').mockResolvedValue({
				ok: true,
				stdout: '',
				stderr: '',
				timed_out: false,
				truncated: false,
				stateful: true,
				artifacts: []
			});
			const filesSpy = vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			const vm = createMatlabTerminalVM();
			await vm.refreshWorkspace();
			expect(replSpy.mock.calls[0][0].source).toBe('whos');
			expect(replSpy.mock.calls[0][0].session_id).toBe(vm.sessionId);
			expect(filesSpy).toHaveBeenCalledWith(vm.sessionId);
		});

		it('coalesces concurrent refresh calls (only one in-flight)', async () => {
			const replSpy = vi.spyOn(matlabApi, 'repl').mockImplementation(
				() =>
					new Promise((r) =>
						setTimeout(
							() =>
								r({
									ok: true,
									stdout: '',
									stderr: '',
									timed_out: false,
									truncated: false,
									stateful: true,
									artifacts: []
								}),
							5
						)
					)
			);
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			const vm = createMatlabTerminalVM();
			await Promise.all([vm.refreshWorkspace(), vm.refreshWorkspace()]);
			expect(replSpy).toHaveBeenCalledTimes(1);
		});

		it('records partial failure (files OK, whos fails) in workspaceError', async () => {
			vi.spyOn(matlabApi, 'repl').mockRejectedValue(new Error('whos boom'));
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([
				{ path: 'x.bin', size: 1, modified: 0 }
			]);
			const vm = createMatlabTerminalVM();
			await vm.refreshWorkspace();
			expect(vm.workspaceError).toMatch(/whos boom/);
			expect(vm.workspaceFiles).toHaveLength(1);
		});

		it('auto-refreshes after a successful REPL turn', async () => {
			vi.spyOn(matlabApi, 'repl')
				.mockResolvedValueOnce({
					ok: true,
					stdout: 'hello\n',
					stderr: '',
					timed_out: false,
					truncated: false,
					stateful: true,
					artifacts: []
				})
				.mockResolvedValueOnce({
					// Second call is the auto-refresh ``whos``.
					ok: true,
					stdout: '  Name  Size  Class\n  z  1x1  double\n',
					stderr: '',
					timed_out: false,
					truncated: false,
					stateful: true,
					artifacts: []
				});
			vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([]);
			const vm = createMatlabTerminalVM();
			vm.setInput('z = 7');
			await vm.submitRepl();
			// runOne fires the refresh in a non-awaited microtask via
			// ``void refreshWorkspace()``; flush a tick or two.
			await new Promise((r) => setTimeout(r, 5));
			expect(vm.workspaceVariables).toEqual([
				{ name: 'z', size: '1x1', klass: 'double' }
			]);
		});
	});

	describe('appendToInput', () => {
		it('appends with a newline when input is non-empty', () => {
			const vm = createMatlabTerminalVM();
			vm.setInput('A = magic(5)');
			vm.appendToInput('disp(A)');
			expect(vm.input).toBe('A = magic(5)\ndisp(A)');
		});
		it('does not double the newline when input ends with one', () => {
			const vm = createMatlabTerminalVM();
			vm.setInput('A = magic(5)\n');
			vm.appendToInput('disp(A)');
			expect(vm.input).toBe('A = magic(5)\ndisp(A)');
		});
		it('writes verbatim when input is empty', () => {
			const vm = createMatlabTerminalVM();
			vm.appendToInput('disp(A)');
			expect(vm.input).toBe('disp(A)');
		});
	});

	describe('uploadWorkspaceFile + downloadWorkspaceFile', () => {
		it('uploadWorkspaceFile POSTs and re-lists files', async () => {
			const uploadSpy = vi.spyOn(matlabApi, 'uploadFile').mockResolvedValue({
				ok: true,
				file: { path: 'data.csv', size: 32, modified: 0 }
			});
			const listSpy = vi.spyOn(matlabApi, 'listFiles').mockResolvedValue([
				{ path: 'data.csv', size: 32, modified: 0 }
			]);
			const vm = createMatlabTerminalVM();
			const file = new File(['1,2,3'], 'data.csv', { type: 'text/csv' });
			await vm.uploadWorkspaceFile(file);
			expect(uploadSpy).toHaveBeenCalledWith(file, 'data.csv', vm.sessionId);
			expect(listSpy).toHaveBeenCalledWith(vm.sessionId);
			expect(vm.workspaceFiles).toHaveLength(1);
		});

		it('uploadWorkspaceFile surfaces errors via workspaceError', async () => {
			vi.spyOn(matlabApi, 'uploadFile').mockRejectedValue(new Error('quota exceeded'));
			const vm = createMatlabTerminalVM();
			const file = new File(['x'], 'too-big.bin');
			await vm.uploadWorkspaceFile(file);
			expect(vm.workspaceError).toMatch(/quota exceeded/);
		});

		it('downloadWorkspaceFile triggers a hidden anchor with the right filename', async () => {
			vi.spyOn(matlabApi, 'downloadArtifact').mockResolvedValue({
				url: 'blob:dl',
				contentType: 'image/png',
				bytes: 100
			});
			// Spy on anchor click to confirm the download was triggered.
			const clickSpy = vi
				.spyOn(HTMLAnchorElement.prototype, 'click')
				.mockImplementation(() => {});
			const vm = createMatlabTerminalVM();
			await vm.downloadWorkspaceFile('plots/figure.png');
			expect(clickSpy).toHaveBeenCalledTimes(1);
			clickSpy.mockRestore();
		});
	});
});
