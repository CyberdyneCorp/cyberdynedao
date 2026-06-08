import { describe, expect, it } from 'vitest';
import { splitPlotSegments, compileExpr, parsePlot, resolvePlot } from '../lessonPlot';

describe('splitPlotSegments', () => {
	it('splits ```plot fences out of markdown, preserving order', () => {
		const body = 'intro\n```plot\n{"functions":[]}\n```\noutro';
		const segs = splitPlotSegments(body);
		expect(segs.map((s) => s.kind)).toEqual(['md', 'plot', 'md']);
		expect(segs[1].content.trim()).toBe('{"functions":[]}');
	});
	it('treats a plain body as one md segment', () => {
		expect(splitPlotSegments('just text')).toEqual([{ kind: 'md', content: 'just text' }]);
	});
	it('also recognises ```vectors fences', () => {
		const segs = splitPlotSegments('```vectors\n{"vectors":[]}\n```');
		expect(segs.map((s) => s.kind)).toEqual(['plot']);
	});
});

describe('compileExpr (safe evaluator)', () => {
	it('evaluates arithmetic with precedence', () => {
		expect(compileExpr('2 + 3 * 4')(0)).toBe(14);
		expect(compileExpr('(2 + 3) * 4')(0)).toBe(20);
	});
	it('handles the variable x, powers, and unary minus', () => {
		expect(compileExpr('x^2')(3)).toBe(9);
		expect(compileExpr('-x + 1')(5)).toBe(-4);
	});
	it('supports functions and constants', () => {
		expect(compileExpr('sin(x)')(0)).toBeCloseTo(0);
		expect(compileExpr('cos(0)')(0)).toBe(1);
		expect(compileExpr('sqrt(x)')(16)).toBe(4);
		expect(compileExpr('pi')(0)).toBeCloseTo(Math.PI);
	});
	it('throws on unknown names / bad input (no eval)', () => {
		expect(() => compileExpr('foo(x)')(1)).toThrow();
		expect(() => compileExpr('2 +')(0)).toThrow();
	});
});

describe('parsePlot', () => {
	it('parses valid JSON', () => {
		expect(parsePlot('{"title":"t"}')).toEqual({ title: 't' });
	});
	it('returns an error for invalid JSON', () => {
		expect(parsePlot('{nope')).toHaveProperty('error');
	});
});

describe('resolvePlot', () => {
	it('samples a function and computes bounds', () => {
		const r = resolvePlot({ functions: [{ expr: 'x^2', label: 'parabola' }], xRange: [-2, 2] });
		expect(r.curves).toHaveLength(1);
		expect(r.curves[0].points.length).toBeGreaterThan(50);
		expect(r.bounds.xmin).toBe(-2);
		expect(r.bounds.xmax).toBe(2);
		expect(r.curves[0].color).toBeTruthy();
	});
	it('captures a per-function error without throwing', () => {
		const r = resolvePlot({ functions: [{ expr: 'bogus(x)' }], xRange: [0, 1] });
		expect(r.error).toBeTruthy();
	});
	it('resolves vectors with a default origin and equal aspect', () => {
		const r = resolvePlot({ vectors: [{ x: 3, y: 4, label: 'F' }] });
		expect(r.vectors[0].from).toEqual([0, 0]);
		expect(r.vectors[0].label).toBe('F');
		expect(r.equal).toBe(true); // vectors-only spec defaults to equal aspect
	});
});
