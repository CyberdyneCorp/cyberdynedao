"""Curated quiz questions for the RFIC & RF Circuit Design - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Noise in RF: noise figure & Friis": (
            q(
                "What does a block's noise figure measure?",
                (
                    opt("How much gain it provides"),
                    opt("How much it degrades the signal-to-noise ratio, in dB", correct=True),
                    opt("Its input impedance"),
                    opt("Its power consumption"),
                ),
                "Noise figure NF = 10*log10(F), where F is the ratio of input SNR to output SNR, quantifying SNR degradation.",
            ),
            q(
                "In the Friis cascade formula, why does the first stage dominate the total noise?",
                (
                    opt("Because the first stage has the most gain after it"),
                    opt(
                        "Because each later stage's noise is divided by the total gain ahead of it",
                        correct=True,
                    ),
                    opt("Because later stages add no noise"),
                    opt("Because noise only exists at the antenna"),
                ),
                "Friis divides each later stage's (F-1) by the product of preceding gains, so the first stage dominates and we lead with a high-gain LNA.",
            ),
            q(
                "What is the approximate thermal noise floor in a 1 Hz bandwidth at room temperature?",
                (
                    opt("-174 dBm/Hz", correct=True),
                    opt("-104 dBm/Hz"),
                    opt("0 dBm/Hz"),
                    opt("+30 dBm/Hz"),
                ),
                "The thermal noise floor is about -174 dBm/Hz; add bandwidth, NF and required SNR to get sensitivity.",
            ),
        ),
        "Linearity: 1-dB compression & IP3": (
            q(
                "What is the 1-dB compression point?",
                (
                    opt("The level where the output power reaches zero"),
                    opt(
                        "The level where gain has dropped 1 dB below its small-signal value",
                        correct=True,
                    ),
                    opt("The frequency where gain peaks"),
                    opt("The noise figure plus 1 dB"),
                ),
                "P1dB marks where gain has compressed 1 dB below small-signal, the top of the usable linear range.",
            ),
            q(
                "On an IP3 plot, what slopes do the fundamental and the third-order product follow?",
                (
                    opt("Both rise at 1 dB/dB"),
                    opt("Fundamental at 1 dB/dB, IM3 at 3 dB/dB", correct=True),
                    opt("Fundamental at 3 dB/dB, IM3 at 1 dB/dB"),
                    opt("Both rise at 2 dB/dB"),
                ),
                "The fundamental rises 1 dB per dB of input while the third-order intermodulation product rises 3 dB per dB; their extrapolated crossing is IP3.",
            ),
            q(
                "Why are third-order intermodulation products especially troublesome?",
                (
                    opt("They appear far outside the band and are easy to filter"),
                    opt(
                        "They fall close to the wanted signal (at 2f1-f2 and 2f2-f1), often in-band and unfilterable",
                        correct=True,
                    ),
                    opt("They only occur at DC"),
                    opt("They increase the noise figure directly"),
                ),
                "IM3 products land at 2f1-f2 and 2f2-f1, very close to the tones and often inside the band, so they cannot be filtered out.",
            ),
        ),
        "The low-noise amplifier (LNA)": (
            q(
                "Why does the LNA receive so much design attention?",
                (
                    opt("It is the last stage and sets output power"),
                    opt(
                        "As the first active stage it dominates the receiver noise figure via Friis",
                        correct=True,
                    ),
                    opt("It consumes the most power on the chip"),
                    opt("It generates the local oscillator"),
                ),
                "By Friis the first stage dominates total noise, so a low-noise, high-gain LNA sets the receiver's noise floor.",
            ),
            q(
                "What is special about inductive-source-degeneration in a common-source LNA?",
                (
                    opt("It adds a large physical resistor for matching"),
                    opt(
                        "It creates a real input resistance from gm and Cgs without adding a noisy resistor",
                        correct=True,
                    ),
                    opt("It eliminates the need for any inductors"),
                    opt("It converts the LNA into an oscillator"),
                ),
                "Source degeneration synthesises a real input resistance from the device parameters, letting noise-match and power-match coincide without a noisy resistor.",
            ),
            q(
                "What is the central trade-off in LNA input design?",
                (
                    opt("Gain vs supply voltage"),
                    opt(
                        "The 50 ohm power match vs the source impedance that gives minimum noise",
                        correct=True,
                    ),
                    opt("Layout area vs clock speed"),
                    opt("DC current vs output swing only"),
                ),
                "The impedance for minimum noise generally differs from 50 ohms, so the LNA must reconcile noise match with power match.",
            ),
        ),
        "Mixers: conversion gain & image": (
            q(
                "What operation does a mixer fundamentally perform?",
                (
                    opt("It adds the RF and LO voltages"),
                    opt(
                        "It multiplies the RF signal by the LO, producing sum and difference frequencies",
                        correct=True,
                    ),
                    opt("It filters out the LO"),
                    opt("It amplifies without changing frequency"),
                ),
                "Multiplying two sinusoids yields sum and difference frequencies; a receiver keeps the difference (IF).",
            ),
            q(
                "What is the image problem in a mixer?",
                (
                    opt("The LO leaks to the antenna"),
                    opt(
                        "Two RF frequencies, at f_LO +/- f_IF, both map to the same IF, so an unwanted image folds onto the signal",
                        correct=True,
                    ),
                    opt("The mixer reflects all incoming power"),
                    opt("The conversion gain is always negative"),
                ),
                "Both f_LO+f_IF and f_LO-f_IF down-convert to the same IF, so the image must be rejected before or during mixing.",
            ),
            q(
                "How do active and passive mixers typically compare?",
                (
                    opt(
                        "Active mixers can have gain; passive mixers have loss but better linearity",
                        correct=True,
                    ),
                    opt("Passive mixers always have higher gain"),
                    opt("Active mixers never add noise"),
                    opt("Both have identical conversion gain"),
                ),
                "Active mixers can provide conversion gain, while passive mixers have conversion loss but generally better linearity.",
            ),
        ),
        "RF oscillators & phase noise": (
            q(
                "How does a cross-coupled LC oscillator sustain oscillation?",
                (
                    opt("By using an external clock source"),
                    opt(
                        "The cross-coupled pair presents a negative resistance that cancels the tank's loss",
                        correct=True,
                    ),
                    opt("By shorting the tank periodically"),
                    opt("By increasing the supply voltage continuously"),
                ),
                "The cross-coupled pair's positive feedback creates a negative resistance that exactly offsets the tank loss, sustaining oscillation at f0.",
            ),
            q(
                "What is phase noise?",
                (
                    opt("The DC offset of the oscillator output"),
                    opt(
                        "Random fluctuation of the oscillator's phase, seen as skirts around the carrier (dBc/Hz)",
                        correct=True,
                    ),
                    opt("The harmonic distortion of the amplifier"),
                    opt("The thermal noise of the bias resistor only"),
                ),
                "Phase noise is random phase jitter producing skirts around the carrier, quoted in dBc/Hz at an offset.",
            ),
            q(
                "According to Leeson, phase noise improves with:",
                (
                    opt("Lower tank Q and lower signal power"),
                    opt("Higher tank Q and higher signal power", correct=True),
                    opt("Higher temperature"),
                    opt("A larger divide ratio"),
                ),
                "Leeson's model shows phase noise falls with higher tank Q and higher carrier power.",
            ),
        ),
        "Receiver & transmitter architectures": (
            q(
                "What characterises a direct-conversion (zero-IF) receiver?",
                (
                    opt("It uses a fixed non-zero intermediate frequency"),
                    opt(
                        "It mixes the signal straight to baseband using I/Q, avoiding an image filter but suffering DC offset and flicker noise",
                        correct=True,
                    ),
                    opt("It requires no local oscillator"),
                    opt("It cannot be integrated on a chip"),
                ),
                "Zero-IF mixes to baseband with I/Q, removing the image filter but introducing DC offsets, flicker noise and I/Q imbalance.",
            ),
            q(
                "What is the main drawback of the superheterodyne architecture?",
                (
                    opt("It has poor selectivity"),
                    opt(
                        "The image frequency must be rejected and the IF filters can be bulky",
                        correct=True,
                    ),
                    opt("It cannot demodulate any signal"),
                    opt("It has no gain"),
                ),
                "Superhet offers excellent selectivity but must deal with the image and needs (often bulky) IF filtering.",
            ),
            q(
                "Why does direct-conversion dominate modern RFICs?",
                (
                    opt("It needs no transistors"),
                    opt(
                        "It integrates onto a single chip without external image filters",
                        correct=True,
                    ),
                    opt("It has zero phase noise"),
                    opt("It works only above 100 GHz"),
                ),
                "Zero-IF is highly integrable, needing no off-chip image filter, which suits single-chip CMOS RFICs.",
            ),
        ),
    },
    final=(
        q(
            "Why does the first stage of a receiver dominate its noise figure?",
            (
                opt("Because it is physically the largest"),
                opt(
                    "Because Friis divides each later stage's noise by the gain ahead of it",
                    correct=True,
                ),
                opt("Because only the first stage has thermal noise"),
                opt("Because the antenna adds no noise"),
            ),
            "Friis shows later-stage noise is suppressed by preceding gain, so the front-end LNA sets the noise floor.",
        ),
        q(
            "Which relationship between P1dB and IP3 is a common rule of thumb?",
            (
                opt("IP3 is about 10 dB below P1dB"),
                opt("IP3 is about P1dB + 10 dB", correct=True),
                opt("IP3 equals P1dB"),
                opt("IP3 is unrelated to P1dB"),
            ),
            "A common rule of thumb is IP3 is roughly P1dB + 10 dB.",
        ),
        q(
            "What does inductive source degeneration achieve in an LNA?",
            (
                opt("It adds gain at DC"),
                opt(
                    "A real input resistance from gm and Cgs, so noise match and power match can coincide without a noisy resistor",
                    correct=True,
                ),
                opt("It removes the need for a tank load"),
                opt("It increases the supply current tenfold"),
            ),
            "Source degeneration synthesises a real input resistance from device parameters, aligning the noise and power matches cleanly.",
        ),
        q(
            "An RF mixer translates frequency by:",
            (
                opt("Adding the LO and RF voltages"),
                opt(
                    "Multiplying RF by the LO, producing sum and difference frequencies",
                    correct=True,
                ),
                opt("Dividing the RF frequency by N"),
                opt("Integrating the RF signal"),
            ),
            "Mixing multiplies RF and LO, generating sum and difference tones; the receiver keeps the difference (IF).",
        ),
        q(
            "What single specification most distinguishes a good RF oscillator?",
            (
                opt("Its DC current"),
                opt("Its phase noise (dBc/Hz at an offset)", correct=True),
                opt("Its package size"),
                opt("Its input impedance"),
            ),
            "Phase noise is the defining oscillator spec, improving with higher tank Q and signal power.",
        ),
        q(
            "Which is a true contrast between superheterodyne and zero-IF receivers?",
            (
                opt("Zero-IF needs a bulky image filter; superhet does not"),
                opt(
                    "Superhet uses a non-zero IF and faces the image; zero-IF goes to baseband but faces DC offset and flicker noise",
                    correct=True,
                ),
                opt("Both place the signal at the same IF"),
                opt("Superhet cannot be built with mixers"),
            ),
            "Superhet uses an IF (image problem, bulky filters); zero-IF mixes to baseband (DC offset, flicker, I/Q imbalance) but integrates well.",
        ),
    ),
)
