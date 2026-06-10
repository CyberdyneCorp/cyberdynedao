from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Flip-flops & sequential logic": (
            q(
                "What distinguishes sequential logic from combinational logic?",
                (
                    opt("Its outputs depend only on the current inputs"),
                    opt("Its outputs depend on inputs and on stored state", correct=True),
                    opt("It never uses a clock signal"),
                    opt("It cannot be described in SystemVerilog or VHDL"),
                ),
                "Sequential logic remembers: outputs depend on inputs and on stored state, with the clock deciding when state updates.",
            ),
            q(
                "When does an edge-triggered D flip-flop copy its input d to output q?",
                (
                    opt("Continuously, whenever d changes"),
                    opt("On each rising clock edge", correct=True),
                    opt("Only while the clock is held high"),
                    opt("Only during an asynchronous reset"),
                ),
                "An edge-triggered D flip-flop captures d into q on each rising clock edge and holds it the rest of the time.",
            ),
            q(
                "Which assignment style belongs in a clocked register block?",
                (
                    opt("Blocking = in always_comb"),
                    opt("Nonblocking <= in always_ff", correct=True),
                    opt("Blocking = in always_ff"),
                    opt("Continuous assign for the register output"),
                ),
                "Use nonblocking <= in clocked SystemVerilog blocks for registers, and blocking = only in always_comb, to avoid sim-vs-synthesis mismatches.",
            ),
        ),
        "Registers, counters & shift registers": (
            q(
                "In a binary counter, how often does each bit toggle relative to the bit below it?",
                (
                    opt("Twice as often"),
                    opt("Half as often", correct=True),
                    opt("At exactly the same rate"),
                    opt("Only on reset"),
                ),
                "In binary counting each bit toggles half as often as the one below it, with bit0 the fastest LSB.",
            ),
            q(
                "What does a shift register do each clock cycle?",
                (
                    opt("Increments its value by one"),
                    opt("Moves bits along one position", correct=True),
                    opt("Holds every bit unchanged forever"),
                    opt("Resolves a metastable state"),
                ),
                "A shift register moves bits along one position per clock, which is the heart of serial links like UART and SPI, delay lines, and LFSRs.",
            ),
            q(
                "Why prefer a synchronous counter over a ripple counter?",
                (
                    opt("Ripple counters are easier to verify with CocoTB"),
                    opt("Ripple counters accumulate delay and cause glitches", correct=True),
                    opt("Synchronous counters need no clock"),
                    opt("Synchronous counters clock each FF from the previous one"),
                ),
                "A synchronous counter has all flip-flops on one clock edge; a ripple counter clocks each FF from the next and accumulates delay and glitches.",
            ),
        ),
        "Finite State Machines": (
            q(
                "In a Moore machine, the outputs depend on what?",
                (
                    opt("State and inputs together"),
                    opt("Only the current state", correct=True),
                    opt("Only the clock frequency"),
                    opt("The setup and hold times"),
                ),
                "Moore outputs depend only on the current state, making them glitch-free but one clock late; Mealy outputs depend on state and inputs.",
            ),
            q(
                "What are the three blocks of the standard three-block FSM idiom?",
                (
                    opt("Clock generator, synchronizer, and reset"),
                    opt("State register, next-state logic, and output logic", correct=True),
                    opt("Setup, hold, and clock-to-Q"),
                    opt("Counter, shift register, and decoder"),
                ),
                "The three-block FSM is a clocked state register, combinational next-state logic, and output logic.",
            ),
            q(
                "Why encode FSM states with an enum or enumerated type rather than raw numbers?",
                (
                    opt("It forces a Mealy implementation"),
                    opt(
                        "The synthesizer picks an efficient encoding and waveforms show readable names",
                        correct=True,
                    ),
                    opt("It removes the need for a state register"),
                    opt("It guarantees glitch-free Mealy outputs"),
                ),
                "Using an enum lets the synthesizer choose an efficient encoding like binary or one-hot, and waveforms display readable state names.",
            ),
        ),
        "Timing, setup/hold & metastability": (
            q(
                "What does setup time require?",
                (
                    opt("Data stable after the clock edge"),
                    opt("Data stable before the clock edge", correct=True),
                    opt("The delay from edge to output changing"),
                    opt("Two flip-flops in series"),
                ),
                "Setup time requires data stable before the edge; hold time requires it stable after the edge; clock-to-Q is the delay from edge to output.",
            ),
            q(
                "Which expression gives the minimum clock period between two registers?",
                (
                    opt("Tclk >= tcq only"),
                    opt("Tclk >= tcq + tlogic + tsu", correct=True),
                    opt("Tclk >= tsu + th"),
                    opt("Tclk >= tlogic - tcq"),
                ),
                "The maximum clock frequency comes from the longest register-to-register path: Tclk >= tcq + tlogic + tsu.",
            ),
            q(
                "What is the standard fix for a single async signal crossing into a clock domain?",
                (
                    opt("A ripple counter on the source clock"),
                    opt("A two-flop synchronizer on the destination clock", correct=True),
                    opt("Removing the reset signal"),
                    opt("Using blocking assignments in always_comb"),
                ),
                "A two-flop synchronizer puts two flip-flops in series on the destination clock so a metastable first stage resolves before the second samples it.",
            ),
        ),
        "CocoTB for sequential logic": (
            q(
                "How do you start a free-running 10 ns clock in CocoTB?",
                (
                    opt("await RisingEdge(dut.clk) in a loop"),
                    opt("cocotb.start_soon(Clock(dut.clk, 10, units=ns).start())", correct=True),
                    opt("dut.clk.value = 1 once at the start"),
                    opt("Timer(10, units=ns) returned from the test"),
                ),
                "cocotb.start_soon with Clock(dut.clk, 10, units=ns).start() runs a free-running clock as a background coroutine.",
            ),
            q(
                "What does await RisingEdge(dut.clk) do in a CocoTB test?",
                (
                    opt("Starts the clock coroutine"),
                    opt("Suspends the test until the next rising edge", correct=True),
                    opt("Resets the DUT synchronously"),
                    opt("Computes the reference model value"),
                ),
                "await RisingEdge(dut.clk) suspends the test until the next rising edge, the natural unit of time for synchronous logic.",
            ),
            q(
                "What is the role of the expected variable in the counter test?",
                (
                    opt("It drives the clock signal"),
                    opt(
                        "It is a Python reference model compared against the DUT each cycle",
                        correct=True,
                    ),
                    opt("It sets the setup and hold times"),
                    opt("It selects between Moore and Mealy outputs"),
                ),
                "The expected variable is a Python reference model; the DUT-vs-model comparison every cycle is the backbone of real verification.",
            ),
        ),
    },
    final=(
        q(
            "Which block and assignment style is correct for a register in SystemVerilog?",
            (
                opt("always_comb with nonblocking <="),
                opt("always_ff with nonblocking <=", correct=True),
                opt("always_ff with blocking ="),
                opt("continuous assign with blocking ="),
            ),
            "Registers use always_ff with nonblocking <=; blocking = belongs only in always_comb.",
        ),
        q(
            "In the VHDL D flip-flop, which construct captures data on the clock edge?",
            (
                opt("a continuous concurrent assignment"),
                opt("elsif rising_edge(clk) inside a process", correct=True),
                opt("an always_ff block"),
                opt("a case statement with no clock"),
            ),
            "In VHDL the clocked process uses elsif rising_edge(clk) then q <= d to capture on the rising edge.",
        ),
        q(
            "Which statement about Moore versus Mealy machines is correct?",
            (
                opt("Mealy outputs depend only on the current state"),
                opt(
                    "Moore outputs depend only on the current state and are glitch-free but one clock late",
                    correct=True,
                ),
                opt("Moore outputs react faster than Mealy outputs"),
                opt("Mealy machines never need a state register"),
            ),
            "Moore outputs depend only on the current state, so they are glitch-free but one clock late; Mealy outputs depend on state and inputs for faster reaction.",
        ),
        q(
            "Why is a synchronizer needed when a signal crosses clock domains?",
            (
                opt("To increase the clock-to-Q delay on purpose"),
                opt(
                    "Because a setup/hold violation can drive the flip-flop metastable",
                    correct=True,
                ),
                opt("To convert a Moore FSM into a Mealy FSM"),
                opt("To make a ripple counter synchronous"),
            ),
            "A cross-domain edge can violate setup/hold and push the flip-flop metastable; a two-flop synchronizer lets it resolve before resampling.",
        ),
        q(
            "Which CocoTB pattern is the backbone of verifying a clocked design?",
            (
                opt("Reading outputs continuously without any clock"),
                opt("Comparing the DUT against a Python reference model every cycle", correct=True),
                opt("Using blocking assignments inside the testbench"),
                opt("Replacing RisingEdge with a single Timer call"),
            ),
            "Driving a clock, awaiting RisingEdge, and comparing the DUT to a Python reference model each cycle is the core DUT-vs-model verification pattern.",
        ),
    ),
)
