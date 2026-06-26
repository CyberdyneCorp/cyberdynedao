"""Systems & Network Biology track: Basics -> Intermediate -> Advanced.

A university-level systems-biology curriculum: from biological networks,
pathways and recurring circuit motifs, through dynamical (ODE) and
constraint-based (flux-balance) modelling, to multi-omics integration,
single-cell inference and emergent collective behaviour. Lessons use
interactive ```plot blocks for quantitative relationships (kinetics, dose
response, flux cones, network degree distributions) and ```mermaid diagrams
for pathways, motifs, classifications and analysis pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Systems & Network Biology -- Basics --------------------------------------

_BASICS = SeedCourse(
    slug="systems-biology-basics",
    title="Systems & Network Biology — Basics",
    description=(
        "Why the whole is more than the parts. The intuition behind systems "
        "biology: representing cells as networks of genes, proteins and "
        "metabolites; reading pathways; recognising recurring wiring patterns "
        "(network motifs); and seeing how feedback produces behaviour no single "
        "molecule has. Built on real molecular detail with interactive plots and "
        "network diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is systems biology?",
            "10 min",
            r"""
# What is systems biology?

**Systems biology** studies how the components of a living cell — genes,
proteins, metabolites — interact as a *network* to produce behaviour that no
single molecule has on its own. Classical molecular biology is *reductionist*:
isolate one gene, one enzyme, one reaction. Systems biology is *integrative*: it
asks how thousands of those parts, wired together, generate **emergent**
properties like robustness, oscillation, switching and adaptation.

The workflow is a loop: measure many components at once (omics), build a
**mathematical model** of their interactions, simulate it, compare predictions
to data, then refine. The cell is treated as an information-processing and
chemical-processing system whose dynamics we can write down and analyse.

```mermaid
flowchart LR
  DATA["Omics measurements"] --> MODEL["Network / math model"]
  MODEL --> SIM["Simulation & analysis"]
  SIM --> PRED["Predictions"]
  PRED --> EXP["New experiments"]
  EXP --> DATA
```

Emergence is concrete: two genes that mutually repress each other form a
**toggle switch** that is bistable — a property neither gene has alone. A simple
saturating response of one component to another already shows the nonlinearity
that makes such behaviour possible:

```plot
{"title": "Saturating molecular response (building block of emergence)", "xLabel": "input signal", "yLabel": "response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating response", "color": "#2563eb"}]}
```

**Next:** how to draw the cell as a network.
""",
        ),
        _t(
            "Biological networks and graphs",
            "11 min",
            r"""
# Biological networks and graphs

A cell's interactions are naturally a **graph**: **nodes** are molecules,
**edges** are interactions. Several network types matter. **Protein–protein
interaction (PPI)** networks (databases like STRING, BioGRID) have undirected
edges. **Gene regulatory networks (GRNs)** are directed: a transcription factor
activates or represses a target. **Metabolic networks** connect metabolites
through enzyme-catalysed reactions. **Signalling networks** carry directed
information from receptors to effectors.

Graph metrics summarise structure. A node's **degree** is its number of edges;
**hubs** are high-degree nodes, often essential. The **clustering coefficient**
measures how interconnected a node's neighbours are. Many biological networks
are **scale-free**: their degree distribution follows a power law
$P(k) \sim k^{-\gamma}$, so most nodes have few links and a few hubs have many.

```mermaid
flowchart LR
  TF["Transcription factor"] -->|activates| G1["Gene A"]
  TF -->|represses| G2["Gene B"]
  G1 --> P1["Protein A"]
  P1 -.interacts.- P2["Protein B"]
```

The hallmark power-law degree distribution falls off steeply, so hubs are rare
but dominant:

```plot
{"title": "Scale-free degree distribution P(k) ~ k^-2.2", "xLabel": "degree k", "yLabel": "P(k)", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(x^2.2)", "label": "P(k)", "color": "#dc2626"}]}
```

**Next:** following information along pathways.
""",
        ),
        _t(
            "Pathways: metabolism, signalling and regulation",
            "11 min",
            r"""
# Pathways: metabolism, signalling and regulation

A **pathway** is a curated chain of reactions or interactions achieving a
function. **Metabolic pathways** (glycolysis, the TCA cycle) convert substrates
to products through ordered enzyme steps, channelling matter and energy.
**Signalling pathways** (the MAPK cascade, PI3K/AKT) transmit a signal from a
membrane receptor to the nucleus, often *amplifying* it through successive
phosphorylations. **Regulatory pathways** control gene expression in response.

Pathways are not isolated lines; they branch and cross-talk, forming the network
of the previous lesson. Curated resources — **KEGG**, **Reactome**, **WikiPathways**
— encode them in machine-readable form so they can be analysed and modelled.

```mermaid
flowchart LR
  R["Receptor"] --> RAS["RAS"]
  RAS --> RAF["RAF"]
  RAF --> MEK["MEK"]
  MEK --> ERK["ERK"]
  ERK --> TF["Gene expression"]
```

A multi-step cascade amplifies and *sharpens* the response: the output becomes a
steep, switch-like function of the stimulus rather than a gentle line:

```plot
{"title": "Signalling cascade sharpens the dose response", "xLabel": "stimulus", "yLabel": "active output", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "sigmoidal output", "color": "#16a34a"}]}
```

**Next:** the recurring wiring patterns inside these networks.
""",
        ),
        _t(
            "Network motifs",
            "11 min",
            r"""
# Network motifs

Uri Alon and colleagues found that real networks are built from a small set of
recurring sub-circuits — **network motifs** — that appear far more often than in
random graphs and perform identifiable computations.

The most studied is the **feed-forward loop (FFL)**: X regulates Y, and both X
and Y regulate Z. In the **coherent type-1 FFL** with an AND gate at Z, Z turns
on only after a *persistent* input — a **sign-sensitive delay** that filters out
brief noise pulses. The **incoherent FFL** produces a *pulse* then adapts. Other
motifs include **negative autoregulation** (a gene repressing itself, which
speeds response and reduces noise) and the **single-input module** that
coordinates many genes.

```mermaid
flowchart LR
  X["X"] --> Y["Y"]
  X --> Z["Z"]
  Y --> Z
```

Negative autoregulation makes a gene reach steady state faster than simple
(unregulated) accumulation, which approaches its plateau slowly:

```plot
{"title": "Negative autoregulation speeds the response", "xLabel": "time", "yLabel": "protein level", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "simple accumulation", "color": "#2563eb"}, {"expr": "1-exp(-1.2*x)", "label": "with neg. autoreg.", "color": "#dc2626"}]}
```

**Next:** the kinetics that make a single edge quantitative.
""",
        ),
        _t(
            "Enzyme kinetics and dose response",
            "11 min",
            r"""
# Enzyme kinetics and dose response

To make a network quantitative we need rate laws for its edges. The
**Michaelis–Menten** equation describes an enzyme converting substrate S to
product at rate
$$v = \frac{V_{max}\,[S]}{K_m + [S]}$$
where $V_{max}$ is the maximum rate and $K_m$ is the substrate concentration at
half-maximal rate — a measure of affinity. At low $[S]$ the rate is roughly
linear in $[S]$; at high $[S]$ it saturates at $V_{max}$.

Cooperative binding (e.g. a transcription factor binding as a dimer, or
haemoglobin binding oxygen) gives a steeper **Hill** response,
$\theta = \frac{[S]^n}{K^n + [S]^n}$, where the **Hill coefficient** $n$ sets the
sharpness. $n>1$ produces the switch-like dose response that builds toggles and
oscillators.

```mermaid
flowchart LR
  E["Enzyme E"] --> ES["E·S complex"]
  S["Substrate S"] --> ES
  ES --> P["Product P"]
  ES --> E
```

The Michaelis–Menten curve rises then saturates toward $V_{max}$:

```plot
{"title": "Michaelis-Menten kinetics (Vmax=8, Km=2)", "xLabel": "substrate [S]", "yLabel": "rate v", "xRange": [0, 20], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

**Next:** how feedback turns kinetics into dynamic behaviour.
""",
        ),
        _t(
            "Feedback, robustness and homeostasis",
            "10 min",
            r"""
# Feedback, robustness and homeostasis

Feedback closes a network on itself. **Negative feedback** — an output that
suppresses its own production — drives **homeostasis** and stability; the
classic example is bacterial **chemotaxis**, which achieves *exact adaptation*:
the cell returns to its baseline tumbling rate regardless of the absolute
attractant level, sensing only changes. **Positive feedback** — an output that
boosts its own production — creates amplification and **bistability** (memory,
all-or-none decisions like cell-cycle commitment).

**Robustness** is a system-level property: the phenotype is insensitive to
parameter or environmental variation. It arises from network structure
(redundancy, feedback, modularity), not from any single molecule, and is a
recurring theme of systems biology.

```mermaid
flowchart LR
  STIM["Stimulus"] --> OUT["Output"]
  OUT -->|negative feedback| OUT
  OUT --> RESP["Adapted response"]
```

After a step stimulus, an adaptive (negative-feedback) circuit spikes then
relaxes back toward baseline — the signature of homeostatic control:

```plot
{"title": "Adaptation: response relaxes back to baseline", "xLabel": "time after step", "yLabel": "output", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "adapting response", "color": "#16a34a"}]}
```

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Systems & Network Biology -- Intermediate --------------------------------

_INTERMEDIATE = SeedCourse(
    slug="systems-biology-intermediate",
    title="Systems & Network Biology — Intermediate",
    description=(
        "The quantitative core. Turning networks into equations: ordinary "
        "differential equation (ODE) models and the law of mass action; "
        "stability, bifurcations and oscillators; stochastic gene expression; "
        "and constraint-based metabolic modelling with flux-balance analysis. "
        "Hands-on with rate laws, phase behaviour and the stoichiometric matrix."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "ODE models and mass action",
            "12 min",
            r"""
# ODE models and mass action

The workhorse of dynamical systems biology is a system of **ordinary
differential equations (ODEs)**: each species' concentration changes at a rate
set by the reactions that make and consume it. The **law of mass action** says a
reaction's rate is proportional to the product of reactant concentrations. For
$A + B \rightarrow C$ with rate constant $k$, the production of C is
$$\frac{d[C]}{dt} = k\,[A][B]$$
and A and B are consumed at the same rate.

For enzymatic and regulatory steps we substitute Michaelis–Menten or Hill
terms. Stacking these balance equations for every species gives a model we
integrate numerically (e.g. with SciPy `odeint`/`solve_ivp`, COPASI, or
Tellurium) to predict time courses.

```mermaid
flowchart LR
  A["A"] --> RXN["k: A + B -> C"]
  B["B"] --> RXN
  RXN --> C["C"]
```

A simple first-order decay $\frac{d[A]}{dt} = -k[A]$ has the closed-form
solution $[A](t) = [A]_0 e^{-kt}$:

```plot
{"title": "First-order decay [A](t) = A0 * exp(-kt), k=0.5", "xLabel": "time", "yLabel": "[A]", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "[A](t)", "color": "#2563eb"}]}
```

**Next:** finding and judging steady states.
""",
        ),
        _t(
            "Steady states and stability analysis",
            "12 min",
            r"""
# Steady states and stability analysis

A **steady state (fixed point)** is where every derivative is zero — the system
holds constant. Setting $\frac{dx}{dt}=0$ and solving gives the fixed points,
but we also need their **stability**: do small perturbations decay (stable) or
grow (unstable)?

We linearise around the fixed point and compute the **Jacobian** matrix of
partial derivatives. The signs of its **eigenvalues** decide stability: if all
eigenvalues have negative real part the state is stable; a positive real part
makes it unstable. Complex eigenvalues signal oscillatory approach. This is the
same local-linearisation logic used throughout dynamical systems.

```mermaid
flowchart LR
  ODE["dx/dt = f(x)"] --> FP["Solve f(x*)=0"]
  FP --> JAC["Jacobian J at x*"]
  JAC --> EIG["Eigenvalues of J"]
  EIG --> STAB["Stable / unstable"]
```

Near a stable fixed point a perturbation decays exponentially; near an unstable
one it grows — the two qualitatively different fates:

```plot
{"title": "Perturbation fate near a fixed point", "xLabel": "time", "yLabel": "perturbation size", "xRange": [0, 6], "yRange": [0, 6], "grid": true, "functions": [{"expr": "exp(-0.7*x)", "label": "stable (decays)", "color": "#16a34a"}, {"expr": "exp(0.5*x)", "label": "unstable (grows)", "color": "#dc2626"}]}
```

**Next:** when feedback makes the system oscillate or switch.
""",
        ),
        _t(
            "Bifurcations, switches and oscillators",
            "12 min",
            r"""
# Bifurcations, switches and oscillators

As a parameter changes, the *number or stability* of fixed points can change
qualitatively — a **bifurcation**. A **saddle-node** bifurcation creates or
destroys a pair of fixed points; combined with positive feedback it underlies
**bistable switches** (two stable states with **hysteresis**, as in the
Xenopus cell-cycle trigger). A **Hopf** bifurcation gives birth to a stable
**limit cycle** — sustained oscillations such as circadian rhythms and the
**repressilator**, a synthetic three-gene ring of repressors.

Bistability needs a sharp (cooperative, $n>1$) positive-feedback response that
intersects the degradation line at three points; oscillation needs negative
feedback with delay plus nonlinearity.

```mermaid
flowchart LR
  A["geneA"] -->|repress| B["geneB"]
  B -->|repress| C["geneC"]
  C -->|repress| A
```

A steep Hill production curve crossing a linear removal line produces the three
intersections (two stable, one unstable) that define a bistable switch:

```plot
{"title": "Bistability: sharp production vs linear removal", "xLabel": "protein level x", "yLabel": "rate", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(4/x)^4)", "label": "Hill production", "color": "#dc2626"}, {"expr": "0.1*x", "label": "linear removal", "color": "#2563eb"}]}
```

**Next:** what happens when molecule numbers are small and noisy.
""",
        ),
        _t(
            "Stochastic gene expression",
            "11 min",
            r"""
# Stochastic gene expression

When molecules are present in small numbers — a handful of mRNAs, one or two
copies of a gene — reactions are inherently **random**. Deterministic ODEs give
average behaviour but miss the cell-to-cell variability (**noise**) that this
discreteness produces. The correct description is the **chemical master
equation**, usually simulated with the **Gillespie stochastic simulation
algorithm (SSA)**, which draws random reaction times and identities exactly.

Noise is split into **intrinsic** (randomness of the gene's own reactions,
measured with a two-reporter assay) and **extrinsic** (fluctuations in shared
factors like polymerase). For a simple birth–death process the steady-state copy
number follows a **Poisson** distribution, so the **Fano factor** (variance/mean)
is 1; bursty transcription pushes it above 1.

```mermaid
flowchart LR
  GENE["Gene"] -->|bursty| MRNA["mRNA"]
  MRNA --> PROT["Protein"]
  MRNA -->|degrade| NULL["∅"]
  PROT -->|degrade| NULL
```

For a Poisson copy-number distribution the relative noise (CV) falls as
$1/\sqrt{\langle n \rangle}$ — fewer molecules, more noise:

```plot
{"title": "Poisson noise: CV = 1/sqrt(mean copy number)", "xLabel": "mean copy number", "yLabel": "coefficient of variation", "xRange": [1, 50], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "CV", "color": "#2563eb"}]}
```

**Next:** modelling metabolism without knowing every rate constant.
""",
        ),
        _t(
            "Constraint-based modelling and FBA",
            "12 min",
            r"""
# Constraint-based modelling and FBA

Genome-scale metabolic networks have thousands of reactions whose kinetic
constants are mostly unknown, so detailed ODEs are impractical. **Constraint-based
modelling** sidesteps kinetics by assuming a **steady state**: at metabolic
balance, production equals consumption for every internal metabolite, giving the
linear constraint
$$S\,v = 0$$
where $S$ is the **stoichiometric matrix** (rows = metabolites, columns =
reactions) and $v$ is the flux vector. Together with flux bounds
$v_{min} \le v \le v_{max}$, these define a **flux cone** of feasible states.

**Flux-balance analysis (FBA)** uses **linear programming** to find the flux
distribution that maximises an objective — usually **biomass production** — inside
that cone. Tools like COBRApy run FBA on reconstructions such as *E. coli*
iML1515. Variants include **FVA** (flux ranges) and **pFBA** (parsimonious flux).

```mermaid
flowchart LR
  RECON["Genome-scale reconstruction"] --> S["Stoichiometric matrix S"]
  S --> CON["S·v = 0, bounds"]
  CON --> LP["Linear program: max biomass"]
  LP --> FLUX["Optimal flux distribution"]
```

Predicted growth rate rises with nutrient uptake but saturates as another
constraint becomes limiting — a Monod-like dependence:

```plot
{"title": "FBA-predicted growth vs substrate uptake", "xLabel": "substrate uptake flux", "yLabel": "growth rate", "xRange": [0, 20], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8*x/(3+x)", "label": "growth rate", "color": "#16a34a"}]}
```

**Next:** check your understanding of the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Systems & Network Biology -- Advanced ------------------------------------

_ADVANCED = SeedCourse(
    slug="systems-biology-advanced",
    title="Systems & Network Biology — Advanced",
    description=(
        "State of the art and applied. Integrating multi-omics layers; "
        "reconstructing networks from single-cell data with machine learning; "
        "whole-cell and digital-twin modelling; design principles of synthetic "
        "circuits; and the emergent collective behaviour of cell populations. "
        "Connects modern computational and AI methods to mechanistic models."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multi-omics data integration",
            "12 min",
            r"""
# Multi-omics data integration

Modern systems biology layers **genomics, transcriptomics, proteomics,
metabolomics** and epigenomics on the same samples. Each layer is a different,
noisy view of the same underlying state, so the challenge is **integration**:
combining them into a coherent model despite differing scales, sparsity and
batch effects.

Methods span **similarity-network fusion (SNF)**, multi-omics factor analysis
(**MOFA**) that learns shared latent factors, joint dimensionality reduction
(**DIABLO**, joint NMF), and network-based fusion that maps each layer onto a
common interaction graph. The goal is to find the few latent axes of variation
that explain many measurements at once — and to link, say, a methylation change
to an expression change to a metabolite shift.

```mermaid
flowchart LR
  GEN["Genomics"] --> INT["Integration (MOFA / SNF)"]
  TRX["Transcriptomics"] --> INT
  PRO["Proteomics"] --> INT
  MET["Metabolomics"] --> INT
  INT --> FACT["Shared latent factors"]
```

A handful of latent factors typically captures most of the joint variance, so
explained variance saturates quickly with the number of factors:

```plot
{"title": "Cumulative variance explained by latent factors", "xLabel": "number of factors", "yLabel": "cumulative variance explained", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "cumulative variance", "color": "#2563eb"}]}
```

**Next:** learning network structure from single cells.
""",
        ),
        _t(
            "Single-cell network inference",
            "12 min",
            r"""
# Single-cell network inference

**Single-cell RNA-seq (scRNA-seq)** measures thousands of cells individually,
exposing heterogeneity invisible in bulk data and giving the many observations
needed to *infer* regulatory networks. **GRN inference** estimates which genes
regulate which from expression patterns. Tree-ensemble methods (**GENIE3**,
**GRNBoost2**) rank regulators by feature importance; **SCENIC** adds
motif-based pruning to keep biologically plausible edges.

Because cells lie along developmental trajectories, **pseudotime** ordering and
**RNA velocity** (using the ratio of unspliced to spliced reads to infer the
direction of change) turn a static snapshot into dynamics, enabling
**dynamic** GRN inference. Deep-learning approaches — variational autoencoders
(scVI) and graph neural networks — denoise the sparse data and learn embeddings
that improve inference.

```mermaid
flowchart LR
  SC["scRNA-seq matrix"] --> PT["Pseudotime / RNA velocity"]
  SC --> IMP["Denoise (scVI / VAE)"]
  PT --> GRN["GRN inference (SCENIC)"]
  IMP --> GRN
  GRN --> NET["Regulatory network"]
```

Inference accuracy (e.g. AUPRC against a gold standard) improves with the number
of profiled cells but plateaus once the network is well constrained:

```plot
{"title": "GRN inference accuracy vs number of cells", "xLabel": "thousands of cells", "yLabel": "AUPRC (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(2/x)^2)", "label": "AUPRC", "color": "#16a34a"}]}
```

**Next:** integrating everything into a whole-cell model.
""",
        ),
        _t(
            "Whole-cell models and digital twins",
            "12 min",
            r"""
# Whole-cell models and digital twins

A **whole-cell model** simulates *every* known molecular function of a cell at
once. The landmark 2012 model of *Mycoplasma genitalium* (Karr et al.) coupled
28 sub-models — metabolism, transcription, replication, division — each with its
own formalism (FBA for metabolism, ODEs and stochastic processes elsewhere),
synchronised every time step. It predicted phenotypes, including the effect of
single-gene knockouts, from genotype.

This **multi-scale, hybrid** approach is the basis of biological **digital
twins**: a continuously updated computational replica of a specific cell,
tissue or patient, fed by live data and used to predict interventions. Building
them requires **parameter estimation** (fitting many constants to data) and
careful **identifiability** and **uncertainty quantification**.

```mermaid
flowchart TB
  META["Metabolism (FBA)"] --> SYNC["Time-step synchronisation"]
  TXN["Transcription (stochastic)"] --> SYNC
  REP["Replication (ODE)"] --> SYNC
  DIV["Division"] --> SYNC
  SYNC --> PHEN["Predicted phenotype"]
```

Calibrating such a model reduces prediction error as more data are assimilated,
with diminishing returns — the classic error-versus-data curve:

```plot
{"title": "Model prediction error vs assimilated data", "xLabel": "data assimilated", "yLabel": "prediction error", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "prediction error", "color": "#dc2626"}]}
```

**Next:** designing circuits rather than just describing them.
""",
        ),
        _t(
            "Synthetic biology design principles",
            "12 min",
            r"""
# Synthetic biology design principles

**Synthetic biology** uses systems-biology models to *engineer* new cellular
behaviour from standardised parts (promoters, ribosome-binding sites, coding
sequences, terminators). Foundational devices include the **toggle switch**
(Gardner et al. 2000), two mutually repressing genes giving stable memory, and
the **repressilator** (Elowitz & Leibler 2000), a three-gene ring that
oscillates.

The engineering ethos is **abstraction** (parts → devices → systems),
**characterisation** in standard units, and **orthogonality** so parts do not
interfere. Real designs must respect **load and resource competition** (shared
ribosomes/RNA polymerase couple circuits) and **noise**. Model-guided design,
increasingly assisted by ML for sequence-to-function prediction, shortens the
**design–build–test–learn** cycle.

```mermaid
flowchart LR
  DESIGN["Design (model)"] --> BUILD["Build (assemble DNA)"]
  BUILD --> TEST["Test (measure)"]
  TEST --> LEARN["Learn (fit / refine)"]
  LEARN --> DESIGN
```

A repressor-based switch shows the steep, near-digital input–output transfer
function engineers exploit for reliable ON/OFF logic:

```plot
{"title": "Engineered switch transfer function (sharp threshold)", "xLabel": "input (repressor)", "yLabel": "output expression", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(x/5)^4)", "label": "repression transfer", "color": "#2563eb"}]}
```

**Next:** behaviour that emerges across whole populations.
""",
        ),
        _t(
            "Emergent and collective behaviour",
            "12 min",
            r"""
# Emergent and collective behaviour

The most striking emergent properties appear across **populations** of cells.
**Quorum sensing** lets bacteria estimate their density via a diffusible
autoinducer; when its concentration crosses a threshold the population switches
behaviour synchronously (bioluminescence in *Vibrio fischeri*, biofilm and
virulence programs). This is cell–cell **communication** producing a coordinated,
all-or-none group decision no single cell could make.

Other collective phenomena include **synchronised oscillations** (coupled
genetic clocks entraining), **pattern formation** via **Turing**
reaction–diffusion instabilities (a short-range activator with a long-range
inhibitor spontaneously breaks symmetry into spots and stripes), and
**spatial self-organisation** in development and tissues. The common thread:
local rules plus coupling yield global order — emergence again, now in space and
across many cells.

```mermaid
flowchart LR
  CELL["Cell secretes autoinducer"] --> DIFF["Diffusion / accumulation"]
  DIFF --> THR["Threshold crossed"]
  THR --> SYNC["Synchronised group response"]
```

Quorum sensing is itself a sharp, density-dependent switch — group response is
near-zero below a critical density and saturates above it:

```plot
{"title": "Quorum sensing: response vs population density", "xLabel": "cell density", "yLabel": "group response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(5/x)^6)", "label": "group response", "color": "#16a34a"}]}
```

**Next:** check your understanding of the state of the art.
""",
        ),
        _quiz(),
    ),
)


SYSTEMS_BIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["SYSTEMS_BIOLOGY_COURSES"]
