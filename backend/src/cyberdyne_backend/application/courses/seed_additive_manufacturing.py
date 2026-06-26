"""Additive Manufacturing track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on 3D printing. Starts from AM
principles, the seven ASTM/ISO process families and the FFF/SLA workflow; moves
through powder-bed fusion (SLS/DMLS), thermal physics, materials and process
parameters; and ends with design for additive manufacturing (DfAM), lattices,
topology optimization, supports, slicing and build-prep. Lessons are `text`
with LaTeX, interactive ```plot blocks (thermal, mechanical, cost and
optimization curves), ```mermaid process/workflow diagrams and runnable
```python/```matlab snippets for slicing, thermal and lattice computations.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Additive Manufacturing — Basics ──────────────────────────────────────────

_BASICS = SeedCourse(
    slug="additive-manufacturing-basics",
    title="Additive Manufacturing — Basics",
    description=(
        "The foundations of additive manufacturing: what 'building layer by "
        "layer' means, the seven ASTM/ISO process families, and a hands-on "
        "tour of the two most accessible processes — fused filament "
        "fabrication (FFF) and stereolithography (SLA). Covers the digital "
        "thread (CAD -> STL -> slicer -> G-code), layer height and resolution, "
        "and basic part quality. Interactive plots and process diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is additive manufacturing?",
            "10 min",
            r"""
# What is additive manufacturing?

**Additive manufacturing (AM)**, commonly called 3D printing, builds a part by
adding material **layer upon layer** directly from a 3D model — the opposite of
**subtractive** machining (milling, turning), which removes material from a
billet, and **formative** processes (casting, forging) that shape it in a mould.
The standard ISO/ASTM 52900 defines AM and its vocabulary.

Why does it matter? AM's cost is largely **decoupled from geometric
complexity**: an internal cooling channel or a lattice costs little more to print
than a solid block, whereas every undercut adds machining setups. This enables
part consolidation, lightweighting and one-off customization.

```mermaid
flowchart LR
  CAD["3D CAD model"] --> MESH["Tessellate -> STL / 3MF"]
  MESH --> SLICE["Slice into layers + toolpaths"]
  SLICE --> GCODE["Machine instructions (G-code)"]
  GCODE --> BUILD["Build layer by layer"]
  BUILD --> POST["Post-process: support removal, cure, finish"]
```

The trade-off appears in **build time**, which scales roughly with the number of
layers and therefore with part height $H$ divided by layer thickness $t$. Thinner
layers give finer detail but multiply the layer count:

```plot
{"title": "Layers vs layer thickness for a 50 mm part", "xLabel": "layer thickness t (mm)", "yLabel": "number of layers", "xRange": [0.05, 0.4], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "50/x", "label": "N = H/t (H = 50 mm)", "color": "#2563eb"}]}
```

**Next:** the seven process families that organize all AM technologies.
""",
        ),
        _t(
            "The seven AM process families",
            "11 min",
            r"""
# The seven AM process families

ISO/ASTM 52900 groups every AM technology into **seven families** by how
material is deposited and fused. Knowing the family tells you the feedstock,
typical materials and the dominant physics.

```mermaid
flowchart TB
  AM["Additive manufacturing (ISO/ASTM 52900)"] --> ME["Material extrusion (FFF/FDM)"]
  AM --> VP["Vat photopolymerization (SLA/DLP)"]
  AM --> PBF["Powder bed fusion (SLS/SLM/DMLS/EBM)"]
  AM --> MJ["Material jetting (PolyJet)"]
  AM --> BJ["Binder jetting"]
  AM --> DED["Directed energy deposition (LMD/WAAM)"]
  AM --> SL["Sheet lamination (LOM)"]
```

- **Material extrusion** — a heated nozzle lays molten thermoplastic beads
  (cheap, ubiquitous).
- **Vat photopolymerization** — a laser or projector cures liquid resin
  (smooth, high detail).
- **Powder bed fusion** — a laser/electron beam sinters or melts a powder bed
  (functional metals and polymers).
- **Material jetting** — droplets of photopolymer are jetted and UV-cured
  (multi-material, full color).
- **Binder jetting** — a liquid binder glues powder; parts are later sintered.
- **Directed energy deposition** — powder/wire is melted as it is deposited
  (repair, large metal parts).
- **Sheet lamination** — sheets are bonded and cut to shape.

Each family occupies a niche in the **resolution vs build-rate** space — finer
features generally mean slower builds:

```plot
{"title": "Resolution vs build rate (qualitative)", "xLabel": "build rate (a.u.)", "yLabel": "min feature size (mm)", "xRange": [0.5, 10], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "1/x", "label": "finer detail costs throughput", "color": "#dc2626"}]}
```

**Next:** how fused filament fabrication actually works.
""",
        ),
        _t(
            "Fused filament fabrication (FFF/FDM)",
            "12 min",
            r"""
# Fused filament fabrication (FFF/FDM)

**FFF** (trademarked FDM by Stratasys) is material extrusion with a
thermoplastic filament. A stepper-driven **extruder** pushes 1.75 mm filament
into a **hot end** where it melts (PLA ~200 °C, ABS ~240 °C, PETG ~235 °C), and a
nozzle (typically 0.4 mm) deposits beads onto a heated bed, layer by layer.

```mermaid
flowchart LR
  SPOOL["Filament spool"] --> EXT["Extruder gear"]
  EXT --> HOT["Hot end (melt zone)"]
  HOT --> NOZ["Nozzle 0.4 mm"]
  NOZ --> BED["Heated bed"]
  BED --> PART["Part built layer by layer"]
```

**Volumetric flow** sets the speed limit. The cross-section of a deposited bead
is roughly layer height $h$ times line width $w$, so for print speed $v$ the
required flow is:

$$\dot{V} = w\,h\,v.$$

A hot end that can only melt ~10 mm³/s caps how fast you can print at a given
layer height. Increase $h$ and the achievable feedrate $v$ for fixed flow drops:

```plot
{"title": "Max print speed vs layer height (flow-limited)", "xLabel": "layer height h (mm)", "yLabel": "max speed v (mm/s)", "xRange": [0.1, 0.4], "yRange": [0, 320], "grid": true, "functions": [{"expr": "10/(0.4*x)", "label": "v = Vdot/(w h), Vdot = 10 mm^3/s, w = 0.4 mm", "color": "#2563eb"}]}
```

Key parameters: **layer height** (detail vs time), **infill** density/pattern
(strength vs weight), **wall/perimeter count**, **print/bed temperature** and
**cooling**. Strength is anisotropic — bonds between layers (Z) are weaker than
beads within a layer (XY), so orientation matters.

**Next:** stereolithography — printing with light-cured resin.
""",
        ),
        _t(
            "Stereolithography (SLA/DLP)",
            "11 min",
            r"""
# Stereolithography (SLA/DLP)

**Vat photopolymerization** cures a liquid **photopolymer resin** with UV light.
In laser **SLA** a galvanometer traces each layer point by point; in **DLP** a
projector flashes a whole layer at once; **masked SLA (mSLA)** uses an LCD mask
over a UV array. Because the spot/pixel is tiny, SLA resolves features far finer
than FFF (25-100 μm layers, sharp edges), at the cost of messy post-processing.

```mermaid
flowchart TB
  RES["Resin vat"] --> EXPOSE["UV exposure cures one layer"]
  EXPOSE --> LIFT["Build platform lifts / peels"]
  LIFT --> RECOAT["Fresh resin flows under part"]
  RECOAT --> EXPOSE
  LIFT --> WASH["Wash (IPA) -> UV post-cure"]
```

Curing follows the **Jacobs working-curve** equation: the cure depth $C_d$ grows
logarithmically with the exposure energy $E$ relative to the resin's critical
energy $E_c$, scaled by the penetration depth $D_p$:

$$C_d = D_p \, \ln\!\left(\frac{E}{E_c}\right).$$

You set exposure so $C_d$ slightly exceeds the layer thickness for good layer
bonding without over-curing. The log shape means doubling exposure adds only a
fixed $D_p\ln 2$ of depth:

```plot
{"title": "Jacobs working curve: cure depth vs exposure", "xLabel": "exposure E (mJ/cm^2)", "yLabel": "cure depth Cd (mm)", "xRange": [5, 60], "yRange": [0, 0.5], "grid": true, "functions": [{"expr": "0.14*log(x/8)", "label": "Cd = Dp ln(E/Ec), Dp = 0.14 mm, Ec = 8", "color": "#16a34a"}]}
```

Workflow: print -> wash in isopropanol -> remove supports -> **UV post-cure** to
reach full mechanical properties.

**Next:** the digital thread — from CAD model to printable G-code.
""",
        ),
        _t(
            "The digital workflow: CAD to G-code",
            "11 min",
            r"""
# The digital workflow: CAD to G-code

Every print travels a **digital thread**. The CAD solid is tessellated into an
**STL** (a triangle mesh of the surface) or the richer **3MF** (units, color,
materials). A **slicer** (Cura, PrusaSlicer, Bambu Studio) intersects the mesh
with horizontal planes, generates **perimeters, infill and supports**, and emits
**G-code** — line-by-line motion and extrusion commands.

```mermaid
flowchart LR
  SOLID["CAD solid (B-rep)"] --> STL["STL mesh (triangles)"]
  STL --> REPAIR["Repair: watertight, normals"]
  REPAIR --> SLICE["Slice + toolpath planning"]
  SLICE --> PREVIEW["Preview / collision check"]
  PREVIEW --> GCODE["G-code"]
```

STL **resolution** is a faceting trade-off: the **chord error** $\delta$ between
a circle of radius $R$ and its flat facet relates to the facet half-angle. For a
segment spanning angle $\theta$:

$$\delta = R\left(1 - \cos\tfrac{\theta}{2}\right).$$

A coarse export shows visible facets; too fine an export bloats the file. A tiny
slicer in Python shows the core idea — intersect each triangle with a Z-plane:

```python
import numpy as np

def slice_layer(triangles, z):
    # Return line segments where mesh triangles cross plane Z = z.
    segments = []
    for tri in triangles:                  # tri: 3x3 array of vertices
        below = tri[:, 2] < z
        if below.all() or (~below).all():
            continue                       # triangle doesn't cross the plane
        pts = []
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            if (a[2] < z) != (b[2] < z):   # edge crosses z
                f = (z - a[2]) / (b[2] - a[2])
                pts.append(a + f * (b - a))
        if len(pts) == 2:
            segments.append((pts[0][:2], pts[1][:2]))
    return segments
```

```plot
{"title": "STL chord (faceting) error vs facet angle, R = 10 mm", "xLabel": "facet angle theta (rad)", "yLabel": "chord error delta (mm)", "xRange": [0.05, 0.8], "yRange": [0, 0.8], "grid": true, "functions": [{"expr": "10*(1-cos(x/2))", "label": "delta = R(1 - cos(theta/2))", "color": "#dc2626"}]}
```

**Next:** quick knowledge check on AM fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Additive Manufacturing — Intermediate ────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="additive-manufacturing-intermediate",
    title="Additive Manufacturing — Intermediate",
    description=(
        "Core quantitative methods for metal and polymer powder-bed fusion. "
        "Covers selective laser sintering (SLS) and laser/electron metal "
        "processes (SLM/DMLS/EBM), the laser-melting energy balance and melt "
        "pool, volumetric energy density and process windows, AM materials and "
        "microstructure, residual stress and distortion, and dimensional "
        "accuracy. Plots, process diagrams and Python/MATLAB models throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Powder bed fusion: SLS, SLM, DMLS, EBM",
            "12 min",
            r"""
# Powder bed fusion: SLS, SLM, DMLS, EBM

**Powder bed fusion (PBF)** spreads a thin powder layer with a recoater, fuses
the cross-section with a focused beam, lowers the build platform and repeats.
The variants differ by material and heat source:

- **SLS** — laser **sinters** polymer powder (nylon PA12); no support needed,
  the powder cake holds the part.
- **SLM / DMLS** — laser **fully melts** metal powder (Ti-6Al-4V, AlSi10Mg,
  316L); requires supports and an inert (Ar/N₂) atmosphere.
- **EBM** — an **electron beam** melts metal in vacuum at high preheat, giving
  low residual stress but coarser resolution.

```mermaid
flowchart LR
  HOPPER["Powder hopper"] --> RECOAT["Recoater spreads layer"]
  RECOAT --> SCAN["Beam scans cross-section -> fuse"]
  SCAN --> LOWER["Platform lowers by layer t"]
  LOWER --> RECOAT
  SCAN --> PART["Fused part in powder bed"]
```

A central parameter is **packing density** of the powder bed; loose powder packs
only ~50-60% of solid, and full melting must close that porosity. Particle size
distribution (PSD), typically 15-45 μm for laser metal AM, governs spreadability
and minimum layer thickness. Build rate rises with layer thickness but at the
cost of resolution and melt stability:

```plot
{"title": "PBF build rate vs layer thickness", "xLabel": "layer thickness t (mm)", "yLabel": "build rate (cm^3/h)", "xRange": [0.02, 0.1], "yRange": [0, 40], "grid": true, "functions": [{"expr": "350*x", "label": "rate ~ hatch x speed x t", "color": "#2563eb"}]}
```

**Next:** the physics of the laser melt pool and energy density.
""",
        ),
        _t(
            "Laser melting physics and energy density",
            "13 min",
            r"""
# Laser melting physics and energy density

In laser PBF a beam of power $P$ scans at speed $v$, depositing energy into a
moving **melt pool**. Engineers collapse the main parameters into the
**volumetric energy density (VED)**:

$$E_V = \frac{P}{v \, h \, t},$$

where $h$ is hatch spacing and $t$ is layer thickness (units J/mm³). Too low and
the powder under-melts (lack-of-fusion porosity); too high and the pool destabil-
izes into **keyholing** (entrapped vapor pores). A good process window typically
sits around 40-80 J/mm³ for many alloys.

The thermal field around a moving point source follows **Rosenthal's** solution.
For a fast, intense source the **keyhole-mode** threshold scales with the
normalized enthalpy $\Delta H/h_s \propto P/(v\,\sqrt{\cdots})$; in practice we
map porosity vs VED and find a clean valley:

```plot
{"title": "Porosity vs volumetric energy density (process window)", "xLabel": "energy density EV (J/mm^3)", "yLabel": "porosity (%)", "xRange": [20, 120], "yRange": [0, 8], "grid": true, "functions": [{"expr": "0.002*(x-60)^2+0.3", "label": "lack-of-fusion (low) ... keyholing (high)", "color": "#dc2626"}]}
```

A quick VED sweep and the Rosenthal peak temperature in Python:

```python
import numpy as np

def energy_density(P, v, h, t):
    # Volumetric energy density (J/mm^3). P[W], v[mm/s], h,t[mm].
    return P / (v * h * t)

# Sweep laser power for fixed scan strategy
P = np.linspace(150, 400, 6)          # W
v, h, t = 900.0, 0.10, 0.03           # mm/s, mm, mm
print(np.round(energy_density(P, v, h, t), 1))   # -> J/mm^3

# Rosenthal peak temperature rise for a moving point source (quasi-steady)
def rosenthal_dT(P, eta, k, v, r, alpha, T0=300.0):
    # k[W/mm.K], alpha[mm^2/s], r[mm]; on the centreline behind the source
    return (eta * P) / (2 * np.pi * k * r) * np.exp(-v * (r) / (2 * alpha))
```

**Next:** AM materials and the microstructures they form.
""",
        ),
        _t(
            "Materials and microstructure in AM",
            "12 min",
            r"""
# Materials and microstructure in AM

AM materials span **polymers** (PLA, ABS, PETG, nylon PA12, PEEK), **metals**
(Ti-6Al-4V, AlSi10Mg, Inconel 718, 316L stainless, maraging steel),
**photopolymers** and **ceramics/composites**. The defining feature of fusion AM
is an **extreme thermal history**: cooling rates of $10^3$-$10^6$ K/s and
repeated reheating from subsequent layers.

```mermaid
flowchart TB
  POWDER["Metal powder"] --> MELT["Rapid melt"]
  MELT --> SOLID["Directional, rapid solidification"]
  SOLID --> COL["Columnar grains along build (Z)"]
  COL --> CYCLE["Reheat from next layers"]
  CYCLE --> HT["Heat treat / HIP -> equiaxed, dense"]
```

This produces **fine, often columnar grains** aligned with the steep thermal
gradient $G$ along the build direction, and metastable phases (e.g. martensitic
$\alpha'$ in Ti-6Al-4V). Solidification morphology is read from a **$G$ vs
solidification rate $R$** map: high $G/R$ favors planar/columnar growth, low
$G/R$ favors equiaxed. The **cooling rate** $G\cdot R$ sets the dendrite arm
spacing:

$$\lambda \approx A \,(G R)^{-n}, \qquad n \approx 0.3\text{-}0.5.$$

```plot
{"title": "Secondary dendrite arm spacing vs cooling rate", "xLabel": "log10 cooling rate G*R (K/s)", "yLabel": "arm spacing lambda (um)", "xRange": [2, 6], "yRange": [0, 12], "grid": true, "functions": [{"expr": "50*exp(-0.9*x)", "label": "finer microstructure at high cooling rate", "color": "#16a34a"}]}
```

Post-processing matters: **hot isostatic pressing (HIP)** closes internal pores,
and **heat treatment** relaxes residual stress and tunes phases. Properties are
**anisotropic** — Z-direction strength and ductility are typically lower.

**Next:** residual stress, distortion and how to control them.
""",
        ),
        _t(
            "Residual stress and distortion",
            "12 min",
            r"""
# Residual stress and distortion

Localized melting and fast cooling make each new layer **shrink** while clamped
by the solid below. The **thermal gradient mechanism (TGM)** leaves the part in
self-equilibrated **residual stress** that can warp it, crack it, or peel it off
the plate. A first estimate of the thermally induced strain is:

$$\varepsilon_{th} = \alpha \, \Delta T,$$

and the locked-in stress approaches yield, $\sigma_{res} \lesssim \sigma_y$, near
fused regions. Distortion grows with part footprint and reduces with stiffer
support / scan strategy.

```mermaid
flowchart LR
  MELT["Hot layer expands then is cooled"] --> SHRINK["Contracts, restrained by layer below"]
  SHRINK --> TENS["Tensile residual stress at top"]
  TENS --> WARP["Warping / curling / plate peel"]
  WARP --> MIT["Mitigate: scan rotation, preheat, supports, stress relief"]
```

Stress accumulates with the number of deposited layers before relaxation; a
simple lumped model shows it building toward a saturation set by yield:

```plot
{"title": "Residual stress build-up vs deposited layers", "xLabel": "layers deposited", "yLabel": "residual stress (MPa)", "xRange": [0, 30], "yRange": [0, 320], "grid": true, "functions": [{"expr": "300*(1-exp(-0.15*x))", "label": "approach to yield-limited saturation", "color": "#dc2626"}]}
```

A 1-D thermo-mechanical layer estimate in MATLAB:

```matlab
% Estimate thermal strain and stress per layer for Ti-6Al-4V
alpha = 8.6e-6;     % 1/K, CTE
E     = 110e3;      % MPa, modulus
sy    = 900;        % MPa, yield
dT    = linspace(200, 1200, 6);     % K above stress-free temp
eps_th = alpha .* dT;               % thermal strain
sigma  = min(E .* eps_th, sy);      % clip at yield
disp([dT(:) eps_th(:) sigma(:)])
```

Mitigations: **scan-vector rotation** (e.g. 67° per layer), **base-plate
preheat** (strong in EBM), robust **supports** as heat sinks/anchors, and a
**stress-relief** cycle before removing the part from the plate.

**Next:** dimensional accuracy, tolerances and surface finish.
""",
        ),
        _t(
            "Dimensional accuracy and tolerances",
            "11 min",
            r"""
# Dimensional accuracy and tolerances

AM parts deviate from nominal through **shrinkage**, **stair-stepping**, **beam/
bead spreading** and **distortion**. As-built tolerances are coarser than CNC —
roughly ±0.1-0.5 mm for metal PBF — so critical features are printed oversize and
**finish-machined**.

**Stair-stepping** dominates surface roughness on slopes. For a surface inclined
at angle $\theta$ from horizontal and layer thickness $t$, the theoretical
roughness scales as:

$$R_a \approx \frac{t}{4}\,\cos\theta \quad\text{(cusp height } \propto t\cos\theta).$$

Near-vertical walls ($\theta \to 90°$) are smooth; near-horizontal up-facing
surfaces show pronounced steps. Reduce $t$ or reorient to improve:

```plot
{"title": "Stair-step roughness vs surface angle (t = 0.05 mm)", "xLabel": "surface angle theta (rad)", "yLabel": "roughness Ra (um)", "xRange": [0.05, 1.55], "yRange": [0, 14], "grid": true, "functions": [{"expr": "12.5*cos(x)", "label": "Ra ~ (t/4) cos(theta)", "color": "#2563eb"}]}
```

Account for **shrinkage** with a scaling factor and inspect with GD&T:

```python
def compensate_shrinkage(nominal_mm, shrink_pct):
    # Pre-scale CAD dimension so the printed part lands on nominal.
    return nominal_mm / (1.0 - shrink_pct / 100.0)

# 0.7% shrink on a 100 mm feature -> model it at:
print(round(compensate_shrinkage(100.0, 0.7), 3))   # -> 100.705 mm
```

Best practice: orient critical surfaces vertically, add **machining stock** to
toleranced faces, and verify with CMM/CT scanning.

**Next:** quick knowledge check on PBF and AM materials.
""",
        ),
        _quiz(),
    ),
)


# ── Additive Manufacturing — Advanced ────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="additive-manufacturing-advanced",
    title="Additive Manufacturing — Advanced",
    description=(
        "State-of-the-art design and build preparation for additive "
        "manufacturing. Covers design for additive manufacturing (DfAM) rules "
        "and part consolidation, lattice and TPMS structures, topology "
        "optimization, support generation and the overhang rule, slicing and "
        "build-orientation optimization, and the role of simulation, machine "
        "learning and in-situ monitoring. Plots, workflow diagrams and "
        "Python/MATLAB optimization code throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Design for additive manufacturing (DfAM)",
            "12 min",
            r"""
# Design for additive manufacturing (DfAM)

**DfAM** turns AM's freedoms into better parts instead of just printing existing
designs. The core ideas: **consolidate** assemblies into one printed part,
**lightweight** with lattices and topology optimization, exploit **complex
internal channels** (conformal cooling), and design **with** the process
constraints (overhangs, supports, minimum walls, anisotropy).

```mermaid
flowchart TB
  REQ["Functional requirements + loads"] --> CONS["Consolidate parts"]
  CONS --> TOPO["Topology optimization / generative design"]
  TOPO --> LAT["Lattices / TPMS infill"]
  LAT --> CONSTR["Apply AM constraints (overhang, min wall, supports)"]
  CONSTR --> VAL["Simulate -> validate -> print"]
```

A guiding metric is the **buy-to-fly ratio** (raw material per finished part):
machined aerospace brackets can exceed 10-20:1, while AM near-net shapes approach
1-2:1, saving cost and weight. Part-count consolidation compounds the savings —
fewer fasteners, joints and inspection steps:

```plot
{"title": "Relative assembly cost vs part count", "xLabel": "number of consolidated parts", "yLabel": "relative assembly cost", "xRange": [1, 20], "yRange": [0, 22], "grid": true, "functions": [{"expr": "1.1*x", "label": "cost ~ part count + interfaces", "color": "#2563eb"}]}
```

Design rules to internalize: minimum wall ~0.4-1.0 mm, self-supporting overhangs
above ~45°, bridge/hole limits, escape holes for trapped powder, and orienting
critical stresses **within** layers (not across them).

**Next:** lattice and TPMS structures for lightweight, tunable parts.
""",
        ),
        _t(
            "Lattices and TPMS structures",
            "13 min",
            r"""
# Lattices and TPMS structures

**Lattices** replace solid volume with a repeating cellular network — **strut-
based** (BCC, FCC, octet-truss) or **triply periodic minimal surfaces (TPMS)**
like **gyroid**, **Schwarz-P** and **diamond**. They give high stiffness- and
strength-to-weight, energy absorption and large surface area (heat exchangers,
implants).

The mechanics follow **Gibson-Ashby** scaling: a cellular solid's modulus
relates to the bulk modulus through the **relative density** $\bar{\rho} =
\rho^*/\rho_s$:

$$\frac{E^*}{E_s} = C\left(\frac{\rho^*}{\rho_s}\right)^{n},$$

with $n \approx 2$ for **bending-dominated** lattices (e.g. BCC) and $n \approx
1$ for **stretching-dominated** ones (e.g. octet-truss) — the latter are far
stiffer at the same weight:

```plot
{"title": "Gibson-Ashby: relative modulus vs relative density", "xLabel": "relative density rho*/rhos", "yLabel": "relative modulus E*/Es", "xRange": [0.05, 0.6], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "x^2", "label": "bending-dominated (n=2)", "color": "#dc2626"}, {"expr": "0.9*x", "label": "stretching-dominated (n=1)", "color": "#16a34a"}]}
```

TPMS are defined by an implicit field; thresholding it yields the surface, which
is smooth and self-supporting. A gyroid sampled on a grid in Python:

```python
import numpy as np

def gyroid(x, y, z, period=10.0, t=0.0):
    # Gyroid implicit field; isosurface f = t. period in mm.
    k = 2 * np.pi / period
    return (np.sin(k*x)*np.cos(k*y)
            + np.sin(k*y)*np.cos(k*z)
            + np.sin(k*z)*np.cos(k*x) - t)

# Build a voxel grid and mark solid where field < 0 (one of the two phases)
n = 60
g = np.linspace(0, 30, n)
X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
solid = gyroid(X, Y, Z, period=10.0, t=0.0) < 0
print("relative density:", round(solid.mean(), 3))
```

Wall thickness (the $t$ offset) tunes relative density and therefore stiffness.

**Next:** topology optimization for load-driven, minimal-mass geometry.
""",
        ),
        _t(
            "Topology optimization for AM",
            "13 min",
            r"""
# Topology optimization for AM

**Topology optimization (TO)** finds the material layout that minimizes
**compliance** (maximizes stiffness) for a mass budget — perfect for AM, which
can build the organic, freeform result. The classic **SIMP** (Solid Isotropic
Material with Penalization) method assigns each element a density $x_e \in [0,1]$
and penalizes intermediate values:

$$E_e(x_e) = E_{min} + x_e^{\,p}\,(E_0 - E_{min}), \qquad p \approx 3,$$

minimizing compliance $c = \mathbf{U}^\top \mathbf{K}\,\mathbf{U}$ subject to a
volume fraction $\sum x_e v_e \le V^*$. Sensitivities drive an update; a density
filter avoids checkerboarding.

```mermaid
flowchart LR
  INIT["Initialize densities x_e"] --> FEA["FE solve K U = F"]
  FEA --> SENS["Compliance + sensitivities dc/dx"]
  SENS --> FILT["Density / sensitivity filter"]
  FILT --> UPD["Optimality-criteria update"]
  UPD --> CONV{"Converged?"}
  CONV -- no --> FEA
  CONV -- yes --> RESULT["Optimized layout -> smooth -> print"]
```

The optimizer drives compliance down over iterations, converging to a stiff,
minimal-mass design:

```plot
{"title": "Topology optimization convergence", "xLabel": "iteration", "yLabel": "normalized compliance", "xRange": [0, 25], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)+0.15", "label": "compliance decreases to optimum", "color": "#16a34a"}]}
```

The OC density update used inside the loop:

```python
import numpy as np

def oc_update(x, dc, volfrac, move=0.2):
    # Optimality-criteria update for SIMP topology optimization.
    l1, l2 = 1e-9, 1e9
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        xnew = np.clip(x * np.sqrt(-dc / lmid), x - move, x + move)
        xnew = np.clip(xnew, 0.0, 1.0)
        if xnew.mean() > volfrac:        # too much material -> raise multiplier
            l1 = lmid
        else:
            l2 = lmid
    return xnew
```

Add **AM-aware constraints** — overhang/self-support filters and minimum
member size — so the result prints without excessive supports.

**Next:** supports, the overhang rule and slicing strategy.
""",
        ),
        _t(
            "Supports, overhangs and slicing",
            "12 min",
            r"""
# Supports, overhangs and slicing

Overhanging features need **support structures** to anchor them, conduct heat and
resist recoater forces. The **overhang rule of thumb**: surfaces steeper than the
**critical angle** (often ~45° from horizontal) are self-supporting; shallower
ones sag or curl. Support **must be removable**, so designers balance build
success against post-processing labor.

```mermaid
flowchart TB
  GEOM["Sliced geometry"] --> DETECT["Detect overhangs < critical angle"]
  DETECT --> GEN["Generate supports (tree / block / lattice)"]
  GEN --> ANCHOR["Anchor + heat sink + recoater stability"]
  ANCHOR --> PRINT["Print"]
  PRINT --> REMOVE["Remove supports -> finish surface"]
```

Required support **area** grows sharply as features approach horizontal — roughly
inversely with the sine of the inclination above the critical angle. Orienting a
part to minimize supported area is a real optimization:

```plot
{"title": "Relative support area vs overhang angle", "xLabel": "surface angle from horizontal theta (rad)", "yLabel": "relative support area", "xRange": [0.15, 1.55], "yRange": [0, 7], "grid": true, "functions": [{"expr": "1/sin(x)", "label": "more support as surfaces flatten", "color": "#dc2626"}]}
```

A simple per-facet overhang test, given mesh facet normals, in Python:

```python
import numpy as np

def needs_support(normals, build_dir=(0, 0, 1), crit_deg=45.0):
    # Flag downward-facing facets steeper than the critical overhang angle.
    b = np.asarray(build_dir, float)
    n = normals / np.linalg.norm(normals, axis=1, keepdims=True)
    cos_to_down = n @ (-b)                       # how down-facing the facet is
    angle_from_horiz = np.degrees(np.arcsin(np.clip(cos_to_down, -1, 1)))
    return angle_from_horiz > (90.0 - crit_deg)  # too overhung -> support
```

Slicing then sets layer height (adaptive layers thin only where curvature is
high), perimeters, and the support interface gap for clean removal.

**Next:** simulation, machine learning and in-situ monitoring.
""",
        ),
        _t(
            "Simulation, ML and in-situ monitoring",
            "13 min",
            r"""
# Simulation, ML and in-situ monitoring

Modern AM closes the loop with **physics simulation**, **machine learning** and
**in-situ sensing**. Build simulators (e.g. the **inherent-strain** method)
predict distortion and residual stress before printing so the geometry can be
**pre-compensated** — warp the CAD by the negative of predicted distortion so it
springs back to nominal.

```mermaid
flowchart LR
  CAD["Build layout"] --> SIM["Thermo-mech / inherent-strain simulation"]
  SIM --> COMP["Pre-compensate geometry"]
  COMP --> PRINT["Print"]
  PRINT --> SENSE["In-situ sensors: melt-pool camera, pyrometer, photodiode"]
  SENSE --> ML["ML anomaly / porosity detection"]
  ML --> FEED["Feedback: flag defects, adapt parameters"]
```

**In-situ monitoring** streams high-rate signals (coaxial melt-pool imaging,
photodiode intensity, layer-wise cameras). A CNN or anomaly model classifies
porosity-prone events; detection accuracy improves with labeled data and tends to
saturate:

```plot
{"title": "Defect-detection accuracy vs labeled training builds", "xLabel": "labeled builds", "yLabel": "detection accuracy", "xRange": [0, 40], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1-0.8*exp(-0.12*x)", "label": "learning curve to a ceiling", "color": "#16a34a"}]}
```

A minimal anomaly flag on melt-pool signals (z-score) plus the distortion
pre-compensation idea in Python:

```python
import numpy as np

def flag_anomalies(signal, k=3.0):
    # Flag melt-pool samples beyond k sigma from the running mean.
    mu, sigma = signal.mean(), signal.std() + 1e-9
    z = (signal - mu) / sigma
    return np.abs(z) > k                    # True where likely a defect event

def precompensate(nodes, predicted_disp, gain=1.0):
    # Warp mesh nodes by the negative predicted distortion (morphing).
    return nodes - gain * predicted_disp    # part springs back toward nominal
```

The frontier: **physics-informed ML** surrogates that replace hours of FE
simulation, closed-loop **feedback control** of laser power per scan, and
**digital twins** of the whole build. These cut qualification cost — the largest
barrier to industrial AM adoption.

**Next:** final knowledge check across DfAM, lattices, TO and build prep.
""",
        ),
        _quiz(),
    ),
)


ADDITIVE_MANUFACTURING_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ADDITIVE_MANUFACTURING_COURSES"]
