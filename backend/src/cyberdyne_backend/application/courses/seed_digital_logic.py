"""Curated Digital Logic track: Basics, Intermediate, Advanced.

Teaches digital design with a focus on the two industry HDLs -- SystemVerilog
and VHDL -- shown side by side for every construct, plus CocoTB (Python)
testbenches for verification. There is NO live simulation in the Academy, so all
HDL and CocoTB code is illustrative (you would run it under Verilator / Icarus /
a commercial simulator); the interactivity comes from animated ```plot waveforms
(clocks, counters, timing) and Mermaid schematics / state diagrams.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/digital_logic_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# ── Digital Logic — Basics ────────────────────────────────────────────────────

_DIGITAL_BASICS = SeedCourse(
    slug="digital-logic-basics",
    title="Digital Logic — Basics",
    description=(
        "From bits and logic gates to your first hardware description: Boolean "
        "algebra, combinational logic, and the two industry HDLs (SystemVerilog "
        "and VHDL) shown side by side, plus your first CocoTB testbench - with "
        "animated waveforms, gate diagrams, and a quiz after every lesson."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Digital logic & a bit of history",
            "10 min",
            """\
# Digital logic & a bit of history

The world is analog - voltages vary continuously - but **digital** circuits
agree to read only **two** levels: **0** (low) and **1** (high). That one
decision buys enormous **noise immunity**: a 0.3 V glitch can't turn a 0 into a
1 when "0" means "below 0.8 V" and "1" means "above 2.0 V". Everything in a CPU,
phone, or FPGA is built from this idea.

```plot
{"title": "A clock: the heartbeat that paces every digital circuit", "xLabel": "time", "yLabel": "logic level", "xRange": [0, 4], "yRange": [-0.3, 1.4], "grid": true, "controls": [{"name": "f", "range": [0.5, 3], "value": 1, "label": "clock frequency"}], "animate": {"param": "t", "range": [0, 4], "label": "scrub time"}, "functions": [{"expr": "mod(floor(2*f*x), 2)", "label": "clk"}], "points": [{"xExpr": "t", "yExpr": "mod(floor(2*f*t), 2)", "label": "now", "color": "#dc2626", "size": 7, "trail": true}]}
```

Press **Play** and watch the dot ride the clock; drag **frequency** to speed it
up. A real chip's clock does this billions of times a second.

## A short history

- **1847/1854 - George Boole** invents the algebra of **true/false** - logic as
  math, decades before any machine could use it.
- **1937 - Claude Shannon's master's thesis** shows that Boolean algebra
  describes **switching circuits** (relays). This is the founding insight of
  digital design - arguably the most influential thesis ever written.
- **1947 - the transistor** (Bardeen, Brattain, Shockley) gives a tiny, fast
  electronic switch. **TTL** then **CMOS** logic families follow.
- **1980s - HDLs.** As chips grew to millions of gates, engineers stopped
  drawing schematics and started *describing* hardware in text: **VHDL** (1983,
  US DoD) and **Verilog** (1984, later **SystemVerilog**, 2005).
- **Today - verification dominates.** Most chip effort is *checking* the design.
  Python-based **CocoTB** brought modern software testing to hardware.

> **What this track covers:** Boolean logic and combinational circuits, then
> sequential logic and FSMs, then datapaths and advanced design - always in both
> **SystemVerilog** and **VHDL**, and verified with **CocoTB**. We show the code
> and the waveforms; running it on a simulator is the one step you do outside
> the browser.

**Next:** the atoms of digital logic - gates and Boolean algebra.
""",
        ),
        _t(
            "Logic gates & Boolean algebra",
            "12 min",
            """\
# Logic gates & Boolean algebra

A **logic gate** computes a Boolean function of its inputs. Seven you must know:

| Gate | Symbol | Output is 1 when... |
|------|--------|---------------------|
| AND | $A \\cdot B$ | both inputs are 1 |
| OR | $A + B$ | at least one input is 1 |
| NOT | $\\overline{A}$ | input is 0 |
| NAND | $\\overline{A \\cdot B}$ | NOT(AND) |
| NOR | $\\overline{A + B}$ | NOT(OR) |
| XOR | $A \\oplus B$ | inputs differ |
| XNOR | $\\overline{A \\oplus B}$ | inputs match |

```mermaid
flowchart LR
  A[A] --> AND[AND]
  B[B] --> AND
  AND --> Y["Y = A . B"]
```

## The laws that let you simplify

Boolean algebra has rules just like ordinary algebra, plus a famous one:

$$\\overline{A \\cdot B} = \\overline{A} + \\overline{B}, \\qquad \\overline{A + B} = \\overline{A} \\cdot \\overline{B}.$$

That's **De Morgan's theorem** - it turns ANDs into ORs (and is why you can build
*any* circuit). In fact **NAND** (and NOR) are **universal**: every other gate is
some arrangement of NANDs, which is why silicon is full of them.

## Your first HDL: a gate in both languages

```systemverilog
// SystemVerilog
module and_gate(input logic a, b, output logic y);
  assign y = a & b;          // continuous assignment
endmodule
```

```vhdl
-- VHDL
library ieee; use ieee.std_logic_1164.all;
entity and_gate is
  port (a, b : in  std_logic;
        y    : out std_logic);
end entity;
architecture rtl of and_gate is
begin
  y <= a and b;              -- concurrent signal assignment
end architecture;
```

Same circuit, two dialects: SystemVerilog's `module`/`assign`/`&` vs. VHDL's
`entity`+`architecture`/`<=`/`and`. You'll see this pairing all track long.

**Next:** wiring gates into useful circuits - combinational logic.
""",
        ),
        _t(
            "Combinational logic",
            "12 min",
            """\
# Combinational logic

**Combinational** logic has **no memory**: the outputs depend only on the
*current* inputs (no clock). Any truth table becomes a circuit.

## From truth table to gates

Write the **sum of products (SOP)**: OR together one AND term per row where the
output is 1. A 1-bit majority ("2 of 3 inputs high") is

$$Y = A\\cdot B + A\\cdot C + B\\cdot C.$$

Tools (and **Karnaugh maps**) then minimise it to fewer gates.

## The workhorses: mux, decoder, encoder

A **multiplexer** selects one of several inputs with a select line - the most
common building block in all of hardware:

```mermaid
flowchart LR
  D0[d0] --> MUX{{"MUX (sel)"}}
  D1[d1] --> MUX
  SEL[sel] --> MUX
  MUX --> Y["y = sel ? d1 : d0"]
```

```systemverilog
// SystemVerilog: a 2:1 mux, two idiomatic styles
module mux2(input logic d0, d1, sel, output logic y);
  assign y = sel ? d1 : d0;          // conditional operator
  // or, for bigger logic:
  // always_comb begin
  //   case (sel) 1'b0: y = d0; default: y = d1; endcase
  // end
endmodule
```

```vhdl
-- VHDL: the same 2:1 mux
architecture rtl of mux2 is
begin
  y <= d1 when sel = '1' else d0;    -- conditional assignment
  -- or: with sel select  y <= d0 when '0', d1 when others;
end architecture;
```

> **Practical insight:** describe combinational logic with SystemVerilog's
> `always_comb` (or VHDL's `process(all)`) and assign **every** output in
> **every** branch - a missing assignment infers an unwanted **latch**, the
> classic beginner bug.

**Next:** the structure of an HDL design - modules, entities, and ports.
""",
        ),
        _t(
            "HDL fundamentals: SystemVerilog & VHDL",
            "13 min",
            """\
# HDL fundamentals: SystemVerilog & VHDL

An HDL **describes hardware**, it doesn't run like a program - the synthesizer
turns it into gates and wires. The two industry standards:

| | SystemVerilog | VHDL |
|--|---------------|------|
| Origin | Verilog (1984) -> SV (2005) | US DoD (1983) |
| Design unit | `module` ... `endmodule` | `entity` + `architecture` |
| Wire type | `logic` (4-state) | `std_logic` |
| Assign | `assign` / `<=` / `=` | `<=` (signals) |
| Style | C-like, terse | Ada-like, verbose, strongly typed |
| Common in | US, semiconductors, verification | Europe, defense, aerospace |

## The same block, side by side: a 4-bit 2:1 mux

```systemverilog
module mux4 #(parameter int W = 4) (
  input  logic [W-1:0] d0, d1,
  input  logic         sel,
  output logic [W-1:0] y
);
  assign y = sel ? d1 : d0;
endmodule
```

```vhdl
library ieee; use ieee.std_logic_1164.all;
entity mux4 is
  generic (W : integer := 4);
  port (d0, d1 : in  std_logic_vector(W-1 downto 0);
        sel    : in  std_logic;
        y      : out std_logic_vector(W-1 downto 0));
end entity;
architecture rtl of mux4 is
begin
  y <= d1 when sel = '1' else d0;
end architecture;
```

Note the parallels: SV **`parameter`** = VHDL **`generic`**; SV
**`logic [W-1:0]`** = VHDL **`std_logic_vector(W-1 downto 0)`**. Master one and
the other reads easily.

## Why std_logic has nine values

VHDL's `std_logic` isn't just 0/1 - it includes `'Z'` (high-impedance, for
tri-state buses), `'X'` (unknown/contention), `'U'` (uninitialised), and more.
SystemVerilog's `logic` is **4-state** (0, 1, X, Z). These extra values are how
simulators flag real bugs like two drivers fighting over one wire.

> **Practical insight:** keep your design **synthesizable** - a clean subset of
> the language maps to gates. Much of the language exists for *testbenches*,
> which never become hardware.

**Next:** checking your design works - CocoTB.
""",
        ),
        _t(
            "Verification with CocoTB",
            "12 min",
            """\
# Verification with CocoTB

A design you haven't tested is a design that doesn't work. **CocoTB**
(*coroutine co-simulation testbench*) lets you write the testbench in **Python**
instead of HDL: it drives the inputs of your HDL module (the **DUT**, device
under test) and checks the outputs, running on a simulator like **Verilator** or
**Icarus** underneath.

```mermaid
flowchart LR
  PY["Python test (CocoTB)"] -- drive inputs --> SIM["HDL simulator"]
  SIM --> DUT["DUT: your SystemVerilog / VHDL"]
  DUT -- read outputs --> SIM
  SIM -- values --> PY
  PY --> CHK{"assert == expected"}
```

## A first CocoTB test (for our 2:1 mux)

```python
import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux2(dut):
    # Drive every input combination and check the output.
    for sel in (0, 1):
        for d0 in (0, 1):
            for d1 in (0, 1):
                dut.sel.value = sel
                dut.d0.value = d0
                dut.d1.value = d1
                await Timer(1, units="ns")        # let values settle
                expected = d1 if sel else d0
                assert dut.y.value == expected, \\
                    f"sel={sel} d0={d0} d1={d1}: got {dut.y.value}, want {expected}"
```

What's happening:

- **`@cocotb.test()`** marks an `async` coroutine as a test.
- **`dut`** is your module; `dut.sel.value = ...` drives a port, `dut.y.value`
  reads one.
- **`await Timer(...)`** advances simulated time so combinational outputs settle.
- a plain Python **`assert`** is your check - full Python is available (loops,
  randomness, models, even numpy).

Why teams love it: reuse Python's whole ecosystem, write **reference models** in
a few lines, and keep testbench skills portable across projects.

> **In this course we show the testbenches but don't run them** - executing
> CocoTB needs an HDL simulator on your machine (`pip install cocotb`, a
> `Makefile`, and Verilator/Icarus). The patterns here are exactly what you'd
> run there.

**Next:** circuits that remember - sequential logic (Intermediate course).
""",
        ),
    ),
)


# ── Digital Logic — Intermediate ──────────────────────────────────────────────

_DIGITAL_INTERMEDIATE = SeedCourse(
    slug="digital-logic-intermediate",
    title="Digital Logic — Intermediate: Sequential Logic",
    description=(
        "Circuits that remember: flip-flops and registers, counters and shift "
        "registers, finite state machines, and the timing rules (setup/hold, "
        "metastability) that make synchronous design work - in SystemVerilog and "
        "VHDL, verified with clocked CocoTB testbenches, with animated waveforms."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Flip-flops & sequential logic",
            "12 min",
            """\
# Flip-flops & sequential logic

**Sequential** logic *remembers*: its outputs depend on inputs **and** on stored
state. The storage element is the **flip-flop** - and the **clock** decides when
it updates. An **edge-triggered D flip-flop** copies its input `d` to its output
`q` on each rising clock edge, and holds it the rest of the time.

```plot
{"title": "D flip-flop: q captures d on each rising clock edge", "xLabel": "time", "yLabel": "stacked signals", "xRange": [0, 6], "yRange": [-0.3, 5], "grid": true, "functions": [{"expr": "mod(floor(x), 2)", "label": "clk", "color": "#2563eb"}, {"expr": "2.2 + mod(floor((x+0.4)/1.7), 2)", "label": "d (input)", "color": "#16a34a"}, {"expr": "4.4 + mod(floor((x-0.6)/1.7), 2)", "label": "q (output, delayed)", "color": "#dc2626"}]}
```

The clock (bottom) ticks; `q` (top) follows `d` (middle) but only **changes at
clock edges** - that one-clock memory is the basis of all synchronous design.

## The D flip-flop in both HDLs

```systemverilog
// SystemVerilog: always_ff is the synthesis-friendly clocked block
module dff(input logic clk, rst_n, d, output logic q);
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) q <= 1'b0;       // async active-low reset
    else        q <= d;          // nonblocking <= for registers
endmodule
```

```vhdl
library ieee; use ieee.std_logic_1164.all;
entity dff is
  port (clk, rst_n, d : in std_logic; q : out std_logic);
end entity;
architecture rtl of dff is
begin
  process (clk, rst_n) begin
    if rst_n = '0' then     q <= '0';        -- async reset
    elsif rising_edge(clk) then q <= d;      -- capture on rising edge
    end if;
  end process;
end architecture;
```

> **Practical insight:** use **nonblocking** `<=` in clocked SystemVerilog blocks
> (and `<=` in VHDL processes) for registers, and blocking `=` only in
> `always_comb`. Mixing them is the source of countless simulation-vs-synthesis
> mismatches. Flavours of flip-flop (T, JK) all reduce to a D-FF plus logic.

**Next:** wiring flip-flops into registers, counters, and shift registers.
""",
        ),
        _t(
            "Registers, counters & shift registers",
            "12 min",
            """\
# Registers, counters & shift registers

Group $N$ flip-flops on a common clock and you get an **$N$-bit register**. Add
a little logic and you get the two most useful sequential blocks.

## Counters

A binary **counter** increments each clock. Watch how each bit toggles **half as
often** as the one below it - that's binary counting made visible:

```plot
{"title": "3-bit binary counter (each bit toggles half as often)", "xLabel": "clock ticks", "yLabel": "bits (stacked)", "xRange": [0, 8], "yRange": [-0.3, 6], "grid": true, "animate": {"param": "t", "range": [0, 8], "label": "tick"}, "functions": [{"expr": "mod(floor(x), 2)", "label": "bit0 (LSB)", "color": "#2563eb"}, {"expr": "2.2 + mod(floor(x/2), 2)", "label": "bit1", "color": "#16a34a"}, {"expr": "4.4 + mod(floor(x/4), 2)", "label": "bit2 (MSB)", "color": "#dc2626"}], "points": [{"xExpr": "t", "yExpr": "mod(floor(t), 2)", "color": "#1e3a8a", "size": 6, "trail": true}]}
```

```systemverilog
module counter #(parameter int W = 8)
  (input logic clk, rst_n, en, output logic [W-1:0] count);
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n)   count <= '0;
    else if (en)  count <= count + 1'b1;
endmodule
```

```vhdl
architecture rtl of counter is
  signal cnt : unsigned(W-1 downto 0);
begin
  process (clk, rst_n) begin
    if rst_n = '0' then            cnt <= (others => '0');
    elsif rising_edge(clk) then
      if en = '1' then             cnt <= cnt + 1;
      end if;
    end if;
  end process;
  count <= std_logic_vector(cnt);
end architecture;
```

## Shift registers

A **shift register** moves bits along one position per clock - the heart of
serial links (UART, SPI), delay lines, and LFSRs:

```systemverilog
always_ff @(posedge clk) q <= {q[W-2:0], serial_in};   // shift left
```

```vhdl
if rising_edge(clk) then q <= q(W-2 downto 0) & serial_in; end if;
```

> **Practical insight:** prefer a synchronous counter (all FFs on one clock
> edge) over a **ripple** counter (each FF clocks the next). Ripple counters are
> tempting but accumulate delay and cause glitches - synchronous design is the
> rule for a reason.

**Next:** giving a circuit a plan - finite state machines.
""",
        ),
        _t(
            "Finite State Machines",
            "13 min",
            """\
# Finite State Machines

A **finite state machine (FSM)** is sequential logic organised around a set of
named **states** and the **transitions** between them. It's how you describe
controllers, protocols, and any "do this, then that" behaviour.

```mermaid
stateDiagram-v2
  [*] --> RED
  RED --> GREEN: timer
  GREEN --> YELLOW: timer
  YELLOW --> RED: timer
```

Two flavours:

- **Moore** - outputs depend **only on the current state** (glitch-free, one
  clock late). A traffic light is naturally Moore.
- **Mealy** - outputs depend on **state and inputs** (faster reaction, fewer
  states, but can glitch).

## The "three-block" FSM (the idiom every shop uses)

State register (clocked) + next-state logic (combinational) + output logic:

```systemverilog
module traffic(input logic clk, rst_n, timer, output logic [1:0] light);
  typedef enum logic [1:0] {RED, GREEN, YELLOW} state_t;
  state_t state, next;

  always_ff @(posedge clk or negedge rst_n)        // 1) state register
    if (!rst_n) state <= RED; else state <= next;

  always_comb begin                                // 2) next-state logic
    next = state;
    case (state)
      RED:    if (timer) next = GREEN;
      GREEN:  if (timer) next = YELLOW;
      YELLOW: if (timer) next = RED;
    endcase
  end

  assign light = state;                            // 3) Moore output
endmodule
```

```vhdl
architecture rtl of traffic is
  type state_t is (RED, GREEN, YELLOW);
  signal state, next : state_t;
begin
  process (clk, rst_n) begin                       -- state register
    if rst_n = '0' then state <= RED;
    elsif rising_edge(clk) then state <= next; end if;
  end process;

  process (all) begin                              -- next-state logic
    next <= state;
    case state is
      when RED    => if timer = '1' then next <= GREEN;  end if;
      when GREEN  => if timer = '1' then next <= YELLOW; end if;
      when YELLOW => if timer = '1' then next <= RED;    end if;
    end case;
  end process;
end architecture;
```

> **Practical insight:** use an **enum** (SV) / **enumerated type** (VHDL) for
> states, not raw numbers - the synthesizer picks an efficient encoding
> (binary, one-hot) and your waveforms show readable state *names*.

**Next:** the physics that constrains all of this - timing.
""",
        ),
        _t(
            "Timing, setup/hold & metastability",
            "12 min",
            """\
# Timing, setup/hold & metastability

Flip-flops aren't instantaneous. For a register to capture data reliably, the
input must be **stable in a window around the clock edge**:

- **Setup time ($t_{su}$)** - data stable *before* the edge.
- **Hold time ($t_h$)** - data stable *after* the edge.
- **Clock-to-Q ($t_{cq}$)** - delay from edge to the output changing.

```plot
{"title": "Setup/hold: data must be stable around the clock edge at t=3", "xLabel": "time", "yLabel": "stacked", "xRange": [0, 6], "yRange": [-0.3, 3.6], "grid": true, "functions": [{"expr": "mod(floor(x), 2)", "label": "clk", "color": "#2563eb"}, {"expr": "2.2 + (x>1.2)*(x<4.4)", "label": "data (stable across the edge = OK)", "color": "#16a34a"}]}
```

The maximum clock frequency comes from the longest path between two registers:

$$T_{clk} \\ge t_{cq} + t_{logic} + t_{su}.$$

Violate setup and you miss the edge; the design fails timing.

## Metastability and crossing clock domains

If data changes *right at* the edge (a setup/hold violation - unavoidable when a
signal comes from a **different clock domain** or an asynchronous button), the
flip-flop can go **metastable**: hover between 0 and 1 for an unpredictable time.

The fix is a **synchronizer** - two flip-flops in series on the destination
clock; the first may go metastable, but it almost always resolves before the
second samples it:

```systemverilog
// Two-flop synchronizer for a single async signal
always_ff @(posedge clk) {sync2, sync1} <= {sync1, async_in};
```

```vhdl
if rising_edge(clk) then sync1 <= async_in; sync2 <= sync1; end if;
```

> **Practical insight:** **every** signal crossing between clock domains needs a
> synchronizer (single bits) or an async FIFO / handshake (buses). Unsynchronised
> crossings are the #1 cause of intermittent, impossible-to-reproduce hardware
> bugs.

**Next:** verifying clocked designs with CocoTB.
""",
        ),
        _t(
            "CocoTB for sequential logic",
            "12 min",
            """\
# CocoTB for sequential logic

Testing sequential logic means **driving a clock** and checking outputs **across
clock cycles**. CocoTB makes this clean with a `Clock` and edge triggers.

```python
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_counter(dut):
    # 1) Start a 10 ns clock on dut.clk
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # 2) Apply reset, synchronous to the clock
    dut.rst_n.value = 0
    dut.en.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.en.value = 1

    # 3) Check it counts: a Python reference model alongside the DUT
    expected = 0
    for _ in range(20):
        await RisingEdge(dut.clk)          # wait one cycle
        expected = (expected + 1) % 256
        assert dut.count.value == expected, \\
            f"cycle mismatch: dut={int(dut.count.value)} model={expected}"
```

The key pieces:

- **`Clock(dut.clk, 10, units="ns").start()`** with `cocotb.start_soon(...)`
  runs a free-running clock as a background coroutine.
- **`await RisingEdge(dut.clk)`** suspends the test until the next rising edge -
  the natural unit of time for synchronous logic.
- A **reference model** (the `expected` variable here) is just Python; for an
  FSM you'd mirror the states, for an ALU you'd compute the result, and compare
  every cycle. This "DUT vs. model" pattern is the backbone of real verification.

For an FSM you'd drive the inputs, `await RisingEdge`, and assert both the state
output and any Mealy outputs - exactly the same shape.

> **Practical insight:** check on the **right edge**. Read `dut` outputs after
> the clock edge (and after `Timer(1, units="ns")` if you need combinational
> settle) so you compare stable values, not mid-transition ones.

**Next:** datapaths, advanced HDL, and serious verification (Advanced course).
""",
        ),
    ),
)


# ── Digital Logic — Advanced ──────────────────────────────────────────────────

_DIGITAL_ADVANCED = SeedCourse(
    slug="digital-logic-advanced",
    title="Digital Logic — Advanced: Datapaths, RTL & Verification",
    description=(
        "Build real hardware: arithmetic datapaths and pipelining, advanced "
        "SystemVerilog/VHDL (parameters, interfaces, packages, generate), "
        "memories and FIFOs, modern CocoTB verification (constrained-random, "
        "scoreboards, coverage), and the FPGA/ASIC synthesis flow - with use "
        "cases that tie it together."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Datapaths & arithmetic",
            "12 min",
            """\
# Datapaths & arithmetic

A **datapath** is the part of a design that *moves and transforms* data -
adders, multipliers, ALUs, registers - while an FSM (the **control path**) tells
it what to do when.

## Adders: the speed/area trade-off

A **full adder** sums two bits and a carry. Chain $N$ of them and you get a
**ripple-carry adder** - simple, but the carry ripples through all $N$ stages, so
delay grows with $N$. A **carry-lookahead adder** computes carries in parallel:

$$g_i = a_i b_i \\;(\\text{generate}), \\qquad p_i = a_i \\oplus b_i \\;(\\text{propagate}), \\qquad c_{i+1} = g_i + p_i c_i.$$

```mermaid
flowchart LR
  A[a, b] --> ALU["ALU (add/sub/and/or/...)"]
  OP[op] --> ALU
  ALU --> R["result"]
  ALU --> FLAGS["flags: zero, carry, overflow"]
```

```systemverilog
// SystemVerilog: an adder that exposes the carry out
module adder #(parameter int W = 8)
  (input logic [W-1:0] a, b, input logic cin,
   output logic [W-1:0] sum, output logic cout);
  assign {cout, sum} = a + b + cin;     // synthesis picks the adder structure
endmodule
```

```vhdl
sum_ext <= ('0' & a) + ('0' & b) + cin;   -- W+1 bits to capture carry
sum  <= sum_ext(W-1 downto 0);
cout <= sum_ext(W);
```

## Pipelining: throughput vs. latency

Split a long combinational path with registers and you can clock it **faster** -
each stage does less work per cycle. A multiply that took one slow cycle becomes
3 fast pipeline stages: same latency in nanoseconds, but a result **every**
cycle once the pipe is full. This is how DSP blocks and CPUs hit high clock
rates.

> **Practical insight:** let the synthesizer build adders/multipliers from
> `+`/`*` - it knows the target's fast-carry chains and DSP blocks far better
> than hand-drawn gates. Describe *intent*, not structure.

**Next:** the language features that make big designs manageable.
""",
        ),
        _t(
            "Advanced SystemVerilog & VHDL",
            "13 min",
            """\
# Advanced SystemVerilog & VHDL

Real designs are big, so both languages give you tools to **parameterise** and
**organise**.

## Parameterised, reusable modules

```systemverilog
// SystemVerilog: parameters + a generate loop instantiating W stages
module reg_file #(parameter int W = 32, parameter int N = 16) (
  input  logic clk,
  input  logic [$clog2(N)-1:0] waddr, raddr,
  input  logic we,
  input  logic [W-1:0] wdata,
  output logic [W-1:0] rdata
);
  logic [W-1:0] mem [N];
  always_ff @(posedge clk) if (we) mem[waddr] <= wdata;
  assign rdata = mem[raddr];
endmodule
```

```vhdl
-- VHDL: generics + an array type
entity reg_file is
  generic (W : integer := 32; N : integer := 16);
  port (clk : in std_logic; we : in std_logic;
        waddr, raddr : in integer range 0 to N-1;
        wdata : in std_logic_vector(W-1 downto 0);
        rdata : out std_logic_vector(W-1 downto 0));
end entity;
```

## The features worth knowing

| Need | SystemVerilog | VHDL |
|------|---------------|------|
| Compile-time constant | `parameter` | `generic` |
| Group of signals | `struct` / `interface` | `record` |
| Reusable defs | `package` | `package` |
| Repeated hardware | `generate` / `for` | `for ... generate` |
| Bundle a bus + protocol | **`interface`** (+ modports) | records + procedures |

SystemVerilog **interfaces** are a standout: bundle a whole bus (data, valid,
ready, ...) into one connection, cutting port lists from dozens of wires to one.

> **Practical insight:** stay inside the **synthesizable subset**. `always_comb`,
> `always_ff`, `generate`, parameters and structs synthesize; `initial` blocks,
> `#delays`, `class`, dynamic arrays and `fork/join` are **simulation-only** -
> great for testbenches, invalid for hardware.

**Next:** storing lots of data - memories and FIFOs.
""",
        ),
        _t(
            "Memories, FIFOs & LFSRs",
            "12 min",
            """\
# Memories, FIFOs & LFSRs

## On-chip memory

FPGAs and ASICs have dedicated **RAM** blocks. You don't instantiate them by
name - you write a memory *pattern* and the tool **infers** block RAM:

```systemverilog
// Synchronous single-port RAM (infers block RAM)
module ram #(parameter int W = 32, D = 1024) (
  input logic clk, we,
  input logic [$clog2(D)-1:0] addr,
  input logic [W-1:0] din,
  output logic [W-1:0] dout
);
  logic [W-1:0] mem [D];
  always_ff @(posedge clk) begin
    if (we) mem[addr] <= din;
    dout <= mem[addr];          // registered read -> infers BRAM
  end
endmodule
```

## FIFOs: the universal glue

A **FIFO** (first-in first-out queue) buffers data between blocks that produce
and consume at different rates. An **asynchronous FIFO** (with Gray-coded
pointers through synchronizers) is the standard, safe way to move a *bus* across
clock domains - the bus-level answer to last course's synchronizer.

## LFSRs: cheap pseudo-randomness

A **linear-feedback shift register** is a shift register whose input is the XOR
of selected taps. With the right taps it cycles through all $2^n - 1$ nonzero
states - used for pseudo-random test patterns, scramblers, and CRCs:

```systemverilog
// 8-bit maximal-length LFSR (taps 8,6,5,4 -> x^8+x^6+x^5+x^4+1)
always_ff @(posedge clk)
  if (!rst_n) lfsr <= 8'h01;
  else lfsr <= {lfsr[6:0], lfsr[7]^lfsr[5]^lfsr[4]^lfsr[3]};
```

```vhdl
if rising_edge(clk) then
  lfsr <= lfsr(6 downto 0) & (lfsr(7) xor lfsr(5) xor lfsr(4) xor lfsr(3));
end if;
```

> **Practical insight:** match the memory *template* your vendor documents -
> a read that's registered vs. combinational, or an extra reset, decides whether
> you get fast block RAM or a pile of slow flip-flops. The HDL is a request the
> synthesizer must recognise.

**Next:** verifying it all - modern CocoTB.
""",
        ),
        _t(
            "Advanced verification with CocoTB",
            "13 min",
            """\
# Advanced verification with CocoTB

Directed tests (drive a value, check a value) miss corner cases. Modern
verification is **constrained-random** with **self-checking** scoreboards and
**coverage** - and CocoTB does it all in Python.

```python
import cocotb, random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_alu_random(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    mismatches = 0
    seen_ops = set()                       # crude functional coverage
    for _ in range(1000):                  # 1000 random stimuli
        a  = random.randint(0, 255)
        b  = random.randint(0, 255)
        op = random.randint(0, 3)
        dut.a.value, dut.b.value, dut.op.value = a, b, op
        await RisingEdge(dut.clk)
        # reference model: the "golden" answer, in plain Python
        ref = (a + b, a - b, a & b, a | b)[op] & 0xFF
        if int(dut.result.value) != ref:
            mismatches += 1
        seen_ops.add(op)
    assert mismatches == 0, f"{mismatches} ALU mismatches"
    assert seen_ops == {0, 1, 2, 3}, f"coverage hole: only hit {seen_ops}"
```

The modern verification toolkit, all here:

- **Constrained-random stimulus** - `random` with constraints explores far more
  of the input space than hand-picked vectors.
- **Reference model / scoreboard** - compute the expected result independently
  and compare; the gap between model and DUT is a bug in one of them.
- **Coverage** - track *what you actually exercised* (which ops, which corner
  cases) so "all tests pass" means something.
- **Drivers & monitors** - reusable coroutines that speak a bus protocol, often
  organised with `cocotb.start_soon`, `Queue`, and `Combine`/`First`.
- **Assertions** - inline Python `assert`, or **SVA** (SystemVerilog Assertions)
  embedded in the design for protocol checks.

This mirrors **UVM** (the SystemVerilog verification methodology) but in Python -
which is why CocoTB has spread fast, especially in open-source and FPGA work.

> **Practical insight:** make tests **self-checking and random with a seed**.
> Print the seed on failure so any bug is reproducible - a test that needs a
> human to read the waveform doesn't scale.

**Next:** how your HDL becomes silicon - synthesis, FPGA vs. ASIC.
""",
        ),
        _t(
            "FPGA vs. ASIC & the synthesis flow",
            "11 min",
            """\
# FPGA vs. ASIC & the synthesis flow

Your RTL is just a description until a toolchain turns it into hardware. Two
destinations:

| | FPGA | ASIC |
|--|------|------|
| What it is | reconfigurable chip (LUTs, FFs, DSPs, block RAM) | custom-fabricated silicon |
| Cost | cheap per chip, instant | huge up-front (masks), cheap at volume |
| Speed/power | good | best |
| Turnaround | minutes to reprogram | months per fab spin |
| Use when | prototyping, low/medium volume | high volume, peak performance |

## The flow (RTL to hardware)

```mermaid
flowchart LR
  RTL["RTL: SystemVerilog / VHDL"] --> SYN["Synthesis -> gate netlist"]
  SYN --> PNR["Place & route"]
  PNR --> TIM["Timing analysis (does it meet T_clk?)"]
  TIM --> BIT["FPGA bitstream / ASIC layout"]
```

1. **Synthesis** maps your RTL to the target's primitives (LUTs+FFs on an FPGA;
   standard cells on an ASIC).
2. **Place and route** decides where each element goes and how wires connect.
3. **Static timing analysis** checks every register-to-register path meets
   $T_{clk} \\ge t_{cq} + t_{logic} + t_{su}$ - the setup equation from the
   Intermediate course, now over *real* wire delays. You give it **constraints**
   (clock period, I/O timing); it reports the worst path (**critical path**).
4. The result is an FPGA **bitstream** or an ASIC **layout** sent to a fab.

> **Practical insight:** "it simulates" is not "it works." A design can pass
> CocoTB and still **fail timing** at the target clock. Read the timing report,
> find the critical path, and pipeline or restructure it - timing closure is a
> real, iterative part of the job.

**Next:** where all of this ships - applications.
""",
        ),
        _t(
            "Applications & the throughline",
            "10 min",
            """\
# Applications & the throughline

Everything in this track builds the digital world:

- **Processors** - CPUs, GPUs, and microcontrollers are datapaths (ALUs,
  register files, pipelines) steered by FSMs - exactly what you've built.
- **Accelerators** - AI/ML chips, video codecs, and crypto engines are custom
  datapaths squeezing out performance per watt.
- **Networking** - switches and NICs parse and route packets in hardware at line
  rate, with FIFOs and clock-domain crossings everywhere.
- **DSP** - the filters and FFTs from the Signals track run as pipelined
  multiply-accumulate hardware on FPGAs and ASICs.
- **Everywhere else** - every sensor, motor driver, display, and radio has a
  state machine and a datapath at its core.

## SystemVerilog vs. VHDL in the real world

Both are alive and hiring. **SystemVerilog** dominates US semiconductors and
*verification* (its testbench features are unmatched); **VHDL** is strong in
Europe, defense, and aerospace (its strict typing catches bugs at compile time).
Many teams design in one and verify in the other - and increasingly verify in
**CocoTB/Python** regardless of the design language.

```mermaid
flowchart LR
  SPEC["spec"] --> RTL["RTL (SystemVerilog / VHDL)"]
  RTL --> VER["verify (CocoTB / UVM)"]
  VER --> SYN["synthesize + place & route"]
  SYN --> HW["FPGA / ASIC"]
  VER -. bug found .-> RTL
```

## The throughline

Digital design is a small set of ideas used over and over: **gates** form
**combinational** logic; **flip-flops** add **memory**; a **clock** plus
**setup/hold** discipline makes it reliable; **FSMs** add control and
**datapaths** do the work; and **verification** proves it before it costs
silicon. Describe the *intent* in SystemVerilog or VHDL, check it hard in
CocoTB, and let synthesis turn it into hardware. The tools differ; the
discipline is the same.

**Next:** the final check.
""",
        ),
    ),
)


DIGITAL_LOGIC_COURSES: tuple[SeedCourse, ...] = (
    _DIGITAL_BASICS,
    _DIGITAL_INTERMEDIATE,
    _DIGITAL_ADVANCED,
)

__all__ = ["DIGITAL_LOGIC_COURSES"]
