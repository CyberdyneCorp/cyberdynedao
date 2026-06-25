"""Curated quiz questions for Probability & Statistics with Python - Basics.

Per-lesson checkpoint quizzes (keyed by the EXACT content-lesson title) plus a
final comprehensive quiz spanning the whole course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "NumPy arrays for data": (
            q(
                "Why is a NumPy `ndarray` generally faster than a Python list for numeric data?",
                (
                    opt(
                        "It is a fixed-type, contiguous block of numbers that supports "
                        "vectorised elementwise operations with no Python loop",
                        correct=True,
                    ),
                    opt("It stores each number as a separate Python object"),
                    opt("It automatically runs on the GPU"),
                    opt("It can only hold strings, which compress better"),
                ),
                "A NumPy array is a fixed-type contiguous buffer, so vectorised ops apply "
                "elementwise in fast compiled code with no Python-level loop.",
            ),
            q(
                "What does the boolean mask `a[a > 4.5]` return?",
                (
                    opt("The indices where the condition is True"),
                    opt("Only the elements of `a` that are greater than 4.5", correct=True),
                    opt("A single True/False value for the whole array"),
                    opt("The array sorted in descending order"),
                ),
                "Boolean-mask indexing keeps exactly the elements where the mask is True.",
            ),
            q(
                "What does `np.linspace(0, 1, 5)` produce?",
                (
                    opt("5 random numbers between 0 and 1"),
                    opt(
                        "5 evenly spaced points from 0 to 1, including both endpoints", correct=True
                    ),
                    opt("The integers 0, 1, 2, 3, 4"),
                    opt("A 5x5 grid of zeros"),
                ),
                "`np.linspace(start, stop, num)` returns `num` evenly spaced values including "
                "both endpoints.",
            ),
        ),
        "Descriptive statistics with NumPy & pandas": (
            q(
                "To get a sample variance (dividing by `n - 1`) with NumPy, which argument do you set?",
                (
                    opt("`bins=1`"),
                    opt("`ddof=1`", correct=True),
                    opt("`axis=1`"),
                    opt("`sample=True`"),
                ),
                "NumPy defaults to `ddof=0` (population). Pass `ddof=1` to divide by `n - 1` "
                "for the sample variance/standard deviation.",
            ),
            q(
                "Which measure of centre is robust to outliers?",
                (
                    opt("The mean"),
                    opt("The median", correct=True),
                    opt("The variance"),
                    opt("The standard deviation"),
                ),
                "The median is the middle value and is robust to outliers, unlike the mean.",
            ),
            q(
                "What does `df.describe()` return for a numeric DataFrame?",
                (
                    opt("Only the column names and dtypes"),
                    opt(
                        "A summary table of count, mean, std, min, the quartiles, and max per column",
                        correct=True,
                    ),
                    opt("A single correlation coefficient"),
                    opt("The first five rows of the data"),
                ),
                "`describe()` gives count, mean, std, min, 25%/50%/75% quantiles and max for "
                "each numeric column.",
            ),
        ),
        "Probability foundations & random sampling": (
            q(
                "What is the recommended modern way to get reproducible random numbers in NumPy?",
                (
                    opt("`np.random.default_rng(seed)` and reuse that Generator", correct=True),
                    opt("Call `np.random.rand()` repeatedly without seeding"),
                    opt("Use Python's built-in `random` module instead"),
                    opt("Set the system clock to a fixed time"),
                ),
                "Modern NumPy uses an explicit `Generator` from `np.random.default_rng(seed)`, "
                "which is reproducible when reused.",
            ),
            q(
                "As the number of fair-coin flips grows, what happens to the running proportion of heads?",
                (
                    opt("It diverges away from 0.5"),
                    opt(
                        "It converges toward the true probability 0.5 (law of large numbers)",
                        correct=True,
                    ),
                    opt("It stays fixed at the value of the first flip"),
                    opt("It oscillates forever between 0 and 1 without settling"),
                ),
                "By the law of large numbers, the observed frequency converges to the true "
                "probability as the number of trials grows.",
            ),
            q(
                "How do you draw 5 distinct positions (no repeats) from 0..19 with a Generator `rng`?",
                (
                    opt("`rng.choice(20, size=5, replace=False)`", correct=True),
                    opt("`rng.integers(0, 20, size=5)`"),
                    opt("`rng.normal(0, 20, size=5)`"),
                    opt("`rng.random(5)`"),
                ),
                "`rng.choice(20, size=5, replace=False)` samples 5 distinct values without "
                "replacement.",
            ),
        ),
        "Common distributions with scipy.stats": (
            q(
                "For a discrete distribution like the Binomial, which method gives the probability of an exact value?",
                (
                    opt("`pdf`"),
                    opt("`pmf`", correct=True),
                    opt("`rvs`"),
                    opt("`ppf`"),
                ),
                "Discrete distributions use `pmf` (probability mass); continuous ones use "
                "`pdf` (probability density).",
            ),
            q(
                "What does `scipy.stats.norm(loc=3, scale=1).cdf(3)` return?",
                (
                    opt("0.0"),
                    opt("0.5", correct=True),
                    opt("1.0"),
                    opt("3.0"),
                ),
                "The CDF at the mean of a Normal is 0.5 — half the probability mass lies below "
                "the mean.",
            ),
            q(
                "Which `scipy.stats` method generates random draws from a distribution?",
                (
                    opt("`cdf`"),
                    opt("`pmf`"),
                    opt("`rvs`", correct=True),
                    opt("`mean`"),
                ),
                "`rvs` (random variates) draws samples from the distribution.",
            ),
        ),
        "Visualising data: histograms, box plots & scatter": (
            q(
                "Which plot best shows the shape of a single variable's distribution?",
                (
                    opt("A histogram", correct=True),
                    opt("A scatter plot"),
                    opt("A line of best fit"),
                    opt("A correlation matrix"),
                ),
                "A histogram bins one variable and shows the shape of its distribution.",
            ),
            q(
                "What does the box in a box plot span?",
                (
                    opt("The full range from min to max"),
                    opt("The interquartile range, from Q1 to Q3", correct=True),
                    opt("Plus or minus one standard deviation"),
                    opt("The 95% confidence interval"),
                ),
                "The box spans the interquartile range (Q1 to Q3) with the median marked inside.",
            ),
            q(
                "Which plot is best for showing the relationship between two numeric variables?",
                (
                    opt("A histogram"),
                    opt("A box plot"),
                    opt("A scatter plot", correct=True),
                    opt("A pie chart"),
                ),
                "A scatter plot places one variable on each axis to reveal their relationship.",
            ),
        ),
        "pandas DataFrames & Series for tabular data": (
            q(
                "What is the difference between a pandas `Series` and a `DataFrame`?",
                (
                    opt(
                        "A `Series` is one labelled column; a `DataFrame` is a whole table",
                        correct=True,
                    ),
                    opt("A `Series` holds only strings; a `DataFrame` holds only numbers"),
                    opt("They are identical names for the same object"),
                    opt("A `Series` is two-dimensional; a `DataFrame` is one-dimensional"),
                ),
                "A `Series` is a single labelled column; a `DataFrame` is a table of multiple "
                "columns.",
            ),
            q(
                "How do you keep only the rows where the `temp` column exceeds 29?",
                (
                    opt("`df[df['temp'] > 29]`", correct=True),
                    opt("`df.temp.describe()`"),
                    opt("`df.groupby('temp')`"),
                    opt("`df.sort_values('temp')`"),
                ),
                "Boolean masking with `df[df['temp'] > 29]` filters rows that satisfy the "
                "condition.",
            ),
            q(
                "What does `df.groupby('city')['temp'].mean()` compute?",
                (
                    opt("The overall mean temperature ignoring city"),
                    opt("The mean temperature for each city (split-apply-combine)", correct=True),
                    opt("The number of cities in the table"),
                    opt("The correlation between city and temperature"),
                ),
                "`groupby` splits rows by city, then `.mean()` aggregates the temp within each "
                "group.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about NumPy vectorised operations is correct?",
            (
                opt("They require an explicit Python `for` loop over each element"),
                opt(
                    "They apply elementwise in fast compiled code, e.g. `celsius * 9 / 5 + 32`",
                    correct=True,
                ),
                opt("They only work on arrays of length 1"),
                opt("They convert the array to a Python list first"),
            ),
            "Vectorised ops apply elementwise without a Python loop, which is why NumPy is fast.",
        ),
        q(
            "Which call divides by `n - 1` to give a sample standard deviation?",
            (
                opt("`x.std()` with no arguments"),
                opt("`x.std(ddof=1)`", correct=True),
                opt("`x.std(ddof=0)`"),
                opt("`np.median(x)`"),
            ),
            "`ddof=1` makes NumPy divide by `n - 1`, giving the sample (not population) "
            "standard deviation.",
        ),
        q(
            "What is the modern, reproducible way to sample random numbers in NumPy?",
            (
                opt("`rng = np.random.default_rng(seed)` then call methods on `rng`", correct=True),
                opt("Repeated `np.random.rand()` calls with no seed"),
                opt("Reading from `/dev/urandom` directly"),
                opt("Using `math.random` from the standard library"),
            ),
            "`np.random.default_rng(seed)` returns a Generator that produces reproducible streams.",
        ),
        q(
            "For a continuous distribution in `scipy.stats`, which method gives the density at a point?",
            (
                opt("`pmf`"),
                opt("`pdf`", correct=True),
                opt("`rvs`"),
                opt("`cdf`"),
            ),
            "Continuous distributions expose `pdf` (density); discrete ones expose `pmf`.",
        ),
        q(
            "Which plot reveals the relationship between two numeric variables?",
            (
                opt("A histogram"),
                opt("A box plot"),
                opt("A scatter plot", correct=True),
                opt("A bar chart of one column"),
            ),
            "A scatter plot maps each observation to (x, y) so you can see how two variables "
            "relate.",
        ),
        q(
            "What does the split-apply-combine pattern `df.groupby('city')['temp'].mean()` do?",
            (
                opt("Computes one overall mean across all rows"),
                opt("Splits rows by city, then averages temp within each group", correct=True),
                opt("Drops the city column"),
                opt("Sorts the DataFrame by temperature"),
            ),
            "`groupby` splits the rows into groups by city and applies the mean aggregation to "
            "each.",
        ),
    ),
)
