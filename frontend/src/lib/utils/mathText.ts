/**
 * Split a prose string into plain-text and inline-math runs so the view can
 * typeset `\( … \)` formulas while leaving the rest as text. Single-`$` is
 * intentionally NOT treated as math — prices ("$5k-15k", treasury USD) would
 * otherwise be swallowed. Display math (`\[ … \]`, `$$ … $$`) is handled
 * earlier by `parseSegments`, not here.
 *
 * Pure + framework-free so it's unit-testable.
 */

export type InlineRun = { kind: 'text'; text: string } | { kind: 'math'; code: string };

const INLINE_MATH = /\\\(([\s\S]*?)\\\)/g;

export function parseInlineMath(text: string): InlineRun[] {
	const runs: InlineRun[] = [];
	let last = 0;
	let m: RegExpExecArray | null;
	INLINE_MATH.lastIndex = 0;
	while ((m = INLINE_MATH.exec(text)) !== null) {
		if (m.index > last) runs.push({ kind: 'text', text: text.slice(last, m.index) });
		const code = m[1].trim();
		// Empty \(\) isn't math — keep the literal delimiters as text.
		runs.push(code ? { kind: 'math', code } : { kind: 'text', text: m[0] });
		last = INLINE_MATH.lastIndex;
	}
	if (last < text.length) runs.push({ kind: 'text', text: text.slice(last) });
	if (runs.length === 0) runs.push({ kind: 'text', text });
	return runs;
}
