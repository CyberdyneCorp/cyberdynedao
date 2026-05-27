import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createAgentVM } from '../agentViewModel.svelte';
import * as agentApi from '$lib/api/agentApi';

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

	it('send creates a session on first call and persists bubbles', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's-new',
			createdAt: '2026-05-26T09:00:00Z'
		});
		vi.spyOn(agentApi, 'sendMessage').mockResolvedValue({
			id: 'm-r',
			sessionId: 's-new',
			role: 'assistant',
			content: 'pong',
			toolCalls: [],
			toolCallId: null,
			tokensIn: 1,
			tokensOut: 1,
			model: 'gpt-4o-mini',
			createdAt: '2026-05-26T09:00:01Z'
		});
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

	it('send surfaces 401 with a "Sign in required" prefix', async () => {
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's',
			createdAt: ''
		});
		vi.spyOn(agentApi, 'sendMessage').mockRejectedValue(
			new agentApi.AgentApiError(401, 'authentication required')
		);
		const vm = createAgentVM();
		vm.setInput('hi');
		await vm.send();
		const assistantBubble = vm.bubbles[vm.bubbles.length - 1];
		expect(assistantBubble.error).toMatch(/Sign in required/);
		expect(vm.error).toMatch(/Sign in required/);
	});

	it('resetSession clears bubbles + storage and starts a fresh session', async () => {
		const startSpy = vi
			.spyOn(agentApi, 'startSession')
			.mockResolvedValueOnce({ sessionId: 's-1', createdAt: '' })
			.mockResolvedValueOnce({ sessionId: 's-2', createdAt: '' });
		vi.spyOn(agentApi, 'sendMessage').mockResolvedValue({
			id: 'm',
			sessionId: 's-1',
			role: 'assistant',
			content: 'ok',
			toolCalls: [],
			toolCallId: null,
			tokensIn: 0,
			tokensOut: 0,
			model: null,
			createdAt: ''
		});
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
		let resolveSend!: (v: agentApi.AgentMessage) => void;
		vi.spyOn(agentApi, 'startSession').mockResolvedValue({
			sessionId: 's',
			createdAt: ''
		});
		const sendSpy = vi.spyOn(agentApi, 'sendMessage').mockImplementation(
			() => new Promise((r) => (resolveSend = r))
		);
		const vm = createAgentVM();
		vm.setInput('first');
		const inflight = vm.send();
		expect(vm.running).toBe(true);
		// Let the first send's ``await ensureSession()`` flush so
		// sendMessage actually fires and resolveSend gets assigned.
		await new Promise((r) => setTimeout(r, 0));
		expect(sendSpy).toHaveBeenCalledTimes(1);
		vm.setInput('second');
		await vm.send();
		// The running-guard short-circuited; sendMessage still called once.
		expect(sendSpy).toHaveBeenCalledTimes(1);
		expect(vm.bubbles.length).toBe(2);
		resolveSend({
			id: 'm',
			sessionId: 's',
			role: 'assistant',
			content: 'ok',
			toolCalls: [],
			toolCallId: null,
			tokensIn: 0,
			tokensOut: 0,
			model: null,
			createdAt: ''
		});
		await inflight;
		expect(vm.running).toBe(false);
	});
});
