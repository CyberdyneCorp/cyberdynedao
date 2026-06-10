from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with JavaScript": (
            q(
                "Which keyword does the lesson recommend for a variable that will not be reassigned?",
                (
                    opt("var"),
                    opt("const", correct=True),
                    opt("let"),
                    opt("def"),
                ),
                "The lesson uses const for a value that cannot be reassigned and says to prefer it.",
            ),
            q(
                "Why does the lesson tell you to use === instead of == for equality?",
                (
                    opt("=== is strict while == coerces types", correct=True),
                    opt("== is not valid JavaScript syntax"),
                    opt("=== compares only numbers"),
                    opt("== is faster but less readable"),
                ),
                "The lesson warns against loose equality: === is strict, while == coerces types.",
            ),
            q(
                "What does typeof 42 return according to the lesson?",
                (
                    opt("'integer'"),
                    opt("'float'"),
                    opt("'number'", correct=True),
                    opt("'numeric'"),
                ),
                "The lesson shows typeof 42 is 'number' because JavaScript has one number type for ints and floats.",
            ),
        ),
        "Functions, scope, arrays & objects": (
            q(
                "How is the arrow function const square = (x) => x * x described?",
                (
                    opt("A function-scoped var declaration"),
                    opt("An arrow function", correct=True),
                    opt("A class method"),
                    opt("A template literal"),
                ),
                "The lesson labels const square = (x) => x * x as an arrow function.",
            ),
            q(
                "What does the array method nums.map((n) => n * 2) produce for [1, 2, 3, 4]?",
                (
                    opt("[1, 2, 3, 4]"),
                    opt("[2, 4]"),
                    opt("[2, 4, 6, 8]", correct=True),
                    opt("10"),
                ),
                "The lesson shows map doubling each element, giving [2,4,6,8].",
            ),
            q(
                "In the lesson, what does const { name } = user do?",
                (
                    opt("Destructures the name property out of user", correct=True),
                    opt("Deletes the name key from user"),
                    opt("Creates a new array from user"),
                    opt("Adds an active key to user"),
                ),
                "The lesson calls const { name } = user destructuring, which extracts name = 'Ada'.",
            ),
        ),
        "Control flow & the DOM": (
            q(
                "According to the lesson, what does for...of iterate over?",
                (
                    opt("The keys of an object"),
                    opt("The values", correct=True),
                    opt("The indexes only"),
                    opt("The prototype chain"),
                ),
                "The lesson notes that for...of iterates values.",
            ),
            q(
                "What does document.querySelector do as described in the lesson?",
                (
                    opt("Runs a callback on an event"),
                    opt("Finds an element by CSS selector", correct=True),
                    opt("Creates a new HTML element"),
                    opt("Sends a network request"),
                ),
                "The lesson states querySelector finds an element by CSS selector.",
            ),
            q(
                "What is addEventListener used for in the lesson?",
                (
                    opt("To change an element's text content"),
                    opt("To select an element by id"),
                    opt("To run a callback on events such as click or input", correct=True),
                    opt("To define a CSS selector"),
                ),
                "The lesson says addEventListener runs a callback on events like click, input, and submit.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about JavaScript types is true per the course?",
            (
                opt("Variables must declare their type up front"),
                opt(
                    "JavaScript is dynamically typed and variables do not declare a type",
                    correct=True,
                ),
                opt("There are separate int and float number types"),
                opt("typeof true returns 'bool'"),
            ),
            "The course explains JavaScript is dynamically typed, so variables do not declare a type.",
        ),
        q(
            "How are let and const scoped according to the course?",
            (
                opt("Block-scoped", correct=True),
                opt("Function-scoped like var"),
                opt("Globally scoped only"),
                opt("Scoped to the whole module"),
            ),
            "The course shows let and const are block-scoped, unlike the older function-scoped var.",
        ),
        q(
            "Which array method keeps only elements that pass a test, such as even numbers?",
            (
                opt("push"),
                opt("map"),
                opt("filter", correct=True),
                opt("querySelector"),
            ),
            "The course uses filter with n % 2 === 0 to keep only the even numbers.",
        ),
        q(
            "What is the DOM as described in the course?",
            (
                opt("A way to declare variables in the browser"),
                opt("The live tree of elements that JavaScript reads and changes", correct=True),
                opt("A strict equality operator"),
                opt("A server-side runtime for JavaScript"),
            ),
            "The course defines the DOM as the live tree of elements that JavaScript reads and changes.",
        ),
        q(
            "Which template literal correctly interpolates name and age?",
            (
                opt('"name is age"'),
                opt("`${name} is ${age}`", correct=True),
                opt('"$name is $age"'),
                opt("name + is + age"),
            ),
            "The course uses a backtick template literal with ${name} and ${age} for interpolation.",
        ),
    ),
)
