"""Cell Biology track: Basics -> Intermediate -> Advanced.

A university-level cell biology curriculum from the cell, membranes and
organelles, through the cytoskeleton, membrane transport and signalling, to the
cell cycle, cancer and modern imaging and computational methods. Lessons use
interactive ```plot blocks for quantitative relationships (Michaelis-Menten,
dose-response, binding, growth/decay) and ```mermaid diagrams for pathways,
organelle classifications and experimental pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# -- Cell Biology -- Basics ----------------------------------------------------

_BASICS = SeedCourse(
    slug="cell-biology-basics",
    title="Cell Biology — Basics",
    description=(
        "The cell from the ground up: the cell theory and the prokaryote vs "
        "eukaryote divide, the plasma membrane as a fluid mosaic, the major "
        "organelles and the secretory pathway, the nucleus and the central "
        "dogma, and how energy is harvested in mitochondria and chloroplasts. "
        "Built on real molecular detail with interactive plots and pathway "
        "diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The cell and the cell theory",
            "10 min",
            r"""
# The cell and the cell theory

The **cell** is the smallest unit of life: the simplest thing that can
metabolise, grow, respond and reproduce. The **cell theory**, built by Schleiden,
Schwann and refined by Virchow ("omnis cellula e cellula"), states that all
living things are made of cells, the cell is the basic unit of structure and
function, and every cell arises from a pre-existing cell.

Two great lineages exist. **Prokaryotes** (bacteria, archaea) have no
membrane-bound nucleus; their DNA sits in a nucleoid. **Eukaryotes** (protists,
fungi, plants, animals) compartmentalise functions into membrane-bound
**organelles** — nucleus, mitochondria, ER, Golgi.

```mermaid
flowchart TB
  LIFE["Cellular life"] --> PRO["Prokaryotes: no nucleus, ~1-5 um"]
  LIFE --> EUK["Eukaryotes: organelles, ~10-100 um"]
  PRO --> BACT["Bacteria"]
  PRO --> ARCH["Archaea"]
  EUK --> ANI["Animal / plant / fungi / protists"]
```

Why are cells small? Because metabolism depends on **surface area to volume
ratio**. Volume (demand) grows as $r^3$ while surface (supply) grows as $r^2$,
so $S/V = 3/r$ falls as a cell enlarges — large cells starve for membrane area.

```plot
{"title": "Surface-to-volume ratio of a spherical cell", "xLabel": "radius r (um)", "yLabel": "S/V (1/um)", "xRange": [0.5, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "3/x", "label": "S/V = 3/r", "color": "#2563eb"}]}
```

**Next:** the membrane that defines the cell's boundary.
""",
        ),
        _t(
            "The plasma membrane: the fluid mosaic",
            "11 min",
            r"""
# The plasma membrane: the fluid mosaic

Every cell is wrapped in a **phospholipid bilayer**. Each phospholipid is
**amphipathic**: a hydrophilic phosphate head and two hydrophobic fatty-acid
tails. In water the tails hide inward, heads face out, spontaneously forming a
~5 nm bilayer — the lowest free-energy arrangement.

The **Singer–Nicolson fluid mosaic model** describes this bilayer as a
two-dimensional fluid studded with proteins that drift laterally. Components:

| Component | Role |
|-----------|------|
| Phospholipids | the fluid barrier |
| Cholesterol | buffers fluidity; stiffens at warm, fluidises at cold |
| Integral proteins | transporters, channels, receptors |
| Glycolipids/glycoproteins | the glycocalyx, recognition |

```mermaid
flowchart LR
  HEAD["Hydrophilic heads (outside)"] --> CORE["Hydrophobic tail core"]
  CORE --> HEAD2["Hydrophilic heads (cytosol)"]
  PROT["Integral / peripheral proteins"] --> CORE
```

**Membrane fluidity** depends on temperature and lipid composition. Above the
transition temperature the bilayer is a disordered liquid; below it gels.
Unsaturated tails (with kinks) and cholesterol broaden the transition. A simple
sigmoid captures the fraction of fluid (disordered) lipid versus temperature:

```plot
{"title": "Lipid order-to-fluid transition", "xLabel": "temperature (relative)", "yLabel": "fraction fluid", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fluid fraction", "color": "#dc2626"}]}
```

**Next:** the organelles enclosed by such membranes.
""",
        ),
        _t(
            "Organelles and the endomembrane system",
            "12 min",
            r"""
# Organelles and the endomembrane system

Eukaryotic cells divide labour among **organelles**. The **endomembrane system**
is a connected set of compartments that synthesise, modify and traffic proteins
and lipids.

- **Rough ER**: ribosome-studded; folds and glycosylates secretory and membrane
  proteins entering the lumen.
- **Smooth ER**: lipid synthesis, calcium storage, detoxification.
- **Golgi apparatus**: cis-to-trans processing, sorting and packaging.
- **Lysosomes**: acidic (pH ~4.5) hydrolase-filled recycling centres.
- **Peroxisomes**: oxidative reactions, breakdown of fatty acids.

The **secretory pathway** moves cargo via vesicles:

```mermaid
flowchart LR
  RER["Rough ER (synthesis/folding)"] --> COPII["COPII vesicles"]
  COPII --> GOLGI["Golgi (cis -> trans)"]
  GOLGI --> SEC["Secretory vesicles"]
  SEC --> PM["Plasma membrane / exocytosis"]
  GOLGI --> LYS["Lysosomes"]
```

Vesicle budding is driven by coat proteins (COPII outbound from ER, COPI
retrograde, clathrin at the plasma membrane and Golgi). Each compartment keeps a
distinct chemistry — the lysosome's V-ATPase pumps protons to maintain a steep
gradient. The activity of a typical lysosomal hydrolase is sharply pH-dependent,
peaking near its optimum and falling away on either side; near the acidic side
the activity rises steeply with proton concentration, a saturating response:

```plot
{"title": "Lysosomal hydrolase activity vs proton availability", "xLabel": "relative [H+]", "yLabel": "relative activity", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating activity", "color": "#16a34a"}]}
```

**Next:** the nucleus and how genetic information flows.
""",
        ),
        _t(
            "The nucleus and the central dogma",
            "11 min",
            r"""
# The nucleus and the central dogma

The **nucleus** stores the genome as **chromatin** — DNA wound around histone
octamers into **nucleosomes**, the "beads on a string" that compact further into
chromosomes. It is bounded by a double-membrane **nuclear envelope** perforated
by **nuclear pore complexes** that gate macromolecular traffic, and lined by the
**lamina** (intermediate-filament lamins) that gives mechanical shape.

The **central dogma** is the directional flow of sequence information:

```mermaid
flowchart LR
  DNA["DNA"] -->|transcription| RNA["pre-mRNA -> mRNA"]
  RNA -->|export through NPC| CYTO["cytoplasm"]
  CYTO -->|translation at ribosome| PROT["protein"]
```

**Transcription** by RNA polymerase II copies a gene into pre-mRNA, which is
capped, spliced (introns removed) and polyadenylated, then exported. **Translation**
on ribosomes reads codons via tRNA to build a polypeptide. Reverse transcription
(RNA -> DNA) exists in retroviruses but is the exception.

Gene expression is regulated, so transcript and protein levels rise and relax
over time. After a transcriptional pulse, an unstable mRNA decays with
first-order kinetics, $m(t) = m_0 e^{-k t}$:

```plot
{"title": "First-order mRNA decay after a transcription pulse", "xLabel": "time (relative)", "yLabel": "mRNA level", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "m(t) = m0 e^{-kt}", "color": "#2563eb"}]}
```

**Next:** how cells extract usable energy.
""",
        ),
        _t(
            "Mitochondria, chloroplasts and cellular energy",
            "12 min",
            r"""
# Mitochondria, chloroplasts and cellular energy

Cells run on **ATP**, the universal energy currency. The **mitochondrion**
generates most of it through aerobic respiration; in plants and algae the
**chloroplast** captures light to fix carbon. Both are double-membraned and,
under the **endosymbiotic theory**, descend from engulfed bacteria — they keep
their own circular DNA and 70S-type ribosomes.

```mermaid
flowchart LR
  GLU["Glucose"] -->|glycolysis (cytosol)| PYR["Pyruvate + 2 ATP"]
  PYR -->|matrix| KREBS["Krebs cycle: NADH, FADH2"]
  KREBS --> ETC["Electron transport chain"]
  ETC -->|proton gradient| ATP["ATP synthase -> ~30 ATP"]
```

The engine is **chemiosmosis** (Mitchell's hypothesis): the electron transport
chain pumps protons across the inner membrane, building a **proton-motive force**;
protons flow back through **ATP synthase**, whose rotation phosphorylates ADP.
Folded **cristae** maximise inner-membrane area for this machinery.

Respiration rate saturates with oxygen availability much like an enzyme with its
substrate — fast at first, then plateauing as the chain runs at capacity, a
Michaelis–Menten-shaped curve:

```plot
{"title": "Respiration rate vs oxygen availability", "xLabel": "[O2] (relative)", "yLabel": "O2 consumption rate", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "saturating respiration", "color": "#dc2626"}]}
```

Photosynthesis runs the reverse balance: light reactions in the thylakoid build
ATP and NADPH, the Calvin cycle in the stroma fixes CO2 into sugar.

**Next:** test your understanding of the cell's foundations.
""",
        ),
        _quiz(),
    ),
)


# -- Cell Biology -- Intermediate ---------------------------------------------

_INTERMEDIATE = SeedCourse(
    slug="cell-biology-intermediate",
    title="Cell Biology — Intermediate",
    description=(
        "Quantitative cell biology: enzyme and membrane-transport kinetics, the "
        "cytoskeleton and molecular motors, signal transduction and dose-"
        "response, bioenergetics and the proton-motive force, and protein "
        "trafficking and quality control. Emphasis on the core equations and "
        "methods — Michaelis-Menten, the GHK and Nernst relations, Hill "
        "cooperativity — with interactive plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Enzyme kinetics: Michaelis-Menten",
            "12 min",
            r"""
# Enzyme kinetics: Michaelis-Menten

Enzymes accelerate reactions by lowering the activation barrier. The
**Michaelis–Menten** model assumes a fast-forming enzyme–substrate complex,
$E + S \rightleftharpoons ES \rightarrow E + P$, and the steady-state assumption
($d[ES]/dt \approx 0$) yields the rate law:

$$v = \frac{V_{max}[S]}{K_m + [S]}.$$

Here $V_{max} = k_{cat}[E]_T$ is the saturating velocity and $K_m$ is the
substrate concentration at half-maximal rate. At $[S] \ll K_m$ the rate is
first-order in substrate; at $[S] \gg K_m$ it saturates. The hyperbola:

```plot
{"title": "Michaelis-Menten saturation kinetics", "xLabel": "[S] (relative to Km)", "yLabel": "v (fraction of Vmax)", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

The **specificity constant** $k_{cat}/K_m$ ranks catalytic efficiency and is
bounded by diffusion (~$10^8$–$10^9$ M⁻¹s⁻¹). The **Lineweaver–Burk** double
reciprocal $1/v$ vs $1/[S]$ linearises the data and distinguishes inhibition
types: **competitive** inhibitors raise apparent $K_m$ (same $V_{max}$),
**noncompetitive** lower $V_{max}$ (same $K_m$).

```mermaid
flowchart LR
  E["E + S"] --> ES["ES complex"]
  ES --> P["E + P"]
  INH["competitive inhibitor"] --> E
```

**Next:** moving solutes across the membrane.
""",
        ),
        _t(
            "Membrane transport: diffusion, Nernst and GHK",
            "12 min",
            r"""
# Membrane transport: diffusion, Nernst and GHK

Solutes cross membranes by **passive** routes (down their electrochemical
gradient) or **active** routes (pumping uphill at ATP cost).

```mermaid
flowchart TB
  TRANS["Membrane transport"] --> PASS["Passive (no ATP)"]
  TRANS --> ACT["Active (uses energy)"]
  PASS --> SIMP["Simple diffusion"]
  PASS --> FAC["Facilitated: channels / carriers"]
  ACT --> PRIM["Primary: Na/K-ATPase"]
  ACT --> SEC["Secondary: symport / antiport"]
```

**Carrier-mediated** facilitated diffusion saturates because carriers are
finite, following the same hyperbolic law as enzymes — flux rises then plateaus:

```plot
{"title": "Carrier-mediated transport saturates", "xLabel": "[solute] (relative)", "yLabel": "flux", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "Jmax[S]/(Kt+[S])", "color": "#16a34a"}]}
```

For an ion, the **equilibrium potential** at which the electrical force balances
the concentration gradient is the **Nernst equation**:

$$E_{ion} = \frac{RT}{zF}\ln\frac{[\text{ion}]_{out}}{[\text{ion}]_{in}}.$$

The resting membrane potential, set by several permeant ions at once, follows
the **Goldman–Hodgkin–Katz** equation weighting each ion by its permeability.
The **Na⁺/K⁺-ATPase** maintains the gradients, exporting 3 Na⁺ for every 2 K⁺
per ATP, and powers **secondary active transport** (e.g. the SGLT1 glucose
symporter riding the Na⁺ gradient).

**Next:** the cytoskeleton and the motors that walk on it.
""",
        ),
        _t(
            "The cytoskeleton and molecular motors",
            "12 min",
            r"""
# The cytoskeleton and molecular motors

The **cytoskeleton** is a dynamic polymer scaffold giving cells shape, mechanics
and the rails for transport. Three filament systems:

| Filament | Subunit | Diameter | Roles |
|----------|---------|----------|-------|
| Microfilaments | actin (G-actin) | ~7 nm | shape, migration, cytokinesis |
| Intermediate filaments | keratin, lamin, vimentin | ~10 nm | tensile strength |
| Microtubules | alpha/beta tubulin | ~25 nm | tracks, spindle, cilia |

Microtubules are **polar** (plus/minus ends) and exhibit **dynamic
instability**: stochastic switching between growth and catastrophic shrinkage,
governed by GTP hydrolysis on beta-tubulin.

```mermaid
flowchart LR
  MINUS["Minus end (centrosome)"] --- MT["Microtubule"] --- PLUS["Plus end"]
  KIN["Kinesin -> plus end"] --> PLUS
  DYN["Dynein -> minus end"] --> MINUS
```

**Motor proteins** convert ATP hydrolysis into directed steps: **kinesin** and
**dynein** walk microtubules (anterograde and retrograde), **myosin** walks
actin. Motor velocity rises with ATP concentration and saturates as the
ATPase cycle becomes rate-limiting — again hyperbolic:

```plot
{"title": "Motor stepping velocity vs ATP", "xLabel": "[ATP] (relative)", "yLabel": "velocity", "xRange": [0, 10], "yRange": [0, 9], "grid": true, "functions": [{"expr": "8*x/(1+x)", "label": "v = Vmax[ATP]/(Km+[ATP])", "color": "#dc2626"}]}
```

**Next:** how cells receive and amplify signals.
""",
        ),
        _t(
            "Signal transduction and dose-response",
            "12 min",
            r"""
# Signal transduction and dose-response

Cells sense their environment through **receptors** that convert an extracellular
ligand into an intracellular response. Two dominant classes:

- **G-protein-coupled receptors (GPCRs)**: ligand binding activates a
  heterotrimeric G protein, which modulates effectors (adenylyl cyclase ->
  cAMP -> PKA) — a fast, amplifying cascade.
- **Receptor tyrosine kinases (RTKs)**: ligand-induced dimerisation triggers
  autophosphorylation and the Ras–MAPK and PI3K–Akt pathways controlling growth.

```mermaid
flowchart LR
  LIG["Ligand"] --> REC["Receptor (GPCR / RTK)"]
  REC --> XDUCE["Transducer (G protein / kinase)"]
  XDUCE --> SEC["Second messenger (cAMP, Ca2+, IP3)"]
  SEC --> RESP["Cellular response"]
```

The **dose-response** of a receptor is sigmoidal on a log-dose axis. Fractional
occupancy follows the Hill equation; the **EC50** is the dose giving half-maximal
response and the **Hill coefficient** $n$ measures cooperativity:

```plot
{"title": "Sigmoidal dose-response (log dose)", "xLabel": "log dose", "yLabel": "fractional response", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "response", "color": "#2563eb"}]}
```

**Amplification** is key: one active receptor activates many G proteins, each
making many cAMP molecules — a single hormone yields a large intracellular
signal. Termination (GTP hydrolysis, phosphodiesterases, phosphatases) resets
the system.

**Next:** the bioenergetics that powers all of this.
""",
        ),
        _t(
            "Bioenergetics and the proton-motive force",
            "12 min",
            r"""
# Bioenergetics and the proton-motive force

Reactions proceed when the **Gibbs free-energy change** is negative:
$\Delta G = \Delta G^{\circ\prime} + RT\ln Q$, where $Q$ is the
mass-action ratio. ATP hydrolysis ($\Delta G^{\circ\prime} \approx -30.5$ kJ/mol)
is exergonic and is **coupled** to drive unfavourable reactions.

Oxidative phosphorylation stores energy in an electrochemical proton gradient,
the **proton-motive force**:

$$\Delta p = \Delta\psi - \frac{2.3RT}{F}\,\Delta\text{pH},$$

combining the membrane potential $\Delta\psi$ and the pH difference. ATP synthase
uses $\Delta p$ to phosphorylate ADP; roughly 4 H⁺ pass per ATP.

```mermaid
flowchart LR
  NADH["NADH/FADH2"] --> ETC["Complexes I-IV pump H+"]
  ETC --> PMF["Proton-motive force (delta-p)"]
  PMF --> SYN["ATP synthase (Complex V)"]
  SYN --> ATP["ATP"]
```

The **redox potential** of carriers sets the energy released as electrons fall
from NADH ($E^{\circ\prime} \approx -0.32$ V) to O2 (+0.82 V). The accumulated
free energy as electrons traverse the chain grows steeply then levels —
think of cumulative energy released along the electron path:

```plot
{"title": "Cumulative free energy along the electron transport chain", "xLabel": "electron progress through complexes", "yLabel": "cumulative -deltaG (relative)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "cumulative energy", "color": "#16a34a"}]}
```

**Next:** how proteins reach the right compartment.
""",
        ),
        _t(
            "Protein trafficking and quality control",
            "11 min",
            r"""
# Protein trafficking and quality control

A protein's **address** is encoded in its sequence. **Signal sequences** and
**signal patches** route nascent and folded proteins to the right destination.
Secretory and membrane proteins are recognised co-translationally by the
**signal recognition particle (SRP)**, which docks the ribosome on the ER
translocon (Sec61) so the chain threads into the ER lumen.

```mermaid
flowchart LR
  RIB["Ribosome + signal peptide"] --> SRP["SRP binds, pauses"]
  SRP --> TRANS["Sec61 translocon (ER)"]
  TRANS --> FOLD["Folding + N-glycosylation"]
  FOLD --> GOLGI["Golgi sorting"]
  GOLGI --> DEST["PM / secretion / lysosome"]
```

In the ER, **chaperones** (BiP, calnexin/calreticulin) assist folding and
**glycosylation** tags proteins; lysosomal enzymes get a mannose-6-phosphate
tag. Misfolded proteins trigger the **unfolded protein response (UPR)** and, if
unresolved, **ER-associated degradation (ERAD)** retro-translocates them for
ubiquitin–proteasome destruction.

The fraction of correctly folded protein rises with available chaperone
capacity and saturates as folding intermediates are captured — a binding-like
curve:

```plot
{"title": "Folding yield vs chaperone capacity", "xLabel": "chaperone availability (relative)", "yLabel": "fraction correctly folded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "folding yield", "color": "#2563eb"}]}
```

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# -- Cell Biology -- Advanced -------------------------------------------------

_ADVANCED = SeedCourse(
    slug="cell-biology-advanced",
    title="Cell Biology — Advanced",
    description=(
        "State-of-the-art and applied cell biology: cell-cycle control and its "
        "checkpoints, apoptosis and programmed death, the hallmarks of cancer "
        "and its kinetics, super-resolution and live imaging, single-cell omics "
        "and CRISPR, and deep-learning image analysis. Connects mechanism to "
        "modern computational and imaging methods with interactive plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Cell-cycle control and checkpoints",
            "13 min",
            r"""
# Cell-cycle control and checkpoints

The **cell cycle** (G1 -> S -> G2 -> M) is driven by oscillating
**cyclin–CDK** complexes. Cyclin levels rise and fall while CDK is constitutive;
their product times each transition. Activity is sharpened by phosphorylation
(Wee1 inhibits, Cdc25 activates) and by CDK inhibitors (p21, p27).

```mermaid
flowchart LR
  G1["G1"] -->|G1/S CDK| S["S (DNA replication)"]
  S --> G2["G2"]
  G2 -->|M-CDK| M["M (mitosis)"]
  M --> G1
  RP["Restriction point (Rb/E2F)"] --> S
```

**Checkpoints** halt progression until conditions are met: the **G1/S
restriction point** (growth signals, Rb–E2F), the **G2/M DNA-damage** checkpoint
(ATM/ATR -> Chk -> p53), and the **spindle assembly checkpoint** (kinetochore
attachment, the APC/C inhibited until all chromosomes are bioriented).

Cyclin–CDK activation is **switch-like** (bistable), a steep sigmoid in mitotic
trigger versus cyclin level, giving an all-or-none commitment:

```plot
{"title": "Switch-like M-CDK activation vs cyclin level", "xLabel": "cyclin level (relative)", "yLabel": "active CDK fraction", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^4)", "label": "ultrasensitive switch", "color": "#2563eb"}]}
```

**Next:** how cells decide to die.
""",
        ),
        _t(
            "Apoptosis and programmed cell death",
            "12 min",
            r"""
# Apoptosis and programmed cell death

**Apoptosis** is regulated, non-inflammatory cell death essential for
development and homeostasis. It is executed by **caspases** — cysteine proteases
acting in a cascade of initiators (caspase-8, -9) and executioners (caspase-3,
-7).

```mermaid
flowchart TB
  DEATH["Apoptotic triggers"] --> EXT["Extrinsic: death receptors (Fas/TNF)"]
  DEATH --> INT["Intrinsic: mitochondrial"]
  EXT --> C8["Caspase-8"]
  INT --> CYTC["Bax/Bak -> cytochrome c -> apoptosome -> Caspase-9"]
  C8 --> EXEC["Executioner caspase-3"]
  CYTC --> EXEC
  EXEC --> APOP["DNA fragmentation, blebbing, phagocytosis"]
```

The **intrinsic pathway** is gated at the mitochondrion by the **Bcl-2 family**:
pro-apoptotic Bax/Bak permeabilise the outer membrane (MOMP) releasing
cytochrome c; anti-apoptotic Bcl-2/Bcl-xL restrain them. The balance is a
rheostat — but downstream of MOMP, caspase activation is an irreversible,
self-amplifying switch (the "point of no return"):

```plot
{"title": "Caspase activation after MOMP (cumulative)", "xLabel": "time after MOMP (relative)", "yLabel": "active caspase-3", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-4)))", "label": "irreversible activation", "color": "#dc2626"}]}
```

Distinct from apoptosis are **necroptosis** (RIPK/MLKL, lytic) and **pyroptosis**
(gasdermin pores, inflammatory) — therapeutically relevant in cancer and
infection.

**Next:** what happens when these controls fail.
""",
        ),
        _t(
            "Cancer: hallmarks and growth kinetics",
            "13 min",
            r"""
# Cancer: hallmarks and growth kinetics

Cancer is a disease of **dysregulated cell behaviour** arising from somatic
mutation and selection. Hanahan and Weinberg's **hallmarks** include sustained
proliferative signalling, evading growth suppressors, resisting apoptosis,
enabling replicative immortality, inducing angiogenesis, and activating
invasion/metastasis — plus enabling characteristics like genome instability and
immune evasion.

```mermaid
flowchart LR
  ONC["Oncogene activation (Ras, Myc)"] --> PROL["Excess proliferation"]
  TSG["Tumor-suppressor loss (p53, Rb)"] --> PROL
  PROL --> CLONE["Clonal expansion + selection"]
  CLONE --> INV["Invasion / metastasis"]
```

Tumour growth is **not** purely exponential: nutrient and oxygen limits make it
**Gompertzian** — fast early, decelerating as the tumour enlarges. Compare an
early exponential phase with a saturating realistic curve:

```plot
{"title": "Tumor growth: exponential vs saturating", "xLabel": "time (relative)", "yLabel": "tumor burden (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "early exponential", "color": "#dc2626"}, {"expr": "9*x/(2+x)", "label": "saturating (resource-limited)", "color": "#2563eb"}]}
```

**Driver** mutations confer fitness; **passenger** mutations ride along.
Therapy targets dependencies — kinase inhibitors (imatinib vs BCR-ABL),
synthetic lethality (PARP inhibitors in BRCA-mutant tumours), and immune
checkpoint blockade (anti-PD-1/PD-L1).

**Next:** seeing cells beyond the diffraction limit.
""",
        ),
        _t(
            "Super-resolution and live-cell imaging",
            "12 min",
            r"""
# Super-resolution and live-cell imaging

Conventional light microscopy is capped by **diffraction** at
$d \approx \lambda / (2\,\text{NA}) \approx 200$ nm. **Super-resolution**
techniques break this limit:

| Method | Principle | Resolution |
|--------|-----------|-----------|
| STED | depletes fluorescence at the periphery of the spot | ~30-80 nm |
| PALM/STORM | localises single blinking molecules | ~10-30 nm |
| SIM | structured illumination, frequency mixing | ~100 nm |
| Expansion microscopy | physically swells the sample | effective ~70 nm |

```mermaid
flowchart LR
  SAMP["Fluorescent sample"] --> EXC["Excitation"]
  EXC --> MOD["Spatial/temporal modulation (STED / blinking / SIM)"]
  MOD --> LOC["Localization / reconstruction"]
  LOC --> IMG["Super-resolved image"]
```

In single-molecule localisation, precision improves with the number of detected
**photons** $N$ roughly as $\sigma \approx s/\sqrt{N}$ — more photons, sharper
localisation, with diminishing returns:

```plot
{"title": "Localization precision vs photon count", "xLabel": "photons detected N (relative)", "yLabel": "localization error sigma", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "sigma ~ 1/sqrt(N)", "color": "#2563eb"}]}
```

**Live-cell** imaging adds dynamics: genetically encoded reporters (GFP fusions,
GCaMP for Ca²⁺, FRET biosensors), light-sheet microscopy for low-phototoxicity
volumetric movies, and FRAP/photoactivation to measure mobility.

**Next:** reading single cells at genomic scale.
""",
        ),
        _t(
            "Single-cell omics and CRISPR",
            "13 min",
            r"""
# Single-cell omics and CRISPR

**Single-cell RNA sequencing (scRNA-seq)** measures the transcriptome of
thousands of individual cells, revealing heterogeneity hidden in bulk averages.
Cells are isolated (droplet microfluidics, e.g. 10x Genomics), barcoded,
reverse-transcribed with **UMIs** (to count molecules, not reads), and
sequenced.

```mermaid
flowchart LR
  CELLS["Dissociated cells"] --> DROP["Droplet barcoding + UMI"]
  DROP --> LIB["cDNA library"]
  LIB --> SEQ["Sequencing"]
  SEQ --> MAT["Cell x gene matrix"]
  MAT --> EMB["QC -> normalize -> PCA -> UMAP -> cluster"]
  EMB --> CELLTYPE["Cell-type / state annotation"]
```

Downstream, dimensionality reduction (**PCA**, then **UMAP/t-SNE**) and
clustering (Leiden) define cell types; **pseudotime** orders cells along
differentiation trajectories. The number of distinct cell states resolved rises
with sequencing depth but saturates — capturing the rare populations last:

```plot
{"title": "Detected cell states vs sequencing depth", "xLabel": "reads per cell (relative)", "yLabel": "fraction of states detected", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1.5)", "label": "saturating detection", "color": "#16a34a"}]}
```

**CRISPR–Cas9** enables precise genome editing: a guide RNA targets Cas9 to a
genomic locus where it cuts; repair by NHEJ (knockouts) or HDR (knock-ins)
rewrites the sequence. **CRISPRi/a** (dCas9 fused to repressors/activators) tunes
expression without cutting, and pooled **CRISPR screens** map gene function
genome-wide — increasingly read out by single-cell sequencing (Perturb-seq).

**Next:** letting machines analyse the images.
""",
        ),
        _t(
            "Deep learning for cellular image analysis",
            "12 min",
            r"""
# Deep learning for cellular image analysis

Modern microscopy produces terabytes of images; **deep learning** automates
their analysis. The core task of **segmentation** — drawing the boundary of each
cell or nucleus — is solved by convolutional neural networks. **U-Net** (an
encoder–decoder with skip connections) and generalist tools like **Cellpose**
and **StarDist** segment cells robustly across modalities.

```mermaid
flowchart LR
  IMG["Microscopy image"] --> PRE["Normalize / tile"]
  PRE --> CNN["U-Net / Cellpose encoder-decoder"]
  CNN --> MASK["Instance masks"]
  MASK --> FEAT["Per-cell features (size, intensity, shape)"]
  FEAT --> CLASS["Phenotype classification / profiling"]
```

Other applications: **denoising and restoration** (Noise2Noise, CARE),
**super-resolution** reconstruction from low-res inputs, **virtual staining**
(predicting fluorescence from brightfield), and **morphological profiling**
(Cell Painting -> embeddings for drug discovery). Foundation models pretrained on
large image corpora now transfer to new assays with little labelling.

Model accuracy improves with the amount of **labelled training data** but with
diminishing returns — a saturating learning curve that motivates self-supervised
pretraining:

```plot
{"title": "Segmentation accuracy vs labeled training data", "xLabel": "labeled images (relative)", "yLabel": "validation accuracy", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "learning curve", "color": "#2563eb"}]}
```

Care is needed: **batch effects**, domain shift across microscopes, and the need
for proper validation (held-out plates, not just held-out cells) to avoid
overstated performance.

**Next:** the capstone quiz.
""",
        ),
        _quiz(),
    ),
)


CELL_BIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["CELL_BIOLOGY_COURSES"]
