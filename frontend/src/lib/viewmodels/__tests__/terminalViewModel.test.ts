import { describe, it, expect, beforeEach } from 'vitest';
import { createTerminalViewModel } from '../terminalViewModel.svelte';

beforeEach(() => {
	sessionStorage.clear();
});

function lastOutput(vm: ReturnType<typeof createTerminalViewModel>): string {
	return vm.lines
		.filter((l) => l.type === 'output' || l.type === 'error')
		.map((l) => l.text)
		.join('\n');
}

describe('terminalViewModel — basics', () => {
	it('boots with a banner and home prompt', () => {
		const vm = createTerminalViewModel();
		expect(vm.lines.some((l) => l.text.includes('CyberdyneOS'))).toBe(true);
		expect(vm.prompt).toBe('user@cyberdyne:~$');
	});

	it('echoes the command with the prompt', () => {
		const vm = createTerminalViewModel();
		vm.submit('pwd');
		const input = vm.lines.find((l) => l.type === 'input');
		expect(input?.text).toBe('user@cyberdyne:~$ pwd');
	});

	it('pwd prints the working directory', () => {
		const vm = createTerminalViewModel();
		vm.submit('pwd');
		expect(lastOutput(vm)).toContain('/home/user');
	});

	it('cd updates cwd and prompt', () => {
		const vm = createTerminalViewModel();
		vm.submit('cd projects');
		expect(vm.cwd).toBe('/home/user/projects');
		expect(vm.prompt).toBe('user@cyberdyne:~/projects$');
	});

	it('blank submit only echoes the prompt', () => {
		const vm = createTerminalViewModel();
		const before = vm.lines.length;
		vm.submit('   ');
		expect(vm.lines.length).toBe(before + 1);
		expect(vm.lines[vm.lines.length - 1].type).toBe('input');
	});

	it('clear empties the scrollback', () => {
		const vm = createTerminalViewModel();
		vm.submit('ls');
		vm.submit('clear');
		expect(vm.lines.length).toBe(0);
	});

	it('unknown command reports an error line', () => {
		const vm = createTerminalViewModel();
		vm.submit('frobnicate');
		expect(vm.lines.some((l) => l.type === 'error' && /command not found/.test(l.text))).toBe(true);
	});
});

describe('terminalViewModel — persistence', () => {
	it('mutations survive a fresh view-model (same session)', () => {
		const vm1 = createTerminalViewModel();
		vm1.submit('mkdir demo-dir');
		vm1.submit('cd demo-dir');
		const vm2 = createTerminalViewModel();
		// cwd restored, and the dir exists
		expect(vm2.cwd).toBe('/home/user/demo-dir');
		vm2.submit('cd ..');
		vm2.submit('ls');
		expect(lastOutput(vm2)).toContain('demo-dir');
	});

	it('reset re-seeds and clears storage', () => {
		const vm = createTerminalViewModel();
		vm.submit('rm readme.txt');
		vm.reset();
		expect(sessionStorage.getItem('cyberdyne.shell.v1')).toBe(null);
		vm.submit('ls');
		expect(lastOutput(vm)).toContain('readme.txt');
	});
});

describe('terminalViewModel — history recall', () => {
	it('↑ walks back through commands, ↓ forward', () => {
		const vm = createTerminalViewModel();
		vm.submit('ls');
		vm.submit('pwd');
		expect(vm.recallPrev('')).toBe('pwd');
		expect(vm.recallPrev('')).toBe('ls');
		expect(vm.recallNext('')).toBe('pwd');
		expect(vm.recallNext('')).toBe('');
	});

	it('does not store consecutive duplicates', () => {
		const vm = createTerminalViewModel();
		vm.submit('ls');
		vm.submit('ls');
		expect(vm.recallPrev('')).toBe('ls');
		// only one entry → going further back stays put
		expect(vm.recallPrev('')).toBe('ls');
	});
});

describe('terminalViewModel — tab completion', () => {
	it('completes a unique command name with a trailing space', () => {
		const vm = createTerminalViewModel();
		const r = vm.complete('gre');
		expect(r.line).toBe('grep ');
	});

	it('lists multiple command matches', () => {
		const vm = createTerminalViewModel();
		const r = vm.complete('t'); // top, touch, tree, tail
		expect(r.suggestions.length).toBeGreaterThan(1);
	});

	it('completes a path operand against the VFS', () => {
		const vm = createTerminalViewModel();
		const r = vm.complete('cat read');
		expect(r.line).toBe('cat readme.txt');
	});

	it('appends a slash when completing a directory', () => {
		const vm = createTerminalViewModel();
		const r = vm.complete('cd proj');
		expect(r.line).toBe('cd projects/');
	});
});

describe('terminalViewModel — vi integration', () => {
	it('launches vi and exposes the editor', () => {
		const vm = createTerminalViewModel();
		vm.submit('vi scratch.txt');
		expect(vm.activeProgram).toBe('vi');
		expect(vm.editor).not.toBe(null);
	});

	it(':wq writes the buffer back to the VFS and closes', () => {
		const vm = createTerminalViewModel();
		vm.submit('vi newfile.txt');
		for (const k of ['i', 'h', 'e', 'l', 'l', 'o', 'Escape', ':', 'w', 'q', 'Enter']) {
			vm.feedEditor(k);
		}
		expect(vm.activeProgram).toBe(null);
		vm.submit('cat newfile.txt');
		expect(lastOutput(vm)).toContain('hello');
	});

	it(':q! discards changes', () => {
		const vm = createTerminalViewModel();
		vm.submit('vi scratch.txt');
		for (const k of ['i', 'x', 'Escape', ':', 'q', '!', 'Enter']) vm.feedEditor(k);
		expect(vm.activeProgram).toBe(null);
		vm.submit('cat scratch.txt');
		// scratch.txt seeded empty → still empty
		expect(lastOutput(vm).trim()).toBe('');
	});

	it('refuses to open a directory in vi', () => {
		const vm = createTerminalViewModel();
		vm.submit('vi projects');
		expect(vm.activeProgram).toBe(null);
		expect(vm.lines.some((l) => l.type === 'error' && /Is a directory/.test(l.text))).toBe(true);
	});
});

describe('terminalViewModel — top integration', () => {
	it('launches top and ticks update the model', () => {
		const vm = createTerminalViewModel();
		vm.submit('top');
		expect(vm.activeProgram).toBe('top');
		expect(vm.top).not.toBe(null);
		vm.tickTop();
		expect(vm.top!.ticks).toBe(1);
		vm.quitTop();
		expect(vm.activeProgram).toBe(null);
	});
});
