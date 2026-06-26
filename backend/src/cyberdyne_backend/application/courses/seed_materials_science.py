"""Materials Science & Engineering track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on the structure-property-processing
triangle. Starts from atomic bonding, crystal structures and the mechanical
intuition of stress and strain; builds the quantitative core of defects,
diffusion, phase diagrams and strengthening; and ends with the engineering
classes (metals, ceramics, polymers, composites), failure analysis and
computational/ML-driven materials selection. Lessons are `text` with LaTeX,
interactive ```plot blocks (stress-strain, Arrhenius, S-N, Ashby), ```mermaid
classification/process diagrams and ```python/```matlab code where it teaches a
method.
"""

# Lesson prose uses typographic characters (×, →, ≈, Å, μ, σ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Materials Science — Basics ───────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="materials-science-basics",
    title="Materials Science & Engineering — Basics",
    description=(
        "The foundations of why materials behave as they do: the four classes of "
        "engineering materials and the structure-property-processing triangle, "
        "atomic bonding, crystal structures and the unit cell, the elastic regime "
        "(stress, strain, Young's modulus and Poisson's ratio), and the basic "
        "vocabulary of strength, ductility and toughness read off a tensile test. "
        "Interactive plots and classification diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What materials science is",
            "10 min",
            r"""
# What materials science is

Materials science studies the link between a material's **internal structure**,
its **properties**, and how it is **processed** — and how all three feed back on
each other. This is the **structure-property-processing-performance** tetrahedron,
the central paradigm of the field.

Engineers group materials into four broad classes, plus composites that mix
them:

- **Metals** — metallic bonding; strong, stiff, ductile, conductive (steel, Al).
- **Ceramics** — ionic/covalent bonding; hard, stiff, heat-resistant, brittle
  (alumina, $\mathrm{Al_2O_3}$).
- **Polymers** — long covalent chains; light, flexible, cheap (nylon, PE).
- **Composites** — engineered combinations (carbon-fibre-reinforced polymer).

```mermaid
flowchart LR
  S["Processing (casting, rolling, heat treat)"] --> ST["Structure (atoms, grains, phases)"]
  ST --> P["Properties (strength, stiffness, conductivity)"]
  P --> PE["Performance (in service)"]
  PE -->|"feedback: redesign"| S
```

The same chemistry can give wildly different properties: slow-cooled vs quenched
steel differ enormously in hardness because **processing** changes the
**structure**. Mastering that chain is what lets a mechanical engineer pick — or
design — the right material for a part.

**Next:** the glue that holds atoms together — bonding.
""",
        ),
        _t(
            "Atomic bonding",
            "11 min",
            r"""
# Atomic bonding

Properties begin at the bond. How atoms share or trade electrons sets stiffness,
melting point and conductivity. The **primary** (strong) bonds are:

- **Ionic** — electrons transferred (Na⁺Cl⁻); strong, non-directional, brittle,
  insulating.
- **Covalent** — electrons shared and **directional** (diamond, Si); very stiff
  and hard.
- **Metallic** — a shared "sea" of delocalised electrons; ductile and
  conductive.

Plus weaker **secondary** bonds (van der Waals, hydrogen) that hold polymer
chains together.

A bond is captured by an **interatomic potential** $U(r)$: short-range
repulsion plus longer-range attraction, with a minimum at the equilibrium
spacing $r_0$. The **force** is $F = -dU/dr$, and the curvature at $r_0$ sets the
material's **stiffness** (Young's modulus). A deeper, narrower well means a
stiffer, higher-melting material.

```plot
{"title": "Lennard-Jones interatomic potential U(r)", "xLabel": "separation r (relative)", "yLabel": "energy U (relative)", "xRange": [0.9, 2.5], "yRange": [-1.3, 1.5], "grid": true, "functions": [{"expr": "1/x^12 - 2/x^6", "label": "U(r) = (1/r)^12 - 2(1/r)^6", "color": "#2563eb"}]}
```

The minimum at $r \approx 1$ is the equilibrium bond length; pulling atoms apart
(right) costs energy until the bond breaks, while pushing them together (left)
is strongly resisted.

**Next:** how bonded atoms stack into ordered crystals.
""",
        ),
        _t(
            "Crystal structures & the unit cell",
            "12 min",
            r"""
# Crystal structures & the unit cell

Most metals and ceramics are **crystalline**: atoms repeat on a periodic
lattice. The smallest repeating block is the **unit cell**. Three structures
dominate the metals:

- **BCC** (body-centred cubic) — Fe (room T), W, Cr. 2 atoms/cell.
- **FCC** (face-centred cubic) — Al, Cu, Ni, γ-Fe. 4 atoms/cell, very ductile.
- **HCP** (hexagonal close-packed) — Mg, Ti, Zn. 6 atoms/cell, fewer slip
  systems → less ductile.

A key descriptor is the **atomic packing factor** (APF), the fraction of space
filled by hard-sphere atoms:

$$\mathrm{APF} = \frac{n \cdot \tfrac{4}{3}\pi r^3}{a^3},$$

where $n$ is atoms per cell, $r$ the atomic radius and $a$ the lattice
parameter. FCC and HCP are **close-packed** at $\mathrm{APF}=0.74$; BCC is
$0.68$. Higher packing and more **slip systems** generally mean more ductility.

```mermaid
flowchart TB
  C["Crystalline metal"] --> BCC["BCC: APF 0.68, n=2 (Fe, W)"]
  C --> FCC["FCC: APF 0.74, n=4 (Al, Cu)"]
  C --> HCP["HCP: APF 0.74, n=6 (Mg, Ti)"]
```

**Polymorphism** matters in practice: iron transforms from BCC (ferrite) to FCC
(austenite) on heating past ~912 °C — the basis of all steel heat treatment.

**Next:** how we describe elastic deformation — stress and strain.
""",
        ),
        _t(
            "Stress, strain & elasticity",
            "12 min",
            r"""
# Stress, strain & elasticity

Apply a load and a material deforms. We normalise force by area and elongation
by length so the description is geometry-independent.

- **Engineering stress:** $\sigma = F/A_0$ (Pa or MPa).
- **Engineering strain:** $\varepsilon = \Delta L / L_0$ (dimensionless).

In the small-strain **elastic** regime, deformation is reversible and **linear**
— this is **Hooke's law**:

$$\sigma = E\,\varepsilon,$$

where $E$ is **Young's modulus** (stiffness, GPa). Stretching along one axis also
contracts the transverse directions; the ratio is **Poisson's ratio**
$\nu = -\varepsilon_\text{lat}/\varepsilon_\text{axial}$ (≈ 0.3 for most metals).
Shear has its own law $\tau = G\gamma$, with $G = E/[2(1+\nu)]$.

The elastic line is steep and straight — its slope *is* $E$. Steel ($E\approx
200$ GPa) climbs far faster in stress than aluminium ($\approx 70$ GPa) for the
same strain:

```plot
{"title": "Elastic stress-strain: slope = Young's modulus E", "xLabel": "strain ε", "yLabel": "stress σ (MPa)", "xRange": [0, 0.002], "yRange": [0, 400], "grid": true, "functions": [{"expr": "200000*x", "label": "steel, E = 200 GPa", "color": "#2563eb"}, {"expr": "70000*x", "label": "aluminium, E = 70 GPa", "color": "#dc2626"}]}
```

$E$ is set by bond stiffness (the curvature of $U(r)$) and is barely changed by
processing — unlike strength, which we can tune dramatically.

**Next:** reading the full mechanical story off a tensile test.
""",
        ),
        _t(
            "The tensile test & mechanical properties",
            "12 min",
            r"""
# The tensile test & mechanical properties

Pull a standard specimen to failure and the **stress-strain curve** reveals a
material's whole mechanical character. Key landmarks:

- **Elastic region** — linear, slope $E$; unloads with no permanent set.
- **Yield strength** $\sigma_y$ — onset of permanent (plastic) deformation,
  measured at the **0.2 % offset**.
- **Ultimate tensile strength (UTS)** — the peak stress.
- **Ductility** — total plastic strain at fracture (% elongation).
- **Toughness** — the **area under the curve**, energy absorbed before fracture.

A ductile metal shows a long plastic plateau; a brittle ceramic snaps near the
elastic limit with almost no plastic strain. The schematic below rises elastically
($200x$), then yields and work-hardens more gently before necking:

```plot
{"title": "Ductile tensile curve: elastic then plastic to UTS", "xLabel": "strain ε (%)", "yLabel": "stress σ (MPa)", "xRange": [0, 20], "yRange": [0, 500], "grid": true, "functions": [{"expr": "250 + 90*sqrt(abs(x))", "label": "plastic / work hardening", "color": "#dc2626"}, {"expr": "200*x", "label": "elastic region (slope E)", "color": "#2563eb"}]}
```

Note the difference between **true stress** ($\sigma_t = F/A_\text{inst}$) and
engineering stress: as the cross-section necks, true stress keeps rising even
after the engineering curve turns over. Designers size parts against $\sigma_y$
with a **safety factor**, and choose tough materials where energy absorption
(crashworthiness) matters.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Materials Science — Intermediate ─────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="materials-science-intermediate",
    title="Materials Science & Engineering — Intermediate",
    description=(
        "The quantitative core that explains and controls properties: crystal "
        "defects and the dislocations that carry plastic flow, the strengthening "
        "mechanisms that obstruct them, diffusion and Fick's laws, binary phase "
        "diagrams and the lever rule, the iron-carbon system with TTT-driven heat "
        "treatment, and fracture/fatigue/creep failure. LaTeX, interactive plots "
        "and Python computation throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Crystal defects & dislocations",
            "12 min",
            r"""
# Crystal defects & dislocations

Real crystals are never perfect, and it is the **defects** that govern
mechanical behaviour. They are classified by dimensionality:

- **0-D (point):** vacancies, interstitials, substitutional atoms. The
  equilibrium vacancy fraction follows an Arrhenius law,
  $n_v/N = \exp(-Q_v/k_BT)$.
- **1-D (line):** **dislocations** — edge and screw. These are the carriers of
  **plastic deformation**.
- **2-D (planar):** **grain boundaries**, free surfaces, twin and phase
  boundaries.
- **3-D (volume):** voids, inclusions, precipitates.

The crucial insight: a crystal deforms plastically not by ripping all bonds
across a plane at once (which would need its huge theoretical strength), but by
**gliding one dislocation line** through the lattice — like moving a rug ripple
instead of dragging the whole rug. This is why real yield strengths are 10–100×
**below** the ideal bond-breaking strength.

```mermaid
flowchart TB
  D["Crystal defects"] --> P0["0-D: vacancies, interstitials"]
  D --> P1["1-D: dislocations (edge, screw) -> plasticity"]
  D --> P2["2-D: grain boundaries, twins"]
  D --> P3["3-D: voids, precipitates"]
```

The slip plane (the resolved shear stress on a slip system is the **Schmid
law**, $\tau_R = \sigma\cos\phi\cos\lambda$) and the **Burgers vector** $\mathbf{b}$
quantify a dislocation's slip. Computing the equilibrium vacancy concentration:

```python
import numpy as np
kB = 8.617e-5          # eV/K
Qv = 0.9               # vacancy formation energy, eV (Cu ~0.9)
T  = np.array([300., 600., 900., 1200.])
nv_over_N = np.exp(-Qv / (kB * T))
for t, f in zip(T, nv_over_N):
    print(f"T={t:6.0f} K   n_v/N = {f:.3e}")
# vacancies multiply by orders of magnitude as T rises -> faster diffusion
```

**Next:** how we deliberately obstruct dislocations to make metals stronger.
""",
        ),
        _t(
            "Strengthening mechanisms",
            "12 min",
            r"""
# Strengthening mechanisms

If plastic flow is dislocation motion, **strengthening = making dislocations
harder to move**. Four mechanisms dominate, and they superpose:

1. **Grain-size (Hall-Petch).** Grain boundaries block slip. Yield strength rises
   as grains shrink:
   $$\sigma_y = \sigma_0 + \frac{k_y}{\sqrt{d}}.$$
2. **Solid-solution.** Dissolved atoms strain the lattice and pin dislocations
   (Zn in brass).
3. **Strain (work) hardening.** Cold work multiplies dislocations until they
   tangle; flow stress scales as $\sigma \propto \sqrt{\rho}$ (dislocation
   density).
4. **Precipitation/dispersion.** Fine second-phase particles force dislocations
   to bow (Orowan) or cut them (age-hardened Al alloys).

Hall-Petch is strikingly powerful — halving grain size from 100 µm to 25 µm can
add tens of MPa. Sweep grain size $d$ and watch $\sigma_y$ climb as $1/\sqrt{d}$:

```plot
{"title": "Hall-Petch: yield strength vs grain size", "xLabel": "grain size d (micron)", "yLabel": "yield strength sigma_y (MPa)", "xRange": [1, 100], "yRange": [0, 400], "grid": true, "functions": [{"expr": "100 + 600/sqrt(x)", "label": "sigma_y = sigma_0 + k_y / sqrt(d)", "color": "#2563eb"}]}
```

Fitting Hall-Petch constants from data:

```python
import numpy as np
d   = np.array([100., 50., 25., 10., 5.]) * 1e-6      # m
sy  = np.array([170., 190., 220., 290., 370.])         # MPa
x   = 1.0 / np.sqrt(d)
ky, s0 = np.polyfit(x, sy, 1)        # slope = k_y, intercept = sigma_0
print(f"sigma_0 = {s0:.1f} MPa,  k_y = {ky:.3f} MPa*sqrt(m)")
```

Every strengthening route trades against ductility — stronger usually means less
formable, the central tension in alloy design.

**Next:** the mass-transport process behind heat treatment — diffusion.
""",
        ),
        _t(
            "Diffusion & Fick's laws",
            "12 min",
            r"""
# Diffusion & Fick's laws

**Diffusion** is the net migration of atoms down a concentration gradient — the
engine behind doping, carburising, sintering and phase transformations.

**Fick's first law** (steady state): flux is proportional to the gradient,
$$J = -D\,\frac{dC}{dx}.$$

**Fick's second law** (transient) governs how concentration evolves in time,
$$\frac{\partial C}{\partial t} = D\,\frac{\partial^2 C}{\partial x^2}.$$

The diffusion coefficient $D$ is fiercely **temperature-dependent** via an
Arrhenius law,
$$D = D_0\,\exp\!\left(-\frac{Q_d}{RT}\right),$$
so a modest temperature rise can speed diffusion by orders of magnitude. Plotting
$\ln D$ vs $1/T$ gives a straight line of slope $-Q_d/R$:

```plot
{"title": "Arrhenius: ln D vs 1000/T (straight line, slope = -Q/R)", "xLabel": "1000/T (1/K)", "yLabel": "ln D", "xRange": [0.7, 2.0], "yRange": [-40, -10], "grid": true, "functions": [{"expr": "-2 - 18*x", "label": "ln D = ln D0 - (Q/R)(1/T)", "color": "#dc2626"}]}
```

For a semi-infinite solid with fixed surface composition (carburising steel) the
solution is the **error function**:
$$\frac{C(x,t)-C_0}{C_s-C_0} = 1 - \mathrm{erf}\!\left(\frac{x}{2\sqrt{Dt}}\right).$$

```python
import numpy as np
from scipy.special import erf
D, t = 1.6e-11, 3600*10        # m^2/s at 950C, 10 h carburise
Cs, C0 = 1.0, 0.2              # wt% C surface / core
x = np.linspace(0, 2e-3, 6)
C = C0 + (Cs - C0) * (1 - erf(x / (2*np.sqrt(D*t))))
for xi, Ci in zip(x*1e3, C):
    print(f"depth {xi:4.1f} mm  ->  C = {Ci:.3f} wt%")
```

The case depth scales as $\sqrt{Dt}$ — quadrupling time only doubles depth.

**Next:** the maps that tell us which phases exist — phase diagrams.
""",
        ),
        _t(
            "Phase diagrams & the lever rule",
            "12 min",
            r"""
# Phase diagrams & the lever rule

A **phase diagram** maps the equilibrium phases of an alloy against composition
and temperature. The **lever rule** then tells us *how much* of each phase is
present.

For a binary isomorphous system (e.g. Cu-Ni), between the **liquidus** and
**solidus** lines liquid and solid coexist. At a given temperature, draw a
horizontal **tie line**; its ends give the two phase compositions
($C_L$, $C_\alpha$), and the **lever rule** gives the fractions:

$$W_L = \frac{C_\alpha - C_0}{C_\alpha - C_L}, \qquad
W_\alpha = \frac{C_0 - C_L}{C_\alpha - C_L}.$$

Many systems are **eutectic**: at the eutectic point a single liquid freezes
into two solids at once, $L \rightarrow \alpha + \beta$ (the lowest melting
point, e.g. 61.9 wt% Sn in Pb-Sn solder). The **Gibbs phase rule** $P + F = C +
1$ (at fixed pressure) fixes the degrees of freedom.

```mermaid
flowchart TB
  PD["Cool a liquid alloy"] --> LIQ["Above liquidus: all liquid"]
  LIQ --> TWO["Between curves: liquid + solid (use lever rule)"]
  TWO --> SOL["Below solidus: all solid (alpha)"]
  TWO --> EUT["At eutectic: L -> alpha + beta simultaneously"]
```

Computing phase fractions across the two-phase field:

```python
import numpy as np
C0 = 35.0                      # overall composition, wt% B
CL, Ca = 20.0, 45.0            # tie-line ends at this temperature
W_L  = (Ca - C0) / (Ca - CL)
W_a  = (C0 - CL) / (Ca - CL)
print(f"liquid fraction = {W_L:.2f}, solid (alpha) fraction = {W_a:.2f}")
assert abs(W_L + W_a - 1.0) < 1e-9   # fractions sum to 1
```

**Next:** the most important phase diagram in engineering — iron-carbon.
""",
        ),
        _t(
            "Iron-carbon & heat treatment",
            "12 min",
            r"""
# Iron-carbon & heat treatment

Steel is iron with up to ~2 wt% carbon, and its behaviour is read off the
**iron-carbon (Fe-Fe₃C) diagram**. The key phases and reactions:

- **Ferrite (α)** — BCC, soft, low carbon solubility.
- **Austenite (γ)** — FCC, high carbon solubility, stable above ~727 °C.
- **Cementite (Fe₃C)** — hard, brittle iron carbide.
- **Eutectoid** at 0.76 wt% C, 727 °C: $\gamma \rightarrow \alpha + \mathrm{Fe_3C}$,
  forming the lamellar **pearlite**.

What makes steel so versatile is that **cooling rate decides the structure**,
captured by **TTT (time-temperature-transformation)** curves. Slow cooling gives
soft pearlite; very fast **quenching** traps carbon into hard, brittle
**martensite** (a diffusionless transformation), which is then **tempered** to
restore toughness.

Hardness rises sharply with carbon content (more cementite/martensite):

```plot
{"title": "Steel hardness rises with carbon content", "xLabel": "carbon content (wt%)", "yLabel": "hardness (HRC, schematic)", "xRange": [0, 1.0], "yRange": [0, 70], "grid": true, "functions": [{"expr": "20 + 55*sqrt(abs(x))", "label": "quenched hardness vs %C", "color": "#dc2626"}]}
```

The standard heat-treat sequence:

```mermaid
flowchart LR
  A["Austenitise (heat into gamma)"] --> Q["Quench fast -> martensite (hard, brittle)"]
  Q --> T["Temper (reheat) -> tempered martensite (tough)"]
  A --> S["Slow cool -> pearlite (soft, ductile)"]
```

Annealing, normalising, quenching and tempering are all just paths on this
diagram — the same alloy spanning a 5× range in strength.

**Next:** how parts actually fail — fracture, fatigue and creep.
""",
        ),
        _t(
            "Fracture, fatigue & creep",
            "12 min",
            r"""
# Fracture, fatigue & creep

Most service failures are not simple overload; they are progressive. Three
mechanisms dominate.

**Fracture.** A sharp crack concentrates stress. **Linear elastic fracture
mechanics** says a crack of length $a$ grows catastrophically when the **stress
intensity** reaches the material's **fracture toughness** $K_{IC}$:
$$K = Y\sigma\sqrt{\pi a} \ge K_{IC}.$$
This sets the **critical flaw size** a part can tolerate.

**Fatigue.** Cyclic loading far **below** yield grows cracks over many cycles.
The **S-N (Wöhler) curve** plots stress amplitude vs cycles to failure; steels
show an **endurance limit** below which life is effectively infinite:

```plot
{"title": "S-N fatigue curve: stress amplitude vs log cycles", "xLabel": "log10(cycles to failure)", "yLabel": "stress amplitude (MPa)", "xRange": [3, 8], "yRange": [100, 500], "grid": true, "functions": [{"expr": "550 - 60*x", "label": "S-N curve (endurance limit at high N)", "color": "#2563eb"}]}
```

**Creep.** At high temperature ($T > 0.4\,T_m$), materials deform slowly under
constant load. The steady-state creep rate is Arrhenius-and-stress dependent,
$\dot{\varepsilon}_s = A\,\sigma^n\exp(-Q_c/RT)$ — critical for turbine blades.

```python
import numpy as np
Y, KIC = 1.0, 50e6            # geometry factor, K_IC (Pa*sqrt(m)) for a steel
sigma  = 300e6                # applied stress, Pa
a_crit = (KIC / (Y * sigma))**2 / np.pi
print(f"critical crack length a_c = {a_crit*1e3:.2f} mm")
# inspection interval must catch cracks well below a_c
```

Designing against these means damage-tolerant sizing, stress-relief of
notches, and fatigue/creep life prediction — not just a static safety factor.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Materials Science — Advanced ─────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="materials-science-advanced",
    title="Materials Science & Engineering — Advanced",
    description=(
        "The engineering material classes and how we choose between them at the "
        "state of the art: structure-property design of metal alloys, ceramics and "
        "glasses, polymers and viscoelasticity, the micromechanics of composites, "
        "Ashby-chart materials selection with performance indices, and "
        "computational/ML-driven discovery (DFT, CALPHAD, ICME and surrogate "
        "models). LaTeX, interactive plots, mermaid workflows and Python "
        "throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Metals & alloy design",
            "12 min",
            r"""
# Metals & alloy design

Engineering metals are rarely pure — they are **alloys** designed by combining the
strengthening mechanisms from the Intermediate course against cost, weight,
corrosion and formability targets.

- **Steels** — Fe-C plus alloying (Cr, Ni, Mo, V). Stainless steels use ≥ 10.5 %
  Cr for a passive $\mathrm{Cr_2O_3}$ film; HSLA steels use micro-alloying +
  grain refinement.
- **Aluminium alloys** — light ($\rho \approx 2.7$ g/cm³), age-hardened (2xxx,
  7xxx) for aerospace.
- **Titanium** — high specific strength, biocompatible, expensive.
- **Superalloys** — Ni-based, $\gamma'$-strengthened for turbine creep
  resistance.

The figure of merit for lightweighting is **specific strength** $\sigma_y/\rho$.
Plotting it shows why Ti and CFRP displace steel where mass matters even at higher
cost:

```plot
{"title": "Specific strength vs density (lightweighting target)", "xLabel": "density rho (g/cm^3)", "yLabel": "specific strength sigma_y/rho (rel.)", "xRange": [1, 9], "yRange": [0, 200], "grid": true, "functions": [{"expr": "400/x", "label": "constant strength contour (sigma_y/rho)", "color": "#16a34a"}]}
```

A first-pass alloy screen ranking candidates by specific strength:

```python
import numpy as np
alloys = ["mild steel", "7075-Al", "Ti-6Al-4V", "Mg AZ31"]
sy     = np.array([250., 500., 900., 200.])    # MPa
rho    = np.array([7.85, 2.81, 4.43, 1.77])    # g/cm^3
spec   = sy / rho
for a, s in sorted(zip(alloys, spec), key=lambda p: -p[1]):
    print(f"{a:12s}  specific strength = {s:6.1f} MPa/(g/cm^3)")
```

Modern practice couples thermodynamic (CALPHAD) databases with these targets to
design alloys computationally — covered in the final lesson.

**Next:** the hard, brittle, heat-resistant class — ceramics and glasses.
""",
        ),
        _t(
            "Ceramics & glasses",
            "11 min",
            r"""
# Ceramics & glasses

Ceramics are ionic/covalent compounds — oxides, carbides, nitrides. Their strong,
directional, non-metallic bonds make them **hard, stiff, refractory and
chemically inert**, but **brittle**: with no easy dislocation glide, they cannot
relieve a crack tip by plastic flow.

The defining consequence is **flaw-controlled strength**. A ceramic fails from
its largest pre-existing flaw, so strength is **statistical**, not deterministic,
and is described by the **Weibull distribution**:

$$P_f = 1 - \exp\!\left[-\left(\frac{\sigma}{\sigma_0}\right)^m\right],$$

where $m$ is the **Weibull modulus** (higher $m$ = less scatter, more reliable).
Sweep applied stress and watch failure probability rise steeply for a ceramic
($m \approx 10$):

```plot
{"title": "Weibull failure probability vs stress (m = 10)", "xLabel": "stress / sigma_0", "yLabel": "probability of failure P_f", "xRange": [0, 1.6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - exp(-(x)^10)", "label": "P_f = 1 - exp(-(s/s0)^m)", "color": "#dc2626"}]}
```

**Glasses** are **amorphous** (no long-range order); below the **glass transition**
$T_g$ they are rigid, above it they flow. Toughening strategies — transformation
toughening in zirconia, fibre/whisker reinforcement, residual surface compression
in tempered glass — all aim to blunt or close cracks.

```python
import numpy as np
sigma = np.array([200., 250., 300., 350.])    # MPa
s0, m = 300.0, 10.0
Pf = 1 - np.exp(-(sigma/s0)**m)
for s, p in zip(sigma, Pf):
    print(f"sigma = {s:5.0f} MPa  ->  P_f = {p:.3f}")
# fit m by linear regression of ln(ln(1/(1-Pf))) vs ln(sigma)
```

**Next:** the light, chain-based, time-dependent class — polymers.
""",
        ),
        _t(
            "Polymers & viscoelasticity",
            "12 min",
            r"""
# Polymers & viscoelasticity

Polymers are long covalent chains held to one another by weak secondary bonds.
That architecture makes them light, cheap and tough but **time- and
temperature-dependent**. They divide into:

- **Thermoplastics** — chains slide on heating, remeltable (PE, PP, nylon).
- **Thermosets** — cross-linked networks, set permanently (epoxy).
- **Elastomers** — lightly cross-linked, huge reversible strains (rubber).

The defining behaviour is **viscoelasticity** — part elastic (spring), part
viscous (dashpot). Under a held load they **creep**; under a held strain they
**stress-relax**. The simple **Maxwell model** (spring + dashpot in series)
predicts exponential stress relaxation with a characteristic time
$\tau = \eta/E$:

$$\sigma(t) = \sigma_0\,e^{-t/\tau}.$$

```plot
{"title": "Maxwell stress relaxation (tau = 1)", "xLabel": "time t (units of tau)", "yLabel": "normalised stress sigma/sigma_0", "xRange": [0, 6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-x)", "label": "sigma(t) = sigma_0 e^(-t/tau)", "color": "#2563eb"}]}
```

Behaviour also pivots at the **glass transition** $T_g$: below it a thermoplastic
is glassy and stiff, above it rubbery. The **time-temperature superposition**
(WLF) principle lets short high-temperature tests predict long-term behaviour.

```python
import numpy as np
E0, eta = 2.0e3, 2.0e3*10      # MPa, MPa*s -> tau = 10 s
tau = eta / E0
t   = np.array([0, 5, 10, 20, 40.])
sig = 1.0 * np.exp(-t/tau)     # normalised relaxation
for ti, si in zip(t, sig):
    print(f"t={ti:5.0f}s  sigma/sigma0 = {si:.3f}")
```

**Next:** engineering two materials into one — composites.
""",
        ),
        _t(
            "Composites & micromechanics",
            "12 min",
            r"""
# Composites & micromechanics

A **composite** combines a stiff, strong **reinforcement** (carbon/glass fibre,
ceramic particles) in a **matrix** (polymer, metal, ceramic) to beat what either
phase achieves alone. The classic is **CFRP** — carbon fibre in epoxy.

Properties follow **micromechanics**. For stiffness along aligned continuous
fibres, the **rule of mixtures** (Voigt, iso-strain) gives an upper bound:

$$E_\parallel = V_f E_f + (1-V_f)E_m.$$

Transverse to the fibres the matrix dominates (Reuss, iso-stress lower bound):

$$\frac{1}{E_\perp} = \frac{V_f}{E_f} + \frac{1-V_f}{E_m}.$$

The strong **anisotropy** between these is why laminates are stacked in plies at
several angles. Longitudinal modulus rises **linearly** with fibre volume
fraction $V_f$ — the design lever:

```plot
{"title": "Rule of mixtures: longitudinal modulus vs fibre fraction", "xLabel": "fibre volume fraction V_f", "yLabel": "E_parallel (GPa)", "xRange": [0, 0.7], "yRange": [0, 250], "grid": true, "functions": [{"expr": "230*x + 3*(1-x)", "label": "E = Vf*Ef + (1-Vf)*Em", "color": "#2563eb"}]}
```

```python
import numpy as np
Ef, Em = 230.0, 3.0            # GPa: carbon fibre, epoxy
Vf = np.linspace(0, 0.6, 4)
E_par = Vf*Ef + (1-Vf)*Em                       # Voigt (upper)
E_perp = 1.0 / (Vf/Ef + (1-Vf)/Em)              # Reuss (lower)
for v, ep, et in zip(Vf, E_par, E_perp):
    print(f"Vf={v:.2f}  E_par={ep:6.1f}  E_perp={et:5.1f} GPa")
```

Composites trade superb specific stiffness/strength against cost, anisotropy and
hard-to-inspect failure modes (delamination) — addressed by selection methods next.

**Next:** choosing among all these classes — Ashby selection.
""",
        ),
        _t(
            "Materials selection & Ashby charts",
            "12 min",
            r"""
# Materials selection & Ashby charts

With metals, ceramics, polymers and composites on the table, **how do you
choose?** The **Ashby method** (Cambridge) makes selection systematic via
**material property charts** and **performance indices**.

A performance index is a material-property group that, when maximised, optimises a
design objective under a constraint. The derivation: write the objective (e.g.
mass), substitute the constraint (e.g. required stiffness), and collect the
material terms.

- **Stiff, light tie-rod:** maximise $E/\rho$.
- **Stiff, light beam (bending):** maximise $E^{1/2}/\rho$.
- **Strong, light beam:** maximise $\sigma_y^{2/3}/\rho$.

On a log-log $E$ vs $\rho$ chart, a line of slope 2 represents constant
$E^{1/2}/\rho$; sliding it toward the top-left picks the best materials for a light
stiff beam:

```plot
{"title": "Ashby selection line: constant E^(1/2)/rho (log axes)", "xLabel": "density rho (rel.)", "yLabel": "modulus E (rel.)", "xRange": [1, 10], "yRange": [1, 100], "grid": true, "functions": [{"expr": "x^2", "label": "guideline slope 2: E = C*rho^2 (beam index)", "color": "#16a34a"}]}
```

```python
import numpy as np
mats = ["steel", "Al alloy", "CFRP", "wood"]
E    = np.array([200., 70., 120., 12.])    # GPa
rho  = np.array([7.85, 2.7, 1.6, 0.6])     # g/cm^3
index = np.sqrt(E) / rho                    # light stiff beam index
for m, i in sorted(zip(mats, index), key=lambda p: -p[1]):
    print(f"{m:9s}  E^0.5/rho = {i:.2f}")
# higher index -> lighter beam at equal stiffness
```

Selection also weighs cost, manufacturability, corrosion and recyclability —
multi-objective trade-offs that modern tools (CES, Granta) and optimisation
handle. The final lesson takes this to computation and ML.

**Next:** computing and discovering materials — DFT, CALPHAD, ICME and ML.
""",
        ),
        _t(
            "Computational & ML materials discovery",
            "13 min",
            r"""
# Computational & ML materials discovery

The state of the art designs materials **in silico** before any furnace runs,
spanning length scales — the **ICME** (Integrated Computational Materials
Engineering) vision.

- **DFT (density functional theory)** — quantum, ab-initio properties (elastic
  constants, formation energies) from electronic structure.
- **MD (molecular dynamics)** — atomistic dynamics, defects, diffusion.
- **CALPHAD** — thermodynamic phase-diagram modelling for multicomponent alloys.
- **Phase-field / FEM** — microstructure evolution and part-scale behaviour.

```mermaid
flowchart LR
  DFT["DFT / MD (atomic)"] --> CAL["CALPHAD (phases)"]
  CAL --> PF["Phase-field (microstructure)"]
  PF --> FEM["FEM / crystal plasticity (part)"]
  FEM --> PERF["Performance prediction"]
```

The new layer is **machine learning**: train a **surrogate model** on simulated
or measured data, then screen millions of candidates fast, and close the loop with
**Bayesian optimisation / active learning** to choose the next experiment. The
payoff is rapid convergence to an optimum with few costly evaluations:

```plot
{"title": "Active-learning convergence: error vs iterations", "xLabel": "design iteration", "yLabel": "property error (rel.)", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "error ~ exp(-0.4 * iter)", "color": "#16a34a"}]}
```

A minimal property-prediction surrogate over a composition feature set:

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
# features: [%Cr, %Ni, %C, grain_size_um]; target: yield strength (MPa)
X = np.array([[18,8,0.08,30],[12,1,0.20,15],[0,0,0.40,10],[10,0,0.05,50]])
y = np.array([310., 450., 600., 280.])
model = RandomForestRegressor(n_estimators=200, random_state=0).fit(X, y)
cand = np.array([[14, 4, 0.15, 12]])          # a new candidate composition
print(f"predicted yield strength = {model.predict(cand)[0]:.0f} MPa")
# screen 1e6 such candidates, then run DFT/experiment only on the top few
```

This data-driven, multiscale loop — DFT/CALPHAD physics feeding ML surrogates and
optimisation — is how new alloys, batteries and high-entropy materials are now
discovered.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


MATERIALS_SCIENCE_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["MATERIALS_SCIENCE_COURSES"]
