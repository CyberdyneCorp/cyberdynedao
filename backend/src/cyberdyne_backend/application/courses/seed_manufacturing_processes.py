"""Manufacturing Processes track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on how parts are made: from casting
and bulk/sheet forming through machining, joining and welding, up to process
selection, tolerancing, cost modelling and design for manufacturing. Lessons are
`text` with LaTeX, interactive ```plot blocks (force, temperature, tool life,
cost curves), ```mermaid process/decision diagrams, and ```python/```matlab code
for cutting-force, tool-life and process-optimisation calculations.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Manufacturing Processes — Basics ─────────────────────────────────────────

_BASICS = SeedCourse(
    slug="manufacturing-processes-basics",
    title="Manufacturing Processes — Basics",
    description=(
        "An intuitive tour of how engineering parts are produced. We classify "
        "the major process families, then build physical intuition for casting, "
        "bulk and sheet forming, material removal by machining, and the main "
        "joining methods. The emphasis is on what each process does, the part "
        "geometries it suits, and the defects to watch for."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The manufacturing process families",
            "10 min",
            r"""
# The manufacturing process families

Manufacturing turns raw material into finished parts. Almost every process
belongs to one of five families: **casting/molding** (pour or inject liquid into
a cavity), **forming/deformation** (plastically reshape solid material),
**machining/material removal** (cut away unwanted material), **joining**
(weld, braze, fasten, bond), and **additive/finishing** (build up layers, or
improve surfaces). Choosing among them depends on geometry, material, tolerance,
production volume and cost.

A useful first split is whether mass is *conserved*, *added*, or *removed*.
Casting and forming conserve mass and waste little material; machining removes
mass (high scrap, but excellent tolerance); additive adds mass layer by layer.

```mermaid
flowchart LR
  R[Raw material] --> C[Casting / Molding]
  R --> F[Forming / Deformation]
  R --> M[Machining / Removal]
  R --> A[Additive]
  C --> J[Joining & Assembly]
  F --> J
  M --> J
  A --> J
  J --> P[Finished product]
```

As volume rises, processes with high tooling cost but low per-part cost
(casting, forming) win; for one-off or prototype parts, machining and additive
dominate because they need little dedicated tooling.

**Next:** how molten metal fills a mold.
""",
        ),
        _t(
            "Casting fundamentals",
            "12 min",
            r"""
# Casting fundamentals

Casting pours molten metal into a mold cavity and lets it solidify. Sand
casting, investment casting and die casting differ in the mold, but the physics
is shared: fill the cavity completely, feed shrinkage, and control cooling so the
microstructure and dimensions come out right.

Solidification time scales with the part's volume-to-surface ratio. **Chvorinov's
rule** captures this:

$$t_s = B\left(\frac{V}{A}\right)^n$$

where $V/A$ is the casting modulus, $n \approx 2$, and $B$ is a mold constant.
Thick sections solidify last, so risers (feeders) must stay molten longer than
the part to feed shrinkage and avoid internal voids.

Liquid-to-solid shrinkage is typically a few percent (steel ~2.5-3% solidification
shrinkage plus ~7% liquid contraction), so patterns are oversized using a
**shrink rule**.

```plot
{"title": "Solidification time vs casting modulus (Chvorinov)", "xLabel": "V/A modulus (cm)", "yLabel": "solidification time (s)", "xRange": [0, 5], "yRange": [0, 250], "grid": true, "functions": [{"expr": "10*x^2", "label": "t_s = B(V/A)^2", "color": "#2563eb"}]}
```

Common defects: **porosity** (trapped gas or shrinkage), **misruns/cold shuts**
(metal froze before filling), and **hot tears** (cracks from restrained
contraction). Good gating, venting and riser design prevent most of them.

**Next:** reshaping solid metal by forming.
""",
        ),
        _t(
            "Bulk and sheet forming",
            "12 min",
            r"""
# Bulk and sheet forming

Forming plastically deforms solid metal above its yield stress without melting.
**Bulk forming** (forging, rolling, extrusion, drawing) imposes large
three-dimensional strains; **sheet forming** (bending, deep drawing, stamping)
works thin stock where the thickness stays roughly constant.

The flow stress of most metals rises with plastic strain — **strain hardening** —
following a power law:

$$\sigma = K\,\varepsilon^{n}$$

where $K$ is the strength coefficient and $n$ the strain-hardening exponent.
A larger $n$ spreads deformation and improves formability (it delays necking; in
tension, necking begins near $\varepsilon = n$).

```plot
{"title": "Flow stress: strength coefficient and strain hardening", "xLabel": "true strain ε", "yLabel": "flow stress σ (MPa)", "xRange": [0, 0.6], "yRange": [0, 700], "grid": true, "functions": [{"expr": "600*x^0.25", "label": "σ = K ε^n, n=0.25", "color": "#2563eb"}, {"expr": "600*x^0.5", "label": "n=0.5 (more formable)", "color": "#16a34a"}]}
```

Hot working (above recrystallization) lowers forces and erases hardening but
gives a rougher, oxidized surface; cold working raises strength and surface
finish but needs higher forces and may require annealing between steps. Sheet
limits are mapped on a **forming limit diagram (FLD)**, beyond which the sheet
necks or tears.

**Next:** cutting material away by machining.
""",
        ),
        _t(
            "Machining: turning, milling, drilling",
            "12 min",
            r"""
# Machining: turning, milling, drilling

Machining removes material with a hard cutting tool to reach tight tolerances and
fine finishes that casting and forming cannot. The three workhorses are
**turning** (rotating workpiece, single-point tool), **milling** (rotating
multi-tooth cutter, stationary work) and **drilling** (rotating drill makes
holes).

The key kinematic variable is **cutting speed** $v_c$, the surface speed at the
cut. For turning a diameter $D$ at spindle speed $N$:

$$v_c = \pi D N$$

Material is removed at the **material removal rate (MRR)**. In turning,
$\mathrm{MRR} = v_c\, f\, d$, where $f$ is the feed and $d$ the depth of cut.
Higher MRR means faster production but more heat and faster tool wear.

```mermaid
flowchart LR
  W[Workpiece] --> T[Turning: round parts]
  W --> M[Milling: flats, slots, pockets]
  W --> D[Drilling: holes]
  T --> S[Surface finish + tolerance]
  M --> S
  D --> S
```

Most cutting energy becomes heat at the tool-chip interface, so coolant and the
right tool material (HSS, carbide, ceramic, CBN) matter. Surface finish improves
with smaller feed and larger tool nose radius; roughly $R_a \approx f^2/(32 r)$.

**Next:** putting parts together by joining.
""",
        ),
        _t(
            "Joining and assembly overview",
            "11 min",
            r"""
# Joining and assembly overview

Few products are a single part; most are assemblies joined by **welding**
(fusion or solid-state), **brazing/soldering** (a lower-melting filler wets the
joint without melting the base), **adhesive bonding**, or **mechanical
fastening** (bolts, rivets, snap-fits). Joints are classified as *permanent*
(weld, rivet, adhesive) or *removable* (bolt, screw).

Fusion welding melts the base metals together, creating a **fusion zone** and a
surrounding **heat-affected zone (HAZ)** whose microstructure — and often
strength — is altered by the thermal cycle. The heat input per unit length,

$$H = \frac{\eta\,V I}{v}$$

(arc efficiency $\eta$, voltage $V$, current $I$, travel speed $v$), governs
penetration, HAZ size and residual stress.

```mermaid
flowchart TB
  J[Joining] --> P[Permanent]
  J --> R[Removable]
  P --> W[Welding]
  P --> B[Brazing / Soldering]
  P --> A[Adhesive bonding]
  R --> F[Bolts / Screws]
  R --> S[Snap-fits]
```

Choosing a method trades strength, sealing, disassembly, cost and material
compatibility: welding suits load-bearing steel structures; adhesives join
dissimilar or thin materials and spread stress; bolts allow service and
disassembly.

**Next:** match each process to the right part.
""",
        ),
        _t(
            "Matching process to part",
            "10 min",
            r"""
# Matching process to part

No process is best for everything. Selection balances **geometry** (size,
complexity, wall thickness), **material**, **tolerance and finish**, **production
volume**, and **cost**. The dominant lever is usually volume, because tooling
cost is amortized over the batch.

A simple cost model splits **fixed tooling cost** $C_t$ over a quantity $Q$ plus a
**variable per-part cost** $c_v$:

$$C_{\text{unit}} = c_v + \frac{C_t}{Q}$$

Die casting and stamping have large $C_t$ but tiny $c_v$, so unit cost falls fast
with volume; machining and additive have near-zero $C_t$ but high $c_v$, so they
win only at low volume. The crossover sets the **break-even quantity**.

```plot
{"title": "Unit cost vs volume: low-tooling vs high-tooling process", "xLabel": "quantity Q", "yLabel": "unit cost (currency)", "xRange": [1, 1000], "yRange": [0, 120], "grid": true, "functions": [{"expr": "80 + 200/x", "label": "machining (high c_v, low C_t)", "color": "#dc2626"}, {"expr": "10 + 20000/x", "label": "die casting (low c_v, high C_t)", "color": "#2563eb"}]}
```

Rules of thumb: high volume + complex shape -> casting or molding; sheet parts
in volume -> stamping; tight tolerance features -> finish-machine; one-offs or
internal channels -> additive. Real selection iterates these against tolerance
and material limits.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


# ── Manufacturing Processes — Intermediate ───────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="manufacturing-processes-intermediate",
    title="Manufacturing Processes — Intermediate",
    description=(
        "The core quantitative methods of manufacturing. We model solidification "
        "and feeding in casting, compute forces and energy in forming, derive "
        "cutting mechanics and Taylor tool life for machining, analyse the weld "
        "thermal cycle, and set up tolerances and process capability with "
        "worked code in Python and MATLAB."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Solidification, feeding and riser design",
            "13 min",
            r"""
# Solidification, feeding and riser design

A sound casting needs the riser (feeder) to freeze *after* the section it feeds,
so liquid metal keeps flowing into shrinkage cavities. Using **Chvorinov's rule**
$t_s = B(V/A)^2$, the design criterion is simply that the riser modulus exceeds
the casting modulus, in practice $M_r \ge 1.2\,M_c$ where $M = V/A$.

```plot
{"title": "Riser must out-last the casting it feeds", "xLabel": "casting modulus M_c (cm)", "yLabel": "required riser solidification time (s)", "xRange": [0, 4], "yRange": [0, 300], "grid": true, "functions": [{"expr": "15*x^2", "label": "casting t_s", "color": "#2563eb"}, {"expr": "15*(1.2*x)^2", "label": "riser t_s (1.2 x modulus)", "color": "#dc2626"}]}
```

We can size a cylindrical riser numerically by matching its modulus to the
target:

```python
import numpy as np

def cylinder_modulus(d, h):
    V = np.pi * d**2 / 4 * h
    A = np.pi * d * h + 2 * (np.pi * d**2 / 4)  # side + two ends
    return V / A

M_casting = 1.0          # cm, plate section modulus
M_target = 1.2 * M_casting
# search riser diameter for a riser with h = d (compact, low surface area)
for d in np.linspace(2, 12, 1001):
    if cylinder_modulus(d, d) >= M_target:
        print(f"riser d = h = {d:.2f} cm, modulus = {cylinder_modulus(d, d):.2f} cm")
        break
```

The riser must also hold enough volume to feed the shrinkage; both the
*freezing-time* and *volume* criteria must pass. Directional solidification —
toward the riser — is encouraged with chills and tapered sections.

**Next:** forces and energy in forming.
""",
        ),
        _t(
            "Forming forces and energy",
            "13 min",
            r"""
# Forming forces and energy

To form a part you must supply enough force to exceed flow stress over the
contact area, and enough energy to drive the plastic strain. For uniform
upsetting (open-die compression) of a cylinder, friction at the die faces raises
the average pressure above the flow stress — the **friction hill**:

$$p_{\text{avg}} = \bar\sigma_f\left(1 + \frac{\mu d}{3h}\right)$$

with friction coefficient $\mu$, instantaneous diameter $d$ and height $h$. The
forging force is $F = p_{\text{avg}}\,A$, and the **ideal plastic work per unit
volume** is $u = \int \sigma\, d\varepsilon = K\varepsilon^{n+1}/(n+1)$.

```plot
{"title": "Forging pressure rises with d/h (friction hill)", "xLabel": "aspect ratio d/h", "yLabel": "p_avg / flow stress", "xRange": [0, 12], "yRange": [1, 4], "grid": true, "functions": [{"expr": "1 + 0.2*x/3", "label": "μ = 0.2", "color": "#2563eb"}, {"expr": "1 + 0.4*x/3", "label": "μ = 0.4", "color": "#dc2626"}]}
```

```python
import numpy as np

K, n = 600e6, 0.25      # Pa, strain-hardening exponent (annealed steel-ish)
mu = 0.2
d0, h0 = 0.05, 0.05     # m, initial billet
h = 0.03                # m, current height
eps = np.log(h0 / h)    # true (compressive) strain
d = d0 * np.sqrt(h0 / h)            # volume constancy
sigma_f = K * eps**n                # flow stress at this strain
p_avg = sigma_f * (1 + mu * d / (3 * h))
F = p_avg * (np.pi * d**2 / 4)
print(f"strain={eps:.3f}  flow stress={sigma_f/1e6:.0f} MPa  force={F/1e3:.0f} kN")
```

Real presses must supply the *peak* force at the end of the stroke. Lubrication
(lowering $\mu$) and hot working (lowering $\bar\sigma_f$) cut both force and
energy.

**Next:** the mechanics of metal cutting.
""",
        ),
        _t(
            "Metal cutting mechanics",
            "13 min",
            r"""
# Metal cutting mechanics

Orthogonal cutting models the chip as shearing along a thin **shear plane** at
angle $\phi$. From the uncut and chip thicknesses, the **chip thickness ratio**
$r = t_o/t_c \le 1$ gives the shear angle via the rake angle $\alpha$:

$$\tan\phi = \frac{r\cos\alpha}{1 - r\sin\alpha}$$

The cutting force, multiplied by speed, gives the power. The **specific cutting
energy** $u_s$ (energy per unit volume removed) lets you estimate power directly:
$P = u_s \cdot \mathrm{MRR}$.

```python
import numpy as np

t_o, t_c = 0.25e-3, 0.50e-3     # m, uncut and chip thickness
alpha = np.deg2rad(10)          # rake angle
r = t_o / t_c
phi = np.arctan(r * np.cos(alpha) / (1 - r * np.sin(alpha)))
gamma = 1 / np.tan(phi) + np.tan(phi - alpha)   # shear strain
print(f"chip ratio r={r:.2f}  shear angle phi={np.rad2deg(phi):.1f} deg  shear strain={gamma:.2f}")

# Power from specific cutting energy
u_s = 2.5e9          # J/m^3 for steel (~2.5 GPa)
vc = 2.0             # m/s cutting speed
f, d = 0.25e-3, 2e-3 # feed (m), depth (m)
MRR = vc * f * d
print(f"MRR={MRR*1e6:.1f} cm^3/s  power={u_s*MRR/1e3:.2f} kW")
```

A larger (more positive) rake angle raises $\phi$, thins the chip and lowers
force, but weakens the cutting edge. Most cutting energy converts to heat at the
shear plane and the tool-chip rake face, which drives tool wear.

```plot
{"title": "Higher chip ratio means a larger shear angle (alpha=10deg)", "xLabel": "chip thickness ratio r", "yLabel": "shear angle phi (rad)", "xRange": [0.1, 0.95], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "atan(r*cos(0.1745)/(1 - r*sin(0.1745)))", "label": "phi(r)", "color": "#2563eb"}], "rename": {"r": "x"}}
```

**Next:** how long the tool lasts.
""",
        ),
        _t(
            "Tool life and Taylor's equation",
            "12 min",
            r"""
# Tool life and Taylor's equation

Tools wear as they cut; cutting speed is by far the strongest driver. **Taylor's
tool-life equation** captures this empirically:

$$v_c\,T^{\,n} = C$$

where $T$ is tool life (min), $v_c$ cutting speed, $n$ the Taylor exponent
(~0.1-0.2 HSS, ~0.2-0.4 carbide, ~0.4-0.6 ceramic) and $C$ a constant equal to
the speed giving one-minute life. Doubling speed can cut tool life by an order of
magnitude.

```plot
{"title": "Taylor tool life: speed vs life (log-shaped)", "xLabel": "cutting speed v_c (m/min)", "yLabel": "tool life T (min)", "xRange": [60, 300], "yRange": [0, 120], "grid": true, "functions": [{"expr": "(300/x)^5", "label": "carbide, n=0.2, C=300", "color": "#2563eb"}, {"expr": "(300/x)^10", "label": "HSS, n=0.1", "color": "#dc2626"}]}
```

The extended form adds feed $f$ and depth $d$:
$v_c\,T^{n} f^{a} d^{b} = C$. Fitting $n$ and $C$ from two tests is a linear
regression in log space:

```python
import numpy as np

# two cutting tests: (speed m/min, life min)
v1, T1 = 150, 60
v2, T2 = 250, 8
# v T^n = C  ->  ln v = ln C - n ln T
n = (np.log(v2) - np.log(v1)) / (np.log(T1) - np.log(T2))
C = v1 * T1**n
print(f"Taylor n = {n:.3f}, C = {C:.0f}")
# predict life at a new speed
v_new = 200
T_new = (C / v_new)**(1 / n)
print(f"at {v_new} m/min, expected life = {T_new:.1f} min")
```

Optimum speed trades tool cost and change time against machining time, giving a
**minimum-cost** and a **maximum-production** speed that bracket the operating
window.

**Next:** the weld thermal cycle.
""",
        ),
        _t(
            "Weld thermal cycle and heat input",
            "12 min",
            r"""
# Weld thermal cycle and heat input

Welding is a moving heat source. The **net heat input per unit length**
$H = \eta VI/v$ (arc efficiency $\eta$, voltage $V$, current $I$, travel speed
$v$) sets penetration, the size of the heat-affected zone (HAZ), and the cooling
rate. Faster cooling (high $v$, thick plate) hardens steel HAZs and risks
cracking; slower cooling coarsens grains.

The Rosenthal solution gives the peak temperature and cooling rate; engineers
often track the **cooling time from 800 to 500 deg C** ($t_{8/5}$), which
correlates with HAZ hardness. A thick-plate cooling rate at temperature $T$ scales
as $R \propto (T - T_0)^2 / H$.

```plot
{"title": "Weld point cooling: damped thermal decay", "xLabel": "time after pass (s)", "yLabel": "relative temperature", "xRange": [0, 30], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.2*x)", "label": "low heat input (fast cool)", "color": "#dc2626"}, {"expr": "exp(-0.1*x)", "label": "high heat input (slow cool)", "color": "#2563eb"}]}
```

```matlab
% Heat input and a thick-plate cooling-rate estimate
eta = 0.8; V = 25; I = 250; v = 5e-3;   % arc eff, volts, amps, m/s
H = eta * V * I / v;                     % J/m net heat input
fprintf('Heat input H = %.0f kJ/m\n', H/1e3);

% Rosenthal thick-plate cooling rate at T (deg C), 2-D conduction
k = 50; T0 = 25; T = 650;                % W/mK, preheat, temperature
R = 2*pi*k*(T - T0)^2 / H;               % deg C/s
fprintf('Cooling rate at %d C = %.1f C/s\n', T, R);
```

Preheat raises $T_0$, slowing cooling and reducing cracking in hardenable steels.
Heat input also drives **residual stress** and distortion, controlled by joint
design, clamping and weld sequence.

**Next:** tolerances and process capability.
""",
        ),
        _t(
            "Tolerances and process capability",
            "12 min",
            r"""
# Tolerances and process capability

A drawing specifies a nominal dimension with a **tolerance**; the process must
hold it. The link between a process's natural spread and the tolerance band is
the **capability index**. For a centered process,

$$C_p = \frac{\text{USL} - \text{LSL}}{6\sigma}, \qquad
C_{pk} = \min\!\left(\frac{\text{USL}-\mu}{3\sigma},\ \frac{\mu-\text{LSL}}{3\sigma}\right)$$

$C_p$ compares tolerance width to six standard deviations; $C_{pk}$ penalises a
shifted mean. $C_{pk} \ge 1.33$ is a common target (about 30 ppm defects).

```python
import numpy as np

USL, LSL = 10.05, 9.95          # mm spec limits
mu, sigma = 10.01, 0.012        # measured mean and std (mm)
Cp  = (USL - LSL) / (6 * sigma)
Cpk = min((USL - mu) / (3 * sigma), (mu - LSL) / (3 * sigma))
print(f"Cp = {Cp:.2f}, Cpk = {Cpk:.2f}")
# expected fraction out of spec (normal model)
from math import erf, sqrt
def tail(z): return 0.5 * (1 - erf(z / sqrt(2)))
ppm = 1e6 * (tail((USL - mu)/sigma) + tail((mu - LSL)/sigma))
print(f"expected defects ~ {ppm:.0f} ppm")
```

```plot
{"title": "Process distribution inside the tolerance band", "xLabel": "deviation from mean (in sigma)", "yLabel": "probability density", "xRange": [-4, 4], "yRange": [0, 0.45], "grid": true, "functions": [{"expr": "exp(-x^2/2)/sqrt(2*3.14159)", "label": "process spread", "color": "#2563eb"}]}
```

Tighter tolerances need either a more capable (lower $\sigma$) process or a
costlier finishing step, so tolerances should be no tighter than the function
requires.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


# ── Manufacturing Processes — Advanced ───────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="manufacturing-processes-advanced",
    title="Manufacturing Processes — Advanced",
    description=(
        "State-of-the-art and applied manufacturing: numerical process "
        "simulation (casting and forming FEM), additive manufacturing physics, "
        "machining-parameter and cost optimisation, statistical design of "
        "experiments and machine-learning surrogates for process windows, and a "
        "design-for-manufacturing capstone. Worked Python/MATLAB throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Process simulation: casting and forming FEM",
            "14 min",
            r"""
# Process simulation: casting and forming FEM

Modern process engineering predicts defects before cutting steel using numerical
simulation. Casting solvers couple fluid flow (Navier-Stokes filling) with
solidification (the heat equation plus a latent-heat source), flagging cold shuts
and shrinkage porosity. Forming solvers use large-deformation **finite-element
analysis** with elastoplastic flow rules to predict forces, fold/lap defects and
springback.

The governing transient heat equation with phase change is

$$\rho c_p \frac{\partial T}{\partial t} = \nabla\!\cdot(k\nabla T) + \dot q_L$$

where $\dot q_L$ releases latent heat over the freezing range. A 1-D explicit
finite-difference march illustrates the solidification front:

```python
import numpy as np

L, nx, dt, steps = 0.05, 50, 0.05, 4000
dx = L / nx
alpha = 5e-6                      # thermal diffusivity m^2/s
T = np.full(nx, 1550.0)          # molten, deg C
T_mold = 25.0
r = alpha * dt / dx**2
assert r <= 0.5, "explicit scheme unstable"     # stability criterion
for _ in range(steps):
    Tn = T.copy()
    T[1:-1] = Tn[1:-1] + r * (Tn[2:] - 2*Tn[1:-1] + Tn[:-2])
    T[0] = T_mold                # chilled mold wall
    T[-1] = Tn[-2]              # insulated centre
front = np.argmax(T > 1450)     # crude solidus front index
print(f"solidified shell ~ {front*dx*1e3:.1f} mm after {steps*dt:.0f} s")
```

```plot
{"title": "Solidified shell thickness grows with sqrt(time)", "xLabel": "time (s)", "yLabel": "shell thickness (mm)", "xRange": [0, 200], "yRange": [0, 40], "grid": true, "functions": [{"expr": "3*sqrt(x)", "label": "shell ~ k sqrt(t)", "color": "#2563eb"}]}
```

Mesh refinement, accurate material data and validated boundary conditions decide
whether a simulation is predictive or merely pretty.

**Next:** the physics of additive manufacturing.
""",
        ),
        _t(
            "Additive manufacturing physics",
            "13 min",
            r"""
# Additive manufacturing physics

Powder-bed fusion (laser/electron beam) and directed energy deposition build
parts by melting metal track by track. The single most useful scalar is the
**volumetric energy density**:

$$E_v = \frac{P}{v\,h\,t}$$

with laser power $P$, scan speed $v$, hatch spacing $h$ and layer thickness $t$.
Too low $E_v$ leaves **lack-of-fusion** voids; too high causes **keyholing** and
gas porosity. A printable **process window** lives between these bounds.

```plot
{"title": "Process window: relative density vs energy density", "xLabel": "volumetric energy density (J/mm^3)", "yLabel": "relative density (%)", "xRange": [20, 120], "yRange": [90, 101], "grid": true, "functions": [{"expr": "100 - 0.01*(x-70)^2", "label": "density(E_v)", "color": "#2563eb"}]}
```

```python
import numpy as np

def energy_density(P, v, h, t):
    return P / (v * h * t)           # W / (mm/s * mm * mm) = J/mm^3

# sweep speed at fixed power and find the in-window band (60-90 J/mm^3)
P, h, t = 200.0, 0.10, 0.03          # W, mm, mm
for v in np.arange(400, 1600, 100):  # mm/s
    Ev = energy_density(P, v, h, t)
    tag = "OK" if 60 <= Ev <= 90 else "out"
    print(f"v={v:4.0f} mm/s  E_v={Ev:5.1f} J/mm^3  [{tag}]")
```

Rapid solidification gives fine microstructures but steep thermal gradients and
**residual stress** that warp parts and demand support structures or stress
relief. Post-processing (HIP to close pores, machining critical surfaces) is
usually part of the AM workflow, not optional.

**Next:** optimising machining parameters and cost.
""",
        ),
        _t(
            "Machining parameter and cost optimization",
            "13 min",
            r"""
# Machining parameter and cost optimization

Choosing cutting speed is an optimisation: faster cutting reduces machining time
but shortens tool life, adding tool and change-over cost. The **cost per part**
combines machining, tool-change and tooling costs. Using Taylor's
$v_c T^n = C$, the **minimum-cost cutting speed** has a closed form:

$$v_{\text{opt}} = C\left[\frac{n}{(1-n)}\,\frac{C_m}{t_c\,C_m + C_t}\right]^{n}$$

where $C_m$ is machine+labour rate, $t_c$ tool-change time and $C_t$ tooling cost
per edge. The cost curve is convex, so a clear optimum exists.

```plot
{"title": "Cost per part is convex in cutting speed", "xLabel": "cutting speed (relative)", "yLabel": "cost per part (relative)", "xRange": [0.3, 2.0], "yRange": [0, 5], "grid": true, "functions": [{"expr": "1/x + 0.6*x^4", "label": "machining + tool cost", "color": "#2563eb"}]}
```

```python
import numpy as np
from scipy.optimize import minimize_scalar

n, C = 0.25, 350.0           # Taylor params (m/min)
Cm = 1.0                     # machine+labour cost rate (per min)
tc = 2.0                     # tool change time (min)
Ct = 4.0                     # tooling cost per edge
L, f = 200.0, 0.25           # cut length (mm), feed (mm/rev) -> time proxy

def cost(vc):
    T = (C / vc)**(1 / n)            # tool life (min)
    t_mach = L / (vc * f)            # machining time (min) proxy
    return Cm * t_mach + (t_mach / T) * (tc * Cm + Ct)

res = minimize_scalar(cost, bounds=(50, 400), method="bounded")
print(f"optimal v_c = {res.x:.0f} m/min, cost = {res.fun:.3f} per part")
```

In practice the optimum is bracketed by **minimum-cost** and **maximum-
production** speeds; modern CAM and adaptive controllers push toward this window
while respecting power, chatter and surface-finish constraints.

**Next:** designing experiments and ML process models.
""",
        ),
        _t(
            "Design of experiments and ML process models",
            "14 min",
            r"""
# Design of experiments and ML process models

Process windows depend on many coupled parameters, so brute-force trials are
expensive. **Design of experiments (DOE)** — full/fractional factorials,
response-surface and Taguchi designs — extracts the most information from the
fewest runs by varying factors systematically. A second-order **response
surface** fits a quadratic model

$$y = \beta_0 + \sum_i \beta_i x_i + \sum_i \beta_{ii} x_i^2 + \sum_{i<j}\beta_{ij} x_i x_j$$

and locates the optimum analytically. Increasingly, **machine-learning
surrogates** (Gaussian-process regression, gradient boosting) model the
process from experimental + simulation data, and **Bayesian optimisation** picks
the next experiment to run.

```plot
{"title": "Surrogate model converges toward the true optimum", "xLabel": "experiment / iteration", "yLabel": "best objective so far (relative)", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "optimality gap", "color": "#16a34a"}]}
```

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# DOE: speed and feed (coded -1..+1), measured surface roughness Ra
X = np.array([[-1,-1],[1,-1],[-1,1],[1,1],[0,0],[1,0],[0,1]], float)
Ra = np.array([0.8, 1.4, 1.1, 2.0, 1.0, 1.6, 1.3])
poly = PolynomialFeatures(degree=2, include_bias=False)
Xp = poly.fit_transform(X)
model = LinearRegression().fit(Xp, Ra)
print("R^2 =", round(model.score(Xp, Ra), 3))
# predict roughness at mid speed, low feed
print("Ra pred:", round(model.predict(poly.transform([[0, -1]]))[0], 2))
```

The payoff is a validated, low-cost **process model** that predicts quality,
defines robust operating windows, and feeds closed-loop control.

**Next:** turning it into design rules.
""",
        ),
        _t(
            "Design for manufacturing and assembly",
            "13 min",
            r"""
# Design for manufacturing and assembly

**Design for Manufacturing and Assembly (DFMA)** moves cost decisions upstream:
70-80% of a product's cost is locked in at design. The principles are simple but
powerful — minimise part count, design for the chosen process, use standard
features and fasteners, and ease assembly (symmetry, self-location, top-down
insertion).

The **Boothroyd-Dewhurst** method scores a design's assembly efficiency:

$$\eta_{\text{assy}} = \frac{N_{\min}\,t_a}{T_{\text{assy}}}$$

where $N_{\min}$ is the theoretical minimum number of parts (a part must move
relative to its neighbours, be of different material, or need separation for
assembly — otherwise combine it), $t_a$ an ideal handling+insertion time, and
$T_{\text{assy}}$ the actual time. Low efficiency flags parts to merge.

```mermaid
flowchart TB
  S[Design intent] --> Q1{Must it move<br/>relative to others?}
  Q1 -- no --> Q2{Different material<br/>required?}
  Q1 -- yes --> K[Keep as separate part]
  Q2 -- no --> Q3{Needed for<br/>assembly/service?}
  Q2 -- yes --> K
  Q3 -- no --> C[Candidate to combine]
  Q3 -- yes --> K
```

```python
# Boothroyd-Dewhurst assembly efficiency
N_min = 4          # theoretical minimum parts
t_a = 3.0          # ideal time per part (s)
T_assy = 38.0      # actual total assembly time (s)
eta = N_min * t_a / T_assy
print(f"Design efficiency = {eta*100:.0f}%  (>60% is good; redesign if low)")
```

Coupled with **GD&T** (ISO 1101 / ASME Y14.5) to communicate functional
tolerances and tolerance stack-up analysis, DFMA turns process knowledge into
designs that are cheaper, faster and more reliable to make.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


MANUFACTURING_PROCESSES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MANUFACTURING_PROCESSES_COURSES"]
