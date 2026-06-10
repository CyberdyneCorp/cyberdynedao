from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The quadrotor model: frames, state & inputs": (
            q(
                "How many numbers make up the quadrotor state vector described in the lesson?",
                (
                    opt("6"),
                    opt("12", correct=True),
                    opt("4"),
                    opt("9"),
                ),
                "The state has 12 numbers: position, roll/pitch/yaw, body velocity, and body angular velocity.",
            ),
            q(
                "How does each rotor's thrust relate to its spin rate in the model?",
                (
                    opt("Thrust is proportional to the spin rate Omega"),
                    opt(
                        "Thrust is proportional to the square of the spin rate, T = kT * Omega^2",
                        correct=True,
                    ),
                    opt("Thrust is inversely proportional to the spin rate"),
                    opt("Thrust is independent of the spin rate"),
                ),
                "Each rotor makes thrust T_i = kT * Omega_i^2, proportional to the square of its spin rate.",
            ),
            q(
                "After the mixer is introduced, what does the flight controller treat as its inputs?",
                (
                    opt("The four individual rotor spin rates only"),
                    opt("One thrust T and three moments tau_phi, tau_theta, tau_psi", correct=True),
                    opt("The 12 state variables directly"),
                    opt("Earth-frame position and yaw"),
                ),
                "The four motors combine into one thrust and three moments, which are treated as the inputs from then on.",
            ),
        ),
        "Newton–Euler equations of motion": (  # noqa: RUF001
            q(
                "In which frame does the lesson apply the two rigid-body equations?",
                (
                    opt("The Earth (inertial) frame"),
                    opt("The body frame", correct=True),
                    opt("A camera-fixed frame"),
                    opt("A wind frame"),
                ),
                "The Newton-Euler equations are applied in the body frame.",
            ),
            q(
                "What do the omega cross m*v terms in the translational dynamics represent?",
                (
                    opt("Aerodynamic drag forces"),
                    opt(
                        "Fictitious Coriolis and centripetal forces from a rotating frame",
                        correct=True,
                    ),
                    opt("The thrust contribution"),
                    opt("Gravitational potential energy"),
                ),
                "Those terms are the fictitious Coriolis/centripetal forces that appear when writing Newton's law in a rotating frame.",
            ),
            q(
                "Near hover with small angles, what does the vertical equation decouple to?",
                (
                    opt("m * z_ddot = mg - T", correct=True),
                    opt("m * z_ddot = T only"),
                    opt("Ixx * phi_ddot = mg"),
                    opt("Izz * psi_ddot = T"),
                ),
                "Near hover the model decouples and the vertical equation becomes m * z_ddot = mg - T.",
            ),
        ),
        "The Lagrangian derivation": (
            q(
                "How is the Lagrangian defined in the recipe?",
                (
                    opt("L = T_kin + V (kinetic plus potential)"),
                    opt("L = T_kin - V (kinetic minus potential)", correct=True),
                    opt("L = V - T_kin (potential minus kinetic)"),
                    opt("L = T_kin times V"),
                ),
                "The Lagrangian is formed as L = T_kin - V, kinetic energy minus potential energy.",
            ),
            q(
                "What generalised coordinates does the lesson pick for the quadrotor?",
                (
                    opt("Only x, y, z"),
                    opt("x, y, z, phi, theta, psi", correct=True),
                    opt("The four rotor spin rates"),
                    opt("u, v, w, p, q, r"),
                ),
                "The generalised coordinates chosen are q = (x, y, z, phi, theta, psi).",
            ),
            q(
                "What is described as the Lagrangian payoff over Newton-Euler?",
                (
                    opt("It needs detailed free-body diagrams"),
                    opt(
                        "The gyroscopic omega cross I*omega term falls out of the derivatives instead of being added by hand",
                        correct=True,
                    ),
                    opt("It avoids using any energy at all"),
                    opt("It only works for linear systems"),
                ),
                "In the Lagrangian method the gyroscopic term that was added by hand in Newton-Euler simply falls out of the derivatives.",
            ),
        ),
        "The Hamiltonian derivation": (
            q(
                "What does the Hamiltonian reformulation use in place of velocities?",
                (
                    opt("Accelerations"),
                    opt("Momenta", correct=True),
                    opt("Forces"),
                    opt("Rotor spin rates"),
                ),
                "The Hamiltonian reformulates the physics in terms of momenta instead of velocities.",
            ),
            q(
                "How does the Hamiltonian view change the order and count of the equations?",
                (
                    opt("It turns n second-order equations into 2n first-order ones", correct=True),
                    opt("It turns 2n first-order equations into n second-order ones"),
                    opt("It leaves the equations second-order but halves their number"),
                    opt("It makes the equations algebraic with no derivatives"),
                ),
                "It converts n second-order equations into 2n first-order ones, exactly the state-space form a simulator wants.",
            ),
            q(
                "In the comparison table, which method is described as best for state-space form and numerics?",
                (
                    opt("Newton-Euler"),
                    opt("Lagrangian"),
                    opt("Hamiltonian", correct=True),
                    opt("All methods are equally poor at it"),
                ),
                "The table lists the Hamiltonian as best for state-space form, controls, energy methods, and numerics.",
            ),
        ),
        "Simulate it: integrate the EOM": (
            q(
                "Which integration scheme does the code use to advance the equations of motion?",
                (
                    opt("Runge-Kutta 4th order"),
                    opt("Simple Euler steps", correct=True),
                    opt("Implicit backward differentiation"),
                    opt("Symplectic leapfrog"),
                ),
                "The code integrates the decoupled hover model with simple Euler steps.",
            ),
            q(
                "According to the code comments, what happens if you set T = m*g exactly?",
                (
                    opt("It climbs steadily"),
                    opt("It hovers and altitude stays near zero", correct=True),
                    opt("It descends rapidly"),
                    opt("It pitches over"),
                ),
                "Setting thrust equal to weight makes the craft hover, so altitude stays around zero.",
            ),
            q(
                "What effect does raising Ixx have, per the try-it-yourself notes?",
                (
                    opt("It makes the craft pitch slower", correct=True),
                    opt("It makes the craft pitch faster"),
                    opt("It changes the climb rate"),
                    opt("It has no effect on anything"),
                ),
                "Raising Ixx (the roll/pitch inertia) makes the craft pitch more slowly.",
            ),
        ),
    },
    final=(
        q(
            "The course derives the quadrotor equations of motion in how many different ways?",
            (
                opt("Two"),
                opt("Three: Newton-Euler, Lagrangian, and Hamiltonian", correct=True),
                opt("Four"),
                opt("One"),
            ),
            "The capstone derives the equations of motion three ways: Newton-Euler, Lagrangian, and Hamiltonian.",
        ),
        q(
            "How does a quadrotor accelerate forward according to the Newton-Euler lesson?",
            (
                opt("A dedicated forward-facing motor pushes it"),
                opt(
                    "It pitches so the tilted thrust gains a horizontal component T*sin(theta)",
                    correct=True,
                ),
                opt("Gravity pulls it forward"),
                opt("The yaw moment drives it forward"),
            ),
            "There is no forward motor; the craft leans, and the tilted thrust gives a sideways force T*sin(theta).",
        ),
        q(
            "What vertical-axis equation do all three methods agree on?",
            (
                opt("m * z_ddot = mg - T", correct=True),
                opt("m * z_ddot = T + mg"),
                opt("Ixx * z_ddot = tau"),
                opt("m * z_ddot = -mg"),
            ),
            "Newton, Lagrange, and Hamilton all yield the identical vertical equation m * z_ddot = mg - T.",
        ),
        q(
            "What is the main message about the three derivation methods?",
            (
                opt("They each describe a different aircraft"),
                opt(
                    "They are different languages that yield the same equations of motion for one system",
                    correct=True,
                ),
                opt("Only the Hamiltonian method is physically correct"),
                opt("They produce conflicting results that must be averaged"),
            ),
            "All three describe the same quadrotor and yield the same equations of motion; they are different languages for one truth.",
        ),
        q(
            "In the Hamiltonian phase-space picture, what does a conservative system trace?",
            (
                opt("A straight line of increasing energy"),
                opt("A closed constant-energy orbit", correct=True),
                opt("A random scatter of points"),
                opt("An ever-expanding spiral"),
            ),
            "A conservative system holds H constant, so its state endlessly circles a closed constant-energy orbit.",
        ),
    ),
)
