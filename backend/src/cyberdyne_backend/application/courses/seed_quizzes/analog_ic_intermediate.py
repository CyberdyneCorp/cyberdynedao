from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The two-stage op-amp": (
            q(
                "Why cascade two gain stages in a precision op-amp?",
                (
                    opt("A single stage already gives over 100 dB"),
                    opt(
                        "One stage gives only about 30 to 50 dB, and cascading multiplies the gains",
                        correct=True,
                    ),
                    opt("Two stages reduce the input offset to zero"),
                    opt("It removes the need for any feedback"),
                ),
                "A single stage gives g_m r_o (about 30 to 50 dB); cascading two multiplies the gains to about 100 dB.",
            ),
            q(
                "In the two-stage Miller op-amp, what is the role of stage 1?",
                (
                    opt("A common-source stage that provides the output swing"),
                    opt(
                        "A differential pair with an active mirror load that sets gain, offset, and most noise",
                        correct=True,
                    ),
                    opt("A class-AB push-pull output buffer"),
                    opt("The Miller compensation capacitor"),
                ),
                "Stage 1 is the differential pair with a mirror load: high gain, diff-to-single conversion, sets offset and most noise.",
            ),
            q(
                "Why does an op-amp driving a real resistor or pin add a class-AB output stage?",
                (
                    opt("To increase the DC gain to (g_m r_o) squared"),
                    opt("To create the Miller compensation effect"),
                    opt(
                        "The common-source stage has high output resistance, poor for driving resistive loads",
                        correct=True,
                    ),
                    opt("To convert the differential signal to single-ended"),
                ),
                "The common-source second stage has high output resistance, so a class-AB push-pull buffer is added to drive real loads.",
            ),
        ),
        "Feedback and stability": (
            q(
                "What does the loop gain A times beta determine in a feedback amplifier?",
                (
                    opt("Only the slew rate"),
                    opt(
                        "Whether closed-loop gain depends on the precise feedback network rather than the transistor",
                        correct=True,
                    ),
                    opt("The thermal noise floor"),
                    opt("The bandgap reference voltage"),
                ),
                "Large loop gain A times beta makes the closed-loop gain depend only on the precise passive feedback network.",
            ),
            q(
                "An amplifier oscillates when, at the unity-gain frequency, the phase lag reaches what value?",
                (
                    opt("-90 degrees"),
                    opt("-45 degrees"),
                    opt("-180 degrees, turning negative feedback positive", correct=True),
                    opt("-60 degrees"),
                ),
                "If loop gain still exceeds 1 when phase lag reaches -180 degrees, negative feedback becomes positive and it oscillates.",
            ),
            q(
                "What does Miller compensation do to the two close poles of a two-stage op-amp?",
                (
                    opt("It removes the second stage entirely"),
                    opt(
                        "Pole splitting: pushes the dominant pole way down so it rolls off before the second pole adds lag",
                        correct=True,
                    ),
                    opt("It raises both poles equally"),
                    opt("It increases the tail current to widen bandwidth"),
                ),
                "Miller compensation splits the poles, pushing the first pole way down so the amp rolls off before the second pole adds phase lag.",
            ),
        ),
        "Noise in analog circuits": (
            q(
                "Which noise source is white (flat across frequency)?",
                (
                    opt("Flicker (1/f) noise"),
                    opt("Thermal (Johnson) noise", correct=True),
                    opt("Quantization noise only"),
                    opt("Shot noise from the bandgap"),
                ),
                "Thermal (Johnson) noise is white, the same at every frequency; flicker noise rises at low frequencies.",
            ),
            q(
                "Why are the input differential-pair transistors made large in a low-noise op-amp?",
                (
                    opt("To increase the supply voltage"),
                    opt(
                        "Large W times L lowers flicker noise, and they dominate input-referred noise",
                        correct=True,
                    ),
                    opt("To raise the Miller capacitance"),
                    opt("To reduce the loop gain"),
                ),
                "Input-referred noise is dominated by the input pair; large devices lower flicker noise and they are biased for low thermal noise.",
            ),
            q(
                "What technique specifically cancels the flicker noise contributed by the input pair?",
                (
                    opt("Miller compensation"),
                    opt("Pole splitting"),
                    opt("Chopping and correlated double sampling", correct=True),
                    opt("Increasing the slew rate"),
                ),
                "Chopping and correlated double sampling cancel the low-frequency flicker noise the diff pair would otherwise contribute.",
            ),
        ),
        "Bandgap and voltage references": (
            q(
                "How does a bandgap reference achieve a voltage that is flat over temperature?",
                (
                    opt("By using a single diode VBE term"),
                    opt(
                        "By adding a scaled PTAT term to a CTAT term so the opposite slopes cancel",
                        correct=True,
                    ),
                    opt("By raising the supply voltage"),
                    opt("By increasing the OSR"),
                ),
                "A CTAT VBE (falls with T) plus a scaled PTAT delta-VBE (rises with T) cancel slopes to give about 1.2 V flat over temperature.",
            ),
            q(
                "The PTAT term in a bandgap comes from which quantity?",
                (
                    opt("A single base-emitter voltage VBE"),
                    opt(
                        "The difference delta-VBE of two VBE at different current densities, equal to kT/q times ln N",
                        correct=True,
                    ),
                    opt("The thermal noise of the load resistor"),
                    opt("The Miller capacitor charging current"),
                ),
                "delta-VBE = (kT/q) ln N rises with temperature, providing the PTAT term that offsets the falling CTAT VBE.",
            ),
            q(
                "Why is PSRR important for a voltage reference?",
                (
                    opt("It sets the slew rate of the op-amp"),
                    opt(
                        "Supply ripple must be rejected or it shows up directly in an ADC output",
                        correct=True,
                    ),
                    opt("It determines the 1/f corner frequency"),
                    opt("It fixes the unity-gain bandwidth"),
                ),
                "PSRR quantifies supply-ripple rejection; without it the supply wiggle would appear directly in Vref and the ADC output.",
            ),
        ),
        "The OTA and switched-capacitor circuits": (
            q(
                "What does an Operational Transconductance Amplifier output?",
                (
                    opt("A voltage proportional to input current"),
                    opt("A current proportional to its differential input voltage", correct=True),
                    opt("A fixed 1.2 V reference"),
                    opt("A square-wave clock"),
                ),
                "An OTA outputs a current i_out = g_m times v_id; it drives capacitors, not resistive loads.",
            ),
            q(
                "A capacitor toggled between two nodes at frequency f_s emulates a resistor of what value?",
                (
                    opt("R_eq = C times f_s"),
                    opt("R_eq = 1/(C times f_s)", correct=True),
                    opt("R_eq = f_s / C"),
                    opt("R_eq = C / f_s"),
                ),
                "Each cycle the switched cap ferries charge C times delta-V; the average current makes R_eq = 1/(C f_s).",
            ),
            q(
                "Why are switched-capacitor integrators remarkably precise on silicon?",
                (
                    opt("Because absolute capacitor values are very accurate"),
                    opt(
                        "Their time constant is a ratio of capacitors times a clock, and ratios match to about 0.1%",
                        correct=True,
                    ),
                    opt("Because on-chip resistors are extremely precise"),
                    opt("Because the OTA cancels all noise"),
                ),
                "Capacitor ratios match to about 0.1% while absolute values vary wildly, so SC time constants (C1/(C2 f_s)) are precise and process-independent.",
            ),
        ),
        "Lab: loop gain, phase margin, and a bandgap curve": (
            q(
                "In the lab, why is the feedback factor beta set to 1 for the loop-gain analysis?",
                (
                    opt("To maximize the bandgap accuracy"),
                    opt("Unity-gain feedback is the worst case for stability", correct=True),
                    opt("To remove the second pole"),
                    opt("Because beta = 1 gives the lowest noise"),
                ),
                "The lab sets beta = 1.0 noting it is unity-gain feedback, the worst case for stability when reading phase margin.",
            ),
            q(
                "What happens in the lab if you move the second pole fp2 down to 5e5?",
                (
                    opt("The bandgap drift goes to zero"),
                    opt("The phase margin collapses and the op-amp rings", correct=True),
                    opt("The loop DC gain doubles"),
                    opt("The unity-gain crossover disappears"),
                ),
                "The Try it yourself note says moving fp2 down to 5e5 collapses the phase margin so the op-amp rings.",
            ),
            q(
                "How does the lab locate the bandgap flat point over temperature?",
                (
                    opt("By taking the maximum of Vref"),
                    opt(
                        "By finding the minimum-slope (minimum gradient) point of Vref vs T",
                        correct=True,
                    ),
                    opt("By setting M to zero"),
                    opt("By integrating the quantization noise"),
                ),
                "The lab finds flat_T as the temperature where the gradient of Vref vs Tc is minimum (the minimum-slope point).",
            ),
        ),
    },
    final=(
        q(
            "What is the total DC gain of an ideal two-stage Miller op-amp?",
            (
                opt("About g_m r_o, roughly 30 to 50 dB"),
                opt("Roughly (g_m r_o) squared, about 100 dB", correct=True),
                opt("Exactly 1.2 V"),
                opt("6.02 N + 1.76 dB"),
            ),
            "Two cascaded stages multiply gains, giving about (g_m r_o) squared, roughly 100 dB.",
        ),
        q(
            "Which pair of specifications are independent limits, one small-signal and one large-signal?",
            (
                opt("PSRR and 1/f corner"),
                opt(
                    "Bandwidth (small-signal) and slew rate SR = I_tail/C_c (large-signal)",
                    correct=True,
                ),
                opt("Thermal noise and flicker noise"),
                opt("PTAT and CTAT"),
            ),
            "Bandwidth is a small-signal limit; slew rate SR = I_tail/C_c is the large-signal speed limit; both matter independently.",
        ),
        q(
            "A bandgap reference cancels temperature drift by combining which two terms?",
            (
                opt("Two thermal noise sources"),
                opt(
                    "A CTAT VBE that falls with T and a scaled PTAT delta-VBE that rises with T",
                    correct=True,
                ),
                opt("Loop gain and phase margin"),
                opt("Two identical VBE terms"),
            ),
            "CTAT (VBE falling at about -2 mV/C) plus a scaled PTAT (delta-VBE rising) cancel to about 1.2 V flat over temperature.",
        ),
        q(
            "Why does a switched capacitor make an integrator's time constant precise on silicon?",
            (
                opt("Because absolute capacitance is accurate"),
                opt(
                    "Because the constant becomes a ratio of capacitors times a clock, and ratios match closely",
                    correct=True,
                ),
                opt("Because OTAs have infinite output resistance"),
                opt("Because thermal noise is white"),
            ),
            "Replacing the resistor with a switched cap makes the time constant C1/(C2 f_s); capacitor ratios match to about 0.1%.",
        ),
        q(
            "Which quantity is the single most important one in feedback design?",
            (
                opt("The slew rate"),
                opt("The loop gain A times beta", correct=True),
                opt("The 1/f corner frequency"),
                opt("The PSRR"),
            ),
            "The loop gain A times beta determines precision, bandwidth, and stability and is the single most important quantity in feedback design.",
        ),
    ),
)
