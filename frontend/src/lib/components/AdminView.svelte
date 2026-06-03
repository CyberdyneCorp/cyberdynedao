<script lang="ts">
	import {
		PixelScrollArea,
		PixelButton,
		PixelInput,
		PixelCheckbox,
		Textarea,
		Select,
		Badge
	} from '@cyberdynecorp/svelte-ui-core';
	import { createAdminViewModel, shouldAutoLoad } from '$lib/viewmodels/adminViewModel';
	import type { CourseLevel, LessonType } from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const STATUS_VARIANT = { draft: 'warning', published: 'success' } as const;

	const vm = createAdminViewModel();
	const { courses, selected, loading, busy, error } = vm;

	const canEdit = $derived(
		authVM.isRestored && authVM.isAuthenticated && (authVM.isEditor || authVM.isAdmin)
	);

	// New-course form.
	let title = $state('');
	let description = $state('');
	let level = $state<CourseLevel>('Beginner');

	const levels: CourseLevel[] = ['Beginner', 'Intermediate', 'Advanced'];
	const levelOptions = levels.map((l) => ({ value: l, label: l }));

	// New-lesson form (within the open-course editor).
	let lTitle = $state('');
	let lType = $state<LessonType>('text');
	let lContentUrl = $state('');
	let lTextBody = $state('');
	let lDuration = $state('');
	let uploadName = $state<string | null>(null);

	const lessonTypes: LessonType[] = ['text', 'video', 'pdf', 'presentation', 'quiz', 'code'];
	const lessonTypeOptions = lessonTypes.map((t) => ({ value: t, label: t }));
	const URL_TYPES: LessonType[] = ['video', 'pdf', 'presentation'];
	const urlBacked = $derived(URL_TYPES.includes(lType));

	// Load the course list once when authoring becomes available. Do NOT
	// key this on `$courses.length` — an empty list is a valid result, and
	// re-triggering on it loops the load forever ("Loading…" that never
	// settles). The user can re-run it via the Retry button on error.
	let loadAttempted = $state(false);
	$effect(() => {
		if (shouldAutoLoad(canEdit, loadAttempted, $loading)) {
			loadAttempted = true;
			void vm.load();
		}
	});

	// Edit-course form, re-seeded from the open course whenever it changes.
	let eTitle = $state('');
	let eDescription = $state('');
	let eMandatory = $state(false);
	let eDueAt = $state(''); // datetime-local value (local time)
	let editingSlug = $state<string | null>(null);

	function isoToLocalInput(iso: string): string {
		const d = new Date(iso);
		const pad = (n: number) => String(n).padStart(2, '0');
		return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
	}

	$effect(() => {
		const c = $selected;
		if (c && c.slug !== editingSlug) {
			editingSlug = c.slug;
			eTitle = c.title;
			eDescription = c.description ?? '';
			eMandatory = c.mandatory;
			eDueAt = c.dueAt ? isoToLocalInput(c.dueAt) : '';
		}
	});

	async function saveCourseEdits(): Promise<void> {
		const c = $selected;
		if (!c || !eTitle.trim()) return;
		await vm.editCourse(c.slug, {
			title: eTitle.trim(),
			description: eDescription.trim(),
			mandatory: eMandatory
		});
	}

	async function saveDeadline(): Promise<void> {
		const c = $selected;
		if (!c) return;
		await vm.setDeadline(c.slug, eDueAt ? new Date(eDueAt).toISOString() : null);
	}

	async function clearDeadline(): Promise<void> {
		const c = $selected;
		if (!c) return;
		eDueAt = '';
		await vm.setDeadline(c.slug, null);
	}

	// Inline lesson editing.
	let editingLessonId = $state<string | null>(null);
	let elTitle = $state('');
	let elDuration = $state('');
	let elContentUrl = $state('');
	let elTextBody = $state('');

	function openLessonEdit(lesson: {
		id: string;
		title: string;
		duration: string | null;
		contentUrl: string | null;
		textBody: string | null;
	}): void {
		editingLessonId = lesson.id;
		elTitle = lesson.title;
		elDuration = lesson.duration ?? '';
		elContentUrl = lesson.contentUrl ?? '';
		elTextBody = lesson.textBody ?? '';
	}

	function closeLessonEdit(): void {
		editingLessonId = null;
	}

	async function saveLessonEdit(): Promise<void> {
		if (!editingLessonId || !elTitle.trim()) return;
		const ok = await vm.editLesson(editingLessonId, {
			title: elTitle.trim(),
			duration: elDuration.trim() || undefined,
			contentUrl: elContentUrl.trim() || undefined,
			textBody: elTextBody.trim() || undefined
		});
		if (ok) closeLessonEdit();
	}

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

<PixelScrollArea maxHeight="100%" ariaLabel="Academy admin">
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
			You need the <strong>editor</strong> role or an <strong>admin</strong> account to author courses.
			{#if !authVM.isAuthenticated}Sign in with an editor or admin account to continue.{/if}
		</p>
	{:else}
		{#if $error}
			<p class="banner banner--error" role="alert">{$error}</p>
		{/if}

		{#if $selected}
			{@const course = $selected}
			<!-- Lesson editor for the open course -->
			<PixelButton variant="ghost" size="sm" onclick={() => vm.closeCourse()}>← All courses</PixelButton>
			<div class="detail-head">
				<Badge variant={STATUS_VARIANT[course.status]} size="sm">{course.status}</Badge>
				<h2>{course.title}</h2>
			</div>

			{#if quizLessonId}
				<!-- Quiz builder for a quiz-type lesson -->
				<PixelButton variant="ghost" size="sm" onclick={closeQuizEditor}>← Back to lessons</PixelButton>
				<h2>Quiz</h2>
				<label class="passing">
					Passing score (%)
					<input class="num" type="number" min="1" max="100" bind:value={quizPassing} />
				</label>

				{#each quizQuestions as q, qi (qi)}
					<div class="qcard">
						<PixelInput placeholder={`Question ${qi + 1}`} bind:value={q.prompt} ariaLabel="Question prompt" />
						<PixelInput
							placeholder="Explanation (shown after answering)"
							bind:value={q.explanation}
							ariaLabel="Explanation"
						/>
						{#each q.options as opt, oi (oi)}
							<div class="opt">
								<input
									type="radio"
									name="correct-{qi}"
									checked={opt.isCorrect}
									onchange={() => setCorrect(qi, oi)}
									aria-label="Mark option {oi + 1} correct"
								/>
								<div class="opt__input">
									<PixelInput placeholder={`Option ${oi + 1}`} bind:value={opt.text} ariaLabel="Option text" />
								</div>
								<PixelButton
									variant="ghost"
									size="sm"
									disabled={q.options.length <= 2}
									ariaLabel="Remove option"
									onclick={() => removeOption(qi, oi)}
								>
									✕
								</PixelButton>
							</div>
						{/each}
						<div class="row">
							<PixelButton variant="outline" size="sm" disabled={q.options.length >= 6} onclick={() => addOption(qi)}>
								+ option
							</PixelButton>
							<PixelButton variant="ghost" size="sm" onclick={() => removeQuestion(qi)}>
								Remove question
							</PixelButton>
						</div>
					</div>
				{/each}

				<PixelButton variant="outline" size="sm" disabled={quizQuestions.length >= 15} onclick={addQuestion}>
					+ question
				</PixelButton>
				<p class="hint">Select the radio next to the correct option. 2–6 options per question, 1–15 questions.</p>
				<div class="row">
					<PixelButton variant="solid" disabled={$busy || !quizValid} onclick={saveQuiz}>
						{$busy ? 'Saving…' : 'Save quiz'}
					</PixelButton>
					<PixelButton variant="ghost" disabled={$busy} onclick={deleteQuiz}>Delete quiz</PixelButton>
				</div>
			{:else}
				<!-- Edit course metadata -->
				<form class="new-course" onsubmit={(e) => { e.preventDefault(); void saveCourseEdits(); }}>
					<h2>Edit course</h2>
					<PixelInput placeholder="Course title" bind:value={eTitle} ariaLabel="Course title" />
					<Textarea label="Description" rows={2} bind:value={eDescription} />
					<PixelCheckbox bind:checked={eMandatory} label="Mandatory course" />
					<PixelButton type="submit" variant="solid" size="sm" disabled={$busy || !eTitle.trim()}>
						{$busy ? 'Saving…' : 'Save changes'}
					</PixelButton>
				</form>

				<!-- Deadline -->
				<div class="new-course">
					<h2>Deadline</h2>
					<div class="row row--end">
						<label class="grow dt-field">
							<span>Due date &amp; time</span>
							<input class="dt" type="datetime-local" bind:value={eDueAt} aria-label="Course deadline" />
						</label>
						<PixelButton variant="solid" size="sm" disabled={$busy || !eDueAt} onclick={saveDeadline}>
							Set
						</PixelButton>
						<PixelButton variant="ghost" size="sm" disabled={$busy || !course.dueAt} onclick={clearDeadline}>
							Clear
						</PixelButton>
					</div>
					{#if course.dueAt}
						<p class="hint">Current: {new Date(course.dueAt).toLocaleString()} · {course.deadlineStatus}</p>
					{:else}
						<p class="hint">No deadline set.</p>
					{/if}
				</div>

				<h2>Lessons</h2>
				{#if course.lessons.length === 0}
					<p class="hint">No lessons yet — add the first one below.</p>
				{:else}
					<ul class="list">
						{#each course.lessons as lesson, li (lesson.id)}
							<li class="item">
								<div class="item__main">
									<span class="item__meta">{lesson.lessonType}</span>
									<span class="item__title">{lesson.title}</span>
								</div>
								<div class="item__actions">
									<PixelButton variant="ghost" size="sm" ariaLabel="Move lesson up" disabled={$busy || li === 0} onclick={() => vm.moveLesson(lesson.id, 'up')}>
										▲
									</PixelButton>
									<PixelButton variant="ghost" size="sm" ariaLabel="Move lesson down" disabled={$busy || li === course.lessons.length - 1} onclick={() => vm.moveLesson(lesson.id, 'down')}>
										▼
									</PixelButton>
									<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => openLessonEdit(lesson)}>
										Edit
									</PixelButton>
									{#if lesson.lessonType === 'quiz'}
										<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => openQuizEditor(lesson.id)}>
											Quiz
										</PixelButton>
									{/if}
									<PixelButton
										variant="ghost"
										size="sm"
										disabled={$busy}
										onclick={() => vm.removeLesson(lesson.id)}
									>
										Delete
									</PixelButton>
								</div>
							</li>
							{#if editingLessonId === lesson.id}
								<li class="edit-row">
									<form class="new-course" onsubmit={(e) => { e.preventDefault(); void saveLessonEdit(); }}>
										<h2>Edit lesson</h2>
										<PixelInput placeholder="Lesson title" bind:value={elTitle} ariaLabel="Lesson title" />
										<PixelInput placeholder="Duration (optional)" bind:value={elDuration} ariaLabel="Duration" />
										{#if URL_TYPES.includes(lesson.lessonType)}
											<PixelInput placeholder="Content URL" bind:value={elContentUrl} ariaLabel="Content URL" />
										{:else if lesson.lessonType === 'text'}
											<Textarea label="Lesson text (markdown)" rows={3} bind:value={elTextBody} />
										{/if}
										<div class="row">
											<PixelButton type="submit" variant="solid" size="sm" disabled={$busy || !elTitle.trim()}>
												{$busy ? 'Saving…' : 'Save lesson'}
											</PixelButton>
											<PixelButton variant="ghost" size="sm" onclick={closeLessonEdit}>Cancel</PixelButton>
										</div>
									</form>
								</li>
							{/if}
						{/each}
					</ul>
				{/if}

				<form class="new-course" onsubmit={(e) => { e.preventDefault(); void submitLesson(); }}>
					<h2>Add lesson</h2>
					<PixelInput placeholder="Lesson title" bind:value={lTitle} ariaLabel="Lesson title" />
					<div class="row row--end">
						<div class="grow">
							<Select
								label="Lesson type"
								value={lType}
								options={lessonTypeOptions}
								onchange={(e) => (lType = (e.target as HTMLSelectElement).value as LessonType)}
							/>
						</div>
						<div class="grow">
							<PixelInput placeholder="Duration (optional)" bind:value={lDuration} ariaLabel="Duration" />
						</div>
					</div>
					{#if urlBacked}
						<div class="row">
							<input type="file" onchange={onPickFile} aria-label="Upload material" />
							{#if uploadName}<span class="hint">Uploaded: {uploadName}</span>{/if}
						</div>
						<PixelInput placeholder="Content URL" bind:value={lContentUrl} ariaLabel="Content URL" />
					{:else if lType === 'text'}
						<Textarea label="Lesson text (markdown)" rows={3} bind:value={lTextBody} />
					{:else if lType === 'quiz'}
						<p class="hint">Add the lesson, then click <strong>Quiz</strong> on its row to author questions.</p>
					{:else}
						<p class="hint">Code lessons run interactively against the MATLAB engine — no content needed.</p>
					{/if}
					<PixelButton type="submit" variant="solid" disabled={$busy || !lessonValid}>
						{$busy ? 'Saving…' : 'Add lesson'}
					</PixelButton>
				</form>
			{/if}
		{:else}
			<!-- New course -->
			<form class="new-course" onsubmit={(e) => { e.preventDefault(); void submit(); }}>
				<h2>New course</h2>
				<PixelInput placeholder="Course title" bind:value={title} ariaLabel="Course title" />
				<Textarea label="Description" rows={2} bind:value={description} />
				<div class="row row--end">
					<div class="grow">
						<Select
							label="Level"
							value={level}
							options={levelOptions}
							onchange={(e) => (level = (e.target as HTMLSelectElement).value as CourseLevel)}
						/>
					</div>
					<PixelButton type="submit" variant="solid" disabled={$busy || !title.trim()}>
						{$busy ? 'Saving…' : 'Create draft'}
					</PixelButton>
				</div>
			</form>

			<!-- Course list -->
			<h2>Courses</h2>
			{#if $loading && $courses.length === 0}
				<p class="hint">Loading…</p>
			{:else if $courses.length === 0}
				{#if $error}
					<p class="hint">Couldn't load courses.</p>
					<PixelButton variant="outline" size="sm" disabled={$loading} onclick={() => void vm.load()}>
						Retry
					</PixelButton>
				{:else}
					<p class="hint">No courses yet — create your first draft above.</p>
				{/if}
			{:else}
				<ul class="list">
					{#each $courses as course, ci (course.id)}
						<li class="item">
							<div class="item__main">
								<Badge variant={STATUS_VARIANT[course.status]} size="sm">{course.status}</Badge>
								<span class="item__title">{course.title}</span>
								<span class="item__meta">{course.level} · {course.lessonCount} lessons</span>
							</div>
							<div class="item__actions">
								<PixelButton variant="ghost" size="sm" ariaLabel="Move course up" disabled={$busy || ci === 0} onclick={() => vm.moveCourse(course.slug, 'up')}>
									▲
								</PixelButton>
								<PixelButton variant="ghost" size="sm" ariaLabel="Move course down" disabled={$busy || ci === $courses.length - 1} onclick={() => vm.moveCourse(course.slug, 'down')}>
									▼
								</PixelButton>
								<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => vm.openCourse(course.slug)}>
									Edit
								</PixelButton>
								{#if course.status === 'published'}
									<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => vm.unpublish(course.slug)}>
										Unpublish
									</PixelButton>
								{:else}
									<PixelButton variant="solid" size="sm" disabled={$busy} onclick={() => vm.publish(course.slug)}>
										Publish
									</PixelButton>
								{/if}
								<PixelButton variant="ghost" size="sm" disabled={$busy} onclick={() => vm.remove(course.slug)}>
									Delete
								</PixelButton>
							</div>
						</li>
					{/each}
				</ul>
			{/if}
		{/if}
	{/if}
</div>
</PixelScrollArea>

<style>
	.admin-view {
		padding: 1.25rem;
		color: #e5e7eb;
		font-family: system-ui, sans-serif;
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
	.row {
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}
	.row--end {
		align-items: flex-end;
	}
	.grow {
		flex: 1;
		min-width: 0;
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
	.hint {
		color: #9ca3af;
		font-size: 0.85rem;
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
	.num {
		width: 5rem;
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 5px;
		color: #e5e7eb;
		padding: 0.4rem 0.55rem;
		font: inherit;
		box-sizing: border-box;
	}
	.dt-field {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		font-size: 0.78rem;
		color: #9ca3af;
	}
	.dt {
		background: #0b1220;
		border: 1px solid #1f2937;
		border-radius: 5px;
		color: #e5e7eb;
		padding: 0.4rem 0.55rem;
		font: inherit;
		box-sizing: border-box;
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
	.opt__input {
		flex: 1;
	}
	.edit-row {
		list-style: none;
	}
	.edit-row .new-course {
		margin-bottom: 0.45rem;
	}
</style>
