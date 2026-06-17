"""Quiz spec for the SystemVerilog -- Intermediate (FSMs, Datapaths & Memory) course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Finite state machines in SystemVerilog": (
            q(
                "In the two-process FSM style, what does the always_ff block do?",
                (
                    opt("Computes the next state and outputs"),
                    opt("Holds the current state, updating it on the clock edge", correct=True),
                    opt("Both next-state and output logic"),
                    opt("Nothing -- it is optional"),
                ),
                "The sequential block just registers the state; a separate always_comb "
                "computes next-state and outputs.",
            ),
            q(
                "How does a Moore output differ from a Mealy output?",
                (
                    opt("Moore depends on state only; Mealy on state and inputs", correct=True),
                    opt("Moore is asynchronous; Mealy is clocked"),
                    opt("Moore needs no reset"),
                    opt("They are the same thing"),
                ),
                "Moore outputs are a function of state alone (glitch-free, one cycle "
                "latency); Mealy outputs also depend on inputs.",
            ),
        ),
        "Building a register file": (
            q(
                "What does a '2R1W' register file provide?",
                (
                    opt("Two write ports and one read port"),
                    opt("Two read ports and one write port", correct=True),
                    opt("One combined read/write port"),
                    opt("Two of everything"),
                ),
                "A classic RISC register file reads two operands and writes one result "
                "per cycle: two read ports, one write port.",
            ),
            q(
                "Why is register x0 handled specially on read?",
                (
                    opt("It is the fastest register"),
                    opt("It is hardwired to zero, so reads must return 0", correct=True),
                    opt("It stores the program counter"),
                    opt("It cannot be read"),
                ),
                "In RISC-V/MIPS x0 always reads as zero regardless of any write, so the "
                "read port forces 0 for address 0.",
            ),
        ),
        "An ALU with status flags": (
            q(
                "What is the difference between the Carry and oVerflow flags?",
                (
                    opt("Carry is signed overflow; overflow is unsigned"),
                    opt(
                        "Carry is the unsigned out-of-range signal; overflow is the signed one",
                        correct=True,
                    ),
                    opt("They always have the same value"),
                    opt("Carry is for subtraction only"),
                ),
                "Carry flags unsigned wrap/borrow; overflow flags signed wrap. They are "
                "independent because they describe different number interpretations.",
            ),
            q(
                "How is the Zero flag computed from the ALU result y?",
                (
                    opt("y[0] == 1"),
                    opt("y == '0 (all bits zero)", correct=True),
                    opt("y[W-1] == 1"),
                    opt("The carry-out is 1"),
                ),
                "Zero is set when every bit of the result is 0; branches like beq use it.",
            ),
        ),
        "Inferring memory: RAM and ROM": (
            q(
                "What RTL feature makes the tool infer a block RAM instead of flip-flops?",
                (
                    opt("A combinational (asynchronous) read"),
                    opt("A registered (clocked) read", correct=True),
                    opt("Using the 'reg' keyword"),
                    opt("A large initial block"),
                ),
                "A clocked read matches the block-RAM template; an asynchronous read "
                "tends to map to LUT/flip-flop memory instead.",
            ),
            q(
                "How is a ROM's contents typically initialized in synthesizable RTL?",
                (
                    opt("With a runtime for-loop"),
                    opt("With an initial block, e.g. $readmemh of a hex file", correct=True),
                    opt("By writing every location at reset"),
                    opt("It cannot be initialized"),
                ),
                "$readmemh/$readmemb in an initial block loads ROM contents at time 0, "
                "which synthesis honors for FPGA memory init.",
            ),
        ),
    },
    final=(
        q(
            "Why name FSM states with a typedef enum?",
            (
                opt("It makes the circuit faster"),
                opt(
                    "Readable waveforms and the tool can catch illegal-state assignments",
                    correct=True,
                ),
                opt("It is required by SystemVerilog"),
                opt("It reduces the number of flip-flops to zero"),
            ),
            "An enum gives states names in waveforms and lets the compiler check you "
            "never assign an undefined state.",
        ),
        q(
            "A pipeline reads a register the same cycle it is being written. What must you decide?",
            (
                opt("Whether the read sees the old or the newly written value", correct=True),
                opt("Which clock edge to use"),
                opt("How many read ports to add"),
                opt("Whether to use a ROM"),
            ),
            "Same-cycle write/read needs an explicit policy (and often a bypass) so the "
            "reader gets the intended value.",
        ),
        q(
            "Set-less-than (slt) on signed operands should use which comparison?",
            (
                opt("a < b on the raw bits"),
                opt("$signed(a) < $signed(b)", correct=True),
                opt("a == b"),
                opt("$unsigned(a) < $unsigned(b)"),
            ),
            "Signed slt must compare with signed semantics; otherwise negative numbers "
            "(high bit set) look large.",
        ),
        q(
            "Why copy a vendor's exact memory inference template?",
            (
                opt("It is shorter to type"),
                opt("Small deviations can cost the block RAM and wreck timing", correct=True),
                opt("Templates are legally required"),
                opt("It changes the data width automatically"),
            ),
            "Inference is pattern-matched; deviating from the template can drop you to "
            "flip-flop memory and miss timing.",
        ),
    ),
)
