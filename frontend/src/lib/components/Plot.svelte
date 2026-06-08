<script lang="ts">
	// Renders a lesson plot as themed SVG from a PlotSpec: 2D curves & vectors,
	// 3D surfaces / trajectories (orthographic projection), plus interactive
	// sliders and a play/pause control for animated specs.
	import {
		resolvePlot,
		plotControls,
		type PlotSpec,
		type Scope,
		type Vec2
	} from '$lib/utils/lessonPlot';

	let { spec }: { spec: PlotSpec } = $props();

	const cfg = $derived(plotControls(spec));
	// Slider defaults, overlaid with live user/animation overrides.
	let overrides = $state<Record<string, number>>({});
	$effect(() => {
		void spec; // reset interaction when the lesson swaps in a new plot
		overrides = {};
		playing = false;
	});
	const baseScope = $derived(
		Object.fromEntries(cfg.sliders.map((s) => [s.name, s.value])) as Scope
	);
	const scope = $derived({ ...baseScope, ...overrides });
	const r = $derived(resolvePlot(spec, scope));

	// Inner drawing area inside the SVG (room for axis labels/ticks).
	const PAD = { l: 44, r: 16, t: 28, b: 36 };
	const geom = $derived.by(() => {
		const { bounds, width, height, equal } = r;
		const iw = width - PAD.l - PAD.r;
		const ih = height - PAD.t - PAD.b;
		let sx = iw / (bounds.xmax - bounds.xmin);
		let sy = ih / (bounds.ymax - bounds.ymin);
		if (equal) {
			const s = Math.min(sx, sy);
			sx = s;
			sy = s;
		}
		const usedW = (bounds.xmax - bounds.xmin) * sx;
		const usedH = (bounds.ymax - bounds.ymin) * sy;
		const ox = PAD.l + (iw - usedW) / 2;
		const oy = PAD.t + (ih - usedH) / 2;
		const X = (x: number) => ox + (x - bounds.xmin) * sx;
		const Y = (y: number) => oy + usedH - (y - bounds.ymin) * sy;
		return { X, Y };
	});

	function path(points: Vec2[]): string {
		return points
			.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${geom.X(x).toFixed(1)},${geom.Y(y).toFixed(1)}`)
			.join(' ');
	}
	function poly(points: Vec2[]): string {
		return points.map(([x, y]) => `${geom.X(x).toFixed(1)},${geom.Y(y).toFixed(1)}`).join(' ');
	}
	function arrowHead(from: Vec2, tip: Vec2): string {
		const px1 = geom.X(from[0]);
		const py1 = geom.Y(from[1]);
		const px2 = geom.X(tip[0]);
		const py2 = geom.Y(tip[1]);
		const ang = Math.atan2(py2 - py1, px2 - px1);
		const size = 9;
		const a1 = ang + Math.PI - 0.4;
		const a2 = ang + Math.PI + 0.4;
		return [
			`${px2.toFixed(1)},${py2.toFixed(1)}`,
			`${(px2 + size * Math.cos(a1)).toFixed(1)},${(py2 + size * Math.sin(a1)).toFixed(1)}`,
			`${(px2 + size * Math.cos(a2)).toFixed(1)},${(py2 + size * Math.sin(a2)).toFixed(1)}`
		].join(' ');
	}

	function ticks(min: number, max: number, n = 5): number[] {
		const out: number[] = [];
		for (let i = 0; i <= n; i++) out.push(min + ((max - min) * i) / n);
		return out;
	}
	const fmt = (v: number) =>
		Math.abs(v) >= 1000 || (v !== 0 && Math.abs(v) < 0.01)
			? v.toExponential(1)
			: Number(v.toFixed(2)).toString();
	const sliderFmt = (v: number) => Number(v.toFixed(2)).toString();

	const legendCurves = $derived(r.curves.filter((c) => c.label && c.legend !== false));

	function setScope(name: string, value: number): void {
		overrides = { ...overrides, [name]: value };
	}

	// ── Animation loop (requestAnimationFrame; client-only via $effect) ──
	let playing = $state(false);
	$effect(() => {
		if (!playing || !cfg.animateParam) return;
		const p = cfg.animateParam;
		const s = cfg.sliders.find((x) => x.name === p);
		if (!s) return;
		let raf = 0;
		let prev: number | null = null;
		const tick = (ts: number): void => {
			if (prev === null) prev = ts;
			const dt = (ts - prev) / 1000;
			prev = ts;
			let v = (overrides[p] ?? s.value) + s.step * cfg.fps * dt;
			if (v >= s.max) {
				if (cfg.loop) v = s.min;
				else {
					v = s.max;
					playing = false;
				}
			}
			setScope(p, v);
			if (playing) raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(raf);
	});
	function togglePlay(): void {
		if (cfg.animateParam) {
			const cur = scope[cfg.animateParam];
			const s = cfg.sliders.find((x) => x.name === cfg.animateParam);
			if (!playing && s && cur >= s.max) setScope(cfg.animateParam, s.min);
		}
		playing = !playing;
	}
</script>

<figure class="plot">
	{#if r.error}
		<p class="plot__err">⚠ Plot error: {r.error}</p>
	{/if}
	<svg
		viewBox="0 0 {r.width} {r.height}"
		class="plot__svg"
		role="img"
		aria-label={r.title ?? 'plot'}
	>
		{#if r.title}<text class="plot__title" x={r.width / 2} y="16" text-anchor="middle"
				>{r.title}</text
			>{/if}

		<!-- 2D grid + ticks -->
		{#if r.grid && !r.is3d}
			{#each ticks(r.bounds.xmin, r.bounds.xmax) as gx}
				<line class="plot__grid" x1={geom.X(gx)} y1={PAD.t} x2={geom.X(gx)} y2={r.height - PAD.b} />
				<text class="plot__tick" x={geom.X(gx)} y={r.height - PAD.b + 14} text-anchor="middle"
					>{fmt(gx)}</text
				>
			{/each}
			{#each ticks(r.bounds.ymin, r.bounds.ymax) as gy}
				<line class="plot__grid" x1={PAD.l} y1={geom.Y(gy)} x2={r.width - PAD.r} y2={geom.Y(gy)} />
				<text class="plot__tick" x={PAD.l - 6} y={geom.Y(gy) + 3} text-anchor="end">{fmt(gy)}</text>
			{/each}
		{/if}

		<!-- 2D zero axes -->
		{#if !r.is3d && r.bounds.ymin <= 0 && r.bounds.ymax >= 0}
			<line class="plot__axis" x1={PAD.l} y1={geom.Y(0)} x2={r.width - PAD.r} y2={geom.Y(0)} />
		{/if}
		{#if !r.is3d && r.bounds.xmin <= 0 && r.bounds.xmax >= 0}
			<line class="plot__axis" x1={geom.X(0)} y1={PAD.t} x2={geom.X(0)} y2={r.height - PAD.b} />
		{/if}

		<!-- 3D surface mesh (already depth-sorted back-to-front) -->
		{#each r.polys as q}
			<polygon points={poly(q.points)} style="fill:{q.fill};stroke:{q.stroke}" stroke-width="0.5" />
		{/each}

		<!-- guide lines (3D axes) -->
		{#each r.guides as g}
			<path class="plot__guide" d={path(g.points)} style="stroke:{g.color}" />
		{/each}

		<!-- curves (and dashed animation trails) -->
		{#each r.curves as c}
			<path
				class="plot__curve"
				d={path(c.points)}
				style="stroke:{c.color}"
				stroke-width={c.width ?? 2}
				stroke-dasharray={c.dashed ? '4 4' : undefined}
			/>
		{/each}

		<!-- vectors -->
		{#each r.vectors as v}
			<line
				class="plot__vec"
				x1={geom.X(v.from[0])}
				y1={geom.Y(v.from[1])}
				x2={geom.X(v.tip[0])}
				y2={geom.Y(v.tip[1])}
				style="stroke:{v.color}"
			/>
			<polygon class="plot__head" points={arrowHead(v.from, v.tip)} style="fill:{v.color}" />
			{#if v.label}
				<text class="plot__vlabel" x={geom.X(v.tip[0]) + 4} y={geom.Y(v.tip[1]) - 4} style="fill:{v.color}"
					>{v.label}</text
				>
			{/if}
		{/each}

		<!-- points -->
		{#each r.points as p}
			<circle cx={geom.X(p.x)} cy={geom.Y(p.y)} r={p.size} style="fill:{p.color}" stroke="#fff" stroke-width="1" />
			{#if p.label}<text class="plot__plabel" x={geom.X(p.x) + 7} y={geom.Y(p.y) - 7}>{p.label}</text>{/if}
		{/each}

		<!-- 3D axis labels -->
		{#each r.labels as lb}
			<text class="plot__axis3d" x={geom.X(lb.x)} y={geom.Y(lb.y)} style="fill:{lb.color}">{lb.text}</text>
		{/each}

		<!-- 2D axis labels -->
		{#if r.xLabel}<text class="plot__axlabel" x={r.width / 2} y={r.height - 4} text-anchor="middle"
				>{r.xLabel}</text
			>{/if}
		{#if r.yLabel}<text
				class="plot__axlabel"
				x={12}
				y={r.height / 2}
				text-anchor="middle"
				transform="rotate(-90 12 {r.height / 2})">{r.yLabel}</text
			>{/if}
	</svg>

	{#if legendCurves.length}
		<figcaption class="plot__legend">
			{#each legendCurves as c}
				<span class="plot__key"><span class="plot__swatch" style="background:{c.color}"></span>{c.label}</span
				>
			{/each}
		</figcaption>
	{/if}

	{#if cfg.sliders.length}
		<div class="plot__controls">
			{#if cfg.animateParam}
				<button class="plot__play" type="button" onclick={togglePlay} aria-pressed={playing}>
					{playing ? '⏸ Pause' : '▶ Play'}
				</button>
			{/if}
			{#each cfg.sliders as s}
				<label class="plot__slider">
					<span class="plot__slabel">{s.label} <b>{sliderFmt(scope[s.name])}</b></span>
					<input
						type="range"
						min={s.min}
						max={s.max}
						step={s.step}
						value={scope[s.name]}
						oninput={(e) => setScope(s.name, +e.currentTarget.value)}
					/>
				</label>
			{/each}
		</div>
	{/if}
</figure>

<style>
	.plot {
		margin: 0.7rem 0;
		background: #ffffff;
		border: 2px solid #000000;
		border-radius: 8px;
		padding: 6px 8px;
	}
	.plot__svg {
		width: 100%;
		height: auto;
		display: block;
	}
	.plot__title {
		font-size: 13px;
		font-weight: 700;
		fill: #111827;
	}
	.plot__grid {
		stroke: #eef0f3;
		stroke-width: 1;
	}
	.plot__axis {
		stroke: #9ca3af;
		stroke-width: 1.5;
	}
	.plot__guide {
		fill: none;
		stroke-width: 1.25;
		stroke-dasharray: 2 3;
	}
	.plot__tick {
		font-size: 9px;
		fill: #6b7280;
	}
	.plot__curve {
		fill: none;
	}
	.plot__vec {
		stroke-width: 2.5;
	}
	.plot__vlabel,
	.plot__plabel {
		font-size: 11px;
		font-weight: 700;
	}
	.plot__plabel {
		fill: #374151;
	}
	.plot__axis3d {
		font-size: 11px;
		font-weight: 700;
	}
	.plot__err {
		margin: 0 0 6px;
		font-size: 0.78rem;
		color: #b91c1c;
	}
	.plot__legend {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem 0.9rem;
		font-size: 0.72rem;
		color: #374151;
		padding: 4px 2px 2px;
	}
	.plot__key {
		display: inline-flex;
		align-items: center;
		gap: 5px;
	}
	.plot__swatch {
		width: 12px;
		height: 3px;
		border-radius: 2px;
	}
	.plot__controls {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 0.4rem 0.9rem;
		padding: 6px 2px 2px;
		border-top: 1px solid #eef0f3;
		margin-top: 4px;
	}
	.plot__play {
		font: inherit;
		font-size: 0.74rem;
		font-weight: 700;
		padding: 3px 10px;
		border: 2px solid #000;
		border-radius: 6px;
		background: #fde047;
		cursor: pointer;
	}
	.plot__play:hover {
		background: #facc15;
	}
	.plot__slider {
		display: inline-flex;
		flex-direction: column;
		gap: 1px;
		font-size: 0.7rem;
		color: #374151;
	}
	.plot__slabel b {
		color: #111827;
	}
	.plot__slider input {
		width: 130px;
	}
</style>
