export interface ContactMethod {
	id: string;
	name: string;
	icon: string;
	description: string;
	action: string;
	link: string;
	colorPalette: {
		solid: string;
		hover: string;
		rgb: string;
	};
	tagline: string;
}

export const contactMethods: ContactMethod[] = [
	{
		id: 'whatsapp',
		name: 'WhatsApp Bot',
		icon: '💬',
		description: 'AI support for your Web3 projects',
		action: 'Start Chatting',
		link: 'https://wa.me/1234567890?text=Hello%20Cyberdyne%20Team',
		colorPalette: { solid: '#25d366', hover: '#128c7e', rgb: '37, 211, 102' },
		tagline: '24/7 AI • INSTANT'
	},
	{
		id: 'discord',
		name: 'Discord Community',
		icon: '🎮',
		description: 'Join our vibrant developer community',
		action: 'Join Server',
		link: 'https://discord.gg/cyberdyne',
		colorPalette: { solid: '#5865f2', hover: '#4752c4', rgb: '88, 101, 242' },
		tagline: 'COMMUNITY • EXPERTS'
	}
];
