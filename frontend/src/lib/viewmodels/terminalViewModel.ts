import { writable, type Writable } from 'svelte/store';
import { terminalCommands } from '$lib/utils/terminalCommands';

export type TerminalLineType = 'input' | 'output' | 'system';

export interface TerminalLine {
	type: TerminalLineType;
	text: string;
	timestamp?: string;
}

function bootHistory(): TerminalLine[] {
	const now = new Date();
	return [
		{ type: 'system', text: 'Welcome to CyberdyneOS!' },
		{ type: 'system', text: 'For available commands, try "help".' },
		{ type: 'system', text: `Last login: ${now.toLocaleDateString()}, ${now.toLocaleTimeString()}` },
		{ type: 'system', text: '' }
	];
}

function clearHistory(): TerminalLine[] {
	return [
		{ type: 'system', text: 'Welcome to CyberdyneOS!' },
		{ type: 'system', text: 'For available commands, try "help".' }
	];
}

export interface TerminalViewModel {
	history: Writable<TerminalLine[]>;
	user: string;
	host: string;
	submit: (input: string) => void;
	reset: () => void;
}

export function createTerminalViewModel(
	user = 'user',
	host = 'CyberdyneOS',
	process: (input: string) => string = terminalCommands.processCommand
): TerminalViewModel {
	const history = writable<TerminalLine[]>(bootHistory());

	return {
		history,
		user,
		host,
		submit: (rawInput) => {
			const input = rawInput.trim();
			if (input === '') return;
			const timestamp = new Date().toLocaleTimeString();
			const inputLine: TerminalLine = {
				type: 'input',
				text: `${user}@${host} $ ${rawInput}`,
				timestamp
			};
			if (input.toLowerCase() === 'clear') {
				history.set(clearHistory());
				return;
			}
			const response = process(input);
			history.update(current => [...current, inputLine, { type: 'output', text: response }]);
		},
		reset: () => history.set(bootHistory())
	};
}
