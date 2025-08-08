<script lang="ts">
    import { onMount } from 'svelte';
    import type { WindowState } from '$lib/stores/windowStore';
    import { bringToFront, closeWindow, windows } from '$lib/stores/windowStore';
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
    class="retro-window window-root"
    style={windowStyle}
    on:mousedown={handleWindowClick}
    role="dialog"
    tabindex="-1"
>
    <div
        bind:this={titleBarElement}
        class="title-bar"
        on:mousedown={handleMouseDown}
        role="button"
        tabindex="0"
    >
        <div class="title-controls">
            <button 
                class="window-control"
                on:click={() => closeWindow(window.id)}
            >
                ×
            </button>
        </div>

        <div class="title-lines">
            <div class="title-line"></div>
            <div class="title-line"></div>
            <div class="title-line"></div>
        </div>
        
        <div class="title-center">
            <div class="title-pill">
                <h2 class="title-text">{window.title}</h2>
            </div>
        </div>
    </div>
	
    <div class="window-content">
		<TerminalWindow 
			title={window.title}
			showCart={window.content === 'cart'}
			currentView={window.content}
			bind:cartItems
			{onAddToCart}
			embedded={true}
		/>
	</div>

    <div class="window-footer">
        <div class="footer-spacer"></div>
        <div class="footer-controls">
            <div 
                class="footer-resize-control"
                on:mousedown={handleResizeStart}
                role="button"
                tabindex="0"
                aria-label="Resize window"
            ></div>
        </div>
    </div>
</div>