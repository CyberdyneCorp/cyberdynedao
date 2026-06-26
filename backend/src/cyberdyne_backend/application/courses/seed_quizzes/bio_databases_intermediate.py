"""Quiz questions for the Biological Databases & Data Management - Intermediate course."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The relational model for biological data": (
            q(
                "What does a foreign key do in a relational schema?",
                (
                    opt("References a key in another table, encoding a relationship", correct=True),
                    opt("Uniquely identifies a row within its own table"),
                    opt("Stores the row in compressed form"),
                    opt("Indexes the table automatically"),
                ),
                "A foreign key points to a primary key elsewhere, linking the two tables.",
            ),
            q(
                "One gene having many transcripts is an example of which cardinality?",
                (
                    opt("One-to-many (1:N)", correct=True),
                    opt("One-to-one (1:1)"),
                    opt("Many-to-many (N:M)"),
                    opt("Zero-to-zero"),
                ),
                "A single gene relates to multiple transcripts, a 1:N relationship.",
            ),
            q(
                "A protein mapping to many external databases is best modelled with:",
                (
                    opt("a junction table resolving an N:M relationship", correct=True),
                    opt("a single extra column holding a comma list"),
                    opt("duplicating the protein row per database"),
                    opt("no relationship at all"),
                ),
                "Many-to-many links are resolved by a junction/association table.",
            ),
        ),
        "Querying with SQL: SELECT and JOIN": (
            q(
                "An INNER JOIN returns:",
                (
                    opt("only rows with a match on both sides", correct=True),
                    opt("all rows from the left table, matched or not"),
                    opt("all rows from both tables regardless of keys"),
                    opt("only rows with no match"),
                ),
                "INNER JOIN keeps rows that satisfy the join condition in both tables.",
            ),
            q(
                "To list every gene including those with no annotated protein, use:",
                (
                    opt("a LEFT JOIN from gene to protein", correct=True),
                    opt("an INNER JOIN from gene to protein"),
                    opt("a WHERE clause with COUNT"),
                    opt("a GROUP BY on protein"),
                ),
                "A LEFT JOIN keeps all left rows, filling unmatched protein columns with NULL.",
            ),
            q(
                "Which clause restricts which rows a query returns?",
                (
                    opt("WHERE", correct=True),
                    opt("SELECT"),
                    opt("FROM"),
                    opt("ORDER BY"),
                ),
                "WHERE filters rows; SELECT chooses columns and FROM names the source.",
            ),
        ),
        "Aggregation, grouping and set operations": (
            q(
                "What is the difference between WHERE and HAVING?",
                (
                    opt(
                        "WHERE filters rows before grouping; HAVING filters groups after",
                        correct=True,
                    ),
                    opt("They are interchangeable synonyms"),
                    opt("HAVING runs first, then WHERE"),
                    opt("WHERE works only on aggregates"),
                ),
                "HAVING applies to aggregated groups; WHERE applies to individual rows first.",
            ),
            q(
                "Which set operation returns rows present in BOTH query results?",
                (
                    opt("INTERSECT", correct=True),
                    opt("UNION"),
                    opt("EXCEPT"),
                    opt("JOIN"),
                ),
                "INTERSECT yields rows common to both result sets.",
            ),
            q(
                "GROUP BY organism with COUNT(*) computes:",
                (
                    opt("one count per distinct organism", correct=True),
                    opt("a single count over all rows"),
                    opt("the number of columns"),
                    opt("the average protein length"),
                ),
                "GROUP BY partitions rows so each group gets its own aggregate.",
            ),
        ),
        "Indexing and query performance": (
            q(
                "A B-tree index changes a key lookup from O(n) to:",
                (
                    opt("O(log n)", correct=True),
                    opt("O(n^2)"),
                    opt("O(1) always"),
                    opt("O(n log n)"),
                ),
                "A balanced B-tree gives logarithmic lookups versus a linear full scan.",
            ),
            q(
                "Why not just index every column?",
                (
                    opt("Indexes cost storage and slow inserts/updates", correct=True),
                    opt("Indexes corrupt the primary key"),
                    opt("Databases allow only one index"),
                    opt("Indexes make all queries slower"),
                ),
                "Each index must be maintained on writes and consumes space, so index selectively.",
            ),
            q(
                "Which tool shows whether the planner actually uses an index?",
                (
                    opt("EXPLAIN / EXPLAIN ANALYZE", correct=True),
                    opt("GROUP BY"),
                    opt("UNION"),
                    opt("a FASTA header"),
                ),
                "EXPLAIN reveals the chosen plan, e.g. index scan versus sequential scan.",
            ),
        ),
        "Normalisation and schema design": (
            q(
                "Normalisation primarily reduces:",
                (
                    opt("redundancy and the update anomalies it causes", correct=True),
                    opt("the number of tables to exactly one"),
                    opt("the need for primary keys"),
                    opt("query readability"),
                ),
                "Normal forms remove duplicated data so updates stay consistent.",
            ),
            q(
                "Putting organism taxonomy in its own table referenced by proteins satisfies:",
                (
                    opt("3NF, removing a transitive dependency", correct=True),
                    opt("1NF, ensuring atomic cells"),
                    opt("denormalisation"),
                    opt("a UNION operation"),
                ),
                "Moving transitively dependent attributes to a referenced table reaches 3NF.",
            ),
            q(
                "Why might a read-heavy genome browser deliberately denormalise?",
                (
                    opt("To cut query latency by precomputing joined wide tables", correct=True),
                    opt("To make writes impossible"),
                    opt("To violate all integrity constraints"),
                    opt("Because indexes are forbidden"),
                ),
                "Denormalisation trades controlled redundancy for faster reads.",
            ),
        ),
        "Structure data, mmCIF and ontologies": (
            q(
                "Why did mmCIF/PDBx replace the legacy PDB format?",
                (
                    opt("Fixed-width columns broke for very large complexes", correct=True),
                    opt("mmCIF stores no coordinates"),
                    opt("PDB format was never machine-readable"),
                    opt("mmCIF removes the need for any annotation"),
                ),
                "mmCIF's self-describing categories handle large structures the fixed format could not.",
            ),
            q(
                "The Gene Ontology is organised as:",
                (
                    opt("three hierarchies forming a directed acyclic graph", correct=True),
                    opt("a single flat list of keywords"),
                    opt("a relational primary key"),
                    opt("a FASTA file"),
                ),
                "GO has molecular function, biological process and cellular component as a DAG.",
            ),
            q(
                "For X-ray structures, a lower resolution value means:",
                (
                    opt("more reliable atomic coordinates", correct=True),
                    opt("less reliable coordinates"),
                    opt("a larger file only"),
                    opt("no relationship to quality"),
                ),
                "Lower (better) resolution gives more trustworthy coordinates.",
            ),
        ),
    },
    final=(
        q(
            "In a relational schema, the column that uniquely identifies each row is the:",
            (
                opt("primary key", correct=True),
                opt("foreign key"),
                opt("index"),
                opt("aggregate"),
            ),
            "The primary key uniquely identifies rows; foreign keys reference other tables.",
        ),
        q(
            "Which JOIN preserves unmatched rows from the left table?",
            (
                opt("LEFT JOIN", correct=True),
                opt("INNER JOIN"),
                opt("INTERSECT"),
                opt("GROUP BY"),
            ),
            "A LEFT JOIN keeps every left row, with NULLs where no right match exists.",
        ),
        q(
            "HAVING differs from WHERE because HAVING filters:",
            (
                opt("groups after aggregation", correct=True),
                opt("rows before aggregation"),
                opt("columns in SELECT"),
                opt("the table source"),
            ),
            "HAVING applies predicates to grouped/aggregated results.",
        ),
        q(
            "Adding a B-tree index on a frequently searched accession column:",
            (
                opt("turns full scans into O(log n) lookups", correct=True),
                opt("removes the primary key"),
                opt("forces a sequential scan"),
                opt("compresses the sequence"),
            ),
            "Indexes accelerate lookups on WHERE/JOIN columns at some write cost.",
        ),
        q(
            "Reaching 3NF mainly removes:",
            (
                opt("transitive dependencies", correct=True),
                opt("all foreign keys"),
                opt("the need for SQL"),
                opt("every index"),
            ),
            "3NF eliminates transitive dependencies, e.g. by factoring out taxonomy.",
        ),
        q(
            "What does the Gene Ontology provide that free-text keywords do not?",
            (
                opt(
                    "Structured, machine-readable terms whose annotations propagate up the hierarchy",
                    correct=True,
                ),
                opt("Atomic 3D coordinates"),
                opt("Per-base quality scores"),
                opt("Faster disk compression"),
            ),
            "GO's controlled DAG enables comparable, queryable annotation and enrichment analysis.",
        ),
    ),
)
