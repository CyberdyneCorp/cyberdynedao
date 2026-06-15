"""Quiz spec for the SystemVerilog for Digital Design -- Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "RTL and the synthesis mindset": (
            q(
                "What does a synthesis tool turn your SystemVerilog RTL into?",
                (
                    opt("A sequential program executed by a CPU"),
                    opt("A netlist of gates and flip-flops", correct=True),
                    opt("A Python script"),
                    opt("A block of documentation"),
                ),
                "Synthesis maps RTL to a gate-level netlist that is then placed and "
                "routed into an ASIC or FPGA.",
            ),
            q(
                "Outside a procedural block, how do multiple assign statements relate?",
                (
                    opt("They run top to bottom like software"),
                    opt("They all describe concurrent hardware that exists at once", correct=True),
                    opt("Only the last one takes effect"),
                    opt("They run once at startup then stop"),
                ),
                "RTL describes hardware: statements are concurrent, so textual order "
                "does not matter the way it does in software.",
            ),
        ),
        "Combinational logic: assign and always_comb": (
            q(
                "In an always_comb block, what happens if an output is not assigned on every path?",
                (
                    opt("The tool sets it to zero"),
                    opt("It infers an unintended latch (memory)", correct=True),
                    opt("It is a syntax error"),
                    opt("It becomes a flip-flop"),
                ),
                "An unassigned path means the output must hold its value, so the tool "
                "infers a latch -- usually a bug. Assign a default on every path.",
            ),
            q(
                "Why does a ripple-carry adder get slower as it gets wider?",
                (
                    opt("It uses more memory"),
                    opt("The carry must propagate through every bit in series", correct=True),
                    opt("Wider numbers need more clock cycles"),
                    opt("The clock frequency drops automatically"),
                ),
                "The carry chain is serial, so combinational delay grows linearly with "
                "width; carry-lookahead trades area to make it grow logarithmically.",
            ),
        ),
        "Bits, vectors, and number formats": (
            q(
                "An 8-bit signal holds 8'hFF. What is it as a two's-complement number?",
                (
                    opt("255"),
                    opt("-1", correct=True),
                    opt("-128"),
                    opt("127"),
                ),
                "All ones is 255 unsigned but -1 in two's complement; the top bit "
                "subtracts a full 2^N.",
            ),
            q(
                "How do you sign-extend an 8-bit signed value s to 16 bits?",
                (
                    opt("Pad with eight zeros on the left"),
                    opt("Replicate the sign bit: {{8{s[7]}}, s}", correct=True),
                    opt("Replicate the low bit on the right"),
                    opt("Cast it to unsigned first"),
                ),
                "Sign extension replicates the most-significant (sign) bit so the value "
                "is preserved in the wider signed representation.",
            ),
        ),
        "Sequential logic: always_ff and flip-flops": (
            q(
                "Which assignment operator belongs in an always_ff block?",
                (
                    opt("Blocking '='"),
                    opt("Non-blocking '<='", correct=True),
                    opt("Either works identically"),
                    opt("The continuous 'assign'"),
                ),
                "Flip-flops sample inputs then update together, which non-blocking '<=' "
                "models; '=' belongs in always_comb.",
            ),
            q(
                "What appears in a flip-flop's sensitivity list @(posedge clk or negedge rst_n)?",
                (
                    opt("Every data input the block reads"),
                    opt("Only the clock and (asynchronous) reset", correct=True),
                    opt("Nothing -- it is empty"),
                    opt("The outputs only"),
                ),
                "A flop only reacts to its clock edge (and async reset); data is captured "
                "at the edge, so it is not in the list.",
            ),
        ),
    },
    final=(
        q(
            "Which keyword pair best expresses combinational vs sequential intent?",
            (
                opt("always @* and always @(posedge clk)"),
                opt("always_comb and always_ff", correct=True),
                opt("assign and reg"),
                opt("wire and logic"),
            ),
            "always_comb and always_ff state intent so the tool can verify you built "
            "combinational vs clocked logic as you meant.",
        ),
        q(
            "What is the carry-out captured by 'assign {cout, sum} = a + b + cin;'?",
            (
                opt("The least-significant bit of the sum"),
                opt("The extra high bit of the full-width addition", correct=True),
                opt("Always zero"),
                opt("The sign of the result"),
            ),
            "Concatenating cout above sum captures the (W+1)-th bit of the sum, which is "
            "the carry-out.",
        ),
        q(
            "A 3-bit counter with enable held high counts which sequence?",
            (
                opt("0,1,2,3,4,5,6,7,0,1,... (wraps at 8)", correct=True),
                opt("0,1,2,...,7 then stops"),
                opt("0,2,4,6,0,..."),
                opt("It counts down"),
            ),
            "A W-bit counter counts 0..2^W-1 then wraps; for W=3 that is modulo 8.",
        ),
        q(
            "Why prefer 'logic' over Verilog's 'reg' and 'wire'?",
            (
                opt("It is faster in hardware"),
                opt("It is a single 4-state type the tool checks against your intent blocks", correct=True),
                opt("It uses less memory"),
                opt("It is required for ROMs only"),
            ),
            "'logic' unifies reg/wire; combined with always_comb/always_ff the tool "
            "checks you drove it the way you intended.",
        ),
    ),
)
