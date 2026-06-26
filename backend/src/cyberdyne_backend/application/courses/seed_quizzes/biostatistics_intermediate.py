"""Quiz questions for the Statistics & Biostatistics - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Estimation & confidence intervals": (
            q(
                "The correct interpretation of a 95% confidence interval is:",
                (
                    opt(
                        "Over many repeated samples, 95% of such intervals contain the parameter",
                        correct=True,
                    ),
                    opt("There is a 95% probability the parameter is in this one interval"),
                    opt("95% of the data fall in the interval"),
                    opt("The interval is correct 95% of the time for the sample mean"),
                ),
                "The 95% is a property of the procedure across repeated samples, not of a single interval.",
            ),
            q(
                "When n is small and sigma is unknown, the CI for a mean uses critical values from the:",
                (
                    opt("Student-t distribution", correct=True),
                    opt("Standard Normal only"),
                    opt("Chi-square distribution"),
                    opt("Poisson distribution"),
                ),
                "Estimating sigma from small samples requires the wider Student-t distribution.",
            ),
            q(
                "To halve the margin of error of a mean, you must:",
                (
                    opt("Quadruple the sample size", correct=True),
                    opt("Double the sample size"),
                    opt("Halve the sample size"),
                    opt("Increase alpha"),
                ),
                "Margin scales as 1/sqrt(n), so halving it needs 4x the data.",
            ),
        ),
        "Hypothesis testing & p-values": (
            q(
                "A p-value is:",
                (
                    opt(
                        "The probability of data at least this extreme if the null is true",
                        correct=True,
                    ),
                    opt("The probability that the null hypothesis is true"),
                    opt("The probability of a Type II error"),
                    opt("The size of the effect"),
                ),
                "It is computed assuming the null and measures how surprising the data are, not P(H0).",
            ),
            q(
                "A Type I error is:",
                (
                    opt("Rejecting a true null hypothesis (false positive)", correct=True),
                    opt("Failing to reject a false null"),
                    opt("Using the wrong test statistic"),
                    opt("A miscalculated mean"),
                ),
                "Type I error is the false-positive rate, controlled at level alpha.",
            ),
            q(
                "Statistical power is defined as:",
                (
                    opt("1 minus beta", correct=True),
                    opt("alpha"),
                    opt("1 minus alpha"),
                    opt("beta"),
                ),
                "Power is the probability of detecting a real effect, 1 - beta.",
            ),
        ),
        "t-tests & ANOVA": (
            q(
                "A paired t-test is appropriate when:",
                (
                    opt("The same subjects are measured before and after", correct=True),
                    opt("Two independent groups are compared"),
                    opt("There are five or more groups"),
                    opt("The outcome is categorical"),
                ),
                "Pairing removes between-subject variation by comparing within-subject differences.",
            ),
            q(
                "Why use ANOVA instead of many pairwise t-tests across several groups?",
                (
                    opt("Repeated t-tests inflate the overall false-positive rate", correct=True),
                    opt("t-tests cannot compute a mean"),
                    opt("ANOVA needs no assumptions"),
                    opt("ANOVA is only for two groups"),
                ),
                "Multiple tests inflate Type I error; ANOVA provides one global test of equality.",
            ),
            q(
                "The ANOVA F-statistic is a ratio of:",
                (
                    opt("Between-group variance to within-group variance", correct=True),
                    opt("Within-group variance to between-group variance"),
                    opt("Mean to standard deviation"),
                    opt("Observed to expected counts"),
                ),
                "A large F means group means vary more than would be expected from within-group noise.",
            ),
        ),
        "Categorical data & the chi-square test": (
            q(
                "The chi-square test of independence compares:",
                (
                    opt("Observed counts to counts expected under independence", correct=True),
                    opt("Two sample means"),
                    opt("Survival curves"),
                    opt("Regression slopes"),
                ),
                "Chi-square sums (O - E)^2 / E across the contingency table.",
            ),
            q(
                "For a sparse 2x2 table with small expected counts, the better choice is:",
                (
                    opt("Fisher's exact test", correct=True),
                    opt("A paired t-test"),
                    opt("ANOVA"),
                    opt("Linear regression"),
                ),
                "The chi-square approximation fails for expected counts below ~5; Fisher's exact is appropriate.",
            ),
            q(
                "Expected cell counts in a contingency table are computed as:",
                (
                    opt("Row total times column total divided by n", correct=True),
                    opt("Row total plus column total"),
                    opt("n divided by the number of cells"),
                    opt("The observed count squared"),
                ),
                "Under independence E = (row total)(column total)/n.",
            ),
        ),
        "Linear & logistic regression": (
            q(
                "In multiple linear regression, a coefficient beta_j represents:",
                (
                    opt(
                        "The change in y per unit of x_j holding other predictors fixed",
                        correct=True,
                    ),
                    opt("The total variance of y"),
                    opt("The correlation of x_j with y ignoring others"),
                    opt("The p-value of the model"),
                ),
                "Coefficients are adjusted effects, controlling for the other predictors.",
            ),
            q(
                "Logistic regression models which quantity as a linear function of the predictors?",
                (
                    opt("The log-odds of the outcome", correct=True),
                    opt("The probability directly"),
                    opt("The raw count"),
                    opt("The variance"),
                ),
                "Logistic regression is linear on the log-odds (logit) scale.",
            ),
            q(
                "Exponentiating a logistic regression coefficient gives:",
                (
                    opt("An odds ratio", correct=True),
                    opt("An R-squared"),
                    opt("A hazard ratio"),
                    opt("A standard error"),
                ),
                "exp(beta_j) is the odds ratio for a one-unit change in the predictor.",
            ),
        ),
    },
    final=(
        q(
            "Which best describes the value of reporting a confidence interval?",
            (
                opt("It conveys both the estimate and its uncertainty", correct=True),
                opt("It proves the null hypothesis"),
                opt("It removes the need for a sample"),
                opt("It is the same as a p-value"),
            ),
            "A CI shows a plausible range plus reliability, more informative than a bare estimate.",
        ),
        q(
            "Increasing the sample size primarily improves:",
            (
                opt("Statistical power", correct=True),
                opt("The significance level alpha"),
                opt("The Type I error rate"),
                opt("The effect size"),
            ),
            "Larger n raises power (lowers beta), making real effects easier to detect.",
        ),
        q(
            "Welch's t-test is preferred over the pooled t-test when:",
            (
                opt("Group variances are unequal", correct=True),
                opt("The outcome is categorical"),
                opt("There are many groups"),
                opt("Data are perfectly paired"),
            ),
            "Welch's test does not assume equal variances and is a safer default.",
        ),
        q(
            "A significant chi-square test of independence indicates:",
            (
                opt("An association between the two categorical variables", correct=True),
                opt("A difference in two means"),
                opt("A causal effect"),
                opt("Equal variances"),
            ),
            "It signals dependence between the variables, not causation.",
        ),
        q(
            "R-squared in linear regression measures:",
            (
                opt("The fraction of outcome variance explained by the model", correct=True),
                opt("The probability of a Type I error"),
                opt("The slope of the line"),
                opt("The number of predictors"),
            ),
            "R-squared is the proportion of variance in y explained by the predictors.",
        ),
        q(
            "A small p-value alone tells you:",
            (
                opt(
                    "The result is surprising under the null, but not the effect size", correct=True
                ),
                opt("The effect is large and important"),
                opt("The probability the null is true"),
                opt("That the study is well designed"),
            ),
            "Significance is not the same as importance; always report effect size and CI.",
        ),
    ),
)
