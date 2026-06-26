"""Molecular Dynamics Simulations track: Basics -> Intermediate -> Advanced.

A three-level computational track spanning Newtonian dynamics, force fields and
time integrators; through ensembles, thermostats, barostats, periodic boundary
conditions and solvation; and on to free energy, enhanced sampling, trajectory
analysis and machine-learned potentials. Lessons are `text` with LaTeX,
interactive ```plot blocks (potentials, integrator stability, autocorrelation,
free-energy profiles) and ```mermaid diagrams for the MD loop and pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Molecular Dynamics Simulations — Basics ──────────────────────────────────

_BASICS = SeedCourse(
    slug="molecular-dynamics-basics",
    title="Molecular Dynamics Simulations — Basics",
    description=(
        "The conceptual and physical foundations of molecular dynamics: Newton's "
        "equations of motion for atoms, the potential energy surface and force "
        "fields, the Lennard-Jones and Coulomb interactions, time integration with "
        "the Verlet family of algorithms, and how temperature emerges from atomic "
        "velocities. Built around intuition with interactive plots and process "
        "diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What molecular dynamics computes",
            "10 min",
            r"""
# What molecular dynamics computes

Molecular dynamics (MD) follows the motion of a collection of atoms by solving
**Newton's second law** for every particle:

$$m_i \frac{d^2 \mathbf{r}_i}{dt^2} = \mathbf{F}_i = -\nabla_i U(\mathbf{r}_1,\dots,\mathbf{r}_N).$$

The force on atom $i$ is minus the gradient of a **potential energy function**
$U$ that depends on all atomic positions. Given positions and velocities at one
instant, MD advances them by a tiny **time step** $\Delta t$ (typically $1$–$2$
femtoseconds) and repeats millions of times. The output is a **trajectory**: the
positions and velocities as a function of time, from which thermodynamic and
kinetic properties are extracted by averaging.

MD treats nuclei as classical point masses moving on a single potential energy
surface — the **Born–Oppenheimer** approximation lets us separate fast electrons
from slow nuclei. Tools like GROMACS, NAMD, LAMMPS, OpenMM and AMBER implement
this loop efficiently on GPUs.

The number of integration steps grows linearly with the physical time you want
to simulate:

```plot
{"title": "Steps required vs simulated time (dt = 2 fs)", "xLabel": "simulated time (ns)", "yLabel": "steps (millions)", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "0.5*x", "label": "steps = t / dt", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  POS["Positions & velocities"] --> FORCE["Compute forces F = -grad U"]
  FORCE --> INT["Integrate one step dt"]
  INT --> POS
  INT --> TRAJ["Save trajectory frame"]
```

**Next:** the potential energy surface and what a force field is.
""",
        ),
        _t(
            "The potential energy surface & force fields",
            "11 min",
            r"""
# The potential energy surface & force fields

The heart of MD is the **potential energy function** $U(\mathbf{r})$, also called
the **force field**. A classical biomolecular force field (AMBER, CHARMM, OPLS,
GROMOS) splits energy into bonded and non-bonded terms:

$$U = \sum_{\text{bonds}} \tfrac{1}{2} k_b (r-r_0)^2 + \sum_{\text{angles}} \tfrac{1}{2} k_\theta (\theta-\theta_0)^2 + \sum_{\text{dihedrals}} \tfrac{V_n}{2}\big(1+\cos(n\phi-\gamma)\big) + U_{\text{nonbonded}}.$$

Bonds and angles are stiff harmonic springs; **dihedrals** are periodic torsion
terms that encode rotational preferences. The **non-bonded** part — van der Waals
and electrostatics — is the most expensive because it couples every pair of
atoms. The parameters ($k_b$, $r_0$, partial charges, Lennard-Jones radii) are
fit to quantum chemistry and experiment.

A harmonic bond energy is a parabola centred on the equilibrium length:

```plot
{"title": "Harmonic bond potential", "xLabel": "bond length r (relative to r0)", "yLabel": "energy (relative)", "xRange": [-3, 3], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x^2", "label": "U = (1/2) k (r - r0)^2", "color": "#2563eb"}]}
```

```mermaid
flowchart TB
  U["Force field U"] --> B["Bonded terms"]
  U --> NB["Non-bonded terms"]
  B --> BO["bonds"]
  B --> AN["angles"]
  B --> DI["dihedrals"]
  NB --> VDW["van der Waals (Lennard-Jones)"]
  NB --> EL["electrostatics (Coulomb)"]
```

**Next:** the Lennard-Jones and Coulomb interactions in detail.
""",
        ),
        _t(
            "Lennard-Jones & electrostatic interactions",
            "11 min",
            r"""
# Lennard-Jones & electrostatic interactions

Non-bonded forces dominate MD cost and physics. The **Lennard-Jones (LJ)**
potential models van der Waals interactions between two neutral atoms:

$$U_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right].$$

The $r^{-12}$ term is steep **Pauli repulsion** (overlapping electron clouds);
the $r^{-6}$ term is attractive **dispersion** (London forces from instantaneous
dipoles). The well depth is $\varepsilon$ and the zero-crossing is at $\sigma$;
the minimum sits at $r_{min}=2^{1/6}\sigma$. **Electrostatics** uses Coulomb's
law between partial charges:

$$U_{C}(r) = \frac{1}{4\pi\varepsilon_0}\frac{q_i q_j}{r}.$$

Coulomb decays slowly ($r^{-1}$), so it cannot simply be truncated — long-range
methods like Particle-Mesh Ewald (covered later) are needed. LJ decays fast, so
a **cutoff** of $\sim 1$ nm is acceptable.

The LJ curve shows repulsion, an attractive well, and a flat tail:

```plot
{"title": "Lennard-Jones potential (sigma = 1, eps = 1)", "xLabel": "separation r/sigma", "yLabel": "energy / eps", "xRange": [0.9, 3], "yRange": [-1.5, 3], "grid": true, "functions": [{"expr": "4*((1/x)^12 - (1/x)^6)", "label": "U_LJ", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  NB["Non-bonded pair"] --> LJ["Lennard-Jones: short range, r^-6/r^-12"]
  NB --> CO["Coulomb: long range, r^-1"]
  LJ --> CUT["cutoff ~ 1 nm OK"]
  CO --> PME["needs Ewald/PME"]
```

**Next:** turning forces into motion with the Verlet integrator.
""",
        ),
        _t(
            "Time integration & the Verlet algorithm",
            "11 min",
            r"""
# Time integration & the Verlet algorithm

Once forces are known we must advance positions and velocities in time. The
workhorse is the **velocity Verlet** integrator:

$$\mathbf{r}(t+\Delta t) = \mathbf{r}(t) + \mathbf{v}(t)\Delta t + \tfrac{1}{2}\mathbf{a}(t)\Delta t^2,$$
$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \tfrac{1}{2}\big(\mathbf{a}(t)+\mathbf{a}(t+\Delta t)\big)\Delta t.$$

Verlet is popular because it is **symplectic** (it conserves a shadow energy and
shows no long-term energy drift), **time-reversible**, and needs only one force
evaluation per step. The accuracy is $O(\Delta t^2)$ in position.

The step size is bounded by the **fastest motion** — bond vibrations of hydrogen
at $\sim 10$ fs periods force $\Delta t \le 1$–$2$ fs. Constraining bonds with
**SHAKE/LINCS** removes those vibrations and allows larger steps.

Energy error per step grows steeply with the time step, so stability is lost
abruptly past a critical $\Delta t$:

```plot
{"title": "Energy drift vs time step (schematic)", "xLabel": "time step dt (fs)", "yLabel": "relative energy error", "xRange": [0, 5], "yRange": [0, 5], "grid": true, "functions": [{"expr": "0.04*x^3", "label": "error ~ dt^3 per step", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  A["a(t) from forces"] --> R["update r(t+dt)"]
  R --> F2["recompute forces -> a(t+dt)"]
  F2 --> V["update v(t+dt)"]
  V --> A
```

**Next:** how temperature emerges from atomic velocities.
""",
        ),
        _t(
            "Temperature, kinetic energy & equipartition",
            "10 min",
            r"""
# Temperature, kinetic energy & equipartition

In MD, **temperature is not an input — it is measured** from how fast atoms move.
The instantaneous kinetic energy is

$$E_K = \sum_{i=1}^{N} \tfrac{1}{2} m_i v_i^2,$$

and the **equipartition theorem** assigns $\tfrac{1}{2}k_B T$ of energy to each
quadratic degree of freedom. For $N_f$ degrees of freedom (about $3N$ minus
constraints),

$$T = \frac{2 E_K}{N_f k_B}.$$

At equilibrium, atomic speeds follow the **Maxwell–Boltzmann distribution**, so
heavy atoms move slowly and light atoms fast at the same temperature. Initial
velocities are usually drawn from this distribution at the target $T$; the system
then **equilibrates** before data collection. Because $T$ comes from kinetic
energy, controlling temperature means controlling velocities — the job of a
**thermostat**, introduced in the next course.

Mean kinetic energy rises linearly with temperature (equipartition):

```plot
{"title": "Average kinetic energy vs temperature", "xLabel": "temperature T (relative)", "yLabel": "average E_K per atom", "xRange": [0, 10], "yRange": [0, 15], "grid": true, "functions": [{"expr": "1.5*x", "label": "E_K = (3/2) k_B T", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  V["Atomic velocities"] --> EK["Kinetic energy E_K"]
  EK --> T["Instantaneous T = 2 E_K / (N_f k_B)"]
  T --> MB["Maxwell-Boltzmann at equilibrium"]
```

**Next:** test your grasp of the MD fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Dynamics Simulations — Intermediate ────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="molecular-dynamics-intermediate",
    title="Molecular Dynamics Simulations — Intermediate",
    description=(
        "The core quantitative machinery of production MD: statistical ensembles "
        "and how they are realised, thermostats and barostats for NVT/NPT, periodic "
        "boundary conditions and the minimum-image convention, long-range "
        "electrostatics with Particle-Mesh Ewald, explicit and implicit solvation, "
        "and a practical equilibration-to-production workflow."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Statistical ensembles in MD",
            "11 min",
            r"""
# Statistical ensembles in MD

A single trajectory samples a **statistical ensemble** — the set of microstates
consistent with fixed macroscopic constraints. Plain Newtonian MD conserves
energy, so it naturally samples the **microcanonical (NVE)** ensemble: fixed
particle number $N$, volume $V$, and total energy $E$. But experiments are
usually at fixed temperature and pressure, so we want other ensembles:

- **NVT (canonical):** fixed $N,V,T$ — couple to a thermostat.
- **NPT (isothermal-isobaric):** fixed $N,P,T$ — add a barostat.
- **muVT (grand canonical):** fixed chemical potential, exchange particles.

The **ergodic hypothesis** justifies replacing an ensemble average over many
microstates with a **time average** over one long trajectory:

$$\langle A \rangle = \lim_{t\to\infty}\frac{1}{t}\int_0^t A(\tau)\,d\tau.$$

Properties fluctuate around their mean; fluctuations themselves carry physics —
e.g. energy fluctuations in NVT give the heat capacity.

A measured observable converges to its ensemble mean as the average lengthens:

```plot
{"title": "Running average converging to the ensemble mean", "xLabel": "simulation time (ns)", "yLabel": "running average of A", "xRange": [0.2, 10], "yRange": [0, 4], "grid": true, "functions": [{"expr": "3 - 2*exp(-0.5*x)", "label": "running mean -> <A>", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  NVE["NVE: fix E"] --> NVT["NVT: fix T (thermostat)"]
  NVT --> NPT["NPT: fix P,T (barostat)"]
  NPT --> AVG["Time average = ensemble average (ergodic)"]
```

**Next:** controlling temperature with thermostats.
""",
        ),
        _t(
            "Thermostats: controlling temperature",
            "12 min",
            r"""
# Thermostats: controlling temperature

A **thermostat** holds the average temperature at a target by adjusting atomic
velocities. The simplest is **velocity rescaling**, which multiplies all
velocities by $\lambda=\sqrt{T_0/T}$; the **Berendsen** thermostat does this
weakly with a coupling time $\tau$:

$$\frac{dT}{dt} = \frac{T_0 - T}{\tau}.$$

Berendsen equilibrates fast but **suppresses fluctuations**, so it does not
generate a true canonical ensemble — fine for warm-up, wrong for production. For
correct NVT sampling use **Nosé–Hoover** (an extended-system method that adds a
fictitious thermostat variable with its own equation of motion) or
**velocity-rescale (v-rescale / CSVR)**, which adds a stochastic term so the
kinetic energy distribution is exactly canonical. **Langevin dynamics** couples
each atom to a friction-plus-random-force bath.

Berendsen coupling relaxes the temperature exponentially toward the target:

```plot
{"title": "Temperature relaxation under a thermostat", "xLabel": "time (ps)", "yLabel": "temperature (K, offset from target)", "xRange": [0, 10], "yRange": [0, 50], "grid": true, "functions": [{"expr": "50*exp(-0.5*x)", "label": "T - T0 ~ exp(-t/tau)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  KE["Measured kinetic energy -> T"] --> CMP["Compare to target T0"]
  CMP --> ADJ["Scale velocities"]
  ADJ -->|"Berendsen: weak, no true canonical"| KE
  ADJ -->|"Nose-Hoover / v-rescale: correct NVT"| KE
```

**Next:** controlling pressure with barostats.
""",
        ),
        _t(
            "Barostats & periodic boundary conditions",
            "12 min",
            r"""
# Barostats & periodic boundary conditions

To reach NPT we also control **pressure**, computed from the **virial**:

$$P = \frac{N k_B T}{V} + \frac{1}{3V}\left\langle \sum_{i<j} \mathbf{r}_{ij}\cdot\mathbf{F}_{ij}\right\rangle.$$

A **barostat** rescales the box volume (and atomic coordinates) to drive $P$ to
target. **Berendsen** pressure coupling relaxes weakly; **Parrinello–Rahman** and
**Monte Carlo (MC) barostats** give correct NPT fluctuations and allow the box
shape to change.

To avoid surfaces, MD uses **periodic boundary conditions (PBC)**: the simulation
box is tiled infinitely, and an atom leaving one face re-enters the opposite
face. Forces use the **minimum-image convention** — each atom interacts with the
nearest periodic copy of every other atom. The cutoff must be below half the box
length so no atom sees two images of the same neighbour.

The error in the minimum-image scheme stays controlled only while the cutoff is
below half the box edge:

```plot
{"title": "Cutoff constraint under the minimum-image convention", "xLabel": "cutoff / box length", "yLabel": "self-interaction error (relative)", "xRange": [0, 0.9], "yRange": [0, 5], "grid": true, "functions": [{"expr": "0.1/(0.5-x)", "label": "error blows up as cutoff -> L/2", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  BOX["Central box"] --> IMG["Tile periodic images"]
  IMG --> MIN["Minimum-image: nearest copy"]
  MIN --> CUT["Cutoff < L/2"]
  BOX --> VOL["Barostat rescales V to set P"]
```

**Next:** long-range electrostatics with Particle-Mesh Ewald.
""",
        ),
        _t(
            "Long-range electrostatics: Particle-Mesh Ewald",
            "12 min",
            r"""
# Long-range electrostatics: Particle-Mesh Ewald

Coulomb interactions decay as $r^{-1}$ — too slowly to truncate at a cutoff
without artifacts. **Ewald summation** splits the electrostatic energy into a
fast-converging **real-space** part and a **reciprocal-space** part using a
Gaussian charge-screening parameter $\alpha$:

$$\frac{q_iq_j}{r} = \underbrace{\frac{q_iq_j\,\mathrm{erfc}(\alpha r)}{r}}_{\text{short range}} + \underbrace{\text{(reciprocal-space sum)}}_{\text{long range}}.$$

The complementary error function $\mathrm{erfc}(\alpha r)$ damps the short-range
term so it can use a cutoff; the smooth long-range part is summed efficiently in
Fourier space. **Particle-Mesh Ewald (PME)** interpolates charges onto a grid and
uses the **FFT**, cutting cost from $O(N^2)$ to $O(N\log N)$. PME is the default
for periodic biomolecular MD; **Particle-Particle Particle-Mesh (PPPM)** is the
analogous LAMMPS method.

The screened short-range term decays rapidly thanks to the complementary error
function:

```plot
{"title": "Ewald real-space damping of Coulomb (alpha = 1)", "xLabel": "separation r", "yLabel": "screened energy (relative)", "xRange": [0.3, 4], "yRange": [0, 3], "grid": true, "functions": [{"expr": "exp(-x)/x", "label": "erfc-like decay -> cutoff OK", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  C["Coulomb 1/r"] --> SPLIT["Ewald split (alpha)"]
  SPLIT --> RS["Real space: erfc, short, cutoff"]
  SPLIT --> KS["Reciprocal space: smooth"]
  KS --> GRID["PME: charges on grid"]
  GRID --> FFT["FFT -> O(N log N)"]
```

**Next:** putting the molecule in water — solvation.
""",
        ),
        _t(
            "Solvation: explicit & implicit water",
            "11 min",
            r"""
# Solvation: explicit & implicit water

Biomolecules live in water, so most MD adds **solvent**. In **explicit
solvation** the box is filled with thousands of water molecules using models like
**TIP3P, TIP4P, SPC/E** — rigid point-charge geometries fit to reproduce water's
density, dielectric and structure. Counter-ions (Na+, Cl-) neutralise net charge
and set ionic strength. Explicit water is accurate but expensive: most atoms in a
typical simulation are water.

**Implicit solvation** replaces water with a continuum dielectric, modelling
solvation free energy with **Generalized Born (GB)** or **Poisson–Boltzmann (PB)**
theory plus a surface-area term for the nonpolar cost. It is far cheaper and
removes solvent viscosity (faster conformational sampling) but loses specific
water-mediated contacts and hydrodynamics.

The radial distribution function $g(r)$ of explicit water shows clear hydration
shells — peaks where neighbouring molecules pack:

```plot
{"title": "Water structure: radial distribution function g(r)", "xLabel": "distance r (relative)", "yLabel": "g(r)", "xRange": [0.5, 6], "yRange": [0, 3], "grid": true, "functions": [{"expr": "1 + 1.5*exp(-(x-1)*(x-1))*cos(2*(x-1))", "label": "first/second hydration shells", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  SOL["Solvation"] --> EXP["Explicit: TIP3P/SPC/E + ions"]
  SOL --> IMP["Implicit: GB / Poisson-Boltzmann"]
  EXP --> ACC["accurate, expensive"]
  IMP --> FAST["fast, no specific waters"]
```

**Next:** the equilibration-to-production workflow.
""",
        ),
        _t(
            "Equilibration & the production workflow",
            "11 min",
            r"""
# Equilibration & the production workflow

A reliable MD study follows a staged **protocol**, not a single run. The typical
pipeline is: build and parameterise the system; **solvate** and add ions;
**energy-minimise** to remove bad contacts (steepest descent); **heat** gradually
to the target temperature under NVT with position restraints on the solute;
**equilibrate** density under NPT; release restraints; then run **production** MD
for analysis.

Skipping equilibration corrupts results — properties measured before the system
relaxes are meaningless. **Convergence checks** include energy and temperature
stability, RMSD plateauing, and density settling. Restraints on heavy atoms during
heating prevent the structure from distorting while solvent and velocities relax.
Frame-saving frequency trades disk for time resolution; observables are averaged
only over the **production** segment.

Potential energy falls steeply during minimisation, then levels off — the cue to
move to heating:

```plot
{"title": "Energy minimisation before dynamics", "xLabel": "minimisation step (x100)", "yLabel": "potential energy (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "9*exp(-0.8*x) + 0.5", "label": "U decreasing to a plateau", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  BUILD["Build & parameterise"] --> SOLV["Solvate + ions"]
  SOLV --> MIN["Minimise"]
  MIN --> HEAT["Heat (NVT, restraints)"]
  HEAT --> EQ["Equilibrate (NPT)"]
  EQ --> PROD["Production MD -> analysis"]
```

**Next:** check your understanding of production MD methods.
""",
        ),
        _quiz(),
    ),
)


# ── Molecular Dynamics Simulations — Advanced ────────────────────────────────

_ADVANCED = SeedCourse(
    slug="molecular-dynamics-advanced",
    title="Molecular Dynamics Simulations — Advanced",
    description=(
        "State-of-the-art and applied molecular dynamics: free energy from "
        "thermodynamic integration and FEP, enhanced sampling with umbrella "
        "sampling, metadynamics and replica exchange, trajectory analysis "
        "(RMSD/RMSF, PCA, Markov state models), machine-learned interatomic "
        "potentials, and ab initio / QM-MM dynamics."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Free energy: thermodynamic integration & FEP",
            "12 min",
            r"""
# Free energy: thermodynamic integration & FEP

The quantity that decides binding, folding and solubility is the **free energy
difference** $\Delta G$, not the potential energy. Free energies cannot be read
off a single trajectory because they include entropy. Two rigorous alchemical
methods dominate.

**Thermodynamic integration (TI)** couples states $A$ and $B$ with a parameter
$\lambda$ and integrates the average derivative of the Hamiltonian:

$$\Delta G = \int_0^1 \left\langle \frac{\partial H}{\partial \lambda} \right\rangle_\lambda \, d\lambda.$$

**Free energy perturbation (FEP)** uses the Zwanzig exponential-averaging
identity between neighbouring $\lambda$ windows:

$$\Delta G = -k_B T \ln \left\langle e^{-(H_B - H_A)/k_B T} \right\rangle_A.$$

Both need good overlap between windows; **Bennett acceptance ratio (BAR)** and
**MBAR** combine all windows optimally and are the modern standard. Relative
binding free energies (FEP+) now guide drug design.

The TI integrand $\langle \partial H / \partial \lambda \rangle$ is integrated
across the alchemical path; the area under it is $\Delta G$:

```plot
{"title": "Thermodynamic integration: dH/dlambda along the path", "xLabel": "coupling parameter lambda", "yLabel": "<dH/dlambda>", "xRange": [0, 1], "yRange": [-5, 5], "grid": true, "functions": [{"expr": "4*cos(3.14159*x)", "label": "area under curve = Delta G", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  A["State A"] --> L["lambda windows 0 -> 1"]
  L --> B["State B"]
  L --> TI["TI: integrate <dH/dl>"]
  L --> FEP["FEP: exp-average"]
  TI --> G["Delta G"]
  FEP --> G
```

**Next:** biasing the sampling to cross high barriers.
""",
        ),
        _t(
            "Enhanced sampling: umbrella sampling & metadynamics",
            "12 min",
            r"""
# Enhanced sampling: umbrella sampling & metadynamics

Plain MD is trapped by **free-energy barriers**: a process that takes
microseconds to milliseconds is rarely seen in a nanosecond run. **Enhanced
sampling** adds a bias along chosen **collective variables (CVs)** — distances,
dihedrals, coordination numbers — to flatten barriers.

**Umbrella sampling** runs many windows, each with a harmonic restraint pinning
the CV to a different value; the **weighted histogram analysis method (WHAM)** or
MBAR stitches the windows into a **potential of mean force (PMF)**, the free
energy along the CV. **Metadynamics** instead deposits Gaussian "hills" of bias
into already-visited regions, progressively filling wells so the system escapes;
**well-tempered metadynamics** shrinks the hills over time for convergence. The
accumulated bias is the negative of the free-energy surface.

A double-well PMF along a reaction coordinate shows the barrier enhanced sampling
must overcome:

```plot
{"title": "Potential of mean force along a collective variable", "xLabel": "collective variable", "yLabel": "free energy G (kJ/mol)", "xRange": [-3, 3], "yRange": [-2, 12], "grid": true, "functions": [{"expr": "x^4 - 5*x^2 + 6", "label": "double-well PMF", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  CV["Choose collective variables"] --> US["Umbrella sampling: harmonic windows"]
  CV --> MD["Metadynamics: deposit Gaussian hills"]
  US --> WHAM["WHAM/MBAR -> PMF"]
  MD --> FES["Bias -> free-energy surface"]
```

**Next:** parallel tempering with replica exchange.
""",
        ),
        _t(
            "Replica exchange molecular dynamics",
            "11 min",
            r"""
# Replica exchange molecular dynamics

**Replica exchange MD (REMD)**, or parallel tempering, runs many copies of the
system at different temperatures simultaneously. High-temperature replicas cross
barriers easily; periodically, neighbouring replicas attempt to **swap**
configurations with a Metropolis criterion that preserves each ensemble:

$$P_{\text{accept}} = \min\!\left(1,\; \exp\!\big[(\beta_i-\beta_j)(E_i-E_j)\big]\right),$$

where $\beta = 1/k_B T$. Accepted swaps let a low-temperature replica inherit a
barrier-crossing move discovered hotter, dramatically improving sampling of
folding and conformational change. Efficiency requires **overlapping potential
energy distributions** between neighbours, so the temperature ladder is spaced
geometrically and the replica count grows with system size. **Hamiltonian
replica exchange (H-REMD)** swaps along a scaled interaction instead of
temperature, needing fewer replicas.

Acceptance probability falls as the temperature gap widens, which sets the
spacing of the replica ladder:

```plot
{"title": "Swap acceptance vs temperature gap", "xLabel": "temperature gap between replicas (relative)", "yLabel": "acceptance probability", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.6*x)", "label": "P_accept decreases with gap", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  R1["Replica T1 (low)"] -->|"swap?"| R2["Replica T2"]
  R2 -->|"swap?"| R3["Replica T3 (high)"]
  R3 --> CROSS["Hot replica crosses barrier"]
  CROSS --> R1
```

**Next:** extracting meaning from trajectories.
""",
        ),
        _t(
            "Trajectory analysis: RMSD, PCA & Markov models",
            "12 min",
            r"""
# Trajectory analysis: RMSD, PCA & Markov models

A trajectory is high-dimensional; analysis projects it onto interpretable
coordinates. **RMSD** (root-mean-square deviation, after optimal alignment)
measures how far a structure has drifted from a reference; **RMSF**
(root-mean-square fluctuation) measures per-residue flexibility. **Principal
component analysis (PCA)** diagonalises the coordinate covariance matrix; the top
eigenvectors are large-amplitude collective motions, and projecting onto them
gives the **essential dynamics**.

**Markov state models (MSMs)** discretise conformational space into states and
estimate a transition matrix $T(\tau)$ from observed jumps over a lag time
$\tau$. Eigenvalues of $T$ give relaxation timescales; slow eigenvectors reveal
metastable states and pathways, letting many short trajectories be stitched into
long-timescale kinetics (PyEMMA, MSMBuilder, MDAnalysis, MDTraj).

RMSD typically rises then plateaus as a structure equilibrates around a basin:

```plot
{"title": "Backbone RMSD over a trajectory", "xLabel": "time (ns)", "yLabel": "RMSD (nm)", "xRange": [0, 10], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.35*(1 - exp(-0.6*x))", "label": "RMSD plateau = equilibrated", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  TRAJ["Trajectory"] --> RMSD["RMSD / RMSF"]
  TRAJ --> PCA["PCA -> essential dynamics"]
  TRAJ --> MSM["Discretise + transition matrix"]
  MSM --> KIN["Slow eigenvectors -> kinetics & states"]
```

**Next:** machine-learned interatomic potentials.
""",
        ),
        _t(
            "Machine-learned interatomic potentials",
            "12 min",
            r"""
# Machine-learned interatomic potentials

Classical force fields are fast but fixed; quantum methods are accurate but
scale poorly. **Machine-learned interatomic potentials (MLIPs)** bridge the gap:
a neural network is trained on **ab initio** (DFT) energies and forces, then
predicts them at near-classical cost with near-quantum accuracy.

Models respect physical symmetries — translation, rotation and permutation
invariance — using local atomic environments. Early networks (**Behler–Parrinello
SchNet**) used hand-designed descriptors; modern **equivariant graph neural
networks (NequIP, Allegro, MACE)** and foundation potentials trained on huge
datasets generalise across chemistries. Training minimises a combined
energy-plus-force loss:

$$\mathcal{L} = \sum \big(E_{\text{pred}}-E_{\text{DFT}}\big)^2 + \gamma \sum \big\|\mathbf{F}_{\text{pred}}-\mathbf{F}_{\text{DFT}}\big\|^2.$$

MLIPs now run reactive MD (bond breaking) that classical fields cannot, and
**active learning** adds new DFT points where the model is uncertain.

Validation loss falls steeply as training data grows, approaching DFT-level
error:

```plot
{"title": "MLIP error vs training set size", "xLabel": "training configurations (x1000)", "yLabel": "force error (relative)", "xRange": [0.2, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "4/sqrt(x)", "label": "error ~ 1/sqrt(N)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  DFT["DFT energies & forces"] --> TRAIN["Train equivariant GNN (MACE/NequIP)"]
  TRAIN --> POT["ML potential"]
  POT --> MD["Run reactive MD at low cost"]
  MD --> UNC["Uncertain? -> active learning"]
  UNC --> DFT
```

**Next:** quantum effects with ab initio and QM/MM dynamics.
""",
        ),
        _t(
            "Ab initio & QM/MM molecular dynamics",
            "11 min",
            r"""
# Ab initio & QM/MM molecular dynamics

When chemistry changes — bonds break, charges transfer, electrons matter —
classical force fields fail. **Ab initio MD (AIMD)** computes forces directly
from electronic structure each step. **Born–Oppenheimer MD** solves the
electronic problem to self-consistency before moving the nuclei;
**Car–Parrinello MD** instead propagates fictitious electronic degrees of freedom
alongside the nuclei to avoid the full SCF each step. AIMD is accurate but limited
to small systems and short times.

**QM/MM** combines both worlds: a small **quantum region** (an enzyme active site,
a reacting solute) is treated with DFT or a wavefunction method, while the
surrounding protein and solvent use a classical force field. The coupling handles
electrostatics across the boundary and "link atoms" cap cut bonds. QM/MM is the
standard for **enzyme reaction mechanisms** and is often paired with umbrella
sampling to get reaction free-energy barriers.

Accuracy and cost rise together with the size of the quantum region — the central
QM/MM trade-off:

```plot
{"title": "QM/MM cost vs quantum-region size", "xLabel": "QM atoms (x10)", "yLabel": "relative cost", "xRange": [1, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "0.1*x^3", "label": "QM cost scales steeply", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  SYS["Full system"] --> QM["QM region: DFT (active site)"]
  SYS --> MM["MM region: force field"]
  QM --> CPL["Coupling + link atoms"]
  MM --> CPL
  CPL --> RXN["Reaction mechanism & barrier"]
```

**Next:** check your mastery of advanced MD methods.
""",
        ),
        _quiz(),
    ),
)


MOLECULAR_DYNAMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MOLECULAR_DYNAMICS_COURSES"]
