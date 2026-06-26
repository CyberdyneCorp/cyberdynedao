"""ADMET & Toxicity Prediction track: Basics -> Intermediate -> Advanced.

Three courses tracing how absorption, distribution, metabolism, excretion and
toxicity decide whether a molecule survives: from ADME intuition and why drugs
fail, through quantitative solubility/permeability/metabolism models, to hERG,
toxicity prediction and modern in-silico ADMET pipelines. Lessons embed
interactive ```plot blocks (Michaelis-Menten, dose-response, decay, binding)
and ```mermaid diagrams (pathways, classifications, prediction pipelines).
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ──────────────────────────────────────────────────────────────────────
# 1. admet-prediction-basics (Beginner)
# ──────────────────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="admet-prediction-basics",
    title="ADMET & Toxicity Prediction — Basics",
    description=(
        "What ADME means and why so many drug candidates fail. You'll meet the "
        "journey of a molecule through the body — absorption, distribution, "
        "metabolism, excretion — plus toxicity, and build intuition for "
        "drug-likeness rules, solubility, and the concentration-time curve that "
        "ties it all together."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is ADMET and why molecules fail",
            "10 min",
            r"""# What is ADMET and why molecules fail

A molecule can bind its target beautifully in a test tube and still fail as a
drug. To work, it must reach the target in the body at the right concentration,
stay long enough, and not poison the patient. **ADMET** captures these
properties: **A**bsorption, **D**istribution, **M**etabolism, **E**xcretion,
and **T**oxicity.

Historically, poor pharmacokinetics (ADME) caused roughly **40%** of clinical
failures before the 1990s. After the industry began screening ADMET early, that
share dropped — but **toxicity and lack of efficacy** now dominate attrition.
The lesson is the same: failing late is enormously expensive, so predicting
ADMET problems *early* and cheaply is hugely valuable.

```mermaid
flowchart LR
  A[Dose] --> B[Absorption]
  B --> C[Distribution]
  C --> D[Metabolism]
  D --> E[Excretion]
  C --> T[Toxicity?]
  C --> Eff[Reaches target]
```

The core tension: properties that help one ADMET dimension often hurt another.
A greasy molecule crosses membranes well (good absorption) but is poorly soluble
and prone to metabolism. ADMET is the art of balancing these trade-offs so a
molecule is **drug-like**, not just potent.

**Next:** the ADME journey, step by step.
""",
        ),
        _t(
            "The ADME journey through the body",
            "11 min",
            r"""# The ADME journey through the body

Follow an oral drug from tablet to elimination.

**Absorption.** The drug dissolves in the gut and crosses the intestinal
epithelium into the portal blood. Most small-molecule drugs cross by *passive
diffusion*, so lipophilicity and solubility both matter.

**Distribution.** Blood carries the drug to tissues. Much of it binds plasma
proteins (albumin); only the *free* fraction is active. Lipophilic drugs
partition into fat and tissues, giving a large **volume of distribution**.

**Metabolism.** The liver chemically modifies the drug — mostly **cytochrome
P450** enzymes (Phase I) and conjugation (Phase II) — usually making it more
water-soluble for excretion.

**Excretion.** The kidneys filter the drug (and metabolites) into urine; the
liver can excrete into bile. This clears the drug from the body.

```mermaid
flowchart LR
  G[Gut] -->|absorption| Bl[Blood]
  Bl --> Ti[Tissues]
  Bl --> Li[Liver / metabolism]
  Li --> Ki[Kidney]
  Ki --> Ur[Urine]
```

A crucial twist: drug absorbed from the gut passes through the liver *before*
reaching general circulation. This **first-pass metabolism** can destroy much of
an oral dose before it ever acts.

**Next:** the curve that summarises this — concentration over time.
""",
        ),
        _t(
            "The concentration-time curve and key PK parameters",
            "11 min",
            r"""# The concentration-time curve and key PK parameters

Plotting plasma drug concentration against time after a dose gives the central
picture of pharmacokinetics (PK). After an IV bolus, concentration falls roughly
**exponentially** as the body clears the drug — first-order kinetics.

```plot
{"title": "Plasma concentration after IV dose", "xLabel": "Time (h)", "yLabel": "Concentration (mg/L)", "xRange": [0,10], "yRange": [0,11], "grid": true, "functions": [{"expr": "10*exp(-0.5*x)", "label": "C(t) = C0 e^(-kt)", "color": "#2563eb"}]}
```

Key parameters read off this curve:

- **C_max** — peak concentration reached.
- **t_max** — time of the peak (oral dosing).
- **AUC** — area under the curve, total exposure; proportional to dose / clearance.
- **half-life $t_{1/2}$** — time for concentration to halve, $t_{1/2}=\frac{\ln 2}{k}$.
- **Clearance (CL)** — volume of blood cleared per unit time.
- **Volume of distribution $V_d$** — apparent volume the drug occupies.

These link by $CL = k \cdot V_d$ and $t_{1/2}=\frac{0.693 \cdot V_d}{CL}$.
A long half-life allows infrequent dosing; high clearance means the drug
disappears fast and may need frequent dosing or modification.

**Next:** what makes a molecule "drug-like".
""",
        ),
        _t(
            "Drug-likeness and Lipinski's Rule of Five",
            "10 min",
            r"""# Drug-likeness and Lipinski's Rule of Five

In 1997, Christopher Lipinski analysed orally active drugs and noticed that poor
absorption is more likely when a molecule violates **two or more** of four
simple limits — the **Rule of Five** (the numbers are multiples of 5):

- molecular weight **≤ 500** Da
- calculated **logP ≤ 5** (lipophilicity)
- hydrogen-bond **donors ≤ 5**
- hydrogen-bond **acceptors ≤ 10**

The intuition: very large, very greasy, or heavily hydrogen-bonding molecules
struggle to cross membranes passively. Later refinements added **rotatable bonds
≤ 10** and **polar surface area (PSA) ≤ 140 Å²** (Veber's rules) for good oral
bioavailability.

```mermaid
flowchart TB
  M[Molecule] --> R1{MW <= 500?}
  M --> R2{logP <= 5?}
  M --> R3{HBD <= 5?}
  M --> R4{HBA <= 10?}
  R1 --> S[<= 1 violation -> drug-like]
  R2 --> S
  R3 --> S
  R4 --> S
```

These are **filters, not laws**: many successful drugs (antibiotics, natural
products, "beyond Rule of Five" compounds) break them. They are a fast, cheap
first triage in early discovery, not a verdict.

**Next:** why solubility is the gatekeeper of absorption.
""",
        ),
        _t(
            "Solubility, logP and the absorption gatekeeper",
            "10 min",
            r"""# Solubility, logP and the absorption gatekeeper

For an oral drug to be absorbed it must first **dissolve**. A molecule that
never enters solution cannot cross the gut wall, no matter how potent. Aqueous
solubility is therefore the gatekeeper of absorption.

**logP**, the octanol-water partition coefficient, measures lipophilicity. As
logP rises, solubility usually *falls* but membrane permeability *rises* — the
classic ADMET trade-off. A useful sweet spot for oral drugs is roughly
**logP 1–3**.

```plot
{"title": "Fraction absorbed vs lipophilicity (schematic)", "xLabel": "logP", "yLabel": "Relative absorption", "xRange": [0,8], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "permeability-limited rise", "color": "#16a34a"}]}
```

At very high logP, poor solubility drags absorption back down, giving a
bell-shaped real-world relationship. The **Developability Classification System
(DCS)** and the **Biopharmaceutics Classification System (BCS)** group drugs by
solubility and permeability into four classes — Class II (low solubility, high
permeability) being the most common formulation headache.

Tools like RDKit estimate logP (Crippen's **clogP**) and solubility (**ESOL**,
log S) directly from structure, enabling early ranking before any synthesis.

**Next:** test your ADMET basics.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 2. admet-prediction-intermediate (Intermediate)
# ──────────────────────────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="admet-prediction-intermediate",
    title="ADMET & Toxicity Prediction — Intermediate",
    description=(
        "The quantitative core of ADMET modelling. You'll work through "
        "permeability assays and models, enzyme-kinetics metabolism with "
        "Michaelis-Menten and clearance scaling, plasma protein binding, "
        "drug-drug interactions, and how QSAR/QSPR models are built and "
        "validated for ADMET endpoints."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Permeability: Caco-2, PAMPA and predictive models",
            "12 min",
            r"""# Permeability: Caco-2, PAMPA and predictive models

Permeability is how readily a molecule crosses a membrane — the rate-limiting
step in absorption once a drug has dissolved. Two assays dominate.

**Caco-2** uses a monolayer of human colon-derived cells grown on a porous
filter; it expresses transporters and tight junctions, so it captures both
passive diffusion and active transport / efflux. **PAMPA** (Parallel Artificial
Membrane Permeability Assay) is a cell-free lipid membrane measuring *passive*
permeability only — cheaper and higher-throughput.

The readout is **apparent permeability**:

$$P_{app} = \frac{1}{A \cdot C_0}\cdot\frac{dQ}{dt}$$

where $\frac{dQ}{dt}$ is the transport rate, $A$ the membrane area and $C_0$ the
initial donor concentration. High $P_{app}$ (> ~10⁻⁶ cm/s) predicts good
absorption.

```mermaid
flowchart LR
  D[Donor side] -->|passive| M[Membrane / cells]
  M --> R[Receiver side]
  M -->|efflux P-gp| D
```

Comparing apical-to-basolateral vs basolateral-to-apical flux gives an **efflux
ratio**; a ratio > 2 flags **P-glycoprotein (P-gp)** efflux, a common reason a
permeable molecule still absorbs poorly. In-silico models predict $\log P_{app}$
from descriptors (PSA, logD, H-bonding), enabling virtual screening.

**Next:** enzyme kinetics of metabolism.
""",
        ),
        _t(
            "Metabolism kinetics: Michaelis-Menten and clearance",
            "12 min",
            r"""# Metabolism kinetics: Michaelis-Menten and clearance

Most drug metabolism is enzyme-catalysed and follows **Michaelis-Menten**
kinetics. The reaction rate $v$ depends on substrate (drug) concentration $[S]$:

$$v=\frac{V_{max}[S]}{K_m+[S]}$$

where $V_{max}$ is the maximum rate and $K_m$ the concentration giving half of
$V_{max}$. At low $[S]$ (typical of drugs in vivo), $v\approx\frac{V_{max}}{K_m}[S]$
— first-order, linear in concentration.

```plot
{"title": "Michaelis-Menten metabolic rate", "xLabel": "Drug concentration [S]", "yLabel": "Rate v", "xRange": [0,20], "yRange": [0,9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

The **intrinsic clearance** is $CL_{int}=\frac{V_{max}}{K_m}$ in the linear
regime. Microsomal or hepatocyte assays measure $CL_{int}$, then **IVIVE**
(in-vitro-to-in-vivo extrapolation) scales it to whole-liver hepatic clearance
$CL_H$ using the well-stirred model:

$$CL_H=\frac{Q_H\cdot f_u\cdot CL_{int}}{Q_H+f_u\cdot CL_{int}}$$

with hepatic blood flow $Q_H$ and unbound fraction $f_u$. When clearance is
limited by $Q_H$, the drug is "high-extraction"; when limited by $CL_{int}$, it
is "low-extraction" and sensitive to enzyme inhibition.

**Next:** the P450 enzymes doing the work.
""",
        ),
        _t(
            "Cytochrome P450 and drug-drug interactions",
            "11 min",
            r"""# Cytochrome P450 and drug-drug interactions

The **cytochrome P450 (CYP)** superfamily performs most Phase I oxidative
metabolism. A handful of isoforms handle the majority of drugs — **CYP3A4**
(~50%), **CYP2D6**, **CYP2C9**, **CYP2C19** and **CYP1A2**.

Trouble arises when drugs **inhibit** or **induce** these enzymes:

- An **inhibitor** (e.g. ketoconazole on CYP3A4) slows metabolism of co-dosed
  substrates, raising their levels — possibly to toxic concentrations.
- An **inducer** (e.g. rifampicin) increases enzyme expression, lowering
  substrate levels and risking loss of efficacy.

These are **drug-drug interactions (DDIs)**, a major safety concern.

```mermaid
flowchart TB
  S[Substrate drug] --> C[CYP3A4]
  I[Inhibitor] -.blocks.-> C
  N[Inducer] -.upregulates.-> C
  C --> M[Metabolites]
```

Inhibition is quantified by $K_i$ (or IC50); the predicted interaction scales
with $\frac{[I]}{K_i}$. **Pharmacogenomics** adds a layer: CYP2D6 has poor-,
intermediate-, extensive- and ultrarapid-metabolizer genotypes, so the same dose
behaves very differently between patients. ML classifiers (e.g. trained on
PubChem CYP-inhibition bioassays) predict isoform inhibition directly from
structure to flag DDI risk early.

**Next:** how much drug is actually free to act.
""",
        ),
        _t(
            "Plasma protein binding and the free drug hypothesis",
            "10 min",
            r"""# Plasma protein binding and the free drug hypothesis

Only **unbound** drug can cross membranes, bind targets, and be cleared. Much of
a drug in blood is reversibly bound to plasma proteins — mainly **albumin**
(acids) and **α1-acid glycoprotein** (bases). The **fraction unbound** is

$$f_u=\frac{C_{free}}{C_{total}}$$

The **free drug hypothesis** states that at steady state the unbound
concentration in plasma equals that at the site of action, so $f_u$ — not total
concentration — drives both efficacy and clearance.

```plot
{"title": "Bound fraction vs binding affinity (saturable)", "xLabel": "Protein affinity (relative)", "yLabel": "Fraction bound", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturable binding", "color": "#dc2626"}]}
```

Binding is measured by **equilibrium dialysis** or ultrafiltration. A highly
bound drug (e.g. $f_u = 0.01$) has only 1% free, but this does **not**
automatically mean low efficacy — what matters is the absolute free
concentration. Importantly, optimizing a molecule for "lower protein binding"
alone is usually a red herring; binding and clearance co-vary so that free
exposure often stays similar. Predictive models estimate $f_u$ from
lipophilicity and charge, since acidic, lipophilic drugs bind albumin strongly.

**Next:** building QSAR/QSPR models for ADMET.
""",
        ),
        _t(
            "Building and validating QSAR/QSPR models",
            "12 min",
            r"""# Building and validating QSAR/QSPR models

ADMET endpoints (solubility, $P_{app}$, $CL_{int}$, CYP inhibition) are
predicted by **QSPR/QSAR** models that map molecular structure to a property.
The workflow:

1. **Curate** measured data (e.g. ChEMBL, public ADME sets), removing duplicates
   and errors.
2. **Featurize** molecules — descriptors (MW, logP, PSA), fingerprints (ECFP), or
   learned graph features.
3. **Train** a regressor/classifier (random forest, gradient boosting, neural net).
4. **Validate** rigorously.

```mermaid
flowchart LR
  D[Curated data] --> F[Featurize]
  F --> Tr[Train model]
  Tr --> V[Validate]
  V --> P[Predict new molecules]
```

Validation is where models live or die. Random train/test splits **leak**
similar molecules between sets and overstate performance; use **scaffold
splits** or **time splits** to mimic real prospective use. Report regression
metrics ($R^2$, RMSE) or classification metrics (ROC-AUC, MCC), and always
quote an **applicability domain** — predictions for molecules unlike the
training set are unreliable.

```plot
{"title": "Learning curve: error vs training size", "xLabel": "Training examples (x1000)", "yLabel": "Test error", "xRange": [0.5,10], "yRange": [0,2], "grid": true, "functions": [{"expr": "1.5*exp(-0.4*x)+0.2", "label": "test error", "color": "#16a34a"}]}
```

More data helps, but with diminishing returns; data *quality and diversity*
often beat raw quantity for ADMET.

**Next:** test your quantitative ADMET skills.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 3. admet-prediction-advanced (Advanced)
# ──────────────────────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="admet-prediction-advanced",
    title="ADMET & Toxicity Prediction — Advanced",
    description=(
        "State-of-the-art toxicity and ADMET prediction. You'll cover cardiac "
        "hERG liability, hepatotoxicity and structural alerts, deep-learning "
        "models (graph neural nets, multitask, uncertainty), PBPK simulation, "
        "and how production in-silico ADMET pipelines integrate these to triage "
        "molecules before synthesis."
    ),
    level="Advanced",
    lessons=(
        _t(
            "hERG and cardiotoxicity prediction",
            "12 min",
            r"""# hERG and cardiotoxicity prediction

The **hERG** potassium channel (encoded by *KCNH2*) carries the cardiac
repolarizing current I_Kr. Drugs that block hERG prolong the **QT interval**,
risking the lethal arrhythmia **torsades de pointes**. hERG liability has caused
high-profile withdrawals (terfenadine, cisapride), so it is a mandatory safety
endpoint (ICH S7B / the newer CiPA initiative).

The channel's large, aromatic-lined inner cavity binds many basic, lipophilic
drugs — a broad pharmacophore that makes hERG block frustratingly common. Risk
is usually expressed as an **IC50** (potency of block), and the **safety margin**
is the ratio of hERG IC50 to the free therapeutic plasma concentration; margins
below ~30-fold raise concern.

```plot
{"title": "hERG block: fraction inhibited vs concentration", "xLabel": "log[drug] (relative)", "yLabel": "Fraction blocked", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "sigmoid concentration-response", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  D[Drug] --> H[hERG block]
  H --> Q[QT prolongation]
  Q --> T[Torsades risk]
```

Classifiers (random forests, GNNs trained on hERG bioactivity data) predict
block from structure; medicinal chemists then mitigate it by reducing basicity
(lowering pKa) or lipophilicity, or by disrupting the cation-π / hydrophobic
interactions that drive binding.

**Next:** hepatotoxicity and structural alerts.
""",
        ),
        _t(
            "Hepatotoxicity, mutagenicity and structural alerts",
            "12 min",
            r"""# Hepatotoxicity, mutagenicity and structural alerts

The liver concentrates and metabolizes drugs, so it is the most common site of
drug toxicity. **Drug-induced liver injury (DILI)** is a leading cause of
withdrawals and is hard to predict because it is often **idiosyncratic** —
dependent on reactive metabolites, immune response and patient factors.

A key mechanism is bioactivation to a **reactive metabolite** that covalently
binds proteins or DNA. Certain substructures — **structural alerts** (or
"toxicophores") — flag this risk: nitroaromatics, anilines, michael acceptors,
epoxides, quinones. Expert systems like **DEREK** encode such alerts as rules.

```mermaid
flowchart TB
  D[Drug] --> B[Bioactivation / CYP]
  B --> RM[Reactive metabolite]
  RM --> Cov[Covalent protein binding]
  RM --> DNA[DNA adduct -> mutagenicity]
  Cov --> Tox[Hepatotoxicity]
```

For **mutagenicity**, the **Ames test** (bacterial reverse mutation) is the
regulatory standard; **ICH M7** allows two complementary **(Q)SAR** systems
(one expert/rule-based, one statistical) to assess impurities in place of
testing. Tools such as **Toxtree** and **VEGA** implement these.

Caveat: structural alerts are *sensitive but not specific* — many safe drugs
contain alerting groups that are detoxified before harm. Alerts prioritize
follow-up; they are not convictions, and context (dose, exposure, metabolism)
decides actual risk.

**Next:** deep learning for toxicity and ADMET.
""",
        ),
        _t(
            "Deep learning for ADMET: graph nets, multitask, uncertainty",
            "13 min",
            r"""# Deep learning for ADMET: graph nets, multitask, uncertainty

Classical QSAR uses fixed descriptors; modern models *learn* representations.
**Graph neural networks (GNNs)** treat a molecule as a graph — atoms as nodes,
bonds as edges — and pass messages between neighbours to build features tuned to
the endpoint. **Directed message-passing** networks (e.g. **Chemprop**) are a
strong, widely used baseline for ADMET.

**Multitask learning** trains one network to predict many ADMET endpoints at
once. Because endpoints are correlated (logP, solubility, permeability) and data
is scarce per task, sharing a representation improves data-poor tasks — a result
popularized by the Tox21 / DeepTox work.

```mermaid
flowchart LR
  G[Molecular graph] --> E[Message passing]
  E --> R[Shared embedding]
  R --> T1[Solubility]
  R --> T2[hERG]
  R --> T3[CYP inhibition]
```

Crucially, predictions need **uncertainty**. A model must say "I don't know" for
molecules outside its applicability domain. Approaches include deep **ensembles**,
**Monte-Carlo dropout**, and **conformal prediction**, which gives calibrated
prediction intervals with coverage guarantees.

```plot
{"title": "Calibration: predicted vs true error", "xLabel": "Predicted uncertainty", "yLabel": "Observed error", "xRange": [0,5], "yRange": [0,5], "grid": true, "functions": [{"expr": "x", "label": "perfect calibration", "color": "#16a34a"}]}
```

Benchmarks like **MoleculeNet** and **TDC** (Therapeutics Data Commons)
standardize ADMET datasets and scaffold splits so methods can be compared fairly.

**Next:** PBPK — mechanistic whole-body simulation.
""",
        ),
        _t(
            "PBPK modelling: mechanistic whole-body simulation",
            "12 min",
            r"""# PBPK modelling: mechanistic whole-body simulation

Where QSAR predicts a single property, **physiologically based pharmacokinetic
(PBPK)** models simulate the *whole concentration-time course* mechanistically.
The body is a set of compartments — liver, gut, kidney, fat, brain — connected by
blood flow, each described by a mass-balance differential equation:

$$V_t\frac{dC_t}{dt}=Q_t\left(C_{art}-\frac{C_t}{K_{p,t}}\right)-CL_t\,C_t$$

with tissue volume $V_t$, blood flow $Q_t$, tissue:plasma partition $K_{p,t}$ and
tissue clearance $CL_t$. The inputs are physiology (from databases) plus
drug-specific ADMET parameters — often predicted in silico ($f_u$, $CL_{int}$,
$P_{app}$, logP).

```mermaid
flowchart TB
  G[Gut] --> Li[Liver]
  Li --> Bl[Blood pool]
  Bl --> Ki[Kidney]
  Bl --> Fa[Fat]
  Bl --> Br[Brain]
  Ki --> Ur[Urine]
```

The payoff: PBPK predicts plasma curves for new doses, routes, populations
(pediatric, hepatic-impaired) and **DDIs** without new clinical trials.

```plot
{"title": "PBPK oral profile: absorption then elimination", "xLabel": "Time (h)", "yLabel": "Concentration", "xRange": [0,12], "yRange": [0,5], "grid": true, "functions": [{"expr": "5*(exp(-0.3*x)-exp(-1.2*x))", "label": "oral one-compartment", "color": "#2563eb"}]}
```

Regulators (FDA, EMA) now accept PBPK in submissions, especially for DDI and
special-population dosing. Platforms include **Simcyp**, **GastroPlus** and the
open-source **PK-Sim/OSP**.

**Next:** assembling a full in-silico ADMET pipeline.
""",
        ),
        _t(
            "In-silico ADMET pipelines and design triage",
            "12 min",
            r"""# In-silico ADMET pipelines and design triage

In modern discovery, ADMET prediction is woven into the **design-make-test-
analyze (DMTA)** loop *before* synthesis. A production pipeline scores every
proposed molecule across many endpoints and surfaces trade-offs to the chemist.

```mermaid
flowchart LR
  D[Designed molecule] --> Filt[Drug-likeness filters]
  Filt --> Phys[Solubility / logP / PSA]
  Phys --> Perm[Permeability / P-gp]
  Perm --> Met[Metabolism / CYP]
  Met --> Tox[hERG / DILI / Ames]
  Tox --> Score[Multi-parameter score]
  Score --> Chem[Chemist decision]
```

Rather than pass/fail on each axis, teams use **multi-parameter optimization
(MPO)** — e.g. the CNS MPO score — combining endpoints into a single desirability
that respects the trade-offs (a fix for one property must not wreck another).

```plot
{"title": "Desirability vs an ADMET property", "xLabel": "Property value", "yLabel": "Desirability", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-((x-5)/2)^2)", "label": "Gaussian desirability", "color": "#16a34a"}]}
```

Best practices that make these pipelines trustworthy: report **uncertainty and
applicability domain** with every prediction; track **prospective** accuracy as
new assay data arrives (closing the loop); and treat predictions as *prioritizers*
that focus expensive experiments, not replacements for them. Open tools like
**ADMET-AI**, **SwissADME**, **pkCSM** and **TDC** make these workflows
accessible.

**Next:** test your advanced ADMET mastery.
""",
        ),
        _quiz(),
    ),
)


ADMET_PREDICTION_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ADMET_PREDICTION_COURSES"]
