<script lang="ts">
	import Terminal from './Terminal.svelte';
	import NewsView from './NewsView.svelte';
	import ShopView from './ShopView.svelte';
	import CartView from './CartView.svelte';
	import InvestmentsView from './InvestmentsView.svelte';
	import ProductsView from './ProductsView.svelte';
	import TeamView from './TeamView.svelte';
	import DaoView from './DaoView.svelte';
	import ServicesView from './ServicesView.svelte';
	import CyberddyneView from './CyberddyneView.svelte';
	import LearnView from './LearnView.svelte';
	import ContactView from './ContactView.svelte';
	
	export const title: string = 'Terminal';
	export let showCart: boolean = false;
	export let cartItems: any[] = [];
	export let currentView: string = 'read';
	export let onAddToCart: ((item: any) => void) | undefined = undefined;
	export let embedded: boolean = false;
</script>

{#if embedded}
	<div class="window-content" class:terminal-content={currentView === 'terminal'}>
		{#if showCart}
			<CartView bind:cartItems />
		{:else if currentView === 'terminal'}
			<Terminal />
		{:else if currentView === 'investments'}
			<InvestmentsView />
		{:else if currentView === 'shop'}
			<ShopView {onAddToCart} />
		{:else if currentView === 'products'}
			<ProductsView />
		{:else if currentView === 'team'}
			<TeamView />
		{:else if currentView === 'dao'}
			<DaoView />
		{:else if currentView === 'services'}
			<ServicesView />
		{:else if currentView === 'cyberdyne'}
			<CyberddyneView />
		{:else if currentView === 'listen'}
			<LearnView />
		{:else if currentView === 'contact'}
			<ContactView />
		{:else}
			<NewsView />
		{/if}
	</div>
{:else}
	<div class="retro-window flex-1 mx-4 my-4 overflow-hidden">
		<div class="bg-white p-4 h-full overflow-y-auto">
			{#if showCart}
				<CartView bind:cartItems />
			{:else if currentView === 'terminal'}
				<Terminal />
			{:else if currentView === 'investments'}
				<InvestmentsView />
			{:else if currentView === 'shop'}
				<ShopView {onAddToCart} />
			{:else if currentView === 'products'}
				<ProductsView />
			{:else if currentView === 'team'}
				<TeamView />
			{:else if currentView === 'dao'}
				<DaoView />
			{:else if currentView === 'services'}
				<ServicesView />
			{:else if currentView === 'cyberdyne'}
				<CyberddyneView />
			{:else if currentView === 'listen'}
				<LearnView />
			{:else if currentView === 'contact'}
				<ContactView />
			{:else}
				<NewsView />
			{/if}
		</div>
	</div>
{/if}

<style>
	.window-content {
		padding: 16px;
		overflow-y: auto;
		flex: 1;
	}
	
	.window-content.terminal-content {
		padding: 0;
		height: 100%;
	}
</style>