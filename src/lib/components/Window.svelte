<script lang="ts">
	import { onMount } from 'svelte';
	import type { WindowState } from '$lib/stores/windowStore';
	import { bringToFront, closeWindow, minimizeWindow, maximizeWindow, windows } from '$lib/stores/windowStore';
	import TerminalWindow from './TerminalWindow.svelte';

	export let window: WindowState;
	export let cartItems: any[] = [];
	export let onAddToCart: ((item: any) => void) | undefined = undefined;

	let windowElement: HTMLDivElement;
	let titleBarElement: HTMLDivElement;
	let isDragging = false;
	let isResizing = false;
	let dragOffset = { x: 0, y: 0 };
	let resizeStartSize = { width: 0, height: 0 };
	let resizeStartMouse = { x: 0, y: 0 };

	function handleMouseDown(e: MouseEvent) {
		if (e.target === titleBarElement || titleBarElement.contains(e.target as Node)) {
			isDragging = true;
			dragOffset.x = e.clientX - window.x;
			dragOffset.y = e.clientY - window.y;
			bringToFront(window.id);
		}
	}

	function handleResizeStart(e: MouseEvent) {
		isResizing = true;
		resizeStartSize.width = window.width;
		resizeStartSize.height = window.height;
		resizeStartMouse.x = e.clientX;
		resizeStartMouse.y = e.clientY;
		bringToFront(window.id);
		e.stopPropagation();
	}

	function handleMouseMove(e: MouseEvent) {
		if (isDragging) {
			windows.update(wins => wins.map(w => 
				w.id === window.id 
					? { ...w, x: e.clientX - dragOffset.x, y: e.clientY - dragOffset.y }
					: w
			));
		} else if (isResizing) {
			const deltaX = e.clientX - resizeStartMouse.x;
			const deltaY = e.clientY - resizeStartMouse.y;
			windows.update(wins => wins.map(w => 
				w.id === window.id 
					? { 
						...w, 
						width: Math.max(300, resizeStartSize.width + deltaX),
						height: Math.max(200, resizeStartSize.height + deltaY)
					}
					: w
			));
		}
	}

	function handleMouseUp() {
		isDragging = false;
		isResizing = false;
	}

	function handleWindowClick() {
		bringToFront(window.id);
	}

	onMount(() => {
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);

		return () => {
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		};
	});

	$: windowStyle = `
		left: ${window.x}px;
		top: ${window.y}px;
		width: ${window.maximized ? '100vw' : `${window.width}px`};
		height: ${window.maximized ? '100vh' : `${window.height}px`};
		z-index: ${window.zIndex};
		display: ${window.minimized ? 'none' : 'block'};
	`;
</script>

<div
	bind:this={windowElement}
	class="fixed retro-window overflow-hidden"
	style={windowStyle}
	on:mousedown={handleWindowClick}
	role="dialog"
	tabindex="-1"
>
	<div
		bind:this={titleBarElement}
		class="bg-white border-b-4 border-black p-1 flex items-center cursor-move"
		on:mousedown={handleMouseDown}
		role="button"
		tabindex="0"
		style="background: linear-gradient(to bottom, #ffffff 0%, #e5e5e5 50%, #ffffff 100%);"
	>
		<div class="flex items-center gap-1 px-2">
			<div class="w-4 h-1 bg-black"></div>
			<div class="w-4 h-1 bg-black"></div>
			<div class="w-4 h-1 bg-black"></div>
		</div>
		
		<div class="flex-1 text-center">
			<div class="inline-block bg-white border-2 border-black px-4 py-1" style="background: linear-gradient(to bottom, #ffffff 0%, #f0f0f0 100%);">
				<h2 class="font-mono font-bold text-black text-sm">{window.title}</h2>
			</div>
		</div>
		
		<div class="flex items-center gap-1 px-2">
			<button 
				class="w-6 h-4 bg-gray-300 border border-black text-xs font-mono hover:bg-gray-400 flex items-center justify-center"
				on:click={() => minimizeWindow(window.id)}
			>
				_
			</button>
			<button 
				class="w-6 h-4 bg-gray-300 border border-black text-xs font-mono hover:bg-gray-400 flex items-center justify-center"
				on:click={() => maximizeWindow(window.id)}
			>
				□
			</button>
			<button 
				class="w-6 h-4 bg-gray-300 border border-black text-xs font-mono hover:bg-gray-400 flex items-center justify-center"
				on:click={() => closeWindow(window.id)}
			>
				×
			</button>
		</div>
	</div>
	
	<div class="bg-white h-full overflow-hidden relative">
		<TerminalWindow 
			title={window.title}
			showCart={window.content === 'cart'}
			currentView={window.content}
			bind:cartItems
			{onAddToCart}
			embedded={true}
		/>
		
		<!-- Resize handle -->
		<div 
			class="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize bg-gray-300 border-l-2 border-t-2 border-black"
			on:mousedown={handleResizeStart}
			role="button"
			tabindex="0"
		></div>
	</div>
</div>