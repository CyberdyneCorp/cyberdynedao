from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Digital logic & a bit of history": (
            q(
                "Why do digital circuits agree to read only two voltage levels?",
                (
                    opt("Because transistors can only ever be fully on or fully off"),
                    opt(
                        "It buys enormous noise immunity, so a small glitch cannot flip a 0 into a 1",
                        correct=True,
                    ),
                    opt("Because the world is fundamentally analog and continuous"),
                    opt("To make the clock run billions of times per second"),
                ),
                "Reading only 0 and 1 gives noise immunity: a small glitch cannot cross the gap between the low and high thresholds.",
            ),
            q(
                "Whose 1937 work showed that Boolean algebra describes switching circuits?",
                (
                    opt("George Boole"),
                    opt("Claude Shannon", correct=True),
                    opt("Bardeen, Brattain, and Shockley"),
                    opt("The US Department of Defense"),
                ),
                "Claude Shannon's 1937 master's thesis connected Boolean algebra to switching relay circuits, the founding insight of digital design.",
            ),
            q(
                "Why did engineers move from drawing schematics to writing HDLs like VHDL and Verilog in the 1980s?",
                (
                    opt("Because schematics could not represent the transistor"),
                    opt("Because chips grew to millions of gates, too many to draw", correct=True),
                    opt("Because Boolean algebra had not been invented yet"),
                    opt("Because simulators could not read schematics at all"),
                ),
                "As chips reached millions of gates, drawing schematics became impractical, so engineers began describing hardware in text with HDLs.",
            ),
        ),
        "Logic gates & Boolean algebra": (
            q(
                "When is the output of an XOR gate equal to 1?",
                (
                    opt("When both inputs are 1"),
                    opt("When the two inputs differ", correct=True),
                    opt("When at least one input is 1"),
                    opt("When the two inputs match"),
                ),
                "XOR outputs 1 exactly when its inputs differ; XNOR outputs 1 when they match.",
            ),
            q(
                "What does De Morgan's theorem state about the complement of an AND?",
                (
                    opt("NOT(A AND B) equals NOT(A) AND NOT(B)"),
                    opt("NOT(A AND B) equals NOT(A) OR NOT(B)", correct=True),
                    opt("NOT(A AND B) equals A OR B"),
                    opt("NOT(A AND B) equals A XOR B"),
                ),
                "De Morgan's theorem turns the complement of an AND into an OR of complements, and the complement of an OR into an AND of complements.",
            ),
            q(
                "Why is silicon full of NAND gates?",
                (
                    opt("NAND is the fastest possible gate to fabricate"),
                    opt(
                        "NAND is universal, so every other gate can be built from NANDs",
                        correct=True,
                    ),
                    opt("NAND uses fewer inputs than any other gate"),
                    opt("NAND is the only gate Boolean algebra can describe"),
                ),
                "NAND (and NOR) are universal: every other gate is an arrangement of them, which is why they dominate real silicon.",
            ),
        ),
        "Combinational logic": (
            q(
                "What defines combinational logic?",
                (
                    opt("Outputs depend only on the current inputs, with no memory", correct=True),
                    opt("Outputs depend on inputs and on stored state"),
                    opt("Outputs change only on a rising clock edge"),
                    opt("Outputs are always driven by a flip-flop"),
                ),
                "Combinational logic has no memory: outputs depend only on the current inputs, with no clock involved.",
            ),
            q(
                "How do you build a sum of products (SOP) expression from a truth table?",
                (
                    opt("AND together one OR term per row where the output is 0"),
                    opt("OR together one AND term per row where the output is 1", correct=True),
                    opt("XOR together every input column"),
                    opt("Take the complement of every input and AND them"),
                ),
                "SOP ORs together one AND (product) term for each row where the output is 1; Karnaugh maps then minimise it.",
            ),
            q(
                "What is the classic beginner bug when describing combinational logic in always_comb?",
                (
                    opt("Using a multiplexer instead of a decoder"),
                    opt(
                        "Leaving an output unassigned in some branch, inferring an unwanted latch",
                        correct=True,
                    ),
                    opt("Using the conditional operator instead of a case statement"),
                    opt("Adding a clock to the sensitivity list"),
                ),
                "A missing assignment in some branch infers an unwanted latch; assign every output in every branch to avoid it.",
            ),
        ),
        "HDL fundamentals: SystemVerilog & VHDL": (
            q(
                "Which pair correctly matches SystemVerilog and VHDL design units?",
                (
                    opt(
                        "SystemVerilog module/endmodule and VHDL entity plus architecture",
                        correct=True,
                    ),
                    opt("SystemVerilog entity and VHDL module"),
                    opt("SystemVerilog architecture and VHDL endmodule"),
                    opt("Both use module/endmodule"),
                ),
                "SystemVerilog uses module ... endmodule, while VHDL splits a design into an entity plus an architecture.",
            ),
            q(
                "Which wire type belongs to which language?",
                (
                    opt("logic is VHDL, std_logic is SystemVerilog"),
                    opt("logic is SystemVerilog (4-state), std_logic is VHDL", correct=True),
                    opt("Both languages use std_logic"),
                    opt("Both languages use logic"),
                ),
                "SystemVerilog's logic is a 4-state type (0, 1, X, Z); VHDL uses std_logic, which has nine values.",
            ),
            q(
                "What does a SystemVerilog parameter correspond to in VHDL?",
                (
                    opt("A signal"),
                    opt("A generic", correct=True),
                    opt("A process"),
                    opt("A std_logic_vector"),
                ),
                "A SystemVerilog parameter is a compile-time constant equivalent to a VHDL generic.",
            ),
        ),
        "Verification with CocoTB": (
            q(
                "In CocoTB terminology, what is the DUT?",
                (
                    opt("The Python coroutine that runs the test"),
                    opt(
                        "The device under test, the HDL module being driven and checked",
                        correct=True,
                    ),
                    opt("The simulator such as Verilator or Icarus"),
                    opt("The clock generator background task"),
                ),
                "The DUT (device under test) is your HDL module; the CocoTB test drives its inputs and checks its outputs.",
            ),
            q(
                "What does the decorator @cocotb.test() do?",
                (
                    opt("It starts a free-running clock on the DUT"),
                    opt("It marks an async coroutine as a test", correct=True),
                    opt("It advances simulated time by one nanosecond"),
                    opt("It compiles the HDL into a netlist"),
                ),
                "@cocotb.test() marks an async coroutine as a CocoTB test; full Python is then available inside it.",
            ),
            q(
                'Why do you call await Timer(1, units="ns") in the mux test?',
                (
                    opt("To start the simulator"),
                    opt("To advance simulated time so combinational outputs settle", correct=True),
                    opt("To reset the DUT to a known state"),
                    opt("To mark the end of the test"),
                ),
                "await Timer advances simulated time so combinational outputs settle before the assert reads dut.y.value.",
            ),
        ),
    },
    final=(
        q(
            "What single decision gives digital circuits their noise immunity?",
            (
                opt("Running the clock as fast as possible"),
                opt(
                    "Reading only two levels, 0 and 1, with a gap between thresholds", correct=True
                ),
                opt("Using only NAND gates throughout"),
                opt("Describing hardware in an HDL"),
            ),
            "Agreeing to read just two levels with a threshold gap means small glitches cannot flip a bit, giving noise immunity.",
        ),
        q(
            "Which statement about gate universality is correct?",
            (
                opt("Only AND and OR together are universal"),
                opt("NAND (and NOR) are universal: any gate can be built from them", correct=True),
                opt("XOR is the only universal gate"),
                opt("No single gate type is ever universal"),
            ),
            "NAND and NOR are each universal; every other gate can be constructed from them, which is why they fill silicon.",
        ),
        q(
            "A truth table output that is 1 in three rows is best turned into gates by which method?",
            (
                opt("A two-flop synchronizer"),
                opt("A sum of products: OR of one AND term per 1 row, then minimise", correct=True),
                opt("A ripple-carry chain"),
                opt("De Morgan applied to the clock"),
            ),
            "Sum of products ORs one AND term per row where the output is 1; tools and Karnaugh maps then minimise the gate count.",
        ),
        q(
            "Which row correctly pairs a SystemVerilog construct with its VHDL counterpart?",
            (
                opt("assign in SystemVerilog corresponds to entity in VHDL"),
                opt(
                    "logic [W-1:0] in SystemVerilog corresponds to std_logic_vector(W-1 downto 0) in VHDL",
                    correct=True,
                ),
                opt("module in SystemVerilog corresponds to signal in VHDL"),
                opt("parameter in SystemVerilog corresponds to architecture in VHDL"),
            ),
            "SystemVerilog logic [W-1:0] matches VHDL std_logic_vector(W-1 downto 0); learn one and the other reads easily.",
        ),
        q(
            "In a CocoTB test, how do you drive a port and read an output of the DUT?",
            (
                opt("dut.port = value to drive and return dut.port to read"),
                opt("dut.port.value = value to drive and dut.port.value to read", correct=True),
                opt("Timer(dut.port) to drive and assert dut.port to read"),
                opt("cocotb.test(dut.port) to drive and dut.read() to read"),
            ),
            "You drive an input with dut.port.value = ... and read an output with dut.port.value, then assert it against the expected value.",
        ),
    ),
)
