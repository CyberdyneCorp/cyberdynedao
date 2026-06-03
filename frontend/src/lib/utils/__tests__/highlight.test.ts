import { describe, expect, it } from 'vitest';
import { highlight, isSupportedLanguage } from '../highlight';

describe('highlight util', () => {
	it('supports the academy languages (incl. aliases)', () => {
		for (const lang of [
			'matlab',
			'python',
			'verilog',
			'systemverilog', // alias → verilog
			'c',
			'cpp',
			'c++', // alias → cpp
			'bash',
			'sh', // alias → bash
			'typescript',
			'ts', // alias → typescript
			'javascript',
			'js' // alias → javascript
		]) {
			expect(isSupportedLanguage(lang), lang).toBe(true);
		}
	});

	it('does not claim support for unknown languages', () => {
		expect(isSupportedLanguage('cobol')).toBe(false);
		expect(isSupportedLanguage('')).toBe(false);
		expect(isSupportedLanguage(undefined)).toBe(false);
	});

	it('emits hljs token markup for a known language', () => {
		const html = highlight('total = 0;\nfor k = 1:5\nend', 'matlab');
		expect(html).toContain('hljs-'); // at least one token span
	});

	it('escapes and does not tokenise an unknown language', () => {
		const html = highlight('a < b && c > d', 'cobol');
		expect(html).toContain('&lt;');
		expect(html).toContain('&gt;');
		expect(html).not.toContain('hljs-');
	});
});
