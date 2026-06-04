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
});
