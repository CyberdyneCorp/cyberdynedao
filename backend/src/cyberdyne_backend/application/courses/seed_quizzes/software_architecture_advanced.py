"""Quizzes for Software Architecture - Advanced (checkpoints + final)."""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "Hexagonal architecture (Ports & Adapters)": (
            q(
                "What is a `port` in hexagonal architecture?",
                (
                    opt("A network socket the application listens on"),
                    opt(
                        "A technology-agnostic interface defined by the core describing "
                        "what it needs or offers",
                        correct=True,
                    ),
                    opt("A concrete database driver"),
                    opt("A UI component"),
                ),
                "A port is an interface owned by the core. An adapter is the concrete, "
                "technology-specific implementation that plugs into a port.",
            ),
            q(
                "Which is a driving (primary) adapter?",
                (
                    opt("A SQL repository the core calls out to"),
                    opt("An SMTP email sender"),
                    opt("A REST controller that calls into the core", correct=True),
                    opt("A message-queue publisher used by the core"),
                ),
                "Driving/primary adapters call into the core via inbound ports (REST "
                "controller, CLI, tests). Driven/secondary adapters (SQL, SMTP) are called "
                "by the core via outbound ports.",
            ),
            q(
                "What does the hexagonal dependency rule require?",
                (
                    opt("The core depends on the database and web framework"),
                    opt(
                        "All dependencies point inward; the core depends on no external technology",
                        correct=True,
                    ),
                    opt("Adapters must not depend on ports"),
                    opt("Every layer depends on every other"),
                ),
                "Dependencies point inward toward the core. Adapters depend on the core's "
                "ports; the core depends on nothing external - so you can test it with "
                "fakes and swap technologies freely.",
            ),
        ),
        "Clean & Onion architecture": (
            q(
                "In Clean/Onion architecture, which code is the most stable, at the centre?",
                (
                    opt("The web framework"),
                    opt("The database driver"),
                    opt("The entities / domain", correct=True),
                    opt("The UI templates"),
                ),
                "The innermost ring holds entities/domain - enterprise business rules, the "
                "most stable code. Frameworks, DBs, and UI are outer `details`.",
            ),
            q(
                "What does the dependency rule say about source-code dependencies?",
                (
                    opt("They may point in any direction if documented"),
                    opt(
                        "They point only inward; an inner ring never names an outer ring",
                        correct=True,
                    ),
                    opt("They must point outward toward frameworks"),
                    opt("Inner rings depend on the database directly"),
                ),
                "Source dependencies point only inward. Crossing a boundary outward-to-"
                "inward uses an interface the inner ring owns (Dependency Inversion).",
            ),
            q(
                "How do Hexagonal, Onion, and Clean architecture relate?",
                (
                    opt("They are unrelated and contradictory styles"),
                    opt(
                        "They share the same dependency rule (point inward, protect the "
                        "domain) and differ mainly in vocabulary and emphasis",
                        correct=True,
                    ),
                    opt("Only Clean uses interfaces; the others forbid them"),
                    opt("Onion requires microservices; the others forbid them"),
                ),
                "All three enforce the same inward dependency rule to protect the domain; "
                "they differ in terminology (ports/adapters vs rings) and emphasis, not "
                "essence.",
            ),
        ),
        "Monolith, microservices & modular monolith": (
            q(
                "What defines a modular monolith?",
                (
                    opt("Many independently deployable services, each with its own database"),
                    opt(
                        "A single deployable with strongly enforced internal module boundaries",
                        correct=True,
                    ),
                    opt("A monolith with no structure at all"),
                    opt("A UI-only application"),
                ),
                "A modular monolith ships as one deployable but enforces clear module "
                "boundaries (separate schemas, no reaching into internals) - much of the "
                "clarity of microservices without distributed-systems cost.",
            ),
            q(
                "Service boundaries are best aligned with what?",
                (
                    opt("Technical layers (UI, logic, data)"),
                    opt("Bounded contexts / business capabilities", correct=True),
                    opt("Team seating arrangements"),
                    opt("The number of database tables"),
                ),
                "Good boundaries follow bounded contexts so each service owns a coherent "
                "slice of the business and its data. Splitting by technical layer creates "
                "chatty, coupled services.",
            ),
            q(
                "What is a `distributed monolith`?",
                (
                    opt("A monolith deployed to many regions for resilience"),
                    opt(
                        "Microservices so tightly coupled they must be deployed together - "
                        "the cost of distribution without the autonomy",
                        correct=True,
                    ),
                    opt("A modular monolith with two databases"),
                    opt("A correctly designed microservice system"),
                ),
                "A distributed monolith has services that cannot be released "
                "independently, so you pay network and operational costs while losing the "
                "independence microservices are meant to provide.",
            ),
        ),
        "Event-driven architecture, CQRS & event sourcing": (
            q(
                "What is the difference between a command and an event?",
                (
                    opt("Commands are facts; events are intents"),
                    opt(
                        "A command is an intent directed at one handler and may be "
                        "rejected; an event is a past-tense fact broadcast to many",
                        correct=True,
                    ),
                    opt("They are the same thing"),
                    opt("Events can be rejected; commands cannot"),
                ),
                "A command (`PlaceOrder`) is an intent that may fail; an event "
                "(`OrderPlaced`) is an immutable fact about the past, broadcast to any "
                "interested consumers.",
            ),
            q(
                "What does CQRS separate?",
                (
                    opt("The UI from the database"),
                    opt("The write model (commands) from the read model (queries)", correct=True),
                    opt("Authentication from authorisation"),
                    opt("Logging from monitoring"),
                ),
                "CQRS splits the command/write side (enforcing invariants) from the "
                "query/read side (denormalised views optimised for display), so each can "
                "evolve and scale independently.",
            ),
            q(
                "In event sourcing, what is the source of truth?",
                (
                    opt("A single row holding the current state"),
                    opt(
                        "The ordered sequence of events, replayed to derive current state",
                        correct=True,
                    ),
                    opt("A cache of the latest read model"),
                    opt("The UI session"),
                ),
                "Event sourcing stores the append-only sequence of events; current state "
                "is derived by folding (replaying) them - giving a full audit trail at the "
                "cost of eventual consistency and event versioning.",
            ),
        ),
        "Documenting architecture — C4, ADRs & 4+1": (
            q(
                "What are the four levels of the C4 model, from highest zoom to lowest?",
                (
                    opt("Code, Component, Container, Context"),
                    opt("Context, Container, Component, Code", correct=True),
                    opt("Class, Cluster, Cloud, Code"),
                    opt("Customer, Contract, Container, Code"),
                ),
                "C4 zooms from System Context (highest) to Container, then Component, then "
                "Code (often skipped in favour of UML). You draw only the levels you need.",
            ),
            q(
                "What does an Architecture Decision Record (ADR) capture?",
                (
                    opt("The full source code of a module"),
                    opt(
                        "A single significant decision: its context, the decision, and its consequences",
                        correct=True,
                    ),
                    opt("The deployment script for the system"),
                    opt("A list of open bugs"),
                ),
                "An ADR is a short, immutable, numbered record of one decision - context, "
                "decision, consequences - committed with the code so the `why` is "
                "preserved.",
            ),
            q(
                "In the 4+1 view model, what is the `+1`?",
                (
                    opt("The deployment view"),
                    opt("Scenarios (use cases) that tie the four views together", correct=True),
                    opt("An extra database view"),
                    opt("The security view"),
                ),
                "The `+1` is scenarios/use cases, which illustrate and validate the "
                "logical, process, development, and physical views together.",
            ),
        ),
        "Evolution & anti-patterns": (
            q(
                "What characterises a `Big Ball of Mud`?",
                (
                    opt("Excessive use of design patterns"),
                    opt(
                        "No discernible structure and pervasive coupling, so every change is risky",
                        correct=True,
                    ),
                    opt("Too many small, well-separated modules"),
                    opt("A strict layered architecture"),
                ),
                "A Big Ball of Mud is the lack of deliberate structure: tangled, pervasive "
                "coupling where any change can break anything - usually the product of "
                "time pressure and no architectural care.",
            ),
            q(
                "What is a `fitness function` in architecture?",
                (
                    opt("A function that benchmarks CPU speed once at startup"),
                    opt(
                        "An automated test that verifies an architectural characteristic "
                        "holds, failing the build if violated",
                        correct=True,
                    ),
                    opt("A UI animation helper"),
                    opt("A database stored procedure"),
                ),
                "A fitness function automates an architectural rule (e.g. `domain must not "
                "import infrastructure`) so a violation fails CI instead of decaying "
                "silently.",
            ),
            q(
                "What does the Strangler Fig pattern describe?",
                (
                    opt("Rewriting the whole system at once"),
                    opt(
                        "Growing a new structure around the old and redirecting capability "
                        "by capability until the old is removed",
                        correct=True,
                    ),
                    opt("Deleting all tests to move faster"),
                    opt("Merging all microservices into one"),
                ),
                "Strangler Fig migrates incrementally: route traffic to new components "
                "piece by piece behind a facade, shrinking the legacy system until it can "
                "be deleted safely.",
            ),
        ),
    },
    final=(
        q(
            "In hexagonal architecture, which direction do all dependencies point?",
            (
                opt("Outward, toward the database and frameworks"),
                opt("Inward, toward the application core", correct=True),
                opt("In both directions equally"),
                opt("Toward whichever adapter is fastest"),
            ),
            "All dependencies point inward toward the core; adapters depend on the core's "
            "ports, never the reverse, keeping the core technology-agnostic and testable.",
        ),
        q(
            "What do Hexagonal, Clean, and Onion architecture have in common?",
            (
                opt("They all require microservices"),
                opt(
                    "They enforce the same inward dependency rule to protect the domain",
                    correct=True,
                ),
                opt("They forbid the use of interfaces"),
                opt("They put the database at the centre"),
            ),
            "They are the same discipline in different vocabulary: dependencies point "
            "inward and the domain is isolated from frameworks and infrastructure.",
        ),
        q(
            "Why start a new system as a modular monolith rather than microservices?",
            (
                opt("Because microservices cannot use a database"),
                opt(
                    "It keeps operational simplicity while preserving clean boundaries you "
                    "can later extract into services when a real need appears",
                    correct=True,
                ),
                opt("Because monoliths cannot have modules"),
                opt("Because microservices are always slower"),
            ),
            "A modular monolith avoids distributed-systems complexity up front while "
            "keeping boundaries strong enough to extract a service later when independent "
            "scaling or deployment is genuinely needed.",
        ),
        q(
            "In CQRS, what is the role of a projector?",
            (
                opt("It validates incoming commands"),
                opt("It updates read models from events emitted by the write side", correct=True),
                opt("It encrypts the database"),
                opt("It routes HTTP requests"),
            ),
            "After the write model emits events, a projector updates one or more "
            "denormalised read models shaped for their queries - decoupling reads from "
            "writes.",
        ),
        q(
            "Which C4 diagram is the highest-level view, suitable for any stakeholder?",
            (
                opt("Code diagram"),
                opt("Component diagram"),
                opt("System Context diagram", correct=True),
                opt("Container diagram"),
            ),
            "The System Context diagram shows the system, its users, and external systems "
            "at the highest zoom - the right starting point for non-technical readers.",
        ),
        q(
            "How do you best recover from a Big Ball of Mud?",
            (
                opt("Rewrite everything from scratch in one release"),
                opt(
                    "Establish a boundary, guard it with a fitness function, and strangle "
                    "the worst parts incrementally",
                    correct=True,
                ),
                opt("Add more global variables to simplify access"),
                opt("Delete the tests so changes are faster"),
            ),
            "You evolve out of a mud ball with small, enforced steps: create a seam, add a "
            "fitness function so it cannot be re-crossed, and migrate incrementally (e.g. "
            "Strangler Fig).",
        ),
    ),
)
