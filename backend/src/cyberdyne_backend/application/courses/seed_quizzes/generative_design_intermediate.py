"""Quiz questions for the Generative Design & AI for CAD - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Topology optimization with SIMP": (
            q(
                "In SIMP, the design variable assigned to each element is its:",
                (
                    opt("density rho between 0 and 1", correct=True),
                    opt("temperature"),
                    opt("colour index"),
                    opt("node count"),
                ),
                "SIMP uses a continuous element density rho in [0, 1].",
            ),
            q(
                "Why is stiffness penalized as E = Emin + rho^p (E0 - Emin) with p about 3?",
                (
                    opt(
                        "to make intermediate (grey) densities inefficient and force near 0/1",
                        correct=True,
                    ),
                    opt("to make grey densities cheaper than solid"),
                    opt("to increase the mesh resolution"),
                    opt("to add colour to the result"),
                ),
                "The penalty exponent pushes densities toward solid or void.",
            ),
            q(
                "The objective minimized in classic SIMP topology optimization is:",
                (
                    opt("compliance C = U^T K U under a volume budget", correct=True),
                    opt("the number of elements"),
                    opt("the surface area only"),
                    opt("the colour contrast"),
                ),
                "Minimize compliance (maximize stiffness) subject to a volume fraction limit.",
            ),
        ),
        "Sensitivity analysis and filtering": (
            q(
                "The compliance sensitivity dC/drho_e for SIMP is:",
                (
                    opt("non-positive - adding material never increases compliance", correct=True),
                    opt("always positive"),
                    opt("always zero"),
                    opt("undefined"),
                ),
                "Adding material can only lower or hold compliance, so the sensitivity is <= 0.",
            ),
            q(
                "A density/sensitivity filter with radius rmin is used to:",
                (
                    opt("remove checkerboarding and enforce a minimum length scale", correct=True),
                    opt("speed up the FE solve only"),
                    opt("add random noise"),
                    opt("delete the supports"),
                ),
                "Filtering cures checkerboards and mesh dependence by imposing a length scale.",
            ),
            q(
                "Without a filter, the optimized result tends to be:",
                (
                    opt("mesh-dependent - it changes as the mesh is refined", correct=True),
                    opt("perfectly mesh-independent"),
                    opt("always heavier"),
                    opt("identical to the input"),
                ),
                "Unfiltered SIMP gives finer features on finer meshes (mesh dependence).",
            ),
        ),
        "Design of experiments for exploration": (
            q(
                "A full-factorial DOE with L levels and k factors needs how many runs?",
                (
                    opt("L^k - it grows exponentially with k", correct=True),
                    opt("L times k"),
                    opt("L plus k"),
                    opt("always exactly 10"),
                ),
                "Full factorial cost is L^k, which explodes for many factors.",
            ),
            q(
                "Latin Hypercube Sampling is preferred for expensive simulations because it:",
                (
                    opt("is space-filling and needs far fewer points than a grid", correct=True),
                    opt("always uses more samples than a grid"),
                    opt("ignores the parameter ranges"),
                    opt("only works for one factor"),
                ),
                "LHS gives good space-filling coverage on a linear budget.",
            ),
            q(
                "After running a DOE, sensitivity ranking lets you:",
                (
                    opt("fix the weak factors and keep the influential ones", correct=True),
                    opt("delete the strongest factor"),
                    opt("ignore all results"),
                    opt("double the number of factors"),
                ),
                "Ranking factor influence shrinks the problem to what matters.",
            ),
        ),
        "Surrogate models for fast evaluation": (
            q(
                "A surrogate (metamodel) is used to:",
                (
                    opt(
                        "approximate the expensive solver so evaluations become near-instant",
                        correct=True,
                    ),
                    opt("replace the CAD geometry"),
                    opt("increase the solve time"),
                    opt("generate random meshes"),
                ),
                "A surrogate predicts outputs in microseconds from a modest training sample.",
            ),
            q(
                "An advantage of Kriging / Gaussian-process regression over a plain polynomial fit is that it:",
                (
                    opt("returns a predictive variance (uncertainty estimate)", correct=True),
                    opt("never needs training data"),
                    opt("ignores the samples"),
                    opt("only works in 1D"),
                ),
                "The GP variance flags where the model is least trustworthy and guides sampling.",
            ),
            q(
                "Adaptive sampling improves a surrogate by adding points where:",
                (
                    opt(
                        "the model is most uncertain or expected improvement is largest",
                        correct=True,
                    ),
                    opt("the model is already most accurate"),
                    opt("the objective is constant"),
                    opt("points are chosen at random only"),
                ),
                "Refine where variance or expected improvement is high - where it matters.",
            ),
        ),
        "Multi-objective optimization and the Pareto front": (
            q(
                "Design a dominates design b when a is:",
                (
                    opt(
                        "at least as good on every objective and strictly better on one",
                        correct=True,
                    ),
                    opt("better on exactly one objective and worse on the rest"),
                    opt("heavier than b"),
                    opt("generated before b"),
                ),
                "Domination requires no-worse-everywhere and strictly-better-somewhere.",
            ),
            q(
                "The Pareto front is:",
                (
                    opt("the set of non-dominated trade-off designs", correct=True),
                    opt("the single lightest design"),
                    opt("all infeasible designs"),
                    opt("the first generation only"),
                ),
                "The front is the non-dominated set the engineer chooses among.",
            ),
            q(
                "Which algorithm evolves a population toward the whole Pareto front in one run?",
                (
                    opt("NSGA-II", correct=True),
                    opt("Gaussian elimination"),
                    opt("the bisection method"),
                    opt("Newton-Raphson"),
                ),
                "NSGA-II uses non-dominated sorting and crowding distance to spread the front.",
            ),
        ),
        "Constraint handling in design search": (
            q(
                "The penalty method handles a constraint by:",
                (
                    opt("adding a cost for violation to the objective", correct=True),
                    opt("deleting the constraint"),
                    opt("ignoring the objective"),
                    opt("randomizing the variables"),
                ),
                "f-tilde = f + mu * max(0, g)^2 turns it into an unconstrained problem.",
            ),
            q(
                "As the penalty weight mu increases, the optimum's constraint violation:",
                (
                    opt("shrinks toward zero", correct=True),
                    opt("grows without bound"),
                    opt("stays constant"),
                    opt("becomes negative mass"),
                ),
                "Larger mu enforces the constraint harder, but stiffens the landscape.",
            ),
            q(
                "In population methods like NSGA-II, a common feasibility rule is to:",
                (
                    opt(
                        "prefer feasible designs and rank infeasible ones by total violation",
                        correct=True,
                    ),
                    opt("always prefer the most-violating design"),
                    opt("delete all feasible designs"),
                    opt("ignore constraints entirely"),
                ),
                "Feasibility-first ranking pushes the population into the feasible region.",
            ),
        ),
    },
    final=(
        q(
            "SIMP penalizes intermediate densities mainly to:",
            (
                opt("drive the result toward a clean solid/void layout", correct=True),
                opt("speed up meshing"),
                opt("add colour"),
                opt("increase compliance"),
            ),
            "The penalty exponent makes grey material inefficient, sharpening the design.",
        ),
        q(
            "A density filter with radius rmin primarily prevents:",
            (
                opt("checkerboarding and mesh dependence", correct=True),
                opt("convergence"),
                opt("any stress calculation"),
                opt("the use of FEA"),
            ),
            "Filtering enforces a minimum length scale, removing numerical artefacts.",
        ),
        q(
            "Compared with a full-factorial grid, Latin Hypercube Sampling:",
            (
                opt("covers the space well with far fewer runs", correct=True),
                opt("always needs more runs"),
                opt("ignores the ranges"),
                opt("only works for two levels"),
            ),
            "LHS is space-filling on a linear budget instead of exponential L^k.",
        ),
        q(
            "A surrogate model lets you optimize cheaply, after which you should:",
            (
                opt("verify the predicted optimum with one true solver run", correct=True),
                opt("never check it"),
                opt("delete the training data"),
                opt("discard the optimum"),
            ),
            "Optimize on the surrogate, then confirm with the expensive model.",
        ),
        q(
            "On a two-objective Pareto front, improving one objective:",
            (
                opt("necessarily worsens the other", correct=True),
                opt("improves the other too"),
                opt("leaves both unchanged"),
                opt("violates physics"),
            ),
            "The front is the locus of conflicting trade-offs.",
        ),
        q(
            "A quadratic penalty f + mu*max(0,g)^2 enforces a constraint by:",
            (
                opt("penalizing the objective when the constraint is violated", correct=True),
                opt("removing the objective"),
                opt("doubling the variables"),
                opt("freezing the optimizer"),
            ),
            "Larger mu shrinks the violation at the optimum toward zero.",
        ),
    ),
)
