export interface TeamMember {
	id: string;
	name: string;
	title: string;
	image: string;
	bio: string;
	tags: string[];
	palette: 'purple' | 'green' | 'orange' | 'blue';
}

export const teamMembers: TeamMember[] = [
	{
		id: 'giounona',
		name: 'Giounona Tzanidou',
		title: 'International Researcher',
		image: '/assets/team/Giounona.webp',
		bio: 'Our International Researcher, she is responsible for everything related to Mathematics and Artificial Intelligence.',
		tags: ['Mathematics', 'Artificial Intelligence', 'Machine Learning', 'Research'],
		palette: 'purple'
	},
	{
		id: 'bruno',
		name: 'Bruno Jessen',
		title: 'Code Wizard',
		image: '/assets/team/Bruno.webp',
		bio: 'Our "code wizard" programs in everything!',
		tags: ['C++', 'Java', 'Python', 'Solidity', 'Rust', 'Go', 'Verilog'],
		palette: 'green'
	},
	{
		id: 'rafael',
		name: 'Rafael Serpa',
		title: 'Creative Artist',
		image: '/assets/team/Rafael.webp',
		bio: 'Our Artist, responsible for visual creativity and game design.',
		tags: ['3D Modeling', 'Texturing', 'Concept Art', 'Game Design'],
		palette: 'orange'
	},
	{
		id: 'leonardo',
		name: 'Leonardo Araujo',
		title: 'Full-Stack Researcher',
		image: '/assets/team/Leonardo.webp',
		bio: "Does everything, and isn't good at anything. Machine Learning Researcher and Developer who also loves Surfing and Financial Markets.",
		tags: ['Machine Learning', 'Python', 'Solidity', 'C++', 'C#', 'Verilog', '🏄 Surfing', '📈 Finance'],
		palette: 'blue'
	}
];
