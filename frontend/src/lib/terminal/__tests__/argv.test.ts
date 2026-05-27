import { describe, it, expect } from 'vitest';
import { tokenize, parseArgs } from '../argv';

describe('tokenize', () => {
	it('splits on whitespace', () => {
		expect(tokenize('ls -la /home')).toEqual(['ls', '-la', '/home']);
	});
	it('collapses repeated spaces and tabs', () => {
		expect(tokenize('  echo   a\tb ')).toEqual(['echo', 'a', 'b']);
	});
	it('groups double-quoted tokens', () => {
		expect(tokenize('echo "hello world"')).toEqual(['echo', 'hello world']);
	});
	it('groups single-quoted tokens', () => {
		expect(tokenize("grep 'to do' file")).toEqual(['grep', 'to do', 'file']);
	});
	it('keeps an empty quoted token', () => {
		expect(tokenize('echo ""')).toEqual(['echo', '']);
	});
	it('honors backslash escape outside quotes', () => {
		expect(tokenize('touch a\\ b')).toEqual(['touch', 'a b']);
	});
	it('honors backslash escape inside double quotes', () => {
		expect(tokenize('echo "a\\"b"')).toEqual(['echo', 'a"b']);
	});
	it('returns empty for blank input', () => {
		expect(tokenize('   ')).toEqual([]);
	});
});

describe('parseArgs', () => {
	it('separates operands from flags', () => {
		const { flags, operands } = parseArgs(['ls', '-l', 'dir']);
		expect([...flags]).toEqual(['l']);
		expect(operands).toEqual(['ls', 'dir']);
	});
	it('explodes bundled short flags', () => {
		const { flags } = parseArgs(['-la']);
		expect(flags.has('l')).toBe(true);
		expect(flags.has('a')).toBe(true);
	});
	it('keeps long flags whole', () => {
		const { flags } = parseArgs(['--color', 'x']);
		expect(flags.has('color')).toBe(true);
	});
	it('-- stops flag parsing', () => {
		const { flags, operands } = parseArgs(['--', '-weird-name']);
		expect(flags.size).toBe(0);
		expect(operands).toEqual(['-weird-name']);
	});
	it('treats a lone - as an operand', () => {
		const { operands } = parseArgs(['-']);
		expect(operands).toEqual(['-']);
	});
});
