<script lang="ts">
	interface NavItem {
		name: string;
		icon: string;
		href?: string;
		action?: () => void;
	}

	export let currentView: string = 'read';
	export let onViewChange: (view: string) => void;
	export let cartCount: number = 0;

	const navItems: NavItem[] = [
		{ name: 'Substack', icon: '/assets/substack.svg' },
		{ name: 'Read', icon: '/assets/read.svg' },
		{ name: 'Investments', icon: '/assets/investments.svg' },
		{ name: 'Watch', icon: '/assets/watch.svg' },
		{ name: 'Contact Me', icon: '/assets/contact.svg' },
		{ name: 'Listen', icon: '/assets/listen.svg' },
		{ name: 'enigma', icon: '/assets/enigma.svg' },
		{ name: 'Shop', icon: '/assets/shop.svg' }
	];

	import { createWindow } from '$lib/stores/windowStore';

	function handleItemClick(item: NavItem) {
		const viewMap: { [key: string]: any } = {
			'Shop': 'shop',
			'Read': 'read',
			'Investments': 'investments',
			'Watch': 'watch',
			'Listen': 'listen',
			'Substack': 'substack',
			'Contact Me': 'contact',
			'enigma': 'enigma'
		};
		
		const view = viewMap[item.name] || item.name.toLowerCase();
		createWindow(view, item.name);
	}
</script>

<!-- 4x2 Grid Layout like original -->
<div class="grid grid-cols-2 gap-4 p-4">
	{#each navItems as item, index}
		<div class="flex flex-col items-center gap-1">
			<button
				class="sidebar-icon flex items-center justify-center p-2 cursor-pointer"
				on:click={() => handleItemClick(item)}
				title={item.name}
			>
				<img src={item.icon} alt={item.name} class="w-8 h-8" />
			</button>
			<span class="nav-label text-white text-xs font-mono text-center px-2 py-0.5 rounded">
				{item.name}
			</span>
		</div>
	{/each}
</div>

