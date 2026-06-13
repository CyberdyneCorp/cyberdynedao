"""Academy seed content — the Software Testing & QA track (Beginner → Advanced).

* ``testing-basics``        — why test, test types, asserts, coverage
* ``testing-intermediate``  — test doubles, TDD, parameterisation, CI
* ``testing-advanced``      — property-based, mutation, perf, contract, strategy

Runnable ``code`` lessons use plain ``assert`` + builtins/numpy (the sandbox
blocks pytest/unittest), so you write and run real tests; pytest/unittest
syntax is shown as read-only ```python.
"""
# Lesson content uses arrows/symbols (→, ✓, ✗, ²) in diagrams and labels.
# ruff: noqa: RUF001

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
# testing-basics
# ──────────────────────────────────────────────────────────────────────

_TEST_BASICS = SeedCourse(
    slug="testing-basics",
    title="Software Testing & QA — Basics",
    description=(
        "Why automated tests are non-negotiable, the test pyramid (unit / "
        "integration / e2e), how to write clear assertion-based tests with "
        "Arrange-Act-Assert, and what code coverage really tells you (and what "
        "it doesn't)."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why test? The cost of bugs",
            "9 min",
            r"""# Why test? The cost of bugs

Automated tests aren't bureaucracy — they're what lets you **change code without
fear**. They give you:

- **Confidence to refactor** — green tests say "you didn't break anything".
- **Living documentation** — a test shows exactly how code is meant to be used.
- **Faster feedback** — catch a bug in seconds locally, not in a customer
  report.
- **Fewer regressions** — a bug you fix gets a test so it never returns.

The economic argument is stark: **the later a bug is found, the more it costs**
to fix — roughly exponentially. A bug caught while typing is nearly free; the
same bug in production can mean an incident, data loss, and a frantic hotfix:

```plot
{"title": "Cost to fix a bug by the stage it's caught", "xLabel": "stage (design → code → test → release → production)", "yLabel": "relative cost", "xRange": [0, 5], "yRange": [0, 110], "functions": [{"expr": "2^x", "label": "cost ≈ 2^stage", "color": "#dc2626"}]}
```

This is why testing **shifts left** — push detection as early as possible. The
goal isn't 100% bug-free software (impossible); it's a **fast, trustworthy
safety net** that catches the bugs that matter before your users do, and lets
the team move quickly *because* they're confident.
""",
        ),
        _t(
            "Test types & the pyramid",
            "10 min",
            r"""# Test types & the pyramid

Tests come at different scopes, each with a trade-off between **speed/stability**
and **realism**:

- **Unit tests** — one function/class in isolation. Tiny, fast (milliseconds),
  pinpoint failures. The foundation.
- **Integration tests** — several units together (code + database, two
  services). Slower, catch wiring bugs unit tests miss.
- **End-to-end (e2e) tests** — the whole system through its real interface (a
  browser, the API). Most realistic, but slow, brittle, and hard to debug.

The **test pyramid** prescribes the healthy mix:

```
        /\\        e2e         few   (slow, broad)
       /--\\       integration  some
      /----\\      unit         many  (fast, focused)
```

Lots of fast unit tests, fewer integration tests, a thin layer of e2e for
critical user journeys. The **anti-pattern** is the "ice-cream cone" — mostly
slow, flaky e2e tests and few unit tests: a suite that's slow, fragile, and
useless as fast feedback.

Other useful axes: **functional** (does it do the right thing?) vs
**non-functional** (performance, security, usability), and **manual** vs
**automated** (automate everything repeatable; reserve humans for exploratory
testing). Aim your effort at the bottom of the pyramid — that's where you get the
most reliability per second of test time.
""",
        ),
        _code(
            "Write your first tests (asserts)",
            "11 min",
            r"""# A test is just code that checks code. The core tool is `assert`:
# assert <condition>, "message if it fails". Press Run — all should pass.

def is_leap_year(year):
    # Leap if divisible by 4, except centuries unless divisible by 400.
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# --- tests: cover normal cases AND edge cases ---
# (the function under test is passed in as `leap` so each test is self-contained)
def test_typical_leap(leap):
    assert leap(2024) is True
    assert leap(2023) is False

def test_century_rule(leap):
    assert leap(1900) is False    # divisible by 100, not 400
    assert leap(2000) is True     # divisible by 400 -> leap

def test_edges(leap):
    assert leap(0) is True
    assert leap(1) is False

tests = [
    ("typical leap years", test_typical_leap),
    ("century rule", test_century_rule),
    ("edge cases", test_edges),
]
for name, test in tests:
    test(is_leap_year)                     # raises AssertionError if a check fails
    print("PASS", name)                    # reached only if no assert tripped

print("All tests passed ✓")
# Try breaking is_leap_year (e.g. drop the % 400 rule) and re-run — a test fails.
""",
        ),
        _t(
            "Anatomy of a good test: Arrange-Act-Assert",
            "9 min",
            r"""# Anatomy of a good test: Arrange-Act-Assert

A clear test has three visible phases — **AAA**:

```python
def test_cart_total_applies_discount():
    # Arrange — set up inputs and state
    cart = Cart(items=[Item("book", 30), Item("pen", 5)])
    cart.apply_coupon("SAVE10")          # 10% off

    # Act — perform the ONE action under test
    total = cart.total()

    # Assert — check the outcome
    assert total == 31.5
```

What makes tests *good*:

- **One reason to fail.** Test a single behaviour; a failure should point at one
  thing. Multiple unrelated asserts make failures ambiguous.
- **Descriptive names.** `test_cart_total_applies_discount` tells you what broke
  from the report alone.
- **Independent & repeatable.** No test depends on another's order or leftover
  state; same result every run (the **FIRST** principles: Fast, Independent,
  Repeatable, Self-validating, Timely).
- **Deterministic.** No reliance on real time, randomness, or network — control
  those (you'll see how with test doubles in the next course).
- **Test behaviour, not implementation.** Assert *what* the code does, not *how*,
  so refactors don't break tests that should still pass.

Tests are code your team reads constantly — keep them as clean as production
code.
""",
        ),
        _t(
            "Test frameworks: pytest & unittest",
            "9 min",
            r"""# Test frameworks: pytest & unittest

You *can* test with bare `assert` (you just did), but a **framework** finds your
tests, runs them, isolates failures, and reports nicely. In Python the two
standards:

**pytest** — concise, the community favourite. Plain functions + plain `assert`
(it rewrites asserts to show rich failure detail):

```python
# read-along (pytest isn't in the sandbox) — pip install pytest, then `pytest`
import pytest

def test_add():
    assert add(2, 3) == 5

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

@pytest.fixture
def cart():                 # reusable setup, injected into tests
    return Cart()
```

**unittest** — built into the standard library, class-based (xUnit style):

```python
import unittest

class TestMath(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
```

Both give you **fixtures/setup** (shared, isolated setup), **assertions** with
good messages, **test discovery** (auto-find `test_*`), and machine-readable
reports for CI. pytest's brevity and plugin ecosystem make it the usual choice
for new projects; unittest needs no install. Either way the *ideas* are what you
already learned — frameworks just make running them pleasant.
""",
        ),
        _t(
            "Code coverage: useful but not the goal",
            "9 min",
            r"""# Code coverage

**Coverage** measures how much of your code your tests execute — line coverage,
**branch coverage** (were both sides of each `if` taken?), etc. It's a useful
flashlight: it shows you **untested** code.

But coverage is a **necessary, not sufficient** signal:

- **High coverage ≠ good tests.** You can *execute* a line without *asserting*
  anything about it. 100% coverage with weak assertions catches nothing.
- **It can't see missing cases.** Coverage tells you the code you have is run —
  not that you handled the empty list, the negative number, or the timeout you
  never wrote code for.

So returns diminish, and chasing the last few percent often means testing
trivial getters or impossible branches:

```plot
{"title": "Bugs found vs coverage: diminishing returns", "xLabel": "coverage %", "yLabel": "real bugs caught", "xRange": [0, 100], "yRange": [0, 1.05], "functions": [{"expr": "1 - exp(-0.045*x)", "label": "value", "color": "#16a34a"}]}
```

Pragmatic use: set a **floor** (e.g. 80–90%) as a CI gate to stop coverage
*regressing*, focus the effort on **critical paths and edge cases**, and judge
test quality by whether tests actually *fail when you introduce a bug*
(mutation testing, in the Advanced course, measures exactly that). Coverage is a
means, never the goal.
""",
        ),
        quiz_lesson(
            "Quiz: Testing Basics",
            (
                q(
                    "Why does the cost of fixing a bug grow the later it's found?",
                    (
                        opt(
                            "More code/users depend on it, and diagnosis/rework/incident cost compounds",
                            correct=True,
                        ),
                        opt("Older bugs are encrypted"),
                        opt("Compilers slow down over time"),
                        opt("It doesn't — cost is constant"),
                    ),
                    "Late bugs mean incidents, broader impact, and expensive diagnosis — hence 'shift left'.",
                ),
                q(
                    "What does the test pyramid recommend?",
                    (
                        opt("Many fast unit tests, fewer integration, few e2e", correct=True),
                        opt("Mostly slow end-to-end tests"),
                        opt("Equal numbers of every type"),
                        opt("Only manual testing"),
                    ),
                    "A wide base of unit tests with a thin e2e top gives speed and reliability; the inverse is the ice-cream-cone anti-pattern.",
                ),
                q(
                    "What are the three phases of a well-structured test?",
                    (
                        opt("Arrange, Act, Assert", correct=True),
                        opt("Setup, Sleep, Stop"),
                        opt("Build, Run, Deploy"),
                        opt("Mock, Merge, Measure"),
                    ),
                    "AAA: arrange the inputs/state, perform the one action, assert the outcome.",
                ),
                q(
                    "Why should a test have 'one reason to fail'?",
                    (
                        opt("So a failure points clearly at a single behaviour", correct=True),
                        opt("To make tests run faster"),
                        opt("Because frameworks only allow one assert"),
                        opt("To increase coverage"),
                    ),
                    "Testing a single behaviour makes failures unambiguous and easy to diagnose.",
                ),
                q(
                    "Why is 100% code coverage not proof of good tests?",
                    (
                        opt(
                            "Code can be executed without being meaningfully asserted, and missing cases aren't counted",
                            correct=True,
                        ),
                        opt("Coverage tools are always wrong"),
                        opt("100% coverage is impossible"),
                        opt("Coverage measures performance, not correctness"),
                    ),
                    "Coverage shows what ran, not whether you asserted the right things or covered missing scenarios.",
                ),
                q(
                    "What does pytest's `with pytest.raises(...)` check?",
                    (
                        opt("That the enclosed code raises the expected exception", correct=True),
                        opt("That the code runs without any output"),
                        opt("That coverage is above a threshold"),
                        opt("That the test is skipped"),
                    ),
                    "It asserts the expected error is raised — testing failure paths, not just happy paths.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# testing-intermediate
# ──────────────────────────────────────────────────────────────────────

_TEST_INTERMEDIATE = SeedCourse(
    slug="testing-intermediate",
    title="Software Testing & QA — Intermediate",
    description=(
        "Testing real code: isolating dependencies with test doubles, "
        "dependency injection, TDD's red-green-refactor loop, parameterised "
        "tests, integration testing with fixtures, and running it all in CI "
        "(including the scourge of flaky tests)."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Test doubles: stubs, mocks, fakes & spies",
            "10 min",
            r"""# Test doubles

Real dependencies — databases, networks, clocks, payment gateways — make tests
slow, flaky, and hard to control. **Test doubles** stand in for them (like a
stunt double), so a unit test stays fast and deterministic. The family:

- **Dummy** — passed but never used (just fills a parameter).
- **Stub** — returns canned answers ("`get_user()` always returns this fixed
  user"). Controls the *input* to your code.
- **Fake** — a working but lightweight implementation (an in-memory database
  instead of Postgres).
- **Spy** — records how it was called, so you can assert on it afterwards.
- **Mock** — a spy with **pre-set expectations**; the test fails if it isn't
  called as expected.

The distinction that matters: **stubs help you control inputs** (state
verification — "given this data, the output is X"); **mocks/spies verify
interactions** (behaviour verification — "the email service *was called* once
with this address").

Over-mocking is a real trap: if a test mocks everything, it tests your mocks, not
your code, and breaks on every refactor. Rule of thumb: **mock at boundaries**
(I/O, external services, time/randomness) and use **real objects within your own
domain**. You'll build a stub and a spy by hand next, so the magic disappears.
""",
        ),
        _code(
            "Dependency injection + a hand-rolled mock",
            "13 min",
            r"""# 'Mocking' isn't magic — it's just passing a fake that records calls.
# The key enabler is DEPENDENCY INJECTION: place_order receives its 'send'
# function (and where to record calls) instead of hard-coding a real emailer.

def place_order(send, calls, user, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    send(calls, user, "Order confirmed: " + str(amount))   # use the injected sender
    return {"user": user, "amount": amount, "status": "placed"}

# A hand-rolled SPY: records every call instead of sending real email.
def spy_send(calls, to, body):
    calls.append((to, body))

# --- test: verify behaviour without sending real email ---
calls = []
result = place_order(spy_send, calls, "alice", 30)

assert result["status"] == "placed"              # state check
assert len(calls) == 1                             # interaction check
assert calls[0][0] == "alice"
print("order placed; emailer called with:", calls[0])

# Error path: no email should be sent on a bad order.
calls2 = []
try:
    place_order(spy_send, calls2, "bob", -5)
except ValueError:
    pass
assert calls2 == []                                # nothing sent
print("invalid order: emailer NOT called ✓")
""",
        ),
        _t(
            "Test-Driven Development (TDD)",
            "10 min",
            r"""# Test-Driven Development

TDD inverts the usual order: **write the test first**, then the code. The cycle
is **Red → Green → Refactor**:

1. **Red** — write a small failing test for the next bit of behaviour. It fails
   (the code doesn't exist yet) — proving the test actually tests something.
2. **Green** — write the *simplest* code to make it pass. Don't gold-plate; just
   go green.
3. **Refactor** — now that you're safe, clean up the code (and the test) without
   changing behaviour. Tests stay green.

Repeat in tiny loops, minutes each.

Why it works:

- **Design pressure** — writing the test first forces you to think about the
  *interface* and *usage* before the implementation, yielding more usable APIs.
- **Built-in safety net** — you accumulate tests as you go, never "I'll add
  tests later" (you won't).
- **Just-enough code** — you only write code a test demands, curbing
  over-engineering.
- **Tight feedback** — you're never more than a minute from a green bar.

TDD isn't dogma — it shines for logic-heavy code with clear inputs/outputs and
is awkward for exploratory or UI work. But the discipline of "could I write a
test for this?" *before* coding improves design even when you don't follow it
strictly. The habit it builds — small steps, always-runnable code — is the real
prize.
""",
        ),
        _t(
            "Parameterised & data-driven tests",
            "8 min",
            r"""# Parameterised & data-driven tests

Copy-pasting a test five times with different inputs is noise. **Parameterised
tests** run the same logic over a table of cases, so adding a case is one line
and each case reports separately.

```python
# read-along (pytest): one test, many cases
import pytest

@pytest.mark.parametrize("value, expected", [
    (1,     "1"),
    (5,     "Buzz"),       # divisible by 5
    (3,     "Fizz"),       # divisible by 3
    (15,    "FizzBuzz"),   # both
    (0,     "FizzBuzz"),
])
def test_fizzbuzz(value, expected):
    assert fizzbuzz(value) == expected
```

Each row is reported as its own test (`test_fizzbuzz[15-FizzBuzz]`), so a
failure tells you exactly which case broke.

This shines for **boundary and equivalence testing**: pick representative inputs
from each class (negative / zero / positive, empty / one / many, just-below /
at / just-above a limit) rather than thousands of random values. A close cousin
is **table-driven tests** (popular in Go): a slice/array of `{input, expected}`
structs looped over. Same idea — data and logic separated, cases easy to extend.
The Advanced course pushes this further with **property-based testing**, which
*generates* the inputs for you.
""",
        ),
        _code(
            "Build a tiny test runner",
            "12 min",
            r"""# Frameworks like pytest do three things: discover tests, run them isolating
# failures, and report. Here's that core in ~20 lines — no library needed.

# The functions under test:
def add(a, b):
    return a + b

def divide(a, b):
    return a / b

# A collection of named test cases (name, callable):
def t_add_positive():
    assert add(2, 3) == 5

def t_add_negative():
    assert add(-1, -1) == -2

def t_divide():
    assert divide(10, 2) == 5

def t_divide_by_zero_raises():
    raised = False
    try:
        divide(1, 0)
    except ZeroDivisionError:
        raised = True
    assert raised, "expected ZeroDivisionError"

def t_buggy_on_purpose():
    assert add(2, 2) == 5        # this one is wrong, to show a failure report

tests = [
    ("add_positive", t_add_positive),
    ("add_negative", t_add_negative),
    ("divide", t_divide),
    ("divide_by_zero_raises", t_divide_by_zero_raises),
    ("buggy_on_purpose", t_buggy_on_purpose),
]

passed, failed = 0, 0
for name, test in tests:
    try:
        test()
        passed = passed + 1
        print("PASS", name)
    except AssertionError as e:
        failed = failed + 1
        print("FAIL", name, "(assertion)", str(e))
    except Exception as e:
        failed = failed + 1
        print("ERROR", name, str(e))

print("\\n--- summary:", passed, "passed,", failed, "failed ---")
# A real runner adds discovery (find t_*), fixtures, and a non-zero exit on failure.
""",
        ),
        _t(
            "Integration tests & fixtures",
            "9 min",
            r"""# Integration tests & fixtures

Unit tests prove pieces work; **integration tests** prove they work *together* —
your code with a real database, two services over HTTP, the ORM against an
actual schema. They catch the bugs that live in the seams: wrong SQL, mismatched
serialisation, misconfigured wiring.

The challenge is **managing external state** reliably:

- **Fixtures** — set up the needed state before a test and tear it down after,
  so every test starts clean and independent.
- **Test databases** — a real-but-disposable DB: spin one up (often in a
  container), run migrations, seed data, and **roll back or recreate** between
  tests so they don't pollute each other. (An in-memory SQLite is a fast stand-in
  for many cases.)
- **Test containers** — programmatically start real dependencies (Postgres,
  Redis, Kafka) in Docker for the test run, then throw them away.

Keep them honest and maintainable:

- **Isolation** — each test owns its data; never depend on another test's
  leftovers or on run order.
- **Realistic but bounded** — test the real integration, but a *few* well-chosen
  scenarios, not the whole matrix (that's the pyramid — keep these fewer than
  unit tests).
- **Clean up always** — use fixtures' teardown so a failing test doesn't leave
  state that breaks the next one.

Integration tests are slower and more fragile than unit tests, so invest in them
deliberately — enough to trust your wiring, not so many that the suite crawls.
""",
        ),
        _t(
            "Running tests in CI; flaky tests",
            "9 min",
            r"""# Running tests in CI; flaky tests

Tests only protect you if they **run automatically**. **Continuous Integration
(CI)** executes your suite on every push and pull request: check out the code,
install deps, run lint + type-check + tests (+ coverage), and **block the merge**
if anything fails. Pair it with **branch protection** so red code can't reach
`main`. This is the authoritative gate from your Git course — the safety net the
whole team relies on.

CI essentials:

- **Fast feedback** — keep the suite quick (parallelise, cache deps); a 40-minute
  suite gets ignored or bypassed.
- **Deterministic environment** — pin dependency versions and a clean container
  so "works on my machine" disappears.
- **Clear reports** — surface exactly which test failed and why.

**The flaky-test plague.** A *flaky* test passes and fails without code changes —
usually from timing (sleeps, real clocks), test interdependence (shared state,
order), randomness, or network calls. Flakies are corrosive: people start
re-running until green and **stop trusting the suite**, so real failures get
ignored. Treatment:

- **Quarantine** the flaky test (mark it, stop it blocking) and **fix the root
  cause** — inject the clock, control randomness with a seed, remove shared
  state, mock the network.
- **Never** "fix" flakiness with a blanket retry that hides a real race.

A trustworthy CI suite is one where **red always means broken**. Protect that
signal fiercely — it's the foundation of shipping confidently.
""",
        ),
        quiz_lesson(
            "Quiz: Testing Real Code",
            (
                q(
                    "What is the main difference between a stub and a mock?",
                    (
                        opt(
                            "A stub supplies canned inputs (state); a mock verifies interactions (behaviour)",
                            correct=True,
                        ),
                        opt("A stub is faster than a mock"),
                        opt("A mock returns random data"),
                        opt("They are identical"),
                    ),
                    "Stubs control what your code receives; mocks/spies assert how a dependency was called.",
                ),
                q(
                    "What makes dependency injection valuable for testing?",
                    (
                        opt(
                            "Code receives its dependencies, so tests can pass in doubles",
                            correct=True,
                        ),
                        opt("It makes code run faster in production"),
                        opt("It removes the need for any tests"),
                        opt("It encrypts dependencies"),
                    ),
                    "Injected dependencies can be swapped for stubs/mocks, isolating the unit under test.",
                ),
                q(
                    "What is the TDD cycle?",
                    (
                        opt("Red (failing test) → Green (make it pass) → Refactor", correct=True),
                        opt("Write code → write docs → deploy"),
                        opt("Plan → build → ship"),
                        opt("Mock → merge → measure"),
                    ),
                    "Write a failing test, the simplest code to pass it, then refactor safely — in tiny loops.",
                ),
                q(
                    "Why use parameterised tests?",
                    (
                        opt(
                            "Run the same logic over many input cases, each reported separately, with no duplication",
                            correct=True,
                        ),
                        opt("To make tests run in parallel"),
                        opt("To increase code coverage automatically"),
                        opt("To avoid writing assertions"),
                    ),
                    "One test body + a table of cases keeps tests DRY and pinpoints which case failed.",
                ),
                q(
                    "Why are flaky tests dangerous beyond just being annoying?",
                    (
                        opt(
                            "People stop trusting the suite and start ignoring real failures",
                            correct=True,
                        ),
                        opt("They permanently corrupt the codebase"),
                        opt("They increase coverage falsely"),
                        opt("They only fail in production"),
                    ),
                    "If red doesn't reliably mean broken, the safety net loses its value; fix root causes, don't blind-retry.",
                ),
                q(
                    "What's the right scope for integration tests in the pyramid?",
                    (
                        opt(
                            "Fewer than unit tests — a focused set proving the wiring/seams work",
                            correct=True,
                        ),
                        opt("More than unit tests"),
                        opt("None — units cover everything"),
                        opt("Only manual"),
                    ),
                    "Integration tests are slower/fragile; keep a deliberate, bounded set above the unit base.",
                ),
            ),
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# testing-advanced
# ──────────────────────────────────────────────────────────────────────

_TEST_ADVANCED = SeedCourse(
    slug="testing-advanced",
    title="Software Testing & QA — Advanced",
    description=(
        "Beyond example-based tests: property-based testing, mutation testing to "
        "measure test quality, performance/load testing, contract testing for "
        "microservices, and building a coherent quality strategy with the right "
        "metrics and gates."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Property-based testing",
            "10 min",
            r"""# Property-based testing

Example-based tests check specific inputs you thought of. **Property-based
testing** flips it: you state a **property** that must hold for *all* inputs, and
the framework (Hypothesis in Python, QuickCheck's descendants elsewhere)
**generates hundreds of random inputs** trying to break it.

You don't assert exact outputs — you assert **invariants**:

- **Round-trip** — `decode(encode(x)) == x` for any `x`.
- **Idempotence** — `sort(sort(x)) == sort(x)`.
- **Commutativity / equivalence** — `add(a, b) == add(b, a)`; your fast function
  agrees with a slow obvious reference.
- **Structural** — the output of `sort` is ordered and a permutation of the input.

```python
# read-along (Hypothesis): generate ints, check a property
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sorted_is_ordered_and_same_multiset(xs):
    result = sorted(xs)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))
    assert sorted(result) == sorted(xs)     # same elements
```

The superpower: it explores edge cases you'd never enumerate — empty lists,
duplicates, huge/negative numbers, weird Unicode — and when it finds a failure,
it **shrinks** it to the *minimal* reproducing input (e.g. `[0, -1]`), making the
bug obvious. You'll run a property check next. It complements example tests, it
doesn't replace them — use it where clear invariants exist.
""",
        ),
        _code(
            "A property-based check (numpy-generated inputs)",
            "13 min",
            r"""# Property-based testing in miniature: generate many random inputs and assert
# INVARIANTS hold for all of them. (numpy stands in for a generator like Hypothesis.)
import numpy as np

np.random.seed(0)

# Property 1: output is ordered.  Property 2: it's a permutation of the input.
def check_sort(xs):
    result = sorted(xs)        # the function under test
    ordered = all(result[i] <= result[i + 1] for i in range(len(result) - 1))
    same_multiset = sorted(result) == sorted(xs)
    return ordered and same_multiset

failures = []
for trial in range(500):
    n = int(np.random.randint(0, 12))
    xs = [int(v) for v in np.random.randint(-50, 50, size=n)]   # random case
    if not check_sort(xs):
        failures.append(xs)

print("trials:", 500, " failures:", len(failures))
print("sort properties hold for all generated inputs:", len(failures) == 0)

# Now a BUGGY 'unique' to see a property catch it (and 'shrink' to a small case):
# it claims to keep first-seen order, but list(set(...)) loses ordering.
def keeps_order(xs):
    seen = []
    for v in xs:
        if v not in seen:
            seen.append(v)
    buggy = list(set(xs))      # the bug: set() drops order
    return buggy == seen

counterexample = None
for trial in range(500):
    xs = [int(v) for v in np.random.randint(0, 5, size=int(np.random.randint(0, 6)))]
    if not keeps_order(xs):
        counterexample = xs
        break
print("order-preserving property — counterexample found:", counterexample)
""",
        ),
        _t(
            "Mutation testing: who tests the tests?",
            "9 min",
            r"""# Mutation testing

Coverage tells you code *ran*; it can't tell you your assertions are any good. A
test that executes a line but checks nothing gives false confidence.
**Mutation testing** measures test quality directly by asking: *if I introduce a
bug, will a test catch it?*

How it works:

1. The tool makes small **mutants** of your code — flip `>` to `>=`, `+` to `-`,
   `and` to `or`, `True` to `False`, delete a line.
2. It runs your test suite against each mutant.
3. If a test **fails**, the mutant is **killed** (good — your tests caught the
   injected bug). If all tests still **pass**, the mutant **survived** (bad —
   that change is invisible to your tests).

Your **mutation score** = killed / total mutants. Surviving mutants point at
exactly where your tests are weak — a line you execute but never truly check.

It's the honest answer to "are these tests actually protecting me?" — far more
meaningful than a coverage percentage. Tools: `mutmut`/`cosmic-ray` (Python),
Stryker (JS), PIT (Java). The catch is **cost**: running the whole suite once
per mutant is slow, so target it at critical modules and run it periodically (not
every commit). Use it to find and fix the gaps coverage can't see.
""",
        ),
        _t(
            "Performance & load testing",
            "10 min",
            r"""# Performance & load testing

Functional tests ask "is it correct?"; performance tests ask "is it **fast
enough**, and does it **hold up** under load?" The main flavours:

- **Load testing** — expected traffic. Does it meet latency/throughput targets
  at normal and peak volume?
- **Stress testing** — push *past* the limit to find the breaking point and check
  it **fails gracefully** (sheds load, returns errors) rather than collapsing.
- **Spike testing** — sudden surges (a launch, a flash sale).
- **Soak/endurance** — sustained load for hours to surface leaks and slow
  degradation.

Measure the **right numbers**: not the average (which hides pain) but
**percentiles** — p95, p99 latency — because the slowest 1% of requests are
often where users churn and SLAs break. Track throughput (req/s), error rate,
and resource use (CPU, memory, connections) together.

Practical guidance:

- Test against a **production-like environment** with realistic data volumes —
  results from a laptop are meaningless.
- **Define targets first** (SLOs: "p99 < 200 ms at 1k req/s") so a result is
  pass/fail, not vibes.
- Find the **bottleneck** (database, lock, GC, N+1 query), fix, re-test — it's
  iterative.
- Tools: k6, Locust, JMeter, Gatling.

Performance is a feature; bake these tests into CI for critical paths so a
regression is caught before users feel it.
""",
        ),
        _t(
            "Contract testing for microservices",
            "9 min",
            r"""# Contract testing for microservices

When your system is many services talking over APIs, a classic gap appears: each
service's unit tests pass, but they break each other because their **API
expectations drift apart** (the provider renames a field; the consumer still
expects the old one). Full end-to-end tests across all services catch it but are
slow, flaky, and need everything deployed together.

**Contract testing** fills the gap. It verifies the **agreement (contract)**
between a **consumer** and a **provider** without running both at once:

- The **consumer** defines what it expects: "when I GET /users/1, I expect a JSON
  object with `id` and `name`." This generates a contract.
- The **provider** is tested against that contract: "does my real response
  satisfy every consumer's expectations?"

If the provider changes in a way that breaks a consumer's contract, *its* tests
fail — at build time, in isolation, before deployment. **Consumer-driven
contracts** (e.g. **Pact**) share these contracts via a broker so providers know
every consumer they must not break.

The payoff: the **confidence of integration testing** with the **speed and
independence of unit tests**, and teams can deploy services independently without
fear of silently breaking a downstream consumer. It's a cornerstone of testing
in a microservices/distributed architecture.
""",
        ),
        _t(
            "A coherent quality strategy",
            "10 min",
            r"""# A coherent quality strategy

Quality isn't a pile of test types — it's a **strategy** that puts the right
checks in the right places, balancing confidence against speed and cost. Pull
the whole track together:

- **Honour the pyramid** — many unit, fewer integration, few e2e; add
  property-based where invariants exist, contract tests at service boundaries,
  performance tests on critical paths.
- **Automate the gate** — CI runs everything on every PR; **branch protection**
  blocks merging on red or on a coverage drop. Quality you don't enforce decays.
- **Pick metrics that mean something** — coverage as a *floor* (don't regress),
  **mutation score** for test strength, flaky-rate (keep near zero), escaped-bug
  count (bugs found in production — the ultimate scoreboard), and lead time.
- **Shift left *and* right** — catch issues early (tests, types, review) *and*
  watch production (monitoring, alerting, error tracking, feature flags for safe
  rollout). You can't test everything pre-release; observe what you can't predict.
- **Quality is everyone's job** — developers own their tests; QA shapes
  strategy, exploratory testing, and tooling — not a gate at the end.

The endgame is **shipping fast *because* you're confident**: a fast,
trustworthy suite + automated gates + production observability let a team move
quickly *and* safely. Tests aren't the cost of going fast — they're what makes
going fast sustainable.
""",
        ),
        quiz_lesson(
            "Quiz: Advanced Testing & QA",
            (
                q(
                    "What does property-based testing assert?",
                    (
                        opt(
                            "Invariants that must hold for many auto-generated inputs", correct=True
                        ),
                        opt("Exact outputs for a few hand-picked inputs"),
                        opt("That coverage is 100%"),
                        opt("That the code compiles"),
                    ),
                    "You state a property (e.g. round-trip, ordering) and the tool generates inputs trying to break it.",
                ),
                q(
                    "When property-based testing finds a failure, what's especially helpful?",
                    (
                        opt("It shrinks the failure to a minimal reproducing input", correct=True),
                        opt("It automatically fixes the bug"),
                        opt("It increases coverage"),
                        opt("It disables the test"),
                    ),
                    "Shrinking reduces a random failing case to the smallest one, making the bug obvious.",
                ),
                q(
                    "What does mutation testing measure that coverage cannot?",
                    (
                        opt(
                            "Whether your tests actually fail when a bug is introduced (test strength)",
                            correct=True,
                        ),
                        opt("How many lines ran"),
                        opt("Execution speed"),
                        opt("Memory usage"),
                    ),
                    "It injects bugs (mutants) and checks if tests kill them — directly grading assertion quality.",
                ),
                q(
                    "Why report p95/p99 latency instead of the average?",
                    (
                        opt(
                            "The slowest requests (tail) are where users churn and SLAs break; averages hide them",
                            correct=True,
                        ),
                        opt("Percentiles are easier to compute"),
                        opt("Averages are always zero"),
                        opt("p99 measures throughput"),
                    ),
                    "Tail latency reflects the worst real user experience; averages mask it.",
                ),
                q(
                    "What problem does contract testing solve?",
                    (
                        opt(
                            "Drift between a consumer's expectations and a provider's API, without full e2e runs",
                            correct=True,
                        ),
                        opt("Slow unit tests"),
                        opt("Lack of code coverage"),
                        opt("Memory leaks under load"),
                    ),
                    "It verifies the consumer–provider agreement in isolation, catching breaking API changes at build time.",
                ),
                q(
                    "Which is the most meaningful 'scoreboard' metric for quality?",
                    (
                        opt("Bugs that escaped to production", correct=True),
                        opt("Total lines of test code"),
                        opt("Number of test files"),
                        opt("How long the suite takes"),
                    ),
                    "Escaped defects measure real outcomes; coverage/mutation are inputs, not the goal.",
                ),
            ),
        ),
    ),
)


TESTING_COURSES = (_TEST_BASICS, _TEST_INTERMEDIATE, _TEST_ADVANCED)
