from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "PostgreSQL essentials": (
            q(
                "Which shell command connects to and explores a PostgreSQL database?",
                (
                    opt("pgsh"),
                    opt("psql", correct=True),
                    opt("pgcli-only"),
                    opt("postgres-shell"),
                ),
                "The lesson connects and explores with the psql shell.",
            ),
            q(
                "In psql, which meta-command lists the tables?",
                (
                    opt("\\l"),
                    opt("\\d users"),
                    opt("\\dt", correct=True),
                    opt("\\q"),
                ),
                "\\dt lists tables, while \\l lists databases and \\d users describes a table.",
            ),
            q(
                "Which property describes PostgreSQL according to the lesson?",
                (
                    opt("It is a NoSQL document store with no SQL support"),
                    opt("It is fully ACID and standards-compliant", correct=True),
                    opt("It only supports INTEGER and TEXT types"),
                    opt("It cannot be extended with extensions"),
                ),
                "The lesson calls Postgres a standards-compliant, fully ACID database.",
            ),
        ),
        "Beyond standard SQL": (
            q(
                "Which JSONB operator returns a value as text?",
                (
                    opt("->", correct=False),
                    opt("->>", correct=True),
                    opt("#>"),
                    opt("@>"),
                ),
                "The lesson notes that ->> gets text from a JSONB value.",
            ),
            q(
                "What does an INSERT with ON CONFLICT DO UPDATE accomplish?",
                (
                    opt("It deletes conflicting rows"),
                    opt("It performs an upsert, inserting or updating", correct=True),
                    opt("It always raises an error on conflict"),
                    opt("It creates a new table"),
                ),
                "ON CONFLICT DO UPDATE is the upsert pattern that inserts or updates.",
            ),
            q(
                "How do window functions differ from GROUP BY?",
                (
                    opt("They compute across rows without collapsing them", correct=True),
                    opt("They always collapse rows into one"),
                    opt("They cannot use PARTITION BY"),
                    opt("They only work on JSONB columns"),
                ),
                "Window functions compute across rows without collapsing them, unlike GROUP BY.",
            ),
        ),
        "Performance & integrity": (
            q(
                "Which index type powers fast JSONB and array containment queries?",
                (
                    opt("B-tree"),
                    opt("GIN", correct=True),
                    opt("Hash"),
                    opt("BRIN"),
                ),
                "GIN indexes power fast JSONB and array containment queries.",
            ),
            q(
                "What does EXPLAIN ANALYZE show?",
                (
                    opt("It rewrites the query automatically"),
                    opt("How Postgres executes a query and where time goes", correct=True),
                    opt("The list of all databases"),
                    opt("The table schema definition"),
                ),
                "EXPLAIN ANALYZE shows how Postgres executes a query and where the time goes.",
            ),
            q(
                "On a big table, a Seq Scan in the query plan usually indicates what?",
                (
                    opt("The query is optimal"),
                    opt("You need an index", correct=True),
                    opt("The table is corrupted"),
                    opt("A foreign key is missing"),
                ),
                "A Seq Scan on a big table usually means you need an index.",
            ),
        ),
    },
    final=(
        q(
            "Which list correctly contains rich types offered by PostgreSQL?",
            (
                opt("BOOLEAN, TIMESTAMPTZ, UUID, JSONB, arrays", correct=True),
                opt("Only INTEGER and TEXT"),
                opt("VARCHAR and BLOB only"),
                opt("DOCUMENT and COLLECTION"),
            ),
            "The lesson lists BOOLEAN, TIMESTAMPTZ, UUID, NUMERIC, arrays, and JSONB among rich types.",
        ),
        q(
            "What is the purpose of a WITH clause (CTE) in a query?",
            (
                opt("It names a subquery so complex queries read top-to-bottom", correct=True),
                opt("It creates an index automatically"),
                opt("It enforces a foreign key constraint"),
                opt("It converts JSON to text"),
            ),
            "A CTE uses WITH to name a subquery so complex queries read top-to-bottom.",
        ),
        q(
            "Which constraints can the database enforce to keep data consistent?",
            (
                opt("Foreign keys, CHECK, UNIQUE, and NOT NULL", correct=True),
                opt("Only NOT NULL"),
                opt("Only primary keys"),
                opt("No constraints are supported"),
            ),
            "The lesson lists foreign keys, CHECK, UNIQUE, and NOT NULL constraints.",
        ),
        q(
            "Which extensions are cited as adding whole new capabilities to Postgres?",
            (
                opt("pgvector for embeddings and PostGIS for geospatial", correct=True),
                opt("psql and pgcli"),
                opt("B-tree and GIN"),
                opt("BEGIN and COMMIT"),
            ),
            "The essentials lesson cites pgvector (embeddings) and PostGIS (geospatial) as extensions.",
        ),
        q(
            "Wrapping changes in BEGIN and COMMIT does what?",
            (
                opt("Wraps them in a transaction to keep data consistent", correct=True),
                opt("Creates a GIN index"),
                opt("Lists the databases"),
                opt("Performs an upsert"),
            ),
            "Constraints wrapped in transactions (BEGIN/COMMIT) keep data consistent.",
        ),
    ),
)
