"""Quiz questions for the Mathematics for Life Sciences - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Integration: accumulating change": (
            q(
                "What does the definite integral of a function over an interval represent?",
                (
                    opt("The signed area under the curve over that interval", correct=True),
                    opt("The slope of the curve"),
                    opt("The maximum value of the curve"),
                    opt("The number of roots of the function"),
                ),
                "A definite integral is the signed area under the curve.",
            ),
            q(
                "In pharmacokinetics, what does the AUC of a plasma concentration curve measure?",
                (
                    opt("Total systemic drug exposure over time", correct=True),
                    opt("The peak concentration"),
                    opt("The half-life"),
                    opt("The volume of distribution"),
                ),
                "AUC, the integral of concentration over time, measures total exposure.",
            ),
            q(
                "What does the Fundamental Theorem of Calculus connect?",
                (
                    opt("Integration and differentiation as inverse operations", correct=True),
                    opt("Addition and multiplication"),
                    opt("Vectors and matrices"),
                    opt("Mean and variance"),
                ),
                "The theorem ties the integral to the antiderivative F(b) - F(a).",
            ),
        ),
        "Vectors and matrices for biological systems": (
            q(
                "In a Leslie/Lefkovitch matrix model, what does Mn (matrix times vector) compute?",
                (
                    opt("The population stage vector at the next time step", correct=True),
                    opt("The total area under a curve"),
                    opt("A single scalar growth rate"),
                    opt("The variance of the data"),
                ),
                "The projection matrix maps the current stage vector to the next.",
            ),
            q(
                "What do the sub-diagonal entries of a Leslie matrix typically encode?",
                (
                    opt("Survival probabilities between stages", correct=True),
                    opt("Fecundities only"),
                    opt("Drug clearance"),
                    opt("Random noise"),
                ),
                "Sub-diagonal entries are stage-to-stage survival; the top row is fecundity.",
            ),
            q(
                "A vector in a stage-structured model holds what?",
                (
                    opt("The abundances of several life stages at once", correct=True),
                    opt("A single number"),
                    opt("Only the growth rate"),
                    opt("The carrying capacity"),
                ),
                "A vector collects the abundances of each stage.",
            ),
        ),
        "Eigenvalues and long-run population growth": (
            q(
                "For an eigenvector v of matrix A, what is true?",
                (
                    opt("A v = lambda v: A only rescales v by the eigenvalue lambda", correct=True),
                    opt("A v is always zero"),
                    opt("A rotates v by 90 degrees"),
                    opt("v has no relation to A"),
                ),
                "An eigenvector is only stretched by its eigenvalue, not rotated.",
            ),
            q(
                "What does the dominant eigenvalue of a Leslie matrix give?",
                (
                    opt("The asymptotic (long-run) growth rate per time step", correct=True),
                    opt("The carrying capacity"),
                    opt("The half-life"),
                    opt("The variance"),
                ),
                "The dominant eigenvalue is the long-run multiplicative growth rate.",
            ),
            q(
                "An equilibrium of an ODE system is stable when the Jacobian eigenvalues satisfy what?",
                (
                    opt("All have negative real part", correct=True),
                    opt("All are positive"),
                    opt("They sum to one"),
                    opt("They are all complex"),
                ),
                "Negative real parts mean perturbations decay, so the equilibrium is stable.",
            ),
        ),
        "Probability and distributions in biology": (
            q(
                "Which distribution best models counts of rare independent events, like mutations per genome?",
                (
                    opt("Poisson", correct=True),
                    opt("Normal"),
                    opt("Uniform"),
                    opt("Exponential"),
                ),
                "The Poisson distribution models counts of rare independent events.",
            ),
            q(
                "For a Poisson distribution, the variance equals what?",
                (
                    opt("Its mean lambda", correct=True),
                    opt("Zero"),
                    opt("The square of the mean"),
                    opt("One always"),
                ),
                "A defining property of the Poisson is that variance equals the mean.",
            ),
            q(
                "Why does the normal distribution arise so often for continuous traits?",
                (
                    opt(
                        "By the Central Limit Theorem, sums of many small effects tend to be normal",
                        correct=True,
                    ),
                    opt("Because all biology is exactly Gaussian"),
                    opt("Because it has no variance"),
                    opt("Because counts are always normal"),
                ),
                "The CLT makes sums/averages of many small independent effects approximately normal.",
            ),
        ),
        "Linear regression and curve fitting": (
            q(
                "What does ordinary least-squares regression minimise?",
                (
                    opt("The sum of squared residuals between data and the line", correct=True),
                    opt("The number of data points"),
                    opt("The slope of the line"),
                    opt("The maximum residual only"),
                ),
                "Least squares minimises the sum of squared residuals.",
            ),
            q(
                "What does R-squared report?",
                (
                    opt("The fraction of variance in y explained by the model", correct=True),
                    opt("The slope of the regression line"),
                    opt("The number of parameters"),
                    opt("The mean of x"),
                ),
                "R-squared is the proportion of variance explained.",
            ),
            q(
                "Why is fitting Michaelis-Menten by nonlinear least squares preferred over a Lineweaver-Burk plot?",
                (
                    opt(
                        "The reciprocal transform distorts the error structure and biases estimates",
                        correct=True,
                    ),
                    opt("Nonlinear fitting is always less accurate"),
                    opt("Lineweaver-Burk needs no data"),
                    opt("Nonlinear fitting ignores the data"),
                ),
                "Double-reciprocal plots distort errors; direct nonlinear fitting is unbiased.",
            ),
        ),
        "First-order differential equations": (
            q(
                "A differential equation specifies what about a quantity?",
                (
                    opt("Its rate of change rather than its value directly", correct=True),
                    opt("Only its final value"),
                    opt("Its variance"),
                    opt("Its units"),
                ),
                "A differential equation describes how fast a quantity changes.",
            ),
            q(
                "In the logistic equation dN/dt = r N (1 - N/K), what is K?",
                (
                    opt(
                        "The carrying capacity, the ceiling the population approaches", correct=True
                    ),
                    opt("The growth rate"),
                    opt("The doubling time"),
                    opt("The initial population"),
                ),
                "K is the carrying capacity at which growth stops.",
            ),
            q(
                "The solution of dC/dt = -k C is which function?",
                (
                    opt("C(t) = C0 exp(-k t), first-order exponential decay", correct=True),
                    opt("C(t) = C0 + k t, linear growth"),
                    opt("C(t) = C0 t squared"),
                    opt("A constant"),
                ),
                "First-order decay gives an exponential solution.",
            ),
        ),
    },
    final=(
        q(
            "The AUC of a single-dose curve C0 exp(-k t) integrated from 0 to infinity equals what?",
            (
                opt("C0 / k", correct=True),
                opt("C0 times k"),
                opt("k / C0"),
                opt("C0 only"),
            ),
            "Integrating C0 exp(-k t) from 0 to infinity gives C0/k.",
        ),
        q(
            "The dominant eigenvalue of a projection matrix being greater than 1 implies what?",
            (
                opt("Long-run population growth", correct=True),
                opt("Long-run decline"),
                opt("A stationary population"),
                opt("Extinction immediately"),
            ),
            "A dominant eigenvalue above 1 means the population grows in the long run.",
        ),
        q(
            "Count data such as colonies per plate are best modelled with which distribution?",
            (
                opt("Poisson", correct=True),
                opt("Normal"),
                opt("Uniform"),
                opt("Binomial with n = 1"),
            ),
            "Counts of rare events fit a Poisson (or negative binomial) model.",
        ),
        q(
            "Nonlinear least squares fits a model by minimising what?",
            (
                opt("The sum of squared residuals between data and model", correct=True),
                opt("The number of parameters"),
                opt("The mean of the predictors"),
                opt("The maximum of the data"),
            ),
            "It minimises squared residuals, like linear least squares but for nonlinear models.",
        ),
        q(
            "The logistic differential equation produces what shape of solution?",
            (
                opt("An S-shaped curve approaching the carrying capacity", correct=True),
                opt("A straight line"),
                opt("An unbounded exponential"),
                opt("A decaying exponential"),
            ),
            "Logistic growth gives an S-shaped curve leveling off at K.",
        ),
        q(
            "What is the eigenvector associated with the dominant eigenvalue of a Leslie matrix called?",
            (
                opt("The stable stage distribution", correct=True),
                opt("The carrying capacity"),
                opt("The Jacobian"),
                opt("The residual vector"),
            ),
            "The dominant eigenvector gives the stable stage distribution.",
        ),
    ),
)
