/**
 * View-model for the Linux-course terminal sandbox.
 *
 * Owns the virtual filesystem, command dispatch, scrollback, command
 * history (↑/↓ recall), tab completion, and the two interactive
 * programs (vi/top). The Svelte component is a thin renderer over the
 * runed state exposed here.
 *
 * Persistence: the VFS + cwd + command history are mirrored to
 * sessionStorage so a refresh keeps the student's work within a visit,
 * but a new tab/session starts from the seed.
 */

import { tokenize } from '$lib/terminal/argv';
import {
	runCommandLine,
	listCommandNames,
	type CommandContext
} from '$lib/terminal/commands';
import { Vfs, isDir, isFile, displayPath, segmentsToPath, normalizePath } from '$lib/terminal/vfs';
import { seedFilesystem, HOME } from '$lib/terminal/seed';
import { ViEditor } from '$lib/terminal/vi';
import { TopModel } from '$lib/terminal/top';

const STORAGE_KEY = 'cyberdyne.shell.v1';
const USER = 'user';
const HOST = 'cyberdyne';
const MAX_SCROLLBACK = 2000;

export type LineType = 'input' | 'output' | 'error' | 'system';

export interface ScrollLine {
	type: LineType;
	text: string;
}

export type ActiveProgram = 'vi' | 'top' | null;

export interface CompletionResult {
	line: string;
	suggestions: string[];
}

export interface TerminalViewModel {
	readonly lines: ScrollLine[];
	readonly cwd: string;
	readonly prompt: string;
	readonly user: string;
	readonly host: string;
	readonly activeProgram: ActiveProgram;
	readonly editor: ViEditor | null;
	readonly top: TopModel | null;
	/** Bumps on every vi keystroke / top tick so views re-render the
	 *  mutated (non-proxied) program instances. */
	readonly programVersion: number;
	submit(line: string): void;
	recallPrev(current: string): string;
	recallNext(current: string): string;
	complete(line: string): CompletionResult;
	feedEditor(key: string): void;
	tickTop(): void;
	quitTop(): void;
	reset(): void;
}

function loadVfs(): { vfs: Vfs; cwd: string; cmds: string[] } {
	const fallback = { vfs: seedFilesystem(), cwd: HOME, cmds: [] as string[] };
	try {
		const raw = sessionStorage.getItem(STORAGE_KEY);
		if (!raw) return fallback;
		const parsed = JSON.parse(raw) as { fs?: string; cwd?: string; cmds?: string[] };
		if (!parsed.fs) return fallback;
		const vfs = Vfs.fromJSON(parsed.fs);
		// Validate the restored cwd still exists; fall back home if not.
		const cwd = parsed.cwd && isDir(vfs.resolve(parsed.cwd, '/')) ? parsed.cwd : HOME;
		return { vfs, cwd, cmds: parsed.cmds ?? [] };
	} catch {
		return fallback;
	}
}

export function createTerminalViewModel(): TerminalViewModel {
	const restored = loadVfs();
	let vfs = restored.vfs;

	let lines = $state<ScrollLine[]>(bootBanner());
	let cwd = $state<string>(restored.cwd);
	let activeProgram = $state<ActiveProgram>(null);
	let editor = $state<ViEditor | null>(null);
	let top = $state<TopModel | null>(null);
	// ViEditor / TopModel are plain classes (not $state proxies), so
	// in-place mutations don't trigger reactivity. Bump this on each
	// keystroke/tick and have the view read it to force a re-render.
	let programVersion = $state<number>(0);

	// Command history is plain (non-runed) state — only the recall
	// helpers read it, and they return strings the view binds to.
	const cmdHistory: string[] = [...restored.cmds];
	let historyCursor = cmdHistory.length;
	// Path captured when vi launched, so :w writes to the right place
	// even if the user somehow changes cwd mid-edit (they can't, but
	// it keeps the write self-contained).
	let editorPath = '';
	let editorCwd = HOME;

	const env: Record<string, string> = {
		HOME,
		USER,
		PATH: '/usr/local/bin:/usr/bin:/bin',
		SHELL: '/bin/sh',
		TERM: 'xterm-256color',
		PWD: restored.cwd
	};

	function persist() {
		try {
			sessionStorage.setItem(
				STORAGE_KEY,
				JSON.stringify({ fs: vfs.toJSON(), cwd, cmds: cmdHistory.slice(-200) })
			);
		} catch {
			/* storage unavailable — sandbox still works, just no persistence */
		}
	}

	function push(line: ScrollLine) {
		lines.push(line);
		if (lines.length > MAX_SCROLLBACK) lines = lines.slice(-MAX_SCROLLBACK);
	}

	function pushText(type: LineType, text: string) {
		if (text === '') return;
		for (const t of text.split('\n')) push({ type, text: t });
	}

	function promptString(): string {
		return `${USER}@${HOST}:${displayPath(cwd, HOME)}$`;
	}

	function submit(raw: string) {
		const line = raw.replace(/\n$/, '');
		// Always echo the prompt + command, even for blanks (real shells do).
		push({ type: 'input', text: `${promptString()} ${line}` });

		const trimmed = line.trim();
		if (trimmed !== '') {
			if (cmdHistory[cmdHistory.length - 1] !== trimmed) cmdHistory.push(trimmed);
			historyCursor = cmdHistory.length;
		} else {
			return;
		}

		const ctx: CommandContext = {
			vfs,
			cwd,
			env: { ...env, PWD: cwd },
			user: USER,
			host: HOST,
			history: cmdHistory
		};
		const result = runCommandLine(line, ctx);

		if (result.clear) {
			lines = [];
			persist();
			return;
		}
		if (result.launch) {
			launch(result.launch.program, result.launch.args);
			persist();
			return;
		}
		pushText('output', result.stdout ?? '');
		pushText('error', result.stderr ?? '');
		if (result.cwd) {
			cwd = result.cwd;
			env.PWD = cwd;
		}
		persist();
	}

	function launch(program: 'vi' | 'top', args: string[]) {
		if (program === 'vi') {
			const target = args[0];
			let content = '';
			if (target) {
				const node = vfs.resolve(target, cwd);
				if (node && isDir(node)) {
					pushText('error', `vi: ${target}: Is a directory`);
					return;
				}
				if (isFile(node)) content = node.content;
				editorPath = target;
			} else {
				editorPath = '';
			}
			editorCwd = cwd;
			editor = new ViEditor(editorPath || '[No Name]', content);
			activeProgram = 'vi';
			return;
		}
		// top
		top = new TopModel();
		activeProgram = 'top';
	}

	function feedEditor(key: string) {
		if (!editor) return;
		const action = editor.feed(key);
		programVersion++;
		if (!action) return;
		if (action.kind === 'write' || action.kind === 'write-quit') {
			if (editorPath) {
				try {
					vfs.writeFile(editorPath, editor.text(), editorCwd);
					persist();
				} catch (e) {
					editor.status = `E212: Can't open file for writing (${(e as Error).message})`;
				}
			} else {
				editor.status = 'E32: No file name';
				if (action.kind === 'write') return;
			}
		}
		if (action.kind === 'quit' || action.kind === 'write-quit') {
			closeEditor();
		}
	}

	function closeEditor() {
		const name = editor?.filename;
		editor = null;
		activeProgram = null;
		if (name) push({ type: 'system', text: promptString() + ' vi ' + name });
	}

	function tickTop() {
		if (!top) return;
		top.tick();
		programVersion++;
	}

	function quitTop() {
		top = null;
		activeProgram = null;
	}

	function recallPrev(current: string): string {
		if (cmdHistory.length === 0) return current;
		if (historyCursor > 0) historyCursor -= 1;
		return cmdHistory[historyCursor] ?? current;
	}

	function recallNext(current: string): string {
		if (historyCursor < cmdHistory.length) historyCursor += 1;
		return historyCursor >= cmdHistory.length ? '' : cmdHistory[historyCursor];
	}

	function complete(line: string): CompletionResult {
		const trailingSpace = /\s$/.test(line);
		const tokens = tokenize(line);
		// Completing the command name: first token, no trailing space.
		if (tokens.length <= 1 && !trailingSpace) {
			const prefix = tokens[0] ?? '';
			const matches = listCommandNames().filter((c) => c.startsWith(prefix));
			return applyMatches(line, prefix, matches, false);
		}
		// Completing a path operand.
		const partial = trailingSpace ? '' : tokens[tokens.length - 1];
		const slash = partial.lastIndexOf('/');
		const dirPart = slash >= 0 ? partial.slice(0, slash + 1) : '';
		const basePart = slash >= 0 ? partial.slice(slash + 1) : partial;
		const dirPath = dirPart === '' ? cwd : dirPart;
		const dirNode = vfs.resolve(dirPath, cwd);
		if (!dirNode || !isDir(dirNode)) return { line, suggestions: [] };
		const entries = vfs.list(dirPath, cwd);
		const matched = entries
			.filter((n) => n.name.startsWith(basePart))
			.map((n) => (isDir(n) ? n.name + '/' : n.name));
		return applyMatches(line, basePart, matched, true, dirPart);
	}

	function applyMatches(
		line: string,
		prefix: string,
		matches: string[],
		isPath: boolean,
		dirPart = ''
	): CompletionResult {
		if (matches.length === 0) return { line, suggestions: [] };
		if (matches.length === 1) {
			const completion = matches[0];
			const base = line.slice(0, line.length - prefix.length);
			// For non-path command completion, add a trailing space.
			const suffix = isPath ? '' : ' ';
			return { line: base + (isPath ? dirPart + completion : completion) + suffix, suggestions: [] };
		}
		// Multiple: extend to the longest common prefix, list the options.
		const lcp = longestCommonPrefix(matches.map((m) => m.replace(/\/$/, '')));
		if (lcp.length > prefix.length) {
			const base = line.slice(0, line.length - prefix.length);
			return { line: base + dirPart + lcp, suggestions: matches };
		}
		return { line, suggestions: matches };
	}

	function reset() {
		vfs = seedFilesystem();
		cwd = HOME;
		env.PWD = HOME;
		lines = bootBanner();
		cmdHistory.length = 0;
		historyCursor = 0;
		activeProgram = null;
		editor = null;
		top = null;
		try {
			sessionStorage.removeItem(STORAGE_KEY);
		} catch {
			/* ignore */
		}
	}

	return {
		get lines() {
			return lines;
		},
		get cwd() {
			return cwd;
		},
		get prompt() {
			return promptString();
		},
		get user() {
			return USER;
		},
		get host() {
			return HOST;
		},
		get activeProgram() {
			return activeProgram;
		},
		get editor() {
			return editor;
		},
		get top() {
			return top;
		},
		get programVersion() {
			return programVersion;
		},
		submit,
		recallPrev,
		recallNext,
		complete,
		feedEditor,
		tickTop,
		quitTop,
		reset
	};
}

function bootBanner(): ScrollLine[] {
	return [
		{ type: 'system', text: 'CyberdyneOS 1.0 (Skynet)  —  sandboxed Linux shell' },
		{ type: 'system', text: "Type 'help' for commands, or 'cat readme.txt' to get started." },
		{ type: 'system', text: '' }
	];
}

function longestCommonPrefix(strings: string[]): string {
	if (strings.length === 0) return '';
	let prefix = strings[0];
	for (const s of strings) {
		while (!s.startsWith(prefix)) {
			prefix = prefix.slice(0, -1);
			if (prefix === '') return '';
		}
	}
	return prefix;
}

// Re-exported for the component's path display.
export { segmentsToPath, normalizePath };
