"""Curated quiz questions for the matlab-basics course (per-lesson checkpoints
plus a final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Welcome to MATLAB": (
            q(
                "What single idea is MATLAB built around?",
                (
                    opt("Everything is an object"),
                    opt("Everything is a matrix", correct=True),
                    opt("Everything is a function"),
                    opt("Everything is a string"),
                ),
                "MATLAB (Matrix Laboratory) treats everything as a matrix, so a single number is a 1x1 matrix.",
            ),
            q(
                "What does a trailing semicolon do at the end of a MATLAB line?",
                (
                    opt("It suppresses the output but still runs the line", correct=True),
                    opt("It stops the line from running"),
                    opt("It starts a comment"),
                    opt("It transposes the result"),
                ),
                "A trailing ; hides the result but still executes the line, keeping the Command Window tidy.",
            ),
            q(
                "Which command opens the full documentation page for a function such as sin?",
                (
                    opt("help sin"),
                    opt("doc sin", correct=True),
                    opt("info sin"),
                    opt("man sin"),
                ),
                "doc sin opens the full documentation page, while help sin only prints quick docs.",
            ),
        ),
        "Variables & Matrices": (
            q(
                "How do you separate rows when building a matrix literal in MATLAB?",
                (
                    opt("With semicolons", correct=True),
                    opt("With spaces"),
                    opt("With commas"),
                    opt("With colons"),
                ),
                "Spaces or commas separate columns, while semicolons separate rows.",
            ),
            q(
                "What index refers to the first element of a vector in MATLAB?",
                (
                    opt("0"),
                    opt("1", correct=True),
                    opt("-1"),
                    opt("end"),
                ),
                "MATLAB indices are 1-based, so v(1) is the first element.",
            ),
            q(
                "What is the difference between * and .* in MATLAB?",
                (
                    opt("* is element-wise and .* is matrix multiplication"),
                    opt("* is matrix multiplication and .* is element-wise", correct=True),
                    opt("They are identical operators"),
                    opt("* transposes and .* multiplies"),
                ),
                "* performs matrix multiplication while .* performs element-wise multiplication.",
            ),
        ),
        "How a MATLAB script runs": (
            q(
                "In what order do the statements in a MATLAB script execute?",
                (
                    opt("Top to bottom", correct=True),
                    opt("Bottom to top"),
                    opt("Starting from a main function"),
                    opt("In a random order"),
                ),
                "A script is a .m file of statements that execute top to bottom, sharing the Command Window workspace.",
            ),
            q(
                "Which function prints a value formatted in a C-style way in MATLAB?",
                (
                    opt("disp"),
                    opt("fprintf", correct=True),
                    opt("print"),
                    opt("echo"),
                ),
                "fprintf does formatted, C-style printing, while disp prints one value with no name.",
            ),
            q(
                "How does a function differ from a script regarding the workspace?",
                (
                    opt("A function shares the script workspace"),
                    opt("A function gets its own workspace and takes inputs", correct=True),
                    opt("A function cannot return a value"),
                    opt("A function runs bottom to top"),
                ),
                "A script shares your workspace, but a function gets its own workspace and takes inputs.",
            ),
        ),
        "Control flow: if, for & while": (
            q(
                "What keyword closes every if, for, and while block in MATLAB?",
                (
                    opt("end", correct=True),
                    opt("done"),
                    opt("stop"),
                    opt("close"),
                ),
                "MATLAB groups every block with the keyword end; indenting is style, not syntax.",
            ),
            q(
                "What does the break statement do inside a loop?",
                (
                    opt("Skips the rest of this pass and jumps to the next one"),
                    opt("Leaves the loop immediately", correct=True),
                    opt("Restarts the loop from the beginning"),
                    opt("Pauses execution until input"),
                ),
                "break leaves the loop immediately, while continue skips the rest of the current pass.",
            ),
            q(
                "Which operator means not equal in a MATLAB condition?",
                (
                    opt("!="),
                    opt("~=", correct=True),
                    opt("<>"),
                    opt("=/="),
                ),
                "MATLAB uses ~= for not equal, along with == for equal and && and || for and and or.",
            ),
        ),
        "Run your first script": (
            q(
                "In the script, what does B = A' compute?",
                (
                    opt("The transpose of A", correct=True),
                    opt("The inverse of A"),
                    opt("The element-wise square of A"),
                    opt("A copy of A unchanged"),
                ),
                "The apostrophe operator transposes a matrix, so B = A' is the transpose of A.",
            ),
            q(
                "What does the trace function return in the script?",
                (
                    opt("The sum of the diagonal", correct=True),
                    opt("The product of all elements"),
                    opt("The largest element"),
                    opt("The number of rows"),
                ),
                "trace(C) returns the sum of the diagonal of C.",
            ),
            q(
                "Why does A .* B differ from A * B in the script comparison?",
                (
                    opt(".* is element-wise while * is matrix multiplication", correct=True),
                    opt(".* transposes while * multiplies"),
                    opt("They are the same and never differ"),
                    opt(".* is matrix multiplication while * is element-wise"),
                ),
                "A * B is matrix multiplication while A .* B is element-wise, which can error on mismatched shapes.",
            ),
        ),
    },
    final=(
        q(
            "What core concept does MATLAB build everything around?",
            (
                opt("Linked lists"),
                opt("The matrix", correct=True),
                opt("Hash maps"),
                opt("Pointers"),
            ),
            "MATLAB is built around the idea that everything is a matrix.",
        ),
        q(
            "At what number does MATLAB start indexing?",
            (
                opt("0"),
                opt("1", correct=True),
                opt("-1"),
                opt("Any value you choose"),
            ),
            "MATLAB indices are 1-based, so the first element is at index 1.",
        ),
        q(
            "Which operator performs element-wise multiplication in MATLAB?",
            (
                opt("*"),
                opt(".*", correct=True),
                opt("x"),
                opt("./"),
            ),
            ".* is element-wise multiplication, while * is matrix multiplication.",
        ),
        q(
            "What keyword must close every if, for, and while block?",
            (
                opt("end", correct=True),
                opt("fi"),
                opt("done"),
                opt("stop"),
            ),
            "Every if, for, and while block in MATLAB is closed with its own end.",
        ),
        q(
            "Which function gives formatted C-style printing in MATLAB?",
            (
                opt("disp"),
                opt("fprintf", correct=True),
                opt("println"),
                opt("write"),
            ),
            "fprintf does formatted, C-style printing of values.",
        ),
    ),
)
