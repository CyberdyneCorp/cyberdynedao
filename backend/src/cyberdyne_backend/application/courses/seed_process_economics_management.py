"""Academy seed content - Process Economics and Project Management.

The money and management side of chemical engineering projects: how to
estimate capital (CAPEX) and operating (OPEX) costs, put a value on money
across time, judge profitability with NPV, IRR and payback, test a project
against uncertainty, and then actually run it - PMBOK, stage-gate and Agile
delivery plus Lean/Six Sigma/TPM operational excellence. Every lesson is a
direct explanation with a worked calculation and a mermaid diagram, followed
by a checkpoint quiz; the course closes with a comprehensive final quiz.
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


_PROCESS_ECONOMICS_MANAGEMENT = SeedCourse(
    slug="process-economics-management",
    title="Process Economics & Project Management",
    description=(
        "The money and management of chemical projects: capital and operating "
        "cost estimation, profitability analysis (NPV, IRR, payback), "
        "sensitivity and risk, project management (PMBOK, stage-gate, Agile), "
        "and operational excellence (Lean, Six Sigma, TPM) - with worked "
        "cost, cash-flow and discounting calculations and a diagram in every "
        "lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Process Economics and Project Management

A process can be technically brilliant and still never get built - because
it does not make money, or because the project to build it runs late and
over budget. This course is about the two questions every engineering
manager asks: **is it worth doing?** and **can we deliver it?**

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short worked calculation (a cost estimate, a
cash-flow table, a discounting formula), and draws the idea as a diagram.
After each lesson there is a short quiz; at the end, a final quiz covers
the whole course.

What you will build understanding for, in order:

1. **Capital cost estimation (CAPEX)** - what a plant costs to build
2. **Operating cost estimation (OPEX)** - what it costs to run each year
3. **Time value of money** - a dollar today beats a dollar next year
4. **Profitability metrics** - NPV, IRR and payback for the go decision
5. **Sensitivity and risk analysis** - how wrong could the estimate be
6. **Project management** - PMBOK, stage-gate and Agile delivery
7. **Operational excellence** - Lean, Six Sigma and TPM once it runs
8. **Techno-economic decision-making** - putting it all together

Grounded in real practice - Aspen Process Economic Analyzer factored
estimates, AACE estimate classes, PMBOK and stage-gate governance - but
kept teachable. The point is judgement: numbers plus the management to act
on them.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What two questions does this course help you answer?",
                    (
                        opt("Which programming language and which cloud"),
                        opt(
                            "Is the project worth doing (economics) and can we "
                            "deliver it (project management)",
                            correct=True,
                        ),
                        opt("Who to hire and where to build the office"),
                        opt("Which reactor and which distillation column"),
                    ),
                    "Economics answers 'worth doing'; project and operations "
                    "management answer 'can we deliver and run it'.",
                ),
                q(
                    "How is each content lesson structured?",
                    (
                        opt("A long theory dump with no examples"),
                        opt(
                            "A direct explanation, one worked calculation, and a "
                            "mermaid diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A video with no text"),
                    ),
                    "Explain, show a worked number, draw the idea, then check "
                    "understanding with a quiz.",
                ),
            ),
        ),
        # -- 1. CAPEX --------------------------------------------------
        _t(
            "Capital cost estimation (CAPEX)",
            "10 min",
            """# Capital cost estimation (CAPEX)

**Capital expenditure (CAPEX)** is the one-time cost to design, build and
commission a plant before it earns a cent. It is dominated by equipment,
but the equipment is only a fraction of the total: pipes, instruments,
electrical, civil works, engineering and contingency multiply it up.

Estimates come in **classes** of increasing accuracy and effort. The AACE
International system runs from **Class 5** (order-of-magnitude, plus or
minus 30 to 50 percent) to **Class 1** (definitive, plus or minus 5 to 10
percent). You do not pay for a Class 1 estimate to screen an idea.

Two workhorse methods:

- **Capacity scaling (the six-tenths rule)** - scale a known plant cost by
  the capacity ratio raised to an exponent (about 0.6). Bigger plants cost
  less per unit of capacity - economy of scale.
- **Factored (Lang / Hand) estimates** - price the major equipment, then
  multiply by installation factors to reach total installed cost, and by a
  **Lang factor** to reach total capital. Aspen Process Economic Analyzer
  automates this from a simulation.

The six-tenths rule, worked:

```text
Cost scaling (six-tenths rule):
  Cost_2 = Cost_1 * (Capacity_2 / Capacity_1) ^ n,  n approx 0.6

Known:  a 100,000 t/yr plant cost 40 MUSD.
Want:   cost of a 250,000 t/yr plant of the same type.

  Cost_2 = 40 * (250,000 / 100,000) ^ 0.6
         = 40 * (2.5) ^ 0.6
         = 40 * 1.732
         = 69.3 MUSD

Per-unit capacity: 400 USD/t vs 277 USD/t -> economy of scale.
Then adjust to today with a cost index (e.g. CEPCI):
  Cost_now = Cost_then * (Index_now / Index_then)
```

```mermaid
graph TD
    EQ["Purchased equipment cost"] --> INST["Installation factors"]
    INST --> TIC["Total installed cost"]
    TIC --> IND["Indirect costs engineering"]
    IND --> CONT["Contingency"]
    CONT --> TCI["Total capital investment"]
    TCI --> CLASS["AACE estimate class sets accuracy"]
```

Remember: equipment is the seed, factors grow it to total capital, and the
estimate class tells you how much to trust the number.
""",
        ),
        quiz_lesson(
            "Quiz: Capital cost estimation (CAPEX)",
            (
                q(
                    "What does the six-tenths rule let you do?",
                    (
                        opt("Convert costs between currencies"),
                        opt(
                            "Scale a known plant cost to a different capacity using "
                            "the capacity ratio raised to about 0.6",
                            correct=True,
                        ),
                        opt("Estimate annual operating labour"),
                        opt("Compute the internal rate of return"),
                    ),
                    "Cost_2 = Cost_1 * (Cap_2/Cap_1)^0.6; the sub-linear exponent "
                    "captures economy of scale.",
                ),
                q(
                    "What is a Lang (or Hand) factor used for?",
                    (
                        opt("Discounting future cash flows"),
                        opt(
                            "Multiplying purchased-equipment cost up to total "
                            "capital investment, accounting for installation and "
                            "indirects",
                            correct=True,
                        ),
                        opt("Converting mass to moles"),
                        opt("Setting the depreciation schedule"),
                    ),
                    "Factored estimates: equipment cost times installation and Lang "
                    "factors gives total installed and total capital.",
                ),
                q(
                    "Why do AACE estimate classes matter?",
                    (
                        opt("They set the plant's selling price"),
                        opt(
                            "They tell you the accuracy and effort - a Class 5 "
                            "screen is rough, a Class 1 definitive estimate is tight",
                            correct=True,
                        ),
                        opt("They are legal safety limits"),
                        opt("They fix the exchange rate"),
                    ),
                    "Class 5 is plus or minus 30 to 50 percent for screening; Class "
                    "1 is plus or minus 5 to 10 percent for sanction.",
                ),
            ),
        ),
        # -- 2. OPEX ---------------------------------------------------
        _t(
            "Operating cost estimation (OPEX)",
            "10 min",
            """# Operating cost estimation (OPEX)

**Operating expenditure (OPEX)** is the recurring annual cost to run the
plant. Where CAPEX is one-time, OPEX repeats every year the plant operates,
and over a plant life it usually dwarfs the capital cost.

Split OPEX into two families:

- **Variable costs** scale with production rate: **raw materials**
  (usually the largest single item in a chemical process), **utilities**
  (steam, cooling water, electricity, refrigeration), and consumables like
  catalyst and solvents.
- **Fixed costs** are incurred whether you make one tonne or full rate:
  **operating labour** and supervision, **maintenance** (often estimated
  as a percentage of CAPEX, say 3 to 5 percent per year), insurance, local
  taxes and plant overhead.

Raw-material cost per tonne of product comes straight from the **mass
balance** and yield - poor yield burns money twice, in wasted feed and in
extra separation. Utility cost comes from the **energy balance** and unit
utility prices.

A simple annual OPEX build-up:

```text
Annual operating cost (per year), 200,000 t/yr product:

  Raw materials: 1.1 t feed / t product at 600 USD/t feed
     = 200,000 * 1.1 * 600            = 132.0 MUSD/yr
  Utilities: 4 GJ steam / t at 8 USD/GJ
     = 200,000 * 4 * 8                =   6.4 MUSD/yr
  Fixed - labour, 20 operators at 90 kUSD =  1.8 MUSD/yr
  Fixed - maintenance, 4 percent of 70 MUSD CAPEX =  2.8 MUSD/yr
  Overhead and insurance                =   1.5 MUSD/yr
  ------------------------------------------------------
  Total annual OPEX                     = 144.5 MUSD/yr

  Cash cost of production = 144.5 / 200,000 = 722 USD/t
```

```mermaid
graph TD
    OPEX["Annual operating cost"] --> VAR["Variable costs"]
    OPEX --> FIX["Fixed costs"]
    VAR --> RAW["Raw materials from mass balance"]
    VAR --> UTIL["Utilities from energy balance"]
    FIX --> LAB["Labour and supervision"]
    FIX --> MAINT["Maintenance percent of CAPEX"]
```

Remember: raw materials usually dominate, variable costs follow the mass
and energy balances, and fixed costs run whether the plant is busy or idle.
""",
        ),
        quiz_lesson(
            "Quiz: Operating cost estimation (OPEX)",
            (
                q(
                    "Which item is usually the largest single OPEX component in a "
                    "chemical process?",
                    (
                        opt("Operating labour"),
                        opt("Raw materials", correct=True),
                        opt("Insurance"),
                        opt("Local property taxes"),
                    ),
                    "Feedstock cost, set by the mass balance and yield, typically "
                    "dominates the cash cost of production.",
                ),
                q(
                    "What distinguishes a variable cost from a fixed cost?",
                    (
                        opt("Variable costs are paid once, fixed costs recur"),
                        opt(
                            "Variable costs scale with production rate; fixed costs "
                            "are incurred regardless of output",
                            correct=True,
                        ),
                        opt("Fixed costs only apply to imported materials"),
                        opt("There is no real difference"),
                    ),
                    "Raw materials and utilities scale with rate; labour and "
                    "maintenance are largely fixed.",
                ),
                q(
                    "Maintenance cost is often estimated as...",
                    (
                        opt("a fixed 1 USD per tonne of product"),
                        opt("the same as raw-material cost"),
                        opt(
                            "a percentage of the capital investment, commonly 3 to "
                            "5 percent per year",
                            correct=True,
                        ),
                        opt("zero until the plant is ten years old"),
                    ),
                    "A percent-of-CAPEX rule of thumb gives a defensible fixed "
                    "maintenance figure early in a study.",
                ),
            ),
        ),
        # -- 3. Time value of money ------------------------------------
        _t(
            "Time value of money and cash flow",
            "10 min",
            """# Time value of money and cash flow

A dollar today is worth more than a dollar next year - you could invest
today's dollar and earn a return, and inflation erodes the future one.
This is the **time value of money**, and it is the reason we cannot simply
add up a project's cash flows across years and compare the total.

Two mirror operations, both using a **discount rate** i (the return the
company requires, often the weighted average cost of capital):

- **Compounding** grows a present value forward: a value P grows to
  **F = P (1 + i)^n** after n years.
- **Discounting** brings a future value back: **PV = F / (1 + i)^n**. The
  factor **1 / (1 + i)^n** is the discount factor; it shrinks with time.

A project is a stream of **cash flows** over its life: a large negative
outflow while you build (CAPEX), then annual net inflows (revenue minus
OPEX minus tax) once it runs, spread over the plant life. Discounting each
year's cash flow to today lets you add them on a common basis.

Discounting a cash flow, worked:

```text
Discount rate i = 10 percent (0.10). Discount factor DF = 1/(1+i)^n

  Year n   Cash flow (MUSD)   DF = 1/1.1^n   Present value (MUSD)
    0        -70.0            1.000           -70.00
    1        +18.0            0.909           +16.36
    2        +18.0            0.826           +14.88
    3        +18.0            0.751           +13.52
    4        +18.0            0.683           +12.29
    5        +18.0            0.621           +11.18
  ---------------------------------------------------------------
  Sum of discounted inflows (yr 1-5)          +68.23
  Net (add year 0 outflow)                     -1.77  -> NPV
```

```mermaid
graph LR
    NOW["Cash flow at year n"] --> DF["Divide by one plus i to the n"]
    DF --> PV["Present value today"]
    PV --> SUM["Sum all years"]
    SUM --> BASIS["Common basis for comparison"]
    RATE["Discount rate i is required return"] --> DF
```

Remember: money has a time value, so discount every future cash flow to
today before you add or compare - the discount rate carries the required
return.
""",
        ),
        quiz_lesson(
            "Quiz: Time value of money and cash flow",
            (
                q(
                    "Why is a dollar today worth more than a dollar next year?",
                    (
                        opt("Because banks charge fees"),
                        opt(
                            "Today's dollar can be invested to earn a return, and "
                            "inflation erodes the future dollar's value",
                            correct=True,
                        ),
                        opt("Because coins wear out over time"),
                        opt("It is not - they are always equal"),
                    ),
                    "Opportunity to earn a return plus inflation gives money a time value.",
                ),
                q(
                    "What is the present value of a future cash flow F, n years "
                    "out, at discount rate i?",
                    (
                        opt("F * (1 + i)^n"),
                        opt("F / (1 + i)^n", correct=True),
                        opt("F * i * n"),
                        opt("F - i * n"),
                    ),
                    "Discounting divides by (1+i)^n; compounding would multiply by it.",
                ),
                q(
                    "What does the discount rate usually represent?",
                    (
                        opt("The plant's electricity tariff"),
                        opt(
                            "The return the company requires, often the weighted "
                            "average cost of capital",
                            correct=True,
                        ),
                        opt("The corporate tax rate"),
                        opt("The rate of product price inflation only"),
                    ),
                    "The discount rate encodes the required return / cost of "
                    "capital used to value future money today.",
                ),
            ),
        ),
        # -- 4. Profitability metrics ----------------------------------
        _t(
            "Profitability metrics (NPV, IRR, payback)",
            "11 min",
            """# Profitability metrics (NPV, IRR, payback)

With discounted cash flows in hand, three metrics turn the stream into a
go / no-go answer. Each asks a different question.

**Net Present Value (NPV)** - the sum of every cash flow discounted to
today. **NPV greater than zero** means the project earns more than the
discount rate demands; it creates value. NPV is the single most defensible
metric because it is in money and it respects the time value of money.

```text
NPV = sum over n of  CF_n / (1 + i)^n

From the year 0-5 table (i = 10 percent): NPV = -1.77 MUSD  (reject)
```

**Internal Rate of Return (IRR)** - the discount rate that makes NPV
exactly zero. Compare it to the **hurdle rate**: if IRR is above the
hurdle, accept. IRR is intuitive (a percentage) but has traps: it assumes
reinvestment at the IRR, and unconventional cash flows (sign changes) can
give multiple IRRs.

**Payback period** - how long until cumulative cash flow turns positive.
**Simple payback** ignores the time value of money; **discounted payback**
uses discounted flows. Payback measures how fast you get your money back
(a rough risk/liquidity gauge) but ignores everything after break-even, so
never use it alone.

```text
Simple payback (undiscounted), CAPEX 70 MUSD, 18 MUSD/yr net:
  Payback = 70 / 18 = 3.9 years

Rule set:
  NPV > 0          -> accept (creates value at the discount rate)
  IRR > hurdle     -> accept
  Payback          -> supporting risk gauge only, not decisive
```

```mermaid
graph TD
    CF["Discounted cash flows"] --> NPV["NPV sum of discounted flows"]
    CF --> IRR["IRR rate where NPV is zero"]
    CF --> PB["Payback time to break even"]
    NPV --> DEC{"NPV greater than zero"}
    DEC -->|"yes"| GO["Create value accept"]
    DEC -->|"no"| STOP["Reject or rework"]
    IRR --> HURD["Compare to hurdle rate"]
```

Remember: NPV decides (value in money), IRR communicates (a percentage to
compare with the hurdle), and payback flags risk - use NPV as the anchor.
""",
        ),
        quiz_lesson(
            "Quiz: Profitability metrics (NPV, IRR, payback)",
            (
                q(
                    "What does a positive NPV tell you?",
                    (
                        opt("The project pays back in under a year"),
                        opt(
                            "The project earns more than the discount rate requires "
                            "- it creates value",
                            correct=True,
                        ),
                        opt("The IRR is exactly zero"),
                        opt("The plant will never lose money in any year"),
                    ),
                    "NPV > 0 means the discounted inflows exceed the outflows at "
                    "the required return.",
                ),
                q(
                    "How is the internal rate of return (IRR) defined?",
                    (
                        opt("The plant's gross margin"),
                        opt("The average annual profit"),
                        opt(
                            "The discount rate at which NPV equals zero",
                            correct=True,
                        ),
                        opt("The payback period in years"),
                    ),
                    "IRR is the break-even discount rate; accept if it exceeds the hurdle rate.",
                ),
                q(
                    "Why should payback period never be the sole decision metric?",
                    (
                        opt("It is too hard to calculate"),
                        opt(
                            "It ignores all cash flows after break-even and (in "
                            "simple form) the time value of money",
                            correct=True,
                        ),
                        opt("It always gives a negative number"),
                        opt("It requires the IRR first"),
                    ),
                    "Payback is a liquidity/risk gauge; it says nothing about total "
                    "value created, so anchor on NPV.",
                ),
            ),
        ),
        # -- 5. Sensitivity and risk -----------------------------------
        _t(
            "Sensitivity and risk analysis",
            "10 min",
            """# Sensitivity and risk analysis

Every number in an economic study is an estimate, and the NPV can flip
from positive to negative on assumptions you are not sure of. **Sensitivity
and risk analysis** ask: how wrong could we be, and which inputs matter
most?

**Sensitivity analysis** varies one input at a time and watches the
output. Plot NPV against each input across a range (say plus or minus 20
percent) and the steepest lines are the variables that dominate - a
**tornado diagram** ranks them. In most chemical projects the top drivers
are **product price**, **feedstock cost**, and **plant capacity /
utilisation**, not the small line items.

**Scenario analysis** bundles inputs into coherent cases - a pessimistic,
base, and optimistic set - because inputs move together (low demand often
means low price and low utilisation at once).

**Monte Carlo simulation** goes further: assign a probability distribution
to each uncertain input, sample thousands of combinations, and get a
**distribution of NPV**. Instead of one number you get the probability the
project loses money and the expected value.

A sensitivity sweep on price:

```python
import numpy as np

capex = 70.0            # MUSD
years = np.arange(1, 11)
i = 0.10                # discount rate
df = 1 / (1 + i) ** years

# base net cash flow 18 MUSD/yr; sweep +/-20% on product price,
# which moves revenue and thus net cash flow
for price_factor in (0.8, 0.9, 1.0, 1.1, 1.2):
    net = 18.0 * price_factor          # simplified: price scales net CF
    npv = -capex + np.sum(net * df)
    print(f"price {price_factor:>4}x -> NPV {npv:6.1f} MUSD")

# price 0.8x -> NPV  18.5 MUSD
# price 1.0x -> NPV  40.6 MUSD
# price 1.2x -> NPV  62.7 MUSD   (NPV is highly sensitive to price)
```

```mermaid
graph TD
    BASE["Base case estimate"] --> SENS["Sensitivity vary one input"]
    SENS --> TORN["Tornado ranks the drivers"]
    BASE --> SCEN["Scenarios low base high"]
    BASE --> MC["Monte Carlo distributions"]
    MC --> PDIST["Distribution of NPV"]
    PDIST --> PLOSS["Probability of loss"]
```

Remember: find the few inputs that swing the answer, stress them honestly,
and where it matters use Monte Carlo to turn a single NPV into a probability
of success.
""",
        ),
        quiz_lesson(
            "Quiz: Sensitivity and risk analysis",
            (
                q(
                    "What does a sensitivity (tornado) analysis reveal?",
                    (
                        opt("The exact future price of the product"),
                        opt(
                            "Which input variables the NPV is most sensitive to, "
                            "ranked by their impact",
                            correct=True,
                        ),
                        opt("The plant's maintenance schedule"),
                        opt("The number of operators required"),
                    ),
                    "Vary one input at a time; the steepest responses (widest "
                    "tornado bars) are the dominant drivers.",
                ),
                q(
                    "What does a Monte Carlo simulation give you that a single "
                    "base-case NPV does not?",
                    (
                        opt("A lower CAPEX"),
                        opt(
                            "A distribution of NPV outcomes and the probability the "
                            "project loses money",
                            correct=True,
                        ),
                        opt("The correct discount rate"),
                        opt("A guaranteed profit"),
                    ),
                    "Sampling distributions for uncertain inputs yields a spread of "
                    "NPVs and a probability of loss.",
                ),
                q(
                    "In a typical chemical project, which inputs most often dominate the NPV?",
                    (
                        opt("Insurance premiums and office supplies"),
                        opt(
                            "Product price, feedstock cost, and plant capacity/utilisation",
                            correct=True,
                        ),
                        opt("The colour of the paint and the fence height"),
                        opt("The number of car-park spaces"),
                    ),
                    "Big revenue and variable-cost levers dominate; small fixed "
                    "line items rarely swing the decision.",
                ),
            ),
        ),
        # -- 6. Project management -------------------------------------
        _t(
            "Project management (PMBOK, stage-gate, Agile)",
            "11 min",
            """# Project management (PMBOK, stage-gate, Agile)

A positive NPV is a promise; a **project** is how you keep it. Project
management delivers a defined scope on time and on budget, and the classic
tension is the **triple constraint**: **scope, time and cost** bound
**quality**. Change one and the others move - you cannot add scope for
free.

The **PMBOK** (Project Management Body of Knowledge, from PMI) organises
the work into process groups - **initiating, planning, executing,
monitoring and controlling, and closing** - across knowledge areas like
scope, schedule, cost, risk and quality. A core planning tool is the
**Work Breakdown Structure (WBS)**, which decomposes the project into
deliverables, and the **critical path** through the schedule network sets
the shortest possible duration.

Capital projects in the process industries run on a **stage-gate** (or
phase-gate) process: the project passes through phases - appraise, select,
define, execute, operate (FEL 1 / 2 / 3, front-end loading) - and at each
**gate** management decides go, no-go, or recycle. Spending grows as
uncertainty falls; the gates kill weak projects cheaply, before big money
is committed.

**Agile** delivery - iterative sprints, a prioritised backlog, frequent
working increments - suits software and R and D where requirements evolve.
Physical plant construction is largely predictive/stage-gate, but hybrid
models apply Agile to the digital, control-system and commissioning scopes.

Critical path, worked:

```text
Task network (duration in weeks):
  A Design (6) -> B Procure (10) -> D Install (8) -> E Commission (4)
  A Design (6) -> C Permits (5)  -> D Install (8)

Path 1 A-B-D-E = 6 + 10 + 8 + 4 = 28 weeks  <- critical path (longest)
Path 2 A-C-D-E = 6 +  5 + 8 + 4 = 23 weeks

Project duration = 28 weeks. Slack on Permits (C) = 28 - 23 = 5 weeks.
Delaying any task on the critical path delays the whole project.
```

```mermaid
graph LR
    INIT["Initiate charter"] --> PLAN["Plan scope schedule cost"]
    PLAN --> GATE1{"Stage gate decision"}
    GATE1 -->|"go"| EXEC["Execute build"]
    GATE1 -->|"no go"| STOP["Stop or recycle"]
    EXEC --> MON["Monitor and control"]
    MON --> CLOSE["Close and handover"]
```

Remember: the triple constraint frames the trade-offs, PMBOK gives the
process, stage-gates kill weak projects cheaply, and the critical path
tells you which delays actually matter.
""",
        ),
        quiz_lesson(
            "Quiz: Project management (PMBOK, stage-gate, Agile)",
            (
                q(
                    "What is the 'triple constraint' of project management?",
                    (
                        opt("Design, build, test"),
                        opt(
                            "Scope, time and cost - which together bound quality",
                            correct=True,
                        ),
                        opt("People, process, technology"),
                        opt("Plan, do, check"),
                    ),
                    "Change scope, schedule or budget and the others must move; "
                    "they jointly constrain quality.",
                ),
                q(
                    "What is the purpose of a stage-gate (phase-gate) process?",
                    (
                        opt("To skip planning and start building"),
                        opt(
                            "To review the project at defined gates and decide go, "
                            "no-go or recycle before committing more money",
                            correct=True,
                        ),
                        opt("To fix the product price"),
                        opt("To replace the mass balance"),
                    ),
                    "Gates let management kill weak projects cheaply as spending "
                    "grows and uncertainty falls.",
                ),
                q(
                    "What does the critical path of a schedule represent?",
                    (
                        opt("The cheapest set of tasks"),
                        opt(
                            "The longest chain of dependent tasks, which sets the "
                            "shortest possible project duration",
                            correct=True,
                        ),
                        opt("The tasks with the most slack"),
                        opt("The order tasks were written down"),
                    ),
                    "Delaying any task on the critical path delays the whole "
                    "project; off-path tasks have slack.",
                ),
            ),
        ),
        # -- 7. Operational excellence ---------------------------------
        _t(
            "Operational excellence (Lean, Six Sigma, TPM)",
            "10 min",
            """# Operational excellence (Lean, Six Sigma, TPM)

Once the plant is built and running, the economics depend on running it
**well** - high uptime, low waste, consistent quality. **Operational
excellence** is the discipline of continuous improvement, and three
methodologies dominate.

**Lean** targets **waste** (Japanese *muda*) - the eight wastes are often
remembered as **DOWNTIME**: Defects, Overproduction, Waiting, Non-utilised
talent, Transportation, Inventory, Motion, Excess processing. Lean tools
include value-stream mapping, 5S workplace organisation, and pull/just-in-
time flow. The goal: maximise value to the customer with minimum waste.

**Six Sigma** targets **variation**. Using the **DMAIC** cycle - Define,
Measure, Analyze, Improve, Control - and statistics, it drives defects
toward the six-sigma level of **3.4 defects per million opportunities**.
In a chemical plant that means tighter product spec, less off-spec
material, and fewer trips.

**Total Productive Maintenance (TPM)** targets **equipment
effectiveness**. Its headline metric is **OEE (Overall Equipment
Effectiveness) = Availability * Performance * Quality**. TPM moves from
reactive repair toward planned and operator-led autonomous maintenance so
equipment does not fail unexpectedly.

OEE, worked:

```text
OEE = Availability * Performance * Quality

  Availability = run time / planned time = 20 h / 24 h   = 0.833
  Performance  = actual rate / rated rate = 90 / 100 t/h = 0.900
  Quality      = good units / total units = 950 / 1000   = 0.950

  OEE = 0.833 * 0.900 * 0.950 = 0.712  ->  71 percent

World-class OEE is about 85 percent. The gap (loss) here is dominated by
downtime (availability), so TPM would target unplanned stops first.
```

```mermaid
graph TD
    OPEX2["Operational excellence"] --> LEAN["Lean cut waste"]
    OPEX2 --> SIX["Six Sigma cut variation"]
    OPEX2 --> TPM["TPM equipment uptime"]
    LEAN --> VALUE["More value less muda"]
    SIX --> DMAIC["DMAIC toward 3.4 dpmo"]
    TPM --> OEE["OEE availability performance quality"]
```

Remember: Lean removes waste, Six Sigma removes variation, TPM keeps the
equipment running - and OEE is the number that tells you how much capacity
you are actually capturing.
""",
        ),
        quiz_lesson(
            "Quiz: Operational excellence (Lean, Six Sigma, TPM)",
            (
                q(
                    "What does Lean primarily target?",
                    (
                        opt("Process variation"),
                        opt("Waste (muda) in all its forms", correct=True),
                        opt("Equipment breakdowns only"),
                        opt("The discount rate"),
                    ),
                    "Lean maximises customer value by eliminating the eight wastes "
                    "(DOWNTIME); Six Sigma tackles variation.",
                ),
                q(
                    "What does the Six Sigma DMAIC cycle stand for?",
                    (
                        opt("Design, Make, Assemble, Inspect, Close"),
                        opt(
                            "Define, Measure, Analyze, Improve, Control",
                            correct=True,
                        ),
                        opt("Do, Monitor, Act, Iterate, Confirm"),
                        opt("Deliver, Maintain, Audit, Inspect, Certify"),
                    ),
                    "DMAIC is the data-driven improvement cycle aiming at 3.4 "
                    "defects per million opportunities.",
                ),
                q(
                    "How is Overall Equipment Effectiveness (OEE) calculated?",
                    (
                        opt("Availability plus Performance plus Quality"),
                        opt(
                            "Availability times Performance times Quality",
                            correct=True,
                        ),
                        opt("Run time divided by defects"),
                        opt("Revenue minus operating cost"),
                    ),
                    "OEE multiplies the three loss factors; 0.833 * 0.900 * 0.950 = "
                    "0.71, versus world-class ~0.85.",
                ),
            ),
        ),
        # -- 8. Techno-economic decision-making ------------------------
        _t(
            "Techno-economic decision-making",
            "11 min",
            """# Techno-economic decision-making

The final skill is putting it all together: a **techno-economic
assessment (TEA)** links the *technical* design to the *economic* outcome
so a decision-maker can choose. It is the bridge from a process simulation
to a sanctioned project.

The chain of a TEA:

1. **Process model** - simulate the flowsheet (Aspen Plus, HYSYS, DWSIM)
   to get the mass and energy balances and equipment sizes.
2. **CAPEX** - size and cost the equipment, factor up to total capital.
3. **OPEX** - feed raw-material and utility rates from the balances into
   annual operating cost.
4. **Cash-flow model** - build the year-by-year after-tax cash flow over
   the plant life, including depreciation and working capital.
5. **Metrics** - discount to NPV, solve for IRR, compute payback.
6. **Uncertainty** - sensitivity and Monte Carlo on the key drivers.

A common single-number output is the **minimum selling price** or **levelised
cost** - the product price at which **NPV equals zero** at the hurdle rate.
It answers "what must we sell at to just clear our required return?" and
lets you compare competing technologies on one axis.

Minimum selling price, worked:

```text
Levelised / minimum selling price: solve for price where NPV = 0.

  Annualise CAPEX with the capital recovery factor CRF:
     CRF = i(1+i)^n / ((1+i)^n - 1),  i=0.10, n=15
     CRF = 0.10*1.1^15 / (1.1^15 - 1) = 0.1315
  Annualised capital = 70 MUSD * 0.1315        = 9.20 MUSD/yr
  Annual OPEX                                   = 40.0 MUSD/yr
  Total annual cost                             = 49.2 MUSD/yr
  Annual production                             = 100,000 t/yr

  Minimum selling price = 49.2e6 / 100,000 = 492 USD/t

If the market price exceeds ~492 USD/t, the project clears its hurdle.
```

```mermaid
graph LR
    SIM["Process simulation"] --> CAPEX3["CAPEX estimate"]
    SIM --> OPEX3["OPEX estimate"]
    CAPEX3 --> CF["Cash flow model"]
    OPEX3 --> CF
    CF --> MET["NPV IRR payback"]
    MET --> RISK["Sensitivity and Monte Carlo"]
    RISK --> DEC{"Clears hurdle rate"}
    DEC -->|"yes"| SANC["Sanction and deliver"]
    DEC -->|"no"| REW["Rework or reject"]
```

Remember: a techno-economic assessment turns a flowsheet into a decision -
model the process, cost it, build the cash flow, judge it on NPV and a
minimum selling price, and stress the drivers before you sanction.
""",
        ),
        quiz_lesson(
            "Quiz: Techno-economic decision-making",
            (
                q(
                    "What is the purpose of a techno-economic assessment (TEA)?",
                    (
                        opt("To design the piping isometrics"),
                        opt(
                            "To link the technical process design to the economic "
                            "outcome so a decision can be made",
                            correct=True,
                        ),
                        opt("To schedule operator shifts"),
                        opt("To choose the paint colour"),
                    ),
                    "A TEA is the bridge from simulation (mass/energy balances) to "
                    "CAPEX, OPEX, cash flow and profitability metrics.",
                ),
                q(
                    "What does a 'minimum selling price' (levelised cost) tell you?",
                    (
                        opt("The maximum price the market will ever pay"),
                        opt(
                            "The product price at which NPV equals zero at the "
                            "hurdle rate - the price needed to just clear the "
                            "required return",
                            correct=True,
                        ),
                        opt("The raw-material cost per tonne"),
                        opt("The plant's OEE"),
                    ),
                    "It is the break-even price; compare technologies on one axis "
                    "and against the market price.",
                ),
                q(
                    "What is the correct order of a techno-economic assessment?",
                    (
                        opt("Metrics, then OPEX, then simulation"),
                        opt(
                            "Process model, then CAPEX and OPEX, then cash-flow "
                            "model, then NPV/IRR, then uncertainty",
                            correct=True,
                        ),
                        opt("Payback first, then design the flowsheet"),
                        opt("Monte Carlo before any cost estimate"),
                    ),
                    "Balances feed costs, costs feed the cash flow, the cash flow "
                    "feeds the metrics, and uncertainty stresses the result.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is CAPEX?",
                    (
                        opt("The annual cost of raw materials and utilities"),
                        opt(
                            "The one-time capital cost to design, build and commission the plant",
                            correct=True,
                        ),
                        opt("The discount rate used in NPV"),
                        opt("The product selling price"),
                    ),
                    "CAPEX is the one-off capital investment; OPEX is the recurring "
                    "annual operating cost.",
                ),
                q(
                    "The six-tenths rule scales cost by the capacity ratio raised to about...",
                    (
                        opt("0.1"),
                        opt("0.6", correct=True),
                        opt("1.0"),
                        opt("6.0"),
                    ),
                    "Cost_2 = Cost_1 * (Cap_2/Cap_1)^0.6; the sub-linear exponent is "
                    "economy of scale.",
                ),
                q(
                    "Which OPEX item usually dominates a chemical process?",
                    (
                        opt("Raw materials", correct=True),
                        opt("Insurance"),
                        opt("Property tax"),
                        opt("Paint and signage"),
                    ),
                    "Feedstock cost, set by the mass balance and yield, is normally "
                    "the largest single operating cost.",
                ),
                q(
                    "The present value of a future cash flow F at rate i after n years is...",
                    (
                        opt("F * (1 + i)^n"),
                        opt("F / (1 + i)^n", correct=True),
                        opt("F * i * n"),
                        opt("F + i * n"),
                    ),
                    "Discounting divides by (1+i)^n to bring future money to today.",
                ),
                q(
                    "A project with a positive NPV at the required discount rate...",
                    (
                        opt("should be rejected"),
                        opt("creates value and should be accepted", correct=True),
                        opt("has an IRR of zero"),
                        opt("pays back instantly"),
                    ),
                    "NPV > 0 means the discounted inflows exceed the outflows at "
                    "the required return.",
                ),
                q(
                    "The internal rate of return (IRR) is...",
                    (
                        opt("the average yearly profit"),
                        opt(
                            "the discount rate that makes NPV equal to zero",
                            correct=True,
                        ),
                        opt("the payback period"),
                        opt("the raw-material cost"),
                    ),
                    "Accept when IRR exceeds the hurdle rate; beware multiple IRRs "
                    "with unconventional cash flows.",
                ),
                q(
                    "What does a Monte Carlo economic simulation produce?",
                    (
                        opt("A single guaranteed NPV"),
                        opt(
                            "A distribution of NPV outcomes and the probability of loss",
                            correct=True,
                        ),
                        opt("The exact future product price"),
                        opt("The critical path"),
                    ),
                    "Sampling input distributions gives a spread of NPVs and a "
                    "probability the project loses money.",
                ),
                q(
                    "In project management, what does the critical path determine?",
                    (
                        opt("The cheapest tasks"),
                        opt(
                            "The shortest possible project duration, via the "
                            "longest chain of dependent tasks",
                            correct=True,
                        ),
                        opt("The number of operators"),
                        opt("The discount rate"),
                    ),
                    "Delays on the critical path delay the whole project; off-path "
                    "tasks carry slack.",
                ),
                q(
                    "Overall Equipment Effectiveness (OEE) is the product of...",
                    (
                        opt("scope, time and cost"),
                        opt(
                            "availability, performance and quality",
                            correct=True,
                        ),
                        opt("NPV, IRR and payback"),
                        opt("raw materials, utilities and labour"),
                    ),
                    "OEE = Availability * Performance * Quality; world-class is about 85 percent.",
                ),
                q(
                    "A 'minimum selling price' from a techno-economic assessment "
                    "is the price at which...",
                    (
                        opt("the plant runs at full capacity"),
                        opt(
                            "NPV equals zero at the hurdle rate - the break-even "
                            "price to clear the required return",
                            correct=True,
                        ),
                        opt("OPEX equals CAPEX"),
                        opt("the OEE reaches 100 percent"),
                    ),
                    "It is the levelised break-even price; compare it against the "
                    "market price and competing technologies.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PROCESS_ECONOMICS_MANAGEMENT_COURSES: tuple[SeedCourse, ...] = (_PROCESS_ECONOMICS_MANAGEMENT,)
