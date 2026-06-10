"""Curated quiz questions for the Go - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Interfaces & methods": (
            q(
                "How do you attach a method to your own type in Go?",
                (
                    opt("By listing it inside the type's struct body"),
                    opt(
                        "By declaring a function with a receiver, such as func (r Rect) Area() int",
                        correct=True,
                    ),
                    opt("By using an implements keyword on the type"),
                    opt("By registering the function with the runtime"),
                ),
                "Methods are declared as functions with a receiver, like func (r Rect) Area() int.",
            ),
            q(
                "How does a type satisfy an interface in Go?",
                (
                    opt("It must use the implements keyword to declare the interface"),
                    opt("It must inherit from the interface type"),
                    opt("Implicitly, just by having the methods the interface lists", correct=True),
                    opt("It must be registered in the interface's method table"),
                ),
                "Go uses structural typing, so a type satisfies an interface implicitly just by having the required methods.",
            ),
            q(
                "What does the empty interface any hold?",
                (
                    opt("Any value", correct=True),
                    opt("Only pointer values"),
                    opt("Only types that declare methods"),
                    opt("Nothing, it is purely a marker"),
                ),
                "The empty interface any, an alias for interface{}, can hold any value.",
            ),
        ),
        "Goroutines & channels": (
            q(
                "How do you start a goroutine in Go?",
                (
                    opt("Call sync.Start on the function"),
                    opt("Prefix a function call with the go keyword", correct=True),
                    opt("Wrap the call in a select statement"),
                    opt("Send the function over a channel"),
                ),
                "A goroutine is started by prefixing a function call with the go keyword, so it runs concurrently.",
            ),
            q(
                "What happens when you receive from a channel with v := <-ch?",
                (
                    opt("It returns immediately with a zero value if empty"),
                    opt("It blocks until a value arrives", correct=True),
                    opt("It panics if no value is ready"),
                    opt("It spawns a new goroutine to wait"),
                ),
                "Receiving from a channel blocks until a value arrives.",
            ),
            q(
                "What is the recommended way to wait for many goroutines to finish?",
                (
                    opt("A select statement"),
                    opt("The any interface"),
                    opt("sync.WaitGroup", correct=True),
                    opt("A buffered channel of size one"),
                ),
                "sync.WaitGroup is used to wait for many goroutines to complete.",
            ),
        ),
        "Errors, defer & modules": (
            q(
                "What does the %w verb do in fmt.Errorf?",
                (
                    opt("It wraps the error to add context", correct=True),
                    opt("It writes the error to standard output"),
                    opt("It silently discards the underlying error"),
                    opt("It converts the error into a panic"),
                ),
                "The %w verb wraps an error so context can be added while preserving the original.",
            ),
            q(
                "When does a deferred call such as defer f.Close() run?",
                (
                    opt("Immediately when the defer statement is reached"),
                    opt("When the function returns, no matter how it returns", correct=True),
                    opt("Only if the function returns without an error"),
                    opt("Only when recover is called"),
                ),
                "A deferred call runs when the function returns, regardless of how it returns.",
            ),
            q(
                "Which command starts a new Go module?",
                (
                    opt("go get example.com/app"),
                    opt("go build example.com/app"),
                    opt("go mod init example.com/app", correct=True),
                    opt("go run example.com/app"),
                ),
                "go mod init starts a new module, while go get adds a dependency.",
            ),
        ),
    },
    final=(
        q(
            "What kind of typing does Go use for interface satisfaction?",
            (
                opt("Nominal typing with an implements keyword"),
                opt("Structural typing, where having the methods is enough", correct=True),
                opt("Duck typing checked only at runtime"),
                opt("Inheritance from a base interface type"),
            ),
            "Go uses structural typing, so a type satisfies an interface just by having the listed methods.",
        ),
        q(
            "How do goroutines communicate idiomatically in Go?",
            (
                opt("By sharing memory through global variables"),
                opt("By passing values over channels", correct=True),
                opt("By raising and recovering panics"),
                opt("By writing to shared files"),
            ),
            "The Go motto is do not share memory, share by communicating, which means passing values over channels.",
        ),
        q(
            "What is error in Go?",
            (
                opt("A built-in exception class"),
                opt("Just an interface returned as the last value", correct=True),
                opt("A reserved panic type"),
                opt("A field automatically added to every struct"),
            ),
            "error is just an interface, typically returned as the last value of a function.",
        ),
        q(
            "What is panic intended for, according to the lesson?",
            (
                opt("Expected, recoverable conditions"),
                opt("Truly unrecoverable bugs", correct=True),
                opt("Closing resources cleanly"),
                opt("Wrapping errors with context"),
            ),
            "panic is for truly unrecoverable bugs, while expected failures should use returned errors.",
        ),
        q(
            "What does the go.mod file provide?",
            (
                opt("A buffer for channel sends"),
                opt("Pinned dependencies for reproducible builds", correct=True),
                opt("A list of goroutines to start"),
                opt("The set of interfaces a package satisfies"),
            ),
            "go.mod pins your dependencies so builds are reproducible.",
        ),
    ),
)
