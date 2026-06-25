"""Academy seed content — a single foundational course that opens the Computer
Engineering path: "Basics of Algorithms, Logic and Computing".

It frames the last ~100 years of computer science (Hilbert's
Entscheidungsproblem -> Turing -> Shannon -> ... -> modern AI) around one
question: *can every mathematical problem be solved by an algorithm?* The
answer is no, and the course builds the intuition for **why** — the Turing
machine, formal logic, the Halting Problem, Goedel's incompleteness, Rice's
theorem, and the Busy Beaver — with a heavy, deliberate focus on the
**day-to-day problems no algorithm can fully solve** (bug-free software, perfect
antivirus, AI-agent safety, perfect compression, inferring true human intent,
spec/code equivalence, market prediction).

A single course (no Basics/Intermediate/Advanced split), text lessons with
Mermaid diagrams, a checkpoint quiz after each lesson plus a final. A standard
technical course (no ``[[keep]]`` markers) — fully translatable.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_COURSE = SeedCourse(
    slug="algorithms-logic-computing",
    title="Basics of Algorithms, Logic and Computing",
    description=(
        "The real foundations of computer science, in one course. Starting from "
        "the question that started it all — 'can every mathematical problem be "
        "solved by an algorithm?' — we trace a 100-year chain reaction from "
        "Hilbert and Turing to modern AI, learn what an algorithm and a Turing "
        "machine actually are, the basics of logic and formal systems, and the "
        "deep limits of computation: the Halting Problem, Goedel's "
        "incompleteness, Rice's theorem, and the Busy Beaver. The payoff is "
        "practical: a clear-eyed look at the everyday problems — bug-free "
        "software, perfect antivirus, AI-agent safety, perfect compression, "
        "reading true human intent — that no algorithm can ever fully solve."
    ),
    level="Beginner",
    lessons=(
        _t(
            "A 100-year chain reaction: the big question",
            "9 min",
            r"""# A 100-year chain reaction: the big question

Almost everything in modern computing — your phone, the cloud, the AI that
writes code — traces back to a single, surprisingly boring question a
mathematician asked nearly a century ago:

> **Can every mathematical problem be solved by an algorithm?**

In the 1920s, David Hilbert dreamed of *automating mathematics*. He asked
whether there is a universal mechanical procedure that, given any mathematical
statement, decides whether it is true. He called it the
**Entscheidungsproblem** (German for "decision problem"). The hope: turn the
crank, and math answers itself.

In 1936, Alan Turing answered: **no**. But to prove it, he first had to define
what an "algorithm" even *is* — and in doing so he invented the abstract
blueprint of every computer ever built. That single "no" is the bedrock this
whole course stands on.

From there, a chain reaction:

```mermaid
timeline
    title 100 years of computer science, in one breath
    1928 : Hilbert asks the Entscheidungsproblem
    1931 : Goedel - incompleteness theorems
    1936 : Turing - the machine, and the Halting Problem ("no")
    1948 : Shannon - information, the bit, entropy
    1950s : Logic + circuits become real computers
    2012 : Deep learning works (data + compute)
    2017 : Transformers - "attention is all you need"
    2020s : Large language models, AI agents
```

Notice the shape of the story. Turing **defined the machine**; Shannon gave it a
**currency** (the bit); decades of work gave it **data and architectures**; and
modern AI **turned the dial to maximum**. Every layer is astonishing — and yet
the very first result, Turing's "no", drew a hard boundary that *no amount of
scale will ever cross*.

This course is about that boundary. Not to discourage you — most real problems
*can* be attacked by algorithms — but because knowing **where the edges are**
makes you a far sharper engineer. By the end you will understand why "just throw
more compute at it" is sometimes not a strategy but a category error.

Here is the throughline to keep in mind:

> A computer is a machine for running algorithms. An algorithm is a **finite**
> procedure. But mathematics is full of **infinities** — infinitely many
> numbers, programs, and proofs. The drama of this course is what happens when
> we try to squeeze that infinitude into a finite machine.
""",
        ),
        _t(
            "What is an algorithm? The Turing machine",
            "11 min",
            r"""# What is an algorithm? The Turing machine

Before we can ask "what can't algorithms do?", we need a precise definition of
**algorithm**. Intuitively, an algorithm is a *finite list of unambiguous steps*
that, given an input, eventually produces an output — like a recipe a machine
can follow with no creativity required.

Turing made this precise with an imaginary device now called the **Turing
machine**. It is deliberately minimal:

- an **infinite tape** divided into cells (the memory),
- a **read/write head** that sits over one cell,
- a small **table of rules** (the program),
- and a **current state**.

At each step the machine reads the symbol under the head, and the rule for
*(state, symbol)* tells it what to write, which way to move (left/right), and
which state to enter next.

```mermaid
flowchart LR
    subgraph Tape
      direction LR
      C1["...|1|0|1|1|0|..."]
    end
    H["Read/Write head<br/>(current state)"] --> C1
    R["Rule table:<br/>(state, symbol) -><br/>(write, move, next state)"] --> H
```

A tiny rule table behaves like a state machine. For example, a machine that
flips bits until it hits a blank:

```mermaid
stateDiagram-v2
    [*] --> Scan
    Scan --> Scan: read 0 / write 1, move right
    Scan --> Scan: read 1 / write 0, move right
    Scan --> Halt: read blank
    Halt --> [*]
```

That's it. No screen, no internet — yet this is enough to compute **anything any
computer can compute**. That claim is the **Church-Turing thesis**: every
"effective procedure" (anything a human could in principle carry out
mechanically with paper and pencil) can be done by a Turing machine. Different
formalisms — Turing machines, lambda calculus, your favourite programming
language — all turn out to capture exactly the same set of computable functions.
We call such languages **Turing-complete**.

Two consequences matter for the rest of the course:

1. **"Computable" has a precise meaning.** A function is computable if *some*
   Turing machine computes it. This lets us prove that certain functions are
   **not** computable — a mathematical fact, not a temporary limitation.
2. **Programs are data.** A Turing machine's rule table can itself be written on
   a tape and fed to another machine — a **universal** machine that runs any
   program. This is why your laptop can run any app; it is also the seed of the
   self-reference trick that breaks the Halting Problem two lessons from now.

Keep the core image: an algorithm is a **finite** rulebook. The power — and the
limits — of computing both flow from that finiteness.
""",
        ),
        _t(
            "The basics of logic & formal systems",
            "11 min",
            r"""# The basics of logic & formal systems

Computation and logic are two sides of one coin. To talk about what can be
*proved* or *decided*, we need the basics of formal logic.

**Propositional logic** deals with statements that are true or false, combined
with connectives: AND, OR, NOT, IMPLIES. Their meaning is fixed by **truth
tables**:

| `A` | `B` | `A AND B` | `A OR B` | `A IMPLIES B` |
|---|---|---|---|---|
| T | T | T | T | T |
| T | F | F | T | F |
| F | T | F | T | T |
| F | F | F | F | T |

**Predicate logic** adds *quantifiers* — "for all" and "there exists" — so we can
state things like "for all programs p, p halts on input 0". This extra power is
exactly what lets us phrase deep questions about all programs at once.

A **formal system** is a game played with symbols. It has:

- **axioms** — statements accepted without proof,
- **inference rules** — mechanical ways to derive new statements from old ones,
- **theorems** — everything you can reach by applying the rules to the axioms.

```mermaid
flowchart TD
    AX["Axioms<br/>(starting truths)"] --> IR["Inference rules<br/>(mechanical steps)"]
    IR --> TH["Theorems<br/>(everything derivable)"]
    IR --> IR
    style AX fill:#e8f0ff
    style TH fill:#e8ffe8
```

The crucial insight: **a proof is a computation, and a formal system is a kind of
machine.** Deriving a theorem is just applying rules step by step — exactly the
sort of finite, mechanical process a Turing machine can do. So "is there an
algorithm to decide truth?" and "can this formal system prove every truth?" turn
out to be the *same question* wearing different clothes.

Two properties we want from a formal system:

- **Soundness** — it only ever proves things that are actually true.
- **Completeness** — it can prove *every* true statement (in its language).

Hilbert wanted a system for all of mathematics that was sound, complete, and
**decidable** (a machine could check any statement). It sounds reasonable. The
next three lessons show, one devastating result at a time, that you **cannot
have all of it**. Logic itself sets the limits of computation.
""",
        ),
        _t(
            "Can we automate math? The Entscheidungsproblem",
            "9 min",
            r"""# Can we automate math? The Entscheidungsproblem

Now we can state Hilbert's dream precisely. The **Entscheidungsproblem** asks:

> Is there a single algorithm that takes **any** statement in first-order logic
> and decides — always, in finite time — whether it is provable (true)?

If such an algorithm existed, mathematics would, in a sense, be **solved**: hard
conjectures would become a matter of waiting for the machine to print "true" or
"false". Whole research careers would be replaced by a loop.

To reason about this we need the idea of a **decision problem** — a yes/no
question about an input — and what it means to *decide* one:

```mermaid
flowchart TD
    P["A decision problem<br/>(a yes/no question)"] --> Q{"Is there an algorithm that<br/>ALWAYS halts with the<br/>correct yes/no answer?"}
    Q -->|"yes"| D["DECIDABLE<br/>e.g. 'is n prime?'"]
    Q -->|"no"| U["UNDECIDABLE<br/>e.g. the Entscheidungsproblem"]
```

Many problems are happily **decidable**: "is this number prime?", "does this
finite graph have a cycle?", "is this propositional formula a tautology?". For
these, a guaranteed-terminating procedure exists.

But in 1936 Turing (and independently Alonzo Church) proved the
Entscheidungsproblem is **undecidable**. There is no universal algorithm that
decides the truth of arbitrary mathematical statements. Math **cannot** be fully
automated.

The strategy of Turing's proof is worth savouring, because it is the template
for almost every limit in this course:

1. Define precisely what an algorithm is (the Turing machine — done last lesson).
2. Find one specific problem and show **no** Turing machine can solve it (that's
   the Halting Problem — next lesson).
3. Show that *if* you could decide arbitrary math statements, you could solve
   that impossible problem too. Contradiction — so deciding math is impossible.

This is **reduction**: "if I could solve A, I could solve B; but B is known
impossible; therefore A is impossible." It is the single most important proof
technique in computability. Once one domino (the Halting Problem) falls, it
knocks over a whole row of "can we automate ___?" questions.

So let's go knock over that first domino.
""",
        ),
        _t(
            "The Halting Problem",
            "11 min",
            r"""# The Halting Problem

Here is the most famous impossible problem in computer science.

> **The Halting Problem:** write a program `halts(program, input)` that returns
> `true` if `program` eventually stops on that `input`, and `false` if it runs
> forever. It must work for **every** program and always answer in finite time.

It sounds plausible. Some cases are trivial. This obviously never stops:

```python
while True:
    pass
```

But this one?

```python
def f(n):
    if collatz_conjecture_holds(n):
        return True
    while True:
        pass
```

Whether `f` halts depends on an unsolved math problem. A truly universal
`halts` would have to settle questions like that for *all* programs at once.

Turing proved **no such program can exist** — by self-reference. Suppose `halts`
existed. Then we could build a troublemaker:

```python
def trouble():
    if halts(trouble, no_input):   # ask: do I halt?
        while True:                # if "yes", loop forever
            pass
    else:
        return                     # if "no", halt immediately
```

`trouble` is deliberately built to **do the opposite** of whatever `halts`
predicts about it. Now ask: does `trouble` halt?

```mermaid
sequenceDiagram
    participant H as halts(trouble)
    participant T as trouble()
    H->>T: predicts "it halts"
    T-->>H: then it loops forever (contradiction!)
    H->>T: predicts "it loops forever"
    T-->>H: then it halts immediately (contradiction!)
    Note over H,T: No consistent answer exists -> halts() cannot exist
```

Either prediction is immediately wrong. The only way out is that our assumption
was false: **`halts` cannot exist.** The Halting Problem is undecidable.

This is the same diagonalization trick Cantor used to show some infinities are
bigger than others, and that Goedel used for incompleteness. The pattern: build
something that *refers to itself* and *negates the answer*, and any
all-knowing decider collapses into paradox.

Why it's not just a curiosity:

- The Halting Problem **reduces to** countless practical questions. "Does this
  program ever crash / leak this secret / reach this line?" all contain a hidden
  halting question, so they inherit its undecidability.
- It confirms Turing's answer to Hilbert: because deciding math statements would
  let you solve halting, deciding math is impossible too.

One domino down. Next we'll see the same wall from the side of pure mathematics.
""",
        ),
        _t(
            "Goedel's incompleteness & undecidable truths",
            "10 min",
            r"""# Goedel's incompleteness & undecidable truths

Five years *before* Turing, in 1931, Kurt Goedel delivered the first crushing
blow to Hilbert's dream — from inside mathematics itself.

**Goedel's first incompleteness theorem:** any formal system that is powerful
enough to describe basic arithmetic, and is **consistent** (never proves a
contradiction), must be **incomplete** — there are true statements it can
**neither prove nor disprove**.

His method, again, is self-reference. Goedel found a way to encode statements
about the system *as numbers inside the system* (Goedel numbering), and built a
sentence that effectively says:

> "This statement has no proof."

```mermaid
flowchart TD
    G["G: 'I am not provable'"] --> Q{"Is G provable?"}
    Q -->|"yes -> we proved a falsehood"| C1["system is UNSOUND"]
    Q -->|"no -> then G is true but unprovable"| C2["system is INCOMPLETE"]
    style C2 fill:#fff0e8
```

If the system could prove `G`, then `G` (which says it's unprovable) would be
false — so the system proves falsehoods. To stay consistent, it must **not**
prove `G` — but then `G` is true and unprovable. Truth outruns proof.

**Second incompleteness theorem:** such a system also cannot prove **its own
consistency**. You can never fully certify the foundations from the inside.

The landscape of statements therefore splits into three regions, not two:

```mermaid
flowchart LR
    S["A statement in the system"] --> P["Provable<br/>(theorems)"]
    S --> R["Refutable<br/>(negation is a theorem)"]
    S --> I["Independent<br/>(neither provable nor refutable)"]
    style I fill:#ffe8e8
```

That third region is real and inhabited. The most famous resident is the
**Continuum Hypothesis** (about the sizes of infinite sets): Goedel and Cohen
showed it is **independent** of the standard axioms of set theory (ZFC). You can
add it *or* its negation and get a perfectly consistent mathematics. The axioms
simply do not decide it.

Goedel (truths that can't be proved) and Turing (problems that can't be decided)
are two faces of the same coin: **the mechanical, finite nature of proof and
computation cannot capture the full, infinite richness of mathematical truth.**
""",
        ),
        _t(
            "Rice's theorem, program equivalence & Busy Beaver",
            "11 min",
            r"""# Rice's theorem, program equivalence & Busy Beaver

The Halting Problem isn't a lone exception. Undecidability is *everywhere* once
you ask about what programs **mean**.

**Rice's theorem** generalises the bad news dramatically:

> *Every* non-trivial **semantic** property of a program is undecidable.

"Semantic" means a property of the program's behaviour (what it computes), not
its text. "Non-trivial" means some programs have it and some don't. So there is
**no general algorithm** to decide questions like:

- "Does this program ever output a negative number?"
- "Does this program compute the same function as that one?"
- "Is this program free of infinite loops?"

```mermaid
flowchart TD
    Q["A question about a program"] --> A{"Is it about syntax<br/>(the text) or semantics<br/>(the behaviour)?"}
    A -->|"syntax: 'does it contain goto?'"| D["decidable"]
    A -->|"semantics + non-trivial"| U["UNDECIDABLE<br/>(Rice's theorem)"]
```

**Program equivalence** — "do these two programs do exactly the same thing on
all inputs?" — is the classic victim. It is undecidable in general, which is why
compiler optimisation, refactoring tools, and formal verification can never be
*perfect* in full generality; they prove what they can and give up safely on the
rest.

Now meet the strangest creature in computability: the **Busy Beaver** function,
`BB(n)`.

> Among all `n`-state Turing machines that eventually halt (on a blank tape),
> `BB(n)` is the **largest number of steps** any of them runs before stopping.

`BB(n)` is **uncomputable** — and not by a little. It grows faster than *any*
computable function. The known values explode immediately:

```mermaid
flowchart LR
    B1["BB(1) = 1"] --> B2["BB(2) = 6"]
    B2 --> B3["BB(3) = 21"]
    B3 --> B4["BB(4) = 107"]
    B4 --> B5["BB(5) = 47,176,870"]
    B5 --> B6["BB(6) > 10 ^ 10 ^ 10 ^ 18  (astronomical)"]
```

Why is it uncomputable? Because **if you could compute `BB(n)`, you could solve
the Halting Problem.** To decide whether some `n`-state machine halts, run it for
`BB(n)` steps; if it hasn't stopped by then, it never will. A Halting oracle is
hidden inside Busy Beaver — so Busy Beaver must be just as impossible.

The lesson: undecidability is not a rare edge case you can route around. The
moment you ask a non-trivial question about what arbitrary code *does*, you are
standing at the same wall Turing found.
""",
        ),
        _t(
            "The day-to-day limits: problems no algorithm can solve",
            "12 min",
            r"""# The day-to-day limits: problems no algorithm can solve

This is the lesson that pays for the others. These limits are not abstract
trivia — they shape real engineering every day. First, a vital distinction:

```mermaid
flowchart TD
    P["Your problem"] --> Q1{"Does ANY algorithm<br/>always solve it?"}
    Q1 -->|"no"| UC["UNCOMPUTABLE<br/>no universal algorithm exists<br/>(a math limit, not a hardware one)"]
    Q1 -->|"yes"| Q2{"Can it be solved<br/>in reasonable time?"}
    Q2 -->|"often not at scale"| NP["INTRACTABLE<br/>(e.g. NP-hard) - solvable<br/>but maybe not quickly"]
    Q2 -->|"yes"| OK["Tractable - go build it"]
    style UC fill:#ffe0e0
    style NP fill:#fff2cc
```

**Uncomputable** is the strong claim: even with *infinite* CPU and memory, no
single algorithm works for all cases. Here are everyday problems that hit that
wall — almost always via the Halting Problem or Rice's theorem:

| Real-world wish | Why it's impossible in general |
|---|---|
| **Bug-free software, proven automatically** — "prove this arbitrary program never crashes / deadlocks" (avionics, banking, smart contracts) | "Does it ever reach a bad state?" is a halting/semantic question -> undecidable |
| **A perfect antivirus** — detect *all* malware, *zero* false positives | "Does this program ever behave maliciously?" is a non-trivial semantic property -> Rice |
| **Provably safe AI agents** — "will this autonomous agent *never* take a catastrophic action?" | For arbitrarily general agents, this is a semantic property of behaviour -> undecidable |
| **Perfect compression for every file** | Pigeonhole: most files are incompressible; no algorithm shrinks all inputs |
| **"Does this code implement this spec?"** — automatic spec/code equivalence | Program equivalence is undecidable in general |
| **Read a user's true intent** — they ask for X but really need Y | "Understanding" is not a fully formalisable function |
| **Perfectly predict the market** | Reflexivity: the prediction changes the system -> self-reference |

Notice the recurring shapes: **behaviour over all inputs**, **self-reference**,
and **infinitude**. Whenever a wish has those, suspect a wall.

```mermaid
mindmap
  root(("No universal<br/>algorithm"))
    Halting-flavoured
      "will it crash / loop / reach line X?"
      "is this agent always safe?"
    Rice-flavoured
      "perfect malware detection"
      "does code match spec?"
    Information limits
      "compress every file"
    Self-reference
      "predict a market you act in"
```

**But — undecidable does NOT mean "nobody ever solves it".** This is the most
important nuance in the course:

- "Undecidable" means *no single algorithm works for **all** inputs.*
- For **specific** inputs, humans and specialised tools succeed all the time.
  Static analyzers prove many real programs terminate; type checkers catch whole
  classes of bugs; mathematicians prove individual theorems by hand; antivirus
  vendors use heuristics and machine learning that are usefully good, just not
  perfect.

So the engineering posture is not despair — it's **honesty about guarantees**.
You trade a *perfect, universal* answer for a *good-enough, bounded* one: tests
instead of proofs of correctness, sandboxes and least-privilege instead of
proven-safe agents, monitoring and kill-switches instead of certainty.

The deepest takeaway of the whole 100-year story:

> **Not everything that is precisely defined is computable.** Some problems are
> beyond algorithms — not because our machines are too slow, but because of the
> mathematical nature of computation itself. Knowing which problems those are is
> what separates an engineer who promises the impossible from one who designs
> for the possible.
""",
        ),
    ),
)


COMPUTING_FOUNDATIONS_COURSES = (_COURSE,)
