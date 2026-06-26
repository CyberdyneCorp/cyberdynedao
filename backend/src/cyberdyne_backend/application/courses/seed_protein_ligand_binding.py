"""Protein-Ligand Binding & Free-Energy Methods track: Basics -> Intermediate -> Advanced.

A three-level track on the thermodynamics and computation of binding affinity.
Basics builds intuition for binding equilibria, Kd/Ki and the molecular forces;
Intermediate covers scoring functions, end-point methods (MM/PBSA, MM/GBSA) and
the statistical mechanics of binding; Advanced treats alchemical free-energy
perturbation (FEP/TI), enhanced sampling and machine-learning affinity prediction.
Lessons are `text` with LaTeX, interactive ```plot blocks (binding isotherms,
free-energy cycles, convergence) and ```mermaid pipeline/cycle diagrams.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Protein-Ligand Binding — Basics ───────────────────────────────────────────

_BASICS = SeedCourse(
    slug="protein-ligand-binding-basics",
    title="Protein-Ligand Binding & Free-Energy Methods — Basics",
    description=(
        "An intuitive introduction to how small molecules bind proteins and how "
        "we quantify that binding. Covers the binding equilibrium and the "
        "dissociation constant Kd, the link between affinity and free energy, "
        "the enthalpy-entropy decomposition, the molecular forces that drive "
        "recognition, the induced-fit and conformational-selection models, and "
        "how affinity is measured experimentally. Interactive binding isotherms "
        "and process diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The binding equilibrium and Kd",
            "10 min",
            r"""
# The binding equilibrium and Kd

Drug action almost always begins with a reversible association between a protein
**receptor** $R$ and a small-molecule **ligand** $L$:

$$R + L \rightleftharpoons RL$$

At equilibrium the **dissociation constant** measures how readily the complex
falls apart:

$$K_d = \frac{[R][L]}{[RL]} = \frac{k_{off}}{k_{on}}$$

A *small* $K_d$ means a *tight* binder. $K_d$ has units of concentration, and a
useful intuition is that it equals the free-ligand concentration at which the
receptor is **half-occupied**. The fractional occupancy follows the Langmuir
isotherm:

$$\theta = \frac{[L]}{K_d + [L]}$$

```plot
{"title": "Fractional occupancy vs free ligand (Kd = 1)", "xLabel": "[L] / Kd", "yLabel": "occupancy θ", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+1)", "label": "θ = [L]/([L]+Kd)", "color": "#2563eb"}]}
```

Typical drug affinities span $K_d \approx 10^{-6}$ M (micromolar, weak) down to
$10^{-9}$ M (nanomolar, strong) and beyond. Enzyme inhibitors are often reported
as $K_i$, the same idea for an inhibitor competing with substrate.

**Next:** turning Kd into a binding free energy.
""",
        ),
        _t(
            "From affinity to free energy",
            "11 min",
            r"""
# From affinity to free energy

Affinity is just a free energy in disguise. The standard binding free energy is

$$\Delta G^{\circ} = -RT \ln K_a = RT \ln K_d$$

where $K_a = 1/K_d$ is the association constant, $R = 8.314$ J/(mol·K) and $T$ is
absolute temperature. A more negative $\Delta G^{\circ}$ means tighter binding.

At $T = 298$ K, $RT \approx 0.593$ kcal/mol, so every factor-of-ten improvement
in $K_d$ buys only about $1.36$ kcal/mol of binding free energy. That logarithmic
relationship is why moving from micromolar to nanomolar (a 1000-fold gain) costs
roughly $4$ kcal/mol — a small energy that medicinal chemists fight hard for.

```plot
{"title": "Binding free energy vs affinity", "xLabel": "−log10(Kd)  (pKd)", "yLabel": "−ΔG° (kcal/mol)", "xRange": [3, 12], "yRange": [0, 18], "grid": true, "functions": [{"expr": "1.364*x", "label": "−ΔG° = 1.364·pKd", "color": "#16a34a"}]}
```

The key takeaway: affinity differences we care about are tiny on the scale of a
molecule's total energy. Predicting binding *in silico* therefore demands methods
accurate to about $1$ kcal/mol — the famous "chemical accuracy" target.

**Next:** splitting free energy into enthalpy and entropy.
""",
        ),
        _t(
            "Enthalpy, entropy and the binding signature",
            "11 min",
            r"""
# Enthalpy, entropy and the binding signature

The binding free energy decomposes into enthalpic and entropic parts:

$$\Delta G = \Delta H - T\Delta S$$

**Enthalpy** ($\Delta H$) reflects the strength of the new interactions formed —
hydrogen bonds, salt bridges, van der Waals contacts. **Entropy** ($\Delta S$)
captures changes in disorder: the ligand and protein lose translational and
rotational freedom (unfavourable), but releasing ordered water from the binding
site into bulk solvent is strongly favourable (the **hydrophobic effect**).

Two ligands can reach the *same* $\Delta G$ by very different routes — one
enthalpy-driven, one entropy-driven. This "thermodynamic signature", measured by
**isothermal titration calorimetry (ITC)**, guides optimisation: enthalpic
binders are often considered higher quality because specific polar contacts are
harder to achieve than burying greasy surface.

```mermaid
flowchart LR
  G["ΔG (affinity)"] --> H["ΔH: H-bonds, salt bridges, vdW"]
  G --> S["−TΔS"]
  S --> S1["loss of ligand/protein motion (unfavourable)"]
  S --> S2["water release / hydrophobic effect (favourable)"]
```

Beware **enthalpy-entropy compensation**: tightening a contact often rigidifies
the complex, paying back in lost entropy, so $\Delta G$ moves less than $\Delta H$.

**Next:** the molecular forces behind recognition.
""",
        ),
        _t(
            "Molecular forces in recognition",
            "10 min",
            r"""
# Molecular forces in recognition

Binding is the sum of many weak, non-covalent interactions acting over the
contact surface. The main contributors are:

- **Hydrogen bonds** (~1–5 kcal/mol each) between donors (N–H, O–H) and
  acceptors (O, N); directional and central to specificity.
- **Electrostatic / salt bridges** between charged groups (e.g. a ligand
  carboxylate and a protein arginine); strong but screened by water.
- **Van der Waals** contacts — weak per atom but numerous; shape complementarity
  ("lock and key") maximises them.
- **The hydrophobic effect** — burying nonpolar surface to release structured
  water; the dominant driver for many drugs.

The Lennard-Jones potential captures the vdW balance of attraction and repulsion:

$$V_{LJ}(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right]$$

```plot
{"title": "Lennard-Jones potential (ε=1, σ=1)", "xLabel": "distance r/σ", "yLabel": "V (units of ε)", "xRange": [0.9, 2.5], "yRange": [-1.2, 2], "grid": true, "functions": [{"expr": "4*((1/x)^12 - (1/x)^6)", "label": "V_LJ(r)", "color": "#dc2626"}]}
```

The minimum sits near $r \approx 1.12\,\sigma$, the ideal contact distance; closer
contacts clash sterically, farther ones lose attraction.

**Next:** how proteins move to accommodate ligands.
""",
        ),
        _t(
            "Induced fit and conformational selection",
            "10 min",
            r"""
# Induced fit and conformational selection

The rigid "lock and key" picture is incomplete: proteins are flexible. Two
limiting models describe how a complex forms.

In **induced fit**, the ligand binds a dominant protein conformation and *then*
the protein reshapes its pocket to optimise contacts. In **conformational
selection**, the protein already samples a rare binding-competent conformation in
its ensemble, and the ligand simply *selects* and stabilises it, shifting the
equilibrium toward that state. Real systems usually mix both.

```mermaid
flowchart LR
  subgraph Induced fit
    A["R (open) + L"] --> B["R·L loose"] --> C["R·L optimised"]
  end
  subgraph Conformational selection
    D["R (open) ⇌ R* (closed, rare)"] --> E["R* + L → R*·L"]
  end
```

This matters computationally: a single static crystal structure may not show the
conformation a given ligand prefers. Flexible-receptor docking, ensemble docking
and molecular dynamics all try to capture protein motion. It also explains why
**cryptic pockets** — invisible in the apo structure — can open transiently and
be drugged.

**Next:** how affinity is measured in the lab.
""",
        ),
        _t(
            "Measuring affinity experimentally",
            "10 min",
            r"""
# Measuring affinity experimentally

Computed affinities are only useful if validated against experiment. The main
biophysical methods report complementary quantities:

- **Isothermal titration calorimetry (ITC)** measures heat released on
  titration, giving $K_d$, $\Delta H$ and stoichiometry in one experiment — the
  gold standard for the full thermodynamic signature.
- **Surface plasmon resonance (SPR)** measures association/dissociation in real
  time, yielding $k_{on}$, $k_{off}$ and thus kinetics plus $K_d$.
- **Fluorescence / FRET** and **microscale thermophoresis (MST)** track binding
  through optical signal changes versus concentration.
- **Enzyme inhibition assays** give $IC_{50}$, converted to $K_i$ via the
  Cheng-Prusoff relation $K_i = IC_{50}/(1 + [S]/K_m)$.

A binding curve from any of these fits the same saturating isotherm:

```plot
{"title": "Saturable binding curve (signal vs ligand)", "xLabel": "ligand concentration (arb.)", "yLabel": "fractional signal", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x/(x+2)", "label": "signal = [L]/([L]+Kd)", "color": "#2563eb"}]}
```

Kinetics matter beyond $K_d$: a long **residence time** ($1/k_{off}$) can give
sustained efficacy even when equilibrium affinity is modest.

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


# ── Protein-Ligand Binding — Intermediate ─────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="protein-ligand-binding-intermediate",
    title="Protein-Ligand Binding & Free-Energy Methods — Intermediate",
    description=(
        "The core quantitative methods for predicting binding affinity. Covers "
        "the statistical-mechanics definition of the binding constant, "
        "molecular-mechanics force fields, docking scoring functions and their "
        "limits, implicit-solvent end-point methods (MM/PBSA and MM/GBSA), "
        "entropy estimation, and how the thermodynamic cycle frames every "
        "free-energy calculation. Interactive plots of energy terms, "
        "convergence and solvation, plus method pipelines."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Statistical mechanics of binding",
            "12 min",
            r"""
# Statistical mechanics of binding

Underneath $K_d$ lies statistical mechanics. The binding constant is a ratio of
configurational integrals over the bound and unbound states. Equivalently, the
binding free energy is a difference in the **potential of mean force** between
the complex and the separated partners, integrated over all configurations:

$$\Delta G_{bind} = -RT \ln\!\left(\frac{Z_{RL}}{Z_R\,Z_L}\,\frac{1}{C^{\circ}V}\right)$$

where the $Z$ are configuration integrals and $C^{\circ}$ is the $1$ M standard
state. The crucial point: $\Delta G$ depends on the **free energy** of each
ensemble, not a single minimum-energy pose. Enthalpic depth can be offset by a
narrow, entropically poor well.

```mermaid
flowchart LR
  E["Ensemble of R, L, RL states"] --> B["Boltzmann weights exp(−E/kT)"]
  B --> P["Partition functions Z_R, Z_L, Z_RL"]
  P --> G["ΔG = −RT ln(Z_RL/(Z_R Z_L)) + standard-state term"]
```

The Boltzmann factor governs how states are populated, so high-energy poses still
contribute if they are numerous:

```plot
{"title": "Boltzmann weight vs energy (kT = 1)", "xLabel": "energy above minimum (kT)", "yLabel": "relative population", "xRange": [0, 8], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "exp(−E/kT)", "color": "#2563eb"}]}
```

This ensemble view is why rigorous methods sample many configurations rather than
scoring one pose.

**Next:** the force fields that score those configurations.
""",
        ),
        _t(
            "Molecular mechanics force fields",
            "11 min",
            r"""
# Molecular mechanics force fields

Sampling millions of configurations demands a fast energy function. **Molecular
mechanics (MM)** force fields model atoms as balls and bonds as springs, summing
bonded and non-bonded terms:

$$U = \sum_{bonds} k_b (r-r_0)^2 + \sum_{angles} k_\theta(\theta-\theta_0)^2 + \sum_{dih} V_n[1+\cos(n\phi-\gamma)] + \sum_{i<j}\left[\frac{q_iq_j}{4\pi\varepsilon_0 r_{ij}} + 4\varepsilon_{ij}\!\left(\frac{\sigma^{12}}{r^{12}}-\frac{\sigma^{6}}{r^{6}}\right)\right]$$

Common protein force fields include **AMBER (ff14SB, ff19SB)**, **CHARMM36** and
**OPLS**; ligands are parameterised with **GAFF** or **CGenFF**. The non-bonded
electrostatic and van der Waals terms dominate protein-ligand interaction energy.

```plot
{"title": "Harmonic bond-stretch energy", "xLabel": "displacement r − r0 (Å)", "yLabel": "energy (kcal/mol)", "xRange": [-0.5, 0.5], "yRange": [0, 25], "grid": true, "functions": [{"expr": "100*x^2", "label": "U = k(r−r0)²", "color": "#16a34a"}]}
```

Classical force fields are fast but approximate: fixed partial charges miss
**polarisation**, and they cannot break bonds. Polarisable force fields (AMOEBA)
and ML potentials address this at higher cost.

**Next:** docking scoring functions.
""",
        ),
        _t(
            "Scoring functions and their limits",
            "11 min",
            r"""
# Scoring functions and their limits

Docking poses a ligand in the pocket and ranks poses with a fast **scoring
function**. Three families dominate:

- **Force-field based** — sum MM van der Waals and electrostatic terms (e.g.
  DOCK, GOLD's GoldScore).
- **Empirical** — weighted sums of physically motivated terms (H-bonds,
  hydrophobic contacts, rotatable-bond penalty) fitted to known affinities
  (e.g. ChemScore, Glide SP/XP).
- **Knowledge-based** — statistical potentials from observed contact frequencies
  in the PDB (e.g. DrugScore, PMF).

```mermaid
flowchart LR
  P["Ligand pose"] --> FF["Force-field score"]
  P --> EMP["Empirical score (fitted terms)"]
  P --> KB["Knowledge-based potential"]
  FF --> R["Rank / select pose"]
  EMP --> R
  KB --> R
```

Scoring functions are good at **pose prediction** but notoriously weak at
**affinity ranking**: they neglect entropy, treat solvent crudely and use a
single conformation. Correlation with experiment is often modest. This gap
motivates rescoring with end-point methods (MM/PBSA) and the rigorous free-energy
methods of the Advanced course.

```plot
{"title": "Idealised score vs measured affinity (weak correlation)", "xLabel": "docking score (arb.)", "yLabel": "measured pKd", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.5*x + 2", "label": "noisy trend", "color": "#dc2626"}]}
```

**Next:** end-point methods that add solvent physics.
""",
        ),
        _t(
            "MM/PBSA and MM/GBSA end-point methods",
            "12 min",
            r"""
# MM/PBSA and MM/GBSA end-point methods

End-point methods estimate $\Delta G_{bind}$ from simulations of only the two end
states (complex and free partners), without an alchemical path. The free energy
of each state combines gas-phase MM energy, a solvation free energy, and an
entropy term:

$$\Delta G_{bind} = \Delta E_{MM} + \Delta G_{solv} - T\Delta S$$

In **MM/PBSA** the polar solvation is the **Poisson-Boltzmann** electrostatic
free energy; in **MM/GBSA** it is the faster **Generalized Born** approximation.
A nonpolar term, proportional to buried surface area, captures the hydrophobic
contribution:

```mermaid
flowchart LR
  MD["MD trajectory of complex"] --> S["Extract snapshots"]
  S --> MM["Gas-phase MM energy ΔE_MM"]
  S --> PB["Polar solvation (PB or GB)"]
  S --> NP["Nonpolar term γ·SASA"]
  MM --> SUM["ΔG_bind = ΔE_MM + ΔG_solv − TΔS"]
  PB --> SUM
  NP --> SUM
```

The nonpolar term scales with the solvent-accessible surface area buried on
binding:

```plot
{"title": "Nonpolar solvation vs buried surface area", "xLabel": "buried SASA (100 Å²)", "yLabel": "−ΔG_nonpolar (kcal/mol)", "xRange": [0, 10], "yRange": [0, 8], "grid": true, "functions": [{"expr": "0.72*x", "label": "γ·ΔSASA (γ≈0.0072)", "color": "#16a34a"}]}
```

MM/GBSA is cheaper and widely used for **relative** ranking of congeneric series,
but absolute accuracy is limited and results are sensitive to the dielectric
constant and entropy treatment.

**Next:** estimating the entropy term.
""",
        ),
        _t(
            "Entropy estimation in binding",
            "10 min",
            r"""
# Entropy estimation in binding

Entropy is the hardest term to compute, yet often decisive. Binding loses
**translational and rotational** entropy of the ligand (a roughly fixed cost of
several kcal/mol at room temperature) and **conformational** entropy as flexible
groups become rigid, while gaining **solvent** entropy from released water.

Two classical estimators of the configurational (vibrational) entropy from an MD
trajectory are:

- **Normal-mode analysis (NMA)** — diagonalise the mass-weighted Hessian and sum
  harmonic-oscillator entropies of each mode; expensive and noisy.
- **Quasi-harmonic analysis** — build the covariance matrix of atomic
  fluctuations and treat its eigenvalues as effective modes.

For a single harmonic mode of frequency $\nu$, the entropy rises as the mode
softens (lower frequency, larger amplitude):

```plot
{"title": "Harmonic-oscillator entropy vs mode 'looseness'", "xLabel": "amplitude (arb.)", "yLabel": "vibrational entropy (arb.)", "xRange": [0.2, 6], "yRange": [0, 4], "grid": true, "functions": [{"expr": "log(1+x)", "label": "S ∝ ln(amplitude)", "color": "#2563eb"}]}
```

Because entropy estimates are noisy, many practitioners drop $-T\Delta S$ in
MM/GBSA when ranking similar ligands, assuming it largely cancels — a shortcut
that fails when ligands differ in flexibility.

**Next:** the thermodynamic cycle that frames free-energy methods.
""",
        ),
        _t(
            "The thermodynamic cycle",
            "11 min",
            r"""
# The thermodynamic cycle

Free energy is a **state function**: its change depends only on the end states,
not the path taken. This lets us replace a hard physical process (a ligand
leaving solvent and entering the pocket) with a convenient, possibly
*unphysical*, computational path that has the same endpoints.

The canonical **relative binding free-energy** cycle compares two ligands, A and
B, binding the same protein:

```mermaid
flowchart LR
  AB["A bound  --ΔG_bind(A)-->  A free"]
  L1["ΔΔG = ΔG_bind(B) − ΔG_bind(A)"]
  C1["A bound  --ΔG_mut,complex-->  B bound"]
  C2["A free   --ΔG_mut,solv-->     B free"]
  C1 --> R["ΔΔG = ΔG_mut,complex − ΔG_mut,solv"]
  C2 --> R
```

Because the cycle closes, the experimentally relevant difference equals the
difference of two *alchemical* "mutations" of A into B — one in the complex, one
in solvent. Each leg is computed by gradually transforming A into B and
integrating the free-energy change, which is far easier than the absolute
binding event.

This single idea — close the loop, compute the easy legs — underlies FEP,
thermodynamic integration and all the rigorous methods in the Advanced course.

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


# ── Protein-Ligand Binding — Advanced ─────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="protein-ligand-binding-advanced",
    title="Protein-Ligand Binding & Free-Energy Methods — Advanced",
    description=(
        "State-of-the-art rigorous affinity prediction. Covers alchemical free-"
        "energy perturbation (FEP) and the Zwanzig equation, thermodynamic "
        "integration, optimal estimators (BAR/MBAR), absolute binding free "
        "energy with restraints, enhanced sampling (replica exchange, "
        "metadynamics), and machine-learning approaches to scoring and free "
        "energy. Interactive plots of dV/dλ, overlap and convergence, plus "
        "workflow diagrams for production FEP campaigns."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Free-energy perturbation (FEP)",
            "12 min",
            r"""
# Free-energy perturbation (FEP)

FEP computes the free-energy difference between two states (e.g. ligand A and
ligand B) coupled by a parameter $\lambda$ that morphs one Hamiltonian into the
other, $H(\lambda) = (1-\lambda)H_A + \lambda H_B$. The **Zwanzig equation**
gives the exact relation between adjacent states:

$$\Delta G_{A\to B} = -RT \ln \left\langle \exp\!\left(-\frac{H_B - H_A}{RT}\right)\right\rangle_A$$

The average is over configurations sampled from state $A$. This is exact only if
the two states **overlap** in phase space; if B's important configurations are
rarely visited by A, the exponential average is dominated by a few snapshots and
the estimate is biased. The fix is **windows**: insert intermediate $\lambda$
values so neighbours overlap, then sum the steps.

```mermaid
flowchart LR
  A["λ=0 (ligand A)"] --> W1["λ=0.25"] --> W2["λ=0.5"] --> W3["λ=0.75"] --> B["λ=1 (ligand B)"]
  B --> SUM["ΔG = Σ ΔG(λ_i → λ_{i+1})"]
```

Good overlap means the energy-difference distributions of neighbouring windows
share substantial area:

```plot
{"title": "Overlap of neighbouring λ-window energy distributions", "xLabel": "ΔU (kT)", "yLabel": "probability", "xRange": [-6, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-(x+1)*(x+1)/2)", "label": "window i", "color": "#2563eb"}, {"expr": "exp(-(x-1)*(x-1)/2)", "label": "window i+1", "color": "#dc2626"}]}
```

Modern FEP+ (Schrödinger) and open tools (GROMACS, OpenFE) reach ~1 kcal/mol RMSE
on congeneric series — true predictive power.

**Next:** the continuous-path alternative, thermodynamic integration.
""",
        ),
        _t(
            "Thermodynamic integration",
            "11 min",
            r"""
# Thermodynamic integration

Thermodynamic integration (TI) takes the same $\lambda$ path but integrates the
*derivative* of the free energy rather than exponential averages:

$$\Delta G = \int_0^1 \left\langle \frac{\partial H}{\partial \lambda} \right\rangle_\lambda \, d\lambda$$

At each $\lambda$ window we run a simulation and average $\partial H/\partial
\lambda$; the curve is then numerically integrated (trapezoidal or Gaussian
quadrature). TI is conceptually simple and the integrand is well-behaved, but
needs enough windows to resolve curvature, especially where the integrand spikes
near the endpoints when atoms appear or vanish.

```plot
{"title": "Typical ⟨∂H/∂λ⟩ integrand over the λ path", "xLabel": "λ", "yLabel": "⟨∂H/∂λ⟩ (kcal/mol)", "xRange": [0, 1], "yRange": [-2, 6], "grid": true, "functions": [{"expr": "5*exp(-8*x) - 1", "label": "integrand vs λ", "color": "#16a34a"}]}
```

The endpoint singularity — a vanishing atom's Lennard-Jones term blowing up — is
tamed by **soft-core potentials** that smoothly remove interactions:

```mermaid
flowchart LR
  L0["λ=0 full interaction"] --> SC["soft-core scaling of LJ & Coulomb"] --> L1["λ=1 decoupled atom"]
```

TI and FEP are two views of the same path; the choice of *estimator* (next
lesson) often matters more than TI-vs-FEP.

**Next:** optimal estimators — BAR and MBAR.
""",
        ),
        _t(
            "BAR, MBAR and convergence",
            "11 min",
            r"""
# BAR, MBAR and convergence

Raw Zwanzig averaging wastes data because it uses only forward (or only
backward) sampling. The **Bennett Acceptance Ratio (BAR)** combines forward and
reverse work between two states to give the minimum-variance estimate, solving a
self-consistent equation for $\Delta G$. **MBAR** (multistate BAR) generalises
this to *all* windows simultaneously, extracting the most information from the
full dataset and providing rigorous error bars.

```mermaid
flowchart LR
  F["Forward samples (i→i+1)"] --> BAR["BAR / MBAR self-consistent solve"]
  R["Reverse samples (i+1→i)"] --> BAR
  BAR --> G["ΔG + statistical uncertainty"]
```

Convergence must be checked, not assumed. The statistical error of a free-energy
estimate falls roughly as $1/\sqrt{N}$ with the number of **uncorrelated**
samples, so doubling accuracy costs four times the simulation:

```plot
{"title": "Free-energy error vs sampling time", "xLabel": "simulation length (ns)", "yLabel": "error (kcal/mol)", "xRange": [1, 50], "yRange": [0, 2], "grid": true, "functions": [{"expr": "2/sqrt(x)", "label": "error ∝ 1/√N", "color": "#dc2626"}]}
```

Diagnostics include the BAR/MBAR **overlap matrix**, hysteresis between forward
and reverse estimates, and block-averaging of $\partial H/\partial\lambda$. Poor
overlap signals that more windows or longer sampling are needed.

**Next:** computing absolute binding free energies.
""",
        ),
        _t(
            "Absolute binding free energy with restraints",
            "12 min",
            r"""
# Absolute binding free energy with restraints

Relative FEP compares two ligands; **absolute binding free energy (ABFE)**
computes $\Delta G_{bind}$ for one ligand directly by alchemically **decoupling**
it from the protein and from solvent, then taking the difference via a
thermodynamic cycle.

The problem: as the ligand's interactions vanish, it wanders out of the pocket,
making the integral diverge and sampling impossible. The solution is the
**double-decoupling method (DDM)** with **Boresch restraints** — a set of
distance, angle and dihedral restraints that hold the decoupling ligand in place.
The known analytical free energy of those restraints is then subtracted:

$$\Delta G_{bind} = -\big(\Delta G_{decouple}^{site} - \Delta G_{decouple}^{bulk} + \Delta G_{restraint}\big)$$

```mermaid
flowchart LR
  B["Ligand bound (restrained)"] --> D1["Decouple in site"]
  D1 --> G1["Ligand off, restraints on"]
  G1 --> RR["Release restraints (analytic)"]
  F["Ligand in bulk"] --> D2["Decouple in solvent"]
  RR --> CYC["Cycle: ΔG_bind"]
  D2 --> CYC
```

The standard-state correction ties the result to $1$ M, and restraint strength
must be chosen so the bound ensemble is well sampled yet the analytic correction
stays valid:

```plot
{"title": "Restraint free-energy correction vs restraint strength", "xLabel": "force constant (arb.)", "yLabel": "ΔG_restraint (kcal/mol)", "xRange": [0.5, 20], "yRange": [0, 8], "grid": true, "functions": [{"expr": "1.5*log(x)+1", "label": "ΔG_restraint ∝ ln(k)", "color": "#16a34a"}]}
```

ABFE handles diverse, non-congeneric ligands and even fragments, at higher cost
and care than relative FEP.

**Next:** enhanced sampling for slow degrees of freedom.
""",
        ),
        _t(
            "Enhanced sampling methods",
            "11 min",
            r"""
# Enhanced sampling methods

Free-energy estimates are only as good as the sampling. Slow motions — sidechain
flips, loop closures, ligand reorientation, water exchange — can be missed in
nanosecond simulations, biasing results. Enhanced-sampling methods accelerate
barrier crossing.

- **Replica exchange (REMD / parallel tempering)** runs copies at different
  temperatures (or $\lambda$ values, "Hamiltonian REMD") and periodically swaps
  them, letting high-temperature replicas cross barriers that low ones cannot.
- **Metadynamics** deposits a history-dependent Gaussian bias along chosen
  **collective variables**, filling free-energy wells so the system escapes and
  the bias reconstructs the free-energy surface.
- **Umbrella sampling** restrains a CV to overlapping windows and recombines them
  with WHAM to recover the potential of mean force.

```mermaid
flowchart LR
  CV["Choose collective variable(s)"] --> M["Add bias (metadynamics) or windows (umbrella)"]
  M --> S["Enhanced barrier crossing"]
  S --> PMF["Reconstruct free-energy surface / PMF"]
```

Metadynamics progressively flattens the underlying free-energy landscape as bias
accumulates:

```plot
{"title": "Underlying free-energy surface along a collective variable", "xLabel": "collective variable", "yLabel": "free energy (kcal/mol)", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "3*(1+cos(x))*exp(-0.15*x)+0.5", "label": "double-well FES", "color": "#2563eb"}]}
```

Combining enhanced sampling with alchemy (e.g. $\lambda$-REMD FEP) is now routine
for difficult targets.

**Next:** machine learning for affinity prediction.
""",
        ),
        _t(
            "Machine learning for affinity prediction",
            "12 min",
            r"""
# Machine learning for affinity prediction

Physics-based FEP is accurate but expensive. Machine learning aims for similar
accuracy at a fraction of the cost, and to fix the weak link in docking —
scoring.

- **ML scoring functions** (RF-Score, $K_{DEEP}$, OnionNet, Pafnucy) learn the
  score-affinity map from PDBbind structures using random forests or 3D CNNs over
  voxelised pockets.
- **Graph neural networks** treat the complex as a graph of atoms and contacts,
  learning interaction features directly (e.g. interaction GNNs, equivariant
  models).
- **ML potentials / hybrid ML/MM** (ANI, NequIP, MACE) approach quantum accuracy
  for the ligand inside FEP, correcting force-field errors.
- **Active learning** couples cheap ML predictions with selective FEP on the most
  informative candidates to triage huge libraries.

```mermaid
flowchart LR
  D["PDBbind / experimental affinities"] --> F["Featurise: voxels, graphs, descriptors"]
  F --> M["Train CNN / GNN / RF model"]
  M --> P["Predict affinity"]
  P --> AL["Active learning → select for FEP / assay"]
  AL --> D
```

The central caveat is **generalisation**: models can memorise the protein or
ligand rather than the *interaction*, inflating benchmark scores. Honest
evaluation needs scaffold- and target-split test sets, and ML predictions are
best used to *prioritise* compounds for rigorous FEP or experiment, not to
replace them outright. Learning curves typically show error falling and plateauing
as training data grows:

```plot
{"title": "ML model error vs training-set size", "xLabel": "training examples (×1000)", "yLabel": "test RMSE (kcal/mol)", "xRange": [1, 30], "yRange": [0.5, 3], "grid": true, "functions": [{"expr": "0.8 + 4/sqrt(x)", "label": "RMSE vs data", "color": "#dc2626"}]}
```

**Next:** check what you have learned.
""",
        ),
        _quiz(),
    ),
)


PROTEIN_LIGAND_BINDING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PROTEIN_LIGAND_BINDING_COURSES"]
