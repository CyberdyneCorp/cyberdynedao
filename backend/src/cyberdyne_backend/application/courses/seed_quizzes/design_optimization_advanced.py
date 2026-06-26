"""Quiz questions for the Engineering Design Optimization - Advanced course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Multi-objective optimization and Pareto fronts": (
            q(
                "Design A dominates design B when A is:",
                (
                    opt(
                        "at least as good on every objective and strictly better on one",
                        correct=True,
                    ),
                    opt("better on exactly one objective and worse on the rest"),
                    opt("equal to B on all objectives"),
                    opt("cheaper to manufacture only"),
                ),
                "Dominance requires no objective worse and at least one strictly better.",
            ),
            q(
                "The Pareto front is the set of:",
                (
                    opt("non-dominated trade-off solutions", correct=True),
                    opt("all infeasible designs"),
                    opt("the single global optimum"),
                    opt("dominated solutions only"),
                ),
                "On the front you can only improve one objective by worsening another.",
            ),
            q(
                "A weighted-sum scalarization can fail to find:",
                (
                    opt("points on a non-convex part of the Pareto front", correct=True),
                    opt("any feasible design at all"),
                    opt("the cheapest design"),
                    opt("the constraint boundaries"),
                ),
                "Weighted sums miss non-convex regions, motivating dominance-based methods.",
            ),
        ),
        "Surrogate-based optimization": (
            q(
                "Surrogate-based optimization is most useful when:",
                (
                    opt("each true objective evaluation is very expensive", correct=True),
                    opt("the objective is free to evaluate millions of times"),
                    opt("there are no constraints"),
                    opt("the function is exactly linear"),
                ),
                "It replaces costly simulations with a cheap fitted model.",
            ),
            q(
                "A common choice for the initial sampling plan is a:",
                (
                    opt("Latin-hypercube design of experiments", correct=True),
                    opt("single point at the origin"),
                    opt("full gradient evaluation"),
                    opt("random walk of one step"),
                ),
                "Latin hypercube spreads samples well across the space.",
            ),
            q(
                "Examples of surrogate models include:",
                (
                    opt("response surfaces, radial basis functions and Kriging", correct=True),
                    opt("Newton steps and line searches"),
                    opt("crossover and mutation"),
                    opt("KKT multipliers"),
                ),
                "These fit cheap approximations of the expensive response.",
            ),
        ),
        "Bayesian optimization and acquisition functions": (
            q(
                "The surrogate at the heart of Bayesian optimization is a:",
                (
                    opt("Gaussian process giving a mean and an uncertainty", correct=True),
                    opt("linear regression with no uncertainty"),
                    opt("genetic algorithm"),
                    opt("finite-element model"),
                ),
                "A GP predicts both mean and variance at every point.",
            ),
            q(
                "An acquisition function decides where to sample next by balancing:",
                (
                    opt("exploitation against exploration", correct=True),
                    opt("mass against stiffness"),
                    opt("crossover against mutation"),
                    opt("primal against dual feasibility"),
                ),
                "It trades sampling where the mean is good against where uncertainty is high.",
            ),
            q(
                "Expected Improvement rewards points that are likely to:",
                (
                    opt("beat the best objective value seen so far", correct=True),
                    opt("maximize the model variance only"),
                    opt("lie exactly at a sampled point"),
                    opt("violate every constraint"),
                ),
                "EI measures expected gain over the current best.",
            ),
        ),
        "Robust and reliability-based design optimization": (
            q(
                "Robust Design Optimization (RDO) typically minimizes:",
                (
                    opt("a blend of the mean and standard deviation of the response", correct=True),
                    opt("only the nominal value, ignoring scatter"),
                    opt("the number of design variables"),
                    opt("the gradient norm"),
                ),
                "RDO seeks performance insensitive to variation: mu + k*sigma.",
            ),
            q(
                "Reliability-Based Design Optimization (RBDO) enforces that:",
                (
                    opt(
                        "the probability of constraint violation stays below a target", correct=True
                    ),
                    opt("all variables are deterministic"),
                    opt("the objective gradient is zero"),
                    opt("the front is convex"),
                ),
                "RBDO uses chance constraints like P[g>0] <= Pf.",
            ),
            q(
                "Compared with a deterministic optimum on a constraint, a reliable design is:",
                (
                    opt(
                        "pulled back from the boundary by a margin sized to the scatter",
                        correct=True,
                    ),
                    opt("pushed further past the boundary"),
                    opt("identical in every case"),
                    opt("always infeasible"),
                ),
                "The margin reflects the actual uncertainty, not a blanket safety factor.",
            ),
        ),
        "Topology optimization": (
            q(
                "Topology optimization decides:",
                (
                    opt("where material should exist within a design domain", correct=True),
                    opt("only the diameter of a fixed rod"),
                    opt("the color of the part"),
                    opt("the solver tolerance"),
                ),
                "Element densities are driven toward solid or void.",
            ),
            q(
                "The SIMP scheme penalizes intermediate densities using:",
                (
                    opt("E = rho^p * E0 with p around 3", correct=True),
                    opt("E = rho * E0 strictly linear"),
                    opt("E independent of rho"),
                    opt("E = exp(rho)"),
                ),
                "The power-law penalty makes grey densities inefficient.",
            ),
            q(
                "A sensitivity (density) filter is applied mainly to:",
                (
                    opt("prevent checkerboarding and mesh dependence", correct=True),
                    opt("increase the volume budget"),
                    opt("make the problem convex"),
                    opt("remove all constraints"),
                ),
                "Filtering regularizes the layout for manufacturable results.",
            ),
        ),
        "Adjoint methods and automatic differentiation": (
            q(
                "The key advantage of the adjoint method is that the gradient cost is:",
                (
                    opt("essentially independent of the number of design variables", correct=True),
                    opt("proportional to the number of variables"),
                    opt("always zero"),
                    opt("proportional to the number of objectives squared"),
                ),
                "One extra linear solve yields the full gradient regardless of n.",
            ),
            q(
                "Finite-difference gradients for n variables require about:",
                (
                    opt("n + 1 solver evaluations and are noisy", correct=True),
                    opt("a single evaluation, exactly"),
                    opt("no evaluations at all"),
                    opt("two evaluations regardless of n"),
                ),
                "Each variable needs a perturbed run, so cost scales with n.",
            ),
            q(
                "Reverse-mode automatic differentiation is the discrete analogue of the:",
                (
                    opt("adjoint method", correct=True),
                    opt("finite-difference method"),
                    opt("genetic algorithm"),
                    opt("Latin-hypercube design"),
                ),
                "One backward sweep gives gradients for all inputs, like the adjoint.",
            ),
        ),
    },
    final=(
        q(
            "The Pareto front consists of:",
            (
                opt("non-dominated trade-off solutions", correct=True),
                opt("the single best design"),
                opt("all dominated designs"),
                opt("only infeasible designs"),
            ),
            "Improving one objective on the front costs another.",
        ),
        q(
            "Surrogate-based optimization is motivated by:",
            (
                opt(
                    "expensive simulations that cannot be evaluated thousands of times",
                    correct=True,
                ),
                opt("functions that are free to evaluate"),
                opt("the absence of any objective"),
                opt("strictly linear problems"),
            ),
            "A cheap fitted model stands in for the costly truth.",
        ),
        q(
            "In Bayesian optimization, the next sample is chosen by:",
            (
                opt(
                    "maximizing an acquisition function such as Expected Improvement", correct=True
                ),
                opt("picking a random feasible point"),
                opt("taking a Newton step"),
                opt("evaluating the gradient norm"),
            ),
            "Acquisition balances exploration and exploitation.",
        ),
        q(
            "RBDO enforces reliability by:",
            (
                opt("keeping the probability of constraint violation below a target", correct=True),
                opt("ignoring uncertainty entirely"),
                opt("minimizing only the mean"),
                opt("setting all multipliers to zero"),
            ),
            "It uses chance constraints like P[g>0] <= Pf.",
        ),
        q(
            "SIMP in topology optimization penalizes intermediate densities via:",
            (
                opt("E = rho^p * E0 with p around 3", correct=True),
                opt("a strictly linear E = rho * E0"),
                opt("constant stiffness"),
                opt("a negative exponent"),
            ),
            "The power law pushes densities to solid or void.",
        ),
        q(
            "The adjoint method (and reverse-mode AD) computes gradients at a cost that is:",
            (
                opt("nearly independent of the number of design variables", correct=True),
                opt("proportional to the number of variables"),
                opt("quadratic in the number of constraints"),
                opt("always larger than finite differences"),
            ),
            "This is why they scale to thousands of variables.",
        ),
    ),
)
