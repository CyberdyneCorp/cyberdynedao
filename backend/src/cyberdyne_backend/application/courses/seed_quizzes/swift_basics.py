from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with Swift": (
            q(
                "Which keyword should you reach for by default to declare a value in Swift?",
                (
                    opt("var, because most values change"),
                    opt("let, because it declares an immutable constant", correct=True),
                    opt("const, the standard Swift keyword"),
                    opt("def, used for definitions"),
                ),
                "The lesson says prefer let by default; it declares an immutable constant and use var only when the value changes.",
            ),
            q(
                "What does the expression \\(name) do inside a Swift string literal?",
                (
                    opt("It escapes the parentheses as literal text"),
                    opt(
                        "It performs string interpolation, inserting the value of name",
                        correct=True,
                    ),
                    opt("It declares a new optional named name"),
                    opt("It calls a function named name"),
                ),
                "The lesson shows print(\\(name) is \\(age)) producing Ada is 36, which is string interpolation.",
            ),
            q(
                "What is true about types in Swift according to the lesson?",
                (
                    opt("Every variable must always have an explicit type annotation"),
                    opt(
                        "Types are inferred, but you can annotate with : Type when you want",
                        correct=True,
                    ),
                    opt("Swift has no concept of types"),
                    opt("Type annotations require semicolons"),
                ),
                "The lesson states types are inferred (name is a String) but you can annotate with : Type.",
            ),
        ),
        "Optionals: Swift's nil-safety": (
            q(
                "How is the type of a value that might be missing written in Swift?",
                (
                    opt("T! the force type"),
                    opt("T? an Optional type", correct=True),
                    opt("Maybe<T>"),
                    opt("nil T"),
                ),
                "The lesson says a value that might be missing has an Optional type written T?.",
            ),
            q(
                "What does the ?? operator do in the line let shown = nickname ?? Guest?",
                (
                    opt("It force-unwraps nickname"),
                    opt("It supplies a default value when nickname is nil", correct=True),
                    opt("It compares nickname to Guest for equality"),
                    opt("It declares nickname as optional"),
                ),
                "The lesson shows ?? supplies a default value, so shown becomes Guest when nickname is nil.",
            ),
            q(
                "Why does the lesson recommend avoiding force-unwrap with name!?",
                (
                    opt("It is slower than optional chaining"),
                    opt("It crashes if the value is nil", correct=True),
                    opt("It is not valid Swift syntax"),
                    opt("It permanently converts the value to non-optional"),
                ),
                "The lesson warns to avoid force-unwrap (name!) because it crashes if the value is nil.",
            ),
        ),
        "Control flow, functions & collections": (
            q(
                "What does the closed range expression for i in 1...5 iterate over?",
                (
                    opt("1, 2, 3, 4 (excluding 5)"),
                    opt("1, 2, 3, 4, 5 (including 5)", correct=True),
                    opt("0, 1, 2, 3, 4"),
                    opt("only the values 1 and 5"),
                ),
                "The lesson notes 1...5 is a closed range producing 1,2,3,4,5.",
            ),
            q(
                "In the closure let square = { (x: Int) -> Int in x * x }, what does square(5) return?",
                (
                    opt("10"),
                    opt("25", correct=True),
                    opt("5"),
                    opt("125"),
                ),
                "The closure squares its argument, so square(5) returns 25.",
            ),
            q(
                "What does nums.map { $0 * 2 } produce for the array [1, 2, 3, 4]?",
                (
                    opt("[1, 2, 3, 4]"),
                    opt("[2, 4, 6, 8]", correct=True),
                    opt("[1, 4, 9, 16]"),
                    opt("10"),
                ),
                "The lesson shows map doubling each element where $0 is the first arg, yielding [2,4,6,8].",
            ),
        ),
    },
    final=(
        q(
            "Which statement best describes Swift as introduced in the course?",
            (
                opt("A scripting language only for the web"),
                opt(
                    "A safe, fast, expressive language primarily for Apple platforms but also server-side",
                    correct=True,
                ),
                opt("A language that requires semicolons after every statement"),
                opt("A language with no type inference"),
            ),
            "The first lesson describes Swift as safe, fast, expressive, primarily for Apple platforms but also server-side.",
        ),
        q(
            "Which unwrapping form gives an early exit when the optional is nil and keeps the value non-optional afterward?",
            (
                opt("if let"),
                opt("guard let ... else { return }", correct=True),
                opt("the ?? operator"),
                opt("force-unwrap with !"),
            ),
            "The lesson shows guard let name = nickname else { return } early-exits on nil and name is non-optional afterward.",
        ),
        q(
            "What happens with optional chaining like user?.profile?.email?",
            (
                opt("It crashes if any part is nil"),
                opt("It stops at the first nil", correct=True),
                opt("It supplies a default value automatically"),
                opt("It forces every value to be unwrapped"),
            ),
            "The lesson states optional chaining stops at the first nil.",
        ),
        q(
            "Which of these is declared as a Dictionary in the collections lesson?",
            (
                opt("[1, 2, 3]"),
                opt('["name": "Ada"]', correct=True),
                opt("nums.append(4)"),
                opt("nums.map { $0 * 2 }"),
            ),
            "The lesson shows let user = [name: Ada] as a Dictionary, while [1, 2, 3] is an Array.",
        ),
        q(
            "Which functions are described as taking closures and being everywhere in Swift?",
            (
                opt("print, append, and return"),
                opt("map, filter, and reduce", correct=True),
                opt("let, var, and guard"),
                opt("if, switch, and for"),
            ),
            "The lesson says map, filter, and reduce take closures and are everywhere in Swift.",
        ),
    ),
)
