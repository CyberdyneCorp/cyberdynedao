"""Curated PCB & Hardware Design track: Basics, Intermediate, Advanced.

A complete printed-circuit-board curriculum: schematic capture and the EDA flow
(symbols, footprints, BOMs, gerbers in KiCad/Altium), stackup and materials,
placement/routing and DRC, manufacturing and assembly; then power distribution,
grounding and return paths, signal integrity, high-speed routing and thermal
design; and finally EMC/EMI, advanced signal/power integrity, RF and
mixed-signal layout, and design for manufacturing, test and reliability. Dual
MATLAB + Python focus for the engineering calculations (trace width, impedance,
signal integrity), with runnable Python labs (numpy + matplotlib), interactive
```plot blocks, Mermaid diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- PCB & Hardware Design -- Basics -------------------------------------------

_PCB_BASICS = SeedCourse(
    slug="pcb-basics",
    title="PCB & Hardware Design -- Basics",
    description=(
        "From schematic to finished board: components, symbols, nets and the BOM; "
        "footprints, layers and copper; the EDA flow in KiCad/Altium; stackup and "
        "materials; placement, routing and DRC; gerbers, fab tolerances and THT vs "
        "SMT assembly - with side-by-side MATLAB and Python, interactive plots, "
        "and a runnable IPC-2221 trace-width lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Components, symbols & schematics",
            "11 min",
            """\
# Components, symbols & schematics

A **schematic** is the electrical blueprint of a circuit: it says *what connects
to what*, with zero regard for physical position. Everything that follows -
layout, manufacturing, debugging - traces back to it.

## The vocabulary

| Term | Meaning |
|------|---------|
| **Symbol** | the drawn shape of a part (resistor zig-zag, op-amp triangle) |
| **Reference designator** | the part's label: R1, C3, U2, J4, Q1 |
| **Pin** | a single electrical connection point on a part |
| **Net** | a set of pins that are electrically the same node (a wire) |
| **Net label** | a name (GND, +3V3, SDA) that ties pins together without a drawn line |
| **BOM** | bill of materials - every part, its value, package and part number |

Reference designators follow a convention: **R** resistor, **C** capacitor, **L**
inductor, **D** diode, **Q** transistor, **U** integrated circuit, **J**
connector, **Y** crystal, **SW** switch. A real board's debugging starts by
finding "R47" on the schematic and on the board.

## A net is just a node

A **net** in EDA is exactly a **node** from circuit analysis: every pin on the
same net is the same voltage. You connect pins either by drawing a wire or by
giving them the **same net label** - on a dense schematic, labels keep it
readable.

```mermaid
flowchart LR
  VIN["+3V3 (net)"] --> R1["R1 1k"] --> N(("SENSE (net)"))
  N --> R2["R2 2k"] --> GND["GND (net)"]
  N --> U1["U1 pin 3 (ADC)"]
```

Above, three pins share the **SENSE** net; R1 and R2 form a divider whose midpoint
the ADC reads. The same divider math from any electronics course applies:

$$V_{SENSE} = V_{in}\\,\\frac{R_2}{R_1 + R_2}.$$

Slide $R_1$ and watch where a 3.3 V rail lands on the ADC input as $R_2$ grows:

```plot
{"title": "Sense divider: Vsense = 3.3 * R2/(R1+R2) (slide R1)", "xLabel": "R2 (kohm)", "yLabel": "Vsense (V)", "xRange": [0, 50], "yRange": [0, 3.3], "grid": true, "controls": [{"name": "R1", "range": [1, 50], "value": 10, "label": "R1 (kohm)"}], "functions": [{"expr": "3.3*x/(R1+x)", "label": "Vsense"}]}
```

## The BOM is half the design

Two boards with identical schematics but different part numbers can behave
completely differently (a 16 V vs 6.3 V cap, a 1% vs 5% resistor). The BOM is the
contract with the factory: reference designator, value, package/footprint,
manufacturer part number, and quantity.

```matlab
% A divider's mid-voltage from its two resistors
Vin = 3.3; R1 = 10e3; R2 = 20e3;
Vsense = Vin * R2/(R1+R2);     % 2.2 V
```

```python
Vin, R1, R2 = 3.3, 10e3, 20e3
Vsense = Vin * R2/(R1+R2)      # 2.2 V
```

> **Practical insight:** name your nets meaningfully (+5V, USB_DP, MOTOR_A) - a
> well-labelled schematic is self-documenting, and the net names carry through to
> the layout where you debug.

**Next:** turning that schematic into copper - footprints, layers and the flow.
""",
        ),
        _t(
            "From schematic to PCB: footprints, layers & the EDA flow",
            "12 min",
            """\
# From schematic to PCB: footprints, layers & the EDA flow

The schematic says *what connects*; the **layout** decides *where the copper
goes*. The bridge between them is the **footprint**.

## Symbol vs footprint

Every part has two faces in an EDA tool:

- a **symbol** (schematic) - the electrical shape and pin **functions**;
- a **footprint** (layout) - the physical **copper pads**, drill holes, and
  silkscreen outline that the real part solders to.

A resistor symbol is one zig-zag; its footprint might be an 0402, 0603, or
through-hole package - same electrical part, very different copper. Picking the
wrong footprint is the single most common way to make a board that arrives and
**does not fit the parts**.

```mermaid
flowchart LR
  SCH["schematic (symbols + nets)"] --> NET["netlist"]
  NET --> LAY["layout (footprints)"]
  LAY --> ROUTE["route copper to match netlist"]
  ROUTE --> DRC["design rule check"]
  DRC --> GBR["gerbers + drill + BOM"]
```

The **netlist** is the handoff: an exported list of every net and which footprint
pads sit on it. The layout tool shows unrouted connections as thin lines
("ratsnest") that you replace with real copper traces.

## Layers and copper

A PCB is a sandwich. Even a simple 2-layer board has:

- **Top / bottom copper** - the signal and power traces.
- **Soldermask** - the green (or other colour) coating; it *opens* over pads.
- **Silkscreen** - the white printed text: reference designators, outlines, logos.
- **Drill** - the holes for vias and through-hole pins.

Copper is specified by **weight** in ounces per square foot; 1 oz copper is about
35 microns thick. Thicker copper carries more current for the same width - which
is exactly what the trace-width lab computes.

## The EDA tools in practice

**KiCad** (free, open source) and **Altium Designer** (commercial, industry
standard) share the same flow: capture a schematic, assign footprints, push to
layout, route, run DRC, and export manufacturing files. KiCad is dominant in
education, hobby, and increasingly in industry; Altium dominates large commercial
teams with its library management and high-speed tooling.

```matlab
% Copper cross-section vs current capacity (more area -> more current)
oz = 1; thick_um = 35*oz;          % 1 oz ~ 35 um
width_mm = 0.5;
area_mm2 = thick_um/1000 * width_mm;   % cross-sectional area
```

```python
oz = 1; thick_um = 35*oz           # 1 oz ~ 35 um
width_mm = 0.5
area_mm2 = thick_um/1000 * width_mm    # cross-sectional area
```

> **Practical insight:** assign and **check every footprint against the part's
> datasheet** before routing. A swapped pin order or a 0.1 mm pad-pitch error is
> invisible on screen and fatal on the bench.

**Next:** what the board is actually made of - stackup and materials.
""",
        ),
        _t(
            "PCB stackup & materials",
            "12 min",
            """\
# PCB stackup & materials

The **stackup** is the layer-by-layer recipe of the board: how many copper
layers, how thick each is, and what insulator separates them. It sets impedance,
current capacity, cost, and how easy the board is to route.

## What it is made of

- **FR4** - the default substrate: woven glass-epoxy laminate. Cheap, sturdy,
  good to a few GHz. Its **relative permittivity** is about $\\varepsilon_r
  \\approx 4.3$ (it drifts with frequency), which sets trace impedance.
- **Copper foil** - the conductor, specified by **weight**: 0.5 oz, 1 oz (~35
  um), 2 oz... heavier copper carries more current and spreads more heat.
- **Prepreg & core** - the bonding (prepreg) and rigid (core) glass-epoxy layers
  that build up a multilayer sandwich.
- **High-frequency laminates** (Rogers, PTFE) - lower loss and stable
  $\\varepsilon_r$ for RF/microwave, at higher cost.

## Layer counts and planes

| Layers | Typical use |
|--------|-------------|
| 2 | simple/hobby, low speed |
| 4 | signal / GND / PWR / signal - the workhorse |
| 6-8 | dense or high-speed digital |
| 10+ | servers, RF, HDI phones |

A **plane** is a whole copper layer dedicated to **ground** or **power**. Planes
give a low-impedance supply, a clean current **return path** (Intermediate
course), and shielding. The classic 4-layer stack puts signals on the outside and
a solid GND + PWR pair in the middle.

```mermaid
flowchart TB
  L1["L1 top - signals"] --> L2["L2 - GND plane"]
  L2 --> L3["L3 - PWR plane"]
  L3 --> L4["L4 bottom - signals"]
```

## Trace, space and vias

- **Trace width / space** - the minimum copper width and gap your fab can make.
  Cheap process: 6 mil / 6 mil (about 0.15 mm). HDI: down to ~3 mil.
- **Via** - a plated hole connecting layers. Through-hole vias go all the way;
  **blind** (outer to inner) and **buried** (inner to inner) vias save space on
  dense boards at higher cost.

## Dielectric thickness sets impedance

A trace over a plane is a transmission line whose impedance depends on trace
**width** $w$, **dielectric height** $h$, and $\\varepsilon_r$. As a first feel,
the microstrip impedance **falls** as the trace gets wider relative to the
dielectric - slide the dielectric height $h$:

```plot
{"title": "Microstrip impedance vs trace width (slide dielectric height h)", "xLabel": "trace width w (mm)", "yLabel": "Z0 (ohm)", "xRange": [0.1, 1], "yRange": [0, 120], "grid": true, "controls": [{"name": "h", "range": [0.1, 0.4], "value": 0.2, "label": "dielectric height h (mm)"}], "functions": [{"expr": "87/sqrt(4.3+1.41)*ln(5.98*h/(0.8*x+0.035))", "label": "Z0 (microstrip approx)"}]}
```

```matlab
% Wheeler/IPC microstrip impedance approximation
er = 4.3; h = 0.2; w = 0.3; t = 0.035;     % mm
Z0 = 87/sqrt(er+1.41) * log(5.98*h/(0.8*w + t));
```

```python
import numpy as np
er, h, w, t = 4.3, 0.2, 0.3, 0.035          # mm
Z0 = 87/np.sqrt(er+1.41) * np.log(5.98*h/(0.8*w + t))
```

> **Practical insight:** decide the stackup **before** you route a fast board.
> The fab gives you a stackup table with the exact dielectric heights and
> $\\varepsilon_r$ - feed those into the impedance calculator, not textbook
> defaults.

**Next:** placing parts and routing copper without breaking the rules.
""",
        ),
        _t(
            "Placement & routing basics",
            "12 min",
            """\
# Placement & routing basics

Once footprints land on the board, two crafts decide whether it works:
**placement** (where parts go) and **routing** (how copper connects them).
Placement is 80% of the battle - good placement makes routing almost draw itself.

## Placement: organise before you route

- **Group by function** - keep a power supply, an MCU and its decoupling, a sensor
  front-end as tidy clusters.
- **Connectors and mechanical parts first** - their positions are fixed by the
  enclosure; everything else flexes around them.
- **Decoupling caps hug their chip** - place each bypass capacitor right at the
  IC's power pin (Intermediate course explains why).
- **Respect signal flow** - input on one side, output on the other, so signals
  travel forward, not back and forth.

```mermaid
flowchart LR
  CONN["connectors / power in"] --> PWR["regulator cluster"]
  PWR --> MCU["MCU + decoupling"]
  MCU --> IO["sensor / IO front-end"]
```

## Routing: turning the ratsnest into copper

The **ratsnest** shows every unrouted connection as a thin line. Routing replaces
each with a real **trace**. Good habits:

- **Wide traces for power**, thin for signals (current capacity - the lab).
- **Avoid 90-degree corners**; use 45-degree or curved corners (cleaner etch,
  less reflection at high speed).
- **Keep a continuous return plane** under signals (Intermediate course).
- **Short and direct** for sensitive nets (clocks, resets, analog).

## Design rules and DRC

Your fab can only make traces and gaps down to some minimum, drill holes down to
some diameter, and needs copper kept back from the board edge. You encode these
as **design rules** (clearance, min trace/space, min annular ring, min drill), and
the **DRC** (Design Rule Check) flags every violation. A clean DRC is the
gate before you generate manufacturing files.

| Rule | Typical low-cost value |
|------|------------------------|
| Min trace width | 6 mil (0.15 mm) |
| Min clearance | 6 mil (0.15 mm) |
| Min drill | 0.3 mm |
| Min annular ring | 0.13 mm |
| Edge clearance | 0.5 mm |

A wider trace is cheaper to make reliably (better yield), but takes more room.
The cost-vs-density trade-off is real: as minimum feature size shrinks, the price
of the board rises sharply. Slide the board complexity factor:

```plot
{"title": "Relative fab cost vs minimum feature size (slide complexity)", "xLabel": "min trace/space (mil)", "yLabel": "relative cost", "xRange": [3, 10], "yRange": [0, 6], "grid": true, "controls": [{"name": "k", "range": [10, 60], "value": 30, "label": "complexity factor k"}], "functions": [{"expr": "1 + k/(x^2)", "label": "relative cost"}]}
```

```matlab
% Track clearance check: does a 0.2 mm gap meet a 0.15 mm rule?
gap_mm = 0.2; rule_mm = 0.15;
ok = gap_mm >= rule_mm;        % true -> passes DRC
```

```python
gap_mm, rule_mm = 0.2, 0.15
ok = gap_mm >= rule_mm         # True -> passes DRC
```

> **Practical insight:** set your design rules to the **fab's capability** at the
> start, then route inside them. Tightening rules later means rerouting; loosening
> them earlier means a cheaper, higher-yield board.

**Next:** sending it to be built - gerbers, tolerances and assembly.
""",
        ),
        _t(
            "Manufacturing & assembly: gerbers, fab & soldering",
            "11 min",
            """\
# Manufacturing & assembly: gerbers, fab & soldering

A finished layout is not a board - it is a set of **manufacturing files** that a
factory turns into copper, then into a populated assembly.

## The output package: gerbers and friends

- **Gerber files (RS-274X)** - one file per layer (copper, soldermask,
  silkscreen), describing shapes as 2D apertures. The universal fab language.
- **Excellon drill file** - hole positions and sizes.
- **Pick-and-place / centroid file** - X, Y, rotation of each part for the
  assembly robot.
- **BOM** - what to populate.
- Increasingly, **ODB++** or **IPC-2581** bundle all of this into one
  intelligent file.

```mermaid
flowchart LR
  LAY["layout"] --> GBR["gerbers + drill"]
  LAY --> CPL["pick-and-place"]
  LAY --> BOM["BOM"]
  GBR --> FAB["fab: bare board"]
  CPL --> ASM["assembly: populated board"]
  BOM --> ASM
  FAB --> ASM
```

Always open the gerbers in a **viewer** before ordering - it is the last chance to
catch a missing soldermask opening or a mirrored layer.

## Fab tolerances

Manufacturing is physical, so everything has a **tolerance**: board thickness
(+/- 10%), hole position, copper width (etching eats some copper), soldermask
registration. Design with margin - do not put a 0.15 mm trace right next to the
0.15 mm clearance limit and a 0.15 mm fab tolerance.

## THT vs SMT

| | Through-hole (THT) | Surface-mount (SMT) |
|--|---------------------|---------------------|
| Mounting | leads through drilled holes | pads on the surface |
| Density | low | high (both sides, tiny parts) |
| Assembly | wave/hand solder | solder paste + reflow oven |
| Strength | very mechanically strong | needs care for big/heavy parts |
| Use | connectors, power, prototyping | almost everything modern |

**SMT reflow** is the dominant modern process: a stencil deposits **solder paste**
on the pads, a robot places parts, and the board passes through a **reflow oven**
whose temperature profile melts the paste. The profile matters - too cool and
joints do not form, too hot and parts cook:

```plot
{"title": "SMT reflow temperature profile (preheat, soak, reflow, cool)", "xLabel": "time (s)", "yLabel": "temperature (C)", "xRange": [0, 300], "yRange": [0, 260], "grid": true, "functions": [{"expr": "min(150, 1.3*x)*(x<=120) + (150 + (x-120)*0.3)*(x>120)*(x<=180) + (170 + (x-180)*2.0)*(x>180)*(x<=220) + max(50, 245 - (x-220)*2.5)*(x>220)", "label": "oven profile"}]}
```

The curve climbs through **preheat**, holds in the **soak** (activates flux),
spikes through the **reflow** peak (~245 C for lead-free), then cools.

## Design for manufacture (DFM)

DFM is designing so the factory can actually build it cheaply and reliably:
adequate trace/space, thermal reliefs on pads tied to planes, room between parts
for the pick-and-place head, fiducial marks for the camera, and panelization (many
small boards in one panel) for efficient assembly.

```matlab
% Will a 0.15 mm trace survive a 0.04 mm etch tolerance with a 0.15 mm gap?
trace = 0.15; etch_tol = 0.04; gap = 0.15;
min_final_gap = gap - etch_tol;     % worst-case gap after etching
ok = min_final_gap > 0.1;           % keep margin above the rule
```

```python
trace, etch_tol, gap = 0.15, 0.04, 0.15
min_final_gap = gap - etch_tol      # worst-case gap after etching
ok = min_final_gap > 0.1
```

> **Practical insight:** the cheapest reliability win is **margin** - back off
> from the absolute fab minimums. A board that is 10% looser than the rules yields
> better, assembles faster, and reworks easier.

**Next:** compute trace width from current in a runnable lab.
""",
        ),
        _code(
            "Lab: trace width vs current (IPC-2221)",
            "13 min",
            """\
# Compute the minimum copper trace width to carry a given current, using the
# IPC-2221 design rule, and plot width vs current for several temperature rises.
#
# IPC-2221: I = k * dT^0.44 * A^0.725, where
#   I  = current (A), dT = allowed temperature rise (C),
#   A  = cross-sectional area (mil^2), k = 0.048 (external) or 0.024 (internal).
# Invert for area, then width = area / (thickness in mils).
import numpy as np
import matplotlib.pyplot as plt

k_ext = 0.048                 # external (outer-layer) constant
oz = 1.0                      # copper weight
thickness_mil = 1.378 * oz    # 1 oz copper ~ 1.378 mil thick

I = np.linspace(0.1, 10.0, 200)        # current in amps

plt.figure(figsize=(8, 4.5))
for dT, color in [(10, "#2563eb"), (20, "#16a34a"), (40, "#dc2626")]:
    # A = (I / (k dT^0.44))^(1/0.725)  in mil^2
    area_mil2 = (I / (k_ext * dT**0.44))**(1/0.725)
    width_mil = area_mil2 / thickness_mil
    width_mm = width_mil * 0.0254
    plt.plot(I, width_mm, color=color, label=f"dT = {dT} C rise")

# Worked point: 3 A at 20 C rise on 1 oz outer copper
area_3a = (3.0 / (k_ext * 20**0.44))**(1/0.725)
w_3a_mil = area_3a / thickness_mil
w_3a_mm = w_3a_mil * 0.0254
plt.scatter([3.0], [w_3a_mm], color="#000000", zorder=5)
plt.annotate(f"3 A -> {w_3a_mm:.2f} mm", (3.0, w_3a_mm),
             textcoords="offset points", xytext=(8, 8))

plt.xlabel("current (A)")
plt.ylabel("minimum trace width (mm)")
plt.title("IPC-2221 trace width vs current (1 oz external copper)")
plt.legend(); plt.grid(True); plt.show()

print(f"For 3 A at 20 C rise on 1 oz outer copper:")
print(f"  required area = {area_3a:.1f} mil^2")
print(f"  minimum width = {w_3a_mil:.1f} mil = {w_3a_mm:.2f} mm")

# Try it yourself:
#   1. Set oz = 2.0: thicker copper -> the same current needs a narrower trace.
#   2. Use k = 0.024 for an internal (buried) trace: it needs to be much wider,
#      because buried copper cannot shed heat as easily.
""",
        ),
    ),
)


# -- PCB & Hardware Design -- Intermediate -------------------------------------

_PCB_INTERMEDIATE = SeedCourse(
    slug="pcb-intermediate",
    title="PCB & Hardware Design -- Intermediate: Power, Ground & Signal Integrity",
    description=(
        "Make the board behave: power distribution and decoupling, the PDN and its "
        "impedance; grounding, return paths and the perils of split planes; signal "
        "integrity - traces as transmission lines, controlled impedance, "
        "termination and reflections; high-speed routing (length matching, "
        "differential pairs, crosstalk); and thermal design - with dual "
        "MATLAB/Python, interactive plots, and a runnable microstrip/reflection lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Power distribution & decoupling",
            "12 min",
            """\
# Power distribution & decoupling

A chip does not draw a steady current - it draws **bursts** every clock edge as
millions of transistors switch. The job of the **power distribution network
(PDN)** is to deliver those bursts with the supply voltage barely moving.

## Why a plane is not enough

The supply travels from a regulator through copper to the chip. Every centimetre
of trace has **inductance**, and inductance fights *changes* in current:

$$v = L\\,\\frac{di}{dt}.$$

When the chip suddenly demands current, that $L\\,di/dt$ drops the local voltage -
a **voltage droop** or **ground bounce**. At gigahertz clocks the regulator is far
too slow and too far away to help on the nanosecond timescale.

## Decoupling capacitors: a local energy reservoir

A **decoupling (bypass) capacitor** placed right at the chip's power pin is a
tiny, fast battery: it dumps charge in nanoseconds to cover the burst, then the
slower plane and regulator refill it. The closer the cap, the lower the loop
inductance, the better it works - which is why placement (Basics) matters.

```mermaid
flowchart LR
  REG["regulator (slow, far)"] --> PLANE["power plane"]
  PLANE --> CAP["decoupling cap (fast, local)"]
  CAP --> CHIP["chip (fast bursts)"]
```

## The PDN impedance target

We design the PDN as an **impedance** seen by the chip across frequency, and aim
to keep it below a **target impedance**:

$$Z_{target} = \\frac{\\Delta V_{allowed}}{\\Delta I_{max}}.$$

A real capacitor is not ideal - it has series inductance (**ESL**) and resistance
(**ESR**), so it is a **series RLC** that resonates at

$$f_{res} = \\frac{1}{2\\pi\\sqrt{L_{ESL}\\,C}}.$$

Below resonance it looks capacitive, above it looks inductive - so each cap value
only helps in a band. Slide the capacitance and watch the impedance notch move:

```plot
{"title": "Decoupling cap impedance |Z| vs frequency (slide C)", "xLabel": "frequency (MHz)", "yLabel": "|Z| (ohm)", "xRange": [1, 200], "yRange": [0, 4], "grid": true, "controls": [{"name": "C", "range": [10, 200], "value": 100, "label": "capacitance C (nF)"}], "functions": [{"expr": "sqrt(0.02^2 + (159000/(C*x) - 0.001*x*6.283)^2)", "label": "|Z| of one cap"}]}
```

This is why boards use **many cap values in parallel** (e.g. 100 nF + 1 uF +
10 uF + a bulk electrolytic): each covers a different frequency band, and together
they hold $|Z|$ below target from kHz to hundreds of MHz.

```matlab
dV = 0.05; dI = 5;                 % allow 50 mV droop at 5 A step
Ztarget = dV/dI;                   % 0.01 ohm target impedance
C = 100e-9; ESL = 1e-9;
fres = 1/(2*pi*sqrt(ESL*C));       % cap self-resonant frequency
```

```python
import numpy as np
dV, dI = 0.05, 5                   # 50 mV droop at 5 A step
Ztarget = dV/dI                    # 0.01 ohm
C, ESL = 100e-9, 1e-9
fres = 1/(2*np.pi*np.sqrt(ESL*C))  # self-resonant frequency
```

> **Practical insight:** the **mounting inductance** (the loop from pad through
> via to plane) usually dominates ESL. A small 0402 cap with short, fat vias right
> at the pin beats a big cap 10 mm away.

**Next:** where that current goes back - grounding and return paths.
""",
        ),
        _t(
            "Grounding & return paths",
            "12 min",
            """\
# Grounding & return paths

Beginners think about how current gets **to** a chip; experts think about how it
gets **back**. Every signal current flows in a complete **loop**, and the return
path is half of it.

## Current returns underneath the signal

At DC, return current spreads to take the lowest-**resistance** path. But at high
frequency it takes the lowest-**inductance** path, which is the route that
**minimises loop area** - and that is the copper **directly beneath the signal
trace** on the reference plane. The signal and its return hug each other:

```mermaid
flowchart LR
  DRV["driver"] -->|signal trace| RCV["receiver"]
  RCV -->|"return current (in plane, under the trace)"| DRV
```

A small loop area means low inductance, low emitted radiation, and low
susceptibility to noise. This single idea drives most layout rules.

## Why a solid plane is gold

A continuous ground plane lets the return current flow **right under every trace**,
wherever the trace goes, automatically minimising loop area. That is why a
4-layer board with a solid plane is so much quieter than a 2-layer board with a
scattered ground.

## The trap: gaps and splits

If a slot, a split, or a row of vias **breaks the plane** under a signal, the
return current cannot follow directly - it must detour **around** the gap. That
detour:

- **enlarges the loop area** (more inductance, more EMI),
- creates a **voltage difference** across the gap (noise into other circuits).

Slide the gap width and watch the return-loop area (and thus inductance) climb:

```plot
{"title": "Return loop area vs plane gap the current must detour around (slide trace length)", "xLabel": "gap width (mm)", "yLabel": "extra loop area (mm^2)", "xRange": [0, 10], "yRange": [0, 60], "grid": true, "controls": [{"name": "len", "range": [2, 12], "value": 6, "label": "detour length (mm)"}], "functions": [{"expr": "x*len", "label": "extra loop area"}]}
```

## Split planes and ground loops

- **Split planes** (e.g. analog vs digital ground) can help isolate noise - but
  **never route a signal across the split**, or its return is severed. Join the
  grounds at a single point, ideally under the ADC.
- **Ground loops** - two ground connections at different potentials let current
  circulate, injecting noise (the classic audio "hum"). Prefer a **single-point
  (star) ground** for low-frequency/analog, a **solid plane** for high-frequency.

```matlab
% Loop inductance scales with loop area; keep it tiny
mu0 = 4*pi*1e-7;
area = 6e-3 * 2e-3;                % loop ~ 6 mm x 2 mm (m^2)
L_est = mu0 * area / 1e-3;         % crude estimate, henries
```

```python
import numpy as np
mu0 = 4*np.pi*1e-7
area = 6e-3 * 2e-3                 # loop area (m^2)
L_est = mu0 * area / 1e-3          # crude estimate, H
```

> **Practical insight:** before routing a fast signal, ask "where does its return
> current flow, and is the plane under it continuous the whole way?" Keep a solid
> reference plane and never cut it under high-speed nets.

**Next:** when a trace stops being a wire - transmission lines.
""",
        ),
        _t(
            "Signal integrity intro: transmission lines & reflections",
            "13 min",
            """\
# Signal integrity intro: transmission lines & reflections

At low speed a trace is just a wire. But once the signal's **edge** is fast
compared to the time it takes to travel the trace, the trace behaves like a
**transmission line** - and ignoring that gives ringing, overshoot, and false
edges.

## When does a trace become a transmission line?

Rule of thumb: treat a trace as a transmission line when its length exceeds about
**one tenth of the edge's rise distance**. Signals travel at roughly half the
speed of light on FR4 (about $1.5 \\times 10^8$ m/s, ~6 ps/mm). A 1 ns edge covers
~150 mm, so traces longer than ~15 mm already matter.

## Characteristic impedance

A transmission line has a **characteristic impedance** $Z_0$ set by its geometry
and dielectric - typically **50 ohm** (single-ended) or **100 ohm** differential.
For a microstrip (trace over a plane) a common approximation is

$$Z_0 \\approx \\frac{87}{\\sqrt{\\varepsilon_r + 1.41}}\\,
  \\ln\\!\\left(\\frac{5.98\\,h}{0.8\\,w + t}\\right),$$

with dielectric height $h$, trace width $w$, copper thickness $t$. **Controlled
impedance** means choosing $w$ and $h$ so $Z_0$ hits the target; the fab guarantees
it. Slide the width and watch $Z_0$ cross 50 ohm:

```plot
{"title": "Microstrip Z0 vs trace width, find the 50 ohm width (slide h)", "xLabel": "trace width w (mm)", "yLabel": "Z0 (ohm)", "xRange": [0.1, 0.8], "yRange": [0, 110], "grid": true, "controls": [{"name": "h", "range": [0.1, 0.35], "value": 0.2, "label": "dielectric height h (mm)"}], "functions": [{"expr": "87/sqrt(5.71)*ln(5.98*h/(0.8*x+0.035))", "label": "Z0"}, {"expr": "50", "label": "50 ohm target", "color": "#dc2626"}]}
```

## Reflections and the reflection coefficient

When a signal meets an impedance change (the line end, a connector, a stub), part
of it **reflects**. The fraction is the **reflection coefficient**:

$$\\Gamma = \\frac{Z_L - Z_0}{Z_L + Z_0}.$$

- $Z_L = Z_0$ (matched): $\\Gamma = 0$, no reflection - clean.
- $Z_L = \\infty$ (open): $\\Gamma = +1$, full reflection - overshoot/ringing.
- $Z_L = 0$ (short): $\\Gamma = -1$, inverted reflection.

Reflections bounce back and forth, distorting the waveform. Slide the load
impedance and watch $\\Gamma$ pass through zero at the match:

```plot
{"title": "Reflection coefficient vs load impedance (Z0 = 50)", "xLabel": "load impedance ZL (ohm)", "yLabel": "reflection coefficient", "xRange": [0, 200], "yRange": [-1.1, 1.1], "grid": true, "functions": [{"expr": "(x - 50)/(x + 50)", "label": "Gamma"}, {"expr": "0", "label": "matched", "color": "#16a34a"}]}
```

## Termination: the fix

To kill reflections you **terminate** the line so the load matches $Z_0$:

- **Series termination** - a resistor at the driver ($R_s + Z_{driver} = Z_0$);
  good for point-to-point.
- **Parallel termination** - a resistor at the receiver to ground/Vtt ($= Z_0$);
  good for multi-drop, but burns DC power.

Press Play to launch an edge down the line and watch it travel toward the load
(at the open end it would bounce straight back):

```plot
{"title": "A voltage edge travels down the trace (press Play)", "xLabel": "position along trace", "yLabel": "voltage", "xRange": [0, 10], "yRange": [-0.2, 1.3], "grid": true, "animate": {"param": "t", "range": [0, 10], "label": "time"}, "functions": [{"expr": "(x < t)*1", "label": "wavefront"}], "points": [{"xExpr": "t", "yExpr": "1", "label": "edge", "color": "#dc2626", "size": 6, "trail": true}]}
```

```matlab
Z0 = 50; ZL = 75;
gamma = (ZL - Z0)/(ZL + Z0);       % +0.2 -> 20% reflects
Rseries = Z0 - 20;                 % series term if driver out-Z ~ 20 ohm
```

```python
Z0, ZL = 50, 75
gamma = (ZL - Z0)/(ZL + Z0)        # +0.2
Rseries = Z0 - 20                  # series termination resistor
```

> **Practical insight:** the **edge rate**, not the clock frequency, decides if
> you need to care. A slow 1 MHz clock with a 1 ns edge still rings. Slow your
> edges where you can; terminate where you cannot.

**Next:** routing fast buses - length matching, diff pairs and crosstalk.
""",
        ),
        _t(
            "High-speed routing: length matching, differential pairs & crosstalk",
            "12 min",
            """\
# High-speed routing: length matching, differential pairs & crosstalk

Modern buses (DDR memory, USB, HDMI, PCIe, Ethernet) push edges into the
hundreds of picoseconds. Routing them is about **timing** and **coupling**.

## Length matching: aligning arrivals

In a parallel bus, all bits must arrive **at the same time**. Since signals travel
at ~6 ps/mm, a length difference becomes a **skew** in time:

$$t_{skew} = \\frac{\\Delta\\ell}{v}, \\qquad v \\approx 1.5\\times10^8\\ \\text{m/s}.$$

So a 10 mm mismatch is ~67 ps of skew - enough to break a fast DDR bus. The fix is
**serpentine routing**: deliberately wiggling the short traces to add length until
all match. Slide the mismatch and watch the skew grow:

```plot
{"title": "Timing skew from a length mismatch (slide propagation speed)", "xLabel": "length mismatch (mm)", "yLabel": "skew (ps)", "xRange": [0, 30], "yRange": [0, 220], "grid": true, "controls": [{"name": "v", "range": [120, 200], "value": 150, "label": "speed (mm/ns)"}], "functions": [{"expr": "1000*x/v", "label": "skew (ps)"}]}
```

## Differential pairs: two wires, one signal

Fast interfaces carry a signal as the **difference** of two traces driven
oppositely (+ and -). Benefits:

- **Noise rejection** - noise hits both equally and cancels in the difference.
- **Low emission** - the two opposite currents' fields cancel.
- **Defined impedance** - a controlled **differential impedance** (often 90 or
  100 ohm).

Route diff pairs **tightly coupled, equal length, symmetric**, and keep their
intra-pair skew tiny (length-match *within* the pair as well as between pairs).

```mermaid
flowchart LR
  DRV["differential driver"] -->|"P (+)"| RCV["receiver"]
  DRV -->|"N (-)"| RCV
```

## Vias: not free at high speed

Each via adds a short impedance discontinuity and a **stub** (the unused barrel
past the layer you exit on). On multi-GHz links you **back-drill** stubs away and
minimise via count. Every via on a fast net is a small reflection.

## Crosstalk basics

A switching trace couples into its neighbour through mutual capacitance and
inductance - **crosstalk**. It grows with **coupled length** and shrinks fast with
**spacing**. The common rule is **3W**: keep centre-to-centre spacing at least
three times the trace width. Crosstalk falls steeply with separation:

```plot
{"title": "Relative crosstalk vs trace spacing (slide coupled length)", "xLabel": "edge-to-edge spacing / trace width", "yLabel": "relative crosstalk", "xRange": [0.5, 5], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "Lc", "range": [5, 40], "value": 20, "label": "coupled length (mm)"}], "functions": [{"expr": "(Lc/20)/(1 + (2*x)^2)", "label": "relative crosstalk"}]}
```

```matlab
v = 1.5e8;                         % signal speed on FR4 (m/s)
dl = 10e-3;                        % 10 mm length mismatch
skew = dl/v;                       % ~67 ps
```

```python
v = 1.5e8                          # m/s on FR4
dl = 10e-3                         # 10 mm mismatch
skew = dl/v                        # ~67 ps
```

> **Practical insight:** budget your timing in **picoseconds** and your spacing in
> **trace widths**. Match lengths to the tightest interface's tolerance, keep
> aggressor and victim apart, and minimise vias on the fastest nets.

**Next:** keeping the board cool - thermal design.
""",
        ),
        _t(
            "Thermal design of boards",
            "11 min",
            """\
# Thermal design of boards

Every watt a part dissipates becomes **heat** that must escape, or the part
overheats and fails. On a PCB the copper is both your conductor and your primary
**heatsink**.

## The thermal Ohm's law

Heat flow is exactly analogous to current: temperature difference drives heat
through a **thermal resistance** $\\theta$ (in C/W):

$$\\Delta T = P\\,\\theta_{ja}, \\qquad T_{junction} = T_{ambient} + P\\,\\theta_{ja}.$$

$\\theta_{ja}$ (junction-to-ambient) is the total resistance from the chip's silicon
to the surrounding air. Lower it and the part runs cooler. As dissipated power
rises, junction temperature climbs linearly - and you must stay under the part's
limit (often 125 C or 150 C). Slide the thermal resistance:

```plot
{"title": "Junction temperature vs power (Tamb=25), slide theta_ja", "xLabel": "dissipated power (W)", "yLabel": "junction temperature (C)", "xRange": [0, 5], "yRange": [0, 160], "grid": true, "controls": [{"name": "theta", "range": [10, 60], "value": 40, "label": "theta_ja (C/W)"}], "functions": [{"expr": "25 + theta*x", "label": "Tj"}, {"expr": "125", "label": "limit", "color": "#dc2626"}]}
```

## Copper pours spread heat

A part soldered to a small pad cooks; the same part with a large **copper pour**
(a filled area of copper) connected to its thermal pad spreads the heat over a big
area that convects to air. More copper area means lower thermal resistance - a
broad, flattening curve:

```plot
{"title": "Thermal resistance vs copper pour area (diminishing returns)", "xLabel": "copper pour area (cm^2)", "yLabel": "theta to air (C/W)", "xRange": [1, 50], "yRange": [0, 90], "grid": true, "functions": [{"expr": "15 + 120/x", "label": "theta_pour"}]}
```

The curve flattens: doubling a small pour helps a lot, doubling a big one barely
moves it - air convection eventually limits you.

## Thermal vias: pull heat to the other side

A power part on top can dump heat through an array of **thermal vias** under its
thermal pad into an internal or bottom plane, which then spreads and convects.
A grid of vias under a QFN's centre pad is standard practice. Each via is a small
parallel thermal path - more vias, less resistance (until diminishing returns).

```mermaid
flowchart TB
  CHIP["power chip (top)"] --> PAD["thermal pad + copper pour"]
  PAD --> VIAS["thermal via array"]
  VIAS --> PLANE["internal/bottom plane"]
  PLANE --> AIR["convects to air"]
```

```matlab
Tamb = 25; P = 2; theta_ja = 35;
Tj = Tamb + P*theta_ja;            % 95 C junction temperature
margin = 125 - Tj;                 % 30 C headroom to a 125 C limit
```

```python
Tamb, P, theta_ja = 25, 2, 35
Tj = Tamb + P*theta_ja             # 95 C
margin = 125 - Tj                  # 30 C headroom
```

> **Practical insight:** read $\\theta_{ja}$ from the datasheet but trust it only
> with the **same copper** they tested on (often "1 oz, 4-layer, 2 in^2 pour").
> On a tiny board with little copper, the real $\\theta_{ja}$ is far worse - add
> pour and thermal vias.

**Next:** compute impedance and watch a reflection in code.
""",
        ),
        _code(
            "Lab: microstrip impedance & trace reflection",
            "14 min",
            """\
# Two parts:
#   (1) Compute microstrip characteristic impedance Z0 vs trace width and find
#       the width that gives 50 ohm on a given stackup.
#   (2) Simulate a step launched down a mismatched line and watch the reflection
#       bounce, using the lattice (bounce) summation.
import numpy as np
import matplotlib.pyplot as plt

# --- Part 1: microstrip Z0 (Wheeler/IPC approximation) ---
er = 4.3            # FR4 relative permittivity
h = 0.20            # dielectric height to the reference plane (mm)
t = 0.035           # copper thickness, 1 oz (mm)
w = np.linspace(0.10, 0.80, 300)        # trace width sweep (mm)

Z0 = 87/np.sqrt(er + 1.41) * np.log(5.98*h / (0.8*w + t))

# find the width closest to 50 ohm
idx = np.argmin(np.abs(Z0 - 50))
w50 = w[idx]
print(f"For h={h} mm FR4, 1 oz copper:")
print(f"  width for ~50 ohm = {w50:.3f} mm  (Z0 = {Z0[idx]:.1f} ohm)")

# --- Part 2: step reflections on a mismatched line ---
Z0_line = 50.0      # line impedance
Zs = 25.0           # source impedance (under-damped: Zs < Z0)
ZL = 1e9            # open-circuit load (receiver, high impedance)
Vsrc = 1.0          # 1 V step

gamma_s = (Zs - Z0_line) / (Zs + Z0_line)     # source reflection coeff
gamma_L = (ZL - Z0_line) / (ZL + Z0_line)     # load reflection coeff (~ +1)

tof = 0.5e-9        # one-way time of flight (line length / velocity)
tmax = 6e-9
dt = 1e-12
time = np.arange(0, tmax, dt)

# initial launched wave: divider between Zs and Z0
v_launch = Vsrc * Z0_line / (Zs + Z0_line)
vL = np.zeros_like(time)            # voltage seen at the receiver (load) end

# lattice diagram: each wave arrives at the load after odd multiples of tof
amp = v_launch
bounce = 0
arrival = tof
while arrival < tmax and abs(amp) > 1e-4:
    incident = amp
    reflected = gamma_L * incident
    vL[time >= arrival] += incident + reflected     # load sees incident+reflected
    amp = gamma_s * reflected                        # re-reflects off the source
    arrival += 2*tof
    bounce += 1

vfinal = Vsrc * ZL / (Zs + ZL)      # ~1 V dc final value

plt.figure(figsize=(8, 4.5))
plt.plot(time*1e9, vL, color="#dc2626", lw=2, label="receiver voltage")
plt.axhline(vfinal, ls="--", color="#94a3b8", label="settled value")
plt.xlabel("time (ns)"); plt.ylabel("voltage (V)")
plt.title(f"Reflections on a mismatched 50 ohm line (Zs={Zs:.0f} ohm, open load)")
plt.legend(); plt.grid(True); plt.show()

print(f"source reflection coeff = {gamma_s:+.2f}, load = {gamma_L:+.2f}")
print(f"first overshoot peak ~ {vL.max():.2f} V (settles to {vfinal:.2f} V)")

# Try it yourself:
#   1. Set Zs = 50: matched source, the ringing vanishes (series termination).
#   2. Set ZL = 50: matched load, also no ringing (parallel termination).
#   3. Raise h in Part 1: a wider trace is needed to hit 50 ohm.
""",
        ),
    ),
)


# -- PCB & Hardware Design -- Advanced -----------------------------------------

_PCB_ADVANCED = SeedCourse(
    slug="pcb-advanced",
    title="PCB & Hardware Design -- Advanced: EMC, High-Speed & Reliability",
    description=(
        "The hard parts: EMC/EMI (emissions, immunity, loop area, filtering, "
        "shielding, CISPR/FCC); advanced signal integrity (crosstalk, ISI, eye "
        "diagrams, S-parameters); power integrity and PDN analysis (target "
        "impedance, decoupling networks); RF and mixed-signal layout; and design "
        "for manufacturing, test and reliability (DFM/DFT, panelization, ICT). "
        "Dual MATLAB/Python, interactive plots, a runnable eye-diagram lab, and a "
        "full board bring-up workflow."
    ),
    level="Advanced",
    lessons=(
        _t(
            "EMC & EMI design",
            "13 min",
            """\
# EMC & EMI design

**EMC** (electromagnetic compatibility) means a product neither **emits** too much
interference nor is too easily **disturbed** by it. It is both a physics problem
and a legal one - a product cannot ship without passing **CISPR/FCC** limits.

## Two halves: emissions and immunity

- **Emissions** - how much energy your board radiates (and conducts onto its
  cables). Limited by **CISPR 32 / FCC Part 15**.
- **Immunity (susceptibility)** - how well it survives external fields, ESD
  zaps, and surges (**IEC 61000** family).

## The root cause: loop area and current

A current loop is a little antenna. Radiated emission rises with the **loop
area**, the **current**, and the **square of frequency**:

$$E \\propto \\frac{A\\,I\\,f^2}{r}.$$

So the single most powerful EMC fix is to **shrink loop areas** - which is exactly
the return-path discipline from the Intermediate course. Slide frequency and watch
emission climb steeply with loop area:

```plot
{"title": "Relative radiated emission vs loop area (slide frequency)", "xLabel": "loop area (mm^2)", "yLabel": "relative emission", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "controls": [{"name": "f", "range": [50, 300], "value": 100, "label": "frequency (MHz)"}], "functions": [{"expr": "x*(f/100)^2", "label": "emission ~ A f^2"}]}
```

## The toolkit

| Technique | Attacks |
|-----------|---------|
| Solid ground plane, tight return paths | loop area (emissions + immunity) |
| Slow edge rates (series R, ferrite) | high-frequency harmonic content |
| Filtering (decoupling, ferrites, common-mode chokes) | conducted noise on power/cables |
| Shielding (cans, chassis, gaskets) | radiated coupling |
| Guard traces / ground stitching | crosstalk and field leakage |

## Why edges, not clocks, dominate emissions

A signal's harmonic content extends to about $f_{knee} = 0.35/t_{rise}$. A fast
1 ns edge has strong energy past 350 MHz regardless of the clock rate, and those
high harmonics radiate hardest ($f^2$ above). **Slowing the edges** you do not
need to be fast is free EMC margin.

```mermaid
flowchart LR
  SRC["switching current"] --> LOOP["loop area"]
  LOOP --> EMIT["radiated emission"]
  CABLE["attached cable"] --> ANT["acts as antenna"]
  EMIT --> FAIL["CISPR/FCC test"]
  ANT --> FAIL
```

Cables are notorious: a noisy ground turns an attached cable into an efficient
antenna. **Common-mode chokes** and good connector grounding tame it.

```matlab
trise = 1e-9;
fknee = 0.35/trise;                % ~350 MHz significant bandwidth
```

```python
trise = 1e-9
fknee = 0.35/trise                 # ~350 MHz
```

> **Practical insight:** design for EMC from the **first placement**, not after a
> failed test. 90% of fixes are free at layout time (plane integrity, edge rates,
> decoupling) and expensive afterward (shield cans, ferrites, board respins).

**Next:** the eye closes - advanced signal integrity.
""",
        ),
        _t(
            "Advanced signal integrity: crosstalk, ISI, eye diagrams & S-parameters",
            "13 min",
            """\
# Advanced signal integrity: crosstalk, ISI, eye diagrams & S-parameters

At multi-gigabit speeds, a channel is no longer "fast wire" - it is a frequency-
dependent filter that smears and closes the data. Advanced SI is about
**quantifying** that damage.

## Inter-symbol interference (ISI)

A real channel has **loss that rises with frequency** (copper skin effect and
dielectric loss). High-frequency content is attenuated more, so a sharp bit edge
**spreads in time** and bleeds into neighbouring bits - **ISI**. The previous bits
leave a tail that shifts where the current bit crosses the threshold.

## The eye diagram: the SI scorecard

Overlay every bit period of a long random data stream on top of each other and you
get an **eye diagram**. A clean channel gives a wide-open "eye"; loss, ISI,
crosstalk and jitter **close** it. Receivers need a minimum **eye height**
(voltage margin) and **eye width** (timing margin) to recover data. A stylised eye
- two crossing transition bundles framing the open centre:

```plot
{"title": "Eye diagram outline: transitions cross, the open centre is the eye", "xLabel": "time within bit period (UI)", "yLabel": "voltage", "xRange": [0, 1], "yRange": [-1.3, 1.3], "grid": true, "parametric": [{"x": "t", "y": "tanh(6*(t-0.5))", "range": [0, 1], "label": "rising edges", "color": "#2563eb"}, {"x": "t", "y": "-tanh(6*(t-0.5))", "range": [0, 1], "label": "falling edges", "color": "#dc2626"}, {"x": "t", "y": "1", "range": [0, 1], "label": "high level", "color": "#16a34a"}, {"x": "t", "y": "-1", "range": [0, 1], "label": "low level", "color": "#16a34a"}]}
```

The vertical gap at the centre is the eye **height**; the horizontal span at the
threshold is the eye **width**. ISI and crosstalk shrink both.

## Channel loss closes the eye

Insertion loss grows with frequency, so a faster bit rate (more high-frequency
content) suffers more. Slide the per-length loss and watch eye opening collapse as
data rate rises:

```plot
{"title": "Eye opening vs data rate (slide channel loss)", "xLabel": "data rate (Gbps)", "yLabel": "relative eye opening", "xRange": [1, 25], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "loss", "range": [0.1, 1.5], "value": 0.5, "label": "loss factor (dB/Gbps/in)"}], "functions": [{"expr": "exp(-loss*x/8)", "label": "eye opening"}]}
```

The cure at high speed is **equalization** - pre-emphasis at the transmitter and
**CTLE/DFE** at the receiver boost the attenuated highs to reopen the eye.

## S-parameters: the language of high-speed channels

Above ~1 GHz we characterise interconnects by **scattering parameters**
(S-parameters), measured with a vector network analyser or simulated:

- $S_{11}$ - **return loss** (how much reflects back; want it very negative dB).
- $S_{21}$ - **insertion loss** (how much gets through; want it near 0 dB).
- Differential and crosstalk terms ($S_{dd21}$, near/far-end crosstalk).

These feed channel simulators that predict the eye before fabrication.

```matlab
% Insertion loss magnitude to dB
S21 = 0.5;                          % linear (half the amplitude through)
S21_dB = 20*log10(S21);             % -6 dB
fknee = 0.35/50e-12;                % 50 ps edge -> 7 GHz content
```

```python
import numpy as np
S21 = 0.5
S21_dB = 20*np.log10(S21)           # -6 dB
fknee = 0.35/50e-12                 # 7 GHz content
```

> **Practical insight:** at >5 Gbps, simulate the **channel** (trace + vias +
> connectors + package) from S-parameters and check the eye before you build.
> Most high-speed failures are designed in, then discovered on a $50k respin.

**Next:** keeping the supply quiet - power integrity and PDN analysis.
""",
        ),
        _t(
            "Power integrity & PDN analysis",
            "12 min",
            """\
# Power integrity & PDN analysis

**Power integrity (PI)** asks: does every chip see a clean, stable supply across
all frequencies, even as it draws fast transient current? The tool is the **PDN
impedance profile** versus frequency, compared to a **target impedance**.

## The target impedance

If a chip may step its current by $\\Delta I$ and you allow a supply ripple
$\\Delta V$, the PDN must satisfy, at **every** frequency of interest:

$$Z_{PDN}(f) \\le Z_{target} = \\frac{\\Delta V}{\\Delta I}.$$

A modern core might allow only 30 mV on a 20 A step - a target near **1.5
milliohm**, flat to tens of MHz. That is extraordinarily low and only achievable
with planes plus a designed capacitor network.

## The PDN is a chain of resonators

Each piece covers a frequency band:

| Element | Helps in band |
|---------|---------------|
| VRM (regulator) + bulk caps | DC to ~100 kHz |
| Electrolytic / large MLCC | ~100 kHz to ~1 MHz |
| Mid MLCC (1-10 uF) | ~1 to ~20 MHz |
| Small MLCC (10-100 nF) | ~20 to ~200 MHz |
| On-package / on-die caps | > 200 MHz |

Where two stages overlap, their inductance and capacitance can form an
**anti-resonance** - a *peak* in impedance that may poke above target. PI design
is largely about flattening these peaks. Slide the number of decoupling caps and
watch the impedance profile drop toward target:

```plot
{"title": "PDN impedance vs frequency (slide number of decoupling caps)", "xLabel": "frequency (MHz)", "yLabel": "|Z_PDN| (milliohm)", "xRange": [1, 200], "yRange": [0, 20], "grid": true, "controls": [{"name": "N", "range": [1, 30], "value": 8, "label": "number of caps N"}], "functions": [{"expr": "1.5 + 60/N + 0.06*x", "label": "|Z_PDN|"}, {"expr": "5", "label": "target", "color": "#dc2626"}]}
```

## Designing the decoupling network

1. Compute $Z_{target}$ from the chip's $\\Delta V$, $\\Delta I$.
2. Pick capacitor **values** so their self-resonances tile the frequency range.
3. Choose **quantities** so the parallel impedance stays under target between
   resonances (more caps in parallel = lower $Z$, and they split current).
4. **Minimise mounting inductance** (short, fat vias; caps near the chip).
5. Verify with a PDN simulator (or measure with a VNA on a prototype).

```mermaid
flowchart LR
  VRM["VRM + bulk"] --> BULK["bulk caps (low f)"]
  BULK --> MID["mid MLCC"]
  MID --> SMALL["small MLCC (high f)"]
  SMALL --> DIE["on-die caps"]
  DIE --> CORE["chip core"]
```

```matlab
dV = 0.030; dI = 20;               % 30 mV on a 20 A step
Ztarget = dV/dI;                   % 0.0015 ohm = 1.5 milliohm
N = 10; Zcap = 0.02;               % each cap ~20 milliohm at its resonance
Zpar = Zcap/N;                     % N in parallel -> 2 milliohm
```

```python
dV, dI = 0.030, 20                 # 30 mV on a 20 A step
Ztarget = dV/dI                    # 1.5 milliohm
N, Zcap = 10, 0.02
Zpar = Zcap/N                      # 2 milliohm
```

> **Practical insight:** do not just sprinkle "100 nF per pin." Compute the target,
> tile the resonances, watch for **anti-resonant peaks** between stages, and put
> the highest-frequency caps closest to the die.

**Next:** the hardest neighbours - RF and mixed-signal layout.
""",
        ),
        _t(
            "RF & mixed-signal layout",
            "12 min",
            """\
# RF & mixed-signal layout

When sensitive analog/RF shares a board with noisy digital, layout decides whether
the radio hears the signal or the switching regulator. The themes are
**partitioning**, **isolation**, and disciplined **grounding**.

## Partition the board by function

Physically separate the **noisy** (digital, switching supplies, clocks) from the
**quiet** (precision analog, RF front-end, ADC inputs). Group each domain, give it
its own clean local supply, and route signals so they never wander through a
foreign domain.

```mermaid
flowchart LR
  RF["RF / antenna front-end"] --- ANALOG["precision analog + ADC"]
  ANALOG --- DIGITAL["digital MCU / DSP"]
  DIGITAL --- POWER["switching supplies"]
```

## Isolation and grounding

- **One solid ground plane** under RF is usually best - it gives a continuous
  return and a reference for controlled impedance. The old "cut the plane" advice
  often makes EMC worse.
- For mixed analog/digital with an ADC, keep both grounds as **one plane** but
  **partition the placement** so digital return currents do not flow under analog.
  Join domains under the converter.
- **Guard rings and ground stitching vias** fence sensitive nodes and stop fields
  leaking between sections.
- Keep noisy clocks and switchers far from the antenna and ADC inputs.

## Controlled impedance and matching for RF

RF traces are transmission lines that must hold **50 ohm** (or the system
impedance) and connect to **impedance-matching networks** so power transfers
instead of reflecting. A mismatch wastes power and detunes the radio. The matched
condition (load = source impedance) is where delivered power peaks - the same
maximum-power-transfer idea from circuits:

```plot
{"title": "Delivered RF power vs load match (source 50 ohm), peak at the match", "xLabel": "load resistance (ohm)", "yLabel": "relative delivered power", "xRange": [0, 200], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "4*50*x/(50+x)^2", "label": "delivered power"}, {"expr": "1", "label": "matched maximum", "color": "#16a34a"}]}
```

## Antennas on the PCB

Many products use a **PCB antenna** (a trace - inverted-F, meander) or a chip
antenna. Rules: give it a **keep-out** (no copper/ground under or near it), place
it at a **board edge**, keep it clear of metal and the battery, and respect the
manufacturer's reference layout exactly. A few millimetres of stray ground can
detune it badly.

```matlab
% Quarter-wave PCB trace antenna physical length (with FR4 shortening)
c = 3e8; f = 2.45e9; er_eff = 3.0;
lambda = c/f;
quarter = (lambda/4)/sqrt(er_eff);   % shortened by the dielectric
```

```python
import numpy as np
c, f, er_eff = 3e8, 2.45e9, 3.0
lam = c/f
quarter = (lam/4)/np.sqrt(er_eff)     # shortened quarter-wave length
```

> **Practical insight:** for RF, **copy the chip vendor's reference layout** for
> the antenna and matching network first, then optimise. The physics is
> unforgiving and a measured VNA sweep beats any guess.

**Next:** making it buildable, testable and reliable for the long haul.
""",
        ),
        _t(
            "Design for manufacturing, test & reliability",
            "12 min",
            """\
# Design for manufacturing, test & reliability

A board that works on the bench but cannot be **built**, **tested**, or **trusted
to last** is not a product. DFM, DFT and DFR turn a prototype into something you
can ship by the thousand.

## DFM - design for manufacturing

Make it easy and cheap to fabricate and assemble:

- Honour the fab's **trace/space, drill, annular ring** capabilities with margin.
- **Thermal reliefs** on pads tied to planes so they solder (a pad sucking heat
  into a plane will not reflow well).
- Component **courtyards** - spacing for the placement head and rework.
- **Fiducials** - reference marks the assembly camera uses to align.
- **Panelization** - arrange many boards in a panel (with tabs or V-scores) so the
  assembly line runs efficiently; add panel rails and tooling holes.

```mermaid
flowchart LR
  PCB["single board"] --> PANEL["panelize (array + rails + fiducials)"]
  PANEL --> ASM["assembly line"]
  ASM --> DEPANEL["depanel to single boards"]
```

## DFT - design for test

You must prove each built board works. Provide:

- **Test points** on key nets (power rails, clocks, buses) for a bed-of-nails
  **in-circuit test (ICT)** or flying-probe.
- **Boundary scan (JTAG)** to test digital interconnects without physical probes.
- A **functional test** fixture that exercises the real behaviour.
- Programming/debug headers (SWD/JTAG) and, ideally, status LEDs.

Test coverage is an explicit goal: more accessible nodes = higher fault coverage,
but more test points cost board area. There is a sweet spot of diminishing
returns:

```plot
{"title": "Fault coverage vs number of test points (diminishing returns)", "xLabel": "test points", "yLabel": "fault coverage (%)", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "95*(1 - exp(-x/25))", "label": "coverage"}]}
```

## DFR - design for reliability

Make it survive years of stress:

- **Derate** parts - run capacitors, resistors and semiconductors well below
  their max voltage/power/temperature.
- Plan for **thermal cycling** - mismatched expansion fatigues solder joints
  (BGA corners especially); thermal vias and pad design help.
- Mind **electromigration** and current density in narrow traces.

Reliability often follows a **bathtub curve**: high early failures (infant
mortality, screened out by burn-in), a long low-rate useful life, then wear-out:

```plot
{"title": "Reliability bathtub curve: failure rate over a product life", "xLabel": "time (arbitrary)", "yLabel": "failure rate", "xRange": [0, 10], "yRange": [0, 5], "grid": true, "functions": [{"expr": "3*exp(-1.5*x) + 0.3 + 0.04*x^2", "label": "failure rate"}]}
```

```matlab
Vmax = 50; derate = 0.5;
Vrated_use = Vmax*derate;          % use a 50 V cap at <= 25 V
```

```python
Vmax, derate = 50, 0.5
Vrated_use = Vmax*derate           # use a 50 V cap at <= 25 V
```

> **Practical insight:** DFM/DFT/DFR are cheapest at **design time** and ruinous
> later. Add test points, fiducials and derating before the first build - retrofit
> is a respin.

**Next:** see the math close an eye in a runnable lab.
""",
        ),
        _code(
            "Lab: eye diagram from a lossy channel",
            "14 min",
            """\
# Build an eye diagram for a PRBS-like bit stream sent through a simple lossy
# (low-pass) channel, and measure how the eye closes as channel bandwidth drops.
# An eye diagram overlays every bit period of the received waveform.
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)

bitrate = 5e9                  # 5 Gbps
ui = 1/bitrate                 # unit interval (one bit period)
sps = 32                       # samples per bit
n_bits = 400
dt = ui/sps

# random bit stream -> NRZ levels (+1 / -1)
bits = np.random.randint(0, 2, n_bits)
nrz = 2*bits - 1
tx = np.repeat(nrz, sps).astype(float)        # ideal transmitted waveform

# simple one-pole low-pass channel (RC), models frequency-dependent loss
f3db = 3e9                     # channel bandwidth (Hz)
alpha = dt / (dt + 1/(2*np.pi*f3db))
rx = np.zeros_like(tx)
acc = 0.0
for k in range(len(tx)):
    acc = acc + alpha*(tx[k] - acc)           # first-order IIR low-pass
    rx[k] = acc

# fold the received waveform into eye traces, two UI wide
eye_len = 2*sps
n_traces = len(rx)//sps - 2
t_eye = np.linspace(0, 2, eye_len)            # in units of UI

plt.figure(figsize=(8, 4.5))
for i in range(n_traces):
    seg = rx[i*sps:i*sps + eye_len]
    if len(seg) == eye_len:
        plt.plot(t_eye, seg, color="#2563eb", alpha=0.15)

# measure eye height at the sampling instant (centre of a bit, t = 0.5 UI here)
sample_idx = sps//2
levels = rx[sample_idx::sps]
hi = levels[levels > 0]
lo = levels[levels < 0]
eye_height = (hi.min() - lo.max()) if len(hi) and len(lo) else 0.0

plt.axvline(0.5, ls="--", color="#dc2626", label="sample instant")
plt.xlabel("time (UI)"); plt.ylabel("voltage")
plt.title(f"Eye diagram at {bitrate/1e9:.0f} Gbps, channel BW {f3db/1e9:.0f} GHz")
plt.legend(loc="upper right"); plt.grid(True); plt.show()

print(f"unit interval = {ui*1e12:.0f} ps")
print(f"measured eye height = {eye_height:.2f} (of 2.0 full swing)")
print("Lower f3db (less channel bandwidth) -> ISI grows -> eye closes.")

# Try it yourself:
#   1. Set f3db = 1e9: the eye nearly closes (heavy ISI).
#   2. Set f3db = 10e9: a wide-open eye (low-loss channel).
#   3. Raise bitrate to 10e9: faster data through the same channel closes the eye.
""",
        ),
        _t(
            "Applications & a full board bring-up workflow",
            "12 min",
            """\
# Applications & a full board bring-up workflow

This final lesson ties the whole track to **real products** and to the day every
hardware engineer dreads and loves: **bring-up**, when the first boards arrive.

## Real boards, real constraints

| Product | The PCB challenge that dominates |
|---------|----------------------------------|
| **Smartphone** | HDI stackup, blind/buried vias, RF antenna isolation, brutal space and thermal limits |
| **DDR memory module** | length matching to picoseconds, controlled differential impedance, PDN for the controller |
| **Switching power supply** | thermal copper pours, tight switching loops to cut EMI, creepage/clearance for safety |
| **Motor driver / EV inverter** | heavy copper for current, thermal vias and heatsinks, isolation between power and control |
| **IoT sensor node** | tiny 2/4-layer board, integrated antenna, ultra-low-power layout, cost-driven DFM |
| **Server / GPU board** | 12+ layers, multi-gigabit SerDes with equalization, milliohm PDN, dense BGA escape routing |
| **Medical / aerospace** | DFR and traceability dominate: derating, conformal coat, redundancy, documented test coverage |

Every one of these is the **same physics** from this track, weighted differently:
loop area and return paths (EMC), controlled impedance and eye margin (SI), target
impedance (PI), copper and vias (thermal), and DFM/DFT/DFR for production.

## The design-to-product pipeline

```mermaid
flowchart TB
  REQ["requirements"] --> SCH["schematic capture"]
  SCH --> STK["stackup + impedance plan"]
  STK --> LAY["placement + routing"]
  LAY --> SIM["SI / PI / thermal / DRC checks"]
  SIM --> FAB["fab + assembly"]
  FAB --> BRINGUP["bring-up + test"]
  BRINGUP --> SHIP["volume production"]
  BRINGUP -->|"issues"| SCH
```

## Board bring-up: a disciplined first-power sequence

When the first prototype lands, resist the urge to plug it in. Work outward from
power, checking at every step:

```mermaid
stateDiagram-v2
  [*] --> Inspect
  Inspect --> PowerOffChecks: visual + DMM
  PowerOffChecks --> CurrentLimitedPower: no shorts rail-to-GND
  CurrentLimitedPower --> CheckRails: bench supply, low I-limit
  CheckRails --> Clocks: rails in spec
  Clocks --> Programming: oscillators alive
  Programming --> Functional: MCU/FPGA boots
  Functional --> Debug: exercise features
  Debug --> [*]: passes
  CurrentLimitedPower --> Debug: over-current -> find short
  CheckRails --> Debug: wrong voltage -> trace it
```

Step by step:

1. **Inspect** - look for solder bridges, tombstoned parts, wrong/missing
   components, reversed polarity.
2. **Power-off checks** - DMM continuity: confirm no rail is shorted to ground,
   confirm part orientations.
3. **Current-limited first power** - feed the board from a **bench supply with a
   low current limit**. If it slams into the limit, you have a short - power down
   and find it before anything cooks.
4. **Check the rails** - measure every supply voltage at the point of load; verify
   sequencing and ripple on a scope.
5. **Clocks** - scope every oscillator/crystal; nothing digital works without them.
6. **Program and boot** - load firmware over SWD/JTAG; get the simplest "blink an
   LED" alive.
7. **Functional test** - exercise each interface, compare against your simulation
   and expectations, and reconcile every difference.

```matlab
% Bring-up sanity: expected vs measured rail, flag if out of tolerance
Vexp = 3.3; Vmeas = 3.21; tol = 0.05;     % 5% tolerance
ok = abs(Vmeas - Vexp) <= tol*Vexp;       % true -> rail in spec
```

```python
Vexp, Vmeas, tol = 3.3, 3.21, 0.05
ok = abs(Vmeas - Vexp) <= tol*Vexp        # True -> rail in spec
```

## The throughline

A schematic of nets becomes footprints on a stackup, routed as controlled-impedance
copper with continuous return paths, decoupled to a milliohm PDN, kept cool by
copper and vias, made quiet enough to pass CISPR/FCC, and designed so the factory
can build it, the line can test it, and the field can trust it. Model it
(MATLAB/Python/SPICE/field solvers), respect the physics, measure it on bring-up,
and iterate. The tools change; the loop area, the impedance, and the return path
never stop mattering.

**Next:** the final check.
""",
        ),
    ),
)


PCB_COURSES: tuple[SeedCourse, ...] = (
    _PCB_BASICS,
    _PCB_INTERMEDIATE,
    _PCB_ADVANCED,
)

__all__ = ["PCB_COURSES"]
