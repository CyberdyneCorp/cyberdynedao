<script lang="ts">
	import { onMount } from 'svelte';
	import { createAdminViewModel } from '$lib/viewmodels/adminViewModel';
	import type { CourseLevel } from '$lib/api/coursesApi';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const vm = createAdminViewModel();
	const { courses, loading, busy, error } = vm;

	const canEdit = $derived(authVM.isRestored && authVM.isAuthenticated && authVM.isEditor);

	// New-course form.
	let title = $state('');
	let description = $state('');
	let level = $state<CourseLevel>('Beginner');

	const levels: CourseLevel[] = ['Beginner', 'Intermediate', 'Advanced'];

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
</style>
