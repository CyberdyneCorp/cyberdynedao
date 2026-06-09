import { describe, it, expect } from 'vitest';
import { contactMethods } from '../contact';
import { teamMembers } from '../team';
import { productSuite } from '../products';
import { serviceSections, workflowSteps, whyCyberdynePoints } from '../services';
import {
	domains,
	beliefs,
	targetUsers,
	tokenomicsRows,
	tokenUtilityPoints,
	exampleEconomics,
	roadmapPhases
} from '../cyberdyne';
import { liquidityPositions } from '../investments';

describe('additional data fixtures', () => {
	it('contactMethods are non-empty and shaped correctly', () => {
		expect(contactMethods.length).toBeGreaterThan(0);
		contactMethods.forEach(c => {
			expect(c.id).toBeTruthy();
			expect(c.link).toMatch(/^https?:/);
			expect(c.colorPalette.solid).toMatch(/^#/);
		});
	});

	it('teamMembers cover all palettes used by TeamView', () => {
		expect(teamMembers.length).toBeGreaterThan(0);
		teamMembers.forEach(m => expect(m.tags.length).toBeGreaterThan(0));
	});

	it('productSuite entries each have features', () => {
		expect(productSuite.length).toBeGreaterThan(0);
		productSuite.forEach(p => expect(p.features.length).toBeGreaterThan(0));
	});

	it('serviceSections have at least one bullet each', () => {
		expect(serviceSections.length).toBeGreaterThan(0);
		serviceSections.forEach(s => expect(s.bullets.length).toBeGreaterThan(0));
		expect(workflowSteps.length).toBeGreaterThan(0);
		expect(whyCyberdynePoints.length).toBeGreaterThan(0);
	});

	it('cyberdyne DAO content sections non-empty', () => {
		expect(domains.length).toBeGreaterThan(0);
		domains.forEach(d => expect(d.projects.length).toBeGreaterThan(0));
		expect(beliefs.length).toBeGreaterThan(0);
		expect(targetUsers.length).toBeGreaterThan(0);
		expect(tokenomicsRows.length).toBe(5);
		expect(tokenUtilityPoints.length).toBeGreaterThan(0);
		expect(exampleEconomics.length).toBe(4);
		// Geospatial Cluster and Sovereign Scale phases were removed to avoid
		// overlap with Amini's space, leaving three.
		expect(roadmapPhases.length).toBe(3);
		roadmapPhases.forEach(p => expect(p.items.length).toBeGreaterThan(0));
	});

	it('liquidityPositions covers in-range and out-of-range', () => {
		const statuses = new Set(liquidityPositions.map(p => p.status));
		expect(statuses.has('in-range')).toBe(true);
		expect(statuses.has('out-of-range')).toBe(true);
	});
});
