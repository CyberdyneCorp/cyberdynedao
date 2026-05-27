import { describe, it, expect, beforeEach } from 'vitest';
import { runCommandLine, listCommandNames, type CommandContext } from '../commands';
import { seedFilesystem, HOME } from '../seed';

function ctx(overrides: Partial<CommandContext> = {}): CommandContext {
	return {
		vfs: seedFilesystem(),
		cwd: HOME,
		env: { HOME, USER: 'user', PATH: '/usr/bin:/bin', SHELL: '/bin/sh' },
		user: 'user',
		host: 'cyberdyne',
		history: ['ls', 'pwd'],
		...overrides
	};
}

describe('navigation', () => {
	it('pwd prints cwd', () => {
		expect(runCommandLine('pwd', ctx()).stdout).toBe(HOME);
	});
	it('cd changes directory', () => {
		const r = runCommandLine('cd projects', ctx());
		expect(r.cwd).toBe('/home/user/projects');
	});
	it('cd with no arg returns home', () => {
		const r = runCommandLine('cd', ctx({ cwd: '/etc' }));
		expect(r.cwd).toBe(HOME);
	});
	it('cd .. goes up', () => {
		expect(runCommandLine('cd ..', ctx()).cwd).toBe('/home');
	});
	it('cd into a file errors', () => {
		expect(runCommandLine('cd readme.txt', ctx()).stderr).toMatch(/Not a directory/);
	});
	it('cd missing path errors', () => {
		expect(runCommandLine('cd ghost', ctx()).stderr).toMatch(/No such file/);
	});
});

describe('ls', () => {
	it('lists current dir', () => {
		const out = runCommandLine('ls', ctx()).stdout!;
		expect(out).toContain('readme.txt');
		expect(out).toContain('projects');
	});
	it('-a includes . and ..', () => {
		const out = runCommandLine('ls -a', ctx()).stdout!;
		expect(out).toContain('.');
		expect(out).toContain('..');
	});
	it('-l shows long format with mode', () => {
		const out = runCommandLine('ls -l', ctx()).stdout!;
		expect(out).toMatch(/-rw-r--r--/);
		expect(out).toMatch(/drwxr-xr-x/);
	});
	it('errors on a missing path', () => {
		expect(runCommandLine('ls nope', ctx()).stderr).toMatch(/cannot access/);
	});
});

describe('cat / echo', () => {
	it('cat prints file content', () => {
		expect(runCommandLine('cat readme.txt', ctx()).stdout).toMatch(/Welcome to the CyberdyneOS shell/);
	});
	it('cat on a dir errors', () => {
		expect(runCommandLine('cat projects', ctx()).stderr).toMatch(/Is a directory/);
	});
	it('echo joins args', () => {
		expect(runCommandLine('echo hello world', ctx()).stdout).toBe('hello world');
	});
	it('echo respects quotes', () => {
		expect(runCommandLine('echo "a   b"', ctx()).stdout).toBe('a   b');
	});
});

describe('mutations', () => {
	it('mkdir + touch + ls reflect changes', () => {
		const c = ctx();
		runCommandLine('mkdir sub', c);
		runCommandLine('touch sub/file.txt', c);
		const out = runCommandLine('ls sub', c).stdout!;
		expect(out).toContain('file.txt');
	});
	it('mkdir -p builds nested', () => {
		const c = ctx();
		expect(runCommandLine('mkdir a/b', c).stderr).toMatch(/No such file/);
		runCommandLine('mkdir -p a/b/c', c);
		expect(runCommandLine('ls a/b', c).stdout).toContain('c');
	});
	it('rm removes a file; -r removes a dir', () => {
		const c = ctx();
		runCommandLine('rm readme.txt', c);
		expect(runCommandLine('cat readme.txt', c).stderr).toMatch(/No such file/);
		expect(runCommandLine('rm notes', c).stderr).toMatch(/Is a directory/);
		runCommandLine('rm -r notes', c);
		expect(runCommandLine('ls notes', c).stderr).toMatch(/cannot access/);
	});
	it('rm -f swallows missing-file errors', () => {
		expect(runCommandLine('rm -f ghost', ctx())).toEqual({});
	});
	it('mv renames', () => {
		const c = ctx();
		runCommandLine('mv readme.txt README', c);
		expect(runCommandLine('cat README', c).stdout).toMatch(/Welcome/);
	});
	it('cp -r copies a tree', () => {
		const c = ctx();
		runCommandLine('cp -r notes notes-bak', c);
		expect(runCommandLine('ls notes-bak', c).stdout).toContain('todo.md');
	});
});

describe('find', () => {
	it('lists everything from .', () => {
		const out = runCommandLine('find .', ctx()).stdout!;
		expect(out).toContain('.');
		expect(out).toContain('./notes/todo.md');
	});
	it('-name with glob', () => {
		const out = runCommandLine("find . -name '*.md'", ctx()).stdout!;
		expect(out).toContain('./notes/todo.md');
		expect(out).not.toContain('readme.txt');
	});
	it('-type d lists only directories', () => {
		const out = runCommandLine('find . -type d', ctx()).stdout!;
		expect(out).toContain('./projects');
		expect(out).not.toContain('readme.txt');
	});
});

describe('grep', () => {
	it('matches a line in a file', () => {
		const out = runCommandLine('grep Welcome readme.txt', ctx()).stdout!;
		expect(out).toMatch(/Welcome/);
	});
	it('-n shows line numbers', () => {
		const out = runCommandLine('grep -n TODO notes/todo.md', ctx()).stdout!;
		expect(out).toMatch(/^1:/);
	});
	it('-i is case-insensitive', () => {
		const out = runCommandLine('grep -i welcome readme.txt', ctx()).stdout!;
		expect(out).toMatch(/Welcome/);
	});
	it('-r recurses and prefixes paths', () => {
		const out = runCommandLine('grep -r robot .', ctx()).stdout!;
		expect(out).toMatch(/ideas\.md/);
	});
	it('grep on a dir without -r errors', () => {
		expect(runCommandLine('grep x notes', ctx()).stderr).toMatch(/Is a directory/);
	});
});

describe('head / tail / wc', () => {
	it('head -n limits lines', () => {
		const c = ctx();
		runCommandLine('rm readme.txt', c);
		c.vfs.writeFile('nums.txt', '1\n2\n3\n4\n5\n', HOME);
		expect(runCommandLine('head -n 2 nums.txt', c).stdout).toBe('1\n2');
	});
	it('tail -n limits from the end', () => {
		const c = ctx();
		c.vfs.writeFile('nums.txt', '1\n2\n3\n4\n5\n', HOME);
		expect(runCommandLine('tail -n 2 nums.txt', c).stdout).toBe('4\n5');
	});
	it('wc -l counts lines', () => {
		const c = ctx();
		c.vfs.writeFile('nums.txt', '1\n2\n3\n', HOME);
		expect(runCommandLine('wc -l nums.txt', c).stdout).toMatch(/3 nums\.txt/);
	});
});

describe('tree', () => {
	it('draws branches and a summary', () => {
		const out = runCommandLine('tree notes', ctx()).stdout!;
		expect(out).toContain('├── ');
		expect(out).toMatch(/director/);
	});
});

describe('system info + meta', () => {
	it('whoami / hostname', () => {
		expect(runCommandLine('whoami', ctx()).stdout).toBe('user');
		expect(runCommandLine('hostname', ctx()).stdout).toBe('cyberdyne');
	});
	it('uname -a is verbose', () => {
		expect(runCommandLine('uname -a', ctx()).stdout).toMatch(/CyberdyneOS cyberdyne/);
	});
	it('env prints vars', () => {
		expect(runCommandLine('env', ctx()).stdout).toMatch(/USER=user/);
	});
	it('history numbers entries', () => {
		expect(runCommandLine('history', ctx()).stdout).toMatch(/1  ls/);
	});
	it('clear signals a screen clear', () => {
		expect(runCommandLine('clear', ctx()).clear).toBe(true);
	});
	it('help lists commands', () => {
		expect(runCommandLine('help', ctx()).stdout).toMatch(/grep/);
	});
	it('man shows usage', () => {
		expect(runCommandLine('man ls', ctx()).stdout).toMatch(/SYNOPSIS/);
	});
	it('man on unknown errors', () => {
		expect(runCommandLine('man zzz', ctx()).stderr).toMatch(/No manual entry/);
	});
});

describe('dispatch', () => {
	it('unknown command', () => {
		expect(runCommandLine('frobnicate', ctx()).stderr).toMatch(/command not found/);
	});
	it('blank line is a no-op', () => {
		expect(runCommandLine('   ', ctx())).toEqual({});
	});
	it('vi requests a launch', () => {
		expect(runCommandLine('vi scratch.txt', ctx()).launch).toEqual({
			program: 'vi',
			args: ['scratch.txt']
		});
	});
	it('top requests a launch', () => {
		expect(runCommandLine('top', ctx()).launch).toEqual({ program: 'top', args: [] });
	});
	it('registry exposes the documented commands', () => {
		const names = listCommandNames();
		for (const n of ['ls', 'cd', 'grep', 'find', 'vi', 'top', 'help', 'man']) {
			expect(names).toContain(n);
		}
	});
});
