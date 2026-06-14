"""Academy seed content — the Data Engineering track (Beginner → Advanced).

* ``dataeng-basics``        — pipelines & ETL, formats & storage, modeling, data quality
* ``dataeng-intermediate``  — batch/MapReduce, warehouses, orchestration, incremental/CDC
* ``dataeng-advanced``      — streaming, exactly-once, the lakehouse, governance, performance

Runnable ``code`` lessons use pandas + Python builtins (the sandbox ships
numpy/pandas), so the labs do real ETL: clean and aggregate a DataFrame, run
data-quality checks, a MapReduce-style word count, a star-schema join + rollup,
an incremental upsert, and a tumbling-window stream aggregation. SQL appears as
read-only illustrative blocks.
"""
# Lesson content uses arrows/symbols (→, ←, ≈, ×) in diagrams and labels.
# ruff: noqa: RUF001, RUF003

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# dataeng-basics
# ──────────────────────────────────────────────────────────────────────

_DE_BASICS = SeedCourse(
    slug="dataeng-basics",
    title="Data Engineering — Basics",
    description=(
        "Move and shape data reliably: what data engineering is, the ETL/ELT "
        "pipeline, file formats and storage (row vs columnar, lake vs "
        "warehouse), dimensional modeling, and data quality. With runnable "
        "pandas labs for a real ETL transform and quality checks."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is data engineering?",
            "10 min",
            r"""# What is data engineering?

**Data engineering** is the discipline of **moving and shaping data** so others
can use it — building the **pipelines** that take raw data from many sources and
deliver clean, reliable, well-structured data to analysts, dashboards, and machine
learning. If data science is cooking, data engineering is the **supply chain,
kitchen, and plumbing** that makes cooking possible.

**Why it exists.** Raw data is messy, scattered, and huge: app databases, event
streams, third-party APIs, log files, spreadsheets — each with different formats,
schemas, and quality. Turning that into something trustworthy and queryable is a
full engineering problem, and most analytics/ML failures trace back to **data**,
not models.

**The data lifecycle** a pipeline manages:

```
Sources → Ingest → Store → Transform → Serve → (Analytics / ML / Dashboards)
            (extract)        (clean, model)     (consume)
```

**Core concepts you'll meet throughout:**

- **Pipeline** — an automated, repeatable flow that moves data through stages.
- **Batch vs streaming** — process data in **scheduled chunks** (e.g. nightly) or
  **continuously** as events arrive. Batch is simpler and cheaper; streaming gives
  freshness. (Both later.)
- **ETL vs ELT** — **E**xtract, **T**ransform, **L**oad — transform *before*
  loading (classic) or *after* loading into a powerful warehouse (**ELT**, the
  modern norm).
- **Idempotency** — re-running a pipeline must not double-count or corrupt data.
  Failures are normal (Distributed Systems track), so reruns must be **safe** —
  the single most important property of a good pipeline.
- **Data warehouse / lake / lakehouse** — where the processed data lives for
  analytics (later lessons).

The data engineer's north star is **reliable, timely, correct data**. The
glamorous part (Spark, streaming, the modern stack) all serves that goal — but the
job is fundamentally about **trustworthy plumbing**: pipelines that run on
schedule, survive failure, and produce data people can stake decisions on. You'll
build real transformations in pandas as you go.
""",
        ),
        _t(
            "Data formats & storage",
            "10 min",
            r"""# Data formats & storage

How you **store** data determines how fast and cheaply you can process it. Two
choices dominate: the **file format** and the **storage layout**.

**Text/row formats** — human-friendly, row-oriented:

- **CSV** — ubiquitous, simple, but untyped, verbose, and fragile (commas in
  values, no schema). Fine for small interchange, poor for scale.
- **JSON / JSONL** — flexible, nested, self-describing; great for APIs and
  semi-structured events, but bulky and slow to scan in bulk.

**Columnar formats** — the workhorses of analytics:

- **Parquet** (and ORC) — store data **by column**, not by row. This is
  transformative for analytics because most queries touch **a few columns over
  many rows**: columnar layout lets you **read only the columns you need**,
  compresses far better (similar values sit together), and supports **predicate
  pushdown** (skip row-groups that can't match). A query summing one column of a
  billion-row table reads a tiny fraction of the bytes a CSV would.

```
Row store (CSV):    [id,name,amount][id,name,amount]...   read everything
Columnar (Parquet): [id,id,...][name,name,...][amount,...] read only 'amount'
```

**Row vs columnar = OLTP vs OLAP.** Row stores suit **transactions** (read/write
whole records — your app database); columnar suits **analytics** (aggregate few
columns over many rows — the warehouse).

**Where the bytes live:**

- **Object storage** (S3, GCS, Azure Blob) — cheap, virtually infinite, durable;
  the foundation of the **data lake** (store raw/processed files as-is).
- **Data warehouse** (Snowflake, BigQuery, Redshift) — managed, columnar, SQL-
  optimised analytics stores.
- **Lakehouse** (Delta/Iceberg/Hudi over object storage) — warehouse-like
  features (transactions, schema) on cheap lake storage (Advanced course).

The practical rule: **use columnar (Parquet) for anything analytical at scale**,
keep raw data cheaply in object storage, and choose formats deliberately — the
right format can make a query 10–100× faster and cheaper before you optimise
anything else.
""",
        ),
        _t(
            "ETL & ELT pipelines",
            "11 min",
            r"""# ETL & ELT pipelines

The heart of data engineering is the pipeline that gets data from source to
usable. Three stages:

- **Extract** — pull data from sources: app databases, APIs, event streams, files.
  Decide **full** vs **incremental** extraction (only what's new — crucial at
  scale), and handle source schemas and rate limits.
- **Transform** — the real work: **clean** (fix nulls, types, duplicates),
  **standardise** (units, formats, time zones), **enrich** (join reference data),
  **aggregate**, and **reshape** into the target model.
- **Load** — write the result to the destination (warehouse, lake, serving DB).

**ETL vs ELT — the order matters:**

- **ETL (Extract → Transform → Load)** — transform **before** loading, often on a
  dedicated processing tier. Classic; good when the destination is limited or you
  must not land raw/sensitive data.
- **ELT (Extract → Load → Transform)** — load **raw** data into a powerful
  warehouse/lake **first**, then transform **inside** it with SQL (e.g. **dbt**).
  The **modern default**, because cloud warehouses are cheap and massively
  parallel, raw data is preserved (re-transform anytime), and analysts can work in
  SQL.

**Properties that separate a toy script from a real pipeline:**

- **Idempotency** — re-running produces the same result, never duplicates. The
  rerun-safety that makes failures survivable (use upserts/overwrite-partition,
  not blind appends).
- **Incrementality** — process only new/changed data using **watermarks** (a
  high-water mark like `updated_at > last_run`) — far cheaper than reprocessing
  everything.
- **Schema handling** — sources change; pipelines must detect/adapt to **schema
  drift** rather than silently break.
- **Observability & data quality** — log row counts, validate outputs, alert on
  anomalies (a pipeline that "succeeds" but writes garbage is worse than one that
  fails loudly).

A useful framing is **medallion layers**: **bronze** (raw, as-ingested) → **silver**
(cleaned, conformed) → **gold** (aggregated, business-ready). Each stage adds
trust. You'll write a real Extract-Transform-Load in pandas next.
""",
        ),
        _code(
            "ETL with pandas",
            "13 min",
            r"""# A real ETL: extract raw records, transform (clean + enrich + derive), and
# 'load' an aggregated result. The sandbox ships pandas. Press Run.

import pandas as pd

# EXTRACT — raw, messy source records (as you'd get from an API/CSV).
raw = [
    {"order_id": 1, "user": "ada",  "country": "us", "amount": "120.50", "status": "paid"},
    {"order_id": 2, "user": "Bob",  "country": "US", "amount": "80",     "status": "paid"},
    {"order_id": 3, "user": "ada",  "country": "uk", "amount": "",       "status": "failed"},
    {"order_id": 4, "user": "cleo", "country": "uk", "amount": "200.00", "status": "paid"},
    {"order_id": 5, "user": "Bob",  "country": "us", "amount": "45.25",  "status": "paid"},
]
df = pd.DataFrame(raw)
print("EXTRACTED:")
print(df)

# TRANSFORM — clean and standardise.
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")   # "" -> NaN
df["user"] = df["user"].str.lower()                            # normalise names
df["country"] = df["country"].str.upper()                      # standardise codes
df = df[df["status"] == "paid"]                                # keep successful orders
df = df.dropna(subset=["amount"])                              # drop unusable rows

print()
print("TRANSFORMED (clean, paid only):")
print(df)

# LOAD — the gold table: revenue per country.
revenue = df.groupby("country")["amount"].sum().reset_index()
revenue = revenue.rename(columns={"amount": "revenue"})
print()
print("LOADED (revenue by country):")
print(revenue)
print("total revenue:", round(df["amount"].sum(), 2))
""",
        ),
        _t(
            "Data modeling & schemas",
            "10 min",
            r"""# Data modeling & schemas

**Data modeling** is designing how data is structured for its purpose. The right
model makes queries fast and intuitive; the wrong one makes everything painful.
The key insight: **transactional** and **analytical** systems want **opposite**
models.

**Normalized (OLTP)** — your app's database. Data is split into many tables with
**no redundancy** (3rd normal form): a customer's address lives in one place, and
orders reference it by id. **Great for writes** (update once, no anomalies) but
analytical queries need many **joins**.

**Dimensional / denormalized (OLAP)** — the warehouse. Optimised for **reads and
aggregation**, accepting redundancy for speed and simplicity. The standard is the
**star schema**:

```
            dim_date
                |
 dim_user --- FACT_orders --- dim_product
                |
           dim_country
```

- **Fact table** — the **measurements/events** at the centre: one row per business
  event (an order), with **numeric measures** (amount, quantity) and **foreign
  keys** to dimensions. Long and narrow; this is where the rows pile up.
- **Dimension tables** — the **descriptive context** you slice/filter by: who
  (user), what (product), when (date), where (country). Short and wide.

Analysts then "slice and dice": *revenue (fact measure) by product category and
month (dimensions)* — a simple star join. (A **snowflake schema** further
normalises dimensions; usually the star's simplicity wins.)

Two more modeling realities:

- **Slowly Changing Dimensions (SCD)** — dimension attributes change (a user moves
  country). **Type 1** overwrites (lose history); **Type 2** adds a new row with
  validity dates (**keep history**) — vital for correct "as-of" reporting.
- **Grain** — define exactly **what one fact row represents** ("one row per order
  line") before anything else; a fuzzy grain corrupts every aggregate built on it.

Model with the **consumer** in mind: normalize for transactional integrity,
**dimensionalise for analytics**. Picking the grain and the star schema well is
what makes a warehouse fast and a joy to query.
""",
        ),
        _t(
            "Data quality & validation",
            "10 min",
            r"""# Data quality & validation

A pipeline that runs perfectly but delivers **wrong data** is worse than one that
fails — because people *trust* it and make bad decisions. **Data quality** is
therefore a first-class concern, not an afterthought. The dimensions to check:

- **Completeness** — are required fields present? How many **nulls**? Did the
  expected **row count** arrive (not 0, not 10× normal)?
- **Uniqueness** — are keys actually unique? Any **duplicate** records (a top cause
  of inflated metrics)?
- **Validity** — do values fit their **type and range** (age 0–120, amount ≥ 0, a
  valid country code, a parseable date)?
- **Consistency** — do related values agree across tables (every order's `user_id`
  exists in users — **referential integrity**)?
- **Timeliness** — is the data **fresh** enough (did today's batch land)?
- **Accuracy** — does it match reality (hardest to check; often via reconciliation
  against a source of truth).

**Where to enforce it:**

- **Schema/contract at ingestion** — reject or quarantine malformed records early;
  **data contracts** make producers responsible for the shape they emit.
- **Tests in the pipeline** — assert expectations on every run (row counts in
  range, no nulls in keys, values in domain). Tools like **Great Expectations**,
  **dbt tests**, and **Soda** codify these as runnable checks.
- **Monitoring & anomaly detection** — track distributions over time and alert when
  they shift (volume spikes, a column's nulls jump).

**Fail loudly, fail early.** A bad batch should **stop the pipeline or quarantine**
the bad rows — never silently propagate downstream where it poisons dashboards and
models and is far harder to trace. Pair this with **idempotent** reruns so you can
fix the source and safely reprocess.

The cultural point: **garbage in, garbage out** governs all analytics and ML.
Investing in automated quality checks is the highest-leverage thing a data team
does — it's the difference between a warehouse people **trust** and one they quietly
work around. You'll write quality checks in pandas next.
""",
        ),
        _code(
            "Data quality checks",
            "12 min",
            r"""# A pipeline must validate its data, not just move it. Run automated quality
# checks over a batch and decide pass/fail. Uses pandas. Press Run.

import pandas as pd

batch = pd.DataFrame({
    "user_id": [1, 2, 2, 4, 5],                 # note the duplicate '2'
    "email":   ["a@x.com", "b@x.com", "b@x.com", "", "e@x.com"],  # one empty
    "age":     [30, 25, 25, 200, 41],           # 200 is out of range
    "country": ["US", "UK", "UK", "US", "ZZ"],
})
print(batch)
print()

valid_countries = ["US", "UK", "BR", "ES", "FR"]
issues = []

# Completeness: no empty emails.
empty_emails = int((batch["email"] == "").sum())
if empty_emails > 0:
    issues.append("completeness: " + str(empty_emails) + " empty email(s)")

# Uniqueness: user_id must be unique.
dupes = int(batch["user_id"].duplicated().sum())
if dupes > 0:
    issues.append("uniqueness: " + str(dupes) + " duplicate user_id(s)")

# Validity: age in [0, 120].
bad_age = int(((batch["age"] < 0) | (batch["age"] > 120)).sum())
if bad_age > 0:
    issues.append("validity: " + str(bad_age) + " age(s) out of range")

# Consistency: country in the allowed set.
bad_country = int((~batch["country"].isin(valid_countries)).sum())
if bad_country > 0:
    issues.append("consistency: " + str(bad_country) + " unknown country code(s)")

print("quality report:")
if issues:
    for i in issues:
        print("  FAIL -", i)
    print("=> BATCH REJECTED (quarantine and alert; do not load downstream)")
else:
    print("  all checks passed -> load")
""",
        ),
        quiz_lesson(
            "Quiz: Data Engineering Basics",
            (
                q(
                    "What is the primary goal of data engineering?",
                    (
                        opt(
                            "Building pipelines that deliver reliable, timely, correct data for analytics and ML",
                            correct=True,
                        ),
                        opt("Designing user interfaces"),
                        opt("Training neural networks"),
                        opt("Writing CSS"),
                    ),
                    "Data engineering is the supply chain/plumbing: trustworthy data delivered on schedule, surviving failure.",
                ),
                q(
                    "Why are columnar formats like Parquet so much faster for analytics than CSV?",
                    (
                        opt(
                            "Queries read only the columns they need, compress better, and can skip non-matching row groups",
                            correct=True,
                        ),
                        opt("They store data as plain text"),
                        opt("They are row-oriented"),
                        opt("They cannot be compressed"),
                    ),
                    "Analytics touch few columns over many rows; columnar layout reads a fraction of the bytes and compresses similar values together.",
                ),
                q(
                    "What is the difference between ETL and ELT?",
                    (
                        opt(
                            "ETL transforms before loading; ELT loads raw data first and transforms inside a powerful warehouse",
                            correct=True,
                        ),
                        opt("ELT never loads data"),
                        opt("ETL has no transform step"),
                        opt("They are identical"),
                    ),
                    "ELT is the modern default: cheap, parallel warehouses transform raw loaded data (e.g. with dbt), preserving the raw source.",
                ),
                q(
                    "Why must a data pipeline be idempotent?",
                    (
                        opt(
                            "So re-running it after a failure produces the same result without duplicating or corrupting data",
                            correct=True,
                        ),
                        opt("To make it run slower"),
                        opt("So it can never be re-run"),
                        opt("To avoid using a warehouse"),
                    ),
                    "Failures are normal; idempotent reruns (upsert/overwrite-partition, not blind append) make recovery safe.",
                ),
                q(
                    "In a star schema, what does the fact table hold?",
                    (
                        opt(
                            "The business events/measurements (numeric measures + foreign keys to dimensions)",
                            correct=True,
                        ),
                        opt("Only descriptive text"),
                        opt("The application's normalized tables"),
                        opt("Nothing — it's empty"),
                    ),
                    "The central fact table records events (orders) with measures and keys; dimensions give the descriptive context to slice by.",
                ),
                q(
                    "A pipeline runs successfully but writes wrong data. Why is that worse than failing?",
                    (
                        opt(
                            "People trust it and make bad decisions; bad data silently poisons downstream dashboards and models",
                            correct=True,
                        ),
                        opt("It uses more CPU"),
                        opt("It is actually better"),
                        opt("Failing is never acceptable"),
                    ),
                    "Garbage in, garbage out — so checks should fail loudly/quarantine bad batches rather than propagate them silently.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# dataeng-intermediate
# ──────────────────────────────────────────────────────────────────────

_DE_INTERMEDIATE = SeedCourse(
    slug="dataeng-intermediate",
    title="Data Engineering — Intermediate",
    description=(
        "Processing data at scale: batch processing and MapReduce/Spark, data "
        "warehouses and dimensional rollups, workflow orchestration (Airflow), "
        "and incremental loads with change data capture — with runnable "
        "MapReduce, star-schema rollup, and incremental-upsert labs."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Batch processing & MapReduce",
            "11 min",
            r"""# Batch processing & MapReduce

When data is too big for one machine, you process it **in parallel across a
cluster**. The idea that started it all is **MapReduce**, and its mental model
still underpins Spark and modern engines.

**MapReduce** splits a computation into two functions you provide, plus a shuffle
the framework runs:

- **Map** — applied to each input record independently, in parallel across the
  cluster, emitting **key → value** pairs.
- **Shuffle** — the framework **groups all values by key** and moves them to the
  right node (the expensive, network-heavy step).
- **Reduce** — combine all values for each key into a result, in parallel per key.

The canonical example — **word count**:

```
Map:    "a b a" -> (a,1)(b,1)(a,1)
Shuffle: group by word -> a:[1,1]  b:[1]
Reduce: sum -> a:2  b:1
```

Because map and reduce are independent per record/key, the framework **scales
horizontally** (add machines) and **tolerates failure** (re-run a failed task's
chunk — idempotency again).

**Apache Spark** is the modern successor and the industry workhorse. Its
advantages over classic Hadoop MapReduce:

- **In-memory** processing (vs writing to disk between steps) → often **10–100×
  faster**.
- A **rich API** beyond map/reduce — `filter`, `join`, `groupBy`, SQL — over
  **DataFrames**.
- **Lazy evaluation** — Spark builds a **DAG** of transformations and optimises the
  whole plan before executing on an **action** (like `count`/`write`).

Key performance concepts you'll hear constantly: **partitions** (the unit of
parallelism — data is split into chunks processed in parallel), and the
**shuffle** (redistributing data across the network for joins/group-bys) — the
**main cost** in big-data jobs, so good engineers **minimise shuffles** and
**data skew** (one key with far more data than others, which stalls on one node).

The throughline: **express work as parallel, independent, idempotent operations
over partitioned data**, and the engine scales it across a cluster. You'll
implement the MapReduce pattern next.
""",
        ),
        _code(
            "MapReduce word count",
            "12 min",
            r"""# The MapReduce pattern — map to key/value pairs, shuffle (group by key),
# reduce — is the foundation of big-data processing. Implement it on a small
# dataset with pure builtins (the same logic Spark runs across a cluster).

documents = [
    "data pipelines move data",
    "pipelines transform data reliably",
    "reliable data builds trust",
]

# MAP: each document -> list of (word, 1), done independently (parallelisable).
mapped = []
for doc in documents:
    for word in doc.split():
        mapped.append((word, 1))
print("map emitted", len(mapped), "pairs")

# SHUFFLE: group values by key.
grouped = {}
for word, count in mapped:
    if word in grouped:
        grouped[word] = grouped[word] + [count]
    else:
        grouped[word] = [count]

# REDUCE: combine each key's values (sum).
reduced = {}
for word in grouped:
    total = 0
    for c in grouped[word]:
        total = total + c
    reduced[word] = total

print("word counts (sorted by count desc):")
items = []
for word in reduced:
    items.append((reduced[word], word))
items.sort(key=lambda pair: (-pair[0], pair[1]))
for count, word in items:
    print("  ", word, "->", count)
# Map and reduce are independent per record/key -> the framework runs them in
# parallel across machines and re-runs only failed chunks.
""",
        ),
        _t(
            "Data warehouses & OLAP",
            "10 min",
            r"""# Data warehouses & OLAP

A **data warehouse** is a database **built for analytics** (OLAP) rather than
transactions (OLTP). It's the central, integrated store where cleaned data from
across the company lands to be queried, sliced, and reported on.

**Why a separate system from the app database?**

- **Different workload.** OLTP handles many tiny read/write transactions (place an
  order); OLAP runs **few, huge, read-only aggregations** (revenue by region by
  quarter over 5 years). One system can't be great at both — and you don't want
  heavy analytics queries slowing your production app.
- **Integration.** It unifies data from many sources into one consistent,
  historical model — a **single source of truth**.

**What makes warehouses fast at analytics:**

- **Columnar storage** (earlier lesson) — read only the columns a query needs.
- **Massively Parallel Processing (MPP)** — distribute a query across many nodes
  that each scan a slice, then combine.
- **Separation of storage and compute** (the cloud breakthrough — Snowflake,
  BigQuery) — scale compute up for a big query and down to nothing when idle, while
  data sits cheaply in object storage. You pay for what you scan/run.

**OLAP vs OLTP at a glance:**

```
OLTP (app DB)      OLAP (warehouse)
row-oriented       columnar
many small txns    few large scans
normalized         dimensional (star)
current state      historical + current
```

**Modern cloud warehouses** — **Snowflake**, **Google BigQuery**, **Amazon
Redshift**, **Databricks SQL** — are managed, elastic, and SQL-first, which is why
**ELT** took over: load raw data in, then transform with SQL/**dbt** inside the
warehouse's power.

The takeaway: the warehouse is the **analytical heart** of a data platform —
columnar + MPP + elastic compute make it possible to ask big questions of huge,
historical, integrated data in seconds. Model it dimensionally (star schema) and
it's both fast and pleasant to query. You'll build a star-schema rollup next.
""",
        ),
        _code(
            "Star-schema join & rollup",
            "13 min",
            r"""# Analytics = join the fact table to dimensions, then aggregate ('roll up').
# Here: orders (fact) joined to product and date dimensions, summarised by
# category and month. Uses pandas.

import pandas as pd

# FACT: one row per order line (measures + foreign keys).
fact = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "product_id": [10, 20, 10, 30, 20, 30],
    "date_id": [1, 1, 2, 2, 2, 3],
    "quantity": [2, 1, 5, 1, 3, 2],
})

# DIMENSIONS: descriptive context.
dim_product = pd.DataFrame({
    "product_id": [10, 20, 30],
    "name": ["Widget", "Gadget", "Gizmo"],
    "category": ["tools", "electronics", "electronics"],
    "price": [9.0, 25.0, 40.0],
})
dim_date = pd.DataFrame({
    "date_id": [1, 2, 3],
    "month": ["2026-01", "2026-01", "2026-02"],
})

# JOIN fact -> dimensions (star join).
star = fact.merge(dim_product, on="product_id").merge(dim_date, on="date_id")
star["revenue"] = star["quantity"] * star["price"]
print("joined star (fact + dims):")
print(star[["order_id", "name", "category", "month", "quantity", "revenue"]])

# ROLL UP: revenue by category and month.
rollup = star.groupby(["month", "category"])["revenue"].sum().reset_index()
print()
print("revenue by month and category:")
print(rollup)
print()
print("revenue by category (all time):")
print(star.groupby("category")["revenue"].sum().reset_index())
""",
        ),
        _t(
            "Workflow orchestration",
            "10 min",
            r"""# Workflow orchestration

A real data platform runs **hundreds of interdependent tasks** on schedules:
extract from a dozen sources, transform in order, run quality checks, refresh
dashboards — where step C must wait for A and B, and a failure in one shouldn't
silently break everything downstream. **Orchestration** manages this.

The core abstraction is the **DAG** (Directed Acyclic Graph): tasks are **nodes**,
dependencies are **edges**, and "acyclic" means no loops — so there's always a
valid order to run them.

```
extract_orders ─┐
                ├─> transform ─> quality_check ─> load_warehouse ─> refresh_dashboard
extract_users ──┘
```

**Apache Airflow** popularised this (define DAGs in Python); **Dagster** and
**Prefect** are modern alternatives, and **dbt** orchestrates SQL transformations
within the warehouse. What an orchestrator gives you:

- **Scheduling** — run on a cron/interval, or trigger on events/data arrival.
- **Dependency management** — run tasks **in the right order**, parallelise the
  independent ones, and **don't start a task until its inputs are ready**.
- **Retries & alerting** — automatically retry transient failures (with backoff),
  and alert when something truly breaks.
- **Backfills** — re-run the pipeline for **past dates** (e.g. after fixing a bug),
  which is why each run is **parameterised by a date/partition**.
- **Observability** — a UI showing what ran, when, how long, and what failed.

Two principles make orchestrated pipelines robust:

- **Idempotent, parameterised tasks** — each task is keyed to a **partition**
  (usually a date) and **overwrites** that partition's output, so retries and
  backfills are safe and never double-count. This is the operational form of the
  idempotency rule from day one.
- **Atomicity** — a task should fully succeed or leave no partial output (write to
  a temp location, then swap), so a failed run never leaves half-written data.

Orchestration is what turns a pile of scripts into a **dependable, observable,
re-runnable platform** — the backbone that lets a data team sleep at night.
""",
        ),
        _t(
            "Incremental loading & CDC",
            "10 min",
            r"""# Incremental loading & CDC

Reprocessing **all** your data every run is simple but quickly becomes impossibly
slow and expensive. **Incremental processing** — handle only what's **new or
changed** since last time — is essential at scale, and getting it right is a core
data-engineering skill.

**Watermark-based incremental loads.** Track a **high-water mark** — the latest
value you've processed of a monotonically increasing column (an `updated_at`
timestamp or an auto-increment id). Each run extracts only rows **beyond** the
mark, then advances it:

```
last run processed up to updated_at = 2026-06-13 02:00
this run: SELECT * FROM orders WHERE updated_at > '2026-06-13 02:00'
then advance the watermark to the new max
```

**Change Data Capture (CDC).** Instead of polling a column, **capture changes
directly from the database's transaction log** (the write-ahead log) — every
insert/update/delete as an event stream (tools: **Debezium**, Kafka Connect). CDC
is lower-latency, catches **deletes** (which a `WHERE updated_at >` query misses),
and avoids hammering the source DB. It's the modern way to keep a warehouse in
near-real-time sync with operational databases.

**The hard parts incremental processing must handle:**

- **Idempotency via upsert/merge** — apply changes with **MERGE** (update if the
  key exists, insert if not), not blind appends, so a re-run doesn't create
  duplicates. (You'll build this next.)
- **Late-arriving data** — events can show up **after** their time window has been
  processed; pipelines need a strategy (reprocess affected partitions, or
  allowed-lateness windows in streaming — Advanced course).
- **Deletes & updates** — appends alone can't reflect changed/removed source rows;
  merge logic or CDC is required for correctness.

The payoff is enormous: incremental + CDC turns a nightly full reload that costs
hours and a fortune into a continuous, cheap, **fresh** flow of just-the-changes.
The trade-off is **complexity** — watermarks, merges, and late data — but it's the
difference between a pipeline that scales and one that grinds to a halt. You'll
implement an idempotent incremental **upsert** next.
""",
        ),
        _code(
            "Incremental upsert (merge)",
            "13 min",
            r"""# Incremental loads must MERGE new/changed rows into existing data by key
# (update if present, insert if new) so re-running never duplicates. Build an
# idempotent upsert with pandas.

import pandas as pd

# The warehouse table as it stands after yesterday's load.
existing = pd.DataFrame({
    "user_id": [1, 2, 3],
    "name": ["ada", "bob", "cleo"],
    "updated_at": ["2026-06-12", "2026-06-12", "2026-06-12"],
})

# A new incremental batch: user 2 changed, user 4 is new (user 1,3 unchanged).
batch = pd.DataFrame({
    "user_id": [2, 4],
    "name": ["robert", "dan"],          # bob -> robert
    "updated_at": ["2026-06-13", "2026-06-13"],
})

key = "user_id"

# Upsert: keep existing rows whose key is NOT in the batch, then append the batch.
keep = existing[~existing[key].isin(batch[key])]
result = pd.concat([keep, batch], ignore_index=True).sort_values(key).reset_index(drop=True)
print("after upsert:")
print(result)

# Idempotency check: applying the SAME batch again changes nothing.
keep_again = result[~result[key].isin(batch[key])]
again = pd.concat([keep_again, batch], ignore_index=True)
print()
print("rows after re-applying the same batch:", len(again), "(unchanged -> idempotent)")
print("user 2 name is now:", result[result["user_id"] == 2]["name"].iloc[0])
""",
        ),
        quiz_lesson(
            "Quiz: Processing at Scale",
            (
                q(
                    "In MapReduce, what does the shuffle step do?",
                    (
                        opt(
                            "Groups all values by key and moves them to the right node (the network-heavy step)",
                            correct=True,
                        ),
                        opt("Encrypts the data"),
                        opt("Deletes duplicate records"),
                        opt("Compiles the code"),
                    ),
                    "Map emits key/value pairs in parallel; shuffle groups by key (expensive, network-bound); reduce combines per key.",
                ),
                q(
                    "Why is Apache Spark typically much faster than classic Hadoop MapReduce?",
                    (
                        opt(
                            "It processes in memory and optimises a lazy DAG of transformations instead of writing to disk between steps",
                            correct=True,
                        ),
                        opt("It uses CSV instead of Parquet"),
                        opt("It runs on a single machine"),
                        opt("It avoids parallelism"),
                    ),
                    "In-memory processing + whole-plan optimisation (lazy DAG, rich API over DataFrames) make Spark 10–100× faster.",
                ),
                q(
                    "Why use a separate data warehouse instead of querying the app's database?",
                    (
                        opt(
                            "OLAP analytics (few huge read-only scans) need a different design than OLTP, and shouldn't slow the production app",
                            correct=True,
                        ),
                        opt("App databases cannot store data"),
                        opt("Warehouses are row-oriented and slower"),
                        opt("There is no real difference"),
                    ),
                    "Warehouses use columnar + MPP + elastic compute for big historical aggregations, isolated from the transactional workload.",
                ),
                q(
                    "What does a DAG represent in workflow orchestration?",
                    (
                        opt(
                            "Tasks as nodes and dependencies as edges, with no cycles — giving a valid execution order",
                            correct=True,
                        ),
                        opt("A type of database index"),
                        opt("A compression format"),
                        opt("A network protocol"),
                    ),
                    "The Directed Acyclic Graph lets the orchestrator run tasks in order, parallelise independent ones, retry, and backfill.",
                ),
                q(
                    "What is a watermark in incremental loading?",
                    (
                        opt(
                            "A high-water mark (e.g. max updated_at) tracking what's been processed, so each run handles only newer rows",
                            correct=True,
                        ),
                        opt("A visible logo on the data"),
                        opt("A type of encryption"),
                        opt("A duplicate record"),
                    ),
                    "Watermarks let a pipeline extract only data beyond the last processed point, avoiding full reprocessing.",
                ),
                q(
                    "Why use MERGE/upsert rather than appending in an incremental pipeline?",
                    (
                        opt(
                            "So updates and re-runs don't create duplicates — it updates existing keys and inserts new ones (idempotent)",
                            correct=True,
                        ),
                        opt("Because appending is impossible"),
                        opt("To make the pipeline non-repeatable"),
                        opt("To avoid using keys"),
                    ),
                    "Upsert keys on the primary key (update if present, insert if new), keeping reruns idempotent and reflecting changes.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# dataeng-advanced
# ──────────────────────────────────────────────────────────────────────

_DE_ADVANCED = SeedCourse(
    slug="dataeng-advanced",
    title="Data Engineering — Advanced",
    description=(
        "Real-time and modern data platforms: stream processing with event-time "
        "windows and watermarks, exactly-once semantics, the lakehouse "
        "(Delta/Iceberg), governance and cost, and performance tuning — with "
        "runnable tumbling-window and sessionization labs."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Stream processing",
            "11 min",
            r"""# Stream processing

Batch processing answers "what happened *yesterday*?" Stream processing answers
"what's happening *now*?" — handling **unbounded** data **continuously**, event by
event, as it arrives. It powers fraud detection, live dashboards, recommendations,
monitoring, and real-time ETL.

The backbone is usually a **distributed log** like **Apache Kafka**: producers
append **events** to **topics** (partitioned, ordered, replayable); consumers read
them at their own pace. Processing engines — **Flink**, **Spark Structured
Streaming**, **Kafka Streams** — run continuous computations over these streams.

**The central complication: two notions of time.**

- **Event time** — when the event **actually happened** (stamped at the source).
- **Processing time** — when your system **gets around to** handling it.

They differ because of network delays, retries, buffering, and offline devices —
so events arrive **late and out of order**. Correct analytics (e.g. "sales per
minute") must use **event time**, not processing time.

**Windows** carve an infinite stream into finite chunks to aggregate:

- **Tumbling** — fixed, non-overlapping (every 1 minute). Each event in exactly
  one window.
- **Sliding** — fixed size, overlapping (last 5 min, updated every minute).
- **Session** — dynamic, grouped by activity with a gap timeout (a user's session
  = events until they're idle for 30 min).

**Watermarks** handle late data: a watermark is the system's assertion "I've
probably now seen all events up to time T," letting it **close** a window and emit
its result — while an **allowed-lateness** policy decides how long to still accept
and incorporate stragglers before discarding them. It's the explicit trade-off
between **latency** (emit results soon) and **completeness** (wait for late
events).

The mindset shift from batch: data is **never complete**, time is **ambiguous**,
and you design around **windows, event-time, and lateness**. You'll implement a
tumbling-window aggregation next.
""",
        ),
        _code(
            "Tumbling-window aggregation",
            "13 min",
            r"""# Stream processing groups unbounded events into finite WINDOWS. Here we
# aggregate a stream of events into fixed 60-second tumbling windows by EVENT
# time (handling out-of-order arrivals). Pure builtins.

# Each event: (event_time_seconds, value). Note they arrive OUT OF ORDER.
events = [
    (5, 10), (42, 5), (8, 7),        # window [0,60)
    (75, 3), (61, 8), (119, 4),      # window [60,120)
    (130, 9), (185, 2), (140, 6),    # windows [120,180) and [180,240)
]

window_size = 60

# Assign each event to its tumbling window by event time, then aggregate.
windows = {}
for event_time, value in events:
    window_start = (event_time // window_size) * window_size      # floor to window
    if window_start in windows:
        windows[window_start] = {
            "count": windows[window_start]["count"] + 1,
            "sum": windows[window_start]["sum"] + value,
        }
    else:
        windows[window_start] = {"count": 1, "sum": value}

print("tumbling 60s windows (by event time, despite out-of-order arrival):")
for start in sorted(windows):
    w = windows[start]
    print("  [", start, ",", start + window_size, ") -> count", w["count"], " sum", w["sum"])
# Bucketing by EVENT time (not arrival order) is what makes the result correct;
# a real engine uses watermarks to decide when each window is safe to emit.
""",
        ),
        _t(
            "Exactly-once & reliability",
            "10 min",
            r"""# Exactly-once & reliability

Streaming pipelines run forever, so failures are **guaranteed** — a node dies
mid-process, a network blips, a job restarts. The question that defines a
pipeline's correctness is its **processing guarantee**:

- **At-most-once** — never reprocess; on failure, events can be **lost**. Fast,
  unacceptable for anything important.
- **At-least-once** — replay on failure so nothing is lost, but events may be
  **processed more than once** → **duplicates** (double-counted revenue, repeated
  side effects). The common baseline.
- **Exactly-once** — each event affects the result **precisely once**, even across
  failures. The gold standard for correctness.

True exactly-once *delivery* is impossible in general (Distributed Systems track),
so engines achieve **exactly-once *processing* semantics** by combining a few
mechanisms:

- **Checkpointing / snapshots** — periodically save the operator state **and** the
  input position (Kafka offset) **atomically**. On restart, restore the snapshot
  and replay from exactly that offset — no gaps, no overlaps. (Flink's distributed
  snapshots, Spark's checkpoints.)
- **Idempotent writes / transactional sinks** — make the output side safe under
  replay: **upsert by key** (last lesson), or use **transactions** so a batch of
  results and its offset commit succeed or fail together (Kafka's transactional
  producer).
- **Deduplication** — drop already-seen events by a unique id within a window.

The recurring tools are the same ones from across this curriculum: **idempotency**
(safe replays), **atomic commits** (state + offset together), and **dedup keys**.
"Exactly-once" is really "**at-least-once delivery + idempotent/transactional
effects**."

The practical advice: decide the guarantee **per pipeline** by what the data is
worth. Counting page views? At-least-once is fine. Moving money or billing? You
need exactly-once — and you pay for it in latency and complexity (checkpoints,
transactions). Knowing **which guarantee you have** — and not assuming a stronger
one than you've actually built — is what separates reliable data platforms from
ones quietly corrupting numbers.
""",
        ),
        _t(
            "The lakehouse & modern data stack",
            "10 min",
            r"""# The lakehouse & modern data stack

For years teams chose between two flawed options: a **data lake** (cheap, flexible
object storage for any data — but no transactions, no schema enforcement, easy to
turn into a "data swamp") or a **data warehouse** (reliable, fast, governed — but
expensive and rigid about data types). The **lakehouse** unifies them.

**Lakehouse = warehouse features on lake storage.** Open **table formats** —
**Delta Lake**, **Apache Iceberg**, **Apache Hudi** — add a transactional metadata
layer on top of plain Parquet files in object storage, giving you:

- **ACID transactions** on the lake — concurrent reads/writes without corruption.
- **Schema enforcement & evolution** — reject bad data; add columns safely.
- **Time travel** — query the table **as of** a past version/timestamp (audit,
  reproducibility, rollback).
- **Upserts/MERGE & deletes** — needed for CDC and GDPR (delete a user) on files
  that were previously append-only.

So you keep the **cheap, open, scalable** storage of a lake **and** the
**reliability** of a warehouse, with one copy of the data serving both BI (SQL) and
ML/Spark.

**The modern data stack** assembles best-of-breed cloud tools around this:

```
Ingest (Fivetran/Airbyte, CDC)  →  Store (lakehouse / warehouse)
   →  Transform (dbt: SQL + tests + lineage)  →  Orchestrate (Airflow/Dagster)
   →  Serve (BI tools, reverse-ETL, ML, semantic layer)
   +  Catalog/quality/observability across it all
```

Defining traits: **ELT** (load raw, transform in-warehouse), **SQL-centric**
transformation with **dbt** (version-controlled, tested, documented models),
**managed/elastic** components, and **modularity** (swap any layer).

The direction of travel is clear: **open formats** (Iceberg/Delta) so data isn't
locked into one vendor, **separation of storage and compute** for elastic cost, and
**one governed copy** of data powering analytics *and* ML. The lakehouse is the
architecture most new platforms now target.
""",
        ),
        _code(
            "Sessionization",
            "12 min",
            r"""# Session windows group a user's events into 'sessions' that end after a gap of
# inactivity (e.g. 30 min) — key for product analytics. Compute sessions from a
# stream of (user, timestamp) events. Pure builtins.

# Events as (user, event_time_seconds). Unsorted, multiple users interleaved.
events = [
    ("ada", 100), ("bob", 105), ("ada", 200), ("ada", 2000),
    ("bob", 300), ("ada", 2100), ("bob", 5000), ("ada", 2300),
]

gap = 1800        # 30 minutes of inactivity ends a session

# Group events per user, then walk each user's sorted timeline splitting on gaps.
by_user = {}
for user, ts in events:
    if user in by_user:
        by_user[user] = by_user[user] + [ts]
    else:
        by_user[user] = [ts]

print("sessions (gap =", gap, "s):")
for user in sorted(by_user):
    times = sorted(by_user[user])
    sessions = []
    start = times[0]
    last = times[0]
    count = 1
    for ts in times[1:]:
        if ts - last > gap:
            sessions.append((start, last, count))     # close current session
            start = ts
            count = 1
        else:
            count = count + 1
        last = ts
    sessions.append((start, last, count))             # close final session
    print(" ", user, "->", len(sessions), "session(s):")
    for s_start, s_end, n in sessions:
        print("      [", s_start, "..", s_end, "]  events:", n, " duration:", s_end - s_start, "s")
""",
        ),
        _t(
            "Governance, privacy & cost",
            "9 min",
            r"""# Governance, privacy & cost

At scale, *running* pipelines is only half the job; **governing** the data — and
its **cost** — is what keeps a platform trustworthy, legal, and affordable.

**Data governance** — making data discoverable, understood, and trusted:

- **Catalog & metadata** — a searchable inventory (tables, owners, descriptions)
  so people can **find** data and know what it means. (DataHub, Amundsen, Unity
  Catalog.)
- **Lineage** — track where each dataset **came from** and what depends on it.
  Essential for **impact analysis** ("if I change this column, what breaks?") and
  debugging bad numbers back to their source.
- **Data contracts** — explicit, enforced agreements on the **schema and
  semantics** a producer guarantees, so upstream changes don't silently break
  downstream consumers.

**Privacy & compliance** — handling personal data responsibly (and legally —
**GDPR, CCPA**):

- **PII** (personally identifiable information) must be identified and protected:
  **masking/tokenization**, **encryption** (at rest and in transit), and **access
  controls** (least privilege — who can see raw vs aggregated data).
- **Right to be deleted** — regulations require deleting a user's data on request,
  which is why **lakehouse delete/MERGE** matters (append-only files couldn't
  comply).
- **Retention & audit** — keep data only as long as needed; log who accessed what.

**Cost** — cloud data systems bill for **storage**, **compute** (per query/scan),
and **data transfer (egress)**, and bills balloon silently:

- **Partition & prune** so queries scan **less** data (the biggest lever —
  columnar + partition pruning + predicate pushdown).
- **Right-size file formats** (Parquet, sensible file sizes — see the small-files
  problem next) and **compress**.
- **Lifecycle storage** — move cold data to cheaper tiers; drop temp/intermediate
  data.
- **Monitor spend** per pipeline/query; a single unpartitioned full-table scan run
  hourly can cost a fortune.

The maturity signal: a great data platform isn't just fast — it's **governed**
(findable, documented, lineage-tracked), **compliant** (PII protected, deletable,
audited), and **cost-aware** (scan less, store smart). These "unglamorous"
concerns are exactly what separate a hobby pipeline from a production data
platform.
""",
        ),
        _t(
            "Performance: partitioning & file layout",
            "10 min",
            r"""# Performance: partitioning & file layout

Most data pipeline performance (and cost) comes down to one principle: **read less
data**. How you lay data out on storage decides how much a query must scan.

**Partitioning** — physically split a table into folders by a column, usually
**date**:

```
/orders/dt=2026-06-12/part-*.parquet
/orders/dt=2026-06-13/part-*.parquet
```

A query for `dt = '2026-06-13'` then reads **only that folder** — **partition
pruning** — instead of the whole table. Choosing the right partition key (commonly
date, sometimes region/tenant) is the highest-impact tuning decision. But **don't
over-partition**: too many tiny partitions create the small-files problem (below).

**File formats & pushdown** (earlier lessons, now as a tuning lever):

- **Columnar (Parquet/ORC)** — read only needed columns.
- **Predicate pushdown** — formats store per-row-group **min/max stats**, so the
  engine **skips** chunks that can't match a filter (e.g. skip a row group whose
  `amount` max < your threshold).
- **Compression** (Snappy/Zstd) — less I/O.

**The small-files problem** — a classic trap. Many tiny files (from
over-partitioning or streaming micro-batches) are **slow**: each file has open/seek
overhead and metadata, so thousands of 10 KB files are far slower to scan than a
few well-sized ones. The fix is **compaction** — periodically rewrite small files
into larger ones (~100 MB–1 GB target). Lakehouse formats automate this
(Delta `OPTIMIZE`, Iceberg compaction).

**Other levers:**

- **Z-ordering / clustering** — co-locate related values so pushdown skips more.
- **Minimise shuffles & skew** (Spark) — the dominant cost in big jobs; pre-
  aggregate, broadcast small dimension tables in joins, salt skewed keys.
- **Cache/materialise** hot intermediate results.

Roughly, scan cost falls inversely with how well you partition — pruning to one of
N partitions reads about 1/N of the data:

```plot
{"title": "Scan cost drops as partition pruning narrows the data read", "xLabel": "number of partitions (pruned to one)", "yLabel": "fraction of data scanned", "xRange": [1, 32], "yRange": [0, 1], "functions": [{"expr": "1 / x", "label": "1 / partitions", "color": "#16a34a"}]}
```

The mantra: **scan less data.** Partition by how you query, store columnar, let
pushdown skip chunks, avoid tiny files, and minimise shuffles — and the same query
runs in seconds for cents instead of minutes for dollars.
""",
        ),
        quiz_lesson(
            "Quiz: Streaming & Modern Platforms",
            (
                q(
                    "Why must stream analytics use event time rather than processing time?",
                    (
                        opt(
                            "Events arrive late and out of order, so only event time gives correct time-based results",
                            correct=True,
                        ),
                        opt("Processing time is always earlier"),
                        opt("Event time is easier to compute"),
                        opt("They are always identical"),
                    ),
                    "Network delays/retries/offline devices make arrival order unreliable; aggregations like 'sales per minute' must key on when events actually happened.",
                ),
                q(
                    "What do watermarks enable in stream processing?",
                    (
                        opt(
                            "Deciding when a window has likely seen all its events so it can be closed/emitted, trading latency vs completeness",
                            correct=True,
                        ),
                        opt("Encrypting the stream"),
                        opt("Removing the need for windows"),
                        opt("Visible logos on dashboards"),
                    ),
                    "A watermark asserts 'seen all events up to T'; allowed-lateness decides how long to still accept stragglers before emitting.",
                ),
                q(
                    "How is exactly-once processing actually achieved?",
                    (
                        opt(
                            "At-least-once delivery plus checkpointing of state+offset and idempotent/transactional writes",
                            correct=True,
                        ),
                        opt(
                            "By guaranteeing each message is delivered exactly once over the network"
                        ),
                        opt("By never retrying"),
                        opt("By disabling checkpoints"),
                    ),
                    "True exactly-once delivery is impossible; engines combine atomic checkpoints (state + offset) with idempotent/transactional sinks.",
                ),
                q(
                    "What does a lakehouse table format (Delta/Iceberg/Hudi) add to a data lake?",
                    (
                        opt(
                            "ACID transactions, schema enforcement/evolution, time travel, and upserts/deletes on cheap object storage",
                            correct=True,
                        ),
                        opt("It removes the ability to use SQL"),
                        opt("It forces row-oriented storage"),
                        opt("It deletes all historical data"),
                    ),
                    "A transactional metadata layer over Parquet gives warehouse-like reliability (ACID, MERGE, time travel) on cheap lake storage.",
                ),
                q(
                    "What is the small-files problem?",
                    (
                        opt(
                            "Many tiny files add per-file overhead and slow scans; the fix is compaction into larger files",
                            correct=True,
                        ),
                        opt("Files that are too large to open"),
                        opt("A security vulnerability"),
                        opt("A type of encryption"),
                    ),
                    "Thousands of tiny files (over-partitioning/streaming) are slow to scan; compact them into ~100MB–1GB files.",
                ),
                q(
                    "What is the highest-impact way to make a large analytical query cheaper?",
                    (
                        opt(
                            "Partition the data so the query prunes to only the partitions it needs (scan less data)",
                            correct=True,
                        ),
                        opt("Convert everything to CSV"),
                        opt("Add more tiny files"),
                        opt("Always scan the full table"),
                    ),
                    "Partition pruning + columnar + predicate pushdown minimise bytes scanned — the dominant driver of speed and cost.",
                ),
            ),
        ),
    ),
)


DATAENG_COURSES = (_DE_BASICS, _DE_INTERMEDIATE, _DE_ADVANCED)
