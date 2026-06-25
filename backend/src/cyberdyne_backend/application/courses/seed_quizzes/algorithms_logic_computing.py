"""Curated quiz questions for "Basics of Algorithms, Logic and Computing".
Keys are the EXACT content-lesson titles; the seed interleaves a checkpoint quiz
after each content lesson plus a final comprehensive quiz.

A standard technical course (not a language course): no ``[[keep]]`` markers,
fully translatable; code/terms in options use markdown backticks."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "A 100-year chain reaction: the big question": (
            q(
                "What was Hilbert's Entscheidungsproblem asking?",
                (
                    opt(
                        "Whether a universal mechanical procedure could decide if any "
                        "mathematical statement is true",
                        correct=True,
                    ),
                    opt("Whether machines can think like humans"),
                    opt("How fast a computer can run"),
                    opt("Whether every number is prime or composite"),
                ),
                "The Entscheidungsproblem ('decision problem') asked whether math could be "
                "fully automated by an algorithm.",
            ),
            q(
                "What was Turing's answer to whether every math problem can be solved by an "
                "algorithm?",
                (
                    opt("No", correct=True),
                    opt("Yes"),
                    opt("Only with infinite memory"),
                    opt("Only for prime numbers"),
                ),
                "Turing proved (1936) that no universal algorithm can decide all mathematical "
                "statements.",
            ),
            q(
                "Why does 'just use more compute' not overcome the limits in this course?",
                (
                    opt(
                        "The limits are mathematical, not about speed or memory",
                        correct=True,
                    ),
                    opt("Because computers are too expensive"),
                    opt("Because algorithms are always slow"),
                    opt("It actually does overcome them"),
                ),
                "Undecidability is a mathematical boundary; infinite CPU/memory does not cross it.",
            ),
        ),
        "What is an algorithm? The Turing machine": (
            q(
                "Which best describes an algorithm?",
                (
                    opt("A finite list of unambiguous mechanical steps", correct=True),
                    opt("Any piece of computer hardware"),
                    opt("A creative guess at an answer"),
                    opt("An infinite list of instructions"),
                ),
                "An algorithm is a finite, unambiguous procedure a machine can follow.",
            ),
            q(
                "What does the Church-Turing thesis claim?",
                (
                    opt(
                        "Anything effectively computable can be computed by a Turing machine",
                        correct=True,
                    ),
                    opt("Turing machines are faster than real computers"),
                    opt("Every program halts"),
                    opt("Lambda calculus is more powerful than Turing machines"),
                ),
                "All reasonable models of computation capture the same computable functions.",
            ),
            q(
                "Why does 'programs are data' matter?",
                (
                    opt(
                        "A universal machine can run any program, enabling the self-reference "
                        "used to break the Halting Problem",
                        correct=True,
                    ),
                    opt("It makes programs run faster"),
                    opt("It means data cannot be programs"),
                    opt("It proves every program halts"),
                ),
                "Encoding a program as data lets one machine run another - and lets a program "
                "reason about itself.",
            ),
        ),
        "The basics of logic & formal systems": (
            q(
                "In logic, what do quantifiers ('for all', 'there exists') let us express?",
                (
                    opt("Statements about all or some members of a domain", correct=True),
                    opt("Only true statements"),
                    opt("The speed of a computation"),
                    opt("Numbers in binary"),
                ),
                "Predicate logic's quantifiers let us state claims about all programs/numbers at "
                "once.",
            ),
            q(
                "What are the parts of a formal system?",
                (
                    opt("Axioms, inference rules, and theorems", correct=True),
                    opt("Variables, loops, and functions"),
                    opt("Inputs, outputs, and memory"),
                    opt("Bits, bytes, and words"),
                ),
                "A formal system derives theorems from axioms via mechanical inference rules.",
            ),
            q(
                "A formal system is 'complete' when it...",
                (
                    opt("can prove every true statement in its language", correct=True),
                    opt("never proves anything false"),
                    opt("always halts"),
                    opt("has finitely many axioms"),
                ),
                "Completeness = proves all truths; soundness = proves only truths.",
            ),
        ),
        "Can we automate math? The Entscheidungsproblem": (
            q(
                "A decision problem is 'decidable' when...",
                (
                    opt(
                        "an algorithm always halts with the correct yes/no answer",
                        correct=True,
                    ),
                    opt("it can be answered by a human"),
                    opt("it has a yes answer"),
                    opt("it runs quickly"),
                ),
                "Decidable means a guaranteed-terminating algorithm gives the right yes/no answer.",
            ),
            q(
                "Which problem is UNDECIDABLE?",
                (
                    opt(
                        "Deciding the truth of arbitrary first-order math statements", correct=True
                    ),
                    opt("Deciding whether a number is prime"),
                    opt("Deciding whether a finite graph has a cycle"),
                    opt("Deciding whether a propositional formula is a tautology"),
                ),
                "The Entscheidungsproblem is undecidable; the others are decidable.",
            ),
            q(
                "What is a 'reduction' in computability proofs?",
                (
                    opt(
                        "Showing that if you could solve A you could solve a known-impossible B, "
                        "so A is impossible too",
                        correct=True,
                    ),
                    opt("Making a program shorter"),
                    opt("Lowering the time complexity"),
                    opt("Removing axioms from a system"),
                ),
                "Reduction transfers impossibility: solve A -> solve B; B impossible -> A "
                "impossible.",
            ),
        ),
        "The Halting Problem": (
            q(
                "What does the Halting Problem ask?",
                (
                    opt(
                        "For a general program that decides if any program halts on a given input",
                        correct=True,
                    ),
                    opt("Whether a program runs quickly"),
                    opt("Whether a program has bugs"),
                    opt("Whether a program uses too much memory"),
                ),
                "It asks for a universal `halts(program, input)` that always answers correctly.",
            ),
            q(
                "How did Turing prove the Halting Problem is unsolvable?",
                (
                    opt(
                        "By building a program that does the opposite of whatever `halts` "
                        "predicts about it, creating a contradiction",
                        correct=True,
                    ),
                    opt("By running every program to completion"),
                    opt("By measuring CPU speed"),
                    opt("By proving all programs loop forever"),
                ),
                "Self-reference + negation: the 'trouble' program contradicts any decider.",
            ),
            q(
                "Why is the Halting Problem relevant to real software questions?",
                (
                    opt(
                        "Questions like 'does this program ever crash or reach line X?' contain a "
                        "hidden halting question and inherit its undecidability",
                        correct=True,
                    ),
                    opt("It is only a theoretical curiosity with no impact"),
                    opt("It makes programs run faster"),
                    opt("It proves antivirus software is perfect"),
                ),
                "Many practical 'does it ever...?' questions reduce to halting.",
            ),
        ),
        "Goedel's incompleteness & undecidable truths": (
            q(
                "What does Goedel's first incompleteness theorem say?",
                (
                    opt(
                        "Any consistent system rich enough for arithmetic has true statements it "
                        "cannot prove",
                        correct=True,
                    ),
                    opt("Every true statement is provable"),
                    opt("Mathematics is fully decidable"),
                    opt("All systems are inconsistent"),
                ),
                "Consistency forces incompleteness: truth outruns proof.",
            ),
            q(
                "The Continuum Hypothesis is an example of a statement that is...",
                (
                    opt("independent of ZFC - neither provable nor refutable in it", correct=True),
                    opt("provably true in ZFC"),
                    opt("provably false in ZFC"),
                    opt("about prime numbers"),
                ),
                "Goedel and Cohen showed CH is independent of the standard axioms of set theory.",
            ),
            q(
                "What do Goedel (incompleteness) and Turing (undecidability) have in common?",
                (
                    opt(
                        "Both show finite, mechanical proof/computation cannot capture all "
                        "mathematical truth, using self-reference",
                        correct=True,
                    ),
                    opt("Both proved every problem is solvable"),
                    opt("Both invented the transistor"),
                    opt("Both are about hardware speed"),
                ),
                "They are two faces of one coin, both built on self-reference.",
            ),
        ),
        "Rice's theorem, program equivalence & Busy Beaver": (
            q(
                "What does Rice's theorem state?",
                (
                    opt(
                        "Every non-trivial semantic property of programs is undecidable",
                        correct=True,
                    ),
                    opt("Every program halts eventually"),
                    opt("Syntax errors are undecidable"),
                    opt("All programs are equivalent"),
                ),
                "Any non-trivial property of program BEHAVIOUR is undecidable in general.",
            ),
            q(
                "Why can compiler optimisation and verification never be perfect in general?",
                (
                    opt("Program equivalence is undecidable", correct=True),
                    opt("Compilers are too slow"),
                    opt("Programs are always buggy"),
                    opt("There is no demand for it"),
                ),
                "Deciding whether two programs compute the same function is undecidable.",
            ),
            q(
                "Why is the Busy Beaver function BB(n) uncomputable?",
                (
                    opt(
                        "Computing BB(n) would let you solve the Halting Problem",
                        correct=True,
                    ),
                    opt("It only has finitely many values"),
                    opt("It grows slower than linear functions"),
                    opt("Because Turing machines are slow"),
                ),
                "Run a machine BB(n) steps; if not halted, it never will - a halting oracle.",
            ),
        ),
        "The day-to-day limits: problems no algorithm can solve": (
            q(
                "What is the difference between 'uncomputable' and 'intractable' (e.g. NP-hard)?",
                (
                    opt(
                        "Uncomputable = no algorithm works for all inputs; intractable = solvable "
                        "but maybe not in reasonable time",
                        correct=True,
                    ),
                    opt("They mean exactly the same thing"),
                    opt("Intractable problems have no solution ever"),
                    opt("Uncomputable problems just need a faster CPU"),
                ),
                "Uncomputable is a hard mathematical wall; intractable is about practical time.",
            ),
            q(
                "Why can't there be a perfect antivirus (detect all malware, zero false "
                "positives)?",
                (
                    opt(
                        "'Does this program ever behave maliciously?' is a non-trivial semantic "
                        "property - undecidable by Rice's theorem",
                        correct=True,
                    ),
                    opt("Antivirus companies are not trying hard enough"),
                    opt("Malware is always easy to spot"),
                    opt("Because CPUs are too slow"),
                ),
                "Perfect detection is a semantic property of behaviour, hence undecidable.",
            ),
            q(
                "Does 'undecidable' mean a problem can never be solved for any input?",
                (
                    opt(
                        "No - it means no single algorithm solves ALL inputs; specific cases can "
                        "still be solved by humans or specialised tools",
                        correct=True,
                    ),
                    opt("Yes, it can never be solved in any case"),
                    opt("Yes, not even for one input"),
                    opt("It means the problem is illegal"),
                ),
                "Undecidable = no universal algorithm; specific instances are often solvable.",
            ),
        ),
    },
    final=(
        q(
            "The question that launched theoretical computer science was:",
            (
                opt("Can every mathematical problem be solved by an algorithm?", correct=True),
                opt("How many transistors fit on a chip?"),
                opt("What is the fastest sorting algorithm?"),
                opt("Can machines feel emotions?"),
            ),
            "Hilbert's Entscheidungsproblem; Turing answered 'no'.",
        ),
        q(
            "A Turing machine consists of...",
            (
                opt("an infinite tape, a read/write head, states, and a rule table", correct=True),
                opt("a CPU, RAM, and a hard drive"),
                opt("a keyboard, screen, and mouse"),
                opt("neurons and synapses"),
            ),
            "The minimal abstract model that captures all computation.",
        ),
        q(
            "Which is TRUE about the Halting Problem?",
            (
                opt("No general algorithm can decide if an arbitrary program halts", correct=True),
                opt("It can be solved with enough memory"),
                opt("It only applies to buggy programs"),
                opt("Modern compilers solve it completely"),
            ),
            "It is undecidable, proved by self-reference.",
        ),
        q(
            "Goedel's incompleteness theorems show that...",
            (
                opt(
                    "a consistent arithmetic system has true statements it cannot prove",
                    correct=True,
                ),
                opt("all mathematics is decidable"),
                opt("every statement can be proved or disproved"),
                opt("computers will replace mathematicians"),
            ),
            "Truth outruns proof in any sufficiently powerful consistent system.",
        ),
        q(
            "Which real-world goal is impossible IN GENERAL due to undecidability?",
            (
                opt(
                    "Automatically proving that any arbitrary program is bug-free",
                    correct=True,
                ),
                opt("Sorting a list of numbers"),
                opt("Adding two integers"),
                opt("Checking if a finite list contains a value"),
            ),
            "Proving arbitrary programs never misbehave reduces to halting/Rice - undecidable.",
        ),
        q(
            "The healthiest engineering takeaway from these limits is to...",
            (
                opt(
                    "be honest about guarantees - use tests, sandboxes, monitoring and "
                    "kill-switches instead of promising perfect, universal correctness",
                    correct=True,
                ),
                opt("give up on building software"),
                opt("assume more compute will always solve it"),
                opt("ignore the limits entirely"),
            ),
            "Undecidable does not mean hopeless; it means trade perfect/universal for "
            "good-enough/bounded.",
        ),
    ),
)
