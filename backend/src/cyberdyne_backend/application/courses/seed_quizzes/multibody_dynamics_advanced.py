"""Quiz questions for the Multibody Dynamics & Simulation - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Recursive O(n) algorithms for robot dynamics": (
            q(
                "What does the Recursive Newton-Euler Algorithm (RNEA) compute?",
                (
                    opt("Inverse dynamics: joint torques from q, qdot, qddot", correct=True),
                    opt("Forward dynamics only"),
                    opt("The contact forces between two robots"),
                    opt("The thermal load of the motors"),
                ),
                "RNEA finds the torques needed to produce a prescribed motion.",
            ),
            q(
                "The Articulated-Body Algorithm (ABA) solves forward dynamics in",
                (
                    opt("O(n) time", correct=True),
                    opt("O(n^3) time"),
                    opt("O(2^n) time"),
                    opt("constant time regardless of accuracy"),
                ),
                "ABA exploits the tree structure for linear-time forward dynamics.",
            ),
            q(
                "In M(q) qddot + C(q,qdot) qdot + g(q) = tau, the term C represents",
                (
                    opt("Coriolis and centrifugal effects", correct=True),
                    opt("gravity"),
                    opt("the applied motor torque"),
                    opt("the constraint Jacobian"),
                ),
                "C captures velocity-dependent Coriolis/centrifugal terms.",
            ),
        ),
        "Flexible multibody dynamics": (
            q(
                "The floating frame of reference (FFR) formulation splits motion into",
                (
                    opt("large rigid-body motion plus small elastic deformation", correct=True),
                    opt("only rigid-body motion"),
                    opt("only thermal expansion"),
                    opt("two unrelated rigid bodies"),
                ),
                "A moving frame carries large motion; modal coordinates carry deformation.",
            ),
            q(
                "Which method is best suited to large deformation of slender bodies like cables?",
                (
                    opt("Absolute Nodal Coordinate Formulation (ANCF)", correct=True),
                    opt("Small-strain FFR with few modes"),
                    opt("Rigid-body-only modelling"),
                    opt("A single particle model"),
                ),
                "ANCF handles geometric nonlinearity with a constant mass matrix.",
            ),
            q(
                "Flexible bodies add many lightly damped modes, which favors",
                (
                    opt("implicit, numerically damped integrators", correct=True),
                    opt("explicit Euler with a large step"),
                    opt("a static solver"),
                    opt("ignoring the dynamics entirely"),
                ),
                "Generalized-alpha / HHT damp spurious high-frequency content.",
            ),
        ),
        "Contact, impact and friction": (
            q(
                "Penalty (compliant) contact models the contact force as",
                (
                    opt("a stiff spring-damper on the interpenetration", correct=True),
                    opt("an exact rigid non-penetration constraint"),
                    opt("zero in all cases"),
                    opt("a constant independent of penetration"),
                ),
                "Penalty methods let bodies slightly interpenetrate and react elastically.",
            ),
            q(
                "The Signorini condition states that",
                (
                    opt(
                        "either the gap or the normal force is zero, never both nonzero",
                        correct=True,
                    ),
                    opt("the normal force is always negative"),
                    opt("friction is unlimited"),
                    opt("bodies always interpenetrate"),
                ),
                "It is a complementarity condition: 0 <= Fn perpendicular to gap >= 0.",
            ),
            q(
                "Coulomb friction limits the tangential force to",
                (
                    opt("mu times the normal force (the friction cone)", correct=True),
                    opt("zero always"),
                    opt("the body weight regardless of contact"),
                    opt("the spring stiffness"),
                ),
                "The tangential force magnitude cannot exceed mu * Fn.",
            ),
        ),
        "Application: vehicle dynamics simulation": (
            q(
                "The bicycle (single-track) model simplifies a car by",
                (
                    opt("lumping each axle into one wheel", correct=True),
                    opt("removing the chassis"),
                    opt("ignoring all tire forces"),
                    opt("treating it as a single particle with no yaw"),
                ),
                "It collapses left/right wheels into one per axle for handling studies.",
            ),
            q(
                "In a linear tire model, lateral force is proportional to",
                (
                    opt("the slip angle, via cornering stiffness", correct=True),
                    opt("the vehicle mass only"),
                    opt("the engine torque"),
                    opt("the ambient temperature"),
                ),
                "Fy = -C_alpha * alpha for small slip angles.",
            ),
            q(
                "Which is a widely used nonlinear empirical tire model in full vehicle simulation?",
                (
                    opt("The Pacejka Magic Formula", correct=True),
                    opt("The ideal gas law"),
                    opt("Ohm's law"),
                    opt("The Bernoulli equation"),
                ),
                "Pacejka's Magic Formula fits measured tire force/slip curves.",
            ),
        ),
        "Differentiable simulation and trajectory optimization": (
            q(
                "A differentiable simulator additionally provides",
                (
                    opt(
                        "gradients of the dynamics with respect to states and inputs", correct=True
                    ),
                    opt("only a final image of the motion"),
                    opt("nothing beyond a standard simulator"),
                    opt("the material cost of the bodies"),
                ),
                "Gradients enable gradient-based design and control optimization.",
            ),
            q(
                "Direct collocation enforces the equations of motion as",
                (
                    opt("defect constraints between knot points", correct=True),
                    opt("an unconstrained cost only"),
                    opt("a single algebraic equation"),
                    opt("a random sampling step"),
                ),
                "States/controls are discretized and the dynamics become equality constraints.",
            ),
            q(
                "Trajectory optimization with contact is hard mainly because",
                (
                    opt("contact makes the problem hybrid / non-smooth", correct=True),
                    opt("there is never a cost function"),
                    opt("gradients are always exactly zero"),
                    opt("the dynamics become linear"),
                ),
                "Contact-implicit optimization must handle mode switches and complementarity.",
            ),
        ),
        "Machine learning for multibody dynamics": (
            q(
                "A surrogate model is used to",
                (
                    opt("cheaply approximate expensive simulations for optimization", correct=True),
                    opt("replace the laws of physics permanently"),
                    opt("increase simulation cost"),
                    opt("eliminate the need for any data"),
                ),
                "Surrogates let you optimize cheaply, validating only the best designs.",
            ),
            q(
                "Lagrangian / Hamiltonian neural networks are attractive because they",
                (
                    opt("respect physical structure such as energy conservation", correct=True),
                    opt("ignore all physics for speed"),
                    opt("require no training"),
                    opt("only work for static problems"),
                ),
                "Embedding structure improves generalization over black-box nets.",
            ),
            q(
                "Graph Network Simulators represent a multibody system as",
                (
                    opt("nodes for bodies and edges for joints/interactions", correct=True),
                    opt("a single scalar value"),
                    opt("a flat image with no structure"),
                    opt("a list of unrelated numbers"),
                ),
                "The graph encodes bodies and their connections for learned rollouts.",
            ),
        ),
    },
    final=(
        q(
            "What is the time complexity advantage of recursive (Featherstone) algorithms?",
            (
                opt("O(n) instead of O(n^3) for chain dynamics", correct=True),
                opt("O(n^3) instead of O(n)"),
                opt("Exponential in n"),
                opt("Constant regardless of accuracy"),
            ),
            "RNEA and ABA scale linearly with the number of bodies.",
        ),
        q(
            "For small-strain flexible bodies, which formulation is typically used?",
            (
                opt("Floating frame of reference with modal coordinates", correct=True),
                opt("Single-particle model"),
                opt("Rigid-body-only model"),
                opt("Pure thermal model"),
            ),
            "FFR plus reduced modes is efficient for small elastic deformation.",
        ),
        q(
            "Rigid contact solvers commonly cast a step as a",
            (
                opt("Linear Complementarity Problem (LCP) or its convex relaxation", correct=True),
                opt("simple linear regression"),
                opt("Fourier transform"),
                opt("sorting algorithm"),
            ),
            "Signorini plus Coulomb friction yields an LCP per step.",
        ),
        q(
            "Understeer and oversteer can first be predicted with which model?",
            (
                opt("The linear bicycle (single-track) model", correct=True),
                opt("A single particle in free fall"),
                opt("A static truss"),
                opt("A thermal conduction model"),
            ),
            "The bicycle model captures yaw/lateral handling behavior.",
        ),
        q(
            "Why is a differentiable simulator valuable for design and control?",
            (
                opt("It supplies gradients for gradient-based optimization", correct=True),
                opt("It removes the need for any model"),
                opt("It only produces screenshots"),
                opt("It makes the dynamics linear"),
            ),
            "Gradients through the dynamics enable efficient optimization and learning.",
        ),
        q(
            "A key benefit of physics-structured neural dynamics models is",
            (
                opt("better generalization by respecting conservation laws", correct=True),
                opt("they need no data and no physics"),
                opt("they are always slower than full simulation"),
                opt("they only apply to statics"),
            ),
            "Encoding structure (energy, mass matrix) improves extrapolation.",
        ),
    ),
)
