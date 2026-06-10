from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Joins": (
            q(
                "What does an INNER JOIN return?",
                (
                    opt("All rows from the left table with NULLs on the right"),
                    opt("Only the rows that match in both tables", correct=True),
                    opt("All rows from both tables regardless of any match"),
                    opt("All right rows with NULLs on the left"),
                ),
                "An INNER JOIN keeps only rows that have a match in both tables.",
            ),
            q(
                "Which join returns all left rows, filling NULLs where the right table has no match?",
                (
                    opt("INNER JOIN"),
                    opt("RIGHT JOIN"),
                    opt("LEFT JOIN", correct=True),
                    opt("CROSS JOIN"),
                ),
                "A LEFT JOIN returns all left rows and uses NULLs where the right table has no match.",
            ),
            q(
                "What links rows across separate tables so a join can stitch them back together?",
                (
                    opt("Foreign keys", correct=True),
                    opt("Table aliases"),
                    opt("Aggregate functions"),
                    opt("Indexes"),
                ),
                "Real schemas split data across tables and link them with foreign keys.",
            ),
        ),
        "Aggregation & grouping": (
            q(
                "What does GROUP BY do?",
                (
                    opt("Computes an aggregate per group", correct=True),
                    opt("Sorts the result rows in ascending order"),
                    opt("Removes duplicate columns from the output"),
                    opt("Joins two tables on a shared column"),
                ),
                "GROUP BY computes an aggregate value for each group of rows.",
            ),
            q(
                "What is the difference between WHERE and HAVING?",
                (
                    opt("WHERE filters groups after grouping; HAVING filters rows before"),
                    opt(
                        "WHERE filters rows before grouping; HAVING filters groups after",
                        correct=True,
                    ),
                    opt("They are interchangeable and do exactly the same thing"),
                    opt("WHERE only works with joins; HAVING only works with subqueries"),
                ),
                "WHERE filters rows before grouping while HAVING filters groups after they are formed.",
            ),
            q(
                "Which of these is an aggregate function that collapses many rows into one value?",
                (
                    opt("JOIN"),
                    opt("AVG", correct=True),
                    opt("WHERE"),
                    opt("INDEX"),
                ),
                "AVG is an aggregate function, like COUNT, MAX, MIN, and SUM.",
            ),
        ),
        "Subqueries, indexes & transactions": (
            q(
                "What is an index used for?",
                (
                    opt("Grouping rows so aggregates can be computed per group"),
                    opt(
                        "Making WHERE and JOIN on a column fast at the cost of slower writes",
                        correct=True,
                    ),
                    opt("Undoing all statements in a transaction"),
                    opt("Combining the rows of two tables that match"),
                ),
                "An index is a lookup structure that speeds up WHERE and JOIN on a column but slows writes slightly.",
            ),
            q(
                "In a transaction, what does ROLLBACK do if something fails before COMMIT?",
                (
                    opt("Leaves the data untouched, undoing everything", correct=True),
                    opt("Commits only the statements that already succeeded"),
                    opt("Creates an index to retry the failed statement"),
                    opt("Permanently saves the partial changes made so far"),
                ),
                "ROLLBACK leaves the data untouched so there are no half-finished transfers.",
            ),
            q(
                "What is a subquery?",
                (
                    opt("A query inside a query", correct=True),
                    opt("A statement that creates a new index"),
                    opt("A group of statements that succeed or fail together"),
                    opt("A function that collapses many rows into one value"),
                ),
                "A subquery is a query nested inside another query.",
            ),
        ),
    },
    final=(
        q(
            "Which join returns only rows that match in both tables?",
            (
                opt("LEFT JOIN"),
                opt("RIGHT JOIN"),
                opt("INNER JOIN", correct=True),
                opt("CROSS JOIN"),
            ),
            "INNER JOIN keeps only the rows that match in both tables.",
        ),
        q(
            "To keep only groups with more than five people, which clause filters the groups?",
            (
                opt("WHERE COUNT(*) > 5 before GROUP BY"),
                opt("HAVING COUNT(*) > 5 after GROUP BY", correct=True),
                opt("ORDER BY COUNT(*) > 5"),
                opt("JOIN ON COUNT(*) > 5"),
            ),
            "HAVING filters groups after grouping, so it can use an aggregate like COUNT(*).",
        ),
        q(
            "What trade-off comes with adding an index on a column?",
            (
                opt("Faster reads and faster writes with no downside"),
                opt("Faster filtering and joins but slightly slower writes", correct=True),
                opt("Slower reads in exchange for faster writes"),
                opt("It removes the need for foreign keys"),
            ),
            "An index speeds up WHERE and JOIN lookups at the cost of slightly slower writes.",
        ),
        q(
            "What does COMMIT do at the end of a transaction?",
            (
                opt("Undoes every statement in the transaction"),
                opt("Makes all the grouped statements take effect together", correct=True),
                opt("Creates an index on the updated columns"),
                opt("Starts a new transaction block"),
            ),
            "COMMIT applies the grouped statements together, while ROLLBACK undoes them all.",
        ),
        q(
            "What keeps multi-table queries readable when joining users and orders?",
            (
                opt("Table aliases such as u and o", correct=True),
                opt("Removing all foreign keys"),
                opt("Indexing every column"),
                opt("Using HAVING instead of WHERE"),
            ),
            "Table aliases like u and o keep multi-table join queries readable.",
        ),
    ),
)
