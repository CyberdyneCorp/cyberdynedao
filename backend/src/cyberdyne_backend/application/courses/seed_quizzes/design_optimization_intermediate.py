"""Quiz questions for the Engineering Design Optimization - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Gradients and optimality conditions": (
            q(
                "The first-order necessary condition for an unconstrained local minimum is:",
                (
                    opt("the gradient is zero, grad f = 0", correct=True),
                    opt("the gradient is maximal"),
                    opt("the Hessian is negative definite"),
                    opt("the objective is zero"),
                ),
                "A stationary point has a vanishing gradient.",
            ),
            q(
                "A stationary point is confirmed as a strict local minimum when its Hessian is:",
                (
                    opt("positive definite", correct=True),
                    opt("negative definite"),
                    opt("indefinite"),
                    opt("singular and zero"),
                ),
                "Positive definite curvature means a true minimum, not a saddle.",
            ),
            q(
                "Why is grad f = 0 necessary but not sufficient for a minimum?",
                (
                    opt("maxima and saddle points are also stationary", correct=True),
                    opt("it never holds at a minimum"),
                    opt("it only holds for linear functions"),
                    opt("constraints make it irrelevant"),
                ),
                "The second-order test distinguishes minima from saddles and maxima.",
            ),
        ),
        "Line search and Newton methods": (
            q(
                "Steepest descent uses the search direction:",
                (
                    opt("the negative gradient, -grad f", correct=True),
                    opt("the positive gradient, +grad f"),
                    opt("a random direction"),
                    opt("the Hessian itself"),
                ),
                "It moves opposite the direction of steepest increase.",
            ),
            q(
                "Newton's method gains fast (quadratic) convergence by using:",
                (
                    opt("curvature from the Hessian", correct=True),
                    opt("only the function value"),
                    opt("a fixed unit step always"),
                    opt("random restarts"),
                ),
                "Newton solves Hessian * p = -gradient for the direction.",
            ),
            q(
                "The Armijo condition in a backtracking line search ensures:",
                (
                    opt("a sufficient decrease in the objective for the chosen step", correct=True),
                    opt("the step is always exactly 1.0"),
                    opt("the gradient becomes zero in one step"),
                    opt("the Hessian is positive definite"),
                ),
                "Armijo requires enough decrease relative to the slope.",
            ),
        ),
        "KKT conditions and Lagrange multipliers": (
            q(
                "Complementary slackness in the KKT conditions states that:",
                (
                    opt("either a constraint is active or its multiplier is zero", correct=True),
                    opt("all multipliers must be negative"),
                    opt("the objective gradient is zero at the optimum"),
                    opt("equality constraints can be ignored"),
                ),
                "lambda_i * g_i = 0, so slack and multiplier cannot both be nonzero.",
            ),
            q(
                "Inequality-constraint multipliers in the KKT conditions must satisfy:",
                (
                    opt("lambda_i >= 0", correct=True),
                    opt("lambda_i <= 0"),
                    opt("lambda_i = 1"),
                    opt("lambda_i is unrestricted"),
                ),
                "Dual feasibility requires non-negative multipliers for inequalities.",
            ),
            q(
                "A Lagrange multiplier can be interpreted as a:",
                (
                    opt(
                        "shadow price - the sensitivity of the optimum to relaxing that constraint",
                        correct=True,
                    ),
                    opt("random scaling factor"),
                    opt("count of design variables"),
                    opt("step length of the line search"),
                ),
                "It tells how much the optimal objective improves per unit of relaxation.",
            ),
        ),
        "Penalty and SQP methods": (
            q(
                "A quadratic penalty method handles constraints by:",
                (
                    opt(
                        "adding a growing cost for violations and solving unconstrained subproblems",
                        correct=True,
                    ),
                    opt("deleting the constraints entirely"),
                    opt("converting the objective to its negative"),
                    opt("requiring exact second derivatives of the objective"),
                ),
                "As the penalty weight grows, the minimizer approaches the constrained optimum.",
            ),
            q(
                "A drawback of using a very large penalty weight is:",
                (
                    opt("the subproblem becomes ill-conditioned", correct=True),
                    opt("the optimum disappears"),
                    opt("constraints are always violated"),
                    opt("the objective becomes convex automatically"),
                ),
                "Large weights distort the problem and hurt the solver.",
            ),
            q(
                "Sequential Quadratic Programming (SQP) works by, at each step:",
                (
                    opt(
                        "solving a quadratic model of the objective with linearized constraints",
                        correct=True,
                    ),
                    opt("evaluating only random points"),
                    opt("ignoring the KKT conditions"),
                    opt("fitting a Gaussian process"),
                ),
                "SQP solves a QP subproblem for the search direction each iteration.",
            ),
        ),
        "Genetic algorithms": (
            q(
                "The core operators of a genetic algorithm are:",
                (
                    opt("selection, crossover and mutation", correct=True),
                    opt("gradient, Hessian and line search"),
                    opt("inertia, cognitive and social terms"),
                    opt("DOE, surrogate and infill"),
                ),
                "A GA selects fit parents, recombines them, and mutates for diversity.",
            ),
            q(
                "Mutation in a GA primarily serves to:",
                (
                    opt("inject random variation and preserve population diversity", correct=True),
                    opt("guarantee a convex problem"),
                    opt("compute exact gradients"),
                    opt("remove all constraints"),
                ),
                "Mutation prevents premature convergence by maintaining diversity.",
            ),
            q(
                "Genetic algorithms are well suited to problems that are:",
                (
                    opt(
                        "multimodal, discrete or black-box, where gradients are unavailable",
                        correct=True,
                    ),
                    opt("strictly convex with cheap gradients"),
                    opt("one-dimensional and linear only"),
                    opt("limited to a single function evaluation"),
                ),
                "They need only function values and can escape local optima.",
            ),
        ),
        "Particle swarm optimization": (
            q(
                "In PSO, each particle's velocity update combines its inertia with attraction to:",
                (
                    opt("its personal best and the swarm's global best", correct=True),
                    opt("the gradient and the Hessian"),
                    opt("two fixed grid points"),
                    opt("the constraint multipliers"),
                ),
                "Velocity blends inertia, cognitive (personal best) and social (global best) terms.",
            ),
            q(
                "The inertia weight w in PSO controls the balance between:",
                (
                    opt("exploration and exploitation", correct=True),
                    opt("feasibility and infeasibility"),
                    opt("convexity and concavity"),
                    opt("mean and variance"),
                ),
                "Higher inertia favors exploration; lower favors local refinement.",
            ),
            q(
                "A practical advantage of PSO over gradient methods is that it:",
                (
                    opt("needs no gradients and is simple to implement", correct=True),
                    opt("always converges in one iteration"),
                    opt("requires the exact Hessian"),
                    opt("only works on convex problems"),
                ),
                "PSO uses only function values and has few parameters.",
            ),
        ),
    },
    final=(
        q(
            "The first-order optimality condition for an unconstrained minimum is:",
            (
                opt("grad f = 0", correct=True),
                opt("Hessian = 0"),
                opt("f = 0"),
                opt("grad f is maximal"),
            ),
            "Stationarity: the gradient vanishes.",
        ),
        q(
            "Newton's method converges fast because it uses:",
            (
                opt("second-order curvature from the Hessian", correct=True),
                opt("a random search direction"),
                opt("only the objective value"),
                opt("a constant step of zero"),
            ),
            "Curvature gives quadratic local convergence.",
        ),
        q(
            "Complementary slackness says, for each inequality constraint:",
            (
                opt("lambda_i * g_i = 0", correct=True),
                opt("lambda_i + g_i = 1"),
                opt("lambda_i = g_i"),
                opt("g_i must be positive"),
            ),
            "Either the constraint is active or its multiplier is zero.",
        ),
        q(
            "SQP solves, at each iteration, a subproblem that is:",
            (
                opt("a quadratic program with linearized constraints", correct=True),
                opt("a full nonlinear black box"),
                opt("a Gaussian-process fit"),
                opt("a random sampling step"),
            ),
            "It uses a QP model to get the next search direction.",
        ),
        q(
            "Which method is gradient-free and population-based?",
            (
                opt("particle swarm optimization", correct=True),
                opt("Newton's method"),
                opt("steepest descent"),
                opt("interior-point method"),
            ),
            "PSO evolves a swarm using only function values.",
        ),
        q(
            "A Lagrange multiplier at the optimum represents the:",
            (
                opt(
                    "sensitivity of the optimal objective to relaxing that constraint", correct=True
                ),
                opt("number of iterations used"),
                opt("step length of the search"),
                opt("population size of a GA"),
            ),
            "It is the shadow price of the constraint.",
        ),
    ),
)
