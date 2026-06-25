"""Curated quiz questions for the RFIC & RF Circuit Design - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "RF basics: why RF is different": (
            q(
                "Why does a wire stop behaving like a simple node at radio frequencies?",
                (
                    opt("Because the metal resistance suddenly drops to zero"),
                    opt(
                        "Because its length becomes a non-trivial fraction of the wavelength, so voltage and current vary along it",
                        correct=True,
                    ),
                    opt("Because RF signals carry no current, only voltage"),
                    opt("Because capacitors stop conducting at high frequency"),
                ),
                "When a conductor is a significant fraction of a wavelength long, the signal varies along it and the circuit is distributed rather than lumped.",
            ),
            q(
                "Approximately what is the free-space wavelength at 1 GHz?",
                (
                    opt("About 3 mm"),
                    opt("About 30 cm", correct=True),
                    opt("About 3 m"),
                    opt("About 30 m"),
                ),
                "lambda = c/f = 3e8 / 1e9 = 0.3 m, about 30 cm.",
            ),
            q(
                "Which statement best captures why parasitics matter so much at RF?",
                (
                    opt("Parasitics only matter in digital circuits"),
                    opt(
                        "A bond wire, pad or trace becomes an inductor, capacitor or transmission line that is part of the circuit",
                        correct=True,
                    ),
                    opt("Parasitics cancel out at high frequency"),
                    opt("Parasitics only affect DC bias points"),
                ),
                "At RF the parasitic L of a bond wire, C of a pad and the line behaviour of a trace are the circuit, not afterthoughts.",
            ),
        ),
        "Decibels, dBm & link-budget intuition": (
            q(
                "How many milliwatts is 0 dBm?",
                (
                    opt("0 mW"),
                    opt("1 mW", correct=True),
                    opt("10 mW"),
                    opt("1000 mW"),
                ),
                "dBm is referenced to 1 mW, so 0 dBm is exactly 1 mW.",
            ),
            q(
                "A power ratio of x2 corresponds to about how many dB?",
                (
                    opt("About +1 dB"),
                    opt("About +3 dB", correct=True),
                    opt("About +6 dB"),
                    opt("About +10 dB"),
                ),
                "10*log10(2) is about 3.01 dB, so doubling power is roughly +3 dB.",
            ),
            q(
                "Why are decibels convenient for a link budget?",
                (
                    opt("They convert all powers to zero"),
                    opt(
                        "Gains and losses simply add and subtract instead of multiplying",
                        correct=True,
                    ),
                    opt("They eliminate the need to know the transmit power"),
                    opt("They make every stage have the same gain"),
                ),
                "In dB the output level is input plus gains minus losses, turning multiplication into addition.",
            ),
        ),
        "Impedance matching & the Smith chart": (
            q(
                "What value of the reflection coefficient Gamma indicates a perfect match?",
                (
                    opt("Gamma = 1"),
                    opt("Gamma = 0", correct=True),
                    opt("Gamma = -1"),
                    opt("Gamma = 50"),
                ),
                "Gamma = (Z_L - Z0)/(Z_L + Z0); when Z_L = Z0 the numerator is zero, so Gamma = 0 is a perfect match.",
            ),
            q(
                "What does the Smith chart let an RF designer do graphically?",
                (
                    opt("Measure the noise figure of a transistor directly"),
                    opt(
                        "Plot every possible reflection coefficient and turn adding L or C into moves along arcs toward the matched centre",
                        correct=True,
                    ),
                    opt("Read the DC operating point of a circuit"),
                    opt("Compute digital bit error rates"),
                ),
                "The Smith chart maps Gamma inside the unit circle with an impedance grid, so matching becomes finding a path to the centre.",
            ),
            q(
                "For maximum power transfer in a 50 ohm system, what should each interface present?",
                (
                    opt("An open circuit"),
                    opt("A short circuit"),
                    opt("50 ohms (the conjugate match)", correct=True),
                    opt("As high an impedance as possible"),
                ),
                "Maximum power transfers when the load is the conjugate of the source; in a real 50 ohm system that means presenting 50 ohms.",
            ),
        ),
        "S-parameters & two-port RF networks": (
            q(
                "Which S-parameter represents the forward gain of a two-port?",
                (
                    opt("S11"),
                    opt("S12"),
                    opt("S21", correct=True),
                    opt("S22"),
                ),
                "S21 is the forward transmission, the gain you usually quote in dB.",
            ),
            q(
                "What does S11 describe?",
                (
                    opt("Reverse isolation"),
                    opt("Input reflection / input match", correct=True),
                    opt("Forward gain"),
                    opt("Output match"),
                ),
                "S11 is the input reflection coefficient, describing how well the input is matched (return loss).",
            ),
            q(
                "Why are S-parameters preferred over open/short measurements at RF?",
                (
                    opt("They require no test equipment"),
                    opt(
                        "They use matched 50 ohm terminations, avoiding the reflections and instability that opens/shorts cause",
                        correct=True,
                    ),
                    opt("They only work at DC"),
                    opt("They ignore reflected waves entirely"),
                ),
                "Open/short tests reflect heavily and can make devices oscillate; S-parameters use travelling waves in a matched environment.",
            ),
        ),
        "Transmission lines: reflection & VSWR": (
            q(
                "What is the VSWR of a perfectly matched line?",
                (
                    opt("0:1"),
                    opt("1:1", correct=True),
                    opt("2:1"),
                    opt("infinity:1"),
                ),
                "VSWR = (1+|Gamma|)/(1-|Gamma|); with Gamma = 0 this is 1:1, a perfect match.",
            ),
            q(
                "What sets a transmission line's characteristic impedance Z0?",
                (
                    opt("Its length"),
                    opt("Its geometry (cross-section / dielectric)", correct=True),
                    opt("The frequency of operation"),
                    opt("The source voltage"),
                ),
                "Z0 is determined by the line's geometry and dielectric, independent of its length.",
            ),
            q(
                "A quarter-wave line transforms impedance according to which relation?",
                (
                    opt("Z_in = Z_L"),
                    opt("Z_in = Z0^2 / Z_L", correct=True),
                    opt("Z_in = Z0 + Z_L"),
                    opt("Z_in = Z0 * Z_L"),
                ),
                "A quarter-wave transformer gives Z_in = Z0^2 / Z_L, the basis of many matching networks.",
            ),
        ),
        "Resonant tanks & matching networks": (
            q(
                "What is the resonant frequency of an LC tank?",
                (
                    opt("f0 = 1/(2*pi*R*C)"),
                    opt("f0 = 1/(2*pi*sqrt(L*C))", correct=True),
                    opt("f0 = 2*pi*sqrt(L*C)"),
                    opt("f0 = L*C"),
                ),
                "The LC resonant frequency is f0 = 1/(2*pi*sqrt(L*C)).",
            ),
            q(
                "What does a high quality factor Q indicate for a tank?",
                (
                    opt("A broad, low-selectivity response"),
                    opt("A narrow, sharp, low-loss response", correct=True),
                    opt("That the tank cannot resonate"),
                    opt("A purely resistive impedance"),
                ),
                "Q = f0/bandwidth; high Q means a narrow, selective, low-loss peak.",
            ),
            q(
                "What advantage does a pi- or T-match have over a simple L-match?",
                (
                    opt("It uses fewer components"),
                    opt(
                        "It lets you set the loaded Q (bandwidth) independently of the transformation ratio",
                        correct=True,
                    ),
                    opt("It works only at DC"),
                    opt("It removes the need for inductors"),
                ),
                "The third element in a pi or T network gives a free parameter so bandwidth and transformation ratio can be chosen separately.",
            ),
        ),
    },
    final=(
        q(
            "Fundamentally, why is RF circuit design different from low-frequency design?",
            (
                opt("Resistors stop working above 1 MHz"),
                opt(
                    "At RF the geometry is circuitry: distributed effects, parasitics and reflections dominate",
                    correct=True,
                ),
                opt("RF circuits use no transistors"),
                opt("Voltage no longer matters at RF"),
            ),
            "At RF, wavelength-scale geometry makes circuits distributed, so parasitics, matching and reflections dominate.",
        ),
        q(
            "Which set of anchors is correct?",
            (
                opt("0 dBm = 1 W and +30 dBm = 1 mW"),
                opt("0 dBm = 1 mW and +30 dBm = 1 W", correct=True),
                opt("0 dBm = 1 uW and +3 dB = x10"),
                opt("+10 dB = x2 and +3 dB = x10"),
            ),
            "0 dBm = 1 mW, +30 dBm = 1 W, +3 dB is about x2 and +10 dB is x10.",
        ),
        q(
            "The reflection coefficient Gamma is defined as:",
            (
                opt("(Z_L + Z0)/(Z_L - Z0)"),
                opt("(Z_L - Z0)/(Z_L + Z0)", correct=True),
                opt("Z_L / Z0"),
                opt("Z0 / Z_L"),
            ),
            "Gamma = (Z_L - Z0)/(Z_L + Z0), zero at a perfect match.",
        ),
        q(
            "Which S-parameter pairing is correct?",
            (
                opt("S21 = input match, S11 = forward gain"),
                opt("S12 = forward gain, S22 = reverse isolation"),
                opt("S21 = forward gain, S11 = input match, S22 = output match", correct=True),
                opt("S11 = output match, S22 = input match"),
            ),
            "S21 is forward gain, S11 input match, S22 output match, and S12 reverse isolation.",
        ),
        q(
            "On a mismatched transmission line, the standing-wave maximum and minimum are:",
            (
                opt("1 and 0 regardless of Gamma"),
                opt("1+|Gamma| and 1-|Gamma|", correct=True),
                opt("Gamma and 1/Gamma"),
                opt("Z0 and Z_L"),
            ),
            "The standing-wave envelope ranges between 1+|Gamma| (max) and 1-|Gamma| (min).",
        ),
        q(
            "Why might a designer choose a pi-match instead of an L-match?",
            (
                opt("To avoid using any capacitors"),
                opt(
                    "To control the bandwidth (loaded Q) independently of the impedance transformation ratio",
                    correct=True,
                ),
                opt("Because L-matches cannot transform impedance"),
                opt("Because pi-matches are always lower loss"),
            ),
            "The extra element in a pi-match adds a degree of freedom, letting bandwidth be set separately from the transformation ratio.",
        ),
    ),
)
