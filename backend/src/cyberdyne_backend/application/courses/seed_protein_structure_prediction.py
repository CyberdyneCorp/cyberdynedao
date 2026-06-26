"""Protein Structure Prediction track: Basics -> Intermediate -> Advanced.

A university-level path from sequence, homology modeling and threading, through
coevolution and contact prediction, to AlphaFold/RoseTTAFold and model quality
assessment. Lessons use interactive ```plot blocks for quantitative
relationships (energy landscapes, accuracy vs identity, error metrics) and
```mermaid diagrams for pipelines, classifications and data flows.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Protein Structure Prediction -- Basics -----------------------------------

_BASICS = SeedCourse(
    slug="protein-structure-prediction-basics",
    title="Protein Structure Prediction — Basics",
    description=(
        "How a one-dimensional amino-acid sequence specifies a three-dimensional "
        "fold: the levels of protein structure, the folding problem, the "
        "energy landscape, and the experimental methods that give us the "
        "structures we learn from. Then the first computational idea that "
        "works — homology (comparative) modeling — explained with interactive "
        "plots and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "From sequence to structure: the folding problem",
            "11 min",
            r"""
# From sequence to structure: the folding problem

A protein is a linear polymer of amino acids, but its biological function comes
from the compact three-dimensional **fold** it adopts. **Anfinsen's
experiment** (1961) showed that ribonuclease A refolds spontaneously to its
native state after denaturation, supporting the **thermodynamic hypothesis**:
for many proteins the native structure is the global minimum of free energy and
is encoded entirely in the sequence.

The hard part is that the conformational space is astronomically large.
**Levinthal's paradox** notes that random search over all backbone angles would
take longer than the age of the universe, yet folding happens in microseconds to
seconds. Proteins fold fast because the landscape is **funnel-shaped**: many
high-energy unfolded states collapse toward a narrow native basin.

```mermaid
flowchart LR
  SEQ["Sequence (1D)"] --> PHYS["Physics: H-bonds, hydrophobic effect, van der Waals"]
  PHYS --> FOLD["Folding"]
  FOLD --> NAT["Native fold (3D)"]
  NAT --> FUNC["Function"]
```

We can picture free energy decreasing as the chain becomes more native-like:

```plot
{"title": "Folding funnel (energy vs nativeness)", "xLabel": "fraction native contacts", "yLabel": "free energy", "xRange": [0, 1], "yRange": [0, 10], "grid": true, "functions": [{"expr": "10*exp(-3*x)", "label": "free energy", "color": "#2563eb"}]}
```

**Next:** the four levels of protein structure.
""",
        ),
        _t(
            "The four levels of protein structure",
            "11 min",
            r"""
# The four levels of protein structure

Protein architecture is described at four levels. **Primary structure** is the
amino-acid sequence, linked by peptide bonds. **Secondary structure** is local
backbone hydrogen bonding that forms **α-helices** and **β-sheets**;
**tertiary structure** is the full 3D arrangement of one chain; **quaternary
structure** is the assembly of multiple chains into a complex.

The peptide backbone has two main rotatable dihedral angles per residue,
$\phi$ and $\psi$. Steric clashes forbid most combinations, so observed angles
cluster in allowed regions of the **Ramachandran plot** — one region for
right-handed helices, another for β-strands.

```mermaid
flowchart TB
  P["Primary: sequence"] --> S["Secondary: helices & sheets"]
  S --> T["Tertiary: one folded chain"]
  T --> Q["Quaternary: multi-chain complex"]
```

Secondary-structure content correlates with stability. As an illustration, a
helix-stabilising trend can be sketched as a saturating curve of helix fraction
versus a favourable interaction strength:

```plot
{"title": "Helix fraction vs stabilising interaction", "xLabel": "interaction strength", "yLabel": "helix fraction", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "helix fraction", "color": "#16a34a"}]}
```

**Next:** the forces that drive folding.
""",
        ),
        _t(
            "Forces that stabilise the fold",
            "10 min",
            r"""
# Forces that stabilise the fold

Folding is governed by a balance of weak interactions. The dominant driving
force in water is the **hydrophobic effect**: nonpolar side chains bury
themselves in the core to minimise the ordering of surrounding water, increasing
entropy of the system overall. Around this core, **hydrogen bonds** (especially
in secondary structure), **van der Waals** contacts, and **electrostatic
(salt-bridge)** interactions fine-tune the structure.

The net stability is a small difference between large opposing terms,
$\Delta G_{fold} = \Delta H - T\Delta S$, typically only 5–15 kcal/mol — about
the energy of a few hydrogen bonds. This marginal stability lets proteins be
both stable and flexible.

```mermaid
flowchart LR
  HYD["Hydrophobic effect"] --> STAB["Net stability"]
  HB["Hydrogen bonds"] --> STAB
  VDW["van der Waals"] --> STAB
  ELEC["Salt bridges"] --> STAB
  STAB --> NATIVE["Marginally stable native fold"]
```

Thermal denaturation often follows a sharp two-state (folded/unfolded)
transition. The folded fraction versus temperature looks sigmoidal, with a
midpoint melting temperature $T_m$:

```plot
{"title": "Two-state thermal denaturation", "xLabel": "temperature (arb.)", "yLabel": "fraction unfolded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fraction unfolded", "color": "#dc2626"}]}
```

**Next:** how structures are measured experimentally.
""",
        ),
        _t(
            "How experimental structures are determined",
            "11 min",
            r"""
# How experimental structures are determined

Prediction methods are trained and validated against experimentally solved
structures, almost all deposited in the **Protein Data Bank (PDB)**. Three
techniques dominate. **X-ray crystallography** diffracts X-rays through a protein
crystal and reconstructs an electron-density map; resolution (in ångström) sets
how much detail is visible. **Nuclear magnetic resonance (NMR)** measures
distance and angle restraints in solution, ideal for small, flexible proteins.
**Cryo-electron microscopy (cryo-EM)** images frozen single particles and has
recently reached near-atomic resolution for large complexes.

```mermaid
flowchart LR
  PROT["Purified protein"] --> XRAY["X-ray crystallography"]
  PROT --> NMR["Solution NMR"]
  PROT --> CRYO["Cryo-EM"]
  XRAY --> PDB["PDB deposition"]
  NMR --> PDB
  CRYO --> PDB
```

Crystallography quality is summarised by the **R-factor** and **R-free**; lower
resolution numbers mean sharper maps. The information content rises steeply as
resolution improves, which we can sketch as a decaying curve of ambiguity versus
resolution value:

```plot
{"title": "Map ambiguity vs resolution", "xLabel": "resolution (Å)", "yLabel": "model ambiguity", "xRange": [1, 6], "yRange": [0, 10], "grid": true, "functions": [{"expr": "exp(0.5*x)", "label": "ambiguity", "color": "#dc2626"}]}
```

**Next:** the central idea of homology modeling.
""",
        ),
        _t(
            "Homology modeling: structure follows sequence",
            "12 min",
            r"""
# Homology modeling: structure follows sequence

When two proteins share a common ancestor (are **homologous**), their 3D
structures are far more conserved than their sequences. This is the foundation of
**homology (comparative) modeling**: if a **query** sequence is similar enough to
a protein of known structure (a **template**), we can copy the template's fold
and thread the query onto it.

The standard pipeline is: (1) find templates by sequence search, (2) align query
to template, (3) build the backbone from aligned regions, (4) model loops and
side chains, (5) refine and assess. Tools such as **MODELLER** and **SWISS-MODEL**
implement this.

```mermaid
flowchart LR
  QUERY["Query sequence"] --> SEARCH["Template search"]
  SEARCH --> ALIGN["Query-template alignment"]
  ALIGN --> BUILD["Backbone from template"]
  BUILD --> LOOPS["Loop & side-chain modeling"]
  LOOPS --> REFINE["Refine & assess"]
```

Model accuracy depends strongly on **sequence identity** to the template.
Above ~50% identity models are excellent; the **twilight zone** below ~25–30%
is unreliable. Backbone error (RMSD) rises sharply as identity falls:

```plot
{"title": "Model error vs template identity", "xLabel": "sequence identity (%)", "yLabel": "expected RMSD (Å)", "xRange": [10, 90], "yRange": [0, 10], "grid": true, "functions": [{"expr": "20*exp(-0.05*x)", "label": "RMSD", "color": "#2563eb"}]}
```

**Next:** what to do when no template is detectable.
""",
        ),
        _t(
            "When homology fails: the de novo problem",
            "10 min",
            r"""
# When homology fails: the de novo problem

Homology modeling works only when a usable template exists. For many sequences —
novel folds, fast-evolving proteins, the **twilight zone** — sequence search
finds nothing reliable. These cases require **template-free** (de novo / ab
initio) prediction, which must search conformational space guided by an energy
function rather than copying a known fold.

Classic approaches like **Rosetta** assemble short backbone **fragments** drawn
from the PDB and use Monte Carlo sampling plus a physics- and statistics-based
scoring function to find low-energy conformations. This is computationally
expensive and historically limited to small proteins, motivating the
coevolution and deep-learning ideas in later courses.

```mermaid
flowchart TB
  SEQ["Sequence, no template"] --> FRAG["Fragment libraries"]
  FRAG --> MC["Monte Carlo sampling"]
  MC --> SCORE["Energy scoring"]
  SCORE --> DECOY["Decoy structures"]
  DECOY --> SELECT["Select lowest energy"]
```

Sampling many random starts produces a distribution of model qualities; the best
of N samples improves with more sampling but with diminishing returns:

```plot
{"title": "Best model quality vs sampling effort", "xLabel": "samples (x100)", "yLabel": "fraction near-native", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "near-native fraction", "color": "#16a34a"}]}
```

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Protein Structure Prediction -- Intermediate -----------------------------

_INTERMEDIATE = SeedCourse(
    slug="protein-structure-prediction-intermediate",
    title="Protein Structure Prediction — Intermediate",
    description=(
        "The quantitative core: multiple sequence alignments and profiles, "
        "fold recognition by threading, secondary-structure and contact "
        "prediction, the breakthrough of evolutionary coupling analysis, and "
        "how predicted contacts fold a protein. Interactive plots and diagrams "
        "make the statistics and pipelines concrete."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Multiple sequence alignments and profiles",
            "12 min",
            r"""
# Multiple sequence alignments and profiles

The single most informative input for modern prediction is a **multiple
sequence alignment (MSA)** of the query with its evolutionary relatives.
Aligning many homologs reveals which positions are conserved (functionally or
structurally important) and which vary. Tools like **HHblits** and **jackhmmer**
search large databases (UniRef, BFD) iteratively to gather **deep** MSAs.

From an MSA we build a **profile**: a position-specific scoring matrix (**PSSM**)
giving the probability of each amino acid at each column. Position-specific
profiles detect remote homologs far better than a single sequence, which powers
**PSI-BLAST** and profile-HMM methods (**HMMER**, **HHpred**).

```mermaid
flowchart LR
  QUERY["Query sequence"] --> SEARCH["Iterative DB search"]
  SEARCH --> MSA["Deep MSA"]
  MSA --> PROFILE["Profile / PSSM / HMM"]
  PROFILE --> SENS["Sensitive remote-homolog detection"]
```

Conservation at a column is quantified by **information content** in bits,
$IC = \log_2 20 - H$, where $H = -\sum_a p_a \log_2 p_a$ is the entropy. A fully
conserved column carries ~4.3 bits; a random column carries ~0. Detection power
grows with the number of effective sequences in the MSA, saturating:

```plot
{"title": "Detection power vs MSA depth", "xLabel": "effective sequences (x100)", "yLabel": "remote-homolog recall", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1.5)", "label": "recall", "color": "#2563eb"}]}
```

**Next:** recognising folds by threading.
""",
        ),
        _t(
            "Fold recognition by threading",
            "11 min",
            r"""
# Fold recognition by threading

When sequence similarity is too low for homology modeling, **threading** (fold
recognition) asks a different question: which known fold best accommodates this
sequence? The query is **threaded** onto each template fold and scored with
**knowledge-based statistical potentials** that capture how well each residue
fits its predicted environment (buried/exposed, secondary structure, contacts).

The score combines a **mean-force potential** derived from observed
residue-residue contact frequencies in the PDB (via the **inverse Boltzmann**
relation) with sequence-profile and secondary-structure agreement. Methods such
as **I-TASSER**, **RaptorX** and **Phyre2** rank templates and build full models.

```mermaid
flowchart LR
  QUERY["Query (no clear homolog)"] --> LIB["Fold library (templates)"]
  LIB --> THREAD["Thread query onto each fold"]
  THREAD --> POT["Statistical potential scoring"]
  POT --> RANK["Rank folds"]
  RANK --> MODEL["Build best model"]
```

The inverse Boltzmann relation turns observed frequencies into pseudo-energies:
$E(r) = -kT \ln\!\left(\frac{p_{obs}(r)}{p_{ref}(r)}\right)$. Pairs observed more
often than a reference state get favourable (negative) energy. Contact
preference falls off with distance, which we can sketch as an exponential decay:

```plot
{"title": "Contact potential vs residue separation", "xLabel": "distance (Å)", "yLabel": "interaction energy (arb.)", "xRange": [3, 12], "yRange": [0, 10], "grid": true, "functions": [{"expr": "10*exp(-0.4*x)", "label": "favourability", "color": "#16a34a"}]}
```

**Next:** predicting secondary structure.
""",
        ),
        _t(
            "Secondary-structure and solvent prediction",
            "11 min",
            r"""
# Secondary-structure and solvent prediction

Predicting per-residue **secondary structure** (helix H, strand E, coil C) and
**solvent accessibility** is a classic intermediate task and a useful feature for
full 3D prediction. Early methods (Chou-Fasman, GOR) used amino-acid
propensities; the leap came with **profile-based neural networks** — **PSIPRED**
fed a PSI-BLAST profile into a network and reached ~80% three-state accuracy
(**Q3**).

The reason profiles help: conservation patterns reflect structural constraints
that a single sequence hides. Modern predictors use deep networks and report Q3
or the more granular eight-state Q8 accuracy.

```mermaid
flowchart LR
  MSA["MSA / profile"] --> FEAT["Per-position features"]
  FEAT --> NN["Neural network"]
  NN --> SS["H / E / C per residue"]
  NN --> ACC["Solvent accessibility"]
```

Accuracy improves with profile depth but plateaus near the ~88% theoretical
ceiling set by disagreement among experimental assignment methods (DSSP vs
STRIDE). The accuracy-vs-information curve is saturating:

```plot
{"title": "Q3 accuracy vs profile information", "xLabel": "profile information (arb.)", "yLabel": "Q3 accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.9*x/(x+1)", "label": "Q3", "color": "#2563eb"}]}
```

**Next:** the coevolution breakthrough.
""",
        ),
        _t(
            "Coevolution and evolutionary couplings",
            "12 min",
            r"""
# Coevolution and evolutionary couplings

A pair of residues that contact each other in 3D tends to **coevolve**: a
mutation in one is compensated by a mutation in the other, so the columns are
statistically correlated across the MSA. Detecting these correlations lets us
predict spatial contacts from sequence alone — the key idea behind the
2010s revolution in prediction.

Naive correlation (mutual information) is confounded by **indirect** (transitive)
couplings: if A contacts B and B contacts C, A and C appear correlated. **Direct
coupling analysis (DCA)** solves this with a global statistical model (a Potts /
maximum-entropy model) that separates **direct** from indirect couplings. Methods
include **EVfold**, **plmDCA**, **GREMLIN** and **CCMpred**.

```mermaid
flowchart LR
  MSA["Deep MSA"] --> COV["Column covariation"]
  COV --> DCA["Direct coupling analysis (Potts model)"]
  DCA --> DIRECT["Direct couplings"]
  DIRECT --> CONTACT["Predicted contacts"]
```

The Potts model assigns a probability to each sequence
$P(\sigma) \propto \exp\!\left(\sum_i h_i(\sigma_i) + \sum_{i<j} J_{ij}(\sigma_i,\sigma_j)\right)$;
strong couplings $J_{ij}$ flag contacts. Crucially, the signal needs many
sequences — coupling accuracy rises with the number of effective sequences per
length ($N_{eff}/L$):

```plot
{"title": "Contact precision vs Neff/L", "xLabel": "Neff / L", "yLabel": "top-L contact precision", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "precision", "color": "#16a34a"}]}
```

**Next:** turning contacts into accuracy and structures.
""",
        ),
        _t(
            "Contact and distance prediction",
            "11 min",
            r"""
# Contact and distance prediction

DCA gives noisy contacts; the next advance was to feed coevolution features into
**deep convolutional networks** that predict a full **contact map** — a residue×
residue matrix of contact probabilities. Treating the map like an image,
**RaptorX-Contact** and **DeepContact** used residual networks to dramatically
improve precision, evaluated as **top-L/n precision** on long-range pairs.

The field then moved from binary contacts to predicting full **distance
distributions** (distograms): for each residue pair, a probability over binned
distances. Richer distance restraints fold proteins far more reliably, a step
that **AlphaFold 1** pioneered and that links directly to the next course.

```mermaid
flowchart LR
  COEV["Coevolution + profile features"] --> CNN["Deep residual network"]
  CNN --> MAP["Contact / distance map"]
  MAP --> RESTR["Distance restraints"]
  RESTR --> FOLD["3D structure"]
```

A contact map is sparse: most residue pairs are far apart. The number of true
contacts grows roughly linearly with chain length, while possible pairs grow
quadratically — so precision on the **top predicted** pairs matters more than
recall. Predicted-contact yield versus model confidence is a saturating curve:

```plot
{"title": "Usable contacts vs predictor confidence", "xLabel": "confidence threshold (arb.)", "yLabel": "fraction true positives", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "true-positive fraction", "color": "#2563eb"}]}
```

**Next:** test the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# -- Protein Structure Prediction -- Advanced ---------------------------------

_ADVANCED = SeedCourse(
    slug="protein-structure-prediction-advanced",
    title="Protein Structure Prediction — Advanced",
    description=(
        "State-of-the-art end-to-end deep learning: AlphaFold2's Evoformer and "
        "structure module, RoseTTAFold's three-track design, predicted "
        "confidence (pLDDT, PAE), model quality assessment, complexes and the "
        "frontier of design and dynamics. Interactive plots and diagrams ground "
        "the architectures and metrics."
    ),
    level="Advanced",
    lessons=(
        _t(
            "AlphaFold2: end-to-end structure prediction",
            "13 min",
            r"""
# AlphaFold2: end-to-end structure prediction

**AlphaFold2 (AF2)**, which won **CASP14** in 2020, replaced the multi-stage
pipeline with an **end-to-end** neural network trained from sequence and MSA
directly to atomic coordinates. Two modules define it: the **Evoformer**, a deep
attention stack that jointly reasons over the MSA and a residue-pair
representation, and the **structure module**, which produces 3D coordinates and
iteratively refines them by **recycling** the outputs back into the network.

Key innovations include **triangle attention** on the pair representation
(enforcing geometric consistency of distances), an **invariant point attention**
in the structure module that operates in 3D frames, and end-to-end training
against the true structure with the **FAPE** (frame-aligned point error) loss.

```mermaid
flowchart LR
  SEQ["Sequence + MSA + templates"] --> EVO["Evoformer (MSA + pair)"]
  EVO --> SM["Structure module (IPA)"]
  SM --> COORD["3D coordinates"]
  COORD -->|recycle| EVO
  COORD --> CONF["Per-residue confidence (pLDDT)"]
```

CASP14 backbone accuracy (median **GDT_TS** ~92) was close to experimental,
a step change over previous CASPs. Accuracy still depends on MSA depth, rising
and then saturating as more homologs are available:

```plot
{"title": "AF2 accuracy vs MSA depth", "xLabel": "log effective sequences", "yLabel": "GDT_TS (0-1)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.95/(1+exp(-(x-3)))", "label": "GDT_TS", "color": "#2563eb"}]}
```

**Next:** RoseTTAFold's three-track architecture.
""",
        ),
        _t(
            "RoseTTAFold and the three-track idea",
            "11 min",
            r"""
# RoseTTAFold and the three-track idea

Shortly after AF2, the Baker lab released **RoseTTAFold (RF)**, built on a
**three-track** network that simultaneously processes information at three
levels: the **1D** sequence/MSA track, the **2D** residue-pair (distance) track,
and the **3D** coordinate track. Information flows between all three so that
sequence patterns, pairwise geometry, and explicit 3D structure refine one
another.

While slightly less accurate than AF2 on average, RoseTTAFold was open,
fast, and could predict **protein complexes**. Later **RoseTTAFold All-Atom**
and **RoseTTAFold Diffusion (RFdiffusion)** extended the family to ligands,
nucleic acids and de novo **protein design**.

```mermaid
flowchart TB
  T1["1D track: sequence / MSA"] <--> T2["2D track: pairwise distances"]
  T2 <--> T3["3D track: coordinates"]
  T1 <--> T3
  T3 --> OUT["Predicted structure"]
```

A practical advantage of multi-track coupling is faster convergence with fewer
refinement cycles. The accuracy gained per refinement iteration shows
diminishing returns, motivating a fixed small number of cycles:

```plot
{"title": "Accuracy gain per refinement cycle", "xLabel": "refinement cycle", "yLabel": "cumulative accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "accuracy", "color": "#16a34a"}]}
```

**Next:** how models report their own confidence.
""",
        ),
        _t(
            "Confidence metrics: pLDDT and PAE",
            "11 min",
            r"""
# Confidence metrics: pLDDT and PAE

A defining feature of AF2 is that it predicts its own reliability. **pLDDT**
(predicted Local Distance Difference Test) is a per-residue score from 0–100
estimating local accuracy: above 90 is highly accurate, 70–90 generally good,
50–70 low confidence, and below 50 often signals **intrinsic disorder** rather
than error. pLDDT is what colours the familiar AlphaFold structures.

For global/relative reliability, the **PAE** (Predicted Aligned Error) gives the
expected position error of residue *j* when the structure is aligned on residue
*i*. PAE reveals confident **domains** (low intra-domain error) and uncertain
relative **domain orientations** (high inter-domain error) — essential when
interpreting multi-domain proteins and complexes.

```mermaid
flowchart LR
  PRED["AF2 prediction"] --> PLDDT["pLDDT (per-residue local)"]
  PRED --> PAE["PAE (pairwise relative)"]
  PLDDT --> DISORDER["Flag disorder"]
  PAE --> DOMAINS["Domain confidence & orientation"]
```

Empirically, low pLDDT regions correlate strongly with disorder predictors and
with crystallographic B-factors. The relationship between pLDDT and true
accuracy is monotonic and roughly sigmoidal:

```plot
{"title": "True accuracy vs pLDDT", "xLabel": "pLDDT (x10)", "yLabel": "fraction correct", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-6)))", "label": "accuracy", "color": "#2563eb"}]}
```

**Next:** independent model quality assessment.
""",
        ),
        _t(
            "Model quality assessment (MQA)",
            "11 min",
            r"""
# Model quality assessment (MQA)

Predicted confidence is internal; independent **model quality assessment (MQA,
or EMA)** estimates accuracy of any model, including those from external tools,
against the (unknown) true structure. Methods are **single-model** (score one
structure from its physics/geometry, e.g. **ProQ3D**, **DeepAccNet**) or
**consensus** (compare across many decoys; better structures cluster together).

Standard accuracy metrics quantify agreement with a reference: **RMSD** (overall
backbone deviation, sensitive to outliers), **GDT_TS** (fraction of residues
within distance cutoffs after superposition, the CASP standard), **TM-score**
(length-normalised, 0–1, >0.5 means same fold), and **lDDT** (superposition-free,
local). CASP runs blind, so MQA is what lets you pick a model without the answer.

```mermaid
flowchart LR
  MODEL["Candidate model"] --> SINGLE["Single-model MQA"]
  POOL["Decoy pool"] --> CONS["Consensus MQA"]
  SINGLE --> EST["Estimated quality"]
  CONS --> EST
  EST --> SELECT["Select best model"]
```

TM-score's length normalisation makes it robust: a random pair of structures
scores near 0.17 regardless of size, and the >0.5 threshold reliably separates
same-fold from different-fold. Score versus structural overlap is sigmoidal:

```plot
{"title": "TM-score vs structural overlap", "xLabel": "fraction well-aligned residues (x10)", "yLabel": "TM-score", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "TM-score", "color": "#16a34a"}]}
```

**Next:** complexes, design and dynamics.
""",
        ),
        _t(
            "Complexes, design and the frontier",
            "12 min",
            r"""
# Complexes, design and the frontier

Single-chain prediction is largely solved; the frontier is interactions and
function. **AlphaFold-Multimer** and the three-track RoseTTAFold predict
**protein-protein complexes**, scored with interface metrics such as **ipTM**
and **DockQ**. **AlphaFold3** (2024) and RoseTTAFold All-Atom extend prediction
to **ligands, nucleic acids, ions and modifications**, using diffusion-style
generative decoders.

Prediction also enabled **de novo design**: **RFdiffusion** generates novel
backbones by denoising, and **ProteinMPNN** designs sequences that fold to a
target backbone, now experimentally validated for binders and enzymes. Open
questions remain: **conformational dynamics** and alternative states, **mutation
effects** (single structures miss subtle ΔΔG), and **orphan** sequences with
shallow MSAs where **protein language models** (ESMFold, OmegaFold) predict
structure from a single sequence.

```mermaid
flowchart TB
  PRED["Modern predictors"] --> CPLX["Complexes (ipTM, DockQ)"]
  PRED --> AA["All-atom: ligands, RNA/DNA"]
  PRED --> DESIGN["Design: RFdiffusion + ProteinMPNN"]
  PRED --> LM["Language models (ESMFold)"]
  LM --> ORPHAN["Orphan / shallow-MSA proteins"]
```

Language-model predictors trade some accuracy for speed and MSA-independence;
their accuracy versus model scale keeps rising but with diminishing returns:

```plot
{"title": "ESM accuracy vs model scale", "xLabel": "log parameters", "yLabel": "structure accuracy (0-1)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.9*x/(x+2)", "label": "accuracy", "color": "#dc2626"}]}
```

**Next:** the final assessment.
""",
        ),
        _quiz(),
    ),
)


PROTEIN_STRUCTURE_PREDICTION_COURSES: tuple[SeedCourse, ...] = (
    _BASICS,
    _INTERMEDIATE,
    _ADVANCED,
)
__all__ = ["PROTEIN_STRUCTURE_PREDICTION_COURSES"]
