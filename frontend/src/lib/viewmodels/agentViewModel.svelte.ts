/**
 * Cyberdyne agent VM — manages the chat session and message log.
 *
 * Persistence: sessionStorage under `cyberdyne.agent.v1`. Refresh
 * preserves session_id + visible message log so a conversation
 * survives navigation. Tab close clears it on purpose (same pattern
 * as authVM); for cross-tab persistence we'd move to localStorage.
 *
 * The backend's chat endpoint is non-streaming: one POST returns the
 * final assistant message after all tool rounds. We optimistic-append
 * the user message immediately and add a placeholder "thinking…"
 * assistant cell, then patch it in once the response lands.
 */

import {
	AgentApiError,
	getHistory,
	sendMessage,
	startSession,
	type AgentMessage,
	type AgentToolCall
} from '$lib/api/agentApi';

const STORAGE_KEY = 'cyberdyne.agent.v1';

export interface AgentPlot {
	/** data: URL (base64 PNG) — renderable directly in an <img src>. */
	dataUrl: string;
	caption: string;
}

export interface AgentBubble {
	id: string;
	role: 'user' | 'assistant';
	content: string;
	toolCalls: AgentToolCall[];
	/** Figures produced by matlab_plot/matlab_repl tool calls made by
	 *  this assistant turn, captured inline so they survive a refresh. */
	plots: AgentPlot[];
	model: string | null;
	createdAt: string;
	pending: boolean;
	error: string | null;
}

interface Persisted {
	sessionId: string;
	bubbles: AgentBubble[];
}

function nowIso(): string {
	return new Date().toISOString();
}

function localId(prefix: string): string {
	if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
		return `${prefix}-${crypto.randomUUID()}`;
	}
	return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function read(): Persisted | null {
	if (typeof sessionStorage === 'undefined') return null;
	try {
		const raw = sessionStorage.getItem(STORAGE_KEY);
		if (!raw) return null;
		const parsed = JSON.parse(raw) as Persisted;
		if (typeof parsed.sessionId !== 'string' || !Array.isArray(parsed.bubbles)) return null;
		return parsed;
	} catch {
		return null;
	}
}

function write(p: Persisted): void {
	if (typeof sessionStorage === 'undefined') return;
	try {
		sessionStorage.setItem(STORAGE_KEY, JSON.stringify(p));
	} catch {
		/* quota / private mode — non-fatal */
	}
}

function wipe(): void {
	if (typeof sessionStorage === 'undefined') return;
	try {
		sessionStorage.removeItem(STORAGE_KEY);
	} catch {
		/* ignore */
	}
}

/**
 * Map a backend AgentMessage → display bubble. Tool + system roles
 * are filtered out at the call site; this only handles user +
 * assistant.
 */
function toBubble(m: AgentMessage): AgentBubble {
	return {
		id: m.id,
		role: m.role === 'assistant' ? 'assistant' : 'user',
		content: m.content,
		toolCalls: m.toolCalls ?? [],
		plots: [],
		model: m.model,
		createdAt: m.createdAt,
		pending: false,
		error: null
	};
}

/** Pull an inline figure out of a matlab tool-result JSON, if present. */
function extractPlot(toolResultContent: string): AgentPlot | null {
	try {
		const parsed = JSON.parse(toolResultContent) as {
			image_base64?: string;
			image_content_type?: string;
		};
		if (!parsed.image_base64) return null;
		const ct = parsed.image_content_type || 'image/png';
		return {
			dataUrl: `data:${ct};base64,${parsed.image_base64}`,
			caption: 'MATLAB figure'
		};
	} catch {
		return null;
	}
}

/**
 * Build the visible bubble list from a full message history. Tool
 * messages aren't rendered as their own bubbles, but their results
 * are mined for inline figures and attached to the assistant turn
 * that called them (matched by tool_call_id).
 */
function bubblesFromMessages(messages: AgentMessage[]): AgentBubble[] {
	const toolResultsById = new Map<string, AgentMessage>();
	for (const m of messages) {
		if (m.role === 'tool' && m.toolCallId) toolResultsById.set(m.toolCallId, m);
	}
	const out: AgentBubble[] = [];
	for (const m of messages) {
		if (m.role !== 'user' && m.role !== 'assistant') continue;
		const bubble = toBubble(m);
		if (m.role === 'assistant') {
			for (const tc of bubble.toolCalls) {
				const res = toolResultsById.get(tc.id);
				if (!res) continue;
				const plot = extractPlot(res.content);
				if (plot) bubble.plots.push(plot);
			}
		}
		out.push(bubble);
	}
	return out;
}

export interface AgentViewModel {
	readonly sessionId: string | null;
	readonly bubbles: AgentBubble[];
	readonly input: string;
	readonly running: boolean;
	readonly error: string | null;
	readonly bootstrapped: boolean;
	bootstrap(): Promise<void>;
	setInput(value: string): void;
	send(): Promise<void>;
	resetSession(): Promise<void>;
	clearError(): void;
}

export function createAgentVM(): AgentViewModel {
	let sessionId = $state<string | null>(null);
	let bubbles = $state<AgentBubble[]>([]);
	let input = $state<string>('');
	let running = $state<boolean>(false);
	let error = $state<string | null>(null);
	let bootstrapped = $state<boolean>(false);

	function persist(): void {
		if (sessionId !== null) {
			write({ sessionId, bubbles });
		}
	}

	function patchBubble(id: string, patch: Partial<AgentBubble>): void {
		bubbles = bubbles.map((b) => (b.id === id ? { ...b, ...patch } : b));
		persist();
	}

	async function ensureSession(): Promise<string> {
		if (sessionId !== null) return sessionId;
		const s = await startSession();
		sessionId = s.sessionId;
		persist();
		return sessionId;
	}

	async function bootstrap(): Promise<void> {
		if (bootstrapped) return;
		try {
			const persisted = read();
			if (persisted) {
				sessionId = persisted.sessionId;
				bubbles = persisted.bubbles;
				// Try to refresh the history from the backend in case
				// another tab progressed the conversation. Failures
				// here are non-fatal — we keep the cached bubbles.
				try {
					const remote = await getHistory(persisted.sessionId);
					bubbles = bubblesFromMessages(remote.messages);
					persist();
				} catch {
					/* offline / 404 — keep local cache */
				}
			}
		} finally {
			bootstrapped = true;
		}
	}

	async function send(): Promise<void> {
		const text = input.trim();
		if (!text || running) return;
		running = true;
		error = null;
		input = '';

		const userBubble: AgentBubble = {
			id: localId('local-user'),
			role: 'user',
			content: text,
			toolCalls: [],
			plots: [],
			model: null,
			createdAt: nowIso(),
			pending: false,
			error: null
		};
		const assistantBubble: AgentBubble = {
			id: localId('local-assistant'),
			role: 'assistant',
			content: '',
			toolCalls: [],
			plots: [],
			model: null,
			createdAt: nowIso(),
			pending: true,
			error: null
		};
		bubbles = [...bubbles, userBubble, assistantBubble];
		persist();

		try {
			const sid = await ensureSession();
			const reply = await sendMessage(sid, text);
			patchBubble(assistantBubble.id, {
				id: reply.id,
				content: reply.content || '(no response)',
				toolCalls: reply.toolCalls ?? [],
				model: reply.model,
				createdAt: reply.createdAt,
				pending: false
			});
			// The send response is just the final assistant message —
			// it doesn't carry the intermediate tool results (where the
			// figures live). If this turn used tools, re-read history so
			// any matlab_plot images attach to their bubble.
			if ((reply.toolCalls ?? []).length > 0) {
				try {
					const remote = await getHistory(sid);
					bubbles = bubblesFromMessages(remote.messages);
					persist();
				} catch {
					/* keep optimistic bubbles on refresh failure */
				}
			}
		} catch (err) {
			const message =
				err instanceof AgentApiError
					? `${err.status === 401 ? 'Sign in required — ' : ''}${err.message}`
					: err instanceof Error
						? err.message
						: String(err);
			patchBubble(assistantBubble.id, {
				pending: false,
				error: message
			});
			error = message;
		} finally {
			running = false;
		}
	}

	async function resetSession(): Promise<void> {
		sessionId = null;
		bubbles = [];
		input = '';
		error = null;
		wipe();
		// Spawn a fresh session eagerly so the next send is one round-
		// trip, not two. Failure here is non-fatal — `send()` will
		// retry on demand.
		try {
			await ensureSession();
		} catch {
			/* deferred to next send() */
		}
	}

	return {
		get sessionId() { return sessionId; },
		get bubbles() { return bubbles; },
		get input() { return input; },
		get running() { return running; },
		get error() { return error; },
		get bootstrapped() { return bootstrapped; },
		bootstrap,
		setInput: (value) => {
			input = value;
		},
		send,
		resetSession,
		clearError: () => {
			error = null;
		}
	};
}
