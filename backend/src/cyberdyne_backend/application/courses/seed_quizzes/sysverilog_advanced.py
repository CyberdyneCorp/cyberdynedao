"""Quiz spec for the SystemVerilog -- Advanced (Pipelining, Generics & Verification) course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pipelining RTL: stalls and flushes": (
            q(
                "What does asserting 'flush' on a pipeline register do?",
                (
                    opt("Holds the current value"),
                    opt("Injects a zero/NOP bubble into the stage", correct=True),
                    opt("Doubles the clock speed"),
                    opt("Disables the reset"),
                ),
                "Flush squashes the stage by loading a bubble; stall instead holds the "
                "current value.",
            ),
            q(
                "Pipelining a 2-stage MAC primarily improves which metric?",
                (
                    opt("The latency of a single result"),
                    opt("Throughput -- one result per cycle once full", correct=True),
                    opt("Power consumption"),
                    opt("The number of registers needed"),
                ),
                "Pipelining raises throughput (results per cycle); a single result's "
                "latency is unchanged or slightly higher.",
            ),
        ),
        "Parameterization and generate": (
            q(
                "When does a generate-for loop run?",
                (
                    opt("Every clock cycle at runtime"),
                    opt("Once at build/elaboration time, laying out parallel hardware", correct=True),
                    opt("Only in simulation"),
                    opt("When reset is asserted"),
                ),
                "generate elaborates once at build time into concurrent hardware; its "
                "bounds must be constants.",
            ),
            q(
                "What must the condition of a generate-if be?",
                (
                    opt("A runtime signal"),
                    opt("A compile-time constant (parameter/localparam)", correct=True),
                    opt("Always true"),
                    opt("A clock edge"),
                ),
                "generate-if includes or excludes hardware at elaboration, so its "
                "condition must be a constant.",
            ),
        ),
        "Interfaces, packages, and structs": (
            q(
                "What problem does a SystemVerilog 'interface' solve?",
                (
                    opt("It speeds up the clock"),
                    opt("It bundles a bus's signals + protocol into one typed port", correct=True),
                    opt("It replaces always_ff"),
                    opt("It initializes memory"),
                ),
                "An interface groups related signals (and modports for direction) so a "
                "module takes one port instead of many loose wires.",
            ),
            q(
                "Why put XLEN and the opcode enum in a package?",
                (
                    opt("Packages run faster"),
                    opt("Every module that imports it shares one definition, kept in sync", correct=True),
                    opt("It is the only place enums are allowed"),
                    opt("To avoid using parameters"),
                ),
                "A package centralizes shared types/constants; importing it keeps all "
                "modules consistent and avoids drift.",
            ),
        ),
        "Verification: testbenches, assertions, and coverage": (
            q(
                "What does the SVA property 'req |-> ##[1:4] gnt' assert?",
                (
                    opt("req and gnt are always equal"),
                    opt("After req, gnt must arrive 1 to 4 cycles later", correct=True),
                    opt("gnt must precede req"),
                    opt("req happens at most 4 times"),
                ),
                "The implication |-> with ##[1:4] requires gnt within 1 to 4 cycles of "
                "each req; the tool checks it every cycle.",
            ),
            q(
                "What does functional coverage tell you that a passing testbench does not?",
                (
                    opt("Whether the checks passed"),
                    opt("What fraction of the intended behaviour you actually exercised", correct=True),
                    opt("The clock frequency"),
                    opt("The gate count"),
                ),
                "Passing checks only cover the cases you ran; coverage measures how much "
                "of the design space was hit -- needed for signoff.",
            ),
        ),
    },
    final=(
        q(
            "In a stalled pipeline register (stall=1, flush=0), what does q do?",
            (
                opt("Loads d"),
                opt("Keeps its current value", correct=True),
                opt("Goes to zero"),
                opt("Becomes unknown"),
            ),
            "Stall holds the register: with stall asserted and no flush, q retains its "
            "value so the stage freezes.",
        ),
        q(
            "What builds an N-bit ripple-carry adder bit by bit in reusable RTL?",
            (
                opt("A runtime for-loop in always_ff"),
                opt("A genvar generate-for over the bit slices", correct=True),
                opt("A single assign with no parameters"),
                opt("A covergroup"),
            ),
            "generate-for with a genvar elaborates one full-adder slice per bit into "
            "parallel hardware.",
        ),
        q(
            "What is a key benefit of passing a packed struct through a pipeline register?",
            (
                opt("It runs without a clock"),
                opt("The whole bundle moves as one typed signal, changed in one place", correct=True),
                opt("It removes the need for reset"),
                opt("It halves the latency"),
            ),
            "A packed struct bundles related fields into one vector, so the pipeline "
            "carries them together and edits happen in a single definition.",
        ),
        q(
            "What is 'coverage closure'?",
            (
                opt("Closing the simulator window"),
                opt("Reaching full functional coverage with all checks passing", correct=True),
                opt("Disabling assertions"),
                opt("Routing the chip"),
            ),
            "Signoff requires both: every check passes AND coverage of the intended "
            "behaviour is complete.",
        ),
        q(
            "How is a simulation clock typically generated in a testbench?",
            (
                opt("assign clk = 1;"),
                opt("always #5 clk = ~clk;", correct=True),
                opt("always_comb clk = ~clk;"),
                opt("It is driven by the DUT"),
            ),
            "Toggling clk every fixed delay (e.g. #5) creates a free-running clock for "
            "the testbench to drive the DUT.",
        ),
    ),
)
