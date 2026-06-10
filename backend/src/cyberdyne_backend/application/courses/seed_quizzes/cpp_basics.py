from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Getting started with modern C++": (
            q(
                "What does the main function return on success?",
                (
                    opt("A std::string"),
                    opt("An int with the value 0", correct=True),
                    opt("A bool set to true"),
                    opt("Nothing, it is void"),
                ),
                "The lesson states main returns an int where 0 means success.",
            ),
            q(
                "What does the auto keyword do in a declaration like auto x = 42;?",
                (
                    opt("Lets the compiler infer the type, here int", correct=True),
                    opt("Forces the variable to be a double"),
                    opt("Makes the variable a constant"),
                    opt("Allocates the variable on the heap"),
                ),
                "The lesson says auto lets the compiler infer a type, so auto x = 42; is an int.",
            ),
            q(
                "What is std:: in the example program?",
                (
                    opt("The name of the main function"),
                    opt("A compiler flag for C++20"),
                    opt("The standard-library namespace", correct=True),
                    opt("A header file that must be created"),
                ),
                "The lesson explains that std:: is the standard-library namespace.",
            ),
        ),
        "Types, variables & references": (
            q(
                "When is the type of a variable in C++ checked?",
                (
                    opt("At compile time, since C++ is statically typed", correct=True),
                    opt("At run time only"),
                    opt("Never, types are dynamic"),
                    opt("Only when using auto"),
                ),
                "The lesson states C++ is statically typed and every variable has a fixed type checked at compile time.",
            ),
            q(
                "What is a reference in C++ according to the lesson?",
                (
                    opt("A value that can be null or reseated"),
                    opt("An alias for an existing variable", correct=True),
                    opt("A header from the standard library"),
                    opt("A copy of a variable stored on the heap"),
                ),
                "The lesson defines a reference as an alias for an existing variable.",
            ),
            q(
                "Why might you reach for a pointer instead of a reference?",
                (
                    opt("Because pointers are always faster than references"),
                    opt("Because references cannot hold integers"),
                    opt("When you need nullability or reseating", correct=True),
                    opt("Because pointers do not need an address"),
                ),
                "The lesson advises using pointers only when you need nullability or reseating.",
            ),
        ),
        "Control flow, functions & lambdas": (
            q(
                "What kind of loop is for (int n : v) shown in the lesson?",
                (
                    opt("A range-based for loop", correct=True),
                    opt("A while loop"),
                    opt("A do-while loop"),
                    opt("An infinite loop"),
                ),
                "The lesson labels for (int n : v) as a range-based for loop.",
            ),
            q(
                "What does the capture list [] of a lambda specify?",
                (
                    opt("The return type of the lambda"),
                    opt("The parameters passed to the lambda"),
                    opt("What outside variables the lambda captures", correct=True),
                    opt("The name of the lambda function"),
                ),
                "The lesson says [] is the capture list and shows capturing factor by value.",
            ),
            q(
                "What does the capture form [&] do?",
                (
                    opt("Captures by reference", correct=True),
                    opt("Copies all captured variables"),
                    opt("Captures nothing"),
                    opt("Captures only the first argument"),
                ),
                "The lesson states [=] copies and [&] captures by reference.",
            ),
        ),
    },
    final=(
        q(
            "Which command compiles hello.cpp with the C++20 standard?",
            (
                opt("python hello.cpp -o hello"),
                opt("g++ -std=c++20 hello.cpp -o hello", correct=True),
                opt("gcc hello.cpp --run"),
                opt("c++20 build hello.cpp"),
            ),
            "The lesson shows g++ -std=c++20 hello.cpp -o hello as the compile command.",
        ),
        q(
            "Which keyword marks a value that cannot change, as in const int MAX = 100;?",
            (
                opt("auto"),
                opt("static"),
                opt("const", correct=True),
                opt("final"),
            ),
            "The lesson uses const to declare a value that cannot change.",
        ),
        q(
            "After int& ref = x; the statement ref = 20; does what?",
            (
                opt("Creates a new variable named ref"),
                opt("Sets x to 20 because ref is an alias for x", correct=True),
                opt("Leaves x unchanged"),
                opt("Causes a compile error"),
            ),
            "The lesson shows ref is x, so assigning to ref changes x to 20.",
        ),
        q(
            "What does the lambda auto square = [](int x) { return x * x; }; return for square(5)?",
            (
                opt("10"),
                opt("25", correct=True),
                opt("5"),
                opt("55"),
            ),
            "The lesson shows square(5) evaluates to 25.",
        ),
        q(
            "What type does auto total = count * 2; get when count is an int?",
            (
                opt("double"),
                opt("bool"),
                opt("int", correct=True),
                opt("std::string"),
            ),
            "The lesson shows auto total = count * 2; is inferred as int.",
        ),
    ),
)
