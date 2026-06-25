"""Renewable Energy & EV Powertrains track: Basics -> Intermediate -> Advanced.

From the energy transition, solar PV and wind fundamentals through PV/wind
system design and the EV powertrain (battery -> inverter -> motor), up to
grid-forming inverters, microgrids, V2G and a renewable + EV integration case
study. Lessons are `text` with LaTeX, interactive ```plot blocks (PV I-V/P-V
curves, wind power curve, battery discharge/SoC, motor efficiency) and
```mermaid block diagrams (PV system, EV powertrain, charging, V2G).
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, η, °, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Renewable Energy & EV Powertrains — Basics ───────────────────────────────

_RE_BASICS = SeedCourse(
    slug="renewable-ev-basics",
    title="Renewable Energy & EV Powertrains — Basics",
    description=(
        "The energy transition from the ground up: solar PV and wind "
        "fundamentals (I-V/P-V curves, power curve, Betz limit), energy storage, "
        "grid connection via inverters, and capacity factor & LCOE intuition. "
        "The foundation for renewables and electric vehicles, with interactive "
        "plots and system diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The energy transition & renewable overview",
            "10 min",
            """\
# The energy transition & renewable overview

The **energy transition** is the shift from burning fossil fuels to harvesting
energy from flows that never run out — sunlight, wind, water and heat. It is
driven by two forces: **decarbonisation** (cutting CO₂ to limit climate change)
and **economics** (solar and wind are now the cheapest new electricity in most
of the world).

**The renewable family**
- **Solar PV** — converts light straight to electricity, no moving parts.
- **Wind** — a turbine turns moving air into rotational then electrical energy.
- **Hydro** — falling water spins a turbine; dispatchable and storable.
- **Geothermal / biomass** — heat-driven, run around the clock.

Two features set renewables apart from a coal plant:

- They are **variable** — the sun sets, the wind drops. Output follows weather,
  not demand.
- They are **inverter-based** — PV and modern wind feed the grid through power
  electronics, not a heavy spinning generator.

Those two facts shape everything in this track: we need **storage** to move
energy in time, **inverters** to shape it, and **smart loads** (like EVs) to
soak up surplus. Electrifying transport with renewable electricity is the single
biggest lever for cutting emissions — which is why renewables and EVs belong in
the same course.

**Next:** how a solar cell actually makes electricity.
""",
        ),
        _t(
            "Solar PV fundamentals: the I-V & P-V curves",
            "12 min",
            """\
# Solar PV fundamentals: the I-V & P-V curves

A **photovoltaic (PV) cell** is a semiconductor diode: photons knock electrons
loose, and the junction sweeps them into a current. A cell makes about $0.6$ V;
wire many in series into a **module**, modules into **strings**, strings into an
**array**.

**The I-V curve.** A PV module is characterised by how its current $I$ varies
with terminal voltage $V$. At a short circuit it delivers the **short-circuit
current** $I_{sc}$; at open circuit, zero current at the **open-circuit voltage**
$V_{oc}$. Between them the current is roughly flat then collapses near $V_{oc}$:

```plot
{"title": "PV module I-V curve (current vs voltage)", "xLabel": "voltage V (V)", "yLabel": "current I (A)", "xRange": [0, 40], "yRange": [0, 9], "functions": [{"expr": "8 - 8*exp((x-37)/3)", "label": "I(V)", "color": "#2563eb"}], "points": [{"x": 0, "y": 8, "label": "I_sc (short circuit)", "color": "#16a34a", "size": 6}, {"x": 37, "y": 0, "label": "V_oc (open circuit)", "color": "#dc2626", "size": 6}, {"x": 30, "y": 7.1, "label": "MPP", "color": "#f59e0b", "size": 7}]}
```

**The P-V curve.** Power is $P = V \\times I$. It is zero at both ends (no voltage,
or no current) and peaks in between at the **maximum power point (MPP)**:

```plot
{"title": "PV module P-V curve — the maximum power point", "xLabel": "voltage V (V)", "yLabel": "power P (W)", "xRange": [0, 40], "yRange": [0, 250], "functions": [{"expr": "x*(8 - 8*exp((x-37)/3))", "label": "P(V) = V·I(V)", "color": "#7c3aed"}], "points": [{"x": 30, "y": 213, "label": "MPP (P_max ≈ 213 W)", "color": "#f59e0b", "size": 7}]}
```

The MPP voltage $V_{mp}$ and current $I_{mp}$ give the rated power; the ratio
$P_{mp}/(V_{oc} I_{sc})$ is the **fill factor**. Both curves shift with sunlight
and temperature, so operating *exactly* at the MPP needs active tracking —
**MPPT**, the subject of the Intermediate course.

**Next:** the wind side of the picture.
""",
        ),
        _t(
            "Wind energy fundamentals: power curve & Betz limit",
            "11 min",
            """\
# Wind energy fundamentals: power curve & Betz limit

The kinetic power in wind passing through a rotor of swept area $A$ at wind speed
$v$ is

$$P_{wind} = \\tfrac12\\,\\rho\\,A\\,v^3.$$

The **cubic** dependence on $v$ is the whole story: double the wind, get **eight
times** the power. That is why turbine siting obsesses over wind speed.

**The Betz limit.** No turbine can capture all of it — slowing the air too much
would block the flow. **Betz's law** caps the fraction any rotor can extract at

$$C_{p,\\max} = \\tfrac{16}{27} \\approx 0.593.$$

Real turbines reach a power coefficient $C_p$ of about $0.45$–$0.50$.

**The power curve.** A turbine's real output vs wind speed has four regions:
below **cut-in** ($\\approx$ 3 m/s) it makes nothing; then output rises steeply
(the cubic law); at **rated** speed it flattens to the generator's limit; above
**cut-out** ($\\approx$ 25 m/s) it shuts down to protect itself.

```plot
{"title": "Wind turbine power curve (output vs wind speed)", "xLabel": "wind speed v (m/s)", "yLabel": "power output (kW)", "xRange": [0, 30], "yRange": [0, 2200], "functions": [{"expr": "2000/(1 + exp(-(x-8)*0.8)) - 2000/(1+exp(8*0.8))", "label": "P(v)", "color": "#0891b2"}], "points": [{"x": 3, "y": 0, "label": "cut-in", "color": "#16a34a", "size": 6}, {"x": 12, "y": 1960, "label": "rated", "color": "#f59e0b", "size": 6}, {"x": 25, "y": 2000, "label": "cut-out", "color": "#dc2626", "size": 6}]}
```

So a turbine spends much of its life **rated-limited** (flat top) or idle (calm
or storm). The next lesson explains why that variability forces us to store
energy.

**Next:** storing renewable energy.
""",
        ),
        _t(
            "Energy storage for renewables",
            "11 min",
            """\
# Energy storage for renewables

Because sun and wind are variable, we need to **move energy in time** — store the
midday solar surplus for the evening peak. The dominant technology is the
**lithium-ion battery**.

**The vocabulary**
- **Capacity** — energy a pack holds, in **kilowatt-hours (kWh)**. A home pack is
  $\\sim$10 kWh; an EV pack 40–100 kWh.
- **Power** — how fast it charges/discharges, in **kilowatts (kW)**.
- **C-rate** — power relative to capacity. A **1C** rate empties a pack in 1 hour;
  **2C** in half an hour; **0.5C** in two hours. So $\\text{power} = C\\text{-rate}
  \\times \\text{capacity}$.
- **State of charge (SoC)** — fraction of capacity remaining, 0–100%.

**Discharge behaviour.** As you draw energy, SoC falls roughly linearly with time
at a constant load, while terminal **voltage** sags — gently across the middle,
then steeply near empty. Below is SoC over time at a 0.5C discharge (full in
2 hours):

```plot
{"title": "Battery state of charge during a 0.5C discharge", "xLabel": "time (hours)", "yLabel": "state of charge (%)", "xRange": [0, 2], "yRange": [0, 100], "functions": [{"expr": "100 - 50*x", "label": "SoC(t) at 0.5C", "color": "#16a34a"}], "points": [{"x": 0, "y": 100, "label": "full", "color": "#2563eb", "size": 6}, {"x": 2, "y": 0, "label": "empty (2 h)", "color": "#dc2626", "size": 6}]}
```

Two more numbers matter: **round-trip efficiency** ($\\sim$90% — you lose ~10% in
and out) and **cycle life** (how many charge/discharge cycles before the pack
fades). Both are central to the EV and storage economics later in the track.

**Next:** how stored DC energy actually reaches the AC grid.
""",
        ),
        _t(
            "Grid connection of renewables: inverters",
            "11 min",
            """\
# Grid connection of renewables: inverters

PV panels and batteries produce **direct current (DC)**; the grid and most loads
run on **alternating current (AC)**. The bridge is the **inverter** — a power-
electronics box that synthesises a clean AC sine wave from DC.

How it works in one line: fast semiconductor switches (**IGBTs** or **MOSFETs**)
chop the DC and a filter smooths the result into a sinusoid at grid frequency
(50/60 Hz), matched in **voltage, frequency and phase** to the grid.

A grid-tied PV system is a short chain:

```mermaid
flowchart LR
    A[PV array<br/>DC] --> B[DC combiner /<br/>MPPT input]
    B --> C[Inverter<br/>DC to AC + MPPT]
    C --> D[AC filter +<br/>protection]
    D --> E[Meter]
    E --> F[Grid / loads]
    B -.optional.-> G[Battery<br/>storage]
    G -.-> C
```

A grid-tied inverter does three jobs at once:
- **MPPT** — continuously hunts the panel's maximum power point (last lesson's
  P-V peak) as sun and temperature change.
- **Synchronisation** — locks its output to the grid's voltage and phase.
- **Protection** — **anti-islanding**: if the grid goes down it must disconnect,
  so it never back-feeds a line a worker thinks is dead.

This is what "inverter-based generation" means — and why grid stability now
depends on software and switches, not just spinning mass. We will revisit that
tension (grid-forming vs grid-following) in the Advanced course.

**Next:** how we measure and price all this energy.
""",
        ),
        _t(
            "Capacity factor & LCOE intuition",
            "10 min",
            """\
# Capacity factor & LCOE intuition

Two numbers let you compare any power source on a level field.

**Capacity factor (CF).** A plant rarely runs flat out. The capacity factor is

$$\\mathrm{CF} = \\frac{\\text{energy actually produced}}{\\text{rated power} \\times \\text{hours}}.$$

A 100 kW solar array that yields the energy of 20 kW running continuously has a
CF of 20%. Typical values: rooftop solar 15–25%, onshore wind 30–45%, offshore
wind 45–55%, nuclear 90%+. Low CF is not "bad" — it is just *why* a 1 kW solar
panel and a 1 kW gas turbine are not the same asset.

**Levelised cost of electricity (LCOE).** The lifetime cost of a plant divided by
the lifetime energy it makes — the price per kWh that breaks even:

$$\\mathrm{LCOE} = \\frac{\\text{total lifetime cost (build + run)}}{\\text{total lifetime energy}}.$$

Renewables have **high upfront cost, near-zero fuel cost**; fossil plants are the
reverse. Because the denominator scales with the capacity factor, LCOE falls as
CF rises — siting a wind farm where it is windy matters as much as the turbine
price. The plot shows LCOE dropping as a fixed-cost asset earns over more energy
(higher CF):

```plot
{"title": "LCOE falls as the capacity factor rises", "xLabel": "capacity factor (%)", "yLabel": "relative LCOE", "xRange": [10, 60], "yRange": [0, 6], "functions": [{"expr": "60/x", "label": "LCOE ∝ 1 / CF", "color": "#dc2626"}], "points": [{"x": 20, "y": 3, "label": "rooftop solar", "color": "#f59e0b", "size": 6}, {"x": 40, "y": 1.5, "label": "onshore wind", "color": "#0891b2", "size": 6}]}
```

Over the last decade solar and wind LCOE fell ~80–90%, which is the real engine
of the energy transition. With the fundamentals in hand, the Intermediate course
designs real systems.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Renewable Energy & EV Powertrains — Intermediate ─────────────────────────

_RE_INTERMEDIATE = SeedCourse(
    slug="renewable-ev-intermediate",
    title="Renewable Energy & EV Powertrains — Intermediate",
    description=(
        "Designing real systems: PV strings and MPPT, wind generators (DFIG, "
        "PMSG), power converters for grid integration, and the EV powertrain end "
        "to end — battery to inverter to motor, AC/DC charging standards, and the "
        "battery management system. With block diagrams and an interactive "
        "efficiency map."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "PV system design: modules, strings & MPPT",
            "12 min",
            """\
# PV system design: modules, strings & MPPT

Designing a PV system is mostly **matching the array to the inverter's window**.

**Series and parallel.** Cells in **series** add voltage; **strings** in parallel
add current. You size a string so its voltage stays inside the inverter's MPPT
range across temperature — and watch the limits: cold mornings *raise* $V_{oc}$
(panel voltage rises as temperature falls), which can overvoltage an inverter if
the string is too long.

**MPPT algorithms.** From the Basics P-V curve, the maximum power point drifts
with sun and temperature, so the inverter must hunt it continuously. The classic
algorithm is **Perturb & Observe (P&O)**:

1. Nudge the operating voltage by a small step.
2. Measure power. If it rose, keep going the same way; if it fell, reverse.
3. Repeat — the operating point dithers around the MPP.

```plot
{"title": "P&O climbs the P-V curve toward the MPP", "xLabel": "operating voltage (V)", "yLabel": "power (W)", "xRange": [0, 40], "yRange": [0, 250], "functions": [{"expr": "x*(8 - 8*exp((x-37)/3))", "label": "P(V)", "color": "#7c3aed"}], "points": [{"x": 18, "y": 142, "label": "start", "color": "#2563eb", "size": 6}, {"x": 25, "y": 196, "label": "step up", "color": "#0891b2", "size": 6}, {"x": 30, "y": 213, "label": "MPP reached", "color": "#f59e0b", "size": 7}]}
```

**Incremental Conductance** is a smarter variant that compares $dP/dV$ to zero
directly, settling faster and dithering less. Under **partial shading** the P-V
curve grows multiple bumps (local maxima); global MPPT algorithms sweep to avoid
getting stuck on the wrong one.

**Next:** the rotating-machine side — wind generators.
""",
        ),
        _t(
            "Wind turbine systems & generators (DFIG, PMSG)",
            "12 min",
            """\
# Wind turbine systems & generators (DFIG, PMSG)

Wind turbines are nearly always **variable speed** — the rotor must speed up and
slow down to track the wind and stay near the optimal $C_p$. Two generator
architectures dominate.

**DFIG — Doubly-Fed Induction Generator.** The stator connects straight to the
grid; the rotor connects through a **partial** power converter (~30% of rated
power). That small converter is the cost win — but it needs a gearbox and slip
rings, and rides through grid faults poorly.

**PMSG — Permanent-Magnet Synchronous Generator.** Permanent magnets on the
rotor; the **full** output passes through a back-to-back converter. This allows a
**direct-drive** (gearbox-free) design and clean grid behaviour, at the cost of a
larger, pricier converter and rare-earth magnets. It dominates modern offshore
turbines.

```mermaid
flowchart LR
    W[Rotor blades] --> G1[Gearbox]
    G1 --> DFIG[DFIG]
    DFIG -- stator --> GRID[Grid]
    DFIG -- rotor --> PC[Partial converter ~30%]
    PC --> GRID
    W -.direct drive.-> PMSG[PMSG]
    PMSG --> FC[Full converter 100%] --> GRID
```

Both let the turbine decouple rotor speed from grid frequency, so the blades can
sit at the **optimal tip-speed ratio** while the converter delivers fixed-
frequency AC. The trade is classic: **DFIG** = cheaper converter, more mechanics;
**PMSG** = more power electronics, fewer mechanics and better fault ride-through.

**Next:** the power converters that make all this possible.
""",
        ),
        _t(
            "Power converters for renewable integration",
            "11 min",
            """\
# Power converters for renewable integration

Every modern renewable source talks to the grid through **power converters**.
Three building blocks recur:

- **DC-DC converter** (boost/buck) — steps a PV string's variable DC up to a
  fixed DC-bus voltage; this is where MPPT often lives.
- **Inverter (DC-AC)** — synthesises grid-frequency AC from the DC bus.
- **Rectifier (AC-DC)** — runs the other way (e.g. a wind PMSG's variable AC into
  DC), often as the first half of a **back-to-back** converter.

**PWM.** Inverters build a sine wave by **pulse-width modulation**: switching the
DC on and off thousands of times a second, wide pulses near the peak and narrow
ones near the zero-crossing. An **LC filter** averages those pulses into a clean
sinusoid. Higher switching frequency → smaller filter, but more switching loss.

A **back-to-back converter** chains a rectifier and an inverter across a shared
DC link — the universal interface for full-converter wind, battery storage and
EV chargers. It **decouples** the source from the grid: the source side can run
at any voltage/frequency while the grid side stays locked to 50/60 Hz.

A practical concern is **harmonics** — the switching leaves distortion on the AC
that grid codes limit (e.g. total harmonic distortion under a few percent). This
is why converters carry filters and why grid operators care so much about
inverter behaviour. The same converter ideas reappear unchanged inside an EV.

**Next:** the EV powertrain itself.
""",
        ),
        _t(
            "The EV powertrain architecture",
            "12 min",
            """\
# The EV powertrain architecture

An electric vehicle is, electrically, a battery feeding a motor through power
electronics — the same DC-bus-and-inverter pattern as a renewable plant, packaged
for the road. The core chain is **battery → inverter → motor**:

```mermaid
flowchart LR
    BATT[Traction battery<br/>~400/800 V DC] --> BMS[Battery management<br/>system]
    BATT --> INV[Traction inverter<br/>DC to 3-phase AC]
    INV --> MOT[Electric motor<br/>PMSM / induction]
    MOT --> GB[Single-speed<br/>reduction gear] --> WHEEL[Wheels]
    MOT -. regenerative braking .-> INV
    INV -. recovered energy .-> BATT
    DCDC[DC-DC converter] --> AUX[12 V auxiliaries]
    BATT --> DCDC
```

**The pieces**
- **Traction battery** — a high-voltage pack (commonly 400 V, increasingly
  800 V). Higher voltage = lower current for the same power, so thinner cables
  and faster charging.
- **Traction inverter** — converts pack DC into the **3-phase AC** the motor
  needs, and controls torque by shaping current ($d$-$q$ / **field-oriented
  control**). This is the powertrain's brain.
- **Electric motor** — usually a **PMSM** (permanent-magnet synchronous) for
  efficiency, or an induction machine. Flat torque from zero RPM is why EVs
  launch instantly; a single reduction gear replaces the multi-speed gearbox.
- **Regenerative braking** — running the motor as a generator turns braking
  energy back into the battery, the energy arrows reversed.

So the renewable inverter and the EV inverter are the *same machine* doing
opposite jobs — one feeds the grid, one feeds a motor.

**Next:** putting energy back into the pack — charging.
""",
        ),
        _t(
            "EV charging: AC/DC levels & fast charging",
            "11 min",
            """\
# EV charging: AC/DC levels & fast charging

Charging splits on one question: **where does AC become DC?** The battery only
takes DC, so the **rectifier** is either onboard the car or in the charger.

**AC charging (onboard charger).** The wall delivers AC; the car's **onboard
charger (OBC)** rectifies it. Power is limited by the OBC (typically 7–22 kW) —
fine overnight at home or at work.
- **Level 1** — a normal household socket, ~1.4–2 kW (very slow).
- **Level 2** — 240 V / dedicated circuit, ~7–22 kW (the home/workplace default).

**DC fast charging (off-board).** A big roadside charger does the AC→DC
conversion itself and pushes DC straight into the pack, bypassing the OBC.
Power runs 50 kW to 350 kW+, taking a pack from 10→80% in 15–40 minutes.

```mermaid
flowchart LR
    subgraph AC charging
      G1[Grid AC] --> EVSE[Wall box / EVSE]
      EVSE --> OBC[Onboard charger<br/>AC to DC] --> B1[Battery]
    end
    subgraph DC fast charging
      G2[Grid AC] --> DCFC[DC fast charger<br/>AC to DC off-board]
      DCFC --> B2[Battery]
    end
```

**Standards.** **CCS** (Combined Charging System) is dominant in Europe and North
America, **NACS** (Tesla's connector) is spreading in the US, **CHAdeMO** is
legacy/Japan, and **GB/T** is China's. They differ in connector and protocol but
share the AC-vs-DC split above.

**Why charging tapers.** Fast charging is fastest at low SoC; near full, the BMS
*throttles current* to protect the cells — which is why "10→80%" is the quoted
figure, not 0→100%.

**Next:** the system that guards the pack — the BMS.
""",
        ),
        _t(
            "Battery management systems: SoC & SoH",
            "11 min",
            """\
# Battery management systems: SoC & SoH

A traction pack is hundreds of cells in series and parallel, and lithium-ion is
unforgiving — overcharge, over-discharge or overheat a cell and it degrades or
fails. The **battery management system (BMS)** is the guardian.

**What a BMS does**
- **Monitors** every cell's voltage, current and temperature.
- **Protects** — opens contactors on over-voltage, under-voltage, over-current or
  over-temperature.
- **Balances** — cells drift apart; the BMS bleeds or shuttles charge so the pack
  ages evenly (a string is only as good as its weakest cell).
- **Estimates** the two key states below.

**State of Charge (SoC).** "How full is it?" — 0–100%. Hard to read directly,
because terminal voltage sags under load. The BMS fuses a **coulomb count**
(integrating current in/out) with a **voltage model** to stay accurate.

**State of Health (SoH).** "How much capacity is left vs new?" Cells fade with
cycles, calendar age and heat, so a pack rated 60 kWh new might hold 54 kWh at
90% SoH. This curve drives warranty, range estimates and resale value:

```plot
{"title": "Battery State of Health fades with cycles", "xLabel": "charge cycles", "yLabel": "state of health (%)", "xRange": [0, 2000], "yRange": [60, 100], "functions": [{"expr": "100 - 0.012*x", "label": "SoH(cycles)", "color": "#dc2626"}], "points": [{"x": 0, "y": 100, "label": "new", "color": "#16a34a", "size": 6}, {"x": 1500, "y": 82, "label": "end of warranty (~80%)", "color": "#f59e0b", "size": 6}]}
```

Accurate SoC stops a driver being stranded; accurate SoH sets the car's residual
value. The Advanced course pushes further into keeping the pack cool and using it
to support the grid.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Renewable Energy & EV Powertrains — Advanced ─────────────────────────────

_RE_ADVANCED = SeedCourse(
    slug="renewable-ev-advanced",
    title="Renewable Energy & EV Powertrains — Advanced",
    description=(
        "The system-integration frontier: grid-forming vs grid-following "
        "inverters, microgrid sizing and dispatch, vehicle-to-grid and smart "
        "charging, traction-motor efficiency maps, thermal management of "
        "batteries and drives, and a full renewable + EV integration case study. "
        "With an interactive efficiency-map slice and V2G block diagram."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Grid-forming vs grid-following inverters",
            "12 min",
            """\
# Grid-forming vs grid-following inverters

As inverter-based generation displaces spinning generators, *who sets the grid's
voltage and frequency?* This is the defining question of a high-renewable grid.

**Grid-following (GFL).** The classic PV/wind inverter. It uses a **phase-locked
loop (PLL)** to *measure* the grid's voltage and frequency, then injects current
in sync. It is a good **citizen** but a **follower** — it needs an existing,
stable grid to lock onto. Fill a grid with only GFL inverters and there is
nothing left to define the reference: the grid cannot start or stand on its own.

**Grid-forming (GFM).** A GFM inverter behaves like a **voltage source**: it sets
its own voltage magnitude and frequency and *holds* them, letting other devices
follow it. It can **black-start** a dead grid and provide **synthetic inertia** —
mimicking the stabilising mass of a spinning generator in software.

| | Grid-following | Grid-forming |
|---|---|---|
| Role | current source, follows | voltage source, leads |
| Needs a live grid? | yes (PLL lock) | no (can black-start) |
| Provides inertia? | no | yes (synthetic) |
| Typical use today | most PV/wind | batteries, microgrids, islands |

**Why it matters now.** Less spinning mass means **lower inertia** — frequency
swings faster after a disturbance. GFM inverters (usually on batteries) backfill
that inertia, which is why grid codes increasingly *require* grid-forming
capability. A microgrid that must run islanded needs at least one GFM source.

**Next:** building those islanded systems — microgrids.
""",
        ),
        _t(
            "Hybrid systems & microgrids: sizing & dispatch",
            "12 min",
            """\
# Hybrid systems & microgrids: sizing & dispatch

A **microgrid** is a local cluster of generation, storage and loads that can run
**grid-connected** or **islanded**. A **hybrid system** combines complementary
sources — e.g. solar + wind + battery + a backup generator — so their weaknesses
cancel.

**Sizing** is an optimisation: pick PV, wind and battery capacities to meet load
at minimum lifetime cost (LCOE from the Basics course) subject to a reliability
target — the **loss-of-load probability**, how often you are allowed to fall
short. Oversize and you waste capital on curtailed energy; undersize and you run
the diesel backup too often.

**Dispatch** is the minute-to-minute control: given current generation, load and
SoC, decide what charges, discharges or curtails. A simple **rule-based**
strategy:

1. Serve load directly from renewables first.
2. **Surplus** → charge the battery (then curtail if full).
3. **Deficit** → discharge the battery; if empty, start the backup generator.

```plot
{"title": "Microgrid dispatch: solar vs load over a day (battery fills the gap)", "xLabel": "hour of day", "yLabel": "power (kW)", "xRange": [0, 24], "yRange": [0, 12], "functions": [{"expr": "9*exp(-((x-13)^2)/14)", "label": "solar generation", "color": "#f59e0b"}, {"expr": "5 + 2*sin((x-8)/24*2*pi)", "label": "load demand", "color": "#2563eb"}]}
```

Where the orange solar curve sits **above** the blue load, the surplus charges
the battery; where it sits **below** (mornings, evenings), the battery covers the
gap. Smarter dispatch uses forecasts and optimisation (e.g. model-predictive
control) to plan the battery's day ahead. **EVs are mobile batteries** in this
picture — which is the next lesson.

**Next:** turning parked EVs into grid assets.
""",
        ),
        _t(
            "Vehicle-to-grid (V2G) & smart charging",
            "12 min",
            """\
# Vehicle-to-grid (V2G) & smart charging

A car is parked ~95% of the time, and an EV pack (40–100 kWh) dwarfs a home
battery. **Smart charging** and **V2G** turn that idle fleet into grid
infrastructure.

- **Smart charging (V1G)** — *modulate* charging power and timing. Charge when
  electricity is cheap/green (overnight, midday solar), pause during peaks. One-
  directional, but already hugely valuable.
- **Vehicle-to-grid (V2G)** — *bidirectional*: the car can also **discharge** to
  the home (V2H), building (V2B) or grid (V2G), acting as distributed storage and
  selling energy or grid services back.

V2G needs a **bidirectional** charger and an inverter that can both rectify (in)
and invert (out), coordinated with an aggregator and the BMS:

```mermaid
flowchart LR
    GRID[Grid] <--> CHG[Bidirectional charger<br/>AC to DC]
    CHG <--> BATT[EV battery]
    BMS[BMS limits & SoC floor] --- BATT
    AGG[Aggregator / utility signal] --> CHG
    PV[Home solar] --> CHG
    HOME[Home loads V2H] <--> CHG
```

**The economics.** A fleet of EVs can provide **frequency regulation** and **peak
shaving** — fast, valuable grid services. The car earns money parked.

**The catch.** Every discharge cycle adds wear (recall SoH), so V2G control must
respect a **SoC floor** (always leave enough to drive) and **cycle budget**, and
the value of grid services must outweigh battery degradation. Done right, EVs
become the cheapest storage on the grid — the literal link between this course's
two halves.

**Next:** squeezing the most from the traction motor.
""",
        ),
        _t(
            "EV traction motor & drive optimisation",
            "12 min",
            """\
# EV traction motor & drive optimisation

An EV motor does not run at one operating point — it spans a 2-D map of **torque
vs speed**, and its **efficiency** changes across that map. The traction
inverter's job is to operate the motor where it wastes the least energy.

**Two regions.** Below **base speed** the motor delivers **constant torque** (the
flat launch feel), limited by current. Above it, the inverter runs out of voltage
headroom and enters **field weakening** — trading torque for speed at **constant
power**.

**The efficiency map.** Plotted over torque and speed, efficiency forms islands:
a broad high-efficiency plateau (often 95%+ for a PMSM) with losses rising at low
load (fixed losses dominate), very high torque (copper / $I^2R$ losses) and very
high speed (iron and switching losses). Here is a **slice at fixed torque** —
efficiency vs speed:

```plot
{"title": "Motor efficiency vs speed (slice of the efficiency map)", "xLabel": "motor speed (% of max)", "yLabel": "efficiency (%)", "xRange": [5, 100], "yRange": [60, 100], "functions": [{"expr": "97 - 600/x - 0.0015*x^2", "label": "η(speed) at mid torque", "color": "#16a34a"}], "points": [{"x": 45, "y": 93.4, "label": "peak-efficiency island", "color": "#f59e0b", "size": 7}, {"x": 10, "y": 36, "label": "low-load losses dominate", "color": "#dc2626", "size": 6}]}
```

**Optimising the drive.** **Field-oriented control** sets the current angle for
**maximum torque per amp (MTPA)** below base speed and minimum loss in field
weakening. Gear ratio, motor type and inverter switching strategy are all chosen
to keep the *common* driving points (cruising, gentle acceleration) inside that
high-efficiency island — directly extending range. Losses that escape as heat
lead straight into the next topic.

**Next:** keeping batteries and drives cool.
""",
        ),
        _t(
            "Thermal management of batteries & drives",
            "11 min",
            """\
# Thermal management of batteries & drives

Every percent of inefficiency becomes **heat**, and both cells and power
electronics have narrow happy temperature bands. Thermal management is what makes
performance, fast charging and long life possible at once.

**Why batteries care.** Lithium-ion likes ~15–35 °C. Too hot accelerates ageing
and risks **thermal runaway** (a self-feeding overheating chain); too cold cuts
power and forbids fast charging (lithium plating). Fast charging itself dumps a
lot of heat, so it depends on good cooling.

**Cooling methods**, roughly in order of capability:
- **Air cooling** — simple, cheap; struggles under fast charge or hard driving.
- **Liquid cooling** — a glycol loop through cold plates between cells; the modern
  default for performance EVs.
- **Immersion / refrigerant** — emerging for the highest power densities.

**Power electronics** (inverter, OBC) run hotter limits (~125–150 °C junction)
but produce intense, concentrated heat; they usually share a liquid loop with
their own cold plates.

**The system view.** A modern EV runs an integrated **thermal loop** — a heat
pump and valves that move heat between cabin, battery and drive. It can **pre-
condition** the pack (warm it before a winter fast-charge, cool it before a
summer one) to hit full charging power safely. Good thermal design is *why* one
EV fast-charges in 18 minutes and another throttles to a crawl — the same cells,
different cooling.

**Next:** put it all together in a design case study.
""",
        ),
        _t(
            "Case study: renewable + EV integration design",
            "12 min",
            """\
# Case study: renewable + EV integration design

A workplace wants to power its building and an **EV-charging car park** mostly
from on-site solar, staying resilient to grid outages. This ties every lesson
together.

**1. The load.** Building base load plus a fleet of EVs charging during the day —
a large, *flexible* load (the smart-charging lesson) that we can shift in time.

**2. Generation & storage (sizing).** Solar carport canopies provide energy;
because solar peaks midday but cars arrive in waves, we add a **stationary
battery** and treat parked EVs as extra **V2G** storage. We size PV + battery to
a target loss-of-load probability at minimum LCOE — the microgrid sizing problem.

**3. The power architecture.** PV arrays → MPPT/DC-DC → a shared **DC bus**; a
**grid-forming** battery inverter sets the reference so the site can **island**
through an outage; bidirectional EV chargers hang off the same bus.

```mermaid
flowchart LR
    PV[Solar carport<br/>PV array] --> DCB[DC bus]
    BATT[Stationary battery] <--> DCB
    DCB <--> GFM[Grid-forming<br/>inverter]
    GFM <--> GRID[Utility grid]
    DCB <--> EVC[Bidirectional<br/>EV chargers V2G]
    EVC <--> EV[EV fleet]
    GFM --> BLDG[Building loads]
    EMS[Energy mgmt system<br/>forecast + dispatch] -.controls.-> DCB
    EMS -.smart charging.-> EVC
```

**4. Control (dispatch).** An **energy management system** forecasts solar and
arrivals, then each interval: serve the building from solar first, **smart-charge**
cars with the surplus, charge the stationary battery, and curtail or export only
when full. On an outage it **islands** on the grid-forming inverter and can pull
**V2G** energy from plugged-in cars — respecting each pack's SoC floor and cycle
budget (V2G + SoH).

**5. The result.** High solar self-consumption, lower peak demand charges,
backup ride-through, and EVs that arrive charged on clean energy. This is the
energy transition in miniature — generation, storage, power electronics and
electrified transport as **one coordinated system**.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


RENEWABLE_EV_COURSES: tuple[SeedCourse, ...] = (_RE_BASICS, _RE_INTERMEDIATE, _RE_ADVANCED)

__all__ = ["RENEWABLE_EV_COURSES"]
