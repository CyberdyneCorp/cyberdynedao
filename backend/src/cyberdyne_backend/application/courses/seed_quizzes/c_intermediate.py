"""Curated quiz questions for the C - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles so the seed can interleave a checkpoint quiz after each one."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Pointers": (
            q(
                "What does a pointer hold?",
                (
                    opt("A copy of another variable's value"),
                    opt("The memory address of another variable", correct=True),
                    opt("The size in bytes of a type"),
                    opt("The name of a function"),
                ),
                "A pointer holds the memory address of another variable.",
            ),
            q(
                "In the expression int *p = &x, what does the & operator do?",
                (
                    opt("It takes the address of x", correct=True),
                    opt("It dereferences x to read its value"),
                    opt("It declares x as a pointer"),
                    opt("It frees the memory used by x"),
                ),
                "The & operator means 'address of', so &x yields the address of x.",
            ),
            q(
                "Why must you pass a variable's address to let a function modify the caller's variable?",
                (
                    opt("Because C does not allow functions to take arguments"),
                    opt(
                        "Because C copies arguments, so the function needs the address to write back",
                        correct=True,
                    ),
                    opt("Because pointers are faster than plain integers"),
                    opt("Because NULL pointers cannot be incremented"),
                ),
                "C copies arguments by value, so passing the address lets the function write through the pointer to the caller's variable.",
            ),
        ),
        "Arrays, strings & dynamic memory": (
            q(
                "How does C know where a string ends?",
                (
                    opt("By a stored length prefix at the start"),
                    opt("By the terminating '\\0' null character", correct=True),
                    opt("By a newline character at the end"),
                    opt("By the size given to malloc"),
                ),
                "C strings are char arrays ending in a '\\0' null terminator, which marks where the string ends.",
            ),
            q(
                "What does the lesson say about bounds checking on array access like nums[0]?",
                (
                    opt("The compiler inserts automatic bounds checks"),
                    opt("There is no bounds checking; it is your job", correct=True),
                    opt("The runtime throws an exception on overflow"),
                    opt("malloc validates every index for you"),
                ),
                "Arrays in C have no bounds checking, so avoiding out-of-range access is the programmer's responsibility.",
            ),
            q(
                "What is the rule for malloc and free described in the lesson?",
                (
                    opt("Every malloc needs exactly one free", correct=True),
                    opt("free is optional because the OS reclaims everything"),
                    opt("You should free each block twice to be safe"),
                    opt("malloc automatically frees memory after use"),
                ),
                "Every malloc must be matched by exactly one free, or you leak memory.",
            ),
        ),
        "Structs & the build process": (
            q(
                "Which operator accesses a struct field through a pointer to the struct?",
                (
                    opt("The dot operator ."),
                    opt("The arrow operator ->", correct=True),
                    opt("The address-of operator &"),
                    opt("The dereference operator *"),
                ),
                "When you have a pointer to a struct you use the -> operator, as in pp->y.",
            ),
            q(
                "What does the C preprocessor do?",
                (
                    opt("Runs after linking to optimize the binary"),
                    opt("Runs before compilation doing textual substitution", correct=True),
                    opt("Checks pointers for NULL at runtime"),
                    opt("Allocates heap memory for structs"),
                ),
                "The preprocessor runs before compilation and performs textual substitution, such as #include and #define.",
            ),
            q(
                "In a multi-file build, what step combines object files into a binary?",
                (
                    opt("Preprocessing"),
                    opt("Linking", correct=True),
                    opt("Tokenizing"),
                    opt("Allocating"),
                ),
                "Each .c file is compiled to an object file, then linking combines those objects into the final binary.",
            ),
        ),
    },
    final=(
        q(
            "What does the * operator do when applied to a pointer p as in *p?",
            (
                opt("It takes the address of p"),
                opt("It dereferences p to access the value it points at", correct=True),
                opt("It declares p as a NULL pointer"),
                opt("It frees the memory p points at"),
            ),
            "The * operator dereferences a pointer, giving access to the value stored at the address it holds.",
        ),
        q(
            "What kind of behaviour is dereferencing a NULL or dangling pointer?",
            (
                opt("A compile-time error caught by gcc"),
                opt("Undefined behaviour, typically a crash", correct=True),
                opt("A harmless no-op"),
                opt("Automatically retried by the runtime"),
            ),
            "Dereferencing NULL or a dangling pointer is undefined behaviour and typically crashes the program.",
        ),
        q(
            "After calling free(arr), what does the lesson recommend doing to avoid a dangling pointer?",
            (
                opt("Call free(arr) a second time"),
                opt("Set arr = NULL", correct=True),
                opt("Reassign arr with malloc immediately"),
                opt("Call strlen on arr"),
            ),
            "Setting arr = NULL after free avoids leaving a dangling pointer to released memory.",
        ),
        q(
            "What is the relationship between an array name and a pointer in C?",
            (
                opt("An array name decays to a pointer to its first element", correct=True),
                opt("An array name is always a copy of the whole array"),
                opt("An array name is the same as a NULL pointer"),
                opt("An array name stores the array's length"),
            ),
            "An array is a contiguous block whose name decays to a pointer to the first element.",
        ),
        q(
            "What does typedef accomplish when defining a struct type?",
            (
                opt("It allocates the struct on the heap"),
                opt("It lets you drop the struct keyword when declaring variables", correct=True),
                opt("It marks the struct fields as constant"),
                opt("It links the struct across multiple files"),
            ),
            "A typedef on a struct lets you use the new type name directly, dropping the struct keyword.",
        ),
    ),
)
