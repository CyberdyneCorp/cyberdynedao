"""Transcriptomics (RNA-Seq) track: Basics -> Intermediate -> Advanced.

A university-level RNA-seq curriculum: from the transcriptome, library
preparation and experimental design, through alignment, quantification,
normalization and differential expression, to pathway and co-expression
analysis, isoform/transcript inference and single-cell methods. Lessons use
interactive ```plot blocks for quantitative relationships (saturation, dispersion,
dose-response, power) and ```mermaid diagrams for processes, pipelines and
classifications.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Transcriptomics -- Basics ------------------------------------------------

_BASICS = SeedCourse(
    slug="transcriptomics-basics",
    title="Transcriptomics (RNA-Seq) — Basics",
    description=(
        "What the transcriptome is and how we measure it. The biology of RNA "
        "and gene expression, the chemistry of an RNA-seq library, how reads "
        "become counts, and the core ideas of experimental design and "
        "replication. Built on real molecular detail with interactive plots and "
        "process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is the transcriptome?",
            "10 min",
            r"""
# What is the transcriptome?

The **transcriptome** is the complete set of RNA molecules present in a cell,
tissue or sample at a given time. Unlike the genome, which is essentially fixed,
the transcriptome is **dynamic**: it changes with cell type, developmental stage,
environment and disease. Measuring it tells us *which genes are on, and how
strongly*.

A human cell transcribes a small fraction of its ~20,000 protein-coding genes at
any moment, plus thousands of **non-coding RNAs** (lncRNAs, miRNAs, snoRNAs).
Most of the *mass* of total RNA is **ribosomal RNA (rRNA)**, ~80–90%, while the
information-rich **messenger RNA (mRNA)** is only ~1–5%. This is why library prep
must either select mRNA or deplete rRNA.

```mermaid
flowchart LR
  GENOME["Genome (fixed DNA)"] --> TX["Transcription"]
  TX --> TRANSCRIPTOME["Transcriptome (RNA snapshot)"]
  TRANSCRIPTOME --> MRNA["mRNA (~1-5%)"]
  TRANSCRIPTOME --> RRNA["rRNA (~80-90%)"]
  TRANSCRIPTOME --> NCRNA["ncRNA (lncRNA, miRNA)"]
```

Expression levels span many orders of magnitude — a few highly expressed genes
dominate the read budget, while most genes are expressed at low levels:

```plot
{"title": "Gene expression is highly skewed (rank-abundance)", "xLabel": "gene rank", "yLabel": "relative abundance", "xRange": [0.2, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/x", "label": "abundance", "color": "#2563eb"}]}
```

**Next:** the central dogma and what RNA-seq actually counts.
""",
        ),
        _t(
            "From gene to RNA: the central dogma",
            "11 min",
            r"""
# From gene to RNA: the central dogma

RNA-seq measures the **product of transcription**. In eukaryotes, RNA
polymerase II transcribes a **pre-mRNA** that is processed: a **5' cap** is
added, **introns are spliced out**, and a **poly(A) tail** of ~100–250 adenines
is appended. The mature mRNA is exported and translated.

Two features matter for RNA-seq. First, the **poly(A) tail** lets us capture
mRNA with **oligo-dT** beads. Second, **alternative splicing** means one gene can
produce many **isoforms**; a read mapping to a shared exon cannot, by itself,
tell us which isoform it came from.

```mermaid
flowchart LR
  DNA["Gene (DNA)"] --> PRE["Pre-mRNA"]
  PRE --> CAP["5' cap + splicing + poly(A)"]
  CAP --> MRNA["Mature mRNA"]
  MRNA --> ISO["Isoforms (alternative splicing)"]
```

The **steady-state** level of an mRNA reflects a balance between its synthesis
rate and its degradation. With first-order decay, after transcription stops the
abundance falls exponentially with a transcript-specific half-life:

```plot
{"title": "mRNA decays exponentially after transcription stops", "xLabel": "time (half-lives)", "yLabel": "relative mRNA level", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "mRNA level", "color": "#dc2626"}]}
```

**Next:** how an RNA-seq library is built in the lab.
""",
        ),
        _t(
            "Building an RNA-seq library",
            "12 min",
            r"""
# Building an RNA-seq library

To sequence RNA we must convert it into a DNA library compatible with an
Illumina (or similar) sequencer. The standard short-read workflow is:

1. **RNA selection** — either **poly(A) selection** (oligo-dT capture of mRNA)
   or **rRNA depletion** (e.g. RiboZero), which also retains non-polyadenylated
   and degraded RNA.
2. **Fragmentation** of RNA into ~200–400 nt pieces.
3. **Reverse transcription** to **cDNA**, sometimes with strand marking (dUTP
   method) to preserve **strandedness**.
4. **Adapter ligation** and **PCR amplification** to add sequencing handles and
   indices.

```mermaid
flowchart LR
  RNA["Total RNA"] --> SEL["polyA select / rRNA deplete"]
  SEL --> FRAG["Fragment"]
  FRAG --> CDNA["Reverse-transcribe to cDNA"]
  CDNA --> ADAPT["Ligate adapters + PCR"]
  ADAPT --> SEQ["Sequence"]
```

PCR is a double-edged step: it lets us sequence tiny inputs but introduces
**duplicates** and amplification bias. The number of distinct molecules captured
saturates as we sequence deeper — a key reason why **library complexity** limits
how much extra depth helps:

```plot
{"title": "Distinct molecules saturate with sequencing depth", "xLabel": "reads sequenced (relative)", "yLabel": "unique molecules detected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "unique molecules", "color": "#16a34a"}]}
```

**Next:** how raw reads turn into a count matrix.
""",
        ),
        _t(
            "From reads to a count matrix",
            "11 min",
            r"""
# From reads to a count matrix

A sequencer outputs millions of short **reads** (FASTQ files). To know which
gene each read came from, we **align** reads to a reference genome with a
**splice-aware** aligner (e.g. **STAR**, **HISAT2**) — splice-aware because a
read can straddle an exon–exon junction. Alternatively, **pseudo-alignment**
tools (**salmon**, **kallisto**) skip base-level alignment and assign reads to
transcripts directly, which is much faster.

We then **count** reads per gene (e.g. with **featureCounts** or **HTSeq**) to
build a **count matrix**: rows = genes, columns = samples, entries = read counts.
This matrix is the input to nearly all downstream analysis.

```mermaid
flowchart LR
  FASTQ["FASTQ reads"] --> QC["QC + trim (FastQC, Trim Galore)"]
  QC --> ALN["Align (STAR) or pseudo-align (salmon)"]
  ALN --> CNT["Count per gene (featureCounts)"]
  CNT --> MAT["Count matrix (genes x samples)"]
```

Counts are **discrete and non-negative**, and a longer or more highly expressed
gene yields more reads. The expected count for a gene rises with its true
expression but saturates relative to total library size, motivating the
normalization we meet next:

```plot
{"title": "Expected gene counts vs true expression", "xLabel": "true expression (relative)", "yLabel": "expected read count", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "expected counts", "color": "#2563eb"}]}
```

**Next:** why raw counts are not comparable, and how to normalize.
""",
        ),
        _t(
            "Normalization: CPM, TPM and FPKM",
            "11 min",
            r"""
# Normalization: CPM, TPM and FPKM

Raw counts are not comparable across samples or genes because of two nuisances:
**sequencing depth** (some libraries are bigger) and **gene length** (longer
genes catch more reads). Normalization corrects these.

- **CPM** (counts per million) divides by library size: $\text{CPM} =
  \frac{c \times 10^6}{N}$, where $c$ is the gene's count and $N$ the total
  mapped reads. It fixes depth but not length.
- **FPKM/RPKM** additionally divides by gene length in kilobases.
- **TPM** (transcripts per million) normalizes by length **first**, then by
  total, so every sample's TPM values **sum to the same total** ($10^6$). This
  makes TPM the preferred *within-sample* relative measure.

```mermaid
flowchart TB
  COUNTS["Raw counts"] --> DEPTH["Correct for depth"]
  COUNTS --> LEN["Correct for gene length"]
  DEPTH --> CPM["CPM"]
  LEN --> TPM["TPM / FPKM"]
```

Crucially, these metrics are good for **visualization and ranking within a
sample**, but differential expression tools work on **raw counts** with their own
internal normalization (we will see why). The relationship between CPM and raw
count is simply linear at fixed depth:

```plot
{"title": "CPM scales linearly with raw count at fixed depth", "xLabel": "raw count", "yLabel": "CPM (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "CPM", "color": "#16a34a"}]}
```

**Next:** designing an experiment that can actually detect change.
""",
        ),
        _t(
            "Experimental design and replication",
            "10 min",
            r"""
# Experimental design and replication

Good RNA-seq starts before any sequencing. The dominant source of uncertainty in
detecting differential expression is **biological variability** between
replicates — not sequencing noise. Three principles guide design:

- **Replication**: use **biological replicates** (independent samples), not just
  technical ones. Three is a practical minimum; more replicates beat more depth
  for detecting moderate fold changes.
- **Randomization and blocking**: spread conditions across sequencing lanes and
  days to avoid **batch effects** being confounded with biology.
- **Depth**: ~20–30 million reads per sample is typical for gene-level
  differential expression; isoform work needs more.

```mermaid
flowchart LR
  Q["Biological question"] --> REP["Biological replicates >= 3"]
  Q --> RAND["Randomize across batches"]
  REP --> POW["Statistical power"]
  RAND --> POW
  POW --> DE["Reliable differential expression"]
```

Statistical **power** — the chance of detecting a real effect — rises with
replicate number and saturates: going from 2 to 4 replicates helps far more than
8 to 10:

```plot
{"title": "Power rises with replicates and saturates", "xLabel": "biological replicates per group", "yLabel": "power to detect change", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "power", "color": "#dc2626"}]}
```

**Next:** check your understanding of RNA-seq fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Transcriptomics -- Intermediate ------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="transcriptomics-intermediate",
    title="Transcriptomics (RNA-Seq) — Intermediate",
    description=(
        "The quantitative core of RNA-seq analysis. Count distributions and the "
        "negative binomial model, library normalization with median-of-ratios "
        "and TMM, differential expression with DESeq2 and edgeR, multiple-testing "
        "control, shrinkage and visualization. Hands-on statistical reasoning with "
        "interactive plots and pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Count distributions and overdispersion",
            "12 min",
            r"""
# Count distributions and overdispersion

RNA-seq counts are integers, so a natural first model is the **Poisson**
distribution, where the variance equals the mean ($\text{Var}=\mu$). Poisson
holds well for **technical** replicates. But across **biological** replicates,
the variance is consistently **larger** than the mean — a phenomenon called
**overdispersion**.

The standard fix is the **negative binomial (NB)** distribution, which adds a
**dispersion** parameter $\alpha$:

$$\text{Var}(Y) = \mu + \alpha\,\mu^2$$

When $\alpha \to 0$ the NB collapses to Poisson; larger $\alpha$ means more
biological variability. DESeq2 and edgeR both build on this model.

```mermaid
flowchart LR
  COUNTS["Gene counts"] --> POIS["Poisson (Var = mean)"]
  POIS --> OVER["Biological reps: Var > mean"]
  OVER --> NB["Negative binomial (Var = mu + a*mu^2)"]
```

The extra variance grows **quadratically** with the mean, so highly expressed
genes are noisier in absolute terms than Poisson would predict:

```plot
{"title": "Negative binomial variance exceeds the mean", "xLabel": "mean count (mu)", "yLabel": "variance", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "x", "label": "Poisson (Var=mu)", "color": "#2563eb"}, {"expr": "x+0.1*x^2", "label": "NB (Var=mu+a*mu^2)", "color": "#dc2626"}]}
```

**Next:** normalizing across samples for differential expression.
""",
        ),
        _t(
            "Normalization for differential expression",
            "12 min",
            r"""
# Normalization for differential expression

TPM and CPM correct depth and length but assume libraries are *comparable in
composition*. They are not: if a few genes dominate one condition, they "steal"
reads from everything else, biasing simple per-million scaling. Differential
expression tools therefore use **composition-aware** normalization.

- **DESeq2 — median of ratios**: compute, for each gene, the ratio of its count
  to a **geometric mean** across samples; the sample's **size factor** is the
  **median** of these ratios. Robust to a few highly variable genes.
- **edgeR — TMM** (trimmed mean of M-values): estimate a scaling factor from the
  trimmed set of log-ratios, excluding extreme genes.

```mermaid
flowchart TB
  RAW["Raw counts"] --> GEO["DESeq2: ratio to geometric mean"]
  RAW --> MV["edgeR: log-ratios (M-values)"]
  GEO --> SF["Size factor = median of ratios"]
  MV --> TMM["TMM scaling factor"]
  SF --> NORM["Normalized counts"]
  TMM --> NORM
```

The **median** is the key robustness trick: it ignores the handful of strongly
differential genes that would distort a mean. A normalization factor near 1
means a sample is typical; values drift from 1 as library composition shifts:

```plot
{"title": "Size factor scales a library to a common reference", "xLabel": "relative library composition", "yLabel": "scaling applied", "xRange": [0, 10], "yRange": [0, 2], "grid": true, "functions": [{"expr": "2*x/(x+5)", "label": "size factor", "color": "#16a34a"}]}
```

**Next:** testing for differential expression and shrinkage.
""",
        ),
        _t(
            "Differential expression with DESeq2 and edgeR",
            "13 min",
            r"""
# Differential expression with DESeq2 and edgeR

**Differential expression (DE)** asks whether a gene's mean count differs
between conditions, accounting for biological variability. DESeq2 and edgeR fit a
**negative binomial generalized linear model (GLM)** per gene:

$$\log_2(\mu_{ij}) = \beta_0 + \beta_1 x_j + \log(s_j)$$

where $x_j$ encodes condition, $\beta_1$ is the **log2 fold change**, and $s_j$
is the size factor (an offset). A **Wald test** (DESeq2) or **likelihood-ratio
test** (edgeR) gives a p-value per gene.

The hard part is estimating dispersion from few replicates. Both tools
**shrink** each gene's noisy dispersion estimate toward a fitted **mean–variance
trend** (empirical Bayes), stabilizing low-replicate experiments.

```mermaid
flowchart LR
  CNT["Count matrix"] --> DISP["Estimate dispersion per gene"]
  DISP --> SHRINK["Shrink toward trend (empirical Bayes)"]
  SHRINK --> GLM["Fit NB GLM"]
  GLM --> TEST["Wald / LRT test"]
  TEST --> RES["log2FC + p-value per gene"]
```

Per-gene dispersion estimates are unreliable at low counts; shrinkage pulls them
toward a smooth trend that declines as expression rises:

```plot
{"title": "Fitted dispersion trend declines with expression", "xLabel": "mean normalized count (log scale)", "yLabel": "dispersion estimate", "xRange": [0.2, 10], "yRange": [0, 2], "grid": true, "functions": [{"expr": "0.2+1/x", "label": "dispersion trend", "color": "#dc2626"}]}
```

**Next:** controlling the flood of false positives.
""",
        ),
        _t(
            "Multiple testing and the false discovery rate",
            "11 min",
            r"""
# Multiple testing and the false discovery rate

A typical experiment tests ~15,000–20,000 genes simultaneously. At a raw
threshold of $p<0.05$, even with **no real differences** we would expect ~1,000
false positives. We must adjust for **multiple testing**.

Controlling the **family-wise error rate** (e.g. **Bonferroni**, dividing the
threshold by the number of tests) is far too strict for genomics. Instead we
control the **false discovery rate (FDR)** — the expected *proportion* of false
positives **among the genes we call significant** — using the
**Benjamini–Hochberg** procedure. An **adjusted p-value (q-value)** of 0.05 means
~5% of the called genes are expected to be false.

```mermaid
flowchart LR
  PVALS["Raw p-values (all genes)"] --> SORT["Rank ascending"]
  SORT --> BH["Benjamini-Hochberg"]
  BH --> Q["Adjusted p-values (FDR / q)"]
  Q --> SIG["Significant set at FDR 5%"]
```

Under the null, p-values are **uniform**; a real signal piles up extra small
p-values. The BH threshold rises with rank, accepting more genes as the evidence
density at small p increases. The number of expected false positives grows
linearly with how many tests you do at a fixed cutoff:

```plot
{"title": "Expected false positives grow with the number of tests", "xLabel": "tests (thousands)", "yLabel": "expected false positives", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "FP at p<0.001", "color": "#dc2626"}]}
```

**Next:** reading the standard DE diagnostic plots.
""",
        ),
        _t(
            "Visualizing results: MA, volcano and PCA",
            "11 min",
            r"""
# Visualizing results: MA, volcano and PCA

DE output is summarized with a few canonical plots, each answering a different
question.

- **MA plot**: log2 fold change (M, y-axis) versus mean expression (A, x-axis).
  Reveals whether fold changes depend on expression level and exposes the need
  for **fold-change shrinkage** (DESeq2's `lfcShrink`), which pulls in noisy
  low-count estimates.
- **Volcano plot**: log2 fold change (x) versus $-\log_{10}$ p-value (y).
  Significant, large-effect genes sit in the upper corners.
- **PCA / sample clustering**: on **variance-stabilized** counts, checks whether
  samples group by biology rather than by batch — a key quality control.

```mermaid
flowchart LR
  RES["DE results"] --> MA["MA plot (M vs A)"]
  RES --> VOLC["Volcano (logFC vs -log10 p)"]
  VST["Variance-stabilized counts"] --> PCA["PCA / clustering"]
  PCA --> QC["Detect batch effects"]
```

Without shrinkage, low-count genes show wildly inflated fold changes; the
$-\log_{10}$ transform on the volcano y-axis stretches small p-values so the
strongest hits separate cleanly:

```plot
{"title": "The -log10 transform stretches small p-values", "xLabel": "p-value", "yLabel": "-log10(p)", "xRange": [0.001, 1], "yRange": [0, 3], "grid": true, "functions": [{"expr": "-log(x)/log(10)", "label": "-log10(p)", "color": "#2563eb"}]}
```

**Next:** turning gene lists into biological meaning.
""",
        ),
        _t(
            "From gene lists to biology: an overview",
            "10 min",
            r"""
# From gene lists to biology: an overview

A DE analysis yields a list of significant genes — but a list is not an
explanation. The next step is to ask **what those genes have in common**:
shared pathways, functions or regulators.

Two broad strategies exist. **Over-representation analysis (ORA)** takes your
significant gene set and asks, via a **hypergeometric / Fisher's exact test**,
whether any annotated category (a **GO term** or **KEGG pathway**) appears more
often than expected by chance. **Gene set enrichment analysis (GSEA)** instead
uses the **whole ranked list** and detects categories whose genes cluster toward
the top or bottom, catching coordinated but individually modest changes.

```mermaid
flowchart LR
  DE["DE gene list / ranked list"] --> ORA["ORA: hypergeometric on significant set"]
  DE --> GSEA["GSEA: enrichment on full ranking"]
  ORA --> PATH["Enriched GO / KEGG terms"]
  GSEA --> PATH
  PATH --> BIO["Biological interpretation"]
```

ORA's significance depends on the overlap between your gene set and a pathway; as
the overlap grows, the enrichment p-value falls sharply (more $-\log_{10}$
significance):

```plot
{"title": "Enrichment significance rises with pathway overlap", "xLabel": "genes overlapping a pathway", "yLabel": "enrichment significance (-log10 p)", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "0.6*x", "label": "-log10 p", "color": "#16a34a"}]}
```

**Next:** check your understanding of quantitative RNA-seq.
""",
        ),
        _quiz(),
    ),
)


# -- Transcriptomics -- Advanced ----------------------------------------------

_ADVANCED = SeedCourse(
    slug="transcriptomics-advanced",
    title="Transcriptomics (RNA-Seq) — Advanced",
    description=(
        "State-of-the-art and applied transcriptomics. Pathway and gene-set "
        "enrichment, weighted gene co-expression networks (WGCNA), isoform and "
        "transcript-level inference, single-cell RNA-seq and its computational "
        "stack, long-read and spatial methods, and deep-learning models for "
        "expression. Rigorous methods with interactive plots and pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Pathway and gene-set enrichment analysis",
            "13 min",
            r"""
# Pathway and gene-set enrichment analysis

Beyond simple over-representation, **GSEA** (Subramanian et al., 2005) tests
whether a predefined gene set is concentrated at the top or bottom of a list
ranked by, say, the DE statistic. It walks the ranked list computing a running
**enrichment score (ES)** — increasing at set members, decreasing otherwise —
and takes the maximum deviation from zero. Significance comes from
**permutation** (of sample labels or genes), and an FDR adjusts for testing many
sets.

Modern variants include **fgsea** (fast pre-ranked GSEA), **camera** (accounting
for inter-gene correlation), and **GSVA** (per-sample pathway scores for
downstream modeling). Curated collections live in **MSigDB** (Hallmark, C2, GO).

```mermaid
flowchart LR
  RANK["Genes ranked by DE statistic"] --> WALK["Running enrichment score"]
  WALK --> ES["Max deviation = ES"]
  ES --> PERM["Permutation null"]
  PERM --> FDR["FDR-adjusted significance"]
```

The running sum rises as set members are encountered early in the ranking and
falls back over the bulk of non-members; a set enriched at the top produces a
clear positive peak before decaying:

```plot
{"title": "GSEA running enrichment score peaks then decays", "xLabel": "rank position in list (relative)", "yLabel": "running enrichment score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x*exp(-0.6*x)*1.6", "label": "running ES", "color": "#2563eb"}]}
```

**Next:** building networks from co-expression.
""",
        ),
        _t(
            "Co-expression networks and WGCNA",
            "13 min",
            r"""
# Co-expression networks and WGCNA

**WGCNA** (Weighted Gene Co-expression Network Analysis) groups genes that vary
together across samples into **modules**, then relates modules to traits. Rather
than thresholding correlations into a hard (0/1) network, WGCNA raises the
absolute correlation to a **soft-thresholding power** $\beta$:

$$a_{ij} = |\text{cor}(i,j)|^{\beta}$$

This emphasizes strong correlations and suppresses weak, noisy ones, yielding a
network that better approximates **scale-free** topology. Modules are found by
hierarchical clustering on the **topological overlap measure (TOM)**, summarized
by their first principal component (the **module eigengene**), and correlated
with phenotypes; central genes are **hubs**.

```mermaid
flowchart LR
  EXPR["Expression matrix"] --> COR["Pairwise correlation"]
  COR --> SOFT["Soft threshold (^beta)"]
  SOFT --> TOM["Topological overlap"]
  TOM --> MOD["Modules (clustering)"]
  MOD --> EIG["Module eigengene -> trait"]
```

Raising correlations to a power $\beta>1$ is a nonlinear emphasis: a correlation
of 0.5 becomes 0.5^6 ≈ 0.016, while 0.9 stays ~0.53, sharply separating real
co-expression from noise:

```plot
{"title": "Soft-thresholding sharpens strong correlations", "xLabel": "absolute correlation", "yLabel": "adjacency (cor^6)", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x^6", "label": "adjacency", "color": "#16a34a"}]}
```

**Next:** measuring expression at isoform resolution.
""",
        ),
        _t(
            "Isoform and transcript-level quantification",
            "13 min",
            r"""
# Isoform and transcript-level quantification

Genes produce multiple **isoforms** via alternative splicing, and the same gene
can shift its isoform usage without changing total output. Quantifying isoforms
is hard because reads from **shared exons** are ambiguous. Tools like **salmon**,
**kallisto** and **RSEM** resolve this with a probabilistic model, assigning
reads to transcripts via **expectation–maximization (EM)** to maximize the
likelihood of the observed reads.

Downstream, **differential transcript usage (DTU)** (e.g. **DEXSeq**,
**DRIMSeq**) detects proportion shifts, while **tximport** aggregates transcript
estimates to robust gene-level counts. **rMATS** quantifies specific splicing
events (exon skipping, intron retention) as **percent spliced-in (PSI)**.

```mermaid
flowchart LR
  READS["Reads"] --> EM["EM assignment to isoforms (salmon)"]
  EM --> TXQ["Transcript-level estimates"]
  TXQ --> GENE["tximport -> gene counts"]
  TXQ --> DTU["DTU: DEXSeq / DRIMSeq"]
  TXQ --> PSI["rMATS PSI per event"]
```

The EM algorithm increases the data log-likelihood at every iteration and
converges, with the largest gains in the first few rounds:

```plot
{"title": "EM log-likelihood rises and converges", "xLabel": "EM iteration", "yLabel": "relative log-likelihood", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "log-likelihood", "color": "#2563eb"}]}
```

**Next:** measuring expression one cell at a time.
""",
        ),
        _t(
            "Single-cell RNA-seq",
            "13 min",
            r"""
# Single-cell RNA-seq

**Single-cell RNA-seq (scRNA-seq)** measures expression in individual cells,
revealing heterogeneity hidden by bulk averaging. Droplet platforms (**10x
Genomics**) tag each cell with a **cell barcode** and each molecule with a
**unique molecular identifier (UMI)**, so PCR duplicates collapse to true
molecule counts.

The data are **sparse** (most genes are zero in any cell — dropout) and
high-dimensional. A standard pipeline (Seurat, Scanpy): filter cells by QC
metrics, **normalize** (log or SCTransform), select **highly variable genes**,
reduce dimensions with **PCA → UMAP/t-SNE**, **cluster** (Leiden/Louvain), and
annotate cell types by **marker genes**.

```mermaid
flowchart LR
  DROP["Droplets: barcode + UMI"] --> QC["QC filter cells"]
  QC --> NORM["Normalize + HVG"]
  NORM --> PCA["PCA"]
  PCA --> UMAP["UMAP / clustering (Leiden)"]
  UMAP --> ANN["Annotate cell types"]
```

A core trade-off is **depth vs cell number** at fixed budget: more cells improve
population coverage but each is shallowly sampled, so genes detected per cell
saturates with reads:

```plot
{"title": "Genes detected per cell saturate with reads", "xLabel": "reads per cell (relative)", "yLabel": "genes detected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "genes detected", "color": "#16a34a"}]}
```

**Next:** long-read, spatial and deep-learning frontiers.
""",
        ),
        _t(
            "Long-read, spatial and deep learning",
            "12 min",
            r"""
# Long-read, spatial and deep learning

Short reads fragment transcripts, leaving isoform structure ambiguous.
**Long-read RNA-seq** (**Oxford Nanopore**, **PacBio Iso-Seq**) sequences
full-length cDNA or **native RNA**, reading whole isoforms — including novel
splicing and poly(A) length — though with higher per-base error.

**Spatial transcriptomics** (**Visium**, **MERFISH**, **Slide-seq**) keeps the
**tissue coordinates** of each measurement, mapping expression onto histology.

**Deep learning** now pervades the field: **scVI** (variational autoencoders)
models scRNA-seq counts and corrects batch in a latent space; **Enformer** and
**Borzoi** predict expression from DNA sequence with transformers; **scGPT** and
**Geneformer** are foundation models pretrained on millions of cells for transfer
to annotation and perturbation tasks.

```mermaid
flowchart LR
  RNA["RNA sample"] --> LONG["Long-read: full isoforms"]
  RNA --> SPAT["Spatial: expression + coordinates"]
  RNA --> SC["Single-cell counts"]
  SC --> DL["Deep models: scVI, scGPT"]
  LONG --> DL
  SPAT --> DL
  DL --> PRED["Denoise, integrate, predict"]
```

Foundation-model performance on downstream tasks improves with pretraining scale
but shows diminishing returns — a familiar saturating curve:

```plot
{"title": "Foundation-model accuracy vs pretraining scale", "xLabel": "pretraining cells (log relative)", "yLabel": "downstream accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "8*x/(2+x)/10", "label": "accuracy", "color": "#2563eb"}]}
```

**Next:** integrating multi-omics with the transcriptome.
""",
        ),
        _t(
            "Multi-omics integration and applications",
            "12 min",
            r"""
# Multi-omics integration and applications

The transcriptome is one layer; biology emerges from integrating it with others.
**Multi-omics** combines RNA-seq with **chromatin accessibility** (ATAC-seq),
**DNA methylation**, **proteomics** and **genotype** to build mechanistic
pictures — for example linking a regulatory variant to a chromatin change to a
transcript to a protein.

Key integrative analyses include **eQTL mapping** (variants associated with
expression; GTEx), **multi-modal single cell** (10x Multiome: RNA + ATAC in the
same cell, integrated by tools like **MOFA+**, **Seurat WNN** and **scVI**), and
**deconvolution** of bulk samples into cell-type proportions (**CIBERSORTx**).
Clinically, RNA-seq drives **tumor subtyping**, **biomarker discovery** and
**fusion-gene** detection.

```mermaid
flowchart LR
  RNA["RNA-seq"] --> INT["Integration (MOFA+, WNN)"]
  ATAC["ATAC-seq"] --> INT
  METH["Methylation"] --> INT
  GENO["Genotype (eQTL)"] --> INT
  INT --> APP["Subtyping, biomarkers, mechanism"]
```

As more omics layers are integrated, the explained biological variance rises but
with diminishing returns, so layer choice should be hypothesis-driven:

```plot
{"title": "Explained variance vs number of omics layers", "xLabel": "omics layers integrated", "yLabel": "explained variance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "explained variance", "color": "#16a34a"}]}
```

**Next:** check your mastery of advanced transcriptomics.
""",
        ),
        _quiz(),
    ),
)


TRANSCRIPTOMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["TRANSCRIPTOMICS_COURSES"]
