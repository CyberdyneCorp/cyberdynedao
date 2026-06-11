from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What VLSI is and the CMOS inverter": (
            q(
                "In a static CMOS inverter, what is the output when the input is logic 0?",
                (
                    opt("logic 0, because the NMOS pulls it down"),
                    opt("logic 1, because the PMOS is on and pulls it to VDD", correct=True),
                    opt("high impedance, because both transistors are off"),
                    opt("a short between VDD and ground"),
                ),
                "Input 0 turns the PMOS on and the NMOS off, so the output is pulled to VDD (1).",
            ),
            q(
                "Why does a static CMOS gate draw almost no static current in steady state?",
                (
                    opt("the NMOS is always slightly leaking"),
                    opt("both networks conduct equally and cancel out"),
                    opt(
                        "exactly one of the pull-up or pull-down networks conducts, so no direct VDD-to-ground path exists",
                        correct=True,
                    ),
                    opt("the gate capacitance blocks all DC current"),
                ),
                "In steady state only one network conducts, leaving no direct path from VDD to ground.",
            ),
            q(
                "On the voltage transfer characteristic (VTC), what does the steep middle region represent?",
                (
                    opt("the gain region near the switching threshold Vm", correct=True),
                    opt("the flat-high output region"),
                    opt("the leakage current region"),
                    opt("the region where the input equals VDD"),
                ),
                "The VTC is flat-high, then drops sharply near Vm; that steep middle is the gain region.",
            ),
        ),
        "Combinational CMOS logic": (
            q(
                "How is a 2-input NAND gate built in static CMOS?",
                (
                    opt("two NMOS in parallel and two PMOS in series"),
                    opt("two NMOS in series and two PMOS in parallel", correct=True),
                    opt("one NMOS and one PMOS only"),
                    opt("two PMOS in series feeding two NMOS in series"),
                ),
                "NAND uses series NMOS (low only when both inputs are high) and parallel PMOS.",
            ),
            q(
                "Why must a PMOS transistor generally be made wider than an NMOS?",
                (
                    opt("PMOS transistors have a higher threshold voltage"),
                    opt(
                        "holes are less mobile than electrons, so PMOS sources less current for the same width",
                        correct=True,
                    ),
                    opt("PMOS transistors leak more at low voltage"),
                    opt("wider PMOS reduces the gate capacitance"),
                ),
                "Electrons in NMOS are 2-3x more mobile than holes in PMOS, so PMOS is widened to match current.",
            ),
            q(
                "What kind of gates are the natural building blocks in static CMOS?",
                (
                    opt("AND and OR gates"),
                    opt("inverting gates such as NAND, NOR, and INV", correct=True),
                    opt("XOR and XNOR gates"),
                    opt("transmission gates only"),
                ),
                "Static CMOS gates are always inverting, so designers build from NAND, NOR, and INV.",
            ),
        ),
        "Sequential CMOS: latches, flip-flops & clocking": (
            q(
                "What is the key difference between a latch and a flip-flop?",
                (
                    opt(
                        "a latch is level-sensitive while a flip-flop is edge-triggered",
                        correct=True,
                    ),
                    opt("a latch is edge-triggered while a flip-flop is level-sensitive"),
                    opt("a latch has no clock while a flip-flop does"),
                    opt("a latch stores two bits while a flip-flop stores one"),
                ),
                "A latch is transparent while the enable is high (level-sensitive); a flip-flop samples on the clock edge.",
            ),
            q(
                "A master-slave D flip-flop is built from which components?",
                (
                    opt("two cross-coupled inverters"),
                    opt("two opposite-phase latches in series", correct=True),
                    opt("a single level-sensitive latch"),
                    opt("two flip-flops in parallel"),
                ),
                "A master-slave D flip-flop chains two opposite-phase latches in series.",
            ),
            q(
                "The minimum clock period satisfies T >= tcq + tlogic + tsetup. What does this constrain?",
                (
                    opt("the leakage power of the flip-flops"),
                    opt("the maximum clock frequency f = 1/T", correct=True),
                    opt("the area of the combinational logic"),
                    opt("the threshold voltage of the transistors"),
                ),
                "The clock period must be long enough for the signal to propagate; this sets the max frequency f = 1/T.",
            ),
        ),
        "The IC design flow: spec to GDSII": (
            q(
                "What does logic synthesis produce from RTL?",
                (
                    opt("a GDSII layout file"),
                    opt("a gate-level netlist of standard cells", correct=True),
                    opt("a floorplan with placed cells"),
                    opt("a set of photolithography masks"),
                ),
                "Logic synthesis maps RTL to a gate-level netlist of standard cells, optimizing timing/area/power.",
            ),
            q(
                "What is GDSII in the IC design flow?",
                (
                    opt("the behavioral RTL description"),
                    opt("the final layout file sent to the foundry to make masks", correct=True),
                    opt("the static timing analysis report"),
                    opt("the standard-cell library catalog"),
                ),
                "GDSII is the final layout file sent to the foundry to make the masks.",
            ),
            q(
                "Which statement best contrasts an ASIC with an FPGA?",
                (
                    opt(
                        "an ASIC is custom silicon with huge NRE and tiny unit cost; an FPGA is reconfigurable with no NRE but higher unit cost",
                        correct=True,
                    ),
                    opt("an FPGA is custom silicon fixed at fab; an ASIC is reconfigurable"),
                    opt("both have identical NRE and unit costs"),
                    opt("an ASIC can be reprogrammed in minutes; an FPGA cannot"),
                ),
                "ASICs have huge NRE but cheap parts; FPGAs are reconfigurable with no NRE but pricier parts.",
            ),
        ),
        "Layout & design rules": (
            q(
                "What does DRC (Design Rule Check) verify?",
                (
                    opt(
                        "that the layout geometry obeys the foundry rules and is manufacturable",
                        correct=True,
                    ),
                    opt("that the extracted netlist matches the schematic"),
                    opt("that the timing meets the clock constraint"),
                    opt("that the power grid delivers enough current"),
                ),
                "DRC checks minimum widths, spacings, and enclosures so the geometry is manufacturable.",
            ),
            q(
                "What does LVS (Layout Versus Schematic) confirm?",
                (
                    opt("that the geometry meets minimum spacing rules"),
                    opt(
                        "that the netlist extracted from the layout matches the intended schematic",
                        correct=True,
                    ),
                    opt("that the layout passes static timing analysis"),
                    opt("that the feature size scales with lambda"),
                ),
                "LVS extracts a netlist from the drawn layout and checks it matches the intended schematic.",
            ),
            q(
                "If the feature size is tightened by a factor k, how does the area of a fixed-function block scale?",
                (
                    opt("roughly as 1/k^2", correct=True),
                    opt("roughly as k^2"),
                    opt("linearly as 1/k"),
                    opt("it stays constant"),
                ),
                "Area scales roughly as 1/k^2 when feature size shrinks by k - the engine of Moore's Law.",
            ),
        ),
        "Lab: CMOS inverter VTC & noise margins": (
            q(
                "In the lab, how are the unity-gain points VIL and VIH found?",
                (
                    opt("where the VTC output equals VDD"),
                    opt("where the slope (gain) of the VTC has magnitude at least 1", correct=True),
                    opt("where the input equals zero"),
                    opt("where the leakage current is maximum"),
                ),
                "The lab takes the gradient of the VTC and uses points where the gain magnitude is at least 1 as VIL and VIH.",
            ),
            q(
                "How does the lab define the switching threshold Vm?",
                (
                    opt("the input where Vout equals Vin", correct=True),
                    opt("the input where Vout equals VDD"),
                    opt("the maximum of the VTC"),
                    opt("the average of VIL and VIH"),
                ),
                "Vm is taken at the input where the VTC output equals the input (Vout == Vin).",
            ),
            q(
                "According to the lab notes, what happens to noise margins if VDD is lowered to 1.2 V?",
                (
                    opt("they grow larger"),
                    opt("they shrink, which is why low voltage is hard", correct=True),
                    opt("they stay exactly the same"),
                    opt("they become negative"),
                ),
                "The lab notes that lowering VDD to 1.2 shrinks the noise margins, showing why low voltage is hard.",
            ),
        ),
    },
    final=(
        q(
            "Which property of static CMOS is responsible for its very low static power?",
            (
                opt(
                    "only one of the pull-up or pull-down networks conducts at a time", correct=True
                ),
                opt("the PMOS is always wider than the NMOS"),
                opt("the gate is built from level-sensitive latches"),
                opt("the output is always high impedance"),
            ),
            "Because exactly one network conducts in steady state, there is no DC path from VDD to ground.",
        ),
        q(
            "In static CMOS, why do designers build logic from NAND, NOR, and INV rather than AND and OR?",
            (
                opt("AND and OR cannot be synthesized"),
                opt(
                    "static CMOS gates are inherently inverting, so AND/OR cost an extra inverter",
                    correct=True,
                ),
                opt("NAND and NOR use fewer metal layers"),
                opt("AND and OR have no noise margins"),
            ),
            "Static CMOS gates are naturally inverting; AND/OR require an extra inverter, so NAND/NOR/INV are the natural cells.",
        ),
        q(
            "Which sequencing element samples its input only at a clock edge?",
            (
                opt("a level-sensitive latch"),
                opt("an edge-triggered flip-flop", correct=True),
                opt("a pull-down network"),
                opt("a sense amplifier"),
            ),
            "A flip-flop is edge-triggered, sampling only at the clock edge; a latch is level-sensitive.",
        ),
        q(
            "Put the design-flow stages in order from RTL toward fabrication.",
            (
                opt("RTL -> logic synthesis -> place and route -> signoff -> GDSII", correct=True),
                opt("RTL -> GDSII -> place and route -> synthesis -> signoff"),
                opt("logic synthesis -> RTL -> signoff -> GDSII -> place and route"),
                opt("place and route -> RTL -> synthesis -> GDSII -> signoff"),
            ),
            "RTL is synthesized to a netlist, then placed and routed, signed off, and emitted as GDSII to the foundry.",
        ),
        q(
            "Which pair of checks must both pass before a layout is done?",
            (
                opt(
                    "DRC (manufacturable geometry) and LVS (layout matches schematic)", correct=True
                ),
                opt("setup time and hold time"),
                opt("NMOS mobility and PMOS mobility"),
                opt("dynamic power and leakage power"),
            ),
            "A layout is not done until DRC (rules obeyed) and LVS (matches the intended netlist) both pass.",
        ),
    ),
)
