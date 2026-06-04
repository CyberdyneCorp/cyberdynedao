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
	/** Artifact filename in the MATLAB workspace (e.g. plot_abc.png). */
	artifactPath: string;
	/** The agent's MATLAB session (agent-<chatSessionId>) the figure
	 *  lives in. The view downloads it via the authed /api/matlab proxy. */
	sessionId: string;
	caption: string;
}

/** A downloadable file the agent produced via python_exec / create_document. */
export interface AgentArtifact {
	/** Filename in the interpreter workspace (e.g. summary.md, report.pdf). */
	name: string;
	/** The interpreter session the file lives in. Downloaded via the
	 *  authed /api/interpreter proxy. */
	sessionId: string;
	sizeBytes: number;
}

export interface AgentBubble {
	id: string;
	role: 'user' | 'assistant';
	content: string;
	toolCalls: AgentToolCall[];
	/** Figures produced by matlab_plot/matlab_repl tool calls made by
	 *  this assistant turn, captured inline so they survive a refresh. */
	plots: AgentPlot[];
	/** Downloadable files produced by python_exec / create_document. */
	artifacts: AgentArtifact[];
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
		artifacts: [],
		model: m.model,
		createdAt: m.createdAt,
		pending: false,
		error: null
	};
}

/** Pull figure references out of a matlab tool-result JSON. */
function extractPlots(toolResultContent: string): AgentPlot[] {
	try {
		const parsed = JSON.parse(toolResultContent) as {
			figures?: string[];
			session_id?: string;
		};
		const figures = parsed.figures ?? [];
		const sessionId = parsed.session_id ?? '';
		if (!figures.length || !sessionId) return [];
		return figures.map((artifactPath, i) => ({
			artifactPath,
			sessionId,
			caption: figures.length > 1 ? `MATLAB figure ${i + 1}` : 'MATLAB figure'
		}));
	} catch {
		return [];
	}
}

/** Image extensions already rendered inline as plots — don't also list
 *  them as downloadable files. */
const IMAGE_EXT = /\.(png|jpe?g|svg|gif|webp)$/i;

/** Pull downloadable file references out of a python_exec / create_document
 *  tool-result JSON (`{session_id, artifacts: [{name,size_bytes,...}]}`). */
function extractArtifacts(toolResultContent: string): AgentArtifact[] {
	try {
		const parsed = JSON.parse(toolResultContent) as {
			session_id?: string;
			filename?: string;
			artifacts?: Array<{ name?: string; size_bytes?: number }>;
		};
		const sessionId = parsed.session_id ?? '';
		if (!sessionId) return [];
		// create_document returns a single {filename}; python_exec returns an
		// artifacts[] workspace listing.
		const entries = parsed.artifacts?.length
			? parsed.artifacts
			: parsed.filename
				? [{ name: parsed.filename, size_bytes: 0 }]
				: [];
		return entries
			.map((a) => ({ name: a.name ?? '', sizeBytes: a.size_bytes ?? 0, sessionId }))
			.filter((a) => a.name && !IMAGE_EXT.test(a.name));
	} catch {
		return [];
	}
}

/**
 * Build the visible bubble list from a full message history.
 *
 * A tool-using turn produces several backend messages: an intermediate
 * assistant message that *only* carries tool_calls (empty text), the
 * tool result messages, then the final assistant message with the
 * actual text reply. We don't want to render the empty intermediate
 * bubble, and the figure should land on the final text bubble — so we
 * accumulate figures as we walk the turn and flush them onto the next
 * assistant message that actually has content.
 */
function bubblesFromMessages(messages: AgentMessage[]): AgentBubble[] {
	const toolResultsById = new Map<string, AgentMessage>();
	for (const m of messages) {
		if (m.role === 'tool' && m.toolCallId) toolResultsById.set(m.toolCallId, m);
	}
	const out: AgentBubble[] = [];
	let pendingPlots: AgentPlot[] = [];
	let pendingArtifacts: AgentArtifact[] = [];
	for (const m of messages) {
		if (m.role === 'tool' || m.role === 'system') continue;
		if (m.role === 'assistant') {
			// Collect figures + files from any tool calls this message made.
			for (const tc of m.toolCalls ?? []) {
				const res = toolResultsById.get(tc.id);
				if (res) {
					pendingPlots.push(...extractPlots(res.content));
					pendingArtifacts.push(...extractArtifacts(res.content));
				}
			}
			// Skip the empty tool-call-only round; keep its figures/files
			// pending for the final text bubble.
			if (m.content.trim() === '') continue;
			const bubble = toBubble(m);
			bubble.plots = pendingPlots;
			bubble.artifacts = dedupeArtifacts(pendingArtifacts);
			pendingPlots = [];
			pendingArtifacts = [];
			out.push(bubble);
		} else {
			out.push(toBubble(m));
		}
	}
	// Figures/files with no trailing text bubble (rare) — attach to the
	// last assistant bubble so they aren't lost.
	if (pendingPlots.length || pendingArtifacts.length) {
		const lastAssistant = [...out].reverse().find((b) => b.role === 'assistant');
		if (lastAssistant) {
			lastAssistant.plots = [...lastAssistant.plots, ...pendingPlots];
			lastAssistant.artifacts = dedupeArtifacts([
				...lastAssistant.artifacts,
				...pendingArtifacts
			]);
		}
	}
	return out;
}

/** python_exec returns the whole workspace listing each turn, so the same
 *  file can appear across calls — keep the last occurrence per name+session. */
function dedupeArtifacts(artifacts: AgentArtifact[]): AgentArtifact[] {
	const byKey = new Map<string, AgentArtifact>();
	for (const a of artifacts) byKey.set(`${a.sessionId}/${a.name}`, a);
	return [...byKey.values()];
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
			artifacts: [],
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
			artifacts: [],
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
			// The send response is only the FINAL assistant message — and
			// on a tool-using turn that message has empty tool_calls (the
			// calls live on an earlier intermediate message). So we can't
			// tell from the reply whether a figure was produced. Re-read
			// the full history so any matlab figures attach to their
			// bubble. The text is already shown via the patch above, so
			// this just enriches; failure is non-fatal.
			try {
				const remote = await getHistory(sid);
				bubbles = bubblesFromMessages(remote.messages);
				persist();
			} catch {
				/* keep optimistic bubbles on refresh failure */
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
