"""Curated quiz questions for the SQL - Basics course (per-lesson checkpoints
plus a final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Relational databases & SQL": (
            q(
                "In a relational database, how is data organized?",
                (
                    opt("As nested documents with flexible keys"),
                    opt(
                        "In tables made of rows and columns, like a strict spreadsheet",
                        correct=True,
                    ),
                    opt("As a single continuous stream of bytes"),
                    opt("In a graph of nodes and edges"),
                ),
                "A relational database stores data in tables with rows (records) and columns (fields), like a strict spreadsheet.",
            ),
            q(
                "What does a schema define for each table?",
                (
                    opt(
                        "The columns and their types such as INTEGER, TEXT, and DATE", correct=True
                    ),
                    opt("The physical disk blocks where rows are stored"),
                    opt("The network port the database listens on"),
                    opt("The order in which rows must be inserted"),
                ),
                "A schema defines each table's columns and their types like INTEGER, TEXT, and DATE.",
            ),
            q(
                "What does it mean that SQL is declarative?",
                (
                    opt("You must specify the exact algorithm used to read rows"),
                    opt(
                        "You say what you want, not how to fetch it, and the query planner decides how",
                        correct=True,
                    ),
                    opt("Every statement must be written in lowercase"),
                    opt("You can only declare tables, never query them"),
                ),
                "SQL is declarative: you say what you want and the database's query planner figures out how to fetch it.",
            ),
        ),
        "Querying with SELECT": (
            q(
                "Which clause filters which rows a SELECT returns?",
                (
                    opt("ORDER BY"),
                    opt("LIMIT"),
                    opt("WHERE", correct=True),
                    opt("DISTINCT"),
                ),
                "WHERE filters rows; ORDER BY sorts and LIMIT caps the number of results.",
            ),
            q(
                "How do you correctly test for a missing value in SQL?",
                (
                    opt("WHERE city = NULL"),
                    opt("WHERE city IS NULL", correct=True),
                    opt("WHERE city == NULL"),
                    opt("WHERE city LIKE NULL"),
                ),
                "You must use IS NULL rather than = NULL to test for a missing value.",
            ),
            q(
                "In a LIKE pattern such as 'A%', what does the % represent?",
                (
                    opt("A single required character"),
                    opt("A literal percent sign in the data"),
                    opt("The wildcard matching any sequence of characters", correct=True),
                    opt("A range between two values"),
                ),
                "In LIKE, % is the wildcard, so 'A%' matches any name starting with A.",
            ),
        ),
        "Changing data & creating tables": (
            q(
                "Which statement adds a new row to a table?",
                (
                    opt("INSERT INTO", correct=True),
                    opt("CREATE TABLE"),
                    opt("UPDATE"),
                    opt("SELECT"),
                ),
                "INSERT INTO ... VALUES adds a new row to a table.",
            ),
            q(
                "Why should you always include a WHERE clause on UPDATE or DELETE?",
                (
                    opt("Otherwise the statement is rejected as a syntax error"),
                    opt(
                        "Without it the statement changes or deletes every row in the table",
                        correct=True,
                    ),
                    opt("WHERE is required to make the change permanent"),
                    opt("It is the only way to sort the affected rows"),
                ),
                "Without a WHERE clause, UPDATE and DELETE affect every row, the most common beginner accident.",
            ),
            q(
                "Which constraint links one table to another?",
                (
                    opt("NOT NULL"),
                    opt("UNIQUE"),
                    opt("DEFAULT"),
                    opt("FOREIGN KEY", correct=True),
                ),
                "A FOREIGN KEY links tables together, while NOT NULL, UNIQUE, and DEFAULT just constrain a single column.",
            ),
        ),
    },
    final=(
        q(
            "What does SQL stand for?",
            (
                opt("Sequential Query Logic"),
                opt("Structured Query Language", correct=True),
                opt("Standard Relational Query"),
                opt("Simple Query Layer"),
            ),
            "SQL stands for Structured Query Language, used to talk to relational databases.",
        ),
        q(
            "Which keyword caps the number of rows a query returns?",
            (
                opt("LIMIT", correct=True),
                opt("DISTINCT"),
                opt("BETWEEN"),
                opt("WHERE"),
            ),
            "LIMIT caps the results, after filtering with WHERE and sorting with ORDER BY.",
        ),
        q(
            "Which statement removes rows from an existing table?",
            (
                opt("DROP COLUMN"),
                opt("DELETE FROM", correct=True),
                opt("INSERT INTO"),
                opt("CREATE TABLE"),
            ),
            "DELETE FROM removes rows, and should include a WHERE to avoid deleting every row.",
        ),
        q(
            "In SQL, how are string literals written?",
            (
                opt("In double quotes"),
                opt("In single quotes", correct=True),
                opt("With no quotes at all"),
                opt("In backticks"),
            ),
            "Strings go in single quotes, as shown in WHERE city = 'London'.",
        ),
        q(
            "What uniquely identifies each row in a well-designed table?",
            (
                opt("Its position in the file"),
                opt("A primary key, often an id column", correct=True),
                opt("The WHERE clause used to insert it"),
                opt("The DISTINCT keyword"),
            ),
            "Each row should have a unique primary key, often an id column.",
        ),
    ),
)
