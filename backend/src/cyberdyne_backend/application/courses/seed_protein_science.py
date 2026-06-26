"""Protein Science & Enzymology track: Basics -> Intermediate -> Advanced.

A three-level track on proteins as molecular machines. It begins with amino
acids, the peptide bond and the four levels of structure; advances through
folding thermodynamics, dynamics and quantitative enzyme kinetics; and ends with
catalytic mechanism, protein engineering, inhibitor design and the
computational/AI methods (AlphaFold2, RFdiffusion, free-energy perturbation,
molecular dynamics) used in modern research. Lessons are `text` with LaTeX,
interactive ```plot blocks (kinetics, stability, dose-response) and ```mermaid
diagrams of pathways and pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Protein Science & Enzymology — Basics ────────────────────────────────────

_BASICS = SeedCourse(
    slug="protein-science-basics",
    title="Protein Science & Enzymology — Basics",
    description=(
        "The molecular vocabulary of proteins: the twenty amino acids and their "
        "side-chain chemistry, the rigid peptide bond, and the four levels of "
        "structure from sequence to quaternary assembly. We meet the forces "
        "that hold folds together and the idea that a protein's three-"
        "dimensional shape is what does the work. Interactive structure and "
        "energy plots and pathway diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Amino acids: the building blocks",
            "11 min",
            r"""
# Amino acids: the building blocks

Proteins are linear polymers of **amino acids**. Each of the twenty standard
amino acids shares the same backbone — a central $\alpha$-carbon bonded to an
amino group ($-\mathrm{NH_3^+}$), a carboxyl group ($-\mathrm{COO^-}$), a
hydrogen, and a variable **side chain** (R group) — and differs only in that R
group. The side chain decides everything: charge, polarity, size and chemistry.

We classify side chains as **nonpolar/hydrophobic** (Ala, Val, Leu, Ile, Phe),
**polar uncharged** (Ser, Thr, Asn, Gln), **acidic** (Asp, Glu) and **basic**
(Lys, Arg, His). Special cases matter: glycine (R = H) is tiny and flexible,
proline kinks the backbone, and cysteine can form **disulfide bonds**.

```mermaid
flowchart LR
  AA["Amino acid: NH3+ - CHR - COO-"] --> NP["Nonpolar: Ala Val Leu"]
  AA --> PU["Polar uncharged: Ser Asn"]
  AA --> AC["Acidic: Asp Glu"]
  AA --> BA["Basic: Lys Arg His"]
```

Because amino acids carry both acidic and basic groups, their net charge depends
on pH. The fraction of a group in its deprotonated form follows a sigmoid set by
its $\mathrm{p}K_a$ (here the carboxyl, pKa about 2):

```plot
{"title": "Carboxyl deprotonation vs pH", "xLabel": "pH", "yLabel": "fraction as COO-", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-2)))", "label": "COO- fraction (pKa 2)", "color": "#dc2626"}]}
```

**Next:** how amino acids link into chains through the peptide bond.
""",
        ),
        _t(
            "The peptide bond and primary structure",
            "10 min",
            r"""
# The peptide bond and primary structure

A **peptide bond** forms by condensation: the carboxyl of one amino acid reacts
with the amino group of the next, releasing water and creating an amide
($-\mathrm{C(=O)-NH-}$) linkage. A chain of these is a **polypeptide**, and its
ordered sequence of residues — read N-terminus to C-terminus — is the
**primary structure**.

The peptide bond has partial double-bond character from resonance, so the six
atoms of the amide unit are **planar** and rotation about the C–N bond is
restricted. Conformational freedom is confined to the two backbone dihedral
angles, **phi** ($\phi$, around N–C$\alpha$) and **psi** ($\psi$, around
C$\alpha$–C). Steric clashes forbid most ($\phi$, $\psi$) combinations; the
allowed regions are mapped by the **Ramachandran plot**.

```mermaid
flowchart LR
  N["N-terminus"] --> R1["Res 1"] --> PB["peptide bond (planar amide)"]
  PB --> R2["Res 2"] --> RN["..."] --> C["C-terminus"]
```

Most peptide bonds adopt the *trans* configuration; *cis* is rare except before
proline. The proportion of *cis* X-Pro bonds rises modestly with chain context,
but *trans* dominates overwhelmingly:

```plot
{"title": "Backbone bond population (illustrative)", "xLabel": "relative steric strain", "yLabel": "fraction trans", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(5-x)))", "label": "fraction trans", "color": "#2563eb"}]}
```

**Next:** the regular folding patterns of secondary structure.
""",
        ),
        _t(
            "Secondary structure: helices and sheets",
            "11 min",
            r"""
# Secondary structure: helices and sheets

Local, repetitive backbone folding stabilised by hydrogen bonds is
**secondary structure**. The two dominant motifs are the **alpha-helix** and the
**beta-sheet**, both predicted by Pauling and Corey from the geometry of the
planar peptide unit.

In the **alpha-helix** the backbone coils so that each carbonyl oxygen
hydrogen-bonds to the amide N–H four residues ahead ($i \to i+4$). It rises
about 1.5 Å per residue with 3.6 residues per turn, and side chains point
outward. In a **beta-sheet**, extended strands lie side by side, hydrogen-bonded
across strands; arrangements can be **parallel** or **antiparallel**, the latter
forming more linear, stronger hydrogen bonds.

```mermaid
flowchart LR
  BB["Backbone H-bonding"] --> H["Alpha-helix: i to i+4 H-bonds"]
  BB --> S["Beta-sheet: inter-strand H-bonds"]
  S --> AP["Antiparallel"]
  S --> PA["Parallel"]
  BB --> T["Turns and loops connect elements"]
```

Different residues have different helix propensities. Alanine and leucine favour
helices; glycine and proline disrupt them. The cumulative stabilisation of a
helix grows then saturates with length as end effects become negligible:

```plot
{"title": "Helix stabilisation vs length", "xLabel": "helix length (residues)", "yLabel": "relative stability", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+4)", "label": "stability", "color": "#16a34a"}]}
```

**Next:** how secondary elements pack into a tertiary fold.
""",
        ),
        _t(
            "Tertiary and quaternary structure",
            "11 min",
            r"""
# Tertiary and quaternary structure

**Tertiary structure** is the full three-dimensional fold of a single
polypeptide — how its helices, sheets and loops pack together. The dominant
driving force is the **hydrophobic effect**: nonpolar side chains bury into a
water-excluded **core**, while polar and charged residues face the solvent.
Additional stabilisers include hydrogen bonds, salt bridges, van der Waals
contacts and covalent **disulfide bonds** between cysteines.

Recurring tertiary arrangements are **domains** and **folds** (e.g. the
Rossmann fold, the TIM barrel, immunoglobulin folds). **Quaternary structure**
arises when multiple polypeptide chains (**subunits**) assemble — haemoglobin is
an $\alpha_2\beta_2$ tetramer, for instance.

```mermaid
flowchart TB
  PRI["Primary: sequence"] --> SEC["Secondary: helices/sheets"]
  SEC --> TER["Tertiary: 3D fold, buried core"]
  TER --> QUAT["Quaternary: subunit assembly"]
```

Burying nonpolar surface area releases ordered water and stabilises the fold;
the free-energy gain grows roughly with buried area before other effects level
it off:

```plot
{"title": "Folding stabilisation vs buried core area", "xLabel": "buried nonpolar area (nm^2)", "yLabel": "stabilisation |dG| (kJ/mol)", "xRange": [0, 8], "yRange": [0, 35], "grid": true, "functions": [{"expr": "30*x/(x+2)", "label": "stabilisation", "color": "#2563eb"}]}
```

**Next:** how three-dimensional shape creates biological function.
""",
        ),
        _t(
            "From structure to function",
            "10 min",
            r"""
# From structure to function

A protein's job is dictated by its shape. A precisely arranged surface pocket —
the **binding site** or **active site** — recognises a partner molecule (the
**ligand** or **substrate**) through complementary shape and chemistry. This is
the **structure-function** principle: enzymes catalyse, antibodies recognise,
motors move and channels gate because their folds position the right atoms in the
right places.

Binding is described by an equilibrium. For $\mathrm{E} + \mathrm{L}
\rightleftharpoons \mathrm{EL}$, the **dissociation constant** is $K_d =
[\mathrm{E}][\mathrm{L}]/[\mathrm{EL}]$; a smaller $K_d$ means tighter binding.
The fraction of protein bound rises hyperbolically with free ligand and equals
0.5 when $[\mathrm{L}] = K_d$.

```mermaid
flowchart LR
  SEQ["Sequence"] --> FOLD["Fold"] --> SITE["Active/binding site"]
  SITE --> BIND["Specific ligand binding"]
  BIND --> FUNC["Catalysis / recognition / transport"]
```

The hyperbolic saturation of binding sites is the foundation for both enzyme
kinetics and pharmacology:

```plot
{"title": "Fractional saturation vs free ligand", "xLabel": "[L] / Kd", "yLabel": "fraction bound", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "theta = [L]/([L]+Kd)", "color": "#16a34a"}]}
```

**Next:** check your understanding of protein fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Protein Science & Enzymology — Intermediate ──────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="protein-science-intermediate",
    title="Protein Science & Enzymology — Intermediate",
    description=(
        "The quantitative core of protein science: folding thermodynamics and "
        "kinetics, conformational dynamics, and the steady-state enzyme "
        "kinetics that underlie Michaelis-Menten behaviour, catalytic "
        "efficiency, inhibition and cooperativity. We pair each idea with the "
        "equations and experiments used to measure it. Interactive kinetics, "
        "stability and Eadie-Hofstee plots throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Folding thermodynamics and stability",
            "12 min",
            r"""
# Folding thermodynamics and stability

Folding is an equilibrium between **unfolded** (U) and **native** (N) states.
Its stability is the free-energy difference $\Delta G_{fold} = G_N - G_U$, and
for typical small proteins the native state is favoured by only
20-60 kJ/mol — a small margin from the difference of large opposing terms. The
hydrophobic effect and hydrogen bonding favour folding (enthalpy and solvent
entropy), while the loss of chain **conformational entropy** opposes it.

Stability is measured by **denaturation**: adding urea or guanidinium chloride,
or raising temperature, shifts the equilibrium toward U. From the fraction
unfolded $f_U$ we get $K = f_U/(1 - f_U)$ and $\Delta G = -RT \ln K$. Many small
proteins unfold in an apparently **two-state**, cooperative transition with no
populated intermediates.

```mermaid
flowchart LR
  N["Native"] -->|"denaturant / heat"| U["Unfolded"]
  U -->|"refold"| N
  N --> STAB["dG_fold sets stability margin"]
```

The thermal melting curve is sigmoidal; its midpoint is the **melting
temperature** $T_m$, where half the molecules are unfolded:

```plot
{"title": "Thermal unfolding curve", "xLabel": "temperature (relative)", "yLabel": "fraction unfolded", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "fraction unfolded (Tm at 5)", "color": "#dc2626"}]}
```

**Next:** how chains find the native state — the folding problem.
""",
        ),
        _t(
            "Folding kinetics and the energy landscape",
            "11 min",
            r"""
# Folding kinetics and the energy landscape

**Levinthal's paradox** notes that a chain cannot find its native state by
random search — the conformational space is astronomically large, yet folding
takes microseconds to seconds. The resolution is the **folding funnel**: the
energy landscape is biased toward the native state, so many downhill routes
converge. Folding is guided, not blind.

Kinetically, small proteins often fold in a single exponential phase through a
rate-limiting **transition state**. **Phi-value analysis** probes which contacts
are formed at that transition state by measuring how point mutations change both
stability and folding rate. In cells, **molecular chaperones** (Hsp70,
GroEL/GroES) prevent misfolding and aggregation.

```mermaid
flowchart TB
  U["Unfolded ensemble"] --> TS["Transition state"]
  TS --> N["Native"]
  U -.->|"chaperones prevent"| AGG["Misfolded / aggregated"]
```

A two-state folding reaction relaxes to equilibrium exponentially with an
observed rate $k_{obs} = k_f + k_u$; the approach to the folded population looks
like a first-order rise:

```plot
{"title": "Approach to folded population", "xLabel": "time (relative)", "yLabel": "fraction native", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "1 - exp(-k t)", "color": "#2563eb"}]}
```

**Next:** proteins are not static — conformational dynamics.
""",
        ),
        _t(
            "Protein dynamics and allostery",
            "11 min",
            r"""
# Protein dynamics and allostery

A folded protein is not a frozen statue but a fluctuating ensemble exploring
**conformational substates** across timescales from picosecond bond vibrations to
millisecond domain motions. These dynamics enable function: induced fit in
binding, gating in channels, and catalytic cycles in enzymes.

**Allostery** is regulation at a distance: a ligand binding one site changes
activity at another, distinct site. The classic models are **MWC**
(concerted: the whole oligomer flips between tense T and relaxed R states) and
**KNF** (sequential: subunits change one at a time). Allostery underlies
oxygen transport by haemoglobin and feedback inhibition of metabolic enzymes.
Techniques such as NMR relaxation dispersion, HDX-MS and single-molecule FRET
report these motions.

```mermaid
flowchart LR
  E["Effector binds allosteric site"] --> CONF["Conformational shift"]
  CONF --> ACT["Activity at active site changes"]
  CONF --> MWC["MWC: concerted T <-> R"]
  CONF --> KNF["KNF: sequential"]
```

Cooperative (allosteric) ligand binding gives a **sigmoidal** saturation curve,
sharper than hyperbolic binding — here a Hill curve with coefficient 2:

```plot
{"title": "Cooperative binding (Hill, n=2)", "xLabel": "[ligand] (relative)", "yLabel": "fractional saturation", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill n=2", "color": "#16a34a"}]}
```

**Next:** the steady-state kinetics of enzymes.
""",
        ),
        _t(
            "Enzyme kinetics: Michaelis-Menten",
            "12 min",
            r"""
# Enzyme kinetics: Michaelis-Menten

Enzymes accelerate reactions by lowering the activation barrier without being
consumed. The **Michaelis-Menten** model treats catalysis as $\mathrm{E} +
\mathrm{S} \rightleftharpoons \mathrm{ES} \to \mathrm{E} + \mathrm{P}$. Under the
**steady-state assumption** ($d[\mathrm{ES}]/dt \approx 0$) the initial velocity
is

$$v = \frac{V_{max}[\mathrm{S}]}{K_m + [\mathrm{S}]},$$

where $V_{max} = k_{cat}[\mathrm{E}]_T$ is the maximum rate and $K_m$ is the
substrate concentration giving half-maximal velocity. At low $[\mathrm{S}]$ the
rate is first-order in substrate; at high $[\mathrm{S}]$ it saturates at
$V_{max}$.

The **turnover number** $k_{cat}$ is reactions per active site per second, and
the **specificity constant** $k_{cat}/K_m$ measures catalytic efficiency,
bounded by the diffusion limit (~$10^8$-$10^9\,\mathrm{M^{-1}s^{-1}}$).

```mermaid
flowchart LR
  ES1["E + S"] --> ESc["ES complex"]
  ESc --> EP["E + P"]
  ESc -.->|"k_-1"| ES1
```

The hyperbolic dependence of rate on substrate is the signature of saturable,
single-site catalysis:

```plot
{"title": "Michaelis-Menten rate vs substrate", "xLabel": "[S] (relative to Km)", "yLabel": "v (relative to Vmax)", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "8*x/(2+x)/8", "label": "v = Vmax[S]/(Km+[S])", "color": "#2563eb"}]}
```

**Next:** linearising kinetics and analysing inhibition.
""",
        ),
        _t(
            "Linearisations and enzyme inhibition",
            "11 min",
            r"""
# Linearisations and enzyme inhibition

Before nonlinear fitting was routine, kineticists linearised the
Michaelis-Menten equation. The **Lineweaver-Burk** (double-reciprocal) plot
graphs $1/v$ against $1/[\mathrm{S}]$ as a line with slope $K_m/V_{max}$ and
intercept $1/V_{max}$; it is intuitive but weights low-substrate points heavily.
The **Eadie-Hofstee** ($v$ vs $v/[\mathrm{S}]$) and **Hanes-Woolf**
($[\mathrm{S}]/v$ vs $[\mathrm{S}]$) plots distribute error better. Today we fit
the hyperbola directly by nonlinear regression.

**Inhibitors** alter kinetics diagnostically. A **competitive** inhibitor binds
the active site and raises apparent $K_m$ while leaving $V_{max}$ unchanged. A
**noncompetitive** inhibitor binds elsewhere and lowers $V_{max}$ without
changing $K_m$. **Uncompetitive** inhibitors bind only ES, lowering both.

```mermaid
flowchart LR
  I["Inhibitor"] --> C["Competitive: Km up, Vmax same"]
  I --> NC["Noncompetitive: Vmax down, Km same"]
  I --> UC["Uncompetitive: Km and Vmax down"]
```

In a Lineweaver-Burk plot, competitive inhibition pivots the line about the
shared $1/V_{max}$ intercept while increasing the slope:

```plot
{"title": "Lineweaver-Burk: control vs competitive inhibitor", "xLabel": "1/[S]", "yLabel": "1/v", "xRange": [0, 5], "yRange": [0, 6], "grid": true, "functions": [{"expr": "0.5*x+1", "label": "control", "color": "#2563eb"}, {"expr": "1.2*x+1", "label": "+ competitive inhibitor", "color": "#dc2626"}]}
```

**Next:** check your understanding of folding and kinetics.
""",
        ),
        _quiz(),
    ),
)


# ── Protein Science & Enzymology — Advanced ──────────────────────────────────

_ADVANCED = SeedCourse(
    slug="protein-science-advanced",
    title="Protein Science & Enzymology — Advanced",
    description=(
        "State-of-the-art protein science and engineering: catalytic mechanism "
        "and transition-state theory, structure determination, deep-learning "
        "structure prediction (AlphaFold2) and generative design "
        "(RFdiffusion, ProteinMPMN), directed evolution, and computational "
        "inhibitor design with free-energy methods. Interactive energy-profile, "
        "kinetics and binding plots throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Catalytic mechanism and transition-state theory",
            "12 min",
            r"""
# Catalytic mechanism and transition-state theory

Enzymes achieve rate enhancements of $10^{6}$ to $10^{17}$ by stabilising the
reaction's **transition state** more than the ground state. By **transition-state
theory**, the rate depends exponentially on the activation free energy:
$k \propto \exp(-\Delta G^{\ddagger}/RT)$, so lowering $\Delta G^{\ddagger}$ by a
few tens of kJ/mol buys enormous speed-up. Linus Pauling framed catalysis as
**preferential binding of the transition state**.

Catalytic strategies include **general acid-base catalysis** (e.g. His shuttling
protons), **covalent catalysis** (a transient enzyme-substrate covalent
intermediate, as in serine proteases via the Ser-His-Asp **catalytic triad**),
**metal-ion catalysis**, and **proximity and orientation** effects that pay the
entropic cost of aligning reactants.

```mermaid
flowchart LR
  GS["Ground state E+S"] --> TS["Transition state (stabilised)"]
  TS --> PR["Products E+P"]
  TS --> STRAT["Acid-base / covalent / metal / proximity"]
```

Catalysis is best seen as lowering the barrier on a free-energy reaction
coordinate; the catalysed path peaks lower than the uncatalysed one:

```plot
{"title": "Reaction free-energy profile", "xLabel": "reaction coordinate", "yLabel": "free energy", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*exp(-(x-5)^2)", "label": "uncatalysed", "color": "#dc2626"}, {"expr": "4*exp(-(x-5)^2)", "label": "enzyme-catalysed", "color": "#16a34a"}]}
```

**Next:** how we determine and predict protein structures.
""",
        ),
        _t(
            "Structure determination and AlphaFold",
            "12 min",
            r"""
# Structure determination and AlphaFold

For decades, atomic structures came from **X-ray crystallography** (most PDB
entries), **NMR spectroscopy** (smaller proteins in solution, with dynamics),
and increasingly **cryo-electron microscopy** (large complexes, no crystals
needed). Each yields coordinates we evaluate by resolution and validation
metrics.

In 2021 **AlphaFold2** transformed the field, predicting structures from
sequence at near-experimental accuracy. It feeds a **multiple sequence
alignment** (capturing coevolving, contacting residues) through the **Evoformer**
attention network and a geometry-aware **structure module**, scoring confidence
per residue as **pLDDT** and inter-domain confidence as **PAE**. RoseTTAFold and
ESMFold followed; the AlphaFold DB now covers hundreds of millions of proteins.

```mermaid
flowchart LR
  SEQ["Sequence"] --> MSA["MSA + templates"]
  MSA --> EVO["Evoformer (attention)"]
  EVO --> SM["Structure module"]
  SM --> PRED["3D coords + pLDDT/PAE"]
```

Predictions are most reliable in well-folded cores and least reliable in
disordered regions; per-residue confidence (pLDDT) typically falls with local
disorder:

```plot
{"title": "Confidence vs local disorder (illustrative)", "xLabel": "local disorder", "yLabel": "pLDDT", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "95*exp(-0.3*x)", "label": "pLDDT", "color": "#2563eb"}]}
```

**Next:** designing new proteins from scratch.
""",
        ),
        _t(
            "Protein engineering and de novo design",
            "12 min",
            r"""
# Protein engineering and de novo design

We reshape proteins two ways. **Directed evolution** (Frances Arnold, Nobel
2018) mimics natural selection in the lab: diversify a gene by error-prone PCR or
DNA shuffling, screen or select for an improved variant, and iterate. It needs no
mechanistic model — only a good assay — and has produced enzymes for non-natural
chemistry and improved stability.

**Rational and computational design** instead reason from structure. **Rosetta**
optimises sequence on a fixed backbone; deep learning now leads: **ProteinMPNN**
designs sequences for a target backbone, and **RFdiffusion** generates entirely
new backbones by denoising diffusion, enabling **de novo** binders, enzymes and
scaffolds validated experimentally.

```mermaid
flowchart LR
  DE["Directed evolution: mutate -> screen -> select"] --> VAR["Improved variant"]
  CD["Computational: RFdiffusion backbone"] --> MP["ProteinMPNN sequence"]
  MP --> AF["AlphaFold filter"] --> LAB["Express & test"]
```

Each round of directed evolution gives diminishing-returns gains as a property
approaches its functional ceiling — fitness rises and saturates:

```plot
{"title": "Fitness gain across evolution rounds", "xLabel": "round", "yLabel": "relative activity", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "activity", "color": "#16a34a"}]}
```

**Next:** designing inhibitors and drugs against protein targets.
""",
        ),
        _t(
            "Inhibitor design and computational methods",
            "12 min",
            r"""
# Inhibitor design and computational methods

Most drugs are **protein inhibitors**. Tight binding is quantified by $K_i$ or
$K_d$ and, for clinical potency, $\mathrm{IC_{50}}$; binding free energy is
$\Delta G = RT \ln K_d$. Designers grow a hit into a lead by adding interactions
(hydrogen bonds, hydrophobic contacts, shape complementarity) while watching
**ligand efficiency** and drug-likeness.

Computation accelerates this. **Molecular docking** poses candidates in a binding
pocket and scores them; **virtual screening** ranks libraries of millions.
**Molecular dynamics** simulates the flexible complex, and rigorous
**free-energy perturbation (FEP)** predicts relative binding affinities within
~1 kcal/mol for congeneric series. Covalent and **PROTAC** strategies extend the
toolkit beyond classical reversible inhibition.

```mermaid
flowchart LR
  LIB["Compound library"] --> DOCK["Docking / virtual screen"]
  DOCK --> HIT["Hits"] --> MD["MD + FEP affinity"]
  MD --> LEAD["Optimised lead"]
```

Inhibition follows a sigmoidal **dose-response** curve; the inflection point is
the $\mathrm{IC_{50}}$, the concentration giving half-maximal inhibition:

```plot
{"title": "Dose-response inhibition curve", "xLabel": "log[inhibitor] (relative)", "yLabel": "fractional inhibition", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "inhibition (IC50 at 5)", "color": "#dc2626"}]}
```

**Next:** intrinsic disorder, condensates and the frontier.
""",
        ),
        _t(
            "Disorder, condensates and the frontier",
            "11 min",
            r"""
# Disorder, condensates and the frontier

Not every functional protein folds. **Intrinsically disordered proteins** (IDPs)
and regions lack a stable structure yet are central to signalling and regulation,
functioning as flexible ensembles that fold upon binding or stay dynamic. They
defy the classic structure-function paradigm and are enriched in
disease-associated and hub proteins.

Many disordered, low-complexity regions drive **biomolecular condensates** via
**liquid-liquid phase separation (LLPS)** — membraneless organelles such as the
nucleolus and stress granules concentrate molecules through multivalent, weak
interactions. Aberrant transitions of these condensates to solid aggregates are
linked to neurodegeneration (e.g. FUS, TDP-43 in ALS). Modelling disorder and
condensates is a frontier for both physics-based and AI methods.

```mermaid
flowchart LR
  IDP["Disordered / low-complexity regions"] --> MULT["Multivalent weak contacts"]
  MULT --> LLPS["Liquid-liquid phase separation"]
  LLPS --> COND["Condensate (functional)"]
  LLPS -.->|"aging"| AGG["Aggregate (pathological)"]
```

Phase separation is concentration-driven: below a saturation threshold the system
is one phase; above it, droplets form, so condensate fraction rises sharply past
a critical concentration:

```plot
{"title": "Condensate formation vs concentration", "xLabel": "concentration (relative)", "yLabel": "condensed fraction", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-6)))", "label": "condensed fraction", "color": "#2563eb"}]}
```

**Next:** check your mastery of advanced protein science.
""",
        ),
        _quiz(),
    ),
)


PROTEIN_SCIENCE_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PROTEIN_SCIENCE_COURSES"]
