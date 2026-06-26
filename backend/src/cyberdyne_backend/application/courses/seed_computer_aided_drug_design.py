"""Computer-Aided Drug Design (CADD) track: Basics -> Intermediate -> Advanced.

A three-level track on rational drug discovery. Basics builds intuition for the
discovery pipeline, targets, ligand-receptor binding and ADMET; Intermediate
covers the core quantitative methods (molecular docking, scoring functions,
pharmacophores, QSAR, molecular dynamics, free-energy calculations); Advanced
treats fragment-based and de novo design, generative AI/ML models and applied
case studies. Lessons are `text` with LaTeX, interactive ```plot blocks
(binding, dose-response, kinetics, enrichment) and ```mermaid pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── CADD — Basics ─────────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="computer-aided-drug-design-basics",
    title="Computer-Aided Drug Design (CADD) — Basics",
    description=(
        "An intuitive introduction to rational drug discovery: the long "
        "pipeline from target to approved medicine, what makes a good drug "
        "target, how small molecules bind receptors and the thermodynamics of "
        "affinity, dose-response and the meaning of potency, drug-likeness "
        "rules, and the ADMET properties that decide whether a hit ever "
        "becomes a drug. Interactive binding and dose-response plots and "
        "pipeline diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The drug discovery pipeline",
            "10 min",
            r"""
# The drug discovery pipeline

Bringing a new medicine to patients takes 10–15 years and often exceeds US$1–2
billion, with attrition at every stage. **Computer-aided drug design (CADD)**
aims to make the early stages faster, cheaper and more rational by predicting
which molecules are worth synthesising and testing.

The pipeline begins with **target identification and validation** — choosing a
protein (or nucleic acid) whose modulation should treat disease. **Hit
discovery** then finds molecules that bind that target, via high-throughput
screening (HTS) or *in silico* (virtual) screening. Promising **hits** are
optimised into **leads** with better potency and properties, then refined in
**lead optimisation** before **preclinical** animal studies and three phases of
**clinical trials** in humans.

```mermaid
flowchart LR
  T["Target ID & validation"] --> H["Hit discovery (HTS / virtual screening)"]
  H --> L["Hit-to-lead"]
  L --> LO["Lead optimisation"]
  LO --> PC["Preclinical (ADMET, tox)"]
  PC --> CT["Clinical trials I-III"]
  CT --> A["Regulatory approval"]
```

Attrition is brutal: of thousands of screened molecules, only one may reach the
market. Success probability compounds across stages, so even modest per-stage
gains multiply:

```plot
{"title": "Surviving compounds across pipeline stages", "xLabel": "stage number", "yLabel": "fraction surviving", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "fraction = exp(-0.5·stage)", "color": "#2563eb"}]}
```

**Next:** what makes a protein a good drug target.
""",
        ),
        _t(
            "Drug targets and druggability",
            "10 min",
            r"""
# Drug targets and druggability

Most marketed drugs act on a handful of protein families: **enzymes** (e.g.
kinases, proteases, HMG-CoA reductase), **G-protein-coupled receptors (GPCRs)**,
**ion channels** and **nuclear receptors**. A useful target must be both
**disease-relevant** (modulating it changes the disease) and **druggable** — it
must possess a binding pocket that a small molecule can occupy with high
affinity and selectivity.

**Druggability** depends on the geometry and chemistry of the binding site: a
well-defined, partly hydrophobic concave pocket of moderate size is ideal.
Flat protein-protein interfaces are notoriously hard. Tools such as fpocket,
SiteMap and DoGSiteScorer estimate pocket volume, enclosure and hydrophobicity
to score druggability before any chemistry begins.

```mermaid
flowchart TB
  TGT["Candidate target"] --> DR{"Disease-relevant?"}
  DR -->|no| REJ["Reject"]
  DR -->|yes| DG{"Druggable pocket?"}
  DG -->|no| REJ
  DG -->|yes| SEL{"Achievable selectivity?"}
  SEL -->|yes| GO["Validated target"]
```

Target validation uses genetics (knockouts, GWAS), chemical probes and clinical
evidence. A target's **expression** or activity often rises with disease
severity, motivating its modulation:

```plot
{"title": "Target activity vs disease severity", "xLabel": "disease severity", "yLabel": "relative target activity", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating rise", "color": "#dc2626"}]}
```

**Next:** how a drug actually binds its target.
""",
        ),
        _t(
            "Ligand-receptor binding and affinity",
            "11 min",
            r"""
# Ligand-receptor binding and affinity

A drug (**ligand**, L) and its target (**receptor**, R) associate reversibly:
$\mathrm{R} + \mathrm{L} \rightleftharpoons \mathrm{RL}$. At equilibrium the
**dissociation constant** is
$$K_d = \frac{[\mathrm{R}][\mathrm{L}]}{[\mathrm{RL}]}.$$
A smaller $K_d$ means tighter binding; typical drugs sit in the nanomolar
($10^{-9}\,\mathrm{M}$) range. The fraction of receptor occupied follows a
saturating (Langmuir) isotherm,
$$\theta = \frac{[\mathrm{L}]}{[\mathrm{L}] + K_d},$$
so $K_d$ equals the ligand concentration giving half-maximal occupancy.

Binding is governed by the **Gibbs free energy** $\Delta G = -RT\ln K_a =
RT\ln K_d$, with contributions from hydrogen bonds, salt bridges, van der Waals
contacts and the hydrophobic effect (enthalpy $\Delta H$ and entropy
$T\Delta S$). Shape and chemical **complementarity** between ligand and pocket
maximise favourable contacts.

```mermaid
flowchart LR
  R["Receptor + Ligand"] --> RL["Complex RL"]
  RL --> DG["ΔG = ΔH − TΔS"]
  DG --> KD["Kd = exp(ΔG/RT)"]
```

The occupancy curve is the foundation of pharmacology — note half-saturation at
$[\mathrm{L}] = K_d$:

```plot
{"title": "Receptor occupancy vs ligand concentration", "xLabel": "[L] / Kd", "yLabel": "fractional occupancy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "theta = [L]/([L]+Kd)", "color": "#2563eb"}]}
```

**Next:** turning occupancy into a measurable dose-response.
""",
        ),
        _t(
            "Dose-response, potency and efficacy",
            "11 min",
            r"""
# Dose-response, potency and efficacy

In a cell or animal, increasing drug dose produces a graded biological response
that, plotted against the **logarithm** of concentration, traces a sigmoidal
curve. Two quantities summarise it: **potency**, the concentration giving
half-maximal effect ($EC_{50}$ for agonists, $IC_{50}$ for inhibitors), and
**efficacy**, the maximal achievable response ($E_{max}$).

The standard model is the **Hill equation**,
$$E = \frac{E_{max}\,[\mathrm{D}]^{n}}{EC_{50}^{n} + [\mathrm{D}]^{n}},$$
where the **Hill coefficient** $n$ reflects cooperativity (steepness). A drug
can be highly potent (low $EC_{50}$) yet have low efficacy — a **partial
agonist**. **Antagonists** bind but produce no response, shifting agonist
curves rightward.

```mermaid
flowchart LR
  D["Dose (log scale)"] --> R["Response"]
  R --> P["Potency = EC50"]
  R --> E["Efficacy = Emax"]
  R --> H["Steepness = Hill n"]
```

On a log-concentration axis the response is the familiar S-curve, half-maximal
at the $EC_{50}$:

```plot
{"title": "Sigmoidal dose-response (log concentration)", "xLabel": "log[dose]", "yLabel": "response (fraction of Emax)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "EC50 at midpoint", "color": "#16a34a"}]}
```

**Next:** what chemical features make a molecule drug-like.
""",
        ),
        _t(
            "Drug-likeness and Lipinski's rules",
            "10 min",
            r"""
# Drug-likeness and Lipinski's rules

A potent binder is useless if it cannot reach its target. **Drug-likeness**
captures whether a molecule's physicochemical properties are compatible with
oral absorption. Christopher **Lipinski's "Rule of Five" (Ro5)** flags poor
absorption when a molecule violates two or more of: molecular weight
$\le 500\,\mathrm{Da}$; calculated lipophilicity $\log P \le 5$; hydrogen-bond
**donors** $\le 5$; hydrogen-bond **acceptors** $\le 10$.

Later refinements add **rotatable bonds** $\le 10$ and **polar surface area
(PSA)** $\le 140\,\text{Å}^2$ (Veber's rules) for good bioavailability. These
are heuristics, not laws — many natural products and antibiotics break them —
but they bias libraries toward developable chemical space.

```mermaid
flowchart TB
  M["Molecule"] --> MW["MW <= 500 Da"]
  M --> LP["logP <= 5"]
  M --> HD["H-bond donors <= 5"]
  M --> HA["H-bond acceptors <= 10"]
  MW --> RO5{"<= 1 violation?"}
  LP --> RO5
  HD --> RO5
  HA --> RO5
  RO5 -->|yes| OK["Likely orally absorbable"]
```

Lipophilicity drives membrane permeation but too much causes poor solubility
and toxicity — permeability rises with $\log P$ then plateaus:

```plot
{"title": "Membrane permeability vs lipophilicity", "xLabel": "logP", "yLabel": "relative permeability", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating permeability", "color": "#2563eb"}]}
```

**Next:** the ADMET properties that govern a drug's fate in the body.
""",
        ),
        _t(
            "ADMET: from molecule to medicine",
            "11 min",
            r"""
# ADMET: from molecule to medicine

A drug's fate in the body is summarised by **ADMET**: **A**bsorption,
**D**istribution, **M**etabolism, **E**xcretion and **T**oxicity. Poor ADMET,
not lack of potency, historically caused most clinical failures, so modern CADD
predicts these properties early.

**Absorption** depends on solubility and permeability (recall Lipinski).
**Distribution** is shaped by plasma-protein binding and the volume of
distribution. **Metabolism** is dominated by liver **cytochrome P450** enzymes
(CYP3A4, CYP2D6); their action both clears drugs and can create reactive
metabolites or drug-drug interactions. **Excretion** (renal/biliary) sets the
**half-life** $t_{1/2}$. **Toxicity** screens include hERG channel block
(cardiac risk), mutagenicity (Ames) and hepatotoxicity.

```mermaid
flowchart LR
  DOSE["Dose"] --> ABS["Absorption"]
  ABS --> DIST["Distribution"]
  DIST --> MET["Metabolism (CYP450)"]
  MET --> EXC["Excretion"]
  DIST --> TOX["Toxicity screens"]
```

Plasma concentration after a dose typically falls by **first-order
elimination**, $C(t) = C_0 e^{-k_e t}$, with half-life $t_{1/2} = \ln 2 / k_e$:

```plot
{"title": "Plasma drug concentration over time", "xLabel": "time (half-lives)", "yLabel": "concentration / C0", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "first-order decay", "color": "#dc2626"}]}
```

**Next:** test your grasp of the CADD fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── CADD — Intermediate ───────────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="computer-aided-drug-design-intermediate",
    title="Computer-Aided Drug Design (CADD) — Intermediate",
    description=(
        "The core quantitative methods of CADD. Structure-based design via "
        "molecular docking and scoring functions; pharmacophore modelling and "
        "ligand-based virtual screening by similarity; quantitative "
        "structure-activity relationships (QSAR); molecular dynamics for "
        "protein flexibility; and rigorous free-energy methods (MM-PBSA, FEP) "
        "for ranking affinity. Interactive enrichment, scoring and kinetics "
        "plots with method-pipeline diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Molecular docking",
            "12 min",
            r"""
# Molecular docking

**Docking** predicts how a ligand binds a target by searching for the
**pose** — position, orientation and conformation — that best fits the binding
site. It answers two questions: *where/how* (the search/sampling problem) and
*how well* (the scoring problem). Programs such as **AutoDock Vina**, **Glide**
and **GOLD** dominate practice.

Search algorithms include genetic algorithms (GOLD), incremental fragment
growth (DOCK, FlexX) and Monte-Carlo / gradient methods (Vina). The ligand is
usually treated as flexible (rotatable bonds sampled) against a mostly rigid
receptor — though induced-fit and ensemble docking relax this. Combinatorial
explosion of conformations is the central computational challenge.

```mermaid
flowchart LR
  REC["Prepared receptor"] --> GRID["Define binding-site grid"]
  LIG["Prepared ligand"] --> SAMP["Sample poses (search)"]
  GRID --> SAMP
  SAMP --> SCORE["Score each pose"]
  SCORE --> POSE["Top-ranked binding pose"]
```

The conformational search space grows roughly exponentially with the number of
rotatable bonds, so efficient sampling matters enormously:

```plot
{"title": "Search space vs ligand rotatable bonds", "xLabel": "rotatable bonds", "yLabel": "relative conformations", "xRange": [0, 10], "yRange": [0, 20], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "exponential growth", "color": "#dc2626"}]}
```

**Next:** the scoring functions that rank docked poses.
""",
        ),
        _t(
            "Scoring functions",
            "11 min",
            r"""
# Scoring functions

A **scoring function** estimates binding affinity (or a proxy) for a pose. Three
families exist. **Force-field-based** scores sum physics terms — van der Waals,
electrostatics, hydrogen bonds — from molecular mechanics. **Empirical** scores
(e.g. Glide SP/XP, Vina) fit weighted terms to experimental affinities.
**Knowledge-based** scores derive statistical potentials from observed atom-pair
distances in crystal structures (PMF, DrugScore).

A typical empirical form is
$$\Delta G_{bind} = \Delta G_{vdW} + \Delta G_{Hbond} + \Delta G_{elec} +
\Delta G_{desolv} + \Delta G_{rot},$$
where the last penalises lost rotational entropy on binding. No single function
is universally accurate; **consensus scoring** averages several to reduce error.
Scoring is the weakest link in docking — good at finding poses, poorer at
ranking affinities.

```mermaid
flowchart TB
  POSE["Docked pose"] --> FF["Force-field terms"]
  POSE --> EMP["Empirical fitted terms"]
  POSE --> KB["Knowledge-based potentials"]
  FF --> CS["Consensus score"]
  EMP --> CS
  KB --> CS
  CS --> RANK["Ranked compounds"]
```

The van der Waals contribution follows a Lennard-Jones-like well — attractive
at moderate distance, sharply repulsive on clash:

```plot
{"title": "van der Waals interaction energy", "xLabel": "interatomic distance (relative)", "yLabel": "energy", "xRange": [1, 6], "yRange": [-2, 4], "grid": true, "functions": [{"expr": "1/x^6*40-1/x^3*8", "label": "Lennard-Jones-like", "color": "#2563eb"}]}
```

**Next:** describing what a binder must look like with pharmacophores.
""",
        ),
        _t(
            "Pharmacophore modelling",
            "11 min",
            r"""
# Pharmacophore modelling

A **pharmacophore** is the abstract set of steric and electronic **features**
that a molecule must present to trigger (or block) a biological response —
independent of any specific scaffold. IUPAC features include hydrogen-bond
**donors** and **acceptors**, **hydrophobic** centres, **aromatic** rings and
positively/negatively **ionisable** groups, arranged in a defined 3D geometry.

Pharmacophores are built **structure-based** (from a ligand-protein complex) or
**ligand-based** (by aligning several known actives and extracting common
features). The model becomes a 3D query: screen a database for molecules whose
conformers can place matching features within tolerance spheres. Tools include
Phase, LigandScout and Pharmer.

```mermaid
flowchart LR
  ACT["Known active ligands"] --> ALIGN["3D alignment"]
  ALIGN --> FEAT["Extract common features"]
  FEAT --> QUERY["3D pharmacophore query"]
  QUERY --> SCREEN["Screen compound database"]
  SCREEN --> HITS["Candidate hits"]
```

Tighter feature-distance tolerances raise selectivity but shrink the number of
matching hits — a precision-recall trade-off:

```plot
{"title": "Hits retrieved vs tolerance radius", "xLabel": "feature tolerance (Angstrom)", "yLabel": "relative hits matched", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "more tolerance, more hits", "color": "#16a34a"}]}
```

**Next:** quantifying activity from molecular descriptors with QSAR.
""",
        ),
        _t(
            "QSAR and molecular descriptors",
            "12 min",
            r"""
# QSAR and molecular descriptors

**Quantitative structure-activity relationship (QSAR)** models learn a function
mapping molecular **descriptors** to activity, $\text{Activity} = f(d_1, d_2,
\ldots, d_n)$. The classic Hansch linear form relates potency to physicochemical
terms, e.g.
$$\log\!\left(\frac{1}{C}\right) = a\,\log P + b\,\sigma + c\,E_s + d,$$
with $\log P$ (lipophilicity), Hammett $\sigma$ (electronic) and Taft $E_s$
(steric) parameters.

Descriptors range from simple **2D** (counts, topological indices, fingerprints)
to **3D** fields (CoMFA, CoMSIA). Modern QSAR uses machine learning — random
forests, gradient boosting, neural networks — over thousands of descriptors.
**Validation** is essential: split into training/test sets, report
cross-validated $q^2$ and external $R^2$, and define the **applicability
domain** beyond which predictions are unreliable. Beware **overfitting**: too
many descriptors on too few compounds memorise noise.

```mermaid
flowchart LR
  MOL["Molecules + activities"] --> DESC["Compute descriptors"]
  DESC --> SPLIT["Train / test split"]
  SPLIT --> MODEL["Fit QSAR model"]
  MODEL --> VAL["Cross-validate (q2, R2)"]
  VAL --> PRED["Predict new molecules"]
```

Activity often rises with lipophilicity then falls (toxicity, poor solubility)
— a parabolic Hansch relationship with an optimum $\log P$:

```plot
{"title": "Activity vs lipophilicity (Hansch parabola)", "xLabel": "logP", "yLabel": "log(1/C) activity", "xRange": [0, 8], "yRange": [0, 6], "grid": true, "functions": [{"expr": "6-0.4*(x-4)^2", "label": "optimum logP", "color": "#dc2626"}]}
```

**Next:** giving the receptor flexibility with molecular dynamics.
""",
        ),
        _t(
            "Molecular dynamics simulations",
            "12 min",
            r"""
# Molecular dynamics simulations

Docking usually treats the receptor as rigid, but proteins **breathe**.
**Molecular dynamics (MD)** integrates Newton's equations of motion,
$$\mathbf{F}_i = m_i \frac{d^2 \mathbf{r}_i}{dt^2} = -\nabla_i U,$$
where the potential $U$ comes from a **force field** (AMBER, CHARMM, OPENMM /
GROMACS engines) with bonded and non-bonded terms. Femtosecond time steps
($\sim 2\,\mathrm{fs}$) are accumulated over nanoseconds-to-microseconds to
sample conformations.

In CADD, MD refines docked complexes, reveals **cryptic pockets**, generates
receptor **ensembles** for ensemble docking, and assesses complex **stability**
via RMSD/RMSF. Explicit solvent and periodic boundary conditions make it
expensive, but GPU acceleration and enhanced sampling (metadynamics, replica
exchange) extend reach.

```mermaid
flowchart LR
  INIT["System + solvent + force field"] --> EQ["Energy minimise & equilibrate"]
  EQ --> PROD["Production MD (ns-us)"]
  PROD --> ANA["Analyse RMSD / RMSF / pockets"]
  ANA --> ENS["Conformational ensemble"]
```

Complex RMSD typically rises then plateaus as the structure relaxes to a stable
basin — a hallmark of an equilibrated trajectory:

```plot
{"title": "Backbone RMSD vs simulation time", "xLabel": "time (ns)", "yLabel": "RMSD (Angstrom)", "xRange": [0, 10], "yRange": [0, 4], "grid": true, "functions": [{"expr": "3*x/(1+x)", "label": "relax then plateau", "color": "#2563eb"}]}
```

**Next:** computing binding free energies rigorously.
""",
        ),
        _t(
            "Binding free-energy methods",
            "12 min",
            r"""
# Binding free-energy methods

Ranking affinity accurately requires more physics than a docking score.
**End-point** methods such as **MM-PBSA** / **MM-GBSA** estimate
$$\Delta G_{bind} = \langle E_{MM}\rangle + \langle G_{solv}\rangle -
T\langle S\rangle,$$
combining molecular-mechanics energy, an implicit-solvent (Poisson-Boltzmann or
Generalised-Born) solvation term and an entropy estimate, averaged over MD
snapshots. They are fast but approximate.

**Alchemical** methods are the gold standard for relative affinities.
**Free-energy perturbation (FEP)** and **thermodynamic integration (TI)**
gradually mutate one ligand into another through unphysical intermediate
$\lambda$ states, using the Zwanzig relation
$$\Delta G = -k_B T \ln \langle e^{-\Delta U / k_B T}\rangle.$$
A thermodynamic cycle then yields the **relative** binding free energy
$\Delta\Delta G$ between congeneric ligands, often within ~1 kcal/mol of
experiment.

```mermaid
flowchart LR
  MD["MD snapshots"] --> MMPBSA["MM-PBSA / MM-GBSA"]
  MD --> FEP["Alchemical FEP / TI"]
  MMPBSA --> RANK["Approximate ranking"]
  FEP --> DDG["Accurate ddG"]
  DDG --> DECISION["Synthesis decision"]
```

In TI the integrand $\langle \partial U / \partial \lambda \rangle$ is
integrated over $\lambda$ from 0 to 1; the area under that curve is $\Delta G$:

```plot
{"title": "TI integrand over the alchemical path", "xLabel": "coupling parameter lambda", "yLabel": "dU/dlambda (relative)", "xRange": [0, 1], "yRange": [-2, 4], "grid": true, "functions": [{"expr": "4*x-1", "label": "integrate to get dG", "color": "#16a34a"}]}
```

**Next:** test your grasp of the quantitative CADD methods.
""",
        ),
        _quiz(),
    ),
)


# ── CADD — Advanced ───────────────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="computer-aided-drug-design-advanced",
    title="Computer-Aided Drug Design (CADD) — Advanced",
    description=(
        "State-of-the-art and applied CADD. Fragment-based drug design and the "
        "efficiency metrics that drive it; de novo molecular design and "
        "generative AI (VAEs, reinforcement learning, diffusion models); "
        "deep-learning structure prediction (AlphaFold) and structure-based "
        "generation; multi-parameter and free-energy-driven lead optimisation; "
        "and real case studies from HIV protease inhibitors to modern "
        "AI-discovered candidates. Interactive efficiency and learning plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Fragment-based drug design",
            "12 min",
            r"""
# Fragment-based drug design

**Fragment-based drug design (FBDD)** starts from very small molecules
(< 300 Da, the "Rule of Three": MW < 300, $\log P \le 3$, $\le 3$ H-bond
donors/acceptors). Fragments bind weakly (millimolar-to-micromolar $K_d$) but
sample chemical space far more efficiently than drug-sized molecules — a small
fragment library covers more of it than a huge HTS deck.

Weak binding demands sensitive **biophysical** detection: X-ray crystallography,
NMR, surface plasmon resonance (SPR) and thermal-shift assays. A confirmed
fragment, with its high-quality contacts, is then **grown**, **linked** or
**merged** into a potent lead. The guiding metric is **ligand efficiency**,
$$\mathrm{LE} = \frac{-\Delta G_{bind}}{N_{heavy}} \approx
\frac{1.37 \times pK_d}{N_{heavy}},$$
the binding energy per heavy atom — fragments excel here.

```mermaid
flowchart LR
  LIB["Fragment library"] --> SCR["Biophysical screen (X-ray/NMR/SPR)"]
  SCR --> HIT["Confirmed fragment hit"]
  HIT --> GROW["Grow / link / merge"]
  GROW --> LEAD["Potent lead"]
```

Ligand efficiency tends to dilute as molecules grow, so good campaigns add atoms
that pay their way — affinity must rise faster than heavy-atom count:

```plot
{"title": "Ligand efficiency vs molecular size", "xLabel": "heavy atom count", "yLabel": "ligand efficiency (relative)", "xRange": [5, 40], "yRange": [0, 1], "grid": true, "functions": [{"expr": "5/x", "label": "LE dilutes with size", "color": "#dc2626"}]}
```

**Next:** designing molecules from scratch with de novo methods.
""",
        ),
        _t(
            "De novo molecular design",
            "12 min",
            r"""
# De novo molecular design

**De novo design** builds novel molecules to satisfy a target, rather than
screening existing libraries. Classical structure-based approaches (LUDI,
SPROUT) grow atoms or fragments inside a binding pocket to maximise predicted
interactions, while ligand-based methods evolve structures toward a
pharmacophore or QSAR objective.

The central challenge is **navigating chemical space** — estimated at $10^{60}$
drug-like molecules — toward regions that are simultaneously potent, selective,
**synthesisable** and developable. Genetic algorithms, fragment recombination
and Monte-Carlo tree search were early engines; today **generative models**
(next lesson) dominate. Crucial guards are **synthetic accessibility (SA)**
scoring and retrosynthesis prediction, so proposed molecules can actually be
made.

```mermaid
flowchart LR
  OBJ["Design objective (pocket / pharmacophore)"] --> GEN["Generate candidate structures"]
  GEN --> EVAL["Score: affinity, ADMET, SA"]
  EVAL --> SEL["Select best"]
  SEL --> GEN
  SEL --> OUT["Designed molecules"]
```

The accessible chemical space explodes combinatorially with building blocks, so
generation must be tightly steered by multi-objective scoring:

```plot
{"title": "Chemical space size vs building blocks", "xLabel": "building blocks used", "yLabel": "log10(reachable molecules)", "xRange": [1, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.2*x", "label": "combinatorial explosion", "color": "#2563eb"}]}
```

**Next:** the generative AI models powering modern de novo design.
""",
        ),
        _t(
            "Generative AI for molecule generation",
            "13 min",
            r"""
# Generative AI for molecule generation

Deep generative models learn the distribution of valid, drug-like molecules and
sample new ones. **Variational autoencoders (VAEs)** encode molecules (as SMILES
or graphs) into a continuous **latent space** where optimisation and
interpolation become tractable. **Recurrent / transformer** language models
generate SMILES token-by-token. **Generative adversarial networks (GANs)** and,
increasingly, **diffusion models** (e.g. for 3D structures) produce novel
scaffolds.

To bias generation toward goals, **reinforcement learning** (REINVENT) rewards
molecules scoring well on predicted affinity, QED drug-likeness and synthetic
accessibility, while a prior keeps outputs realistic. Conditioning on the target
pocket yields **structure-based generative** models (Pocket2Mol, DiffSBDD) that
place atoms directly into the binding site. Validity, novelty, uniqueness and
synthesisability are the standard evaluation metrics.

```mermaid
flowchart LR
  DATA["Molecule dataset"] --> ENC["Encode (SMILES / graph)"]
  ENC --> LAT["Latent space"]
  LAT --> RL["RL / property optimisation"]
  RL --> DEC["Decode to new molecules"]
  DEC --> FILT["Filter: validity, SA, ADMET"]
```

During RL optimisation the average reward (e.g. predicted potency + drug-
likeness) climbs over training steps toward a plateau:

```plot
{"title": "Average reward during RL fine-tuning", "xLabel": "training step (x100)", "yLabel": "mean reward", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "reward improves", "color": "#16a34a"}]}
```

**Next:** predicting the protein structures these models target.
""",
        ),
        _t(
            "AlphaFold and structure prediction",
            "12 min",
            r"""
# AlphaFold and structure prediction

Structure-based design needs a 3D target, but many proteins lack experimental
structures. **AlphaFold2** (DeepMind, 2021) transformed the field by predicting
protein structures from sequence at near-experimental accuracy for many
proteins, using a transformer (**Evoformer**) over multiple-sequence alignments
and a structure module that outputs 3D coordinates. Its per-residue confidence
**pLDDT** and inter-domain **PAE** scores tell users where to trust the model.

For CADD this unlocks targets without crystal structures, but caveats matter:
AlphaFold predicts a single (often apo) conformation, models side chains and
binding-site flexibility imperfectly, and is **not** trained to place ligands —
so docking into predicted structures can disappoint. AlphaFold3 and successors
extend to complexes with ligands and nucleic acids, narrowing this gap.

```mermaid
flowchart LR
  SEQ["Protein sequence"] --> MSA["Build MSA + templates"]
  MSA --> EVO["Evoformer attention"]
  EVO --> STR["Structure module -> 3D coords"]
  STR --> CONF["Confidence: pLDDT / PAE"]
  CONF --> SBDD["Use in structure-based design"]
```

Docking and design reliability tracks model confidence — high-pLDDT pockets give
usable structures, low-confidence regions do not:

```plot
{"title": "Docking reliability vs model confidence", "xLabel": "binding-site pLDDT", "yLabel": "relative docking reliability", "xRange": [0, 100], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-70)/8))", "label": "usable above ~70 pLDDT", "color": "#2563eb"}]}
```

**Next:** balancing many objectives in lead optimisation.
""",
        ),
        _t(
            "Multi-parameter lead optimisation",
            "12 min",
            r"""
# Multi-parameter lead optimisation

Real drugs must satisfy many objectives at once — potency, selectivity,
solubility, permeability, metabolic stability, low hERG/toxicity — that often
**conflict**. **Multi-parameter optimisation (MPO)** formalises this trade-off.
A desirability function maps each property onto $[0,1]$ and combines them, e.g.
the geometric mean
$$D = \left(\prod_{i=1}^{n} d_i\right)^{1/n},$$
so a single failing property tanks the overall score. The CNS-MPO score is a
well-known example.

In practice, free-energy methods (FEP+) prioritise which analogues to make,
ADMET models filter liabilities, and the **design-make-test-analyse (DMTA)**
cycle iterates. AI is increasingly closing the loop: active-learning models
choose the next batch, and automated synthesis platforms execute it, compressing
cycle time dramatically.

```mermaid
flowchart LR
  D["Design candidates"] --> M["Make (synthesis)"]
  M --> T["Test (assays / ADMET)"]
  T --> A["Analyse + model"]
  A --> D
  A --> MPO["MPO desirability score"]
```

Because objectives are multiplied, the joint desirability falls steeply as the
number of independent must-pass criteria grows — optimisation gets harder fast:

```plot
{"title": "Joint desirability vs number of objectives", "xLabel": "number of objectives", "yLabel": "probability all pass", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.3*x)", "label": "harder with more goals", "color": "#dc2626"}]}
```

**Next:** how these methods played out in real drug-discovery campaigns.
""",
        ),
        _t(
            "Case studies in CADD",
            "12 min",
            r"""
# Case studies in CADD

CADD has shaped landmark medicines. **HIV protease inhibitors** (saquinavir,
indinavir, the later darunavir) were designed against crystal structures of the
viral protease, exploiting its C2-symmetric active site — a textbook
structure-based success. **Captopril**, an ACE inhibitor, grew from rational
design around the enzyme's zinc and a known peptide. **Imatinib** (Gleevec)
emerged from optimising a kinase-targeting series guided by structural insight
into BCR-ABL.

More recently, structure-based and AI methods accelerated the SARS-CoV-2 main
protease inhibitor in **nirmatrelvir** (Paxlovid), and AI-first companies report
candidates such as Exscientia's and Insilico Medicine's clinical molecules
reaching trials in a fraction of typical timelines. The pattern is consistent:
a validated, druggable target with structural data plus rigorous computational
prioritisation shortens the path to a lead.

```mermaid
flowchart TB
  SBDD["Structure-based design"] --> HIV["HIV protease inhibitors"]
  SBDD --> COV["SARS-CoV-2 Mpro (nirmatrelvir)"]
  AI["AI-driven design"] --> EXS["Generative/ML candidates in trials"]
  HIV --> WIN["Faster, more rational discovery"]
  COV --> WIN
  EXS --> WIN
```

A recurring claim is that CADD compresses the early discovery timeline; reported
cycle times shrink markedly as computational prioritisation replaces brute-force
screening:

```plot
{"title": "Discovery time vs computational prioritisation", "xLabel": "computational effort (relative)", "yLabel": "time to lead (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "shorter timelines", "color": "#16a34a"}]}
```

**Next:** test your grasp of state-of-the-art CADD.
""",
        ),
        _quiz(),
    ),
)


COMPUTER_AIDED_DRUG_DESIGN_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["COMPUTER_AIDED_DRUG_DESIGN_COURSES"]
