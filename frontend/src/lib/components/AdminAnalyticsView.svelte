<script lang="ts">
	import { PixelScrollArea, StatCard } from '@cyberdynecorp/svelte-ui-core';
	import { createAdminAnalyticsViewModel } from '$lib/viewmodels/adminAnalyticsViewModel';
	import { authVM } from '$lib/auth/authViewModel.svelte';

	const vm = createAdminAnalyticsViewModel();
	const { overview, loading, error } = vm;

	const canAccess = $derived(
		authVM.isRestored && authVM.isAuthenticated && (authVM.isAdmin || authVM.isEditor)
	);

	// One-shot load when access is available (see AdminView's shouldAutoLoad
	// note: don't key auto-load on the result, or it loops).
	let loadAttempted = $state(false);
	$effect(() => {
		if (canAccess && !loadAttempted && !$loading) {
			loadAttempted = true;
			void vm.load();
		}
	});

	// Rates may arrive as a 0–1 fraction or already as a percentage;
	// normalise either to a whole-number percent.
	const pct = (x: number) => `${Math.round(x <= 1 ? x * 100 : x)}%`;
	const score = (x: number) => `${Math.round(x * 10) / 10}`;
</script>

<PixelScrollArea maxHeight="100%" ariaLabel="Admin analytics">
	<div class="analytics-view">
		<header class="hero">
			<span aria-hidden="true">📊</span>
			<div>
				<h1>Academy Analytics</h1>
				<p>Platform-wide learning metrics.</p>
			</div>
		</header>

		{#if !authVM.isRestored}
			<p class="hint">Checking your session…</p>
		{:else if !canAccess}
			<p class="banner banner--warn" role="alert">
				This dashboard is restricted to <strong>admin</strong> accounts.
			</p>
		{:else if $loading && !$overview}
			<p class="hint">Loading…</p>
		{:else if $error && !$overview}
			<p class="banner banner--error" role="alert">Couldn't load analytics: {$error}</p>
			<button class="retry" onclick={() => void vm.load()}>Retry</button>
		{:else if $overview}
			{@const o = $overview}
			<div class="grid">
				<StatCard
					icon="👥"
					title="Learners"
					primary={o.totalLearners}
					rows={[
						{ label: 'Enrollments', value: o.totalEnrollments },
						{ label: 'Completed', value: o.completedEnrollments, accent: 'success' },
						{ label: 'Completion', value: pct(o.enrollmentCompletionRate) }
					]}
				/>
				<StatCard
					icon="📚"
					title="Courses"
					primary={o.publishedCourses}
					primaryAccent="brand"
					rows={[
						{ label: 'Drafts', value: o.draftCourses },
						{ label: 'Modules', value: o.totalModules },
						{ label: 'Paths', value: o.totalPaths }
					]}
				/>
				<StatCard
					icon="🎓"
					title="Certificates"
					primary={o.totalCertificates}
					primaryAccent="success"
				/>
				<StatCard
					icon="🧠"
					title="Quizzes"
					primary={o.totalQuizAttempts}
					rows={[
						{ label: 'Pass rate', value: pct(o.quizPassRate), accent: 'info' },
						{ label: 'Avg score', value: score(o.avgQuizScore) }
					]}
				/>
			</div>
		{/if}
	</div>
</PixelScrollArea>

<style>
	.analytics-view {
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
	.banner--warn {
		background: #fef3c7;
		color: #92400e;
	}
	.banner--error {
		background: #fee2e2;
		color: #991b1b;
	}
	.hint {
		font-size: 0.85rem;
		color: #374151;
	}
	.retry {
		font-size: 0.78rem;
		padding: 0.35rem 0.7rem;
		border-radius: 5px;
		border: 1px solid #374151;
		background: #d4d4d8;
		color: #000000;
		cursor: pointer;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
		gap: 0.75rem;
	}
</style>
