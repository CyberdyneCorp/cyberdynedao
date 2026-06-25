"""Curated quiz questions for the Data Converters & PLLs - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Sampling & the Nyquist theorem": (
            q(
                "What does the Nyquist-Shannon sampling theorem require for perfect reconstruction?",
                (
                    opt("The sample rate must equal the highest signal frequency"),
                    opt(
                        "The sample rate must be greater than twice the highest signal frequency",
                        correct=True,
                    ),
                    opt("The sample rate must be a multiple of the signal amplitude"),
                    opt("The signal must be perfectly periodic"),
                ),
                "Perfect reconstruction needs f_s greater than 2*f_max; the threshold f_s/2 is the Nyquist frequency.",
            ),
            q(
                "What is aliasing?",
                (
                    opt("Rounding each sample to the nearest level"),
                    opt(
                        "Energy above f_s/2 folding back to a lower frequency, indistinguishable from a real low tone",
                        correct=True,
                    ),
                    opt("The droop of the reconstruction filter at high frequencies"),
                    opt("Timing uncertainty in the sampling clock edge"),
                ),
                "When sampled too slowly, energy above the Nyquist frequency folds down and masquerades as a lower frequency.",
            ),
            q(
                "How do you prevent aliasing?",
                (
                    opt("Add more bits of resolution"),
                    opt("Increase the hold capacitor"),
                    opt(
                        "Place an anti-alias low-pass filter before the sampler",
                        correct=True,
                    ),
                    opt("Use an R-2R ladder in the DAC"),
                ),
                "An anti-alias filter removes energy above f_s/2 before sampling, since aliases cannot be removed afterward.",
            ),
        ),
        "Quantization, resolution & quantization noise": (
            q(
                "What is the size of one LSB for an N-bit converter over full-scale range V_FS?",
                (
                    opt("V_FS times 2^N"),
                    opt("V_FS divided by 2^N", correct=True),
                    opt("V_FS divided by N"),
                    opt("2^N divided by V_FS"),
                ),
                "One LSB is the step between levels, Delta = V_FS / 2^N.",
            ),
            q(
                "Approximately how much does each extra bit add to a converter's SQNR?",
                (
                    opt("About 1.76 dB"),
                    opt("About 3 dB"),
                    opt("About 6 dB", correct=True),
                    opt("About 20 dB"),
                ),
                "SQNR is about 6.02*N + 1.76 dB, so each additional bit buys roughly 6 dB of dynamic range.",
            ),
            q(
                "Quantization error of a converter is usually modeled as what?",
                (
                    opt("A constant DC offset"),
                    opt(
                        "Uniform noise in the range +/- Delta/2 with power Delta^2/12",
                        correct=True,
                    ),
                    opt("A pure sinusoid at the Nyquist frequency"),
                    opt("Gaussian noise with infinite variance"),
                ),
                "Rounding error lies in [-Delta/2, +Delta/2] and is treated as uniform noise with power Delta^2/12.",
            ),
        ),
        "DAC fundamentals & architectures": (
            q(
                "What is the main advantage of the R-2R ladder DAC over a binary-weighted DAC?",
                (
                    opt("It is the only architecture that can be monotonic"),
                    opt(
                        "It needs only two distinct resistor values, easing matching and scaling",
                        correct=True,
                    ),
                    opt("It requires no switches"),
                    opt("It has zero glitch energy by construction"),
                ),
                "The R-2R ladder uses only R and 2R values, so matching and scalability are far better than scaling one resistor per bit.",
            ),
            q(
                "Why is a binary-weighted resistor DAC impractical for many bits?",
                (
                    opt("It is too slow to settle"),
                    opt(
                        "The required spread of resistor values becomes huge and hard to match",
                        correct=True,
                    ),
                    opt("It cannot represent the MSB"),
                    opt("It needs a separate sample-and-hold per bit"),
                ),
                "Binary weighting scales resistors as R, 2R, 4R...; for many bits that spread is impractical and poorly matched.",
            ),
            q(
                "What does a DAC do?",
                (
                    opt("Maps an analog voltage to the nearest digital code"),
                    opt("Filters out frequencies above the Nyquist rate"),
                    opt(
                        "Turns an N-bit digital code into an analog voltage or current",
                        correct=True,
                    ),
                    opt("Holds the input steady while the ADC resolves bits"),
                ),
                "A DAC converts a digital code to an analog output; the ADC does the reverse.",
            ),
        ),
        "ADC fundamentals & key specs": (
            q(
                "What does ENOB measure?",
                (
                    opt("The nominal number of bits printed on the datasheet"),
                    opt(
                        "The effective resolution after all noise and distortion are accounted for",
                        correct=True,
                    ),
                    opt("The number of comparators in the converter"),
                    opt("The size of one LSB in volts"),
                ),
                "ENOB = (SINAD - 1.76)/6.02 gives the real resolution once noise and distortion are included.",
            ),
            q(
                "A DNL worse than -1 LSB indicates what?",
                (
                    opt("Excellent linearity"),
                    opt("A missing code", correct=True),
                    opt("A high SFDR"),
                    opt("That the converter is oversampling"),
                ),
                "DNL below -1 LSB means a code is so narrow it never appears: a missing code.",
            ),
            q(
                "What does SFDR (spurious-free dynamic range) describe?",
                (
                    opt("The DC offset of the converter"),
                    opt("The running sum of DNL across codes"),
                    opt(
                        "The distance from the signal to the largest spur in the spectrum",
                        correct=True,
                    ),
                    opt("The settling time of the sample-and-hold"),
                ),
                "SFDR is the level difference between the signal and the tallest spur (often a harmonic).",
            ),
        ),
        "The sample-and-hold": (
            q(
                "Why does an ADC need a sample-and-hold?",
                (
                    opt("To amplify the signal above full scale"),
                    opt(
                        "To freeze the input steady while the ADC resolves the code",
                        correct=True,
                    ),
                    opt("To remove aliasing before sampling"),
                    opt("To convert the code back to a voltage"),
                ),
                "The S/H holds the value still during conversion so the input is not moving while bits are decided.",
            ),
            q(
                "In the hold phase of a sample-and-hold, what happens?",
                (
                    opt("The switch closes and the capacitor tracks the input"),
                    opt(
                        "The switch opens and the capacitor holds the last value steady",
                        correct=True,
                    ),
                    opt("The ADC code is converted back to analog"),
                    opt("The anti-alias filter is bypassed"),
                ),
                "During hold the switch opens, isolating the capacitor so it holds the sampled voltage for the ADC.",
            ),
            q(
                "Which of these is a real sample-and-hold error?",
                (
                    opt("Missing codes"),
                    opt("Aperture jitter from clock-edge uncertainty", correct=True),
                    opt("Sinc droop of the reconstruction filter"),
                    opt("Thermometer-to-binary encoding errors"),
                ),
                "Aperture jitter, droop and charge injection are S/H errors; aperture jitter is uncertainty in the sampling instant.",
            ),
        ),
        "Analog vs digital domains & anti-alias filtering": (
            q(
                "Where must the anti-alias filter be placed?",
                (
                    opt("After the ADC, in the digital domain"),
                    opt("Before the sampler, in the analog domain", correct=True),
                    opt("Inside the DAC reconstruction path only"),
                    opt("It can be placed anywhere in the chain"),
                ),
                "Aliases cannot be removed once sampled, so the AAF must attenuate above f_s/2 before the sampler.",
            ),
            q(
                "What is the benefit of oversampling for the anti-alias filter?",
                (
                    opt("It removes the need for any filter at all"),
                    opt(
                        "It pushes the Nyquist edge well above the band, relaxing the filter's sharpness",
                        correct=True,
                    ),
                    opt("It increases quantization noise power"),
                    opt("It eliminates the need for a sample-and-hold"),
                ),
                "Sampling faster moves f_s/2 above the band of interest, so the anti-alias filter can roll off gently.",
            ),
            q(
                "Which statement about the analog and digital domains is correct?",
                (
                    opt("Both are discrete in time and amplitude"),
                    opt("Both are continuous in time and amplitude"),
                    opt(
                        "Analog is continuous in time and amplitude; digital is discrete in both",
                        correct=True,
                    ),
                    opt("Analog is discrete and digital is continuous"),
                ),
                "Analog signals are continuous in time and amplitude; digital signals are discrete in both, with converters as the gateways.",
            ),
        ),
    },
    final=(
        q(
            "A 14-bit ADC achieves SINAD of 80 dB. Roughly what is its ENOB?",
            (
                opt("About 14 bits"),
                opt("About 13 bits", correct=True),
                opt("About 10 bits"),
                opt("About 6 bits"),
            ),
            "ENOB = (80 - 1.76)/6.02 is about 13 bits, below the nominal 14.",
        ),
        q(
            "Why must the sample rate exceed twice the highest signal frequency?",
            (
                opt("To reduce quantization noise"),
                opt("To improve the SFDR"),
                opt(
                    "To avoid aliasing, where high frequencies fold back as indistinguishable low ones",
                    correct=True,
                ),
                opt("To reduce charge injection in the switch"),
            ),
            "Sampling above the Nyquist rate prevents aliasing; otherwise high frequencies fold down irrecoverably.",
        ),
        q(
            "Which DAC architecture uses only two resistor values repeated in a ladder?",
            (
                opt("Binary-weighted DAC"),
                opt("R-2R ladder DAC", correct=True),
                opt("Flash DAC"),
                opt("Sigma-delta DAC"),
            ),
            "The R-2R ladder uses just R and 2R values, giving good matching and scalability.",
        ),
        q(
            "What is the role of the sample-and-hold in an ADC?",
            (
                opt("It removes harmonics from the spectrum"),
                opt("It converts codes back into voltages"),
                opt(
                    "It holds the input steady so the converter resolves a stationary value",
                    correct=True,
                ),
                opt("It oversamples to relax the anti-alias filter"),
            ),
            "The S/H freezes the input during conversion so the value is not moving as the bits are decided.",
        ),
        q(
            "Each additional bit of resolution improves the best-case SQNR by approximately how much?",
            (
                opt("1.76 dB"),
                opt("3 dB"),
                opt("6 dB", correct=True),
                opt("12 dB"),
            ),
            "From SQNR = 6.02*N + 1.76 dB, each extra bit adds about 6 dB.",
        ),
        q(
            "What does the anti-alias filter do, and why can't aliasing be fixed later?",
            (
                opt("It adds gain; aliasing is removed digitally after the ADC"),
                opt(
                    "It attenuates energy above f_s/2 before sampling; once aliased, frequencies are indistinguishable and unrecoverable",
                    correct=True,
                ),
                opt("It compensates the sinc droop; aliasing is a DAC-only issue"),
                opt("It increases resolution; aliasing only affects DC"),
            ),
            "The AAF rejects above-Nyquist energy before sampling because after folding, those frequencies cannot be separated from real low ones.",
        ),
    ),
)
