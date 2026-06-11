from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Power distribution & decoupling": (
            q(
                "What is the primary job of the power distribution network (PDN)?",
                (
                    opt("To filter analog audio noise out of the ground plane"),
                    opt(
                        "To deliver the chip's current bursts with the supply voltage barely moving",
                        correct=True,
                    ),
                    opt("To convert AC mains into a regulated DC rail"),
                    opt("To match trace impedance to 50 ohm"),
                ),
                "The PDN must supply the bursty switching current while keeping the rail voltage steady.",
            ),
            q(
                "Why can a decoupling capacitor right at the chip pin help when the regulator cannot?",
                (
                    opt(
                        "The regulator is too slow and too far to respond on a nanosecond timescale",
                        correct=True,
                    ),
                    opt("The capacitor increases the loop inductance to the regulator"),
                    opt("The capacitor steps the voltage up to a higher rail"),
                    opt("The regulator only works above gigahertz frequencies"),
                ),
                "A local cap dumps charge in nanoseconds to cover the burst before the slow regulator refills it.",
            ),
            q(
                "Why do boards use many capacitor values in parallel (e.g. 100 nF, 1 uF, 10 uF)?",
                (
                    opt("To increase the total ESR of the PDN"),
                    opt("Because identical caps would short the rail to ground"),
                    opt(
                        "Each value has a self-resonant band, so together they hold Z below target across frequency",
                        correct=True,
                    ),
                    opt("To raise the target impedance Z_target"),
                ),
                "Each cap is a series RLC that only helps in a band, so a mix keeps the impedance low from kHz to hundreds of MHz.",
            ),
        ),
        "Grounding & return paths": (
            q(
                "At high frequency, which path does the return current take?",
                (
                    opt("The lowest-resistance path, spreading widely across the plane"),
                    opt(
                        "The lowest-inductance path, directly beneath the signal trace",
                        correct=True,
                    ),
                    opt("The path through the nearest decoupling capacitor"),
                    opt("A random path determined by the dielectric"),
                ),
                "High-frequency return current minimises loop area by flowing in the plane right under the trace.",
            ),
            q(
                "What happens when a gap or split breaks the plane under a high-speed signal?",
                (
                    opt(
                        "The return current detours around the gap, enlarging loop area and inductance",
                        correct=True,
                    ),
                    opt("The signal speeds up because it has less copper to cross"),
                    opt("Nothing, because return current ignores plane gaps"),
                    opt("The characteristic impedance automatically drops to zero"),
                ),
                "Forced to detour, the return current enlarges the loop, adding inductance and EMI plus a voltage across the gap.",
            ),
            q(
                "Which grounding approach does the lesson recommend for high-frequency circuits?",
                (
                    opt("A single-point star ground"),
                    opt("Two separate ground connections at different potentials"),
                    opt("A solid reference plane", correct=True),
                    opt("Routing signals across a plane split"),
                ),
                "A solid plane is preferred for high frequency; single-point star ground suits low-frequency/analog.",
            ),
        ),
        "Signal integrity intro: transmission lines & reflections": (
            q(
                "By the rule of thumb, when should a trace be treated as a transmission line?",
                (
                    opt(
                        "When its length exceeds about one tenth of the edge's rise distance",
                        correct=True,
                    ),
                    opt("Only when the clock frequency exceeds 1 GHz"),
                    opt("When it is shorter than 1 mm"),
                    opt("Whenever it crosses a ground plane gap"),
                ),
                "The rule is roughly one tenth of the edge rise distance; on FR4 a 1 ns edge means traces over ~15 mm matter.",
            ),
            q(
                "For a load Z_L equal to Z_0 (matched), what is the reflection coefficient?",
                (
                    opt("+1, a full reflection"),
                    opt("-1, an inverted reflection"),
                    opt("0, no reflection", correct=True),
                    opt("Infinite"),
                ),
                "Gamma = (Z_L - Z_0)/(Z_L + Z_0), so a matched load gives Gamma = 0 and a clean signal.",
            ),
            q(
                "Which termination places a resistor at the driver so R_s plus Z_driver equals Z_0?",
                (
                    opt("Parallel termination"),
                    opt("Series termination", correct=True),
                    opt("Thevenin termination to two rails"),
                    opt("AC termination with a capacitor"),
                ),
                "Series termination puts a resistor at the driver for point-to-point links; parallel termination sits at the receiver.",
            ),
        ),
        "High-speed routing: length matching, differential pairs & crosstalk": (
            q(
                "How is a length mismatch on a parallel bus converted into a timing problem?",
                (
                    opt("It becomes skew, since signals travel at about 6 ps/mm", correct=True),
                    opt("It raises the differential impedance above 100 ohm"),
                    opt("It shorts the two traces together"),
                    opt("It has no timing effect on a parallel bus"),
                ),
                "t_skew = delta length / v, and at ~6 ps/mm a 10 mm mismatch is about 67 ps of skew.",
            ),
            q(
                "What is a key benefit of routing a signal as a differential pair?",
                (
                    opt("It eliminates the need for any reference plane"),
                    opt(
                        "Noise hits both traces equally and cancels in the difference", correct=True
                    ),
                    opt("It doubles the supply voltage to the receiver"),
                    opt("It removes the need to length-match the bus"),
                ),
                "Differential signaling rejects common noise, has low emission, and uses a defined differential impedance.",
            ),
            q(
                "What does the common 3W rule for crosstalk specify?",
                (
                    opt("Use three times the supply voltage on fast nets"),
                    opt("Add three vias per high-speed trace"),
                    opt(
                        "Keep centre-to-centre spacing at least three times the trace width",
                        correct=True,
                    ),
                    opt("Limit traces to three watts of dissipation"),
                ),
                "Crosstalk shrinks with spacing, so the 3W rule keeps centre-to-centre spacing at least three trace widths apart.",
            ),
        ),
        "Thermal design of boards": (
            q(
                "In the thermal Ohm's law analogy, what plays the role of resistance?",
                (
                    opt("Thermal resistance theta in C/W", correct=True),
                    opt("Dissipated power P in watts"),
                    opt("Ambient temperature T_ambient"),
                    opt("The characteristic impedance Z_0"),
                ),
                "Delta T = P times theta_ja, so theta (C/W) is the thermal analog of electrical resistance.",
            ),
            q(
                "Why does increasing copper pour area give diminishing returns on thermal resistance?",
                (
                    opt("Copper loses conductivity above a certain area"),
                    opt(
                        "Air convection eventually limits how much more heat can escape",
                        correct=True,
                    ),
                    opt("Larger pours raise the junction temperature limit"),
                    opt("Extra copper adds series inductance to the heat path"),
                ),
                "More pour lowers theta, but the curve flattens because convection to air becomes the limiting factor.",
            ),
            q(
                "What is the purpose of a thermal via array under a power part's pad?",
                (
                    opt("To match the trace impedance to 50 ohm"),
                    opt("To decouple the power supply at high frequency"),
                    opt(
                        "To pull heat through to an internal or bottom plane that then convects to air",
                        correct=True,
                    ),
                    opt("To increase the loop area for better radiation"),
                ),
                "A grid of thermal vias gives parallel heat paths into a plane that spreads and convects the heat.",
            ),
        ),
        "Lab: microstrip impedance & trace reflection": (
            q(
                "In Part 1 of the lab, how is the trace width for ~50 ohm found?",
                (
                    opt("By picking the width with the largest Z0 in the sweep"),
                    opt(
                        "By selecting the width where Z0 is closest to 50 ohm via argmin of abs(Z0 - 50)",
                        correct=True,
                    ),
                    opt("By solving a system of linear equations"),
                    opt("By reading it directly from the FR4 permittivity"),
                ),
                "The lab uses np.argmin(np.abs(Z0 - 50)) to locate the swept width nearest 50 ohm.",
            ),
            q(
                "In Part 2, what condition makes the launched step under-damped and ring?",
                (
                    opt("Source impedance Zs less than the line impedance Z0", correct=True),
                    opt("Load impedance ZL equal to Z0"),
                    opt("A dielectric height h of zero"),
                    opt("Copper thickness t larger than the trace width"),
                ),
                "The lab sets Zs = 25 ohm, below the 50 ohm line, giving an under-damped, ringing response into the open load.",
            ),
            q(
                "Per the lab's 'Try it yourself', what does setting Zs = 50 accomplish?",
                (
                    opt("It opens the receiver end of the line"),
                    opt(
                        "It matches the source so the ringing vanishes (series termination)",
                        correct=True,
                    ),
                    opt("It doubles the overshoot peak voltage"),
                    opt("It changes the FR4 relative permittivity"),
                ),
                "Matching the source impedance to the 50 ohm line removes the reflections, acting as series termination.",
            ),
        ),
    },
    final=(
        q(
            "Which single layout discipline most directly reduces both EMI and PDN/return-path noise?",
            (
                opt("Using the largest possible decoupling capacitor only"),
                opt(
                    "Keeping return current loop areas small with a solid reference plane",
                    correct=True,
                ),
                opt("Routing every signal across plane splits"),
                opt("Maximising via count on fast nets"),
            ),
            "Minimising loop area via a continuous plane lowers inductance, radiation, and noise susceptibility.",
        ),
        q(
            "A 50 ohm line is driven into a 75 ohm load. What is the reflection coefficient?",
            (
                opt("0, the line is matched"),
                opt("+0.2, a partial reflection", correct=True),
                opt("-0.2, an inverted reflection"),
                opt("+1, a full reflection"),
            ),
            "Gamma = (75 - 50)/(75 + 50) = 25/125 = +0.2, so about 20 percent reflects.",
        ),
        q(
            "On FR4 signals travel at about 6 ps/mm. Roughly how much skew does a 10 mm length mismatch create?",
            (
                opt("About 6 ps"),
                opt("About 67 ps", correct=True),
                opt("About 600 ps"),
                opt("Zero, length does not affect timing"),
            ),
            "t_skew = 10 mm / (1.5e8 m/s) is about 67 ps, enough to break a fast DDR bus.",
        ),
        q(
            "A part dissipates 2 W with theta_ja of 35 C/W in a 25 C ambient. What is the junction temperature?",
            (
                opt("70 C"),
                opt("95 C", correct=True),
                opt("125 C"),
                opt("35 C"),
            ),
            "T_junction = T_ambient + P times theta_ja = 25 + 2 times 35 = 95 C.",
        ),
        q(
            "Why does a fast edge matter for signal integrity even on a slow clock?",
            (
                opt(
                    "The edge rate, not the clock frequency, decides if reflections and ringing occur",
                    correct=True,
                ),
                opt("Slow clocks cannot drive transmission lines at all"),
                opt("A slow clock automatically terminates the line"),
                opt("Edge rate only affects thermal design"),
            ),
            "A 1 MHz clock with a 1 ns edge still rings; the fast edge is what turns a trace into a transmission line.",
        ),
    ),
)
