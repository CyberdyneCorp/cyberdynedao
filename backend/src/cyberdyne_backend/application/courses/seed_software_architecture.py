"""Curated Software Architecture track: Basics, Intermediate, Advanced.

Teaches software architecture from first principles -- what architecture is and
why it matters, UML (class, use-case, sequence diagrams), design principles
(SOLID, DRY/KISS/YAGNI, coupling vs cohesion), and the foundational patterns
MVC, MVVM/MVP, layered, GoF, DDD, REST -- through to Hexagonal (Ports &
Adapters), Clean/Onion architecture, monolith vs microservices, event-driven
architecture/CQRS, documenting architecture (C4, ADRs, 4+1), and architectural
evolution and anti-patterns.

This is a visual, diagram-driven subject: the interactivity comes from heavy use
of Mermaid diagrams -- UML class diagrams (``classDiagram``), interaction
diagrams (``sequenceDiagram``), state machines (``stateDiagram-v2``), layered
and dependency diagrams (``flowchart``), domain models (``erDiagram``), and C4
context/component views. Every UML/architecture concept is shown as a diagram,
not just described. Short code sketches accompany the patterns.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY (seed_quizzes/software_architecture_*.py) at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


# -- Software Architecture - Basics --------------------------------------------

_SA_BASICS = SeedCourse(
    slug="software-architecture-basics",
    title="Software Architecture — Basics",
    description=(
        "Start from the ground up: what software architecture is and why it "
        "matters, the UML diagrams every developer should read (class, use-case, "
        "sequence), the design principles that keep systems healthy (SOLID, "
        "DRY/KISS/YAGNI, coupling vs cohesion), layered architecture, and the "
        "classic MVC pattern - with a Mermaid diagram for every concept."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is software architecture",
            "10 min",
            r"""# What is software architecture

**Software architecture** is the set of *significant decisions* about how a
system is organised: its major components, how they relate, and the principles
that govern their design and evolution. It is the stuff that is **hard to change
later** - so it deserves deliberate thought up front.

## Architecture vs. design

The line is fuzzy, but a useful rule of thumb:

- **Architecture** - the high-level, structural, hard-to-reverse decisions:
  "we will use a layered backend with a relational database and a message
  queue", "the UI talks to the server over REST".
- **Design** - the lower-level, localised decisions inside a component: which
  class implements an interface, how a method is written, which loop to use.

Architecture is about **structure and trade-offs**; design is about
**implementation detail**.

```mermaid
flowchart TD
  ARCH["Architecture<br/>(structure, trade-offs, hard to change)"]
  ARCH --> C1["Component boundaries"]
  ARCH --> C2["Technology choices"]
  ARCH --> C3["Cross-cutting concerns<br/>(security, logging)"]
  C1 --> DES["Design<br/>(implementation detail, easier to change)"]
  DES --> D1["Class & method design"]
  DES --> D2["Data structures & algorithms"]
```

## Why it matters

A good architecture makes the system's **quality attributes** achievable:

- **Maintainability** - changes stay local; you can reason about one part.
- **Scalability** - the system grows with load.
- **Testability** - components can be exercised in isolation.
- **Reliability & security** - failures and threats are contained.

A poor architecture makes every change risky and slow - the cost of change rises
over time instead of staying flat.

## The architect's concerns

```mermaid
mindmap
  root((Architect's concerns))
    Stakeholders
      Users
      Developers
      Business
    Quality attributes
      Performance
      Security
      Maintainability
    Constraints
      Budget
      Deadlines
      Existing systems
    Trade-offs
      Cost vs speed
      Simplicity vs flexibility
```

An architect balances **stakeholder needs**, **quality attributes**, and
**constraints**, and makes **trade-offs** explicit. There is no perfect
architecture - only one that best fits *this* system's forces.

> **Practical insight:** architecture is not a phase you finish; it is a set of
> decisions you record and revisit. Capture the *why* behind big choices (we will
> see Architecture Decision Records in the Advanced course) so future you - and
> your teammates - understand the trade-offs.

**Next:** the universal language for describing structure - UML class diagrams.
""",
        ),
        _t(
            "UML essentials — class diagrams",
            "12 min",
            r"""# UML essentials — class diagrams

**UML** (Unified Modeling Language) is a standard visual notation for describing
software. The **class diagram** is the most-used UML diagram: it shows the
*static structure* - the classes, their attributes and operations, and the
relationships between them.

## Anatomy of a class

A class box has three compartments: name, attributes, operations. UML uses
visibility markers: `+` public, `-` private, `#` protected.

```mermaid
classDiagram
  class Account {
    -id: int
    -balance: Decimal
    +deposit(amount) void
    +withdraw(amount) bool
    +getBalance() Decimal
  }
```

## The relationships (and their semantics)

This is the part people get wrong - the *kind* of line and arrowhead carries
precise meaning:

- **Inheritance (generalisation)** - "is-a". Hollow triangle arrow.
- **Association** - "uses/knows". A plain line; objects reference each other.
- **Aggregation** - "has-a", **shared** lifecycle. Hollow diamond. The part can
  outlive the whole (a `Team` *has* `Player`s, but players exist without the team).
- **Composition** - "has-a", **owned** lifecycle. Filled diamond. The part dies
  with the whole (an `Order` *owns* its `OrderLine`s).

```mermaid
classDiagram
  Animal <|-- Dog : inheritance (is-a)
  Team o-- Player : aggregation (shared)
  Order *-- OrderLine : composition (owned)
  Order --> Customer : association (knows)

  class Animal {
    +makeSound() void
  }
  class Dog {
    +makeSound() void
  }
  class Team
  class Player
  class Order
  class OrderLine
  class Customer
```

Read it as: a `Dog` *is an* `Animal`; a `Team` *aggregates* `Player`s (shared
lifecycle); an `Order` is *composed of* `OrderLine`s (it owns them); an `Order`
*is associated with* a `Customer`.

## Multiplicity

Numbers on the ends say *how many*: `1`, `0..1`, `1..*`, `*`.

```mermaid
classDiagram
  Customer "1" --> "0..*" Order : places
  Order "1" *-- "1..*" OrderLine : contains
```

"One customer places zero-or-more orders; one order contains one-or-more lines."

## Interfaces and abstract classes

An **interface** is a contract with no implementation; realisation uses a dashed
hollow-triangle arrow.

```mermaid
classDiagram
  class PaymentMethod {
    <<interface>>
    +pay(amount) Receipt
  }
  PaymentMethod <|.. CreditCard : realises
  PaymentMethod <|.. PayPal : realises
```

In code, that interface + two implementations:

```python
from typing import Protocol


class PaymentMethod(Protocol):
    def pay(self, amount: float) -> "Receipt": ...


class CreditCard:
    def pay(self, amount: float) -> "Receipt": ...


class PayPal:
    def pay(self, amount: float) -> "Receipt": ...
```

> **Practical insight:** you do not need to draw every class. Use class diagrams
> to communicate the *interesting* structure - the relationships that are easy to
> get wrong. Getting aggregation vs composition right tells readers about
> ownership and lifecycle, which drives real code (e.g. cascade deletes).

**Next:** modelling behaviour - use-case and sequence diagrams.
""",
        ),
        _t(
            "UML behavior — use-case & sequence diagrams",
            "11 min",
            r"""# UML behavior — use-case & sequence diagrams

Class diagrams show *structure*; **behavioural** diagrams show *what the system
does over time*. Two are essential early on: the **use-case diagram** (what
actors can do) and the **sequence diagram** (how objects collaborate to do it).

## Use-case diagrams

A use-case diagram captures the system's **functional scope**: the **actors**
(users or external systems) and the **use cases** (goals they pursue). It is a
conversation tool with stakeholders, not a design.

```mermaid
flowchart LR
  customer(("Customer")):::actor
  admin(("Admin")):::actor
  subgraph Shop["Online Shop"]
    uc1(["Browse catalog"])
    uc2(["Place order"])
    uc3(["Track shipment"])
    uc4(["Manage products"])
  end
  customer --> uc1
  customer --> uc2
  customer --> uc3
  admin --> uc4
  classDef actor fill:#eef,stroke:#669
```

Relationships between use cases include **«include»** (a use case always uses
another) and **«extend»** (optional, conditional behaviour).

## Sequence diagrams

A **sequence diagram** shows objects exchanging **messages** over time.
Lifelines run top-to-bottom; arrows are calls; dashed arrows are returns. This
is where you reason about *who calls whom* to fulfil a use case.

```mermaid
sequenceDiagram
  actor C as Customer
  participant UI as Web UI
  participant API as OrderService
  participant PAY as PaymentGateway
  participant DB as Database
  C->>UI: click "Place order"
  UI->>API: POST /orders
  API->>DB: save order (PENDING)
  API->>PAY: charge(card, total)
  PAY-->>API: approved
  API->>DB: update order (PAID)
  API-->>UI: 201 Created
  UI-->>C: confirmation page
```

### Alternatives and loops

Combined fragments express control flow: `alt` (alternatives), `opt`
(optional), `loop` (repetition).

```mermaid
sequenceDiagram
  participant API as OrderService
  participant PAY as PaymentGateway
  API->>PAY: charge(card, total)
  alt payment approved
    PAY-->>API: approved
    API->>API: mark order PAID
  else payment declined
    PAY-->>API: declined
    API->>API: mark order FAILED
  end
```

## State diagrams: an object's lifecycle

When a single object moves through **states**, a **state machine** captures the
rules - which transitions are allowed.

```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Paid : payment approved
  Pending --> Failed : payment declined
  Paid --> Shipped : dispatch
  Shipped --> Delivered : arrives
  Delivered --> [*]
  Failed --> [*]
```

> **Practical insight:** pick the diagram to the question you are answering -
> use-case for *scope*, sequence for *collaboration*, state for *lifecycle*. A
> few focused diagrams beat one giant one. Sequence diagrams are especially good
> for spotting a missing error path before you write the code.

**Next:** the principles that keep designs healthy - SOLID and friends.
""",
        ),
        _t(
            "Design principles & best practices",
            "12 min",
            r"""# Design principles & best practices

Patterns and diagrams help, but a handful of **principles** do the heavy lifting
of keeping code maintainable. Master these and most "good design" follows.

## SOLID

Five object-oriented principles (Robert C. Martin):

- **S** - Single Responsibility: a class should have one reason to change.
- **O** - Open/Closed: open for extension, closed for modification.
- **L** - Liskov Substitution: subtypes must be usable wherever the base type is.
- **I** - Interface Segregation: many small interfaces beat one fat one.
- **D** - Dependency Inversion: depend on abstractions, not concretions.

```mermaid
flowchart TD
  S["S - Single Responsibility"]
  O["O - Open/Closed"]
  L["L - Liskov Substitution"]
  I["I - Interface Segregation"]
  D["D - Dependency Inversion"]
  S --> GOAL["Maintainable,<br/>extensible OO design"]
  O --> GOAL
  L --> GOAL
  I --> GOAL
  D --> GOAL
```

**Dependency Inversion** in a class diagram - the high-level policy depends on an
abstraction, and the detail implements it:

```mermaid
classDiagram
  class ReportService {
    +generate() void
  }
  class Storage {
    <<interface>>
    +save(data) void
  }
  class S3Storage {
    +save(data) void
  }
  ReportService --> Storage : depends on abstraction
  Storage <|.. S3Storage : implements
```

```python
class Storage(Protocol):
    def save(self, data: bytes) -> None: ...


class ReportService:
    def __init__(self, storage: Storage):   # inject the abstraction
        self._storage = storage

    def generate(self) -> None:
        self._storage.save(b"...")
```

`ReportService` never names `S3Storage` - so you can swap in a local or in-memory
store (great for tests) without touching it.

## DRY, KISS, YAGNI

- **DRY** - Don't Repeat Yourself: one authoritative place for each piece of
  knowledge.
- **KISS** - Keep It Simple: prefer the simplest thing that works.
- **YAGNI** - You Aren't Gonna Need It: don't build for imagined futures.

These pull against each other - over-applying DRY can add coupling; YAGNI keeps
you from over-engineering. Balance is the skill.

## Separation of concerns

Each part of the system should address **one concern** (UI, business rules,
persistence). This is the seed of layered, MVC, and hexagonal architectures.

## Coupling and cohesion

- **Coupling** - how much modules depend on each other. Aim for **loose**.
- **Cohesion** - how related the things inside a module are. Aim for **high**.

```mermaid
flowchart LR
  subgraph Bad["High coupling, low cohesion"]
    A1["Module A"] <--> B1["Module B"]
    A1 <--> C1["Module C"]
    B1 <--> C1
  end
  subgraph Good["Loose coupling, high cohesion"]
    A2["Module A"] --> IFACE["interface"]
    B2["Module B"] --> IFACE
  end
```

The goal: **loose coupling, high cohesion**. Modules that change together live
together; modules that change for different reasons stay apart.

> **Practical insight:** when a change forces edits in many unrelated places, you
> have a coupling/cohesion problem - not a tooling one. Apply Single
> Responsibility and Dependency Inversion to break the knot.

**Next:** the first structural pattern - layered (n-tier) architecture.
""",
        ),
        _t(
            "Layered (n-tier) architecture",
            "10 min",
            r"""# Layered (n-tier) architecture

**Layered architecture** (a.k.a. *n-tier*) organises a system into horizontal
layers, each with a clear responsibility, where each layer depends only on the
one **below** it. It is the most common starting architecture - and the default
for many web apps.

## The classic layers

```mermaid
flowchart TD
  P["Presentation Layer<br/>(UI / controllers / API)"]
  A["Application Layer<br/>(use cases / orchestration)"]
  D["Domain / Business Layer<br/>(rules, entities)"]
  I["Infrastructure / Data Layer<br/>(database, external services)"]
  P --> A
  A --> D
  D --> I
```

- **Presentation** - talks to the outside world (HTTP, CLI, UI).
- **Application** - orchestrates use cases; thin coordination logic.
- **Domain** - the business rules and entities; the heart of the system.
- **Infrastructure** - databases, message queues, third-party APIs.

The **dependency direction** is downward: presentation may call application,
application calls domain, domain uses infrastructure. Higher layers never reach
*up*.

## A request flowing through the layers

```mermaid
sequenceDiagram
  participant UI as Controller (Presentation)
  participant APP as OrderUseCase (Application)
  participant DOM as Order (Domain)
  participant REPO as OrderRepository (Infra)
  UI->>APP: placeOrder(cmd)
  APP->>DOM: Order.create(...)
  DOM-->>APP: order (valid)
  APP->>REPO: save(order)
  REPO-->>APP: ok
  APP-->>UI: OrderId
```

## Open vs. closed layers

A **closed** layer must be passed through (the default - it gives isolation). An
**open** layer may be bypassed (e.g. a shared "services" layer). Closing layers
maximises isolation; opening them trades isolation for fewer hops.

## Strengths and weaknesses

```mermaid
mindmap
  root((Layered))
    Pros
      Simple & familiar
      Clear separation
      Easy to staff by layer
    Cons
      Can become a "layered monolith"
      Changes ripple top to bottom
      Risk of an anemic domain
      Performance: many hops
```

A common smell is the **"sinkhole anti-pattern"**: requests pass straight through
layers that add no value (a controller that just forwards to a repository). If a
layer only delegates, question whether it earns its place.

> **Practical insight:** layered architecture is a fine default, but watch the
> dependency on the database. If your domain layer imports your ORM, business
> rules get coupled to infrastructure. The Advanced course's hexagonal/clean
> styles invert that dependency to keep the domain pure.

**Next:** the pattern that organised the first interactive UIs - MVC.
""",
        ),
        _t(
            "The MVC pattern",
            "11 min",
            r"""# The MVC pattern

**Model-View-Controller (MVC)** is a classic pattern for separating an
application into three responsibilities, so presentation logic and business
logic do not tangle together. It originated in Smalltalk and underpins most web
frameworks today.

## The three parts

- **Model** - the data and business rules. Knows nothing about the UI.
- **View** - the presentation. Renders the model; knows nothing about business
  rules.
- **Controller** - the glue. Handles input, updates the model, selects the view.

```mermaid
classDiagram
  class Controller {
    +handleRequest(input) void
  }
  class Model {
    -state
    +update(data) void
    +getState() State
  }
  class View {
    +render(model) Html
  }
  Controller --> Model : updates
  Controller --> View : selects
  View --> Model : reads
```

## The flow of a request

```mermaid
sequenceDiagram
  actor U as User
  participant C as Controller
  participant M as Model
  participant V as View
  U->>C: action (e.g. submit form)
  C->>M: update(data)
  M-->>C: new state
  C->>V: render(model)
  V->>M: read state
  V-->>U: HTML response
```

The controller never holds business rules (those live in the model) and never
generates HTML (that is the view's job). Each part can change independently.

## MVC on the web

Web MVC differs slightly from the original (the server is stateless between
requests, and the "view" is usually a template):

```mermaid
flowchart LR
  REQ["HTTP request"] --> ROUTER["Router"]
  ROUTER --> CTRL["Controller"]
  CTRL --> MDL["Model (domain + data)"]
  MDL --> CTRL
  CTRL --> VW["View (template)"]
  VW --> RESP["HTTP response (HTML/JSON)"]
```

A minimal sketch:

```python
class OrderController:
    def __init__(self, orders: "OrderModel"):
        self._orders = orders

    def show(self, order_id: int) -> str:
        order = self._orders.find(order_id)     # talk to the model
        return render_template("order.html", order=order)   # pick the view
```

## Why MVC

- **Separation of concerns** - test the model without a browser; restyle the view
  without touching rules.
- **Parallel work** - designers on views, developers on models.
- **Reuse** - one model, many views (web, API, mobile).

> **Practical insight:** keep controllers **thin** and models **rich**. A common
> failure is the "fat controller" that grows business logic - push that logic
> down into the model (or a service the model uses). The next course shows MVVM
> and MVP, which refine the same separation for richer client UIs.

**Next:** the Intermediate course - MVVM, GoF patterns, dependencies, DDD, APIs,
and quality attributes.
""",
        ),
    ),
)


# -- Software Architecture - Intermediate --------------------------------------

_SA_INTERMEDIATE = SeedCourse(
    slug="software-architecture-intermediate",
    title="Software Architecture — Intermediate",
    description=(
        "Level up: MVVM and MVP and how they differ from MVC, the Gang-of-Four "
        "design patterns (creational/structural/behavioural with concrete "
        "examples), component and dependency diagrams with the Dependency "
        "Inversion Principle, Domain-Driven Design building blocks, API and "
        "integration design (REST, client-server, layered APIs), and how to weigh "
        "quality attributes and trade-offs - all illustrated with UML."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "MVVM and MVP",
            "11 min",
            r"""# MVVM and MVP

MVC separates model, view, and controller - but rich client UIs (desktop,
mobile, single-page apps) pushed the pattern in two directions: **MVP**
(Model-View-Presenter) and **MVVM** (Model-View-ViewModel). Both aim to make the
view **thin and testable**.

## MVP — Model-View-Presenter

The **Presenter** holds all presentation logic and talks to the view through an
**interface**, so the view is a dumb shell you can replace with a test double.

```mermaid
classDiagram
  class View {
    <<interface>>
    +showOrders(items) void
    +showError(msg) void
  }
  class AndroidOrderView {
    +showOrders(items) void
    +showError(msg) void
  }
  class OrderPresenter {
    +loadOrders() void
  }
  class Model {
    +fetchOrders() List
  }
  View <|.. AndroidOrderView
  OrderPresenter --> View : updates via interface
  OrderPresenter --> Model : reads/writes
```

The view forwards events to the presenter; the presenter calls back through the
`View` interface. Because that interface is mockable, presenter logic is fully
unit-testable without a UI framework.

## MVVM — Model-View-ViewModel

MVVM introduces the **ViewModel**: a UI-shaped projection of the model that
exposes observable state and commands. The view **binds** to the ViewModel
(data binding), so there is no manual "update the widget" code.

```mermaid
classDiagram
  class View {
    binds to ViewModel
  }
  class ViewModel {
    +orders: Observable
    +isLoading: Observable
    +loadCommand()
  }
  class Model {
    +fetchOrders() List
  }
  View ..> ViewModel : data binding
  ViewModel --> Model : reads/writes
```

The key arrow is **data binding** (dashed): the view observes the ViewModel and
re-renders automatically when observables change. The ViewModel has **no
reference** to the view at all.

## How they differ from MVC (and each other)

```mermaid
flowchart LR
  subgraph MVC
    c1["View"] --> c2["Controller"] --> c3["Model"]
    c1 -.reads.-> c3
  end
  subgraph MVP
    p1["View (passive)"] <--> p2["Presenter"] --> p3["Model"]
  end
  subgraph MVVM
    v1["View"] -. binding .-> v2["ViewModel"] --> v3["Model"]
  end
```

- **MVC** - controller handles input; the view often reads the model directly.
- **MVP** - the view is **passive**; the presenter drives it through an interface
  (one presenter per view, two-way).
- **MVVM** - the view **binds** to the ViewModel; updates are automatic and the
  ViewModel never knows the view exists.

> **Practical insight:** choose by your platform's tooling. MVVM shines where the
> framework provides data binding (modern web/mobile frameworks, WPF). MVP fits
> platforms without binding. All three share one goal: keep presentation logic
> out of the view so it can be tested - the view should be the thinnest part.

**Next:** the reusable solutions catalog - GoF design patterns.
""",
        ),
        _t(
            "GoF design patterns overview",
            "12 min",
            r"""# GoF design patterns overview

The **Gang of Four** (GoF) catalog names 23 reusable solutions to recurring
design problems, in three families:

- **Creational** - how objects are made (Factory, Builder, Singleton...).
- **Structural** - how objects are composed (Adapter, Decorator, Facade...).
- **Behavioural** - how objects interact (Observer, Strategy, Command...).

```mermaid
mindmap
  root((GoF Patterns))
    Creational
      Factory Method
      Abstract Factory
      Builder
      Singleton
    Structural
      Adapter
      Decorator
      Facade
      Composite
    Behavioural
      Observer
      Strategy
      Command
      State
```

## Factory Method (creational)

Defer instantiation to a method so callers depend on an abstraction, not a
concrete class.

```mermaid
classDiagram
  class ExporterFactory {
    +create(kind) Exporter
  }
  class Exporter {
    <<interface>>
    +export(data) bytes
  }
  class CsvExporter
  class PdfExporter
  Exporter <|.. CsvExporter
  Exporter <|.. PdfExporter
  ExporterFactory ..> Exporter : creates
```

```python
def create_exporter(kind: str) -> Exporter:
    if kind == "csv":
        return CsvExporter()
    if kind == "pdf":
        return PdfExporter()
    raise ValueError(kind)
```

## Adapter (structural)

Wrap an incompatible class so it fits the interface your code expects -
"convert one interface into another".

```mermaid
classDiagram
  class Target {
    <<interface>>
    +request() Result
  }
  class LegacyService {
    +doOldThing() OldResult
  }
  class LegacyAdapter {
    +request() Result
  }
  Target <|.. LegacyAdapter
  LegacyAdapter --> LegacyService : delegates
```

```python
class LegacyAdapter:           # implements Target, wraps LegacyService
    def __init__(self, legacy: LegacyService):
        self._legacy = legacy

    def request(self) -> "Result":
        old = self._legacy.do_old_thing()
        return adapt(old)      # translate to the expected shape
```

## Strategy and Observer (behavioural)

**Strategy** makes an algorithm interchangeable; **Observer** notifies dependents
when state changes.

```mermaid
classDiagram
  class Checkout {
    -strategy: PricingStrategy
    +total() Money
  }
  class PricingStrategy {
    <<interface>>
    +price(cart) Money
  }
  class RegularPricing
  class BlackFridayPricing
  PricingStrategy <|.. RegularPricing
  PricingStrategy <|.. BlackFridayPricing
  Checkout --> PricingStrategy : uses (swappable)
```

Observer as a sequence - the subject pushes updates to all subscribers:

```mermaid
sequenceDiagram
  participant S as Subject (Cart)
  participant O1 as Observer (Totals)
  participant O2 as Observer (Analytics)
  S->>S: addItem()
  S->>O1: notify(changed)
  S->>O2: notify(changed)
  O1-->>S: ack
  O2-->>S: ack
```

> **Practical insight:** patterns are a **vocabulary**, not a checklist. Reach for
> one when you feel the problem it solves (e.g. "I keep adding `if kind ==`" ->
> Strategy/Factory). Forcing patterns where they are not needed adds ceremony -
> remember KISS and YAGNI.

**Next:** organising the big picture - component and dependency diagrams.
""",
        ),
        _t(
            "Component, package & dependency diagrams",
            "11 min",
            r"""# Component, package & dependency diagrams

Class diagrams zoom into objects; **component** and **package** diagrams zoom
out to the building blocks of a system and the **dependencies** between them -
which is where architecture lives or dies.

## Package diagrams

A **package** groups related types. The arrows show *who depends on whom* - and
the golden rule is **no cycles**.

```mermaid
flowchart TD
  WEB["web<br/>(controllers)"] --> APP["application<br/>(use cases)"]
  APP --> DOMAIN["domain<br/>(entities, rules)"]
  APP --> PORTS["domain.ports<br/>(interfaces)"]
  INFRA["infrastructure<br/>(db, http)"] --> PORTS
  INFRA --> DOMAIN
```

Note that `infrastructure` depends on the **ports** (interfaces) defined near the
domain - it does *not* point the other way. That is the Dependency Inversion
Principle applied at the package level.

## Components and their interfaces

A **component** is a deployable/replaceable unit that exposes **provided**
interfaces and consumes **required** ones (the "lollipop and socket").

```mermaid
flowchart LR
  subgraph OrderSvc["OrderService (component)"]
    OP(["provides: OrdersAPI"])
    OR(["requires: Payments"])
  end
  subgraph PaySvc["PaymentService (component)"]
    PP(["provides: Payments"])
  end
  OR --> PP
  CLIENT["Web Client"] --> OP
```

`OrderService` *requires* `Payments`, which `PaymentService` *provides*. Wiring
the requirement to a provider is the system's composition.

## The Dependency Inversion Principle, structurally

The trick that keeps dependencies pointing the "right" way: high-level modules
and low-level modules **both** depend on an abstraction owned by the high-level
side.

```mermaid
classDiagram
  class BillingService {
    +charge() void
  }
  class PaymentPort {
    <<interface>>
    +pay(amount) Receipt
  }
  class StripeAdapter {
    +pay(amount) Receipt
  }
  BillingService --> PaymentPort : depends on
  PaymentPort <|.. StripeAdapter : implemented by
```

Without DIP, `BillingService` would point at `StripeAdapter` (a hard dependency
on a vendor). With DIP, the arrow flips: the adapter depends on *our* interface.

## Managing dependencies

- **Acyclic** - dependencies form a DAG; cycles make modules un-shippable
  independently and hard to test.
- **Stable abstractions** - things many others depend on should be abstract and
  change rarely.
- **Direction** - point dependencies toward stability and toward your domain.

```mermaid
flowchart LR
  UNSTABLE["volatile detail<br/>(adapters, frameworks)"] --> STABLE["stable abstraction<br/>(domain, ports)"]
```

> **Practical insight:** dependency direction *is* architecture. Tools like
> import-linter (Python) or ArchUnit (Java) can fail your build if a forbidden
> arrow appears - encoding the rules so they cannot rot. If you draw one diagram
> for a codebase, draw the package dependency graph.

**Next:** modelling the business itself - Domain-Driven Design.
""",
        ),
        _t(
            "Domain-Driven Design basics",
            "12 min",
            r"""# Domain-Driven Design basics

**Domain-Driven Design (DDD)** puts the **business domain** at the centre of the
software. Its tactical building blocks give you a vocabulary for modelling rich
domains; its strategic patterns help you split a large system sensibly.

## The tactical building blocks

- **Entity** - has a stable **identity** over time (a `Customer` with an id);
  two entities differ even with identical attributes.
- **Value Object** - defined **only** by its attributes, no identity, immutable
  (a `Money`, an `Address`). Two with the same values are equal.
- **Aggregate** - a cluster of entities/value objects treated as one
  consistency boundary, accessed through a single **aggregate root**.
- **Repository** - a collection-like interface for loading and saving
  aggregates, hiding the database.

```mermaid
classDiagram
  class Order {
    <<aggregate root>>
    -id: OrderId
    +addLine(product, qty) void
    +total() Money
  }
  class OrderLine {
    -product: ProductId
    -qty: int
  }
  class Money {
    <<value object>>
    +amount: Decimal
    +currency: str
  }
  Order *-- OrderLine : owns
  OrderLine --> Money : price
  Order --> Money : total
```

The **aggregate root** (`Order`) is the only entry point: you never reach in and
edit an `OrderLine` directly - you go through the root, which enforces invariants.

## Repositories hide persistence

```mermaid
classDiagram
  class OrderRepository {
    <<interface>>
    +findById(id) Order
    +save(order) void
  }
  class SqlOrderRepository {
    +findById(id) Order
    +save(order) void
  }
  OrderRepository <|.. SqlOrderRepository
```

```python
class OrderRepository(Protocol):
    def find_by_id(self, id: "OrderId") -> "Order": ...
    def save(self, order: "Order") -> None: ...
```

The domain talks to the **interface**; the SQL implementation lives in
infrastructure - exactly the Dependency Inversion we have been building toward.

## Strategic design: bounded contexts

A big domain has different models for the same word. A **bounded context** is a
boundary inside which a model and its **ubiquitous language** are consistent. A
`Customer` in Sales is not the same `Customer` in Support.

```mermaid
flowchart LR
  subgraph Sales["Bounded Context: Sales"]
    s_cust["Customer (credit limit, orders)"]
  end
  subgraph Support["Bounded Context: Support"]
    sup_cust["Customer (tickets, SLA)"]
  end
  Sales <-->|context map:<br/>shared id, translation| Support
```

The **context map** records how contexts relate (shared kernel, customer/supplier,
anti-corruption layer). This is also how you find good **microservice boundaries**
(Advanced course).

> **Practical insight:** start tactical only where the domain is genuinely
> complex - DDD's machinery is overkill for CRUD. The strategic ideas (bounded
> contexts, ubiquitous language) pay off on almost any non-trivial system: agree
> on words, and draw the boundaries before you split the code.

**Next:** how systems talk to each other - API and integration design.
""",
        ),
        _t(
            "API & integration design",
            "11 min",
            r"""# API & integration design

Most systems are not islands - they expose and consume **APIs**. Designing them
well is an architectural concern: the API is a **contract** that is expensive to
change once clients depend on it.

## Client-server, layered

The web's foundational style is **client-server**: a clear split between the
consumer (client) and the provider (server), often with intermediaries (caches,
gateways) layered between them.

```mermaid
flowchart LR
  CLIENT["Client<br/>(browser / mobile)"] --> GW["API Gateway<br/>(auth, rate limit)"]
  GW --> SVC["Application Service"]
  SVC --> DB["Database"]
  GW --> CACHE["Cache / CDN"]
```

Each layer can be developed, scaled, and secured independently - and the client
need not know how many layers sit behind the gateway.

## REST in a nutshell

**REST** models the API as **resources** (nouns) addressed by URLs, manipulated
with standard **HTTP verbs**, returning standard **status codes**. It is
stateless: each request carries everything needed to process it.

| Verb | Resource | Meaning |
|------|----------|---------|
| `GET` | `/orders` | list orders |
| `POST` | `/orders` | create an order |
| `GET` | `/orders/42` | read order 42 |
| `PUT/PATCH` | `/orders/42` | update order 42 |
| `DELETE` | `/orders/42` | delete order 42 |

```mermaid
sequenceDiagram
  participant C as Client
  participant API as REST API
  participant DB as Database
  C->>API: POST /orders {items}
  API->>DB: INSERT order
  DB-->>API: id = 42
  API-->>C: 201 Created<br/>Location: /orders/42
  C->>API: GET /orders/42
  API->>DB: SELECT
  DB-->>API: row
  API-->>C: 200 OK {order}
```

## Layering inside an API

A well-structured API service still has internal layers - the HTTP edge is thin,
and business rules sit behind it.

```mermaid
flowchart TD
  ROUTE["Route / Controller<br/>(parse, validate, status codes)"] --> UC["Use case / Service"]
  UC --> DOMAIN["Domain rules"]
  UC --> REPO["Repository (data)"]
```

```python
@router.post("/orders", status_code=201)
def create_order(cmd: CreateOrder, svc: OrderService = Depends()):
    order_id = svc.place_order(cmd)        # controller stays thin
    return {"id": order_id}
```

## Design qualities for APIs

- **Consistency** - predictable naming, verbs, and error shapes.
- **Versioning** - evolve without breaking clients (`/v1/`, media types).
- **Idempotency** - safe retries for `PUT`/`DELETE`; idempotency keys for `POST`.
- **Backward compatibility** - add fields, don't remove or repurpose them.

> **Practical insight:** treat the API as a published contract. Document it
> (OpenAPI), version it, and never make a breaking change silently - a consumer
> you cannot see is depending on today's behaviour. The same discipline applies
> to message/event contracts in event-driven systems (Advanced course).

**Next:** weighing competing goals - quality attributes and trade-offs.
""",
        ),
        _t(
            "Architectural quality attributes & trade-offs",
            "10 min",
            r"""# Architectural quality attributes & trade-offs

Architecture is the art of **trade-offs**. You cannot maximise everything at
once, so you decide which **quality attributes** (the "-ilities") matter most for
*this* system, and accept the costs that buys.

## The main quality attributes

```mermaid
mindmap
  root((Quality attributes))
    Performance
      Latency
      Throughput
    Scalability
      Vertical
      Horizontal
    Maintainability
      Modularity
      Readability
    Testability
      Isolation
      Determinism
    Reliability
      Availability
      Fault tolerance
    Security
      Confidentiality
      Integrity
```

- **Scalability** - handle more load. *Vertical* = bigger machine; *horizontal* =
  more machines (needs statelessness).
- **Maintainability** - cheap to change; driven by modularity and low coupling.
- **Testability** - components run in isolation; favoured by dependency inversion.
- **Performance** - latency and throughput under load.

## The trade-offs are real

Improving one attribute often costs another:

```mermaid
flowchart LR
  CACHE["Add caching"] -->|improves| PERF["Performance"]
  CACHE -->|hurts| FRESH["Consistency / freshness"]
  MICRO["Split into microservices"] -->|improves| SCALE["Scalability & autonomy"]
  MICRO -->|hurts| SIMPLE["Operational simplicity"]
  ABSTRACT["More abstraction layers"] -->|improves| FLEX["Flexibility / testability"]
  ABSTRACT -->|hurts| PERF2["Raw performance & simplicity"]
```

There is no free lunch: caching trades freshness for speed; microservices trade
operational simplicity for scalability; abstraction trades raw performance for
flexibility.

## A simple way to decide: scenarios

Make quality attributes **measurable** with scenarios, then evaluate options
against them:

- *"The checkout page must respond in under 300 ms at the 95th percentile with
  1,000 concurrent users."* (performance + scalability)
- *"A new payment provider can be added without changing the order code."*
  (modifiability)

```mermaid
flowchart TD
  SCN["Quality scenario<br/>(measurable)"] --> OPT1["Option A"]
  SCN --> OPT2["Option B"]
  OPT1 --> EVAL["Evaluate cost & risk"]
  OPT2 --> EVAL
  EVAL --> DECIDE["Decide & record (ADR)"]
```

This is the heart of methods like **ATAM** (Architecture Tradeoff Analysis
Method): surface the scenarios, find where attributes conflict, and choose
consciously.

> **Practical insight:** write the top three or four quality attributes down and
> rank them - they drive every structural choice. A design that is "scalable,
> simple, flexible, and fast" with no ranking is a wish, not an architecture.
> When you pick, record *why* (an ADR) so the trade-off is not relitigated monthly.

**Next:** the Advanced course - hexagonal, clean architecture, microservices,
event-driven systems, documentation, and evolution.
""",
        ),
    ),
)


# -- Software Architecture - Advanced ------------------------------------------

_SA_ADVANCED = SeedCourse(
    slug="software-architecture-advanced",
    title="Software Architecture — Advanced",
    description=(
        "Architect for change at scale: Hexagonal (Ports & Adapters) and "
        "Clean/Onion architecture and the dependency rule, monolith vs "
        "microservices vs modular monolith and service boundaries, event-driven "
        "architecture with messaging, CQRS and event sourcing, documenting "
        "architecture with the C4 model, ADRs and the 4+1 view model, and "
        "recognising and refactoring away from architectural anti-patterns."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Hexagonal architecture (Ports & Adapters)",
            "12 min",
            r"""# Hexagonal architecture (Ports & Adapters)

**Hexagonal architecture** (Alistair Cockburn's *Ports and Adapters*) puts the
application core at the centre and pushes every external concern - UI, database,
message bus - to the edges, where they plug in through **ports** and **adapters**.
The goal: the core knows nothing about the outside world.

## Ports and adapters

- **Port** - an interface defined by the core describing *what it needs* or
  *what it offers*. Technology-agnostic.
- **Adapter** - a concrete implementation of a port that speaks a specific
  technology (HTTP, SQL, Kafka).

Two kinds:

- **Driving (primary) adapters** - they *call into* the core (a REST controller,
  a CLI, a test). They use **inbound ports** (use-case interfaces).
- **Driven (secondary) adapters** - the core *calls out to* them (a database, an
  email service). They implement **outbound ports**.

```mermaid
flowchart LR
  subgraph Driving["Driving side (primary)"]
    REST["REST Controller"]
    CLI["CLI"]
    TEST["Test harness"]
  end
  subgraph Core["Application Core (domain + use cases)"]
    INPORT(["inbound port:<br/>PlaceOrder"])
    APP["Use cases + Domain"]
    OUTPORT(["outbound port:<br/>OrderRepository, Mailer"])
  end
  subgraph Driven["Driven side (secondary)"]
    DB["SQL Adapter"]
    SMTP["SMTP Adapter"]
  end
  REST --> INPORT
  CLI --> INPORT
  TEST --> INPORT
  INPORT --> APP
  APP --> OUTPORT
  OUTPORT --> DB
  OUTPORT --> SMTP
```

## The dependency rule

All dependencies point **inward**, toward the core. The core depends on
**nothing** external - adapters depend on the core's ports, never the reverse.

```mermaid
flowchart TD
  ADAPTERS["Adapters (HTTP, SQL, SMTP)"] --> PORTS["Ports (interfaces)"]
  PORTS --> CORE["Core (domain + use cases)"]
```

In code, the outbound port lives with the core; the adapter implements it:

```python
# core/ports.py - owned by the application core
class OrderRepository(Protocol):
    def save(self, order: "Order") -> None: ...


# adapters/sql.py - infrastructure, depends inward on the port
class SqlOrderRepository:           # implements OrderRepository
    def save(self, order: "Order") -> None:
        ...                          # talk to the database here
```

## Why it pays off

```mermaid
sequenceDiagram
  participant T as Test (driving adapter)
  participant UC as PlaceOrder (core)
  participant FAKE as InMemoryRepo (driven adapter)
  T->>UC: placeOrder(cmd)
  UC->>FAKE: save(order)
  FAKE-->>UC: ok
  UC-->>T: OrderId
```

Because the core only knows ports, you can run it with a **fake** repository in
tests, a **SQL** one in production, and a **REST** or **CLI** driver on top -
swapping technology without touching a line of business logic.

> **Practical insight:** the litmus test for hexagonal done right - can you delete
> the web framework and the database and still compile and unit-test the core? If
> an `import` of your ORM or HTTP library appears inside the domain, a dependency
> is pointing the wrong way.

**Next:** the same idea, layered in rings - Clean and Onion architecture.
""",
        ),
        _t(
            "Clean & Onion architecture",
            "11 min",
            r"""# Clean & Onion architecture

**Onion** (Jeffrey Palermo) and **Clean** (Robert C. Martin) architecture are
close cousins of hexagonal. All three enforce the same **dependency rule** -
dependencies point inward toward the domain - but draw it as concentric rings.

## The rings

```mermaid
flowchart TD
  subgraph L4["Frameworks & Drivers (outermost)"]
    subgraph L3["Interface Adapters (controllers, gateways, presenters)"]
      subgraph L2["Application / Use Cases"]
        subgraph L1["Entities / Domain (innermost)"]
          CORE["Enterprise business rules"]
        end
      end
    end
  end
```

- **Entities / Domain** (centre) - enterprise-wide business rules, the most
  stable code.
- **Use cases / Application** - application-specific rules orchestrating
  entities.
- **Interface adapters** - controllers, presenters, gateways that translate
  between the use cases and the outside.
- **Frameworks & drivers** (outer) - the web, the database, the UI - details.

## The dependency rule, restated

Source-code dependencies point **only inward**. An inner ring never names an
outer ring. Crossing a boundary outward-to-inward uses an interface the inner
ring owns (Dependency Inversion again).

```mermaid
flowchart LR
  DETAILS["Frameworks / DB / Web<br/>(volatile details)"] --> ADAPT["Interface Adapters"]
  ADAPT --> UC["Use Cases"]
  UC --> ENT["Entities (stable)"]
```

The arrow of dependency runs opposite to the flow of control: a request flows
inward at runtime, but at *compile time* the outer layers depend on the inner,
never the reverse.

## Clean vs. Onion vs. Hexagonal

```mermaid
flowchart TD
  GOAL["Same goal:<br/>protect the domain,<br/>dependencies point inward"]
  GOAL --> HEX["Hexagonal:<br/>ports & adapters,<br/>symmetric edges"]
  GOAL --> ONION["Onion:<br/>concentric rings,<br/>domain at centre"]
  GOAL --> CLEAN["Clean:<br/>rings + explicit<br/>use-case layer & screaming structure"]
```

They differ mainly in **vocabulary and emphasis**, not in essence:

- **Hexagonal** - emphasises the symmetry of driving/driven adapters and ports.
- **Onion** - emphasises the domain model at the very centre, services around it.
- **Clean** - adds an explicit use-case (interactor) layer and the idea that the
  folder structure should "scream" the domain, not the framework.

```python
# A clean-architecture interactor depends only on inward abstractions
class PlaceOrder:                          # use case (application ring)
    def __init__(self, orders: OrderRepository):   # port owned inward
        self._orders = orders

    def execute(self, cmd: PlaceOrderCommand) -> OrderId:
        order = Order.create(cmd.items)     # entity (domain ring)
        self._orders.save(order)
        return order.id
```

> **Practical insight:** do not get lost in which name is "correct" - they are
> the same discipline. Pick one vocabulary for your team and apply the dependency
> rule consistently. The payoff is identical: a domain you can test in
> milliseconds and infrastructure you can swap without fear.

**Next:** how big should a service be - monolith vs microservices.
""",
        ),
        _t(
            "Monolith, microservices & modular monolith",
            "11 min",
            r"""# Monolith, microservices & modular monolith

A central architectural decision is **how to slice a system into deployable
units**. The spectrum runs from a single monolith to many fine-grained
microservices, with the **modular monolith** as a pragmatic middle ground.

## The three shapes

```mermaid
flowchart LR
  subgraph Monolith
    M["One deployable<br/>(all modules, one DB)"]
  end
  subgraph Modular["Modular Monolith"]
    A["Module A"] --- B["Module B"] --- C["Module C"]
    note1["One deployable,<br/>strong internal boundaries"]
  end
  subgraph Micro["Microservices"]
    S1["Service A<br/>+ own DB"]
    S2["Service B<br/>+ own DB"]
    S3["Service C<br/>+ own DB"]
  end
```

- **Monolith** - one codebase, one deployable, usually one database. Simple to
  build, test, and deploy; can become a tangled "big ball of mud" without
  internal discipline.
- **Modular monolith** - still one deployable, but with **enforced module
  boundaries** (separate schemas, no reaching across internals). Most of the
  clarity of microservices without the distributed-systems cost.
- **Microservices** - many independently deployable services, each owning its
  data, communicating over the network. Independent scaling and deployment, at
  the price of operational and data complexity.

## Finding service boundaries

Boundaries should follow **bounded contexts** (DDD), not technical layers. A
service that owns a coherent slice of the business is autonomous; one split by
layer ("the database service") couples everyone.

```mermaid
flowchart TD
  DDD["Bounded contexts<br/>(business capabilities)"] --> GOOD["Good service boundary:<br/>owns its data & rules"]
  LAYER["Technical layers<br/>(UI / logic / data)"] --> BAD["Bad service boundary:<br/>chatty, shared DB, coupled"]
```

## The trade-off, made concrete

```mermaid
flowchart LR
  MONO["Monolith"] -->|simpler ops,<br/>harder to scale teams| MID["Modular Monolith"]
  MID -->|extract a module<br/>when a real need appears| MICRO["Microservices"]
  MICRO -->|independent deploy/scale,<br/>distributed complexity| MONO
```

Microservices add network latency, partial failure, distributed transactions,
and deployment overhead. They pay off when teams must deploy and scale
**independently** - not as a default.

> **Practical insight:** start with a **modular monolith**. Keep the modules so
> well-separated (own schema, communicate through interfaces) that you *could*
> extract one into a service when a concrete need arises - independent scaling, a
> separate team, a different release cadence. Distribute reluctantly: the network
> is not free.

**Next:** loosely coupling services through events - event-driven architecture.
""",
        ),
        _t(
            "Event-driven architecture, CQRS & event sourcing",
            "12 min",
            r"""# Event-driven architecture, CQRS & event sourcing

**Event-driven architecture (EDA)** decouples components by having them
communicate through **events** - "something happened" messages - rather than
direct calls. Producers emit events; consumers react, without the producer
knowing who is listening.

## Events and messaging

```mermaid
flowchart LR
  ORDER["Order Service"] -->|OrderPlaced| BROKER["Message Broker<br/>(Kafka / RabbitMQ)"]
  BROKER --> INV["Inventory Service"]
  BROKER --> MAIL["Email Service"]
  BROKER --> ANALYTICS["Analytics Service"]
```

One `OrderPlaced` event fans out to inventory, email, and analytics. Adding a new
consumer requires **no change** to the order service - the hallmark of loose
coupling.

```mermaid
sequenceDiagram
  participant O as Order Service
  participant B as Broker
  participant I as Inventory
  participant E as Email
  O->>B: publish OrderPlaced(id, items)
  B-->>I: OrderPlaced
  B-->>E: OrderPlaced
  I->>I: reserve stock
  E->>E: send confirmation
```

## Commands vs. events

- **Command** - an *intent*, directed at one handler: `PlaceOrder` ("please do
  this"). May be rejected.
- **Event** - a *fact*, broadcast to many: `OrderPlaced` ("this happened"). Past
  tense, immutable.

## CQRS — Command Query Responsibility Segregation

**CQRS** splits the **write** model (commands that change state) from the
**read** model (queries optimised for display). Each can be modelled and scaled
independently.

```mermaid
flowchart LR
  CMD["Command<br/>(PlaceOrder)"] --> WM["Write Model<br/>(domain, validation)"]
  WM --> STORE[("Write store")]
  WM -->|events| PROJ["Projector"]
  PROJ --> RM[("Read store<br/>(denormalised views)")]
  QRY["Query<br/>(GET /orders)"] --> RM
```

The write side enforces invariants; events update one or more **read models**
shaped exactly for their queries (no joins at read time).

## Event sourcing

Instead of storing current state, **event sourcing** stores the **sequence of
events** and derives state by replaying them. The event log is the source of
truth.

```mermaid
stateDiagram-v2
  [*] --> Empty
  Empty --> Placed : OrderPlaced
  Placed --> Paid : OrderPaid
  Paid --> Shipped : OrderShipped
  Shipped --> [*]
  note right of Paid
    Current state = fold(events).
    Full history is retained.
  end note
```

```python
def replay(events: list[Event]) -> OrderState:
    state = OrderState.empty()
    for event in events:           # fold events into current state
        state = state.apply(event)
    return state
```

Benefits: a complete audit trail, time-travel/debugging, and natural fit with
CQRS projections. Costs: eventual consistency, schema/versioning of events, and
more moving parts.

> **Practical insight:** EDA, CQRS, and event sourcing are **separable** - adopt
> the smallest that solves your problem. Plain events for decoupling are cheap;
> CQRS is worth it when read and write needs truly diverge; event sourcing is the
> heaviest and only pays off when the audit log or temporal queries are
> first-class requirements. Mind **eventual consistency** at every step.

**Next:** making architecture legible - documenting it.
""",
        ),
        _t(
            "Documenting architecture — C4, ADRs & 4+1",
            "10 min",
            r"""# Documenting architecture — C4, ADRs & 4+1

An architecture that lives only in someone's head is a liability. Three
lightweight, complementary tools keep it **legible**: the **C4 model** (a set of
zoom levels for diagrams), **ADRs** (records of decisions), and the **4+1 view
model** (multiple viewpoints).

## The C4 model: four levels of zoom

C4 (Simon Brown) gives diagrams a consistent zoom: **C**ontext -> **C**ontainer
-> **C**omponent -> **C**ode. You draw only the levels you need.

```mermaid
flowchart TD
  L1["1. System Context<br/>(system + users + external systems)"] --> L2["2. Container<br/>(apps, services, DBs)"]
  L2 --> L3["3. Component<br/>(major parts inside a container)"]
  L3 --> L4["4. Code<br/>(classes - usually skip, use UML)"]
```

A **System Context** diagram - the highest zoom, for any stakeholder:

```mermaid
C4Context
  title System Context - Online Shop
  Person(customer, "Customer", "Buys products")
  System(shop, "Online Shop", "Lets customers browse and order")
  System_Ext(payment, "Payment Gateway", "Processes card payments")
  System_Ext(email, "Email Provider", "Sends transactional email")
  Rel(customer, shop, "Browses & orders")
  Rel(shop, payment, "Charges via", "HTTPS")
  Rel(shop, email, "Sends mail via", "SMTP")
```

Zoom one level in - the **Container** view shows the deployable pieces:

```mermaid
flowchart TD
  CUST(["Customer"]) --> SPA["Single-Page App<br/>(browser)"]
  SPA --> API["API Application<br/>(service)"]
  API --> DB[("Database")]
  API --> PAY["Payment Gateway (ext)"]
```

## ADRs: Architecture Decision Records

An **ADR** is a short markdown file capturing one significant decision: its
**context**, the **decision**, and the **consequences**. They are numbered,
immutable, and committed with the code.

```mermaid
stateDiagram-v2
  [*] --> Proposed
  Proposed --> Accepted : team agrees
  Proposed --> Rejected
  Accepted --> Deprecated : better option found
  Deprecated --> Superseded : ADR-NNN replaces it
  Superseded --> [*]
```

A typical ADR template:

```text
# ADR 0007: Use a message broker for order events
## Status: Accepted
## Context
Order events must reach inventory, email, and analytics without coupling.
## Decision
Publish domain events to Kafka; consumers subscribe independently.
## Consequences
+ New consumers need no change to the order service.
- We accept eventual consistency and broker operational cost.
```

## The 4+1 view model

One diagram cannot serve every stakeholder. Kruchten's **4+1** describes a system
from multiple **views**, tied together by **scenarios** (use cases - the "+1").

```mermaid
mindmap
  root((4+1 views))
    Logical
      classes, responsibilities
    Process
      concurrency, runtime
    Development
      modules, packages
    Physical
      deployment, nodes
    Scenarios
      use cases tie it together
```

> **Practical insight:** favour **lightweight, living** docs over a 100-page
> document nobody reads. A C4 context + container diagram and a folder of ADRs
> usually tells a newcomer 90% of what they need - and because ADRs record *why*,
> they stop teams from relitigating settled decisions.

**Next:** keeping architecture healthy over time - evolution and anti-patterns.
""",
        ),
        _t(
            "Evolution & anti-patterns",
            "11 min",
            r"""# Evolution & anti-patterns

Architecture is never "done" - it **evolves** with the system. The job is to keep
it healthy as requirements change, recognise **anti-patterns** before they
metastasise, and refactor deliberately toward a better structure.

## Common anti-patterns

```mermaid
mindmap
  root((Anti-patterns))
    Big Ball of Mud
      no clear structure
      everything coupled
    Spaghetti
      tangled control flow
    God Object
      one class does everything
    Sinkhole layers
      layers that only delegate
    Distributed monolith
      microservices that must deploy together
```

- **Big Ball of Mud** - the most common architecture: no discernible structure,
  pervasive coupling, every change risky. Usually the result of *no* deliberate
  architecture plus time pressure.
- **God Object** - one class/module that knows and does everything (violates
  Single Responsibility).
- **Distributed Monolith** - microservices so coupled they must be deployed
  together: all the cost of distribution, none of the autonomy.

## Why entropy wins by default

```mermaid
flowchart LR
  PRESSURE["Deadline pressure"] --> SHORTCUT["Take a shortcut"]
  SHORTCUT --> COUPLE["Coupling creeps in"]
  COUPLE --> HARDER["Changes get harder"]
  HARDER --> PRESSURE
```

Without active care, structure decays - each shortcut makes the next change
harder, which invites the next shortcut. Breaking the loop requires deliberate,
continuous refactoring.

## Fitness functions: automating architectural goals

A **fitness function** is an automated test that an architectural characteristic
holds - so a violation fails the build instead of rotting quietly.

```mermaid
flowchart TD
  RULE["Architectural rule<br/>(e.g. 'domain must not import infrastructure')"] --> FF["Fitness function<br/>(automated test in CI)"]
  FF --> PASS["Passes -> merge"]
  FF --> FAIL["Fails -> block the PR"]
```

```python
# A dependency fitness function (pytest + a tool like import-linter / pytestarch)
def test_domain_does_not_depend_on_infrastructure():
    violations = imports_from("app.domain", into="app.infrastructure")
    assert violations == [], f"domain leaks into infra: {violations}"
```

Fitness functions can also guard performance budgets, cyclic-dependency rules,
and layering - turning "we agreed not to do X" into something the CI enforces.

## Refactoring toward better architecture

You rarely rewrite; you **evolve** in safe steps, often via the **Strangler Fig**
pattern - grow the new structure around the old, redirect piece by piece, then
remove the old.

```mermaid
sequenceDiagram
  participant C as Client
  participant F as Facade / Router
  participant OLD as Legacy module
  participant NEW as New module
  C->>F: request
  F->>OLD: route (still legacy)
  Note over F,NEW: migrate one capability
  C->>F: request
  F->>NEW: route (now migrated)
  Note over OLD: shrink, then delete
```

## Trade-off analysis as a habit

Every evolution is a trade-off. Make them **explicit**: state the quality
attributes in tension, the options, and the chosen path - then record it as an
ADR.

```mermaid
flowchart LR
  FORCES["Competing forces<br/>(speed vs flexibility, ...)"] --> OPTIONS["Enumerate options"]
  OPTIONS --> SCORE["Score against ranked<br/>quality attributes"]
  SCORE --> CHOOSE["Choose & record (ADR)"]
  CHOOSE --> REVISIT["Revisit as context changes"]
```

> **Practical insight:** you do not fix a Big Ball of Mud with a rewrite - you
> establish boundaries inside it (a seam), add a fitness function so the boundary
> cannot be re-crossed, and strangle the worst parts incrementally. Architecture
> stays healthy through small, enforced, continuous decisions - not heroics.

**Next:** the final check - prove what you have learned across the whole track.
""",
        ),
    ),
)


SOFTWARE_ARCHITECTURE_COURSES = (_SA_BASICS, _SA_INTERMEDIATE, _SA_ADVANCED)

__all__ = ["SOFTWARE_ARCHITECTURE_COURSES"]
