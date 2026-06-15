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
	import { fetchCourseLanguages, translateCourse, type CourseLanguages } from '$lib/api/adminApi';
	import { SUPPORTED_LOCALES } from '$lib/i18n';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const STATUS_VARIANT = { draft: 'warning', published: 'success' } as const;

	const vm = createAdminViewModel();
	const { courses, categories, selected, loading, busy, error, notice } = vm;

	// Auto-dismiss the success notice a few seconds after it appears.
	$effect(() => {
		if ($notice) {
			const t = setTimeout(() => vm.clearNotice(), 3000);
			return () => clearTimeout(t);
		}
	});

	// Two-step delete confirmation, keyed by course slug.
	let confirmingDelete = $state<string | null>(null);

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

	// ── Search, category filter + category management ──────────────────
	let courseSearch = $state('');
	let categoryFilter = $state<string>('all'); // 'all' | 'uncategorized' | <category slug>
	let newCategoryName = $state('');
	let newCategoryIcon = $state('');
	let newCategoryParent = $state(''); // '' = top-level group
	let confirmingCategoryDelete = $state<string | null>(null);

	// Top-level categories are the only valid parents (max one level of nesting).
	const parentOptions = $derived([
		{ value: '', label: '— Top-level group' },
		...$categories
			.filter((c) => c.parentId === null)
			.map((c) => ({ value: c.id, label: `${c.icon} ${c.name}`.trim() }))
	]);

	// Categories as a group → sub-categories tree for the admin panel.
	const categoryTree = $derived.by(() => {
		const byOrder = (a: { sortOrder: number }, b: { sortOrder: number }) =>
			a.sortOrder - b.sortOrder;
		const tops = $categories.filter((c) => c.parentId === null).sort(byOrder);
		return tops.map((top) => ({
			top,
			children: $categories.filter((c) => c.parentId === top.id).sort(byOrder)
		}));
	});

	// Filter dropdown options: All / Uncategorized / each category.
	const categoryFilterOptions = $derived([
		{ value: 'all', label: 'All categories' },
		{ value: 'uncategorized', label: 'Uncategorized' },
		...$categories.map((c) => ({ value: c.slug, label: `${c.icon} ${c.name}`.trim() }))
	]);
	// Per-course assignment dropdown options (— = clear/uncategorized).
	const categoryAssignOptions = $derived([
		{ value: '', label: '— Uncategorized' },
		...$categories.map((c) => ({ value: c.id, label: `${c.icon} ${c.name}`.trim() }))
	]);

	// Courses filtered by the search box (title or category name) + the
	// category filter. Search and filter are view-only; the list itself is
	// server truth from the view model.
	const visibleCourses = $derived.by(() => {
		const q = courseSearch.trim().toLowerCase();
		return $courses.filter((c) => {
			const matchesSearch =
				q === '' ||
				c.title.toLowerCase().includes(q) ||
				(c.category?.name.toLowerCase().includes(q) ?? false);
			const matchesFilter =
				categoryFilter === 'all' ||
				(categoryFilter === 'uncategorized' && c.category === null) ||
				c.category?.slug === categoryFilter;
			return matchesSearch && matchesFilter;
		});
	});

	// Reorder only makes sense against the full list, so it's disabled while a
	// search/filter narrows the view.
	const filtering = $derived(courseSearch.trim() !== '' || categoryFilter !== 'all');

	async function createCategory(): Promise<void> {
		const name = newCategoryName.trim();
		if (!name) return;
		const ok = await vm.makeCategory({
			name,
			icon: newCategoryIcon.trim() || undefined,
			parentId: newCategoryParent || null
		});
		if (ok) {
			newCategoryName = '';
			newCategoryIcon = '';
			newCategoryParent = '';
		}
	}

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

	// ── Languages / translations ──────────────────────────────────────
	let langInfo = $state<CourseLanguages | null>(null);
	let langSlug = $state<string | null>(null);
	let langLoading = $state(false);
	let langError = $state<string | null>(null);
	let translating = $state<string[]>([]); // languages with an in-flight job

	function localeLabel(code: string): string {
		return SUPPORTED_LOCALES.find((l) => l.code === code)?.nativeLabel ?? code;
	}
	function localeFlag(code: string): string {
		return SUPPORTED_LOCALES.find((l) => l.code === code)?.flag ?? '🏳️';
	}

	async function loadLanguages(slug: string): Promise<void> {
		langLoading = true;
		langError = null;
		try {
			langInfo = await fetchCourseLanguages(slug);
		} catch (e) {
			langError = e instanceof Error ? e.message : String(e);
		} finally {
			langLoading = false;
		}
	}

	// Load the available languages whenever the open course changes.
	$effect(() => {
		const c = $selected;
		if (c && c.slug !== langSlug) {
			langSlug = c.slug;
			langInfo = null;
			translating = [];
			void loadLanguages(c.slug);
		}
	});

	// Trigger a background translation, then poll until the language lands.
	async function doTranslate(language: string): Promise<void> {
		const c = $selected;
		if (!c || translating.includes(language)) return;
		translating = [...translating, language];
		langError = null;
		try {
			await translateCourse(c.slug, language);
			// The job runs server-side; the language appears in `available`
			// once it finishes. Poll for a few minutes (big courses are slow).
			for (let i = 0; i < 90; i++) {
				await new Promise((r) => setTimeout(r, 4000));
				if (langSlug !== c.slug) return; // user switched courses — stop
				const info = await fetchCourseLanguages(c.slug);
				langInfo = info;
				if (info.available.includes(language)) break;
			}
		} catch (e) {
			langError = e instanceof Error ? e.message : String(e);
		} finally {
			translating = translating.filter((l) => l !== language);
		}
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
		{#if $notice}
			<p class="banner banner--ok" role="status">{$notice}</p>
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

				<!-- Languages / translations -->
				<div class="new-course">
					<h2>Languages</h2>
					{#if langLoading && !langInfo}
						<p class="hint">Loading languages…</p>
					{:else if langInfo}
						<div class="langs">
							{#each langInfo.supported as code (code)}
								{@const available = langInfo.available.includes(code)}
								{@const inProgress = translating.includes(code)}
								<div class="langrow" class:langrow--on={available}>
									<span class="langrow__flag" aria-hidden="true">{localeFlag(code)}</span>
									<span class="langrow__name">{localeLabel(code)}</span>
									{#if code === 'en'}
										<Badge variant="neutral" size="sm">source</Badge>
									{:else if available}
										<Badge variant="success" size="sm">✓ translated</Badge>
									{:else}
										<Badge variant="warning" size="sm">not translated</Badge>
									{/if}
									{#if code !== 'en' && langInfo.canTranslate}
										<PixelButton
											variant="outline"
											size="sm"
											disabled={inProgress}
											onclick={() => doTranslate(code)}
										>
											{inProgress ? 'Translating…' : available ? 'Re-translate' : 'Translate'}
										</PixelButton>
									{/if}
								</div>
							{/each}
						</div>
						{#if translating.length > 0}
							<p class="hint">Translating in the background — this can take a few minutes per course.</p>
						{/if}
						{#if !langInfo.canTranslate}
							<p class="hint">Translation is unavailable (no AI key configured on the server).</p>
						{/if}
					{/if}
					{#if langError}<p class="hint err">{langError}</p>{/if}
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

			<!-- Categories -->
			{#snippet categoryRow(cat: (typeof $categories)[number], child: boolean)}
				<li class="cat" class:cat--child={child}>
					<span class="cat__name">{cat.icon} {cat.name}</span>
					<span class="cat__slug">{cat.slug}</span>
					<span class="cat__parent">
						<Select
							value={cat.parentId ?? ''}
							options={parentOptions.filter((o) => o.value !== cat.id)}
							onchange={(e) =>
								vm.editCategory(cat.id, {
									parentId: (e.target as HTMLSelectElement).value || null
								})}
						/>
					</span>
					{#if confirmingCategoryDelete === cat.id}
						<PixelButton
							variant="solid"
							size="sm"
							disabled={$busy}
							onclick={async () => {
								await vm.removeCategory(cat.id);
								confirmingCategoryDelete = null;
							}}
						>
							Confirm
						</PixelButton>
						<PixelButton variant="ghost" size="sm" onclick={() => (confirmingCategoryDelete = null)}>
							Cancel
						</PixelButton>
					{:else}
						<PixelButton
							variant="ghost"
							size="sm"
							disabled={$busy}
							onclick={() => (confirmingCategoryDelete = cat.id)}
						>
							Delete
						</PixelButton>
					{/if}
				</li>
			{/snippet}
			<div class="new-course">
				<h2>Categories</h2>
				<p class="hint">
					Categories group courses in the catalogue. A category can sit under a parent group
					(one level). Deleting one leaves its courses uncategorized and promotes any
					sub-categories to top level — it never deletes courses.
				</p>
				{#if categoryTree.length > 0}
					<ul class="cat-list">
						{#each categoryTree as node (node.top.id)}
							{@render categoryRow(node.top, false)}
							{#each node.children as child (child.id)}
								{@render categoryRow(child, true)}
							{/each}
						{/each}
					</ul>
				{/if}
				<form
					class="row row--end"
					onsubmit={(e) => {
						e.preventDefault();
						void createCategory();
					}}
				>
					<div class="grow">
						<PixelInput placeholder="New category name" bind:value={newCategoryName} ariaLabel="New category name" />
					</div>
					<div class="cat-icon">
						<PixelInput placeholder="Icon" bind:value={newCategoryIcon} ariaLabel="Category icon (emoji)" />
					</div>
					<div class="toolbar__filter">
						<Select
							label="Parent group"
							value={newCategoryParent}
							options={parentOptions}
							onchange={(e) => (newCategoryParent = (e.target as HTMLSelectElement).value)}
						/>
					</div>
					<PixelButton type="submit" variant="solid" size="sm" disabled={$busy || !newCategoryName.trim()}>
						Add category
					</PixelButton>
				</form>
			</div>

			<!-- Course list -->
			<h2>Courses</h2>
			<div class="toolbar">
				<div class="grow">
					<PixelInput placeholder="Search courses by name or category…" bind:value={courseSearch} ariaLabel="Search courses" />
				</div>
				<div class="toolbar__filter">
					<Select
						label="Category"
						value={categoryFilter}
						options={categoryFilterOptions}
						onchange={(e) => (categoryFilter = (e.target as HTMLSelectElement).value)}
					/>
				</div>
			</div>
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
			{:else if visibleCourses.length === 0}
				<p class="hint">No courses match your search/filter.</p>
			{:else}
				<ul class="list">
					{#each visibleCourses as course, ci (course.id)}
						<li class="item item--{course.status}">
							<div class="item__main">
								<Badge variant={STATUS_VARIANT[course.status]} size="sm">{course.status}</Badge>
								<span class="item__title">{course.title}</span>
								<span class="item__meta">{course.level} · {course.lessonCount} lessons</span>
								<span class="item__cat">{course.category ? `${course.category.icon} ${course.category.name}` : '— uncategorized'}</span>
							</div>
							<div class="item__actions">
								<span class="item__reorder">
									<PixelButton variant="ghost" size="sm" ariaLabel="Move course up" disabled={$busy || filtering || ci === 0} onclick={() => vm.moveCourse(course.slug, 'up')}>
										▲
									</PixelButton>
									<PixelButton variant="ghost" size="sm" ariaLabel="Move course down" disabled={$busy || filtering || ci === visibleCourses.length - 1} onclick={() => vm.moveCourse(course.slug, 'down')}>
										▼
									</PixelButton>
								</span>
								<span class="item__assign">
									<Select
										value={course.category?.id ?? ''}
										options={categoryAssignOptions}
										onchange={(e) =>
											vm.assignCategory(course.slug, (e.target as HTMLSelectElement).value || null)}
									/>
								</span>
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
								{#if confirmingDelete === course.slug}
									<PixelButton
										variant="solid"
										size="sm"
										disabled={$busy}
										onclick={async () => {
											await vm.remove(course.slug);
											confirmingDelete = null;
										}}
									>
										Confirm
									</PixelButton>
									<PixelButton variant="ghost" size="sm" onclick={() => (confirmingDelete = null)}>
										Cancel
									</PixelButton>
								{:else}
									<PixelButton variant="ghost" size="sm" disabled={$busy} onclick={() => (confirmingDelete = course.slug)}>
										Delete
									</PixelButton>
								{/if}
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
		color: #000000;
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
		color: #374151;
	}
	.banner {
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		font-size: 0.85rem;
		margin-bottom: 0.75rem;
	}
	.banner--error {
		background: #fee2e2;
		color: #991b1b;
	}
	.banner--warn {
		background: #fef3c7;
		color: #92400e;
	}
	.banner--ok {
		background: #dcfce7;
		color: #166534;
	}
	.new-course {
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.85rem;
		margin-bottom: 1.25rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.18);
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
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 6px;
		padding: 0.55rem 0.7rem 0.55rem 0;
		/* Status accent stripe on the left edge. */
		border-left-width: 6px;
		transition: border-color 0.12s ease;
	}
	.item--published {
		border-left-color: #22c55e;
	}
	.item--draft {
		border-left-color: #f59e0b;
	}
	.item:hover {
		border-color: #3b82f6;
	}
	.item__main {
		display: flex;
		gap: 0.55rem;
		align-items: center;
		min-width: 0;
		flex-wrap: wrap;
		padding-left: 0.7rem;
	}
	.item__title {
		font-size: 0.92rem;
		font-weight: 700;
	}
	.item__meta {
		font-size: 0.72rem;
		color: #6b7280;
	}
	.item__cat {
		font-size: 0.72rem;
		color: #6d28d9;
		font-weight: 600;
	}
	.item__assign {
		min-width: 150px;
	}
	/* Search + category filter toolbar above the course list. */
	.toolbar {
		display: flex;
		gap: 0.6rem;
		align-items: flex-end;
		flex-wrap: wrap;
		margin-bottom: 0.6rem;
	}
	.toolbar__filter {
		min-width: 180px;
	}
	/* Category management list. */
	.cat-list {
		list-style: none;
		margin: 0 0 0.6rem;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}
	.cat {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		padding: 0.3rem 0.5rem;
		border: 1px solid #e5e7eb;
		border-radius: 6px;
	}
	.cat__name {
		font-weight: 600;
	}
	.cat__slug {
		font-size: 0.72rem;
		color: #9ca3af;
		margin-right: auto;
	}
	.cat--child {
		margin-left: 1.4rem;
		border-left: 3px solid #c7d2fe;
	}
	.cat__parent {
		min-width: 160px;
	}
	.cat-icon {
		width: 70px;
		flex-shrink: 0;
	}
	.item__actions {
		display: flex;
		gap: 0.4rem;
		flex-shrink: 0;
		align-items: center;
		flex-wrap: wrap;
		justify-content: flex-end;
	}
	/* Stack the ▲▼ reorder controls tightly so they read as one control. */
	.item__reorder {
		display: inline-flex;
		flex-direction: column;
		border: 2px solid #000;
		border-radius: 5px;
		overflow: hidden;
	}
	.item__reorder :global(button) {
		padding: 0 0.35rem;
		line-height: 1.1;
	}
	.hint {
		color: #374151;
		font-size: 0.85rem;
	}
	.hint.err {
		color: #991b1b;
	}
	.langs {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.langrow {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		padding: 0.45rem 0.6rem;
		border: 2px solid #000000;
		border-radius: 6px;
		background: #f3f4f6;
	}
	.langrow--on {
		background: #dcfce7;
	}
	.langrow__flag {
		font-size: 1.1rem;
	}
	.langrow__name {
		flex: 1;
		font-weight: 600;
		font-size: 0.9rem;
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
		color: #374151;
		margin-bottom: 0.75rem;
	}
	.num {
		width: 5rem;
		background: #f3f4f6;
		border: 2px solid #000000;
		border-radius: 5px;
		color: #000000;
		padding: 0.4rem 0.55rem;
		font: inherit;
		box-sizing: border-box;
	}
	.dt-field {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		font-size: 0.78rem;
		color: #374151;
	}
	.dt {
		background: #f3f4f6;
		border: 2px solid #000000;
		border-radius: 5px;
		color: #000000;
		padding: 0.4rem 0.55rem;
		font: inherit;
		box-sizing: border-box;
	}
	.qcard {
		background: #ffffff;
		border: 2px solid #000000;
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
