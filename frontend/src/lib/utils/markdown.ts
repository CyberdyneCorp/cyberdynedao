/**
 * A tiny, dependency-free Markdown parser for the agent's prose. It covers
 * exactly what the chat model emits — headings, bullet/numbered lists, bold,
 * italic, inline code, links, and inline math (`\( … \)`) — and renders to a
 * small node tree the Svelte view walks with escaped text (no `{@html}`), so
 * it stays XSS-safe. Fenced code, Mermaid, and display math are split out
 * earlier by `parseSegments`; this only handles the leftover prose.
 */

export type Inline =
	| { kind: 'text'; text: string }
	| { kind: 'bold'; text: string }
	| { kind: 'italic'; text: string }
	| { kind: 'code'; text: string }
	| { kind: 'link'; text: string; href: string }
	| { kind: 'math'; code: string };

export type Block =
	| { kind: 'heading'; level: number; text: string }
	| { kind: 'list'; ordered: boolean; items: string[] }
	| { kind: 'paragraph'; text: string };

const HEADING = /^(#{1,6})\s+(.*)$/;
const UL_ITEM = /^[-*+]\s+(.*)$/;
const OL_ITEM = /^\d+[.)]\s+(.*)$/;

export function parseBlocks(src: string): Block[] {
	const blocks: Block[] = [];
	let para: string[] = [];
	let list: { ordered: boolean; items: string[] } | null = null;

	const flushPara = () => {
		if (para.length) {
			blocks.push({ kind: 'paragraph', text: para.join(' ').trim() });
			para = [];
		}
	};
	const flushList = () => {
		if (list) {
			blocks.push({ kind: 'list', ordered: list.ordered, items: list.items });
			list = null;
		}
	};

	for (const raw of src.split('\n')) {
		const line = raw.trim();
		if (line === '') {
			flushPara();
			flushList();
			continue;
		}
		const heading = HEADING.exec(line);
		if (heading) {
			flushPara();
			flushList();
			blocks.push({ kind: 'heading', level: heading[1].length, text: heading[2] });
			continue;
		}
		const ul = UL_ITEM.exec(line);
		if (ul) {
			flushPara();
			if (list && !list.ordered) list.items.push(ul[1]);
			else {
				flushList();
				list = { ordered: false, items: [ul[1]] };
			}
			continue;
		}
		const ol = OL_ITEM.exec(line);
		if (ol) {
			flushPara();
			if (list && list.ordered) list.items.push(ol[1]);
			else {
				flushList();
				list = { ordered: true, items: [ol[1]] };
			}
			continue;
		}
		flushList();
		para.push(line);
	}
	flushPara();
	flushList();
	return blocks;
}

interface Hit {
	index: number;
	len: number;
	run: Inline;
}

function safeHref(href: string): boolean {
	return /^(https?:|mailto:)/i.test(href.trim());
}

function earliestToken(s: string): Hit | null {
	const hits: Hit[] = [];
	const add = (m: RegExpExecArray | null, run: (m: RegExpExecArray) => Inline) => {
		if (m) hits.push({ index: m.index, len: m[0].length, run: run(m) });
	};
	add(/`([^`]+)`/.exec(s), (m) => ({ kind: 'code', text: m[1] }));
	add(/\*\*([^*]+?)\*\*/.exec(s), (m) => ({ kind: 'bold', text: m[1] }));
	add(/__([^_]+?)__/.exec(s), (m) => ({ kind: 'bold', text: m[1] }));
	add(/\\\(([\s\S]+?)\\\)/.exec(s), (m) => ({ kind: 'math', code: m[1].trim() }));
	add(/\[([^\]]+)\]\(([^)\s]+)\)/.exec(s), (m) => ({ kind: 'link', text: m[1], href: m[2] }));
	// Italic: delimiter must hug non-space text, so "5 * 3" isn't matched.
	add(/\*(\S[^*\n]*?)\*/.exec(s), (m) => ({ kind: 'italic', text: m[1] }));
	add(/(?:^|\s)_(\S[^_\n]*?)_(?=\s|$)/.exec(s), (m) => ({
		kind: 'italic',
		text: m[1]
	}));
	if (!hits.length) return null;
	// Earliest match wins; on a tie the longer token wins (** beats *).
	hits.sort((a, b) => a.index - b.index || b.len - a.len);
	return hits[0];
}

export function parseInline(text: string): Inline[] {
	const runs: Inline[] = [];
	let rest = text;
	while (rest) {
		const hit = earliestToken(rest);
		if (!hit) {
			runs.push({ kind: 'text', text: rest });
			break;
		}
		// The `_..._` matcher may include a leading space in its match; keep it.
		let { index, len } = hit;
		const matched = rest.slice(index, index + len);
		if (hit.run.kind === 'italic' && /^\s/.test(matched)) {
			runs.push({ kind: 'text', text: rest.slice(0, index + 1) });
			rest = rest.slice(index + 1);
			continue;
		}
		if (index > 0) runs.push({ kind: 'text', text: rest.slice(0, index) });
		if (hit.run.kind === 'link' && !safeHref(hit.run.href)) {
			runs.push({ kind: 'text', text: matched });
		} else {
			runs.push(hit.run);
		}
		rest = rest.slice(index + len);
	}
	// Coalesce adjacent text runs (a downgraded link can split text in two).
	const merged: Inline[] = [];
	for (const run of runs) {
		const prev = merged[merged.length - 1];
		if (run.kind === 'text' && prev && prev.kind === 'text') prev.text += run.text;
		else merged.push(run);
	}
	return merged.length ? merged : [{ kind: 'text', text }];
}
