<script lang="ts">
	import { Modal, PixelButton, PixelInput, PixelTabs } from '@cyberdynecorp/svelte-ui-core';

	type Tab = 'account' | 'wallet';

	let {
		open = $bindable(false),
		loading = false,
		error = null,
		onGoogle,
		onEmailLogin,
		onWalletConnect,
		onClose
	}: {
		open?: boolean;
		loading?: boolean;
		error?: string | null;
		onGoogle: () => void | Promise<void>;
		onEmailLogin: (email: string, password: string) => void | Promise<void>;
		onWalletConnect: () => void | Promise<void>;
		onClose: () => void;
	} = $props();

	let activeTab = $state<Tab>('account');
	let email = $state('');
	let password = $state('');
	let formError = $state<string | null>(null);

	const tabs = [
		{ id: 'account', label: '👤 Account' },
		{ id: 'wallet', label: '🔐 Wallet' }
	];

	function handleSubmit(event: Event) {
		event.preventDefault();
		formError = null;
		if (!email.trim() || !password) {
			formError = 'Email and password are required.';
			return;
		}
		void onEmailLogin(email.trim(), password);
	}

	function close() {
		formError = null;
		onClose();
	}
</script>

<Modal {open} title="🖥️  CONNECT" size="md">
	<div class="connect">
		<PixelTabs
			items={tabs}
			value={activeTab}
			onChange={(id) => (activeTab = id as Tab)}
			ariaLabel="Sign-in method"
		/>

		{#if error || formError}
			<div class="alert" role="alert">{formError ?? error}</div>
		{/if}

		{#if activeTab === 'account'}
			<div class="pane">
				<button
					type="button"
					class="google-btn"
					onclick={() => void onGoogle()}
					disabled={loading}
				>
					<span class="google-btn__g" aria-hidden="true">G</span>
					<span class="google-btn__label">Continue with Google</span>
				</button>

				<div class="divider">
					<span class="divider__line"></span>
					<span class="divider__label">or continue with email</span>
					<span class="divider__line"></span>
				</div>

				<form class="form" onsubmit={handleSubmit}>
					<PixelInput
						type="email"
						label="EMAIL"
						placeholder="you@example.com"
						bind:value={email}
						disabled={loading}
						required
						ariaLabel="Email"
					/>
					<PixelInput
						type="password"
						label="PASSWORD"
						placeholder="••••••••"
						bind:value={password}
						disabled={loading}
						required
						ariaLabel="Password"
					/>
					<PixelButton type="submit" variant="solid" size="md" fullWidth disabled={loading}>
						{loading ? '> SIGNING IN…' : 'Access Platform →'}
					</PixelButton>
				</form>

				<p class="footer-note">
					<span class="footer-note__shield" aria-hidden="true">🛡</span>
					Authentication secured by CyberdyneAuth
				</p>
			</div>
		{:else}
			<div class="pane">
				<button
					type="button"
					class="wallet-btn"
					onclick={() => void onWalletConnect()}
					disabled={loading}
				>
					<span class="wallet-btn__icon" aria-hidden="true">📱</span>
					<span class="wallet-btn__body">
						<span class="wallet-btn__title">WalletConnect</span>
						<span class="wallet-btn__sub">
							MetaMask, Trust Wallet, Coinbase &amp; 50+ wallets
						</span>
					</span>
				</button>

				<p class="wallet-note">
					Your wallet signs a one-time challenge — the signature proves you control the address, then CyberdyneAuth issues a session token.
				</p>

				<p class="footer-note">
					<span class="footer-note__shield" aria-hidden="true">🛡</span>
					SIWE handshake secured by CyberdyneAuth
				</p>
			</div>
		{/if}

		<div class="close-row">
			<PixelButton variant="ghost" size="sm" onclick={close} disabled={loading}>
				Cancel
			</PixelButton>
		</div>
	</div>
</Modal>

<style>
	.connect {
		display: flex;
		flex-direction: column;
		gap: 14px;
		font-family: var(--font-mono, 'JetBrains Mono', monospace);
		min-width: 0;
	}
	.pane {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.alert {
		font-size: 0.8125rem;
		color: #b91c1c;
		background: #fef2f2;
		border: 2px solid #b91c1c;
		box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
		padding: 8px 10px;
	}

	/* ---------- Google ---------- */
	.google-btn {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 10px 14px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45);
		font-family: inherit;
		font-size: 0.875rem;
		font-weight: 700;
		color: #111827;
		cursor: pointer;
		transition: transform 0.12s ease, box-shadow 0.12s ease;
	}
	.google-btn:hover:not(:disabled) {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.5);
	}
	.google-btn:disabled { opacity: 0.6; cursor: not-allowed; }
	.google-btn__g {
		flex: 0 0 auto;
		width: 28px;
		height: 28px;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-weight: 800;
		font-size: 0.95rem;
		background: linear-gradient(135deg, #ea4335, #fbbc05 50%, #34a853);
		color: #ffffff;
		border: 2px solid #000;
	}
	.google-btn__label { flex: 1 1 auto; text-align: left; }

	/* ---------- Divider ---------- */
	.divider {
		display: flex;
		align-items: center;
		gap: 10px;
		margin: 2px 0;
	}
	.divider__line {
		flex: 1 1 auto;
		height: 2px;
		background: #d1d5db;
	}
	.divider__label {
		font-size: 0.7rem;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: #6b7280;
	}

	/* ---------- Form ---------- */
	.form {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	/* ---------- Wallet ---------- */
	.wallet-btn {
		position: relative;
		display: flex;
		align-items: center;
		gap: 14px;
		padding: 14px 16px;
		background: #ffffff;
		border: 2px solid #000;
		box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45);
		font-family: inherit;
		color: #111827;
		cursor: pointer;
		text-align: left;
		transition: transform 0.12s ease, box-shadow 0.12s ease;
	}
	.wallet-btn::before {
		content: '';
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		width: 6px;
		background: #22c55e;
		border-right: 2px solid #000;
	}
	.wallet-btn:hover:not(:disabled) {
		transform: translate(-1px, -1px);
		box-shadow: 4px 4px 0 rgba(0, 0, 0, 0.55);
	}
	.wallet-btn:disabled { opacity: 0.6; cursor: not-allowed; }
	.wallet-btn__icon {
		flex: 0 0 auto;
		width: 36px;
		height: 36px;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-size: 1.2rem;
		background: #22c55e;
		color: #ffffff;
		border: 2px solid #000;
	}
	.wallet-btn__body { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
	.wallet-btn__title { font-size: 0.95rem; font-weight: 700; }
	.wallet-btn__sub { font-size: 0.75rem; color: #4b5563; }
	.wallet-note {
		font-size: 0.75rem;
		line-height: 1.55;
		color: #374151;
		margin: 0;
	}

	/* ---------- Footer ---------- */
	.footer-note {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 0.7rem;
		color: #6b7280;
		margin: 4px 0 0;
	}
	.footer-note__shield { line-height: 1; }

	.close-row {
		display: flex;
		justify-content: flex-end;
		padding-top: 6px;
		border-top: 1px solid #e5e7eb;
	}
</style>
