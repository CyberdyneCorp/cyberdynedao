"""Quiz questions for the Multibody Dynamics & Simulation - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Generalized coordinates and constraint equations": (
            q(
                "A holonomic constraint is written at which level?",
                (
                    opt("Position: Phi(q, t) = 0", correct=True),
                    opt("Force level only"),
                    opt("Acceleration level only"),
                    opt("It cannot be written algebraically"),
                ),
                "Holonomic constraints are algebraic relations among positions.",
            ),
            q(
                "What is the constraint Jacobian?",
                (
                    opt("The partial derivative of Phi with respect to q", correct=True),
                    opt("The total system mass"),
                    opt("The integral of the forces"),
                    opt("The inverse of the inertia tensor"),
                ),
                "Phi_q maps coordinate rates to constraint rates and is central to the dynamics.",
            ),
            q(
                "Rolling without slipping (xdot = R thetadot) is an example of a",
                (
                    opt("nonholonomic constraint", correct=True),
                    opt("holonomic position constraint"),
                    opt("force constraint"),
                    opt("redundant constraint that can be dropped"),
                ),
                "It constrains velocities and cannot be integrated to a position relation.",
            ),
        ),
        "Newton-Euler equations of motion": (
            q(
                "In M qddot + Phi_q^T lambda = Q, what do the multipliers lambda represent?",
                (
                    opt("The joint constraint (reaction) forces", correct=True),
                    opt("The applied external torques"),
                    opt("The body masses"),
                    opt("The integration time step"),
                ),
                "Lagrange multipliers are the constraint forces enforcing the joints.",
            ),
            q(
                "The augmented KKT system is solved simultaneously for",
                (
                    opt("accelerations qddot and multipliers lambda", correct=True),
                    opt("only the positions"),
                    opt("only the velocities"),
                    opt("only the masses"),
                ),
                "The block system yields both accelerations and reaction forces.",
            ),
            q(
                "For a planar rigid body, the mass block is",
                (
                    opt("diag(m, m, I_G)", correct=True),
                    opt("diag(m, m, m)"),
                    opt("diag(I_G, I_G, I_G)"),
                    opt("a full dense 6x6 matrix"),
                ),
                "Two translational masses and one rotational inertia about G.",
            ),
        ),
        "Lagrangian formulation": (
            q(
                "The Lagrangian is defined as",
                (
                    opt("L = T - V (kinetic minus potential energy)", correct=True),
                    opt("L = T + V"),
                    opt("L = V - T"),
                    opt("L = m a"),
                ),
                "The Lagrangian is kinetic energy minus potential energy.",
            ),
            q(
                "An advantage of using minimal generalized coordinates is that",
                (
                    opt("ideal joint reactions doing no work never appear", correct=True),
                    opt("the mass matrix is always the identity"),
                    opt("no energy needs to be computed"),
                    opt("the system becomes static"),
                ),
                "Workless constraint forces drop out in minimal coordinates.",
            ),
            q(
                "Non-conservative generalized forces Q_nc model",
                (
                    opt("motors and dampers", correct=True),
                    opt("gravity"),
                    opt("ideal spring potential energy"),
                    opt("the mass distribution"),
                ),
                "Conservative effects sit in V; motors and damping are non-conservative.",
            ),
        ),
        "The descriptor form: differential-algebraic equations": (
            q(
                "Why are the descriptor equations of motion a DAE rather than an ODE?",
                (
                    opt(
                        "They include an algebraic constraint Phi = 0 with no lambda derivative",
                        correct=True,
                    ),
                    opt("They contain no derivatives at all"),
                    opt("They are linear"),
                    opt("They have no constraints"),
                ),
                "The algebraic constraint coupled to the ODE makes the system a DAE.",
            ),
            q(
                "What is the differentiation index of the standard index-3 multibody DAE?",
                (
                    opt("3", correct=True),
                    opt("0"),
                    opt("1"),
                    opt("5"),
                ),
                "Phi must be differentiated three times to recover an ODE for lambda.",
            ),
            q(
                "Reducing the index by solving at the acceleration level causes",
                (
                    opt("drift of the position and velocity constraints", correct=True),
                    opt("perfect satisfaction of all constraints forever"),
                    opt("the mass matrix to vanish"),
                    opt("the system to become static"),
                ),
                "Only Phi-doubledot is enforced, so Phi and Phidot slowly drift.",
            ),
        ),
        "Constraint stabilization and drift": (
            q(
                "Baumgarte stabilization works by",
                (
                    opt(
                        "feeding back position and velocity constraint error like a PD controller",
                        correct=True,
                    ),
                    opt("ignoring the constraints entirely"),
                    opt("increasing the body masses"),
                    opt("switching to an explicit integrator"),
                ),
                "It adds 2 alpha Phidot + beta^2 Phi terms to drive errors to zero.",
            ),
            q(
                "Coordinate projection corrects drift by",
                (
                    opt("projecting q back onto Phi(q) = 0 after each step", correct=True),
                    opt("doubling the time step"),
                    opt("removing all joints"),
                    opt("setting all velocities to zero"),
                ),
                "A few Newton iterations restore the constraint manifold each step.",
            ),
            q(
                "Without stabilization, a simulated pendulum tends to",
                (
                    opt("slowly violate its length constraint (drift)", correct=True),
                    opt("conserve its length exactly to machine precision"),
                    opt("stop moving immediately"),
                    opt("gain infinite energy on step one"),
                ),
                "Truncation and rounding accumulate as constraint drift.",
            ),
        ),
        "Numerical integration of multibody systems": (
            q(
                "When are implicit integrators (BDF, Radau, generalized-alpha) preferred?",
                (
                    opt("For stiff systems with fast time constants", correct=True),
                    opt("Only for perfectly rigid frictionless systems"),
                    opt("Never, explicit is always better"),
                    opt("Only when there are no forces"),
                ),
                "Implicit methods take large stable steps despite stiffness.",
            ),
            q(
                "A drawback of explicit Runge-Kutta methods on stiff systems is",
                (
                    opt("the stable step size shrinks dramatically", correct=True),
                    opt("they cannot represent any oscillation"),
                    opt("they require no function evaluations"),
                    opt("they always diverge even when non-stiff"),
                ),
                "Explicit stability ties the step to the fastest time constant.",
            ),
            q(
                "Symplectic / variational integrators are valued because they",
                (
                    opt("conserve energy well over long horizons", correct=True),
                    opt("are the fastest possible methods"),
                    opt("eliminate the need for a mass matrix"),
                    opt("only work for static problems"),
                ),
                "They preserve geometric structure, ideal for conservative systems.",
            ),
        ),
    },
    final=(
        q(
            "Holonomic constraints relate which quantities directly?",
            (
                opt("Positions (and possibly time)", correct=True),
                opt("Only accelerations"),
                opt("Only forces"),
                opt("Only temperatures"),
            ),
            "Holonomic constraints are algebraic position relations Phi(q,t) = 0.",
        ),
        q(
            "In the augmented system, the term Phi_q^T lambda represents",
            (
                opt("the constraint (joint reaction) forces", correct=True),
                opt("the gravity load only"),
                opt("the kinetic energy"),
                opt("the time derivative of mass"),
            ),
            "Multipliers projected by the Jacobian transpose are the reactions.",
        ),
        q(
            "Both Newton-Euler and Lagrangian formulations ultimately lead to",
            (
                opt("the same descriptor (DAE) equations of motion", correct=True),
                opt("completely unrelated equations"),
                opt("a purely static balance"),
                opt("an algebraic equation with no dynamics"),
            ),
            "The two routes converge on the same constrained equations of motion.",
        ),
        q(
            "The standard index-3 multibody DAE is challenging because",
            (
                opt("naive integration is unstable and constraints drift", correct=True),
                opt("it has a closed-form solution always"),
                opt("it contains no derivatives"),
                opt("it never involves the mass matrix"),
            ),
            "High index demands index reduction plus stabilization.",
        ),
        q(
            "Which technique drives accumulated constraint error back toward zero each step?",
            (
                opt("Coordinate projection or Baumgarte stabilization", correct=True),
                opt("Increasing the body masses"),
                opt("Removing the joints"),
                opt("Using a larger time step"),
            ),
            "Projection and Baumgarte both correct constraint drift.",
        ),
        q(
            "For a system with very stiff contact springs, the best integrator choice is",
            (
                opt("an implicit method such as Radau or BDF", correct=True),
                opt("a low-order explicit method with a tiny step"),
                opt("no integration at all"),
                opt("a static solver"),
            ),
            "Implicit methods handle stiffness without vanishingly small steps.",
        ),
    ),
)
