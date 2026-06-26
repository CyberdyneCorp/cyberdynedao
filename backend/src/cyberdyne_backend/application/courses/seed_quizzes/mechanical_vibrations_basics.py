"""Quiz questions for the Mechanical Vibrations - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What vibration is and why it matters": (
            q(
                "Which three physical ingredients let a system vibrate?",
                (
                    opt("Inertia, elasticity, and energy dissipation", correct=True),
                    opt("Friction, gravity, and pressure"),
                    opt("Voltage, current, and resistance"),
                    opt("Temperature, volume, and entropy"),
                ),
                "Mass stores kinetic energy, stiffness stores potential energy, and damping removes energy.",
            ),
            q(
                "What does a degree of freedom (DOF) count?",
                (
                    opt(
                        "Independent coordinates needed to describe the configuration", correct=True
                    ),
                    opt("The number of springs in a system"),
                    opt("The amount of damping present"),
                    opt("The total mass of the system"),
                ),
                "DOF count equals the number of independent coordinates, and it sets the number of natural frequencies.",
            ),
            q(
                "Why do engineers usually want to reduce vibration?",
                (
                    opt(
                        "Oscillating stress drives fatigue, noise, and loss of precision",
                        correct=True,
                    ),
                    opt("Vibration always increases efficiency"),
                    opt("Vibration adds mass to a structure"),
                    opt("Vibration is required for static equilibrium"),
                ),
                "Cyclic stress fatigues materials, and oscillation causes noise and precision loss.",
            ),
        ),
        "The spring-mass-damper model": (
            q(
                "What is the equation of motion of a forced single-DOF spring-mass-damper?",
                (
                    opt("m x'' + c x' + k x = F(t)", correct=True),
                    opt("m x'' + k x' + c x = F(t)"),
                    opt("c x'' + m x' + k x = F(t)"),
                    opt("m x' + c x + k = F(t)"),
                ),
                "Newton's law gives inertia m x'', viscous damping c x', and spring force k x balancing F(t).",
            ),
            q(
                "How is the undamped natural frequency defined?",
                (
                    opt("omega_n = sqrt(k/m)", correct=True),
                    opt("omega_n = sqrt(m/k)"),
                    opt("omega_n = k/m"),
                    opt("omega_n = c/(2 m)"),
                ),
                "Dividing the EOM by m gives omega_n = sqrt(k/m).",
            ),
            q(
                "What is the damping ratio zeta?",
                (
                    opt("zeta = c / (2 sqrt(k m))", correct=True),
                    opt("zeta = c / (k m)"),
                    opt("zeta = 2 sqrt(k m) / c"),
                    opt("zeta = k / (2 m)"),
                ),
                "Zeta is dimensionless, comparing actual damping c to critical damping 2 sqrt(k m).",
            ),
        ),
        "Free vibration and simple harmonic motion": (
            q(
                "In undamped free vibration, the oscillation frequency depends on what?",
                (
                    opt("Only m and k, not the amplitude", correct=True),
                    opt("The initial amplitude only"),
                    opt("The damping coefficient c"),
                    opt("The applied force magnitude"),
                ),
                "For SHM the frequency omega_n = sqrt(k/m) is independent of amplitude.",
            ),
            q(
                "For m = 0.5 kg and k = 200 N/m, the natural frequency is about?",
                (
                    opt("About 3.2 Hz", correct=True),
                    opt("About 20 Hz"),
                    opt("About 0.3 Hz"),
                    opt("About 64 Hz"),
                ),
                "omega_n = sqrt(200/0.5) = 20 rad/s, so f_n = 20/(2 pi) ~ 3.18 Hz.",
            ),
            q(
                "In undamped SHM, the total mechanical energy does what?",
                (
                    opt("Stays constant, sloshing between kinetic and potential", correct=True),
                    opt("Decays exponentially"),
                    opt("Grows without bound"),
                    opt("Is entirely dissipated each cycle"),
                ),
                "With no damping nothing dissipates energy, so the total stays constant.",
            ),
        ),
        "Damping and the decay of free vibration": (
            q(
                "Which damping condition gives oscillation inside a decaying envelope?",
                (
                    opt("Underdamped, 0 < zeta < 1", correct=True),
                    opt("Critically damped, zeta = 1"),
                    opt("Overdamped, zeta > 1"),
                    opt("Undamped, zeta = 0"),
                ),
                "Underdamped systems oscillate at omega_d inside an exp(-zeta omega_n t) envelope.",
            ),
            q(
                "What is the damped natural frequency omega_d?",
                (
                    opt("omega_d = omega_n sqrt(1 - zeta^2)", correct=True),
                    opt("omega_d = omega_n sqrt(1 + zeta^2)"),
                    opt("omega_d = omega_n / zeta"),
                    opt("omega_d = omega_n (1 - zeta)"),
                ),
                "Damping lowers the oscillation frequency by the factor sqrt(1 - zeta^2).",
            ),
            q(
                "The logarithmic decrement is measured from what?",
                (
                    opt("The ratio of successive peak amplitudes in a ring-down", correct=True),
                    opt("The steady-state forced amplitude"),
                    opt("The applied force frequency"),
                    opt("The static deflection under gravity"),
                ),
                "delta = ln(x_i / x_{i+1}) reads off successive peaks and yields zeta.",
            ),
        ),
        "Forced vibration and resonance, intuitively": (
            q(
                "At steady state, a harmonically forced system oscillates at which frequency?",
                (
                    opt("The driving frequency omega", correct=True),
                    opt("Its own natural frequency omega_n"),
                    opt("The damped frequency omega_d"),
                    opt("Zero frequency"),
                ),
                "After transients decay the response is at the drive frequency, not omega_n.",
            ),
            q(
                "Resonance occurs when the frequency ratio r = omega/omega_n is approximately?",
                (
                    opt("Near 1", correct=True),
                    opt("Near 0"),
                    opt("Much greater than 10"),
                    opt("Exactly 0.5"),
                ),
                "When r ~ 1 the force pushes in step with the motion and amplitude balloons.",
            ),
            q(
                "At resonance, what keeps the amplitude finite?",
                (
                    opt("Damping", correct=True),
                    opt("Increasing the stiffness"),
                    opt("Increasing the mass"),
                    opt("Removing the force"),
                ),
                "Only damping limits the peak; at r = 1 amplification is roughly 1/(2 zeta).",
            ),
        ),
    },
    final=(
        q(
            "Which single equation models a forced single-DOF system?",
            (
                opt("m x'' + c x' + k x = F(t)", correct=True),
                opt("k x'' + c x' + m x = F(t)"),
                opt("m x' + c x = F(t)"),
                opt("x'' + x = 0 always"),
            ),
            "Inertia, damping, and stiffness terms balance the applied force.",
        ),
        q(
            "Natural frequency omega_n equals?",
            (
                opt("sqrt(k/m)", correct=True),
                opt("sqrt(m/k)"),
                opt("c/(2 m)"),
                opt("k m"),
            ),
            "omega_n = sqrt(k/m); higher stiffness or lower mass raises it.",
        ),
        q(
            "A damping ratio of zeta = 1 corresponds to which case?",
            (
                opt("Critically damped: fastest return with no overshoot", correct=True),
                opt("Underdamped with many oscillations"),
                opt("Undamped, never decaying"),
                opt("Resonant amplification"),
            ),
            "zeta = 1 returns to equilibrium fastest without oscillating.",
        ),
        q(
            "In undamped SHM, what is true about the period?",
            (
                opt("It is independent of amplitude", correct=True),
                opt("It doubles when amplitude doubles"),
                opt("It depends on the initial velocity only"),
                opt("It depends on the damping c"),
            ),
            "SHM is isochronous: frequency depends only on m and k.",
        ),
        q(
            "Vibration isolation and resonance avoidance matter mainly because?",
            (
                opt("Cyclic stress causes fatigue and unwanted noise/motion", correct=True),
                opt("Vibration always saves energy"),
                opt("Higher amplitude is always desirable"),
                opt("It eliminates the need for damping"),
            ),
            "Repeated stress cycles fatigue parts, and resonance can be destructive.",
        ),
        q(
            "The damped natural frequency omega_d is always?",
            (
                opt("Slightly lower than omega_n for an underdamped system", correct=True),
                opt("Higher than omega_n"),
                opt("Equal to the drive frequency"),
                opt("Zero for any damping"),
            ),
            "omega_d = omega_n sqrt(1 - zeta^2) < omega_n when 0 < zeta < 1.",
        ),
    ),
)
