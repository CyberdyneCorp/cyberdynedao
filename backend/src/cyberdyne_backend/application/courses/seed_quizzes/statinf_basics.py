"""Curated quiz questions for the Statistical Inference - Basics course.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Populations, samples & statistics": (
            q(
                "What is a parameter in this lesson's terminology?",
                (
                    opt("A value computed from the sample, such as the sample mean"),
                    opt(
                        "A quantity that describes the population, such as the true mean, usually unknown",
                        correct=True,
                    ),
                    opt("The size of the sample we choose to measure"),
                    opt("A random error introduced by biased sampling"),
                ),
                "A parameter describes the population (the true mean or true proportion) and is usually unknown.",
            ),
            q(
                "Why is a statistic such as the sample mean itself random?",
                (
                    opt("Because the population mean changes over time"),
                    opt("Because measurement instruments are always inaccurate"),
                    opt(
                        "Because the sample it is computed from is random, so it lands near the true value but rarely exactly on it",
                        correct=True,
                    ),
                    opt("Because parameters are defined to be random variables"),
                ),
                "A sample is random, so any statistic computed from it is random too and only lands near the parameter.",
            ),
            q(
                "What property must good sampling have to keep downstream inference valid?",
                (
                    opt("It must be as large as the population itself"),
                    opt("It must be measured with no rounding"),
                    opt(
                        "It must be representative, ideally random, since biased samples break everything downstream",
                        correct=True,
                    ),
                    opt("It must be collected from the most convenient subjects"),
                ),
                "Sampling must be representative (ideally random); biased samples break inference no matter how much data you collect.",
            ),
        ),
        "Describing data: centre & spread": (
            q(
                "Which measure of centre is described as robust to outliers?",
                (
                    opt("The mean"),
                    opt("The median", correct=True),
                    opt("The variance"),
                    opt("The standard error"),
                ),
                "The median is the middle value and is robust to outliers, unlike the mean which is sensitive to them.",
            ),
            q(
                "For a Normal distribution, about what fraction of the data lies within one standard deviation of the mean?",
                (
                    opt("About 50%"),
                    opt("About 68%", correct=True),
                    opt("About 95%"),
                    opt("About 99%"),
                ),
                "For a Normal, about 68% of the data lies within one standard deviation and about 95% within two.",
            ),
            q(
                "Which formula does the lesson give for the sample variance?",
                (
                    opt("The sum of the values divided by n"),
                    opt("The most common value in the data set"),
                    opt(
                        "The sum of squared deviations from the mean divided by n minus 1",
                        correct=True,
                    ),
                    opt("The middle-50% range between quartiles"),
                ),
                "Variance is the sum of squared deviations from the mean divided by n minus 1.",
            ),
        ),
        "Sampling distributions & standard error": (
            q(
                "What is the sampling distribution?",
                (
                    opt("The distribution of a single sample's raw values"),
                    opt(
                        "The distribution of the sample mean obtained from taking many samples of size n",
                        correct=True,
                    ),
                    opt("The distribution of the population parameter"),
                    opt("The distribution of the standard error across populations"),
                ),
                "Taking many samples of size n and computing the mean each time gives the sampling distribution of the mean.",
            ),
            q(
                "What is the formula for the standard error of the sample mean?",
                (
                    opt("sigma times the square root of n"),
                    opt("sigma divided by the square root of n", correct=True),
                    opt("sigma divided by n"),
                    opt("the square root of sigma divided by n"),
                ),
                "The standard error is sigma divided by the square root of n.",
            ),
            q(
                "To halve the standard error, how much more data do you need?",
                (
                    opt("Twice as much data"),
                    opt("Four times as much data", correct=True),
                    opt("Half as much data"),
                    opt("Ten times as much data"),
                ),
                "Because the error shrinks only as the square root of n, halving it requires four times the data.",
            ),
        ),
        "Confidence intervals": (
            q(
                "What is the formula given for a 95% confidence interval for the mean?",
                (
                    opt("the sample mean plus or minus sigma divided by n"),
                    opt(
                        "the sample mean plus or minus 1.96 times sigma divided by the square root of n",
                        correct=True,
                    ),
                    opt("the sample mean plus or minus the sample mean"),
                    opt("the sample mean plus or minus 2.58 times sigma"),
                ),
                "A 95% confidence interval is the sample mean plus or minus 1.96 times sigma over the square root of n.",
            ),
            q(
                "What is the correct interpretation of a 95% confidence interval?",
                (
                    opt("There is a 95% probability the sample mean equals the true mean"),
                    opt(
                        "If the experiment were repeated many times, about 95% of the intervals built would cover the true mean",
                        correct=True,
                    ),
                    opt("95% of the data points fall inside the interval"),
                    opt("The interval is wrong 95% of the time"),
                ),
                "If you repeated the experiment many times, about 95% of the intervals constructed would cover the true mean.",
            ),
            q(
                "What happens to the width of a confidence interval as the sample size increases?",
                (
                    opt("It stays the same regardless of n"),
                    opt("It widens around the mean"),
                    opt("It shrinks around the mean", correct=True),
                    opt("It becomes centered on a different value"),
                ),
                "More data tightens the interval, so it shrinks around the mean as the sample size increases.",
            ),
        ),
    },
    final=(
        q(
            "What is the difference between a parameter and a statistic?",
            (
                opt("A parameter is random while a statistic is fixed"),
                opt(
                    "A parameter describes the population and is usually unknown, while a statistic is computed from the sample to estimate it",
                    correct=True,
                ),
                opt("They are two names for the same quantity"),
                opt("A parameter comes from the sample and a statistic from the population"),
            ),
            "A parameter describes the population (usually unknown); a statistic is computed from the sample to estimate it.",
        ),
        q(
            "Which pairing of centre and spread measures is correct?",
            (
                opt("The mean is robust to outliers; the median is sensitive to them"),
                opt("The mode is a spread measure; the variance is a centre measure"),
                opt(
                    "The median is robust to outliers; the variance and standard deviation measure spread",
                    correct=True,
                ),
                opt("The standard error measures centre; the mean measures spread"),
            ),
            "The median is robust to outliers, and variance and standard deviation are the spread measures.",
        ),
        q(
            "Why does a bigger sample give a tighter estimate of the mean?",
            (
                opt("Because the population variance falls as n grows"),
                opt(
                    "Because the standard error is sigma over the square root of n, so it shrinks as n grows",
                    correct=True,
                ),
                opt("Because larger samples remove all bias automatically"),
                opt("Because the true mean moves toward the sample mean"),
            ),
            "The standard error is sigma over the square root of n, so it decreases as the sample size grows.",
        ),
        q(
            "Which constant multiplies the standard error in a 95% confidence interval for a Normal?",
            (
                opt("1.0"),
                opt("1.96", correct=True),
                opt("2.58"),
                opt("3.0"),
            ),
            "The 1.96 is the Normal's 95% cutoff used to build the confidence interval.",
        ),
        q(
            "Which statement about confidence intervals and precision is correct?",
            (
                opt("A wider interval gives both more confidence and more precision"),
                opt(
                    "A wider interval gives more confidence but less precision; more data tightens it",
                    correct=True,
                ),
                opt("Interval width is unrelated to the amount of data collected"),
                opt("A narrower interval always means lower confidence in the estimate"),
            ),
            "A wider interval means more confidence but less precision, and collecting more data tightens the interval.",
        ),
    ),
)
