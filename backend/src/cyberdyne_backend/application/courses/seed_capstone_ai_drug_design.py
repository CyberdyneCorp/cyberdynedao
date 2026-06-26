"""Capstone: End-to-End AI Drug Design Project track: Basics -> Intermediate -> Advanced.

Three courses that run one project from start to finish: framing a target and
assembling data; through virtual screening, ML modeling and generative design;
to validation, simulation and a decision dossier. Lessons embed interactive
```plot blocks (dose-response, enrichment, learning and convergence curves) and
```mermaid diagrams (the DMTA loop, data pipelines, decision gates).
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ──────────────────────────────────────────────────────────────────────
# 1. capstone-ai-drug-design-basics (Beginner)
# ──────────────────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="capstone-ai-drug-design-basics",
    title="Capstone: End-to-End AI Drug Design Project — Basics",
    description=(
        "Frame a real AI drug-design project from scratch. You'll choose and "
        "validate a target, assemble and clean bioactivity data, learn the "
        "Design-Make-Test-Analyze loop, and scope a hit-finding plan with a clear "
        "objective and success criteria before any model is trained."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Framing the project: the DMTA loop end to end",
            "10 min",
            r"""# Framing the project: the DMTA loop end to end

A capstone drug-design project is not a single model — it is a **loop**. The
organizing cycle of modern discovery is **Design-Make-Test-Analyze (DMTA)**:
propose molecules, synthesize them, assay them, learn, and propose again. AI
accelerates the *Design* and *Analyze* arms, but the loop only closes when
predictions meet real measurements.

Before any code, you fix three things: the **target** (the protein or pathway
you will act on), the **objective** (e.g. find sub-micromolar, selective,
drug-like inhibitors), and the **success criteria** (how many validated hits,
at what potency, by when).

```mermaid
flowchart LR
  Design[Design: propose molecules] --> Make[Make: synthesize]
  Make --> Test[Test: assay activity]
  Test --> Analyze[Analyze: model + learn]
  Analyze --> Design
```

Each turn of the loop should improve your best candidate. The discipline of a
good capstone is to define, up front, what "better" means and how you will
measure it — so that progress is visible cycle by cycle rather than asserted at
the end.

**Next:** choosing a target worth pursuing.
""",
        ),
        _t(
            "Choosing and validating a target",
            "11 min",
            r"""# Choosing and validating a target

A drug acts on a **target** — most often a protein whose activity drives a
disease. **Target validation** asks two questions: does modulating this target
change the disease (causality), and can a small molecule actually bind it
(**druggability**)?

Evidence for causality comes from genetics (loss-of-function variants),
knockdown/knockout studies, and known biology. Druggability is judged from the
structure: does the protein have a well-defined, enclosed **binding pocket**
with the right size and hydrophobicity? Enzymes (kinases, proteases) and
receptors are classically tractable; flat protein-protein interfaces are hard.

```mermaid
flowchart TB
  T[Candidate target] --> C{Causal in disease?}
  C -->|genetics, knockouts| D{Druggable pocket?}
  D -->|structure, pocket detection| V[Validated target]
  C -->|weak evidence| R[Reject]
  D -->|flat, shallow| R
```

A capstone target should have public data: known ligands in **ChEMBL**, a
structure (experimental or AlphaFold) in the **PDB**, and a defensible disease
link. Picking a heavily studied target makes data assembly tractable and lets
you benchmark against the literature.

**Next:** finding the data that will train every later model.
""",
        ),
        _t(
            "Assembling the dataset: ChEMBL, PDB and beyond",
            "11 min",
            r"""# Assembling the dataset: ChEMBL, PDB and beyond

Every model downstream is only as good as the data you assemble now. The core
public sources are **ChEMBL** (curated bioactivities — IC50, Ki, EC50 with
assay context), **PubChem** (bioassay screens), the **PDB** (3D protein and
complex structures), and **BindingDB** (binding affinities).

You pull all measured compounds for your target, then **harmonize** units:
activities are converted to a common log scale, $pIC_{50} = -\log_{10}(IC_{50})$
with $IC_{50}$ in molar, so that a wide dynamic range becomes a well-behaved
continuous label.

```mermaid
flowchart LR
  CHEMBL[ChEMBL bioactivities] --> Merge[Merge by target]
  PUBCHEM[PubChem assays] --> Merge
  BDB[BindingDB] --> Merge
  PDB[PDB structures] --> Merge
  Merge --> DS[Project dataset]
```

Because activity spans many orders of magnitude, the log transform also makes
the label distribution roughly symmetric, which most regressors prefer.

```plot
{"title": "Activity is log-distributed: convert IC50 to pIC50", "xLabel": "IC50 (uM)", "yLabel": "relative count", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "raw IC50 counts", "color": "#dc2626"}]}
```

**Next:** cleaning that data so the project does not inherit its errors.
""",
        ),
        _t(
            "Cleaning and curating chemical data",
            "10 min",
            r"""# Cleaning and curating chemical data

Raw bioactivity data is noisy. **Curation** is unglamorous but decisive — a
sloppy dataset poisons every model trained on it. The standard steps:

- **Standardize structures**: neutralize charges, remove salts and solvents,
  pick a canonical tautomer (RDKit's standardizer is the common tool).
- **Deduplicate**: the same compound measured many times must be merged; if
  values disagree wildly across assays, the measurement is unreliable.
- **Filter by assay quality**: keep a single, comparable assay type; mixing
  IC50 from different protocols introduces systematic offsets.
- **Flag outliers and PAINS**: pan-assay interference compounds give false
  positives and should be quarantined, not trusted.

```mermaid
flowchart LR
  Raw[Raw records] --> Std[Standardize structures]
  Std --> Dedup[Deduplicate + aggregate]
  Dedup --> QC[Assay-type filter]
  QC --> PAINS[Flag PAINS / outliers]
  PAINS --> Clean[Clean dataset]
```

A well-curated set typically loses a meaningful fraction of raw records — that
loss is a feature, not a failure. Document every filter so the pipeline is
reproducible.

```plot
{"title": "Records retained as curation tightens", "xLabel": "curation strictness", "yLabel": "fraction retained", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "retained", "color": "#2563eb"}]}
```

**Next:** turning molecules into numbers a model can read.
""",
        ),
        _t(
            "Representing molecules for modeling",
            "10 min",
            r"""# Representing molecules for modeling

A model cannot read a molecule directly; it needs a numerical representation.
Three dominate, and you will use them throughout the project.

**SMILES** is a text string (ethanol is `CCO`), read directly by sequence and
generative models. **Fingerprints** — notably the **ECFP / Morgan** fingerprint
— hash circular atom neighborhoods into a fixed bit vector, so molecules sharing
substructures share bits. **Descriptors** are computed numbers: molecular
weight, logP, hydrogen-bond donors/acceptors, TPSA.

Similarity between two fingerprints $A$ and $B$ is the **Tanimoto coefficient**

$$T(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

which underpins clustering, deduplication and ligand-based search later.

```mermaid
flowchart LR
  M[Molecule] --> S[SMILES]
  M --> F[ECFP fingerprint]
  M --> D[Descriptors MW, logP, TPSA]
  S --> Model[Model input]
  F --> Model
  D --> Model
```

```plot
{"title": "Similar pairs tend to share more fingerprint bits", "xLabel": "Tanimoto similarity", "yLabel": "shared substructure (norm.)", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x", "label": "trend", "color": "#16a34a"}]}
```

**Next:** writing the project plan and its success criteria.
""",
        ),
        _t(
            "Scoping the project plan and success criteria",
            "10 min",
            r"""# Scoping the project plan and success criteria

A capstone needs a plan you can be held to. State the **objective** as a target
product profile in miniature: e.g. "identify 5 commercially available
compounds with predicted $pIC_{50} > 7$, drug-like properties, and confirmed
binding in a docking model." Vague goals make success unfalsifiable.

Then lay out the **stages and gates**. Each gate is a go/no-go decision with an
explicit threshold, so weak candidates are killed cheaply and early — the
economic logic of the whole field.

```mermaid
flowchart LR
  Plan[Objective + criteria] --> Data[Data assembled]
  Data --> Model[Model trained + validated]
  Model --> Screen[Virtual screen]
  Screen --> Gate{Hits meet criteria?}
  Gate -->|yes| Dossier[Decision dossier]
  Gate -->|no| Iterate[Refine + loop]
```

Crucially, decide your validation strategy *now*: a scaffold split, a held-out
test set, and a baseline to beat. Resources are finite, so the plan also says
how many compounds you can afford to "test" (dock, simulate, or buy) — the
budget that the whole loop is optimized against.

```plot
{"title": "Value of catching failures earlier in the plan", "xLabel": "stage of failure", "yLabel": "cost incurred", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "cost", "color": "#dc2626"}]}
```

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 2. capstone-ai-drug-design-intermediate (Intermediate)
# ──────────────────────────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="capstone-ai-drug-design-intermediate",
    title="Capstone: End-to-End AI Drug Design Project — Intermediate",
    description=(
        "The quantitative core of the project. Build and honestly validate a QSAR "
        "model, run a ligand-based virtual screen, dock the top candidates, generate "
        "new molecules, and read the metrics — enrichment, ROC-AUC, scaffold splits — "
        "that decide whether each stage actually worked."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Building the QSAR activity model",
            "12 min",
            r"""# Building the QSAR activity model

With a curated dataset and representations in hand, the first model predicts
activity from structure — **Quantitative Structure-Activity Relationship
(QSAR)**. You learn a function $y = f(\mathbf{x}) + \varepsilon$ where
$\mathbf{x}$ is an ECFP fingerprint (or descriptor vector) and $y$ is
$pIC_{50}$.

Start with a strong, fast baseline: a **random forest** or **gradient boosting**
(XGBoost, LightGBM) on ECFP. These dominate small-to-medium chemical datasets
and are hard to beat without far more data. Training minimizes mean squared
error,

$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2$$

```mermaid
flowchart LR
  S[Curated structures] --> X[ECFP / descriptors]
  X --> RF[Random forest / XGBoost]
  RF --> P[Predict pIC50]
  P --> M[Metrics: R^2, RMSE]
```

Predictive skill rises with data then saturates, bounded by assay noise — a key
expectation to set before you over-engineer the model.

```plot
{"title": "QSAR R-squared saturates with data", "xLabel": "compounds (x100)", "yLabel": "R squared", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "R^2", "color": "#2563eb"}]}
```

**Next:** validating that model without fooling yourself.
""",
        ),
        _t(
            "Validating the model honestly",
            "12 min",
            r"""# Validating the model honestly

The easiest way to ship a useless model is a **random train/test split**. Your
project must predict *novel* chemistry, so validate with a **scaffold split**
(Bemis-Murcko frameworks): molecules sharing a core go to the same fold, forcing
generalization across series.

Guard against **data leakage** — near-duplicate molecules straddling the split,
or scaling features with test-set statistics, both inflate scores. For small
sets use $k$-fold cross-validation:

$$\text{CV error} = \frac{1}{k}\sum_{j=1}^{k}\text{MSE}_j$$

A prediction is only trustworthy inside the **applicability domain** — the
region of chemical space near training data. Flag predictions for molecules with
low Tanimoto similarity to anything seen.

```mermaid
flowchart LR
  D[Dataset] --> SC[Scaffold split]
  SC --> TR[Train]
  SC --> TE[Test on unseen scaffolds]
  TE --> AD{Inside applicability domain?}
  AD -->|yes| Trust[Trust prediction]
  AD -->|no| Flag[Flag uncertain]
```

```plot
{"title": "Reliability falls outside the applicability domain", "xLabel": "distance from training data", "yLabel": "reliability", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "reliability", "color": "#dc2626"}]}
```

**Next:** using the validated model to screen a large library.
""",
        ),
        _t(
            "Running the virtual screen",
            "11 min",
            r"""# Running the virtual screen

A validated model becomes a **virtual screen**: rank a large library so the few
compounds you can afford to test are the most promising. **Ligand-based**
screening scores each library molecule with your QSAR model or by similarity to
known actives; **structure-based** uses docking (next lesson).

Because actives are rare (often <1%), success is measured by **enrichment**, not
raw accuracy. The **enrichment factor** at the top $x\%$ is

$$EF_{x\%} = \frac{\text{actives found in top } x\%}{\text{actives expected by random}}$$

and the overall ranking is summarized by **ROC-AUC** — or, better for early
recognition, **BEDROC**, which up-weights actives at the very top of the list.

```plot
{"title": "ROC: a useful ranker vs random", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "ranker", "color": "#2563eb"}, {"expr": "x", "label": "random", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Lib[Library e.g. Enamine REAL] --> Score[Score with QSAR / similarity]
  Score --> Rank[Rank]
  Rank --> Top[Take top fraction]
  Top --> Next[Dock + inspect]
```

**Next:** structure-based scoring of the shortlist with docking.
""",
        ),
        _t(
            "Docking the shortlist",
            "12 min",
            r"""# Docking the shortlist

The screen's top compounds are passed to **molecular docking**, which predicts
how each ligand binds the target pocket and estimates affinity. Docking has two
parts: a **search** over poses (position, orientation, conformation) and a
**scoring function** ranking them.

Scoring functions approximate binding free energy as a sum of physical terms —
van der Waals, electrostatics, hydrogen bonds, desolvation:

$$\Delta G_{\text{bind}} \approx \sum_i w_i\, E_i$$

Affinity relates to the dissociation constant by $\Delta G = RT \ln K_d$, so
tighter binders (smaller $K_d$) have more negative $\Delta G$. Receptor
occupancy saturates with ligand concentration.

```plot
{"title": "Receptor occupancy vs ligand concentration", "xLabel": "[ligand] / Kd", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Pocket[Target pocket] --> Search[Pose search]
  Lig[Shortlisted ligand] --> Search
  Search --> SF[Scoring function]
  SF --> Pose[Top pose + deltaG]
  Pose --> Inspect[Visual + interaction check]
```

Tools include **AutoDock Vina**, **Glide** and **GOLD**. Classical scores are
fast but noisy, so always inspect the pose: are key interactions present, or is
the score an artifact? Docking ranks, it does not prove.

**Next:** generating brand-new molecules to feed the loop.
""",
        ),
        _t(
            "Generating new candidate molecules",
            "12 min",
            r"""# Generating new candidate molecules

Screening searches a fixed library; **generative design** invents new molecules
optimized toward your objective. The families you can use in the capstone:

- **Autoregressive SMILES / SELFIES** models build strings token by token;
  SELFIES guarantees every output is a valid molecule.
- **Variational autoencoders (VAEs)** learn a continuous latent space where you
  can optimize and interpolate.
- **Graph and diffusion models** build the molecular graph or 3D coordinates
  directly.

You steer generation toward high predicted $pIC_{50}$ while constraining
**validity**, **novelty**, and **synthetic accessibility (SA score)** — the
guards against the model proposing unmakeable, adversarial structures.

```mermaid
flowchart LR
  Seed[Known actives] --> Train[Train generator]
  Train --> Gen[Sample candidates]
  Gen --> Filter[Validity + SA + novelty]
  Filter --> Pred[Score with QSAR]
  Pred --> Loop[Feed best into DMTA]
```

Property gains saturate as you push optimization — and an over-optimized oracle
invites **reward hacking**, so generated molecules still go through the same
docking and validation gates as screened ones.

```plot
{"title": "Generated-property gains saturate", "xLabel": "optimization steps (x10)", "yLabel": "predicted property", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "8*x/(2+x)/9", "label": "property", "color": "#16a34a"}]}
```

**Next:** reading the metrics that decide if each stage worked.
""",
        ),
        _t(
            "Reading the metrics that gate each stage",
            "11 min",
            r"""# Reading the metrics that gate each stage

Each stage of the project has its own honest metric, and confusing them is a
classic mistake. For the **QSAR model**, report $R^2$ and RMSE on a scaffold
split. For the **virtual screen**, report enrichment factor, ROC-AUC and
BEDROC — never plain accuracy, which is meaningless when actives are 1%. For
**generation**, report validity, uniqueness, novelty and SA score alongside
predicted potency.

For classification thresholds (active vs inactive), precision and recall trade
off; the **F1 score** balances them:

$$F_1 = \frac{2\,P\,R}{P + R}$$

```mermaid
flowchart TB
  Stage[Pipeline stage] --> Q{Which metric?}
  Q -->|QSAR regression| R2[R^2 / RMSE on scaffold split]
  Q -->|virtual screen| EF[EF / ROC-AUC / BEDROC]
  Q -->|generation| GV[validity / novelty / SA]
  Q -->|classifier| F1[precision / recall / F1]
```

A model that wins on the wrong metric can still fail the project. Always tie
each number back to the success criteria you wrote in the plan.

```plot
{"title": "Precision-recall trade-off", "xLabel": "recall", "yLabel": "precision", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-x^2", "label": "PR curve", "color": "#2563eb"}]}
```

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 3. capstone-ai-drug-design-advanced (Advanced)
# ──────────────────────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="capstone-ai-drug-design-advanced",
    title="Capstone: End-to-End AI Drug Design Project — Advanced",
    description=(
        "Validate, simulate and decide. Run molecular dynamics and free-energy "
        "calculations on top candidates, predict ADMET and off-target risk, close "
        "the loop with active learning, quantify uncertainty, and assemble a "
        "defensible decision dossier with the AI/computational evidence behind it."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Molecular dynamics: validating the binding pose",
            "13 min",
            r"""# Molecular dynamics: validating the binding pose

A docking pose is a static snapshot; proteins move. **Molecular dynamics (MD)**
simulates the protein-ligand complex over time by integrating Newton's equations
under a **force field** (AMBER, CHARMM, OPLS), revealing whether the predicted
binding mode is *stable* once water and thermal motion are present.

The standard stability readout is the **RMSD** of the ligand from its docked
pose over the trajectory; a pose that drifts away was likely an artifact, while
one that fluctuates around a low value is plausible. Tools: **GROMACS**,
**OpenMM**, **AMBER**.

```plot
{"title": "Ligand RMSD: stable pose settles to a plateau", "xLabel": "simulation time (ns)", "yLabel": "RMSD (norm.)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "stable pose", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Complex[Docked complex] --> Prep[Solvate + parametrize]
  Prep --> Eq[Equilibrate]
  Eq --> Prod[Production MD]
  Prod --> Ana[RMSD / contacts / stability]
```

MD is expensive, so it is reserved for the handful of top candidates — a
deeper, costlier "test" in the loop that filters out poses docking got wrong.

**Next:** quantifying affinity with free-energy methods.
""",
        ),
        _t(
            "Free-energy calculations and binding affinity",
            "13 min",
            r"""# Free-energy calculations and binding affinity

Docking scores rank but estimate affinity poorly. For the final candidates,
**free-energy methods** give physics-grounded affinity predictions. The
rigorous approach is **free-energy perturbation (FEP)** or thermodynamic
integration, which computes the *relative* binding free energy between two
similar ligands by alchemically transforming one into the other.

The relative binding free energy between ligands A and B is

$$\Delta\Delta G_{\text{bind}} = \Delta G_{\text{bind}}^{B} - \Delta G_{\text{bind}}^{A}$$

A cheaper middle ground is **MM-GBSA / MM-PBSA**, which estimates binding energy
from MD snapshots. FEP is accurate (often within ~1 kcal/mol on congeneric
series) but costly, so it is applied only to closely related top compounds where
relative ranking decides synthesis.

```plot
{"title": "Predicted vs measured affinity (ideal = diagonal)", "xLabel": "predicted deltaG (norm.)", "yLabel": "measured deltaG (norm.)", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x", "label": "ideal", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  Pair[Congeneric ligand pair] --> Alch[Alchemical transform]
  Alch --> Sim[MD windows]
  Sim --> DDG[Compute deltadeltaG]
  DDG --> Rank[Rank for synthesis]
```

**Next:** predicting whether a candidate survives the body — ADMET.
""",
        ),
        _t(
            "ADMET and off-target risk prediction",
            "13 min",
            r"""# ADMET and off-target risk prediction

A potent binder is worthless if the body destroys it or it is toxic. **ADMET**
— Absorption, Distribution, Metabolism, Excretion, Toxicity — drives most
late-stage failures, so predicting it now, with ML models, protects the project.

Key learned endpoints: solubility and permeability (absorption), blood-brain
barrier penetration (distribution), **CYP** inhibition and metabolic clearance
(metabolism), and toxicity flags — above all **hERG** channel block, a cardiac
liability. Plasma concentration after a dose decays roughly first-order;
clearance sets the dosing interval.

```plot
{"title": "Plasma concentration decay (first-order clearance)", "xLabel": "time (h)", "yLabel": "concentration", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  Cand[Candidate] --> A[Absorption: solubility, permeability]
  Cand --> D[Distribution: BBB]
  Cand --> M[Metabolism: CYP, clearance]
  Cand --> T[Toxicity: hERG, mutagenicity]
  A --> Score[ADMET profile]
  D --> Score
  M --> Score
  T --> Score
```

**Selectivity** matters too: dock or model against off-targets to flag
promiscuity early. ADMET turns a "binds well" candidate into a "could be a
drug" candidate.

**Next:** closing the loop intelligently with active learning.
""",
        ),
        _t(
            "Closing the loop with active learning",
            "13 min",
            r"""# Closing the loop with active learning

Synthesis and assays are the bottleneck, so the project should learn the most
from the fewest experiments. **Active learning** closes the DMTA loop: the model
predicts, **proposes** the next batch to test, you run it, retrain, and repeat.

The proposal balances **exploitation** (test the predicted-best) against
**exploration** (test where the model is uncertain). **Bayesian optimization**
formalizes this with an acquisition function over a surrogate that yields a
predictive mean $\mu(x)$ and uncertainty $\sigma(x)$:

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

Each cycle should improve the best candidate with diminishing returns, making
**cost per cycle** the binding constraint — exactly the budget you scoped in the
plan.

**Next:** quantifying how much to trust each prediction.
""",
        ),
        _t(
            "Uncertainty quantification and decision risk",
            "12 min",
            r"""# Uncertainty quantification and decision risk

A point prediction is not enough to spend synthesis budget on; you need to know
how *confident* the model is. **Uncertainty quantification (UQ)** separates
**aleatoric** uncertainty (irreducible assay noise) from **epistemic**
uncertainty (the model not having seen similar chemistry).

Practical tools: **deep ensembles** (variance across independently trained
models), **Monte Carlo dropout**, and **conformal prediction**, which yields
calibrated prediction intervals with a guaranteed coverage rate. Well-calibrated
uncertainty grows for molecules far from the training data — and those should be
explored cautiously or de-prioritized.

```plot
{"title": "Epistemic uncertainty grows away from training data", "xLabel": "distance from training data", "yLabel": "predicted uncertainty", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "uncertainty", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  Pred[Prediction] --> UQ[Uncertainty estimate]
  UQ --> Cal{Calibrated + confident?}
  Cal -->|yes| Act[Advance candidate]
  Cal -->|no| Hold[Gather more data]
```

Decisions should weigh predicted value against its uncertainty — a slightly less
potent but well-characterized candidate often beats a high-risk one with a wide
interval.

**Next:** assembling the decision dossier that ends the project.
""",
        ),
        _t(
            "Assembling the decision dossier",
            "13 min",
            r"""# Assembling the decision dossier

The project ends not with a model but with a **decision** — and a **dossier**
that justifies it to chemists, biologists and reviewers. The dossier carries
every candidate forward with its full evidence chain: predicted potency and
uncertainty, docking pose and key interactions, MD stability, free-energy
ranking, ADMET profile, selectivity, synthetic accessibility and cost.

Because no candidate wins on every axis, you reason over a **Pareto front** of
non-dominated trade-offs and often summarize with a **desirability function**

$$D = \left(\prod_i d_i\right)^{1/n}$$

the geometric mean of per-property desirabilities $d_i \in [0,1]$, so any zero
kills the candidate and balance is enforced.

```mermaid
flowchart LR
  C[Final candidates] --> E[Evidence: potency, MD, FEP, ADMET]
  E --> D[Desirability D]
  D --> Pareto[Pareto-optimal set]
  Pareto --> Rec[Ranked recommendation]
  Rec --> Go{Go / no-go gate}
```

```plot
{"title": "Pareto front: potency vs developability trade-off", "xLabel": "potency (norm.)", "yLabel": "max developability", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-x^2", "label": "Pareto front", "color": "#2563eb"}]}
```

A good dossier is honest about what the AI does and does not know: it states the
applicability domain, the uncertainty, and the assumptions — so the next team
can act, not just admire. AI compresses the early funnel; the dossier hands the
decision back to people.

**Next:** check your knowledge.
""",
        ),
        _quiz(),
    ),
)


CAPSTONE_AI_DRUG_DESIGN_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["CAPSTONE_AI_DRUG_DESIGN_COURSES"]
