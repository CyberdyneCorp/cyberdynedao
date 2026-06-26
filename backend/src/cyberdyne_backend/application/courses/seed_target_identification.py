"""Computational Target Identification track: Basics -> Intermediate -> Advanced.

A university-level curriculum on finding and validating drug targets in silico:
from disease biology and what makes a protein a target, through omics, network
and human-genetics evidence, to druggability assessment, causal validation and
quantitative target-disease association scoring. Lessons use interactive ```plot
blocks for quantitative relationships (dose response, expression effect sizes,
enrichment, genetic odds ratios, evidence aggregation) and ```mermaid diagrams
for pathways, evidence pipelines, classifications and decision flows.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Computational Target Identification -- Basics ----------------------------

_BASICS = SeedCourse(
    slug="target-identification-basics",
    title="Computational Target Identification — Basics",
    description=(
        "What a drug target is and why we look for one. The intuition behind "
        "target identification: disease as perturbed biology, the central dogma "
        "as a chain of interventable steps, the major target classes, and the "
        "first lines of computational evidence — differential expression, "
        "pathways and the basics of binding. Built on real molecular detail with "
        "interactive plots and pathway diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a drug target?",
            "10 min",
            r"""
# What is a drug target?

A **drug target** is a biomolecule — usually a protein — whose activity a drug
modulates to change the course of a disease. Most marketed small molecules and
biologics act on a few thousand human proteins: enzymes, receptors, ion
channels, transporters and a smaller set of protein–protein interfaces. The
guiding idea is **causality**: a good target sits *upstream* in the chain of
events that produces the disease phenotype, so perturbing it shifts the
phenotype in a therapeutic direction.

**Target identification** is the computational and experimental process of
proposing such a biomolecule and assembling evidence that it is both
*disease-relevant* (modulating it should help patients) and *tractable* (we can
actually make a molecule that engages it). These two axes — biology and
druggability — run through the whole field.

```mermaid
flowchart LR
  DIS["Disease biology"] --> HYP["Target hypothesis"]
  HYP --> EVID["Evidence: omics, genetics, networks"]
  EVID --> DRUG["Druggability & tractability"]
  DRUG --> VAL["Validation"]
  VAL --> LEAD["Hit / lead discovery"]
```

A drug rarely fully abolishes its target. Engagement is graded and saturable:
as drug concentration rises, target occupancy follows a binding curve, and only
*sufficient* occupancy yields a clinical effect. That saturating relationship is
the quantitative backbone of everything downstream.

```plot
{"title": "Target occupancy vs drug concentration", "xLabel": "drug concentration (relative)", "yLabel": "fraction of target bound", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy", "color": "#2563eb"}]}
```

**Next:** how disease biology turns into a target hypothesis.
""",
        ),
        _t(
            "Disease biology as perturbed networks",
            "11 min",
            r"""
# Disease biology as perturbed networks

Disease is rarely one broken gene acting alone. It is a **perturbation of a
biological system**: a mutation, an environmental insult or an ageing process
shifts the activity of many genes and proteins, and the phenotype emerges from
the altered network. To find a target we ask which node, if nudged, would push
the system back toward health.

The **central dogma** — DNA → RNA → protein — is also a chain of *interventable
steps*. We can silence a transcript (antisense, siRNA), block a protein's active
site (small molecule), or neutralise a secreted protein (antibody). The level we
choose constrains the modality.

```mermaid
flowchart LR
  DNA["Gene (DNA)"] -->|transcription| RNA["mRNA"]
  RNA -->|translation| PROT["Protein"]
  PROT --> FUNC["Function / phenotype"]
  ASO["Antisense / siRNA"] -. blocks .-> RNA
  SM["Small molecule"] -. inhibits .-> PROT
  AB["Antibody"] -. neutralises .-> PROT
```

A central concept is the **dose–response** relationship: as we increase the
strength of an intervention, the phenotype changes, often as a sigmoid. The
midpoint (the EC50 or IC50) tells us the potency required, and the steepness
tells us how switch-like the response is — both matter when judging whether a
target is worth pursuing.

```plot
{"title": "Sigmoidal dose-response of a phenotype to intervention", "xLabel": "intervention strength (log scale)", "yLabel": "phenotypic effect", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#2563eb"}]}
```

**Next:** the major classes of druggable targets.
""",
        ),
        _t(
            "Target classes and modalities",
            "11 min",
            r"""
# Target classes and modalities

Targets cluster into recurring **protein classes**, each with characteristic
biology and a preferred drug **modality**. Knowing the class immediately
suggests how — and whether — it can be drugged.

- **Enzymes** (kinases, proteases, oxidoreductases): catalytic sites are deep,
  well-defined pockets ideal for competitive small-molecule inhibitors.
- **G-protein-coupled receptors (GPCRs)**: seven-transmembrane receptors; the
  single largest class of small-molecule drug targets, modulated by agonists,
  antagonists and allosteric modulators.
- **Ion channels** and **transporters**: control flux of ions/solutes; targeted
  by blockers and modulators.
- **Nuclear receptors**: ligand-activated transcription factors.
- **Secreted and surface proteins** (cytokines, growth factors, their
  receptors): natural substrates for **antibodies**.

```mermaid
flowchart TB
  T["Drug target"] --> ENZ["Enzymes"]
  T --> GPCR["GPCRs"]
  T --> CHAN["Ion channels / transporters"]
  T --> NR["Nuclear receptors"]
  T --> SEC["Secreted / surface proteins"]
  ENZ --> SM["Small-molecule inhibitor"]
  GPCR --> SM
  CHAN --> SM
  NR --> SM
  SEC --> AB["Antibody / biologic"]
```

Enzyme kinetics make the inhibitor logic concrete. A Michaelis–Menten enzyme
converts substrate at a rate that saturates with substrate concentration;
a competitive inhibitor effectively raises the apparent $K_m$, so more substrate
is needed to reach the same velocity.

```plot
{"title": "Michaelis-Menten enzyme velocity", "xLabel": "substrate [S]", "yLabel": "reaction velocity v", "xRange": [0, 20], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

**Next:** reading differential gene expression for target clues.
""",
        ),
        _t(
            "Differential expression as a first signal",
            "11 min",
            r"""
# Differential expression as a first signal

One of the earliest computational signals for a target is **differential
expression (DE)**: a gene whose transcript level changes between disease and
healthy tissue is a candidate worth examining. We compare expression across
groups and ask which genes move *and* by how much, reliably.

The standard summary is the **log2 fold-change** ($\log_2 FC$) — the ratio of
mean expression in disease versus control on a log scale — paired with a
statistical test. A volcano plot places $\log_2 FC$ on the x-axis and statistical
significance ($-\log_{10} p$) on the y-axis; genes in the upper corners are large,
confident changes.

```mermaid
flowchart LR
  RAW["Counts / intensities"] --> NORM["Normalise"]
  NORM --> TEST["Per-gene test (disease vs control)"]
  TEST --> FC["log2 fold-change"]
  TEST --> P["p-value -> FDR"]
  FC --> VOLC["Volcano plot & ranking"]
  P --> VOLC
```

A fold-change alone is not enough: with thousands of genes tested, some look
extreme by chance, so we control the **false discovery rate (FDR)** (e.g.
Benjamini–Hochberg). Importantly, DE is *correlative* — a gene may change because
it *drives* disease or merely *responds* to it. DE points the flashlight; later
lessons add the evidence that tells driver from passenger.

The relationship between fold-change and the underlying ratio is exponential:
a $\log_2 FC$ of 1 means a 2-fold change, 2 means 4-fold, 3 means 8-fold.

```plot
{"title": "Fold-change grows exponentially with log2 fold-change", "xLabel": "log2 fold-change", "yLabel": "linear fold-change", "xRange": [0, 5], "yRange": [0, 32], "grid": true, "functions": [{"expr": "2^x", "label": "fold-change = 2^(log2FC)", "color": "#dc2626"}]}
```

**Next:** putting genes into pathways.
""",
        ),
        _t(
            "Pathways and biological context",
            "10 min",
            r"""
# Pathways and biological context

A single differentially expressed gene is hard to interpret; a *coordinated*
change across a **pathway** is far more convincing. Pathways are curated sets of
genes/proteins that act together — signalling cascades, metabolic routes, immune
programmes. Resources like **KEGG**, **Reactome** and the **Gene Ontology (GO)**
encode this knowledge.

**Enrichment analysis** asks: among my list of candidate genes, is any pathway
over-represented relative to chance? The classic test is a hypergeometric /
Fisher's exact test comparing the overlap between my gene list and a pathway to
what random sampling would give.

```mermaid
flowchart LR
  GENES["Candidate gene list"] --> MAP["Map to pathway sets (KEGG/Reactome/GO)"]
  MAP --> TEST["Over-representation test"]
  TEST --> RANK["Enriched pathways ranked by p / FDR"]
  RANK --> CTX["Biological hypothesis"]
```

Enrichment turns a flat gene list into mechanism: if oxidative-phosphorylation
genes are enriched, mitochondrial metabolism is implicated, and proteins in that
pathway become target candidates. Statistical significance climbs sharply as the
observed overlap exceeds the expected overlap — a saturating gain in confidence.

```plot
{"title": "Enrichment confidence vs observed/expected overlap", "xLabel": "observed / expected overlap ratio", "yLabel": "relative confidence (-log10 p, scaled)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(2/x)^2)", "label": "confidence", "color": "#16a34a"}]}
```

**Next:** the basics of how drugs bind targets.
""",
        ),
        _t(
            "Binding, affinity and the dose-response idea",
            "10 min",
            r"""
# Binding, affinity and the dose-response idea

For a target to be useful, a molecule must **bind** it selectively and tightly
enough. Binding is an equilibrium: drug (L) plus target (R) form a complex (LR).
The **dissociation constant** $K_d$ is the drug concentration at which half the
target is occupied; smaller $K_d$ means tighter binding (higher affinity).

At equilibrium the fraction of target bound follows a saturating curve in drug
concentration:

$$\theta = \frac{[L]}{[L] + K_d}$$

This is the same hyperbola as enzyme saturation and receptor occupancy — a
recurring shape across the field.

```mermaid
flowchart LR
  L["Drug (ligand)"] --> C["Complex L·R"]
  R["Target (receptor)"] --> C
  C -->|Kd| L
  C -->|Kd| R
  C --> EFF["Functional / phenotypic effect"]
```

For *functional* readouts (a cellular response rather than raw binding), the
dose–response is usually sigmoidal on a log-concentration axis, summarised by the
**EC50** (half-maximal effective concentration). The steepness is captured by a
**Hill coefficient**: values above 1 indicate cooperative, switch-like behaviour.

```plot
{"title": "Hill dose-response (cooperative binding, n=2)", "xLabel": "drug concentration (relative)", "yLabel": "fractional response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill response (EC50=3)", "color": "#2563eb"}]}
```

Affinity, selectivity and the shape of the dose–response together decide whether
a target is *pharmacologically* approachable — the bridge to druggability.

**Next:** test your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Computational Target Identification -- Intermediate ----------------------

_INTERMEDIATE = SeedCourse(
    slug="target-identification-intermediate",
    title="Computational Target Identification — Intermediate",
    description=(
        "The quantitative core of computational target identification: rigorous "
        "differential-expression statistics, network-based prioritisation, human "
        "genetics evidence (GWAS, eQTL, colocalisation, Mendelian randomization), "
        "druggability and pocket assessment, and how disparate evidence is "
        "combined into a target-disease association score. Built with worked "
        "equations, interactive plots and analysis-pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Differential expression done rigorously",
            "12 min",
            r"""
# Differential expression done rigorously

Robust DE is a statistics problem. Microarray-era tools like **limma** model
log-intensities with linear models and **empirical Bayes** shrinkage of variance;
RNA-seq tools like **DESeq2** and **edgeR** model raw counts with a **negative
binomial** distribution, estimating a gene-specific *dispersion* that captures
biological variability beyond Poisson noise.

The core statistic is a **moderated** version of the fold-change-over-error
ratio. Empirical Bayes borrows information across thousands of genes to stabilise
each gene's variance estimate, which dramatically improves power when sample
sizes are small.

```mermaid
flowchart LR
  COUNTS["Count matrix"] --> NORM["Size-factor / TMM normalisation"]
  NORM --> DISP["Estimate dispersion (shrinkage)"]
  DISP --> FIT["Fit NB / linear model per gene"]
  FIT --> TEST["Wald / LRT test"]
  TEST --> FDR["BH FDR control"]
  FDR --> RANK["Ranked DE genes"]
```

Because we test ~20,000 genes, multiple testing is unavoidable. The
**Benjamini–Hochberg** procedure controls the expected proportion of false
positives among the calls (the FDR). The number of true discoveries that survive
a fixed FDR rises with effect size: genes with larger $|\log_2 FC|$ and lower
variance clear the threshold first.

```plot
{"title": "Statistical power rises with effect size", "xLabel": "true log2 fold-change", "yLabel": "probability of detection (power)", "xRange": [0, 5], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(2*x-3)))", "label": "power", "color": "#2563eb"}]}
```

**Next:** prioritising candidates with network topology.
""",
        ),
        _t(
            "Network-based target prioritisation",
            "12 min",
            r"""
# Network-based target prioritisation

Targets do not act alone, so their position in interaction networks is
informative. Given a protein–protein interaction graph (STRING, BioGRID), we
prioritise candidates by **topology** and by **proximity to known disease
genes**. Two ideas dominate.

**Centrality**: degree (number of partners), betweenness (how often a node lies
on shortest paths), and eigenvector/PageRank centrality (importance weighted by
neighbours' importance). High-centrality **hubs** are often essential.

**Guilt by association / network propagation**: starting from known disease
"seed" genes, a **random walk with restart (RWR)** diffuses signal across edges;
nodes that accumulate high stationary probability are guilty by proximity. This
is the engine behind tools like **NetWAS** and many "module"-based methods.

```mermaid
flowchart LR
  SEEDS["Known disease genes (seeds)"] --> RWR["Random walk with restart"]
  PPI["PPI network"] --> RWR
  RWR --> SCORE["Diffusion / proximity scores"]
  SCORE --> MOD["Disease module detection"]
  MOD --> CAND["Ranked candidate targets"]
```

Random walk with restart obeys $p_{t+1} = (1-r)\,W p_t + r\,p_0$, where $W$ is the
column-normalised adjacency, $r$ the restart probability and $p_0$ the seed
vector; iterating to convergence gives the proximity score. Many real PPI
networks are **scale-free**: their degree distribution follows a power law,
$P(k) \sim k^{-\gamma}$, so a few hubs have very many connections.

```plot
{"title": "Scale-free degree distribution (power law)", "xLabel": "node degree k", "yLabel": "fraction of nodes P(k)", "xRange": [1, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/x^2", "label": "P(k) ~ k^-2", "color": "#dc2626"}]}
```

**Next:** human genetics as causal evidence.
""",
        ),
        _t(
            "Genetic evidence: GWAS and eQTL",
            "12 min",
            r"""
# Genetic evidence: GWAS and eQTL

Human genetics is the strongest non-experimental evidence that a target is
*causal*: drug programmes with genetic support succeed in the clinic roughly
twice as often. A **genome-wide association study (GWAS)** tests millions of SNPs
for association with a trait; significant loci ($p < 5\times10^{-8}$) flag genomic
regions, which are then resolved to genes.

The challenge is that GWAS hits are mostly **non-coding** and live in linkage
disequilibrium blocks. **Expression quantitative trait loci (eQTL)** — variants
that change a gene's expression (e.g. from GTEx) — help map a non-coding signal
to the gene it actually regulates.

```mermaid
flowchart LR
  GWAS["GWAS locus (trait SNPs)"] --> COLOC["Colocalisation"]
  EQTL["eQTL (expression SNPs)"] --> COLOC
  COLOC --> GENE["Implicated gene"]
  GENE --> TARGET["Target hypothesis"]
```

Effect sizes are reported as **odds ratios (OR)** for binary traits or **beta**
for quantitative ones. A Manhattan plot displays $-\log_{10} p$ along the genome;
peaks are associated loci. The genetic signal is the chance the region is truly
involved — the multiple-testing burden is severe, hence the genome-wide
threshold.

```plot
{"title": "Disease risk grows with risk-allele dose (log-additive)", "xLabel": "number of risk alleles", "yLabel": "relative risk", "xRange": [0, 2], "yRange": [0, 4], "grid": true, "functions": [{"expr": "exp(0.6*x)", "label": "risk = exp(beta * dose)", "color": "#dc2626"}]}
```

**Next:** turning association into causation.
""",
        ),
        _t(
            "Colocalisation and Mendelian randomization",
            "12 min",
            r"""
# Colocalisation and Mendelian randomization

A GWAS locus overlapping an eQTL does not prove they share a causal variant —
they could be two distinct signals in linkage disequilibrium. **Colocalisation**
(e.g. **coloc**) computes the posterior probability that the trait and the gene's
expression are driven by the *same* variant, giving a principled hand-off from
locus to gene.

To estimate the *causal effect* of a target's activity on disease, we use
**Mendelian randomization (MR)**. Genetic variants act as **instrumental
variables**: because alleles are randomised at conception, they mimic a lifelong
randomized trial. If a variant raises a biomarker (or a target's expression) and
correspondingly changes disease risk, that supports a causal link.

```mermaid
flowchart LR
  IV["Genetic instrument (SNP)"] --> EXP["Exposure: target activity"]
  EXP --> OUT["Outcome: disease risk"]
  IV -. must NOT bypass exposure .-> OUT
  CONF["Confounders"] -. blocked by randomisation .-> EXP
```

The simplest MR estimate is a ratio (Wald) of the SNP–outcome to the SNP–exposure
effect; with many instruments, **inverse-variance weighting (IVW)** combines them,
and **MR-Egger** tests for pleiotropy (an instrument affecting the outcome through
a path other than the exposure — the key threat to validity). The MR causal
estimate scales linearly: the slope of outcome effect against exposure effect
across instruments *is* the causal estimate.

```plot
{"title": "MR: SNP-outcome vs SNP-exposure effects (slope = causal estimate)", "xLabel": "SNP effect on exposure (target activity)", "yLabel": "SNP effect on outcome (disease)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.8*x", "label": "IVW causal slope", "color": "#2563eb"}]}
```

**Next:** is the target druggable?
""",
        ),
        _t(
            "Druggability and pocket assessment",
            "11 min",
            r"""
# Druggability and pocket assessment

Disease-relevance is necessary but not sufficient: we must be able to *engage*
the target. **Druggability** asks whether a molecule of the intended modality can
bind with useful affinity and selectivity. For small molecules this hinges on the
existence of a suitable **binding pocket**.

Structure-based methods (using PDB structures or AlphaFold models) detect and
score cavities: **fpocket**, **SiteMap** and **DoGSiteScorer** measure pocket
volume, depth, enclosure and hydrophobicity, yielding a druggability score. A
pocket that is too shallow, too polar, or too flat (typical of protein–protein
interfaces) is "undruggable" by conventional small molecules.

```mermaid
flowchart LR
  STRUCT["3D structure (PDB / AlphaFold)"] --> POCK["Pocket detection (fpocket)"]
  POCK --> DESC["Descriptors: volume, hydrophobicity, enclosure"]
  DESC --> SCORE["Druggability score"]
  SCORE --> CALL{"Druggable?"}
  CALL -->|yes| SM["Small-molecule campaign"]
  CALL -->|no| ALT["Biologic / PROTAC / undruggable"]
```

Sequence- and ligand-based evidence complements structure: membership in a
historically tractable class (kinase, GPCR), existing chemical matter in
**ChEMBL**, and **ligandability** from fragment screens. Ligand efficiency —
binding energy per heavy atom — guides whether a pocket yields efficient
chemistry. Binding free energy relates to affinity logarithmically,
$\Delta G = -RT \ln(1/K_d)$, so each order-of-magnitude gain in potency adds a
roughly constant increment of free energy.

```plot
{"title": "Binding free energy vs affinity (log relationship)", "xLabel": "affinity 1/Kd (relative)", "yLabel": "binding free energy magnitude |dG|", "xRange": [1, 10], "yRange": [0, 3], "grid": true, "functions": [{"expr": "log(x)", "label": "|dG| ~ ln(1/Kd)", "color": "#16a34a"}]}
```

**Next:** combining all the evidence into a score.
""",
        ),
        _t(
            "Aggregating evidence into a target score",
            "11 min",
            r"""
# Aggregating evidence into a target score

No single line of evidence is decisive, so platforms like **Open Targets**
combine many **data types** — genetic association, somatic mutations, known drugs,
differential expression, pathways, animal models, literature text-mining — into a
**target–disease association score**.

The recipe: within each data type, evidence is harmonised to a 0–1 score; data
types are aggregated by a **harmonic-sum** that rewards multiple independent
strands; and a weighted combination across data types yields an overall score in
$[0, 1]$. The harmonic sum, $\sum_i s_i / i$ over ranked scores $s_i$, is dominated
by the strongest evidence while still rewarding corroboration.

```mermaid
flowchart TB
  GEN["Genetic association"] --> AGG["Per-datatype harmonisation"]
  SOM["Somatic mutations"] --> AGG
  DRUG["Known drugs"] --> AGG
  RNA["Expression"] --> AGG
  PATH["Pathways"] --> AGG
  LIT["Literature"] --> AGG
  AGG --> WSUM["Weighted harmonic aggregation"]
  WSUM --> SCORE["Target-disease score in [0,1]"]
```

Aggregation has **diminishing returns**: the first few strong, independent lines
of evidence move the score a lot; additional weak strands add little. This
concave shape — confidence rising fast then saturating — is exactly what we want,
penalising single-source claims and rewarding convergent, orthogonal support.

```plot
{"title": "Diminishing returns of accumulating evidence", "xLabel": "number of independent evidence strands", "yLabel": "aggregated confidence score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "aggregated score", "color": "#16a34a"}]}
```

**Next:** test the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# -- Computational Target Identification -- Advanced --------------------------

_ADVANCED = SeedCourse(
    slug="target-identification-advanced",
    title="Computational Target Identification — Advanced",
    description=(
        "State-of-the-art and applied target identification: causal "
        "perturbation maps and CRISPR dependency screens, single-cell and "
        "spatial resolution, machine-learning and graph/representation-learning "
        "target prediction, structure-based druggability with deep learning, "
        "expanded modalities (PROTACs, molecular glues) and rigorous validation "
        "with safety and reverse-translation. Built with quantitative plots and "
        "pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "CRISPR dependency screens",
            "12 min",
            r"""
# CRISPR dependency screens

Genome-wide **CRISPR–Cas9 knockout screens** provide functional, near-causal
evidence: knock out each gene in a pool of cells, then see which knockouts kill
or impair growth. Projects like **DepMap** (Project Achilles) screen hundreds of
cancer cell lines, revealing **genetic dependencies** — genes a given cell line
*needs* to survive — which are prime targets.

Each gene gets a **dependency score** (e.g. CERES/Chronos), corrected for
copy-number and guide efficacy. A strongly negative score means dropout (the gene
is essential); **selective dependencies** — essential in disease cells but not in
normal cells — define a therapeutic window. **Synthetic lethality** (a gene
essential only in a specific mutant background, e.g. *PARP* in *BRCA*-mutant
tumours) is found by contrasting dependency across genotypes.

```mermaid
flowchart LR
  LIB["Genome-wide sgRNA library"] --> POOL["Pooled cell screen"]
  POOL --> SEQ["Sequence guide abundance (t0 vs tN)"]
  SEQ --> LFC["Guide log fold-change (dropout)"]
  LFC --> DEP["Gene dependency score"]
  DEP --> SEL["Selective / synthetic-lethal targets"]
```

Essentiality is read from guide **dropout**: essential-gene guides deplete
exponentially over the screen as those cells fail to proliferate, while neutral
guides hold steady. The separation between the two grows with screen duration.

```plot
{"title": "Guide dropout for an essential gene over time", "xLabel": "screen time (doublings)", "yLabel": "relative guide abundance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "essential-gene guide", "color": "#dc2626"}]}
```

**Next:** resolving targets at single-cell and spatial scale.
""",
        ),
        _t(
            "Single-cell and spatial target discovery",
            "12 min",
            r"""
# Single-cell and spatial target discovery

Bulk assays average over heterogeneous tissue, hiding the cell type that drives
disease. **Single-cell RNA-seq (scRNA-seq)** profiles thousands of individual
cells, letting us pinpoint *which cell type or state* expresses a candidate
target — critical for efficacy and for predicting on-target toxicity in healthy
tissues. **Spatial transcriptomics** adds the missing coordinates, showing where
in the tissue (e.g. tumour core vs margin) the target is expressed.

The pipeline clusters cells into types, finds **cell-type marker genes**, and
tests for disease-vs-control changes *within* a cell type. A good target is
ideally **cell-type-restricted** in disease and largely absent from vital normal
cell types.

```mermaid
flowchart LR
  CELLS["scRNA-seq cells"] --> QC["QC & normalise"]
  QC --> DR["Dimensionality reduction (PCA/UMAP)"]
  DR --> CLUST["Clustering -> cell types"]
  CLUST --> MARK["Marker / DE per cell type"]
  MARK --> CTX["Cell-type-resolved targets"]
  SPAT["Spatial transcriptomics"] --> CTX
```

Cell-type **specificity** is quantified with entropy-like indices (e.g. the tau
score): a target expressed in one cell type scores near 1, one expressed
everywhere scores near 0. Specificity climbs sharply as expression concentrates
in fewer cell types — a saturating gain that maps directly onto therapeutic
selectivity.

```plot
{"title": "Target specificity vs expression concentration", "xLabel": "concentration of expression in target cell type", "yLabel": "specificity index (tau-like)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "specificity", "color": "#16a34a"}]}
```

**Next:** machine-learning target prediction.
""",
        ),
        _t(
            "Machine-learning target prediction",
            "13 min",
            r"""
# Machine-learning target prediction

When evidence is sparse, **machine learning** ranks genes by their resemblance to
known successful targets. Features span sequence, expression, network topology,
genetic association, tissue specificity and tractability; models range from
gradient-boosted trees to graph methods. The setup is typically **positive-
unlabelled**: known drug targets are positives, but unlabelled genes are a mix of
true negatives and undiscovered targets.

**Graph representation learning** — node2vec embeddings, and especially **graph
neural networks (GNNs)** — learns a vector per gene from the topology of PPI,
regulatory and knowledge graphs, then predicts disease links. **Knowledge-graph
embedding** (e.g. over the Open Targets / Hetionet graph) frames target discovery
as **link prediction** between gene and disease nodes.

```mermaid
flowchart LR
  KG["Biological knowledge graph"] --> EMB["GNN / KG embedding"]
  FEAT["Omics + genetics + tractability features"] --> MODEL["Classifier / ranker"]
  EMB --> MODEL
  MODEL --> PRED["Ranked candidate targets"]
  PRED --> EVAL["Cross-validation / temporal holdout"]
```

Because positives are rare, accuracy is misleading; we evaluate with **precision–
recall** and **AUPRC**, and guard against leakage with **temporal validation**
(train on targets known before year Y, test on those discovered after). Precision
typically falls as we recall more candidates — the precision–recall trade-off
that governs how deep into the ranked list a programme can afford to go.

```plot
{"title": "Precision-recall trade-off in target ranking", "xLabel": "recall", "yLabel": "precision", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-x^2", "label": "PR curve", "color": "#2563eb"}]}
```

**Next:** structure-based druggability with deep learning.
""",
        ),
        _t(
            "Structure-based and AI druggability",
            "12 min",
            r"""
# Structure-based and AI druggability

**AlphaFold2/3** and successors made high-quality predicted structures available
for nearly the whole proteome, vastly expanding structure-based target
assessment beyond the experimentally solved fraction. With a model in hand we can
detect cryptic pockets, run **molecular docking** and estimate ligandability for
targets that previously had no structure.

Deep learning now also drives druggability and discovery directly: **DiffDock**
and related diffusion models predict ligand poses; co-folding methods predict the
protein–ligand complex; and structure-conditioned **generative models** design
novel binders. These let us ask not just "is there a pocket?" but "can a molecule
plausibly fill it?".

```mermaid
flowchart LR
  SEQ["Protein sequence"] --> AF["AlphaFold structure"]
  AF --> POCK["Pocket / cryptic-site detection"]
  POCK --> DOCK["Docking / co-folding (DiffDock)"]
  DOCK --> SCORE["Ligandability & pose confidence"]
  SCORE --> GEN["Generative binder design"]
```

A caveat: predicted models carry **confidence** (pLDDT, PAE). Low-confidence and
intrinsically disordered regions mislead pocket detection, so model reliability
gates downstream use. Usable structure-derived signal rises steeply with model
confidence and then plateaus — high-pLDDT cores are trustworthy, the long tail of
low-confidence residues is not.

```plot
{"title": "Usable structural signal vs model confidence (pLDDT)", "xLabel": "predicted confidence pLDDT (scaled)", "yLabel": "reliable structural signal", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "reliability", "color": "#2563eb"}]}
```

**Next:** targeting the undruggable with new modalities.
""",
        ),
        _t(
            "Expanding the druggable space: new modalities",
            "12 min",
            r"""
# Expanding the druggable space: new modalities

Roughly 80% of the proteome is "undruggable" by classical occupancy-based small
molecules — transcription factors, scaffolding proteins and most protein–protein
interfaces lack deep pockets. New modalities reframe what counts as a target.

**Targeted protein degradation** — **PROTACs** and **molecular glues** — recruits
an E3 ubiquitin ligase to mark a target for destruction. Crucially it needs only
a *binding* handle, not an active-site inhibitor, and is **catalytic** (event-
driven): one degrader molecule can destroy many copies of the target, so deep
target knockdown is possible at low occupancy. Other expansions include
**RNA-targeting** small molecules, **antisense/siRNA**, **covalent** chemistry
(e.g. KRAS-G12C), and **allosteric** sites.

```mermaid
flowchart LR
  TGT["Target protein"] --> PRO["PROTAC binds target + E3"]
  E3["E3 ubiquitin ligase"] --> PRO
  PRO --> UBQ["Polyubiquitination"]
  UBQ --> DEG["Proteasomal degradation"]
  DEG --> RECYC["Degrader released -> next target (catalytic)"]
```

The degradation modality follows **event-driven** rather than occupancy-driven
pharmacology. Because the degrader is recycled, sustained low concentrations
drive deep, durable target loss; effective knockdown saturates well below the
levels a stoichiometric inhibitor would require.

```plot
{"title": "Catalytic degradation: deep knockdown at low concentration", "xLabel": "degrader concentration (relative)", "yLabel": "fraction of target degraded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+0.5)", "label": "degradation", "color": "#16a34a"}]}
```

**Next:** validating and de-risking the chosen target.
""",
        ),
        _t(
            "Target validation, safety and reverse translation",
            "12 min",
            r"""
# Target validation, safety and reverse translation

A prioritised target must be **validated** before heavy investment.
**Genetic validation** perturbs the target (CRISPR knockout, knock-in,
degron, siRNA) and checks the disease phenotype reverses; **pharmacological
validation** uses tool compounds and tests that the effect tracks **target
engagement** (CETSA, occupancy assays), guarding against off-target artefacts.
**Orthogonal** evidence across systems — cell lines, organoids, animal models,
human genetics — converging on the same conclusion is the gold standard.

Equally important is **safety**: human **loss-of-function** variants (gnomAD)
that abolish the gene without harm are reassuring; essential or constrained genes
warn of toxicity. **On-target toxicity** is predicted from the target's
expression in vital tissues, and **selectivity** from off-target binding profiles.

```mermaid
flowchart LR
  CAND["Prioritised target"] --> GEN["Genetic perturbation"]
  CAND --> PHARM["Tool compound + engagement"]
  GEN --> ORTH["Orthogonal model convergence"]
  PHARM --> ORTH
  ORTH --> SAFE["Safety: LoF tolerance, expression, selectivity"]
  SAFE --> GO{"Progress?"}
  GO -->|yes| LEAD["Hit-to-lead"]
  GO -->|no| BACK["Reverse-translate / deprioritise"]
```

**Reverse translation** closes the loop: clinical failures and human data feed
back to refine which evidence actually predicts success. The probability of
clinical success rises with the number of *independent, orthogonal* validation
lines — diminishing returns again, but each early strand removes substantial
risk.

```plot
{"title": "Probability of success vs orthogonal validation lines", "xLabel": "number of orthogonal validation lines", "yLabel": "probability of clinical success", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "P(success)", "color": "#16a34a"}]}
```

**Next:** test the state-of-the-art material.
""",
        ),
        _quiz(),
    ),
)


TARGET_IDENTIFICATION_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["TARGET_IDENTIFICATION_COURSES"]
