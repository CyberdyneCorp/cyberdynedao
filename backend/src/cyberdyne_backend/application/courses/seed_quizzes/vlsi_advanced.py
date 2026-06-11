from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Low-power design: DVFS, clock gating, multi-Vt & power domains": (
            q(
                "Why does running a task slower at a lower voltage save power so dramatically under DVFS?",
                (
                    opt("Leakage power drops to zero at lower frequency"),
                    opt(
                        "Dynamic power scales as roughly C times V squared times f, and a lower voltage also forces a lower f, so savings stack",
                        correct=True,
                    ),
                    opt("Clock gating is automatically disabled at low voltage"),
                    opt("The number of transistors that switch decreases"),
                ),
                "P_dyn ~ alpha C V^2 f and lower voltage forces lower f, so power falls faster than linearly.",
            ),
            q(
                "What does clock gating do to save dynamic power?",
                (
                    opt("Lowers the supply voltage of idle registers"),
                    opt("Swaps in high-Vt cells off the critical path"),
                    opt(
                        "Shuts off the clock to idle registers so they stop switching",
                        correct=True,
                    ),
                    opt("Powers down an entire domain with sleep transistors"),
                ),
                "Clock gating shuts off the clock to idle registers, eliminating their switching power.",
            ),
            q(
                "When crossing from a powered-down domain to a live block, what prevents a floating output from corrupting the live block?",
                (
                    opt("Level shifters"),
                    opt("Sleep transistors"),
                    opt("Isolation cells", correct=True),
                    opt("Clock-gating cells"),
                ),
                "Isolation cells clamp a powered-down output so it does not float into a live block; level shifters handle voltage changes.",
            ),
        ),
        "Clocking & clock distribution: trees, skew, jitter & PLLs": (
            q(
                "How is the clock delivered to millions of flip-flops at nearly the same instant?",
                (
                    opt("From a single large buffer driving all loads directly"),
                    opt(
                        "Through a balanced tree (or H-tree, or mesh) of buffers sized so every leaf sees a similar delay",
                        correct=True,
                    ),
                    opt("By a separate PLL placed next to each flip-flop"),
                    opt("Through the data routing using isolation cells"),
                ),
                "A balanced clock tree of buffers distributes the clock so every leaf flop sees a similar delay and edge rate.",
            ),
            q(
                "How does clock skew differ from jitter?",
                (
                    opt("Skew is random per cycle while jitter is a fixed spatial offset"),
                    opt(
                        "Skew is a fixed spatial offset between flops while jitter is random cycle-to-cycle wobble",
                        correct=True,
                    ),
                    opt("Both are identical and only matter for hold timing"),
                    opt("Skew comes from the PLL while jitter comes from the clock tree shape"),
                ),
                "Skew is a fixed spatial arrival-time offset; jitter is random cycle-to-cycle wobble. Together they form clock uncertainty.",
            ),
            q(
                "What is the role of a PLL on a chip?",
                (
                    opt("It synchronizes asynchronous data with a 2-flop chain"),
                    opt("It gates the clock to idle registers"),
                    opt(
                        "It multiplies a clean low-frequency crystal reference up to the GHz on-chip clock and locks its phase",
                        correct=True,
                    ),
                    opt("It measures wire parasitics after routing"),
                ),
                "A phase-locked loop multiplies a clean reference up to the on-chip GHz clock and locks phase via a feedback loop.",
            ),
        ),
        "Physical design & signoff": (
            q(
                "What does static timing analysis (STA) do?",
                (
                    opt("Simulates functional test vectors to find logic bugs"),
                    opt(
                        "Checks every path's timing without simulating vectors, propagating worst-case delays across corners",
                        correct=True,
                    ),
                    opt("Generates scan patterns to detect stuck-at faults"),
                    opt("Places the big blocks and lays down the power grid"),
                ),
                "STA checks every path's setup and hold without vectors, across PVT corners, reporting slack.",
            ),
            q(
                "In STA, what does negative slack indicate?",
                (
                    opt("Extra timing margin on the path"),
                    opt("A timing violation", correct=True),
                    opt("That parasitic extraction has not run yet"),
                    opt("A successful tape-out to GDSII"),
                ),
                "Slack = required time minus arrival time; negative slack is a timing violation.",
            ),
            q(
                "Why is parasitic extraction run after routing before re-running STA?",
                (
                    opt("To balance the clock tree and minimize skew"),
                    opt("To select high-Vt cells off the critical path"),
                    opt(
                        "To measure the actual R and C of every wire so STA uses real interconnect delays",
                        correct=True,
                    ),
                    opt("To generate the UPF power-intent file"),
                ),
                "Extraction captures the real wire R and C into a SPEF; re-running STA with it catches post-route timing surprises.",
            ),
        ),
        "Design for test: scan, BIST, ATPG & fault coverage": (
            q(
                "What is the most common fault model used in DFT?",
                (
                    opt("The crosstalk fault"),
                    opt("The stuck-at fault, a node permanently stuck at 0 or 1", correct=True),
                    opt("The electromigration fault"),
                    opt("The metastability fault"),
                ),
                "DFT abstracts physical defects into the stuck-at fault model: a node stuck at 0 or 1.",
            ),
            q(
                "How do scan chains make internal flip-flops testable?",
                (
                    opt("They add a PLL to each flop to control its clock"),
                    opt("They lower the supply voltage so flops can be probed directly"),
                    opt(
                        "In test mode they chain flops into one giant shift register so a known state can be shifted in and the result shifted out",
                        correct=True,
                    ),
                    opt("They isolate each flop into its own power domain"),
                ),
                "Scan flops chain into a shift register in test mode: shift in a state, pulse the clock, shift out and compare.",
            ),
            q(
                "What does ATPG produce?",
                (
                    opt("The on-chip LFSR pattern generator for BIST"),
                    opt(
                        "The minimal set of scan patterns that detects the modeled faults",
                        correct=True,
                    ),
                    opt("The signature compressed from test responses"),
                    opt("The power grid for the floorplan"),
                ),
                "Automatic Test Pattern Generation computes a minimal set of scan patterns that detects the faults.",
            ),
        ),
        "Analog/mixed-signal & advanced nodes: FinFET, SoC, chiplets & 3D-IC": (
            q(
                "What advantage does a FinFET have over a planar MOSFET?",
                (
                    opt("It eliminates the need for a power grid"),
                    opt(
                        "Wrapping the gate around a thin fin on three sides gives better electrostatic control, less leakage, and higher speed",
                        correct=True,
                    ),
                    opt("It removes the need for clock-tree synthesis"),
                    opt("It makes analog blocks shrink as easily as digital"),
                ),
                "The FinFET wraps the gate around a vertical fin on three sides for better control, less leakage, lower voltage, higher speed.",
            ),
            q(
                "Why do chiplets yield better than one huge monolithic die?",
                (
                    opt("They run at a lower clock frequency"),
                    opt("They share a single power domain"),
                    opt(
                        "Smaller dies have fewer defects each, and they can mix and match best-suited process nodes",
                        correct=True,
                    ),
                    opt("They avoid the need for static timing analysis"),
                ),
                "Smaller dies have fewer defects, improving yield, and chiplets let each die use its best-suited node.",
            ),
            q(
                "What does 3D-IC use to stack dies vertically for high bandwidth at low energy?",
                (
                    opt("Through-silicon vias (TSVs)", correct=True),
                    opt("Level shifters"),
                    opt("Scan chains"),
                    opt("An AXI/NoC fabric"),
                ),
                "3D-IC stacks dies vertically with through-silicon vias; HBM on AI accelerators is the headline example.",
            ),
        ),
        "Lab: technology scaling of delay & power": (
            q(
                "Under ideal Dennard (constant-field) scaling, what happens to power density per area?",
                (
                    opt("It rises by a factor of s squared"),
                    opt("It stays roughly constant", correct=True),
                    opt("It falls as 1 over s squared"),
                    opt("It rises linearly with s"),
                ),
                "Per-device power scales as 1/s^2 and devices per area scale as s^2, so power density stays flat: the Dennard gift.",
            ),
            q(
                "In the modern (post-Dennard) model used in the lab, why does power density rise as s grows?",
                (
                    opt("Capacitance stops scaling with the node"),
                    opt("Frequency falls instead of rising"),
                    opt(
                        "Voltage barely scales (it is stuck near a floor), so per-device power no longer drops as 1 over s squared",
                        correct=True,
                    ),
                    opt("The number of devices per area decreases"),
                ),
                "In the modern model voltage scales much more slowly, so power density rises with s: the power wall.",
            ),
            q(
                "Under Dennard scaling in the lab, how do gate delay and frequency change with the scaling factor s?",
                (
                    opt("Delay rises as s and frequency falls as 1 over s"),
                    opt("Both delay and frequency rise as s"),
                    opt(
                        "Delay scales as roughly 1 over s and frequency as roughly s", correct=True
                    ),
                    opt("Both stay constant regardless of s"),
                ),
                "Shrinking dimensions makes gate delay ~ 1/s while frequency ~ s; devices get faster as they shrink.",
            ),
        ),
        "Applications & the VLSI throughline": (
            q(
                "Which low-power techniques does a smartphone SoC combine for battery life, per the lesson?",
                (
                    opt("Only clock gating"),
                    opt(
                        "DVFS, clock gating, power gating, and multi-Vt together",
                        correct=True,
                    ),
                    opt("Only high-Vt cells everywhere"),
                    opt("Only DVFS with a fixed voltage"),
                ),
                "A smartphone SoC uses aggressive DVFS plus clock gating plus power gating plus multi-Vt on an advanced node.",
            ),
            q(
                "What does the energy-delay tradeoff curve say a newer process node buys you?",
                (
                    opt("Lower energy only, at the cost of higher delay"),
                    opt("Lower delay only, at the cost of higher energy"),
                    opt(
                        "It pushes the whole curve toward both lower energy and lower delay",
                        correct=True,
                    ),
                    opt("Constant energy and delay but more transistors"),
                ),
                "A newer node shifts the energy-delay frontier toward both lower energy and lower delay at once.",
            ),
            q(
                "How are AI accelerators (TPUs/NPUs) described as embodying the track's lessons?",
                (
                    opt("As pure array-and-sense-amplifier memory pushed to density limits"),
                    opt("As reconfigurable seas of LUTs and DSP blocks"),
                    opt(
                        "As arrays of multipliers doing matrix multiply, fed by HBM stacked in 3D for bandwidth",
                        correct=True,
                    ),
                    opt("As mixed-signal chips dominated by ADC/DAC front-ends"),
                ),
                "AI accelerators are arrays of multipliers fed by 3D-stacked HBM: the datapath and 3D-IC lessons made into a product.",
            ),
        ),
    },
    final=(
        q(
            "Which of the following best states why DVFS saves power so effectively?",
            (
                opt("It reduces the number of power domains on the chip"),
                opt(
                    "Dynamic power follows C times V squared times f, and lowering voltage also forces lower frequency, compounding the savings",
                    correct=True,
                ),
                opt("It eliminates all leakage by inserting isolation cells"),
                opt("It increases the threshold voltage of every cell"),
            ),
            "P_dyn ~ alpha C V^2 f; lowering V also lowers f, so DVFS savings compound.",
        ),
        q(
            "Why does STA rather than simulation sign off chip timing?",
            (
                opt("It is the only tool that can run functional test vectors"),
                opt(
                    "It exhaustively checks every path's setup and hold across corners without vectors, and is fast",
                    correct=True,
                ),
                opt("It generates the scan patterns needed for tape-out"),
                opt("It measures wire parasitics directly during routing"),
            ),
            "STA is exhaustive and fast, checking all paths across PVT corners without simulating vectors.",
        ),
        q(
            "What is the purpose of scan chains and ATPG together in DFT?",
            (
                opt("To balance the clock tree and minimize skew"),
                opt("To stack dies vertically using through-silicon vias"),
                opt(
                    "Scan makes internal flops controllable/observable as a shift register, and ATPG computes the minimal patterns to detect faults",
                    correct=True,
                ),
                opt("To scale voltage and frequency per workload"),
            ),
            "Scan chains expose internal flops as a shift register; ATPG generates the minimal pattern set to detect modeled faults.",
        ),
        q(
            "Which statement about advanced packaging and nodes is correct?",
            (
                opt("FinFETs increase leakage compared with planar MOSFETs"),
                opt("3D-IC connects separate packages over a board-level bus"),
                opt(
                    "Chiplets improve yield because smaller dies have fewer defects and can mix and match best-suited nodes",
                    correct=True,
                ),
                opt("An SoC always uses a single IP block with no on-chip bus"),
            ),
            "Chiplets split a design into smaller dies with fewer defects each, mixing nodes; this is the More-than-Moore frontier.",
        ),
        q(
            "What is the technology-scaling throughline captured by the lab and the closing lesson?",
            (
                opt("Voltage scaling continued indefinitely, keeping power density flat"),
                opt(
                    "Devices got faster as they shrank, but voltage stopped scaling, so power density rose and pushed designs to multi-core",
                    correct=True,
                ),
                opt("Frequency fell with each node, forcing lower clock speeds"),
                opt("Leakage became irrelevant on advanced nodes"),
            ),
            "Dennard scaling kept density flat, but modern voltage barely scales, so power density rises (the power wall), driving multi-core.",
        ),
    ),
)
