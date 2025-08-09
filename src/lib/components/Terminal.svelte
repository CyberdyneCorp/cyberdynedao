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
	
	// Auto-focus on mount
	onMount(() => {
		setTimeout(() => {
			focusInput();
		}, 200);
	});
</script>

<div class="flex flex-col h-full bg-black text-retro-green font-mono text-base">
	<div class="flex-1 overflow-y-auto p-4 min-h-0 cursor-text" on:click={focusInput}>
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
	
	<div class="border-t border-retro-border p-4 flex items-center">
		<span class="text-retro-green mr-2">{currentUser}@{currentHost} $ </span>
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

