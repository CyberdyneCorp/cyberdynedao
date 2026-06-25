"""Quizzes for Software Architecture - Basics (per-lesson checkpoints + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "What is software architecture": (
            q(
                "What best distinguishes architecture from design?",
                (
                    opt("Architecture is about syntax; design is about semantics"),
                    opt(
                        "Architecture covers the high-level, hard-to-change structural "
                        "decisions; design covers localised implementation detail",
                        correct=True,
                    ),
                    opt("Architecture is done by managers; design is done by developers"),
                    opt("There is no difference; the terms are interchangeable"),
                ),
                "Architecture is the set of significant, hard-to-reverse structural "
                "decisions and trade-offs; design is the lower-level detail inside a "
                "component.",
            ),
            q(
                "Which of these is a `quality attribute` (an `-ility`) that architecture "
                "aims to enable?",
                (
                    opt("Indentation style"),
                    opt("Maintainability", correct=True),
                    opt("The choice of variable names"),
                    opt("The number of code comments"),
                ),
                "Maintainability, scalability, testability, reliability, and security are "
                "quality attributes that a good architecture is meant to make achievable.",
            ),
            q(
                "Why is recording the reasoning behind big decisions valuable?",
                (
                    opt("It is required by the UML standard"),
                    opt(
                        "Architecture is a set of decisions you revisit, so capturing the "
                        "`why` helps future maintainers understand the trade-offs",
                        correct=True,
                    ),
                    opt("It makes the code run faster"),
                    opt("It removes the need for any testing"),
                ),
                "Architecture is an ongoing set of decisions, not a one-off phase. "
                "Recording the why (e.g. in an ADR) preserves the trade-off context.",
            ),
        ),
        "UML essentials — class diagrams": (
            q(
                "In a UML class diagram, what does a filled (solid) diamond represent?",
                (
                    opt("Inheritance"),
                    opt(
                        "Composition - an owned `has-a` with shared lifecycle ending", correct=True
                    ),
                    opt("A simple association"),
                    opt("Interface realisation"),
                ),
                "A filled diamond is composition: the part is owned by the whole and dies "
                "with it (e.g. an `Order` owns its `OrderLine`s). A hollow diamond is "
                "aggregation (shared lifecycle).",
            ),
            q(
                "Which relationship means `is-a` and uses a hollow triangle arrowhead?",
                (
                    opt("Aggregation"),
                    opt("Association"),
                    opt("Inheritance (generalisation)", correct=True),
                    opt("Composition"),
                ),
                "Inheritance/generalisation expresses an `is-a` relationship and is drawn "
                "with a hollow triangle pointing at the parent class.",
            ),
            q(
                "What does the multiplicity `1..*` on an association end mean?",
                (
                    opt("Exactly one"),
                    opt("Zero or one"),
                    opt("One or more", correct=True),
                    opt("Zero or more"),
                ),
                "`1..*` means one or more. `0..*` (or `*`) is zero or more, `0..1` is zero "
                "or one, and `1` is exactly one.",
            ),
        ),
        "UML behavior — use-case & sequence diagrams": (
            q(
                "What does a use-case diagram primarily capture?",
                (
                    opt("The order of method calls between objects"),
                    opt("The actors and the goals (use cases) the system supports", correct=True),
                    opt("The database tables and their columns"),
                    opt("The deployment topology of servers"),
                ),
                "A use-case diagram captures functional scope: the actors (users/external "
                "systems) and the use cases (goals) they pursue. It is a scope tool, not a "
                "design.",
            ),
            q(
                "On a sequence diagram, what is shown along the vertical axis?",
                (
                    opt("Class inheritance depth"),
                    opt("Time - messages are ordered from top to bottom", correct=True),
                    opt("Memory usage"),
                    opt("Network bandwidth"),
                ),
                "A sequence diagram orders messages over time, top to bottom, along each "
                "object's lifeline - it shows who calls whom and in what order.",
            ),
            q(
                "Which UML diagram best models a single object moving through allowed "
                "states and transitions?",
                (
                    opt("Class diagram"),
                    opt("Use-case diagram"),
                    opt("State machine (state) diagram", correct=True),
                    opt("Component diagram"),
                ),
                "A state machine diagram captures an object's lifecycle: its states and the "
                "transitions allowed between them (e.g. `Pending -> Paid -> Shipped`).",
            ),
        ),
        "Design principles & best practices": (
            q(
                "What does the `D` in SOLID (Dependency Inversion) advise?",
                (
                    opt("Always duplicate code for safety"),
                    opt("Depend on abstractions, not on concrete implementations", correct=True),
                    opt("Make every class a singleton"),
                    opt("Avoid using interfaces entirely"),
                ),
                "Dependency Inversion says high-level policy should depend on an "
                "abstraction (interface), and details should implement it - so concrete "
                "classes can be swapped without changing the policy.",
            ),
            q(
                "What is the goal expressed by `loose coupling, high cohesion`?",
                (
                    opt("Modules depend heavily on each other but do unrelated things"),
                    opt(
                        "Modules depend little on each other, and each module's contents "
                        "are closely related",
                        correct=True,
                    ),
                    opt("All code lives in one large class"),
                    opt("Every function is duplicated across modules"),
                ),
                "Loose coupling = few inter-module dependencies; high cohesion = the things "
                "inside a module belong together. Together they make systems easier to "
                "change.",
            ),
            q(
                "Which principle warns against building features for an imagined future need?",
                (
                    opt("DRY"),
                    opt("YAGNI - You Aren't Gonna Need It", correct=True),
                    opt("Liskov Substitution"),
                    opt("Single Responsibility"),
                ),
                "YAGNI advises against speculative generality - build what is needed now. "
                "DRY targets duplication, and KISS targets unnecessary complexity.",
            ),
        ),
        "Layered (n-tier) architecture": (
            q(
                "In a classic layered architecture, which way do dependencies point?",
                (
                    opt("Each layer depends on the layer above it"),
                    opt("Each layer depends only on the layer below it", correct=True),
                    opt("Every layer depends on every other layer"),
                    opt("Layers have no dependencies at all"),
                ),
                "In layered architecture dependencies point downward: presentation -> "
                "application -> domain -> infrastructure. Higher layers never reach up.",
            ),
            q(
                "What is the `sinkhole` anti-pattern in layered architecture?",
                (
                    opt("A layer that caches too aggressively"),
                    opt(
                        "Requests passing straight through layers that add no value, only "
                        "delegating",
                        correct=True,
                    ),
                    opt("A layer that is missing entirely"),
                    opt("Two layers that share a database"),
                ),
                "The sinkhole/architecture-sinkhole anti-pattern is when layers merely "
                "forward calls without adding logic - a sign a layer may not earn its place.",
            ),
            q(
                "Which layer holds the core business rules and entities?",
                (
                    opt("Presentation layer"),
                    opt("Domain / business layer", correct=True),
                    opt("Infrastructure layer"),
                    opt("The web server"),
                ),
                "The domain (business) layer is the heart of the system - the rules and "
                "entities. Presentation handles I/O and infrastructure handles persistence "
                "and external services.",
            ),
        ),
        "The MVC pattern": (
            q(
                "In MVC, what is the Controller's responsibility?",
                (
                    opt("Holding the business rules and data"),
                    opt(
                        "Handling input, updating the model, and selecting the view to render",
                        correct=True,
                    ),
                    opt("Rendering the final HTML markup"),
                    opt("Storing rows in the database directly"),
                ),
                "The controller is the glue: it handles user input, tells the model to "
                "update, and chooses the view. The model holds rules/data; the view renders.",
            ),
            q(
                "Why does MVC keep the View free of business logic?",
                (
                    opt("Because views cannot contain any code at all"),
                    opt(
                        "So presentation can change independently and the model can be "
                        "tested without a UI",
                        correct=True,
                    ),
                    opt("Because the view is compiled separately"),
                    opt("To make the controller larger"),
                ),
                "Separating presentation from business rules lets you restyle the view "
                "without touching logic, test the model without a browser, and reuse one "
                "model across many views.",
            ),
            q(
                "What is the `fat controller` smell, and the recommended fix?",
                (
                    opt("A controller with too few methods; add more"),
                    opt(
                        "A controller that accumulates business logic; push that logic down "
                        "into the model or a service",
                        correct=True,
                    ),
                    opt("A controller that renders HTML; that is correct and fine"),
                    opt("A controller written in the wrong language"),
                ),
                "Controllers should stay thin. When they grow business rules, move that "
                "logic into the model (or a service the model uses) to keep concerns "
                "separated.",
            ),
        ),
    },
    final=(
        q(
            "Which statement about architecture vs. design is correct?",
            (
                opt("Design decisions are always harder to reverse than architectural ones"),
                opt(
                    "Architectural decisions are the structural, hard-to-change ones; "
                    "design is more localised detail",
                    correct=True,
                ),
                opt("Architecture only concerns the database schema"),
                opt("Design covers technology choices like the message broker"),
            ),
            "Architecture is about significant, structural, hard-to-reverse decisions and "
            "trade-offs; design handles lower-level, more changeable implementation detail.",
        ),
        q(
            "A hollow diamond on a UML class diagram denotes which relationship?",
            (
                opt("Composition (owned, dies with the whole)"),
                opt("Aggregation (shared lifecycle, part can outlive the whole)", correct=True),
                opt("Inheritance"),
                opt("Interface realisation"),
            ),
            "A hollow diamond is aggregation - a `has-a` where the part has an independent "
            "lifecycle. A filled diamond is composition (owned lifecycle).",
        ),
        q(
            "Which UML diagram shows objects exchanging messages over time?",
            (
                opt("Class diagram"),
                opt("Sequence diagram", correct=True),
                opt("Use-case diagram"),
                opt("Package diagram"),
            ),
            "A sequence diagram is an interaction diagram: lifelines exchange messages "
            "ordered top-to-bottom in time, ideal for reasoning about collaborations.",
        ),
        q(
            "Which SOLID principle says `a class should have one reason to change`?",
            (
                opt("Open/Closed Principle"),
                opt("Single Responsibility Principle", correct=True),
                opt("Liskov Substitution Principle"),
                opt("Interface Segregation Principle"),
            ),
            "Single Responsibility: a class should do one thing, so it has a single reason "
            "to change. This drives high cohesion.",
        ),
        q(
            "In layered architecture, where should business rules live?",
            (
                opt("In the presentation layer"),
                opt("In the domain/business layer", correct=True),
                opt("In the infrastructure layer"),
                opt("Spread evenly across all layers"),
            ),
            "Business rules belong in the domain layer - the heart of the system - so they "
            "are not coupled to the UI or to persistence concerns.",
        ),
        q(
            "Which mapping of MVC responsibilities is correct?",
            (
                opt("Model renders HTML; View stores data; Controller holds rules"),
                opt(
                    "Model holds data/rules; View renders presentation; Controller handles "
                    "input and coordinates",
                    correct=True,
                ),
                opt("Model handles input; Controller renders; View holds the database"),
                opt("All three do the same job for redundancy"),
            ),
            "Model = data and rules; View = presentation/rendering; Controller = input "
            "handling and coordination between model and view.",
        ),
    ),
)
