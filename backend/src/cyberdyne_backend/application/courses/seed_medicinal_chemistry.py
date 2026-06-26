"""Medicinal Chemistry track: Basics -> Intermediate -> Advanced.

A three-level track on how chemistry becomes medicine: from drug-likeness,
functional groups and binding, through SAR, bioisosteres, ADME and lead
optimization, to prodrugs, scaffolds and modern modalities (PROTACs, peptides,
covalent drugs, generative AI design). Lessons are `text` with LaTeX,
interactive ```plot blocks (dose response, kinetics, binding, free-energy) and
```mermaid diagrams for pipelines, pathways and design cycles.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Medicinal Chemistry — Basics ─────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="medicinal-chemistry-basics",
    title="Medicinal Chemistry — Basics",
    description=(
        "The foundations of drug design: what medicinal chemistry is and the "
        "discovery pipeline, drug-likeness rules (Lipinski, Veber), the "
        "functional groups and physicochemical properties that govern behaviour, "
        "how drugs bind their targets, and the basics of dose, potency and the "
        "therapeutic window. Interactive plots and pathway diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is medicinal chemistry?",
            "11 min",
            r"""
# What is medicinal chemistry?

**Medicinal chemistry** is the discipline that designs, synthesizes and optimizes
molecules that modulate a biological target to treat disease. It sits at the
intersection of organic chemistry, pharmacology and structural biology: a
medicinal chemist must reason simultaneously about *synthesis* (can we make it?),
*potency* (does it hit the target?) and *drug-likeness* (will it survive the body
and reach the site of action?).

The journey from idea to medicine is long and attritional. A typical pipeline
runs **target identification → hit discovery (screening) → hit-to-lead → lead
optimization → preclinical → clinical phases I–III → approval**. Of thousands of
compounds made, perhaps one reaches patients, and the process spans ~10–15 years.
Because attrition compounds at every stage, the surviving fraction decays roughly
exponentially across the funnel:

```plot
{"title": "Compound attrition across the discovery funnel", "xLabel": "pipeline stage", "yLabel": "fraction surviving", "xRange": [0, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.6*x)", "label": "survival", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  TI["Target ID"] --> HIT["Hit discovery"]
  HIT --> H2L["Hit-to-lead"]
  H2L --> LO["Lead optimization"]
  LO --> PRE["Preclinical"]
  PRE --> CLIN["Clinical I-III"]
  CLIN --> APP["Approval"]
```

**Next:** the rules of thumb that predict whether a molecule can be a drug.
""",
        ),
        _t(
            "Drug-likeness and the Rule of Five",
            "12 min",
            r"""
# Drug-likeness and the Rule of Five

Most *oral* drugs occupy a narrow region of chemical space. Christopher
Lipinski's **Rule of Five** (1997), derived from marketed drugs, flags poor
absorption/permeability when **two or more** of these limits are broken:

- molecular weight **MW ≤ 500** Da,
- calculated lipophilicity **cLogP ≤ 5**,
- hydrogen-bond **donors ≤ 5** (sum of OH + NH),
- hydrogen-bond **acceptors ≤ 10** (sum of N + O).

Veber's rules add **rotatable bonds ≤ 10** and **polar surface area (PSA) ≤ 140
Å²** for good oral bioavailability. These are *guidelines*, not laws — many
successful drugs (and most biologics) break them — but they keep early design
honest.

Lipophilicity (logP) is a central dial. Too low and the molecule cannot cross
membranes; too high and it is insoluble, promiscuous and metabolically labile.
Permeability rises with logP up to an optimum and then falls, giving the classic
parabolic relationship:

```plot
{"title": "Membrane permeability vs lipophilicity (parabolic)", "xLabel": "logP", "yLabel": "relative permeability", "xRange": [-2, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.15*(x-3)^2)", "label": "optimum near logP 2-3", "color": "#2563eb"}]}
```

```mermaid
flowchart TB
  RO5["Rule of Five"] --> MW["MW <= 500"]
  RO5 --> LP["cLogP <= 5"]
  RO5 --> HBD["H-bond donors <= 5"]
  RO5 --> HBA["H-bond acceptors <= 10"]
  RO5 --> VEB["Veber: rot. bonds <= 10, PSA <= 140"]
```

**Next:** the functional groups that carry a drug's activity.
""",
        ),
        _t(
            "Functional groups in drug molecules",
            "12 min",
            r"""
# Functional groups in drug molecules

A drug's **functional groups** decide how it binds, how it dissolves, and how it
is metabolized. Recurring motifs and their roles:

- **Amines** (basic): protonate at physiological pH, forming salt bridges with
  acidic residues (Asp/Glu); they also improve solubility as salts.
- **Carboxylic acids** (acidic): ionize to carboxylate, anchoring to basic
  residues but limiting passive permeability.
- **Amides**: the backbone of peptides and countless drugs; planar, H-bond donor
  and acceptor, metabolically stable.
- **Aromatic and heteroaromatic rings** (pyridine, imidazole, indole): rigid
  scaffolds providing π-stacking and shape complementarity.
- **Halogens** (F, Cl): tune lipophilicity, block metabolism, and make
  **halogen bonds**; fluorine is the medicinal chemist's favourite "magic" atom.

Ionizable groups make a drug's charge depend on pH (covered next with pKa). For a
weak base, the **fraction protonated** rises sharply as pH falls below its pKa,
following a sigmoid that governs both solubility and absorption:

```plot
{"title": "Fraction protonated of a weak base (pKa ~ 8)", "xLabel": "pH", "yLabel": "fraction ionized (BH+)", "xRange": [4, 12], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp((x-8)))", "label": "BH+ fraction", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  FG["Drug functional groups"] --> B["Amine (basic): salt bridges, salts"]
  FG --> A["Carboxylic acid: anchors, lowers permeability"]
  FG --> AM["Amide: H-bonds, stable backbone"]
  FG --> AR["(Hetero)aromatics: pi-stacking, rigidity"]
  FG --> HAL["Halogens: tune logP, block metabolism"]
```

**Next:** how physicochemical properties shape a drug's fate.
""",
        ),
        _t(
            "Physicochemical properties: pKa, logP and solubility",
            "13 min",
            r"""
# Physicochemical properties: pKa, logP and solubility

Three properties dominate a drug's *developability*:

- **pKa** sets the ionization state at a given pH. The Henderson–Hasselbalch
  relation, $\mathrm{pH} = \mathrm{p}K_a + \log_{10}\frac{[\text{A}^-]}{[\text{HA}]}$,
  predicts charge in the stomach (pH ~ 1.5), blood (pH ~ 7.4) and lysosomes. Most
  oral drugs are weak acids or bases so a neutral fraction can cross membranes.
- **logP / logD** quantify lipophilicity. **logP** is the octanol/water partition
  of the neutral species; **logD** is the *distribution* of all species at a given
  pH and is what matters for ionizable drugs in vivo.
- **Aqueous solubility** governs dissolution and dose. It typically *falls* as
  lipophilicity rises, the central tension of optimization.

The pH-partition hypothesis says only the neutral form permeates well, so
absorption is highest where the drug is least ionized. For a weak acid, the
neutral (absorbable) fraction decays as pH climbs above its pKa:

```plot
{"title": "Neutral (absorbable) fraction of a weak acid vs pH (pKa ~ 4)", "xLabel": "pH", "yLabel": "fraction neutral (HA)", "xRange": [1, 9], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp((x-4)))", "label": "neutral HA fraction", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  PC["Physicochemistry"] --> PKA["pKa: ionization vs pH"]
  PC --> LOGD["logD: lipophilicity in vivo"]
  PC --> SOL["solubility: dose & dissolution"]
  PKA --> ABS["Absorption (neutral form crosses)"]
  LOGD --> ABS
  SOL --> ABS
```

**Next:** how a drug actually grips its biological target.
""",
        ),
        _t(
            "How drugs bind their targets",
            "12 min",
            r"""
# How drugs bind their targets

A drug works by binding a **target** — most often a protein (receptor, enzyme,
ion channel or transporter) — and changing its activity. Binding is governed by
**molecular recognition**: the ligand and pocket must be complementary in *shape*
and in *chemistry*. The non-covalent forces involved, from weak to strong:

- **van der Waals / hydrophobic** contacts — many small, additive interactions;
  burying greasy surface releases ordered water (the hydrophobic effect).
- **Hydrogen bonds** — directional, ~2–8 kJ/mol each, decisive for specificity.
- **Electrostatic / salt bridges** — between charged groups, strong but
  desolvation-costly.
- **π-stacking and cation–π** — between aromatic systems and charges.

Binding affinity is reported as the **dissociation constant** $K_d$ (or $K_i$ for
inhibitors): a *lower* $K_d$ means *tighter* binding. It relates to free energy by
$\Delta G = RT\ln K_d$, so each ~1.4 kcal/mol gain at room temperature improves
affinity tenfold. The fraction of target occupied follows a saturable binding
isotherm in ligand concentration:

```plot
{"title": "Receptor occupancy vs ligand concentration (Kd = 1)", "xLabel": "[ligand] / Kd", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy = L/(L+Kd)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  L["Ligand"] -->|"shape + chemical complementarity"| C["Ligand-target complex"]
  C --> VDW["van der Waals / hydrophobic"]
  C --> HB["hydrogen bonds"]
  C --> ION["salt bridges / cation-pi"]
  C --> EFF["altered target activity"]
```

**Next:** turning binding into a measurable, useful dose.
""",
        ),
        _t(
            "Dose, potency and the therapeutic window",
            "12 min",
            r"""
# Dose, potency and the therapeutic window

Binding is necessary but not sufficient; what matters clinically is the
**dose–response** relationship. As concentration rises, response increases and
then plateaus, giving the characteristic sigmoidal curve (linear on a log-dose
axis). Two parameters summarize it:

- **Potency**, the **EC₅₀** (or IC₅₀ for inhibition) — the concentration giving
  half-maximal effect. Lower EC₅₀ = more potent.
- **Efficacy**, the maximal effect $E_{max}$ a drug can produce.

A full agonist reaches $E_{max}$; a *partial agonist* plateaus below it; an
*antagonist* produces no effect alone but blocks the agonist.

Safety is captured by the **therapeutic window**, the gap between the effective
dose and the toxic dose. The **therapeutic index** $TI = \mathrm{TD}_{50} /
\mathrm{ED}_{50}$ (or $\mathrm{LD}_{50}/\mathrm{ED}_{50}$) measures it: a larger
index means a safer drug. The efficacy curve, plotted against log dose, is the
canonical sigmoid:

```plot
{"title": "Sigmoidal dose-response (log dose)", "xLabel": "log dose", "yLabel": "response (fraction of Emax)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  D["Increasing dose"] --> EFF["Therapeutic effect (ED50)"]
  D --> TOX["Toxic effect (TD50)"]
  EFF --> TI["Therapeutic index = TD50 / ED50"]
  TOX --> TI
```

**Next:** check your understanding of drug-likeness and binding.
""",
        ),
        _quiz(),
    ),
)


# ── Medicinal Chemistry — Intermediate ───────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="medicinal-chemistry-intermediate",
    title="Medicinal Chemistry — Intermediate",
    description=(
        "The quantitative core of drug optimization: structure–activity "
        "relationships and QSAR, bioisosterism, enzyme inhibition kinetics and "
        "modes, ADME and pharmacokinetics, ligand and lipophilic efficiency "
        "metrics, and the strategies of lead optimization. Kinetics plots, "
        "binding curves and design-cycle diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Structure-activity relationships (SAR)",
            "13 min",
            r"""
# Structure-activity relationships (SAR)

The central craft of medicinal chemistry is reading the **structure–activity
relationship (SAR)**: how systematic changes to a molecule change its biological
activity. By making analogue series and measuring potency, chemists build a map
of which features the target *requires*, *tolerates*, or *rejects*.

Classic SAR moves:

- **Substituent scanning** — vary a position with groups of differing size,
  electronics and lipophilicity (the Topliss scheme orders these efficiently).
- **Homologation** — lengthen a chain to probe a pocket's depth.
- **Ring variation / scaffold hopping** — swap the core while keeping the
  pharmacophore.
- Identifying the **pharmacophore**: the minimal 3D arrangement of features
  (H-bond donor/acceptor, hydrophobe, charge) needed for activity.

A *cliff* is a small structural change causing a large activity jump — evidence
of a specific interaction. Hansch analysis correlates activity with physical
parameters; potency often tracks lipophilicity parabolically, peaking at an
optimum logP and falling on either side:

```plot
{"title": "Hansch: activity vs lipophilicity (parabolic)", "xLabel": "logP of analogue", "yLabel": "log(1/C) potency", "xRange": [-1, 7], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.25*(x-3)^2)", "label": "activity", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  CORE["Lead scaffold"] --> SUB["Substituent scan"]
  CORE --> HOM["Homologation"]
  CORE --> HOP["Scaffold hop"]
  SUB --> SAR["SAR map -> pharmacophore"]
  HOM --> SAR
  HOP --> SAR
```

**Next:** swapping groups intelligently with bioisosteres.
""",
        ),
        _t(
            "Bioisosterism",
            "12 min",
            r"""
# Bioisosterism

A **bioisostere** is a substituent or group that can replace another while
retaining similar biological activity, because the two share key physical or
electronic properties. Bioisosteric replacement is the scalpel of optimization:
it lets chemists fix a liability (metabolism, toxicity, solubility, patent space)
without losing potency.

Two families:

- **Classical** isosteres — atoms/groups with the same valence and similar size:
  $-\mathrm{CH}_2-$ / $-\mathrm{O}-$ / $-\mathrm{NH}-$ / $-\mathrm{S}-$; or
  $-\mathrm{F}$ for $-\mathrm{H}$.
- **Non-classical** isosteres — different structures with similar function: a
  **tetrazole** or acylsulfonamide for a **carboxylic acid** (same acidity and
  H-bonding, better permeability); a **bioisosteric amide** surrogate; or
  replacing a phenyl with a bicyclo[1.1.1]pentane to cut metabolism.

Fluorine deserves special mention: tiny, electron-withdrawing, it blocks
oxidative metabolism at that site, lowers pKa of nearby groups, and modulates
logP — so adding F often *extends* metabolic half-life. As more labile sites are
capped, the metabolic clearance falls and half-life rises:

```plot
{"title": "Half-life extension as labile sites are blocked", "xLabel": "metabolic blocking (e.g. F substitutions)", "yLabel": "relative half-life", "xRange": [0, 6], "yRange": [0, 6], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "t1/2", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  PROB["Liability (metabolism / tox / solubility)"] --> CL["Classical isostere (CH2/O/NH/S; H->F)"]
  PROB --> NCL["Non-classical (COOH -> tetrazole)"]
  CL --> FIX["Same activity, fixed liability"]
  NCL --> FIX
```

**Next:** how drugs that inhibit enzymes do so, kinetically.
""",
        ),
        _t(
            "Enzyme inhibition and kinetics",
            "14 min",
            r"""
# Enzyme inhibition and kinetics

Many drugs are **enzyme inhibitors**. To design them you must understand enzyme
kinetics. Most enzymes obey **Michaelis–Menten** kinetics: initial velocity rises
with substrate then saturates,

$$v = \frac{V_{max}\,[S]}{K_m + [S]},$$

where $K_m$ (the [S] giving half $V_{max}$) reflects substrate affinity and
$V_{max} = k_{cat}[E]$ the catalytic ceiling.

Inhibitors act by distinct **modes**:

- **Competitive** — binds the active site, competes with substrate; raises
  apparent $K_m$, $V_{max}$ unchanged (outcompeted by excess substrate).
- **Non-competitive / mixed** — binds elsewhere (allosteric); lowers $V_{max}$.
- **Uncompetitive** — binds only the enzyme–substrate complex.
- **Irreversible / covalent** — forms a permanent bond (e.g. aspirin acetylating
  COX); potency is measured by $k_{inact}/K_I$, not a simple $K_i$.

The hyperbolic Michaelis–Menten curve underlies all of this — half-saturation at
$[S]=K_m$:

```plot
{"title": "Michaelis-Menten kinetics (Km = 2)", "xLabel": "[S]", "yLabel": "velocity v", "xRange": [0, 20], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  E["Enzyme"] --> COMP["Competitive: active site, Km up"]
  E --> NONC["Non-competitive: allosteric, Vmax down"]
  E --> UNC["Uncompetitive: binds ES only"]
  E --> COV["Irreversible/covalent: kinact/KI"]
```

**Next:** what the body does to the drug — ADME.
""",
        ),
        _t(
            "ADME and pharmacokinetics",
            "14 min",
            r"""
# ADME and pharmacokinetics

A drug must survive a hostile journey. **ADME** describes its fate:

- **Absorption** — crossing the gut wall; depends on solubility, permeability
  (Caco-2, PAMPA assays) and first-pass metabolism. **Bioavailability (F)** is
  the fraction reaching systemic circulation.
- **Distribution** — partitioning into tissues; the **volume of distribution**
  $V_d$ and plasma-protein binding control free (active) concentration.
- **Metabolism** — chiefly hepatic **cytochrome P450** oxidation (CYP3A4, CYP2D6,
  CYP2C9) in **Phase I**, then **Phase II** conjugation (glucuronidation,
  sulfation) to water-soluble, excretable metabolites. CYP inhibition/induction
  drives **drug–drug interactions**.
- **Excretion** — renal and biliary clearance.

Pharmacokinetics models the resulting concentration–time curve. After an IV dose,
plasma concentration usually declines by **first-order elimination**,
$C(t) = C_0 e^{-k_e t}$, with **half-life** $t_{1/2} = \ln 2 / k_e$ and
**clearance** $CL = k_e V_d$. The exponential decay sets dosing intervals:

```plot
{"title": "First-order plasma decay after a dose", "xLabel": "time (half-lives)", "yLabel": "plasma concentration (fraction)", "xRange": [0, 8], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.69*x)", "label": "C(t) = C0 exp(-ke t)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  DOSE["Oral dose"] --> A["Absorption (F)"]
  A --> DIST["Distribution (Vd, protein binding)"]
  DIST --> MET["Metabolism (CYP450, Phase I/II)"]
  MET --> EXC["Excretion (renal/biliary)"]
```

**Next:** the efficiency metrics that keep optimization honest.
""",
        ),
        _t(
            "Ligand efficiency and optimization metrics",
            "12 min",
            r"""
# Ligand efficiency and optimization metrics

Raw potency can mislead — you can always add greasy bulk to push affinity while
ruining drug-likeness. **Efficiency metrics** normalize potency by the cost of
achieving it, keeping molecules lean.

- **Ligand efficiency (LE):** binding energy per heavy atom,
  $\mathrm{LE} = \dfrac{\Delta G}{N_{\text{heavy}}} \approx \dfrac{-1.4\,\log
  \mathrm{IC}_{50}}{N_{\text{heavy}}}$ (kcal/mol per atom). A useful target is
  LE ≳ 0.3; fragments start high and you must *defend* LE as you grow them.
- **Lipophilic efficiency (LipE / LLE):** $\mathrm{LLE} = \mathrm{pIC}_{50} -
  \mathrm{logP}$, rewarding potency that does *not* come from lipophilicity;
  LLE ≳ 5 is a healthy lead.

These metrics fight **molecular obesity** — the drift to high MW and logP that
correlates with attrition. Because LE divides a slowly growing affinity by a
linearly growing atom count, naive "just add atoms" optimization causes LE to
*decline* as the molecule swells:

```plot
{"title": "Ligand efficiency tends to fall as molecules grow", "xLabel": "heavy-atom count", "yLabel": "ligand efficiency (relative)", "xRange": [10, 50], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "12/x", "label": "LE ~ dG / N", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  POT["Potency (pIC50, dG)"] --> LE["LE = dG / heavy atoms"]
  POT --> LLE["LLE = pIC50 - logP"]
  LE --> LEAN["Lean, drug-like leads"]
  LLE --> LEAN
```

**Next:** putting it together — the lead optimization cycle.
""",
        ),
        _t(
            "Lead optimization strategy",
            "13 min",
            r"""
# Lead optimization strategy

**Lead optimization** is the iterative refinement of a validated lead into a
preclinical candidate, balancing many objectives at once: potency, selectivity,
ADME, safety, solubility and synthesizability. No single property wins — the goal
is a **multi-parameter optimization (MPO)** sweet spot.

The engine is the **design–make–test–analyze (DMTA)** cycle: propose analogues
(now often with computational scoring), synthesize them, assay potency and ADME,
then feed results back into the next design round. Each turn tightens the SAR and
fills the **property profile**.

Key strategies:

- **Selectivity** — design out off-target activity (e.g. against related kinases
  or the hERG channel that causes cardiotoxicity).
- **Metabolic stabilization** — block soft spots (fluorination, deuteration,
  ring fusion) identified by metabolite ID.
- **Solubility/permeability balance** — add polarity or break planarity to lift
  solubility without killing permeability.

Because each DMTA cycle yields diminishing but compounding gains, the candidate's
overall quality score rises toward a plateau as cycles accumulate:

```plot
{"title": "Candidate quality improves and plateaus over DMTA cycles", "xLabel": "DMTA cycle number", "yLabel": "multi-parameter score", "xRange": [0, 12], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1-exp(-0.35*x)", "label": "MPO score", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  DES["Design (MPO + modeling)"] --> MAKE["Make (synthesis)"]
  MAKE --> TEST["Test (potency + ADME + safety)"]
  TEST --> ANAL["Analyze (SAR update)"]
  ANAL --> DES
  ANAL --> CAND["Preclinical candidate"]
```

**Next:** check your understanding of SAR, kinetics and optimization.
""",
        ),
        _quiz(),
    ),
)


# ── Medicinal Chemistry — Advanced ───────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="medicinal-chemistry-advanced",
    title="Medicinal Chemistry — Advanced",
    description=(
        "State-of-the-art design strategies and modalities: prodrugs and "
        "soft-drug design, fragment-based and structure-based drug design, "
        "scaffold strategy and macrocycles, covalent inhibitors and targeted "
        "protein degradation (PROTACs), beyond-Rule-of-Five modalities "
        "(peptides, oligonucleotides, antibody-drug conjugates), and "
        "computational and AI/ML methods for generative design. Free-energy, "
        "kinetics and pipeline diagrams throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Prodrugs and soft drugs",
            "13 min",
            r"""
# Prodrugs and soft drugs

A **prodrug** is an inactive (or less active) derivative that is converted *in
vivo* to the active drug, used to fix a delivery problem that the active molecule
cannot solve directly:

- **Solubility / dissolution** — phosphate esters (fosphenytoin) hydrolyzed by
  phosphatases.
- **Permeability** — esterify a polar acid (enalapril → enalaprilat) so it
  crosses membranes, then carboxylesterases unmask it.
- **Targeting** — capecitabine is activated to 5-FU preferentially in tumour
  tissue; antibody-directed and PSA-cleaved prodrugs localize action.

The reverse idea is the **soft drug**: an active molecule deliberately designed
with a metabolically labile group so it is *rapidly* deactivated after acting
(e.g. esmolol, remifentanil), giving short, controllable duration and low
systemic toxicity.

The active-drug concentration after a prodrug dose rises as the prodrug is
converted, then falls as the drug is cleared — a rise-and-fall profile set by the
two rate constants (here conversion faster than elimination):

```plot
{"title": "Active-drug concentration after a prodrug dose", "xLabel": "time (relative)", "yLabel": "active drug concentration", "xRange": [0, 12], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.3*x)-exp(-1.2*x)", "label": "rise then clearance", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  PD["Prodrug (inactive)"] -->|"enzymatic conversion"| AD["Active drug"]
  AD --> EFF["Therapeutic effect"]
  AD -->|"soft drug: fast deactivation"| OUT["Inactive metabolite"]
```

**Next:** building potency from tiny starting points — fragments and structure.
""",
        ),
        _t(
            "Fragment-based and structure-based design",
            "14 min",
            r"""
# Fragment-based and structure-based design

**Structure-based drug design (SBDD)** uses an experimental 3D structure of the
target — from **X-ray crystallography, cryo-EM or NMR** — to design ligands that
complement the binding pocket. With the pocket in hand, chemists place H-bonds,
fill hydrophobic subpockets and avoid steric clashes rationally, often guided by
**molecular docking**.

**Fragment-based drug discovery (FBDD)** starts even smaller. Very small,
low-affinity fragments (the "**Rule of Three**": MW ≤ 300, ≤ 3 H-bond
donors/acceptors, cLogP ≤ 3) are screened by sensitive biophysics — **SPR**,
**thermal shift**, **ligand-observed NMR** or X-ray. Hits bind weakly
(mM–μM) but with high **ligand efficiency**; they are then **grown**, **linked**,
or **merged** into potent leads while *defending* LE.

Because fragments sample chemical space far more efficiently per compound, a small
fragment library covers a target's pharmacophore space that would need an
enormous HTS deck. The expected number of distinct binding motifs found rises
steeply, then saturates, with library size:

```plot
{"title": "Pharmacophore coverage vs fragment library size", "xLabel": "fragments screened (relative)", "yLabel": "binding motifs found", "xRange": [0, 12], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "coverage", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  STR["Target structure (X-ray/cryo-EM/NMR)"] --> DOCK["Docking & SBDD"]
  FRAG["Fragment screen (SPR/NMR/X-ray)"] --> HIT["Weak, high-LE fragments"]
  HIT -->|"grow / link / merge"| LEAD["Potent lead"]
  DOCK --> LEAD
```

**Next:** choosing and shaping the molecular scaffold.
""",
        ),
        _t(
            "Scaffolds, privileged structures and macrocycles",
            "13 min",
            r"""
# Scaffolds, privileged structures and macrocycles

The **scaffold** is a molecule's core framework, presenting substituents in a
fixed 3D arrangement. Some scaffolds — **privileged structures** like the
benzodiazepine, indole, biphenyl, and 2-aminopyrimidine cores — recur across many
drug classes because they bind diverse targets productively.

Strategic moves on the scaffold:

- **Rigidification** — locking a flexible chain into a ring pays back entropy on
  binding, raising affinity and selectivity (conformational restriction).
- **Scaffold hopping** — replacing the core with a topologically distinct one
  that keeps the pharmacophore, to escape patents or fix properties.
- **Fraction sp³ (Fsp³)** — adding three-dimensionality (more sp³ carbons,
  fewer flat aromatics) improves solubility and success rates ("escape from
  flatland").

**Macrocycles** (rings ≥ 12 atoms) sit in *beyond-Rule-of-Five* space yet can be
orally active: they bind large, flat protein–protein interfaces and, through
intramolecular H-bonds, can shield polarity to stay permeable. Rigidifying a
ligand reduces the entropic penalty of binding, so affinity (lower binding
free energy) improves as flexible rotatable bonds are removed:

```plot
{"title": "Binding free energy improves with rigidification", "xLabel": "rotatable bonds removed", "yLabel": "binding dG (relative, lower=better)", "xRange": [0, 6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "dG (more negative)", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  SC["Scaffold"] --> PRIV["Privileged structures (benzodiazepine, indole)"]
  SC --> RIG["Rigidification (entropy payback)"]
  SC --> HOP["Scaffold hopping"]
  SC --> MAC["Macrocycles (bRo5, PPI targets)"]
```

**Next:** modalities beyond classic reversible binders.
""",
        ),
        _t(
            "Covalent inhibitors and targeted protein degradation",
            "14 min",
            r"""
# Covalent inhibitors and targeted protein degradation

Two modern modalities break the reversible-binding mould.

**Covalent inhibitors** form a bond to the target, usually via a mild
**electrophilic warhead** (acrylamide, chloroacetamide) reacting with a pocket
cysteine. They give durable, near-irreversible inhibition (effect outlasts plasma
exposure) and high potency, but demand careful warhead tuning to avoid off-target
reactivity. Potency is governed by the two-step model: reversible recognition
($K_I$) then covalent capture ($k_{inact}$), summarized by $k_{inact}/K_I$.
Targeted covalent drugs include the BTK inhibitor ibrutinib and the KRAS^G12C
drug sotorasib.

**Targeted protein degradation (TPD)** is *event-driven* rather than
occupancy-driven. A **PROTAC** (proteolysis-targeting chimera) is a bifunctional
molecule: a target-binding ligand, a linker, and an **E3 ligase** recruiter
(e.g. cereblon, VHL). It forms a **ternary complex** that tags the target with
ubiquitin for proteasomal destruction — then releases and acts again
**catalytically**, so sub-stoichiometric, low-occupancy molecules can eliminate
the whole protein. **Molecular glues** (lenalidomide) do this without an obvious
linker.

PROTAC efficacy shows a **hook effect**: at high concentration the two ends
saturate separately and block productive ternary-complex formation, so degradation
*falls* — a bell-shaped curve:

```plot
{"title": "PROTAC ternary complex / degradation (hook effect)", "xLabel": "log [PROTAC]", "yLabel": "ternary complex (relative)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.4*(x-5)^2)", "label": "bell-shaped response", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  PRO["PROTAC: target ligand - linker - E3 binder"] --> TC["Ternary complex (target + E3)"]
  TC --> UBI["Ubiquitination"]
  UBI --> DEG["Proteasomal degradation"]
  DEG -->|"catalytic recycle"| PRO
```

**Next:** larger modalities that leave small-molecule space behind.
""",
        ),
        _t(
            "Beyond small molecules: peptides, oligonucleotides and conjugates",
            "13 min",
            r"""
# Beyond small molecules: peptides, oligonucleotides and conjugates

When a target is "undruggable" by small molecules — a flat protein–protein
interface, an RNA, or a gene — larger modalities take over.

- **Therapeutic peptides** access PPIs and receptors with high specificity but
  suffer protease degradation and poor oral uptake; chemists fight back with
  D-amino acids, N-methylation, **stapled** (cross-linked α-helix) and cyclic
  peptides, and lipidation (semaglutide).
- **Oligonucleotides** act on the genetic message: **antisense (ASO)** and
  **siRNA** silence target mRNAs; the chemistry (phosphorothioate backbone,
  2′-MOE/LNA sugars, **GalNAc** conjugation for liver delivery) is the whole
  battle for stability and uptake.
- **Antibody–drug conjugates (ADCs)** marry an antibody's targeting to a potent
  cytotoxic **payload** via a cleavable or non-cleavable **linker**, widening the
  therapeutic window for oncology.
- **mRNA and gene therapies** deliver instructions rather than drugs.

These modalities trade developability for reach: as **molecular size grows**,
accessible target space *expands* but oral bioavailability *collapses*, a defining
tension of modern pharma. Oral bioavailability falls sharply with molecular
weight beyond the small-molecule regime:

```plot
{"title": "Oral bioavailability declines with molecular size", "xLabel": "molecular weight (relative)", "yLabel": "oral bioavailability (relative)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "oral F", "color": "#dc2626"}]}
```

```mermaid
flowchart TB
  TARG["Undruggable target"] --> PEP["Peptides (stapled/cyclic)"]
  TARG --> OLI["Oligonucleotides (ASO/siRNA, GalNAc)"]
  TARG --> ADC["Antibody-drug conjugates"]
  TARG --> GEN["mRNA / gene therapy"]
```

**Next:** computation and AI that now drive design.
""",
        ),
        _t(
            "Computational and AI methods in drug design",
            "14 min",
            r"""
# Computational and AI methods in drug design

Modern medicinal chemistry is increasingly *computational*. The layers:

- **Physics-based modeling:** **molecular docking** poses ligands in a pocket;
  **molecular dynamics** samples flexibility; **free-energy perturbation (FEP)**
  predicts relative binding affinities of analogues to ~1 kcal/mol, ranking
  designs *before* synthesis. **QM/MM** treats reactive or covalent steps.
- **Cheminformatics & QSAR:** molecules encoded as **SMILES** or fingerprints;
  tools like RDKit compute descriptors; ADMET predictors (e.g. for CYP
  inhibition, hERG, solubility) flag liabilities early.
- **Machine learning & generative AI:** **graph neural networks** predict potency
  and ADMET from molecular graphs; **generative models** (VAEs, transformers,
  diffusion) and **reinforcement-learning** design (REINVENT) invent novel,
  synthesizable molecules optimized for a multi-parameter scoring function;
  **AlphaFold**-class structure prediction supplies targets for SBDD; and
  **active learning** chooses the most informative next compounds to make.

ML model error decays predictably with training-set size — the empirical scaling
law that justifies assembling large, high-quality bioactivity datasets (ChEMBL,
proprietary screens):

```plot
{"title": "ML potency-prediction error vs training-set size", "xLabel": "training examples (relative)", "yLabel": "prediction error (relative)", "xRange": [1, 20], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "error ~ 1/sqrt(N)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  M["Molecule (SMILES / graph)"] --> PHYS["Docking / MD / FEP"]
  M --> QSAR["QSAR & ADMET prediction"]
  M --> GEN["Generative AI (RL / diffusion)"]
  GEN --> DESIGN["Proposed candidates"]
  PHYS --> DESIGN
  QSAR --> DESIGN
  DESIGN -->|"active learning"| M
```

**Next:** check your understanding of modalities and modern methods.
""",
        ),
        _quiz(),
    ),
)


MEDICINAL_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MEDICINAL_CHEMISTRY_COURSES"]
