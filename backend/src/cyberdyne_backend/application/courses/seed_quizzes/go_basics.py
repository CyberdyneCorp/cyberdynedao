"""Curated quiz spec for the 'go-basics' course (per-lesson checkpoints plus a
final comprehensive quiz). Keys are the EXACT content-lesson titles."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with Go": (
            q(
                "According to the lesson, which package is the entry point of a Go program?",
                (
                    opt("package entry"),
                    opt("package start"),
                    opt("package main", correct=True),
                    opt("package init"),
                ),
                "The lesson states that every file belongs to a package and main is the entry point.",
            ),
            q(
                "What does the := operator do in Go?",
                (
                    opt("It compares two values for equality"),
                    opt("It declares a variable and infers its type", correct=True),
                    opt("It imports a package by alias"),
                    opt("It formats code the way gofmt would"),
                ),
                "The lesson shows := declares and infers, as in name := 'Ada'.",
            ),
            q(
                "How does Go treat unused imports or variables?",
                (
                    opt("They are silently ignored at runtime"),
                    opt("They produce a warning but compile fine"),
                    opt("They are compile errors", correct=True),
                    opt("They are automatically removed by go build"),
                ),
                "The lesson notes unused imports and variables are compile errors, keeping things tidy.",
            ),
        ),
        "Types, variables & functions": (
            q(
                "What is the zero value of a string in Go according to the lesson?",
                (
                    opt("nil"),
                    opt("an empty string", correct=True),
                    opt("0"),
                    opt("false"),
                ),
                "The lesson lists the zero values as 0, the empty string, false, and nil.",
            ),
            q(
                "What is the idiomatic pattern for a Go function that can fail?",
                (
                    opt("It throws an exception that the caller catches"),
                    opt("It returns a result plus an error value", correct=True),
                    opt("It returns a single boolean indicating success"),
                    opt("It sets a global error flag"),
                ),
                "The lesson presents multiple returns as the idiom for result plus error, like (int, error).",
            ),
            q(
                "How do you handle errors in idiomatic Go?",
                (
                    opt("With try and catch blocks"),
                    opt("By checking if err != nil explicitly", correct=True),
                    opt("By ignoring the second return value"),
                    opt("With a finally clause that always runs"),
                ),
                "The lesson says you handle errors explicitly with if err != nil rather than exceptions.",
            ),
        ),
        "Control flow & data structures": (
            q(
                "Which looping construct does Go provide?",
                (
                    opt("Only while"),
                    opt("for is the only loop, and it covers while too", correct=True),
                    opt("Both for and foreach as separate keywords"),
                    opt("do-while and for"),
                ),
                "The lesson states for is Go's only loop and it covers while as well.",
            ),
            q(
                "When indexing a map like v, ok := ages['Ada'], what does ok indicate?",
                (
                    opt("Whether the value is greater than zero"),
                    opt("Whether the key existed in the map", correct=True),
                    opt("Whether the map is empty"),
                    opt("Whether the assignment succeeded"),
                ),
                "The lesson explains ok reports whether the key existed in the map.",
            ),
            q(
                "How does the lesson describe a slice in Go?",
                (
                    opt("A fixed-size array that cannot grow"),
                    opt("A dynamic array you can append to", correct=True),
                    opt("A key-value collection like a map"),
                    opt("A class that groups related fields"),
                ),
                "The lesson shows []int as a slice (dynamic array) that you grow with append.",
            ),
        ),
    },
    final=(
        q(
            "How does Go keep code formatting consistent across projects?",
            (
                opt("Each team picks its own style guide"),
                opt("gofmt formats the code for you", correct=True),
                opt("The compiler rejects any indentation"),
                opt("A linter must be installed separately"),
            ),
            "The lesson says there is essentially one way to write things and gofmt formats it for you.",
        ),
        q(
            "Which command compiles and runs a Go program in one step?",
            (
                opt("go build main.go"),
                opt("go run main.go", correct=True),
                opt("go exec main.go"),
                opt("go start main.go"),
            ),
            "The lesson lists go run main.go as compile plus run, while go build produces a binary.",
        ),
        q(
            "What does the lesson say about uninitialised variables in Go?",
            (
                opt("They hold garbage memory until assigned"),
                opt(
                    "They are never uninitialised because every type has a zero value", correct=True
                ),
                opt("They must always be given an explicit value"),
                opt("They default to nil regardless of type"),
            ),
            "The lesson stresses every type has a zero value, so variables are never uninitialised.",
        ),
        q(
            "How does Go group related fields, given it has no classes?",
            (
                opt("With structs", correct=True),
                opt("With maps"),
                opt("With slices"),
                opt("With packages"),
            ),
            "The lesson states structs group related fields and that there are no classes in Go.",
        ),
        q(
            "Which Go construct lets you write an if with a short statement before the condition?",
            (
                opt("if n := compute(); n > 0 { }", correct=True),
                opt("switch n := compute() { }"),
                opt("for n := compute(); n > 0 { }"),
                opt("range n := compute() { }"),
            ),
            "The lesson shows if with a short statement, as in if n := compute(); n > 0 { }.",
        ),
    ),
)
