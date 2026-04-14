import { describe, it, expect } from 'vitest';
import { terminalCommands } from '../terminalCommands';

describe('terminalCommands', () => {
	it('help lists commands', () => {
		const out = terminalCommands.processCommand('help');
		expect(out).toContain('Available commands');
	});

	it('clear returns empty string', () => {
		expect(terminalCommands.processCommand('clear')).toBe('');
	});

	it('date returns date-like string', () => {
		const out = terminalCommands.processCommand('date');
		expect(out.length).toBeGreaterThan(0);
	});

	it('whoami returns user', () => {
		expect(terminalCommands.processCommand('whoami')).toBe('user');
	});

	it('chat greeting', () => {
		expect(terminalCommands.processCommand('chat')).toContain('ChatBot');
	});

	it('about returns version', () => {
		expect(terminalCommands.processCommand('about')).toContain('CyberdyneOS');
	});

	it('exit returns goodbye', () => {
		expect(terminalCommands.processCommand('exit')).toContain('Goodbye');
	});

	it('ask with args echoes question', () => {
		expect(terminalCommands.processCommand('ask What is JS?')).toContain('What is JS?');
	});

	it('ask without args falls through to not-found', () => {
		expect(terminalCommands.processCommand('ask')).toContain('not found');
	});

	it('unknown command returns not found', () => {
		expect(terminalCommands.processCommand('blargh')).toMatch(/not found/);
	});

	it('is case-insensitive', () => {
		expect(terminalCommands.processCommand('HELP')).toContain('Available commands');
	});

	it('getAvailableCommands returns list', () => {
		expect(terminalCommands.getAvailableCommands().length).toBeGreaterThan(0);
	});
});
