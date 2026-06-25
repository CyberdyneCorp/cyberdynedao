"""Curated quiz questions for the Filter Design - Intermediate course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Op-amp basics for filters": (
            q(
                "Under negative feedback, what do the ideal op-amp's golden rules state?",
                (
                    opt("Large current flows into the inputs and the output is fixed"),
                    opt(
                        "No current flows into the inputs and the two inputs sit at the same voltage",
                        correct=True,
                    ),
                    opt("The inputs are always 90° out of phase"),
                    opt("The output equals the supply rail"),
                ),
                "With negative feedback the inputs draw no current and sit at the same voltage (the virtual short).",
            ),
            q(
                "What is the gain of an inverting amplifier?",
                (
                    opt("1 + Rf/Rg"),
                    opt("−Rf/Rin", correct=True),
                    opt("Rin/Rf"),
                    opt("Rf·Rin"),
                ),
                "The inverting amplifier gain is −Rf/Rin, and its '−' input is a virtual ground.",
            ),
            q(
                "Why does buffering by the op-amp let you cascade active filter stages freely?",
                (
                    opt("Because each stage loads the previous one heavily"),
                    opt(
                        "Because the low output impedance means a stage does not load the one before it",
                        correct=True,
                    ),
                    opt("Because op-amps remove all noise"),
                    opt("Because passive filters cannot be cascaded at all"),
                ),
                "The op-amp's low output impedance buffers the signal, so stages can cascade without loading each other.",
            ),
        ),
        "Active first-order filters": (
            q(
                "How do you turn an inverting amplifier into an active first-order low-pass?",
                (
                    opt("Add a capacitor in series with the input resistor"),
                    opt("Put a capacitor across the feedback resistor Rf", correct=True),
                    opt("Remove the feedback resistor"),
                    opt("Ground the inverting input"),
                ),
                "A capacitor across Rf lowers the feedback impedance at high frequency, giving a low-pass roll-off.",
            ),
            q(
                "What advantage does an active first-order filter have over a passive RC filter?",
                (
                    opt(
                        "It can provide passband gain and filtering at the same time", correct=True
                    ),
                    opt("It rolls off at −40 dB/decade with one stage"),
                    opt("It needs no power supply"),
                    opt("It has zero noise"),
                ),
                "Unlike a passive RC, the active stage provides passband gain together with filtering, and is buffered.",
            ),
            q(
                "What is the cutoff frequency of the active low-pass with feedback Rf and Cf?",
                (
                    opt("ωc = Rf·Cf"),
                    opt("ωc = 1/(Rf·Cf)", correct=True),
                    opt("ωc = Rin·Cf"),
                    opt("ωc = 1/Rin"),
                ),
                "The cutoff is set by the feedback network: ωc = 1/(Rf·Cf).",
            ),
        ),
        "Sallen-Key second-order LP & HP": (
            q(
                "What makes the Sallen-Key topology attractive for second-order active filters?",
                (
                    opt("It needs an inductor for resonance"),
                    opt(
                        "One op-amp, two resistors and two capacitors set ω₀ and Q with no inductor",
                        correct=True,
                    ),
                    opt("It only works at very high Q"),
                    opt("It cannot provide a Butterworth response"),
                ),
                "Sallen-Key realises a second-order response with one op-amp and RC parts, with Q set by component ratios and no inductor.",
            ),
            q(
                "How is a Sallen-Key low-pass converted into a high-pass?",
                (
                    opt("By doubling the op-amp gain"),
                    opt("By swapping the positions of the resistors and capacitors", correct=True),
                    opt("By adding a second op-amp"),
                    opt("By grounding the output"),
                ),
                "Swapping the R and C positions turns the same Sallen-Key topology into a high-pass.",
            ),
            q(
                "Which design Q gives a maximally flat (Butterworth) Sallen-Key response?",
                (
                    opt("Q = 0.5"),
                    opt("Q = 0.707", correct=True),
                    opt("Q = 2"),
                    opt("Q = 10"),
                ),
                "Q = 0.707 gives the maximally flat Butterworth response with no passband peak.",
            ),
        ),
        "Multiple-feedback band-pass": (
            q(
                "What is the bandwidth of a multiple-feedback band-pass in terms of ω₀ and Q?",
                (
                    opt("BW = ω₀·Q"),
                    opt("BW = ω₀/Q", correct=True),
                    opt("BW = Q/ω₀"),
                    opt("BW = ω₀ + Q"),
                ),
                "The band-pass bandwidth is BW = ω₀/Q, so higher Q means a narrower, more selective band.",
            ),
            q(
                "Compared with Sallen-Key, why is the multiple-feedback topology often preferred for band-pass?",
                (
                    opt("It has no feedback paths"),
                    opt(
                        "It holds its Q better and is the default for moderate-Q active band-pass filters",
                        correct=True,
                    ),
                    opt("It uses no capacitors"),
                    opt("It cannot invert the signal"),
                ),
                "MFB holds its Q better than Sallen-Key (and inverts the signal), making it the default moderate-Q band-pass.",
            ),
            q(
                "A higher Q in a band-pass filter produces what kind of response?",
                (
                    opt("A wider, less selective band"),
                    opt("A narrower, more selective band", correct=True),
                    opt("A low-pass response"),
                    opt("No passband at all"),
                ),
                "Higher Q narrows the band (BW = ω₀/Q), making the band-pass more selective.",
            ),
        ),
        "Filter order & cascading stages": (
            q(
                "When buffered stages are cascaded, how do their transfer functions combine?",
                (
                    opt("They add"),
                    opt("They multiply, so H_total = H1·H2···Hk", correct=True),
                    opt("They subtract"),
                    opt("Only the last stage matters"),
                ),
                "Because each stage is buffered, the overall transfer function is the product of the stage transfer functions.",
            ),
            q(
                "An odd-order filter is built from how many sections?",
                (
                    opt("Only first-order sections"),
                    opt(
                        "floor(n/2) second-order sections plus one first-order section",
                        correct=True,
                    ),
                    opt("n identical Butterworth sections"),
                    opt("A single high-order op-amp stage"),
                ),
                "An n-th-order filter uses floor(n/2) second-order sections, plus one first-order section when n is odd.",
            ),
            q(
                "Are the individual stages of a cascade each designed to be Butterworth on their own?",
                (
                    opt("Yes, every stage is independently Butterworth"),
                    opt(
                        "No, each stage gets specific ω₀ and Q values so their product gives the target response",
                        correct=True,
                    ),
                    opt("Yes, but only the first stage"),
                    opt("It does not matter what each stage does"),
                ),
                "Stages are assigned table ω₀ and Q values so that their product, not each stage alone, gives the target response.",
            ),
        ),
        "Sensitivity & component selection": (
            q(
                "What does the sensitivity S of a filter parameter to a component measure?",
                (
                    opt("The absolute value of the component"),
                    opt(
                        "How much the parameter changes per relative change in the component",
                        correct=True,
                    ),
                    opt("The noise added by the component"),
                    opt("The temperature of the component"),
                ),
                "Sensitivity is the relative change in a parameter (e.g. ω₀ or Q) per relative change in a component value.",
            ),
            q(
                "Which stages are most troublesome for component tolerance?",
                (
                    opt("Low-Q stages"),
                    opt("High-Q stages, since Q sensitivity grows roughly with Q", correct=True),
                    opt("First-order stages"),
                    opt("Unity-gain buffers"),
                ),
                "High-Q stages are sensitive because Q sensitivity grows roughly with Q, so loose parts drift them badly.",
            ),
            q(
                "Which practical choice reduces drift on the frequency-setting elements?",
                (
                    opt("Use the widest-tolerance parts available"),
                    opt(
                        "Use tight-tolerance, low-temperature-coefficient parts such as C0G/NP0 caps and metal-film resistors",
                        correct=True,
                    ),
                    opt("Maximise all resistor values"),
                    opt("Concentrate all gain in the last stage"),
                ),
                "Tight-tolerance, low-tempco parts (C0G/NP0 caps, metal-film resistors) on the frequency-setting elements reduce drift.",
            ),
        ),
    },
    final=(
        q(
            "Which two op-amp golden rules hold under negative feedback?",
            (
                opt("Infinite output current and zero gain"),
                opt(
                    "No current into the inputs and equal input voltages (virtual short)",
                    correct=True,
                ),
                opt("Inputs 90° out of phase and infinite bandwidth"),
                opt("Output clamped to ground"),
            ),
            "Under negative feedback the ideal op-amp draws no input current and holds its inputs at the same voltage.",
        ),
        q(
            "What is the key practical advantage of active over passive filters?",
            (
                opt("They require no power"),
                opt(
                    "Op-amp buffering lets stages cascade and provide gain without loading each other",
                    correct=True,
                ),
                opt("They never have tolerance issues"),
                opt("They eliminate the need for capacitors"),
            ),
            "Active filters add gain and buffer each stage, so they cascade cleanly without inter-stage loading.",
        ),
        q(
            "Which design Q gives a Sallen-Key a maximally flat Butterworth response?",
            (
                opt("0.5"),
                opt("0.707", correct=True),
                opt("1.0"),
                opt("5.0"),
            ),
            "Q = 0.707 yields the maximally flat Butterworth shape.",
        ),
        q(
            "For a multiple-feedback band-pass, the bandwidth equals which expression?",
            (
                opt("ω₀·Q"),
                opt("ω₀/Q", correct=True),
                opt("Q²"),
                opt("1/(ω₀·Q)"),
            ),
            "Band-pass bandwidth is BW = ω₀/Q; higher Q narrows the band.",
        ),
        q(
            "How do the transfer functions of cascaded buffered stages combine?",
            (
                opt("By addition"),
                opt("By multiplication, with the orders adding", correct=True),
                opt("By taking the maximum"),
                opt("Only the first stage counts"),
            ),
            "Cascaded buffered stages multiply their transfer functions, so their orders add.",
        ),
        q(
            "Why split a high-Q specification across more stages rather than one extreme stage?",
            (
                opt("To save power"),
                opt(
                    "Because Q sensitivity grows with Q, so extreme-Q stages are very sensitive to component tolerance",
                    correct=True,
                ),
                opt("Because op-amps cannot provide gain"),
                opt("To make the circuit larger for its own sake"),
            ),
            "Q sensitivity rises with Q, so spreading a high-Q spec across stages keeps each stage less sensitive and more robust.",
        ),
    ),
)
