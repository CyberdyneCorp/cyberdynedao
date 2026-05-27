import { describe, it, expect } from 'vitest';
import {
	Vfs,
	VfsError,
	makeDir,
	makeFile,
	normalizePath,
	displayPath,
	isDir,
	isFile
} from '../vfs';

function sampleRoot() {
	const root = makeDir('');
	const home = makeDir('home');
	const user = makeDir('user');
	user.children['readme.txt'] = makeFile('readme.txt', 'hello\nworld\n');
	const notes = makeDir('notes');
	notes.children['a.md'] = makeFile('a.md', 'note a');
	user.children['notes'] = notes;
	home.children['user'] = user;
	root.children['home'] = home;
	return root;
}

describe('normalizePath', () => {
	it('resolves relative segments against cwd', () => {
		expect(normalizePath('notes', '/home/user', '/home/user')).toEqual(['home', 'user', 'notes']);
	});
	it('handles . and ..', () => {
		expect(normalizePath('../user/./notes', '/home/user', '/home/user')).toEqual([
			'home',
			'user',
			'notes'
		]);
	});
	it('expands ~ to home', () => {
		expect(normalizePath('~/notes', '/', '/home/user')).toEqual(['home', 'user', 'notes']);
		expect(normalizePath('~', '/', '/home/user')).toEqual(['home', 'user']);
	});
	it('absolute paths ignore cwd', () => {
		expect(normalizePath('/etc', '/home/user', '/home/user')).toEqual(['etc']);
	});
	it('cannot pop above root', () => {
		expect(normalizePath('../../../..', '/home', '/home/user')).toEqual([]);
	});
});

describe('displayPath', () => {
	it('collapses home to ~', () => {
		expect(displayPath('/home/user', '/home/user')).toBe('~');
		expect(displayPath('/home/user/notes', '/home/user')).toBe('~/notes');
		expect(displayPath('/etc', '/home/user')).toBe('/etc');
	});
});

describe('Vfs read/resolve', () => {
	it('resolves nested nodes', () => {
		const fs = new Vfs(sampleRoot());
		expect(isFile(fs.resolve('/home/user/readme.txt', '/'))).toBe(true);
		expect(isDir(fs.resolve('/home/user/notes', '/'))).toBe(true);
		expect(fs.resolve('/nope', '/')).toBe(null);
	});
	it('reads file content', () => {
		const fs = new Vfs(sampleRoot());
		expect(fs.readFile('readme.txt', '/home/user')).toBe('hello\nworld\n');
	});
	it('throws reading a directory', () => {
		const fs = new Vfs(sampleRoot());
		expect(() => fs.readFile('notes', '/home/user')).toThrow(VfsError);
	});
	it('throws on missing path', () => {
		const fs = new Vfs(sampleRoot());
		expect(() => fs.resolveOrThrow('ghost', '/home/user')).toThrow(/No such file/);
	});
});

describe('Vfs mutations', () => {
	it('writeFile creates and overwrites', () => {
		const fs = new Vfs(sampleRoot());
		fs.writeFile('new.txt', 'abc', '/home/user');
		expect(fs.readFile('new.txt', '/home/user')).toBe('abc');
		fs.writeFile('new.txt', 'xyz', '/home/user');
		expect(fs.readFile('new.txt', '/home/user')).toBe('xyz');
	});
	it('touch creates empty file', () => {
		const fs = new Vfs(sampleRoot());
		fs.touch('empty', '/home/user');
		expect(fs.readFile('empty', '/home/user')).toBe('');
	});
	it('mkdir without -p refuses missing parents', () => {
		const fs = new Vfs(sampleRoot());
		expect(() => fs.mkdir('a/b/c', '/home/user')).toThrow(/No such file/);
	});
	it('mkdir -p builds the chain', () => {
		const fs = new Vfs(sampleRoot());
		fs.mkdir('a/b/c', '/home/user', true);
		expect(isDir(fs.resolve('/home/user/a/b/c', '/'))).toBe(true);
	});
	it('rm refuses a dir without recursive', () => {
		const fs = new Vfs(sampleRoot());
		expect(() => fs.rm('notes', '/home/user')).toThrow(/Is a directory/);
	});
	it('rm -r removes a subtree', () => {
		const fs = new Vfs(sampleRoot());
		fs.rm('notes', '/home/user', true);
		expect(fs.resolve('/home/user/notes', '/')).toBe(null);
	});
	it('rmdir refuses a non-empty dir', () => {
		const fs = new Vfs(sampleRoot());
		expect(() => fs.rmdir('notes', '/home/user')).toThrow(/not empty/);
	});
	it('mv renames within a dir', () => {
		const fs = new Vfs(sampleRoot());
		fs.mv('readme.txt', 'README', '/home/user');
		expect(fs.resolve('/home/user/readme.txt', '/')).toBe(null);
		expect(fs.readFile('README', '/home/user')).toBe('hello\nworld\n');
	});
	it('mv into a directory keeps the basename', () => {
		const fs = new Vfs(sampleRoot());
		fs.mv('readme.txt', 'notes', '/home/user');
		expect(fs.readFile('notes/readme.txt', '/home/user')).toBe('hello\nworld\n');
	});
	it('cp duplicates a file', () => {
		const fs = new Vfs(sampleRoot());
		fs.cp('readme.txt', 'copy.txt', '/home/user');
		expect(fs.readFile('copy.txt', '/home/user')).toBe('hello\nworld\n');
		expect(fs.readFile('readme.txt', '/home/user')).toBe('hello\nworld\n');
	});
	it('cp -r deep-copies a directory (independent clone)', () => {
		const fs = new Vfs(sampleRoot());
		fs.cp('notes', 'notes2', '/home/user', true);
		fs.writeFile('notes2/a.md', 'changed', '/home/user');
		expect(fs.readFile('notes/a.md', '/home/user')).toBe('note a');
		expect(fs.readFile('notes2/a.md', '/home/user')).toBe('changed');
	});
});

describe('Vfs list + serialize', () => {
	it('lists sorted children', () => {
		const fs = new Vfs(sampleRoot());
		const names = fs.list('/home/user', '/').map((n) => n.name);
		expect(names).toEqual(['notes', 'readme.txt']);
	});
	it('round-trips through JSON', () => {
		const fs = new Vfs(sampleRoot(), '/home/user');
		const restored = Vfs.fromJSON(fs.toJSON());
		expect(restored.home).toBe('/home/user');
		expect(restored.readFile('readme.txt', '/home/user')).toBe('hello\nworld\n');
	});
});
