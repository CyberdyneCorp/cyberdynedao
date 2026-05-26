<script lang="ts">
	import { onMount } from 'svelte';
	import { createTerminalViewModel } from '$lib/viewmodels/terminalViewModel';
	import { sendChatMessage, startChatSession } from '$lib/api/contentApi';

	const vm = createTerminalViewModel();
	const terminalHistory = vm.history;
	const currentUser = vm.user;
	const currentHost = vm.host;
	let terminalInput = '';

	// Lazy chat session — created on first `ask` use.
	let chatSessionId: string | null = null;
	let isAsking = false;

	async function handleSubmit() {
		const raw = terminalInput.trim();
		if (raw === '') return;
		const inputForLog = terminalInput;
		terminalInput = '';

		// `ask <question>` routes to the real AI chat backend. Everything
		// else stays on the local command processor.
		const parts = raw.split(' ');
		const cmd = parts[0].toLowerCase();
		const rest = parts.slice(1).join(' ').trim();
		if (cmd === 'ask' && rest) {
			vm.submit(inputForLog);
			scrollToBottom();
			await dispatchAsk(rest);
			scrollToBottom();
			setTimeout(() => focusInput(), 10);
			return;
		}

		vm.submit(inputForLog);
		scrollToBottom();
		setTimeout(() => focusInput(), 10);
	}

	async function dispatchAsk(question: string) {
		if (isAsking) return;
		isAsking = true;
		try {
			if (!chatSessionId) {
				const session = await startChatSession();
				if (!session) {
					vm.history.update((h) => [
						...h,
						{ type: 'output', text: 'ChatBot: chat backend unavailable — VITE_BACKEND_API_URL missing or backend down.' }
					]);
					return;
				}
				chatSessionId = session.sessionId;
			}
			vm.history.update((h) => [
				...h,
				{ type: 'system', text: 'ChatBot: thinking…' }
			]);
			const reply = await sendChatMessage(chatSessionId, question);
			vm.history.update((h) => {
				// Drop the trailing "thinking…" line.
				const trimmed = h[h.length - 1]?.text === 'ChatBot: thinking…' ? h.slice(0, -1) : h;
				const text = reply?.content?.trim() || 'ChatBot: (no reply)';
				return [...trimmed, { type: 'output', text: `ChatBot: ${text}` }];
			});
		} finally {
			isAsking = false;
		}
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
			event.preventDefault();
			event.stopPropagation();
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
		{#each $terminalHistory as line}
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
			autocapitalize="off"
			autocorrect="off"
			spellcheck="false"
			type="text"
			name="terminal-command"
			data-form-type="other"
		/>
	</div>
</div>

<style>
	.terminal-container {
		min-height: 200px;
		background: #000 !important;
		color: #00ff00 !important;
	}
	.terminal-container :global(.text-retro-green) {
		color: #00ff00 !important;
	}
	.terminal-container :global(.text-retro-green-dark) {
		color: #00dd00 !important;
	}
	.terminal-container :global(.text-retro-green-darker) {
		color: #00aa00 !important;
	}
	.terminal-container :global(.border-retro-border) {
		border-color: #166534 !important;
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

