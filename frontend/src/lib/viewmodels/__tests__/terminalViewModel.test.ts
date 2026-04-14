import { describe, it, expect, vi } from 'vitest';
import { get } from 'svelte/store';
import { createTerminalViewModel } from '../terminalViewModel';

describe('terminalViewModel', () => {
	it('boots with welcome messages', () => {
		const vm = createTerminalViewModel();
		const h = get(vm.history);
		expect(h[0].text).toContain('Welcome');
	});

	it('empty submit is a noop', () => {
		const vm = createTerminalViewModel();
		const before = get(vm.history).length;
		vm.submit('  ');
		expect(get(vm.history).length).toBe(before);
	});

	it('submit appends input and response', () => {
		const process = vi.fn().mockReturnValue('response!');
		const vm = createTerminalViewModel('u', 'h', process);
		vm.submit('help');
		const h = get(vm.history);
		const last = h.slice(-2);
		expect(last[0].type).toBe('input');
		expect(last[0].text).toContain('u@h $ help');
		expect(last[1]).toEqual({ type: 'output', text: 'response!' });
		expect(process).toHaveBeenCalledWith('help');
	});

	it('clear resets history to welcome only', () => {
		const process = vi.fn();
		const vm = createTerminalViewModel('u', 'h', process);
		vm.submit('clear');
		const h = get(vm.history);
		expect(h.length).toBe(2);
		expect(process).not.toHaveBeenCalled();
	});

	it('reset restores boot history', () => {
		const vm = createTerminalViewModel();
		vm.submit('help');
		vm.reset();
		const h = get(vm.history);
		expect(h[0].text).toContain('Welcome');
	});

	it('uses provided user/host defaults', () => {
		const vm = createTerminalViewModel();
		expect(vm.user).toBe('user');
		expect(vm.host).toBe('CyberdyneOS');
	});
});
