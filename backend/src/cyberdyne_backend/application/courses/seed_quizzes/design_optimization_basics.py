"""Quiz questions for the Engineering Design Optimization - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is design optimization": (
            q(
                "The three ingredients of every optimization problem are:",
                (
                    opt("objective, design variables and constraints", correct=True),
                    opt("mesh, solver and post-processor"),
                    opt("cost, schedule and scope"),
                    opt("stress, strain and modulus"),
                ),
                "We minimize an objective over design variables subject to constraints.",
            ),
            q(
                "In a typical engineering design, the optimum usually lies:",
                (
                    opt("on an active constraint, not in the interior", correct=True),
                    opt("always at the centre of the feasible region"),
                    opt("wherever the first feasible design happens to be"),
                    opt("only where all variables are zero"),
                ),
                "Pushing toward best performance drives the design onto a binding limit.",
            ),
            q(
                "A poor problem formulation tends to:",
                (
                    opt("optimize the wrong thing very precisely", correct=True),
                    opt("always return an infeasible result"),
                    opt("guarantee the global optimum anyway"),
                    opt("remove the need for constraints"),
                ),
                "Choosing the objective and constraints well is most of the work.",
            ),
        ),
        "The standard optimization problem": (
            q(
                "To maximize a function f using a minimizer, you:",
                (
                    opt("minimize -f", correct=True),
                    opt("minimize 1/f"),
                    opt("minimize f squared"),
                    opt("cannot do it at all"),
                ),
                "Maximizing f is identical to minimizing its negative.",
            ),
            q(
                "A requirement 'sigma <= sigma_allow' becomes the standard-form constraint:",
                (
                    opt("g = sigma - sigma_allow <= 0", correct=True),
                    opt("g = sigma_allow - sigma <= 0"),
                    opt("h = sigma * sigma_allow = 0"),
                    opt("g = sigma + sigma_allow <= 0"),
                ),
                "Inequalities are written as g(x) <= 0.",
            ),
            q(
                "Why is scaling variables and constraints important?",
                (
                    opt(
                        "solvers struggle when quantities have very different magnitudes",
                        correct=True,
                    ),
                    opt("it changes the location of the optimum"),
                    opt("it removes the need for bounds"),
                    opt("it converts the problem to a maximization"),
                ),
                "Mixing metres with pascals ill-conditions the problem.",
            ),
        ),
        "Feasible region and constraints": (
            q(
                "The feasible region is:",
                (
                    opt(
                        "the set of all designs satisfying every constraint and bound", correct=True
                    ),
                    opt("the single best design point"),
                    opt("the region where the gradient is zero"),
                    opt("the set of all designs that violate a constraint"),
                ),
                "It is the intersection of all the allowed half-spaces and bounds.",
            ),
            q(
                "A constraint is 'active' at a point when:",
                (
                    opt("it holds as an equality there, g = 0", correct=True),
                    opt("it has slack, g < 0"),
                    opt("its multiplier is negative"),
                    opt("the objective is zero there"),
                ),
                "An active constraint presses the design against its limit.",
            ),
            q(
                "If the feasible region is empty, the problem is:",
                (
                    opt("infeasible - the requirements contradict each other", correct=True),
                    opt("convex by definition"),
                    opt("guaranteed to have a global optimum"),
                    opt("unbounded below"),
                ),
                "Empty feasible region means something must be relaxed.",
            ),
        ),
        "Local and global optima": (
            q(
                "A global minimum differs from a local minimum because:",
                (
                    opt("no feasible point anywhere has a smaller objective", correct=True),
                    opt("it is always at a constraint boundary"),
                    opt("its gradient need not be zero"),
                    opt("it depends on the starting point"),
                ),
                "Global is best over the whole feasible set; local is best only nearby.",
            ),
            q(
                "Most gradient-based methods find:",
                (
                    opt("a local optimum, depending on the starting point", correct=True),
                    opt("always the global optimum"),
                    opt("only saddle points"),
                    opt("the feasible region but never an optimum"),
                ),
                "They walk downhill to the nearest valley, which may not be deepest.",
            ),
            q(
                "A practical defense against a bad local optimum is:",
                (
                    opt("using multiple random starts or a global method", correct=True),
                    opt("increasing the step size to infinity"),
                    opt("removing all constraints"),
                    opt("ignoring the objective"),
                ),
                "Multistart and global methods (GA, PSO) help escape poor local optima.",
            ),
        ),
        "Convexity and why it matters": (
            q(
                "In a convex optimization problem:",
                (
                    opt("every local minimum is also the global minimum", correct=True),
                    opt("there are always many global minima"),
                    opt("gradients cannot be used"),
                    opt("the feasible region must be empty"),
                ),
                "Convexity guarantees a local optimum is global.",
            ),
            q(
                "A twice-differentiable function is convex when its Hessian is:",
                (
                    opt("positive semidefinite everywhere", correct=True),
                    opt("negative definite everywhere"),
                    opt("always zero"),
                    opt("indefinite at the optimum"),
                ),
                "Positive semidefinite curvature means the graph never bows above its chords.",
            ),
            q(
                "Real mechanical designs with stress, contact and buckling are usually:",
                (
                    opt("nonconvex", correct=True),
                    opt("always convex"),
                    opt("always linear"),
                    opt("free of any constraints"),
                ),
                "Such physics typically yields nonconvex landscapes.",
            ),
        ),
        "A map of optimization methods": (
            q(
                "The first big split in choosing an optimizer is whether:",
                (
                    opt("derivatives are available and cheap", correct=True),
                    opt("the design is painted or unpainted"),
                    opt("the company uses metric or imperial units"),
                    opt("the part is made of steel"),
                ),
                "Derivative availability decides gradient-based vs gradient-free.",
            ),
            q(
                "Gradient-free methods such as GA and PSO are preferred when:",
                (
                    opt("the function is noisy, discrete or a black box", correct=True),
                    opt("smooth analytic gradients are cheap to compute"),
                    opt("the problem has millions of smooth variables"),
                    opt("only one function evaluation is allowed"),
                ),
                "They need only function values and tolerate ruggedness.",
            ),
            q(
                "A healthy convergence history typically shows the objective:",
                (
                    opt("dropping quickly then flattening near a stationary point", correct=True),
                    opt("increasing without bound"),
                    opt("oscillating forever with no trend"),
                    opt("staying exactly constant from the start"),
                ),
                "The gap to the optimum decays and levels off as it converges.",
            ),
        ),
    },
    final=(
        q(
            "Which trio defines a standard optimization problem?",
            (
                opt("objective, design variables, constraints", correct=True),
                opt("mean, variance, skew"),
                opt("force, area, stress"),
                opt("cost, mass, color"),
            ),
            "Minimize an objective over variables subject to constraints.",
        ),
        q(
            "An inequality constraint in standard form is written as:",
            (
                opt("g(x) <= 0", correct=True),
                opt("g(x) = 1"),
                opt("g(x) >= 100"),
                opt("g(x) is undefined"),
            ),
            "Standard form uses g(x) <= 0 and h(x) = 0.",
        ),
        q(
            "A constraint with no slack at the optimum is called:",
            (
                opt("active", correct=True),
                opt("inactive"),
                opt("convex"),
                opt("unbounded"),
            ),
            "Active means g = 0 there.",
        ),
        q(
            "Convexity is valued because it guarantees:",
            (
                opt("a local optimum is the global optimum", correct=True),
                opt("the problem has no constraints"),
                opt("gradients are never needed"),
                opt("multiple global optima always exist"),
            ),
            "Convex programs let a fast local solver be trusted globally.",
        ),
        q(
            "To escape a poor local optimum on a multimodal problem you can:",
            (
                opt("use multistart or a global method like PSO/GA", correct=True),
                opt("set the gradient to a large constant"),
                opt("delete the objective function"),
                opt("require the feasible region to be empty"),
            ),
            "Multistart and global search explore beyond one basin.",
        ),
        q(
            "Compared with gradient-based methods, gradient-free methods generally:",
            (
                opt(
                    "need many more evaluations but tolerate black boxes and multimodality",
                    correct=True,
                ),
                opt("always converge faster on smooth problems"),
                opt("require exact second derivatives"),
                opt("cannot handle discrete variables"),
            ),
            "They trade extra evaluations for robustness and no derivative need.",
        ),
    ),
)
