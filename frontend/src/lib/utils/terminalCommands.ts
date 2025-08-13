/**
 * Terminal command processing utility
 * Handles all terminal command logic in a reusable way
 */

interface Command {
	name: string;
	description: string;
	execute: (args?: string) => string;
}

const commands: Record<string, Command> = {
	help: {
		name: 'help',
		description: 'Show this help message',
		execute: () => `Available commands:
help     - Show this help message
clear    - Clear the terminal
date     - Show current date and time
whoami   - Show current user
chat     - Start chatbot conversation
ask      - Ask the AI assistant a question (e.g., "ask What is JavaScript?")
about    - Show information about this terminal
exit     - Close terminal (same as clicking X)`
	},
	
	clear: {
		name: 'clear',
		description: 'Clear the terminal',
		execute: () => '' // Special case handled in component
	},
	
	date: {
		name: 'date',
		description: 'Show current date and time',
		execute: () => new Date().toString()
	},
	
	whoami: {
		name: 'whoami',
		description: 'Show current user',
		execute: () => 'user'
	},
	
	chat: {
		name: 'chat',
		description: 'Start chatbot conversation',
		execute: () => `ChatBot: Hello! I'm your AI assistant. How can I help you today?
Type your questions or messages, and I'll do my best to help!`
	},
	
	about: {
		name: 'about',
		description: 'Show information about this terminal',
		execute: () => `CyberdyneOS Terminal v1.0
A retro-style terminal interface for chatbot interactions
Built with Svelte and styled with classic green terminal aesthetics`
	},
	
	exit: {
		name: 'exit',
		description: 'Close terminal (same as clicking X)',
		execute: () => 'Goodbye! Closing terminal...'
	}
};

/**
 * Process a terminal command and return the response
 */
function processCommand(input: string): string {
	const trimmed = input.trim();
	const parts = trimmed.split(' ');
	const commandName = parts[0].toLowerCase();
	const args = parts.slice(1).join(' ');
	
	// Handle 'ask' command specially
	if (commandName === 'ask' && args) {
		return `ChatBot: You asked: "${args}"
I'm a demo chatbot. In a real implementation, I would process your question and provide a helpful response!`;
	}
	
	// Handle regular commands
	const command = commands[commandName];
	if (command) {
		return command.execute(args);
	}
	
	// Command not found
	return `Command not found: ${commandName}
Type 'help' for available commands.`;
}

/**
 * Get list of available commands
 */
function getAvailableCommands(): Command[] {
	return Object.values(commands);
}

export const terminalCommands = {
	processCommand,
	getAvailableCommands
};