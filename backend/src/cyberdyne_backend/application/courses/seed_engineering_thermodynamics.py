"""Engineering Thermodynamics track: Basics -> Intermediate -> Advanced.

University-level classical thermodynamics from properties, work and heat through
the first and second laws and entropy to power and refrigeration cycles (Otto,
Diesel, Rankine, Brayton). Lessons use interactive ```plot blocks (T-s/p-v
diagrams, efficiency curves), ```mermaid diagrams (control volumes, cycle
schematics) and runnable ```python/```matlab code (CoolProp-style property
calls, cycle solvers, exergy and optimization loops).
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Engineering Thermodynamics — Basics ───────────────────────────────────────

_BASICS = SeedCourse(
    slug="engineering-thermodynamics-basics",
    title="Engineering Thermodynamics — Basics",
    description=(
        "The vocabulary of thermodynamics built from intuition: systems and "
        "control volumes, properties and state, temperature and the zeroth law, "
        "the ideal gas, and the two currencies of energy transfer - work and "
        "heat. With p-v diagrams, process schematics and worked numbers."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Systems, surroundings and control volumes",
            "10 min",
            r"""
# Systems, surroundings and control volumes

Thermodynamics is the bookkeeping of energy. Before any equation, you must draw a
boundary and decide what is *inside* (the **system**) and what is *outside* (the
**surroundings**). The boundary may be real (a piston wall) or imaginary (a plane
across a pipe).

```mermaid
flowchart LR
  subgraph CV["Control volume"]
    T[Turbine]
  end
  IN[mass in, h1] --> CV
  CV --> OUT[mass out, h2]
  Q[heat Q] --> CV
  CV --> W[shaft work W]
```

Two framings dominate engineering:

- **Closed system (control mass).** No mass crosses the boundary; energy may.
  Example: gas trapped in a sealed cylinder. Bookkeeping is per *unit mass m*.
- **Open system (control volume).** Mass *and* energy cross the boundary. Example:
  a turbine, pump or nozzle with flowing fluid. Bookkeeping uses *mass flow rate*
  $\dot m$.

An **isolated system** exchanges neither mass nor energy. A boundary that blocks
heat is **adiabatic**; one that allows only heat is **diathermal**.

Choosing the boundary well is half the problem: put it where you know the states.
For a steam power plant we analyse each device (boiler, turbine, condenser, pump)
as its own control volume, then chain them.

**Next:** what we are allowed to measure - properties and state.
""",
        ),
        _t(
            "Properties, state and the ideal gas",
            "12 min",
            r"""
# Properties, state and the ideal gas

A **property** is a measurable characteristic of a system at equilibrium:
pressure $p$, temperature $T$, specific volume $v$, internal energy $u$, enthalpy
$h$, entropy $s$. Properties are either **intensive** (independent of size: $p$,
$T$, $v$) or **extensive** (scale with mass: $V$, $U$, $S$).

The **state** is the full set of property values. The **state postulate** says a
simple compressible substance's state is fixed by **two independent intensive
properties**. Fix two, and all the rest follow.

For gases at low density the **ideal gas law** links them:

$$pv = RT \qquad pV = mRT$$

with $R = R_u/M$ the specific gas constant ($R_u = 8.314$ J/mol·K). For air,
$R = 287$ J/kg·K. Isotherms ($pv = \text{const}$) are hyperbolas on a p-v diagram:

```plot
{"title": "Ideal-gas isotherms p = RT/v (air)", "xLabel": "specific volume v (m^3/kg)", "yLabel": "pressure p (kPa)", "xRange": [0.2, 1.5], "yRange": [0, 500], "grid": true, "functions": [{"expr": "287*300/x/1000", "label": "T=300 K", "color": "#2563eb"}, {"expr": "287*450/x/1000", "label": "T=450 K", "color": "#dc2626"}]}
```

Real substances near phase change need property **tables** or equations of state
(e.g. CoolProp), but the ideal gas captures air, combustion gases and many cycles
to within a few percent.

**Next:** how we agree on "hotter" - temperature and the zeroth law.
""",
        ),
        _t(
            "Temperature and the zeroth law",
            "9 min",
            r"""
# Temperature and the zeroth law

Temperature is the property that decides the *direction* of heat flow: energy
moves spontaneously from hot to cold. But what makes a thermometer trustworthy?
The **zeroth law of thermodynamics**:

> If two bodies are each in thermal equilibrium with a third, they are in thermal
> equilibrium with each other.

```mermaid
flowchart LR
  A[Body A] --- C[Thermometer C]
  B[Body B] --- C
  A -. "same reading => equal T" .- B
```

This is exactly what licenses a thermometer: the third body C carries a
reproducible property (column height, resistance, EMF) we call temperature. It
sounds obvious, but it is an independent axiom - hence "zeroth".

**Scales.** The **Kelvin** scale is absolute and thermodynamic: $T(\text{K}) =
T(^{\circ}\text{C}) + 273.15$. All thermodynamic relations (ideal gas, Carnot
efficiency, entropy) demand absolute temperature. The ideal-gas thermometer
extrapolates pressure to zero to define $0$ K.

```plot
{"title": "Constant-volume gas thermometer: p vs T (linear)", "xLabel": "temperature T (K)", "yLabel": "pressure p (kPa)", "xRange": [0, 600], "yRange": [0, 200], "grid": true, "functions": [{"expr": "0.3*x", "label": "p ∝ T at fixed v", "color": "#16a34a"}]}
```

The straight line through the origin in Kelvin is why $-273.15\,^{\circ}$C is
absolute zero: extrapolated, the gas pressure would vanish.

**Next:** the first currency of energy transfer - work.
""",
        ),
        _t(
            "Work: the boundary integral",
            "11 min",
            r"""
# Work: the boundary integral

**Work** is energy transfer driven by a force acting through a distance - the
organised, "useful" form. For a closed system whose volume changes against
pressure, the **boundary (p-dV) work** is

$$W = \int_{1}^{2} p \, dV$$

so on a **p-v diagram the work is the area under the process curve**. Sign
convention (engineering): work *done by* the system is positive.

```plot
{"title": "p-V work = area under the process path", "xLabel": "volume V (m^3)", "yLabel": "pressure p (kPa)", "xRange": [0.2, 1.5], "yRange": [0, 400], "grid": true, "functions": [{"expr": "120/x", "label": "isothermal pV=const", "color": "#2563eb"}]}
```

Special cases:

- **Isobaric** ($p$ const): $W = p(V_2 - V_1)$.
- **Isothermal ideal gas**: $W = mRT \ln(V_2/V_1)$.
- **Polytropic** ($pV^n = C$): $W = (p_2 V_2 - p_1 V_1)/(1-n)$ for $n \neq 1$.

Work is a **path function**, not a property: it depends on *how* you get from 1
to 2, not just the endpoints. That is why we write $\delta W$ (inexact
differential), never $dW$.

```python
import numpy as np
# Isothermal compression of 1 kg air, T=300 K, V1=0.86 -> V2=0.43 m^3
R, T, m = 287.0, 300.0, 1.0
V1, V2 = 0.86, 0.43
W = m * R * T * np.log(V2 / V1)
print(f"Boundary work = {W/1000:.1f} kJ")  # negative: work done ON the gas
```

**Next:** the other currency - heat - and the first law that ties them together.
""",
        ),
        _t(
            "Heat and the first law for closed systems",
            "12 min",
            r"""
# Heat and the first law for closed systems

**Heat** $Q$ is energy transfer driven by a *temperature difference* - the
disorganised counterpart to work. Like work it is a **path function** ($\delta
Q$), not a property. The **first law of thermodynamics** is conservation of
energy for a closed system:

$$Q - W = \Delta U \qquad \text{or} \qquad \delta Q - \delta W = dU$$

Heat in minus work out equals the rise in **internal energy** $U$ (a property).
For an ideal gas $U$ depends on temperature alone: $\Delta U = m c_v \Delta T$.

```mermaid
flowchart LR
  Q[Heat Q in] --> SYS[Closed system, ΔU]
  SYS --> W[Work W out]
```

Define **enthalpy** $H = U + pV$ to simplify constant-pressure processes:
$Q_p = \Delta H = m c_p \Delta T$. The two specific heats satisfy
**Mayer's relation** $c_p - c_v = R$, and their ratio is $\gamma = c_p/c_v$
($\approx 1.4$ for air).

A constant-pressure heating shows the linear $Q$-$T$ trend:

```plot
{"title": "Constant-pressure heating: Q = m*cp*(T-T1), air", "xLabel": "temperature T (K)", "yLabel": "heat added Q (kJ/kg)", "xRange": [300, 800], "yRange": [0, 520], "grid": true, "functions": [{"expr": "1.005*(x-300)", "label": "cp=1.005 kJ/kg.K", "color": "#dc2626"}]}
```

```python
cv, cp, R = 0.718, 1.005, 0.287  # kJ/kg.K for air
dT = 200.0
print(f"dU = {cv*dT:.1f} kJ/kg,  dH = {cp*dT:.1f} kJ/kg")
```

**Next:** quick check on the language and laws you now command.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Thermodynamics — Intermediate ─────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="engineering-thermodynamics-intermediate",
    title="Engineering Thermodynamics — Intermediate",
    description=(
        "The quantitative core: the first law for open systems (SFEE), the "
        "second law and Carnot limit, entropy and isentropic processes, and a "
        "first full pass at the Rankine vapour power cycle - with property-table "
        "code, T-s diagrams and component-by-component energy balances."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "First law for control volumes (SFEE)",
            "12 min",
            r"""
# First law for control volumes (SFEE)

Most machines are *open*: fluid flows through. The **Steady-Flow Energy Equation
(SFEE)** is the first law written per unit time for a control volume at steady
state ($d/dt = 0$, $\sum \dot m_{in} = \sum \dot m_{out}$):

$$\dot Q - \dot W_s = \sum_{out}\dot m\left(h + \tfrac{V^2}{2} + gz\right) - \sum_{in}\dot m\left(h + \tfrac{V^2}{2} + gz\right)$$

Enthalpy $h$ appears (not $u$) because flow work $pv$ is bundled in. For a single
inlet/outlet, dividing by $\dot m$:

$$q - w_s = (h_2 - h_1) + \tfrac{1}{2}(V_2^2 - V_1^2) + g(z_2 - z_1)$$

```mermaid
flowchart LR
  I["in: h1, V1"] --> D[Device]
  Qd[Q] --> D
  D --> Ws[shaft work Ws]
  D --> O["out: h2, V2"]
```

Device idealisations drop terms:

- **Turbine / pump / compressor:** $w_s = h_1 - h_2$ (adiabatic, KE/PE small).
- **Nozzle:** adiabatic, no shaft work, KE matters: $V_2 = \sqrt{V_1^2 + 2(h_1-h_2)}$.
- **Throttle (valve):** $h_1 = h_2$ (isenthalpic).
- **Heat exchanger:** $\dot Q = \dot m(h_2 - h_1)$, no shaft work.

```python
# Adiabatic steam turbine power, single inlet/outlet
mdot = 20.0        # kg/s
h1, h2 = 3450.0, 2300.0   # kJ/kg (inlet, outlet)
Wdot = mdot * (h1 - h2)
print(f"Turbine power = {Wdot/1000:.2f} MW")
```

**Next:** why energy balance alone cannot tell you which way a process runs.
""",
        ),
        _t(
            "The second law and the Carnot limit",
            "12 min",
            r"""
# The second law and the Carnot limit

The first law forbids creating energy; it does **not** forbid a cup of coffee
spontaneously reheating itself. The **second law** supplies direction. Two
classic statements:

- **Kelvin-Planck:** no cycle can convert heat *entirely* into work from a single
  reservoir. Some heat must be rejected.
- **Clausius:** heat cannot flow from cold to hot with no other effect (a fridge
  needs work input).

```mermaid
flowchart TB
  H[Hot reservoir TH] -->|QH| E[Heat engine]
  E -->|W| L[Load]
  E -->|QL rejected| C[Cold reservoir TL]
```

The best *any* engine between two reservoirs can do is the reversible **Carnot
efficiency**, a function of absolute temperatures only:

$$\eta_{Carnot} = 1 - \frac{T_L}{T_H}$$

Real, irreversible engines fall below this ceiling. The curve shows why high
$T_H$ (or low $T_L$) is worth chasing:

```plot
{"title": "Carnot efficiency vs TH (TL = 300 K)", "xLabel": "hot source temperature TH (K)", "yLabel": "max efficiency", "xRange": [300, 1500], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1-300/x", "label": "1 - TL/TH", "color": "#16a34a"}]}
```

For refrigerators and heat pumps the limit is a **coefficient of performance**:
$COP_{ref} = T_L/(T_H - T_L)$, $COP_{hp} = T_H/(T_H - T_L)$.

**Next:** the property that turns the second law into an equation - entropy.
""",
        ),
        _t(
            "Entropy and isentropic processes",
            "13 min",
            r"""
# Entropy and isentropic processes

The second law gets a property: **entropy** $S$, defined via the reversible heat
transfer

$$dS = \left(\frac{\delta Q}{T}\right)_{rev} \qquad \Delta S = \int \frac{\delta Q_{rev}}{T}$$

The **Clausius inequality** $\oint \delta Q/T \le 0$ gives the **entropy balance**
for a control volume:

$$\Delta S_{gen} = \Delta S_{sys} - \sum \frac{Q_k}{T_k} \ge 0$$

Entropy generation $S_{gen} \ge 0$ measures irreversibility; it is zero only for a
reversible process. A **reversible adiabatic** process therefore has $S_{gen}=0$
and $Q=0$, i.e. constant entropy - **isentropic**. For an ideal gas with constant
specific heats:

$$\frac{T_2}{T_1} = \left(\frac{p_2}{p_1}\right)^{(\gamma-1)/\gamma} = \left(\frac{v_1}{v_2}\right)^{\gamma-1}$$

On a **T-s diagram**, area under a reversible path is heat. An ideal-gas isobar
$T = T_1 \exp(s/c_p)$ rises exponentially in $s$:

```plot
{"title": "Ideal-gas isobar on T-s: T = T1*exp(s/cp)", "xLabel": "entropy change s - s1 (kJ/kg.K)", "yLabel": "temperature T (K)", "xRange": [0, 1.5], "yRange": [300, 1400], "grid": true, "functions": [{"expr": "300*exp(x/1.005)", "label": "p = const", "color": "#2563eb"}]}
```

Component efficiency uses the isentropic case as the yardstick - e.g. turbine
$\eta_T = (h_1 - h_2)/(h_1 - h_{2s})$.

```python
# Isentropic outlet temperature, air, gamma=1.4
gamma = 1.4
T1, p1, p2 = 300.0, 100.0, 800.0   # K, kPa
T2s = T1 * (p2/p1)**((gamma-1)/gamma)
print(f"T2s = {T2s:.1f} K")
```

**Next:** assemble these tools into a real power plant - the Rankine cycle.
""",
        ),
        _t(
            "The Rankine vapour power cycle",
            "14 min",
            r"""
# The Rankine vapour power cycle

The **Rankine cycle** is how most of the world makes electricity (coal, nuclear,
solar-thermal, combined-cycle bottoming). Water is the working fluid; it changes
phase, which keeps the pump cheap (pumping liquid costs far less than compressing
vapour).

```mermaid
flowchart LR
  P[Pump] -->|2| B[Boiler]
  B -->|3| T[Turbine]
  T -->|4| C[Condenser]
  C -->|1| P
  B -. Qin .-> B
  C -. Qout .-> C
  T -. Wt .-> T
```

Four ideal processes (numbering 1->2->3->4):

1. **1->2 Pump (isentropic):** $w_p = h_2 - h_1 \approx v_1(p_2 - p_1)$.
2. **2->3 Boiler (isobaric):** $q_{in} = h_3 - h_2$.
3. **3->4 Turbine (isentropic):** $w_t = h_3 - h_4$.
4. **4->1 Condenser (isobaric):** $q_{out} = h_4 - h_1$.

Thermal efficiency:

$$\eta = \frac{w_t - w_p}{q_{in}} = 1 - \frac{q_{out}}{q_{in}}$$

Raising boiler pressure/temperature or lowering condenser pressure all raise
$\eta$ - the same Carnot intuition. Efficiency climbs with mean boiler pressure:

```plot
{"title": "Rankine efficiency trend vs boiler pressure", "xLabel": "boiler pressure (MPa)", "yLabel": "thermal efficiency", "xRange": [2, 20], "yRange": [0.3, 0.5], "grid": true, "functions": [{"expr": "0.30+0.05*log(x)", "label": "η rises with log(p)", "color": "#16a34a"}]}
```

```python
# Ideal Rankine (illustrative property values, kJ/kg)
h1, h2 = 191.8, 200.0      # condenser exit (sat liq), pump exit
h3, h4 = 3450.0, 2360.0    # boiler exit, turbine exit
wt, wp = h3 - h4, h2 - h1
qin = h3 - h2
print(f"eta = {(wt-wp)/qin:.3f}")
```

**Next:** test your grasp of open-system balances, the second law and Rankine.
""",
        ),
        _t(
            "Improving Rankine: reheat and regeneration",
            "12 min",
            r"""
# Improving Rankine: reheat and regeneration

The ideal Rankine cycle is a starting point; real plants squeeze more out of the
fuel with two refinements that raise the *mean temperature of heat addition*.

**Reheat.** Expanding all the way in one turbine stage drives the steam wet
(droplets erode blades). Instead, expand partway, return the steam to the boiler
for a **reheat** to high temperature, then expand again. This keeps turbine exit
quality high and adds work.

```mermaid
flowchart LR
  B[Boiler] --> HP[HP turbine]
  HP --> RH[Reheater]
  RH --> LP[LP turbine]
  LP --> C[Condenser]
  C --> P[Pump] --> B
```

**Regeneration.** Bleed (extract) some steam partway through the turbine and use
it to **preheat the feedwater** in a feedwater heater. Less cold liquid enters the
boiler, so the average heat-addition temperature rises and external heat input
drops - directly improving $\eta$.

$$\eta_{regen} = 1 - \frac{q_{out}}{q_{in}}, \quad q_{in}\downarrow \Rightarrow \eta\uparrow$$

Combined, modern supercritical reheat-regenerative plants reach ~45-48% thermal
efficiency. Adding feedwater heaters shows diminishing returns:

```plot
{"title": "Efficiency gain vs number of feedwater heaters", "xLabel": "number of feedwater heaters", "yLabel": "efficiency gain (points)", "xRange": [0, 8], "yRange": [0, 6], "grid": true, "functions": [{"expr": "6*(1-exp(-0.4*x))", "label": "diminishing returns", "color": "#dc2626"}]}
```

```python
# Optimal open-FWH extraction pressure ~ geometric mean of boiler & condenser p
p_boiler, p_cond = 15000.0, 10.0  # kPa
p_extract = (p_boiler * p_cond) ** 0.5
print(f"Suggested extraction pressure ~ {p_extract:.0f} kPa")
```

**Next:** consolidate the intermediate cycle toolkit.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Thermodynamics — Advanced ─────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="engineering-thermodynamics-advanced",
    title="Engineering Thermodynamics — Advanced",
    description=(
        "State-of-the-art and applied cycles: gas-power cycles (Otto, Diesel, "
        "Brayton) with air-standard analysis, refrigeration and heat pumps, "
        "exergy (availability) accounting, and computational cycle "
        "optimization - with CoolProp-style property code and numeric solvers."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Gas-power cycles: Otto and Diesel",
            "13 min",
            r"""
# Gas-power cycles: Otto and Diesel

Internal-combustion engines are modelled with the **air-standard** abstraction:
air as an ideal gas, combustion replaced by heat addition, exhaust by heat
rejection. Two staples:

**Otto cycle** (spark ignition) - heat added at *constant volume*:

$$\eta_{Otto} = 1 - \frac{1}{r^{\,\gamma-1}}, \qquad r = \frac{V_1}{V_2}$$

Efficiency depends only on **compression ratio** $r$ and $\gamma$. Knock limits
gasoline engines to $r \approx 8$-$11$.

**Diesel cycle** (compression ignition) - heat added at *constant pressure*:

$$\eta_{Diesel} = 1 - \frac{1}{r^{\,\gamma-1}}\,\frac{r_c^{\gamma}-1}{\gamma(r_c-1)}$$

with cutoff ratio $r_c = V_3/V_2$. Diesels run higher $r$ ($\approx 14$-$22$), so
despite the cutoff penalty they out-efficiency gasoline engines.

```mermaid
flowchart LR
  A["1: BDC"] -->|isentropic compress| B["2: TDC"]
  B -->|heat in| C["3"]
  C -->|isentropic expand| D["4"]
  D -->|heat reject| A
```

Otto efficiency vs compression ratio:

```plot
{"title": "Air-standard Otto efficiency vs compression ratio", "xLabel": "compression ratio r", "yLabel": "thermal efficiency", "xRange": [4, 16], "yRange": [0.3, 0.7], "grid": true, "functions": [{"expr": "1-1/(x^0.4)", "label": "1 - 1/r^(γ-1), γ=1.4", "color": "#2563eb"}]}
```

```python
import numpy as np
gamma = 1.4
for r in (8, 10, 18):
    eta = 1 - 1/r**(gamma-1)
    print(f"r={r:2d}  eta_Otto={eta:.3f}")
```

**Next:** the gas-turbine cousin - the Brayton cycle.
""",
        ),
        _t(
            "The Brayton cycle and gas turbines",
            "13 min",
            r"""
# The Brayton cycle and gas turbines

The **Brayton cycle** powers jet engines and combined-cycle plants: compress air,
burn fuel at constant pressure, expand through a turbine. Air-standard, the ideal
efficiency depends only on the **pressure ratio** $r_p = p_2/p_1$:

$$\eta_{Brayton} = 1 - \frac{1}{r_p^{\,(\gamma-1)/\gamma}}$$

```mermaid
flowchart LR
  IN[air in] --> C[Compressor]
  C --> CC[Combustor, Qin]
  CC --> T[Turbine]
  T --> OUT[exhaust, Qout]
  T -.->|shaft| C
```

But efficiency is not the whole story: **net specific work** has an optimum
pressure ratio, peaking near $r_{p,opt} = (T_3/T_1)^{\gamma/[2(\gamma-1)]}$. Push
$r_p$ too high and the compressor eats the turbine's output. **Real** machines
add component efficiencies, and the **back-work ratio** (compressor work / turbine
work) is large (~40-60%), so isentropic efficiencies dominate performance.

Efficiency vs pressure ratio:

```plot
{"title": "Ideal Brayton efficiency vs pressure ratio", "xLabel": "pressure ratio rp", "yLabel": "thermal efficiency", "xRange": [2, 40], "yRange": [0.2, 0.7], "grid": true, "functions": [{"expr": "1-1/(x^0.2857)", "label": "1 - rp^-(γ-1)/γ", "color": "#16a34a"}]}
```

Regeneration, intercooling and reheat plus a Rankine bottoming cycle push
**combined-cycle** plants past 60% - the highest of any heat engine.

```python
import numpy as np
gamma = 1.4
T1, T3 = 300.0, 1500.0
rp = np.linspace(2, 40, 400)
eta = 1 - rp**(-(gamma-1)/gamma)
# net-work-optimal pressure ratio
rp_opt = (T3/T1)**(gamma/(2*(gamma-1)))
print(f"rp for max net work ~ {rp_opt:.1f}")
```

**Next:** run the cycles backwards - refrigeration and heat pumps.
""",
        ),
        _t(
            "Refrigeration and heat pump cycles",
            "12 min",
            r"""
# Refrigeration and heat pump cycles

Reverse a power cycle and it *moves* heat from cold to hot using work input - a
**vapour-compression refrigeration** cycle, the basis of every fridge, A/C and
heat pump.

```mermaid
flowchart LR
  E[Evaporator, QL in] --> Cmp[Compressor, Win]
  Cmp --> Cnd[Condenser, QH out]
  Cnd --> V[Expansion valve]
  V --> E
```

Four processes: isentropic compression, isobaric condensation (reject $Q_H$),
isenthalpic throttling, isobaric evaporation (absorb $Q_L$). Performance is the
**coefficient of performance**:

$$COP_{ref} = \frac{q_L}{w_{in}} = \frac{h_1 - h_4}{h_2 - h_1}, \qquad COP_{hp} = COP_{ref} + 1$$

COP exceeds 1 because you are *pumping* heat, not making it. The reversible
ceiling is $COP_{ref} = T_L/(T_H - T_L)$ - performance collapses as the
temperature lift grows:

```plot
{"title": "Carnot refrigeration COP vs temperature lift (TL=263 K)", "xLabel": "temperature lift TH - TL (K)", "yLabel": "COP_ref", "xRange": [5, 60], "yRange": [0, 12], "grid": true, "functions": [{"expr": "263/x", "label": "TL/(TH-TL)", "color": "#dc2626"}]}
```

Refrigerant choice (R-134a, R-1234yf, ammonia, CO2) trades off COP, pressures,
flammability and **GWP** (global warming potential) - a live regulatory issue.

```python
# Vapour-compression COP from cycle enthalpies (kJ/kg)
h1, h2 = 244.5, 280.0   # evaporator exit, compressor exit
h3 = 95.5               # condenser exit = h4 (throttle, isenthalpic)
qL, win = h1 - h3, h2 - h1
print(f"COP_ref = {qL/win:.2f}, COP_hp = {qL/win + 1:.2f}")
```

**Next:** measure the *quality* of energy, not just quantity - exergy.
""",
        ),
        _t(
            "Exergy analysis and the dead state",
            "13 min",
            r"""
# Exergy analysis and the dead state

The first law counts energy quantity; the second law counts its **quality**.
**Exergy** (availability) is the maximum *useful work* obtainable as a system
comes to equilibrium with a reference **dead state** $(T_0, p_0)$ - usually the
environment.

For a flow stream, **specific flow exergy** is

$$\psi = (h - h_0) - T_0(s - s_0) + \tfrac{1}{2}V^2 + gz$$

Every real process *destroys* exergy in proportion to entropy generation - the
**Gouy-Stodola** relation:

$$\dot X_{dest} = T_0\,\dot S_{gen} \ge 0$$

This is the engineer's most powerful diagnostic: an exergy balance pinpoints
*where* the losses are (the combustor in a gas turbine, the heat exchanger pinch,
the throttle), so you fix what matters. **Second-law (exergetic) efficiency**
$\varepsilon = \dot X_{out}/\dot X_{in}$ compares against the reversible ideal,
not just energy in/out.

```mermaid
flowchart LR
  XIN[Exergy in] --> DEV[Component]
  DEV --> XOUT[Exergy out, useful]
  DEV --> XD[Exergy destroyed = T0*Sgen]
```

Exergy destruction grows linearly with entropy generation:

```plot
{"title": "Exergy destroyed vs entropy generated (T0 = 298 K)", "xLabel": "entropy generation Sgen (kJ/kg.K)", "yLabel": "exergy destroyed (kJ/kg)", "xRange": [0, 1.2], "yRange": [0, 360], "grid": true, "functions": [{"expr": "298*x", "label": "Xdest = T0*Sgen", "color": "#dc2626"}]}
```

```python
# Throttle valve exergy destruction (isenthalpic, ideal gas)
T0, R = 298.0, 0.287          # K, kJ/kg.K
p1, p2 = 800.0, 150.0         # kPa
s_gen = -R * (0.0) + R * (1.0) * 0.0  # placeholder
s_gen = R * ( (1.0) ) * 0.0   # for ideal gas isothermal throttle:
import math
s_gen = R * math.log(p1/p2)   # ds = -R ln(p2/p1) at constant h (ideal gas)
print(f"Sgen = {s_gen:.3f} kJ/kg.K,  Xdest = {T0*s_gen:.1f} kJ/kg")
```

**Next:** let a computer search the cycle design space - optimization.
""",
        ),
        _t(
            "Computational cycle optimization",
            "14 min",
            r"""
# Computational cycle optimization

Modern thermodynamic design is computational: couple an accurate **property
library** (CoolProp / REFPROP) to a cycle model, then let an optimizer search
design variables (pressure ratios, reheat pressures, pinch points) against an
objective (efficiency, net power, cost, exergy destruction) subject to
constraints (turbine exit quality, material temperature limits).

```mermaid
flowchart LR
  X[design vars: rp, p_reheat...] --> M[Cycle model + CoolProp]
  M --> F[objective: -eta]
  F --> O[Optimizer SLSQP/GA]
  O -->|update X| X
  O --> S[optimal design]
```

A typical loop maximises efficiency over Brayton pressure ratio with
`scipy.optimize`:

```python
import numpy as np
from scipy.optimize import minimize_scalar

gamma, eta_c, eta_t = 1.4, 0.85, 0.88
T1, T3 = 300.0, 1500.0
cp = 1.005

def neg_eff(rp):
    T2s = T1 * rp**((gamma-1)/gamma)
    T2 = T1 + (T2s - T1)/eta_c            # real compressor
    T4s = T3 * rp**(-(gamma-1)/gamma)
    T4 = T3 - eta_t*(T3 - T4s)            # real turbine
    w_net = cp*(T3 - T4) - cp*(T2 - T1)
    q_in = cp*(T3 - T2)
    return -w_net/q_in if q_in > 0 else 0.0

res = minimize_scalar(neg_eff, bounds=(2, 50), method="bounded")
print(f"optimal rp = {res.x:.1f}, eta = {-res.fun:.3f}")
```

Convergence of such a gradient search is fast and monotone in well-posed cycles:

```plot
{"title": "Optimizer convergence: objective vs iteration", "xLabel": "iteration", "yLabel": "objective gap", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "e^(-0.4 k)", "color": "#16a34a"}]}
```

Beyond gradients: **genetic algorithms** and **Bayesian optimization** handle
non-convex, multi-objective trade-offs (efficiency vs capital cost), and
**surrogate / ML models** replace slow property calls inside the loop. This is
the state of the art in power-plant and ORC (organic Rankine cycle) design.

**Next:** the final check across gas cycles, refrigeration, exergy and
optimization.
""",
        ),
        _quiz(),
    ),
)


ENGINEERING_THERMODYNAMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ENGINEERING_THERMODYNAMICS_COURSES"]
