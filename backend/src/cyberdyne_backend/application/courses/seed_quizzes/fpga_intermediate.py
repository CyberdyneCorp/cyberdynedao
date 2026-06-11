from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Static timing analysis: setup, hold & Fmax": (
            q(
                "What does static timing analysis (STA) do?",
                (
                    opt("It simulates the design with test vectors to find bugs"),
                    opt(
                        "It checks setup/hold on all paths without simulating",
                        correct=True,
                    ),
                    opt("It synthesizes RTL into a netlist of LUTs"),
                    opt("It places and routes the design on the die"),
                ),
                "STA checks the setup/hold window for all paths without simulating, gating compiles from actually running.",
            ),
            q(
                "What is the critical path of a design?",
                (
                    opt("The shortest register-to-register path"),
                    opt("The path with the most fanout"),
                    opt(
                        "The slowest register-to-register path, which sets Fmax",
                        correct=True,
                    ),
                    opt("The path closest to the clock pin"),
                ),
                "Fmax is set by the critical path, the slowest register-to-register path in the design.",
            ),
            q(
                "What does negative slack on a path mean?",
                (
                    opt("There is timing margin to spare"),
                    opt("A timing violation: data arrives too late", correct=True),
                    opt("The path is unconstrained"),
                    opt("The clock is running too slowly"),
                ),
                "Slack is what is left over after the setup equation; negative slack means a timing violation.",
            ),
        ),
        "Clocking: PLLs, MMCMs & clock domains": (
            q(
                "A PLL produces an output frequency of fin times M divided by what?",
                (
                    opt("D times O (input divide times output divide)", correct=True),
                    opt("M times O"),
                    opt("Just D, the input divide"),
                    opt("The clock skew"),
                ),
                "fout = fin * M / (D * O), where M multiplies, D is the input divide, and O the output divide.",
            ),
            q(
                "What do MMCMs add on top of a basic PLL?",
                (
                    opt("Higher input voltage tolerance"),
                    opt(
                        "Fine phase shifting and dynamic reconfiguration",
                        correct=True,
                    ),
                    opt("Built-in FIFO buffering"),
                    opt("Automatic clock-domain crossing"),
                ),
                "MMCMs add fine phase shifting and dynamic reconfiguration, used to align a clock with data.",
            ),
            q(
                "Why can STA not guarantee timing for signals crossing between clock domains?",
                (
                    opt("The combinational logic is too deep"),
                    opt("The clocks are too fast"),
                    opt(
                        "The launch and capture clocks are unrelated",
                        correct=True,
                    ),
                    opt("The routing is unconstrained"),
                ),
                "Across domains the launch and capture clocks are unrelated, so STA cannot guarantee the setup/hold window.",
            ),
        ),
        "Metastability & the MTBF of a synchronizer": (
            q(
                "What is metastability in a flip-flop?",
                (
                    opt(
                        "The output hanging at an in-between voltage before resolving randomly",
                        correct=True,
                    ),
                    opt("The clock losing lock"),
                    opt("A permanent stuck-at fault"),
                    opt("Excess static power draw"),
                ),
                "On a setup/hold violation the output can hang at an in-between voltage for a while before resolving randomly to 0 or 1.",
            ),
            q(
                "How does synchronizer MTBF change as more settling time is allowed?",
                (
                    opt("It decreases linearly"),
                    opt("It grows exponentially with settling time", correct=True),
                    opt("It stays constant"),
                    opt("It depends only on the data rate"),
                ),
                "MTBF grows exponentially with settling time, so one more clock cycle buys astronomically more reliability.",
            ),
            q(
                "How does a 2-flip-flop synchronizer protect a single-bit crossing?",
                (
                    opt("It encodes the bit in Gray code"),
                    opt("It uses a FIFO to buffer the bit"),
                    opt(
                        "The first FF gets a full clock period to resolve before the second samples it",
                        correct=True,
                    ),
                    opt("It slows the destination clock"),
                ),
                "The first FF may go metastable but gets a full clock period to resolve before the second resamples it.",
            ),
        ),
        "Memory, FIFOs & AXI-Stream": (
            q(
                "What is a FIFO built from on an FPGA?",
                (
                    opt(
                        "Block RAM plus a write pointer, read pointer, and full/empty logic",
                        correct=True,
                    ),
                    opt("A chain of 2-flip-flop synchronizers"),
                    opt("A PLL and a clock tree"),
                    opt("A LUT-based adder tree"),
                ),
                "A FIFO is BRAM plus a write pointer and a read pointer and logic that reports full and empty.",
            ),
            q(
                "How is a multi-bit stream safely moved across a clock domain?",
                (
                    opt("By synchronizing each bit with its own 2-FF synchronizer"),
                    opt(
                        "With an asynchronous FIFO whose pointers cross in Gray code",
                        correct=True,
                    ),
                    opt("By slowing the producer to the consumer clock"),
                    opt("By using a single MMCM phase shift"),
                ),
                "An asynchronous FIFO is the canonical safe way, with pointers crossed in Gray code through synchronizers.",
            ),
            q(
                "In AXI4-Stream, when does a word actually transfer?",
                (
                    opt("On every rising clock edge"),
                    opt("Whenever tvalid is high"),
                    opt(
                        "Only on the cycle where both tvalid and tready are high",
                        correct=True,
                    ),
                    opt("Whenever tready is high"),
                ),
                "A word transfers only on the cycle where both tvalid and tready are high; this backpressure self-throttles the chain.",
            ),
        ),
        "FSMs & datapath design: pipelining for Fmax": (
            q(
                "What is the clean, synthesizable pattern for coding an FSM?",
                (
                    opt(
                        "Two or three processes: a clocked state register plus combinational next-state logic",
                        correct=True,
                    ),
                    opt("A single combinational block computing everything"),
                    opt(
                        "One clocked block that does state and outputs together with no next-state logic"
                    ),
                    opt("A FIFO feeding the state register"),
                ),
                "The clean pattern is a clocked block for the state register and a combinational block for next-state logic and outputs.",
            ),
            q(
                "What does pipelining a long combinational datapath trade off?",
                (
                    opt("It lowers Fmax to save latency"),
                    opt(
                        "It raises Fmax and throughput at the cost of more latency cycles",
                        correct=True,
                    ),
                    opt("It reduces both latency and throughput"),
                    opt("It removes the need for a clock"),
                ),
                "Pipelining inserts registers to shorten the critical path, raising Fmax and throughput at the cost of N cycles of latency.",
            ),
            q(
                "Why does adding pipeline stages give diminishing returns on Fmax?",
                (
                    opt("Each stage doubles the routing delay"),
                    opt("The clock skew grows with stages"),
                    opt(
                        "The per-stage register overhead eventually dominates",
                        correct=True,
                    ),
                    opt("BRAM runs out"),
                ),
                "Throughput rises with N but with diminishing returns as the per-stage register overhead floor dominates.",
            ),
        ),
        "On-chip interfaces & buses: AXI and the SoC FPGA": (
            q(
                "Which AXI variant is used for simple one-word-at-a-time register access?",
                (
                    opt("AXI4 (full)"),
                    opt("AXI4-Lite", correct=True),
                    opt("AXI4-Stream"),
                    opt("AXI-Coherent"),
                ),
                "AXI4-Lite is for simple register access (control/status), one word at a time.",
            ),
            q(
                "On a SoC FPGA like the Zynq, what is the split between PS and PL?",
                (
                    opt("PS is the programmable logic, PL is the processor"),
                    opt(
                        "PS is the hard ARM processing system, PL is the programmable logic",
                        correct=True,
                    ),
                    opt("Both PS and PL are soft cores in fabric"),
                    opt("PS and PL are two separate dies on a board"),
                ),
                "The PS is the hard ARM processing system running Linux; the PL is the programmable logic; they share memory over AXI.",
            ),
            q(
                "Why do longer AXI bursts approach peak bandwidth?",
                (
                    opt("They use a wider bus automatically"),
                    opt("They run at a higher clock frequency"),
                    opt(
                        "They amortize the per-transaction address overhead over many beats",
                        correct=True,
                    ),
                    opt("They skip the valid/ready handshake"),
                ),
                "Bursts move many beats per address, so long bursts amortize the addressing overhead and approach peak; BW = W f L/(L+h).",
            ),
        ),
        "Lab: CDC metastability MTBF & Fmax vs pipeline depth": (
            q(
                "In the lab, what effect does adding a synchronizer FF stage have on MTBF?",
                (
                    opt("It leaves MTBF unchanged"),
                    opt("Each stage multiplies the MTBF", correct=True),
                    opt("Each stage halves the MTBF"),
                    opt("It only matters above 400 MHz"),
                ),
                "The lab shows each FF stage adds a full period of settling, multiplying the MTBF (titled Each stage multiplies MTBF).",
            ),
            q(
                "How does raising fdata (more asynchronous crossings) affect the synchronizer in the lab?",
                (
                    opt("MTBF rises"),
                    opt("MTBF drops, and you add a stage to recover it", correct=True),
                    opt("Fmax falls"),
                    opt("Latency increases"),
                ),
                "The try-it-yourself note says raising fdata drops MTBF; adding a stage recovers it.",
            ),
            q(
                "Once a pipeline is full, what is its throughput in the lab model?",
                (
                    opt("One result every N cycles"),
                    opt("One result per clock (equal to Fmax)", correct=True),
                    opt("Zero until latency is paid each time"),
                    opt("Half of Fmax"),
                ),
                "Throughput once the pipe is full equals Fmax (one result per clock); latency is N cycles, paid only once.",
            ),
        ),
    },
    final=(
        q(
            "What sets the maximum clock frequency Fmax of a synchronous design?",
            (
                opt("The PLL feedback multiplier M"),
                opt("The critical path, the slowest register-to-register path", correct=True),
                opt("The FIFO depth"),
                opt("The AXI burst length"),
            ),
            "Fmax = 1/(tcq + tlogic + troute + tsu) and is set by the slowest register-to-register (critical) path.",
        ),
        q(
            "Which technique is the single most common timing-closure move?",
            (
                opt("Adding more clock domains"),
                opt("Widening the AXI bus"),
                opt("Pipelining a long combinational path into shorter stages", correct=True),
                opt("Increasing the PLL output divide"),
            ),
            "Pipelining splits a long combinational path with registers to shorten tlogic and is the most common timing-closure move.",
        ),
        q(
            "What is the safe way to move a multi-bit value across unrelated clock domains?",
            (
                opt("A 2-FF synchronizer on the whole bus"),
                opt("An asynchronous FIFO or a Gray-coded handshake", correct=True),
                opt("A combinational mux"),
                opt("An MMCM phase shift"),
            ),
            "Never sync a multi-bit bus bit-by-bit; use an async FIFO or a Gray-coded handshake.",
        ),
        q(
            "In AXI4-Stream, what guarantees a chain of FIFOs is self-throttling?",
            (
                opt("The PLL keeping all clocks aligned"),
                opt("The Gray-code pointer encoding"),
                opt("Backpressure via the valid/ready handshake", correct=True),
                opt("The burst-length amortization"),
            ),
            "The valid/ready (tvalid/tready) backpressure is what makes a FIFO chain self-throttling.",
        ),
        q(
            "On a SoC FPGA, how do software control and fast parallel work divide?",
            (
                opt("The CPU does the parallel math, the fabric runs Linux"),
                opt(
                    "The CPU runs slow irregular control, the fabric does fast parallel deterministic work, sharing memory over AXI",
                    correct=True,
                ),
                opt("Both run on soft cores with no shared memory"),
                opt("The fabric handles networking, the CPU does image processing"),
            ),
            "Software runs slow irregular control on the ARM cores; the fabric does fast parallel deterministic work; they share memory over AXI.",
        ),
    ),
)
