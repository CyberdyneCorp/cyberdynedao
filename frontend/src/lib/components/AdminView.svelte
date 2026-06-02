<script lang="ts">
	import { createAdminViewModel } from '$lib/viewmodels/adminViewModel';
	import type { CourseLevel, LessonType } from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const vm = createAdminViewModel();
	const { courses, selected, loading, busy, error } = vm;

	const canEdit = $derived(authVM.isRestored && authVM.isAuthenticated && authVM.isEditor);

	// New-course form.
	let title = $state('');
	let description = $state('');
	let level = $state<CourseLevel>('Beginner');

	const levels: CourseLevel[] = ['Beginner', 'Intermediate', 'Advanced'];

	// New-lesson form (within the open-course editor).
	let lTitle = $state('');
	let lType = $state<LessonType>('text');
	let lContentUrl = $state('');
	let lTextBody = $state('');
	let lDuration = $state('');
	let uploadName = $state<string | null>(null);

	const lessonTypes: LessonType[] = ['text', 'video', 'pdf', 'presentation', 'quiz', 'code'];
	const URL_TYPES: LessonType[] = ['video', 'pdf', 'presentation'];
	const urlBacked = $derived(URL_TYPES.includes(lType));

	$effect(() => {
		if (canEdit && $courses.length === 0 && !$loading) {
			void vm.load();
		}
	});

	async function submit(): Promise<void> {
		if (!title.trim()) return;
		const ok = await vm.create({ title: title.trim(), description: description.trim(), level });
		if (ok) {
			title = '';
			description = '';
			level = 'Beginner';
		}
	}

	function resetLessonForm(): void {
		lTitle = '';
		lType = 'text';
		lContentUrl = '';
		lTextBody = '';
		lDuration = '';
		uploadName = null;
	}

	async function onPickFile(e: Event): Promise<void> {
		const input = e.target as HTMLInputElement;
		const file = input.files?.[0];
		if (!file) return;
		const result = await vm.upload(file);
		if (result) {
			lContentUrl = result.url;
			uploadName = result.originalFilename;
		}
	}

	const lessonValid = $derived(
		!!lTitle.trim() &&
			(urlBacked ? !!lContentUrl.trim() : lType === 'text' ? !!lTextBody.trim() : true)
	);

	async function submitLesson(): Promise<void> {
		if (!lessonValid) return;
		const ok = await vm.addLesson({
			title: lTitle.trim(),
			lessonType: lType,
			contentUrl: urlBacked ? lContentUrl.trim() : undefined,
			textBody: lType === 'text' ? lTextBody.trim() : undefined,
			duration: lDuration.trim() || undefined
		});
		if (ok) resetLessonForm();
	}

	// ── Quiz builder (local editable draft for the open quiz lesson) ──
	type DraftOption = { text: string; isCorrect: boolean };
	type DraftQuestion = { prompt: string; explanation: string; options: DraftOption[] };

	let quizLessonId = $state<string | null>(null);
	let quizPassing = $state(70);
	let quizQuestions = $state<DraftQuestion[]>([]);

	function blankQuestion(): DraftQuestion {
		return {
			prompt: '',
			explanation: '',
			options: [
				{ text: '', isCorrect: true },
				{ text: '', isCorrect: false }
			]
		};
	}

	async function openQuizEditor(lessonId: string): Promise<void> {
		const existing = await vm.loadQuiz(lessonId);
		if (existing) {
			quizPassing = existing.passingScore;
			quizQuestions = existing.questions.map((q) => ({
				prompt: q.prompt,
				explanation: q.explanation,
				options: q.options.map((o) => ({ text: o.text, isCorrect: o.isCorrect }))
			}));
		} else {
			quizPassing = 70;
			quizQuestions = [blankQuestion()];
		}
		quizLessonId = lessonId;
	}

	function closeQuizEditor(): void {
		quizLessonId = null;
		quizQuestions = [];
	}

	function addQuestion(): void {
		quizQuestions = [...quizQuestions, blankQuestion()];
	}
	function removeQuestion(i: number): void {
		quizQuestions = quizQuestions.filter((_, idx) => idx !== i);
	}
	function addOption(qi: number): void {
		quizQuestions[qi].options = [...quizQuestions[qi].options, { text: '', isCorrect: false }];
	}
	function removeOption(qi: number, oi: number): void {
		quizQuestions[qi].options = quizQuestions[qi].options.filter((_, idx) => idx !== oi);
	}
	function setCorrect(qi: number, oi: number): void {
		quizQuestions[qi].options = quizQuestions[qi].options.map((o, idx) => ({
			...o,
			isCorrect: idx === oi
		}));
	}

	const quizValid = $derived(
		quizQuestions.length > 0 &&
			quizQuestions.every(
				(q) =>
					q.prompt.trim() !== '' &&
					q.options.length >= 2 &&
					q.options.every((o) => o.text.trim() !== '') &&
					q.options.filter((o) => o.isCorrect).length === 1
			)
	);

	async function saveQuiz(): Promise<void> {
		if (!quizLessonId || !quizValid) return;
		const ok = await vm.saveQuiz(quizLessonId, {
			passingScore: quizPassing,
			questions: quizQuestions.map((q) => ({
				prompt: q.prompt.trim(),
				explanation: q.explanation.trim(),
				options: q.options.map((o) => ({ text: o.text.trim(), isCorrect: o.isCorrect }))
			}))
		});
		if (ok) closeQuizEditor();
	}

	async function deleteQuiz(): Promise<void> {
		if (!quizLessonId) return;
		const ok = await vm.removeQuiz(quizLessonId);
		if (ok) closeQuizEditor();
	}
</script>

<div class="admin-view">
	<header class="hero">
		<span aria-hidden="true">🛠️</span>
		<div>
			<h1>Academy Admin — Courses</h1>
			<p>Create, publish, and manage courses. Requires the editor role.</p>
		</div>
	</header>

	{#if !authVM.isRestored}
		<p class="hint">Checking your session…</p>
	{:else if !canEdit}
		<p class="banner banner--warn" role="alert">
			You need the <strong>editor</strong> role to author courses.
			{#if !authVM.isAuthenticated}Sign in with an editor account to continue.{/if}
		</p>
	{:else}
		{#if $error}
			<p class="banner banner--error" role="alert">{$error}</p>
		{/if}

		{#if $selected}
			{@const course = $selected}
			<!-- Lesson editor for the open course -->
			<button class="back" onclick={() => vm.closeCourse()}>← All courses</button>
			<div class="detail-head">
				<span class="status status--{course.status}">{course.status}</span>
				<h2>{course.title}</h2>
			</div>

			{#if quizLessonId}
				<!-- Quiz builder for a quiz-type lesson -->
				<button class="back" onclick={closeQuizEditor}>← Back to lessons</button>
				<h2>Quiz</h2>
				<label class="passing">
					Passing score (%)
					<input class="field field--num" type="number" min="1" max="100" bind:value={quizPassing} />
				</label>

				{#each quizQuestions as q, qi (qi)}
					<div class="qcard">
						<input class="field" placeholder="Question {qi + 1}" bind:value={q.prompt} aria-label="Question prompt" />
						<input class="field" placeholder="Explanation (shown after answering)" bind:value={q.explanation} aria-label="Explanation" />
						{#each q.options as opt, oi (oi)}
							<div class="opt">
								<input
									type="radio"
									name="correct-{qi}"
									checked={opt.isCorrect}
									onchange={() => setCorrect(qi, oi)}
									aria-label="Mark option {oi + 1} correct"
								/>
								<input class="field" placeholder="Option {oi + 1}" bind:value={opt.text} aria-label="Option text" />
								<button class="btn" type="button" disabled={q.options.length <= 2} onclick={() => removeOption(qi, oi)}>
									✕
								</button>
							</div>
						{/each}
						<div class="row">
							<button class="btn" type="button" disabled={q.options.length >= 6} onclick={() => addOption(qi)}>
								+ option
							</button>
							<button class="btn btn--danger" type="button" onclick={() => removeQuestion(qi)}>
								Remove question
							</button>
						</div>
					</div>
				{/each}

				<button class="btn" type="button" disabled={quizQuestions.length >= 15} onclick={addQuestion}>
					+ question
				</button>
				<p class="hint">Select the radio next to the correct option. 2–6 options per question, 1–15 questions.</p>
				<div class="row">
					<button class="btn btn--primary" disabled={$busy || !quizValid} onclick={saveQuiz}>
						{$busy ? 'Saving…' : 'Save quiz'}
					</button>
					<button class="btn btn--danger" disabled={$busy} onclick={deleteQuiz}>Delete quiz</button>
				</div>
			{:else}
				{#if course.lessons.length === 0}
					<p class="hint">No lessons yet — add the first one below.</p>
				{:else}
					<ul class="list">
						{#each course.lessons as lesson (lesson.id)}
							<li class="item">
								<div class="item__main">
									<span class="item__meta">{lesson.lessonType}</span>
									<span class="item__title">{lesson.title}</span>
								</div>
								<div class="item__actions">
									{#if lesson.lessonType === 'quiz'}
										<button class="btn" disabled={$busy} onclick={() => openQuizEditor(lesson.id)}>
											Quiz
										</button>
									{/if}
									<button
										class="btn btn--danger"
										disabled={$busy}
										onclick={() => vm.removeLesson(lesson.id)}
									>
										Delete
									</button>
								</div>
							</li>
						{/each}
					</ul>
				{/if}

				<form class="new-course" onsubmit={(e) => { e.preventDefault(); void submitLesson(); }}>
					<h2>Add lesson</h2>
					<input class="field" placeholder="Lesson title" bind:value={lTitle} aria-label="Lesson title" />
					<div class="row">
						<select class="field field--sel" bind:value={lType} aria-label="Lesson type">
							{#each lessonTypes as t (t)}
								<option value={t}>{t}</option>
							{/each}
						</select>
						<input class="field" placeholder="Duration (optional)" bind:value={lDuration} aria-label="Duration" />
					</div>
					{#if urlBacked}
						<div class="row">
							<input type="file" onchange={onPickFile} aria-label="Upload material" />
							{#if uploadName}<span class="hint">Uploaded: {uploadName}</span>{/if}
						</div>
						<input class="field" placeholder="Content URL" bind:value={lContentUrl} aria-label="Content URL" />
					{:else if lType === 'text'}
						<textarea class="field" rows="3" placeholder="Lesson text (markdown)" bind:value={lTextBody} aria-label="Lesson text"></textarea>
					{:else if lType === 'quiz'}
						<p class="hint">Add the lesson, then click <strong>Quiz</strong> on its row to author questions.</p>
					{:else}
						<p class="hint">Code lessons run interactively against the MATLAB engine — no content needed.</p>
					{/if}
					<button class="btn btn--primary" type="submit" disabled={$busy || !lessonValid}>
						{$busy ? 'Saving…' : 'Add lesson'}
					</button>
				</form>
			{/if}
		{:else}
			<!-- New course -->
			<form class="new-course" onsubmit={(e) => { e.preventDefault(); void submit(); }}>
				<h2>New course</h2>
				<input
					class="field"
					placeholder="Course title"
					bind:value={title}
					aria-label="Course title"
				/>
				<textarea
					class="field"
					placeholder="Description"
					rows="2"
					bind:value={description}
					aria-label="Course description"
				></textarea>
				<div class="row">
					<select class="field field--sel" bind:value={level} aria-label="Level">
						{#each levels as lvl (lvl)}
							<option value={lvl}>{lvl}</option>
						{/each}
					</select>
					<button class="btn btn--primary" type="submit" disabled={$busy || !title.trim()}>
						{$busy ? 'Saving…' : 'Create draft'}
					</button>
				</div>
			</form>

			<!-- Course list -->
			<h2>Courses</h2>
			{#if $loading && $courses.length === 0}
				<p class="hint">Loading…</p>
			{:else if $courses.length === 0}
				<p class="hint">No courses yet — create your first draft above.</p>
			{:else}
				<ul class="list">
					{#each $courses as course (course.id)}
						<li class="item">
							<div class="item__main">
								<span class="status status--{course.status}">{course.status}</span>
								<span class="item__title">{course.title}</span>
								<span class="item__meta">{course.level} · {course.lessonCount} lessons</span>
							</div>
							<div class="item__actions">
								<button class="btn" disabled={$busy} onclick={() => vm.openCourse(course.slug)}>
									Edit
								</button>
								{#if course.status === 'published'}
									<button class="btn" disabled={$busy} onclick={() => vm.unpublish(course.slug)}>
										Unpublish
									</button>
								{:else}
									<button
										class="btn btn--primary"
										disabled={$busy}
										onclick={() => vm.publish(course.slug)}
									>
										Publish
									</button>
								{/if}
								<button class="btn btn--danger" disabled={$busy} onclick={() => vm.remove(course.slug)}>
									Delete
								</button>
							</div>
						</li>
					{/each}
				</ul>
			{/if}
		{/if}
	{/if}
</div>

<style>
	.admin-view {
		padding: 1.25rem;
		color: #e5e7eb;
		font-family: system-ui, sans-serif;
		overflow-y: auto;
		height: 100%;
	}
	.hero {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		margin-bottom: 1rem;
	}
	.hero h1 {
		margin: 0;
		font-size: 1.2rem;
	}
	.hero p {
		margin: 0.15rem 0 0;
		font-size: 0.82rem;
		color: #9ca3af;
	}
	.banner {
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.85rem;
		margin-bottom: 0.75rem;
	}
	.banner--error {
		background: #7f1d1d;
		color: #fecaca;
	}
	.banner--warn {
		background: #78350f;
		color: #fcd34d;
	}
	.new-course {
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 8px;
		padding: 0.85rem;
		margin-bottom: 1.25rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.new-course h2,
	.admin-view > h2 {
		margin: 0 0 0.4rem;
		font-size: 1rem;
	}
	.field {
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 5px;
		color: #e5e7eb;
		padding: 0.4rem 0.55rem;
		font: inherit;
		width: 100%;
		box-sizing: border-box;
	}
	.row {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
	.field--sel {
		width: auto;
	}
	.btn {
		font-size: 0.78rem;
		padding: 0.35rem 0.7rem;
		border-radius: 5px;
		border: 1px solid #374151;
		background: #1f2937;
		color: #e5e7eb;
		cursor: pointer;
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
	.btn--danger {
		border-color: #b91c1c;
		color: #fca5a5;
		background: none;
	}
	.list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.45rem;
	}
	.item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 0.75rem;
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 6px;
		padding: 0.5rem 0.7rem;
	}
	.item__main {
		display: flex;
		gap: 0.55rem;
		align-items: center;
		min-width: 0;
	}
	.item__title {
		font-size: 0.9rem;
	}
	.item__meta {
		font-size: 0.72rem;
		color: #6b7280;
	}
	.item__actions {
		display: flex;
		gap: 0.4rem;
		flex-shrink: 0;
	}
	.status {
		font-size: 0.65rem;
		text-transform: uppercase;
		padding: 0.1rem 0.4rem;
		border-radius: 999px;
		font-weight: 600;
	}
	.status--published {
		background: #064e3b;
		color: #6ee7b7;
	}
	.status--draft {
		background: #374151;
		color: #d1d5db;
	}
	.hint {
		color: #9ca3af;
		font-size: 0.85rem;
	}
	.back {
		background: none;
		border: none;
		color: #93c5fd;
		cursor: pointer;
		padding: 0;
		font-size: 0.85rem;
		margin-bottom: 0.5rem;
	}
	.detail-head {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		margin-bottom: 0.5rem;
	}
	.detail-head h2 {
		margin: 0;
		font-size: 1.1rem;
	}
	.passing {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		font-size: 0.85rem;
		color: #9ca3af;
		margin-bottom: 0.75rem;
	}
	.field--num {
		width: 5rem;
	}
	.qcard {
		background: #111827;
		border: 1px solid #1f2937;
		border-radius: 8px;
		padding: 0.7rem;
		margin-bottom: 0.6rem;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.opt {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
</style>
