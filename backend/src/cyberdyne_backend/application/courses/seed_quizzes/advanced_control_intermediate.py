"""Quiz questions for the Advanced Control Systems — Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pole placement & state feedback": (
            q(
                "State feedback u = -Kx lets you place the closed-loop poles arbitrarily if the system is:",
                (
                    opt("controllable", correct=True),
                    opt("unobservable"),
                    opt("open-loop unstable"),
                    opt("single-output"),
                ),
                "Arbitrary pole placement requires controllability.",
            ),
            q(
                "The closed-loop dynamics under u = -Kx are governed by:",
                (
                    opt("(A - BK)", correct=True),
                    opt("(A - C)"),
                    opt("(A + D)"),
                    opt("B alone"),
                ),
                "Eigenvalues of A-BK are the closed-loop poles.",
            ),
            q(
                "Placing poles further into the left half-plane generally gives:",
                (
                    opt("faster response but larger control effort", correct=True),
                    opt("slower response, less effort"),
                    opt("instability"),
                    opt("no change"),
                ),
                "Aggressive poles cost actuator effort.",
            ),
        ),
        "State observers & the separation principle": (
            q(
                "An observer (estimator) is needed when:",
                (
                    opt("the full state is not directly measured", correct=True),
                    opt("the system has no inputs"),
                    opt("all states are sensors"),
                    opt("the plant is static"),
                ),
                "Observers reconstruct unmeasured states from outputs.",
            ),
            q(
                "The separation principle states that:",
                (
                    opt(
                        "controller and observer gains can be designed independently", correct=True
                    ),
                    opt("they must be identical"),
                    opt("observers make systems unstable"),
                    opt("feedback is unnecessary"),
                ),
                "Closed-loop poles = controller poles union observer poles.",
            ),
            q(
                "Observer error dynamics are governed by:",
                (
                    opt("(A - LC)", correct=True),
                    opt("(A - BK)"),
                    opt("(C - D)"),
                    opt("B"),
                ),
                "L is the observer gain; A-LC sets error decay.",
            ),
        ),
        "The linear quadratic regulator (LQR)": (
            q(
                "LQR designs feedback by minimizing:",
                (
                    opt("a quadratic cost of state and control effort", correct=True),
                    opt("the number of poles"),
                    opt("the sampling rate"),
                    opt("the output offset"),
                ),
                "J = integral of x'Qx + u'Ru.",
            ),
            q(
                "Increasing R (relative to Q) in LQR yields:",
                (
                    opt("more conservative control (less effort)", correct=True),
                    opt("faster, more aggressive control"),
                    opt("guaranteed instability"),
                    opt("no effect"),
                ),
                "R penalizes control effort.",
            ),
            q(
                "The LQR gain is obtained by solving:",
                (
                    opt("the algebraic Riccati equation", correct=True),
                    opt("a Bode integral"),
                    opt("the FFT"),
                    opt("Ohm's law"),
                ),
                "K = R^-1 B' P, with P from the Riccati equation.",
            ),
        ),
        "Integral action & reference tracking": (
            q(
                "Adding integral action to state feedback primarily:",
                (
                    opt(
                        "eliminates steady-state error to step references/disturbances",
                        correct=True,
                    ),
                    opt("increases noise"),
                    opt("removes all poles"),
                    opt("disables the observer"),
                ),
                "Integral action drives steady-state error to zero.",
            ),
            q(
                "To track a non-zero reference, a common approach is:",
                (
                    opt("augment the state with the integral of the tracking error", correct=True),
                    opt("remove feedback"),
                    opt("set Q = 0"),
                    opt("ignore the reference"),
                ),
                "State augmentation with integral error enables tracking.",
            ),
            q(
                "Steady-state error to a step with pure proportional state feedback is generally:",
                (
                    opt("non-zero unless explicitly compensated", correct=True),
                    opt("always zero"),
                    opt("infinite"),
                    opt("negative"),
                ),
                "Without integral action or feedforward, offset remains.",
            ),
        ),
        "Introduction to nonlinear systems": (
            q(
                "Linearization approximates a nonlinear system near:",
                (
                    opt("an equilibrium (operating) point", correct=True),
                    opt("infinity"),
                    opt("the origin only, never elsewhere"),
                    opt("the output saturation"),
                ),
                "The Jacobian linearizes about an equilibrium.",
            ),
            q(
                "A feature nonlinear systems can show that linear ones cannot is:",
                (
                    opt("limit cycles & multiple equilibria", correct=True),
                    opt("a single transfer function"),
                    opt("superposition"),
                    opt("constant gain"),
                ),
                "Limit cycles, bifurcations, multiple equilibria are nonlinear phenomena.",
            ),
            q(
                "Superposition (scaling/adding responses) holds for:",
                (
                    opt("linear systems only", correct=True),
                    opt("all nonlinear systems"),
                    opt("chaotic systems"),
                    opt("saturating systems"),
                ),
                "Superposition is a defining property of linearity.",
            ),
        ),
        "Lyapunov stability": (
            q(
                "A Lyapunov function V(x) for stability must be:",
                (
                    opt(
                        "positive definite with a negative (semi)definite derivative", correct=True
                    ),
                    opt("negative everywhere"),
                    opt("constant"),
                    opt("the input signal"),
                ),
                "V > 0 and V' <= 0 prove stability without solving the ODE.",
            ),
            q(
                "Lyapunov's direct method is valuable because it:",
                (
                    opt("proves stability without explicitly solving the equations", correct=True),
                    opt("requires the closed-form solution"),
                    opt("only works for linear systems"),
                    opt("needs the FFT"),
                ),
                "It infers stability from an energy-like function.",
            ),
            q(
                "For a linear system, a Lyapunov function can be found by solving:",
                (
                    opt("the Lyapunov equation A'P + PA = -Q", correct=True),
                    opt("Ohm's law"),
                    opt("the wave equation"),
                    opt("a Bode plot"),
                ),
                "Solving for P > 0 proves stability.",
            ),
        ),
    },
    final=(
        q(
            "Arbitrary pole placement via u = -Kx requires the system to be:",
            (opt("controllable", correct=True), opt("unobservable"), opt("static"), opt("scalar")),
            "Controllability enables pole placement.",
        ),
        q(
            "The separation principle allows:",
            (
                opt("independent design of controller and observer", correct=True),
                opt("only one of them"),
                opt("identical gains"),
                opt("no feedback"),
            ),
            "Design K and L separately.",
        ),
        q(
            "LQR minimizes:",
            (
                opt("a quadratic state + control cost", correct=True),
                opt("the pole count"),
                opt("the bandwidth"),
                opt("the offset"),
            ),
            "Via the Riccati equation.",
        ),
        q(
            "Integral action is added to:",
            (
                opt("remove steady-state error", correct=True),
                opt("add noise"),
                opt("destabilize"),
                opt("remove poles"),
            ),
            "Eliminates offset.",
        ),
        q(
            "Linearization is performed about:",
            (
                opt("an equilibrium point", correct=True),
                opt("infinity"),
                opt("the noise floor"),
                opt("the sample time"),
            ),
            "Using the Jacobian.",
        ),
        q(
            "A valid Lyapunov function is:",
            (
                opt("positive definite with V' <= 0", correct=True),
                opt("negative definite"),
                opt("constant"),
                opt("the input"),
            ),
            "Energy-like certificate of stability.",
        ),
    ),
)
