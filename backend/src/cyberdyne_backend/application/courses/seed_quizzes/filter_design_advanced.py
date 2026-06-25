"""Curated quiz questions for the Filter Design - Advanced course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Approximation theory: Butterworth, Chebyshev, elliptic, Bessel": (
            q(
                "Which approximation family has a maximally flat passband and a monotonic response?",
                (
                    opt("Chebyshev I"),
                    opt("Butterworth", correct=True),
                    opt("Elliptic"),
                    opt("Chebyshev II"),
                ),
                "Butterworth is maximally flat in the passband and monotonic, with a gentle knee.",
            ),
            q(
                "What does an elliptic (Cauer) filter trade to achieve the steepest transition for a given order?",
                (
                    opt("A flat stopband only"),
                    opt("Ripple in both the passband and stopband, plus worse phase", correct=True),
                    opt("Infinite order"),
                    opt("Zero gain everywhere"),
                ),
                "Elliptic filters allow ripple in both bands (and worse phase) to get the steepest transition per order.",
            ),
            q(
                "Which family is chosen for maximally flat group delay (linear phase) so pulse shapes pass undistorted?",
                (
                    opt("Bessel", correct=True),
                    opt("Elliptic"),
                    opt("Chebyshev I"),
                    opt("Butterworth"),
                ),
                "Bessel sacrifices steepness for maximally flat group delay, preserving pulse shapes.",
            ),
        ),
        "Pole-zero placement & the s-plane": (
            q(
                "On what locus do the poles of a Butterworth filter lie?",
                (
                    opt("On a straight vertical line"),
                    opt("On a circle of radius ωc, equally spaced", correct=True),
                    opt("On the real axis only"),
                    opt("At the origin"),
                ),
                "Butterworth poles lie equally spaced on a circle of radius ωc; that even spacing gives the flat passband.",
            ),
            q(
                "What do zeros placed on the jω axis create in a response?",
                (
                    opt("Resonant peaks"),
                    opt("Transmission nulls (notches)", correct=True),
                    opt("DC gain"),
                    opt("Instability"),
                ),
                "Zeros on the jω axis create transmission nulls; elliptic filters use finite zeros to crush the stopband.",
            ),
            q(
                "How is a conjugate pole pair turned into a circuit?",
                (
                    opt("It is discarded"),
                    opt(
                        "It maps to a second-order section whose ω₀ and Q are read from the pole location",
                        correct=True,
                    ),
                    opt("It becomes a first-order RC stage"),
                    opt("It sets only the DC gain"),
                ),
                "Each conjugate pole pair maps to a second-order section, with ω₀ and Q read directly off the pole location.",
            ),
        ),
        "Switched-capacitor filters": (
            q(
                "What is the equivalent resistance of a capacitor C switched at clock frequency f_clk?",
                (
                    opt("R = f_clk·C"),
                    opt("R = 1/(f_clk·C)", correct=True),
                    opt("R = C/f_clk"),
                    opt("R = f_clk/C"),
                ),
                "A switched capacitor emulates a resistor of value R = 1/(f_clk·C).",
            ),
            q(
                "Why are switched-capacitor filters well suited to integrated circuits?",
                (
                    opt("Because accurate resistors are easy to fabricate on silicon"),
                    opt(
                        "Because the cutoff depends on a precise capacitor ratio and the clock, both good on silicon",
                        correct=True,
                    ),
                    opt("Because they need no clock"),
                    opt("Because they are immune to aliasing"),
                ),
                "Capacitor ratios and clocks are precise on silicon, so the cutoff (∝ f_clk·C1/C2) is accurate and digitally tunable.",
            ),
            q(
                "What signal-processing caveat comes with switched-capacitor filters?",
                (
                    opt("They cannot have gain"),
                    opt(
                        "The signal is sampled, so anti-alias and reconstruction filtering are needed",
                        correct=True,
                    ),
                    opt("Their cutoff cannot be changed"),
                    opt("They only work at DC"),
                ),
                "Because the signal is sampled, switched-capacitor filters need anti-alias and reconstruction filtering, and have clock noise.",
            ),
        ),
        "From analog prototype to digital: the bilinear transform & IIR": (
            q(
                "What does the bilinear transform substitute for s?",
                (
                    opt("s ← z"),
                    opt("s ← (2/T)·(1 − z⁻¹)/(1 + z⁻¹)", correct=True),
                    opt("s ← z²"),
                    opt("s ← 1/z"),
                ),
                "The bilinear transform substitutes s ← (2/T)(1 − z⁻¹)/(1 + z⁻¹), mapping the left half-plane into the unit circle.",
            ),
            q(
                "Why must you pre-warp the critical frequency before applying the bilinear transform?",
                (
                    opt("Because the transform adds noise"),
                    opt(
                        "Because the transform warps frequencies nonlinearly (ω_a = (2/T)tan(ω_d/2))",
                        correct=True,
                    ),
                    opt("Because z must be negative"),
                    opt("Because IIR filters cannot be stable otherwise"),
                ),
                "The bilinear mapping warps frequencies via a tangent relation, so the critical frequency is pre-warped to land correctly.",
            ),
            q(
                "What kind of digital filter does the bilinear transform of an analog prototype produce?",
                (
                    opt("An FIR filter with linear phase"),
                    opt("An IIR filter described by a recursive difference equation", correct=True),
                    opt("A purely analog filter"),
                    opt("A filter with no feedback"),
                ),
                "Transforming an analog H(s) gives an IIR filter, a recursive difference equation in past inputs and outputs.",
            ),
        ),
        "A complete design example: spec to components": (
            q(
                "In the worked example, which family is chosen and why?",
                (
                    opt("Bessel, because steepness is the priority"),
                    opt(
                        "Butterworth, because phase is not critical and a clean passband with a steep-enough edge is wanted",
                        correct=True,
                    ),
                    opt("Elliptic, because ripple is desired in the passband"),
                    opt("Chebyshev II, because stopband ripple is required"),
                ),
                "With phase uncritical and a clean passband wanted, Butterworth is chosen for the example.",
            ),
            q(
                "What is the universal filter-design recipe shown by the example?",
                (
                    opt("Components first, then spec"),
                    opt("Spec → family → order → topology → components → verify", correct=True),
                    opt("Topology → spec → verify"),
                    opt("Pick any op-amp and adjust later"),
                ),
                "The example follows spec → family → order → topology → components → verify.",
            ),
            q(
                "Why is the 4th-order filter realised as two Sallen-Key sections with different Q values?",
                (
                    opt("To make each section identical"),
                    opt(
                        "Because the two Butterworth pole pairs require different Q values (e.g. 0.541 and 1.307)",
                        correct=True,
                    ),
                    opt("To reduce the order to 2"),
                    opt("Because Sallen-Key cannot do low-pass"),
                ),
                "The 4th-order Butterworth has two pole pairs with distinct Q values (0.541 and 1.307), one per Sallen-Key section.",
            ),
        ),
        "Practical issues: noise, tolerance & GBW limits": (
            q(
                "What is the dominant source of resistor noise in a filter?",
                (
                    opt("Quantisation noise"),
                    opt(
                        "Thermal (Johnson) noise, proportional to resistance and bandwidth",
                        correct=True,
                    ),
                    opt("Clock feedthrough"),
                    opt("Aliasing"),
                ),
                "Resistors add thermal (Johnson) noise proportional to R and bandwidth; high-Q stages amplify it near ω₀.",
            ),
            q(
                "How does a real op-amp's finite gain-bandwidth (GBW) affect a filter stage?",
                (
                    opt("It has no effect at any frequency"),
                    opt(
                        "As f₀ approaches GBW, the realised ω₀ and Q drift from their design values",
                        correct=True,
                    ),
                    opt("It increases the order automatically"),
                    opt("It removes all noise"),
                ),
                "When f₀ becomes a non-negligible fraction of GBW, the stage's actual ω₀ and Q drift away from design.",
            ),
            q(
                "Which is a sound rule of thumb for choosing an op-amp for a filter stage?",
                (
                    opt("Keep GBW well above Q²·f₀", correct=True),
                    opt("Keep GBW below f₀"),
                    opt("Make GBW exactly equal to f₀"),
                    opt("GBW does not matter"),
                ),
                "A useful guideline is to keep the op-amp GBW well above Q²·f₀ so the stage holds its design values.",
            ),
        ),
    },
    final=(
        q(
            "Which family gives the steepest transition for a given order?",
            (
                opt("Butterworth"),
                opt("Bessel"),
                opt("Elliptic (Cauer), with ripple in both bands", correct=True),
                opt("First-order RC"),
            ),
            "Elliptic filters achieve the steepest transition per order by allowing ripple in both bands.",
        ),
        q(
            "Where do Butterworth poles lie in the s-plane?",
            (
                opt("On the imaginary axis"),
                opt("Equally spaced on a circle in the left half-plane", correct=True),
                opt("On the real axis at the origin"),
                opt("In the right half-plane"),
            ),
            "Butterworth poles are equally spaced on a circle, in the left half-plane for stability.",
        ),
        q(
            "In a switched-capacitor filter, the cutoff frequency depends mainly on what?",
            (
                opt("Absolute resistor values"),
                opt("A capacitor ratio and the clock frequency", correct=True),
                opt("The supply voltage"),
                opt("The op-amp offset"),
            ),
            "The cutoff is ωc ∝ f_clk·(C1/C2), depending on a capacitor ratio and the clock, making it digitally tunable.",
        ),
        q(
            "The bilinear transform maps the stable region of the s-plane to which region of the z-plane?",
            (
                opt("The outside of the unit circle"),
                opt("The inside of the unit circle", correct=True),
                opt("The real axis only"),
                opt("The origin"),
            ),
            "It maps the left half s-plane into the inside of the unit circle, so a stable analog filter stays stable.",
        ),
        q(
            "What is the correct order of the universal filter-design recipe?",
            (
                opt("Components → topology → spec → verify"),
                opt("Spec → family → order → topology → components → verify", correct=True),
                opt("Verify → spec → components"),
                opt("Family → components → spec"),
            ),
            "Design proceeds spec → family → order → topology → components → verify.",
        ),
        q(
            "Which practical limit causes a stage's realised ω₀ and Q to drift as its design frequency rises?",
            (
                opt("Johnson noise"),
                opt("Component tolerance only"),
                opt("The op-amp's finite gain-bandwidth (GBW)", correct=True),
                opt("Clock feedthrough"),
            ),
            "As f₀ approaches the op-amp's GBW, the available loop gain falls and the stage's ω₀ and Q drift.",
        ),
    ),
)
