/**
 * Command registry for the Linux-course terminal.
 *
 * Each command is a pure function over a CommandContext: it may mutate
 * the VFS, and it returns a CommandResult the view-model applies
 * (text output, a new cwd, a screen clear, or a request to launch an
 * interactive program like vi/top). No I/O, no async — everything is
 * deterministic so the whole surface is unit-testable.
 */

import { tokenize, parseArgs, type ParsedArgs } from './argv';
import {
	Vfs,
	VfsError,
	isDir,
	isFile,
	normalizePath,
	segmentsToPath,
	displayPath,
	type VfsNode
} from './vfs';

export interface CommandContext {
	vfs: Vfs;
	cwd: string;
	env: Record<string, string>;
	user: string;
	host: string;
	history: string[];
}

export interface LaunchRequest {
	program: 'vi' | 'top';
	args: string[];
}

export interface CommandResult {
	stdout?: string;
	stderr?: string;
	cwd?: string;
	clear?: boolean;
	launch?: LaunchRequest;
}

type CommandFn = (ctx: CommandContext, args: ParsedArgs, tokens: string[]) => CommandResult;

interface CommandSpec {
	name: string;
	summary: string;
	usage: string;
	run: CommandFn;
}

// ── helpers ──────────────────────────────────────────────────────────

function err(name: string, msg: string): CommandResult {
	return { stderr: `${name}: ${msg}` };
}

function globToRegExp(glob: string, caseInsensitive = false): RegExp {
	const escaped = glob.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*').replace(/\?/g, '.');
	return new RegExp(`^${escaped}$`, caseInsensitive ? 'i' : '');
}

/** Depth-first walk yielding [absolutePath, node] for a subtree. */
function walk(vfs: Vfs, startAbs: string): Array<{ path: string; node: VfsNode }> {
	const out: Array<{ path: string; node: VfsNode }> = [];
	const startNode = vfs.resolve(startAbs, '/');
	if (!startNode) return out;
	const stack: Array<{ path: string; node: VfsNode }> = [{ path: startAbs, node: startNode }];
	while (stack.length) {
		const item = stack.pop()!;
		out.push(item);
		if (isDir(item.node)) {
			const kids = Object.values(item.node.children).sort((a, b) => a.name.localeCompare(b.name));
			// push reversed so traversal stays alphabetical
			for (let i = kids.length - 1; i >= 0; i--) {
				const child = kids[i];
				const childPath = item.path === '/' ? `/${child.name}` : `${item.path}/${child.name}`;
				stack.push({ path: childPath, node: child });
			}
		}
	}
	return out;
}

function absOf(path: string, ctx: CommandContext): string {
	return segmentsToPath(normalizePath(path, ctx.cwd, ctx.vfs.home));
}

function fmtLong(node: VfsNode): string {
	const size = isFile(node) ? node.content.length : 4096;
	const d = new Date(node.mtime);
	const month = d.toLocaleString('en-US', { month: 'short' });
	const day = String(d.getDate()).padStart(2, ' ');
	const hh = String(d.getHours()).padStart(2, '0');
	const mm = String(d.getMinutes()).padStart(2, '0');
	const nlink = isDir(node) ? 2 : 1;
	return `${node.mode} ${nlink} user user ${String(size).padStart(6, ' ')} ${month} ${day} ${hh}:${mm} ${node.name}`;
}

// ── commands ─────────────────────────────────────────────────────────

const SPECS: CommandSpec[] = [
	{
		name: 'ls',
		summary: 'list directory contents',
		usage: 'ls [-l] [-a] [-1] [path...]',
		run: (ctx, { flags, operands }) => {
			const targets = operands.slice(1);
			const paths = targets.length ? targets : ['.'];
			const long = flags.has('l');
			const all = flags.has('a');
			const onePer = flags.has('1') || long;
			const blocks: string[] = [];
			let hadError = false;
			for (const p of paths) {
				const node = ctx.vfs.resolve(p, ctx.cwd);
				if (!node) {
					blocks.push(`ls: cannot access '${p}': No such file or directory`);
					hadError = true;
					continue;
				}
				let entries: VfsNode[];
				let header = '';
				if (isFile(node)) {
					entries = [node];
				} else {
					entries = ctx.vfs.list(p, ctx.cwd);
					if (paths.length > 1) header = `${p}:`;
				}
				let names = entries.map((n) => n);
				if (all && isDir(node)) {
					// Synthesize . and .. for realism (cosmetic).
					names = [
						{ ...node, name: '.' },
						{ ...node, name: '..' },
						...names
					];
				}
				const rendered = long
					? names.map(fmtLong).join('\n')
					: names.map((n) => n.name).join(onePer ? '\n' : '  ');
				blocks.push(header ? `${header}\n${rendered}` : rendered);
			}
			const text = blocks.join('\n\n');
			return hadError ? { stderr: text } : { stdout: text };
		}
	},
	{
		name: 'cd',
		summary: 'change the working directory',
		usage: 'cd [path]',
		run: (ctx, { operands }) => {
			const target = operands[1] ?? '~';
			const node = ctx.vfs.resolve(target, ctx.cwd);
			if (!node) return err('cd', `${target}: No such file or directory`);
			if (!isDir(node)) return err('cd', `${target}: Not a directory`);
			return { cwd: absOf(target, ctx) };
		}
	},
	{
		name: 'pwd',
		summary: 'print working directory',
		usage: 'pwd',
		run: (ctx) => ({ stdout: ctx.cwd })
	},
	{
		name: 'cat',
		summary: 'concatenate and print files',
		usage: 'cat [file...]',
		run: (ctx, { operands }) => {
			const files = operands.slice(1);
			if (!files.length) return err('cat', 'missing file operand');
			const out: string[] = [];
			let hadError = false;
			for (const f of files) {
				const node = ctx.vfs.resolve(f, ctx.cwd);
				if (!node) {
					out.push(`cat: ${f}: No such file or directory`);
					hadError = true;
				} else if (isDir(node)) {
					out.push(`cat: ${f}: Is a directory`);
					hadError = true;
				} else {
					out.push(node.content.replace(/\n$/, ''));
				}
			}
			const text = out.join('\n');
			return hadError ? { stderr: text } : { stdout: text };
		}
	},
	{
		name: 'echo',
		summary: 'display a line of text',
		usage: 'echo [text...]',
		run: (_ctx, { operands }) => ({ stdout: operands.slice(1).join(' ') })
	},
	{
		name: 'mkdir',
		summary: 'make directories',
		usage: 'mkdir [-p] dir...',
		run: (ctx, { flags, operands }) => {
			const dirs = operands.slice(1);
			if (!dirs.length) return err('mkdir', 'missing operand');
			const errors: string[] = [];
			for (const d of dirs) {
				try {
					ctx.vfs.mkdir(d, ctx.cwd, flags.has('p'));
				} catch (e) {
					errors.push(`mkdir: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'rmdir',
		summary: 'remove empty directories',
		usage: 'rmdir dir...',
		run: (ctx, { operands }) => {
			const dirs = operands.slice(1);
			if (!dirs.length) return err('rmdir', 'missing operand');
			const errors: string[] = [];
			for (const d of dirs) {
				try {
					ctx.vfs.rmdir(d, ctx.cwd);
				} catch (e) {
					errors.push(`rmdir: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'rm',
		summary: 'remove files or directories',
		usage: 'rm [-r] [-f] path...',
		run: (ctx, { flags, operands }) => {
			const paths = operands.slice(1);
			const force = flags.has('f');
			if (!paths.length) return force ? {} : err('rm', 'missing operand');
			const recursive = flags.has('r') || flags.has('R');
			const errors: string[] = [];
			for (const p of paths) {
				try {
					ctx.vfs.rm(p, ctx.cwd, recursive);
				} catch (e) {
					if (!force) errors.push(`rm: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'touch',
		summary: 'create empty files / update timestamps',
		usage: 'touch file...',
		run: (ctx, { operands }) => {
			const files = operands.slice(1);
			if (!files.length) return err('touch', 'missing file operand');
			const errors: string[] = [];
			for (const f of files) {
				try {
					ctx.vfs.touch(f, ctx.cwd);
				} catch (e) {
					errors.push(`touch: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'mv',
		summary: 'move (rename) files',
		usage: 'mv src dest',
		run: (ctx, { operands }) => {
			const rest = operands.slice(1);
			if (rest.length < 2) return err('mv', 'missing destination file operand');
			const dest = rest[rest.length - 1];
			const sources = rest.slice(0, -1);
			const errors: string[] = [];
			for (const s of sources) {
				try {
					ctx.vfs.mv(s, dest, ctx.cwd);
				} catch (e) {
					errors.push(`mv: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'cp',
		summary: 'copy files and directories',
		usage: 'cp [-r] src dest',
		run: (ctx, { flags, operands }) => {
			const rest = operands.slice(1);
			if (rest.length < 2) return err('cp', 'missing destination file operand');
			const recursive = flags.has('r') || flags.has('R');
			const dest = rest[rest.length - 1];
			const sources = rest.slice(0, -1);
			const errors: string[] = [];
			for (const s of sources) {
				try {
					ctx.vfs.cp(s, dest, ctx.cwd, recursive);
				} catch (e) {
					errors.push(`cp: ${(e as VfsError).message}`);
				}
			}
			return errors.length ? { stderr: errors.join('\n') } : {};
		}
	},
	{
		name: 'find',
		summary: 'search for files in a directory hierarchy',
		usage: "find [path] [-name pattern] [-type f|d]",
		run: (ctx, _parsed, tokens) => {
			// find has its own mini-syntax (predicates like -name take a
			// value), so parse the raw tokens rather than the generic
			// flag/operand split.
			const rest = tokens.slice(1);
			let start = '.';
			let namePat: RegExp | null = null;
			let typeFilter: 'f' | 'd' | null = null;
			const positional: string[] = [];
			for (let i = 0; i < rest.length; i++) {
				const tok = rest[i];
				if (tok === '-name') {
					namePat = globToRegExp(rest[++i] ?? '');
				} else if (tok === '-iname') {
					namePat = globToRegExp(rest[++i] ?? '', true);
				} else if (tok === '-type') {
					const t = rest[++i];
					typeFilter = t === 'd' ? 'd' : t === 'f' ? 'f' : null;
				} else {
					positional.push(tok);
				}
			}
			if (positional.length) start = positional[0];
			const startAbs = absOf(start, ctx);
			if (!ctx.vfs.resolve(startAbs, '/')) {
				return err('find', `'${start}': No such file or directory`);
			}
			const lines: string[] = [];
			for (const { path, node } of walk(ctx.vfs, startAbs)) {
				if (typeFilter === 'f' && !isFile(node)) continue;
				if (typeFilter === 'd' && !isDir(node)) continue;
				if (namePat && !namePat.test(node.name)) continue;
				// Print relative to the start arg the way real find does.
				const rel =
					start === '.'
						? path === startAbs
							? '.'
							: '.' + path.slice(startAbs.length)
						: path;
				lines.push(rel);
			}
			return { stdout: lines.join('\n') };
		}
	},
	{
		name: 'grep',
		summary: 'print lines matching a pattern',
		usage: 'grep [-i] [-n] [-r] pattern [file...]',
		run: (ctx, { flags, operands }) => {
			const rest = operands.slice(1);
			if (!rest.length) return err('grep', 'missing pattern');
			const pattern = rest[0];
			const files = rest.slice(1);
			const ci = flags.has('i');
			const showNum = flags.has('n');
			const recursive = flags.has('r') || flags.has('R');
			const needle = ci ? pattern.toLowerCase() : pattern;
			const targets = files.length ? files : ['.'];

			interface Hit {
				path: string;
				line: number;
				text: string;
			}
			const hits: Hit[] = [];
			const errors: string[] = [];
			let scannedMultiple = files.length > 1 || recursive;

			const scanFile = (absPath: string, label: string) => {
				const content = ctx.vfs.resolve(absPath, '/');
				if (!isFile(content)) return;
				content.content.split('\n').forEach((raw, idx) => {
					const hay = ci ? raw.toLowerCase() : raw;
					if (hay.includes(needle)) hits.push({ path: label, line: idx + 1, text: raw });
				});
			};

			for (const t of targets) {
				const abs = absOf(t, ctx);
				const node = ctx.vfs.resolve(abs, '/');
				if (!node) {
					errors.push(`grep: ${t}: No such file or directory`);
					continue;
				}
				if (isDir(node)) {
					if (!recursive) {
						errors.push(`grep: ${t}: Is a directory`);
						continue;
					}
					scannedMultiple = true;
					for (const entry of walk(ctx.vfs, abs)) {
						if (isFile(entry.node)) {
							const label =
								t === '.' ? '.' + entry.path.slice(abs.length) : entry.path;
							scanFile(entry.path, label.replace(/^\.\//, './') || entry.path);
						}
					}
				} else {
					scanFile(abs, t);
				}
			}

			const lines = hits.map((h) => {
				const parts: string[] = [];
				if (scannedMultiple) parts.push(h.path);
				if (showNum) parts.push(String(h.line));
				parts.push(h.text);
				return parts.join(':');
			});
			if (errors.length && !lines.length) return { stderr: errors.join('\n') };
			const text = [...lines, ...errors].join('\n');
			return errors.length ? { stderr: text } : { stdout: text };
		}
	},
	{
		name: 'head',
		summary: 'output the first part of files',
		usage: 'head [-n N] file...',
		run: (ctx, _parsed, tokens) => headTail(ctx, tokens, 'head')
	},
	{
		name: 'tail',
		summary: 'output the last part of files',
		usage: 'tail [-n N] file...',
		run: (ctx, _parsed, tokens) => headTail(ctx, tokens, 'tail')
	},
	{
		name: 'wc',
		summary: 'count lines, words and bytes',
		usage: 'wc [-l] [-w] [-c] file...',
		run: (ctx, { flags, operands }) => {
			const files = operands.slice(1);
			if (!files.length) return err('wc', 'missing file operand');
			const showL = flags.has('l');
			const showW = flags.has('w');
			const showC = flags.has('c');
			const showAll = !showL && !showW && !showC;
			const lines: string[] = [];
			const errors: string[] = [];
			for (const f of files) {
				const node = ctx.vfs.resolve(f, ctx.cwd);
				if (!isFile(node)) {
					errors.push(`wc: ${f}: No such file or directory`);
					continue;
				}
				const content = node.content;
				const lc = content === '' ? 0 : content.split('\n').length - (content.endsWith('\n') ? 1 : 0);
				const wc = content.trim() === '' ? 0 : content.trim().split(/\s+/).length;
				const cc = content.length;
				const cols: number[] = [];
				if (showAll || showL) cols.push(lc);
				if (showAll || showW) cols.push(wc);
				if (showAll || showC) cols.push(cc);
				lines.push(`${cols.map((n) => String(n).padStart(7, ' ')).join('')} ${f}`);
			}
			const text = [...lines, ...errors].join('\n');
			return errors.length ? { stderr: text } : { stdout: text };
		}
	},
	{
		name: 'tree',
		summary: 'list contents of directories in a tree-like format',
		usage: 'tree [path]',
		run: (ctx, { operands }) => {
			const start = operands[1] ?? '.';
			const node = ctx.vfs.resolve(start, ctx.cwd);
			if (!node) return err('tree', `${start}: No such file or directory`);
			const out: string[] = [start];
			let dirs = 0;
			let files = 0;
			const render = (dir: VfsNode, prefix: string) => {
				if (!isDir(dir)) return;
				const kids = Object.values(dir.children).sort((a, b) => a.name.localeCompare(b.name));
				kids.forEach((child, i) => {
					const last = i === kids.length - 1;
					out.push(`${prefix}${last ? '└── ' : '├── '}${child.name}`);
					if (isDir(child)) {
						dirs++;
						render(child, prefix + (last ? '    ' : '│   '));
					} else {
						files++;
					}
				});
			};
			render(node, '');
			out.push('');
			out.push(`${dirs} ${dirs === 1 ? 'directory' : 'directories'}, ${files} ${files === 1 ? 'file' : 'files'}`);
			return { stdout: out.join('\n') };
		}
	},
	{
		name: 'whoami',
		summary: 'print the current user',
		usage: 'whoami',
		run: (ctx) => ({ stdout: ctx.user })
	},
	{
		name: 'hostname',
		summary: 'print the system hostname',
		usage: 'hostname',
		run: (ctx) => ({ stdout: ctx.host })
	},
	{
		name: 'uname',
		summary: 'print system information',
		usage: 'uname [-a]',
		run: (ctx, { flags }) => ({
			stdout: flags.has('a')
				? `CyberdyneOS ${ctx.host} 1.0-skynet #1 SMP x86_64 GNU/Linux`
				: 'CyberdyneOS'
		})
	},
	{
		name: 'date',
		summary: 'print the system date and time',
		usage: 'date',
		run: () => ({ stdout: new Date().toString() })
	},
	{
		name: 'env',
		summary: 'print environment variables',
		usage: 'env',
		run: (ctx) => ({
			stdout: Object.entries(ctx.env)
				.map(([k, v]) => `${k}=${v}`)
				.join('\n')
		})
	},
	{
		name: 'history',
		summary: 'show command history',
		usage: 'history',
		run: (ctx) => ({
			stdout: ctx.history.map((h, i) => `${String(i + 1).padStart(4, ' ')}  ${h}`).join('\n')
		})
	},
	{
		name: 'clear',
		summary: 'clear the terminal screen',
		usage: 'clear',
		run: () => ({ clear: true })
	},
	{
		name: 'vi',
		summary: 'a modal text editor',
		usage: 'vi [file]',
		run: (_ctx, { operands }) => ({ launch: { program: 'vi', args: operands.slice(1) } })
	},
	{
		name: 'vim',
		summary: 'a modal text editor (alias of vi)',
		usage: 'vim [file]',
		run: (_ctx, { operands }) => ({ launch: { program: 'vi', args: operands.slice(1) } })
	},
	{
		name: 'top',
		summary: 'display running processes',
		usage: 'top',
		run: () => ({ launch: { program: 'top', args: [] } })
	}
];

function headTail(ctx: CommandContext, tokens: string[], mode: 'head' | 'tail'): CommandResult {
	// Parse raw tokens: -n N (split), -nN (bundled), or -N (count).
	let n = 10;
	const rest = tokens.slice(1);
	const files: string[] = [];
	for (let i = 0; i < rest.length; i++) {
		const tok = rest[i];
		if (tok === '-n') {
			const parsed = parseInt(rest[++i] ?? '', 10);
			if (!Number.isNaN(parsed)) n = parsed;
		} else if (/^-n\d+$/.test(tok)) {
			n = parseInt(tok.slice(2), 10);
		} else if (/^-\d+$/.test(tok)) {
			n = parseInt(tok.slice(1), 10);
		} else {
			files.push(tok);
		}
	}
	if (!files.length) return err(mode, 'missing file operand');
	const out: string[] = [];
	const errors: string[] = [];
	for (const f of files) {
		const node = ctx.vfs.resolve(f, ctx.cwd);
		if (!isFile(node)) {
			errors.push(`${mode}: cannot open '${f}' for reading: No such file or directory`);
			continue;
		}
		const allLines = node.content.replace(/\n$/, '').split('\n');
		const slice = mode === 'head' ? allLines.slice(0, n) : allLines.slice(-n);
		if (files.length > 1) out.push(`==> ${f} <==`);
		out.push(slice.join('\n'));
	}
	const text = [...out, ...errors].join('\n');
	return errors.length ? { stderr: text } : { stdout: text };
}

const REGISTRY: Record<string, CommandSpec> = Object.fromEntries(SPECS.map((s) => [s.name, s]));

// `help` and `man` need the registry, so define them after it exists.
REGISTRY['help'] = {
	name: 'help',
	summary: 'list available commands',
	usage: 'help',
	run: () => {
		const names = Object.values(REGISTRY)
			.map((s) => s.name)
			.sort();
		const width = Math.max(...names.map((n) => n.length));
		const lines = names.map((n) => `  ${n.padEnd(width)}  ${REGISTRY[n].summary}`);
		return {
			stdout: `CyberdyneOS shell — available commands:\n${lines.join('\n')}\n\nType 'man <command>' for usage.`
		};
	}
};

REGISTRY['man'] = {
	name: 'man',
	summary: 'show a command manual entry',
	usage: 'man <command>',
	run: (_ctx, { operands }) => {
		const cmd = operands[1];
		if (!cmd) return err('man', 'what manual page do you want?');
		const spec = REGISTRY[cmd];
		if (!spec) return { stderr: `No manual entry for ${cmd}` };
		return {
			stdout: `NAME\n    ${spec.name} — ${spec.summary}\n\nSYNOPSIS\n    ${spec.usage}`
		};
	}
};

export function listCommandNames(): string[] {
	return Object.keys(REGISTRY).sort();
}

/**
 * Parse and execute a single command line. Returns the command result;
 * the view-model is responsible for applying cwd/clear and rendering
 * stdout/stderr. Empty input yields an empty result.
 */
export function runCommandLine(line: string, ctx: CommandContext): CommandResult {
	const tokens = tokenize(line);
	if (!tokens.length) return {};
	const name = tokens[0];
	const spec = REGISTRY[name];
	if (!spec) {
		return { stderr: `${name}: command not found` };
	}
	const parsed = parseArgs(tokens);
	// parseArgs keeps the command name as operands[0]; each command
	// slices from there. find/head/tail also get the raw tokens for
	// their value-taking predicates.
	return spec.run(ctx, parsed, tokens);
}

export { REGISTRY as _registry };
export type { CommandSpec };
export { Vfs, displayPath };
