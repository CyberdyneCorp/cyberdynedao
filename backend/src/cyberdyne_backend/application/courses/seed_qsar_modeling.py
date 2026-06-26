"""QSAR & Pharmacophore Modeling track: Basics -> Intermediate -> Advanced.

A three-level track on quantitative structure-activity relationships: from
biological activity, molecular descriptors and the SAR concept, through linear
(Hansch, Free-Wilson) and nonlinear/machine-learning QSAR, to 3D-QSAR (CoMFA,
CoMSIA), pharmacophore modeling, rigorous validation and the applicability
domain. Lessons are `text` with LaTeX, interactive ```plot blocks (dose
response, Hansch parabolas, learning curves, ROC) and ```mermaid diagrams for
workflows, descriptor families and validation pipelines.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── QSAR & Pharmacophore Modeling — Basics ───────────────────────────────────

_BASICS = SeedCourse(
    slug="qsar-modeling-basics",
    title="QSAR & Pharmacophore Modeling — Basics",
    description=(
        "The intuition behind structure-activity relationships: what biological "
        "activity is and how we measure it, why we convert potency to pIC50, the "
        "molecular descriptors that encode structure as numbers, the SAR concept "
        "and activity cliffs, and a first linear QSAR model. Interactive plots "
        "and workflow diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is QSAR?",
            "11 min",
            r"""
# What is QSAR?

A **quantitative structure-activity relationship (QSAR)** is a mathematical model
that connects the *structure* of a molecule, encoded as numerical **descriptors**,
to a measured **property or biological activity**. The founding idea, due to
Corwin Hansch in the 1960s, is simple but powerful: if similar molecules have
similar activities, then activity must be a function of measurable structural
features, and we can *fit* that function and use it to predict untested compounds.

Formally we seek $A = f(D_1, D_2, \dots, D_n)$, where $A$ is activity and the
$D_i$ are descriptors (lipophilicity, electronic, steric, topological). A QSAR
model lets a medicinal chemist prioritize which analogues to synthesize, saving
time and reagents — virtual screening before bench work.

```plot
{"title": "Activity rises then falls with lipophilicity (Hansch)", "xLabel": "logP", "yLabel": "relative activity", "xRange": [-2, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.18*(x-3)^2)", "label": "activity", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  STR["Molecular structure"] --> DESC["Numerical descriptors"]
  DESC --> MODEL["QSAR model f(D)"]
  MODEL --> PRED["Predicted activity"]
  PRED --> RANK["Rank/prioritize analogues"]
```

**Next:** how biological activity is actually measured and expressed.
""",
        ),
        _t(
            "Measuring biological activity",
            "12 min",
            r"""
# Measuring biological activity

QSAR needs a **dependent variable**: a clean, comparable measure of potency.
The most common come from dose-response assays. The half-maximal **IC50** is the
concentration that inhibits 50% of a target's activity; **EC50** is the analogous
concentration for an agonist response; **Ki** is an inhibition constant corrected
for substrate competition. Binding affinity is often reported as the dissociation
constant **Kd**.

A dose-response curve plotting effect against **log concentration** is sigmoidal,
described by the Hill equation $E = \frac{E_{max}[L]^n}{EC_{50}^n + [L]^n}$, where
$n$ is the Hill slope. The midpoint of the sigmoid is the EC50/IC50.

```plot
{"title": "Sigmoidal dose-response curve", "xLabel": "log concentration", "yLabel": "fractional response", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#16a34a"}]}
```

Crucially, QSAR almost never models IC50 directly. Potencies span orders of
magnitude, so we use the **negative log molar potency**, $pIC_{50} = -\log_{10}(IC_{50})$
(with IC50 in molar units). This spreads the data evenly, makes it additive in
free-energy terms, and turns a multiplicative scale into a linear one suitable
for regression.

```mermaid
flowchart LR
  ASSAY["Dose-response assay"] --> IC["IC50 / EC50 / Ki"]
  IC --> PLOG["pIC50 = -log10(IC50)"]
  PLOG --> Y["QSAR response variable"]
```

**Next:** turning a molecule into the numbers a model can read.
""",
        ),
        _t(
            "Molecular descriptors",
            "13 min",
            r"""
# Molecular descriptors

A **descriptor** is a number computed from a molecule that captures some aspect
of its structure. Descriptors are the *independent variables* of QSAR, and the
classic Hansch scheme groups them into three physicochemical families:

- **Lipophilic (hydrophobic):** logP, the Hansch $\pi$ substituent constant.
  Governs membrane crossing and hydrophobic binding.
- **Electronic:** Hammett $\sigma$ constants, partial charges, dipole moment,
  HOMO/LUMO energies. Govern reactivity and electrostatic interactions.
- **Steric:** Taft $E_s$, molar refractivity (MR), molecular volume. Govern
  shape complementarity and fit in the binding pocket.

Beyond these, **2D topological** descriptors (connectivity indices, the number
of rotatable bonds, topological polar surface area) and **structural keys /
fingerprints** (e.g. ECFP/Morgan, MACCS) encode substructure presence. Modern
toolkits — RDKit, Mordred, PaDEL, DRAGON — compute thousands.

Descriptor count grows quickly with structural complexity, so feature selection
matters:

```plot
{"title": "Available descriptors grow with structural complexity", "xLabel": "structural complexity", "yLabel": "descriptor count (x100)", "xRange": [0, 10], "yRange": [0, 21], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "descriptor count", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  DESC["Descriptors"] --> LIP["Lipophilic: logP, pi"]
  DESC --> ELE["Electronic: sigma, charges, HOMO/LUMO"]
  DESC --> STE["Steric: MR, volume, Es"]
  DESC --> TOP["Topological: TPSA, connectivity"]
  DESC --> FP["Fingerprints: ECFP, MACCS"]
```

**Next:** the SAR concept and what makes structure and activity track together.
""",
        ),
        _t(
            "The SAR concept and activity cliffs",
            "12 min",
            r"""
# The SAR concept and activity cliffs

A **structure-activity relationship (SAR)** is the qualitative observation that
changing a molecule's structure changes its activity in a systematic way: adding
a methyl boosts potency, swapping a chlorine for fluorine reduces it, and so on.
SAR is the conceptual parent of QSAR — QSAR makes the relationship *quantitative*.

The whole enterprise rests on the **similar property principle**: structurally
similar molecules tend to have similar activities. Plot activity against a
similarity axis and most pairs cluster along a smooth trend.

But the principle has dramatic exceptions called **activity cliffs**: pairs of
very similar molecules with very *different* activities. A single small change —
a hydrogen for a chlorine at one position — can swing potency 100-fold. Cliffs
are where SAR is most informative (they pinpoint critical interactions) and where
QSAR models fail hardest, because the smoothness assumption breaks.

```plot
{"title": "Smooth SAR trend with an activity cliff region", "xLabel": "structural similarity to lead", "yLabel": "pIC50", "xRange": [0, 10], "yRange": [4, 9], "grid": true, "functions": [{"expr": "4+0.4*x", "label": "smooth SAR", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  CHG["Small structural change"] --> SMOOTH["Smooth SAR: similar activity"]
  CHG --> CLIFF["Activity cliff: large activity jump"]
  CLIFF --> KEY["Reveals a key interaction"]
```

**Next:** matched molecular pairs, a systematic way to read SAR.
""",
        ),
        _t(
            "Matched molecular pairs",
            "11 min",
            r"""
# Matched molecular pairs

A **matched molecular pair (MMP)** is two molecules that differ by a single,
well-defined structural transformation — for example, replacing an H by a methyl,
or an ester by an amide — while the rest of the molecule (the *context*) stays
fixed. By comparing the property values of many such pairs sharing the *same*
transformation, we can attribute the average property change to that one edit.

MMP analysis is the data-mining engine behind much modern SAR. Pool every
H→Cl pair in a dataset and the distribution of $\Delta pIC_{50}$ tells you, on
average, what a chlorine does to potency in that series. It separates the *signal*
of a transformation from molecule-to-molecule noise, and it surfaces activity
cliffs automatically (transformations with a wide, bimodal $\Delta$ distribution).

```plot
{"title": "Distribution of activity change for one transformation", "xLabel": "delta pIC50 bin", "yLabel": "relative frequency", "xRange": [-4, 4], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-(x-1)^2)", "label": "H to Cl pairs", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  DB["Compound dataset"] --> FRAG["Fragment / index molecules"]
  FRAG --> PAIR["Find pairs differing by one edit"]
  PAIR --> DELTA["Aggregate delta-property per transformation"]
  DELTA --> RULE["SAR transformation rules"]
```

**Next:** assembling descriptors and activity into your first linear QSAR model.
""",
        ),
        _t(
            "A first linear QSAR model",
            "13 min",
            r"""
# A first linear QSAR model

The simplest QSAR is **multiple linear regression (MLR)**: model activity as a
weighted sum of descriptors,
$$pIC_{50} = c_0 + c_1 D_1 + c_2 D_2 + \dots + c_n D_n.$$
We fit the coefficients $c_i$ by **least squares**, minimizing the sum of squared
residuals between predicted and observed activity. The coefficients are
interpretable: a positive $c_i$ means increasing that descriptor raises potency.

Fit quality is summarized by the coefficient of determination
$$R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2},$$
which lies between 0 and 1; higher is a tighter fit. A good model hugs the
identity line on an observed-vs-predicted plot:

```plot
{"title": "Observed vs predicted activity (ideal model)", "xLabel": "predicted pIC50", "yLabel": "observed pIC50", "xRange": [4, 9], "yRange": [4, 9], "grid": true, "functions": [{"expr": "x", "label": "y = x (perfect)", "color": "#2563eb"}]}
```

A key caution: a high $R^2$ only proves the model *fits* the data it saw, not
that it *predicts* new compounds. With many descriptors and few compounds you can
fit noise — **overfitting**. That is why the next course is all about honest
validation.

```mermaid
flowchart LR
  D["Descriptor matrix X"] --> FIT["Least-squares fit"]
  Y["Activities y"] --> FIT
  FIT --> COEF["Coefficients c_i"]
  COEF --> R2["Report R^2, residuals"]
```

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)


# ── QSAR & Pharmacophore Modeling — Intermediate ─────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="qsar-modeling-intermediate",
    title="QSAR & Pharmacophore Modeling — Intermediate",
    description=(
        "The core quantitative methods of QSAR: the Hansch and Free-Wilson "
        "approaches, taming collinear descriptors with PLS regression, "
        "regularization and feature selection, nonlinear and machine-learning "
        "models (random forests, SVMs, neural nets), and rigorous internal and "
        "external validation. Interactive plots and method diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Hansch and Free-Wilson analysis",
            "13 min",
            r"""
# Hansch and Free-Wilson analysis

The two classical linear QSAR frameworks take opposite philosophies.

The **Hansch (linear free-energy) approach** uses *continuous physicochemical*
descriptors. Its signature equation captures a parabolic dependence on
lipophilicity, because activity rises with membrane penetration then falls when
the compound is too lipophilic to leave the lipid phase:
$$pIC_{50} = a(\log P) - b(\log P)^2 + \rho\sigma + c.$$
The optimum $\log P^{*} = a/2b$ is where activity peaks.

```plot
{"title": "Hansch parabola in logP", "xLabel": "logP", "yLabel": "pIC50", "xRange": [-1, 7], "yRange": [4, 9], "grid": true, "functions": [{"expr": "8.5 - 0.3*(x-3)^2", "label": "pIC50", "color": "#2563eb"}]}
```

The **Free-Wilson (de novo) approach** instead treats activity as an additive
sum of *substituent contributions*: each substituent at each position adds a
fixed increment $a_{ij}$ to the activity of a base scaffold,
$pIC_{50} = \mu + \sum a_{ij}$. It needs no external descriptors but cannot
predict substituents it has never seen. The two views are complementary, and the
**mixed Hansch-Free-Wilson** model combines them.

```mermaid
flowchart TB
  CLS["Classical linear QSAR"] --> H["Hansch: physicochemical (logP, sigma, Es)"]
  CLS --> FW["Free-Wilson: additive substituent constants"]
  H --> MIX["Mixed Hansch-Free-Wilson"]
  FW --> MIX
```

**Next:** what to do when descriptors are correlated and outnumber compounds.
""",
        ),
        _t(
            "Collinearity and PLS regression",
            "13 min",
            r"""
# Collinearity and PLS regression

Real descriptor sets are **collinear** (logP, MR and volume all rise together)
and often number more variables than compounds ($p > n$). Ordinary least squares
then becomes unstable or undefined: tiny data changes swing the coefficients
wildly, and the inverse $(X^{T}X)^{-1}$ is ill-conditioned.

**Partial least squares (PLS) regression** is the workhorse cure, and the engine
of 3D-QSAR. Instead of regressing on the raw descriptors, PLS extracts a few
orthogonal **latent variables** (components) that are linear combinations of
descriptors chosen to maximize covariance with the *activity*. Regressing on a
handful of components sidesteps collinearity and the $p>n$ problem.

The number of components is the key hyperparameter. Predictive performance,
measured by cross-validated $q^2$, rises then falls as components are added —
too few underfit, too many refit noise:

```plot
{"title": "Cross-validated q^2 vs number of PLS components", "xLabel": "number of components", "yLabel": "q^2", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.2*(x-4)^2)", "label": "q^2", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  X["Collinear descriptors (p > n)"] --> LV["Extract latent components"]
  Y["Activity"] --> LV
  LV --> REG["Regress on few components"]
  REG --> Q2["Choose components by max q^2"]
```

**Next:** regularization and choosing the descriptors that matter.
""",
        ),
        _t(
            "Regularization and feature selection",
            "12 min",
            r"""
# Regularization and feature selection

Another way to control too-many-descriptors is to **penalize** large coefficients.
**Ridge regression** adds an $L_2$ penalty $\lambda\sum c_j^2$ to the least-squares
loss, shrinking coefficients toward zero and stabilizing the fit. **Lasso** uses
an $L_1$ penalty $\lambda\sum |c_j|$, which drives many coefficients exactly to
zero — performing **feature selection** automatically. **Elastic net** blends
both penalties.

The penalty strength $\lambda$ controls the bias-variance trade-off. As $\lambda$
grows, training error rises (more bias) but the model generalizes better up to a
point; tune $\lambda$ by cross-validation. The hallmark U-shaped test-error curve:

```plot
{"title": "Test error vs regularization strength", "xLabel": "log lambda", "yLabel": "prediction error", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "0.2 + 0.08*(x-5)^2", "label": "test error", "color": "#dc2626"}]}
```

Explicit selection methods — stepwise regression, genetic algorithms, recursive
feature elimination — search descriptor subsets directly. The goal is a
*parsimonious* model: the fewest interpretable descriptors that predict well, with
a sensible compounds-to-descriptors ratio (a common rule of thumb is at least 5
compounds per descriptor).

```mermaid
flowchart TB
  MANY["Many descriptors"] --> RIDGE["Ridge (L2): shrink"]
  MANY --> LASSO["Lasso (L1): shrink + select"]
  MANY --> WRAP["Wrapper: GA, RFE, stepwise"]
  RIDGE --> CV["Tune by cross-validation"]
  LASSO --> CV
  WRAP --> CV
```

**Next:** when straight lines are not enough — nonlinear and ML models.
""",
        ),
        _t(
            "Nonlinear and machine-learning QSAR",
            "13 min",
            r"""
# Nonlinear and machine-learning QSAR

Many structure-activity relationships are genuinely **nonlinear**, and modern
QSAR reaches for machine learning. **Random forests** average many decision trees
grown on bootstrap samples and random descriptor subsets; they are robust,
handle interactions and collinearity gracefully, and rank descriptor importance.
**Gradient-boosted trees** (XGBoost, LightGBM) often top benchmark leaderboards.

**Support vector machines (SVMs)** with a radial-basis kernel fit smooth
nonlinear surfaces by mapping descriptors into a high-dimensional space.
**Artificial neural networks** — and, for molecular graphs, **graph neural
networks (GNNs)** that learn descriptors directly from the bonded structure —
capture complex patterns when data are plentiful.

The catch is the **bias-variance trade-off**: flexible models can chase noise.
Performance typically improves with more training data (the learning curve) but
plateaus, and flexibility must be matched to dataset size:

```plot
{"title": "Learning curve: accuracy vs training-set size", "xLabel": "training-set size (x100)", "yLabel": "predictive accuracy", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - exp(-0.5*x)", "label": "accuracy", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  ML["Nonlinear QSAR"] --> RF["Random forest / boosting"]
  ML --> SVM["SVM (RBF kernel)"]
  ML --> NN["Neural nets / GNN"]
  RF --> TRADE["Match flexibility to data size"]
  SVM --> TRADE
  NN --> TRADE
```

**Next:** the validation that separates real models from lucky fits.
""",
        ),
        _t(
            "Internal validation and cross-validation",
            "12 min",
            r"""
# Internal validation and cross-validation

A high training $R^2$ proves nothing about prediction. **Internal validation**
estimates predictive power using only the training set. The standard tool is
**k-fold cross-validation**: split the data into k parts, train on k-1 and predict
the held-out part, rotate, and aggregate. **Leave-one-out (LOO)** is the extreme
$k=n$ case.

The cross-validated metric is $q^2$ (often $Q^2$):
$$q^2 = 1 - \frac{\sum (y_i - \hat{y}_{i,\,\text{pred}})^2}{\sum (y_i - \bar{y})^2},$$
computed from *predictions made on held-out points*. A model is generally
considered acceptable only when $q^2 > 0.5$; the gap between $R^2$ and $q^2$
exposes overfitting — a large gap is a red flag.

```plot
{"title": "R^2 keeps rising while q^2 turns down (overfitting)", "xLabel": "model complexity", "yLabel": "score", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - exp(-0.4*x)", "label": "R^2 (fit)", "color": "#2563eb"}, {"expr": "exp(-0.12*(x-4)^2)", "label": "q^2 (predictive)", "color": "#dc2626"}]}
```

Robustness is further checked with **y-randomization** (Y-scrambling): permute the
activities, refit, and confirm the scrambled models are much worse — otherwise the
original fit was chance correlation.

```mermaid
flowchart LR
  DATA["Training set"] --> KF["k-fold split"]
  KF --> CV["Predict held-out folds"]
  CV --> Q2["q^2 > 0.5?"]
  Q2 --> YR["y-randomization sanity check"]
```

**Next:** the gold standard — external validation on truly unseen compounds.
""",
        ),
        _t(
            "External validation and statistics",
            "12 min",
            r"""
# External validation and statistics

Cross-validation can still be optimistic. The **gold standard** is **external
validation**: set aside a **test set** that never touches model building (training,
feature selection or hyperparameter tuning), then measure prediction on it. The
external metric is usually $R^2_{ext}$ (sometimes written $Q^2_{F1/F2/F3}$ in the
OECD-aligned literature).

A trustworthy model satisfies several criteria together — not just one number.
Tropsha's widely used thresholds require $q^2 > 0.5$ and external $R^2 > 0.6$,
with the regression of observed vs predicted passing through the origin (slope
$k$ near 1). Always report error in original units too: the **root mean square
error (RMSE)**
$$RMSE = \sqrt{\frac{1}{n}\sum (y_i - \hat{y}_i)^2}$$
tells you the typical prediction error in pIC50 units, which RMSE shrinks toward
zero as predictions improve.

```plot
{"title": "External RMSE falls as the model improves", "xLabel": "model quality index", "yLabel": "external RMSE (pIC50)", "xRange": [0, 10], "yRange": [0, 1.6], "grid": true, "functions": [{"expr": "1.5*exp(-0.4*x)", "label": "RMSE", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  ALL["Full dataset"] --> SPLIT["Train / external test split"]
  SPLIT --> BUILD["Build model on train only"]
  BUILD --> EXT["Predict external test"]
  EXT --> CRIT["Check q^2 > 0.5, R2_ext > 0.6, slope ~ 1, RMSE"]
```

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)


# ── QSAR & Pharmacophore Modeling — Advanced ─────────────────────────────────

_ADVANCED = SeedCourse(
    slug="qsar-modeling-advanced",
    title="QSAR & Pharmacophore Modeling — Advanced",
    description=(
        "State-of-the-art and applied QSAR: 3D-QSAR with CoMFA and CoMSIA, "
        "pharmacophore modeling and screening, the applicability domain that "
        "bounds reliable prediction, deep learning on molecular graphs, "
        "interpretability and matched-pair attribution, and regulatory-grade "
        "modeling under the OECD principles. Interactive plots and pipeline "
        "diagrams throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "3D-QSAR: CoMFA and CoMSIA",
            "14 min",
            r"""
# 3D-QSAR: CoMFA and CoMSIA

**3D-QSAR** correlates activity with the three-dimensional fields a molecule
projects, rather than scalar descriptors. **Comparative Molecular Field Analysis
(CoMFA)**, introduced by Cramer in 1988, aligns a series of molecules in a common
frame, places them in a 3D grid, and at each grid point computes **steric**
(Lennard-Jones) and **electrostatic** (Coulombic) interaction energies with a
probe atom. The thousands of grid energies become descriptors, and **PLS**
regresses them against activity.

**CoMSIA** (Comparative Molecular Similarity Indices Analysis) replaces the
steep Lennard-Jones potential with smooth **Gaussian similarity** functions and
adds hydrophobic and hydrogen-bond donor/acceptor fields, avoiding CoMFA's
singularities near atoms. The Gaussian form keeps field values finite and
differentiable everywhere:

```plot
{"title": "CoMSIA Gaussian field vs CoMFA steric singularity", "xLabel": "distance from atom (A)", "yLabel": "field value", "xRange": [0.5, 6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.5*(x-2)^2)", "label": "CoMSIA Gaussian", "color": "#2563eb"}]}
```

Results are displayed as **contour maps** showing where bulk or charge favours or
disfavours activity. The Achilles' heel of 3D-QSAR is **alignment**: poorly
aligned molecules give meaningless fields, so success hinges on a good bioactive
conformation and superposition.

```mermaid
flowchart LR
  SER["Aligned molecule series"] --> GRID["3D grid + probe"]
  GRID --> FIELDS["Steric / electrostatic / HB fields"]
  FIELDS --> PLS["PLS regression"]
  PLS --> CONT["Contour maps + prediction"]
```

**Next:** abstracting the binding requirements into a pharmacophore.
""",
        ),
        _t(
            "Pharmacophore modeling",
            "13 min",
            r"""
# Pharmacophore modeling

A **pharmacophore** is the abstract spatial arrangement of **features** required
for a molecule to interact with a target — not specific atoms, but the *pattern*
of an H-bond donor here, an aromatic ring there, a hydrophobic group at a defined
distance. The IUPAC definition emphasizes it is the ensemble of steric and
electronic features needed to trigger (or block) the biological response.

Models are built two ways. **Ligand-based** pharmacophores align several known
actives (e.g. with Catalyst/HypoGen, PHASE, or LigandScout) and extract the
common feature geometry. **Structure-based** pharmacophores read the features
directly from a protein-ligand complex or an apo binding site.

A finished model is a set of feature spheres with **distance and angle
constraints** plus optional **exclusion volumes** marking forbidden space. As the
geometric tolerance on those constraints tightens, the query becomes more
selective and matches fewer molecules:

```plot
{"title": "Database hits vs pharmacophore match tolerance", "xLabel": "match tolerance (A)", "yLabel": "fraction of database matching", "xRange": [0, 4], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - exp(-1.2*x)", "label": "hit fraction", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  PH["Pharmacophore model"] --> LB["Ligand-based: align actives"]
  PH --> SB["Structure-based: from complex/site"]
  LB --> FEAT["Features: HBD, HBA, aromatic, hydrophobic, charge"]
  SB --> FEAT
  FEAT --> CONS["Distances, angles, exclusion volumes"]
```

**Next:** using a pharmacophore to screen virtual libraries.
""",
        ),
        _t(
            "Pharmacophore-based virtual screening",
            "13 min",
            r"""
# Pharmacophore-based virtual screening

A validated pharmacophore becomes a **3D query** for searching large compound
libraries. Each database molecule must first be expanded into a set of plausible
**conformers** (it is flexible), then tested for whether any conformer can place
its features inside the query's feature spheres — a sub-graph matching problem.
Hits are ranked by geometric fit and feature coverage.

Screening performance is judged by **enrichment**: how much the screen
concentrates known actives near the top of the ranked list versus random. The
**enrichment factor** at the top x% is $EF_{x\%} = \frac{\text{actives found}/N_x}{\text{total actives}/N}$,
and the **ROC curve** (true-positive vs false-positive rate) summarizes ranking
quality; a good screen bows toward the top-left:

```plot
{"title": "ROC curve for a virtual screen", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "screen (AUC > 0.5)", "color": "#2563eb"}]}
```

Pharmacophore screening is fast and interpretable, and is often a *prefilter*
before the slower step of molecular docking, dramatically shrinking the library
that needs expensive scoring.

```mermaid
flowchart LR
  LIB["Compound library"] --> CONF["Generate conformers"]
  CONF --> MATCH["Match to 3D pharmacophore"]
  MATCH --> RANK["Rank by fit / enrichment"]
  RANK --> DOCK["Pass top hits to docking"]
```

**Next:** the boundary inside which predictions can be trusted.
""",
        ),
        _t(
            "The applicability domain",
            "12 min",
            r"""
# The applicability domain

A QSAR model is only reliable for compounds *similar to those it was trained on*.
The **applicability domain (AD)** is the region of descriptor space where
predictions can be trusted; extrapolating outside it gives unreliable numbers no
matter how good the global statistics look. Defining and reporting the AD is one
of the OECD principles for regulatory acceptance.

Several methods bound the domain. The **range/box** method bounds each descriptor;
the **leverage** approach uses the diagonal of the hat matrix $H = X(X^{T}X)^{-1}X^{T}$
and flags compounds above a warning leverage $h^{*} = 3p/n$ in a Williams plot of
standardized residuals vs leverage. **Distance-to-model** (e.g. k-nearest-neighbour
distance in descriptor space) and **probability-density** methods are also common.

Prediction reliability decays as a compound drifts from the training centroid:

```plot
{"title": "Prediction reliability vs distance from training data", "xLabel": "distance to model (descriptor space)", "yLabel": "reliability", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "reliability", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  NEW["New compound"] --> CHK["Inside applicability domain?"]
  CHK -->|"yes"| PRED["Reliable prediction"]
  CHK -->|"no"| FLAG["Flag: extrapolation, low confidence"]
```

**Next:** deep learning that designs and predicts on molecular graphs.
""",
        ),
        _t(
            "Deep learning and generative QSAR",
            "14 min",
            r"""
# Deep learning and generative QSAR

Modern QSAR increasingly *learns the representation*. **Graph neural networks
(GNNs)** — message-passing networks, Chemprop's D-MPNN, attentive FP — treat the
molecule as a graph of atoms and bonds and learn task-specific descriptors end to
end, often outperforming fixed fingerprints when data are abundant. **Transformer**
models pretrained on SMILES/SELFIES (ChemBERTa, MolFormer) bring self-supervised
representation learning to chemistry.

Two ideas stretch data efficiency. **Transfer learning / pretraining** initializes
on millions of unlabeled molecules then fine-tunes on a small activity set.
**Multitask learning** trains one network on many endpoints at once, borrowing
statistical strength across assays. Accuracy improves with data but with
diminishing returns, so pretraining shifts the whole curve upward:

```plot
{"title": "Pretraining lifts the data-efficiency curve", "xLabel": "labeled training data (x100)", "yLabel": "accuracy", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - 0.9*exp(-0.7*x)", "label": "pretrained + fine-tuned", "color": "#16a34a"}, {"expr": "1 - exp(-0.4*x)", "label": "from scratch", "color": "#2563eb"}]}
```

**Generative** models invert QSAR: variational autoencoders, recurrent SMILES
generators and reinforcement-learning agents *design* new molecules optimized for
a predicted activity, closing an autonomous design-make-test-analyze loop.

```mermaid
flowchart LR
  PRE["Pretrain on unlabeled molecules"] --> FT["Fine-tune on activity"]
  FT --> PRED["GNN/transformer prediction"]
  PRED --> GEN["Generative design (VAE/RL)"]
  GEN --> DMTA["Design-Make-Test-Analyze loop"]
```

**Next:** interpreting models and meeting regulatory standards.
""",
        ),
        _t(
            "Interpretability and regulatory QSAR",
            "13 min",
            r"""
# Interpretability and regulatory QSAR

Powerful models are only useful if chemists trust and act on them, and if
regulators accept them. **Interpretability** turns predictions into design
guidance: **SHAP** values and feature-importance scores attribute a prediction
to individual descriptors; **atom/fragment attribution** and attention maps in
GNNs highlight which substructures drive activity; **matched-molecular-pair**
analysis validates that the model's learned transformations match real SAR.

For regulatory use (e.g. REACH read-across, toxicity prediction), a QSAR must
satisfy the **five OECD principles**: a defined endpoint; an unambiguous
algorithm; a defined applicability domain; appropriate measures of goodness-of-fit,
robustness and predictivity; and, where possible, a mechanistic interpretation.
A model that scores well but cannot articulate these is not deployable.

Confidence should also be quantified. **Conformal prediction** and ensemble
variance produce calibrated prediction intervals: as required coverage rises, the
interval widens, making the accuracy-vs-confidence trade-off explicit:

```plot
{"title": "Prediction interval width vs required confidence", "xLabel": "required confidence level", "yLabel": "interval width (pIC50)", "xRange": [0, 1], "yRange": [0, 2.1], "grid": true, "functions": [{"expr": "0.3/(1.02-x)", "label": "interval width", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  MOD["Trained QSAR model"] --> INT["Interpret: SHAP, attribution, MMP"]
  MOD --> OECD["OECD: endpoint, algorithm, AD, stats, mechanism"]
  MOD --> CONF["Conformal / ensemble uncertainty"]
  INT --> DEP["Trusted, deployable, regulatory-grade model"]
  OECD --> DEP
  CONF --> DEP
```

**Next:** test what you have learned.
""",
        ),
        _quiz(),
    ),
)


QSAR_MODELING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["QSAR_MODELING_COURSES"]
