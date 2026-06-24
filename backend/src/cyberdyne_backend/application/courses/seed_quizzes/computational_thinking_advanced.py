"""Curated quiz questions for the Programming Logic & Computational Thinking -
Advanced course. Keys are the EXACT content-lesson titles; the seed interleaves
a checkpoint quiz after each content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Flowcharts & pseudocode": (
            q(
                "Which flowchart symbol represents a yes/no question that branches the flow?",
                (
                    opt("A rectangle (process)"),
                    opt("A diamond (decision)", correct=True),
                    opt("A parallelogram (input/output)"),
                    opt("A rounded terminator"),
                ),
                "A diamond is the decision symbol that splits the flow into branches.",
            ),
            q(
                "What does a parallelogram symbol mean in a flowchart?",
                (
                    opt("Start or end of the algorithm"),
                    opt("Input or output (read or display data)", correct=True),
                    opt("A calculation"),
                    opt("A decision"),
                ),
                "The parallelogram is the input/output symbol.",
            ),
            q(
                "How do a flowchart and its matching pseudocode relate?",
                (
                    opt("They describe completely different algorithms"),
                    opt("They describe the SAME algorithm in different notations", correct=True),
                    opt("Pseudocode is always wrong"),
                    opt("A flowchart can only show input, never logic"),
                ),
                "Both express the same algorithm; the diagram just makes control flow visual.",
            ),
        ),
        "A problem-solving methodology": (
            q(
                "What is the FIRST step of the five-step methodology?",
                (
                    opt("Write the code"),
                    opt("Read the statement and underline the inputs", correct=True),
                    opt("Pick a programming language"),
                    opt("Optimise for speed"),
                ),
                "Start by identifying the inputs from the problem statement.",
            ),
            q(
                "When should you actually write the code in this methodology?",
                (
                    opt("First, before anything else"),
                    opt(
                        "Last, after finding the formula, defining variables and desk-checking",
                        correct=True,
                    ),
                    opt("Right after reading the inputs"),
                    opt("Only if the program is large"),
                ),
                "Coding is the final step, once the reasoning is settled.",
            ),
            q(
                "Why desk-check with simple numbers before coding?",
                (
                    opt("To make the program run faster"),
                    opt("To catch logic errors while they are still cheap to fix", correct=True),
                    opt("Because the computer requires it"),
                    opt("To increase code coverage"),
                ),
                "A hand trace with easy values reveals logic mistakes before any code exists.",
            ),
        ),
        "Common errors & debugging": (
            q(
                "Calling age = input(...) then doing age + 1 fails because input() returns what?",
                (
                    opt("A float"),
                    opt("A string (text), which can't be added to a number", correct=True),
                    opt("A boolean"),
                    opt("Nothing at all"),
                ),
                "input() always returns text; you must convert with int()/float() before arithmetic.",
            ),
            q(
                "What does a ZeroDivisionError tell you?",
                (
                    opt("A variable name was misspelled"),
                    opt("A denominator was 0; validate it before dividing", correct=True),
                    opt("Indentation is inconsistent"),
                    opt("A string was used as a number"),
                ),
                "Dividing by zero raises ZeroDivisionError; guard with a count > 0 check.",
            ),
            q(
                "What's a sensible FIRST debugging move when a program errors?",
                (
                    opt("Rewrite the whole program from scratch"),
                    opt(
                        "Read the error message and the line it points to, then print variables",
                        correct=True,
                    ),
                    opt("Delete the failing line"),
                    opt("Assume the computer is broken"),
                ),
                "The error type and line are most of the answer; print() shows the real values.",
            ),
        ),
        "CODE LAB: desk-check a loop (trace variables)": (
            q(
                "What is a desk-check (teste de mesa)?",
                (
                    opt("Running the program on a faster machine"),
                    opt(
                        "Simulating execution by hand, tracking each variable step by step",
                        correct=True,
                    ),
                    opt("A type of unit test framework"),
                    opt("Automatically formatting the code"),
                ),
                "A desk-check traces variable values by hand to verify the logic.",
            ),
            q(
                "Tracing soma = soma + i for i in range(1, 4) starting at soma = 0, what is the final soma?",
                (
                    opt("3"),
                    opt("6", correct=True),
                    opt("10"),
                    opt("4"),
                ),
                "0+1=1, 1+2=3, 3+3=6, so the final soma is 6.",
            ),
            q(
                "In the trace table, what is 'soma before' at the step where i = 2?",
                (
                    opt("0"),
                    opt("1", correct=True),
                    opt("3"),
                    opt("2"),
                ),
                "After i=1 soma became 1, so before the i=2 step soma is 1.",
            ),
        ),
        "CODE LAB: worked problem — the kilowatt bill": (
            q(
                "Given that 100 kWh cost salary/7, what is the price of 1 kWh?",
                (
                    opt("salary / 7"),
                    opt("salary / 700", correct=True),
                    opt("salary / 100"),
                    opt("salary * 0.10"),
                ),
                "1 kWh = (salary / 7) / 100 = salary / 700.",
            ),
            q(
                "In the lab, salary = 1400 makes the price per kWh equal to what?",
                (
                    opt("R$ 1.00"),
                    opt("R$ 2.00", correct=True),
                    opt("R$ 7.00"),
                    opt("R$ 14.00"),
                ),
                "1400 / 700 = 2.00 per kWh.",
            ),
            q(
                "A total of 300.00 with a 10% discount applied becomes what?",
                (
                    opt("R$ 330.00"),
                    opt("R$ 270.00", correct=True),
                    opt("R$ 290.00"),
                    opt("R$ 30.00"),
                ),
                "300 * 0.90 = 270.00 (a 10% discount).",
            ),
        ),
        "From logic to clean, maintainable code": (
            q(
                "What does the DRY principle stand for?",
                (
                    opt("Don't Repeat Yourself", correct=True),
                    opt("Do Repeat Yearly"),
                    opt("Data Reads Yield"),
                    opt("Define, Run, Yield"),
                ),
                "DRY means avoid duplicated logic; extract it into one reusable place.",
            ),
            q(
                "Why prefer clear variable names like price_per_kwh over c?",
                (
                    opt("Longer names run faster"),
                    opt(
                        "A good name conveys intent and removes the need for a comment",
                        correct=True,
                    ),
                    opt("Short names cause syntax errors"),
                    opt("The interpreter requires long names"),
                ),
                "Readable names make code self-documenting and easier to maintain.",
            ),
            q(
                "Reducing deep nesting of if statements primarily lowers what?",
                (
                    opt("The file size on disk"),
                    opt("Cognitive complexity — how hard the code is to follow", correct=True),
                    opt("The number of variables"),
                    opt("The program's memory usage only"),
                ),
                "Shallow nesting and guard clauses lower cognitive complexity for human readers.",
            ),
        ),
    },
    final=(
        q(
            "Which flowchart symbol is the rounded terminator used for?",
            (
                opt("A decision"),
                opt("Start and End of the algorithm", correct=True),
                opt("A calculation"),
                opt("Reading input"),
            ),
            "The rounded terminator marks Start and End.",
        ),
        q(
            "In the problem-solving methodology, which comes BEFORE writing code?",
            (
                opt("Deploying to production"),
                opt("Finding the formula, defining variables and desk-checking", correct=True),
                opt("Measuring performance"),
                opt("Nothing; code comes first"),
            ),
            "Reasoning, variable definition and a desk-check all precede coding.",
        ),
        q(
            "Using = instead of == inside an if condition is an example of what?",
            (
                opt("A correct comparison"),
                opt("A common error: assignment where a comparison was meant", correct=True),
                opt("An indentation error"),
                opt("A division-by-zero error"),
            ),
            "= assigns; == compares — confusing them is a classic beginner bug.",
        ),
        q(
            "A desk-check of soma = soma + i for i in 1..3 (from 0) ends at which value?",
            (
                opt("3"),
                opt("6", correct=True),
                opt("9"),
                opt("1"),
            ),
            "0+1+2+3 = 6.",
        ),
        q(
            "If 100 kWh cost salary/7, the price of a single kWh is:",
            (
                opt("salary / 700", correct=True),
                opt("salary / 7"),
                opt("salary * 7"),
                opt("salary / 70"),
            ),
            "Dividing salary/7 across 100 kWh gives salary/700 per kWh.",
        ),
        q(
            "Which practice most improves maintainability of correct code?",
            (
                opt("Copy-pasting logic wherever it's needed"),
                opt("Clear names, small single-purpose functions, and no repetition", correct=True),
                opt("Using single-letter names to save space"),
                opt("Nesting conditionals as deeply as possible"),
            ),
            "Clear names, decomposition and DRY turn working logic into maintainable code.",
        ),
    ),
)
