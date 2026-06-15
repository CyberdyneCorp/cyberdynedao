"""Curated SystemVerilog for Digital Design track: Basics, Intermediate, Advanced.

A hands-on RTL curriculum that backs the Computer Architecture track with the
hardware-description language used to *build* the blocks it describes: modules
and the synthesis mindset, combinational logic, bit/vector arithmetic and number
formats, and sequential logic (Basics); finite-state machines, register files,
an ALU with flags, and inferring on-chip memory (Intermediate); pipelining with
stalls and flushes, parameterization and generate, interfaces/packages/structs,
and verification with testbenches, assertions and coverage (Advanced).

SystemVerilog examples throughout (highlighted via the ``systemverilog`` fence),
with Mermaid diagrams for datapaths and state machines and interactive ```plot
blocks for the quantitative trade-offs (gate delay, number ranges, throughput).

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time, keyed by the exact lesson titles below.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# -- SystemVerilog for Digital Design -- Basics --------------------------------

_SV_BASICS = SeedCourse(
    slug="sysverilog-basics",
    title="SystemVerilog for Digital Design -- Basics",
    description=(
        "Describe real hardware in SystemVerilog: what RTL is and how it becomes "
        "gates, combinational logic with assign and always_comb, bit-vector "
        "arithmetic and signed/unsigned number formats, and sequential logic with "
        "always_ff, flip-flops and reset -- with synthesizable examples, datapath "
        "diagrams, and interactive plots."
    ),
    level="Beginner",
    lessons=(
        _t(
            "RTL and the synthesis mindset",
            "11 min",
            """\
# RTL and the synthesis mindset

SystemVerilog is a **hardware description language (HDL)**. You are not writing a
program that runs step by step -- you are *describing hardware that exists all at
once*. The synthesis tool turns your description into a netlist of gates and
flip-flops. Getting this mindset right is the whole game.

## Register-Transfer Level (RTL)

RTL describes a circuit as **registers** (state that updates on a clock edge) and
the **combinational logic** between them. The synthesis flow maps that to silicon:

```mermaid
flowchart LR
  RTL["SystemVerilog RTL"] --> SYN["synthesis"]
  SYN --> NET["gate-level netlist"]
  NET --> PNR["place and route"]
  PNR --> CHIP["ASIC / FPGA bitstream"]
```

## A module is a block of hardware

A `module` has a name, a list of **ports** (its wires to the outside), and a body
that describes what the hardware does. Here is a 2-to-1 multiplexer two ways --
one structural, one behavioural; both synthesize to the same mux:

```systemverilog
// Behavioural: a conditional expression the tool maps to a mux.
module mux2 #(parameter int W = 8) (
    input  logic [W-1:0] a, b,
    input  logic         sel,
    output logic [W-1:0] y
);
  assign y = sel ? b : a;   // sel=0 -> a, sel=1 -> b
endmodule
```

## Three habits of the synthesis mindset

1. **Everything is concurrent.** Statements outside a procedural block all run at
   once -- order does not matter, unlike software.
2. **Describe hardware you can point to.** Every signal becomes a wire or a
   register. If you cannot say what gate a line of code builds, rethink it.
3. **Prefer the SystemVerilog intent keywords** -- `always_comb`, `always_ff`,
   `logic` -- over the legacy Verilog `reg`/`wire` and bare `always`. They let the
   tool *check* that you built what you meant.

**Next:** combinational logic -- the gates between the registers.
""",
        ),
        _t(
            "Combinational logic: assign and always_comb",
            "12 min",
            """\
# Combinational logic: assign and always_comb

**Combinational** logic has no memory: the outputs are a pure function of the
current inputs. In SystemVerilog you write it with continuous `assign` statements
or an `always_comb` block.

## assign for simple expressions

```systemverilog
module adder #(parameter int W = 8) (
    input  logic [W-1:0] a, b,
    input  logic         cin,
    output logic [W-1:0] sum,
    output logic         cout
);
  assign {cout, sum} = a + b + cin;   // concatenation captures the carry-out
endmodule
```

## always_comb for case/if logic

`always_comb` is for multi-way logic. The golden rule: **assign every output on
every path**, or you accidentally describe a latch (memory you did not want).

```systemverilog
// A 4-function ALU. `unique case` tells the tool the cases are exclusive.
module alu4 #(parameter int W = 8) (
    input  logic [W-1:0] a, b,
    input  logic [1:0]   op,
    output logic [W-1:0] y
);
  always_comb begin
    unique case (op)
      2'b00: y = a + b;
      2'b01: y = a - b;
      2'b10: y = a & b;
      2'b11: y = a | b;
    endcase
  end
endmodule
```

## Wider logic is slower

Combinational delay grows with the circuit. A **ripple-carry** adder's carry must
propagate through every bit, so delay grows *linearly* with width; a
**carry-lookahead** adder spends area to make it grow *logarithmically*. That
trade-off is why wide adders are not free:

```plot
{"title": "Adder delay vs width: ripple-carry vs lookahead", "xLabel": "operand width (bits)", "yLabel": "relative gate delay", "xRange": [1, 32], "yRange": [0, 66], "grid": true, "functions": [{"expr": "2*x", "label": "ripple-carry (linear)", "color": "#dc2626"}, {"expr": "6*log2(x+1)", "label": "carry-lookahead (log)", "color": "#2563eb"}]}
```

> **Latch trap:** if an `always_comb` `if` has no `else` and you read the output
> elsewhere, the tool infers a latch and warns. Always provide a default.

**Next:** the bits themselves -- vectors and number formats.
""",
        ),
        _t(
            "Bits, vectors, and number formats",
            "12 min",
            """\
# Bits, vectors, and number formats

Hardware is just bundles of wires. A **vector** `logic [N-1:0] x` is `N` wires you
can treat as one number -- but *how* you interpret those bits (unsigned vs signed)
changes the arithmetic the tool builds.

## Literals, width, and base

The form is `<width>'<base><value>`: `8'hFF`, `4'b1010`, `12'd255`. Sizing
literals avoids surprises when they meet wider or narrower signals.

```systemverilog
logic [7:0] a = 8'hA5;     // 1010_0101
logic [7:0] b = 8'b0000_1111;
logic [7:0] c = 8'd16;     // decimal 16
```

## Slicing and concatenation

```systemverilog
logic [31:0] word;
logic [7:0]  hi  = word[31:24];        // a byte slice
logic [15:0] swapped = {word[7:0], word[15:8]};  // concatenate to byte-swap
logic [31:0] rep = {4{8'hAB}};         // replication: AB_AB_AB_AB
```

## Signed vs unsigned is an interpretation

The same bit pattern is two different numbers. In an 8-bit code, `8'hFF` is `255`
unsigned but `-1` in two's complement. The high bit flips the sign and subtracts a
full `2^N`. Plot the two interpretations across a 4-bit code to see the wrap:

```plot
{"title": "4-bit code read as unsigned vs two's complement", "xLabel": "bit pattern (0..15)", "yLabel": "numeric value", "xRange": [0, 15], "yRange": [-9, 16], "grid": true, "functions": [{"expr": "x", "label": "unsigned", "color": "#2563eb"}, {"expr": "x - 16*(x >= 8)", "label": "two's complement", "color": "#dc2626"}]}
```

```systemverilog
// `signed` changes comparisons and the >>> arithmetic shift.
logic signed [7:0] s = -8'sd1;   // 8'hFF
logic [15:0] ext = {{8{s[7]}}, s};  // sign-extend by replicating the sign bit
```

> **Width gotcha:** mixing signed and unsigned in one expression makes the whole
> expression unsigned. Cast explicitly with `$signed(...)` / `$unsigned(...)` when
> the intent matters.

**Next:** adding memory -- sequential logic and the clock.
""",
        ),
        _t(
            "Sequential logic: always_ff and flip-flops",
            "12 min",
            """\
# Sequential logic: always_ff and flip-flops

Combinational logic forgets instantly. To *remember*, you need **state**, and
state lives in **flip-flops** that update on a clock edge. `always_ff` is how you
describe them.

## The D flip-flop

```systemverilog
// One D flip-flop with an asynchronous active-low reset.
module dff (
    input  logic clk, rst_n,
    input  logic d,
    output logic q
);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) q <= 1'b0;   // reset wins
    else        q <= d;      // otherwise capture d on the rising edge
  end
endmodule
```

Two rules make this synthesizable and correct:

- Use **non-blocking** assignment `<=` in `always_ff` (all flops sample their
  inputs, then update together -- matching real hardware).
- The sensitivity list is the **clock and reset only**. Data does not appear; the
  flop only looks at `d` at the clock edge.

## A counter is a flop plus an adder

```systemverilog
module counter #(parameter int W = 4) (
    input  logic         clk, rst_n, en,
    output logic [W-1:0] count
);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n)   count <= '0;
    else if (en)  count <= count + 1'b1;   // wraps at 2^W automatically
  end
endmodule
```

A `W`-bit counter counts `0..2^W-1` then wraps -- a sawtooth in time:

```plot
{"title": "A 3-bit counter wraps every 8 clocks (modulo arithmetic)", "xLabel": "clock tick", "yLabel": "count value", "xRange": [0, 24], "yRange": [0, 8], "grid": true, "functions": [{"expr": "mod(floor(x), 8)", "label": "count = tick mod 8"}]}
```

## Clocked timing

```mermaid
flowchart LR
  D["d (data)"] --> FF["D flip-flop"]
  CLK["clk (edge)"] --> FF
  FF --> Q["q (held until next edge)"]
```

> **Blocking vs non-blocking:** use `=` in `always_comb`, `<=` in `always_ff`.
> Mixing them is the single most common source of simulation-vs-synthesis bugs.

**Next:** put state to work -- finite-state machines (Intermediate course).
""",
        ),
        SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min"),
    ),
)


# -- SystemVerilog for Digital Design -- Intermediate --------------------------

_SV_INTERMEDIATE = SeedCourse(
    slug="sysverilog-intermediate",
    title="SystemVerilog for Digital Design -- Intermediate: FSMs, Datapaths & Memory",
    description=(
        "Build the datapath blocks of a CPU in SystemVerilog: finite-state "
        "machines in the clean two-process style, a register file with two read "
        "ports and one write port, an ALU with zero/carry/overflow flags, and "
        "inferring on-chip RAM and ROM -- with state diagrams, datapath schematics, "
        "and synthesizable RTL throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Finite state machines in SystemVerilog",
            "13 min",
            """\
# Finite state machines in SystemVerilog

A **finite-state machine (FSM)** is a controller: it holds a *state*, and on each
clock it decides the next state and the outputs from the state and inputs. FSMs
drive everything from traffic lights to a CPU's control unit.

## The two-process style

The cleanest, most portable pattern splits the FSM into a **sequential** block (the
state register) and a **combinational** block (next-state + output logic):

```systemverilog
module seq_detect (              // detects the bit sequence 1-0-1 on `din`
    input  logic clk, rst_n, din,
    output logic found
);
  typedef enum logic [1:0] {S0, S1, S10, S101} state_t;
  state_t state, next;

  // 1) sequential: hold the state
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) state <= S0;
    else        state <= next;

  // 2) combinational: next-state logic (every path assigns `next`)
  always_comb begin
    next = state;
    unique case (state)
      S0:   next = din ? S1  : S0;
      S1:   next = din ? S1  : S10;
      S10:  next = din ? S101: S0;
      S101: next = din ? S1  : S10;
    endcase
  end

  // Moore output: a function of state only
  assign found = (state == S101);
endmodule
```

## State diagram

```mermaid
stateDiagram-v2
  [*] --> S0
  S0 --> S1: din=1
  S0 --> S0: din=0
  S1 --> S1: din=1
  S1 --> S10: din=0
  S10 --> S101: din=1
  S10 --> S0: din=0
  S101 --> S1: din=1
  S101 --> S10: din=0
```

## Moore vs Mealy

- **Moore** -- outputs depend on *state only*. Glitch-free, one cycle of latency.
- **Mealy** -- outputs depend on state *and inputs*. Fewer states, but outputs can
  change mid-cycle. Use Moore unless you need the lower latency.

> **Why `enum`:** naming states with a `typedef enum` makes waveforms readable
> (you see `S101`, not `2'b11`) and lets the tool check you never assign an
> illegal state.

**Next:** the CPU's scratchpad -- the register file.
""",
        ),
        _t(
            "Building a register file",
            "12 min",
            """\
# Building a register file

A CPU's **register file** is a small, fast memory of `2^A` words. The classic
RISC shape has **two read ports** (to feed both ALU operands) and **one write
port** (to store a result) -- a "2R1W" file.

```systemverilog
module regfile #(
    parameter int W = 32,        // word width
    parameter int A = 5          // address width -> 32 registers
)(
    input  logic         clk,
    input  logic         we,           // write enable
    input  logic [A-1:0] ra1, ra2, wa, // two read addrs, one write addr
    input  logic [W-1:0] wd,            // write data
    output logic [W-1:0] rd1, rd2       // two read data
);
  logic [W-1:0] mem [0:(1<<A)-1];

  // Combinational (asynchronous) reads -- typical for a CPU regfile.
  assign rd1 = mem[ra1];
  assign rd2 = mem[ra2];

  // Synchronous write on the clock edge.
  always_ff @(posedge clk)
    if (we) mem[wa] <= wd;
endmodule
```

## Two subtleties that bite everyone

1. **Register zero.** In RISC-V/MIPS, `x0` is hardwired to zero. Force it on read:
   `assign rd1 = (ra1 == '0) ? '0 : mem[ra1];`
2. **Write-before-read in the same cycle.** If a port reads the same address being
   written this cycle, decide explicitly whether it sees the old or new value
   (bypass it if your pipeline needs the new one).

```mermaid
flowchart LR
  RA1["ra1"] --> RF["register file (2R1W)"]
  RA2["ra2"] --> RF
  WA["wa + wd + we"] --> RF
  RF --> RD1["rd1 -> ALU operand A"]
  RF --> RD2["rd2 -> ALU operand B"]
```

> **Synthesis note:** small register files map to flip-flops or distributed LUT
> RAM; large ones map to block RAM. The read-port style (sync vs async) decides
> which, so it affects timing -- check your target's guidelines.

**Next:** the unit that does the math -- an ALU with flags.
""",
        ),
        _t(
            "An ALU with status flags",
            "12 min",
            """\
# An ALU with status flags

The **ALU** computes; the **flags** summarize the result so branches and
condition codes can act on it. The four classic flags are **Zero**, **Carry**,
**Negative**, and **oVerflow**.

```systemverilog
module alu #(parameter int W = 32) (
    input  logic [W-1:0] a, b,
    input  logic [2:0]   op,           // 000 add, 001 sub, 010 and, 011 or, 100 slt
    output logic [W-1:0] y,
    output logic         zero, carry, negative, overflow
);
  logic [W:0] add_ext;   // one extra bit captures carry-out
  logic [W:0] sub_ext;

  always_comb begin
    add_ext = {1'b0, a} + {1'b0, b};
    sub_ext = {1'b0, a} - {1'b0, b};
    carry   = 1'b0;
    unique case (op)
      3'b000: begin y = add_ext[W-1:0]; carry = add_ext[W]; end
      3'b001: begin y = sub_ext[W-1:0]; carry = sub_ext[W]; end
      3'b010:       y = a & b;
      3'b011:       y = a | b;
      3'b100:       y = ($signed(a) < $signed(b)) ? 1 : 0;  // set-less-than
      default:      y = '0;
    endcase
  end

  assign zero     = (y == '0);
  assign negative = y[W-1];
  // Signed overflow on add: operands same sign, result differs.
  assign overflow = (op == 3'b000) & (a[W-1] == b[W-1]) & (y[W-1] != a[W-1]);
endmodule
```

## Flag meanings

| Flag | Set when | Used by |
|------|----------|---------|
| Zero (Z) | result is all zeros | `beq` / `bne` |
| Carry (C) | unsigned add overflows / sub borrows | unsigned compares, multi-word add |
| Negative (N) | top bit of result is 1 | signed compares |
| oVerflow (V) | signed result wrapped | signed compares, trap-on-overflow |

> **Carry vs overflow:** carry is the *unsigned* out-of-range signal; overflow is
> the *signed* one. `1111_1111 + 1` sets carry (unsigned wrap) but not overflow
> (signed -1 + 1 = 0 is fine). Different flags for different number worlds.

**Next:** where the data lives -- inferring RAM and ROM.
""",
        ),
        _t(
            "Inferring memory: RAM and ROM",
            "12 min",
            """\
# Inferring memory: RAM and ROM

You rarely instantiate memory by hand. Instead you write RTL in a shape the tool
**recognizes** and maps to a dedicated block RAM (BRAM) or ROM. Match the template
and you get fast, dense memory; deviate and you get a wall of flip-flops.

## Synchronous single-port RAM

The key is a **registered (clocked) read** -- that is what makes it a block RAM
rather than a register array:

```systemverilog
module sram #(
    parameter int W = 32,
    parameter int DEPTH = 1024
)(
    input  logic                       clk,
    input  logic                       we,
    input  logic [$clog2(DEPTH)-1:0]   addr,
    input  logic [W-1:0]               wd,
    output logic [W-1:0]               rd
);
  logic [W-1:0] mem [0:DEPTH-1];

  always_ff @(posedge clk) begin
    if (we) mem[addr] <= wd;
    rd <= mem[addr];          // registered read -> infers block RAM
  end
endmodule
```

## ROM from an initial block or a file

```systemverilog
module rom #(parameter int W = 8, DEPTH = 256) (
    input  logic [$clog2(DEPTH)-1:0] addr,
    output logic [W-1:0]             data
);
  logic [W-1:0] mem [0:DEPTH-1];
  initial $readmemh("rom_init.hex", mem);  // load contents at time 0
  assign data = mem[addr];
endmodule
```

## Memory map

```mermaid
flowchart LR
  ADDR["addr"] --> DEC["address decode"]
  DEC --> RAM["RAM block"]
  DEC --> ROM["ROM block"]
  DEC --> MMIO["memory-mapped I/O"]
```

> **Template discipline:** vendors publish exact "inference templates" for each
> RAM style (single-port, true dual-port, byte-enable). Copy them. A one-line
> change to the read can silently cost you the BRAM and blow your timing.

**Next:** make it fast -- pipelining RTL (Advanced course).
""",
        ),
        SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min"),
    ),
)


# -- SystemVerilog for Digital Design -- Advanced ------------------------------

_SV_ADVANCED = SeedCourse(
    slug="sysverilog-advanced",
    title="SystemVerilog for Digital Design -- Advanced: Pipelining, Generics & Verification",
    description=(
        "Production-grade SystemVerilog: pipelining with stall/flush control, "
        "parameterization and generate for reusable hardware, interfaces, packages "
        "and structs for clean designs, and verification with testbenches, "
        "SystemVerilog Assertions (SVA) and functional coverage -- the skills that "
        "turn RTL into a taped-out design."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Pipelining RTL: stalls and flushes",
            "13 min",
            """\
# Pipelining RTL: stalls and flushes

Pipelining overlaps work: while one stage computes, the next operates on the
previous result. In RTL each stage boundary is a **pipeline register**, and the
control logic can **stall** (freeze) or **flush** (bubble) it.

## The pipeline register

```systemverilog
module pipe_reg #(parameter int W = 32) (
    input  logic         clk, rst_n,
    input  logic         stall,   // hold current value
    input  logic         flush,   // inject a zero/NOP bubble
    input  logic [W-1:0] d,
    output logic [W-1:0] q
);
  always_ff @(posedge clk or negedge rst_n) begin
    if      (!rst_n) q <= '0;
    else if (flush)  q <= '0;
    else if (!stall) q <= d;      // if stalled, q keeps its value
  end
endmodule
```

## A 2-stage multiply-accumulate

Stage 1 multiplies, stage 2 adds. The pipeline register between them lets a new
multiply start every cycle:

```systemverilog
module mac2 #(parameter int W = 16) (
    input  logic                clk, rst_n,
    input  logic [W-1:0]        a, b,
    output logic [2*W:0]        acc
);
  logic [2*W-1:0] prod_q;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin prod_q <= '0; acc <= '0; end
    else begin
      prod_q <= a * b;            // stage 1: multiply, register the product
      acc    <= acc + prod_q;     // stage 2: accumulate the registered product
    end
  end
endmodule
```

## Throughput vs latency

Pipelining does not cut a single result's latency -- it raises **throughput** to
one result per cycle once the pipe is full. With N items and k stages it takes
`N + k - 1` cycles, approaching a `k`x speedup:

```plot
{"title": "Pipeline speedup vs item count (slide stage count k)", "xLabel": "items N", "yLabel": "speedup", "xRange": [1, 100], "yRange": [0, 9], "grid": true, "controls": [{"name": "k", "range": [2, 8], "value": 4, "label": "stages k"}], "functions": [{"expr": "x*k/(x + k - 1)", "label": "speedup"}, {"expr": "k", "label": "limit = k", "color": "#94a3b8"}]}
```

```mermaid
flowchart LR
  IN["a, b"] --> S1["stage 1: multiply"]
  S1 --> PR["pipe reg"]
  PR --> S2["stage 2: accumulate"]
  S2 --> OUT["acc"]
```

**Next:** write each block once -- parameterization and generate.
""",
        ),
        _t(
            "Parameterization and generate",
            "12 min",
            """\
# Parameterization and generate

Good RTL is **reusable**: one module that works at any width or depth. Parameters
size it; `generate` builds repeated or optional structure.

## Parameters size a module

```systemverilog
// One adder definition serves 8, 16, 32, 64 bits.
module adder #(parameter int W = 8) (
    input  logic [W-1:0] a, b,
    output logic [W:0]   sum
);
  assign sum = a + b;
endmodule

// Instantiate with an override:
adder #(.W(32)) u_add32 (.a(x), .b(y), .sum(s));
```

## generate-for builds repeated hardware

`genvar` + `generate` elaborate a loop into *parallel* hardware (not a runtime
loop). Here is a ripple-carry adder built bit by bit:

```systemverilog
module ripple_adder #(parameter int W = 8) (
    input  logic [W-1:0] a, b,
    input  logic         cin,
    output logic [W-1:0] sum,
    output logic         cout
);
  logic [W:0] c;
  assign c[0] = cin;
  genvar i;
  generate
    for (i = 0; i < W; i++) begin : bit_slice
      assign sum[i]  = a[i] ^ b[i] ^ c[i];
      assign c[i+1]  = (a[i] & b[i]) | (c[i] & (a[i] ^ b[i]));
    end
  endgenerate
  assign cout = c[W];
endmodule
```

## generate-if includes hardware conditionally

```systemverilog
generate
  if (W > 16) begin : g_fast
    // instantiate a carry-lookahead block for wide adders
  end else begin : g_simple
    // ripple is fine for narrow ones
  end
endgenerate
```

> **Elaboration, not execution:** `generate` runs *once* at build time. The loop
> bound and `if` condition must be constants (parameters/localparams), because the
> tool is laying out physical hardware, not iterating at runtime.

**Next:** keep big designs clean -- interfaces, packages, and structs.
""",
        ),
        _t(
            "Interfaces, packages, and structs",
            "12 min",
            """\
# Interfaces, packages, and structs

As designs grow, port lists explode and constants drift out of sync. Three
SystemVerilog features keep large RTL maintainable.

## packages share types and constants

```systemverilog
package cpu_pkg;
  parameter int XLEN = 32;
  typedef enum logic [2:0] {ALU_ADD, ALU_SUB, ALU_AND, ALU_OR, ALU_SLT} alu_op_e;
  typedef struct packed {
    logic [XLEN-1:0] pc;
    logic [XLEN-1:0] instr;
  } if_id_t;                 // a whole pipeline bundle as one type
endpackage
```

Import it where needed: `import cpu_pkg::*;` -- now every module agrees on `XLEN`
and the opcode encoding.

## packed structs bundle related signals

A `packed` struct is just a vector with named fields -- you can pass it through a
single pipeline register instead of a dozen loose wires:

```systemverilog
import cpu_pkg::*;
if_id_t if_id_d, if_id_q;
assign if_id_d = '{pc: pc_next, instr: imem_data};
// ...register the whole bundle in one always_ff...
```

## interfaces bundle a bus + its protocol

```systemverilog
interface mem_if #(parameter int W = 32) (input logic clk);
  logic        req, gnt;
  logic [W-1:0] addr, wdata, rdata;
  modport master (output req, addr, wdata, input gnt, rdata, clk);
  modport slave  (input  req, addr, wdata, output gnt, rdata);
endinterface
```

A module takes `mem_if.master bus` as one port instead of five, and the `modport`
documents which side drives what.

```mermaid
flowchart LR
  CORE["CPU core (master)"] -->|mem_if| BUS["interconnect"]
  BUS -->|mem_if| MEM["memory (slave)"]
```

> **Why it matters:** a packed struct or interface changes the bus in *one* place.
> Loose port lists drift; typed bundles are checked by the compiler.

**Next:** prove it works -- verification.
""",
        ),
        _t(
            "Verification: testbenches, assertions, and coverage",
            "13 min",
            """\
# Verification: testbenches, assertions, and coverage

Most of the effort on a real chip is **verification**. SystemVerilog is also a
verification language: it drives stimulus, checks results, states properties, and
measures how much of the design space you exercised.

## A self-checking testbench

```systemverilog
module tb_alu;
  logic [31:0] a, b, y;
  logic [2:0]  op;
  alu dut (.a(a), .b(b), .op(op), .y(y), .zero(), .carry(),
           .negative(), .overflow());

  initial begin
    a = 32'd7; b = 32'd5; op = 3'b000; #1;   // add
    assert (y == 32'd12) else $error("add failed: got %0d", y);
    op = 3'b001; #1;                          // sub
    assert (y == 32'd2)  else $error("sub failed: got %0d", y);
    $display("all checks passed");
    $finish;
  end
endmodule
```

## Clock generation

```systemverilog
logic clk = 0;
always #5 clk = ~clk;   // a 100 MHz clock (10 ns period) in simulation
```

## SystemVerilog Assertions (SVA)

A **concurrent assertion** states a property that must hold every cycle -- the
tool checks it for you across the whole run:

```systemverilog
// After a request, a grant must arrive within 1 to 4 cycles.
property req_gnt;
  @(posedge clk) disable iff (!rst_n)
  req |-> ##[1:4] gnt;
endproperty
assert property (req_gnt) else $error("grant came too late");
```

## Functional coverage

Coverage answers "did we actually test it?" A `covergroup` records which cases the
stimulus hit:

```systemverilog
covergroup alu_cov @(posedge clk);
  coverpoint op { bins ops[] = {[0:4]}; }   // did we exercise every opcode?
endgroup
```

```mermaid
flowchart LR
  STIM["stimulus"] --> DUT["design under test"]
  DUT --> CHK["assertions + checks"]
  DUT --> COV["coverage"]
  COV --> DONE["coverage closure?"]
```

> **Coverage closure:** a passing testbench only proves the cases you ran worked.
> Coverage tells you *what fraction* of the intended behaviour you ran -- you sign
> off when both pass *and* coverage is full.

**You finished the track.** You can now describe combinational and sequential
logic, build FSMs and datapaths, parameterize and pipeline them, and verify the
result -- the full RTL-to-signoff loop.
""",
        ),
        SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min"),
    ),
)


SYSVERILOG_COURSES: tuple[SeedCourse, ...] = (
    _SV_BASICS,
    _SV_INTERMEDIATE,
    _SV_ADVANCED,
)

__all__ = ["SYSVERILOG_COURSES"]
