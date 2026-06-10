from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Probability, events & the long run": (
            q(
                "On the probability scale described, what value represents a certain event?",
                (
                    opt("0"),
                    opt("0.5"),
                    opt("1", correct=True),
                    opt("100"),
                ),
                "Probability runs from 0 (impossible) to 1 (certain).",
            ),
            q(
                "What is the complement rule for an event A?",
                (
                    opt("P(not A) = 1 - P(A)", correct=True),
                    opt("P(not A) = P(A) - 1"),
                    opt("P(not A) = 1 + P(A)"),
                    opt("P(not A) = P(A)"),
                ),
                "The complement rule states P(not A) = 1 - P(A).",
            ),
            q(
                "What does the Law of Large Numbers say about flipping a fair coin many times?",
                (
                    opt("The number of heads always equals the number of tails"),
                    opt("The fraction of heads settles toward 0.5", correct=True),
                    opt("The fraction of heads grows without bound"),
                    opt("Each flip becomes more likely to be heads"),
                ),
                "The fraction of heads converges toward the true probability 0.5 as trials increase.",
            ),
        ),
        "Random variables: expectation & variance": (
            q(
                "What is the expectation E[X] of a fair die roll according to the lesson?",
                (
                    opt("3.5", correct=True),
                    opt("6"),
                    opt("1"),
                    opt("3"),
                ),
                "A fair die has E[X] = 3.5, the long-run average and balance point.",
            ),
            q(
                "How is the standard deviation sigma related to the variance?",
                (
                    opt("It is the square of the variance"),
                    opt("It is the square root of the variance", correct=True),
                    opt("It equals the variance exactly"),
                    opt("It is half the variance"),
                ),
                "The standard deviation sigma is the square root of the variance.",
            ),
            q(
                "By linearity of expectation, what is E[aX + b]?",
                (
                    opt("a E[X] + b", correct=True),
                    opt("a E[X]"),
                    opt("E[X] + b"),
                    opt("a (E[X] + b)"),
                ),
                "Linearity gives E[aX + b] = a E[X] + b.",
            ),
        ),
        "Distributions you'll actually use": (
            q(
                "Which distribution models the waiting time until the next event and is memoryless?",
                (
                    opt("Exponential", correct=True),
                    opt("Binomial"),
                    opt("Uniform"),
                    opt("Normal"),
                ),
                "The Exponential distribution models waiting time until the next event and is memoryless.",
            ),
            q(
                "The Poisson distribution is described by how many parameters?",
                (
                    opt("One parameter, the rate lambda", correct=True),
                    opt("Two parameters, mean and variance"),
                    opt("No parameters"),
                    opt("Three parameters"),
                ),
                "Poisson has a single parameter, the rate lambda.",
            ),
            q(
                "For the Exponential distribution with rate lambda, what is E[X]?",
                (
                    opt("1/lambda", correct=True),
                    opt("lambda"),
                    opt("lambda^2"),
                    opt("2/lambda"),
                ),
                "The Exponential distribution has mean E[X] = 1/lambda.",
            ),
        ),
        "Bayes' theorem & inference": (
            q(
                "Bayes' theorem expresses the posterior as proportional to which combination?",
                (
                    opt("likelihood times prior", correct=True),
                    opt("prior divided by likelihood"),
                    opt("likelihood minus prior"),
                    opt("prior plus evidence"),
                ),
                "Bayes gives posterior proportional to likelihood times prior.",
            ),
            q(
                "In the medical-test example with a 99% accurate test and a 1% disease rate, P(sick | positive) is about what?",
                (
                    opt("99%"),
                    opt("50%", correct=True),
                    opt("1%"),
                    opt("90%"),
                ),
                "Because false positives swamp true positives at a low base rate, P(sick | positive) is about 50%.",
            ),
            q(
                "In the base-rate trap, what dominates when a condition is rare?",
                (
                    opt("The prior", correct=True),
                    opt("The likelihood"),
                    opt("The sample size"),
                    opt("The standard deviation"),
                ),
                "Rare conditions make even good tests misleading because the prior dominates.",
            ),
        ),
        "Sampling & the Central Limit Theorem": (
            q(
                "According to the Central Limit Theorem, for large n the sample mean is approximately what?",
                (
                    opt("Normal", correct=True),
                    opt("Uniform"),
                    opt("Exponential"),
                    opt("Poisson"),
                ),
                "The CLT says the sample mean is approximately Normal for large n regardless of the original distribution.",
            ),
            q(
                "Under the CLT, the standard deviation of the sample mean is what?",
                (
                    opt("sigma / sqrt(n)", correct=True),
                    opt("sigma times n"),
                    opt("sigma / n"),
                    opt("sigma times sqrt(n)"),
                ),
                "The sample mean has standard deviation sigma / sqrt(n).",
            ),
            q(
                "Because of the sqrt(n) law, how much more data do you need to halve your error?",
                (
                    opt("Twice the data"),
                    opt("Four times the data", correct=True),
                    opt("The same amount"),
                    opt("Ten times the data"),
                ),
                "To halve the error you need four times the data, by the sqrt(n) law.",
            ),
        ),
        "Monte-Carlo lab: estimate π, mean/variance & Bayes": (
            q(
                "How does the lab estimate pi from darts thrown in a unit square?",
                (
                    opt("The fraction inside the quarter circle times 4", correct=True),
                    opt("The fraction inside the quarter circle times pi"),
                    opt("The total number of darts divided by 4"),
                    opt("The fraction outside the circle times 2"),
                ),
                "Pi is estimated as the fraction of darts inside the quarter circle multiplied by 4.",
            ),
            q(
                "For the uniform draws, what mean and variance does the lab expect?",
                (
                    opt("mean 0.5 and variance 0.0833", correct=True),
                    opt("mean 0 and variance 1"),
                    opt("mean 1 and variance 0.5"),
                    opt("mean 0.5 and variance 0.5"),
                ),
                "Uniform draws on [0,1) have mean 0.5 and variance 1/12 = 0.0833.",
            ),
            q(
                "With a Beta(1,1) prior, after H heads and T tails the posterior mean of P(heads) is what?",
                (
                    opt("(1 + H) / (2 + H + T)", correct=True),
                    opt("H / (H + T)"),
                    opt("(1 + H) / (1 + H + T)"),
                    opt("H / (2 + H + T)"),
                ),
                "Starting from Beta(1,1), the posterior mean is (1 + H) / (2 + H + T).",
            ),
        ),
    },
    final=(
        q(
            "What is the addition rule for P(A or B)?",
            (
                opt("P(A) + P(B) - P(A and B)", correct=True),
                opt("P(A) + P(B)"),
                opt("P(A) P(B)"),
                opt("P(A) - P(B)"),
            ),
            "The addition rule is P(A or B) = P(A) + P(B) - P(A and B).",
        ),
        q(
            "Which formula gives the variance of X?",
            (
                opt("E[X^2] - mu^2", correct=True),
                opt("E[X] - mu"),
                opt("(E[X])^2 - E[X^2]"),
                opt("mu^2 - E[X^2]"),
            ),
            "Variance equals E[(X - mu)^2] = E[X^2] - mu^2.",
        ),
        q(
            "Which distribution is the bell curve that arises as the limit in the Central Limit Theorem?",
            (
                opt("Normal (Gaussian)", correct=True),
                opt("Poisson"),
                opt("Exponential"),
                opt("Bernoulli"),
            ),
            "The Normal (Gaussian) is the bell curve and the limiting distribution in the CLT.",
        ),
        q(
            "What is a 95% confidence interval roughly equal to?",
            (
                opt("x-bar plus or minus 1.96 sigma / sqrt(n)", correct=True),
                opt("x-bar plus or minus sigma"),
                opt("x-bar plus or minus 1.96 sigma times n"),
                opt("x-bar plus or minus 1.96 sigma"),
            ),
            "A 95% confidence interval is roughly x-bar plus or minus 1.96 sigma / sqrt(n).",
        ),
        q(
            "Why do Monte-Carlo simulation, casinos, and A/B tests work?",
            (
                opt("With enough samples the average becomes reliable", correct=True),
                opt("Because each individual trial is perfectly predictable"),
                opt("Because probabilities change over time"),
                opt("Because variance grows with more samples"),
            ),
            "By the Law of Large Numbers, enough samples make the average reliable.",
        ),
    ),
)
