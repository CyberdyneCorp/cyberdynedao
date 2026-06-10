from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Asynchronous JavaScript": (
            q(
                "Why does slow work like network or timers run asynchronously in JavaScript?",
                (
                    opt("Because JavaScript spawns a new OS thread per task"),
                    opt(
                        "Because JavaScript is single-threaded and gives you the result later",
                        correct=True,
                    ),
                    opt("Because Promises run on a separate CPU core"),
                    opt("Because the browser disables synchronous code"),
                ),
                "JavaScript is single-threaded, so slow work runs asynchronously and you get the result later via a Promise.",
            ),
            q(
                "What does await do inside an async function?",
                (
                    opt("It cancels the Promise immediately"),
                    opt("It converts a callback into a Promise"),
                    opt("It pauses until the Promise resolves", correct=True),
                    opt("It runs the function on a background thread"),
                ),
                "await pauses until the Promise resolves.",
            ),
            q(
                "How do you run multiple async operations in parallel according to the lesson?",
                (
                    opt("Promise.all([a, b])", correct=True),
                    opt("await.parallel(a, b)"),
                    opt("setTimeout(a, b)"),
                    opt("fetch.all(a, b)"),
                ),
                "The lesson says to run things in parallel with Promise.all([a, b]).",
            ),
        ),
        "Closures, this & prototypes": (
            q(
                "What is a closure as described in the lesson?",
                (
                    opt(
                        "A function that remembers the variables from where it was created",
                        correct=True,
                    ),
                    opt("A function that has no access to outer variables"),
                    opt("A way to close a network connection"),
                    opt("A class that inherits from another class"),
                ),
                "A closure is a function that remembers the variables from where it was created.",
            ),
            q(
                "What determines the value of this for a regular function?",
                (
                    opt("The file the function is defined in"),
                    opt("How the function is called", correct=True),
                    opt("The name of the function"),
                    opt("The number of arguments passed"),
                ),
                "this depends on how a function is called.",
            ),
            q(
                "Why are arrow functions useful in callbacks regarding this?",
                (
                    opt("They create a brand new this for the callback"),
                    opt("They do not have their own this and inherit it instead", correct=True),
                    opt("They always set this to the global object"),
                    opt("They disable this entirely"),
                ),
                "Arrow functions do not have their own this; they inherit it, which is usually what you want in callbacks.",
            ),
        ),
        "Modules & functional patterns": (
            q(
                "How do you make a value available from one ES module to another?",
                (
                    opt("Use require() at the top of the file"),
                    opt("Use the export keyword and import it elsewhere", correct=True),
                    opt("Declare it with var so it becomes global"),
                    opt("Wrap it in a setTimeout call"),
                ),
                "ES modules expose values with export and consume them with import, as in import { add, PI } from ./math.js.",
            ),
            q(
                "What does nums.reduce((sum, n) => sum + n, 0) produce for [1, 2, 3, 4]?",
                (
                    opt("[2, 4, 6, 8]"),
                    opt("[1, 2, 3, 4]"),
                    opt("10", correct=True),
                    opt("4"),
                ),
                "reduce accumulates the sum starting from 0, giving 1 + 2 + 3 + 4 = 10.",
            ),
            q(
                "What does const { ...defaults, ...overrides } style syntax demonstrate in the lesson?",
                (
                    opt("The spread operator merging objects", correct=True),
                    opt("A class declaration"),
                    opt("An async iterator"),
                    opt("A prototype chain lookup"),
                ),
                "The merged object uses spread to combine defaults and overrides.",
            ),
        ),
    },
    final=(
        q(
            "Which syntax makes asynchronous code read like synchronous code?",
            (
                opt("Callbacks"),
                opt("async / await", correct=True),
                opt("setInterval"),
                opt("Generators only"),
            ),
            "async / await is syntactic sugar that makes async code read like sync code.",
        ),
        q(
            "What is the prototype chain described as in the lesson?",
            (
                opt(
                    "A way for objects to inherit from other objects, with class as modern sugar over it",
                    correct=True,
                ),
                opt("A list of pending Promises"),
                opt("A queue of asynchronous callbacks"),
                opt("A module import resolver"),
            ),
            "Objects inherit from other objects via the prototype chain, and class is modern sugar over it.",
        ),
        q(
            "Which array method returns a new array containing only the elements that pass a test?",
            (
                opt("reduce"),
                opt("map"),
                opt("filter", correct=True),
                opt("forEach"),
            ),
            "filter keeps only matching elements, as in nums.filter((n) => n % 2 === 0).",
        ),
        q(
            "What is the basis of private state and callbacks in JavaScript per the course?",
            (
                opt("Closures", correct=True),
                opt("Promises"),
                opt("ES modules"),
                opt("The spread operator"),
            ),
            "A closure remembers its creation-scope variables, which is the basis of private state and callbacks.",
        ),
        q(
            "What do immutable, declarative patterns like map, filter, and reduce avoid doing to data?",
            (
                opt("Returning a value"),
                opt("Mutating it", correct=True),
                opt("Iterating over it"),
                opt("Importing it"),
            ),
            "Functional patterns transform data without mutating it.",
        ),
    ),
)
