import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createCyberfliesVM } from '../cyberfliesViewModel.svelte';
import * as cyberfliesApi from '$lib/api/cyberfliesApi';
import type { ChannelResponse, RecordingResponse } from '$lib/api/cyberfliesApi';

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
			vm.setChatScope('chan-7');
			await vm.sendChat('what changed?');
			expect(channelSpy).toHaveBeenCalledWith('chan-7', [
				{ role: 'user', content: 'what changed?' }
			]);
			expect(globalSpy).not.toHaveBeenCalled();
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
			vm.setChatScope('c1');
			await vm.deleteChannel('c1');
			expect(delSpy).toHaveBeenCalledWith('c1');
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
	});
});
