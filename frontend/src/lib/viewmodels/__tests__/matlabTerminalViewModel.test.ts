import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createMatlabTerminalVM } from '../matlabTerminalViewModel.svelte';
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

	it('submitPlot calls plot() and downloads artifacts in parallel', async () => {
		vi.spyOn(matlabApi, 'plot').mockResolvedValue({
			ok: true,
			stdout: '',
			stderr: '',
			timed_out: false,
			truncated: false,
			stateful: true,
			artifacts: ['/m/figs/a.png', '/m/figs/b.png']
		});
		const dlSpy = vi
			.spyOn(matlabApi, 'downloadArtifact')
			.mockImplementation(async (path) => ({
				url: `blob:mock://${path}`,
				contentType: 'image/png',
				bytes: 1024
			}));
		const vm = createMatlabTerminalVM();
		vm.setInput('plot(rand(10,1))');
		await vm.submitPlot();
		expect(dlSpy).toHaveBeenCalledTimes(2);
		expect(vm.cells[0].plots).toHaveLength(2);
		expect(vm.cells[0].plots[0].contentType).toBe('image/png');
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
			stateful: true,
			artifacts: ['/m/a.png']
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
});
