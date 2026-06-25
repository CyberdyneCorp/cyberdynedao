"""Curated quiz questions for the RFIC & RF Circuit Design - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Power amplifiers: classes & efficiency": (
            q(
                "What is the theoretical maximum drain efficiency of a Class A power amplifier?",
                (
                    opt("25%"),
                    opt("50%", correct=True),
                    opt("78.5%"),
                    opt("100%"),
                ),
                "Class A conducts the full cycle and is most linear, but its theoretical maximum drain efficiency is only 50%.",
            ),
            q(
                "What largely distinguishes one PA class from another?",
                (
                    opt("The supply voltage only"),
                    opt(
                        "The conduction angle (how much of each RF cycle the device conducts)",
                        correct=True,
                    ),
                    opt("The package material"),
                    opt("The operating frequency"),
                ),
                "The conduction angle sets the class and the linearity-versus-efficiency trade-off.",
            ),
            q(
                "How do switching PAs (Class D/E/F) achieve high efficiency?",
                (
                    opt("By conducting for the full 360 degrees"),
                    opt(
                        "By operating the transistor as a switch rather than a linear amplifier",
                        correct=True,
                    ),
                    opt("By adding more bias current"),
                    opt("By lowering the load impedance to zero"),
                ),
                "In switching classes the transistor acts as a switch (ideally 100% efficient), with waveform/harmonic shaping, but is non-linear.",
            ),
        ),
        "PA linearization: back-off, predistortion, Doherty": (
            q(
                "Why does a high-PAPR signal force a linear PA into back-off?",
                (
                    opt("To increase its gain"),
                    opt(
                        "To keep the signal peaks below the compression point, at the cost of efficiency",
                        correct=True,
                    ),
                    opt("To reduce the operating frequency"),
                    opt("To eliminate phase noise"),
                ),
                "High peak-to-average ratio means peaks must stay below P1dB, so the PA runs backed off and efficiency suffers.",
            ),
            q(
                "What does digital predistortion (DPD) do?",
                (
                    opt("It filters the output spectrum"),
                    opt(
                        "It pre-warps the input with the inverse of the PA's distortion so the cascade is linear",
                        correct=True,
                    ),
                    opt("It lowers the supply voltage"),
                    opt("It adds a second antenna"),
                ),
                "DPD applies the inverse nonlinearity ahead of the PA so their combination is linear.",
            ),
            q(
                "How does a Doherty PA maintain efficiency over back-off?",
                (
                    opt("By turning the whole amplifier off at low power"),
                    opt(
                        "A peaking amplifier turns on only for peaks and load-modulates the main amplifier through a combining network",
                        correct=True,
                    ),
                    opt("By increasing phase noise"),
                    opt("By using a single Class A device"),
                ),
                "The Doherty's peaking stage engages at peaks and modulates the main device's load, keeping efficiency high across back-off.",
            ),
        ),
        "Frequency synthesis: integer & fractional-N PLLs": (
            q(
                "In an integer-N PLL, the output frequency is:",
                (
                    opt("f_out = f_ref / N"),
                    opt("f_out = N * f_ref", correct=True),
                    opt("f_out = f_ref - N"),
                    opt("f_out = f_ref * f_ref"),
                ),
                "With a divide-by-N in feedback, the loop forces f_out = N * f_ref.",
            ),
            q(
                "What is the channel step of an integer-N PLL?",
                (
                    opt("Always 1 Hz"),
                    opt("Equal to the reference frequency f_ref", correct=True),
                    opt("Equal to the VCO frequency"),
                    opt("Independent of f_ref"),
                ),
                "Integer-N steps in increments of f_ref, so fine resolution forces a small reference (and large N / narrow bandwidth).",
            ),
            q(
                "How does a fractional-N PLL get fine resolution without a tiny reference?",
                (
                    opt("By using two crystals"),
                    opt(
                        "A sigma-delta modulator dithers N between integers so the average divide ratio is fractional",
                        correct=True,
                    ),
                    opt("By removing the divider entirely"),
                    opt("By increasing the charge-pump current"),
                ),
                "Dithering N with a sigma-delta modulator yields a fractional average ratio, decoupling step size from f_ref at the cost of fractional spurs.",
            ),
        ),
        "On-chip passives: inductors, Q & transformers": (
            q(
                "Why is an on-chip spiral inductor usually the worst component on the chip?",
                (
                    opt("It consumes the most DC current"),
                    opt(
                        "Metal resistance, skin effect and substrate eddy currents limit its Q to only about 5-20",
                        correct=True,
                    ),
                    opt("It cannot store energy"),
                    opt("It only works at DC"),
                ),
                "Series resistance, skin effect and substrate losses keep on-chip Q low (about 5-20) versus hundreds for a discrete coil.",
            ),
            q(
                "What does an on-chip transformer (two coupled spirals) provide?",
                (
                    opt("Only DC gain"),
                    opt(
                        "Impedance transformation, single-ended to differential conversion (balun), isolation and bias injection",
                        correct=True,
                    ),
                    opt("A reduction in phase noise to zero"),
                    opt("Digital logic functions"),
                ),
                "Transformers give impedance transformation, single-ended/differential conversion, DC isolation and a bias-injection point.",
            ),
            q(
                "Why does an inductor's Q peak and then fall with frequency?",
                (
                    opt("Because the inductance grows without bound"),
                    opt(
                        "Rising reactance helps until losses and self-resonance from parasitic capacitance pull Q back down",
                        correct=True,
                    ),
                    opt("Because the substrate becomes a perfect conductor"),
                    opt("Because Q is constant with frequency"),
                ),
                "Q rises with frequency until frequency-dependent losses and parasitic-capacitance self-resonance dominate, so you design the peak in-band.",
            ),
        ),
        "RFIC layout, packaging & EM coupling": (
            q(
                "Why is the statement 'the layout is the schematic' especially true at RF?",
                (
                    opt("Because schematics are not used in RF design"),
                    opt(
                        "Because interconnect parasitics, EM coupling and substrate noise are part of the circuit and can detune or destabilise it",
                        correct=True,
                    ),
                    opt("Because RF circuits have no transistors"),
                    opt("Because layout only affects DC behaviour"),
                ),
                "At RF, traces, parasitics, coupling and substrate effects are circuit elements; poor layout can detune, desensitise or oscillate.",
            ),
            q(
                "What is a typical bond-wire inductance, and why does it matter?",
                (
                    opt("About 1 nH/mm; it shifts the impedance match", correct=True),
                    opt("About 1 F/mm; it shorts the supply"),
                    opt("Exactly zero; bond wires are ideal"),
                    opt("About 1 ohm/mm; it only adds DC loss"),
                ),
                "Bond wires add roughly 1 nH/mm of inductance, shifting the match; flip-chip packaging reduces it.",
            ),
            q(
                "Which technique helps isolate a sensitive RF node from substrate noise?",
                (
                    opt("Removing all ground connections"),
                    opt("Deep n-well isolation, guard rings and separate supplies", correct=True),
                    opt("Placing aggressor and victim as close as possible"),
                    opt("Sharing one bond wire for ground"),
                ),
                "Deep n-well, guard rings, ground shields and separate supplies isolate sensitive nodes from substrate and EM coupling.",
            ),
        ),
        "Design example: an RX front-end from spec to budget": (
            q(
                "Starting from sensitivity, how is the allowed system noise figure found?",
                (
                    opt("Sensitivity minus the thermal floor minus the required SNR"),
                    opt(
                        "Sensitivity = thermal floor + bandwidth + NF + required SNR, solved for NF",
                        correct=True,
                    ),
                    opt("It equals the LNA gain"),
                    opt("It is always 0 dB"),
                ),
                "Sensitivity = (-174 dBm/Hz + 10log(BW)) + NF + SNR, so NF is the slack between the floor-plus-SNR and the sensitivity target.",
            ),
            q(
                "When budgeting an RX chain, how do gain choices pull noise and linearity?",
                (
                    opt("More front-end gain improves both noise and linearity"),
                    opt(
                        "More front-end gain lowers noise figure but worsens cascade linearity (IIP3)",
                        correct=True,
                    ),
                    opt("Gain has no effect on either"),
                    opt("More gain only changes the package"),
                ),
                "Front-end gain suppresses later-stage noise (better NF) but degrades cascade IIP3, so the design point balances both with margin.",
            ),
            q(
                "What is the overarching mindset of RFIC design captured by this example?",
                (
                    opt("Pick the cheapest transistor and simulate once"),
                    opt(
                        "Translate a system spec into a per-block noise/linearity/gain budget, verify with Friis and inverse-IP3, then design each block",
                        correct=True,
                    ),
                    opt("Maximise gain everywhere regardless of spec"),
                    opt("Ignore the mixer and oscillator"),
                ),
                "RFIC design is budgeting: allocate noise, linearity and gain across blocks, check with Friis and inverse-IP3, then design each block to its slice.",
            ),
        ),
    },
    final=(
        q(
            "Which ordering reflects rising efficiency (and falling linearity) of PA classes?",
            (
                opt("Class C, then AB, then A"),
                opt("Class A, then AB/B, then C, then switching D/E/F", correct=True),
                opt("Switching first, then Class A"),
                opt("All classes have identical efficiency"),
            ),
            "Efficiency rises from Class A through AB/B to C and the switching classes, trading off linearity along the way.",
        ),
        q(
            "Which technique recovers PA efficiency across back-off using a peaking amplifier and load modulation?",
            (
                opt("Envelope tracking"),
                opt("Doherty", correct=True),
                opt("Simple back-off"),
                opt("Class A biasing"),
            ),
            "The Doherty PA uses a peaking amplifier and a combining network to keep efficiency high over a wide back-off range.",
        ),
        q(
            "What key advantage does a fractional-N PLL have over integer-N?",
            (
                opt("It removes the VCO"),
                opt(
                    "It decouples frequency step size from the reference, allowing a high f_ref (fast loop, low N) with fine resolution",
                    correct=True,
                ),
                opt("It has no phase noise"),
                opt("It uses no divider"),
            ),
            "Fractional-N dithers the divide ratio so step size is independent of f_ref, enabling a high reference and fine steps (at the cost of fractional spurs).",
        ),
        q(
            "Why is on-chip inductor Q so important?",
            (
                opt("It sets the digital clock speed"),
                opt(
                    "Low Q directly degrades oscillator phase noise and filter selectivity",
                    correct=True,
                ),
                opt("It determines the supply voltage"),
                opt("It has no effect on RF performance"),
            ),
            "Inductor Q (about 5-20 on chip) limits oscillator phase noise via Leeson and tank/filter selectivity.",
        ),
        q(
            "Which is a real RFIC layout hazard?",
            (
                opt("The PA coupling into the VCO and pulling it"),
                opt("Bond-wire inductance shifting the match"),
                opt("Digital switching noise coupling through the substrate into the LNA"),
                opt("All of the above", correct=True),
            ),
            "EM coupling (PA into VCO), bond-wire inductance, and substrate noise into the LNA are all genuine RF layout hazards.",
        ),
        q(
            "In the RX front-end design flow, what is the correct sequence?",
            (
                opt("Design blocks first, then guess a spec"),
                opt(
                    "Spec -> noise/linearity (NF & IIP3) budget -> allocate to blocks (Friis, inverse-IP3) -> design each block",
                    correct=True,
                ),
                opt("Choose a package, then ignore the budget"),
                opt("Maximise gain, then check nothing"),
            ),
            "Top-down: turn the spec into an NF/IP3 budget, allocate it across blocks with Friis and inverse-IP3, then design each block to its slice.",
        ),
    ),
)
