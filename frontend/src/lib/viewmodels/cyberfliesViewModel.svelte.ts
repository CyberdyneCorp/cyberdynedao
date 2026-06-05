/**
 * Cyberflies (meetings) view-model.
 *
 * Owns three concerns for the Cyberflies app:
 *   1. Recordings — list past meetings, upload audio, drill into one.
 *   2. Async processing — an upload returns a `pending` recording (202);
 *      we poll `getRecording` until the status is terminal so the
 *      transcript/summary appear without a manual reload.
 *   3. Chat — ask questions over all meetings (`/chat`) or scoped to a
 *      single channel (`/channels/{id}/chat`), keeping a running message
 *      history the backend sees on each turn.
 *
 * The poll interval is injectable so tests can drive the loop fast.
 */

import {
	listRecordings,
	getRecording,
	deleteRecording,
	uploadRecording,
	fetchAudioFile,
	listChannels,
	createChannel as createChannelApi,
	deleteChannel as deleteChannelApi,
	addRecordingToChannel,
	removeRecordingFromChannel,
	listChannelRecordings,
	generateChannelRecap,
	chat as chatAll,
	chatInChannel,
	chatInRecording,
	joinMeeting as joinMeetingApi,
	listMeetingSessions,
	getMeetingSession,
	isTerminalStatus,
	isTerminalMeetingStatus,
	CyberfliesApiError,
	type RecordingResponse,
	type ChannelResponse,
	type SummarySchema,
	type ChatMessage,
	type MeetingSession,
	type MeetingPlatform,
	type JoinMeetingRequest
} from '$lib/api/cyberfliesApi';

/**
 * Chat scope, encoded as a string so it round-trips through a `<select>`:
 *   - `'all'`            → every meeting (`POST /chat`)
 *   - `'channel:<id>'`   → one channel  (`POST /channels/{id}/chat`)
 *   - `'recording:<id>'` → one meeting  (`POST /recordings/{id}/chat`)
 */
export type ChatScope = 'all' | `channel:${string}` | `recording:${string}`;

/** A single chat turn as rendered in the panel. */
export interface ChatTurn {
	role: 'user' | 'assistant';
	content: string;
	/** Tools the backend used to answer — only set on assistant turns. */
	usedTools?: string[];
}

export interface CyberfliesViewModel {
	readonly recordings: RecordingResponse[];
	readonly selectedId: string | null;
	readonly selectedRecording: RecordingResponse | null;
	readonly loading: boolean;
	readonly uploading: boolean;
	readonly error: string | null;

	readonly channels: ChannelResponse[];
	readonly chatScope: ChatScope;
	readonly chatTurns: ChatTurn[];
	readonly chatSending: boolean;
	readonly chatError: string | null;

	/** True while a delete/organize action is in flight. */
	readonly busy: boolean;
	/** Transient confirmation for the last organize action (e.g. "Added to Standups"). */
	readonly notice: string | null;

	/** Channels tab: currently-expanded channel + its lazily-loaded contents/recap. */
	readonly expandedChannelId: string | null;
	readonly channelRecordings: RecordingResponse[];
	readonly channelContentsLoading: boolean;
	readonly channelRecap: SummarySchema | null;
	readonly recapLoading: boolean;

	/** Bot tab: meeting-capture sessions. */
	readonly meetingSessions: MeetingSession[];
	readonly sessionsLoading: boolean;
	readonly sendingBot: boolean;
	readonly botError: string | null;

	refreshRecordings(): Promise<void>;
	refreshChannels(): Promise<void>;
	refreshMeetingSessions(): Promise<void>;
	joinMeeting(req: JoinMeetingRequest): Promise<void>;
	selectRecording(id: string | null): void;
	uploadAudio(file: File): Promise<void>;
	/** Stream the original audio/video through the API and save it. */
	downloadAudio(id: string): Promise<void>;
	/** Delete a recording and drop it from the list. */
	deleteRecording(id: string): Promise<void>;

	/** Create a channel and add it to the list; returns it (or null on failure). */
	createChannel(name: string, description?: string): Promise<ChannelResponse | null>;
	/** Delete a channel and drop it from the list. */
	deleteChannel(channelId: string): Promise<void>;
	/** Add a recording to an existing channel. */
	addToChannel(recordingId: string, channelId: string): Promise<void>;
	/** Expand/collapse a channel, loading its recordings on expand. */
	toggleChannel(channelId: string): Promise<void>;
	/** Generate (and store) an AI recap for a channel. */
	recapChannel(channelId: string): Promise<void>;
	/** Remove a recording from a channel (keeps the recording). */
	removeFromChannel(channelId: string, recordingId: string): Promise<void>;
	clearNotice(): void;

	setChatScope(scope: ChatScope): void;
	sendChat(text: string): Promise<void>;

	/** Stop all in-flight polling — call from the view's onDestroy. */
	destroy(): void;
}

const DEFAULT_POLL_INTERVAL_MS = 4000;
/** Stop polling after this many attempts so a stuck recording can't loop
 *  forever (≈ 5 min at the 4 s default). */
const MAX_POLL_ATTEMPTS = 75;

export function createCyberfliesVM(
	pollIntervalMs: number = DEFAULT_POLL_INTERVAL_MS
): CyberfliesViewModel {
	let recordings = $state<RecordingResponse[]>([]);
	let selectedId = $state<string | null>(null);
	let loading = $state<boolean>(false);
	let uploading = $state<boolean>(false);
	let error = $state<string | null>(null);

	let channels = $state<ChannelResponse[]>([]);
	let chatScope = $state<ChatScope>('all');
	let chatTurns = $state<ChatTurn[]>([]);
	let chatSending = $state<boolean>(false);
	let chatError = $state<string | null>(null);

	let busy = $state<boolean>(false);
	let notice = $state<string | null>(null);

	// Meeting-capture bot sessions.
	let meetingSessions = $state<MeetingSession[]>([]);
	let sessionsLoading = $state<boolean>(false);
	let sendingBot = $state<boolean>(false);
	let botError = $state<string | null>(null);

	// Channels tab: the currently-expanded channel and its lazily-loaded
	// contents / recap.
	let expandedChannelId = $state<string | null>(null);
	let channelRecordings = $state<RecordingResponse[]>([]);
	let channelContentsLoading = $state<boolean>(false);
	let channelRecap = $state<SummarySchema | null>(null);
	let recapLoading = $state<boolean>(false);

	// Recordings currently being polled, plus a kill switch for onDestroy.
	const polling = new Set<string>();
	let destroyed = false;

	function toMessage(err: unknown): string {
		if (err instanceof CyberfliesApiError) {
			return `${err.status === 401 ? 'Sign in required — ' : ''}${err.message}`;
		}
		return err instanceof Error ? err.message : String(err);
	}

	function upsertRecording(rec: RecordingResponse): void {
		const idx = recordings.findIndex((r) => r.id === rec.id);
		if (idx === -1) {
			recordings = [rec, ...recordings];
		} else {
			recordings = recordings.map((r) => (r.id === rec.id ? rec : r));
		}
	}

	function upsertMeetingSession(session: MeetingSession): void {
		const idx = meetingSessions.findIndex((s) => s.id === session.id);
		if (idx === -1) {
			meetingSessions = [session, ...meetingSessions];
		} else {
			meetingSessions = meetingSessions.map((s) => (s.id === session.id ? session : s));
		}
	}

	const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

	const meetingPolling = new Set<string>();
	async function pollMeetingUntilTerminal(id: string): Promise<void> {
		if (meetingPolling.has(id)) return;
		meetingPolling.add(id);
		try {
			for (let attempt = 0; attempt < MAX_POLL_ATTEMPTS; attempt++) {
				if (destroyed) return;
				await sleep(pollIntervalMs);
				if (destroyed) return;
				try {
					const session = await getMeetingSession(id);
					upsertMeetingSession(session);
					if (isTerminalMeetingStatus(session.status)) {
						// Once the bot's capture is ingested, the produced
						// recording shows up in the meetings list — refresh so
						// "View recording" resolves.
						if (session.status.toLowerCase() === 'completed' && session.recording_id) {
							void refreshRecordings();
						}
						return;
					}
				} catch (err) {
					botError = toMessage(err);
				}
			}
		} finally {
			meetingPolling.delete(id);
		}
	}

	async function pollUntilTerminal(id: string): Promise<void> {
		if (polling.has(id)) return;
		polling.add(id);
		try {
			for (let attempt = 0; attempt < MAX_POLL_ATTEMPTS; attempt++) {
				if (destroyed) return;
				await sleep(pollIntervalMs);
				if (destroyed) return;
				try {
					const rec = await getRecording(id);
					upsertRecording(rec);
					if (isTerminalStatus(rec.status)) return;
				} catch (err) {
					// Transient errors shouldn't kill the loop, but surface
					// the most recent one so the user isn't left guessing.
					error = toMessage(err);
				}
			}
		} finally {
			polling.delete(id);
		}
	}

	async function refreshRecordings(): Promise<void> {
		loading = true;
		try {
			const res = await listRecordings();
			recordings = res.items;
			error = null;
			// Resume polling for anything still processing after a reload.
			for (const r of res.items) {
				if (!isTerminalStatus(r.status)) void pollUntilTerminal(r.id);
			}
		} catch (err) {
			error = toMessage(err);
		} finally {
			loading = false;
		}
	}

	async function refreshChannels(): Promise<void> {
		try {
			const res = await listChannels();
			channels = res.items;
		} catch (err) {
			// Channels are optional context for the chat scope selector;
			// don't clobber the recordings error banner over it.
			chatError = toMessage(err);
		}
	}

	async function refreshMeetingSessions(): Promise<void> {
		sessionsLoading = true;
		try {
			const res = await listMeetingSessions();
			meetingSessions = res.items;
			botError = null;
			// Resume polling any bot still in flight after a reload.
			for (const s of res.items) {
				if (!isTerminalMeetingStatus(s.status)) void pollMeetingUntilTerminal(s.id);
			}
		} catch (err) {
			botError = toMessage(err);
		} finally {
			sessionsLoading = false;
		}
	}

	async function joinMeeting(req: JoinMeetingRequest): Promise<void> {
		if (sendingBot) return;
		if (!req.meeting_url.trim()) {
			botError = 'A meeting URL is required.';
			return;
		}
		sendingBot = true;
		try {
			const session = await joinMeetingApi({
				platform: req.platform,
				meeting_url: req.meeting_url.trim(),
				bot_display_name: req.bot_display_name?.trim() || undefined,
				consent_message: req.consent_message?.trim() || undefined
			});
			upsertMeetingSession(session);
			botError = null;
			if (!isTerminalMeetingStatus(session.status)) void pollMeetingUntilTerminal(session.id);
		} catch (err) {
			botError = toMessage(err);
		} finally {
			sendingBot = false;
		}
	}

	async function uploadAudio(file: File): Promise<void> {
		if (uploading) return;
		uploading = true;
		try {
			const rec = await uploadRecording(file, { device: 'web' });
			upsertRecording(rec);
			selectedId = rec.id;
			error = null;
			if (!isTerminalStatus(rec.status)) void pollUntilTerminal(rec.id);
		} catch (err) {
			error = toMessage(err);
		} finally {
			uploading = false;
		}
	}

	async function downloadAudio(id: string): Promise<void> {
		try {
			const { blob, filename } = await fetchAudioFile(id);
			// Save the streamed blob via a transient object URL + hidden
			// anchor (same pattern as the interpreter file download).
			const url = URL.createObjectURL(blob);
			const anchor = document.createElement('a');
			anchor.href = url;
			anchor.download = filename;
			document.body.appendChild(anchor);
			anchor.click();
			document.body.removeChild(anchor);
			setTimeout(() => URL.revokeObjectURL(url), 30_000);
			error = null;
		} catch (err) {
			error = toMessage(err);
		}
	}

	async function deleteRecording_(id: string): Promise<void> {
		if (busy) return;
		busy = true;
		try {
			await deleteRecording(id);
			recordings = recordings.filter((r) => r.id !== id);
			if (selectedId === id) selectedId = null;
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			busy = false;
		}
	}

	async function createChannel_(
		name: string,
		description?: string
	): Promise<ChannelResponse | null> {
		const trimmed = name.trim();
		if (trimmed === '') return null;
		busy = true;
		try {
			const channel = await createChannelApi(trimmed, description?.trim() || undefined);
			channels = [...channels, channel];
			notice = `Channel "${channel.name}" created`;
			error = null;
			return channel;
		} catch (err) {
			error = toMessage(err);
			return null;
		} finally {
			busy = false;
		}
	}

	async function deleteChannel_(channelId: string): Promise<void> {
		if (busy) return;
		busy = true;
		try {
			await deleteChannelApi(channelId);
			channels = channels.filter((c) => c.id !== channelId);
			// If the chat was scoped to this channel, fall back to "all".
			if (chatScope === `channel:${channelId}`) chatScope = 'all';
			if (expandedChannelId === channelId) expandedChannelId = null;
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			busy = false;
		}
	}

	async function addToChannel(recordingId: string, channelId: string): Promise<void> {
		if (busy) return;
		busy = true;
		try {
			await addRecordingToChannel(channelId, recordingId);
			const name = channels.find((c) => c.id === channelId)?.name ?? 'channel';
			notice = `Added to ${name}`;
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			busy = false;
		}
	}

	async function toggleChannel(channelId: string): Promise<void> {
		// Collapse if it's already open.
		if (expandedChannelId === channelId) {
			expandedChannelId = null;
			return;
		}
		expandedChannelId = channelId;
		channelRecordings = [];
		channelRecap = null;
		channelContentsLoading = true;
		try {
			const res = await listChannelRecordings(channelId);
			channelRecordings = res.items;
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			channelContentsLoading = false;
		}
	}

	async function recapChannel(channelId: string): Promise<void> {
		if (recapLoading) return;
		expandedChannelId = channelId;
		recapLoading = true;
		try {
			channelRecap = await generateChannelRecap(channelId);
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			recapLoading = false;
		}
	}

	async function removeFromChannel(channelId: string, recordingId: string): Promise<void> {
		if (busy) return;
		busy = true;
		try {
			await removeRecordingFromChannel(channelId, recordingId);
			if (expandedChannelId === channelId) {
				channelRecordings = channelRecordings.filter((r) => r.id !== recordingId);
			}
			notice = 'Removed from channel';
			error = null;
		} catch (err) {
			error = toMessage(err);
		} finally {
			busy = false;
		}
	}

	async function sendChat(text: string): Promise<void> {
		const trimmed = text.trim();
		if (trimmed === '' || chatSending) return;
		chatSending = true;
		chatError = null;
		chatTurns = [...chatTurns, { role: 'user', content: trimmed }];
		// The backend wants the full running history (role/content only).
		const history: ChatMessage[] = chatTurns.map((t) => ({
			role: t.role,
			content: t.content
		}));
		try {
			let reply;
			if (chatScope === 'all') {
				reply = await chatAll(history);
			} else if (chatScope.startsWith('recording:')) {
				reply = await chatInRecording(chatScope.slice('recording:'.length), history);
			} else {
				reply = await chatInChannel(chatScope.slice('channel:'.length), history);
			}
			chatTurns = [
				...chatTurns,
				{ role: 'assistant', content: reply.reply, usedTools: reply.used_tools }
			];
		} catch (err) {
			chatError = toMessage(err);
		} finally {
			chatSending = false;
		}
	}

	return {
		get recordings() {
			return recordings;
		},
		get selectedId() {
			return selectedId;
		},
		get selectedRecording() {
			return recordings.find((r) => r.id === selectedId) ?? null;
		},
		get loading() {
			return loading;
		},
		get uploading() {
			return uploading;
		},
		get error() {
			return error;
		},
		get channels() {
			return channels;
		},
		get chatScope() {
			return chatScope;
		},
		get chatTurns() {
			return chatTurns;
		},
		get chatSending() {
			return chatSending;
		},
		get chatError() {
			return chatError;
		},
		get busy() {
			return busy;
		},
		get notice() {
			return notice;
		},
		get expandedChannelId() {
			return expandedChannelId;
		},
		get channelRecordings() {
			return channelRecordings;
		},
		get channelContentsLoading() {
			return channelContentsLoading;
		},
		get channelRecap() {
			return channelRecap;
		},
		get recapLoading() {
			return recapLoading;
		},
		get meetingSessions() {
			return meetingSessions;
		},
		get sessionsLoading() {
			return sessionsLoading;
		},
		get sendingBot() {
			return sendingBot;
		},
		get botError() {
			return botError;
		},
		refreshRecordings,
		refreshChannels,
		refreshMeetingSessions,
		joinMeeting,
		selectRecording: (id) => {
			selectedId = id;
		},
		uploadAudio,
		downloadAudio,
		deleteRecording: deleteRecording_,
		createChannel: createChannel_,
		deleteChannel: deleteChannel_,
		addToChannel,
		toggleChannel,
		recapChannel,
		removeFromChannel,
		clearNotice: () => {
			notice = null;
		},
		setChatScope: (scope) => {
			chatScope = scope;
		},
		sendChat,
		destroy: () => {
			destroyed = true;
			polling.clear();
			meetingPolling.clear();
		}
	};
}
