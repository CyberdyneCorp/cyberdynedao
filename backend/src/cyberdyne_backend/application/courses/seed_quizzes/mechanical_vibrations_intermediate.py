"""Quiz questions for the Mechanical Vibrations - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Frequency response and the magnification factor": (
            q(
                "The dynamic magnification factor M(r) is given by?",
                (
                    opt("1 / sqrt((1 - r^2)^2 + (2 zeta r)^2)", correct=True),
                    opt("(1 - r^2)^2 + (2 zeta r)^2"),
                    opt("1 / (1 - r^2)"),
                    opt("2 zeta r"),
                ),
                "M(r) = X/X_static for a harmonically forced SDOF system.",
            ),
            q(
                "Near resonance the peak magnification is approximately?",
                (
                    opt("1/(2 zeta)", correct=True),
                    opt("2 zeta"),
                    opt("1 - zeta"),
                    opt("zeta^2"),
                ),
                "Lightly damped systems peak near 1/(2 zeta), so low damping means a tall peak.",
            ),
            q(
                "At the resonance crossing r = 1, the phase lag is about?",
                (
                    opt("90 degrees", correct=True),
                    opt("0 degrees"),
                    opt("180 degrees"),
                    opt("45 degrees"),
                ),
                "Phi = 90 degrees at r = 1 regardless of damping, the cleanest resonance marker.",
            ),
        ),
        "Transmissibility and vibration isolation": (
            q(
                "Force transmissibility curves all pass through T_r = 1 at which frequency ratio?",
                (
                    opt("r = sqrt(2)", correct=True),
                    opt("r = 1"),
                    opt("r = 0"),
                    opt("r = 2"),
                ),
                "All transmissibility curves cross unity at r = sqrt(2); isolation needs r > sqrt(2).",
            ),
            q(
                "To isolate a machine, the mount should be designed so that?",
                (
                    opt(
                        "The operating frequency lies well above the mount natural frequency",
                        correct=True,
                    ),
                    opt("The operating frequency equals the mount natural frequency"),
                    opt("The mount is as stiff as possible"),
                    opt("Damping is removed entirely"),
                ),
                "A soft mount (low omega_n) puts operation in the r > sqrt(2) isolation region.",
            ),
            q(
                "For r > sqrt(2), increasing damping has what effect on isolation?",
                (
                    opt("It worsens isolation", correct=True),
                    opt("It always improves isolation"),
                    opt("It has no effect at all"),
                    opt("It shifts the crossover to r = 1"),
                ),
                "More damping helps near resonance but raises T_r above sqrt(2), worsening isolation.",
            ),
        ),
        "Base excitation and rotating unbalance": (
            q(
                "For rotating unbalance, the injected force scales with?",
                (
                    opt("omega^2 (the square of speed)", correct=True),
                    opt("omega (linearly with speed)"),
                    opt("1/omega"),
                    opt("a constant independent of speed"),
                ),
                "The eccentric mass produces a force m e omega^2, growing with the square of speed.",
            ),
            q(
                "For rotating unbalance at high speed (r >> 1), the response MX/(me) approaches?",
                (
                    opt("A constant value of about 1", correct=True),
                    opt("Zero"),
                    opt("Infinity"),
                    opt("r^4"),
                ),
                "MX/(me) -> 1 as r grows, so the mass amplitude approaches me/M.",
            ),
            q(
                "Base excitation displacement transmissibility uses the same formula as?",
                (
                    opt("Force transmissibility", correct=True),
                    opt("The logarithmic decrement"),
                    opt("The static deflection formula"),
                    opt("The mass matrix eigenvalues"),
                ),
                "Mass displacement transmissibility for base motion equals the force transmissibility.",
            ),
        ),
        "The tuned mass damper": (
            q(
                "An ideal undamped tuned absorber tuned to the disturbance frequency does what to the primary mass?",
                (
                    opt("Drives its steady amplitude toward zero", correct=True),
                    opt("Doubles its amplitude"),
                    opt("Has no effect"),
                    opt("Increases its natural frequency"),
                ),
                "The absorber moves out of phase and its spring force cancels the applied force.",
            ),
            q(
                "Den Hartog's optimum tuning ratio for mass ratio mu is?",
                (
                    opt("omega2/omega1 = 1/(1 + mu)", correct=True),
                    opt("omega2/omega1 = 1 + mu"),
                    opt("omega2/omega1 = mu"),
                    opt("omega2/omega1 = sqrt(mu)"),
                ),
                "Den Hartog tuning sets the absorber frequency to 1/(1 + mu) of the primary.",
            ),
            q(
                "Taipei 101 famously uses which device to limit sway?",
                (
                    opt("A large pendulum tuned mass damper", correct=True),
                    opt("A magnetic levitation core"),
                    opt("Active rocket thrusters"),
                    opt("A water-filled flywheel"),
                ),
                "Its 660-tonne pendulum TMD is a classic real-world dynamic absorber.",
            ),
        ),
        "Measuring damping and the half-power method": (
            q(
                "The half-power (3 dB) points on an FRF are where the response falls to?",
                (
                    opt("1/sqrt(2) of the peak", correct=True),
                    opt("Half of the peak"),
                    opt("Zero"),
                    opt("Twice the peak"),
                ),
                "At -3 dB the magnitude is 1/sqrt(2) of the peak; the bandwidth gives damping.",
            ),
            q(
                "The half-power method estimates damping as?",
                (
                    opt("zeta ~ (omega2 - omega1) / (2 omega_n)", correct=True),
                    opt("zeta ~ (omega2 - omega1) * omega_n"),
                    opt("zeta ~ omega_n / (omega2 - omega1)"),
                    opt("zeta ~ omega2 + omega1"),
                ),
                "The fractional bandwidth between the half-power points equals 2 zeta.",
            ),
            q(
                "The quality factor Q is approximately?",
                (
                    opt("1/(2 zeta)", correct=True),
                    opt("2 zeta"),
                    opt("zeta^2"),
                    opt("1 - zeta"),
                ),
                "A sharp, narrow peak (high Q) means light damping, Q ~ 1/(2 zeta).",
            ),
        ),
    },
    final=(
        q(
            "The magnification factor peaks near which frequency ratio?",
            (
                opt("r close to 1", correct=True),
                opt("r close to 0"),
                opt("r close to 10"),
                opt("r exactly sqrt(2)"),
            ),
            "Resonance sits near r = 1 with peak height ~ 1/(2 zeta).",
        ),
        q(
            "Vibration isolation (T_r < 1) requires the frequency ratio to be?",
            (
                opt("Greater than sqrt(2)", correct=True),
                opt("Less than 1"),
                opt("Exactly 1"),
                opt("Exactly sqrt(2)"),
            ),
            "Below sqrt(2) the mount amplifies; isolation only happens for r > sqrt(2).",
        ),
        q(
            "Rotating-unbalance force grows with speed as?",
            (
                opt("omega^2", correct=True),
                opt("omega"),
                opt("1/omega"),
                opt("constant"),
            ),
            "The eccentric mass injects m e omega^2, so response rises with speed.",
        ),
        q(
            "A tuned mass damper works by?",
            (
                opt(
                    "Adding a secondary mass-spring tuned to absorb energy at the disturbance frequency",
                    correct=True,
                ),
                opt("Increasing the primary stiffness only"),
                opt("Removing all damping from the system"),
                opt("Lowering the excitation amplitude at the source"),
            ),
            "The absorber moves out of phase and counteracts the applied force.",
        ),
        q(
            "The logarithmic decrement is best used in which domain?",
            (
                opt("Time domain, from a free ring-down", correct=True),
                opt("Frequency domain, from an FRF sweep"),
                opt("Static loading tests"),
                opt("Thermal measurements"),
            ),
            "Log decrement reads successive peaks in a decaying free response.",
        ),
        q(
            "A high quality factor Q on an FRF peak indicates?",
            (
                opt("Light damping and a sharp, narrow peak", correct=True),
                opt("Heavy damping and a broad peak"),
                opt("That the system is overdamped"),
                opt("Zero natural frequency"),
            ),
            "Q ~ 1/(2 zeta); a tall narrow peak corresponds to low damping.",
        ),
    ),
)
