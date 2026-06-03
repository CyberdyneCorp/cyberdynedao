import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createInterpreterVM } from '../interpreterViewModel.svelte';
import * as interpreterApi from '$lib/api/interpreterApi';
import type { ExecuteResponse } from '$lib/api/interpreterApi';

function execResponse(over: Partial<ExecuteResponse> = {}): ExecuteResponse {
	return {
		success: true,
		result: null,
		stdout: '',
		stderr: '',
		error: null,
		truncated: false,
		artifacts: [],
		...over
	};
}

beforeEach(() => {
	URL.createObjectURL = vi.fn(() => 'blob:mock://abc') as typeof URL.createObjectURL;
	URL.revokeObjectURL = vi.fn() as typeof URL.revokeObjectURL;
});

afterEach(() => {
	vi.restoreAllMocks();
});

describe('interpreterViewModel', () => {
	it('starts empty with a stable web- session id', () => {
		const vm = createInterpreterVM();
		expect(vm.cells).toEqual([]);
		expect(vm.input).toBe('');
		expect(vm.running).toBe(false);
		expect(vm.sessionId).toMatch(/^web-/);
	});

	it('runCode is a no-op on empty input', async () => {
		const spy = vi.spyOn(interpreterApi, 'execute');
		const vm = createInterpreterVM();
		vm.setInput('   ');
		await vm.runCode();
		expect(spy).not.toHaveBeenCalled();
		expect(vm.cells).toEqual([]);
	});

	it('runCode records stdout/result on success and adopts artifacts', async () => {
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
			execResponse({
				stdout: '45\n',
				result: '45',
				artifacts: [{ name: 'out.txt', size_bytes: 12, modified_at: 1700000000 }]
			})
		);
		const vm = createInterpreterVM();
		vm.setInput('print(sum(range(10)))');
		await vm.runCode();
		expect(vm.cells).toHaveLength(1);
		expect(vm.cells[0].status).toBe('ok');
		expect(vm.cells[0].stdout).toBe('45\n');
		expect(vm.cells[0].result).toBe('45');
		expect(vm.input).toBe('');
		expect(vm.files).toHaveLength(1);
		expect(vm.files[0].name).toBe('out.txt');
	});

	it('passes session_id to execute', async () => {
		const spy = vi.spyOn(interpreterApi, 'execute').mockResolvedValue(execResponse());
		const vm = createInterpreterVM();
		vm.setInput('1+1');
		await vm.runCode();
		expect(spy.mock.calls[0][0].session_id).toBe(vm.sessionId);
		expect(spy.mock.calls[0][0].code).toBe('1+1');
	});

	it('marks the cell as error when success is false', async () => {
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
			execResponse({ success: false, stderr: 'Traceback', error: 'NameError: x' })
		);
		const vm = createInterpreterVM();
		vm.setInput('print(x)');
		await vm.runCode();
		expect(vm.cells[0].status).toBe('error');
		expect(vm.cells[0].stderr).toBe('Traceback');
		expect(vm.cells[0].error).toBe('NameError: x');
	});

	it('prefixes 401 with "Sign in required"', async () => {
		vi.spyOn(interpreterApi, 'execute').mockRejectedValue(
			new interpreterApi.InterpreterApiError(401, 'missing bearer')
		);
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		expect(vm.cells[0].status).toBe('error');
		expect(vm.cells[0].error).toMatch(/Sign in required/);
		expect(vm.cells[0].error).toMatch(/missing bearer/);
	});

	it('surfaces generic errors verbatim', async () => {
		vi.spyOn(interpreterApi, 'execute').mockRejectedValue(new Error('network down'));
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		expect(vm.cells[0].error).toBe('network down');
	});

	it('shows a non-401 ApiError message without the sign-in prefix', async () => {
		vi.spyOn(interpreterApi, 'execute').mockRejectedValue(
			new interpreterApi.InterpreterApiError(500, 'sandbox crashed')
		);
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		expect(vm.cells[0].error).toBe('sandbox crashed');
	});

	it('tolerates a response without an artifacts array', async () => {
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue({
			success: true,
			stdout: 'ok\n',
			stderr: ''
		} as unknown as ExecuteResponse);
		const vm = createInterpreterVM();
		vm.setInput('print("ok")');
		await vm.runCode();
		expect(vm.cells[0].status).toBe('ok');
		expect(vm.files).toEqual([]);
	});

	it('refreshFiles surfaces errors', async () => {
		vi.spyOn(interpreterApi, 'listFiles').mockRejectedValue(new Error('list failed'));
		const vm = createInterpreterVM();
		await vm.refreshFiles();
		expect(vm.error).toMatch(/list failed/);
	});

	it('downloadWorkspaceFile surfaces errors', async () => {
		vi.spyOn(interpreterApi, 'downloadFile').mockRejectedValue(new Error('404'));
		const vm = createInterpreterVM();
		await vm.downloadWorkspaceFile('missing.png');
		expect(vm.error).toMatch(/404/);
	});

	it('refuses a second run while one is in flight', async () => {
		let resolveFirst!: (v: ExecuteResponse) => void;
		vi.spyOn(interpreterApi, 'execute').mockImplementationOnce(
			() => new Promise((res) => (resolveFirst = res))
		);
		const vm = createInterpreterVM();
		vm.setInput('first');
		const inflight = vm.runCode();
		expect(vm.running).toBe(true);
		vm.setInput('second');
		await vm.runCode();
		expect(vm.cells).toHaveLength(1);
		resolveFirst(execResponse());
		await inflight;
		expect(vm.running).toBe(false);
	});

	it('clearCells empties history; resetSession also bumps session id and files', async () => {
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
			execResponse({ artifacts: [{ name: 'a', size_bytes: 1, modified_at: 0 }] })
		);
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		expect(vm.cells).toHaveLength(1);
		expect(vm.files).toHaveLength(1);
		const sid = vm.sessionId;
		vm.clearCells();
		expect(vm.cells).toEqual([]);
		expect(vm.files).toHaveLength(1); // clearCells leaves files alone
		vm.resetSession();
		expect(vm.files).toEqual([]);
		expect(vm.sessionId).not.toBe(sid);
	});

	it('refreshFiles lists workspace files', async () => {
		const spy = vi
			.spyOn(interpreterApi, 'listFiles')
			.mockResolvedValue([{ name: 'data.csv', size_bytes: 30, modified_at: 0 }]);
		const vm = createInterpreterVM();
		await vm.refreshFiles();
		expect(spy).toHaveBeenCalledWith(vm.sessionId);
		expect(vm.files).toHaveLength(1);
		expect(vm.error).toBe(null);
	});

	it('uploadWorkspaceFile uploads then re-lists', async () => {
		const upSpy = vi.spyOn(interpreterApi, 'uploadFile').mockResolvedValue({
			session_id: 's',
			file: { name: 'data.csv', size_bytes: 30, modified_at: 0 }
		});
		const listSpy = vi
			.spyOn(interpreterApi, 'listFiles')
			.mockResolvedValue([{ name: 'data.csv', size_bytes: 30, modified_at: 0 }]);
		const vm = createInterpreterVM();
		const file = new File(['1,2'], 'data.csv', { type: 'text/csv' });
		await vm.uploadWorkspaceFile(file);
		expect(upSpy).toHaveBeenCalledWith(file, 'data.csv', vm.sessionId);
		expect(listSpy).toHaveBeenCalledWith(vm.sessionId);
		expect(vm.files).toHaveLength(1);
	});

	it('uploadWorkspaceFile surfaces errors', async () => {
		vi.spyOn(interpreterApi, 'uploadFile').mockRejectedValue(new Error('too big'));
		const vm = createInterpreterVM();
		await vm.uploadWorkspaceFile(new File(['x'], 'x.bin'));
		expect(vm.error).toMatch(/too big/);
	});

	it('downloadWorkspaceFile triggers a hidden anchor', async () => {
		vi.spyOn(interpreterApi, 'downloadFile').mockResolvedValue({
			url: 'blob:dl',
			contentType: 'image/png',
			bytes: 10
		});
		const clickSpy = vi
			.spyOn(HTMLAnchorElement.prototype, 'click')
			.mockImplementation(() => {});
		const vm = createInterpreterVM();
		await vm.downloadWorkspaceFile('plot.png');
		expect(clickSpy).toHaveBeenCalledTimes(1);
		clickSpy.mockRestore();
	});

	describe('appendToInput', () => {
		it('joins with a newline when input is non-empty', () => {
			const vm = createInterpreterVM();
			vm.setInput('a = 1');
			vm.appendToInput('print(a)');
			expect(vm.input).toBe('a = 1\nprint(a)');
		});
		it('writes verbatim when empty', () => {
			const vm = createInterpreterVM();
			vm.appendToInput('print(a)');
			expect(vm.input).toBe('print(a)');
		});
		it('does not double the newline when input ends with one', () => {
			const vm = createInterpreterVM();
			vm.setInput('a = 1\n');
			vm.appendToInput('print(a)');
			expect(vm.input).toBe('a = 1\nprint(a)');
		});
	});
});
