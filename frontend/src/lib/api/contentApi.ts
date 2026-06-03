/**
 * Cyberdyne backend client — content endpoints.
 *
 * Loads team and cyberdyne page data from `${VITE_BACKEND_API_URL}/api/v1/content/*`.
 * Falls back to the local static data files on any error (network down,
 * 5xx, schema mismatch) so the frontend keeps rendering during a
 * backend outage — the static fallback is by-design for one PR and
 * gets removed once the API has been live for a release cycle.
 *
 * Response shape is camelCase end-to-end; the backend serializes via
 * pydantic alias_generator=to_camel.
 */

import type { TeamMember } from '$lib/data/team';
import { teamMembers as staticTeamMembers } from '$lib/data/team';
import {
	beliefs as staticBeliefs,
	closingBody as staticClosingBody,
	closingHeadline as staticClosingHeadline,
	domains as staticDomains,
	exampleEconomics as staticExampleEconomics,
	heroTagline as staticHeroTagline,
	introBullets as staticIntroBullets,
	introLead as staticIntroLead,
	roadmapPhases as staticRoadmapPhases,
	targetUsers as staticTargetUsers,
	tokenUtilityPoints as staticTokenUtilityPoints,
	tokenomicsRows as staticTokenomicsRows,
	type Domain,
	type Palette,
	type RoadmapPhase,
	type TokenomicsRow
} from '$lib/data/cyberdyne';

const API_BASE = (import.meta.env.VITE_BACKEND_API_URL ?? '').replace(/\/+$/, '');

/**
 * Shape returned by the team list endpoint. Mirrors the backend's
 * `TeamMemberResponse` exactly; same fields the static data file uses
 * minus the `image` rename (the API field is `imageUrl`).
 */
interface ApiTeamMember {
	id: string;
	name: string;
	title: string;
	imageUrl: string;
	bio: string;
	tags: string[];
	palette: TeamMember['palette'];
}

function apiTeamMemberToTeamMember(api: ApiTeamMember): TeamMember {
	return {
		id: api.id,
		name: api.name,
		title: api.title,
		image: api.imageUrl,
		bio: api.bio,
		tags: api.tags,
		palette: api.palette
	};
}

/**
 * Shape returned by the cyberdyne page endpoint. Every field maps 1:1
 * to a named export from `cyberdyne.ts` — no rename, just bundled in
 * a single response so the page renders in one round-trip.
 */
export interface CyberdynePagePayload {
	heroTagline: string;
	introLead: string;
	introBullets: string[];
	domains: Domain[];
	beliefs: { title: string; description: string }[];
	targetUsers: { name: string; description: string }[];
	tokenomicsRows: TokenomicsRow[];
	tokenUtilityPoints: string[];
	exampleEconomics: { label: string; value: string }[];
	roadmapPhases: RoadmapPhase[];
	closingHeadline: string;
	closingBody: string;
}

const STATIC_CYBERDYNE_PAGE: CyberdynePagePayload = {
	heroTagline: staticHeroTagline,
	introLead: staticIntroLead,
	introBullets: [...staticIntroBullets],
	domains: [...staticDomains],
	beliefs: [...staticBeliefs],
	targetUsers: [...staticTargetUsers],
	tokenomicsRows: [...staticTokenomicsRows],
	tokenUtilityPoints: [...staticTokenUtilityPoints],
	exampleEconomics: [...staticExampleEconomics],
	roadmapPhases: [...staticRoadmapPhases],
	closingHeadline: staticClosingHeadline,
	closingBody: staticClosingBody
};

async function fetchJson<T>(path: string): Promise<T> {
	if (!API_BASE) {
		throw new Error('VITE_BACKEND_API_URL is not configured');
	}
	const response = await fetch(`${API_BASE}${path}`, {
		headers: { Accept: 'application/json' }
	});
	if (!response.ok) {
		throw new Error(`${path} returned ${response.status}`);
	}
	return (await response.json()) as T;
}

/**
 * Fetch the team list. Logs and falls back to the static data on
 * any error — the page keeps rendering even if the API is down.
 */
export async function fetchTeam(): Promise<TeamMember[]> {
	try {
		const api = await fetchJson<ApiTeamMember[]>('/api/v1/content/team');
		return api.map(apiTeamMemberToTeamMember);
	} catch (err) {
		console.warn('[contentApi] team fetch failed, using static fallback:', err);
		return staticTeamMembers;
	}
}

/**
 * Fetch the cyberdyne page bundle. Same fallback behaviour as the team
 * fetcher.
 */
export async function fetchCyberdynePage(): Promise<CyberdynePagePayload> {
	try {
		return await fetchJson<CyberdynePagePayload>('/api/v1/content/cyberdyne');
	} catch (err) {
		console.warn('[contentApi] cyberdyne fetch failed, using static fallback:', err);
		return STATIC_CYBERDYNE_PAGE;
	}
}

// Re-export the palette type from the cyberdyne data file for
// convenience — callers that already import from $lib/data/cyberdyne
// can keep doing so; only the API consumer needs the Palette name.
export type { Palette };


// ── Phase 2 fetchers ────────────────────────────────────────────────


import type { ProductEntry, ProductStatus } from '$lib/data/products';
import { productSuite as staticProductSuite } from '$lib/data/products';

interface ApiProject {
	id: string;
	name: string;
	icon: string;
	description: string;
	features: string[];
	extraFeatures: string[] | null;
	palette: ProductEntry['palette'];
	status: ProductStatus;
	fullWidth: boolean;
}

function apiProjectToProductEntry(api: ApiProject): ProductEntry {
	return {
		id: api.id,
		name: api.name,
		icon: api.icon,
		description: api.description,
		features: api.features,
		extraFeatures: api.extraFeatures ?? undefined,
		palette: api.palette,
		status: api.status,
		fullWidth: api.fullWidth
	};
}

// Products hidden from the Products view for now, regardless of whether
// the backend still returns them. Matched on the normalized name/id so a
// rename or id change on the backend doesn't silently re-surface them.
const HIDDEN_PRODUCT_KEYS = new Set(['cyberspace', 'cyberdyneauth', 'cyberstac', 'cybergeopy']);

function isHiddenProduct(p: ProductEntry): boolean {
	const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
	return HIDDEN_PRODUCT_KEYS.has(norm(p.id)) || HIDDEN_PRODUCT_KEYS.has(norm(p.name));
}

export async function fetchProjects(): Promise<ProductEntry[]> {
	try {
		const api = await fetchJson<ApiProject[]>('/api/v1/content/projects');
		return api.map(apiProjectToProductEntry).filter((p) => !isHiddenProduct(p));
	} catch (err) {
		console.warn('[contentApi] projects fetch failed, using static fallback:', err);
		return staticProductSuite.filter((p) => !isHiddenProduct(p));
	}
}


import type {
	ServiceSection as StaticServiceSection,
	ServicePalette
} from '$lib/data/services';
import {
	heroSubtitle as staticServicesHero,
	serviceSections as staticServiceSections,
	workflowSteps as staticWorkflowSteps,
	whyCyberdynePoints as staticWhyPoints,
	ctaHeadline as staticServicesCtaHeadline,
	ctaBody as staticServicesCtaBody,
	ctaPills as staticServicesCtaPills
} from '$lib/data/services';

export interface ServicesPagePayload {
	sections: StaticServiceSection[];
	heroSubtitle: string;
	workflowSteps: { title: string; description: string }[];
	whyPoints: { title: string; description: string }[];
	ctaHeadline: string;
	ctaBody: string;
	ctaPills: string[];
}

interface ApiServiceSection {
	id: string;
	icon: string;
	title: string;
	intro: string;
	bullets: { title: string; description: string }[];
	palette: ServicePalette;
	fullWidth: boolean;
}

interface ApiServicesPage {
	sections: ApiServiceSection[];
	heroSubtitle: string;
	workflowSteps: { title: string; description: string }[];
	whyPoints: { title: string; description: string }[];
	ctaHeadline: string;
	ctaBody: string;
	ctaPills: string[];
}

const STATIC_SERVICES_PAGE: ServicesPagePayload = {
	sections: staticServiceSections.map((s) => ({ ...s, fullWidth: s.fullWidth ?? false })),
	heroSubtitle: staticServicesHero,
	workflowSteps: [...staticWorkflowSteps],
	whyPoints: [...staticWhyPoints],
	ctaHeadline: staticServicesCtaHeadline,
	ctaBody: staticServicesCtaBody,
	ctaPills: [...staticServicesCtaPills]
};

export async function fetchServicesPage(): Promise<ServicesPagePayload> {
	try {
		const api = await fetchJson<ApiServicesPage>('/api/v1/content/services');
		return {
			sections: api.sections.map((s) => ({
				id: s.id,
				icon: s.icon,
				title: s.title,
				intro: s.intro,
				bullets: s.bullets,
				palette: s.palette,
				fullWidth: s.fullWidth
			})),
			heroSubtitle: api.heroSubtitle,
			workflowSteps: api.workflowSteps,
			whyPoints: api.whyPoints,
			ctaHeadline: api.ctaHeadline,
			ctaBody: api.ctaBody,
			ctaPills: api.ctaPills
		};
	} catch (err) {
		console.warn('[contentApi] services fetch failed, using static fallback:', err);
		return STATIC_SERVICES_PAGE;
	}
}


import type { ContactMethod as StaticContactMethod } from '$lib/data/contact';
import { contactIntro as staticContactIntro, contactMethods as staticContactMethods } from '$lib/data/contact';

export interface ContactPagePayload {
	methods: StaticContactMethod[];
	intro: { headline: string; body: string };
}

interface ApiContactMethod {
	id: string;
	name: string;
	icon: string;
	description: string;
	action: string;
	link: string;
	brandSolid: string;
	brandHover: string;
	brandRgb: string;
	tagline: string;
}

interface ApiContactPage {
	methods: ApiContactMethod[];
	intro: { headline: string; body: string };
}

function apiContactMethodToStatic(api: ApiContactMethod): StaticContactMethod {
	return {
		id: api.id,
		name: api.name,
		icon: api.icon,
		description: api.description,
		action: api.action,
		link: api.link,
		colorPalette: { solid: api.brandSolid, hover: api.brandHover, rgb: api.brandRgb },
		tagline: api.tagline
	};
}

const STATIC_CONTACT_PAGE: ContactPagePayload = {
	methods: [...staticContactMethods],
	intro: { ...staticContactIntro }
};

export async function fetchContactPage(): Promise<ContactPagePayload> {
	try {
		const api = await fetchJson<ApiContactPage>('/api/v1/content/contact');
		return {
			methods: api.methods.map(apiContactMethodToStatic),
			intro: api.intro
		};
	} catch (err) {
		console.warn('[contentApi] contact fetch failed, using static fallback:', err);
		return STATIC_CONTACT_PAGE;
	}
}


export interface AskSubmission {
	name: string;
	email: string;
	body: string;
	channel?: 'contact_form' | 'marketplace_service_inquiry' | 'chat_agent_handoff';
	productSlug?: string | null;
	sourceUrl?: string | null;
	captchaToken: string;
}

export async function postAsk(submission: AskSubmission): Promise<{ ok: boolean; error?: string }> {
	if (!API_BASE) {
		// In dev with no backend, pretend the submission succeeded so the
		// UI flow can be exercised. A console warn flags it.
		console.warn('[contentApi] postAsk skipped — VITE_BACKEND_API_URL not configured');
		return { ok: true };
	}
	try {
		const response = await fetch(`${API_BASE}/api/v1/asks`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
			body: JSON.stringify({
				name: submission.name,
				email: submission.email,
				body: submission.body,
				channel: submission.channel ?? 'contact_form',
				productSlug: submission.productSlug ?? null,
				sourceUrl: submission.sourceUrl ?? null,
				captchaToken: submission.captchaToken
			})
		});
		if (response.status === 201) {
			return { ok: true };
		}
		const detail = (await response.json().catch(() => null)) as { detail?: unknown } | null;
		const msg = typeof detail?.detail === 'string' ? detail.detail : `HTTP ${response.status}`;
		return { ok: false, error: msg };
	} catch (err) {
		console.warn('[contentApi] postAsk failed:', err);
		return { ok: false, error: err instanceof Error ? err.message : 'unknown error' };
	}
}


// ── Phase 3 fetchers (blog) ─────────────────────────────────────────


export interface BlogPostSummary {
	id: string;
	slug: string;
	title: string;
	excerpt: string;
	categorySlug: string | null;
	tags: string[];
	status: 'draft' | 'published';
	createdAt: string;
	publishedAt: string | null;
}

export interface BlogPostDetail extends BlogPostSummary {
	bodyMd: string;
}

export interface BlogPostList {
	items: BlogPostSummary[];
	total: number;
	page: number;
	pageSize: number;
}

export async function fetchBlogPosts(
	options: { category?: string; tag?: string; page?: number; pageSize?: number } = {}
): Promise<BlogPostList> {
	const params = new URLSearchParams();
	if (options.category) params.set('category', options.category);
	if (options.tag) params.set('tag', options.tag);
	params.set('page', String(options.page ?? 1));
	params.set('pageSize', String(options.pageSize ?? 20));
	try {
		return await fetchJson<BlogPostList>(`/api/v1/blog/posts?${params}`);
	} catch (err) {
		console.warn('[contentApi] blog posts fetch failed:', err);
		// Empty list is a safe fallback — the blog is allowed to be empty.
		return { items: [], total: 0, page: 1, pageSize: 20 };
	}
}

export async function fetchBlogPost(slug: string): Promise<BlogPostDetail | null> {
	try {
		return await fetchJson<BlogPostDetail>(`/api/v1/blog/posts/${encodeURIComponent(slug)}`);
	} catch (err) {
		console.warn('[contentApi] blog post fetch failed:', err);
		return null;
	}
}


// ── Phase 5 fetchers (DAO treasury) ─────────────────────────────────


export interface DaoTokenBalance {
	symbol: string;
	name: string;
	address: string;
	balance: number;
	usdValue: number;
	change24hPct: number;
	icon: string;
}

export interface DaoAavePosition {
	symbol: string;
	aTokenBalance: number;
	variableDebt: number;
	supplyApy: number;
	borrowApy: number;
	usdValueSupplied: number;
	usdValueBorrowed: number;
}

export interface DaoUniswapPosition {
	positionId: string;
	poolId: string;
	token0Symbol: string;
	token1Symbol: string;
	token0Amount: number;
	token1Amount: number;
	feeTierBps: number;
	tickLower: number;
	tickUpper: number;
	inRange: boolean;
	usdValue: number;
	uncollectedFeesUsd: number;
}

export interface DaoTreasurySnapshot {
	treasuryAddress: string;
	chainId: number;
	snapshotAt: string;
	tokenBalances: DaoTokenBalance[];
	aavePositions: DaoAavePosition[];
	uniswapPositions: DaoUniswapPosition[];
	totalUsdValue: number;
}

export interface DaoOverview {
	snapshot: DaoTreasurySnapshot;
	holders: number;
}

export async function fetchDaoOverview(): Promise<DaoOverview | null> {
	try {
		return await fetchJson<DaoOverview>('/api/v1/dao/overview');
	} catch (err) {
		console.warn('[contentApi] dao overview fetch failed:', err);
		return null;
	}
}


// ── Phase 6 fetchers (marketplace) ──────────────────────────────────


import type { MarketplaceItem } from '$lib/types/components';
import { marketplaceItems as staticMarketplaceItems } from '$lib/data/shop';

interface ApiProduct {
	slug: string;
	type: 'service' | 'training' | 'license';
	title: string;
	descriptionMd: string;
	priceCents: number;
	currency: string;
	durationLabel: string;
	features: string[];
	category: string;
	subcategory: string | null;
	imageUrl: string;
	popular: boolean;
	status: 'available' | 'beta' | 'coming_soon' | 'retired';
	isPurchasable: boolean;
}

function apiProductToMarketplaceItem(api: ApiProduct): MarketplaceItem {
	const statusMap: Record<ApiProduct['status'], MarketplaceItem['status']> = {
		available: 'available',
		beta: 'beta',
		coming_soon: 'coming-soon',
		retired: 'available'
	};
	return {
		id: api.slug,
		title: api.title,
		description: api.descriptionMd,
		category: api.category as MarketplaceItem['category'],
		subcategory: api.subcategory ?? undefined,
		price: api.priceCents / 100,
		duration: api.durationLabel,
		features: api.features,
		popular: api.popular || undefined,
		image: api.imageUrl || '',
		status: statusMap[api.status] ?? 'available'
	};
}

export async function fetchMarketplaceItems(): Promise<MarketplaceItem[]> {
	try {
		const api = await fetchJson<ApiProduct[]>('/api/v1/marketplace/products');
		return api.map(apiProductToMarketplaceItem);
	} catch (err) {
		console.warn('[contentApi] marketplace fetch failed, using static fallback:', err);
		return staticMarketplaceItems;
	}
}
