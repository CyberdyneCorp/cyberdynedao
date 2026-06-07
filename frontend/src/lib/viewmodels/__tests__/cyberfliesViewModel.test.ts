import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createCyberfliesVM } from '../cyberfliesViewModel.svelte';
import * as cyberfliesApi from '$lib/api/cyberfliesApi';
import type {
	ChannelResponse,
	MeetingSession,
	RecordingResponse
} from '$lib/api/cyberfliesApi';

function session(over: Partial<MeetingSession> = {}): MeetingSession {
	return {
		id: 'sess-1',
		owner_id: 'u-1',
		platform: 'google_meet',
		meeting_url: 'https://meet.google.com/abc',
		status: 'scheduled',
		created_at: '2026-06-05T10:00:00Z',
		updated_at: '2026-06-05T10:00:00Z',
		...over
	};
}

function channel(over: Partial<ChannelResponse> = {}): ChannelResponse {
	return {
		id: 'chan-1',
		owner_id: 'u-1',
		name: 'Standups',
		created_at: '2026-06-01T00:00:00Z',
		updated_at: '2026-06-01T00:00:00Z',
		...over
	};
}

function recording(over: Partial<RecordingResponse> = {}): RecordingResponse {
	return {
		id: 'rec-1',
		owner_id: 'u-1',
		status: 'completed',
		audio_format: 'm4a',
		size_bytes: 1024,
		created_at: '2026-06-01T10:00:00Z',
		updated_at: '2026-06-01T10:01:00Z',
		...over
	};
}

const flush = (ms = 0) => new Promise((r) => setTimeout(r, ms));

afterEach(() => {
	vi.restoreAllMocks();
});

describe('cyberfliesViewModel', () => {
	it('refreshRecordings populates the list and clears error', async () => {
		vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
			items: [recording(), recording({ id: 'rec-2' })],
			limit: 50,
			offset: 0
		});
		const vm = createCyberfliesVM(1);
		await vm.refreshRecordings();
		expect(vm.recordings).toHaveLength(2);
		expect(vm.error).toBe(null);
	});

	it('refreshRecordings surfaces a 401 with the sign-in prefix', async () => {
		vi.spyOn(cyberfliesApi, 'listRecordings').mockRejectedValue(
			new cyberfliesApi.CyberfliesApiError(401, 'no token')
		);
		const vm = createCyberfliesVM(1);
		await vm.refreshRecordings();
		expect(vm.error).toMatch(/Sign in required/);
		expect(vm.error).toMatch(/no token/);
	});

	it('selectRecording exposes the matching record via selectedRecording', async () => {
		vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
			items: [recording(), recording({ id: 'rec-2', status: 'completed' })],
			limit: 50,
			offset: 0
		});
		const vm = createCyberfliesVM(1);
		await vm.refreshRecordings();
		vm.selectRecording('rec-2');
		expect(vm.selectedId).toBe('rec-2');
		expect(vm.selectedRecording?.id).toBe('rec-2');
		vm.selectRecording(null);
		expect(vm.selectedRecording).toBe(null);
	});

	it('uploadAudio inserts the recording, selects it, and polls until terminal', async () => {
		vi.spyOn(cyberfliesApi, 'uploadRecording').mockResolvedValue(
			recording({ id: 'rec-new', status: 'pending' })
		);
		vi.spyOn(cyberfliesApi, 'getRecording')
			.mockResolvedValueOnce(recording({ id: 'rec-new', status: 'processing' }))
			.mockResolvedValueOnce(
				recording({
					id: 'rec-new',
					status: 'completed',
					summary: { headline: 'Standup', abstract: 'We synced.', bullets: ['a', 'b'] }
				})
			);
		const vm = createCyberfliesVM(1);
		await vm.uploadAudio(new File(['audio'], 'meeting.m4a'));
		expect(vm.recordings[0].id).toBe('rec-new');
		expect(vm.selectedId).toBe('rec-new');
		// Let the poll loop run (1ms interval × 2 attempts).
		await flush(20);
		expect(vm.selectedRecording?.status).toBe('completed');
		expect(vm.selectedRecording?.summary?.headline).toBe('Standup');
	});

	it('does not poll when the upload comes back already terminal', async () => {
		vi.spyOn(cyberfliesApi, 'uploadRecording').mockResolvedValue(
			recording({ id: 'rec-done', status: 'completed' })
		);
		const getSpy = vi.spyOn(cyberfliesApi, 'getRecording');
		const vm = createCyberfliesVM(1);
		await vm.uploadAudio(new File(['a'], 'x.m4a'));
		await flush(20);
		expect(getSpy).not.toHaveBeenCalled();
	});

	it('uploadAudio surfaces upload errors', async () => {
		vi.spyOn(cyberfliesApi, 'uploadRecording').mockRejectedValue(new Error('bad format'));
		const vm = createCyberfliesVM(1);
		await vm.uploadAudio(new File(['a'], 'x.txt'));
		expect(vm.error).toMatch(/bad format/);
	});

	it('shows a non-401 ApiError message without the sign-in prefix', async () => {
		vi.spyOn(cyberfliesApi, 'listRecordings').mockRejectedValue(
			new cyberfliesApi.CyberfliesApiError(503, 'upstream down')
		);
		const vm = createCyberfliesVM(1);
		await vm.refreshRecordings();
		expect(vm.error).toBe('upstream down');
	});

	it('uploadAudio is a no-op while another upload is in flight', async () => {
		let resolveFirst!: (v: RecordingResponse) => void;
		const upSpy = vi
			.spyOn(cyberfliesApi, 'uploadRecording')
			.mockImplementationOnce(() => new Promise((res) => (resolveFirst = res)));
		const vm = createCyberfliesVM(1);
		const inflight = vm.uploadAudio(new File(['a'], 'a.m4a'));
		expect(vm.uploading).toBe(true);
		await vm.uploadAudio(new File(['b'], 'b.m4a')); // guarded no-op
		expect(upSpy).toHaveBeenCalledTimes(1);
		resolveFirst(recording({ id: 'rec-x', status: 'completed' }));
		await inflight;
		expect(vm.uploading).toBe(false);
	});

	it('refreshRecordings resumes polling for items still processing', async () => {
		vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
			items: [recording({ id: 'rec-proc', status: 'processing' })],
			limit: 50,
			offset: 0
		});
		const getSpy = vi
			.spyOn(cyberfliesApi, 'getRecording')
			.mockResolvedValue(recording({ id: 'rec-proc', status: 'completed' }));
		const vm = createCyberfliesVM(1);
		await vm.refreshRecordings();
		await flush(20);
		expect(getSpy).toHaveBeenCalledWith('rec-proc');
		expect(vm.recordings[0].status).toBe('completed');
	});

	it('keeps polling through a transient getRecording failure', async () => {
		vi.spyOn(cyberfliesApi, 'uploadRecording').mockResolvedValue(
			recording({ id: 'rec-t', status: 'pending' })
		);
		vi.spyOn(cyberfliesApi, 'getRecording')
			.mockRejectedValueOnce(new Error('blip'))
			.mockResolvedValueOnce(recording({ id: 'rec-t', status: 'completed' }));
		const vm = createCyberfliesVM(1);
		await vm.uploadAudio(new File(['a'], 'a.m4a'));
		await flush(30);
		expect(vm.recordings[0].status).toBe('completed');
	});

	it('destroy stops the poll loop', async () => {
		vi.spyOn(cyberfliesApi, 'uploadRecording').mockResolvedValue(
			recording({ id: 'rec-p', status: 'pending' })
		);
		const getSpy = vi
			.spyOn(cyberfliesApi, 'getRecording')
			.mockResolvedValue(recording({ id: 'rec-p', status: 'processing' }));
		const vm = createCyberfliesVM(1);
		await vm.uploadAudio(new File(['a'], 'x.m4a'));
		vm.destroy();
		await flush(20);
		// At most one in-flight getRecording may have been issued before
		// destroy took effect; it must not keep looping.
		expect(getSpy.mock.calls.length).toBeLessThanOrEqual(1);
	});

	describe('chat', () => {
		it('sendChat appends the user turn then the assistant reply (global scope)', async () => {
			const spy = vi
				.spyOn(cyberfliesApi, 'chat')
				.mockResolvedValue({ reply: 'Here is the summary.', used_tools: ['search'] });
			const vm = createCyberfliesVM(1);
			await vm.sendChat('summarize my meetings');
			expect(vm.chatTurns).toHaveLength(2);
			expect(vm.chatTurns[0]).toEqual({ role: 'user', content: 'summarize my meetings' });
			expect(vm.chatTurns[1].role).toBe('assistant');
			expect(vm.chatTurns[1].content).toBe('Here is the summary.');
			expect(vm.chatTurns[1].usedTools).toEqual(['search']);
			// The backend receives the running history.
			expect(spy.mock.calls[0][0]).toEqual([
				{ role: 'user', content: 'summarize my meetings' }
			]);
		});

		it('routes to the channel endpoint when scoped to a channel', async () => {
			const channelSpy = vi
				.spyOn(cyberfliesApi, 'chatInChannel')
				.mockResolvedValue({ reply: 'scoped', used_tools: [] });
			const globalSpy = vi.spyOn(cyberfliesApi, 'chat');
			const vm = createCyberfliesVM(1);
			vm.setChatScope('channel:chan-7');
			await vm.sendChat('what changed?');
			expect(channelSpy).toHaveBeenCalledWith('chan-7', [
				{ role: 'user', content: 'what changed?' }
			]);
			expect(globalSpy).not.toHaveBeenCalled();
		});

		it('routes to the single-meeting endpoint when scoped to a recording', async () => {
			const recSpy = vi
				.spyOn(cyberfliesApi, 'chatInRecording')
				.mockResolvedValue({ reply: 'about this meeting', used_tools: [] });
			const globalSpy = vi.spyOn(cyberfliesApi, 'chat');
			const channelSpy = vi.spyOn(cyberfliesApi, 'chatInChannel');
			const vm = createCyberfliesVM(1);
			vm.setChatScope('recording:rec-9');
			await vm.sendChat('what was this about?');
			expect(recSpy).toHaveBeenCalledWith('rec-9', [
				{ role: 'user', content: 'what was this about?' }
			]);
			expect(globalSpy).not.toHaveBeenCalled();
			expect(channelSpy).not.toHaveBeenCalled();
		});

		it('sendChat ignores empty input', async () => {
			const spy = vi.spyOn(cyberfliesApi, 'chat');
			const vm = createCyberfliesVM(1);
			await vm.sendChat('   ');
			expect(spy).not.toHaveBeenCalled();
			expect(vm.chatTurns).toEqual([]);
		});

		it('sendChat surfaces errors via chatError but keeps the user turn', async () => {
			vi.spyOn(cyberfliesApi, 'chat').mockRejectedValue(new Error('llm down'));
			const vm = createCyberfliesVM(1);
			await vm.sendChat('hi');
			expect(vm.chatError).toMatch(/llm down/);
			expect(vm.chatTurns).toHaveLength(1);
			expect(vm.chatTurns[0].role).toBe('user');
		});
	});

	it('refreshChannels surfaces errors via chatError', async () => {
		vi.spyOn(cyberfliesApi, 'listChannels').mockRejectedValue(new Error('no channels'));
		const vm = createCyberfliesVM(1);
		await vm.refreshChannels();
		expect(vm.chatError).toMatch(/no channels/);
	});

	it('refreshChannels populates the channel list', async () => {
		vi.spyOn(cyberfliesApi, 'listChannels').mockResolvedValue({
			items: [
				{
					id: 'c1',
					owner_id: 'u',
					name: 'Standups',
					created_at: '2026-06-01T00:00:00Z',
					updated_at: '2026-06-01T00:00:00Z'
				}
			],
			limit: 50,
			offset: 0
		});
		const vm = createCyberfliesVM(1);
		await vm.refreshChannels();
		expect(vm.channels).toHaveLength(1);
		expect(vm.channels[0].name).toBe('Standups');
	});

	describe('downloadAudio', () => {
		it('streams the file through the API and saves it via a hidden anchor', async () => {
			const blob = new Blob(['audio-bytes'], { type: 'audio/mp4' });
			vi.spyOn(cyberfliesApi, 'fetchAudioFile').mockResolvedValue({
				blob,
				filename: 'recording-rec-1.m4a',
				contentType: 'audio/mp4'
			});
			const createSpy = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:mock');
			const clickSpy = vi
				.spyOn(HTMLAnchorElement.prototype, 'click')
				.mockImplementation(() => {});
			const vm = createCyberfliesVM(1);
			await vm.downloadAudio('rec-1');
			expect(createSpy).toHaveBeenCalledWith(blob);
			expect(clickSpy).toHaveBeenCalledTimes(1);
			expect(vm.error).toBeNull();
			clickSpy.mockRestore();
			createSpy.mockRestore();
		});

		it('surfaces a streaming error (e.g. 401/404) instead of saving', async () => {
			vi.spyOn(cyberfliesApi, 'fetchAudioFile').mockRejectedValue(
				new cyberfliesApi.CyberfliesApiError(404, 'recording not found')
			);
			const clickSpy = vi
				.spyOn(HTMLAnchorElement.prototype, 'click')
				.mockImplementation(() => {});
			const vm = createCyberfliesVM(1);
			await vm.downloadAudio('rec-1');
			expect(clickSpy).not.toHaveBeenCalled();
			expect(vm.error).toMatch(/recording not found/);
			clickSpy.mockRestore();
		});
	});

	describe('filenameFromContentDisposition', () => {
		it('parses a quoted filename', () => {
			expect(
				cyberfliesApi.filenameFromContentDisposition('attachment; filename="recording-7.m4a"')
			).toBe('recording-7.m4a');
		});
		it('parses an RFC 5987 filename* and decodes it', () => {
			expect(
				cyberfliesApi.filenameFromContentDisposition(
					"attachment; filename*=UTF-8''recording%20note.mp3"
				)
			).toBe('recording note.mp3');
		});
		it('returns null when no header is present', () => {
			expect(cyberfliesApi.filenameFromContentDisposition(null)).toBeNull();
		});
	});

	describe('deleteRecording', () => {
		it('removes the recording and clears selection when it was selected', async () => {
			vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
				items: [recording({ id: 'a' }), recording({ id: 'b' })],
				limit: 50,
				offset: 0
			});
			const delSpy = vi.spyOn(cyberfliesApi, 'deleteRecording').mockResolvedValue(undefined);
			const vm = createCyberfliesVM(1);
			await vm.refreshRecordings();
			vm.selectRecording('a');
			await vm.deleteRecording('a');
			expect(delSpy).toHaveBeenCalledWith('a');
			expect(vm.recordings.map((r) => r.id)).toEqual(['b']);
			expect(vm.selectedId).toBeNull();
		});

		it('surfaces delete errors and keeps the recording', async () => {
			vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
				items: [recording({ id: 'a' })],
				limit: 50,
				offset: 0
			});
			vi.spyOn(cyberfliesApi, 'deleteRecording').mockRejectedValue(new Error('nope'));
			const vm = createCyberfliesVM(1);
			await vm.refreshRecordings();
			await vm.deleteRecording('a');
			expect(vm.error).toMatch(/nope/);
			expect(vm.recordings).toHaveLength(1);
		});
	});

	describe('organize into channels', () => {
		it('createChannel adds the channel and returns it', async () => {
			vi.spyOn(cyberfliesApi, 'createChannel').mockResolvedValue(channel({ id: 'c9', name: 'Planning' }));
			const vm = createCyberfliesVM(1);
			const ch = await vm.createChannel('Planning');
			expect(ch?.id).toBe('c9');
			expect(vm.channels.map((c) => c.name)).toContain('Planning');
		});

		it('createChannel ignores blank names without calling the API', async () => {
			const spy = vi.spyOn(cyberfliesApi, 'createChannel');
			const vm = createCyberfliesVM(1);
			const ch = await vm.createChannel('   ');
			expect(ch).toBeNull();
			expect(spy).not.toHaveBeenCalled();
		});

		it('createChannel forwards a trimmed description (or undefined when blank)', async () => {
			const spy = vi
				.spyOn(cyberfliesApi, 'createChannel')
				.mockResolvedValue(channel({ id: 'c1', name: 'Planning' }));
			const vm = createCyberfliesVM(1);
			await vm.createChannel('Planning', '  weekly  ');
			expect(spy).toHaveBeenCalledWith('Planning', 'weekly');
			await vm.createChannel('Planning', '   ');
			expect(spy).toHaveBeenLastCalledWith('Planning', undefined);
		});

		it('deleteChannel removes it and resets chat scope when it was selected', async () => {
			vi.spyOn(cyberfliesApi, 'listChannels').mockResolvedValue({
				items: [channel({ id: 'c1', name: 'A' }), channel({ id: 'c2', name: 'B' })],
				limit: 50,
				offset: 0
			});
			const delSpy = vi.spyOn(cyberfliesApi, 'deleteChannel').mockResolvedValue(undefined);
			const vm = createCyberfliesVM(1);
			await vm.refreshChannels();
			vm.setChatScope('channel:c1');
			await vm.deleteChannel('c1');
			expect(delSpy).toHaveBeenCalledWith('c1');
			expect(vm.chatScope).toBe('all');
			expect(vm.channels.map((c) => c.id)).toEqual(['c2']);
			expect(vm.chatScope).toBe('all');
		});

		it('deleteChannel surfaces errors and keeps the channel', async () => {
			vi.spyOn(cyberfliesApi, 'listChannels').mockResolvedValue({
				items: [channel({ id: 'c1', name: 'A' })],
				limit: 50,
				offset: 0
			});
			vi.spyOn(cyberfliesApi, 'deleteChannel').mockRejectedValue(new Error('locked'));
			const vm = createCyberfliesVM(1);
			await vm.refreshChannels();
			await vm.deleteChannel('c1');
			expect(vm.error).toMatch(/locked/);
			expect(vm.channels).toHaveLength(1);
		});

		it('addToChannel posts membership and sets a confirmation notice', async () => {
			vi.spyOn(cyberfliesApi, 'listChannels').mockResolvedValue({
				items: [channel({ id: 'c1', name: 'Standups' })],
				limit: 50,
				offset: 0
			});
			const addSpy = vi.spyOn(cyberfliesApi, 'addRecordingToChannel').mockResolvedValue(undefined);
			const vm = createCyberfliesVM(1);
			await vm.refreshChannels();
			await vm.addToChannel('rec-7', 'c1');
			expect(addSpy).toHaveBeenCalledWith('c1', 'rec-7');
			expect(vm.notice).toBe('Added to Standups');
			vm.clearNotice();
			expect(vm.notice).toBeNull();
		});

		it('addToChannel surfaces errors', async () => {
			vi.spyOn(cyberfliesApi, 'addRecordingToChannel').mockRejectedValue(new Error('403'));
			const vm = createCyberfliesVM(1);
			await vm.addToChannel('rec-7', 'c1');
			expect(vm.error).toMatch(/403/);
		});

		it('toggleChannel loads the channel contents, and collapses on a second call', async () => {
			const listSpy = vi.spyOn(cyberfliesApi, 'listChannelRecordings').mockResolvedValue({
				items: [recording({ id: 'r1' }), recording({ id: 'r2' })],
				limit: 50,
				offset: 0
			});
			const vm = createCyberfliesVM(1);
			await vm.toggleChannel('c1');
			expect(listSpy).toHaveBeenCalledWith('c1');
			expect(vm.expandedChannelId).toBe('c1');
			expect(vm.channelRecordings.map((r) => r.id)).toEqual(['r1', 'r2']);
			await vm.toggleChannel('c1');
			expect(vm.expandedChannelId).toBeNull();
		});

		it('recapChannel generates and stores the recap', async () => {
			vi.spyOn(cyberfliesApi, 'generateChannelRecap').mockResolvedValue({
				headline: 'Q3 sync',
				abstract: 'We **shipped** a lot.',
				bullets: ['a', 'b']
			});
			const vm = createCyberfliesVM(1);
			await vm.recapChannel('c1');
			expect(vm.channelRecap?.headline).toBe('Q3 sync');
			expect(vm.channelRecap?.bullets).toEqual(['a', 'b']);
		});

	});

	describe('meeting bot', () => {
		it('joinMeeting trims fields, inserts the session, and polls until terminal', async () => {
			const joinSpy = vi
				.spyOn(cyberfliesApi, 'joinMeeting')
				.mockResolvedValue(session({ id: 'm1', status: 'scheduled' }));
			vi.spyOn(cyberfliesApi, 'getMeetingSession')
				.mockResolvedValueOnce(session({ id: 'm1', status: 'recording' }))
				.mockResolvedValueOnce(
					session({ id: 'm1', status: 'completed', recording_id: 'rec-99' })
				);
			vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
				items: [],
				limit: 50,
				offset: 0
			});
			const vm = createCyberfliesVM(1);
			await vm.joinMeeting({
				platform: 'google_meet',
				meeting_url: '  https://meet.google.com/x  ',
				bot_display_name: '  Notetaker  ',
				consent_message: ''
			});
			expect(joinSpy).toHaveBeenCalledWith({
				platform: 'google_meet',
				meeting_url: 'https://meet.google.com/x',
				bot_display_name: 'Notetaker',
				consent_message: undefined
			});
			expect(vm.meetingSessions[0].id).toBe('m1');
			await flush(20);
			expect(vm.meetingSessions[0].status).toBe('completed');
			expect(vm.meetingSessions[0].recording_id).toBe('rec-99');
		});

		it('joinMeeting requires a URL', async () => {
			const joinSpy = vi.spyOn(cyberfliesApi, 'joinMeeting');
			const vm = createCyberfliesVM(1);
			await vm.joinMeeting({ platform: 'google_meet', meeting_url: '   ' });
			expect(joinSpy).not.toHaveBeenCalled();
			expect(vm.botError).toMatch(/url is required/i);
		});

		it('joinMeeting surfaces errors', async () => {
			vi.spyOn(cyberfliesApi, 'joinMeeting').mockRejectedValue(new Error('bot busy'));
			const vm = createCyberfliesVM(1);
			await vm.joinMeeting({ platform: 'microsoft_teams', meeting_url: 'https://teams/x' });
			expect(vm.botError).toMatch(/bot busy/);
		});

		it('refreshMeetingSessions lists sessions and resumes polling non-terminal ones', async () => {
			vi.spyOn(cyberfliesApi, 'listMeetingSessions').mockResolvedValue({
				items: [session({ id: 'm2', status: 'joining' })],
				limit: 50,
				offset: 0
			});
			const getSpy = vi
				.spyOn(cyberfliesApi, 'getMeetingSession')
				.mockResolvedValue(session({ id: 'm2', status: 'failed', error: 'lobby timeout' }));
			const vm = createCyberfliesVM(1);
			await vm.refreshMeetingSessions();
			expect(vm.meetingSessions).toHaveLength(1);
			await flush(20);
			expect(getSpy).toHaveBeenCalledWith('m2');
			expect(vm.meetingSessions[0].status).toBe('failed');
		});

		it('does not poll a session that is already terminal', async () => {
			vi.spyOn(cyberfliesApi, 'joinMeeting').mockResolvedValue(
				session({ id: 'm3', status: 'completed', recording_id: 'r1' })
			);
			vi.spyOn(cyberfliesApi, 'listRecordings').mockResolvedValue({
				items: [],
				limit: 50,
				offset: 0
			});
			const getSpy = vi.spyOn(cyberfliesApi, 'getMeetingSession');
			const vm = createCyberfliesVM(1);
			await vm.joinMeeting({ platform: 'google_meet', meeting_url: 'https://meet/x' });
			await flush(20);
			expect(getSpy).not.toHaveBeenCalled();
		});
	});

	describe('organize remove (cont.)', () => {
		it('removeFromChannel drops the recording from the expanded list', async () => {
			vi.spyOn(cyberfliesApi, 'listChannelRecordings').mockResolvedValue({
				items: [recording({ id: 'r1' }), recording({ id: 'r2' })],
				limit: 50,
				offset: 0
			});
			const rmSpy = vi
				.spyOn(cyberfliesApi, 'removeRecordingFromChannel')
				.mockResolvedValue(undefined);
			const vm = createCyberfliesVM(1);
			await vm.toggleChannel('c1');
			await vm.removeFromChannel('c1', 'r1');
			expect(rmSpy).toHaveBeenCalledWith('c1', 'r1');
			expect(vm.channelRecordings.map((r) => r.id)).toEqual(['r2']);
			expect(vm.notice).toBe('Removed from channel');
		});
	});

	describe('channel rename', () => {
		it('renameChannel updates the channel in the list', async () => {
			vi.spyOn(cyberfliesApi, 'listChannels').mockResolvedValue({
				items: [channel({ id: 'c1', name: 'Old' })],
				limit: 50,
				offset: 0
			});
			vi.spyOn(cyberfliesApi, 'updateChannel').mockResolvedValue(
				channel({ id: 'c1', name: 'New name' })
			);
			const vm = createCyberfliesVM(1);
			await vm.refreshChannels();
			await vm.renameChannel('c1', 'New name');
			expect(vm.channels[0].name).toBe('New name');
			expect(vm.notice).toBe('Channel renamed');
		});
	});

	describe('MCP servers', () => {
		const srv = (over = {}) => ({
			id: 's1',
			name: 'Jira',
			url: 'https://x/mcp',
			enabled: true,
			has_auth_token: false,
			...over
		});
		it('refresh / add / toggle / remove', async () => {
			vi.spyOn(cyberfliesApi, 'listMcpServers').mockResolvedValue({ items: [srv()] });
			vi.spyOn(cyberfliesApi, 'createMcpServer').mockResolvedValue(srv({ id: 's2', name: 'GH' }));
			vi.spyOn(cyberfliesApi, 'setMcpServerEnabled').mockResolvedValue(srv({ enabled: false }));
			vi.spyOn(cyberfliesApi, 'deleteMcpServer').mockResolvedValue(undefined);
			const vm = createCyberfliesVM(1);

			await vm.refreshMcpServers();
			expect(vm.mcpServers.map((s) => s.id)).toEqual(['s1']);

			await vm.addMcpServer('GH', 'https://gh/mcp');
			expect(vm.mcpServers.map((s) => s.id)).toEqual(['s1', 's2']);

			await vm.toggleMcpServer('s1', false);
			expect(vm.mcpServers.find((s) => s.id === 's1')?.enabled).toBe(false);

			await vm.removeMcpServer('s1');
			expect(vm.mcpServers.map((s) => s.id)).toEqual(['s2']);
		});
	});

	describe('uploads', () => {
		it('small files use the multipart upload', async () => {
			const up = vi.spyOn(cyberfliesApi, 'uploadRecording').mockResolvedValue(recording());
			const presign = vi.spyOn(cyberfliesApi, 'requestUploadUrl');
			const vm = createCyberfliesVM(1);
			await vm.uploadAudio(new File(['x'], 'small.m4a'));
			expect(up).toHaveBeenCalledOnce();
			expect(presign).not.toHaveBeenCalled();
		});

		it('large files use the presigned direct upload', async () => {
			const big = new File(['x'], 'big.mp4');
			Object.defineProperty(big, 'size', { value: 25 * 1024 * 1024 });
			const presign = vi.spyOn(cyberfliesApi, 'requestUploadUrl').mockResolvedValue({
				recording_id: 'r9',
				upload_url: 'https://storage/put',
				storage_key: 'k',
				expires_in: 900,
				status: 'pending'
			});
			const put = vi.spyOn(cyberfliesApi, 'putToPresignedUrl').mockResolvedValue(undefined);
			const complete = vi.spyOn(cyberfliesApi, 'completeUpload').mockResolvedValue(undefined);
			vi.spyOn(cyberfliesApi, 'getRecording').mockResolvedValue(recording({ id: 'r9' }));
			const multipart = vi.spyOn(cyberfliesApi, 'uploadRecording');
			const vm = createCyberfliesVM(1);

			await vm.uploadAudio(big);
			expect(presign).toHaveBeenCalledOnce();
			expect(put).toHaveBeenCalledWith('https://storage/put', big);
			expect(complete).toHaveBeenCalledWith('r9');
			expect(multipart).not.toHaveBeenCalled();
			expect(vm.selectedId).toBe('r9');
		});
	});

	describe('media url', () => {
		it('mediaUrl returns the presigned url', async () => {
			vi.spyOn(cyberfliesApi, 'recordingMediaUrl').mockResolvedValue({
				url: 'https://storage/play.mp4',
				expires_seconds: 600
			});
			const vm = createCyberfliesVM(1);
			expect(await vm.mediaUrl('rec-1')).toBe('https://storage/play.mp4');
		});
	});
});
