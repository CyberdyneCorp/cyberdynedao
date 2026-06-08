<script lang="ts">
	import { PixelButton, MarkdownPreview } from '@cyberdynecorp/svelte-ui-core';
	import {
		runLessonCode,
		type CodeLanguage,
		type CourseLesson,
		type RunCodeResult
	} from '$lib/api/coursesApi';
	import CodeEditor from './CodeEditor.svelte';
	import Plot from './Plot.svelte';
	import { highlightElement } from '$lib/utils/highlight';
	import { splitPlotSegments, parsePlot } from '$lib/utils/lessonPlot';

	let { lesson, language = 'matlab' }: { lesson: CourseLesson; language?: CodeLanguage } =
		$props();
	const langLabel = $derived(language === 'python' ? 'Python' : 'MATLAB');

	// Colour fenced code blocks inside rendered markdown (```python, ```matlab,
	// ```systemverilog, …). MarkdownPreview emits <code class="language-x">;
	// highlight.js recolours them once they're in the DOM.
	let mdWrap = $state<HTMLElement | null>(null);
	$effect(() => {
		const _ = lesson.textBody; // re-run when the lesson content changes
		if (lesson.lessonType !== 'text') return;
		queueMicrotask(() => {
			mdWrap
				?.querySelectorAll<HTMLElement>('code[class*="language-"]')
				.forEach((el) => highlightElement(el));
		});
	});

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
			result = await runLessonCode(lesson.id, source, language);
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
		<div class="md" bind:this={mdWrap}>
			{#each splitPlotSegments(lesson.textBody ?? 'No content.') as seg}
				{#if seg.kind === 'plot'}
					{@const parsed = parsePlot(seg.content)}
					{#if 'error' in parsed}
						<p class="plot-err">⚠ Plot spec error: {parsed.error}</p>
					{:else}
						<Plot spec={parsed} />
					{/if}
				{:else}
					<MarkdownPreview content={seg.content} />
				{/if}
			{/each}
		</div>
	{:else if lesson.lessonType === 'code'}
		<p class="hint">Edit and run against the {langLabel} engine:</p>
		<CodeEditor
			bind:value={source}
			{language}
			ariaLabel="{langLabel} code"
			minHeight="9rem"
		/>
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
	/* Dark code fences inside rendered markdown, matching the code editor. */
	.md :global(pre) {
		background: #0d1117;
		border-radius: 6px;
		padding: 0.7rem 0.85rem;
		overflow-x: auto;
	}
	.md :global(pre code) {
		background: transparent;
		color: #c9d1d9;
	}
	.run {
		margin-top: 0.4rem;
	}
	.out {
		margin-top: 0.5rem;
		white-space: pre-wrap;
		font-family: ui-monospace, monospace;
		font-size: 0.78rem;
		background: #0d1117;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.6rem;
		color: #c9d1d9;
	}
	.out--err {
		color: #ffa198;
	}
	.hint {
		color: #374151;
	}
</style>
