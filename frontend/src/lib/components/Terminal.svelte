<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { createTerminalViewModel } from '$lib/viewmodels/terminalViewModel.svelte';

	const vm = createTerminalViewModel();

	let inputValue = $state('');
	let completions = $state<string[]>([]);
	// Autocomplete defence: the field starts readonly so Chrome/Safari
	// won't fire their autofill heuristics on mount; focus flips it off
	// so typing works. Combined with the data-*ignore attrs below this
	// reliably kills the "save login / suggest password" popups that
	// plagued the old terminal input.
	let inputReadonly = $state(true);

	let scrollEl = $state<HTMLElement | null>(null);
	let inputEl = $state<HTMLInputElement | null>(null);
	let viEl = $state<HTMLElement | null>(null);
	let topEl = $state<HTMLElement | null>(null);

	// Auto-scroll the log whenever it grows.
	$effect(() => {
		void vm.lines.length;
		void tick().then(() => {
			if (scrollEl) scrollEl.scrollTop = scrollEl.scrollHeight;
		});
	});

	// Move focus to whichever surface is live.
	$effect(() => {
		const prog = vm.activeProgram;
		void tick().then(() => {
			if (prog === 'vi') viEl?.focus();
			else if (prog === 'top') topEl?.focus();
			else focusInput();
		});
	});

	// `top` refreshes on a timer while it's the active program.
	$effect(() => {
		if (vm.activeProgram !== 'top') return;
		const id = setInterval(() => vm.tickTop(), 1500);
		return () => clearInterval(id);
	});

	onMount(() => {
		setTimeout(focusInput, 150);
	});

	function focusInput() {
		inputEl?.focus();
	}

	function onShellKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			e.preventDefault();
			completions = [];
			vm.submit(inputValue);
			inputValue = '';
			return;
		}
		if (e.key === 'ArrowUp') {
			e.preventDefault();
			inputValue = vm.recallPrev(inputValue);
			moveCaretToEnd();
			return;
		}
		if (e.key === 'ArrowDown') {
			e.preventDefault();
			inputValue = vm.recallNext(inputValue);
			moveCaretToEnd();
			return;
		}
		if (e.key === 'Tab') {
			e.preventDefault();
			const r = vm.complete(inputValue);
			inputValue = r.line;
			completions = r.suggestions;
			moveCaretToEnd();
			return;
		}
		// any other key clears stale completion hints
		if (completions.length) completions = [];
	}

	function moveCaretToEnd() {
		void tick().then(() => {
			if (inputEl) {
				const n = inputEl.value.length;
				inputEl.setSelectionRange(n, n);
			}
		});
	}

	// ── vi key bridge ────────────────────────────────────────────────
	function onViKeydown(e: KeyboardEvent) {
		// Let browser shortcuts (copy/paste, devtools) through.
		if (e.metaKey || e.ctrlKey || e.altKey) return;
		const key = e.key;
		const handled = [
			'Enter',
			'Backspace',
			'Escape',
			'Tab',
			'ArrowUp',
			'ArrowDown',
			'ArrowLeft',
			'ArrowRight'
		];
		if (key.length === 1 || handled.includes(key)) {
			e.preventDefault();
			// vi has no Tab insert here; treat it as two spaces in insert.
			if (key === 'Tab') {
				vm.feedEditor(' ');
				vm.feedEditor(' ');
			} else {
				vm.feedEditor(key);
			}
		}
	}

	// ── top key bridge ───────────────────────────────────────────────
	function onTopKeydown(e: KeyboardEvent) {
		if (e.key === 'q' || e.key === 'Escape') {
			e.preventDefault();
			vm.quitTop();
		}
	}

	// Editor render helpers — split the cursor row so the block cursor
	// can be highlighted at the right column.
	function rowBefore(line: string, col: number): string {
		return line.slice(0, col);
	}
	function rowAt(line: string, col: number): string {
		return col < line.length ? line[col] : ' ';
	}
	function rowAfter(line: string, col: number): string {
		return col < line.length ? line.slice(col + 1) : '';
	}
</script>

<div class="term" role="application" aria-label="Linux terminal sandbox">
	{#if vm.activeProgram === 'vi' && vm.editor}
		<!-- vi full-screen editor -->
		<div
			class="vi"
			tabindex="0"
			role="textbox"
			aria-label="vi editor"
			aria-multiline="true"
			bind:this={viEl}
			onkeydown={onViKeydown}
		>
			{#key vm.programVersion}
			<div class="vi-body">
				{#each vm.editor.lines as line, i}
					<div class="vi-line">
						{#if i === vm.editor.row && vm.editor.mode !== 'command'}
							<span>{rowBefore(line, vm.editor.col)}</span><span class="vi-cursor"
								>{rowAt(line, vm.editor.col)}</span
							><span>{rowAfter(line, vm.editor.col)}</span>
						{:else}
							<span>{line === '' ? ' ' : line}</span>
						{/if}
					</div>
				{/each}
				{#each Array(Math.max(0, 18 - vm.editor.lines.length)) as _}
					<div class="vi-line vi-tilde">~</div>
				{/each}
			</div>
			<div class="vi-status">
				<span>{vm.editor.status || (vm.editor.mode === 'insert' ? '-- INSERT --' : '')}</span>
				<span class="vi-pos">{vm.editor.filename}  {vm.editor.row + 1},{vm.editor.col + 1}</span>
			</div>
			{/key}
		</div>
	{:else if vm.activeProgram === 'top' && vm.top}
		<!-- top live process view -->
		<div
			class="top"
			tabindex="0"
			role="textbox"
			aria-readonly="true"
			aria-label="top process viewer"
			bind:this={topEl}
			onkeydown={onTopKeydown}
		>
			{#key vm.programVersion}<pre class="top-pre">{vm.top.render()}</pre>{/key}
			<div class="top-hint">press <b>q</b> to quit</div>
		</div>
	{:else}
		<!-- interactive shell -->
		<div
			class="screen"
			bind:this={scrollEl}
			role="button"
			tabindex="0"
			aria-label="terminal output, click to focus"
			onclick={focusInput}
			onkeydown={(e) => {
				if (e.key === 'Enter') focusInput();
			}}
		>
			{#each vm.lines as line}
				<div class="line {line.type}">{line.text === '' ? ' ' : line.text}</div>
			{/each}
			{#if completions.length}
				<div class="line completions">{completions.join('   ')}</div>
			{/if}
			<div class="prompt-row">
				<span class="prompt">{vm.prompt}</span>
				<input
					class="cmd"
					bind:this={inputEl}
					bind:value={inputValue}
					onkeydown={onShellKeydown}
					onfocus={() => (inputReadonly = false)}
					readonly={inputReadonly}
					type="text"
					name="cyberdyne-shell-cmd"
					autocomplete="off"
					autocapitalize="off"
					autocorrect="off"
					spellcheck="false"
					aria-autocomplete="none"
					data-lpignore="true"
					data-1p-ignore
					data-form-type="other"
					inputmode="text"
				/>
			</div>
		</div>
	{/if}
</div>

<style>
	.term {
		height: 100%;
		min-height: 240px;
		background: #050805;
		color: #00ff66;
		font-family: 'Courier New', ui-monospace, 'SF Mono', Menlo, monospace;
		font-size: 14px;
		line-height: 1.45;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	/* ── shell ─────────────────────────────────────────────────────── */
	.screen {
		flex: 1;
		min-height: 0;
		overflow-y: auto;
		padding: 12px 14px;
		cursor: text;
		scrollbar-width: thin;
		scrollbar-color: #00aa44 #001a0a;
	}
	.line {
		white-space: pre-wrap;
		word-break: break-word;
	}
	.line.output {
		color: #00dd55;
	}
	.line.error {
		color: #ff5555;
	}
	.line.system {
		color: #00aa44;
	}
	.line.input {
		color: #9dffc0;
	}
	.line.completions {
		color: #66ffaa;
		opacity: 0.8;
	}
	.prompt-row {
		display: flex;
		align-items: baseline;
		gap: 8px;
	}
	.prompt {
		color: #57ff8f;
		white-space: nowrap;
		flex-shrink: 0;
	}
	.cmd {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		color: #eaffea;
		font: inherit;
		caret-color: #00ff66;
		padding: 0;
	}

	/* ── vi ────────────────────────────────────────────────────────── */
	.vi {
		flex: 1;
		display: flex;
		flex-direction: column;
		outline: none;
		min-height: 0;
	}
	.vi-body {
		flex: 1;
		overflow-y: auto;
		padding: 4px 8px;
	}
	.vi-line {
		white-space: pre-wrap;
		min-height: 1.45em;
	}
	.vi-tilde {
		color: #1c6b3a;
	}
	.vi-cursor {
		background: #00ff66;
		color: #050805;
	}
	.vi-status {
		display: flex;
		justify-content: space-between;
		background: #0c1f12;
		color: #b9ffce;
		padding: 2px 8px;
		border-top: 1px solid #123322;
	}
	.vi-pos {
		opacity: 0.8;
	}

	/* ── top ───────────────────────────────────────────────────────── */
	.top {
		flex: 1;
		display: flex;
		flex-direction: column;
		outline: none;
		min-height: 0;
	}
	.top-pre {
		flex: 1;
		margin: 0;
		padding: 8px 10px;
		overflow: auto;
		white-space: pre;
		color: #c9ffd9;
		font: inherit;
	}
	.top-hint {
		background: #0c1f12;
		color: #8fffb6;
		padding: 2px 8px;
		border-top: 1px solid #123;
	}

	@media (max-width: 480px) {
		.term {
			font-size: 12px;
		}
	}
</style>
