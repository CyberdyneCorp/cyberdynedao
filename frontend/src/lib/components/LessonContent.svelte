<script lang="ts">
	import { runLessonCode, type CourseLesson, type RunCodeResult } from '$lib/api/coursesApi';

	let { lesson }: { lesson: CourseLesson } = $props();

	// ── Video: embed YouTube, otherwise play an uploaded file. ──
	function youtubeEmbed(url: string): string | null {
		const m = url.match(
			/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]{11})/
		);
		return m ? `https://www.youtube.com/embed/${m[1]}` : null;
	}

	const ytEmbed = $derived(lesson.contentUrl ? youtubeEmbed(lesson.contentUrl) : null);

	// ── Code runner (code lessons execute on the MATLAB engine). ──
	let source = $state(lesson.textBody ?? '');
	let running = $state(false);
	let result = $state<RunCodeResult | null>(null);
	let runError = $state<string | null>(null);

	async function run(): Promise<void> {
		if (!source.trim()) return;
		running = true;
		runError = null;
		try {
			result = await runLessonCode(lesson.id, source);
		} catch (err) {
			runError = err instanceof Error ? err.message : String(err);
		} finally {
			running = false;
		}
	}
</script>

<div class="content">
	{#if lesson.lessonType === 'video' && lesson.contentUrl}
		{#if ytEmbed}
			<div class="frame frame--16x9">
				<iframe src={ytEmbed} title={lesson.title} allowfullscreen loading="lazy"></iframe>
			</div>
		{:else}
			<!-- svelte-ignore a11y_media_has_caption -->
			<video class="video" src={lesson.contentUrl} controls></video>
		{/if}
	{:else if lesson.lessonType === 'pdf' && lesson.contentUrl}
		<div class="frame frame--doc">
			<iframe src={lesson.contentUrl} title={lesson.title} loading="lazy"></iframe>
		</div>
		<a class="ext" href={lesson.contentUrl} target="_blank" rel="noopener">Open PDF ↗</a>
	{:else if lesson.lessonType === 'presentation' && lesson.contentUrl}
		<a class="ext" href={lesson.contentUrl} target="_blank" rel="noopener">Open presentation ↗</a>
	{:else if lesson.lessonType === 'text'}
		<div class="text">{lesson.textBody ?? 'No content.'}</div>
	{:else if lesson.lessonType === 'code'}
		<p class="hint">Edit and run against the MATLAB engine:</p>
		<textarea class="code" rows="6" bind:value={source} spellcheck="false" aria-label="Code"></textarea>
		<button class="btn btn--primary" disabled={running || !source.trim()} onclick={run}>
			{running ? 'Running…' : 'Run'}
		</button>
		{#if runError}
			<pre class="out out--err">{runError}</pre>
		{:else if result}
			{#if result.stdout}<pre class="out">{result.stdout}</pre>{/if}
			{#if result.stderr}<pre class="out out--err">{result.stderr}</pre>{/if}
			{#if result.timedOut}<p class="hint">⏱ Execution timed out.</p>{/if}
		{/if}
	{:else}
		<p class="hint">No previewable content for this lesson.</p>
	{/if}
</div>

<style>
	.content {
		margin-top: 0.5rem;
		font-size: 0.85rem;
	}
	.frame {
		position: relative;
		width: 100%;
		background: #000;
		border-radius: 6px;
		overflow: hidden;
	}
	.frame--16x9 {
		aspect-ratio: 16 / 9;
	}
	.frame--doc {
		height: 420px;
	}
	.frame iframe {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		border: 0;
	}
	.video {
		width: 100%;
		border-radius: 6px;
		background: #000;
	}
	.ext {
		display: inline-block;
		margin-top: 0.4rem;
		color: #93c5fd;
	}
	.text {
		white-space: pre-wrap;
		line-height: 1.5;
		color: #d1d5db;
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.7rem;
	}
	.code {
		width: 100%;
		box-sizing: border-box;
		font-family: ui-monospace, monospace;
		font-size: 0.8rem;
		background: #0b1220;
		color: #e5e7eb;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.6rem;
	}
	.btn {
		font-size: 0.78rem;
		padding: 0.35rem 0.7rem;
		border-radius: 5px;
		border: 1px solid #374151;
		background: #1f2937;
		color: #e5e7eb;
		cursor: pointer;
		margin-top: 0.4rem;
	}
	.btn:disabled {
		opacity: 0.5;
		cursor: default;
	}
	.btn--primary {
		border-color: #2563eb;
		background: #1d4ed8;
		color: #fff;
	}
	.out {
		margin-top: 0.5rem;
		white-space: pre-wrap;
		font-family: ui-monospace, monospace;
		font-size: 0.78rem;
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.6rem;
		color: #d1d5db;
	}
	.out--err {
		color: #fca5a5;
		border-color: #7f1d1d;
	}
	.hint {
		color: #9ca3af;
	}
</style>
