<script lang="ts">
	// Renders a lesson plot / vector diagram as themed SVG from a PlotSpec.
	import { resolvePlot, type PlotSpec } from '$lib/utils/lessonPlot';

	let { spec }: { spec: PlotSpec } = $props();
	const r = $derived(resolvePlot(spec));

	// Inner drawing area inside the SVG (leave room for axis labels/ticks).
	const PAD = { l: 44, r: 16, t: 28, b: 36 };

	// Screen mappers (data → pixels). For `equal` aspect we use one scale so a
	// vector at 45° looks like 45°.
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
		const X = (x: number) => PAD.l + (x - bounds.xmin) * sx;
		const Y = (y: number) => PAD.t + ih - (y - bounds.ymin) * sy;
		return { X, Y, iw, ih };
	});

	function path(points: [number, number][]): string {
		return points
			.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${geom.X(x).toFixed(1)},${geom.Y(y).toFixed(1)}`)
			.join(' ');
	}

	// Arrowhead polygon points for a vector ending at (hx,hy) coming from angle a.
	function arrowHead(fx: number, fy: number, tx: number, ty: number): string {
		const px1 = geom.X(fx);
		const py1 = geom.Y(fy);
		const px2 = geom.X(tx);
		const py2 = geom.Y(ty);
		const ang = Math.atan2(py2 - py1, px2 - px1);
		const size = 9;
		const a1 = ang + Math.PI - 0.4;
		const a2 = ang + Math.PI + 0.4;
		return [
			`${px2},${py2}`,
			`${(px2 + size * Math.cos(a1)).toFixed(1)},${(py2 + size * Math.sin(a1)).toFixed(1)}`,
			`${(px2 + size * Math.cos(a2)).toFixed(1)},${(py2 + size * Math.sin(a2)).toFixed(1)}`
		].join(' ');
	}

	// A few evenly-spaced grid/tick values across a range.
	function ticks(min: number, max: number, n = 5): number[] {
		const out: number[] = [];
		for (let i = 0; i <= n; i++) out.push(min + ((max - min) * i) / n);
		return out;
	}
	const fmt = (v: number) => (Math.abs(v) >= 1000 || (v !== 0 && Math.abs(v) < 0.01) ? v.toExponential(1) : Number(v.toFixed(2)).toString());
</script>

<figure class="plot">
	{#if r.error}
		<p class="plot__err">⚠ Plot error: {r.error}</p>
	{/if}
	<svg viewBox="0 0 {r.width} {r.height}" class="plot__svg" role="img" aria-label={r.title ?? 'plot'}>
		{#if r.title}<text class="plot__title" x={r.width / 2} y="16" text-anchor="middle">{r.title}</text>{/if}

		<!-- grid + ticks -->
		{#if r.grid}
			{#each ticks(r.bounds.xmin, r.bounds.xmax) as gx}
				<line class="plot__grid" x1={geom.X(gx)} y1={PAD.t} x2={geom.X(gx)} y2={r.height - PAD.b} />
				<text class="plot__tick" x={geom.X(gx)} y={r.height - PAD.b + 14} text-anchor="middle">{fmt(gx)}</text>
			{/each}
			{#each ticks(r.bounds.ymin, r.bounds.ymax) as gy}
				<line class="plot__grid" x1={PAD.l} y1={geom.Y(gy)} x2={r.width - PAD.r} y2={geom.Y(gy)} />
				<text class="plot__tick" x={PAD.l - 6} y={geom.Y(gy) + 3} text-anchor="end">{fmt(gy)}</text>
			{/each}
		{/if}

		<!-- axes (x=0 / y=0 lines if in range) -->
		{#if r.bounds.ymin <= 0 && r.bounds.ymax >= 0}
			<line class="plot__axis" x1={PAD.l} y1={geom.Y(0)} x2={r.width - PAD.r} y2={geom.Y(0)} />
		{/if}
		{#if r.bounds.xmin <= 0 && r.bounds.xmax >= 0}
			<line class="plot__axis" x1={geom.X(0)} y1={PAD.t} x2={geom.X(0)} y2={r.height - PAD.b} />
		{/if}

		<!-- curves -->
		{#each r.curves as c}
			<path class="plot__curve" d={path(c.points)} style="stroke:{c.color}" />
		{/each}

		<!-- vectors -->
		{#each r.vectors as v}
			<line
				class="plot__vec"
				x1={geom.X(v.from[0])}
				y1={geom.Y(v.from[1])}
				x2={geom.X(v.x)}
				y2={geom.Y(v.y)}
				style="stroke:{v.color}"
			/>
			<polygon class="plot__head" points={arrowHead(v.from[0], v.from[1], v.x, v.y)} style="fill:{v.color}" />
			{#if v.label}
				<text class="plot__vlabel" x={geom.X(v.x) + 4} y={geom.Y(v.y) - 4} style="fill:{v.color}">{v.label}</text>
			{/if}
		{/each}

		<!-- points -->
		{#each r.points as p}
			<circle class="plot__pt" cx={geom.X(p.x)} cy={geom.Y(p.y)} r="3.5" style="fill:{p.color}" />
			{#if p.label}<text class="plot__plabel" x={geom.X(p.x) + 6} y={geom.Y(p.y) - 6}>{p.label}</text>{/if}
		{/each}

		<!-- axis labels -->
		{#if r.xLabel}<text class="plot__axlabel" x={r.width / 2} y={r.height - 4} text-anchor="middle">{r.xLabel}</text>{/if}
		{#if r.yLabel}<text class="plot__axlabel" x={12} y={r.height / 2} text-anchor="middle" transform="rotate(-90 12 {r.height / 2})">{r.yLabel}</text>{/if}
	</svg>

	{#if r.curves.some((c) => c.label)}
		<figcaption class="plot__legend">
			{#each r.curves.filter((c) => c.label) as c}
				<span class="plot__key"><span class="plot__swatch" style="background:{c.color}"></span>{c.label}</span>
			{/each}
		</figcaption>
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
	.plot__tick {
		font-size: 9px;
		fill: #6b7280;
	}
	.plot__curve {
		fill: none;
		stroke-width: 2;
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
</style>
