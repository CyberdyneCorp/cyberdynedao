"""Scientific Data Visualization track: Basics -> Intermediate -> Advanced.

From the grammar of charts, perceptual encoding and colour, through distributions,
relationships and small multiples, to networks, genomic tracks and molecular
figures. Lessons are ``text`` with LaTeX, interactive ```plot blocks and
``mermaid`` pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Scientific Data Visualization -- Basics ----------------------------------

_BASICS = SeedCourse(
    slug="data-visualization-bio-basics",
    title="Scientific Data Visualization — Basics",
    description=(
        "Build the foundations: why we visualise data, the grammar that turns "
        "variables into marks and channels, the perceptual ranking of visual "
        "encodings, principled use of colour, and chart-type selection. The "
        "intuition every figure in a paper or dashboard rests on, with "
        "interactive curves and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why visualise data",
            "10 min",
            r"""
# Why visualise data

A visualisation is a *mapping from data to an image* that lets the visual system
do statistics for us. The classic warning is **Anscombe's quartet**: four
datasets with identical mean, variance, correlation and regression line that look
completely different once plotted. Summary statistics compress; pictures reveal
structure — clusters, outliers, gaps, nonlinearity.

Visualisation serves two distinct goals. **Exploratory** graphics are for *you*,
made fast and disposable to find patterns. **Explanatory** graphics are for a
*reader*, polished to communicate one clear message. Confusing the two produces
cluttered figures that neither explore nor explain.

```mermaid
flowchart LR
  A[Raw data] --> B[Exploratory plots]
  B --> C{Pattern found?}
  C -->|Yes| D[Explanatory figure]
  C -->|No| B
  D --> E[Reader insight]
```

Good figures obey three rules: show the data, minimise non-data ink, and make
comparison easy. A growth curve, for example, only earns its place if the eye can
read the *rate* — the slope — at a glance.

```plot
{"title": "Population growth over time", "xLabel": "Time (h)", "yLabel": "Cells (relative)", "xRange": [0, 10], "yRange": [0, 25], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "Exponential phase", "color": "#2563eb"}]}
```

**Next:** the grammar that turns variables into marks.
""",
        ),
        _t(
            "The grammar of graphics",
            "11 min",
            r"""
# The grammar of graphics

Wilkinson's *grammar of graphics* — implemented in ggplot2, Vega-Lite and
plotnine — decomposes any statistical chart into composable layers rather than
naming chart "types". The core idea: a chart is a set of **marks** (geometric
objects: points, lines, bars, areas) whose **aesthetics** are bound to data
columns through **scales**.

The essential pieces are:

- **Data** — a tidy table, one row per observation.
- **Mapping (aesthetics)** — which column drives $x$, $y$, colour, size, shape.
- **Geometry** — the mark that draws the encoded value.
- **Scale** — the function from data values to pixels, colours or sizes.
- **Facet / coordinate / theme** — splitting, projecting and styling.

```mermaid
flowchart LR
  A[Tidy data] --> B[Aesthetic mapping]
  B --> C[Scale]
  C --> D[Geometry / mark]
  D --> E[Facet + coord + theme]
  E --> F[Rendered chart]
```

Because the layers are orthogonal, you can swap a bar geometry for a point
geometry without touching the mapping, or add a smoothing layer on top of raw
points. This compositional view is why "what chart should I use?" is better
phrased as "which variable goes on which channel, drawn with which mark?".

**Next:** how well each visual channel is actually perceived.
""",
        ),
        _t(
            "Perceptual encoding & channels",
            "12 min",
            r"""
# Perceptual encoding & channels

Not all visual channels are read equally well. **Cleveland & McGill** ranked the
*elementary perceptual tasks* by accuracy. For comparing magnitudes the ranking,
best to worst, is roughly:

1. Position on a common scale
2. Position on non-aligned scales
3. Length
4. Angle / slope
5. Area
6. Colour value / saturation, then volume

This is the empirical reason a **dot plot or bar chart beats a pie chart**: a pie
forces the eye to compare angles and areas (tasks 4–5) where a bar uses length and
aligned position (tasks 1–3). Stevens' power law formalises the bias: perceived
magnitude scales as $\psi = k\,I^{a}$, and for area the exponent $a<1$, so big
areas are systematically *underestimated* — a bubble twice the data value looks
far less than twice as big.

```plot
{"title": "Stevens' law: perceived vs actual area", "xLabel": "Actual magnitude", "yLabel": "Perceived magnitude", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "Veridical (ideal)", "color": "#16a34a"}, {"expr": "x^0.7", "label": "Perceived area (a=0.7)", "color": "#dc2626"}]}
```

The practical rule: encode the quantity you most want compared on the *highest*
available channel — position — and reserve weaker channels (colour, size) for
secondary or categorical attributes.

**Next:** using colour without lying.
""",
        ),
        _t(
            "Colour done right",
            "12 min",
            r"""
# Colour done right

Colour is the most abused channel because it is so eye-catching and so easy to
misuse. Match the **colour-scale type to the data**:

- **Sequential** (light to dark of one hue) for ordered magnitudes — e.g. gene
  expression from low to high.
- **Diverging** (two hues meeting at a neutral midpoint) for data with a
  meaningful centre — log fold-change around zero, residuals.
- **Qualitative** (distinct hues, similar lightness) for unordered categories —
  cell types, treatment groups.

The classic **rainbow / jet** colormap fails on every count: it is not
perceptually uniform (equal data steps give unequal perceived steps), it
introduces false boundaries at yellow and cyan, and it is unreadable for the
~8% of men with red–green colour-vision deficiency. Modern perceptually-uniform
maps — **viridis, magma, cividis** — fix this and stay legible in greyscale.

```mermaid
flowchart TB
  A[What is the data?] --> B{Has natural order?}
  B -->|No| C[Qualitative palette]
  B -->|Yes| D{Meaningful midpoint?}
  D -->|No| E[Sequential viridis]
  D -->|Yes| F[Diverging palette]
```

Always check a figure with a colour-blindness simulator, and never encode
information by hue alone — pair it with shape, position or a direct label.

**Next:** choosing the right chart for the question.
""",
        ),
        _t(
            "Choosing the right chart",
            "11 min",
            r"""
# Choosing the right chart

Chart choice follows from the **question** and the **variable types**, not from
aesthetics. A compact decision guide:

- **Distribution of one variable** — histogram, density, box or violin plot.
- **Comparison across categories** — bar chart (sorted!) or dot plot.
- **Relationship between two numerics** — scatter plot, add a smoother.
- **Change over time** — line chart.
- **Part-to-whole** — stacked bar; avoid pie charts for more than 2–3 slices.

```mermaid
flowchart LR
  A[Question] --> B{How many variables?}
  B -->|One numeric| C[Histogram / density]
  B -->|Category vs value| D[Bar / dot]
  B -->|Two numerics| E[Scatter]
  B -->|Value vs time| F[Line]
```

Two ideas guide refinement. **Tufte's data-ink ratio** says maximise the
fraction of ink that encodes data; erase chartjunk, heavy gridlines and 3-D
effects. The **lie factor** quantifies distortion as the ratio of the visual
effect's size to the data effect's size; an honest chart has a lie factor near
$1$. The commonest violation is a truncated bar-chart axis, which exaggerates a
small difference. Bars must start at zero; line charts, which encode change via
slope, need not.

```plot
{"title": "Saturating dose response", "xLabel": "Dose (relative)", "yLabel": "Response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "Response", "color": "#2563eb"}]}
```

**Next:** test your visual intuition.
""",
        ),
        _quiz(),
    ),
)


# -- Scientific Data Visualization -- Intermediate ----------------------------

_INTERMEDIATE = SeedCourse(
    slug="data-visualization-bio-intermediate",
    title="Scientific Data Visualization — Intermediate",
    description=(
        "Core quantitative methods: visualising distributions honestly, binning "
        "and kernel density estimation, scatterplots with uncertainty and "
        "overplotting fixes, small multiples and faceting, and the log/symlog "
        "transforms that biological data demand. Hands-on with curves and "
        "pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Visualising distributions",
            "12 min",
            r"""
# Visualising distributions

Comparing groups by their **means alone hides the shape**. A bar chart of means
cannot tell a unimodal group from a bimodal one, nor reveal skew or outliers.
Richer encodings show the full distribution:

- **Box plot** — median, quartiles ($Q_1, Q_3$) and whiskers; compact but hides
  multimodality entirely.
- **Violin plot** — a mirrored kernel density; reveals shape but can imply data
  where there is none in small samples.
- **Strip / jitter / beeswarm** — every raw point; honest for small $n$.

The modern recommendation for small samples is to **overlay the raw points** on
a box or violin so the reader sees both summary and data. Beware the "bar-bar"
plot of mean ± SEM for skewed assay data: the bar starts at zero and implies a
symmetric spread the data do not have.

```mermaid
flowchart LR
  A[Group data] --> B[Box: quartiles]
  A --> C[Violin: density shape]
  A --> D[Jitter: raw points]
  B --> E[Overlay points]
  C --> E
  D --> E
```

A useful diagnostic is the **empirical CDF**, which needs no binning choice and
makes shifts in location and spread directly comparable between groups.

**Next:** the binning and bandwidth choices behind histograms.
""",
        ),
        _t(
            "Histograms & kernel density",
            "13 min",
            r"""
# Histograms & kernel density

A histogram counts observations into bins, but the **bin width $h$** controls the
story: too wide oversmooths and hides modes; too narrow turns noise into spikes.
Common rules pick $h$ from the data — **Sturges** ($k=\lceil\log_2 n\rceil+1$
bins) assumes roughness near Normal, while **Freedman–Diaconis**
$h = 2\,\mathrm{IQR}\,n^{-1/3}$ is robust to outliers and usually preferred.

**Kernel density estimation (KDE)** removes the arbitrary bin *edges* by placing
a smooth kernel $K$ at each point:

$$\hat f(x) = \frac{1}{n h}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right)$$

Now the **bandwidth $h$** plays the role of bin width: it is the bias–variance
knob. Silverman's rule of thumb, $h \approx 1.06\,\hat\sigma\,n^{-1/5}$, is a
reasonable default for roughly Normal data but oversmooths multimodal
distributions.

```plot
{"title": "A Gaussian kernel (one data point)", "xLabel": "x", "yLabel": "Density", "xRange": [0, 10], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "exp(-(x-5)^2/2)/sqrt(2*3.14159)", "label": "K centred at 5", "color": "#2563eb"}]}
```

A frequent error is letting a KDE spill below a hard physical bound — densities
of concentrations or counts must not extend past zero; reflect the data at the
boundary or use a log scale instead.

**Next:** scatterplots, overplotting and uncertainty.
""",
        ),
        _t(
            "Scatterplots & uncertainty",
            "13 min",
            r"""
# Scatterplots & uncertainty

The scatterplot is the workhorse for two numeric variables, but it breaks down
with **overplotting** when thousands of points pile up. Fixes, roughly in order
of data size:

- **Alpha transparency** — lets density show through overlap.
- **Jitter** — small random offsets for discrete or tied values.
- **2-D binning** — hexbin or density contours for very large $n$.

Add a **smoother** to summarise the trend: LOESS for exploratory local fits, or a
fitted model line with its confidence band. Crucially, show **uncertainty**. A
$95\%$ confidence interval communicates precision; error bars must be *labelled*
as SD, SEM or CI, because they differ by roughly $\sqrt n$ and readers routinely
confuse them.

```plot
{"title": "Trend with saturating relationship", "xLabel": "Predictor", "yLabel": "Response", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "LOESS-like fit", "color": "#dc2626"}]}
```

Two cautions. First, never extrapolate a smoother beyond the data range. Second,
remember that a fitted line can hide subgroups — **Simpson's paradox** arises
when an overall trend reverses within strata, which colour-coding or faceting by
the lurking variable will expose.

```mermaid
flowchart LR
  A[Two numerics] --> B{n large?}
  B -->|No| C[Points + alpha]
  B -->|Yes| D[Hexbin / contours]
  C --> E[Add smoother + CI]
  D --> E
```

**Next:** comparing many groups with small multiples.
""",
        ),
        _t(
            "Small multiples & faceting",
            "12 min",
            r"""
# Small multiples & faceting

Tufte's **small multiples** — a grid of mini-charts that share axes and encoding,
differing only in one conditioning variable — are one of the most powerful tools
in visualisation. Because every panel uses the *same scales*, the eye compares
across panels effortlessly, and the design scales to dozens of categories where a
single overloaded chart with a rainbow legend would collapse.

In the grammar of graphics this is **faceting**: `facet_wrap` lays panels in a
flowing grid, `facet_grid` arranges them by the cross of two variables (rows ×
columns).

```mermaid
flowchart TB
  A[One dataset] --> B[Split by condition]
  B --> C[Panel: tissue A]
  B --> D[Panel: tissue B]
  B --> E[Panel: tissue C]
  C --> F[Shared axes + scale]
  D --> F
  E --> F
```

The non-negotiable rule is **fix the scales**. If each panel auto-scales its
axes, cross-panel comparison becomes a lie — a small bump in one panel can look
identical to a huge peak in another. Use free scales only deliberately, and flag
it in the caption. Order panels meaningfully (by magnitude or biology, not
alphabetically), and keep per-panel chartjunk minimal since it multiplies across
the grid.

**Next:** the transforms biological data demand.
""",
        ),
        _t(
            "Log scales & transforms",
            "12 min",
            r"""
# Log scales & transforms

Biological data span orders of magnitude — gene counts, viral titres,
concentrations — and **multiplicative** processes dominate. On a linear axis the
small values are crushed against the floor; a **logarithmic axis** turns
exponential growth into a straight line and makes *fold-changes* the visual unit,
since equal ratios map to equal distances.

$$y = a\,e^{kt} \;\Longrightarrow\; \log y = \log a + k t$$

So the slope on a semi-log plot *is* the rate constant $k$. For data that
include zeros or negatives (log fold-change, residuals) a plain log fails; use a
**symlog** transform — linear in a small band around zero, logarithmic beyond —
or `log1p`. For proportions and odds, the **logit** transform spreads out values
near 0 and 1.

```plot
{"title": "Exponential decay (first-order)", "xLabel": "Time", "yLabel": "Signal", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "Decay, k=0.5", "color": "#16a34a"}]}
```

Three rules keep log plots honest: label the axis as log and show the original
units in the ticks ($10^0, 10^1, 10^2$); never put a zero baseline on a log
axis (it is at $-\infty$); and remember that a log transform also reshapes the
distribution, often pulling right-skewed data toward symmetry, which is exactly
why statisticians log-transform before testing.

**Next:** test your quantitative skills.
""",
        ),
        _quiz(),
    ),
)


# -- Scientific Data Visualization -- Advanced --------------------------------

_ADVANCED = SeedCourse(
    slug="data-visualization-bio-advanced",
    title="Scientific Data Visualization — Advanced",
    description=(
        "State-of-the-art and applied: dimensionality-reduction maps (PCA, t-SNE, "
        "UMAP) for single-cell data, network and graph layouts, genome-browser "
        "tracks, molecular and structural figures, and interactive and AI-assisted "
        "visualisation. The toolkit behind modern computational-biology figures."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Dimensionality reduction maps",
            "14 min",
            r"""
# Dimensionality reduction maps

Single-cell RNA-seq yields a matrix of ~$20{,}000$ genes by hundreds of
thousands of cells. To *see* it we project to 2-D. **PCA** is the linear
baseline: it finds orthogonal axes of maximal variance, so distances and global
structure are faithful, but it cannot unfold curved manifolds. Nonlinear
embeddings — **t-SNE** and **UMAP** — are designed instead to preserve *local
neighbourhoods*, producing the familiar islands of cell types.

t-SNE minimises the KL divergence between neighbour probabilities in high and low
dimensions; UMAP optimises a fuzzy-simplicial graph and is faster with better
global structure. Both are **stochastic and parameterised** — t-SNE's
*perplexity* and UMAP's *n_neighbors* trade local against global detail.

```mermaid
flowchart LR
  A[Cell x gene matrix] --> B[PCA: top 50 PCs]
  B --> C[Neighbour graph]
  C --> D[UMAP / t-SNE 2D]
  D --> E[Colour by cluster / gene]
```

The critical caveat for readers and authors: in t-SNE and UMAP, **distances
between clusters and cluster sizes are not meaningful** — only neighbour
membership is. Never read a gap between two blobs as a quantitative distance, and
always report the parameters, since different settings yield qualitatively
different maps.

```plot
{"title": "Neighbour weight vs distance (UMAP-like)", "xLabel": "Distance in embedding", "yLabel": "Edge weight", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(x/2)^2)", "label": "Low-dim affinity", "color": "#2563eb"}]}
```

**Next:** drawing networks and graphs.
""",
        ),
        _t(
            "Network & graph visualisation",
            "13 min",
            r"""
# Network & graph visualisation

Protein–protein interaction maps, gene-regulatory networks and metabolic pathways
are **graphs** $G=(V,E)$, and their layout determines whether structure is
visible. **Force-directed** algorithms (Fruchterman–Reingold, ForceAtlas2) treat
edges as springs and nodes as mutually repelling charges, settling into a
low-energy layout where tightly connected modules cluster together.

Encode graph properties onto visual channels: **node size** for degree or
expression, **colour** for community/module, **edge width** for interaction
confidence. Tools like Cytoscape and Gephi are standard in systems biology.

```mermaid
flowchart LR
  A[Edge list] --> B[Build graph]
  B --> C[Compute centrality]
  C --> D[Force-directed layout]
  D --> E[Encode degree / module]
```

Beware the **"hairball"**: dense graphs (thousands of edges) collapse into an
uninformative tangle. Remedies include filtering by edge weight, extracting the
backbone, collapsing communities into meta-nodes, or switching to a **matrix
view** (an adjacency heatmap), which scales far better for dense graphs and makes
clusters appear as on-diagonal blocks once rows are ordered by community.

```plot
{"title": "Degree distribution of a scale-free network", "xLabel": "Degree k", "yLabel": "P(k) (relative)", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(x^2)", "label": "Power law P(k) ~ k^-2", "color": "#dc2626"}]}
```

**Next:** visualising the genome itself.
""",
        ),
        _t(
            "Genomic tracks & heatmaps",
            "13 min",
            r"""
# Genomic tracks & heatmaps

Genomic data are **positional**: every value lives at a coordinate on a
chromosome. The dominant idiom is the **genome browser** (IGV, UCSC, JBrowse),
which stacks aligned **tracks** sharing a common horizontal genomic axis — gene
models, read pileups (BAM), peaks (ChIP-seq), coverage (bigWig) and variants
(VCF). Vertical alignment lets the eye correlate, for instance, a ChIP-seq peak
with a promoter.

```mermaid
flowchart TB
  A[Genomic coordinate axis] --> B[Gene model track]
  A --> C[RNA-seq coverage]
  A --> D[ChIP-seq peaks]
  A --> E[Variant track]
```

For genome-wide summaries, two encodings dominate. The **Manhattan plot** of a
GWAS puts chromosomal position on $x$ and $-\log_{10} p$ on $y$, so the strongest
associations *rise* above the multiple-testing threshold line. The **clustered
heatmap** displays an expression matrix (genes × samples) with a colour scale,
flanked by dendrograms from hierarchical clustering that reorder rows and columns
so co-regulated blocks become visible.

```plot
{"title": "Manhattan plot significance: -log10 p", "xLabel": "p-value", "yLabel": "-log10(p)", "xRange": [0.001, 1], "yRange": [0, 3], "grid": true, "functions": [{"expr": "0-log(x)/log(10)", "label": "Signal strength", "color": "#16a34a"}]}
```

Two rules: a diverging, zero-centred scale on row-scaled ($z$-score) data so
over- and under-expression read symmetrically; and a perceptually-uniform
sequential map for raw intensities so equal steps look equal.

**Next:** rendering molecules and structures.
""",
        ),
        _t(
            "Molecular & structural figures",
            "13 min",
            r"""
# Molecular & structural figures

Macromolecular structures (PDB, and now AlphaFold predictions) are 3-D, and the
chosen **representation** answers a specific question. Tools — PyMOL, ChimeraX,
Mol* — offer a vocabulary of idioms:

- **Cartoon / ribbon** — abstracts the backbone to show secondary structure
  (helices, sheets) and overall fold.
- **Surface** — the solvent-accessible envelope, for pockets and
  complementarity.
- **Ball-and-stick / sticks** — atomic detail for active sites and ligands.

```mermaid
flowchart LR
  A[Structure question] --> B{Scale?}
  B -->|Whole fold| C[Cartoon]
  B -->|Binding pocket| D[Surface]
  B -->|Atomic mechanism| E[Sticks / ball-and-stick]
```

Colour carries meaning: by **secondary structure**, by **chain** for complexes,
by **B-factor / pLDDT** to flag mobile or low-confidence regions, or by
**electrostatic potential** on a surface (red negative, blue positive). For
AlphaFold models, always show the pLDDT confidence colouring and the PAE plot —
presenting a low-confidence loop as if it were a determined structure is a
serious error.

```plot
{"title": "AlphaFold pLDDT confidence vs residue", "xLabel": "Residue index (relative)", "yLabel": "pLDDT", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "100/(1+exp(-(x-2)))-20*exp(-(x-7)^2)", "label": "Per-residue confidence", "color": "#2563eb"}]}
```

Finish with a scale bar or distance label, an explicit orientation, and only the
atoms the message needs — clutter is as harmful in 3-D as in 2-D.

**Next:** making figures interactive and AI-assisted.
""",
        ),
        _t(
            "Interactive & AI-assisted visualisation",
            "14 min",
            r"""
# Interactive & AI-assisted visualisation

Static figures are giving way to **interactive** ones for large or
high-dimensional data. The toolkit — Plotly, Bokeh, D3, Vega-Lite, and
notebook widgets — supports Shneiderman's mantra: *"overview first, zoom and
filter, then details on demand."* For genomics and single-cell atlases, tile
servers (Deck.gl, cellxgene) stream millions of points so users can pan, brush
and link selections across coordinated views.

```mermaid
flowchart LR
  A[Overview] --> B[Zoom + filter]
  B --> C[Brush / linked views]
  C --> D[Details on demand]
  D --> A
```

**AI now enters the pipeline** at three points. (1) *Generation* —
natural-language-to-chart systems and LLM copilots in notebooks translate a
prompt into Vega-Lite or ggplot code. (2) *Layout and embedding* — the
neural-network-based UMAP and parametric, GPU-accelerated t-SNE scale embeddings
to tens of millions of cells. (3) *Captioning and accessibility* — vision models
draft alt-text and summarise trends for screen readers.

```plot
{"title": "Embedding runtime scaling vs dataset size", "xLabel": "Cells (relative)", "yLabel": "Relative runtime", "xRange": [0, 10], "yRange": [0, 25], "grid": true, "functions": [{"expr": "x^1.2", "label": "Modern GPU embedding", "color": "#16a34a"}]}
```

The cautions sharpen rather than vanish. Interactivity must not hide the
default view's honesty; AI-generated charts inherit the model's blind spots and
**must be checked** for misleading axes, wrong scale types and fabricated trends;
and accessibility — colour-blind-safe palettes, alt-text, direct labels — is a
requirement, not a finishing touch.

**Next:** test your mastery.
""",
        ),
        _quiz(),
    ),
)


DATA_VISUALIZATION_BIO_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["DATA_VISUALIZATION_BIO_COURSES"]
