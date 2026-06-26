"""Pharmacology track: Basics -> Intermediate -> Advanced.

A university-level pharmacology curriculum spanning drugs, receptors and
dose-response; pharmacodynamics and pharmacokinetics; and ADME, toxicology and
pharmacogenomics. Lessons use interactive ```plot blocks for quantitative
relationships (dose-response sigmoids, Hill cooperativity, Michaelis-Menten
metabolism, first-order clearance, receptor occupancy) and ```mermaid diagrams
for signalling pathways, ADME processes and drug-development pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Pharmacology -- Basics ---------------------------------------------------

_BASICS = SeedCourse(
    slug="pharmacology-basics",
    title="Pharmacology — Basics",
    description=(
        "The foundations of pharmacology: what a drug is, how drugs bind "
        "receptors, agonists and antagonists, the dose-response curve, and the "
        "ideas of potency, efficacy and the therapeutic window. Built on real "
        "molecular detail with interactive dose-response plots and signalling "
        "diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a drug and what does it do",
            "10 min",
            r"""
# What is a drug and what does it do

**Pharmacology** is the science of how chemicals interact with living systems.
A **drug** is any substance that, when applied to a biological system, alters
its function through a molecular interaction. Most drugs are small organic
molecules (under ~500 Da, per Lipinski's rules) but biologics — antibodies,
peptides, oligonucleotides — are increasingly important.

The discipline splits into two halves. **Pharmacodynamics** asks *what the drug
does to the body*: which target it binds, and the response that follows.
**Pharmacokinetics** asks *what the body does to the drug*: absorption,
distribution, metabolism and excretion (ADME). A useful drug needs both — the
right molecular action *and* the ability to reach its target at an effective,
safe concentration.

The central idea is **selectivity**: a good drug perturbs one target far more
than others. Most drugs act on four target classes — **receptors**, **enzymes**,
**ion channels** and **transporters**.

```mermaid
flowchart LR
  D[Drug molecule] --> PK[Pharmacokinetics: ADME]
  PK --> C[Concentration at target]
  C --> PD[Pharmacodynamics: binding + response]
  PD --> E[Therapeutic effect]
  PD --> AE[Adverse effect]
```

**Next:** how drugs recognise and bind their receptors.
""",
        ),
        _t(
            "Receptors and drug binding",
            "11 min",
            r"""
# Receptors and drug binding

A **receptor** is a macromolecule — usually a protein — that a drug binds to
produce a response. Binding is governed by the law of mass action. For a drug
$D$ binding receptor $R$ to form complex $DR$, equilibrium is set by the
**dissociation constant** $K_d = \frac{[D][R]}{[DR]}$. A smaller $K_d$ means
tighter binding (higher affinity); $K_d$ equals the free drug concentration
that occupies half the receptors.

Fractional occupancy follows a **rectangular hyperbola** in concentration:

$$\text{occupancy} = \frac{[D]}{[D] + K_d}$$

This saturating shape — many receptors are finite — is why higher doses give
ever-smaller extra binding. Binding forces are mostly reversible and
non-covalent: hydrogen bonds, ionic and van der Waals interactions, and the
hydrophobic effect. The receptor's three-dimensional pocket gives **chemical
and stereoselectivity** — often only one enantiomer fits.

The four major receptor superfamilies are **ligand-gated ion channels**,
**G-protein-coupled receptors (GPCRs)**, **enzyme-linked receptors** (e.g.
receptor tyrosine kinases) and **nuclear receptors**.

```plot
{"title": "Fractional receptor occupancy vs concentration", "xLabel": "free drug concentration", "yLabel": "fraction bound", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy (Kd=1)", "color": "#2563eb"}]}
```

**Next:** agonists and antagonists.
""",
        ),
        _t(
            "Agonists and antagonists",
            "11 min",
            r"""
# Agonists and antagonists

Binding alone is not enough — what matters is what happens next. An **agonist**
binds *and* stabilises the active receptor conformation, producing a response.
Its ability to do so is its **efficacy** (or intrinsic activity). A **full
agonist** reaches the system's maximal response; a **partial agonist** (e.g.
buprenorphine) plateaus below it even at full occupancy because its efficacy is
sub-maximal.

An **antagonist** binds with affinity but zero efficacy: it occupies the
receptor without activating it, blocking agonist action. A **competitive
antagonist** (e.g. naloxone, propranolol) competes for the same site; it shifts
the agonist curve rightward but is surmountable by more agonist. A
**non-competitive** (often irreversible or allosteric) antagonist depresses the
maximal response and cannot be fully overcome.

The **two-state model** frames receptors as flipping between resting (R) and
active (R*) states; ligands bias that equilibrium. An **inverse agonist**
stabilises R, suppressing constitutive (baseline) activity below it.

```mermaid
flowchart TB
  R[Receptor] --> A[Agonist: full response]
  R --> P[Partial agonist: submaximal]
  R --> C[Competitive antagonist: surmountable block]
  R --> N[Non-competitive antagonist: lowers max]
  R --> I[Inverse agonist: below baseline]
```

**Next:** the dose-response curve.
""",
        ),
        _t(
            "The dose-response curve",
            "11 min",
            r"""
# The dose-response curve

Plot drug effect against concentration and you get a hyperbola; plot it against
the **logarithm** of concentration and it becomes a familiar **sigmoid**. The
log axis spreads out the wide concentration range and makes the linear middle
region — the most informative part — easy to read and compare.

The graded relationship is captured by the **Hill-Langmuir equation**:

$$E = \frac{E_{max} \cdot [D]^n}{EC_{50}^n + [D]^n}$$

Here $E_{max}$ is the maximal effect, $EC_{50}$ is the concentration producing
half-maximal effect, and $n$ is the **Hill coefficient**, which reflects
cooperativity and steepens the curve when $n > 1$. Reading the curve: its
**ceiling** reports efficacy, its **horizontal position** reports potency.

A **quantal** dose-response, by contrast, plots the *fraction of a population*
showing an all-or-nothing response, yielding the median effective dose
$ED_{50}$ used in safety calculations.

```plot
{"title": "Sigmoidal log dose-response curve", "xLabel": "log dose", "yLabel": "effect (fraction of Emax)", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "graded response", "color": "#2563eb"}]}
```

**Next:** potency, efficacy and the therapeutic window.
""",
        ),
        _t(
            "Potency, efficacy and the therapeutic window",
            "11 min",
            r"""
# Potency, efficacy and the therapeutic window

Two drugs hitting the same target can differ in two independent ways.
**Potency** is *how much* drug is needed: a lower $EC_{50}$ (or $ED_{50}$) means
higher potency and a leftward-shifted curve. **Efficacy** is *how large* an
effect is achievable: a higher $E_{max}$ (a taller ceiling). A potent drug is
not necessarily a better drug — potency mostly affects the dose, while efficacy
and safety affect the clinical value.

Safety is framed by comparing the dose that helps with the dose that harms. The
**therapeutic index** is $TI = \frac{TD_{50}}{ED_{50}}$ (toxic vs effective
median dose). A large $TI$ (penicillin) is forgiving; a small one (warfarin,
digoxin, lithium) demands careful dosing and monitoring. The **therapeutic
window** is the concentration range above the minimum effective level but below
the toxic threshold.

```plot
{"title": "Effective vs toxic quantal curves (therapeutic window)", "xLabel": "log dose", "yLabel": "fraction of population responding", "xRange": [0,12], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-4)))", "label": "therapeutic effect", "color": "#16a34a"}, {"expr": "1/(1+exp(-(x-8)))", "label": "toxic effect", "color": "#dc2626"}]}
```

**Next:** test your understanding of the basics.
""",
        ),
        _quiz(),
    ),
)


# -- Pharmacology -- Intermediate ---------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="pharmacology-intermediate",
    title="Pharmacology — Intermediate",
    description=(
        "The quantitative core of pharmacology: receptor signalling and "
        "second messengers, receptor theory and spare receptors, "
        "one-compartment pharmacokinetics and clearance, Michaelis-Menten "
        "metabolism, and the maths of dosing regimens. Worked equations with "
        "interactive plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Receptor signalling and second messengers",
            "11 min",
            r"""
# Receptor signalling and second messengers

Receptor activation must be converted into a cellular response — and often
**amplified**. **GPCRs** are the largest druggable family. An agonist switches
the receptor to a GEF that loads GTP onto a heterotrimeric **G protein**;
$G\alpha$ and $G\beta\gamma$ then act on effectors. $G_s$ stimulates and $G_i$
inhibits **adenylyl cyclase** (changing cAMP, which activates **PKA**); $G_q$
activates **phospholipase C**, generating $IP_3$ (releasing $Ca^{2+}$) and DAG
(activating PKC).

The key feature is a **cascade**: one receptor activates many G proteins, each
enzyme makes many messenger molecules, so a few occupied receptors drive a large
response. This biochemical gain explains **spare receptors**. Signalling is
terminated by GTP hydrolysis, phosphodiesterases (degrading cAMP) and receptor
desensitisation via **GRK/β-arrestin**.

```mermaid
flowchart LR
  L[Agonist] --> GPCR
  GPCR --> G[G protein GTP exchange]
  G --> AC[Adenylyl cyclase]
  AC --> cAMP
  cAMP --> PKA[PKA: phosphorylates targets]
  PKA --> Resp[Cellular response]
```

**Next:** receptor theory and spare receptors.
""",
        ),
        _t(
            "Receptor theory and spare receptors",
            "11 min",
            r"""
# Receptor theory and spare receptors

Classical **occupancy theory** assumed response is proportional to occupancy, so
$EC_{50}$ would equal $K_d$. Experiments often disagree: maximal response is
reached when only a fraction of receptors are bound. These unused receptors are
**spare receptors** (a *receptor reserve*), and their consequence is that
$EC_{50} < K_d$ — the system is half-maximally activated below half occupancy.

The **operational (Black-Leff) model** captures this with a single transducer
parameter $\tau = \frac{R_{total}}{K_E}$, where $K_E$ is the occupancy giving
half-maximal effect. Response is:

$$E = \frac{E_{max} \cdot \tau \cdot [D]}{K_d + (1 + \tau)[D]}$$

A large $\tau$ means high efficiency, a large reserve, and an effect curve far
left of the binding curve. The reserve buffers responses against partial
receptor loss and lets low agonist concentrations act fast. It also explains why
**irreversible antagonists** first only shift the agonist curve (using up the
reserve) before they finally depress the maximum.

```plot
{"title": "Effect curve left-shifted by a receptor reserve", "xLabel": "log concentration", "yLabel": "fraction of maximum", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "effect (with reserve)", "color": "#2563eb"}, {"expr": "1/(1+exp(-(x-5)))", "label": "occupancy", "color": "#dc2626"}]}
```

**Next:** one-compartment pharmacokinetics.
""",
        ),
        _t(
            "One-compartment pharmacokinetics",
            "12 min",
            r"""
# One-compartment pharmacokinetics

The simplest PK model treats the body as a single well-mixed **compartment**.
After an IV bolus dose, plasma concentration falls **exponentially** by
first-order elimination:

$$C(t) = C_0 \, e^{-k_e t}, \qquad C_0 = \frac{Dose}{V_d}$$

Two parameters define the system. The **volume of distribution**
$V_d = \frac{Dose}{C_0}$ is an *apparent* volume linking dose to plasma level;
large $V_d$ means extensive tissue distribution. The **elimination rate
constant** $k_e$ sets the speed of decline. The **half-life**
$t_{1/2} = \frac{0.693}{k_e}$ is the time for concentration to halve; after about
4–5 half-lives a drug is ~97% gone.

The third pillar is **clearance** $CL = k_e \cdot V_d$, the volume of plasma
cleared of drug per unit time. Clearance is the parameter that determines the
**maintenance dose**, since at steady state input rate equals $CL \cdot
C_{ss}$. Plotting $\ln C$ vs $t$ gives a straight line of slope $-k_e$.

```plot
{"title": "Plasma concentration after an IV bolus (first-order decay)", "xLabel": "time (half-lives)", "yLabel": "plasma concentration", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t) = C0 e^(-ke t)", "color": "#2563eb"}]}
```

**Next:** metabolism and Michaelis-Menten kinetics.
""",
        ),
        _t(
            "Metabolism and Michaelis-Menten kinetics",
            "12 min",
            r"""
# Metabolism and Michaelis-Menten kinetics

Most drugs are eliminated after **biotransformation** by enzymes — chiefly the
hepatic **cytochrome P450** family (CYP3A4, CYP2D6, CYP2C9 and others). Because
enzymes are saturable, metabolic rate obeys **Michaelis-Menten kinetics**:

$$v = \frac{V_{max}[S]}{K_m + [S]}$$

Here $V_{max}$ is the maximal rate and $K_m$ the substrate concentration at half
$V_{max}$. At low concentrations ($[S] \ll K_m$) rate is roughly proportional to
$[S]$ — this is the **first-order** regime that gives the constant half-life of
ordinary PK. As $[S]$ rises toward and beyond $K_m$, the enzyme saturates and
elimination becomes **zero-order** (constant amount per unit time).

This **capacity-limited** behaviour is clinically dangerous: for drugs like
**phenytoin, ethanol and high-dose aspirin**, a small dose increase near
saturation causes a disproportionate jump in concentration. Inhibition (e.g.
grapefruit juice on CYP3A4) and induction (rifampicin, phenobarbital) of these
enzymes are major sources of **drug-drug interactions**.

```plot
{"title": "Michaelis-Menten metabolic rate vs drug concentration", "xLabel": "drug concentration [S]", "yLabel": "rate of metabolism v", "xRange": [0,20], "yRange": [0,10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v (Vmax=8, Km=2)", "color": "#16a34a"}]}
```

**Next:** dosing regimens and steady state.
""",
        ),
        _t(
            "Dosing regimens and steady state",
            "12 min",
            r"""
# Dosing regimens and steady state

Single doses rarely suffice; therapy needs concentrations held inside the
therapeutic window over time. With **repeated dosing** (or a constant infusion)
drug accumulates until input balances elimination, reaching **steady state**
after about 4–5 half-lives — independent of the dose size. The average
steady-state concentration is:

$$C_{ss} = \frac{F \cdot Dose}{CL \cdot \tau}$$

where $F$ is **bioavailability** (the fraction of an oral dose reaching the
systemic circulation, reduced by incomplete absorption and **first-pass**
hepatic metabolism) and $\tau$ is the dosing interval. Two levers shape the
profile: the **maintenance dose / rate** sets the steady-state *level* (via
$CL$), while the **interval** sets the peak-to-trough *fluctuation*.

To skip the slow climb, a **loading dose** $= C_{target} \cdot V_d / F$ fills
the volume of distribution at once — used when a fast effect matters (e.g.
loading digoxin or an antibiotic). Approach to steady state follows
$1 - e^{-k_e t}$.

```plot
{"title": "Approach to steady state during repeated dosing", "xLabel": "time (half-lives)", "yLabel": "fraction of Css", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1-exp(-0.7*x)", "label": "accumulation to Css", "color": "#2563eb"}]}
```

**Next:** test your understanding of the intermediate methods.
""",
        ),
        _quiz(),
    ),
)


# -- Pharmacology -- Advanced -------------------------------------------------

_ADVANCED = SeedCourse(
    slug="pharmacology-advanced",
    title="Pharmacology — Advanced",
    description=(
        "State-of-the-art pharmacology: the full ADME picture, principles of "
        "toxicology and dose-response thresholds, pharmacogenomics and "
        "personalised dosing, PK/PD modelling, and AI-driven drug discovery. "
        "Applied, quantitative, and connected to current practice."
    ),
    level="Advanced",
    lessons=(
        _t(
            "ADME: the full journey of a drug",
            "12 min",
            r"""
# ADME: the full journey of a drug

**ADME** — absorption, distribution, metabolism, excretion — is the integrated
fate of a drug. **Absorption** across membranes depends on lipophilicity,
ionisation (the Henderson-Hasselbalch balance of a drug's $pK_a$ against local
$pH$) and transporters; orally, bioavailability is cut by first-pass
metabolism. **Distribution** is governed by perfusion, plasma-protein binding
(albumin, α1-acid glycoprotein) and barriers like the **blood-brain barrier**,
whose P-glycoprotein efflux pumps keep many drugs out of the CNS.

**Metabolism** runs in two phases: **Phase I** (oxidation/reduction/hydrolysis,
mostly cytochrome P450) introduces or exposes a functional group; **Phase II**
(conjugation — glucuronidation, sulfation, acetylation, glutathione) attaches a
polar group to ease excretion. **Excretion** is mainly renal (glomerular
filtration, tubular secretion and reabsorption) and biliary, sometimes with
enterohepatic recycling.

```mermaid
flowchart LR
  A[Absorption: gut to blood] --> D[Distribution: tissues + protein binding]
  D --> M1[Phase I: CYP oxidation]
  M1 --> M2[Phase II: conjugation]
  M2 --> Ex[Excretion: renal + biliary]
```

**Next:** principles of toxicology.
""",
        ),
        _t(
            "Toxicology and dose-response thresholds",
            "12 min",
            r"""
# Toxicology and dose-response thresholds

Paracelsus' dictum — *"the dose makes the poison"* — is the foundation of
**toxicology**. Toxicity may be **on-target** (an exaggerated pharmacological
effect) or **off-target** (action at unintended sites), and may be acute or
chronic. A central regulatory concept is the **threshold**: for most non-genotoxic
effects there is a **NOAEL** (no-observed-adverse-effect level) below which no
harm is detected, from which safe human exposures are derived by applying
uncertainty factors.

Many toxicities are **mechanistic** rather than the parent drug itself. The
classic example is **acetaminophen (paracetamol)**: normal doses are conjugated
safely, but in overdose the minor CYP2E1 pathway floods the liver with the
reactive metabolite **NAPQI**, which depletes glutathione and binds proteins —
treated by replenishing glutathione with **N-acetylcysteine**. Modern safety
work also screens for **hERG** channel block (QT prolongation) and uses
biomarkers and *in vitro* assays to predict organ toxicity early.

```plot
{"title": "Threshold (sigmoidal) toxic dose-response", "xLabel": "log dose", "yLabel": "fraction with toxic effect", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-6)))", "label": "toxic response (threshold near NOAEL)", "color": "#dc2626"}]}
```

**Next:** pharmacogenomics and personalised dosing.
""",
        ),
        _t(
            "Pharmacogenomics and personalised dosing",
            "12 min",
            r"""
# Pharmacogenomics and personalised dosing

Patients respond differently to the same dose, and much of that variability is
**genetic**. **Pharmacogenomics** studies how inherited variants shape drug
response, mostly via metabolising enzymes, transporters and targets. The
canonical example is **CYP2D6**, which metabolises ~25% of drugs: copy-number and
sequence variants sort people into **poor, intermediate, extensive and
ultra-rapid metabolisers**. A codeine ultra-rapid metaboliser converts too much
prodrug to morphine (toxicity risk); a poor metaboliser gets no analgesia.

Other actionable pairs include **TPMT/NUDT15** (thiopurine toxicity),
**CYP2C19** (clopidogrel activation), **VKORC1/CYP2C9** (warfarin dosing) and
**HLA-B*57:01** (abacavir hypersensitivity — now genotyped before prescribing).
Consortia like **CPIC** publish gene-drug dosing guidelines, turning a genotype
into a concrete dose recommendation — a core piece of precision medicine.

```mermaid
flowchart LR
  G[Patient genotype] --> P[Metaboliser phenotype]
  P --> PM[Poor: drug accumulates]
  P --> EM[Extensive: standard dose]
  P --> UM[Ultra-rapid: subtherapeutic / prodrug toxicity]
  PM --> Dose[Adjust dose or switch drug]
  UM --> Dose
```

**Next:** PK/PD modelling and simulation.
""",
        ),
        _t(
            "PK/PD modelling and simulation",
            "12 min",
            r"""
# PK/PD modelling and simulation

**PK/PD modelling** links the time course of concentration (PK) to the time
course of effect (PD), letting us predict regimens rather than guess them.
Effect is commonly described by an **$E_{max}$ model**,
$E = \frac{E_{max} \cdot C}{EC_{50} + C}$, or its sigmoidal Hill form. When
effect lags concentration, an **effect-compartment** (hysteresis) or
**indirect-response** model captures the delay between plasma level and
biological turnover.

For antimicrobials, **PK/PD indices** decide dosing: $\beta$-lactams are
*time-dependent* (maximise the time above MIC), while aminoglycosides and
fluoroquinolones are *concentration-dependent* (maximise $C_{max}/MIC$ or
$AUC/MIC$). The modern workhorse is **population PK (NONMEM, Monolix,
nlmixr2)**: nonlinear mixed-effects models that separate **fixed effects**
(covariates like weight, renal function) from **random effects**
(between-patient variability), enabling **Bayesian** individualised dosing from
sparse samples and **clinical-trial simulation**.

```plot
{"title": "Emax pharmacodynamic model (Hill cooperativity, n=2)", "xLabel": "concentration / EC50", "yLabel": "fraction of Emax", "xRange": [0,8], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "sigmoidal Emax", "color": "#2563eb"}]}
```

**Next:** AI and computational drug discovery.
""",
        ),
        _t(
            "AI and computational drug discovery",
            "12 min",
            r"""
# AI and computational drug discovery

Computation now spans the whole discovery pipeline. **Structure-based design**
uses molecular **docking** and free-energy perturbation against a target
structure — increasingly one predicted by **AlphaFold**. **Ligand-based**
methods learn from known actives via **QSAR** and molecular fingerprints.

Modern machine learning reshaped both. **Graph neural networks** treat molecules
as graphs to predict activity, solubility and toxicity (ADMET); the landmark
**halicin** antibiotic was found by screening compounds with a trained GNN.
**Generative models** — variational autoencoders, diffusion models and
reinforcement learning — design novel molecules with desired properties, while
large language models trained on SMILES propose and optimise candidates. In the
clinic, ML supports **virtual screening**, **drug-target interaction**
prediction, **drug repurposing** and even patient stratification.

These tools accelerate but do not replace pharmacology: predictions still need
experimental validation, and PK/PD plus safety remain the gatekeepers. The frontier
is end-to-end pipelines coupling generation, property prediction and
physiologically-based PK (PBPK) simulation.

```mermaid
flowchart LR
  T[Target structure: AlphaFold] --> S[Virtual screen / docking]
  Data[Bioactivity data] --> GNN[GNN ADMET prediction]
  S --> Gen[Generative design]
  GNN --> Gen
  Gen --> Cand[Candidate molecules]
  Cand --> Val[Experimental + PBPK validation]
```

**Next:** test your understanding of the advanced topics.
""",
        ),
        _quiz(),
    ),
)


PHARMACOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PHARMACOLOGY_COURSES"]
