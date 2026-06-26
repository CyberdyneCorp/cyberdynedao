"""Sequence Analysis & Alignment track: Basics -> Intermediate -> Advanced.

A university-level path from biological sequences, scoring schemes and dot plots,
through pairwise and multiple alignment, BLAST and its statistics, to profile
HMMs, sequence motifs and protein-domain detection. Lessons embed interactive
```plot blocks for quantitative relationships (scoring, E-values, information
content, neural performance) and ```mermaid diagrams for algorithms, pipelines
and classifications.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Sequence Analysis -- Basics -----------------------------------------------

_BASICS = SeedCourse(
    slug="sequence-analysis-basics",
    title="Sequence Analysis & Alignment — Basics",
    description=(
        "The foundations of comparing biological sequences: what a sequence is, "
        "why homology and alignment matter, how matches, mismatches and gaps are "
        "scored, how identity and similarity differ, and how dot plots give a "
        "first visual picture of relatedness. Built on real biological detail "
        "with interactive plots and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What sequence analysis is and why we align",
            "10 min",
            r"""
# What sequence analysis is and why we align

**Sequence analysis** compares biological sequences — DNA, RNA or protein — to
reveal shared ancestry, conserved function and divergence. Its central tool is
**alignment**: lining up two or more sequences so that corresponding residues
sit in the same column. The biological motivation is **homology** — sequences
that descend from a common ancestor tend to remain similar, so a good alignment
exposes that shared signal against a background of random change.

```mermaid
flowchart LR
  A["Common ancestor sequence"] --> B["Species 1 sequence"]
  A --> C["Species 2 sequence"]
  B --> ALN["Alignment"]
  C --> ALN
  ALN --> INF["Homology, conservation, function"]
```

A crucial distinction: **homology** is a yes/no statement of shared ancestry,
while **similarity** (percent identity) is a measurable quantity. High
similarity is evidence for homology but is not the same thing. Two related
sequences diverge over time, so the fraction of identical positions decays
roughly exponentially as evolutionary distance grows.

```plot
{"title": "Sequence identity decays with divergence time", "xLabel": "evolutionary distance", "yLabel": "fraction identical", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "percent identity", "color": "#2563eb"}]}
```

Because related sequences keep functionally important residues conserved,
alignment is the gateway to nearly every downstream task: search, annotation,
structure prediction and phylogenetics.

**Next:** how matches, mismatches and gaps are scored.
""",
        ),
        _t(
            "Scoring matches, mismatches and gaps",
            "11 min",
            r"""
# Scoring matches, mismatches and gaps

To compare alignments objectively we attach a **score**. Each aligned column is
rewarded or penalised: a **match** scores positively, a **mismatch**
negatively, and a **gap** (an insertion or deletion, an *indel*) carries a
penalty. The alignment score is the sum over all columns, and the best
alignment is the one that maximises this total.

A simple DNA scheme might give $+1$ for a match, $-1$ for a mismatch, and $-2$
per gap position. For a fixed identity, the expected score grows linearly with
the number of aligned columns, so longer convincing alignments accumulate more
signal.

```plot
{"title": "Expected alignment score vs aligned length", "xLabel": "aligned columns", "yLabel": "raw score", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "1*x", "label": "score ~ length", "color": "#16a34a"}]}
```

Gaps need special care. A single long indel is biologically more plausible than
many separate ones, so an **affine** gap model charges a large **opening** cost
plus a small **extension** cost per residue: $\gamma(g) = -(o + e \cdot g)$.

```mermaid
flowchart LR
  COL["Each aligned column"] --> M["Match: +"]
  COL --> X["Mismatch: -"]
  COL --> G["Gap: opening + extension"]
  M --> S["Total alignment score"]
  X --> S
  G --> S
```

Choosing the scoring scheme is not cosmetic: it decides which alignment wins and
therefore what biological conclusion you draw.

**Next:** percent identity versus similarity, and conservative substitutions.
""",
        ),
        _t(
            "Identity, similarity and conservation",
            "11 min",
            r"""
# Identity, similarity and conservation

Once two sequences are aligned, we summarise how alike they are. **Percent
identity** is the fraction of aligned columns that hold the same residue.
**Similarity** is broader: for proteins it counts **conservative
substitutions** — swaps between chemically alike amino acids (e.g. leucine for
isoleucine) that usually preserve function — so similarity is always at least as
high as identity.

```mermaid
flowchart TB
  ALN["Aligned columns"] --> ID["Identical residue -> identity"]
  ALN --> SIM["Similar residue -> similarity"]
  ALN --> DIFF["Different -> mismatch"]
  ID --> SCORE["Summary statistics"]
  SIM --> SCORE
```

A famous rule of thumb is the **twilight zone**: above roughly 30% identity
homology is usually clear, but below it true relationships hide among chance
similarities and must be confirmed with sensitive methods. The reliability of a
percent-identity call rises steeply with the length of the aligned region,
because short matches happen by chance.

```plot
{"title": "Confidence in homology vs alignment length", "xLabel": "aligned length (residues)", "yLabel": "confidence", "xRange": [0, 100], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+20)", "label": "saturating confidence", "color": "#2563eb"}]}
```

Conservation is positional: active-site and structural residues stay fixed while
surface loops vary freely. Reading *which* columns are conserved, not just how
many, is where biological insight begins.

**Next:** seeing relatedness at a glance with dot plots.
""",
        ),
        _t(
            "Dot plots: visualising sequence relatedness",
            "11 min",
            r"""
# Dot plots: visualising sequence relatedness

A **dot plot** is the simplest way to *see* the relationship between two
sequences before any alignment algorithm runs. One sequence labels the rows, the
other the columns, and a dot is placed wherever two residues match. Diagonal
runs of dots reveal regions of similarity at a glance.

```mermaid
flowchart LR
  X["Sequence X on x-axis"] --> GRID["Match matrix"]
  Y["Sequence Y on y-axis"] --> GRID
  GRID --> DIAG["Diagonals = similar regions"]
  DIAG --> READ["Read structure visually"]
```

The patterns are interpretable: a single main diagonal means the sequences are
globally similar; broken or shifted diagonals signal **insertions and
deletions**; off-diagonal segments reveal **repeats**; and an anti-diagonal
hints at an **inverted** (reverse-complement) region. To suppress random
single-residue noise, dot plots use a sliding **window** and a **threshold**,
plotting a dot only when enough residues in the window match.

Random matches grow with sequence size: for two random DNA sequences, the
expected number of chance dots scales with the product of their lengths, so
larger comparisons need stricter windows.

```plot
{"title": "Expected chance dots vs sequence length", "xLabel": "sequence length", "yLabel": "expected random dots", "xRange": [0, 100], "yRange": [0, 2600], "grid": true, "functions": [{"expr": "0.25*x*x/4", "label": "~ L^2 / alphabet", "color": "#dc2626"}]}
```

Dot plots remain a fast diagnostic — for self-comparison, repeats and rearrangements.

**Next:** the alphabets and substitution patterns that scoring captures.
""",
        ),
        _t(
            "Sequence alphabets and substitution patterns",
            "11 min",
            r"""
# Sequence alphabets and substitution patterns

Scoring is only meaningful if it reflects how sequences actually change. DNA uses
a 4-letter alphabet $\{A, C, G, T\}$; proteins use 20 amino acids. The mutations
between them are **not** equally likely, and good scoring schemes encode that.

In DNA, **transitions** (purine to purine, $A \leftrightarrow G$, or pyrimidine
to pyrimidine, $C \leftrightarrow T$) occur far more often than **transversions**
(purine to pyrimidine). In proteins, swaps between chemically similar residues
are common while drastic changes are rare and often deleterious.

```mermaid
flowchart LR
  MUT["Observed substitutions"] --> TS["Transitions (frequent)"]
  MUT --> TV["Transversions (rare)"]
  TS --> MAT["Scoring matrix"]
  TV --> MAT
  MAT --> ALN["Biologically tuned alignment"]
```

These observed frequencies are turned into **log-odds** scores: a substitution
that happens more than chance scores positive, one that happens less scores
negative. Because rare, drastic mutations are penalised more, the penalty rises
sharply as chemical dissimilarity increases.

```plot
{"title": "Substitution penalty vs chemical dissimilarity", "xLabel": "dissimilarity", "yLabel": "penalty magnitude", "xRange": [0, 5], "yRange": [0, 30], "grid": true, "functions": [{"expr": "exp(x)", "label": "rare swaps cost more", "color": "#dc2626"}]}
```

This is exactly the idea formalised by PAM and BLOSUM matrices in the next
course: the alphabet plus its substitution pattern *is* the scoring model.

**Next:** check your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Sequence Analysis -- Intermediate -----------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="sequence-analysis-intermediate",
    title="Sequence Analysis & Alignment — Intermediate",
    description=(
        "The core quantitative methods of sequence comparison: dynamic-programming "
        "alignment with Needleman-Wunsch (global) and Smith-Waterman (local), "
        "substitution matrices (PAM and BLOSUM) and affine gap penalties, "
        "heuristic database search with BLAST and its E-value statistics, and "
        "multiple sequence alignment with progressive methods. Includes "
        "interactive plots of scoring and search statistics."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Global alignment with Needleman-Wunsch",
            "13 min",
            r"""
# Global alignment with Needleman-Wunsch

A **global alignment** lines up two sequences end to end. Brute force is
exponential, but the **Needleman-Wunsch** algorithm solves it exactly with
**dynamic programming** in $O(mn)$ time. It fills a matrix $F$ where $F(i,j)$ is
the best score aligning the first $i$ residues of $X$ with the first $j$ of $Y$:

$$F(i,j) = \max\begin{cases} F(i-1,j-1) + s(x_i,y_j) \\ F(i-1,j) - d \\ F(i,j-1) - d \end{cases}$$

Here $s$ is the substitution score and $d$ the gap penalty. After filling the
matrix, a **traceback** from the bottom-right corner reconstructs the optimal
alignment.

```mermaid
flowchart LR
  INIT["Initialise first row/column with gap costs"] --> FILL["Fill F(i,j) by recurrence"]
  FILL --> TB["Traceback from F(m,n)"]
  TB --> ALN["Optimal global alignment"]
```

The defining feature of DP is that work scales with the **product** of the two
lengths, not exponentially — turning an intractable problem into a routine one.
For aligning a sequence against ones of growing length, runtime rises linearly
once the other length is fixed.

```plot
{"title": "Needleman-Wunsch matrix cells to fill", "xLabel": "length of sequence Y", "yLabel": "cells (x1000) for m=50", "xRange": [0, 100], "yRange": [0, 5], "grid": true, "functions": [{"expr": "50*x/1000", "label": "cells = m * n", "color": "#2563eb"}]}
```

Needleman-Wunsch is the right choice when both sequences are expected to be
related along their whole length.

**Next:** local alignment for finding shared sub-regions.
""",
        ),
        _t(
            "Local alignment with Smith-Waterman",
            "12 min",
            r"""
# Local alignment with Smith-Waterman

Often two sequences share only a **region** — a conserved domain inside
otherwise unrelated proteins. **Local alignment** finds the best-scoring
*subsegment*, and the **Smith-Waterman** algorithm computes it exactly. It uses
the same DP table as Needleman-Wunsch with two changes: a **zero** option in the
recurrence, and traceback starting from the matrix's **maximum** cell.

$$H(i,j) = \max\begin{cases} 0 \\ H(i-1,j-1) + s(x_i,y_j) \\ H(i-1,j) - d \\ H(i,j-1) - d \end{cases}$$

The zero clamps scores at the floor, so a region of poor matching cannot drag
the alignment negative; instead the algorithm simply restarts a fresh local
alignment.

```mermaid
flowchart LR
  FILL["Fill H with 0-floor recurrence"] --> MAX["Find maximum cell"]
  MAX --> TB["Traceback until a 0 is reached"]
  TB --> SUB["Best local sub-alignment"]
```

Because scores cannot go below zero, the score profile along a sequence stays at
the floor in unrelated regions and rises only where similarity exists — a
rectified, non-negative behaviour.

```plot
{"title": "Local score is floored at zero", "xLabel": "position along sequence", "yLabel": "running local score", "xRange": [0, 10], "yRange": [0, 30], "grid": true, "functions": [{"expr": "abs(x-5)*4", "label": "rectified, never negative", "color": "#16a34a"}]}
```

Smith-Waterman is the conceptual core of BLAST and of every tool that hunts for
shared domains rather than end-to-end matches.

**Next:** the substitution matrices that make scores biological.
""",
        ),
        _t(
            "Substitution matrices: PAM and BLOSUM",
            "13 min",
            r"""
# Substitution matrices: PAM and BLOSUM

For proteins, a **substitution matrix** gives a log-odds score for every
amino-acid pair, derived from how often each substitution is observed in related
sequences versus chance:

$$s(a,b) = \frac{1}{\lambda} \log \frac{p_{ab}}{q_a q_b}$$

where $p_{ab}$ is the observed joint frequency and $q_a q_b$ the expected one.

**PAM** matrices (Dayhoff) are built from closely related sequences and a model
of **accepted point mutations**, then extrapolated to longer distances by matrix
multiplication — so PAM250 represents distant relatives. **BLOSUM** matrices are
built directly from conserved **blocks** clustered at an identity threshold:
BLOSUM62 (the BLAST default) uses blocks at 62% identity.

```mermaid
flowchart LR
  ALN["Trusted alignments / blocks"] --> FREQ["Observed frequencies p_ab"]
  FREQ --> LO["Log-odds scores"]
  LO --> MAT["PAM / BLOSUM matrix"]
  MAT --> SCORE["Used in alignment & BLAST"]
```

The two families run in **opposite directions**: a *higher* PAM number means
*more* divergence, whereas a *higher* BLOSUM number means *less*. So BLOSUM45 (or
PAM250) suits distant homologs while BLOSUM80 (or PAM30) suits close ones. The
right matrix for the expected divergence maximises sensitivity.

```plot
{"title": "Match score declines with evolutionary distance", "xLabel": "PAM distance (more divergence)", "yLabel": "average identity score", "xRange": [0, 250], "yRange": [0, 5], "grid": true, "functions": [{"expr": "5*exp(-0.01*x)", "label": "score shrinks as PAM rises", "color": "#dc2626"}]}
```

**Next:** affine gaps and tuning the gap model.
""",
        ),
        _t(
            "Affine gap penalties and gap models",
            "12 min",
            r"""
# Affine gap penalties and gap models

A **linear** gap model charges a fixed cost per gap position, which wrongly makes
one 10-residue indel as costly as ten scattered 1-residue indels. Biology favours
fewer, longer indels, so the standard is the **affine** model: a large
**opening** penalty $o$ plus a small **extension** penalty $e$ per residue,
giving total cost $\gamma(g) = -(o + e \cdot g)$ for a gap of length $g$.

```mermaid
flowchart LR
  GAP["Open a new gap"] --> OPEN["Pay opening cost o"]
  OPEN --> EXT["Each extra residue pays e"]
  EXT --> TOTAL["Total = o + e*g"]
```

Because $o$ is paid once and $e$ many times, the per-residue cost of a gap
*drops* as it lengthens — exactly the incentive to merge indels. Affine scoring
needs the **Gotoh** algorithm, which keeps three DP matrices (match, gap-in-X,
gap-in-Y) but preserves the $O(mn)$ runtime.

```plot
{"title": "Affine vs linear gap penalty", "xLabel": "gap length g", "yLabel": "penalty magnitude", "xRange": [0, 20], "yRange": [0, 40], "grid": true, "functions": [{"expr": "10 + 1*x", "label": "affine: o + e*g", "color": "#2563eb"}, {"expr": "2*x", "label": "linear: c*g", "color": "#dc2626"}]}
```

Note how the linear line starts lower but overtakes the affine one: linear
under-penalises a first gap yet over-penalises a long one. Tuning $o$ and $e$ to
the substitution matrix is essential — mismatched gap costs produce alignments
riddled with implausible micro-indels.

**Next:** searching whole databases fast with BLAST.
""",
        ),
        _t(
            "BLAST and E-value statistics",
            "13 min",
            r"""
# BLAST and E-value statistics

Running full Smith-Waterman against an entire database is too slow, so **BLAST**
(Basic Local Alignment Search Tool) uses a **seed-and-extend** heuristic. It
breaks the query into short **words** (k-mers — length 3 for proteins, 11 for
DNA by default), finds where those words hit the indexed database, and only there
does it extend into local alignments called **high-scoring pairs (HSPs)**.

```mermaid
flowchart LR
  Q["Query"] --> W["List query words (k-mers)"]
  W --> HIT["Find word hits in DB index"]
  HIT --> EXT["Ungapped then gapped extension"]
  EXT --> HSP["High-scoring pairs"]
  HSP --> E["E-value & ranking"]
```

The headline statistic is the **E-value**: the number of alignments scoring at
least $S$ expected *by chance* in a database of that size, from the
Karlin-Altschul model:

$$E = K\,m\,n\,e^{-\lambda S}$$

with query length $m$, database length $n$, and scoring parameters $K, \lambda$.
Because $E$ falls **exponentially** with score, a few extra bits of score make a
hit dramatically more significant.

```plot
{"title": "BLAST E-value vs alignment score", "xLabel": "bit score S", "yLabel": "E-value", "xRange": [0, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "E ~ exp(-lambda*S)", "color": "#2563eb"}]}
```

A common cutoff is $E < 10^{-5}$ for confident homology. The BLAST family —
blastn, blastp, blastx, tblastn — covers nucleotide and protein queries against
either kind of database.

**Next:** aligning many sequences at once.
""",
        ),
        _t(
            "Multiple sequence alignment basics",
            "12 min",
            r"""
# Multiple sequence alignment basics

A **multiple sequence alignment (MSA)** aligns three or more sequences at once,
exposing columns of conservation and the variation that drives motif discovery,
profile building and phylogenetics. Optimal MSA by DP is NP-hard — cost grows
like $L^N$ for $N$ sequences of length $L$ — so practical tools are heuristic.

The dominant strategy is **progressive alignment**: estimate pairwise
distances, build a **guide tree**, then align sequences and profiles from most to
least similar, never undoing earlier decisions. **Clustal Omega**, **MUSCLE** and
**MAFFT** add iterative refinement and consistency scoring to reduce the
"greedy" errors of pure progressive alignment.

```mermaid
flowchart TB
  SEQ["Input sequences"] --> DIST["Pairwise distances"]
  DIST --> TREE["Guide tree"]
  TREE --> PROG["Progressive alignment"]
  PROG --> REFINE["Iterative refinement"]
  REFINE --> MSA["Final MSA"]
```

The explosive cost of exact MSA is the whole reason heuristics exist: adding
sequences multiplies the search space.

```plot
{"title": "Exact MSA cost vs number of sequences", "xLabel": "number of sequences N", "yLabel": "relative cost", "xRange": [0, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "2^x", "label": "grows like L^N", "color": "#dc2626"}]}
```

Column conservation is later summarised by information content and drawn as a
sequence logo — the bridge to the profile methods of the advanced course.

**Next:** test your command of the core methods.
""",
        ),
        _quiz(),
    ),
)


# -- Sequence Analysis -- Advanced ---------------------------------------------

_ADVANCED = SeedCourse(
    slug="sequence-analysis-advanced",
    title="Sequence Analysis & Alignment — Advanced",
    description=(
        "State-of-the-art and applied sequence analysis: position-specific scoring "
        "matrices and PSI-BLAST, profile hidden Markov models with HMMER, sequence "
        "logos and information content, motif discovery, protein-domain databases "
        "(Pfam, InterPro) and structure-based alignment, and modern protein "
        "language models and AlphaFold. Includes interactive plots of information "
        "content, HMM likelihood and neural performance."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Position-specific scoring and PSI-BLAST",
            "13 min",
            r"""
# Position-specific scoring and PSI-BLAST

A single substitution matrix treats every column the same, but real families
conserve some positions absolutely and tolerate others freely. A
**position-specific scoring matrix (PSSM)** captures this: it stores a separate
log-odds score for each amino acid *at each column* of an alignment, so conserved
columns reward the right residue strongly and variable columns barely at all.

```mermaid
flowchart LR
  MSA["Seed alignment of homologs"] --> COUNT["Per-column residue counts"]
  COUNT --> PSSM["Position-specific scores"]
  PSSM --> SEARCH["Sensitive database search"]
```

**PSI-BLAST** (Position-Specific Iterated BLAST) automates this: an initial
blastp search collects significant hits, builds a PSSM from their alignment, then
searches again with the PSSM, iterating until convergence. Each round pulls in
more distant homologs that a flat matrix would miss — at the risk of
**profile drift** if unrelated hits contaminate the model.

The payoff is sensitivity to **remote homology**: detection rate climbs with
each iteration but with diminishing returns as the profile saturates.

```plot
{"title": "Remote homologs detected vs PSI-BLAST iterations", "xLabel": "iteration", "yLabel": "fraction of homologs found", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating detection", "color": "#2563eb"}]}
```

PSSMs are the conceptual step from a fixed scoring matrix to the full profile
HMMs that dominate modern family modelling.

**Next:** profile hidden Markov models and HMMER.
""",
        ),
        _t(
            "Profile hidden Markov models and HMMER",
            "13 min",
            r"""
# Profile hidden Markov models and HMMER

A **profile hidden Markov model (HMM)** is the probabilistic generalisation of a
PSSM. It represents a family with a chain of **match** states (one per consensus
column), plus **insert** and **delete** states that model indels explicitly with
their own transition probabilities — so position-specific gap behaviour is part
of the model, not a fixed penalty.

```mermaid
flowchart LR
  BEGIN["Begin"] --> M1["Match 1"]
  M1 --> M2["Match 2"]
  M1 --> I1["Insert 1"]
  M1 --> D2["Delete 2"]
  M2 --> M3["Match 3"]
  M3 --> END["End"]
```

Three algorithms drive HMMs: **Viterbi** finds the single most likely state path,
the **forward** algorithm sums probability over all paths, and **Baum-Welch**
(an EM method) trains parameters. The **HMMER** package builds profile HMMs
(`hmmbuild`) and searches with them (`hmmsearch`), underpinning the **Pfam**
domain database.

In log space, path probabilities become sums of per-position log terms, so the
model's negative log-likelihood accumulates roughly linearly along a matching
sequence.

```plot
{"title": "HMM negative log-likelihood along a sequence", "xLabel": "position", "yLabel": "accumulated -log P", "xRange": [0, 50], "yRange": [0, 100], "grid": true, "functions": [{"expr": "2*x", "label": "sums per matched column", "color": "#16a34a"}]}
```

Because they pool evidence across an entire family, profile HMMs detect distant
relationships that pairwise BLAST cannot.

**Next:** quantifying conservation with sequence logos.
""",
        ),
        _t(
            "Sequence logos and information content",
            "12 min",
            r"""
# Sequence logos and information content

A **sequence logo** turns an alignment column into a stack of letters whose total
height shows how conserved the position is and whose letter heights show the
residue mix. The height is **information content**, measured in **bits** using
Shannon entropy. For a column with residue frequencies $p_i$:

$$R = \log_2 N - \left(-\sum_i p_i \log_2 p_i\right)$$

where $N$ is the alphabet size (4 for DNA, 20 for protein). A fully conserved DNA
column carries $\log_2 4 = 2$ bits; a uniform column carries 0.

```mermaid
flowchart LR
  COL["Alignment column"] --> FREQ["Residue frequencies p_i"]
  FREQ --> ENT["Entropy H = -sum p log p"]
  ENT --> IC["Information = log2(N) - H"]
  IC --> LOGO["Letter-stack height in logo"]
```

Information content is maximal when one residue dominates and falls to zero as
the column approaches a uniform mix — making logos an instant read of which
positions matter.

```plot
{"title": "DNA column information vs dominant-residue frequency", "xLabel": "frequency of dominant base", "yLabel": "information (bits)", "xRange": [0.25, 1], "yRange": [0, 2], "grid": true, "functions": [{"expr": "2 + log(x)/log(2)", "label": "approx information content", "color": "#2563eb"}]}
```

Logos are the standard visual language for motifs, binding sites and the match
states of profile HMMs.

**Next:** discovering motifs without a known alignment.
""",
        ),
        _t(
            "Motif discovery in sequences",
            "12 min",
            r"""
# Motif discovery in sequences

A **motif** is a short, recurring pattern with biological meaning — a
transcription-factor binding site, a splice signal, a kinase target. **Motif
discovery** finds such patterns *de novo* in a set of sequences thought to share
one, without a prior alignment.

Two model families dominate. **Enumerative** methods scan candidate words and
test for over-representation. **Probabilistic** methods fit a position-weight
matrix: **MEME** uses expectation-maximisation, and **Gibbs sampling** uses
stochastic search, both refining a motif model against a background.

```mermaid
flowchart TB
  SEQ["Co-regulated sequences"] --> INIT["Initial motif guess"]
  INIT --> SCAN["Score occurrences (EM / Gibbs)"]
  SCAN --> UPDATE["Update position-weight matrix"]
  UPDATE --> SCAN
  UPDATE --> PWM["Converged motif + logo"]
```

The hard part is the signal-to-noise problem: a real motif is a faint pattern
buried in random background, and the chance of a spurious match rises as the
search space (sequence set size times length) grows.

```plot
{"title": "Expected random motif hits vs background size", "xLabel": "total background length (kb)", "yLabel": "expected chance hits", "xRange": [0, 20], "yRange": [0, 20], "grid": true, "functions": [{"expr": "1*x", "label": "hits scale with background", "color": "#dc2626"}]}
```

Discovered motifs are validated by statistical significance (E-value) and by
matching curated databases such as JASPAR for transcription-factor sites.

**Next:** protein domains, families and structure-aware alignment.
""",
        ),
        _t(
            "Protein domains and structure-based alignment",
            "13 min",
            r"""
# Protein domains and structure-based alignment

Proteins are modular: a **domain** is an independently folding, evolutionarily
reusable unit, and most proteins are mosaics of several. Classifying domains is
how we transfer functional annotation across the proteome. **Pfam** stores
profile-HMM models of domain families; **InterPro** integrates Pfam, PROSITE,
SMART and others; **CATH** and **SCOP** classify domains by 3D structure.

```mermaid
flowchart LR
  SEQ["Query protein"] --> SCAN["Scan against Pfam HMMs"]
  SCAN --> DOM["Identified domains"]
  DOM --> INT["InterPro integration"]
  INT --> ANN["Functional annotation (GO terms)"]
```

Structure is conserved far longer than sequence, so two proteins can share a fold
at undetectable sequence identity. **Structure-based alignment** (DALI, TM-align)
superposes 3D coordinates rather than residues, and the **TM-score** measures
similarity on a 0–1 scale where above ~0.5 implies the same fold. As sequences
diverge, sequence identity collapses while structural similarity persists.

```plot
{"title": "Structure outlasts sequence as divergence grows", "xLabel": "evolutionary divergence", "yLabel": "similarity (0-1)", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "sequence identity", "color": "#dc2626"}, {"expr": "exp(-0.12*x)", "label": "structural similarity", "color": "#16a34a"}]}
```

This is why domain and fold recognition extend homology detection well beyond the
reach of raw sequence alignment.

**Next:** protein language models and AlphaFold.
""",
        ),
        _t(
            "Protein language models and AlphaFold",
            "13 min",
            r"""
# Protein language models and AlphaFold

Deep learning has reshaped sequence analysis. **Protein language models** such as
the **ESM** family are transformers trained on hundreds of millions of sequences
with masked-residue prediction. Their learned **embeddings** capture structure
and function, enabling alignment-free homology detection and variant-effect
prediction directly from a single sequence.

The landmark result is **AlphaFold**, which predicts 3D protein structure from
sequence at near-experimental accuracy. It feeds a **multiple sequence
alignment** and pairwise features through the **Evoformer**, then a structure
module outputs coordinates — turning decades of alignment-based co-evolution
signal into structure.

```mermaid
flowchart LR
  SEQ["Protein sequence"] --> MSA["MSA + pair features"]
  MSA --> EVO["Evoformer (deep network)"]
  EVO --> STR["3D structure"]
  STR --> CONF["Per-residue pLDDT confidence"]
```

These models still need care: AlphaFold's per-residue **pLDDT** flags unreliable
regions, and accuracy improves with training data but with **diminishing
returns**, so diverse, curated data beats sheer volume.

```plot
{"title": "Model accuracy vs training data (diminishing returns)", "xLabel": "relative training data", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating accuracy", "color": "#16a34a"}]}
```

Embeddings, MSAs and HMM profiles increasingly combine — the modern toolkit
fuses classical alignment with learned representations.

**Next:** test your command of state-of-the-art sequence analysis.
""",
        ),
        _quiz(),
    ),
)


SEQUENCE_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["SEQUENCE_ANALYSIS_COURSES"]
