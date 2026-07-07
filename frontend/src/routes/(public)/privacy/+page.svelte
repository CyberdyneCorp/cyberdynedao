<script lang="ts">
	import {
		LEGAL_ENTITY,
		CNPJ,
		REGISTERED_ADDRESS,
		PRIVACY_EMAIL,
		MINIMUM_AGE,
		POLICY_LAST_UPDATED
	} from '$lib/constants/company';

	const sections = [
		{ id: 'data', label: '1. Data we process' },
		{ id: 'legal-bases', label: '2. Legal bases' },
		{ id: 'sharing', label: '3. Who we share with' },
		{ id: 'transfers', label: '4. Transfers' },
		{ id: 'retention', label: '5. Retention' },
		{ id: 'blockchain', label: '6. Blockchain' },
		{ id: 'rights', label: '7. Your rights' },
		{ id: 'security', label: '8. Security' },
		{ id: 'children', label: '9. Children' },
		{ id: 'changes', label: '10. Changes' },
		{ id: 'contact', label: '11. Contact' }
	];
</script>

<svelte:head>
	<title>Privacy Policy · Cyberdyne</title>
	<meta
		name="description"
		content="How Cyberdyne processes your personal data: what we collect, why, who we share it with, retention, and your rights."
	/>
</svelte:head>

<article class="prose">
	<h1>Privacy Policy</h1>
	<p class="updated">Last updated: {POLICY_LAST_UPDATED}</p>

	<p><strong>Controller:</strong> {LEGAL_ENTITY} ("Cyberdyne", "we", "us") — CNPJ {CNPJ}</p>
	<p><strong>Address:</strong> {REGISTERED_ADDRESS}</p>
	<p><strong>Contact / Data Protection:</strong> <a href="mailto:{PRIVACY_EMAIL}">{PRIVACY_EMAIL}</a></p>

	<p class="lead">
		Cyberdyne operates the CyberdyneAuth identity service, which provides account
		registration, sign-in, multi-factor authentication, a managed cryptocurrency
		wallet, and access to Cyberdyne products purchased through the web or the Apple
		App Store. This policy explains what personal data we process, why, on what legal
		basis, who we share it with, how long we keep it, and the rights you have.
	</p>

	<nav class="toc" aria-label="On this page">
		<span class="toc-title">On this page</span>
		<ul>
			{#each sections as s (s.id)}
				<li><a href="#{s.id}">{s.label}</a></li>
			{/each}
		</ul>
	</nav>

	<h2 id="data">1. Personal data we process</h2>
	<table>
		<thead>
			<tr><th>Category</th><th>Examples</th><th>Purpose</th></tr>
		</thead>
		<tbody>
			<tr>
				<td>Account identifiers</td>
				<td>Email address, phone number</td>
				<td>Create and secure your account; send verification and security messages</td>
			</tr>
			<tr>
				<td>Authentication secrets</td>
				<td>Password (stored hashed with Argon2id), TOTP secret and MFA recovery codes (encrypted / hashed)</td>
				<td>Authenticate you and protect the account</td>
			</tr>
			<tr>
				<td>Managed wallet</td>
				<td>Ethereum wallet address, public key, and a <strong>custodial private key</strong> (encrypted at rest)</td>
				<td>Provide the managed-wallet feature</td>
			</tr>
			<tr>
				<td>Profile (optional)</td>
				<td>Display name and avatar from Google / Microsoft sign-in</td>
				<td>Personalize your account when you use social sign-in</td>
			</tr>
			<tr>
				<td>Security / device metadata</td>
				<td>IP address, user-agent, session and token records</td>
				<td>Detect abuse, enforce rate limits, and let you review active sessions</td>
			</tr>
			<tr>
				<td>Billing references</td>
				<td>Stripe customer / subscription identifiers, Apple transaction identifiers, your entitlements</td>
				<td>Grant and maintain access to products you purchase</td>
			</tr>
			<tr>
				<td>Administrative audit records</td>
				<td>Actions taken on your account by administrators, with actor and timestamp</td>
				<td>Security, accountability, and incident investigation</td>
			</tr>
		</tbody>
	</table>
	<p>
		We do <strong>not</strong> collect or store payment-card numbers. Card and in-app
		purchase processing is handled entirely by Stripe and Apple.
	</p>

	<h2 id="legal-bases">2. Legal bases</h2>
	<p>
		We process personal data under the applicable data-protection law — Brazil's Lei
		Geral de Proteção de Dados (LGPD) and, where it applies to you, the EU/UK GDPR — on
		these bases:
	</p>
	<ul>
		<li>
			<strong>Performance of a contract</strong> — creating your account, authenticating
			you, providing the wallet, and delivering products you purchase.
		</li>
		<li>
			<strong>Legitimate interests</strong> — security, fraud and abuse prevention, and
			keeping auditable records of administrative actions.
		</li>
		<li>
			<strong>Legal obligation</strong> — retaining certain billing and audit records where
			law requires it.
		</li>
		<li>
			<strong>Consent</strong> — where you sign in with a third-party provider, or where you
			opt into optional features. You may withdraw consent at any time.
		</li>
	</ul>

	<h2 id="sharing">3. Who we share data with</h2>
	<p>We share personal data only with the processors and services needed to run the product:</p>
	<ul>
		<li>
			<strong>Email delivery</strong> — our transactional email provider (delivered over
			SMTP): your email address and the verification / reset links we send you.
		</li>
		<li><strong>Stripe</strong> — billing: your Stripe customer and subscription identifiers.</li>
		<li><strong>Apple</strong> — App Store purchases: your transaction identifiers.</li>
		<li>
			<strong>Google / Microsoft</strong> — only if you choose social sign-in: they are the
			source of your profile data, per their own privacy policies.
		</li>
		<li>
			<strong>Public blockchain</strong> — if you use the on-chain identity feature, your
			<strong>wallet address and public key</strong> are written to a public, immutable ledger
			(see Section 6). We do <strong>not</strong> write your email or other direct identifiers
			on-chain.
		</li>
		<li>
			<strong>Operator-authored automation ("hooks")</strong> — administrators may configure
			server-side automation that receives limited event data; it receives your email or
			wallet address only when explicitly enabled for that automation.
		</li>
	</ul>
	<p>
		We do <strong>not</strong> sell personal data. We do not currently transmit error or
		analytics data to third-party observability vendors.
	</p>

	<h2 id="transfers">4. International transfers</h2>
	<p>
		Some processors (Apple, Stripe, Google, Microsoft, and our email provider) process
		data outside Brazil, including in the United States. Where required, such transfers
		rely on appropriate safeguards, such as Standard Contractual Clauses.
	</p>

	<h2 id="retention">5. How long we keep it</h2>
	<p>We keep personal data only as long as needed for the purposes above, under a documented retention schedule:</p>
	<ul>
		<li>Short-lived authentication data (one-time codes, sign-in challenges, verification and reset tokens) is deleted within days of use or expiry.</li>
		<li>Session and device records are deleted within 30 days of expiry or revocation.</li>
		<li>Automation execution records are kept for up to 90 days.</li>
		<li>Billing and administrative audit records are kept for up to 12 months (or longer where law requires).</li>
	</ul>
	<p>
		When you delete your account, we erase your personal data — including your custodial
		private key, email, phone, and wallet identifiers held off-chain — except records we
		are legally required to retain. <strong>Data already written to a public blockchain
		cannot be deleted</strong> (Section 6).
	</p>

	<h2 id="blockchain">6. Blockchain and permanence</h2>
	<p>
		If you use the on-chain identity feature, your <strong>wallet address and public key
		are recorded on a public blockchain</strong>. By design, blockchain data is
		world-readable, permanent, and cannot be modified or deleted — including by us. We
		deliberately keep direct identifiers such as your <strong>email off-chain</strong> so
		they remain erasable. Consider this before enabling on-chain features.
	</p>

	<h2 id="rights">7. Your rights</h2>
	<p>
		Subject to applicable law, you may request to <strong>access</strong>,
		<strong>correct</strong>, <strong>export</strong>, or <strong>erase</strong> your
		personal data, <strong>object to</strong> or <strong>restrict</strong> certain
		processing, and <strong>withdraw consent</strong>. To exercise any right, contact
		<a href="mailto:{PRIVACY_EMAIL}">{PRIVACY_EMAIL}</a>. We will respond within the period
		required by law. You also have the right to complain to your local data-protection
		authority — in Brazil, the Autoridade Nacional de Proteção de Dados (ANPD).
	</p>

	<h2 id="security">8. Security</h2>
	<p>
		We protect your data with encryption in transit and at rest: custodial private keys
		and MFA secrets are encrypted with authenticated encryption under a key-derivation
		scheme, passwords are hashed with Argon2id, and other credentials are stored only as
		hashes. Access to administrative functions is restricted and audited.
	</p>

	<h2 id="children">9. Children</h2>
	<p>
		The service is not directed to children under {MINIMUM_AGE}, and we do not knowingly
		collect their data.
	</p>

	<h2 id="changes">10. Changes</h2>
	<p>
		We may update this policy; we will change the "Last updated" date and, for material
		changes, notify you through the service.
	</p>

	<h2 id="contact">11. Contact</h2>
	<p>
		{LEGAL_ENTITY} — CNPJ {CNPJ} — {REGISTERED_ADDRESS} —
		<a href="mailto:{PRIVACY_EMAIL}">{PRIVACY_EMAIL}</a>
	</p>
</article>

<style>
	.toc {
		border: 1px solid #17331a;
		border-radius: 12px;
		padding: 1rem 1.25rem 1.15rem;
		margin: 1.5rem 0 0.5rem;
		background: rgba(14, 26, 14, 0.5);
	}

	.toc-title {
		display: block;
		font-size: 0.72rem;
		letter-spacing: 0.2em;
		text-transform: uppercase;
		color: #7fae7f;
		margin-bottom: 0.6rem;
	}

	.toc ul {
		list-style: none;
		padding: 0;
		margin: 0;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
		gap: 0.35rem 1.1rem;
	}

	.toc li {
		margin: 0;
	}

	.toc a {
		color: #a7cba7;
		text-decoration: none;
		font-size: 0.86rem;
		border-bottom: 1px solid transparent;
	}

	.toc a:hover {
		color: #4ade80;
		border-bottom-color: #4ade80;
	}
</style>
