<script lang="ts">
	/**
	 * Cyberdyne-OS Start menu — sectioned dark launcher.
	 *
	 * Layout matches the design mock:
	 *   header tile (title + tagline + pixel cube)
	 *   search input (⌘K opens + focuses it)
	 *   sections: CORE / ECOSYSTEM / LEARN / SYSTEM
	 *     - per-section label colour (CORE green, others blue)
	 *     - items render an icon + label + optional subtitle line
	 *     - items with `children` reveal a right-hand submenu on hover
	 *   account row pinned at the bottom (status + short identity + copy)
	 *
	 * Clicking an item calls ``onItemSelect(id)`` — the shell decides
	 * what each id means (open a window via viewMap, openCart, logout…).
	 */
	import { onMount, tick } from 'svelte';
	import type { StartMenuSection } from './StartMenu.types';

	interface Props {
		sections: StartMenuSection[];
		open?: boolean;
		header?: string;
		tagline?: string;
		connected?: boolean;
		identity?: string | null;
		identityFull?: string | null;
		onItemSelect?: (id: string) => void;
	}

	let {
		sections,
		open = $bindable(false),
		header = 'CYBERDYNE OS',
		tagline = 'Open infrastructure for AI, Web3, DeFi and beyond.',
		connected = false,
		identity = null,
		identityFull = null,
		onItemSelect
	}: Props = $props();

	let search = $state('');
	let hoveredId = $state<string | null>(null);
	let copied = $state(false);
	let searchEl = $state<HTMLInputElement | null>(null);
	// Submenu anchors against the viewport (position: fixed) so the
	// inner scroll container can't clip it. Position is recomputed on
	// each hover; auto-flips to the left of the item when there isn't
	// room on the right.
	let submenuTop = $state(0);
	let submenuLeft = $state(0);
	const SUBMENU_W = 280;
	const SUBMENU_GAP = 8;

	function placeSubmenu(target: EventTarget | null): void {
		const btn = target instanceof Element ? (target.closest('.item') as HTMLElement | null) : null;
		if (!btn) return;
		const r = btn.getBoundingClientRect();
		const wouldOverflow = r.right + SUBMENU_GAP + SUBMENU_W > window.innerWidth;
		submenuLeft = wouldOverflow ? r.left - SUBMENU_GAP - SUBMENU_W : r.right + SUBMENU_GAP;
		submenuTop = r.top;
	}

	const filteredSections = $derived.by(() => {
		const q = search.trim().toLowerCase();
		if (!q) return sections;
		return sections
			.map((s) => ({
				...s,
				items: s.items.filter(
					(i) =>
						i.label.toLowerCase().includes(q) ||
						(i.subtitle ?? '').toLowerCase().includes(q)
				)
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
				<div class="head__text">
					<div class="head__title">{header}</div>
					<div class="head__sub">{tagline}</div>
				</div>
				<div class="head__cube" aria-hidden="true">
					<div class="head__cube-inner"></div>
				</div>
			</header>

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
					<div class="section section--{section.id}">
						<div class="section__label">{section.label}</div>
						{#each section.items as item (item.id)}
							<!-- svelte-ignore a11y_no_static_element_interactions -->
							<div
								class="item"
								class:item--has-sub={!!item.children}
								onmouseenter={(e) => {
									hoveredId = item.id;
									if (item.children) placeSubmenu(e.currentTarget);
								}}
								onmouseleave={() => {
									if (hoveredId === item.id) hoveredId = null;
								}}
							>
								<button
									type="button"
									class="item__main"
									role="menuitem"
									onclick={() => pick(item.id)}
									onfocus={(e) => {
										hoveredId = item.id;
										if (item.children) placeSubmenu(e.currentTarget);
									}}
								>
									<span class="item__icon" aria-hidden="true">{item.icon}</span>
									<span class="item__text">
										<span class="item__label">{item.label}</span>
										{#if item.subtitle}
											<span class="item__sub">{item.subtitle}</span>
										{/if}
									</span>
									{#if item.badge !== undefined && item.badge > 0}
										<span class="item__badge">{item.badge}</span>
									{/if}
									{#if item.children}
										<span class="item__chev" aria-hidden="true">›</span>
									{/if}
								</button>
								{#if item.children && hoveredId === item.id}
									<div
										class="submenu"
										role="menu"
										aria-label={`${item.label} submenu`}
										style="top: {submenuTop}px; left: {submenuLeft}px; width: {SUBMENU_W}px;"
									>
										{#each item.children as sub (sub.id)}
											{@const isViewAll = sub.id === item.id && sub.icon === '↗'}
											<button
												type="button"
												class="submenu__item"
												class:submenu__item--view-all={isViewAll}
												role="menuitem"
												onclick={() => pick(sub.id)}
											>
												<span class="submenu__icon" aria-hidden="true">{sub.icon}</span>
												<span class="submenu__text">
													<span class="submenu__label">{sub.label}</span>
													{#if sub.subtitle}
														<span class="submenu__sub">{sub.subtitle}</span>
													{/if}
												</span>
												{#if isViewAll}
													<span class="submenu__chev" aria-hidden="true">›</span>
												{/if}
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

			<div class="account" class:account--off={!connected}>
				<span class="dot" class:dot--ok={connected}></span>
				<span class="account__text">
					{connected ? 'ACCOUNT CONNECTED' : 'NOT SIGNED IN'}
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
		</div>
	{/if}
</div>

<style>
	.start-menu {
		position: relative;
		display: inline-block;
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
	}

	/* ── Trigger ──────────────────────────────────────────────────── */
	.trigger {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		/* Match the height of the wallet/account button on the right of
		   the topbar (~36 px) so the bar reads as one row, not two. */
		padding: 10px 18px;
		min-height: 36px;
		background: rgba(255, 255, 255, 0.18);
		border: 2px solid #000;
		color: #fff;
		font-weight: 700;
		font-size: 0.8125rem;
		letter-spacing: 0.02em;
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

	/* ── Panel ────────────────────────────────────────────────────── */
	.panel {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		width: 360px;
		/* No overflow on the panel itself — the inner ``.sections``
		   container scrolls. This lets the absolute-positioned submenu
		   render outside the panel without being clipped. */
		overflow: visible;
		background: #070a25;
		color: #e0e7ff;
		/* Lighter chrome than retro windows, so the menu reads as a
		   menu rather than a third window. */
		border: 1px solid #1e293b;
		box-shadow: 0 16px 36px rgba(0, 0, 0, 0.55), 0 2px 0 rgba(0, 0, 0, 0.4);
		z-index: 200;
		padding: 12px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	/* ── Header tile ──────────────────────────────────────────────── */
	.head {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 14px;
		align-items: center;
		padding: 12px 14px;
		background: linear-gradient(135deg, #0e1538 0%, #1e1b4b 100%);
		border: 1px solid #312e81;
	}
	.head__title {
		font-weight: 800;
		letter-spacing: 0.08em;
		color: #fff;
		font-size: 0.95rem;
	}
	.head__sub {
		font-size: 0.72rem;
		color: #c7d2fe;
		margin-top: 4px;
		line-height: 1.35;
	}
	.head__cube {
		width: 42px;
		height: 42px;
		display: grid;
		place-items: center;
		background: linear-gradient(135deg, #4338ca 0%, #6366f1 50%, #818cf8 100%);
		border: 2px solid #1e1b4b;
		box-shadow: inset -2px -2px 0 rgba(0, 0, 0, 0.35), inset 2px 2px 0 rgba(255, 255, 255, 0.15);
	}
	.head__cube-inner {
		width: 18px;
		height: 18px;
		background: #c7d2fe;
		border: 1.5px solid #1e1b4b;
		transform: rotate(45deg);
		box-shadow: inset 1px 1px 0 #fff, inset -1px -1px 0 #4338ca;
	}

	/* ── Search ───────────────────────────────────────────────────── */
	.search {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 10px;
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
		font-size: 0.85rem;
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
		padding: 2px 6px;
		border: 1px solid #334155;
	}

	/* ── Sections ─────────────────────────────────────────────────── */
	.sections {
		display: flex;
		flex-direction: column;
		gap: 4px;
		/* Scroll here, not on the panel — so the submenu (rendered
		   position: fixed) can escape the panel's viewport. */
		max-height: clamp(220px, 60vh, 520px);
		overflow-y: auto;
		overflow-x: hidden;
		/* Subtle scrollbar to match the dark panel. */
		scrollbar-width: thin;
		scrollbar-color: #1e293b transparent;
	}
	.section {
		display: flex;
		flex-direction: column;
		padding-top: 6px;
	}
	.section + .section {
		margin-top: 6px;
		border-top: 1px solid #1e293b;
	}
	.section__label {
		font-size: 0.625rem;
		font-weight: 700;
		letter-spacing: 0.14em;
		color: #60a5fa;
		padding: 6px 10px 4px;
	}
	/* Per-section accents (mock: CORE in green, the rest in blue). */
	.section--core .section__label {
		color: #4ade80;
	}
	.section--ecosystem .section__label {
		color: #60a5fa;
	}
	.section--learn .section__label {
		color: #93c5fd;
	}
	.section--system .section__label {
		color: #93c5fd;
	}

	/* ── Items ────────────────────────────────────────────────────── */
	.item {
		position: relative;
	}
	.item__main {
		all: unset;
		width: 100%;
		display: grid;
		grid-template-columns: 24px 1fr auto auto;
		gap: 12px;
		align-items: center;
		padding: 8px 10px;
		font-size: 0.85rem;
		color: #e0e7ff;
		border-left: 3px solid transparent;
		cursor: pointer;
		transition: background 0.1s ease, border-color 0.1s ease;
	}
	.item__main:hover,
	.item__main:focus-visible {
		background: #1e1b4b;
		border-left-color: #6366f1;
		outline: none;
	}
	.item__icon {
		width: 24px;
		text-align: center;
		font-size: 1rem;
	}
	.item__text {
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 1px;
	}
	.item__label {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.item__sub {
		font-size: 0.65rem;
		color: #94a3b8;
		line-height: 1.3;
	}
	.item__badge {
		display: inline-grid;
		place-items: center;
		min-width: 22px;
		height: 22px;
		padding: 0 7px;
		font-size: 0.7rem;
		font-weight: 700;
		color: #052e16;
		background: #22c55e;
		border-radius: 999px;
	}
	.item__chev {
		color: #93c5fd;
		font-size: 1.1rem;
		line-height: 1;
	}

	/* ── Submenu ──────────────────────────────────────────────────── */
	.submenu {
		/* Anchored to the viewport via JS-computed top/left so the
		   panel's scrolling/clipping never affects it. */
		position: fixed;
		background: #070a25;
		color: #e0e7ff;
		border: 1px solid #1e293b;
		box-shadow: 0 16px 36px rgba(0, 0, 0, 0.55);
		padding: 6px;
		display: flex;
		flex-direction: column;
		gap: 2px;
		z-index: 250;
	}
	.submenu__item {
		all: unset;
		display: grid;
		grid-template-columns: 26px 1fr auto;
		gap: 12px;
		align-items: center;
		padding: 8px 10px;
		font-size: 0.85rem;
		color: #e0e7ff;
		cursor: pointer;
	}
	.submenu__item:hover,
	.submenu__item:focus-visible {
		background: #1e1b4b;
		outline: none;
	}
	.submenu__icon {
		width: 26px;
		text-align: center;
		font-size: 1.05rem;
	}
	.submenu__text {
		min-width: 0;
		display: flex;
		flex-direction: column;
		gap: 1px;
	}
	.submenu__label {
		font-weight: 600;
	}
	.submenu__sub {
		font-size: 0.65rem;
		color: #94a3b8;
		line-height: 1.3;
	}
	.submenu__chev {
		color: #93c5fd;
		font-size: 1.1rem;
		line-height: 1;
	}
	.submenu__item--view-all {
		border-top: 1px solid #1e293b;
		margin-top: 4px;
		padding-top: 10px;
		color: #c7d2fe;
		font-weight: 600;
	}
	.submenu__item--view-all .submenu__icon {
		color: #93c5fd;
	}

	/* ── Account row (pinned at bottom of the panel) ─────────────── */
	.account {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 10px 12px;
		background: #050a25;
		border: 1px solid #1e293b;
		font-size: 0.7rem;
		letter-spacing: 0.08em;
		color: #94a3b8;
		margin-top: 2px;
	}
	.dot {
		width: 9px;
		height: 9px;
		border-radius: 50%;
		background: #64748b;
		flex: 0 0 auto;
		box-shadow: 0 0 6px rgba(100, 116, 139, 0.5);
	}
	.dot--ok {
		background: #22c55e;
		box-shadow: 0 0 8px rgba(34, 197, 94, 0.7);
	}
	.account__text {
		font-weight: 700;
		color: #e0e7ff;
	}
	.account__id {
		margin-left: auto;
		font-family: inherit;
		font-size: 0.7rem;
		letter-spacing: normal;
		color: #c7d2fe;
		background: #1e1b4b;
		padding: 2px 7px;
		border: 1px solid #312e81;
		max-width: 11em;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.account__copy {
		font-family: inherit;
		background: transparent;
		border: 1px solid #312e81;
		color: #c7d2fe;
		padding: 2px 6px;
		cursor: pointer;
	}
	.account__copy:hover {
		background: #1e1b4b;
		color: #fff;
	}

	.empty {
		font-size: 0.78rem;
		color: #94a3b8;
		font-style: italic;
		padding: 12px 10px;
		margin: 0;
	}

	@media (max-width: 480px) {
		.panel {
			width: min(92vw, 320px);
		}
		.submenu {
			width: min(82vw, 260px);
		}
	}
</style>
