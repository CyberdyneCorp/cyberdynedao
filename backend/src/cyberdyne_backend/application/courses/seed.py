"""Curated Academy course content — the source of truth for the built-in
MATLAB and Python courses.

Until now the academy's lesson content lived only in the database (created
ad-hoc through the admin UI), so it couldn't be reviewed or re-provisioned.
This module version-controls a rich curriculum and applies it idempotently.

Titles are kept in sync with the live courses so reconciliation updates the
existing lessons in place. Reconciliation is non-destructive and matched by
title:
  * a lesson whose title (case-insensitive) already exists and has the same
    type is updated in place — its id is kept, so learner progress and any
    attached quiz survive;
  * a curated lesson with no match is appended;
  * existing lessons the seed doesn't mention (e.g. a hand-authored quiz) are
    left untouched, never deleted or overwritten.

Run it with ``python -m cyberdyne_backend.cli.seed_academy`` (see that module).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from cyberdyne_backend.domain.courses import (
    Course,
    CourseNotFoundError,
    CourseRepository,
    new_course,
    new_lesson,
)


@dataclass(frozen=True, slots=True)
class SeedLesson:
    title: str
    lesson_type: str  # 'text' | 'code' | 'quiz' | …
    text_body: str | None = None
    duration: str | None = None


@dataclass(frozen=True, slots=True)
class SeedCourse:
    slug: str
    title: str
    description: str
    level: str
    lessons: tuple[SeedLesson, ...] = field(default_factory=tuple)


# ── Content ──────────────────────────────────────────────────────────────

_MATLAB = SeedCourse(
    slug="matlab-basics",
    title="Matlab Basics",
    description=(
        "Go from zero to writing and running your own MATLAB scripts: the "
        "workspace, variables and matrices, element-wise vs. matrix math, and "
        "how a script executes — with code you run live in the browser."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="Welcome to MATLAB",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# Welcome to MATLAB

MATLAB (*Matrix Laboratory*) is a numerical computing language built around
one idea: **everything is a matrix**. A single number is just a 1x1 matrix and
a row vector is 1xN, so the same operators work whether you're adding two
numbers or two thousand.

## Where you type things

- **Command Window** — type an expression, press Enter, see the result now.
- **Editor** — write reusable `.m` script files (you'll do this shortly).
- **Workspace** — every variable you create lives here until you `clear` it.

## Your first expressions

```matlab
2 + 2          % 4
x = 5;         % the ; suppresses output — x is stored silently
y = x .^ 2     % 25  (no semicolon, so MATLAB prints it)
```

A `%` starts a comment. A trailing `;` hides the result but still runs the
line — use it to keep the Command Window tidy.

## Getting help

`help sin` prints quick docs for any function; `doc sin` opens the full page.

**Next:** how MATLAB stores data — variables, vectors, and matrices.
""",
        ),
        SeedLesson(
            title="Variables & Matrices",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Variables & Matrices

You never declare a type in MATLAB — assign a value and the variable exists.

```matlab
name = "Ada";      % a string
n    = 42;         % a number
v    = [1 2 3 4];  % a row vector
```

## Building matrices

Spaces (or commas) separate columns; semicolons separate rows:

```matlab
A = [1 2 3;
     4 5 6];       % a 2x3 matrix
size(A)            % [2 3]
```

Handy generators: `zeros(2,3)`, `ones(3)`, `eye(3)` (identity), and the
**colon operator** for ranges:

```matlab
t = 0:0.5:2        % [0 0.5 1 1.5 2]  — start:step:stop
```

## Indexing (1-based!)

MATLAB indices start at **1**, not 0.

```matlab
v(1)        % first element
A(2, 3)     % row 2, column 3  -> 6
A(:, 2)     % every row of column 2  -> [2; 5]
v(end)      % last element
```

## Element-wise vs. matrix math

This trips up everyone: `*` is **matrix** multiplication, `.*` is
**element-wise**. The same goes for `./` and `.^`, and `'` transposes.

```matlab
[1 2 3] .* [4 5 6]   % [4 10 18]  element-wise
[1 2 3] *  [4;5;6]   % 32         row x column (dot product)
```

**Next:** turning these expressions into a script that runs top to bottom.
""",
        ),
        SeedLesson(
            title="How a MATLAB script runs",
            lesson_type="text",
            duration="7 min",
            text_body="""\
# How a MATLAB script runs

A **script** is a `.m` file of statements that execute **top to bottom**,
sharing the same workspace as the Command Window. There's no `main()` — the
first line runs first, and each line updates the workspace as the interpreter
walks the file:

```mermaid
flowchart TD
  A[Read next line] --> B{Statement type?}
  B -->|Assignment| C[Store variable in workspace]
  B -->|Expression| D[Evaluate and display]
  C --> E[More lines?]
  D --> E
  E -->|Yes| A
  E -->|No| F([Done])
```

## Printing results

- `disp(value)` — print one value, no name.
- `fprintf("mean = %.2f\\n", mean(y))` — formatted, C-style printing.
- Drop the `;` to let MATLAB echo a value with its variable name.

## A small script

```matlab
total = 0;
for k = 1:5
    total = total + k^2;   % 1 + 4 + 9 + 16 + 25
end
fprintf('sum of squares = %d\\n', total)   % 55
```

## Scripts vs. functions

A script shares your workspace; a **function** gets its own and takes inputs:

```matlab
function r = rms(v)
    r = sqrt(mean(v .^ 2));
end
```

> Tip: open the **code** lesson next and run a script yourself.
""",
        ),
        SeedLesson(
            title="Control flow: if, for & while",
            lesson_type="text",
            duration="11 min",
            text_body="""\
# Control flow: if, for & while

Real programs make **decisions** and **repeat** work. MATLAB groups every
block with the keyword `end` (indenting is style, not syntax). Conditions use
`==`, `~=` (not equal), `&&` (and), `||` (or).

## if / elseif / else

Branches are tested top to bottom; the first true one runs.

```matlab
score = 82;
if score >= 90
    grade = 'A';
elseif score >= 80
    grade = 'B';
else
    grade = 'C';
end
disp(grade)   % B
```

```mermaid
flowchart TD
  A{score at least 90} -->|yes| B[grade A]
  A -->|no| C{score at least 80}
  C -->|yes| D[grade B]
  C -->|no| E[grade C]
```

## for — repeat a known number of times

A `for` walks the columns of whatever you give it; `1:5` is just a row vector.

```matlab
total = 0;
for k = 1:5
    total = total + k;     % 1+2+3+4+5
end
fprintf('total = %d\\n', total)   % 15
```

## while — repeat until the condition is false

```matlab
n = 1;
while n < 100
    n = n * 2;   % 1, 2, 4, ... 128 -> stops
end
```

```mermaid
flowchart TD
  S([start]) --> C{condition true}
  C -->|yes| B[run loop body]
  B --> C
  C -->|no| E([exit loop])
```

## break and continue

Inside any loop:

- **`break`** leaves the loop immediately.
- **`continue`** skips the rest of this pass and jumps to the next one.

```matlab
for n = 1:7
    if n == 5
        break;        % stop entirely at 5
    end
    if mod(n, 2) == 0
        continue;     % skip even numbers
    end
    disp(n)           % prints 1, 3
end
```

```mermaid
flowchart TD
  N[next item] --> Q{break?}
  Q -->|yes| X([leave loop])
  Q -->|no| S{continue?}
  S -->|yes| N
  S -->|no| B[run body]
  B --> N
```

> Every `if` / `for` / `while` must be closed with its own `end`.
""",
        ),
        SeedLesson(
            title="Run your first script",
            lesson_type="code",
            duration="10 min",
            text_body="""\
% Your first MATLAB script — edit it and press Run.
% Build a matrix, transpose it, and combine the two.

A = [1 2; 3 4];
B = A';            % transpose
C = A * B;         % matrix multiply

disp('A * A^T =')
disp(C)
fprintf('trace = %d\\n', trace(C))   % sum of the diagonal

% Try it yourself:
%   1. Change A to a 3x3 matrix and re-run.
%   2. Compare C = A * B (matrix) with A .* B (element-wise) — why the error?
""",
        ),
    ),
)

_PYTHON = SeedCourse(
    slug="python-course",
    title="Python Course",
    description=(
        "A hands-on introduction to Python: values and types, how the "
        "interpreter runs your code, and writing your first runnable script — "
        "executed live in a sandboxed interpreter."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="Welcome to Python",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# Welcome to Python

Python is a readable, batteries-included language used for scripting, data,
the web, and AI. Its defining trait: **indentation defines structure** — there
are no curly braces.

## What this course covers

- values, variables and the core types
- how the interpreter turns your file into output
- writing and running your own script
- a quick knowledge check

## Your first lines

```python
print("hello, cyberdyne")
name = "Ada"
print(f"welcome, {name}")     # f-strings drop expressions in { }
```

`print()` shows a value and `type(x)` tells you its type. There's no compile
step you manage by hand — you run the file and see the result.

**Next:** the values and types you'll use everywhere.
""",
        ),
        SeedLesson(
            title="Variables & Types",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Variables & Types

Python is **dynamically typed** — assign a value and the variable exists, no
declaration needed.

```python
name = "Ada"        # str
age = 36            # int
pi = 3.14159        # float
ready = True        # bool
```

Inspect a type with `type(x)`; format text with f-strings:

```python
print(f"{name} is {age}")        # Ada is 36
print(f"pi to 2dp = {pi:.2f}")   # pi to 2dp = 3.14
```

## The everyday collections

```python
nums = [1, 2, 3]            # list — ordered, mutable
nums.append(4)             # [1, 2, 3, 4]
nums[0], nums[-1]          # 1, 4   (0-based; -1 is the last)

user = {"name": "Ada", "role": "admin"}   # dict — key -> value
user["role"]               # "admin"
user.get("email", "—")    # default if the key is missing
```

Rule of thumb: a **list** for an ordered collection, a **dict** when you look
things up by name.

**Next:** how Python actually runs the file you wrote.
""",
        ),
        SeedLesson(
            title="How Python runs your code",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# How Python runs your code

When you run a `.py` file, Python compiles it to **bytecode** and a virtual
machine executes that, line by line, producing your output:

```mermaid
flowchart LR
  S([source.py]) --> C[Compile to bytecode]
  C --> V[Python VM executes]
  V --> O([Output])
```

Statements run top to bottom. Indentation (4 spaces) groups a block:

```python
for n in [1, 2, 3]:
    print(n * n)        # 1, 4, 9

total = 0
for k in range(1, 6):
    total += k          # 1+2+3+4+5
print("total =", total) # total = 15
```

A **comprehension** builds a list in one expressive line:

```python
squares = [k * k for k in range(1, 6)]
print("sum of squares =", sum(squares))   # 55
```

> Tip: open the **code** lesson next and run a script yourself.
""",
        ),
        SeedLesson(
            title="Control flow: if, for & while",
            lesson_type="text",
            duration="11 min",
            text_body="""\
# Control flow: if, for & while

Real programs make **decisions** and **repeat** work. Python uses
**indentation** (4 spaces) to mark a block and a colon `:` to open it.

## if / elif / else

Branches are tested top to bottom; the first true one runs.

```python
score = 82
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print(grade)   # B
```

```mermaid
flowchart TD
  A{score at least 90} -->|yes| B[grade A]
  A -->|no| C{score at least 80}
  C -->|yes| D[grade B]
  C -->|no| E[grade C]
```

## for — repeat over a sequence

```python
for n in [1, 2, 3]:
    print(n * n)        # 1, 4, 9

for i in range(3):       # 0, 1, 2
    print(i)
```

## while — repeat until the condition is false

```python
total = 0
while total < 10:
    total += 3           # 3, 6, 9, 12 -> stops
```

```mermaid
flowchart TD
  S([start]) --> C{condition true}
  C -->|yes| B[run loop body]
  B --> C
  C -->|no| E([exit loop])
```

## break and continue

Inside any loop:

- **`break`** leaves the loop immediately.
- **`continue`** skips the rest of this pass and jumps to the next one.

```python
for n in range(1, 8):
    if n == 5:
        break            # stop entirely at 5
    if n % 2 == 0:
        continue         # skip even numbers
    print(n)             # prints 1, 3
```

```mermaid
flowchart TD
  N[next item] --> Q{break?}
  Q -->|yes| X([leave loop])
  Q -->|no| S{continue?}
  S -->|yes| N
  S -->|no| B[run body]
  B --> N
```

> Reach for **for** when you know what you're iterating over, **while** when
> you loop until something changes.
""",
        ),
        SeedLesson(
            title="Run your first Python script",
            lesson_type="code",
            duration="10 min",
            text_body="""\
# Your first Python script — edit it and press Run.
# Goal: summarise a small dataset of scores.

scores = [88, 72, 95, 64, 80, 91]

print(f"count:   {len(scores)}")
print(f"highest: {max(scores)}")
print(f"lowest:  {min(scores)}")
print(f"average: {sum(scores) / len(scores):.1f}")

# A comprehension to find who passed (>= 70):
passed = [s for s in scores if s >= 70]
print(f"passed:  {len(passed)} of {len(scores)}")

# Try it yourself:
#   1. Add a score of 100 and re-run — watch the average move.
#   2. Print the scores sorted high-to-low: sorted(scores, reverse=True)
""",
        ),
    ),
)

_BLOCKCHAIN = SeedCourse(
    slug="blockchain-basics",
    title="Blockchain Basics",
    description=(
        "Understand blockchains from first principles: the distributed-ledger "
        "idea, hashing and how blocks chain together, Proof-of-Work consensus "
        "(with a miner you run yourself), and how Bitcoin ties it all into "
        "peer-to-peer digital money."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="What is a blockchain?",
            lesson_type="text",
            duration="8 min",
            text_body="""\
# What is a blockchain?

A blockchain is a **distributed ledger** — a database that many computers keep
a copy of, where everyone agrees on the same history without trusting a central
authority. A useful mental model is a very particular database:

- **fast to read**, but **slow to write** — every write needs the network to
  reach *consensus* first;
- **append-only** — you add new records, you don't edit old ones;
- **every write costs money** (a "gas" fee), so you store small things
  (amounts, hashes, short strings), not files.

## The problem it solves: double-spending

Digital money is just data — and data can be copied. What stops Alice paying
the same coin to two people?

```mermaid
flowchart TD
  A[Alice has 1 coin] --> B[pays Bob]
  A --> C[copies it]
  C --> D[pays Carol the same coin]
  B --> G[Double spend!]
  D --> G
  G --> H[Bank: a trusted middleman decides]
  G --> I[Blockchain: shared ledger + consensus]
```

A bank solves this by being a trusted middleman. A blockchain solves it by
making **everyone** hold the ledger and agree, via math, on which transaction
came first — no middleman required.

## A chain of blocks

Transactions are grouped into **blocks**, and each block points back to the one
before it, forming a chain:

```mermaid
flowchart LR
  G([Genesis]) --> B1[Block 1] --> B2[Block 2] --> B3[Block N...]
```

**Next:** the cryptographic glue that makes this chain tamper-evident — hashing.
""",
        ),
        SeedLesson(
            title="Hashing & blocks",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Hashing & blocks

A **hash function** (Bitcoin uses SHA-256) turns any input into a fixed-size
fingerprint. Three properties make it the backbone of a blockchain:

- **deterministic** — same input always gives the same hash;
- **one-way** — you can't reverse the hash back into the input;
- **avalanche** — change one character and the hash looks completely different.

```python
import hashlib
hashlib.sha256(b"hello").hexdigest()   # 2cf24dba5fb0a30e26e83b2ac5b9e29e...
hashlib.sha256(b"hellp").hexdigest()   # 7f1a... totally different
```

## What's in a block

| Field | Purpose |
|-------|---------|
| **Previous hash** | links to the block before it |
| **Transactions** | the data being recorded (a Merkle root, really) |
| **Timestamp** | when it was made |
| **Nonce** | a number miners search for (next lesson) |

Because each block includes the **previous block's hash**, the blocks are
chained — and that makes tampering obvious:

```mermaid
flowchart LR
  B1["Block 1\\nhash: 00a1"] --> B2["Block 2\\nprev: 00a1\\nhash: 00b2"]
  B2 --> B3["Block 3\\nprev: 00b2\\nhash: 00c3"]
```

If someone edits Block 1, its hash changes, so Block 2's "previous hash" no
longer matches — and every block after it breaks. To rewrite history you'd have
to redo **all** the following blocks, which (next lesson) is made deliberately
expensive.

**Next:** how the network agrees on new blocks — Proof of Work.
""",
        ),
        SeedLesson(
            title="Consensus & Proof of Work",
            lesson_type="text",
            duration="10 min",
            text_body="""\
# Consensus & Proof of Work

Only one block can be added at a time, and thousands of nodes must agree on
which. The rule they follow is the **consensus mechanism**. The original one,
used by Bitcoin, is **Proof of Work (PoW)**.

## The mining puzzle

Miners race to find a **nonce** that makes the block's hash fall below a
target — in practice, "start with N zeros". Hashing is unpredictable, so the
only way to find it is to try nonces one by one:

```mermaid
flowchart TD
  T[Take block data + nonce] --> H[Hash it]
  H --> Q{Hash starts with N zeros?}
  Q -->|no| I[nonce = nonce + 1] --> T
  Q -->|yes| B[Broadcast block, claim reward]
```

Finding the nonce is **hard** (lots of guessing), but checking it is **instant**
(one hash). That asymmetry is what secures the chain.

## Why it's secure: the 51% attack

To rewrite history an attacker must out-mine the rest of the network combined —
controlling **>50% of the hash power**. For Bitcoin that's billions in hardware
and energy. Even then they could only double-spend their own coins or censor
transactions; they **cannot** steal others' coins or mint new ones.

## Proof of Work vs Proof of Stake

| | Proof of Work | Proof of Stake |
|---|---|---|
| **Who writes** | first to solve the hash puzzle | a validator chosen by stake |
| **Cost to attack** | 51% of hash power | 51% of staked tokens |
| **Energy** | very high | low |
| **Examples** | Bitcoin, Litecoin | Ethereum, Cardano |

**Next:** run a tiny miner yourself.
""",
        ),
        SeedLesson(
            title="Mine a block (toy example)",
            lesson_type="code",
            duration="10 min",
            text_body="""\
# A toy Proof-of-Work miner. Edit and press Run.
# It searches for a nonce so the block "hash" starts with N zeros —
# exactly what Bitcoin miners do, just with a tiny stand-in hash.

def toy_hash(s):
    # A tiny teaching hash (NOT secure!). Real Bitcoin uses SHA-256.
    h = 2166136261
    for ch in s:
        h = ((h ^ ord(ch)) * 16777619) % (2 ** 32)
    return format(h, "08x")

block = "Alice -> Bob: 1 coin | prev: 0000abc"
zeros = 4                      # the difficulty: more zeros = more work
target = "0" * zeros

nonce = 0
digest = toy_hash(f"{block}{nonce}")
while not digest.startswith(target):
    nonce += 1
    digest = toy_hash(f"{block}{nonce}")

print(f"difficulty: {zeros} leading zeros")
print(f"nonce found: {nonce}")
print(f"block hash:  {digest}")

# Try it yourself:
#   1. Raise zeros to 5 and re-run — notice how much longer it takes.
#   2. Change one character of `block` and watch the nonce change completely.
""",
        ),
        SeedLesson(
            title="Bitcoin",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Bitcoin

Bitcoin (BTC) is the first cryptocurrency, launched in 2009 by the pseudonymous
**Satoshi Nakamoto** as "a peer-to-peer electronic cash system". It was the
first design to solve double-spending without a trusted middleman, by combining
a distributed ledger with Proof of Work.

| Property | Value |
|----------|-------|
| Created | January 2009 |
| Max supply | 21 million (fixed) |
| Block time | ~10 minutes |
| Consensus | Proof of Work (SHA-256) |
| Smallest unit | 1 satoshi = 0.00000001 BTC |

## Why it matters

- **Trust math, not institutions** — rules are enforced by code, not a bank.
- **Fixed supply** — 21M cap creates digital scarcity (no money printing).
- **Permissionless & borderless** — anyone can transact, 24/7, censorship-resistant.

## The UTXO model

Bitcoin doesn't store account balances. Instead your wallet owns **Unspent
Transaction Outputs (UTXOs)** — like physical coins. To spend, you consume
whole UTXOs as inputs and create new ones as outputs (the leftover is your
change; the gap is the miner's fee):

```mermaid
flowchart LR
  UA[UTXO 0.5 BTC] --> TX[Transaction]
  UB[UTXO 0.3 BTC] --> TX
  TX --> O1[0.6 BTC to Dave]
  TX --> O2[0.199 BTC change to Alice]
  TX --> FEE[0.001 BTC fee to miner]
```

## Halving

Every ~4 years (210,000 blocks) the block reward halves — 50 → 25 → ... →
3.125 BTC (2024). This steadily slows new supply until the last bitcoin is
mined around 2140.

> Bitcoin is intentionally simple and conservative. Programmable money — smart
> contracts, DeFi — is where chains like Ethereum and Solana go next.
""",
        ),
        SeedLesson(
            title="Check your knowledge",
            lesson_type="quiz",
            duration="3 min",
        ),
    ),
)

ACADEMY_COURSES: tuple[SeedCourse, ...] = (_MATLAB, _PYTHON, _BLOCKCHAIN)


# ── Apply ────────────────────────────────────────────────────────────────


async def seed_courses(
    repo: CourseRepository,
    *,
    courses: tuple[SeedCourse, ...] = ACADEMY_COURSES,
    now: datetime | None = None,
) -> list[str]:
    """Upsert each curated course and return a human-readable summary per
    course. Idempotent: a second run produces no further changes."""
    summary: list[str] = []
    for spec in courses:
        course, created = await _get_or_create(repo, spec, now=now)
        _apply_metadata(course, spec)
        added, updated = _reconcile_lessons(course, spec, now=now)
        course.publish(now=now)
        await repo.save(course)
        verb = "created" if created else "updated"
        summary.append(
            f"{spec.slug}: {verb} (+{added} lessons, {updated} updated, "
            f"{len(course.lessons)} total)"
        )
    return summary


async def _get_or_create(
    repo: CourseRepository, spec: SeedCourse, *, now: datetime | None
) -> tuple[Course, bool]:
    try:
        return await repo.get_by_slug(spec.slug, include_drafts=True), False
    except CourseNotFoundError:
        course = new_course(
            title=spec.title,
            description=spec.description,
            level=spec.level,
            slug=spec.slug,
            now=now,
        )
        return course, True


def _apply_metadata(course: Course, spec: SeedCourse) -> None:
    course.description = spec.description
    # The slug (the stable key) is left alone so existing links and progress
    # keep resolving.


def _reconcile_lessons(
    course: Course, spec: SeedCourse, *, now: datetime | None
) -> tuple[int, int]:
    by_title = {lesson.title.casefold(): lesson for lesson in course.lessons}
    added = updated = 0
    for sl in spec.lessons:
        existing = by_title.get(sl.title.casefold())
        if existing is not None and existing.lesson_type.value == sl.lesson_type:
            existing.set_content(text_body=sl.text_body, duration=sl.duration, now=now)
            updated += 1
        elif existing is None:
            course.lessons.append(
                new_lesson(
                    course_id=course.id,
                    title=sl.title,
                    lesson_type=sl.lesson_type,
                    text_body=sl.text_body,
                    duration=sl.duration,
                    sort_order=len(course.lessons),
                    now=now,
                )
            )
            added += 1
        # else: a lesson with this title but a different type exists — leave
        # it untouched rather than clobber hand-authored content.
    return added, updated


__all__ = ["ACADEMY_COURSES", "SeedCourse", "SeedLesson", "seed_courses"]
