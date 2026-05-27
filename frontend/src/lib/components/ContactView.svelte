<script lang="ts">
	import { onMount } from 'svelte';
	import { createContactViewModel } from '$lib/viewmodels/contactViewModel';
	import {
		contactIntro as staticContactIntro,
		contactMethods as staticContactMethods,
		type ContactMethod
	} from '$lib/data/contact';
	import { PixelButton } from '@cyberdynecorp/svelte-ui-core';
	import { fetchContactPage, postAsk } from '$lib/api/contentApi';

	const vm = createContactViewModel();

	// Stale-while-revalidate for methods + intro. The viewmodel still
	// owns the click handler so the ContactMethod-related behaviour
	// (opening the link in a new tab, instrumentation) stays in one
	// place — we just refresh the underlying list.
	let contactMethods = $state<ContactMethod[]>(staticContactMethods);
	let contactIntro = $state(staticContactIntro);

	onMount(async () => {
		const page = await fetchContactPage();
		contactMethods = page.methods;
		contactIntro = page.intro;
	});

	// ── Message form → POST /api/v1/asks ──────────────────────────────
	let formName = $state('');
	let formEmail = $state('');
	let formBody = $state('');
	let sending = $state(false);
	let sent = $state(false);
	let formError = $state<string | null>(null);

	const emailValid = $derived(/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(formEmail.trim()));
	const canSend = $derived(
		!sending && formName.trim().length > 0 && emailValid && formBody.trim().length > 0
	);

	async function submitMessage(e: SubmitEvent) {
		e.preventDefault();
		if (!canSend) return;
		sending = true;
		formError = null;
		const res = await postAsk({
			name: formName.trim(),
			email: formEmail.trim(),
			body: formBody.trim(),
			channel: 'contact_form',
			// The backend requires a non-empty captcha token; this deployment
			// runs CyberdyneAuth's mock (always-pass) provider. If Turnstile is
			// enabled later, swap this for a real widget token.
			captchaToken: 'contact-form'
		});
		sending = false;
		if (res.ok) {
			sent = true;
			formName = '';
			formEmail = '';
			formBody = '';
		} else {
			formError = res.error ?? 'Something went wrong. Try a channel above.';
		}
	}
</script>

<div class="contact-view">
	<!-- Hero -->
	<header class="hero">
		<div class="hero__brand">
			<span class="hero__mark" aria-hidden="true">📡</span>
			<h1 class="hero__title">CONTACT CYBERDYNE</h1>
		</div>
		<p class="hero__tagline">Pick a channel. We read everything that lands.</p>
	</header>

	<div class="content">
		<!-- Intro card -->
		<section class="intro">
			<h2 class="intro__headline">{contactIntro.headline}</h2>
			<p class="intro__body">{contactIntro.body}</p>
			<div class="intro__divider" aria-hidden="true"></div>
		</section>

		<!-- Channels grid -->
		<div class="channels">
			{#each contactMethods as method}
				<article
					class="channel"
					style="--brand: {method.colorPalette.solid}; --brand-hover: {method.colorPalette.hover}; --brand-rgb: {method.colorPalette.rgb};"
				>
					<header class="channel__head">
						<div class="channel__avatar">
							<span aria-hidden="true">{method.icon}</span>
						</div>
						<div class="channel__head-text">
							<h3 class="channel__name">{method.name}</h3>
							<div class="channel__id">ID: {method.id.toUpperCase()}</div>
						</div>
						<div class="channel__status">
							<span class="channel__dot" aria-hidden="true"></span>
							ONLINE
						</div>
					</header>

					<p class="channel__desc">{method.description}</p>

					<div class="channel__tagline">{method.tagline}</div>

					<button
						type="button"
						class="channel__cta"
						onclick={() => vm.openContact(method)}
					>
						<span class="channel__cta-bracket">[</span>
						<span>{method.action}</span>
						<span class="channel__cta-bracket">]</span>
					</button>
				</article>
			{/each}
		</div>

		<!-- Direct message form -->
		<section class="msg">
			<div class="msg__head">
				<span class="msg__icon" aria-hidden="true">✉</span>
				<h2 class="msg__title">SEND A DIRECT MESSAGE</h2>
			</div>
			{#if sent}
				<div class="msg__sent" role="status">
					<span class="msg__sent-icon" aria-hidden="true">✓</span>
					<div>
						<p class="msg__sent-title">Message received.</p>
						<p class="msg__sent-body">We read everything that lands — expect a reply by email.</p>
					</div>
					<button type="button" class="msg__again" onclick={() => (sent = false)}>
						Send another
					</button>
				</div>
			{:else}
				<form class="msg__form" onsubmit={submitMessage}>
					<div class="msg__row">
						<label class="msg__field">
							<span class="msg__label">Name</span>
							<input
								class="msg__input"
								type="text"
								bind:value={formName}
								maxlength="128"
								autocomplete="name"
								placeholder="Sarah Connor"
							/>
						</label>
						<label class="msg__field">
							<span class="msg__label">Email</span>
							<input
								class="msg__input"
								class:msg__input--bad={formEmail.length > 0 && !emailValid}
								type="email"
								bind:value={formEmail}
								maxlength="256"
								autocomplete="email"
								placeholder="you@domain.com"
							/>
						</label>
					</div>
					<label class="msg__field">
						<span class="msg__label">Message</span>
						<textarea
							class="msg__input msg__textarea"
							bind:value={formBody}
							maxlength="4000"
							rows="5"
							placeholder="Tell us what you're building or what you need."
						></textarea>
					</label>
					{#if formError}
						<p class="msg__error">{formError}</p>
					{/if}
					<div class="msg__actions">
						<PixelButton variant="solid" size="md" type="submit" disabled={!canSend}>
							{sending ? 'Sending…' : 'Transmit message'}
						</PixelButton>
					</div>
				</form>
			{/if}
		</section>

		<!-- Trust footer -->
		<section class="trust">
			<div class="trust__pixel-stripe" aria-hidden="true"></div>
			<div class="trust__grid">
				<div class="trust__item">
					<div class="trust__icon" aria-hidden="true">◆</div>
					<div class="trust__label">Web3-native team</div>
					<div class="trust__sub">Production experience across the stack</div>
				</div>
				<div class="trust__item">
					<div class="trust__icon" aria-hidden="true">◆</div>
					<div class="trust__label">Open by default</div>
					<div class="trust__sub">Source for everything we ship is public</div>
				</div>
				<div class="trust__item">
					<div class="trust__icon" aria-hidden="true">◆</div>
					<div class="trust__label">Pragmatic responses</div>
					<div class="trust__sub">No sales theatre — engineers answer engineers</div>
				</div>
			</div>
		</section>
	</div>
</div>

<style>
	.contact-view {
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		background: #0b1120;
		color: #e5e7eb;
		height: 100%;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
	}

	/* ---------- Hero ---------- */
	.hero {
		padding: 18px 24px;
		background: linear-gradient(135deg, #064e3b 0%, #22c55e 100%);
		border-bottom: 2px solid #000;
		color: #ffffff;
		flex: 0 0 auto;
		position: relative;
	}
	.hero::after {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		bottom: -2px;
		height: 4px;
		background: linear-gradient(
			to right,
			#22c55e 0%, #22c55e 25%,
			#3b82f6 25%, #3b82f6 50%,
			#a855f7 50%, #a855f7 75%,
			#f97316 75%, #f97316 100%
		);
		border-top: 2px solid #000;
	}
	.hero__brand { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
	.hero__mark { font-size: 1.5rem; }
	.hero__title { font-size: 1.5rem; font-weight: 800; letter-spacing: 0.1em; margin: 0; color: #fff; }
	.hero__tagline { margin: 0; font-size: 0.875rem; line-height: 1.5; color: #d1fae5; }

	.content {
		max-width: 1100px;
		margin: 0 auto;
		padding: 26px 20px 32px;
		display: flex;
		flex-direction: column;
		gap: 20px;
		width: 100%;
	}

	/* ---------- Intro ---------- */
	.intro {
		position: relative;
		background: #ffffff;
		color: #111827;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.6);
		padding: 22px 22px 18px 30px;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 10px;
		text-align: center;
	}
	.intro::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: #22c55e;
		border-right: 2px solid #000;
	}
	.intro__headline {
		font-size: 1.5rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #15803d;
		margin: 0;
	}
	.intro__body {
		font-size: 0.9375rem;
		line-height: 1.55;
		color: #1f2937;
		margin: 0;
		max-width: 640px;
	}
	.intro__divider {
		width: 100%;
		max-width: 240px;
		height: 2px;
		background: linear-gradient(
			to right,
			#22c55e 0%, #22c55e 33%,
			#3b82f6 33%, #3b82f6 66%,
			#a855f7 66%, #a855f7 100%
		);
		margin-top: 4px;
	}

	/* ---------- Channels ---------- */
	.channels {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 16px;
	}
	@media (max-width: 900px) {
		.channels { grid-template-columns: repeat(2, minmax(0, 1fr)); }
	}
	@media (max-width: 600px) {
		.channels { grid-template-columns: minmax(0, 1fr); }
	}

	.channel {
		position: relative;
		background: #ffffff;
		color: #111827;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.6);
		padding: 16px 16px 18px 22px;
		display: flex;
		flex-direction: column;
		gap: 12px;
		transition: transform 0.15s ease, box-shadow 0.15s ease;
	}
	.channel::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 8px;
		background: var(--brand);
		border-right: 2px solid #000;
	}
	.channel:hover {
		transform: translate(-2px, -2px);
		box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.7);
	}

	.channel__head {
		display: grid;
		grid-template-columns: 48px 1fr auto;
		gap: 12px;
		align-items: center;
	}
	.channel__avatar {
		width: 48px;
		height: 48px;
		border: 2px solid #000;
		background: var(--brand);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 22px;
		color: #ffffff;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
	}
	.channel__head-text { min-width: 0; }
	.channel__name {
		font-size: 1.0625rem;
		font-weight: 800;
		color: #000;
		margin: 0;
		line-height: 1.2;
	}
	.channel__id {
		font-size: 0.625rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #6b7280;
		margin-top: 2px;
	}
	.channel__status {
		font-size: 0.625rem;
		font-weight: 800;
		letter-spacing: 0.08em;
		color: #15803d;
		display: inline-flex;
		align-items: center;
		gap: 4px;
		flex: 0 0 auto;
	}
	.channel__dot {
		width: 8px;
		height: 8px;
		background: #22c55e;
		border: 1.5px solid #000;
		display: inline-block;
		animation: pulse 1.8s ease-in-out infinite;
	}
	@keyframes pulse {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.4; }
	}

	.channel__desc {
		font-size: 0.8125rem;
		line-height: 1.5;
		color: #374151;
		margin: 0;
		flex: 1 1 auto;
	}

	.channel__tagline {
		font-size: 0.6875rem;
		font-weight: 700;
		color: var(--brand);
		text-transform: uppercase;
		letter-spacing: 0.06em;
		padding: 6px 10px;
		background: #f9fafb;
		border: 1.5px solid #000;
		align-self: flex-start;
	}

	.channel__cta {
		font-family: inherit;
		font-size: 0.875rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		padding: 10px 14px;
		background: var(--brand);
		color: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
		cursor: pointer;
		display: inline-flex;
		justify-content: center;
		align-items: center;
		gap: 6px;
		transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.1s ease;
	}
	.channel__cta:hover {
		background: var(--brand-hover);
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.6);
	}
	.channel__cta-bracket { opacity: 0.7; font-weight: 700; }

	/* ---------- Trust footer ---------- */
	.trust {
		position: relative;
		background: #0f172a;
		color: #ffffff;
		border: 2px solid #000;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.6);
		padding: 22px 18px 18px;
	}
	.trust__pixel-stripe {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(
			to right,
			#22c55e 0%, #22c55e 25%,
			#3b82f6 25%, #3b82f6 50%,
			#a855f7 50%, #a855f7 75%,
			#f97316 75%, #f97316 100%
		);
		border-bottom: 2px solid #000;
	}
	.trust__grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 16px;
	}
	@media (max-width: 720px) {
		.trust__grid { grid-template-columns: minmax(0, 1fr); }
	}
	.trust__item {
		display: flex;
		flex-direction: column;
		gap: 2px;
		text-align: center;
	}
	.trust__icon {
		font-size: 1rem;
		color: #67e8f9;
	}
	.trust__label {
		font-size: 0.8125rem;
		font-weight: 800;
		text-transform: uppercase;
		letter-spacing: 0.06em;
		color: #ffffff;
	}
	.trust__sub {
		font-size: 0.75rem;
		color: #94a3b8;
		line-height: 1.45;
	}

	/* ---------- Message form ---------- */
	.msg {
		border: 2px solid #000;
		background: #111827;
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.6);
		padding: 16px 18px;
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.msg__head {
		display: flex;
		align-items: center;
		gap: 10px;
	}
	.msg__icon {
		font-size: 1.1rem;
		color: #22c55e;
	}
	.msg__title {
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0.1em;
		margin: 0;
		color: #e5e7eb;
	}
	.msg__form {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.msg__row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
	}
	@media (max-width: 560px) {
		.msg__row { grid-template-columns: 1fr; }
	}
	.msg__field {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.msg__label {
		font-size: 0.6875rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #94a3b8;
	}
	.msg__input {
		font-family: inherit;
		font-size: 0.875rem;
		color: #e5e7eb;
		background: #0b1120;
		border: 2px solid #334155;
		padding: 8px 10px;
		outline: none;
		transition: border-color 0.12s ease;
	}
	.msg__input:focus {
		border-color: #22c55e;
	}
	.msg__input::placeholder {
		color: #475569;
	}
	.msg__input--bad {
		border-color: #ef4444;
	}
	.msg__textarea {
		resize: vertical;
		min-height: 96px;
		line-height: 1.5;
	}
	.msg__error {
		margin: 0;
		font-size: 0.8125rem;
		color: #fca5a5;
		font-weight: 600;
	}
	.msg__actions {
		display: flex;
		justify-content: flex-end;
	}
	.msg__sent {
		display: flex;
		align-items: center;
		gap: 12px;
		background: #052e16;
		border: 2px solid #15803d;
		padding: 12px 14px;
	}
	.msg__sent-icon {
		flex: 0 0 auto;
		width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: 800;
		color: #052e16;
		background: #22c55e;
		border: 2px solid #000;
	}
	.msg__sent-title {
		margin: 0;
		font-weight: 700;
		color: #bbf7d0;
	}
	.msg__sent-body {
		margin: 2px 0 0;
		font-size: 0.8125rem;
		color: #86efac;
	}
	.msg__again {
		margin-left: auto;
		font-family: inherit;
		font-size: 0.75rem;
		font-weight: 700;
		color: #bbf7d0;
		background: transparent;
		border: 1.5px solid #15803d;
		padding: 6px 10px;
		cursor: pointer;
	}
	.msg__again:hover {
		background: #064e3b;
	}
</style>
