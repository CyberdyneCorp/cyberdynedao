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
