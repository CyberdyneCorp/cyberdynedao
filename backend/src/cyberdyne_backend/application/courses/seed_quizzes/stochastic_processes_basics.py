"""Curated quiz questions for the Random & Stochastic Processes - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Probability & random variables review": (
            q(
                "For a continuous random variable, what does the area under its PDF over an interval give?",
                (
                    opt("The height of the density at the midpoint"),
                    opt("The probability the variable falls in that interval", correct=True),
                    opt("The mean of the variable"),
                    opt("The number of samples observed"),
                ),
                "Area under the PDF over [a, b] equals P(a < X ≤ b); height alone is not probability.",
            ),
            q(
                "How are the CDF and PDF related for a continuous random variable?",
                (
                    opt("The PDF is the integral of the CDF"),
                    opt("The CDF is the derivative of the PDF"),
                    opt("The PDF is the derivative of the CDF", correct=True),
                    opt("They are unrelated quantities"),
                ),
                "F_X(x) integrates the PDF up to x, so the PDF is the derivative of the CDF.",
            ),
            q(
                "What must a valid probability density function satisfy?",
                (
                    opt("It must be nonnegative and integrate to 1 over all values", correct=True),
                    opt("It must sum to 1 and be at most 1 everywhere"),
                    opt("It must be symmetric about zero"),
                    opt("It must be a decreasing function"),
                ),
                "A PDF is nonnegative everywhere and its total integral equals 1.",
            ),
        ),
        "Expectation, variance & moments": (
            q(
                "Which identity gives the variance from moments?",
                (
                    opt("Var(X) = E[X]^2 - E[X^2]"),
                    opt("Var(X) = E[X^2] - (E[X])^2", correct=True),
                    opt("Var(X) = E[X^2] + (E[X])^2"),
                    opt("Var(X) = E[X] - E[X^2]"),
                ),
                "Variance is the second moment minus the square of the mean: E[X^2] - μ^2.",
            ),
            q(
                "How does variance scale when X is multiplied by a constant a?",
                (
                    opt("Var(aX) = a·Var(X)"),
                    opt("Var(aX) = a^2·Var(X)", correct=True),
                    opt("Var(aX) = Var(X)"),
                    opt("Var(aX) = |a|·Var(X)"),
                ),
                "Variance scales with the square of the factor, so Var(aX) = a^2 Var(X).",
            ),
            q(
                "Which property does expectation always have?",
                (
                    opt("It is linear: E[aX + b] = a·E[X] + b", correct=True),
                    opt("It equals the most likely value"),
                    opt("It is always positive"),
                    opt("It equals the median for every distribution"),
                ),
                "Expectation is linear regardless of the distribution: E[aX + b] = a E[X] + b.",
            ),
        ),
        "Common distributions": (
            q(
                "For a Poisson distribution with rate λ, what are its mean and variance?",
                (
                    opt("Mean λ, variance λ^2"),
                    opt("Both equal to λ", correct=True),
                    opt("Mean 1/λ, variance 1/λ^2"),
                    opt("Mean λ, variance 1"),
                ),
                "A Poisson distribution has mean = variance = λ.",
            ),
            q(
                "What is the mean of an exponential distribution with rate λ?",
                (
                    opt("λ"),
                    opt("λ^2"),
                    opt("1/λ", correct=True),
                    opt("1/λ^2"),
                ),
                "The exponential distribution has mean 1/λ and variance 1/λ^2.",
            ),
            q(
                "What is the relationship between Poisson counts and exponential gaps?",
                (
                    opt("They are unrelated distributions"),
                    opt(
                        "If events arrive as a Poisson count, the gaps between them are exponential",
                        correct=True,
                    ),
                    opt("Poisson gaps are uniform and exponential counts are Gaussian"),
                    opt("Both describe the spread of a Gaussian"),
                ),
                "Poisson arrivals have exponential (memoryless) inter-arrival times.",
            ),
        ),
        "Pairs of RVs: joint, conditional, covariance": (
            q(
                "What range does the correlation coefficient ρ take?",
                (
                    opt("0 to 1"),
                    opt("-1 to +1", correct=True),
                    opt("-infinity to +infinity"),
                    opt("0 to infinity"),
                ),
                "ρ normalises covariance by the standard deviations, giving a value in [-1, +1].",
            ),
            q(
                "Which statement about independence and correlation is correct?",
                (
                    opt("Uncorrelated always implies independent"),
                    opt(
                        "Independent implies uncorrelated, but uncorrelated does not generally imply independent",
                        correct=True,
                    ),
                    opt("Independent and uncorrelated are identical for all distributions"),
                    opt("Correlation has nothing to do with independence"),
                ),
                "Independence implies zero correlation; the converse holds only for jointly Gaussian RVs.",
            ),
            q(
                "When do two random variables X and Y count as independent?",
                (
                    opt("When their covariance is positive"),
                    opt("When the joint density factors as f_X(x)·f_Y(y)", correct=True),
                    opt("When they have the same mean"),
                    opt("When ρ = 1"),
                ),
                "Independence means the joint density factors into the product of the marginals.",
            ),
        ),
        "Functions of random variables": (
            q(
                "What does the law of the unconscious statistician let you compute directly?",
                (
                    opt("The PDF of Y = g(X) without integration"),
                    opt("E[g(X)] using f_X without first finding f_Y", correct=True),
                    opt("The median of g(X)"),
                    opt("The inverse function g^{-1}"),
                ),
                "E[g(X)] = ∫ g(x) f_X(x) dx, so you need only the density of X.",
            ),
            q(
                "For the linear map Y = aX + b, what is the variance of Y?",
                (
                    opt("a·Var(X)"),
                    opt("a^2·Var(X)", correct=True),
                    opt("a^2·Var(X) + b"),
                    opt("Var(X) + b^2"),
                ),
                "Adding b shifts the mean only; variance scales by a^2.",
            ),
            q(
                "Why does the change-of-variables formula include a |dx/dy| factor?",
                (
                    opt("To make the density negative where needed"),
                    opt(
                        "To conserve probability mass as the axis stretches or compresses",
                        correct=True,
                    ),
                    opt("To convert between mean and variance"),
                    opt("To normalise the correlation coefficient"),
                ),
                "The Jacobian |dx/dy| keeps total probability equal to 1 under the transform.",
            ),
        ),
        "Intro to random processes": (
            q(
                "What is a realization (sample path) of a random process?",
                (
                    opt("The process viewed at a fixed time as a random variable"),
                    opt("One deterministic function of time from a single outcome ω", correct=True),
                    opt("The average across all outcomes"),
                    opt("The variance of the process"),
                ),
                "Fixing the outcome ω gives one deterministic sample path x(t, ω).",
            ),
            q(
                "What is an ensemble average?",
                (
                    opt("An average of one sample path over time"),
                    opt("An average across many sample paths at a fixed time", correct=True),
                    opt("The peak value of a single realization"),
                    opt("The Fourier transform of one path"),
                ),
                "The ensemble average averages across realizations at a fixed time t.",
            ),
            q(
                "What does it mean for a process to be ergodic?",
                (
                    opt("Its mean is zero"),
                    opt("Time averages equal ensemble averages", correct=True),
                    opt("It has no variance"),
                    opt("All sample paths are identical"),
                ),
                "Ergodicity means a single path's time average matches the ensemble average.",
            ),
        ),
    },
    final=(
        q(
            "For a continuous random variable, probability corresponds to which feature of the PDF?",
            (
                opt("Its peak height"),
                opt("The area under it over an interval", correct=True),
                opt("Its derivative"),
                opt("Its value at zero"),
            ),
            "Probability is the area under the PDF over the interval of interest.",
        ),
        q(
            "Which expression equals the variance of X?",
            (
                opt("E[X^2] - (E[X])^2", correct=True),
                opt("(E[X])^2 - E[X^2]"),
                opt("E[X] - E[X^2]"),
                opt("E[X^2] + (E[X])^2"),
            ),
            "Variance is the second moment minus the squared mean.",
        ),
        q(
            "Which pairing of distribution and its mean is correct?",
            (
                opt("Exponential(λ) has mean λ"),
                opt("Poisson(λ) has mean λ", correct=True),
                opt("Uniform(a,b) has mean (b-a)/2"),
                opt("Gaussian(μ, σ^2) has mean σ"),
            ),
            "A Poisson(λ) has mean λ (and variance λ); the others are stated incorrectly.",
        ),
        q(
            "Two random variables are uncorrelated. What can you conclude in general?",
            (
                opt("They must be independent"),
                opt("They have no linear relationship, but may still be dependent", correct=True),
                opt("Their joint density factors automatically"),
                opt("They are identically distributed"),
            ),
            "Zero correlation rules out a linear relationship only; dependence can still exist.",
        ),
        q(
            "Under the linear transform Y = aX + b of a Gaussian X, the result is:",
            (
                opt("No longer Gaussian"),
                opt("Gaussian with mean aμ + b and variance a^2 σ^2", correct=True),
                opt("Gaussian with mean μ and variance σ^2 unchanged"),
                opt("Uniform on [a, b]"),
            ),
            "A linear map of a Gaussian stays Gaussian; the mean and variance transform accordingly.",
        ),
        q(
            "A random process is best described as:",
            (
                opt("A single fixed function of time"),
                opt(
                    "A family of random variables indexed by time, with an ensemble of paths",
                    correct=True,
                ),
                opt("A constant equal to its mean"),
                opt("The Fourier transform of a deterministic signal"),
            ),
            "A stochastic process is a time-indexed family of RVs whose realizations form an ensemble.",
        ),
    ),
)
