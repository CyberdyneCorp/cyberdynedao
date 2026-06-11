import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createInterpreterVM } from '../interpreterViewModel.svelte';
import * as interpreterApi from '$lib/api/interpreterApi';
import type {
	CapabilitiesResponse,
	ExecuteResponse,
	KernelResponse,
	KernelExecuteResponse
} from '$lib/api/interpreterApi';

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

function capsResponse(over: Partial<CapabilitiesResponse> = {}): CapabilitiesResponse {
	return {
		service_version: '1.0.0',
		python_version: '3.12.1',
		restricted_by_default: true,
		allow_unrestricted: false,
		libraries: [],
		algorithms: [],
		limits: {
			timeout_seconds: 30,
			max_memory_mb: 512,
			max_output_length: 100_000,
			max_code_size: 100_000
		},
		workspace: { enabled: true, max_file_mb: 10, max_session_mb: 100, max_files: 50 },
		manim: { enabled: false, formats: [], qualities: [], timeout_seconds: 120, max_file_mb: 50 },
		kernels: { enabled: false, idle_ttl_seconds: 600, max_ttl_seconds: 3600, max_sessions: 5 },
		...over
	};
}

function kernelResponse(over: Partial<KernelResponse> = {}): KernelResponse {
	return {
		id: 'k1',
		session_id: 'srv-1',
		created_at: 0,
		last_active_at: 0,
		execution_count: 0,
		idle_expires_at: 0,
		hard_expires_at: 0,
		alive: true,
		...over
	};
}

function kernelExec(over: Partial<KernelExecuteResponse> = {}): KernelExecuteResponse {
	return {
		kernel_id: 'k1',
		alive: true,
		execution_count: 1,
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
	// The VM lazily creates a server-issued session before any execute /
	// listFiles / upload; default it so each test doesn't have to.
	vi.spyOn(interpreterApi, 'createSession').mockResolvedValue({ session_id: 'srv-1' });
	// Default to a deployment WITHOUT kernels so the existing tests exercise
	// the stateless /execute path; kernel tests override this.
	vi.spyOn(interpreterApi, 'getCapabilities').mockResolvedValue(capsResponse());
});

afterEach(() => {
	vi.restoreAllMocks();
});

describe('interpreterViewModel', () => {
	it('starts empty with no session until first use', () => {
		const vm = createInterpreterVM();
		expect(vm.cells).toEqual([]);
		expect(vm.input).toBe('');
		expect(vm.running).toBe(false);
		expect(vm.sessionId).toBeNull();
	});

	it('creates one server session and reuses it across calls', async () => {
		const createSpy = vi.spyOn(interpreterApi, 'createSession');
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue(execResponse());
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		vm.setInput('2');
		await vm.runCode();
		expect(vm.sessionId).toBe('srv-1');
		expect(createSpy).toHaveBeenCalledTimes(1);
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

	it('passes the created session_id to execute', async () => {
		const spy = vi.spyOn(interpreterApi, 'execute').mockResolvedValue(execResponse());
		const vm = createInterpreterVM();
		vm.setInput('1+1');
		await vm.runCode();
		expect(spy.mock.calls[0][0].session_id).toBe('srv-1');
		expect(vm.sessionId).toBe('srv-1');
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
		// Let the first run progress past createSession() to the (hanging)
		// execute() so resolveFirst is assigned.
		await new Promise((r) => setTimeout(r, 0));
		resolveFirst(execResponse());
		await inflight;
		expect(vm.running).toBe(false);
	});

	it('clearCells empties history; resetSession also drops session + files', async () => {
		vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
			execResponse({ artifacts: [{ name: 'a', size_bytes: 1, modified_at: 0 }] })
		);
		const vm = createInterpreterVM();
		vm.setInput('1');
		await vm.runCode();
		expect(vm.cells).toHaveLength(1);
		expect(vm.files).toHaveLength(1);
		expect(vm.sessionId).toBe('srv-1');
		vm.clearCells();
		expect(vm.cells).toEqual([]);
		expect(vm.files).toHaveLength(1); // clearCells leaves files alone
		vm.resetSession();
		expect(vm.files).toEqual([]);
		// Session dropped; the next run will create a fresh one.
		expect(vm.sessionId).toBeNull();
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

	describe('execution mode', () => {
		it('falls back to stateless /execute when kernels are disabled', async () => {
			const execSpy = vi.spyOn(interpreterApi, 'execute').mockResolvedValue(execResponse());
			const kernelSpy = vi.spyOn(interpreterApi, 'createKernel');
			const vm = createInterpreterVM();
			vm.setInput('1');
			await vm.runCode();
			expect(vm.executionMode).toBe('stateless');
			expect(execSpy).toHaveBeenCalledTimes(1);
			expect(kernelSpy).not.toHaveBeenCalled();
			expect(vm.capabilities?.python_version).toBe('3.12.1');
		});

		it('uses a persistent kernel when the deployment enables them', async () => {
			vi.spyOn(interpreterApi, 'getCapabilities').mockResolvedValue(
				capsResponse({ kernels: { enabled: true, idle_ttl_seconds: 600, max_ttl_seconds: 3600, max_sessions: 5 } })
			);
			const kernelSpy = vi.spyOn(interpreterApi, 'createKernel').mockResolvedValue(kernelResponse());
			const execInKernel = vi
				.spyOn(interpreterApi, 'executeInKernel')
				.mockResolvedValueOnce(kernelExec({ stdout: 'one\n', execution_count: 1 }))
				.mockResolvedValueOnce(kernelExec({ stdout: 'two\n', execution_count: 2 }));
			const stateless = vi.spyOn(interpreterApi, 'execute');

			const vm = createInterpreterVM();
			vm.setInput('a = 1');
			await vm.runCode();
			vm.setInput('a + 1');
			await vm.runCode();

			expect(vm.executionMode).toBe('kernel');
			// One kernel reused across both runs (state persists).
			expect(kernelSpy).toHaveBeenCalledTimes(1);
			expect(execInKernel).toHaveBeenCalledTimes(2);
			expect(stateless).not.toHaveBeenCalled();
			expect(vm.sessionId).toBe('srv-1');
			expect(vm.cells[1].executionCount).toBe(2);
			expect(vm.cells[1].stdout).toBe('two\n');
		});

		it('restarts a dead kernel and retries the run once', async () => {
			vi.spyOn(interpreterApi, 'getCapabilities').mockResolvedValue(
				capsResponse({ kernels: { enabled: true, idle_ttl_seconds: 600, max_ttl_seconds: 3600, max_sessions: 5 } })
			);
			const kernelSpy = vi
				.spyOn(interpreterApi, 'createKernel')
				.mockResolvedValueOnce(kernelResponse({ id: 'k1' }))
				.mockResolvedValueOnce(kernelResponse({ id: 'k2' }));
			const execInKernel = vi
				.spyOn(interpreterApi, 'executeInKernel')
				.mockResolvedValueOnce(kernelExec({ alive: false }))
				.mockResolvedValueOnce(kernelExec({ alive: true, stdout: 'recovered\n' }));

			const vm = createInterpreterVM();
			vm.setInput('1');
			await vm.runCode();

			expect(kernelSpy).toHaveBeenCalledTimes(2); // dead kernel recreated
			expect(execInKernel).toHaveBeenCalledTimes(2);
			expect(vm.cells[0].status).toBe('ok');
			expect(vm.cells[0].stdout).toBe('recovered\n');
			expect(vm.error).toMatch(/restarted/i);
		});
	});

	describe('rich outputs', () => {
		it('resolves image outputs to blob URLs and keeps text outputs inline', async () => {
			vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
				execResponse({
					rich_outputs: [
						{ mime_type: 'image/png', artifact: 'fig.png', text: null },
						{ mime_type: 'application/json', artifact: null, text: '{"a": 1}' }
					]
				})
			);
			const dlSpy = vi.spyOn(interpreterApi, 'downloadFile').mockResolvedValue({
				url: 'blob:img',
				contentType: 'image/png',
				bytes: 10
			});
			const vm = createInterpreterVM();
			vm.setInput('plt.plot([1,2]); plt.show()');
			await vm.runCode();

			expect(dlSpy).toHaveBeenCalledWith('srv-1', 'fig.png');
			expect(vm.cells[0].images).toHaveLength(1);
			expect(vm.cells[0].images[0]).toMatchObject({ name: 'fig.png', url: 'blob:img' });
			expect(vm.cells[0].texts).toHaveLength(1);
			expect(vm.cells[0].texts[0]).toMatchObject({ mimeType: 'application/json', text: '{"a": 1}' });
		});

		it('skips an image it cannot download without failing the cell', async () => {
			vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
				execResponse({ rich_outputs: [{ mime_type: 'image/png', artifact: 'gone.png' }] })
			);
			vi.spyOn(interpreterApi, 'downloadFile').mockRejectedValue(new Error('404'));
			const vm = createInterpreterVM();
			vm.setInput('1');
			await vm.runCode();
			expect(vm.cells[0].status).toBe('ok');
			expect(vm.cells[0].images).toHaveLength(0);
		});

		it('destroy revokes the blob URLs it minted', async () => {
			vi.spyOn(interpreterApi, 'execute').mockResolvedValue(
				execResponse({ rich_outputs: [{ mime_type: 'image/png', artifact: 'fig.png' }] })
			);
			vi.spyOn(interpreterApi, 'downloadFile').mockResolvedValue({
				url: 'blob:img',
				contentType: 'image/png',
				bytes: 10
			});
			const vm = createInterpreterVM();
			vm.setInput('1');
			await vm.runCode();
			vm.destroy();
			expect(URL.revokeObjectURL).toHaveBeenCalledWith('blob:img');
		});
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
