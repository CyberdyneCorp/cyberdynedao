"""Quiz questions for the Scientific Data Visualization - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Visualising distributions": (
            q(
                "What does a box plot fail to reveal that a violin plot shows?",
                (
                    opt("Multimodality (multiple peaks) in the distribution", correct=True),
                    opt("The median"),
                    opt("The interquartile range"),
                    opt("The maximum value"),
                ),
                "A box only shows quartiles; a violin's density can expose two or more modes.",
            ),
            q(
                "For a small sample, the recommended distribution display is to:",
                (
                    opt("Overlay the raw points on a box or violin", correct=True),
                    opt("Show a bar of the mean only"),
                    opt("Use a pie chart"),
                    opt("Hide the data and show only SEM"),
                ),
                "With small n, plotting every point alongside a summary is the honest choice.",
            ),
            q(
                "An advantage of the empirical CDF over a histogram is that it:",
                (
                    opt("Requires no binning or bandwidth choice", correct=True),
                    opt("Always looks Normal"),
                    opt("Hides outliers"),
                    opt("Cannot compare groups"),
                ),
                "The ECDF is parameter-free and makes location and spread shifts directly comparable.",
            ),
        ),
        "Histograms & kernel density": (
            q(
                "Which bin-width rule is robust to outliers?",
                (
                    opt("Freedman-Diaconis (uses the IQR)", correct=True),
                    opt("A fixed 10 bins always"),
                    opt("One bin per data point"),
                    opt("Sturges, because it ignores spread"),
                ),
                "Freedman-Diaconis h = 2*IQR*n^(-1/3) uses the robust IQR.",
            ),
            q(
                "In kernel density estimation, the bandwidth h controls:",
                (
                    opt("The bias-variance tradeoff (smoothness)", correct=True),
                    opt("The colour of the curve"),
                    opt("The number of data points"),
                    opt("The axis labels"),
                ),
                "Small h is noisy (high variance); large h oversmooths (high bias).",
            ),
            q(
                "A KDE of concentration data should not:",
                (
                    opt("Extend below zero past a physical lower bound", correct=True),
                    opt("Be smooth"),
                    opt("Use a Gaussian kernel"),
                    opt("Have a single mode"),
                ),
                "Densities must respect hard bounds; reflect at the boundary or use a log scale.",
            ),
        ),
        "Scatterplots & uncertainty": (
            q(
                "For a scatterplot of millions of points, the best overplotting fix is:",
                (
                    opt("2-D binning such as hexbin or density contours", correct=True),
                    opt("Drawing larger opaque markers"),
                    opt("Removing the axes"),
                    opt("Switching to a pie chart"),
                ),
                "At very large n, binning summarises density where raw points just overlap.",
            ),
            q(
                "Why must error bars be labelled as SD, SEM or CI?",
                (
                    opt(
                        "They differ by roughly the square root of n and are easily confused",
                        correct=True,
                    ),
                    opt("They are all identical"),
                    opt("Labelling is purely decorative"),
                    opt("CIs are always smaller than SDs"),
                ),
                "SEM = SD/sqrt(n); unlabelled bars mislead about precision.",
            ),
            q(
                "Simpson's paradox in a scatterplot is exposed by:",
                (
                    opt("Faceting or colour-coding by the lurking subgroup variable", correct=True),
                    opt("Removing all subgroups"),
                    opt("Using a log axis"),
                    opt("Extrapolating the smoother"),
                ),
                "An overall trend can reverse within strata; conditioning on the subgroup reveals it.",
            ),
        ),
        "Small multiples & faceting": (
            q(
                "The defining feature of small multiples is that panels:",
                (
                    opt(
                        "Share axes and encoding, differing by one conditioning variable",
                        correct=True,
                    ),
                    opt("Each use different chart types"),
                    opt("Each auto-scale independently"),
                    opt("Use a different colour palette per panel"),
                ),
                "Shared scales are what make cross-panel comparison effortless.",
            ),
            q(
                "The non-negotiable rule for faceted panels is to:",
                (
                    opt("Fix the scales across panels", correct=True),
                    opt("Sort panels alphabetically"),
                    opt("Add a 3-D effect"),
                    opt("Use free scales by default"),
                ),
                "Auto-scaling each panel makes a small bump look like a huge peak.",
            ),
            q(
                "facet_grid arranges panels by:",
                (
                    opt("The cross of two variables (rows by columns)", correct=True),
                    opt("Random placement"),
                    opt("File size"),
                    opt("Colour only"),
                ),
                "facet_grid lays out rows x columns; facet_wrap flows panels in a grid.",
            ),
        ),
        "Log scales & transforms": (
            q(
                "On a semi-log plot, exponential growth y = a*e^(kt) appears as:",
                (
                    opt("A straight line whose slope is the rate constant k", correct=True),
                    opt("A parabola"),
                    opt("A flat line"),
                    opt("A circle"),
                ),
                "Taking logs gives log y = log a + k t, a line with slope k.",
            ),
            q(
                "Which transform handles data containing zeros or negatives?",
                (
                    opt("Symlog (linear near zero, logarithmic beyond)", correct=True),
                    opt("Plain log10"),
                    opt("Reciprocal"),
                    opt("None can"),
                ),
                "Symlog or log1p cope with zeros and negatives where plain log fails.",
            ),
            q(
                "A log axis must never:",
                (
                    opt("Include a zero baseline (zero is at minus infinity)", correct=True),
                    opt("Show tick labels"),
                    opt("Be used for fold-changes"),
                    opt("Span several orders of magnitude"),
                ),
                "Zero cannot be placed on a log scale; baselines belong on linear axes.",
            ),
        ),
    },
    final=(
        q(
            "Comparing groups by their means alone is dangerous because it hides:",
            (
                opt("The shape of the distribution (skew, modes, outliers)", correct=True),
                opt("The colour palette"),
                opt("The axis units"),
                opt("The chart title"),
            ),
            "Means cannot distinguish unimodal from bimodal or symmetric from skewed groups.",
        ),
        q(
            "Silverman's rule of thumb for KDE bandwidth tends to:",
            (
                opt("Oversmooth multimodal distributions", correct=True),
                opt("Always undersmooth"),
                opt("Ignore the sample size"),
                opt("Produce zero bandwidth"),
            ),
            "It assumes near-Normal data and can wash out real multiple peaks.",
        ),
        q(
            "Alpha transparency in a scatterplot helps by:",
            (
                opt("Letting density show through overlapping points", correct=True),
                opt("Changing the axis scale"),
                opt("Removing outliers"),
                opt("Adding a legend"),
            ),
            "Semi-transparent points reveal where many observations pile up.",
        ),
        q(
            "Why order facet panels by magnitude or biology rather than alphabetically?",
            (
                opt("Meaningful ordering aids comparison and reveals structure", correct=True),
                opt("It is required by the file format"),
                opt("Alphabetical order is impossible"),
                opt("It reduces file size"),
            ),
            "Order is itself an encoding; alphabetical is usually arbitrary.",
        ),
        q(
            "Logging right-skewed biological data before testing often:",
            (
                opt("Pulls the distribution toward symmetry", correct=True),
                opt("Makes it more skewed"),
                opt("Removes all variance"),
                opt("Creates negative counts"),
            ),
            "Log transforms compress the long right tail, approaching symmetry.",
        ),
        q(
            "A bar plot of mean +/- SEM for skewed assay data is misleading because:",
            (
                opt("The zero-based bar implies a symmetric spread the data lack", correct=True),
                opt("Bars cannot show means"),
                opt("SEM equals SD"),
                opt("It uses too many colours"),
            ),
            "Such plots hide skew and the raw distribution; show the points instead.",
        ),
    ),
)
