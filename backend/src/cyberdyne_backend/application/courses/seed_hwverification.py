"""Academy seed content — the Hardware Design Verification track (SystemVerilog/UVM).

* ``hw-verification-basics``        — why verify, the testbench, directed vs random, functional coverage
* ``hw-verification-intermediate``  — the UVM methodology, components, scoreboards, sequences, coverage, assertions
* ``hw-verification-advanced``      — assertion-based & formal, coverage closure, regression, sign-off

Verifies *digital hardware* (RTL) — distinct from the FPGA/VLSI design tracks.
SystemVerilog and UVM appear as read-only illustrative blocks; runnable ``code``
lessons use Python builtins to simulate the *concepts*: a testbench with a golden
reference model, constrained-random generation (deterministic LCG), a scoreboard,
a functional-coverage model, an assertion/property check, and a coverage-driven
loop. Part of the Electronic Engineering curriculum.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ×) in diagrams and labels.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# hw-verification-basics
# ──────────────────────────────────────────────────────────────────────

_HV_BASICS = SeedCourse(
    slug="hw-verification-basics",
    title="Hardware Verification — Basics",
    description=(
        "Prove a digital design is correct before silicon: the verification gap "
        "and why it dominates chip projects, the testbench (stimulus, DUT, "
        "checker, reference model), directed vs constrained-random testing, and "
        "functional coverage. With runnable testbench and constrained-random labs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why verification?",
            "10 min",
            r"""# Why verification?

Designing a chip (writing the RTL) is only half the job — arguably the smaller
half. **Functional verification** is the discipline of **proving the design does
what it should** (and *nothing* it shouldn't) **before** it's committed to silicon.
On modern ASIC/SoC projects, verification consumes **60–70%+ of the total effort**
and headcount — it is its own major engineering role, distinct from design.

**Why so much effort? The cost of a bug.**

- A bug found in **simulation** costs minutes to fix.
- A bug found in **FPGA prototype** costs hours/days.
- A bug found **after tape-out**, in fabricated silicon, costs a **respin**:
  **months of delay and millions of dollars** in mask and fab costs — and possibly
  a recall if it ships. (Intel's 1994 FDIV bug cost ~$475M.)

There's no "patch" for a hardware bug in a shipped chip the way there is for
software. So the economic imperative is overwhelming: **find every bug before
silicon.**

**The verification gap.** Design productivity and chip complexity have grown
exponentially (billions of transistors), but verification complexity grows even
**faster** — the number of possible states and interactions explodes
combinatorially. You **cannot** exhaustively test a real design (a 64-bit adder
alone has 2¹²⁸ input combinations). This gap is why verification needs **methodology
and automation**, not ad-hoc testing.

**Design vs verification — separate, adversarial roles:**

- The **designer** writes RTL to implement the spec.
- The **verification engineer** writes an independent environment to **break** it,
  ideally interpreting the **spec** independently (so both don't make the same
  mistake). This independence is a feature — like having a separate test team.

**What verification must establish:**

- **Functional correctness** — matches the specification across all scenarios.
- **Corner cases & error handling** — overflow, resets, illegal inputs, back-to-back
  transactions, full/empty conditions.
- **Completeness** — you've actually *exercised* the design enough to trust it
  (measured by **coverage**, later).

The mindset shift this track teaches: verification is not "run a few tests and see
if it works" — it's a **systematic, measurable campaign** to expose every bug, built
on reusable methodology (UVM), randomization, checking, and coverage. The rest of
the track builds that campaign, starting with the **testbench**.
""",
        ),
        _t(
            "The testbench",
            "11 min",
            r"""# The testbench

A **testbench** is the verification environment that surrounds the **DUT** (Design
Under Test — the RTL you're verifying) to **stimulate** it and **check** its
responses. The DUT itself has no idea it's being tested; the testbench drives its
inputs and observes its outputs, all in simulation.

Every testbench, from trivial to UVM-scale, has the same **core jobs**:

```
            ┌──────────── Testbench ────────────┐
 stimulus → │  Driver → [ DUT (RTL) ] → Monitor │ → Checker → pass/fail
            │                ▲                   │     ▲
            │          reference model ──────────┘─────┘
            └────────────── Coverage ────────────────┘
```

- **Generate stimulus** — produce input sequences to exercise the DUT (directed or
  random — next lessons).
- **Drive** the stimulus onto the DUT's input pins, respecting its protocol/timing.
- **Monitor** the DUT's outputs (and inputs), capturing what actually happened.
- **Check** correctness — compare actual outputs against **expected** results. This
  is the heart of verification: **a test that doesn't check is worthless** (it can't
  fail).
- **Measure coverage** — track how much of the design's behaviour you've exercised.

**The reference model (a.k.a. golden model / predictor)** is what makes checking
**self-checking and scalable**: an **independent** implementation of the spec (often
in a high-level language or a behavioural model) that computes what the output
*should* be for each input. The checker compares **DUT output vs reference output**
automatically — so you can run **millions** of random tests without a human eyeballing
waveforms.

**Self-checking is non-negotiable.** Early/naïve testbenches just dump waveforms for
a human to inspect — utterly unscalable and error-prone. A real testbench **decides
pass/fail itself** (reference model + automatic comparison + assertions), so a
regression of thousands of tests reports a clean "PASS" or points at the exact
failing case.

**Verifying at the right level:** **unit/block** testbenches verify one module
thoroughly; **subsystem** and **chip/SoC** testbenches verify integration and
interactions. Bugs are cheapest to find at the **block level**, so thorough block
verification comes first.

The takeaway: a testbench **stimulates, drives, monitors, checks (against a
reference), and covers** — and the **self-checking** reference-model architecture is
what lets verification scale to the millions of tests modern designs demand. You'll
build a minimal self-checking testbench next.
""",
        ),
        _code(
            "A self-checking testbench",
            "12 min",
            r"""# A testbench drives stimulus into the DUT and CHECKS each output against an
# independent reference model (golden model) -> self-checking, no human needed.
# Here the 'DUT' is a 4-bit ALU; the reference computes the expected result.
# Pure builtins.

# --- DUT under test (imagine this is the RTL; one operation has a BUG) ---
def dut_alu(op, a, b):
    if op == "ADD":
        return (a + b) & 0xF
    if op == "SUB":
        return (a - b) & 0xF
    if op == "AND":
        return a & b
    if op == "OR":
        return (a | b) - 1        # <-- injected BUG (should be a | b)
    return 0

# --- Independent reference model (the spec, implemented separately) ---
def reference_alu(op, a, b):
    if op == "ADD":
        return (a + b) % 16
    if op == "SUB":
        return (a - b) % 16
    if op == "AND":
        return a & b
    if op == "OR":
        return a | b
    return 0

vectors = [("ADD", 3, 4), ("SUB", 2, 5), ("AND", 12, 10), ("OR", 8, 1), ("OR", 4, 2), ("ADD", 15, 1)]
fails = 0
print(" op    a   b   DUT   ref   result")
for op, a, b in vectors:
    got = dut_alu(op, a, b)
    exp = reference_alu(op, a, b)
    ok = got == exp
    if not ok:
        fails = fails + 1
    print(" %-4s  %2d  %2d   %2d    %2d    %s" % (op, a, b, got, exp, "PASS" if ok else "*** FAIL ***"))

print()
print("result:", "ALL PASS" if fails == 0 else ("%d FAILURE(S) -> the OR op is broken" % fails))
print("the checker found the bug automatically by comparing DUT vs reference.")
""",
        ),
        _t(
            "SystemVerilog for verification",
            "10 min",
            r"""# SystemVerilog for verification

**SystemVerilog (SV)** is the dominant language for both designing and verifying
digital hardware. For **design** it's a superset of Verilog (RTL); for
**verification** it adds powerful, software-like features — it's effectively an
object-oriented programming language aimed at building testbenches. (These are
read-only illustrations; the runnable labs use Python to model the same ideas.)

**Verification-oriented features SV adds beyond RTL Verilog:**

- **Rich data types** — `logic` (4-state: 0,1,X,Z), `bit` (2-state), dynamic
  arrays, **queues**, **associative arrays**, `struct`, `enum` — for modeling
  transactions and scoreboards.
- **Classes & OOP** — `class`, inheritance, polymorphism — to build reusable,
  layered testbench components (the basis of UVM).
- **Constrained randomization** — `rand`/`randc` variables with `constraint`
  blocks, solved by the simulator (next lessons) — the core of modern stimulus.
- **Interfaces** — bundle related signals (and their timing/`clocking` blocks) into
  one connectable unit, cleaning up DUT↔testbench wiring.
- **Assertions (SVA)** — declarative temporal properties (advanced course).
- **Functional coverage** — `covergroup`/`coverpoint`/`cross` to measure what you've
  tested.
- **`program` blocks / fork-join** — manage concurrency and the race between
  testbench and DUT.

A flavour of SV verification code (read-only):

```systemverilog
// A transaction class with constrained-random fields
class alu_txn;
  rand bit [3:0] a, b;
  rand enum {ADD, SUB, AND_, OR_} op;
  constraint c_legal { a < b; }      // solver honours this
endclass

// A simple interface bundling the DUT pins
interface alu_if(input bit clk);
  logic [3:0] a, b, result;
  logic [1:0] op;
endinterface
```

**Why a specialised language?** Hardware verification has needs general languages
lack: **4-state logic** (X/Z for unknowns and tri-states), **time and concurrency**
as first-class (everything happens on clock edges, in parallel), **constrained
randomization** built into the language, and **native coverage/assertions**. SV
unifies design and verification in one ecosystem.

**The bridge to other languages:** SV connects to C/C++ models via **DPI** (Direct
Programming Interface) — often the reference model is written in C/C++ and called
from the SV testbench. And UVM (next course) is a **class library** written *in*
SystemVerilog.

You don't need to be an SV expert to grasp this track — the **concepts** (classes
as reusable components, constrained-random, coverage, assertions) are what matter,
and you'll exercise each in Python. But knowing that SV provides **OOP + randomization
+ concurrency + coverage + assertions** explains *why* it (and UVM on top) is the
industry standard for taping out correct chips.
""",
        ),
        _t(
            "Directed vs constrained-random testing",
            "11 min",
            r"""# Directed vs constrained-random testing

How do you generate the stimulus that exercises the DUT? Two philosophies — and the
shift between them defines modern verification.

**Directed testing** — you **hand-write** specific test cases for specific
scenarios: "add 3+4, check 7"; "reset mid-transaction, check recovery".

- **Pros:** precise, readable, great for targeting **known** corner cases and for
  early bring-up.
- **Cons:** **doesn't scale**. You can only write tests for bugs you **think of**,
  and complex designs have astronomically many scenarios. You'll never hand-write
  enough directed tests to cover a real chip — and the bugs that bite are the ones
  **nobody thought to test**.

**Constrained-random testing (CRV)** — you let the tool **generate random**
stimulus, but **constrained** to be **legal** (valid opcodes, in-range addresses,
protocol-correct ordering). The simulator's constraint solver picks random values
satisfying your `constraint` blocks.

- **Pros:** explores a **vast** space automatically and hits **unexpected**
  combinations and corner cases a human would never enumerate — finding the bugs you
  didn't anticipate. Run it for millions of cycles across a regression farm.
- **Cons:** you need **self-checking** (a reference model — you can't predict random
  outputs by hand) and **functional coverage** to know **what** the randomness
  actually hit (next lesson). Pure randomness may also need **steering** toward rare
  scenarios.

The constraints are the craft: too **loose** and you generate illegal stimulus that
falsely fails (or wastes cycles); too **tight** and you re-create directed testing,
missing the surprising cases. Good constraints define the **legal but wide** space.

```
Directed:    you choose the inputs   -> finds bugs you expect
Constrained- the tool chooses, you   -> finds bugs you DON'T expect
random:      bound it to be legal
```

**The modern practice — coverage-driven, mostly random:** start with constrained-
random to blanket the space and surface surprises, **measure coverage** to see
what's been hit, then add **directed tests** (or tighten constraints toward
"interesting" regions) to fill the remaining **coverage holes**. Randomization does
the heavy lifting; directed tests mop up the corners random rarely reaches.

This is the central engine of contemporary verification: **constrained-random
stimulus + self-checking + functional coverage**, iterated until coverage closes.
You'll generate constrained-random stimulus next.
""",
        ),
        _code(
            "Constrained-random stimulus",
            "13 min",
            r"""# Constrained-random verification generates RANDOM but LEGAL stimulus. The
# simulator has a constraint solver; here we emulate randomness with a determin-
# istic LCG (the sandbox has no random module) and reject values that violate the
# constraints. Pure builtins.

def lcg(state):
    # Linear congruential generator: deterministic pseudo-randomness.
    return (1103515245 * state + 12345) & 0x7FFFFFFF

ops = ["ADD", "SUB", "AND", "OR"]
state = 42

# Constraints: opcode is legal, operands 0..15, and a < b (a 'legal' transaction).
generated = []
attempts = 0
while len(generated) < 10:
    attempts = attempts + 1
    state = lcg(state)
    op = ops[state % 4]
    state = lcg(state)
    a = state % 16
    state = lcg(state)
    b = state % 16
    if a < b:                       # constraint check (solver would guarantee this)
        generated.append((op, a, b))

print("constrained-random transactions (op, a, b) with a < b:")
for g in generated:
    print("  ", g)
print()
print("generated %d legal transactions in %d attempts (%d rejected by the a<b constraint)"
      % (len(generated), attempts, attempts - len(generated)))

# Notice the spread of opcodes/values explores combinations no one hand-picked.
op_counts = {}
for op in ops:
    op_counts[op] = 0
for g in generated:
    op_counts[g[0]] = op_counts[g[0]] + 1
print("opcode spread:", op_counts, "-> random exploration across the legal space")
""",
        ),
        quiz_lesson(
            "Quiz: Verification Foundations",
            (
                q(
                    "Why does functional verification consume the majority of chip-project effort?",
                    (
                        opt(
                            "A post-silicon bug means a costly respin (months, millions); you must find every bug before tape-out, and the state space is enormous",
                            correct=True,
                        ),
                        opt("Because writing RTL is impossible"),
                        opt("Because verification is optional"),
                        opt("Because chips are simple"),
                    ),
                    "There's no patch for shipped silicon; the verification gap (complexity grows faster than testability) forces huge, methodical effort.",
                ),
                q(
                    "What makes a testbench 'self-checking'?",
                    (
                        opt(
                            "It compares DUT outputs against an independent reference model automatically and decides pass/fail without a human",
                            correct=True,
                        ),
                        opt("It only dumps waveforms for a person to inspect"),
                        opt("It never checks outputs"),
                        opt("It requires manual review of every test"),
                    ),
                    "A reference/golden model predicts expected outputs; automatic comparison lets millions of tests run and report pass/fail — eyeballing waveforms doesn't scale.",
                ),
                q(
                    "What is the key advantage of constrained-random testing over directed testing?",
                    (
                        opt(
                            "It explores a vast legal stimulus space automatically, finding corner cases nobody thought to test",
                            correct=True,
                        ),
                        opt("It needs no checking"),
                        opt("It tests fewer cases"),
                        opt("It only tests what you explicitly wrote"),
                    ),
                    "Directed tests only cover bugs you anticipate; constrained-random hits unexpected combinations — but needs self-checking and coverage to be useful.",
                ),
                q(
                    "Why must constrained-random stimulus be 'constrained'?",
                    (
                        opt(
                            "So generated stimulus stays legal/valid (e.g. valid opcodes, in-range, protocol-correct) — too loose causes false fails, too tight re-creates directed testing",
                            correct=True,
                        ),
                        opt("To make it slower"),
                        opt("Constraints are not needed"),
                        opt("To always produce the same value"),
                    ),
                    "Constraints define the legal-but-wide space; the craft is being broad enough to surprise yet legal enough not to generate invalid stimulus.",
                ),
                q(
                    "Why is SystemVerilog used for verification rather than a general-purpose language alone?",
                    (
                        opt(
                            "It natively provides 4-state logic, time/concurrency, constrained randomization, coverage, and assertions — plus OOP for reusable testbenches",
                            correct=True,
                        ),
                        opt("It is the only language that exists"),
                        opt("It cannot describe hardware"),
                        opt("It has no randomization"),
                    ),
                    "HW verification needs X/Z logic, clock-edge concurrency, built-in constrained-random + coverage + assertions; SV unifies design and verification (and UVM is built on it).",
                ),
                q(
                    "In the modern coverage-driven flow, how are directed tests typically used?",
                    (
                        opt(
                            "To fill the remaining coverage holes that constrained-random rarely reaches, after random does the bulk of the work",
                            correct=True,
                        ),
                        opt("As the only form of testing"),
                        opt("They are never used"),
                        opt("To replace the reference model"),
                    ),
                    "Random blankets the space and surfaces surprises; coverage reveals holes; directed tests (or tightened constraints) then target those specific gaps.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# hw-verification-intermediate
# ──────────────────────────────────────────────────────────────────────

_HV_INTERMEDIATE = SeedCourse(
    slug="hw-verification-intermediate",
    title="Hardware Verification — Intermediate",
    description=(
        "The industry-standard methodology: UVM and why it exists, its components "
        "(driver, monitor, sequencer, agent, scoreboard, env), sequences and "
        "stimulus, functional coverage modeling, and SystemVerilog assertions. "
        "With runnable scoreboard and functional-coverage labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The UVM methodology",
            "11 min",
            r"""# The UVM methodology

If everyone builds testbenches from scratch, every project reinvents drivers,
monitors, randomization, and reporting — incompatibly. The **UVM (Universal
Verification Methodology)** is a standardized **class library and methodology** (an
Accellera/IEEE standard, written in SystemVerilog) that gives the whole industry a
**common architecture** for building **reusable, scalable** verification
environments. It is *the* dominant methodology for ASIC/SoC verification.

**What UVM provides:**

- **A standard component architecture** — base classes (`uvm_component`,
  `uvm_object`) and a set of roles (driver, monitor, sequencer, agent, scoreboard,
  env — next lesson) so every testbench has the **same recognizable structure**.
  An engineer can move between projects and instantly understand the environment.
- **Reusability** — components are written to be **configurable** and **reused**
  across block → subsystem → chip levels and across projects. A verified UVM agent
  for a bus (AXI, etc.) is reused everywhere that bus appears (this is huge — most
  VIP, Verification IP, is UVM).
- **Separation of concerns** — **stimulus generation** (sequences) is cleanly
  separated from the **driving mechanism**, so you can change *what* you send
  without touching *how* it's sent.
- **A phasing system** — standard simulation **phases** (`build`, `connect`,
  `run`, `report`…) so components construct, connect, and execute in a
  coordinated order.
- **Configuration & factory** — the **config database** passes settings down the
  hierarchy without hard-wiring; the **factory** lets you **override** any component/
  transaction type (e.g. swap in an error-injecting driver) **without editing** the
  existing code — key for reuse and targeted testing.
- **Standard reporting & messaging** — uniform `uvm_info`/`uvm_error` with verbosity
  control.

**The conceptual model:** transactions (high-level `uvm_sequence_item` objects, e.g.
"an AXI write") flow from **sequences** → **sequencer** → **driver** (which converts
them to pin wiggles on the DUT), while a **monitor** observes the pins and
reconstructs transactions for the **scoreboard** and **coverage**. You think and
randomize at the **transaction level**, not the bit level.

```
Sequence (what to send) → Sequencer → Driver → DUT pins
                                                  │
                            Scoreboard ← Monitor ←┘   (+ Coverage)
```

**Why learn it even if you won't write SV today?** UVM encodes **hard-won best
practices** for verification at scale: transaction-level modeling, layered
reusable components, factory-based configurability, and a clean stimulus/driver
split. The *patterns* — not the syntax — are the value, and they reappear in any
serious verification environment. The next lesson breaks down the components; the
labs model a scoreboard and coverage in Python.
""",
        ),
        _t(
            "UVM components",
            "11 min",
            r"""# UVM components

A UVM testbench is assembled from standard **components**, each with one job. Knowing
the roles — and how transactions flow between them — is the core of reading or
building any UVM environment.

```
┌──────────────────── env ─────────────────────────┐
│   ┌──────────── agent ────────────┐               │
│   │  Sequencer → Driver ─────────────→ DUT pins   │
│   │                  Monitor ←──────────┘          │
│   └───────────────────│──────────┘                │
│                       ▼                            │
│              Scoreboard      Coverage              │
└────────────────────────────────────────────────────┘
   ▲ Sequences run on the sequencer (the stimulus)
```

The roles:

- **Sequence item / transaction** — a high-level, often **randomized** object
  representing one operation (a bus read, a packet). The unit you think in.
- **Sequence** — generates a **stream of transactions** (the *what* — the test
  scenario). Sequences are where stimulus is created and randomized; they're
  **reusable and composable** (sequences can call sub-sequences).
- **Sequencer** — arbitrates and routes transactions from sequences to the driver.
- **Driver** — converts each transaction into **actual pin-level activity** on the
  DUT interface, respecting protocol/timing (the *how*). The sequence/driver split
  means stimulus is independent of the signaling.
- **Monitor** — **passively observes** the DUT pins and reconstructs transactions
  (it drives nothing). Feeds the scoreboard and coverage. (Often DUT input and
  output have monitors.)
- **Agent** — a reusable bundle of **sequencer + driver + monitor** for one
  interface/protocol. Can be **active** (drives) or **passive** (monitors only).
  This is the reuse unit — an "AXI agent," a "UART agent."
- **Scoreboard** — the **checker**: receives observed transactions and compares them
  against the **reference model**'s expected results (the lab builds one).
- **Coverage collector** — samples transactions to measure **functional coverage**.
- **Environment (env)** — the top container holding the agents, scoreboard, and
  coverage; envs nest (block env → subsystem env) for hierarchical reuse.
- **Test** — the top-level object that configures the env and **starts sequences**;
  a regression is a **set of tests** (different sequences/seeds/configs).

**The flow in one sentence:** a **test** starts **sequences** that produce
**transactions**, the **sequencer/driver** apply them to the DUT, the **monitor**
observes results, and the **scoreboard** + **coverage** check correctness and
measure completeness — all inside a reusable **env**.

The genius of this structure is **transaction-level thinking + reuse**: you write
randomized scenarios as sequences (portable), wrap each protocol in an agent
(reused across projects), and keep checking (scoreboard) and measurement (coverage)
separate and reusable. It's the same separation-of-concerns and composition that
good software architecture preaches — applied to proving hardware correct.
""",
        ),
        _code(
            "A scoreboard / checker",
            "12 min",
            r"""# A SCOREBOARD checks the DUT: it holds expected results (from the reference
# model) and compares them, in order, against the transactions the monitor
# observed -- reporting matches and the exact mismatches. Pure builtins.

# The monitor observed these DUT output transactions (id, value):
observed = [(0, 6), (1, 14), (2, 0), (3, 12), (4, 0)]

# The reference model predicts the expected value for each id (e.g. double & 4-bit):
inputs = [3, 7, 0, 15, 8]
expected = []
for idx in range(len(inputs)):
    expected.append((idx, (inputs[idx] * 2) & 0xF))

# Scoreboard compare: match observed against expected by id.
exp_map = {}
for tid, val in expected:
    exp_map[tid] = val

matches = 0
mismatches = []
for tid, got in observed:
    want = exp_map.get(tid, None)
    if want is not None and got == want:
        matches = matches + 1
    else:
        mismatches.append((tid, got, want))

print("scoreboard report:")
print("  transactions checked:", len(observed))
print("  matches:", matches)
for tid, got, want in mismatches:
    print("  MISMATCH id=%d: DUT=%d expected=%d" % (tid, got, want))
print()
print("verdict:", "PASS" if not mismatches else "FAIL (%d mismatch) -> id 3: 15*2&0xF should be 14, DUT gave 12" % len(mismatches))
""",
        ),
        _t(
            "Sequences & stimulus generation",
            "10 min",
            r"""# Sequences & stimulus generation

In UVM, **sequences** are where stimulus lives — the **scenarios** you run against
the DUT. The big idea is **transaction-level, reusable, layered** stimulus,
decoupled from how signals are driven.

**The hierarchy:**

- **Sequence item (transaction)** — one operation: a randomizable object with
  fields and **constraints** (a bus write with `addr`, `data`, `size`). You
  randomize at this level.
- **Sequence** — a **procedure** that creates and sends a **series** of items,
  possibly with logic between them ("write then read back and expect a match",
  "send N random packets", "do a reset then a burst"). Sequences **randomize** the
  items they send and can be **constrained** or **directed**.
- **Virtual sequence** — coordinates **multiple** sequences across **multiple
  agents/interfaces** to create **system-level scenarios** (e.g. drive the bus and
  the interrupt line and the config port in a coordinated pattern). The conductor of
  a multi-interface test.

**Why sequences are powerful:**

- **Layering / composition** — small sequences combine into bigger ones; a library
  of reusable sequences (reset, random-traffic, error-injection, corner-case) is
  built up and **reused** across tests and projects.
- **Separation from the driver** — a sequence says *what* transactions to send; the
  **driver** decides *how* to wiggle pins. Change the protocol timing without
  touching the scenarios; reuse scenarios on a different driver.
- **Randomization with control** — a sequence can send fully random items, or
  **steer** them (override constraints, set distributions/weights) to push toward
  rare scenarios that pure randomness reaches slowly. **`randomize() with { ... }`**
  applies in-line constraints per call.

A read-only flavour:

```systemverilog
class burst_seq extends uvm_sequence #(bus_txn);
  task body();
    repeat (10) begin
      bus_txn t = bus_txn::type_id::create("t");
      start_item(t);
      assert(t.randomize() with { addr inside {[0:255]}; kind == WRITE; });
      finish_item(t);            // sent to the driver via the sequencer
    end
  endtask
endclass
```

**Stimulus strategy in practice:** combine **broad random** sequences (blanket the
space), **constrained/steered** sequences (target interesting regions and rare
corners), and **directed** sequences (specific known cases and coverage-hole
fillers). The reusable sequence **library** becomes a project asset — and the engine
that, together with coverage, drives the verification campaign to closure.

The principle to carry: **think in transactions and scenarios, not pins**, build
**reusable, composable** sequences, and **separate stimulus from driving** — so your
verification scales and ports, exactly as UVM intends.
""",
        ),
        _t(
            "Functional coverage",
            "11 min",
            r"""# Functional coverage

Constrained-random testing creates a crucial question: **"are we done yet?"** You've
run ten million random cycles — but did they actually exercise the **features and
corner cases** that matter, or just hammer the easy paths? **Functional coverage**
answers this: it **measures what you've verified** against a plan, turning "we ran a
lot of tests" into "we exercised these specific behaviours."

**Two kinds of coverage, often confused:**

- **Code coverage** — *automatic*, measures which **RTL lines/branches/toggles/FSM
  states** the tests executed. Necessary but **not sufficient**: 100% code coverage
  just means every line ran, **not** that every *interesting scenario* was tested
  (you can execute a line with only boring inputs).
- **Functional coverage** — *you define it*, measures whether **specific functional
  scenarios** happened: every opcode, every burst length, FIFO full **and** empty,
  every error type, key **combinations**. This captures **intent** from the spec —
  it's the real "are we done" metric.

**How functional coverage is modeled (SystemVerilog `covergroup`):**

- **Coverpoint** — a variable/event to track, divided into **bins** (value ranges or
  specific values). E.g. `opcode` with a bin per opcode; `length` binned into
  small/medium/large.
- **Cross coverage** — the **combination** of coverpoints: not just "every opcode
  was used" and "every length was used," but "**every opcode at every length**" —
  catching interaction bugs. Crosses are where the real corner cases hide.
- **Coverage %** — bins hit ÷ total bins. **Coverage holes** are bins never hit —
  the precise list of what you still need to test.

```systemverilog
covergroup alu_cg;
  cp_op:  coverpoint txn.op;                 // bins: ADD, SUB, AND, OR
  cp_amt: coverpoint amount { bins z={0}; bins sm={[1:7]}; bins lg={[8:15]}; }
  cross cp_op, cp_amt;                        // every op x every magnitude
endgroup
```

**The coverage-driven loop** (the engine of modern verification):

```
run constrained-random  →  measure functional coverage  →  find holes
   →  add directed tests / steer constraints to hit them  →  repeat until closed
```

This is **coverage-driven verification (CDV)**: randomness does the bulk, coverage
tells you what's missing, and you target the gaps — until coverage **closes** at the
goal (often near 100% of the planned bins). Coverage is also the basis of the
**verification plan (vplan)** — the agreed list of features/scenarios that *must* be
covered for sign-off.

The mental model: **functional coverage is your map of "tested vs untested"** in the
space of *intended behaviour*. Without it, constrained-random is firing blind; with
it, you have a **measurable, plannable** path to "done." You'll build a coverage
model with a cross next.
""",
        ),
        _code(
            "Functional coverage model",
            "13 min",
            r"""# Functional coverage measures WHICH scenarios were exercised. We define bins
# for opcode and operand-magnitude, plus their CROSS (every op x every magnitude),
# run stimulus, and report coverage % and the holes. Pure builtins.

opcodes = ["ADD", "SUB", "AND", "OR"]
magnitudes = ["zero", "small", "large"]

# Build the cross-coverage bins (opcode x magnitude) and zero the hit counts.
cov = {}
for op in opcodes:
    for mag in magnitudes:
        cov[(op, mag)] = 0

def magnitude_of(value):
    if value == 0:
        return "zero"
    if value < 8:
        return "small"
    return "large"

# Some stimulus (op, operand) -- note it never exercises certain combinations.
stimulus = [
    ("ADD", 0), ("ADD", 5), ("ADD", 12), ("SUB", 9), ("SUB", 0),
    ("AND", 3), ("OR", 14), ("OR", 6), ("ADD", 15), ("SUB", 4),
]
for op, val in stimulus:
    key = (op, magnitude_of(val))
    cov[key] = cov[key] + 1

# Coverage = bins hit / total bins.
total = 0
hit = 0
holes = []
for key in cov:
    total = total + 1
    if cov[key] > 0:
        hit = hit + 1
    else:
        holes.append(key)

print("functional coverage (opcode x magnitude cross):")
print("  bins hit: %d of %d  ->  %.0f%% coverage" % (hit, total, 100.0 * hit / total))
print("  coverage HOLES (scenarios never exercised):")
for key in holes:
    print("    ", key)
print()
print("the holes tell you EXACTLY what stimulus to add (directed tests or steering)")
print("to reach closure -- e.g. an AND with a 'large' operand was never tested.")
""",
        ),
        quiz_lesson(
            "Quiz: UVM, Scoreboards & Coverage",
            (
                q(
                    "What is the main purpose of UVM?",
                    (
                        opt(
                            "A standard class library/methodology for building reusable, scalable verification environments with a common architecture",
                            correct=True,
                        ),
                        opt("A language for designing RTL"),
                        opt("A chip-fabrication process"),
                        opt("A way to skip verification"),
                    ),
                    "UVM standardizes testbench architecture (driver/monitor/sequencer/agent/scoreboard/env), reuse, phasing, config/factory, and reporting.",
                ),
                q(
                    "In UVM, what is the role of the driver vs the sequence?",
                    (
                        opt(
                            "The sequence decides WHAT transactions to send; the driver converts each transaction into pin-level activity (HOW)",
                            correct=True,
                        ),
                        opt("They are the same component"),
                        opt("The driver generates random stimulus; the sequence wiggles pins"),
                        opt("Neither touches the DUT"),
                    ),
                    "Separating stimulus (sequences) from signaling (driver) lets you reuse scenarios across protocols and change timing without touching tests.",
                ),
                q(
                    "What does a scoreboard do?",
                    (
                        opt(
                            "Compares the DUT's observed transactions against the reference model's expected results and flags mismatches",
                            correct=True,
                        ),
                        opt("Generates the clock"),
                        opt("Drives stimulus onto the DUT"),
                        opt("Measures power consumption"),
                    ),
                    "The scoreboard is the checker: it predicts (via the reference model) and compares, automatically detecting incorrect DUT behaviour.",
                ),
                q(
                    "Why is functional coverage necessary even with 100% code coverage?",
                    (
                        opt(
                            "Code coverage only shows every line ran; functional coverage shows whether the intended scenarios/combinations were actually exercised",
                            correct=True,
                        ),
                        opt("They are identical"),
                        opt("Code coverage is always enough"),
                        opt("Functional coverage measures speed"),
                    ),
                    "You can execute every line with boring inputs; functional coverage (coverpoints + crosses) captures spec intent — the real 'are we done' metric.",
                ),
                q(
                    "What does cross coverage add over individual coverpoints?",
                    (
                        opt(
                            "It checks combinations (e.g. every opcode at every magnitude), catching interaction bugs single coverpoints miss",
                            correct=True,
                        ),
                        opt("Nothing — it's the same"),
                        opt("It measures code lines"),
                        opt("It reduces the number of bins to track"),
                    ),
                    "Hitting every opcode and every length separately isn't the same as hitting every opcode×length combination, where corner-case interactions hide.",
                ),
                q(
                    "What is the coverage-driven verification loop?",
                    (
                        opt(
                            "Run constrained-random → measure coverage → find holes → add directed tests/steer constraints → repeat until coverage closes",
                            correct=True,
                        ),
                        opt("Write one test and ship"),
                        opt("Only run directed tests"),
                        opt("Disable coverage and randomize forever"),
                    ),
                    "CDV uses randomness for bulk exploration, coverage to reveal gaps, and targeted stimulus to close them — a measurable path to sign-off.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# hw-verification-advanced
# ──────────────────────────────────────────────────────────────────────

_HV_ADVANCED = SeedCourse(
    slug="hw-verification-advanced",
    title="Hardware Verification — Advanced",
    description=(
        "Closing the loop and proving correctness: assertion-based verification "
        "and formal methods, coverage closure and coverage-driven verification at "
        "scale, regression/CI, emulation and gate-level/low-power/DFT, and "
        "verification planning & sign-off. With runnable assertion-check and "
        "coverage-closure labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Assertion-based verification & formal",
            "11 min",
            r"""# Assertion-based verification & formal

**Assertions** are executable statements of **what must always (or never) be true**
about a design — embedded in the RTL or testbench and checked **continuously**.
**Assertion-Based Verification (ABV)** uses them to catch bugs **at their source**,
the instant a rule is violated, instead of only seeing a wrong output much later.

**SystemVerilog Assertions (SVA)** come in two forms:

- **Immediate assertions** — checked like a procedural `if` at a point in time.
- **Concurrent assertions** — **temporal** properties checked over **clock cycles**,
  the powerful kind. They express sequences across time:

```systemverilog
// "Every req must be granted within 1 to 3 cycles" (a temporal property)
property p_req_grant;
  @(posedge clk) req |-> ##[1:3] grant;
endproperty
assert property (p_req_grant) else $error("req not granted in time");
```

`|->` is "implies," `##[1:3]` is "1 to 3 cycles later." Assertions encode protocol
rules, handshakes, FIFO never-overflow, one-hot states, "X never propagates," etc.

**Why assertions are so valuable:**

- **Catch bugs at the source** — fire the moment the rule breaks, pinpointing the
  cause (not 10,000 cycles downstream at the output).
- **Document intent** — an assertion *is* a precise, checkable statement of the
  spec/protocol.
- **Double as coverage** — **cover properties** measure whether interesting
  **sequences** actually occurred.
- **Reusable** — protocol **assertion IP** (e.g. for AXI) checks correctness
  wherever the protocol appears.

**Formal verification** takes assertions further: instead of *simulating* stimulus,
a **formal tool mathematically PROVES** (via model checking) that a property holds
for **all possible** inputs and states — or produces a **counterexample** (a
specific trace that violates it). This is **exhaustive** within its scope — no test
vectors, no coverage holes, complete proof — which simulation can never achieve.

- **Strengths:** exhaustive proof of properties; finds the corner case no random
  test would hit; great for control logic, arbiters, protocols, FIFOs, and proving
  the **absence** of a bug.
- **Limits:** **state-space explosion** (can't formally prove huge datapaths
  directly), needs skilled property writing, and proving "no bug" requires the right
  properties (and **constraints/assumptions** on inputs, or you get false
  counterexamples).

**The modern combination:** **dynamic** simulation (constrained-random + coverage,
the previous course) for broad system behaviour, **plus** assertions everywhere to
localize bugs, **plus** **formal** on the tricky control blocks where exhaustive
proof is feasible and most valuable. Each covers the others' weak spots.

The advanced mindset: don't just *observe* outputs — **assert the rules** the design
must obey (catching bugs at the source and documenting intent), and where the block
is amenable, **prove** correctness formally rather than sampling it. You'll check a
temporal property over a trace next.
""",
        ),
        _code(
            "Assertion / property check",
            "12 min",
            r"""# A concurrent assertion checks a TEMPORAL property over clock cycles. Here:
# 'every req must be followed by ack within 2 cycles' (req |-> ##[1:2] ack).
# We check the property over a signal trace and report violations. Pure builtins.

# Trace of (req, ack) sampled each clock cycle.
trace = [
    (1, 0),   # 0: req asserted
    (0, 1),   # 1: ack -> satisfies the req at cycle 0
    (0, 0),   # 2
    (1, 0),   # 3: req asserted
    (0, 0),   # 4: no ack
    (0, 0),   # 5: still no ack -> VIOLATION for req at cycle 3
    (1, 0),   # 6: req asserted
    (0, 1),   # 7: ack -> satisfies req at cycle 6
]

window = 2     # ack must arrive within 1..2 cycles after req
violations = []
req_cycles = []
for i in range(len(trace)):
    req = trace[i][0]
    if req == 1:
        req_cycles.append(i)
        satisfied = False
        for j in range(i + 1, min(i + 1 + window, len(trace))):
            if trace[j][1] == 1:        # ack found in the window
                satisfied = True
                break
        if not satisfied:
            violations.append(i)

print("property: req |-> ##[1:%d] ack" % window)
print("req asserted at cycles:", req_cycles)
if violations:
    for c in violations:
        print("  *** ASSERTION FAILED: req at cycle %d got no ack within %d cycles" % (c, window))
else:
    print("  all requests acknowledged in time")
print()
print("result:", "PASS" if not violations else "FAIL (%d violation)" % len(violations))
print("the assertion fires AT the offending cycle -> bug localized to its source.")
""",
        ),
        _t(
            "Coverage closure & CDV at scale",
            "10 min",
            r"""# Coverage closure & CDV at scale

**Coverage closure** is the endgame of a verification project: driving **functional
(and code) coverage** to its goal — typically **near 100%** of the planned bins —
which is the primary evidence that verification is **complete** enough to sign off.
Getting there is a managed, often months-long process.

**The closure process:**

```
1. Run the regression (many random seeds, many tests) on a compute farm
2. MERGE coverage from all runs into one database
3. Analyze: what % is covered? WHERE are the holes?
4. Classify each hole:
     - reachable & meaningful  -> write directed test / steer constraints
     - reachable but low-value  -> still cover it
     - UNREACHABLE (dead code, illegal by design) -> WAIVE with justification
5. Add stimulus, re-run, re-merge  -> repeat until goal met
```

**Key realities at scale:**

- **Coverage is a curve of diminishing returns.** Random stimulus covers the bulk
  **fast**, then progress **slows** as only rare corner cases remain — the classic
  saturating curve. The **last few percent** is the hardest and needs directed
  effort.
- **Coverage merging** — closure aggregates coverage across **thousands** of
  regression runs (different seeds/configs); no single run covers everything.
- **Waivers** — some bins are **legitimately unreachable** (illegal combinations,
  dead default branches). These are **waived** with documented justification —
  otherwise you'd chase 100% forever. Reviewing waivers is part of sign-off.
- **Coverage ≠ correctness.** A subtle but vital caveat: **coverage measures that a
  scenario was *exercised*, not that it was *checked***. High coverage with weak
  checking (no good scoreboard/assertions) gives false confidence. Coverage and
  checking are **both** required — you must hit the scenario **and** verify the
  result.

**Coverage-Driven Verification (CDV) at scale** is the organizational engine: the
**verification plan (vplan)** lists every feature/scenario to cover (traced to the
spec); coverage is tracked **against the vplan** in dashboards; the team steers
random regressions and adds directed tests to close holes; **closure metrics** drive
the schedule and the sign-off decision.

```plot
{"title": "Coverage closure: random covers fast, the tail is slow", "xLabel": "tests run (thousands)", "yLabel": "functional coverage (%)", "xRange": [0, 200], "yRange": [0, 100], "functions": [{"expr": "100 * x / (x + 25)", "label": "coverage vs effort", "color": "#16a34a"}]}
```

The takeaway: **closure is how verification ends** — drive planned coverage to goal,
analyze and fill (or justifiably waive) every hole, and never confuse "covered" with
"checked." It converts the open-ended question "have we tested enough?" into a
**tracked, defensible metric** for tape-out. You'll run a coverage-closing loop next.
""",
        ),
        _code(
            "Coverage-driven closure loop",
            "13 min",
            r"""# Coverage-driven verification: keep generating constrained-random stimulus
# until functional coverage CLOSES (every bin hit), then stop. Watch how the
# common bins fill fast but the last (rare) bin takes many more tests. Uses an LCG.

def lcg(state):
    return (1103515245 * state + 12345) & 0x7FFFFFFF

# 8 functional bins to cover; bin 7 is RARE (only hit by a narrow value) to show
# the diminishing-returns tail of coverage closure.
num_bins = 8
bins = {}
for b in range(num_bins):
    bins[b] = 0

state = 99
tests = 0
covered = 0
milestones = []
while covered < num_bins and tests < 100000:
    state = lcg(state)
    r = state % 100
    # Map most of the range to bins 0..6, but reserve a tiny slice for the rare bin 7.
    if r < 98:
        target = r % 7              # common bins 0..6
    else:
        target = 7                  # rare bin (only ~2% of the time)
    bins[target] = bins[target] + 1
    tests = tests + 1
    new_covered = 0
    for b in bins:
        if bins[b] > 0:
            new_covered = new_covered + 1
    if new_covered > covered:
        milestones.append((new_covered, tests))
    covered = new_covered

print("coverage milestones (bins covered, tests needed):")
for c, t in milestones:
    print("  %d/%d bins covered after %d tests" % (c, num_bins, t))
print()
print("CLOSED: all %d bins hit after %d random tests" % (num_bins, tests))
print("bin hit counts:", dict(bins))
print("note the tail: the first 7 bins close quickly; the RARE bin 7 dominates the")
print("run -> in practice you'd write a DIRECTED test for it instead of waiting.")
""",
        ),
        _t(
            "Regression, CI & verification at scale",
            "10 min",
            r"""# Regression, CI & verification at scale

A real verification environment isn't run once — it's run **continuously, at
massive scale**, as the design and testbench evolve. **Regression** is the
disciplined, automated re-running of the whole test suite to ensure new changes
**don't break** what worked (and to keep accumulating coverage).

**The regression system:**

- **The test suite** — hundreds to thousands of tests: many **constrained-random**
  tests each run with **many random seeds** (each seed explores a different slice of
  the space), plus **directed** tests for specific scenarios.
- **Seeds & reproducibility** — random tests are seeded; a failing run's **seed**
  (and config) lets you **reproduce the exact failure** deterministically to debug
  it. Reproducibility is sacred in verification.
- **Compute farm / grid** — regressions run across **hundreds or thousands of CPUs**
  (on-prem grid or cloud) overnight or continuously — verification is enormously
  compute-hungry.
- **Coverage merge** — every run contributes coverage to the merged database
  (closure, previous lesson).

**Continuous Integration for hardware:**

- Every RTL or testbench **commit** triggers (at least a smoke) regression — catch
  breakage immediately, exactly like software CI (this very platform's "Quality
  gate," applied to hardware).
- **Triage & dashboards** — automated **pass/fail reporting**, **failure
  bucketing** (group failures by likely root cause), and **trend tracking** (pass
  rate, coverage over time) so a team can manage thousands of results.
- **Bisecting** — when a regression starts failing, find the offending commit
  (same idea as `git bisect`).

**Debugging a failure at scale:**

```
fail in regression → grab the seed/config → reproduce locally (deterministic)
→ dump waveforms / use assertions to localize → fix RTL or testbench → re-run
```

**Performance matters** because of the scale: simulation speed, **smart seed/test
selection** (run the tests most likely to find bugs or add coverage first), and
**ranking** (which seeds add the most coverage) all reduce the compute bill and
time-to-closure. For the biggest designs, **emulation/FPGA prototyping** (next
lesson) runs orders of magnitude faster than simulation for long tests.

The organizational picture: verification at scale is a **continuously-running,
reproducible, dashboarded regression machine** on a compute farm — generating
coverage, catching regressions on every commit, and feeding a triage process that
keeps thousands of results manageable. It's as much **infrastructure and process**
as it is testbench code — and it's why verification teams are large and tooling-
heavy. Reproducible seeds + automated regression + coverage merge + triage is the
backbone that gets a complex chip to a confident tape-out.
""",
        ),
        _t(
            "Emulation, gate-level, low-power & DFT",
            "10 min",
            r"""# Emulation, gate-level, low-power & DFT

Beyond RTL simulation, sign-off requires verifying the design through the **rest of
the flow** — at speed, after synthesis, with power intent, and for testability. A
survey of the advanced verification surfaces:

**Emulation & FPGA prototyping — verification at speed.** RTL simulation is
thorough but **slow** (kHz–MHz effective clock), far too slow to **boot an OS** or
run real software workloads on a big SoC. **Hardware emulators** (specialized
boxes) and **FPGA prototypes** map the design onto reconfigurable hardware running
**thousands to millions of times faster**, enabling:

- **Hardware-software co-verification** — run real firmware/drivers/OS on the
  pre-silicon design (find HW/SW integration bugs before tape-out).
- **Long, realistic workloads** — boot sequences, video frames, network traffic —
  infeasible in simulation.
- Trade-off: emulation has **less visibility/debuggability** than simulation and
  costs a lot — used **alongside** simulation, not instead.

**Gate-level simulation (GLS).** After **synthesis** turns RTL into a **gate
netlist**, you simulate that netlist — often with **timing (SDF back-annotation)** —
to catch what RTL sim can't: **X-propagation** issues, **reset/initialization**
problems, **timing-related** bugs, and synthesis/tool mismatches. Slow, so run
selectively; complemented by **STA** (static timing analysis) for timing sign-off
and **LEC** (logical equivalence checking — formally prove the netlist == RTL).

**Low-power verification (UPF/CPF).** Modern chips aggressively **power-gate** and
**voltage-scale** regions. The **power intent** (which domains shut off, isolation,
retention, level-shifters) is captured in **UPF** and must be **verified**: that
isolation cells prevent X-corruption when a domain is off, retention restores
state, and power sequencing is correct. A functional-only sim **misses** these —
power-aware simulation is its own sign-off.

**Design-for-Test (DFT) & manufacturing test.** Separate from *functional*
verification: ensuring the fabricated chip can be **tested for manufacturing
defects**. **Scan chains** stitch flip-flops into shift registers; **ATPG**
(Automatic Test Pattern Generation) creates patterns to detect stuck-at/transition
faults; **fault coverage** measures the fraction of possible defects detectable;
**BIST** (built-in self-test) tests memories/logic on-chip; **JTAG/boundary scan**
tests board-level connectivity. DFT verification confirms the test logic works and
hits its fault-coverage target.

The big-picture sign-off view: a chip is signed off when it's verified
**functionally** (sim + formal + coverage), **at speed** (emulation/HW-SW), **post-
synthesis** (GLS, STA, LEC), **for power** (UPF), and **for manufacturability**
(DFT/ATPG fault coverage) — each a distinct verification discipline. "Verified"
means correct across **all** these axes, which is why pre-silicon sign-off is such a
broad, multi-tool effort.
""",
        ),
        _t(
            "Verification planning & sign-off",
            "10 min",
            r"""# Verification planning & sign-off

Verification only works if it's **planned and measured** — otherwise "are we done?"
becomes a guess and bugs slip to silicon. **Verification planning** and **sign-off**
are the management spine that ties together everything in this track.

**The verification plan (vplan)** — written **early**, from the **specification**,
**before** (or alongside) the testbench:

- **Enumerate features & scenarios** to verify — every function, mode, corner case,
  error condition, and interface, derived from the spec.
- **Map each to a method** — directed test, constrained-random + coverage,
  assertion, or formal proof — and to **coverage points** that measure it.
- **Define sign-off criteria** — the explicit, agreed bar for "done."
- The vplan is **traceable to the spec** (every requirement has verification) and
  **living** (updated as the design/spec evolve).

**Sign-off criteria — the bar for tape-out** typically includes:

- **Functional coverage** at goal (e.g. 100% of planned bins, with **reviewed
  waivers** for unreachable ones).
- **Code coverage** at goal (e.g. ≥ 95–100% line/branch, waivers justified).
- **All tests passing** in regression; **zero open critical bugs**; bug-discovery
  rate **flattened** (few new bugs found despite heavy testing — a key maturity
  signal).
- **Assertions** in place and passing; key properties **formally proven**.
- **Other axes complete**: gate-level, low-power (UPF), timing (STA), DFT fault
  coverage, HW-SW (emulation) — each to its criterion.

**Metrics & maturity tracking** — dashboards trend **coverage over time**, **pass
rate**, and the **bug-discovery curve** (cumulative bugs found). A flattening bug
curve **plus** closed coverage is the strongest evidence verification is converging;
bugs still pouring in means you're **not** done regardless of the calendar.

**The honest limits to communicate:**

- *"Verification can prove the presence of bugs, but not their absence"* (Dijkstra)
  — except where **formal** proves a specific property. Coverage closure means "we
  exercised and checked the **planned** space," not "the design is provably perfect."
- **The plan is only as good as the spec interpretation** — a missing scenario in
  the vplan is a blind spot no amount of coverage will reveal. Review the plan
  adversarially.

The professional throughline of the whole track: verification is a **planned,
measured engineering campaign**, not ad-hoc testing. You **plan** from the spec
(vplan), **execute** with the right mix of methods (directed, constrained-random +
coverage, assertions, formal, emulation, GLS, low-power, DFT), **measure** progress
(coverage + bug curve + pass rate), and **sign off** against explicit, defensible
criteria. That discipline — making "done" a tracked, evidence-backed decision — is
what stands between a design and a multi-million-dollar respin.
""",
        ),
        quiz_lesson(
            "Quiz: Assertions, Closure & Sign-off",
            (
                q(
                    "What advantage do concurrent (temporal) assertions provide?",
                    (
                        opt(
                            "They check rules across clock cycles and fire AT the offending cycle, localizing bugs to their source",
                            correct=True,
                        ),
                        opt("They make simulation faster"),
                        opt("They replace the need for a clock"),
                        opt("They only work after tape-out"),
                    ),
                    "SVA concurrent assertions express temporal properties (req |-> ##[1:3] grant); they catch violations at the source and document protocol intent.",
                ),
                q(
                    "How does formal verification differ from simulation?",
                    (
                        opt(
                            "It mathematically proves a property holds for ALL inputs/states (or gives a counterexample) — exhaustive within scope, no test vectors",
                            correct=True,
                        ),
                        opt("It just runs more random tests"),
                        opt("It needs no properties"),
                        opt("It can verify any size design easily"),
                    ),
                    "Formal model-checking is exhaustive (proves absence of a violation) but limited by state-space explosion; great for control logic/protocols.",
                ),
                q(
                    "Why must you not confuse coverage with correctness?",
                    (
                        opt(
                            "Coverage shows a scenario was exercised, not that its result was checked — high coverage with weak checking gives false confidence",
                            correct=True,
                        ),
                        opt("Coverage always implies correctness"),
                        opt("Checking is unnecessary"),
                        opt("They mean the same thing"),
                    ),
                    "You need BOTH: hit the scenario (coverage) AND verify the output (scoreboard/assertions). Coverage with no checking proves nothing.",
                ),
                q(
                    "What are coverage waivers?",
                    (
                        opt(
                            "Documented justifications for bins that are legitimately unreachable (illegal/dead), so you don't chase 100% forever",
                            correct=True,
                        ),
                        opt("A way to ignore failing tests"),
                        opt("Tests that always pass"),
                        opt("A type of assertion"),
                    ),
                    "Some bins can't be hit (illegal combos, dead defaults); they're waived with justification and reviewed at sign-off — the rest must be covered.",
                ),
                q(
                    "Why are random-test seeds important in regression?",
                    (
                        opt(
                            "Each seed explores a different slice of the space, and a failing seed reproduces the exact failure deterministically for debugging",
                            correct=True,
                        ),
                        opt("Seeds make tests run slower"),
                        opt("Seeds are irrelevant"),
                        opt("They replace the reference model"),
                    ),
                    "Many seeds widen exploration; reproducibility (re-run the failing seed/config) is essential to debug and fix the exact failure.",
                ),
                q(
                    "Besides coverage at goal, what is a key sign-off maturity signal?",
                    (
                        opt(
                            "A flattened bug-discovery curve — few new bugs found despite heavy testing",
                            correct=True,
                        ),
                        opt("The number of lines of testbench code"),
                        opt("Running exactly one test"),
                        opt("Disabling assertions"),
                    ),
                    "Closed coverage PLUS a flattening cumulative-bug curve (and all tests passing, no critical bugs) is the strongest evidence verification has converged.",
                ),
            ),
        ),
    ),
)


HW_VERIFICATION_COURSES = (_HV_BASICS, _HV_INTERMEDIATE, _HV_ADVANCED)
