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
		name: 'WhatsApp',
		icon: '💬',
		description: 'Quickest path to a human. Project enquiries, contracts, and quick technical questions.',
		action: 'Start Chatting',
		link: 'https://wa.me/1234567890?text=Hello%20Cyberdyne%20Team',
		colorPalette: { solid: '#25d366', hover: '#128c7e', rgb: '37, 211, 102' },
		tagline: 'Usually responds within hours'
	},
	{
		id: 'discord',
		name: 'Discord',
		icon: '🎮',
		description: 'Our open community — builders, researchers, and the curious. Drop in, lurk, ask questions.',
		action: 'Join Server',
		link: 'https://discord.gg/cyberdyne',
		colorPalette: { solid: '#5865f2', hover: '#4752c4', rgb: '88, 101, 242' },
		tagline: 'Community channel'
	},
	{
		id: 'github',
		name: 'GitHub',
		icon: '🛠️',
		description: 'Source for everything we ship. Open an issue, send a PR, or just browse the stack.',
		action: 'Visit Org',
		link: 'https://github.com/CyberdyneCorp',
		colorPalette: { solid: '#1f2937', hover: '#000000', rgb: '31, 41, 55' },
		tagline: 'Open source, by default'
	}
];

export const contactIntro = {
	headline: 'Let’s talk',
	body:
		'Whether it’s a contract, a collaboration, or a research partnership — pick the channel that fits. We read everything that lands.'
};
