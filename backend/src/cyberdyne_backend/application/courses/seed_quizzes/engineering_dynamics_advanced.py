"""Quiz questions for the Engineering Dynamics - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Rigid-body planar kinematics": (
            q(
                "How many degrees of freedom does a rigid body have in planar motion?",
                (
                    opt("Three (two translation, one rotation)", correct=True),
                    opt("Two"),
                    opt("Six"),
                    opt("One"),
                ),
                "Planar rigid-body motion has two translational and one rotational DOF.",
            ),
            q(
                "The rigid-body velocity equation is?",
                (
                    opt("v_B = v_A + omega cross r_B/A", correct=True),
                    opt("v_B = v_A * r_B/A"),
                    opt("v_B = omega / r_B/A"),
                    opt("v_B = v_A - alpha r_B/A"),
                ),
                "Velocities relate through v_B = v_A + omega x r_B/A.",
            ),
            q(
                "At the instantaneous center of zero velocity, a point's speed equals?",
                (
                    opt("omega times its distance to the IC", correct=True),
                    opt("Zero everywhere"),
                    opt("v_A always"),
                    opt("alpha times distance"),
                ),
                "Every point appears to rotate purely about the IC, so v = omega * d.",
            ),
        ),
        "Mass moment of inertia and the parallel-axis theorem": (
            q(
                "The parallel-axis theorem states?",
                (
                    opt("I = I_G + m d^2", correct=True),
                    opt("I = I_G - m d^2"),
                    opt("I = I_G / (m d^2)"),
                    opt("I = m d^2 only"),
                ),
                "Shifting a distance d from the centroidal axis adds m d^2.",
            ),
            q(
                "A thin rod about its end has how much inertia compared with about its center?",
                (
                    opt("Four times as much", correct=True),
                    opt("Half as much"),
                    opt("The same"),
                    opt("Twice as much"),
                ),
                "I_end = (1/3) m L^2 vs I_center = (1/12) m L^2, a factor of 4.",
            ),
            q(
                "The radius of gyration k is defined by?",
                (
                    opt("k = sqrt(I/m)", correct=True),
                    opt("k = I m"),
                    opt("k = I / m^2"),
                    opt("k = m / I"),
                ),
                "k packages the mass distribution as an equivalent distance: I = m k^2.",
            ),
        ),
        "Rigid-body kinetics and rolling": (
            q(
                "The rotational equation of motion about the mass center is?",
                (
                    opt("Sum of moments about G = I_G alpha", correct=True),
                    opt("Sum of moments about G = m a_G"),
                    opt("Sum of moments about G = 0 always"),
                    opt("Sum of moments about G = I_G omega"),
                ),
                "Moments about G equal I_G times the angular acceleration.",
            ),
            q(
                "Rolling without slipping imposes which constraint?",
                (
                    opt("a_G = R alpha", correct=True),
                    opt("a_G = R omega^2"),
                    opt("a_G = 0"),
                    opt("alpha = 0"),
                ),
                "The contact point is the IC, giving a_G = R alpha (and v_G = R omega).",
            ),
            q(
                "Which body rolls fastest down an incline?",
                (
                    opt("A solid sphere (smallest I/(mR^2))", correct=True),
                    opt("A hoop"),
                    opt("A solid cylinder"),
                    opt("They all roll at the same rate"),
                ),
                "a_G = g sin(theta)/(1 + I/(mR^2)); the sphere has the smallest factor (0.4), so it is fastest.",
            ),
        ),
        "Energy and momentum for rigid bodies": (
            q(
                "The kinetic energy of a rigid body in planar motion is?",
                (
                    opt("(1/2) m v_G^2 + (1/2) I_G omega^2", correct=True),
                    opt("(1/2) m v_G^2 only"),
                    opt("(1/2) I_G omega^2 only"),
                    opt("m v_G + I_G omega"),
                ),
                "It combines translational and rotational kinetic energy.",
            ),
            q(
                "For rolling without slipping, the friction force does how much work?",
                (
                    opt(
                        "Zero, because its point of application is instantaneously at rest",
                        correct=True,
                    ),
                    opt("Negative work equal to mu N d"),
                    opt("Positive work equal to the kinetic energy"),
                    opt("Half the gravitational work"),
                ),
                "The contact point is momentarily at rest, so static friction does no work during rolling.",
            ),
            q(
                "Angular momentum of a rigid body about its mass center is?",
                (
                    opt("H_G = I_G omega", correct=True),
                    opt("H_G = m v_G"),
                    opt("H_G = (1/2) I_G omega^2"),
                    opt("H_G = I_G alpha"),
                ),
                "H_G = I_G omega; angular impulse equals I_G times the change in omega.",
            ),
        ),
        "Introduction to vibration: free and damped response": (
            q(
                "The natural frequency of a mass-spring system is?",
                (
                    opt("omega_n = sqrt(k/m)", correct=True),
                    opt("omega_n = sqrt(m/k)"),
                    opt("omega_n = k/m"),
                    opt("omega_n = m k"),
                ),
                "omega_n = sqrt(k/m) for an undamped mass-spring oscillator.",
            ),
            q(
                "A damping ratio of 0 < zeta < 1 produces what response?",
                (
                    opt("Underdamped: decaying oscillation at omega_d", correct=True),
                    opt("Overdamped: slow non-oscillating return"),
                    opt("Critically damped: fastest non-oscillating return"),
                    opt("Undamped: constant-amplitude oscillation"),
                ),
                "Underdamped systems oscillate while decaying, at omega_d = omega_n sqrt(1 - zeta^2).",
            ),
            q(
                "The logarithmic decrement is used to?",
                (
                    opt("Estimate the damping ratio from a decaying trace", correct=True),
                    opt("Measure the natural frequency directly"),
                    opt("Compute the spring stiffness"),
                    opt("Find the resonant amplitude"),
                ),
                "delta = ln(x_n/x_{n+1}) = 2 pi zeta / sqrt(1 - zeta^2) gives zeta from successive peaks.",
            ),
        ),
        "Forced vibration, resonance and design optimization": (
            q(
                "Resonance of a forced oscillator occurs near which frequency ratio?",
                (
                    opt("r = omega/omega_n approximately 1", correct=True),
                    opt("r = 0"),
                    opt("r much greater than 1"),
                    opt("r negative"),
                ),
                "The magnification factor peaks when the drive frequency nears the natural frequency, r ~= 1.",
            ),
            q(
                "Increasing damping near resonance does what to the response peak?",
                (
                    opt("Lowers and flattens it", correct=True),
                    opt("Raises it sharply"),
                    opt("Shifts it to r = 0"),
                    opt("Has no effect"),
                ),
                "More damping reduces the peak magnification and broadens the response.",
            ),
            q(
                "For vibration isolation, the mount should be designed so that?",
                (
                    opt(
                        "r is greater than sqrt(2), where transmissibility drops below one",
                        correct=True,
                    ),
                    opt("r equals 1"),
                    opt("r is exactly zero"),
                    opt("damping is removed entirely"),
                ),
                "Above r = sqrt(2) the transmissibility falls below unity, isolating the base from the force.",
            ),
        ),
    },
    final=(
        q(
            "The acceleration relation for a point on a rigid body includes which centripetal term?",
            (
                opt("-omega^2 r_B/A", correct=True),
                opt("+alpha r_B/A only"),
                opt("-alpha^2 r_B/A"),
                opt("+omega r_B/A"),
            ),
            "a_B = a_A + alpha x r_B/A - omega^2 r_B/A; the last term is centripetal.",
        ),
        q(
            "A solid cylinder rolling down a theta incline has acceleration?",
            (
                opt("(2/3) g sin(theta)", correct=True),
                opt("(1/2) g sin(theta)"),
                opt("g sin(theta)"),
                opt("(2/5) g sin(theta)"),
            ),
            "With I/(mR^2) = 1/2, a_G = g sin(theta)/(1 + 1/2) = (2/3) g sin(theta).",
        ),
        q(
            "Which energy expression is correct for a rolling rigid body?",
            (
                opt("T = (1/2) m v_G^2 + (1/2) I_G omega^2", correct=True),
                opt("T = (1/2) I_G omega^2 only"),
                opt("T = m v_G^2"),
                opt("T = I_G alpha"),
            ),
            "Total kinetic energy is the sum of translational and rotational parts.",
        ),
        q(
            "The damping ratio is defined as?",
            (
                opt("zeta = c / (2 sqrt(k m))", correct=True),
                opt("zeta = c / k"),
                opt("zeta = 2 sqrt(k m) / c"),
                opt("zeta = c m"),
            ),
            "zeta = c / (2 sqrt(km)); zeta = 1 is critical damping.",
        ),
        q(
            "The steady-state magnification factor is largest when?",
            (
                opt("The frequency ratio r is near 1 and damping is light", correct=True),
                opt("r is much greater than 1"),
                opt("damping is very high"),
                opt("the force amplitude is zero"),
            ),
            "Light damping at r ~= 1 gives the large resonant peak in M(r).",
        ),
        q(
            "A modern design loop minimizing peak transmissibility typically uses?",
            (
                opt(
                    "Numerical optimization (e.g. scipy.optimize) over design variables",
                    correct=True,
                ),
                opt("Only hand calculation of one case"),
                opt("Ignoring damping entirely"),
                opt("Static equilibrium analysis alone"),
            ),
            "Treating stiffness/damping as variables and optimizing a cost (often with surrogate or Bayesian methods) is standard practice.",
        ),
    ),
)
