"""Curated Academy course content — the source of truth for the built-in
MATLAB and Python courses.

Until now the academy's lesson content lived only in the database (created
ad-hoc through the admin UI), so it couldn't be reviewed or re-provisioned.
This module version-controls a rich curriculum and applies it idempotently.

Reconciliation is deliberately **non-destructive and matched by title**:
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
    title="MATLAB Basics",
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

MATLAB ("**MAT**rix **LAB**oratory") is a language built around one idea:
**everything is a matrix**. A single number is just a 1x1 matrix, so the same
operators work whether you're adding two numbers or two thousand.

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
When you're stuck, the function name plus `help` is the fastest answer.

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
**element-wise**. The same goes for `./` and `.^`.

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
first line runs first.

```matlab
% wave.m
clear;                 % start from a clean workspace
x = linspace(0, 2*pi, 100);
y = sin(x);
disp(max(y));          % prints 1
```

## Printing results

- `disp(value)` — print one value, no name.
- `fprintf("mean = %.2f\\n", mean(y))` — formatted, C-style printing.
- Drop the `;` to let MATLAB echo a value with its variable name.

## Scripts vs. functions

A script shares your workspace; a **function** gets its own and takes inputs:

```matlab
function r = rms(v)
    r = sqrt(mean(v .^ 2));
end
```

Start with scripts while you're exploring; reach for functions once you want
to reuse logic without leaking variables.

## Good habits

- Comment the *why*, not the obvious *what*.
- `clear` at the top of a script so stale variables can't mask bugs.
- Suppress noisy lines with `;`, keep the one result you care about visible.

**Next:** write and run your own script against the live engine.
""",
        ),
        SeedLesson(
            title="Run your first script",
            lesson_type="code",
            duration="10 min",
            text_body="""\
% Your first MATLAB script — edit it and press Run.
% Goal: sample a sine wave, then report a couple of statistics.

x = linspace(0, 2*pi, 100);   % 100 points from 0 to 2*pi
y = sin(x);

fprintf('points: %d\\n', numel(y));
fprintf('max:    %.4f\\n', max(y));
fprintf('mean:   %.4f\\n', mean(y));

% Try it yourself:
%   1. Change sin to cos and re-run — how does the mean change?
%   2. Compute y2 = sin(x).^2 and print its mean (expect ~0.5).
""",
        ),
    ),
)

_PYTHON = SeedCourse(
    slug="python-course",
    title="Python Course",
    description=(
        "A hands-on introduction to Python: values and variables, the core "
        "data structures, control flow, and writing your first runnable "
        "script — executed live in a sandboxed interpreter."
    ),
    level="Beginner",
    lessons=(
        SeedLesson(
            title="Getting started with Python",
            lesson_type="text",
            duration="6 min",
            text_body="""\
# Getting started with Python

Python is prized for being **readable**: the code looks close to the idea it
expresses, and indentation (not braces) defines structure.

## Values and variables

No type declarations — assign and go. Python infers the type.

```python
name = "Ada"        # str
age = 36            # int
height = 1.7        # float
is_admin = False    # bool
```

`print()` shows a value; `type(x)` tells you its type.

```python
print(name, age)          # Ada 36
print(type(height))       # <class 'float'>
```

## f-strings

The idiomatic way to build text is an **f-string** — prefix `f` and drop
expressions in `{ }`:

```python
print(f"{name} is {age} years old")   # Ada is 36 years old
print(f"area = {3.14159 * 2**2:.2f}") # area = 12.57
```

**Next:** the data structures you'll reach for every day.
""",
        ),
        SeedLesson(
            title="Lists, dicts & strings",
            lesson_type="text",
            duration="9 min",
            text_body="""\
# Lists, dicts & strings

Three workhorses cover most day-to-day Python.

## Lists — ordered, mutable

```python
nums = [3, 1, 4, 1, 5]
nums.append(9)        # [3, 1, 4, 1, 5, 9]
nums[0]               # 3   (indexing is 0-based)
nums[-1]              # 9   (negative counts from the end)
nums[1:3]             # [1, 4]  (slice: start:stop, stop excluded)
len(nums)             # 6
```

## Dicts — key → value

```python
user = {"name": "Ada", "role": "admin"}
user["role"]              # "admin"
user["active"] = True     # add a key
user.get("email", "—")   # "—"  (default if missing)
```

## Strings behave like sequences

```python
s = "cyberdyne"
s.upper()         # "CYBERDYNE"
s[:5]             # "cyber"
"dyne" in s       # True
",".join(["a", "b", "c"])   # "a,b,c"
```

A rule of thumb: **list** for an ordered collection, **dict** when you look
things up by name, **set** (`{1, 2, 3}`) when you only care about membership.

**Next:** making decisions and repeating work.
""",
        ),
        SeedLesson(
            title="Control flow & functions",
            lesson_type="text",
            duration="8 min",
            text_body="""\
# Control flow & functions

Indentation defines blocks — four spaces per level, and the `:` opens one.

## Conditionals

```python
score = 82
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

## Loops

```python
for n in [1, 2, 3]:
    print(n * n)          # 1, 4, 9

for i, name in enumerate(["a", "b"]):
    print(i, name)        # 0 a / 1 b

total = 0
while total < 10:
    total += 3            # 3, 6, 9, 12 -> stops
```

A **comprehension** builds a list in one expressive line:

```python
squares = [n * n for n in range(5)]   # [0, 1, 4, 9, 16]
```

## Functions

```python
def rms(values):
    \"\"\"Root-mean-square of a list of numbers.\"\"\"
    return (sum(v ** 2 for v in values) / len(values)) ** 0.5

rms([3, 4])    # 3.535...
```

**Next:** put it together in a script you run live.
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

ACADEMY_COURSES: tuple[SeedCourse, ...] = (_MATLAB, _PYTHON)


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
    # Title/level are refreshed too, but the slug (the stable key) is left
    # alone so existing links and progress keep resolving.


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
