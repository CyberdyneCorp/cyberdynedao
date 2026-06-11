from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "EMC & EMI design": (
            q(
                "What are the two halves of EMC?",
                (
                    opt("emissions and immunity", correct=True),
                    opt("voltage and current"),
                    opt("loss and reflection"),
                    opt("DFM and DFT"),
                ),
                "EMC means a product neither emits too much interference nor is too easily disturbed (immunity).",
            ),
            q(
                "According to the lesson, radiated emission rises with what factors?",
                (
                    opt("loop area, current, and the square of frequency", correct=True),
                    opt("trace width and copper weight only"),
                    opt("the inverse of frequency"),
                    opt("dielectric constant alone"),
                ),
                "Emission is proportional to A times I times f squared, over distance r.",
            ),
            q(
                "Why do fast edges, not the clock rate, dominate emissions?",
                (
                    opt(
                        "a fast edge has strong harmonic energy past the knee frequency, and high harmonics radiate hardest",
                        correct=True,
                    ),
                    opt("clocks are always filtered out by decoupling caps"),
                    opt("the clock frequency is too low to radiate"),
                    opt("edges carry no energy above 1 MHz"),
                ),
                "A 1 ns edge has energy past 350 MHz regardless of clock rate, and high harmonics radiate with f squared.",
            ),
        ),
        "Advanced signal integrity: crosstalk, ISI, eye diagrams & S-parameters": (
            q(
                "What causes inter-symbol interference (ISI)?",
                (
                    opt(
                        "frequency-dependent loss spreads a bit edge in time so it bleeds into neighbouring bits",
                        correct=True,
                    ),
                    opt("two boards sharing one ground plane"),
                    opt("too many decoupling capacitors"),
                    opt("a perfectly lossless transmission line"),
                ),
                "Loss rising with frequency attenuates highs more, spreading the edge in time into neighbouring bits.",
            ),
            q(
                "On an eye diagram, what does the vertical gap at the centre represent?",
                (
                    opt("the eye height (voltage margin)", correct=True),
                    opt("the eye width (timing margin)"),
                    opt("the return loss"),
                    opt("the clock period"),
                ),
                "The vertical gap is eye height; the horizontal span at threshold is eye width.",
            ),
            q(
                "Which S-parameter represents insertion loss, ideally near 0 dB?",
                (
                    opt("S21", correct=True),
                    opt("S11"),
                    opt("Sdd21 crosstalk"),
                    opt("S22 only"),
                ),
                "S21 is insertion loss (how much gets through, want near 0 dB); S11 is return loss.",
            ),
        ),
        "Power integrity & PDN analysis": (
            q(
                "How is the target impedance defined?",
                (
                    opt("delta V divided by delta I", correct=True),
                    opt("delta I divided by delta V"),
                    opt("delta V times delta I"),
                    opt("the VRM output current"),
                ),
                "Z_target equals the allowed ripple delta V divided by the transient current step delta I.",
            ),
            q(
                "What is an anti-resonance in a PDN?",
                (
                    opt(
                        "a peak in impedance where two stages overlap that may poke above target",
                        correct=True,
                    ),
                    opt("a dip in impedance that always helps"),
                    opt("the DC resistance of the VRM"),
                    opt("the resonance of a single cap only"),
                ),
                "Where two stages overlap, their L and C can form an impedance peak above target that PI design flattens.",
            ),
            q(
                "Where should the highest-frequency decoupling caps be placed?",
                (
                    opt("closest to the die", correct=True),
                    opt("near the VRM"),
                    opt("at the board edge"),
                    opt("under the antenna"),
                ),
                "On-package and on-die caps cover the highest band; put the high-frequency caps closest to the die.",
            ),
        ),
        "RF & mixed-signal layout": (
            q(
                "What is the recommended grounding approach under RF?",
                (
                    opt("one solid continuous ground plane", correct=True),
                    opt("cut the plane into many islands"),
                    opt("no ground plane at all"),
                    opt("a separate floating ground per trace"),
                ),
                "One solid ground plane gives a continuous return and reference; cutting the plane often makes EMC worse.",
            ),
            q(
                "What system impedance do RF traces typically need to hold?",
                (
                    opt("50 ohm", correct=True),
                    opt("1.5 milliohm"),
                    opt("377 ohm"),
                    opt("0 ohm"),
                ),
                "RF traces are transmission lines that must hold 50 ohm and connect to impedance-matching networks.",
            ),
            q(
                "What does a PCB antenna require around it?",
                (
                    opt("a keep-out with no copper or ground under or near it", correct=True),
                    opt("a dense ground pour directly beneath it"),
                    opt("placement at the board centre"),
                    opt("proximity to the battery"),
                ),
                "A PCB antenna needs a keep-out, board-edge placement, and clearance; stray ground detunes it.",
            ),
        ),
        "Design for manufacturing, test & reliability": (
            q(
                "What are fiducials used for in DFM?",
                (
                    opt("reference marks the assembly camera uses to align", correct=True),
                    opt("test points for in-circuit test"),
                    opt("thermal relief on plane pads"),
                    opt("derating semiconductor parts"),
                ),
                "Fiducials are reference marks the assembly camera uses to align the board.",
            ),
            q(
                "What does boundary scan (JTAG) provide in DFT?",
                (
                    opt(
                        "testing digital interconnects without physical probes",
                        correct=True,
                    ),
                    opt("panelization of many boards"),
                    opt("derating of capacitors"),
                    opt("matching RF antenna impedance"),
                ),
                "Boundary scan (JTAG) tests digital interconnects without physical probes.",
            ),
            q(
                "What does the reliability bathtub curve describe?",
                (
                    opt(
                        "high early failures, a long low-rate useful life, then wear-out",
                        correct=True,
                    ),
                    opt("a constant failure rate forever"),
                    opt("failures that only increase linearly"),
                    opt("a single failure peak at end of life only"),
                ),
                "The bathtub curve has infant mortality, a low-rate useful life, then a wear-out rise.",
            ),
        ),
        "Lab: eye diagram from a lossy channel": (
            q(
                "What kind of channel model does the lab use to add frequency-dependent loss?",
                (
                    opt("a simple one-pole low-pass (RC) filter", correct=True),
                    opt("an ideal lossless transmission line"),
                    opt("a high-pass differentiator"),
                    opt("a band-stop notch filter"),
                ),
                "The lab uses a first-order IIR low-pass (RC) channel to model frequency-dependent loss.",
            ),
            q(
                "In the lab, lowering f3db (less channel bandwidth) causes what?",
                (
                    opt("ISI grows and the eye closes", correct=True),
                    opt("the eye opens wider"),
                    opt("the bit rate decreases"),
                    opt("the return loss improves"),
                ),
                "Lower f3db means less channel bandwidth, so ISI grows and the eye closes.",
            ),
            q(
                "What does the lab overlay to build the eye diagram?",
                (
                    opt("every bit period of the received waveform", correct=True),
                    opt("the transmitter clock harmonics"),
                    opt("the S-parameter magnitudes"),
                    opt("the PDN impedance profile"),
                ),
                "An eye diagram overlays every bit period of the received waveform, folded two UI wide.",
            ),
        ),
        "Applications & a full board bring-up workflow": (
            q(
                "Why feed a new prototype board from a current-limited bench supply first?",
                (
                    opt(
                        "if it slams into the limit you have a short and can power down before anything cooks",
                        correct=True,
                    ),
                    opt("to charge the battery faster"),
                    opt("to increase the clock frequency"),
                    opt("to test the antenna match"),
                ),
                "Current-limited first power reveals a short before damage; you find it before anything cooks.",
            ),
            q(
                "What is the correct early step in a disciplined bring-up sequence?",
                (
                    opt(
                        "inspect for solder bridges, tombstones, wrong parts and reversed polarity",
                        correct=True,
                    ),
                    opt("immediately run the full functional test"),
                    opt("solder a shield can before powering"),
                    opt("program the firmware before checking rails"),
                ),
                "Bring-up starts with visual inspection for bridges, tombstones, wrong parts and reversed polarity.",
            ),
            q(
                "Which PCB challenge dominates a server / GPU board?",
                (
                    opt(
                        "multi-gigabit SerDes with equalization, milliohm PDN, dense BGA escape routing",
                        correct=True,
                    ),
                    opt("integrated antenna and ultra-low-power layout"),
                    opt("creepage and clearance for a switching supply"),
                    opt("a tiny 2/4-layer cost-driven board"),
                ),
                "Server/GPU boards face 12+ layers, multi-gigabit SerDes with equalization, milliohm PDN and dense BGA escape.",
            ),
        ),
    },
    final=(
        q(
            "What is the single most powerful EMC fix at layout time?",
            (
                opt("shrink loop areas with tight return paths", correct=True),
                opt("add more layers to the stackup"),
                opt("raise every clock frequency"),
                opt("remove the ground plane"),
            ),
            "Radiated emission rises with loop area, so shrinking loop areas (return-path discipline) is the most powerful fix.",
        ),
        q(
            "At high speed, what reopens an eye closed by channel loss?",
            (
                opt("equalization: transmitter pre-emphasis and receiver CTLE/DFE", correct=True),
                opt("more decoupling capacitors near the die"),
                opt("a larger antenna keep-out"),
                opt("lowering the supply ripple target"),
            ),
            "Equalization boosts the attenuated high frequencies to reopen the eye at high data rates.",
        ),
        q(
            "A core allowing 30 mV ripple on a 20 A step needs a target impedance near what value?",
            (
                opt("1.5 milliohm", correct=True),
                opt("50 ohm"),
                opt("1.5 ohm"),
                opt("20 milliohm"),
            ),
            "Z_target = delta V / delta I = 0.030 / 20 = 0.0015 ohm = 1.5 milliohm.",
        ),
        q(
            "For an RF antenna and matching network, what does the lesson recommend doing first?",
            (
                opt("copy the chip vendor's reference layout, then optimise", correct=True),
                opt("cut the ground plane under the antenna"),
                opt("place the antenna at the board centre"),
                opt("skip the VNA measurement and guess"),
            ),
            "RF physics is unforgiving: copy the vendor reference layout first, and a measured VNA sweep beats any guess.",
        ),
        q(
            "When are DFM, DFT and DFR cheapest to address?",
            (
                opt("at design time, before the first build", correct=True),
                opt("after a failed CISPR test"),
                opt("only during volume production"),
                opt("after the first respin"),
            ),
            "DFM/DFT/DFR are cheapest at design time and ruinous later; add test points, fiducials and derating up front.",
        ),
    ),
)
