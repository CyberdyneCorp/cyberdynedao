"""Curated quiz questions for the Filter Design - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What a filter is & the four response types": (
            q(
                "Which filter type passes a band of frequencies around a centre frequency and attenuates both below and above it?",
                (
                    opt("Low-pass"),
                    opt("High-pass"),
                    opt("Band-pass", correct=True),
                    opt("All-pass"),
                ),
                "A band-pass passes a band around a centre frequency and attenuates frequencies on both sides.",
            ),
            q(
                "What does a band-stop (notch) filter do?",
                (
                    opt("Passes only the lowest frequencies"),
                    opt("Rejects a narrow band of frequencies, e.g. 50/60 Hz hum", correct=True),
                    opt("Passes every frequency equally"),
                    opt("Passes only the highest frequencies"),
                ),
                "A band-stop / notch filter rejects a narrow band, such as mains hum, while passing the rest.",
            ),
            q(
                "A high-pass filter is best described as which of the following?",
                (
                    opt("It passes low frequencies and blocks high ones"),
                    opt(
                        "It passes high frequencies and blocks low ones, useful for DC blocking",
                        correct=True,
                    ),
                    opt("It rejects a band around a centre frequency"),
                    opt("It has no effect on the spectrum"),
                ),
                "A high-pass passes high frequencies and blocks low ones, used for DC blocking and rumble removal.",
            ),
        ),
        "Decibels, cutoff & roll-off: reading a Bode plot": (
            q(
                "At the cutoff frequency, the magnitude has fallen to what level relative to the passband?",
                (
                    opt("0 dB (no change)"),
                    opt("−3 dB, i.e. about 0.707 of the passband value (half power)", correct=True),
                    opt("−20 dB"),
                    opt("−6 dB, i.e. 0.5 of the passband value"),
                ),
                "Cutoff is the −3 dB point, where the magnitude is 1/√2 ≈ 0.707 of its passband value (half power).",
            ),
            q(
                "What is the roll-off of a first-order filter?",
                (
                    opt("−20 dB/decade (−6 dB/octave)", correct=True),
                    opt("−40 dB/decade"),
                    opt("0 dB/decade"),
                    opt("−60 dB/octave"),
                ),
                "A first-order filter rolls off at −20 dB/decade, equivalently −6 dB/octave; each extra order adds another −20.",
            ),
            q(
                "The decibel value of a voltage ratio is given by which expression?",
                (
                    opt("10 log10 of the ratio"),
                    opt("20 log10 of the ratio", correct=True),
                    opt("the ratio squared"),
                    opt("the natural log of the ratio"),
                ),
                "For a voltage ratio, |H| in dB = 20 log10 |H|; a gain of 0.707 is −3 dB.",
            ),
        ),
        "Passive first-order filters: RC & RL": (
            q(
                "For an RC low-pass with output across the capacitor, what is the cutoff frequency?",
                (
                    opt("ωc = RC"),
                    opt("ωc = 1/RC", correct=True),
                    opt("ωc = R/C"),
                    opt("ωc = 1/(R + C)"),
                ),
                "The RC low-pass has ωc = 1/RC; for the RL version it is ωc = R/L.",
            ),
            q(
                "What is the phase of a first-order RC low-pass exactly at its cutoff frequency?",
                (
                    opt("0°"),
                    opt("−45°", correct=True),
                    opt("−90°"),
                    opt("+45°"),
                ),
                "The phase lags from 0° toward −90° and passes through exactly −45° at the cutoff.",
            ),
            q(
                "How can the same RC network be turned from a low-pass into a high-pass?",
                (
                    opt("By increasing the resistor value tenfold"),
                    opt(
                        "By tapping the output across the other element (the resistor instead of the capacitor)",
                        correct=True,
                    ),
                    opt("By adding a second capacitor in parallel"),
                    opt("It cannot be turned into a high-pass"),
                ),
                "Swapping which element you take the output across turns a low-pass into a high-pass.",
            ),
        ),
        "Second-order RLC filters: resonance & Q": (
            q(
                "What does the quality factor Q control in a second-order RLC filter?",
                (
                    opt("The DC gain only"),
                    opt("How peaked the response is near the natural frequency", correct=True),
                    opt("The sign of the output"),
                    opt("The number of poles"),
                ),
                "Q sets how peaked the response is near ω₀: high Q gives a tall resonant bump, low Q a smooth curve.",
            ),
            q(
                "What is the natural frequency ω₀ of a series RLC circuit?",
                (
                    opt("ω₀ = 1/(RC)"),
                    opt("ω₀ = 1/√(LC)", correct=True),
                    opt("ω₀ = R/L"),
                    opt("ω₀ = √(LC)"),
                ),
                "The natural frequency is ω₀ = 1/√(LC).",
            ),
            q(
                "A second-order low-pass with Q = 0.707 is described as which of the following?",
                (
                    opt("Maximally flat (Butterworth), with no peak", correct=True),
                    opt("Overdamped with two real poles"),
                    opt("A sharp, narrow band-pass"),
                    opt("Unstable"),
                ),
                "Q = 0.707 gives the maximally flat (Butterworth) response with the flattest passband and no peak.",
            ),
        ),
        "Reading a frequency-response specification": (
            q(
                "Which four numbers define a basic filter specification template?",
                (
                    opt("Gain, phase, slew rate and offset"),
                    opt("Passband edge and ripple, stopband edge and attenuation", correct=True),
                    opt("Resistance, capacitance, inductance and frequency"),
                    opt("Order, topology, family and tolerance"),
                ),
                "A spec is set by the passband edge and max ripple plus the stopband edge and min attenuation.",
            ),
            q(
                "The transition band sits between which two frequencies?",
                (
                    opt("Between DC and the passband edge"),
                    opt("Between the passband edge ωp and the stopband edge ωs", correct=True),
                    opt("Between the stopband edge and infinity"),
                    opt("Between two passbands"),
                ),
                "The transition band lies between the passband edge ωp and the stopband edge ωs.",
            ),
            q(
                "What happens to the required filter order as you demand a narrower transition band?",
                (
                    opt("The order can be lowered"),
                    opt("The order stays the same"),
                    opt("A higher order is needed", correct=True),
                    opt("Order is unrelated to the transition band"),
                ),
                "The narrower the transition band you demand, the higher the filter order required.",
            ),
        ),
        "The transfer function H(s) of a filter": (
            q(
                "In a transfer function H(s) = N(s)/D(s), what are the roots of the denominator D(s)?",
                (
                    opt("The zeros, which the filter kills"),
                    opt(
                        "The poles, which set resonances and must be in the left half-plane for stability",
                        correct=True,
                    ),
                    opt("The cutoff frequencies only"),
                    opt("The passband gain"),
                ),
                "The denominator roots are the poles; they set the resonances and must lie in the left half-plane for stability.",
            ),
            q(
                "How is the steady-state frequency response read from H(s)?",
                (
                    opt("Set s = 0"),
                    opt("Evaluate H on the imaginary axis, s = jω", correct=True),
                    opt("Take the derivative of H"),
                    opt("Set s to infinity"),
                ),
                "The frequency response H(jω) is obtained by evaluating H(s) on the imaginary axis, s = jω.",
            ),
            q(
                "The order n of a filter (the number of poles) fixes which property?",
                (
                    opt("The DC gain"),
                    opt("The ultimate roll-off, −20n dB/decade", correct=True),
                    opt("The passband ripple"),
                    opt("The input impedance"),
                ),
                "The order n is the number of poles and fixes the ultimate roll-off at −20n dB/decade.",
            ),
        ),
    },
    final=(
        q(
            "Which response type passes high frequencies while blocking low ones?",
            (
                opt("Low-pass"),
                opt("High-pass", correct=True),
                opt("Band-pass"),
                opt("Band-stop"),
            ),
            "A high-pass passes high frequencies and blocks low ones.",
        ),
        q(
            "A gain of 0.707 corresponds to how many decibels, and what point is that on a response?",
            (
                opt("−6 dB; the half-amplitude point"),
                opt("−3 dB; the cutoff (half-power) point", correct=True),
                opt("0 dB; the passband"),
                opt("−20 dB; the stopband"),
            ),
            "A ratio of 0.707 is −3 dB, which marks the cutoff (half-power) frequency.",
        ),
        q(
            "What is the cutoff frequency of a passive RC low-pass filter?",
            (
                opt("ωc = RC"),
                opt("ωc = 1/RC", correct=True),
                opt("ωc = R/C"),
                opt("ωc = C/R"),
            ),
            "The RC low-pass cutoff is ωc = 1/RC.",
        ),
        q(
            "In a second-order RLC filter, which statement about Q is correct?",
            (
                opt("Higher Q gives a flatter, less peaked response"),
                opt(
                    "Higher Q gives a more peaked response near ω₀ and a sharper filter",
                    correct=True,
                ),
                opt("Q has no effect on the shape of the response"),
                opt("Q sets the DC gain"),
            ),
            "Higher Q yields a more peaked response near the natural frequency and a sharper filter.",
        ),
        q(
            "In a filter specification, what does the stopband attenuation As describe?",
            (
                opt("How much the passband gain may wobble"),
                opt("The minimum amount unwanted frequencies must be pushed down", correct=True),
                opt("The width of the passband"),
                opt("The cutoff frequency"),
            ),
            "As is the minimum stopband attenuation: how far down unwanted frequencies must be pushed.",
        ),
        q(
            "For a transfer function H(s), where must the poles lie for the filter to be stable?",
            (
                opt("On the imaginary axis"),
                opt("In the left half of the s-plane (negative real part)", correct=True),
                opt("In the right half of the s-plane"),
                opt("At the origin"),
            ),
            "Poles must lie in the left half-plane (negative real part) for the filter to be stable.",
        ),
    ),
)
