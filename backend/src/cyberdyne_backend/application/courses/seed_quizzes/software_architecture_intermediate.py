"""Quizzes for Software Architecture - Intermediate (checkpoints + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "MVVM and MVP": (
            q(
                "In MVVM, how does the View stay in sync with the ViewModel?",
                (
                    opt("The ViewModel calls methods on the View directly"),
                    opt(
                        "The View binds to observable state on the ViewModel (data binding)",
                        correct=True,
                    ),
                    opt("A controller polls the model every second"),
                    opt("The View reads the database directly"),
                ),
                "In MVVM the View binds to the ViewModel's observable state and updates "
                "automatically. The ViewModel holds no reference to the View.",
            ),
            q(
                "In MVP, why is the View defined behind an interface?",
                (
                    opt("To make the View render faster"),
                    opt(
                        "So the Presenter can drive a passive View through a mockable "
                        "interface, making its logic unit-testable",
                        correct=True,
                    ),
                    opt("Because interfaces are required by all UI frameworks"),
                    opt("To let the View access the database"),
                ),
                "MVP uses a passive View behind an interface; the Presenter updates it via "
                "that interface, which can be mocked, so presenter logic is testable "
                "without a UI.",
            ),
            q(
                "What is the key difference between MVVM and MVP?",
                (
                    opt("MVVM has no model; MVP has no view"),
                    opt(
                        "MVVM relies on data binding and the ViewModel never references the "
                        "View; MVP's Presenter drives the View through an interface",
                        correct=True,
                    ),
                    opt("MVP is only for web; MVVM is only for databases"),
                    opt("They are identical patterns with different names"),
                ),
                "MVVM uses automatic data binding (ViewModel unaware of the View); MVP has "
                "the Presenter explicitly update a passive View via an interface.",
            ),
        ),
        "GoF design patterns overview": (
            q(
                "Which family does the Adapter pattern belong to?",
                (
                    opt("Creational"),
                    opt("Structural", correct=True),
                    opt("Behavioural"),
                    opt("Concurrency"),
                ),
                "Adapter is a structural pattern: it composes objects to make one "
                "interface fit another. Factory is creational; Strategy/Observer are "
                "behavioural.",
            ),
            q(
                "What problem does the Strategy pattern solve?",
                (
                    opt("Ensuring only one instance of a class exists"),
                    opt(
                        "Making an algorithm interchangeable at runtime via a common interface",
                        correct=True,
                    ),
                    opt("Converting an incompatible interface to an expected one"),
                    opt("Building a complex object step by step"),
                ),
                "Strategy encapsulates interchangeable algorithms behind one interface so "
                "the client can swap behaviour (e.g. pricing rules) without changing its "
                "own code.",
            ),
            q(
                "The Observer pattern is best described as:",
                (
                    opt("A way to create objects without naming their class"),
                    opt(
                        "A subject notifying many dependent observers when its state changes",
                        correct=True,
                    ),
                    opt("Wrapping a legacy class to fit a new interface"),
                    opt("Restricting a class to a single instance"),
                ),
                "Observer defines a one-to-many dependency: when the subject's state "
                "changes, all registered observers are notified - the basis of "
                "event/notification systems.",
            ),
        ),
        "Component, package & dependency diagrams": (
            q(
                "What is the golden rule for dependencies between packages?",
                (
                    opt("Every package should depend on every other"),
                    opt(
                        "Dependencies should form a directed acyclic graph - no cycles",
                        correct=True,
                    ),
                    opt("Packages should never depend on anything"),
                    opt("Cycles are fine as long as they are documented"),
                ),
                "Package dependencies should be acyclic. Cycles make modules impossible to "
                "build, test, or ship independently.",
            ),
            q(
                "With the Dependency Inversion Principle applied at the package level, "
                "which way does infrastructure depend?",
                (
                    opt("The domain depends on infrastructure's concrete classes"),
                    opt(
                        "Infrastructure depends on ports/interfaces defined near the "
                        "domain, not the reverse",
                        correct=True,
                    ),
                    opt("Neither depends on the other"),
                    opt("They depend on the web layer equally"),
                ),
                "DIP flips the arrow: infrastructure (a volatile detail) depends on the "
                "stable abstractions (ports) owned by the domain side.",
            ),
            q(
                "In component diagrams, the `lollipop and socket` notation shows what?",
                (
                    opt("Database tables and their indexes"),
                    opt(
                        "Provided interfaces (lollipop) and required interfaces (socket)",
                        correct=True,
                    ),
                    opt("Threads and processes"),
                    opt("Inheritance hierarchies"),
                ),
                "A component provides interfaces (the lollipop) and requires others (the "
                "socket); wiring a required interface to a provider composes the system.",
            ),
        ),
        "Domain-Driven Design basics": (
            q(
                "What distinguishes a Value Object from an Entity in DDD?",
                (
                    opt("A Value Object has identity; an Entity does not"),
                    opt(
                        "A Value Object is defined only by its attributes and has no "
                        "identity; an Entity has a stable identity over time",
                        correct=True,
                    ),
                    opt("Value Objects are stored in the database; entities are not"),
                    opt("There is no difference"),
                ),
                "An Entity is defined by a continuous identity (e.g. a `Customer` id); a "
                "Value Object is defined purely by its attributes and is typically "
                "immutable (e.g. `Money`).",
            ),
            q(
                "What is the role of an aggregate root?",
                (
                    opt("It is a database connection pool"),
                    opt(
                        "It is the single entry point to an aggregate, enforcing the "
                        "cluster's invariants",
                        correct=True,
                    ),
                    opt("It renders the UI for the aggregate"),
                    opt("It is the network gateway for the service"),
                ),
                "The aggregate root is the only object outside code accesses; it guards the "
                "consistency boundary, so you never modify inner entities directly.",
            ),
            q(
                "What is a bounded context?",
                (
                    opt("A limit on how many classes a package may have"),
                    opt(
                        "A boundary within which a model and its ubiquitous language are "
                        "consistent",
                        correct=True,
                    ),
                    opt("A timeout for database transactions"),
                    opt("A rule that forbids interfaces"),
                ),
                "A bounded context is a boundary inside which one model and its language "
                "stay consistent - the same word (e.g. `Customer`) can mean different "
                "things in different contexts.",
            ),
        ),
        "API & integration design": (
            q(
                "In REST, which HTTP verb is conventionally used to create a new resource?",
                (
                    opt("`GET`"),
                    opt("`POST`", correct=True),
                    opt("`DELETE`"),
                    opt("`OPTIONS`"),
                ),
                "`POST /orders` creates a new order (often returning `201 Created` with a "
                "`Location` header). `GET` reads, `PUT/PATCH` update, `DELETE` removes.",
            ),
            q(
                "What does it mean that REST is `stateless`?",
                (
                    opt("The server never stores any data"),
                    opt(
                        "Each request carries everything needed to process it; the server "
                        "keeps no client session state between requests",
                        correct=True,
                    ),
                    opt("Clients cannot send any data"),
                    opt("Responses are always empty"),
                ),
                "Statelessness means each request is self-contained; the server does not "
                "rely on stored per-client session context, which aids scalability.",
            ),
            q(
                "Why version an API and only add (not remove) fields?",
                (
                    opt("To make responses larger"),
                    opt(
                        "To evolve the contract without breaking existing clients that "
                        "depend on current behaviour",
                        correct=True,
                    ),
                    opt("Because REST forbids deleting endpoints"),
                    opt("To improve raw performance"),
                ),
                "An API is a published contract. Versioning and additive-only changes let "
                "you evolve it while keeping backward compatibility for unseen consumers.",
            ),
        ),
        "Architectural quality attributes & trade-offs": (
            q(
                "What is horizontal scaling?",
                (
                    opt("Making a single machine bigger (more CPU/RAM)"),
                    opt("Adding more machines, which usually requires statelessness", correct=True),
                    opt("Deleting unused code"),
                    opt("Caching every response forever"),
                ),
                "Horizontal scaling adds more machines (scale out) and typically needs "
                "stateless services; vertical scaling makes one machine bigger (scale up).",
            ),
            q(
                "Which is a real trade-off when adding caching?",
                (
                    opt(
                        "It improves performance but can hurt data freshness/consistency",
                        correct=True,
                    ),
                    opt("It improves both performance and consistency with no cost"),
                    opt("It always reduces system complexity"),
                    opt("It removes the need for a database"),
                ),
                "Caching trades freshness for speed: cached data may be stale. Every "
                "architectural improvement tends to cost another attribute.",
            ),
            q(
                "Why express quality requirements as measurable scenarios?",
                (
                    opt("Because UML requires it"),
                    opt(
                        "So options can be evaluated objectively and conflicting "
                        "attributes surfaced and chosen consciously",
                        correct=True,
                    ),
                    opt("To make documentation longer"),
                    opt("Because vague goals are easier to test"),
                ),
                "Measurable scenarios (e.g. `respond in under 300 ms at p95 with 1,000 "
                "users`) make trade-offs concrete and evaluable - the basis of methods "
                "like ATAM.",
            ),
        ),
    },
    final=(
        q(
            "Which pattern uses automatic data binding so the ViewModel never references the View?",
            (
                opt("MVC"),
                opt("MVP"),
                opt("MVVM", correct=True),
                opt("Layered architecture"),
            ),
            "MVVM binds the View to observable ViewModel state; the ViewModel is unaware "
            "of the View. MVP instead drives a passive View through an interface.",
        ),
        q(
            "Which GoF pattern converts one class's interface into the one a client expects?",
            (
                opt("Observer"),
                opt("Adapter", correct=True),
                opt("Strategy"),
                opt("Factory Method"),
            ),
            "Adapter (structural) wraps an incompatible class so it satisfies the "
            "interface the calling code expects.",
        ),
        q(
            "What rule keeps a package dependency graph healthy?",
            (
                opt("It must contain at least one cycle"),
                opt(
                    "It must be acyclic, with dependencies pointing toward stable abstractions",
                    correct=True,
                ),
                opt("Every package must depend on the web layer"),
                opt("Packages must never expose interfaces"),
            ),
            "Dependencies should form a DAG and point toward stable abstractions (and "
            "toward the domain), which is the Dependency Inversion Principle at scale.",
        ),
        q(
            "In DDD, what is an aggregate?",
            (
                opt("A single immutable value with no identity"),
                opt(
                    "A cluster of objects treated as one consistency boundary, accessed "
                    "through its root",
                    correct=True,
                ),
                opt("A database index"),
                opt("A UI component"),
            ),
            "An aggregate groups entities and value objects under one consistency "
            "boundary; only the aggregate root is accessed from outside.",
        ),
        q(
            "Which property of REST most helps horizontal scalability?",
            (
                opt("It requires XML payloads"),
                opt("It is stateless - each request is self-contained", correct=True),
                opt("It forbids caching"),
                opt("It mandates a single server"),
            ),
            "Statelessness lets any server handle any request without shared session "
            "state, so you can add servers freely.",
        ),
        q(
            "Why must architects rank quality attributes rather than maximise all of them?",
            (
                opt("Because tools only allow one attribute at a time"),
                opt(
                    "Because attributes trade off against each other; improving one often "
                    "costs another",
                    correct=True,
                ),
                opt("Because ranking makes the system slower on purpose"),
                opt("Because UML requires a ranked list"),
            ),
            "You cannot maximise everything; caching, microservices, and abstraction each "
            "buy one attribute at another's expense, so you rank and choose consciously.",
        ),
    ),
)
