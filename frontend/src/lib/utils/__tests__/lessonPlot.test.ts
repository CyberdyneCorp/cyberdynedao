import { describe, expect, it } from 'vitest';
import {
	splitPlotSegments,
	compileExpr,
	parsePlot,
	resolvePlot,
	plotIs3d,
	plotControls,
	normalizeMathBlocks,
	stripKeepMarkers
} from '../lessonPlot';

// The downstream MarkdownPreview protects display math with this exact regex —
// it only matches `$$` that is followed by a newline.
const BLOCK_MATH = /\$\$\n([\s\S]*?)\n?\$\$/g;
function countMathBlocks(md: string): number {
	return [...md.matchAll(BLOCK_MATH)].length;
}

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
		expect(compileExpr('2 + 3 * 4')()).toBe(14);
		expect(compileExpr('(2 + 3) * 4')()).toBe(20);
	});
	it('resolves variables from the scope', () => {
		expect(compileExpr('x^2')({ x: 3 })).toBe(9);
		expect(compileExpr('-x + 1')({ x: 5 })).toBe(-4);
		expect(compileExpr('a*t')({ a: 2, t: 4 })).toBe(8);
	});
	it('supports functions and constants', () => {
		expect(compileExpr('sin(x)')({ x: 0 })).toBeCloseTo(0);
		expect(compileExpr('cos(0)')()).toBe(1);
		expect(compileExpr('sqrt(x)')({ x: 16 })).toBe(4);
		expect(compileExpr('pi')()).toBeCloseTo(Math.PI);
		expect(compileExpr('rad(180)')()).toBeCloseTo(Math.PI);
	});
	it('supports multi-arg functions and arity checks', () => {
		expect(compileExpr('min(3, 7, 2)')()).toBe(2);
		expect(compileExpr('max(3, 7, 2)')()).toBe(7);
		expect(compileExpr('pow(2, 10)')()).toBe(1024);
		expect(compileExpr('clamp(15, 0, 10)')()).toBe(10);
		expect(compileExpr('if(x > 0, 1, -1)')({ x: -4 })).toBe(-1);
		expect(() => compileExpr('clamp(1, 2)')()).toThrow();
	});
	it('supports comparison and logic operators (1/0)', () => {
		expect(compileExpr('3 > 2')()).toBe(1);
		expect(compileExpr('3 <= 2')()).toBe(0);
		expect(compileExpr('(1 > 0) && (2 > 5)')()).toBe(0);
		expect(compileExpr('(1 > 0) || (2 > 5)')()).toBe(1);
		expect(compileExpr('!0')()).toBe(1);
	});
	it('throws on unknown names / bad input (no eval)', () => {
		expect(() => compileExpr('foo(x)')({ x: 1 })).toThrow();
		expect(() => compileExpr('2 +')()).toThrow();
		expect(() => compileExpr('nope')()).toThrow();
	});
});

describe('normalizeMathBlocks (display-math fix)', () => {
	it('wraps a single inline $$…$$ block onto its own lines so it renders', () => {
		const out = normalizeMathBlocks('intro\n\n$$x = 1$$\n\nmore');
		expect(out).toContain('$$\nx = 1\n$$');
		expect(countMathBlocks(out)).toBe(1);
	});

	it('regression: two single-line $$…$$ blocks no longer swallow the text between them', () => {
		// Reproduces the Energy & momentum lesson: the renderer's regex would
		// otherwise span from the first block's closing $$ to the second's opening
		// $$, eating the "## Potential energy" heading and corrupting both blocks.
		const md = [
			'$$W_{net} = \\Delta K = \\tfrac{1}{2} m v_f^2.$$',
			'',
			'## Potential energy & conservation',
			'',
			'Near Earth $U = m g h$.',
			'',
			'$$\\tfrac{1}{2} m v^2 + m g h = C.$$'
		].join('\n');

		// Before: the renderer sees only ONE (bogus) block spanning the gap.
		expect(countMathBlocks(md)).toBe(1);

		const fixed = normalizeMathBlocks(md);
		// After: two clean blocks, and the heading survives between them.
		expect(countMathBlocks(fixed)).toBe(2);
		expect(fixed).toContain('## Potential energy & conservation');
		expect(fixed).toContain('$$\nW_{net} = \\Delta K = \\tfrac{1}{2} m v_f^2.\n$$');
		expect(fixed).toContain('$$\n\\tfrac{1}{2} m v^2 + m g h = C.\n$$');
	});

	it('is idempotent on already-normalized blocks and leaves inline $…$ alone', () => {
		const already = 'a $x$ b\n\n$$\ny = 2\n$$\n';
		expect(normalizeMathBlocks(already)).toContain('$$\ny = 2\n$$');
		expect(normalizeMathBlocks('only inline $a+b$ here')).toBe('only inline $a+b$ here');
	});
});

describe('stripKeepMarkers (do-not-translate spans)', () => {
	it('removes the markers and keeps the inner text', () => {
		expect(stripKeepMarkers('Diga [[keep]]the pipeline[[/keep]] aqui.')).toBe(
			'Diga the pipeline aqui.'
		);
	});
	it('handles multiple spans and leaves normal text alone', () => {
		expect(stripKeepMarkers('[[keep]]push[[/keep]] e [[keep]]deploy[[/keep]]')).toBe(
			'push e deploy'
		);
		expect(stripKeepMarkers('no markers here')).toBe('no markers here');
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

describe('plotIs3d', () => {
	it('detects 3D from mode, surfaces, zRange, or z coords', () => {
		expect(plotIs3d({ functions: [{ expr: 'x^2' }] })).toBe(false);
		expect(plotIs3d({ mode: '3d' })).toBe(true);
		expect(plotIs3d({ surfaces: [{ expr: 'x^2+y^2' }] })).toBe(true);
		expect(plotIs3d({ zRange: [0, 5] })).toBe(true);
		expect(plotIs3d({ points: [{ x: 1, y: 2, z: 3 }] })).toBe(true);
		expect(plotIs3d({ parametric: [{ x: 'cos(t)', y: 'sin(t)', z: 't', range: [0, 6] }] })).toBe(
			true
		);
	});
});

describe('resolvePlot (2D)', () => {
	it('samples a function and computes bounds', () => {
		const r = resolvePlot({ functions: [{ expr: 'x^2', label: 'parabola' }], xRange: [-2, 2] });
		expect(r.is3d).toBe(false);
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
		expect(r.vectors[0].tip).toEqual([3, 4]);
		expect(r.vectors[0].label).toBe('F');
		expect(r.equal).toBe(true);
	});
	it('samples a parametric curve', () => {
		const r = resolvePlot({
			parametric: [{ x: 'cos(t)', y: 'sin(t)', range: [0, 6.283], samples: 40 }]
		});
		expect(r.curves[0].points.length).toBe(41);
	});
});

describe('resolvePlot (animation & scope)', () => {
	it('places an expression-driven point using the current scope', () => {
		const spec = {
			animate: { param: 't', range: [0, 5] },
			points: [{ xExpr: '2*t', y: 1, trail: true, color: '#000' }] as const
		};
		const at0 = resolvePlot(spec as never, { t: 0 });
		const at2 = resolvePlot(spec as never, { t: 2 });
		expect(at0.points[0].x).toBe(0);
		expect(at2.points[0].x).toBe(4);
		// trail is added as an extra (non-legend) dashed curve
		expect(at2.curves.some((c) => c.dashed && c.legend === false)).toBe(true);
	});
});

describe('resolvePlot (3D)', () => {
	it('projects a surface into depth-sorted polygons', () => {
		const r = resolvePlot({ surfaces: [{ expr: 'x^2 + y^2', samples: 6 }] }, { azimuth: 35, elevation: 25 });
		expect(r.is3d).toBe(true);
		expect(r.polys.length).toBe(36); // 6 x 6 quads
		expect(r.equal).toBe(true);
		expect(r.labels.map((l) => l.text)).toEqual(['x', 'y', 'z']);
	});
	it('projects a 3D parametric curve', () => {
		const r = resolvePlot({
			parametric: [{ x: 'cos(t)', y: 'sin(t)', z: 't', range: [0, 6.283], samples: 30 }]
		});
		expect(r.is3d).toBe(true);
		expect(r.curves[0].points.length).toBe(31);
	});
});

describe('plotControls', () => {
	it('emits a slider for the animation param', () => {
		const { sliders, animateParam } = plotControls({ animate: { param: 't', range: [0, 5] } });
		expect(animateParam).toBe('t');
		expect(sliders[0]).toMatchObject({ name: 't', min: 0, max: 5, kind: 'param' });
	});
	it('emits named control sliders with defaults', () => {
		const { sliders } = plotControls({ controls: [{ name: 'v0', range: [1, 10], value: 4 }] });
		expect(sliders[0]).toMatchObject({ name: 'v0', value: 4, kind: 'control' });
	});
	it('adds rotate/tilt camera sliders for 3D specs', () => {
		const { sliders } = plotControls({ mode: '3d' });
		expect(sliders.map((s) => s.name)).toEqual(['azimuth', 'elevation']);
		expect(sliders[0].kind).toBe('camera');
	});
	it('omits camera sliders when the camera is locked', () => {
		const { sliders } = plotControls({ mode: '3d', lockCamera: true });
		expect(sliders).toHaveLength(0);
	});
});
