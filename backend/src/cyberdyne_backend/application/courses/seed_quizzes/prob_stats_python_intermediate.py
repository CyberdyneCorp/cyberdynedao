"""Curated quiz questions for Probability & Statistics with Python - Intermediate.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The Central Limit Theorem by simulation": (
            q(
                "What does the Central Limit Theorem say about the mean of many independent samples?",
                (
                    opt(
                        "It is approximately Normal regardless of the shape of the original distribution",
                        correct=True,
                    ),
                    opt("It always equals the population median"),
                    opt("It follows the same shape as the original distribution exactly"),
                    opt("It is uniform between the min and max of the data"),
                ),
                "The CLT says the distribution of the sample mean is approximately Normal even "
                "when the source distribution is not.",
            ),
            q(
                "In the simulation, what is the standard error of the sample mean equal to?",
                (
                    opt("The population standard deviation times n"),
                    opt(
                        "The population standard deviation divided by the square root of n",
                        correct=True,
                    ),
                    opt("The population variance divided by n squared"),
                    opt("Always exactly 1.0"),
                ),
                "The standard error is sigma divided by the square root of n, so it shrinks as "
                "n grows.",
            ),
            q(
                "How do you compute one mean per row from a `(reps, n)` array of draws?",
                (
                    opt("`draws.mean(axis=1)`", correct=True),
                    opt("`draws.mean(axis=0)`"),
                    opt("`draws.sum()`"),
                    opt("`draws.std(ddof=1)`"),
                ),
                "`axis=1` reduces along the columns, giving one mean per row (one per repetition).",
            ),
        ),
        "Confidence intervals with numpy & scipy": (
            q(
                "What is the standard error of the mean in terms of the sample standard deviation `s`?",
                (
                    opt("`s` times the square root of n"),
                    opt("`s` divided by the square root of n", correct=True),
                    opt("`s` divided by n squared"),
                    opt("`s` plus n"),
                ),
                "The standard error of the mean is `s / sqrt(n)`.",
            ),
            q(
                "Why use the t-distribution rather than the Normal for small-sample confidence intervals?",
                (
                    opt(
                        "It has heavier tails, accounting for estimating sigma from the data",
                        correct=True,
                    ),
                    opt("It is always narrower than the Normal"),
                    opt("It does not require knowing the sample size"),
                    opt("It only applies to proportions"),
                ),
                "When sigma is estimated from a small sample, the t-distribution's heavier "
                "tails give the correct, wider interval.",
            ),
            q(
                "Which scipy call builds a 95% confidence interval for the mean in one line?",
                (
                    opt("`stats.t.interval(0.95, df=n-1, loc=mean, scale=se)`", correct=True),
                    opt("`stats.norm.pdf(mean)`"),
                    opt("`stats.ttest_ind(a, b)`"),
                    opt("`np.percentile(x, 95)`"),
                ),
                "`stats.t.interval` returns the lower and upper bounds for the given "
                "confidence level, df, location and scale.",
            ),
        ),
        "Hypothesis testing with scipy.stats": (
            q(
                "What is a p-value?",
                (
                    opt(
                        "The probability of a result at least this extreme if the null hypothesis were true",
                        correct=True,
                    ),
                    opt("The probability that the null hypothesis is true"),
                    opt("The probability that the alternative hypothesis is true"),
                    opt("The size of the observed effect"),
                ),
                "A p-value is the probability of observing data at least this extreme assuming "
                "the null hypothesis holds.",
            ),
            q(
                "Which scipy function compares the means of two independent groups without assuming equal variances?",
                (
                    opt("`stats.ttest_ind(a, b, equal_var=False)`", correct=True),
                    opt("`stats.ttest_1samp(a, 0)`"),
                    opt("`stats.chi2_contingency(a)`"),
                    opt("`stats.linregress(a, b)`"),
                ),
                "`ttest_ind` with `equal_var=False` is Welch's t-test, the safer default for "
                "two-sample comparisons.",
            ),
            q(
                "Which test checks whether two categorical variables in a contingency table are independent?",
                (
                    opt("`stats.ttest_rel`"),
                    opt("`stats.chi2_contingency`", correct=True),
                    opt("`stats.norm.cdf`"),
                    opt("`np.corrcoef`"),
                ),
                "`chi2_contingency` tests independence of the row and column categories of a "
                "contingency table.",
            ),
        ),
        "Correlation & covariance": (
            q(
                "What is the range of the Pearson correlation coefficient r?",
                (
                    opt("From 0 to 1"),
                    opt("From -1 to 1", correct=True),
                    opt("From -infinity to infinity"),
                    opt("From 0 to 100"),
                ),
                "The correlation coefficient is standardised to lie between -1 and 1.",
            ),
            q(
                "Which NumPy function returns the Pearson correlation matrix of two arrays?",
                (
                    opt("`np.corrcoef(x, y)`", correct=True),
                    opt("`np.cov(x, y)`"),
                    opt("`np.polyfit(x, y, 1)`"),
                    opt("`np.histogram(x)`"),
                ),
                "`np.corrcoef` returns the correlation matrix; `np.cov` returns the "
                "(unstandardised) covariance matrix.",
            ),
            q(
                "Why can a strong relationship still show a correlation r near zero?",
                (
                    opt(
                        "Because r only measures linear association, missing curved relationships",
                        correct=True,
                    ),
                    opt("Because correlation always equals zero for related variables"),
                    opt("Because NumPy rounds small correlations to zero"),
                    opt("Because covariance and correlation are unrelated"),
                ),
                "Pearson r captures only linear association, so a strong nonlinear (e.g. "
                "parabolic) relationship can give r near zero.",
            ),
        ),
        "Simple linear regression": (
            q(
                "What does ordinary least-squares regression minimise?",
                (
                    opt(
                        "The sum of squared vertical residuals between points and the line",
                        correct=True,
                    ),
                    opt("The maximum horizontal distance to the line"),
                    opt("The number of points above the line"),
                    opt("The correlation between x and y"),
                ),
                "Least squares fits the line that minimises the sum of squared vertical residuals.",
            ),
            q(
                "What does `R**2` (the square of `rvalue`) from `stats.linregress` tell you?",
                (
                    opt("The fraction of variance in y explained by the line", correct=True),
                    opt("The slope of the regression line"),
                    opt("The number of data points"),
                    opt("The p-value for the intercept"),
                ),
                "R-squared is the fraction of the variance in y that the fitted line explains.",
            ),
            q(
                "Which call gives the slope and intercept of a degree-1 fit with NumPy?",
                (
                    opt("`np.polyfit(x, y, deg=1)`", correct=True),
                    opt("`np.corrcoef(x, y)`"),
                    opt("`np.histogram(x, y)`"),
                    opt("`np.percentile(x, 1)`"),
                ),
                "`np.polyfit(x, y, deg=1)` returns the coefficients [slope, intercept] of the "
                "best-fit line.",
            ),
        ),
        "Real-world data wrangling with pandas": (
            q(
                "Which call counts the missing values in each column of a DataFrame?",
                (
                    opt("`df.isna().sum()`", correct=True),
                    opt("`df.dropna()`"),
                    opt("`df.describe()`"),
                    opt("`df.corr()`"),
                ),
                "`df.isna()` marks missing cells as True and `.sum()` counts them per column.",
            ),
            q(
                "What does `pivot_table(values='revenue', index='city', columns='quarter', aggfunc='sum')` produce?",
                (
                    opt(
                        "A grid of summed revenue with cities as rows and quarters as columns",
                        correct=True,
                    ),
                    opt("A single total revenue number"),
                    opt("A correlation matrix of revenue"),
                    opt("The first rows of the table"),
                ),
                "A pivot table reshapes long data into a grid indexed by city with quarter "
                "columns, summing revenue in each cell.",
            ),
            q(
                "Which method adds columns from another table by matching on a key, keeping all left rows?",
                (
                    opt("`df.merge(other, on='city', how='left')`", correct=True),
                    opt("`df.groupby('city')`"),
                    opt("`df.fillna(0)`"),
                    opt("`df.sort_values('city')`"),
                ),
                "A left merge on the key column keeps every row of the left table and attaches "
                "matching columns from the right.",
            ),
        ),
    },
    final=(
        q(
            "The Central Limit Theorem explains why which distribution appears so often in inference?",
            (
                opt("The uniform distribution"),
                opt("The Normal distribution", correct=True),
                opt("The Poisson distribution"),
                opt("The exponential distribution"),
            ),
            "The CLT makes the sample mean approximately Normal, which is why Normal-based "
            "methods are so widely used.",
        ),
        q(
            "A 95% confidence interval for the mean uses which standard-error expression?",
            (
                opt("`s * sqrt(n)`"),
                opt("`s / sqrt(n)`", correct=True),
                opt("`s / n**2`"),
                opt("`s + n`"),
            ),
            "The CI is the mean plus or minus a critical value times the standard error "
            "`s / sqrt(n)`.",
        ),
        q(
            "Which scipy function performs a two-sample comparison of means (Welch's t-test)?",
            (
                opt("`stats.ttest_ind(a, b, equal_var=False)`", correct=True),
                opt("`stats.chi2_contingency(a)`"),
                opt("`stats.linregress(a, b)`"),
                opt("`np.corrcoef(a, b)`"),
            ),
            "`ttest_ind` with `equal_var=False` compares two independent group means without "
            "assuming equal variances.",
        ),
        q(
            "A correlation coefficient of r near -1 indicates what?",
            (
                opt("A strong positive linear relationship"),
                opt("A strong negative linear relationship", correct=True),
                opt("No relationship at all"),
                opt("A perfectly curved relationship"),
            ),
            "Values of r near -1 indicate a strong negative linear association.",
        ),
        q(
            "In `stats.linregress`, what does `rvalue**2` represent?",
            (
                opt("The slope of the line"),
                opt("The fraction of variance in y explained by the model", correct=True),
                opt("The residual standard error"),
                opt("The number of observations"),
            ),
            "R-squared, the square of the r value, is the fraction of variance the regression "
            "line explains.",
        ),
        q(
            "Which pandas operation reshapes long data into a grid of one aggregated statistic?",
            (
                opt("`df.isna()`"),
                opt("`df.pivot_table(...)`", correct=True),
                opt("`df.dropna()`"),
                opt("`df.head()`"),
            ),
            "`pivot_table` reshapes long rows into a grid indexed by one variable with another "
            "as columns, aggregating the values.",
        ),
    ),
)
