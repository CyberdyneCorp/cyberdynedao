"""Curated VLSI & IC Design track: Basics, Intermediate, Advanced.

A complete VLSI curriculum: CMOS device and gate fundamentals (the inverter,
combinational and sequential logic, the design flow, layout and design rules),
delay/power/interconnect and datapath/memory design, and advanced topics
(low-power design, clocking, physical design and signoff, design-for-test, and
analog/mixed-signal plus advanced nodes). Dual SystemVerilog (RTL) + Python
(modeling/analysis) focus throughout, with runnable Python labs (numpy +
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


# -- VLSI & IC Design -- Basics ------------------------------------------------

_VLSI_BASICS = SeedCourse(
    slug="vlsi-basics",
    title="VLSI & IC Design -- Basics",
    description=(
        "VLSI from the ground up: MOSFETs as switches and the static CMOS "
        "inverter, combinational and sequential CMOS logic, the spec-to-GDSII "
        "design flow (ASIC vs FPGA), and layout with design rules - with "
        "side-by-side SystemVerilog and Python, interactive plots, and a "
        "runnable CMOS inverter VTC lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What VLSI is and the CMOS inverter",
            "12 min",
            """\
# What VLSI is and the CMOS inverter

**VLSI** (Very-Large-Scale Integration) is the art of putting *billions* of
transistors on a single chip. A modern CPU, GPU, or phone SoC is VLSI: the same
physics you will learn here, repeated a few billion times. The building block of
almost all of it is the **MOSFET used as a switch**, wired up in **CMOS**
(Complementary MOS).

## MOSFETs as switches

A MOSFET has a gate, a source, and a drain. The gate voltage decides whether the
drain-source path conducts:

- **NMOS** - turns **on** when the gate is **high**, passes a strong 0. Think of
  it as a switch to ground.
- **PMOS** - turns **on** when the gate is **low**, passes a strong 1. Think of
  it as a switch to the supply $V_{DD}$.

The two are complementary, which is the whole trick of CMOS.

## The static CMOS inverter

Stack one PMOS (top, to $V_{DD}$) and one NMOS (bottom, to ground), gates tied
together as the input, drains tied together as the output:

```mermaid
flowchart TB
  VDD["VDD"] --> P["PMOS (on when in = 0)"]
  P --> OUT(("out"))
  OUT --> N["NMOS (on when in = 1)"]
  N --> GND["ground"]
  IN["in"] --> P
  IN --> N
```

- Input **0** -> PMOS on, NMOS off -> output pulled to **1**.
- Input **1** -> PMOS off, NMOS on -> output pulled to **0**.

Exactly **one** network conducts at a time, so in the steady state there is no
direct path from $V_{DD}$ to ground: a static CMOS gate draws **almost no static
current**. That single property is why CMOS won and why your laptop battery
lasts hours instead of minutes.

## The voltage transfer characteristic (VTC)

Sweep the input from 0 to $V_{DD}$ and plot the output. The result is the
**VTC**: flat-high, a sharp drop near the switching threshold $V_M$, then
flat-low. The steep middle is the **gain** region. Slide $V_{DD}$ and watch the
curve rescale:

```plot
{"title": "CMOS inverter VTC (idealized, slide VDD)", "xLabel": "input Vin (V)", "yLabel": "output Vout (V)", "xRange": [0, 3.3], "yRange": [0, 3.3], "grid": true, "controls": [{"name": "VDD", "range": [1, 3.3], "value": 3.3, "label": "supply VDD (V)"}], "functions": [{"expr": "VDD/(1 + exp(12*(x - VDD/2)/VDD))", "label": "Vout(Vin)"}]}
```

## Noise margins

A gate must reject small voltage disturbances. The **noise margins** measure
how much noise an input can tolerate and still be read correctly:

$$NM_H = V_{OH} - V_{IH}, \\qquad NM_L = V_{IL} - V_{OL}.$$

We unpack these in the lab at the end of this course.

## Same idea, two languages

```systemverilog
// Behavioral RTL: synthesis maps this to a CMOS inverter.
module inv (input  logic a,
            output logic y);
  assign y = ~a;
endmodule
```

```python
def cmos_inverter(a: int) -> int:
    return 0 if a else 1  # ideal: in=1 -> out=0, in=0 -> out=1
```

**Next:** building real combinational logic from pull-up/pull-down networks.
""",
        ),
        _t(
            "Combinational CMOS logic",
            "12 min",
            """\
# Combinational CMOS logic

An inverter is one transistor each side. Real gates use a **pull-up network**
(PUN, PMOS to $V_{DD}$) and a **pull-down network** (PDN, NMOS to ground) that
are **logical complements** of each other:

- The PDN pulls the output **low** for exactly the input combinations where the
  function is 0.
- The PUN pulls the output **high** for the complementary combinations.

Series NMOS = AND in the pull-down; parallel NMOS = OR. The PUN is the dual:
series becomes parallel.

## NAND and NOR

A 2-input **NAND** has two NMOS in **series** (output low only when *both* inputs
are high) and two PMOS in **parallel**:

```mermaid
flowchart TB
  VDD["VDD"] --> PA["PMOS a"] --> OUT(("out"))
  VDD --> PB["PMOS b"] --> OUT
  OUT --> NA["NMOS a (series)"]
  NA --> NB["NMOS b (series)"]
  NB --> GND["ground"]
```

A 2-input **NOR** is the mirror image: NMOS in parallel, PMOS in series. In CMOS,
**NAND and NOR are the natural gates** - AND/OR cost an extra inverter. Static
CMOS gates are always **inverting**, so designers build logic from NAND/NOR/INV.

## Transistor sizing

Electrons (NMOS) are roughly 2-3x more mobile than holes (PMOS), so a PMOS must
be made **wider** to source as much current as an NMOS sinks. To get a symmetric
inverter you size $W_p/W_n \\approx 2$. In a NAND, the **series** NMOS each see
half the drive, so they are widened; in a NOR the **series** PMOS hurt more,
which is why NOR is usually slower than NAND. The drive current rises with the
width-to-length ratio:

$$I_D \\propto \\frac{W}{L}\\,(V_{GS} - V_{th})^2 \\;\\text{(saturation, long channel)}.$$

Slide the threshold and watch the saturation drive current of one transistor:

```plot
{"title": "MOSFET saturation drive vs gate voltage (slide threshold)", "xLabel": "gate voltage Vgs (V)", "yLabel": "drain current Id (relative)", "xRange": [0, 3.3], "yRange": [0, 12], "grid": true, "controls": [{"name": "Vth", "range": [0.3, 1.2], "value": 0.6, "label": "threshold Vth (V)"}], "functions": [{"expr": "(x > Vth)*1.5*(x - Vth)^2", "label": "Id (on above Vth)"}]}
```

## Two languages, one NAND

```systemverilog
module nand2 (input  logic a, b,
              output logic y);
  assign y = ~(a & b);   // synthesizes to series-NMOS / parallel-PMOS
endmodule
```

```python
def nand2(a: int, b: int) -> int:
    return 0 if (a and b) else 1
```

> **Practical insight:** every standard-cell library is a catalog of pre-sized,
> pre-laid-out gates (INV, NAND, NOR, AOI, flip-flops) at several drive
> strengths (1x, 2x, 4x). Synthesis picks from this catalog - you rarely draw
> transistors by hand.

**Next:** adding memory - sequential CMOS.
""",
        ),
        _t(
            "Sequential CMOS: latches, flip-flops & clocking",
            "12 min",
            """\
# Sequential CMOS: latches, flip-flops & clocking

Combinational logic has no memory - its output depends only on the present
input. To **store state** you add feedback, and to keep a whole chip marching in
step you add a **clock**.

## Latches vs flip-flops

- A **latch** is **level-sensitive**: while the clock (enable) is high it is
  transparent (output follows input); when low it holds.
- A **flip-flop** is **edge-triggered**: it samples the input only at the clock
  **edge** (usually rising). Build one from two opposite-phase latches in
  series - a **master-slave** D flip-flop.

```mermaid
stateDiagram-v2
  [*] --> Hold
  Hold --> Sample: rising clock edge
  Sample --> Hold: capture D into Q
```

Edge-triggered flip-flops are the backbone of **synchronous design**: state
updates once per clock edge, which makes timing analysis tractable (next
course).

## Clocking and the clock period

Between two flip-flops sits combinational logic. The clock period $T$ must be
long enough for a signal to leave one flop, propagate through the logic, and
arrive before the next flop samples:

$$T \\ge t_{cq} + t_{logic} + t_{setup}.$$

Slide the logic delay and see the minimum clock period (hence the maximum clock
frequency $f = 1/T$):

```plot
{"title": "Minimum clock period vs logic delay (tcq=0.1, tsetup=0.05 ns)", "xLabel": "logic delay (ns)", "yLabel": "min clock period T (ns)", "xRange": [0.1, 5], "yRange": [0, 6], "grid": true, "controls": [{"name": "margin", "range": [0, 1], "value": 0.2, "label": "extra timing margin (ns)"}], "functions": [{"expr": "x + 0.1 + 0.05 + margin", "label": "T_min"}]}
```

## Two languages, one D flip-flop

```systemverilog
module dff (input  logic clk, d,
            output logic q);
  always_ff @(posedge clk)   // edge-triggered: sample d on the rising edge
    q <= d;
endmodule
```

```python
class DFF:
    def __init__(self):
        self.q = 0

    def clock_edge(self, d: int) -> int:
        self.q = d  # capture on the (modeled) rising edge
        return self.q
```

> **Practical insight:** mixing latches and flops, or gating clocks carelessly,
> causes the hardest bugs in VLSI. Beginners stick to a single clock and
> edge-triggered flip-flops; that discipline is what makes static timing
> analysis possible.

**Next:** how a chip actually gets built - the design flow.
""",
        ),
        _t(
            "The IC design flow: spec to GDSII",
            "12 min",
            """\
# The IC design flow: spec to GDSII

A chip travels a long pipeline from idea to silicon. Knowing the stages tells you
where your RTL fits and what each tool does.

```mermaid
flowchart LR
  SPEC["spec / architecture"] --> RTL["RTL (SystemVerilog)"]
  RTL --> SYN["logic synthesis -> gate netlist"]
  SYN --> PNR["place & route"]
  PNR --> SIGN["timing/power signoff"]
  SIGN --> GDS["GDSII -> mask / fab"]
```

## The stages

1. **Specification & architecture** - what the chip does, performance, power,
   area budgets.
2. **RTL design** - describe behavior register-transfer-level in
   **SystemVerilog** or VHDL; verify with simulation and testbenches.
3. **Logic synthesis** - a tool maps RTL to a **gate-level netlist** of
   standard cells, optimizing for timing/area/power.
4. **Place & route (P&R)** - physically place cells and wire them together on
   the silicon floorplan.
5. **Signoff** - static timing analysis, power, and physical verification
   confirm the design meets constraints.
6. **GDSII** - the final layout file sent to the **foundry** to make the masks.

## ASIC vs FPGA

| | ASIC | FPGA |
|--|------|------|
| What it is | custom silicon, fixed at fab | pre-fabricated, **reconfigurable** logic |
| NRE / unit cost | huge NRE, tiny unit cost | no NRE, higher unit cost |
| Performance / power | best | good, but more overhead |
| Time to working chip | months | minutes (just reprogram) |
| Best for | very high volume, max performance | prototypes, low/medium volume, field updates |

The **same RTL** can target either: synthesis maps to standard cells (ASIC) or
to look-up tables and the FPGA fabric. ASICs power iPhones and data-center
accelerators; FPGAs power prototypes, networking gear, and aerospace where a
field update beats a respin.

## A simple comparison

The relative *unit* cost of each technology crosses over with volume: FPGAs win
at low volume, ASICs win once the NRE is amortized.

```plot
{"title": "Cost per part vs production volume (relative)", "xLabel": "volume (thousands of units)", "yLabel": "cost per part (relative)", "xRange": [1, 100], "yRange": [0, 60], "grid": true, "functions": [{"expr": "30000/x + 2", "label": "ASIC (huge NRE, cheap parts)", "color": "#2563eb"}, {"expr": "0*x + 25", "label": "FPGA (no NRE, pricey parts)", "color": "#dc2626"}]}
```

The crossover (where the lines meet) is the volume above which an ASIC pays off.

```systemverilog
// The same module targets an ASIC standard-cell library or an FPGA fabric.
module adder8 (input  logic [7:0] a, b,
               output logic [8:0] sum);
  assign sum = a + b;
endmodule
```

```python
def adder8(a: int, b: int) -> int:
    return (a & 0xFF) + (b & 0xFF)  # the model synthesis must match
```

**Next:** what the layout actually looks like, and the rules it must obey.
""",
        ),
        _t(
            "Layout & design rules",
            "11 min",
            """\
# Layout & design rules

Eventually transistors and wires become **geometry**: stacked rectangles on
different material **layers**. Layout is where logical intent meets manufacturing
reality.

## The layers

From bottom up, roughly:

- **Active / diffusion** - where transistors live (source/drain regions).
- **Polysilicon** - the gate; where poly crosses active, a transistor forms.
- **Contacts / vias** - vertical connections between layers.
- **Metal 1, Metal 2, ... (M1-M10+)** - the wiring stack that routes signals,
  power, and clock.

```mermaid
flowchart TB
  M2["Metal 2 (routing)"] --> V1["via"]
  V1 --> M1["Metal 1 (routing)"]
  M1 --> CT["contact"]
  CT --> POLY["poly gate over active"]
  POLY --> ACT["active / diffusion (transistor)"]
```

## Lambda rules and stick diagrams

To stay process-portable, classic layouts use **lambda ($\\lambda$) rules**:
express every spacing and width as a multiple of one scalable unit $\\lambda$
(half the minimum feature size). A minimum wire might be $3\\lambda$ wide with
$3\\lambda$ spacing.

A **stick diagram** is a quick, color-coded sketch of a cell - lines for poly and
metal, without exact dimensions - used to plan a layout's topology before drawing
real rectangles.

## DRC and LVS - the two gatekeepers

- **DRC (Design Rule Check)** - verifies the geometry obeys the foundry's rules
  (minimum widths, spacings, enclosures). A DRC-clean layout is *manufacturable*.
- **LVS (Layout Versus Schematic)** - extracts a netlist from the drawn layout
  and checks it **matches the schematic/netlist** you intended. LVS-clean means
  *you drew what you meant*.

You are not done until both pass.

## Area scales with the square of the rule

If you tighten the design rule (feature size) by a factor $k$, the area of a
fixed-function block scales roughly as $1/k^2$ - the engine of Moore's Law. Slide
the feature size and watch a cell's relative area:

```plot
{"title": "Cell area vs feature size (area ~ 1/feature^2)", "xLabel": "feature size (relative)", "yLabel": "cell area (relative)", "xRange": [0.2, 2], "yRange": [0, 30], "grid": true, "controls": [{"name": "cells", "range": [1, 4], "value": 1, "label": "number of cells"}], "functions": [{"expr": "cells*1/(x*x)", "label": "area"}]}
```

```systemverilog
// RTL is layer-agnostic, but constraints tell P&R the physical targets.
// (constraint excerpt, not synthesizable logic)
//   create_clock -period 2.0 [get_ports clk]
//   set_max_area 5000
module cell_top (input logic clk, a, output logic y);
  always_ff @(posedge clk) y <= ~a;
endmodule
```

```python
def cell_area(feature_um: float, base_area_um2: float = 4.0) -> float:
    # smaller feature -> quadratically smaller area for the same function
    return base_area_um2 * feature_um**2
```

> **Practical insight:** designers almost never draw transistor rectangles
> today - they use **standard cells** that are already DRC/LVS-clean. But
> understanding layers and rules explains *why* wires have delay, why density is
> limited, and why DRC/LVS failures block tape-out.

**Next:** make the inverter VTC and noise margins concrete in code.
""",
        ),
        _code(
            "Lab: CMOS inverter VTC & noise margins",
            "14 min",
            """\
# Sweep a CMOS inverter and extract its VTC, switching point, gain, and
# noise margins. We model each transistor's current with the simple
# long-channel square law and balance the pull-up vs pull-down currents.
import numpy as np
import matplotlib.pyplot as plt

VDD = 3.3
Vtn = 0.6        # NMOS threshold
Vtp = 0.6        # |PMOS threshold|
kn = 1.0         # NMOS transconductance (relative)
kp = 1.0         # PMOS transconductance (balanced design)

vin = np.linspace(0, VDD, 600)

# For each Vin, solve for Vout where I_pull-down == I_pull-up.
# I_n drives Vout toward 0, I_p drives Vout toward VDD. We sweep a candidate
# Vout grid and pick the balance point (module-level vectorized search).
vout_grid = np.linspace(0, VDD, 600)
VTC = np.zeros_like(vin)
for i in range(vin.size):
    vgn = vin[i]               # NMOS gate-source
    vgp = VDD - vin[i]         # PMOS source-gate
    # saturation-region drive currents (clamped at 0 below threshold)
    idn = kn * np.maximum(0.0, vgn - Vtn) ** 2
    idp = kp * np.maximum(0.0, vgp - Vtp) ** 2
    # NMOS conducts more -> output low; balance sets Vout
    # model Vout as VDD * idp / (idn + idp) (a smooth current divider)
    denom = idn + idp
    VTC[i] = VDD * idp / denom if denom > 1e-9 else VDD * (1 - vin[i] / VDD)

# Slope (gain) of the VTC; unity-gain points define VIL and VIH.
gain = np.gradient(VTC, vin)
unity = np.where(np.abs(gain) >= 1.0)[0]
VIL = vin[unity[0]]
VIH = vin[unity[-1]]
VOH = VTC[unity[0]]      # output high at VIL
VOL = VTC[unity[-1]]     # output low at VIH
NMH = VOH - VIH
NML = VIL - VOL
Vm = vin[np.argmin(np.abs(VTC - vin))]   # switching threshold (Vout == Vin)

plt.figure(figsize=(7, 4.5))
plt.plot(vin, VTC, color="#2563eb", lw=2, label="VTC: Vout(Vin)")
plt.plot([0, VDD], [0, VDD], "--", color="#94a3b8", label="Vout = Vin")
plt.axvline(VIL, color="#16a34a", ls=":", label=f"VIL={VIL:.2f}")
plt.axvline(VIH, color="#dc2626", ls=":", label=f"VIH={VIH:.2f}")
plt.xlabel("input Vin (V)")
plt.ylabel("output Vout (V)")
plt.title(f"CMOS inverter VTC (Vm={Vm:.2f} V)")
plt.legend(fontsize=8)
plt.grid(True)
plt.show()

print(f"switching threshold Vm = {Vm:.3f} V")
print(f"VIL = {VIL:.3f} V, VIH = {VIH:.3f} V")
print(f"VOH = {VOH:.3f} V, VOL = {VOL:.3f} V")
print(f"noise margin high NMH = {NMH:.3f} V")
print(f"noise margin low  NML = {NML:.3f} V")

# Try it yourself:
#   1. Set kp = 2.0 (weaker-looking PMOS compensated): Vm shifts.
#   2. Lower VDD to 1.2: noise margins shrink (why low voltage is hard).
""",
        ),
    ),
)


# -- VLSI & IC Design -- Intermediate ------------------------------------------

_VLSI_INTERMEDIATE = SeedCourse(
    slug="vlsi-intermediate",
    title="VLSI & IC Design -- Intermediate: Timing, Power & Datapath",
    description=(
        "What makes chips fast and efficient: RC delay and logical effort, the "
        "critical path and setup/hold, dynamic/short-circuit/leakage power, "
        "interconnect and repeaters, arithmetic datapath (adders, multipliers), "
        "and memory (SRAM/DRAM/ROM) - with dual SystemVerilog/Python, "
        "interactive plots, and a runnable delay/power lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Delay & timing: RC model, logical effort & setup/hold",
            "13 min",
            """\
# Delay & timing: RC model, logical effort & setup/hold

Speed is the currency of VLSI. To make a chip fast you must understand what makes
a gate slow.

## The RC delay model

A gate's output drives a capacitance through an on-resistance. To first order the
propagation delay is

$$t_{pd} \\approx 0.69\\,R\\,C,$$

where $R$ is the driving transistor's on-resistance and $C$ is the load it must
charge (the next gates' gates plus wire). Bigger load = slower; stronger
(wider) driver = smaller $R$ = faster, but a wider driver is itself a bigger load
for whatever drives *it*. That tension is the heart of sizing.

Slide the load capacitance and watch delay grow linearly:

```plot
{"title": "Gate delay vs load capacitance (t = 0.69 R C, slide R)", "xLabel": "load capacitance C (fF)", "yLabel": "delay (ps)", "xRange": [0, 100], "yRange": [0, 200], "grid": true, "controls": [{"name": "R", "range": [1, 4], "value": 2, "label": "driver on-resistance (kohm)"}], "functions": [{"expr": "0.69*R*x", "label": "t_pd"}]}
```

## Logical effort

**Logical effort** is a clean way to reason about sizing and the number of
stages. The delay of a stage is

$$d = g\\,h + p,$$

where $g$ is the **logical effort** (how much harder a gate is to drive than an
inverter: INV=1, NAND2=4/3, NOR2=5/3), $h$ is the **electrical effort**
(fanout = $C_{out}/C_{in}$), and $p$ is the parasitic delay. For a path, delay is
minimized when **each stage carries equal effort** $\\hat{f} = (G H)^{1/N}$, and
the best number of stages makes $\\hat{f} \\approx 4$ (the famous "fanout-of-4").

## The critical path

A chip's clock is limited by its **slowest** combinational path between
registers - the **critical path**. You speed up a design by finding that path and
shortening it (resizing gates, restructuring logic, pipelining). Everything else
has slack.

## Setup and hold

A flip-flop needs the data **stable** around the clock edge:

- **Setup time** $t_{su}$ - data must arrive *before* the edge. Violated by a
  path that is **too slow** -> raise the clock period or speed up logic.
- **Hold time** $t_h$ - data must stay *after* the edge. Violated by a path that
  is **too fast** (a short path) -> add delay. Hold violations do **not** go away
  by slowing the clock, which makes them nasty.

$$T \\ge t_{cq} + t_{logic} + t_{su}, \\qquad t_{cq} + t_{logic,min} \\ge t_h.$$

```systemverilog
// A two-stage pipeline shortens the critical path between flops.
module pipe (input logic clk, input logic [7:0] a, b,
             output logic [8:0] s);
  logic [7:0] ar, br;
  always_ff @(posedge clk) begin
    ar <= a; br <= b;       // stage 1
    s  <= ar + br;          // stage 2 (shorter combinational path)
  end
endmodule
```

```python
def stage_delay(g: float, h: float, p: float) -> float:
    return g * h + p  # logical-effort stage delay d = g*h + p
```

**Next:** the energy side of the ledger - power.
""",
        ),
        _t(
            "Power in CMOS: dynamic, short-circuit & leakage",
            "12 min",
            """\
# Power in CMOS: dynamic, short-circuit & leakage

A static CMOS gate draws little *static* current - but a billion of them
switching fast still burns watts. Total power has three parts:

$$P = \\underbrace{\\alpha C V_{DD}^2 f}_{\\text{dynamic}} + \\underbrace{P_{sc}}_{\\text{short-circuit}} + \\underbrace{V_{DD} I_{leak}}_{\\text{leakage (static)}}.$$

## 1. Dynamic (switching) power

Every time an output charges its load to $V_{DD}$ and back, it dissipates
$C V_{DD}^2$ of energy. With activity factor $\\alpha$ (fraction of cycles a node
switches) at frequency $f$:

$$P_{dyn} = \\alpha\\,C\\,V_{DD}^2\\,f.$$

The **$V_{DD}^2$** dependence is the single most important lever in low-power
design: halving the voltage quarters the dynamic power. Slide $V_{DD}$:

```plot
{"title": "Dynamic power vs supply voltage (P = a C VDD^2 f, slide activity)", "xLabel": "supply voltage VDD (V)", "yLabel": "dynamic power (relative)", "xRange": [0.5, 1.5], "yRange": [0, 12], "grid": true, "controls": [{"name": "alpha", "range": [0.1, 1], "value": 0.5, "label": "activity factor"}], "functions": [{"expr": "alpha*5*x*x", "label": "P_dyn"}]}
```

## 2. Short-circuit power

During an input transition, both the PUN and PDN are briefly on at once, so a
small current flows straight through. Fast (sharp) input edges minimize it;
typically a few percent of total power.

## 3. Leakage (static) power

Even when "off," a MOSFET leaks **subthreshold** current that rises
*exponentially* as the threshold $V_{th}$ drops. Modern nodes leak a lot, and
leakage **dominates** when a chip is idle. It also rises steeply with
temperature. Slide $V_{th}$ and watch leakage explode at low thresholds:

```plot
{"title": "Subthreshold leakage vs threshold voltage (slide temperature)", "xLabel": "threshold Vth (V)", "yLabel": "leakage current (relative)", "xRange": [0.1, 0.6], "yRange": [0, 12], "grid": true, "controls": [{"name": "Tfac", "range": [0.5, 2], "value": 1, "label": "temperature factor"}], "functions": [{"expr": "10*exp(-(x - 0.1)/(0.08*Tfac))", "label": "I_leak"}]}
```

## Power gating

The fix for idle leakage is **power gating**: insert a big "sleep" transistor
that disconnects a block from the supply when it is not in use, cutting its
leakage to nearly zero. It is a cornerstone of phone-chip battery life.

```systemverilog
// A clock-enable cuts dynamic power on an idle register (clock gating idea).
module gated_reg (input logic clk, en, input logic [7:0] d,
                  output logic [7:0] q);
  always_ff @(posedge clk)
    if (en) q <= d;     // synthesis can map to a clock-gated register
endmodule
```

```python
def dynamic_power(alpha: float, C: float, vdd: float, f: float) -> float:
    return alpha * C * vdd**2 * f  # the VDD^2 lever dominates
```

> **Practical insight:** dynamic power says "lower the voltage and clock only
> what you need"; leakage says "raise the threshold or power-gate idle blocks."
> Modern design juggles both with multi-Vt cells and power domains (Advanced).

**Next:** the wires that connect it all - interconnect delay.
""",
        ),
        _t(
            "Interconnect & wire delay",
            "12 min",
            """\
# Interconnect & wire delay

For decades, transistors got faster every generation - but **wires did not**. In
modern chips, interconnect delay often dominates, and a big part of physical
design is fighting it.

## Wires are distributed RC

A wire has resistance per unit length and capacitance to its neighbors and to the
substrate. A wire of length $L$ has $R \\propto L$ and $C \\propto L$, so its
intrinsic delay grows as

$$t_{wire} \\propto R C \\propto L^2.$$

That **quadratic** in length is the problem: double the wire, quadruple the
delay. Slide a per-length factor and watch wire delay blow up with length:

```plot
{"title": "Wire delay grows with the square of length (slide RC per length)", "xLabel": "wire length (mm)", "yLabel": "wire delay (ps)", "xRange": [0, 5], "yRange": [0, 200], "grid": true, "controls": [{"name": "rc", "range": [2, 12], "value": 6, "label": "RC per mm^2 factor"}], "functions": [{"expr": "rc*x*x", "label": "t_wire ~ L^2"}]}
```

## Repeaters break the quadratic

Insert **buffers (repeaters)** along a long wire to chop it into shorter
segments. With $k$ equal segments the delay becomes roughly linear in $L$ instead
of quadratic (each segment is $L/k$, and there are $k$ of them):

$$t \\approx k\\left(t_{buf} + r c (L/k)^2\\right),$$

which you minimize by choosing the optimal number and size of repeaters. Long
buses, clock lines, and reset nets are full of inserted repeaters.

## Scaling makes it worse

As features shrink, wires get thinner and closer, so resistance per length
**rises** and coupling capacitance grows - while gate delays fall. The crossover
is why interconnect, not the transistor, sets the pace on advanced nodes, and why
chips use **many metal layers** (thick, low-resistance layers up top for global
routing and the power grid; thin dense layers below for local connections).

```mermaid
flowchart LR
  SRC["driver"] --> W1["wire seg"] --> B1["repeater"] --> W2["wire seg"] --> B2["repeater"] --> SINK["load"]
```

```systemverilog
// You don't write repeaters in RTL - the tool inserts them. But you can
// pipeline a long on-chip link to hide its latency:
module link (input logic clk, input logic [7:0] d, output logic [7:0] q);
  logic [7:0] hop1, hop2;
  always_ff @(posedge clk) begin
    hop1 <= d; hop2 <= hop1; q <= hop2;  // 3-cycle pipelined wire
  end
endmodule
```

```python
def wire_delay(length_mm: float, rc_per_mm2: float = 6.0) -> float:
    return rc_per_mm2 * length_mm**2  # unbuffered: quadratic in length
```

> **Practical insight:** "it met timing in synthesis but fails after place and
> route" almost always means **wire delay** the early estimate missed. Floorplan
> to keep communicating blocks close, and let the tool insert repeaters.

**Next:** building arithmetic - adders and multipliers.
""",
        ),
        _t(
            "Arithmetic & datapath in VLSI",
            "12 min",
            """\
# Arithmetic & datapath in VLSI

The **datapath** is the part of a chip that does arithmetic - adders,
multipliers, shifters, comparators - arranged in regular, bit-sliced columns.
Datapath design is a constant trade of **area** against **delay** against
**power**.

## Adders: the ripple-carry vs the fast adder

A **ripple-carry adder** chains full adders; the carry ripples from bit 0 to bit
$n-1$, so its delay grows **linearly** with width $n$. Simple and small, but slow
for wide words.

A **carry-lookahead** (or carry-select, or prefix) adder computes carries in
parallel, cutting delay to roughly **logarithmic** in $n$ - at the cost of more
area. Compare the delay scaling:

```plot
{"title": "Adder delay vs word width: ripple (linear) vs lookahead (log)", "xLabel": "word width n (bits)", "yLabel": "delay (gate delays)", "xRange": [1, 64], "yRange": [0, 70], "grid": true, "functions": [{"expr": "x", "label": "ripple-carry (~n)", "color": "#dc2626"}, {"expr": "4*log2(x) + 2", "label": "carry-lookahead (~log n)", "color": "#2563eb"}]}
```

## Multipliers

A multiplier forms partial products and sums them. An **array multiplier** is a
regular grid (easy to lay out, $O(n)$ delay); a **Wallace/Dadda tree** reduces
the partial products in $O(\\log n)$ using carry-save adders, then a final fast
adder. Booth encoding halves the number of partial products. Multipliers are
often the largest, hottest blocks in a DSP or CPU - which is why much of
machine-learning hardware is "just" arrays of small multipliers.

## Layout tradeoffs

Datapaths are laid out as **bit-sliced** regular arrays so wiring is short and
repeatable; control logic is synthesized as random logic. The choice of adder or
multiplier architecture is a direct **area-delay-power** trade: a faster adder
costs area and (usually) power.

```systemverilog
// Let synthesis pick the adder architecture from your timing constraint.
module add16 (input  logic [15:0] a, b,
              input  logic        cin,
              output logic [15:0] sum,
              output logic        cout);
  assign {cout, sum} = a + b + cin;   // tool maps to ripple/CLA per timing
endmodule
```

```python
def ripple_carry_delay(n: int, fa_delay: float = 1.0) -> float:
    return n * fa_delay  # carry ripples bit by bit -> O(n)
```

> **Practical insight:** never hand-build a generic adder - write `a + b` and let
> synthesis choose the architecture to meet timing. Hand-craft only the special
> blocks (a 1024-bit multiplier, a crypto unit) where the tool needs help.

**Next:** where the bits live - memory.
""",
        ),
        _t(
            "Memory design: SRAM, DRAM, ROM & sense amplifiers",
            "12 min",
            """\
# Memory design: SRAM, DRAM, ROM & sense amplifiers

Most of a modern chip's *transistors* are **memory**. Memory is laid out as dense
**arrays** of identical cells addressed by rows (word lines) and columns (bit
lines), and the cell design dominates density, speed, and power.

## The 6T SRAM cell

Static RAM stores one bit in **cross-coupled inverters** (a latch) plus two
access transistors - **six transistors** total:

```mermaid
flowchart LR
  WL["word line"] --> AL["access L"]
  WL --> AR["access R"]
  AL --> Q(("Q"))
  AR --> QB(("Q-bar"))
  Q --> INV1["inverter"] --> QB
  QB --> INV2["inverter"] --> Q
```

- **Read/write** by driving the word line and the two **bit lines** (BL, BL-bar).
- It is **static**: holds its value as long as power is on, no refresh.
- Fast and robust, but **6 transistors per bit** makes it area-hungry - which is
  why caches (L1/L2/L3) are SRAM and are a huge fraction of a CPU's die area.

Sizing the cell is a careful balance of **read stability** (don't flip the bit
while reading) against **writeability** (be able to flip it on a write) against
area - the SRAM "butterfly" margins.

## DRAM

Dynamic RAM stores a bit as charge on a tiny capacitor with **one transistor**
(1T1C) - far denser, which is why main memory is DRAM. But the charge **leaks**,
so DRAM must be **refreshed** every few milliseconds, and reads are
**destructive** (you must write the value back).

## ROM

Read-only memory bakes its contents into the layout (presence/absence of a
transistor at each cross-point) - dense and nonvolatile, used for boot code and
constants. Flash/EEPROM add reprogrammability.

## Sense amplifiers

Bit lines are long and heavily loaded, so a read only nudges them by a tiny
**$\\Delta V$**. A **sense amplifier** is a fast differential comparator that
amplifies that small difference into a full logic level quickly. The bigger the
swing you wait for, the slower the read - sense amps let you decide early. Slide
the sensing threshold and see how a smaller required swing speeds the read:

```plot
{"title": "Bit-line develops a small delta-V; sense amp decides early", "xLabel": "time (ns)", "yLabel": "bit-line difference (mV)", "xRange": [0, 3], "yRange": [0, 220], "grid": true, "controls": [{"name": "thresh", "range": [20, 200], "value": 100, "label": "sense threshold (mV)"}], "functions": [{"expr": "200*(1 - exp(-x/0.8))", "label": "delta-V(t)"}, {"expr": "0*x + thresh", "label": "sense threshold", "color": "#dc2626"}]}
```

```systemverilog
// Inferred memory: synthesis maps this to a RAM macro or flops.
module ram16x8 (input logic clk, we, input logic [3:0] addr,
                input logic [7:0] din, output logic [7:0] dout);
  logic [7:0] mem [0:15];
  always_ff @(posedge clk) begin
    if (we) mem[addr] <= din;
    dout <= mem[addr];
  end
endmodule
```

```python
def sense_time(target_mv: float, tau_ns: float = 0.8, swing_mv: float = 200.0) -> float:
    import math
    # time for the bit-line difference to reach the sense threshold
    return -tau_ns * math.log(1.0 - target_mv / swing_mv)
```

> **Practical insight:** memory is a separate craft from logic. You usually
> **instantiate vendor memory macros** (compiled SRAM, DRAM controllers) rather
> than draw cells, but knowing 6T vs 1T1C explains the cache-vs-DRAM hierarchy in
> every computer.

**Next:** put delay and power together in code.
""",
        ),
        _code(
            "Lab: delay & power vs supply voltage",
            "14 min",
            """\
# Explore the fundamental energy-delay trade in CMOS. As supply voltage VDD
# drops: dynamic power falls (~VDD^2) but gates get SLOWER (delay rises),
# and leakage stays. We sweep VDD and find the energy-per-operation sweet spot.
import numpy as np
import matplotlib.pyplot as plt

Vth = 0.4          # threshold voltage (V)
C = 1.0            # load capacitance (relative)
alpha = 0.3        # activity factor
k = 1.0            # drive strength constant
Ileak0 = 0.05      # leakage current scale (relative)

vdd = np.linspace(0.5, 1.5, 200)

# Gate delay ~ C*VDD / drive_current; drive ~ k*(VDD - Vth)^2 in saturation.
drive = k * np.maximum(0.01, (vdd - Vth)) ** 2
delay = C * vdd / drive                       # rises sharply as VDD -> Vth

# Frequency we could run at (1/delay), and dynamic power at that frequency.
freq = 1.0 / delay
p_dyn = alpha * C * vdd**2 * freq             # dynamic power
p_leak = Ileak0 * vdd                         # static (leakage) power
p_total = p_dyn + p_leak

# Energy per operation = power * delay (the metric to minimize).
energy_per_op = p_total * delay
best = np.argmin(energy_per_op)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(vdd, delay, color="#dc2626", label="gate delay")
ax[0].set_xlabel("supply VDD (V)")
ax[0].set_ylabel("delay (relative)")
ax[0].set_title("Delay rises as VDD -> Vth")
ax[0].grid(True)
ax[0].legend()

ax[1].plot(vdd, p_dyn, color="#2563eb", label="dynamic")
ax[1].plot(vdd, p_leak, color="#16a34a", label="leakage")
ax[1].plot(vdd, p_total, color="#111827", lw=2, label="total")
ax[1].axvline(vdd[best], color="#f59e0b", ls="--", label="min energy/op")
ax[1].set_xlabel("supply VDD (V)")
ax[1].set_ylabel("power (relative)")
ax[1].set_title("Power vs VDD")
ax[1].grid(True)
ax[1].legend()
plt.tight_layout()
plt.show()

print(f"min energy/op at VDD = {vdd[best]:.3f} V")
print(f"  delay there       = {delay[best]:.3f}")
print(f"  total power there = {p_total[best]:.3f}")
print(f"  energy/op         = {energy_per_op[best]:.4f}")

# Try it yourself:
#   1. Raise Vth to 0.6: delay explodes near low VDD, sweet spot shifts up.
#   2. Raise Ileak0 to 0.5 (leaky process): the energy minimum moves higher.
""",
        ),
    ),
)


# -- VLSI & IC Design -- Advanced ----------------------------------------------

_VLSI_ADVANCED = SeedCourse(
    slug="vlsi-advanced",
    title="VLSI & IC Design -- Advanced: Low-Power, Physical Design & Test",
    description=(
        "The advanced craft of modern chips: low-power design (DVFS, clock "
        "gating, multi-Vt, power domains, UPF), clocking and distribution "
        "(clock trees, skew, jitter, PLLs), physical design and signoff "
        "(floorplanning, CTS, STA, extraction), design-for-test (scan, BIST, "
        "ATPG), and analog/mixed-signal plus advanced nodes (FinFET, SoC, "
        "chiplets, 3D-IC) - with dual SystemVerilog/Python, interactive plots, "
        "a runnable scaling lab, and a closing applications lesson."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Low-power design: DVFS, clock gating, multi-Vt & power domains",
            "13 min",
            """\
# Low-power design: DVFS, clock gating, multi-Vt & power domains

Power, not transistors, is the limiter on modern chips ("the power wall"). A
whole discipline exists to spend energy only where and when it is needed.

## DVFS - dynamic voltage and frequency scaling

Because $P_{dyn} = \\alpha C V_{DD}^2 f$ and a lower voltage also forces a lower
$f$, running slower at a lower voltage saves power **cubically** for a given task
spread out in time. DVFS picks an operating point per workload: a phone races to
finish, then drops to a low-voltage idle. Slide the voltage/frequency operating
point:

```plot
{"title": "DVFS: power vs operating point (lower V and f save big)", "xLabel": "relative frequency f", "yLabel": "power (relative)", "xRange": [0.3, 1], "yRange": [0, 12], "grid": true, "controls": [{"name": "vmin", "range": [0.6, 1], "value": 0.7, "label": "min voltage floor"}], "functions": [{"expr": "10*x*(vmin + (1 - vmin)*x)^2", "label": "P ~ f * V(f)^2"}]}
```

(Voltage scales roughly with frequency, so power falls faster than linearly.)

## Clock gating

The clock network itself is one of the biggest dynamic-power consumers because it
toggles every cycle, everywhere. **Clock gating** shuts off the clock to idle
registers, eliminating their switching power. Synthesis inserts integrated
clock-gating cells automatically when it sees an enable.

## Multi-Vt

Foundries offer cells at several **threshold voltages**:

- **Low-Vt (LVT)** - fast but leaky. Use only on the critical path.
- **High-Vt (HVT)** - slow but low-leakage. Use everywhere with slack.

Tools swap in HVT cells off the critical path to cut leakage with no speed loss -
the cheapest leakage win there is.

## Power domains and UPF

A chip is partitioned into **power domains** that can be at different voltages, or
switched off entirely (power gating with sleep transistors). Crossing a domain
boundary needs **level shifters** (voltage change) and **isolation cells** (so a
powered-down output does not float into a live block). The intent is captured in
**UPF** (Unified Power Format) - a side file telling the tools the supplies,
switches, level shifters, and isolation, kept separate from the RTL.

```mermaid
flowchart LR
  ALWAYS["always-on domain"] -->|isolation + level shift| GATED["switchable domain"]
  PMU["power manager"] -->|enable| SW["sleep transistor"]
  SW --> GATED
```

```systemverilog
// RTL stays power-agnostic; intent lives in UPF, but enables enable gating:
module core (input logic clk, en, rst_n, input logic [7:0] d,
             output logic [7:0] q);
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) q <= '0;
    else if (en) q <= d;   // 'en' lets the tool clock-gate this register
endmodule
```

```python
def dvfs_power(f_rel: float, vmin: float = 0.7) -> float:
    v = vmin + (1 - vmin) * f_rel     # voltage tracks frequency
    return f_rel * v**2               # power ~ f * V^2
```

> **Practical insight:** the big wins stack - DVFS + clock gating + multi-Vt +
> power gating together cut a phone SoC's power by an order of magnitude versus a
> naive design. UPF lets you describe all of it without touching functional RTL.

**Next:** the clock that drives it all.
""",
        ),
        _t(
            "Clocking & clock distribution: trees, skew, jitter & PLLs",
            "13 min",
            """\
# Clocking & clock distribution: trees, skew, jitter & PLLs

A synchronous chip is only as good as its clock. Getting one clean edge to
millions of flip-flops at (nearly) the same instant is one of physical design's
hardest jobs.

## The clock tree

You cannot drive millions of loads from one buffer, so the clock is distributed
through a balanced **tree** (or an **H-tree**, or a mesh/grid for the highest
performance) of buffers, sized so every leaf flip-flop sees a similar delay and
edge rate.

```mermaid
flowchart TB
  ROOT["clock source"] --> B1["buffer"]
  B1 --> B2["buffer"]
  B1 --> B3["buffer"]
  B2 --> L1["flops"]
  B2 --> L2["flops"]
  B3 --> L3["flops"]
  B3 --> L4["flops"]
```

## Skew

**Clock skew** is the difference in clock arrival time between two flops. It eats
into the timing budget two ways:

$$T \\ge t_{cq} + t_{logic} + t_{su} + t_{skew}, \\qquad t_{cq} + t_{logic,min} \\ge t_h + t_{skew}.$$

Positive skew toward the capturing flop *helps* setup but *hurts* hold - skew is a
double-edged sword, and uncontrolled skew causes silicon that simply does not
work. Slide skew and watch the usable timing window shrink:

```plot
{"title": "Usable data window shrinks with clock skew (period T=2 ns)", "xLabel": "clock skew (ns)", "yLabel": "usable logic budget (ns)", "xRange": [0, 1], "yRange": [0, 2], "grid": true, "controls": [{"name": "T", "range": [1, 3], "value": 2, "label": "clock period (ns)"}], "functions": [{"expr": "max(0, T - 0.15 - 0.05 - x)", "label": "budget = T - tcq - tsu - skew"}]}
```

## Jitter

**Jitter** is the cycle-to-cycle wobble in the clock edge's timing (from supply
noise, the PLL, thermal noise). Unlike skew (a fixed spatial offset), jitter is
random and must be subtracted from every cycle's budget. Together skew + jitter
are the clock **uncertainty** that signoff pads the period with.

## PLLs

A **phase-locked loop** multiplies a clean low-frequency reference (a crystal) up
to the GHz on-chip clock and locks its phase to the reference. A
phase-frequency detector compares reference and feedback, a loop filter
integrates the error, and a **voltage-controlled oscillator** generates the
output - a feedback control loop (see the Control track) that settles to lock.
Press Play to watch a PLL's frequency error decay as it acquires lock:

```plot
{"title": "PLL lock acquisition: phase error decays to zero (press Play)", "xLabel": "time (relative)", "yLabel": "phase error", "xRange": [0, 10], "yRange": [-1.1, 1.1], "grid": true, "controls": [{"name": "bw", "range": [0.3, 1.5], "value": 0.7, "label": "loop bandwidth"}], "animate": {"param": "t", "range": [0, 10], "label": "time"}, "functions": [{"expr": "exp(-bw*x)*cos(3*x)", "label": "phase error(t)"}], "points": [{"xExpr": "t", "yExpr": "exp(-bw*t)*cos(3*t)", "label": "now", "color": "#dc2626", "size": 6, "trail": true}]}
```

```systemverilog
// Clock-domain crossing needs a synchronizer; never sample async data raw.
module sync2 (input logic clk, input logic async_in, output logic clean_out);
  logic meta;
  always_ff @(posedge clk) begin
    meta      <= async_in;   // first flop may go metastable
    clean_out <= meta;       // second flop resolves it
  end
endmodule
```

```python
def setup_budget(period_ns: float, tcq=0.15, tsu=0.05, skew=0.0, jitter=0.0) -> float:
    # logic delay budget left after clocking overheads
    return period_ns - tcq - tsu - skew - jitter
```

> **Practical insight:** crossing between clock domains (different frequencies or
> phases) is where metastability bugs hide - always use a **2-flop synchronizer**
> or an async FIFO. And budget for skew + jitter; the clock is never perfect.

**Next:** turning a netlist into manufacturable layout - physical design.
""",
        ),
        _t(
            "Physical design & signoff",
            "13 min",
            """\
# Physical design & signoff

**Physical design** turns the synthesized gate netlist into a real, manufacturable
layout, then **signoff** proves it will work. This is where timing, power, and
geometry all become concrete.

## The physical-design flow

```mermaid
flowchart LR
  NETLIST["gate netlist"] --> FP["floorplan"]
  FP --> PLACE["placement"]
  PLACE --> CTS["clock-tree synthesis"]
  CTS --> ROUTE["routing"]
  ROUTE --> EXT["parasitic extraction"]
  EXT --> STA["static timing analysis"]
  STA --> SIGN["signoff (DRC/LVS, power, IR)"]
```

## Floorplanning

Decide where the big blocks, memory macros, and I/O pads go, and lay down the
**power grid**. A good floorplan keeps communicating blocks close (short wires =
less delay and power) and leaves room for routing. Floorplanning early mistakes
are the most expensive to fix.

## Clock-tree synthesis (CTS)

Build the balanced clock tree discussed in the clocking lesson, minimizing skew
and meeting the clock's edge-rate targets. CTS happens after placement (it needs
to know where the flops are) and before final routing.

## Static timing analysis (STA)

**STA** checks *every* path's timing **without simulating vectors** - it
propagates worst-case delays and verifies setup and hold on all paths across
**corners** (process/voltage/temperature: slow-cold, fast-hot, etc.). It reports
**slack** = required time - arrival time; **negative slack** is a violation. STA
is exhaustive and fast, which is why it - not simulation - signs off timing.

A path's slack worsens as the clock period tightens; below a critical period it
goes negative (fails). Slide the clock period:

```plot
{"title": "Setup slack vs clock period (negative = timing FAIL)", "xLabel": "path delay (ns)", "yLabel": "setup slack (ns)", "xRange": [0.5, 4], "yRange": [-2, 2], "grid": true, "controls": [{"name": "period", "range": [1, 4], "value": 2.5, "label": "clock period (ns)"}], "functions": [{"expr": "period - 0.2 - x", "label": "slack = T - overhead - path"}, {"expr": "0*x", "label": "fail line", "color": "#dc2626"}]}
```

## Parasitic extraction

After routing, **extraction** measures the actual R and C of every wire (into a
SPEF file). Re-running STA with these *real* parasitics is what catches the "met
timing in synthesis, fails after route" surprises from the interconnect lesson.

## Signoff

The final gate: **timing** (STA, all corners), **physical** (DRC/LVS),
**power/IR-drop** (the supply grid must deliver current without sagging),
**electromigration**, and **signal integrity** (crosstalk). Pass all, and you
**tape out** to GDSII.

```systemverilog
// Constraints (SDC) drive physical design - the clock and I/O timing:
//   create_clock -period 2.5 -name clk [get_ports clk]
//   set_input_delay 0.4 -clock clk [all_inputs]
//   set_output_delay 0.4 -clock clk [all_outputs]
module top (input logic clk, input logic [7:0] a, output logic [7:0] y);
  always_ff @(posedge clk) y <= a + 8'd1;
endmodule
```

```python
def setup_slack(period_ns: float, path_ns: float, overhead_ns: float = 0.2) -> float:
    return period_ns - overhead_ns - path_ns  # negative slack = timing fail
```

> **Practical insight:** "timing closure" - iterating physical design until STA is
> clean at all corners with margin - is where most of a chip's schedule goes.
> Good floorplanning and realistic constraints up front save weeks later.

**Next:** proving the silicon works - design for test.
""",
        ),
        _t(
            "Design for test: scan, BIST, ATPG & fault coverage",
            "12 min",
            """\
# Design for test: scan, BIST, ATPG & fault coverage

A chip that works in simulation can still come back from the fab with
**manufacturing defects** - a shorted via, an open wire. **Design for test
(DFT)** builds in structures to find those defects cheaply on a tester, because
you cannot probe a billion internal nodes.

## The fault model

DFT abstracts physical defects into a tractable model - most commonly the
**stuck-at fault**: a node permanently stuck at 0 or 1. A 100k-gate block has
~200k stuck-at faults (each node stuck-at-0 and stuck-at-1); the goal is a set of
test patterns that **detects** as many as possible.

## Scan chains

Ordinary flip-flops are not observable or controllable from the pins. **Scan**
replaces them with **scan flops** that, in test mode, chain together into one
giant **shift register**:

```mermaid
flowchart LR
  SI["scan-in pin"] --> FF1["scan FF"] --> FF2["scan FF"] --> FF3["scan FF"] --> SO["scan-out pin"]
```

To test: **shift in** a known state, pulse the clock once (let the logic compute),
then **shift out** the captured result and compare. Scan turns the impossible
"observe every internal flop" into a simple shift-in/shift-out.

## ATPG

**Automatic Test Pattern Generation** is a tool that, given the netlist and fault
model, computes the minimal set of scan patterns that detects the faults. More
patterns = higher coverage but longer (costlier) test time.

## Fault coverage

**Fault coverage** is the fraction of modeled faults the patterns detect. High
coverage (often 99%+) is required because **undetected** faults mean defective
chips ship. Coverage rises with pattern count but with diminishing returns:

```plot
{"title": "Fault coverage vs number of test patterns (diminishing returns)", "xLabel": "test patterns (thousands)", "yLabel": "fault coverage (%)", "xRange": [0, 20], "yRange": [0, 100], "grid": true, "controls": [{"name": "rate", "range": [0.2, 1], "value": 0.5, "label": "pattern effectiveness"}], "functions": [{"expr": "100*(1 - exp(-rate*x))", "label": "coverage"}]}
```

## BIST

**Built-In Self-Test** puts the test *on the chip*: an on-chip pattern generator
(often an LFSR) stimulates the logic or memory, and a **signature analyzer**
compresses the responses into one signature compared against the golden value.
**MBIST** (memory BIST) is standard for the SRAM/DRAM arrays, which scan cannot
test well. BIST enables fast, at-speed, in-field testing with little tester
support.

```systemverilog
// A scan flop in test mode selects the scan-in path over functional data.
module scan_ff (input logic clk, test_en, d, scan_in,
                output logic q);
  always_ff @(posedge clk)
    q <= test_en ? scan_in : d;   // shift in test mode, compute in functional
endmodule
```

```python
def fault_coverage(patterns_k: float, rate: float = 0.5) -> float:
    import math
    return 100.0 * (1.0 - math.exp(-rate * patterns_k))  # diminishing returns
```

> **Practical insight:** DFT is not optional - test cost and yield directly hit
> the bottom line. Budget scan, MBIST, and coverage targets from the start;
> retrofitting test into a finished design is painful and never as good.

**Next:** the analog edges and the most advanced silicon.
""",
        ),
        _t(
            "Analog/mixed-signal & advanced nodes: FinFET, SoC, chiplets & 3D-IC",
            "12 min",
            """\
# Analog/mixed-signal & advanced nodes: FinFET, SoC, chiplets & 3D-IC

Real chips are not pure digital. They mix analog and digital, ride the most
advanced transistors, and increasingly stop being a single die at all.

## Analog and mixed-signal

Sensors, radios, and power are inherently **analog**. A **mixed-signal** chip
combines analog front-ends (amplifiers, **ADCs/DACs**, PLLs, references,
regulators) with a digital core. Analog does not shrink or port like digital -
it is hand-crafted, matching-sensitive, and noise-sensitive, so isolating it from
the noisy digital switching (separate supplies, guard rings, careful floorplan) is
a central mixed-signal challenge.

## FinFET and advanced transistors

As planar MOSFETs shrank, leakage and short-channel effects grew unmanageable.
The **FinFET** wraps the gate around a thin vertical fin on three sides, giving far
better electrostatic control - less leakage, lower voltage, higher speed. Beyond
FinFET come **gate-all-around / nanosheet** transistors (the gate fully surrounds
the channel). These device innovations are what kept scaling alive past ~22 nm.

The intrinsic delay of a CMOS stage scales with its parameters; as nodes shrink,
delay falls but leakage pressure rises (slide a scaling factor):

```plot
{"title": "Relative gate delay across process generations (slide node scale)", "xLabel": "process node (relative, smaller = newer)", "yLabel": "gate delay (relative)", "xRange": [0.3, 1], "yRange": [0, 12], "grid": true, "controls": [{"name": "vfac", "range": [0.7, 1], "value": 0.85, "label": "voltage scaling"}], "functions": [{"expr": "10*x/vfac", "label": "delay ~ node / Vscale"}]}
```

## SoC, chiplets and 3D-IC

- **SoC (System-on-Chip)** - integrate CPU, GPU, memory controllers, radios, and
  accelerators on one die. Built by composing reusable **IP blocks** over standard
  on-chip buses/networks (AXI, NoC). Your phone is an SoC.
- **Chiplets** - instead of one huge die, build several smaller dies (each on its
  best-suited process) and connect them in a package over a die-to-die link. Better
  yield (small dies have fewer defects) and mix-and-match nodes - the strategy
  behind modern CPUs and GPUs.
- **3D-IC** - stack dies vertically with **through-silicon vias (TSVs)**, putting
  memory right on top of logic for huge bandwidth at low energy. High-bandwidth
  memory (HBM) on AI accelerators is the headline example.

```mermaid
flowchart LR
  CPU["CPU chiplet"] --> INT["interposer / die-to-die link"]
  GPU["GPU chiplet"] --> INT
  IO["I/O chiplet"] --> INT
  INT --> HBM["stacked HBM (3D)"]
```

```systemverilog
// An SoC composes IP blocks over a standard bus interface.
module soc_top (input logic clk, rst_n);
  cpu      u_cpu  (.clk, .rst_n);
  accel    u_acc  (.clk, .rst_n);
  mem_ctrl u_mem  (.clk, .rst_n);
  // ...wired together by an AXI/NoC fabric
endmodule
```

```python
def yield_gain(die_area_rel: float, defect_density: float = 0.5) -> float:
    import math
    # smaller dies (chiplets) yield better: simple Poisson yield model
    return math.exp(-defect_density * die_area_rel)
```

> **Practical insight:** the industry's growth now comes as much from
> **packaging and integration** (chiplets, 3D, advanced packaging) as from
> shrinking transistors. "More than Moore" - heterogeneous integration - is the
> frontier.

**Next:** run a scaling experiment yourself.
""",
        ),
        _code(
            "Lab: technology scaling of delay & power",
            "14 min",
            """\
# Model how delay, dynamic power, and energy-per-operation change as a process
# scales down. Classic 'constant-field' (Dennard) scaling shrinks dimensions
# and voltage by the same factor s>1; we compare it to the modern reality where
# voltage barely scales, so power density rises (the power wall).
import numpy as np
import matplotlib.pyplot as plt

# scaling factor s: each generation shrinks linear dimensions by 1/s.
s = np.linspace(1.0, 8.0, 200)

# Ideal Dennard scaling (per device, relative to the s=1 baseline):
#   dimensions ~ 1/s, voltage ~ 1/s, so:
#   capacitance C ~ 1/s, delay ~ 1/s, frequency f ~ s,
#   dynamic power/device ~ C*V^2*f ~ (1/s)(1/s^2)(s) = 1/s^2,
#   devices per area ~ s^2, so power DENSITY ~ constant. The Dennard gift.
C_dennard = 1.0 / s
V_dennard = 1.0 / s
f_dennard = s
p_dev_dennard = C_dennard * V_dennard**2 * f_dennard
density_dennard = p_dev_dennard * s**2          # per-area: stays flat

# Modern reality: voltage stops scaling (stuck near a floor ~ const).
V_modern = 1.0 / (1.0 + 0.15 * (s - 1.0))       # scales much more slowly
C_modern = 1.0 / s
f_modern = s
p_dev_modern = C_modern * V_modern**2 * f_modern
density_modern = p_dev_modern * s**2            # per-area: RISES -> power wall

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(s, 1.0 / s, color="#2563eb", label="gate delay ~ 1/s")
ax[0].plot(s, f_dennard, color="#16a34a", label="frequency ~ s")
ax[0].set_xlabel("scaling factor s")
ax[0].set_ylabel("relative")
ax[0].set_title("Devices get faster as they shrink")
ax[0].grid(True)
ax[0].legend()

ax[1].plot(s, density_dennard, color="#16a34a", lw=2, label="Dennard: density flat")
ax[1].plot(s, density_modern, color="#dc2626", lw=2, label="modern: density rises")
ax[1].set_xlabel("scaling factor s")
ax[1].set_ylabel("power density (relative)")
ax[1].set_title("The power wall: voltage stopped scaling")
ax[1].grid(True)
ax[1].legend()
plt.tight_layout()
plt.show()

print(f"at s=8 (8x shrink):")
print(f"  Dennard power density = {density_dennard[-1]:.2f} (flat by design)")
print(f"  modern  power density = {density_modern[-1]:.2f} (the power wall)")
print(f"  ratio modern/Dennard  = {density_modern[-1] / density_dennard[-1]:.1f}x")

# Try it yourself:
#   1. Make V_modern scale better (smaller 0.15 coefficient): density rises less.
#   2. This is exactly why chips went multi-core instead of ever-higher GHz.
""",
        ),
        _t(
            "Applications & the VLSI throughline",
            "11 min",
            """\
# Applications & the VLSI throughline

Everything in this track converges on real silicon. Here is where the ideas show
up in chips you use every day - and the throughline that ties them together.

## Where it all lands

- **Smartphone SoC (e.g. application processors).** A textbook integration of
  every topic: multi-core CPUs and a GPU (datapath + memory), aggressive
  **DVFS + clock gating + power gating + multi-Vt** for battery life, on-die
  SRAM caches, DRAM controllers, PLLs, and analog/RF front-ends - all on an
  advanced **FinFET** node, full of scan and MBIST for test.
- **CPUs and GPUs.** Deep pipelines (timing/critical-path engineering), huge
  SRAM cache hierarchies, fast adders and multipliers, elaborate clock trees, and
  now **chiplets** stitched over an interposer to beat the yield of one giant die.
- **AI accelerators (TPUs / NPUs).** Literally **arrays of multipliers** doing
  matrix multiply, fed by **HBM stacked in 3D** for bandwidth - the datapath and
  3D-IC lessons made into a product.
- **Memory chips.** DRAM and NAND flash are pure array-and-sense-amplifier design
  pushed to the density limit; the densest VLSI made.
- **FPGAs.** Reconfigurable seas of LUTs and DSP/RAM blocks - the **same RTL** you
  write, mapped to a fabric instead of standard cells, used for prototyping and
  low-volume, update-in-the-field systems.
- **Mixed-signal & sensors.** Image sensors, RF transceivers, power-management
  ICs, and the ADC/DAC bridges between the analog world and the digital core.

## The end-to-end picture

```mermaid
flowchart LR
  SPEC["spec"] --> RTL["RTL (SystemVerilog)"]
  RTL --> SYN["synthesis"]
  SYN --> PD["physical design: floorplan/place/CTS/route"]
  PD --> SIGN["signoff: STA + power + DRC/LVS + DFT"]
  SIGN --> FAB["fab -> packaging (SoC / chiplet / 3D)"]
  FAB --> PROD["product"]
```

## The throughline

A MOSFET is a switch; complementary switches make a CMOS gate that burns almost
no static power; gates make combinational and sequential logic; **delay** (RC,
logical effort) and **power** ($\\alpha C V^2 f$ + leakage) govern how fast and how
hot it runs; **wires** increasingly set the pace; a **flow** (RTL -> synthesis ->
physical design -> signoff -> GDSII) turns intent into silicon; **clocking**,
**low-power** technique, and **test** make it actually work in volume; and
**packaging** (SoC, chiplets, 3D) is the new frontier of integration.

The devices and nodes keep changing - planar to FinFET to nanosheet, one die to
chiplets to 3D stacks - but the chain from a logic equation to a manufacturable,
testable, power-budgeted layout is the constant skill of the VLSI engineer.

The energy-delay relationship sums up the whole discipline - you are always
trading speed against power, and the art is finding the right point:

```plot
{"title": "The fundamental energy-delay tradeoff of a CMOS design", "xLabel": "delay (relative)", "yLabel": "energy per operation (relative)", "xRange": [0.5, 4], "yRange": [0, 12], "grid": true, "controls": [{"name": "tech", "range": [0.5, 2], "value": 1, "label": "technology factor (smaller = newer node)"}], "functions": [{"expr": "tech*(2 + 8/x)", "label": "energy(delay) frontier"}]}
```

A newer node (slide the technology factor down) pushes the whole curve toward
**both** lower energy and lower delay - that is what a process generation buys
you, and why the industry keeps chasing it.

That is VLSI: from one switch to a billion, from a logic equation to a chip in
your pocket.
""",
        ),
    ),
)


VLSI_COURSES: tuple[SeedCourse, ...] = (
    _VLSI_BASICS,
    _VLSI_INTERMEDIATE,
    _VLSI_ADVANCED,
)

__all__ = ["VLSI_COURSES"]
