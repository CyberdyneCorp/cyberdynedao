<script lang="ts">
	import { PixelScrollArea } from '@cyberdynecorp/svelte-ui-core';
	import { t, locale, setLocale, SUPPORTED_LOCALES } from '$lib/i18n';
	import { reduceMotion } from '$lib/stores/settingsStore';
</script>

<PixelScrollArea maxHeight="100%" ariaLabel={$t('settings.title')}>
	<div class="settings">
		<header class="hero">
			<span class="hero__mark" aria-hidden="true">⚙️</span>
			<h1>{$t('settings.title')}</h1>
		</header>

		<!-- Language -->
		<section class="card">
			<h2 class="card__title">{$t('settings.language.title')}</h2>
			<p class="card__desc">{$t('settings.language.desc')}</p>
			<div class="langs" role="radiogroup" aria-label={$t('settings.language.title')}>
				{#each SUPPORTED_LOCALES as loc (loc.code)}
					<button
						type="button"
						role="radio"
						aria-checked={$locale === loc.code}
						class="lang"
						class:lang--active={$locale === loc.code}
						onclick={() => setLocale(loc.code)}
					>
						<span class="lang__flag" aria-hidden="true">{loc.flag}</span>
						<span class="lang__name">{loc.nativeLabel}</span>
						{#if $locale === loc.code}<span class="lang__check" aria-hidden="true">✓</span>{/if}
					</button>
				{/each}
			</div>
		</section>

		<!-- Appearance -->
		<section class="card">
			<h2 class="card__title">{$t('settings.appearance.title')}</h2>
			<label class="toggle">
				<input type="checkbox" bind:checked={$reduceMotion} />
				<span class="toggle__body">
					<span class="toggle__label">{$t('settings.reduceMotion.label')}</span>
					<span class="toggle__desc">{$t('settings.reduceMotion.desc')}</span>
				</span>
			</label>
		</section>
	</div>
</PixelScrollArea>

<style>
	.settings {
		padding: 1.25rem;
		color: #000000;
		font-family: system-ui, sans-serif;
	}
	.hero {
		display: flex;
		gap: 0.6rem;
		align-items: center;
		margin-bottom: 1rem;
	}
	.hero__mark {
		font-size: 1.75rem;
	}
	.hero h1 {
		margin: 0;
		font-size: 1.25rem;
	}
	.card {
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 0.85rem 1rem;
		margin-bottom: 0.85rem;
	}
	.card__title {
		margin: 0 0 0.25rem;
		font-size: 1rem;
	}
	.card__desc {
		margin: 0 0 0.7rem;
		font-size: 0.85rem;
		color: #374151;
	}
	.langs {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
		gap: 0.5rem;
	}
	.lang {
		display: flex;
		align-items: center;
		gap: 0.55rem;
		padding: 0.55rem 0.7rem;
		background: #f3f4f6;
		border: 2px solid #000000;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.9rem;
		text-align: left;
		transition: background 0.15s ease;
	}
	.lang:hover {
		background: #e5e7eb;
	}
	.lang--active {
		background: #dbeafe;
		box-shadow: inset 0 0 0 2px #1d4ed8;
	}
	.lang__flag {
		font-size: 1.2rem;
	}
	.lang__name {
		flex: 1;
	}
	.lang__check {
		color: #1d4ed8;
		font-weight: 700;
	}
	.toggle {
		display: flex;
		align-items: flex-start;
		gap: 0.6rem;
		cursor: pointer;
	}
	.toggle input {
		margin-top: 0.2rem;
		width: 1.1rem;
		height: 1.1rem;
		flex: 0 0 auto;
	}
	.toggle__body {
		display: flex;
		flex-direction: column;
	}
	.toggle__label {
		font-size: 0.9rem;
		font-weight: 600;
	}
	.toggle__desc {
		font-size: 0.8rem;
		color: #374151;
	}
</style>
