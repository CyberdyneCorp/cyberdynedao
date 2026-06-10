from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Structs vs classes": (
            q(
                "What are the semantics of a struct in Swift?",
                (
                    opt("Reference semantics, so instances are shared"),
                    opt("Value semantics, so instances are copied", correct=True),
                    opt("Identity semantics compared with ==="),
                    opt("Inheritance semantics like a base class"),
                ),
                "A struct has value semantics, meaning it is copied rather than shared.",
            ),
            q(
                "After var b = a copies a Point struct, what happens to a.x when b.x is set to 99?",
                (
                    opt("a.x stays at its original value 1", correct=True),
                    opt("a.x also becomes 99 because they are shared"),
                    opt("a.x becomes nil"),
                    opt("The assignment is a compile error"),
                ),
                "Because the struct is copied, mutating b leaves a unchanged.",
            ),
            q(
                "What keyword must mark a method that changes a struct's own properties?",
                (
                    opt("override"),
                    opt("static"),
                    opt("mutating", correct=True),
                    opt("shared"),
                ),
                "A method that mutates a struct's own properties must be marked mutating.",
            ),
        ),
        "Protocols & extensions": (
            q(
                "What is a protocol in Swift described as?",
                (
                    opt("A concrete class you must subclass"),
                    opt(
                        "A contract of requirements a type can adopt, like an interface",
                        correct=True,
                    ),
                    opt("A way to copy value types"),
                    opt("A keyword that starts asynchronous work"),
                ),
                "A protocol is a contract of requirements a type can adopt, similar to an interface.",
            ),
            q(
                "What can extensions do in Swift according to the lesson?",
                (
                    opt("Add behaviour to existing types, even ones you do not own", correct=True),
                    opt("Only add stored properties to classes"),
                    opt("Replace a type's existing methods at runtime"),
                    opt("Force a type to inherit from a base class"),
                ),
                "Extensions add behaviour to existing types, even ones you do not own, and can give protocols default implementations.",
            ),
            q(
                "Which style does the lesson call idiomatic Swift, preferred over deep class hierarchies?",
                (
                    opt("Composing with protocols and extensions", correct=True),
                    opt("Subclassing a common base class for every type"),
                    opt("Using global mutable state"),
                    opt("Avoiding protocols entirely"),
                ),
                "Composing with protocols plus extensions is idiomatic Swift, preferred over deep class hierarchies.",
            ),
        ),
        "Concurrency: async/await": (
            q(
                "What does await do in Swift concurrency?",
                (
                    opt("It blocks the thread until the result is ready"),
                    opt(
                        "It suspends until the result is ready, freeing the thread meanwhile",
                        correct=True,
                    ),
                    opt("It starts a new operating system process"),
                    opt("It cancels the current asynchronous work"),
                ),
                "await suspends until the result is ready while freeing the thread in the meantime.",
            ),
            q(
                "How do you start asynchronous work from synchronous code?",
                (
                    opt("With a Task { } block", correct=True),
                    opt("With the mutating keyword"),
                    opt("With an extension on Int"),
                    opt("With the === identity operator"),
                ),
                "Task { } starts asynchronous work from synchronous code.",
            ),
            q(
                "What does async let let you do?",
                (
                    opt("Run independent work in parallel concurrently", correct=True),
                    opt("Declare a constant that cannot change"),
                    opt("Mark a struct method as mutating"),
                    opt("Define a protocol requirement"),
                ),
                "async let runs independent work in parallel so both tasks run concurrently.",
            ),
        ),
    },
    final=(
        q(
            "Which Swift construct does the course say Swift favours for predictable, no shared-mutable-state code?",
            (
                opt("Classes"),
                opt("Structs", correct=True),
                opt("Actors"),
                opt("Protocols"),
            ),
            "Swift favours structs because they are predictable and avoid shared-mutable-state bugs.",
        ),
        q(
            "When should you reach for a class instead of a struct?",
            (
                opt("When you need shared identity or inheritance", correct=True),
                opt("Whenever you want value copying"),
                opt("Only for asynchronous code"),
                opt("Never, classes are not allowed in Swift"),
            ),
            "You reach for a class when you need shared identity or inheritance.",
        ),
        q(
            "What can give protocols default implementations that are free for every conformer?",
            (
                opt("Extensions", correct=True),
                opt("The mutating keyword"),
                opt("Task blocks"),
                opt("The === operator"),
            ),
            "Extensions can give protocols default implementations available to every conformer.",
        ),
        q(
            "What protects shared mutable state from data races in Swift concurrency?",
            (
                opt("Structs"),
                opt("Actors", correct=True),
                opt("Protocols"),
                opt("Extensions"),
            ),
            "Actors protect shared mutable state from data races.",
        ),
        q(
            "In the example, what does try await (a, b) with async let a and async let b achieve?",
            (
                opt("It runs fetchA and fetchB sequentially one after another"),
                opt(
                    "It runs both fetches concurrently and awaits their combined result",
                    correct=True,
                ),
                opt("It cancels both fetches"),
                opt("It converts the values to structs"),
            ),
            "Using async let, both fetches run concurrently and try await collects their combined result.",
        ),
    ),
)
