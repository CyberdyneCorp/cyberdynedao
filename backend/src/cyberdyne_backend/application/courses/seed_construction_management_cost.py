"""Academy seed content - Construction Management and Cost Engineering.

An advanced, practitioner-oriented course on planning, costing and
controlling building and infrastructure projects: construction methods
and site logistics, the work breakdown structure and scheduling,
PERT/CPM and the critical path, lean construction and the Last Planner
System, quantity take-off and unit-price cost composition, BDI and
indirect costs with cash flow, 4D/5D BIM and earned-value control, and
health and safety management on site. Every lesson is a direct
explanation grounded in real practice (ABNT/NBR, AACE, PMI, NR
regulations) with a mermaid diagram and a worked schedule or cost
example, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import (
    SeedCourse,
    SeedLesson,
    opt,
    q,
    quiz_lesson,
)


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


_CONSTRUCTION_MANAGEMENT_COST = SeedCourse(
    slug="construction-management-cost",
    title="Construction Management & Cost Engineering",
    description=(
        "Planning, costing and controlling construction: construction methods "
        "and site logistics, the work breakdown structure and scheduling, "
        "PERT/CPM and the critical path, lean construction and the Last "
        "Planner System, quantity take-off and cost composition, BDI and cash "
        "flow, 4D/5D BIM and earned-value control, and site health and safety "
        "- with worked schedule and cost examples and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Construction Management and Cost Engineering

Delivering a building or a piece of infrastructure is a problem of
**planning, costing and control**. A design tells you *what* to build;
construction management decides *how*, *in what order*, *for how much*,
and *how you know you are still on track*. This course is the discipline
that connects the drawing to the finished, paid-for asset.

The approach is **advanced and concrete**: every lesson explains one idea
directly, shows it in a short worked example (a schedule calculation, a
unit-price composition, an earned-value table), and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **Construction methods and site logistics** - how the work is executed
2. **Work breakdown structure and scheduling** - decomposing and sequencing
3. **PERT/CPM and the critical path** - which activities drive the deadline
4. **Lean construction and the Last Planner System** - reliable flow
5. **Quantity take-off and cost composition** - pricing the work
6. **BDI, indirect costs and cash flow** - from direct cost to a bid price
7. **4D/5D BIM and earned-value control** - digital planning and control
8. **Health and safety management on site** - building without harm

Grounded in real practice and standards (ABNT/NBR, AACE International,
the PMI schedule and cost bodies of knowledge, and Brazilian NR safety
regulations), but kept teachable. This is the map from design to
delivered project.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core problem construction management addresses?",
                    (
                        opt("Producing the architectural design"),
                        opt(
                            "Planning, costing and controlling how a designed asset gets "
                            "built - order, price and staying on track",
                            correct=True,
                        ),
                        opt("Selling the finished building"),
                        opt("Only calculating structural loads"),
                    ),
                    "The design says what to build; management decides how, in what "
                    "order, for how much, and how you know you are on track.",
                ),
                q(
                    "How is each lesson in this course structured?",
                    (
                        opt("A long theoretical essay with no examples"),
                        opt(
                            "A direct explanation plus a worked schedule or cost example "
                            "and a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A video with no text"),
                    ),
                    "Explain one idea, show it worked out, draw it, then check understanding.",
                ),
            ),
        ),
        # -- 1. Construction methods and site logistics ----------------
        _t(
            "Construction methods and site logistics",
            "10 min",
            """# Construction methods and site logistics

Before any schedule or budget, you decide **how the work will be
executed** - the **construction method** - and how the site will be
**organized to feed that method**. These two choices shape everything
downstream: durations, crew sizes, equipment, and cost.

The **construction method** is the chosen technology and sequence for a
scope: cast-in-place reinforced concrete versus **precast**; conventional
masonry versus structural masonry; formwork systems; earthmoving by
excavator-and-truck versus scraper. Each method trades **cost, speed,
quality and risk** differently. Precast, for example, moves work off the
critical path into a controlled plant and speeds erection, at the cost of
craneage and transport logistics.

**Site logistics** (the *canteiro de obras* layout, per **NBR 12284**)
organizes the temporary works so materials, plant and people flow with
minimum re-handling:

- **Access and circulation** - gates, haul roads, crane radius, turning.
- **Storage and staging** - near the point of use, in delivery sequence.
- **Production facilities** - rebar yard, batching, carpentry shop.
- **Welfare and offices** - changing rooms, canteen, site office.
- **Material flow** - every extra move is waste (a lean idea, lesson 4).

A good layout minimizes **transport and handling distance** - the biggest
avoidable cost on a congested site.

```mermaid
graph TD
    SCOPE["Scope and design"] --> METHOD["Choose construction method"]
    METHOD --> RESRC["Crews plant and materials"]
    METHOD --> LAYOUT["Site logistics layout"]
    LAYOUT --> FLOW["Material and people flow"]
    RESRC --> FLOW
    FLOW --> SCHED["Feeds schedule and budget"]
```

A quick method comparison for a multi-storey structural frame:

```text
Method comparison - 8-storey frame, 1200 m2 slab

                     Cast-in-place    Precast
Cycle per floor      12 working days   6 working days
Peak site crew       28 workers        14 workers
Crane requirement    1 tower crane     1 tower + mobile
Weather sensitivity  high              low (plant cast)
Structure duration   96 days           48 days
Best when            complex geometry  repetitive layout
```

Remember: the method and the site layout are the first design decisions of
construction itself - get them right and the schedule and budget become
achievable rather than optimistic.
""",
        ),
        quiz_lesson(
            "Quiz: Construction methods and site logistics",
            (
                q(
                    "What does the choice of construction method primarily determine?",
                    (
                        opt("The colour of the facade"),
                        opt(
                            "The technology and sequence of execution, which drive "
                            "durations, crews, equipment and cost",
                            correct=True,
                        ),
                        opt("Only the architectural style"),
                        opt("The client's financing rate"),
                    ),
                    "Method is the chosen technology and sequence; it shapes every "
                    "downstream schedule and cost figure.",
                ),
                q(
                    "What is the main goal of a good site logistics layout?",
                    (
                        opt("To make the site look tidy for photos"),
                        opt(
                            "To let materials, plant and people flow with minimum "
                            "re-handling and transport distance",
                            correct=True,
                        ),
                        opt("To store all materials as far from work as possible"),
                        opt("To remove the need for a schedule"),
                    ),
                    "Every extra move is waste; the layout minimizes handling and "
                    "transport, the biggest avoidable congested-site cost.",
                ),
                q(
                    "In the worked comparison, why can precast shorten the structure duration?",
                    (
                        opt("It uses no concrete at all"),
                        opt(
                            "Elements are cast off-site in a controlled plant and only "
                            "erected on site, cutting the per-floor cycle",
                            correct=True,
                        ),
                        opt("It skips the design phase"),
                        opt("It needs no crane"),
                    ),
                    "Precast moves work off the critical path into a plant, so on-site "
                    "erection is faster and less weather-sensitive.",
                ),
            ),
        ),
        # -- 2. WBS and scheduling -------------------------------------
        _t(
            "Work breakdown structure and scheduling",
            "11 min",
            """# Work breakdown structure and scheduling

You cannot plan a whole building at once. The **Work Breakdown Structure
(WBS)** decomposes the total scope into a hierarchy of ever-smaller,
manageable **work packages**, until each leaf is something you can
estimate, schedule and assign to someone. The WBS is the backbone that
the schedule, the budget and the control system all hang from.

Two rules keep a WBS sound:

- **100 percent rule** - the children of any node sum to exactly the whole
  of that node, no more and no less. Nothing scoped is missing; nothing is
  double counted.
- **Deliverable or work-package oriented** - leaves are nouns of work
  (a slab poured, a wall built), not vague phases.

From the WBS leaves you build the **schedule**. Each leaf becomes an
**activity** with a **duration**, estimated from quantity and productivity:

```text
Duration of an activity

duration (days) = quantity / (crew productivity per day)

Example - masonry walls, one crew:
  quantity          = 640 m2 of block wall
  crew productivity = 32 m2 per day
  duration          = 640 / 32 = 20 working days
```

Activities are then **sequenced** with logical dependencies - most often
**Finish-to-Start (FS)**: the successor cannot start until the predecessor
finishes (you cannot plaster a wall before it is built). Other links exist
(Start-to-Start, Finish-to-Finish, with lead or lag), but FS dominates.
Laying activities on a calendar with these links produces the **network**
we analyse in the next lesson, and its familiar view - the **Gantt chart**
(bar chart against time).

```mermaid
graph TD
    PROJ["Project total scope"] --> A["Substructure"]
    PROJ --> B["Superstructure"]
    PROJ --> C["Finishes"]
    B --> B1["Columns work package"]
    B --> B2["Slabs work package"]
    B2 --> ACT["Activity pour slab with duration"]
    ACT --> SEQ["Sequence by dependencies"]
```

Remember: decompose scope with the 100 percent rule into work packages,
turn each into an activity with a duration from quantity over
productivity, then sequence them - that is the skeleton of every project
plan.
""",
        ),
        quiz_lesson(
            "Quiz: Work breakdown structure and scheduling",
            (
                q(
                    "What is the '100 percent rule' of a WBS?",
                    (
                        opt("Every activity must take 100 days"),
                        opt(
                            "The children of any node sum to exactly the whole of that "
                            "node - nothing missing, nothing double counted",
                            correct=True,
                        ),
                        opt("The project must be 100 percent designed first"),
                        opt("Every crew must be 100 percent utilized"),
                    ),
                    "Decomposition is complete and non-overlapping; scope adds up "
                    "exactly at every level.",
                ),
                q(
                    "A crew lays 32 m2 of block wall per day and there are 640 m2. What "
                    "is the activity duration?",
                    (
                        opt("32 working days"),
                        opt("20 working days", correct=True),
                        opt("640 working days"),
                        opt("6.4 working days"),
                    ),
                    "duration = quantity / productivity = 640 / 32 = 20 working days.",
                ),
                q(
                    "What does a Finish-to-Start (FS) dependency mean?",
                    (
                        opt("Both activities must finish together"),
                        opt("Both activities must start together"),
                        opt(
                            "The successor cannot start until the predecessor finishes",
                            correct=True,
                        ),
                        opt("The activities can never overlap in cost"),
                    ),
                    "FS is the dominant construction link - you cannot plaster a wall "
                    "before it is built.",
                ),
            ),
        ),
        # -- 3. PERT/CPM and the critical path -------------------------
        _t(
            "PERT/CPM and the critical path",
            "12 min",
            """# PERT/CPM and the critical path

Once activities are sequenced into a **network**, the **Critical Path
Method (CPM)** finds the **longest path** of dependent activities through
it. That length is the shortest possible project duration, and the
activities on it are **critical** - delay any of them and the whole
project slips.

CPM works by two passes over the network:

- **Forward pass** - compute Early Start (ES) and Early Finish
  (EF = ES + duration) from start to end, taking the latest predecessor.
- **Backward pass** - compute Late Finish (LF) and Late Start
  (LS = LF - duration) from end back to start, taking the earliest successor.
- **Total float** = LS - ES (or LF - EF). Activities with **zero float**
  are on the critical path.

Worked example - a small five-activity network (durations in days):

```text
Activity  Dur  Predecessor
A          4   -
B          6   A
C          3   A
D          5   B, C
E          2   D

Paths and lengths:
  A-B-D-E = 4 + 6 + 5 + 2 = 17 days   <- longest = CRITICAL
  A-C-D-E = 4 + 3 + 5 + 2 = 14 days

Float on C = 17 - 14 shared portion:
  C early finish = 7, but D needs its input by day 10
  total float on C = 3 days (it can slip 3 days safely)

Project duration = 17 days. Critical path = A, B, D, E (float = 0).
```

**PERT** (Program Evaluation and Review Technique) adds **uncertainty**:
each duration gets optimistic (o), most likely (m) and pessimistic (p)
estimates, and the expected duration is a weighted mean:

```text
PERT expected duration:   te = (o + 4m + p) / 6

Example (activity B):  o = 4, m = 6, p = 14
  te = (4 + 4*6 + 14) / 6 = (4 + 24 + 14) / 6 = 42 / 6 = 7 days
```

```mermaid
graph LR
    A["A dur 4"] --> B["B dur 6"]
    A --> C["C dur 3"]
    B --> D["D dur 5"]
    C --> D
    D --> E["E dur 2"]
    E --> END["Finish 17 days"]
```

Remember: the critical path is the chain with zero float that sets the
deadline; watch it relentlessly, and use float on non-critical work to
absorb problems. PERT tells you how confident that deadline is.
""",
        ),
        quiz_lesson(
            "Quiz: PERT/CPM and the critical path",
            (
                q(
                    "What is the critical path?",
                    (
                        opt("The most expensive chain of activities"),
                        opt(
                            "The longest path of dependent activities, whose length is "
                            "the shortest possible project duration",
                            correct=True,
                        ),
                        opt("The path with the most float"),
                        opt("The first activity in the network"),
                    ),
                    "Longest path = minimum project duration; its activities have zero "
                    "float, so any delay slips the whole project.",
                ),
                q(
                    "An activity has total float of 3 days. What does that mean?",
                    (
                        opt("It is on the critical path"),
                        opt("It must be done 3 days early"),
                        opt(
                            "It can slip up to 3 days without delaying the project",
                            correct=True,
                        ),
                        opt("It costs 3 days of extra money"),
                    ),
                    "Total float = LS - ES; non-critical activities have positive float "
                    "you can spend to absorb problems.",
                ),
                q(
                    "Using PERT with o=4, m=6, p=14, what is the expected duration te?",
                    (
                        opt("6 days"),
                        opt("7 days", correct=True),
                        opt("8 days"),
                        opt("14 days"),
                    ),
                    "te = (o + 4m + p) / 6 = (4 + 24 + 14) / 6 = 42 / 6 = 7 days.",
                ),
            ),
        ),
        # -- 4. Lean construction and Last Planner ---------------------
        _t(
            "Lean construction and the Last Planner System",
            "11 min",
            """# Lean construction and the Last Planner System

A CPM schedule tells you the plan; **lean construction** is about making
the work actually **flow** as planned. Adapted from the Toyota Production
System, its central idea is to **maximize value and eliminate waste**
(*muda*). On site, the classic wastes are **waiting, transport, rework,
over-processing, excess inventory, unnecessary motion and defects** - and
the biggest hidden one is **making-do**, starting a task without all its
prerequisites.

Lean reframes a project as a **flow of work** through **crews**, not just
a set of activities. Three ideas dominate:

- **Reduce variability** - unreliable hand-offs between trades destroy
  productivity; steady, predictable flow beats local speed.
- **Pull, not push** - a downstream trade signals readiness to pull work,
  rather than an upstream trade pushing unfinished work forward.
- **Continuous improvement (kaizen)** - measure, learn, adjust weekly.

The operational engine is the **Last Planner System (LPS)** by Ballard and
Howell - a set of nested planning conversations that turn *SHOULD* into
*CAN*, *WILL* and *DID*:

- **Master schedule** - the milestone-level plan (what SHOULD happen).
- **Phase / pull planning** - the team plans a phase backward from its
  milestone.
- **Lookahead (6 weeks)** - make tasks **ready** by removing constraints
  (design, materials, labour, space) - screening what CAN be done.
- **Weekly work plan** - only constraint-free tasks are committed (WILL).
- **Measure PPC** - the health metric of the whole system.

```text
Percent Plan Complete (PPC)

PPC = (tasks completed as planned) / (tasks planned) * 100

Example - one week:
  tasks planned    = 20
  tasks completed  = 16 (4 slipped: 2 no material, 2 prior trade late)
  PPC = 16 / 20 * 100 = 80 percent

Track the reasons for non-completion (RNC) and attack the top causes.
```

```mermaid
graph TD
    SHOULD["Master schedule SHOULD"] --> PHASE["Phase pull planning"]
    PHASE --> LOOK["Lookahead make ready CAN"]
    LOOK --> WEEK["Weekly plan committed WILL"]
    WEEK --> DONE["Done and measure PPC DID"]
    DONE --> LEARN["Reasons for non completion"]
    LEARN --> LOOK
```

Remember: CPM sets the target; lean and the Last Planner make the flow
reliable by only committing to work that is truly ready, and by learning
from every task that fails to complete.
""",
        ),
        quiz_lesson(
            "Quiz: Lean construction and the Last Planner System",
            (
                q(
                    "What is the central aim of lean construction?",
                    (
                        opt("Building as fast as possible regardless of waste"),
                        opt(
                            "Maximizing value while eliminating waste and making work "
                            "flow reliably",
                            correct=True,
                        ),
                        opt("Using the cheapest materials only"),
                        opt("Removing the schedule entirely"),
                    ),
                    "Lean, from the Toyota system, maximizes value and cuts waste; "
                    "steady flow beats local speed.",
                ),
                q(
                    "In the Last Planner System, what does the lookahead plan do?",
                    (
                        opt("Commits every task immediately"),
                        opt(
                            "Makes tasks ready by removing constraints, screening what "
                            "CAN be done before it is committed",
                            correct=True,
                        ),
                        opt("Replaces the master schedule"),
                        opt("Measures cost variance"),
                    ),
                    "Lookahead turns SHOULD into CAN by clearing design, material, "
                    "labour and space constraints.",
                ),
                q(
                    "20 tasks were planned this week and 16 finished as planned. What is PPC?",
                    (
                        opt("16 percent"),
                        opt("80 percent", correct=True),
                        opt("20 percent"),
                        opt("125 percent"),
                    ),
                    "PPC = completed / planned * 100 = 16 / 20 * 100 = 80 percent; then "
                    "study the reasons the other 4 slipped.",
                ),
            ),
        ),
        # -- 5. Quantity take-off and cost composition -----------------
        _t(
            "Quantity take-off and cost composition",
            "12 min",
            """# Quantity take-off and cost composition

The budget starts from **quantities**. **Quantity take-off** (or
*levantamento de quantitativos*) is the systematic measurement of every
item of work from the drawings and specifications - cubic metres of
concrete, square metres of formwork, kilograms of rebar, and so on -
following measurement conventions so nothing is missed or double counted.

Each quantity is then priced through a **unit-price composition**
(*composicao de custo unitario*, the basis of reference systems like
**SINAPI** and **TCPO**). A composition builds the cost of **one unit** of
a service from its **inputs**: labour, materials and equipment, each as a
**coefficient** (consumption per unit) times a **unit price**.

```text
Unit-price composition - 1 m3 of structural concrete (cast in place)

Input              Coefficient   Unit price     Cost per m3
Concrete C25        1.03 m3       105.00         108.15
Carpenter          0.80 h          22.00          17.60
Labourer           1.60 h          16.00          25.60
Concrete vibrator  0.30 h           8.00           2.40
                                   -------------------------
Direct unit cost per m3                          153.75
```

Multiply the composition's unit cost by the taken-off quantity to get the
**direct cost** of that service, and sum all services for the **total
direct cost** of the project:

```text
Service direct cost = unit cost * quantity

Concrete:   153.75 * 240 m3   =  36 900.00
Formwork:    62.00 * 1 850 m2  = 114 700.00
Rebar:        9.80 * 19 200 kg = 188 160.00
                                 -----------
Total direct cost (extract)      339 760.00
```

The coefficients embed **productivity and losses** - the 1.03 on concrete,
for instance, accounts for a 3 percent placing loss. Getting coefficients
right (from reference tables or your own historical data) is what makes an
estimate realistic.

```mermaid
graph TD
    DWG["Drawings and specs"] --> TO["Quantity take-off"]
    TO --> QTY["Quantities per service"]
    COMP["Unit-price composition"] --> UC["Unit cost of service"]
    QTY --> MULT["Quantity times unit cost"]
    UC --> MULT
    MULT --> DIRECT["Total direct cost"]
```

Remember: quantities from the drawings, unit costs from compositions,
multiply and sum for the **direct cost**. This is the raw cost of the work
itself - what it takes to convert it into a bid price is the next lesson.
""",
        ),
        quiz_lesson(
            "Quiz: Quantity take-off and cost composition",
            (
                q(
                    "What is a quantity take-off?",
                    (
                        opt("A discount taken off the final price"),
                        opt(
                            "The systematic measurement of every item of work from the "
                            "drawings and specifications",
                            correct=True,
                        ),
                        opt("The removal of scope from a project"),
                        opt("A schedule of activity durations"),
                    ),
                    "Take-off measures the quantities (m3, m2, kg) that the budget is "
                    "then built on.",
                ),
                q(
                    "In a unit-price composition, a coefficient represents what?",
                    (
                        opt("The profit margin"),
                        opt(
                            "The consumption of an input per unit of the service (e.g. "
                            "hours of labour per m3)",
                            correct=True,
                        ),
                        opt("The tax rate"),
                        opt("The number of activities"),
                    ),
                    "Coefficient times unit price, summed over inputs, gives the unit "
                    "cost; coefficients embed productivity and losses.",
                ),
                q(
                    "If 1 m3 of concrete costs 153.75 and you need 240 m3, what is the "
                    "direct cost of the concrete service?",
                    (
                        opt("153.75"),
                        opt("240.00"),
                        opt("36 900.00", correct=True),
                        opt("393.75"),
                    ),
                    "Service direct cost = unit cost * quantity = 153.75 * 240 = 36 900.00.",
                ),
            ),
        ),
        # -- 6. BDI, indirect costs and cash flow ----------------------
        _t(
            "BDI, indirect costs and cash flow",
            "12 min",
            """# BDI, indirect costs and cash flow

The direct cost is not the price. To turn direct cost into a **selling
price**, you add **indirect costs**, taxes and profit through the **BDI**
(*Beneficios e Despesas Indiretas* - a benchmark discussed in Brazil by
TCU Acordao 2622/2013 and NBR conventions). Everything that is not a
direct input to a specific service lives here:

- **Site indirect costs (canteiro)** - site management salaries,
  temporary facilities, security, insurance: real costs not tied to one
  service, often carried as a separate item or inside BDI.
- **Central administration** - the head-office overhead a project must
  help pay for.
- **Financial cost** - the cost of financing the works before payment.
- **Risk / contingency** - allowance for uncertain events.
- **Taxes on turnover** - e.g. ISS, PIS, COFINS.
- **Profit** - the contractor's margin.

BDI is expressed as a **markup rate** applied to the direct cost:

```text
BDI rate (multiplicative form):

BDI = ( (1 + AC + R + F) * (1 + G) ) / (1 - T) - 1

  AC = admin + site indirects   (e.g. 0.08)
  R  = risk / contingency       (e.g. 0.01)
  F  = financial cost           (e.g. 0.01)
  G  = profit                   (e.g. 0.07)
  T  = taxes on turnover        (e.g. 0.0865)

  BDI = ((1 + 0.08 + 0.01 + 0.01) * (1 + 0.07)) / (1 - 0.0865) - 1
      = (1.10 * 1.07) / 0.9135 - 1
      = 1.1770 / 0.9135 - 1  =  0.2885  ->  28.85 percent

Selling price = direct cost * (1 + BDI)
  = 339 760.00 * 1.2885 = 437 785.00 (approx)
```

Money also has **timing**. The **cash flow** spreads cost and revenue
across the schedule; because expenses often lead receipts, a project
usually needs **working capital**. Plotting cumulative cost over time
gives the classic **S-curve** (slow start, steep middle, tapering end),
the baseline you later compare actual spend against.

```text
Cumulative cost S-curve (planned, R$ thousand)

Month    1    2    3    4    5    6
Monthly  20   55   90   95   60   30
Cumul.   20   75  165  260  320  350   <- slow, steep, taper
```

```mermaid
graph LR
    DC["Direct cost"] --> ADD["Add indirects admin risk finance"]
    ADD --> TAX["Apply taxes and profit"]
    TAX --> BDI["BDI markup rate"]
    BDI --> PRICE["Selling price"]
    PRICE --> SCURVE["Distribute over time S-curve"]
    SCURVE --> CAP["Working capital need"]
```

Remember: **price = direct cost * (1 + BDI)**, BDI packages indirects,
taxes, risk and profit, and the S-curve turns that price into a
time-phased plan you will control against.
""",
        ),
        quiz_lesson(
            "Quiz: BDI, indirect costs and cash flow",
            (
                q(
                    "What does BDI add to the direct cost?",
                    (
                        opt("Only the profit"),
                        opt(
                            "Indirect costs, central administration, financial cost, "
                            "risk, taxes on turnover and profit",
                            correct=True,
                        ),
                        opt("Nothing - it is a discount"),
                        opt("Only the taxes"),
                    ),
                    "BDI is the markup that turns direct cost into a selling price, "
                    "packaging everything not tied to a specific service.",
                ),
                q(
                    "If the direct cost is 339 760 and BDI is 28.85 percent, the selling "
                    "price is about...",
                    (
                        opt("339 760"),
                        opt("437 785", correct=True),
                        opt("98 025"),
                        opt("240 000"),
                    ),
                    "Selling price = direct cost * (1 + BDI) = 339 760 * 1.2885 = 437 785 approx.",
                ),
                q(
                    "What does the cumulative-cost S-curve represent?",
                    (
                        opt("The critical path length"),
                        opt(
                            "The planned spend distributed over time - slow start, steep "
                            "middle, tapering end - used as a control baseline",
                            correct=True,
                        ),
                        opt("The number of workers per trade"),
                        opt("The tax rate over time"),
                    ),
                    "The S-curve time-phases the budget; because cost often leads "
                    "revenue, the project needs working capital.",
                ),
            ),
        ),
        # -- 7. 4D/5D BIM and earned-value control ---------------------
        _t(
            "4D/5D BIM planning and earned-value control",
            "12 min",
            """# 4D/5D BIM planning and earned-value control

Modern planning is **digital**. A **BIM** (Building Information Modeling)
model is a coordinated 3D database of the asset. Linking that model to
**time** gives **4D**; linking it further to **cost** gives **5D**:

- **4D BIM** - each model element is tied to a schedule activity, so you
  can **simulate the build sequence** visually, spot space and access
  clashes, and communicate the plan far better than a bar chart.
- **5D BIM** - quantities extracted from the model drive the cost, so a
  design change updates quantities, cost and schedule together. Open
  exchange uses **IFC** (the neutral **openBIM** format).

Digital planning still needs **objective control**. **Earned Value
Management (EVM)** measures progress in money, combining scope, schedule
and cost in three base values:

- **PV** (Planned Value) - budgeted cost of work **scheduled** to date.
- **EV** (Earned Value) - budgeted cost of work **actually done** to date.
- **AC** (Actual Cost) - what that done work actually cost.

From these come the variances and indices:

```text
Earned Value control - end of month 4

Planned value  PV = 260 000   (from the S-curve)
Earned value   EV = 234 000   (percent complete * budget)
Actual cost    AC = 250 000   (invoices and payroll)

Schedule variance  SV = EV - PV = 234 000 - 260 000 = -26 000  (behind)
Cost variance      CV = EV - AC = 234 000 - 250 000 = -16 000  (over)

Schedule Perf. Index  SPI = EV / PV = 234000 / 260000 = 0.90
Cost Perf. Index      CPI = EV / AC = 234000 / 250000 = 0.94

Estimate at Completion (typical):
  EAC = BAC / CPI = 500 000 / 0.94 = 531 915  (forecast overrun)
```

SPI and CPI below 1.0 both signal trouble - here the project is **behind
schedule and over cost**, and the forecast EAC exceeds the budget at
completion (BAC). EVM turns a vague "we feel late" into a number and a
forecast.

```mermaid
graph TD
    MODEL["3D BIM model"] --> D4["Link to schedule 4D"]
    MODEL --> D5["Link to cost 5D"]
    D4 --> PLAN["Time phased plan PV"]
    D5 --> BUDGET["Model based budget"]
    PLAN --> EVM["Earned value EV AC"]
    EVM --> INDEX["SPI and CPI and EAC forecast"]
```

Remember: 4D/5D BIM builds the project virtually before it is built for
real, and earned value control measures schedule and cost performance in
one consistent currency - SPI and CPI under 1.0 mean act now.
""",
        ),
        quiz_lesson(
            "Quiz: 4D/5D BIM planning and earned-value control",
            (
                q(
                    "What do 4D and 5D BIM add to a 3D model?",
                    (
                        opt("Colour and lighting only"),
                        opt(
                            "4D links elements to the schedule (time); 5D links them to "
                            "cost, so changes update quantities, cost and schedule together",
                            correct=True,
                        ),
                        opt("Nothing - they are marketing terms"),
                        opt("They remove the need for a model"),
                    ),
                    "3D + time = 4D (sequence simulation); 4D + cost = 5D; IFC is the "
                    "neutral openBIM exchange format.",
                ),
                q(
                    "In EVM, what is Earned Value (EV)?",
                    (
                        opt("What the work actually cost"),
                        opt("The cost scheduled to date"),
                        opt(
                            "The budgeted cost of the work actually completed to date",
                            correct=True,
                        ),
                        opt("The profit margin"),
                    ),
                    "EV = budgeted cost of work done; PV is scheduled, AC is actual "
                    "cost - the three anchor every EVM metric.",
                ),
                q(
                    "SPI = 0.90 and CPI = 0.94. What does this tell you?",
                    (
                        opt("Ahead of schedule and under budget"),
                        opt(
                            "Behind schedule and over cost - both indices below 1.0",
                            correct=True,
                        ),
                        opt("Exactly on plan"),
                        opt("The project is finished"),
                    ),
                    "Indices under 1.0 signal trouble; EAC = BAC / CPI then forecasts an overrun.",
                ),
            ),
        ),
        # -- 8. Health and safety management ---------------------------
        _t(
            "Health and safety management on site",
            "11 min",
            """# Health and safety management on site

No schedule or budget matters if people are harmed building it.
Construction is a high-hazard industry, and **health and safety
management** is both a legal duty and a core management function. In
Brazil it is framed by the **Normas Regulamentadoras (NR)**, notably
**NR-18** (construction), **NR-35** (work at height), **NR-6** (personal
protective equipment) and **NR-12** (machinery), alongside international
frameworks such as **ISO 45001**.

The professional approach is **prevention through a hierarchy of
controls** - always prefer measures that remove the hazard over those that
merely protect the worker:

- **Elimination** - remove the hazard (design out a hazardous task).
- **Substitution** - replace it with something safer.
- **Engineering controls** - guardrails, edge protection, mechanized lifting.
- **Administrative controls** - permits to work, training, signage, sequence.
- **PPE** - helmet, harness, boots - the **last** line, not the first.

The engine is **risk assessment**: identify hazards, assess each by
**likelihood** and **severity**, prioritize, and apply controls to the top
risks. A simple **risk matrix** ranks them:

```text
Risk score = Likelihood (1-5) * Severity (1-5)

Hazard                     L   S   Score   Priority
Fall from slab edge        4   5    20     Critical - edge protection now
Struck by crane load       2   5    10     High - exclusion zone, banksman
Manual handling strain     4   2     8     Medium - mechanize, train
Trip on cable runs         3   1     3     Low - housekeeping

Act on highest scores first; re-score after controls (residual risk).
```

Key site instruments include the **PCMAT/PGR** (safety programme), the
daily **DDS** toolbox talks, the **CIPA** workers' safety committee,
permits to work for high-risk tasks, and **leading indicators** (near-miss
reports, audits) rather than only reacting to injury statistics.

```mermaid
graph TD
    ID["Identify hazards"] --> ASSESS["Assess likelihood and severity"]
    ASSESS --> RANK["Rank on risk matrix"]
    RANK --> ELIM["Eliminate or substitute"]
    ELIM --> ENG["Engineering controls"]
    ENG --> ADMIN["Administrative controls"]
    ADMIN --> PPE["PPE last line"]
    PPE --> MONITOR["Monitor audit and improve"]
    MONITOR --> ID
```

Remember: safety is managed, not hoped for - assess risk, apply the
hierarchy of controls with PPE as the last resort, comply with the NR
framework, and lead with near-misses so you learn before, not after,
someone is hurt.
""",
        ),
        quiz_lesson(
            "Quiz: Health and safety management on site",
            (
                q(
                    "In the hierarchy of controls, where does PPE sit?",
                    (
                        opt("First - it is the primary defence"),
                        opt(
                            "Last - after elimination, substitution, engineering and "
                            "administrative controls",
                            correct=True,
                        ),
                        opt("It is not part of the hierarchy"),
                        opt("Above engineering controls"),
                    ),
                    "Always prefer removing the hazard; PPE (helmet, harness, boots) is "
                    "the last line, not the first.",
                ),
                q(
                    "A hazard has likelihood 4 and severity 5. What is its risk score "
                    "and priority?",
                    (
                        opt("9 - low"),
                        opt("20 - the highest, act first", correct=True),
                        opt("1 - ignore it"),
                        opt("45 - medium"),
                    ),
                    "Risk score = likelihood * severity = 4 * 5 = 20; the fall-from-edge "
                    "hazard is critical and gets edge protection immediately.",
                ),
                q(
                    "Which Brazilian regulation specifically governs work at height?",
                    (
                        opt("NR-18"),
                        opt("NR-35", correct=True),
                        opt("NR-6"),
                        opt("NR-12"),
                    ),
                    "NR-35 covers work at height; NR-18 is construction generally, NR-6 "
                    "PPE, NR-12 machinery.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does the choice of construction method drive?",
                    (
                        opt("Only the paint colour"),
                        opt(
                            "The technology and sequence of execution, and therefore "
                            "durations, crews, equipment and cost",
                            correct=True,
                        ),
                        opt("Only the financing rate"),
                        opt("Nothing measurable"),
                    ),
                    "Method and site logistics are the first design decisions of "
                    "construction; they shape the schedule and budget.",
                ),
                q(
                    "What is the '100 percent rule' of a WBS?",
                    (
                        opt("Every activity takes 100 days"),
                        opt(
                            "The children of a node sum to exactly the whole of that node "
                            "- nothing missing, nothing double counted",
                            correct=True,
                        ),
                        opt("Crews must be fully utilized"),
                        opt("The design must be complete first"),
                    ),
                    "Complete, non-overlapping decomposition; scope adds up at every level.",
                ),
                q(
                    "A crew does 40 m2 per day and there are 800 m2. The duration is...",
                    (
                        opt("40 days"),
                        opt("20 days", correct=True),
                        opt("800 days"),
                        opt("2 days"),
                    ),
                    "duration = quantity / productivity = 800 / 40 = 20 working days.",
                ),
                q(
                    "What defines the critical path?",
                    (
                        opt("The cheapest chain of activities"),
                        opt(
                            "The longest path of dependent activities, with zero float, "
                            "setting the minimum project duration",
                            correct=True,
                        ),
                        opt("The path with the most float"),
                        opt("The first activity only"),
                    ),
                    "Zero float means any delay on it slips the whole project.",
                ),
                q(
                    "Using PERT with o=3, m=5, p=13, the expected duration te is...",
                    (
                        opt("5 days"),
                        opt("6 days", correct=True),
                        opt("7 days"),
                        opt("13 days"),
                    ),
                    "te = (o + 4m + p) / 6 = (3 + 20 + 13) / 6 = 36 / 6 = 6 days.",
                ),
                q(
                    "In the Last Planner System, what does PPC measure?",
                    (
                        opt("The profit margin"),
                        opt(
                            "The fraction of planned tasks completed as planned - the "
                            "reliability of the weekly plan",
                            correct=True,
                        ),
                        opt("The concrete strength"),
                        opt("The critical path length"),
                    ),
                    "PPC = completed / planned * 100; low PPC plus reasons for "
                    "non-completion drives improvement.",
                ),
                q(
                    "In a unit-price composition, a coefficient is...",
                    (
                        opt("The profit"),
                        opt(
                            "The consumption of an input per unit of service, embedding "
                            "productivity and losses",
                            correct=True,
                        ),
                        opt("The tax rate"),
                        opt("The total quantity"),
                    ),
                    "Coefficient times unit price, summed over labour, materials and "
                    "equipment, gives the unit cost.",
                ),
                q(
                    "How do you turn direct cost into a selling price?",
                    (
                        opt("Subtract the taxes"),
                        opt(
                            "Multiply by (1 + BDI), where BDI packages indirects, "
                            "finance, risk, taxes and profit",
                            correct=True,
                        ),
                        opt("Divide by the number of activities"),
                        opt("Add only the profit"),
                    ),
                    "Price = direct cost * (1 + BDI); the S-curve then time-phases it.",
                ),
                q(
                    "In earned value, SPI = 0.90 and CPI = 0.94 mean the project is...",
                    (
                        opt("Ahead and under budget"),
                        opt("Behind schedule and over cost", correct=True),
                        opt("Exactly on plan"),
                        opt("Complete"),
                    ),
                    "Both indices under 1.0 signal trouble; EAC = BAC / CPI forecasts an overrun.",
                ),
                q(
                    "In the hierarchy of controls, PPE is...",
                    (
                        opt("The first and best defence"),
                        opt(
                            "The last line, used after elimination, substitution, "
                            "engineering and administrative controls",
                            correct=True,
                        ),
                        opt("Not a real control"),
                        opt("Only for managers"),
                    ),
                    "Prefer removing the hazard; PPE protects the worker only when "
                    "higher controls cannot fully eliminate the risk.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CONSTRUCTION_MANAGEMENT_COST_COURSES: tuple[SeedCourse, ...] = (_CONSTRUCTION_MANAGEMENT_COST,)
