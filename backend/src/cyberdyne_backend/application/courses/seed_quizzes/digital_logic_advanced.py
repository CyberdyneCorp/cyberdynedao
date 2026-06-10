from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Datapaths & arithmetic": (
            q(
                "What is the role of the datapath versus the control path?",
                (
                    opt(
                        "The datapath moves and transforms data while an FSM control path says when",
                        correct=True,
                    ),
                    opt("The datapath decides timing while the control path holds the registers"),
                    opt("The control path performs the arithmetic and the datapath sequences it"),
                    opt("They are two names for the same combinational block"),
                ),
                "A datapath has adders, multipliers, ALUs and registers; the FSM control path tells it what to do when.",
            ),
            q(
                "Why does a ripple-carry adder get slower as the width N grows?",
                (
                    opt(
                        "The carry must ripple through all N stages so delay grows with N",
                        correct=True,
                    ),
                    opt("Each stage needs an extra clock cycle to settle"),
                    opt("The generate and propagate signals are computed in parallel"),
                    opt("Wider operands need more registers in the control path"),
                ),
                "In a ripple-carry adder the carry propagates serially through every full adder, so delay scales with N.",
            ),
            q(
                "In a pipelined multiplier, what improves when you split the path with registers?",
                (
                    opt(
                        "Throughput: a result every cycle once the pipe is full, at a faster clock",
                        correct=True,
                    ),
                    opt("Latency in nanoseconds drops to zero"),
                    opt("Area shrinks because fewer gates are needed"),
                    opt("The carry-lookahead logic is no longer required"),
                ),
                "Pipelining keeps the same nanosecond latency but lets you clock faster and get a result every cycle.",
            ),
        ),
        "Advanced SystemVerilog & VHDL": (
            q(
                "Which pair are the compile-time constant features in SystemVerilog and VHDL?",
                (
                    opt("parameter in SystemVerilog and generic in VHDL", correct=True),
                    opt("interface in SystemVerilog and record in VHDL"),
                    opt("package in SystemVerilog and generate in VHDL"),
                    opt("struct in SystemVerilog and array in VHDL"),
                ),
                "SystemVerilog uses parameter and VHDL uses generic for compile-time constants.",
            ),
            q(
                "What makes a SystemVerilog interface a standout feature?",
                (
                    opt(
                        "It bundles a whole bus into one connection, cutting port lists to one",
                        correct=True,
                    ),
                    opt("It runs only in simulation and is stripped before synthesis"),
                    opt("It replaces the need for any package definitions"),
                    opt("It computes carries in parallel like a lookahead adder"),
                ),
                "Interfaces (with modports) bundle data, valid, ready and more into a single connection.",
            ),
            q(
                "Which construct is simulation-only and NOT part of the synthesizable subset?",
                (
                    opt("initial blocks with #delays and fork/join", correct=True),
                    opt("always_comb combinational logic"),
                    opt("always_ff sequential logic"),
                    opt("generate loops with parameters"),
                ),
                "always_comb, always_ff, generate and parameters synthesize; initial, #delays, class and fork/join are sim-only.",
            ),
        ),
        "Memories, FIFOs & LFSRs": (
            q(
                "How do you get block RAM on an FPGA or ASIC in your HDL?",
                (
                    opt(
                        "Write a memory pattern the tool recognizes and it infers block RAM",
                        correct=True,
                    ),
                    opt("Instantiate the RAM primitive by its vendor name directly"),
                    opt("Use an initial block to preload the memory contents"),
                    opt("Declare the array inside an interface so it is bundled"),
                ),
                "You write a memory template (e.g. a registered read) and the synthesizer infers block RAM.",
            ),
            q(
                "What is the standard safe way to move a bus across clock domains?",
                (
                    opt(
                        "An asynchronous FIFO with Gray-coded pointers through synchronizers",
                        correct=True,
                    ),
                    opt("A single flip-flop on each bus bit"),
                    opt("A ripple-carry adder between the two domains"),
                    opt("A combinational read from block RAM"),
                ),
                "An async FIFO with Gray-coded pointers is the bus-level answer for crossing clock domains safely.",
            ),
            q(
                "What property does a maximal-length LFSR have?",
                (
                    opt(
                        "With the right taps it cycles through all 2^n - 1 nonzero states",
                        correct=True,
                    ),
                    opt("It cycles through all 2^n states including zero"),
                    opt("It generates true random numbers from thermal noise"),
                    opt("It infers a block RAM instead of flip-flops"),
                ),
                "A maximal-length LFSR with correct taps visits every nonzero state, useful for pseudo-random patterns and CRCs.",
            ),
        ),
        "Advanced verification with CocoTB": (
            q(
                "What is the modern alternative to directed tests that miss corner cases?",
                (
                    opt(
                        "Constrained-random stimulus with self-checking scoreboards and coverage",
                        correct=True,
                    ),
                    opt("Running the same fixed vectors more times"),
                    opt("Manually reading the waveform after each run"),
                    opt("Synthesizing the design and checking timing"),
                ),
                "Modern verification uses constrained-random stimulus, scoreboards and coverage instead of only directed tests.",
            ),
            q(
                "What is the purpose of a reference model (scoreboard) in CocoTB?",
                (
                    opt(
                        "Compute the expected result independently and compare to the DUT",
                        correct=True,
                    ),
                    opt("Track which input ops were actually exercised"),
                    opt("Drive random values onto the bus protocol"),
                    opt("Map the RTL onto the target primitives"),
                ),
                "The reference model computes the golden answer independently; a gap between it and the DUT is a bug.",
            ),
            q(
                "CocoTB's Python verification methodology mirrors which SystemVerilog approach?",
                (
                    opt("UVM, the SystemVerilog verification methodology", correct=True),
                    opt("The synthesizable subset of SystemVerilog"),
                    opt("The generate construct for repeated hardware"),
                    opt("Static timing analysis of the critical path"),
                ),
                "CocoTB mirrors UVM (drivers, monitors, scoreboards, coverage) but in Python.",
            ),
        ),
        "FPGA vs. ASIC & the synthesis flow": (
            q(
                "What distinguishes an FPGA from an ASIC?",
                (
                    opt(
                        "An FPGA is a reconfigurable chip while an ASIC is custom-fabricated silicon",
                        correct=True,
                    ),
                    opt("An FPGA has huge up-front mask cost while an ASIC reprograms in minutes"),
                    opt("An ASIC is reconfigurable while an FPGA needs a fab spin"),
                    opt("Both are reprogrammed by editing the RTL at runtime"),
                ),
                "FPGAs are reconfigurable (LUTs, FFs, DSPs, block RAM); ASICs are custom silicon with high up-front cost.",
            ),
            q(
                "What is the correct order of the RTL-to-hardware flow?",
                (
                    opt(
                        "Synthesis, then place and route, then timing analysis, then bitstream or layout",
                        correct=True,
                    ),
                    opt("Place and route, then synthesis, then bitstream, then timing analysis"),
                    opt("Timing analysis, then synthesis, then place and route, then layout"),
                    opt("Synthesis, then timing analysis, then bitstream, then place and route"),
                ),
                "The flow is synthesis to a gate netlist, then place and route, then static timing analysis, then the bitstream or layout.",
            ),
            q(
                "What does static timing analysis check for every register-to-register path?",
                (
                    opt(
                        "That Tclk is at least tcq plus tlogic plus tsu, reporting the critical path",
                        correct=True,
                    ),
                    opt("That the design infers block RAM correctly"),
                    opt("That the random coverage hit every op"),
                    opt("That the FIFO pointers are Gray coded"),
                ),
                "STA checks the setup equation Tclk >= tcq + tlogic + tsu over real wire delays and reports the worst (critical) path.",
            ),
        ),
        "Applications & the throughline": (
            q(
                "How are processors like CPUs and GPUs described in hardware terms?",
                (
                    opt(
                        "Datapaths such as ALUs, register files and pipelines steered by FSMs",
                        correct=True,
                    ),
                    opt("Pure combinational logic with no memory or control"),
                    opt("Only constrained-random testbenches in CocoTB"),
                    opt("Asynchronous FIFOs with no datapath"),
                ),
                "CPUs, GPUs and microcontrollers are datapaths (ALUs, register files, pipelines) steered by FSMs.",
            ),
            q(
                "Which is true about SystemVerilog versus VHDL in the real world?",
                (
                    opt(
                        "SystemVerilog dominates US semiconductors and verification while VHDL is strong in Europe and aerospace",
                        correct=True,
                    ),
                    opt("VHDL has unmatched testbench features and dominates verification"),
                    opt("Only one of them is still used in industry today"),
                    opt("Neither can be verified using CocoTB or Python"),
                ),
                "SystemVerilog leads US semiconductors and verification; VHDL is strong in Europe, defense and aerospace for its strict typing.",
            ),
            q(
                "What is the throughline of digital design according to the lesson?",
                (
                    opt(
                        "Gates make combinational logic, flip-flops add memory, FSMs add control, datapaths do the work, and verification proves it",
                        correct=True,
                    ),
                    opt("Every design must be hand-drawn at the gate level"),
                    opt("Simulation passing always guarantees the chip works"),
                    opt("Verification can be skipped once synthesis succeeds"),
                ),
                "The discipline is the same set of ideas: combinational logic, memory, clocking, FSMs, datapaths and verification.",
            ),
        ),
    },
    final=(
        q(
            "Which adder computes carries in parallel using generate and propagate signals?",
            (
                opt("Carry-lookahead adder", correct=True),
                opt("Ripple-carry adder"),
                opt("Linear-feedback shift register"),
                opt("Asynchronous FIFO"),
            ),
            "A carry-lookahead adder uses gi (generate) and pi (propagate) to compute carries in parallel.",
        ),
        q(
            "Pipelining a long combinational path primarily improves which metric?",
            (
                opt(
                    "Throughput, by allowing a faster clock and a result every cycle", correct=True
                ),
                opt("Latency in nanoseconds, which drops to zero"),
                opt("Area, by removing all registers"),
                opt("Code coverage in the testbench"),
            ),
            "Pipelining raises throughput and clock rate while keeping nanosecond latency roughly the same.",
        ),
        q(
            "Which feature is part of the synthesizable subset rather than simulation-only?",
            (
                opt("generate loops with parameters", correct=True),
                opt("fork/join"),
                opt("class and dynamic arrays"),
                opt("initial blocks with #delays"),
            ),
            "generate, parameters, always_comb and always_ff synthesize; class, dynamic arrays, fork/join and initial are sim-only.",
        ),
        q(
            "Why is an asynchronous FIFO with Gray-coded pointers used between clock domains?",
            (
                opt(
                    "It safely moves a bus across clock domains through synchronizers", correct=True
                ),
                opt("It infers a faster block RAM than a single-port memory"),
                opt("It computes the critical path during timing analysis"),
                opt("It replaces the reference model in a scoreboard"),
            ),
            "Gray-coded pointers through synchronizers make the async FIFO the safe bus-level clock-domain crossing.",
        ),
        q(
            "A design passes CocoTB but fails at the target clock. What does this illustrate?",
            (
                opt(
                    "It simulates is not it works; you must read the timing report and fix the critical path",
                    correct=True,
                ),
                opt("Constrained-random stimulus was not used"),
                opt("The reference model had a coverage hole"),
                opt("The FIFO pointers were not Gray coded"),
            ),
            "A design can pass simulation yet fail static timing analysis; timing closure means fixing the critical path.",
        ),
    ),
)
