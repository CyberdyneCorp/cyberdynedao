"""Heat Transfer track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on the three modes of heat transfer.
Basics builds intuition for conduction (Fourier's law), convection (Newton's law
of cooling) and radiation; Intermediate develops the quantitative methods —
thermal resistance networks, fins, dimensionless numbers and correlations,
transient lumped/1-D conduction; Advanced covers heat-exchanger design (LMTD and
effectiveness-NTU), boiling/condensation, numerical conduction (finite
differences/CFD) and design optimization. Lessons are `text` with LaTeX,
interactive ```plot blocks, ```mermaid diagrams and ```python/```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, °, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Heat Transfer — Basics ───────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="heat-transfer-basics",
    title="Heat Transfer — Basics",
    description=(
        "The physical foundations of heat transfer: how thermal energy moves by "
        "conduction, convection and radiation. Covers Fourier's law and thermal "
        "conductivity, Newton's law of cooling and convection coefficients, the "
        "Stefan-Boltzmann law for radiation, the energy balance, and steady-state "
        "conduction through plane walls. Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The three modes of heat transfer",
            "10 min",
            r"""
# The three modes of heat transfer

Heat is energy in transit driven by a **temperature difference**, always flowing
from hot to cold (second law of thermodynamics). There are exactly three modes:

- **Conduction** — energy diffuses through a solid or stationary fluid by
  molecular vibration and free-electron drift; no bulk motion.
- **Convection** — heat carried by a moving fluid; combines conduction at the
  wall with advection by the flow.
- **Radiation** — energy emitted as electromagnetic waves; needs no medium and
  works across a vacuum.

A single device often mixes all three. A finned CPU heat sink conducts heat from
the die through the base, convects it into the air stream, and radiates a little
to the case.

```mermaid
flowchart LR
  HOT["Hot body / source"] -->|conduction| SOLID["Solid wall"]
  SOLID -->|convection| FLUID["Moving fluid (air, water)"]
  HOT -->|radiation| SURF["Cooler surfaces (no medium needed)"]
  FLUID --> AMB["Ambient / sink"]
```

The rate of heat transfer is called the **heat rate** $q$ (watts, W); per unit
area it is the **heat flux** $q'' = q/A$ (W/m²). Each mode has its own rate law,
which the next lessons develop. Roughly, conduction and convection scale with the
temperature difference $\Delta T$, while radiation scales with the difference of
the fourth powers of absolute temperature.

**Next:** Fourier's law — the rate law for conduction.
""",
        ),
        _t(
            "Conduction and Fourier's law",
            "12 min",
            r"""
# Conduction and Fourier's law

Conduction is governed by **Fourier's law**. In one dimension the heat flux is
proportional to the temperature gradient:

$$q''_x = -k\,\frac{dT}{dx},$$

where $k$ is the **thermal conductivity** (W/m·K), a material property. The minus
sign encodes that heat flows *down* the gradient (toward lower temperature). For
a plane wall of thickness $L$ with faces at $T_1 > T_2$ and constant $k$, the
profile is linear and the rate is

$$q = \frac{k\,A}{L}\,(T_1 - T_2).$$

Thermal conductivity spans orders of magnitude: copper $\approx 400$, aluminium
$\approx 240$, steel $\approx 50$, water $\approx 0.6$, air $\approx 0.026$, and
insulating foams $\approx 0.03$ W/m·K. Metals conduct via free electrons; gases
conduct poorly, which is why trapped air makes good insulation.

The steady linear temperature profile in a wall (face at 100°C, far face at
20°C):

```plot
{"title": "Temperature profile across a plane wall", "xLabel": "position x (m)", "yLabel": "temperature T (degC)", "xRange": [0, 0.1], "yRange": [0, 110], "grid": true, "functions": [{"expr": "100 - 800*x", "label": "T(x) linear (steady, constant k)", "color": "#dc2626"}]}
```

```python
import numpy as np
k, A, L = 50.0, 0.5, 0.1          # steel wall: W/m.K, m^2, m
T1, T2 = 100.0, 20.0              # face temperatures, degC
q = k * A * (T1 - T2) / L         # Fourier's law for a plane wall
print(f"Heat rate q = {q:.0f} W")  # -> 20000 W
```

**Next:** convection — heat carried away by a moving fluid.
""",
        ),
        _t(
            "Convection and Newton's law of cooling",
            "11 min",
            r"""
# Convection and Newton's law of cooling

When a fluid flows past a surface at a different temperature, heat crosses the
**thermal boundary layer**. The engineering rate law is **Newton's law of
cooling**:

$$q = h\,A\,(T_s - T_\infty),$$

where $T_s$ is the surface temperature, $T_\infty$ the free-stream fluid
temperature, $A$ the area, and $h$ the **convection heat-transfer coefficient**
(W/m²·K). Unlike $k$, $h$ is *not* a material property — it lumps together fluid
properties, flow speed and geometry, and is the hardest quantity to pin down.

- **Natural (free) convection** — buoyancy-driven; $h \approx 2$–25 W/m²·K for
  air, larger for water.
- **Forced convection** — fan or pump driven; $h \approx 25$–250 for gases,
  hundreds to thousands for liquids.
- **Phase change** (boiling, condensation) — $h$ in the thousands to tens of
  thousands.

Cooling of a hot object follows the law: heat rate is linear in $\Delta T$, and
larger $h$ steepens the line:

```plot
{"title": "Newton's law of cooling: heat rate vs temperature difference", "xLabel": "T_s - T_inf (K)", "yLabel": "heat rate q (W)", "xRange": [0, 50], "yRange": [0, 600], "grid": true, "functions": [{"expr": "0.2*25*x", "label": "h=25 (forced air)", "color": "#2563eb"}, {"expr": "0.2*5*x", "label": "h=5 (natural air)", "color": "#16a34a"}]}
```

A lumped object cooling in time obeys $T(t)-T_\infty = (T_0-T_\infty)e^{-t/\tau}$
with $\tau = \rho V c_p/(hA)$ — exponential approach to ambient. We treat this
transient case quantitatively in the Intermediate course.

**Next:** radiation — heat exchanged as electromagnetic waves.
""",
        ),
        _t(
            "Radiation and the Stefan-Boltzmann law",
            "11 min",
            r"""
# Radiation and the Stefan-Boltzmann law

Every surface above absolute zero emits thermal radiation. A perfect emitter (a
**blackbody**) radiates at the maximum possible rate given by the
**Stefan-Boltzmann law**:

$$E_b = \sigma\,T^4, \qquad \sigma = 5.67\times10^{-8}\ \text{W/m}^2\text{K}^4,$$

with $T$ in **kelvin**. Real surfaces emit a fraction $\varepsilon$ (the
**emissivity**, $0 \le \varepsilon \le 1$) of this. The *net* exchange between a
small surface at $T_s$ and large surroundings at $T_{sur}$ is

$$q = \varepsilon\,\sigma\,A\,(T_s^4 - T_{sur}^4).$$

The fourth-power dependence makes radiation dominate at high temperature: a
furnace wall at 1000 K radiates far more than at 500 K. Note temperatures must be
absolute — a common student error is using °C in $T^4$.

```plot
{"title": "Blackbody emissive power vs temperature", "xLabel": "temperature T (100 K units)", "yLabel": "E_b (relative)", "xRange": [3, 10], "yRange": [0, 110], "grid": true, "functions": [{"expr": "0.01*x^4", "label": "E_b ~ T^4", "color": "#dc2626"}]}
```

Polished metals have low emissivity ($\varepsilon \approx 0.05$) and stay cool by
radiating little; oxidized or painted surfaces have $\varepsilon \approx 0.9$.
This is why spacecraft and vacuum flasks use shiny multilayer foils.

```python
sigma = 5.67e-8
eps, A = 0.9, 0.5
Ts, Tsur = 400.0, 300.0          # kelvin
q = eps * sigma * A * (Ts**4 - Tsur**4)
print(f"Net radiative heat rate = {q:.1f} W")  # -> ~446 W
```

**Next:** combining the modes with the energy balance.
""",
        ),
        _t(
            "Energy balance and steady-state",
            "10 min",
            r"""
# Energy balance and steady-state

Every heat-transfer problem rests on **conservation of energy**. For a control
volume:

$$\dot E_{in} - \dot E_{out} + \dot E_{gen} = \dot E_{st},$$

inflow minus outflow plus internal generation equals the rate of energy storage.
At **steady state** nothing accumulates ($\dot E_{st}=0$), so inflow plus
generation equals outflow.

A **surface energy balance** has no volume and no storage or generation, so it
simply says: heat arriving equals heat leaving. At a wall exposed to a fluid,
conduction *to* the surface equals convection plus radiation *away*:

$$\underbrace{\frac{k}{L}(T_i - T_s)}_{\text{conduction in}} =
\underbrace{h(T_s - T_\infty)}_{\text{convection out}} +
\underbrace{\varepsilon\sigma(T_s^4 - T_{sur}^4)}_{\text{radiation out}}.$$

This single equation lets you solve for an unknown surface temperature.

```mermaid
flowchart LR
  subgraph CV["Control volume"]
    GEN["E_gen (internal heating)"]
  end
  IN["E_in (q in)"] --> CV
  CV --> OUT["E_out (q out)"]
  CV --> ST["E_st (storage; 0 at steady state)"]
```

```plot
{"title": "Approach to steady state: stored energy decays", "xLabel": "time (units of tau)", "yLabel": "T - T_inf (relative)", "xRange": [0, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-x)", "label": "transient decays to steady state", "color": "#2563eb"}]}
```

The energy balance is the bookkeeping that ties conduction, convection and
radiation together — master it and every later problem becomes substitution.

**Next:** combining conduction across layers — the plane composite wall.
""",
        ),
        _t(
            "The plane wall and composite walls",
            "11 min",
            r"""
# The plane wall and composite walls

A wall is rarely one material — think brick + insulation + plaster, or a furnace
lining. Each layer is a **conduction resistance**, and layers in series add, just
like electrical resistors. This **thermal-circuit analogy** is the workhorse of
1-D steady conduction.

Define resistances:

$$R_{cond} = \frac{L}{kA}, \qquad R_{conv} = \frac{1}{hA}.$$

For heat flowing from a hot fluid through two solid layers into a cold fluid, the
resistances stack in series and the rate is

$$q = \frac{T_{\infty,1} - T_{\infty,2}}{R_{conv,1} + R_{cond,1} + R_{cond,2} + R_{conv,2}}.$$

The driving "voltage" is the overall temperature difference; the "current" is the
heat rate $q$, the same through every layer in series.

```mermaid
flowchart LR
  Th["T_inf,1 (hot fluid)"] --> Rci["R_conv,1"]
  Rci --> R1["R_cond layer 1"]
  R1 --> R2["R_cond layer 2"]
  R2 --> Rco["R_conv,2"]
  Rco --> Tc["T_inf,2 (cold fluid)"]
```

```python
def series_q(dT, resistances):
    R_total = sum(resistances)
    return dT / R_total          # heat rate through the series stack

# brick (0.1 m, k=0.7) + foam (0.05 m, k=0.03), A=10 m^2, h_in=10, h_out=25
A = 10.0
R = [1/(10*A), 0.1/(0.7*A), 0.05/(0.03*A), 1/(25*A)]
print(f"q = {series_q(20.0, R):.1f} W")  # foam dominates the resistance
```

The temperature drop across each layer is proportional to its resistance — the
insulating foam, despite being thin, carries most of the $\Delta T$.

**Next:** test your understanding of the three modes and the energy balance.
""",
        ),
        _quiz(),
    ),
)


# ── Heat Transfer — Intermediate ─────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="heat-transfer-intermediate",
    title="Heat Transfer — Intermediate",
    description=(
        "Core quantitative methods of heat transfer. Builds the thermal-resistance "
        "network for multidimensional and radial geometries, designs extended "
        "surfaces (fins) and their efficiency, develops the dimensionless groups "
        "(Reynolds, Prandtl, Nusselt) and the empirical correlations that give h, "
        "and solves transient conduction with the lumped-capacitance and Biot/Fourier "
        "framework. Worked Python/MATLAB throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Thermal resistance networks",
            "12 min",
            r"""
# Thermal resistance networks

The electrical analogy generalizes beyond plane walls. **Radial conduction**
through a cylindrical pipe wall of inner/outer radii $r_1, r_2$ and length $L$
has resistance

$$R_{cyl} = \frac{\ln(r_2/r_1)}{2\pi k L},$$

and a spherical shell has $R_{sph} = (1/r_1 - 1/r_2)/(4\pi k)$. Resistances in
**series** add; resistances in **parallel** combine reciprocally — useful when
heat can take two paths (e.g. a stud and the insulation beside it in a wall).

A subtlety for pipes: adding insulation increases conduction resistance but also
the outer area, *lowering* convection resistance. Below the **critical radius**
$r_c = k_{ins}/h$, adding insulation can actually *raise* heat loss — important
for thin wires and small tubes.

```plot
{"title": "Total resistance vs insulation outer radius (critical radius)", "xLabel": "outer radius r (units of r_c)", "yLabel": "total resistance (relative)", "xRange": [0.2, 3], "yRange": [0, 5], "grid": true, "functions": [{"expr": "log(x)+1/x", "label": "R_cond + R_conv (min at r_c)", "color": "#2563eb"}]}
```

```python
import numpy as np

def R_cyl(r1, r2, k, L):
    return np.log(r2 / r1) / (2 * np.pi * k * L)

def R_conv(r, h, L):
    return 1.0 / (h * 2 * np.pi * r * L)

k_ins, h, L = 0.05, 5.0, 1.0
r_c = k_ins / h                  # critical radius of insulation
print(f"critical radius r_c = {r_c*1000:.1f} mm")
```

**Next:** extended surfaces — fins — to beat the convection bottleneck.
""",
        ),
        _t(
            "Fins and extended surfaces",
            "13 min",
            r"""
# Fins and extended surfaces

When convection from a surface is the bottleneck ($hA$ too small), add **fins**
to increase area. The fin temperature falls along its length, so not all the
added area is fully effective. The 1-D fin equation (uniform cross-section,
constant properties) is

$$\frac{d^2\theta}{dx^2} - m^2\theta = 0, \qquad m = \sqrt{\frac{hP}{kA_c}},
\qquad \theta = T - T_\infty,$$

where $P$ is the perimeter and $A_c$ the cross-section. For a long fin the
temperature decays exponentially, $\theta(x) = \theta_b\,e^{-mx}$.

Two key metrics: **fin efficiency** $\eta_f = q_{fin}/(h A_{fin}\theta_b)$
(actual vs ideal isothermal fin), and **fin effectiveness**
$\varepsilon_f = q_{fin}/(h A_c \theta_b)$ (gain over the bare base). A fin is
only worthwhile when $\varepsilon_f > 2$ or so; high-$k$ material, thin profile
and low $h$ all help.

```plot
{"title": "Fin temperature excess vs distance from base", "xLabel": "x/L along fin", "yLabel": "theta/theta_b", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-2.5*x)", "label": "long fin (high mL)", "color": "#dc2626"}, {"expr": "exp(-0.8*x)", "label": "stubby fin (low mL)", "color": "#16a34a"}]}
```

```python
import numpy as np

h, k, t, w, L = 40.0, 200.0, 2e-3, 1.0, 0.05   # aluminium fin
P = 2 * (w + t)
Ac = w * t
m = np.sqrt(h * P / (k * Ac))
mL = m * L
eta_fin = np.tanh(mL) / mL        # efficiency of an adiabatic-tip fin
print(f"mL = {mL:.2f}, fin efficiency = {eta_fin:.3f}")
```

**Next:** the dimensionless numbers that govern convection.
""",
        ),
        _t(
            "Dimensionless numbers in convection",
            "12 min",
            r"""
# Dimensionless numbers in convection

Convection correlations are written in dimensionless form so one curve serves all
scales. The key groups:

- **Reynolds** $Re = \rho u L/\mu = uL/\nu$ — inertial vs viscous forces; sets
  laminar ($Re < 2300$ in pipes) vs turbulent flow.
- **Prandtl** $Pr = \nu/\alpha = \mu c_p/k$ — momentum vs thermal diffusivity; a
  fluid property ($\approx 0.7$ for air, $\approx 7$ for water, $\gg 1$ for oils).
- **Nusselt** $Nu = hL/k$ — dimensionless convection coefficient; the *output* we
  solve for, then invert to get $h = Nu\,k/L$.
- **Grashof / Rayleigh** $Gr, Ra = Gr\,Pr$ — buoyancy vs viscous forces, for
  natural convection.

The whole game is: find a correlation $Nu = f(Re, Pr)$ (or $f(Ra, Pr)$) for your
geometry, compute $Nu$, then recover $h$.

```mermaid
flowchart LR
  GEOM["Geometry + flow"] --> RE["Compute Re, Pr (or Ra)"]
  RE --> CORR["Pick correlation Nu = f(Re,Pr)"]
  CORR --> NU["Nu"]
  NU --> H["h = Nu*k/L"]
  H --> Q["q = h*A*dT"]
```

```python
import numpy as np
# air over a flat plate: properties at film temperature
rho, mu, k, cp = 1.06, 2.0e-5, 0.030, 1007.0
u, L = 10.0, 0.5
Re = rho * u * L / mu
Pr = mu * cp / k
print(f"Re = {Re:.0f}  Pr = {Pr:.3f}")   # turbulent if Re > ~5e5
```

**Next:** turning these numbers into h with empirical correlations.
""",
        ),
        _t(
            "Forced convection correlations",
            "13 min",
            r"""
# Forced convection correlations

With $Re$ and $Pr$ in hand, standard correlations give $Nu$. A few you will use
constantly:

**Flat plate, laminar, average:** $\overline{Nu}_L = 0.664\,Re_L^{1/2}Pr^{1/3}$
(valid $Re_L < 5\times10^5$, $Pr \gtrsim 0.6$).

**Internal pipe flow, turbulent (Dittus-Boelter):**
$$Nu_D = 0.023\,Re_D^{0.8}Pr^{n},$$
with $n = 0.4$ for heating the fluid and $n = 0.3$ for cooling it, valid for
$Re_D \gtrsim 10\,000$ and fully developed flow. $L$ here is the pipe diameter
$D$, and $h = Nu_D\,k/D$.

**Cylinder in cross-flow (Hilpert/Churchill-Bernstein)** and **sphere** have
their own forms. Always evaluate fluid properties at an appropriate mean
temperature (film temperature for external flow, bulk mean for internal).

```plot
{"title": "Dittus-Boelter: Nu vs Reynolds number (Pr=4, log-log feel)", "xLabel": "Re (10^4 units)", "yLabel": "Nu", "xRange": [1, 20], "yRange": [0, 400], "grid": true, "functions": [{"expr": "0.023*(10000*x)^0.8*4^0.4", "label": "Nu = 0.023 Re^0.8 Pr^0.4", "color": "#2563eb"}]}
```

```python
def dittus_boelter(Re, Pr, heating=True):
    n = 0.4 if heating else 0.3
    return 0.023 * Re**0.8 * Pr**n

Re, Pr, D, k = 5e4, 4.0, 0.025, 0.6   # water in a 25 mm tube
Nu = dittus_boelter(Re, Pr, heating=True)
h = Nu * k / D
print(f"Nu = {Nu:.1f}, h = {h:.0f} W/m2K")
```

**Next:** natural convection and the Rayleigh number.
""",
        ),
        _t(
            "Natural convection",
            "11 min",
            r"""
# Natural convection

Without a fan or pump, density differences from heating drive **buoyant** flow.
The governing group is the **Rayleigh number**

$$Ra_L = \frac{g\,\beta\,(T_s - T_\infty)\,L^3}{\nu\,\alpha},$$

where $\beta$ is the thermal expansion coefficient ($\beta = 1/T$ for an ideal
gas). Correlations take the form $\overline{Nu}_L = C\,Ra_L^{\,n}$ with $n=1/4$
in laminar and $n=1/3$ in turbulent regimes. For a vertical plate, Churchill-Chu
gives a single smooth expression spanning both.

Natural convection coefficients are small (a few W/m²·K in air), so natural-only
cooling limits power density — the reason CPUs need fans and why passive heat
sinks are large and finned. The cube-law on $L$ means small objects barely
convect naturally and lose proportionally more by radiation.

```plot
{"title": "Natural-convection Nu vs Rayleigh number (laminar exponent 1/4)", "xLabel": "Ra (10^6 units)", "yLabel": "Nu", "xRange": [0.1, 10], "yRange": [0, 60], "grid": true, "functions": [{"expr": "0.59*(1000000*x)^0.25", "label": "Nu = 0.59 Ra^(1/4)", "color": "#16a34a"}]}
```

```matlab
g = 9.81; beta = 1/300; nu = 1.6e-5; alpha = 2.2e-5; % air ~300 K
Ts = 350; Tinf = 300; L = 0.3;       % vertical plate, m
Ra = g*beta*(Ts-Tinf)*L^3/(nu*alpha);
Nu = 0.59*Ra^0.25;                   % laminar vertical plate
k = 0.026; h = Nu*k/L;
fprintf('Ra=%.2e  Nu=%.1f  h=%.2f W/m^2K\n', Ra, Nu, h);
```

**Next:** transient conduction and the lumped-capacitance model.
""",
        ),
        _t(
            "Transient conduction and lumped capacitance",
            "12 min",
            r"""
# Transient conduction and lumped capacitance

When a body is suddenly exposed to a different environment, its temperature
evolves in time. The simplest model assumes the body is **spatially isothermal**
(no internal gradients) — valid when internal conduction resistance is small
compared with surface convection resistance, measured by the **Biot number**

$$Bi = \frac{h\,L_c}{k}, \qquad L_c = \frac{V}{A_s}.$$

If $Bi < 0.1$, lumped capacitance applies and

$$\frac{T(t)-T_\infty}{T_0-T_\infty} = e^{-t/\tau}, \qquad
\tau = \frac{\rho V c_p}{h A_s}.$$

When $Bi > 0.1$, internal gradients matter and you need the 1-D transient
solution (one-term series with the **Fourier number** $Fo = \alpha t/L_c^2$, or
Heisler charts).

```plot
{"title": "Lumped-capacitance cooling: dimensionless temperature vs time", "xLabel": "t / tau", "yLabel": "(T - T_inf)/(T0 - T_inf)", "xRange": [0, 5], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-x)", "label": "exponential decay", "color": "#dc2626"}]}
```

```python
import numpy as np
rho, V, cp, h, As = 8000.0, 1e-5, 500.0, 100.0, 6e-4   # small steel sphere
k, Lc = 50.0, V / As
Bi = h * Lc / k
tau = rho * V * cp / (h * As)
t = 120.0                                # seconds
theta = np.exp(-t / tau)
print(f"Bi = {Bi:.3f} ({'lumped OK' if Bi < 0.1 else 'use 1-D solution'})")
print(f"tau = {tau:.0f} s, theta(120 s) = {theta:.3f}")
```

**Next:** test your quantitative heat-transfer methods.
""",
        ),
        _quiz(),
    ),
)


# ── Heat Transfer — Advanced ─────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="heat-transfer-advanced",
    title="Heat Transfer — Advanced",
    description=(
        "State-of-the-art and applied heat transfer. Designs heat exchangers with "
        "the LMTD and effectiveness-NTU methods, treats boiling and condensation, "
        "develops the finite-difference / CFD numerical solution of the heat "
        "equation, models radiation exchange with view factors, and closes with "
        "thermal design optimization and surrogate/ML-assisted methods. Worked "
        "Python and MATLAB throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Heat exchangers and the LMTD method",
            "13 min",
            r"""
# Heat exchangers and the LMTD method

A **heat exchanger** transfers heat between two fluids without mixing them
(double-pipe, shell-and-tube, plate, cross-flow). The overall conductance is
captured by the **overall heat-transfer coefficient** $U$, combining both
convection films and the wall (plus fouling):

$$\frac{1}{UA} = \frac{1}{h_i A_i} + R_{wall} + R_{foul} + \frac{1}{h_o A_o}.$$

For design, the **Log-Mean Temperature Difference** method gives

$$q = U A\,\Delta T_{lm}, \qquad
\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1/\Delta T_2)},$$

where $\Delta T_1, \Delta T_2$ are the end temperature differences. For
multi-pass and cross-flow units, multiply by a correction factor $F$.
Counterflow extracts more heat than parallel flow for the same areas.

```mermaid
flowchart LR
  HIN["Hot in (T_h,i)"] --> HX["Heat exchanger UA"]
  CIN["Cold in (T_c,i)"] --> HX
  HX --> HOUT["Hot out (T_h,o)"]
  HX --> COUT["Cold out (T_c,o)"]
```

```python
import numpy as np

def lmtd(dT1, dT2):
    return (dT1 - dT2) / np.log(dT1 / dT2)

Th_i, Th_o = 120.0, 80.0       # hot fluid degC
Tc_i, Tc_o = 20.0, 60.0        # cold fluid degC (counterflow)
dT1, dT2 = Th_i - Tc_o, Th_o - Tc_i
UA = 2000.0
q = UA * lmtd(dT1, dT2)
print(f"LMTD = {lmtd(dT1, dT2):.1f} K, q = {q/1000:.1f} kW")
```

**Next:** rating exchangers when outlet temperatures are unknown — effectiveness-NTU.
""",
        ),
        _t(
            "Effectiveness-NTU design method",
            "13 min",
            r"""
# Effectiveness-NTU design method

LMTD needs the outlet temperatures; for a *rating* problem (given $UA$ and inlet
conditions, find performance) the **effectiveness-NTU** method is cleaner.
Define the heat-capacity rates $C = \dot m c_p$, with $C_{min}, C_{max}$ the
smaller and larger. Then

$$\text{NTU} = \frac{UA}{C_{min}}, \qquad C_r = \frac{C_{min}}{C_{max}},
\qquad \varepsilon = \frac{q}{q_{max}}, \qquad q_{max} = C_{min}(T_{h,i}-T_{c,i}).$$

Each configuration has an $\varepsilon = f(\text{NTU}, C_r)$ relation. For
counterflow,

$$\varepsilon = \frac{1 - e^{-\text{NTU}(1-C_r)}}{1 - C_r\,e^{-\text{NTU}(1-C_r)}}.$$

Effectiveness rises with NTU but with diminishing returns — past NTU ≈ 3–4,
adding area buys little. This curve drives the size/cost trade-off.

```plot
{"title": "Effectiveness vs NTU (counterflow, Cr=0.5) - diminishing returns", "xLabel": "NTU", "yLabel": "effectiveness", "xRange": [0, 6], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "(1-exp(-x*0.5))/(1-0.5*exp(-x*0.5))", "label": "epsilon (Cr=0.5)", "color": "#2563eb"}]}
```

```python
import numpy as np

def eps_counterflow(NTU, Cr):
    if abs(Cr - 1.0) < 1e-9:
        return NTU / (1 + NTU)
    e = np.exp(-NTU * (1 - Cr))
    return (1 - e) / (1 - Cr * e)

UA, Cmin, Cmax = 2000.0, 1500.0, 3000.0
NTU, Cr = UA / Cmin, Cmin / Cmax
eps = eps_counterflow(NTU, Cr)
qmax = Cmin * (120.0 - 20.0)
print(f"NTU={NTU:.2f} eps={eps:.3f} q={eps*qmax/1000:.1f} kW")
```

**Next:** the high-h regimes — boiling and condensation.
""",
        ),
        _t(
            "Boiling and condensation",
            "12 min",
            r"""
# Boiling and condensation

Phase-change heat transfer achieves enormous coefficients because latent heat is
absorbed/released at nearly constant temperature. The **pool boiling curve**
(Nukiyama) plots heat flux against wall superheat $\Delta T_e = T_s - T_{sat}$:

- **Free convection** boiling at small superheat.
- **Nucleate** boiling — bubbles form at sites; the workhorse regime, very high
  flux, well predicted by the **Rohsenow correlation**.
- The **critical heat flux (CHF)** — the peak; exceeding it triggers...
- **Film boiling** — an insulating vapor blanket forms, flux drops and wall
  temperature can spike catastrophically (burnout).

Designers stay safely below CHF. **Condensation** (Nusselt's falling-film theory)
likewise gives large $h$; dropwise condensation beats filmwise.

```plot
{"title": "Pool boiling curve (heat flux vs wall superheat, schematic)", "xLabel": "wall superheat dT_e (relative)", "yLabel": "heat flux q'' (relative)", "xRange": [0.2, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*(x-3)^2)", "label": "nucleate peak ~ CHF then film boiling", "color": "#dc2626"}]}
```

```python
import numpy as np
# Rohsenow nucleate pool boiling (water on a surface)
rho_l, rho_v, sigma = 957.9, 0.6, 0.0589
hfg, mu_l, cp_l, Pr_l = 2257e3, 279e-6, 4217.0, 1.76
Csf, n, g = 0.013, 1.0, 9.81
dTe = 10.0                       # superheat, K
qpp = mu_l*hfg*np.sqrt(g*(rho_l-rho_v)/sigma)*(cp_l*dTe/(Csf*hfg*Pr_l**n))**3
print(f"nucleate boiling flux = {qpp/1e3:.0f} kW/m2")
```

**Next:** solving conduction numerically when geometry is complex.
""",
        ),
        _t(
            "Numerical conduction and CFD",
            "13 min",
            r"""
# Numerical conduction and CFD

Real geometries lack closed-form solutions. The **heat equation**

$$\frac{\partial T}{\partial t} = \alpha\nabla^2 T + \frac{\dot q}{\rho c_p}$$

is discretized on a grid. For 2-D steady conduction, a central finite-difference
on a uniform mesh gives the classic five-point stencil: each interior node is the
average of its four neighbours,

$$T_{i,j} = \tfrac{1}{4}\,(T_{i+1,j}+T_{i-1,j}+T_{i,j+1}+T_{i,j-1}),$$

solved by Gauss-Seidel/SOR iteration or a sparse direct solver. Transient
problems add stability limits — explicit schemes require $Fo \le 1/2$ (1-D) for
stability; implicit (Crank-Nicolson) schemes are unconditionally stable. Full
**CFD** (finite volume, e.g. OpenFOAM/ANSYS Fluent) couples this with the
Navier-Stokes equations to resolve convection too.

```plot
{"title": "Explicit scheme: error decay vs iterations (convergence)", "xLabel": "iteration (10s)", "yLabel": "residual (relative)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "iterative convergence", "color": "#16a34a"}]}
```

```python
import numpy as np

def laplace_2d(n=41, tol=1e-5):
    T = np.zeros((n, n))
    T[0, :] = 100.0              # top edge hot, others 0 (Dirichlet BCs)
    for _ in range(20000):
        Tn = T.copy()
        T[1:-1, 1:-1] = 0.25 * (
            Tn[2:, 1:-1] + Tn[:-2, 1:-1] + Tn[1:-1, 2:] + Tn[1:-1, :-2]
        )
        if np.max(np.abs(T - Tn)) < tol:
            break
    return T

T = laplace_2d()
print(f"centre temperature = {T[20, 20]:.2f} degC")
```

**Next:** radiation exchange between surfaces with view factors.
""",
        ),
        _t(
            "Radiation exchange and view factors",
            "12 min",
            r"""
# Radiation exchange and view factors

Between multiple surfaces, radiation depends on geometry through the **view
factor** $F_{ij}$ — the fraction of radiation leaving surface $i$ that strikes
$j$. Two rules: **reciprocity** $A_i F_{ij} = A_j F_{ji}$ and the **summation
rule** $\sum_j F_{ij} = 1$ for an enclosure.

For an enclosure of diffuse-gray surfaces, the **radiosity network** uses surface
resistances $(1-\varepsilon_i)/(\varepsilon_i A_i)$ and space resistances
$1/(A_i F_{ij})$, solved exactly like a resistor network with blackbody emissive
powers $E_b = \sigma T^4$ as the "potentials". For two large parallel plates,

$$q_{12} = \frac{\sigma A (T_1^4 - T_2^4)}{1/\varepsilon_1 + 1/\varepsilon_2 - 1}.$$

**Radiation shields** (extra low-emissivity sheets) add resistances in series and
sharply cut net exchange — the principle behind multilayer insulation on
satellites.

```mermaid
flowchart LR
  E1["E_b1 = sigma T1^4"] --> SR1["surface R1"]
  SR1 --> J1["radiosity J1"]
  J1 --> SPACE["space R = 1/(A F12)"]
  SPACE --> J2["radiosity J2"]
  J2 --> SR2["surface R2"]
  SR2 --> E2["E_b2 = sigma T2^4"]
```

```python
sigma = 5.67e-8
eps1, eps2, A = 0.8, 0.5, 2.0
T1, T2 = 800.0, 500.0            # kelvin, parallel plates
q = sigma * A * (T1**4 - T2**4) / (1/eps1 + 1/eps2 - 1)
print(f"net radiative exchange = {q/1000:.2f} kW")
```

**Next:** optimizing thermal designs with simulation and ML.
""",
        ),
        _t(
            "Thermal design optimization and ML",
            "13 min",
            r"""
# Thermal design optimization and ML

Modern thermal design is an **optimization** problem: minimize a heat sink's mass
or pumping power subject to a junction-temperature limit. The design vector might
be fin count, thickness, height and pitch; the objective and constraints come
from the correlations and networks of the earlier lessons.

Because each high-fidelity CFD evaluation is expensive, engineers fit a
**surrogate** (Gaussian-process or neural-network regressor) to a sampled design
set, then optimize the cheap surrogate and verify with CFD — **Bayesian /
surrogate-based optimization**. Topology optimization and physics-informed neural
networks (PINNs) push this further, learning conduction paths or temperature
fields directly.

```plot
{"title": "Surrogate-based optimization: objective vs iteration", "xLabel": "design iteration", "yLabel": "thermal resistance (relative)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "convergence to optimum", "color": "#2563eb"}]}
```

```python
import numpy as np
from scipy.optimize import minimize

def thermal_resistance(x):
    n, t = x                      # fin count, fin thickness (mm)
    h, k, H, base = 40.0, 200.0, 0.04, 0.1
    Ac = (t*1e-3) * 0.1
    P = 2 * (0.1 + t*1e-3)
    m = np.sqrt(h * P / (k * Ac))
    eta = np.tanh(m*H) / (m*H)
    A_fin = n * P * H
    UA = h * eta * A_fin + h * (base*0.1 - n*Ac)
    return 1.0 / UA               # minimize R_th = 1/(UA)

res = minimize(thermal_resistance, x0=[20, 2.0],
               bounds=[(5, 60), (0.5, 5.0)])
print(f"optimal fins={res.x[0]:.0f}, t={res.x[1]:.2f} mm, R_th={res.fun:.4f} K/W")
```

This closes the arc: from Fourier's law to AI-assisted heat-sink design.

**Next:** the final assessment across the whole track.
""",
        ),
        _quiz(),
    ),
)


HEAT_TRANSFER_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["HEAT_TRANSFER_COURSES"]
