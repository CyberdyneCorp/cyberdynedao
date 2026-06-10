"""Curated quiz spec for the 'c-basics' course (per-lesson checkpoints plus a
final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with C": (
            q(
                "According to the lesson, why are Unix, Linux, and most language runtimes written in C?",
                (
                    opt("Because C is an interpreted language that needs no compiler"),
                    opt("Because C maps closely to how the machine actually works", correct=True),
                    opt("Because C is dynamically typed and very flexible"),
                    opt("Because C runs only inside a virtual machine"),
                ),
                "The lesson describes C as a small, compiled, statically-typed language that maps closely to how the machine works.",
            ),
            q(
                "In the hello program, what does the main function return and what does the value mean?",
                (
                    opt("It returns a double, and the value is the runtime in seconds"),
                    opt("It returns void, so no value is produced"),
                    opt("It returns an int, and 0 means success", correct=True),
                    opt("It returns a char, and A means success"),
                ),
                "main is the entry point that returns an int, and returning 0 means success.",
            ),
            q(
                "What does the -Wall flag do when compiling with gcc, per the lesson?",
                (
                    opt("It turns on warnings, which you should always keep on", correct=True),
                    opt("It links all available system libraries"),
                    opt("It walls off memory to prevent leaks"),
                    opt("It writes all output to a log file"),
                ),
                "The lesson says -Wall turns on warnings and advises always keeping it on.",
            ),
        ),
        "Types, variables & operators": (
            q(
                "What is the result of the integer division 7 / 2 in C according to the lesson?",
                (
                    opt("3.5"),
                    opt("4"),
                    opt("3, because integer division truncates", correct=True),
                    opt("It is a compile error"),
                ),
                "The lesson warns that integer division truncates, so 7 / 2 is 3, not 3.5.",
            ),
            q(
                "Which printf format specifier is used for a double value?",
                (
                    opt("%d"),
                    opt("%c"),
                    opt("%f", correct=True),
                    opt("%s"),
                ),
                "The lesson maps %f to double, %d to int, %c to char, and %s to strings.",
            ),
            q(
                "What does declaring a variable with const, as in const int MAX = 100, mean?",
                (
                    opt("It can be reassigned freely at any time"),
                    opt("It cannot be reassigned", correct=True),
                    opt("It must always be a floating point value"),
                    opt("It is automatically a single character"),
                ),
                "The lesson notes that a const variable cannot be reassigned.",
            ),
        ),
        "Control flow & functions": (
            q(
                "In a C switch statement, what is the purpose of break as shown in the lesson?",
                (
                    opt("It exits the entire program immediately"),
                    opt("It stops fall-through to the next case", correct=True),
                    opt("It restarts the switch from the top"),
                    opt("It declares a default case"),
                ),
                "The lesson comments that break stops fall-through in a switch.",
            ),
            q(
                "How does C pass arguments to functions, according to the lesson?",
                (
                    opt("By reference, so changes affect the caller"),
                    opt("By value, so the function gets a copy", correct=True),
                    opt("By name, resolving each use lazily"),
                    opt("By pointer always, even for plain ints"),
                ),
                "C passes arguments by value, so the function gets a copy and changes do not affect the caller's variable.",
            ),
            q(
                "Which loop is described as having a body that runs at least once?",
                (
                    opt("The for loop"),
                    opt("The while loop"),
                    opt("The do-while loop", correct=True),
                    opt("The switch statement"),
                ),
                "The lesson labels the do { ... } while (...) construct as a body that runs at least once.",
            ),
        ),
    },
    final=(
        q(
            "Which statement best describes C as introduced in this course?",
            (
                opt("A large, interpreted, dynamically-typed language"),
                opt(
                    "A small, compiled, statically-typed language close to the machine",
                    correct=True,
                ),
                opt("A garbage-collected scripting language for the web"),
                opt("A language that runs only inside a virtual machine"),
            ),
            "The course presents C as a small, compiled, statically-typed language that maps closely to the machine.",
        ),
        q(
            "What is the correct printf specifier for printing an int, a double, and a char in that order?",
            (
                opt("%c, %d, %f"),
                opt("%d, %f, %c", correct=True),
                opt("%f, %c, %d"),
                opt("%s, %p, %d"),
            ),
            "The lesson maps %d to int, %f to double, and %c to char.",
        ),
        q(
            "Because C passes arguments by value, how do you change a caller's variable inside a function?",
            (
                opt("You return the value and the caller is updated automatically"),
                opt("You pass a pointer to it", correct=True),
                opt("You declare the parameter const"),
                opt("You cannot ever change a caller's variable"),
            ),
            "The course notes that to change the caller's data you pass a pointer.",
        ),
        q(
            "What does the value 0 returned from main signify?",
            (
                opt("An error occurred"),
                opt("Success", correct=True),
                opt("The number of arguments received"),
                opt("That warnings were enabled"),
            ),
            "Returning 0 from main means success, as the hello program's comment states.",
        ),
        q(
            "Which evaluation of 7 / 2 and its fix are correct per the course?",
            (
                opt("7 / 2 is 3.5; no fix is needed"),
                opt("7 / 2 is 3 because of truncation; use a double to get 3.5", correct=True),
                opt("7 / 2 is 4 due to rounding; cast to int to fix"),
                opt("7 / 2 is a compile error; add a semicolon"),
            ),
            "Integer division truncates so 7 / 2 is 3, and using a double yields 3.5.",
        ),
    ),
)
