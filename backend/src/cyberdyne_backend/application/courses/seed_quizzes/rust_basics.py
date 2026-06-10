"""Curated quiz questions for the Rust - Basics course (per-lesson checkpoints
plus a final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with Rust": (
            q(
                "In Rust, what is the default mutability of a variable bound with let?",
                (
                    opt("Mutable, and you add const to make it immutable"),
                    opt("Immutable by default, and you add mut to allow change", correct=True),
                    opt("Always mutable regardless of keywords"),
                    opt("Immutable, and it can never be changed under any circumstance"),
                ),
                "Variables are immutable by default in Rust; you add mut to allow them to change.",
            ),
            q(
                "What does the trailing ! mark in println! and vec! indicate?",
                (
                    opt("That the call is a macro", correct=True),
                    opt("That the function returns an error"),
                    opt("That the value is negated"),
                    opt("That the variable is mutable"),
                ),
                "The ! marks a macro, such as println! and vec!.",
            ),
            q(
                "What does shadowing let you do in Rust, as shown by let x = 5; let x = x + 1;?",
                (
                    opt("Reuse a name by declaring it again", correct=True),
                    opt("Mutate an immutable variable without mut"),
                    opt("Hide a variable from the compiler entirely"),
                    opt("Define two variables that share the same memory address"),
                ),
                "Shadowing lets you reuse a name by declaring it again, as in let x = 5; let x = x + 1;.",
            ),
        ),
        "Types & control flow": (
            q(
                "Because Rust is expression-based, what can if and match do that statements cannot?",
                (
                    opt("They can only be used at the top level of main"),
                    opt("They return values", correct=True),
                    opt("They run asynchronously"),
                    opt("They automatically allocate on the heap"),
                ),
                "Rust is expression-based, so if and match return values.",
            ),
            q(
                "What range of values does the range 0..5 cover?",
                (
                    opt("0 through 5 inclusive"),
                    opt("1 through 5 inclusive"),
                    opt("0 through 4, with 5 excluded", correct=True),
                    opt("Only the single value 5"),
                ),
                "The range 0..5 excludes 5, covering 0 through 4.",
            ),
            q(
                "What is the role of _ in a match expression?",
                (
                    opt("It is the catch-all arm, and match must be exhaustive", correct=True),
                    opt("It marks the match as a macro"),
                    opt("It declares a mutable binding"),
                    opt("It converts the matched value to a string"),
                ),
                "The _ is the catch-all arm; match must be exhaustive.",
            ),
        ),
        "Structs, enums & pattern matching": (
            q(
                "Where do methods like dist for a struct live in Rust?",
                (
                    opt("Inside the struct definition itself"),
                    opt("In an impl block", correct=True),
                    opt("In a separate trait that is always required"),
                    opt("In the main function"),
                ),
                "Methods go in an impl block for the type.",
            ),
            q(
                "What makes Rust enums powerful, as shown by the Shape enum?",
                (
                    opt("Each variant can hold different data", correct=True),
                    opt("They can only hold integer discriminants"),
                    opt("They are mutable by default"),
                    opt("They cannot be used with match"),
                ),
                "Rust enums are powerful because each variant can hold different data, such as Circle(f64) and Rect { w, h }.",
            ),
            q(
                "Why is match everywhere in Rust according to this lesson?",
                (
                    opt("Because Option<T> and Result<T, E> are just enums", correct=True),
                    opt("Because match is the only way to declare variables"),
                    opt("Because Rust has no if expression"),
                    opt("Because every struct must be matched before use"),
                ),
                "Option<T> and Result<T, E> are just enums, which is why match is everywhere in Rust.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about Rust is accurate based on the course?",
            (
                opt("It uses a garbage collector to manage memory"),
                opt(
                    "It focuses on safety and performance with errors caught at compile time",
                    correct=True,
                ),
                opt("It cannot catch data races"),
                opt("It has no build tool or package manager"),
            ),
            "Rust focuses on safety and performance with no garbage collector and errors caught at compile time.",
        ),
        q(
            "What is cargo in the Rust ecosystem?",
            (
                opt("A type used for fixed arrays"),
                opt("Its build tool and package manager", correct=True),
                opt("The macro that prints to the console"),
                opt("A keyword that makes a variable mutable"),
            ),
            "cargo is Rust's build tool and package manager, used with commands like cargo new and cargo run.",
        ),
        q(
            "Which keyword allows a variable to be changed after binding?",
            (
                opt("const"),
                opt("mut", correct=True),
                opt("let"),
                opt("static"),
            ),
            "You add mut to allow a variable to change, since variables are immutable by default.",
        ),
        q(
            "In the Shape enum example, how is the area of a Circle(r) computed in the match?",
            (
                opt("w * h"),
                opt("3.14 * r * r", correct=True),
                opt("r.sqrt()"),
                opt("r + r"),
            ),
            "The Circle(r) arm computes 3.14 * r * r, while the Rect arm computes w * h.",
        ),
        q(
            "Which control-flow construct creates an infinite loop in Rust?",
            (
                opt("for i in 0..5"),
                opt("while x < 10"),
                opt("loop", correct=True),
                opt("match n"),
            ),
            "loop creates an infinite loop, exited with break.",
        ),
    ),
)
