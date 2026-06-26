"""Cheminformatics track: Basics -> Intermediate -> Advanced.

A university-level path from molecular representation (SMILES, graphs,
canonicalisation) through the core quantitative methods (descriptors,
fingerprints, similarity, QSAR) to state-of-the-art applied workflows
(chemical space, clustering, RDKit pipelines and machine learning). Lessons use
interactive ```plot blocks for quantitative relationships (similarity, Lipinski
ranges, decay, dose-response) and ```mermaid diagrams for pipelines,
representations and classifications.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Cheminformatics -- Basics -------------------------------------------------

_BASICS = SeedCourse(
    slug="cheminformatics-basics",
    title="Cheminformatics — Basics",
    description=(
        "What cheminformatics is and how molecules become data: atoms and bonds "
        "as a graph, line notations such as SMILES and InChI, the importance of "
        "canonicalisation, hydrogen handling and valence, and the file formats "
        "and databases that hold chemical structures. Built on real chemical "
        "detail with interactive plots and pipeline diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is cheminformatics and why it exists",
            "10 min",
            r"""
# What is cheminformatics and why it exists

**Cheminformatics** is the science of representing, storing, searching and
analysing chemical information with computers. It emerged because chemistry
became a data discipline: vendor catalogues list millions of compounds,
high-throughput screening assays test hundreds of thousands of molecules, and
public collections such as **PubChem** and **ChEMBL** hold tens of millions of
structures with measured properties. No chemist can inspect that by hand.

The field sits at the intersection of **chemistry, computer science and
statistics**. Its central problems are: how to encode a molecule unambiguously,
how to search a database for substructures, how to measure whether two
molecules are *similar*, and how to predict properties (solubility, toxicity,
binding affinity) from structure alone — a programme known as **QSAR**
(quantitative structure–activity relationship).

A key idea is that growth in chemical data outpaces our ability to test
compounds in the lab, so computational triage becomes essential.

```mermaid
flowchart LR
  A[Molecular structure] --> B[Encoding: SMILES / graph]
  B --> C[Descriptors & fingerprints]
  C --> D[Similarity & search]
  C --> E[QSAR / ML models]
  D --> F[Hit selection]
  E --> F
```

The enumerated, *drug-like* chemical space is estimated near $10^{60}$
molecules — far too many to synthesise — so the field is fundamentally about
choosing the few worth making.

**Next:** how a molecule becomes a graph of atoms and bonds.
""",
        ),
        _t(
            "Molecules as graphs: atoms, bonds and valence",
            "11 min",
            r"""
# Molecules as graphs: atoms, bonds and valence

The dominant abstraction in cheminformatics is the **molecular graph**: atoms
are **vertices** (nodes) and bonds are **edges**. A vertex carries an element
(carbon, nitrogen…), a formal charge and often an explicit hydrogen count; an
edge carries a bond order (single, double, triple, aromatic). This 2D
*connection table* — the basis of the MDL **Molfile** format — ignores exact
geometry but captures connectivity, which is enough for most property
prediction.

Atoms obey **valence** rules: a neutral carbon makes four bonds, neutral
nitrogen three, oxygen two, hydrogen one. Cheminformatics toolkits exploit this
to infer **implicit hydrogens** so chemists need not draw every H. Total bond
order plus formal charge must be consistent with the element, otherwise the
molecule is rejected as chemically invalid during *sanitisation*.

```mermaid
flowchart LR
  C1[C] --- C2[C]
  C2 --- O[O]
  C1 --- H1[H implicit]
  C2 --- H2[H implicit]
```

Because a molecule is a graph, two seemingly different drawings can be the
**same** structure (graph isomorphism), and substructure search becomes the
**subgraph isomorphism** problem. Treating chemistry as graph theory lets us
reuse decades of algorithms for matching, traversal and hashing.

As molecules grow, the number of distinct atom environments grows roughly
linearly with atom count, which matters for how fingerprints scale.

```plot
{"title": "Atom environments vs molecule size", "xLabel": "heavy atoms", "yLabel": "distinct environments", "xRange": [0, 40], "yRange": [0, 40], "grid": true, "functions": [{"expr": "x", "label": "~linear growth", "color": "#2563eb"}]}
```

**Next:** writing molecules as text with SMILES.
""",
        ),
        _t(
            "SMILES: writing molecules as text",
            "12 min",
            r"""
# SMILES: writing molecules as text

**SMILES** (Simplified Molecular-Input Line-Entry System) encodes a molecular
graph as a compact ASCII string by walking the graph and writing atoms in
order. Organic-subset atoms (B, C, N, O, P, S, F, Cl, Br, I) need no brackets;
anything else, or any atom with a charge or non-default hydrogen count, uses
brackets like `[NH4+]` or `[O-]`.

Core syntax:

- **Atoms**: `C`, `N`, `O`; lowercase `c`, `n`, `o` mean **aromatic**.
- **Bonds**: `-` single (default), `=` double, `#` triple, `:` aromatic.
- **Branches**: parentheses, e.g. `CC(=O)O` is acetic acid.
- **Rings**: matching digits open and close a ring bond, e.g. benzene is
  `c1ccccc1`.

Worked examples: water `O`, ethanol `CCO`, carbon dioxide `O=C=O`, acetic acid
`CC(=O)O`, and caffeine `Cn1cnc2c1c(=O)n(C)c(=O)n2C`.

```mermaid
flowchart LR
  A["SMILES string 'CCO'"] --> B[Parser]
  B --> C[Molecular graph]
  C --> D[Atoms: C,C,O + implicit H]
```

SMILES is **non-unique**: ethanol is `CCO` or `OCC`. The same molecule has many
valid strings, which is why a *canonical* form is needed before strings can be
compared — the subject of the next lesson. SMILES remains the workhorse format
because it is human-readable, line-oriented and trivially stored in a database
column.

**Next:** making SMILES unique with canonicalisation.
""",
        ),
        _t(
            "Canonicalisation and structure validation",
            "11 min",
            r"""
# Canonicalisation and structure validation

Because SMILES is non-unique, comparing molecules by raw string fails — `CCO`
and `OCC` are the same ethanol. **Canonicalisation** fixes a deterministic atom
ordering so every input for a molecule yields one **canonical SMILES**. The
classic approach is the **Morgan algorithm**: assign each atom an initial
invariant (degree, element, charge), then iteratively refine by summing
neighbours' values until ranks stabilise, breaking ties consistently. Modern
toolkits (RDKit, OpenEye) use refined variants of this idea.

A second normaliser is **InChI** (IUPAC International Chemical Identifier), a
layered canonical string designed as a registry standard; its hash, the
**InChIKey**, gives a fixed-length searchable key for exact-structure lookup.

```mermaid
flowchart LR
  A[Input SMILES] --> B[Sanitise: valence, aromaticity]
  B --> C[Canonical atom ranking]
  C --> D[Canonical SMILES]
  B --> E[InChI / InChIKey]
```

**Sanitisation** runs first: it checks valences, perceives **aromaticity**
(does a ring satisfy Hückel's $4n+2$ rule?), kekulises, and computes implicit
hydrogens. Invalid structures are flagged so bad data never enters the
pipeline. Canonicalisation is what makes deduplication of a million-compound
library tractable: hash the canonical form and group identical hashes — the
collision count falls toward zero as the representation becomes truly unique.

```plot
{"title": "Duplicate collisions vs canonicalisation quality", "xLabel": "normalisation effort", "yLabel": "false duplicates", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "residual errors", "color": "#dc2626"}]}
```

**Next:** the file formats and databases that store all this.
""",
        ),
        _t(
            "Chemical file formats and databases",
            "10 min",
            r"""
# Chemical file formats and databases

Chemical structures travel between tools in standard formats. The **MDL
Molfile** (`.mol`) is a connection table listing atom coordinates and a bond
block; the **SDF** (`.sdf`) concatenates many Molfiles plus tagged property
fields, making it the standard for shipping screening libraries with data.
**SMILES** files (`.smi`) are lightweight one-line-per-molecule tables, while
**PDB** and **mol2** carry 3D coordinates for docking and modelling.

```mermaid
flowchart LR
  A[Drawing tool] --> B[".mol / .sdf"]
  B --> C[Toolkit RDKit]
  C --> D[".smi canonical"]
  D --> E[(Database)]
  E --> F[Search & retrieval]
```

Public databases anchor the field. **PubChem** (NIH) holds over 100 million
compounds with bioassay data; **ChEMBL** (EMBL-EBI) curates ~2 million
bioactive molecules with measured potencies; the **PDB** stores macromolecular
structures; **DrugBank** and **ZINC** serve drug and purchasable-compound data.
Each entry is keyed by an identifier (PubChem CID, ChEMBL ID, InChIKey) so
records can be cross-referenced.

The practical lesson: always convert incoming structures to a **canonical**
form on ingest, store the InChIKey for exact lookup, and keep a fingerprint
column for similarity — the size of these collections grows steeply year on
year.

```plot
{"title": "Public compound counts over time", "xLabel": "years", "yLabel": "relative size", "xRange": [0, 12], "yRange": [0, 30], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "database growth", "color": "#16a34a"}]}
```

**Next:** a knowledge check on representation fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Cheminformatics -- Intermediate -------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="cheminformatics-intermediate",
    title="Cheminformatics — Intermediate",
    description=(
        "The core quantitative methods: molecular descriptors and Lipinski-style "
        "drug-likeness, the major fingerprint families (MACCS, ECFP/Morgan, "
        "Daylight path), the Tanimoto and Dice similarity coefficients, "
        "substructure search and SMARTS, and the foundations of QSAR modelling. "
        "Worked equations with interactive plots and method diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Molecular descriptors and drug-likeness",
            "12 min",
            r"""
# Molecular descriptors and drug-likeness

A **molecular descriptor** is a number computed from structure that summarises a
property. Simple ones are *constitutional* — molecular weight, atom counts,
ring count. Others are *topological*, derived from the graph, such as the
**Wiener index** (sum of shortest-path lengths between all atom pairs) or
**TPSA** (topological polar surface area), a strong proxy for membrane
permeability and oral absorption.

The most famous use is **Lipinski's Rule of Five** for oral drug-likeness: a
compound tends to be poorly absorbed if it violates two or more of — molecular
weight $\le 500$, $\log P \le 5$, hydrogen-bond donors $\le 5$, and
hydrogen-bond acceptors $\le 10$. Here $\log P$ is the octanol–water partition
coefficient, a measure of lipophilicity.

```mermaid
flowchart LR
  A[Molecule] --> B[MW]
  A --> C[logP]
  A --> D[HBD / HBA]
  A --> E[TPSA]
  B & C & D --> F{Rule of Five}
  F --> G[Drug-like?]
```

Descriptors must be **interpretable and reproducible**: the same molecule, same
toolkit version, same number. They form the feature vectors fed to QSAR models.
A useful intuition is that bioavailability falls steeply once lipophilicity
($\log P$) climbs past the optimum, motivating the Rule-of-Five cut-offs.

```plot
{"title": "Oral absorption vs lipophilicity (schematic)", "xLabel": "logP", "yLabel": "relative absorption", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "absorption drop-off", "color": "#dc2626"}]}
```

**Next:** turning structure into a bit-vector fingerprint.
""",
        ),
        _t(
            "Molecular fingerprints",
            "12 min",
            r"""
# Molecular fingerprints

A **fingerprint** encodes a molecule as a fixed bit-vector so structures can be
compared by fast bitwise operations. Three families dominate:

- **Structural keys (MACCS)**: 166 predefined substructure questions ("is there
  an aromatic ring?", "a carboxyl?"); each bit is *interpretable*.
- **Path-based (Daylight)**: enumerate linear atom paths up to a length, hash
  each to set bits — a *hashed* fingerprint with no fixed meaning per bit.
- **Circular (ECFP / Morgan, FCFP)**: for each atom, hash its circular
  neighbourhood out to radius $r$ (ECFP4 means diameter 4, radius 2). These
  capture local environments and are the de-facto standard for similarity and
  machine learning.

```mermaid
flowchart LR
  A[Molecule] --> B[Enumerate substructures]
  B --> C[Hash to bit positions]
  C --> D["Bit-vector e.g. 2048 bits"]
  D --> E[Similarity / ML feature]
```

Hashing into a fixed length (commonly 1024 or 2048 bits) creates **bit
collisions** — different features landing on the same bit. Longer vectors and
*counted* fingerprints reduce this. The bit density rises with molecule size
but saturates as the vector fills.

```plot
{"title": "Fingerprint fill fraction vs molecule size", "xLabel": "feature count (scaled)", "yLabel": "fraction of bits set", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+3)", "label": "saturating fill", "color": "#2563eb"}]}
```

ECFP fingerprints power both **similarity search** and feature input to QSAR —
the topics of the next two lessons.

**Next:** measuring how similar two fingerprints are.
""",
        ),
        _t(
            "Molecular similarity and the Tanimoto coefficient",
            "12 min",
            r"""
# Molecular similarity and the Tanimoto coefficient

Once molecules are fingerprints, similarity is a set-overlap calculation. The
standard metric is the **Tanimoto (Jaccard) coefficient**. For two bit-vectors
with $a$ bits set in the first, $b$ in the second and $c$ in common:

$$T = \frac{c}{a + b - c}$$

$T$ ranges from $0$ (no shared features) to $1$ (identical fingerprints). The
**Dice coefficient** $D = \frac{2c}{a+b}$ weights the intersection more
heavily. The empirical **similarity principle** holds that structurally similar
molecules *tend* to have similar bioactivity — the basis for screening by
similarity to a known active.

```mermaid
flowchart LR
  A[Query fingerprint] --> C[Compare]
  B[Database fingerprints] --> C
  C --> D[Tanimoto score]
  D --> E["Rank; threshold ~0.7 ECFP4"]
```

A common rule of thumb is that an ECFP4 Tanimoto above ~0.7 suggests likely
shared activity, though this is descriptor-dependent and not a guarantee
(*activity cliffs* break it). As the count of shared bits $c$ grows for fixed
$a+b$, Tanimoto rises toward 1.

```plot
{"title": "Tanimoto vs shared bits (a+b fixed at 20)", "xLabel": "shared bits c", "yLabel": "Tanimoto", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(20-x)", "label": "T = c/(a+b-c)", "color": "#16a34a"}]}
```

**Next:** searching by substructure with SMARTS.
""",
        ),
        _t(
            "Substructure search and SMARTS",
            "11 min",
            r"""
# Substructure search and SMARTS

**Substructure search** asks: does molecule M contain pattern P? Formally this
is the **subgraph isomorphism** problem, which is NP-hard in general but fast in
practice on small molecular graphs using backtracking matchers (the
Ullmann/VF2 algorithms). It powers "find all molecules with a sulfonamide" type
queries.

Patterns are written in **SMARTS**, a query language that extends SMILES with
wildcards and logic. Examples: `[#6]` any carbon, `[!#1]` any non-hydrogen,
`[O;H1]` an oxygen with exactly one hydrogen, `c1ccccc1` a benzene ring, and
`[CX3](=O)[OX2H1]` a carboxylic acid. SMARTS expresses atom and bond
*constraints*, not a concrete molecule.

```mermaid
flowchart LR
  A[SMARTS pattern] --> B[Query graph]
  C[Database molecule] --> D[Target graph]
  B & D --> E[Subgraph isomorphism VF2]
  E --> F{Match?}
```

To avoid running an expensive subgraph match on every record, databases use a
**fingerprint screen** first: a candidate can match only if every bit set by
the query is also set in the molecule (a necessary condition). This cheap
filter discards most non-matches, so the costly VF2 step runs on a small
survivor set — search time per query drops sharply as the screen gets more
selective.

```plot
{"title": "Search cost vs screen selectivity", "xLabel": "screen strength", "yLabel": "relative match cost", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "candidates remaining", "color": "#dc2626"}]}
```

**Next:** predicting properties with QSAR.
""",
        ),
        _t(
            "Foundations of QSAR modelling",
            "12 min",
            r"""
# Foundations of QSAR modelling

**QSAR** (quantitative structure–activity relationship) builds a model
$y = f(\mathbf{x})$ that predicts a property $y$ (potency, solubility,
toxicity) from descriptor or fingerprint features $\mathbf{x}$. The
foundational example is the **Hansch equation**, relating biological activity
to lipophilicity and electronic terms, e.g.
$\log(1/C) = a\,\log P + b\,\sigma + c$, where $C$ is the concentration for an
effect and $\sigma$ a Hammett substituent constant.

The workflow is a supervised-learning loop: curate data, compute features,
**split** into train and test, fit a model, then validate.

```mermaid
flowchart LR
  A[Curated activity data] --> B[Compute descriptors]
  B --> C[Train/test split]
  C --> D[Fit model]
  D --> E[Validate: R2, RMSE, Q2]
  E --> F[Applicability domain]
```

Validation uses cross-validated $Q^2$ and external-set $R^2$; a model is only
trusted inside its **applicability domain** — the descriptor region the
training set actually covers. Overfitting is the central danger: as model
complexity grows, training error keeps falling but test error eventually rises,
giving the classic U-shaped generalisation curve. Choosing the complexity at
the minimum of the test curve is the goal.

```plot
{"title": "Generalisation error vs model complexity", "xLabel": "model complexity", "yLabel": "test error", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "test error rises late", "color": "#dc2626"}]}
```

**Next:** consolidate the quantitative methods with a quiz.
""",
        ),
        _quiz(),
    ),
)


# -- Cheminformatics -- Advanced -----------------------------------------------

_ADVANCED = SeedCourse(
    slug="cheminformatics-advanced",
    title="Cheminformatics — Advanced",
    description=(
        "State-of-the-art and applied cheminformatics: navigating chemical "
        "space and dimensionality reduction, clustering large libraries, "
        "building RDKit workflows, graph neural networks and learned "
        "representations, and generative models for de novo design. "
        "Modern methods with worked plots and pipeline diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Chemical space and dimensionality reduction",
            "12 min",
            r"""
# Chemical space and dimensionality reduction

**Chemical space** is the abstract high-dimensional space whose axes are
molecular features (descriptors or fingerprint bits). Each molecule is a point;
"nearby" points are structurally similar. The space is vast — enumerations of
drug-like molecules reach ~$10^{60}$ — so the goal is to *navigate* and
*visualise* it rather than enumerate it.

Because feature vectors have hundreds to thousands of dimensions, we project
them to 2D for inspection. **PCA** finds orthogonal directions of maximum
variance (linear); **t-SNE** and **UMAP** preserve local neighbourhoods
(non-linear), revealing clusters of related chemotypes.

```mermaid
flowchart LR
  A[Fingerprints high-D] --> B[PCA / UMAP / t-SNE]
  B --> C[2D embedding]
  C --> D[Visualise clusters]
  D --> E[Diversity / coverage analysis]
```

A practical concern is the **curse of dimensionality**: in high dimensions,
distances concentrate and pairwise contrasts shrink, so similarity becomes less
discriminating. The contrast between nearest and farthest points decays as
dimensionality rises, which is exactly why reduction and careful metric choice
matter.

```plot
{"title": "Distance contrast vs dimensionality", "xLabel": "dimensions (scaled)", "yLabel": "relative contrast", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "contrast decays", "color": "#dc2626"}]}
```

**Next:** grouping molecules with clustering.
""",
        ),
        _t(
            "Clustering chemical libraries",
            "12 min",
            r"""
# Clustering chemical libraries

**Clustering** groups a library into families of similar molecules to pick
diverse representatives, deduplicate series, or summarise screening hits. The
chemist's classic is the **Taylor–Butina** algorithm: using a Tanimoto
threshold, it greedily forms clusters around the most-connected molecules
(those with the most neighbours above threshold), assigning leftovers as
singletons. It is *deterministic* and needs no preset cluster count.

Alternatives include **k-means** on descriptor vectors (needs $k$ and a
Euclidean space), **hierarchical** clustering (a dendrogram, no fixed $k$), and
**sphere exclusion** for diversity picking.

```mermaid
flowchart LR
  A[Fingerprints] --> B[Pairwise Tanimoto]
  B --> C{Above threshold?}
  C -->|yes| D[Same cluster]
  C -->|no| E[New centroid]
  D & E --> F[Cluster set]
  F --> G[Pick representatives]
```

A key design choice is the **similarity threshold**: too high and almost every
molecule is its own singleton; too low and everything collapses into one giant
cluster. The number of clusters therefore falls as the threshold loosens,
typically a smooth decay — tuning it for a useful, interpretable partition is
the art.

```plot
{"title": "Cluster count vs Tanimoto threshold (loosening)", "xLabel": "1 - threshold (looser ->)", "yLabel": "relative cluster count", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "clusters merge", "color": "#16a34a"}]}
```

**Next:** building these workflows with RDKit.
""",
        ),
        _t(
            "RDKit workflows in practice",
            "12 min",
            r"""
# RDKit workflows in practice

**RDKit** is the leading open-source cheminformatics toolkit. A typical Python
workflow reads structures, sanitises them, computes fingerprints and runs an
analysis. The objects you touch most are `Mol` (a molecule) created via
`Chem.MolFromSmiles`, fingerprints from `AllChem.GetMorganFingerprintAsBitVect`,
and similarity from `DataStructs.TanimotoSimilarity`.

A standard hit-triage pipeline:

```mermaid
flowchart LR
  A["Read SDF / SMILES"] --> B[Sanitize & standardize]
  B --> C[Compute ECFP4 + descriptors]
  C --> D[Filter: Rule of Five / PAINS]
  D --> E[Similarity to known actives]
  E --> F[Cluster -> pick diverse hits]
```

Critical practical steps: **standardisation** (neutralise charges, strip salts,
canonicalise tautomers) so the same compound is never counted twice; and
**substructure filters** such as **PAINS** (Pan-Assay Interference compoundS) to
remove frequent false positives before they waste assay slots. Skipping
standardisation silently inflates duplicate and similarity counts.

Performance matters at scale: fingerprint similarity is bitwise and embarrassingly
parallel, so throughput grows nearly linearly with cores until I/O or memory
bandwidth saturates it.

```plot
{"title": "Screening throughput vs parallel workers", "xLabel": "workers", "yLabel": "relative throughput", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating speed-up", "color": "#2563eb"}]}
```

**Next:** learning representations with graph neural networks.
""",
        ),
        _t(
            "Graph neural networks and learned representations",
            "12 min",
            r"""
# Graph neural networks and learned representations

Fixed fingerprints encode *predefined* features; **graph neural networks
(GNNs)** instead *learn* a representation directly from the molecular graph. A
**message-passing neural network (MPNN)** repeatedly updates each atom's vector
by aggregating messages from its bonded neighbours; after $k$ rounds an atom's
embedding summarises its $k$-hop environment — a learned, differentiable analogue
of circular (ECFP) fingerprints. A **readout** pools atom vectors into one
molecule vector for prediction.

```mermaid
flowchart LR
  A[Molecular graph] --> B[Atom & bond features]
  B --> C[Message passing x k]
  C --> D[Atom embeddings]
  D --> E[Readout / pooling]
  E --> F[Property prediction]
```

Influential architectures include **D-MPNN** (Chemprop, message passing on
directed bonds), **graph attention** variants, and large **pretrained**
molecular transformers on SMILES. They often beat descriptor models when data
is plentiful, but offer less interpretability and can extrapolate poorly outside
the training distribution.

Their advantage grows with dataset size: with few labelled molecules a simple
ECFP + random-forest model wins, but learned representations overtake it as data
scales — a classic learning-curve crossover.

```plot
{"title": "Model accuracy vs training-set size", "xLabel": "training data (scaled)", "yLabel": "relative accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "GNN learning curve", "color": "#2563eb"}]}
```

**Next:** generating new molecules with generative models.
""",
        ),
        _t(
            "Generative models for de novo design",
            "12 min",
            r"""
# Generative models for de novo design

**De novo design** generates *new* molecules with desired properties rather than
screening existing ones. Generative models learn the distribution of valid,
drug-like molecules and sample from it. Major families: **SMILES-based RNNs /
VAEs** that learn a latent space of strings, **graph generative models** that
build molecules atom-by-atom while enforcing valence, and **reinforcement
learning** that fine-tunes a generator toward a scoring objective (potency,
synthesisability, novelty).

```mermaid
flowchart LR
  A[Training library] --> B[Learn distribution]
  B --> C[Sample candidates]
  C --> D[Score: QSAR / docking / SA]
  D --> E{Good?}
  E -->|reward| B
  E -->|keep| F[Candidate set]
```

Key evaluation axes are **validity** (chemically valid SMILES), **uniqueness**,
**novelty** (not in the training set), and **synthetic accessibility (SA)**.
The hard part is **multi-objective optimisation**: pushing potency often hurts
drug-likeness or synthesisability, so methods like Pareto optimisation or
weighted rewards balance competing goals. Frameworks such as **REINVENT** couple
an RNN generator to a multi-component scoring function.

As reinforcement-learning episodes accumulate, the fraction of generated
molecules meeting the target profile rises and then plateaus as the model
converges on the rewarded region of chemical space.

```plot
{"title": "Fraction of on-target molecules vs RL steps", "xLabel": "training steps (scaled)", "yLabel": "fraction on-target", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "RL optimisation", "color": "#16a34a"}]}
```

**Next:** a final knowledge check across the advanced methods.
""",
        ),
        _quiz(),
    ),
)


CHEMINFORMATICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["CHEMINFORMATICS_COURSES"]
