import { describe, it, expect } from 'vitest';
import { contactMethods } from '../contact';
import { teamMembers } from '../team';
import { productSuite } from '../products';
import { serviceSections, workflowSteps, whyCyberdynePoints } from '../services';
import {
	problemPoints,
	solutionOfferings,
	targetUsers,
	tokenomicsRows,
	tokenUtilityPoints,
	strategicAdvantages,
	flagshipProducts,
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

	it('productSuite includes full-width product', () => {
		expect(productSuite.some(p => p.fullWidth)).toBe(true);
		productSuite.forEach(p => expect(p.features.length).toBeGreaterThan(0));
	});

	it('serviceSections have at least one bullet each', () => {
		expect(serviceSections.length).toBeGreaterThan(0);
		serviceSections.forEach(s => expect(s.bullets.length).toBeGreaterThan(0));
		expect(workflowSteps.length).toBeGreaterThan(0);
		expect(whyCyberdynePoints.length).toBeGreaterThan(0);
	});

	it('cyberdyne DAO content sections non-empty', () => {
		expect(problemPoints.length).toBeGreaterThan(0);
		expect(solutionOfferings.length).toBeGreaterThan(0);
		expect(targetUsers.length).toBeGreaterThan(0);
		expect(tokenomicsRows.length).toBe(5);
		expect(tokenUtilityPoints.length).toBeGreaterThan(0);
		expect(strategicAdvantages.length).toBeGreaterThan(0);
		expect(flagshipProducts.length).toBeGreaterThan(0);
		expect(exampleEconomics.length).toBe(4);
		expect(roadmapPhases.length).toBe(5);
		roadmapPhases.forEach(p => expect(p.items.length).toBeGreaterThan(0));
	});

	it('liquidityPositions covers in-range and out-of-range', () => {
		const statuses = new Set(liquidityPositions.map(p => p.status));
		expect(statuses.has('in-range')).toBe(true);
		expect(statuses.has('out-of-range')).toBe(true);
	});
});
