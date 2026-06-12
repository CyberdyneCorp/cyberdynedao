export interface NavItem {
	name: string;
	mobileLabel?: string;
	icon: string;
	/** i18n key for the launcher label (see `$lib/i18n` `nav.*`). */
	i18nKey: string;
}

export const navItems: NavItem[] = [
	{ name: 'Cyberdyne', mobileLabel: 'Cyber', icon: '/assets/cyberdyne_logo.svg', i18nKey: 'nav.cyberdyne' },
	{ name: 'Blog', icon: '/assets/read.svg', i18nKey: 'nav.blog' },
	{ name: 'Investments', mobileLabel: 'Invest', icon: '/assets/crypto_icon.svg', i18nKey: 'nav.investments' },
	{ name: 'Services', mobileLabel: 'Service', icon: '/assets/services_icon.svg', i18nKey: 'nav.services' },
	{ name: 'Contact Us', mobileLabel: 'Contact', icon: '/assets/contact.svg', i18nKey: 'nav.contact' },
	{ name: 'Learn', icon: '/assets/study_icon.svg', i18nKey: 'nav.learn' },
	{ name: 'DAO', icon: '/assets/blockchain_icon.svg', i18nKey: 'nav.dao' },
	{ name: 'Products', mobileLabel: 'Product', icon: '/assets/products_icon.svg', i18nKey: 'nav.products' },
	{ name: 'Team', icon: '/assets/the_team.svg', i18nKey: 'nav.team' },
	{ name: 'Marketplace', mobileLabel: 'Market', icon: '/assets/marketplace_icon.svg', i18nKey: 'nav.marketplace' },
	{ name: 'MATLAB', icon: '/assets/matlab_icon.svg', i18nKey: 'nav.matlab' },
	{ name: 'Agent', icon: '/assets/agent_icon.svg', i18nKey: 'nav.agent' },
	{ name: 'Cyberflies', mobileLabel: 'Meets', icon: '/assets/cyberflies_icon.svg', i18nKey: 'nav.cyberflies' },
	{ name: 'Python', icon: '/assets/python_icon.svg', i18nKey: 'nav.python' }
];

export const viewMap: { [key: string]: any } = {
	'Marketplace': 'shop',
	'Blog': 'read',
	'Investments': 'investments',
	'Services': 'services',
	'Learn': 'courses',
	'Admin': 'admin',
	'System Admin': 'sysadmin',
	'Cyberdyne': 'cyberdyne',
	'Contact Us': 'contact',
	'DAO': 'dao',
	'Products': 'products',
	'Team': 'team',
	'MATLAB': 'matlab',
	'Agent': 'agent',
	'Cyberflies': 'cyberflies',
	'Python': 'interpreter'
};