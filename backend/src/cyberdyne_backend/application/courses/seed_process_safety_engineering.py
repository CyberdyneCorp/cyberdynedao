"""Academy seed content - Process Safety Engineering.

An advanced course on preventing catastrophic incidents in facilities that
handle hazardous materials and energy. It walks through process safety
management as a system, structured hazard identification with HAZOP,
layers of protection analysis and safety instrumented systems (LOPA and
SIL), fire and explosion hazards (including ATEX area classification),
overpressure protection with relief systems and flares, toxic release and
atmospheric dispersion, and the incident investigation and safety-culture
practices that keep the whole thing honest. Every lesson is a direct
explanation with a worked example and a mermaid diagram, followed by a
checkpoint quiz; the course closes with a comprehensive final quiz.
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


_PROCESS_SAFETY_ENGINEERING = SeedCourse(
    slug="process-safety-engineering",
    title="Process Safety Engineering",
    description=(
        "Preventing catastrophic incidents in plants that handle hazardous "
        "materials and energy: process safety management, hazard "
        "identification and HAZOP, layers of protection analysis, safety "
        "instrumented systems and SIL, fire and explosion and ATEX, relief "
        "systems and flares, toxic release and dispersion, and building a "
        "strong safety culture - with risk matrices, LOPA tables and worked "
        "calculations, plus a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Process Safety Engineering

**Process safety** is the discipline of preventing the low-frequency,
high-consequence events - fires, explosions, and toxic releases - that
can destroy a plant and the community around it. It is different from
**occupational safety** (slips, trips, hand injuries): a facility can have
a spotless personal-injury record and still be one loss-of-containment
away from a disaster. Bhopal, Piper Alpha, Texas City and Buncefield all
happened at sites that thought they were safe.

The approach in this course is **systematic and layered**: identify what
can go wrong, understand how bad and how likely it is, and stack
independent protection layers so that no single failure leads to
catastrophe. Every lesson explains one idea directly, shows it with a
worked example (a risk matrix, a LOPA table, or a design calculation),
and draws it as a diagram. After each lesson there is a short quiz; at the
end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Process safety management** - the system and inherent safety
2. **Hazard identification and HAZOP** - finding what can go wrong
3. **Layers of protection analysis (LOPA)** - is the risk tolerable?
4. **Safety instrumented systems and SIL** - engineered trips that work
5. **Fire, explosion and ATEX** - flammable atmospheres and ignition
6. **Relief systems and flares** - protecting against overpressure
7. **Toxic release and dispersion** - how far the cloud reaches
8. **Incident investigation and safety culture** - learning from failure

This maps directly onto how regulators and standards bodies think - OSHA
PSM, the Seveso Directive, CCPS Risk Based Process Safety, IEC 61511 and
API standards. Knowing where each piece fits makes the specialist topics
far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How does process safety differ from occupational safety?",
                    (
                        opt("They are the same thing measured differently"),
                        opt(
                            "Process safety targets low-frequency high-consequence loss "
                            "of containment (fires, explosions, toxic releases); "
                            "occupational safety targets everyday personal injuries",
                            correct=True,
                        ),
                        opt("Process safety only applies to office buildings"),
                        opt("Occupational safety covers explosions and toxic clouds"),
                    ),
                    "A site can have an excellent personal-injury record and still be "
                    "at high risk of a catastrophic process incident - they are "
                    "measured and managed separately.",
                ),
                q(
                    "What is the core strategy this course teaches for preventing catastrophe?",
                    (
                        opt("Rely on a single very reliable safety device"),
                        opt("Train operators to never make mistakes"),
                        opt(
                            "Identify hazards, quantify how bad and how likely, and stack "
                            "independent protection layers so no single failure is enough",
                            correct=True,
                        ),
                        opt("Keep the plant paperwork up to date"),
                    ),
                    "No single barrier is trusted; independent layers of protection are "
                    "the defining idea of modern process safety.",
                ),
            ),
        ),
        # -- 1. PSM and inherent safety --------------------------------
        _t(
            "Process safety management and inherent safety",
            "11 min",
            """# Process safety management and inherent safety

**Process Safety Management (PSM)** is the management system that keeps
hazardous processes under control over their whole life. It is codified in
**OSHA 29 CFR 1910.119** (US), the **Seveso III Directive** (EU), and the
CCPS **Risk Based Process Safety (RBPS)** framework. Rather than a single
device, PSM is a set of interlocking **elements** - for example: process
safety information, process hazard analysis, operating procedures,
management of change, mechanical integrity, pre-startup safety review,
emergency planning, and incident investigation. A gap in any element
(often **management of change**) shows up again and again in major
accident reports.

The most powerful idea sits underneath PSM: **inherent safety**. Instead
of adding protection to a dangerous process, you make the process **less
dangerous by design** so the hazard is smaller or absent. Trevor Kletz
summed it up: **"What you do not have cannot leak."** The four classic
principles:

- **Minimize** - use smaller inventories of hazardous material (intensify).
- **Substitute** - replace a hazardous material with a safer one.
- **Moderate** - use less hazardous conditions (lower pressure, dilution).
- **Simplify** - remove complexity and error-prone equipment.

There is a **hierarchy of controls**: inherent measures are most reliable
because they cannot be defeated, then passive engineered protection (a
dike, a thicker vessel), then active engineered protection (a trip, a
relief valve), then procedural controls (a checklist), which are weakest
because they depend on people every time.

```mermaid
graph TD
    HAZ["Hazard identified"] --> INH["Inherent - remove or reduce hazard"]
    INH --> PAS["Passive - dike or robust vessel"]
    PAS --> ACT["Active - trips and relief valves"]
    ACT --> PROC["Procedural - checklists and training"]
    INH --> BEST["Most reliable at top"]
    PROC --> WEAK["Weakest at bottom"]
```

A worked judgement of inherent safety, minimizing inventory:

```text
Reactor A: batch stores 20,000 kg of chlorine intermediate on site.
Reactor B: continuous process, holdup 200 kg, made just in time.

Potential release inventory:  A = 20,000 kg   B = 200 kg
Ratio                         A / B = 100x smaller worst case for B

Inherent principle applied: MINIMIZE (intensification).
Design B is inherently safer - the worst credible release is 100x
smaller, so every downstream protection layer has less to contain.
```

Remember: PSM is the system that manages the hazard; inherent safety is
the strategy that shrinks the hazard before any protection is needed.
""",
        ),
        quiz_lesson(
            "Quiz: Process safety management and inherent safety",
            (
                q(
                    "Which best describes Process Safety Management?",
                    (
                        opt("A single relief valve on the main reactor"),
                        opt(
                            "A management system of interlocking elements (hazard "
                            "analysis, management of change, mechanical integrity, and "
                            "more) that controls a hazardous process over its life",
                            correct=True,
                        ),
                        opt("Personal protective equipment for operators"),
                        opt("A one-time inspection before startup only"),
                    ),
                    "PSM (OSHA 1910.119, Seveso, CCPS RBPS) is a lifecycle system of "
                    "elements, not a device or a one-off check.",
                ),
                q(
                    "What is the central idea of inherent safety?",
                    (
                        opt("Add more alarms and interlocks to a dangerous process"),
                        opt("Write more detailed operating procedures"),
                        opt(
                            "Make the process less dangerous by design so the hazard is "
                            "smaller or absent - what you do not have cannot leak",
                            correct=True,
                        ),
                        opt("Buy more insurance for the site"),
                    ),
                    "Inherent safety reduces or removes the hazard itself (minimize, "
                    "substitute, moderate, simplify) rather than adding protection.",
                ),
                q(
                    "In the hierarchy of controls, why is an inherent measure preferred "
                    "over a procedural control?",
                    (
                        opt("It is always cheaper to install"),
                        opt("Procedures are illegal in most plants"),
                        opt(
                            "Inherent measures cannot be defeated or forgotten, while "
                            "procedural controls depend on a person acting correctly "
                            "every single time",
                            correct=True,
                        ),
                        opt("Procedures cannot be written down"),
                    ),
                    "Reliability decreases down the hierarchy: inherent and passive "
                    "measures do not rely on people or active systems working on demand.",
                ),
            ),
        ),
        # -- 2. Hazard ID and HAZOP ------------------------------------
        _t(
            "Hazard identification and HAZOP",
            "12 min",
            """# Hazard identification and HAZOP

You cannot protect against a hazard you have not identified. **Hazard
identification** is the structured search for everything that could go
wrong, and the most widely used technique for continuous and batch
processes is the **HAZOP** (Hazard and Operability study).

A HAZOP is a **team-based, systematic** review of a design, driven by
**guide words** applied to process **parameters** at each **node** (a
section of the P&ID, for example the line into a reactor). The guide word
plus the parameter creates a **deviation**; the team then reasons out
**causes**, **consequences**, existing **safeguards**, and
**recommendations**.

Standard guide words (from IEC 61882) combined with parameters:

```text
Guide word x Parameter  ->  Deviation to explore
------------------------------------------------------------
NO / NONE   + Flow       ->  No feed (pump stopped, valve shut)
MORE        + Pressure   ->  Overpressure (blocked outlet, runaway)
LESS        + Temperature->  Under-cooling / freezing
AS WELL AS  + Composition->  Contaminant or extra phase present
REVERSE     + Flow       ->  Backflow into upstream equipment
OTHER THAN  + Operation  ->  Wrong material charged (maintenance)
```

For each credible deviation the team records a worksheet row. A single
line of a HAZOP worksheet looks like this:

```text
Node: Reactor feed line       Parameter: Flow      Guide word: NO
Deviation:   No flow of coolant to the reactor jacket
Cause:       Coolant pump P-101 trips on power loss
Consequence: Loss of cooling -> exothermic runaway -> overpressure
             -> possible vessel rupture and release
Safeguards:  Low-flow alarm FAL-101; high-temperature trip TSH-102
             closing feed; relief valve PSV-103 to flare
Action:      Confirm PSV-103 sized for runaway case (see relief lesson)
```

HAZOP is powerful because the guide words force the team to consider
deviations no individual would think of alone, and it is **qualitative** -
it finds scenarios but does not by itself decide whether the risk is
tolerable. That is the job of LOPA in the next lesson. Related techniques
include **What-If**, **checklists**, **FMEA** (failure modes and effects),
and **Bow-Tie** analysis for visualizing a top event with its causes and
consequences.

```mermaid
graph LR
    NODE["Select node on the PandID"] --> GW["Apply guide word to parameter"]
    GW --> DEV["Deviation such as no flow"]
    DEV --> CAUSE["Identify causes"]
    CAUSE --> CONS["Assess consequences"]
    CONS --> SAFE["List existing safeguards"]
    SAFE --> ACT["Raise actions where gaps remain"]
    ACT --> NODE
```

Remember: HAZOP systematically turns a P&ID into a list of credible
deviations and their consequences - the raw material every later analysis
depends on.
""",
        ),
        quiz_lesson(
            "Quiz: Hazard identification and HAZOP",
            (
                q(
                    "What drives the systematic search in a HAZOP study?",
                    (
                        opt("A random selection of past incidents"),
                        opt(
                            "Guide words (NO, MORE, LESS, REVERSE, ...) applied to "
                            "process parameters at each node to generate deviations",
                            correct=True,
                        ),
                        opt("The plant manager's intuition alone"),
                        opt("A software model that needs no team"),
                    ),
                    "Guide word plus parameter yields a deviation; the team then works "
                    "out causes, consequences, safeguards and actions.",
                ),
                q(
                    "The guide word REVERSE applied to Flow prompts the team to consider…",
                    (
                        opt("Higher than normal flow"),
                        opt("No flow at all"),
                        opt(
                            "Backflow - fluid flowing in the opposite direction into "
                            "upstream equipment",
                            correct=True,
                        ),
                        opt("A change in fluid composition"),
                    ),
                    "REVERSE + Flow = backflow, which can carry contaminants upstream or "
                    "over-pressure equipment not rated for it.",
                ),
                q(
                    "Why is HAZOP alone not sufficient to decide if a risk is acceptable?",
                    (
                        opt("Because it is fully automated and untrustworthy"),
                        opt(
                            "It is qualitative - it identifies deviations and "
                            "consequences but does not quantify likelihood against a "
                            "tolerable risk target",
                            correct=True,
                        ),
                        opt("Because it ignores safeguards entirely"),
                        opt("Because it can only be used on batch processes"),
                    ),
                    "HAZOP finds the scenarios; a semi-quantitative method like LOPA "
                    "then tests whether protection is enough.",
                ),
            ),
        ),
        # -- 3. LOPA ---------------------------------------------------
        _t(
            "Layers of protection analysis (LOPA)",
            "12 min",
            """# Layers of protection analysis (LOPA)

**LOPA** is a **semi-quantitative** method that takes a single scenario
(usually a serious one flagged by HAZOP) and asks: **is the existing
protection enough, or do we need more?** It is order-of-magnitude
arithmetic, deliberately simple and conservative.

The logic is a chain. An **initiating cause** happens at some frequency
per year. Each **independent protection layer (IPL)** in the path reduces
the frequency by its **probability of failure on demand (PFD)**. Multiply
them together and compare the resulting **mitigated frequency** to your
**tolerable frequency** for that consequence.

An IPL must be **independent** of the initiating cause and of the other
layers, **effective** at preventing the consequence, and **auditable**.
Typical IPLs and credited PFDs:

```text
Layer                                   Typical PFD    Risk reduction
--------------------------------------------------------------------
Basic Process Control System (as IPL)   1e-1           10x
Operator response to an alarm           1e-1           10x
Relief valve (well maintained)          1e-2           100x
Safety Instrumented Function - SIL 1    1e-1 to 1e-2   10x to 100x
Safety Instrumented Function - SIL 2    1e-2 to 1e-3   100x to 1000x
```

A worked LOPA for the runaway scenario from the HAZOP lesson:

```text
Scenario:  Loss of cooling -> reactor runaway -> vessel rupture, release
Tolerable frequency for this consequence:  1e-5 per year (1 in 100,000 yr)

Initiating cause: coolant pump trips           f = 1e-1 /yr
IPL 1  High-temperature alarm + operator       PFD = 1e-1
IPL 2  Relief valve PSV-103 to flare           PFD = 1e-2

Mitigated frequency = f * PFD1 * PFD2
                    = 1e-1 * 1e-1 * 1e-2
                    = 1e-4 per year

Compare:  1e-4 (achieved)  vs  1e-5 (tolerable)
Gap = factor of 10 too frequent  ->  need ONE more IPL giving 10x

Decision: add a Safety Instrumented Function (SIF).
Required SIF risk reduction >= 10x  ->  PFD <= 1e-1  ->  SIL 1.
```

That last line is the crucial handoff: **LOPA sizes the safety
instrumented function**. The risk-reduction gap becomes the required PFD,
which becomes the **SIL target** for the SIS in the next lesson.

```mermaid
graph LR
    IC["Initiating cause frequency"] --> L1["IPL 1 reduces by its PFD"]
    L1 --> L2["IPL 2 reduces by its PFD"]
    L2 --> MIT["Mitigated frequency"]
    MIT --> CMP{"Below tolerable frequency"}
    CMP -->|"yes"| OK["Protection adequate"]
    CMP -->|"no"| ADD["Add an independent layer or SIF"]
```

Remember: LOPA multiplies an initiating frequency by the PFD of each
independent layer, compares to a tolerable target, and turns any shortfall
into a required risk reduction - the SIL target for an engineered trip.
""",
        ),
        quiz_lesson(
            "Quiz: Layers of protection analysis (LOPA)",
            (
                q(
                    "How does LOPA arrive at a mitigated event frequency?",
                    (
                        opt("It adds up the PFDs of every safeguard"),
                        opt(
                            "It multiplies the initiating cause frequency by the "
                            "probability of failure on demand (PFD) of each independent "
                            "protection layer",
                            correct=True,
                        ),
                        opt("It takes the largest single PFD only"),
                        opt("It ignores the initiating frequency"),
                    ),
                    "Mitigated frequency = initiating frequency times the product of "
                    "the IPL PFDs; compare that to the tolerable frequency. "
                    "Order-of-magnitude multiplication is the whole method.",
                ),
                q(
                    "Which is a required property of an Independent Protection Layer?",
                    (
                        opt("It must share components with the initiating cause"),
                        opt("It must be operated by the same control loop that failed"),
                        opt(
                            "It must be independent of the initiating cause and other "
                            "layers, effective, and auditable",
                            correct=True,
                        ),
                        opt("It must be procedural rather than engineered"),
                    ),
                    "Independence is what lets you multiply PFDs; a layer that shares a "
                    "failure with another cannot be credited separately.",
                ),
                q(
                    "In the worked example the mitigated frequency was 1e-4/yr against a "
                    "tolerable 1e-5/yr. What does LOPA conclude?",
                    (
                        opt("The risk is already tolerable, do nothing"),
                        opt(
                            "There is a 10x shortfall, so add one more IPL giving at "
                            "least 10x reduction - here a SIL 1 safety function",
                            correct=True,
                        ),
                        opt("Remove the relief valve to simplify"),
                        opt("The plant must be shut down permanently"),
                    ),
                    "The factor-of-10 gap becomes the required risk reduction, which "
                    "sets the SIL target for the new safety instrumented function.",
                ),
            ),
        ),
        # -- 4. SIS and SIL --------------------------------------------
        _t(
            "Safety instrumented systems and SIL",
            "12 min",
            """# Safety instrumented systems and SIL

When LOPA says an independent, engineered trip is needed, that trip is a
**Safety Instrumented Function (SIF)**, implemented by a **Safety
Instrumented System (SIS)** and governed by **IEC 61511** (process
industry) and **IEC 61508** (the underlying standard). A SIF is a complete
loop: **sensor -> logic solver -> final element**, for example a
high-pressure transmitter, a safety PLC, and a shutdown valve that isolates
the feed.

Critically, the **SIS is separate from the Basic Process Control System
(BPCS)**. The BPCS runs the plant day to day; the SIS does nothing until a
demand occurs, then acts to bring the process to a **safe state**. Keeping
them separate preserves independence - a failure of the control system
that causes the upset cannot also disable the protection.

**Safety Integrity Level (SIL)** measures how reliable the SIF is, defined
by its **average Probability of Failure on Demand (PFDavg)** for a
low-demand function:

```text
SIL   PFDavg (per demand)      Risk Reduction Factor (RRF = 1/PFDavg)
---------------------------------------------------------------------
 1    1e-1  to 1e-2            10   to 100
 2    1e-2  to 1e-3            100  to 1000
 3    1e-3  to 1e-4            1000 to 10000
 4    1e-4  to 1e-5            10000 to 100000
```

The SIL target comes straight from LOPA: the required risk reduction is
the RRF, and 1/RRF is the PFDavg the loop must achieve. You then verify
the design meets it. A simplified PFDavg for a single (1oo1) subsystem
with a periodic proof test:

```python
# Simplified low-demand PFDavg for one element (1oo1)
# lambda_du = dangerous-undetected failure rate (per hour)
# TI        = proof-test interval (hours)
lambda_du = 5e-7          # per hour (from reliability data)
TI = 8760                 # test once per year, in hours

pfd_avg = lambda_du * TI / 2      # = 0.5 * lambda * TI
rrf = 1 / pfd_avg

print(round(pfd_avg, 5))   # -> 0.00219  (about 2.2e-3)
print(round(rrf))          # -> 457       -> meets SIL 2 (100-1000)
```

Two levers raise SIL: **better components** (lower dangerous failure rate),
**more frequent proof testing** (smaller TI), and **redundant voting**
architectures such as **1oo2** (either of two trips) for availability or
**2oo3** (two of three agree) to tolerate a single failure without spurious
trips. Every SIF also has a defined **proof-test interval** and must be
tested end to end, or its real PFD drifts far above the design value.

```mermaid
graph LR
    SENS["Sensor - pressure transmitter"] --> LOGIC["Logic solver - safety PLC"]
    LOGIC --> FE["Final element - shutdown valve"]
    FE --> SAFE["Process driven to safe state"]
    LOPA["LOPA sets required RRF"] --> SIL["SIL target"]
    SIL --> VER["Verify PFDavg by design and testing"]
```

Remember: a SIF is a sensor-logic-final-element loop, kept independent of
the BPCS; SIL is its reliability tier set by the required risk reduction
and verified through low failure rates, redundancy, and proof testing.
""",
        ),
        quiz_lesson(
            "Quiz: Safety instrumented systems and SIL",
            (
                q(
                    "What are the three parts of a Safety Instrumented Function loop?",
                    (
                        opt("Operator, procedure, and alarm"),
                        opt(
                            "Sensor, logic solver, and final element (for example "
                            "transmitter, safety PLC, and shutdown valve)",
                            correct=True,
                        ),
                        opt("Relief valve, dike, and flare"),
                        opt("Pump, heat exchanger, and reactor"),
                    ),
                    "A SIF senses the demand, decides, and acts on a final element to "
                    "reach a safe state.",
                ),
                q(
                    "Why must the Safety Instrumented System be independent of the BPCS?",
                    (
                        opt("To reduce the cost of instrumentation"),
                        opt("Because IEC 61511 forbids using any PLCs"),
                        opt(
                            "So a control-system failure that causes the upset cannot "
                            "also disable the protection - preserving independence",
                            correct=True,
                        ),
                        opt("So operators cannot see the alarms"),
                    ),
                    "Shared equipment would mean one failure defeats both control and "
                    "protection, breaking the LOPA independence assumption.",
                ),
                q(
                    "A SIF must achieve a PFDavg of about 2e-3 (RRF around 500). Which "
                    "SIL does that meet?",
                    (
                        opt("SIL 1"),
                        opt("SIL 2", correct=True),
                        opt("SIL 3"),
                        opt("SIL 4"),
                    ),
                    "PFDavg of 1e-2 to 1e-3 (RRF 100 to 1000) is SIL 2; 2e-3 with RRF "
                    "about 500 sits squarely in that band.",
                ),
            ),
        ),
        # -- 5. Fire, explosion and ATEX ------------------------------
        _t(
            "Fire, explosion and ATEX",
            "12 min",
            """# Fire, explosion and ATEX

Most catastrophic energy releases come from **fire and explosion**. The
starting point is the **fire triangle**: **fuel + oxidizer + ignition**.
Remove any side and combustion cannot occur - the basis of both prevention
(exclude ignition, inert with nitrogen) and firefighting.

A flammable gas or vapor only burns within its **flammable range**,
between the **Lower Flammable Limit (LFL)** and **Upper Flammable Limit
(UFL)** in air. Below the LFL the mixture is too lean, above the UFL too
rich. The most dangerous cloud sits between them.

Key fire and explosion phenomena:

- **Pool fire / jet fire** - burning liquid pool or pressurized leak; heat
  radiation can escalate to nearby equipment (a **domino** effect).
- **Flash fire** - a flammable cloud ignites and burns back to the source
  with little overpressure.
- **VCE (vapor cloud explosion)** - a large congested cloud ignites and
  the flame accelerates, producing damaging **overpressure** (Buncefield,
  Flixborough).
- **BLEVE** - a pressure vessel of liquid above its atmospheric boiling
  point fails in a fire; the flashing liquid produces a huge fireball.
- **Dust explosion** - combustible dust (flour, sugar, metals) suspended
  in air; needs the fire triangle **plus** confinement and dispersion (the
  **dust pentagon**).

Where a flammable atmosphere may occur, electrical and mechanical ignition
sources must be controlled. This is **hazardous area classification**,
governed in Europe by the **ATEX** directives and internationally by **IEC
60079**. Areas are divided into **zones** by how often a flammable
atmosphere is present, and only suitably certified equipment is allowed:

```text
Gas/vapor zones (IEC 60079 / ATEX)
-----------------------------------------------------------
Zone 0  Explosive atmosphere present continuously or long periods
Zone 1  Likely to occur in normal operation occasionally
Zone 2  Not likely in normal operation; only briefly if it does
(Dust equivalents: Zone 20 / 21 / 22)

Equipment must carry an Ex marking suited to the zone, e.g.
  Ex db IIB T3 Gb  -> flameproof enclosure, gas group IIB,
                      max surface temp class T3 (<= 200 C)
```

A quick worked check - is a leak concentration flammable?

```text
Methane in air:  LFL = 5 percent vol,  UFL = 15 percent vol
Measured concentration near a flange leak = 8 percent vol

5 < 8 < 15   ->  inside the flammable range: IGNITABLE.
Action: eliminate ignition sources, ventilate/disperse, isolate leak.
```

```mermaid
graph TD
    FUEL["Fuel - flammable vapor"] --> TRI["Fire triangle"]
    OXY["Oxidizer - air"] --> TRI
    IGN["Ignition source"] --> TRI
    TRI --> RANGE{"Concentration between LFL and UFL"}
    RANGE -->|"yes"| BURN["Fire or explosion possible"]
    RANGE -->|"no"| SAFE["Too lean or too rich to burn"]
    BURN --> ATEX["Control ignition by ATEX zoning"]
```

Remember: combustion needs fuel, oxidizer and ignition together, only
within the LFL-to-UFL range; ATEX and IEC 60079 zone classification keeps
certified-only ignition sources out of places where flammable atmospheres
can form.
""",
        ),
        quiz_lesson(
            "Quiz: Fire, explosion and ATEX",
            (
                q(
                    "A vapor concentration is above its Upper Flammable Limit (UFL). "
                    "Can it burn as a premixed flame in air?",
                    (
                        opt("Yes, richer is always more flammable"),
                        opt(
                            "No - above the UFL the mixture is too rich (too little "
                            "oxygen) to propagate a flame, though it can become "
                            "flammable if diluted back into range",
                            correct=True,
                        ),
                        opt("Only if the pressure is below atmospheric"),
                        opt("Only inside a Zone 2 area"),
                    ),
                    "Flammability exists only between the LFL and UFL; too lean or too "
                    "rich will not propagate, but dilution of a rich cloud is dangerous.",
                ),
                q(
                    "What distinguishes a BLEVE from a simple pool fire?",
                    (
                        opt("A BLEVE produces no heat"),
                        opt(
                            "A BLEVE is the catastrophic failure of a pressurized vessel "
                            "of liquid above its atmospheric boiling point, flashing to a "
                            "large fireball, often triggered by an engulfing fire",
                            correct=True,
                        ),
                        opt("A BLEVE only happens with non-flammable liquids"),
                        opt("A pool fire always causes more overpressure"),
                    ),
                    "BLEVE = Boiling Liquid Expanding Vapor Explosion: sudden vessel "
                    "rupture and flashing produce a fireball and blast.",
                ),
                q(
                    "What does ATEX / IEC 60079 hazardous area zoning determine?",
                    (
                        opt("The colour the pipes must be painted"),
                        opt("The maximum number of operators on site"),
                        opt(
                            "How often a flammable atmosphere is expected in a location "
                            "(Zone 0/1/2), which sets the ignition-protection rating of "
                            "equipment allowed there",
                            correct=True,
                        ),
                        opt("The tolerable financial loss from a fire"),
                    ),
                    "Zones classify likelihood of a flammable atmosphere; only "
                    "certified Ex equipment suited to the zone may be installed.",
                ),
            ),
        ),
        # -- 6. Relief systems and flares ------------------------------
        _t(
            "Relief systems and flares",
            "12 min",
            """# Relief systems and flares

No matter how good the controls, equipment can still be **over-pressured** -
by a blocked outlet, external fire, thermal expansion, a control failure,
or a runaway reaction. The last line of defence for the equipment itself
is the **pressure relief system**, designed to **API 520/521** and built
to the **ASME Boiler and Pressure Vessel Code (BPVC) Section VIII**.

A **pressure relief valve (PRV/PSV)** is a self-actuated device that opens
when pressure reaches the **set pressure** and recloses when it falls,
venting excess material to a safe location. Two broad types:

- **Conventional / balanced-bellows spring PRV** - opens proportionally;
  the workhorse for most services.
- **Rupture disc** - a one-shot bursting membrane, used for fast pressure
  rise, very corrosive service, or upstream of a PRV to protect it.

Relief sizing is a two-step process: determine the **worst-case relieving
scenario** (the governing case sets the required rate) then size the
orifice for it. The classic fire-case heat input uses the **API 521**
formula:

```text
API 521 fire case (adequate drainage, prompt firefighting):
    Q = 21000 * F * A^0.82        [Q in BTU/hr, A = wetted area, ft2]
    F = environment factor (1.0 bare vessel)

Required vapor relief rate:   W = Q / h_fg    [mass/time]
    h_fg = latent heat of vaporization of the relieving fluid

Then size the orifice area with the API 520 vapor equation and pick the
next-larger standard orifice (D, E, F ... T letter designations).
```

A worked required-rate example:

```text
Fire-exposed vessel:  wetted area A = 300 ft2,  F = 1.0
Q = 21000 * 1.0 * 300^0.82
  = 21000 * 111.5  =  2.34e6 BTU/hr

Relieving fluid latent heat  h_fg = 150 BTU/lb
Required relief rate W = 2.34e6 / 150 = 15,600 lb/hr of vapor
-> size the PSV orifice for >= 15,600 lb/hr, round up to standard orifice.
```

The PRV has to discharge somewhere. Hydrocarbons and toxics are routed
through a **relief header** to a **flare**, which burns the released gas so
it leaves as mostly CO2 and water instead of a flammable or toxic cloud. A
flare needs a **knockout drum** (removes liquid so you do not rain burning
droplets), a reliable **pilot and ignition**, **purge gas** to keep air
out of the header (preventing an explosive mixture), and often a **steam or
air assist** for smokeless combustion.

```mermaid
graph LR
    OP["Overpressure scenario"] --> PSV["Relief valve lifts at set pressure"]
    PSV --> HDR["Relief header"]
    HDR --> KO["Knockout drum removes liquid"]
    KO --> FLR["Flare stack"]
    FLR --> BURN["Burns gas to CO2 and water"]
    PURGE["Purge gas keeps air out"] --> HDR
```

Remember: relief valves protect the equipment by venting overpressure for
the worst credible scenario (often fire), sized to API 520/521 and ASME
VIII; the flare then safely destroys what is vented, with a knockout drum,
purge and reliable ignition making that disposal safe.
""",
        ),
        quiz_lesson(
            "Quiz: Relief systems and flares",
            (
                q(
                    "What is the purpose of a pressure relief valve in a process plant?",
                    (
                        opt("To control the normal operating flow rate"),
                        opt(
                            "To open at a set pressure and vent excess material to a safe "
                            "location, protecting equipment from overpressure failure",
                            correct=True,
                        ),
                        opt("To measure the temperature of the vessel"),
                        opt("To ignite the flare pilot"),
                    ),
                    "A PRV/PSV is the last line of defence for the equipment, sized to "
                    "API 520/521 for the worst credible overpressure scenario.",
                ),
                q(
                    "When sizing relief, why do you first find the governing scenario?",
                    (
                        opt("Because every scenario needs the same orifice"),
                        opt(
                            "Because the worst-case relieving rate (for example the "
                            "external fire case) determines the required orifice size",
                            correct=True,
                        ),
                        opt("To decide the paint colour of the valve"),
                        opt("Scenarios are irrelevant to sizing"),
                    ),
                    "Different upsets give different required rates; you size for the "
                    "largest credible one, commonly the API 521 fire case.",
                ),
                q(
                    "Why does a flare system need a knockout drum and continuous purge gas?",
                    (
                        opt("To cool the gas below its freezing point"),
                        opt(
                            "The knockout drum removes liquid so burning droplets do not "
                            "rain out, and purge gas keeps air out of the header to "
                            "prevent an explosive mixture",
                            correct=True,
                        ),
                        opt("To increase the pressure in the relief header"),
                        opt("They are decorative and not required"),
                    ),
                    "Safe flaring needs liquid removal, a reliable pilot, and purge to "
                    "exclude air from forming a flammable mix inside the header.",
                ),
            ),
        ),
        # -- 7. Toxic release and dispersion ---------------------------
        _t(
            "Toxic release and dispersion",
            "12 min",
            """# Toxic release and dispersion

Not every loss of containment burns; some releases are **toxic**, and the
harm depends on **how far the cloud travels** and **at what
concentration**. Consequence modelling has two stages: the **source term**
(how much, how fast, in what phase the material escapes) and the
**dispersion** (how the cloud spreads and dilutes downwind).

For a gas escaping through a hole, the **source term** is often a choked
(sonic) or subsonic orifice flow. Once airborne, the material dilutes.
Neutrally buoyant gases follow the classic **Gaussian plume model**;
denser-than-air gases (chlorine, propane) first slump and spread as a
**dense gas** before diluting - specialist tools like **PHAST, SLAB, or
ALOHA** handle this.

The centreline concentration of a continuous, ground-level Gaussian plume:

```text
Gaussian plume, continuous ground-level release, downwind centreline:

              Q
 C(x) = -----------------
         pi * u * sy * sz

 C  = concentration            Q  = release rate (mass/time)
 u  = wind speed               sy, sz = dispersion coefficients (grow
                                        with distance x; depend on
                                        Pasquill stability class A-F)
```

Atmospheric **stability class** matters enormously: a stable night (class
F, light wind) keeps a cloud tight and concentrated so it reaches far;
an unstable sunny day (class A) mixes it quickly. A worked estimate:

```python
import math

Q  = 0.05      # kg/s of toxic gas released
u  = 2.0       # m/s wind speed (light)
# dispersion coeffs at x = 500 m, stability class F (stable, worst case)
sy = 12.0      # m
sz = 6.5       # m

C = Q / (math.pi * u * sy * sz)   # kg/m3 on the centreline
print(round(C * 1e6, 1), "mg/m3") # -> 102.0 mg/m3 at 500 m
```

You then compare the predicted concentration and exposure duration against
**toxic endpoints**: **ERPG** (Emergency Response Planning Guidelines),
**AEGL** (Acute Exposure Guideline Levels), or **IDLH** (Immediately
Dangerous to Life or Health). If the distance to a harmful endpoint reaches
occupied areas, you must reduce the source (inherent safety), add
detection and isolation, or improve emergency response and land-use
planning around the site.

```mermaid
graph LR
    REL["Loss of containment"] --> SRC["Source term - rate and phase"]
    SRC --> DENSE{"Denser than air"}
    DENSE -->|"yes"| SLUMP["Dense gas slumps then dilutes"]
    DENSE -->|"no"| GAUSS["Gaussian plume dilutes downwind"]
    SLUMP --> CONC["Concentration versus distance"]
    GAUSS --> CONC
    CONC --> END["Compare to ERPG or AEGL or IDLH"]
```

Remember: model the source term, then disperse it with the right model for
the gas density and atmospheric stability, and compare the downwind
concentration to toxic endpoints to see whether people could be harmed and
how far the effect reaches.
""",
        ),
        quiz_lesson(
            "Quiz: Toxic release and dispersion",
            (
                q(
                    "What are the two stages of modelling a toxic release consequence?",
                    (
                        opt("Ignition and combustion"),
                        opt(
                            "The source term (how much escapes and how) and the "
                            "dispersion (how the cloud spreads and dilutes downwind)",
                            correct=True,
                        ),
                        opt("Relief sizing and flare design"),
                        opt("HAZOP and LOPA"),
                    ),
                    "First quantify the release, then predict where it goes and at what "
                    "concentration.",
                ),
                q(
                    "Why does a stable atmosphere (Pasquill class F, light wind) often "
                    "give the worst toxic reach?",
                    (
                        opt("It disperses the cloud instantly"),
                        opt(
                            "Little vertical mixing keeps the cloud tight and "
                            "concentrated, so harmful concentrations extend farther "
                            "downwind",
                            correct=True,
                        ),
                        opt("It converts the gas to a liquid"),
                        opt("It always ignites the cloud"),
                    ),
                    "Stable, low-wind conditions minimize dilution; unstable sunny "
                    "conditions (class A) mix and dilute the cloud quickly.",
                ),
                q(
                    "What are ERPG, AEGL and IDLH used for in dispersion analysis?",
                    (
                        opt("They are wind-speed categories"),
                        opt("They are types of relief valve"),
                        opt(
                            "They are toxic exposure endpoints - concentration and "
                            "duration thresholds you compare the predicted cloud against "
                            "to judge harm",
                            correct=True,
                        ),
                        opt("They are flare emission standards"),
                    ),
                    "These benchmarks define concentrations at which health effects "
                    "occur, setting the distance to a harmful endpoint.",
                ),
            ),
        ),
        # -- 8. Incident investigation and safety culture --------------
        _t(
            "Incident investigation and safety culture",
            "11 min",
            """# Incident investigation and safety culture

Even the best-designed plant relies on people and organizations behaving
well over years. The final pillar of process safety is **learning from what
goes wrong** and sustaining a **safety culture** that keeps the earlier
layers real rather than paper.

**Incident investigation** looks past the immediate trigger to the **root
causes**. Structured methods - the **5 Whys**, **fault trees**, **causal
factor charts**, and formal systems like **TapRooT** - move from the
surface event down to systemic and management causes. James Reason's
**Swiss cheese model** captures why big accidents are rare but severe: many
layers of defence each have holes (latent weaknesses), and disaster occurs
only when the holes line up.

A worked 5 Whys on the runaway scenario from earlier lessons:

```text
Event: Reactor over-pressured and relieved to flare during a power dip.

Why 1  Coolant pump stopped        -> because site power dipped
Why 2  No backup cooling started   -> because the auto-start was disabled
Why 3  Auto-start was disabled     -> left off after maintenance last month
Why 4  Nobody caught it            -> the change bypassed Management of Change
Why 5  MoC was bypassed            -> MoC seen as slow; no enforcement/audit

Root cause: weak Management of Change process and safety culture,
NOT "the pump tripped." Fix the system, not just the pump.
```

Notice the root cause is a **management-system and culture** failure - the
same pattern found in Bhopal, Piper Alpha, Texas City and Deepwater
Horizon. That is why culture is treated as engineering, not soft skills:

- **Leadership commitment** - management demonstrably prioritizes safety
  over short-term output, and resources it.
- **A reporting and just culture** - people report near-misses and errors
  without fear; blame is reserved for recklessness, not honest mistakes.
- **Learning culture** - the organization acts on what incidents and
  audits reveal, and closes the loop.
- **Leading vs lagging indicators** - do not wait for injuries (lagging);
  track leading indicators (overdue PSV tests, bypassed interlocks,
  overdue actions) that predict trouble.

This closes the loop back to Lesson 1: investigations feed the PSM
elements, drive inherent-safety improvements, and refresh the HAZOP and
LOPA - so the whole system keeps getting safer.

```mermaid
graph LR
    INC["Incident or near miss"] --> RCA["Root cause analysis"]
    RCA --> SYS["Find system and culture causes"]
    SYS --> ACT["Corrective actions"]
    ACT --> LEARN["Share lessons across sites"]
    LEARN --> PSM["Feed back into PSM and HAZOP"]
    PSM --> IND["Track leading indicators"]
    IND --> INC
```

Remember: investigate to the systemic root cause, not the last domino;
sustain a just, learning safety culture led from the top and steered by
leading indicators - that is what keeps every earlier protection layer
trustworthy.
""",
        ),
        quiz_lesson(
            "Quiz: Incident investigation and safety culture",
            (
                q(
                    "What is the goal of a proper incident investigation?",
                    (
                        opt("To identify which operator to discipline"),
                        opt(
                            "To find the underlying systemic and management root causes, "
                            "not just the immediate trigger, so the system can be fixed",
                            correct=True,
                        ),
                        opt("To close the case as quickly as possible"),
                        opt("To prove the equipment was faulty"),
                    ),
                    "Techniques like 5 Whys and fault trees drive past the trigger to "
                    "root causes; major accidents almost always trace to system and "
                    "culture failures.",
                ),
                q(
                    "What does James Reason's Swiss cheese model illustrate?",
                    (
                        opt("That one perfect barrier is enough"),
                        opt(
                            "That defences have latent holes, and an accident happens "
                            "only when holes in multiple layers line up",
                            correct=True,
                        ),
                        opt("That cheese should not be stored near reactors"),
                        opt("That procedures are always the strongest layer"),
                    ),
                    "It explains why layered defences work most of the time yet fail "
                    "catastrophically when weaknesses align - reinforcing the value of "
                    "independent layers.",
                ),
                q(
                    "Why track leading indicators rather than only lagging ones?",
                    (
                        opt("Leading indicators are cheaper to ignore"),
                        opt("Lagging indicators are illegal to record"),
                        opt(
                            "Leading indicators (overdue PSV tests, bypassed interlocks) "
                            "predict trouble before harm occurs, whereas lagging "
                            "indicators only count harm after the fact",
                            correct=True,
                        ),
                        opt("They are the same measurement"),
                    ),
                    "Waiting for injuries or releases is too late; leading indicators "
                    "warn while there is still time to act.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What primarily distinguishes process safety from occupational safety?",
                    (
                        opt("Process safety is only about paperwork"),
                        opt(
                            "Process safety prevents low-frequency high-consequence loss "
                            "of containment (fires, explosions, toxic releases), not "
                            "everyday personal injuries",
                            correct=True,
                        ),
                        opt("Occupational safety covers reactor runaways"),
                        opt("There is no real difference"),
                    ),
                    "A clean injury record does not mean the catastrophic risk is "
                    "controlled - they are managed separately.",
                ),
                q(
                    "Which is the most reliable place to control a hazard in the "
                    "hierarchy of controls?",
                    (
                        opt("A procedural checklist"),
                        opt("An active engineered trip"),
                        opt(
                            "An inherent measure that removes or reduces the hazard by "
                            "design, since it cannot be defeated or forgotten",
                            correct=True,
                        ),
                        opt("Extra personal protective equipment"),
                    ),
                    "Inherent and passive measures sit at the top; procedures depend on "
                    "people every time and are weakest.",
                ),
                q(
                    "In a HAZOP, the guide word MORE applied to Pressure prompts the "
                    "team to consider…",
                    (
                        opt("Loss of feed to the unit"),
                        opt("A contaminant in the stream"),
                        opt(
                            "Overpressure - for example a blocked outlet or a runaway "
                            "raising pressure beyond the design limit",
                            correct=True,
                        ),
                        opt("Backflow into upstream equipment"),
                    ),
                    "MORE + Pressure = overpressure deviation; the team then works out "
                    "causes, consequences and safeguards.",
                ),
                q(
                    "How does LOPA compute whether protection is adequate?",
                    (
                        opt("It sums the consequences in dollars"),
                        opt(
                            "It multiplies the initiating cause frequency by each "
                            "independent layer's PFD and compares the result to a "
                            "tolerable frequency",
                            correct=True,
                        ),
                        opt("It counts the number of valves on the P&ID"),
                        opt("It uses the single worst PFD only"),
                    ),
                    "Any shortfall becomes the required risk reduction, which sets the "
                    "SIL target for a safety instrumented function. The gap between "
                    "achieved and tolerable frequency drives the design.",
                ),
                q(
                    "A safety instrumented function must achieve PFDavg of 1e-3 to 1e-4 "
                    "(RRF 1000 to 10000). What SIL is that?",
                    (
                        opt("SIL 1"),
                        opt("SIL 2"),
                        opt("SIL 3", correct=True),
                        opt("SIL 4"),
                    ),
                    "PFDavg 1e-3 to 1e-4 corresponds to SIL 3; SIL rises as PFDavg falls "
                    "and risk reduction increases.",
                ),
                q(
                    "A flammable vapor concentration must be where, to ignite as a "
                    "premixed flame in air?",
                    (
                        opt("Below the Lower Flammable Limit"),
                        opt("Above the Upper Flammable Limit"),
                        opt(
                            "Between the Lower and Upper Flammable Limits - too lean or "
                            "too rich will not propagate",
                            correct=True,
                        ),
                        opt("At exactly atmospheric pressure only"),
                    ),
                    "Only the LFL-to-UFL range is flammable; ATEX zoning keeps ignition "
                    "sources out of areas where such a cloud can form.",
                ),
                q(
                    "What determines the required orifice size of a pressure relief valve?",
                    (
                        opt("The colour of the process fluid"),
                        opt(
                            "The worst credible relieving scenario (often the external "
                            "fire case), which sets the required relief rate per API "
                            "520/521",
                            correct=True,
                        ),
                        opt("The number of operators on shift"),
                        opt("The length of the flare header only"),
                    ),
                    "You find the governing scenario, compute the required rate, then "
                    "size the orifice to ASME VIII and API standards.",
                ),
                q(
                    "Why is a knockout drum placed before a flare stack?",
                    (
                        opt("To increase the flare's smoke output"),
                        opt(
                            "To remove liquid from the relief stream so burning droplets "
                            "do not rain out of the flare",
                            correct=True,
                        ),
                        opt("To store the relieved gas permanently"),
                        opt("To measure the wind speed"),
                    ),
                    "Liquid carryover to a flare produces burning rain; the knockout "
                    "drum separates it, alongside purge gas and reliable ignition.",
                ),
                q(
                    "In Gaussian dispersion, why is a stable low-wind night often the "
                    "worst case for a toxic release?",
                    (
                        opt("The gas cannot disperse at night ever"),
                        opt(
                            "Little atmospheric mixing keeps the cloud concentrated, so "
                            "harmful concentrations reach farther downwind",
                            correct=True,
                        ),
                        opt("Wind speed does not affect concentration"),
                        opt("Stable air always ignites the cloud"),
                    ),
                    "Pasquill class F with light wind minimizes dilution; the distance "
                    "to a toxic endpoint (ERPG/AEGL/IDLH) is greatest.",
                ),
                q(
                    "Investigations of Bhopal, Piper Alpha and Texas City most often "
                    "trace the root cause to…",
                    (
                        opt("A single mechanical part that could not be improved"),
                        opt("Bad luck with no preventable cause"),
                        opt(
                            "Failures of management systems and safety culture (such as "
                            "weak management of change), not just the last technical "
                            "trigger",
                            correct=True,
                        ),
                        opt("Operators who were simply careless"),
                    ),
                    "The Swiss cheese pattern of aligned latent weaknesses is why "
                    "safety culture and management systems are treated as core "
                    "engineering, and why leading indicators are tracked.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PROCESS_SAFETY_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_PROCESS_SAFETY_ENGINEERING,)
