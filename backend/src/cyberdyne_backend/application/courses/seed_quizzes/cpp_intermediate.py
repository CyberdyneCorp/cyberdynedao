from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Memory & RAII": (
            q(
                "What does RAII (Resource Acquisition Is Initialization) tie a resource's lifetime to?",
                (
                    opt("The lifetime of the program"),
                    opt(
                        "An object's scope, so the destructor frees it automatically", correct=True
                    ),
                    opt("A manual call to delete at program exit"),
                    opt("The garbage collector's next cycle"),
                ),
                "RAII ties a resource's lifetime to an object's scope so its destructor frees it automatically, even when exceptions fire.",
            ),
            q(
                "Where is a variable like int a = 5; allocated, and when is it freed?",
                (
                    opt("On the heap, freed when you call delete"),
                    opt("On the stack, freed automatically when scope ends", correct=True),
                    opt("On the heap, freed by the garbage collector"),
                    opt("In static storage, never freed"),
                ),
                "Stack memory is automatic and fast, and it is freed when the scope ends.",
            ),
            q(
                "What is the lesson's takeaway about raw new and delete?",
                (
                    opt("Use new and delete everywhere for full control"),
                    opt(
                        "Do not write raw new/delete; let objects own their resources", correct=True
                    ),
                    opt("Replace new with malloc for safety"),
                    opt("Only call delete inside the main function"),
                ),
                "The takeaway is to avoid raw new/delete and let RAII objects own their resources to prevent leaks.",
            ),
        ),
        "Smart pointers & move semantics": (
            q(
                "Which smart pointer represents exclusive ownership with zero overhead and is recommended as the default?",
                (
                    opt("shared_ptr"),
                    opt("unique_ptr", correct=True),
                    opt("weak_ptr"),
                    opt("auto_ptr"),
                ),
                "unique_ptr provides exclusive ownership with zero overhead and is the recommended default.",
            ),
            q(
                "After std::vector<int> b = std::move(a); what happens to a and b?",
                (
                    opt("a and b both hold copies of the same buffer"),
                    opt("b steals a's buffer with no copy, and a is now empty", correct=True),
                    opt("a keeps its buffer and b is empty"),
                    opt("Both a and b become empty"),
                ),
                "Moving transfers ownership of the buffer, so b takes a's guts without a copy and a is left empty.",
            ),
            q(
                "What does std::move actually do to enable a move?",
                (
                    opt("It immediately frees the object's memory"),
                    opt("It casts to an rvalue so the move constructor runs", correct=True),
                    opt("It deep-copies the object into a new location"),
                    opt("It increments a reference count"),
                ),
                "std::move casts to an rvalue so the move constructor runs instead of the copy constructor.",
            ),
        ),
        "Templates & the STL": (
            q(
                "What does a template let you do in C++?",
                (
                    opt("Run code without compiling it"),
                    opt(
                        "Write code once that works for any type, with the compiler stamping out a version per type",
                        correct=True,
                    ),
                    opt("Convert all types to a single base type at runtime"),
                    opt("Disable type checking entirely"),
                ),
                "Templates let you write generic code once and the compiler generates a version per type used.",
            ),
            q(
                "Which STL call sorts a vector v in place?",
                (
                    opt("v.order()"),
                    opt("std::sort(v.begin(), v.end())", correct=True),
                    opt("std::find(v.begin(), v.end())"),
                    opt("v.sorted()"),
                ),
                "std::sort(v.begin(), v.end()) sorts the elements of the vector in place.",
            ),
            q(
                "According to the lesson, what should you do before hand-rolling your own containers and algorithms?",
                (
                    opt("Write your own linked list first"),
                    opt(
                        "Reach for STL containers and algorithms, which cover most day-to-day needs",
                        correct=True,
                    ),
                    opt("Avoid the STL because it is too slow"),
                    opt("Copy code from another language"),
                ),
                "The STL's battle-tested containers and algorithms cover most needs, so reach for them before hand-rolling.",
            ),
        ),
    },
    final=(
        q(
            "What core C++ idea ensures resources are freed automatically when an object's scope ends?",
            (
                opt("Garbage collection"),
                opt("RAII", correct=True),
                opt("Manual reference counting by the programmer"),
                opt("Static analysis at compile time"),
            ),
            "RAII ties a resource's lifetime to an object's scope so the destructor frees it automatically.",
        ),
        q(
            "Which smart pointer is reference-counted and freed only when the last owner drops it?",
            (
                opt("unique_ptr"),
                opt("shared_ptr", correct=True),
                opt("raw pointer"),
                opt("scoped_ptr"),
            ),
            "shared_ptr is reference-counted shared ownership and is freed when the last owner drops it.",
        ),
        q(
            "Why is moving often preferred over copying for objects like vectors?",
            (
                opt("Moving duplicates the data for safety"),
                opt(
                    "Moving transfers ownership of the guts instead of duplicating them",
                    correct=True,
                ),
                opt("Moving always allocates new heap memory"),
                opt("Moving increases the reference count"),
            ),
            "Copying can be expensive, while moving transfers ownership of the internal buffer without duplicating it.",
        ),
        q(
            "What is the recommended default choice between stack and heap allocation?",
            (
                opt("Heap, because it lives until you free it"),
                opt(
                    "Stack, because it is automatic, fast, and freed when scope ends", correct=True
                ),
                opt("Static storage, because it never changes"),
                opt("Whichever the garbage collector chooses"),
            ),
            "The stack is automatic, fast, and freed at end of scope, making it the default choice.",
        ),
        q(
            "How does the compiler handle a template like max_of used with both int and double?",
            (
                opt("It throws a type error and requires one type"),
                opt("It stamps out a separate version of the code per type used", correct=True),
                opt("It converts both calls to use double"),
                opt("It defers type resolution to runtime"),
            ),
            "Templates let the compiler generate a version of the code for each type the template is used with.",
        ),
    ),
)
