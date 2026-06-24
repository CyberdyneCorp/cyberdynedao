"""Academy seed content — the Programming Logic & Computational Thinking track
(Beginner → Advanced).

* ``computational-thinking-basics``        — what logic is, the four pillars,
  the IPO model, variables/types/operators, first runnable programs.
* ``computational-thinking-intermediate``  — conditionals, loops & accumulators,
  lists/vectors/matrices, and organising logic into functions.
* ``computational-thinking-advanced``      — flowcharts & pseudocode, a
  problem-solving methodology, debugging, desk-checking, a worked problem, and
  the road from logic to clean code.

Runnable ``code`` lessons use plain ``assert`` + ``print`` with builtins only
(the sandbox blocks ``input()`` and ``import``). Where we teach ``input()`` it
is shown as read-only ```python; every ``code`` lab assigns literal example
values instead so it runs unattended.
"""
# Lesson content uses arrows/symbols (→, ✓, ✗) in diagrams and prose.
# ruff: noqa: RUF001

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# computational-thinking-basics
# ──────────────────────────────────────────────────────────────────────

_CT_BASICS = SeedCourse(
    slug="computational-thinking-basics",
    title="Programming Logic & Computational Thinking — Basics",
    description=(
        "Learn to turn problems into clear, ordered steps before you touch a "
        "language: what programming logic is, the four pillars of computational "
        "thinking, the input → processing → output model of an algorithm, and "
        "the variables, types and operators you build every program from — then "
        "write and run your first real Python programs."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is programming logic?",
            "9 min",
            r"""# What is programming logic?

**Programming logic** is the skill of organising a solution as a **sequence of
steps a computer can execute**. Before you think about a language, think about
the *reasoning*: which data goes in, what must be computed, and which result
must come out.

A computer executes instructions **exactly as written**, in order — it has no
common sense. So the order of the steps matters enormously, and "almost right"
is wrong.

The vocabulary you'll use throughout this track:

- **Problem** — something to solve, e.g. *compute a car's average fuel use*.
- **Input** — the data you're given, e.g. *distance* and *litres*.
- **Processing** — the formula or decision, e.g. *distance / litres*.
- **Output** — the final answer shown to the user, e.g. *12 km/l*.

Think of a recipe: ingredients (input), the steps (processing), the finished
dish (output). Programming is writing that recipe precisely enough that a
literal-minded machine can follow it.

```mermaid
flowchart LR
  P["Problem: average fuel use"] --> I["Input: distance, litres"]
  I --> PR["Processing: distance / litres"]
  PR --> O["Output: 12 km/l"]
```

**The golden rule:** if you can't explain the solution in simple steps to a
person, you're not ready to write it as code. Logic first, syntax second — that
order is the whole point of this track.
""",
        ),
        _t(
            "The four pillars of computational thinking",
            "10 min",
            r"""# The four pillars of computational thinking

Programming isn't memorising commands — it's a **way of thinking** about
problems. Computer scientists distil it into four pillars. Apply them to *any*
problem, in any language (or none):

- **Decomposition** — break a big, scary problem into small, solvable parts.
  "Build a payroll system" becomes "read hours", "compute gross pay", "apply
  tax", "print payslip". Each part is now approachable on its own.
- **Pattern recognition** — spot what repeats or resembles something you've
  solved before. If three reports all "read a list of numbers and average
  them", that's *one* pattern you can reuse, not three problems.
- **Abstraction** — keep what matters, ignore the rest. A map abstracts a city
  to the roads you need; a function named `average(numbers)` lets you use
  averaging without re-thinking *how* it works.
- **Algorithms** — express the solution as a clear, ordered, finite sequence of
  steps that always terminates with an answer.

```mermaid
mindmap
  root((Computational thinking))
    Decomposition
      Split into parts
      Solve each piece
    Pattern recognition
      Spot what repeats
      Reuse a solution
    Abstraction
      Keep the essentials
      Hide the detail
    Algorithms
      Ordered steps
      Always terminates
```

These four reinforce each other: you **decompose** a problem, **recognise**
familiar pieces, **abstract** away the noise, and write an **algorithm** for
each piece. Master this mental toolkit and a new language is just new
vocabulary for ideas you already have.
""",
        ),
        _t(
            "Algorithms: input → processing → output",
            "9 min",
            r"""# Algorithms: input → processing → output

An **algorithm** is a *finite* sequence of steps that solves a problem. You can
write it in plain language, in pseudocode, as a flowchart, or directly in
Python — the steps are the same; only the notation changes.

Almost every program follows the **IPO** shape: **Input → Processing →
Output**.

```mermaid
flowchart TB
  A["1. Input: data the algorithm receives"] --> B["2. Processing: calculations, decisions, repetitions"]
  B --> C["3. Output: result shown to the user"]
```

**A worked example in plain language — average fuel use**

- **Problem:** find a car's average consumption in km/l.
- **Input:** total distance travelled and litres of fuel used.
- **Processing:** `average = distance / litres`.
- **Output:** show `average` in km/l.

The same steps written in Python (read-along — `input()` is shown here for
realism; you'll run a no-input version in the next lab):

```python
distance = float(input("Distance in km: "))
litres = float(input("Fuel in litres: "))

average = distance / litres

print(f"Average consumption: {average:.2f} km/l")
```

Notice the three blocks line up exactly with IPO. When you face a new problem,
**name the inputs, find the processing formula, and state the output first** —
then writing the code is almost mechanical. That habit is the backbone of every
program in this track.

Many processing formulas are simple and **linear** — the output grows in direct
proportion to the input. For an electricity bill at, say, R$ 2 per kWh, the cost
is just `2 * quantity`, a straight line through the origin:

```plot
{"title": "A linear formula: cost = price per kWh * quantity", "xLabel": "quantity (kWh)", "yLabel": "cost (R$)", "xRange": [0, 200], "yRange": [0, 400], "functions": [{"expr": "2*x", "label": "cost = 2 * kWh", "color": "#2563eb"}]}
```

You'll compute exactly this bill in the Advanced course. Recognising the *shape*
of the processing — linear, stepwise (a decision), repeated (a loop) — is part
of thinking algorithmically before you write a line of code.
""",
        ),
        _code(
            "Variables, types & operators",
            "11 min",
            r"""# A VARIABLE is a name that stores a value in memory. In Python you don't
# declare a type up front — the type is decided by the value you assign.
# The four basic types:
age = 20          # int   — whole numbers, counts
weight = 87.4     # float — numbers with decimals
name = "Ana"      # str   — text (words and sentences)
passed = True     # bool  — True / False

print("age:", age, type(age).__name__)
print("weight:", weight, type(weight).__name__)
print("name:", name, type(name).__name__)
print("passed:", passed, type(passed).__name__)
assert type(age).__name__ == "int"
assert type(weight).__name__ == "float"

# --- Arithmetic operators ---
print("\nArithmetic:")
print("10 + 2  =", 10 + 2)       # add        -> 12
print("10 - 2  =", 10 - 2)       # subtract   -> 8
print("10 * 2  =", 10 * 2)       # multiply   -> 20
print("10 / 4  =", 10 / 4)       # true div   -> 2.5 (always a float)
print("10 // 4 =", 10 // 4)      # floor div  -> 2
print("10 % 4  =", 10 % 4)       # remainder  -> 2
print("2 ** 3  =", 2 ** 3)       # power      -> 8
assert 10 / 4 == 2.5
assert 10 // 4 == 2
assert 10 % 4 == 2
assert 2 ** 3 == 8

# --- Relational operators yield a bool: >  >=  <  <=  ==  != ---
print("\nRelational & logical:")
print("age >= 18           ->", age >= 18)        # True
print("age == 18           ->", age == 18)        # False
print("age != 18           ->", age != 18)        # True

# --- Logical operators combine booleans: and / or / not ---
has_id = True
average = 7.0
print("age >= 18 and has_id->", age >= 18 and has_id)          # True
print("average>=7 or >=6   ->", average >= 7 or average >= 6)  # True
print("not has_id          ->", not has_id)                    # False
assert (age >= 18 and has_id) is True
assert (not has_id) is False

# Two classic traps:
#   '='  ASSIGNS a value, while '=='  COMPARES — never confuse them in an if.
#   '/'  always gives a float (10 / 5 -> 2.0); use '//' for an integer quotient.
print("\n10 / 5 =", 10 / 5, "(a float)  vs  10 // 5 =", 10 // 5, "(an int)")
print("\nAll type/operator checks passed ✓")
""",
        ),
        _code(
            "CODE LAB: your first program (fuel consumption)",
            "10 min",
            r"""# Your first complete program, following Input → Processing → Output.
# In a real program you'd read the inputs from the user. Here we ASSIGN literal
# values so the lab runs without input():
#   distance = float(input("Distance in km: "))   # the real-program version
#   litres   = float(input("Litres used: "))
# Press Run.

# --- 1. Input (literal example values) ---
distance = 300.0   # km
litres = 25.0      # litres

# --- 2. Processing ---
average = distance / litres        # km per litre

# --- 3. Output ---
print("Distance:", distance, "km")
print("Fuel used:", litres, "litres")
print(f"Average consumption: {average:.2f} km/l")

# A desk-check (we'll formalise this later): 300 / 25 = 12, and 180 / 15 = 12.
assert average == 12.0, "300 / 25 should be 12 km/l"

# Try a second car to prove the logic, not just one lucky number:
average2 = 180.0 / 15.0
assert average2 == 12.0
print(f"Second car: {average2:.2f} km/l")

print("Both cars computed correctly ✓")
# Experiment: change distance to 450 and re-run — what consumption do you get?
""",
        ),
        _code(
            "CODE LAB: arithmetic & percentages (10% raise/discount)",
            "11 min",
            r"""# Percentages are just multiplication. To ADD 10% multiply by 1.10; to take
# 10% OFF multiply by 0.90. Why? A percentage is a fraction of 100:
#   10%  = 10 / 100 = 0.10
#   100% + 10% = 1 + 0.10 = 1.10   (a 10% raise)
#   100% - 10% = 1 - 0.10 = 0.90   (a 10% discount)
# In a real program: value = float(input("Enter a value: "))

# --- Input (literal example value) ---
value = 1000.0

# --- Processing ---
raised = value * 1.10        # +10%
discounted = value * 0.90    # -10%

# --- Output ---
print(f"Original value:     {value:.2f}")
print(f"After +10% raise:   {raised:.2f}")
print(f"After -10% discount:{discounted:.2f}")

assert raised == 1100.0      # 1000 * 1.10
assert discounted == 900.0   # 1000 * 0.90

# A general helper for any percentage, using the same idea:
percent = 15.0
factor = 1 + percent / 100        # 1.15 for a 15% raise
print(f"\n{percent:.0f}% raise on 200 ->", round(200 * factor, 2))
assert round(200 * factor, 2) == 230.0

# The other arithmetic operators, for reference:
print("\nfloor division 10 // 4 =", 10 // 4)   # 2
print("remainder    10 %  4 =", 10 % 4)        # 2
print("power        2  ** 3 =", 2 ** 3)        # 8
print("\nAll percentage checks passed ✓")
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# computational-thinking-intermediate
# ──────────────────────────────────────────────────────────────────────

_CT_INTERMEDIATE = SeedCourse(
    slug="computational-thinking-intermediate",
    title="Programming Logic & Computational Thinking — Intermediate",
    description=(
        "Give your programs a brain and stamina: choose between paths with "
        "if / elif / else, repeat work with for and while loops (and avoid the "
        "infinite-loop trap), accumulate results, store many values in lists, "
        "vectors and matrices, and organise your logic into reusable functions."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Conditionals: if / elif / else",
            "10 min",
            r"""# Conditionals: if / elif / else

A **conditional** lets a program choose different paths depending on a
condition. In Python, blocks are defined by **indentation** — the spaces at the
start of a line decide what belongs inside the `if`.

```python
nota = 8.0   # in a real program: float(input("Grade: "))

if nota >= 7:
    print("Pass")
elif nota >= 5:
    print("Retake")
else:
    print("Fail")
```

How it reads:

- **`if`** tests the first condition.
- **`elif`** ("else if") tests another condition *only if* the previous ones
  were false.
- **`else`** runs when none of the conditions above were true.

The branches are checked **top to bottom** and exactly **one** block runs. A
grade of `8.0` matches the first test and prints `Pass`; the `elif`/`else` are
skipped.

```mermaid
flowchart TB
  S["Start"] --> Q1{"nota >= 7?"}
  Q1 -- yes --> P["Pass"]
  Q1 -- no --> Q2{"nota >= 5?"}
  Q2 -- yes --> R["Retake"]
  Q2 -- no --> F["Fail"]
  P --> E["End"]
  R --> E
  F --> E
```

Watch the two classic mistakes: use `==` (not `=`) to compare, and keep your
indentation consistent — Python uses it to know where the block ends, so a
stray space changes the meaning of your program.
""",
        ),
        _code(
            "CODE LAB: a grading decision",
            "10 min",
            r"""# Turn the if / elif / else flowchart into running code. We classify several
# grades to prove every branch works.
# In a real program: grade = float(input("Enter the grade: "))

def classify(grade):                 # one small function; we call it below
    if grade >= 7:
        return "Pass"
    elif grade >= 5:
        return "Retake"
    else:
        return "Fail"

# --- exercise every branch with literal example values ---
cases = [
    (9.0, "Pass"),
    (7.0, "Pass"),      # boundary: >= 7 is a pass
    (6.0, "Retake"),
    (5.0, "Retake"),    # boundary: >= 5 is a retake
    (4.0, "Fail"),
]

for grade, expected in cases:
    result = classify(grade)
    print(f"grade {grade:>4} -> {result}")
    assert result == expected, f"grade {grade} should be {expected}"

print("\nAll branches behaved correctly ✓")
# Boundaries matter: try changing >= 7 to > 7 and see grade 7.0 flip to Retake.
""",
        ),
        _t(
            "Loops: for and while",
            "10 min",
            r"""# Loops: for and while

A **loop** repeats a block of statements many times instead of copying it. The
two you'll use constantly:

**`for`** — when you know *how many* times to repeat (iterate over a range or a
list):

```python
for i in range(1, 6):
    print(i)
# prints 1 2 3 4 5  — range(1, 6) stops BEFORE 6
```

**`while`** — repeat *as long as* a condition stays true:

```python
password = ""
while password != "python":
    password = input("Enter the password: ")   # read-along
print("Access granted")
```

A loop has three moving parts: an **initial value**, a **condition** to keep
going, and an **update** that moves toward the condition becoming false.

```mermaid
flowchart TB
  S["Start"] --> I["i = 1"]
  I --> Q{"i <= 5?"}
  Q -- yes --> B["print i; i = i + 1"]
  B --> Q
  Q -- no --> E["End"]
```

**The infinite-loop trap.** If a `while` condition can *never* become false, the
program never stops:

```python
i = 1
while i <= 5:
    print(i)
    # forgot i = i + 1  → i stays 1 forever → infinite loop!
```

Always make sure something inside the loop moves you toward the exit. A `for`
over a `range` updates the counter for you, which is why it's the safer choice
when the count is known.

A loop that *accumulates* (you'll build one next) makes a value grow with each
pass. Summing `1 + 2 + ... + n` produces the running total `n * (n + 1) / 2` —
notice it curves upward (grows faster than the input) rather than rising in a
straight line:

```plot
{"title": "Cumulative sum 1..n grows as n*(n+1)/2", "xLabel": "n (iterations)", "yLabel": "running total", "xRange": [0, 20], "yRange": [0, 220], "functions": [{"expr": "x*(x+1)/2", "label": "sum 1..n", "color": "#16a34a"}]}
```
""",
        ),
        _code(
            "CODE LAB: loops & accumulators (sum 1..n, list average)",
            "12 min",
            r"""# An ACCUMULATOR is a variable you build up inside a loop: start at a neutral
# value, then update it each pass. The two most common are a running SUM and a
# COUNT (which together give an average).

# --- 1. Sum 1 + 2 + ... + n with a for loop ---
n = 5
total = 0                      # accumulator starts at 0
for i in range(1, n + 1):      # 1, 2, 3, 4, 5
    total = total + i          # add each value
print(f"Sum 1..{n} = {total}")
assert total == 15             # 1+2+3+4+5

# Cross-check with the closed-form formula n*(n+1)//2:
assert total == n * (n + 1) // 2

# --- 2. Average of a list of grades ---
grades = [8.0, 7.5, 9.0, 6.5]
running = 0.0                  # sum accumulator
count = 0                      # count accumulator
for g in grades:
    running = running + g
    count = count + 1
average = running / count
print(f"Grades: {grades}")
print(f"Average = {average:.2f}")
assert count == len(grades)
assert average == sum(grades) / len(grades)   # builtins agree

# --- 3. A while loop with a guard against division by zero ---
values = [10.0, 20.0, 30.0]
acc = 0.0
idx = 0
while idx < len(values):       # condition moves toward false as idx grows
    acc = acc + values[idx]
    idx = idx + 1              # the UPDATE that avoids an infinite loop
print(f"While-sum = {acc}")
assert acc == 60.0
print("\nAll accumulator checks passed ✓")
""",
        ),
        _t(
            "Lists, vectors & matrices",
            "10 min",
            r"""# Lists, vectors & matrices

A **list** stores several values under one name. In algorithmic logic a list
represents a **vector** (a one-dimensional sequence). A **matrix** is a *list of
lists* — rows and columns.

**Vector / list**

```python
grades = [8.0, 7.5, 9.0]
print(grades[0])     # 8.0  — indexing starts at 0
print(len(grades))   # 3    — how many items

for grade in grades: # iterate over every element
    print(grade)
```

Indexing from **0** is the rule almost every language shares: the first item is
`grades[0]`, the last is `grades[len(grades) - 1]`.

**Matrix — a list of lists**

```python
# a 2-row, 3-column matrix
mat = [
    [1, 2, 3],   # row 0
    [4, 5, 6],   # row 1
]
print(mat[1][2])     # 6  — row 1, column 2
```

To visit every cell you use **nested loops** — an outer loop over rows, an inner
loop over columns:

```mermaid
flowchart TB
  S["Start"] --> OR["for i in rows"]
  OR --> IC["for j in columns"]
  IC --> V["visit mat[i][j]"]
  V --> IC
  IC --> OR
  OR --> E["End"]
```

In Python, `range(10)` produces `0, 1, ..., 9`, so two nested `range` loops
walk a 10×20 matrix. Build matrices safely with `.append` rather than assigning
to an index that doesn't exist yet — you'll do exactly that in the functions
lab and the advanced track.
""",
        ),
        _code(
            "CODE LAB: functions — organizing logic",
            "12 min",
            r"""# A FUNCTION is a reusable block of code. It has:
#   def        — the keyword that creates it
#   parameters — values that go in
#   return     — the value it gives back
#   the call   — where we use it
# We define ONE function and call it from module level (the function does not
# call any other user-defined function).

def fuel_report(distance, litres):
    # Return a (consumption, label) pair for a trip. Everything it needs is
    # passed in as an argument — a function can't see module-level variables.
    consumption = distance / litres
    if consumption >= 10:
        label = "efficient"
    else:
        label = "thirsty"
    return consumption, label          # return more than one value as a tuple

# --- call the function with literal example values ---
# In a real program: distance = float(input("km: ")); litres = float(input("L: "))
trips = [
    (300.0, 25.0),   # 12 km/l
    (180.0, 15.0),   # 12 km/l
    (200.0, 25.0),   # 8 km/l
]

for distance, litres in trips:
    consumption, label = fuel_report(distance, litres)
    print(f"{distance:>6} km / {litres:>5} L -> {consumption:5.2f} km/l ({label})")

# Verify the function instead of trusting one run:
c1, l1 = fuel_report(300.0, 25.0)
assert c1 == 12.0 and l1 == "efficient"
c2, l2 = fuel_report(200.0, 25.0)
assert c2 == 8.0 and l2 == "thirsty"

print("\nfuel_report verified on every case ✓")
# Defining the logic ONCE and calling it many times is the whole point of a
# function: less repetition, one place to fix a bug.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# computational-thinking-advanced
# ──────────────────────────────────────────────────────────────────────

_CT_ADVANCED = SeedCourse(
    slug="computational-thinking-advanced",
    title="Programming Logic & Computational Thinking — Advanced",
    description=(
        "Plan and verify before you code: read and draw flowcharts and "
        "pseudocode, follow a repeatable problem-solving methodology, recognise "
        "and debug the most common errors, trace a loop by hand with a "
        "desk-check, solve a full exam-style problem (the kilowatt bill), and "
        "turn working logic into clean, maintainable code."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Flowcharts & pseudocode",
            "10 min",
            r"""# Flowcharts & pseudocode

Before writing code, it helps to sketch the algorithm. Two notations dominate:

**Pseudocode** — structured plain language, no strict syntax:

```
READ salary, kWh
value_kWh = salary / 700
total = value_kWh * kWh
WRITE total
```

**Flowcharts** — a visual map of the steps. The standard symbols:

- **Terminator** (rounded / stadium) — *Start* and *End*.
- **Input/Output** (parallelogram) — read or display data.
- **Process** (rectangle) — a calculation or assignment.
- **Decision** (diamond) — a yes/no question that branches the flow.
- **Arrows** — the order in which steps run.

```mermaid
flowchart TB
  S(["Start / End: terminator"]) --> IO[/"Input / Output: read or show data"/]
  IO --> PR["Process: a calculation"]
  PR --> D{"Decision: x > 0?"}
  D -- yes --> Y["one path"]
  D -- no --> N["another path"]
```

A flowchart and the matching pseudocode describe the *same* algorithm; the
diagram makes the **control flow** (especially branches and loops) obvious at a
glance, while pseudocode is faster to jot down. Use whichever helps you *see*
the steps — the goal is to get the logic right on paper, where mistakes are
cheap to fix, before committing it to code.
""",
        ),
        _t(
            "A problem-solving methodology",
            "10 min",
            r"""# A problem-solving methodology

Good code is born from clear reasoning, not from typing fast. Use this
repeatable five-step recipe on any exam-style or real problem:

1. **Read the statement and underline the inputs.** What data are you given?
   (e.g. *minimum salary*, *kilowatts*, *distance*, *litres*.)
2. **Find the formula or rule.** What turns the inputs into the answer?
   (e.g. `consumption = distance / litres`.)
3. **Define the variables.** Pick clear names for inputs, intermediate values
   and the output (`distance`, `litres`, `consumption`).
4. **Desk-check with simple numbers.** Trace it by hand with easy values
   (300 / 25 = 12) to catch logic errors before any code exists.
5. **Only then, write the code.** With the reasoning settled, coding is almost
   mechanical.

```mermaid
flowchart TB
  A["1. Read & underline inputs"] --> B["2. Find the formula"]
  B --> C["3. Define the variables"]
  C --> D["4. Desk-check with simple numbers"]
  D --> E["5. Write the code"]
```

A handy **universal template** that mirrors the IPO model:

```python
# 1. Input
a = float(input("First value: "))
b = float(input("Second value: "))

# 2. Processing
result = a + b

# 3. Output
print(f"Result: {result:.2f}")
```

Skipping steps 1–4 is the most common reason beginners get stuck: they write
code for a problem they haven't fully understood. Reason first; the keyboard can
wait.
""",
        ),
        _code(
            "Common errors & debugging",
            "10 min",
            r"""# Every programmer makes mistakes — the skill is finding and fixing them
# CALMLY. This lab reproduces the most common beginner errors (safely) and
# shows the fix for each, so the error messages become familiar friends.

# --- Error 1: forgetting to convert input() text to a number ---
# input() always returns a str; "20" + 1 is a TypeError.
age_text = "20"                       # imagine: age_text = input("Age: ")
try:
    broken = age_text + 1             # str + int -> TypeError
except TypeError as e:
    print("Error 1 (no conversion):", type(e).__name__)
age = int(age_text) + 1               # FIX: convert first
print("  fixed ->", age)
assert age == 21

# --- Error 2: '=' (assign) vs '==' (compare) ---
# 'if nota = 10:' is a SyntaxError; the comparison you meant is '=='.
nota = 10
print("Error 2: 'if nota = 10' is a SyntaxError; use 'nota == 10' ->", nota == 10)
assert (nota == 10) is True

# --- Error 3: division by zero ---
total, count = 50.0, 0
try:
    mean = total / count              # ZeroDivisionError
except ZeroDivisionError as e:
    print("Error 3 (divide by zero):", type(e).__name__)
mean = total / count if count > 0 else 0.0   # FIX: guard count > 0
print("  guarded mean ->", mean)
assert mean == 0.0

# --- Error 4: inconsistent names ---
# 'salarioMinimo' then 'salario_minimo' -> NameError. Use ONE name everywhere.
salario_minimo = 1400.0
print("Error 4: pick one name; salario_minimo =", salario_minimo)

# Debugging checklist: read the error TYPE and LINE, print the variables, test
# with small easy numbers, and desk-check before blaming the computer.
print("\nAll error fixes verified ✓")
""",
        ),
        _code(
            "CODE LAB: desk-check a loop (trace variables)",
            "12 min",
            r"""# A DESK-CHECK ("teste de mesa") is simulating a program by hand, tracking how
# each variable changes step by step. Here we make the program PRINT its own
# trace table so you can compare the machine's steps to your pencil-and-paper
# ones for this loop:
#     soma = 0
#     for i in range(1, 4):
#         soma = soma + i
#     print(soma)

print("Tracing:  soma = 0;  for i in range(1, 4): soma = soma + i")
print()
print(f"{'step':>4} | {'i':>2} | {'soma before':>11} | {'calc':>7} | {'soma after':>10}")
print("-" * 48)

soma = 0
step = 0
trace = []                       # remember each row so we can assert on it
for i in range(1, 4):            # i takes 1, 2, 3
    step = step + 1
    before = soma
    soma = soma + i              # the accumulation
    calc = f"{before}+{i}"
    print(f"{step:>4} | {i:>2} | {before:>11} | {calc:>7} | {soma:>10}")
    trace.append((step, i, before, soma))

print("-" * 48)
print(f"Final result: soma = {soma}")

# The desk-check predicted: step1 -> 1, step2 -> 3, step3 -> 6.
assert trace[0] == (1, 1, 0, 1)
assert trace[1] == (2, 2, 1, 3)
assert trace[2] == (3, 3, 3, 6)
assert soma == 6
print("\nMachine trace matches the hand desk-check ✓")
""",
        ),
        _code(
            "CODE LAB: worked problem — the kilowatt bill",
            "13 min",
            r"""# WORKED PROBLEM (exam style):
# "100 kWh cost one seventh of the minimum salary. Given the minimum salary and
#  the kilowatts used, compute the price per kWh, the total, and the total with
#  a 10% discount."
#
# Reasoning (do this BEFORE coding):
#   100 kWh = salary / 7
#   1   kWh = (salary / 7) / 100 = salary / 700
#   total        = price_per_kWh * quantity
#   with_discount = total * 0.90        (a 10% discount)
#
# In a real program:
#   salary    = float(input("Minimum salary: R$ "))
#   kilowatts = float(input("Kilowatts used: "))

# --- 1. Input (literal example values) ---
salary = 1400.0       # makes price_per_kWh exactly 2.00 for an easy check
kilowatts = 150.0

# --- 2. Processing ---
price_per_kwh = salary / 700
total = price_per_kwh * kilowatts
with_discount = total * 0.90

# --- 3. Output ---
print(f"Price per kWh:        R$ {price_per_kwh:.2f}")
print(f"Total:                R$ {total:.2f}")
print(f"Total with 10% off:   R$ {with_discount:.2f}")

# Desk-check: 1400/700 = 2.00; 2.00 * 150 = 300.00; 300 * 0.90 = 270.00
assert price_per_kwh == 2.0
assert total == 300.0
assert with_discount == 270.0

# Confirm the relationship "100 kWh = salary / 7":
assert round(price_per_kwh * 100, 2) == round(salary / 7, 2)

print("\nAll kilowatt-bill checks passed ✓")
""",
        ),
        _t(
            "From logic to clean, maintainable code",
            "10 min",
            r"""# From logic to clean, maintainable code

Working code is the start, not the finish. Code is read far more often than it's
written — by teammates, by future-you, and increasingly by AI agents. Once your
logic is correct, refine it so it stays correct and easy to change.

Principles that turn working logic into *maintainable* code:

- **Clear names.** `consumption` and `price_per_kwh` beat `x` and `c`. A good
  name removes the need for a comment.
- **One job per function.** Small functions with a single responsibility are
  easy to name, test and reuse — exactly the decomposition pillar from the
  Basics course.
- **Don't repeat yourself (DRY).** If you copy-paste logic, extract it into a
  function. One place to read, one place to fix.
- **Avoid deep nesting.** Prefer early returns and guard clauses over pyramids
  of `if` inside `if`. Lower nesting means lower **cognitive complexity** — how
  hard the code is for a human to follow.
- **Comment the *why*, not the *what*.** The code already says what it does;
  comments should explain intent or a non-obvious decision.
- **Validate inputs.** Guard against the division-by-zero and bad-data cases you
  met in the debugging lesson.

```mermaid
flowchart LR
  A["Correct logic"] --> B["Clear names"]
  B --> C["Small functions"]
  C --> D["No repetition (DRY)"]
  D --> E["Shallow nesting"]
  E --> F["Maintainable code"]
```

The journey of this track — decompose, find the pattern, abstract, write the
algorithm, desk-check, then code — naturally produces clean code. Logic and
readability aren't separate skills: clear thinking, written down faithfully, is
clean code.
""",
        ),
    ),
)


COMPUTATIONAL_THINKING_COURSES = (_CT_BASICS, _CT_INTERMEDIATE, _CT_ADVANCED)
