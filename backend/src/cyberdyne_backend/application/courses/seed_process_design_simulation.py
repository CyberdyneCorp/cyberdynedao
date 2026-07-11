"""Academy seed content - Process Design and Simulation.

Turning chemistry into a working plant: how a process moves from a block
flow idea to flowsheets and P&IDs, how steady-state simulators (Aspen
Plus, HYSYS, DWSIM) close mass and energy balances, how to pick the right
thermodynamic method, heat integration and pinch analysis, the link to
process economics, dynamic simulation, and digital twins. Every lesson is
a direct explanation with a worked example - a flowsheet, a spec table, or
a calculation - and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz.
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


_PROCESS_DESIGN_SIMULATION = SeedCourse(
    slug="process-design-simulation",
    title="Process Design & Simulation",
    description=(
        "Turning chemistry into a plant: flowsheets and P&IDs, steady-state "
        "and dynamic simulation in Aspen Plus, HYSYS and DWSIM, thermodynamic "
        "method selection, heat integration and pinch analysis, the link to "
        "process economics, and digital twins - with a worked example and a "
        "diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Process Design and Simulation

A reaction that works in a flask is not yet a process. Turning chemistry
into a **plant** means deciding what equipment to use, in what order, at
what temperature and pressure, closing every mass and energy balance, and
proving the economics - all before steel is cut. Modern process engineers
do this on a **process simulator**: a piece of software that solves the
whole flowsheet against rigorous thermodynamics.

This course is the bridge from chemistry to engineering. It is **direct
and worked**: every lesson explains one idea, shows it in a concrete
example (a flowsheet, a spec table, or a calculation you can follow), and
draws it as a diagram. After each lesson there is a short quiz; a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **The process design workflow** - from concept to detailed design
2. **Flowsheets and P&IDs** - the drawings that define a process
3. **Steady-state simulation** - Aspen Plus, HYSYS, DWSIM
4. **Thermodynamic method selection** - the single most important choice
5. **Heat integration and pinch analysis** - saving energy by design
6. **Design and process economics** - CAPEX, OPEX, and profitability
7. **Dynamic simulation** - how the plant behaves over time
8. **Digital twins** - a live model running beside the real plant

By the end you should be able to read a flowsheet, understand what a
simulator is actually solving, choose a property method sensibly, and see
how a design decision moves both energy use and money.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core aim of process design and simulation?",
                    (
                        opt("To improve a single reaction yield in the lab"),
                        opt(
                            "To turn chemistry into a working plant - equipment, "
                            "conditions, and balances - and prove it on a simulator "
                            "before construction",
                            correct=True,
                        ),
                        opt("To write the plant operating manual only"),
                        opt("To market the final product"),
                    ),
                    "Design takes a reaction and defines the equipment, conditions, "
                    "balances and economics of a full plant; the simulator is the tool.",
                ),
                q(
                    "How is each content lesson structured in this course?",
                    (
                        opt("A long theory dump with no examples"),
                        opt(
                            "One idea explained directly, a concrete worked example "
                            "(flowsheet, spec table, or calculation), and a diagram, then "
                            "a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A list of software download links"),
                    ),
                    "Explain, show a worked example, draw the diagram, then check "
                    "understanding with a quiz.",
                ),
            ),
        ),
        # -- 1. The process design workflow ----------------------------
        _t(
            "The process design workflow",
            "10 min",
            """# The process design workflow

A process is not designed in one leap. It moves through **stages of
increasing detail**, and at each stage a gate asks "is this still worth
continuing?" Getting the concept right is cheap; changing a built plant is
ruinously expensive - so most of the value is decided early.

The usual progression:

- **Concept and scoping** - what product, what capacity, what chemistry.
  Draw a **Block Flow Diagram (BFD)**: a few boxes for the major sections
  (reaction, separation, purification) and the streams between them.
- **Conceptual / preliminary design** - synthesize the flowsheet: pick the
  unit operations and their sequence. This is where **Douglas' hierarchy**
  helps: decide batch vs continuous, then input-output structure, then the
  recycle structure, then separations, then heat integration - outer
  decisions first because they constrain everything inside.
- **Basic (FEED) design** - close rigorous mass and energy balances on a
  simulator, size the major equipment, and produce the **Process Flow
  Diagram (PFD)** with a stream table.
- **Detailed design** - full **P&IDs**, instrumentation, control, piping,
  and mechanical specs, ready for procurement and construction.

A rule of thumb: the earliest phases lock in roughly **80 percent of the
eventual cost** while spending only a few percent of the engineering
effort. That is why simulation - which lets you try structures cheaply on
a computer - pays off most in the conceptual phase.

```mermaid
graph LR
    CONCEPT["Concept and scoping"] --> BFD["Block flow diagram"]
    BFD --> SYNTH["Flowsheet synthesis"]
    SYNTH --> FEED["Basic design PFD and balances"]
    FEED --> DETAIL["Detailed design and PID"]
    DETAIL --> BUILD["Procurement and construction"]
    FEED -->|"gate says no"| SYNTH
```

A worked framing of Douglas' hierarchy as ordered decisions:

```text
Level 1  Batch or continuous?
Level 2  Input-output: feeds, products, purge streams
Level 3  Recycle structure and reactor considerations
Level 4  Separation system (vapor and liquid recovery)
Level 5  Heat integration (energy network)
Rule: settle outer levels first - they constrain all inner ones.
```

Remember: design is staged and gated; the cheapest place to get a plant
right is on paper and in the simulator, long before it is built.
""",
        ),
        quiz_lesson(
            "Quiz: The process design workflow",
            (
                q(
                    "Why is it so important to get the early design phases right?",
                    (
                        opt("Because software licences are cheaper early on"),
                        opt(
                            "The earliest phases lock in most of the eventual cost while "
                            "using little engineering effort - changes get far more "
                            "expensive later",
                            correct=True,
                        ),
                        opt("Because detailed design is optional"),
                        opt("Because P&IDs are drawn first"),
                    ),
                    "Roughly 80 percent of lifetime cost is committed in concept and "
                    "conceptual design; that is where simulation pays off most.",
                ),
                q(
                    "What does a Block Flow Diagram (BFD) show?",
                    (
                        opt("Every valve, instrument and pipe spec"),
                        opt(
                            "The major process sections as a few boxes with the streams "
                            "between them - the highest-level view",
                            correct=True,
                        ),
                        opt("The detailed control logic"),
                        opt("The plant's financial statements"),
                    ),
                    "A BFD is the coarse map: reaction, separation, purification blocks "
                    "and the streams; detail comes later in PFDs and P&IDs.",
                ),
                q(
                    "In Douglas' hierarchy, why decide the outer levels (batch/continuous, "
                    "input-output) before the inner ones (separations, heat integration)?",
                    (
                        opt("Because inner levels are unimportant"),
                        opt(
                            "Outer decisions constrain everything inside them, so settling "
                            "them first avoids reworking the inner structure",
                            correct=True,
                        ),
                        opt("Because heat integration is always done first"),
                        opt("Because the simulator requires that order"),
                    ),
                    "The hierarchy is outer-to-inner: each level's choice bounds the "
                    "options available at the next.",
                ),
            ),
        ),
        # -- 2. Flowsheets and P&IDs -----------------------------------
        _t(
            "Process flowsheets and P&IDs",
            "10 min",
            """# Process flowsheets and P&IDs

A process is communicated through a small family of drawings, each with a
different level of detail and a different audience.

- **Block Flow Diagram (BFD)** - boxes and streams; the concept.
- **Process Flow Diagram (PFD)** - the **main equipment**, the major
  process streams connecting them, and the key operating conditions. It
  carries a **stream table** listing flow, temperature, pressure and
  composition at each numbered stream. The PFD answers "what does the
  process do and what flows where?"
- **Piping and Instrumentation Diagram (P&ID)** - **everything** needed to
  build and operate: every pipe with its size and spec, every valve,
  every instrument and control loop, relief devices, and utility
  connections. The P&ID answers "how is it plumbed, measured and
  controlled?" It is the master reference for construction, operation and
  HAZOP safety reviews.

Equipment and instruments follow standard symbols and tags. Instrument
tags come from the **ISA-5.1** standard: a letter code plus a loop number.
For example **TIC-101** is a Temperature Indicating Controller on loop
101; **FT-204** is a Flow Transmitter on loop 204. The first letter is the
measured variable (T, F, L, P), the following letters the function
(Indicate, Record, Control, Transmit).

```text
ISA-5.1 instrument tag: [variable][function]-[loop]
  T I C - 101   Temperature Indicating Controller, loop 101
  F  T  - 204   Flow Transmitter, loop 204
  L  V  - 305   Level control Valve, loop 305
  P I  - 110    Pressure Indicator, loop 110
First letter = measured variable; next = function; number = loop.
```

A simple control loop as it appears in concept on a P&ID: a transmitter
measures, a controller compares to setpoint, a valve acts.

```mermaid
graph LR
    PROC["Process line"] --> FT["FT flow transmitter"]
    FT --> FIC["FIC flow controller"]
    FIC --> FV["FV control valve"]
    FV --> PROC
    SP["Setpoint"] --> FIC
```

Remember: BFD is the concept, PFD is what the process does with a stream
table, and the P&ID is the buildable, operable master - down to every
valve, instrument and ISA tag.
""",
        ),
        quiz_lesson(
            "Quiz: Process flowsheets and P&IDs",
            (
                q(
                    "What distinguishes a P&ID from a PFD?",
                    (
                        opt("The P&ID has fewer details than the PFD"),
                        opt(
                            "The P&ID adds everything needed to build and operate - every "
                            "pipe, valve, instrument and control loop - while the PFD "
                            "shows main equipment, major streams and conditions",
                            correct=True,
                        ),
                        opt("They are the same drawing with different titles"),
                        opt("The PFD shows the control system, the P&ID does not"),
                    ),
                    "PFD = what the process does (with a stream table); P&ID = how it is "
                    "plumbed, measured and controlled - the construction and HAZOP master.",
                ),
                q(
                    "In the ISA-5.1 tag TIC-101, what does the tag tell you?",
                    (
                        opt("Tank Inlet Connection number 101"),
                        opt(
                            "A Temperature Indicating Controller on loop 101 - variable T, "
                            "functions Indicate and Control",
                            correct=True,
                        ),
                        opt("Total Instrument Count of 101"),
                        opt("A pressure relief valve"),
                    ),
                    "First letter is the measured variable (T), following letters the "
                    "function (Indicating Controller), number is the loop.",
                ),
                q(
                    "What information does a PFD's stream table carry?",
                    (
                        opt("Valve part numbers and pipe schedules"),
                        opt(
                            "For each numbered stream: flow rate, temperature, pressure "
                            "and composition",
                            correct=True,
                        ),
                        opt("The wiring diagram of the control room"),
                        opt("The plant's maintenance schedule"),
                    ),
                    "The stream table quantifies each PFD stream - the numeric backbone "
                    "of the mass and energy balance.",
                ),
            ),
        ),
        # -- 3. Steady-state simulation --------------------------------
        _t(
            "Steady-state process simulation (Aspen Plus, HYSYS, DWSIM)",
            "11 min",
            """# Steady-state process simulation

A **steady-state simulator** solves the flowsheet assuming conditions do
not change with time: every stream's flow, composition, temperature and
pressure is constant. You build the flowsheet from **unit-operation
blocks** (mixers, reactors, heat exchangers, pumps, distillation columns),
connect them with **streams**, choose a **thermodynamic property method**,
and the solver closes all the **mass and energy balances** plus the
**phase equilibrium** at once.

The major tools:

- **Aspen Plus** - the industry workhorse, especially for chemicals; a
  **sequential-modular** solver that computes blocks in flow order and
  iterates recycles to convergence.
- **Aspen HYSYS** - dominant in oil, gas and refining; strong on
  hydrocarbons and pressure-driven networks.
- **DWSIM** - a free, open-source simulator with the same concepts (unit
  ops, streams, property packages), excellent for learning without a
  licence.

A tear-and-iterate view of how a sequential-modular solver handles a
**recycle**: it guesses the torn stream, marches through the blocks, then
updates the guess until the loop converges.

```mermaid
graph LR
    FEED["Fresh feed"] --> MIX["Mixer"]
    MIX --> RX["Reactor"]
    RX --> SEP["Separator"]
    SEP --> PROD["Product"]
    SEP --> REC["Recycle stream"]
    REC --> MIX
    REC -->|"tear and iterate"| MIX
```

A minimal worked balance a simulator does automatically - a reactor with
80 percent conversion of A, feed 100 kmol/h A plus 100 kmol/h B, reaction
A + B to C:

```text
Basis: 100 kmol/h A, 100 kmol/h B in.  Reaction A + B -> C.
Conversion of A = 0.80  ->  A reacted = 80 kmol/h
  A out = 100 - 80 = 20 kmol/h
  B out = 100 - 80 = 20 kmol/h
  C out = 0 + 80   = 80 kmol/h
  Total out = 20 + 20 + 80 = 120 kmol/h  (moles fall: 2 -> 1)
Overall atom balance closes; the solver does this for every block and
iterates any recycle until inputs match outputs.
```

The engineer's job is not the arithmetic - the solver does that - but
**setting it up correctly**: the right blocks, realistic specifications,
and above all the right property method (next lesson). Garbage
thermodynamics in, garbage flowsheet out.

Remember: a steady-state simulator closes mass, energy and phase-equilibrium
balances over a connected set of unit-operation blocks, iterating recycles
to convergence - it is only as good as the specifications and properties
you give it.
""",
        ),
        quiz_lesson(
            "Quiz: Steady-state process simulation (Aspen Plus, HYSYS, DWSIM)",
            (
                q(
                    "What does a steady-state process simulator compute?",
                    (
                        opt("How the plant behaves second-by-second during a startup"),
                        opt(
                            "The time-invariant solution of the flowsheet - mass, energy "
                            "and phase-equilibrium balances over connected unit-operation "
                            "blocks",
                            correct=True,
                        ),
                        opt("Only the piping layout"),
                        opt("The plant's financial accounts"),
                    ),
                    "Steady state assumes nothing changes with time; the solver closes "
                    "all balances and phase equilibria at once. (Time behaviour is "
                    "dynamic simulation.)",
                ),
                q(
                    "How does a sequential-modular solver handle a recycle stream?",
                    (
                        opt("It ignores the recycle"),
                        opt(
                            "It tears the recycle, guesses that stream, marches through "
                            "the blocks, and iterates the guess until the loop converges",
                            correct=True,
                        ),
                        opt("It requires the user to solve it by hand"),
                        opt("It deletes the recycle to simplify"),
                    ),
                    "Tear-and-iterate: block-by-block in flow order, updating the torn "
                    "stream until inputs and outputs match.",
                ),
                q(
                    "Which statement about the tools is correct?",
                    (
                        opt("DWSIM is a paid tool with no unit operations"),
                        opt(
                            "DWSIM is a free, open-source simulator with the same core "
                            "concepts (unit ops, streams, property packages), good for "
                            "learning; HYSYS is strong in oil and gas",
                            correct=True,
                        ),
                        opt("HYSYS cannot handle hydrocarbons"),
                        opt("Aspen Plus has no recycle handling"),
                    ),
                    "Aspen Plus for chemicals, HYSYS for oil/gas/refining, DWSIM free "
                    "and open-source - all share the block-and-stream model.",
                ),
            ),
        ),
        # -- 4. Thermodynamic method selection -------------------------
        _t(
            "Thermodynamic method selection",
            "11 min",
            """# Thermodynamic method selection

The single most consequential choice in a simulation is the
**thermodynamic property method** (also called the property package or
fluid package). It sets how the simulator computes **phase equilibrium**
(the K-values that decide what boils and what dissolves) and enthalpies.
Pick it wrong and every downstream result - column, recycle, duty - is
wrong, even though the solver still "converges."

There are two broad families:

- **Equation-of-state (EOS)** methods - **Peng-Robinson (PR)** and
  **Soave-Redlich-Kwong (SRK)**. They handle both vapor and liquid from
  one equation and shine for **non-polar and lightly polar** systems at
  high pressure: hydrocarbons, natural gas, refinery streams, light gases.
- **Activity-coefficient** methods - **NRTL**, **UNIQUAC**, **Wilson**.
  They model **strongly non-ideal liquids** - polar mixtures, alcohols,
  water, anything that might form an **azeotrope** or split into two
  liquid phases - at low to moderate pressure. The vapor is handled
  separately (ideal gas or an EOS).

A widely used **selection heuristic**:

```text
Is the system real (non-ideal) polar liquid? e.g. water, alcohols, acids
  YES -> activity-coefficient model
          moderate/low pressure   -> NRTL or UNIQUAC (Wilson if no LLE)
          need vapor at pressure  -> pair with an EOS for the vapor
  NO (non-polar, hydrocarbons, gases, high pressure)
      -> equation of state: Peng-Robinson or SRK
Electrolytes / acids-bases in water -> electrolyte NRTL
Always: check binary interaction parameters exist and are regressed to
data; a missing or estimated parameter is the usual reason a column is wrong.
```

The parameters matter as much as the model: NRTL and UNIQUAC rely on
**binary interaction parameters** regressed against experimental VLE/LLE
data. If those are missing, the simulator estimates them (e.g. UNIFAC
group contribution) - useful for screening, dangerous for final design.

```mermaid
graph TD
    START["Choose property method"] --> Q1{"Polar non-ideal liquid?"}
    Q1 -->|"yes"| ACT["Activity model NRTL or UNIQUAC"]
    Q1 -->|"no"| EOS["Equation of state PR or SRK"]
    ACT --> Q2{"Electrolytes present?"}
    Q2 -->|"yes"| ELEC["Electrolyte NRTL"]
    Q2 -->|"no"| PARAMS["Check binary parameters vs data"]
    EOS --> PARAMS
    PARAMS --> DONE["Validate against known data"]
```

Remember: EOS (Peng-Robinson, SRK) for non-polar and high pressure;
activity models (NRTL, UNIQUAC, Wilson) for polar, non-ideal liquids and
azeotropes - and always validate the binary parameters against real data.
""",
        ),
        quiz_lesson(
            "Quiz: Thermodynamic method selection",
            (
                q(
                    "Why is the thermodynamic method the most important choice in a simulation?",
                    (
                        opt("It changes the colour of the flowsheet"),
                        opt(
                            "It sets phase equilibrium (K-values) and enthalpies, so a "
                            "wrong method makes every downstream result wrong even though "
                            "the solver converges",
                            correct=True,
                        ),
                        opt("It only affects the report formatting"),
                        opt("It has no effect on distillation columns"),
                    ),
                    "The property method decides what boils and dissolves; a converged "
                    "run on wrong thermodynamics is still wrong.",
                ),
                q(
                    "Which method family suits non-polar hydrocarbons and gases at high pressure?",
                    (
                        opt("Activity-coefficient models like NRTL"),
                        opt(
                            "Equation-of-state methods such as Peng-Robinson or SRK",
                            correct=True,
                        ),
                        opt("Electrolyte NRTL"),
                        opt("Ideal gas only, always"),
                    ),
                    "EOS methods (PR, SRK) handle vapor and liquid together and excel "
                    "for non-polar systems and high pressure.",
                ),
                q(
                    "A mixture of water and ethanol that forms an azeotrope should be modelled with…",
                    (
                        opt("Peng-Robinson alone, because it is simplest"),
                        opt(
                            "an activity-coefficient model (NRTL or UNIQUAC) with binary "
                            "parameters regressed to VLE data",
                            correct=True,
                        ),
                        opt("no property method at all"),
                        opt("an ideal solution assumption"),
                    ),
                    "Strongly non-ideal polar liquids and azeotropes need activity "
                    "models with good binary interaction parameters.",
                ),
            ),
        ),
        # -- 5. Heat integration and pinch analysis --------------------
        _t(
            "Heat integration and pinch analysis",
            "11 min",
            """# Heat integration and pinch analysis

Many streams in a plant need **heating**; others need **cooling**. Instead
of buying steam for every heater and cooling water for every cooler, you
can make the **hot streams heat the cold streams** through a network of
exchangers. **Heat integration** designs that network; **pinch analysis**
(Linnhoff) is the systematic method to find the best it can do.

The idea: combine all hot streams into one **hot composite curve** and all
cold streams into one **cold composite curve** on a temperature-versus-
enthalpy plot. Slide them together until the closest vertical approach
equals a chosen **minimum temperature difference, delta-T-min** (say 10 C).
That closest point is the **pinch**. It splits the problem in two and sets
the **energy targets**: the minimum hot utility (top) and minimum cold
utility (bottom) the process can possibly need.

Three golden rules follow from the pinch - break them and you waste energy:

```text
1. Do NOT transfer heat across the pinch.
2. Do NOT use hot utility below the pinch (nothing to reject it usefully).
3. Do NOT use cold utility above the pinch.
Above the pinch = heat sink (needs hot utility only).
Below the pinch = heat source (needs cold utility only).
```

A worked mini-target: two hot and two cold streams, delta-T-min = 10 C.

```text
Hot streams give up (need cooling):  H1 200->40 C, H2 150->60 C
Cold streams take up (need heating): C1 30->180 C, C2 50->140 C
Build composite curves, set delta-T-min = 10 C, read the overlap.
Result (illustrative): pinch at 90/80 C hot/cold; targets
  Q_hot,min  = 1.8 MW   (minimum steam)
  Q_cold,min = 1.2 MW   (minimum cooling water)
Any exchanger that moves heat across the 90/80 pinch forces you to add
BOTH more steam and more cooling - pure waste.
```

The payoff: pinch targets tell you the **minimum utilities before you draw
a single exchanger**, so you know how good a network could be and how far
your current design is from ideal. It is a classic energy-and-cost trade:
a smaller delta-T-min saves utilities but needs larger, costlier exchangers.

```mermaid
graph TD
    STREAMS["All hot and cold streams"] --> COMP["Build composite curves"]
    COMP --> DTMIN["Choose delta-T-min"]
    DTMIN --> PINCH["Find the pinch point"]
    PINCH --> TARGET["Set min hot and cold utility targets"]
    TARGET --> NET["Design exchanger network"]
    NET --> RULES["Obey no cross-pinch heat transfer"]
```

Remember: pinch analysis sets the energy targets first - minimum hot and
cold utility - then you design a network that never transfers heat across
the pinch. Targets before design.
""",
        ),
        quiz_lesson(
            "Quiz: Heat integration and pinch analysis",
            (
                q(
                    "What is the 'pinch' in pinch analysis?",
                    (
                        opt("The hottest stream in the plant"),
                        opt(
                            "The point of closest approach between the hot and cold "
                            "composite curves - set by delta-T-min - which fixes the "
                            "minimum utility targets",
                            correct=True,
                        ),
                        opt("A type of valve"),
                        opt("The largest heat exchanger"),
                    ),
                    "Slide the composite curves to delta-T-min; the closest point is the "
                    "pinch, and it sets the minimum hot and cold utilities.",
                ),
                q(
                    "Which is one of the golden rules of pinch design?",
                    (
                        opt("Always transfer heat across the pinch"),
                        opt(
                            "Do not transfer heat across the pinch - doing so forces both "
                            "extra hot and extra cold utility",
                            correct=True,
                        ),
                        opt("Use hot utility below the pinch freely"),
                        opt("Ignore delta-T-min entirely"),
                    ),
                    "No cross-pinch heat, no hot utility below, no cold utility above - "
                    "each violation adds avoidable utility cost.",
                ),
                q(
                    "What is the trade-off in choosing a smaller delta-T-min?",
                    (
                        opt("It has no effect on cost"),
                        opt(
                            "Smaller delta-T-min lowers utility use but needs larger, "
                            "more expensive heat exchangers - an energy-versus-capital "
                            "trade",
                            correct=True,
                        ),
                        opt("It always reduces both utilities and exchanger size"),
                        opt("It only changes the drawing, not the cost"),
                    ),
                    "A tighter approach recovers more heat (less utility) but demands "
                    "more area (more capital) - the classic pinch trade-off.",
                ),
            ),
        ),
        # -- 6. Design and economics -----------------------------------
        _t(
            "Linking design to process economics",
            "11 min",
            """# Linking design to process economics

A design is only good if it makes money. Every simulation decision - a
larger column for higher purity, a tighter delta-T-min for less steam, a
recycle to raise conversion - is a trade between **capital cost (CAPEX)**
and **operating cost (OPEX)**. Economics is how the design is judged.

The building blocks:

- **CAPEX** - the one-time cost to build. Equipment cost usually scales
  with size by the **six-tenths rule**: doubling capacity does *not*
  double cost. Bare equipment is multiplied up by **Lang factors** to
  cover installation, piping, instruments and engineering, giving the
  total plant investment.
- **OPEX** - the recurring cost to run: raw materials (often dominant),
  utilities (steam, cooling water, electricity), labour and maintenance.
- **Profitability** - combine them over the plant life with the time value
  of money: **Net Present Value (NPV)**, **payback period**, and
  **discounted cash flow rate of return**.

The six-tenths (economy-of-scale) scaling rule:

```text
Cost_2 = Cost_1 * (Size_2 / Size_1) ^ 0.6

Example: a reactor for 100 m3/h costs 500,000 USD.
Estimate the cost at 200 m3/h:
  Cost_2 = 500,000 * (200/100)^0.6
         = 500,000 * 2^0.6
         = 500,000 * 1.516
         = 758,000 USD
Doubling the size raised cost by ~52 percent, not 100 percent - which is
why bigger single units are usually cheaper per unit of capacity.
```

A quick calculation in Python of a simple payback and NPV:

```python
capex = 758_000            # installed equipment cost, USD
annual_profit = 220_000    # revenue minus OPEX, USD/year
rate = 0.10                # discount rate
life = 8                   # years

payback = capex / annual_profit                    # simple payback
npv = -capex + sum(annual_profit / (1 + rate) ** t
                   for t in range(1, life + 1))     # discounted
print(f"payback = {payback:.1f} yr")   # -> 3.4 yr
print(f"NPV = {npv:,.0f} USD")         # -> 415,000 USD (positive = worth it)
```

Modern simulators plug straight into this: **Aspen Process Economic
Analyzer** and HYSYS economics map each block to sized, costed equipment,
so you can see a design change ripple into CAPEX, OPEX and NPV immediately.

```mermaid
graph LR
    DESIGN["Simulation and sizing"] --> CAPEX["Capital cost CAPEX"]
    DESIGN --> OPEX["Operating cost OPEX"]
    CAPEX --> CASH["Cash flow over plant life"]
    OPEX --> CASH
    CASH --> NPV["NPV and payback"]
    NPV --> DECIDE["Accept or revise design"]
    DECIDE -->|"revise"| DESIGN
```

Remember: design choices are CAPEX-versus-OPEX trades; equipment scales by
the six-tenths rule, and NPV or payback - not size alone - decides whether
a flowsheet is worth building.
""",
        ),
        quiz_lesson(
            "Quiz: Linking design to process economics",
            (
                q(
                    "What does the 'six-tenths rule' describe?",
                    (
                        opt("Six-tenths of a plant must be built first"),
                        opt(
                            "Equipment cost scales with size to about the 0.6 power, so "
                            "doubling capacity costs far less than double - economy of "
                            "scale",
                            correct=True,
                        ),
                        opt("Sixty percent of streams are recycled"),
                        opt("The discount rate is always 0.6"),
                    ),
                    "Cost_2 = Cost_1 * (Size_2/Size_1)^0.6; bigger single units are "
                    "cheaper per unit of capacity.",
                ),
                q(
                    "What is the difference between CAPEX and OPEX?",
                    (
                        opt("They are the same, measured in different currencies"),
                        opt(
                            "CAPEX is the one-time cost to build the plant; OPEX is the "
                            "recurring cost to run it (feed, utilities, labour, "
                            "maintenance)",
                            correct=True,
                        ),
                        opt("CAPEX is only labour; OPEX is only equipment"),
                        opt("OPEX is paid once, CAPEX every year"),
                    ),
                    "CAPEX builds it (multiplied up by Lang factors); OPEX runs it - "
                    "both feed into NPV over the plant life.",
                ),
                q(
                    "Why use NPV or payback rather than judging a design by equipment size alone?",
                    (
                        opt("Because size cannot be measured"),
                        opt(
                            "Because profitability combines CAPEX and OPEX over time with "
                            "the time value of money - a bigger unit can still be the more "
                            "profitable choice",
                            correct=True,
                        ),
                        opt("Because NPV ignores operating cost"),
                        opt("Because payback is the same as CAPEX"),
                    ),
                    "NPV/payback weigh capital against operating cash flows over the "
                    "plant life; size alone hides the CAPEX-OPEX trade.",
                ),
            ),
        ),
        # -- 7. Dynamic simulation -------------------------------------
        _t(
            "Dynamic simulation",
            "11 min",
            """# Dynamic simulation

Steady-state answers "where does the plant settle?" **Dynamic simulation**
answers "**how does it get there, and what happens when something
changes?**" It solves the same balances but keeps the **accumulation
terms** - so results are functions of time, not single numbers. Where a
steady-state model has algebraic balances, a dynamic model integrates
**differential equations** with equipment holdups, volumes and inertia.

The general dynamic balance for any quantity is:

```text
Accumulation = In - Out + Generation - Consumption

For a well-mixed tank, total mass:
   d(rho * V) / dt = m_in - m_out
For a component A with reaction:
   d(V * C_A) / dt = F_in*C_A,in - F_out*C_A - k*C_A*V
Steady state is just the special case where every d/dt = 0.
Dynamics keep the d/dt terms, so holdup and time constants matter.
```

What dynamic simulation is used for - things a steady-state model
fundamentally cannot show:

- **Startup, shutdown and transitions** - filling columns, warming
  reactors, moving between grades.
- **Control system design and tuning** - test PID loops, setpoint changes
  and disturbances *in the model* before the real plant. Aspen HYSYS
  Dynamics and Aspen Plus Dynamics are built for this.
- **Safety studies** - relief valve sizing, response to a cooling failure
  or a runaway reaction, compressor surge.
- **Operator training simulators (OTS)** - a live model behind a real
  control interface so operators practise upsets safely.

A control loop responding to a disturbance over time - the essence of what
a dynamic model reveals:

```mermaid
graph LR
    DIST["Disturbance feed change"] --> PLANT["Process with holdup"]
    PLANT --> MEAS["Measured variable drifts"]
    MEAS --> CTRL["Controller acts over time"]
    CTRL --> VALVE["Valve moves"]
    VALVE --> PLANT
    MEAS --> SETTLE["Settles to new steady state"]
```

The key mental shift: steady state ignores **time and holdup**; dynamics
put them back. A vessel's volume, a controller's tuning, and a heater's
thermal inertia all determine *how fast and how smoothly* the plant reaches
the steady state the other model predicted.

Remember: dynamic simulation keeps the accumulation terms, so it shows
startups, disturbances, control behaviour and safety transients over time -
the trajectory, not just the destination.
""",
        ),
        quiz_lesson(
            "Quiz: Dynamic simulation",
            (
                q(
                    "How does a dynamic simulation differ from a steady-state one?",
                    (
                        opt("It uses different chemistry"),
                        opt(
                            "It keeps the accumulation (d/dt) terms and integrates over "
                            "time, so results are trajectories rather than single "
                            "steady values",
                            correct=True,
                        ),
                        opt("It cannot model reactors"),
                        opt("It ignores mass balances"),
                    ),
                    "Accumulation = In - Out + Generation - Consumption; steady state is "
                    "the special case where every d/dt = 0.",
                ),
                q(
                    "Which task genuinely requires a dynamic model?",
                    (
                        opt("Closing a single steady mass balance"),
                        opt(
                            "Designing and tuning control loops, and studying startup, "
                            "disturbances or a cooling-failure transient",
                            correct=True,
                        ),
                        opt("Reading a stream table"),
                        opt("Choosing a property method"),
                    ),
                    "Control tuning, startup/shutdown, and safety transients are "
                    "time-dependent - only a dynamic model shows them.",
                ),
                q(
                    "Why do equipment holdup and vessel volume matter in dynamics but not in steady state?",
                    (
                        opt("They never matter"),
                        opt(
                            "They set the time constants - how fast and smoothly the "
                            "plant moves between states - which steady state, having no "
                            "time, cannot capture",
                            correct=True,
                        ),
                        opt("They only affect the drawing"),
                        opt("They change the chemistry of the reaction"),
                    ),
                    "Holdup, volume and thermal inertia govern the trajectory; steady "
                    "state only reports the endpoint.",
                ),
            ),
        ),
        # -- 8. Digital twins ------------------------------------------
        _t(
            "Digital twins of processes",
            "11 min",
            """# Digital twins of processes

A **digital twin** is a simulation model that runs **alongside the real
plant**, continuously fed with **live sensor data**, so it mirrors the
actual operating state in real time. A design simulation is a model of a
plant that might exist; a digital twin is a model of the plant that *does*
exist, kept in step with it.

What makes a twin more than a simulation:

- **Live data link** - plant historians and sensors (via OPC UA, MQTT, or
  a historian like OSIsoft PI) stream measured flows, temperatures and
  pressures into the model continuously.
- **Data reconciliation** - measurements always carry error, so the twin
  reconciles them against the mass and energy balances to produce one
  consistent, corrected picture of the plant.
- **Feedback and use** - the reconciled model then supports monitoring,
  what-if studies, soft sensors (estimating things you cannot measure),
  predictive maintenance and optimization.

The three levels are worth keeping straight:

```text
Digital MODEL   - a static simulation; no automatic data exchange.
Digital SHADOW  - real plant data flows INTO the model (one direction).
Digital TWIN    - two-way: data flows in, and model-driven decisions
                  (setpoints, advice, optimization) flow back to the plant.
The two-way feedback loop is what makes it a true twin.
```

Digital twins are a pillar of **Industry 4.0**, and increasingly they
couple a first-principles simulator with **machine-learning models**
trained on operating history - hybrid models for property prediction,
optimization and anomaly detection that a rigorous model alone would be
too slow to provide online.

```mermaid
graph TD
    PLANT["Real plant sensors"] --> DATA["Live data historian"]
    DATA --> RECON["Data reconciliation"]
    RECON --> TWIN["Digital twin model"]
    TWIN --> INSIGHT["Monitoring and soft sensors"]
    TWIN --> OPT["Optimization and what-if"]
    OPT --> SETPT["Improved setpoints"]
    SETPT --> PLANT
```

Use cases in practice: catching equipment drift before it fails
(predictive maintenance), estimating an unmeasured composition from
temperatures and pressures (a soft sensor), and continuously nudging
setpoints toward the most profitable operating point (real-time
optimization).

Remember: a digital twin is a live, data-fed, two-way model of an existing
plant - reconciled against real measurements and closing the loop back to
operations, often with machine learning alongside the physics.
""",
        ),
        quiz_lesson(
            "Quiz: Digital twins of processes",
            (
                q(
                    "What distinguishes a digital twin from an ordinary design simulation?",
                    (
                        opt("A twin uses no thermodynamics"),
                        opt(
                            "A twin runs alongside an existing plant, continuously fed "
                            "with live sensor data and reconciled to mirror the real "
                            "operating state",
                            correct=True,
                        ),
                        opt("A twin is only a drawing"),
                        opt("A twin cannot be updated"),
                    ),
                    "Design simulation models a plant that might exist; a twin mirrors "
                    "the plant that does exist, in real time.",
                ),
                q(
                    "What separates a digital 'shadow' from a true digital 'twin'?",
                    (
                        opt("Nothing, the terms are identical"),
                        opt(
                            "A shadow has data flowing one way (plant into model); a true "
                            "twin closes the loop with model-driven decisions flowing back "
                            "to the plant",
                            correct=True,
                        ),
                        opt("A shadow needs no sensors"),
                        opt("A twin never uses plant data"),
                    ),
                    "Model = static; shadow = one-way data in; twin = two-way feedback - "
                    "that returning loop is the defining feature.",
                ),
                q(
                    "Why does a digital twin perform data reconciliation?",
                    (
                        opt("To delete the sensor readings"),
                        opt(
                            "Because raw measurements carry error; reconciling them "
                            "against the mass and energy balances yields one consistent, "
                            "corrected picture of the plant",
                            correct=True,
                        ),
                        opt("To slow the model down"),
                        opt("Because balances are optional"),
                    ),
                    "Reconciliation forces noisy measurements to obey conservation laws, "
                    "giving a trustworthy state for monitoring and optimization.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why does the early, conceptual phase of process design deserve the most care?",
                    (
                        opt("Because it is the most fun"),
                        opt(
                            "It commits most of the plant's lifetime cost while using "
                            "little effort - and a simulator lets you try structures "
                            "cheaply there",
                            correct=True,
                        ),
                        opt("Because detailed design is skipped"),
                        opt("Because P&IDs are drawn first"),
                    ),
                    "Roughly 80 percent of cost is locked in early; cheap changes on the "
                    "computer, ruinous changes on built steel.",
                ),
                q(
                    "A P&ID differs from a PFD because it…",
                    (
                        opt("shows less detail"),
                        opt(
                            "adds every pipe, valve, instrument and control loop needed "
                            "to build and operate the plant - the construction and HAZOP "
                            "master",
                            correct=True,
                        ),
                        opt("omits the equipment"),
                        opt("shows only economics"),
                    ),
                    "PFD = what the process does with a stream table; P&ID = how it is "
                    "plumbed, measured and controlled.",
                ),
                q(
                    "What does a steady-state simulator do with a recycle stream?",
                    (
                        opt("Deletes it"),
                        opt(
                            "Tears it, guesses the stream, marches through the blocks and "
                            "iterates until the loop converges",
                            correct=True,
                        ),
                        opt("Solves it only by hand"),
                        opt("Ignores mass balance on it"),
                    ),
                    "Sequential-modular solvers tear-and-iterate recycles to convergence.",
                ),
                q(
                    "For a high-pressure natural-gas (non-polar) system, the best "
                    "property method family is…",
                    (
                        opt("activity-coefficient models like NRTL"),
                        opt(
                            "an equation of state such as Peng-Robinson or SRK",
                            correct=True,
                        ),
                        opt("electrolyte NRTL"),
                        opt("no method at all"),
                    ),
                    "EOS methods handle non-polar vapor and liquid at high pressure; "
                    "activity models are for polar, non-ideal liquids.",
                ),
                q(
                    "In pinch analysis, what does the pinch point fix before any "
                    "exchanger is drawn?",
                    (
                        opt("The plant's revenue"),
                        opt(
                            "The minimum hot and cold utility targets - the least energy "
                            "the process can possibly need",
                            correct=True,
                        ),
                        opt("The number of pumps"),
                        opt("The control loop tuning"),
                    ),
                    "Composite curves at delta-T-min give the pinch and the utility "
                    "targets; then you design a network that never crosses the pinch.",
                ),
                q(
                    "Which golden rule keeps a heat-exchanger network at its energy target?",
                    (
                        opt("Transfer as much heat across the pinch as possible"),
                        opt(
                            "Never transfer heat across the pinch",
                            correct=True,
                        ),
                        opt("Use hot utility below the pinch"),
                        opt("Ignore delta-T-min"),
                    ),
                    "Cross-pinch heat transfer forces extra hot AND cold utility - pure waste.",
                ),
                q(
                    "By the six-tenths rule, doubling equipment capacity roughly…",
                    (
                        opt("doubles the cost"),
                        opt(
                            "raises the cost by about 50 percent, not 100 percent - "
                            "economy of scale",
                            correct=True,
                        ),
                        opt("halves the cost"),
                        opt("leaves cost unchanged"),
                    ),
                    "Cost scales with size^0.6, so 2^0.6 is about 1.5 - bigger units are "
                    "cheaper per unit of capacity.",
                ),
                q(
                    "What fundamentally separates a dynamic simulation from a steady-state one?",
                    (
                        opt("Different chemistry"),
                        opt(
                            "The dynamic model keeps the accumulation (d/dt) terms and "
                            "integrates over time; steady state sets every d/dt to zero",
                            correct=True,
                        ),
                        opt("Dynamics cannot model reactors"),
                        opt("Steady state uses no property method"),
                    ),
                    "Dynamics show the trajectory (startup, disturbances, control); "
                    "steady state shows only the destination.",
                ),
                q(
                    "A digital twin is best described as…",
                    (
                        opt("a static drawing of a proposed plant"),
                        opt(
                            "a live model of an existing plant, fed with real sensor data, "
                            "reconciled to the balances, closing the loop back to "
                            "operations",
                            correct=True,
                        ),
                        opt("a spreadsheet of costs"),
                        opt("a control valve"),
                    ),
                    "Twin = data-fed, reconciled, two-way model of the real plant - often "
                    "coupled with machine learning.",
                ),
                q(
                    "Why does a digital twin reconcile its incoming sensor data?",
                    (
                        opt("To discard the data"),
                        opt(
                            "Because measurements carry error; reconciling them against "
                            "mass and energy balances yields one consistent, trustworthy "
                            "plant state",
                            correct=True,
                        ),
                        opt("To make the model run slower"),
                        opt("Because balances do not apply to real plants"),
                    ),
                    "Reconciliation forces noisy readings to obey conservation, giving a "
                    "reliable state for monitoring, soft sensors and optimization.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PROCESS_DESIGN_SIMULATION_COURSES: tuple[SeedCourse, ...] = (_PROCESS_DESIGN_SIMULATION,)
