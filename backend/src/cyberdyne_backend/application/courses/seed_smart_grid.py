"""Smart Grid, HVDC & Power Quality track: Basics -> Intermediate -> Advanced.

From the modern grid vision and power-quality fundamentals (sags, swells,
harmonics, reactive power) through mitigation, FACTS, distributed generation and
microgrids, up to HVDC transmission, wide-area monitoring and renewable
integration. Lessons are `text` with LaTeX, interactive ```plot blocks (sag/swell
and harmonic-distorted waveforms, daily load curves) and ```mermaid diagrams
(smart-grid architecture, HVDC links, FACTS/STATCOM, PMU/WAMS).
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, Δ, °, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Smart Grid, HVDC & Power Quality — Basics ────────────────────────────────

_SG_BASICS = SeedCourse(
    slug="smart-grid-basics",
    title="Smart Grid, HVDC & Power Quality — Basics",
    description=(
        "How electricity gets from generation through transmission and "
        "distribution to your loads, and what 'good' power actually means: "
        "voltage sags and swells, harmonics and total harmonic distortion, "
        "reactive power and power-factor correction, smart metering, demand "
        "response and grid codes. Interactive waveform and load-curve plots plus "
        "a smart-grid architecture diagram."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The power grid today & the smart-grid vision",
            "10 min",
            """\
# The power grid today & the smart-grid vision

Electricity flows through a chain: **generation → transmission → distribution →
loads**.

- **Generation** — power plants and renewables produce bulk energy, stepped up to
  high voltage by transformers.
- **Transmission** — high-voltage (hundreds of kV) lines move power long distances
  with low loss (loss $\\propto I^2R$, so high voltage means low current).
- **Distribution** — substations step voltage down (e.g. to 11 kV then 400/230 V)
  and feed neighbourhoods.
- **Loads** — homes, factories and EV chargers consume it.

```mermaid
flowchart LR
  GEN["generation"] --> SU["step-up xfmr"] --> TX["transmission (HV)"]
  TX --> SUB["substation"] --> DIST["distribution"]
  DIST --> LOAD["loads"]
  PV["rooftop solar / DER"] --> DIST
  LOAD -. "two-way data + power" .-> DIST
```

The **smart grid** adds a digital layer on top of this: sensors, two-way
communication, smart meters and control. Power and information now flow *both
ways* — rooftop solar feeds back, meters report by the second, and the grid
self-heals around faults. The old grid was one-directional and dumb; the smart
grid is observable and controllable.

**Next:** what "good quality" power actually means.
""",
        ),
        _t(
            "Power-quality fundamentals: sags, swells & interruptions",
            "11 min",
            """\
# Power-quality fundamentals: sags, swells & interruptions

Ideal mains is a clean sinusoid at constant amplitude and frequency. **Power
quality** measures how far reality departs from that ideal. The most common
disturbances are *voltage variations*:

- **Sag (dip)** — a short drop to 10–90% of nominal (e.g. a large motor starting,
  or a fault elsewhere). Most common and most disruptive.
- **Swell** — a short rise above 110% (e.g. a big load switching off, or a fault
  on another phase).
- **Interruption** — voltage falls below 10% (effectively off) for a moment to
  minutes.

Magnitude and **duration** together classify each event (the IEC / IEEE 1159
view). Below, the blue curve is a healthy waveform and the red curve a sag —
notice the reduced amplitude over part of the cycle:

```plot
{"title": "Voltage sag: reduced amplitude vs the healthy waveform", "xLabel": "time (rad)", "yLabel": "voltage (pu)", "xRange": [0, 12.6], "yRange": [-1.3, 1.3], "grid": true, "functions": [{"expr": "sin(x)", "label": "nominal (1.0 pu)", "color": "#2563eb"}, {"expr": "0.6*sin(x)", "label": "sag (0.6 pu)", "color": "#dc2626"}]}
```

Sensitive equipment (drives, servers, PLCs) trips on even brief sags, so power
quality is a money problem, not just a tidiness one.

**Next:** a subtler distortion — harmonics.
""",
        ),
        _t(
            "Harmonics & total harmonic distortion",
            "11 min",
            """\
# Harmonics & total harmonic distortion

Non-linear loads — rectifiers, variable-speed drives, LED drivers, switch-mode
supplies — draw current in pulses, not smooth sinusoids. By Fourier's theorem any
periodic distortion is a sum of a **fundamental** (50/60 Hz) plus **harmonics** at
integer multiples (150 Hz, 250 Hz, …). The odd harmonics (3rd, 5th, 7th) dominate.

A waveform with a strong 3rd and 5th harmonic is visibly "flat-topped" — slide
your eye along the red curve and compare it to the clean fundamental:

```plot
{"title": "Harmonic distortion: fundamental + 3rd + 5th vs pure sine", "xLabel": "time (rad)", "yLabel": "current (pu)", "xRange": [0, 12.6], "yRange": [-1.6, 1.6], "grid": true, "functions": [{"expr": "sin(x)", "label": "fundamental", "color": "#2563eb"}, {"expr": "sin(x)+0.3*sin(3*x)+0.2*sin(5*x)", "label": "distorted (3rd+5th)", "color": "#dc2626"}]}
```

We quantify this with **total harmonic distortion**:

$$\\mathrm{THD} = \\frac{\\sqrt{\\sum_{h\\ge 2} V_h^2}}{V_1},$$

the RMS of all harmonics over the fundamental. Standards (IEEE 519) cap voltage
THD around **5%** at the point of common coupling. Harmonics overheat
transformers and neutral conductors, trip breakers and corrupt metering.

**Next:** reactive power and power factor.
""",
        ),
        _t(
            "Reactive power & power-factor correction",
            "11 min",
            """\
# Reactive power & power-factor correction

AC loads draw two kinds of power:

- **Real power** $P$ (watts) — does actual work (heat, torque, light).
- **Reactive power** $Q$ (var) — sloshes back and forth charging magnetic fields
  in motors and transformers. It does no work but still loads the wires.

They combine into **apparent power** $S = \\sqrt{P^2+Q^2}$ (VA). The **power
factor** is

$$\\text{pf} = \\cos\\phi = \\frac{P}{S}.$$

```mermaid
flowchart LR
  P["real power P (W)"] --> S["apparent power S (VA)"]
  P --> Q["reactive power Q (var)"]
  Q --> S
```

A low power factor (say 0.7, common for lightly loaded motors) means you draw far
more current than the work requires, wasting capacity and incurring utility
penalties. **Correction** adds capacitor banks (or a STATCOM) to supply $Q$
locally, pushing pf toward 1. With $P$ fixed at 8 kW, watch how much reactive
power you must cancel as pf drops:

```plot
{"title": "Reactive power Q vs power factor (P fixed at 8 kW)", "xLabel": "power factor (cos phi)", "yLabel": "reactive power Q (kvar)", "xRange": [0.5, 1], "yRange": [0, 14], "grid": true, "functions": [{"expr": "8*tan(acos(x))", "label": "Q = P tan(phi)", "color": "#2563eb"}]}
```

**Next:** how smart meters turn this into actionable data.
""",
        ),
        _t(
            "Smart metering & demand response",
            "10 min",
            """\
# Smart metering & demand response

A **smart meter** replaces the spinning-disc meter with a digital device that
records consumption at fine intervals (every 15–30 min) and reports it over a
communications network — the backbone of **Advanced Metering Infrastructure
(AMI)**. It enables time-of-use pricing, outage detection and remote
connect/disconnect.

That fine data exposes the daily **load curve** — demand peaks in the morning and
again in the evening, with a midday solar-driven dip in many regions:

```plot
{"title": "Daily load curve: morning and evening peaks", "xLabel": "hour of day", "yLabel": "demand (GW)", "xRange": [0, 24], "yRange": [0, 12], "grid": true, "functions": [{"expr": "6 + 3*exp(-(x-8)^2/4) + 4*exp(-(x-19)^2/6) - 1.5*exp(-(x-14)^2/6)", "label": "system demand", "color": "#2563eb"}]}
```

**Demand response** flattens that curve: utilities signal customers (via price or
direct control) to shift or shed load at peak — pre-cooling buildings, delaying EV
charging, dimming non-critical loads. Shaving the evening peak avoids firing up
expensive, dirty "peaker" plants and defers grid upgrades.

**Next:** the rules that keep all this interconnected.
""",
        ),
        _t(
            "Grid codes & interconnection basics",
            "10 min",
            """\
# Grid codes & interconnection basics

A **grid code** is the rulebook every connected device — generator, wind farm,
solar inverter, large load — must obey so the shared grid stays stable. It is a
contract for behaviour, not just a wiring standard.

Typical requirements:

- **Voltage and frequency ranges** — stay connected while voltage and frequency
  stay within a band (e.g. 49.5–50.5 Hz), and trip outside it.
- **Ride-through** — during a fault, generators must *not* disconnect
  instantly (**fault ride-through / LVRT**); a mass disconnect would collapse the
  grid.
- **Reactive-power support** — sources must supply or absorb $Q$ on demand to help
  regulate voltage.
- **Power quality limits** — harmonic injection and flicker caps (IEEE 519,
  IEC 61000).

**Interconnection** is the process of getting approved to connect: a study checks
your fault contribution, voltage impact and protection coordination. For rooftop
solar this is governed by standards such as **IEEE 1547**, which now *requires*
smart inverters to ride through disturbances and provide grid support rather than
simply tripping off.

Grid codes are why a million rooftop inverters can coexist without destabilising
the system — they all play by the same rules.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Smart Grid, HVDC & Power Quality — Intermediate ──────────────────────────

_SG_INTERMEDIATE = SeedCourse(
    slug="smart-grid-intermediate",
    title="Smart Grid, HVDC & Power Quality — Intermediate",
    description=(
        "Engineering the modern distribution grid: harmonic sources and "
        "passive/active filters, voltage regulation, flicker and unbalance, FACTS "
        "devices (SVC, STATCOM, UPFC), distributed generation and microgrids, "
        "grid-scale storage, and the SCADA/AMI/communications stack. With "
        "interactive plots and a STATCOM diagram."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Harmonic sources & mitigation",
            "11 min",
            """\
# Harmonic sources & mitigation

Harmonics come from **non-linear loads** that draw non-sinusoidal current. The
classic culprits and their signature harmonics:

- **6-pulse rectifiers / VFDs** → 5th, 7th, 11th, 13th (orders $6k\\pm 1$).
- **Single-phase switch-mode supplies / LED drivers** → strong **3rd** harmonic,
  which adds up in the neutral of a three-phase system.
- **Arc furnaces, welders** → broadband, time-varying harmonics.

Distorted current flowing through line impedance distorts the voltage everyone
shares. Mitigation:

- **Passive filters** — an LC branch tuned to short-circuit one harmonic (e.g. a
  5th-harmonic trap). Cheap, but tuned to a single frequency and can resonate with
  the grid.
- **Active power filters (APF)** — measure the distorted current and *inject the
  opposite* harmonic current in real time, cancelling it. Flexible, handles many
  orders, but costs more.
- **Phase-shifting transformers / 12-pulse** — cancel low-order harmonics at the
  source.

A distorted current and the active filter's injected cancellation signal are
mirror images — add them and the result is clean:

```plot
{"title": "Active filter injects the inverse harmonic to cancel distortion", "xLabel": "time (rad)", "yLabel": "current (pu)", "xRange": [0, 12.6], "yRange": [-1, 1], "grid": true, "functions": [{"expr": "0.3*sin(3*x)+0.2*sin(5*x)", "label": "harmonic content", "color": "#dc2626"}, {"expr": "-(0.3*sin(3*x)+0.2*sin(5*x))", "label": "filter injection", "color": "#16a34a"}]}
```

**Next:** the slower voltage problems — regulation, flicker and unbalance.
""",
        ),
        _t(
            "Voltage regulation, flicker & unbalance",
            "11 min",
            """\
# Voltage regulation, flicker & unbalance

Beyond fast events, three steady-state voltage problems matter:

- **Regulation** — keeping voltage within a band (e.g. ±5% of nominal) along a
  feeder as load varies. Voltage **drops with distance and load**
  ($\\Delta V \\approx IR + IX$). Tools: on-load tap-changers, line voltage
  regulators, switched capacitor banks, and increasingly inverter $Q$ support.
- **Flicker** — rapid, repetitive voltage fluctuations (from arc furnaces, wind
  gusts, large cyclic loads) that make lamps visibly shimmer. Quantified by the
  short-term flicker index $P_{st}$; the human eye is most sensitive around
  8.8 Hz.
- **Unbalance** — the three phases carrying unequal voltage/current, usually from
  uneven single-phase loading. The **voltage unbalance factor** is the
  negative-sequence over positive-sequence magnitude; even 2% badly overheats
  three-phase motors.

Voltage falling along a loaded feeder, before and after a mid-feeder regulator
boosts it back up:

```plot
{"title": "Feeder voltage profile: drop with distance, then regulator boost", "xLabel": "distance along feeder (km)", "yLabel": "voltage (pu)", "xRange": [0, 10], "yRange": [0.9, 1.05], "grid": true, "functions": [{"expr": "1 - 0.012*x", "label": "uncorrected", "color": "#dc2626"}, {"expr": "1 - 0.012*x + 0.05*(1/(1+exp(-4*(x-5))))", "label": "with regulator at 5 km", "color": "#2563eb"}]}
```

**Next:** the power-electronic devices that fix these at the speed of light.
""",
        ),
        _t(
            "FACTS devices: SVC, STATCOM & UPFC",
            "12 min",
            """\
# FACTS devices: SVC, STATCOM & UPFC

**FACTS** (Flexible AC Transmission Systems) are power-electronic controllers that
regulate voltage, reactive power and power flow far faster than mechanical
switches. The main shunt and series families:

- **SVC** (Static Var Compensator) — thyristor-switched capacitors and
  thyristor-controlled reactors that vary $Q$ in steps/ramps. The first
  generation; output sags as voltage sags.
- **STATCOM** (Static Synchronous Compensator) — a voltage-source converter (VSC)
  that *synthesises* a controllable AC voltage behind a reactor. It sources or
  sinks reactive current almost instantly and, crucially, **maintains current
  even at low voltage** (better than SVC during faults).
- **UPFC** (Unified Power Flow Controller) — a shunt + series converter pair that
  controls voltage, *and* the real and reactive power flow on a line
  simultaneously. The most capable (and complex) FACTS device.

A STATCOM exchanges only reactive power by setting its converter voltage relative
to the grid:

```mermaid
flowchart LR
  GRID["AC grid bus"] --- RX["coupling reactor X"]
  RX --- VSC["voltage-source converter (STATCOM)"]
  VSC --- DC["DC capacitor"]
  VSC -. "Vconv > Vgrid -> supply Q" .-> GRID
  VSC -. "Vconv < Vgrid -> absorb Q" .-> GRID
```

If the converter voltage exceeds the bus voltage it **supplies** vars (raising
voltage); if lower, it **absorbs** them. STATCOMs are the workhorse for fast
voltage support at wind farms and weak grid points.

**Next:** generation moving to the edge — distributed generation and microgrids.
""",
        ),
        _t(
            "Distributed generation & microgrids",
            "11 min",
            """\
# Distributed generation & microgrids

**Distributed generation (DG)** means many small sources connected near the load —
rooftop solar, small wind, fuel cells, diesel/gas gensets, batteries. It cuts
transmission loss and adds resilience, but it also reverses power flow on feeders
designed for one-way flow, complicating voltage regulation and protection.

A **microgrid** groups local generation, storage and loads behind a single point
of common coupling, with a controller that can run **grid-connected** *or*
disconnect and run **islanded**:

- **Grid-connected** — the main grid sets voltage and frequency; the microgrid
  imports/exports as needed.
- **Islanded** — when the grid fails, the microgrid **seamlessly disconnects** and
  its own sources hold voltage and frequency (a battery inverter usually
  "forms the grid").

The hard part is the transition (intentional islanding and resynchronisation) and
keeping frequency stable with little inertia. Microgrids power campuses,
hospitals and remote communities, and during a wider outage they "**island**" to
keep critical loads alive.

The duck-curve effect of midday solar on a feeder — net demand the grid must
serve dips at noon and ramps hard in the evening:

```plot
{"title": "Net load with rooftop solar: the midday 'duck' dip", "xLabel": "hour of day", "yLabel": "net demand (GW)", "xRange": [0, 24], "yRange": [0, 12], "grid": true, "functions": [{"expr": "6 + 3*exp(-(x-8)^2/4) + 4*exp(-(x-19)^2/6)", "label": "gross demand", "color": "#94a3b8"}, {"expr": "6 + 3*exp(-(x-8)^2/4) + 4*exp(-(x-19)^2/6) - 5*exp(-(x-13)^2/8)", "label": "net of solar", "color": "#2563eb"}]}
```

**Next:** the storage that fills those dips and ramps.
""",
        ),
        _t(
            "Grid-scale energy storage",
            "10 min",
            """\
# Grid-scale energy storage

Storage decouples *when* energy is generated from *when* it is used — essential as
variable renewables grow. The main technologies and their niches:

- **Pumped hydro** — water pumped uphill, released through turbines. ~80%
  round-trip efficiency, GWh scale, the dominant bulk store, but geography-limited.
- **Lithium-ion batteries** — fast (millisecond) response, ~90% efficiency, modular.
  Now the default for grid frequency regulation and 1–4 h shifting.
- **Flow batteries** — decouple power (stack) from energy (tanks); good for long
  duration.
- **Flywheels / supercapacitors** — very fast, high cycle life, seconds–minutes,
  for frequency support and ride-through.

Storage provides stacked services: **energy arbitrage** (charge cheap/midday solar,
discharge at the evening peak), **frequency regulation**, **ramp smoothing** for
wind/solar, and **black-start**. A battery's value is in how many of these it can
stack.

The key metrics are **power** (MW — how fast) versus **energy** (MWh — how long),
and **round-trip efficiency**. A 100 MW / 400 MWh battery delivers 100 MW for
4 hours — sizing it is a load-curve problem.

**Next:** the nervous system tying it together — SCADA, AMI and communications.
""",
        ),
        _t(
            "SCADA, AMI & grid communications",
            "11 min",
            """\
# SCADA, AMI & grid communications

The smart grid runs on data. Two layers carry it:

- **SCADA** (Supervisory Control and Data Acquisition) — the operations backbone.
  **RTUs** and **IEDs** in substations gather measurements and breaker status; a
  central **master** displays them and sends control commands. Protocols:
  **DNP3**, **Modbus**, and the substation standard **IEC 61850**.
- **AMI** (Advanced Metering Infrastructure) — the meter-to-utility network. Smart
  meters report usage and outages over **RF mesh**, cellular or power-line carrier
  to a head-end system, then to billing and analytics.

Latency requirements differ sharply: protection messages need **milliseconds**,
SCADA telemetry **seconds**, AMI reads **minutes to hours**. Designing the comms
network means matching each to the right medium.

Because these networks now reach control equipment, **cybersecurity** is
first-class: segmentation, encryption, and standards such as **IEC 62351** and
**NERC CIP**. A compromised SCADA link is no longer a data breach — it is a
controllable grid.

```mermaid
flowchart TB
  IED["substation IEDs / RTUs"] -->|"DNP3 / IEC 61850"| SCADA["SCADA master / control centre"]
  METER["smart meters"] -->|"RF mesh / cellular"| HEADEND["AMI head-end"]
  HEADEND --> MDM["meter data mgmt / billing"]
  SCADA --> OPS["operators + EMS / DMS"]
  MDM --> OPS
```

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Smart Grid, HVDC & Power Quality — Advanced ──────────────────────────────

_SG_ADVANCED = SeedCourse(
    slug="smart-grid-advanced",
    title="Smart Grid, HVDC & Power Quality — Advanced",
    description=(
        "Bulk power-electronic transmission and grid intelligence: HVDC (LCC vs "
        "VSC) and multi-terminal DC grids, HVDC control, wide-area monitoring with "
        "PMUs and synchrophasors, renewable integration and grid inertia, "
        "demand-side management, markets and DERMS, and a full smart-grid / "
        "power-quality case study. With HVDC and WAMS diagrams and interactive "
        "plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "HVDC transmission: LCC vs VSC",
            "12 min",
            """\
# HVDC transmission: LCC vs VSC

For very long distances, submarine cables, or linking two **asynchronous** grids,
**HVDC** beats AC: no reactive charging current on cables, no synchronism
requirement, lower loss, and full control of power flow. The chain is **rectifier
→ DC line → inverter**.

```mermaid
flowchart LR
  ACA["AC grid A"] --> RECT["rectifier (AC->DC)"]
  RECT --> DCL["DC line / cable"]
  DCL --> INV["inverter (DC->AC)"]
  INV --> ACB["AC grid B"]
```

Two converter technologies:

- **LCC** (Line-Commutated Converter) — thyristor valves, commutated by the AC
  grid voltage. Highest power and voltage (multi-GW, ±800 kV "UHVDC"), very
  efficient, but it **consumes reactive power** (~50–60% of rating, needing big
  filter/cap banks), **cannot start into a dead grid**, and reverses power only by
  reversing voltage polarity.
- **VSC** (Voltage-Source Converter, e.g. **MMC**) — IGBT valves switching
  independently of the grid. It **independently controls real and reactive power**,
  can **black-start** and feed passive/weak grids, reverses power by reversing
  current (so it suits **multi-terminal** DC grids), and has a smaller footprint —
  at slightly higher loss and (historically) lower max rating.

Rule of thumb: **LCC for bulk point-to-point**, **VSC for offshore wind,
city-infeed, and DC grids**.

**Next:** how an HVDC link is actually controlled.
""",
        ),
        _t(
            "HVDC control & multi-terminal grids",
            "12 min",
            """\
# HVDC control & multi-terminal grids

An HVDC link is a *controlled* device — power does not just flow, it is commanded.
In a classic two-terminal LCC scheme:

- The **rectifier** holds **constant current** (controlling its firing angle $\\alpha$).
- The **inverter** holds **constant voltage** (or constant extinction angle
  $\\gamma$ to avoid commutation failure).
- Their characteristics cross at the **operating point**; sliding the rectifier
  current order moves the transmitted power.

For VSC links, one terminal regulates **DC voltage** (the "slack" that balances the
DC node) while others set their **power** — exactly like a generator-vs-load split.

This generalises to a **multi-terminal DC (MTDC) grid**: three or more VSC stations
on a shared DC network, the embryo of a future **DC supergrid** linking offshore
wind farms and onshore grids. The control challenge is sharing the
voltage-regulation duty — solved with **DC voltage droop**, where every terminal
adjusts power in proportion to DC-voltage deviation (no single point of failure):

```plot
{"title": "DC voltage droop: terminals share balancing duty", "xLabel": "terminal power P (pu)", "yLabel": "DC voltage (pu)", "xRange": [-1, 1], "yRange": [0.95, 1.05], "grid": true, "functions": [{"expr": "1 - 0.04*x", "label": "stiff droop (terminal 1)", "color": "#2563eb"}, {"expr": "1 - 0.02*x", "label": "soft droop (terminal 2)", "color": "#dc2626"}]}
```

A flatter droop means a terminal takes more of any imbalance. Losing one terminal,
the others automatically pick up the slack.

**Next:** seeing the whole grid at once — wide-area monitoring.
""",
        ),
        _t(
            "Wide-area monitoring: PMUs, synchrophasors & WAMS",
            "12 min",
            """\
# Wide-area monitoring: PMUs, synchrophasors & WAMS

Traditional SCADA samples voltage *magnitudes* every few seconds and across the
grid those samples are not time-aligned — you cannot compare *angles*. A
**Phasor Measurement Unit (PMU)** fixes this: it measures voltage and current
**phasors** (magnitude *and* phase angle) up to 30–120 times a second, each stamped
with a **GPS time reference** accurate to a microsecond.

GPS-synchronised phasors from across the grid — **synchrophasors** — are
comparable directly. The **phase-angle difference** between two buses reveals how
stressed the line between them is, and growing angle separation is an early warning
of instability.

```mermaid
flowchart TB
  GPS["GPS clock (1 µs)"] --> PMU1["PMU bus 1"]
  GPS --> PMU2["PMU bus 2"]
  GPS --> PMU3["PMU bus 3"]
  PMU1 -->|"C37.118 stream"| PDC["phasor data concentrator"]
  PMU2 --> PDC
  PMU3 --> PDC
  PDC --> WAMS["WAMS / wide-area control + visualisation"]
```

A **Phasor Data Concentrator (PDC)** aligns the streams by timestamp and feeds a
**Wide-Area Monitoring System (WAMS)**. WAMS enables oscillation detection, angle
monitoring and even **wide-area control** — and post-mortems of blackouts (the 2003
US Northeast event drove PMU adoption). The data protocol is **IEEE C37.118**.

**Next:** the stability problem these tools watch — renewable integration.
""",
        ),
        _t(
            "Renewable integration & grid stability",
            "12 min",
            """\
# Renewable integration & grid stability

A conventional grid is stabilised by the **inertia** of large spinning generators:
their rotating mass resists frequency change, buying seconds for controls to react.
The **swing equation** says the rate of frequency change after a loss of generation
is

$$\\frac{df}{dt} = \\frac{f_0}{2H}\\,\\Delta P,$$

where $H$ is the system inertia constant. Wind and solar connect through
**inverters** and contribute **no natural inertia**, so as their share grows, $H$
falls and frequency dives faster after a disturbance — a steeper, more dangerous
**RoCoF** (rate of change of frequency).

Lower inertia means a faster, deeper frequency drop for the same generation loss —
compare a high-$H$ and low-$H$ system after a trip at $t=0$:

```plot
{"title": "Frequency dip after a generation trip: high vs low inertia", "xLabel": "time after trip (s)", "yLabel": "frequency (Hz)", "xRange": [0, 12], "yRange": [49, 50.2], "grid": true, "functions": [{"expr": "50 - 0.4*exp(-0.3*x)*(1-exp(-1.5*x))*3", "label": "high inertia", "color": "#2563eb"}, {"expr": "50 - 0.8*exp(-0.3*x)*(1-exp(-2.5*x))*3", "label": "low inertia", "color": "#dc2626"}]}
```

The fixes: **synthetic / virtual inertia** and **fast frequency response** from
batteries and grid-forming inverters, **synchronous condensers** (spinning mass
with no fuel), and **grid-forming control** that sets voltage and frequency rather
than chasing them. Maintaining stability with high renewables is the defining
challenge of the modern grid.

**Next:** managing demand and the markets that price all this.
""",
        ),
        _t(
            "Demand-side management, markets & DERMS",
            "11 min",
            """\
# Demand-side management, markets & DERMS

The cheapest "power plant" is the load you avoid. **Demand-side management (DSM)**
shapes consumption rather than supply:

- **Demand response** — shifting or shedding load on a price or control signal.
- **Energy efficiency** — permanently lowering demand.
- **Dynamic pricing** — time-of-use and real-time tariffs that nudge behaviour.

These plug into **electricity markets**. Generators (and increasingly storage and
aggregated demand) bid into a **day-ahead** and **real-time** market; the
**marginal** unit sets the clearing price, so prices spike when demand approaches
supply. A battery or a flexible factory can **arbitrage** that spread — and an
**aggregator** can bundle thousands of homes' flexibility into a market bid (a
**virtual power plant**).

Orchestrating millions of distributed resources needs a **DERMS** (Distributed
Energy Resource Management System): it forecasts, dispatches and constrains DERs so
their combined behaviour respects feeder limits while maximising value. Where a
DERMS faces the wholesale market, it becomes the engine of a **VPP**.

The point: with cheap sensing, communication and storage, **demand becomes a
controllable, tradeable resource** — the grid's flexibility increasingly comes from
the edge, not just the centre.

**Next:** put it all together in a case study.
""",
        ),
        _t(
            "Case study: a smart-grid / power-quality deployment",
            "12 min",
            """\
# Case study: a smart-grid / power-quality deployment

A mid-size utility feeds an **industrial park** (many variable-speed drives) plus a
growing cluster of **rooftop solar** down a long rural feeder. Three problems
appear at once:

1. **Harmonics** — the drives push voltage THD past the IEEE 519 5% limit at the
   point of common coupling, overheating a transformer.
2. **Voltage rise & sags** — midday solar pushes feeder voltage *above* limits; a
   motor start at the factory causes sags that trip a sensitive line.
3. **Evening ramp** — when solar fades, demand ramps hard and the feeder voltage
   sags at the far end.

The integrated fix:

- An **active power filter** at the industrial park cancels the 5th/7th harmonics,
  pulling THD back under 5%.
- A **STATCOM** provides fast $Q$ — absorbing vars at midday (taming the solar
  voltage rise) and supplying them during motor starts and the evening ramp.
- A **battery + DERMS** charges on midday solar and discharges into the evening
  peak, flattening the net load curve and deferring a feeder upgrade.
- **Smart inverters** (IEEE 1547) on the solar provide volt-var support and ride
  through disturbances instead of tripping.
- **PMUs and AMI** confirm the result: THD, voltage profile and the flattened load
  curve are all now in spec.

The net load curve before and after the battery + DSM intervention — the evening
peak is shaved and the midday excess absorbed:

```plot
{"title": "Net load before vs after storage + demand-side management", "xLabel": "hour of day", "yLabel": "net demand (GW)", "xRange": [0, 24], "yRange": [0, 12], "grid": true, "functions": [{"expr": "6 + 3*exp(-(x-8)^2/4) + 4*exp(-(x-19)^2/6) - 5*exp(-(x-13)^2/8)", "label": "before (raw net load)", "color": "#dc2626"}, {"expr": "6.5 + 1.5*exp(-(x-8)^2/4) + 2*exp(-(x-19)^2/6) - 1.5*exp(-(x-13)^2/8)", "label": "after (storage + DSM)", "color": "#2563eb"}]}
```

The lesson: **no single device fixes a modern feeder** — power quality, hosting
capacity and economics are solved together with filters, FACTS, storage, smart
inverters and data.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


SMART_GRID_COURSES: tuple[SeedCourse, ...] = (_SG_BASICS, _SG_INTERMEDIATE, _SG_ADVANCED)

__all__ = ["SMART_GRID_COURSES"]
