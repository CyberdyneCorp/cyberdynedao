import { describe, it, expect } from 'vitest';
import { ViEditor } from '../vi';

function type(ed: ViEditor, keys: string[]) {
	for (const k of keys) ed.feed(k);
}

describe('ViEditor', () => {
	it('seeds buffer from content and starts in normal mode', () => {
		const ed = new ViEditor('f.txt', 'one\ntwo\n');
		expect(ed.lines).toEqual(['one', 'two']);
		expect(ed.mode).toBe('normal');
	});

	it('empty file yields a single empty line', () => {
		const ed = new ViEditor('f.txt', '');
		expect(ed.lines).toEqual(['']);
	});

	it('i enters insert mode and types characters', () => {
		const ed = new ViEditor('f.txt', '');
		ed.feed('i');
		expect(ed.mode).toBe('insert');
		type(ed, ['h', 'i']);
		expect(ed.lines[0]).toBe('hi');
		expect(ed.dirty).toBe(true);
	});

	it('Enter splits a line in insert mode', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'a', 'b']);
		ed.feed('Enter');
		ed.feed('c');
		expect(ed.lines).toEqual(['ab', 'c']);
	});

	it('Backspace joins lines at column 0', () => {
		const ed = new ViEditor('f.txt', 'ab\ncd\n');
		// move to row 1, enter insert at col 0, backspace
		type(ed, ['j', 'i', 'Backspace']);
		expect(ed.lines).toEqual(['abcd']);
	});

	it('Escape returns to normal mode', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'x', 'Escape']);
		expect(ed.mode).toBe('normal');
	});

	it('x deletes the char under the cursor', () => {
		const ed = new ViEditor('f.txt', 'abc\n');
		ed.feed('x');
		expect(ed.lines[0]).toBe('bc');
	});

	it('dd deletes the current line', () => {
		const ed = new ViEditor('f.txt', 'a\nb\nc\n');
		type(ed, ['d', 'd']);
		expect(ed.lines).toEqual(['b', 'c']);
	});

	it('o opens a line below and inserts', () => {
		const ed = new ViEditor('f.txt', 'top\n');
		type(ed, ['o', 'n', 'e', 'w']);
		expect(ed.lines).toEqual(['top', 'new']);
	});

	it('hjkl movement is bounded', () => {
		const ed = new ViEditor('f.txt', 'abc\ndef\n');
		type(ed, ['j', 'l', 'l']);
		expect(ed.row).toBe(1);
		expect(ed.col).toBe(2);
		type(ed, ['k', 'k', 'h', 'h', 'h']);
		expect(ed.row).toBe(0);
		expect(ed.col).toBe(0);
	});

	it('G jumps to the last line, gg to the first', () => {
		const ed = new ViEditor('f.txt', 'a\nb\nc\n');
		ed.feed('G');
		expect(ed.row).toBe(2);
		type(ed, ['g', 'g']);
		expect(ed.row).toBe(0);
	});

	it(':w returns a write action and clears dirty', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'x', 'Escape']);
		expect(ed.dirty).toBe(true);
		const action = feedCmd(ed, 'w');
		expect(action).toEqual({ kind: 'write' });
		expect(ed.dirty).toBe(false);
	});

	it(':q refuses when there are unsaved changes', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'x', 'Escape']);
		const action = feedCmd(ed, 'q');
		expect(action).toBe(null);
		expect(ed.status).toMatch(/No write since last change/);
	});

	it(':q! quits even when dirty', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'x', 'Escape']);
		expect(feedCmd(ed, 'q!')).toEqual({ kind: 'quit' });
	});

	it(':wq writes and quits', () => {
		const ed = new ViEditor('f.txt', '');
		type(ed, ['i', 'h', 'i', 'Escape']);
		expect(feedCmd(ed, 'wq')).toEqual({ kind: 'write-quit' });
	});

	it('unknown : command reports an error', () => {
		const ed = new ViEditor('f.txt', '');
		expect(feedCmd(ed, 'zzz')).toBe(null);
		expect(ed.status).toMatch(/Not an editor command/);
	});

	it('text() round-trips with a trailing newline', () => {
		const ed = new ViEditor('f.txt', 'a\nb\n');
		expect(ed.text()).toBe('a\nb\n');
	});
});

// Helper: enter command mode and type a command, then Enter.
function feedCmd(ed: ViEditor, cmd: string) {
	ed.feed(':');
	for (const c of cmd) ed.feed(c);
	return ed.feed('Enter');
}
