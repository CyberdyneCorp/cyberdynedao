export interface NavItem {
	name: string;
	mobileLabel?: string;
	icon: string;
}

export const navItems: NavItem[] = [
	{ name: 'Cyberdyne', mobileLabel: 'Cyber', icon: '/assets/cyberdyne_logo.svg' },
	{ name: 'Blog', icon: '/assets/read.svg' },
	{ name: 'Investments', mobileLabel: 'Invest', icon: '/assets/crypto_icon.svg' },
	{ name: 'Services', mobileLabel: 'Service', icon: '/assets/services_icon.svg' },
	{ name: 'Contact Us', mobileLabel: 'Contact', icon: '/assets/contact.svg' },
	{ name: 'Learn', icon: '/assets/study_icon.svg' },
	{ name: 'DAO', icon: '/assets/blockchain_icon.svg' },
	{ name: 'Products', mobileLabel: 'Product', icon: '/assets/products_icon.svg' },
	{ name: 'Team', icon: '/assets/the_team.svg' },
	{ name: 'Marketplace', mobileLabel: 'Market', icon: '/assets/marketplace_icon.svg' }
];

export const viewMap: { [key: string]: any } = {
	'Marketplace': 'shop',
	'Blog': 'read',
	'Investments': 'investments',
	'Services': 'services',
	'Learn': 'listen',
	'Cyberdyne': 'cyberdyne',
	'Contact Us': 'contact',
	'DAO': 'dao',
	'Products': 'products',
	'Team': 'team'
};