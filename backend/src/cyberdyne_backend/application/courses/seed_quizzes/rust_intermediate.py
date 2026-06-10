"""Curated quiz questions for the Rust - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Ownership & borrowing": (
            q(
                "How does Rust manage memory according to the lesson?",
                (
                    opt("With a garbage collector that runs periodically"),
                    opt("With ownership, checked at compile time", correct=True),
                    opt("By requiring a manual free call for every value"),
                    opt("By reference counting every value at runtime"),
                ),
                "Rust has no garbage collector and no manual free; memory is managed by ownership, checked at compile time.",
            ),
            q(
                "After let s2 = s1 where s1 is a String, why is s1 no longer valid?",
                (
                    opt("Because ownership moves to s2", correct=True),
                    opt("Because s1 was borrowed by s2"),
                    opt("Because String values cannot be copied or moved"),
                    opt("Because s1 went out of scope"),
                ),
                "Assigning s1 to s2 moves ownership to s2, so s1 is no longer valid.",
            ),
            q(
                "What is the borrowing rule that prevents data races at compile time?",
                (
                    opt("Many mutable borrows are allowed at once"),
                    opt("Many shared borrows OR one mutable borrow, never both", correct=True),
                    opt("One shared borrow and one mutable borrow together"),
                    opt("No borrows are allowed once a value is owned"),
                ),
                "The rule is many shared (&) borrows or one mutable (&mut) borrow, never both.",
            ),
        ),
        "Error handling: Result, Option & ?": (
            q(
                "What does the Option enum represent?",
                (
                    opt("A value that may be absent, via Some or None", correct=True),
                    opt("A success or failure, via Ok or Err"),
                    opt("An exception that must be caught"),
                    opt("A reference that may be mutable"),
                ),
                "Option<T> has Some(T) and None and represents a value that may be absent.",
            ),
            q(
                "What does the ? operator do when applied to a Result?",
                (
                    opt("It panics and aborts the program on any error"),
                    opt("It returns the Err early, otherwise unwraps the Ok", correct=True),
                    opt("It converts the Result into an Option"),
                    opt("It logs the error and continues with a default value"),
                ),
                "? propagates an error early by returning the Err, otherwise it unwraps the Ok value.",
            ),
            q(
                "How does Rust handle fallible operations, given it has no exceptions?",
                (
                    opt("It returns an enum you must handle", correct=True),
                    opt("It throws an exception you catch with try"),
                    opt("It returns a null pointer on failure"),
                    opt("It sets a global error flag you check later"),
                ),
                "Rust has no exceptions; fallible operations return an enum (Result or Option) you must handle.",
            ),
        ),
        "Traits & generics": (
            q(
                "What are traits described as in the lesson?",
                (
                    opt("Shared behaviour, like interfaces, that you can require", correct=True),
                    opt("A way to allocate memory on the heap"),
                    opt("Concrete types that hold data fields"),
                    opt("Runtime checks that replace the borrow checker"),
                ),
                "Traits are shared behaviour, like interfaces, that you can require.",
            ),
            q(
                "In fn print_area<T: Area>(shape: &T), what does T: Area mean?",
                (
                    opt("T must implement the Area trait", correct=True),
                    opt("T is automatically the Area struct"),
                    opt("T cannot be borrowed inside the function"),
                    opt("T is converted into an Area at runtime"),
                ),
                "The trait bound T: Area requires that T implements the Area trait.",
            ),
            q(
                "What benefit do traits plus generics give Rust?",
                (
                    opt("Garbage collection of unused values"),
                    opt(
                        "Zero-cost abstraction, compiling to the same machine code as hand-written",
                        correct=True,
                    ),
                    opt("Automatic exception handling"),
                    opt("Dynamic typing at runtime"),
                ),
                "Traits plus generics give zero-cost abstraction: generic code compiles to the same machine code you would write by hand.",
            ),
        ),
    },
    final=(
        q(
            "Which statement matches the three ownership rules in the course?",
            (
                opt("A value can have many owners at once"),
                opt(
                    "Each value has a single owner and is dropped when the owner goes out of scope",
                    correct=True,
                ),
                opt("Values are never dropped until the program exits"),
                opt("Ownership can never move to a new owner"),
            ),
            "Each value has a single owner, is dropped when that owner goes out of scope, and ownership can move.",
        ),
        q(
            "Which two enums does Rust use for fallible operations and absent values?",
            (
                opt("Result and Option", correct=True),
                opt("Try and Catch"),
                opt("Some and Ok"),
                opt("Vec and Box"),
            ),
            "Result<T, E> models success or failure and Option<T> models a value that may be absent.",
        ),
        q(
            "What does borrowing with a shared reference (&) allow compared to moving?",
            (
                opt("It transfers ownership permanently to the callee"),
                opt("It lets the original value stay usable while it is read", correct=True),
                opt("It always allows mutation of the value"),
                opt("It drops the value immediately after use"),
            ),
            "A shared borrow lets you read a value without moving it, so the original stays usable.",
        ),
        q(
            "Which derivable traits are shown to save boilerplate on a struct?",
            (
                opt("Debug, Clone, PartialEq", correct=True),
                opt("Some, None, Ok"),
                opt("Area, Circle, Point"),
                opt("Move, Borrow, Drop"),
            ),
            "The lesson derives Debug, Clone, and PartialEq to save boilerplate.",
        ),
        q(
            "Why does the ? operator help keep code readable?",
            (
                opt(
                    "It keeps the happy path clean while forcing every error to be handled",
                    correct=True,
                ),
                opt("It silently ignores all errors that occur"),
                opt("It replaces the need for the Result type entirely"),
                opt("It runs the function asynchronously"),
            ),
            "? keeps the happy path clean while still forcing every error to be handled.",
        ),
    ),
)
