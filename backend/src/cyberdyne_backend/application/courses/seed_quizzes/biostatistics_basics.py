"""Quiz questions for the Statistics & Biostatistics - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Data types & study designs": (
            q(
                "Tumour grade recorded as I, II, III, IV is what kind of variable?",
                (
                    opt("Ordinal categorical", correct=True),
                    opt("Nominal categorical"),
                    opt("Continuous numerical"),
                    opt("Discrete count"),
                ),
                "The grades have a meaningful order but are categories, not measured quantities.",
            ),
            q(
                "Which design best supports a causal claim about a treatment?",
                (
                    opt("Randomised controlled trial", correct=True),
                    opt("Cross-sectional survey"),
                    opt("Retrospective case-control study"),
                    opt("Observational cohort study"),
                ),
                "Randomisation and intervention break confounding, so the RCT supports causal inference.",
            ),
            q(
                "The main threat to causal interpretation in observational studies is:",
                (
                    opt("Confounding", correct=True),
                    opt("Rounding error"),
                    opt("Too large a sample"),
                    opt("Using the median"),
                ),
                "Observed associations may be driven by an unmeasured common cause (confounder).",
            ),
        ),
        "Describing data: centre & spread": (
            q(
                "Which summary of centre is most robust to outliers?",
                (
                    opt("Median", correct=True),
                    opt("Mean"),
                    opt("Sum"),
                    opt("Range"),
                ),
                "The median depends only on the middle value, so extreme points barely move it.",
            ),
            q(
                "For strongly right-skewed incubation times, the best centre+spread pair is:",
                (
                    opt("Median and IQR", correct=True),
                    opt("Mean and standard deviation"),
                    opt("Mode and range"),
                    opt("Mean and variance"),
                ),
                "Skew pulls the mean and SD around; median + IQR are robust to skew.",
            ),
            q(
                "The sample variance uses a divisor of:",
                (
                    opt("n minus 1", correct=True),
                    opt("n"),
                    opt("n plus 1"),
                    opt("the square root of n"),
                ),
                "Dividing by n-1 (Bessel's correction) gives an unbiased estimate of the variance.",
            ),
        ),
        "Probability essentials": (
            q(
                "Events A and B are independent when:",
                (
                    opt("P(A and B) = P(A) times P(B)", correct=True),
                    opt("P(A and B) = P(A) + P(B)"),
                    opt("P(A) = P(B)"),
                    opt("P(A or B) = 1"),
                ),
                "Independence means the joint probability factorises into the product.",
            ),
            q(
                "Why does an accurate test for a rare disease still give many false positives?",
                (
                    opt(
                        "The low prevalence makes false positives numerous relative to true positives",
                        correct=True,
                    ),
                    opt("Sensitivity is always low"),
                    opt("Specificity cannot exceed prevalence"),
                    opt("Bayes' theorem does not apply to medicine"),
                ),
                "With a low base rate, even a small false-positive rate produces many positives among the healthy majority.",
            ),
            q(
                "Sensitivity of a diagnostic test is defined as:",
                (
                    opt("P(test positive | disease)", correct=True),
                    opt("P(disease | test positive)"),
                    opt("P(test negative | no disease)"),
                    opt("P(no disease)"),
                ),
                "Sensitivity is the true-positive rate among those who have the disease.",
            ),
        ),
        "Discrete distributions: Binomial & Poisson": (
            q(
                "The number of patients responding out of 20, each independently with probability p, follows a:",
                (
                    opt("Binomial distribution", correct=True),
                    opt("Poisson distribution"),
                    opt("Normal distribution"),
                    opt("Uniform distribution"),
                ),
                "A fixed number of independent yes/no trials with constant p is Binomial.",
            ),
            q(
                "For a Poisson distribution, the mean and variance are:",
                (
                    opt("Equal (both lambda)", correct=True),
                    opt("Mean lambda, variance lambda squared"),
                    opt("Mean np, variance np(1-p)"),
                    opt("Unrelated"),
                ),
                "A defining property of the Poisson is mean = variance = lambda.",
            ),
            q(
                "RNA-seq counts with variance much larger than the mean are called:",
                (
                    opt("Overdispersed", correct=True),
                    opt("Underdispersed"),
                    opt("Perfectly Poisson"),
                    opt("Normally distributed"),
                ),
                "Variance exceeding the mean is overdispersion, often modelled by the negative binomial.",
            ),
        ),
        "The Normal distribution & the CLT": (
            q(
                "Approximately what fraction of a Normal distribution lies within one standard deviation of the mean?",
                (
                    opt("About 68%", correct=True),
                    opt("About 50%"),
                    opt("About 95%"),
                    opt("About 99.7%"),
                ),
                "The 68-95-99.7 rule: ~68% within 1 SD, ~95% within 2 SD.",
            ),
            q(
                "The Central Limit Theorem says the sample mean is approximately Normal:",
                (
                    opt("For almost any population shape, given large enough n", correct=True),
                    opt("Only if the population is already Normal"),
                    opt("Only for proportions"),
                    opt("Only when n is very small"),
                ),
                "The CLT holds regardless of population shape once n is moderately large.",
            ),
            q(
                "A z-score is computed as:",
                (
                    opt("(x minus mu) divided by sigma", correct=True),
                    opt("(x minus mu) times sigma"),
                    opt("x divided by sigma"),
                    opt("mu divided by x"),
                ),
                "Standardising subtracts the mean and divides by the standard deviation.",
            ),
        ),
    },
    final=(
        q(
            "A case-control study is best described as:",
            (
                opt("Observational", correct=True),
                opt("Experimental"),
                opt("A randomised trial"),
                opt("A power calculation"),
            ),
            "Case-control studies observe groups defined by outcome; they do not intervene.",
        ),
        q(
            "Which pair correctly matches a measure of centre with a measure of spread?",
            (
                opt("Median with IQR", correct=True),
                opt("Mean with IQR"),
                opt("Median with standard deviation"),
                opt("Mode with variance"),
            ),
            "The median naturally pairs with the IQR; the mean pairs with the standard deviation.",
        ),
        q(
            "Bayes' theorem is used to compute:",
            (
                opt("A posterior probability from a prior and likelihood", correct=True),
                opt("The mean of a sample"),
                opt("The variance of a Poisson"),
                opt("A confidence interval width"),
            ),
            "Bayes combines the prior and likelihood (via the evidence) into the posterior.",
        ),
        q(
            "The Poisson distribution is a good model for:",
            (
                opt("Counts of rare events in a fixed window", correct=True),
                opt("Continuous blood pressure"),
                opt("The proportion responding to therapy"),
                opt("A categorical blood type"),
            ),
            "Poisson counts independent rare events over a fixed exposure (mutations, arrivals).",
        ),
        q(
            "As sample size n increases, the standard error of the mean:",
            (
                opt("Decreases as 1 over the square root of n", correct=True),
                opt("Increases linearly with n"),
                opt("Stays constant"),
                opt("Decreases as 1 over n"),
            ),
            "Standard error is sigma / sqrt(n), so it shrinks only as the square root of n.",
        ),
        q(
            "Which statement about the Normal distribution is correct?",
            (
                opt(
                    "About 95% of values lie within two standard deviations of the mean",
                    correct=True,
                ),
                opt("It is defined only for counts"),
                opt("Its mean and median always differ"),
                opt("It has no standard deviation"),
            ),
            "By the empirical rule, ~95% of a Normal lies within 2 SD of the mean.",
        ),
    ),
)
