"""Quiz questions for the R & Data Analysis - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The tidyverse and dplyr verbs": (
            q(
                "What does the pipe |> do?",
                (
                    opt(
                        "Passes the left value as the first argument of the next call", correct=True
                    ),
                    opt("Multiplies two vectors"),
                    opt("Comments out a line"),
                    opt("Imports a package"),
                ),
                "The pipe chains operations so code reads top-to-bottom.",
            ),
            q(
                "Which pair implements split-apply-combine in dplyr?",
                (
                    opt("group_by() then summarise()", correct=True),
                    opt("select() then arrange()"),
                    opt("filter() then rename()"),
                    opt("read_csv() then library()"),
                ),
                "group_by defines the groups and summarise collapses each to a summary.",
            ),
            q(
                "Which verb adds or transforms a column?",
                (
                    opt("mutate()", correct=True),
                    opt("filter()"),
                    opt("arrange()"),
                    opt("select()"),
                ),
                "mutate() creates or modifies columns; filter selects rows.",
            ),
        ),
        "Reshaping and joining with tidyr": (
            q(
                "pivot_longer() converts data:",
                (
                    opt("From wide to long form", correct=True),
                    opt("From long to wide form"),
                    opt("From numeric to character"),
                    opt("From a tibble to a matrix"),
                ),
                "It gathers wide columns into key/value rows; pivot_wider does the reverse.",
            ),
            q(
                "A left_join(a, b) keeps:",
                (
                    opt("All rows of a, with NA where b has no match", correct=True),
                    opt("Only rows present in both a and b"),
                    opt("Only rows unique to b"),
                    opt("No rows at all"),
                ),
                "left_join retains every row of the left table, filling unmatched right columns with NA.",
            ),
            q(
                "Why is the long format preferred for ggplot2 and modelling?",
                (
                    opt(
                        "It is tidy: one observation per row, one variable per column", correct=True
                    ),
                    opt("It uses less memory than any other layout"),
                    opt("It cannot contain missing values"),
                    opt("It removes the need for metadata"),
                ),
                "Tidy long data maps cleanly onto aesthetics and model formulas.",
            ),
        ),
        "ggplot2 and the grammar of graphics": (
            q(
                "In ggplot2, what does aes() specify?",
                (
                    opt("The mapping from variables to visual channels", correct=True),
                    opt("The file path to save the plot"),
                    opt("The statistical test to run"),
                    opt("The number of CPU cores"),
                ),
                "aes maps variables like x, y and colour to visual properties.",
            ),
            q(
                "Layers in ggplot2 are combined with:",
                (
                    opt("The + operator", correct=True),
                    opt("The |> pipe"),
                    opt("A comma"),
                    opt("The %in% operator"),
                ),
                "ggplot2 adds geoms, scales and themes with +.",
            ),
            q(
                "facet_wrap(~ group) produces:",
                (
                    opt("Small multiples, one panel per group", correct=True),
                    opt("A single merged panel"),
                    opt("A statistical summary table"),
                    opt("A log-scaled axis"),
                ),
                "Faceting splits the plot into one panel per level of the faceting variable.",
            ),
        ),
        "Linear models with lm()": (
            q(
                "lm() fits its coefficients by:",
                (
                    opt("Ordinary least squares", correct=True),
                    opt("Maximum entropy"),
                    opt("Random sampling"),
                    opt("Gradient-free search only"),
                ),
                "lm minimises the sum of squared residuals (OLS).",
            ),
            q(
                "A coefficient beta_j in a multiple linear model represents:",
                (
                    opt(
                        "The expected change in y per unit of x_j, holding others fixed",
                        correct=True,
                    ),
                    opt("The correlation between y and x_j ignoring others"),
                    opt("The residual standard error"),
                    opt("The total variance of y"),
                ),
                "Each slope is a partial effect with the other predictors held constant.",
            ),
            q(
                "Which diagnostic checks the constant-variance and linearity assumptions?",
                (
                    opt("Residuals-vs-fitted plot", correct=True),
                    opt("A bar chart of coefficients"),
                    opt("The correlation matrix of predictors"),
                    opt("The number of rows"),
                ),
                "plot(fit) gives residuals vs fitted for linearity and homoscedasticity.",
            ),
        ),
        "GLMs and hypothesis testing": (
            q(
                "For a binary outcome you fit a GLM with which family and link?",
                (
                    opt("Binomial family, logit link (logistic regression)", correct=True),
                    opt("Poisson family, log link"),
                    opt("Gaussian family, identity link"),
                    opt("Gamma family, inverse link"),
                ),
                "Logistic regression models a binary response with the binomial family and logit link.",
            ),
            q(
                "Which test compares the means of more than two groups?",
                (
                    opt("ANOVA", correct=True),
                    opt("Chi-square test"),
                    opt("Paired t-test for two groups only"),
                    opt("Pearson correlation"),
                ),
                "ANOVA generalises the two-sample t-test to several group means.",
            ),
            q(
                "A p-value is:",
                (
                    opt("The probability of data this extreme if the null were true", correct=True),
                    opt("The probability the null hypothesis is true"),
                    opt("The probability the alternative is true"),
                    opt("The effect size"),
                ),
                "It quantifies evidence against the null, not the probability the null holds.",
            ),
        ),
        "Reproducible analysis with Quarto": (
            q(
                "Quarto (.qmd) documents:",
                (
                    opt("Interleave prose, code and output and render to a report", correct=True),
                    opt("Only store raw data"),
                    opt("Replace the need for any code"),
                    opt("Are a type of database"),
                ),
                "Quarto renders code chunks with their output into HTML/PDF/Word.",
            ),
            q(
                "Which tool pins package versions for a restorable environment?",
                (
                    opt("renv", correct=True),
                    opt("ggplot2"),
                    opt("dplyr"),
                    opt("table()"),
                ),
                "renv records and restores the exact package versions used.",
            ),
            q(
                "Why call set.seed(42) before random steps?",
                (
                    opt("So the random results reproduce exactly on re-run", correct=True),
                    opt("To make the analysis run faster"),
                    opt("To install packages"),
                    opt("To remove missing values"),
                ),
                "Fixing the seed makes pseudo-random output deterministic and reproducible.",
            ),
        ),
    },
    final=(
        q(
            "The five core dplyr verbs include filter, select, mutate, arrange and:",
            (
                opt("summarise", correct=True),
                opt("ggplot"),
                opt("read_csv"),
                opt("install.packages"),
            ),
            "summarise (with group_by) collapses groups to summaries.",
        ),
        q(
            "pivot_wider() is the inverse of:",
            (
                opt("pivot_longer()", correct=True),
                opt("left_join()"),
                opt("mutate()"),
                opt("lm()"),
            ),
            "The two pivot functions reshape between wide and long form.",
        ),
        q(
            "A ggplot2 plot is built from data, an aesthetic mapping and:",
            (
                opt("one or more geoms", correct=True),
                opt("a single p-value"),
                opt("a database connection"),
                opt("a random seed"),
            ),
            "Geoms (points, lines, bars) draw the mapped data.",
        ),
        q(
            "Count data with over-dispersion are best modelled with:",
            (
                opt("A Poisson or negative-binomial GLM", correct=True),
                opt("An ordinary least-squares line on the raw counts"),
                opt("A logistic regression on the counts"),
                opt("No model at all"),
            ),
            "Counts use a log-link GLM; over-dispersion favours the negative binomial.",
        ),
        q(
            "Benjamini-Hochberg adjustment is most relevant when you:",
            (
                opt(
                    "Test many hypotheses and want to control the false discovery rate",
                    correct=True,
                ),
                opt("Fit a single linear model"),
                opt("Read a CSV file"),
                opt("Make one boxplot"),
            ),
            "BH controls the FDR across many simultaneous tests (covered further in Advanced).",
        ),
        q(
            "The cornerstone of a reproducible R analysis is:",
            (
                opt("One document that runs top to bottom from data to report", correct=True),
                opt("Many undocumented manual console steps"),
                opt("Storing results only as screenshots"),
                opt("Avoiding version control"),
            ),
            "Automating every step from data to output keeps results re-runnable.",
        ),
    ),
)
