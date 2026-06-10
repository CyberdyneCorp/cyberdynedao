"""Curated quiz questions for the Python Course (per-lesson checkpoints plus a
final comprehensive quiz). Keys are the EXACT content-lesson titles; the seed
interleaves a checkpoint quiz after each content lesson."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Welcome to Python": (
            q(
                "According to the lesson, what defines code structure in Python?",
                (
                    opt("Curly braces around each block"),
                    opt("Indentation", correct=True),
                    opt("Semicolons at the end of lines"),
                    opt("A separate header file"),
                ),
                "The lesson states that indentation defines structure and there are no curly braces.",
            ),
            q(
                "What does the type(x) function tell you?",
                (
                    opt("The type of a value", correct=True),
                    opt("The length of a value"),
                    opt("Whether a value is true or false"),
                    opt("The memory address of a value"),
                ),
                "The lesson says print() shows a value and type(x) tells you its type.",
            ),
            q(
                "In the example, what do f-strings let you do inside curly braces?",
                (
                    opt("Drop in expressions", correct=True),
                    opt("Import other modules"),
                    opt("Define a new function"),
                    opt("Comment out a line"),
                ),
                "The comment notes that f-strings drop expressions in { }, as in welcome, {name}.",
            ),
        ),
        "Variables & Types": (
            q(
                "How does the lesson describe Python's typing?",
                (
                    opt("Statically typed with declarations"),
                    opt("Dynamically typed", correct=True),
                    opt("Untyped at runtime"),
                    opt("Strongly compiled ahead of time"),
                ),
                "The lesson says Python is dynamically typed: assign a value and the variable exists, no declaration needed.",
            ),
            q(
                "Which collection does the lesson recommend when you look things up by name?",
                (
                    opt("A list"),
                    opt("A dict", correct=True),
                    opt("A bool"),
                    opt("A float"),
                ),
                "The rule of thumb is a list for an ordered collection and a dict when you look things up by name.",
            ),
            q(
                "Given nums = [1, 2, 3], what does nums[-1] return?",
                (
                    opt("1"),
                    opt("3", correct=True),
                    opt("2"),
                    opt("An error"),
                ),
                "Indexing is 0-based and -1 refers to the last element, which is 3.",
            ),
        ),
        "How Python runs your code": (
            q(
                "When you run a .py file, what does Python compile it to first?",
                (
                    opt("Machine code"),
                    opt("Bytecode", correct=True),
                    opt("Assembly"),
                    opt("HTML"),
                ),
                "The lesson explains Python compiles the file to bytecode that a virtual machine then executes.",
            ),
            q(
                "How many spaces does the lesson use to group a block via indentation?",
                (
                    opt("2 spaces"),
                    opt("4 spaces", correct=True),
                    opt("8 spaces"),
                    opt("1 tab only"),
                ),
                "The lesson states indentation of 4 spaces groups a block.",
            ),
            q(
                "What does a comprehension let you do in one expressive line?",
                (
                    opt("Build a list", correct=True),
                    opt("Compile the file"),
                    opt("Import a module"),
                    opt("Define a class"),
                ),
                "The lesson shows a comprehension that builds a list of squares in one line.",
            ),
        ),
        "Control flow: if, for & while": (
            q(
                "In an if / elif / else chain, which branch runs?",
                (
                    opt("The last true one"),
                    opt("The first true one", correct=True),
                    opt("All true ones"),
                    opt("Only the else branch"),
                ),
                "The lesson says branches are tested top to bottom and the first true one runs.",
            ),
            q(
                "What does the break statement do inside a loop?",
                (
                    opt("Leaves the loop immediately", correct=True),
                    opt("Skips the rest of this pass and continues"),
                    opt("Restarts the loop from the beginning"),
                    opt("Pauses execution until input"),
                ),
                "The lesson states break leaves the loop immediately, while continue skips the rest of the current pass.",
            ),
            q(
                "When does the lesson suggest reaching for a while loop instead of a for loop?",
                (
                    opt("When you know exactly what you are iterating over"),
                    opt("When you loop until something changes", correct=True),
                    opt("When you only need to run the body once"),
                    opt("When you want to skip even numbers"),
                ),
                "The lesson advises using for when you know what you are iterating over and while when you loop until something changes.",
            ),
        ),
        "Run your first Python script": (
            q(
                "In the script, how is the average of scores computed?",
                (
                    opt("max(scores) / len(scores)"),
                    opt("sum(scores) / len(scores)", correct=True),
                    opt("min(scores) / len(scores)"),
                    opt("len(scores) / sum(scores)"),
                ),
                "The script prints the average as sum(scores) / len(scores) formatted to one decimal place.",
            ),
            q(
                "What does the comprehension passed = [s for s in scores if s >= 70] collect?",
                (
                    opt("Scores that are at least 70", correct=True),
                    opt("Scores below 70"),
                    opt("The highest score only"),
                    opt("The total of all scores"),
                ),
                "The comprehension keeps each score s where s is greater than or equal to 70, the passing threshold.",
            ),
            q(
                "Which function does the script use to get the highest score?",
                (
                    opt("min(scores)"),
                    opt("max(scores)", correct=True),
                    opt("sum(scores)"),
                    opt("len(scores)"),
                ),
                "The script prints the highest value with max(scores).",
            ),
        ),
    },
    final=(
        q(
            "What is the defining trait of Python introduced in this course?",
            (
                opt("Indentation defines structure", correct=True),
                opt("Curly braces define structure"),
                opt("Semicolons end every statement"),
                opt("Types must be declared before use"),
            ),
            "The course opens by stating that in Python indentation defines structure and there are no curly braces.",
        ),
        q(
            "Which statement about Python's type system is correct?",
            (
                opt("It is dynamically typed, so no declaration is needed", correct=True),
                opt("Every variable must declare its type first"),
                opt("Variables cannot change value once set"),
                opt("Only strings and ints are allowed"),
            ),
            "Python is dynamically typed: you assign a value and the variable exists without a declaration.",
        ),
        q(
            "How does Python execute a .py file?",
            (
                opt("It interprets the raw text with no intermediate step"),
                opt("It compiles to bytecode that a virtual machine executes", correct=True),
                opt("It translates directly to machine code you manage"),
                opt("It requires a manual compile step you run by hand"),
            ),
            "Python compiles the source to bytecode and a virtual machine executes it line by line.",
        ),
        q(
            "Inside a loop, what is the difference between break and continue?",
            (
                opt("break leaves the loop, continue skips to the next pass", correct=True),
                opt("break skips to the next pass, continue leaves the loop"),
                opt("Both leave the loop immediately"),
                opt("Both skip only even numbers"),
            ),
            "break leaves the loop immediately while continue skips the rest of the current pass and moves to the next one.",
        ),
        q(
            "Which collection does the course recommend for looking things up by name?",
            (
                opt("A list"),
                opt("A dict", correct=True),
                opt("A bool"),
                opt("A float"),
            ),
            "The course advises a dict when you look things up by name and a list for an ordered collection.",
        ),
    ),
)
