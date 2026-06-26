"""Physical Chemistry & Thermodynamics track: Basics -> Intermediate -> Advanced.

A three-level chemistry track spanning energy, enthalpy and entropy through the
laws of thermodynamics; chemical kinetics and equilibria; and on to quantum
chemistry and spectroscopy underlying molecular modeling. Lessons are `text`
with LaTeX, interactive ```plot blocks (rate laws, Boltzmann/Arrhenius, free
energy, spectra) and ```mermaid diagrams for cycles, pathways and pipelines.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Physical Chemistry & Thermodynamics — Basics ─────────────────────────────

_BASICS = SeedCourse(
    slug="physical-chemistry-basics",
    title="Physical Chemistry & Thermodynamics — Basics",
    description=(
        "The conceptual foundations of physical chemistry: the system/surroundings "
        "picture, internal energy and the first law, enthalpy and thermochemistry, "
        "entropy and the second law, and the Gibbs free energy that decides whether "
        "a reaction is spontaneous. Built around intuition with interactive plots "
        "and process diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Systems, state functions & the first law",
            "11 min",
            r"""
# Systems, state functions & the first law

Physical chemistry begins by drawing a boundary. Everything inside is the
**system**; everything outside is the **surroundings**. Energy crosses the
boundary in two ways: as **heat** $q$ (driven by a temperature difference) and
as **work** $w$ (e.g. a gas pushing a piston). The **first law of
thermodynamics** is just conservation of energy applied to that boundary:

$$\Delta U = q + w,$$

where $U$ is the **internal energy** — the total kinetic and potential energy of
all the molecules. $U$ is a **state function**: it depends only on the current
state (temperature, pressure, composition), not the path taken to reach it. Heat
and work are *path* quantities — different routes between the same two states can
exchange different $q$ and $w$, but their sum $\Delta U$ is fixed.

For an ideal gas, $U$ depends only on temperature, so internal energy rises
linearly with $T$ (slope set by the heat capacity):

```plot
{"title": "Internal energy of an ideal gas vs temperature", "xLabel": "temperature T (relative)", "yLabel": "internal energy U (relative)", "xRange": [0, 10], "yRange": [0, 15], "grid": true, "functions": [{"expr": "1.5*x", "label": "U = (3/2) n R T (monatomic)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  SUR["Surroundings"] -->|"heat q"| SYS["System (internal energy U)"]
  SUR -->|"work w"| SYS
  SYS -->|"ΔU = q + w"| STATE["New state"]
```

**Next:** counting energy that goes into volume work — enthalpy.
""",
        ),
        _t(
            "Enthalpy & thermochemistry",
            "11 min",
            r"""
# Enthalpy & thermochemistry

Most chemistry happens in open beakers at constant **pressure**, where a
reacting system can expand or contract against the atmosphere. To account for
that expansion work automatically we define **enthalpy**:

$$H = U + pV.$$

At constant pressure the heat released or absorbed equals the enthalpy change:
$q_p = \Delta H$. A reaction with $\Delta H < 0$ is **exothermic** (releases
heat); $\Delta H > 0$ is **endothermic**.

Because $H$ is a state function, **Hess's law** lets us add reaction enthalpies
along any convenient route. Using **standard enthalpies of formation**
$\Delta_f H^\circ$:

$$\Delta_r H^\circ = \sum \nu\,\Delta_f H^\circ(\text{products}) - \sum \nu\,\Delta_f H^\circ(\text{reactants}).$$

The heat actually measured tracks how far the reaction has proceeded (the extent
of reaction). For an exothermic reaction, accumulated heat released grows toward
a plateau as reactants run out:

```plot
{"title": "Cumulative heat released vs extent of reaction", "xLabel": "extent of reaction", "yLabel": "heat released (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "q_p approaches |ΔH|", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  R["Reactants"] -->|"ΔH1 (route A)"| I["Intermediate"]
  I -->|"ΔH2"| P["Products"]
  R -->|"ΔH (route B, direct)"| P
  P -.->|"Hess: ΔH = ΔH1 + ΔH2"| R
```

**Next:** why heat alone does not predict spontaneity — entropy.
""",
        ),
        _t(
            "Entropy & the second law",
            "12 min",
            r"""
# Entropy & the second law

Some processes happen on their own (gases mix, hot bodies cool) and never
reverse spontaneously, even though energy is conserved either way. The missing
ingredient is **entropy** $S$, a measure of how many microscopic arrangements
(microstates $W$) are consistent with the macroscopic state. Boltzmann's
equation makes this precise:

$$S = k_B \ln W,$$

with $k_B$ the Boltzmann constant. More accessible microstates means higher
entropy. The **second law of thermodynamics** states that for an isolated
system the total entropy never decreases:

$$\Delta S_{\text{universe}} = \Delta S_{\text{sys}} + \Delta S_{\text{surr}} \ge 0.$$

Entropy rises sharply when few microstates are available and flattens as $W$
grows — its logarithmic shape:

```plot
{"title": "Boltzmann entropy S = k ln W (k set to 1)", "xLabel": "number of microstates W", "yLabel": "entropy S (relative)", "xRange": [1, 10], "yRange": [0, 3], "grid": true, "functions": [{"expr": "log(x)", "label": "S = k ln W", "color": "#16a34a"}]}
```

Heat flowing into the surroundings raises *their* entropy by
$\Delta S_{\text{surr}} = -\Delta H_{\text{sys}}/T$ — which is why exothermic
reactions are often (but not always) spontaneous.

```mermaid
flowchart LR
  A["Ordered state (few microstates, low S)"] -->|"spontaneous"| B["Disordered state (many microstates, high S)"]
  B -.->|"never spontaneous in isolation"| A
```

**Next:** combining enthalpy and entropy into one criterion — Gibbs energy.
""",
        ),
        _t(
            "Gibbs free energy & spontaneity",
            "12 min",
            r"""
# Gibbs free energy & spontaneity

At constant temperature and pressure we want a single property of the *system*
that tells us whether a change is spontaneous, without bookkeeping the
surroundings. That property is the **Gibbs free energy**:

$$G = H - TS, \qquad \Delta G = \Delta H - T\,\Delta S.$$

The criterion is simple: a process at constant $T,p$ is spontaneous when
$\Delta G < 0$, at equilibrium when $\Delta G = 0$, and non-spontaneous when
$\Delta G > 0$. The $-T\Delta S$ term is why temperature can flip spontaneity:
an endothermic reaction with $\Delta S > 0$ becomes spontaneous above the
crossover temperature $T = \Delta H/\Delta S$.

Plotting $\Delta G$ versus temperature for $\Delta H>0,\ \Delta S>0$ shows the
line crossing zero — below it the reaction is forbidden, above it allowed:

```plot
{"title": "ΔG = ΔH − TΔS vs temperature (ΔH=6, ΔS=1)", "xLabel": "temperature T (relative)", "yLabel": "ΔG (relative)", "xRange": [0, 12], "yRange": [-6, 6], "grid": true, "functions": [{"expr": "6 - 1*x", "label": "ΔG; spontaneous where ΔG < 0", "color": "#2563eb"}]}
```

```mermaid
flowchart TB
  Q{"Sign of ΔG = ΔH − TΔS?"}
  Q -->|"ΔG < 0"| S["Spontaneous (forward)"]
  Q -->|"ΔG = 0"| E["At equilibrium"]
  Q -->|"ΔG > 0"| N["Non-spontaneous (reverse favoured)"]
```

**Next:** how molecules share energy across available levels — the Boltzmann
distribution.
""",
        ),
        _t(
            "Temperature, heat capacity & the Boltzmann distribution",
            "11 min",
            r"""
# Temperature, heat capacity & the Boltzmann distribution

Temperature is not "amount of heat" — it is a measure of the *average* thermal
energy per molecule. Energy is quantized into levels, and at thermal equilibrium
the fraction of molecules in a level of energy $\varepsilon_i$ follows the
**Boltzmann distribution**:

$$\frac{n_i}{N} = \frac{g_i\,e^{-\varepsilon_i / k_B T}}{q}, \qquad q = \sum_i g_i\,e^{-\varepsilon_i/k_B T},$$

where $q$ is the molecular **partition function** and $g_i$ the degeneracy. As
$T$ rises, higher levels become populated. The population of an excited level
*decays exponentially* with its energy at fixed temperature:

```plot
{"title": "Relative population vs level energy (Boltzmann factor, kT=2)", "xLabel": "level energy ε (relative)", "yLabel": "relative population", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "exp(−ε/kT)", "color": "#dc2626"}]}
```

**Heat capacity** $C$ measures how much energy a substance must absorb to raise
its temperature by one kelvin: $C_p = (\partial H/\partial T)_p$ and
$C_V = (\partial U/\partial T)_V$. Larger molecules have more vibrational and
rotational modes to store energy, so they have larger heat capacities.

```mermaid
flowchart LR
  E0["Ground level (most populated)"] --> E1["Level 1 (fewer)"]
  E1 --> E2["Level 2 (fewer still)"]
  E2 --> E3["Level 3 (rare)"]
  T["Raise T"] -.->|"populates higher levels"| E2
```

**Next:** put it to the test — the Basics checkpoint quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Physical Chemistry & Thermodynamics — Intermediate ───────────────────────

_INTERMEDIATE = SeedCourse(
    slug="physical-chemistry-intermediate",
    title="Physical Chemistry & Thermodynamics — Intermediate",
    description=(
        "The core quantitative machinery: chemical potential and the reaction "
        "quotient, the equilibrium constant and its temperature dependence, "
        "rate laws and reaction orders, the Arrhenius equation and transition "
        "state theory, reaction mechanisms, and an introduction to electrochemistry. "
        "Worked equations with interactive kinetics and equilibrium plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Chemical potential & the equilibrium constant",
            "12 min",
            r"""
# Chemical potential & the equilibrium constant

The **chemical potential** $\mu_i$ is the molar Gibbs energy of species $i$ and
the true driving force for matter to flow or react. For an ideal mixture,

$$\mu_i = \mu_i^\circ + RT \ln a_i,$$

with $a_i$ the **activity** (effectively concentration or partial pressure
relative to a standard state). The reaction Gibbs energy is

$$\Delta_r G = \Delta_r G^\circ + RT \ln Q, \qquad Q = \prod_i a_i^{\nu_i},$$

where $Q$ is the **reaction quotient**. At equilibrium $\Delta_r G = 0$, so
$Q = K$, the **equilibrium constant**, and we obtain the cornerstone relation

$$\Delta_r G^\circ = -RT \ln K.$$

A reaction is product-favoured ($K > 1$) exactly when $\Delta_r G^\circ < 0$.
The driving force $\Delta_r G = RT\ln(Q/K)$ is negative while $Q < K$, reaching
zero at equilibrium:

```plot
{"title": "Reaction driving force vs Q/K (RT=1)", "xLabel": "Q / K", "yLabel": "Δr G (relative)", "xRange": [0.1, 5], "yRange": [-3, 3], "grid": true, "functions": [{"expr": "log(x)", "label": "Δr G = RT ln(Q/K)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Q1["Q < K (Δr G < 0)"] -->|"forward reaction"| EQ["Q = K (equilibrium)"]
  Q2["Q > K (Δr G > 0)"] -->|"reverse reaction"| EQ
```

**Next:** how equilibrium shifts with temperature — van 't Hoff.
""",
        ),
        _t(
            "Le Chatelier & the van 't Hoff equation",
            "11 min",
            r"""
# Le Chatelier & the van 't Hoff equation

**Le Chatelier's principle** gives the qualitative response: a system at
equilibrium that is disturbed (concentration, pressure, temperature) shifts to
partly oppose the disturbance. Adding reactant pushes the reaction forward;
compressing a gas mixture favours the side with fewer moles of gas.

The quantitative version for temperature is the **van 't Hoff equation**,
obtained by differentiating $\ln K = -\Delta_r G^\circ/RT$:

$$\frac{d \ln K}{dT} = \frac{\Delta_r H^\circ}{R T^2}, \qquad
\ln K = -\frac{\Delta_r H^\circ}{R}\frac{1}{T} + \frac{\Delta_r S^\circ}{R}.$$

So a plot of $\ln K$ against $1/T$ is a straight line of slope
$-\Delta_r H^\circ/R$. For an **exothermic** reaction ($\Delta_r H^\circ < 0$),
$K$ *decreases* as temperature rises — heating disfavours products:

```plot
{"title": "ln K vs 1/T (van 't Hoff, exothermic: positive slope)", "xLabel": "1/T (relative)", "yLabel": "ln K", "xRange": [0, 5], "yRange": [-2, 8], "grid": true, "functions": [{"expr": "2*x - 1", "label": "slope = −ΔrH°/R > 0", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  D["Disturbance (add heat / reactant / pressure)"] --> S["System shifts to oppose it"]
  S --> NEW["New equilibrium position"]
```

**Next:** how *fast* a reaction reaches equilibrium — rate laws.
""",
        ),
        _t(
            "Rate laws & reaction order",
            "12 min",
            r"""
# Rate laws & reaction order

Thermodynamics says *whether*; kinetics says *how fast*. The **rate law**
relates the reaction rate to concentrations:

$$\text{rate} = k\,[A]^m[B]^n,$$

where $k$ is the rate constant and $m, n$ are the **orders** (determined
experimentally, not from stoichiometry). For a **first-order** reaction,
$\text{rate}=k[A]$, integration gives exponential decay:

$$[A](t) = [A]_0\,e^{-kt}, \qquad t_{1/2} = \frac{\ln 2}{k},$$

with a half-life independent of starting concentration. A **second-order**
reaction instead obeys $1/[A] = 1/[A]_0 + kt$, with a concentration-dependent
half-life. First-order decay is the canonical curve:

```plot
{"title": "First-order decay of reactant concentration (k=0.5)", "xLabel": "time t", "yLabel": "[A] / [A]0", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "[A] = [A]0 e^(−kt)", "color": "#2563eb"}]}
```

Identifying the order is a matter of finding which transform of the data is
linear: $\ln[A]$ vs $t$ (first order) or $1/[A]$ vs $t$ (second order).

```mermaid
flowchart LR
  DATA["Concentration vs time data"] --> T1["ln[A] linear?"]
  DATA --> T2["1/[A] linear?"]
  T1 -->|"yes"| O1["First order"]
  T2 -->|"yes"| O2["Second order"]
```

**Next:** why rate constants explode with temperature — Arrhenius.
""",
        ),
        _t(
            "Arrhenius equation & transition state theory",
            "12 min",
            r"""
# Arrhenius equation & transition state theory

Rate constants rise steeply with temperature because molecules must surmount an
energy barrier. The **Arrhenius equation** captures this:

$$k = A\,e^{-E_a / RT},$$

where $E_a$ is the **activation energy** and $A$ the pre-exponential (frequency)
factor. Taking logs, $\ln k = \ln A - E_a/(RT)$, so $\ln k$ versus $1/T$ is
linear with slope $-E_a/R$. The Boltzmann factor $e^{-E_a/RT}$ — the fraction of
collisions with enough energy — grows rapidly with $T$:

```plot
{"title": "Fraction of collisions exceeding the barrier vs temperature", "xLabel": "temperature T (relative)", "yLabel": "exp(−Ea/RT)", "xRange": [0.5, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-3/x)", "label": "exp(−Ea/RT)", "color": "#dc2626"}]}
```

**Transition state theory (TST)** refines this picture: reactants pass through
an activated complex at the saddle point of the potential energy surface, and the
rate is governed by the Gibbs energy of activation via the Eyring equation,
$k = (k_B T/h)\,e^{-\Delta^\ddagger G/RT}$. A **catalyst** speeds a reaction by
lowering $E_a$ (offering a new pathway), not by changing $\Delta_r G$ or $K$.

```mermaid
flowchart LR
  R["Reactants"] -->|"climb Ea"| TS["Transition state (saddle point)"]
  TS -->|"descend"| P["Products"]
  CAT["Catalyst"] -.->|"lowers Ea"| TS
```

**Next:** how elementary steps combine into observed kinetics — mechanisms.
""",
        ),
        _t(
            "Reaction mechanisms & rate-determining steps",
            "11 min",
            r"""
# Reaction mechanisms & rate-determining steps

A balanced equation is a summary; the **mechanism** is the sequence of
**elementary steps** that actually occur. Each elementary step has a
molecularity (unimolecular, bimolecular) and a rate law read directly from its
stoichiometry. The overall observed rate law must be *derived* from the
mechanism and matched to experiment.

The **rate-determining step (RDS)** is the slowest elementary step; it acts as a
bottleneck that controls the overall rate. Two common tools simplify the
algebra: the **steady-state approximation** (net rate of change of a reactive
intermediate is approximately zero) and the **pre-equilibrium approximation**
(a fast reversible step stays near equilibrium). For an enzyme reaction the
Michaelis–Menten mechanism yields the saturating rate law
$v = V_{max}[S]/(K_m + [S])$:

```plot
{"title": "Michaelis–Menten rate vs substrate concentration", "xLabel": "[S] (relative)", "yLabel": "rate v (relative)", "xRange": [0, 12], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8*x/(2+x)", "label": "v = Vmax[S]/(Km+[S])", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  R["Reactants"] -->|"fast"| INT["Intermediate"]
  INT -->|"slow (RDS)"| P["Products"]
  INT -.->|"steady state: d[INT]/dt ≈ 0"| INT
```

**Next:** chemistry driven by electron flow — electrochemistry.
""",
        ),
        _t(
            "Electrochemistry & the Nernst equation",
            "11 min",
            r"""
# Electrochemistry & the Nernst equation

Redox reactions transfer electrons, and an electrochemical cell turns that
transfer into measurable voltage. The maximum electrical work links cell
potential to Gibbs energy:

$$\Delta_r G = -n F E, \qquad \Delta_r G^\circ = -n F E^\circ,$$

where $n$ is the number of electrons, $F$ the Faraday constant and $E^\circ$ the
standard cell potential (from a table of half-cell reduction potentials). A
spontaneous (galvanic) cell has $E > 0$.

Away from standard conditions, the **Nernst equation** gives the potential as a
function of composition:

$$E = E^\circ - \frac{RT}{nF}\ln Q.$$

As the reaction proceeds, $Q$ rises toward $K$ and the potential falls toward
zero (a dead battery). For $n=1$ at room temperature, $E$ drops by about
59 mV per decade of $Q$ — its logarithmic decline:

```plot
{"title": "Cell potential vs reaction quotient (Nernst, E°=1, RT/nF=0.5)", "xLabel": "Q", "yLabel": "E (V)", "xRange": [0.1, 5], "yRange": [-0.5, 2], "grid": true, "functions": [{"expr": "1 - 0.5*log(x)", "label": "E = E° − (RT/nF) ln Q", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  AN["Anode (oxidation, loses e−)"] -->|"electrons via wire"| CAT["Cathode (reduction, gains e−)"]
  SALT["Salt bridge"] -.->|"ion balance"| AN
  SALT -.-> CAT
```

**Next:** check your mastery — the Intermediate quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Physical Chemistry & Thermodynamics — Advanced ───────────────────────────

_ADVANCED = SeedCourse(
    slug="physical-chemistry-advanced",
    title="Physical Chemistry & Thermodynamics — Advanced",
    description=(
        "Quantum chemistry and spectroscopy underlying modern molecular modeling: "
        "the Schrödinger equation and particle-in-a-box quantization, the molecular "
        "Hamiltonian and Born–Oppenheimer surfaces, electronic structure methods "
        "(Hartree–Fock to DFT), statistical thermodynamics from partition functions, "
        "molecular spectroscopy, and machine-learning interatomic potentials. "
        "State-of-the-art and computational throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The Schrödinger equation & quantization",
            "13 min",
            r"""
# The Schrödinger equation & quantization

At molecular scales, particles obey quantum mechanics. The **time-independent
Schrödinger equation** determines the allowed stationary states:

$$\hat{H}\psi = E\psi, \qquad \hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r}),$$

where $\psi$ is the wavefunction, $\hat{H}$ the Hamiltonian, and $|\psi|^2$ the
probability density. **Quantization** — discrete energy levels — emerges from
boundary conditions. For a **particle in a 1D box** of length $L$:

$$E_n = \frac{n^2 h^2}{8 m L^2}, \qquad \psi_n(x) = \sqrt{\tfrac{2}{L}}\sin\!\frac{n\pi x}{L}, \quad n = 1,2,3,\dots$$

Energies scale as $n^2$, so the spacing widens as $n$ grows — the parabolic
ladder of levels:

```plot
{"title": "Particle-in-a-box energy levels E_n ∝ n^2", "xLabel": "quantum number n", "yLabel": "energy E_n (relative)", "xRange": [0, 6], "yRange": [0, 36], "grid": true, "functions": [{"expr": "x^2", "label": "E_n ∝ n²", "color": "#2563eb"}]}
```

This simple model already explains why confining electrons (e.g. in conjugated
dyes or quantum dots) shifts their absorption colour, and it underpins the
basis-set picture used in computational chemistry.

```mermaid
flowchart LR
  BC["Boundary conditions (ψ=0 at walls)"] --> QN["Allowed quantum numbers n"]
  QN --> EL["Discrete energy levels E_n ∝ n²"]
  EL --> SP["Spectroscopic transitions"]
```

**Next:** scaling from one particle to whole molecules — the molecular
Hamiltonian.
""",
        ),
        _t(
            "Molecular Hamiltonian & Born–Oppenheimer",
            "12 min",
            r"""
# Molecular Hamiltonian & Born–Oppenheimer

A molecule's Hamiltonian contains kinetic energy of nuclei and electrons plus
all Coulomb interactions among them. Solving it exactly is intractable beyond a
few electrons, so we make the **Born–Oppenheimer approximation**: because nuclei
are thousands of times heavier than electrons, they move much more slowly, and we
can freeze the nuclei, solve the *electronic* Schrödinger equation at fixed
geometry, and obtain the electronic energy $E_{\text{elec}}(\mathbf{R})$ as a
function of nuclear coordinates.

That function is the **potential energy surface (PES)**. Minima are stable
structures; first-order saddle points are transition states; the steepest-descent
path connecting them is the reaction coordinate. Near a minimum the PES is
approximately harmonic, $V \approx \tfrac{1}{2}k(R-R_0)^2$ — the parabola that
defines vibrational frequencies:

```plot
{"title": "Harmonic approximation to a PES minimum", "xLabel": "displacement R − R0", "yLabel": "potential energy V (relative)", "xRange": [-4, 4], "yRange": [0, 8], "grid": true, "functions": [{"expr": "0.5*x^2", "label": "V ≈ ½ k (R−R0)²", "color": "#16a34a"}]}
```

Forces on the nuclei are $-\nabla_{\mathbf{R}} E_{\text{elec}}$, the foundation
of **geometry optimization** and **ab initio molecular dynamics**.

```mermaid
flowchart LR
  HAM["Full molecular Hamiltonian"] -->|"freeze nuclei (BO)"| ELEC["Electronic Schrödinger eqn at fixed R"]
  ELEC --> PES["E_elec(R) = potential energy surface"]
  PES --> OPT["Geometry optimization / dynamics"]
```

**Next:** how we actually solve the electronic problem — HF and DFT.
""",
        ),
        _t(
            "Electronic structure: Hartree–Fock to DFT",
            "13 min",
            r"""
# Electronic structure: Hartree–Fock to DFT

The electronic Schrödinger equation is solved approximately by **electronic
structure methods**. **Hartree–Fock (HF)** writes the wavefunction as a single
Slater determinant of molecular orbitals and treats electron–electron repulsion
as an averaged (mean) field, solved self-consistently (the SCF cycle). HF misses
**electron correlation**; post-HF methods (MP2, coupled cluster CCSD(T) — the
"gold standard") recover it at steep computational cost.

**Density functional theory (DFT)** reformulates the problem in terms of the
electron density $n(\mathbf{r})$ rather than the many-electron wavefunction. The
Hohenberg–Kohn theorems guarantee the ground-state energy is a functional of the
density, and the Kohn–Sham equations make it practical. DFT (with functionals
like B3LYP or PBE) offers a favourable accuracy/cost balance and dominates
applied molecular modeling. Cost scales steeply with system size $N$ — roughly
$N^3$ for DFT versus $N^7$ for CCSD(T):

```plot
{"title": "Computational cost vs system size (illustrative scaling)", "xLabel": "system size N (relative)", "yLabel": "cost (relative)", "xRange": [1, 6], "yRange": [0, 250], "grid": true, "functions": [{"expr": "x^3", "label": "DFT ~ N³", "color": "#2563eb"}, {"expr": "x^4", "label": "MP2-like ~ N⁴", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  HF["Hartree–Fock (mean field)"] -->|"add correlation"| POST["MP2 / CCSD(T)"]
  HF -->|"density functional"| DFT["DFT (Kohn–Sham)"]
  DFT --> APP["Applied molecular modeling"]
  POST --> APP
```

**Next:** bridging quantum energy levels to bulk thermodynamics — partition
functions.
""",
        ),
        _t(
            "Statistical thermodynamics & partition functions",
            "12 min",
            r"""
# Statistical thermodynamics & partition functions

**Statistical thermodynamics** derives macroscopic properties from molecular
energy levels. The central quantity is the **partition function** — for a
canonical ensemble of $N$ particles,

$$Q = \sum_i g_i\, e^{-\varepsilon_i / k_B T},$$

which counts the thermally accessible states. Every thermodynamic property
follows from $Q$ (or its molecular factor $q = q_{\text{trans}} q_{\text{rot}}
q_{\text{vib}} q_{\text{elec}}$):

$$U = k_B T^2 \left(\frac{\partial \ln Q}{\partial T}\right)_V, \qquad
S = k_B \ln Q + \frac{U}{T}, \qquad A = -k_B T \ln Q.$$

This is how computational chemistry converts a vibrational frequency calculation
into entropies, heat capacities and free energies of reaction at any
temperature. The molecular partition function *grows* with temperature as more
states become accessible — illustrated by a saturating, then rising count:

```plot
{"title": "Thermally accessible states vs temperature (illustrative)", "xLabel": "temperature T (relative)", "yLabel": "partition function q (relative)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "exp(0.2*x)", "label": "q grows with T", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  LEV["Quantum energy levels (from QM)"] --> Q["Partition function q(T)"]
  Q --> THERMO["U, S, A, Cv, G via derivatives of ln Q"]
  THERMO --> RXN["Reaction thermodynamics at any T"]
```

**Next:** probing those levels experimentally — spectroscopy.
""",
        ),
        _t(
            "Molecular spectroscopy",
            "12 min",
            r"""
# Molecular spectroscopy

**Spectroscopy** measures transitions between quantized states by absorption or
emission of light, with the resonance condition $\Delta E = h\nu$. Different
energy scales probe different motions: **microwave** (rotational), **infrared**
(vibrational), **UV–visible** (electronic), and **NMR** (nuclear spin in a
magnetic field).

For a **harmonic vibration**, allowed transitions are $\Delta v = \pm 1$ and
require a changing dipole moment; the fundamental appears at the vibrational
frequency $\tilde\nu = (1/2\pi c)\sqrt{k/\mu}$, where $\mu$ is the reduced mass.
**Rotational** levels are $E_J = h c B J(J+1)$, giving evenly spaced lines in a
rigid rotor. A spectral peak is well modelled by a Lorentzian/Gaussian band
centred at the transition frequency:

```plot
{"title": "Absorption band (Gaussian line shape) centred at ν0=5", "xLabel": "frequency (relative)", "yLabel": "absorbance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-(x-5)^2)", "label": "absorption band", "color": "#dc2626"}]}
```

Selection rules, peak positions and intensities are computed directly from the
electronic-structure and partition-function machinery, making spectroscopy the
key validation of molecular models.

```mermaid
flowchart LR
  MW["Microwave → rotational"] --> SP["Spectrum"]
  IR["Infrared → vibrational"] --> SP
  UV["UV–Vis → electronic"] --> SP
  NMR["NMR → nuclear spin"] --> SP
  SP --> ID["Structure & dynamics"]
```

**Next:** learning the energy surface itself — ML interatomic potentials.
""",
        ),
        _t(
            "Machine-learning interatomic potentials",
            "12 min",
            r"""
# Machine-learning interatomic potentials

Accurate quantum methods (DFT, CCSD(T)) are too expensive for long molecular
dynamics or large systems. **Machine-learning interatomic potentials (MLIPs)**
fix this: a model is trained on a dataset of quantum-computed energies and forces
and then predicts the PES at a tiny fraction of the cost, with near-quantum
accuracy. Methods include **Behler–Parrinello neural networks**, the **Gaussian
Approximation Potential (GAP)**, and modern **equivariant graph neural networks**
(NequIP, MACE) plus large **foundation models** trained on broad chemistry.

The workflow is a data pipeline: sample configurations, label them with quantum
calculations, fit the model, then run fast dynamics — often with **active
learning** that flags high-uncertainty structures for new quantum labels. Test
error typically falls off as a power law with training-set size $N$:

```plot
{"title": "MLIP error vs training-set size (power-law decay)", "xLabel": "training examples N (relative)", "yLabel": "test error (relative)", "xRange": [1, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "error ~ N^(−1/2)", "color": "#16a34a"}]}
```

MLIPs now enable million-atom simulations of catalysis, batteries and proteins
that were previously impossible at quantum accuracy.

```mermaid
flowchart LR
  SAMP["Sample configurations"] --> QM["Label with DFT/CCSD(T)"]
  QM --> TRAIN["Train ML potential"]
  TRAIN --> MD["Fast molecular dynamics"]
  MD -->|"active learning: high uncertainty"| QM
```

**Next:** prove your mastery — the Advanced quiz.
""",
        ),
        _quiz(),
    ),
)


PHYSICAL_CHEMISTRY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["PHYSICAL_CHEMISTRY_COURSES"]
