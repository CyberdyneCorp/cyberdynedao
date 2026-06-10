from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Why TypeScript": (
            q(
                "What is TypeScript best described as?",
                (
                    opt("A replacement for JavaScript that runs in the browser directly"),
                    opt("JavaScript plus static types", correct=True),
                    opt("A runtime that interprets JavaScript faster"),
                    opt("A CSS preprocessor for typed stylesheets"),
                ),
                "TypeScript is JavaScript plus static types.",
            ),
            q(
                "When does the TypeScript compiler catch type mistakes?",
                (
                    opt("Before the code runs", correct=True),
                    opt("Only at runtime when the error is hit"),
                    opt("After deployment to production"),
                    opt("Never, it only formats the code"),
                ),
                "The compiler tsc catches type mistakes before your code runs.",
            ),
            q(
                "After type-checking, what does tsc produce?",
                (
                    opt("A binary executable"),
                    opt("Plain JS with the types erased", correct=True),
                    opt("A WebAssembly module"),
                    opt("A typed JSON schema file"),
                ),
                "tsc erases the types to produce plain JavaScript.",
            ),
        ),
        "Basic types & interfaces": (
            q(
                "Which type is the safe alternative to any that must be narrowed first?",
                (
                    opt("unknown", correct=True),
                    opt("void"),
                    opt("never"),
                    opt("object"),
                ),
                "unknown is the safe any that you must narrow before using.",
            ),
            q(
                "What does the readonly modifier on an interface property mean?",
                (
                    opt("It cannot be reassigned", correct=True),
                    opt("It is optional and may be omitted"),
                    opt("It is only visible inside the interface"),
                    opt("It must always be a string"),
                ),
                "A readonly property cannot be reassigned.",
            ),
            q(
                "How does an object qualify as fitting an interface in TypeScript?",
                (
                    opt("It must explicitly declare it implements the interface"),
                    opt("It must be created with the new keyword"),
                    opt("If it has the required properties (structural typing)", correct=True),
                    opt("It must be frozen with Object.freeze"),
                ),
                "TypeScript uses structural typing: having the required properties is enough.",
            ),
        ),
        "Functions & union types": (
            q(
                "What does a union type like string | number allow?",
                (
                    opt("Either of several types", correct=True),
                    opt("Only values that are both a string and a number"),
                    opt("Exactly one fixed string value"),
                    opt("Any type at all, like any"),
                ),
                "A union allows a value to be any one of several types.",
            ),
            q(
                "What does the literal type Direction = up | down restrict values to?",
                (
                    opt("Any string"),
                    opt("Only those two exact strings", correct=True),
                    opt("Any string or number"),
                    opt("Only numbers 0 and 1"),
                ),
                "Literal types restrict a value to the exact listed values.",
            ),
            q(
                "In the lesson, what keeps function call sites clean?",
                (
                    opt("Optional and default parameters", correct=True),
                    opt("Marking every parameter readonly"),
                    opt("Using any for all parameters"),
                    opt("Returning void from every function"),
                ),
                "Optional and default parameters keep call sites clean.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about adopting TypeScript is true?",
            (
                opt("You must rewrite all JavaScript at once"),
                opt(
                    "All valid JavaScript is valid TypeScript, so you adopt it gradually",
                    correct=True,
                ),
                opt("TypeScript cannot run any existing JavaScript"),
                opt("Types are kept in the compiled output"),
            ),
            "All valid JavaScript is valid TypeScript, allowing gradual adoption.",
        ),
        q(
            "Which annotation syntax is used to give a variable a type?",
            (
                opt("let age = number"),
                opt("let age: number", correct=True),
                opt("let age as number"),
                opt("number age"),
            ),
            "You annotate with the colon type syntax, such as let age: number.",
        ),
        q(
            "What is the difference between any and unknown?",
            (
                opt("any is safe and unknown opts out of checking"),
                opt("They are identical in behavior"),
                opt("unknown is the safe any and must be narrowed before use", correct=True),
                opt("unknown cannot hold any value"),
            ),
            "unknown is the safe any that must be narrowed before you can use it.",
        ),
        q(
            "Which is a valid type alias from the lessons?",
            (
                opt("type ID = string | number", correct=True),
                opt("interface ID = string | number"),
                opt("type ID: string | number"),
                opt("alias ID = string | number"),
            ),
            "type aliases use the form type ID = string | number.",
        ),
        q(
            "How does a literal union type like up | down help functions?",
            (
                opt("It lets the function accept any string argument"),
                opt(
                    "It restricts arguments to the exact listed values, rejecting others",
                    correct=True,
                ),
                opt("It disables type checking for that parameter"),
                opt("It makes the parameter optional"),
            ),
            "Literal types restrict arguments to exact values, so other strings are errors.",
        ),
    ),
)
