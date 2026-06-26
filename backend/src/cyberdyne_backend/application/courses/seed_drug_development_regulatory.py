"""Drug Development, Clinical Trials & Regulatory track: Basics -> Intermediate -> Advanced.

Three courses tracing a medicine from target to clinic: the discovery-to-approval
arc and key players (Basics); preclinical PK/PD, trial design, statistics and GxP
quality (Intermediate); regulatory pathways, intellectual property, pharmacovigilance
and modern AI/computational methods (Advanced). Lessons embed interactive ```plot
blocks (dose-response, PK curves, survival, hazard) and ```mermaid diagrams
(pipelines, trial phases, regulatory routes, signal-detection loops).
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ──────────────────────────────────────────────────────────────────────
# 1. drug-development-regulatory-basics (Beginner)
# ──────────────────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="drug-development-regulatory-basics",
    title="Drug Development, Clinical Trials & Regulatory — Basics",
    description=(
        "How a medicine travels from a biological idea to an approved product. "
        "You'll map the discovery-to-clinic pipeline, meet drug targets and "
        "dose-response, learn what preclinical and clinical phases test, and see "
        "who the regulators are and why the whole process takes a decade."
    ),
    level="Beginner",
    lessons=(
        _t(
            "From target to clinic: the drug development pipeline",
            "10 min",
            r"""# From target to clinic: the drug development pipeline

Bringing a new medicine to patients typically takes **10–15 years** and costs
well over a billion dollars, because attrition is brutal: of compounds entering
human trials, only about **1 in 10** is approved. The pipeline is a funnel.

It begins with **basic research and target identification** (finding a protein
or pathway whose modulation should treat disease), then **drug discovery**
(finding molecules that hit the target), **preclinical** studies (lab and animal
safety and efficacy), three **clinical phases** in humans, **regulatory review**,
and finally **post-marketing** surveillance once the drug is on the market.

```mermaid
flowchart LR
  A[Target identification] --> B[Discovery / hit-to-lead]
  B --> C[Preclinical]
  C --> D[Phase I]
  D --> E[Phase II]
  E --> F[Phase III]
  F --> G[Regulatory review]
  G --> H[Approval and Phase IV]
```

Each stage answers a sharper question: *Is the target valid? Does a molecule
engage it? Is it safe enough to give a human? Does it work? Does it work better
than what exists?* Most projects die early, which is by design — failing cheaply
and early is the economic engine of the whole enterprise.

**Next:** what a drug target actually is.
""",
        ),
        _t(
            "Drug targets, mechanisms and modalities",
            "11 min",
            r"""# Drug targets, mechanisms and modalities

A **drug target** is a molecule in the body — most often a **protein** — whose
activity a drug changes to produce a therapeutic effect. The largest target
classes are **G-protein-coupled receptors (GPCRs)**, **enzymes** (e.g. kinases,
proteases), **ion channels**, and **nuclear receptors**. A good target is
**druggable** (it has a pocket a molecule can bind) and **validated** (changing
it actually changes the disease).

A drug can act as an **agonist** (activates the target), an **antagonist**
(blocks it), or an **inhibitor** (slows an enzyme). The **modality** is the kind
of molecule used: **small molecules** (oral, cheap, cross membranes),
**biologics** such as monoclonal antibodies (large, injected, highly specific),
and newer modalities like **antisense oligonucleotides** and **mRNA**.

```mermaid
flowchart TB
  T[Drug target] --> R[GPCRs]
  T --> E[Enzymes]
  T --> I[Ion channels]
  T --> N[Nuclear receptors]
  M[Modality] --> S[Small molecule]
  M --> B[Biologic / antibody]
  M --> O[Oligonucleotide / mRNA]
```

The choice of modality shapes everything downstream: how the drug is made, how
it is dosed, how it is regulated, and how long its patent protection lasts.

**Next:** how dose relates to effect.
""",
        ),
        _t(
            "Dose, response and the therapeutic window",
            "11 min",
            r"""# Dose, response and the therapeutic window

The central relationship in pharmacology is **dose-response**: as drug
concentration rises, effect rises — but not linearly. Plotted against the
**logarithm of concentration**, response traces a characteristic **sigmoid**
curve that saturates once all targets are engaged.

```plot
{"title": "Dose-response (sigmoid)", "xLabel": "log concentration", "yLabel": "fraction of max effect", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#2563eb"}]}
```

Two quantities summarize potency and efficacy. **EC50** (or **IC50** for
inhibition) is the concentration giving **half** the maximal effect — the curve's
midpoint. The **maximal effect** is its plateau. A more potent drug shifts the
curve left (smaller EC50).

Crucially, every drug also has a dose where it becomes toxic. The
**therapeutic window** is the gap between the dose that helps and the dose that
harms, captured by the **therapeutic index** $TI = \frac{TD_{50}}{ED_{50}}$,
the ratio of the toxic dose to the effective dose in 50% of subjects. A wide
window (large $TI$) is safe and forgiving; a narrow one (e.g. warfarin, digoxin)
demands careful monitoring. Picking the right human dose from this balance is a
core goal of early clinical trials.

**Next:** what preclinical studies establish before any human is dosed.
""",
        ),
        _t(
            "Preclinical studies: efficacy, safety and toxicology",
            "11 min",
            r"""# Preclinical studies: efficacy, safety and toxicology

Before a candidate reaches a human, **preclinical** research must show it is
likely to work and unlikely to cause unacceptable harm. This happens *in vitro*
(cells, biochemical assays) and *in vivo* (animal models), under
**Good Laboratory Practice (GLP)** for the safety-critical studies.

Key questions answered here: Does the molecule produce the intended effect in a
disease model (**proof of mechanism / efficacy**)? What does the body do to it —
its **pharmacokinetics (PK)**: absorption, distribution, metabolism, excretion?
And what does it do to the body at high doses — **toxicology**, including
single- and repeat-dose studies, **genotoxicity**, and effects on organs?

```mermaid
flowchart LR
  C[Lead candidate] --> V[In vitro assays]
  C --> A[Animal PK]
  C --> Tox[GLP toxicology]
  V --> IND[IND-enabling package]
  A --> IND
  Tox --> IND
  IND --> FIH[First-in-human dose]
```

These data are assembled into a regulatory submission — an **IND**
(Investigational New Drug) in the US or a **CTA** (Clinical Trial Application)
in Europe — that justifies a safe **starting dose** in humans, usually derived
from the **NOAEL** (No Observed Adverse Effect Level) in the most sensitive
animal species with a generous safety margin.

**Next:** the three phases of human trials.
""",
        ),
        _t(
            "Clinical trial phases I, II and III",
            "11 min",
            r"""# Clinical trial phases I, II and III

Human testing proceeds in **escalating phases**, each gating the next.

**Phase I** (≈20–100 participants, often healthy volunteers) asks *is it safe?*
It establishes the safety profile, the **maximum tolerated dose**, and human PK.

**Phase II** (≈100–300 patients) asks *does it work, and at what dose?* It looks
for the first signals of efficacy and refines dosing; many drugs die here.

**Phase III** (hundreds to thousands of patients) asks *is it better than the
standard of care?* These large, often **multi-centre, randomized, controlled**
trials provide the pivotal evidence regulators require for approval.

```mermaid
flowchart LR
  P1[Phase I: safety, dose] --> P2[Phase II: efficacy signal]
  P2 --> P3[Phase III: confirmatory]
  P3 --> SUB[Marketing application]
  SUB --> P4[Phase IV: post-marketing]
```

The number of patients grows because rare effects and modest benefits need
**statistical power** to detect. The attrition is steep — far fewer compounds
clear Phase III than enter Phase I — so each phase is a deliberate, increasingly
expensive bet placed only after the previous one pays off.

**Next:** the regulators who decide whether a drug reaches patients.
""",
        ),
        _t(
            "Regulators and the approval decision",
            "10 min",
            r"""# Regulators and the approval decision

A drug may not be marketed until an independent **regulatory authority** judges
that its **benefits outweigh its risks** for a defined use. The major agencies
are the **FDA** (United States), the **EMA** (European Union), the **PMDA**
(Japan), and **ANVISA** (Brazil); the **ICH** harmonizes their technical
requirements so a single development programme can serve many markets.

The sponsor submits a dossier — an **NDA**/**BLA** in the US or an **MAA** in
Europe — containing all quality, non-clinical and clinical data. Reviewers
assess efficacy, safety, manufacturing quality, and the proposed **label**
(who may take the drug, at what dose, with what warnings).

```mermaid
flowchart LR
  S[Sponsor dossier] --> R[Agency review]
  R --> AC[Advisory committee]
  AC --> D{Benefit > risk?}
  D -->|Yes| AP[Approval and label]
  D -->|No| CR[Complete response / refusal]
  AP --> PV[Pharmacovigilance]
```

Approval is **conditional on continued evidence**: the label can be restricted,
post-marketing studies (Phase IV) can be required, and the drug can be withdrawn
if real-world safety data turn unfavourable. Regulation is therefore not a single
gate but an ongoing relationship that lasts the product's entire life.

**Next:** test your grasp of the development arc.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 2. drug-development-regulatory-intermediate (Intermediate)
# ──────────────────────────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="drug-development-regulatory-intermediate",
    title="Drug Development, Clinical Trials & Regulatory — Intermediate",
    description=(
        "The quantitative core of development. You'll model pharmacokinetics and "
        "PK/PD, design controlled trials with randomization and blinding, size them "
        "with power and analyze them with survival and hypothesis tests, and learn "
        "the GxP quality systems and ethics that make the data trustworthy."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pharmacokinetics: compartment models and clearance",
            "12 min",
            r"""# Pharmacokinetics: compartment models and clearance

**Pharmacokinetics (PK)** is the quantitative study of how drug concentration
in plasma changes over time. The simplest description is a **one-compartment
model** with first-order elimination: after an IV dose, concentration decays
exponentially, $C(t) = C_0\,e^{-k_e t}$, where $k_e$ is the elimination rate
constant.

```plot
{"title": "First-order plasma decay", "xLabel": "time (h)", "yLabel": "concentration", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t)", "color": "#2563eb"}]}
```

Three parameters dominate. The **half-life** $t_{1/2} = \frac{\ln 2}{k_e}$ is
the time for concentration to halve; it sets dosing frequency. **Clearance**
$CL$ is the volume of plasma cleared of drug per unit time and governs the
**steady-state** level on repeated dosing. The **volume of distribution** $V_d$
relates the dose to the resulting concentration ($C_0 = \frac{Dose}{V_d}$) and
hints at how widely the drug spreads into tissues.

A key integrated measure is the **AUC** (area under the curve), the total drug
exposure, since $AUC = \frac{Dose}{CL}$. For oral drugs, **bioavailability**
$F$ is the fraction of the dose reaching circulation after first-pass
metabolism. Together these let pharmacologists predict concentrations for any
dose and schedule.

**Next:** linking those concentrations to effect.
""",
        ),
        _t(
            "PK/PD modeling: linking exposure to effect",
            "12 min",
            r"""# PK/PD modeling: linking exposure to effect

PK tells us the **concentration** over time; **pharmacodynamics (PD)** tells us
the **effect** at a given concentration. **PK/PD modeling** joins them so we can
predict effect over time and choose a dose rationally.

The workhorse PD relationship is the **Emax model**, a saturable
concentration-effect curve:

$$E = E_0 + \frac{E_{max}\,C}{EC_{50} + C}$$

Effect rises with concentration $C$, saturates at $E_{max}$, and reaches half
that at $EC_{50}$. Its hyperbolic (or, on a log scale, sigmoid) shape is why
doubling a dose rarely doubles effect once you are near the plateau.

```plot
{"title": "Emax concentration-effect", "xLabel": "concentration", "yLabel": "effect", "xRange": [0,20], "yRange": [0,10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "Emax model", "color": "#16a34a"}]}
```

Real drugs add wrinkles: a **Hill coefficient** steepens the curve when binding
is cooperative, and an **effect compartment** captures **hysteresis** — the lag
when effect trails plasma concentration. Population PK/PD methods (e.g.
**nonlinear mixed-effects modeling**, NONMEM) estimate typical parameters *and*
between-patient variability, supporting **model-informed drug development** and
dose individualization.

**Next:** the architecture of a controlled trial.
""",
        ),
        _t(
            "Controlled trial design: randomization, blinding and controls",
            "12 min",
            r"""# Controlled trial design: randomization, blinding and controls

A trial's job is to produce an **unbiased, causal** estimate of a treatment's
effect. Three design pillars deliver this.

**Randomization** assigns participants to treatment or control by chance, so
known *and unknown* confounders are balanced on average between arms — this is
what licenses causal claims. **Blinding** (single, double, or triple) hides the
assignment from patients, clinicians and assessors to prevent expectation and
reporting bias. A **control group** — placebo or active comparator — provides
the counterfactual against which the treatment effect is measured.

```mermaid
flowchart LR
  E[Eligible patients] --> R{Randomize}
  R --> T[Treatment arm]
  R --> C[Control arm]
  T --> O[Outcome assessment - blinded]
  C --> O
  O --> A[Compare arms]
```

The result is the **RCT** (randomized controlled trial), the gold standard for
evidence. Variants suit different questions: **parallel-group** (the default),
**crossover** (each patient is their own control, for stable chronic conditions),
**factorial** (test two interventions at once), and **adaptive** designs that
modify allocation or sample size at pre-planned interims. A pre-registered
**protocol** and **statistical analysis plan** lock these choices in advance,
guarding against data-driven bias.

**Next:** how many patients the trial needs.
""",
        ),
        _t(
            "Endpoints, hypothesis testing and statistical power",
            "12 min",
            r"""# Endpoints, hypothesis testing and statistical power

Every trial defines a **primary endpoint** — the single outcome on which success
is judged (e.g. survival, blood pressure, a responder rate). Choosing it well,
and pre-specifying it, is decisive. **Surrogate endpoints** (a biomarker like
LDL cholesterol) speed trials but must reliably predict the clinical outcome.

Analysis frames a **null hypothesis** ($H_0$: no difference) against an
**alternative**. The **p-value** is the probability of data this extreme if
$H_0$ were true; rejecting $H_0$ risks a **Type I error** (false positive, rate
$\alpha$, conventionally 0.05). Missing a real effect is a **Type II error**
(rate $\beta$); **power** $= 1-\beta$ is the chance of detecting a true effect,
usually targeted at 0.80–0.90.

Required sample size grows as the effect you want to detect shrinks — roughly
$n \propto 1/\Delta^2$ for a difference $\Delta$ — so detecting small effects
needs many patients.

```plot
{"title": "Sample size vs effect size", "xLabel": "effect size", "yLabel": "relative sample size", "xRange": [0.2,3], "yRange": [0,30], "grid": true, "functions": [{"expr": "1/(x*x)", "label": "n proportional to 1/effect^2", "color": "#dc2626"}]}
```

Analysis follows the **intention-to-treat** principle (analyze patients as
randomized) to preserve randomization's protection, and **multiplicity**
corrections guard against false positives when many endpoints are tested.

**Next:** analyzing time-to-event data.
""",
        ),
        _t(
            "Survival analysis and time-to-event endpoints",
            "12 min",
            r"""# Survival analysis and time-to-event endpoints

Many trials measure **time to an event** — death, relapse, progression. Such
data need special methods because some patients are **censored**: they leave the
study or reach its end without the event, so we know only that their event time
*exceeds* their observed time.

The **survival function** $S(t) = P(T > t)$ is the probability of remaining
event-free past time $t$. It is estimated nonparametrically by the
**Kaplan–Meier** curve, a step function that drops at each observed event.

```plot
{"title": "Survival function S(t)", "xLabel": "time", "yLabel": "S(t) = P(T > t)", "xRange": [0,10], "yRange": [0,1.05], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "exponential survival", "color": "#2563eb"}]}
```

Two arms' curves are compared with the **log-rank test**. To quantify the
effect, the **Cox proportional-hazards model** estimates the **hazard ratio**
$HR$: the relative instantaneous event rate in treatment versus control. An
$HR < 1$ means the treatment lowers risk; $HR = 0.7$ is a 30% reduction in the
hazard at any moment, *assuming* the ratio is constant over time (the
**proportional-hazards** assumption, which should be checked).

```mermaid
flowchart LR
  D[Time-to-event data] --> KM[Kaplan-Meier estimate]
  KM --> LR[Log-rank test]
  D --> COX[Cox model]
  COX --> HR[Hazard ratio + CI]
```

**Next:** the quality systems that make trial data trustworthy.
""",
        ),
        _t(
            "GxP quality systems and research ethics",
            "11 min",
            r"""# GxP quality systems and research ethics

Trustworthy development rests on **GxP** — a family of "Good Practice" quality
standards enforced by regulators. **GLP** governs non-clinical safety studies,
**GCP** (Good Clinical Practice, codified in **ICH E6**) governs the conduct of
clinical trials, and **GMP** governs how the drug is manufactured. Their shared
goal is **data integrity** and **subject protection**.

GCP demands a written **protocol**, qualified investigators, source-document
verification, and **traceable, attributable** records — often summarized by the
mnemonic **ALCOA** (Attributable, Legible, Contemporaneous, Original, Accurate).
A **Data Safety Monitoring Board** independently watches accumulating safety data
and can stop a trial early for harm or overwhelming benefit.

```mermaid
flowchart TB
  ETH[Ethics + oversight] --> IRB[IRB / Ethics Committee]
  ETH --> IC[Informed consent]
  ETH --> DSMB[Data Safety Monitoring Board]
  QMS[GxP quality] --> GLP[GLP - preclinical]
  QMS --> GCP[GCP - clinical]
  QMS --> GMP[GMP - manufacturing]
```

Ethics is the bedrock. Anchored in the **Declaration of Helsinki** and the
**Belmont Report** (respect for persons, beneficence, justice), every trial
requires independent review by an **IRB / Ethics Committee** and the **informed
consent** of each participant. These safeguards arose from historical abuses and
are non-negotiable: scientifically valid data obtained unethically cannot be used.

**Next:** check your understanding of the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# 3. drug-development-regulatory-advanced (Advanced)
# ──────────────────────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="drug-development-regulatory-advanced",
    title="Drug Development, Clinical Trials & Regulatory — Advanced",
    description=(
        "The frontier of bringing drugs to market. You'll navigate regulatory "
        "pathways and expedited programmes, the CTD/eCTD dossier, intellectual "
        "property and market exclusivity, modern adaptive and platform trials, "
        "pharmacovigilance signal detection, and the AI/ML methods now reshaping "
        "trial design, safety surveillance and regulatory science."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Regulatory pathways and expedited programmes",
            "12 min",
            r"""# Regulatory pathways and expedited programmes

Beyond the standard review, regulators offer **expedited pathways** for drugs
addressing serious unmet needs. In the US the FDA grants **Fast Track**
(facilitated development and rolling review), **Breakthrough Therapy**
(intensive guidance when early evidence is striking), **Accelerated Approval**
(approval on a *surrogate endpoint* reasonably likely to predict benefit, with
confirmatory trials required), and **Priority Review** (a 6- vs 10-month clock).
The EMA mirrors these with **PRIME** and **conditional marketing authorisation**.

```mermaid
flowchart LR
  N[Serious unmet need] --> FT[Fast Track]
  N --> BT[Breakthrough Therapy]
  N --> AA[Accelerated Approval]
  AA --> CONF[Confirmatory trial]
  CONF -->|fails| W[Withdrawal]
  CONF -->|confirms| FULL[Full approval]
```

These programmes trade **earlier access** for **greater post-market obligation**:
accelerated approvals can be withdrawn if confirmatory trials fail, as has
happened. Separate routes serve special populations — **Orphan Drug**
designation (incentives plus exclusivity for rare diseases), **paediatric**
investigation plans, and the **505(b)(2)** pathway that relies partly on
existing data. Choosing and sequencing these designations is a strategic
discipline that can shorten time-to-market by years.

**Next:** how the evidence is packaged for review.
""",
        ),
        _t(
            "The CTD/eCTD dossier and global submissions",
            "11 min",
            r"""# The CTD/eCTD dossier and global submissions

A modern marketing application can run to hundreds of thousands of pages. To make
it reviewable across regions, ICH defined the **Common Technical Document (CTD)**
— a standard five-module structure now submitted electronically as the **eCTD**.

```mermaid
flowchart TB
  M1[Module 1: regional admin] --> APP[Application]
  M2[Module 2: summaries] --> APP
  M3[Module 3: quality / CMC] --> APP
  M4[Module 4: nonclinical reports] --> APP
  M5[Module 5: clinical reports] --> APP
```

**Module 1** is region-specific (forms, labelling). **Module 2** holds the expert
overviews and summaries reviewers read first. **Module 3** is **quality / CMC**
(Chemistry, Manufacturing and Controls) — how the drug substance and product are
made, characterized and controlled. **Module 4** holds the nonclinical study
reports and **Module 5** the clinical study reports.

The eCTD adds **lifecycle management**: each later submission is a sequence that
*replaces, appends or deletes* documents, so the agency always sees a current,
hyperlinked, validated view. Underlying data increasingly follow **CDISC**
standards (**SDTM** for tabulated data, **ADaM** for analysis datasets), letting
reviewers re-run analyses. A single well-structured dossier can support
near-simultaneous filings in many markets.

**Next:** the intellectual property that funds it all.
""",
        ),
        _t(
            "Intellectual property and market exclusivity",
            "11 min",
            r"""# Intellectual property and market exclusivity

The decade-long, billion-dollar investment is recouped during a window of
**market exclusivity**. Two distinct mechanisms create it.

**Patents** grant ~**20 years** of protection *from the filing date* — but the
clock starts early in discovery, so by launch perhaps **8–12 years** of
**effective** patent life remain. Composition-of-matter, method-of-use and
formulation patents form a "patent estate". Because so much patent life is
consumed by development, jurisdictions grant **patent term extension** /
**supplementary protection certificates** to restore some lost time.

```mermaid
flowchart LR
  F[Patent filed] --> D[Development ~10 yr]
  D --> L[Launch]
  L --> X[Effective exclusivity]
  X --> E[Patent / exclusivity expiry]
  E --> G[Generic / biosimilar entry]
```

**Regulatory exclusivity** is separate and granted by the drug agency regardless
of patents: e.g. US **New Chemical Entity** exclusivity (5 years), **orphan**
exclusivity (7 years US / 10 years EU), and **biologic** exclusivity (12 years
US). When protection lapses, **generics** (small molecules, via an ANDA proving
**bioequivalence**) and **biosimilars** (highly similar biologics) enter, and
prices typically fall sharply — the **patent cliff**. Managing this lifecycle is
central to pharmaceutical strategy.

**Next:** the modern shape of confirmatory trials.
""",
        ),
        _t(
            "Adaptive, platform and Bayesian trial designs",
            "12 min",
            r"""# Adaptive, platform and Bayesian trial designs

Classical fixed trials are powerful but rigid and slow. **Adaptive designs**
use **pre-planned interim analyses** to modify a trial as data arrive — dropping
inferior arms, re-estimating sample size, or stopping early for efficacy or
futility — all while controlling the overall **Type I error** through methods
like **alpha spending**.

**Platform** and **basket/umbrella** trials go further: a shared master protocol
and control group evaluate **many treatments** (or many subtypes) under one
infrastructure, so new arms are added and graduated continuously. This was vital
in oncology and in the COVID-19 RECOVERY and SOLIDARITY trials.

```mermaid
flowchart LR
  M[Master protocol] --> SC[Shared control]
  M --> A1[Arm A]
  M --> A2[Arm B]
  M --> A3[Arm C - added later]
  A1 --> INT{Interim}
  INT -->|futile| DROP[Drop arm]
  INT -->|promising| GRAD[Graduate]
```

Many such designs are **Bayesian**: instead of a fixed p-value, they update a
**posterior** belief about the treatment effect as data accrue, $P(\theta \mid
data) \propto P(data \mid \theta)\,P(\theta)$, and allocate patients toward
arms more likely to be winning (**response-adaptive randomization**). The payoff
is **efficiency** — fewer patients, faster answers, more patients on better
treatments — at the cost of greater statistical and operational complexity that
regulators scrutinize closely.

**Next:** watching safety once the drug is in use.
""",
        ),
        _t(
            "Pharmacovigilance and signal detection",
            "12 min",
            r"""# Pharmacovigilance and signal detection

No trial of a few thousand patients can detect a **1-in-50,000 adverse event**,
so safety surveillance continues for the product's life. **Pharmacovigilance**
is the science of detecting, assessing and preventing **adverse drug reactions
(ADRs)** after approval.

Spontaneous reports flow into large databases (FDA **FAERS**, WHO **VigiBase**)
as **Individual Case Safety Reports**. Because reporting is voluntary and
incomplete, analysts use **disproportionality analysis** to find drug–event
pairs reported more than expected. A core metric is the **Proportional Reporting
Ratio**, essentially $PRR = \frac{a/(a+b)}{c/(c+d)}$ from the 2×2 table of the
event with and without the drug.

```mermaid
flowchart LR
  R[Spontaneous reports] --> DB[Safety database]
  DB --> DA[Disproportionality / PRR]
  DA --> S{Signal?}
  S -->|Yes| EVAL[Causality + benefit-risk review]
  EVAL --> ACT[Label change / REMS / withdrawal]
  S -->|No| MON[Continue monitoring]
```

A statistical **signal** triggers a **causality assessment** (e.g. Bradford-Hill
considerations, the WHO-UMC scale) and a fresh **benefit-risk** evaluation that
can lead to a label warning, a **Risk Evaluation and Mitigation Strategy
(REMS)**, restricted use, or withdrawal. Sponsors also file **Periodic Safety
Update Reports** and run a formal **Risk Management Plan**. This is regulation as
a continuous feedback loop, not a one-time verdict.

**Next:** how AI is reshaping every stage.
""",
        ),
        _t(
            "AI and computational methods across development",
            "12 min",
            r"""# AI and computational methods across development

Computation and **machine learning** now touch the entire development arc, not
just discovery. The aim is to **fail faster, design smarter, and decide better**.

In **discovery**, structure prediction (**AlphaFold**) and generative models
propose targets and molecules. In **preclinical** work, ML predicts **ADMET**
and toxicity, and **physiologically based PK (PBPK)** and **QSP** (quantitative
systems pharmacology) models simulate exposure in virtual patients. In
**clinical** development, ML accelerates **trial design and operations**:
predicting enrolment, identifying eligible patients from electronic health
records, optimizing site selection, and powering **digital twins** and
**synthetic control arms** that borrow external/historical data to shrink trials.

```mermaid
flowchart LR
  AI[AI / ML] --> DISC[Target + molecule design]
  AI --> PK[ADMET / PBPK / QSP]
  AI --> TRIAL[Trial design + recruitment]
  AI --> PV[NLP signal detection]
  AI --> REG[Regulatory science / RWE]
```

In **safety**, **natural-language processing** mines literature, social media and
case narratives to surface signals earlier than manual review. In **regulatory
science**, agencies are building frameworks for **real-world evidence (RWE)** and
for evaluating AI/ML themselves — including **"locked" vs adaptive algorithms**
and **good machine-learning practice**. The hard problems are not accuracy alone
but **validation, bias, interpretability and reproducibility**: a model that
informs a dosing or approval decision must be as rigorously qualified as any
assay. Used well, these methods compress timelines; used carelessly, they import
hidden bias into life-and-death decisions.

**Next:** check your mastery of the regulatory and computational frontier.
""",
        ),
        _quiz(),
    ),
)


DRUG_DEVELOPMENT_REGULATORY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["DRUG_DEVELOPMENT_REGULATORY_COURSES"]
