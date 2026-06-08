/**
 * Lesson plots & vector diagrams — a tiny, dependency-free engine.
 *
 * Lesson authors embed a fenced ```plot (or ```vectors) block whose body is
 * JSON describing functions / data series / points / vectors. This module is
 * pure (no DOM): it splits the blocks out of the markdown, parses the spec,
 * safely evaluates `y = f(x)` expressions (no eval/Function), samples curves,
 * and computes data bounds. `Plot.svelte` turns the result into SVG.
 */

export interface PlotFunction {
	expr: string;
	label?: string;
	color?: string;
}
export interface PlotSeries {
	points: [number, number][];
	label?: string;
	color?: string;
}
export interface PlotPoint {
	x: number;
	y: number;
	label?: string;
	color?: string;
}
export interface PlotVector {
	x: number;
	y: number;
	from?: [number, number];
	label?: string;
	color?: string;
}

export interface PlotSpec {
	title?: string;
	xLabel?: string;
	yLabel?: string;
	xRange?: [number, number];
	yRange?: [number, number];
	functions?: PlotFunction[];
	series?: PlotSeries[];
	points?: PlotPoint[];
	vectors?: PlotVector[];
	grid?: boolean;
	width?: number;
	height?: number;
	/** Force a 1:1 aspect (equal x/y units) — good for vector diagrams. */
	equal?: boolean;
}

export interface ResolvedCurve {
	points: [number, number][];
	label?: string;
	color: string;
}
export interface ResolvedVector {
	x: number;
	y: number;
	from: [number, number];
	label?: string;
	color: string;
}
export interface ResolvedPlot {
	title?: string;
	xLabel?: string;
	yLabel?: string;
	bounds: { xmin: number; xmax: number; ymin: number; ymax: number };
	curves: ResolvedCurve[];
	points: (PlotPoint & { color: string })[];
	vectors: ResolvedVector[];
	grid: boolean;
	equal: boolean;
	width: number;
	height: number;
	error?: string;
}

export type LessonSegment = { kind: 'md'; content: string } | { kind: 'plot'; content: string };

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

const FUNCS: Record<string, (a: number) => number> = {
	sin: Math.sin,
	cos: Math.cos,
	tan: Math.tan,
	asin: Math.asin,
	acos: Math.acos,
	atan: Math.atan,
	sqrt: Math.sqrt,
	abs: Math.abs,
	exp: Math.exp,
	log: Math.log,
	ln: Math.log,
	sign: Math.sign,
	floor: Math.floor,
	ceil: Math.ceil
};
const CONSTS: Record<string, number> = { pi: Math.PI, e: Math.E };
const PREC: Record<string, number> = { '+': 1, '-': 1, '*': 2, '/': 2, '^': 3, neg: 4 };
const RIGHT = new Set(['^', 'neg']);

type Tok = { t: 'num'; v: number } | { t: 'name'; v: string } | { t: 'op'; v: string } | { t: 'paren'; v: string } | { t: 'comma' };

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
				// allow exponent like 1e-3 but stop if +/- isn't part of an exponent
				if ((src[j] === '+' || src[j] === '-') && !/[eE]/.test(src[j - 1])) break;
				j++;
			}
			const num = Number(src.slice(i, j));
			if (Number.isNaN(num)) throw new Error(`bad number near "${src.slice(i, j)}"`);
			toks.push({ t: 'num', v: num });
			i = j;
		} else if (/[a-zA-Z_]/.test(c)) {
			let j = i + 1;
			while (j < src.length && /[a-zA-Z0-9_]/.test(src[j])) j++;
			toks.push({ t: 'name', v: src.slice(i, j) });
			i = j;
		} else if ('+-*/^'.includes(c)) {
			toks.push({ t: 'op', v: c });
			i++;
		} else if (c === '(' || c === ')') {
			toks.push({ t: 'paren', v: c });
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

/** Compile `expr` into a function of x. Throws on invalid input. */
export function compileExpr(expr: string): (x: number) => number {
	const toks = tokenize(expr);
	const output: Tok[] = [];
	const ops: Tok[] = [];
	let prev: Tok | null = null;
	for (let k = 0; k < toks.length; k++) {
		const tok = toks[k];
		if (tok.t === 'num') output.push(tok);
		else if (tok.t === 'name') {
			if (toks[k + 1]?.t === 'paren' && (toks[k + 1] as { v: string }).v === '(') {
				ops.push({ t: 'op', v: `fn:${tok.v}` });
			} else output.push(tok); // variable or constant
		} else if (tok.t === 'comma') {
			while (ops.length && !(ops[ops.length - 1].t === 'paren')) output.push(ops.pop()!);
		} else if (tok.t === 'op') {
			// unary minus / plus
			let op = tok.v;
			const unary =
				!prev ||
				(prev.t === 'op') ||
				(prev.t === 'paren' && prev.v === '(') ||
				prev.t === 'comma';
			if (op === '-' && unary) op = 'neg';
			else if (op === '+' && unary) {
				prev = tok;
				continue;
			}
			while (ops.length) {
				const top = ops[ops.length - 1];
				if (top.t !== 'op' || top.v.startsWith('fn:')) break;
				if (PREC[top.v] > PREC[op] || (PREC[top.v] === PREC[op] && !RIGHT.has(op))) {
					output.push(ops.pop()!);
				} else break;
			}
			ops.push({ t: 'op', v: op });
		} else if (tok.v === '(') {
			ops.push(tok);
		} else if (tok.v === ')') {
			while (ops.length && ops[ops.length - 1].t !== 'paren') output.push(ops.pop()!);
			if (!ops.length) throw new Error('mismatched parentheses');
			ops.pop(); // discard '('
			const top = ops[ops.length - 1];
			if (top && top.t === 'op' && top.v.startsWith('fn:')) output.push(ops.pop()!);
		}
		prev = tok;
	}
	while (ops.length) {
		const o = ops.pop()!;
		if (o.t === 'paren') throw new Error('mismatched parentheses');
		output.push(o);
	}

	return (x: number): number => {
		const st: number[] = [];
		for (const tok of output) {
			if (tok.t === 'num') st.push(tok.v);
			else if (tok.t === 'name') {
				if (tok.v === 'x') st.push(x);
				else if (tok.v in CONSTS) st.push(CONSTS[tok.v]);
				else throw new Error(`unknown name "${tok.v}"`);
			} else if (tok.t === 'op') {
				if (tok.v.startsWith('fn:')) {
					const fn = FUNCS[tok.v.slice(3)];
					if (!fn) throw new Error(`unknown function "${tok.v.slice(3)}"`);
					const a = st.pop();
					if (a === undefined) throw new Error('bad expression');
					st.push(fn(a));
				} else if (tok.v === 'neg') {
					const a = st.pop();
					if (a === undefined) throw new Error('bad expression');
					st.push(-a);
				} else {
					const b = st.pop();
					const a = st.pop();
					if (a === undefined || b === undefined) throw new Error('bad expression');
					st.push(
						tok.v === '+' ? a + b : tok.v === '-' ? a - b : tok.v === '*' ? a * b : tok.v === '/' ? a / b : a ** b
					);
				}
			}
		}
		if (st.length !== 1) throw new Error('bad expression');
		return st[0];
	};
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

const SAMPLES = 160;

/** Resolve a spec into screen-agnostic geometry: sampled curves, bounds, etc. */
export function resolvePlot(spec: PlotSpec): ResolvedPlot {
	const width = spec.width ?? 460;
	const height = spec.height ?? 300;
	const grid = spec.grid ?? true;
	const equal = spec.equal ?? (Boolean(spec.vectors?.length) && !spec.functions?.length);
	const curves: ResolvedCurve[] = [];
	let ci = 0;
	let error: string | undefined;

	const [xmin0, xmax0] = spec.xRange ?? [-10, 10];

	for (const f of spec.functions ?? []) {
		try {
			const fn = compileExpr(f.expr);
			const pts: [number, number][] = [];
			for (let i = 0; i <= SAMPLES; i++) {
				const x = xmin0 + ((xmax0 - xmin0) * i) / SAMPLES;
				const y = fn(x);
				if (Number.isFinite(y)) pts.push([x, y]);
			}
			curves.push({ points: pts, label: f.label, color: f.color ?? PALETTE[ci++ % PALETTE.length] });
		} catch (e) {
			error = `${f.expr}: ${e instanceof Error ? e.message : 'invalid'}`;
		}
	}
	for (const s of spec.series ?? []) {
		curves.push({ points: s.points, label: s.label, color: s.color ?? PALETTE[ci++ % PALETTE.length] });
	}

	const points = (spec.points ?? []).map((p, i) => ({
		...p,
		color: p.color ?? PALETTE[(ci + i) % PALETTE.length]
	}));
	const vectors: ResolvedVector[] = (spec.vectors ?? []).map((v, i) => ({
		x: v.x,
		y: v.y,
		from: v.from ?? [0, 0],
		label: v.label,
		color: v.color ?? PALETTE[i % PALETTE.length]
	}));

	// Bounds: explicit, else from all data (padded), else the x-range.
	const xs: number[] = [];
	const ys: number[] = [];
	for (const c of curves) for (const [x, y] of c.points) { xs.push(x); ys.push(y); }
	for (const p of points) { xs.push(p.x); ys.push(p.y); }
	for (const v of vectors) { xs.push(v.x, v.from[0]); ys.push(v.y, v.from[1]); }

	let [xmin, xmax] = spec.xRange ?? [
		xs.length ? Math.min(...xs) : -1,
		xs.length ? Math.max(...xs) : 1
	];
	let [ymin, ymax] = spec.yRange ?? [
		ys.length ? Math.min(...ys) : -1,
		ys.length ? Math.max(...ys) : 1
	];
	// Pad and guard against degenerate ranges.
	if (xmax - xmin < 1e-9) (xmin -= 1), (xmax += 1);
	if (ymax - ymin < 1e-9) (ymin -= 1), (ymax += 1);
	if (!spec.yRange) {
		const pad = (ymax - ymin) * 0.08;
		ymin -= pad;
		ymax += pad;
	}

	return {
		title: spec.title,
		xLabel: spec.xLabel,
		yLabel: spec.yLabel,
		bounds: { xmin, xmax, ymin, ymax },
		curves,
		points,
		vectors,
		grid,
		equal,
		width,
		height,
		error
	};
}
