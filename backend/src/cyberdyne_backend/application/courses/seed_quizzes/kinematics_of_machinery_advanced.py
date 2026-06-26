"""Quiz questions for the Kinematics & Dynamics of Machinery - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Static and dynamic balancing of rotors": (
            q(
                "The centrifugal force from a rotor unbalance grows with speed as:",
                (
                    opt("omega squared", correct=True),
                    opt("omega"),
                    opt("the square root of omega"),
                    opt("it is independent of omega"),
                ),
                "F = m r omega^2 rises with the square of rotational speed.",
            ),
            q(
                "Dynamic balancing of a rigid rotor generally requires correction in:",
                (
                    opt("two planes", correct=True),
                    opt("one plane only"),
                    opt("zero planes"),
                    opt("at least five planes"),
                ),
                "Two correction planes zero both the net force and the net moment couple.",
            ),
            q(
                "Static balance alone ensures that:",
                (
                    opt("the net unbalance force is zero, but a couple may remain", correct=True),
                    opt("both force and moment couple are zero"),
                    opt("the rotor is balanced only at zero speed"),
                    opt("the bearings carry no load ever"),
                ),
                "Static balance zeros sum(m r) but a residual moment couple can persist without dynamic balance.",
            ),
        ),
        "Reciprocating balancing and engine dynamics": (
            q(
                "In the slider-crank, the cos(2 theta) component of piston acceleration is the:",
                (
                    opt("secondary inertia force, at twice crank frequency", correct=True),
                    opt("primary inertia force, at crank frequency"),
                    opt("Coriolis term"),
                    opt("static gravity load"),
                ),
                "The cos(2 theta)/n term is the secondary force, oscillating at 2*omega.",
            ),
            q(
                "Secondary reciprocating forces are cancelled with balance shafts running at:",
                (
                    opt("twice crank speed", correct=True),
                    opt("crank speed"),
                    opt("half crank speed"),
                    opt("any arbitrary speed"),
                ),
                "Secondary forces (2*omega) need balance shafts at 2x crank speed (Lanchester balancers).",
            ),
            q(
                "Which engine layout is naturally balanced in primary and secondary forces and couples?",
                (
                    opt("inline-six", correct=True),
                    opt("inline-four"),
                    opt("single cylinder"),
                    opt("inline-three"),
                ),
                "The inline-six is inherently balanced in primary/secondary forces and couples.",
            ),
        ),
        "Mechanism synthesis: function, path and motion": (
            q(
                "Making a coupler point trace a specified curve is which synthesis type?",
                (
                    opt("path generation", correct=True),
                    opt("function generation"),
                    opt("force balancing"),
                    opt("modal analysis"),
                ),
                "Path generation requires a coupler point to follow a prescribed trajectory.",
            ),
            q(
                "The Freudenstein equation is useful because, in its unknowns K1, K2, K3, it is:",
                (
                    opt("linear, so three precision points give a linear solve", correct=True),
                    opt("nonlinear and needs global optimization"),
                    opt("only valid for gears"),
                    opt("identical to the Coriolis equation"),
                ),
                "Freudenstein's form is linear in K1, K2, K3, solved exactly at three precision points.",
            ),
            q(
                "Burmester theory is used to synthesize a linkage that:",
                (
                    opt("guides a rigid body through several prescribed positions", correct=True),
                    opt("balances a rotor"),
                    opt("computes gear ratios"),
                    opt("integrates the equations of motion"),
                ),
                "Burmester (motion generation) locates pivots to guide a body through finitely separated positions.",
            ),
        ),
        "Optimization-based and computational synthesis": (
            q(
                "The optimization-synthesis objective typically minimizes the:",
                (
                    opt("squared error between generated and target curves", correct=True),
                    opt("total mass of the links"),
                    opt("number of joints"),
                    opt("bearing temperature"),
                ),
                "It minimizes sum of squared deviations from the target task over many points.",
            ),
            q(
                "The synthesis design space is challenging mainly because it is:",
                (
                    opt("nonconvex with many local minima and defect regions", correct=True),
                    opt("perfectly convex"),
                    opt("one-dimensional"),
                    opt("free of constraints"),
                ),
                "Nonconvexity, circuit/branch defects and constraints favor global stochastic methods.",
            ),
            q(
                "Grashof and transmission-angle requirements enter the optimization as:",
                (
                    opt("constraints or penalty terms on the objective", correct=True),
                    opt("the only design variables"),
                    opt("post-processing only"),
                    opt("irrelevant factors"),
                ),
                "Defective or poorly transmitting designs are penalized or constrained out of the search.",
            ),
        ),
        "Multibody simulation and AI-assisted design": (
            q(
                "Constrained multibody dynamics is most directly formulated as:",
                (
                    opt("differential-algebraic equations (DAEs)", correct=True),
                    opt("a single linear ODE"),
                    opt("a static force balance"),
                    opt("a Fourier series"),
                ),
                "Equations of motion plus algebraic constraints form an index-3 DAE system.",
            ),
            q(
                "In the augmented system, the Lagrange multipliers lambda represent the:",
                (
                    opt("joint reaction (constraint) forces", correct=True),
                    opt("link masses"),
                    opt("gear ratios"),
                    opt("damping coefficients"),
                ),
                "The multipliers are the constraint forces (joint reactions) enforcing the constraints.",
            ),
            q(
                "A neural-network surrogate model is used in mechanism design to:",
                (
                    opt(
                        "predict responses quickly so many candidates can be screened", correct=True
                    ),
                    opt("replace the need for any physics"),
                    opt("increase the number of joints"),
                    opt("eliminate balancing"),
                ),
                "Surrogates approximate expensive simulations, enabling fast optimization over many designs.",
            ),
        ),
    },
    final=(
        q(
            "Rotor unbalance bearing forces are reduced by balancing because they otherwise scale as:",
            (
                opt("omega squared", correct=True),
                opt("omega"),
                opt("1/omega"),
                opt("constant with speed"),
            ),
            "F = m r omega^2 makes unbalance the dominant high-speed excitation.",
        ),
        q(
            "The primary reciprocating inertia force oscillates at a frequency of:",
            (
                opt("the crank speed omega", correct=True),
                opt("twice the crank speed"),
                opt("half the crank speed"),
                opt("zero"),
            ),
            "The cos(theta) term is the primary force at frequency omega; cos(2 theta) is secondary.",
        ),
        q(
            "Matching an output angle to a function of the input angle is:",
            (
                opt("function generation", correct=True),
                opt("path generation"),
                opt("motion generation"),
                opt("dynamic balancing"),
            ),
            "Function generation enforces psi = f(phi) between output and input angles.",
        ),
        q(
            "Compared with precision-point methods, optimization synthesis:",
            (
                opt("minimizes error over the whole task, not just a few points", correct=True),
                opt("matches infinitely many points exactly"),
                opt("ignores constraints"),
                opt("only works for gears"),
            ),
            "Optimization minimizes a continuous error metric over many sampled task points.",
        ),
        q(
            "The index-3 multibody DAE system is solved for accelerations and:",
            (
                opt("Lagrange multipliers (joint reaction forces)", correct=True),
                opt("gear tooth counts"),
                opt("the Grashof condition"),
                opt("the transmission angle"),
            ),
            "The augmented matrix yields both accelerations and the constraint-force multipliers.",
        ),
        q(
            "AI surrogates accelerate mechanism design primarily by:",
            (
                opt("replacing expensive simulations with fast approximations", correct=True),
                opt("removing all design constraints"),
                opt("eliminating the need for synthesis"),
                opt("increasing simulation cost"),
            ),
            "Trained surrogates predict performance in microseconds, enabling large-scale search.",
        ),
    ),
)
