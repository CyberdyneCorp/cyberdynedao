"""AI-Driven Drug Discovery track: Basics -> Intermediate -> Advanced.

Three courses tracing where AI fits across drug discovery: from the pipeline and
molecular representations, through QSAR/property prediction, screening and docking,
to foundation models, generative design, active learning and the modern stack.
Lessons embed interactive ```plot blocks (dose-response, binding, learning curves)
and ```mermaid diagrams (pipelines, model taxonomies, active-learning loops).
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ──────────────────────────────────────────────────────────────────────
# 1. ai-drug-discovery-basics (Beginner)
# ──────────────────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="ai-drug-discovery-basics",
    title="AI-Driven Drug Discovery — Basics",
    description=(
        "Where artificial intelligence fits across the drug discovery pipeline. "
        "You'll meet the funnel from target to clinic, learn how molecules become "
        "machine-readable (SMILES, fingerprints, descriptors), and build intuition "
        "for the predictions AI makes: activity, ADMET and drug-likeness."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The drug discovery pipeline and where AI fits",
            "10 min",
            r"""# The drug discovery pipeline and where AI fits

Bringing a drug to market takes roughly **10–15 years** and over a billion
dollars, with attrition at every stage. The classic funnel runs: **target
identification** → **hit discovery** → **hit-to-lead** → **lead optimization**
→ **preclinical** → **clinical phases I–III** → **regulatory approval**.

AI does not replace this funnel — it accelerates the early, data-rich stages
where decisions are cheap and the search space is astronomically large
(drug-like chemical space is estimated at $10^{60}$ molecules). Machine learning
helps **prioritize** which targets are druggable, which compounds to synthesize,
and which molecules are likely to fail on safety or absorption.

```mermaid
flowchart LR
  A[Target ID] --> B[Hit discovery]
  B --> C[Hit-to-lead]
  C --> D[Lead optimization]
  D --> E[Preclinical]
  E --> F[Clinical I-III]
  F --> G[Approval]
  AI[AI / ML] -.-> A
  AI -.-> B
  AI -.-> C
  AI -.-> D
```

The economic value of AI is concentrated up front: catching a doomed compound
at hit-to-lead saves the enormous cost of a late clinical failure. Roughly 90%
of compounds entering clinical trials never reach approval, so even modest
improvements in early triage compound into large savings.

**Next:** how a molecule becomes data a model can read.
""",
        ),
        _t(
            "How molecules become data: SMILES, fingerprints, descriptors",
            "11 min",
            r"""# How molecules become data: SMILES, fingerprints, descriptors

Before a model can learn, a molecule must be encoded numerically. Three
representations dominate.

**SMILES** (Simplified Molecular-Input Line-Entry System) is a text string:
ethanol is `CCO`, aspirin is `CC(=O)OC1=CC=CC=C1C(=O)O`. SMILES is compact and
sequence-models (RNNs, transformers) read it directly.

**Fingerprints** are fixed-length bit vectors. An **ECFP / Morgan fingerprint**
hashes circular atom neighborhoods of a given radius into bits, so two molecules
with overlapping substructures share set bits. **Tanimoto similarity** between
fingerprints $A$ and $B$ is

$$T(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

**Descriptors** are computed physicochemical numbers — molecular weight, logP,
hydrogen-bond donors/acceptors, topological polar surface area (TPSA).

```mermaid
flowchart LR
  M[Molecule] --> S[SMILES string]
  M --> F[ECFP fingerprint bits]
  M --> D[Descriptors MW, logP, TPSA]
  S --> ML[Model input]
  F --> ML
  D --> ML
```

RDKit is the standard open-source toolkit for generating all three. The choice
of representation often matters as much as the model.

**Next:** what activity prediction actually means.
""",
        ),
        _t(
            "Activity, potency and dose-response",
            "11 min",
            r"""# Activity, potency and dose-response

A compound's **potency** is how much is needed to produce an effect. The
canonical readout is a **dose-response curve**: response plotted against the
logarithm of concentration, which produces a sigmoid.

The **half-maximal** point defines potency. **IC50** is the concentration that
inhibits a process by 50%; **EC50** the concentration giving half-maximal
effect. Because activity spans orders of magnitude, we work in log units:
$pIC_{50} = -\log_{10}(IC_{50})$, so larger $pIC_{50}$ means more potent.

```plot
{"title": "Sigmoidal dose-response", "xLabel": "log[compound]", "yLabel": "response (fraction)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#2563eb"}]}
```

The curve's midpoint (here at $x=5$) is the EC50 on the log axis. Models in drug
discovery most often **regress** $pIC_{50}$ (a continuous potency) or
**classify** active vs inactive against a threshold.

```mermaid
flowchart LR
  C[Concentration sweep] --> R[Measure response]
  R --> Fit[Fit sigmoid]
  Fit --> P[IC50 / EC50 -> pIC50]
```

**Next:** predicting whether a molecule behaves like a drug.
""",
        ),
        _t(
            "Drug-likeness and the Rule of Five",
            "10 min",
            r"""# Drug-likeness and the Rule of Five

Most orally administered drugs share physicochemical traits. **Lipinski's Rule
of Five** flags poor oral absorption when **two or more** of these limits are
violated:

- molecular weight $\le 500$ Da
- $\log P \le 5$ (lipophilicity)
- hydrogen-bond donors $\le 5$
- hydrogen-bond acceptors $\le 10$

Veber's rules add **rotatable bonds $\le 10$** and **TPSA $\le 140\ \text{Å}^2$**
for good bioavailability. These are coarse filters, not laws — many approved
drugs (especially antibiotics and natural products) break them.

```plot
{"title": "Oral absorption falls as lipophilicity grows", "xLabel": "logP", "yLabel": "relative absorption", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "absorption", "color": "#dc2626"}]}
```

AI uses these descriptors as features and also learns subtler patterns from data
that simple rules miss.

```mermaid
flowchart LR
  M[Candidate molecule] --> D[Compute MW, logP, HBD, HBA]
  D --> R{2+ rules broken?}
  R -->|Yes| Flag[Likely poor oral absorption]
  R -->|No| Pass[Drug-like]
```

**Next:** the ADMET properties that decide a drug's fate in the body.
""",
        ),
        _t(
            "ADMET: what happens to a drug in the body",
            "11 min",
            r"""# ADMET: what happens to a drug in the body

A potent molecule is useless if the body destroys, blocks or is harmed by it.
**ADMET** captures this: **A**bsorption, **D**istribution, **M**etabolism,
**E**xcretion, **T**oxicity. Late-stage failures are dominated by poor ADMET, so
predicting these early is one of AI's highest-value jobs.

- **Absorption** — does it cross the gut wall? (related to logP, TPSA)
- **Distribution** — does it reach the target tissue, cross the blood-brain barrier?
- **Metabolism** — how fast do liver enzymes (e.g. **CYP3A4**, **CYP2D6**) clear it?
- **Excretion** — kidney/biliary clearance sets the dosing interval
- **Toxicity** — off-target harm, e.g. **hERG** channel block causing cardiac risk

Plasma concentration after a dose typically rises then decays roughly
first-order; clearance sets the decay rate.

```plot
{"title": "Plasma concentration decay (first-order clearance)", "xLabel": "time (h)", "yLabel": "concentration", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  Dose --> A[Absorption]
  A --> D[Distribution]
  D --> M[Metabolism]
  M --> E[Excretion]
  D --> T[Toxicity risk]
```

**Next:** the families of AI tools used across these tasks.
""",
        ),
        _t(
            "Families of AI models in discovery",
            "10 min",
            r"""# Families of AI models in discovery

The tasks above — potency, ADMET, drug-likeness — are solved with a small zoo of
model families, chosen by data type and size.

- **Classical ML** (random forests, gradient boosting, SVMs) on **fingerprints
  or descriptors**: robust, fast, strong baselines, the workhorse of **QSAR**.
- **Deep neural networks** on the same features, useful with more data.
- **Graph neural networks (GNNs)** operate on the molecular graph directly
  (atoms as nodes, bonds as edges), learning the representation end-to-end.
- **Sequence models** (RNNs, transformers) read SMILES for both prediction and
  **generation** of new molecules.

```mermaid
flowchart TB
  Data[Molecular data] --> FP[Fingerprints/descriptors]
  Data --> G[Molecular graph]
  Data --> SEQ[SMILES sequence]
  FP --> RF[Random forest / XGBoost]
  G --> GNN[Graph neural network]
  SEQ --> TR[RNN / Transformer]
```

A common mistake is reaching for deep learning first. With a few hundred
measured compounds, a random forest on ECFP usually beats a GNN. Data volume,
not novelty, should drive the choice.

```plot
{"title": "Model accuracy vs training-set size", "xLabel": "training examples (x100)", "yLabel": "predictive skill", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "skill", "color": "#2563eb"}]}
```

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 2. ai-drug-discovery-intermediate (Intermediate)
# ──────────────────────────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="ai-drug-discovery-intermediate",
    title="AI-Driven Drug Discovery — Intermediate",
    description=(
        "Core quantitative methods for property and activity prediction. Build and "
        "validate QSAR models, understand graph neural networks for molecules, run "
        "virtual screening, and reason about docking, scaffolds and the metrics that "
        "decide whether a model is trustworthy."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "QSAR: regressing activity from structure",
            "12 min",
            r"""# QSAR: regressing activity from structure

**Quantitative Structure-Activity Relationship** modeling assumes a molecule's
activity is a function of its structure: $y = f(\mathbf{x}) + \varepsilon$, where
$\mathbf{x}$ is a descriptor or fingerprint vector and $y$ is typically
$pIC_{50}$. The earliest QSAR (Hansch analysis) used linear models in
lipophilicity and electronic terms; modern QSAR uses random forests, gradient
boosting and neural nets.

A regression model is trained by minimizing mean squared error,

$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2$$

and reported with $R^2$ on a held-out set. Crucially, performance improves with
data but saturates — and is bounded by experimental noise in the assay.

```plot
{"title": "QSAR skill saturates with data", "xLabel": "compounds (x100)", "yLabel": "R squared", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "R^2", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  S[Structures] --> X[Descriptors / ECFP]
  X --> T[Train regressor]
  T --> P[Predict pIC50]
  P --> V[Validate on held-out set]
```

**Next:** how to validate a QSAR model honestly.
""",
        ),
        _t(
            "Validation, splits and applicability domain",
            "12 min",
            r"""# Validation, splits and applicability domain

The fastest way to fool yourself is a **random train/test split**. Real
projects ask a model to predict *novel* chemistry, so honest validation uses a
**scaffold split** (Bemis-Murcko scaffolds): molecules sharing a core go to the
same fold, forcing the model to generalize across chemical series.

Always beware **data leakage**: near-duplicate molecules, or normalizing using
test-set statistics, inflate scores. Use **cross-validation** for small sets:

$$\text{CV error} = \frac{1}{k}\sum_{j=1}^{k}\text{MSE}_j$$

A model is only trustworthy inside its **applicability domain** — the region of
chemical space close to its training data. Predictions for molecules far from
any training point (low Tanimoto similarity) should be flagged as unreliable.

```plot
{"title": "Confidence falls outside the applicability domain", "xLabel": "distance from training data", "yLabel": "prediction reliability", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "reliability", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  D[Dataset] --> SC[Scaffold split]
  SC --> TR[Train]
  SC --> TE[Test on unseen scaffolds]
  TE --> AD{Inside applicability domain?}
  AD -->|Yes| Trust[Trust prediction]
  AD -->|No| Flag[Flag uncertain]
```

**Next:** learning the representation itself with graph neural networks.
""",
        ),
        _t(
            "Graph neural networks for molecules",
            "12 min",
            r"""# Graph neural networks for molecules

Fingerprints are fixed; a **graph neural network (GNN)** learns the molecular
representation end-to-end. A molecule is a graph: atoms are nodes (with features
like element and charge), bonds are edges.

GNNs use **message passing**: each node updates its embedding $h_v$ by
aggregating messages from neighbors $\mathcal{N}(v)$ over $T$ rounds,

$$h_v^{(t+1)} = \text{UPDATE}\!\left(h_v^{(t)},\ \sum_{u \in \mathcal{N}(v)} \text{MSG}\big(h_u^{(t)}, e_{uv}\big)\right)$$

After $T$ rounds a **readout** pools all node embeddings into a single molecular
vector for prediction. Each round widens the receptive field, so the number of
rounds controls how large a substructure each atom "sees".

```plot
{"title": "Receptive field grows with message-passing rounds", "xLabel": "rounds T", "yLabel": "atoms reached (norm.)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "coverage", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  G[Molecular graph] --> MP[Message passing x T]
  MP --> RO[Readout / pooling]
  RO --> MLP[MLP head]
  MLP --> Y[Property prediction]
```

Frameworks like **DGL-LifeSci**, **PyTorch Geometric** and **Chemprop** (D-MPNN)
make GNNs practical; Chemprop is a strong default for property prediction.

**Next:** searching huge libraries with virtual screening.
""",
        ),
        _t(
            "Virtual screening and enrichment",
            "11 min",
            r"""# Virtual screening and enrichment

**Virtual screening (VS)** ranks a large library so the few compounds you can
afford to test are the most promising. **Ligand-based VS** uses similarity or a
QSAR model; **structure-based VS** uses the protein structure (docking).

Success is measured by **enrichment**, not raw accuracy, because actives are rare
(often <1%). The **enrichment factor** at the top $x\%$ is

$$EF_{x\%} = \frac{\text{(actives found in top } x\%)}{\text{(actives expected by random)}}$$

and the ranking is summarized by **ROC-AUC** or, better for early recognition,
**BEDROC** which up-weights actives ranked near the top.

```plot
{"title": "ROC curve: good ranker vs random", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "good ranker", "color": "#2563eb"}, {"expr": "x", "label": "random", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  L[Million-compound library] --> M[Score with model/docking]
  M --> R[Rank]
  R --> T[Pick top 1%]
  T --> A[Assay -> hits]
```

**Next:** the structure-based engine behind screening — docking.
""",
        ),
        _t(
            "Molecular docking and scoring",
            "12 min",
            r"""# Molecular docking and scoring

**Docking** predicts how a ligand binds in a protein pocket and estimates the
binding affinity. It has two parts: a **search** over poses (position,
orientation, conformation) and a **scoring function** that ranks them.

Scoring functions approximate the binding free energy by summing physically
motivated terms — van der Waals, electrostatics, hydrogen bonds, desolvation:

$$\Delta G_{\text{bind}} \approx \sum_i w_i\, E_i$$

Binding strength relates to the dissociation constant by
$\Delta G = RT \ln K_d$, so tighter binders (smaller $K_d$) have more negative
$\Delta G$. The fraction of receptor bound follows a saturating curve in ligand
concentration.

```plot
{"title": "Receptor occupancy vs ligand concentration", "xLabel": "[ligand] / Kd", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  P[Protein pocket] --> S[Pose search]
  Lig[Ligand] --> S
  S --> SF[Scoring function]
  SF --> Rank[Rank poses by deltaG]
```

Tools include **AutoDock Vina**, **Glide** and **GOLD**. Classical scoring
functions are fast but noisy; ML-based scoring (e.g. GNN rescoring) increasingly
improves pose ranking.

**Next:** scaffolds and how chemists reason about series.
""",
        ),
        _t(
            "Scaffolds, similarity and chemical space",
            "11 min",
            r"""# Scaffolds, similarity and chemical space

Chemists rarely optimize one molecule; they optimize a **series** sharing a
core **scaffold** (a Bemis-Murcko framework: rings plus linkers, stripped of
side chains). Decorating a scaffold with different substituents (an **R-group**
analysis) lets a structure-activity relationship emerge.

The guiding heuristic is the **similarity principle**: structurally similar
molecules tend to have similar activity. Quantified by **Tanimoto similarity**
on fingerprints, it underpins ligand-based screening — but it fails at
**activity cliffs**, where a tiny structural change causes a huge activity
change, the hardest cases for any model.

```plot
{"title": "Similarity principle (with cliff residual)", "xLabel": "Tanimoto similarity", "yLabel": "P(similar activity)", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x", "label": "trend", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  C[Compound set] --> SC[Extract scaffolds]
  SC --> S1[Scaffold A series]
  SC --> S2[Scaffold B series]
  S1 --> R[R-group SAR]
  S2 --> R
```

Visualizing chemical space (e.g. with UMAP of fingerprints) reveals clusters,
diversity gaps and where a library is over- or under-explored.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 3. ai-drug-discovery-advanced (Advanced)
# ──────────────────────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="ai-drug-discovery-advanced",
    title="AI-Driven Drug Discovery — Advanced",
    description=(
        "State of the art and applied. Generative molecular design, foundation models "
        "and self-supervised pretraining, structure prediction (AlphaFold), active "
        "learning loops, multi-objective optimization, and the self-driving lab that "
        "ties prediction, generation and experiment together."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Generative molecular design",
            "13 min",
            r"""# Generative molecular design

Rather than screen a fixed library, **generative models** propose new molecules
optimized for desired properties. The main families:

- **Autoregressive SMILES / SELFIES models** generate strings token by token;
  SELFIES guarantees every string is a valid molecule.
- **Variational autoencoders (VAEs)** learn a continuous latent space where
  optimization and interpolation are possible.
- **Graph generative models** build the molecular graph directly.
- **Diffusion models** denoise atoms/coordinates, now strong for 3D design.

A continuous latent space lets you do gradient-guided optimization: encode,
move toward higher predicted property, decode.

```mermaid
flowchart LR
  D[Molecule dataset] --> ENC[Encoder]
  ENC --> Z[Latent space z]
  Z --> OPT[Optimize toward property]
  OPT --> DEC[Decoder]
  DEC --> New[Novel candidate]
```

The danger is **reward hacking**: a model maximizing a predicted score finds
adversarial, unsynthesizable molecules. Generators must be constrained by
**synthetic accessibility (SA score)**, validity and novelty — and the property
oracle must hold up off-distribution.

```plot
{"title": "Property gains saturate as you optimize", "xLabel": "optimization steps (x10)", "yLabel": "predicted property", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "property", "color": "#2563eb"}]}
```

**Next:** pretraining and molecular foundation models.
""",
        ),
        _t(
            "Foundation models and self-supervised pretraining",
            "13 min",
            r"""# Foundation models and self-supervised pretraining

Labeled bioactivity data is scarce and expensive, but **unlabeled** molecules
number in the hundreds of millions. **Self-supervised pretraining** exploits
this: train on a pretext task (masked-atom prediction, contrastive learning, or
masked-SMILES language modeling à la **ChemBERTa**), then **fine-tune** on a
small labeled set.

This mirrors NLP: a model like **MolBERT**, **Grover** or **Uni-Mol** learns
general chemistry, transferring to downstream property tasks with far fewer
labels. The payoff is steepest exactly where data is smallest.

```plot
{"title": "Pretraining lifts skill most in the low-data regime", "xLabel": "labeled examples (x100)", "yLabel": "skill", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(1+x)/9", "label": "pretrained", "color": "#16a34a"}, {"expr": "8*x/(4+x)/9", "label": "from scratch", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  U[100M+ unlabeled molecules] --> PT[Self-supervised pretrain]
  PT --> FM[Foundation model]
  FM --> FT[Fine-tune on small labeled set]
  FT --> Task[Property / activity head]
```

The caveat: pretrained molecular models still respect the applicability domain
and can encode dataset biases. Pretraining shifts the data-efficiency curve; it
does not remove the need for honest validation.

**Next:** predicting the protein side of the equation.
""",
        ),
        _t(
            "Structure prediction and structure-based AI",
            "13 min",
            r"""# Structure prediction and structure-based AI

Drug binding is 3D, so knowing the target's structure is decisive.
**AlphaFold2** and **AlphaFold3** predict protein 3D structure from sequence at
near-experimental accuracy for many proteins, collapsing what once took years of
crystallography. This unlocks **structure-based design** for targets without an
experimental structure.

Confidence is reported per residue as **pLDDT** (0–100); flexible loops and
disordered regions score low and must be treated cautiously. AI now also tackles
the harder **co-folding** problem — predicting the protein-ligand complex
directly (AlphaFold3, RoseTTAFold All-Atom).

```plot
{"title": "Model usefulness rises with structural confidence", "xLabel": "pLDDT (x10)", "yLabel": "design usefulness", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-6)))", "label": "usefulness", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Seq[Protein sequence] --> AF[AlphaFold]
  AF --> Str[3D structure + pLDDT]
  Str --> Pocket[Pocket detection]
  Pocket --> SBD[Structure-based design / docking]
```

Predicted structures are powerful but not infallible: a high-pLDDT backbone can
still have a misplaced side chain that ruins docking. Treat predicted complexes
as hypotheses to validate.

**Next:** choosing experiments intelligently with active learning.
""",
        ),
        _t(
            "Active learning and Bayesian optimization",
            "13 min",
            r"""# Active learning and Bayesian optimization

Synthesis and assays are the bottleneck, so the goal is to learn the most from
the fewest experiments. **Active learning** closes a loop: a model predicts,
**proposes** the next batch to test, you run it, retrain, repeat.

The proposal balances **exploitation** (test the predicted-best) and
**exploration** (test where the model is uncertain). **Bayesian optimization**
formalizes this with an acquisition function such as **Expected Improvement**
over a surrogate (often a Gaussian process) that yields a predictive mean
$\mu(x)$ and uncertainty $\sigma(x)$:

$$\alpha_{UCB}(x) = \mu(x) + \kappa\,\sigma(x)$$

```plot
{"title": "Active learning reaches the optimum in fewer experiments", "xLabel": "experiments (x10)", "yLabel": "best found", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "active learning", "color": "#16a34a"}, {"expr": "1/(1+exp(-(x-6)))", "label": "random", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Model --> Acq[Acquisition: balance mu and sigma]
  Acq --> Batch[Select next batch]
  Batch --> Exp[Synthesize + assay]
  Exp --> Data[New labels]
  Data --> Model
```

**Next:** optimizing many objectives at once.
""",
        ),
        _t(
            "Multi-objective optimization and the design funnel",
            "12 min",
            r"""# Multi-objective optimization and the design funnel

A real candidate must be potent **and** selective **and** soluble **and**
non-toxic **and** synthesizable. These objectives conflict — pushing potency
often worsens solubility. There is no single best molecule, only a set of
**non-dominated** trade-offs: the **Pareto front**.

A molecule is **Pareto-optimal** if no other is better on every objective. A
common practical tactic is a **desirability function** $D = \left(\prod_i d_i
\right)^{1/n}$, the geometric mean of per-property desirabilities $d_i \in [0,1]$,
so any zero kills the candidate — enforcing balance, not a single inflated
metric.

```plot
{"title": "Pareto front: potency vs solubility trade-off", "xLabel": "potency (norm.)", "yLabel": "max achievable solubility", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-x^2", "label": "Pareto front", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Cand[Candidates] --> P[Potency model]
  Cand --> S[Solubility model]
  Cand --> T[Tox model]
  P --> D[Desirability D]
  S --> D
  T --> D
  D --> F[Pareto-optimal set]
```

**Next:** assembling everything into the modern stack.
""",
        ),
        _t(
            "The modern stack: self-driving labs and the AI loop",
            "13 min",
            r"""# The modern stack: self-driving labs and the AI loop

The frontier integrates every piece into a closed **Design-Make-Test-Analyze
(DMTA)** loop, increasingly automated as a **self-driving lab**. Generative
design proposes molecules; property and ADMET models triage them; active
learning picks the batch; robotic synthesis and high-throughput assays measure
reality; results retrain the models. The loop tightens each cycle.

```mermaid
flowchart LR
  Gen[Generative design] --> Pred[Property/ADMET prediction]
  Pred --> AL[Active learning selection]
  AL --> Make[Automated synthesis]
  Make --> Test[High-throughput assay]
  Test --> Analyze[Analyze + retrain]
  Analyze --> Gen
```

Each turn of the loop should improve the best candidate, with diminishing
returns as chemistry is exhausted — making the **cost per cycle** the binding
constraint.

```plot
{"title": "Best candidate improves each DMTA cycle", "xLabel": "DMTA cycle", "yLabel": "best candidate quality", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "quality", "color": "#16a34a"}]}
```

The hard problems remain **causality** (does the target actually drive disease?),
**generalization** beyond known chemistry, and **trust** — clinicians and
regulators need calibrated, explainable predictions, not just high benchmark
scores. AI compresses the early funnel; biology and the clinic still gate the
finish.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


AI_DRUG_DISCOVERY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["AI_DRUG_DISCOVERY_COURSES"]
