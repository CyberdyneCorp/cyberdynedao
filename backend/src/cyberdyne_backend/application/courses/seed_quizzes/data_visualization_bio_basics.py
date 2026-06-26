"""Quiz questions for the Scientific Data Visualization - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why visualise data": (
            q(
                "What does Anscombe's quartet demonstrate?",
                (
                    opt(
                        "Datasets with identical summary statistics can look totally different when plotted",
                        correct=True,
                    ),
                    opt("Larger samples always have smaller variance"),
                    opt("Correlation always implies causation"),
                    opt("Pie charts outperform bar charts"),
                ),
                "Anscombe built four datasets with matching mean, variance, correlation and regression line that look completely different graphed.",
            ),
            q(
                "Exploratory versus explanatory graphics differ mainly in:",
                (
                    opt(
                        "Audience and purpose: finding patterns vs communicating one message",
                        correct=True,
                    ),
                    opt("The programming language used"),
                    opt("Whether they use colour"),
                    opt("The file format they are saved in"),
                ),
                "Exploratory graphics are fast and for the analyst; explanatory graphics are polished for a reader.",
            ),
            q(
                "Which is a core rule of a good figure?",
                (
                    opt("Make comparison easy and minimise non-data ink", correct=True),
                    opt("Maximise decorative 3-D effects"),
                    opt("Use as many colours as possible"),
                    opt("Always use a pie chart"),
                ),
                "Good figures show the data, reduce chartjunk and make the intended comparison effortless.",
            ),
        ),
        "The grammar of graphics": (
            q(
                "In the grammar of graphics, a chart is built from:",
                (
                    opt(
                        "Composable layers: data, aesthetic mapping, scale, geometry, facet",
                        correct=True,
                    ),
                    opt("A fixed menu of named chart types"),
                    opt("Only colours and fonts"),
                    opt("A single immutable template"),
                ),
                "Wilkinson's grammar decomposes charts into orthogonal layers rather than naming types.",
            ),
            q(
                "An aesthetic mapping specifies:",
                (
                    opt("Which data column drives x, y, colour, size or shape", correct=True),
                    opt("The page margins"),
                    opt("The export resolution"),
                    opt("The random seed"),
                ),
                "Mappings bind data columns to visual channels through scales.",
            ),
            q(
                "Which library implements the grammar of graphics?",
                (
                    opt("ggplot2 / Vega-Lite / plotnine", correct=True),
                    opt("NumPy"),
                    opt("Pandas only"),
                    opt("OpenSSL"),
                ),
                "ggplot2, Vega-Lite and plotnine are direct implementations of the grammar.",
            ),
        ),
        "Perceptual encoding & channels": (
            q(
                "By Cleveland & McGill, the most accurately perceived channel is:",
                (
                    opt("Position on a common scale", correct=True),
                    opt("Area"),
                    opt("Colour saturation"),
                    opt("Angle"),
                ),
                "Position on aligned scales tops the ranking; area and colour are far less accurate.",
            ),
            q(
                "Why does a dot plot or bar chart usually beat a pie chart?",
                (
                    opt(
                        "It uses high-accuracy length and position instead of angle and area",
                        correct=True,
                    ),
                    opt("It always uses fewer colours"),
                    opt("Pie charts cannot show categories"),
                    opt("Bars are required by journals"),
                ),
                "Pies force angle and area comparisons, which sit low on the perceptual ranking.",
            ),
            q(
                "Stevens' power law with exponent below 1 for area implies:",
                (
                    opt("Large areas are systematically underestimated", correct=True),
                    opt("Areas are perceived perfectly"),
                    opt("Small areas look larger than they are"),
                    opt("Colour is the best channel"),
                ),
                "With a<1, doubling the data value produces less than a doubling in perceived area.",
            ),
        ),
        "Colour done right": (
            q(
                "Log fold-change centred on zero is best shown with which palette?",
                (
                    opt("Diverging", correct=True),
                    opt("Sequential"),
                    opt("Qualitative"),
                    opt("Rainbow / jet"),
                ),
                "Diverging palettes have a neutral midpoint, ideal for data with a meaningful centre.",
            ),
            q(
                "Why is the rainbow (jet) colormap discouraged?",
                (
                    opt(
                        "It is not perceptually uniform and fails for colour-blind readers",
                        correct=True,
                    ),
                    opt("It is too dark to print"),
                    opt("It uses too few colours"),
                    opt("It only works for categorical data"),
                ),
                "Jet introduces false boundaries, has uneven perceived steps and is hard for red-green deficiency.",
            ),
            q(
                "An unordered set of cell types should use a:",
                (
                    opt("Qualitative palette", correct=True),
                    opt("Sequential palette"),
                    opt("Diverging palette"),
                    opt("Single-hue gradient"),
                ),
                "Qualitative palettes use distinct hues of similar lightness for categories with no order.",
            ),
        ),
        "Choosing the right chart": (
            q(
                "To show the relationship between two numeric variables, use a:",
                (
                    opt("Scatter plot", correct=True),
                    opt("Pie chart"),
                    opt("Single bar"),
                    opt("Word cloud"),
                ),
                "Scatter plots map two numerics to x and y; add a smoother for the trend.",
            ),
            q(
                "A lie factor near 1 means:",
                (
                    opt("The visual effect matches the size of the data effect", correct=True),
                    opt("The chart is in greyscale"),
                    opt("The axis is logarithmic"),
                    opt("There are exactly two series"),
                ),
                "Lie factor is the ratio of visual change to data change; ~1 is honest.",
            ),
            q(
                "Which axis must start at zero?",
                (
                    opt("A bar chart axis (bars encode length)", correct=True),
                    opt("Every line chart axis"),
                    opt("A log axis"),
                    opt("A time axis"),
                ),
                "Bars encode magnitude via length, so truncating the axis distorts; line charts encode slope and need not start at zero.",
            ),
        ),
    },
    final=(
        q(
            "The data-ink ratio principle says to:",
            (
                opt(
                    "Maximise the fraction of ink that encodes data and erase chartjunk",
                    correct=True,
                ),
                opt("Use as much decoration as possible"),
                opt("Always add a 3-D effect"),
                opt("Print in colour only"),
            ),
            "Tufte's data-ink ratio favours stripping non-data ink.",
        ),
        q(
            "Which channel should carry the quantity you most want compared?",
            (
                opt("Position", correct=True),
                opt("Colour hue"),
                opt("Area"),
                opt("Texture"),
            ),
            "Position on a common scale is the highest-accuracy channel.",
        ),
        q(
            "Gene expression from low to high is best encoded with a:",
            (
                opt("Sequential palette such as viridis", correct=True),
                opt("Qualitative palette"),
                opt("Diverging palette"),
                opt("Rainbow palette"),
            ),
            "Ordered magnitude with no meaningful centre calls for a perceptually-uniform sequential map.",
        ),
        q(
            "A histogram answers questions about:",
            (
                opt("The distribution of a single variable", correct=True),
                opt("Change over time only"),
                opt("Part-to-whole composition"),
                opt("Network connectivity"),
            ),
            "Histograms (and densities) show how one variable is distributed.",
        ),
        q(
            "Encoding information by hue alone is risky because:",
            (
                opt("Colour-blind readers may not distinguish the categories", correct=True),
                opt("Hue is the most accurate channel"),
                opt("It saves ink"),
                opt("It is required by the grammar of graphics"),
            ),
            "Always pair hue with shape, position or labels for accessibility.",
        ),
        q(
            "Exploratory graphics are characterised by being:",
            (
                opt("Fast, disposable and aimed at finding patterns", correct=True),
                opt("Highly polished for publication"),
                opt("Always interactive"),
                opt("Never made by the analyst"),
            ),
            "They are working tools for the analyst, unlike polished explanatory figures.",
        ),
    ),
)
