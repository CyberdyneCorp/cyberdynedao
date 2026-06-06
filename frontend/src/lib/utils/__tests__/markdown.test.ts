import { describe, expect, it } from 'vitest';
import { parseBlocks, parseInline } from '../markdown';

describe('parseInline', () => {
	it('returns a single text run for plain prose', () => {
		expect(parseInline('hello world')).toEqual([{ kind: 'text', text: 'hello world' }]);
	});

	it('parses bold, keeping surrounding text', () => {
		expect(parseInline('a **bold** b')).toEqual([
			{ kind: 'text', text: 'a ' },
			{ kind: 'bold', text: 'bold' },
			{ kind: 'text', text: ' b' }
		]);
	});

	it('prefers bold over italic at the same position', () => {
		expect(parseInline('**x**')).toEqual([{ kind: 'bold', text: 'x' }]);
	});

	it('parses inline code and links', () => {
		expect(parseInline('see `code` and [site](https://x.com)')).toEqual([
			{ kind: 'text', text: 'see ' },
			{ kind: 'code', text: 'code' },
			{ kind: 'text', text: ' and ' },
			{ kind: 'link', text: 'site', href: 'https://x.com' }
		]);
	});

	it('downgrades an unsafe link to plain text', () => {
		expect(parseInline('[x](javascript:alert(1))')).toEqual([
			{ kind: 'text', text: '[x](javascript:alert(1))' }
		]);
	});

	it('parses inline math', () => {
		expect(parseInline('angle \\(x\\) here')).toEqual([
			{ kind: 'text', text: 'angle ' },
			{ kind: 'math', code: 'x' },
			{ kind: 'text', text: ' here' }
		]);
	});

	it('does not treat arithmetic asterisks as italic', () => {
		expect(parseInline('5 * 3 = 15')).toEqual([{ kind: 'text', text: '5 * 3 = 15' }]);
	});
});

describe('parseBlocks', () => {
	it('splits headings, paragraphs, and blank lines', () => {
		const blocks = parseBlocks('# Title\n\nsome text');
		expect(blocks).toEqual([
			{ kind: 'heading', level: 1, text: 'Title' },
			{ kind: 'paragraph', text: 'some text' }
		]);
	});

	it('groups consecutive bullet items into one list', () => {
		const blocks = parseBlocks('- one\n- two\n- three');
		expect(blocks).toEqual([{ kind: 'list', ordered: false, items: ['one', 'two', 'three'] }]);
	});

	it('groups numbered items into an ordered list', () => {
		const blocks = parseBlocks('1. first\n2. second');
		expect(blocks).toEqual([{ kind: 'list', ordered: true, items: ['first', 'second'] }]);
	});

	it('keeps inline markers in block text for later inline parsing', () => {
		const blocks = parseBlocks('1. **Bold label**: detail');
		expect(blocks).toEqual([
			{ kind: 'list', ordered: true, items: ['**Bold label**: detail'] }
		]);
	});

	it('joins wrapped paragraph lines', () => {
		expect(parseBlocks('line one\nline two')).toEqual([
			{ kind: 'paragraph', text: 'line one line two' }
		]);
	});
});
