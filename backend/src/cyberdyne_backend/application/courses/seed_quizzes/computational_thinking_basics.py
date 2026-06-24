"""Curated quiz questions for the Programming Logic & Computational Thinking -
Basics course. Keys are the EXACT content-lesson titles; the seed interleaves a
checkpoint quiz after each content lesson plus a final comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is programming logic?": (
            q(
                "What is programming logic, fundamentally?",
                (
                    opt("A specific programming language you must memorise"),
                    opt(
                        "The skill of organising a solution as an ordered sequence of steps a computer can execute",
                        correct=True,
                    ),
                    opt("A tool that fixes bugs automatically"),
                    opt("The fastest way to type code"),
                ),
                "Logic is about reasoning out clear ordered steps before, and independent of, any language.",
            ),
            q(
                "In the input → processing → output model, which is the OUTPUT for 'compute average fuel use'?",
                (
                    opt("The distance and litres"),
                    opt("The formula distance / litres"),
                    opt("The result shown, e.g. 12 km/l", correct=True),
                    opt("The name of the program"),
                ),
                "Output is the final result presented to the user; distance/litres are input and the formula is processing.",
            ),
            q(
                "What is the 'golden rule' for knowing you're ready to write code?",
                (
                    opt("You have memorised the language syntax"),
                    opt("You can explain the solution in simple steps to a person", correct=True),
                    opt("You have the fastest computer available"),
                    opt("You have written at least one program before"),
                ),
                "If you can't explain it in simple steps, you don't yet understand the solution well enough to code it.",
            ),
        ),
        "The four pillars of computational thinking": (
            q(
                "Which pillar means breaking a big problem into smaller, solvable parts?",
                (
                    opt("Abstraction"),
                    opt("Decomposition", correct=True),
                    opt("Pattern recognition"),
                    opt("Algorithms"),
                ),
                "Decomposition splits a large problem into approachable pieces.",
            ),
            q(
                "What does abstraction do?",
                (
                    opt("Repeats code several times"),
                    opt("Keeps what matters and ignores the irrelevant detail", correct=True),
                    opt("Counts how many times a loop runs"),
                    opt("Always sorts the data first"),
                ),
                "Abstraction keeps the essentials and hides detail, like a map showing only the roads you need.",
            ),
            q(
                "Recognising that three reports all 'average a list of numbers' is an example of which pillar?",
                (
                    opt("Pattern recognition", correct=True),
                    opt("Decomposition"),
                    opt("Abstraction"),
                    opt("Debugging"),
                ),
                "Spotting a repeated structure you can reuse is pattern recognition.",
            ),
        ),
        "Algorithms: input → processing → output": (
            q(
                "What is an algorithm?",
                (
                    opt("A finite sequence of steps that solves a problem", correct=True),
                    opt("A type of variable"),
                    opt("A specific Python keyword"),
                    opt("A way to store data in memory"),
                ),
                "An algorithm is a finite, ordered sequence of steps that solves a problem.",
            ),
            q(
                "What does the IPO acronym stand for?",
                (
                    opt("Integer, Pointer, Object"),
                    opt("Input, Processing, Output", correct=True),
                    opt("Iterate, Print, Output"),
                    opt("Input, Print, Order"),
                ),
                "Almost every program follows Input → Processing → Output.",
            ),
            q(
                "What's the recommended first move when facing a new problem?",
                (
                    opt("Start typing code immediately"),
                    opt(
                        "Name the inputs, find the processing formula, and state the output",
                        correct=True,
                    ),
                    opt("Pick the programming language"),
                    opt("Search for an existing answer online"),
                ),
                "Settling input, processing and output first makes writing the code almost mechanical.",
            ),
        ),
        "Variables, types & operators": (
            q(
                "Which type would you use to store a person's weight like 87.4?",
                (
                    opt("int"),
                    opt("str"),
                    opt("float", correct=True),
                    opt("bool"),
                ),
                "Numbers with decimals are floats; weight = 87.4 is a float.",
            ),
            q(
                "What does the // operator compute?",
                (
                    opt("True division, e.g. 10 // 4 = 2.5"),
                    opt("Floor (integer) division, e.g. 10 // 4 = 2", correct=True),
                    opt("The remainder, e.g. 10 // 4 = 2"),
                    opt("A power, e.g. 10 // 4 = 10000"),
                ),
                "// is floor division: 10 // 4 is 2 (it drops the fractional part).",
            ),
            q(
                "What is the difference between = and == ?",
                (
                    opt("They are identical"),
                    opt("= assigns a value, == compares two values", correct=True),
                    opt("= compares, == assigns"),
                    opt("== is only for strings"),
                ),
                "= stores a value in a variable; == tests whether two values are equal.",
            ),
        ),
        "CODE LAB: your first program (fuel consumption)": (
            q(
                "In the lab, how is average fuel consumption computed?",
                (
                    opt("litres / distance"),
                    opt("distance / litres", correct=True),
                    opt("distance * litres"),
                    opt("distance - litres"),
                ),
                "Consumption in km/l is distance divided by litres; 300 / 25 = 12.",
            ),
            q(
                "Why does the lab assign distance = 300.0 instead of calling input()?",
                (
                    opt("Because input() is faster"),
                    opt(
                        "So the lab runs unattended; the sandbox forbids input()",
                        correct=True,
                    ),
                    opt("Because 300 is the only valid distance"),
                    opt("Because float values cannot be read with input()"),
                ),
                "Labs use literal example values so they run without waiting for user input.",
            ),
            q(
                "What does the assert average == 12.0 line do?",
                (
                    opt("Prints the average"),
                    opt(
                        "Checks the computed result matches the expected value, failing loudly otherwise",
                        correct=True,
                    ),
                    opt("Converts the average to an integer"),
                    opt("Reads a new value from the user"),
                ),
                "assert verifies the logic; if 300/25 were not 12.0 the program would raise an error.",
            ),
        ),
        "CODE LAB: arithmetic & percentages (10% raise/discount)": (
            q(
                "To increase a value by 10%, what do you multiply by?",
                (
                    opt("0.90"),
                    opt("1.10", correct=True),
                    opt("0.10"),
                    opt("10"),
                ),
                "A 10% raise is *1.10 because 100% + 10% = 1 + 0.10 = 1.10.",
            ),
            q(
                "To apply a 10% discount, what do you multiply by?",
                (
                    opt("1.10"),
                    opt("0.90", correct=True),
                    opt("0.10"),
                    opt("0.99"),
                ),
                "A 10% discount is *0.90 because 100% - 10% = 1 - 0.10 = 0.90.",
            ),
            q(
                "In the lab, applying a 15% raise to 200 gives which value?",
                (
                    opt("215.0"),
                    opt("230.0", correct=True),
                    opt("170.0"),
                    opt("300.0"),
                ),
                "200 * (1 + 15/100) = 200 * 1.15 = 230.0.",
            ),
        ),
    },
    final=(
        q(
            "Which sequence correctly orders the IPO model?",
            (
                opt("Output → Processing → Input"),
                opt("Input → Processing → Output", correct=True),
                opt("Processing → Input → Output"),
                opt("Input → Output → Processing"),
            ),
            "An algorithm receives input, processes it, then produces output.",
        ),
        q(
            "Which list correctly names the four pillars of computational thinking?",
            (
                opt(
                    "Decomposition, pattern recognition, abstraction, algorithms",
                    correct=True,
                ),
                opt("Compile, run, test, deploy"),
                opt("Input, output, loop, branch"),
                opt("Variables, types, operators, functions"),
            ),
            "The four pillars are decomposition, pattern recognition, abstraction and algorithms.",
        ),
        q(
            "Which Python type holds a true/false value?",
            (
                opt("int"),
                opt("float"),
                opt("bool", correct=True),
                opt("str"),
            ),
            "A boolean (bool) holds True or False.",
        ),
        q(
            "What is the result of 2 ** 3 ?",
            (
                opt("6"),
                opt("8", correct=True),
                opt("9"),
                opt("5"),
            ),
            "** is power: 2 to the 3rd is 8.",
        ),
        q(
            "A car travels 180 km on 15 litres. What is its consumption in km/l?",
            (
                opt("10"),
                opt("12", correct=True),
                opt("15"),
                opt("195"),
            ),
            "180 / 15 = 12 km/l.",
        ),
        q(
            "What does the golden rule of programming logic emphasise?",
            (
                opt("Memorising syntax before anything else"),
                opt("Explaining the solution in clear simple steps first", correct=True),
                opt("Writing as much code as possible"),
                opt("Avoiding variables altogether"),
            ),
            "Clear step-by-step reasoning comes before, and drives, the code.",
        ),
    ),
)
