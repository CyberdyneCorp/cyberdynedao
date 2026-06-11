"""Curated quiz questions for the FPGA & Reconfigurable Computing - Basics
course (per-lesson checkpoints + a final comprehensive quiz). Keys are the
EXACT content-lesson titles so the seed can interleave a checkpoint quiz after
each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What an FPGA is: LUTs, flip-flops & the fabric": (
            q(
                "What is a k-input LUT, fundamentally?",
                (
                    opt("A dedicated hardware multiplier"),
                    opt("A tiny 2^k-bit memory addressed by its k inputs", correct=True),
                    opt("A programmable clock generator"),
                    opt("A bank of configurable I/O pins"),
                ),
                "A k-input LUT is a 2^k-bit memory: the inputs form the address and the stored bit is the output, so it can implement any truth table.",
            ),
            q(
                "How many distinct logic functions can a k-input LUT be programmed into?",
                (
                    opt("2^(2^k)", correct=True),
                    opt("2^k"),
                    opt("k^2"),
                    opt("2*k"),
                ),
                "A k-input LUT can realize 2^(2^k) distinct functions; a 6-input LUT is one of 2^64, which is why the 6-LUT is the universal building block.",
            ),
            q(
                "According to the lesson, what is the key advantage of an FPGA over a CPU?",
                (
                    opt("It always runs at a higher clock speed"),
                    opt("It is cheaper than an ASIC at high volume"),
                    opt("The hardware itself is programmable and massively parallel", correct=True),
                    opt("It needs no configuration after power-up"),
                ),
                "Unlike a CPU running instructions on fixed hardware, an FPGA becomes the hardware: it is reconfigurable, massively parallel, and low-latency.",
            ),
        ),
        "The FPGA design flow: RTL to bitstream": (
            q(
                "What does synthesis produce from RTL in the design flow?",
                (
                    opt("A placed-and-routed layout"),
                    opt("A netlist of generic gates mapped onto the chip primitives", correct=True),
                    opt("The final bitstream"),
                    opt("A static timing report"),
                ),
                "Synthesis translates RTL into a netlist of generic gates, then maps it onto the chip LUTs, flip-flops, block RAM, and DSP slices.",
            ),
            q(
                "Which step of the flow is described as the slow, NP-hard part?",
                (
                    opt("Synthesis"),
                    opt("Place-and-route", correct=True),
                    opt("Bitstream generation"),
                    opt("Static timing analysis"),
                ),
                "Place-and-route decides where each LUT/FF goes and wires them; the lesson calls it the slow, NP-hard part of the flow.",
            ),
            q(
                "Which toolchain belongs to the open-source FPGA flow named in the lesson?",
                (
                    opt("Vivado"),
                    opt("Quartus"),
                    opt("Yosys + nextpnr", correct=True),
                    opt("Vitis"),
                ),
                "The open-source flow uses Yosys for synthesis and nextpnr for place-and-route, targeting devices like the iCE40 and ECP5.",
            ),
        ),
        "RTL for FPGA: combinational vs sequential logic": (
            q(
                "Which assignment operator should be used inside a clocked always_ff block?",
                (
                    opt("Blocking ="),
                    opt("Non-blocking <=", correct=True),
                    opt("Either, they are equivalent"),
                    opt("The continuous assign keyword"),
                ),
                "The golden rule is non-blocking <= in clocked blocks and blocking = in combinational blocks.",
            ),
            q(
                "What happens if a combinational block fails to assign its output for every input case?",
                (
                    opt("The synthesizer infers an unwanted latch", correct=True),
                    opt("It infers a block RAM"),
                    opt("It raises a clock-domain-crossing error"),
                    opt("It automatically adds a flip-flop"),
                ),
                "A combinational block must drive its output for every input case, otherwise the tool infers an unwanted latch (a memory element).",
            ),
            q(
                "What sets the maximum clock speed of a synchronous design?",
                (
                    opt("The number of I/O pins used"),
                    opt("The amount of combinational logic between two flip-flops", correct=True),
                    opt("The total number of flip-flops"),
                    opt("The size of the bitstream file"),
                ),
                "The longest path of combinational logic between two flip-flops sets the longest delay, which sets Fmax; this is why deep logic is pipelined.",
            ),
        ),
        "FPGA primitives & resources: block RAM, DSP & clocks": (
            q(
                "What is a DSP slice used for?",
                (
                    opt("Distributing low-skew clocks"),
                    opt("A hardened multiply-accumulate operation", correct=True),
                    opt("Driving configurable I/O pins"),
                    opt("Multi-gigabit serial links"),
                ),
                "A DSP slice is a hardened multiply-accumulate block (e.g. 18x18 then add), used for filters, FFTs, matrix multiply, and ML.",
            ),
            q(
                "How do you get the tool to infer a block RAM rather than build memory from flip-flops?",
                (
                    opt("Use a combinational read"),
                    opt("Use a registered read", correct=True),
                    opt("Instantiate a DSP slice"),
                    opt("Add a clock constraint"),
                ),
                "Writing memory with a registered read makes the tool infer BRAM instead of building it from flip-flops.",
            ),
            q(
                "Roughly how does the LUT cost of an N-bit multiplier built from logic grow?",
                (
                    opt("On the order of N^2", correct=True),
                    opt("On the order of log N"),
                    opt("Linearly with N"),
                    opt("It stays constant"),
                ),
                "An N-bit multiply built from LUTs costs on the order of N^2 logic, whereas a DSP slice does the multiply in one hardened block.",
            ),
        ),
        "Constraints & getting started: pins, clocks & a first project": (
            q(
                "What does a clock-period constraint enable the tool to do?",
                (
                    opt("Place I/O on the correct package pins"),
                    opt("Check timing on every path via static timing analysis", correct=True),
                    opt("Generate the bitstream faster"),
                    opt("Infer block RAM automatically"),
                ),
                "A clock-period constraint is what STA measures every path against; no clock constraint means no timing check.",
            ),
            q(
                "What is the traditional first FPGA project, and why?",
                (
                    opt("A UART, because it proves I/O timing"),
                    opt(
                        "A blinking LED, because it proves the toolchain, clock, pin map, and board",
                        correct=True,
                    ),
                    opt("A DSP filter, because it exercises the DSP slices"),
                    opt("A soft processor, because it runs software"),
                ),
                "The blinky LED is every FPGA hello-world: it proves the toolchain, the clock, the pin map, and the board all work.",
            ),
            q(
                "Using counter bit b to drive an LED from clock f_clk, what is the blink frequency?",
                (
                    opt("f_clk / 2^(b+1)", correct=True),
                    opt("f_clk * 2^b"),
                    opt("f_clk / b"),
                    opt("f_clk * b / 2"),
                ),
                "The blink frequency is f_clk divided by 2^(b+1); you pick the bit so the blink lands near 1 Hz to be visible.",
            ),
        ),
        "Lab: LUT logic & resource utilization vs design size": (
            q(
                "In the lab, why is a 4-input LUT equal to its 16-bit truth table?",
                (
                    opt("Because 4 inputs form a 16-entry address space (2^4 = 16)", correct=True),
                    opt("Because each input needs 4 config bits"),
                    opt("Because a LUT has 16 physical pins"),
                    opt("Because 4 times 4 equals 16"),
                ),
                "The 4 inputs are the address into a 2^4 = 16 entry table, so the 16 stored config bits fully define the function.",
            ),
            q(
                "What utilization threshold does the lab flag as where timing closure gets hard?",
                (
                    opt("50%"),
                    opt("80%", correct=True),
                    opt("95%"),
                    opt("100%"),
                ),
                "The lab marks 80% utilization as the line where timing closure gets hard, with 100% being a fully used device.",
            ),
            q(
                "In the lab heuristic, what happens to achievable Fmax as the device fills up?",
                (
                    opt("It rises due to shorter routes"),
                    opt("It stays constant regardless of utilization"),
                    opt("It sags because of congestion", correct=True),
                    opt("It becomes undefined above 50%"),
                ),
                "The lab uses a heuristic where Fmax sags as the device fills, modeling routing congestion as utilization rises.",
            ),
        ),
    },
    final=(
        q(
            "Which three ingredients make up the FPGA fabric described in the course?",
            (
                opt("CPUs, caches, and buses"),
                opt("LUTs, flip-flops, and the routing fabric", correct=True),
                opt("Transistors, resistors, and capacitors"),
                opt("Synthesis, place-and-route, and bitstream"),
            ),
            "An FPGA is built from LUTs (implementing logic), flip-flops (storing state), and a programmable routing fabric wiring them together.",
        ),
        q(
            "Put the design-flow steps in order from source to programmed chip.",
            (
                opt("Bitstream, place-and-route, synthesis, RTL"),
                opt("RTL, synthesis, place-and-route, bitstream", correct=True),
                opt("Synthesis, RTL, bitstream, place-and-route"),
                opt("RTL, place-and-route, synthesis, bitstream"),
            ),
            "You write RTL, synthesis maps it to a netlist of primitives, place-and-route assigns and wires them, then a bitstream programs the chip.",
        ),
        q(
            "To keep an arithmetic-heavy design small and fast, what should you map operations onto?",
            (
                opt("More LUTs and flip-flops"),
                opt("DSP slices for arithmetic and BRAM for memory", correct=True),
                opt("Additional I/O banks"),
                opt("The routing fabric only"),
            ),
            "Mapping multiplies onto DSP slices and memories onto BRAM is most of FPGA performance engineering; a design that ran out of LUTs often just failed to use the hardened blocks.",
        ),
        q(
            "Why does deep combinational logic between flip-flops hurt a design?",
            (
                opt("It increases the bitstream size"),
                opt("It lengthens the path delay and lowers Fmax", correct=True),
                opt("It infers extra block RAM"),
                opt("It violates pin constraints"),
            ),
            "More logic levels between registers lengthen the path delay, which lowers the maximum clock frequency Fmax; the fix is pipelining.",
        ),
        q(
            "Which two constraints does the course say you cannot skip?",
            (
                opt("Power budget and temperature limits"),
                opt("Pin location with I/O standard, and the clock period", correct=True),
                opt("Synthesis effort and routing effort"),
                opt("FIFO depth and burst length"),
            ),
            "RTL says nothing about physical pins or clock speed, so the pin (location plus I/O standard) and clock-period constraints are mandatory.",
        ),
    ),
)
