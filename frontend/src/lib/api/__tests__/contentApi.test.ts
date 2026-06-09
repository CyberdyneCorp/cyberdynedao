import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import {
	fetchCyberdynePage,
	fetchServicesPage,
	type CyberdynePagePayload,
	type ServicesPagePayload
} from '../contentApi';

type FetchMock = ReturnType<typeof vi.fn>;

function mockJsonOnce(status: number, body: unknown): void {
	(globalThis.fetch as unknown as FetchMock).mockResolvedValueOnce(
		new Response(JSON.stringify(body), {
			status,
			headers: { 'content-type': 'application/json' }
		})
	);
}

function rejectOnce(): void {
	(globalThis.fetch as unknown as FetchMock).mockRejectedValueOnce(new Error('network down'));
}

beforeEach(() => {
	globalThis.fetch = vi.fn() as unknown as typeof fetch;
});

afterEach(() => {
	vi.restoreAllMocks();
});

// A cyberdyne payload as the backend still serves it — including the
// Amini-overlapping geospatial and identity domains, the Sovereign-AI
// audience, and the Foundations / Geospatial Cluster / Sovereign Scale
// roadmap phases.
const API_CYBERDYNE: CyberdynePagePayload = {
	heroTagline: 'hero',
	introLead: 'lead',
	introBullets: ['a'],
	domains: [
		{ id: 'geospatial', name: 'Geospatial Intelligence', icon: '🌍', palette: 'green', tagline: 't', projects: ['CyberSTAC'], status: 'shipping' },
		{ id: 'identity', name: 'Identity & Platform', icon: '🔐', palette: 'red', tagline: 't', projects: ['CyberdyneAuth'], status: 'live' },
		{ id: 'ai-knowledge', name: 'AI Knowledge Systems', icon: '🧠', palette: 'purple', tagline: 't', projects: ['OrgPilot'], status: 'active' }
	],
	beliefs: [{ title: 'b', description: 'd' }],
	targetUsers: [
		{ name: 'Builders', description: 'd' },
		{ name: 'Sovereign-AI buyers', description: 'DFIs, ministries' },
		{ name: 'Token holders', description: 'd' }
	],
	tokenomicsRows: [],
	tokenUtilityPoints: [],
	exampleEconomics: [],
	roadmapPhases: [
		{ id: 'phase-1', title: 'Phase 1 · Foundations', subtitle: 's', status: 'shipped', color: 'green', items: [] },
		{ id: 'phase-2', title: 'Phase 2 · Geospatial Cluster', subtitle: 's', status: 'shipping', color: 'blue', items: [] },
		{ id: 'phase-3', title: 'Phase 3 · DAO + Dividends', subtitle: 's', status: 'active', color: 'purple', items: [] },
		{ id: 'phase-4', title: 'Phase 4 · Apps & Games', subtitle: 's', status: 'active', color: 'orange', items: [] },
		{ id: 'phase-5', title: 'Phase 5 · Sovereign Scale', subtitle: 's', status: 'planned', color: 'red', items: [] }
	],
	closingHeadline: 'h',
	closingBody: 'b'
};

describe('contentApi — Amini-overlap sanitization', () => {
	it('strips the geospatial and identity domains from the API response', async () => {
		mockJsonOnce(200, API_CYBERDYNE);
		const page = await fetchCyberdynePage();
		expect(page.domains.map((d) => d.id)).toEqual(['ai-knowledge']);
		expect(page.domains.some((d) => d.id === 'geospatial' || d.id === 'identity')).toBe(false);
	});

	it('strips the Sovereign-AI audience from the API response', async () => {
		mockJsonOnce(200, API_CYBERDYNE);
		const page = await fetchCyberdynePage();
		expect(page.targetUsers.map((u) => u.name)).toEqual(['Builders', 'Token holders']);
	});

	it('drops the foundations/geospatial/sovereign roadmap phases and re-numbers the survivors', async () => {
		mockJsonOnce(200, API_CYBERDYNE);
		const page = await fetchCyberdynePage();
		expect(page.roadmapPhases.map((p) => p.id)).toEqual(['phase-3', 'phase-4']);
		// Titles must stay sequential despite the removed phases.
		expect(page.roadmapPhases.map((p) => p.title)).toEqual([
			'Phase 1 · DAO + Dividends',
			'Phase 2 · Apps & Games'
		]);
	});

	it('keeps the static fallback clean when the API is unreachable', async () => {
		rejectOnce();
		const page = await fetchCyberdynePage();
		expect(page.domains.some((d) => d.id === 'geospatial' || d.id === 'identity')).toBe(false);
		expect(page.targetUsers.some((u) => /sovereign/i.test(u.name))).toBe(false);
		expect(page.roadmapPhases.some((p) => /geospatial|sovereign/i.test(p.title))).toBe(false);
		// Surviving phases are still sequentially numbered.
		const numbers = page.roadmapPhases.map((p) => p.title.match(/^Phase\s+(\d+)/)?.[1]);
		expect(numbers).toEqual(numbers.map((_, i) => String(i + 1)));
	});

	it('strips the Geospatial & Sovereign service section from the API response', async () => {
		const apiServices: ServicesPagePayload = {
			heroSubtitle: 'h',
			sections: [
				{ id: 'geospatial-sovereign', icon: '🌍', title: 'Geospatial & Sovereign AI', intro: 'i', bullets: [], palette: 'green', fullWidth: true },
				{ id: 'strategy', icon: '🎯', title: 'Strategy & Discovery', intro: 'i', bullets: [], palette: 'purple', fullWidth: false }
			],
			workflowSteps: [],
			whyPoints: [],
			ctaHeadline: 'h',
			ctaBody: 'b',
			ctaPills: []
		};
		mockJsonOnce(200, apiServices);
		const page = await fetchServicesPage();
		expect(page.sections.map((s) => s.id)).toEqual(['strategy']);
	});

	it('keeps the static services fallback free of the geospatial section', async () => {
		rejectOnce();
		const page = await fetchServicesPage();
		expect(page.sections.some((s) => s.id === 'geospatial-sovereign')).toBe(false);
	});
});
