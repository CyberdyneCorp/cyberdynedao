from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Generics": (
            q(
                "Why use generics instead of typing a reusable function with any?",
                (
                    opt("They make the code run faster at runtime"),
                    opt(
                        "They let the function keep its types instead of falling back to any",
                        correct=True,
                    ),
                    opt("They disable type checking inside the function body"),
                    opt("They convert every parameter to a string"),
                ),
                "Generics write reusable code that keeps its types instead of falling back to any.",
            ),
            q(
                "For function first<T>(arr: T[]): T | undefined, what is T when called with first([1, 2, 3])?",
                (
                    opt("string"),
                    opt("any"),
                    opt("number", correct=True),
                    opt("undefined"),
                ),
                "Calling first([1, 2, 3]) infers T = number, so the return type is number | undefined.",
            ),
            q(
                "In longest<T extends { length: number }>, what does the extends constraint do?",
                (
                    opt(
                        "It limits T so it must have a length member, which can then be used safely",
                        correct=True,
                    ),
                    opt("It forces T to always be an array of numbers"),
                    opt("It makes T optional so the argument can be omitted"),
                    opt("It copies the length property onto the return value"),
                ),
                "extends constrains what T can be, so you can safely use its members such as .length.",
            ),
        ),
        "Narrowing & type guards": (
            q(
                "When a value has a union type, what does TypeScript do as you check it?",
                (
                    opt("It widens the value to any so all members are allowed"),
                    opt(
                        "It narrows the value to a specific type so member access is safe",
                        correct=True,
                    ),
                    opt("It throws a compile error until you add a cast"),
                    opt("It converts the value to a string automatically"),
                ),
                "TypeScript narrows a union to a specific type as you check it, making member access safe.",
            ),
            q(
                "Which guard is used to check that an object has a particular property?",
                (
                    opt("typeof"),
                    opt("instanceof"),
                    opt("in", correct=True),
                    opt("extends"),
                ),
                "The in guard checks that a property exists on the value; typeof is for primitives and instanceof for classes.",
            ),
            q(
                "In a discriminated union, what lets TypeScript narrow object unions exhaustively?",
                (
                    opt("A shared literal tag such as kind on each member", correct=True),
                    opt("Declaring every member with the any type"),
                    opt("Wrapping each member in a generic Box<T>"),
                    opt("Marking all properties as readonly"),
                ),
                "A shared literal tag like kind lets TS narrow object unions exhaustively in a switch.",
            ),
        ),
        "Utility types & classes": (
            q(
                "What does Partial<User> produce?",
                (
                    opt("A type with all properties of User made optional", correct=True),
                    opt("A type with the email property removed"),
                    opt("A type keeping only the name property"),
                    opt("A record mapping numbers to User values"),
                ),
                "Partial<User> makes all properties of User optional.",
            ),
            q(
                "Which utility type drops the email property from User?",
                (
                    opt('Pick<User, "email">'),
                    opt('Omit<User, "email">', correct=True),
                    opt("Partial<User>"),
                    opt("Record<number, User>"),
                ),
                'Omit<User, "email"> removes the email property; Pick would instead keep only the named property.',
            ),
            q(
                "When are access modifiers like private and readonly checked?",
                (
                    opt("Only at runtime when the object is created"),
                    opt("At compile time", correct=True),
                    opt("Only when the enum is defined"),
                    opt("Never, they are documentation only"),
                ),
                "private, protected, public, and readonly are checked at compile time.",
            ),
        ),
    },
    final=(
        q(
            "What problem do generics solve in TypeScript?",
            (
                opt(
                    "They let you write reusable code that keeps its types instead of falling back to any",
                    correct=True,
                ),
                opt("They make functions run faster by skipping type checks"),
                opt("They replace classes with plain objects"),
                opt("They force every value to be a string"),
            ),
            "Generics write reusable code that keeps its types instead of falling back to any.",
        ),
        q(
            "Which guard checks the type of a primitive value like a string or number?",
            (
                opt("instanceof"),
                opt("in"),
                opt("typeof", correct=True),
                opt("extends"),
            ),
            "typeof is the guard used to narrow primitives; instanceof is for classes and in checks for a property.",
        ),
        q(
            "Which utility type keeps only the name property of User?",
            (
                opt('Omit<User, "name">'),
                opt('Pick<User, "name">', correct=True),
                opt("Partial<User>"),
                opt("Record<number, User>"),
            ),
            'Pick<User, "name"> keeps only the named property.',
        ),
        q(
            "What makes a discriminated union narrow exhaustively in a switch?",
            (
                opt("Each member sharing a literal tag such as kind", correct=True),
                opt("Every member being declared as any"),
                opt("Constraining the union with extends"),
                opt("Marking the union readonly"),
            ),
            "A shared literal tag like kind lets TypeScript narrow the union exhaustively.",
        ),
        q(
            "Together, what do utility types and generics let you do?",
            (
                opt("Describe almost any shape precisely", correct=True),
                opt("Run TypeScript without compiling it"),
                opt("Disable all compile-time type checks"),
                opt("Avoid ever declaring an interface"),
            ),
            "Utility types plus generics let you describe almost any shape precisely.",
        ),
    ),
)
