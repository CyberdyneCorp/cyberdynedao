<script lang="ts">
	import { createWindow, closeAllWindows } from '$lib/stores/windowStore';
	import { onMount } from 'svelte';
	
	// Top navigation bar component
	let showMenu = false;
	let menuContainer: HTMLElement;
	let menuButton: HTMLElement;
	
	function toggleMenu(event) {
		event?.preventDefault();
		event?.stopPropagation();
		console.log('Toggle menu clicked, showMenu:', showMenu);
		showMenu = !showMenu;
	}
	
	function closeMenu() {
		showMenu = false;
	}
	
	function handleMenuItemClick(action: string) {
		closeMenu();
		
		switch(action) {
			case 'terminal':
				createWindow('terminal', 'Terminal');
				break;
			case 'about':
				// Handle about me
				break;
			case 'refresh':
				// Handle refresh ASCII
				break;
			case 'close-all':
				closeAllWindows();
				break;
		}
	}
	
	function handleClickOutside(event: MouseEvent) {
		if (showMenu && menuContainer && menuButton && 
			!menuContainer.contains(event.target as Node) && 
			!menuButton.contains(event.target as Node)) {
			closeMenu();
		}
	}
	
	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});
</script>

<div class="w-full flex items-center justify-between px-6 fixed top-0 left-0 right-0 z-[2147483647] mix-blend-normal border-b-4 border-black" style="height: 60px; background: linear-gradient(to right, #1e3a8a, #3b82f6);">
    <button 
        bind:this={menuButton}
        class="flex items-center gap-3 px-4 py-2 rounded-lg transition-all duration-200 cursor-pointer"
        style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(10px);"
        on:mouseenter={(e) => e.target.style.background = 'rgba(255,255,255,0.25)'}
        on:mouseleave={(e) => e.target.style.background = 'rgba(255,255,255,0.15)'}
        on:click={toggleMenu}
    >
        <div class="w-10 h-10 flex items-center justify-center">
            <svg class="w-8 h-8" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <style>
                        .st0 { fill: #ffffff; }
                        .st1 { fill: #e0e7ff; }
                        .st2 { fill: #c7d2fe; }
                    </style>
                </defs>
                <path class="st1" d="M102,187.5c65.2-39.1,131.7-76.5,197.6-114.5l2.4.6,161.1,93c-19.4,2.1-36.6,17.8-37.1,38,0,3.8,2.4,9.5,0,12L107,400.5l-5,1.5v-93.5c58-34.9,117.3-68.2,176-102.1,3.2-.8,7.1,3.6,10.6,5.4,35.4,18.2,71.5-21.7,50.2-55.2-19.2-30.2-68-17.7-70.7,18s1.9,11.4-.1,13.9l-166,95.5v-96.5Z"/>
                <path class="st2" d="M497,414.5l-196.6,113.5-4.5-1.4c-23.3-14.6-48.2-26.9-71.6-41.4s-7.7-3.9-7.3-5.7l164.7-95.3c4.4,1.4,7.3,5,11.6,7,36.5,16.7,70.7-26,47.5-57.5-20.9-28.6-66.6-16.1-69.7,18.9s1.7,12-.6,14.4l-174.3,100.8-83.2-47.8,322-185.6c4.6-1.4,8.3,3.8,12.3,5.8,13.6,6.5,30.1,5,41.7-4.7l8-8.5v187.5Z"/>
                <polygon class="st0" points="536 164 536 436 516 425.3 515.5 176 302.7 52.8 300 50.5 300 29 536 164"/>
                <polygon class="st0" points="64 165 82.4 175.1 84 177.5 84.2 425.8 300 550.5 300 572 297.1 571.4 64 436.5 64 165"/>
            </svg>
        </div>
        <span class="font-mono font-bold text-xl text-white" style="text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">
            Start {showMenu ? '▼' : '▶'}
        </span>
    </button>
    
    <div class="flex items-center" style="margin-right: 12px;">
        <button class="px-3 py-1.5 bg-green-500 border-2 border-black retro-button flex items-center justify-center hover:bg-green-600">
            <span class="text-white text-sm font-mono font-semibold">Connect Wallet</span>
        </button>
    </div>
</div>

<!-- Dropdown Menu -->
{#if showMenu}
    <div bind:this={menuContainer} class="fixed bg-white border-2 border-black shadow-lg" style="top: 50px; left: 24px; width: 300px; z-index: 2147483647;">
        <!-- Header -->
        <div style="background: linear-gradient(to right, #1e3a8a, #3b82f6); border-bottom: 2px solid black; padding: 8px 12px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.2); border-radius: 4px; border: 1px solid rgba(255,255,255,0.3);">
                    <img src="/assets/icon_menu.svg" alt="Menu" style="width: 24px; height: 24px;" />
                </div>
                <span style="font-family: monospace; font-weight: bold; font-size: 24px; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">Menu</span>
            </div>
        </div>
        <!-- Menu Items -->
        <div>
            <div class="menu-item" on:click={closeMenu} on:keydown={(e) => e.key === 'Enter' && closeMenu()} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <img src="/assets/the_team.svg" alt="Our Team" class="w-6 h-6" />
                </div>
                <span class="menu-item-text">Our Team</span>
            </div>
            <div class="menu-item" on:click={() => handleMenuItemClick('terminal')} on:keydown={(e) => e.key === 'Enter' && handleMenuItemClick('terminal')} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <img src="/assets/icon_terminal.svg" alt="Terminal" class="w-6 h-6" />
                </div>
                <span class="menu-item-text">Terminal</span>
            </div>
            <div class="menu-item" on:click={() => handleMenuItemClick('close-all')} on:keydown={(e) => e.key === 'Enter' && handleMenuItemClick('close-all')} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-xl">❌</span>
                </div>
                <span class="menu-item-text">Close All Windows</span>
            </div>
        </div>
    </div>
{/if}