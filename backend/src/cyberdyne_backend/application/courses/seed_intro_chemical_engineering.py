"""Academy seed content - Introduction to Chemical Engineering.

An orientation to chemical engineering: what chemical engineers do, the
process industries they serve, the unit-operations concept that organizes
the whole discipline, and how the field is being transformed by
simulation, data and AI. Every lesson is a direct explanation with a
concrete example (a design equation, a worked balance, a flow diagram or a
Python snippet) and a mermaid diagram, followed by a checkpoint quiz; the
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


_INTRO_CHEMICAL_ENGINEERING = SeedCourse(
    slug="intro-chemical-engineering",
    title="Introduction to Chemical Engineering",
    description=(
        "An orientation to chemical engineering: what chemical engineers do, "
        "the process industries they serve, the unit-operations concept that "
        "organizes the discipline, process and block flow diagrams, units and "
        "dimensions, the safety and sustainability mindset, and how simulation, "
        "data and AI are transforming the modern chemical engineer - with a "
        "worked example and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Introduction to Chemical Engineering

Chemical engineering is the discipline that turns raw materials into the
products modern life depends on - fuels, plastics, medicines, food,
fertilizers, clean water and semiconductors - at scale, safely, and
economically. A chemist discovers a reaction in a flask; a **chemical
engineer** designs, builds and runs the plant that makes tonnes of it
every day. This course gives you the whole picture before you go deep on
any single topic.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a design equation, a worked
material balance, a flow diagram or a Python snippet), and draws the idea
as a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **History and the role** - what a chemical engineer actually does
2. **The process industries** - petrochemical, pharma, food, materials
3. **Anatomy of a process** - raw materials to finished products
4. **Unit operations** - the reusable building blocks of every plant
5. **Flow diagrams** - block diagrams and process flow diagrams
6. **Units and dimensions** - getting the engineering quantities right
7. **Safety and sustainability** - the mindset that comes first
8. **The modern engineer** - simulation, data, AI and Industry 4.0

This is the map. It sits in front of the deeper courses on
thermodynamics, transport, reaction engineering and process control -
knowing where each fits makes them far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What best describes what a chemical engineer does?",
                    (
                        opt("Discovers new molecules at the laboratory bench only"),
                        opt(
                            "Designs, builds and operates the processes and plants that "
                            "turn raw materials into useful products at scale, safely and "
                            "economically",
                            correct=True,
                        ),
                        opt("Writes the marketing copy for chemical products"),
                        opt("Only sells laboratory glassware"),
                    ),
                    "A chemist finds a reaction; a chemical engineer scales it into a "
                    "safe, economic, continuous process.",
                ),
                q(
                    "How does this course relate to later courses on thermodynamics, "
                    "transport and reaction engineering?",
                    (
                        opt("It replaces them entirely"),
                        opt(
                            "It is the big-picture orientation that shows where each "
                            "topic fits, before the deeper courses",
                            correct=True,
                        ),
                        opt("It only covers plant accounting"),
                        opt("It is unrelated to those subjects"),
                    ),
                    "Learn the map first (this course), then the deep dives make sense in context.",
                ),
            ),
        ),
        # -- 1. History and the role -----------------------------------
        _t(
            "History and the role of the chemical engineer",
            "9 min",
            """# History and the role of the chemical engineer

Chemical engineering emerged when industry needed people who could take a
**bench reaction** and make it work at the scale of tonnes per day. In
the late 1800s, factories making soda ash, sulfuric acid and dyes were
run by chemists and mechanical engineers working separately. The new
profession bridged them: someone who understood **both** the chemistry
and the equipment. The first dedicated program opened at MIT in 1888, and
in 1908 the **AIChE** (American Institute of Chemical Engineers) was
founded.

The defining intellectual move came in 1915, when Arthur D. Little named
the **unit operations** idea: any process, however different its
chemistry, is built from a small set of reusable physical steps -
distillation, filtration, heat exchange, and so on. That insight is what
makes chemical engineering a general discipline rather than a catalogue of
recipes.

What the role covers today:

- **Design** - size the reactors, columns and exchangers; choose
  materials and operating conditions.
- **Operations** - keep a running plant safe, on-spec and efficient.
- **Scale-up** - move a process from lab to pilot plant to full scale,
  where heat, mass transfer and mixing behave very differently.
- **Optimization** - squeeze more yield, less energy and less waste from
  an existing process.

The core skill is the **balance**: track mass and energy through a
process. Nothing is created or destroyed, so what goes in must come out or
accumulate. A steady-state overall mass balance is simply:

```text
mass in  =  mass out
(no accumulation at steady state)

Example: a mixer receives 100 kg/h of water and 25 kg/h of salt.
Product stream = 100 + 25 = 125 kg/h, at 25/125 = 0.20 mass fraction salt.
```

```mermaid
graph LR
    CHEM["Bench chemistry"] --> ENG["Chemical engineer"]
    EQUIP["Process equipment"] --> ENG
    ENG --> DESIGN["Design"]
    ENG --> OPS["Operate"]
    ENG --> SCALE["Scale up"]
    ENG --> OPT["Optimize"]
```

Remember: the chemical engineer is the person who makes chemistry work
at scale - and the mass and energy balance is the tool they never put
down.
""",
        ),
        quiz_lesson(
            "Quiz: History and the role of the chemical engineer",
            (
                q(
                    "Why did chemical engineering emerge as a distinct profession?",
                    (
                        opt("To replace chemists in the laboratory"),
                        opt(
                            "Industry needed people who understood both the chemistry "
                            "and the equipment, to run reactions at industrial scale",
                            correct=True,
                        ),
                        opt("To design bridges and buildings"),
                        opt("Purely to write safety regulations"),
                    ),
                    "It bridged the chemist and the mechanical engineer - scaling bench "
                    "reactions into full plants.",
                ),
                q(
                    "What is the single tool a chemical engineer relies on most across "
                    "design and operations?",
                    (
                        opt("A microscope"),
                        opt(
                            "The mass and energy balance - tracking what enters, leaves "
                            "and accumulates",
                            correct=True,
                        ),
                        opt("A spreadsheet of stock prices"),
                        opt("A hardness tester"),
                    ),
                    "Conservation of mass and energy underlies nearly every calculation "
                    "in the field.",
                ),
                q(
                    "At steady state with no reaction, a mixer takes in 100 kg/h water "
                    "and 25 kg/h salt. What is the product flow?",
                    (
                        opt("100 kg/h"),
                        opt("25 kg/h"),
                        opt("125 kg/h - mass in equals mass out", correct=True),
                        opt("75 kg/h"),
                    ),
                    "Steady state means no accumulation: total out equals total in, 125 kg/h.",
                ),
            ),
        ),
        # -- 2. The process industries ---------------------------------
        _t(
            "The chemical process industries",
            "10 min",
            """# The chemical process industries

Chemical engineers work across a broad set of **process industries** -
sectors that transform matter through physical and chemical steps. They
share the same fundamentals but differ enormously in scale, product value
and the rules they operate under.

The major sectors:

- **Petrochemical and refining** - crude oil and natural gas become
  fuels, and the building-block chemicals (ethylene, propylene, benzene)
  that feed everything downstream. Huge scale, continuous operation, thin
  margins per kilogram. Governed by codes like **ASME BPVC** for pressure
  equipment and **API** standards.
- **Pharmaceutical and fine chemicals** - high-value, low-volume products
  made in batches. Purity and traceability are everything, under **GMP**
  (Good Manufacturing Practice) and **ICH** quality guidelines. A gram can
  be worth more than a tonne of fuel.
- **Food and beverage** - drying, evaporation, pasteurization,
  fermentation and separation, under food-safety rules such as **HACCP**.
  Gentle conditions to preserve quality.
- **Materials, polymers and specialty** - plastics, coatings, fertilizers,
  semiconductors and battery materials. Product **performance** (strength,
  purity, particle size) defines the spec.

A useful way to compare them is **volume versus value**:

```text
Sector            Volume        Value per kg   Mode        Key regime
Petrochemical     very high     low            continuous  ASME/API
Bulk materials    high          low-medium     continuous  performance
Food              medium        medium         both        HACCP
Pharma / fine     low           very high      batch       GMP/ICH
```

```mermaid
graph TD
    CPI["Chemical process industries"] --> PET["Petrochemical and refining"]
    CPI --> PHARMA["Pharma and fine chemicals"]
    CPI --> FOOD["Food and beverage"]
    CPI --> MAT["Materials and polymers"]
    PET --> CONT["High volume continuous"]
    PHARMA --> BATCH["High value batch"]
    FOOD --> QUALITY["Gentle quality driven"]
    MAT --> SPEC["Performance spec driven"]
```

Remember: the same unit operations appear everywhere, but scale, value
and regulation shape how each industry uses them - continuous and cheap at
one end, batch and precious at the other.
""",
        ),
        quiz_lesson(
            "Quiz: The chemical process industries",
            (
                q(
                    "Which pairing correctly describes the petrochemical sector?",
                    (
                        opt("Low volume, very high value, batch, GMP"),
                        opt(
                            "Very high volume, low value per kg, continuous operation, "
                            "governed by codes like ASME and API",
                            correct=True,
                        ),
                        opt("Medium volume, gentle conditions, HACCP only"),
                        opt("Made one gram at a time in a laboratory"),
                    ),
                    "Refining and petrochemicals run continuously at enormous scale with "
                    "thin per-kilogram margins.",
                ),
                q(
                    "Why is pharmaceutical manufacturing typically done in batches under GMP?",
                    (
                        opt("Because the products are cheap and plentiful"),
                        opt(
                            "The products are high-value and low-volume, and purity and "
                            "traceability must be tightly controlled",
                            correct=True,
                        ),
                        opt("Because batch mode is always faster"),
                        opt("Because no equipment exists for continuous pharma"),
                    ),
                    "Batch operation plus GMP/ICH gives the control and traceability "
                    "high-value medicines require.",
                ),
                q(
                    "What do all the process industries have in common?",
                    (
                        opt("They all make fuels"),
                        opt("They all operate in batch mode"),
                        opt(
                            "They transform matter using the same underlying unit "
                            "operations, even though scale, value and regulation differ",
                            correct=True,
                        ),
                        opt("They all avoid any regulation"),
                    ),
                    "The fundamentals and building blocks are shared; scale, value and "
                    "rules differ.",
                ),
            ),
        ),
        # -- 3. Anatomy of a process -----------------------------------
        _t(
            "Anatomy of a chemical process",
            "10 min",
            """# Anatomy of a chemical process

Almost every chemical process, from an oil refinery to a beer brewery,
follows the same three-part **anatomy**: prepare the feed, react it, then
separate and finish the products. Learning to see this shape in any plant
is one of the most useful habits in the field.

The three stages:

1. **Feed preparation (upstream)** - get raw materials to the condition
   the reaction needs: purify, mix, heat, pressurize, grind. Bad feed
   preparation ruins everything downstream.
2. **Reaction** - the chemical heart of the process, where feed becomes
   product in a **reactor**. Temperature, pressure, catalyst and residence
   time set how far and how fast the reaction goes.
3. **Separation and purification (downstream)** - reactions are rarely
   complete or perfectly selective, so the reactor outlet is a mixture.
   Separation (distillation, filtration, extraction) pulls out the product
   and, crucially, **recycles** unreacted feed back to the reactor.

That **recycle** loop is a hallmark of good process design: it lets you
run the reactor at modest conversion per pass while still using almost all
the feed overall. A key definition:

```text
Conversion = (reactant consumed) / (reactant fed)

Example: ammonia synthesis converts only ~15 percent per pass, but by
recycling unreacted N2 and H2, overall use of the feed approaches
~98 percent. Low per-pass conversion, high overall utilization.
```

```mermaid
graph LR
    RAW["Raw materials"] --> PREP["Feed preparation"]
    PREP --> RXN["Reactor"]
    RXN --> SEP["Separation"]
    SEP --> PROD["Product"]
    SEP --> RECYCLE["Unreacted feed"]
    RECYCLE --> RXN
```

Remember: prepare, react, separate - with a recycle that turns modest
single-pass conversion into high overall efficiency. Spot these three
stages and any plant becomes readable.
""",
        ),
        quiz_lesson(
            "Quiz: Anatomy of a chemical process",
            (
                q(
                    "What are the three broad stages common to almost every chemical process?",
                    (
                        opt("Marketing, sales, shipping"),
                        opt(
                            "Feed preparation, reaction, and separation or purification",
                            correct=True,
                        ),
                        opt("Heating, cooling, storage"),
                        opt("Design, build, demolish"),
                    ),
                    "Prepare the feed, react it, then separate and finish the products.",
                ),
                q(
                    "Why is a recycle loop such a common feature of process design?",
                    (
                        opt("It makes the plant look more complicated"),
                        opt(
                            "It returns unreacted feed to the reactor, so modest "
                            "conversion per pass still gives high overall feed use",
                            correct=True,
                        ),
                        opt("It is required by law in all plants"),
                        opt("It removes the need for any reactor"),
                    ),
                    "Recycling unreacted material turns low single-pass conversion into "
                    "near-complete overall utilization.",
                ),
                q(
                    "Ammonia synthesis converts only about 15 percent per pass yet uses "
                    "roughly 98 percent of the feed overall. How?",
                    (
                        opt("The reaction is actually complete each pass"),
                        opt("The feed is thrown away and replaced"),
                        opt(
                            "Unreacted nitrogen and hydrogen are separated and recycled "
                            "back to the reactor",
                            correct=True,
                        ),
                        opt("Conversion and utilization mean the same thing"),
                    ),
                    "Separation plus recycle decouples per-pass conversion from overall "
                    "feed utilization.",
                ),
            ),
        ),
        # -- 4. The unit-operations concept ----------------------------
        _t(
            "The unit-operations concept",
            "10 min",
            """# The unit-operations concept

The single most powerful organizing idea in chemical engineering is the
**unit operation**: any process is built from a small library of standard
**physical steps**, each governed by the same principles no matter what
chemical is flowing through it. Master the handful of unit operations and
you can read - and design - almost any plant.

A unit operation is a **physical** change (separating, heating, mixing);
a **unit process** is the **chemical** change (the reaction itself).
Distillation is a unit operation; oxidation is a unit process.

Common unit operations, grouped by what they exploit:

- **Fluid flow and mixing** - pumps, compressors, agitators. Move and
  blend material.
- **Heat transfer** - heat exchangers, evaporators, condensers. Add or
  remove energy.
- **Mass transfer and separation** - distillation, absorption,
  extraction, drying, adsorption. Move a component from one phase to
  another. This is where most equipment (and most of the energy) goes.
- **Mechanical and particle** - filtration, crushing, crystallization,
  sedimentation. Handle solids and phases.

Why this matters: distillation obeys the **same equations** whether you
are separating crude oil or purifying a drug. So you learn the operation
once and reuse it everywhere. Separations are driven by an **equilibrium
relationship**; for a simple stage the relative volatility governs how
easily two components separate:

```text
alpha = (y_A / x_A) / (y_B / x_B)

y = vapor mole fraction, x = liquid mole fraction.
alpha >> 1  ->  easy to separate by distillation
alpha ~ 1   ->  hard: needs many stages (or another method)

The McCabe-Thiele method counts the ideal stages a column needs from
this equilibrium and the operating lines.
```

```mermaid
graph TD
    PROC["Any process"] --> FLOW["Fluid flow and mixing"]
    PROC --> HEAT["Heat transfer"]
    PROC --> SEP["Mass transfer and separation"]
    PROC --> SOLID["Particle and mechanical"]
    SEP --> DIST["Distillation"]
    SEP --> ABS["Absorption"]
    SEP --> EXT["Extraction"]
    SEP --> DRY["Drying"]
```

Remember: plants look endlessly varied, but they are assembled from the
same reusable unit operations. Learn the operation, not the recipe.
""",
        ),
        quiz_lesson(
            "Quiz: The unit-operations concept",
            (
                q(
                    "What is a unit operation?",
                    (
                        opt("A single chemical reaction"),
                        opt(
                            "A standard physical step (like distillation or heat "
                            "exchange) governed by the same principles regardless of the "
                            "chemical involved",
                            correct=True,
                        ),
                        opt("A department in a chemical company"),
                        opt("A unit of measurement for flow"),
                    ),
                    "Unit operations are the reusable physical building blocks of every process.",
                ),
                q(
                    "What is the difference between a unit operation and a unit process?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "A unit operation is a physical change; a unit process is the "
                            "chemical reaction",
                            correct=True,
                        ),
                        opt("A unit operation only happens in pharma"),
                        opt("A unit process involves no chemistry"),
                    ),
                    "Distillation is a unit operation (physical); oxidation is a unit "
                    "process (chemical).",
                ),
                q(
                    "For distillation, a relative volatility (alpha) far greater than 1 "
                    "means the two components are...",
                    (
                        opt("impossible to separate"),
                        opt("easy to separate, needing relatively few stages", correct=True),
                        opt("identical in every way"),
                        opt("always a solid"),
                    ),
                    "Large alpha means easy separation; alpha near 1 needs many stages "
                    "or another method.",
                ),
            ),
        ),
        # -- 5. Flow diagrams ------------------------------------------
        _t(
            "Process flow diagrams and block diagrams",
            "10 min",
            """# Process flow diagrams and block diagrams

Chemical engineers communicate a process visually, and they use a
**ladder of diagrams** that add detail as a design matures. Reading them
is a core literacy of the profession.

The three main levels:

- **Block Flow Diagram (BFD)** - the simplest view. Each major section is
  a labelled box, joined by arrows for the main streams. It shows the
  logic of the process at a glance, with almost no equipment detail. Ideal
  for explaining the concept.
- **Process Flow Diagram (PFD)** - the working engineering view. It shows
  the **major equipment** (reactors, columns, exchangers, pumps) with tag
  numbers, the main process streams, and a **stream table** listing flow,
  composition, temperature and pressure at each numbered point. This is
  the document engineers reason about daily.
- **Piping and Instrumentation Diagram (PID)** - the detailed build view.
  Every pipe, valve, instrument and control loop, following symbol
  standards such as **ISA-5.1**. Used to construct and operate the plant.

You move down the ladder as the design is confirmed: concept (BFD),
engineering (PFD), construction (PID). A tiny stream table attached to a
PFD looks like this:

```text
Stream            1 Feed    2 Rxn out   3 Product   4 Recycle
Flow (kg/h)       1000      1000        820         180
Temp (deg C)      25        250         40          40
Pressure (bar)    30        30          2           30
Mass frac prod    0.00      0.82        1.00        0.00
```

```mermaid
graph LR
    BFD["Block flow diagram concept"] --> PFD["Process flow diagram engineering"]
    PFD --> PID["Piping and instrumentation detail"]
    PID --> BUILD["Build and operate"]
```

Remember: BFD for the idea, PFD for the engineering (with its stream
table), PID for the build. Learn to read a PFD and you can hold an entire
process in your head.
""",
        ),
        quiz_lesson(
            "Quiz: Process flow diagrams and block diagrams",
            (
                q(
                    "Which diagram shows major equipment with tag numbers and a stream "
                    "table of flows, compositions, temperatures and pressures?",
                    (
                        opt("Block Flow Diagram (BFD)"),
                        opt("Process Flow Diagram (PFD)", correct=True),
                        opt("Piping and Instrumentation Diagram (PID)"),
                        opt("Organization chart"),
                    ),
                    "The PFD is the working engineering view, with equipment and a stream table.",
                ),
                q(
                    "What is a Block Flow Diagram best used for?",
                    (
                        opt("Specifying every valve and instrument"),
                        opt(
                            "Showing the overall logic of a process at a glance, each "
                            "section as a labelled box, with little equipment detail",
                            correct=True,
                        ),
                        opt("Listing employee names"),
                        opt("Recording maintenance schedules"),
                    ),
                    "A BFD conveys the concept simply; detail comes later in the PFD and PID.",
                ),
                q(
                    "As a design matures, in what order are these diagrams typically used?",
                    (
                        opt("PID, then PFD, then BFD"),
                        opt("BFD, then PFD, then PID", correct=True),
                        opt("PFD, then BFD, then PID"),
                        opt("They are all made simultaneously and identical"),
                    ),
                    "Concept (BFD) to engineering (PFD) to construction detail (PID).",
                ),
            ),
        ),
        # -- 6. Units and dimensions -----------------------------------
        _t(
            "Units, dimensions and engineering quantities",
            "10 min",
            """# Units, dimensions and engineering quantities

Every quantity a chemical engineer handles has a **dimension** (mass,
length, time, temperature, amount) and is expressed in **units**. Getting
units right is not bookkeeping - it is safety-critical. NASA lost the Mars
Climate Orbiter in 1999 because two teams mixed metric and imperial units.
In a plant, a units error can mean an overpressured vessel.

Core ideas:

- **SI base units** - the international standard: kilogram, metre, second,
  kelvin, mole, ampere. Derived units follow: force in newtons, pressure
  in pascals (1 Pa = 1 N/m^2), energy in joules, power in watts.
- **Dimensional homogeneity** - every term in a valid equation must have
  the same dimensions. If the two sides of your equation do not match
  dimensionally, the equation is wrong. This is a free error-check on any
  formula.
- **Unit conversion** - carry units through the calculation and cancel
  them like algebra; the units that survive tell you if you did it right.
- **The mole** - chemical engineers count molecules in **moles**, because
  reactions balance by moles, not by mass.

**Dimensionless numbers** are especially powerful: ratios with no units
that capture the physics of a situation and let results scale across
sizes. The **Reynolds number** predicts whether flow is laminar or
turbulent:

```python
# Reynolds number: rho*v*D / mu  (dimensionless)
rho = 1000.0     # density, kg/m^3   (water)
v   = 2.0        # velocity, m/s
D   = 0.05       # pipe diameter, m
mu  = 1.0e-3     # viscosity, Pa*s

Re = rho * v * D / mu
print(Re)                       # 100000.0
print("turbulent" if Re > 4000 else "laminar")   # turbulent
```

Other key ones: **Nusselt** (convective heat transfer), **Sherwood**
(mass transfer), **Prandtl** and **Schmidt**. They recur throughout the
transport courses.

```mermaid
graph TD
    QTY["Engineering quantity"] --> DIM["Dimension mass length time"]
    QTY --> UNIT["Units SI base and derived"]
    UNIT --> CHECK["Dimensional homogeneity check"]
    UNIT --> CONV["Unit conversion cancel like algebra"]
    DIM --> DIMLESS["Dimensionless numbers"]
    DIMLESS --> RE["Reynolds laminar or turbulent"]
```

Remember: track your units and check dimensional homogeneity every time.
It is the cheapest, most reliable error-catcher in engineering.
""",
        ),
        quiz_lesson(
            "Quiz: Units, dimensions and engineering quantities",
            (
                q(
                    "What does 'dimensional homogeneity' require of a valid equation?",
                    (
                        opt("That every term uses the metric system"),
                        opt(
                            "That every term has the same dimensions - if the sides do "
                            "not match dimensionally, the equation is wrong",
                            correct=True,
                        ),
                        opt("That the equation contains only whole numbers"),
                        opt("That all quantities are dimensionless"),
                    ),
                    "Matching dimensions on every term is a free, reliable check on any formula.",
                ),
                q(
                    "Why do chemical engineers count amounts in moles rather than only mass?",
                    (
                        opt("Moles are easier to weigh"),
                        opt(
                            "Chemical reactions balance by moles of molecules, not by mass",
                            correct=True,
                        ),
                        opt("Mass is not an SI quantity"),
                        opt("Moles have no dimension"),
                    ),
                    "Stoichiometry is a molecular count, so reactions are tracked in moles.",
                ),
                q(
                    "A pipe flow gives a Reynolds number of about 100000. What does that tell you?",
                    (
                        opt("The flow is laminar and smooth"),
                        opt("The flow is turbulent (Re well above ~4000)", correct=True),
                        opt("The fluid is a solid"),
                        opt("The pipe is empty"),
                    ),
                    "High Reynolds number means turbulent flow; low (below ~2000) means laminar.",
                ),
            ),
        ),
        # -- 7. Safety and sustainability ------------------------------
        _t(
            "The safety and sustainability mindset",
            "10 min",
            """# The safety and sustainability mindset

In chemical engineering, **safety and sustainability come first** - before
yield, before cost. Processes handle flammable, toxic and high-pressure
materials, and history is full of tragedies (Flixborough, Bhopal, Texas
City) that reshaped the profession. A good engineer treats hazard as a
design input, not an afterthought.

The most important principle is the **hierarchy of controls** - the order
in which you should address a hazard:

1. **Inherently safer design** - remove the hazard at the source. Use less
   hazardous material, hold a smaller inventory, run at milder conditions.
   The best-known slogan: *"what you do not have cannot leak."*
2. **Engineering controls** - if a hazard must exist, contain it: relief
   valves, interlocks, containment, ventilation.
3. **Administrative controls** - procedures, training, permits, alarms.
4. **Personal protective equipment (PPE)** - the last line, not the first.

Structured methods make hazards visible before they bite. **HAZOP**
(Hazard and Operability study) walks through a process asking "what if"
with guidewords (no flow, more pressure, less temperature) at every point.
**Layers of protection** (LOPA) then check that enough independent
safeguards exist.

Alongside safety, **sustainability** is now a core objective, guided by
the **twelve principles of green chemistry** and **green engineering**:
prevent waste rather than treat it, maximize **atom economy**, use safer
solvents, and design for energy efficiency. A key metric is the **E-factor**:

```text
E-factor = mass of waste / mass of product

Bulk chemicals   E-factor ~ 1 to 5
Pharmaceuticals  E-factor ~ 25 to 100+  (lots of solvent and steps)

Lower is greener. Process intensification and better catalysis cut it.
```

```mermaid
graph TD
    HAZARD["Hazard identified"] --> INH["Inherently safer design"]
    INH --> ENG["Engineering controls"]
    ENG --> ADMIN["Administrative controls"]
    ADMIN --> PPE["Personal protective equipment"]
    INH --> GREEN["Green principles prevent waste"]
    GREEN --> EFACT["Low E factor"]
```

Remember: address hazards at the source first and treat waste as a design
failure. The safest, greenest plant is the one that never needed the
hazard or the waste in the first place.
""",
        ),
        quiz_lesson(
            "Quiz: The safety and sustainability mindset",
            (
                q(
                    "What sits at the top of the hierarchy of controls - the most "
                    "preferred way to deal with a hazard?",
                    (
                        opt("Personal protective equipment"),
                        opt("Written procedures and training"),
                        opt(
                            "Inherently safer design - removing or reducing the hazard at "
                            "the source",
                            correct=True,
                        ),
                        opt("Relief valves and interlocks"),
                    ),
                    "What you do not have cannot leak; eliminate the hazard first, PPE "
                    "is the last resort.",
                ),
                q(
                    "What is a HAZOP study?",
                    (
                        opt("A financial audit of the plant"),
                        opt(
                            "A structured 'what if' walkthrough of a process using "
                            "guidewords to find hazards and operability problems",
                            correct=True,
                        ),
                        opt("A marketing analysis"),
                        opt("A type of pressure relief valve"),
                    ),
                    "HAZOP systematically applies guidewords (no flow, more pressure) at "
                    "each point to surface hazards.",
                ),
                q(
                    "A process has an E-factor of 80. What does that indicate?",
                    (
                        opt("It produces 80 times more product than waste"),
                        opt(
                            "It produces 80 kg of waste per kg of product - typical of "
                            "pharma and a target for improvement",
                            correct=True,
                        ),
                        opt("It uses 80 percent renewable energy"),
                        opt("It is the safest possible process"),
                    ),
                    "E-factor is waste mass per product mass; lower is greener, and "
                    "pharma processes are notoriously high.",
                ),
            ),
        ),
        # -- 8. The modern chemical engineer ---------------------------
        _t(
            "The modern chemical engineer",
            "11 min",
            """# The modern chemical engineer

The fundamentals do not change, but the **tools** have been transformed.
Today's chemical engineer works as much with **software, data and AI** as
with pumps and columns. This is the frontier the rest of your studies
prepare you for.

**Process simulation** is now universal. Instead of solving balances by
hand, engineers build a digital model of the whole plant in tools like
**Aspen Plus / HYSYS** or the open-source **DWSIM**, and ask "what if?"
before touching any steel. You specify feeds and equipment; the simulator
solves the mass and energy balances and thermodynamics for the entire
flowsheet.

Four shifts define the modern practice:

- **Machine learning for optimization** - plants generate oceans of sensor
  data. ML models learn to predict yield, energy use or product quality
  and then tune operating conditions in real time - often beating
  hand-tuned setpoints. **Soft sensors** infer hard-to-measure properties
  from easy ones.
- **Digital twins and Industry 4.0** - a live simulation mirrors the real
  plant, fed by its sensors, used to test changes, train operators and do
  **predictive maintenance** (fix a pump before it fails). This is the
  "smart plant" of Industry 4.0.
- **Molecular and drug discovery** - AI now accelerates the chemistry
  itself: **cheminformatics** and **QSAR** models predict properties from
  structure, **molecular docking** screens drug candidates, **generative
  models** invent new molecules, and **AlphaFold-style** models predict
  protein structures that once took years to determine.
- **ML property prediction** - fast surrogate models estimate physical
  properties, reaction rates and phase behaviour in a fraction of the time
  a rigorous simulation takes, so engineers can explore far more designs.

A tiny taste of the data-driven workflow, fitting a model that predicts
reactor yield from temperature and pressure:

```python
# fit a surrogate model of yield from process data
import numpy as np
from sklearn.linear_model import LinearRegression

# columns: temperature (deg C), pressure (bar)
X = np.array([[220, 28], [250, 30], [265, 30], [280, 32]])
y = np.array([0.71, 0.82, 0.85, 0.83])   # measured yield fraction

model = LinearRegression().fit(X, y)
print(model.predict([[260, 30]]))         # predicted yield at new setpoint
```

Underlying it all remains the same engineer's judgement: a model is only
as good as the physics and data behind it. AI is a powerful tool on top of
the fundamentals - not a replacement for them.

```mermaid
graph TD
    PLANT["Physical plant with sensors"] --> DATA["Process data"]
    DATA --> ML["Machine learning optimization"]
    DATA --> TWIN["Digital twin"]
    TWIN --> MAINT["Predictive maintenance"]
    ML --> CONTROL["Real time setpoint tuning"]
    SIM["Process simulation Aspen and DWSIM"] --> TWIN
    AICHEM["AI for molecules"] --> DISCOVERY["Drug and materials discovery"]
```

Remember: simulation, data and AI multiply what a chemical engineer can
do - but they sit on top of mass balances, thermodynamics and transport,
which is exactly why this course starts there.
""",
        ),
        quiz_lesson(
            "Quiz: The modern chemical engineer",
            (
                q(
                    "What does a process simulator like Aspen Plus, HYSYS or DWSIM do?",
                    (
                        opt("It physically builds the plant"),
                        opt(
                            "It builds a digital model of the flowsheet and solves the "
                            "mass, energy and thermodynamic balances so you can ask 'what "
                            "if' before building",
                            correct=True,
                        ),
                        opt("It replaces the need for any engineer"),
                        opt("It only draws logos"),
                    ),
                    "Simulators solve the whole flowsheet in software, letting engineers "
                    "test designs before touching steel.",
                ),
                q(
                    "What is a 'digital twin' of a plant?",
                    (
                        opt("A backup copy of the accounting system"),
                        opt(
                            "A live simulation mirroring the real plant, fed by its "
                            "sensors, used to test changes and predict maintenance",
                            correct=True,
                        ),
                        opt("A second identical physical plant next door"),
                        opt("A photograph of the control room"),
                    ),
                    "A digital twin is a live, sensor-fed model - a pillar of Industry "
                    "4.0 and predictive maintenance.",
                ),
                q(
                    "Which of these is an example of AI accelerating chemistry and drug discovery?",
                    (
                        opt("Painting the storage tanks"),
                        opt(
                            "QSAR property prediction, molecular docking, generative "
                            "molecule design and AlphaFold-style protein structure "
                            "prediction",
                            correct=True,
                        ),
                        opt("Manually distilling a sample overnight"),
                        opt("Replacing all thermodynamics with guesswork"),
                    ),
                    "Cheminformatics, QSAR, docking, generative models and protein-"
                    "structure prediction speed up discovery itself.",
                ),
                q(
                    "What is the right way to think about AI in chemical engineering?",
                    (
                        opt("It replaces the fundamentals entirely"),
                        opt(
                            "It is a powerful tool built on top of mass balances, "
                            "thermodynamics and transport - a model is only as good as "
                            "the physics and data behind it",
                            correct=True,
                        ),
                        opt("It makes safety analysis unnecessary"),
                        opt("It only matters for marketing"),
                    ),
                    "AI multiplies what an engineer can do but rests on - and requires - "
                    "the fundamentals.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what does a chemical engineer do?",
                    (
                        opt("Only discovers reactions at the bench"),
                        opt(
                            "Designs, builds and operates the processes that turn raw "
                            "materials into useful products at scale, safely and "
                            "economically",
                            correct=True,
                        ),
                        opt("Only writes safety regulations"),
                        opt("Only sells chemicals"),
                    ),
                    "The engineer scales chemistry into safe, economic, real-world production.",
                ),
                q(
                    "What tool underlies nearly every chemical engineering calculation?",
                    (
                        opt("A stock ticker"),
                        opt(
                            "The mass and energy balance - what goes in must come out or "
                            "accumulate",
                            correct=True,
                        ),
                        opt("A random-number generator"),
                        opt("A dictionary"),
                    ),
                    "Conservation of mass and energy is the constant companion of the field.",
                ),
                q(
                    "Which correctly contrasts petrochemical and pharmaceutical manufacturing?",
                    (
                        opt("Both are low-volume batch processes"),
                        opt(
                            "Petrochemical is high-volume, low-value, continuous; pharma "
                            "is low-volume, high-value, batch under GMP",
                            correct=True,
                        ),
                        opt("Both avoid all regulation"),
                        opt("Pharma is cheaper per kilogram than fuel"),
                    ),
                    "Volume versus value and continuous versus batch separate the "
                    "sectors, though the fundamentals are shared.",
                ),
                q(
                    "What are the three broad stages of almost every chemical process?",
                    (
                        opt("Buy, store, sell"),
                        opt(
                            "Feed preparation, reaction, and separation or purification "
                            "(often with a recycle)",
                            correct=True,
                        ),
                        opt("Heat, cool, freeze"),
                        opt("Plan, code, deploy"),
                    ),
                    "Prepare, react, separate - with recycle turning modest conversion "
                    "into high overall efficiency.",
                ),
                q(
                    "What is the unit-operations concept?",
                    (
                        opt("A rule that every plant needs exactly one operation"),
                        opt(
                            "The idea that any process is built from a small library of "
                            "standard physical steps, each governed by the same "
                            "principles regardless of the chemical",
                            correct=True,
                        ),
                        opt("A department that runs the plant"),
                        opt("A single reaction repeated forever"),
                    ),
                    "Learn the operation (distillation, heat exchange) once and reuse it "
                    "across every industry.",
                ),
                q(
                    "Which diagram carries a stream table of flows, compositions, "
                    "temperatures and pressures for the major equipment?",
                    (
                        opt("Block Flow Diagram"),
                        opt("Process Flow Diagram", correct=True),
                        opt("Organization chart"),
                        opt("Gantt chart"),
                    ),
                    "The PFD is the working engineering view; the BFD is the concept and "
                    "the PID is the build detail.",
                ),
                q(
                    "Why does checking dimensional homogeneity matter?",
                    (
                        opt("It makes equations look longer"),
                        opt(
                            "If the terms of an equation do not share the same "
                            "dimensions, the equation is wrong - it is a free error "
                            "check",
                            correct=True,
                        ),
                        opt("It converts all units to imperial"),
                        opt("It is only needed in accounting"),
                    ),
                    "Matching dimensions catches errors cheaply - the Mars Climate "
                    "Orbiter was lost to a units mix-up.",
                ),
                q(
                    "What does the Reynolds number predict?",
                    (
                        opt("The price of crude oil"),
                        opt(
                            "Whether flow is laminar or turbulent, from density, "
                            "velocity, diameter and viscosity",
                            correct=True,
                        ),
                        opt("The colour of a solution"),
                        opt("The age of a reactor"),
                    ),
                    "It is a dimensionless ratio; above roughly 4000 flow is turbulent, "
                    "below about 2000 it is laminar.",
                ),
                q(
                    "In the hierarchy of controls, what should you try first?",
                    (
                        opt("Hand out personal protective equipment"),
                        opt("Write more procedures"),
                        opt(
                            "Inherently safer design - remove or reduce the hazard at its source",
                            correct=True,
                        ),
                        opt("Add more alarms only"),
                    ),
                    "Eliminate the hazard first; PPE is the last line of defence, not the first.",
                ),
                q(
                    "How should AI, simulation and data be viewed in modern chemical engineering?",
                    (
                        opt("As a replacement for the fundamentals"),
                        opt(
                            "As powerful tools built on top of mass balances, "
                            "thermodynamics and transport - a model is only as good as "
                            "the physics and data behind it",
                            correct=True,
                        ),
                        opt("As useful only for the pharmaceutical sector"),
                        opt("As a way to skip safety analysis"),
                    ),
                    "Digital twins, ML optimization and molecular AI multiply the "
                    "engineer's reach but rest on the fundamentals.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

INTRO_CHEMICAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_INTRO_CHEMICAL_ENGINEERING,)
