from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is C# and .NET?": (
            q(
                "What does the Common Language Runtime (CLR) do with the intermediate language (IL) that C# compiles to?",
                (
                    opt("It stores the IL permanently and never executes it"),
                    opt(
                        "It just-in-time compiles the IL and runs it, with a garbage collector managing memory",
                        correct=True,
                    ),
                    opt("It translates the IL into Python so .NET can run it"),
                    opt("It uploads the IL to Microsoft servers for remote execution"),
                ),
                "The CLR just-in-time compiles the IL and runs it, while a garbage collector manages memory for you.",
            ),
            q(
                "Which dotnet CLI command scaffolds a new console application named MyApp?",
                (
                    opt("dotnet build MyApp"),
                    opt("dotnet run MyApp"),
                    opt("dotnet new console -n MyApp", correct=True),
                    opt("dotnet publish -c MyApp"),
                ),
                "dotnet new console -n MyApp scaffolds a new console app, while dotnet run builds and runs it.",
            ),
            q(
                "In modern C# with top-level statements, what is true about a single Console.WriteLine line in a file?",
                (
                    opt(
                        "It is a complete program because the compiler generates the boilerplate",
                        correct=True,
                    ),
                    opt("It must still be wrapped in a namespace and a Main method"),
                    opt("It will not compile without an explicit class Program"),
                    opt("It only works inside a static void Main method"),
                ),
                "Top-level statements let a file be the program; that single line is a complete program because the compiler generates the boilerplate.",
            ),
        ),
        "Variables & types": (
            q(
                "Which type does the lesson recommend for currency because it is exact and avoids rounding error?",
                (
                    opt("double"),
                    opt("float"),
                    opt("decimal", correct=True),
                    opt("int"),
                ),
                "decimal is described as exact with no rounding error, making it the choice for money.",
            ),
            q(
                "What is the difference between value types and reference types as described?",
                (
                    opt(
                        "Value types hold the data directly while reference types hold a reference to data on the heap",
                        correct=True,
                    ),
                    opt("Value types live on the heap and reference types live on the stack only"),
                    opt(
                        "Reference types copy their full data on assignment while value types copy a pointer"
                    ),
                    opt("There is no difference; both behave identically when assigned"),
                ),
                "A value type variable holds the data, while a reference type variable holds a reference to data on the heap.",
            ),
            q(
                "What does the null-coalescing operator ?? do in the expression maybe ?? 0?",
                (
                    opt("It throws an exception when maybe is null"),
                    opt("It supplies a default value of 0 when maybe is null", correct=True),
                    opt("It forces maybe to always be null"),
                    opt("It converts maybe into a reference type"),
                ),
                "The ?? operator supplies a default value when the left operand is null.",
            ),
        ),
        "Control flow & pattern matching": (
            q(
                "What is described as the default case in a switch expression?",
                (
                    opt("The default keyword"),
                    opt("The else branch"),
                    opt("The underscore _", correct=True),
                    opt("The null pattern"),
                ),
                "In a switch expression the underscore _ is the default that makes it exhaustive.",
            ),
            q(
                "What does the is keyword let you do in pattern matching?",
                (
                    opt("Test a value and bind it to a new variable in one step", correct=True),
                    opt("Convert any type into a string automatically"),
                    opt("Loop over a collection until a condition is met"),
                    opt("Catch an exception thrown by the value"),
                ),
                "is tests a value and can bind it to a new variable in one step, such as obj is string s.",
            ),
            q(
                "In a loop, what is the difference between break and continue?",
                (
                    opt("break skips to the next iteration while continue exits the loop"),
                    opt(
                        "break leaves the loop immediately while continue skips to the next iteration",
                        correct=True,
                    ),
                    opt("Both immediately exit the loop"),
                    opt("Both skip only the current statement but keep iterating normally"),
                ),
                "break leaves a loop immediately, while continue skips to the next iteration.",
            ),
        ),
        "Collections: arrays, lists & dictionaries": (
            q(
                "According to the lesson, which collection should you pick for a fixed-size structure with fast index access?",
                (
                    opt("List<T>"),
                    opt("Dictionary<K,V>"),
                    opt("int[]", correct=True),
                    opt("HashSet<T>"),
                ),
                "An array such as int[] is the choice for fixed-size, fast index access.",
            ),
            q(
                "Why use Dictionary.TryGetValue instead of indexing for a key that may be missing?",
                (
                    opt(
                        "It is a safe lookup that does not throw when the key is absent",
                        correct=True,
                    ),
                    opt("It automatically adds the missing key with a default value"),
                    opt("It sorts the dictionary before returning"),
                    opt("It is the only way to read any value from a dictionary"),
                ),
                "TryGetValue is described as a safe lookup that does not throw when the key is missing.",
            ),
            q(
                "Which collection does the lesson recommend for an ordered, resizable sequence?",
                (
                    opt("int[]"),
                    opt("List<T>", correct=True),
                    opt("Queue<T>"),
                    opt("Dictionary<K,V>"),
                ),
                "List<T> is the everyday ordered, resizable list.",
            ),
        ),
        "Methods": (
            q(
                "What return type does a method use when it returns nothing?",
                (
                    opt("null"),
                    opt("void", correct=True),
                    opt("empty"),
                    opt("object"),
                ),
                "A method that returns nothing uses the void return type.",
            ),
            q(
                "What does the params keyword allow a method to accept?",
                (
                    opt("A variable number of arguments", correct=True),
                    opt("Only named arguments"),
                    opt("A reference to the caller's variable"),
                    opt("A default value for every parameter"),
                ),
                "params lets a method accept a variable number of arguments collected into an array.",
            ),
            q(
                "How do ref and out differ as described in the lesson?",
                (
                    opt("ref passes arguments by value while out copies them"),
                    opt(
                        "ref lets a method modify the caller's variable while out returns extra values",
                        correct=True,
                    ),
                    opt("Both prevent the method from changing any argument"),
                    opt("out modifies the caller's variable while ref only reads it"),
                ),
                "ref lets a method modify the caller's variable, while out is used to return extra values such as in the Try pattern.",
            ),
        ),
        "Classes & objects": (
            q(
                "What does marking a base-class method virtual allow a subclass to do?",
                (
                    opt("Hide the method from all callers"),
                    opt("override it, enabling polymorphism", correct=True),
                    opt("Prevent the method from being inherited"),
                    opt("Call the method without an instance"),
                ),
                "A virtual method can be overridden by a subclass, which is polymorphism.",
            ),
            q(
                "What is true about an abstract class according to the lesson?",
                (
                    opt("It can be instantiated directly with new"),
                    opt(
                        "It cannot be instantiated and may leave members for subclasses to implement",
                        correct=True,
                    ),
                    opt("It can only contain fully implemented methods"),
                    opt("It is the same thing as an interface in every way"),
                ),
                "An abstract class cannot be instantiated and may leave members for subclasses to implement.",
            ),
            q(
                "Which OOP pillar is described as properties guarding fields?",
                (
                    opt("Inheritance"),
                    opt("Polymorphism"),
                    opt("Encapsulation", correct=True),
                    opt("Abstraction"),
                ),
                "Encapsulation is when properties guard the underlying fields.",
            ),
        ),
        "Exception handling": (
            q(
                "What does the finally block do in a try/catch/finally statement?",
                (
                    opt("It runs only when no exception is thrown"),
                    opt("It always runs, making it the place for cleanup", correct=True),
                    opt("It catches the most specific exception type"),
                    opt("It re-throws the exception automatically"),
                ),
                "The finally block always runs, so cleanup goes there.",
            ),
            q(
                "Why does the lesson prefer throw; over throw ex; when re-throwing?",
                (
                    opt(
                        "throw; preserves the original stack trace while throw ex; resets it",
                        correct=True,
                    ),
                    opt("throw ex; preserves the stack trace while throw; discards it"),
                    opt("throw; suppresses the exception entirely"),
                    opt("There is no difference between the two"),
                ),
                "throw; with no argument rethrows while keeping the original stack trace, whereas throw ex; would reset it.",
            ),
            q(
                "What does a using declaration guarantee for a type that implements IDisposable?",
                (
                    opt(
                        "It disposes the object automatically when the scope ends, even if an exception is thrown",
                        correct=True,
                    ),
                    opt("It prevents the object from ever throwing an exception"),
                    opt("It keeps the object alive for the lifetime of the application"),
                    opt("It converts the object into a value type"),
                ),
                "A using declaration disposes the resource automatically when the scope ends, even if an exception is thrown.",
            ),
        ),
    },
    final=(
        q(
            "What runs the intermediate language that C# compiles to, and manages memory for you?",
            (
                opt("The dotnet CLI"),
                opt("The Common Language Runtime with its garbage collector", correct=True),
                opt("The Newtonsoft serializer"),
                opt("The static Main method"),
            ),
            "The CLR just-in-time compiles and runs the IL, and a garbage collector manages memory.",
        ),
        q(
            "Which statement about types in C# is correct based on the course?",
            (
                opt("var means the variable has no type at all"),
                opt(
                    "decimal is the recommended type for money because it avoids rounding error",
                    correct=True,
                ),
                opt("string is a value type that copies its data on assignment"),
                opt("int is a reference type stored on the heap"),
            ),
            "decimal is exact with no rounding error, making it the right choice for currency.",
        ),
        q(
            "Which pairing of a C# feature to its purpose is correct?",
            (
                opt("params is used to define a compile-time constant"),
                opt("The switch expression underscore _ is the default branch", correct=True),
                opt("virtual prevents a method from being overridden"),
                opt("TryGetValue throws when the key is missing"),
            ),
            "The underscore _ is the default branch in a switch expression, making it exhaustive.",
        ),
        q(
            "Which choice correctly describes a collection from the course?",
            (
                opt("Dictionary<K,V> is for key to value lookups", correct=True),
                opt("int[] grows automatically as you add items"),
                opt("List<T> requires a fixed size at creation"),
                opt("HashSet<T> stores items by integer index only"),
            ),
            "A Dictionary maps keys to values for fast look-ups by key.",
        ),
        q(
            "Which statement about exception handling and OOP is correct?",
            (
                opt("A bare catch (Exception) should be placed before more specific catches"),
                opt("throw; preserves the original stack trace when re-throwing", correct=True),
                opt("An abstract class can be instantiated directly with new"),
                opt("override is what allows a method to be overridden by subclasses"),
            ),
            "throw; with no argument rethrows while preserving the original stack trace.",
        ),
    ),
)
