"""Human Physiology track: Basics -> Intermediate -> Advanced.

A university-level physiology curriculum from homeostasis, cell membranes and
feedback control, through the nervous, cardiovascular and renal systems, to the
endocrine and immune systems and pharmacological targets. Lessons use
interactive ```plot blocks for quantitative relationships (Michaelis-Menten,
dose-response, ligand binding, exponential clearance, Hill cooperativity) and
```mermaid diagrams for pathways, reflex arcs and physiological control loops.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Human Physiology -- Basics -----------------------------------------------

_BASICS = SeedCourse(
    slug="physiology-basics",
    title="Human Physiology — Basics",
    description=(
        "The foundations of physiology: homeostasis and negative feedback, the "
        "cell membrane and resting potential, body fluid compartments and "
        "osmosis, how cells communicate, and the organisation of the body from "
        "cells to systems. Built on real molecular and quantitative detail with "
        "interactive plots and control-loop diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Homeostasis and feedback control",
            "10 min",
            r"""
# Homeostasis and feedback control

**Physiology** studies how living systems function. Its organising principle is
**homeostasis**: the active maintenance of a roughly constant internal
environment (the *milieu intérieur* of Claude Bernard) despite a changing
outside world. Regulated variables — core temperature near 37 °C, arterial
$pH$ near 7.40, plasma glucose, osmolality near 290 mOsm/kg — are held within
narrow bands.

Control loops have a **sensor** (e.g. carotid baroreceptors), an **integrating
centre** (often the hypothalamus or medulla), and **effectors** (muscles,
glands). Most loops use **negative feedback**: a deviation from the set point
triggers a response that opposes it, returning the variable toward target. A
few use **positive feedback** (oxytocin in labour, the action-potential
upstroke), which amplifies and must be terminated by an external event.

The corrected variable typically relaxes back exponentially toward its set
point, error decaying as $e^{-kt}$.

```mermaid
flowchart LR
  S[Stimulus: variable rises] --> R[Sensor / receptor]
  R --> C[Integrating centre]
  C --> E[Effector]
  E --> O[Response opposes change]
  O -->|negative feedback| S
```

```plot
{"title": "Error decay after a homeostatic disturbance", "xLabel": "time", "yLabel": "deviation from set point", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "negative feedback", "color": "#2563eb"}]}
```

**Next:** the cell membrane and the resting potential.
""",
        ),
        _t(
            "The cell membrane and resting potential",
            "11 min",
            r"""
# The cell membrane and resting potential

Every cell is bounded by a **phospholipid bilayer** studded with proteins. The
bilayer is nearly impermeable to ions, so transport depends on **channels**
(passive, down gradients) and **pumps** (active, against gradients). The master
pump is the **Na⁺/K⁺-ATPase**, which exports 3 Na⁺ and imports 2 K⁺ per ATP,
building the gradients that power most of physiology.

At rest the membrane is most permeable to **K⁺** (through leak channels), so the
**resting membrane potential** (about −70 mV in neurons) sits close to the
potassium equilibrium potential given by the **Nernst equation**:

$$E_{ion}=\frac{RT}{zF}\ln\frac{[ion]_{out}}{[ion]_{in}}$$

When several ions contribute, the **Goldman–Hodgkin–Katz** equation weights each
by its permeability. The pump is also slightly **electrogenic**, adding a few
millivolts of hyperpolarisation.

```mermaid
flowchart LR
  ATP[ATP] --> P[Na/K-ATPase]
  P -->|3 Na out| OUT[Outside]
  P -->|2 K in| IN[Inside]
  IN --> G[K gradient] --> RMP[Resting potential ~ -70 mV]
```

```plot
{"title": "Nernst potential for K+ vs external K+", "xLabel": "external K+ (relative)", "yLabel": "E_K (relative, log term)", "xRange": [0.1,10], "yRange": [-3,3], "grid": true, "functions": [{"expr": "log(x)", "label": "RT/F * ln([K]out/[K]in)", "color": "#2563eb"}]}
```

**Next:** body fluids, osmosis and tonicity.
""",
        ),
        _t(
            "Body fluids, osmosis and tonicity",
            "10 min",
            r"""
# Body fluids, osmosis and tonicity

Roughly **60%** of an adult's mass is water, split into the **intracellular
fluid** (ICF, ~2/3) and **extracellular fluid** (ECF, ~1/3); the ECF further
divides into **interstitial fluid** and **plasma**. The ICF is K⁺-rich; the ECF
is Na⁺-rich. The Na⁺/K⁺-ATPase maintains this asymmetry.

Water crosses membranes by **osmosis**, moving toward higher solute
concentration through **aquaporins**. **Osmolarity** counts all solute
particles; **tonicity** counts only solutes that cannot cross the membrane and
therefore drive net water movement. A cell in a **hypotonic** solution swells; in
a **hypertonic** solution it shrinks; in an **isotonic** (~290 mOsm/kg) solution
its volume is stable.

Net filtration across capillaries follows the **Starling equation**, balancing
hydrostatic and oncotic pressures:

$$J_v=K_f\,\big[(P_c-P_i)-\sigma(\pi_c-\pi_i)\big]$$

```mermaid
flowchart TB
  TBW[Total body water ~60%] --> ICF[Intracellular ~2/3]
  TBW --> ECF[Extracellular ~1/3]
  ECF --> ISF[Interstitial]
  ECF --> PL[Plasma]
```

```plot
{"title": "Cell volume vs external tonicity", "xLabel": "external osmolality (relative)", "yLabel": "relative cell volume", "xRange": [0.5,3], "yRange": [0,2], "grid": true, "functions": [{"expr": "1/x", "label": "volume ~ 1/osmolality", "color": "#16a34a"}]}
```

**Next:** how cells communicate.
""",
        ),
        _t(
            "Cell signalling and communication",
            "11 min",
            r"""
# Cell signalling and communication

Cells coordinate through chemical messengers acting over different ranges:
**endocrine** (hormones in blood), **paracrine** (local diffusion),
**autocrine** (self), and **synaptic** (neurotransmitters across a cleft). A
messenger (ligand) acts by binding a **receptor**.

Lipid-soluble signals (steroids, thyroid hormone) cross the membrane and bind
**intracellular receptors** that act as transcription factors — slow but
long-lasting. Water-soluble signals bind **cell-surface receptors**. Two great
families: **G-protein-coupled receptors (GPCRs)**, which activate enzymes like
adenylyl cyclase to make **second messengers** (cAMP, IP₃, Ca²⁺), and
**receptor tyrosine kinases (RTKs)** such as the insulin receptor.

Binding obeys a saturable, hyperbolic relationship — fractional occupancy rises
toward 1 as ligand increases, set by the dissociation constant $K_d$:

$$\theta=\frac{[L]}{[L]+K_d}$$

```mermaid
flowchart LR
  L[Ligand] --> R[GPCR]
  R --> G[G-protein]
  G --> AC[Adenylyl cyclase]
  AC --> cAMP[cAMP]
  cAMP --> PKA[Protein kinase A] --> Resp[Cellular response]
```

```plot
{"title": "Receptor occupancy vs ligand concentration", "xLabel": "ligand [L]", "yLabel": "fractional occupancy", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "theta = [L]/([L]+Kd)", "color": "#dc2626"}]}
```

**Next:** organising the body from cells to systems.
""",
        ),
        _t(
            "From cells to systems",
            "10 min",
            r"""
# From cells to systems

The body is built in a **hierarchy**: molecules form **cells**, similar cells
form **tissues**, tissues form **organs**, organs cooperate as **organ
systems**, and the systems together make the **organism**. There are four basic
tissue types — **epithelial** (covering and secreting), **connective**
(supporting, including blood and bone), **muscle** (contracting), and **nervous**
(signalling).

The organ systems are functionally interdependent. The **respiratory** and
**cardiovascular** systems jointly deliver O₂ and remove CO₂; the **renal**
system tunes fluid, electrolytes and $pH$; the **nervous** and **endocrine**
systems are the two great control systems — fast/electrical and
slow/chemical respectively. Homeostasis is the emergent property of these loops
working together.

```mermaid
flowchart LR
  M[Molecules] --> C[Cells]
  C --> T[Tissues]
  T --> O[Organs]
  O --> S[Organ systems]
  S --> B[Organism]
```

```plot
{"title": "Metabolic rate vs body mass (allometry)", "xLabel": "body mass (relative)", "yLabel": "metabolic rate (relative)", "xRange": [0.1,10], "yRange": [0,6], "grid": true, "functions": [{"expr": "x^0.75", "label": "Kleiber: rate ~ mass^0.75", "color": "#2563eb"}]}
```

**Next:** test your grasp of the foundations.
""",
        ),
        _quiz(),
    ),
)


# -- Human Physiology -- Intermediate -----------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="physiology-intermediate",
    title="Human Physiology — Intermediate",
    description=(
        "Core quantitative physiology of the excitable, cardiovascular and renal "
        "systems: the action potential and Hodgkin–Huxley framework, synaptic "
        "transmission and muscle, cardiac output and the pressure–volume loop, "
        "vascular haemodynamics, and glomerular filtration and clearance. Rich "
        "with equations, plots and system diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The action potential and Hodgkin–Huxley",
            "12 min",
            r"""
# The action potential and Hodgkin–Huxley

An **action potential (AP)** is an all-or-none spike that propagates along
excitable membranes. Subthreshold depolarisation opens **voltage-gated Na⁺
channels**; if threshold (~ −55 mV) is reached, Na⁺ influx drives a regenerative
upstroke (positive feedback) toward $E_{Na}$. Na⁺ channels then **inactivate**
and slower **voltage-gated K⁺ channels** open, repolarising and briefly
hyperpolarising the cell. The **refractory period** enforces one-way, discrete
firing.

**Hodgkin and Huxley (1952)** quantified this in the squid axon with a circuit
model. Membrane current is

$$I_m=C_m\frac{dV}{dt}+g_{Na}m^3h(V-E_{Na})+g_K n^4(V-E_K)+g_L(V-E_L)$$

where $m$, $h$ and $n$ are voltage- and time-dependent **gating variables** each
obeying first-order kinetics. The model reproduces threshold, shape and
conduction velocity, and earned the 1963 Nobel Prize.

```mermaid
flowchart LR
  D[Depolarisation to threshold] --> Na[Na+ channels open: upstroke]
  Na --> I[Na+ inactivation]
  I --> K[K+ channels open: repolarisation]
  K --> H[Hyperpolarisation] --> Rest[Resting potential]
```

```plot
{"title": "Na+ channel activation gate (sigmoid) vs voltage", "xLabel": "membrane potential (shifted, mV)", "yLabel": "open probability m_inf", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "m_inf(V)", "color": "#dc2626"}]}
```

**Next:** synapses, muscle and excitation–contraction coupling.
""",
        ),
        _t(
            "Synaptic transmission and muscle",
            "12 min",
            r"""
# Synaptic transmission and muscle

At a **chemical synapse**, the AP opens presynaptic **voltage-gated Ca²⁺
channels**; Ca²⁺ triggers SNARE-mediated fusion of vesicles, releasing
neurotransmitter that diffuses across the cleft and binds postsynaptic
receptors. At the **neuromuscular junction**, acetylcholine opens nicotinic
receptors, producing an end-plate potential that fires the muscle AP;
**acetylcholinesterase** then clears the transmitter.

In **skeletal muscle**, the AP spreads down **T-tubules** to the DHP receptor,
which couples to the **ryanodine receptor** of the sarcoplasmic reticulum,
releasing Ca²⁺. Ca²⁺ binds **troponin C**, moving tropomyosin to expose
actin-binding sites; **myosin cross-bridges** then cycle, hydrolysing ATP and
sliding filaments (the **sliding-filament** theory). Force depends on
**sarcomere length** through filament overlap — the length–tension relationship.

```mermaid
flowchart LR
  AP[Motor neuron AP] --> Ca[Ca2+ entry]
  Ca --> ACh[ACh release]
  ACh --> EPP[End-plate potential]
  EPP --> SR[SR Ca2+ release]
  SR --> XB[Cross-bridge cycling] --> F[Force]
```

```plot
{"title": "Skeletal muscle length-tension relationship", "xLabel": "sarcomere length (relative)", "yLabel": "active tension", "xRange": [0,4], "yRange": [0,1.2], "grid": true, "functions": [{"expr": "1 - abs(x-2)/2", "label": "filament overlap", "color": "#16a34a"}]}
```

**Next:** the heart as a pump and cardiac output.
""",
        ),
        _t(
            "Cardiac output and the pressure–volume loop",
            "12 min",
            r"""
# Cardiac output and the pressure–volume loop

**Cardiac output (CO)** is the volume of blood the heart ejects per minute:

$$CO = HR \times SV$$

where $HR$ is heart rate and $SV$ is **stroke volume** (end-diastolic minus
end-systolic volume). SV is set by three factors: **preload** (filling, via the
**Frank–Starling** mechanism — greater stretch yields greater force),
**afterload** (the pressure the ventricle must overcome), and **contractility**
(intrinsic strength, raised by sympathetic/β₁ stimulation).

The cardiac cycle is captured by the **pressure–volume (PV) loop**: isovolumetric
contraction, ejection, isovolumetric relaxation, and filling. The area inside is
**stroke work**; the slope of the end-systolic pressure–volume relationship
indexes contractility. The autonomic nervous system tunes all of this beat to
beat.

```mermaid
flowchart LR
  P[Preload / Frank-Starling] --> SV[Stroke volume]
  A[Afterload] --> SV
  C[Contractility] --> SV
  SV --> CO[Cardiac output]
  HR[Heart rate] --> CO
```

```plot
{"title": "Frank-Starling: stroke volume vs preload", "xLabel": "end-diastolic volume (preload)", "yLabel": "stroke volume", "xRange": [0,10], "yRange": [0,8], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "Starling curve", "color": "#2563eb"}]}
```

**Next:** blood pressure and vascular haemodynamics.
""",
        ),
        _t(
            "Vascular haemodynamics and blood pressure",
            "11 min",
            r"""
# Vascular haemodynamics and blood pressure

Blood flow through the circulation obeys an Ohm's-law analogue: flow equals
pressure difference over resistance, $Q=\Delta P/R$. Across the whole
circulation, **mean arterial pressure** drives flow against **total peripheral
resistance**:

$$MAP \approx CO \times TPR$$

Resistance is dominated by vessel **radius** through **Poiseuille's law**,
$R\propto 1/r^4$ — so small changes in arteriolar diameter produce large changes
in resistance, making arterioles the chief **resistance vessels**. MAP is
estimated clinically as $DBP + \tfrac{1}{3}(SBP-DBP)$.

Blood pressure is regulated fast by the **baroreceptor reflex** (carotid sinus
and aortic arch → medulla → autonomic outflow) and slowly by the kidneys and the
**renin–angiotensin–aldosterone system**. Veins, the **capacitance vessels**,
hold most of the blood volume.

```mermaid
flowchart LR
  BP[Arterial pressure] --> Baro[Baroreceptors]
  Baro --> Med[Medullary centre]
  Med --> ANS[Autonomic outflow]
  ANS --> HRT[HR, contractility, TPR]
  HRT --> BP
```

```plot
{"title": "Poiseuille: resistance vs vessel radius", "xLabel": "vessel radius (relative)", "yLabel": "resistance (relative)", "xRange": [0.5,3], "yRange": [0,16], "grid": true, "functions": [{"expr": "1/x^4", "label": "R ~ 1/r^4", "color": "#dc2626"}]}
```

**Next:** the kidney, filtration and clearance.
""",
        ),
        _t(
            "Renal filtration and clearance",
            "12 min",
            r"""
# Renal filtration and clearance

The kidney filters plasma, then reclaims what the body needs. At the
**glomerulus**, **net filtration pressure** is the Starling balance of glomerular
capillary hydrostatic pressure against Bowman's-space pressure and plasma oncotic
pressure. The **glomerular filtration rate (GFR)**, normally ~125 mL/min, is
$GFR = K_f \times NFP$ and is autoregulated over a wide pressure range.

**Renal clearance** measures the plasma volume cleared of a substance per unit
time:

$$C_x = \frac{U_x\,V}{P_x}$$

A solute that is freely filtered but neither reabsorbed nor secreted (inulin, or
clinically **creatinine**) gives clearance equal to GFR. Comparing a drug's
clearance to GFR reveals net reabsorption (lower) or secretion (higher). The
tubule then fine-tunes Na⁺, water (via **ADH/aquaporin-2**), K⁺ and $pH$ to keep
the ECF constant.

```mermaid
flowchart LR
  GC[Glomerular capillary] --> F[Filtration]
  F --> PT[Proximal tubule: bulk reabsorption]
  PT --> LH[Loop of Henle: concentration]
  LH --> DT[Distal tubule + collecting duct: fine tuning]
  DT --> U[Urine]
```

```plot
{"title": "Tubular reabsorption (saturable transport, e.g. glucose Tm)", "xLabel": "plasma concentration", "yLabel": "reabsorption rate", "xRange": [0,10], "yRange": [0,9], "grid": true, "functions": [{"expr": "8*x/(1+x)", "label": "transport maximum (Tm)", "color": "#16a34a"}]}
```

**Next:** check your quantitative understanding.
""",
        ),
        _quiz(),
    ),
)


# -- Human Physiology -- Advanced ---------------------------------------------

_ADVANCED = SeedCourse(
    slug="physiology-advanced",
    title="Human Physiology — Advanced",
    description=(
        "State-of-the-art and applied physiology: endocrine feedback and "
        "receptor enzyme kinetics, integrative glucose and energy regulation, "
        "the immune response, receptor pharmacology and dose–response, "
        "pharmacokinetics and clearance, and computational/AI methods such as "
        "physiome modelling and ML for physiological signals."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Endocrine feedback and enzyme kinetics",
            "12 min",
            r"""
# Endocrine feedback and enzyme kinetics

The **endocrine system** runs on hierarchical **negative-feedback axes**. The
**hypothalamic–pituitary–adrenal (HPA)** axis is canonical: CRH → ACTH →
cortisol, with cortisol feeding back to suppress both upstream steps. Pulsatile
and circadian secretion patterns are layered on top, and **set-point** changes
underlie many endocrine diseases.

Hormone action and metabolism are governed by **enzyme kinetics**.
**Michaelis–Menten** describes a saturable enzyme (or transporter):

$$v=\frac{V_{max}[S]}{K_m+[S]}$$

$K_m$ is the substrate concentration at half-maximal rate; $V_{max}$ scales with
enzyme amount. Competitive inhibitors raise apparent $K_m$; allosteric
modulation reshapes the curve. The same formalism describes hepatic and renal
drug metabolism, which becomes **saturable** at high doses (zero-order kinetics).

```mermaid
flowchart LR
  H[Hypothalamus: CRH] --> P[Pituitary: ACTH]
  P --> A[Adrenal: cortisol]
  A -->|negative feedback| H
  A -->|negative feedback| P
```

```plot
{"title": "Michaelis-Menten enzyme kinetics", "xLabel": "substrate [S]", "yLabel": "reaction velocity v", "xRange": [0,20], "yRange": [0,8], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

**Next:** integrative regulation of glucose and energy.
""",
        ),
        _t(
            "Integrative glucose and energy regulation",
            "12 min",
            r"""
# Integrative glucose and energy regulation

Plasma glucose is held near 5 mmol/L by opposing hormones. After a meal,
**β-cells** sense glucose (via GLUT2 and glucokinase → ATP → K_ATP channel
closure → Ca²⁺ entry) and secrete **insulin**, which binds an RTK to promote
glucose uptake (GLUT4) and storage. In fasting, **glucagon**, cortisol and
adrenaline raise glucose by glycogenolysis and gluconeogenesis.

Glucose-stimulated insulin secretion is **sigmoidal** and shows
**cooperativity**, well described by a **Hill function**:

$$\theta=\frac{[G]^n}{K^n+[G]^n}$$

with Hill coefficient $n>1$. This sharpens the threshold so insulin rises
steeply once glucose exceeds ~5 mmol/L. **Type 2 diabetes** is loss of insulin
sensitivity plus β-cell failure — a shifted, flattened response that integrates
liver, muscle, fat and brain signals (leptin, incretins).

```mermaid
flowchart LR
  Meal[Glucose rises] --> B[Beta cell senses glucose]
  B --> Ins[Insulin secretion]
  Ins --> U[GLUT4 uptake + glycogen storage]
  U --> G[Glucose falls]
  G -->|negative feedback| B
```

```plot
{"title": "Glucose-stimulated insulin secretion (Hill, cooperative)", "xLabel": "glucose [G]", "yLabel": "fractional insulin response", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill, n=2", "color": "#dc2626"}]}
```

**Next:** the immune system as a regulated response.
""",
        ),
        _t(
            "The immune response",
            "11 min",
            r"""
# The immune response

Host defence has two arms. **Innate immunity** is fast and germline-encoded:
barriers, complement, phagocytes (neutrophils, macrophages) and pattern-
recognition receptors (TLRs) that detect conserved microbial motifs and launch
inflammation. **Adaptive immunity** is slower but specific and remembering:
**B cells** make antibodies (humoral) and **T cells** (helper CD4⁺, cytotoxic
CD8⁺) coordinate and kill, all selected clonally from a vast receptor
repertoire.

A hallmark is **immunological memory**: a second exposure yields a faster,
larger, higher-affinity antibody response — the basis of **vaccination**.
Antibody titre during a primary response rises roughly **exponentially** as
clones proliferate before plateauing and contracting. Dysregulation produces
autoimmunity, allergy or immunodeficiency.

```mermaid
flowchart LR
  Pathogen --> Innate[Innate: phagocytes, complement, TLRs]
  Innate --> APC[Antigen presentation]
  APC --> T[T cells CD4/CD8]
  APC --> Bc[B cells -> antibodies]
  T --> Mem[Memory cells]
  Bc --> Mem
```

```plot
{"title": "Antibody titre rise during a primary response", "xLabel": "days post exposure", "yLabel": "antibody titre (relative)", "xRange": [0,10], "yRange": [0,20], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "clonal expansion phase", "color": "#16a34a"}]}
```

**Next:** receptor pharmacology and dose–response.
""",
        ),
        _t(
            "Receptor pharmacology and dose–response",
            "12 min",
            r"""
# Receptor pharmacology and dose–response

Drugs act mostly on physiological **targets**: receptors, ion channels, enzymes
and transporters. **Agonists** bind and activate; **antagonists** bind and
block. Two key parameters: **potency**, the concentration for half-maximal
effect (**EC₅₀**, often reported on a log scale), and **efficacy**, the maximal
effect a drug can produce. A **partial agonist** has lower efficacy than a full
agonist even when fully bound.

The classic **dose–response curve** is sigmoidal on a log-dose axis, described
by the Hill–Langmuir relation. A **competitive antagonist** shifts the curve
**rightward** (raising apparent EC₅₀) without lowering the maximum; a
**non-competitive** antagonist lowers the maximum. The **therapeutic index**,
$TI = TD_{50}/ED_{50}$, captures safety margin.

```mermaid
flowchart LR
  Drug --> Target[Receptor / channel / enzyme]
  Target -->|agonist| Act[Activation -> effect]
  Target -->|antagonist| Block[Blockade -> shift curve]
  Act --> DR[Dose-response]
  Block --> DR
```

```plot
{"title": "Sigmoidal dose-response on a log-dose axis", "xLabel": "log dose", "yLabel": "fraction of maximal effect", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "EC50 at midpoint", "color": "#dc2626"}]}
```

**Next:** pharmacokinetics and drug clearance.
""",
        ),
        _t(
            "Pharmacokinetics and clearance",
            "12 min",
            r"""
# Pharmacokinetics and clearance

**Pharmacokinetics (PK)** is what the body does to a drug, summarised by
**ADME**: absorption, distribution, metabolism, excretion. After an IV bolus,
plasma concentration of a one-compartment drug falls **exponentially** by
**first-order** kinetics:

$$C(t)=C_0\,e^{-k_e t},\qquad t_{1/2}=\frac{\ln 2}{k_e}$$

Two derived parameters dominate dosing. **Volume of distribution** $V_d=Dose/C_0$
relates body load to plasma level. **Clearance** $CL=k_e\,V_d$ is the volume of
plasma cleared per unit time and sets the **maintenance dose** at steady state:
$Dose\,rate = CL \times C_{ss}$. Steady state on repeated dosing is reached after
~4–5 half-lives. High-extraction drugs are sensitive to hepatic blood flow;
renally cleared drugs scale with GFR, so dosing is adjusted in renal impairment.

```mermaid
flowchart LR
  A[Absorption] --> D[Distribution Vd]
  D --> M[Metabolism: liver enzymes]
  D --> E[Excretion: kidney]
  M --> CL[Clearance]
  E --> CL
  CL --> Dose[Maintenance dose at Css]
```

```plot
{"title": "First-order drug elimination after an IV bolus", "xLabel": "time (half-lives)", "yLabel": "plasma concentration", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "C(t) = C0 * exp(-ke*t)", "color": "#2563eb"}]}
```

**Next:** computational and AI methods in physiology.
""",
        ),
        _t(
            "Computational and AI methods in physiology",
            "12 min",
            r"""
# Computational and AI methods in physiology

Modern physiology is increasingly **computational**. **Systems physiology** and
the **Physiome** project encode organs as ODE/PDE models — Hodgkin–Huxley
neurons, the **O'Hara–Rudy** cardiac myocyte, whole-heart electromechanics — and
solve them numerically. **PBPK** (physiologically based pharmacokinetic) models
chain compartments with organ blood flows to predict drug exposure and support
regulatory decisions. **Digital twins** personalise such models to a patient's
data.

**Machine learning** now reads physiological signals at scale: deep networks
detect arrhythmias and estimate ejection fraction from the **ECG**, score sleep
stages from EEG, and flag sepsis early from ICU time series. **Parameter
estimation** fits mechanistic models to data; **physics-informed neural
networks** blend the two. Validation against held-out data and calibration of
uncertainty remain essential before clinical use.

```mermaid
flowchart LR
  Data[Physiological signals + omics] --> Model[Mechanistic ODE/PDE model]
  Data --> ML[Machine learning model]
  Model --> DT[Digital twin]
  ML --> DT
  DT --> Clin[Prediction / decision support]
```

```plot
{"title": "Model fit error decreasing during parameter optimisation", "xLabel": "training iteration", "yLabel": "loss (relative)", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "loss decay", "color": "#16a34a"}]}
```

**Next:** prove your mastery of applied physiology.
""",
        ),
        _quiz(),
    ),
)


PHYSIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PHYSIOLOGY_COURSES"]
