"""Quiz questions for the R & Data Analysis - Basics course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is R and the RStudio workflow": (
            q(
                "Which operator is the conventional way to assign a value in R?",
                (
                    opt("<-", correct=True),
                    opt("=="),
                    opt("=>"),
                    opt(":="),
                ),
                "R uses the arrow <- for assignment; == is the equality test.",
            ),
            q(
                "Why prefer writing a script or Quarto document over typing only at the console?",
                (
                    opt("It makes the analysis reproducible and re-runnable", correct=True),
                    opt("Scripts run faster than the console"),
                    opt("The console cannot load packages"),
                    opt("Scripts skip the need to install packages"),
                ),
                "A saved script captures every step so the whole analysis can be re-run.",
            ),
            q(
                "What does it mean that R is 'vectorised'?",
                (
                    opt("Operations apply to whole vectors at once", correct=True),
                    opt("All data must be stored as images"),
                    opt("You must write explicit for-loops for arithmetic"),
                    opt("Vectors can only hold one element"),
                ),
                "Vectorised operations act element-wise across an entire vector without an explicit loop.",
            ),
        ),
        "Atomic vectors and vectorised arithmetic": (
            q(
                "What happens in R when two vectors of different lengths are added?",
                (
                    opt("The shorter one is recycled to match the longer", correct=True),
                    opt("R always raises an error"),
                    opt("The longer one is truncated to the shorter"),
                    opt("Only the first element of each is used"),
                ),
                "R recycles the shorter vector, which is powerful but a common source of silent bugs.",
            ),
            q(
                "Indexing in R is:",
                (
                    opt("1-based", correct=True),
                    opt("0-based"),
                    opt("Random"),
                    opt("Only by name, never by position"),
                ),
                "R vectors are indexed starting at 1.",
            ),
            q(
                "How do you skip missing values in many summary functions?",
                (
                    opt("Pass na.rm = TRUE", correct=True),
                    opt("Pass skip = TRUE"),
                    opt("Convert NA to 0 first, always"),
                    opt("Missing values are skipped automatically"),
                ),
                "Functions like mean() ignore NA only when na.rm = TRUE is set.",
            ),
        ),
        "Data structures: lists, factors and data frames": (
            q(
                "Which structure can hold elements of different types, including other lists?",
                (
                    opt("A list", correct=True),
                    opt("An atomic vector"),
                    opt("A matrix"),
                    opt("A factor"),
                ),
                "Lists are heterogeneous containers; atomic vectors and matrices hold one type only.",
            ),
            q(
                "A data frame is best described as:",
                (
                    opt("A list of equal-length columns of possibly different types", correct=True),
                    opt("A single atomic vector"),
                    opt("A matrix where every column is the same type"),
                    opt("A function that returns rows"),
                ),
                "Each column can be a different type but all columns share the same length.",
            ),
            q(
                "A factor stores a categorical variable as:",
                (
                    opt("Integer codes plus a set of levels", correct=True),
                    opt("Raw character strings only"),
                    opt("Floating-point numbers"),
                    opt("A nested list of dates"),
                ),
                "Factors are integer codes with an attached vector of levels.",
            ),
        ),
        "Importing and inspecting data": (
            q(
                "Which function gives a fast import returning a tibble with inferred types?",
                (
                    opt("readr::read_csv()", correct=True),
                    opt("plot()"),
                    opt("summary()"),
                    opt("library()"),
                ),
                "read_csv from readr is the fast tidyverse CSV reader producing a tibble.",
            ),
            q(
                "A stray 'N/A' string in a numeric column typically causes:",
                (
                    opt("The whole column to be read as character", correct=True),
                    opt("The file to fail to open"),
                    opt("R to delete the column"),
                    opt("All numbers to round to integers"),
                ),
                "A non-numeric token coerces the entire column to character, so inspect types early.",
            ),
            q(
                "Which call reports the number of missing values per column?",
                (
                    opt("colSums(is.na(df))", correct=True),
                    opt("nrow(df)"),
                    opt("names(df)"),
                    opt("plot(df)"),
                ),
                "is.na() flags NA per cell; colSums adds them per column.",
            ),
        ),
        "Subsetting, summarising and tabulating": (
            q(
                "In base R, df[df$group == 'treat', ] does what?",
                (
                    opt("Keeps the rows where group equals 'treat'", correct=True),
                    opt("Drops the group column"),
                    opt("Sorts the data by group"),
                    opt("Renames the group column"),
                ),
                "A logical condition before the comma selects matching rows.",
            ),
            q(
                "Which function builds a frequency table of a categorical variable?",
                (
                    opt("table()", correct=True),
                    opt("mean()"),
                    opt("hist()"),
                    opt("lm()"),
                ),
                "table() counts occurrences of each level.",
            ),
            q(
                "aggregate(expr ~ group, data = d, FUN = mean) computes:",
                (
                    opt("The mean of expr within each group", correct=True),
                    opt("The total number of rows"),
                    opt("A scatter plot of expr vs group"),
                    opt("The correlation between expr and group"),
                ),
                "It applies the function per group defined by the right-hand side of the formula.",
            ),
        ),
        "A first plot with base graphics": (
            q(
                "Which base function shows the distribution of a single numeric variable?",
                (
                    opt("hist()", correct=True),
                    opt("aggregate()"),
                    opt("table()"),
                    opt("summary()"),
                ),
                "A histogram displays the distribution of one numeric variable.",
            ),
            q(
                "boxplot(expr ~ group, data = d) is useful for:",
                (
                    opt("Comparing the spread of expr across groups", correct=True),
                    opt("Fitting a regression model"),
                    opt("Reading a CSV file"),
                    opt("Joining two tables"),
                ),
                "A grouped boxplot compares the distribution of a variable across categories.",
            ),
            q(
                "A scatter of response vs dose often follows which shape for a logistic dose-response?",
                (
                    opt("A sigmoid (S-shaped) curve", correct=True),
                    opt("A perfectly flat line"),
                    opt("A vertical line"),
                    opt("A decreasing straight line through the origin"),
                ),
                "Logistic dose-response rises in an S-shape, the basis of EC50 estimation.",
            ),
        ),
    },
    final=(
        q(
            "Which assignment and comment characters does R use?",
            (
                opt("<- to assign, # to comment", correct=True),
                opt("= to comment, // to assign"),
                opt(":= to assign, ; to comment"),
                opt("<- to comment, # to assign"),
            ),
            "R assigns with <- and starts comments with #.",
        ),
        q(
            "An atomic vector requires that all elements:",
            (
                opt("Share a single type", correct=True),
                opt("Be of different types"),
                opt("Be character strings"),
                opt("Be missing"),
            ),
            "Atomic vectors are homogeneous; mixed types need a list.",
        ),
        q(
            "Which structure anchors most data analysis in R?",
            (
                opt("The data frame (or tibble)", correct=True),
                opt("The single scalar"),
                opt("The S4 object"),
                opt("The environment"),
            ),
            "Rows as observations and columns as variables make the data frame central.",
        ),
        q(
            "Before any statistics you should:",
            (
                opt("Inspect dimensions, types and missing values", correct=True),
                opt("Immediately publish results"),
                opt("Delete all rows with any value"),
                opt("Run a t-test without looking at the data"),
            ),
            "head, str, summary and missing-value checks catch most problems early.",
        ),
        q(
            "Logical subsetting df[df$x > 2, ] returns:",
            (
                opt("Rows where x exceeds 2", correct=True),
                opt("The mean of x"),
                opt("A sorted copy of df"),
                opt("Only the x column"),
            ),
            "A logical vector before the comma filters rows.",
        ),
        q(
            "Which is the recommended habit for understanding data quickly?",
            (
                opt("Plot early and often", correct=True),
                opt("Avoid plots until the end"),
                opt("Trust summary statistics alone"),
                opt("Never use histograms"),
            ),
            "Visualising data exposes structure that single statistics hide.",
        ),
    ),
)
