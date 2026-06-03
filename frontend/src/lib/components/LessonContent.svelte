<script lang="ts">
	import { PixelButton, MarkdownPreview } from '@cyberdynecorp/svelte-ui-core';
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
		<div class="md">
			<MarkdownPreview content={lesson.textBody ?? 'No content.'} />
		</div>
	{:else if lesson.lessonType === 'code'}
		<p class="hint">Edit and run against the MATLAB engine:</p>
		<textarea class="code" rows="6" bind:value={source} spellcheck="false" aria-label="Code"></textarea>
		<div class="run">
			<PixelButton variant="solid" size="sm" disabled={running || !source.trim()} onclick={run}>
				{running ? 'Running…' : 'Run'}
			</PixelButton>
		</div>
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
		color: #1d4ed8;
	}
	.md {
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.7rem 0.9rem;
	}
	.code {
		width: 100%;
		box-sizing: border-box;
		font-family: ui-monospace, monospace;
		font-size: 0.8rem;
		background: #f3f4f6;
		color: #000000;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.6rem;
	}
	.run {
		margin-top: 0.4rem;
	}
	.out {
		margin-top: 0.5rem;
		white-space: pre-wrap;
		font-family: ui-monospace, monospace;
		font-size: 0.78rem;
		background: #f3f4f6;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.6rem;
		color: #374151;
	}
	.out--err {
		color: #991b1b;
		border-color: #fee2e2;
	}
	.hint {
		color: #374151;
	}
</style>
