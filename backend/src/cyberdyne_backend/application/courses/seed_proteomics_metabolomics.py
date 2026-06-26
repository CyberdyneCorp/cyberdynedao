"""Proteomics & Metabolomics track: Basics -> Intermediate -> Advanced.

A three-level track on the mass-spectrometry-driven study of proteins and small
molecules. Basics builds intuition for MS, peptides and sample workflows;
Intermediate develops identification (database search, FDR) and quantification
(label-free, TMT/SILAC); Advanced reaches PTMs, untargeted metabolomics and
multi-omics integration with machine learning. Lessons are `text` with LaTeX,
interactive ```plot blocks (spectra, calibration, kinetics) and ```mermaid
pipeline/process diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Proteomics & Metabolomics — Basics ──────────────────────  (m/z) ──

_BASICS = SeedCourse(
    slug="proteomics-metabolomics-basics",
    title="Proteomics & Metabolomics — Basics",
    description=(
        "The foundations of mass-spectrometry-based omics: what proteomes and "
        "metabolomes are, how a mass spectrometer measures m/z, the bottom-up "
        "peptide workflow with trypsin digestion, soft ionization (ESI and "
        "MALDI), and the LC-MS coupling that separates complex mixtures before "
        "detection. Interactive spectra and process diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Proteomes, metabolomes & the central dogma",
            "10 min",
            r"""
# Proteomes, metabolomes & the central dogma

The genome is essentially static, but the molecules that actually do the work in
a cell change with time, tissue and condition. The **proteome** is the full set
of proteins expressed by a cell or organism; the **metabolome** is the full set
of small-molecule metabolites (sugars, lipids, amino acids, nucleotides). Unlike
the genome, both are dynamic and context-dependent — one gene can yield many
**proteoforms** through alternative splicing and post-translational modification.

```mermaid
flowchart LR
  A["Genome (DNA)"] --> B["Transcriptome (mRNA)"]
  B --> C["Proteome (proteins)"]
  C --> D["Metabolome (metabolites)"]
  D -.->|feedback| C
```

Why measure them directly? mRNA abundance correlates only weakly with protein
abundance (often $r \approx 0.4$), because translation rate, protein half-life
and modification all intervene. The metabolome sits closest to phenotype — it is
the downstream readout of enzyme activity. **Mass spectrometry (MS)** is the
workhorse for both fields because it can identify and quantify thousands of
molecules in a single run, by measuring mass with extraordinary precision.

The proteome is large: a human cell expresses on the order of $10^4$ protein
species spanning seven orders of magnitude in abundance — the core measurement
challenge this track addresses.

**Next:** how a mass spectrometer turns molecules into a spectrum.
""",
        ),
        _t(
            "What a mass spectrometer measures: m/z",
            "11 min",
            r"""
# What a mass spectrometer measures: m/z

A mass spectrometer never weighs a neutral molecule directly. It measures the
**mass-to-charge ratio**, $m/z$, of gas-phase ions. Every instrument has three
stages: an **ion source** (ionizes the sample), a **mass analyzer** (separates
ions by $m/z$), and a **detector** (counts them).

```mermaid
flowchart LR
  S["Ion source"] --> A["Mass analyzer"]
  A --> D["Detector"]
  D --> P["Mass spectrum (intensity vs m/z)"]
```

For an ion carrying $z$ charges and a neutral mass $M$, with proton mass
$m_H \approx 1.0073$:

$$\frac{m}{z} = \frac{M + z\,m_H}{z}$$

So a $10{,}000\,\text{Da}$ protein with $+10$ charges appears at
$m/z \approx 1001$. Multiple charging is why ESI brings large biomolecules into
the modest $m/z$ range of most analyzers. **Resolution**
$R = m/\Delta m$ describes how well two close peaks are separated; modern
Orbitrap and FT instruments reach $R > 100{,}000$, enough to resolve isotopes
and assign charge from peak spacing.

The isotope envelope itself is informative: peaks spaced by $1/z$ in $m/z$ reveal
the charge state directly.

```plot
{"title": "Resolving power vs peak separation", "xLabel": "m/z offset", "yLabel": "signal", "xRange": [-2,2], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-(x*x)/0.02)", "label": "high R", "color": "#2563eb"}, {"expr": "exp(-(x*x)/0.5)", "label": "low R", "color": "#dc2626"}]}
```

**Next:** the bottom-up workflow that breaks proteins into peptides.
""",
        ),
        _t(
            "Bottom-up proteomics & tryptic digestion",
            "11 min",
            r"""
# Bottom-up proteomics & tryptic digestion

Intact proteins are large, heterogeneous and hard to ionize and fragment
cleanly. The dominant strategy, **bottom-up** (shotgun) proteomics, digests
proteins into peptides first, identifies the peptides by MS, then infers the
parent proteins computationally.

```mermaid
flowchart LR
  A["Protein mixture"] --> B["Reduce + alkylate cysteines"]
  B --> C["Trypsin digestion"]
  C --> D["Peptides"]
  D --> E["LC-MS/MS"]
  E --> F["Peptide IDs -> protein inference"]
```

The standard protease is **trypsin**, which cleaves the peptide bond on the
C-terminal side of lysine (K) and arginine (R), except when followed by proline.
This is ideal: it produces peptides of tractable length (≈7–20 residues) that
each end in a basic residue, so they ionize well and fragment predictably.
Before digestion, disulfide bonds are **reduced** (e.g. with DTT) and free
cysteines **alkylated** (with iodoacetamide) to prevent re-bridging.

A protein of length $L$ has on average about $L/(K+R\text{ frequency})$ cleavage
sites; missed cleavages happen, so search software allows 1–2. The trade-off:
top-down proteomics keeps proteins intact and preserves proteoform information,
but bottom-up wins on sensitivity, depth and throughput — which is why it
dominates.

**Next:** getting peptides into the gas phase with soft ionization.
""",
        ),
        _t(
            "Soft ionization: ESI and MALDI",
            "10 min",
            r"""
# Soft ionization: ESI and MALDI

Early ionization methods shattered fragile biomolecules. The 2002 Nobel Prize
recognized two **soft ionization** techniques that transfer large, intact
molecules into gas-phase ions: **electrospray ionization (ESI)** and
**matrix-assisted laser desorption/ionization (MALDI)**.

```mermaid
flowchart TB
  subgraph ESI
    L["Liquid (LC eluent)"] --> N["Charged droplets"]
    N --> M["Solvent evaporation -> multiply-charged ions"]
  end
  subgraph MALDI
    C["Analyte in matrix crystal"] --> P["UV laser pulse"]
    P --> S["Desorbed singly-charged ions"]
  end
```

In **ESI**, the sample flows through a needle held at high voltage; the liquid
forms a Taylor cone and sprays charged droplets that shrink by evaporation until
ions desorb. ESI produces **multiply-charged** ions, pairs naturally with liquid
chromatography, and is the standard for bottom-up proteomics. In **MALDI**, the
analyte is co-crystallized with a UV-absorbing matrix and hit by a laser pulse;
it yields mostly **singly-charged** ions, tolerates salts and is fast — ideal for
MALDI-TOF imaging and microbial identification.

The ESI signal grows with concentration up to a saturation point where the
droplet surface charge is the limit:

```plot
{"title": "ESI response vs analyte concentration", "xLabel": "relative concentration", "yLabel": "ion signal", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating response", "color": "#16a34a"}]}
```

**Next:** coupling separation to MS with LC-MS.
""",
        ),
        _t(
            "Separation first: LC-MS and the chromatogram",
            "11 min",
            r"""
# Separation first: LC-MS and the chromatogram

A tryptic digest of a single sample can contain $10^5$ peptides. Spraying them
all at once overwhelms the mass spectrometer (**ion suppression** and spectral
overlap). The fix is to separate them in time first with **liquid chromatography
(LC)**, so the MS sees a manageable subset at each moment.

```mermaid
flowchart LR
  A["Peptide mixture"] --> B["C18 reversed-phase column"]
  B --> C["Gradient elution (increasing organic)"]
  C --> D["ESI source"]
  D --> E["MS records spectra over time"]
```

The dominant mode is **reversed-phase** LC on a C18 column: peptides bind to the
hydrophobic stationary phase and elute as the mobile phase becomes more organic
(acetonitrile) along a **gradient**. Each peptide leaves the column in a narrow
window, producing a peak in the **chromatogram** (intensity vs retention time).
The data are therefore three-dimensional: retention time, $m/z$, and intensity.

Chromatographic peaks are roughly Gaussian; resolution between two peaks depends
on the difference in retention time relative to peak width:

```plot
{"title": "Two co-eluting chromatographic peaks", "xLabel": "retention time (min)", "yLabel": "intensity", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-(x-4)*(x-4)/0.3)", "label": "peptide A", "color": "#2563eb"}, {"expr": "exp(-(x-5)*(x-5)/0.3)", "label": "peptide B", "color": "#dc2626"}]}
```

Better separation means fewer peptides competing for ionization at any instant —
directly improving depth of coverage.

**Next:** check your understanding of the basics.
""",
        ),
        _quiz(),
    ),
)


# ── Proteomics & Metabolomics — Intermediate ────────────────  (FDR) ──

_INTERMEDIATE = SeedCourse(
    slug="proteomics-metabolomics-intermediate",
    title="Proteomics & Metabolomics — Intermediate",
    description=(
        "The quantitative core of MS-based proteomics: tandem MS and peptide "
        "fragmentation, database searching with target-decoy FDR control, the "
        "DDA vs DIA acquisition strategies, and the major quantification methods "
        "— label-free (LFQ), metabolic labeling (SILAC) and isobaric tags "
        "(TMT/iTRAQ). Interactive plots of fragment ladders and ratios."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Tandem MS (MS/MS) & peptide fragmentation",
            "12 min",
            r"""
# Tandem MS (MS/MS) & peptide fragmentation

Measuring a peptide's mass alone rarely identifies it — many sequences share a
mass. **Tandem mass spectrometry (MS/MS)** adds sequence information: a
**precursor** ion is isolated, fragmented, and the masses of its fragments are
recorded as an **MS2** spectrum.

```mermaid
flowchart LR
  A["MS1 survey scan"] --> B["Isolate precursor (m/z)"]
  B --> C["Collision cell (CID/HCD)"]
  C --> D["MS2 fragment spectrum"]
  D --> E["Sequence from mass ladder"]
```

The most common method, **collision-induced dissociation (CID)** (or HCD on
Orbitraps), breaks the amide backbone to give **b-ions** (charge retained on the
N-terminus) and **y-ions** (charge on the C-terminus). Consecutive y-ions differ
by exactly one residue mass, so the spacing between peaks spells out the sequence
— a **mass ladder**. For a residue of monoisotopic mass $m_i$, adjacent y-ions
satisfy:

$$m(y_{n}) - m(y_{n-1}) = m_i$$

Alternative dissociation methods — **ETD/ECD** (electron transfer/capture) — give
c- and z-ions and preserve labile PTMs, complementing CID. Reading the gaps
between fragment peaks is the heart of de novo sequencing.

```plot
{"title": "y-ion ladder (idealized)", "xLabel": "fragment index", "yLabel": "cumulative mass (relative)", "xRange": [0,8], "yRange": [0,8], "grid": true, "functions": [{"expr": "x", "label": "y-ion mass (each step = one residue)", "color": "#2563eb"}]}
```

**Next:** matching spectra to sequences with database search.
""",
        ),
        _t(
            "Database search & peptide-spectrum matches",
            "12 min",
            r"""
# Database search & peptide-spectrum matches

Given an experimental MS2 spectrum, how do we name the peptide? **Database
search** engines (SEQUEST, Mascot, Andromeda in MaxQuant, MSFragger) take a
protein FASTA file, perform an *in silico* tryptic digest, predict the theoretical
fragment ions for each candidate peptide within the precursor mass tolerance, and
**score** the match against the observed spectrum.

```mermaid
flowchart LR
  A["Protein FASTA"] --> B["In silico digest -> candidate peptides"]
  C["Observed MS2"] --> D["Match to predicted fragments"]
  B --> D
  D --> E["Score each PSM"]
  E --> F["Best peptide-spectrum match"]
```

The output is a **peptide-spectrum match (PSM)** with a score reflecting how many
predicted b/y ions are observed and how intense they are. Engines like Andromeda
use a binomial probability that the observed matches arose by chance; lower
probability means a better, more significant match.

Key search parameters: **precursor tolerance** (e.g. 10 ppm on a high-res
instrument), **fragment tolerance**, **fixed modifications** (carbamidomethyl on
Cys from alkylation), **variable modifications** (oxidized Met), and **missed
cleavages**. Too loose a tolerance inflates the candidate list and false matches;
too tight loses real IDs. The score distribution of correct matches separates
from random ones — but never perfectly, which is why we need statistical control.

**Next:** controlling errors with target-decoy FDR.
""",
        ),
        _t(
            "False discovery rate & target-decoy",
            "11 min",
            r"""
# False discovery rate & target-decoy

With millions of spectra searched, some high-scoring PSMs are wrong by chance.
Reporting them uncontrolled would corrupt the result. Proteomics controls the
**false discovery rate (FDR)** — the expected fraction of accepted
identifications that are incorrect — using the elegant **target-decoy** strategy.

```mermaid
flowchart LR
  A["Target proteins (real)"] --> C["Combined database"]
  B["Decoy proteins (reversed/shuffled)"] --> C
  C --> D["Search all spectra"]
  D --> E["Count target vs decoy hits above score t"]
  E --> F["Estimate FDR, set threshold"]
```

A **decoy** database of reversed or randomized sequences is searched alongside
the real (target) one. Decoy hits cannot be correct, so they estimate the rate of
false target hits at any score threshold $t$:

$$\text{FDR}(t) = \frac{N_{\text{decoy}}(t)}{N_{\text{target}}(t)}$$

The community standard is **1% FDR** at the PSM, peptide and protein levels. As
the score threshold is relaxed, identifications rise but so does the false
fraction — the trade-off curve every analyst tunes:

```plot
{"title": "FDR vs identifications as threshold relaxes", "xLabel": "identifications accepted (relative)", "yLabel": "FDR", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "x/(x+8)", "label": "estimated FDR", "color": "#dc2626"}]}
```

A related per-hit measure, the **posterior error probability (PEP)**, gives the
probability that one specific match is wrong, complementing the global FDR.

**Next:** how spectra are acquired — DDA vs DIA.
""",
        ),
        _t(
            "Acquisition strategies: DDA vs DIA",
            "11 min",
            r"""
# Acquisition strategies: DDA vs DIA

The instrument cannot fragment everything at once, so the **acquisition method**
decides which precursors get an MS2 scan. The two paradigms are
**data-dependent acquisition (DDA)** and **data-independent acquisition (DIA)**.

```mermaid
flowchart TB
  subgraph DDA
    A["MS1 survey"] --> B["Pick top-N most intense"]
    B --> C["Fragment each in turn"]
  end
  subgraph DIA
    D["MS1 survey"] --> E["Fragment fixed m/z windows"]
    E --> F["All precursors in window co-fragment"]
  end
```

In **DDA**, the software picks the **top-N** most intense precursors per cycle for
MS2. It is simple and gives clean, interpretable spectra, but it is stochastic:
low-abundance peptides are often missed, causing **missing values** across runs.

In **DIA** (e.g. SWATH), the analyzer steps through fixed isolation windows and
fragments **all** precursors in each window, producing complex multiplexed MS2
spectra. DIA samples the sample comprehensively and reproducibly, eliminating the
top-N bottleneck — at the cost of harder deconvolution, handled by spectral
libraries or library-free tools (DIA-NN, Spectronaut) often using deep learning
to predict spectra. The number of peptides identified rises with gradient length
but saturates as the most ionizable species are exhausted:

```plot
{"title": "IDs vs gradient length (saturating)", "xLabel": "gradient length (relative)", "yLabel": "peptides identified", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/8.5", "label": "depth of coverage", "color": "#16a34a"}]}
```

**Next:** turning spectra into numbers — quantification.
""",
        ),
        _t(
            "Quantification: label-free, SILAC & TMT",
            "12 min",
            r"""
# Quantification: label-free, SILAC & TMT

Identifying peptides is only half the job; biology needs **how much**. Three
quantification families dominate, differing in where samples are combined.

```mermaid
flowchart LR
  A["Samples"] --> B{"Quant strategy"}
  B --> C["Label-free (LFQ): separate runs"]
  B --> D["SILAC: metabolic heavy labels"]
  B --> E["TMT/iTRAQ: isobaric tags"]
```

**Label-free quantification (LFQ)** runs each sample separately and compares
either the integrated MS1 peak area (intensity) or spectral counts. It is cheap
and unlimited in sample number but sensitive to run-to-run variation and missing
values.

**SILAC** feeds cells media with heavy isotopes (e.g. $^{13}\text{C}_6$-lysine);
light and heavy samples are mixed early, so the same peptide appears as a doublet
in MS1 and the area ratio gives relative abundance with minimal technical error.

**TMT/iTRAQ** uses **isobaric tags**: chemically identical mass at MS1, so labeled
peptides co-elute and co-isolate, but on fragmentation each tag releases a
distinct low-mass **reporter ion** whose intensity quantifies that channel. TMT
multiplexes up to 18 samples in one run, boosting throughput — though
co-isolation of interfering ions causes **ratio compression**. Measured ratios
trend toward the true ratio but are dampened:

```plot
{"title": "TMT ratio compression", "xLabel": "true fold-change", "yLabel": "measured fold-change", "xRange": [0,10], "yRange": [0,10], "grid": true, "functions": [{"expr": "x", "label": "ideal (no compression)", "color": "#16a34a"}, {"expr": "8*x/(3+x)", "label": "compressed", "color": "#dc2626"}]}
```

**Next:** check your understanding of the methods.
""",
        ),
        _quiz(),
    ),
)


# ── Proteomics & Metabolomics — Advanced ────────────────  (PTM + ML) ──

_ADVANCED = SeedCourse(
    slug="proteomics-metabolomics-advanced",
    title="Proteomics & Metabolomics — Advanced",
    description=(
        "State-of-the-art MS omics: post-translational modifications and "
        "phosphoproteomics with localization scoring, untargeted metabolomics "
        "and the annotation/identification problem, deep learning for spectrum "
        "and retention-time prediction, single-cell proteomics, and statistical "
        "multi-omics integration. Interactive plots and pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Post-translational modifications & phosphoproteomics",
            "12 min",
            r"""
# Post-translational modifications & phosphoproteomics

Proteoform diversity comes largely from **post-translational modifications
(PTMs)** — covalent changes that switch activity, localization and interactions.
Phosphorylation, acetylation, ubiquitination and glycosylation each shift a
residue mass by a characteristic amount, which MS detects as a **variable
modification**: phospho adds $+79.966\,\text{Da}$ (HPO$_3$), acetyl $+42.011$.

```mermaid
flowchart LR
  A["Digest"] --> B["Enrich modified peptides"]
  B --> C["IMAC / TiO2 for phospho"]
  C --> D["LC-MS/MS"]
  D --> E["Search with variable mod"]
  E --> F["Localize site (e.g. Ascore)"]
```

Modified peptides are rare, so **enrichment** is essential — **IMAC** or
**TiO$_2$** for phosphopeptides, antibodies for acetyl-lysine, lectins for
glycopeptides. The hard problem is **site localization**: a peptide with three
serines may carry the phosphate on any one. Tools compute a localization
probability (Ascore, PTM-Score) from the presence of **site-determining**
fragment ions that distinguish the isoforms. A site is confidently localized when
its probability exceeds ~0.75:

```plot
{"title": "Site-localization confidence vs score", "xLabel": "localization score", "yLabel": "P(correct site)", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "localization probability", "color": "#2563eb"}]}
```

Phosphoproteomics maps signaling networks; combined with kinase-substrate
databases it reconstructs which pathways are active in a condition.

**Next:** moving from proteins to small molecules — metabolomics.
""",
        ),
        _t(
            "Untargeted metabolomics & the annotation problem",
            "12 min",
            r"""
# Untargeted metabolomics & the annotation problem

Metabolomics measures small molecules ($<1500\,\text{Da}$). **Targeted** assays
quantify a known panel with standards; **untargeted** profiling tries to capture
everything and discover the unexpected. The catch: identifying an unknown small
molecule from its mass alone is far harder than identifying a peptide, because
metabolites have no simple polymer alphabet.

```mermaid
flowchart LR
  A["LC-MS raw data"] --> B["Peak detection (XCMS)"]
  B --> C["Alignment + grouping -> features"]
  C --> D["Accurate mass + isotopes -> formula"]
  D --> E["MS/MS spectral matching"]
  E --> F["Annotation (confidence level)"]
```

A high-resolution mass and isotope pattern constrain the **molecular formula**,
but many isomers share a formula. MS/MS fragmentation and matching to libraries
(METLIN, MassBank, GNPS) narrow it further. The field reports a **confidence
level** (Schymanski 1–5): level 1 = confirmed with a reference standard, down to
level 5 = exact mass only.

The bottleneck is coverage: a typical study detects thousands of **features**
(unique $m/z$–retention-time pairs) yet annotates only a minority — the **dark
metabolome**. Annotated fraction grows slowly as more orthogonal evidence is
added:

```plot
{"title": "Annotated fraction vs evidence layers", "xLabel": "evidence layers used", "yLabel": "fraction annotated", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "annotation coverage", "color": "#16a34a"}]}
```

**Next:** how deep learning is rewriting spectrum interpretation.
""",
        ),
        _t(
            "Deep learning for spectra & retention time",
            "12 min",
            r"""
# Deep learning for spectra & retention time

Classical search engines treat fragment intensities as roughly equal. In reality
fragmentation is reproducible and predictable — which **deep learning** now
exploits. Models like **Prosit**, **DeepMass** and **pDeep** predict, from a
peptide sequence and charge, the full MS2 **fragment intensity pattern** and the
**retention time**, with accuracy rivaling experiment.

```mermaid
flowchart LR
  A["Peptide sequence + charge"] --> B["Deep model (LSTM/Transformer)"]
  B --> C["Predicted MS2 intensities"]
  B --> D["Predicted retention time"]
  C --> E["Rescore PSMs / build in-silico library"]
  D --> E
```

This enables three advances. First, **predicted spectral libraries** make
library-free DIA practical (DIA-NN), removing the need for costly experimental
libraries. Second, **rescoring** tools (e.g. via Percolator with predicted
features, MS2Rescore) compare observed and predicted intensity vectors, using the
**spectral angle** as a powerful feature that pushes more true PSMs above 1% FDR.
Third, retention-time prediction filters chemically impossible identifications.

The spectral angle $SA = 1 - \frac{2}{\pi}\arccos(\cos\theta)$ between observed
and predicted intensity vectors rises sharply for correct matches:

```plot
{"title": "Spectral angle gain in rescoring", "xLabel": "match quality (a.u.)", "yLabel": "true PSMs recovered (rel.)", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "recovery with ML features", "color": "#2563eb"}]}
```

De novo sequencing models (Casanovo, a transformer) now read spectra directly
into sequence, useful when no database exists.

**Next:** measuring proteomes one cell at a time.
""",
        ),
        _t(
            "Single-cell proteomics",
            "11 min",
            r"""
# Single-cell proteomics

Bulk proteomics averages over millions of cells, masking heterogeneity. **Single-
cell proteomics (SCP)** measures the proteome of individual cells — a frontier
driven by sensitivity gains, because one cell contains only ~$250\,\text{pg}$ of
protein, a million-fold less than a typical bulk sample.

```mermaid
flowchart LR
  A["Isolate single cells"] --> B["Nanoliter lysis + digest"]
  B --> C["TMT multiplex with carrier"]
  C --> D["LC-MS/MS (low-flow)"]
  D --> E["Per-cell protein quantities"]
  E --> F["Cluster cell states"]
```

Key innovations: **miniaturized sample prep** in nanoliter volumes (nanoPOTS) to
avoid losses on surfaces; **isobaric multiplexing with a carrier channel**
(SCoPE-MS) where a high-abundance booster sample drives ion statistics while
reporter ions quantify single cells; and very low-flow LC with extremely
sensitive instruments. Current methods quantify on the order of $1000$–$5000$
proteins per cell.

The signal-to-noise improves with the number of cells/ions sampled roughly as
$\sqrt{N}$, the fundamental Poisson limit of counting ions:

```plot
{"title": "Counting-noise limit: S/N vs ions sampled", "xLabel": "ions sampled (relative)", "yLabel": "signal-to-noise", "xRange": [0,10], "yRange": [0,3.5], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "S/N ~ sqrt(N)", "color": "#2563eb"}]}
```

SCP is reshaping cancer and developmental biology by exposing rare cell states
invisible to bulk measurement, complementing single-cell transcriptomics.

**Next:** integrating proteins, metabolites and genes — multi-omics.
""",
        ),
        _t(
            "Multi-omics integration",
            "12 min",
            r"""
# Multi-omics integration

No single omics layer tells the whole story. **Multi-omics integration** combines
genomics, transcriptomics, proteomics and metabolomics to model a system across
the central dogma — but the layers differ in scale, noise and missingness, making
integration a hard statistical problem.

```mermaid
flowchart TB
  G["Genome"] --> I["Integration model"]
  T["Transcriptome"] --> I
  P["Proteome"] --> I
  M["Metabolome"] --> I
  I --> O["Biomarkers / pathway activity / subtypes"]
```

Integration strategies fall into families. **Early integration** concatenates all
features into one matrix; **intermediate integration** learns a shared latent
space — methods like **MOFA** (multi-omics factor analysis), **DIABLO** (sparse
multivariate) and similarity-network fusion find joint factors explaining
variance across layers; **late integration** builds a model per omics and
combines predictions. Pathway- and network-based methods map features onto known
biology (KEGG, Reactome) to interpret the joint signal.

A central tension is the **curse of dimensionality**: each layer adds thousands of
features but samples stay scarce, so regularization (sparsity) and dimensionality
reduction are essential. The variance explained by added latent factors falls off
quickly — most signal sits in a few shared factors:

```plot
{"title": "Variance explained per latent factor", "xLabel": "factor number", "yLabel": "variance explained", "xRange": [1,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "scree (decaying)", "color": "#dc2626"}]}
```

Done well, integration yields mechanistic biomarkers and disease subtypes no
single layer reveals — the goal of systems-level molecular medicine.

**Next:** check your understanding of the advanced material.
""",
        ),
        _quiz(),
    ),
)


PROTEOMICS_METABOLOMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PROTEOMICS_METABOLOMICS_COURSES"]
