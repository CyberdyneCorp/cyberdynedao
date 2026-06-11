"""Curated FPGA & Reconfigurable Computing track: Basics, Intermediate, Advanced.

A complete FPGA curriculum: the fabric and design flow (LUTs, flip-flops, CLBs,
routing, synthesis, place-and-route, the bitstream, RTL for synthesis,
primitives, constraints), timing/clocking/interfaces (static timing analysis,
PLLs/MMCMs, clock-domain crossing, block RAM/FIFOs/AXI-Stream, FSMs and
pipelining, AXI and SoC FPGAs), and advanced acceleration (soft processors and
RISC-V SoC, high-level synthesis, hardware acceleration and the roofline,
partial reconfiguration and reliability, verification/debug, real applications).
Dual SystemVerilog (RTL) + Python (modeling) focus throughout, with runnable
Python labs (numpy + matplotlib), interactive ```plot blocks, Mermaid diagrams,
LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- FPGA & Reconfigurable Computing -- Basics ---------------------------------

_FPGA_BASICS = SeedCourse(
    slug="fpga-basics",
    title="FPGA & Reconfigurable Computing -- Basics",
    description=(
        "What an FPGA is and how its fabric works (LUTs, flip-flops, CLBs, "
        "routing), the design flow (RTL, synthesis, place-and-route, the "
        "bitstream, toolchains), writing RTL that synthesizes, on-chip "
        "primitives (block RAM, DSP, clocks, I/O), and constraints with a first "
        "project - with side-by-side SystemVerilog and Python, interactive "
        "plots, and a runnable resource-utilization lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What an FPGA is: LUTs, flip-flops & the fabric",
            "11 min",
            """\
# What an FPGA is: LUTs, flip-flops & the fabric

An **FPGA** (Field-Programmable Gate Array) is a chip full of **generic digital
hardware** that you *configure* into whatever circuit you want - and then
re-configure tomorrow into something else. Unlike a CPU, which runs instructions
on fixed hardware, an FPGA *becomes* the hardware.

## The three ingredients

| Block | What it is | What it does |
|-------|------------|--------------|
| **LUT** (look-up table) | a tiny memory addressed by inputs | implements **any** logic function of its inputs |
| **Flip-flop** | a 1-bit register | **stores** state, clocked each cycle |
| **Routing fabric** | a programmable mesh of wires + switches | wires blocks together |

A **LUT** is the magic. A $k$-input LUT is just a $2^k$-bit memory: feed the $k$
inputs as an address, read out the stored bit. By choosing the $2^k$ stored bits
you implement *any* truth table - AND, XOR, a 1-bit adder, anything. Modern
FPGAs use 6-input LUTs ($2^6 = 64$ config bits each).

A **CLB** (Configurable Logic Block, or "slice"/"logic element") packs a handful
of LUTs with their flip-flops and some carry logic. Tile millions of these,
weave the routing fabric through them, and you have an FPGA.

## How many functions can one LUT be?

A $k$-input LUT can be programmed into $2^{2^k}$ distinct functions - it explodes:

$$N(k) = 2^{2^k}.$$

```plot
{"title": "Distinct logic functions a k-input LUT can implement (log2 scale)", "xLabel": "LUT inputs k", "yLabel": "log2(number of functions) = 2^k", "xRange": [1, 6], "yRange": [0, 70], "grid": true, "functions": [{"expr": "2^x", "label": "log2 N = 2^k", "color": "#2563eb"}]}
```

A 2-input LUT is one of 16 functions; a 6-input LUT is one of $2^{64}$ - which is
why the 6-LUT is the universal building block.

## FPGA vs ASIC vs CPU

```mermaid
flowchart LR
  CPU["CPU: fixed HW, runs software, flexible but serial"] --> SPACE["the design space"]
  FPGA["FPGA: reconfigurable HW, parallel, fast to change"] --> SPACE
  ASIC["ASIC: custom silicon, fastest/cheapest at volume, frozen"] --> SPACE
```

- **CPU** - fixed hardware, infinitely reprogrammable in *software*, but executes
  mostly one instruction stream at a time.
- **FPGA** - the hardware itself is programmable; massively **parallel** and
  low-latency, reconfigurable in seconds, but lower clock speeds and higher
  per-unit cost than an ASIC.
- **ASIC** - hardware etched permanently in silicon; the fastest and cheapest *at
  high volume*, but millions of dollars and months to change one gate.

**Real uses today:** FPGAs sit in 5G base stations and network switches (line-rate
packet processing), in data-center SmartNICs (Microsoft put FPGAs in Bing/Azure
servers), in software-defined radio, in pro video gear, and in any product that
needs custom high-speed logic without ASIC volumes.

## Same idea, two languages

A 2-input LUT *is* a truth table. In RTL you describe the function; the tool maps
it onto a LUT:

```systemverilog
// A function the synthesizer will pack into one LUT.
module lut_demo (input logic a, b, c, output logic y);
  assign y = (a & b) | ~c;   // any boolean expr -> a LUT
endmodule
```

```python
# Model the same LUT as its stored truth table (8 bits for 3 inputs).
def lut3(a, b, c):
    return (a and b) or (not c)


table = [lut3(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
print(table)  # the 8 config bits that program this LUT
```

**Next:** how RTL becomes a configured FPGA - the design flow.
""",
        ),
        _t(
            "The FPGA design flow: RTL to bitstream",
            "12 min",
            """\
# The FPGA design flow: RTL to bitstream

You do not draw gates by hand. You **describe behaviour** in an HDL (hardware
description language) and a toolchain turns it into a **bitstream** - the file
that programs every LUT, flip-flop, and routing switch on the chip.

## The pipeline

```mermaid
flowchart LR
  RTL["RTL (SystemVerilog/VHDL)"] --> SYN["synthesis -> netlist of LUTs/FFs"]
  SYN --> MAP["technology map to this chip's primitives"]
  MAP --> PNR["place & route (assign blocks, wire them)"]
  PNR --> STA["static timing analysis"]
  STA --> BIT["bitstream generation"]
  BIT --> FPGA["configure the FPGA"]
```

1. **RTL** - you write *register-transfer level* code: what logic sits between
   registers, what happens each clock edge.
2. **Synthesis** - translates RTL into a **netlist** of generic gates, then maps
   it onto *this* chip's LUTs, flip-flops, block RAM, and DSP slices.
3. **Place-and-route (P&R)** - decides *where* each LUT/FF physically goes and
   programs the routing switches to wire them together. This is the slow,
   NP-hard part.
4. **Static timing analysis (STA)** - checks every path meets the clock; reports
   the maximum frequency $F_{max}$ (Intermediate course).
5. **Bitstream** - the final binary, loaded over JTAG or from flash at power-up.

## The compile-time wall

P&R effort (and runtime) grows steeply as the chip fills up. A handy mental model
of place-and-route runtime vs. **device utilization** $u$ (fraction full):

$$T(u) \\approx \\frac{T_0}{(1 - u)^{2}}.$$

```plot
{"title": "Place-and-route runtime explodes as the device fills (slide T0)", "xLabel": "device utilization u (fraction full)", "yLabel": "relative P&R time", "xRange": [0, 0.95], "yRange": [0, 40], "grid": true, "controls": [{"name": "T0", "range": [0.5, 3], "value": 1, "label": "base time T0"}], "functions": [{"expr": "T0/(1 - x)^2", "label": "P&R time"}]}
```

This is why FPGA builds can take minutes to *hours* (vs. seconds for a software
compile) - and why keeping utilization below ~80% keeps timing closure and
runtimes sane.

## The toolchains

| Vendor / project | Tool | Devices |
|------------------|------|---------|
| **AMD/Xilinx** | **Vivado** (and Vitis) | 7-series, UltraScale, Versal |
| **Intel/Altera** | **Quartus** | Cyclone, Arria, Stratix, Agilex |
| **Lattice / open** | **Yosys + nextpnr** (open source) | iCE40, ECP5 |

The open-source flow (Yosys for synthesis, nextpnr for P&R, the Project IceStorm
bitstream docs) made FPGAs hackable on a hobby budget - a whole maker ecosystem
runs on $30 iCE40 boards.

```systemverilog
// The thing you actually hand to the toolchain: a clocked blinker.
module top (input logic clk, output logic led);
  logic [24:0] cnt = 0;
  always_ff @(posedge clk) cnt <= cnt + 1;
  assign led = cnt[24];   // toggles slowly
endmodule
```

```python
# Model the same counter to predict the blink rate from the clock frequency.
clk_hz = 12_000_000  # 12 MHz oscillator
toggle_bit = 24
blink_hz = clk_hz / (2 ** (toggle_bit + 1))
print(f"LED toggles at {blink_hz:.2f} Hz")
```

**Next:** writing RTL the synthesizer actually likes.
""",
        ),
        _t(
            "RTL for FPGA: combinational vs sequential logic",
            "12 min",
            """\
# RTL for FPGA: combinational vs sequential logic

Synthesizable RTL is a **restricted, disciplined** subset of the HDL. The single
most important idea: every signal is either **combinational** (a function of its
inputs *right now*, mapped to LUTs) or **sequential** (held in a flip-flop,
updated on a clock edge).

## The two block styles

| Style | SystemVerilog | Maps to | Assignment |
|-------|---------------|---------|------------|
| **Combinational** | `always_comb` | LUTs (no memory) | blocking `=` |
| **Sequential** | `always_ff @(posedge clk)` | flip-flops | non-blocking `<=` |

The golden rules that keep synthesis predictable:

- Use **non-blocking** `<=` in clocked blocks, **blocking** `=` in combinational
  ones.
- A combinational block must assign its output for **every** input case, or you
  accidentally infer a **latch** (a memory element you did not want).
- Drive each signal from **one** block only.

## Inferring logic vs. instantiating it

You *describe* what you want and the tool **infers** the hardware: write `a + b`
and it infers an adder; write a clocked register and it infers flip-flops; write
the right memory pattern (next lesson) and it infers block RAM. You only manually
instantiate the special primitives the tool cannot infer.

```mermaid
flowchart LR
  IN["inputs"] --> COMB["combinational logic (LUTs)"]
  COMB --> FF["flip-flops (clocked)"]
  CLK["clk"] --> FF
  FF --> OUT["registered outputs"]
  FF --> COMB
```

## A worked register: the synchronous counter

```systemverilog
module counter #(parameter int W = 8) (
    input  logic         clk,
    input  logic         rst,   // synchronous reset
    input  logic         en,
    output logic [W-1:0] q
);
  always_ff @(posedge clk) begin
    if (rst)      q <= '0;
    else if (en)  q <= q + 1'b1;   // non-blocking in a clocked block
  end
endmodule
```

```python
# Cycle-accurate model of the same counter (state lives between cycles).
W = 8
q = 0
trace = []
en, rst = 1, 0
for _ in range(20):
    if rst:
        q = 0
    elif en:
        q = (q + 1) % (2 ** W)   # wraps like the hardware register
    trace.append(q)
print(trace)
```

## Why coding style is timing

The amount of combinational logic *between* two flip-flops sets the longest path,
which sets the maximum clock speed. A rough model: if you chain $n$ logic levels
each with delay $d$ plus routing, the path delay is

$$t_{path} \\approx n\\,d + t_{route}, \\qquad F_{max} \\approx \\frac{1}{t_{path}}.$$

```plot
{"title": "More logic levels between registers lowers Fmax (slide gate delay)", "xLabel": "logic levels between flip-flops n", "yLabel": "Fmax (MHz)", "xRange": [1, 20], "yRange": [0, 600], "grid": true, "controls": [{"name": "d", "range": [0.3, 2], "value": 0.8, "label": "per-level delay d (ns)"}], "functions": [{"expr": "1000/(d*x + 1.5)", "label": "Fmax = 1000/(n*d + route)"}]}
```

Slide the gate delay: deep combinational logic between registers is exactly why
you **pipeline** (Intermediate course) to push the clock higher.

**Real use:** this discipline - combinational vs sequential, no accidental
latches, one driver per net - is what separates RTL that simulates from RTL that
actually builds and hits timing in a shipping product.

**Next:** the dedicated hardware blocks baked into the silicon.
""",
        ),
        _t(
            "FPGA primitives & resources: block RAM, DSP & clocks",
            "11 min",
            """\
# FPGA primitives & resources: block RAM, DSP & clocks

A modern FPGA is not *only* LUTs and flip-flops. The vendors hardened the most
common, area-hungry functions into **dedicated silicon blocks** scattered across
the fabric. Using them is far smaller and faster than building the same thing
out of LUTs.

## The resource menu

| Primitive | What it is | Use it for |
|-----------|------------|------------|
| **Block RAM (BRAM)** | dedicated dual-port SRAM (e.g. 18/36 kbit each) | buffers, FIFOs, lookup tables, small caches |
| **DSP slice** | a hardened multiply-accumulate (e.g. 18x18 -> add) | filters, FFTs, matrix multiply, ML |
| **Distributed RAM** | LUTs reused as tiny RAM | very small memories |
| **Clock resources** | dedicated low-skew clock trees, **PLL/MMCM** | generate and distribute clocks |
| **I/O banks** | configurable pins (LVCMOS, LVDS, ...) | talk to the outside world |
| **Transceivers** | multi-gigabit serial (GTX/GTY) | PCIe, Ethernet, SerDes |

## Why DSP slices matter: multiplies are expensive in LUTs

An $N$-bit multiply built from LUTs costs on the order of $N^2$ logic, but a DSP
slice does an 18x18 (or wider) multiply in **one** hardened block. Compare the LUT
cost of LUT-built multipliers vs. the count of DSP slices:

```plot
{"title": "Multiplier cost: LUT-built (~N^2) vs DSP slices used", "xLabel": "operand width N (bits)", "yLabel": "resource units", "xRange": [4, 32], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "x^2", "label": "LUTs if built from logic (~N^2)", "color": "#dc2626"}, {"expr": "ceil(x/18)*ceil(x/18)*40", "label": "equivalent if you ran out of DSPs", "color": "#94a3b8"}, {"expr": "ceil(x/18)*ceil(x/18)*5", "label": "DSP-slice path (much cheaper)", "color": "#16a34a"}]}
```

The lesson: **map arithmetic onto DSP slices** and memories onto **BRAM**. A
design that "ran out of LUTs" has often just failed to use the hardened blocks.

## Inferring a block RAM

Write memory with a **registered read** and the tool infers BRAM instead of
building it from flip-flops:

```systemverilog
module bram #(parameter int AW = 10, DW = 32) (
    input  logic            clk, we,
    input  logic [AW-1:0]   addr,
    input  logic [DW-1:0]   din,
    output logic [DW-1:0]   dout
);
  logic [DW-1:0] mem [0:(1<<AW)-1];
  always_ff @(posedge clk) begin
    if (we) mem[addr] <= din;
    dout <= mem[addr];          // registered read -> infers BRAM
  end
endmodule
```

```python
# Model a single-port synchronous RAM (read appears one cycle late).
depth = 1 << 10
mem = [0] * depth
dout = 0
# write 0xABCD to addr 5, then read it back next "cycle"
mem[5] = 0xABCD
dout = mem[5]
print(hex(dout))  # 0xabcd, one cycle after the address was applied
```

**Real use:** a video scaler buffers lines in BRAM; a 5G channel filter runs
hundreds of taps on DSP slices in parallel; an ML inference accelerator is mostly
DSP slices plus BRAM weight storage. Choosing the right primitive is most of
FPGA performance engineering.

**Next:** telling the tool about pins and clocks - constraints.
""",
        ),
        _t(
            "Constraints & getting started: pins, clocks & a first project",
            "11 min",
            """\
# Constraints & getting started: pins, clocks & a first project

RTL describes *logic*; it says nothing about *which physical pin* a signal uses
or *how fast the clock runs*. That information lives in a **constraints file** -
and without it, the tool cannot place your I/O or check timing.

## The two constraints you cannot skip

- **Pin (location + I/O standard)** - "signal `led` goes to package pin H5, at
  the 3.3 V LVCMOS standard." Get this wrong and you can drive a pin into a
  voltage it cannot tolerate.
- **Clock (period)** - "`clk` has a 83.33 ns period (12 MHz)." This is what STA
  measures every path against. No clock constraint means **no timing check** -
  the tool will happily ship a design that fails on the bench.

```mermaid
flowchart TB
  RTL["RTL ports"] --> XDC["constraints file (.xdc / .sdc)"]
  XDC --> LOC["pin location + I/O standard"]
  XDC --> CLK["create_clock period"]
  LOC --> BUILD["place & route"]
  CLK --> STA["timing analysis"]
```

A Vivado XDC snippet:

```systemverilog
// (XDC constraints, not RTL - but lives alongside it)
// set_property PACKAGE_PIN H5  [get_ports led]
// set_property IOSTANDARD LVCMOS33 [get_ports led]
// create_clock -name sysclk -period 83.33 [get_ports clk]
```

## The "blinky": every FPGA's hello-world

The first project is always a blinking LED: it proves the toolchain, the clock,
the pin map, and the board all work. Divide the clock down with a counter and
drive an LED from a high bit. The blink frequency from a clock $f_{clk}$ using bit
$b$ as the output is

$$f_{blink} = \\frac{f_{clk}}{2^{\\,b+1}}.$$

```plot
{"title": "Blinky LED rate vs which counter bit drives it (slide clock)", "xLabel": "counter bit b that drives the LED", "yLabel": "log2 of blink frequency (Hz)", "xRange": [16, 30], "yRange": [-12, 12], "grid": true, "controls": [{"name": "fclk_mhz", "range": [1, 100], "value": 12, "label": "clock frequency (MHz)"}], "functions": [{"expr": "log2(fclk_mhz*1000000) - (x + 1)", "label": "log2(blink Hz)"}]}
```

Slide the clock and pick the bit so the blink lands near 1 Hz (visible to the
eye).

## The second project: a UART

After blinky comes a **UART** transmitter - serialize a byte out one pin at a
fixed baud rate. It introduces a baud-rate clock divider, a shift register, and a
small FSM (start bit, 8 data bits, stop bit), and it lets the FPGA *talk* to a PC.

```systemverilog
// Generate a baud "tick" from the system clock by counting.
module baud_gen #(parameter int CLK = 12_000_000, BAUD = 115_200) (
    input  logic clk, output logic tick
);
  localparam int DIV = CLK / BAUD;
  logic [$clog2(DIV)-1:0] cnt = 0;
  always_ff @(posedge clk) begin
    if (cnt == DIV-1) begin cnt <= 0; tick <= 1'b1; end
    else              begin cnt <= cnt + 1; tick <= 1'b0; end
  end
endmodule
```

```python
# Predict the exact baud-rate error from integer clock division.
clk, baud = 12_000_000, 115_200
div = round(clk / baud)
actual = clk / div
error_pct = 100 * (actual - baud) / baud
print(f"divisor={div}, actual baud={actual:.0f}, error={error_pct:.2f}%")
```

**Real use:** every FPGA bring-up follows this ladder - blinky proves the clock
and toolchain, UART proves I/O and timing, then you add the real design. Pin and
clock constraints are not paperwork; they are how the design meets the physical
world.

**Next:** put it together - model resource utilization vs design size in code.
""",
        ),
        _code(
            "Lab: LUT logic & resource utilization vs design size",
            "13 min",
            """\
# Two experiments in one lab:
#   (1) confirm a k-input LUT really is "any" truth table by programming it, and
#   (2) model how FPGA resource utilization grows with design size, and where a
#       given device "runs out" (the timing-closure danger zone).
import numpy as np
import matplotlib.pyplot as plt

# (1) A 4-input LUT IS its 16-bit truth table. Program one to be (a&b)|(c^d).
inputs = np.array([[a, b, c, d]
                   for a in (0, 1) for b in (0, 1)
                   for c in (0, 1) for d in (0, 1)], dtype=int)
a, b, c, d = inputs[:, 0], inputs[:, 1], inputs[:, 2], inputs[:, 3]
lut_bits = ((a & b) | (c ^ d)).astype(int)   # the 16 config bits
addr = a * 8 + b * 4 + c * 2 + d             # the 4 inputs ARE the address
print("LUT config (16 bits):", lut_bits.tolist())
print("readback matches function:", bool(np.all(lut_bits[addr] == lut_bits)))

# (2) Model utilization vs design size for a mid-size FPGA.
LUTS_AVAIL = 53_200       # like an Artix-7 35T
luts_per_unit = 1200      # LUTs consumed per "design unit" (e.g. a core)
units = np.arange(1, 60)
luts_used = units * luts_per_unit
util = luts_used / LUTS_AVAIL          # fraction of the device used

# A simple timing-closure heuristic: Fmax sags as the device fills (congestion).
fmax_clean = 250.0                                  # MHz when nearly empty
fmax = fmax_clean * np.clip(1.0 - 0.6 * util, 0.05, 1.0)
fits = util <= 1.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(units, 100 * util, color="#2563eb", lw=2)
ax1.axhline(100, ls="--", color="#dc2626", label="device full")
ax1.axhline(80, ls=":", color="#f59e0b", label="80% (closure gets hard)")
ax1.set_xlabel("design size (cores)"); ax1.set_ylabel("LUT utilization (%)")
ax1.set_title("Utilization vs design size"); ax1.grid(True); ax1.legend()

ax2.plot(units[fits], fmax[fits], color="#16a34a", lw=2)
ax2.set_xlabel("design size (cores)"); ax2.set_ylabel("achievable Fmax (MHz)")
ax2.set_title("Congestion lowers Fmax as it fills"); ax2.grid(True)
plt.tight_layout(); plt.show()

last_fit = int(units[fits][-1])
print(f"device holds about {last_fit} cores ({100*util[fits][-1]:.0f}% full)")
print(f"at that point Fmax has sagged to ~{fmax[fits][-1]:.0f} MHz")

# Try it yourself:
#   1. Raise luts_per_unit to model a heavier core - fewer fit.
#   2. The synthesis report (Vivado: report_utilization) gives the real numbers.
""",
        ),
    ),
)


# -- FPGA & Reconfigurable Computing -- Intermediate ---------------------------

_FPGA_INTERMEDIATE = SeedCourse(
    slug="fpga-intermediate",
    title="FPGA & Reconfigurable Computing -- Intermediate: Timing, Clocking & Interfaces",
    description=(
        "Static timing analysis (setup/hold, Fmax, the critical path, timing "
        "closure), clocking (clock domains, PLLs/MMCMs, clock-domain crossing, "
        "metastability), memory and FIFOs with AXI-Stream, FSM and pipelined "
        "datapath design, and on-chip buses (AXI, the SoC FPGA) - with "
        "side-by-side SystemVerilog and Python, interactive plots, and a "
        "runnable CDC/Fmax lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Static timing analysis: setup, hold & Fmax",
            "12 min",
            """\
# Static timing analysis: setup, hold & Fmax

A synchronous design works only if **every** signal that a flip-flop captures is
**stable** in a window around the clock edge. **Static timing analysis (STA)**
checks this for all paths, without simulating - it is the gate between "compiles"
and "actually runs."

## Setup and hold: the capture window

A flip-flop's data input must be steady:

- **Setup time** $t_{su}$ **before** the clock edge,
- **Hold time** $t_h$ **after** the clock edge.

Violate either and the flip-flop can go **metastable** (next lesson). The
**setup** constraint bounds the *slow* path; the **hold** constraint bounds the
*fast* path.

```mermaid
flowchart LR
  FFA["launch FF"] -->|combinational logic + routing| FFB["capture FF"]
  CLK["clock"] --> FFA
  CLK --> FFB
```

## The setup equation and Fmax

For a register-to-register path with clock period $T$, the data must arrive
before the next edge minus the setup time:

$$t_{cq} + t_{logic} + t_{route} + t_{su} \\le T + t_{skew}.$$

The **slack** is whatever is left over; negative slack means a **timing
violation**. Rearranged, the fastest you can clock the design is set by its
**critical path** (the slowest register-to-register path):

$$F_{max} = \\frac{1}{t_{cq} + t_{logic} + t_{route} + t_{su}}.$$

Slide the logic delay and watch $F_{max}$ fall - this is why deep logic kills
speed:

```plot
{"title": "Fmax vs combinational delay on the critical path (slide overhead)", "xLabel": "logic + routing delay (ns)", "yLabel": "Fmax (MHz)", "xRange": [0.5, 15], "yRange": [0, 700], "grid": true, "controls": [{"name": "ovh", "range": [0.3, 2], "value": 0.8, "label": "tcq + tsu overhead (ns)"}], "functions": [{"expr": "1000/(x + ovh)", "label": "Fmax = 1000/(tlogic + overhead)"}]}
```

## Timing closure

**Timing closure** is the iterative job of making all slack non-negative:

- **Pipeline** - split a long combinational path with registers (next datapath
  lesson) to shorten $t_{logic}$.
- **Retime / restructure** logic, balance the path.
- **Floorplan** to cut $t_{route}$, or relax the clock.

```systemverilog
// A long combinational chain - one big critical path, low Fmax.
always_comb sum = a + b + c + d + e + f;   // adder tree all in one cycle
```

```python
# Estimate Fmax from a path delay budget (all in nanoseconds).
t_cq, t_logic, t_route, t_su, t_skew = 0.4, 4.0, 1.5, 0.3, 0.1
T_min = t_cq + t_logic + t_route + t_su - t_skew
fmax_mhz = 1000.0 / T_min
print(f"min period {T_min:.2f} ns -> Fmax {fmax_mhz:.0f} MHz")
```

**Real use:** STA reports (Vivado `report_timing_summary`) are the daily
language of FPGA work - "WNS" (worst negative slack) tells you instantly whether
a build is safe to ship.

**Next:** where clocks come from and the danger of crossing between them.
""",
        ),
        _t(
            "Clocking: PLLs, MMCMs & clock domains",
            "11 min",
            """\
# Clocking: PLLs, MMCMs & clock domains

A board gives you one or two oscillators; a design needs *many* related clocks -
a 100 MHz logic clock, a 148.5 MHz pixel clock, a 200 MHz DDR clock. **PLLs** and
**MMCMs** (Mixed-Mode Clock Managers) synthesize them, and dedicated **clock
trees** distribute them with low skew.

## PLL / MMCM: multiply and divide a clock

A PLL locks an output to the input and produces

$$f_{out} = f_{in}\\,\\frac{M}{D \\cdot O},$$

where $M$ multiplies, $D$ is the input divide, and $O$ the output divide. By
choosing $M, D, O$ you reach almost any frequency. Slide $M$:

```plot
{"title": "PLL output frequency = fin * M / (D*O), fin=100 MHz (slide M)", "xLabel": "output divider O", "yLabel": "output frequency (MHz)", "xRange": [1, 16], "yRange": [0, 800], "grid": true, "controls": [{"name": "M", "range": [4, 64], "value": 12, "label": "feedback multiplier M"}], "functions": [{"expr": "100*M/(1*x)", "label": "fout (MHz)"}]}
```

MMCMs add fine **phase shifting** and dynamic reconfiguration on top of the basic
PLL - used to align a clock with data (e.g. center a clock in a DDR data eye).

## Clock domains

A **clock domain** is the set of flip-flops driven by one clock. Logic *within* a
domain is checked by STA. The problem is signals that pass **between** domains:
the launch and capture clocks are unrelated, so STA cannot guarantee the setup/
hold window - which leads straight to metastability.

```mermaid
flowchart LR
  subgraph A["domain A (100 MHz)"]
    FA["logic"]
  end
  subgraph B["domain B (148.5 MHz)"]
    FB["logic"]
  end
  FA -->|crossing!| FB
```

## Clock-domain crossing (CDC) safely

You **never** let a multi-bit bus cross asynchronously and hope. The safe
patterns:

- **Single-bit control:** a **2-flip-flop synchronizer** (next lesson) lets
  metastability settle.
- **Multi-bit data:** an **asynchronous FIFO** (dual-clock, BRAM-based) or a
  **handshake**; encode counters in **Gray code** so only one bit changes at a
  time.

```systemverilog
// MMCM/PLL is instantiated, not inferred - vendor primitive (sketch):
// MMCME2_BASE #(.CLKFBOUT_MULT_F(12.0), .CLKOUT0_DIVIDE_F(8.0)) mmcm (...);
// -> 100 MHz * 12 / 8 = 150 MHz on CLKOUT0
```

```python
# Solve for PLL settings that hit a target frequency from a 100 MHz input.
fin, target = 100.0, 148.5
best = min(((M, O, abs(fin * M / O - target))
            for M in range(4, 65) for O in range(1, 17)),
           key=lambda t: t[2])
M, O, err = best
print(f"M={M}, O={O} -> {fin*M/O:.3f} MHz (error {err:.3f} MHz)")
```

**Real use:** an HDMI pipeline runs the video logic at the pixel clock and the
memory at the DDR clock, crossing between them through async FIFOs; a SmartNIC
crosses from the line-rate Ethernet clock to the PCIe clock the same way.

**Next:** quantifying the danger - metastability probability.
""",
        ),
        _t(
            "Metastability & the MTBF of a synchronizer",
            "11 min",
            """\
# Metastability & the MTBF of a synchronizer

When a flip-flop's setup/hold window is violated (which is *guaranteed* to
sometimes happen on an asynchronous crossing), its output can hang at an
in-between voltage for a while before resolving randomly to 0 or 1. That is
**metastability**, and you manage it statistically, not by elimination.

## The exponential resolution and MTBF

The probability the device is *still* undecided after a settling time $t$ decays
exponentially with the flip-flop's resolution time constant $\\tau$. The classic
**mean time between failures** for a synchronizer is

$$\\text{MTBF} = \\frac{e^{\\,t/\\tau}}{f_{clk}\\,f_{data}\\,T_w},$$

where $f_{clk}$ is the sampling clock, $f_{data}$ the rate of asynchronous events,
and $T_w$ a small "metastability window." The headline: **MTBF grows
exponentially with settling time** - so giving the signal **one more clock cycle**
to settle buys astronomically more reliability.

```plot
{"title": "Synchronizer MTBF vs settling time (log10 years, slide tau)", "xLabel": "settling time available (ns)", "yLabel": "log10(MTBF in years)", "xRange": [1, 12], "yRange": [-6, 18], "grid": true, "controls": [{"name": "tau", "range": [0.2, 1], "value": 0.4, "label": "resolution time constant tau (ns)"}], "functions": [{"expr": "x/(tau*2.3026) - 9", "label": "log10(MTBF years), schematic"}]}
```

Press Play to watch a metastable node ring near the half-rail and then resolve
(here, settle toward logic 1) - the longer it dithers, the closer it creeps to a
captured failure:

```plot
{"title": "A flip-flop resolving out of metastability (press Play)", "xLabel": "time (settling units)", "yLabel": "node voltage (0 = low rail, 1 = high rail)", "xRange": [0, 10], "yRange": [-0.1, 1.1], "grid": true, "animate": {"param": "t", "range": [0, 10], "label": "time"}, "functions": [{"expr": "0.5 + 0.5*(1 - exp(-x/3))*sign(sin(2))", "label": "resolving node v(t)", "color": "#7c3aed"}], "points": [{"xExpr": "t", "yExpr": "0.5 + 0.5*(1 - exp(-t/3))*sign(sin(2))", "label": "now", "color": "#dc2626", "size": 7, "trail": true}]}
```

## The 2-flip-flop synchronizer

The standard fix for a **single-bit** crossing: two flip-flops in the destination
clock back-to-back. The first may go metastable; it gets a full clock period to
resolve before the second samples it.

```mermaid
flowchart LR
  ASYNC["async signal"] --> FF1["FF1 (may go metastable)"]
  FF1 --> FF2["FF2 (resamples after 1 cycle)"]
  FF2 --> SAFE["clean signal in dest domain"]
  CLKD["dest clock"] --> FF1
  CLKD --> FF2
```

The settling time available is one clock period minus overhead; a **3-FF**
synchronizer adds another period for very high reliability or very fast clocks.

```systemverilog
module sync2 (input logic clk, input logic d_async, output logic q);
  logic ff1;
  always_ff @(posedge clk) begin
    ff1 <= d_async;   // may go metastable; resolves within a cycle
    q   <= ff1;       // clean
  end
endmodule
```

```python
import math
# MTBF for a 2-FF synchronizer with one clock period of settling.
fclk, fdata, Tw, tau = 200e6, 1e6, 0.1e-9, 0.3e-9
t_settle = 1 / fclk - 1e-9          # ~ one period minus overhead
mtbf_s = math.exp(t_settle / tau) / (fclk * fdata * Tw)
print(f"MTBF ~ {mtbf_s/3.15e7:.2e} years")  # 3.15e7 s/year
```

> **Practical insight:** you cannot make metastability impossible - only
> astronomically unlikely. The free lever is *time*: add a flip-flop stage and
> the MTBF jumps by orders of magnitude. Never sync a multi-bit bus bit-by-bit;
> use a FIFO or a Gray-coded handshake.

**Real use:** every chip that mixes clock domains - a phone SoC, a network switch,
a disk controller - relies on exactly these synchronizers; a missing one causes
the maddening "fails once a week in the field" bug.

**Next:** the memory structures that actually move data between domains.
""",
        ),
        _t(
            "Memory, FIFOs & AXI-Stream",
            "12 min",
            """\
# Memory, FIFOs & AXI-Stream

Data on an FPGA lives in **block RAM**, and the workhorse structure built from it
is the **FIFO** - a first-in/first-out queue that absorbs rate mismatches and
safely crosses clock domains.

## Inferring memory, and the FIFO

A FIFO is BRAM plus a **write pointer** and a **read pointer** and a little logic
that reports **full** and **empty**. Two flavors:

- **Synchronous FIFO** - one clock; decouples bursty producers from steady
  consumers (elastic buffering).
- **Asynchronous FIFO** - separate write and read clocks; the canonical safe way
  to move a multi-bit stream across a clock domain (pointers crossed in **Gray
  code** through synchronizers).

```mermaid
flowchart LR
  PROD["producer (wr_clk)"] -->|wr_en, din| FIFO["FIFO (BRAM)"]
  FIFO -->|rd_en, dout| CONS["consumer (rd_clk)"]
  FIFO --> FULL["full"]
  FIFO --> EMPTY["empty"]
```

## Sizing a FIFO: handle the burst

A FIFO must be deep enough that it never overflows when the producer bursts faster
than the consumer drains. For a burst of length $B$ where the producer runs at
rate $r_p$ and consumer at $r_c$ (with $r_p > r_c$ during the burst), the needed
depth is roughly

$$D \\ge B\\left(1 - \\frac{r_c}{r_p}\\right).$$

```plot
{"title": "FIFO depth needed vs burst length (slide consumer/producer ratio)", "xLabel": "burst length B (words)", "yLabel": "minimum FIFO depth", "xRange": [0, 2000], "yRange": [0, 2000], "grid": true, "controls": [{"name": "ratio", "range": [0.1, 0.95], "value": 0.5, "label": "consumer/producer rate ratio"}], "functions": [{"expr": "x*(1 - ratio)", "label": "depth >= B(1 - rc/rp)"}]}
```

## AXI-Stream: the standard data-mover handshake

For streaming data between IP blocks, the industry standard is **AXI4-Stream**: a
simple **valid/ready handshake**. The source asserts `tvalid` when it has data;
the sink asserts `tready` when it can accept; a word transfers only on the cycle
where **both** are high. This backpressure is what makes a FIFO chain
self-throttling.

```systemverilog
// AXI-Stream skip-buffer style transfer: move a word only when both agree.
always_ff @(posedge clk) begin
  if (s_tvalid && s_tready) begin
    data <= s_tdata;             // accepted this cycle
  end
end
assign s_tready = !fifo_full;    // backpressure: stop when we cannot accept
```

```python
# Model an AXI-Stream FIFO over time: a bursty source, a steady sink.
import numpy as np
depth = 16
occ = 0
src = [3, 3, 3, 3, 0, 0, 1, 1, 4, 0, 0, 0]   # words offered per cycle
sink_rate = 2                                  # words drained per cycle
trace = []
for offered in src:
    space = depth - occ
    accepted = min(offered, space)             # tready backpressure
    occ += accepted
    occ -= min(sink_rate, occ)                 # consumer drains
    trace.append(occ)
print("occupancy:", trace, "max:", max(trace))
```

**Real use:** AXI-Stream connects the blocks of a video pipeline, a radio
receiver, and an ML dataflow accelerator; the async FIFO is how a 10 GbE MAC hands
packets to processing logic on a different clock.

**Next:** controlling the dataflow - FSMs and pipelining.
""",
        ),
        _t(
            "FSMs & datapath design: pipelining for Fmax",
            "12 min",
            """\
# FSMs & datapath design: pipelining for Fmax

Most real designs are a **control path** (a finite state machine deciding *what*
to do) driving a **datapath** (the registers and arithmetic doing it). Getting
both right - and fast - is the core of RTL design.

## Coding a finite state machine

The clean, synthesizable pattern is **two (or three) processes**: one clocked
block for the **state register**, one combinational block for the **next-state**
logic and outputs.

```mermaid
stateDiagram-v2
  [*] --> IDLE
  IDLE --> LOAD: start
  LOAD --> RUN: loaded
  RUN --> DONE: count == 0
  DONE --> IDLE: ack
```

```systemverilog
typedef enum logic [1:0] {IDLE, LOAD, RUN, DONE} state_t;
state_t state, next;
always_ff @(posedge clk) state <= rst ? IDLE : next;   // state register
always_comb begin                                      // next-state logic
  next = state;
  unique case (state)
    IDLE: if (start)        next = LOAD;
    LOAD:                   next = RUN;
    RUN:  if (count == 0)   next = DONE;
    DONE: if (ack)          next = IDLE;
  endcase
end
```

## Pipelining: trade latency for throughput (and Fmax)

A long combinational datapath (say a multiply-add chain) is one big critical path
- low $F_{max}$. **Pipelining** inserts registers to break it into $N$ shorter
stages. The clock period drops to roughly the longest *stage*, so $F_{max}$ and
**throughput** rise, at the cost of $N$ cycles of **latency**.

For a path of delay $T_{path}$ split into $N$ balanced stages, each with register
overhead $t_{ovh}$:

$$F_{max}(N) = \\frac{1}{\\dfrac{T_{path}}{N} + t_{ovh}}.$$

Throughput rises with $N$ but with diminishing returns as the per-stage overhead
dominates. Slide the overhead:

```plot
{"title": "Pipelining raises Fmax with diminishing returns (slide overhead)", "xLabel": "pipeline stages N", "yLabel": "Fmax (MHz), path = 10 ns", "xRange": [1, 20], "yRange": [0, 1100], "grid": true, "controls": [{"name": "ovh", "range": [0.2, 2], "value": 0.6, "label": "register overhead per stage (ns)"}], "functions": [{"expr": "1000/(10/x + ovh)", "label": "Fmax(N)"}]}
```

After a point, adding stages just adds latency without raising the clock - the
overhead floor wins.

```python
# Find the pipeline depth where Fmax stops improving meaningfully.
T_path, t_ovh = 10.0, 0.6   # ns
for N in range(1, 13):
    fmax = 1000.0 / (T_path / N + t_ovh)
    print(f"N={N:2d}  Fmax={fmax:6.0f} MHz")
```

> **Practical insight:** pipelining is the single most common timing-closure move.
> A streaming pipeline still finishes one result *per clock* once full - the extra
> latency is paid only once.

**Real use:** an FFT core, a video filter, and a crypto engine are all deep
pipelines; pipelining a DSP datapath is what lets an FPGA sustain hundreds of
MHz on math a CPU would crawl through.

**Next:** connecting your logic to a processor - AXI and SoC FPGAs.
""",
        ),
        _t(
            "On-chip interfaces & buses: AXI and the SoC FPGA",
            "11 min",
            """\
# On-chip interfaces & buses: AXI and the SoC FPGA

Real systems are not one monolithic RTL block - they are many IP cores, often a
**processor**, all talking over a standard **on-chip bus**. On modern FPGAs that
bus is **AXI** (part of ARM's AMBA standard), and the chip is often a **SoC
FPGA**: hard ARM cores next to programmable logic on one die.

## The AXI family

| Variant | Use | Style |
|---------|-----|-------|
| **AXI4 (full)** | high-throughput, burst memory access | address + burst data channels |
| **AXI4-Lite** | simple register access (control/status) | one word at a time |
| **AXI4-Stream** | continuous data flow (no addresses) | valid/ready handshake |

AXI uses independent **read and write channels**, each with its own valid/ready
handshake, so reads and writes and address/data can overlap - that concurrency is
what gives it bandwidth.

```mermaid
flowchart LR
  CPU["ARM cores (PS)"] -->|AXI| INTC["AXI interconnect"]
  INTC -->|AXI-Lite| REGS["your control registers (PL)"]
  INTC -->|AXI| DDR["DDR memory controller"]
  INTC -->|AXI-Stream| ACC["your accelerator (PL)"]
```

## The SoC FPGA: best of both worlds

Devices like the **Zynq** (AMD) and **SoC FPGAs** (Intel) put a hard **processing
system (PS)** - real ARM Cortex cores running Linux - beside the **programmable
logic (PL)**. Software runs the slow, irregular control on the CPU; the FPGA
fabric does the fast, parallel, deterministic work; they share memory over AXI.

This split is the dominant pattern in modern embedded systems: the CPU configures
and orchestrates an accelerator you built in the fabric, and reads results back
through memory-mapped AXI-Lite registers.

## Bandwidth: bursts amortize the address overhead

AXI bursts move many beats per address. Effective bandwidth vs **burst length**
$L$ (with per-transaction overhead $h$ cycles) at a bus width $W$ bytes and clock
$f$:

$$BW = W f\\,\\frac{L}{L + h}.$$

```plot
{"title": "AXI effective bandwidth vs burst length (slide overhead cycles)", "xLabel": "burst length L (beats)", "yLabel": "fraction of peak bandwidth", "xRange": [1, 64], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "h", "range": [1, 16], "value": 6, "label": "per-transaction overhead h (cycles)"}], "functions": [{"expr": "x/(x + h)", "label": "BW / peak"}]}
```

Short bursts waste the bus on addressing overhead; long bursts approach peak.

```systemverilog
// An AXI4-Lite register read responds with a single data beat:
always_ff @(posedge clk)
  if (arvalid && arready) rdata <= regfile[araddr[7:2]];  // word-addressed
```

```python
# Effective AXI bandwidth for a 128-bit bus at 200 MHz vs burst length.
W_bytes, f = 16, 200e6
peak = W_bytes * f / 1e9    # GB/s
h = 6
for L in (1, 4, 16, 64, 256):
    bw = peak * L / (L + h)
    print(f"burst {L:3d}: {bw:.2f} GB/s ({100*L/(L+h):.0f}% of peak)")
```

**Real use:** a Zynq-based camera runs Linux on the ARM cores for networking and
config while the fabric does real-time image processing, streaming results to DDR
over AXI - the template for drones, medical imaging, and industrial vision.

**Next:** simulate clock-domain crossing and pipeline speed yourself.
""",
        ),
        _code(
            "Lab: CDC metastability MTBF & Fmax vs pipeline depth",
            "14 min",
            """\
# Two FPGA timing experiments:
#   (1) how synchronizer MTBF grows with the number of flip-flop stages, and
#   (2) how Fmax and throughput improve with pipeline depth (with diminishing
#       returns as register overhead dominates).
import numpy as np
import matplotlib.pyplot as plt

# (1) Synchronizer MTBF vs number of FF stages at two clock speeds.
fdata = 1e6          # 1 MHz of asynchronous events
Tw = 0.1e-9          # metastability window
tau = 0.3e-9         # resolution time constant
overhead = 0.5e-9    # per-stage routing/setup overhead
stages = np.arange(1, 5)

mtbf_years = {}
for fclk in (100e6, 400e6):
    period = 1.0 / fclk
    # n stages give (n-1) full periods of settling beyond the first capture
    t_settle = (stages - 1) * period + (period - overhead)
    t_settle = np.clip(t_settle, 0, None)
    mtbf_s = np.exp(t_settle / tau) / (fclk * fdata * Tw)
    mtbf_years[fclk] = mtbf_s / 3.15e7

# (2) Fmax and throughput vs pipeline depth for a 12 ns datapath.
T_path, t_ovh = 12.0, 0.6     # ns
N = np.arange(1, 21)
fmax = 1000.0 / (T_path / N + t_ovh)        # MHz
# Throughput once the pipe is full = Fmax (one result per clock); latency = N cycles.
best_N = int(N[np.argmax(np.gradient(fmax) < 5)]) if np.any(np.gradient(fmax) < 5) else N[-1]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
for fclk, color in [(100e6, "#2563eb"), (400e6, "#dc2626")]:
    ax1.semilogy(stages, mtbf_years[fclk], "o-", color=color,
                 label=f"{fclk/1e6:.0f} MHz dest clock")
ax1.axhline(1e6, ls="--", color="#16a34a", label="1 million years")
ax1.set_xlabel("synchronizer FF stages"); ax1.set_ylabel("MTBF (years, log)")
ax1.set_title("Each stage multiplies MTBF"); ax1.grid(True, which="both"); ax1.legend()

ax2.plot(N, fmax, color="#7c3aed", lw=2)
ax2.set_xlabel("pipeline stages N"); ax2.set_ylabel("Fmax (MHz)")
ax2.set_title(f"Fmax vs pipeline depth (12 ns path)"); ax2.grid(True)
plt.tight_layout(); plt.show()

print("MTBF at 400 MHz, 2 stages: "
      f"{mtbf_years[400e6][1]:.2e} years (1 stage: {mtbf_years[400e6][0]:.2e})")
print(f"Fmax: 1 stage {fmax[0]:.0f} MHz -> {N[-1]} stages {fmax[-1]:.0f} MHz")

# Try it yourself:
#   1. Raise fdata (more crossings) - MTBF drops; add a stage to recover it.
#   2. Lower t_ovh to model a faster register - deeper pipelines stay worthwhile.
""",
        ),
    ),
)


# -- FPGA & Reconfigurable Computing -- Advanced -------------------------------

_FPGA_ADVANCED = SeedCourse(
    slug="fpga-advanced",
    title="FPGA & Reconfigurable Computing -- Advanced: Soft Cores, HLS & Acceleration",
    description=(
        "Soft processors and the embedded SoC (RISC-V, MicroBlaze, bare-metal), "
        "high-level synthesis (C-to-RTL, pipeline/unroll pragmas, tradeoffs), "
        "hardware acceleration (parallelism, dataflow, the roofline, DSP/ML), "
        "partial reconfiguration and reliability (SEU, multi-die), verification "
        "and on-chip debug (ILA, coverage), with a runnable accelerator-speedup "
        "lab and a real-world applications finale - dual SystemVerilog/Python."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Soft processors & the embedded FPGA SoC",
            "12 min",
            """\
# Soft processors & the embedded FPGA SoC

You can build an *entire CPU* out of FPGA fabric - a **soft processor**. It runs
slower than a hard ARM core, but it costs only LUTs, you can have *many*, and you
can customize the instruction set. This turns an FPGA into a programmable
**system-on-chip** you define.

## The soft-core options

| Core | Origin | Notes |
|------|--------|-------|
| **MicroBlaze** | AMD/Xilinx | mature 32-bit RISC, rich peripherals |
| **Nios V / Nios II** | Intel | Nios V is RISC-V based |
| **RISC-V** (VexRiscv, Rocket, PicoRV32) | open ISA | open, customizable, no license fee |

**RISC-V** is the momentum pick: an **open instruction set** you can extend with
custom instructions that drop straight into the fabric beside the core - exactly
the kind of hardware/software co-design FPGAs are built for.

```mermaid
flowchart LR
  CORE["soft CPU (RISC-V)"] -->|AXI/Wishbone| BUS["on-chip bus"]
  BUS --> ROM["instruction memory (BRAM)"]
  BUS --> UART["UART"]
  BUS --> ACC["custom accelerator (your RTL)"]
  BUS --> GPIO["GPIO / timers"]
```

## Bare-metal vs OS

- **Bare-metal** - no OS; your C `main()` owns the machine. Lowest latency, fully
  deterministic - ideal for tight control loops.
- **RTOS** (FreeRTOS) - tasks and scheduling for moderately complex firmware.
- **Linux** - on a *hard* core (Zynq PS) or a big soft core; full networking and
  filesystems for the control plane.

## Hard vs soft: a cost/performance tradeoff

A hard core (Zynq ARM) runs ~1 GHz; a soft RISC-V on fabric runs ~100-200 MHz but
costs only a few thousand LUTs, so you can instantiate several. Throughput when
you scale *count* of soft cores vs one fast hard core:

```plot
{"title": "Aggregate MIPS: many soft cores vs one hard core (slide soft clock)", "xLabel": "number of soft cores", "yLabel": "aggregate MIPS", "xRange": [1, 16], "yRange": [0, 3500], "grid": true, "controls": [{"name": "fsoft", "range": [50, 250], "value": 120, "label": "soft-core clock (MHz)"}], "functions": [{"expr": "fsoft*0.8*x", "label": "N soft cores (~0.8 MIPS/MHz each)"}, {"expr": "1000*0.9*1", "label": "one 1 GHz hard core", "color": "#dc2626"}]}
```

Soft cores win on *parallel*, customizable, deterministic work; the hard core
wins on single-thread speed and running Linux.

```systemverilog
// A custom instruction hook: the soft core hands operands to your RTL.
// (sketch of a RISC-V custom-opcode functional unit)
always_ff @(posedge clk)
  if (custom_valid) result <= popcount(rs1) + popcount(rs2);  // 1-cycle insn
```

```c
// On the soft core, that custom instruction is just a function call:
// int r = __builtin_custom_popcount(a, b);   // runs in hardware, 1 cycle
```

**Real use:** soft cores run housekeeping inside big FPGA designs (config,
calibration, slow control) so you do not waste a precious hard core; RISC-V soft
cores are the basis of open silicon research and security-hardened controllers.

**Next:** writing accelerators in C instead of RTL - high-level synthesis.
""",
        ),
        _t(
            "High-level synthesis: from C to RTL",
            "12 min",
            """\
# High-level synthesis: from C to RTL

Writing every accelerator in RTL is slow. **High-level synthesis (HLS)** lets you
describe the *algorithm* in C/C++ and have the tool generate the RTL - schedule
operations into clock cycles, build the datapath and FSM, and infer the memories.
Tools: **Vitis HLS** (AMD), **Intel HLS**, and research flows.

## What HLS automates - and what you still steer

HLS handles scheduling and binding, but the **pragmas** you add decide the
performance. The two that matter most:

- **PIPELINE** - overlap loop iterations so a new one starts every **II**
  (initiation interval) cycles. `II=1` means one result per cycle.
- **UNROLL** - replicate the loop body $K$ times to run $K$ iterations in
  **parallel** (costs $K$x the hardware).

```mermaid
flowchart LR
  C["C/C++ algorithm + pragmas"] --> SCHED["HLS: schedule into cycles"]
  SCHED --> RTL["generated RTL (datapath + FSM)"]
  RTL --> SYN["normal synthesis / P&R"]
```

## Pipelining a loop: throughput vs II

For a loop of $N$ iterations, each doing work that takes $L$ cycles of latency,
pipelined at initiation interval $II$, the total cycles are about

$$\\text{cycles} \\approx (N - 1)\\,II + L.$$

As $N$ grows, throughput is dominated by $II$ - so driving $II$ to 1 is the whole
game. Slide $II$:

```plot
{"title": "HLS loop cycles vs iterations for different II (slide II)", "xLabel": "loop iterations N", "yLabel": "total cycles", "xRange": [0, 1000], "yRange": [0, 5000], "grid": true, "controls": [{"name": "II", "range": [1, 8], "value": 1, "label": "initiation interval II"}], "functions": [{"expr": "(x - 1)*II + 20", "label": "cycles = (N-1)*II + latency"}]}
```

## Unrolling: parallelism for area

Unrolling by $K$ cuts the iteration count by $K$ but uses $K$ copies of the
datapath. Speedup vs hardware cost is the central HLS tradeoff:

```plot
{"title": "Unroll factor: speedup vs hardware cost (slide cost per copy)", "xLabel": "unroll factor K", "yLabel": "relative value", "xRange": [1, 16], "yRange": [0, 18], "grid": true, "controls": [{"name": "cost", "range": [0.3, 2], "value": 1, "label": "hardware cost per copy"}], "functions": [{"expr": "x", "label": "speedup ~ K", "color": "#16a34a"}, {"expr": "cost*x", "label": "hardware used", "color": "#dc2626"}]}
```

## The honest tradeoffs

HLS shrinks development time dramatically and is great for **dataflow** and
math-heavy kernels. But hand-written RTL still wins the last 20-30% of area/
performance and tight I/O timing, and HLS quality is *very* sensitive to how you
write the C (memory access patterns, fixed-point types, pragmas). It is a power
tool, not magic.

```python
# Compare a C-style scalar loop's cycles to a pipelined-II=1 estimate.
N, latency = 1024, 18
for II in (4, 2, 1):
    cycles = (N - 1) * II + latency
    print(f"II={II}: {cycles} cycles  ({N/cycles:.2f} results/cycle)")
```

**Real use:** HLS is how teams ship FPGA video codecs, genomics aligners, and ML
inference kernels in weeks instead of months; cloud FPGA accelerators (AWS F1)
are commonly authored in HLS.

**Next:** the principles behind why accelerators are fast - parallelism, dataflow,
the roofline.
""",
        ),
        _t(
            "Hardware acceleration: parallelism, dataflow & the roofline",
            "13 min",
            """\
# Hardware acceleration: parallelism, dataflow & the roofline

An FPGA accelerates by building **exactly** the parallel datapath a problem
needs - no instruction fetch, no caches, hundreds of operations every cycle. The
art is matching the architecture to the algorithm.

## The three kinds of parallelism

- **Spatial / data parallelism** - replicate hardware to process many data
  elements at once (the unroll lever).
- **Pipeline parallelism** - deep pipelines keep every stage busy on a stream
  (one result per cycle once full).
- **Task / dataflow parallelism** - independent kernels run concurrently, passing
  data through FIFOs (AXI-Stream), so the whole graph runs at the rate of its
  slowest stage.

```mermaid
flowchart LR
  IN["stream in"] --> K1["kernel 1"] --> F1["FIFO"] --> K2["kernel 2"] --> F2["FIFO"] --> K3["kernel 3"] --> OUT["stream out"]
```

## Amdahl's law: the parallel ceiling

If a fraction $p$ of the work is parallelizable and you accelerate that part by
$s$, the overall speedup is bounded:

$$\\text{Speedup} = \\frac{1}{(1 - p) + \\dfrac{p}{s}}.$$

The serial remainder $(1-p)$ caps everything - slide $p$:

```plot
{"title": "Amdahl's law: speedup vs accelerator speedup s (slide parallel fraction p)", "xLabel": "accelerator speedup s on the parallel part", "yLabel": "overall speedup", "xRange": [1, 100], "yRange": [0, 25], "grid": true, "controls": [{"name": "p", "range": [0.5, 0.99], "value": 0.9, "label": "parallelizable fraction p"}], "functions": [{"expr": "1/((1 - p) + p/x)", "label": "overall speedup"}]}
```

## The roofline: are you compute- or memory-bound?

Performance is capped by *either* peak compute *or* memory bandwidth times the
**operational intensity** $I$ (operations per byte moved):

$$\\text{Perf} = \\min\\big(\\text{Peak}_{compute},\\; BW \\times I\\big).$$

Below the "ridge" intensity you are **memory-bound** (the slanted roof); above it
you are **compute-bound** (the flat roof). Slide bandwidth:

```plot
{"title": "Roofline: attainable performance vs operational intensity (slide bandwidth)", "xLabel": "operational intensity (ops/byte)", "yLabel": "performance (GOPS)", "xRange": [0.1, 40], "yRange": [0, 600], "grid": true, "controls": [{"name": "bw", "range": [5, 60], "value": 20, "label": "memory bandwidth (GB/s)"}], "functions": [{"expr": "min(500, bw*x)", "label": "min(peak compute, BW * I)"}]}
```

The takeaway: feeding data is usually the bottleneck. FPGAs win by keeping data
**on-chip** (BRAM, streaming) to raise operational intensity instead of thrashing
external memory.

```systemverilog
// A systolic MAC array tile: each cell multiplies and passes data on (dataflow).
always_ff @(posedge clk) begin
  acc  <= acc + a_in * b_in;   // local multiply-accumulate (a DSP slice)
  a_out <= a_in;  b_out <= b_in;  // stream operands to neighbours
end
```

```python
# Roofline: where does a kernel land for a given FPGA?
peak_gops, bw = 500.0, 20.0      # 500 GOPS compute, 20 GB/s memory
for I in (0.5, 2, 8, 25):        # ops per byte
    perf = min(peak_gops, bw * I)
    bound = "memory" if bw * I < peak_gops else "compute"
    print(f"intensity {I:5.1f} ops/byte -> {perf:6.1f} GOPS ({bound}-bound)")
```

**Real use:** FPGA ML accelerators (Microsoft Brainwave, Xilinx DPU) are systolic
DSP arrays sized to stay compute-bound; SDR and radar use streaming dataflow to
hit deterministic, low latency a GPU cannot match.

**Next:** changing the hardware while it runs - partial reconfiguration and
reliability.
""",
        ),
        _t(
            "Partial reconfiguration, reliability & multi-die",
            "11 min",
            """\
# Partial reconfiguration, reliability & multi-die

An FPGA's defining trick is that it can be reprogrammed - and advanced features
push that further: reprogram **part** of the chip while the rest keeps running,
survive radiation in space, and span multiple silicon dies in one package.

## Dynamic / partial reconfiguration (DPR)

You can define **reconfigurable partitions** and swap the logic in them at runtime
while the static region keeps operating. This **time-multiplexes** scarce fabric:
a chip too small to hold every accelerator at once can load each on demand.

```mermaid
flowchart LR
  STATIC["static region (always running)"] --> SLOT["reconfig partition"]
  BIT1["bitstream A (FIR filter)"] -.load.-> SLOT
  BIT2["bitstream B (FFT)"] -.swap.-> SLOT
  BIT3["bitstream C (crypto)"] -.swap.-> SLOT
```

The win is **virtual area**: how many functions you can field in a fixed fabric
grows with how many you time-share through one slot. But reconfiguration takes
time (loading a partial bitstream), so it pays only when a function is idle long
enough.

## Reliability: SEU in the field and in space

A cosmic ray or stray particle can flip a configuration bit - a **single-event
upset (SEU)**. Because the bitstream *is* the circuit, a flipped config bit can
silently change your logic. Defenses:

- **Configuration scrubbing** - continuously read back and correct config memory
  via ECC.
- **TMR (triple modular redundancy)** - triple critical logic and vote; one
  upset is outvoted.

TMR's reliability advantage over a simplex design (per-module upset probability
$p$) is that the majority voter only fails if **two or three** of the three copies
are hit:

$$R_{TMR} = 1 - \\big(3p^2(1-p) + p^3\\big).$$

```plot
{"title": "TMR vs simplex reliability as upset probability rises", "xLabel": "per-module upset probability p", "yLabel": "system reliability R", "xRange": [0, 0.5], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1 - p", "label": "simplex (one copy)", "color": "#dc2626"}, {"expr": "1 - (3*p^2*(1-p) + p^3)", "label": "TMR (vote of 3)", "color": "#16a34a"}]}
```

TMR wins decisively at low $p$ (the realistic regime) - which is why spacecraft
FPGAs run triplicated, scrubbed logic. Note the curves cross near $p=0.5$: TMR
only helps when modules are *more often right than wrong*.

## Multi-die (SSI) and 3D integration

The biggest FPGAs exceed one reticle, so vendors stitch multiple dies
(**SLRs** - super logic regions) onto a silicon interposer (**stacked silicon
interconnect**). Crossing between dies costs extra delay, so you **floorplan** to
keep critical paths within one SLR. HBM-in-package adds huge memory bandwidth
right next to the fabric.

```systemverilog
// TMR voter for one bit: majority of three redundant copies.
assign voted = (a & b) | (a & c) | (b & c);
```

```python
# Compare simplex vs TMR reliability across upset probabilities.
for p in (0.001, 0.01, 0.05, 0.2):
    simplex = 1 - p
    tmr = 1 - (3 * p**2 * (1 - p) + p**3)
    print(f"p={p:5.3f}: simplex={simplex:.5f}  TMR={tmr:.5f}")
```

**Real use:** Mars rovers and satellites use radiation-tolerant FPGAs with
scrubbing and TMR; data-center FPGAs use DPR to reload accelerators per tenant;
the largest AI/networking parts are multi-die with in-package HBM.

**Next:** finding the bugs - verification and on-chip debug.
""",
        ),
        _t(
            "Verification & debug on FPGA: simulation, ILA & coverage",
            "12 min",
            """\
# Verification & debug on FPGA: simulation, ILA & coverage

Hardware bugs are expensive: you cannot single-step a chip running at 300 MHz, and
a respin of an ASIC costs millions. FPGAs are kinder (just rebuild), but you still
verify hard *before* hardware and debug methodically *on* hardware.

## Simulation: verify before you build

You test RTL in a **simulator** (Verilator, QuestaSim, Vivado XSim) by writing a
**testbench** that drives inputs and checks outputs. This is fast, fully visible
(every signal), and where most bugs should die.

- **Directed tests** - hand-written stimulus for known cases.
- **Constrained-random + assertions (UVM)** - the simulator generates legal
  random stimulus; **assertions** (SVA) flag illegal behaviour automatically.
- **Coverage** - measures how much of the design's behaviour your tests actually
  exercised (next).

```mermaid
flowchart LR
  TB["testbench"] --> DUT["design under test (RTL)"]
  DUT --> CHK["checkers / assertions"]
  TB --> COV["coverage collection"]
  CHK --> PASS["pass/fail"]
```

## Coverage: when is verification "done"?

You never test *every* input, so coverage tells you when you have tested *enough*.
Random testing hits the easy cases fast, then the curve flattens - the last few
percent (corner cases) take most of the effort:

$$\\text{coverage}(n) = 1 - e^{-n/\\tau}.$$

```plot
{"title": "Verification coverage vs test effort (slide difficulty tau)", "xLabel": "simulation cycles (millions)", "yLabel": "functional coverage", "xRange": [0, 50], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "tau", "range": [3, 25], "value": 10, "label": "coverage difficulty tau"}], "functions": [{"expr": "1 - exp(-x/tau)", "label": "coverage closure"}]}
```

The long tail is why teams add **directed** tests for the corners random misses.

## On-chip debug: the ILA / logic analyzer

Once on hardware, you cannot see internal signals directly - so you instantiate an
**Integrated Logic Analyzer (ILA / SignalTap)**: a debug core that uses **BRAM**
to capture chosen signals into a circular buffer, triggered on a condition, then
streams them out over JTAG. It is an oscilloscope *inside* the FPGA.

The catch: capture depth costs BRAM. Capturing $W$ bits at depth $D$ uses about
$W \\times D$ bits of block RAM, so there is always a width-vs-depth budget.

```plot
{"title": "ILA capture: BRAM cost vs depth for different signal widths", "xLabel": "capture depth D (samples)", "yLabel": "BRAM used (kbit)", "xRange": [0, 8192], "yRange": [0, 600], "grid": true, "functions": [{"expr": "32*x/1000", "label": "32 signals", "color": "#2563eb"}, {"expr": "64*x/1000", "label": "64 signals", "color": "#dc2626"}]}
```

```systemverilog
// SystemVerilog assertion: req must be granted within 4 cycles (caught in sim).
assert property (@(posedge clk) req |-> ##[1:4] gnt)
  else $error("grant did not follow request in time");
```

```python
# Budget an ILA capture against an available BRAM pool.
bram_kbit = 1800        # device BRAM available for debug
for width, depth in [(32, 4096), (64, 4096), (128, 8192)]:
    used = width * depth / 1000.0
    print(f"{width} signals x {depth} deep = {used:.0f} kbit "
          f"({'fits' if used <= bram_kbit else 'too big'})")
```

**Real use:** ILAs catch the bugs that only appear with real I/O timing and
real data - a protocol corner case, a CDC glitch, a marginal interface - that
simulation never stimulated.

**Next:** push parallel speedup in code.
""",
        ),
        _code(
            "Lab: accelerator throughput & parallel speedup",
            "14 min",
            """\
# Model an FPGA accelerator's speedup vs a CPU baseline:
#   (1) Amdahl's law - the serial fraction caps overall speedup, and
#   (2) the roofline - whether replicating compute helps depends on memory
#       bandwidth (you eventually become memory-bound).
import numpy as np
import matplotlib.pyplot as plt

# (1) Amdahl: overall speedup vs accelerator speedup, for several parallel
#     fractions p. The serial remainder (1-p) is the hard ceiling.
s = np.linspace(1, 200, 400)        # speedup of the parallel part
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
for p, color in [(0.5, "#94a3b8"), (0.9, "#2563eb"),
                 (0.99, "#16a34a"), (0.999, "#dc2626")]:
    overall = 1.0 / ((1 - p) + p / s)
    ceiling = 1.0 / (1 - p)
    ax1.plot(s, overall, color=color, label=f"p={p}  (max {ceiling:.0f}x)")
ax1.set_xlabel("accelerator speedup on parallel part")
ax1.set_ylabel("overall speedup")
ax1.set_title("Amdahl's law: the serial part caps you")
ax1.grid(True); ax1.legend()

# (2) Roofline: attainable GOPS vs number of parallel MAC lanes (each lane is
#     a DSP slice doing ops/cycle), capped by memory bandwidth * intensity.
fclk = 300e6                         # 300 MHz fabric
ops_per_lane = 2                     # multiply + add per cycle
lanes = np.arange(1, 513)
compute_gops = lanes * ops_per_lane * fclk / 1e9
intensity = 4.0                      # ops per byte for this kernel
bw_gbs = 20.0                        # external memory bandwidth
mem_roof = bw_gbs * intensity        # GOPS the memory can sustain
attainable = np.minimum(compute_gops, mem_roof)

ridge = np.argmax(compute_gops >= mem_roof)
ax2.plot(lanes, compute_gops, "--", color="#94a3b8", label="raw compute (lanes)")
ax2.axhline(mem_roof, color="#dc2626", label=f"memory roof ({mem_roof:.0f} GOPS)")
ax2.plot(lanes, attainable, color="#16a34a", lw=2, label="attainable")
ax2.set_xlabel("parallel MAC lanes (DSP slices)")
ax2.set_ylabel("performance (GOPS)")
ax2.set_title("Roofline: lanes help until memory-bound")
ax2.grid(True); ax2.legend()
plt.tight_layout(); plt.show()

print(f"Amdahl: at p=0.99 even infinite HW caps at {1/(1-0.99):.0f}x")
print(f"Roofline: adding lanes past ~{lanes[ridge]} wastes silicon "
      f"(memory-bound at {mem_roof:.0f} GOPS)")
print("Fix: raise operational intensity (keep data on-chip) to lift the roof.")

# Try it yourself:
#   1. Raise bw_gbs (e.g. HBM at 400) - the memory roof lifts, more lanes pay off.
#   2. Raise intensity (more reuse per byte) - same effect without faster memory.
""",
        ),
        _t(
            "Applications & the throughline: data centers, SDR & vision",
            "11 min",
            """\
# Applications & the throughline: data centers, SDR & vision

Everything in this track converges on one idea: when a problem is **parallel,
streaming, latency-critical, or evolving**, building the *exact* hardware beats
running software on fixed hardware. Here is where that wins in the real world.

## Data centers & networking

- **SmartNICs / DPUs** - FPGAs on the network card process packets at line rate
  (encryption, firewalling, virtual switching), offloading the CPU. Microsoft's
  **Catapult/Azure** put FPGAs in servers for Bing ranking and network accel.
- **Compute acceleration** - **AWS F1**, Alveo cards run genomics, video
  transcoding, databases, and ML inference; reconfigurable per workload.
- **Low, deterministic latency** - high-frequency trading uses FPGAs to react in
  *nanoseconds*, far below any software path.

```mermaid
flowchart LR
  NET["network / sensors / radio"] --> FPGA["FPGA: parallel, low-latency, reconfigurable"]
  FPGA --> DC["data center offload"]
  FPGA --> SDR["software-defined radio / 5G"]
  FPGA --> VIS["vision / imaging"]
  FPGA --> EDGE["edge AI / robotics"]
```

## Software-defined radio & 5G

The radio's physical layer - filters, FFTs, modulation/demodulation, channel
coding - is exactly the streaming DSP an FPGA excels at. **5G base stations**,
radar, and **SDR** platforms (USRP) run these chains on FPGA fabric because the
math is fixed-rate, parallel, and must be deterministic.

## Vision, imaging & edge AI

- **Real-time vision** - cameras, drones, ADAS, and medical imaging do
  pixel-streaming pipelines (debayer, scale, detect) at sensor rate with bounded
  latency.
- **Edge ML inference** - DPU/systolic accelerators run CNNs with custom
  fixed-point precision, hitting high **performance-per-watt** where a GPU is too
  hot or too slow to respond.

## The economic throughline: when does an FPGA win?

The choice among CPU, FPGA, and ASIC is largely about **volume**. NRE
(non-recurring engineering) for an ASIC is enormous but its per-unit cost is
tiny; an FPGA has near-zero NRE but a higher per-unit cost. Total cost vs volume:

$$C_{total}(V) = \\text{NRE} + c_{unit}\\,V.$$

```plot
{"title": "Total cost vs production volume: FPGA vs ASIC crossover", "xLabel": "production volume (thousands of units)", "yLabel": "total cost (relative)", "xRange": [0, 500], "yRange": [0, 600], "grid": true, "functions": [{"expr": "5 + 0.8*x", "label": "FPGA (low NRE, high per-unit)", "color": "#2563eb"}, {"expr": "200 + 0.1*x", "label": "ASIC (high NRE, low per-unit)", "color": "#dc2626"}]}
```

Below the crossover, the FPGA is cheaper (and infinitely flexible); above it, the
ASIC's low per-unit cost wins. FPGAs also win whenever the design *must keep
changing* - evolving standards, per-customer features, in-field upgrades - because
you reflash the bitstream instead of respinning silicon.

```python
# Find the FPGA-vs-ASIC crossover volume.
nre_fpga, unit_fpga = 5.0, 0.8       # relative units
nre_asic, unit_asic = 200.0, 0.1
crossover = (nre_asic - nre_fpga) / (unit_fpga - unit_asic)
print(f"crossover at ~{crossover:.0f}k units")
print("below: FPGA cheaper and flexible; above: ASIC's per-unit cost wins")
```

## The throughline

LUTs and flip-flops wired by a routing fabric (Basics), clocked and pipelined to
hit timing and crossed safely between domains (Intermediate), then organized into
soft-core SoCs, generated by HLS, and replicated into parallel accelerators with
reliability and debug built in (Advanced) - that is reconfigurable computing. The
device gives you raw parallel hardware; the discipline of timing, dataflow, and
verification turns it into a system that ships. The chips get bigger; the
principles - parallelism, the clock, and the bitstream - stay the same.
""",
        ),
    ),
)


FPGA_COURSES: tuple[SeedCourse, ...] = (
    _FPGA_BASICS,
    _FPGA_INTERMEDIATE,
    _FPGA_ADVANCED,
)

__all__ = ["FPGA_COURSES"]
