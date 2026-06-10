"""Curated quiz for the 'Statistical Inference - Intermediate' course
(per-lesson checkpoints keyed by exact content-lesson title plus a final
comprehensive quiz). Kept beside the course seed so the content module stays
readable."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Hypothesis testing & p-values": (
            q(
                "What does the null hypothesis H0 represent in a hypothesis test?",
                (
                    opt("The effect you are hoping to prove is real"),
                    opt(
                        "The default assumption that nothing is going on, such as no effect or no difference",
                        correct=True,
                    ),
                    opt("The probability that the data is correct"),
                    opt("The largest acceptable sample size for the test"),
                ),
                "H0 is the default 'nothing is going on' assumption of no effect or no difference.",
            ),
            q(
                "How is the p-value defined in this lesson?",
                (
                    opt("The probability that the null hypothesis is true"),
                    opt(
                        "The probability of a result at least this extreme if H0 were true",
                        correct=True,
                    ),
                    opt("The probability that the alternative hypothesis is false"),
                    opt("The fixed cutoff alpha used to reject H0"),
                ),
                "The p-value is the probability of a result at least as extreme as observed assuming H0 is true.",
            ),
            q(
                "Which statement about p-values does the lesson warn is a misconception?",
                (
                    opt("A small p-value means the data is unlikely under H0"),
                    opt("A p-value is the probability that the null is true", correct=True),
                    opt("p-hacking and multiple comparisons inflate false positives"),
                    opt("We typically reject H0 at alpha = 0.05"),
                ),
                "The lesson stresses a p-value is NOT the probability the null is true.",
            ),
        ),
        "Errors, power & sample size": (
            q(
                "What is a Type I error?",
                (
                    opt(
                        "Rejecting H0 when it is actually true, a false positive at rate alpha",
                        correct=True,
                    ),
                    opt("Failing to reject H0 when H1 is true, a false negative"),
                    opt("Choosing too large a sample size"),
                    opt("Computing the test statistic incorrectly"),
                ),
                "A Type I error is a false positive: rejecting H0 when it is true, with rate alpha.",
            ),
            q(
                "How is statistical power defined?",
                (
                    opt("alpha, the Type I error rate"),
                    opt("beta, the Type II error rate"),
                    opt("1 minus beta, the chance of detecting a real effect", correct=True),
                    opt("The probability that H0 is true"),
                ),
                "Power equals 1 minus beta, the chance of detecting a real effect.",
            ),
            q(
                "According to the lesson, which factors increase a test's power?",
                (
                    opt("A smaller effect size and a smaller sample size"),
                    opt(
                        "A larger effect size, a larger sample size, and a larger alpha",
                        correct=True,
                    ),
                    opt("A smaller alpha and more overlap between the curves"),
                    opt("Reducing the sample size to limit Type I errors"),
                ),
                "Power grows with the effect size, the sample size, and a larger alpha.",
            ),
        ),
        "t-tests: comparing groups": (
            q(
                "What does the t-statistic measure?",
                (
                    opt(
                        "The difference between group means measured in standard errors",
                        correct=True,
                    ),
                    opt("The total variance of both groups combined"),
                    opt("The probability that the null hypothesis is true"),
                    opt("The sample size needed for adequate power"),
                ),
                "The t-statistic is the difference in means measured in standard errors of the difference.",
            ),
            q(
                "When should you use Student's t-distribution instead of the Normal?",
                (
                    opt("When the sample is large and sigma is known exactly"),
                    opt(
                        "When the sample is small and sigma is estimated from the data",
                        correct=True,
                    ),
                    opt("Only when comparing more than two groups at once"),
                    opt("Whenever the p-value is below 0.05"),
                ),
                "The t-distribution, with heavier tails, is the right reference when the sample is small and sigma is estimated from the data.",
            ),
            q(
                "What is the core idea behind every variant of the t-test?",
                (
                    opt("Maximising the sample size regardless of the effect"),
                    opt("Signal, the difference, over noise, the standard error", correct=True),
                    opt("Always assuming equal variances between the groups"),
                    opt("Replacing the Normal with a uniform distribution"),
                ),
                "Regardless of the variant, the t-test is signal (the difference) over noise (the standard error).",
            ),
        ),
        "A/B testing end to end": (
            q(
                "What is an A/B test as described in the lesson?",
                (
                    opt("A randomised experiment comparing two variants", correct=True),
                    opt("A method for estimating a single conversion rate without a control"),
                    opt("A way to compute power before collecting any data"),
                    opt("A technique that only applies to continuous measurements"),
                ),
                "An A/B test is a randomised experiment comparing two variants such as a button colour, model, or price.",
            ),
            q(
                "What typically happens to the two 95% confidence intervals as the sample size n grows?",
                (
                    opt("They widen and increasingly overlap"),
                    opt("They shrink and separate, revealing a real winner", correct=True),
                    opt("They stay exactly the same regardless of n"),
                    opt("They merge into a single combined interval"),
                ),
                "As n grows the intervals shrink and separate, indicating a real winner; with little data they overlap.",
            ),
            q(
                "Why is peeking, stopping early when results look significant, a pitfall?",
                (
                    opt("It makes the confidence intervals too narrow to read"),
                    opt("It inflates false positives", correct=True),
                    opt("It guarantees a Type II error every time"),
                    opt("It removes the need for randomisation"),
                ),
                "Peeking and stopping early when it looks significant inflates false positives.",
            ),
        ),
    },
    final=(
        q(
            "Which definition of the p-value is correct?",
            (
                opt("The probability the null hypothesis is true"),
                opt(
                    "The probability of a result at least this extreme if H0 were true",
                    correct=True,
                ),
                opt("One minus the statistical power of the test"),
                opt("The effect size divided by the standard error"),
            ),
            "The p-value is the probability of a result at least as extreme as observed if H0 is true.",
        ),
        q(
            "Which pair correctly matches the error types?",
            (
                opt("Type I is a false negative; Type II is a false positive"),
                opt(
                    "Type I is a false positive at rate alpha; Type II is a false negative at rate beta",
                    correct=True,
                ),
                opt("Type I has rate beta; Type II has rate alpha"),
                opt("Both errors share the same rate alpha"),
            ),
            "Type I is a false positive (rate alpha) and Type II is a false negative (rate beta).",
        ),
        q(
            "A t-test compares means by computing which quantity?",
            (
                opt(
                    "The difference in means divided by the standard error of the difference",
                    correct=True,
                ),
                opt("The product of the two sample means"),
                opt("The total variance minus the sample size"),
                opt("The prior belief times the likelihood"),
            ),
            "The t-statistic is the difference in means over the standard error of the difference: signal over noise.",
        ),
        q(
            "In an A/B test comparing conversion rates, what indicates a real winner rather than noise?",
            (
                opt(
                    "The two 95% confidence intervals shrink and separate as n grows", correct=True
                ),
                opt("The two confidence intervals overlap heavily"),
                opt("Stopping the test as soon as it looks significant"),
                opt("Using the smallest possible sample size"),
            ),
            "As data grows the 95% intervals shrink and separate, signalling a real winner instead of noise.",
        ),
        q(
            "Why do studies run a power analysis before collecting data?",
            (
                opt("To guarantee the p-value will be below 0.05"),
                opt(
                    "To pick a sample size big enough to catch an effect worth catching",
                    correct=True,
                ),
                opt("To eliminate the possibility of any Type I error"),
                opt("To avoid having to randomise the participants"),
            ),
            "A power analysis up front chooses a sample size large enough to detect an effect worth catching.",
        ),
    ),
)
