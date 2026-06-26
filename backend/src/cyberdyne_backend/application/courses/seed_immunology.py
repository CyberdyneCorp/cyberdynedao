"""Immunology track: Basics -> Intermediate -> Advanced.

A university-level immunology curriculum from innate barriers, phagocytes and
inflammation, through clonal selection, antibody structure, T-cell biology and
the quantitative tools (affinity, ELISA, flow cytometry) used to measure them,
to checkpoint immunotherapy, CAR-T, vaccine design and computational epitope
prediction. Lessons use interactive ```plot blocks for quantitative
relationships (binding, dose-response, decay, growth) and ```mermaid diagrams
for signalling pathways, cell lineages and experimental pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Immunology -- Basics ------------------------------------------------------

_BASICS = SeedCourse(
    slug="immunology-basics",
    title="Immunology — Basics",
    description=(
        "The immune system from the ground up: the layered defences from "
        "physical barriers to innate and adaptive immunity, the cells and "
        "molecules of innate immunity, pattern recognition and inflammation, "
        "the complement cascade, and a first look at how lymphocytes provide "
        "specificity and memory. Built on real molecular detail with "
        "interactive plots and pathway diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What the immune system defends and how",
            "10 min",
            r"""
# What the immune system defends and how

The **immune system** is the body's defence against pathogens — viruses,
bacteria, fungi, parasites — and against transformed (cancer) cells. Its central
problem is **discrimination**: destroy what is dangerous while sparing healthy
self tissue.

Defence is **layered**. The first layer is **anatomical and chemical barriers**
(skin, mucus, low stomach pH, lysozyme). If breached, **innate immunity** reacts
within minutes to hours: it is fast, germline-encoded and the same on every
exposure. If the threat persists, **adaptive immunity** mounts a slower (days),
highly specific response that improves with experience and leaves **memory**.

```mermaid
flowchart LR
  PATH["Pathogen"] --> BAR["Barriers: skin, mucus, pH, lysozyme"]
  BAR --> INN["Innate: minutes-hours, fixed specificity"]
  INN --> ADA["Adaptive: days, clonal, memory"]
  ADA --> MEM["Immunological memory"]
```

The two arms differ in **kinetics**. A primary innate response rises and falls
quickly; the adaptive response lags but climbs higher, and on re-exposure memory
makes it faster and larger. The growth of a responding lymphocyte clone is
roughly exponential during expansion:

```plot
{"title": "Clonal expansion during a response", "xLabel": "days", "yLabel": "relative cell number", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "expanding clone", "color": "#2563eb"}]}
```

**Next:** the barriers and innate cells that meet a pathogen first.
""",
        ),
        _t(
            "Innate immunity: cells and barriers",
            "11 min",
            r"""
# Innate immunity: cells and barriers

**Innate immunity** is the rapid, evolutionarily ancient defence shared with
plants and insects. Its barriers are continuous: the **epithelium** is a
tight-junction wall, **mucus** traps microbes, **antimicrobial peptides**
(defensins, cathelicidins) puncture membranes, and **commensal flora** crowd out
invaders.

Behind the barrier wait the **innate leukocytes**, all derived from a common
**myeloid progenitor**:

```mermaid
flowchart TB
  HSC["Hematopoietic stem cell"] --> MYE["Myeloid progenitor"]
  MYE --> NEU["Neutrophil: first responder, phagocyte"]
  MYE --> MAC["Macrophage / monocyte: phagocyte, APC"]
  MYE --> DC["Dendritic cell: antigen presentation"]
  MYE --> MAST["Mast cell / basophil / eosinophil"]
  HSC --> LYM["Lymphoid progenitor"]
  LYM --> NK["NK cell: kills stressed cells"]
```

**Phagocytes** (neutrophils, macrophages) engulf microbes into a **phagosome**
that fuses with lysosomes; the **NADPH oxidase** respiratory burst floods it with
reactive oxygen species. **Natural killer (NK) cells** kill virus-infected and
tumour cells that have lowered their MHC-I ("missing-self").

Neutrophils dominate early because they are abundant and short-lived; their
numbers at a wound site spike then decay as the insult clears:

```plot
{"title": "Neutrophil recruitment then resolution", "xLabel": "hours after injury", "yLabel": "relative cell density", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "resolution phase", "color": "#dc2626"}]}
```

**Next:** how innate cells *recognise* a pathogen.
""",
        ),
        _t(
            "Pattern recognition and inflammation",
            "12 min",
            r"""
# Pattern recognition and inflammation

Innate cells recognise classes of microbes, not individual antigens, using
**pattern recognition receptors (PRRs)** that bind conserved
**pathogen-associated molecular patterns (PAMPs)** — molecules microbes cannot
easily discard, such as bacterial **LPS**, flagellin, peptidoglycan, and viral
double-stranded RNA. Damaged self releases **DAMPs** (e.g. ATP, HMGB1).

The best-known PRRs are the **Toll-like receptors (TLRs)**. TLR4 senses LPS;
TLR3 senses dsRNA; TLR9 senses unmethylated CpG DNA. Engagement signals through
adaptors (MyD88, TRIF) to activate **NF-κB**, driving transcription of
inflammatory cytokines.

```mermaid
flowchart LR
  PAMP["PAMP (e.g. LPS)"] --> TLR["TLR4 receptor"]
  TLR --> MYD["MyD88 adaptor"]
  MYD --> NFKB["NF-kB activation"]
  NFKB --> CYT["TNF, IL-1, IL-6, chemokines"]
  CYT --> INF["Inflammation: redness, heat, swelling, pain"]
```

The result is **inflammation**: vasodilation, increased vascular permeability and
**chemotaxis** of leukocytes toward the chemokine gradient. Cytokine
concentration rises with infection load in a saturating fashion, so the signal
is sensitive at low doses and plateaus at high ones:

```plot
{"title": "Cytokine output vs pathogen signal", "xLabel": "PAMP concentration (relative)", "yLabel": "cytokine output", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating response", "color": "#16a34a"}]}
```

**Next:** the complement system, the soluble arm of innate defence.
""",
        ),
        _t(
            "The complement cascade",
            "11 min",
            r"""
# The complement cascade

**Complement** is a system of ~30 plasma proteins, made mainly by the liver,
that "complements" antibody and phagocyte action. It is a **proteolytic
cascade**: each component cleaves and activates the next, amplifying the signal.

Three pathways converge on cleaving **C3** into **C3a** and **C3b**:

```mermaid
flowchart TB
  CLAS["Classical: antibody-antigen (C1q)"] --> C3["C3 convertase cleaves C3"]
  LECT["Lectin: MBL binds microbial sugars"] --> C3
  ALT["Alternative: spontaneous C3 hydrolysis on microbe"] --> C3
  C3 --> C3B["C3b: opsonization"]
  C3 --> C3A["C3a / C5a: anaphylatoxins, chemotaxis"]
  C3B --> MAC["C5-C9: Membrane Attack Complex"]
```

Complement delivers three effector functions: **opsonisation** (C3b coats
microbes for phagocytosis), **inflammation** (C3a/C5a recruit and activate
leukocytes), and **lysis** (the C5b–C9 **membrane attack complex** punches pores
in the target membrane).

Because the cascade is enzymatic, a few activated molecules generate many
products — amplification grows steeply with the number of cleavage steps:

```plot
{"title": "Cascade amplification", "xLabel": "cleavage step", "yLabel": "active molecules (relative)", "xRange": [0, 8], "yRange": [0, 20], "grid": true, "functions": [{"expr": "exp(0.35*x)", "label": "amplification", "color": "#2563eb"}]}
```

Host cells are protected by regulators (CD55, CD59) that the membrane attack
complex of complement cannot overcome on self.

**Next:** how adaptive immunity adds exquisite specificity.
""",
        ),
        _t(
            "Adaptive immunity and clonal selection",
            "12 min",
            r"""
# Adaptive immunity and clonal selection

**Adaptive immunity** is carried by **lymphocytes**: **B cells** (antibodies,
humoral immunity) and **T cells** (cell-mediated immunity). Each lymphocyte
expresses a single, randomly generated **antigen receptor** with one specificity,
created by **V(D)J recombination** that shuffles gene segments to build a
repertoire of ~10^11 distinct receptors.

The organising principle is **clonal selection** (Burnet): an antigen *selects*
the rare pre-existing lymphocytes whose receptor fits it, and those clones
**proliferate and differentiate** into effector and memory cells.

```mermaid
flowchart LR
  REP["Diverse naive repertoire"] --> ANT["Antigen enters"]
  ANT --> SEL["Selects matching clone"]
  SEL --> EXP["Clonal expansion"]
  EXP --> EFF["Effector cells: clear antigen"]
  EXP --> MEM["Memory cells: faster recall"]
```

Two consequences define adaptive immunity. **Specificity**: each clone responds
only to its antigen. **Memory**: surviving memory clones make the secondary
response faster and stronger. The secondary antibody response far exceeds the
primary at the same time point:

```plot
{"title": "Primary vs secondary antibody response", "xLabel": "days after exposure", "yLabel": "antibody titer (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "antibody rise (sigmoidal)", "color": "#dc2626"}]}
```

**Self-tolerance** — failing to react to self — is enforced during lymphocyte
development; its breakdown causes autoimmunity (covered in Advanced).

**Next:** test your grasp of the innate and adaptive fundamentals.
""",
        ),
        _quiz(),
    ),
)


# -- Immunology -- Intermediate ------------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="immunology-intermediate",
    title="Immunology — Intermediate",
    description=(
        "The core molecular and quantitative immunology: antibody structure and "
        "class switching, antigen-antibody binding kinetics and affinity, MHC "
        "and antigen presentation, T-cell activation and helper subsets, B-cell "
        "responses and the germinal center, and the laboratory methods (ELISA, "
        "flow cytometry) that quantify them. Heavy use of binding curves, "
        "dose-response plots and signalling diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Antibody structure and isotypes",
            "12 min",
            r"""
# Antibody structure and isotypes

An **antibody (immunoglobulin)** is a Y-shaped glycoprotein of two **heavy
chains** and two **light chains** linked by disulfide bonds. Each chain has a
**variable (V)** region forming the antigen-binding site and **constant (C)**
regions that define function.

```mermaid
flowchart TB
  AB["Immunoglobulin monomer"] --> FAB["2x Fab arms: antigen binding (V regions, CDRs)"]
  AB --> FC["Fc stem: effector function, receptor binding"]
  FAB --> CDR["CDR1/2/3 loops form the paratope"]
  FC --> ISO["Heavy chain class sets the isotype"]
```

The antigen-binding site is built from **complementarity-determining regions
(CDRs)** — three hypervariable loops per chain; **CDR3** is the most diverse and
contacts the **epitope** most intimately. The **affinity** of one Fab for its
epitope is described by the dissociation constant $K_d = k_{off}/k_{on}$; with
two arms, **avidity** can be far stronger.

The heavy-chain constant region defines the **isotype**:

| Isotype | Key role |
|---------|----------|
| IgM | first made; pentamer; strong complement activation |
| IgG | dominant in serum; opsonisation; crosses placenta |
| IgA | dimer in mucosal secretions |
| IgE | mast-cell arming; allergy and antiparasite |
| IgD | naive B-cell receptor |

Fractional saturation of binding sites follows a hyperbola in free antigen:

```plot
{"title": "Antibody site occupancy vs free antigen", "xLabel": "free antigen [Ag] (relative to Kd)", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy = [Ag]/([Ag]+Kd)", "color": "#2563eb"}]}
```

**Next:** quantify that binding precisely.
""",
        ),
        _t(
            "Antigen-antibody binding and affinity",
            "12 min",
            r"""
# Antigen-antibody binding and affinity

Antibody-antigen recognition is a reversible bimolecular reaction:
$\text{Ab} + \text{Ag} \rightleftharpoons \text{Ab\!-\!Ag}$. At equilibrium the
**dissociation constant** is

$$K_d = \frac{[\text{Ab}][\text{Ag}]}{[\text{Ab\!-\!Ag}]} = \frac{k_{off}}{k_{on}}$$

A small $K_d$ (nanomolar or below) means **high affinity**. The fraction of
antibody bound is $\theta = [\text{Ag}]/([\text{Ag}] + K_d)$, so $K_d$ equals the
free-antigen concentration giving half-maximal binding.

```mermaid
flowchart LR
  FREE["Free Ab + Ag"] -->|kon| BOUND["Ab-Ag complex"]
  BOUND -->|koff| FREE
  BOUND --> KD["Kd = koff/kon; avidity > affinity for multivalent"]
```

Methods to measure this: **surface plasmon resonance (SPR, Biacore)** records
real-time $k_{on}$ and $k_{off}$; **isothermal titration calorimetry** gives
thermodynamics; equilibrium **ELISA** gives apparent $K_d$. **Affinity
maturation** in germinal centres lowers $K_d$ over a response by selecting
better-mutated clones.

A higher-affinity antibody saturates at lower antigen than a lower-affinity one;
the binding hyperbola shifts left as $K_d$ falls:

```plot
{"title": "Binding hyperbola (Michaelis-Menten form)", "xLabel": "free antigen (relative)", "yLabel": "bound antibody (relative)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "Bmax*[Ag]/(Kd+[Ag])", "color": "#dc2626"}]}
```

**Next:** how T cells see antigen via MHC.
""",
        ),
        _t(
            "MHC and antigen presentation",
            "12 min",
            r"""
# MHC and antigen presentation

T cells do not recognise free antigen; they read **peptides displayed on Major
Histocompatibility Complex (MHC)** molecules. Two classes channel two sources of
antigen:

```mermaid
flowchart TB
  ENDO["Cytosolic/viral proteins"] --> PROT["Proteasome degrades"]
  PROT --> TAP["TAP transports peptides to ER"]
  TAP --> MHC1["Loaded on MHC class I"]
  MHC1 --> CD8["Presented to CD8+ T cells (all nucleated cells)"]
  EXO["Extracellular proteins"] --> ENDOC["Endocytosis / phagocytosis"]
  ENDOC --> LYSO["Endolysosomal degradation"]
  LYSO --> MHC2["Loaded on MHC class II (cleared by invariant chain)"]
  MHC2 --> CD4["Presented to CD4+ T cells (professional APCs)"]
```

**MHC-I** (HLA-A/B/C in humans) presents ~8–10-mer peptides from the cytosol to
**CD8+ cytotoxic T cells**; **MHC-II** (HLA-DR/DP/DQ) presents longer ~13–25-mer
peptides from endosomes to **CD4+ helper T cells**. MHC is the most
**polymorphic** locus in the genome, broadening the peptides a population can
present. **Dendritic cells** also use **cross-presentation** to load
extracellular antigen onto MHC-I.

Peptide binding to a given MHC allele is selective; binding probability rises
sigmoidally with the predicted binding score, the basis of epitope prediction
covered later:

```plot
{"title": "Peptide-MHC binding probability vs score", "xLabel": "binding score (relative)", "yLabel": "P(binds)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "sigmoidal threshold", "color": "#16a34a"}]}
```

**Next:** what happens when a T cell engages peptide-MHC.
""",
        ),
        _t(
            "T-cell activation and helper subsets",
            "12 min",
            r"""
# T-cell activation and helper subsets

Full T-cell activation needs **three signals**. **Signal 1**: the **T-cell
receptor (TCR)** engages peptide-MHC (with CD4 or CD8 as co-receptor).
**Signal 2**: **costimulation**, CD28 on the T cell binding B7 (CD80/86) on the
APC — without it the T cell becomes **anergic**. **Signal 3**: cytokines that
direct differentiation.

```mermaid
flowchart LR
  TCR["Signal 1: TCR-pMHC"] --> ACT["T-cell activation"]
  CD28["Signal 2: CD28-B7 costimulation"] --> ACT
  CYT["Signal 3: cytokine milieu"] --> ACT
  ACT --> IL2["IL-2 production, proliferation"]
  IL2 --> DIFF["Differentiate into effector subset"]
```

The cytokine milieu polarises naive **CD4+** cells into helper subsets:
**Th1** (IFN-γ; intracellular pathogens, activates macrophages), **Th2** (IL-4/5/13;
helminths, allergy), **Th17** (IL-17; extracellular bacteria/fungi), **Tfh**
(helps B cells in germinal centres), and **Treg** (FoxP3; suppression, tolerance).
**CD8+** cells become **cytotoxic T lymphocytes** that kill via perforin/granzyme
and Fas.

T-cell proliferation depends on **IL-2** in a saturating, dose-dependent way:

```plot
{"title": "T-cell proliferation vs IL-2", "xLabel": "IL-2 concentration (relative)", "yLabel": "proliferation (relative)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating IL-2 response", "color": "#2563eb"}]}
```

**Next:** the B-cell side and the germinal centre.
""",
        ),
        _t(
            "B-cell responses and the germinal center",
            "12 min",
            r"""
# B-cell responses and the germinal center

When a naive **B cell** binds antigen through its **B-cell receptor** and
receives help from a **Tfh** cell, it can form a **germinal centre (GC)** in a
lymph node follicle — the engine of high-quality antibody.

Two processes act in the GC, both driven by the enzyme **activation-induced
cytidine deaminase (AID)**:

```mermaid
flowchart TB
  GC["Germinal center"] --> SHM["Somatic hypermutation (AID): mutate V regions"]
  SHM --> SEL["Selection: best binders capture antigen and Tfh help survive"]
  SEL --> MAT["Affinity maturation: average Kd falls"]
  GC --> CSR["Class-switch recombination (AID): IgM -> IgG/IgA/IgE"]
  MAT --> PC["Plasma cells: secrete antibody"]
  MAT --> MBC["Memory B cells"]
```

**Somatic hypermutation** randomly mutates the variable region; **selection** by
limited antigen and Tfh help favours higher-affinity variants, so the population
average affinity rises — **affinity maturation**. **Class-switch recombination**
swaps the heavy-chain constant region (IgM to IgG/IgA/IgE) to change effector
function while keeping specificity.

Across rounds of GC selection the mean dissociation constant decays steeply, i.e.
affinity ($1/K_d$) climbs:

```plot
{"title": "Affinity maturation across GC rounds", "xLabel": "selection round", "yLabel": "mean Kd (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "falling Kd = rising affinity", "color": "#dc2626"}]}
```

**Plasma cells** (some long-lived in bone marrow) secrete antibody; **memory B
cells** await re-challenge.

**Next:** consolidate the molecular and quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Immunology -- Advanced ----------------------------------------------------

_ADVANCED = SeedCourse(
    slug="immunology-advanced",
    title="Immunology — Advanced",
    description=(
        "State-of-the-art and applied immunology: immune tolerance and the "
        "mechanisms of autoimmunity, checkpoint-blockade and engineered cell "
        "therapies (CAR-T), modern vaccine platforms including mRNA, the "
        "quantitative immunology toolkit (flow cytometry, single-cell and "
        "repertoire sequencing), and computational/AI methods for epitope and "
        "structure prediction. Combines mechanistic depth with the dosing, "
        "binding and decay curves practitioners model."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Immune tolerance and autoimmunity",
            "13 min",
            r"""
# Immune tolerance and autoimmunity

**Tolerance** is the active process of not attacking self. **Central tolerance**
deletes strongly self-reactive lymphocytes during development: in the thymus,
**AIRE**-driven expression of peripheral self-antigens enables **negative
selection** of T cells; self-reactive B cells in the marrow are deleted or edited.
**Peripheral tolerance** controls cells that escape: **anergy** (signal 1 without
2), suppression by **FoxP3+ Tregs**, and deletion.

```mermaid
flowchart TB
  CENT["Central tolerance"] --> NEG["Thymic negative selection (AIRE)"]
  CENT --> BCELL["B-cell deletion / receptor editing"]
  PERI["Peripheral tolerance"] --> ANER["Anergy: signal 1 without signal 2"]
  PERI --> TREG["Treg suppression (FoxP3, IL-10, TGF-b)"]
  PERI --> DEL["Peripheral deletion"]
  CENT --> BREAK["Breakdown -> autoimmunity"]
  PERI --> BREAK
```

When tolerance fails, **autoimmunity** results — type 1 diabetes (anti-islet
T cells), rheumatoid arthritis, multiple sclerosis, lupus (anti-nuclear
antibodies and immune complexes). Risk is shaped by **HLA alleles**, sex, and
environmental triggers including **molecular mimicry** (a microbial epitope
resembling self).

Self-reactive clones are normally rare; their frequency must stay below a
threshold for safety. The probability of clinical autoimmunity rises sharply once
autoreactive load crosses that threshold:

```plot
{"title": "Risk vs autoreactive clone burden", "xLabel": "autoreactive load (relative)", "yLabel": "P(clinical autoimmunity)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "threshold response", "color": "#dc2626"}]}
```

**Next:** turning these controls into cancer therapy.
""",
        ),
        _t(
            "Cancer immunotherapy: checkpoints and CAR-T",
            "13 min",
            r"""
# Cancer immunotherapy: checkpoints and CAR-T

Tumours evade T cells by exploiting **inhibitory checkpoints**. **CTLA-4**
outcompetes CD28 for B7 during priming; **PD-1** on T cells, engaged by **PD-L1**
on tumour cells, shuts down the effector synapse. **Checkpoint-blockade
antibodies** (anti-CTLA-4 ipilimumab; anti-PD-1 nivolumab/pembrolizumab) release
the brakes — work recognised by the 2018 Nobel Prize (Allison, Honjo).

```mermaid
flowchart LR
  TUM["Tumor PD-L1"] --> PD1["PD-1 on T cell -> exhaustion"]
  PD1 --> BLOCK["Anti-PD-1 antibody blocks"]
  BLOCK --> REACT["T cell reactivated, kills tumor"]
  TCELL["Patient T cells"] --> ENG["Engineer CAR (scFv + CD3z + costim)"]
  ENG --> EXP["Expand ex vivo"]
  EXP --> INF["Infuse: CAR-T kills CD19+ tumor"]
```

**CAR-T therapy** re-engineers a patient's T cells with a **chimeric antigen
receptor** — an antibody **scFv** for tumour antigen (e.g. **CD19**) fused to
**CD3ζ** and costimulatory domains (4-1BB or CD28). Approved for B-cell
malignancies; risks include **cytokine release syndrome**. Response correlates
with tumour antigen density, saturating once enough target is present:

```plot
{"title": "CAR-T killing vs target antigen density", "xLabel": "antigen density (relative)", "yLabel": "cytotoxicity (relative)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating cytotoxicity", "color": "#16a34a"}]}
```

**Next:** vaccines that train immunity prophylactically.
""",
        ),
        _t(
            "Vaccines and mRNA platforms",
            "13 min",
            r"""
# Vaccines and mRNA platforms

A **vaccine** primes adaptive immunity safely, generating memory so a real
infection triggers a fast, strong secondary response. Platforms span
**live-attenuated** (MMR), **inactivated** (polio IPV), **subunit/conjugate**
(HBV surface antigen, pneumococcal conjugate), **viral-vector** (adenovirus), and
**mRNA**.

```mermaid
flowchart LR
  ANT["Antigen design (e.g. stabilized spike)"] --> MRNA["mRNA encodes antigen"]
  MRNA --> LNP["Lipid nanoparticle delivery"]
  LNP --> CELL["Host cell translates antigen"]
  CELL --> APC["APC presents on MHC"]
  APC --> RESP["B + T memory generated"]
```

**mRNA vaccines** deliver nucleoside-modified, **LNP**-encapsulated mRNA that the
host translates into antigen (e.g. prefusion-stabilised spike), engaging both
antibody and T-cell arms. Advantages: rapid design, no live pathogen, scalable.
**Adjuvants** (alum, MF59, the LNP itself) supply the innate "danger" signal
needed for strong adaptive priming.

**Vaccine efficacy** is $VE = 1 - RR$, where $RR$ is the risk ratio of disease in
vaccinated vs unvaccinated. Protective antibody often wanes over time, motivating
boosters; titres decay roughly exponentially after the peak:

```plot
{"title": "Antibody titer decay after vaccination", "xLabel": "months after peak", "yLabel": "titer (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "waning immunity", "color": "#dc2626"}]}
```

**Next:** the instruments that measure all of this.
""",
        ),
        _t(
            "Quantitative immunology: flow and sequencing",
            "13 min",
            r"""
# Quantitative immunology: flow and sequencing

Modern immunology is measurement-driven. **Flow cytometry** streams cells past
lasers; fluorophore-tagged antibodies report surface and intracellular markers,
**immunophenotyping** populations (CD3, CD4, CD8, CD19) and sorting them
(**FACS**). **Mass cytometry (CyTOF)** swaps fluorophores for metal isotopes to
read ~40 parameters at once.

```mermaid
flowchart LR
  CELLS["Cell suspension + labeled antibodies"] --> FLOW["Flow cytometer: lasers + detectors"]
  FLOW --> GATE["Gating on scatter + markers"]
  GATE --> POP["Quantified populations / FACS sort"]
  POP --> SC["scRNA-seq + TCR/BCR repertoire-seq"]
  SC --> CLON["Clonotype + transcriptome per cell"]
```

**Single-cell RNA-seq** with paired **TCR/BCR repertoire sequencing** links each
cell's transcriptional state to its exact receptor sequence, revealing clonal
expansion and differentiation trajectories. **ELISPOT** counts cytokine-secreting
cells; **tetramer** staining quantifies antigen-specific T cells directly.

Repertoire diversity is summarised with ecology indices, e.g. **Shannon entropy**
$H = -\sum_i p_i \log p_i$, which falls as a response becomes **clonally
focused**. As one clone dominates (its fraction $p$ rises), the per-clone entropy
contribution behaves non-monotonically — but overall diversity collapses with
expansion, here shown as decaying effective diversity over a response:

```plot
{"title": "Repertoire diversity collapses with focusing", "xLabel": "days into response", "yLabel": "effective diversity (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "diversity decay", "color": "#2563eb"}]}
```

**Next:** computational and AI methods that predict immunity.
""",
        ),
        _t(
            "Computational and AI methods in immunology",
            "13 min",
            r"""
# Computational and AI methods in immunology

**Computational immunology** predicts what the immune system will see and target.
**Epitope prediction** estimates which peptides a given **HLA allele** presents:
tools like **NetMHCpan** and **MHCflurry** are neural networks trained on mass-
spectrometry-eluted ligands and binding-affinity data, scoring peptide-MHC pairs
to prioritise vaccine and neoantigen candidates.

```mermaid
flowchart LR
  PROT["Pathogen / tumor proteome"] --> FRAG["In-silico peptide fragments"]
  FRAG --> NN["NetMHCpan / MHCflurry: peptide-HLA binding"]
  NN --> RANK["Rank epitopes by predicted presentation"]
  RANK --> STR["AlphaFold / docking: antibody-antigen structure"]
  STR --> DES["Design vaccine / antibody candidates"]
```

For **structure**, **AlphaFold2/3** predict antibody and antigen folds and, with
docking, antibody-antigen interfaces, accelerating **rational antibody design**
and epitope mapping. **Protein language models** (ESM) and generative models now
propose novel binders. Repertoire ML classifies **disease state from TCR/BCR
sequences**.

A classifier's quality is read from its **ROC curve** and the area under it
(AUC); a useful predictor bows toward the top-left, far above the diagonal of
random guessing:

```plot
{"title": "ROC curve of an epitope classifier", "xLabel": "false positive rate", "yLabel": "true positive rate", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "good classifier (AUC > 0.5)", "color": "#16a34a"}, {"expr": "x", "label": "random (AUC = 0.5)", "color": "#dc2626"}]}
```

These methods compress experiments from years to days but still require wet-lab
validation — predicted binders must be confirmed by SPR and functional assays.

**Next:** consolidate the applied and computational frontier.
""",
        ),
        _quiz(),
    ),
)


IMMUNOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["IMMUNOLOGY_COURSES"]
