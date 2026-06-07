"""Curated database courses: SQL (basics + intermediate), MongoDB, PostgreSQL.

Grounded in the user's Obsidian `Databases` vault. Lessons are `text` with
syntax-highlighted code fences (sql / javascript / json) — there's no live
database to run against in the Academy, so queries are illustrative. Each
course ends with a knowledge-check quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="3 min")


# ── SQL ──────────────────────────────────────────────────────────────────────

_SQL_BASICS = SeedCourse(
    slug="sql-basics",
    title="SQL — Basics",
    description=(
        "The language of relational databases: how tables model data, querying with "
        "SELECT, and inserting, updating and deleting rows. The foundation under "
        "PostgreSQL, MySQL, SQLite and more."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Relational databases & SQL",
            "8 min",
            """\
# Relational databases & SQL

A **relational database** stores data in **tables** — rows (records) and
columns (fields), like a strict spreadsheet. **SQL** (Structured Query
Language) is how you talk to it.

```text
users
 id | name | age | city
----+------+-----+--------
  1 | Ada  |  36 | London
  2 | Bob  |  40 | Berlin
```

- A **schema** defines each table's columns and their **types** (`INTEGER`,
  `TEXT`, `DATE`…).
- Each row should have a unique **primary key** (often `id`).
- SQL is **declarative**: you say *what* you want, not *how* to fetch it — the
  database's query planner figures that out.

```sql
SELECT name, city FROM users WHERE age > 30;
```

Keywords are conventionally UPPERCASE; statements end with `;`.

**Next:** querying data with SELECT.
""",
        ),
        _t(
            "Querying with SELECT",
            "9 min",
            """\
# Querying with SELECT

`SELECT` reads rows. The clauses run in a logical order: filter, then sort,
then limit.

```sql
SELECT name, age          -- which columns (* = all)
FROM users                -- which table
WHERE city = 'London'     -- filter rows
ORDER BY age DESC         -- sort
LIMIT 10;                 -- cap the results
```

## Common pieces

```sql
SELECT DISTINCT city FROM users;           -- unique values
SELECT * FROM users WHERE age BETWEEN 30 AND 40;
SELECT * FROM users WHERE name LIKE 'A%';  -- starts with A
SELECT * FROM users WHERE city IN ('London', 'Berlin');
SELECT * FROM users WHERE city IS NULL;    -- use IS NULL, not = NULL
```

Combine conditions with `AND` / `OR`. Strings go in single quotes; `%` is the
wildcard for `LIKE`.

**Next:** changing data and creating tables.
""",
        ),
        _t(
            "Changing data & creating tables",
            "9 min",
            """\
# Changing data & creating tables

## Create a table

```sql
CREATE TABLE users (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age  INTEGER,
    city TEXT
);
```

## Insert, update, delete

```sql
INSERT INTO users (id, name, age, city)
VALUES (1, 'Ada', 36, 'London');

UPDATE users SET age = 37 WHERE id = 1;

DELETE FROM users WHERE id = 1;
```

> **Always include a `WHERE`** on UPDATE/DELETE — without it you change *every*
> row. This is the most common beginner accident.

Constraints keep data valid: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `DEFAULT`,
and `FOREIGN KEY` (next course) which links tables together.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

_SQL_INTERMEDIATE = SeedCourse(
    slug="sql-intermediate",
    title="SQL — Intermediate",
    description=(
        "Combine and summarise data: joins across tables, GROUP BY aggregation, and "
        "subqueries, indexes and transactions."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Joins",
            "10 min",
            """\
# Joins

Real schemas split data across tables and link them with **foreign keys**. A
**join** stitches them back together.

```text
users(id, name)        orders(id, user_id, total)
```

```sql
SELECT u.name, o.total
FROM users AS u
JOIN orders AS o ON o.user_id = u.id;   -- INNER JOIN (matches only)
```

| Join | Returns |
|------|---------|
| `INNER JOIN` | only rows that match in both tables |
| `LEFT JOIN` | all left rows; NULLs where the right has no match |
| `RIGHT JOIN` | all right rows; NULLs on the left |

```sql
-- every user, even those with no orders:
SELECT u.name, o.total
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

Table aliases (`u`, `o`) keep multi-table queries readable.

**Next:** summarising with aggregation.
""",
        ),
        _t(
            "Aggregation & grouping",
            "9 min",
            """\
# Aggregation & grouping

Aggregate functions collapse many rows into one value:

```sql
SELECT COUNT(*), AVG(age), MAX(age), MIN(age), SUM(age)
FROM users;
```

## GROUP BY

`GROUP BY` computes an aggregate **per group**:

```sql
SELECT city, COUNT(*) AS people, AVG(age) AS avg_age
FROM users
GROUP BY city;
```

## HAVING vs WHERE

`WHERE` filters rows **before** grouping; `HAVING` filters **groups after**:

```sql
SELECT city, COUNT(*) AS people
FROM users
WHERE age >= 18         -- filter rows first
GROUP BY city
HAVING COUNT(*) > 5;    -- keep only big cities
```

A handy mental order: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`.

**Next:** subqueries, indexes, and transactions.
""",
        ),
        _t(
            "Subqueries, indexes & transactions",
            "10 min",
            """\
# Subqueries, indexes & transactions

## Subqueries

A query inside a query:

```sql
SELECT name FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 100);
```

## Indexes — speed

An **index** is a lookup structure that makes `WHERE`/`JOIN` on a column fast
(at the cost of slightly slower writes):

```sql
CREATE INDEX idx_orders_user ON orders(user_id);
```

Index the columns you filter and join on; don't index everything.

## Transactions — all-or-nothing

Group statements so they succeed or fail together (**ACID**):

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;   -- or ROLLBACK to undo everything
```

If anything fails before `COMMIT`, `ROLLBACK` leaves the data untouched — no
half-finished transfers.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── MongoDB ──────────────────────────────────────────────────────────────────

_MONGODB = SeedCourse(
    slug="mongodb",
    title="MongoDB — Document Databases",
    description=(
        "A hands-on intro to the most popular NoSQL database: the document model, "
        "CRUD with query operators, and the aggregation pipeline plus indexes."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The document model",
            "8 min",
            """\
# The document model

MongoDB is a **NoSQL** database that stores **documents** (JSON-like, stored as
BSON) grouped into **collections** — no fixed schema, so documents in a
collection can differ.

```json
{
  "_id": ObjectId("64a..."),
  "name": "Ada",
  "age": 36,
  "roles": ["admin", "editor"],
  "address": { "city": "London" }
}
```

| Relational | MongoDB |
|------------|---------|
| table | collection |
| row | document |
| column | field |
| JOIN | embed documents (or `$lookup`) |

Documents can **nest** objects and arrays, so related data often lives together
in one document instead of being split across tables. Every document gets a
unique `_id`.

**Next:** creating and querying documents (CRUD).
""",
        ),
        _t(
            "CRUD & query operators",
            "10 min",
            """\
# CRUD & query operators

Using the `mongosh` shell (JavaScript):

```javascript
// Create
db.users.insertOne({ name: "Ada", age: 36, city: "London" });
db.users.insertMany([{ name: "Bob" }, { name: "Cara" }]);

// Read
db.users.find({ city: "London" });
db.users.findOne({ name: "Ada" });

// Update
db.users.updateOne({ name: "Ada" }, { $set: { age: 37 } });

// Delete
db.users.deleteOne({ name: "Bob" });
```

## Query operators

Filters use `$`-prefixed operators:

```javascript
db.users.find({ age: { $gt: 30 } });             // greater than
db.users.find({ city: { $in: ["London", "Berlin"] } });
db.users.find({ age: { $gte: 18, $lt: 65 } });   // combine
db.users.find({ "address.city": "London" });     // nested field
```

`$gt/$gte/$lt/$lte`, `$in`, `$ne`, `$exists`, `$and/$or` cover most queries.

**Next:** aggregation and indexes.
""",
        ),
        _t(
            "Aggregation & indexes",
            "9 min",
            """\
# Aggregation & indexes

## The aggregation pipeline

Documents flow through **stages**, each transforming the stream — like Unix
pipes. It's how you do grouping and analytics:

```javascript
db.orders.aggregate([
  { $match: { status: "paid" } },                 // filter
  { $group: { _id: "$userId", total: { $sum: "$amount" } } },  // group + sum
  { $sort: { total: -1 } },                       // sort desc
  { $limit: 10 }
]);
```

Common stages: `$match`, `$group`, `$sort`, `$project` (reshape), `$lookup`
(join another collection).

## Indexes

Like SQL, indexes make queries fast:

```javascript
db.users.createIndex({ city: 1 });        // 1 = ascending
db.users.createIndex({ email: 1 }, { unique: true });
```

Without an index, a query scans every document; with one, MongoDB jumps
straight to matches. Index the fields you filter and sort on.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── PostgreSQL ───────────────────────────────────────────────────────────────

_POSTGRESQL = SeedCourse(
    slug="postgresql",
    title="PostgreSQL — Beyond SQL",
    description=(
        "The advanced open-source relational database: psql and rich types, then "
        "Postgres superpowers — JSONB, upserts, CTEs and window functions — plus "
        "indexing and integrity. Assumes you know basic SQL."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "PostgreSQL essentials",
            "9 min",
            """\
# PostgreSQL essentials

**PostgreSQL** ("Postgres") is a powerful, standards-compliant, fully
**ACID** open-source database. It speaks standard SQL and adds a lot on top.

Connect and explore with the `psql` shell:

```bash
psql postgres://user:pass@localhost:5432/mydb
```

```text
\\l            list databases
\\dt           list tables
\\d users      describe a table
\\q            quit
```

## Rich types

Beyond the usual `INTEGER`/`TEXT`, Postgres has first-class `BOOLEAN`,
`TIMESTAMPTZ`, `UUID`, `NUMERIC`, **arrays**, `JSONB`, and even custom types:

```sql
CREATE TABLE events (
    id      BIGSERIAL PRIMARY KEY,   -- auto-incrementing
    tags    TEXT[],                  -- an array column
    payload JSONB,                   -- binary JSON (next lesson)
    at      TIMESTAMPTZ DEFAULT now()
);
```

It's also **extensible** — extensions like `pgvector` (embeddings) and PostGIS
(geospatial) add whole new capabilities.

**Next:** the features that set Postgres apart.
""",
        ),
        _t(
            "Beyond standard SQL",
            "11 min",
            """\
# Beyond standard SQL

## JSONB

Store and query JSON natively:

```sql
SELECT payload->>'email' AS email      -- ->> gets text
FROM events
WHERE payload->'meta'->>'plan' = 'pro';
```

## Upsert (insert or update)

```sql
INSERT INTO users (id, name) VALUES (1, 'Ada')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```

## CTEs — readable building blocks

`WITH` names a subquery so complex queries read top-to-bottom:

```sql
WITH big_spenders AS (
    SELECT user_id, SUM(total) AS spent
    FROM orders GROUP BY user_id HAVING SUM(total) > 1000
)
SELECT u.name, b.spent FROM big_spenders b JOIN users u ON u.id = b.user_id;
```

## Window functions

Compute across rows **without collapsing** them (unlike GROUP BY):

```sql
SELECT name, city,
       RANK() OVER (PARTITION BY city ORDER BY age DESC) AS rank_in_city
FROM users;
```

**Next:** performance and integrity.
""",
        ),
        _t(
            "Performance & integrity",
            "9 min",
            """\
# Performance & integrity

## Indexes

Postgres offers several index types for different jobs:

```sql
CREATE INDEX idx_users_email ON users(email);          -- B-tree (default)
CREATE INDEX idx_events_payload ON events USING GIN (payload);  -- JSONB/arrays
```

B-tree suits equality/range lookups; **GIN** indexes power fast JSONB and array
containment queries.

## EXPLAIN — see the plan

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.com';
```

`EXPLAIN ANALYZE` shows how Postgres executes a query and where the time goes —
a "Seq Scan" on a big table usually means you need an index.

## Integrity

Let the database enforce correctness:

```sql
ALTER TABLE orders
  ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id);
```

Foreign keys, `CHECK`, `UNIQUE`, and `NOT NULL` constraints — wrapped in
transactions (`BEGIN`/`COMMIT`) — keep your data consistent no matter what the
application does.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)


DATABASE_COURSES: tuple[SeedCourse, ...] = (
    _SQL_BASICS,
    _SQL_INTERMEDIATE,
    _MONGODB,
    _POSTGRESQL,
)

__all__ = ["DATABASE_COURSES"]
