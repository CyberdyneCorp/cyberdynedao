"""Curated Computer Architecture & Organization track: Basics, Intermediate,
Advanced.

A complete computer-architecture curriculum: data representation and the ISA,
the datapath and a single-cycle CPU, the memory hierarchy, assembly programming
and the calling convention, and I/O and buses (Basics); pipelining, hazards and
forwarding, caches and AMAT, virtual memory and the TLB, and performance
evaluation with Amdahl's law (Intermediate); instruction-level parallelism and
out-of-order execution, branch prediction, multicore and MESI coherence,
accelerators and the roofline model, and SoC/modern systems (Advanced).

Dual assembly/C (the low-level idea) + Python (modeling and simulation) focus
throughout, with runnable Python labs (numpy + matplotlib), interactive ```plot
blocks, Mermaid diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time, keyed by the exact lesson titles below.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Computer Architecture & Organization -- Basics ----------------------------

_COMPARCH_BASICS = SeedCourse(
    slug="comparch-basics",
    title="Computer Architecture & Organization -- Basics",
    description=(
        "How a computer actually works, from the ground up: data representation "
        "and the instruction set, the datapath of a single-cycle CPU, the memory "
        "hierarchy and buses, RISC-V/MIPS assembly and the calling convention, "
        "and I/O with polling vs interrupts -- with side-by-side assembly/C and "
        "Python, interactive plots, and a runnable tiny-CPU simulator lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Data representation and the ISA",
            "12 min",
            """\
# Data representation and the ISA

A computer only ever moves and transforms **bits**. Everything else -- numbers,
text, images, the program itself -- is an agreement about what those bits *mean*.

## Binary, hex, and two's complement

An $n$-bit unsigned word holds values $0 \\dots 2^n - 1$. To represent negative
numbers nearly every machine uses **two's complement**: the top bit has weight
$-2^{n-1}$, so an 8-bit byte covers $-128 \\dots 127$. Negating is "flip all bits
and add 1". Its great virtue: one adder handles both signed and unsigned.

$$\\text{value} = -b_{n-1}\\,2^{n-1} + \\sum_{i=0}^{n-2} b_i\\,2^{i}.$$

Word sizes are powers of two, so storage grows exponentially with bit width.
Slide the bit count and watch the addressable range explode:

```plot
{"title": "Addressable values vs word width 2^n (slide n)", "xLabel": "bit index", "yLabel": "place value 2^i", "xRange": [0, 16], "yRange": [0, 70000], "grid": true, "controls": [{"name": "n", "range": [1, 16], "value": 8, "label": "word width n (bits)"}], "functions": [{"expr": "(x<n)*pow(2,x)", "label": "weight of bit i (0 above n)"}]}
```

## The ISA: the contract between software and hardware

The **Instruction Set Architecture** is the visible interface a CPU promises to
programmers: its registers, its instructions and their encodings, the addressing
modes, and the memory model. The microarchitecture (how it's built) can change
wildly underneath while the ISA stays stable -- which is why a 2026 x86 chip
still runs 1990s binaries.

| Feature | RISC (e.g. RISC-V, ARM, MIPS) | CISC (e.g. x86) |
|---------|-------------------------------|-----------------|
| Instruction length | fixed (often 32-bit) | variable |
| Memory access | only load/store | many instructions touch memory |
| Instruction count | many simple ones | fewer, more complex ones |
| Decode | simple, pipeline-friendly | complex (often cracked into micro-ops) |

## Registers and addressing modes

**Registers** are the handful of fastest storage slots inside the CPU (RISC-V has
32). **Addressing modes** are the ways an instruction names its operand:

- **Immediate** -- a constant baked into the instruction.
- **Register** -- the operand is in a register.
- **Base + offset** -- `mem[reg + const]`, the workhorse for arrays and structs.
- **PC-relative** -- used for branches.

```c
/* C view: the compiler picks registers and addressing for you */
int sum(int *a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];  /* a[i] = base + offset */
    return s;
}
```

```python
# Python model of two's complement in a fixed word width
def to_signed(bits, n=8):
    return bits - (1 << n) if bits >= (1 << (n - 1)) else bits

print(to_signed(0b11111111))   # -1
print(to_signed(0b10000000))   # -128
```

**Next:** how an instruction physically executes -- the datapath.
""",
        ),
        _t(
            "The datapath and a single-cycle CPU",
            "13 min",
            """\
# The datapath and a single-cycle CPU

An ISA is a promise; the **datapath** is the hardware that keeps it. A
single-cycle CPU does one whole instruction every clock tick by routing bits
through a fixed set of blocks.

## The building blocks

- **Program counter (PC)** -- holds the address of the next instruction.
- **Register file** -- the 32 registers, with two read ports and one write port.
- **ALU** -- the arithmetic/logic unit: add, sub, and, or, compare, shift.
- **Memory** -- instruction memory (fetch) and data memory (load/store).
- **Control unit** -- decodes the opcode into the **control signals** that steer
  multiplexers and enable writes.

## Fetch-decode-execute

Every instruction walks the same cycle:

```mermaid
flowchart LR
  PC["PC"] --> IF["fetch instruction"]
  IF --> ID["decode + read registers"]
  ID --> EX["ALU execute"]
  EX --> MEM["memory access"]
  MEM --> WB["write back to register"]
  WB --> PC
```

## Control signals steer the datapath

The opcode picks the signals. For a load (`lw`): `ALUSrc=1` (use the immediate),
`MemRead=1`, `MemtoReg=1` (write the loaded value), `RegWrite=1`. For an add, the
ALU output goes straight back, memory is idle. One decode table drives the whole
machine.

## The single-cycle trade-off

Clock period must cover the **slowest** instruction's whole path (typically a
load: fetch + decode + ALU + memory + write). That wastes time on quick
instructions. Slide the load fraction and see why a single fixed period is
inefficient -- the average useful work per cycle drops as slow instructions
dominate:

```plot
{"title": "Single-cycle waste: clock fixed to the slowest path", "xLabel": "fraction of loads p", "yLabel": "relative work done per cycle", "xRange": [0, 1], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "ratio", "range": [1, 5], "value": 4, "label": "load path / add path ratio"}], "functions": [{"expr": "1/(1 + p*(ratio-1))", "label": "useful work per fixed cycle"}]}
```

```c
/* Conceptually, one instruction = one trip through the datapath */
int32_t alu(int32_t a, int32_t b, int op) {
    switch (op) {
        case 0: return a + b;   /* add */
        case 1: return a - b;   /* sub */
        case 2: return a & b;   /* and */
        case 3: return a | b;   /* or  */
    }
    return 0;
}
```

```python
# Python model of the ALU + control for one instruction
def alu(a, b, op):
    return {0: a + b, 1: a - b, 2: a & b, 3: a | b}[op]

print(alu(7, 5, 0), alu(7, 5, 1))   # 12 2
```

**Next:** where instructions and data live -- the memory hierarchy.
""",
        ),
        _t(
            "The memory hierarchy and buses",
            "12 min",
            """\
# The memory hierarchy and buses

A CPU is starved without memory to feed it -- but fast memory is small and
expensive, while big memory is slow. The fix is a **hierarchy**: layers that get
larger and slower as you move away from the core.

| Level | Typical size | Typical latency | Technology |
|-------|--------------|-----------------|------------|
| Registers | ~1 KB | <1 ns | flip-flops |
| L1 cache | tens of KB | ~1 ns | SRAM |
| L2/L3 cache | KB to MB | a few ns | SRAM |
| Main memory (RAM) | GB | ~100 ns | DRAM |
| Storage (SSD/disk) | TB | microseconds-ms | flash / magnetic |

Cost-per-bit and latency both climb steeply as you go up. Slide the level and
watch latency grow roughly geometrically:

```plot
{"title": "Memory hierarchy: latency rises with distance from the core", "xLabel": "hierarchy level (0=register .. 4=storage)", "yLabel": "relative latency (log-ish)", "xRange": [0, 4], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "pow(6, x)/3", "label": "relative access latency"}]}
```

## RAM vs ROM

- **RAM** (read/write, volatile) -- holds running programs and data; **DRAM** for
  bulk, **SRAM** for caches.
- **ROM / flash** (mostly read, non-volatile) -- holds firmware and boot code; a
  microcontroller's program lives here.

## Buses: address, data, control

A **bus** is the shared set of wires that carries information between the CPU,
memory, and I/O. Three logical groups:

- **Address bus** -- which location (its width sets the max addressable memory:
  $2^{\\text{bits}}$).
- **Data bus** -- the bits being read or written.
- **Control bus** -- read/write strobes, clock, interrupt lines.

```mermaid
flowchart LR
  CPU["CPU"] -->|address| MEM["memory"]
  CPU -->|control| MEM
  CPU <-->|data| MEM
```

## von Neumann vs Harvard

- **von Neumann** -- one memory and one bus for **both** instructions and data.
  Simple, flexible, but the single bus is a bottleneck (the "von Neumann
  bottleneck").
- **Harvard** -- **separate** instruction and data memories/buses, so the CPU can
  fetch an instruction and read data at the same time. Most CPUs are von Neumann
  at the main-memory level but **Harvard at the L1 cache** (split I-cache and
  D-cache) -- the best of both.

```python
# Address-bus width sets the addressable range
for bits in (16, 20, 32):
    print(bits, "bits ->", 2 ** bits, "addressable bytes")
```

**Next:** writing instructions by hand -- assembly basics.
""",
        ),
        _t(
            "Assembly programming basics",
            "13 min",
            """\
# Assembly programming basics

**Assembly** is a human-readable, one-to-one view of machine instructions. We use
**RISC-V** (a clean, free, modern RISC ISA used from microcontrollers to
supercomputers), but **MIPS** and **ARM** look almost identical.

## A first program

RISC-V has 32 integer registers (`x0`-`x31`, `x0` is always zero) and a
load/store design: only `lw`/`sw` touch memory; everything else works on
registers.

```c
/* The C we want to translate */
int add3(int a, int b, int c) {
    return a + b + c;
}
```

```python
# A Python model of the same register machine
def add3(a, b, c):
    t0 = a + b       # add t0, a0, a1
    t0 = t0 + c      # add t0, t0, a2
    return t0        # mv a0, t0 ; ret

print(add3(2, 3, 4))   # 9
```

In RISC-V assembly that is literally:

```c
/* RISC-V assembly (a0,a1,a2 = args; a0 = return value) */
add3:
    add  t0, a0, a1     /* t0 = a + b           */
    add  a0, t0, a2     /* a0 = t0 + c (return) */
    ret
```

## The stack and the calling convention

The **stack** is a region of memory that grows downward, addressed by the **stack
pointer** (`sp`). Functions use it for local variables and to save registers. The
**calling convention** is the ABI agreement so any function can call any other:

- Arguments go in `a0`-`a7`; the return value comes back in `a0`.
- **Caller-saved** registers (`t0`-`t6`) may be clobbered by a call; save them if
  you need them after.
- **Callee-saved** registers (`s0`-`s11`) must be preserved by the function that
  uses them.
- The **return address** is in `ra`; nested calls save it on the stack.

```mermaid
flowchart TB
  HI["high addresses"] --> ARGS["caller frame"]
  ARGS --> RA["saved ra + saved s-regs"]
  RA --> LOCALS["locals"]
  LOCALS --> SP["sp (grows down)"]
```

A function with locals or calls builds a **stack frame** in its prologue and tears
it down in its epilogue:

```c
/* prologue: make room and save ra; epilogue: restore and return */
myfunc:
    addi sp, sp, -16    /* allocate frame      */
    sw   ra, 12(sp)     /* save return address */
    /* ... body, may call other functions ... */
    lw   ra, 12(sp)     /* restore             */
    addi sp, sp, 16     /* free frame          */
    ret
```

> **Practical insight:** stack depth grows with each nested call. Unbounded
> recursion overflows the stack -- the cause of the classic "stack overflow"
> crash. Compilers exploit the convention to inline and to keep hot variables in
> registers.

**Next:** how the CPU talks to the outside world -- I/O and buses.
""",
        ),
        _t(
            "I/O and buses: polling vs interrupts",
            "12 min",
            """\
# I/O and buses: polling vs interrupts

A CPU that only computes is useless -- it must read sensors, drive displays, and
move data to storage and the network. There are two big questions: **how** does
the CPU address a device, and **how** does it know a device needs attention?

## Memory-mapped I/O

The dominant scheme is **memory-mapped I/O (MMIO)**: device registers live at
ordinary memory addresses. To turn on an LED you just *write* to a magic address;
to read a button you *read* one. No special instructions -- the same `lw`/`sw`
work. (x86 also has a separate **port I/O** address space, the legacy
alternative.)

```c
/* Memory-mapped GPIO on a microcontroller */
#define GPIO_OUT (*(volatile unsigned int *)0x40020014)
GPIO_OUT |= (1 << 5);   /* set bit 5 high -> LED on */
```

```python
# Python model of an MMIO write into a device-register map
regs = {0x40020014: 0}
def mmio_write(addr, value):
    regs[addr] = value
mmio_write(0x40020014, 1 << 5)
print(hex(regs[0x40020014]))   # 0x20
```

The `volatile` keyword in C is essential: it tells the compiler the value can
change outside the program's control, so it must not cache or reorder the access.

## Polling vs interrupts

How does the CPU learn that a key was pressed or a byte arrived?

- **Polling** -- the CPU repeatedly reads a status register in a loop. Simple and
  predictable, but it **burns cycles** spinning and adds latency proportional to
  the poll period.
- **Interrupts** -- the device raises a line; the CPU finishes the current
  instruction, jumps to an **interrupt service routine (ISR)**, handles the event,
  and returns. Efficient -- the CPU does real work until something actually
  happens.

```mermaid
stateDiagram-v2
  [*] --> Running
  Running --> ISR: device asserts IRQ
  ISR --> Running: iret (restore state)
  Running --> Running: poll loop (wastes cycles)
```

## The cost trade-off

Polling wastes CPU on idle checks; interrupts add a fixed **handler overhead** per
event (save/restore state, jump). For rare events, interrupts win big; for very
frequent events, the per-interrupt overhead can dominate and polling (or DMA)
wins. Slide the event rate and watch the crossover:

```plot
{"title": "CPU spent on I/O: polling vs interrupts (slide overhead)", "xLabel": "events per second (thousands)", "yLabel": "CPU fraction spent on I/O", "xRange": [0, 100], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "ovh", "range": [1, 20], "value": 5, "label": "interrupt overhead (us)"}], "functions": [{"expr": "0.5", "label": "polling (fixed spin cost)", "color": "#2563eb"}, {"expr": "min(1, x*ovh/1000)", "label": "interrupts (grows with rate)", "color": "#dc2626"}]}
```

## DMA: cut the CPU out of the loop

For bulk transfers (disk, network, audio), a **DMA controller** moves blocks
between a device and memory on its own, interrupting the CPU only when the whole
transfer is done. That's how a modern machine streams gigabytes without melting
the core.

> **Practical insight:** real systems layer all three -- interrupts to *notice*
> an event, DMA to *move* the bulk data, and a tiny bit of polling for the
> lowest-latency tight loops.

**Next:** build a tiny CPU and watch it run.
""",
        ),
        _code(
            "Lab: simulate a tiny CPU datapath",
            "14 min",
            """\
# Simulate a tiny accumulator CPU: fetch-decode-execute a small program,
# then plot register activity and cycles-per-instruction over the run.
import numpy as np
import matplotlib.pyplot as plt

# A 4-register machine. Instruction = (opcode, dst, src_or_imm, src2).
# Opcodes: 0 LOADI (dst=imm), 1 ADD (dst=src1+src2), 2 SUB, 3 OUT (print reg).
NOP, LOADI, ADD, SUB, OUT = -1, 0, 1, 2, 3

# Program: compute (10 + 5) then (result - 3) into registers, output each step.
program = [
    (LOADI, 0, 10, 0),   # r0 = 10
    (LOADI, 1, 5, 0),    # r1 = 5
    (ADD, 2, 0, 1),      # r2 = r0 + r1 = 15
    (LOADI, 3, 3, 0),    # r3 = 3
    (SUB, 2, 2, 3),      # r2 = r2 - r3 = 12
    (OUT, 2, 0, 0),      # output r2
]

# Per-opcode cycle cost (models a multi-cycle machine, not single-cycle).
cost = {LOADI: 1, ADD: 2, SUB: 2, OUT: 3}

regs = np.zeros(4, dtype=int)
pc = 0
cycle = 0
reg_trace = []      # snapshot of all registers after each instruction
cpi_trace = []      # cycles taken by each instruction
outputs = []

# Fetch-decode-execute loop, all at module level.
while pc < len(program):
    op, dst, a, b = program[pc]     # FETCH + DECODE
    if op == LOADI:                 # EXECUTE
        regs[dst] = a
    elif op == ADD:
        regs[dst] = regs[a] + regs[b]
    elif op == SUB:
        regs[dst] = regs[a] - regs[b]
    elif op == OUT:
        outputs.append(int(regs[dst]))
    cycle += cost[op]
    cpi_trace.append(cost[op])
    reg_trace.append(regs.copy())
    pc += 1                         # next instruction

reg_trace = np.array(reg_trace)
steps = np.arange(1, len(program) + 1)
avg_cpi = cycle / len(program)

print("program output:", outputs)         # [12]
print(f"total cycles = {cycle}, instructions = {len(program)}")
print(f"average CPI = {avg_cpi:.2f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
colors = ["#2563eb", "#16a34a", "#dc2626", "#9333ea"]
for r in range(4):
    ax1.plot(steps, reg_trace[:, r], marker="o", color=colors[r], label=f"r{r}")
ax1.set_xlabel("instruction #"); ax1.set_ylabel("register value")
ax1.set_title("Register activity over the run"); ax1.legend(); ax1.grid(True)

ax2.bar(steps, cpi_trace, color="#0ea5e9")
ax2.axhline(avg_cpi, ls="--", color="#dc2626", label=f"avg CPI = {avg_cpi:.2f}")
ax2.set_xlabel("instruction #"); ax2.set_ylabel("cycles")
ax2.set_title("Cycles per instruction"); ax2.legend(); ax2.grid(True, axis="y")
plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Add more ADD/SUB instructions and watch the average CPI climb.
#   2. Change the cost dict to model a single-cycle machine (all costs = 1).
""",
        ),
    ),
)


# -- Computer Architecture & Organization -- Intermediate ----------------------

_COMPARCH_INTERMEDIATE = SeedCourse(
    slug="comparch-intermediate",
    title="Computer Architecture & Organization -- Intermediate: Pipelining & Memory",
    description=(
        "How real CPUs go fast: the 5-stage pipeline and throughput vs latency, "
        "the hazards that break it and how forwarding/stalls fix them, caches and "
        "AMAT, virtual memory with paging and the TLB, and performance evaluation "
        "with CPI and Amdahl's law -- dual assembly/C and Python, interactive "
        "plots, and a runnable cache / pipeline-speedup lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pipelining: the 5-stage pipeline",
            "13 min",
            """\
# Pipelining: the 5-stage pipeline

Single-cycle CPUs waste time waiting for the slowest instruction. **Pipelining**
borrows the assembly-line idea: split instruction processing into stages and work
on several instructions at once, each in a different stage.

The classic RISC pipeline has **5 stages**:

| Stage | Name | Does |
|-------|------|------|
| IF | Fetch | read the instruction from memory |
| ID | Decode | decode + read registers |
| EX | Execute | ALU operation / address calc |
| MEM | Memory | load or store data |
| WB | Write-back | write the result to a register |

```mermaid
flowchart LR
  IF["IF"] --> ID["ID"] --> EX["EX"] --> MEM["MEM"] --> WB["WB"]
```

## Throughput vs latency

Pipelining does **not** make a single instruction faster -- its **latency** is
still 5 stages. What improves is **throughput**: once the pipe is full, one
instruction *completes* every cycle. With $N$ instructions and $k$ stages, time
is $N + k - 1$ cycles instead of $N \\cdot k$. The speedup approaches $k$ for
large $N$:

$$\\text{speedup} = \\frac{N \\cdot k}{N + k - 1} \\xrightarrow[N \\to \\infty]{} k.$$

Slide the program length and watch speedup climb toward the stage count:

```plot
{"title": "Pipeline speedup vs program length (slide stage count k)", "xLabel": "number of instructions N", "yLabel": "speedup vs single-cycle", "xRange": [1, 100], "yRange": [0, 9], "grid": true, "controls": [{"name": "k", "range": [2, 8], "value": 5, "label": "pipeline stages k"}], "functions": [{"expr": "x*k/(x + k - 1)", "label": "speedup"}, {"expr": "k", "label": "ideal limit = k", "color": "#94a3b8"}]}
```

## Pipeline registers

Between every pair of stages sit **pipeline registers** (IF/ID, ID/EX, EX/MEM,
MEM/WB). They latch the partial results and control signals so each stage hands a
clean snapshot to the next on every clock edge -- the conveyor belts of the line.

The clock period now only has to cover the **slowest single stage**, not the
whole instruction, so the clock can run much faster.

```c
/* Conceptually, three instructions overlap in flight:
   cycle:  1   2   3   4   5   6   7
   i1:     IF  ID  EX  MEM WB
   i2:         IF  ID  EX  MEM WB
   i3:             IF  ID  EX  MEM WB
*/
```

```python
# Model pipeline fill: cycles to finish N instructions with k stages
def pipe_cycles(N, k=5):
    return N + k - 1
def speedup(N, k=5):
    return (N * k) / pipe_cycles(N, k)
print(speedup(1), speedup(100))   # 1.0 ~ 4.81
```

> **Practical insight:** deeper pipelines (Intel's Pentium 4 reached ~20 stages)
> raise the clock but make each stall and misprediction cost more. There's a
> sweet spot -- modern cores sit around 12-20 stages.

**Next:** what stalls the line -- hazards.
""",
        ),
        _t(
            "Hazards: structural, data, and control",
            "13 min",
            """\
# Hazards: structural, data, and control

A pipeline is fast *only* when instructions flow without interference. A
**hazard** is anything that forces the pipeline to wait or do the wrong thing.
There are three kinds.

## Structural hazards

Two instructions need the **same hardware resource** in the same cycle (e.g. one
memory port for both a fetch and a load). Fix: duplicate the resource -- which is
exactly why CPUs use **split I-cache and D-cache** (the Harvard idea from the
Basics course).

## Data hazards

An instruction needs a result that an earlier, still-in-flight instruction hasn't
written back yet:

```c
add  t0, a0, a1    /* writes t0 in WB (cycle 5)   */
sub  t1, t0, a2    /* needs t0 in EX  (cycle 3!)  */
```

Two fixes:

- **Forwarding (bypassing)** -- route the ALU result *directly* from EX/MEM back
  into the next instruction's EX input, before write-back. Eliminates most data
  hazards with no stall.
- **Stall (bubble)** -- when forwarding can't help (a `lw` result isn't ready
  until after MEM), insert a no-op cycle. This is the **load-use hazard**, and it
  costs one bubble.

```mermaid
flowchart LR
  EX["EX (produces result)"] -->|forward| EX2["next instr EX"]
  MEM["MEM (load result)"] -->|1 stall, then forward| ID["dependent instr"]
```

## Control hazards

A **branch** isn't resolved until a later stage, but the pipeline has already
fetched the instructions *after* it -- which may be wrong. Handling:

- **Stall** until the branch resolves (simplest, slowest).
- **Predict** the branch and speculatively fetch; squash if wrong (next course).
- **Delay slot** -- the MIPS trick: always execute the instruction after a branch.

## The cost of stalls

Stalls inflate the effective cycles-per-instruction. If a fraction $f$ of
instructions stall for $p$ penalty cycles, $\\text{CPI} = 1 + f \\cdot p$. Slide
the branch frequency and the penalty:

```plot
{"title": "Effective CPI vs stall fraction (slide branch penalty)", "xLabel": "fraction of stalling instructions f", "yLabel": "effective CPI", "xRange": [0, 0.5], "yRange": [1, 3], "grid": true, "controls": [{"name": "p", "range": [1, 4], "value": 2, "label": "penalty cycles per stall"}], "functions": [{"expr": "1 + x*p", "label": "CPI = 1 + f*p"}]}
```

```python
# Model effective CPI from stalls
def cpi(stall_fraction, penalty):
    return 1 + stall_fraction * penalty
print(cpi(0.20, 2))   # 1.4
```

> **Practical insight:** forwarding makes most arithmetic dependencies free, so
> compilers focus on **scheduling around load-use stalls and branches** -- moving
> independent work in between to fill the gaps.

**Next:** the memory wall and how caches hide it.
""",
        ),
        _t(
            "Caches, locality, and AMAT",
            "13 min",
            """\
# Caches, locality, and AMAT

Main memory is ~100x slower than the core. A **cache** is a small, fast SRAM that
holds recently and nearby-used data, exploiting **locality**:

- **Temporal locality** -- if you used an address, you'll likely use it again
  soon (loop counters, hot variables).
- **Spatial locality** -- if you used an address, you'll likely use its neighbours
  soon (arrays, instruction streams). Caches fetch a whole **block (line)** to
  capture this.

## Mapping: where can a block live?

- **Direct-mapped** -- each block has exactly one slot (`index = address mod
  #lines`). Cheap and fast, but two hot blocks that map to the same slot keep
  evicting each other (**conflict misses**).
- **Set-associative** -- each block may live in any of $w$ ways within its set. An
  $w$-way cache trades a little speed/power for far fewer conflict misses.
- **Fully associative** -- a block can go anywhere (no conflict misses, expensive).

```mermaid
flowchart LR
  ADDR["address"] --> TAG["tag"]
  ADDR --> IDX["index -> set"]
  ADDR --> OFF["block offset"]
  IDX --> SET["set: compare tag in each way"]
```

Higher associativity shrinks the miss rate with diminishing returns -- slide it:

```plot
{"title": "Miss rate vs associativity (diminishing returns), slide size", "xLabel": "associativity (ways)", "yLabel": "relative miss rate", "xRange": [1, 16], "yRange": [0, 0.12], "grid": true, "controls": [{"name": "kb", "range": [4, 64], "value": 16, "label": "cache size (KB)"}], "functions": [{"expr": "0.12*exp(-0.4*x)*16/kb + 0.005", "label": "miss rate model"}]}
```

## Hit, miss, and write policies

A **hit** is found in cache (fast); a **miss** must fetch the block from the next
level (slow), evicting a victim (LRU is the usual policy). On a write:

- **Write-through** -- write to cache *and* memory (simple, more memory traffic).
- **Write-back** -- write only to cache, mark the line **dirty**, flush on
  eviction (less traffic, the common choice).

## AMAT: the bottom line

**Average Memory Access Time** combines it all:

$$\\text{AMAT} = t_{hit} + \\text{miss rate} \\times \\text{miss penalty}.$$

Because the miss penalty is huge (~100 cycles), even a small miss rate dominates.
Slide the miss penalty and watch AMAT explode with a modest miss rate:

```plot
{"title": "AMAT = hit + miss_rate * penalty (slide penalty)", "xLabel": "miss rate", "yLabel": "AMAT (cycles)", "xRange": [0, 0.2], "yRange": [0, 25], "grid": true, "controls": [{"name": "pen", "range": [20, 200], "value": 100, "label": "miss penalty (cycles)"}], "functions": [{"expr": "1 + x*pen", "label": "AMAT"}]}
```

```c
/* Cache-friendly: stride-1 (row-major) walk hits spatial locality.
   Swapping the loops to column-major causes a miss almost every access. */
for (int i = 0; i < N; i++)
    for (int j = 0; j < N; j++)
        sum += A[i][j];   /* contiguous -> few misses */
```

```python
# AMAT model
def amat(t_hit, miss_rate, penalty):
    return t_hit + miss_rate * penalty
print(amat(1, 0.05, 100))   # 6.0 cycles
```

**Next:** giving every program its own private memory -- virtual memory.
""",
        ),
        _t(
            "Virtual memory, paging, and the TLB",
            "12 min",
            """\
# Virtual memory, paging, and the TLB

**Virtual memory** gives every process the illusion of a large, private, contiguous
address space, while the hardware and OS map it onto whatever physical RAM is
free (and spill the rest to disk). It provides **isolation** (one process can't
touch another's memory), **relocation**, and the ability to run programs larger
than physical RAM.

## Paging

Memory is split into fixed-size **pages** (commonly 4 KB). A **page table** maps
each virtual page to a physical **frame**. A virtual address splits into a **page
number** (the table index) and a **page offset** (untouched):

$$\\underbrace{\\text{VPN}}_{\\text{which page}} \\;\\Vert\\; \\underbrace{\\text{offset}}_{\\text{within page}} \\;\\to\\; \\text{PFN} \\;\\Vert\\; \\text{offset}.$$

```mermaid
flowchart LR
  VA["virtual address"] --> VPN["page number"]
  VA --> OFF["offset"]
  VPN --> PT["page table -> frame number"]
  PT --> PA["physical address"]
  OFF --> PA
```

## The TLB: caching translations

A page-table lookup is itself a memory access -- doing one per instruction would
be ruinous. The **Translation Lookaside Buffer (TLB)** is a small, fast cache of
recent virtual-to-physical translations. A **TLB hit** translates in ~1 cycle; a
**TLB miss** walks the page table (slow), and a **page fault** (page not in RAM
at all) traps to the OS to load it from disk.

The effective translation time depends heavily on the TLB hit rate -- slide it:

```plot
{"title": "Translation cost vs TLB hit rate (slide walk cost)", "xLabel": "TLB hit rate", "yLabel": "avg translation time (cycles)", "xRange": [0.8, 1], "yRange": [0, 30], "grid": true, "controls": [{"name": "walk", "range": [10, 100], "value": 40, "label": "page-walk cost (cycles)"}], "functions": [{"expr": "1 + (1-x)*walk", "label": "avg translation time"}]}
```

## Why huge pages help

A bigger page (2 MB "huge page") means each TLB entry covers more memory, so the
**TLB reach** grows and miss rates drop for large data sets -- a real tuning knob
for databases and ML workloads.

```c
/* Address breakdown for 4 KB pages (12-bit offset) */
unsigned vpn    = vaddr >> 12;      /* virtual page number */
unsigned offset = vaddr & 0xFFF;    /* low 12 bits, unchanged */
```

```python
# Virtual-to-physical translation model (4 KB pages)
PAGE_BITS = 12
page_table = {0: 7, 1: 3, 2: 9}     # vpn -> frame number
def translate(vaddr):
    vpn, off = vaddr >> PAGE_BITS, vaddr & ((1 << PAGE_BITS) - 1)
    return (page_table[vpn] << PAGE_BITS) | off
print(hex(translate(0x1ABC)))       # frame 3 + offset 0xABC
```

> **Practical insight:** virtual memory is why a crashing program takes down only
> itself, why `malloc` can hand out gigabytes that don't exist yet (lazy
> allocation), and why memory-mapped files work. The TLB is one of the most
> performance-critical caches in the machine.

**Next:** measuring it all honestly -- performance evaluation.
""",
        ),
        _t(
            "Performance evaluation: CPI and Amdahl's law",
            "12 min",
            """\
# Performance evaluation: CPI and Amdahl's law

You can't improve what you can't measure honestly -- and CPU performance is full
of misleading single numbers (clock speed alone says little).

## The iron law of performance

Execution time decomposes exactly:

$$\\text{time} = \\frac{\\text{instructions}}{\\text{program}} \\times \\frac{\\text{cycles}}{\\text{instruction}} \\times \\frac{\\text{seconds}}{\\text{cycle}}.$$

That is **instruction count $\\times$ CPI $\\times$ clock period**. A faster clock
(smaller period), fewer instructions (better ISA/compiler), or lower **CPI**
(better microarchitecture) all help -- and they trade off against each other.
The combined metric people quote is **IPC** (instructions per cycle = $1/$CPI).

## Amdahl's law: the tyranny of the serial part

If you speed up a fraction $p$ of the work by a factor $s$, the overall speedup is

$$\\text{speedup} = \\frac{1}{(1-p) + \\dfrac{p}{s}}.$$

The brutal consequence: even with $s \\to \\infty$, speedup is capped at
$1/(1-p)$. Optimize the part that dominates the runtime, not the part that's easy.
Slide the parallel/optimizable fraction:

```plot
{"title": "Amdahl's law: speedup vs how much you parallelize (slide p)", "xLabel": "speedup s of the optimized part", "yLabel": "overall speedup", "xRange": [1, 32], "yRange": [0, 12], "grid": true, "controls": [{"name": "p", "range": [0.5, 0.95], "value": 0.8, "label": "fraction that is optimizable p"}], "functions": [{"expr": "1/((1-p) + p/x)", "label": "overall speedup"}, {"expr": "1/(1-p)", "label": "hard ceiling 1/(1-p)", "color": "#94a3b8"}]}
```

## Benchmarking honestly

- Use **real workloads** or standard suites (**SPEC CPU**, and domain ones like
  **MLPerf** for ML) -- not contrived microbenchmarks.
- Report the **right mean**: use the **geometric mean** for normalized ratios; the
  arithmetic mean of speedups is misleading.
- Beware that performance depends on the *whole* system (caches, memory, I/O), not
  just the CPU clock -- the "**MHz myth**".

```c
/* Iron law in code: estimate runtime from the three factors */
double time(double instructions, double cpi, double clock_hz) {
    return instructions * cpi / clock_hz;
}
```

```python
# Amdahl's law and the iron law
def amdahl(p, s):
    return 1 / ((1 - p) + p / s)
def cpu_time(instructions, cpi, clock_hz):
    return instructions * cpi / clock_hz
print(round(amdahl(0.8, 1e9), 2))   # ~5.0 -> ceiling is 1/(1-0.8)=5
```

> **Practical insight:** Amdahl's law is why throwing 64 cores at a problem that
> is 10% serial gives you at most a ~9x speedup. It governs everything from GPU
> offload to choosing what to optimize first.

**Next:** model caches and pipeline speedup yourself.
""",
        ),
        _code(
            "Lab: cache hit-rate and pipeline speedup",
            "14 min",
            """\
# Two experiments: (1) measure cache miss rate vs associativity for a real
# access stream, and (2) plot pipeline + Amdahl speedup. All at module level.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

# ---- Experiment 1: a set-associative cache simulator ----
N_ACCESSES = 4000
N_SETS = 64
BLOCK = 1            # one address per block, for simplicity
# Access stream: mostly a small hot working set (locality) + some random tail.
hot = rng.integers(0, 96, size=int(N_ACCESSES * 0.8))
cold = rng.integers(0, 4000, size=N_ACCESSES - len(hot))
stream = np.concatenate([hot, cold])
rng.shuffle(stream)

assoc_values = [1, 2, 4, 8, 16]
miss_rates = []
for ways in assoc_values:
    # cache[set] = list of tags (LRU: most-recent at the end)
    cache = [[] for _ in range(N_SETS)]
    misses = 0
    for addr in stream:
        s = (addr // BLOCK) % N_SETS
        tag = addr // BLOCK // N_SETS
        way = cache[s]
        if tag in way:                 # HIT: move to most-recent
            way.remove(tag)
            way.append(tag)
        else:                          # MISS: insert, evict LRU if full
            misses += 1
            if len(way) >= ways:
                way.pop(0)
            way.append(tag)
    miss_rates.append(misses / len(stream))

miss_rates = np.array(miss_rates)
print("associativity:", assoc_values)
print("miss rates:   ", np.round(miss_rates, 4))

# ---- Experiment 2: pipeline + Amdahl speedup curves ----
N = np.arange(1, 60)
k = 5
pipe_speedup = N * k / (N + k - 1)        # approaches k as N grows

s = np.linspace(1, 32, 60)
p = 0.8
amdahl_speedup = 1 / ((1 - p) + p / s)    # ceiling at 1/(1-p) = 5

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(assoc_values, miss_rates, marker="o", color="#2563eb")
ax1.set_xscale("log", base=2)
ax1.set_xlabel("associativity (ways)"); ax1.set_ylabel("miss rate")
ax1.set_title("Cache miss rate vs associativity"); ax1.grid(True)

ax2.plot(N, pipe_speedup, color="#16a34a", label="pipeline (k=5)")
ax2.axhline(k, ls="--", color="#16a34a", alpha=0.5)
ax2.plot(s, amdahl_speedup, color="#dc2626", label="Amdahl (p=0.8)")
ax2.axhline(1 / (1 - p), ls="--", color="#dc2626", alpha=0.5)
ax2.set_xlabel("N instructions  /  speedup s")
ax2.set_ylabel("overall speedup")
ax2.set_title("Pipeline vs Amdahl speedup"); ax2.legend(); ax2.grid(True)
plt.tight_layout(); plt.show()

print(f"direct-mapped miss rate = {miss_rates[0]:.3f}, "
      f"16-way = {miss_rates[-1]:.3f}")

# Try it yourself:
#   1. Shrink N_SETS to 8: conflict misses rise, associativity helps more.
#   2. Make the hot set bigger than the cache: capacity misses dominate.
""",
        ),
    ),
)


# -- Computer Architecture & Organization -- Advanced --------------------------

_COMPARCH_ADVANCED = SeedCourse(
    slug="comparch-advanced",
    title="Computer Architecture & Organization -- Advanced: ILP, Parallelism & SoC",
    description=(
        "Modern high-performance architecture: instruction-level parallelism with "
        "superscalar and out-of-order execution (Tomasulo, register renaming, "
        "speculation), branch prediction, multicore and MESI cache coherence, "
        "accelerators and the roofline model (SIMD, GPU, systolic arrays, ML "
        "hardware), and SoC/modern systems -- dual assembly/C and Python, "
        "interactive plots, and a runnable branch-prediction / roofline lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Instruction-level parallelism and out-of-order execution",
            "14 min",
            """\
# Instruction-level parallelism and out-of-order execution

A pipeline overlaps instructions but still issues them in order, one per cycle at
best. **Instruction-level parallelism (ILP)** goes further: find independent
instructions and run several **at once**.

## Superscalar

A **superscalar** core has multiple execution units (several ALUs, a load unit, a
store unit) and can **issue 2-8 instructions per cycle**. The ideal CPI drops
below 1 (IPC > 1). But real code rarely has that much independent work back to
back -- dependencies stall the issue.

## Out-of-order (OoO) execution

Instead of stalling on a dependency, an **out-of-order** core executes ready
instructions while a stalled one waits (e.g. for a cache miss), then **retires**
results in program order so the architectural state stays correct. The pattern:

```mermaid
flowchart LR
  FETCH["fetch + decode (in order)"] --> RENAME["register rename"]
  RENAME --> RS["reservation stations / scheduler"]
  RS --> EX["execute when operands ready (out of order)"]
  EX --> ROB["reorder buffer"]
  ROB --> RETIRE["retire (in order)"]
```

## Register renaming kills false dependencies

Two instructions writing the same architectural register create a **false
dependency (WAR / WAW)** even when there's no real data flow. **Register
renaming** maps architectural registers to a larger pool of **physical
registers**, so independent uses get different physical names and run in parallel.
This is the key enabler of OoO.

## Tomasulo's algorithm and speculation

**Tomasulo's algorithm** (IBM 360/91, 1967) implements OoO with **reservation
stations** that hold instructions until their operands arrive on a **common data
bus**, plus implicit renaming via tags. Combined with **speculation** (executing
past unresolved branches and squashing if wrong, all tracked by a **reorder
buffer**), it's the blueprint inside essentially every high-performance core
today.

## The limit of ILP

Available ILP is finite -- dependency chains and branches cap it. Wider issue
gives diminishing returns; that's a big reason the industry pivoted to
**multicore**. Slide the issue width:

```plot
{"title": "ILP: realized IPC vs issue width (diminishing returns)", "xLabel": "issue width (instructions/cycle)", "yLabel": "realized IPC", "xRange": [1, 8], "yRange": [0, 5], "grid": true, "controls": [{"name": "ilp", "range": [2, 6], "value": 3, "label": "available ILP in the code"}], "functions": [{"expr": "ilp*x/(ilp + x - 1)", "label": "realized IPC"}, {"expr": "ilp", "label": "ILP ceiling", "color": "#94a3b8"}]}
```

```c
/* Independent ops (no shared registers) can issue together;
   the chain below is serial -- each line needs the previous result. */
a = x + y;   /* could run with... */
b = p + q;   /* ...this (independent) */
c = a + b;   /* but this must wait for both */
```

```python
# Model realized IPC: harmonic blend of issue width and available ILP
def realized_ipc(issue_width, ilp):
    return ilp * issue_width / (ilp + issue_width - 1)
print(round(realized_ipc(4, 3), 2))   # ~2.0
```

**Next:** the biggest threat to ILP -- branches.
""",
        ),
        _t(
            "Branch prediction",
            "13 min",
            """\
# Branch prediction

Roughly **one in five** instructions is a branch. A deep, wide, speculative core
has fetched and partly executed *dozens* of instructions before a branch
resolves -- if it guessed wrong, all that work is thrown away. **Branch
prediction** is what keeps the pipeline fed.

## Static prediction

Fixed rules with no runtime state: "predict backward branches taken" (loops
usually repeat), "forward not taken". Cheap, and surprisingly decent for loops.

## Dynamic prediction

Learn from history at runtime:

- **1-bit predictor** -- remember the last outcome; mispredicts **twice** per loop
  (entry and exit).
- **2-bit saturating counter** -- needs **two** wrong guesses to flip, so a loop
  mispredicts only **once** (on exit). The classic baseline.
- **Correlating / two-level** -- index a table by recent global history, capturing
  patterns like "if branch A was taken, branch B usually is too".
- **Tournament / TAGE** -- combine multiple predictors and pick the best per
  branch; modern predictors exceed **95-99%** accuracy.

```mermaid
stateDiagram-v2
  [*] --> StrongNT
  StrongNT --> WeakNT: taken
  WeakNT --> WeakT: taken
  WeakT --> StrongT: taken
  StrongT --> WeakT: not taken
  WeakT --> WeakNT: not taken
  WeakNT --> StrongNT: not taken
```

## BHT and BTB

- **Branch History Table (BHT/PHT)** -- the array of 2-bit counters indexed by
  branch address: predicts the **direction** (taken/not).
- **Branch Target Buffer (BTB)** -- caches the **target address** so the next
  fetch can start immediately, before decode even knows it was a branch.

## The cost of misprediction

A misprediction flushes the speculative work and refills the pipe -- a penalty of
the pipeline depth (10-20+ cycles). The effective CPI penalty is
$\\text{branch freq} \\times \\text{miss rate} \\times \\text{penalty}$. Even 5%
mispredicts hurt at deep pipelines -- slide the accuracy:

```plot
{"title": "Branch misprediction CPI penalty (slide pipeline depth)", "xLabel": "predictor accuracy", "yLabel": "added CPI from branches", "xRange": [0.8, 1], "yRange": [0, 1], "grid": true, "controls": [{"name": "depth", "range": [5, 20], "value": 15, "label": "misprediction penalty (cycles)"}], "functions": [{"expr": "0.2*(1-x)*depth", "label": "added CPI (20% branches)"}]}
```

```c
/* Why branchless code can win: replace an unpredictable branch with arithmetic */
int max_branchy(int a, int b) { return (a > b) ? a : b; }   /* may mispredict */
int max_branchless(int a, int b) { return a ^ ((a ^ b) & -(a < b)); }
```

```python
# 2-bit saturating counter on a loop pattern (mostly taken, exits once)
def two_bit(outcomes):
    state, mispred = 3, 0   # 3 = strongly taken
    for taken in outcomes:
        pred = state >= 2
        if pred != taken:
            mispred += 1
        state = min(3, state + 1) if taken else max(0, state - 1)
    return mispred
loop = [1] * 9 + [0]        # 9 iterations then exit
print(two_bit(loop * 5))    # only a few mispredicts across 5 loops
```

> **Practical insight:** unpredictable data-dependent branches (e.g. sorting
> random data) are a top performance killer. Sorting input first, using branchless
> code, or **`__builtin_expect`/`[[likely]]`** hints can all help.

**Next:** going wide with many cores -- and keeping their caches honest.
""",
        ),
        _t(
            "Multicore and memory consistency",
            "13 min",
            """\
# Multicore and memory consistency

When ILP ran out of steam, the industry went **parallel**: put many cores on a
chip. That solves the throughput problem but creates a new one -- the cores share
memory, and each has its **own cache**. What happens when two caches hold the same
line and one core writes it?

## Cache coherence and MESI

**Coherence** guarantees all cores see a consistent view of each memory location.
The standard mechanism is a **snooping** protocol like **MESI**, where every cache
line is in one of four states:

| State | Meaning |
|-------|---------|
| **M** odified | this cache has the only, dirty copy |
| **E** xclusive | only copy, clean (matches memory) |
| **S** hared | possibly in other caches, clean |
| **I** nvalid | not valid here |

```mermaid
stateDiagram-v2
  [*] --> Invalid
  Invalid --> Exclusive: read miss (no other copy)
  Invalid --> Shared: read miss (others have it)
  Exclusive --> Modified: local write
  Shared --> Modified: local write (invalidate others)
  Modified --> Shared: another core reads
  Shared --> Invalid: another core writes
```

A write must **invalidate** other copies first -- which costs cross-core traffic.

## False sharing: the silent performance killer

If two cores write **different variables that happen to share one cache line**,
the line ping-pongs between them via invalidations even though there's no real
sharing. The cure is **padding/aligning** hot per-core data to separate cache
lines. Slide the contention and watch effective bandwidth collapse:

```plot
{"title": "False sharing: throughput collapses with contention (slide cores)", "xLabel": "write contention level", "yLabel": "relative throughput", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "controls": [{"name": "cores", "range": [2, 16], "value": 8, "label": "cores hammering one line"}], "functions": [{"expr": "1/(1 + x*cores/10)", "label": "throughput with false sharing"}]}
```

## Shared vs distributed memory

- **Shared memory** -- all cores see one address space (multicore CPUs, SMP).
  Easy to program, hard to scale (coherence traffic grows).
- **Distributed memory** -- each node has private memory; communication is
  explicit message passing (clusters, supercomputers). Scales further, harder to
  program.

## Memory consistency and synchronization

**Consistency** is the *ordering* rule for memory operations across cores.
Hardware uses **relaxed** models for speed, so programmers need
**synchronization** -- **atomic** read-modify-write instructions
(`compare-and-swap`, `LL/SC`), **locks/mutexes**, and **memory barriers
(fences)** -- to enforce ordering where it matters.

```c
/* An atomic compare-and-swap: the building block of lock-free code */
_Bool cas(int *p, int expected, int desired) {
    return __atomic_compare_exchange_n(p, &expected, desired, 0,
                                       __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST);
}
```

```python
# Amdahl again, but the serial part is now lock contention
def parallel_speedup(cores, serial_fraction):
    return 1 / (serial_fraction + (1 - serial_fraction) / cores)
print(round(parallel_speedup(16, 0.1), 2))   # ~6.4, not 16
```

> **Practical insight:** the hardest bugs in parallel code -- data races, torn
> reads, lost updates -- come from missing synchronization on a relaxed memory
> model. "It worked on my machine" often means "the race didn't trigger today".

**Next:** specialized hardware that leaves general cores behind -- accelerators.
""",
        ),
        _t(
            "Accelerators, data parallelism, and the roofline model",
            "14 min",
            """\
# Accelerators, data parallelism, and the roofline model

When one program does the **same operation on huge amounts of data**, a general
CPU is wasteful. **Data-parallel accelerators** do that work massively in
parallel -- and they power modern graphics and machine learning.

## SIMD: one instruction, many data

**SIMD** (Single Instruction, Multiple Data) lanes apply one operation to a vector
of elements at once -- CPU extensions like **SSE/AVX** (x86) and **NEON/SVE**
(ARM). One `add` processes 8 or 16 numbers per instruction.

## GPUs

A **GPU** takes this to thousands of lightweight threads running in lockstep
(**SIMT**). It trades single-thread latency for enormous **throughput** and memory
bandwidth -- ideal for graphics, simulations, and the dense linear algebra at the
heart of deep learning.

## Systolic arrays and ML hardware

A **systolic array** is a grid of tiny multiply-accumulate cells that pump data
through rhythmically -- perfect for **matrix multiply**, the dominant operation in
neural networks. Google's **TPU**, the **matrix/tensor cores** in modern GPUs, and
many ML accelerators are built around this idea.

```mermaid
flowchart LR
  A["matrix A rows"] --> PE["grid of multiply-accumulate cells"]
  B["matrix B cols"] --> PE
  PE --> C["result matrix C streams out"]
```

## The roofline model

How fast can a kernel actually go on a given machine? The **roofline model**
plots attainable performance (FLOP/s) against **arithmetic intensity** (FLOPs per
byte of memory traffic):

$$\\text{attainable} = \\min(\\text{peak compute},\\; \\text{intensity} \\times \\text{peak bandwidth}).$$

Low-intensity kernels are **memory-bound** (on the sloped "roof"); high-intensity
ones are **compute-bound** (on the flat roof). The corner is the **ridge point**.
Slide the memory bandwidth and watch the sloped roof tilt:

```plot
{"title": "Roofline: attainable GFLOP/s vs arithmetic intensity (slide BW)", "xLabel": "arithmetic intensity (FLOP/byte)", "yLabel": "attainable GFLOP/s", "xRange": [0, 20], "yRange": [0, 1100], "grid": true, "controls": [{"name": "bw", "range": [50, 300], "value": 100, "label": "memory bandwidth (GB/s)"}], "functions": [{"expr": "min(1000, x*bw)", "label": "roofline (min of compute, BW*intensity)"}, {"expr": "1000", "label": "peak compute roof", "color": "#94a3b8"}]}
```

```c
/* SAXPY: y = a*x + y -- low arithmetic intensity (2 FLOP per ~12 bytes),
   so it is memory-bound and sits on the sloped roof. */
for (int i = 0; i < N; i++) y[i] = a * x[i] + y[i];
```

```python
# Roofline: which regime is a kernel in?
def attainable(intensity, peak_flops, bw):
    return min(peak_flops, intensity * bw)
ridge = 1000 / 100        # peak/BW = ridge-point intensity = 10 FLOP/byte
print("ridge point:", ridge, "FLOP/byte")
print(attainable(2, 1000, 100), attainable(20, 1000, 100))  # 200 (mem), 1000 (compute)
```

> **Practical insight:** the roofline tells you *what to fix*. A memory-bound
> kernel won't get faster from a beefier ALU -- you must raise arithmetic
> intensity (blocking/tiling, fusing ops, reusing data in cache) or buy more
> bandwidth.

**Next:** packing it all onto one chip -- the SoC.
""",
        ),
        _t(
            "SoC and modern systems",
            "13 min",
            """\
# SoC and modern systems

A modern chip is no longer "a CPU". It is a **System-on-Chip (SoC)**: cores,
caches, memory controllers, accelerators, and I/O, all integrated and talking over
an on-chip network. Think of the chip in a phone, a car, or a laptop.

## What's on a typical SoC

```mermaid
flowchart TB
  subgraph SoC
    CPU["CPU cluster (big.LITTLE cores)"]
    GPU["GPU"]
    NPU["NPU / ML accelerator"]
    MC["memory controller -> DRAM"]
    IO["I/O: USB, PCIe, display, radios"]
    NOC["network-on-chip (interconnect)"]
  end
  CPU --- NOC
  GPU --- NOC
  NPU --- NOC
  MC --- NOC
  IO --- NOC
```

## Memory controllers

The **memory controller** turns load/store requests into the precise DRAM command
sequences (activate, read/write, precharge), schedules them for bandwidth, and
handles refresh. It is a major performance lever -- reordering requests to exploit
open DRAM rows can multiply effective bandwidth.

## Network-on-chip (NoC)

With dozens of blocks on one die, a single shared bus can't keep up. A
**network-on-chip** routes packets between blocks over a mesh or ring of routers,
just like a tiny internet inside the chip -- scalable bandwidth and locality-aware
routing.

## Microcontroller vs application SoC

- A **microcontroller (MCU)** -- e.g. an ARM Cortex-M, an ESP32, an AVR -- packs a
  simple core, on-chip flash and SRAM, and peripherals (timers, ADC, GPIO, UART,
  SPI, I2C). Often Harvard, no MMU, runs bare-metal or an RTOS. It is the brain of
  appliances, sensors, and IoT devices.
- An **application SoC** -- e.g. a phone's Apple A-series/Snapdragon -- has
  multi-core OoO CPUs, GPU, NPU, an MMU and full OS (Linux/Android/iOS), and
  gigabytes of DRAM.

Heterogeneity is the theme: **big.LITTLE** pairs fast power-hungry cores with slow
efficient ones, and the scheduler migrates work to balance performance and battery.
Energy efficiency now matters as much as raw speed -- slide the performance target
and watch dynamic power rise steeply (it grows with voltage squared times frequency):

```plot
{"title": "Dynamic power vs clock frequency (P ~ f^3 region), slide efficiency", "xLabel": "relative clock frequency", "yLabel": "relative dynamic power", "xRange": [0, 2], "yRange": [0, 9], "grid": true, "controls": [{"name": "eff", "range": [1, 3], "value": 1, "label": "process efficiency factor"}], "functions": [{"expr": "pow(x,3)/eff", "label": "dynamic power (V^2 f, V ~ f)"}]}
```

```c
/* Bare-metal MCU: configure a peripheral via memory-mapped registers,
   no OS in sight. */
volatile uint32_t *TIMER_CTRL = (uint32_t *)0x40000000;
*TIMER_CTRL = 0x1;   /* start the timer */
```

```python
# Why higher clocks cost so much: dynamic power ~ C * V^2 * f, and V scales with f
def dynamic_power(freq, cap=1.0):
    voltage = freq            # voltage roughly tracks frequency
    return cap * voltage ** 2 * freq
print(dynamic_power(1.0), dynamic_power(1.5))   # 1.0 vs ~3.4
```

> **Practical insight:** because dynamic power rises roughly with the cube of
> frequency, two cores at half the clock can do the same work for far less power
> than one core at full clock -- the physics that drove the multicore era and
> mobile's efficiency cores.

**Next:** real applications and the throughline.
""",
        ),
        _t(
            "Applications, use cases, and the throughline",
            "12 min",
            """\
# Applications, use cases, and the throughline

Everything in this track shows up, by name, in the systems you use every day. This
final lesson connects the ideas to concrete machines.

## Where each idea lives in real hardware

| Concept | Real-world application |
|---------|------------------------|
| ISA stability | x86 binaries from the 1990s still run; Apple shifted Macs to ARM while keeping software working |
| Pipelining + ILP | every laptop/phone core; Apple M-series and AMD Zen issue many instructions per cycle |
| Branch prediction | the **Spectre/Meltdown** vulnerabilities exploited *speculative* execution -- security meets microarchitecture |
| Caches + locality | database and game engines are tuned for cache-friendly data layout (struct-of-arrays, tiling) |
| Virtual memory | process isolation in every OS; containers and VMs; memory-mapped files; `malloc` overcommit |
| MESI coherence | every multicore phone and server; lock-free data structures depend on it |
| SIMD / GPU / TPU | training and serving LLMs, image generation, video codecs, scientific simulation |
| Roofline model | ML engineers use it to decide whether a kernel needs more compute or more bandwidth |
| SoC + NoC | the chip in your phone, your car's ECUs, datacenter accelerators |

## Three worked use cases

- **Training a neural network.** Dominated by matrix multiply -> run on GPUs/TPUs
  (systolic arrays, SIMT). The roofline says raise arithmetic intensity via
  tiling; multi-GPU scaling is bounded by Amdahl (the serial setup) and by
  coherence/communication. Mixed precision trades accuracy for throughput.
- **A high-frequency trading engine.** Latency is everything: keep the hot path in
  L1/L2 (locality), avoid unpredictable branches (branchless code), pin threads to
  cores to avoid coherence traffic and false sharing, and bypass the OS with
  kernel-bypass networking.
- **An IoT temperature sensor.** A tiny Cortex-M MCU, Harvard, no MMU. Sleeps most
  of the time; an **interrupt** from a timer or the radio wakes it (polling would
  drain the battery). Memory-mapped peripherals read the ADC. Every joule counts.

## The throughline

A computer is **bits moving under a clock**: an ISA defines what the bits mean, a
datapath executes them, a pipeline overlaps them, ILP and multicore do more at
once, caches and virtual memory bridge the speed gap to memory, accelerators
specialize for data-parallel work, and an SoC integrates it all under a power
budget. Two laws bound everything: the **memory wall** (compute outran memory, so
hierarchy and locality rule) and **Amdahl's law** (the serial part limits every
parallel speedup). The implementations change every year; these principles do not.

> **Practical insight:** whatever you build -- a web service, a game, an ML model,
> an embedded controller -- performance comes from matching your data and control
> flow to the machine: feed the caches, predict the branches, parallelize the
> independent work, and respect the serial bottleneck.
""",
        ),
        _code(
            "Lab: branch-prediction accuracy and a roofline plot",
            "14 min",
            """\
# Two experiments: (1) compare 1-bit vs 2-bit branch predictors on realistic
# branch streams, and (2) draw a roofline and place real kernels on it.
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)

# ---- Experiment 1: branch predictors ----
# Build a branch outcome stream: nested loops (very predictable) plus a
# data-dependent branch (a coin flip -- the hard case).
loop_pattern = ([1] * 9 + [0]) * 30          # tight loop, exits each pass
random_branch = rng.integers(0, 2, size=300) # unpredictable
stream = np.array(loop_pattern + list(random_branch))

# 1-bit predictor: remember last outcome.
state1 = 1
mis1 = 0
for taken in stream:
    if (state1 == 1) != bool(taken):
        mis1 += 1
    state1 = int(taken)

# 2-bit saturating counter: needs two misses to flip.
state2 = 2
mis2 = 0
for taken in stream:
    pred = state2 >= 2
    if pred != bool(taken):
        mis2 += 1
    state2 = min(3, state2 + 1) if taken else max(0, state2 - 1)

acc1 = 1 - mis1 / len(stream)
acc2 = 1 - mis2 / len(stream)
print(f"1-bit predictor accuracy = {acc1:.3f}")
print(f"2-bit predictor accuracy = {acc2:.3f}")
print("2-bit wins on the loop-heavy part (one mispredict per loop, not two)")

# ---- Experiment 2: roofline ----
peak_flops = 1000.0     # GFLOP/s (flat roof)
bw = 100.0              # GB/s   (sloped roof)
intensity = np.linspace(0.1, 30, 300)
attainable = np.minimum(peak_flops, intensity * bw)
ridge = peak_flops / bw  # ridge-point intensity

# Real kernels: (name, arithmetic intensity in FLOP/byte)
kernels = [("SAXPY", 0.17), ("stencil", 0.5), ("dense matmul", 16.0)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.bar(["1-bit", "2-bit"], [acc1, acc2], color=["#dc2626", "#16a34a"])
ax1.set_ylim(0, 1); ax1.set_ylabel("prediction accuracy")
ax1.set_title("Branch predictor accuracy"); ax1.grid(True, axis="y")

ax2.plot(intensity, attainable, color="#2563eb", lw=2, label="roofline")
ax2.axvline(ridge, ls="--", color="#94a3b8", label=f"ridge = {ridge:.0f}")
for name, ai in kernels:
    perf = min(peak_flops, ai * bw)
    ax2.plot(ai, perf, "o", markersize=9)
    ax2.annotate(name, (ai, perf), textcoords="offset points", xytext=(5, 5))
ax2.set_xlabel("arithmetic intensity (FLOP/byte)")
ax2.set_ylabel("attainable GFLOP/s")
ax2.set_title("Roofline: memory-bound vs compute-bound")
ax2.legend(); ax2.grid(True)
plt.tight_layout(); plt.show()

# Try it yourself:
#   1. Make the random branch a 90/10 bias: 2-bit accuracy jumps.
#   2. Double the bandwidth (bw=200): the ridge point moves left, more kernels
#      become compute-bound.
""",
        ),
    ),
)


COMPARCH_COURSES: tuple[SeedCourse, ...] = (
    _COMPARCH_BASICS,
    _COMPARCH_INTERMEDIATE,
    _COMPARCH_ADVANCED,
)

__all__ = ["COMPARCH_COURSES"]
