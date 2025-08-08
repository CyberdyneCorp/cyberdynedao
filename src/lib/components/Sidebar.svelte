<script lang="ts">
	import { navItems, viewMap, type NavItem } from '$lib/constants/navigation';

	export let currentView: string = 'read';

	import { createWindow } from '$lib/stores/windowStore';

	function handleItemClick(item: NavItem) {
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

