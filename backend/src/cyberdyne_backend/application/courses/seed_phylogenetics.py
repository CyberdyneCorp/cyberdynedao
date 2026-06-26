"""Phylogenetics & Molecular Evolution track: Basics -> Intermediate -> Advanced.

A university-level curriculum from trees, homology and distance methods, through
parsimony, likelihood and substitution models, to Bayesian inference, molecular
dating and phylogenomics. Lessons use interactive ```plot blocks for quantitative
relationships (saturation, likelihood, rate decay) and ```mermaid diagrams for
processes, tree concepts and analytical pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Phylogenetics & Molecular Evolution -- Basics ----------------------------

_BASICS = SeedCourse(
    slug="phylogenetics-basics",
    title="Phylogenetics & Molecular Evolution — Basics",
    description=(
        "How biologists reconstruct the tree of life from molecular data. Start "
        "with reading and rooting phylogenetic trees, the meaning of homology, "
        "orthology and paralogy, how sequences are aligned, and the first "
        "quantitative tools — genetic distances and distance-based tree building. "
        "Built on real biological detail with interactive plots and diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What a phylogenetic tree means",
            "10 min",
            r"""
# What a phylogenetic tree means

A **phylogenetic tree** is a hypothesis about the evolutionary relationships among
**taxa** — species, genes or populations. The tips (**leaves**) are the taxa we
observe today; **internal nodes** represent inferred common ancestors; **branches**
(edges) represent lineages through time. The point where a lineage splits is a
**bifurcation** (speciation or gene duplication).

Trees are read by **shared ancestry**, not by tip order. Two taxa are close
relatives if their most recent common ancestor (**MRCA**) is recent — i.e. few
nodes back — regardless of how near they are drawn on the page. Rotating the two
children of any node gives an *identical* tree.

```mermaid
flowchart TB
  ROOT["Root (oldest ancestor)"] --> A["ancestor of B,C"]
  ROOT --> D["taxon D"]
  A --> B["taxon B"]
  A --> C["taxon C"]
```

A **clade** (monophyletic group) is an ancestor plus *all* its descendants — the
only kind of group that reflects real evolutionary history. Groups that omit some
descendants are **paraphyletic** (e.g. "reptiles" excluding birds); groups built
from unrelated lineages are **polyphyletic**. Branch lengths may be arbitrary
(a **cladogram**) or scaled to amount of change or to time (a **phylogram** or
**chronogram**).

**Next:** rooting trees and the polarity of evolutionary change.
""",
        ),
        _t(
            "Rooting, polarity and the outgroup",
            "10 min",
            r"""
# Rooting, polarity and the outgroup

An **unrooted tree** shows relationships but not the *direction* of time: it has no
identified oldest ancestor. **Rooting** places the root and so gives **polarity** —
which character states are ancestral (**plesiomorphic**) versus derived
(**apomorphic**). Only a rooted tree lets us speak of "ancestor" and "descendant".

The standard method is the **outgroup**: include one or more taxa known to lie
*outside* the group of interest (the **ingroup**). The root is placed on the branch
connecting outgroup to ingroup. A good outgroup is closely related enough to align,
but unambiguously outside the ingroup.

```mermaid
flowchart LR
  OUT["Outgroup (e.g. lamprey)"] --> ROOT["Root"]
  ROOT --> ING["Ingroup MRCA"]
  ING --> SP1["fish"]
  ING --> SP2["tetrapods"]
```

Two outgroup-free alternatives exist. **Midpoint rooting** places the root at the
midpoint of the longest tip-to-tip path, assuming a roughly constant rate (a
**molecular clock**). The **molecular-clock / least-squares** rooting fits a clock
explicitly. Both can mislead when rates vary across lineages, so an outgroup is
preferred whenever a suitable one exists.

**Next:** homology — the basis for comparing sequences at all.
""",
        ),
        _t(
            "Homology, orthology and paralogy",
            "11 min",
            r"""
# Homology, orthology and paralogy

Phylogenetics compares **homologous** features — characters derived from a common
ancestor. For sequences, homology means the residues descend from the *same*
ancestral position. Similarity is *evidence* for homology but is not identical to
it: convergence can produce similarity without common ancestry (**homoplasy**).

Homologous genes come in two flavours that matter enormously. **Orthologs** arise
by **speciation** and tend to keep the ancestral function; **paralogs** arise by
**gene duplication** within a genome and often diverge in function. Building a
species tree from accidentally-sampled paralogs gives the *gene* history, not the
*species* history — a classic error.

```mermaid
flowchart TB
  ANC["Ancestral gene"] --> DUP["Duplication"]
  DUP --> P1["copy alpha"]
  DUP --> P2["copy beta"]
  P1 --> S1["alpha in species A (ortholog)"]
  P1 --> S2["alpha in species B (ortholog)"]
  P2 --> S3["beta in species A (paralog of alpha)"]
```

We also distinguish **positional homology** (the aligned column) from **gene
orthology**. Tools such as OrthoFinder, OMA and reciprocal-best-BLAST-hit
heuristics try to identify orthologs; getting this right is the first quality
control step of any molecular phylogeny.

**Next:** turning raw sequences into an alignment of homologous columns.
""",
        ),
        _t(
            "Multiple sequence alignment",
            "11 min",
            r"""
# Multiple sequence alignment

A tree is only as good as its **alignment**. A **multiple sequence alignment
(MSA)** arranges sequences in a matrix so that each **column** holds residues
inferred to be positionally homologous; insertions and deletions (**indels**) are
shown as **gaps** ("-"). Misaligned columns inject false signal, so alignment is a
substantive evolutionary inference, not mere formatting.

Pairwise alignment is solved optimally by dynamic programming
(Needleman–Wunsch, global; Smith–Waterman, local), scoring matches, mismatches and
gaps. Exact multiple alignment is computationally intractable, so practical tools
use **progressive** alignment along a guide tree (Clustal, MAFFT, MUSCLE) and
**iterative** refinement; T-Coffee and probabilistic methods (ProbCons) add
consistency information.

```mermaid
flowchart LR
  SEQ["Unaligned sequences"] --> GUIDE["Guide tree (quick distances)"]
  GUIDE --> PROG["Progressive alignment"]
  PROG --> REF["Iterative refinement"]
  REF --> TRIM["Trim ambiguous columns (trimAl, Gblocks)"]
  TRIM --> MSA["Final MSA"]
```

Gap-rich, ambiguously aligned regions are often **masked** before tree building
(trimAl, Gblocks) to avoid spurious homology claims. Codon-aware alignment of
protein-coding genes (align at the amino-acid level, back-translate) preserves the
reading frame and improves accuracy.

**Next:** measuring evolutionary distance between aligned sequences.
""",
        ),
        _t(
            "Genetic distances and saturation",
            "11 min",
            r"""
# Genetic distances and saturation

The simplest measure of divergence is the **p-distance**: the proportion of
aligned sites that differ. But as time passes, multiple substitutions hit the same
site (a base mutates, then mutates again or reverts). The observed differences
**saturate** and underestimate the true number of substitutions per site.

A **correction** maps observed differences to an estimated true distance under a
substitution model. The **Jukes–Cantor (JC69)** correction, assuming equal base
frequencies and equal rates, is
$$d = -\frac{3}{4}\,\ln\!\left(1 - \frac{4}{3}p\right)$$
where $p$ is the p-distance and $d$ is substitutions per site. As $p \to 0.75$ the
correction blows up — the signal is saturated.

```plot
{"title": "Multiple-hit correction: corrected vs observed distance", "xLabel": "observed p-distance", "yLabel": "corrected distance d", "xRange": [0, 0.7], "yRange": [0, 3], "grid": true, "functions": [{"expr": "-0.75*log(1-(4/3)*x)", "label": "JC69 corrected d", "color": "#2563eb"}, {"expr": "x", "label": "uncorrected (p)", "color": "#dc2626"}]}
```

Richer models add a **transition/transversion** bias (Kimura 2-parameter, K80) or
unequal base frequencies. The corrected pairwise distances fill a **distance
matrix**, the input for fast tree-building methods covered next.

**Next:** building trees directly from a distance matrix.
""",
        ),
        _t(
            "Distance-based tree building: UPGMA and Neighbor-Joining",
            "11 min",
            r"""
# Distance-based tree building: UPGMA and Neighbor-Joining

Given a distance matrix, **distance methods** cluster taxa into a tree in
polynomial time — fast enough for thousands of taxa. **UPGMA** (unweighted pair
group method with arithmetic mean) repeatedly joins the closest pair and places
their ancestor at half their distance. It produces a **rooted, ultrametric** tree
but *assumes a strict molecular clock*: equal rates in all lineages. When rates
vary, UPGMA misplaces long branches.

**Neighbor-Joining (NJ)** drops the clock assumption. It does not just join the
nearest pair; it minimizes total branch length using a corrected criterion
$$Q(i,j) = (n-2)\,d_{ij} - \sum_k d_{ik} - \sum_k d_{jk}$$
choosing the pair with the smallest $Q$. NJ is **consistent**: given additive
distances it recovers the true tree, and it handles unequal rates well.

```mermaid
flowchart LR
  MAT["Distance matrix"] --> Q["Compute Q(i,j)"]
  Q --> JOIN["Join min-Q pair into new node"]
  JOIN --> UPD["Recompute distances to new node"]
  UPD -->|more than 3 taxa| Q
  UPD -->|done| TREE["Unrooted NJ tree"]
```

NJ is a workhorse for quick trees and for building the guide tree that seeds
alignment. Its weakness: it commits to a single tree from summary distances,
discarding site-by-site information that **character-based** methods (parsimony,
likelihood) exploit — the subject of the next course.

**Next:** test your understanding of the basics.
""",
        ),
        _quiz(),
    ),
)


# -- Phylogenetics & Molecular Evolution -- Intermediate ----------------------

_INTERMEDIATE = SeedCourse(
    slug="phylogenetics-intermediate",
    title="Phylogenetics & Molecular Evolution — Intermediate",
    description=(
        "The core quantitative methods of modern phylogenetics. Maximum "
        "parsimony and homoplasy; continuous-time Markov substitution models from "
        "JC69 to GTR plus among-site rate variation; maximum likelihood and tree "
        "search; statistical confidence by bootstrap and likelihood-ratio tests; "
        "and model selection. Worked equations, plots and pipelines throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Maximum parsimony and homoplasy",
            "11 min",
            r"""
# Maximum parsimony and homoplasy

**Maximum parsimony (MP)** scores a tree by the *minimum number of character
changes* it requires; the best tree needs the fewest changes (Occam's razor).
Given a topology and the tip states, the **Fitch algorithm** computes the minimum
changes for a binary/multistate character in one post-order pass: take the
intersection of children's state sets if non-empty, else the union (adding one
step).

The catch is **homoplasy** — similarity not due to shared ancestry: convergence,
parallelism and reversal. Homoplasy inflates the apparent number of changes and
can actively *mislead* MP. The notorious failure is **long-branch attraction
(LBA)**: two unrelated long branches accumulate independent changes that, by
chance, match, and parsimony groups them together.

```mermaid
flowchart TB
  T["Candidate topology + tip states"] --> FITCH["Fitch pass (post-order)"]
  FITCH --> LEN["Tree length = total steps"]
  LEN --> SEARCH["Search topologies for minimum length"]
  SEARCH --> MPT["Most-parsimonious tree(s)"]
```

The **consistency index** $CI = m/s$ (minimum possible steps over observed steps)
and **retention index** quantify how much homoplasy a dataset carries. MP is fast
and assumption-light but statistically **inconsistent** under LBA conditions —
motivating explicit probabilistic models.

**Next:** modelling substitution as a Markov process.
""",
        ),
        _t(
            "Substitution models: from JC69 to GTR",
            "12 min",
            r"""
# Substitution models: from JC69 to GTR

Likelihood and Bayesian methods need a **probabilistic model** of how one
nucleotide changes into another. The standard framework is a **continuous-time
Markov chain** with an instantaneous **rate matrix** $Q$. The probability of
change over branch length $t$ is the matrix exponential $P(t) = e^{Qt}$.

Models form a nested hierarchy by relaxing assumptions:

- **JC69** — equal base frequencies, single rate.
- **K80 (K2P)** — distinct transition and transversion rates.
- **HKY85 / F81** — unequal base frequencies.
- **GTR** — the **general time-reversible** model: six exchangeability rates plus
  four base frequencies, the most general reversible nucleotide model.

```mermaid
flowchart LR
  JC["JC69"] --> K80["K80: ti/tv"]
  JC --> F81["F81: base freqs"]
  K80 --> HKY["HKY85"]
  F81 --> HKY
  HKY --> GTR["GTR (general time-reversible)"]
```

Under JC69, the probability that a site differs from its ancestor after time $t$
rises and **plateaus** at the equilibrium 3/4 — the source of saturation:
$$P_{\text{diff}}(t) = \frac{3}{4}\left(1 - e^{-\frac{4}{3}t}\right)$$

```plot
{"title": "JC69 probability of a difference vs branch length", "xLabel": "branch length (subst/site)", "yLabel": "P(site differs)", "xRange": [0, 6], "yRange": [0, 0.8], "grid": true, "functions": [{"expr": "0.75*(1-exp(-(4/3)*x))", "label": "P_diff(t)", "color": "#2563eb"}]}
```

**Next:** letting different sites evolve at different rates.
""",
        ),
        _t(
            "Among-site rate variation and the gamma model",
            "10 min",
            r"""
# Among-site rate variation and the gamma model

Real sequences do not evolve uniformly: some sites are highly constrained
(active-site residues, rRNA stems) and barely change, while others are nearly
free. Ignoring this **among-site rate variation (ASRV)** biases branch lengths and
topology. The standard fix multiplies the rate matrix by a site-specific rate $r$
drawn from a **gamma distribution** with mean 1 and shape parameter $\alpha$.

A small $\alpha$ (< 1) means strong rate heterogeneity — most sites slow, a few
fast (an L-shaped density); a large $\alpha$ approaches rate homogeneity. Because
integrating over a continuous gamma is costly, software (PhyML, RAxML, IQ-TREE)
uses a **discrete-gamma** approximation with typically four rate categories
("+G"). A separate **proportion of invariant sites** ("+I") models sites that
never change.

```plot
{"title": "Gamma rate density (shape controls heterogeneity)", "xLabel": "site rate r", "yLabel": "density", "xRange": [0, 4], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x*exp(-2*x)*4", "label": "alpha=2 (mild)", "color": "#2563eb"}, {"expr": "exp(-x)", "label": "alpha=1 (strong)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Q["Base rate matrix Q"] --> CAT["Discrete-gamma categories (+G)"]
  CAT --> INV["Invariant-sites fraction (+I)"]
  INV --> LIK["Per-site likelihood mixture"]
```

The model name "GTR+G+I" thus reads: general substitution process, gamma rate
variation, plus an invariant class — a sensible default for many nucleotide data.

**Next:** computing the likelihood of a tree.
""",
        ),
        _t(
            "Maximum likelihood and tree search",
            "12 min",
            r"""
# Maximum likelihood and tree search

**Maximum likelihood (ML)** chooses the tree (topology + branch lengths) that
maximizes the probability of the observed alignment under the substitution model.
For one site, **Felsenstein's pruning algorithm** computes the likelihood by a
post-order pass, combining the **conditional likelihoods** of subtrees via the
transition probabilities $P(t)=e^{Qt}$; assuming sites are independent, the
log-likelihood sums over sites.

The number of possible **unrooted topologies** explodes super-exponentially —
$(2n-5)!!$ for $n$ taxa — so exhaustive search is impossible beyond a handful of
taxa. ML software optimizes branch lengths and model parameters numerically, then
**heuristically rearranges** the topology: Nearest-Neighbor Interchange (**NNI**),
Subtree Pruning and Regrafting (**SPR**), and Tree Bisection and Reconnection
(**TBR**), keeping moves that raise the likelihood.

```plot
{"title": "Topology count grows super-exponentially", "xLabel": "number of taxa n", "yLabel": "log10(number of unrooted trees)", "xRange": [4, 20], "yRange": [0, 22], "grid": true, "functions": [{"expr": "log(1)/log(10) + (x-3)*log(2*x-5)/log(10)", "label": "approx log10 count", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  START["Starting tree (NJ/parsimony)"] --> OPT["Optimize branch lengths + model"]
  OPT --> MOVE["Propose NNI/SPR/TBR rearrangement"]
  MOVE -->|higher likelihood| OPT
  MOVE -->|no improvement| BEST["ML tree"]
```

Fast modern engines — **RAxML**, **PhyML**, **IQ-TREE** — combine these moves with
clever caching to analyse thousands of taxa.

**Next:** quantifying confidence in the inferred tree.
""",
        ),
        _t(
            "Bootstrap support and model selection",
            "11 min",
            r"""
# Bootstrap support and model selection

A single best tree says nothing about *confidence*. The **nonparametric
bootstrap** resamples alignment columns with replacement to build many
**pseudo-replicate** datasets, infers a tree from each, and reports for every clade
the percentage of replicates that recover it — the **bootstrap support**. Values
above ~70–80% are conventionally treated as well supported. Modern tools use the
faster **ultrafast bootstrap** (UFBoot) and the **SH-aLRT** branch test.

Choosing the substitution model is itself a statistical problem. Nested models are
compared with the **likelihood-ratio test (LRT)**: $2(\ln L_1 - \ln L_0)$ is
$\chi^2$-distributed under the simpler model. Non-nested models are ranked by the
**Akaike Information Criterion**, $AIC = 2k - 2\ln L$, or the **Bayesian
Information Criterion**, $BIC = k\ln n - 2\ln L$, both penalizing parameter count
$k$. ModelTest-NG and IQ-TREE's ModelFinder automate this.

```plot
{"title": "AIC trades fit against parameter count", "xLabel": "number of parameters k", "yLabel": "AIC (lower is better)", "xRange": [1, 12], "yRange": [0, 40], "grid": true, "functions": [{"expr": "2*x + 30*exp(-0.5*x)", "label": "AIC = 2k - 2lnL", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  DATA["Alignment"] --> MF["ModelFinder: fit candidate models"]
  MF --> SCORE["Rank by AIC/BIC"]
  SCORE --> BEST["Best-fit model"]
  BEST --> ML["ML tree + UFBoot support"]
```

**Next:** consolidate the core quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# -- Phylogenetics & Molecular Evolution -- Advanced --------------------------

_ADVANCED = SeedCourse(
    slug="phylogenetics-advanced",
    title="Phylogenetics & Molecular Evolution — Advanced",
    description=(
        "State-of-the-art and applied phylogenetics. Bayesian inference with "
        "MCMC and priors; relaxed-clock molecular dating with fossil and tip "
        "calibrations; the multispecies coalescent and gene-tree/species-tree "
        "discordance; phylogenomics at genome scale; detecting selection with "
        "dN/dS; and machine-learning approaches to phylogenetic inference."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Bayesian inference and MCMC",
            "12 min",
            r"""
# Bayesian inference and MCMC

Bayesian phylogenetics targets the **posterior probability** of trees:
$$P(\text{tree} \mid D) = \frac{P(D \mid \text{tree})\,P(\text{tree})}{P(D)}$$
combining the **likelihood** with **priors** on topology, branch lengths and model
parameters. The denominator integrates over *all* trees and parameters — analytically
impossible — so we sample the posterior with **Markov chain Monte Carlo (MCMC)**.

The **Metropolis–Hastings** algorithm proposes a new state, then accepts it with
probability $\min(1, r)$ where $r$ is the ratio of posterior densities times the
proposal (Hastings) ratio. Over millions of steps the chain visits states in
proportion to their posterior probability. **MrBayes**, **BEAST2** and
**RevBayes** add **Metropolis-coupled MCMC (MC³)** — several heated chains that
help escape local optima.

```mermaid
flowchart LR
  INIT["Initial tree + params"] --> PROP["Propose move (topology/length)"]
  PROP --> RATIO["Compute acceptance ratio r"]
  RATIO -->|accept| KEEP["Move to new state"]
  RATIO -->|reject| STAY["Keep current state"]
  KEEP --> SAMPLE["Sample after burn-in"]
  STAY --> SAMPLE
```

Diagnosis is essential: discard **burn-in**, check the **effective sample size
(ESS > 200)** and the **average standard deviation of split frequencies** between
runs. The output is a posterior *distribution* of trees, summarized as a
**majority-rule consensus** with **posterior probabilities** on clades.

**Next:** turning branch lengths into calendar time.
""",
        ),
        _t(
            "Relaxed clocks and molecular dating",
            "12 min",
            r"""
# Relaxed clocks and molecular dating

ML and Bayesian branch lengths are in units of *substitutions per site*, not time.
The **molecular clock** hypothesis — a roughly constant substitution rate — lets us
convert branch length to time, but a **strict clock** is usually rejected: lineages
differ in generation time, metabolic rate and population size.

**Relaxed-clock** models allow rates to vary across branches. The **uncorrelated
lognormal** clock draws each branch's rate independently from a lognormal; **random
local clocks** let rate shifts occur at a few points. Time then needs an external
**calibration**: a **fossil** placing a minimum age on a node, a known
**biogeographic** event, or **tip dates** for fast-evolving viruses
(**tip-dating**). Calibrations enter Bayesian dating as **priors** on node ages.

```plot
{"title": "Lineages-through-time under a birth-death prior", "xLabel": "time before present (relative)", "yLabel": "log10 number of lineages", "xRange": [0, 10], "yRange": [0, 3], "grid": true, "functions": [{"expr": "log(1+exp(0.6*x))/log(10)", "label": "log10 lineages", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  SEQ["Dated/undated sequences"] --> CLOCK["Relaxed clock model"]
  CAL["Fossil / tip calibrations"] --> PRIOR["Node-age priors"]
  CLOCK --> BEAST["BEAST2 / MCMCtree"]
  PRIOR --> BEAST
  BEAST --> CHRONO["Time-calibrated tree (chronogram)"]
```

**BEAST2** and **MCMCtree** are standard. A **tree prior** (Yule or birth–death for
species; coalescent for populations) models how lineages accumulate, the topic of
the next lesson.

**Next:** when gene trees disagree with the species tree.
""",
        ),
        _t(
            "Multispecies coalescent and gene-tree discordance",
            "12 min",
            r"""
# Multispecies coalescent and gene-tree discordance

Concatenating all genes into one "supermatrix" assumes every gene shares one
history. They often do not. **Incomplete lineage sorting (ILS)** — ancestral
polymorphism that fails to sort before the next speciation — makes individual
**gene trees** disagree with the true **species tree**, especially after rapid
radiations with short internal branches.

The **multispecies coalescent (MSC)** models this by embedding coalescent
population genetics inside the species tree: the probability that lineages fail to
coalesce within a branch depends on its length in **coalescent units**
($t/2N_e$). The most probable gene tree can even differ from the species tree (the
**anomaly zone**) when internal branches are very short.

```mermaid
flowchart TB
  ST["Species tree (population branches)"] --> COAL["Coalescent within branches"]
  COAL --> G1["gene tree 1"]
  COAL --> G2["gene tree 2 (discordant)"]
  COAL --> G3["gene tree 3"]
  G1 --> SUM["Summary species-tree method"]
  G2 --> SUM
  G3 --> SUM
  SUM --> EST["Estimated species tree (ASTRAL)"]
```

**Summary methods** like **ASTRAL** estimate the species tree that agrees with the
most quartets across many gene trees — statistically consistent under the MSC.
Full-likelihood/Bayesian MSC methods (**BPP**, **\*BEAST**) co-estimate gene trees
and the species tree but scale to fewer taxa. ILS also confounds **introgression**;
distinguishing them (e.g. the ABBA-BABA / D-statistic) is an active field.

**Next:** scaling inference to whole genomes.
""",
        ),
        _t(
            "Phylogenomics at genome scale",
            "11 min",
            r"""
# Phylogenomics at genome scale

**Phylogenomics** infers trees from genome-scale data — hundreds to thousands of
loci. More data shrinks *sampling* error, but **systematic** error grows: model
misspecification produces **strongly supported wrong trees**. Bootstrap values
near 100% are routine and no longer informative; the challenge shifts to **bias**.

Key pathologies and remedies:

- **Compositional heterogeneity** (GC bias across lineages) violates stationarity →
  use non-stationary models or recode amino acids (Dayhoff-6).
- **Heterotachy** (rates that shift over time) → covarion or partitioned models.
- **LBA** amplified by long branches → dense taxon sampling, site-heterogeneous
  mixture models (**CAT** in PhyloBayes), removing fast-evolving sites.
- **Orthology/contamination errors** → strict ortholog filtering and gene-tree
  outlier removal.

```mermaid
flowchart LR
  GEN["Genomes / transcriptomes"] --> ORTHO["Ortholog inference"]
  ORTHO --> ALN["Per-gene MSA + trimming"]
  ALN --> GTREE["Gene trees"]
  GTREE --> CONCAT["Concatenation (partitioned ML)"]
  GTREE --> COAL["Coalescent (ASTRAL)"]
  CONCAT --> CMP["Compare + assess conflict"]
  COAL --> CMP
```

Best practice runs **both** concatenation and coalescent analyses and quantifies
gene-wise conflict (gene/site concordance factors in IQ-TREE). Agreement raises
confidence; conflict flags biology (ILS, introgression) or artefact — not a number
to be smoothed over.

**Next:** detecting natural selection from sequences.
""",
        ),
        _t(
            "Detecting selection with dN/dS",
            "11 min",
            r"""
# Detecting selection with dN/dS

Phylogenies let us read the *mode* of selection acting on protein-coding genes by
comparing two substitution rates: **dN**, nonsynonymous (amino-acid-changing)
substitutions per nonsynonymous site, and **dS**, synonymous (silent) per
synonymous site. Their ratio $\omega = dN/dS$ has a clear interpretation:

- $\omega < 1$ — **purifying (negative) selection**, the common case (most amino
  acids are constrained).
- $\omega = 1$ — neutral evolution at the protein level.
- $\omega > 1$ — **positive (diversifying) selection**, the signature of adaptation
  (immune genes, host–pathogen arms races).

```plot
{"title": "Interpreting the dN/dS ratio omega", "xLabel": "omega = dN/dS", "yLabel": "relative log-likelihood under positive selection", "xRange": [0, 3], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-1)*4))", "label": "evidence for positive selection", "color": "#dc2626"}]}
```

Averaging $\omega$ over a whole gene and all branches usually hides selection,
which is episodic and site-specific. **Codon models** in **PAML (codeml)** and
**HyPhy** allow $\omega$ to vary among **sites** (M1a/M2a, M7/M8), among
**branches** (branch models), or both (**branch-site** tests), using likelihood-
ratio tests to detect positively selected lineages or residues.

```mermaid
flowchart LR
  ALN["Codon alignment + tree"] --> NULL["Null model (no omega>1)"]
  ALN --> ALT["Alt model (allows omega>1)"]
  NULL --> LRT["Likelihood-ratio test"]
  ALT --> LRT
  LRT --> SEL["Positively selected sites/branches"]
```

**Next:** machine learning for phylogenetic inference.
""",
        ),
        _t(
            "Machine learning for phylogenetics",
            "11 min",
            r"""
# Machine learning for phylogenetics

Likelihood and Bayesian inference are accurate but expensive, and they require an
explicit model. A fast-growing alternative uses **machine learning** to *learn* the
mapping from alignments to trees or parameters. The training data are millions of
**simulated** alignments with known trees, so the model learns the inverse problem
directly.

Three influential directions:

- **Likelihood-free / simulation-based inference** — train a classifier or neural
  network to pick among candidate topologies or to estimate parameters, sidestepping
  the integral. Convolutional networks read the alignment matrix as an image.
- **Model selection by ML** — tools like **ModelTeller** predict the best
  substitution model far faster than fitting them all.
- **Amortized inference & embeddings** — graph and transformer networks embed
  sequences and propose trees, or guide MCMC proposals to speed convergence.

```mermaid
flowchart LR
  SIM["Simulate alignments (known trees)"] --> TRAIN["Train neural net"]
  TRAIN --> NET["Learned inference model"]
  REAL["Real alignment"] --> NET
  NET --> OUT["Topology / parameters / proposal"]
  OUT --> CHECK["Validate vs ML/Bayesian"]
```

Performance improves as training-set realism rises; networks shine in the
**LBA-prone** and saturated regimes where parsimony fails.

```plot
{"title": "Classifier accuracy vs amount of phylogenetic signal", "xLabel": "internal branch length (signal)", "yLabel": "topology accuracy", "xRange": [0, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-2)*1.5))", "label": "learned-model accuracy", "color": "#16a34a"}]}
```

The field treats these as *complements*: ML for speed and screening, model-based
inference for rigorously calibrated uncertainty. Careful **out-of-distribution**
checks are mandatory, since a net trained on one model class can fail silently on
real data that violate it.

**Next:** the final assessment of the advanced course.
""",
        ),
        _quiz(),
    ),
)


PHYLOGENETICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PHYLOGENETICS_COURSES"]
