<script lang="ts">
	import { createWindow } from '$lib/stores/windowStore';
	
	// Top navigation bar component
	let showMenu = false;
	
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
				// Handle close all windows
				break;
		}
	}
</script>

<div class="w-full h-1/25 bg-white border-b-4 border-black flex items-center justify-between px-6 fixed top-0 left-0 right-0 z-[2147483647] mix-blend-normal" style="background-color:#ffffff;">
    <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-black rounded-full flex items-center justify-center">
            <span class="text-white text-sm">👤</span>
        </div>
        <button 
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

<!-- Background overlay to close menu when clicking outside -->
{#if showMenu}
    <div class="fixed inset-0 z-[2147483647]" on:click={closeMenu}></div>
{/if}


<!-- Dropdown Menu -->
{#if showMenu}
    <div class="fixed bg-white border-4 border-black shadow-lg" style="top: 60px; left: 24px; width: 300px; z-index: 999999;">
        <!-- Header -->
        <div class="bg-white border-b-2 border-black px-4 py-2">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-black rounded-full flex items-center justify-center">
                    <span class="text-white text-xs">👤</span>
                </div>
                <span class="font-mono font-bold text-lg text-blue-600">Cyan Banister</span>
            </div>
        </div>
        <!-- Menu Items -->
        <div>
            <div class="menu-item" on:click={closeMenu} on:keydown={(e) => e.key === 'Enter' && closeMenu()} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">👤</span>
                </div>
                <span class="menu-item-text">About Me</span>
            </div>
            <div class="menu-item" on:click={() => handleMenuItemClick('terminal')} on:keydown={(e) => e.key === 'Enter' && handleMenuItemClick('terminal')} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">⬛</span>
                </div>
                <span class="menu-item-text">Terminal</span>
            </div>
            <div class="menu-item" on:click={closeMenu} on:keydown={(e) => e.key === 'Enter' && closeMenu()} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">🔄</span>
                </div>
                <span class="menu-item-text blue">Refresh ASCII</span>
            </div>
            <div class="menu-item" on:click={closeMenu} on:keydown={(e) => e.key === 'Enter' && closeMenu()} role="button" tabindex="0">
                <div class="menu-item-icon">
                    <span class="text-lg">❌</span>
                </div>
                <span class="menu-item-text">Close All Windows</span>
            </div>
        </div>
    </div>
{/if}