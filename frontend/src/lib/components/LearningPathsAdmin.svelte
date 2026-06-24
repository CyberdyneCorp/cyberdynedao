<script lang="ts">
	import { onMount } from 'svelte';
	import {
		PixelButton,
		PixelInput,
		PixelCheckbox,
		Textarea,
		Select
	} from '@cyberdynecorp/svelte-ui-core';
	import { createLearningAdminViewModel } from '$lib/viewmodels/learningAdminViewModel';
	import type { CourseLevel } from '$lib/api/coursesApi';
	import type { LearningModule } from '$lib/api/adminApi';

	const vm = createLearningAdminViewModel();
	const { modules, paths, courses, busy, error, notice } = vm;

	const levels: CourseLevel[] = ['Beginner', 'Intermediate', 'Advanced'];
	const levelOptions = levels.map((l) => ({ value: l, label: l }));

	// Auto-dismiss the success notice a few seconds after it appears.
	$effect(() => {
		if ($notice) {
			const t = setTimeout(() => vm.clearNotice(), 3000);
			return () => clearTimeout(t);
		}
	});

	onMount(() => {
		void vm.load();
	});

	// Comma-separated topics ↔ string[].
	function splitTopics(value: string): string[] {
		return value
			.split(',')
			.map((t) => t.trim())
			.filter((t) => t !== '');
	}

	// Selected courses, in the course-list order.
	function selectedCourseSlugs(picks: Record<string, boolean>): string[] {
		return $courses.filter((c) => picks[c.slug]).map((c) => c.slug);
	}

	// Resolve a course slug to a display label for the module-list row.
	function courseLabel(slug: string): string {
		const c = $courses.find((x) => x.slug === slug);
		return c ? `${c.title} · ${c.level}` : slug;
	}

	// ── New-module form ────────────────────────────────────────────────
	let mTitle = $state('');
	let mCategory = $state('');
	let mLevel = $state<CourseLevel>('Beginner');
	let mDuration = $state('');
	let mIcon = $state('');
	let mDescription = $state('');
	let mTopics = $state('');
	let mCourses = $state<Record<string, boolean>>({});

	const moduleValid = $derived(!!mTitle.trim() && !!mCategory.trim());

	async function createModule(): Promise<void> {
		if (!moduleValid) return;
		const ok = await vm.createModule({
			title: mTitle.trim(),
			category: mCategory.trim(),
			level: mLevel,
			duration: mDuration.trim(),
			icon: mIcon.trim(),
			description: mDescription.trim(),
			topics: splitTopics(mTopics),
			courseSlugs: selectedCourseSlugs(mCourses)
		});
		if (ok) {
			mTitle = '';
			mCategory = '';
			mLevel = 'Beginner';
			mDuration = '';
			mIcon = '';
			mDescription = '';
			mTopics = '';
			mCourses = {};
		}
	}

	// ── Inline module edit ─────────────────────────────────────────────
	let editingModule = $state<string | null>(null);
	let emTitle = $state('');
	let emCategory = $state('');
	let emLevel = $state<CourseLevel>('Beginner');
	let emDuration = $state('');
	let emIcon = $state('');
	let emDescription = $state('');
	let emTopics = $state('');
	let emCourses = $state<Record<string, boolean>>({});
	let confirmingModuleDelete = $state<string | null>(null);

	function openModuleEdit(m: LearningModule): void {
		editingModule = m.slug;
		emTitle = m.title;
		emCategory = m.category;
		emLevel = m.level;
		emDuration = m.duration;
		emIcon = m.icon;
		emDescription = m.description;
		emTopics = m.topics.join(', ');
		emCourses = Object.fromEntries(m.courseSlugs.map((slug) => [slug, true]));
	}

	async function saveModuleEdit(): Promise<void> {
		if (!editingModule || !emTitle.trim()) return;
		const ok = await vm.editModule(editingModule, {
			title: emTitle.trim(),
			category: emCategory.trim(),
			level: emLevel,
			duration: emDuration.trim(),
			icon: emIcon.trim(),
			description: emDescription.trim(),
			topics: splitTopics(emTopics),
			courseSlugs: selectedCourseSlugs(emCourses)
		});
		if (ok) editingModule = null;
	}

	// ── New-path form ──────────────────────────────────────────────────
	let pTitle = $state('');
	let pDescription = $state('');
	let pEstimatedTime = $state('');
	let pIcon = $state('');
	let pModules = $state<Record<string, boolean>>({});

	// Selected modules, in the module-list order.
	function selectedModuleSlugs(picks: Record<string, boolean>): string[] {
		return $modules.filter((m) => picks[m.slug]).map((m) => m.slug);
	}

	const pathValid = $derived(!!pTitle.trim());

	async function createPath(): Promise<void> {
		if (!pathValid) return;
		const ok = await vm.createPath({
			title: pTitle.trim(),
			description: pDescription.trim(),
			estimatedTime: pEstimatedTime.trim(),
			icon: pIcon.trim(),
			moduleSlugs: selectedModuleSlugs(pModules)
		});
		if (ok) {
			pTitle = '';
			pDescription = '';
			pEstimatedTime = '';
			pIcon = '';
			pModules = {};
		}
	}

	// ── Inline path edit ───────────────────────────────────────────────
	let editingPath = $state<string | null>(null);
	let epTitle = $state('');
	let epDescription = $state('');
	let epEstimatedTime = $state('');
	let epIcon = $state('');
	let confirmingPathDelete = $state<string | null>(null);

	function openPathEdit(slug: string, title: string, description: string, estimatedTime: string, icon: string): void {
		editingPath = slug;
		epTitle = title;
		epDescription = description;
		epEstimatedTime = estimatedTime;
		epIcon = icon;
	}

	async function savePathEdit(): Promise<void> {
		if (!editingPath || !epTitle.trim()) return;
		const ok = await vm.editPath(editingPath, {
			title: epTitle.trim(),
			description: epDescription.trim(),
			estimatedTime: epEstimatedTime.trim(),
			icon: epIcon.trim()
		});
		if (ok) editingPath = null;
	}

	// Resolve a module slug to a display label for the path's ordered list.
	function moduleLabel(slug: string): string {
		const m = $modules.find((x) => x.slug === slug);
		return m ? `${m.icon} ${m.title}`.trim() : slug;
	}
</script>

<div class="learning-admin">
	<header class="hero">
		<span aria-hidden="true">🗺️</span>
		<div>
			<h1>Learning Paths &amp; Modules</h1>
			<p>Author reusable modules and group them into ordered learning paths.</p>
		</div>
	</header>

	{#if $error}
		<p class="banner banner--error" role="alert">{$error}</p>
	{/if}
	{#if $notice}
		<p class="banner banner--ok" role="status">{$notice}</p>
	{/if}

	<!-- ── Learning modules ───────────────────────────────────────── -->
	<form class="new-course" onsubmit={(e) => { e.preventDefault(); void createModule(); }}>
		<h2>New module</h2>
		<PixelInput placeholder="Module title" bind:value={mTitle} ariaLabel="Module title" />
		<div class="row row--end">
			<div class="grow">
				<PixelInput placeholder="Category" bind:value={mCategory} ariaLabel="Module category" />
			</div>
			<div class="grow">
				<Select
					label="Level"
					value={mLevel}
					options={levelOptions}
					onchange={(e) => (mLevel = (e.target as HTMLSelectElement).value as CourseLevel)}
				/>
			</div>
		</div>
		<div class="row row--end">
			<div class="grow">
				<PixelInput placeholder="Duration (e.g. 2h)" bind:value={mDuration} ariaLabel="Module duration" />
			</div>
			<div class="cat-icon">
				<PixelInput placeholder="Icon" bind:value={mIcon} ariaLabel="Module icon (emoji)" />
			</div>
		</div>
		<Textarea label="Description" rows={2} bind:value={mDescription} />
		<PixelInput placeholder="Topics (comma-separated)" bind:value={mTopics} ariaLabel="Module topics" />
		<fieldset class="modules-pick">
			<legend>Courses in this stage</legend>
			{#if $courses.length === 0}
				<p class="hint">No published courses available yet.</p>
			{:else}
				{#each $courses as c (c.slug)}
					<PixelCheckbox bind:checked={mCourses[c.slug]} label={`${c.title} · ${c.level}`} />
				{/each}
			{/if}
		</fieldset>
		<PixelButton type="submit" variant="solid" disabled={$busy || !moduleValid}>
			{$busy ? 'Saving…' : 'Create module'}
		</PixelButton>
	</form>

	<h2>Learning modules</h2>
	{#if $modules.length === 0}
		<p class="hint">No modules yet — create your first one above.</p>
	{:else}
		<ul class="list">
			{#each $modules as m (m.slug)}
				<li class="item">
					<div class="item__main">
						<span class="item__title">{m.icon} {m.title}</span>
						<span class="item__meta">{m.category} · {m.level} · {m.duration}</span>
						{#if m.topics.length > 0}<span class="item__cat">{m.topics.join(', ')}</span>{/if}
						{#if m.courseSlugs.length > 0}<span class="item__courses">Courses: {m.courseSlugs.map((s) => courseLabel(s)).join(', ')}</span>{/if}
					</div>
					<div class="item__actions">
						<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => openModuleEdit(m)}>
							Edit
						</PixelButton>
						{#if confirmingModuleDelete === m.slug}
							<PixelButton
								variant="solid"
								size="sm"
								disabled={$busy}
								onclick={async () => {
									await vm.removeModule(m.slug);
									confirmingModuleDelete = null;
								}}
							>
								Confirm
							</PixelButton>
							<PixelButton variant="ghost" size="sm" onclick={() => (confirmingModuleDelete = null)}>
								Cancel
							</PixelButton>
						{:else}
							<PixelButton variant="ghost" size="sm" disabled={$busy} onclick={() => (confirmingModuleDelete = m.slug)}>
								Delete
							</PixelButton>
						{/if}
					</div>
				</li>
				{#if editingModule === m.slug}
					<li class="edit-row">
						<form class="new-course" onsubmit={(e) => { e.preventDefault(); void saveModuleEdit(); }}>
							<h2>Edit module</h2>
							<PixelInput placeholder="Module title" bind:value={emTitle} ariaLabel="Module title" />
							<div class="row row--end">
								<div class="grow">
									<PixelInput placeholder="Category" bind:value={emCategory} ariaLabel="Module category" />
								</div>
								<div class="grow">
									<Select
										label="Level"
										value={emLevel}
										options={levelOptions}
										onchange={(e) => (emLevel = (e.target as HTMLSelectElement).value as CourseLevel)}
									/>
								</div>
							</div>
							<div class="row row--end">
								<div class="grow">
									<PixelInput placeholder="Duration" bind:value={emDuration} ariaLabel="Module duration" />
								</div>
								<div class="cat-icon">
									<PixelInput placeholder="Icon" bind:value={emIcon} ariaLabel="Module icon (emoji)" />
								</div>
							</div>
							<Textarea label="Description" rows={2} bind:value={emDescription} />
							<PixelInput placeholder="Topics (comma-separated)" bind:value={emTopics} ariaLabel="Module topics" />
							<fieldset class="modules-pick">
								<legend>Courses in this stage</legend>
								{#if $courses.length === 0}
									<p class="hint">No published courses available yet.</p>
								{:else}
									{#each $courses as c (c.slug)}
										<PixelCheckbox bind:checked={emCourses[c.slug]} label={`${c.title} · ${c.level}`} />
									{/each}
								{/if}
							</fieldset>
							<div class="row">
								<PixelButton type="submit" variant="solid" size="sm" disabled={$busy || !emTitle.trim()}>
									{$busy ? 'Saving…' : 'Save module'}
								</PixelButton>
								<PixelButton variant="ghost" size="sm" onclick={() => (editingModule = null)}>Cancel</PixelButton>
							</div>
						</form>
					</li>
				{/if}
			{/each}
		</ul>
	{/if}

	<!-- ── Learning paths ─────────────────────────────────────────── -->
	<form class="new-course" onsubmit={(e) => { e.preventDefault(); void createPath(); }}>
		<h2>New path</h2>
		<PixelInput placeholder="Path title" bind:value={pTitle} ariaLabel="Path title" />
		<Textarea label="Description" rows={2} bind:value={pDescription} />
		<div class="row row--end">
			<div class="grow">
				<PixelInput placeholder="Estimated time (e.g. 6h)" bind:value={pEstimatedTime} ariaLabel="Estimated time" />
			</div>
			<div class="cat-icon">
				<PixelInput placeholder="Icon" bind:value={pIcon} ariaLabel="Path icon (emoji)" />
			</div>
		</div>
		<fieldset class="modules-pick">
			<legend>Modules in this path</legend>
			{#if $modules.length === 0}
				<p class="hint">Create modules first to add them to a path.</p>
			{:else}
				{#each $modules as m (m.slug)}
					<PixelCheckbox bind:checked={pModules[m.slug]} label={`${m.icon} ${m.title}`.trim()} />
				{/each}
			{/if}
		</fieldset>
		<PixelButton type="submit" variant="solid" disabled={$busy || !pathValid}>
			{$busy ? 'Saving…' : 'Create path'}
		</PixelButton>
	</form>

	<h2>Learning paths</h2>
	{#if $paths.length === 0}
		<p class="hint">No paths yet — create your first one above.</p>
	{:else}
		<ul class="list">
			{#each $paths as p (p.slug)}
				<li class="item item--block">
					<div class="path__head">
						<span class="item__title">{p.icon} {p.title}</span>
						<span class="item__meta">{p.estimatedTime} · {p.moduleSlugs.length} modules</span>
						<div class="item__actions">
							<PixelButton variant="outline" size="sm" disabled={$busy} onclick={() => openPathEdit(p.slug, p.title, p.description, p.estimatedTime, p.icon)}>
								Edit
							</PixelButton>
							{#if confirmingPathDelete === p.slug}
								<PixelButton
									variant="solid"
									size="sm"
									disabled={$busy}
									onclick={async () => {
										await vm.removePath(p.slug);
										confirmingPathDelete = null;
									}}
								>
									Confirm
								</PixelButton>
								<PixelButton variant="ghost" size="sm" onclick={() => (confirmingPathDelete = null)}>
									Cancel
								</PixelButton>
							{:else}
								<PixelButton variant="ghost" size="sm" disabled={$busy} onclick={() => (confirmingPathDelete = p.slug)}>
									Delete
								</PixelButton>
							{/if}
						</div>
					</div>
					{#if p.description}<p class="path__desc">{p.description}</p>{/if}
					{#if p.moduleSlugs.length === 0}
						<p class="hint">No modules in this path yet.</p>
					{:else}
						<ul class="path__modules">
							{#each p.moduleSlugs as slug, mi (slug)}
								<li class="path__module">
									<span class="item__reorder">
										<PixelButton variant="ghost" size="sm" ariaLabel="Move module up" disabled={$busy || mi === 0} onclick={() => vm.movePathModule(p.slug, slug, 'up')}>
											▲
										</PixelButton>
										<PixelButton variant="ghost" size="sm" ariaLabel="Move module down" disabled={$busy || mi === p.moduleSlugs.length - 1} onclick={() => vm.movePathModule(p.slug, slug, 'down')}>
											▼
										</PixelButton>
									</span>
									<span class="path__module-name">{moduleLabel(slug)}</span>
								</li>
							{/each}
						</ul>
					{/if}
					{#if editingPath === p.slug}
						<form class="new-course" onsubmit={(e) => { e.preventDefault(); void savePathEdit(); }}>
							<h2>Edit path</h2>
							<PixelInput placeholder="Path title" bind:value={epTitle} ariaLabel="Path title" />
							<Textarea label="Description" rows={2} bind:value={epDescription} />
							<div class="row row--end">
								<div class="grow">
									<PixelInput placeholder="Estimated time" bind:value={epEstimatedTime} ariaLabel="Estimated time" />
								</div>
								<div class="cat-icon">
									<PixelInput placeholder="Icon" bind:value={epIcon} ariaLabel="Path icon (emoji)" />
								</div>
							</div>
							<div class="row">
								<PixelButton type="submit" variant="solid" size="sm" disabled={$busy || !epTitle.trim()}>
									{$busy ? 'Saving…' : 'Save path'}
								</PixelButton>
								<PixelButton variant="ghost" size="sm" onclick={() => (editingPath = null)}>Cancel</PixelButton>
							</div>
						</form>
					{/if}
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.learning-admin {
		color: #000000;
		font-family: system-ui, sans-serif;
	}
	.hero {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		margin: 1.5rem 0 1rem;
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
	.learning-admin > h2 {
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
	.cat-icon {
		width: 70px;
		flex-shrink: 0;
	}
	.list {
		list-style: none;
		margin: 0 0 1.25rem;
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
		padding: 0.55rem 0.7rem;
		transition: border-color 0.12s ease;
	}
	.item:hover {
		border-color: #3b82f6;
	}
	.item--block {
		flex-direction: column;
		align-items: stretch;
	}
	.item__main {
		display: flex;
		gap: 0.55rem;
		align-items: center;
		min-width: 0;
		flex-wrap: wrap;
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
	.item__courses {
		font-size: 0.72rem;
		color: #1d4ed8;
		font-weight: 600;
	}
	.item__actions {
		display: flex;
		gap: 0.4rem;
		flex-shrink: 0;
		align-items: center;
		flex-wrap: wrap;
		justify-content: flex-end;
	}
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
	.edit-row {
		list-style: none;
	}
	.edit-row .new-course {
		margin-bottom: 0.45rem;
	}
	.modules-pick {
		border: 1px solid #e5e7eb;
		border-radius: 6px;
		padding: 0.5rem 0.7rem;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}
	.modules-pick legend {
		font-size: 0.78rem;
		font-weight: 600;
		color: #374151;
		padding: 0 0.3rem;
	}
	.path__head {
		display: flex;
		gap: 0.55rem;
		align-items: center;
		flex-wrap: wrap;
	}
	.path__head .item__actions {
		margin-left: auto;
	}
	.path__desc {
		margin: 0.35rem 0 0;
		font-size: 0.82rem;
		color: #374151;
	}
	.path__modules {
		list-style: none;
		margin: 0.5rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}
	.path__module {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		padding: 0.3rem 0.5rem;
		border: 1px solid #e5e7eb;
		border-radius: 6px;
	}
	.path__module-name {
		font-size: 0.85rem;
		font-weight: 600;
	}
</style>
