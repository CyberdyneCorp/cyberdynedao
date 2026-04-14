import { contactMethods, type ContactMethod } from '$lib/data/contact';

export interface ContactViewModel {
	methods: ContactMethod[];
	openContact: (method: ContactMethod) => void;
}

export function createContactViewModel(
	methods: ContactMethod[] = contactMethods,
	opener: (url: string) => void = (url) => {
		if (typeof window !== 'undefined') window.open(url, '_blank');
	}
): ContactViewModel {
	return {
		methods,
		openContact: (m) => opener(m.link)
	};
}
