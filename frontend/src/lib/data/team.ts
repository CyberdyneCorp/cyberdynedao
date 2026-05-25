export type TeamPalette = 'purple' | 'green' | 'orange' | 'blue';

export interface TeamMember {
	id: string;
	name: string;
	title: string;
	image: string;
	bio: string;
	tags: string[];
	palette: TeamPalette;
}

export const teamHeroTitle = 'About Us';
export const teamHeroBody =
	'A small builder collective of engineers, researchers and artists. We ship production software across geospatial intelligence, AI knowledge systems, identity, DeFi, and games — open by default, and built to outlive any single vendor.';

export const teamMembers: TeamMember[] = [
	{
		id: 'giounona',
		name: 'Giounona Tzanidou',
		title: 'International Researcher',
		image: '/assets/team/Giounona.webp',
		bio: 'Drives everything math-and-AI at Cyberdyne — from training pipelines to research collaborations.',
		tags: ['Mathematics', 'Artificial Intelligence', 'Machine Learning', 'Research'],
		palette: 'purple'
	},
	{
		id: 'bruno',
		name: 'Bruno Jessen',
		title: 'Code Wizard',
		image: '/assets/team/Bruno.webp',
		bio: 'Programs in everything. If it compiles or runs on-chain, Bruno has shipped a version of it.',
		tags: ['C++', 'Java', 'Python', 'Solidity', 'Rust', 'Go', 'Verilog'],
		palette: 'green'
	},
	{
		id: 'rafael',
		name: 'Rafael Serpa',
		title: 'Creative Artist',
		image: '/assets/team/Rafael.webp',
		bio: 'Visual creativity, 3D, and game design — the look and feel behind everything user-facing.',
		tags: ['3D Modeling', 'Texturing', 'Concept Art', 'Game Design'],
		palette: 'orange'
	},
	{
		id: 'leonardo',
		name: 'Leonardo Araujo',
		title: 'Full-Stack Researcher',
		image: '/assets/team/Leonardo.webp',
		bio: 'Does everything and isn\'t great at any of it. ML researcher / engineer who also loves surfing and financial markets.',
		tags: ['Machine Learning', 'Python', 'Solidity', 'C++', 'C#', 'Verilog', '🏄 Surfing', '📈 Finance'],
		palette: 'blue'
	}
];

export const teamCtaHeadline = 'Want to build with us?';
export const teamCtaBody =
	'Open to contracts, collaborations, and the occasional research partnership. The team is small on purpose — pick the channel that fits and we’ll read every message.';
export const teamCtaButton = 'Get in Touch';
