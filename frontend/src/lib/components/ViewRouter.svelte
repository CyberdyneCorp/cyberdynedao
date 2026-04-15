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
	import type { MarketplaceItem } from '$lib/types/components';

	export let content: string;
	export let onAddToCart: ((item: MarketplaceItem) => void) | undefined = undefined;
	export let isMobile = false;
</script>

{#if content === 'cart'}
	<CartView />
{:else if content === 'terminal'}
	<Terminal />
{:else if content === 'investments'}
	<InvestmentsView />
{:else if content === 'shop'}
	<ShopView {onAddToCart} />
{:else if content === 'products'}
	<ProductsView />
{:else if content === 'team'}
	<TeamView />
{:else if content === 'dao'}
	<DaoView />
{:else if content === 'services'}
	<ServicesView />
{:else if content === 'cyberdyne'}
	<CyberddyneView />
{:else if content === 'listen'}
	<LearnView />
{:else if content === 'contact'}
	<ContactView />
{:else}
	<NewsView {isMobile} />
{/if}
