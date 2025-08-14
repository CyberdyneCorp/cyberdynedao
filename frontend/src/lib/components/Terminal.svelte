<script lang="ts">
	import { onMount } from 'svelte';
	import { terminalCommands } from '$lib/utils/terminalCommands';
	
	// Terminal state
	let terminalInput = '';
	let terminalHistory: Array<{
		type: 'input' | 'output' | 'system', 
		text: string, 
		timestamp?: string
	}> = [
		{ type: 'system', text: 'Welcome to CyberdyneOS!' },
		{ type: 'system', text: 'For available commands, try "help".' },
		{ type: 'system', text: `Last login: ${new Date().toLocaleDateString()}, ${new Date().toLocaleTimeString()}` },
		{ type: 'system', text: '' }
	];
	
	const currentUser = 'user';
	const currentHost = 'CyberdyneOS';
	
	function handleSubmit() {
		if (terminalInput.trim() === '') return;
		
		// Add user input to history
		terminalHistory = [...terminalHistory, { 
			type: 'input', 
			text: `${currentUser}@${currentHost} $ ${terminalInput}`,
			timestamp: new Date().toLocaleTimeString()
		}];
		
		// Process command and get response
		const response = terminalCommands.processCommand(terminalInput.trim());
		
		// Handle special commands
		if (terminalInput.trim().toLowerCase() === 'clear') {
			terminalHistory = [
				{ type: 'system', text: 'Welcome to CyberdyneOS!' },
				{ type: 'system', text: 'For available commands, try "help".' }
			];
		} else {
			terminalHistory = [...terminalHistory, { 
				type: 'output', 
				text: response 
			}];
		}
		
		// Clear input and scroll
		terminalInput = '';
		scrollToBottom();
	}
	
	function scrollToBottom() {
		setTimeout(() => {
			const terminal = document.querySelector('.terminal-content');
			if (terminal) {
				terminal.scrollTop = terminal.scrollHeight;
			}
		}, 10);
	}
	
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			handleSubmit();
		}
	}
	
	function focusInput() {
		const input = document.querySelector('.terminal-input') as HTMLInputElement;
		if (input) {
			input.focus();
		}
	}

	function handleTerminalKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			focusInput();
		}
	}
	
	// Auto-focus on mount
	onMount(() => {
		setTimeout(() => {
			focusInput();
		}, 200);
	});
</script>

<div class="flex flex-col h-full bg-black text-retro-green font-mono text-base terminal-container">
	<div 
		class="flex-1 overflow-y-auto p-4 min-h-0 cursor-text terminal-output" 
		on:click={focusInput}
		on:keydown={handleTerminalKeyDown}
		role="button"
		tabindex="0"
		aria-label="Terminal output - click to focus input"
	>
		{#each terminalHistory as line}
			<div class="whitespace-pre-wrap mb-1">
				{#if line.type === 'input'}
					<span class="text-retro-green">{line.text}</span>
				{:else if line.type === 'output'}
					<span class="text-retro-green-dark">{line.text}</span>
				{:else}
					<span class="text-retro-green-darker">{line.text}</span>
				{/if}
			</div>
		{/each}
	</div>
	
	<div class="border-t border-retro-border p-4 flex items-center terminal-input-container">
		<span class="text-retro-green mr-2 terminal-prompt">{currentUser}@{currentHost} $ </span>
		<input 
			bind:value={terminalInput}
			on:keydown={handleKeyDown}
			class="flex-1 terminal-input"
			placeholder=""
			autocomplete="off"
			spellcheck="false"
		/>
	</div>
</div>

<style>
	.terminal-container {
		min-height: 200px;
	}
	
	.terminal-output {
		scrollbar-width: thin;
		scrollbar-color: #00aa00 #001100;
	}
	
	.terminal-prompt {
		flex-shrink: 0;
		white-space: nowrap;
	}
	
	.terminal-input-container {
		flex-shrink: 0;
		min-height: 48px;
		align-items: center;
	}
	
	/* Mobile optimizations */
	@media (max-width: 768px) {
		.terminal-container {
			font-size: 14px;
		}
		
		.terminal-output {
			padding: 8px 12px;
		}
		
		.terminal-input-container {
			padding: 8px 12px;
			min-height: 44px;
		}
		
		.terminal-prompt {
			font-size: 13px;
			margin-right: 8px;
		}
	}
	
	@media (max-width: 480px) {
		.terminal-container {
			font-size: 13px;
		}
		
		.terminal-output {
			padding: 6px 8px;
		}
		
		.terminal-input-container {
			padding: 6px 8px;
			min-height: 40px;
		}
		
		.terminal-prompt {
			font-size: 12px;
			margin-right: 6px;
		}
	}
	
	/* Improve touch targets on mobile */
	@media (hover: none) and (pointer: coarse) {
		.terminal-input-container {
			min-height: 48px;
		}
	}
</style>

