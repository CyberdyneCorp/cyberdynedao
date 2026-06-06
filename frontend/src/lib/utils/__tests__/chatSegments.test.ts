import { describe, expect, it } from 'vitest';
import { parseSegments } from '../chatSegments';

describe('parseSegments', () => {
	it('returns a single text segment when there are no fences', () => {
		expect(parseSegments('just prose')).toEqual([{ kind: 'text', text: 'just prose' }]);
	});

	it('splits prose, code fences, and mermaid into separate segments', () => {
		const content = [
			'Here is a diagram:',
			'```mermaid',
			'graph TD; A-->B',
			'```',
			'And some python:',
			'```python',
			'print(1)',
			'```'
		].join('\n');
		const segs = parseSegments(content);
		expect(segs).toEqual([
			{ kind: 'text', text: 'Here is a diagram:' },
			{ kind: 'mermaid', code: 'graph TD; A-->B' },
			{ kind: 'text', text: 'And some python:' },
			{ kind: 'code', lang: 'python', code: 'print(1)' }
		]);
	});

	it('treats a ```mermaid fence (any case) as a mermaid segment, not code', () => {
		const segs = parseSegments('```Mermaid\nsequenceDiagram\nA->>B: hi\n```');
		expect(segs).toHaveLength(1);
		expect(segs[0]).toEqual({ kind: 'mermaid', code: 'sequenceDiagram\nA->>B: hi' });
	});

	it('keeps a plain code fence as a code segment with its language', () => {
		const segs = parseSegments('```ts\nconst x = 1;\n```');
		expect(segs[0]).toEqual({ kind: 'code', lang: 'ts', code: 'const x = 1;' });
	});

	it('carves \\[ … \\] display math out of prose into a math segment', () => {
		const segs = parseSegments('The sine function:\n\\[\ny = \\sin(x)\n\\]\nis periodic.');
		expect(segs).toEqual([
			{ kind: 'text', text: 'The sine function:' },
			{ kind: 'math', code: 'y = \\sin(x)' },
			{ kind: 'text', text: 'is periodic.' }
		]);
	});

	it('treats $$ … $$ as display math', () => {
		const segs = parseSegments('Euler: $$e^{i\\pi} + 1 = 0$$ done');
		expect(segs).toEqual([
			{ kind: 'text', text: 'Euler:' },
			{ kind: 'math', code: 'e^{i\\pi} + 1 = 0' },
			{ kind: 'text', text: 'done' }
		]);
	});

	it('leaves single-$ prices as plain text (not math)', () => {
		const segs = parseSegments('Budget is $5k-15k for the project.');
		expect(segs).toEqual([{ kind: 'text', text: 'Budget is $5k-15k for the project.' }]);
	});

	it('does not parse math inside a code fence', () => {
		const segs = parseSegments('```python\nx = "\\\\[not math\\\\]"\n```');
		expect(segs).toHaveLength(1);
		expect(segs[0].kind).toBe('code');
	});
});
