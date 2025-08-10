export interface NavItem {
	name: string;
	icon: string;
}

export const navItems: NavItem[] = [
	{ name: 'Cyberdyne', icon: '/assets/cyberdyne_logo.svg' },
	{ name: 'Blog', icon: '/assets/read.svg' },
	{ name: 'Investments', icon: '/assets/crypto_icon.svg' },
	{ name: 'Watch', icon: '/assets/watch.svg' },
	{ name: 'Contact Us', icon: '/assets/contact.svg' },
	{ name: 'Learn', icon: '/assets/study_icon.svg' },
	{ name: 'DAO', icon: '/assets/blockchain_icon.svg' },
	{ name: 'Products', icon: '/assets/products_icon.svg' },
	{ name: 'Team', icon: '/assets/the_team.svg' },
	{ name: 'Marketplace', icon: '/assets/marketplace_icon.svg' }
];

export const viewMap: { [key: string]: any } = {
	'Marketplace': 'shop',
	'Blog': 'read',
	'Investments': 'investments',
	'Watch': 'watch',
	'Learn': 'listen',
	'Cyberdyne': 'substack',
	'Contact Us': 'contact',
	'DAO': 'dao',
	'Products': 'products',
	'Team': 'team'
};