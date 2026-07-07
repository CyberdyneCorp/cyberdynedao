<script lang="ts">
	import { SUPPORT_EMAIL, SUPPORT_RESPONSE_TIME, SUPPORT_HOURS } from '$lib/constants/company';
</script>

<svelte:head>
	<title>Support · Cyberdyne</title>
	<meta
		name="description"
		content="Get help with your Cyberdyne account, sign-in and MFA, managed wallet, purchases and subscriptions, and privacy requests."
	/>
</svelte:head>

<article class="prose">
	<h1>Support</h1>
	<p class="lead">Need help with your Cyberdyne account or a purchase? We're here to help.</p>

	<div class="contact-card">
		<p><strong>Email:</strong> <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
		<p><strong>Response time:</strong> {SUPPORT_RESPONSE_TIME}</p>
		<p><strong>Hours:</strong> {SUPPORT_HOURS}</p>
	</div>

	<h2>Common topics</h2>
	<ul>
		<li>
			<strong>Signing in</strong> — password reset, multi-factor authentication (MFA), and
			recovery codes.
		</li>
		<li><strong>Your managed wallet</strong> — accessing your wallet address and public key.</li>
		<li>
			<strong>Purchases and subscriptions</strong> — access not appearing after an App Store
			or web purchase, renewals, and refunds.
		</li>
		<li>
			<strong>Your data and privacy</strong> — access, correction, export, or deletion
			requests (see our <a href="/privacy">Privacy Policy</a>).
		</li>
	</ul>

	<h2>Account deletion</h2>
	<p>
		To delete your account and associated personal data, email
		<a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a> from the address on your account and
		ask us to delete it. See the <a href="/privacy">Privacy Policy</a> for what is erased and
		what we are legally required to retain.
	</p>

	<h2>Purchases &amp; refunds</h2>
	<p>
		Purchases and subscriptions made through the Apple App Store are billed and refunded by
		Apple. To request a refund for an App Store purchase, use
		<a href="https://reportaproblem.apple.com" rel="noopener noreferrer" target="_blank"
			>reportaproblem.apple.com</a
		>. For anything else — including access that hasn't appeared after a purchase — email us
		and we'll sort it out.
	</p>
</article>
