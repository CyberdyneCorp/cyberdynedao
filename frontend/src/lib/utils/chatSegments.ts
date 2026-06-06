/**
 * Split an assistant chat reply into renderable segments: prose, fenced
 * code blocks, Mermaid diagrams, and display (block) math. Mermaid and math
 * get their own kinds so the view can render them (a diagram / a typeset
 * formula) instead of showing the raw source.
 *
 * Display math uses LaTeX delimiters `\[ … \]` or `$$ … $$`. Inline math
 * (`\( … \)`) is left inside text segments and handled by `parseInlineMath`
 * at render time — single-`$` is deliberately NOT treated as math so prices
 * like "$5k" aren't mangled.
 *
 * Pure + framework-free so it's unit-testable; the rendering lives in the
 * Svelte view.
 */

export type ChatSegment =
	| { kind: 'text'; text: string }
	| { kind: 'code'; lang: string; code: string }
	| { kind: 'mermaid'; code: string }
	| { kind: 'math'; code: string };

// Display-math delimiters: \[ … \] and $$ … $$.
const BLOCK_MATH = /\\\[([\s\S]*?)\\\]|\$\$([\s\S]*?)\$\$/g;

/** Push a prose region, carving out any display-math blocks into `math`
 *  segments and keeping the surrounding prose as `text`. */
function pushProse(segments: ChatSegment[], region: string): void {
	let last = 0;
	let m: RegExpExecArray | null;
	BLOCK_MATH.lastIndex = 0;
	while ((m = BLOCK_MATH.exec(region)) !== null) {
		const before = region.slice(last, m.index).trim();
		if (before) segments.push({ kind: 'text', text: before });
		const code = (m[1] ?? m[2] ?? '').trim();
		if (code) segments.push({ kind: 'math', code });
		last = BLOCK_MATH.lastIndex;
	}
	const tail = region.slice(last).trim();
	if (tail) segments.push({ kind: 'text', text: tail });
}

export function parseSegments(content: string): ChatSegment[] {
	const segments: ChatSegment[] = [];
	const fence = /```([a-zA-Z0-9_+-]*)\n?([\s\S]*?)```/g;
	let last = 0;
	let m: RegExpExecArray | null;
	while ((m = fence.exec(content)) !== null) {
		if (m.index > last) pushProse(segments, content.slice(last, m.index));
		const lang = (m[1] || '').toLowerCase();
		const code = m[2].replace(/\n$/, '');
		if (lang === 'mermaid') {
			segments.push({ kind: 'mermaid', code });
		} else {
			segments.push({ kind: 'code', lang: m[1] || '', code });
		}
		last = fence.lastIndex;
	}
	pushProse(segments, content.slice(last));
	// No fences and no math → a single text segment (covers the common case).
	if (segments.length === 0 && content) segments.push({ kind: 'text', text: content });
	return segments;
}
