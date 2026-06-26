"""Fluid Mechanics track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on the mechanics of fluids. Starts
from fluid properties and hydrostatics, builds through the control-volume
conservation laws, Bernoulli and the Navier-Stokes equations, and ends with pipe
flow, boundary layers, drag, dimensional analysis and CFD/optimisation. Lessons
are `text` with LaTeX, interactive ```plot blocks (pressure, velocity profiles,
Moody/drag curves), ```mermaid classification and workflow diagrams and
runnable ```python/```matlab snippets.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Fluid Mechanics — Basics ─────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="fluid-mechanics-basics",
    title="Fluid Mechanics — Basics",
    description=(
        "Build physical intuition for fluids: what a fluid is and the continuum "
        "hypothesis, the key properties (density, viscosity, surface tension), "
        "hydrostatic pressure and manometry, buoyancy and Archimedes' principle, "
        "and a first look at flow kinematics. Interactive plots and diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a fluid? The continuum hypothesis",
            "10 min",
            r"""
# What is a fluid? The continuum hypothesis

A **fluid** is a substance that cannot resist a shear stress at rest — it keeps
deforming for as long as the stress is applied. That is the defining contrast
with a solid, which reaches a static strain. Both liquids and gases are fluids;
they differ mainly in compressibility.

We almost never track individual molecules. Instead we use the **continuum
hypothesis**: properties such as density and velocity are smooth fields defined
at every point. This is valid when the **Knudsen number** is small,

$$\mathrm{Kn} = \frac{\lambda}{L} \ll 1,$$

where $\lambda$ is the molecular mean free path and $L$ the smallest length scale
of interest. For air at sea level $\lambda \approx 68\,\text{nm}$, so the
continuum picture holds for almost all engineering devices but breaks down in
micro/nano flows and rarefied gases.

A fluid responds to shear with a **strain rate**, not a strain. For most common
fluids the shear stress grows linearly with the velocity gradient (Newtonian
behaviour):

```plot
{"title": "Shear stress vs strain rate", "xLabel": "strain rate du/dy (1/s)", "yLabel": "shear stress tau (Pa)", "xRange": [0, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "0.9*x", "label": "Newtonian (constant mu)", "color": "#2563eb"}, {"expr": "0.4*x^1.4", "label": "shear-thickening", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  M["Matter"] --> S["Solid: resists shear, finite strain"]
  M --> F["Fluid: deforms continuously under shear"]
  F --> L["Liquid: nearly incompressible"]
  F --> G["Gas: compressible"]
```

**Next:** the properties that quantify how a fluid behaves — density and viscosity.
""",
        ),
        _t(
            "Fluid properties: density, viscosity, surface tension",
            "12 min",
            r"""
# Fluid properties: density, viscosity, surface tension

**Density** $\rho$ (kg/m$^3$) is mass per unit volume; **specific weight** is
$\gamma = \rho g$ and **specific gravity** is $SG = \rho/\rho_{water}$. Water is
$\approx 1000\,\text{kg/m}^3$, air $\approx 1.2\,\text{kg/m}^3$.

**Viscosity** measures resistance to shear. Newton's law of viscosity:

$$\tau = \mu\,\frac{du}{dy},$$

where $\mu$ is the **dynamic viscosity** (Pa·s). The **kinematic viscosity** is
$\nu = \mu/\rho$ (m$^2$/s). Liquid viscosity falls with temperature; gas
viscosity rises with it (Sutherland's law). Viscosity of water at 20 °C is
about $1.0\times10^{-3}\,\text{Pa·s}$.

```plot
{"title": "Linear (Couette) velocity profile between plates", "xLabel": "u(y) (m/s)", "yLabel": "y/h", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "u/U = y/h", "color": "#2563eb"}]}
```

**Surface tension** $\sigma$ (N/m) arises from cohesive forces at a liquid
interface. The pressure jump across a curved interface is the **Young-Laplace**
relation; for a spherical droplet of radius $R$,

$$\Delta p = \frac{2\sigma}{R}.$$

Capillary rise in a tube of radius $r$ is $h = 2\sigma\cos\theta/(\rho g r)$.

```python
import numpy as np

mu = 1.0e-3        # Pa.s, water at 20 C
rho = 998.0        # kg/m^3
nu = mu / rho      # kinematic viscosity
U, h = 2.0, 1e-3   # plate speed (m/s), gap (m)
tau = mu * U / h   # wall shear stress, Pa
print(f"nu = {nu:.2e} m^2/s, tau = {tau:.2f} Pa")
```

**Next:** how pressure varies in a fluid at rest — hydrostatics.
""",
        ),
        _t(
            "Hydrostatic pressure and manometry",
            "12 min",
            r"""
# Hydrostatic pressure and manometry

In a fluid **at rest** there is no shear, so the only stress is pressure, which
acts equally in all directions at a point (**Pascal's law**). Balancing forces
on a fluid element gives the **hydrostatic equation**:

$$\frac{dp}{dz} = -\rho g,$$

with $z$ measured upward. For a constant-density liquid this integrates to

$$p = p_0 + \rho g h,$$

so pressure grows linearly with depth $h$ below the surface — independent of the
container shape (the *hydrostatic paradox*).

```plot
{"title": "Gauge pressure vs depth in water", "xLabel": "depth h (m)", "yLabel": "gauge pressure p (kPa)", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "9.81*x", "label": "p = rho g h", "color": "#2563eb"}]}
```

A **manometer** uses this linear law to measure pressure differences by reading
a column height. For a U-tube with a manometer fluid of density $\rho_m$,

$$p_A - p_B = (\rho_m - \rho)\,g\,\Delta h.$$

```mermaid
flowchart LR
  T["Tank pressure p_A"] --> U["U-tube manometer"]
  U --> R["Read height difference dh"]
  R --> C["p_A - p_B = (rho_m - rho) g dh"]
```

Pressures are quoted as **absolute** (from vacuum) or **gauge**
($p_{gauge}=p_{abs}-p_{atm}$). Standard atmosphere is $101.325\,\text{kPa}$.

**Next:** the resultant force a static fluid exerts on a submerged surface.
""",
        ),
        _t(
            "Forces on submerged surfaces and buoyancy",
            "12 min",
            r"""
# Forces on submerged surfaces and buoyancy

The hydrostatic pressure pushing on a wall integrates into a **resultant force**.
For a flat plate of area $A$ whose centroid lies at depth $h_c$,

$$F_R = \rho g\,h_c\,A = p_c\,A.$$

The force does **not** act at the centroid but at the **centre of pressure**,
which sits lower because pressure increases with depth. For a surface inclined at
angle $\theta$, the centre of pressure is offset from the centroid by

$$y_{cp} - y_c = \frac{I_{xc}}{y_c\,A},$$

where $I_{xc}$ is the second moment of area about the centroidal axis.

**Buoyancy** is the net upward pressure force on a submerged body —
**Archimedes' principle**: the buoyant force equals the weight of the displaced
fluid,

$$F_B = \rho_{fluid}\,g\,V_{disp}.$$

A body floats when $F_B$ equals its weight; it is stable if the **metacentre**
lies above the centre of gravity.

```plot
{"title": "Pressure force per unit width on a vertical wall", "xLabel": "wall depth d (m)", "yLabel": "force per width (kN/m)", "xRange": [0, 6], "yRange": [0, 200], "grid": true, "functions": [{"expr": "0.5*9.81*x^2", "label": "F/b = rho g d^2 / 2", "color": "#2563eb"}]}
```

```python
rho, g = 1000.0, 9.81
V_disp = 0.02           # m^3 displaced
F_B = rho * g * V_disp  # buoyant force, N
print(f"Buoyant force = {F_B:.1f} N (lifts {F_B/g:.2f} kg)")
```

**Next:** describing fluids in motion — flow kinematics.
""",
        ),
        _t(
            "Flow kinematics: streamlines, steady vs unsteady",
            "11 min",
            r"""
# Flow kinematics: streamlines, steady vs unsteady

Two viewpoints describe motion. The **Lagrangian** view follows individual fluid
particles; the **Eulerian** view records the velocity field $\mathbf{u}(x,y,z,t)$
at fixed points in space. Engineering almost always uses the Eulerian field.

A flow is **steady** if $\partial/\partial t = 0$ everywhere; otherwise it is
**unsteady**. It is **uniform** if properties do not vary along the flow
direction. Three curves visualise the field:

- **Streamlines** — tangent to $\mathbf{u}$ at an instant.
- **Pathlines** — the actual trajectory of one particle.
- **Streaklines** — the locus of particles that passed a fixed point.

In steady flow all three coincide.

Acceleration in the Eulerian frame uses the **material derivative**, which adds a
convective term to the local one:

$$\mathbf{a} = \frac{D\mathbf{u}}{Dt} = \frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u}.$$

Even in steady flow a particle can accelerate (the convective term) — for
example speeding up through a nozzle.

```plot
{"title": "Speed-up through a converging nozzle (steady, convective accel)", "xLabel": "x along nozzle (m)", "yLabel": "speed u (m/s)", "xRange": [0, 2], "yRange": [0, 12], "grid": true, "functions": [{"expr": "2/(1-0.4*x)", "label": "u(x) as area shrinks", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  K["Flow description"] --> SS["Steady: d/dt = 0"]
  K --> US["Unsteady: time-varying"]
  K --> SL["Streamlines | Pathlines | Streaklines"]
  SL --> EQ["Coincide only in steady flow"]
```

**Next:** put your basics to the test.
""",
        ),
        _quiz(),
    ),
)


# ── Fluid Mechanics — Intermediate ───────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="fluid-mechanics-intermediate",
    title="Fluid Mechanics — Intermediate",
    description=(
        "The quantitative core of fluid mechanics: the Reynolds transport "
        "theorem and continuity, the momentum and energy equations on a control "
        "volume, Bernoulli's equation and its assumptions, the Navier-Stokes "
        "equations and exact solutions, and laminar pipe flow with head loss. "
        "Worked equations, plots and code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Conservation of mass and the continuity equation",
            "12 min",
            r"""
# Conservation of mass and the continuity equation

The **Reynolds transport theorem (RTT)** converts a system law (mass, momentum,
energy follow the matter) into a **control-volume** statement we can apply to a
fixed region. For any extensive property $B$ with intensive value $b$,

$$\frac{dB_{sys}}{dt} = \frac{\partial}{\partial t}\!\int_{CV}\! \rho b\,dV + \int_{CS}\! \rho b\,(\mathbf{u}\cdot\mathbf{n})\,dA.$$

Setting $B=$ mass ($b=1$) and $dB_{sys}/dt=0$ gives **continuity**: storage plus
net outflow is zero. For **steady, incompressible** flow through a duct with one
inlet and one outlet this reduces to

$$Q = A_1 V_1 = A_2 V_2 = \text{const}.$$

So the velocity rises where the area shrinks — the hyperbola below.

```plot
{"title": "Continuity: velocity vs area at fixed Q = 0.5 m^3/s", "xLabel": "area A (m^2)", "yLabel": "velocity V (m/s)", "xRange": [0.05, 1], "yRange": [0, 12], "grid": true, "functions": [{"expr": "0.5/x", "label": "V = Q / A", "color": "#2563eb"}]}
```

The differential form for compressible flow is

$$\frac{\partial \rho}{\partial t} + \nabla\cdot(\rho\mathbf{u}) = 0.$$

```python
import numpy as np

Q = 0.5                       # m^3/s, fixed volumetric flow
A = np.array([0.5, 0.2, 0.1]) # duct areas, m^2
V = Q / A                     # continuity gives velocity
print("V (m/s):", np.round(V, 2))  # [1.   2.5  5. ]
```

**Next:** Bernoulli's equation — energy along a streamline.
""",
        ),
        _t(
            "Bernoulli's equation and its assumptions",
            "13 min",
            r"""
# Bernoulli's equation and its assumptions

Integrating the inviscid momentum equation (Euler) along a streamline for
**steady, incompressible, frictionless** flow gives **Bernoulli's equation**:

$$p + \tfrac{1}{2}\rho V^2 + \rho g z = \text{const}.$$

Each term is a pressure: **static** $p$, **dynamic** $\tfrac12\rho V^2$, and
**hydrostatic** $\rho g z$. Dividing by $\rho g$ gives the **head** form
(pressure head + velocity head + elevation head = total head).

The assumptions matter: no viscosity, along one streamline, steady,
incompressible, no shaft work. Where they hold, faster flow means lower static
pressure — the basis of the **Venturi** and the **Pitot tube**, which reads
stagnation pressure to give speed $V=\sqrt{2(p_0-p)/\rho}$.

```plot
{"title": "Static pressure drop with speed (Bernoulli, p0 = 100 kPa)", "xLabel": "speed V (m/s)", "yLabel": "static pressure p (kPa)", "xRange": [0, 30], "yRange": [0, 110], "grid": true, "functions": [{"expr": "100 - 0.5*1.2*x^2/1000", "label": "p = p0 - rho V^2 / 2", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  IN["Inlet: high p, low V"] --> TH["Throat: low p, high V"]
  TH --> OUT["Outlet: recovers p"]
  TH --> M["Measure dp -> infer Q"]
```

```python
rho = 1000.0
dp = 8000.0                    # Pa, p0 - p from a Pitot tube
V = (2*dp/rho)**0.5           # Bernoulli speed
print(f"V = {V:.2f} m/s")
```

**Next:** the momentum equation and the forces flows exert.
""",
        ),
        _t(
            "The momentum equation on a control volume",
            "13 min",
            r"""
# The momentum equation on a control volume

Applying the RTT to linear momentum ($b=\mathbf{u}$) gives the **integral
momentum equation** — Newton's second law for a control volume:

$$\sum \mathbf{F} = \frac{\partial}{\partial t}\!\int_{CV}\!\rho\mathbf{u}\,dV + \int_{CS}\!\rho\mathbf{u}\,(\mathbf{u}\cdot\mathbf{n})\,dA.$$

For **steady** flow with one inlet and one outlet the storage term vanishes and
the net force equals the **momentum flux** difference:

$$\sum \mathbf{F} = \dot{m}\,(\mathbf{V}_{out} - \mathbf{V}_{in}),\qquad \dot{m}=\rho Q.$$

This sizes the anchoring forces on **pipe bends**, **reducers**, **nozzles**,
and the **thrust** of jets and rockets. For a jet of speed $V_j$ hitting a fixed
flat plate normally, the force is $F = \dot m V_j = \rho A V_j^2$.

```plot
{"title": "Force of a water jet on a plate vs jet speed", "xLabel": "jet speed V (m/s)", "yLabel": "force F (N)", "xRange": [0, 30], "yRange": [0, 1000], "grid": true, "functions": [{"expr": "1000*0.001*x^2", "label": "F = rho A V^2 (A = 1e-3 m^2)", "color": "#2563eb"}]}
```

```python
import numpy as np

rho, Q = 1000.0, 0.05         # kg/m^3, m^3/s
A1, A2 = 0.02, 0.01           # inlet/outlet area of a reducer, m^2
V1, V2 = Q/A1, Q/A2
mdot = rho * Q
# Reaction force to turn the flow 90 degrees (x-momentum only):
Fx = mdot * (0 - V1)          # outlet has no x-velocity
print(f"V1={V1:.1f}, V2={V2:.1f} m/s; Fx on bend = {Fx:.0f} N")
```

**Next:** the energy equation with pumps, turbines and losses.
""",
        ),
        _t(
            "The energy equation and head losses",
            "12 min",
            r"""
# The energy equation and head losses

Bernoulli is energy with **no losses and no machines**. The engineering
**energy equation** restores both, written in head (metres) between sections 1
and 2:

$$\frac{p_1}{\rho g}+\frac{V_1^2}{2g}+z_1 + h_p = \frac{p_2}{\rho g}+\frac{V_2^2}{2g}+z_2 + h_t + h_L.$$

Here $h_p$ is **pump head added**, $h_t$ is **turbine head extracted**, and
$h_L$ is the total **head loss** (friction plus fittings). Pump power is
$P = \rho g Q\, h_p / \eta$.

Major (pipe friction) loss uses the **Darcy-Weisbach** equation, and minor
(fitting) losses use loss coefficients $K$:

$$h_L = f\,\frac{L}{D}\,\frac{V^2}{2g} + \sum K\,\frac{V^2}{2g}.$$

The **system curve** (required head vs flow) rises with $Q^2$; its intersection
with the **pump curve** is the operating point.

```plot
{"title": "Pump and system curves -> operating point", "xLabel": "flow Q (L/s)", "yLabel": "head H (m)", "xRange": [0, 10], "yRange": [0, 40], "grid": true, "functions": [{"expr": "35 - 0.3*x^2", "label": "pump curve", "color": "#2563eb"}, {"expr": "5 + 0.25*x^2", "label": "system curve", "color": "#dc2626"}]}
```

```python
rho, g, Q, hp, eta = 1000.0, 9.81, 0.05, 20.0, 0.7
P = rho*g*Q*hp/eta            # shaft power, W
print(f"Pump shaft power = {P/1000:.2f} kW")
```

**Next:** the full differential laws — the Navier-Stokes equations.
""",
        ),
        _t(
            "The Navier-Stokes equations and exact solutions",
            "14 min",
            r"""
# The Navier-Stokes equations and exact solutions

The **Navier-Stokes equations** are Newton's second law applied to a fluid
element. For an incompressible Newtonian fluid:

$$\rho\!\left(\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u}\right) = -\nabla p + \mu\nabla^2\mathbf{u} + \rho\mathbf{g},\qquad \nabla\cdot\mathbf{u}=0.$$

The left side is inertia (local + convective); the right is pressure gradient,
viscous diffusion and body force. The nonlinear convective term is what makes the
equations hard — and turbulence possible. Only a handful of **exact solutions**
exist for simple geometries.

For **plane Poiseuille flow** between parallel plates driven by a pressure
gradient, the velocity is parabolic:

$$u(y) = \frac{1}{2\mu}\frac{dp}{dx}\,(y^2 - h^2),$$

and for fully developed **pipe (Hagen-Poiseuille) flow** the profile is
parabolic with $u_{max} = 2\bar V$.

```plot
{"title": "Parabolic Poiseuille velocity profile in a pipe", "xLabel": "u/u_max", "yLabel": "r/R", "xRange": [0, 1], "yRange": [-1, 1], "grid": true, "functions": [{"expr": "1 - x^2", "label": "u/u_max = 1 - (r/R)^2", "color": "#2563eb"}]}
```

```python
import numpy as np

mu, dpdx, h = 1.0e-3, -200.0, 0.01   # Pa.s, Pa/m, half-gap m
y = np.linspace(-h, h, 5)
u = (1/(2*mu))*dpdx*(y**2 - h**2)    # plane Poiseuille
print("u (m/s):", np.round(u, 3))    # max at centre, 0 at walls
```

**Next:** laminar vs turbulent flow and the Reynolds number.
""",
        ),
        _t(
            "Laminar vs turbulent flow and the Reynolds number",
            "12 min",
            r"""
# Laminar vs turbulent flow and the Reynolds number

The **Reynolds number** is the ratio of inertial to viscous forces and sets the
flow regime:

$$\mathrm{Re} = \frac{\rho V D}{\mu} = \frac{V D}{\nu}.$$

In a pipe, flow is **laminar** for $\mathrm{Re}\lesssim 2300$ (smooth, ordered,
parabolic profile), **transitional** near 2300-4000, and **turbulent** above
$\approx 4000$ (chaotic eddies, flatter mean profile, much higher mixing and
wall friction). Osborne Reynolds' 1883 dye experiment first revealed the
transition.

For laminar pipe flow the **friction factor** has a clean closed form,
$f = 64/\mathrm{Re}$; in turbulent flow it depends on Reynolds number and
relative roughness (the Moody chart, next course).

```plot
{"title": "Laminar friction factor f = 64/Re", "xLabel": "Reynolds number Re", "yLabel": "friction factor f", "xRange": [200, 2300], "yRange": [0, 0.35], "grid": true, "functions": [{"expr": "64/x", "label": "f = 64/Re (laminar)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  Re["Compute Re = rho V D / mu"] --> L["Re < 2300: laminar"]
  Re --> T["2300-4000: transitional"]
  Re --> U["Re > 4000: turbulent"]
```

```python
rho, V, D, mu = 1000.0, 1.5, 0.05, 1.0e-3
Re = rho*V*D/mu
regime = "laminar" if Re < 2300 else "turbulent" if Re > 4000 else "transitional"
print(f"Re = {Re:.0f} -> {regime}")
```

**Next:** prove what you have learned.
""",
        ),
        _quiz(),
    ),
)


# ── Fluid Mechanics — Advanced ───────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="fluid-mechanics-advanced",
    title="Fluid Mechanics — Advanced",
    description=(
        "Applied and state-of-the-art fluid mechanics: turbulent pipe flow and "
        "the Moody chart, boundary layers and flow separation, drag/lift and bluff "
        "bodies, dimensional analysis and similitude, turbulence modelling and "
        "CFD, and shape optimisation with adjoint and machine-learning methods. "
        "Plots, workflows and runnable code throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Turbulent pipe flow and the Moody chart",
            "14 min",
            r"""
# Turbulent pipe flow and the Moody chart

In turbulent pipe flow the **Darcy friction factor** $f$ depends on Reynolds
number and **relative roughness** $\varepsilon/D$. The implicit
**Colebrook-White** equation is the standard:

$$\frac{1}{\sqrt{f}} = -2\log_{10}\!\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{\mathrm{Re}\sqrt{f}}\right).$$

The **Moody chart** plots its solution. Two limits matter: the **smooth-pipe**
curve at low roughness, and the **fully rough** regime at high $\mathrm{Re}$
where $f$ becomes constant (viscosity stops mattering). For a quick explicit
estimate, the **Haaland** equation is within ~2 %.

```plot
{"title": "Friction factor: laminar vs turbulent (smooth) regimes", "xLabel": "log10(Re)", "yLabel": "friction factor f", "xRange": [3, 7], "yRange": [0, 0.05], "grid": true, "functions": [{"expr": "0.316/exp(0.25*log(10)*x)", "label": "Blasius f = 0.316 Re^-0.25", "color": "#2563eb"}]}
```

Solve Colebrook by fixed-point iteration:

```python
import numpy as np

def colebrook(Re, eps_D, f=0.02):
    for _ in range(50):
        rhs = -2*np.log10(eps_D/3.7 + 2.51/(Re*np.sqrt(f)))
        f = 1.0/rhs**2
    return f

f = colebrook(1e5, 1e-3)
print(f"f = {f:.4f}")          # head loss via Darcy-Weisbach next
```

**Next:** the thin viscous region near walls — boundary layers.
""",
        ),
        _t(
            "Boundary layers and flow separation",
            "14 min",
            r"""
# Boundary layers and flow separation

Prandtl's 1904 insight: viscosity matters mostly in a **thin boundary layer**
near a surface, where velocity rises from zero (no-slip) to the free-stream
value. For a laminar flat plate the **Blasius solution** gives the layer
thickness and wall friction:

$$\frac{\delta}{x} \approx \frac{5.0}{\sqrt{\mathrm{Re}_x}},\qquad C_f = \frac{0.664}{\sqrt{\mathrm{Re}_x}}.$$

The layer thickens downstream and **transitions** to turbulent near
$\mathrm{Re}_x\approx 5\times10^5$, becoming thicker but more resistant to
**separation**.

**Separation** occurs when an **adverse pressure gradient** ($dp/dx>0$) decelerates
near-wall fluid until it reverses, detaching the layer. This is the cause of
**stall** on wings and the large pressure (form) drag on bluff bodies. Turbulent
layers carry more momentum near the wall and separate later — which is why a golf
ball's dimples reduce drag.

```plot
{"title": "Laminar boundary-layer growth (Blasius)", "xLabel": "distance x (m)", "yLabel": "delta (mm)", "xRange": [0, 1], "yRange": [0, 12], "grid": true, "functions": [{"expr": "5000*sqrt(1.5e-5*x/20)", "label": "delta = 5x / sqrt(Re_x)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  FP["Favorable dp/dx < 0"] --> AT["Layer stays attached"]
  AP["Adverse dp/dx > 0"] --> SE["Near-wall reversal -> separation"]
  SE --> WK["Wake + form drag"]
```

```python
import numpy as np

U, nu, x = 20.0, 1.5e-5, 0.5
Re_x = U*x/nu
delta = 5.0*x/np.sqrt(Re_x)
Cf = 0.664/np.sqrt(Re_x)
print(f"Re_x={Re_x:.2e}, delta={delta*1000:.2f} mm, Cf={Cf:.4e}")
```

**Next:** drag, lift and the forces on bluff and streamlined bodies.
""",
        ),
        _t(
            "Drag, lift and bluff-body aerodynamics",
            "13 min",
            r"""
# Drag, lift and bluff-body aerodynamics

The aerodynamic force on a body is non-dimensionalised by the **dynamic
pressure** $\tfrac12\rho V^2$ and a reference area $A$:

$$F_D = C_D\,\tfrac12\rho V^2 A,\qquad F_L = C_L\,\tfrac12\rho V^2 A.$$

Drag has two parts: **friction (skin) drag** from wall shear and **pressure
(form) drag** from the separated wake. **Streamlined** bodies (airfoils) are
friction-dominated and low-$C_D$; **bluff** bodies (cylinders, cars) are
form-dominated. A sphere's $C_D$ falls sharply (the **drag crisis**) near
$\mathrm{Re}\approx 3\times10^5$ when the boundary layer turns turbulent and
delays separation.

For a circular cylinder, vortices shed alternately (the **von Karman street**) at
a frequency set by the **Strouhal number** $St = fD/V \approx 0.2$ — the source
of aeolian tones and flow-induced vibration.

```plot
{"title": "Drag force on a car vs speed (quadratic)", "xLabel": "speed V (m/s)", "yLabel": "drag force (N)", "xRange": [0, 40], "yRange": [0, 800], "grid": true, "functions": [{"expr": "0.5*1.2*0.3*2.2*x^2", "label": "F_D = Cd*0.5*rho*A*V^2", "color": "#dc2626"}]}
```

```python
rho, Cd, A = 1.2, 0.30, 2.2     # air, drag coeff, frontal area m^2
for V in (20, 30, 40):          # m/s
    FD = Cd*0.5*rho*A*V**2
    P = FD*V                    # power to overcome drag, W
    print(f"V={V} m/s -> FD={FD:.0f} N, P={P/1000:.1f} kW")
```

**Next:** scaling experiments and models with dimensional analysis.
""",
        ),
        _t(
            "Dimensional analysis and similitude",
            "13 min",
            r"""
# Dimensional analysis and similitude

**Dimensional analysis** reduces a problem to dimensionless groups, slashing the
number of experiments. The **Buckingham Pi theorem** states that $n$ variables
in $k$ independent dimensions form $n-k$ independent dimensionless **Pi groups**.
Key groups in fluid mechanics:

- **Reynolds** $\mathrm{Re}=\rho VL/\mu$ — inertia/viscous
- **Mach** $\mathrm{Ma}=V/c$ — compressibility
- **Froude** $\mathrm{Fr}=V/\sqrt{gL}$ — free-surface/gravity
- **Weber** $\mathrm{We}=\rho V^2 L/\sigma$ — surface tension

**Similitude** lets a scale model predict full-scale behaviour when geometry is
similar and the governing Pi groups match. Matching $\mathrm{Re}$ for a 1:10 car
model needs 10x the velocity (or a pressurised/heavy-gas tunnel) — often the
core difficulty of model testing.

```plot
{"title": "Drag coefficient collapses onto Re (data collapse)", "xLabel": "log10(Re)", "yLabel": "C_D (sphere, schematic)", "xRange": [0, 6], "yRange": [0, 2], "grid": true, "functions": [{"expr": "24/exp(log(10)*x) + 0.4", "label": "Cd ~ 24/Re + 0.4", "color": "#16a34a"}]}
```

```python
import numpy as np

# Wind-tunnel matching: same Re for model and prototype
rho, mu = 1.2, 1.8e-5
Lp, Vp = 4.0, 30.0            # prototype length (m), speed (m/s)
Lm = 0.4                      # 1:10 model
Vm = Vp * (Lp/Lm)            # Re match (same fluid): V scales inversely with L
print(f"Model tunnel speed for Re match = {Vm:.0f} m/s")
```

**Next:** turbulence modelling and computational fluid dynamics.
""",
        ),
        _t(
            "Turbulence modelling and CFD",
            "15 min",
            r"""
# Turbulence modelling and CFD

Turbulence spans a vast range of eddy scales; the **Kolmogorov** cascade carries
energy from large eddies down to the dissipative microscale
$\eta = (\nu^3/\varepsilon)^{1/4}$. Resolving every scale (**DNS**) costs
$\sim\mathrm{Re}^{9/4}$ grid points — infeasible for most applications. So we
model.

- **RANS** (Reynolds-Averaged Navier-Stokes): solve the mean flow; model the
  **Reynolds stresses** via closures like $k$-$\varepsilon$ or $k$-$\omega$ SST.
  Cheap, the industry workhorse.
- **LES** (Large-Eddy Simulation): resolve large eddies, model the subgrid
  scales. More accurate, much costlier.
- **DNS**: resolve everything — research-only.

A finite-volume **CFD** solver discretises the domain, enforces conservation on
each cell, and couples pressure-velocity (SIMPLE/PISO). Verification (mesh
independence) and validation (against data) are mandatory.

```mermaid
flowchart LR
  G["Geometry + mesh"] --> D["Discretise NS (finite volume)"]
  D --> M["Turbulence model: RANS / LES / DNS"]
  M --> S["Solve + couple p-V (SIMPLE)"]
  S --> V["Verify mesh, validate vs data"]
```

```plot
{"title": "Cost vs accuracy: RANS, LES, DNS (schematic)", "xLabel": "relative accuracy", "yLabel": "log10 cost", "xRange": [0, 1], "yRange": [0, 9], "grid": true, "functions": [{"expr": "9*x^3", "label": "cost rises steeply toward DNS", "color": "#dc2626"}]}
```

```python
import numpy as np

# Order-of-magnitude DNS grid estimate: N ~ Re^(9/4)
for Re in (1e3, 1e4, 1e5):
    N = Re**2.25
    print(f"Re={Re:.0e} -> DNS points ~ {N:.1e}")
```

**Next:** optimise shapes with adjoint and machine-learning methods.
""",
        ),
        _t(
            "Shape optimisation: adjoint and ML methods",
            "14 min",
            r"""
# Shape optimisation: adjoint and ML methods

Beyond simulating a fixed shape, modern design **optimises** it. The objective
$J$ (drag, pressure loss, uniformity) is minimised over design variables
$\boldsymbol{\alpha}$ subject to the flow equations $R(\mathbf{u},\boldsymbol{\alpha})=0$.

The **adjoint method** is the breakthrough: it computes the full gradient
$dJ/d\boldsymbol{\alpha}$ at a cost almost **independent of the number of design
variables** — one extra adjoint solve per objective. That makes thousand-variable
aerodynamic shape optimisation tractable (used across aerospace and turbomachinery).

**Machine learning** now augments the loop: surrogate/**Gaussian-process** models
replace expensive CFD in **Bayesian optimisation**; **physics-informed neural
networks (PINNs)** embed the Navier-Stokes residual in the loss; and learned
turbulence closures correct RANS. Gradient-based design typically converges fast:

```plot
{"title": "Optimisation convergence of normalised drag", "xLabel": "design iteration", "yLabel": "objective J (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "J ~ exp(-0.4 k) (adjoint descent)", "color": "#16a34a"}]}
```

```python
import numpy as np

# Toy adjoint-style gradient descent on a quadratic drag surrogate
def J(a):  return (a - 0.2)**2 + 0.05      # surrogate drag
def dJ(a): return 2*(a - 0.2)              # "adjoint" gradient

a, lr = 1.0, 0.3
for k in range(8):
    a -= lr*dJ(a)
    print(f"iter {k}: alpha={a:.4f}, J={J(a):.5f}")
```

```mermaid
flowchart LR
  P["Parametrise shape (alpha)"] --> C["CFD / surrogate solve"]
  C --> A["Adjoint gradient dJ/dalpha"]
  A --> U["Update alpha (descent / BO)"]
  U --> P
```

**Next:** finish the track — test your mastery.
""",
        ),
        _quiz(),
    ),
)


FLUID_MECHANICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["FLUID_MECHANICS_COURSES"]
