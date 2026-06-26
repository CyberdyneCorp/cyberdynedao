"""Structural Biology track: Basics -> Intermediate -> Advanced.

A three-level track on the three-dimensional architecture of macromolecules. It
starts from amino acids, the peptide bond and the levels of protein and
nucleic-acid structure; advances through folding thermodynamics, X-ray
crystallography and cryo-EM; and ends with structure-function, allostery, and
AI/computational structure-based design (AlphaFold, molecular docking,
molecular dynamics). Lessons are `text` with LaTeX, interactive ```plot blocks
(folding curves, resolution, binding) and ```mermaid pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Structural Biology — Basics ──────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="structural-biology-basics",
    title="Structural Biology — Basics",
    description=(
        "An intuitive introduction to the shapes of life's molecules. We build "
        "from amino acids and the peptide bond to the four levels of protein "
        "structure, the secondary-structure elements captured by the "
        "Ramachandran plot, the double helix of DNA and base pairing, and how "
        "the hydrophobic effect and weak forces hold folded molecules together. "
        "Interactive plots and pathway diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Amino acids and the peptide bond",
            "10 min",
            r"""
# Amino acids and the peptide bond

Proteins are linear polymers of **amino acids**. Each of the 20 standard amino
acids shares a common backbone — a central $\alpha$-carbon bearing an amino
group ($-\mathrm{NH_3^+}$), a carboxyl group ($-\mathrm{COO^-}$) and a hydrogen —
and differs only in its **side chain (R group)**. Side chains range from a single
hydrogen (glycine) to large aromatic rings (tryptophan), and are classified as
nonpolar, polar, acidic or basic. These chemical personalities decide how a
chain will fold.

Amino acids link by a **peptide bond**: the carboxyl of one reacts with the
amino group of the next, releasing water (a condensation reaction). The result
is an amide C–N bond with **partial double-bond character** from resonance,
which makes the six atoms of the peptide unit roughly **planar** and usually
*trans*. Rotation is therefore restricted to the bonds flanking each
$\alpha$-carbon — the $\phi$ (phi) and $\psi$ (psi) torsion angles.

```mermaid
flowchart LR
  AA1["Amino acid 1"] -->|condensation, -H2O| PB["Peptide bond (planar amide)"]
  AA2["Amino acid 2"] --> PB
  PB --> POLY["Polypeptide backbone"]
  POLY --> PHIPSI["Conformation set by phi / psi angles"]
```

By convention the chain has direction, read from the free amino (**N-terminus**)
to the free carboxyl (**C-terminus**). A short curve of side-chain bulk versus
flexibility loss illustrates why small residues like glycine permit more backbone
freedom:

```plot
{"title": "Backbone flexibility vs side-chain size", "xLabel": "side-chain volume (relative)", "yLabel": "allowed conformations (relative)", "xRange": [0, 6], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "fewer conformations as R grows", "color": "#2563eb"}]}
```

**Next:** how the backbone folds into helices and sheets.
""",
        ),
        _t(
            "Secondary structure: helices and sheets",
            "11 min",
            r"""
# Secondary structure: helices and sheets

Local, repeating folds of the backbone — stabilised entirely by **backbone
hydrogen bonds** between the carbonyl oxygen (C=O) and amide hydrogen (N–H) — are
**secondary structure**. The two dominant motifs are the $\alpha$-helix and the
$\beta$-sheet, both proposed by Pauling and Corey in 1951.

In the right-handed **$\alpha$-helix** each C=O hydrogen-bonds to the N–H four
residues ahead ($i \rightarrow i+4$), giving 3.6 residues per turn and a rise of
1.5 Å per residue. Side chains point outward. In a **$\beta$-sheet**, extended
strands lie side by side and hydrogen-bond across the gap; strands can run
**parallel** or **antiparallel** (the latter forms straighter, stronger bonds).
**Turns** and loops connect these elements.

```mermaid
flowchart TB
  BB["Backbone C=O ... H-N hydrogen bonds"] --> H["Alpha-helix: i to i+4, 3.6 res/turn"]
  BB --> S["Beta-sheet: strands H-bond side by side"]
  S --> AP["Antiparallel (stronger)"]
  S --> P["Parallel"]
  H --> SS["Combine into supersecondary motifs"]
  S --> SS
```

Helical content peaks at a characteristic backbone geometry. Plotting a stylised
helix-propensity score against the $\phi$ angle shows a single favoured region
near $-60^\circ$:

```plot
{"title": "Alpha-helix propensity vs phi angle", "xLabel": "phi angle (deg, shifted)", "yLabel": "relative propensity", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-((x-5)^2)/2)", "label": "favoured near phi ~ -60 deg", "color": "#dc2626"}]}
```

**Next:** mapping allowed conformations with the Ramachandran plot.
""",
        ),
        _t(
            "The Ramachandran plot",
            "10 min",
            r"""
# The Ramachandran plot

Because the peptide unit is planar, a residue's local conformation is captured by
just two torsion angles: $\phi$ (rotation about N–C$_\alpha$) and $\psi$
(rotation about C$_\alpha$–C). G. N. Ramachandran asked which combinations are
sterically allowed — i.e., which do not clash atoms — and plotted them on a
$\phi$ vs $\psi$ map now called the **Ramachandran plot**.

Most $(\phi, \psi)$ pairs are forbidden by steric overlap. Allowed regions
cluster in three places: the **$\alpha$-helix** region (around $\phi \approx
-60^\circ, \psi \approx -45^\circ$), the broad **$\beta$-sheet** region (upper
left), and a small **left-handed helix** region populated mainly by glycine,
whose absent side chain frees it to occupy otherwise disallowed space. Proline,
with its ring locking $\phi$, is restricted to a narrow band.

```mermaid
flowchart LR
  PLANAR["Planar peptide unit"] --> PHIPSI["Two free angles: phi, psi"]
  PHIPSI --> RAMA["Ramachandran plot (phi vs psi)"]
  RAMA --> A["Alpha region"]
  RAMA --> B["Beta region"]
  RAMA --> L["Left-handed helix (mostly Gly)"]
```

The plot is a daily quality check: in a good experimental model, >90% of
non-glycine residues fall in the most-favoured regions. A schematic count of
residues at increasing distance from a favoured basin falls off sharply:

```plot
{"title": "Residue density vs distance from favoured basin", "xLabel": "distance in phi/psi space (deg)", "yLabel": "relative residue count", "xRange": [0, 6], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-0.7*x)", "label": "few residues in disallowed space", "color": "#16a34a"}]}
```

**Next:** tertiary and quaternary structure.
""",
        ),
        _t(
            "Tertiary and quaternary structure",
            "11 min",
            r"""
# Tertiary and quaternary structure

**Tertiary structure** is the full three-dimensional fold of one polypeptide
chain — how its helices, sheets and loops pack into a compact globule. It is held
together by the side chains: a **hydrophobic core** of nonpolar residues buried
away from water, plus salt bridges, hydrogen bonds and occasional covalent
**disulfide bonds** (cysteine–cysteine) that staple distant parts together.
Recurring tertiary patterns — the four-helix bundle, the TIM barrel, the
immunoglobulin fold — are called **domains** and often correspond to functional
or evolutionary units.

**Quaternary structure** is the assembly of multiple folded chains
(**subunits**) into one complex, as in haemoglobin's $\alpha_2\beta_2$ tetramer.
Subunit interfaces use the same weak forces as the core, and quaternary
arrangement enables cooperative behaviour and regulation.

```mermaid
flowchart TB
  P["Primary sequence"] --> SEC["Secondary: helices and sheets"]
  SEC --> TER["Tertiary: domains, hydrophobic core, disulfides"]
  TER --> QUAT["Quaternary: subunit assembly"]
  QUAT --> FUNC["Function: catalysis, transport, signalling"]
```

Stability rises steeply as more nonpolar surface is buried in the core, a
roughly saturating relationship between core size and fold stability:

```plot
{"title": "Fold stability vs buried hydrophobic core", "xLabel": "buried nonpolar surface (relative)", "yLabel": "stability |ΔG| (relative)", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "saturating stabilisation", "color": "#2563eb"}]}
```

**Next:** the structure of DNA and base pairing.
""",
        ),
        _t(
            "Nucleic-acid structure and the double helix",
            "11 min",
            r"""
# Nucleic-acid structure and the double helix

DNA and RNA are polymers of **nucleotides**: a sugar (deoxyribose in DNA, ribose
in RNA), a phosphate, and one of four **bases** — adenine, guanine, cytosine and
thymine (uracil in RNA). The sugar–phosphate backbone runs in a definite
$5' \rightarrow 3'$ direction. In 1953 Watson and Crick, using Franklin's X-ray
fibre data, deduced the **double helix**: two antiparallel strands wound around a
common axis.

The strands are held by **complementary base pairing** through hydrogen bonds:
**A pairs with T** (two H-bonds) and **G pairs with C** (three H-bonds). This
complementarity means each strand templates the other — the structural basis of
replication. The canonical right-handed **B-form** helix has ~10.5 base pairs per
turn with a wide **major groove** and narrow **minor groove**, where
sequence-specific proteins read the DNA.

```mermaid
flowchart LR
  NT["Nucleotides: sugar + phosphate + base"] --> BB["5'->3' sugar-phosphate backbone"]
  BB --> BP["Base pairing: A-T (2 H-bonds), G-C (3 H-bonds)"]
  BP --> DH["Antiparallel right-handed double helix"]
  DH --> GR["Major and minor grooves read by proteins"]
```

Because G–C pairs add a third hydrogen bond, duplex stability (its melting
temperature) rises with GC content — more GC, more energy to separate the
strands:

```plot
{"title": "Duplex melting temperature vs GC content", "xLabel": "GC content (%)", "yLabel": "relative melting temperature", "xRange": [0, 100], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+40)", "label": "Tm rises with GC content", "color": "#dc2626"}]}
```

**Next:** the forces that stabilise folded macromolecules.
""",
        ),
        _t(
            "Forces that fold and stabilise molecules",
            "10 min",
            r"""
# Forces that fold and stabilise molecules

No covalent bond decides a protein's fold; it emerges from many **weak,
noncovalent interactions** acting together. The dominant driver is the
**hydrophobic effect**: water orders around nonpolar side chains, and the system
gains entropy by burying them in a core, so folding is largely entropy-driven.
Layered on top are **hydrogen bonds** (backbone and side chain), **van der Waals
contacts** from tight atomic packing, and **electrostatic salt bridges** between
oppositely charged groups.

These forces nearly cancel: the unfolded state has huge conformational entropy
that opposes folding. A typical small protein is stable by only **20–60 kJ/mol** —
the difference between two large numbers — which is why proteins are *marginally*
stable and can be unfolded by heat, pH or denaturants such as urea.

```mermaid
flowchart TB
  HYD["Hydrophobic effect (entropy-driven, dominant)"] --> NET["Net folding free energy"]
  HB["Hydrogen bonds"] --> NET
  VDW["Van der Waals packing"] --> NET
  ES["Salt bridges / electrostatics"] --> NET
  ENT["Backbone conformational entropy (opposes)"] --> NET
  NET --> FOLD["Marginally stable folded state"]
```

The buried nonpolar surface area scales the stabilising free energy almost
linearly — a key rule used in protein design:

```plot
{"title": "Stabilising free energy vs buried nonpolar area", "xLabel": "buried area (nm^2)", "yLabel": "|ΔG| gained (kJ/mol)", "xRange": [0, 6], "yRange": [0, 30], "grid": true, "functions": [{"expr": "4.5*x", "label": "ΔG ≈ 4.5·area", "color": "#16a34a"}]}
```

**Next:** check your understanding of structural fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Structural Biology — Intermediate ────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="structural-biology-intermediate",
    title="Structural Biology — Intermediate",
    description=(
        "The quantitative methods that turn molecules into atomic models. We "
        "cover folding thermodynamics and two-state denaturation curves, the "
        "energy landscape and folding kinetics, X-ray crystallography from "
        "Bragg's law to electron-density maps, cryo-electron microscopy and "
        "resolution, and how models are refined and validated. Interactive "
        "plots of denaturation, diffraction and resolution throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Folding thermodynamics and stability",
            "12 min",
            r"""
# Folding thermodynamics and stability

A small protein often folds as a **two-state** system: only folded (N) and
unfolded (U) states are appreciably populated. The equilibrium $\mathrm{N}
\rightleftharpoons \mathrm{U}$ has constant $K = [\mathrm{U}]/[\mathrm{N}]$ and
free energy $\Delta G = -RT \ln K$. The fraction unfolded is the sigmoid
$$f_U = \frac{K}{1+K} = \frac{1}{1+e^{\Delta G / RT}}.$$

Adding a chemical denaturant (urea, guanidinium) makes $\Delta G$ fall roughly
linearly with concentration, $\Delta G = \Delta G_{H_2O} - m[\text{denaturant}]$,
where the **$m$-value** reflects the surface area newly exposed on unfolding.
Where $f_U = 0.5$ defines the midpoint $C_m$. Thermal melts give the analogous
melting temperature $T_m$. Because folding buries enthalpy and entropy that vary
with temperature, $\Delta G(T)$ is a downward parabola (cold and heat
denaturation), governed by the heat-capacity change $\Delta C_p$.

```mermaid
flowchart LR
  N["Folded N"] -->|denaturant or heat| U["Unfolded U"]
  U --> K["K = [U]/[N]"]
  K --> DG["ΔG = -RT ln K"]
  DG --> CURVE["Sigmoidal denaturation curve"]
  CURVE --> CM["Midpoint Cm / Tm gives stability"]
```

The unfolding transition is a sharp sigmoid against denaturant concentration:

```plot
{"title": "Fraction unfolded vs denaturant", "xLabel": "denaturant (M)", "yLabel": "fraction unfolded f_U", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "two-state unfolding", "color": "#2563eb"}]}
```

**Next:** the folding energy landscape and kinetics.
""",
        ),
        _t(
            "The folding landscape and kinetics",
            "11 min",
            r"""
# The folding landscape and kinetics

How does a chain find its fold so fast? Levinthal's paradox notes that random
search over astronomically many conformations would take longer than the age of
the universe, yet small proteins fold in milliseconds. The resolution is the
**funnel-shaped energy landscape**: instead of one path, the chain rolls
downhill along many routes toward the native basin, biased at every step toward
native-like contacts. The funnel's width is conformational entropy; its depth is
energy.

Folding rate is set by the height of the highest barrier — the **transition
state**. Its position is probed by $\phi$-value analysis (mutating residues and
seeing whether they are native-like at the barrier). Some proteins populate
metastable **intermediates** or get trapped in misfolded states, the origin of
aggregation diseases. **Chaperones** (GroEL/GroES, Hsp70) provide protected
environments that prevent off-pathway aggregation.

```mermaid
flowchart TB
  U["Unfolded ensemble (wide, high)"] --> TS["Transition state (barrier)"]
  TS --> I["Optional intermediate"]
  I --> N["Native basin (narrow, low)"]
  TS --> N
  U -. aggregation .-> AGG["Misfolded / aggregated"]
  CH["Chaperones"] --> N
```

Under simple two-state kinetics, folding is first order, so the unfolded
population decays exponentially toward the native state with rate $k_f$:

```plot
{"title": "Approach to native state (first-order kinetics)", "xLabel": "time (relative)", "yLabel": "fraction still unfolded", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "exp(-k_f t)", "color": "#dc2626"}]}
```

**Next:** determining structures by X-ray crystallography.
""",
        ),
        _t(
            "X-ray crystallography: Bragg's law",
            "12 min",
            r"""
# X-ray crystallography: Bragg's law

X-ray crystallography has solved the majority of known atomic structures. The
sample is a **crystal** — a periodic 3D array of identical molecules — because a
single molecule scatters far too few X-rays to detect; the crystal lattice
amplifies scattering into discrete **diffraction spots (reflections)**.
Constructive interference occurs only at angles satisfying **Bragg's law**,
$$n\lambda = 2d\sin\theta,$$
where $d$ is the spacing between lattice planes, $\theta$ the incidence angle and
$\lambda$ the X-ray wavelength (~1 Å). Smaller $d$ (finer detail) diffracts to
larger $\theta$, so high-resolution data sit at the edge of the detector.

Each reflection has a measurable **intensity** (giving the amplitude) but the
**phase is lost** — the famous *phase problem*, solved by molecular replacement,
heavy-atom (isomorphous replacement) or anomalous methods. Combining amplitudes
and phases via a Fourier transform yields the **electron-density map**, into
which the atomic model is built.

```mermaid
flowchart LR
  XTAL["Protein crystal"] --> BEAM["X-ray beam"]
  BEAM --> DIFF["Diffraction pattern (reflections)"]
  DIFF --> AMP["Intensities -> amplitudes"]
  DIFF --> PHASE["Phase problem -> MR / SAD / MIR"]
  AMP --> FT["Fourier transform"]
  PHASE --> FT
  FT --> MAP["Electron-density map -> atomic model"]
```

Bragg's law ties diffraction angle to plane spacing; for fixed $\lambda$ the
required $\sin\theta$ rises as spacing shrinks:

```plot
{"title": "Bragg condition: sin(theta) vs 1/d", "xLabel": "1/d (1/Angstrom)", "yLabel": "sin(theta) (lambda=1.5 A)", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.75*x", "label": "sin(theta) = lambda/(2d)", "color": "#2563eb"}]}
```

**Next:** cryo-electron microscopy and resolution.
""",
        ),
        _t(
            "Cryo-electron microscopy",
            "12 min",
            r"""
# Cryo-electron microscopy

**Cryo-EM** images molecules directly with an electron beam, no crystal needed.
Purified particles are flash-frozen in a thin film of **vitreous (glassy) ice** —
so fast that water cannot crystallise and the molecules are trapped in random
orientations. A transmission electron microscope records thousands of noisy 2D
projection images.

The breakthrough **single-particle reconstruction** workflow aligns and averages
millions of particles: software assigns each image an orientation, then
back-projects them to rebuild the 3D **Coulomb potential** density. Two advances
drove the "resolution revolution" of the 2010s — **direct electron detectors**
(fast, low-noise, enabling motion correction of beam-induced drift) and better
software (RELION, cryoSPARC). Cryo-EM excels at large, flexible assemblies
(ribosomes, membrane proteins, viruses) that resist crystallisation, and can
even resolve multiple conformational states from one sample.

```mermaid
flowchart LR
  SAMPLE["Purified particles"] --> FREEZE["Plunge-freeze in vitreous ice"]
  FREEZE --> IMG["Many noisy 2D projections"]
  IMG --> ALIGN["Assign orientations and classify"]
  ALIGN --> RECON["3D reconstruction (back-projection)"]
  RECON --> MAP["Coulomb-potential map -> atomic model"]
```

Signal-to-noise — and thus achievable resolution — improves as more particles
are averaged, scaling roughly with the square root of particle count (diminishing
returns):

```plot
{"title": "Map quality vs number of averaged particles", "xLabel": "particles (x10^3)", "yLabel": "relative SNR / quality", "xRange": [0, 100], "yRange": [0, 12], "grid": true, "functions": [{"expr": "sqrt(x)", "label": "SNR ~ sqrt(N)", "color": "#16a34a"}]}
```

**Next:** model building, refinement and validation.
""",
        ),
        _t(
            "Resolution, refinement and validation",
            "11 min",
            r"""
# Resolution, refinement and validation

**Resolution** (in ångströms) states the finest detail an experimental map
distinguishes — *smaller is better*. At ~3.5 Å you see the backbone and bulky
side chains; at ~2 Å individual atoms and water molecules; below ~1.2 Å,
hydrogen positions. The model is improved by **refinement**: adjusting atomic
coordinates and B-factors to best match the data while obeying stereochemical
restraints (bond lengths, angles, Ramachandran).

Fit to data is tracked by the **R-factor** and the cross-validated **$R_{free}$**
(computed on a held-out subset of reflections to detect overfitting); a good
structure keeps $R_{free}$ low and close to $R_{work}$. Geometry is checked with
the Ramachandran plot, clash scores and rotamer outliers (e.g. via MolProbity).
For cryo-EM, resolution is estimated from the **Fourier Shell Correlation (FSC)**
between two independently processed half-maps, with the 0.143 threshold as the
reported figure.

```mermaid
flowchart TB
  MAP["Experimental map"] --> BUILD["Build atomic model"]
  BUILD --> REFINE["Refine: coordinates, B-factors, restraints"]
  REFINE --> RWORK["R-work / R-free vs data"]
  REFINE --> GEOM["Geometry: Ramachandran, clashes, rotamers"]
  REFINE --> FSC["Cryo-EM: FSC half-maps (0.143)"]
  RWORK --> DEPO["Deposit validated model (PDB)"]
  GEOM --> DEPO
  FSC --> DEPO
```

The number of observed reflections — and so the information available per
atom — grows steeply as resolution improves (the count scales with the inverse
cube of resolution):

```plot
{"title": "Reflections available vs resolution", "xLabel": "resolution (Angstrom, lower = better)", "yLabel": "relative reflection count", "xRange": [1, 4], "yRange": [0, 12], "grid": true, "functions": [{"expr": "8/(x^2)", "label": "more data at higher resolution", "color": "#dc2626"}]}
```

**Next:** check your understanding of the core methods.
""",
        ),
        _quiz(),
    ),
)


# ── Structural Biology — Advanced ────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="structural-biology-advanced",
    title="Structural Biology — Advanced",
    description=(
        "State-of-the-art and applied structural biology. We connect structure "
        "to function and mechanism, model allostery and cooperativity with the "
        "MWC framework, study conformational dynamics by molecular dynamics, "
        "and turn structures into drugs through structure-based design and "
        "docking — closing with deep-learning structure prediction (AlphaFold) "
        "and generative design. Quantitative plots throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Structure-function and active sites",
            "12 min",
            r"""
# Structure-function and active sites

Function follows form. An enzyme's **active site** is a precisely shaped pocket
where a handful of residues, often distant in sequence, are brought together by
the fold to bind substrate and catalyse a reaction. Catalysis arises from
**transition-state stabilisation** — the enzyme binds the strained transition
state more tightly than the substrate, lowering the activation barrier $\Delta
G^\ddagger$ and so accelerating the rate (the Eyring relation makes rate fall
exponentially in $\Delta G^\ddagger$).

Classic mechanisms illustrate how geometry encodes chemistry: the **catalytic
triad** (Ser–His–Asp) of serine proteases like chymotrypsin positions a
nucleophilic serine; metal ions, general acid/base residues and oxyanion holes
all tune reactivity. Specificity comes from complementary shape and chemistry —
the **induced-fit** refinement of the older lock-and-key picture.

```mermaid
flowchart LR
  FOLD["3D fold"] --> SITE["Active-site pocket"]
  SITE --> BIND["Bind substrate (shape + chemistry)"]
  BIND --> TS["Stabilise transition state"]
  TS --> CAT["Lower ΔG‡ -> rate boost"]
  CAT --> PROD["Release product"]
```

Because rate depends exponentially on the barrier, even a modest reduction in
$\Delta G^\ddagger$ yields a large rate enhancement:

```plot
{"title": "Rate enhancement vs barrier lowering", "xLabel": "barrier lowered ΔΔG‡ (units of RT)", "yLabel": "relative rate", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "rate ~ exp(ΔΔG‡/RT)", "color": "#2563eb"}]}
```

**Next:** allostery and cooperative binding.
""",
        ),
        _t(
            "Allostery and cooperativity",
            "12 min",
            r"""
# Allostery and cooperativity

**Allostery** is regulation at a distance: a ligand binding one site changes
activity at another, propagated through the structure. The textbook example is
**haemoglobin**, whose four subunits bind oxygen **cooperatively** — binding at
one site raises the affinity of the others, giving a sigmoidal (S-shaped)
oxygen-binding curve ideal for loading O$_2$ in the lungs and unloading it in
tissues.

Two classic models explain this. In the **MWC (concerted)** model the whole
oligomer flips between a low-affinity **T (tense)** state and a high-affinity **R
(relaxed)** state in unison; ligand binding shifts the equilibrium toward R. In
the **KNF (sequential)** model each subunit changes one at a time. Cooperativity
is quantified by the **Hill coefficient** $n_H$ from the Hill equation
$$\theta = \frac{[L]^{n}}{K_d + [L]^{n}};$$
$n_H > 1$ means positive cooperativity (haemoglobin $\approx 2.8$), while $n_H =
1$ is non-cooperative (myoglobin).

```mermaid
flowchart LR
  L1["Ligand binds one site"] --> CONF["Conformational change"]
  CONF --> TR["T-state <-> R-state shift (MWC)"]
  TR --> COOP["Raised affinity at other sites"]
  COOP --> SIG["Sigmoidal binding curve, n_H > 1"]
```

A Hill curve with $n>1$ is sigmoidal — shallow at low ligand, then sharply
switching — unlike the hyperbolic curve of a non-cooperative binder:

```plot
{"title": "Cooperative (Hill) binding curve", "xLabel": "ligand concentration (relative)", "yLabel": "fractional saturation θ", "xRange": [0, 8], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "Hill, n=2 (cooperative)", "color": "#dc2626"}]}
```

**Next:** conformational dynamics by molecular dynamics.
""",
        ),
        _t(
            "Conformational dynamics and molecular dynamics",
            "12 min",
            r"""
# Conformational dynamics and molecular dynamics

A crystal structure is a single snapshot, but proteins **breathe** — loops open,
domains hinge, side chains rotate. These motions are often the function:
substrate access, allosteric signalling and catalysis all rely on dynamics.
**Molecular dynamics (MD)** simulates them by integrating Newton's equations for
every atom under an empirical **force field** (AMBER, CHARMM), advancing in
~2 femtosecond steps so that bond vibrations are resolved.

The catch is timescale: many biological motions take microseconds to
milliseconds, requiring billions of steps. Special hardware (Anton), GPUs and
**enhanced-sampling** methods (replica exchange, metadynamics, Markov state
models) extend reach. Analysis treats the trajectory as an ensemble sampling the
free-energy landscape, revealing metastable states and pathways invisible to a
static model.

```mermaid
flowchart LR
  STRUCT["Starting structure"] --> FF["Force field + solvent"]
  FF --> INT["Integrate Newton's eqns (~2 fs steps)"]
  INT --> TRAJ["Trajectory (ensemble)"]
  TRAJ --> ANALYSIS["Free-energy landscape, MSM, pathways"]
  ANALYSIS --> INSIGHT["Mechanism, cryptic pockets, kinetics"]
```

Accessible simulation length grows linearly with raw compute, but reaching ever
slower processes hits diminishing returns — useful sampling of rare events
saturates with wall-clock time:

```plot
{"title": "Conformational states sampled vs simulation time", "xLabel": "simulation time (relative)", "yLabel": "rare states sampled (relative)", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "diminishing returns on rare events", "color": "#16a34a"}]}
```

**Next:** structure-based drug design and docking.
""",
        ),
        _t(
            "Structure-based drug design and docking",
            "12 min",
            r"""
# Structure-based drug design and docking

Knowing a target's 3D structure lets chemists design molecules to fit it —
**structure-based drug design (SBDD)**. The cycle: solve the target structure
(often with a bound ligand), identify a druggable pocket, design or screen
molecules that complement it, test affinity, then refine using the new
complex structure. HIV protease inhibitors and the kinase inhibitor imatinib are
landmark successes.

**Molecular docking** predicts how a small molecule binds: software (AutoDock
Vina, Glide) samples poses in the pocket and scores each by an approximate
binding energy from shape complementarity, hydrogen bonds and hydrophobic
contacts. **Virtual screening** docks millions of library compounds to rank
candidates cheaply before synthesis. **Fragment-based** design instead starts
from tiny, weakly binding fragments found by crystallography or NMR and grows or
links them. Scoring-function accuracy remains the central limitation, so
predictions are confirmed experimentally.

```mermaid
flowchart LR
  TARGET["Target structure + pocket"] --> DOCK["Dock library (sample + score poses)"]
  DOCK --> RANK["Rank candidates (virtual screen)"]
  RANK --> TEST["Synthesize and assay top hits"]
  TEST --> XRAY["Co-crystal / cryo-EM of complex"]
  XRAY --> OPT["Optimize affinity (design cycle)"]
  OPT --> DOCK
```

Binding strength follows simple mass-action: fractional occupancy of the target
rises hyperbolically with inhibitor concentration relative to its $K_d$:

```plot
{"title": "Target occupancy vs inhibitor concentration", "xLabel": "inhibitor / K_d", "yLabel": "fractional occupancy", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "occupancy = [I]/([I]+K_d)", "color": "#2563eb"}]}
```

**Next:** AI structure prediction and design.
""",
        ),
        _t(
            "Deep learning: AlphaFold and protein design",
            "13 min",
            r"""
# Deep learning: AlphaFold and protein design

In 2020 **AlphaFold 2** largely solved the decades-old protein-structure
prediction problem, reaching near-experimental accuracy at CASP14. Its key ideas:
mine **multiple sequence alignments (MSAs)** — co-evolving residue pairs hint at
3D contacts — process them with an attention-based **Evoformer**, and a
**structure module** that outputs atomic coordinates end to end, with a
per-residue confidence score (**pLDDT**). AlphaFold (and RoseTTAFold) now provide
predicted structures for nearly every known protein, and **AlphaFold-Multimer**
tackles complexes.

The same revolution runs in reverse: **generative design**. Tools like
**RFdiffusion** denoise random coordinates into novel backbones for a desired
function, **ProteinMPNN** designs sequences that fold to a given backbone, and
diffusion/language models propose binders and enzymes never seen in nature.
Predictions still need experimental validation — for novel folds, dynamics,
ligand effects and accuracy where MSAs are shallow.

```mermaid
flowchart LR
  SEQ["Target sequence"] --> MSA["Build MSA (co-evolution)"]
  MSA --> EVO["Evoformer (attention)"]
  EVO --> SM["Structure module -> coordinates"]
  SM --> CONF["pLDDT confidence"]
  CONF --> USE["Use / validate experimentally"]
  DESIGN["Generative design: RFdiffusion + ProteinMPNN"] --> USE
```

Prediction confidence climbs with the number of effective sequences in the MSA,
then plateaus — deep alignments give high-confidence models, shallow ones do
not:

```plot
{"title": "Prediction confidence vs MSA depth", "xLabel": "effective sequences (relative)", "yLabel": "mean pLDDT (relative)", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "confidence saturates with MSA depth", "color": "#16a34a"}]}
```

**Next:** check your understanding of advanced structural biology.
""",
        ),
        _quiz(),
    ),
)


STRUCTURAL_BIOLOGY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["STRUCTURAL_BIOLOGY_COURSES"]
