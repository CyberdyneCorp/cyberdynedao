/**
 * Lesson plots, vector diagrams, 3D surfaces & slider-driven animations —
 * a tiny, dependency-free engine.
 *
 * Authors embed a fenced ```plot (or ```vectors) block whose body is JSON.
 * This module is pure (no DOM): it splits the blocks out of markdown, parses
 * the spec, safely evaluates expressions over a variable *scope* (no
 * eval/Function — a shunting-yard tokenizer → RPN), samples curves and
 * surfaces, projects 3D → 2D, and computes bounds. `Plot.svelte` turns the
 * result into interactive SVG (sliders + play/pause).
 *
 * Expressions can reference any variable the scope provides — `x`/`y` for
 * functions and surfaces, a parametric `t`, plus any animation parameter or
 * named slider control — and support arithmetic, powers, comparison & logic
 * operators (`< <= > >= == != && || !`) and functions including
 * `sin cos tan asin acos atan sinh cosh tanh sqrt cbrt abs exp log ln log10
 * log2 sign floor ceil round deg rad pow mod atan2 hypot min max clamp if`.
 */

export type Scope = Record<string, number>;
export type Vec2 = [number, number];

export interface PlotFunction {
	expr: string;
	label?: string;
	color?: string;
}
export interface PlotParametric {
	x: string;
	y: string;
	z?: string;
	param?: string;
	range: [number, number];
	samples?: number;
	label?: string;
	color?: string;
}
export interface PlotSeries {
	points: number[][];
	label?: string;
	color?: string;
}
export interface PlotPoint {
	x?: number;
	y?: number;
	z?: number;
	xExpr?: string;
	yExpr?: string;
	zExpr?: string;
	label?: string;
	color?: string;
	size?: number;
	/** When the plot is animated, draw the path traced from the start to now. */
	trail?: boolean;
}
export interface PlotVector {
	x?: number;
	y?: number;
	z?: number;
	xExpr?: string;
	yExpr?: string;
	zExpr?: string;
	from?: number[];
	fromExpr?: string[];
	label?: string;
	color?: string;
}
export interface PlotSurface {
	expr: string; // z = f(x, y)
	xRange?: [number, number];
	yRange?: [number, number];
	samples?: number;
	color?: string;
	label?: string;
}
export interface PlotAnimation {
	param: string;
	range: [number, number];
	step?: number;
	fps?: number;
	loop?: boolean;
	label?: string;
}
export interface PlotControl {
	name: string;
	range: [number, number];
	step?: number;
	value?: number;
	label?: string;
}

export interface PlotSpec {
	title?: string;
	xLabel?: string;
	yLabel?: string;
	zLabel?: string;
	mode?: '2d' | '3d';
	xRange?: [number, number];
	yRange?: [number, number];
	zRange?: [number, number];
	functions?: PlotFunction[];
	parametric?: PlotParametric[];
	series?: PlotSeries[];
	points?: PlotPoint[];
	vectors?: PlotVector[];
	surfaces?: PlotSurface[];
	grid?: boolean;
	equal?: boolean;
	width?: number;
	height?: number;
	animate?: PlotAnimation;
	controls?: PlotControl[];
	/** 3D camera (degrees). Becomes interactive rotate/tilt sliders. */
	azimuth?: number;
	elevation?: number;
	lockCamera?: boolean;
}

export interface ResolvedCurve {
	points: Vec2[];
	label?: string;
	color: string;
	dashed?: boolean;
	width?: number;
	legend?: boolean;
}
export interface ResolvedPoint {
	x: number;
	y: number;
	label?: string;
	color: string;
	size: number;
}
export interface ResolvedVector {
	from: Vec2;
	tip: Vec2;
	label?: string;
	color: string;
}
export interface ResolvedPoly {
	points: Vec2[];
	fill: string;
	stroke: string;
}
export interface ResolvedLabel {
	x: number;
	y: number;
	text: string;
	color?: string;
}
export interface ResolvedPlot {
	title?: string;
	xLabel?: string;
	yLabel?: string;
	is3d: boolean;
	bounds: { xmin: number; xmax: number; ymin: number; ymax: number };
	polys: ResolvedPoly[];
	curves: ResolvedCurve[];
	guides: ResolvedCurve[];
	points: ResolvedPoint[];
	vectors: ResolvedVector[];
	labels: ResolvedLabel[];
	grid: boolean;
	equal: boolean;
	width: number;
	height: number;
	error?: string;
}

export type LessonSegment = { kind: 'md'; content: string } | { kind: 'plot'; content: string };

export interface SliderControl {
	name: string;
	min: number;
	max: number;
	step: number;
	value: number;
	label: string;
	kind: 'param' | 'control' | 'camera';
}

const PALETTE = ['#2563eb', '#dc2626', '#16a34a', '#9333ea', '#ea580c', '#0891b2'];

/** Split a lesson body into markdown and ```plot/```vectors segments, in order. */
export function splitPlotSegments(body: string): LessonSegment[] {
	const fence = /```(?:plot|vectors)\s*\n([\s\S]*?)```/g;
	const out: LessonSegment[] = [];
	let last = 0;
	let m: RegExpExecArray | null;
	while ((m = fence.exec(body)) !== null) {
		if (m.index > last) {
			const md = body.slice(last, m.index);
			if (md.trim()) out.push({ kind: 'md', content: md });
		}
		out.push({ kind: 'plot', content: m[1] });
		last = fence.lastIndex;
	}
	const tail = body.slice(last);
	if (tail.trim() || out.length === 0) out.push({ kind: 'md', content: tail });
	return out;
}

// ── Safe expression evaluator (shunting-yard → RPN; no eval) ─────────────────

type FnDef = { a: number | 'var'; f: (args: number[]) => number };
const FUNCS: Record<string, FnDef> = {
	sin: { a: 1, f: (a) => Math.sin(a[0]) },
	cos: { a: 1, f: (a) => Math.cos(a[0]) },
	tan: { a: 1, f: (a) => Math.tan(a[0]) },
	asin: { a: 1, f: (a) => Math.asin(a[0]) },
	acos: { a: 1, f: (a) => Math.acos(a[0]) },
	atan: { a: 1, f: (a) => Math.atan(a[0]) },
	sinh: { a: 1, f: (a) => Math.sinh(a[0]) },
	cosh: { a: 1, f: (a) => Math.cosh(a[0]) },
	tanh: { a: 1, f: (a) => Math.tanh(a[0]) },
	sqrt: { a: 1, f: (a) => Math.sqrt(a[0]) },
	cbrt: { a: 1, f: (a) => Math.cbrt(a[0]) },
	abs: { a: 1, f: (a) => Math.abs(a[0]) },
	exp: { a: 1, f: (a) => Math.exp(a[0]) },
	log: { a: 1, f: (a) => Math.log(a[0]) },
	ln: { a: 1, f: (a) => Math.log(a[0]) },
	log10: { a: 1, f: (a) => Math.log10(a[0]) },
	log2: { a: 1, f: (a) => Math.log2(a[0]) },
	sign: { a: 1, f: (a) => Math.sign(a[0]) },
	floor: { a: 1, f: (a) => Math.floor(a[0]) },
	ceil: { a: 1, f: (a) => Math.ceil(a[0]) },
	round: { a: 1, f: (a) => Math.round(a[0]) },
	deg: { a: 1, f: (a) => (a[0] * 180) / Math.PI },
	rad: { a: 1, f: (a) => (a[0] * Math.PI) / 180 },
	pow: { a: 2, f: (a) => a[0] ** a[1] },
	mod: { a: 2, f: (a) => ((a[0] % a[1]) + a[1]) % a[1] },
	atan2: { a: 2, f: (a) => Math.atan2(a[0], a[1]) },
	hypot: { a: 'var', f: (a) => Math.hypot(...a) },
	min: { a: 'var', f: (a) => Math.min(...a) },
	max: { a: 'var', f: (a) => Math.max(...a) },
	clamp: { a: 3, f: (a) => Math.min(Math.max(a[0], a[1]), a[2]) },
	if: { a: 3, f: (a) => (a[0] !== 0 ? a[1] : a[2]) }
};
const CONSTS: Record<string, number> = { pi: Math.PI, e: Math.E, tau: 2 * Math.PI };
const PREC: Record<string, number> = {
	'||': 1,
	'&&': 2,
	'==': 3,
	'!=': 3,
	'<': 4,
	'<=': 4,
	'>': 4,
	'>=': 4,
	'+': 5,
	'-': 5,
	'*': 6,
	'/': 6,
	'%': 6,
	'^': 7,
	neg: 8,
	not: 8
};
const RIGHT = new Set(['^', 'neg', 'not']);
const TWO = new Set(['<=', '>=', '==', '!=', '&&', '||']);

type Tok =
	| { t: 'num'; v: number }
	| { t: 'name'; v: string }
	| { t: 'op'; v: string }
	| { t: 'lparen' }
	| { t: 'rparen' }
	| { t: 'comma' };

function tokenize(src: string): Tok[] {
	const toks: Tok[] = [];
	let i = 0;
	while (i < src.length) {
		const c = src[i];
		if (c === ' ' || c === '\t' || c === '\n') {
			i++;
			continue;
		}
		if (/[0-9.]/.test(c)) {
			let j = i + 1;
			while (j < src.length && /[0-9.eE+-]/.test(src[j])) {
				if ((src[j] === '+' || src[j] === '-') && !/[eE]/.test(src[j - 1])) break;
				j++;
			}
			const numv = Number(src.slice(i, j));
			if (Number.isNaN(numv)) throw new Error(`bad number near "${src.slice(i, j)}"`);
			toks.push({ t: 'num', v: numv });
			i = j;
		} else if (/[a-zA-Z_]/.test(c)) {
			let j = i + 1;
			while (j < src.length && /[a-zA-Z0-9_]/.test(src[j])) j++;
			toks.push({ t: 'name', v: src.slice(i, j) });
			i = j;
		} else if (TWO.has(src.slice(i, i + 2))) {
			toks.push({ t: 'op', v: src.slice(i, i + 2) });
			i += 2;
		} else if ('+-*/%^<>!'.includes(c)) {
			toks.push({ t: 'op', v: c });
			i++;
		} else if (c === '(') {
			toks.push({ t: 'lparen' });
			i++;
		} else if (c === ')') {
			toks.push({ t: 'rparen' });
			i++;
		} else if (c === ',') {
			toks.push({ t: 'comma' });
			i++;
		} else {
			throw new Error(`unexpected character "${c}"`);
		}
	}
	return toks;
}

type RPN =
	| { k: 'num'; v: number }
	| { k: 'var'; v: string }
	| { k: 'op'; v: string }
	| { k: 'call'; v: string; n: number };
type OpStack = { t: 'op'; v: string } | { t: 'fn'; v: string } | { t: 'lparen' };

/** Compile `expr` into a function of a variable scope. Throws on invalid input. */
export function compileExpr(expr: string): (scope?: Scope) => number {
	const toks = tokenize(expr);
	const out: RPN[] = [];
	const ops: OpStack[] = [];
	const argc: number[] = [];
	let prev: Tok | null = null;
	for (let k = 0; k < toks.length; k++) {
		const tok = toks[k];
		if (tok.t === 'num') out.push({ k: 'num', v: tok.v });
		else if (tok.t === 'name') {
			if (toks[k + 1]?.t === 'lparen') {
				ops.push({ t: 'fn', v: tok.v });
				argc.push(1);
			} else out.push({ k: 'var', v: tok.v });
		} else if (tok.t === 'comma') {
			while (ops.length && ops[ops.length - 1].t !== 'lparen') out.push(asOp(ops.pop()!));
			if (!argc.length) throw new Error('misplaced comma');
			argc[argc.length - 1]++;
		} else if (tok.t === 'op') {
			let op = tok.v;
			const unary =
				!prev || prev.t === 'op' || prev.t === 'lparen' || prev.t === 'comma';
			if (unary && op === '-') op = 'neg';
			else if (unary && op === '+') {
				prev = tok;
				continue;
			} else if (unary && op === '!') op = 'not';
			while (ops.length) {
				const top = ops[ops.length - 1];
				if (top.t !== 'op') break;
				if (PREC[top.v] > PREC[op] || (PREC[top.v] === PREC[op] && !RIGHT.has(op)))
					out.push(asOp(ops.pop()!));
				else break;
			}
			ops.push({ t: 'op', v: op });
		} else if (tok.t === 'lparen') {
			ops.push({ t: 'lparen' });
		} else if (tok.t === 'rparen') {
			while (ops.length && ops[ops.length - 1].t !== 'lparen') out.push(asOp(ops.pop()!));
			if (!ops.length) throw new Error('mismatched parentheses');
			ops.pop(); // discard '('
			const top = ops[ops.length - 1];
			if (top && top.t === 'fn') {
				ops.pop();
				out.push({ k: 'call', v: top.v, n: argc.pop()! });
			}
		}
		prev = tok;
	}
	while (ops.length) {
		const o = ops.pop()!;
		if (o.t === 'lparen') throw new Error('mismatched parentheses');
		out.push(asOp(o));
	}
	return (scope: Scope = {}) => evalRPN(out, scope);
}

function asOp(o: OpStack): RPN {
	if (o.t === 'op') return { k: 'op', v: o.v };
	if (o.t === 'fn') return { k: 'call', v: o.v, n: 1 };
	throw new Error('mismatched parentheses');
}

function popNum(st: number[]): number {
	const v = st.pop();
	if (v === undefined) throw new Error('bad expression');
	return v;
}

function applyBin(op: string, a: number, b: number): number {
	switch (op) {
		case '+':
			return a + b;
		case '-':
			return a - b;
		case '*':
			return a * b;
		case '/':
			return a / b;
		case '%':
			return ((a % b) + b) % b;
		case '^':
			return a ** b;
		case '<':
			return a < b ? 1 : 0;
		case '<=':
			return a <= b ? 1 : 0;
		case '>':
			return a > b ? 1 : 0;
		case '>=':
			return a >= b ? 1 : 0;
		case '==':
			return a === b ? 1 : 0;
		case '!=':
			return a !== b ? 1 : 0;
		case '&&':
			return a !== 0 && b !== 0 ? 1 : 0;
		case '||':
			return a !== 0 || b !== 0 ? 1 : 0;
		default:
			throw new Error(`bad operator ${op}`);
	}
}

function evalRPN(out: RPN[], scope: Scope): number {
	const st: number[] = [];
	for (const node of out) {
		if (node.k === 'num') st.push(node.v);
		else if (node.k === 'var') {
			const v = node.v in CONSTS ? CONSTS[node.v] : scope[node.v];
			if (v === undefined) throw new Error(`unknown name "${node.v}"`);
			st.push(v);
		} else if (node.k === 'op') {
			if (node.v === 'neg') st.push(-popNum(st));
			else if (node.v === 'not') st.push(popNum(st) === 0 ? 1 : 0);
			else {
				const b = popNum(st);
				const a = popNum(st);
				st.push(applyBin(node.v, a, b));
			}
		} else {
			const def = FUNCS[node.v];
			if (!def) throw new Error(`unknown function "${node.v}"`);
			if (def.a !== 'var' && def.a !== node.n)
				throw new Error(`${node.v}() expects ${def.a} argument(s)`);
			const args: number[] = [];
			for (let i = 0; i < node.n; i++) args.unshift(popNum(st));
			st.push(def.f(args));
		}
	}
	if (st.length !== 1) throw new Error('bad expression');
	return st[0];
}

// ── Parse + resolve ──────────────────────────────────────────────────────────

export function parsePlot(jsonText: string): PlotSpec | { error: string } {
	try {
		const spec = JSON.parse(jsonText) as PlotSpec;
		if (typeof spec !== 'object' || spec === null) return { error: 'plot spec must be an object' };
		return spec;
	} catch (e) {
		return { error: e instanceof Error ? e.message : 'invalid plot JSON' };
	}
}

/** Does this spec need the 3D projector? */
export function plotIs3d(spec: PlotSpec): boolean {
	if (spec.mode === '3d') return true;
	if (spec.surfaces?.length) return true;
	if (spec.zRange) return true;
	if (spec.parametric?.some((p) => p.z != null)) return true;
	if (spec.points?.some((p) => p.z != null || p.zExpr != null)) return true;
	if (
		spec.vectors?.some(
			(v) =>
				v.z != null ||
				v.zExpr != null ||
				(v.from != null && v.from.length > 2) ||
				(v.fromExpr != null && v.fromExpr.length > 2)
		)
	)
		return true;
	return false;
}

/** Build the slider list for a spec: animation param, named controls, 3D camera. */
export function plotControls(spec: PlotSpec): {
	sliders: SliderControl[];
	animateParam?: string;
	fps: number;
	loop: boolean;
} {
	const sliders: SliderControl[] = [];
	let animateParam: string | undefined;
	if (spec.animate) {
		const a = spec.animate;
		const step = a.step ?? (a.range[1] - a.range[0]) / 120;
		sliders.push({
			name: a.param,
			min: a.range[0],
			max: a.range[1],
			step,
			value: a.range[0],
			label: a.label ?? a.param,
			kind: 'param'
		});
		animateParam = a.param;
	}
	for (const c of spec.controls ?? []) {
		const step = c.step ?? (c.range[1] - c.range[0]) / 100;
		sliders.push({
			name: c.name,
			min: c.range[0],
			max: c.range[1],
			step,
			value: c.value ?? c.range[0],
			label: c.label ?? c.name,
			kind: 'control'
		});
	}
	if (plotIs3d(spec) && !spec.lockCamera) {
		sliders.push({
			name: 'azimuth',
			min: 0,
			max: 360,
			step: 1,
			value: spec.azimuth ?? 35,
			label: 'rotate',
			kind: 'camera'
		});
		sliders.push({
			name: 'elevation',
			min: -10,
			max: 90,
			step: 1,
			value: spec.elevation ?? 25,
			label: 'tilt',
			kind: 'camera'
		});
	}
	return { sliders, animateParam, fps: spec.animate?.fps ?? 30, loop: spec.animate?.loop ?? true };
}

const SAMPLES = 160;
const PARAM_SAMPLES = 240;
const SURF_SAMPLES = 22;
const TRAIL_SAMPLES = 120;

function d2r(d: number): number {
	return (d * Math.PI) / 180;
}
function projector(az: number, el: number): (x: number, y: number, z: number) => [number, number, number] {
	const ca = Math.cos(az);
	const sa = Math.sin(az);
	const ce = Math.cos(el);
	const se = Math.sin(el);
	return (x, y, z) => {
		const X = ca * x + sa * y;
		const Y = -sa * x + ca * y;
		return [X, z * ce - Y * se, Y * ce + z * se];
	};
}
function hex2rgb(hex: string): [number, number, number] {
	const h = hex.replace('#', '');
	const n = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
	return [parseInt(n.slice(0, 2), 16), parseInt(n.slice(2, 4), 16), parseInt(n.slice(4, 6), 16)];
}
function shade(hex: string, t: number): string {
	const [r, g, b] = hex2rgb(hex);
	const f = 0.5 + 0.5 * Math.max(0, Math.min(1, t));
	return `rgb(${Math.round(r * f)},${Math.round(g * f)},${Math.round(b * f)})`;
}
function coord(v: number | undefined, expr: string | undefined, scope: Scope): number {
	if (v != null) return v;
	if (expr != null) return compileExpr(expr)(scope);
	return 0;
}
function msg(e: unknown): string {
	return e instanceof Error ? e.message : 'invalid';
}

/** Resolve a spec into screen-agnostic 2D geometry, given the current scope. */
export function resolvePlot(spec: PlotSpec, scope: Scope = {}): ResolvedPlot {
	const width = spec.width ?? 460;
	const height = spec.height ?? 320;
	const is3d = plotIs3d(spec);
	const grid = spec.grid ?? !is3d;
	const equal =
		spec.equal ??
		(is3d ||
			(Boolean(spec.vectors?.length) && !spec.functions?.length && !spec.parametric?.length));

	const az = d2r(scope.azimuth ?? spec.azimuth ?? 35);
	const el = d2r(scope.elevation ?? spec.elevation ?? 25);
	const proj: (x: number, y: number, z: number) => [number, number, number] = is3d
		? projector(az, el)
		: (x, y) => [x, y, 0];
	const P = (x: number, y: number, z = 0): Vec2 => {
		const [sx, sy] = proj(x, y, z);
		return [sx, sy];
	};

	const curves: ResolvedCurve[] = [];
	const guides: ResolvedCurve[] = [];
	const polys: (ResolvedPoly & { depth: number })[] = [];
	const points: ResolvedPoint[] = [];
	const vectors: ResolvedVector[] = [];
	const labels: ResolvedLabel[] = [];
	let ci = 0;
	let error: string | undefined;

	const [xmin0, xmax0] = spec.xRange ?? [-10, 10];

	// y = f(x), drawn in the z = 0 plane
	for (const f of spec.functions ?? []) {
		try {
			const fn = compileExpr(f.expr);
			const pts: Vec2[] = [];
			for (let i = 0; i <= SAMPLES; i++) {
				const x = xmin0 + ((xmax0 - xmin0) * i) / SAMPLES;
				const y = fn({ ...scope, x });
				if (Number.isFinite(y)) pts.push(P(x, y, 0));
			}
			curves.push({ points: pts, label: f.label, color: f.color ?? PALETTE[ci++ % PALETTE.length], legend: true });
		} catch (e) {
			error = `${f.expr}: ${msg(e)}`;
		}
	}
	// parametric curves x(t), y(t), [z(t)]
	for (const p of spec.parametric ?? []) {
		try {
			const fx = compileExpr(p.x);
			const fy = compileExpr(p.y);
			const fz = p.z != null ? compileExpr(p.z) : null;
			const param = p.param ?? 't';
			const n = p.samples ?? PARAM_SAMPLES;
			const [a, b] = p.range;
			const pts: Vec2[] = [];
			for (let i = 0; i <= n; i++) {
				const u = a + ((b - a) * i) / n;
				const s = { ...scope, [param]: u };
				const x = fx(s);
				const y = fy(s);
				const z = fz ? fz(s) : 0;
				if (Number.isFinite(x) && Number.isFinite(y) && Number.isFinite(z)) pts.push(P(x, y, z));
			}
			curves.push({ points: pts, label: p.label, color: p.color ?? PALETTE[ci++ % PALETTE.length], legend: true });
		} catch (e) {
			error = `parametric: ${msg(e)}`;
		}
	}
	// explicit data series
	for (const s of spec.series ?? []) {
		const pts: Vec2[] = s.points.map((pt) => P(pt[0], pt[1], pt[2] ?? 0));
		curves.push({ points: pts, label: s.label, color: s.color ?? PALETTE[ci++ % PALETTE.length], legend: true });
	}
	// surfaces z = f(x, y) as a shaded, depth-sorted quad mesh
	for (const s of spec.surfaces ?? []) {
		try {
			const fn = compileExpr(s.expr);
			const [sxmin, sxmax] = s.xRange ?? spec.xRange ?? [-5, 5];
			const [symin, symax] = s.yRange ?? spec.yRange ?? [-5, 5];
			const n = s.samples ?? SURF_SAMPLES;
			const base = s.color ?? '#2563eb';
			const zg: number[][] = [];
			let zmin = Infinity;
			let zmax = -Infinity;
			for (let i = 0; i <= n; i++) {
				zg[i] = [];
				for (let j = 0; j <= n; j++) {
					const x = sxmin + ((sxmax - sxmin) * i) / n;
					const y = symin + ((symax - symin) * j) / n;
					const z = fn({ ...scope, x, y });
					zg[i][j] = z;
					if (Number.isFinite(z)) {
						if (z < zmin) zmin = z;
						if (z > zmax) zmax = z;
					}
				}
			}
			const span = zmax - zmin || 1;
			for (let i = 0; i < n; i++) {
				for (let j = 0; j < n; j++) {
					const x0 = sxmin + ((sxmax - sxmin) * i) / n;
					const x1 = sxmin + ((sxmax - sxmin) * (i + 1)) / n;
					const y0 = symin + ((symax - symin) * j) / n;
					const y1 = symin + ((symax - symin) * (j + 1)) / n;
					const za = zg[i][j];
					const zb = zg[i + 1][j];
					const zc = zg[i + 1][j + 1];
					const zd = zg[i][j + 1];
					if (![za, zb, zc, zd].every(Number.isFinite)) continue;
					const quad: Vec2[] = [P(x0, y0, za), P(x1, y0, zb), P(x1, y1, zc), P(x0, y1, zd)];
					const d1 = proj(x0, y0, za)[2];
					const d3 = proj(x1, y1, zc)[2];
					const avg = (za + zb + zc + zd) / 4;
					polys.push({
						points: quad,
						fill: shade(base, (avg - zmin) / span),
						stroke: 'rgba(0,0,0,0.12)',
						depth: (d1 + d3) / 2
					});
				}
			}
		} catch (e) {
			error = `surface: ${msg(e)}`;
		}
	}
	polys.sort((a, b) => a.depth - b.depth);

	// points (optionally expression-driven → animatable, with a trail)
	for (const p of spec.points ?? []) {
		try {
			const x = coord(p.x, p.xExpr, scope);
			const y = coord(p.y, p.yExpr, scope);
			const z = coord(p.z, p.zExpr, scope);
			const color = p.color ?? PALETTE[ci++ % PALETTE.length];
			const [sx, sy] = P(x, y, z);
			points.push({ x: sx, y: sy, label: p.label, color, size: p.size ?? 4 });
			if (p.trail && spec.animate && (p.xExpr || p.yExpr || p.zExpr)) {
				const param = spec.animate.param;
				const a0 = spec.animate.range[0];
				const cur = scope[param] ?? a0;
				const fx = p.xExpr ? compileExpr(p.xExpr) : null;
				const fy = p.yExpr ? compileExpr(p.yExpr) : null;
				const fz = p.zExpr ? compileExpr(p.zExpr) : null;
				const trail: Vec2[] = [];
				for (let i = 0; i <= TRAIL_SAMPLES; i++) {
					const u = a0 + ((cur - a0) * i) / TRAIL_SAMPLES;
					const s = { ...scope, [param]: u };
					const tx = fx ? fx(s) : x;
					const ty = fy ? fy(s) : y;
					const tz = fz ? fz(s) : z;
					if (Number.isFinite(tx) && Number.isFinite(ty) && Number.isFinite(tz))
						trail.push(P(tx, ty, tz));
				}
				curves.push({ points: trail, color, width: 1.5, dashed: true, legend: false });
			}
		} catch (e) {
			error = `point: ${msg(e)}`;
		}
	}
	// vectors (numeric or expression coordinates, in 2D or 3D)
	let vi = 0;
	for (const v of spec.vectors ?? []) {
		try {
			const tx = coord(v.x, v.xExpr, scope);
			const ty = coord(v.y, v.yExpr, scope);
			const tz = coord(v.z, v.zExpr, scope);
			let fx = 0;
			let fy = 0;
			let fz = 0;
			if (v.from) {
				fx = v.from[0] ?? 0;
				fy = v.from[1] ?? 0;
				fz = v.from[2] ?? 0;
			} else if (v.fromExpr) {
				fx = compileExpr(v.fromExpr[0])(scope);
				fy = compileExpr(v.fromExpr[1])(scope);
				fz = v.fromExpr[2] ? compileExpr(v.fromExpr[2])(scope) : 0;
			}
			vectors.push({
				from: P(fx, fy, fz),
				tip: P(tx, ty, tz),
				label: v.label,
				color: v.color ?? PALETTE[vi++ % PALETTE.length]
			});
		} catch (e) {
			error = `vector: ${msg(e)}`;
		}
	}

	// 3D axes (faint guide lines + x/y/z labels)
	if (is3d) {
		const [axmin, axmax] = spec.xRange ?? [-5, 5];
		const [aymin, aymax] = spec.yRange ?? [-5, 5];
		const [azmin, azmax] = spec.zRange ?? [-5, 5];
		const gcol = '#9ca3af';
		guides.push({ points: [P(axmin, 0, 0), P(axmax, 0, 0)], color: gcol, legend: false });
		guides.push({ points: [P(0, aymin, 0), P(0, aymax, 0)], color: gcol, legend: false });
		guides.push({ points: [P(0, 0, azmin), P(0, 0, azmax)], color: gcol, legend: false });
		const lx = P(axmax, 0, 0);
		const ly = P(0, aymax, 0);
		const lz = P(0, 0, azmax);
		labels.push({ x: lx[0], y: lx[1], text: spec.xLabel ?? 'x', color: '#6b7280' });
		labels.push({ x: ly[0], y: ly[1], text: spec.yLabel ?? 'y', color: '#6b7280' });
		labels.push({ x: lz[0], y: lz[1], text: spec.zLabel ?? 'z', color: '#6b7280' });
	}

	// bounds from every projected coordinate
	const xs: number[] = [];
	const ys: number[] = [];
	const add = (p: Vec2): void => {
		xs.push(p[0]);
		ys.push(p[1]);
	};
	for (const c of curves) c.points.forEach(add);
	for (const g of guides) g.points.forEach(add);
	for (const pl of polys) pl.points.forEach(add);
	for (const p of points) add([p.x, p.y]);
	for (const v of vectors) {
		add(v.from);
		add(v.tip);
	}

	let [xmin, xmax] =
		!is3d && spec.xRange ? spec.xRange : [xs.length ? Math.min(...xs) : -1, xs.length ? Math.max(...xs) : 1];
	let [ymin, ymax] =
		!is3d && spec.yRange ? spec.yRange : [ys.length ? Math.min(...ys) : -1, ys.length ? Math.max(...ys) : 1];
	if (xmax - xmin < 1e-9) {
		xmin -= 1;
		xmax += 1;
	}
	if (ymax - ymin < 1e-9) {
		ymin -= 1;
		ymax += 1;
	}
	if (is3d || !spec.yRange) {
		const pad = (ymax - ymin) * 0.08;
		ymin -= pad;
		ymax += pad;
	}
	if (is3d) {
		const pad = (xmax - xmin) * 0.06;
		xmin -= pad;
		xmax += pad;
	}

	return {
		title: spec.title,
		xLabel: is3d ? undefined : spec.xLabel,
		yLabel: is3d ? undefined : spec.yLabel,
		is3d,
		bounds: { xmin, xmax, ymin, ymax },
		polys: polys.map(({ depth, ...rest }) => rest),
		curves,
		guides,
		points,
		vectors,
		labels,
		grid,
		equal,
		width,
		height,
		error
	};
}
