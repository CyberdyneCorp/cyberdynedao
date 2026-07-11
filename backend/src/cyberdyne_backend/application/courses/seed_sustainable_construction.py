"""Academy seed content - Sustainable Construction and Decarbonization.

An advanced civil-engineering course on building for a low-carbon, resilient
future. It covers sustainability principles, energy and water efficiency,
low-carbon materials and embodied carbon, life-cycle assessment, circularity
and construction waste, green certifications, climate resilience, and
net-zero pathways for infrastructure. Every lesson is a direct explanation
with a worked carbon or LCA calculation and a mermaid diagram, followed by a
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


_SUSTAINABLE_CONSTRUCTION = SeedCourse(
    slug="sustainable-construction",
    title="Sustainable Construction & Decarbonization",
    description=(
        "Building for a low-carbon, resilient future: energy and water "
        "efficiency, low-carbon materials, life-cycle assessment, circularity "
        "and net-zero pathways for infrastructure - grounded in real standards "
        "(EN 15978, ISO 14040, LEED, AQUA-HQE) with worked carbon and LCA "
        "calculations and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Sustainable Construction and Decarbonization

The built environment is responsible for roughly **37 percent of global
energy-related CO2 emissions** - split between the **operational** carbon
of running buildings and the **embodied** carbon locked into their
materials. Decarbonizing construction is therefore one of the highest
-leverage moves available to civil engineers. This course teaches how.

The approach is **quantitative and concrete**: every lesson explains one
idea directly, shows a worked carbon or life-cycle calculation you can
reproduce, and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Sustainability principles** - the three pillars applied to civil works
2. **Energy and water efficiency** - passive design, EUI, WUE
3. **Low-carbon materials** - embodied carbon and how to cut it
4. **Life-cycle assessment (LCA)** - EN 15978 stages A to D
5. **Circular economy** - designing out construction and demolition waste
6. **Green certifications** - LEED and AQUA-HQE, what they reward
7. **Climate resilience** - adapting infrastructure to a changing climate
8. **Net-zero pathways** - reducing, then offsetting residual carbon

Standards referenced include **ISO 14040/44**, **EN 15978** and **EN
15804** for LCA, **ABNT NBR 15575** for building performance, plus **LEED**
and **AQUA-HQE**. The goal is not certification trivia but the engineering
judgment to design and defend a low-carbon project.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "The built environment is responsible for roughly what share of "
                    "global energy-related CO2 emissions?",
                    (
                        opt("About 5 percent"),
                        opt("About 37 percent", correct=True),
                        opt("About 75 percent"),
                        opt("About 95 percent"),
                    ),
                    "Buildings and construction account for around 37 percent of "
                    "energy-related CO2, split between operational and embodied carbon.",
                ),
                q(
                    "What is the difference between operational and embodied carbon?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "Operational carbon comes from running the building (energy, "
                            "water); embodied carbon is locked into the materials and "
                            "construction process",
                            correct=True,
                        ),
                        opt("Operational carbon only applies to bridges"),
                        opt("Embodied carbon is emitted only after demolition"),
                    ),
                    "Operational = in-use energy and water; embodied = extraction, "
                    "manufacture, transport, construction, and end of life of materials.",
                ),
            ),
        ),
        # -- 1. Sustainability principles ------------------------------
        _t(
            "Sustainability principles in civil works",
            "9 min",
            """# Sustainability principles in civil works

**Sustainable construction** means meeting present needs without
compromising the ability of future generations to meet theirs. In practice
it balances **three pillars** - often called the triple bottom line:

- **Environmental** - minimize carbon, resource use, pollution, and habitat
  loss across the whole life of the asset.
- **Social** - safety, health, comfort, accessibility, and fair labor for
  the people who build and use the works.
- **Economic** - deliver value across the life cycle, not just the lowest
  bid on day one. Cheap to build can be expensive to run.

A recurring trap is **first cost tunnel vision**. A sustainable design is
judged on **life-cycle cost** and **life-cycle carbon**, where a higher
capital cost is often repaid many times over in operation.

The discipline is to apply the **reduction hierarchy** in order - avoid
demand first, then be efficient, then supply what remains cleanly, and only
then offset. This ordering matters: an unbuilt lane or an avoided tonne of
concrete is always cheaper and cleaner than a green version of it.

```mermaid
graph TD
    NEED["Project need"] --> AVOID["Avoid demand first"]
    AVOID --> EFF["Improve efficiency"]
    EFF --> CLEAN["Supply cleanly"]
    CLEAN --> OFFSET["Offset residual only"]
    ENV["Environmental"] --> TBL["Triple bottom line"]
    SOC["Social"] --> TBL
    ECON["Economic"] --> TBL
```

A simple **life-cycle cost** comparison shows why first cost misleads. Two
pump options for a water utility, over a 25 year life at a 6 percent
discount rate:

```text
Life-cycle cost = Capital + Present value of running costs

Option A (standard pump)
  Capital            = 100,000
  Annual energy      =  30,000 / yr
  PV factor (6%,25y) =  12.78
  PV of energy       =  30,000 x 12.78 = 383,400
  Life-cycle cost    = 100,000 + 383,400 = 483,400

Option B (efficient pump)
  Capital            = 140,000
  Annual energy      =  20,000 / yr
  PV of energy       =  20,000 x 12.78 = 255,600
  Life-cycle cost    = 140,000 + 255,600 = 395,600

Result: Option B costs 40,000 more up front but saves ~87,800 over life.
```

Remember: sustainability is not one green feature bolted on - it is
optimizing the whole system across its whole life against all three pillars.
""",
        ),
        quiz_lesson(
            "Quiz: Sustainability principles in civil works",
            (
                q(
                    "What are the three pillars of sustainable construction?",
                    (
                        opt("Steel, concrete, and timber"),
                        opt("Environmental, social, and economic", correct=True),
                        opt("Design, build, and demolish"),
                        opt("Water, energy, and waste"),
                    ),
                    "The triple bottom line: environmental, social, and economic value "
                    "considered together across the asset's life.",
                ),
                q(
                    "Why is 'first cost tunnel vision' a trap in sustainable design?",
                    (
                        opt("First cost is impossible to estimate"),
                        opt(
                            "A design cheap to build can be expensive to run; decisions "
                            "should use life-cycle cost and carbon, not day-one capital "
                            "cost alone",
                            correct=True,
                        ),
                        opt("First cost is always higher for green options"),
                        opt("Regulations forbid estimating first cost"),
                    ),
                    "In the worked example the efficient pump cost more up front but was "
                    "far cheaper over its 25 year life.",
                ),
                q(
                    "What is the correct order of the reduction hierarchy?",
                    (
                        opt("Offset, then supply cleanly, then be efficient, then avoid"),
                        opt(
                            "Avoid demand, then improve efficiency, then supply cleanly, "
                            "then offset the residual",
                            correct=True,
                        ),
                        opt("Offset everything, then build normally"),
                        opt("Supply cleanly first, avoiding is unnecessary"),
                    ),
                    "Avoided demand is always cheaper and cleaner than a green version of "
                    "the same demand; offsetting is the last resort.",
                ),
            ),
        ),
        # -- 2. Energy and water efficiency ----------------------------
        _t(
            "Energy and water efficiency",
            "10 min",
            """# Energy and water efficiency

Operational carbon is driven by how much **energy and water** an asset
consumes in use. The cheapest, cleanest unit is the one you never need, so
efficiency starts with **passive design** before any equipment is sized.

**Passive strategies** (little or no running energy):

- **Orientation and shading** - control solar gain; overhangs sized for the
  sun path cut cooling load.
- **Envelope** - insulation, airtightness, and thermal mass reduce heating
  and cooling demand.
- **Daylight and natural ventilation** - displace electric lighting and
  mechanical cooling where climate allows.

Then **active efficiency**: high-efficiency HVAC, LED lighting, heat
recovery, variable-speed drives, and controls. The headline metric is
**Energy Use Intensity (EUI)** - annual energy per unit floor area, in
kWh per square metre per year. Lower is better, and it lets you benchmark
very different buildings on one number.

Water follows the same logic. **Water efficiency** combines low-flow
fixtures, leak detection, rainwater harvesting, and greywater reuse. In
data centres and industry the analogous ratio is **Water Use Efficiency
(WUE)**.

```mermaid
graph LR
    DEMAND["Reduce demand"] --> PASSIVE["Passive design"]
    PASSIVE --> ACTIVE["Efficient systems"]
    ACTIVE --> METER["Meter and benchmark"]
    METER --> EUI["Energy use intensity"]
    METER --> WUE["Water use intensity"]
    EUI --> IMPROVE["Target and improve"]
    WUE --> IMPROVE
```

A worked **EUI** and operational-carbon estimate for an office:

```text
Given:
  Gross floor area          = 5,000 m2
  Annual electricity        = 450,000 kWh
  Annual gas (heating)      = 300,000 kWh
  Grid emission factor      = 0.20 kg CO2 / kWh
  Gas emission factor       = 0.18 kg CO2 / kWh

EUI = total energy / floor area
    = (450,000 + 300,000) kWh / 5,000 m2
    = 150 kWh / m2 / yr

Operational carbon (per year):
  Electricity = 450,000 x 0.20 = 90,000 kg CO2
  Gas         = 300,000 x 0.18 = 54,000 kg CO2
  Total       = 144,000 kg CO2 = 144 t CO2 / yr

Carbon intensity = 144,000 / 5,000 = 28.8 kg CO2 / m2 / yr
```

Remember: reduce demand with passive design first, make what remains
efficient, and manage by metering - you cannot improve what you do not
measure.
""",
        ),
        quiz_lesson(
            "Quiz: Energy and water efficiency",
            (
                q(
                    "What does Energy Use Intensity (EUI) measure?",
                    (
                        opt("The peak power draw of the largest motor"),
                        opt(
                            "Annual energy consumption per unit of floor area, letting "
                            "different buildings be benchmarked on one number",
                            correct=True,
                        ),
                        opt("The number of light fittings per room"),
                        opt("The embodied carbon of the structure"),
                    ),
                    "EUI is kWh per square metre per year - an operational, not embodied, "
                    "metric, and lower is better.",
                ),
                q(
                    "Why does efficient design start with passive strategies?",
                    (
                        opt("Passive strategies are required by law everywhere"),
                        opt(
                            "The cheapest and cleanest unit of energy is the one you never "
                            "need, so reducing demand comes before sizing equipment",
                            correct=True,
                        ),
                        opt("Active systems never save energy"),
                        opt("Passive design has no capital cost"),
                    ),
                    "Orientation, envelope, daylight, and natural ventilation cut demand "
                    "before any active system is added.",
                ),
                q(
                    "Using 450,000 kWh electricity at 0.20 kg CO2/kWh, what is the "
                    "annual electricity carbon?",
                    (
                        opt("9,000 kg CO2"),
                        opt("90,000 kg CO2", correct=True),
                        opt("450,000 kg CO2"),
                        opt("2,250 kg CO2"),
                    ),
                    "450,000 x 0.20 = 90,000 kg CO2 per year from electricity.",
                ),
            ),
        ),
        # -- 3. Low-carbon materials -----------------------------------
        _t(
            "Low-carbon materials and embodied carbon",
            "11 min",
            """# Low-carbon materials and embodied carbon

**Embodied carbon** is the greenhouse gas emitted to produce, transport,
build, maintain, and eventually dispose of the materials in an asset. It is
front-loaded - most is emitted **before the building opens** - which makes
it urgent, because you cannot recover it later.

The dominant contributors in most projects are **concrete and steel**.
Cement clinker alone is responsible for around **8 percent of global CO2**,
because producing clinker both burns fuel and releases CO2 chemically when
limestone is calcined.

Each material carries an **embodied carbon factor**, usually in kg CO2e per
kg or per m3, published in an **Environmental Product Declaration (EPD)**
that follows **EN 15804**. Typical order-of-magnitude values:

```text
Approximate embodied carbon (A1-A3, cradle to gate):
  Portland cement (CEM I) concrete   ~ 300 kg CO2e / m3
  Concrete with 50% GGBS replacement ~ 190 kg CO2e / m3
  Structural steel (virgin)          ~ 2.5 kg CO2e / kg
  Structural steel (recycled EAF)    ~ 1.0 kg CO2e / kg
  Sawn structural timber             ~ 0.4 kg CO2e / kg (stores biogenic C)
```

Strategies to cut embodied carbon, roughly in order of impact:

- **Build less** - reuse or refurbish existing structure; optimize spans.
- **Substitute cement** - replace clinker with **GGBS** (slag) or **fly
  ash** supplementary cementitious materials.
- **Use lower-carbon and bio-based materials** - timber, which also stores
  biogenic carbon, where structurally appropriate.
- **Specify recycled content** - electric-arc-furnace steel, recycled
  aggregate.
- **Right-size** - do not over-design; every unnecessary cubic metre of
  concrete has a carbon cost.

```mermaid
graph LR
    QTY["Material quantities"] --> EPD["Embodied carbon factors from EPD"]
    EPD --> SUM["Sum mass times factor"]
    SUM --> HOT["Find carbon hotspots"]
    HOT --> LESS["Build less"]
    HOT --> SUB["Substitute cement"]
    HOT --> BIO["Use bio based materials"]
```

A worked **embodied carbon** comparison for a floor slab needing 200 m3 of
concrete:

```text
Embodied carbon = Volume x carbon factor

Baseline (CEM I concrete):
  200 m3 x 300 kg CO2e/m3 = 60,000 kg CO2e = 60 t CO2e

Low-carbon mix (50% GGBS):
  200 m3 x 190 kg CO2e/m3 = 38,000 kg CO2e = 38 t CO2e

Saving = 60 - 38 = 22 t CO2e, a 37% reduction, same slab.
```

Remember: embodied carbon is spent up front and cannot be clawed back -
design it out early, because the cheapest tonne is the one never poured.
""",
        ),
        quiz_lesson(
            "Quiz: Low-carbon materials and embodied carbon",
            (
                q(
                    "Why is embodied carbon described as 'front-loaded' and urgent?",
                    (
                        opt("It is only emitted after 50 years of use"),
                        opt(
                            "Most of it is emitted before the building opens, during "
                            "material production and construction, so it cannot be "
                            "recovered later",
                            correct=True,
                        ),
                        opt("It only matters for temporary structures"),
                        opt("It can always be offset for free"),
                    ),
                    "Unlike operational carbon spread over decades, embodied carbon is "
                    "largely spent up front - design it out early.",
                ),
                q(
                    "How can the embodied carbon of concrete be reduced?",
                    (
                        opt("By pouring more of it"),
                        opt(
                            "By replacing part of the Portland cement clinker with "
                            "supplementary cementitious materials such as GGBS or fly ash",
                            correct=True,
                        ),
                        opt("By curing it faster only"),
                        opt("By painting the finished surface"),
                    ),
                    "Clinker is the carbon-intensive part; slag and fly ash substitution "
                    "cut it substantially, as shown by the slab example.",
                ),
                q(
                    "For 200 m3 of concrete, switching from 300 to 190 kg CO2e/m3 saves "
                    "roughly how much?",
                    (
                        opt("About 2 t CO2e"),
                        opt("About 22 t CO2e", correct=True),
                        opt("About 60 t CO2e"),
                        opt("Nothing, it is the same mix"),
                    ),
                    "200 x (300 - 190) = 22,000 kg = 22 t CO2e, a 37 percent reduction.",
                ),
            ),
        ),
        # -- 4. Life-cycle assessment ----------------------------------
        _t(
            "Life-cycle assessment (LCA)",
            "11 min",
            """# Life-cycle assessment (LCA)

**Life-cycle assessment (LCA)** quantifies the environmental impact of an
asset across its **whole life**, so decisions are not made by shifting a
burden from one stage to another. It is standardized by **ISO 14040 and
14044**, and for buildings by **EN 15978** (with product-level rules in
EN 15804).

An LCA has **four phases** (ISO 14040):

1. **Goal and scope** - what is assessed, the boundary, and the
   **functional unit** (e.g. "one square metre of wall over 60 years").
2. **Inventory analysis (LCI)** - tally all inputs and outputs: energy,
   materials, emissions.
3. **Impact assessment (LCIA)** - translate the inventory into impacts, the
   headline usually being **Global Warming Potential** in kg CO2e.
4. **Interpretation** - find hotspots, test assumptions, draw conclusions.

**EN 15978** divides a building's life into **modules A to D**:

```text
A1-A3  Product      raw material supply, transport, manufacture
A4-A5  Construction transport to site, installation
B1-B7  Use          use, maintenance, repair, replacement, operational
                    energy (B6) and water (B7)
C1-C4  End of life   deconstruction, transport, waste processing, disposal
D      Beyond        reuse, recovery, recycling benefits and loads
```

A **cradle-to-gate** study covers A1-A3 only; **cradle-to-grave** covers A
to C; adding **Module D** gives the full circular picture. Choosing the
boundary honestly is essential - a small A1-A3 number can hide a large
maintenance (B) or disposal (C) burden.

```mermaid
graph LR
    GOAL["Goal and scope"] --> LCI["Inventory analysis"]
    LCI --> LCIA["Impact assessment"]
    LCIA --> INTERP["Interpretation"]
    A["A product and construction"] --> WHOLE["Whole life GWP"]
    B["B use stage"] --> WHOLE
    C["C end of life"] --> WHOLE
    D["D beyond boundary"] --> WHOLE
```

A worked **whole-life carbon** roll-up for one square metre of an external
wall over a 60 year study period, per functional unit:

```text
Functional unit: 1 m2 of wall, 60 year reference study period

  A1-A3  Product manufacture        =  120 kg CO2e
  A4-A5  Transport and install      =   15 kg CO2e
  B4     Replace cladding once      =   40 kg CO2e
  C1-C4  End of life                =   10 kg CO2e
  ------------------------------------------------
  Whole-life embodied (A to C)      =  185 kg CO2e / m2

  D      Recycling credit           =  -25 kg CO2e  (reported separately)

Net with Module D                   =  160 kg CO2e / m2
```

Remember: LCA stops you from "winning" one stage while losing overall -
pick a functional unit, set an honest boundary, and add up the whole life.
""",
        ),
        quiz_lesson(
            "Quiz: Life-cycle assessment (LCA)",
            (
                q(
                    "What are the four phases of an ISO 14040 LCA?",
                    (
                        opt("Design, tender, build, demolish"),
                        opt(
                            "Goal and scope, inventory analysis, impact assessment, interpretation",
                            correct=True,
                        ),
                        opt("Reduce, reuse, recycle, recover"),
                        opt("Plan, do, check, act"),
                    ),
                    "Goal and scope -> LCI -> LCIA -> interpretation, per ISO 14040/44.",
                ),
                q(
                    "In EN 15978, what do modules A1-A3 cover?",
                    (
                        opt("The use stage energy and water"),
                        opt("End-of-life demolition and disposal"),
                        opt(
                            "The product stage: raw material supply, transport, and "
                            "manufacture (cradle to gate)",
                            correct=True,
                        ),
                        opt("Benefits beyond the system boundary"),
                    ),
                    "A1-A3 is the product/cradle-to-gate stage; B is use, C is end of "
                    "life, and D is beyond the boundary.",
                ),
                q(
                    "Why must an LCA define a functional unit and boundary?",
                    (
                        opt("To make the report longer"),
                        opt(
                            "So results are comparable and you cannot 'win' one stage "
                            "while hiding a larger burden in another",
                            correct=True,
                        ),
                        opt("Because ISO forbids using kg CO2e"),
                        opt("To avoid measuring the use stage"),
                    ),
                    "A small A1-A3 figure can conceal a large B or C burden; an honest "
                    "boundary and functional unit prevent burden shifting.",
                ),
            ),
        ),
        # -- 5. Circular economy ---------------------------------------
        _t(
            "Circular economy and construction waste",
            "10 min",
            """# Circular economy and construction waste

Construction is the largest waste stream in most economies - **construction
and demolition (CandD) waste** is often a third or more of all waste by
mass. The **linear model** (take, make, dispose) treats materials as
disposable; the **circular economy** keeps them in use at their highest
value for as long as possible.

The **waste hierarchy** ranks options from best to worst:

```text
Best  ->  Prevent      design out waste; build less
          Reuse        reuse components and whole elements
          Recycle      reprocess into new material
          Recover      energy from waste
Worst ->  Dispose      landfill
```

Circular design principles for civil works:

- **Design for adaptability** - long-life, loose-fit structures that can
  change use without demolition.
- **Design for disassembly (DfD)** - bolted and reversible connections
  instead of chemical bonds, so elements can be recovered intact.
- **Material passports** - a record of what is in the building and how to
  recover it, turning the asset into a future **material bank**.
- **Specify recycled and reused content**, and divert site waste from
  landfill.

```mermaid
graph TD
    LINEAR["Take make dispose"] --> PROBLEM["Waste and lost value"]
    CIRCULAR["Circular economy"] --> PREVENT["Prevent"]
    CIRCULAR --> REUSE["Reuse elements"]
    CIRCULAR --> RECYCLE["Recycle materials"]
    REUSE --> BANK["Building as material bank"]
    DFD["Design for disassembly"] --> REUSE
    PASSPORT["Material passport"] --> BANK
```

A worked **waste diversion rate** for a demolition project:

```text
Diversion rate = mass diverted from landfill / total waste x 100

Total CandD waste generated   = 2,000 t
  Reused on site (crushed fill) =   900 t
  Recycled off site (metals)    =   700 t
  Sent to landfill              =   400 t

Diverted = 900 + 700 = 1,600 t
Diversion rate = 1,600 / 2,000 x 100 = 80%

A 80% diversion rate is a common green-certification threshold.
```

Remember: the greenest material is the one already in service - keep
elements in use at their highest value, and design today's building to be
tomorrow's material bank.
""",
        ),
        quiz_lesson(
            "Quiz: Circular economy and construction waste",
            (
                q(
                    "What is the order of the waste hierarchy from best to worst?",
                    (
                        opt("Dispose, recover, recycle, reuse, prevent"),
                        opt("Prevent, reuse, recycle, recover, dispose", correct=True),
                        opt("Recycle, prevent, dispose, reuse, recover"),
                        opt("Reuse, dispose, prevent, recycle, recover"),
                    ),
                    "Prevention is best; landfill disposal is the last resort.",
                ),
                q(
                    "What does 'design for disassembly' (DfD) enable?",
                    (
                        opt("Faster concrete curing"),
                        opt(
                            "Recovering components intact at end of life by using "
                            "reversible connections instead of permanent bonds",
                            correct=True,
                        ),
                        opt("Higher embodied carbon"),
                        opt("Eliminating the need for any structure"),
                    ),
                    "Bolted, reversible connections let elements be reused, supporting the "
                    "building-as-material-bank idea.",
                ),
                q(
                    "If 1,600 t of 2,000 t of waste is kept out of landfill, the "
                    "diversion rate is:",
                    (
                        opt("20 percent"),
                        opt("80 percent", correct=True),
                        opt("160 percent"),
                        opt("40 percent"),
                    ),
                    "1,600 / 2,000 x 100 = 80 percent, a common certification threshold.",
                ),
            ),
        ),
        # -- 6. Green building certifications --------------------------
        _t(
            "Green building certifications (LEED, AQUA)",
            "10 min",
            """# Green building certifications (LEED, AQUA)

**Green building certifications** are third-party rating systems that turn
"sustainable" from a claim into a **verified, comparable score**. They set
credit categories, award points for meeting them, and certify the building
at a level. The main schemes an engineer meets are **LEED** (US Green
Building Council, global), **BREEAM** (UK, Europe), and **AQUA-HQE** - the
Brazilian adaptation of the French **HQE** standard, run by Fundacao Vanzolini.

**LEED** awards points across categories - Location and Transport,
Sustainable Sites, Water Efficiency, **Energy and Atmosphere** (the largest
weighting), Materials and Resources, Indoor Environmental Quality, and
Innovation. The total maps to a **certification level**:

```text
LEED certification thresholds (100 base points):
  Certified   40 - 49 points
  Silver      50 - 59 points
  Gold        60 - 79 points
  Platinum    80+  points
```

**AQUA-HQE** organizes performance into **14 categories** grouped under
site, construction, management, and comfort/health, each rated Good,
Superior, or Excellent, and audited at each phase of the project (program,
design, and construction). It is tailored to the Brazilian climate and
regulatory context (aligned with **ABNT NBR 15575** performance
requirements).

The value of certification: it forces **integrated design** early, gives
clients and markets a trusted label, and makes performance measurable. The
risk: chasing points ("greenwashing by checklist") instead of real
outcomes - the score is a means, not the goal.

```mermaid
graph TD
    CATS["Credit categories"] --> ENERGY["Energy and atmosphere"]
    CATS --> WATER["Water efficiency"]
    CATS --> MAT["Materials and resources"]
    CATS --> IEQ["Indoor environmental quality"]
    ENERGY --> POINTS["Award points"]
    WATER --> POINTS
    MAT --> POINTS
    IEQ --> POINTS
    POINTS --> LEVEL["Certification level"]
```

A worked **LEED level** determination:

```text
Points earned by category:
  Location and Transport        =  12
  Sustainable Sites             =   8
  Water Efficiency              =   9
  Energy and Atmosphere         =  24
  Materials and Resources       =   8
  Indoor Environmental Quality  =   4
  Innovation and Regional       =   2
  ------------------------------------
  Total                         =  67 points

67 points falls in the 60 to 79 band  ->  LEED Gold.
```

Remember: certifications verify and compare sustainability, but the points
are a proxy - design for the real outcome and let the rating follow.
""",
        ),
        quiz_lesson(
            "Quiz: Green building certifications (LEED, AQUA)",
            (
                q(
                    "What is AQUA-HQE?",
                    (
                        opt("A type of low-carbon cement"),
                        opt(
                            "The Brazilian adaptation of the French HQE green-building "
                            "certification, tailored to local climate and standards",
                            correct=True,
                        ),
                        opt("A water-only rating with no energy criteria"),
                        opt("A demolition waste landfill classification"),
                    ),
                    "AQUA-HQE, run by Fundacao Vanzolini, adapts HQE to Brazil and aligns "
                    "with ABNT NBR 15575 performance requirements.",
                ),
                q(
                    "A LEED project earns 67 points. What level does it achieve?",
                    (
                        opt("Certified"),
                        opt("Silver"),
                        opt("Gold", correct=True),
                        opt("Platinum"),
                    ),
                    "67 points falls in the 60 to 79 band, which is LEED Gold.",
                ),
                q(
                    "What is the main risk of chasing certification points?",
                    (
                        opt("The building becomes too energy efficient"),
                        opt(
                            "Optimizing for the checklist instead of real outcomes - "
                            "'greenwashing by checklist', where the score becomes the goal",
                            correct=True,
                        ),
                        opt("Points cannot be audited"),
                        opt("Certification is illegal in Brazil"),
                    ),
                    "The rating is a means to verify performance, not the end - design "
                    "for the outcome and let the score follow.",
                ),
            ),
        ),
        # -- 7. Climate resilience -------------------------------------
        _t(
            "Climate resilience and adaptation",
            "10 min",
            """# Climate resilience and adaptation

Decarbonization (**mitigation**) reduces future warming; but the climate is
**already changing**, so infrastructure must also **adapt**. **Resilience**
is the ability of an asset and the system around it to withstand, absorb,
and recover from climate shocks and stresses - floods, heatwaves, drought,
storm surge, and wildfire - over a design life measured in decades.

The engineering shift is from **stationarity** - the old assumption that
the future looks statistically like the past - to designing for a **moving
baseline**. A culvert sized for the historic "1 in 100 year" storm may face
that flow far more often as rainfall intensifies.

A structured adaptation process:

- **Assess exposure and vulnerability** - which hazards, how severe, what
  fails, and who is affected (often the most vulnerable communities).
- **Design for future conditions** - use forward-looking climate
  projections, add freeboard and capacity **headroom**, and choose robust,
  low-regret measures.
- **Prefer green and hybrid infrastructure** - wetlands, permeable
  surfaces, and urban trees provide flood and heat resilience while also
  storing carbon (co-benefits).
- **Build in redundancy and flexibility** - avoid single points of failure;
  design so capacity can be added later.

```mermaid
graph TD
    HAZARD["Climate hazards"] --> ASSESS["Assess exposure and vulnerability"]
    ASSESS --> DESIGN["Design for future conditions"]
    DESIGN --> GREEN["Green and hybrid infrastructure"]
    DESIGN --> REDUND["Redundancy and headroom"]
    GREEN --> RESILIENT["Resilient system"]
    REDUND --> RESILIENT
    RESILIENT --> RECOVER["Withstand and recover"]
```

A worked **climate-adjusted design flow** for a stormwater culvert:

```text
Rational method:  Q = C x i x A / 360   (Q in m3/s, i in mm/h, A in ha)

Historic design storm:
  C = 0.70   i = 60 mm/h   A = 25 ha
  Q_hist = 0.70 x 60 x 25 / 360 = 2.92 m3/s

Climate uplift: projections add +20% to design rainfall intensity
  i_future = 60 x 1.20 = 72 mm/h
  Q_future = 0.70 x 72 x 25 / 360 = 3.50 m3/s

The culvert must pass 3.50 m3/s, not 2.92 m3/s - about 20% more capacity.
Sizing to the historic flow would under-design it for its service life.
```

Remember: mitigation limits how bad it gets; adaptation prepares for what is
already coming. Design for a moving baseline, add headroom, and use nature
where it pays double.
""",
        ),
        quiz_lesson(
            "Quiz: Climate resilience and adaptation",
            (
                q(
                    "What is the difference between mitigation and adaptation?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "Mitigation reduces future warming by cutting emissions; "
                            "adaptation prepares infrastructure for climate change that is "
                            "already happening",
                            correct=True,
                        ),
                        opt("Adaptation only means adding more concrete"),
                        opt("Mitigation applies only to bridges"),
                    ),
                    "Both are needed: cut emissions to limit warming, and adapt assets "
                    "for the warming already locked in.",
                ),
                q(
                    "Why is the assumption of 'stationarity' now a problem in design?",
                    (
                        opt("It makes calculations too simple"),
                        opt(
                            "It assumes the future is statistically like the past, but a "
                            "changing climate shifts the baseline, so historic storms "
                            "recur more often",
                            correct=True,
                        ),
                        opt("It only applies to structural steel"),
                        opt("It over-designs every culvert"),
                    ),
                    "Design must use forward-looking projections and add headroom rather "
                    "than assume a stationary climate.",
                ),
                q(
                    "With a 20 percent rainfall-intensity uplift, a culvert flow of "
                    "2.92 m3/s becomes about:",
                    (
                        opt("2.34 m3/s"),
                        opt("2.92 m3/s, unchanged"),
                        opt("3.50 m3/s", correct=True),
                        opt("5.84 m3/s"),
                    ),
                    "Q scales with intensity: 2.92 x 1.20 = 3.50 m3/s, so about 20 "
                    "percent more capacity is needed.",
                ),
            ),
        ),
        # -- 8. Net-zero pathways --------------------------------------
        _t(
            "Net-zero pathways for infrastructure",
            "11 min",
            """# Net-zero pathways for infrastructure

**Net zero** means the greenhouse gases an asset emits over its life are
balanced by an equal amount removed from the atmosphere - so its **net
contribution is zero**. For infrastructure this spans **both** operational
and embodied carbon, and the credible route follows the reduction hierarchy:
**reduce first, offset last**.

A whole-life net-zero pathway:

1. **Reduce operational carbon** - passive design, efficiency, and
   electrify end uses so they can run on clean power.
2. **Decarbonize supply** - on-site renewables and a greening grid drive
   operational emissions toward zero.
3. **Reduce embodied carbon** - build less, substitute cement, use bio-based
   and recycled materials (the low-carbon-materials lesson).
4. **Offset only the residual** - after everything feasible is cut, balance
   the remaining hard-to-abate carbon with **high-quality removals**, not
   cheap avoidance credits.

Beware two failure modes: **offsetting instead of reducing** (buying your
way out rather than designing carbon out), and ignoring **embodied carbon**
so an "operationally net-zero" building is not net zero at all.

```mermaid
graph TD
    TOTAL["Whole life carbon"] --> REDOP["Reduce operational"]
    REDOP --> CLEAN["Decarbonize energy supply"]
    TOTAL --> REDEMB["Reduce embodied"]
    CLEAN --> RESID["Residual carbon"]
    REDEMB --> RESID
    RESID --> OFFSET["Offset with quality removals"]
    OFFSET --> NET["Net zero"]
```

A worked **net-zero balance** for a building over its life:

```text
Whole-life carbon before action:
  Embodied (A to C)        = 2,000 t CO2e
  Operational (60 yr, B6)  = 4,500 t CO2e
  Total baseline           = 6,500 t CO2e

Apply the hierarchy:
  Embodied reduced 35%   -> 2,000 x 0.65 = 1,300 t CO2e
  Operational reduced 80% (efficiency + clean power)
                         -> 4,500 x 0.20 =   900 t CO2e
  Residual after reduction = 1,300 + 900 = 2,200 t CO2e

Offset the residual with certified removals:
  Offsets purchased        = 2,200 t CO2e

  Net = 2,200 (residual) - 2,200 (removed) = 0  ->  net zero

Reduction did the heavy lifting: 4,300 of 6,500 t (66%) was designed out
before a single offset was bought.
```

Remember: net zero is earned by reduction first and honored by removing the
small remainder - reduce operational and embodied carbon as far as feasible,
then offset only what is truly left with high-quality removals.
""",
        ),
        quiz_lesson(
            "Quiz: Net-zero pathways for infrastructure",
            (
                q(
                    "What does 'net zero' mean for an infrastructure asset?",
                    (
                        opt("It emits no carbon during construction only"),
                        opt(
                            "Its whole-life greenhouse gas emissions are balanced by an "
                            "equal amount removed, so its net contribution is zero",
                            correct=True,
                        ),
                        opt("It uses zero water"),
                        opt("It has zero capital cost"),
                    ),
                    "Net zero spans operational and embodied carbon; residual emissions "
                    "are balanced by removals.",
                ),
                q(
                    "What is the correct priority in a credible net-zero pathway?",
                    (
                        opt("Offset everything first, then reduce if convenient"),
                        opt(
                            "Reduce operational and embodied carbon as far as feasible "
                            "first, then offset only the residual with quality removals",
                            correct=True,
                        ),
                        opt("Ignore embodied carbon entirely"),
                        opt("Buy the cheapest avoidance credits available"),
                    ),
                    "Reduce first, offset last - and offset residuals with high-quality "
                    "removals, not cheap avoidance credits.",
                ),
                q(
                    "In the worked balance, how much of the 6,500 t baseline was designed "
                    "out before any offset was purchased?",
                    (
                        opt("None of it"),
                        opt("About 2,200 t"),
                        opt("About 4,300 t, roughly 66 percent", correct=True),
                        opt("All 6,500 t"),
                    ),
                    "Reduction cut 6,500 to 2,200 t; the 4,300 t difference (about 66 "
                    "percent) was designed out, and only the residual was offset.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What are the three pillars of sustainable construction?",
                    (
                        opt("Cement, steel, timber"),
                        opt("Environmental, social, economic", correct=True),
                        opt("Design, build, operate"),
                        opt("Air, water, soil"),
                    ),
                    "The triple bottom line, judged across the asset's whole life.",
                ),
                q(
                    "Why should decisions use life-cycle cost rather than first cost?",
                    (
                        opt("First cost cannot be measured"),
                        opt(
                            "A design cheap to build can be expensive to run; life-cycle "
                            "cost and carbon capture the whole picture",
                            correct=True,
                        ),
                        opt("Life-cycle cost is always lower on day one"),
                        opt("Regulations ban first-cost estimates"),
                    ),
                    "The efficient-pump example: higher capital, far lower whole-life cost.",
                ),
                q(
                    "A building uses 750,000 kWh/yr over 5,000 m2. What is its EUI?",
                    (
                        opt("15 kWh/m2/yr"),
                        opt("150 kWh/m2/yr", correct=True),
                        opt("1,500 kWh/m2/yr"),
                        opt("3.75 kWh/m2/yr"),
                    ),
                    "750,000 / 5,000 = 150 kWh per square metre per year.",
                ),
                q(
                    "Why is embodied carbon urgent to design out early?",
                    (
                        opt("It is only emitted after demolition"),
                        opt(
                            "It is front-loaded - largely emitted before the building "
                            "opens - and cannot be recovered afterwards",
                            correct=True,
                        ),
                        opt("It is always smaller than operational carbon"),
                        opt("It can be offset for free"),
                    ),
                    "Front-loaded carbon in materials must be avoided at design stage.",
                ),
                q(
                    "In EN 15978, which modules cover the use stage of a building?",
                    (
                        opt("A1-A3"),
                        opt("A4-A5"),
                        opt("B1-B7", correct=True),
                        opt("C1-C4"),
                    ),
                    "B modules cover use, maintenance, repair, replacement, and "
                    "operational energy (B6) and water (B7).",
                ),
                q(
                    "What is the order of the waste hierarchy from best to worst?",
                    (
                        opt("Dispose, recover, recycle, reuse, prevent"),
                        opt("Prevent, reuse, recycle, recover, dispose", correct=True),
                        opt("Recycle, recover, prevent, reuse, dispose"),
                        opt("Reuse, recycle, dispose, prevent, recover"),
                    ),
                    "Prevention is best, landfill disposal worst; reuse beats recycling.",
                ),
                q(
                    "How can the embodied carbon of a concrete slab be reduced?",
                    (
                        opt("Add more Portland cement"),
                        opt(
                            "Replace part of the clinker with supplementary cementitious "
                            "materials such as GGBS or fly ash",
                            correct=True,
                        ),
                        opt("Cure it in sunlight"),
                        opt("Increase its thickness"),
                    ),
                    "Cement clinker is the carbon-heavy part; slag and fly ash "
                    "substitution cut it, as in the 22 t saving example.",
                ),
                q(
                    "A LEED project earns 55 points. What certification level is that?",
                    (
                        opt("Certified"),
                        opt("Silver", correct=True),
                        opt("Gold"),
                        opt("Platinum"),
                    ),
                    "50 to 59 points is LEED Silver; Gold starts at 60.",
                ),
                q(
                    "Why is designing for 'stationarity' now considered unsafe?",
                    (
                        opt("It over-designs every asset"),
                        opt(
                            "It assumes the future matches the past, but climate change "
                            "shifts the baseline so historic storms recur more often",
                            correct=True,
                        ),
                        opt("It ignores structural loads"),
                        opt("It only affects timber buildings"),
                    ),
                    "Adaptation requires forward-looking projections and capacity "
                    "headroom, not the stationary assumption.",
                ),
                q(
                    "In a credible net-zero pathway, what comes before offsetting?",
                    (
                        opt("Nothing - offset first"),
                        opt(
                            "Reducing operational and embodied carbon as far as feasible, "
                            "so only the true residual is offset with quality removals",
                            correct=True,
                        ),
                        opt("Buying the cheapest avoidance credits"),
                        opt("Ignoring embodied carbon"),
                    ),
                    "Reduce first, offset last; reduction should do the heavy lifting "
                    "before any removals are purchased.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SUSTAINABLE_CONSTRUCTION_COURSES: tuple[SeedCourse, ...] = (_SUSTAINABLE_CONSTRUCTION,)
