"""Hydraulics & Pneumatics track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on fluid power. Starts from Pascal's
law, fluid-power components and pneumatics fundamentals, builds through pumps,
control valves, cylinders/actuators, circuit design and losses, and ends with
proportional/servo control, electrohydraulic system modelling, and
simulation/optimisation. Lessons are `text` with LaTeX, interactive ```plot
blocks (pressure, flow, cylinder force, frequency response), ```mermaid
classification/circuit/workflow diagrams and runnable ```python/```matlab code.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Hydraulics & Pneumatics — Basics ─────────────────────────────────────────

_BASICS = SeedCourse(
    slug="hydraulics-pneumatics-basics",
    title="Hydraulics & Pneumatics — Basics",
    description=(
        "Build physical intuition for fluid power: Pascal's law and pressure "
        "intensification, what flow and pressure each do, the main hydraulic and "
        "pneumatic components, the difference between hydraulics and pneumatics, "
        "and how to read a basic ISO circuit. Interactive plots and diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is fluid power? Pascal's law",
            "10 min",
            r"""
# What is fluid power? Pascal's law

**Fluid power** transmits energy through a confined, pressurised fluid — oil in
**hydraulics**, compressed air in **pneumatics**. It sits between mechanical and
electrical drives, prized for very high force/torque density and smooth
controllable motion.

The foundation is **Pascal's law**: pressure applied to a confined fluid acts
equally in all directions and transmits undiminished. Since pressure is force per
area, $p = F/A$, a small input force on a small piston balances a large output
force on a large piston:

$$\frac{F_1}{A_1} = p = \frac{F_2}{A_2}\;\Rightarrow\; F_2 = F_1\,\frac{A_2}{A_1}.$$

This is the **hydraulic press / jack** — a force multiplier. The cost is stroke:
the volume pushed in equals the volume pushed out, so $A_1 d_1 = A_2 d_2$ and the
large piston moves less. Work is conserved (ideally).

```plot
{"title": "Output force vs cylinder bore area (p = 10 MPa)", "xLabel": "piston area A (cm^2)", "yLabel": "force F (kN)", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x", "label": "F = p A (10 MPa * A)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  FP["Fluid power"] --> H["Hydraulics: oil, high pressure"]
  FP --> PN["Pneumatics: air, compressible"]
  H --> FD["High force density, stiff"]
  PN --> CL["Clean, fast, springy"]
```

**Next:** the two quantities that run every circuit — pressure and flow.
""",
        ),
        _t(
            "Pressure and flow: the two currencies",
            "12 min",
            r"""
# Pressure and flow: the two currencies

A fluid-power system is governed by two variables. **Pressure** $p$ sets the
**force** an actuator can deliver; **flow rate** $Q$ sets its **speed**. A useful
analogy: pressure is like voltage, flow is like current.

- Cylinder force: $F = p\,A$ (bore area $A$).
- Cylinder speed: $v = Q/A$.
- Motor torque: $T = \dfrac{p\,D}{2\pi}$, speed $n = \dfrac{Q}{D}$ ($D$ = displacement).

A key truth often missed by beginners: **pumps create flow, not pressure**.
Pressure only rises when flow meets a resistance (a load or a restriction). The
**hydraulic power** delivered is the product of the two:

$$P = p\,Q.$$

In consistent SI ($p$ in Pa, $Q$ in m$^3$/s) this is watts; a handy field form is
$P\,[\text{kW}] = p\,[\text{bar}]\times Q\,[\text{L/min}]/600$.

```plot
{"title": "Cylinder speed vs supplied flow (bore area 20 cm^2)", "xLabel": "flow Q (L/min)", "yLabel": "rod speed v (m/s)", "xRange": [0, 60], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "x/120", "label": "v = Q / A", "color": "#2563eb"}]}
```

```python
p_bar = 150.0          # bar
Q_lpm = 40.0           # L/min
P_kW = p_bar * Q_lpm / 600.0   # field formula for hydraulic power
A = 20e-4              # m^2 (20 cm^2 bore)
F = (p_bar*1e5) * A    # N
v = (Q_lpm/6e4) / A    # m/s
print(f"P = {P_kW:.1f} kW, F = {F/1000:.1f} kN, v = {v:.3f} m/s")
```

**Next:** the building blocks that make up any fluid-power system.
""",
        ),
        _t(
            "Components of a hydraulic system",
            "12 min",
            r"""
# Components of a hydraulic system

Every hydraulic system is the same handful of building blocks arranged around an
**energy chain**: an electric motor drives a **pump** that converts mechanical
power to fluid power; **valves** direct and regulate the flow; an **actuator**
(cylinder or motor) converts it back to mechanical work; the fluid returns to a
**reservoir** through a **filter** and **cooler**.

- **Power unit**: prime mover + pump + reservoir + filter.
- **Control**: directional, pressure and flow valves.
- **Actuator**: linear cylinder or rotary motor.
- **Conditioning**: filters, coolers, accumulators.
- **Safety**: the **relief valve** caps system pressure (a must — fluid is nearly
  incompressible, so a dead-headed pump would otherwise spike to failure).

The reservoir does more than store oil: it de-aerates, settles contaminants and
dissipates heat. Cleanliness (ISO 4406 code) is the single biggest driver of
component life.

```mermaid
flowchart LR
  M["Electric motor"] --> P["Pump"]
  T["Reservoir + filter"] --> P
  P --> RV["Relief valve (safety)"]
  P --> DV["Directional valve"]
  DV --> A["Cylinder / motor"]
  A --> T
```

```plot
{"title": "System pressure capped by the relief valve", "xLabel": "load demand (relative)", "yLabel": "system pressure (bar)", "xRange": [0, 10], "yRange": [0, 250], "grid": true, "functions": [{"expr": "25*x", "label": "rising with load", "color": "#2563eb"}, {"expr": "200", "label": "relief setting", "color": "#dc2626"}]}
```

**Next:** compressed air — how pneumatics differs from hydraulics.
""",
        ),
        _t(
            "Pneumatics fundamentals: compressed air",
            "11 min",
            r"""
# Pneumatics fundamentals: compressed air

**Pneumatics** uses **compressed air** as the working fluid. Air is cheap, clean,
safe around fire, and exhausts freely to atmosphere — ideal for fast, repetitive,
moderate-force tasks (assembly, packaging, clamping). Typical working pressure is
only **6-8 bar**, far below hydraulics.

The defining difference is **compressibility**. Air obeys the ideal-gas law,

$$pV = mRT,$$

so an air actuator behaves like a stiff spring: it stores energy, gives a
**springy** (compliant) response and cannot hold an exact mid-stroke position
without feedback. This compliance is a feature for cushioning and a drawback for
precise positioning.

A pneumatic system needs **air preparation** — the **FRL** unit: **F**ilter
(remove water/dirt), **R**egulator (set pressure), **L**ubricator (oil mist for
moving seals). Moisture management (drying) is critical to avoid corrosion and
freezing at exhaust ports.

```plot
{"title": "Isothermal compression: pressure vs volume (Boyle)", "xLabel": "volume V (L)", "yLabel": "absolute pressure p (bar)", "xRange": [1, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "10/x", "label": "p V = const (Boyle)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  C["Compressor"] --> R["Receiver tank"]
  R --> DR["Dryer"]
  DR --> FRL["FRL: filter-regulator-lubricator"]
  FRL --> V["Valves"]
  V --> A["Air cylinder"]
  A --> EX["Exhaust to atmosphere"]
```

**Next:** how the ISO symbols turn into a readable circuit diagram.
""",
        ),
        _t(
            "Reading ISO 1219 circuit diagrams",
            "11 min",
            r"""
# Reading ISO 1219 circuit diagrams

Fluid-power schematics use the **ISO 1219** symbol standard — function-based, not
pictorial. Learning a few conventions lets you read any circuit.

- **Lines**: solid = working (pressure) line; dashed = pilot/control line; the
  reservoir is drawn as an open rectangle.
- **Pumps/motors**: a circle with a triangle pointing **out** (pump) or **in**
  (motor); a solid arrow through the circle means variable displacement.
- **Valves**: rectangular boxes, one **box per position**; ports labelled
  P (pressure), T (tank), A/B (actuators). A 4/3 valve has 4 ports and 3 boxes.
- **Actuators**: a rectangle with a rod; double lines on the rod end indicate a
  double-acting cylinder.

A valve is named by **ports / positions**: a **4/2** has 4 ports, 2 positions; a
**4/3** adds a centre position (often closed, tandem or float centre).

```mermaid
flowchart TB
  P["Pump (circle + outward triangle)"] --> RV["Relief valve to tank"]
  P --> DCV["4/3 directional valve (P, T, A, B)"]
  DCV -->|A| CAP["Cylinder cap side"]
  DCV -->|B| ROD["Cylinder rod side"]
  CAP --- ROD
  DCV --> T["Tank"]
```

```plot
{"title": "Valve naming: ports and positions seen in this course", "xLabel": "positions", "yLabel": "ports", "xRange": [1, 4], "yRange": [2, 5], "grid": true, "functions": [{"expr": "x", "label": "more positions -> more functions", "color": "#16a34a"}]}
```

Reading top-to-bottom (source -> control -> actuator -> return) makes even a busy
schematic tractable.

**Next:** prove your fluid-power basics.
""",
        ),
        _quiz(),
    ),
)


# ── Hydraulics & Pneumatics — Intermediate ───────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="hydraulics-pneumatics-intermediate",
    title="Hydraulics & Pneumatics — Intermediate",
    description=(
        "The quantitative core of fluid power: pump types and sizing, directional "
        "and pressure control valves, the valve orifice equation, cylinder force "
        "and speed analysis, meter-in/meter-out circuit design, and the head/heat "
        "losses that set efficiency. Worked equations, plots and code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pumps: types, displacement and sizing",
            "13 min",
            r"""
# Pumps: types, displacement and sizing

A **positive-displacement** pump traps a fixed volume per revolution and is the
heart of every hydraulic power unit (centrifugal pumps cannot build the needed
pressure). The key parameter is **displacement** $D$ (cm$^3$/rev). Ideal flow is

$$Q = D\,n\,\eta_v,$$

with speed $n$ (rev/s) and **volumetric efficiency** $\eta_v$ (leakage past
clearances rises with pressure). Required **input torque** and power are

$$T = \frac{D\,\Delta p}{2\pi\,\eta_m},\qquad P_{in} = \frac{p\,Q}{\eta_t},\quad \eta_t=\eta_v\eta_m.$$

The three families trade cost, pressure and noise:

- **Gear** — cheap, robust, ~250 bar, fixed displacement.
- **Vane** — quiet, mid pressure, can be variable.
- **Piston** (axial/radial) — highest pressure (up to ~400 bar), best efficiency,
  swash-plate **variable displacement** for flow control.

```plot
{"title": "Pump flow vs speed at three displacements", "xLabel": "shaft speed n (rev/s)", "yLabel": "flow Q (L/min)", "xRange": [0, 30], "yRange": [0, 90], "grid": true, "functions": [{"expr": "0.06*x*0.95*10", "label": "small D", "color": "#16a34a"}, {"expr": "0.06*x*0.95*30", "label": "medium D", "color": "#2563eb"}, {"expr": "0.06*x*0.95*60", "label": "large D", "color": "#dc2626"}]}
```

```python
D = 32e-6          # m^3/rev (32 cc/rev)
n = 1450/60.0      # rev/s
eta_v, eta_m = 0.95, 0.92
dp = 200e5         # Pa (200 bar)
Q = D*n*eta_v                 # m^3/s
T = D*dp/(2*3.14159*eta_m)    # N.m
print(f"Q = {Q*6e4:.1f} L/min, input torque = {T:.1f} N.m")
```

**Next:** the valves that direct and switch the flow.
""",
        ),
        _t(
            "Directional control valves",
            "12 min",
            r"""
# Directional control valves

**Directional control valves (DCVs)** route flow to start, stop and reverse an
actuator. They are classified by **ports/positions** (4/3, 4/2, 3/2...) and by
**actuation** (manual, solenoid, pilot, spring-return).

The **spool** is the moving element; lands and grooves connect ports as it
shifts. The crucial design choice in a 4/3 valve is the **centre condition**:

- **Closed (blocked) centre** — holds the load, but the pump dead-heads over
  relief (wasteful, hot).
- **Tandem centre** — P connects to T, **unloading** the pump (low loss) while
  holding the actuator.
- **Open centre** — all ports joined; actuator floats, pump unloaded.
- **Float centre** — A and B to tank; load can drift.

Real spools have small **overlap** (deadband, leak-free hold) or **underlap**
(faster, slight leakage) — a key idea revisited in servo valves.

```mermaid
flowchart LR
  IN["4/3 DCV centre choice"] --> CC["Closed: hold, pump over relief"]
  IN --> TC["Tandem: hold + unload pump"]
  IN --> OC["Open: float + unload"]
  IN --> FC["Float: A,B to tank"]
```

```plot
{"title": "Spool overlap and the resulting flow deadband", "xLabel": "spool position x (mm)", "yLabel": "metered flow (relative)", "xRange": [-3, 3], "yRange": [0, 3], "grid": true, "functions": [{"expr": "abs(x)", "label": "underlap: flow near centre", "color": "#16a34a"}, {"expr": "abs(x)-1", "label": "overlap: deadband", "color": "#dc2626"}]}
```

**Next:** valves that regulate pressure, and the orifice flow law.
""",
        ),
        _t(
            "Pressure control and the orifice equation",
            "13 min",
            r"""
# Pressure control and the orifice equation

**Pressure-control valves** set or limit pressure. The **relief valve** is the
safety limit (opens at a cracking pressure to dump excess flow to tank); a
**pressure-reducing valve** holds a lower secondary pressure for a sub-circuit; a
**sequence valve** triggers a second action once a pressure threshold is reached.

The physics behind every restriction is the **orifice (Bernoulli) equation** —
flow through an opening of area $A_o$ across pressure drop $\Delta p$:

$$Q = C_d\,A_o\sqrt{\frac{2\,\Delta p}{\rho}}.$$

$C_d\approx 0.6$-$0.7$ is the discharge coefficient. The square-root law is
central: flow scales with $\sqrt{\Delta p}$, so doubling flow needs **four times**
the pressure drop. This is also why a fixed orifice makes a load-sensitive (not
load-independent) flow control.

```plot
{"title": "Orifice flow vs pressure drop (square-root law)", "xLabel": "pressure drop dp (bar)", "yLabel": "flow Q (L/min)", "xRange": [0, 100], "yRange": [0, 60], "grid": true, "functions": [{"expr": "6*sqrt(x)", "label": "Q ~ sqrt(dp)", "color": "#2563eb"}]}
```

```python
import math
Cd = 0.65
d = 2e-3                       # orifice diameter, m
A = math.pi*d**2/4
rho = 870.0                    # hydraulic oil, kg/m^3
dp = 50e5                      # Pa (50 bar)
Q = Cd*A*math.sqrt(2*dp/rho)   # m^3/s
print(f"Q = {Q*6e4:.2f} L/min through a {d*1000:.0f} mm orifice")
```

**Next:** sizing the actuator — cylinder force and speed.
""",
        ),
        _t(
            "Cylinders: force, speed and the differential effect",
            "12 min",
            r"""
# Cylinders: force, speed and the differential effect

A **double-acting cylinder** has unequal areas because the rod occupies part of
the rod-side annulus. Let bore area be $A_p=\pi D^2/4$ and rod-side area
$A_a = A_p - \pi d^2/4$. Then:

- **Extend force**: $F_{ext} = p\,A_p$ (full bore pushed).
- **Retract force**: $F_{ret} = p\,A_a$ (smaller area, less force).
- **Extend speed**: $v_{ext} = Q/A_p$; **retract speed**: $v_{ret} = Q/A_a$
  (faster, because less volume to fill).

This area asymmetry is the **differential** effect. In a **regenerative** circuit
the rod-side oil is fed back to the cap side, so the effective area is just the
**rod cross-section** $\pi d^2/4$ — giving fast extension at reduced force, useful
for rapid approach before a work stroke.

Long cylinders must also be checked for **buckling** (Euler) and the rod sized
accordingly.

```plot
{"title": "Extend vs retract force (100 mm bore, 56 mm rod)", "xLabel": "pressure p (bar)", "yLabel": "force F (kN)", "xRange": [0, 200], "yRange": [0, 160], "grid": true, "functions": [{"expr": "0.785*x", "label": "extend F = p*A_bore", "color": "#2563eb"}, {"expr": "0.539*x", "label": "retract F = p*A_annulus", "color": "#dc2626"}]}
```

```python
import math
D, d = 0.100, 0.056           # bore, rod (m)
Ap = math.pi*D**2/4
Aa = Ap - math.pi*d**2/4
p, Q = 160e5, 40/6e4          # 160 bar, 40 L/min in m^3/s
print(f"F_ext={p*Ap/1e3:.1f} kN, F_ret={p*Aa/1e3:.1f} kN")
print(f"v_ext={Q/Ap:.3f} m/s, v_ret={Q/Aa:.3f} m/s")
```

**Next:** combining components into speed-controlled circuits.
""",
        ),
        _t(
            "Circuit design: meter-in, meter-out and losses",
            "13 min",
            r"""
# Circuit design: meter-in, meter-out and losses

Controlling actuator speed means controlling flow with a restrictor. There are
three classic schemes:

- **Meter-in**: throttle on the **inlet**. Precise for resisting (opposing)
  loads, but cannot control an **overrunning** (aiding) load — the load can run
  away.
- **Meter-out**: throttle on the **outlet**. Controls overrunning loads by
  creating back-pressure; the standard for vertical and aiding loads. Watch the
  **pressure intensification** on the rod side from the area ratio.
- **Bleed-off**: a restrictor diverts surplus flow to tank in parallel — most
  efficient but least precise.

Efficiency is set by where the pressure drop is **wasted**. A simple throttle
turns $\Delta p\cdot Q$ straight into heat. **Load-sensing** and variable pumps
match supply to demand and cut this loss dramatically.

```mermaid
flowchart LR
  P["Pump"] --> DCV["Directional valve"]
  DCV --> MI["Meter-in throttle"]
  MI --> CYL["Cylinder"]
  CYL --> MO["Meter-out throttle"]
  MO --> T["Tank"]
  DCV --> BO["Bleed-off to tank (parallel)"]
```

```plot
{"title": "Throttling loss converted to heat power", "xLabel": "flow Q (L/min)", "yLabel": "heat power (kW)", "xRange": [0, 40], "yRange": [0, 8], "grid": true, "functions": [{"expr": "x*120/600", "label": "P_heat = dp*Q (dp=120 bar)", "color": "#dc2626"}]}
```

```python
dp_throttle = 120.0    # bar wasted across the restrictor
Q = 30.0               # L/min
P_heat = dp_throttle*Q/600.0   # kW dumped as heat
print(f"Throttling loss = {P_heat:.1f} kW -> sized cooler/reservoir")
```

**Next:** test the quantitative core.
""",
        ),
        _quiz(),
    ),
)


# ── Hydraulics & Pneumatics — Advanced ───────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="hydraulics-pneumatics-advanced",
    title="Hydraulics & Pneumatics — Advanced",
    description=(
        "Applied and state-of-the-art fluid power: proportional and servo valves, "
        "dynamic modelling of the valve-cylinder-load system, closed-loop position "
        "and force control, energy-efficient architectures (load sensing, digital "
        "hydraulics), accumulators and transient analysis, and simulation, "
        "model-based design and ML/optimisation. Plots, code and workflows."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Proportional and servo valves",
            "14 min",
            r"""
# Proportional and servo valves

Beyond on/off switching, **proportional** and **servo valves** meter flow in
proportion to an electrical command, enabling continuous control. A
**proportional valve** uses a **proportional solenoid** whose force is roughly
linear in current; a **servo valve** uses a torque-motor + flapper-nozzle (or jet
pipe) **pilot stage** to position the spool with very high bandwidth and tiny
deadband.

Key performance metrics:

- **Hysteresis / deadband** — proportional valves overlap (1-5 %); servo valves
  are nearly zero-lap, so leak more but track precisely.
- **Rated flow** at a reference drop (usually 35 bar/notch) with the orifice law
  $Q = Q_R\sqrt{\Delta p/\Delta p_R}$.
- **Frequency response** — bandwidth (-3 dB / -90°), often 50-250 Hz.

The valve's own dynamics are commonly modelled as a 2nd-order system relating
spool position to command:

$$\frac{x_v(s)}{u(s)} = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}.$$

```plot
{"title": "Servo valve frequency response magnitude (2nd order)", "xLabel": "frequency ratio w/wn", "yLabel": "gain |x_v/u|", "xRange": [0, 3], "yRange": [0, 3], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2+(0.2*x)^2)", "label": "zeta = 0.1", "color": "#dc2626"}, {"expr": "1/sqrt((1-x^2)^2+(0.8*x)^2)", "label": "zeta = 0.4", "color": "#2563eb"}]}
```

```python
import numpy as np
wn, zeta = 2*np.pi*120, 0.4     # 120 Hz natural freq
w = np.array([10, 50, 120, 250])*2*np.pi
mag = wn**2/np.sqrt((wn**2-w**2)**2 + (2*zeta*wn*w)**2)
print("gain:", np.round(mag, 3))   # rolls off past ~120 Hz
```

**Next:** the dynamics of the valve-cylinder-load system.
""",
        ),
        _t(
            "Dynamic modelling of the valve-cylinder-load system",
            "15 min",
            r"""
# Dynamic modelling of the valve-cylinder-load system

To design control we need a model. Three coupled relations describe an
electrohydraulic axis:

1. **Valve flow** (linearised about an operating point):
   $Q_L = K_q\,x_v - K_c\,p_L$, with flow gain $K_q$ and flow-pressure
   coefficient $K_c$.
2. **Cylinder continuity** with oil **compressibility** (bulk modulus $\beta$):
   $Q_L = A\,\dot{x} + \dfrac{V_t}{4\beta}\,\dot{p}_L + C_{tp}\,p_L$.
3. **Load dynamics**: $A\,p_L = m\ddot{x} + b\dot{x} + F_{load}$.

Combining them yields the dominant **hydraulic natural frequency**

$$\omega_h = \sqrt{\frac{4\beta A^2}{V_t\,m}},$$

the single most important dynamic limit of a hydraulic servo — it caps achievable
bandwidth and is set by the **stiffness of the trapped oil column**. Compliant
hoses or entrained air lower $\beta$ and wreck performance.

```plot
{"title": "Hydraulic resonance: response of the oil-column 2nd order", "xLabel": "time t (s)", "yLabel": "position (normalised)", "xRange": [0, 12], "yRange": [-1, 1], "grid": true, "functions": [{"expr": "exp(-0.2*x)*cos(3*x)", "label": "lightly damped wh", "color": "#dc2626"}]}
```

```python
import numpy as np
beta = 1.4e9       # Pa, oil bulk modulus
A = 1.96e-3        # m^2 piston area (50 mm bore)
Vt = 1.0e-3        # m^3 trapped volume
m = 500.0          # kg load
wh = np.sqrt(4*beta*A**2/(Vt*m))
print(f"omega_h = {wh:.0f} rad/s = {wh/2/np.pi:.1f} Hz")
```

**Next:** close the loop for position and force control.
""",
        ),
        _t(
            "Closed-loop position and force control",
            "14 min",
            r"""
# Closed-loop position and force control

With a model in hand, we add feedback. The classic **electrohydraulic position
servo** measures cylinder position (LVDT/encoder), compares to a reference and
drives the valve. The open-loop plant is roughly a velocity integrator behind the
valve-oil 2nd order, so a simple **proportional** gain already stabilises it; the
loop gain $K_v$ trades bandwidth against the resonance $\omega_h$.

Practical control adds:

- **Velocity / acceleration feedforward** to cut following error.
- **Lead or notch filtering** to tame $\omega_h$.
- **Force / pressure control** for contact tasks, often **impedance** or hybrid
  position/force control.
- **Friction and deadband compensation** for stick-slip near zero velocity.

A step response shows the bandwidth-damping trade-off as $K_v$ rises:

```plot
{"title": "Position step response vs loop gain", "xLabel": "time t (s)", "yLabel": "position (normalised)", "xRange": [0, 10], "yRange": [0, 1.5], "grid": true, "functions": [{"expr": "1-exp(-0.6*x)", "label": "low Kv: slow, well damped", "color": "#2563eb"}, {"expr": "1-exp(-0.3*x)*cos(1.5*x)", "label": "high Kv: fast, oscillatory", "color": "#dc2626"}]}
```

```python
import numpy as np
from scipy import signal
# Plant: valve-oil 2nd order * integrator (velocity -> position)
wh, zeta = 60.0, 0.15
plant = signal.TransferFunction([wh**2], [1, 2*zeta*wh, wh**2, 0])
for Kv in (20, 60):
    ol = signal.TransferFunction(np.polymul([Kv], plant.num), plant.den)
    cl = signal.feedback(ol) if hasattr(signal, "feedback") else ol
    print(f"Kv={Kv}: dc poles ~", np.round(np.real(cl.poles[:2]), 2))
```

**Next:** architectures that save energy.
""",
        ),
        _t(
            "Energy-efficient hydraulics: load sensing and digital",
            "14 min",
            r"""
# Energy-efficient hydraulics: load sensing and digital

Conventional valve-controlled systems waste energy throttling a fixed supply.
Modern architectures attack this loss:

- **Load sensing (LS)**: a variable pump senses the highest load pressure and
  delivers only $p_{load}+\Delta p_{margin}$ (typically 15-25 bar). Pump output
  tracks demand, so standby and partial-load losses plummet.
- **Pressure/flow-compensated** pumps hold a set pressure or flow on the margin.
- **Displacement control**: drive an actuator directly from a variable pump
  (valveless), eliminating metering loss — used in efficient excavators.
- **Digital hydraulics**: banks of fast on/off valves switched in
  **PWM/PCM** patterns approximate proportional control with near-binary
  efficiency.

The efficiency gain is largest at partial load, where throttling is worst:

```plot
{"title": "Pump output power: fixed vs load-sensing", "xLabel": "load demand (fraction)", "yLabel": "input power (kW)", "xRange": [0, 1], "yRange": [0, 25], "grid": true, "functions": [{"expr": "20", "label": "fixed-displacement (always full)", "color": "#dc2626"}, {"expr": "3+18*x", "label": "load-sensing (tracks demand)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  L["Highest load pressure"] --> LS["LS signal line"]
  LS --> PC["Pump compensator"]
  PC --> VP["Variable pump: delta-p margin only"]
  VP --> A["Actuators"]
```

```python
margin = 20.0          # bar LS margin
loads = [40, 80, 150]  # bar actual loads
Q = 30.0               # L/min
for pl in loads:
    P_ls = (pl+margin)*Q/600.0
    P_fix = 250.0*Q/600.0          # fixed pump at full system pressure
    print(f"load {pl} bar: LS={P_ls:.1f} kW vs fixed={P_fix:.1f} kW")
```

**Next:** accumulators and transient (water-hammer) analysis.
""",
        ),
        _t(
            "Accumulators and transient analysis",
            "13 min",
            r"""
# Accumulators and transient analysis

An **accumulator** stores energy in a compressed-gas precharge behind a
bladder/piston. It supplies peak flow, absorbs shocks, dampens pulsation and
holds pressure during pump-off. Gas-side behaviour follows a polytropic law:

$$p_1 V_1^n = p_2 V_2^n,$$

with $n\approx 1$ (isothermal, slow) to $1.4$ (adiabatic, fast). Sizing for a
duty cycle uses the swept gas volume between $p_1$ (precharge ~90 % of min
working) and $p_2$ (max working).

**Transients** matter because oil is nearly incompressible. Sudden valve closure
sends a **pressure wave** — the **Joukowsky** surge:

$$\Delta p = \rho\,a\,\Delta v,$$

where $a=\sqrt{\beta/\rho}$ is the wave speed (~1200-1400 m/s in oil). The wave
returns in $2L/a$; closing faster than this gives the full surge — a major cause
of burst lines and noise, mitigated by accumulators, slow-shift valves and
softer hoses.

```plot
{"title": "Joukowsky surge vs velocity change", "xLabel": "velocity change dv (m/s)", "yLabel": "pressure surge (bar)", "xRange": [0, 5], "yRange": [0, 80], "grid": true, "functions": [{"expr": "0.87*1300*x/100", "label": "dp = rho a dv", "color": "#dc2626"}]}
```

```python
rho, beta = 870.0, 1.4e9
a = (beta/rho)**0.5            # wave speed, m/s
dv = 3.0                       # m/s flow stopped
dp = rho*a*dv                  # Pa surge
L = 5.0
print(f"a={a:.0f} m/s, surge={dp/1e5:.0f} bar, return time={2*L/a*1000:.1f} ms")
```

**Next:** simulate and optimise the whole system.
""",
        ),
        _t(
            "Simulation, model-based design and optimisation",
            "15 min",
            r"""
# Simulation, model-based design and optimisation

Modern fluid-power engineering is **model-based**. System simulators
(**Simscape Fluids**, **Simcenter Amesim**, **DSHplus**, Modelica/**HydraulicLib**)
assemble validated component models — pumps, valves, lines, accumulators — and
solve the coupled stiff ODE/DAE for pressures and flows, capturing
compressibility, cavitation and thermal effects before any metal is cut.

Beyond simulating a fixed design we **optimise** it. Component sizes, valve gains
and controller parameters $\boldsymbol{\theta}$ minimise an objective (energy use,
cycle time, overshoot) under constraints. Gradient-free methods (**genetic
algorithms**, **Bayesian optimisation**) suit black-box simulators; surrogate
models and **reinforcement-learning** controllers are emerging for nonlinear,
valve-controlled axes. Convergence of a tuning loop:

```plot
{"title": "Controller-tuning convergence (objective vs iteration)", "xLabel": "optimisation iteration", "yLabel": "cost J (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "J ~ exp(-0.4 k)", "color": "#16a34a"}]}
```

```python
import numpy as np
# Simulate a 1st-order pressure build-up then tune a gain by descent
def cost(K):
    t = np.linspace(0, 1, 200)
    y = 1 - np.exp(-K*t)           # closed-loop step
    e = np.trapz((1 - y)**2, t)    # ISE following error
    return e + 1e-4*K**2           # + effort penalty

K, lr = 2.0, 50.0
for k in range(8):
    g = (cost(K+1e-3) - cost(K-1e-3))/2e-3   # numeric gradient
    K -= lr*g
    print(f"iter {k}: K={K:.2f}, J={cost(K):.4f}")
```

```mermaid
flowchart LR
  M["Component models"] --> S["System simulation (DAE solver)"]
  S --> O["Objective: energy / time / overshoot"]
  O --> U["Optimiser: GA / BO / RL"]
  U --> M
```

**Next:** finish the track — test your mastery.
""",
        ),
        _quiz(),
    ),
)


HYDRAULICS_PNEUMATICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["HYDRAULICS_PNEUMATICS_COURSES"]
