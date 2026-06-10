"""Curated quiz questions for the C# - Intermediate course (per-lesson
checkpoints plus a final comprehensive quiz). Keys are the EXACT content-lesson
titles; the seed interleaves a checkpoint quiz after each."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Interfaces & abstraction": (
            q(
                "What does an interface define in C#?",
                (
                    opt("A class blueprint that includes private state and a constructor"),
                    opt(
                        "A contract listing members a type promises to provide, with no implementation",
                        correct=True,
                    ),
                    opt("A sealed type that cannot be implemented by any class"),
                    opt("A value type used only for immutable data"),
                ),
                "An interface is a contract: a list of members a type promises to provide, with no implementation.",
            ),
            q(
                "How many interfaces can a single C# class implement?",
                (
                    opt("Exactly one"),
                    opt("At most two"),
                    opt("Many", correct=True),
                    opt("None, interfaces can only be inherited by other interfaces"),
                ),
                "A class can implement many interfaces, which is how C# does polymorphism without single inheritance.",
            ),
            q(
                "According to the comparison, which capability belongs to an abstract class but NOT an interface?",
                (
                    opt("Being implemented by many unrelated types"),
                    opt("Holding state in fields and having constructors", correct=True),
                    opt("Declaring members without an implementation"),
                    opt("Expressing a can-do-X capability"),
                ),
                "The table shows an abstract class can hold state (fields) and have constructors, while an interface cannot.",
            ),
        ),
        "Records & value equality": (
            q(
                "When two records with identical contents are compared with ==, what is the result?",
                (
                    opt("False, because records compare references like classes"),
                    opt("True, because records compare values, not references", correct=True),
                    opt("A compile error, since records cannot use =="),
                    opt("It depends on whether the record is sealed"),
                ),
                "A record compares VALUES, so two records with the same contents are equal even though they are different objects.",
            ),
            q(
                "What does the with expression do to a record?",
                (
                    opt("Mutates the original record in place"),
                    opt(
                        "Makes a copy with some properties changed, leaving the original unchanged",
                        correct=True,
                    ),
                    opt("Converts the record into a class"),
                    opt("Deletes the specified properties from the record"),
                ),
                "Records are immutable by default; with makes a copy with some properties changed while the original is unchanged.",
            ),
            q(
                "What gives a record value semantics like a value type, per the lesson?",
                (
                    opt("Declaring it as a record struct", correct=True),
                    opt("Marking every property with the m suffix"),
                    opt("Adding a parameterless constructor"),
                    opt("Inheriting from System.ValueType manually"),
                ),
                "A record struct gives the same value semantics as a value type.",
            ),
        ),
        "Generics": (
            q(
                "What do generics let you write?",
                (
                    opt(
                        "A type or method parameterised by another type, type-safe and without boxing",
                        correct=True,
                    ),
                    opt("Code that only works with the object base type"),
                    opt("Methods that always return void"),
                    opt("Types that can never be constrained"),
                ),
                "Generics let you write a type or method parameterised by another type, type-safe and without boxing.",
            ),
            q(
                "What does the constraint where T : new() require of T?",
                (
                    opt("T is a reference type"),
                    opt("T is a value type"),
                    opt("T has a public parameterless constructor", correct=True),
                    opt("T is non-nullable"),
                ),
                "where T : new() means T must have a public parameterless constructor.",
            ),
            q(
                "In generic variance, what does the out keyword make a generic interface?",
                (
                    opt("Contravariant, a consumer"),
                    opt("Covariant, a producer", correct=True),
                    opt("Invariant and sealed"),
                    opt("A value type instead of a reference type"),
                ),
                "out makes a generic interface covariant (a producer), which is why IEnumerable of Dog is usable as IEnumerable of Animal.",
            ),
        ),
        "LINQ": (
            q(
                "What does LINQ bring to any IEnumerable of T?",
                (
                    opt("Automatic multithreading of every loop"),
                    opt(
                        "SQL-like querying over in-memory collections, databases, XML and more",
                        correct=True,
                    ),
                    opt("A replacement for the C# type system"),
                    opt("Direct access to unmanaged memory"),
                ),
                "LINQ (Language Integrated Query) brings SQL-like querying to any IEnumerable of T.",
            ),
            q(
                "Which operator returns the first match or a default value instead of throwing when none is found?",
                (
                    opt("First"),
                    opt("FirstOrDefault", correct=True),
                    opt("Any"),
                    opt("Single"),
                ),
                "FirstOrDefault returns the first match or a default, whereas First throws if there is no match.",
            ),
            q(
                "Because of deferred execution, when does a LINQ query actually run?",
                (
                    opt("Immediately when the query is declared"),
                    opt("Only when you enumerate it, such as with foreach or ToList", correct=True),
                    opt("Never, it is purely a compile-time construct"),
                    opt("Once per program, the first time the assembly loads"),
                ),
                "A LINQ query is a recipe that runs only when enumerated, for example via foreach, ToList or Count.",
            ),
        ),
        "Delegates, lambdas & events": (
            q(
                "What is a delegate in C#?",
                (
                    opt(
                        "A type-safe reference to a method that you can store and pass around",
                        correct=True,
                    ),
                    opt("A way to declare an immutable record"),
                    opt("A keyword that forces a method to run asynchronously"),
                    opt("A container for key-value pairs"),
                ),
                "A delegate is a type-safe reference to a method, a function you can store in a variable and pass around.",
            ),
            q(
                "Which built-in delegate returns nothing (void)?",
                (
                    opt("Func"),
                    opt("Action", correct=True),
                    opt("Predicate"),
                    opt("EventHandler of TArgs"),
                ),
                "Action returns nothing (void), while Func returns a value and Predicate returns a bool.",
            ),
            q(
                "Why is ?.Invoke used when raising an event?",
                (
                    opt("To run the event on a background thread"),
                    opt(
                        "To guard against raising an event that has no subscribers, which would be null",
                        correct=True,
                    ),
                    opt("To unsubscribe all handlers automatically"),
                    opt("To convert the event into a Task"),
                ),
                "The ?.Invoke guards against raising an event with no subscribers, which would otherwise be null.",
            ),
        ),
        "Asynchronous programming": (
            q(
                "What does await do in an async method?",
                (
                    opt("Blocks the thread until the operation completes"),
                    opt(
                        "Yields the thread while waiting and resumes the method when the awaited task completes",
                        correct=True,
                    ),
                    opt("Cancels the awaited task immediately"),
                    opt("Converts the result into a CancellationToken"),
                ),
                "await unwraps the result when the awaited task completes, resuming the method where it left off without blocking.",
            ),
            q(
                "How do you run two independent async operations concurrently rather than sequentially?",
                (
                    opt("Await each call on its own line one after another"),
                    opt(
                        "Start both tasks first, then await them together with Task.WhenAll",
                        correct=True,
                    ),
                    opt("Call .Result on both tasks"),
                    opt("Wrap them in a single using statement"),
                ),
                "Starting the tasks first and awaiting them together with Task.WhenAll makes total time about max(t1, t2) instead of t1 + t2.",
            ),
            q(
                "What is the golden rule of async stated in the lesson?",
                (
                    opt("Block on .Result whenever possible for simplicity"),
                    opt(
                        "Async all the way down: await async calls rather than blocking on .Result or .Wait()",
                        correct=True,
                    ),
                    opt("Always run async work on a new thread manually"),
                    opt("Never pass a CancellationToken to async methods"),
                ),
                "The golden rule is async all the way down: await async calls rather than blocking on .Result or .Wait(), which can deadlock.",
            ),
        ),
        "Files & JSON": (
            q(
                "In server code, why prefer File.ReadAllTextAsync over File.ReadAllText?",
                (
                    opt("It validates the file as JSON before reading"),
                    opt("It avoids blocking a thread on disk I/O", correct=True),
                    opt("It is the only method that can read text files"),
                    opt("It encrypts the file contents automatically"),
                ),
                "The async file helpers avoid blocking a thread on disk I/O, which you should prefer in server code.",
            ),
            q(
                "Which built-in serializer does the lesson present as the modern, fast choice for JSON?",
                (
                    opt("Newtonsoft.Json"),
                    opt("System.Text.Json", correct=True),
                    opt("System.Xml.Serialization"),
                    opt("DataContractSerializer"),
                ),
                "System.Text.Json is the modern, fast, built-in choice, while the older Newtonsoft.Json is still common in legacy code.",
            ),
            q(
                "What does Path.Combine do?",
                (
                    opt("Reads all lines of a file into an array"),
                    opt("Builds file paths portably"),
                    opt("Builds paths portably across operating systems", correct=True),
                    opt("Serializes an object to a JSON file"),
                ),
                "Path.Combine builds paths portably, joining segments correctly across platforms.",
            ),
        ),
    },
    final=(
        q(
            "How does an interface differ from an abstract class regarding inheritance?",
            (
                opt("Both allow only a single base type"),
                opt(
                    "A class can implement many interfaces but inherit only one base class",
                    correct=True,
                ),
                opt("Interfaces support constructors while abstract classes do not"),
                opt(
                    "Abstract classes can be implemented by many unrelated types but interfaces cannot"
                ),
            ),
            "A class can implement many interfaces but can inherit only one base (abstract) class.",
        ),
        q(
            "What is the defining feature of a record compared with a class?",
            (
                opt("It can never be inherited"),
                opt("It compares by value rather than by reference", correct=True),
                opt("It is always a value type allocated on the stack"),
                opt("It cannot have computed members"),
            ),
            "A record is built for immutable data and uses value-based equality, so equal contents mean equal records.",
        ),
        q(
            "Which LINQ behaviour means a query runs only when enumerated?",
            (
                opt("Eager execution"),
                opt("Deferred execution", correct=True),
                opt("Covariance"),
                opt("Boxing"),
            ),
            "Deferred execution means a LINQ query is a recipe that runs only when you enumerate it.",
        ),
        q(
            "What does Task.WhenAll enable when working with multiple async operations?",
            (
                opt(
                    "Running independent tasks concurrently and awaiting them together",
                    correct=True,
                ),
                opt("Cancelling all tasks if any one fails"),
                opt("Forcing tasks to run strictly one after another"),
                opt("Blocking the calling thread until the first task finishes"),
            ),
            "Task.WhenAll lets you start independent tasks first and await them together, so they run concurrently.",
        ),
        q(
            "Which library does the course recommend for serializing objects to JSON in modern C#?",
            (
                opt("Newtonsoft.Json"),
                opt("System.Text.Json", correct=True),
                opt("System.Xml.Serialization"),
                opt("System.Runtime.Serialization"),
            ),
            "System.Text.Json is the modern, fast, built-in serializer recommended for new code.",
        ),
    ),
)
