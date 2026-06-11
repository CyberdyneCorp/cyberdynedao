from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Transmission lines: telegrapher equations, Z0, reflection & VSWR": (
            q(
                "For a lossless transmission line, what is the characteristic impedance Z0?",
                (
                    opt("sqrt(L/C)", correct=True),
                    opt("sqrt(C/L)"),
                    opt("sqrt(L*C)"),
                    opt("L/C"),
                ),
                "For a lossless line (R = G = 0), Z0 reduces to the square root of L over C.",
            ),
            q(
                "The reflection coefficient at the load is Gamma = (ZL - Z0)/(ZL + Z0). What is Gamma for a perfectly matched load?",
                (
                    opt("0", correct=True),
                    opt("1"),
                    opt("-1"),
                    opt("infinity"),
                ),
                "A perfect match has ZL = Z0, so Gamma = 0 and VSWR = 1.",
            ),
            q(
                "Per the rule of thumb in the lesson, when should a wire be treated as a long transmission line?",
                (
                    opt("once its length exceeds about one tenth of a wavelength", correct=True),
                    opt("once its length exceeds one full wavelength"),
                    opt("once its length exceeds 50 cm regardless of frequency"),
                    opt("only at frequencies below 1 GHz"),
                ),
                "The rule of thumb is to treat a line as long once it exceeds about lambda over 10.",
            ),
        ),
        "The Smith chart: impedance, admittance & plotting Gamma": (
            q(
                "On the Smith chart, where does a perfectly matched load (z = 1) appear?",
                (
                    opt("at the center, where Gamma = 0", correct=True),
                    opt("at the far right, where Gamma = +1"),
                    opt("at the far left, where Gamma = -1"),
                    opt("on the outer circle"),
                ),
                "The center corresponds to Gamma = 0 and z = 1, a perfect match.",
            ),
            q(
                "Moving toward the generator (down the line away from the load) does what on a constant-magnitude Gamma circle?",
                (
                    opt("rotates the point clockwise", correct=True),
                    opt("rotates the point counterclockwise"),
                    opt("moves the point toward the center"),
                    opt("moves the point off the chart"),
                ),
                "Moving toward the generator rotates the point clockwise; a half wavelength is one full revolution.",
            ),
            q(
                "Adding shunt elements is easier on which version of the Smith chart?",
                (
                    opt(
                        "the admittance (y = 1/z) chart, the impedance chart rotated 180 degrees",
                        correct=True,
                    ),
                    opt("the impedance chart"),
                    opt("the reactance-only chart"),
                    opt("the logarithmic chart"),
                ),
                "Shunt elements are handled on the admittance chart, which is the impedance chart rotated 180 degrees.",
            ),
        ),
        "Impedance matching: quarter-wave, stub & L-networks": (
            q(
                "A quarter-wave transformer matching a real load RL to Z0 uses a section of impedance equal to what?",
                (
                    opt("the geometric mean, sqrt(Z0 * RL)", correct=True),
                    opt("the arithmetic mean, (Z0 + RL)/2"),
                    opt("the difference, RL - Z0"),
                    opt("the sum, Z0 + RL"),
                ),
                "The quarter-wave section impedance is the geometric mean sqrt(Z0 * RL); for 50 to 100 ohm that is 70.7 ohm.",
            ),
            q(
                "What is the main drawback of the quarter-wave transformer?",
                (
                    opt(
                        "it is only exact at one frequency, so its bandwidth is limited",
                        correct=True,
                    ),
                    opt("it requires lossy resistive elements"),
                    opt("it cannot match real loads"),
                    opt("it only works below 1 GHz"),
                ),
                "A single quarter-wave section is exact only at one frequency and odd harmonics, giving limited bandwidth.",
            ),
            q(
                "How does an L-network match a load using lumped elements?",
                (
                    opt("with two reactive elements, one series and one shunt", correct=True),
                    opt("with two resistors in series"),
                    opt("with a single shorted stub"),
                    opt("with three cascaded transformers"),
                ),
                "An L-network uses two reactive elements (one series, one shunt) to match any load to any source.",
            ),
        ),
        "Waveguides & resonators: modes, cutoff & cavities": (
            q(
                "For a rectangular waveguide of width a, what is the cutoff frequency of the dominant TE10 mode?",
                (
                    opt("c/(2a)", correct=True),
                    opt("c/a"),
                    opt("2c/a"),
                    opt("c/(4a)"),
                ),
                "The dominant TE10 mode cutoff is fc = c/(2a).",
            ),
            q(
                "What happens to a waveguide mode below its cutoff frequency?",
                (
                    opt("it is evanescent and decays instead of propagating", correct=True),
                    opt("it propagates with higher gain"),
                    opt("it converts to a TM mode"),
                    opt("it reflects with VSWR of 1"),
                ),
                "Below cutoff the mode is evanescent, decaying along the guide rather than propagating.",
            ),
            q(
                "Why does a cavity resonator achieve a far higher Q than an LC tank?",
                (
                    opt("the only loss is in the conducting walls", correct=True),
                    opt("it uses superconducting capacitors at room temperature"),
                    opt("it has no resonant frequency"),
                    opt("it radiates energy efficiently"),
                ),
                "A cavity is the microwave version of an LC tank but has very high Q because the only loss is in the conducting walls.",
            ),
        ),
        "Microwave materials & components: connectors, dB & couplers": (
            q(
                "Using the dB anchors in the lesson, a 3 dB power change corresponds to what factor?",
                (
                    opt("a factor of 2", correct=True),
                    opt("a factor of 10"),
                    opt("a factor of 100"),
                    opt("a factor of 1000"),
                ),
                "Handy anchors: 3 dB is x2 power, 10 dB is x10, 20 dB is x100.",
            ),
            q(
                "What does 0 dBm represent?",
                (
                    opt("1 milliwatt", correct=True),
                    opt("1 watt"),
                    opt("0 watts"),
                    opt("1 microwatt"),
                ),
                "dBm references 1 milliwatt, so 0 dBm = 1 mW and +30 dBm = 1 W.",
            ),
            q(
                "What is the role of a directional coupler in a microwave system?",
                (
                    opt(
                        "it samples a known fraction of the forward (and separately the reverse) wave",
                        correct=True,
                    ),
                    opt("it drops power by a fixed dB while staying matched"),
                    opt("it absorbs a wave with no reflection"),
                    opt("it converts coax to waveguide"),
                ),
                "A directional coupler taps a known fraction of the forward wave and separately the reverse, the heart of power and VSWR monitoring.",
            ),
        ),
        "Lab: reflection, VSWR & a Smith-chart trajectory": (
            q(
                "In the lab, how does Gamma change as you move toward the generator down the line?",
                (
                    opt("it rotates clockwise while its magnitude stays constant", correct=True),
                    opt("its magnitude grows while the angle stays fixed"),
                    opt("it moves straight toward the center"),
                    opt("it leaves the unit circle"),
                ),
                "Gamma(d) = GammaL * exp(-j 2 beta d): moving to the source rotates Gamma clockwise at constant magnitude.",
            ),
            q(
                "In the lab, what distance d corresponds to one full turn around the constant-magnitude circle?",
                (
                    opt("half a wavelength", correct=True),
                    opt("a full wavelength"),
                    opt("a quarter wavelength"),
                    opt("an eighth of a wavelength"),
                ),
                "The lab sweeps d from 0 to lambda/2, which is one full revolution on the Smith plane.",
            ),
            q(
                "If you set ZL = 50 (matched) in the lab on a 50 ohm line, what happens to the red trajectory?",
                (
                    opt("it collapses to the center", correct=True),
                    opt("it expands to the outer rim"),
                    opt("it becomes a straight vertical line"),
                    opt("it disappears off the chart"),
                ),
                "With ZL = Z0 the load is matched, Gamma = 0, and the trajectory collapses to the center.",
            ),
        ),
    },
    final=(
        q(
            "Which formula correctly relates VSWR to the magnitude of the reflection coefficient?",
            (
                opt("VSWR = (1 + |Gamma|)/(1 - |Gamma|)", correct=True),
                opt("VSWR = (1 - |Gamma|)/(1 + |Gamma|)"),
                opt("VSWR = |Gamma|/(1 - |Gamma|)"),
                opt("VSWR = 1 + |Gamma|"),
            ),
            "VSWR = (1 + |Gamma|)/(1 - |Gamma|); a perfect match gives Gamma = 0 and VSWR = 1.",
        ),
        q(
            "To match a 100 ohm load to a 50 ohm line, what quarter-wave line impedance is needed?",
            (
                opt("70.7 ohm", correct=True),
                opt("50 ohm"),
                opt("100 ohm"),
                opt("150 ohm"),
            ),
            "The quarter-wave impedance is sqrt(Z0 * RL) = sqrt(50 * 100) = 70.7 ohm.",
        ),
        q(
            "On a Smith chart, what does the outer circle (|Gamma| = 1) represent?",
            (
                opt("pure reactance, total reflection", correct=True),
                opt("a perfect match"),
                opt("an open circuit only"),
                opt("zero reflection"),
            ),
            "The outer circle is |Gamma| = 1, pure reactance with total reflection.",
        ),
        q(
            "Why are microwave power levels and gains expressed in decibels?",
            (
                opt(
                    "because gains add and losses subtract instead of multiplying over huge dynamic ranges",
                    correct=True,
                ),
                opt("because dB values are always integers"),
                opt("because it avoids the need for any reference power"),
                opt("because power cannot be measured linearly at RF"),
            ),
            "The log scale lets an entire RF chain be computed by adding gains and subtracting losses across large dynamic ranges.",
        ),
        q(
            "Above a few GHz, why is a hollow metal waveguide often preferred over coax?",
            (
                opt("it carries energy with very low loss at high power", correct=True),
                opt("it is smaller and cheaper than coax"),
                opt("it works at every frequency with one size"),
                opt("it needs a center conductor for guiding"),
            ),
            "Waveguide is bulky and band-limited but unbeatable for low loss and high power; it has no center conductor.",
        ),
    ),
)
