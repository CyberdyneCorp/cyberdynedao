import { describe, it, expect } from 'vitest';
import { TopModel } from '../top';

// Deterministic RNG so jitter is reproducible.
function seq(values: number[]) {
	let i = 0;
	return () => values[i++ % values.length];
}

describe('TopModel', () => {
	it('boots with the process roster', () => {
		const top = new TopModel(seq([0.5]));
		expect(top.processes.length).toBeGreaterThan(5);
		expect(top.processes.some((p) => p.command === 'top')).toBe(true);
	});

	it('render() includes the standard top header + columns', () => {
		const out = new TopModel(seq([0.5])).render();
		expect(out).toMatch(/top - up/);
		expect(out).toMatch(/Tasks:/);
		expect(out).toMatch(/%Cpu\(s\)/);
		expect(out).toMatch(/PID USER/);
	});

	it('tick() updates cpu values and keeps them sorted desc', () => {
		const top = new TopModel(seq([0.9, 0.1, 0.5, 0.2, 0.8, 0.3, 0.6, 0.4, 0.7, 0.0]));
		top.tick();
		const cpus = top.processes.map((p) => p.cpu);
		const sorted = [...cpus].sort((a, b) => b - a);
		expect(cpus).toEqual(sorted);
		expect(top.ticks).toBe(1);
	});

	it('cpu never goes negative', () => {
		const top = new TopModel(seq([0])); // always pulls jitter to the floor
		top.tick();
		expect(top.processes.every((p) => p.cpu >= 0)).toBe(true);
	});
});
