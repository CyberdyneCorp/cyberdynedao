from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Soft processors & the embedded FPGA SoC": (
            q(
                "What is a soft processor on an FPGA?",
                (
                    opt("A hardened ARM core fabricated in the silicon"),
                    opt("An entire CPU built out of FPGA fabric (LUTs)", correct=True),
                    opt("A software emulator running on a host PC"),
                    opt("A DSP slice configured as a multiplier"),
                ),
                "A soft processor is an entire CPU built out of FPGA fabric, costing only LUTs.",
            ),
            q(
                "Why is RISC-V described as the momentum pick for soft cores?",
                (
                    opt("It is the fastest core, running at 1 GHz on fabric"),
                    opt("It is the only core with a UART peripheral"),
                    opt(
                        "It is an open instruction set you can extend with custom instructions",
                        correct=True,
                    ),
                    opt("It requires a per-unit license fee from AMD"),
                ),
                "RISC-V is an open ISA you can extend with custom instructions dropped into the fabric.",
            ),
            q(
                "When does a bare-metal approach (no OS) fit best?",
                (
                    opt("When you need full networking and filesystems"),
                    opt("When you want tasks and scheduling for complex firmware"),
                    opt("For tight, deterministic, lowest-latency control loops", correct=True),
                    opt("When running on a hard Zynq PS core only"),
                ),
                "Bare-metal gives lowest latency and full determinism, ideal for tight control loops.",
            ),
        ),
        "High-level synthesis: from C to RTL": (
            q(
                "What does high-level synthesis (HLS) do?",
                (
                    opt("Converts RTL back into a C/C++ algorithm"),
                    opt(
                        "Generates RTL from a C/C++ algorithm, scheduling operations into cycles",
                        correct=True,
                    ),
                    opt("Replaces place-and-route with manual floorplanning"),
                    opt("Runs the C code on a soft core instead of building hardware"),
                ),
                "HLS describes the algorithm in C/C++ and generates RTL, scheduling ops into cycles.",
            ),
            q(
                "What does the PIPELINE pragma control?",
                (
                    opt("It replicates the loop body K times to run in parallel"),
                    opt("It infers the on-chip memories for arrays"),
                    opt(
                        "The initiation interval II, how often a new loop iteration starts",
                        correct=True,
                    ),
                    opt("The clock frequency of the generated datapath"),
                ),
                "PIPELINE overlaps iterations so a new one starts every II cycles; II=1 is one result per cycle.",
            ),
            q(
                "What is the central tradeoff when unrolling a loop by K?",
                (
                    opt("It reduces latency but cannot change the clock"),
                    opt(
                        "It cuts iteration count by K but uses K copies of the datapath",
                        correct=True,
                    ),
                    opt("It always reduces hardware while increasing speed"),
                    opt("It only works for fixed-point types"),
                ),
                "Unrolling by K cuts the iteration count by K but costs K copies of the datapath.",
            ),
        ),
        "Hardware acceleration: parallelism, dataflow & the roofline": (
            q(
                "In task/dataflow parallelism, what passes data between concurrent kernels?",
                (
                    opt("A shared cache hierarchy"),
                    opt("FIFOs such as AXI-Stream", correct=True),
                    opt("The instruction fetch unit"),
                    opt("A single global register file"),
                ),
                "Dataflow kernels run concurrently and pass data through FIFOs (AXI-Stream).",
            ),
            q(
                "According to Amdahl's law, what caps the overall speedup?",
                (
                    opt("The serial remainder (1 - p) of the work", correct=True),
                    opt("The clock frequency of the accelerator"),
                    opt("The number of DSP slices available"),
                    opt("The size of the configuration bitstream"),
                ),
                "The serial fraction (1-p) caps everything no matter how fast you accelerate the parallel part.",
            ),
            q(
                "On the roofline, when is a kernel memory-bound?",
                (
                    opt("When operational intensity is above the ridge point"),
                    opt("When performance equals peak compute"),
                    opt(
                        "Below the ridge intensity, where bandwidth times intensity caps performance",
                        correct=True,
                    ),
                    opt("Only when the kernel uses no external memory"),
                ),
                "Below the ridge intensity you are memory-bound on the slanted roof (BW times intensity).",
            ),
        ),
        "Partial reconfiguration, reliability & multi-die": (
            q(
                "What does dynamic/partial reconfiguration (DPR) allow?",
                (
                    opt(
                        "Reprogramming part of the chip while the static region keeps running",
                        correct=True,
                    ),
                    opt("Running two clocks in the same domain"),
                    opt("Converting BRAM into LUTs at runtime"),
                    opt("Permanently fusing the bitstream into the die"),
                ),
                "DPR swaps logic in a reconfigurable partition at runtime while the static region operates.",
            ),
            q(
                "What is a single-event upset (SEU)?",
                (
                    opt("A timing violation on a critical path"),
                    opt(
                        "A particle flipping a configuration bit, silently changing the logic",
                        correct=True,
                    ),
                    opt("A failure to meet the initiation interval"),
                    opt("A crossing delay between two SLRs"),
                ),
                "A cosmic ray or particle can flip a config bit; since the bitstream is the circuit, the logic changes.",
            ),
            q(
                "Why does TMR (triple modular redundancy) improve reliability at low p?",
                (
                    opt("It removes the need for configuration scrubbing"),
                    opt("It triples the clock frequency of critical logic"),
                    opt(
                        "The majority voter only fails if two or three of the three copies are hit",
                        correct=True,
                    ),
                    opt("It guarantees no upset can ever occur"),
                ),
                "TMR triples critical logic and votes; one upset is outvoted, so it only fails on two or three hits.",
            ),
        ),
        "Verification & debug on FPGA: simulation, ILA & coverage": (
            q(
                "What does a testbench in a simulator do?",
                (
                    opt("Loads the bitstream onto the physical FPGA"),
                    opt("Drives inputs to the RTL and checks its outputs", correct=True),
                    opt("Measures BRAM usage of the debug core"),
                    opt("Floorplans logic to keep paths within one SLR"),
                ),
                "A testbench drives inputs and checks outputs in a simulator, fast and fully visible.",
            ),
            q(
                "What does coverage measure in verification?",
                (
                    opt("How fast the simulator runs per cycle"),
                    opt("How much of the design's behaviour your tests exercised", correct=True),
                    opt("The number of LUTs the design consumes"),
                    opt("The reliability of the design under radiation"),
                ),
                "Coverage measures how much of the design's behaviour your tests actually exercised.",
            ),
            q(
                "What is an Integrated Logic Analyzer (ILA / SignalTap)?",
                (
                    opt("A simulator that runs before hardware"),
                    opt("A pragma that pipelines a loop"),
                    opt(
                        "A debug core that captures chosen signals into BRAM, triggered then streamed over JTAG",
                        correct=True,
                    ),
                    opt("A voter circuit for triplicated logic"),
                ),
                "An ILA is an on-chip oscilloscope: it uses BRAM to capture signals on a trigger and streams them over JTAG.",
            ),
        ),
        "Lab: accelerator throughput & parallel speedup": (
            q(
                "In the lab, what caps the overall speedup as the accelerator speedup grows?",
                (
                    opt("The number of MAC lanes"),
                    opt(
                        "The serial fraction, so even infinite hardware at p=0.99 caps at 100x",
                        correct=True,
                    ),
                    opt("The matplotlib figure size"),
                    opt("The 300 MHz fabric clock alone"),
                ),
                "Amdahl: at p=0.99 even infinite hardware caps overall speedup at 1/(1-0.99) = 100x.",
            ),
            q(
                "In the roofline part of the lab, what happens when you add MAC lanes past the ridge?",
                (
                    opt("Attainable performance keeps rising linearly"),
                    opt("The memory roof rises with each lane"),
                    opt(
                        "Adding lanes wastes silicon because the kernel is memory-bound",
                        correct=True,
                    ),
                    opt("The fabric clock drops to compensate"),
                ),
                "Past the ridge the kernel is memory-bound, so extra lanes waste silicon at the memory roof.",
            ),
            q(
                "Per the lab, how do you lift the memory roof so more lanes pay off?",
                (
                    opt("Reduce the number of parallel MAC lanes"),
                    opt(
                        "Raise bandwidth (e.g. HBM) or raise operational intensity by keeping data on-chip",
                        correct=True,
                    ),
                    opt("Lower the fabric clock below 300 MHz"),
                    opt("Increase the serial fraction of the workload"),
                ),
                "Raising bw_gbs (HBM) or operational intensity (more reuse per byte) lifts the memory roof.",
            ),
        ),
        "Applications & the throughline: data centers, SDR & vision": (
            q(
                "Why do high-frequency trading systems use FPGAs?",
                (
                    opt("They are the cheapest option at every volume"),
                    opt("They react with low, deterministic latency, in nanoseconds", correct=True),
                    opt("They run a full Linux networking stack fastest"),
                    opt("They require no bitstream to operate"),
                ),
                "HFT uses FPGAs for low, deterministic latency, reacting in nanoseconds below any software path.",
            ),
            q(
                "Why is software-defined radio a good fit for FPGAs?",
                (
                    opt(
                        "The physical layer math is fixed-rate, parallel, and deterministic streaming DSP",
                        correct=True,
                    ),
                    opt("Radio processing is mostly serial control code"),
                    opt("FPGAs are the only chips with floating-point units"),
                    opt("SDR needs no real-time guarantees"),
                ),
                "The radio physical layer (filters, FFTs, modulation) is the fixed-rate, parallel streaming DSP FPGAs excel at.",
            ),
            q(
                "In the FPGA-vs-ASIC cost model, what mainly decides the crossover?",
                (
                    opt("The clock frequency of the design"),
                    opt("Production volume balancing NRE against per-unit cost", correct=True),
                    opt("The number of SLRs in the package"),
                    opt("The coverage achieved in simulation"),
                ),
                "Cost = NRE + c_unit * V; below the crossover volume the FPGA's near-zero NRE wins, above it the ASIC's low per-unit cost wins.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about soft cores versus a hard core is correct?",
            (
                opt("Soft cores run faster single-thread than a 1 GHz hard core"),
                opt(
                    "Soft cores cost only LUTs and win on parallel, customizable, deterministic work",
                    correct=True,
                ),
                opt("Hard cores cannot run Linux"),
                opt("Soft cores cannot be extended with custom instructions"),
            ),
            "A soft RISC-V runs ~100-200 MHz but costs only LUTs, so you can instantiate several for parallel work.",
        ),
        q(
            "For an HLS loop pipelined at initiation interval II over N iterations with latency L, the total cycles are about?",
            (
                opt("N * L"),
                opt("(N - 1) * II + L", correct=True),
                opt("II / N + L"),
                opt("L - (N - 1) * II"),
            ),
            "Total cycles approximate (N-1)*II + L, so driving II to 1 dominates throughput as N grows.",
        ),
        q(
            "How do FPGAs raise operational intensity to beat the memory roof?",
            (
                opt("By adding more external memory channels only"),
                opt(
                    "By keeping data on-chip (BRAM, streaming) instead of thrashing external memory",
                    correct=True,
                ),
                opt("By lowering the fabric clock"),
                opt("By using bare-metal firmware on a soft core"),
            ),
            "FPGAs keep data on-chip via BRAM and streaming to raise operational intensity instead of thrashing memory.",
        ),
        q(
            "Which pair of defenses protects FPGA configuration against single-event upsets?",
            (
                opt("Pipelining and unrolling"),
                opt("Configuration scrubbing and triple modular redundancy (TMR)", correct=True),
                opt("Constrained-random tests and assertions"),
                opt("Floorplanning and HBM in package"),
            ),
            "Scrubbing reads back and corrects config memory via ECC; TMR triplicates and votes so one upset is outvoted.",
        ),
        q(
            "What does the ILA debug core trade off when capturing signals?",
            (
                opt("Clock frequency against the number of soft cores"),
                opt("Capture width against depth, since W x D bits of BRAM are used", correct=True),
                opt("NRE against per-unit cost"),
                opt("Parallel fraction p against accelerator speedup s"),
            ),
            "Capturing W bits at depth D uses about W*D bits of BRAM, so there is always a width-vs-depth budget.",
        ),
    ),
)
