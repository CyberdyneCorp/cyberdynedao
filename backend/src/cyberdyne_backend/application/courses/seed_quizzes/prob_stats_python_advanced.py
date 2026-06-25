"""Curated quiz questions for Probability & Statistics with Python - Advanced.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Bayesian inference basics": (
            q(
                "In Bayes' rule, the posterior is proportional to which combination?",
                (
                    opt("The likelihood times the prior", correct=True),
                    opt("The prior divided by the likelihood"),
                    opt("The likelihood minus the prior"),
                    opt("The prior alone, ignoring the data"),
                ),
                "Posterior is proportional to likelihood times prior; the data reshapes the "
                "prior into the posterior.",
            ),
            q(
                "After observing `h` successes and `t` failures, a `Beta(alpha, beta)` prior becomes which posterior?",
                (
                    opt("`Beta(alpha + h, beta + t)`", correct=True),
                    opt("`Beta(alpha - h, beta - t)`"),
                    opt("`Beta(h, t)` regardless of the prior"),
                    opt("`Normal(h, t)`"),
                ),
                "The Beta is conjugate to the Binomial, so the posterior is "
                "`Beta(alpha + successes, beta + failures)`.",
            ),
            q(
                "What does a 95% credible interval mean in Bayesian terms?",
                (
                    opt(
                        "There is a 95% probability the parameter lies in the interval given the data",
                        correct=True,
                    ),
                    opt("95% of repeated experiments would cover the parameter"),
                    opt("The parameter is wrong 95% of the time"),
                    opt("95% of the data falls inside the interval"),
                ),
                "A credible interval is a direct probability statement about the parameter "
                "given the observed data.",
            ),
        ),
        "Bootstrap & resampling": (
            q(
                "How does the bootstrap estimate the uncertainty of a statistic?",
                (
                    opt(
                        "By resampling the data with replacement and recomputing the statistic",
                        correct=True,
                    ),
                    opt("By assuming the data is exactly Normal"),
                    opt("By collecting a brand-new dataset each time"),
                    opt("By removing all outliers first"),
                ),
                "The bootstrap draws many resamples with replacement and uses the spread of "
                "the recomputed statistic.",
            ),
            q(
                "How is a 95% percentile bootstrap confidence interval obtained?",
                (
                    opt(
                        "From the 2.5th and 97.5th percentiles of the bootstrap statistics",
                        correct=True,
                    ),
                    opt("From the mean plus or minus the original sample size"),
                    opt("From the single largest bootstrap value"),
                    opt("From a chi-square table"),
                ),
                "The percentile interval reads off the 2.5% and 97.5% quantiles of the "
                "bootstrap distribution.",
            ),
            q(
                "Why is the bootstrap especially useful for a statistic like the median?",
                (
                    opt(
                        "Because no simple closed-form standard-error formula exists for it",
                        correct=True,
                    ),
                    opt("Because the median is always Normally distributed"),
                    opt("Because medians cannot be computed directly"),
                    opt("Because it requires fewer than 10 data points"),
                ),
                "The bootstrap needs no formula, so it gives a standard error and CI even for "
                "statistics like the median that lack one.",
            ),
        ),
        "Monte Carlo methods": (
            q(
                "How does the dartboard Monte Carlo method estimate pi?",
                (
                    opt(
                        "By multiplying the fraction of random points inside the quarter circle by 4",
                        correct=True,
                    ),
                    opt("By measuring the circumference of a drawn circle"),
                    opt("By summing the coordinates of all points"),
                    opt("By integrating the data analytically"),
                ),
                "The quarter circle has area pi/4, so 4 times the fraction of points inside "
                "estimates pi.",
            ),
            q(
                "How does Monte Carlo estimation error scale with the number of simulations N?",
                (
                    opt("It shrinks like 1 over the square root of N", correct=True),
                    opt("It shrinks linearly, like 1 over N"),
                    opt("It grows with N"),
                    opt("It is independent of N"),
                ),
                "Like every sample-based estimate, Monte Carlo error falls as 1/sqrt(N).",
            ),
            q(
                "How can you estimate the integral of `exp(-x**2)` over [0, 1] by Monte Carlo?",
                (
                    opt("Average `exp(-u**2)` over many uniform draws `u` in [0, 1]", correct=True),
                    opt("Take the maximum of `exp(-u**2)` over the draws"),
                    opt("Count how many draws are negative"),
                    opt("Multiply the first draw by 1000"),
                ),
                "On [0, 1] the integral equals the expected value of the integrand, estimated "
                "by the sample average of `exp(-u**2)`.",
            ),
        ),
        "Multivariate statistics & PCA": (
            q(
                "What is stored on the diagonal of a covariance matrix?",
                (
                    opt("The variances of each variable", correct=True),
                    opt("The means of each variable"),
                    opt("The correlations, always equal to 1"),
                    opt("The number of observations"),
                ),
                "The diagonal holds each variable's variance; off-diagonal entries are the "
                "pairwise covariances.",
            ),
            q(
                "In PCA, what do the eigenvectors of the covariance matrix represent?",
                (
                    opt("The directions (principal axes) of greatest variance", correct=True),
                    opt("The mean of each column"),
                    opt("The missing values in the data"),
                    opt("The number of components to keep"),
                ),
                "Eigenvectors of the covariance matrix are the principal axes; eigenvalues are "
                "the variance along each.",
            ),
            q(
                "Why must the data be centred (zero-mean columns) before PCA?",
                (
                    opt(
                        "So the covariance matrix captures variation about the mean correctly",
                        correct=True,
                    ),
                    opt("So all values become positive"),
                    opt("So the data fits in memory"),
                    opt("Because eigenvalues must sum to zero"),
                ),
                "PCA decomposes variation about the mean, so columns must be centred first for "
                "the covariance to be meaningful.",
            ),
        ),
        "Maximum likelihood with scipy.optimize": (
            q(
                "What does maximum likelihood estimation choose?",
                (
                    opt("The parameters that make the observed data most probable", correct=True),
                    opt("The parameters with the smallest absolute value"),
                    opt("The parameters that minimise the data variance"),
                    opt("A random parameter from the prior"),
                ),
                "MLE picks the parameters that maximise the likelihood of the observed data.",
            ),
            q(
                "Why do we minimise the negative log-likelihood instead of maximising the likelihood directly?",
                (
                    opt(
                        "Logs turn products into sums (numerically stable) and optimisers minimise",
                        correct=True,
                    ),
                    opt("Because the likelihood is always negative"),
                    opt("Because scipy cannot compute products"),
                    opt("Because the log changes the location of the maximum"),
                ),
                "The log turns the product of densities into a numerically stable sum, and "
                "minimisers like `scipy.optimize.minimize` expect a function to minimise; "
                "negating turns the max into a min.",
            ),
            q(
                "For a Normal model, the MLE of the mean should land on which value?",
                (
                    opt("The sample mean", correct=True),
                    opt("Zero"),
                    opt("The sample maximum"),
                    opt("The median of the priors"),
                ),
                "The MLE of a Normal's mean is exactly the sample mean, a useful sanity check "
                "on the optimiser.",
            ),
        ),
        "End-to-end analysis: load, explore, test, model, conclude": (
            q(
                "In the end-to-end workflow, which step comes immediately after loading and exploring the data?",
                (
                    opt(
                        "Testing whether the group difference is real with `scipy.stats`",
                        correct=True,
                    ),
                    opt("Deleting the dataset"),
                    opt("Publishing without any analysis"),
                    opt("Reloading the same file again"),
                ),
                "After load and explore, you test the hypothesis (e.g. a t-test) before "
                "modelling the trend.",
            ),
            q(
                "Which function tests whether layout B's mean sales differ from layout A's?",
                (
                    opt("`stats.ttest_ind(b, a, equal_var=False)`", correct=True),
                    opt("`np.histogram(b, a)`"),
                    opt("`df.head()`"),
                    opt("`stats.beta(b, a)`"),
                ),
                "A two-sample (Welch) t-test compares the two groups' means.",
            ),
            q(
                "How should the final conclusion report the effect?",
                (
                    opt(
                        "Together with its confidence interval and p-value, not as a bare 'significant'",
                        correct=True,
                    ),
                    opt("As a single p-value with no effect size"),
                    opt("As the raw data dump only"),
                    opt("By stating the null hypothesis is proven true"),
                ),
                "A good conclusion reports the effect size, its confidence interval and the "
                "p-value together.",
            ),
        ),
    },
    final=(
        q(
            "For a Beta prior and Binomial data, the conjugate posterior after `h` successes and `t` failures is:",
            (
                opt("`Beta(alpha + h, beta + t)`", correct=True),
                opt("`Normal(h, t)`"),
                opt("`Beta(h - alpha, t - beta)`"),
                opt("`Poisson(h + t)`"),
            ),
            "Conjugacy gives `Beta(alpha + h, beta + t)` with no integration required.",
        ),
        q(
            "What is the core idea of the bootstrap?",
            (
                opt(
                    "Resample the data with replacement and recompute the statistic many times",
                    correct=True,
                ),
                opt("Assume the data is exactly Normal and use a z-table"),
                opt("Collect a completely new dataset for each estimate"),
                opt("Fit a straight line through the data"),
            ),
            "The bootstrap uses resampling with replacement to estimate the sampling "
            "distribution of any statistic.",
        ),
        q(
            "Monte Carlo estimation error decreases at what rate as N grows?",
            (
                opt("Like 1 over the square root of N", correct=True),
                opt("Like 1 over N squared"),
                opt("It does not decrease"),
                opt("It increases linearly"),
            ),
            "Monte Carlo error shrinks as 1/sqrt(N), so 4x the simulations halves the error.",
        ),
        q(
            "In PCA, the eigenvalues of the covariance matrix tell you what?",
            (
                opt("The amount of variance captured by each principal component", correct=True),
                opt("The mean of each variable"),
                opt("The number of rows in the data"),
                opt("The correlation between components, always 1"),
            ),
            "Each eigenvalue is the variance along its principal component, used to compute "
            "the variance explained.",
        ),
        q(
            "Maximum likelihood estimation with `scipy.optimize.minimize` typically minimises what?",
            (
                opt("The negative log-likelihood", correct=True),
                opt("The positive likelihood"),
                opt("The data variance"),
                opt("The number of parameters"),
            ),
            "We minimise the negative log-likelihood, which is equivalent to maximising the "
            "likelihood.",
        ),
        q(
            "A complete analysis should conclude by reporting which combination?",
            (
                opt("Effect size, its confidence interval, and the p-value together", correct=True),
                opt("Only whether the result was significant"),
                opt("Only the raw dataset"),
                opt("Only the regression slope with no uncertainty"),
            ),
            "Reporting the effect size with its confidence interval and p-value gives an "
            "honest, complete conclusion.",
        ),
    ),
)
