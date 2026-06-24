"""Curated quiz questions for the Programming Logic & Computational Thinking -
Intermediate course. Keys are the EXACT content-lesson titles; the seed
interleaves a checkpoint quiz after each content lesson plus a final
comprehensive quiz."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Conditionals: if / elif / else": (
            q(
                "When does the else branch run?",
                (
                    opt("Always, after the if"),
                    opt("Only when every preceding if/elif condition was false", correct=True),
                    opt("Only when the if condition is true"),
                    opt("Never; else is optional decoration"),
                ),
                "else runs when none of the conditions above it were true.",
            ),
            q(
                "Given nota = 8.0, what does the if nota >= 7 / elif nota >= 5 / else chain print?",
                (
                    opt("Pass", correct=True),
                    opt("Retake"),
                    opt("Fail"),
                    opt("Nothing"),
                ),
                "8.0 satisfies the first test (>= 7), so it prints Pass and skips the rest.",
            ),
            q(
                "In Python, what defines which statements belong inside an if block?",
                (
                    opt("Curly braces { }"),
                    opt("The indentation (leading spaces)", correct=True),
                    opt("A semicolon at the end"),
                    opt("The keyword end"),
                ),
                "Python uses indentation to delimit blocks.",
            ),
        ),
        "CODE LAB: a grading decision": (
            q(
                "In the lab's classify function, what does a grade of exactly 7.0 return?",
                (
                    opt("Pass", correct=True),
                    opt("Retake"),
                    opt("Fail"),
                    opt("An error"),
                ),
                "The test is grade >= 7, so 7.0 is inclusive and returns Pass.",
            ),
            q(
                "Why does the lab test boundary values like 5.0 and 7.0?",
                (
                    opt("To make the code longer"),
                    opt("Because boundaries are where off-by-one logic errors hide", correct=True),
                    opt("Because only boundaries can be asserted"),
                    opt("To increase the grade automatically"),
                ),
                "Edge/boundary values catch >= vs > mistakes that typical values miss.",
            ),
            q(
                "What would change if >= 7 were rewritten as > 7 ?",
                (
                    opt("Nothing changes"),
                    opt("A grade of exactly 7.0 would become Retake instead of Pass", correct=True),
                    opt("All grades would become Fail"),
                    opt("The function would crash"),
                ),
                "> 7 excludes 7.0, so the boundary grade flips from Pass to Retake.",
            ),
        ),
        "Loops: for and while": (
            q(
                "Which values does range(1, 6) produce?",
                (
                    opt("1 2 3 4 5 6"),
                    opt("1 2 3 4 5", correct=True),
                    opt("0 1 2 3 4 5"),
                    opt("1 6"),
                ),
                "range(1, 6) starts at 1 and stops BEFORE 6, giving 1 2 3 4 5.",
            ),
            q(
                "When is a while loop the better choice over a for loop?",
                (
                    opt("When you know exactly how many repetitions you need"),
                    opt(
                        "When you repeat as long as a condition stays true, count unknown",
                        correct=True,
                    ),
                    opt("When iterating a fixed range of numbers"),
                    opt("while loops are never useful"),
                ),
                "for fits a known count; while fits 'repeat until a condition changes'.",
            ),
            q(
                "What causes an infinite loop in a while statement?",
                (
                    opt("Using range() inside it"),
                    opt(
                        "The condition never becoming false (no progress toward the exit)",
                        correct=True,
                    ),
                    opt("Printing inside the loop"),
                    opt("Using a float counter"),
                ),
                "If nothing moves the loop toward its exit condition, it runs forever.",
            ),
        ),
        "CODE LAB: loops & accumulators (sum 1..n, list average)": (
            q(
                "What is an accumulator?",
                (
                    opt(
                        "A variable built up across loop iterations from a neutral start",
                        correct=True,
                    ),
                    opt("A function that sorts a list"),
                    opt("A type of conditional"),
                    opt("A way to read input"),
                ),
                "An accumulator (e.g. a running sum) starts neutral and is updated each pass.",
            ),
            q(
                "In the lab, summing 1..5 gives which total?",
                (
                    opt("10"),
                    opt("15", correct=True),
                    opt("5"),
                    opt("25"),
                ),
                "1+2+3+4+5 = 15, which also equals n*(n+1)//2 for n = 5.",
            ),
            q(
                "How does the lab compute an average from a list?",
                (
                    opt("By sorting then taking the middle value"),
                    opt(
                        "By dividing a running sum accumulator by a count accumulator", correct=True
                    ),
                    opt("By multiplying the first and last elements"),
                    opt("By calling input() repeatedly"),
                ),
                "It accumulates the sum and the count, then divides sum by count.",
            ),
        ),
        "Lists, vectors & matrices": (
            q(
                "What index accesses the FIRST element of a list named grades?",
                (
                    opt("grades[1]"),
                    opt("grades[0]", correct=True),
                    opt("grades[-1]"),
                    opt("grades[first]"),
                ),
                "List indexing starts at 0, so the first element is grades[0].",
            ),
            q(
                "How is a matrix represented in Python?",
                (
                    opt("As a single number"),
                    opt("As a list of lists (rows and columns)", correct=True),
                    opt("As a string of digits"),
                    opt("As a boolean"),
                ),
                "A matrix is a list of lists; mat[i][j] is row i, column j.",
            ),
            q(
                "What is the usual way to visit every cell of a matrix?",
                (
                    opt("A single while loop"),
                    opt(
                        "Nested loops: an outer loop over rows, an inner over columns", correct=True
                    ),
                    opt("Recursion only"),
                    opt("A conditional"),
                ),
                "Nested loops walk rows in the outer loop and columns in the inner loop.",
            ),
        ),
        "CODE LAB: functions — organizing logic": (
            q(
                "Which keyword defines a function in Python?",
                (
                    opt("func"),
                    opt("def", correct=True),
                    opt("function"),
                    opt("lambda only"),
                ),
                "def creates a function.",
            ),
            q(
                "Why must the lab's fuel_report receive distance and litres as arguments?",
                (
                    opt("To make the call shorter"),
                    opt(
                        "A function cannot see module-level variables; it needs values passed in",
                        correct=True,
                    ),
                    opt("Because functions can only take two arguments"),
                    opt("Because return requires arguments"),
                ),
                "In the sandbox a user function can't read module globals, so values are passed as arguments.",
            ),
            q(
                "What does the return statement do?",
                (
                    opt("Prints a value to the screen"),
                    opt("Sends a value back to where the function was called", correct=True),
                    opt("Reads input from the user"),
                    opt("Ends the whole program"),
                ),
                "return hands a value back to the caller; here it returns a (consumption, label) tuple.",
            ),
        ),
    },
    final=(
        q(
            "In an if / elif / else chain, how many of the blocks run for a single value?",
            (
                opt("All of them"),
                opt("Exactly one (the first matching branch)", correct=True),
                opt("None"),
                opt("At least two"),
            ),
            "The first true condition's block runs; the rest are skipped.",
        ),
        q(
            "Which loop is the safer choice when the number of repetitions is known?",
            (
                opt("while, because it never ends"),
                opt("for, because it updates the counter for you", correct=True),
                opt("Neither can do a known count"),
                opt("Both are equally unsafe"),
            ),
            "A for over a range advances the counter automatically, avoiding infinite loops.",
        ),
        q(
            "Summing 1+2+3 with an accumulator that starts at 0 yields what?",
            (
                opt("5"),
                opt("6", correct=True),
                opt("0"),
                opt("3"),
            ),
            "0+1+2+3 = 6.",
        ),
        q(
            "What does mat[1][2] refer to in a list-of-lists matrix?",
            (
                opt("Row 2, column 1"),
                opt("Row 1, column 2", correct=True),
                opt("The whole second row"),
                opt("The number 12"),
            ),
            "The first index is the row, the second is the column: row 1, column 2.",
        ),
        q(
            "What is the main benefit of putting logic in a function?",
            (
                opt("It makes the program run on more computers"),
                opt("Define the logic once and reuse it, with one place to fix bugs", correct=True),
                opt("It removes the need for variables"),
                opt("It automatically sorts data"),
            ),
            "Functions avoid repetition and centralise the logic, aiding reuse and maintenance.",
        ),
        q(
            "What must a while loop change each pass to avoid running forever?",
            (
                opt("The print message"),
                opt("Something that moves the condition toward becoming false", correct=True),
                opt("The function name"),
                opt("The list length only"),
            ),
            "Progress toward the exit condition (e.g. incrementing an index) prevents an infinite loop.",
        ),
    ),
)
