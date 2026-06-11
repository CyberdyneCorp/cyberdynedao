"""Curated Battery Management & Energy Storage track: Basics, Intermediate,
Advanced.

A complete battery curriculum: electrochemical fundamentals and cell behaviour
(chemistries, OCV/SoC, C-rate, internal resistance, equivalent-circuit models,
safety and degradation), the battery management system and state estimation
(BMS architecture, SoC by coulomb counting / OCV / Kalman, SoH and aging, cell
balancing, pack design), and advanced systems (model-based EKF observers,
electro-thermal modeling, fast charging, grid and stationary storage, second
life and alternatives, with a cross-domain applications throughline). Dual
MATLAB + Python focus throughout, with runnable Python labs (numpy +
matplotlib), interactive ```plot blocks, Mermaid diagrams, LaTeX formulas, and
real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Battery Management & Energy Storage -- Basics -----------------------------

_BATTERY_BASICS = SeedCourse(
    slug="battery-basics",
    title="Battery Management & Energy Storage -- Basics",
    description=(
        "Batteries from the ground up: electrochemical fundamentals (cells, "
        "anode/cathode/electrolyte, redox, voltage and capacity), the major "
        "chemistries and their tradeoffs, cell characteristics (OCV vs SoC, "
        "C-rate, internal resistance, the discharge curve), the "
        "equivalent-circuit model (Rint and RC), and safety and degradation - "
        "with side-by-side MATLAB and Python, interactive plots, and a runnable "
        "discharge-curve lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Electrochemical fundamentals",
            "11 min",
            """\
# Electrochemical fundamentals

A battery stores energy in **chemical bonds** and releases it as **electric
current** through a controlled chemical reaction. Every cell has three parts:

| Part | Role | Example (Li-ion) |
|------|------|------------------|
| **Anode** (negative) | gives up electrons (oxidation) on discharge | graphite |
| **Cathode** (positive) | accepts electrons (reduction) on discharge | lithium metal oxide |
| **Electrolyte** | carries **ions** internally, blocks electrons | lithium salt in solvent |

The reaction is **redox** (reduction-oxidation): electrons leave the anode,
travel through your **external circuit** (doing useful work), and arrive at the
cathode, while ions shuffle through the electrolyte to keep charge balanced.

```mermaid
flowchart LR
  ANODE["anode (-) oxidation"] -->|electrons through load| LOAD["external load"]
  LOAD --> CATHODE["cathode (+) reduction"]
  ANODE -->|ions through electrolyte| CATHODE
```

## Voltage: the push per charge

The **cell voltage** comes from the difference in chemical potential between the
two electrodes. The thermodynamic ceiling is the **Nernst equation**, but the
takeaway is simple: each chemistry has a characteristic voltage. A single Li-ion
cell sits near $3.7\\,$V nominal; lead-acid near $2.0\\,$V; NiMH near $1.2\\,$V.

## Capacity: how much charge

**Capacity** $Q$ is the total charge a cell can deliver, measured in
**amp-hours** (Ah). Energy is capacity times voltage:

$$E = Q \\, V_{nom}, \\qquad [\\text{Wh}] = [\\text{Ah}] \\times [\\text{V}].$$

A $3.2\\,$Ah cell at $3.7\\,$V stores about $11.8\\,$Wh - run it at $1\\,$A and it
lasts roughly $3.2$ hours (ideally). Energy scales linearly with capacity:

```plot
{"title": "Stored energy vs cell capacity (slide nominal voltage)", "xLabel": "capacity Q (Ah)", "yLabel": "energy (Wh)", "xRange": [0, 5], "yRange": [0, 20], "grid": true, "controls": [{"name": "Vnom", "range": [1.2, 3.7], "value": 3.7, "label": "nominal voltage (V)"}], "functions": [{"expr": "Vnom*x", "label": "E = Q * Vnom"}]}
```

## Where you meet it

- A **smartphone** cell: ~$3.7\\,$V, $3$-$5\\,$Ah, ~$15\\,$Wh.
- An **EV** pack: hundreds of cells in series and parallel, ~$400\\,$V,
  $60$-$100\\,$kWh.
- A **grid** battery: thousands of modules, megawatt-hours.

```matlab
Q = 3.2; Vnom = 3.7;          % amp-hours, volts
E = Q * Vnom;                 % 11.84 Wh
runtime = Q / 1.0;            % hours at 1 A (ideal) -> 3.2 h
```

```python
Q, Vnom = 3.2, 3.7            # amp-hours, volts
E = Q * Vnom                  # 11.84 Wh
runtime = Q / 1.0             # hours at 1 A (ideal) -> 3.2 h
```

> **Practical insight:** Ah is charge, Wh is energy. Two cells with the same Ah
> but different voltages store different energy - always compare in Wh.

**Next:** the chemistries that turn this into real products.
""",
        ),
        _t(
            "Battery chemistries & tradeoffs",
            "12 min",
            """\
# Battery chemistries & tradeoffs

The electrode and electrolyte materials are the **chemistry**, and they decide
everything: voltage, energy density, cost, safety, and lifetime. There is no
"best" battery - only the right tradeoff for the job.

| Chemistry | Cell V | Energy density | Strengths | Weaknesses | Typical use |
|-----------|--------|----------------|-----------|------------|-------------|
| **Lead-acid** | 2.0 | low | cheap, robust, high surge current | heavy, short cycle life | car starter, UPS |
| **NiMH** | 1.2 | medium | safe, tolerant of abuse | self-discharge, memory-ish | hybrids, AA cells |
| **Li-ion (NMC/LCO)** | 3.7 | high | best energy density, light | costlier, thermal-runaway risk | phones, laptops, EVs |
| **LiFePO4 (LFP)** | 3.2 | medium-high | very safe, long cycle life, cheap | lower energy density | stationary storage, EVs, tools |

## Reading an energy-vs-power map (the Ragone idea)

Designers plot **energy density** (how much you can store, Wh/kg) against
**power density** (how fast you can deliver it, W/kg). Chemistries occupy
different corners - and a **supercapacitor** sits at the extreme high-power, low-
energy end. Slide the discharge time to see the energy-power tradeoff a single
device faces:

```plot
{"title": "Energy vs power tradeoff (a Ragone-style curve, slide stored energy)", "xLabel": "specific power (W/kg)", "yLabel": "specific energy (Wh/kg)", "xRange": [10, 3000], "yRange": [0, 260], "grid": true, "controls": [{"name": "Emax", "range": [100, 250], "value": 200, "label": "max specific energy (Wh/kg)"}], "functions": [{"expr": "Emax/(1 + x/300)", "label": "deliver faster -> usable energy drops"}]}
```

## The Li-ion family alone is a spectrum

- **LCO** (cobalt) - highest energy, used in phones; least safe.
- **NMC / NCA** - the EV workhorses; high energy, good power.
- **LFP** (LiFePO4) - flatter, safer, longer-lived; now dominant in stationary
  storage and many EVs.
- **LTO** (titanate) - very long life and fast charge, lower energy.

```matlab
% Energy stored in a 5 kg pack at different specific energies
mass = 5;                        % kg
specE = [35, 80, 150, 250];      % Wh/kg: lead-acid, NiMH, LFP, NMC
Etot = mass .* specE;            % Wh
```

```python
mass = 5                          # kg
specE = [35, 80, 150, 250]        # Wh/kg: lead-acid, NiMH, LFP, NMC
Etot = [mass*e for e in specE]    # Wh
```

> **Practical insight:** for a phone you maximise Wh/kg (NMC/LCO); for a home
> battery you maximise safety and cycle life at low cost (LFP); for engine
> cranking you maximise surge power (lead-acid). The application picks the
> chemistry.

**Next:** how a real cell behaves as you draw current.
""",
        ),
        _t(
            "Cell characteristics: OCV, C-rate & internal resistance",
            "12 min",
            """\
# Cell characteristics: OCV, C-rate & internal resistance

A datasheet voltage is a lie of omission. A real cell's terminal voltage depends
on how full it is, how hard you pull, and its internal losses.

## Open-circuit voltage (OCV) vs state of charge (SoC)

With no load, a rested cell settles to its **open-circuit voltage**, and OCV is a
**function of state of charge** - the fraction of capacity remaining,
$0$ to $1$. The OCV-SoC curve is the cell's fingerprint. A Li-ion cell sags
gently across the middle; an **LFP** cell is famously **flat** (great for
cycling, hard for SoC estimation):

```plot
{"title": "OCV vs state of charge: Li-ion vs flat LFP", "xLabel": "state of charge SoC", "yLabel": "open-circuit voltage (V)", "xRange": [0, 1], "yRange": [2.8, 4.3], "grid": true, "functions": [{"expr": "3.3 + 0.9*x - 0.25*exp(-12*x) + 0.15*exp(8*(x-1))", "label": "Li-ion (NMC)", "color": "#2563eb"}, {"expr": "3.1 + 0.35*x - 0.2*exp(-25*x) + 0.12*exp(20*(x-1))", "label": "LFP (flat)", "color": "#16a34a"}]}
```

## C-rate: how fast, relative to capacity

The **C-rate** normalises current to capacity. **1C** discharges the full
capacity in one hour; **2C** in half an hour; **0.5C** in two hours.

$$I = C_{rate} \\times Q, \\qquad t_{ideal} = \\frac{1}{C_{rate}}\\ \\text{hours}.$$

A $3\\,$Ah cell at $2$C draws $6\\,$A. Talking in C-rate lets one spec cover cells
of any size.

## Internal resistance and the discharge curve

A cell has **internal resistance** $R_0$, so under load the terminal voltage
drops below OCV:

$$V_{term} = \\text{OCV}(SoC) - I\\,R_0.$$

That is why the **discharge curve** (voltage vs time/capacity) sags more at high
current, and why the cell warms up ($P_{loss} = I^2 R_0$). Slide the current and
watch the whole discharge curve drop:

```plot
{"title": "Discharge curve sags under load: Vterm = OCV(SoC) - I*R0 (slide current)", "xLabel": "discharged capacity (fraction)", "yLabel": "terminal voltage (V)", "xRange": [0, 1], "yRange": [2.8, 4.3], "grid": true, "controls": [{"name": "I", "range": [0, 8], "value": 2, "label": "discharge current (A)"}], "functions": [{"expr": "3.3 + 0.9*(1-x) - 0.25*exp(-12*(1-x)) + 0.15*exp(8*((1-x)-1)) - I*0.05", "label": "Vterm under load"}]}
```

```matlab
Q = 3.0; Crate = 2;  R0 = 0.05;   % Ah, C, ohm
I = Crate * Q;                    % 6 A
Vdrop = I * R0;                   % 0.3 V sag
Ploss = I^2 * R0;                 % 1.8 W heating
```

```python
Q, Crate, R0 = 3.0, 2, 0.05       # Ah, C, ohm
I = Crate * Q                     # 6 A
Vdrop = I * R0                    # 0.3 V sag
Ploss = I**2 * R0                 # 1.8 W heating
```

> **Practical insight:** a flat OCV curve (LFP) is wonderful for delivering
> steady voltage but a nightmare for estimating SoC from voltage alone - a tiny
> voltage error maps to a huge SoC error. That is why the next courses lean on
> coulomb counting and Kalman filters.

**Next:** turning these effects into a circuit you can simulate.
""",
        ),
        _t(
            "The equivalent-circuit model: Rint & RC",
            "12 min",
            """\
# The equivalent-circuit model: Rint & RC

To **simulate** a cell (and to build a BMS that estimates its state), engineers
replace the messy electrochemistry with an **equivalent circuit** of an ideal
voltage source plus resistors and capacitors that reproduce the measured
behaviour.

## The Rint model (the simplest)

A voltage source equal to $\\text{OCV}(SoC)$ in series with a single internal
resistance $R_0$:

$$V_{term} = \\text{OCV}(SoC) - I\\,R_0.$$

```mermaid
flowchart LR
  OCV["OCV(SoC) source"] --> R0["R0 (series resistance)"]
  R0 --> TPLUS["terminal +"]
  GND["terminal -"] --> OCV
```

It captures the instant voltage drop under load - good enough for first-order
energy bookkeeping, but it ignores the cell's **dynamics**: real cells don't jump
to a new voltage instantly, they **relax** over seconds to minutes.

## The Thevenin / RC model (the workhorse)

Add a **parallel RC branch** ($R_1$ with $C_1$) in series. The RC pair models
**polarization** - the slow voltage recovery you see when you stop drawing
current. After a current step the RC voltage builds up (or decays) with time
constant $\\tau = R_1 C_1$:

$$V_{term} = \\text{OCV}(SoC) - I\\,R_0 - V_1, \\qquad \\tau = R_1 C_1.$$

```mermaid
flowchart LR
  OCV["OCV(SoC)"] --> R0["R0"]
  R0 --> RC["R1 || C1 (polarization)"]
  RC --> TPLUS["terminal +"]
```

Press Play to watch the terminal voltage recover after the load is removed (the
RC branch relaxing back toward OCV):

```plot
{"title": "Voltage relaxation after a load step (RC model, slide tau)", "xLabel": "time (s)", "yLabel": "terminal voltage (V)", "xRange": [0, 60], "yRange": [3.4, 3.85], "grid": true, "controls": [{"name": "tau", "range": [5, 40], "value": 15, "label": "RC time constant tau (s)"}], "animate": {"param": "t", "range": [0, 60], "label": "time (s)"}, "functions": [{"expr": "3.8 - 0.3*exp(-x/tau)", "label": "Vterm relaxing to OCV"}], "points": [{"xExpr": "t", "yExpr": "3.8 - 0.3*exp(-t/tau)", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

Two RC branches (a **second-order Thevenin model**) capture both a fast and a
slow relaxation even better - the standard in production BMS firmware.

```matlab
OCV = 3.8; R0 = 0.03; R1 = 0.02; C1 = 800;  % ohm, ohm, farad
tau = R1 * C1;                               % 16 s polarization
I = 2;                                       % A discharge
% first-order ODE: dV1/dt = -V1/tau + I/C1, Vterm = OCV - I*R0 - V1
```

```python
OCV, R0, R1, C1 = 3.8, 0.03, 0.02, 800       # ohm, ohm, farad
tau = R1 * C1                                 # 16 s polarization
I = 2                                         # A discharge
# dV1/dt = -V1/tau + I/C1, Vterm = OCV - I*R0 - V1
```

> **Practical insight:** the Rint model is one parameter and runs anywhere; the
> RC model adds the dynamics a BMS needs to track voltage during real drive
> cycles. The Advanced course fits these parameters to data and feeds them to a
> Kalman filter.

**Next:** what goes wrong - safety and degradation.
""",
        ),
        _t(
            "Safety & degradation basics",
            "11 min",
            """\
# Safety & degradation basics

Batteries store a lot of energy in a small space, and they wear out. Two topics
no battery engineer can skip: **how they fail dangerously**, and **how they age**.

## Thermal runaway: the dangerous failure

If a cell gets too hot (from overcharge, a short, physical damage, or a
manufacturing defect), exothermic reactions start that generate **more heat**,
which speeds up the reactions - a self-reinforcing loop called **thermal
runaway**. Once it crosses a tipping point, the cell vents, ignites, and can
propagate to neighbours.

```mermaid
stateDiagram-v2
  [*] --> Normal
  Normal --> Heating: overcharge / short / damage
  Heating --> Runaway: temperature passes onset
  Heating --> Normal: cooling / protection trips
  Runaway --> Venting
  Venting --> Fire
```

The feedback is why a small overheat can run away: heat generation rises roughly
**exponentially** with temperature while cooling rises only **linearly** - past
the crossover, temperature climbs without bound:

```plot
{"title": "Thermal runaway: heat generation overtakes cooling (slide onset)", "xLabel": "cell temperature (C)", "yLabel": "heat rate (W)", "xRange": [20, 120], "yRange": [0, 60], "grid": true, "controls": [{"name": "onset", "range": [50, 90], "value": 70, "label": "reaction onset (C)"}], "functions": [{"expr": "2*exp((x-onset)/12)", "label": "heat generated (reactions)", "color": "#dc2626"}, {"expr": "0.4*(x-20)", "label": "heat removed (cooling)", "color": "#2563eb"}]}
```

The crossing point is the danger threshold: below it cooling wins; above it
generation wins and the cell runs away. **Protection** (the next courses) keeps
the cell far from this region: voltage/current/temperature limits, fuses, and
cell isolation.

## Aging: the slow failure

Even used gently, cells degrade. Two effects dominate:

- **Capacity fade** - the usable Ah shrinks (you store less). Driven by loss of
  cyclable lithium and active material.
- **Resistance growth** - $R_0$ rises (more sag, more heat, less power).

**Cycle life** is how many full charge-discharge cycles a cell survives before
capacity drops to a threshold (often $80\\%$). Aging accelerates with **high
temperature**, **high SoC** (sitting full), **deep discharge**, and **high
C-rate**. Capacity fades roughly with the square root of cycles early on:

```plot
{"title": "Capacity fade vs cycles (slide fade rate)", "xLabel": "charge-discharge cycles", "yLabel": "remaining capacity (%)", "xRange": [0, 3000], "yRange": [60, 102], "grid": true, "controls": [{"name": "k", "range": [0.3, 1.5], "value": 0.7, "label": "fade rate"}], "functions": [{"expr": "100 - k*sqrt(x)", "label": "capacity (%)"}]}
```

```matlab
cap0 = 3.0;                       % Ah when new
cycles = 1000; k = 0.7;
cap_now = cap0*(1 - (k*sqrt(cycles))/100);   % faded capacity
soh = cap_now/cap0 * 100;                    % state of health (%)
```

```python
import numpy as np
cap0 = 3.0                        # Ah when new
cycles, k = 1000, 0.7
cap_now = cap0*(1 - (k*np.sqrt(cycles))/100) # faded capacity
soh = cap_now/cap0 * 100                     # state of health (%)
```

> **Practical insight:** to make a pack last, keep it **cool**, avoid sitting at
> $100\\%$ or near empty, and limit fast charging. EVs deliberately hide the top
> and bottom few percent of the pack to extend life - the user never sees the
> full chemical range.

**Next:** simulate a real discharge curve from a cell model yourself.
""",
        ),
        _code(
            "Lab: discharge curve from a cell model",
            "13 min",
            """\
# Simulate a Li-ion cell discharging at constant current.
# Model: SoC drops by coulomb counting; terminal voltage = OCV(SoC) - I*R0 - V1
# where V1 is a polarization RC branch. Pure numpy + matplotlib, module level.
import numpy as np
import matplotlib.pyplot as plt

# Cell parameters
Q_Ah = 3.0          # capacity (amp-hours)
R0 = 0.05           # series resistance (ohm)
R1 = 0.03           # polarization resistance (ohm)
C1 = 1000.0         # polarization capacitance (farad) -> tau = 30 s
Vcut = 3.0          # cut-off voltage

# OCV(SoC) as a smooth empirical curve (SoC in 0..1)
soc_grid = np.linspace(0, 1, 200)
ocv_grid = 3.3 + 0.9*soc_grid - 0.25*np.exp(-12*soc_grid) + 0.15*np.exp(8*(soc_grid - 1))

dt = 1.0                          # 1 second steps
Q_coulomb = Q_Ah * 3600.0         # capacity in coulombs

plt.figure(figsize=(8, 4))
for I, color in [(1.0, "#16a34a"), (3.0, "#2563eb"), (6.0, "#dc2626")]:
    soc = 1.0
    v1 = 0.0
    t_hist = []
    v_hist = []
    t = 0.0
    # discharge until cut-off or empty
    while soc > 0.0:
        ocv = np.interp(soc, soc_grid, ocv_grid)
        v1 = v1 + dt*(-v1/(R1*C1) + I/C1)     # RC branch update
        vterm = ocv - I*R0 - v1
        if vterm <= Vcut:
            break
        t_hist.append(t/60.0)                 # minutes
        v_hist.append(vterm)
        soc = soc - (I*dt)/Q_coulomb
        t = t + dt
    crate = I/Q_Ah
    plt.plot(t_hist, v_hist, color=color, lw=2, label=f"I={I:.0f} A ({crate:.1f}C)")
    print(f"I={I:.0f} A: ran {t/60.0:.1f} min, delivered {(1.0-soc)*Q_Ah:.2f} Ah")

plt.axhline(Vcut, ls="--", color="#94a3b8", label="cut-off")
plt.xlabel("time (min)"); plt.ylabel("terminal voltage (V)")
plt.title("Li-ion discharge curves at different C-rates")
plt.legend(); plt.grid(True); plt.show()

# Try it yourself:
#   1. Raise R0 to 0.15 (an aged cell): every curve sags and cuts off sooner.
#   2. Lower Vcut to 2.7: more capacity delivered, but deeper discharge ages it.
""",
        ),
    ),
)


# -- Battery Management & Energy Storage -- Intermediate -----------------------

_BATTERY_INTERMEDIATE = SeedCourse(
    slug="battery-intermediate",
    title="Battery Management & Energy Storage -- Intermediate: BMS & State Estimation",
    description=(
        "The battery management system and how it keeps a pack safe and "
        "accurate: BMS functions and architecture (analog front-end, "
        "protection), state-of-charge estimation (coulomb counting, OCV lookup, "
        "the Kalman approach), state of health and aging, passive vs active cell "
        "balancing, and pack design (series/parallel scaling, thermal "
        "management) - with dual MATLAB/Python, interactive plots, and a runnable "
        "coulomb-counting / balancing lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The battery management system",
            "12 min",
            """\
# The battery management system

A pack of cells is dangerous and dumb on its own. The **battery management
system (BMS)** is the electronics and firmware that makes it safe, accurate, and
long-lived. Its jobs:

- **Protect** - never let any cell exceed safe voltage, current, or temperature.
- **Monitor** - measure every cell's voltage, the pack current, and temperatures.
- **Estimate** - compute state of charge (SoC) and state of health (SoH).
- **Balance** - keep cells at matching charge (next lessons).
- **Communicate** - report to the charger, the vehicle, or the grid controller.

```mermaid
flowchart TB
  CELLS["cell stack"] --> AFE["analog front-end (AFE): cell V, current, temp"]
  AFE --> MCU["BMS controller (SoC/SoH, logic)"]
  MCU --> PROT["protection: contactors / FETs / fuse"]
  MCU --> BAL["balancing circuits"]
  MCU --> COMMS["comms: CAN / charger / host"]
  PROT --> PACK["pack terminals"]
```

## The analog front-end (AFE)

The **AFE** is the measurement chip(s) that sit across the cells. It must measure
each **series cell voltage** to millivolt accuracy (a tiny error wrecks SoC on a
flat LFP curve), measure **pack current** through a shunt or Hall sensor, and
read **temperatures** at several points. In a big pack the AFEs are
**daisy-chained** modules, each watching a dozen or so cells, reporting up to the
main controller.

## Protection: the safe operating area

The BMS keeps every cell inside its **safe operating area (SOA)** - a box in
voltage, current, and temperature. Cross a limit and it acts (warn, derate, or
open the contactors). The voltage window is hard-bounded:

```plot
{"title": "Protection window: allowed current vs cell voltage (slide derate temp)", "xLabel": "cell voltage (V)", "yLabel": "allowed current (A)", "xRange": [2.5, 4.4], "yRange": [0, 60], "grid": true, "controls": [{"name": "Tderate", "range": [0.5, 1], "value": 1, "label": "thermal derate factor"}], "functions": [{"expr": "Tderate*50*(x>3.0)*(x<4.2)", "label": "allowed current (cut at 3.0 and 4.2 V)"}]}
```

Inside the window full current is allowed; outside it the BMS clamps to zero.

## Where it lives

- **EV**: a master BMS plus slave AFE boards on each module, talking over CAN to
  the vehicle.
- **Laptop/phone**: a single "fuel gauge + protection" IC.
- **Grid storage**: a hierarchy - cell, module, rack, and site controllers.

```matlab
Vmin = 3.0; Vmax = 4.2; Imax = 50;     % SOA limits
vcell = 4.25;
allowed = Imax * (vcell > Vmin) * (vcell < Vmax);   % -> 0, over voltage
```

```python
Vmin, Vmax, Imax = 3.0, 4.2, 50        # SOA limits
vcell = 4.25
allowed = Imax * (vcell > Vmin) * (vcell < Vmax)    # -> 0, over voltage
```

> **Practical insight:** the BMS is a safety system first and a fuel gauge
> second. When in doubt it disconnects - an annoyed user is better than a fire.

**Next:** the headline number - how much charge is left.
""",
        ),
        _t(
            "State-of-charge estimation",
            "13 min",
            """\
# State-of-charge estimation

**State of charge (SoC)** is the fuel gauge: the fraction of usable capacity
remaining, $0$ to $1$. You cannot measure it directly - you must **estimate** it.
Three methods, each with a flaw, combine into the real answer.

## 1. Coulomb counting (current integration)

Integrate current in and out, scaled by capacity:

$$SoC(t) = SoC(0) - \\frac{1}{Q}\\int_0^t I(\\tau)\\,d\\tau.$$

Accurate over short spans, but it **drifts**: any current-sensor bias accumulates
forever, and it needs a correct starting point and a correct $Q$ (which fades
with age). Watch a small sensor bias slowly corrupt the estimate:

```plot
{"title": "Coulomb-counting drift from sensor bias (slide bias)", "xLabel": "time (hours)", "yLabel": "SoC error (%)", "xRange": [0, 10], "yRange": [-15, 15], "grid": true, "controls": [{"name": "bias", "range": [-1, 1], "value": 0.5, "label": "current sensor bias (A)"}], "functions": [{"expr": "bias*3*x", "label": "accumulated SoC error"}]}
```

## 2. OCV lookup

Let the cell **rest**, measure its open-circuit voltage, and look up SoC on the
OCV-SoC curve. Drift-free and absolute - but only valid at rest (it needs
minutes to relax), and **useless on the flat part** of an LFP curve, where a
millivolt of error is a big chunk of SoC.

```mermaid
flowchart LR
  CC["coulomb counting (good short-term, drifts)"] --> FUSE["sensor fusion (Kalman filter)"]
  OCV["OCV lookup (absolute, only at rest)"] --> FUSE
  FUSE --> SOC["robust SoC estimate"]
```

## 3. The Kalman filter (fuse them)

A **Kalman filter** runs the cell's equivalent-circuit model, predicting voltage
from the coulomb-counted SoC, then **corrects** the SoC whenever the measured
terminal voltage disagrees with the model's prediction. It blends coulomb
counting's short-term accuracy with OCV's long-term anchoring, automatically
trusting each more or less based on noise. Slide the correction gain to see a
drifting estimate pulled back to truth:

```plot
{"title": "Kalman correction pulls a drifting estimate back to truth (slide gain)", "xLabel": "time (hours)", "yLabel": "SoC error (%)", "xRange": [0, 10], "yRange": [-2, 12], "grid": true, "controls": [{"name": "L", "range": [0.1, 1.5], "value": 0.6, "label": "correction gain"}], "functions": [{"expr": "10*exp(-L*x)", "label": "estimation error decays"}]}
```

```matlab
Q = 3.0*3600; soc = 0.8; dt = 1;       % coulombs, start 80%, 1 s
I = 2.0;                               % discharge current (A)
soc = soc - (I*dt)/Q;                  % coulomb-counting step
```

```python
Q = 3.0*3600; soc = 0.8; dt = 1        # coulombs, start 80%, 1 s
I = 2.0                                # discharge current (A)
soc = soc - (I*dt)/Q                   # coulomb-counting step
```

> **Practical insight:** production fuel gauges run coulomb counting continuously
> and re-anchor to OCV whenever the pack rests long enough, all wrapped in a
> Kalman filter. The Advanced course builds the model-based EKF version.

**Next:** not just how full, but how worn - state of health.
""",
        ),
        _t(
            "State of health & aging",
            "12 min",
            """\
# State of health & aging

A cell that holds $80\\%$ of its original capacity is still "full" at $100\\%$ SoC -
it just holds less. **State of health (SoH)** tracks that wear so the BMS can
keep SoC honest and predict end of life.

## Two faces of aging

- **Capacity fade** - usable Ah shrinks. The natural SoH metric:

$$SoH_{cap} = \\frac{Q_{now}}{Q_{new}} \\times 100\\%.$$

- **Resistance (power) fade** - $R_0$ grows, so the cell sags more and delivers
  less peak power. A second SoH metric:

$$SoH_{res} = \\frac{R_{new}}{R_{now}} \\times 100\\%.$$

End of life is often defined as SoH reaching $80\\%$ (capacity) or $R_0$
doubling - whichever the application cares about (an EV cares about range,
a power tool about peak current).

## What drives it: calendar vs cycle aging

- **Cycle aging** - wear per charge-discharge cycle (mechanical stress, lithium
  plating). Worse at high C-rate and deep depth-of-discharge.
- **Calendar aging** - wear just from **time**, even idle. Worse at high
  temperature and high SoC.

Both accelerate sharply with **temperature** - a rough rule is that life roughly
**halves for every 10 C** rise. Slide temperature to see cycle life collapse:

```plot
{"title": "Cycle life collapses with temperature (slide reference life)", "xLabel": "average temperature (C)", "yLabel": "cycle life (cycles)", "xRange": [10, 60], "yRange": [0, 6000], "grid": true, "controls": [{"name": "L25", "range": [2000, 5000], "value": 3000, "label": "cycle life at 25 C"}], "functions": [{"expr": "L25*pow(0.5, (x-25)/10)", "label": "cycle life (halves per +10 C)"}]}
```

Shallow cycling helps too: discharging only the middle band of the pack many
times is far gentler than full $0$-to-$100\\%$ cycles. Slide the depth-of-discharge:

```plot
{"title": "Shallow cycling lasts longer: cycles vs depth-of-discharge (slide DoD)", "xLabel": "depth of discharge (%)", "yLabel": "achievable cycles", "xRange": [10, 100], "yRange": [0, 12000], "grid": true, "controls": [{"name": "base", "range": [1500, 4000], "value": 2500, "label": "full-cycle life"}], "functions": [{"expr": "base*100/x", "label": "cycles ~ base*100/DoD"}]}
```

```matlab
Qnew = 3.0; Qnow = 2.55;               % Ah
soh = Qnow/Qnew * 100;                 % 85% state of health
Rnew = 0.03; Rnow = 0.05;
soh_pow = Rnew/Rnow * 100;             % 60% power SoH
```

```python
Qnew, Qnow = 3.0, 2.55                 # Ah
soh = Qnow/Qnew * 100                  # 85% state of health
Rnew, Rnow = 0.03, 0.05
soh_pow = Rnew/Rnow * 100              # 60% power SoH
```

> **Practical insight:** SoH feeds back into SoC: the gauge must divide by the
> **present** capacity, not the nameplate. EVs estimate SoH continuously and use
> it to update the displayed range and to schedule warranty decisions.

**Next:** why cells in a pack drift apart - and how to fix it.
""",
        ),
        _t(
            "Cell balancing: passive vs active",
            "12 min",
            """\
# Cell balancing: passive vs active

Cells in series should hold the same charge, but they never quite do.
Manufacturing spread, temperature differences across the pack, and uneven aging
make them **drift apart**. Because series cells share the same current, the
**weakest cell** decides when charging stops (it hits the upper limit first) and
when discharging stops (it hits the lower limit first) - so an unbalanced pack
**wastes capacity** and risks over-stressing the outlier.

## Why a pack drifts

```mermaid
flowchart LR
  SPREAD["manufacturing spread"] --> DRIFT["cells drift apart"]
  TEMP["temperature gradient across pack"] --> DRIFT
  AGE["uneven aging / self-discharge"] --> DRIFT
  DRIFT --> WEAK["weakest cell limits the whole pack"]
```

## Passive balancing (bleed the strong)

Each cell gets a resistor and a switch. The BMS turns on the resistor across the
**fullest** cells, **burning off** their excess as heat until the laggards catch
up. Simple and cheap (it dominates EVs and most products), but it **wastes
energy** and only equalises during charge. Watch the high cells bleed down to the
pack average over time:

```plot
{"title": "Passive balancing bleeds the high cells to the average (slide bleed rate)", "xLabel": "time (minutes)", "yLabel": "cell voltage above average (mV)", "xRange": [0, 120], "yRange": [-5, 45], "grid": true, "controls": [{"name": "rate", "range": [0.01, 0.08], "value": 0.03, "label": "bleed rate (1/min)"}], "functions": [{"expr": "40*exp(-rate*x)", "label": "high cell", "color": "#dc2626"}, {"expr": "20*exp(-rate*x)", "label": "mid cell", "color": "#f59e0b"}]}
```

## Active balancing (move charge)

Instead of burning energy, **active balancing** **transfers** charge from full
cells to empty ones using capacitors, inductors, or DC-DC converters. It is far
more efficient and works while discharging too - but it is more complex and
costly. Reserved for large, high-value packs (grid storage, some EVs).

| | Passive | Active |
|--|---------|--------|
| Method | bleed excess as heat | move charge between cells |
| Efficiency | low (wastes energy) | high |
| Cost / complexity | low | higher |
| When | mostly during charge | charge and discharge |
| Typical use | EVs, consumer packs | grid, premium EVs |

```matlab
vcells = [3.95 4.02 3.98 4.10];        % series cells (V)
vavg = mean(vcells);
bleed = vcells > (vavg + 0.02);        % turn on resistor where above avg+20mV
```

```python
import numpy as np
vcells = np.array([3.95, 4.02, 3.98, 4.10])   # series cells (V)
vavg = vcells.mean()
bleed = vcells > (vavg + 0.02)                  # bleed cells above avg+20 mV
```

> **Practical insight:** balancing fixes **charge** mismatch, not **capacity**
> mismatch - it cannot make a worn cell hold more. The usable pack capacity is
> still set by the weakest cell, which is why cell **matching** at manufacture and
> good thermal uniformity matter as much as the balancer.

**Next:** scaling one cell up into a real pack.
""",
        ),
        _t(
            "Pack design: series, parallel & thermal",
            "12 min",
            """\
# Pack design: series, parallel & thermal

One cell is ~$3.7\\,$V and a few Ah. Real systems need hundreds of volts and tens
of kWh, so you wire many cells into a **pack**. The notation is **xSyP**: $x$
cells in **series**, $y$ in **parallel**.

## Series adds voltage, parallel adds capacity

- **Series** (S): voltages add, capacity (Ah) stays the same.
  $V_{pack} = N_s \\times V_{cell}$.
- **Parallel** (P): capacities add, voltage stays the same.
  $Q_{pack} = N_p \\times Q_{cell}$.

So total energy scales with the **product**:

$$E_{pack} = N_s\\,N_p\\,V_{cell}\\,Q_{cell}.$$

Slide the parallel count and watch pack energy grow at a fixed series count:

```plot
{"title": "Pack energy vs parallel count, 96S, 3.6 V x 3 Ah cells (slide Np)", "xLabel": "cells in parallel (Np)", "yLabel": "pack energy (kWh)", "xRange": [1, 80], "yRange": [0, 90], "grid": true, "controls": [{"name": "Ns", "range": [48, 120], "value": 96, "label": "cells in series (Ns)"}], "functions": [{"expr": "Ns*x*3.6*3/1000", "label": "pack energy (kWh)"}]}
```

A typical EV pack is roughly **96S** (about $350\\,$V) with many cells in
parallel; a power-tool pack might be **5S2P**.

```mermaid
flowchart TB
  subgraph Module
    C1["cell"] --- C2["cell"] --- C3["cell"]
  end
  Module --> NEXT["...repeat in series for voltage..."]
  Module --> PAR["...parallel groups for capacity..."]
  NEXT --> BMS["BMS monitors every series group"]
```

The BMS monitors every **series group** (parallel cells self-balance, so a
"cell" to the BMS is one parallel group).

## Thermal management

Cells like **15-35 C**: too cold and resistance soars (and charging plates
lithium); too hot and they age fast and risk runaway. A pack must move heat in
and out and keep cells **uniform** (a hot corner ages faster and drags the pack
down). Cooling options scale with power:

| Cooling | Where |
|---------|-------|
| Passive (air, mass) | phones, small tools |
| Forced air | e-bikes, early EVs |
| Liquid (cold plates) | modern EVs, fast-charge |
| Refrigerant / immersion | high-performance, grid |

Heat generated is $P = I^2 R_0$ per cell, so high C-rate and high resistance
both push the cooling requirement up:

```plot
{"title": "Pack heat to remove vs current (slide pack resistance)", "xLabel": "pack current (A)", "yLabel": "heat generated (W)", "xRange": [0, 200], "yRange": [0, 4000], "grid": true, "controls": [{"name": "Rpack", "range": [0.02, 0.1], "value": 0.05, "label": "pack resistance (ohm)"}], "functions": [{"expr": "Rpack*x^2", "label": "P = I^2 * Rpack"}]}
```

```matlab
Ns = 96; Np = 50; Vcell = 3.6; Qcell = 3.0;
Vpack = Ns*Vcell;                  % ~346 V
Qpack = Np*Qcell;                  % 150 Ah
Epack = Vpack*Qpack/1000;          % ~51.8 kWh
```

```python
Ns, Np, Vcell, Qcell = 96, 50, 3.6, 3.0
Vpack = Ns*Vcell                   # ~346 V
Qpack = Np*Qcell                   # 150 Ah
Epack = Vpack*Qpack/1000           # ~51.8 kWh
```

> **Practical insight:** thermal uniformity is as important as average
> temperature - a pack is only as good as its hottest, weakest cell. Good packs
> spend real engineering on getting heat out evenly, not just out.

**Next:** put estimation and balancing together in code.
""",
        ),
        _code(
            "Lab: coulomb-counting SoC & cell balancing",
            "14 min",
            """\
# Two simulations in one lab:
#  (A) coulomb-counting SoC vs a biased sensor (shows drift),
#  (B) passive balancing of four series cells drifting apart.
# Pure numpy + matplotlib, module level only.
import numpy as np
import matplotlib.pyplot as plt

# ---- (A) Coulomb counting with a current-sensor bias ----
Q_Ah = 3.0
Q_coulomb = Q_Ah * 3600.0
dt = 1.0                          # 1 s steps
T = int(2*3600)                   # 2 hours
soc_true = 0.90
soc_est = 0.90
bias = 0.05                       # 50 mA sensor bias (estimator only)
I_load = 1.5                      # constant 1.5 A discharge

t_hist = np.zeros(T)
true_hist = np.zeros(T)
est_hist = np.zeros(T)
for k in range(T):
    soc_true = soc_true - (I_load*dt)/Q_coulomb
    soc_est = soc_est - ((I_load + bias)*dt)/Q_coulomb   # biased measurement
    t_hist[k] = k/3600.0
    true_hist[k] = soc_true*100
    est_hist[k] = soc_est*100

err = est_hist[-1] - true_hist[-1]
print(f"(A) after 2 h: true SoC={true_hist[-1]:.1f}%, est SoC={est_hist[-1]:.1f}%, drift={err:.2f}%")

# ---- (B) Passive balancing of 4 series cells ----
vcells = np.array([3.95, 4.05, 4.00, 4.12])   # initial spread (V)
steps = 600                       # minutes
bleed_k = 0.02                    # bleed strength
V = np.zeros((steps, 4))
for k in range(steps):
    vavg = vcells.mean()
    # bleed only cells above the average (passive: never adds charge)
    over = np.maximum(vcells - vavg, 0.0)
    vcells = vcells - bleed_k*over
    V[k] = vcells
print(f"(B) start spread={4.12-3.95:.3f} V, final spread={V[-1].max()-V[-1].min():.4f} V")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(t_hist, true_hist, color="#16a34a", label="true SoC")
ax1.plot(t_hist, est_hist, color="#dc2626", ls="--", label="coulomb-counted (biased)")
ax1.set_xlabel("time (h)"); ax1.set_ylabel("SoC (%)")
ax1.set_title("(A) Coulomb-counting drift"); ax1.legend(); ax1.grid(True)

for j, color in enumerate(["#2563eb", "#dc2626", "#16a34a", "#f59e0b"]):
    ax2.plot(np.arange(steps), V[:, j], color=color, label=f"cell {j+1}")
ax2.set_xlabel("time (min)"); ax2.set_ylabel("cell voltage (V)")
ax2.set_title("(B) Passive balancing converges"); ax2.legend(); ax2.grid(True)
plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Set bias = 0.0 in (A): the estimate tracks truth exactly (no drift).
#   2. Raise bleed_k in (B): cells converge faster (but waste more energy as heat).
""",
        ),
    ),
)


# -- Battery Management & Energy Storage -- Advanced ---------------------------

_BATTERY_ADVANCED = SeedCourse(
    slug="battery-advanced",
    title="Battery Management & Energy Storage -- Advanced: Systems, Grid & Fast Charging",
    description=(
        "Advanced battery systems: model-based state estimation (EKF and "
        "observers, parameter identification), electro-thermal modeling and "
        "management, fast-charging strategies (CC-CV, multi-stage, degradation "
        "tradeoffs), grid and stationary storage (peak shaving, frequency "
        "regulation), second life, recycling and alternatives (supercapacitors, "
        "solid-state, flow), and a cross-domain applications throughline - with "
        "dual MATLAB/Python, interactive plots, and a runnable EKF / thermal lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Advanced state estimation: EKF & observers",
            "13 min",
            """\
# Advanced state estimation: EKF & observers

The Intermediate course fused coulomb counting and OCV by hand. The production
answer is **model-based estimation**: run the cell's equivalent-circuit model in
software and correct it against the measured terminal voltage. Because OCV(SoC)
is **nonlinear**, the tool is the **extended Kalman filter (EKF)**.

## The state-space cell model

Take the first-order RC (Thevenin) model. The hidden **state** is the SoC and the
polarization voltage $V_1$; the **measurement** is terminal voltage:

$$\\begin{aligned}
SoC_{k+1} &= SoC_k - \\frac{\\Delta t}{Q}\\,I_k \\\\
V_{1,k+1} &= V_{1,k}\\,e^{-\\Delta t/(R_1 C_1)} + R_1\\left(1 - e^{-\\Delta t/(R_1 C_1)}\\right) I_k \\\\
y_k &= \\text{OCV}(SoC_k) - R_0 I_k - V_{1,k}
\\end{aligned}$$

## The predict-correct loop

```mermaid
flowchart LR
  PRED["predict: propagate SoC, V1 with model + current"] --> MEAS["measure terminal voltage"]
  MEAS --> INNOV["innovation = measured - predicted voltage"]
  INNOV --> CORR["correct: nudge state by Kalman gain * innovation"]
  CORR --> PRED
```

The EKF **linearizes** OCV(SoC) at the current estimate (its slope
$\\partial \\text{OCV}/\\partial SoC$ enters the measurement Jacobian), computes a
**Kalman gain** that weighs model trust against sensor noise, and corrects. It
converges to the truth even from a wrong start - watch the gain set how fast:

```plot
{"title": "EKF convergence from a bad initial SoC (slide measurement trust)", "xLabel": "time (s)", "yLabel": "SoC estimate error (%)", "xRange": [0, 200], "yRange": [-2, 22], "grid": true, "controls": [{"name": "L", "range": [0.005, 0.06], "value": 0.02, "label": "effective gain"}], "functions": [{"expr": "20*exp(-L*x)", "label": "error decays to zero"}]}
```

## Parameter identification

The model is only as good as $R_0, R_1, C_1$, and $Q$ - and they **change** with
SoC, temperature, and age. Engineers identify them offline (pulse tests:
apply a current step, fit the voltage response) and track them online (recursive
least squares, or a **dual/joint EKF** that estimates parameters alongside the
state). A pulse-relaxation response is what the fit keys on:

```plot
{"title": "Pulse test for parameter ID: voltage step (R0) then RC relax (R1,C1)", "xLabel": "time (s)", "yLabel": "terminal voltage (V)", "xRange": [0, 80], "yRange": [3.55, 3.85], "grid": true, "controls": [{"name": "tau", "range": [5, 30], "value": 12, "label": "RC time constant (s)"}], "functions": [{"expr": "3.8 - 0.08*(x<40) - 0.12*(x<40)*(1 - exp(-x/tau)) + 0.12*(x>=40)*exp(-(x-40)/tau)", "label": "pulse + relaxation"}]}
```

```matlab
% one EKF measurement update (scalar, conceptual)
dOCV = ocv_slope(soc);                  % d OCV / d SoC at current estimate
H = [dOCV, -1];                         % measurement Jacobian wrt [soc; v1]
K = P*H' / (H*P*H' + Rnoise);           % Kalman gain
x = x + K*(y_meas - y_pred);            % correct state
P = (eye(2) - K*H)*P;                   % covariance update
```

```python
import numpy as np
dOCV = ocv_slope(soc)                   # d OCV / d SoC
H = np.array([[dOCV, -1.0]])            # measurement Jacobian
K = P @ H.T / (H @ P @ H.T + Rnoise)    # Kalman gain
x = x + (K*(y_meas - y_pred)).ravel()   # correct state
P = (np.eye(2) - K @ H) @ P             # covariance update
```

> **Practical insight:** the EKF's secret is the OCV slope. On a flat LFP plateau
> that slope is nearly zero, so voltage tells the filter almost nothing about
> SoC - which is why LFP gauges lean harder on coulomb counting and rest-OCV
> re-anchoring.

**Next:** the heat side of the model - electro-thermal coupling.
""",
        ),
        _t(
            "Thermal modeling & management",
            "12 min",
            """\
# Thermal modeling & management

Temperature controls everything: resistance, capacity, aging, and safety. A
serious BMS runs a **thermal model** alongside the electrical one - together an
**electro-thermal model** - because the two feed each other (heat raises
resistance, resistance generates heat).

## Heat generation

A cell generates heat from two sources:

$$\\dot{Q}_{gen} = \\underbrace{I^2 R_0}_{\\text{irreversible (Joule)}} \\; + \\; \\underbrace{I\\,T\\,\\frac{dU}{dT}}_{\\text{reversible (entropic)}}.$$

The **irreversible** $I^2 R_0$ term dominates at high current; the **reversible**
entropic term can heat or cool depending on direction and is why a cell's heat
isn't perfectly symmetric in charge vs discharge.

## The lumped thermal model

Treat the cell as one thermal mass $m c_p$ losing heat to coolant at rate
$h A$ (Newton cooling):

$$m\\,c_p\\,\\frac{dT}{dt} = I^2 R_0 - h A\\,(T - T_{coolant}).$$

It is the same first-order ODE as an RC circuit: temperature rises toward a
steady value with a thermal time constant. Press Play to watch a cell heat up
under load and settle:

```plot
{"title": "Cell temperature rise under load (slide cooling strength)", "xLabel": "time (minutes)", "yLabel": "temperature rise above coolant (C)", "xRange": [0, 60], "yRange": [0, 40], "grid": true, "controls": [{"name": "hA", "range": [0.2, 1.5], "value": 0.6, "label": "cooling coefficient hA"}], "animate": {"param": "t", "range": [0, 60], "label": "time (min)"}, "functions": [{"expr": "(20/hA)*(1 - exp(-hA*x/10))", "label": "dT(t)"}], "points": [{"xExpr": "t", "yExpr": "(20/hA)*(1 - exp(-hA*t/10))", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

Stronger cooling (higher $hA$) both **lowers** the steady temperature and reaches
it faster.

## Managing it across the pack

```mermaid
flowchart LR
  GEN["I^2 R0 + entropic heat"] --> CELL["cell mass (m cp)"]
  CELL --> COOL["cooling: air / liquid cold plate"]
  COOL --> LOOP["chiller / radiator / heater"]
  LOOP --> CTRL["thermal controller: keep 15-35 C, uniform"]
```

Real packs **heat** in winter (to allow charging without lithium plating) and
**cool** in summer and during fast charge. The control target is not just average
temperature but **uniformity** - cell-to-cell spread under a few degrees - so the
pack ages evenly.

```matlab
m = 0.045; cp = 900; R0 = 0.03; hA = 0.4; Tcool = 25;  % SI
I = 8; T = 25; dt = 1;
dT = (I^2*R0 - hA*(T - Tcool))/(m*cp);    % dT/dt (C/s)
T = T + dT*dt;
```

```python
m, cp, R0, hA, Tcool = 0.045, 900, 0.03, 0.4, 25   # SI
I, T, dt = 8, 25, 1
dT = (I**2*R0 - hA*(T - Tcool))/(m*cp)     # dT/dt (C/s)
T = T + dT*dt
```

> **Practical insight:** fast charging is fundamentally a thermal problem - the
> heat is $I^2 R_0$ and $I$ is huge. The charge rate you can sustain is usually
> set by how fast you can pull heat out, not by the chemistry's ceiling.

**Next:** charging strategies and their tradeoffs.
""",
        ),
        _t(
            "Fast charging & charging strategies",
            "13 min",
            """\
# Fast charging & charging strategies

Charging is where convenience, capacity, and lifetime collide. Push current in
too hard and you plate lithium, heat the cell, and age it fast; too gently and
the user waits. The strategy is an engineered compromise.

## CC-CV: the standard profile

The classic Li-ion charge is **constant current, then constant voltage**:

1. **CC phase** - hold a fixed current; the voltage climbs as SoC rises.
2. **CV phase** - once the voltage hits the limit (e.g. $4.2\\,$V), hold that
   voltage; the current **tapers** exponentially as the cell fills.
3. **Termination** - stop when the taper current drops below a small threshold.

The CC phase does most of the work fast; the CV tail is slow (the last $20\\%$
takes a disproportionate share of the time). Press Play to watch current and
voltage trade places:

```plot
{"title": "CC-CV charge: voltage rises (CC) then current tapers (CV), slide cutoff", "xLabel": "time (minutes)", "yLabel": "value (V or normalized A)", "xRange": [0, 90], "yRange": [0, 4.4], "grid": true, "controls": [{"name": "tcv", "range": [30, 60], "value": 45, "label": "CC->CV transition (min)"}], "animate": {"param": "t", "range": [0, 90], "label": "time (min)"}, "functions": [{"expr": "min(4.2, 3.3 + 0.9*(x/tcv))", "label": "voltage (V)", "color": "#2563eb"}, {"expr": "4.0*((x<tcv) + (x>=tcv)*exp(-(x-tcv)/12))", "label": "current (scaled)", "color": "#dc2626"}], "points": [{"xExpr": "t", "yExpr": "min(4.2, 3.3 + 0.9*(t/tcv))", "label": "V now", "color": "#2563eb", "size": 6, "trail": true}]}
```

## Multi-stage and adaptive fast charging

To go faster without wrecking the cell, modern chargers use **multi-stage**
(several decreasing CC steps) or **model-based** profiles that respect limits on
**voltage, temperature, and lithium-plating** in real time. The harder the charge,
the more it ages the cell - the core tradeoff:

```plot
{"title": "Faster charge ages faster: capacity loss vs charge C-rate (slide temp)", "xLabel": "charge C-rate", "yLabel": "capacity loss per 100 cycles (%)", "xRange": [0.2, 4], "yRange": [0, 12], "grid": true, "controls": [{"name": "Tf", "range": [0.8, 2.5], "value": 1, "label": "temperature stress factor"}], "functions": [{"expr": "Tf*(0.4 + 0.6*x*x)", "label": "fade per 100 cycles"}]}
```

## The plating limit

Below the plating threshold, lithium intercalates safely; above it (high current,
low temperature, high SoC), metallic lithium **plates** on the anode -
irreversible capacity loss and a safety hazard. This is why you **cannot** fast
charge a cold battery, and why charge current is **derated** as the cell fills.

```mermaid
flowchart LR
  START["start charge"] --> CC["CC: high current"]
  CC --> CHECK{"voltage at limit?"}
  CHECK -- no --> CC
  CHECK -- yes --> CV["CV: taper current"]
  CV --> TERM{"current < cutoff?"}
  TERM -- no --> CV
  TERM -- yes --> DONE["done"]
```

```matlab
Vlim = 4.2; Icc = 3.0; Iterm = 0.1; dt = 1; soc = 0.2;
% CC until Vlim, then CV taper (conceptual one-step)
v = ocv(soc) + Icc*R0;
if v < Vlim
    I = Icc;                       % CC phase
else
    I = max(Iterm, I*exp(-dt/30)); % CV taper
end
```

```python
import numpy as np
Vlim, Icc, Iterm, dt, soc = 4.2, 3.0, 0.1, 1, 0.2
v = ocv(soc) + Icc*R0
if v < Vlim:
    I = Icc                        # CC phase
else:
    I = max(Iterm, I*np.exp(-dt/30))  # CV taper
```

> **Practical insight:** the "10-80% in 18 minutes" you see on EVs is exactly the
> CC region; the last 20% is deliberately slow to protect the cell. Charge
> curves are shaped by temperature and SoC limits, not a single C-rate number.

**Next:** scaling all of this up to the grid.
""",
        ),
        _t(
            "Grid & stationary storage",
            "12 min",
            """\
# Grid & stationary storage

Move from one device to the **power grid** and batteries become infrastructure.
A grid-scale **battery energy storage system (BESS)** is thousands of cells in
racks, with site-level BMS, inverters, and cooling - sized in **MWh** and **MW**.

## What it does for the grid

| Service | Time scale | What it does |
|---------|-----------|--------------|
| **Peak shaving** | hours | charge when demand/price is low, discharge at peak |
| **Frequency regulation** | seconds | inject/absorb power to hold grid frequency at 50/60 Hz |
| **Renewable firming** | minutes-hours | smooth solar/wind so the output is dispatchable |
| **Backup / black start** | minutes-hours | ride through outages, restart the grid |

## Peak shaving

The battery flattens the demand curve: it **charges** during cheap off-peak
hours and **discharges** to cover the daily peak, cutting the costly peak draw.
Slide the battery power and watch the peak get clipped:

```plot
{"title": "Peak shaving: battery clips the daily demand peak (slide battery power)", "xLabel": "hour of day", "yLabel": "grid demand (MW)", "xRange": [0, 24], "yRange": [0, 12], "grid": true, "controls": [{"name": "Pbatt", "range": [0, 4], "value": 2, "label": "battery power (MW)"}], "functions": [{"expr": "6 + 4*exp(-(x-18)*(x-18)/8)", "label": "raw demand", "color": "#94a3b8"}, {"expr": "6 + 4*exp(-(x-18)*(x-18)/8) - Pbatt*exp(-(x-18)*(x-18)/8)", "label": "with battery", "color": "#16a34a"}]}
```

## Frequency regulation

Grid frequency rises when generation exceeds load and falls when load exceeds
generation. A BESS responds in **milliseconds** - far faster than a gas turbine -
charging or discharging proportionally to the frequency error to pull it back to
nominal. Batteries excel here precisely because they are fast and bidirectional.

```mermaid
flowchart LR
  GRID["grid frequency"] --> ERR["error = f - 60 Hz"]
  ERR --> CTRL["droop controller"]
  CTRL --> BESS["BESS charges or discharges"]
  BESS --> GRID
```

## Economics and round-trip efficiency

A BESS earns money on the **spread** (buy cheap energy, sell expensive) and on
**ancillary services** (regulation). Every cycle loses energy to inefficiency -
**round-trip efficiency** (RTE), typically $85$-$95\\%$ - and to degradation, so
operators model the **levelized cost of storage** carefully. LFP dominates here:
cheap, safe, and long-lived matter more than energy density when the battery
sits in a field.

```matlab
buy = 30; sell = 120; rte = 0.88;      % $/MWh, round-trip efficiency
profit_per_MWh = sell*rte - buy;       % spread after losses
```

```python
buy, sell, rte = 30, 120, 0.88         # $/MWh, round-trip efficiency
profit_per_MWh = sell*rte - buy        # spread after losses
```

> **Practical insight:** grid storage flips the priorities of consumer
> electronics. Nobody carries it, so energy density barely matters; what matters
> is cost per kWh, cycle life, round-trip efficiency, and safety. That is why the
> grid runs on LFP (and increasingly on flow and other long-duration tech).

**Next:** what happens at end of life, and what might replace lithium.
""",
        ),
        _t(
            "Second life, recycling & alternatives",
            "12 min",
            """\
# Second life, recycling & alternatives

A Li-ion pack that drops to ~$80\\%$ SoH is "done" for an EV but still holds most
of its energy. Sustainability and supply demand we look past first use.

## Second life

An $80\\%$-SoH EV pack is fine for a **less demanding** job - stationary storage,
backup power, solar buffering - where weight and peak power matter less. After a
diagnostic grading, retired EV modules get rebuilt into BESS, getting a second
5-10 years before recycling. The catch: mixed history means uneven aging, so
second-life packs need careful BMS screening and balancing.

```mermaid
flowchart LR
  EV["EV use (100 -> 80% SoH)"] --> GRADE["grade & test"]
  GRADE --> SECOND["second life: stationary storage (80 -> 60%)"]
  SECOND --> RECYCLE["recycle: recover Li, Ni, Co, Cu"]
  RECYCLE --> NEW["new cells"]
```

## Recycling

At true end of life, recycling recovers the valuable metals - **lithium,
nickel, cobalt, copper** - by **pyrometallurgy** (smelting), **hydrometallurgy**
(leaching), or **direct recycling** (recovering cathode material intact). It
closes the loop on a constrained, geopolitically sensitive supply chain and cuts
the mining footprint.

## Alternatives and complements

No single technology wins everywhere - match the device to the job:

| Technology | Energy density | Strength | Best for |
|------------|----------------|----------|----------|
| **Supercapacitor** | very low | huge power, ~1M cycles, fast | power buffering, regen bursts |
| **Solid-state Li** | very high (potential) | safer, denser (maturing) | next-gen EV (emerging) |
| **Flow battery** | low (per volume) | decouples power and energy, very long life | long-duration grid storage |
| **Sodium-ion** | medium | cheap, no lithium/cobalt | cost-driven storage |

A **supercapacitor** stores charge physically (no slow chemistry), so it charges
and discharges in **seconds** and survives a million cycles - but holds little
energy. It pairs beautifully with a battery: the cap handles the fast bursts
(regenerative braking, pulse loads) while the battery handles the bulk energy.
The Ragone tradeoff again - power vs energy:

```plot
{"title": "Supercapacitor vs battery on the power-energy map (slide device)", "xLabel": "specific power (W/kg)", "yLabel": "specific energy (Wh/kg)", "xRange": [50, 12000], "yRange": [0, 260], "grid": true, "controls": [{"name": "shift", "range": [0.5, 2], "value": 1, "label": "tech improvement factor"}], "functions": [{"expr": "shift*220/(1 + x/250)", "label": "battery (high energy)", "color": "#2563eb"}, {"expr": "shift*8*(1 + x/2000)", "label": "supercapacitor (high power)", "color": "#16a34a"}]}
```

**Flow batteries** pump liquid electrolyte from tanks through a cell stack, so you
size **power** (stack) and **energy** (tank volume) **independently** - ideal for
multi-hour grid storage. Scaling energy is just bigger tanks:

```plot
{"title": "Flow battery: energy scales with tank volume, power fixed (slide concentration)", "xLabel": "tank volume (m3)", "yLabel": "stored energy (MWh)", "xRange": [0, 50], "yRange": [0, 30], "grid": true, "controls": [{"name": "conc", "range": [0.3, 0.8], "value": 0.5, "label": "electrolyte energy density (MWh/m3)"}], "functions": [{"expr": "conc*x", "label": "energy = density * volume"}]}
```

```matlab
soh_retire = 0.80; soh_second_end = 0.60;
usable_second_life = soh_retire - soh_second_end;   % 20% more usable life
```

```python
soh_retire, soh_second_end = 0.80, 0.60
usable_second_life = soh_retire - soh_second_end    # 20% more usable life
```

> **Practical insight:** the future is plural - solid-state for energy-dense EVs,
> flow and sodium-ion for cheap long-duration grid storage, supercapacitors for
> power bursts, and aggressive recycling underneath it all. The BMS skills
> transfer across every one.

**Next:** simulate a model-based estimator (EKF) and the thermal model.
""",
        ),
        _code(
            "Lab: EKF SoC estimator with a thermal check",
            "15 min",
            """\
# A simplified extended Kalman filter (EKF) estimating SoC of an RC-model cell,
# plus a lumped thermal trace alongside. Pure numpy + matplotlib, module level.
import numpy as np
import matplotlib.pyplot as plt

# ---- cell + model parameters ----
Q_Ah = 3.0
Q_coulomb = Q_Ah*3600.0
R0, R1, C1 = 0.05, 0.03, 1000.0
dt = 1.0
N = 1200                              # 20 minutes

# OCV(SoC) on a grid (same family as the Basics lab)
sg = np.linspace(0, 1, 400)
og = 3.3 + 0.9*sg - 0.25*np.exp(-12*sg) + 0.15*np.exp(8*(sg - 1))

# a current profile: discharge pulses
I = np.zeros(N)
I[100:400] = 2.0
I[600:1000] = 4.0

# ---- "true" cell (what we measure noisily) ----
soc_true = 0.80
v1_true = 0.0
y_meas = np.zeros(N)
soc_true_hist = np.zeros(N)
rng = np.random.default_rng(0)
for k in range(N):
    ocv = np.interp(soc_true, sg, og)
    v1_true = v1_true*np.exp(-dt/(R1*C1)) + R1*(1 - np.exp(-dt/(R1*C1)))*I[k]
    y_meas[k] = ocv - R0*I[k] - v1_true + rng.normal(0, 0.005)   # 5 mV noise
    soc_true_hist[k] = soc_true
    soc_true = soc_true - (I[k]*dt)/Q_coulomb

# ---- EKF starting from a WRONG initial SoC ----
x = np.array([0.60, 0.0])             # [SoC, V1] bad guess (true is 0.80)
P = np.diag([0.05, 1e-4])
Qn = np.diag([1e-7, 1e-6])            # process noise
Rn = 0.005**2                         # measurement noise
a1 = np.exp(-dt/(R1*C1))
soc_est_hist = np.zeros(N)
T = 25.0; m_cp = 0.045*900; hA = 0.4; Tcool = 25.0
T_hist = np.zeros(N)
for k in range(N):
    # predict
    x[0] = x[0] - (I[k]*dt)/Q_coulomb
    x[1] = x[1]*a1 + R1*(1 - a1)*I[k]
    F = np.array([[1.0, 0.0], [0.0, a1]])
    P = F @ P @ F.T + Qn
    # measurement prediction + Jacobian (numeric OCV slope)
    ocv = np.interp(x[0], sg, og)
    slope = np.interp(x[0] + 1e-3, sg, og) - np.interp(x[0] - 1e-3, sg, og)
    dOCV = slope/2e-3
    y_pred = ocv - R0*I[k] - x[1]
    H = np.array([[dOCV, -1.0]])
    S = (H @ P @ H.T)[0, 0] + Rn
    K = (P @ H.T)/S
    x = x + (K.ravel())*(y_meas[k] - y_pred)
    P = (np.eye(2) - K @ H) @ P
    soc_est_hist[k] = x[0]
    # thermal trace driven by the same current
    T = T + dt*(I[k]**2*R0 - hA*(T - Tcool))/m_cp
    T_hist[k] = T

t = np.arange(N)*dt/60.0
err0 = (soc_est_hist[0] - soc_true_hist[0])*100
errN = (soc_est_hist[-1] - soc_true_hist[-1])*100
print(f"EKF SoC error: start {err0:.1f}%  ->  end {errN:.2f}%  (converged)")
print(f"peak cell temperature: {T_hist.max():.1f} C")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(t, soc_true_hist*100, color="#16a34a", lw=2, label="true SoC")
ax1.plot(t, soc_est_hist*100, color="#dc2626", ls="--", label="EKF estimate")
ax1.set_xlabel("time (min)"); ax1.set_ylabel("SoC (%)")
ax1.set_title("EKF converges from a wrong start"); ax1.legend(); ax1.grid(True)
ax2.plot(t, T_hist, color="#2563eb", lw=2)
ax2.set_xlabel("time (min)"); ax2.set_ylabel("temperature (C)")
ax2.set_title("Lumped thermal trace under the load"); ax2.grid(True)
plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Start x = [0.95, 0.0]: the EKF still converges down to the truth.
#   2. Raise Rn (trust the model more): convergence slows and rides through noise.
""",
        ),
        _t(
            "Applications & the throughline",
            "11 min",
            """\
# Applications & the throughline

Everything in this track - cells, models, the BMS, estimation, thermal, charging,
and systems - comes together differently depending on **what the battery is for**.
The same physics, three very different sets of priorities.

## Electric vehicles (EV)

The headline application. An EV pack balances **energy** (range), **power**
(acceleration and fast charge), **safety**, and **life** (warranty), in a
weight- and volume-constrained box.

- **Chemistry:** NMC/NCA for range, LFP for cost/safety/longevity.
- **BMS:** master + module AFEs over CAN, EKF SoC, continuous SoH for range
  display and warranty.
- **Thermal:** liquid cooling, winter pre-heating before fast charge.
- **Charging:** CC-CV with aggressive but plating-aware fast-charge profiles.

## Grid and stationary storage

Weight is free, cycles are everything.

- **Chemistry:** LFP (and flow, sodium-ion) - cost, cycle life, safety over
  density.
- **BMS:** hierarchical (cell/module/rack/site), active balancing on premium
  systems.
- **Use:** peak shaving, frequency regulation, renewable firming, backup.
- **Economics:** round-trip efficiency and levelized cost dominate decisions.

## Portable and consumer

Energy density per gram and per dollar, plus safety in your pocket.

- **Chemistry:** high-energy Li-ion (LCO/NMC).
- **BMS:** a single fuel-gauge + protection IC; passive balancing.
- **Use:** phones, laptops, tools, wearables, drones.

```mermaid
flowchart TB
  PHYS["same physics: cells, models, BMS, estimation, thermal"]
  PHYS --> EV["EV: energy + power + safety + life, liquid-cooled"]
  PHYS --> GRID["grid: cost + cycles + RTE, LFP/flow"]
  PHYS --> PORT["portable: energy density, single-IC BMS"]
```

## The cost-per-cycle throughline

One number ties the field together: the **effective cost of stored energy over
the life of the pack** - capital cost spread across all the energy it will ever
deliver. Longer cycle life and higher round-trip efficiency both drive it down,
which is why grid and EV makers obsess over them. Slide cycle life to see cost
per delivered kWh fall:

```plot
{"title": "Lifetime cost per delivered kWh vs cycle life (slide pack price)", "xLabel": "cycle life (cycles)", "yLabel": "cost per delivered kWh ($)", "xRange": [500, 8000], "yRange": [0, 0.6], "grid": true, "controls": [{"name": "price", "range": [100, 400], "value": 200, "label": "pack price ($/kWh)"}], "functions": [{"expr": "price/(x*0.9)", "label": "cost / (cycles * RTE)"}]}
```

More cycles and better efficiency turn an expensive pack into cheap delivered
energy - the economic engine behind the whole transition to storage.

## The throughline, stated plainly

A battery is **stored chemical energy** released as current, described by a
**model** (OCV + resistance + dynamics), kept safe and accurate by a **BMS** that
**estimates** SoC/SoH and **manages** temperature, charged by a **strategy** that
trades speed for life, and scaled into **systems** from a phone to the grid. The
chemistry and the scale change; the engineering - model it, estimate it, protect
it, cool it, and account for its life - does not.

**Next:** the final check.
""",
        ),
    ),
)


BATTERY_COURSES: tuple[SeedCourse, ...] = (
    _BATTERY_BASICS,
    _BATTERY_INTERMEDIATE,
    _BATTERY_ADVANCED,
)

__all__ = ["BATTERY_COURSES"]
