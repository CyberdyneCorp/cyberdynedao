<script lang="ts">
	/**
	 * Cyberdyne-OS Start menu.
	 *
	 * Replaces the flat svelte-ui-core ``StartMenu`` with a sectioned
	 * dark panel matching the design spec: a header tile, account row
	 * (wallet/email + copy), search, MAIN / BUSINESS / CONTENT / SYSTEM
	 * sections with icons + chevrons + badges, and a hover submenu for
	 * items that expose children.
	 *
	 * Routing stays on the same contract: clicking an item calls
	 * ``onItemSelect(id)``; the shell's ``handleStartSelect`` decides
	 * what to do (open a window via viewMap, openCart, logout, …).
	 */
	import { onMount, tick } from 'svelte';
	import { Badge } from '@cyberdynecorp/svelte-ui-core';
	import type { StartMenuSection } from './StartMenu.types';

	interface Props {
		sections: StartMenuSection[];
		open?: boolean;
		header?: string;
		tagline?: string;
		/** "Connected" indicator + identity shown at the top. */
		connected?: boolean;
		identity?: string | null;
		/** Full address shown to the copy button (e.g. wallet). */
		identityFull?: string | null;
		onItemSelect?: (id: string) => void;
	}

	let {
		sections,
		open = $bindable(false),
		header = 'CYBERDYNE OS',
		tagline = 'Open infra for AI + Web3',
		connected = false,
		identity = null,
		identityFull = null,
		onItemSelect
	}: Props = $props();

	let search = $state('');
	let hoveredId = $state<string | null>(null);
	let copied = $state(false);
	let searchEl = $state<HTMLInputElement | null>(null);

	const filteredSections = $derived.by(() => {
		const q = search.trim().toLowerCase();
		if (!q) return sections;
		return sections
			.map((s) => ({
				...s,
				items: s.items.filter((i) => i.label.toLowerCase().includes(q))
			}))
			.filter((s) => s.items.length > 0);
	});

	function toggle() {
		open = !open;
	}

	function pick(id: string) {
		onItemSelect?.(id);
		open = false;
	}

	async function copyIdentity() {
		if (!identityFull) return;
		try {
			await navigator.clipboard.writeText(identityFull);
			copied = true;
			setTimeout(() => (copied = false), 1200);
		} catch {
			/* clipboard denied — ignore */
		}
	}

	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape' && open) {
			open = false;
			return;
		}
		// Cmd/Ctrl+K opens the menu and focuses search (matches the
		// mockup's ⌘K hint).
		if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
			e.preventDefault();
			open = true;
			void tick().then(() => searchEl?.focus());
		}
	}

	function onDocClick(e: MouseEvent) {
		const t = e.target as HTMLElement | null;
		if (!t || !t.closest('.start-menu')) open = false;
	}

	onMount(() => {
		document.addEventListener('keydown', onKey);
		return () => document.removeEventListener('keydown', onKey);
	});

	$effect(() => {
		if (open) {
			document.addEventListener('click', onDocClick);
			void tick().then(() => searchEl?.focus());
			return () => document.removeEventListener('click', onDocClick);
		}
	});
</script>

<div class="start-menu">
	<button
		type="button"
		class="trigger"
		class:trigger--open={open}
		onclick={toggle}
		aria-haspopup="menu"
		aria-expanded={open}
	>
		<span class="trigger__label">Start</span>
		<span class="trigger__arrow" aria-hidden="true">{open ? '▼' : '▶'}</span>
	</button>

	{#if open}
		<div class="panel" role="menu" aria-label={header}>
			<header class="head">
				<div class="head__icon" aria-hidden="true">◼</div>
				<div class="head__text">
					<div class="head__title">{header}</div>
					<div class="head__sub">{tagline}</div>
				</div>
				<span class="head__corner" aria-hidden="true">↗</span>
			</header>

			<div class="account" class:account--off={!connected}>
				<span class="dot" class:dot--ok={connected}></span>
				<span class="account__text">
					{connected ? 'Account Connected' : 'Not signed in'}
				</span>
				{#if connected && identity}
					<span class="account__id" title={identityFull ?? identity}>{identity}</span>
					{#if identityFull}
						<button
							type="button"
							class="account__copy"
							onclick={copyIdentity}
							aria-label={copied ? 'Copied' : 'Copy address'}
							title={copied ? 'Copied!' : 'Copy address'}
						>
							{copied ? '✓' : '⧉'}
						</button>
					{/if}
				{/if}
			</div>

			<label class="search">
				<span class="search__icon" aria-hidden="true">⌕</span>
				<input
					bind:this={searchEl}
					bind:value={search}
					type="text"
					class="search__input"
					placeholder="Search Cyberdyne OS…"
					autocomplete="off"
					spellcheck="false"
				/>
				<kbd class="search__kbd">⌘K</kbd>
			</label>

			<div class="sections">
				{#each filteredSections as section (section.id)}
					<div class="section">
						<div class="section__label">{section.label}</div>
						{#each section.items as item (item.id)}
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<div
								class="item"
								class:item--has-sub={!!item.children}
								onmouseenter={() => (hoveredId = item.id)}
								onmouseleave={() => {
									if (hoveredId === item.id) hoveredId = null;
								}}
							>
								<button
									type="button"
									class="item__main"
									role="menuitem"
									onclick={() => pick(item.id)}
									onfocus={() => (hoveredId = item.id)}
								>
									<span class="item__icon" aria-hidden="true">{item.icon}</span>
									<span class="item__label">{item.label}</span>
									{#if item.badge !== undefined && item.badge > 0}
										<Badge variant="info" size="sm">{item.badge}</Badge>
									{/if}
									{#if item.children}
										<span class="item__chev" aria-hidden="true">›</span>
									{/if}
								</button>
								{#if item.children && hoveredId === item.id}
									<div class="submenu" role="menu" aria-label={`${item.label} submenu`}>
										<div class="submenu__head">{item.label.toUpperCase()}</div>
										{#each item.children as sub (sub.id)}
											<button
												type="button"
												class="submenu__item"
												role="menuitem"
												onclick={() => pick(sub.id)}
											>
												<span class="submenu__icon" aria-hidden="true">{sub.icon}</span>
												<span>{sub.label}</span>
											</button>
										{/each}
									</div>
								{/if}
							</div>
						{/each}
					</div>
				{/each}
				{#if filteredSections.length === 0}
					<p class="empty">No matches for "{search}".</p>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.start-menu {
		position: relative;
		display: inline-block;
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
	}

	/* ── Trigger button ─────────────────────────────────────────── */
	.trigger {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 6px 14px;
		background: rgba(255, 255, 255, 0.18);
		border: 2px solid #000;
		color: #fff;
		font-weight: 600;
		font-family: inherit;
		cursor: pointer;
	}
	.trigger:hover,
	.trigger--open {
		background: rgba(255, 255, 255, 0.3);
	}
	.trigger__arrow {
		font-size: 0.75em;
	}

	/* ── Panel ──────────────────────────────────────────────────── */
	.panel {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		width: 320px;
		max-height: min(80vh, 620px);
		overflow-y: auto;
		background: #0b1130;
		color: #e0e7ff;
		border: 2px solid #1e3a8a;
		box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.55);
		z-index: 200;
		padding: 10px;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	/* ── Header tile ────────────────────────────────────────────── */
	.head {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 10px;
		align-items: center;
		padding: 10px 12px;
		background: linear-gradient(135deg, #111c3f 0%, #1e3a8a 100%);
		border: 1.5px solid #312e81;
	}
	.head__icon {
		width: 32px;
		height: 32px;
		display: grid;
		place-items: center;
		background: #4f46e5;
		border: 1.5px solid #1e1b4b;
		color: #fff;
		font-size: 1.1rem;
	}
	.head__title {
		font-weight: 800;
		letter-spacing: 0.08em;
		color: #fff;
	}
	.head__sub {
		font-size: 0.7rem;
		color: #c7d2fe;
		margin-top: 2px;
	}
	.head__corner {
		color: #c7d2fe;
		font-size: 0.9rem;
	}

	/* ── Account row ────────────────────────────────────────────── */
	.account {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 4px 4px 8px;
		font-size: 0.7rem;
		color: #c7d2fe;
		border-bottom: 1px solid #1e293b;
	}
	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #64748b;
		flex: 0 0 auto;
		box-shadow: 0 0 6px rgba(100, 116, 139, 0.4);
	}
	.dot--ok {
		background: #22c55e;
		box-shadow: 0 0 6px rgba(34, 197, 94, 0.7);
	}
	.account__text {
		font-weight: 600;
		color: #e0e7ff;
	}
	.account__id {
		margin-left: auto;
		font-family: inherit;
		font-size: 0.7rem;
		color: #c7d2fe;
		background: #1e1b4b;
		padding: 2px 6px;
		border: 1px solid #312e81;
		max-width: 9em;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.account__copy {
		font-family: inherit;
		background: transparent;
		border: 1px solid #312e81;
		color: #c7d2fe;
		padding: 1px 5px;
		cursor: pointer;
	}
	.account__copy:hover {
		background: #1e1b4b;
		color: #fff;
	}

	/* ── Search ─────────────────────────────────────────────────── */
	.search {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 6px 8px;
		background: #050a25;
		border: 1.5px solid #1e3a8a;
	}
	.search__icon {
		color: #93c5fd;
	}
	.search__input {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		font: inherit;
		font-size: 0.8125rem;
		color: #e0e7ff;
	}
	.search__input::placeholder {
		color: #475569;
	}
	.search__kbd {
		font-family: inherit;
		font-size: 0.625rem;
		color: #94a3b8;
		background: #1e293b;
		padding: 2px 5px;
		border: 1px solid #334155;
	}

	/* ── Sections ───────────────────────────────────────────────── */
	.sections {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}
	.section {
		display: flex;
		flex-direction: column;
		padding-top: 4px;
	}
	.section + .section {
		margin-top: 4px;
	}
	.section__label {
		font-size: 0.625rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		color: #93c5fd;
		padding: 4px 8px;
	}

	/* ── Items ──────────────────────────────────────────────────── */
	.item {
		position: relative;
	}
	.item__main {
		all: unset;
		width: 100%;
		display: grid;
		grid-template-columns: 22px 1fr auto;
		gap: 10px;
		align-items: center;
		padding: 7px 10px;
		font-size: 0.8125rem;
		color: #e0e7ff;
		border-left: 3px solid transparent;
		cursor: pointer;
		transition: background 0.1s ease, border-color 0.1s ease;
	}
	.item__main:hover,
	.item__main:focus-visible {
		background: #1e1b4b;
		border-left-color: #4f46e5;
		outline: none;
	}
	.item__icon {
		width: 22px;
		text-align: center;
		font-size: 0.95rem;
	}
	.item__label {
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.item__chev {
		color: #93c5fd;
		font-size: 1rem;
		line-height: 1;
	}

	/* ── Submenu ────────────────────────────────────────────────── */
	.submenu {
		position: absolute;
		top: 0;
		left: 100%;
		margin-left: 4px;
		min-width: 230px;
		background: #0b1130;
		color: #e0e7ff;
		border: 2px solid #1e3a8a;
		box-shadow: 5px 5px 0 rgba(0, 0, 0, 0.55);
		padding: 6px;
		display: flex;
		flex-direction: column;
		gap: 1px;
		z-index: 1;
	}
	.submenu__head {
		font-size: 0.625rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		color: #93c5fd;
		padding: 4px 8px 6px;
		border-bottom: 1px solid #1e293b;
		margin-bottom: 4px;
	}
	.submenu__item {
		all: unset;
		display: grid;
		grid-template-columns: 20px 1fr;
		gap: 10px;
		align-items: center;
		padding: 6px 8px;
		font-size: 0.8125rem;
		color: #e0e7ff;
		cursor: pointer;
	}
	.submenu__item:hover,
	.submenu__item:focus-visible {
		background: #1e1b4b;
		outline: none;
	}
	.submenu__icon {
		text-align: center;
		font-size: 0.9rem;
	}

	.empty {
		font-size: 0.75rem;
		color: #94a3b8;
		font-style: italic;
		padding: 8px;
		margin: 0;
	}
</style>
