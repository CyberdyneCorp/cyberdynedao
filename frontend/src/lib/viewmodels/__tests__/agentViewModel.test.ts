import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createAgentVM } from '../agentViewModel.svelte';
import * as agentApi from '$lib/api/agentApi';
import * as interpreterApi from '$lib/api/interpreterApi';

beforeEach(() => {
	sessionStorage.clear();
});

afterEach(() => {
	vi.restoreAllMocks();
});

describe('agentViewModel', () => {
	it('starts empty until bootstrap completes', () => {
		const vm = createAgentVM();
		expect(vm.bubbles).toEqual([]);
		expect(vm.sessionId).toBe(null);
		expect(vm.running).toBe(false);
		expect(vm.bootstrapped).toBe(false);
	});

	it('bootstrap with no persisted session leaves sessionId null', async () => {
		const vm = createAgentVM();
		await vm.bootstrap();
		expect(vm.sessionId).toBe(null);
		expect(vm.bubbles).toEqual([]);
		expect(vm.bootstrapped).toBe(true);
	});

	it('bootstrap restores persisted bubbles from sessionStorage', async () => {
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({
				sessionId: 's-1',
				bubbles: [
					{
						id: 'b-1',
						role: 'user',
						content: 'hello',
						toolCalls: [],
						model: null,
						createdAt: '2026-05-26T09:00:00Z',
						pending: false,
						error: null
					}
				]
			})
		);
		vi.spyOn(agentApi, 'getHistory').mockResolvedValue({
			sessionId: 's-1',
			messages: [
				{
					id: 'b-1',
					sessionId: 's-1',
					role: 'user',
					content: 'hello',
					toolCalls: [],
					toolCallId: null,
					tokensIn: 0,
					tokensOut: 0,
					model: null,
					createdAt: '2026-05-26T09:00:00Z'
				}
			]
		});
		const vm = createAgentVM();
		await vm.bootstrap();
		expect(vm.sessionId).toBe('s-1');
		expect(vm.bubbles).toHaveLength(1);
		expect(vm.bubbles[0].content).toBe('hello');
	});

	it('attaches a matlab_plot figure to its assistant bubble', async () => {
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({ sessionId: 's-plot', bubbles: [] })
		);
		vi.spyOn(agentApi, 'getHistory').mockResolvedValue({
			sessionId: 's-plot',
			messages: [
				{
					id: 'u1', sessionId: 's-plot', role: 'user', content: 'plot a sine',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-05-27T09:00:00Z'
				},
				{
					id: 'a1', sessionId: 's-plot', role: 'assistant', content: 'Here you go.',
					toolCalls: [{ id: 'call_1', name: 'matlab_plot', argumentsJson: '{}' }],
					toolCallId: null, tokensIn: 0, tokensOut: 0, model: 'gpt-4o-mini',
					createdAt: '2026-05-27T09:00:01Z'
				},
				{
					id: 't1', sessionId: 's-plot', role: 'tool',
					content: JSON.stringify({ ok: true, has_figure: true, figures: ['plot_abc.png'], session_id: 'agent-s-plot' }),
					toolCalls: [], toolCallId: 'call_1', tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-05-27T09:00:02Z'
				}
			]
		});
		const vm = createAgentVM();
		await vm.bootstrap();
		// tool message is not its own bubble
		expect(vm.bubbles).toHaveLength(2);
		const assistant = vm.bubbles[1];
		expect(assistant.role).toBe('assistant');
		expect(assistant.plots).toHaveLength(1);
		expect(assistant.plots[0].artifactPath).toBe('plot_abc.png');
		expect(assistant.plots[0].sessionId).toBe('agent-s-plot');
		// matlab_* figures download through the MATLAB proxy.
		expect(assistant.plots[0].source).toBe('matlab');
	});

	it('attaches a python_exec figure tagged as an interpreter-sourced plot', async () => {
		// Regression: python figures live in the interpreter workspace and must
		// be tagged 'interpreter' so the view downloads them via /api/interpreter,
		// not the MATLAB proxy (which would 404 → "Figure unavailable").
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({ sessionId: 's-py', bubbles: [] })
		);
		vi.spyOn(agentApi, 'getHistory').mockResolvedValue({
			sessionId: 's-py',
			messages: [
				{
					id: 'u1', sessionId: 's-py', role: 'user', content: 'plot a sine in python',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-06T09:00:00Z'
				},
				{
					id: 'a1', sessionId: 's-py', role: 'assistant', content: 'Here it is.',
					toolCalls: [{ id: 'call_1', name: 'python_exec', argumentsJson: '{}' }],
					toolCallId: null, tokensIn: 0, tokensOut: 0, model: 'gpt-4o-mini',
					createdAt: '2026-06-06T09:00:01Z'
				},
				{
					id: 't1', sessionId: 's-py', role: 'tool',
					content: JSON.stringify({ ok: true, has_figure: true, figures: ['figure_0_1.png'], session_id: 'srv-9' }),
					toolCalls: [], toolCallId: 'call_1', tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-06T09:00:02Z'
				}
			]
		});
		const vm = createAgentVM();
		await vm.bootstrap();
		const assistant = vm.bubbles[1];
		expect(assistant.plots).toHaveLength(1);
		expect(assistant.plots[0].artifactPath).toBe('figure_0_1.png');
		expect(assistant.plots[0].sessionId).toBe('srv-9');
		expect(assistant.plots[0].source).toBe('interpreter');
		// The image is rendered inline as a plot, not listed as a download.
		expect(assistant.artifacts).toHaveLength(0);
	});

	it('attaches python_exec file artifacts (download links) to the assistant bubble, skipping images', async () => {
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({ sessionId: 's-doc', bubbles: [] })
		);
		vi.spyOn(agentApi, 'getHistory').mockResolvedValue({
			sessionId: 's-doc',
			messages: [
				{
					id: 'u1', sessionId: 's-doc', role: 'user', content: 'make a markdown summary',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-04T09:00:00Z'
				},
				{
					id: 'a1', sessionId: 's-doc', role: 'assistant', content: 'Done — download below.',
					toolCalls: [{ id: 'call_1', name: 'python_exec', argumentsJson: '{}' }],
					toolCallId: null, tokensIn: 0, tokensOut: 0, model: 'gpt-4o-mini',
					createdAt: '2026-06-04T09:00:01Z'
				},
				{
					id: 't1', sessionId: 's-doc', role: 'tool',
					content: JSON.stringify({
						ok: true,
						session_id: 'srv-7',
						artifacts: [
							{ name: 'summary.md', size_bytes: 412, modified_at: 1 },
							{ name: 'chart.png', size_bytes: 999, modified_at: 1 }
						]
					}),
					toolCalls: [], toolCallId: 'call_1', tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-04T09:00:02Z'
				}
			]
		});
		const vm = createAgentVM();
		await vm.bootstrap();
		const assistant = vm.bubbles[1];
		// chart.png is an image (shown as a plot path), so it's excluded here.
		expect(assistant.artifacts).toHaveLength(1);
		expect(assistant.artifacts[0].name).toBe('summary.md');
		expect(assistant.artifacts[0].sessionId).toBe('srv-7');
		expect(assistant.artifacts[0].sizeBytes).toBe(412);
	});

	it('attaches the figure to the final text bubble, skipping the empty tool-call round', async () => {
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({ sessionId: 's-turn', bubbles: [] })
		);
		vi.spyOn(agentApi, 'getHistory').mockResolvedValue({
			sessionId: 's-turn',
			messages: [
				{
					id: 'u', sessionId: 's-turn', role: 'user', content: 'plot it',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-05-27T09:00:00Z'
				},
				// intermediate tool-call round — empty text, carries the call
				{
					id: 'a-int', sessionId: 's-turn', role: 'assistant', content: '',
					toolCalls: [{ id: 'call_9', name: 'matlab_plot', argumentsJson: '{}' }],
					toolCallId: null, tokensIn: 0, tokensOut: 0, model: 'm',
					createdAt: '2026-05-27T09:00:01Z'
				},
				{
					id: 't', sessionId: 's-turn', role: 'tool',
					content: JSON.stringify({ ok: true, has_figure: true, figures: ['p.png'], session_id: 'agent-s-turn' }),
					toolCalls: [], toolCallId: 'call_9', tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-05-27T09:00:02Z'
				},
				// final text reply — no tool calls
				{
					id: 'a-final', sessionId: 's-turn', role: 'assistant', content: 'Here is the plot.',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: 'm',
					createdAt: '2026-05-27T09:00:03Z'
				}
			]
		});
		const vm = createAgentVM();
		await vm.bootstrap();
		// empty intermediate bubble is dropped → user + final assistant only
		expect(vm.bubbles).toHaveLength(2);
		const finalBubble = vm.bubbles[1];
		expect(finalBubble.content).toBe('Here is the plot.');
		expect(finalBubble.plots).toHaveLength(1);
		expect(finalBubble.plots[0].artifactPath).toBe('p.png');
	});

	it('bootstrap keeps local cache when remote history fetch fails', async () => {
		sessionStorage.setItem(
			'cyberdyne.agent.v1',
			JSON.stringify({
				sessionId: 's-cache',
				bubbles: [
					{
						id: 'b-1',
						role: 'user',
						content: 'cached',
						toolCalls: [],
						model: null,
						createdAt: '2026-05-26T09:00:00Z',
						pending: false,
						error: null
					}
				]
			})
		);
		vi.spyOn(agentApi, 'getHistory').mockRejectedValue(new Error('offline'));
		const vm = createAgentVM();
		await vm.bootstrap();
		expect(vm.bubbles).toHaveLength(1);
		expect(vm.bubbles[0].content).toBe('cached');
	});

	it('send is a no-op when input is empty', async () => {
		const spy = vi.spyOn(agentApi, 'startSession');
		const vm = createAgentVM();
		vm.setInput('   ');
		await vm.send();
		expect(spy).not.toHaveBeenCalled();
	});

	// Mock streamMessage to emit optional deltas then a final `done` message.
	function mockStream(message: Partial<agentApi.AgentMessage> = {}, deltas: string[] = []) {
		return vi
			.spyOn(agentApi, 'streamMessage')
			.mockImplementation(async (_sid, _content, handlers) => {
				for (const d of deltas) handlers.onDelta(d);
				handlers.onDone({
					id: 'm',
					sessionId: 's',
					role: 'assistant',
					content: deltas.join('') || 'ok',
					toolCalls: [],
					toolCallId: null,
					tokensIn: 0,
					tokensOut: 0,
					model: null,
					createdAt: '',
					...message
				});
			});
	}

	it('send creates a session on first call and streams + persists bubbles', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's-new',
			createdAt: '2026-05-26T09:00:00Z'
		});
		mockStream({ id: 'm-r', content: 'pong', model: 'gpt-4o-mini' }, ['po', 'ng']);
		const vm = createAgentVM();
		vm.setInput('ping');
		await vm.send();
		expect(vm.sessionId).toBe('s-new');
		expect(vm.bubbles).toHaveLength(2);
		expect(vm.bubbles[0].role).toBe('user');
		expect(vm.bubbles[0].content).toBe('ping');
		expect(vm.bubbles[1].role).toBe('assistant');
		expect(vm.bubbles[1].content).toBe('pong');
		expect(vm.bubbles[1].pending).toBe(false);
		// Persistence: re-read from storage and confirm.
		const stored = JSON.parse(sessionStorage.getItem('cyberdyne.agent.v1') ?? 'null');
		expect(stored.sessionId).toBe('s-new');
		expect(stored.bubbles).toHaveLength(2);
	});

	it('shows a tool-status line during the turn, cleared once tokens arrive', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({ sessionId: 's', createdAt: '' });
		let captured: agentApi.StreamHandlers | null = null;
		vi.spyOn(agentApi, 'streamMessage').mockImplementation(async (_s, _c, handlers) => {
			captured = handlers;
			handlers.onStatus('python_exec');
		});
		const vm = createAgentVM();
		vm.setInput('plot it');
		const inflight = vm.send();
		await new Promise((r) => setTimeout(r, 0));
		expect(vm.bubbles[1].status).toBe('running python_exec…');
		// First token clears the status; done finalizes.
		captured!.onDelta('Here');
		expect(vm.bubbles[1].status).toBe('');
		captured!.onDone({
			id: 'm', sessionId: 's', role: 'assistant', content: 'Here you go',
			toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null, createdAt: ''
		});
		await inflight;
		expect(vm.bubbles[1].content).toBe('Here you go');
	});

	it('send surfaces 401 with a "Sign in required" prefix', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's',
			createdAt: ''
		});
		vi.spyOn(agentApi, 'streamMessage').mockRejectedValue(
			new agentApi.AgentApiError(401, 'authentication required')
		);
		const vm = createAgentVM();
		vm.setInput('hi');
		await vm.send();
		const assistantBubble = vm.bubbles[vm.bubbles.length - 1];
		expect(assistantBubble.error).toMatch(/Sign in required/);
		expect(vm.error).toMatch(/Sign in required/);
	});

	it('surfaces an in-band stream error event', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({ sessionId: 's', createdAt: '' });
		vi.spyOn(agentApi, 'streamMessage').mockImplementation(async (_s, _c, handlers) => {
			handlers.onError('provider exploded');
		});
		const vm = createAgentVM();
		vm.setInput('hi');
		await vm.send();
		expect(vm.bubbles[vm.bubbles.length - 1].error).toMatch(/provider exploded/);
	});

	it('resetSession clears bubbles + storage and starts a fresh session', async () => {
		const startSpy = vi
			.spyOn(agentApi, 'startSession')
			.mockResolvedValueOnce({ sessionId: 's-1', createdAt: '' })
			.mockResolvedValueOnce({ sessionId: 's-2', createdAt: '' });
		mockStream();
		const vm = createAgentVM();
		vm.setInput('q1');
		await vm.send();
		expect(vm.sessionId).toBe('s-1');
		expect(vm.bubbles.length).toBe(2);
		await vm.resetSession();
		expect(vm.sessionId).toBe('s-2');
		expect(vm.bubbles).toEqual([]);
		expect(sessionStorage.getItem('cyberdyne.agent.v1')).toMatch(/s-2/);
		expect(startSpy).toHaveBeenCalledTimes(2);
	});

	it('refuses to start a second send while one is in flight', async () => {
		let resolveSend!: () => void;
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's',
			createdAt: ''
		});
		const sendSpy = vi
			.spyOn(agentApi, 'streamMessage')
			.mockImplementation(() => new Promise((r) => (resolveSend = () => r())));
		const vm = createAgentVM();
		vm.setInput('first');
		const inflight = vm.send();
		expect(vm.running).toBe(true);
		// Let the first send's ``await ensureSession()`` flush so
		// streamMessage actually fires and resolveSend gets assigned.
		await new Promise((r) => setTimeout(r, 0));
		expect(sendSpy).toHaveBeenCalledTimes(1);
		vm.setInput('second');
		await vm.send();
		// The running-guard short-circuited; streamMessage still called once.
		expect(sendSpy).toHaveBeenCalledTimes(1);
		expect(vm.bubbles.length).toBe(2);
		resolveSend();
		await inflight;
		expect(vm.running).toBe(false);
	});

	it('attachFile uploads to a new interpreter session and stages a chip', async () => {
		const createSpy = vi.spyOn(interpreterApi, 'createSession').mockResolvedValue({
			session_id: 'isid-1'
		});
		const uploadSpy = vi.spyOn(interpreterApi, 'uploadFile').mockResolvedValue({
			session_id: 'isid-1',
			file: { name: 'scores.csv', size_bytes: 35, modified_at: 1 }
		});
		const vm = createAgentVM();
		await vm.attachFile(new File(['name,score\n'], 'scores.csv', { type: 'text/csv' }));
		expect(createSpy).toHaveBeenCalledOnce();
		// uploadFile(file, filename, sessionId)
		expect(uploadSpy.mock.calls[0][1]).toBe('scores.csv');
		expect(uploadSpy.mock.calls[0][2]).toBe('isid-1');
		expect(vm.attachments).toEqual([{ name: 'scores.csv', sizeBytes: 35 }]);
	});

	it('send forwards staged attachments + interpreter session, then clears them', async () => {
		vi.spyOn(interpreterApi, 'createSession').mockResolvedValue({ session_id: 'isid-9' });
		vi.spyOn(interpreterApi, 'uploadFile').mockResolvedValue({
			session_id: 'isid-9',
			file: { name: 'data.csv', size_bytes: 10, modified_at: 1 }
		});
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's-att',
			createdAt: '2026-06-06T09:00:00Z'
		});
		const sendSpy = vi
			.spyOn(agentApi, 'streamMessage')
			.mockImplementation(async (_s, _c, handlers) => {
				handlers.onDone({
					id: 'm', sessionId: 's-att', role: 'assistant', content: 'done',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-06T09:00:01Z'
				});
			});
		const vm = createAgentVM();
		await vm.attachFile(new File(['x'], 'data.csv'));
		vm.setInput('analyze this');
		await vm.send();
		// streamMessage(sessionId, content, handlers, {interpreterSessionId, filenames})
		expect(sendSpy.mock.calls[0][1]).toBe('analyze this');
		expect(sendSpy.mock.calls[0][3]).toEqual({
			interpreterSessionId: 'isid-9',
			filenames: ['data.csv']
		});
		// Staged attachments are cleared after the turn.
		expect(vm.attachments).toEqual([]);
	});

	it('send with only an attachment (no text) supplies a default ask', async () => {
		vi.spyOn(interpreterApi, 'createSession').mockResolvedValue({ session_id: 'isid-2' });
		vi.spyOn(interpreterApi, 'uploadFile').mockResolvedValue({
			session_id: 'isid-2',
			file: { name: 'report.txt', size_bytes: 4, modified_at: 1 }
		});
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's-x',
			createdAt: '2026-06-06T09:00:00Z'
		});
		const sendSpy = vi
			.spyOn(agentApi, 'streamMessage')
			.mockImplementation(async (_s, _c, handlers) => {
				handlers.onDone({
					id: 'm', sessionId: 's-x', role: 'assistant', content: 'ok',
					toolCalls: [], toolCallId: null, tokensIn: 0, tokensOut: 0, model: null,
					createdAt: '2026-06-06T09:00:01Z'
				});
			});
		const vm = createAgentVM();
		await vm.attachFile(new File(['x'], 'report.txt'));
		await vm.send();
		expect(sendSpy.mock.calls[0][1]).toContain('report.txt');
		expect(vm.bubbles[0].content).toContain('report.txt');
	});
});
