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

<div class="w-full h-1/25 bg-white border-b-4 border-black flex items-center justify-between px-6 fixed top-0 left-0 right-0 z-[2147483647] mix-blend-normal" style="background-color:#ffffff;">
    <div class="flex items-center gap-3">
        <div class="w-10 h-10 flex items-center justify-center">
            <svg class="w-8 h-8" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <style>
                        .st0 { fill: #1c1941; }
                        .st1 { fill: #02adee; }
                        .st2 { fill: #3972c1; }
                    </style>
                </defs>
                <path class="st1" d="M102,187.5c65.2-39.1,131.7-76.5,197.6-114.5l2.4.6,161.1,93c-19.4,2.1-36.6,17.8-37.1,38,0,3.8,2.4,9.5,0,12L107,400.5l-5,1.5v-93.5c58-34.9,117.3-68.2,176-102.1,3.2-.8,7.1,3.6,10.6,5.4,35.4,18.2,71.5-21.7,50.2-55.2-19.2-30.2-68-17.7-70.7,18s1.9,11.4-.1,13.9l-166,95.5v-96.5Z"/>
                <path class="st2" d="M497,414.5l-196.6,113.5-4.5-1.4c-23.3-14.6-48.2-26.9-71.6-41.4s-7.7-3.9-7.3-5.7l164.7-95.3c4.4,1.4,7.3,5,11.6,7,36.5,16.7,70.7-26,47.5-57.5-20.9-28.6-66.6-16.1-69.7,18.9s1.7,12-.6,14.4l-174.3,100.8-83.2-47.8,322-185.6c4.6-1.4,8.3,3.8,12.3,5.8,13.6,6.5,30.1,5,41.7-4.7l8-8.5v187.5Z"/>
                <polygon class="st0" points="536 164 536 436 516 425.3 515.5 176 302.7 52.8 300 50.5 300 29 536 164"/>
                <polygon class="st0" points="64 165 82.4 175.1 84 177.5 84.2 425.8 300 550.5 300 572 297.1 571.4 64 436.5 64 165"/>
            </svg>
        </div>
        <button 
            bind:this={menuButton}
            class="font-mono font-bold text-xl text-black cursor-pointer transition-colors duration-200"
            style="color: #000;"
            on:mouseenter={(e) => e.target.style.color = '#c084fc'}
            on:mouseleave={(e) => e.target.style.color = '#000'}
            on:click={toggleMenu}
        >
            Cyberdyne DAO {showMenu ? '▼' : '▶'}
        </button>
    </div>
    
    <div class="flex items-center gap-3">
        <button class="px-4 py-2 bg-green-500 border-2 border-black retro-button flex items-center justify-center hover:bg-green-600">
            <span class="text-white text-sm font-mono">Connect Wallet</span>
        </button>
    </div>
</div>

<!-- Dropdown Menu -->
{#if showMenu}
    <div bind:this={menuContainer} class="fixed bg-white border-4 border-black shadow-lg" style="top: 50px; left: 24px; width: 300px; z-index: 2147483647;">
        <!-- Header -->
        <div class="bg-white border-b-2 border-black px-4 py-2">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 flex items-center justify-center">
                    <img src="/assets/icon_menu.svg" alt="Menu" class="w-6 h-6" />
                </div>
                <span class="font-mono font-bold text-lg text-blue-600">Menu</span>
            </div>
        </div>
        <!-- Menu Items -->
        <div>
            <div class="menu-item" on:click={closeMenu} on:keydown={(e) => e.key === 'Enter' && closeMenu()} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">👤</span>
                </div>
                <span class="menu-item-text">Our Team</span>
            </div>
            <div class="menu-item" on:click={() => handleMenuItemClick('terminal')} on:keydown={(e) => e.key === 'Enter' && handleMenuItemClick('terminal')} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">⬛</span>
                </div>
                <span class="menu-item-text">Terminal</span>
            </div>
            <div class="menu-item" on:click={() => handleMenuItemClick('close-all')} on:keydown={(e) => e.key === 'Enter' && handleMenuItemClick('close-all')} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">❌</span>
                </div>
                <span class="menu-item-text">Close All Windows</span>
            </div>
        </div>
    </div>
{/if}