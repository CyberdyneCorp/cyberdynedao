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

<div class="terminal-container">
	<div class="terminal-content cursor-text" on:click={focusInput}>
		{#each terminalHistory as line}
			<div class="terminal-line">
				{#if line.type === 'input'}
					<span class="terminal-input-text">{line.text}</span>
				{:else if line.type === 'output'}
					<span class="terminal-output-text">{line.text}</span>
				{:else}
					<span class="terminal-system-text">{line.text}</span>
				{/if}
			</div>
		{/each}
	</div>
	
	<div class="terminal-prompt">
		<span class="terminal-prompt-text">{currentUser}@{currentHost} $ </span>
		<input 
			bind:value={terminalInput}
			on:keydown={handleKeyDown}
			class="terminal-input"
			placeholder=""
			autocomplete="off"
			spellcheck="false"
		/>
	</div>
</div>

<style>
	.terminal-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		background-color: #000;
		color: #00ff00;
		font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
		font-size: 16px;
	}
	
	.terminal-content {
		flex: 1;
		overflow-y: auto;
		padding: 16px;
		min-height: 0;
	}
	
	.terminal-line {
		white-space: pre-wrap;
		margin-bottom: 4px;
	}
	
	.terminal-input-text {
		color: #00ff00;
	}
	
	.terminal-output-text {
		color: #00dd00;
	}
	
	.terminal-system-text {
		color: #00aa00;
	}
	
	.terminal-prompt {
		border-top: 1px solid #166534;
		padding: 16px;
		display: flex;
		align-items: center;
	}
	
	.terminal-prompt-text {
		color: #00ff00;
		margin-right: 8px;
	}
	
	.terminal-input {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		color: #00ff00;
		font-family: inherit;
		font-size: inherit;
		caret-color: #00ff00;
	}
</style>