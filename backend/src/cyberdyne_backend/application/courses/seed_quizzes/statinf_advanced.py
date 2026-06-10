"""Curated quiz questions for the Statistical Inference - Advanced course
(per-lesson checkpoints + a final comprehensive quiz). Keys are the EXACT
content-lesson titles; every question is answerable from the lesson body."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Maximum likelihood estimation": (
            q(
                "What does maximum likelihood estimation pick as its parameter?",
                (
                    opt("The parameter with the largest prior probability"),
                    opt("The parameter that makes the observed data most probable", correct=True),
                    opt("The parameter that minimises the variance of the data"),
                    opt(
                        "The parameter exactly halfway between the smallest and largest data points"
                    ),
                ),
                "Maximum likelihood picks the parameter that makes the observed data most probable.",
            ),
            q(
                "Why is the log-likelihood usually maximised instead of the raw likelihood?",
                (
                    opt("It turns products into sums", correct=True),
                    opt("It is the only function that has a maximum"),
                    opt("It removes the need for any data"),
                    opt("It converts the likelihood into a prior"),
                ),
                "Taking the log of the likelihood turns products into sums, which is easier to maximise.",
            ),
            q(
                "Per the lesson, minimising which loss is the same as maximising likelihood when training neural-network classifiers?",
                (
                    opt("Mean absolute error loss"),
                    opt("Hinge loss"),
                    opt("Cross-entropy loss", correct=True),
                    opt("Squared bias loss"),
                ),
                "The lesson states minimising cross-entropy loss is maximising likelihood, underlying neural-network classifier training.",
            ),
        ),
        "Bayesian inference": (
            q(
                "In Bayesian inference, the posterior is proportional to which product?",
                (
                    opt("The likelihood times the prior", correct=True),
                    opt("The prior divided by the likelihood"),
                    opt("The confidence interval times the variance"),
                    opt("The sample mean times the sample size"),
                ),
                "The posterior is proportional to the likelihood times the prior.",
            ),
            q(
                "What does Bayesian inference keep instead of a single estimate?",
                (
                    opt("A single point estimate refined each step"),
                    opt("A whole distribution of belief that is updated with data", correct=True),
                    opt("Only the maximum likelihood value"),
                    opt("A fixed prior that never changes"),
                ),
                "Bayesian inference keeps a whole distribution of belief and updates it with data.",
            ),
            q(
                "What is the Bayesian analogue of a confidence interval described in the lesson?",
                (
                    opt("A credible interval", correct=True),
                    opt("A prediction band"),
                    opt("A likelihood ratio"),
                    opt("A standard error"),
                ),
                "A credible interval is the Bayesian analogue of a confidence interval and the interpretation people actually want.",
            ),
        ),
        "Regression as inference": (
            q(
                "By what method does linear regression fit y = b0 + b1*x?",
                (
                    opt("Maximum entropy"),
                    opt("Least squares", correct=True),
                    opt("Gradient ascent on the prior"),
                    opt("Nearest-neighbour averaging"),
                ),
                "Linear regression fits the line by least squares.",
            ),
            q(
                "What does R squared report in a regression?",
                (
                    opt("The fraction of variance explained", correct=True),
                    opt("The probability the slope is zero"),
                    opt("The number of data points used"),
                    opt("The size of the prior belief"),
                ),
                "R squared reports the fraction of variance explained by the regression.",
            ),
            q(
                "According to the lesson, how should the residuals of a good regression fit look?",
                (
                    opt("Like a straight increasing line"),
                    opt("Like structureless noise", correct=True),
                    opt("Like a U-shaped curve"),
                    opt("Like the original data points exactly"),
                ),
                "The residuals should look like structureless noise.",
            ),
        ),
        "Bootstrap & the bias-variance trade-off": (
            q(
                "How does the bootstrap estimate a standard error when no formula is handy?",
                (
                    opt(
                        "It draws many samples with replacement and uses the spread of the recomputed statistic",
                        correct=True,
                    ),
                    opt("It assumes the data is Normal and uses 1.96 times the mean"),
                    opt("It splits the data once into train and test halves"),
                    opt("It multiplies the likelihood by the prior"),
                ),
                "The bootstrap resamples with replacement, recomputes the statistic each time, and uses their spread as the standard error.",
            ),
            q(
                "In the bias-variance trade-off, a too-simple model suffers from what?",
                (
                    opt("High variance from overfitting"),
                    opt("High bias from underfitting", correct=True),
                    opt("Zero total error"),
                    opt("An undefined likelihood"),
                ),
                "A too-simple model underfits, which the lesson calls high bias.",
            ),
            q(
                "Which technique does the lesson say estimates total error honestly to pick the sweet spot?",
                (
                    opt("Cross-validation", correct=True),
                    opt("Maximum likelihood"),
                    opt("Bayesian updating"),
                    opt("Least squares"),
                ),
                "Cross-validation trains on part and tests on the rest to estimate total error honestly.",
            ),
        ),
        "Lab: bootstrap confidence interval by simulation": (
            q(
                "In the lab, how are the bootstrap resamples drawn from the data?",
                (
                    opt("Without replacement"),
                    opt("With replacement", correct=True),
                    opt("In sorted order only"),
                    opt("Only the first half of the data"),
                ),
                "The lab comment states it resamples WITH REPLACEMENT B times, recomputing the mean each time.",
            ),
            q(
                "What multiplier does the lab use to build the roughly 95% bootstrap confidence interval around the mean?",
                (
                    opt("1.96", correct=True),
                    opt("2.58"),
                    opt("1.0"),
                    opt("3.29"),
                ),
                "The lab computes mean plus or minus 1.96 times the standard error for a 95% interval.",
            ),
            q(
                "Per the lab's closing notes, how does the interval shrink as you add more data points?",
                (
                    opt("Like 1 over sqrt(n)", correct=True),
                    opt("Like 1 over n squared"),
                    opt("It does not change with more data"),
                    opt("It grows linearly with n"),
                ),
                "The notes say adding more data points makes the interval shrink like 1/sqrt(n).",
            ),
        ),
    },
    final=(
        q(
            "Which method picks the parameter that makes the observed data most probable?",
            (
                opt("Maximum likelihood estimation", correct=True),
                opt("Cross-validation"),
                opt("The bootstrap"),
                opt("Least squares residual analysis"),
            ),
            "Maximum likelihood estimation chooses the parameter making the observed data most probable.",
        ),
        q(
            "In Bayes' rule as presented, the posterior is proportional to which combination?",
            (
                opt("Likelihood times prior", correct=True),
                opt("Prior minus likelihood"),
                opt("Variance times bias"),
                opt("R squared times the sample size"),
            ),
            "The posterior is proportional to the likelihood times the prior.",
        ),
        q(
            "What does the bias-variance trade-off say about total error versus model complexity?",
            (
                opt("It falls monotonically as complexity rises"),
                opt("It is U-shaped with a sweet spot", correct=True),
                opt("It is constant regardless of complexity"),
                opt("It equals the prior probability"),
            ),
            "Total error is the sum of bias and variance, forming a U-curve with a sweet spot.",
        ),
        q(
            "How does the bootstrap produce a standard error when a formula is hard to find?",
            (
                opt(
                    "By resampling the data with replacement and measuring the spread of the statistic",
                    correct=True,
                ),
                opt("By taking the log of the likelihood"),
                opt("By computing R squared on the residuals"),
                opt("By choosing the prior with the largest density"),
            ),
            "The bootstrap resamples with replacement and uses the spread of the recomputed statistic as the standard error.",
        ),
        q(
            "In regression as inference, what accompanies each fitted coefficient beta?",
            (
                opt("A standard error, a confidence interval, and a p-value", correct=True),
                opt("A prior, a posterior, and a credible interval"),
                opt("A bias term, a variance term, and a U-curve"),
                opt("A seed, a multiplier, and a modulus"),
            ),
            "Each coefficient comes with a standard error, a confidence interval, and a p-value.",
        ),
    ),
)
