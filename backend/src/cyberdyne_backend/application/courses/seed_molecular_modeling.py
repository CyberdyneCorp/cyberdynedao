"""Molecular Modeling & Visualization track: Basics -> Intermediate -> Advanced.

A three-level track on building, scoring and inspecting 3D molecular models. It
moves from atomic coordinates, force fields and the potential energy surface;
through energy minimization, conformer generation and molecular visualization;
to homology modeling, model validation and full system preparation for
simulation. Lessons are `text` with LaTeX, interactive ```plot blocks (potential
energy curves, minimization convergence, Boltzmann populations) and ```mermaid
pipeline diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Molecular Modeling & Visualization — Basics ──────────────────────────────

_BASICS = SeedCourse(
    slug="molecular-modeling-basics",
    title="Molecular Modeling & Visualization — Basics",
    description=(
        "An intuitive introduction to representing molecules on a computer. We "
        "build from atomic coordinates and file formats, through the idea of a "
        "potential energy surface and the bonded and non-bonded terms of a "
        "force field, to the difference between molecular mechanics and quantum "
        "methods and the basics of looking at structures in a viewer. "
        "Interactive plots and pipeline diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Atomic coordinates and molecular representations",
            "10 min",
            r"""
# Atomic coordinates and molecular representations

To model a molecule we first describe **where its atoms are**. The simplest
representation is a list of **Cartesian coordinates**: for each atom an element
symbol and an $(x, y, z)$ position, usually in **ångström** ($1\,\text{Å} =
10^{-10}\,\text{m}$). A molecule of $N$ atoms therefore lives in a $3N$-dimensional
configuration space.

Common file formats encode this differently. **XYZ** is a bare element-and-coordinate
list. **PDB** (Protein Data Bank) adds residue names, chain ids and atom names so
biomolecules can be interpreted. **MOL/SDF** and **MOL2** add explicit **bonds**
and **bond orders**, which small-molecule modeling needs. An alternative is the
**Z-matrix** (internal coordinates): each atom is placed by a bond length, a bond
angle and a dihedral relative to atoms already placed.

```mermaid
flowchart LR
  ATOMS["Atoms: element + (x,y,z)"] --> XYZ["XYZ: coords only"]
  ATOMS --> PDB["PDB: + residues/chains"]
  ATOMS --> SDF["SDF/MOL2: + bonds & orders"]
  ATOMS --> ZMAT["Z-matrix: bond/angle/dihedral"]
```

Cartesian and internal coordinates each have uses: Cartesians are simple for
simulation, while internals make it natural to scan a single torsion. Converting
between them is routine. The total atom count grows the cost of everything we do
later, so size matters from the start:

```plot
{"title": "Configuration-space dimension vs atom count", "xLabel": "atoms N", "yLabel": "degrees of freedom (3N)", "xRange": [0, 20], "yRange": [0, 60], "grid": true, "functions": [{"expr": "3*x", "label": "3N Cartesian DOF", "color": "#2563eb"}]}
```

**Next:** the energy landscape that ranks one geometry against another.
""",
        ),
        _t(
            "The potential energy surface",
            "11 min",
            r"""
# The potential energy surface

Every set of coordinates has an **energy**. Mapping energy as a function of all
atomic positions gives the **potential energy surface (PES)**, $E(\mathbf{r})$.
The PES is the central object of molecular modeling: low-energy points are stable
geometries and high-energy points are strained or transient.

Special points matter. A **local minimum** is a stable conformer — the gradient
$\nabla E = 0$ and all curvatures are positive. The **global minimum** is the most
stable arrangement. A **saddle point** (a maximum along one direction, minimum in
the rest) is a **transition state** linking two minima; its height above a minimum
is an **energy barrier**. The Born–Oppenheimer approximation lets us treat $E$ as a
function of nuclear positions because electrons relax almost instantly.

```mermaid
flowchart LR
  PES["Potential energy surface E(r)"] --> MIN["Minima = stable conformers"]
  PES --> TS["Saddle points = transition states"]
  MIN --> GLOB["Global minimum"]
  TS --> BAR["Barrier height between minima"]
```

A one-dimensional slice along a torsion shows the idea: two wells (gauche/anti
conformers) separated by a barrier. A simple cosine model of a dihedral term
captures the periodicity of such a slice:

```plot
{"title": "Torsional energy slice through the PES", "xLabel": "dihedral angle (scaled)", "yLabel": "relative energy", "xRange": [0, 7], "yRange": [-1.2, 1.2], "grid": true, "functions": [{"expr": "cos(2*x)", "label": "two-fold torsion: wells and barriers", "color": "#dc2626"}]}
```

**Next:** the force-field terms that let us compute that energy cheaply.
""",
        ),
        _t(
            "Force fields and bonded terms",
            "11 min",
            r"""
# Force fields and bonded terms

Computing $E$ from quantum mechanics for every geometry is expensive. A **force
field** instead approximates the energy with simple analytical functions of the
geometry plus fitted **parameters**. The total energy splits into **bonded** and
**non-bonded** contributions; this lesson covers the bonded ones.

Bond stretching and angle bending are usually **harmonic** (Hooke's law):
$$E_{bond} = \frac{1}{2} k_b (r - r_0)^2, \qquad E_{angle} = \frac{1}{2} k_\theta (\theta - \theta_0)^2$$
where $r_0$ and $\theta_0$ are equilibrium values and $k_b, k_\theta$ are stiffness
constants. **Torsions** (dihedrals) use a periodic cosine series,
$E_{tors} = \sum_n \frac{V_n}{2}\,[1 + \cos(n\phi - \gamma)]$, capturing the
multiple minima a rotatable bond can adopt.

```mermaid
flowchart TB
  FF["Force field energy"] --> BOND["Bond stretch: harmonic"]
  FF --> ANG["Angle bend: harmonic"]
  FF --> TORS["Torsion: cosine series"]
  FF --> NB["Non-bonded (next lesson)"]
```

Widely used biomolecular force fields include **AMBER**, **CHARMM**, **OPLS** and
**GROMOS**; **MMFF94** and **GAFF** target small molecules. The harmonic bond term
makes a parabola around the equilibrium length — accurate near $r_0$, but it can
never break a bond:

```plot
{"title": "Harmonic bond-stretch energy", "xLabel": "bond length r (A)", "yLabel": "energy (relative)", "xRange": [0, 4], "yRange": [0, 5], "grid": true, "functions": [{"expr": "(x-1.5)^2", "label": "0.5 k (r - r0)^2, r0 = 1.5 A", "color": "#2563eb"}]}
```

**Next:** the non-bonded forces between atoms that are not bonded.
""",
        ),
        _t(
            "Non-bonded interactions: van der Waals and electrostatics",
            "11 min",
            r"""
# Non-bonded interactions: van der Waals and electrostatics

Atoms that are not directly bonded still interact. These **non-bonded** terms
dominate intermolecular forces, packing and binding, and are the most expensive
part of a force-field evaluation because they scale with pairs of atoms.

**Van der Waals** interactions combine short-range Pauli repulsion with longer-range
dispersion attraction, captured by the **Lennard-Jones** potential:
$$E_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$$
with well depth $\varepsilon$ and collision diameter $\sigma$. **Electrostatics**
use Coulomb's law between partial atomic charges, $E_{elec} = \frac{q_i q_j}{4\pi\varepsilon_0 r}$,
decaying slowly as $1/r$ — which is why long-range methods like **Particle Mesh
Ewald** are needed for periodic systems.

```mermaid
flowchart LR
  NB["Non-bonded terms"] --> VDW["Van der Waals (Lennard-Jones)"]
  NB --> ELEC["Electrostatics (Coulomb)"]
  VDW --> REP["r^-12 repulsion"]
  VDW --> DISP["r^-6 dispersion"]
  ELEC --> PME["Long range: Particle Mesh Ewald"]
```

The Lennard-Jones curve has a minimum at $r = 2^{1/6}\sigma$ and rises steeply at
short range. A scaled version shows the characteristic well and the hard wall:

```plot
{"title": "Lennard-Jones potential", "xLabel": "distance r (scaled)", "yLabel": "energy (relative)", "xRange": [0.9, 3], "yRange": [-1.2, 2], "grid": true, "functions": [{"expr": "4*((1/x)^12 - (1/x)^6)", "label": "repulsion + dispersion", "color": "#dc2626"}]}
```

**Next:** when force fields are enough and when you need quantum mechanics.
""",
        ),
        _t(
            "Molecular mechanics vs quantum methods",
            "10 min",
            r"""
# Molecular mechanics vs quantum methods

Two broad families compute molecular energies. **Molecular mechanics (MM)** uses
force fields: it treats atoms as classical balls and springs, ignores electrons
explicitly, and is fast enough for thousands to millions of atoms. **Quantum
mechanics (QM)** solves (approximately) the electronic Schrödinger equation, so it
can describe **bond breaking, charge transfer and electronic states** that MM
cannot — but at a steep cost.

QM methods span a ladder of accuracy and expense: **semi-empirical** (fast,
parameterised), **density functional theory (DFT)** (the workhorse), and
**post-Hartree–Fock** wavefunction methods (highly accurate, very expensive). Cost
scales roughly as $N^3$ to $N^7$ in the number of basis functions, versus near
$N \log N$ for well-implemented MM. **QM/MM** schemes combine both: a small reactive
region is treated with QM, the surroundings with MM.

```mermaid
flowchart LR
  E["Energy method"] --> MM["Molecular mechanics: fast, no electrons"]
  E --> QM["Quantum: electrons explicit"]
  QM --> SE["Semi-empirical"]
  QM --> DFT["DFT"]
  QM --> PHF["Post-Hartree-Fock"]
  MM --> QMMM["QM/MM hybrid"]
  QM --> QMMM
```

The cost gap grows fast with system size. Comparing a cubic MM-like scaling with a
much steeper QM-like power makes the trade-off concrete:

```plot
{"title": "Compute cost vs system size", "xLabel": "system size (relative)", "yLabel": "cost (relative)", "xRange": [1, 6], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x^3", "label": "MM ~ N^3 region", "color": "#16a34a"}, {"expr": "x^4", "label": "QM steeper scaling", "color": "#dc2626"}]}
```

**Next:** turning coordinates into pictures with a molecular viewer.
""",
        ),
        _t(
            "Visualizing molecules",
            "10 min",
            r"""
# Visualizing molecules

A model is only useful if you can **see** it. Molecular viewers read coordinate
files and render atoms and bonds, letting you rotate, slice and color structures
to reason about geometry and interactions. Popular tools include **PyMOL**,
**VMD**, **ChimeraX**, and browser libraries such as **3Dmol.js** and **NGL**.

Different **representations** answer different questions. **Ball-and-stick** and
**stick** show covalent connectivity; **space-filling (CPK)** uses van der Waals
radii to reveal shape and packing; **cartoon/ribbon** abstracts a protein backbone
into helices and sheets so the fold is legible; **surface** views (molecular or
solvent-accessible) expose pockets and electrostatics. Coloring **by element**, **by
secondary structure**, or **by a property** (charge, B-factor, hydrophobicity)
turns numbers into intuition.

```mermaid
flowchart TB
  COORD["Coordinate file"] --> VIEW["Molecular viewer"]
  VIEW --> BS["Ball-and-stick / stick"]
  VIEW --> CPK["Space-filling (CPK)"]
  VIEW --> CART["Cartoon / ribbon"]
  VIEW --> SURF["Surface (SASA / molecular)"]
  SURF --> POCK["Reveals binding pockets"]
```

A practical detail: the **solvent-accessible surface area (SASA)** grows with
molecular size but more slowly than volume, because surface scales sub-linearly with
the number of atoms. A saturating curve captures this diminishing exposure per atom:

```plot
{"title": "Exposed surface per atom (stylised)", "xLabel": "buried-core fraction", "yLabel": "relative exposed surface", "xRange": [0, 6], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating surface exposure", "color": "#2563eb"}]}
```

**Next:** test your grasp of coordinates, energy and force fields.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Modeling & Visualization — Intermediate ────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="molecular-modeling-intermediate",
    title="Molecular Modeling & Visualization — Intermediate",
    description=(
        "The core quantitative methods of molecular modeling. We cover energy "
        "minimization algorithms and convergence, conformational search and the "
        "Boltzmann weighting of conformers, partial-charge assignment and "
        "protonation states, solvation models, and the geometry checks that "
        "tell a good model from a bad one. Interactive plots and method "
        "diagrams throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Energy minimization algorithms",
            "12 min",
            r"""
# Energy minimization algorithms

A raw structure usually sits high on the PES with bad contacts. **Energy
minimization (geometry optimization)** moves atoms downhill to the nearest local
minimum where $\nabla E \approx 0$. It does **not** cross barriers, so the result
depends on the starting point — minimization finds a *local*, not the global,
minimum.

The simplest method is **steepest descent**: step along the negative gradient,
$\mathbf{r}_{k+1} = \mathbf{r}_k - \alpha\,\nabla E(\mathbf{r}_k)$. It is robust far
from a minimum but zig-zags and converges slowly near one. **Conjugate gradient**
mixes in the previous direction to avoid that zig-zag. **Newton/quasi-Newton**
methods (e.g. **L-BFGS**) use curvature (the Hessian, or an approximation) for fast
quadratic convergence close to the minimum. A common recipe runs a few steepest-descent
steps first, then switches to conjugate gradient or L-BFGS.

```mermaid
flowchart LR
  START["Strained start structure"] --> SD["Steepest descent: robust, slow"]
  SD --> CG["Conjugate gradient: faster"]
  CG --> QN["Quasi-Newton / L-BFGS: curvature"]
  QN --> MIN["Local minimum, grad ~ 0"]
```

Convergence is judged by the **gradient norm (RMS force)** and energy change falling
below tolerances. A typical run shows the gradient decaying roughly exponentially as
iterations proceed:

```plot
{"title": "Minimization convergence", "xLabel": "iteration", "yLabel": "RMS gradient (relative)", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "RMS force decaying to tolerance", "color": "#2563eb"}]}
```

**Next:** searching the full conformational landscape, not just one well.
""",
        ),
        _t(
            "Conformational search and sampling",
            "12 min",
            r"""
# Conformational search and sampling

A flexible molecule has many minima — **conformers** — differing in torsion angles.
Because minimization only reaches the nearest well, finding the relevant low-energy
conformers needs a deliberate **conformational search**. The number of conformers
explodes combinatorially: with $m$ rotatable bonds and roughly $k$ states each, there
are about $k^m$ candidates.

Common strategies: **systematic search** rotates each torsion through a grid (exact
but exponential); **stochastic / Monte Carlo** randomly perturbs torsions and accepts
moves by an energy criterion; **distance-geometry** (used by **RDKit's ETKDG**)
generates 3D embeddings from connectivity; and **genetic algorithms** evolve a
population of conformers. Each candidate is then minimized and **clustered** by RMSD
to remove duplicates.

```mermaid
flowchart LR
  MOL["Flexible molecule"] --> GEN["Generate candidates"]
  GEN --> SYS["Systematic grid"]
  GEN --> MC["Monte Carlo / stochastic"]
  GEN --> DG["Distance geometry (ETKDG)"]
  GEN --> GA["Genetic algorithm"]
  SYS --> MIN["Minimize + cluster by RMSD"]
  MC --> MIN
  DG --> MIN
  GA --> MIN
```

Search difficulty grows fast with flexibility. The conformer count rises
exponentially with the number of rotatable bonds, which is why exhaustive search
becomes infeasible quickly:

```plot
{"title": "Conformer count vs rotatable bonds", "xLabel": "rotatable bonds", "yLabel": "candidate conformers (relative)", "xRange": [0, 8], "yRange": [0, 100], "grid": true, "functions": [{"expr": "exp(0.6*x)", "label": "combinatorial explosion ~ k^m", "color": "#dc2626"}]}
```

**Next:** how energies translate into the populations we actually observe.
""",
        ),
        _t(
            "Boltzmann populations of conformers",
            "11 min",
            r"""
# Boltzmann populations of conformers

Knowing conformer energies is not enough; we want their **relative populations** at
a temperature $T$. Statistical mechanics gives the **Boltzmann distribution**: the
probability of conformer $i$ with energy $E_i$ is
$$p_i = \frac{e^{-E_i / k_B T}}{\sum_j e^{-E_j / k_B T}}$$
where $k_B$ is Boltzmann's constant and the denominator is the **partition function**.
A relative energy $\Delta E$ above the lowest conformer gives a population ratio
$e^{-\Delta E / k_B T}$.

At room temperature $k_B T \approx 0.59\,\text{kcal/mol}$ ($\approx 2.5\,\text{kJ/mol}$).
So a conformer only $\sim 1.4\,\text{kcal/mol}$ higher is already about ten-fold less
populated, and anything more than a few $k_B T$ above the minimum is essentially
invisible. Strictly, populations depend on **free energy** $G$, which adds an
**entropy** term; many software defaults approximate this with potential energy plus
a vibrational/entropic correction.

```mermaid
flowchart LR
  ENERGIES["Conformer energies E_i"] --> BOLTZ["Boltzmann weighting exp(-E/kT)"]
  BOLTZ --> Z["Partition function (normalise)"]
  Z --> POP["Populations p_i"]
  POP --> AVG["Boltzmann-averaged property"]
```

The occupancy of a higher state falls exponentially with its energy gap, scaled by
temperature — the core of the distribution:

```plot
{"title": "Population ratio vs energy gap", "xLabel": "delta E / kT", "yLabel": "relative population", "xRange": [0, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-1*x)", "label": "exp(-deltaE/kT)", "color": "#2563eb"}]}
```

**Next:** assigning the partial charges and protonation states models depend on.
""",
        ),
        _t(
            "Partial charges and protonation states",
            "11 min",
            r"""
# Partial charges and protonation states

Force-field electrostatics need a **partial charge** on every atom, and the right
charges depend on the molecule's **protonation state** — which is not obvious from a
bare structure. Getting these wrong is one of the most common causes of garbage
results.

**Partial charges** are assigned by schemes of increasing rigor: empirical
**Gasteiger** charges (fast), bond-charge **AM1-BCC** (the GAFF/AMBER default for
ligands), and **RESP** fitting to a QM electrostatic potential (the gold standard).
**Protonation state** is governed by each ionizable group's $\text{p}K_a$ relative to
the solution pH; the **Henderson–Hasselbalch** relation gives the fraction
deprotonated, $\frac{[\text{A}^-]}{[\text{HA}]} = 10^{\,\text{pH} - \text{p}K_a}$. At
physiological pH ($\approx 7.4$) aspartate/glutamate are anionic, lysine/arginine
cationic, and **histidine** ($\text{p}K_a \approx 6$) sits on the fence — its
tautomer/charge often must be set by hand or by a tool like **PROPKA** or **H++**.

```mermaid
flowchart LR
  STRUCT["Structure (no H, no charges)"] --> PROT["Assign protonation (pKa vs pH)"]
  PROT --> ADDH["Add hydrogens"]
  ADDH --> CHG["Assign partial charges"]
  CHG --> GAST["Gasteiger"]
  CHG --> AM1["AM1-BCC"]
  CHG --> RESP["RESP (QM ESP fit)"]
```

The titration curve from Henderson–Hasselbalch is a sigmoid centered on the $\text{p}K_a$;
the group is half-ionized exactly at $\text{pH} = \text{p}K_a$:

```plot
{"title": "Fraction deprotonated vs pH", "xLabel": "pH", "yLabel": "fraction deprotonated", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "sigmoid centred at pKa = 5", "color": "#dc2626"}]}
```

**Next:** representing the solvent that surrounds almost every real model.
""",
        ),
        _t(
            "Solvation models",
            "11 min",
            r"""
# Solvation models

Molecules rarely live in vacuum. **Solvation** — usually by water — reshapes the
energy landscape, screens electrostatics and drives the hydrophobic effect. Modeling
it well is essential for realistic energies and binding.

Two families dominate. **Explicit solvent** places real water molecules (models such
as **TIP3P, TIP4P, SPC/E**) plus counter-ions in a periodic box around the solute;
it is accurate but adds thousands of atoms and cost. **Implicit solvent** replaces
water with a continuum dielectric: **Poisson–Boltzmann (PB)** solves the
electrostatics rigorously, while **Generalized Born (GB)** approximates it cheaply,
and a surface-area term ($\gamma \cdot \text{SASA}$) models the nonpolar cost of
making a cavity. The combination **MM/PBSA** and **MM/GBSA** is widely used to
estimate binding free energies.

```mermaid
flowchart LR
  SOLV["Solvation model"] --> EXP["Explicit: TIP3P / SPC/E + ions"]
  SOLV --> IMP["Implicit: continuum dielectric"]
  IMP --> PB["Poisson-Boltzmann"]
  IMP --> GB["Generalized Born"]
  PB --> SASA["+ nonpolar SASA term"]
  GB --> SASA
```

A key effect is **dielectric screening**: in water (dielectric constant $\approx 80$)
a charge–charge interaction is damped roughly as $1/\varepsilon r$, far weaker than in
vacuum. The screened Coulomb energy decays much faster with distance:

```plot
{"title": "Electrostatic energy: vacuum vs water", "xLabel": "distance r (scaled)", "yLabel": "interaction energy (relative)", "xRange": [1, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/x", "label": "vacuum ~ 1/r", "color": "#dc2626"}, {"expr": "1/(80*x)", "label": "water ~ 1/(80 r)", "color": "#2563eb"}]}
```

**Next:** checking whether a finished model is geometrically sane.
""",
        ),
        _t(
            "Model quality and geometry validation",
            "10 min",
            r"""
# Model quality and geometry validation

A model that minimizes to low energy can still be **physically wrong**. Validation
checks geometry against known statistics from high-resolution structures before you
trust a model.

Core checks: the **Ramachandran plot** of backbone $\phi/\psi$ angles should place
residues in favoured regions, with outliers explained; **bond lengths and angles**
should match equilibrium values within a small RMSD; **clashscore** counts severe
van der Waals overlaps (steric clashes); **rotamer outliers** flag side chains in
improbable conformations; and **chirality** and *cis/trans* peptide bonds must be
correct. Standard tools include **MolProbity**, **PROCHECK** and **WHAT_CHECK**, and
for comparing two structures the **RMSD** after superposition.

```mermaid
flowchart TB
  MODEL["Candidate model"] --> RAMA["Ramachandran favoured?"]
  MODEL --> CLASH["Clashscore (vdW overlaps)"]
  MODEL --> ROT["Rotamer outliers"]
  MODEL --> GEOM["Bond/angle RMSD"]
  RAMA --> SCORE["MolProbity score"]
  CLASH --> SCORE
  ROT --> SCORE
  GEOM --> SCORE
```

RMSD between two structures grows with atom-position differences but is reported in
ångström; small RMSD means close agreement. A simple saturating view shows how RMSD
rises and then plateaus as structures diverge:

```plot
{"title": "RMSD vs structural divergence (stylised)", "xLabel": "perturbation (relative)", "yLabel": "RMSD (A, relative)", "xRange": [0, 8], "yRange": [0, 3], "grid": true, "functions": [{"expr": "3*x/(x+2)", "label": "RMSD saturating with divergence", "color": "#16a34a"}]}
```

**Next:** test your grasp of minimization, sampling and validation.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Modeling & Visualization — Advanced ────────────────────────────

_ADVANCED = SeedCourse(
    slug="molecular-modeling-advanced",
    title="Molecular Modeling & Visualization — Advanced",
    description=(
        "State-of-the-art and applied molecular modeling. We cover homology and "
        "comparative modeling, AI structure prediction with AlphaFold and "
        "RoseTTAFold, loop and side-chain modeling and refinement, full system "
        "preparation for molecular dynamics, and structure-based and "
        "generative AI approaches to design. Interactive plots and pipeline "
        "diagrams throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Homology and comparative modeling",
            "12 min",
            r"""
# Homology and comparative modeling

When no experimental structure exists, **homology (comparative) modeling** builds
one from a related protein of known structure. It rests on a key fact: **structure
is more conserved than sequence**, so homologous proteins share a fold.

The classic pipeline: (1) **template search** — find structures of homologs (e.g.
via BLAST/HHblits against the PDB); (2) **target–template alignment** — a careful
sequence alignment, the step that most determines model quality; (3) **model
building** — copy conserved core coordinates and build the rest, as **MODELLER** does
by satisfying spatial restraints; (4) **loop and side-chain modeling**; (5)
**refinement and validation**. Accuracy tracks **sequence identity**: above $\sim 50\%$
models rival medium-resolution experiments, around $30\%$ they are useful with care,
and below the **twilight zone** ($\sim 20$–$25\%$) alignments become unreliable.

```mermaid
flowchart LR
  TARGET["Target sequence"] --> SEARCH["Template search (PDB homologs)"]
  SEARCH --> ALIGN["Target-template alignment"]
  ALIGN --> BUILD["Build core (MODELLER restraints)"]
  BUILD --> LOOP["Model loops + side chains"]
  LOOP --> VAL["Refine + validate"]
```

Model quality degrades sharply as identity drops. A stylised curve shows accuracy
falling off as percent identity decreases toward the twilight zone:

```plot
{"title": "Model accuracy vs sequence identity (stylised)", "xLabel": "sequence identity (scaled)", "yLabel": "relative model accuracy", "xRange": [0, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "1/(1+(3/x)^2)", "label": "accuracy rising with identity (Hill)", "color": "#2563eb"}]}
```

**Next:** how deep learning rewrote the structure-prediction game.
""",
        ),
        _t(
            "AI structure prediction: AlphaFold and beyond",
            "12 min",
            r"""
# AI structure prediction: AlphaFold and beyond

In 2020 **AlphaFold2** achieved near-experimental accuracy at CASP14, transforming
the field. It predicts structure directly from sequence using a deep network, with no
explicit force field, by learning from the PDB and from **evolutionary information**.

The central input is a **multiple sequence alignment (MSA)**: co-evolving residue
pairs signal spatial contacts. AlphaFold2's **Evoformer** processes the MSA and a
pairwise residue representation, and a **structure module** outputs 3D coordinates,
iterating by **recycling**. It reports per-residue confidence as **pLDDT** and
inter-domain confidence as **PAE**. Related systems include **RoseTTAFold**, the
**ESMFold** language-model approach (no MSA needed), and **AlphaFold3** /
**AlphaFold-Multimer** for complexes, nucleic acids and ligands. Caveats remain:
single static conformations, weaker results for orphan sequences, disorder and the
effects of point mutations.

```mermaid
flowchart LR
  SEQ["Query sequence"] --> MSA["Build MSA + templates"]
  MSA --> EVO["Evoformer: MSA + pair repr."]
  EVO --> STRUCT["Structure module -> 3D"]
  STRUCT --> RECYC["Recycle (refine)"]
  RECYC --> CONF["pLDDT / PAE confidence"]
```

Prediction accuracy improves with the **depth of the MSA** — more diverse homologs
give stronger co-evolution signal — but with diminishing returns once the alignment
is deep enough:

```plot
{"title": "Predicted accuracy vs MSA depth (stylised)", "xLabel": "effective MSA depth (log-scaled)", "yLabel": "relative accuracy", "xRange": [0, 8], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "saturating gain from more homologs", "color": "#16a34a"}]}
```

**Next:** fixing the hardest parts of a model — loops and side chains.
""",
        ),
        _t(
            "Loop modeling, side chains and refinement",
            "11 min",
            r"""
# Loop modeling, side chains and refinement

Cores copy well from templates; the hard parts are **loops** (insertions/deletions
with no template) and **side-chain placement**. These regions often carry function —
active-site loops, binding specificity — so getting them right matters.

**Loop modeling** uses two approaches: **knowledge-based**, searching a database of
loop fragments matching the anchor geometry and length; and **ab initio**, sampling
loop conformations and scoring them (e.g. **MODELLER's** loop refinement, **Rosetta's**
KIC/CCD, **next-generation KIC**). **Side-chain modeling** places rotamers from a
**backbone-dependent rotamer library** (Dunbrack) and resolves clashes by optimization
(**SCWRL4**, dead-end elimination, simulated annealing). Final **refinement** relieves
strain and improves geometry via energy minimization or short **molecular dynamics**,
ideally guided by a physically realistic energy and validated afterward.

```mermaid
flowchart TB
  MODEL["Core model"] --> LOOPS["Loop modeling"]
  LOOPS --> KB["Knowledge-based fragments"]
  LOOPS --> AB["Ab initio sampling (KIC/CCD)"]
  MODEL --> SC["Side chains: rotamer library"]
  SC --> OPT["SCWRL4 / dead-end elimination"]
  KB --> REFINE["Refine: minimization / short MD"]
  AB --> REFINE
  OPT --> REFINE
```

Loop prediction difficulty rises steeply with **loop length**: short loops are nearly
solved, but accuracy falls off as the loop grows and the conformational space explodes:

```plot
{"title": "Loop prediction accuracy vs length (stylised)", "xLabel": "loop length (residues)", "yLabel": "relative accuracy", "xRange": [1, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.25*x)", "label": "accuracy decaying with loop length", "color": "#dc2626"}]}
```

**Next:** assembling a complete, simulation-ready system.
""",
        ),
        _t(
            "System preparation for molecular dynamics",
            "12 min",
            r"""
# System preparation for molecular dynamics

A validated static model is not yet ready to **simulate**. **System preparation** is
the meticulous set of steps that turn coordinates into a stable, physically meaningful
molecular dynamics (MD) input — and skipped steps cause crashes or silent artefacts.

A standard workflow: **clean the structure** (fix missing atoms/residues, remove
crystallographic waters or keep key ones, model missing loops); **assign protonation
and add hydrogens** at the target pH; **parameterise any ligands** (e.g. GAFF +
AM1-BCC); **solvate** in a periodic box of explicit water with a buffer to the box
edge; **neutralise and add salt** (e.g. 0.15 M NaCl) to set ionic strength; then
**relax in stages** — energy minimize, heat to target temperature with restraints,
**equilibrate** in NVT then NPT to settle density, and finally release restraints for
**production MD**. Tools include **CHARMM-GUI**, **AmberTools (tleap)**, **GROMACS**
and **OpenMM**.

```mermaid
flowchart LR
  CLEAN["Clean structure"] --> PROT["Protonate + add H"]
  PROT --> LIG["Parameterise ligands"]
  LIG --> SOLV["Solvate (periodic box)"]
  SOLV --> IONS["Neutralise + add salt"]
  IONS --> MIN["Minimize"]
  MIN --> EQ["Heat + NVT/NPT equilibrate"]
  EQ --> PROD["Production MD"]
```

Equilibration shows up as observables settling: the system temperature relaxes
exponentially toward the thermostat target before production begins:

```plot
{"title": "Temperature equilibration", "xLabel": "time (relative)", "yLabel": "approach to target T", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1 - exp(-0.6*x)", "label": "T relaxing to setpoint", "color": "#2563eb"}]}
```

**Next:** using models to design new molecules.
""",
        ),
        _t(
            "Structure-based and generative design",
            "12 min",
            r"""
# Structure-based and generative design

The payoff of a good model is **design**: using 3D structure to find or invent
molecules that bind a target. This spans classical **structure-based drug design
(SBDD)** and a new wave of **generative AI**.

In SBDD, **molecular docking** (AutoDock Vina, Glide, GOLD) poses candidate ligands in
a binding pocket and scores them; **virtual screening** ranks large libraries;
**pharmacophore** models abstract the required interaction features; and **free-energy
perturbation (FEP)** computes accurate relative binding affinities for lead
optimization. Generative methods now design from scratch: **RFdiffusion** and protein
**diffusion models** generate novel backbones, **ProteinMPNN** designs sequences to fit
a backbone, and ligand generators propose new chemotypes — all validated by docking,
MD and, ultimately, experiment. The honest loop is **design → model → simulate →
validate → make → test**.

```mermaid
flowchart LR
  TARGET["Target structure / pocket"] --> DOCK["Docking + virtual screening"]
  TARGET --> GEN["Generative design"]
  GEN --> RFD["RFdiffusion (backbone)"]
  GEN --> MPNN["ProteinMPNN (sequence)"]
  DOCK --> FEP["FEP affinity refinement"]
  RFD --> VAL["Model + MD + experiment"]
  MPNN --> VAL
  FEP --> VAL
```

Docking score is only a rough proxy for affinity, but stronger predicted binding
generally raises the chance a candidate is a true hit — a dose-response-like enrichment
that saturates:

```plot
{"title": "Hit probability vs predicted binding (stylised)", "xLabel": "predicted binding strength", "yLabel": "probability of true hit", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-5)))", "label": "enrichment with stronger score", "color": "#16a34a"}]}
```

**Next:** test your grasp of homology, AI prediction and design.
""",
        ),
        _quiz(),
    ),
)


MOLECULAR_MODELING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MOLECULAR_MODELING_COURSES"]
