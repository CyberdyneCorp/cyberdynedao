<script lang="ts">
	import Window from '$lib/components/Window.svelte';
	import { windows, createWindow } from '$lib/stores/windowStore';
	
	import { navItems, viewMap, type NavItem } from '$lib/constants/navigation';

	let cartItems: any[] = [];
	
	function addToCart(item: any) {
		cartItems = [...cartItems, item];
	}
	
	function handleItemClick(item: NavItem) {
		const view = viewMap[item.name] || item.name.toLowerCase();
		createWindow(view, item.name);
	}
	
	$: cartCount = cartItems.length;
</script>

<div class="flex flex-col h-screen">
    <div class="flex-1 relative bg-retro-bg overflow-hidden">
		<!-- Enhanced Futuristic Background Animation -->
		<div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; opacity: 1.2;">
			
			<!-- Grid Pattern -->
			<div class="cyber-grid" style="z-index: 1;"></div>
			
			<!-- Floating Particles -->
			<div class="glow-particle glow-1" style="z-index: 2;"></div>
			<div class="glow-particle glow-2" style="z-index: 2;"></div>
			<div class="glow-particle glow-3" style="z-index: 2;"></div>
			
			<!-- Digital Rain -->
			<div class="digital-rain rain-1" style="z-index: 2;"></div>
			<div class="digital-rain rain-2" style="z-index: 2;"></div>
			
			<!-- ASCII Cyberdyne Logo with Wavy Glow -->
			<div class="ascii-logo" style="z-index: 2;">
				<pre class="logo-text">                                            ██▄,
                                            ▀█████▄
                                               └▀█████▄
                                        ╓@╣╬╬╣▒╓   └▀████▓▄
                                    ,#╣╬╬╬╬╬╬╬╬╬╬╣φ╓   ╙▀████▓µ
                                ,╗╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣φ,   ╙▀████▄,
                            ,eΦ╬╬╬╬╬╬╬╬╬╬╬╬╣╝╝╣╬╬╬╬╬╬╬╬╬╬▒╗.   ╙█████▄
                         ╔Φ╣╬╬╬╬╬╬╬╬╬╬╬╬╣`      "╣╬╬╬╬╬╬╬╬╬╬╬▒╗    ▀█████▄
            ▓µ       ╓@╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣          ╣╬╬╬╬╬╬╬╬╬╬╬╬╣╨^    └▀████
            ██▌  ,@╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬          ╣╬╬╬╬╬╬╬╬╬╬╣           ╫██
            ██▌  ╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╜└           @╬╬╬╬╬╬╬╬╬╬╬⌐           ╫██
            ██▌  ╫╬╬╬╬╬╬╬╬╬╬╬╬╬╣╩└    ╓@╣╬▒╗gg╗Φ╬╬╬╬╬╬╬╬╬╬╬╬╩            ╫██
            ██▌  ╫╬╬╬╬╬╬╬╬╬╬╝╙    ,#╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╝╙    ╓       ▄  ╫██
            ██▌  ╫╬╬╬╬╬╬╝╙    ,╗Φ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╝╙    ,φ▓▓▓▓▓▓▌▓▓▓▓  ╫██
            ██▌  ╫╬╬╣╙    ,╔Φ╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╙    ,╗▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ╫██
            ██▌  ╙`    ╔Φ╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╜└    ╥Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ╫██
            ██▌    ╓@╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╣╩└    ╓Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ╫██
            ██▌  ╣╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╝╙    ╓φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ╫██
            ██▌  ╫╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╝╙    ,φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓Γ      ╙▓▓▓▓▓▓▓▓  ╫██
            ██▌  ╫╬╬╬╬╬╬╬╬╬╬╬╣╙    ,╗▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          ▓▓▓▓▓▓▓  ╫██
            ██▌  ╫╬╬╬╬╬╬╬╣╜`    ▄Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌          ╣▓▓▓▓▓▓  ╫██
            ██▌  ╫╬╬╬╣╨└    ╓Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀Γ           ▄▓▓▓▓▓▓▓  ╫██
            ██▌  ╫╝╙    ╓φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀╙    ╓▄▓▓▌╗╖╖╗Φ▓▓▓▓▓▓▓▓▓  ╫██
            ██▌     ,▄▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀╜    ,φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ╫██
            ███▄   └▀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╨└   ,╗▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀╙    └██
            ╙▀████▌╓   ╙▀▓▓▓▓▓▓▓▓▓▓▀└    ▄Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀╙
                ╙▀████▄,   ╙▀▓▓▀Γ    ╓Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌╨
                    ▀█████▄      ╓Φ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀└
                       ─▀█████▄   └▀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀└
                           └▀████▓▄   └▀▓▓▓▓▓▓▓▓▀Γ
                               ╙▀████▓µ   ╙▀▀╙
                                   ╙▀████▄,
                                       ╙████
                                           ▀</pre>
			</div>
		</div>
		<!-- Desktop Icons positioned on main area -->
		<div class="absolute left-8 top-1/15 z-10">
			<div class="grid grid-cols-2" style="gap: 50px 70px;">
				{#each navItems as item}
					<div class="flex flex-col items-center">
						<button
							class="sidebar-icon flex items-center justify-center cursor-pointer"
							on:click={() => handleItemClick(item)}
							title={item.name}
						>
							<img src={item.icon} alt={item.name} class="w-24 h-24" />
						</button>
						<span class="nav-label text-white text-base font-mono text-center px-2 py-0.5 rounded mt-4">
							{item.name}
						</span>
					</div>
				{/each}
			</div>
		</div>
		
		<!-- Cart icon in right corner at same height as other icons -->
		<div class="absolute right-1/10 top-1/15 z-20">
			<div class="flex flex-col items-center">
				<button
					class="sidebar-icon flex items-center justify-center cursor-pointer relative"
					on:click={() => createWindow('cart', `Your Bag (${cartCount})`)}
					title="Your Bag"
				>
					<img src="/assets/cart.svg" alt="Cart" class="w-24 h-24" />
					{#if cartCount > 0}
						<div class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
							{cartCount}
						</div>
					{/if}
				</button>
				<span class="nav-label text-white text-base font-mono text-center px-2 py-0.5 rounded mt-4">
					Your Bag {cartCount > 0 ? `(${cartCount})` : ''}
				</span>
			</div>
		</div>
		
		<!-- Windows -->
		{#each $windows as window (window.id)}
			<Window 
				{window}
				bind:cartItems
				onAddToCart={addToCart}
			/>
		{/each}
	</div>
</div>

<style global>
	/* Discrete Futuristic Background Animations */
	.cyber-grid {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image: 
			linear-gradient(rgba(0, 255, 255, 0.25) 1px, transparent 1px),
			linear-gradient(90deg, rgba(0, 255, 255, 0.25) 1px, transparent 1px);
		background-size: 60px 60px;
		animation: grid-pulse 25s linear infinite;
	}
	
	@keyframes grid-pulse {
		0%, 100% { 
			opacity: 0.4;
			transform: translate(0, 0);
		}
		50% { 
			opacity: 0.7;
			transform: translate(30px, 30px);
		}
	}
	
	.glow-particle {
		position: absolute;
		width: 6px;
		height: 6px;
		background: #00ffff;
		border-radius: 50%;
		box-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
		animation: particle-glow 6s ease-in-out infinite;
	}
	
	.glow-1 {
		top: 20%;
		left: 20%;
		animation-delay: 0s;
	}
	
	.glow-2 {
		top: 60%;
		right: 20%;
		animation-delay: -2s;
	}
	
	.glow-3 {
		bottom: 30%;
		left: 60%;
		animation-delay: -4s;
	}
	
	@keyframes particle-glow {
		0%, 100% {
			transform: scale(1);
			opacity: 0.7;
		}
		50% {
			transform: scale(1.5);
			opacity: 1.0;
		}
	}
	
	.digital-rain {
		position: absolute;
		width: 2px;
		height: 200px;
		background: linear-gradient(to bottom, 
			transparent, 
			rgba(0, 255, 255, 0.7) 30%, 
			rgba(0, 255, 255, 0.9) 50%, 
			rgba(0, 255, 255, 0.7) 70%, 
			transparent
		);
		animation: rain-fall 5s linear infinite;
	}
	
	.rain-1 {
		left: 25%;
		animation-delay: 0s;
	}
	
	.rain-2 {
		right: 30%;
		animation-delay: -2.5s;
	}
	
	@keyframes rain-fall {
		0% {
			top: -150px;
			opacity: 0;
		}
		20% {
			opacity: 1;
		}
		80% {
			opacity: 1;
		}
		100% {
			top: 100vh;
			opacity: 0;
		}
	}
	
	/* ASCII Cyberdyne Logo with Wavy Glow Effect */
	.ascii-logo {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		opacity: 0.25;
		pointer-events: none;
		animation: logo-breathe 8s ease-in-out infinite;
	}
	
	.logo-text {
		font-family: 'JetBrains Mono', monospace;
		font-size: 12px;
		line-height: 1;
		color: #00ffff;
		text-shadow: 
			0 0 12px rgba(0, 255, 255, 0.8),
			0 0 24px rgba(0, 255, 255, 0.6),
			0 0 36px rgba(0, 255, 255, 0.4);
		animation: 
			wavy-glow 4s ease-in-out infinite,
			text-wave 6s ease-in-out infinite;
		white-space: pre;
		margin: 0;
		padding: 0;
	}
	
	@keyframes logo-breathe {
		0%, 100% {
			opacity: 0.08;
			transform: translate(-50%, -50%) scale(0.95);
		}
		50% {
			opacity: 0.2;
			transform: translate(-50%, -50%) scale(1.05);
		}
	}
	
	@keyframes wavy-glow {
		0%, 100% {
			text-shadow: 
				0 0 5px rgba(0, 255, 255, 0.3),
				0 0 10px rgba(0, 255, 255, 0.2),
				0 0 15px rgba(0, 255, 255, 0.1);
		}
		25% {
			text-shadow: 
				2px 0 8px rgba(0, 255, 255, 0.6),
				0 0 15px rgba(0, 255, 255, 0.4),
				0 0 25px rgba(0, 255, 255, 0.2);
		}
		50% {
			text-shadow: 
				0 2px 10px rgba(0, 255, 255, 0.7),
				0 0 20px rgba(0, 255, 255, 0.5),
				0 0 30px rgba(0, 255, 255, 0.3);
		}
		75% {
			text-shadow: 
				-2px 0 8px rgba(0, 255, 255, 0.6),
				0 0 15px rgba(0, 255, 255, 0.4),
				0 0 25px rgba(0, 255, 255, 0.2);
		}
	}
	
	@keyframes text-wave {
		0%, 100% {
			transform: translateY(0px);
		}
		25% {
			transform: translateY(-2px);
		}
		50% {
			transform: translateY(-1px);
		}
		75% {
			transform: translateY(-3px);
		}
	}
</style>
