/**
 * Minimal shell-style argument splitting + flag parsing.
 *
 * Not a real shell parser — no pipes, redirects, globbing, or variable
 * expansion. Just enough to feel right for a teaching terminal: single
 * and double quotes group tokens, backslash escapes the next char.
 */

export function tokenize(line: string): string[] {
	const tokens: string[] = [];
	let current = '';
	let quote: '"' | "'" | null = null;
	let hasToken = false;

	for (let i = 0; i < line.length; i++) {
		const ch = line[i];

		if (quote) {
			if (ch === quote) {
				quote = null;
			} else if (ch === '\\' && quote === '"' && i + 1 < line.length) {
				current += line[++i];
			} else {
				current += ch;
			}
			continue;
		}

		if (ch === '"' || ch === "'") {
			quote = ch;
			hasToken = true;
			continue;
		}
		if (ch === '\\' && i + 1 < line.length) {
			current += line[++i];
			hasToken = true;
			continue;
		}
		if (ch === ' ' || ch === '\t') {
			if (hasToken) {
				tokens.push(current);
				current = '';
				hasToken = false;
			}
			continue;
		}
		current += ch;
		hasToken = true;
	}
	if (hasToken) tokens.push(current);
	return tokens;
}

export interface ParsedArgs {
	/** Single-letter flags, e.g. `-la` → {l:true, a:true}. */
	flags: Set<string>;
	/** Non-flag positional operands. */
	operands: string[];
}

/**
 * Split tokens into combined short flags + operands. Anything starting
 * with `-` (but not exactly `-` or `--`) is treated as a flag bundle;
 * `--` ends flag parsing. Long flags (`--name`) land in `flags` whole.
 */
export function parseArgs(tokens: string[]): ParsedArgs {
	const flags = new Set<string>();
	const operands: string[] = [];
	let flagsDone = false;

	for (const tok of tokens) {
		if (!flagsDone && tok === '--') {
			flagsDone = true;
			continue;
		}
		if (!flagsDone && tok.startsWith('--') && tok.length > 2) {
			flags.add(tok.slice(2));
			continue;
		}
		if (!flagsDone && tok.startsWith('-') && tok.length > 1) {
			for (const c of tok.slice(1)) flags.add(c);
			continue;
		}
		operands.push(tok);
	}
	return { flags, operands };
}
