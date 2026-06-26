"""Single-Cell & Spatial Omics track: Basics -> Intermediate -> Advanced.

A university-level curriculum on single-cell biology: why bulk averages hide
heterogeneity, how scRNA-seq works (droplets, UMIs, barcodes), QC, normalization,
dimensionality reduction, clustering and cell-type annotation, then trajectories,
batch integration and spatial transcriptomics with modern computational/AI
methods. Lessons use interactive ```plot blocks for quantitative relationships
and ```mermaid diagrams for protocols, pipelines and decision flows.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Single-Cell & Spatial Omics -- Basics ------------------------------------

_BASICS = SeedCourse(
    slug="single-cell-omics-basics",
    title="Single-Cell & Spatial Omics — Basics",
    description=(
        "Why study one cell at a time. The limits of bulk averaging, the core "
        "idea of single-cell RNA sequencing, how droplet platforms capture cells "
        "and tag transcripts with barcodes and UMIs, and what a cell-by-gene "
        "count matrix is. Built on real molecular and experimental detail with "
        "interactive plots and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why single cell? The limits of bulk",
            "10 min",
            r"""
# Why single cell? The limits of bulk

Classic **bulk RNA-seq** grinds up a tissue and measures the *average*
expression across millions of cells. That average can be misleading: a gene that
looks "moderately expressed" in bulk may be **silent in 90% of cells and very
high in 10%** — two completely different biological stories with the same mean.
Bulk also cannot tell you *which* cell types are present or in what proportions.

**Single-cell RNA sequencing (scRNA-seq)** measures the transcriptome of each
cell separately, recovering the full **distribution** of expression, not just its
mean. This reveals rare populations (e.g. stem cells, a handful of malignant
clones), continuous states (differentiation), and cell-type composition.

```mermaid
flowchart LR
  TISSUE["Tissue (mixed cells)"] --> BULK["Bulk RNA-seq: one average profile"]
  TISSUE --> SC["scRNA-seq: one profile per cell"]
  SC --> TYPES["Cell types & states"]
  SC --> RARE["Rare populations"]
```

Consider a gene whose true mean is identical in two samples but whose
cell-to-cell distribution differs. A bulk assay reports only the mean (a flat
average); single-cell recovers the bimodal shape, here sketched as the
fraction of cells expressing at a given level:

```plot
{"title": "Bulk hides distribution shape", "xLabel": "expression level", "yLabel": "fraction of cells", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-(x-2)^2)+0.6*exp(-(x-7)^2)", "label": "true per-cell distribution", "color": "#2563eb"}, {"expr": "0.5", "label": "bulk average", "color": "#dc2626"}]}
```

**Next:** what scRNA-seq actually measures.
""",
        ),
        _t(
            "What scRNA-seq measures",
            "10 min",
            r"""
# What scRNA-seq measures

scRNA-seq counts **mRNA molecules** per gene per cell. The biology: a gene is
transcribed into mRNA; abundant mRNA usually means active expression. After
capture, each transcript is reverse-transcribed to cDNA, amplified and
sequenced. The output for each cell is a vector of **counts** — how many reads
(or, better, unique molecules) mapped to each gene.

Two protocol families dominate. **Full-length** methods (Smart-seq2/3) sequence
the whole transcript from a few hundred plate-sorted cells, giving high
sensitivity and isoform information. **Tag-based droplet** methods (10x
Chromium, Drop-seq) sequence only the transcript's 3' (or 5') end from tens of
thousands of cells — lower per-cell depth but massive throughput.

```mermaid
flowchart LR
  MRNA["mRNA in a cell"] --> RT["Reverse transcription -> cDNA"]
  RT --> AMP["Amplification"]
  AMP --> SEQ["Sequencing"]
  SEQ --> COUNTS["Per-gene counts (this cell)"]
```

Sensitivity is limited: only a fraction of a cell's mRNA is captured (often
**10-30%** for droplet methods). Detected genes rise with sequencing depth but
**saturate** — past a point, extra reads mostly re-sequence molecules you have
already seen:

```plot
{"title": "Genes detected saturate with sequencing depth", "xLabel": "reads per cell (relative)", "yLabel": "genes detected (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1.5)", "label": "saturation curve", "color": "#16a34a"}]}
```

**Next:** how droplet platforms capture single cells.
""",
        ),
        _t(
            "Droplets, barcodes and UMIs",
            "11 min",
            r"""
# Droplets, barcodes and UMIs

Droplet platforms isolate cells using **microfluidics**: a cell suspension and a
stream of **gel beads** (each coated with millions of primers) are co-flowed with
oil so that each aqueous droplet ideally contains **one cell + one bead**. Lysis
inside the droplet releases mRNA, which binds the bead's primers.

Each primer carries two short synthetic sequences:

- a **cell barcode** — identical on one bead, so every transcript from that
  droplet is tagged with the same barcode, marking which cell it came from;
- a **unique molecular identifier (UMI)** — a random ~10-12 nt tag that is
  *different* on each primer, so each captured mRNA molecule gets a unique label.

```mermaid
flowchart LR
  CELLS["Cell suspension"] --> MIX["Microfluidic junction"]
  BEADS["Barcoded gel beads"] --> MIX
  OIL["Oil"] --> MIX
  MIX --> DROP["Droplet: 1 cell + 1 bead"]
  DROP --> LIB["Barcoded + UMI-tagged library"]
```

UMIs let us **collapse PCR duplicates**: many reads sharing the same cell
barcode, gene and UMI are counted as **one** original molecule. This converts
read counts into molecule counts, removing amplification bias. Loading more
cells raises throughput but also the **doublet rate** (two cells in one droplet),
which grows roughly linearly with the number of cells loaded (Poisson statistics):

```plot
{"title": "Doublet rate rises with cells loaded", "xLabel": "cells loaded (thousands)", "yLabel": "approx doublet rate", "xRange": [0, 10], "yRange": [0, 0.1], "grid": true, "functions": [{"expr": "0.008*x", "label": "~0.8% per 1000 cells", "color": "#dc2626"}]}
```

**Next:** the count matrix that all analysis starts from.
""",
        ),
        _t(
            "The count matrix",
            "10 min",
            r"""
# The count matrix

After demultiplexing barcodes, aligning reads and collapsing UMIs, the data
becomes a **count matrix**: rows are **cells** (one per valid barcode), columns
are **genes**, and each entry is the number of UMIs for that gene in that cell.
A typical experiment is ~5,000 cells x ~20,000 genes.

This matrix is **sparse**: most entries are **zero**. A given cell only has a few
thousand mRNA molecules captured spread over thousands of detected genes, so 90%+
of the matrix is zero. Zeros come in two flavours: **biological zeros** (the gene
is truly off) and **technical zeros / dropouts** (the transcript existed but was
not captured) — distinguishing them is a central challenge.

```mermaid
flowchart LR
  FASTQ["Raw reads (FASTQ)"] --> ALIGN["Align + assign barcodes"]
  ALIGN --> UMI["Collapse UMIs"]
  UMI --> MTX["Cell x gene count matrix (sparse)"]
  MTX --> DS["AnnData / Seurat object"]
```

Tools such as **Cell Ranger**, **STARsolo** and **alevin-fry** (with **kallisto |
bustools**) produce this matrix; it is stored in formats like **AnnData (.h5ad)**
for **Scanpy** or a **Seurat** object in R. Total counts per cell (the **library
size**) vary widely and must be normalized before comparing cells — a Poisson-like
mean-variance relationship dominates the raw data:

```plot
{"title": "Raw counts: variance tracks the mean (Poisson-like)", "xLabel": "mean expression", "yLabel": "variance", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "x", "label": "Poisson (var = mean)", "color": "#2563eb"}, {"expr": "x+0.3*x^2", "label": "overdispersed (real data)", "color": "#dc2626"}]}
```

**Next:** telling real cells from empty droplets and debris.
""",
        ),
        _t(
            "From droplets to real cells: basic QC",
            "10 min",
            r"""
# From droplets to real cells: basic QC

Not every barcode is a healthy cell. **Quality control (QC)** filters out empty
droplets, debris, dying cells and doublets before analysis. Three per-cell
metrics drive most decisions:

- **Total counts** (library size) — too low suggests an empty droplet or
  ambient-RNA-only barcode; an extreme high may flag a doublet.
- **Number of detected genes** — very low means little signal.
- **Mitochondrial fraction** — the percentage of counts from mitochondrial
  genes. When a cell's membrane breaks, cytoplasmic mRNA leaks out but
  mitochondria are retained, so **dying/stressed cells show a high mito %**.

```mermaid
flowchart TB
  BARCODE["Each barcode"] --> Q1{"Counts in range?"}
  Q1 -- no --> DROP1["Discard (empty/doublet)"]
  Q1 -- yes --> Q2{"Mito % low?"}
  Q2 -- no --> DROP2["Discard (dying)"]
  Q2 -- yes --> KEEP["Keep: real cell"]
```

A **barcode rank plot** (counts per barcode, sorted descending, on log-log axes)
typically shows a "knee": a steep cliff separating real cells (left) from the
ambient background of empty droplets (right). Thresholds are chosen near the knee,
but should always be sanity-checked against the metric distributions rather than
applied blindly:

```plot
{"title": "Barcode rank plot: the knee separates cells from empties", "xLabel": "barcode rank (log)", "yLabel": "total counts (log)", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "5-4/(1+exp(-(x-5)))", "label": "counts vs rank", "color": "#2563eb"}]}
```

**Next:** test your single-cell foundations.
""",
        ),
        _quiz(),
    ),
)


# -- Single-Cell & Spatial Omics -- Intermediate ------------------------------

_INTERMEDIATE = SeedCourse(
    slug="single-cell-omics-intermediate",
    title="Single-Cell & Spatial Omics — Intermediate",
    description=(
        "The core quantitative pipeline. Normalization and variance stabilization, "
        "feature selection of highly variable genes, principal components and "
        "non-linear embeddings (UMAP/t-SNE), graph-based clustering with the "
        "Leiden algorithm, and principled cell-type annotation with marker genes. "
        "Practical, equation-grounded methods with interactive plots and diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Normalization and variance stabilization",
            "11 min",
            r"""
# Normalization and variance stabilization

Cells differ in **library size** for technical reasons (capture efficiency,
sequencing depth), so raw counts are not comparable. The standard recipe scales
each cell so its counts sum to a fixed total, then log-transforms:

$$x_{ij}' = \log\left(1 + \frac{c_{ij}}{N_i}\,s\right)$$

where $c_{ij}$ is the count of gene $j$ in cell $i$, $N_i$ is that cell's total
counts, and $s$ is a scale factor (often $10^4$ — "CP10K"). The $\log(1+x)$
**stabilizes variance** and tames the heavy right tail, so a handful of highly
expressed genes do not dominate downstream distances.

```mermaid
flowchart LR
  RAW["Raw counts"] --> SIZE["Divide by library size"]
  SIZE --> SCALE["x scale factor (CP10K)"]
  SCALE --> LOG["log(1 + x)"]
  LOG --> NORM["Normalized expression"]
```

Modern alternatives model counts directly. **sctransform** (Seurat) fits a
regularized **negative binomial** per gene and returns Pearson residuals;
analytic **Pearson residuals** (Scanpy) achieve similar variance stabilization
without choosing a size factor. The log1p curve compresses large values far more
than small ones, which is exactly the stabilization we want:

```plot
{"title": "log(1+x) compresses large counts", "xLabel": "raw count", "yLabel": "log(1 + count)", "xRange": [0, 10], "yRange": [0, 3], "grid": true, "functions": [{"expr": "log(1+x)", "label": "log1p", "color": "#2563eb"}]}
```

**Next:** picking the genes that carry signal.
""",
        ),
        _t(
            "Highly variable genes and feature selection",
            "10 min",
            r"""
# Highly variable genes and feature selection

Of ~20,000 genes, most are either off or uniformly "housekeeping" — they add
**noise, not structure**. Feature selection keeps the **highly variable genes
(HVGs)**, typically the top **2,000-3,000**, that vary more than expected given
their mean expression. Restricting to HVGs sharpens cell-type signal and speeds
up everything downstream.

The challenge is that, under technical (Poisson/NB) noise, **variance naturally
rises with the mean**, so the raw variance favours highly expressed genes. HVG
methods correct for this: Seurat's *vst* fits a mean-variance trend and ranks
genes by **standardized variance**; Scanpy's *seurat* and *cell_ranger* flavours
bin genes by mean and score **dispersion** within each bin.

```mermaid
flowchart LR
  GENES["All genes"] --> TREND["Fit mean-variance trend"]
  TREND --> RESID["Excess variance above trend"]
  RESID --> RANK["Rank genes"]
  RANK --> HVG["Top ~2000 HVGs"]
```

A gene is "highly variable" when its observed variance sits **above** the
expected technical trend; genes near or below the curve are dropped:

```plot
{"title": "HVGs sit above the technical mean-variance trend", "xLabel": "mean expression", "yLabel": "variance", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "x", "label": "expected (technical) trend", "color": "#2563eb"}, {"expr": "x+2", "label": "HVG threshold band", "color": "#16a34a"}]}
```

**Next:** compressing the data with PCA.
""",
        ),
        _t(
            "Dimensionality reduction: PCA to UMAP",
            "12 min",
            r"""
# Dimensionality reduction: PCA to UMAP

Even after HVG selection, each cell lives in ~2,000-dimensional space, where
distances become unreliable (the **curse of dimensionality**). The pipeline
reduces dimensions in two stages.

**Principal component analysis (PCA)** finds orthogonal linear axes (principal
components) capturing the most variance. Keeping the top **~30-50 PCs**
denoises the data and captures the major axes of biological variation; PCA is
linear, fast and the input to the neighbour graph. The variance explained per
PC falls off sharply — an **elbow/scree plot** guides how many to keep:

```plot
{"title": "Scree plot: variance explained per principal component", "xLabel": "principal component", "yLabel": "variance explained (%)", "xRange": [1, 10], "yRange": [0, 30], "grid": true, "functions": [{"expr": "28*exp(-0.45*x)", "label": "variance per PC", "color": "#2563eb"}]}
```

**UMAP** and **t-SNE** then take the top PCs and produce a **2D embedding** for
visualization. They are **non-linear** and preserve **local** neighbourhoods.
Crucially: UMAP/t-SNE distances and cluster sizes are **not quantitatively
meaningful** — they are display tools, not the basis for clustering.

```mermaid
flowchart LR
  NORM["Normalized HVG matrix"] --> PCA["PCA (top ~30-50 PCs)"]
  PCA --> KNN["k-nearest-neighbour graph"]
  PCA --> UMAP["UMAP / t-SNE (2D plot)"]
  KNN --> CLUST["Clustering"]
```

**Next:** clustering cells into populations.
""",
        ),
        _t(
            "Graph-based clustering with Leiden",
            "11 min",
            r"""
# Graph-based clustering with Leiden

Single-cell clustering is dominated by **graph-based community detection**, not
k-means. First build a **k-nearest-neighbour (kNN) graph** in PC space (each cell
links to its k most similar cells), often refined into a **shared nearest
neighbour (SNN)** graph weighted by neighbour overlap. Then partition the graph
into densely connected **communities** — the clusters.

The **Leiden** algorithm optimizes **modularity** $Q$: it rewards more edges
inside communities than expected by chance.

$$Q = \frac{1}{2m}\sum_{ij}\left(A_{ij} - \frac{k_i k_j}{2m}\right)\delta(c_i,c_j)$$

Leiden improved on **Louvain** by guaranteeing **well-connected** communities
(Louvain could yield internally disconnected clusters). A **resolution**
parameter tunes granularity: higher resolution -> more, smaller clusters.

```mermaid
flowchart LR
  PCA["PCs"] --> KNN["kNN / SNN graph"]
  KNN --> LEIDEN["Leiden community detection"]
  LEIDEN --> CLUSTERS["Clusters"]
  RES["resolution parameter"] --> LEIDEN
```

Cluster count grows monotonically with the resolution parameter, so it is tuned
to match known biology (and checked for over-splitting):

```plot
{"title": "Cluster count rises with Leiden resolution", "xLabel": "resolution", "yLabel": "number of clusters", "xRange": [0, 2], "yRange": [0, 20], "grid": true, "functions": [{"expr": "2+8*x", "label": "clusters vs resolution", "color": "#16a34a"}]}
```

**Next:** turning clusters into cell types.
""",
        ),
        _t(
            "Cell-type annotation with marker genes",
            "11 min",
            r"""
# Cell-type annotation with marker genes

A cluster is just a number until it is **annotated** with a biological identity.
The classic approach is **differential expression**: for each cluster, find genes
**up-regulated versus the rest** (Scanpy's `rank_genes_groups`, Seurat's
`FindMarkers`, using Wilcoxon rank-sum or a t-test). The top markers are matched
against **canonical cell-type signatures** — e.g. **CD3D/CD3E** for T cells,
**CD19/MS4A1** for B cells, **CD14/LYZ** for monocytes, **PECAM1** for
endothelium.

```mermaid
flowchart LR
  CLUSTER["Cluster k"] --> DE["DE vs rest (Wilcoxon)"]
  DE --> MARKERS["Top up-regulated genes"]
  MARKERS --> MATCH["Match to known signatures"]
  MATCH --> LABEL["Cell-type label"]
```

A good marker is **specific** (expressed in the target type, off elsewhere) and
**sensitive** (expressed in most target cells). Automated tools help at scale:
**reference-based** classifiers (**SingleR**, **Azimuth**, **CellTypist**)
project query cells onto a labelled reference, and **scoring** methods compute a
per-cell signature score. A specific marker's expression rises steeply with the
fraction of true target cells in a cluster, behaving like a sigmoid switch:

```plot
{"title": "A good marker switches on in the target cell type", "xLabel": "marker expression level", "yLabel": "prob. cell is target type", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "specificity (sigmoid)", "color": "#2563eb"}]}
```

**Next:** test your single-cell analysis skills.
""",
        ),
        _quiz(),
    ),
)


# -- Single-Cell & Spatial Omics -- Advanced ----------------------------------

_ADVANCED = SeedCourse(
    slug="single-cell-omics-advanced",
    title="Single-Cell & Spatial Omics — Advanced",
    description=(
        "State-of-the-art single-cell and spatial methods. Trajectory inference "
        "and pseudotime, RNA velocity, batch integration and deep generative "
        "models (Harmony, scVI), foundation models for single cells, and the "
        "rise of spatial transcriptomics — imaging- and sequencing-based — with "
        "cell-cell communication. Frontier methods with interactive plots and "
        "pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Trajectory inference and pseudotime",
            "12 min",
            r"""
# Trajectory inference and pseudotime

Many biological processes — differentiation, the cell cycle, activation — are
**continuous**, not discrete clusters. **Trajectory inference** orders cells
along these continua and assigns each a **pseudotime**: a scalar estimating how
far it has progressed, inferred from transcriptomic similarity rather than a
clock.

Methods build a graph or tree over cells and compute distances from a chosen
**root**. **Slingshot** fits smooth principal curves through clusters;
**Monocle 3** learns a principal graph allowing branches; **PAGA** (Scanpy)
abstracts clusters into a coarse connectivity graph that preserves global
topology, useful as a trustworthy backbone for an embedding.

```mermaid
flowchart LR
  CELLS["Cells in PC space"] --> GRAPH["Graph / principal curve"]
  ROOT["Root cell / cluster"] --> PT["Pseudotime ordering"]
  GRAPH --> PT
  PT --> DYN["Gene dynamics along pseudotime"]
```

Plotting a gene against pseudotime reveals dynamics: transient genes peak then
fall; a lineage-priming transcription factor may rise monotonically. A classic
transient activation peak looks like:

```plot
{"title": "Transient gene expression along pseudotime", "xLabel": "pseudotime", "yLabel": "expression", "xRange": [0, 10], "yRange": [0, 4], "grid": true, "functions": [{"expr": "4*x*exp(-0.6*x)", "label": "transient peak", "color": "#2563eb"}]}
```

**Next:** adding direction with RNA velocity.
""",
        ),
        _t(
            "RNA velocity",
            "11 min",
            r"""
# RNA velocity

Pseudotime gives an *ordering* but not a *direction* — which end is the start?
**RNA velocity** adds the arrow of time by exploiting **unspliced (intronic)**
versus **spliced (mature)** mRNA. Newly transcribed pre-mRNA contains introns;
splicing removes them; mature mRNA is then degraded. Counting reads in introns
vs exons estimates both species per gene per cell.

The original model (La Manno et al.) is a simple kinetic system:

$$\frac{du}{dt} = \alpha - \beta u, \qquad \frac{ds}{dt} = \beta u - \gamma s$$

where $u$ is unspliced, $s$ spliced, $\alpha$ transcription, $\beta$ splicing and
$\gamma$ degradation. If a gene has **more unspliced than its steady-state ratio**
predicts, it is being **up-regulated** (future state higher); less unspliced
means it is shutting down. **scVelo** generalized this to a dynamical model.

```mermaid
flowchart LR
  DNA["Transcription (alpha)"] --> U["Unspliced u"]
  U -->|splicing beta| S["Spliced s"]
  S -->|degradation gamma| DEG["Degraded"]
  U --> VEL["Velocity = du,ds -> arrows"]
```

At steady state $s = (\beta/\gamma)\,u$, a straight line. Points **above** the
line have excess spliced (down-regulating); points **below** have excess
unspliced (up-regulating). The steady-state line:

```plot
{"title": "Velocity phase portrait: spliced vs unspliced at steady state", "xLabel": "unspliced (u)", "yLabel": "spliced (s)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.8*x", "label": "steady-state ratio", "color": "#2563eb"}]}
```

**Next:** removing batch effects across datasets.
""",
        ),
        _t(
            "Batch effects and data integration",
            "12 min",
            r"""
# Batch effects and data integration

Combining samples from different **batches** (donors, days, chemistries, labs)
introduces **technical variation** that can dominate biology: cells cluster by
batch instead of by cell type. **Integration** aligns shared cell types across
batches while preserving genuine biological differences — a delicate balance
between **over-correction** (erasing real signal) and **under-correction**.

A spectrum of methods exists. **Harmony** iteratively clusters in PCA space and
applies soft, cluster-specific linear corrections — fast and effective.
**Seurat CCA/anchors** and **MNN/fastMNN** find **mutual nearest neighbours**
across batches as anchors. **scVI** (next lesson) learns a batch-conditioned
latent space. **BBKNN** modifies the neighbour graph directly.

```mermaid
flowchart LR
  B1["Batch 1"] --> ANCH["Find shared cell types / anchors"]
  B2["Batch 2"] --> ANCH
  ANCH --> CORR["Correct embedding"]
  CORR --> JOINT["Integrated space (cell type, not batch)"]
```

Integration quality is judged by a **trade-off**: **batch mixing** (e.g. kBET,
iLISI) should be high while **biological conservation** (cell-type ARI, cLISI)
stays high — benchmarked by frameworks like **scIB**. Pushing correction
strength improves mixing but eventually destroys biology, so the useful operating
point is a knee, not the maximum:

```plot
{"title": "Integration trade-off: mixing vs biology conservation", "xLabel": "correction strength", "yLabel": "score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "batch mixing", "color": "#16a34a"}, {"expr": "1-1/(1+exp(-(x-7)))", "label": "biology conserved", "color": "#dc2626"}]}
```

**Next:** deep generative and foundation models.
""",
        ),
        _t(
            "Deep generative and foundation models",
            "12 min",
            r"""
# Deep generative and foundation models

Single-cell data is ideal for **deep learning**: millions of high-dimensional,
noisy, sparse observations. **scVI** (single-cell Variational Inference) is the
workhorse: a **variational autoencoder** that models counts with a **zero-inflated
or standard negative binomial** likelihood, encoding each cell into a low-
dimensional **latent space** while conditioning on batch to integrate. From it
follow **scANVI** (semi-supervised annotation), **totalVI** (CITE-seq protein +
RNA) and **PeakVI** (ATAC).

```mermaid
flowchart LR
  COUNTS["Count matrix + batch"] --> ENC["Encoder q(z|x)"]
  ENC --> Z["Latent z (batch-corrected)"]
  Z --> DEC["Decoder -> NB / ZINB params"]
  DEC --> RECON["Reconstructed counts"]
  Z --> USE["Clustering, integration, DE"]
```

The newest frontier is **foundation models** — transformers pretrained on tens of
millions of cells (**scGPT**, **Geneformer**, **scFoundation**). By learning
general "grammar" of gene co-expression, they can be **fine-tuned** for cell-type
annotation, perturbation prediction, batch integration and gene-network
inference, often with little labelled data. As with NLP, performance tends to
**scale** with pretraining cells and parameters (with diminishing returns):

```plot
{"title": "Foundation-model performance scales with pretraining data", "xLabel": "log pretraining cells", "yLabel": "downstream performance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "performance vs scale", "color": "#2563eb"}]}
```

**Next:** putting cells back in space.
""",
        ),
        _t(
            "Spatial transcriptomics",
            "12 min",
            r"""
# Spatial transcriptomics

Dissociating tissue for scRNA-seq discards **where** each cell was. **Spatial
transcriptomics (ST)** measures expression while preserving **tissue
coordinates**, revealing niches, gradients and microenvironments. Two technology
families dominate:

- **Imaging-based** (**MERFISH**, **seqFISH+**, **Xenium**, **CosMx**):
  single-molecule FISH with combinatorial barcodes images **hundreds to
  thousands of targeted genes** at **subcellular** resolution.
- **Sequencing-based** (**Visium**, **Slide-seq/Slide-seqV2**, **Stereo-seq**):
  capture mRNA on a spatially barcoded array, giving **transcriptome-wide**
  coverage at spot resolution (Visium spots span several cells; Slide-seq and
  Stereo-seq approach single-cell).

```mermaid
flowchart LR
  TISSUE["Tissue section"] --> IMG["Imaging-based: MERFISH/Xenium (targeted, subcellular)"]
  TISSUE --> SEQ["Seq-based: Visium/Slide-seq (whole tx, spots)"]
  IMG --> MAP["Gene expression + (x,y) coordinates"]
  SEQ --> MAP
  MAP --> NICHE["Spatial domains & niches"]
```

There is a fundamental **resolution-vs-coverage trade-off**: imaging methods give
subcellular resolution but a limited gene panel; sequencing methods give the
whole transcriptome but coarser spots. Analysis adds spatial questions:
**deconvolving** multi-cell spots (cell2location, RCTD), finding **spatially
variable genes** (SpatialDE, SPARK), detecting **spatial domains** (SpaGCN), and
inferring **cell-cell communication** from ligand-receptor proximity (CellPhoneDB,
Squidpy). Spatial autocorrelation (e.g. Moran's I) typically **decays with
distance** between spots:

```plot
{"title": "Spatial autocorrelation decays with distance", "xLabel": "distance between spots", "yLabel": "expression correlation", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "correlation decay", "color": "#16a34a"}]}
```

**Next:** test your advanced single-cell and spatial knowledge.
""",
        ),
        _quiz(),
    ),
)


SINGLE_CELL_OMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["SINGLE_CELL_OMICS_COURSES"]
