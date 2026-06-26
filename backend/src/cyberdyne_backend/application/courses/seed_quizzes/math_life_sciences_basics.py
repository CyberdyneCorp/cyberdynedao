"""Quiz questions for the Mathematics for Life Sciences - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Functions, variables and units in biology": (
            q(
                "What does it mean to say N is a function of t?",
                (
                    opt("Each time t gives exactly one value of N", correct=True),
                    opt("N and t are always equal"),
                    opt("t can take several values for the same N"),
                    opt("N never changes as t changes"),
                ),
                "A function assigns exactly one output to each input.",
            ),
            q(
                "What are the units of a first-order rate constant?",
                (
                    opt("1 / time, e.g. per hour", correct=True),
                    opt("concentration, e.g. micromolar"),
                    opt("dimensionless"),
                    opt("time, e.g. hours"),
                ),
                "A first-order rate constant has units of inverse time.",
            ),
            q(
                "In the linear model y = a x + b, what does the slope a represent?",
                (
                    opt("The change in y per unit change in x", correct=True),
                    opt("The value of y when x is zero"),
                    opt("The maximum value of y"),
                    opt("The area under the curve"),
                ),
                "The slope is the change in output per unit change in input.",
            ),
        ),
        "Exponential growth and doubling time": (
            q(
                "In exponential growth, the rate of increase is proportional to what?",
                (
                    opt("The current population size", correct=True),
                    opt("Time only"),
                    opt("A fixed constant independent of size"),
                    opt("The square of time"),
                ),
                "Exponential growth means the growth rate is proportional to current size.",
            ),
            q(
                "What is the doubling time for growth rate r?",
                (
                    opt("ln(2) / r", correct=True),
                    opt("r / ln(2)"),
                    opt("2 / r"),
                    opt("r times 2"),
                ),
                "Doubling time equals ln(2)/r, about 0.693/r.",
            ),
            q(
                "For exponential decay N = N0 exp(-k t), what is the half-life?",
                (
                    opt("ln(2) / k", correct=True),
                    opt("k / 2"),
                    opt("1 / k squared"),
                    opt("2 k"),
                ),
                "Half-life is ln(2)/k, the time for the quantity to halve.",
            ),
        ),
        "Logarithms: pH, log scales and linearising data": (
            q(
                "What does a drop of one pH unit mean for hydrogen-ion concentration?",
                (
                    opt("A ten-fold increase in [H+]", correct=True),
                    opt("A ten-fold decrease in [H+]"),
                    opt("No change in [H+]"),
                    opt("A doubling of [H+]"),
                ),
                "pH = -log10[H+], so one unit lower means ten times more H+.",
            ),
            q(
                "Plotting ln N versus time for exponential growth gives what?",
                (
                    opt("A straight line with slope equal to the growth rate r", correct=True),
                    opt("A curve that bends upward"),
                    opt("A flat horizontal line"),
                    opt("A parabola"),
                ),
                "Taking the log linearises exponential data; the slope is r.",
            ),
            q(
                "Which logarithm identity is correct?",
                (
                    opt("log(a b) = log a + log b", correct=True),
                    opt("log(a b) = log a times log b"),
                    opt("log(a + b) = log a + log b"),
                    opt("log(a^n) = log a + n"),
                ),
                "Logs turn products into sums: log(ab) = log a + log b.",
            ),
        ),
        "Rates of change and the derivative": (
            q(
                "Geometrically, the derivative at a point is the slope of what?",
                (
                    opt("The tangent line to the curve at that point", correct=True),
                    opt("The horizontal axis"),
                    opt("A vertical line"),
                    opt("The area under the curve"),
                ),
                "The derivative equals the slope of the tangent line.",
            ),
            q(
                "What is the derivative of exp(r t) with respect to t?",
                (
                    opt("r exp(r t)", correct=True),
                    opt("exp(r t)"),
                    opt("t exp(r t)"),
                    opt("r"),
                ),
                "The derivative of exp(r t) is r exp(r t).",
            ),
            q(
                "At a smooth peak or trough of a curve, the derivative is what?",
                (
                    opt("Zero", correct=True),
                    opt("Maximal"),
                    opt("Infinite"),
                    opt("Always negative"),
                ),
                "At a maximum or minimum the tangent is horizontal, so the slope is zero.",
            ),
        ),
        "Saturation curves: Michaelis-Menten and binding": (
            q(
                "In the Michaelis-Menten equation, what is Km?",
                (
                    opt("The substrate concentration at which v = Vmax/2", correct=True),
                    opt("The maximum reaction velocity"),
                    opt("The total enzyme concentration"),
                    opt("The product concentration at equilibrium"),
                ),
                "Km is the substrate level giving half the maximal velocity.",
            ),
            q(
                "What does Vmax represent?",
                (
                    opt("The maximum velocity when the enzyme is saturated", correct=True),
                    opt("The half-saturation concentration"),
                    opt("The dissociation constant"),
                    opt("The initial substrate concentration"),
                ),
                "Vmax is the maximum reaction rate at saturating substrate.",
            ),
            q(
                "A smaller Km indicates what about an enzyme?",
                (
                    opt(
                        "It reaches half-maximal velocity at lower substrate (higher apparent affinity)",
                        correct=True,
                    ),
                    opt("It has a higher maximum velocity"),
                    opt("It needs more substrate to work"),
                    opt("It is irreversibly inhibited"),
                ),
                "A small Km means half-speed is reached at low substrate, i.e. high affinity.",
            ),
        ),
        "Dose-response and the sigmoid curve": (
            q(
                "What does the EC50 of a dose-response curve measure?",
                (
                    opt("The dose giving 50% of the maximal response", correct=True),
                    opt("The maximal possible response"),
                    opt("The lowest detectable dose"),
                    opt("The slope of the curve"),
                ),
                "EC50 is the dose producing half the maximal effect.",
            ),
            q(
                "What does a Hill coefficient greater than 1 indicate?",
                (
                    opt("Positive cooperativity and a steeper sigmoid curve", correct=True),
                    opt("A simple hyperbolic curve"),
                    opt("No response to the drug"),
                    opt("Negative drug concentration"),
                ),
                "A Hill coefficient above 1 reflects cooperativity and a steeper S-shape.",
            ),
            q(
                "Plotted against the log of dose, a typical dose-response curve is shaped how?",
                (
                    opt("Sigmoidal (S-shaped)", correct=True),
                    opt("A straight line through the origin"),
                    opt("A downward parabola"),
                    opt("A flat line"),
                ),
                "Dose-response curves are typically sigmoidal on a log-dose axis.",
            ),
        ),
    },
    final=(
        q(
            "A bacterial culture grows exponentially with r = 0.693 per hour. Its doubling time is about?",
            (
                opt("1 hour", correct=True),
                opt("2 hours"),
                opt("0.5 hour"),
                opt("10 hours"),
            ),
            "Doubling time = ln(2)/r = 0.693/0.693 = 1 hour.",
        ),
        q(
            "Why do biologists often plot growth data on a semi-log (ln N) axis?",
            (
                opt("Exponential growth becomes a straight line whose slope is r", correct=True),
                opt("It hides the noise in the data"),
                opt("It converts the data to a parabola"),
                opt("It removes the need for units"),
            ),
            "Logs linearise exponential growth so r reads off as the slope.",
        ),
        q(
            "The derivative dN/dt represents what for a population?",
            (
                opt("The instantaneous growth rate in cells per unit time", correct=True),
                opt("The total number of cells ever produced"),
                opt("The carrying capacity"),
                opt("The doubling time"),
            ),
            "dN/dt is the instantaneous rate of change of population size.",
        ),
        q(
            "In v = Vmax[S]/(Km + [S]), at very high [S] the velocity approaches what?",
            (
                opt("Vmax", correct=True),
                opt("Km"),
                opt("Zero"),
                opt("Half of Km"),
            ),
            "As [S] grows large the curve saturates toward Vmax.",
        ),
        q(
            "What is the defining feature of a saturating curve?",
            (
                opt("Output keeps rising with diminishing returns toward a ceiling", correct=True),
                opt("Output increases without bound"),
                opt("Output decreases linearly"),
                opt("Output is constant"),
            ),
            "Saturating curves rise with diminishing returns toward a maximum.",
        ),
        q(
            "pH is defined as which of the following?",
            (
                opt("-log10 of the hydrogen-ion concentration", correct=True),
                opt("The hydrogen-ion concentration itself"),
                opt("ln of the hydroxide concentration"),
                opt("The square root of [H+]"),
            ),
            "pH = -log10[H+], a logarithmic measure of acidity.",
        ),
    ),
)
