"""High-Voltage Engineering track: Basics -> Intermediate -> Advanced.

Why power is moved at high voltage, the physics of electric stress and
breakdown in gases, liquids and solids, then the generation, measurement and
testing of high voltages, insulation coordination and overvoltage protection,
and finally modern HV practice: partial-discharge diagnostics, gas-insulated
switchgear and SF6, HVDC, cable/bushing/transformer insulation and condition
monitoring. Lessons are `text` with LaTeX, interactive ```plot blocks and
```mermaid diagrams of test setups and protection schemes.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, Ω, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── High-Voltage Engineering — Basics ────────────────────────────────────────

_HV_BASICS = SeedCourse(
    slug="high-voltage-basics",
    title="High-Voltage Engineering — Basics",
    description=(
        "Why electric power is transmitted at high voltage, the physics of "
        "electric fields and dielectric stress, and how insulation breaks down "
        "in gases (Paschen's law), liquids and solids. Closes with HV in the "
        "real grid and the safety rules — clearances and creepage — that keep "
        "people alive, with interactive plots and one-line diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why high voltage: transmission efficiency",
            "10 min",
            """\
# Why high voltage: transmission efficiency

Moving power across a country means moving it through wires with resistance $R$.
The power lost as heat in those wires is

$$P_{\\text{loss}} = I^2 R.$$

The power *delivered* is $P = VI$, so for a fixed amount of power the current is
$I = P/V$. Substituting:

$$P_{\\text{loss}} = \\left(\\frac{P}{V}\\right)^2 R.$$

The loss falls with the **square** of the transmission voltage. Raise $V$ ten
times and the line loss drops by **one hundred**. That single fact — far more
than any clever conductor — is why the grid steps voltage *up* with transformers
for transmission and back *down* near the load.

```plot
{"title": "Line loss falls as 1/V² (fixed delivered power)", "xLabel": "transmission voltage V (relative)", "yLabel": "relative I²R loss", "xRange": [0.5, 10], "yRange": [0, 4], "functions": [{"expr": "1/x^2", "label": "loss ∝ 1/V²", "color": "#2563eb"}], "points": [{"x": 1, "y": 1, "label": "baseline", "color": "#dc2626", "size": 7}, {"x": 10, "y": 0.01, "label": "×10 V → loss ÷100", "color": "#16a34a", "size": 6}]}
```

The price is **insulation**: higher voltage means stronger electric fields, which
means more material (or distance) keeping conductors apart. High-voltage
engineering is the study of that trade-off — squeezing the most field a dielectric
can hold before it fails.

The whole transport chain hangs together as a one-line diagram:

```mermaid
flowchart LR
  GEN["generator ~20 kV"] --> SU["step-up xfmr"] --> HV["HV line 400 kV"]
  HV --> SD["step-down xfmr"] --> DIST["distribution 11 kV"]
  DIST --> LOAD["load 230 V"]
```

**Next:** the electric field that all this insulation must withstand.
""",
        ),
        _t(
            "Electric fields, stress & insulation",
            "11 min",
            """\
# Electric fields, stress & insulation

Insulation does not fail because of *voltage* — it fails because of **electric
field strength** (also called **dielectric stress**), measured in volts per metre
(or the practical kV/mm). For a uniform field between parallel plates a distance
$d$ apart,

$$E = \\frac{V}{d}.$$

Every dielectric has a **breakdown strength** $E_b$ — the field above which it
stops insulating and conducts. Air is about $3\\,\\text{kV/mm}$, SF$_6$ gas around
$9$, oil and good polymers far higher.

Real geometry is rarely uniform. A sharp point or thin wire concentrates the
field. Around a cylindrical conductor of radius $r$ inside a sheath the field is
$E(x) \\propto 1/x$, so it is **highest right at the conductor surface**:

```plot
{"title": "Field intensifies near a curved conductor (E ∝ 1/x)", "xLabel": "distance from conductor axis (relative)", "yLabel": "field strength E (relative)", "xRange": [0.3, 5], "yRange": [0, 4], "functions": [{"expr": "1/x", "label": "E(x) ∝ 1/x", "color": "#2563eb"}], "points": [{"x": 0.3, "y": 3.33, "label": "max stress at surface", "color": "#dc2626", "size": 7}]}
```

This is why HV hardware avoids sharp edges, uses **corona rings** and **grading**
to smooth the field, and why the *weakest point* of a design is wherever the field
is most concentrated — never the average. The engineer's job is to keep the
**peak** stress safely below $E_b$ everywhere.

**Next:** what actually happens when a gas breaks down.
""",
        ),
        _t(
            "Breakdown in gases & Paschen's law",
            "12 min",
            """\
# Breakdown in gases & Paschen's law

When the field in a gas gets high enough, a free electron accelerates, collides
with a molecule and knocks out **more** electrons — an **electron avalanche**.
When the avalanche becomes self-sustaining (the **Townsend criterion**), the gap
flashes over.

The remarkable result, **Paschen's law**, is that the breakdown voltage of a gap
depends not on the spacing $d$ alone but on the **product** $pd$ (pressure ×
distance):

$$V_b = \\frac{B\\,(pd)}{\\ln\\!\\big(A\\,(pd)\\big) - \\ln\\ln(1+1/\\gamma)}.$$

Plotting $V_b$ against $pd$ gives the famous **Paschen curve** with a **minimum**.
To the right (large $pd$) there are many collisions, so a high field is needed.
To the left (small $pd$) electrons rarely hit anything and can't start an
avalanche, so the voltage rises again. The dip in between is the easiest place to
break down:

```plot
{"title": "Paschen curve: breakdown voltage vs p·d (note the minimum)", "xLabel": "p·d (relative units)", "yLabel": "breakdown voltage V_b (relative)", "xRange": [0.2, 8], "yRange": [0, 6], "functions": [{"expr": "5*x/(1.5 + 2.5*x)*(1 + 1/x)", "label": "Paschen V_b(pd)", "color": "#2563eb"}], "points": [{"x": 1, "y": 2.5, "label": "Paschen minimum", "color": "#dc2626", "size": 7}]}
```

Practical consequences: at the minimum even a few hundred volts can flash a tiny
gap (a hazard in vacuum gaps and aircraft at altitude), and pressurising a gas
(moving right) raises its withstand — exactly what gas-insulated switchgear
exploits.

**Next:** liquids and solids, where breakdown is messier and permanent.
""",
        ),
        _t(
            "Breakdown in liquid & solid dielectrics",
            "11 min",
            """\
# Breakdown in liquid & solid dielectrics

Gases recover after a flashover; **liquids and solids often do not**.

**Liquids** (transformer oil, esters). Pure liquids have very high strength, but
real oil fails earlier through **impurities, moisture and suspended particles**
that line up along the field and bridge the gap, plus **gas bubbles** that
breakdown inside. Keeping oil clean, dry and de-gassed is most of HV oil
engineering; field strength typically rises with hydrostatic pressure and falls
sharply with water content.

**Solids** (polyethylene, epoxy, paper, porcelain). Here breakdown is **permanent
damage**:

- **Intrinsic / electronic** — pure-material limit at very high field.
- **Thermal** — dielectric losses heat the material faster than it can cool, a
  runaway: $E_b$ falls as temperature rises.
- **Electromechanical** — electrostatic pressure crushes a soft polymer.
- **Treeing & erosion** — partial discharges in tiny voids slowly carve
  conducting "electrical trees" over months or years until the insulation punches
  through. This ageing mechanism is why long-term stress matters as much as the
  one-time withstand.

Because solid failure is cumulative and invisible, HV insulation is rated with a
generous **safety margin** and monitored for the early discharges that precede
failure (covered in the Advanced track).

**Next:** how these limits set the voltages of the real grid.
""",
        ),
        _t(
            "High voltage in the power grid",
            "10 min",
            """\
# High voltage in the power grid

The grid is a hierarchy of voltage levels, each chosen to trade line losses
against the cost of insulation, towers and right-of-way. Rough conventions:

- **HV** — about $33$ to $230\\,\\text{kV}$ (sub-transmission and shorter
  transmission).
- **EHV** (extra-high voltage) — $345$, $400$, $500$, $765\\,\\text{kV}$ for bulk
  long-distance transmission.
- **UHV** (ultra-high voltage) — $1000\\,\\text{kV}$ AC and $\\pm 800\\,\\text{kV}$+
  DC, used for very long, very high-power corridors.

Higher levels carry more power per line and lose less, but cost more to insulate
and need wider corridors — so each link in the chain steps the voltage to suit
its job:

```mermaid
flowchart LR
  G["generation 11–25 kV"] --> SU["step-up"]
  SU --> EHV["EHV transmission 400–765 kV"]
  EHV --> S1["transmission substation"]
  S1 --> HV["HV sub-transmission 110–132 kV"]
  HV --> S2["distribution substation"]
  S2 --> MV["MV distribution 11–33 kV"]
  MV --> LV["LV supply 230/400 V"]
```

Above roughly $345\\,\\text{kV}$, **corona** (partial ionisation of air at the
conductor surface) causes audible noise, radio interference and loss, so EHV
lines use **bundled conductors** to lower the surface field. Long links also
increasingly use **HVDC**, which avoids AC's reactive charging current over
distance (Advanced track).

**Next:** keeping all of this away from people.
""",
        ),
        _t(
            "Safety, clearances & creepage",
            "10 min",
            """\
# Safety, clearances & creepage

High voltage is unforgiving, so safety is engineered into geometry and procedure,
not left to luck.

Two distances govern insulation in air:

- **Clearance** — the shortest distance **through air** between two conductors (or
  conductor and earth). It must exceed what the air can hold at the worst-case
  overvoltage, with margin.
- **Creepage** — the shortest distance **along the surface** of a solid insulator.
  Surfaces collect pollution, salt and moisture that let current track along them,
  so creepage must be **longer** than clearance — especially in dirty or coastal
  environments (specified as a **creepage distance** per kV by pollution class).

Operational safety rests on the rule of **isolate, lock-out and earth before you
touch**: a de-energised line still holds dangerous stored charge and can be
re-energised by induction or error, so it is **bonded to earth** before work.
Minimum **approach distances** keep workers outside the flashover zone, and
**arc-flash** energy — not just shock — drives protective clothing.

The hierarchy of protection is simple to state and absolute in practice:

```mermaid
flowchart TB
  ISO["isolate / open the source"] --> LOCK["lock-out, tag-out"]
  LOCK --> TEST["test for dead"]
  TEST --> EARTH["apply earths"]
  EARTH --> WORK["work safely"]
```

Get the clearances, creepage and the dead-test-earth sequence right and high
voltage is routine; skip one and it is fatal.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── High-Voltage Engineering — Intermediate ──────────────────────────────────

_HV_INTERMEDIATE = SeedCourse(
    slug="high-voltage-intermediate",
    title="High-Voltage Engineering — Intermediate",
    description=(
        "How high voltages are generated (AC cascade transformers, DC multipliers, "
        "impulse generators), measured (resistive/capacitive dividers and sphere "
        "gaps) and standardised. Covers the lightning and switching impulse "
        "waveforms, insulation coordination, the overvoltages the grid must "
        "survive, and the surge arresters that protect it — with interactive "
        "waveform plots and generator diagrams."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Generation of high voltages",
            "12 min",
            """\
# Generation of high voltages

Test labs make three kinds of high voltage, each with its own circuit.

**High AC** — a single test transformer is limited by insulation and size, so
high test voltages use a **cascade** of transformers, each stacked on the
insulated tank of the one below so their secondary voltages add:

$$V_{\\text{total}} = V_1 + V_2 + V_3 + \\dots$$

**High DC** — rectify AC and pump it up with a **Cockcroft–Walton voltage
multiplier**: a ladder of diodes and capacitors that, in $n$ stages from a peak
$V_m$, ideally reaches

$$V_{\\text{DC}} \\approx 2 n V_m,$$

with ripple and voltage drop that grow with load and stage count.

**Impulse** — to mimic lightning, a bank of capacitors is **charged in parallel**
to a DC voltage, then **discharged in series** through spark gaps (a **Marx
generator**), multiplying the output and shaping it with resistors into a fast
surge.

```mermaid
flowchart LR
  DC["DC charging supply"] --> C1["cap stage 1"]
  C1 -. "spark gap" .-> C2["cap stage 2"]
  C2 -. "spark gap" .-> C3["cap stage 3"]
  C3 --> RS["wave-shaping R"] --> OUT["impulse output"]
```

Each generator pairs with a way to **measure** what it produced — next.

**Next:** measuring voltages too high to put on a meter.
""",
        ),
        _t(
            "Measurement of high voltages",
            "11 min",
            """\
# Measurement of high voltages

You cannot wire a megavolt straight into an instrument, so HV is measured by
**scaling it down** or by a **calibrated gap**.

**Dividers** tap a known fraction of the voltage:

- A **resistive divider** ($V_{\\text{out}} = V\\,R_2/(R_1+R_2)$) suits DC and
  low-frequency AC, but its stray capacitance distorts fast transients.
- A **capacitive divider** ($V_{\\text{out}} = V\\,C_1/(C_1+C_2)$) handles AC and
  fast impulses well.
- A **mixed / damped capacitive divider** is the standard for impulse work,
  keeping the ratio flat over a wide bandwidth so the measured waveshape is true.

**Sphere gaps** give an *absolute* reference: two metal spheres flash over at a
voltage fixed by their diameter and spacing (tabulated in the standards), so a
sphere gap calibrates everything else without needing a divider's accuracy.

The peak field at the sphere surface rises as the gap shrinks, so breakdown
voltage grows with spacing but **less than linearly** once the gap approaches the
sphere diameter (the field stops being uniform):

```plot
{"title": "Sphere-gap flashover vs spacing (saturates as gap nears sphere size)", "xLabel": "gap spacing (relative to sphere diameter)", "yLabel": "breakdown voltage (relative)", "xRange": [0.05, 2], "yRange": [0, 3], "functions": [{"expr": "3*x/(1 + 0.9*x)", "label": "V_b(spacing)", "color": "#2563eb"}], "points": [{"x": 0.5, "y": 1.03, "label": "near-uniform field", "color": "#16a34a", "size": 6}, {"x": 2, "y": 2.14, "label": "field non-uniform, saturating", "color": "#dc2626", "size": 6}]}
```

A measurement is only as good as its bandwidth: the divider must reproduce the
**waveshape**, not just the peak — which is what the next lesson is about.

**Next:** the standard impulse waveforms.
""",
        ),
        _t(
            "Impulse voltage waveforms",
            "12 min",
            """\
# Impulse voltage waveforms

Lightning and switching surges are reproduced in the lab as **standard impulse
waveforms** — a fast rise to a peak followed by a slow decay to zero. Each is
modelled as a **double-exponential**:

$$v(t) = V_0\\,\\big(e^{-\\alpha t} - e^{-\\beta t}\\big),$$

where the fast term ($\\beta$) sets the **front** (rise) and the slow term
($\\alpha$) sets the **tail** (decay). Two standards dominate:

- **Lightning impulse** $1.2/50\\,\\mu s$ — a $1.2\\,\\mu s$ front to peak, decaying
  to half-value at $50\\,\\mu s$. It tests withstand against direct/induced
  lightning surges.
- **Switching impulse** $250/2500\\,\\mu s$ — a much slower front, used for EHV
  where switching surges, not lightning, set the design.

The double-exponential shape — sharp rise, long tail — looks like this:

```plot
{"title": "Standard impulse waveform: double-exponential (front + tail)", "xLabel": "time (relative µs)", "yLabel": "voltage (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "functions": [{"expr": "1.03*(exp(-0.15*x) - exp(-2.5*x))", "label": "v(t) = V₀(e^(−αt) − e^(−βt))", "color": "#2563eb"}], "points": [{"x": 0.7, "y": 0.78, "label": "≈ peak (front)", "color": "#dc2626", "size": 6}]}
```

The front time and time-to-half-value are fixed by the generator's wave-shaping
resistors and capacitors; defining them as standards lets a transformer tested in
one lab be compared to one tested anywhere — the basis of insulation coordination.

**Next:** coordinating insulation against these surges.
""",
        ),
        _t(
            "Insulation coordination",
            "11 min",
            """\
# Insulation coordination

**Insulation coordination** is choosing equipment withstand levels and protective
devices so that, when an overvoltage hits, **insulation survives and the cheap,
replaceable protector acts first**. The key rated level is the **BIL** (Basic
Insulation Level) — the lightning-impulse voltage the equipment must withstand.

The principle is a **protective margin**: the surge arrester's **protective
level** must sit safely *below* the equipment's withstand, with the difference
absorbing measurement error, ageing and distance effects:

$$\\text{margin} = \\frac{\\text{equipment withstand (BIL)}}{\\text{arrester protective level}} - 1.$$

A clean way to see it is a "staircase": each insulation level must be higher than
the protection guarding it.

```mermaid
flowchart TB
  SURGE["incoming overvoltage"] --> ARR["surge arrester (protective level)"]
  ARR -->|clamps below BIL| TX["transformer (BIL withstand)"]
  ARR -->|coordinated| BUS["busbar / GIS insulation"]
  TX --> SAFE["insulation survives"]
```

Coordination is **statistical**: overvoltage magnitudes and insulation strength
both scatter, so standards express it as an acceptable **risk of failure** rather
than an absolute. Get the margins right and a substation rides out decades of
surges; get them wrong and either the arresters wear out fast or the transformer
fails.

**Next:** where those overvoltages come from.
""",
        ),
        _t(
            "Overvoltages: lightning & switching surges",
            "11 min",
            """\
# Overvoltages: lightning & switching surges

Insulation is sized for the **transient overvoltages** that briefly dwarf the
normal operating voltage. They fall into families by origin and speed:

- **Lightning (atmospheric) overvoltages** — a direct strike or an induced surge
  injects a huge, very fast transient (microsecond front, the $1.2/50$ shape).
  Magnitude is largely independent of system voltage, so they dominate the
  insulation design of **lower-voltage** systems.
- **Switching overvoltages** — opening or closing breakers, energising long
  lines, or clearing faults excites the network's inductance and capacitance into
  oscillation. These scale **with** the system voltage (expressed in per-unit of
  peak), so they **dominate EHV/UHV** design where lightning is comparatively
  modest.
- **Temporary overvoltages** — slower, sustained rises (load rejection, earth
  faults, ferranti rise on long lines) lasting cycles to seconds; they set the
  **continuous** duty of arresters.

A useful mental model is per-unit: switching surges typically peak at a few
**per-unit** of normal voltage, and the whole job of protection is to clip the
fast, tall transients before they reach the slow withstand limit of the
apparatus. Which device does the clipping is next.

**Next:** the arrester that clips the surge.
""",
        ),
        _t(
            "Surge arresters & protection",
            "11 min",
            """\
# Surge arresters & protection

A **surge arrester** is a voltage-dependent shunt that does **nothing** at normal
voltage and conducts **hard** when an overvoltage arrives, clamping it to a safe
level and diverting the surge energy to earth.

Modern arresters use **metal-oxide varistors (MOV)** — sintered zinc-oxide blocks
with an extremely **non-linear** $V$–$I$ characteristic:

$$I \\propto V^{\\alpha}, \\qquad \\alpha \\approx 20\\text{–}50.$$

Below the knee they leak microamps; just above it the current rises by orders of
magnitude for a tiny voltage increase, so the voltage is **clamped** almost flat
even as the surge current soars. That sharp knee is the whole trick:

```plot
{"title": "Metal-oxide arrester V–I: voltage clamps above the knee", "xLabel": "voltage across arrester (relative)", "yLabel": "current through arrester (relative)", "xRange": [0, 1.4], "yRange": [0, 6], "functions": [{"expr": "(x/1.0)^25", "label": "I ∝ V^α (α ≈ 25)", "color": "#2563eb"}], "points": [{"x": 1.0, "y": 1.0, "label": "knee / protective level", "color": "#dc2626", "size": 7}]}
```

Older designs added a **series spark gap** with silicon-carbide blocks; MOV
arresters dropped the gap because the ZnO non-linearity alone is sharp enough.
Selecting an arrester means picking its **MCOV** (max continuous operating
voltage) above the system's sustained voltage yet low enough that its protective
level keeps the coordination margin to the equipment BIL. Position matters too:
arresters work best mounted **close** to the apparatus they protect, since the
surge re-doubles travelling down the connecting lead.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── High-Voltage Engineering — Advanced ──────────────────────────────────────

_HV_ADVANCED = SeedCourse(
    slug="high-voltage-advanced",
    title="High-Voltage Engineering — Advanced",
    description=(
        "Modern HV practice: standardised testing under IEC, partial-discharge "
        "measurement and diagnostics, gas-insulated switchgear and SF6, HVDC "
        "insulation and converter stations, and the insulation of cables, "
        "bushings and transformers. Ends with condition monitoring and a worked "
        "HV test case study, with diagnostic plots and apparatus diagrams."
    ),
    level="Advanced",
    lessons=(
        _t(
            "HV testing techniques & standards",
            "12 min",
            """\
# HV testing techniques & standards

High-voltage testing proves apparatus against its rated stresses using procedures
fixed by **IEC** standards (notably **IEC 60060** for the techniques and **IEC
60071** for insulation coordination), so results are comparable worldwide. The
core test families are:

- **Power-frequency withstand** — apply rated AC for a fixed time (often 1 min);
  the insulation must not flash over.
- **Lightning-impulse (LI)** — apply the standard $1.2/50\\,\\mu s$ wave at the
  rated BIL, both polarities, counting flashovers against an allowed number.
- **Switching-impulse (SI)** — the slow $250/2500\\,\\mu s$ wave for EHV apparatus.
- **DC withstand** — for DC apparatus and cables.

Tests are either **type tests** (prove a design), **routine tests** (every unit
on the production line) or **on-site/commissioning tests**. A representative HV
test bay wires a source, a divider for measurement and the test object together:

```mermaid
flowchart LR
  SRC["HV source (AC / impulse / DC)"] --> CR["coupling / control"]
  CR --> DUT["test object (DUT)"]
  DUT --> DIV["measuring divider"]
  DIV --> MEAS["peak / waveshape recorder"]
  DUT --> PD["PD detector"]
```

Crucially, many tests are **non-destructive withstand** checks: the goal is to
confirm the equipment survives the rated stress, not to find its breakdown limit.
The sensitive diagnostic that reveals *hidden* weakness without destroying the
sample is partial discharge — next.

**Next:** measuring the discharges that precede failure.
""",
        ),
        _t(
            "Partial discharge measurement & diagnostics",
            "12 min",
            """\
# Partial discharge measurement & diagnostics

A **partial discharge (PD)** is a tiny localised breakdown — in a void, at an
electrode edge, along a surface — that **does not** bridge the full insulation but
slowly erodes it. PD is the single best early warning of insulation that is
ageing toward failure.

PD is measured per **IEC 60270** as **apparent charge** $q$ in picocoulombs,
detected as small current pulses through a coupling capacitor. Two numbers
matter: the **inception voltage** (where PD starts as voltage rises) and the
**magnitude** and **rate** of the pulses.

The classic diagnostic plot is **PD magnitude vs applied voltage**: discharges are
absent until the **inception voltage**, then climb steeply — a void that ignites
early and grows fast is the worrying signature:

```plot
{"title": "PD inception: apparent charge climbs once voltage exceeds inception", "xLabel": "applied voltage (relative)", "yLabel": "PD apparent charge q (pC, relative)", "xRange": [0, 2], "yRange": [0, 5], "functions": [{"expr": "4*(x-0.8)*(x-0.8)", "label": "q above inception", "color": "#2563eb"}], "points": [{"x": 0.8, "y": 0, "label": "inception voltage", "color": "#dc2626", "size": 7}]}
```

Beyond magnitude, the **phase-resolved PD (PRPD) pattern** — where in the AC cycle
the pulses fall — fingerprints the *defect type* (internal void, surface
tracking, corona, floating metal). Modern systems also locate PD by pulse arrival
time. PD testing is the backbone of both factory acceptance and in-service
**condition monitoring** (last lesson).

**Next:** gas-insulated switchgear and SF6.
""",
        ),
        _t(
            "Gas-insulated switchgear (GIS) & SF6",
            "12 min",
            """\
# Gas-insulated switchgear (GIS) & SF6

A **gas-insulated switchgear (GIS)** packs busbars, breakers, disconnectors and
instrument transformers into earthed metal enclosures filled with pressurised
**sulphur hexafluoride (SF$_6$)**. Because SF$_6$ holds roughly three times the
field of air *and* its strength rises with pressure (the right branch of the
Paschen curve), a GIS substation is a fraction of the size of an air-insulated
one — decisive indoors, in cities and offshore.

SF$_6$ is also an outstanding **arc-quenching** medium, recombining fast after a
breaker interrupts current. Its drawbacks are serious: it is an extremely potent
**greenhouse gas** (very high GWP), so leakage is tightly regulated, and its
**arc by-products** are toxic, demanding careful handling — driving active
research into alternative gases.

A single-line view of a GIS bay shows the apparatus strung along the gas-filled
enclosure:

```mermaid
flowchart LR
  CABLE["incoming cable / line"] --> DS1["disconnector"]
  DS1 --> CB["SF6 circuit breaker"]
  CB --> ES["earthing switch"]
  ES --> BUS["GIS busbar (SF6 enclosure)"]
  BUS --> CT["current/voltage transformer"]
  CT --> OUT["outgoing feeder"]
```

GIS reliability hinges on cleanliness — a stray metallic particle in the gas
concentrates the field and triggers PD or flashover — so factory and on-site PD
testing (previous lesson) is essential before energising.

**Next:** insulation under DC stress.
""",
        ),
        _t(
            "HVDC insulation & converter stations",
            "12 min",
            """\
# HVDC insulation & converter stations

**HVDC** transmits bulk power as direct current, avoiding AC's reactive charging
current (which makes long lines and especially **submarine cables** impractical
beyond a few tens of km) and allowing power flow between **asynchronous** grids.
A **converter station** at each end rectifies AC to DC and inverts it back, using
**thyristor (LCC)** or modern **voltage-source (VSC / MMC)** converters.

DC stress is physically different from AC and changes insulation design:

- Under AC the field follows the **permittivity** $\\varepsilon$; under DC it
  follows the **conductivity** $\\sigma$, which depends strongly on temperature.
- A loaded cable is **hotter at the conductor**, so its conductivity gradient can
  **invert** the field — pushing the peak stress toward the *outer* screen, the
  opposite of the AC case.
- **Space charge** injected into the dielectric accumulates and distorts the field
  further, and **polarity reversals** (in LCC links) momentarily double the
  stress.

These effects mean HVDC cables use specially formulated polymers and are qualified
with **long-duration DC and polarity-reversal tests**. The converter station is a
dense HV environment of valves, transformers, smoothing reactors, filters and DC
switchyard:

```mermaid
flowchart LR
  AC["AC grid"] --> CT["converter transformer"]
  CT --> VALVE["thyristor / VSC valves"]
  VALVE --> DCF["smoothing reactor + DC filter"]
  DCF --> POLE["DC pole (±kV)"]
  POLE --> LINE["HVDC line / cable"]
```

The valves, transformers and DC bushings all sit at full pole voltage, so
clearances, grading and PD control inside the hall are as demanding as anywhere in
HV engineering.

**Next:** the insulation of the apparatus itself.
""",
        ),
        _t(
            "Cable, bushing & transformer insulation",
            "11 min",
            """\
# Cable, bushing & transformer insulation

Three pieces of apparatus concentrate the hardest HV-insulation problems.

**Cables.** A HV cable is a conductor inside a coaxial dielectric, so the field is
non-uniform ($E \\propto 1/r$, highest at the conductor). Modern cables use
**cross-linked polyethylene (XLPE)** with **semiconducting screens** that smooth
the field at the conductor and insulation boundaries; the chronic enemies are
**water trees**, **voids** and badly made **joints and terminations**, which is
where most failures start.

**Bushings.** A bushing carries a conductor through an earthed barrier (a
transformer tank wall, a GIS enclosure). The challenge is the **radial** field at
the conductor and the **axial** creepage along the surface. **Condenser
(capacitor-graded) bushings** insert concentric conducting foils that force the
voltage to step evenly, grading both stresses at once so neither runs away.

**Transformers.** A HV transformer mixes **oil and pressboard** insulation under
combined electric, thermal and mechanical stress. Design controls the field at
winding ends and leads, manages **moisture** (which slashes oil strength) and
**partial discharges** in oil ducts, and relies on the oil for both insulation and
cooling — the reason oil **dissolved-gas analysis** is a prime diagnostic.

The unifying theme: in every case the engineer **grades the field** (screens,
foils, shaped electrodes) and **keeps the dielectric clean and dry**, because
local stress concentration and contamination — not the bulk material — are what
fail. Monitoring those weaknesses in service is the final lesson.

**Next:** watching insulation age in service.
""",
        ),
        _t(
            "Condition monitoring & a HV test case study",
            "11 min",
            """\
# Condition monitoring & a HV test case study

Insulation fails slowly, so **condition monitoring** watches the leading
indicators and schedules action *before* breakdown rather than after. The main
tools:

- **Dissolved-gas analysis (DGA)** of transformer oil — fault types produce
  characteristic gases (hydrogen, acetylene, ethylene); ratios reveal overheating
  vs arcing vs PD.
- **On-line partial-discharge monitoring** — trends PD magnitude and PRPD pattern
  over time; a steadily rising trend flags a growing defect.
- **Dielectric response** — **tan δ** (dissipation factor) and capacitance track
  bulk ageing and moisture ingress.
- **Thermal and bushing monitoring** — hotspot temperature and bushing tan δ /
  capacitance.

## Worked case study

A $400\\,\\text{kV}$ transformer's on-line PD monitor shows apparent charge
**rising month over month** while routine DGA reports a creeping rise in hydrogen.
Read together, the signals point to an **internal partial discharge** eroding the
insulation — long before any protection would trip.

The diagnostic trend is the whole story: a defect that is stable looks flat; a
defect that is growing rises, and the slope sets the urgency:

```plot
{"title": "Condition monitoring: rising PD trend signals a growing defect", "xLabel": "months in service", "yLabel": "monitored PD level (pC, relative)", "xRange": [0, 12], "yRange": [0, 6], "functions": [{"expr": "0.5*exp(0.2*x)", "label": "growing defect (act)", "color": "#dc2626"}, {"expr": "1.2", "label": "stable baseline (ok)", "color": "#16a34a"}], "points": [{"x": 12, "y": 5.5, "label": "intervene before failure", "color": "#dc2626", "size": 7}]}
```

The decision: take the unit out at the next planned outage, confirm with an
off-line PD and DGA test, and repair — converting an unplanned, catastrophic,
possibly fiery failure into routine maintenance. That is the payoff of everything
in this track: understand the stress, test against it, and monitor what you cannot
see.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


HIGH_VOLTAGE_COURSES: tuple[SeedCourse, ...] = (_HV_BASICS, _HV_INTERMEDIATE, _HV_ADVANCED)

__all__ = ["HIGH_VOLTAGE_COURSES"]
