export interface NavItem {
	name: string;
	icon: string;
}

export const navItems: NavItem[] = [
	{ name: 'Substack', icon: '/assets/substack.svg' },
	{ name: 'Read', icon: '/assets/read.svg' },
	{ name: 'Investments', icon: '/assets/investments.svg' },
	{ name: 'Watch', icon: '/assets/watch.svg' },
	{ name: 'Contact Me', icon: '/assets/contact.svg' },
	{ name: 'Listen', icon: '/assets/listen.svg' },
	{ name: 'enigma', icon: '/assets/enigma.svg' },
	{ name: 'Shop', icon: '/assets/shop.svg' }
];

export const viewMap: { [key: string]: any } = {
	'Shop': 'shop',
	'Read': 'read',
	'Investments': 'investments',
	'Watch': 'watch',
	'Listen': 'listen',
	'Substack': 'substack',
	'Contact Me': 'contact',
	'enigma': 'enigma'
};