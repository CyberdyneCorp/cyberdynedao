<script lang="ts">
    import { onMount } from 'svelte';
    import type { WindowState } from '$lib/stores/windowStore';
    import { bringToFront, closeWindow, windows } from '$lib/stores/windowStore';
    import TerminalWindow from './TerminalWindow.svelte';

	export let window: WindowState;
	import type { CartItem } from '$lib/types/cart';
	
	export let cartItems: CartItem[] = [];
	export let onAddToCart: ((item: CartItem) => void) | undefined = undefined;

	let windowElement: HTMLDivElement;
	let titleBarElement: HTMLDivElement;
	let isDragging = false;
	let isResizing = false;
	let resizeDirection = '';
	let dragOffset = { x: 0, y: 0 };
	let resizeStartSize = { width: 0, height: 0 };
	let resizeStartMouse = { x: 0, y: 0 };
	let isMobile = false;
	let touchStartPos = { x: 0, y: 0 };
	let touchStartSize = { width: 0, height: 0 };

	// Check if device is mobile
	function checkMobile() {
		isMobile = globalThis.window.innerWidth <= 768 || 'ontouchstart' in globalThis.window;
	}

	function handleMouseDown(e: MouseEvent) {
		if (e.target === titleBarElement || titleBarElement.contains(e.target as Node)) {
			isDragging = true;
			dragOffset.x = e.clientX - window.x;
			dragOffset.y = e.clientY - window.y;
			bringToFront(window.id);
		}
	}

	function handleTouchStart(e: TouchEvent) {
		if (e.target === titleBarElement || titleBarElement.contains(e.target as Node)) {
			isDragging = true;
			const touch = e.touches[0];
			dragOffset.x = touch.clientX - window.x;
			dragOffset.y = touch.clientY - window.y;
			bringToFront(window.id);
		}
	}

	function handleResizeStart(e: MouseEvent) {
		if (isMobile) return; // Disable resize on mobile
		
		isResizing = true;
		
		// Determine resize direction based on target class
		const target = e.target as HTMLElement;
		if (target.classList.contains('resize-right')) {
			resizeDirection = 'right';
		} else if (target.classList.contains('resize-bottom')) {
			resizeDirection = 'bottom';
		} else {
			resizeDirection = 'se'; // southeast (both width and height)
		}
		
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
		} else if (isResizing && !isMobile) {
			const deltaX = e.clientX - resizeStartMouse.x;
			const deltaY = e.clientY - resizeStartMouse.y;
			
			windows.update(wins => wins.map(w => {
				if (w.id === window.id) {
					let newWidth = w.width;
					let newHeight = w.height;
					
					if (resizeDirection === 'right' || resizeDirection === 'se') {
						newWidth = Math.max(300, resizeStartSize.width + deltaX);
					}
					if (resizeDirection === 'bottom' || resizeDirection === 'se') {
						newHeight = Math.max(200, resizeStartSize.height + deltaY);
					}
					
					return { ...w, width: newWidth, height: newHeight };
				}
				return w;
			}));
		}
	}

	function handleTouchMove(e: TouchEvent) {
		if (isDragging) {
			const touch = e.touches[0];
			windows.update(wins => wins.map(w => 
				w.id === window.id 
					? { ...w, x: touch.clientX - dragOffset.x, y: touch.clientY - dragOffset.y }
					: w
			));
		}
	}

	function handleMouseUp() {
		isDragging = false;
		isResizing = false;
	}

	function handleTouchEnd() {
		isDragging = false;
		isResizing = false;
	}

	function handleWindowClick() {
		bringToFront(window.id);
	}

	// Mobile-specific window positioning
	function centerOnMobile() {
		if (isMobile && window.width > globalThis.window.innerWidth) {
			windows.update(wins => wins.map(w => 
				w.id === window.id 
					? { ...w, x: 0, width: Math.min(globalThis.window.innerWidth - 20, w.width) }
					: w
			));
		}
	}

	onMount(() => {
		checkMobile();
		centerOnMobile();
		
		// Add event listeners
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
		document.addEventListener('touchmove', handleTouchMove, { passive: false });
		document.addEventListener('touchend', handleTouchEnd);
		
		// Handle window resize
		globalThis.window.addEventListener('resize', checkMobile);

		return () => {
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
			document.removeEventListener('touchmove', handleTouchMove);
			document.removeEventListener('touchend', handleTouchEnd);
			globalThis.window.removeEventListener('resize', checkMobile);
		};
	});

	$: windowStyle = `
		left: ${window.x}px;
		top: ${window.y}px;
		width: ${window.maximized ? '100vw' : `${window.width}px`};
		min-height: ${window.maximized ? '100vh' : `${window.height}px`};
		z-index: ${window.zIndex};
		display: ${window.minimized ? 'none' : 'block'};
		transition: ${isDragging || isResizing ? 'none' : 'left 0.3s ease-out, top 0.3s ease-out'};
		${isMobile ? 'max-width: calc(100vw - 20px); max-height: calc(100vh - 20px);' : ''}
	`;
</script>

<div
    bind:this={windowElement}
    class="retro-window window-root"
    class:mobile={isMobile}
    style={windowStyle}
    on:mousedown={handleWindowClick}
    on:touchstart={handleTouchStart}
    role="dialog"
    tabindex="-1"
>
    <div
        bind:this={titleBarElement}
        class="title-bar modern"
        on:mousedown={handleMouseDown}
        on:touchstart={handleTouchStart}
        role="button"
        tabindex="0"
    >
        <div class="title-layout-modern">
            <div class="hamburger-icon">
                <div class="hamburger-line"></div>
                <div class="hamburger-line"></div>
                <div class="hamburger-line"></div>
            </div>
            
            <button 
                class="window-control close"
                on:click={() => closeWindow(window.id)}
            >×</button>
            
            <div class="title-bars-left">
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
            </div>
            
            <span class="title-text-modern">{window.title}</span>
            
            <div class="title-bars-right">
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
                <div class="title-bar-line"></div>
            </div>
        </div>
    </div>
	
    <div class="window-content" style="max-height: calc({window.height}px - 72px); {window.content === 'terminal' ? 'height: calc(' + window.height + 'px - 72px);' : ''}">
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
        <div class="footer-left">
            <span class="footer-status">{window.title}</span>
        </div>
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
    
    <!-- Resize handles - hidden on mobile -->
    {#if !isMobile}
        <div 
            class="resize-handle resize-right" 
            on:mousedown={handleResizeStart}
            role="button"
            tabindex="0"
            aria-label="Resize window horizontally"
        ></div>
        <div 
            class="resize-handle resize-bottom" 
            on:mousedown={handleResizeStart}
            role="button"
            tabindex="0"
            aria-label="Resize window vertically"
        ></div>
    {/if}
</div>

<style>
    .retro-window.mobile {
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .retro-window.mobile .title-bar {
        border-radius: 8px 8px 0 0;
    }
    
    .retro-window.mobile .window-footer {
        border-radius: 0 0 8px 8px;
    }
    
    /* Mobile touch improvements */
    @media (max-width: 768px) {
        .retro-window {
            touch-action: manipulation;
        }
        
        .title-bar {
            min-height: 44px;
        }
        
        .window-control {
            min-width: 44px;
            min-height: 44px;
        }
        
        .title-text-modern {
            font-size: 14px;
        }
        
        .window-content {
            padding: 12px;
        }
        
        .window-footer {
            min-height: 36px;
        }
        
        .footer-status {
            font-size: 11px;
        }
    }
    
    /* Very small screens */
    @media (max-width: 480px) {
        .retro-window {
            margin: 10px;
        }
        
        .title-text-modern {
            font-size: 13px;
        }
        
        .window-content {
            padding: 8px;
        }
    }
</style>