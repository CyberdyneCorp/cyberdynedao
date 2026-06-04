/**
 * Split an assistant chat reply into renderable segments: prose, fenced
 * code blocks, and Mermaid diagrams. Mermaid gets its own kind so the view
 * can render the diagram (and offer a `.mmd` download) instead of showing
 * the raw definition.
 *
 * Pure + framework-free so it's unit-testable; the rendering lives in the
 * Svelte view.
 */

export type ChatSegment =
	| { kind: 'text'; text: string }
	| { kind: 'code'; lang: string; code: string }
	| { kind: 'mermaid'; code: string };

export function parseSegments(content: string): ChatSegment[] {
	const segments: ChatSegment[] = [];
	const fence = /```([a-zA-Z0-9_+-]*)\n?([\s\S]*?)```/g;
	let last = 0;
	let m: RegExpExecArray | null;
	while ((m = fence.exec(content)) !== null) {
		if (m.index > last) {
			const text = content.slice(last, m.index).trim();
			if (text) segments.push({ kind: 'text', text });
		}
		const lang = (m[1] || '').toLowerCase();
		const code = m[2].replace(/\n$/, '');
		if (lang === 'mermaid') {
			segments.push({ kind: 'mermaid', code });
		} else {
			segments.push({ kind: 'code', lang: m[1] || '', code });
		}
		last = fence.lastIndex;
	}
	const tail = content.slice(last).trim();
	if (tail) segments.push({ kind: 'text', text: tail });
	// No fences → a single text segment (covers the common case).
	if (segments.length === 0 && content) segments.push({ kind: 'text', text: content });
	return segments;
}
