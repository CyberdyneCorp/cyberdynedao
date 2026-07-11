"""Academy seed content - Concrete Technology.

The science and practice of concrete, from constituents to structures: what
cement is and how it hydrates, mix design (dosagem) around the water-cement
ratio, the behavior of fresh concrete (workability, slump, placing), hardened
properties and compressive strength, chemical and mineral admixtures,
durability with shrinkage and creep, modern special concretes (self-compacting,
high-performance, fiber-reinforced), and the shift to low-carbon, sustainable
mixes. Every lesson is a direct explanation grounded in real practice and
standards (ABNT NBR, ACI, Eurocode) with a worked mix-design calculation or
formula and a mermaid diagram, followed by a checkpoint quiz; the course closes
with a comprehensive final quiz.
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


_CONCRETE_TECHNOLOGY = SeedCourse(
    slug="concrete-technology",
    title="Concrete Technology",
    description=(
        "The science and practice of concrete - mix design, fresh and hardened "
        "behavior, admixtures, durability, and modern special and low-carbon "
        "concretes. Every lesson explains one idea directly, works a real "
        "mix-design calculation or formula, and draws the idea as a diagram, "
        "grounded in ABNT NBR, ACI and Eurocode practice."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Concrete Technology

Concrete is the most-used building material on Earth - and one of the most
misunderstood. It is not just "cement and water": it is a designed composite
whose fresh and hardened behavior you can predict and control. This course
teaches you how concrete works as a material, so you can specify, proportion,
and troubleshoot it with confidence.

The approach is **direct and quantitative**: every lesson explains one idea
plainly, works a short real calculation or gives the governing formula (a
water-cement ratio, a strength estimate, a durability check), and draws the
idea as a diagram. After each lesson there is a short quiz; at the end, a
final quiz covers the whole course.

What you will build understanding for, in order:

1. **Constituents and hydration** - what is in concrete and how cement sets
2. **Mix design (dosagem)** - the water-cement ratio and proportioning
3. **Fresh concrete** - workability, slump, and placing
4. **Hardened concrete** - compressive strength and how we measure it
5. **Admixtures and mineral additions** - chemistry that changes behavior
6. **Durability, shrinkage and creep** - making concrete last
7. **Special concretes** - self-compacting, high-performance, fiber-reinforced
8. **Low-carbon and sustainable concrete** - cutting the CO2 footprint

The through-line is that almost everything - strength, durability, cost, and
carbon - traces back to a few controllable choices: the **water-cement ratio**,
the materials, and how well the concrete is placed and cured. Keep that in mind
and the whole subject holds together.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How does this course frame concrete?",
                    (
                        opt("As a fixed recipe that cannot be changed"),
                        opt(
                            "As a designed composite whose fresh and hardened behavior "
                            "you can predict and control through a few key choices",
                            correct=True,
                        ),
                        opt("As a purely decorative finish material"),
                        opt("As a material that only structural engineers ever touch"),
                    ),
                    "Concrete is engineered; strength, durability, cost and carbon trace "
                    "back to controllable choices - above all the water-cement ratio.",
                ),
                q(
                    "Which single parameter does the course keep returning to as the "
                    "master control on concrete quality?",
                    (
                        opt("The color of the aggregate"),
                        opt("The brand printed on the cement bag"),
                        opt("The water-cement ratio", correct=True),
                        opt("The time of day the concrete is poured"),
                    ),
                    "The water-cement (w/c) ratio governs strength, permeability and "
                    "durability - it is the recurring theme of the whole course.",
                ),
            ),
        ),
        # -- 1. Constituents and hydration -----------------------------
        _t(
            "Concrete constituents and cement hydration",
            "10 min",
            """# Concrete constituents and cement hydration

Concrete is a **composite**: a paste of **cement and water** that binds
together **aggregates** (sand and gravel/crushed stone), often with **chemical
admixtures** and **supplementary cementitious materials**. By volume a typical
mix is roughly 60-75% aggregate, 15-20% paste, and the rest air and water - the
aggregate is the cheap, stable skeleton; the paste is the active glue.

**Portland cement** is made by burning limestone and clay to form **clinker**,
then grinding it with gypsum. Its main compounds (Bogue notation) drive behavior:

- **C3S (alite)** - the main source of early strength.
- **C2S (belite)** - slow, contributes to later strength.
- **C3A** - very reactive, flash-set risk (gypsum controls it), vulnerable to
  sulfate attack.
- **C4AF** - contributes little strength, gives the gray color.

When water is added, **hydration** begins - an exothermic chemical reaction (not
drying) that produces the two key phases:

- **C-S-H** (calcium silicate hydrate) - the glue that gives strength.
- **CH** (calcium hydroxide, portlandite) - keeps the pore water alkaline
  (pH around 13), which protects steel reinforcement from corrosion.

```text
Simplified hydration of alite:
    2 C3S + 6 H  ->  C3S2H3 (C-S-H)  +  3 CH
    (cement)  (water)   (strength glue)   (alkaline reserve)

Heat of hydration is released - important for mass concrete (thermal cracking).
```

Hydration needs water and time. This is why **curing** (keeping concrete moist)
matters: if the water leaves before the cement has reacted, strength and
durability are lost permanently.

```mermaid
graph TD
    CEM["Portland cement"] --> PASTE["Cement plus water paste"]
    WATER["Mixing water"] --> PASTE
    AGG["Aggregates sand and gravel"] --> MIX["Fresh concrete"]
    PASTE --> MIX
    PASTE --> HYD["Hydration reaction"]
    HYD --> CSH["C-S-H strength glue"]
    HYD --> CH["Calcium hydroxide alkalinity"]
    HYD --> HEAT["Heat of hydration"]
```

Remember: cement hydrates, it does not dry. Keep it moist and give it time, and
the C-S-H that gives concrete its strength keeps forming for weeks.
""",
        ),
        quiz_lesson(
            "Quiz: Concrete constituents and cement hydration",
            (
                q(
                    "Which hydration product is the main source of concrete strength?",
                    (
                        opt("Calcium hydroxide (CH)"),
                        opt("Calcium silicate hydrate (C-S-H)", correct=True),
                        opt("Gypsum"),
                        opt("Unreacted clinker"),
                    ),
                    "C-S-H is the binding gel that glues the composite together; CH keeps "
                    "the pore solution alkaline but contributes little strength.",
                ),
                q(
                    "Why does calcium hydroxide (portlandite) matter even though it adds "
                    "little strength?",
                    (
                        opt("It makes the concrete lighter"),
                        opt("It speeds up drying"),
                        opt(
                            "It keeps the pore water highly alkaline (pH around 13), which "
                            "passivates and protects the steel reinforcement",
                            correct=True,
                        ),
                        opt("It gives concrete its gray color"),
                    ),
                    "The alkaline reserve forms a passive film on rebar; losing it (e.g. by "
                    "carbonation) is what lets reinforcement corrode.",
                ),
                q(
                    "Cement hydration is best described as...",
                    (
                        opt("simply the water evaporating and the mix drying out"),
                        opt(
                            "an exothermic chemical reaction between cement and water that "
                            "needs moisture and time to complete",
                            correct=True,
                        ),
                        opt("a purely physical stacking of aggregate particles"),
                        opt("a reaction that stops the moment mixing ends"),
                    ),
                    "Hydration is chemistry, not drying - which is exactly why curing "
                    "(keeping it moist) is essential.",
                ),
            ),
        ),
        # -- 2. Mix design ---------------------------------------------
        _t(
            "Mix design - water-cement ratio and proportioning",
            "12 min",
            """# Mix design - water-cement ratio and proportioning

**Mix design** (Portuguese *dosagem*) is choosing the proportions of cement,
water, aggregates and admixtures to hit a target **strength**, **workability**
and **durability** at the lowest sensible cost. The single most important lever
is **Abrams' law**: for workable concrete, compressive strength depends almost
entirely on the **water-cement ratio (w/c)** - the mass of water divided by the
mass of cement. Lower w/c means fewer capillary pores, so higher strength and
lower permeability.

```text
Abrams' law (form):   fc = A / B^(w/c)

  fc  = compressive strength
  w/c = water-cement ratio (by mass)
  A, B = empirical constants for the materials
Lower w/c  ->  higher strength and lower permeability.
```

A practical proportioning path (the logic behind ACI 211 and the ABNT/IPT-ABCP
methods):

1. **Target strength.** Design for f_cm, above the characteristic f_ck, to
   allow for scatter:  `f_cm = f_ck + 1.65 * s`  (s = standard deviation).
2. **Pick w/c** from a strength-vs-w/c curve for your materials, then take the
   *lower* of that and any durability limit (codes cap w/c by exposure class).
3. **Choose water content** from the workability (slump) and max aggregate size.
4. **Compute cement:**  `cement = water / (w/c)`.
5. **Fill with aggregates** (fine + coarse) to close the volume; check the
   minimum cement content the code requires.

Worked example:

```text
Given:  f_ck = 30 MPa,  s = 4 MPa
Target: f_cm = 30 + 1.65 x 4 = 36.6 MPa

Curve gives w/c = 0.50 for 36.6 MPa; durability class caps w/c at 0.55.
Take the lower -> w/c = 0.50.

Slump target needs ~185 kg of water per m3.
Cement = water / (w/c) = 185 / 0.50 = 370 kg/m3   (>= code minimum: OK)
Remaining volume filled with sand + gravel to reach 1 m3.
```

```mermaid
graph TD
    FCK["Target f_ck"] --> FCM["Design f_cm equals f_ck plus 1.65 s"]
    FCM --> WC["Select w/c from strength curve"]
    DUR["Durability exposure limit"] --> WC
    WC --> WATER["Water from slump and aggregate size"]
    WATER --> CEM["Cement from water and w slash c"]
    CEM --> FILL["Fill volume with aggregates"]
    FILL --> CHECK["Check minimum cement and trial batch"]
```

Remember: choose the w/c first (from strength AND durability, take the stricter),
set the water from workability, and cement falls out as water divided by w/c.
Always confirm with a **trial batch** - tables get you close, the real materials
decide.
""",
        ),
        quiz_lesson(
            "Quiz: Mix design - water-cement ratio and proportioning",
            (
                q(
                    "According to Abrams' law, the compressive strength of workable "
                    "concrete depends primarily on...",
                    (
                        opt("the brand of cement"),
                        opt("the water-cement ratio", correct=True),
                        opt("the color of the sand"),
                        opt("the ambient humidity on delivery day"),
                    ),
                    "Lower w/c means fewer capillary pores, so higher strength and lower "
                    "permeability - the central law of mix design.",
                ),
                q(
                    "Why design for a mean strength f_cm above the characteristic f_ck?",
                    (
                        opt("To waste cement on purpose"),
                        opt(
                            "To account for the natural scatter of concrete production, so "
                            "the characteristic value is still met (f_cm = f_ck + 1.65 s)",
                            correct=True,
                        ),
                        opt("Because codes forbid using f_ck directly"),
                        opt("To make the concrete cure faster"),
                    ),
                    "Production varies; targeting the mean above f_ck by 1.65 standard "
                    "deviations gives the required 95% confidence on f_ck.",
                ),
                q(
                    "If the strength curve allows w/c = 0.55 but the durability exposure "
                    "class caps it at 0.45, what w/c do you use?",
                    (
                        opt("0.55, because strength governs"),
                        opt("0.50, the average of the two"),
                        opt("0.45, the stricter (lower) of the two limits", correct=True),
                        opt("Any value, w/c does not matter here"),
                    ),
                    "You always take the lower w/c - both strength and durability must be "
                    "satisfied, so the more demanding limit wins.",
                ),
            ),
        ),
        # -- 3. Fresh concrete -----------------------------------------
        _t(
            "Fresh concrete - workability, slump and placing",
            "10 min",
            """# Fresh concrete - workability, slump and placing

Before it hardens, concrete has to be **transported, placed, and compacted**
into the forms around the reinforcement. **Workability** is how easily it can
be handled and consolidated without **segregation** (coarse aggregate settling
out) or **bleeding** (water rising to the surface). Too stiff and it will not
fill the forms; too wet and it segregates and loses strength.

The everyday field measure is the **slump test** (ABNT NBR NM 67 / ASTM C143):
fill a standard cone in layers, rod each, lift the cone, and measure how far the
concrete slumps down.

```text
Slump test (Abrams cone: 300 mm high):
    slump = 300 mm - height of the slumped concrete

Rough guidance:
    25-75 mm    stiff        (pavements, heavily compacted)
    75-150 mm   plastic      (normal reinforced sections)
    > 150 mm    flowing      (congested rebar, or with plasticizers)
```

The key trap: you can always add water to make concrete flow more easily, but
**adding water raises the w/c ratio and destroys strength and durability**. The
correct way to gain workability without more water is a **water-reducer /
superplasticizer** admixture. This tension - flowability now versus strength
later - is why fresh-concrete control matters so much.

Placing discipline that protects quality:

- **Do not add water on site** to a stiff truck - re-dose with plasticizer.
- **Compact** with vibration to remove entrapped air (each 1% of trapped air
  costs roughly 5% strength), but do not over-vibrate (segregation).
- **Avoid drop segregation** - do not free-fall concrete from a great height.
- **Watch the initial set** - place and finish before the concrete stiffens.

```mermaid
graph LR
    BATCH["Batch and mix"] --> TRANS["Transport truck mixer"]
    TRANS --> SLUMP["Slump test acceptance"]
    SLUMP --> PLACE["Place in forms"]
    PLACE --> COMPACT["Compact by vibration"]
    COMPACT --> FINISH["Finish surface"]
    SLUMP --> REJECT["Out of spec re dose admixture"]
```

Remember: workability is set at the batch plant, verified by slump, and
protected on site. When it needs to flow more, reach for a superplasticizer -
never the hose.
""",
        ),
        quiz_lesson(
            "Quiz: Fresh concrete - workability, slump and placing",
            (
                q(
                    "What does the slump test measure?",
                    (
                        opt("The compressive strength of hardened concrete"),
                        opt(
                            "The consistency/workability of fresh concrete - how far it "
                            "slumps down from a standard cone",
                            correct=True,
                        ),
                        opt("The chloride content of the mix"),
                        opt("The final set time"),
                    ),
                    "Slump is a quick field index of consistency; it does not measure "
                    "strength, though a sudden slump change can signal a problem.",
                ),
                q(
                    "A truck arrives too stiff to place. What is the correct fix?",
                    (
                        opt("Add water from the site hose until it flows"),
                        opt(
                            "Re-dose with a water-reducer/superplasticizer, which adds "
                            "flowability without raising the w/c ratio",
                            correct=True,
                        ),
                        opt("Place it stiff and hope vibration is enough"),
                        opt("Add extra cement powder on top"),
                    ),
                    "Adding water raises w/c and permanently cuts strength and durability; "
                    "a superplasticizer gives flow at the same w/c.",
                ),
                q(
                    "Why is proper compaction (vibration) important for fresh concrete?",
                    (
                        opt("It speeds up hydration chemically"),
                        opt("It changes the cement type"),
                        opt(
                            "It removes entrapped air voids - each ~1% of trapped air can "
                            "cost roughly 5% of strength",
                            correct=True,
                        ),
                        opt("It is only cosmetic and has no effect on strength"),
                    ),
                    "Entrapped air is a defect; vibration consolidates the concrete, but "
                    "over-vibration causes segregation.",
                ),
            ),
        ),
        # -- 4. Hardened concrete and compressive strength -------------
        _t(
            "Hardened concrete and compressive strength",
            "11 min",
            """# Hardened concrete and compressive strength

Hardened concrete is **strong in compression, weak in tension** - roughly ten
times weaker in tension than compression - which is exactly why we combine it
with steel reinforcement that carries the tension. Its defining property is the
**characteristic compressive strength, f_ck**: the value below which no more than
5% of results are expected to fall.

Strength is verified by crushing standard **specimens** cured and tested at a
set age (usually **28 days**, when most hydration has occurred):

```text
Compressive strength from a crushed cylinder:
    fc = F / A
      F = maximum load at failure (N)
      A = cross-sectional area (mm^2)

Example: 150 mm diameter cylinder, fails at 636 kN
    A  = pi/4 x 150^2 = 17671 mm^2
    fc = 636000 / 17671 = 36.0 MPa
```

Two specimen shapes are used and they are not equal: a **cylinder** (150 x 300
mm, common in Brazil/ACI) reads lower than a **cube** (150 mm, common in
Europe). A rule of thumb is `f_cylinder ~ 0.80 x f_cube`, so a C25/30 in
Eurocode notation means 25 MPa cylinder / 30 MPa cube.

Strength develops over time as hydration continues:

- **Early (1-7 days)** - fast gain, driven by C3S; governs formwork stripping.
- **28 days** - the reference age for f_ck.
- **Beyond** - slow continued gain, especially with slag or fly ash.

Other hardened properties scale with strength: tensile strength (about
`0.3 x f_ck^(2/3)` MPa), and the **elastic modulus** (stiffness), which controls
deflections - Eurocode uses roughly `E ~ 22000 x (f_cm/10)^0.3` MPa.

```mermaid
graph TD
    MIX["Hardened concrete"] --> COMP["Strong in compression"]
    MIX --> TENS["Weak in tension"]
    TENS --> STEEL["Add steel reinforcement for tension"]
    COMP --> SPEC["Crush standard specimens"]
    SPEC --> AGE["Test at 28 days"]
    AGE --> FCK["Characteristic strength f_ck"]
    FCK --> E["Elastic modulus and deflection"]
```

Remember: f_ck at 28 days from crushed specimens is the contract number, concrete
carries compression while steel carries tension, and specimen shape changes the
value - always state cylinder or cube.
""",
        ),
        quiz_lesson(
            "Quiz: Hardened concrete and compressive strength",
            (
                q(
                    "What does the characteristic compressive strength f_ck represent?",
                    (
                        opt("The average of all test results"),
                        opt(
                            "The strength below which no more than 5% of results are "
                            "expected to fall",
                            correct=True,
                        ),
                        opt("The single highest result recorded"),
                        opt("The tensile strength of the concrete"),
                    ),
                    "f_ck is a lower characteristic (5% fractile) value - that is why the "
                    "mix is designed for a higher mean f_cm.",
                ),
                q(
                    "Why is concrete almost always used together with steel reinforcement?",
                    (
                        opt("Steel makes the concrete cheaper"),
                        opt(
                            "Concrete is weak in tension (about ten times weaker than in "
                            "compression), so steel carries the tensile forces",
                            correct=True,
                        ),
                        opt("Steel speeds up hydration"),
                        opt("It is only for decorative reasons"),
                    ),
                    "Concrete handles compression well but cracks under tension; rebar "
                    "carries the tension in beams, slabs and columns.",
                ),
                q(
                    "A 150 mm diameter cylinder fails at 636 kN. Its compressive strength "
                    "is closest to...",
                    (
                        opt("about 4 MPa"),
                        opt("about 18 MPa"),
                        opt("about 36 MPa", correct=True),
                        opt("about 90 MPa"),
                    ),
                    "A = pi/4 x 150^2 = 17671 mm^2; fc = 636000 N / 17671 mm^2 ~ 36 MPa.",
                ),
            ),
        ),
        # -- 5. Admixtures and mineral additions -----------------------
        _t(
            "Admixtures and mineral additions",
            "11 min",
            """# Admixtures and mineral additions

Modern concrete is rarely just cement, water and aggregate. Two families of
extra ingredients let you tune behavior: **chemical admixtures** (small doses,
big effect on fresh/setting behavior) and **mineral additions / supplementary
cementitious materials (SCMs)** (larger fractions replacing part of the cement).

**Chemical admixtures** (ABNT NBR 11768 / ASTM C494), dosed at a few percent of
cement mass or less:

- **Water reducers / superplasticizers** - the workhorses. They disperse cement
  particles so you get the same workability at a **lower w/c** - meaning more
  strength - or the same w/c at much higher flow. High-range types cut water by
  15-30% and are what make self-compacting and high-performance concrete
  possible.
- **Retarders** - delay setting (hot weather, long hauls, mass pours).
- **Accelerators** - speed setting/strength (cold weather, fast formwork
  turnover). Chloride-based accelerators corrode steel - avoid in reinforced
  concrete.
- **Air-entraining agents** - create tiny stable air bubbles that give
  freeze-thaw resistance (essential in cold climates).

**Mineral additions / SCMs** partly replace clinker and react with the calcium
hydroxide from hydration (a **pozzolanic** reaction), forming more C-S-H:

- **Fly ash** - improves workability and long-term strength, lowers heat.
- **Ground granulated blast-furnace slag (GGBFS)** - can replace a large share
  of cement, improves durability.
- **Silica fume** - very fine, gives high strength and very low permeability.

```text
Pozzolanic reaction (why SCMs work):
    SCM (silica) + CH (from hydration) + H  ->  extra C-S-H

Effect: consumes the weak, soluble CH and makes more strength glue
        -> denser, less permeable, more durable concrete.
Bonus: replacing clinker with SCMs cuts CO2 sharply (see the last lesson).
```

```mermaid
graph TD
    CONC["Concrete mix"] --> CHEM["Chemical admixtures"]
    CONC --> SCM["Mineral additions SCMs"]
    CHEM --> SP["Superplasticizer lowers w slash c"]
    CHEM --> AIR["Air entrainer for freeze thaw"]
    CHEM --> SET["Retarder or accelerator"]
    SCM --> POZ["Pozzolanic reaction with CH"]
    POZ --> CSH2["More C-S-H denser and durable"]
    SCM --> CO2["Less clinker lower CO2"]
```

Remember: chemical admixtures fine-tune the fresh and setting behavior at tiny
doses; SCMs replace clinker and, through the pozzolanic reaction, make concrete
denser, more durable, and lower-carbon.
""",
        ),
        quiz_lesson(
            "Quiz: Admixtures and mineral additions",
            (
                q(
                    "What is the primary benefit of a superplasticizer (high-range water reducer)?",
                    (
                        opt("It replaces the cement entirely"),
                        opt(
                            "It disperses cement particles so you get workability at a "
                            "lower w/c (more strength) or high flow at the same w/c",
                            correct=True,
                        ),
                        opt("It colors the concrete"),
                        opt("It permanently stops hydration"),
                    ),
                    "Superplasticizers decouple flow from water content - the key to "
                    "self-compacting and high-performance concrete.",
                ),
                q(
                    "How do pozzolanic SCMs like fly ash or silica fume improve concrete?",
                    (
                        opt("By evaporating faster"),
                        opt(
                            "They react with the calcium hydroxide (CH) from hydration to "
                            "form additional C-S-H, giving denser, less permeable concrete",
                            correct=True,
                        ),
                        opt("By adding chloride to speed setting"),
                        opt("By increasing the w/c ratio"),
                    ),
                    "The pozzolanic reaction consumes the weak, soluble CH and produces "
                    "more strength gel - and replacing clinker cuts CO2.",
                ),
                q(
                    "Why should chloride-based accelerators be avoided in reinforced concrete?",
                    (
                        opt("They make concrete too strong"),
                        opt("They slow setting too much"),
                        opt(
                            "Chlorides promote corrosion of the steel reinforcement",
                            correct=True,
                        ),
                        opt("They have no effect and are simply a waste"),
                    ),
                    "Chlorides break down the passive film on rebar; non-chloride "
                    "accelerators are used where reinforcement is present.",
                ),
            ),
        ),
        # -- 6. Durability, shrinkage and creep ------------------------
        _t(
            "Durability, shrinkage and creep",
            "12 min",
            """# Durability, shrinkage and creep

A structure can be strong yet fail early if it is not **durable**. Most
durability problems are about **transport**: water and aggressive agents moving
through the pore network. A **low w/c ratio** (dense, low-permeability paste)
plus adequate **cover** over the rebar and good **curing** are the front-line
defenses. Codes formalize this with **exposure classes** (Eurocode XC/XD/XS,
ABNT NBR 6118 aggressiveness classes I-IV) that set a maximum w/c, a minimum
cement content, and a minimum cover for each environment.

Common deterioration mechanisms:

- **Carbonation** - atmospheric CO2 reacts with CH, dropping pH; once the
  carbonation front reaches the rebar, the passive film breaks and steel
  corrodes. Corrosion products expand and spall the cover.
- **Chloride attack** - chlorides (seawater, de-icing salt) depassivate steel
  even at high pH - the main threat to marine and bridge structures.
- **Sulfate attack** - external sulfates react with C3A, expanding and cracking
  (use sulfate-resistant cement).
- **Alkali-silica reaction (ASR)** - reactive aggregate + alkalis form an
  expansive gel.
- **Freeze-thaw** - water in pores expands on freezing (air entrainment helps).

Concrete also **moves over time**, even unloaded or under constant load:

- **Shrinkage** - volume loss mainly as water leaves (drying shrinkage);
  restrained shrinkage cracks. Controlled by curing, low w/c, and joints.
- **Creep** - slow, time-dependent strain under sustained load; it increases
  deflections and relaxes prestress.

```text
Carbonation depth grows with the square root of time:
    x = k * sqrt(t)
      x = carbonation depth,  t = time,  k = coefficient (lower for low w/c)

Design idea: keep x < cover over the service life.
  If k = 3 mm/year^0.5:  x(50 yr) = 3 * sqrt(50) = 21 mm
  -> a 25 mm cover is marginal; 40 mm is safe.
```

```mermaid
graph TD
    ENV["Exposure class"] --> WC["Limit w slash c and cement content"]
    ENV --> COVER["Minimum cover over rebar"]
    WC --> DENSE["Dense low permeability paste"]
    COVER --> DENSE
    DENSE --> DUR["Durable concrete"]
    ATT["Aggressive agents"] --> CARB["Carbonation"]
    ATT --> CL["Chlorides"]
    ATT --> SULF["Sulfates"]
    CARB --> CORR["Rebar corrosion"]
    CL --> CORR
```

Remember: durability is won at the mix and detailing stage - low w/c, good
curing, and enough cover for the exposure. Design the cover so the carbonation
(and chloride) front never reaches the steel within the design life, and detail
for shrinkage and creep movement.
""",
        ),
        quiz_lesson(
            "Quiz: Durability, shrinkage and creep",
            (
                q(
                    "What is the front-line defense against most durability problems?",
                    (
                        opt("A high w/c ratio for easy placing"),
                        opt(
                            "A low w/c dense paste, adequate cover over the rebar, and "
                            "good curing - so aggressive agents cannot penetrate",
                            correct=True,
                        ),
                        opt("Painting the surface a light color"),
                        opt("Using the maximum possible aggregate size"),
                    ),
                    "Durability is a transport problem; a dense, low-permeability, "
                    "well-cured cover keeps water and ions out.",
                ),
                q(
                    "How does carbonation lead to reinforcement corrosion?",
                    (
                        opt("It makes the concrete lighter"),
                        opt(
                            "CO2 reacts with calcium hydroxide, lowering the pH; when the "
                            "carbonation front reaches the steel, its passive film breaks "
                            "and it corrodes",
                            correct=True,
                        ),
                        opt("It adds chlorides to the mix"),
                        opt("It increases the concrete's compressive strength"),
                    ),
                    "Carbonation consumes the alkaline reserve; without high pH the rebar "
                    "depassivates - which is why cover depth is a durability design value.",
                ),
                q(
                    "What is the difference between shrinkage and creep?",
                    (
                        opt("They are the same phenomenon"),
                        opt(
                            "Shrinkage is volume loss mainly from water leaving (even "
                            "unloaded); creep is time-dependent strain under sustained load",
                            correct=True,
                        ),
                        opt("Shrinkage only happens under load; creep only when unloaded"),
                        opt("Both only occur during the first hour after mixing"),
                    ),
                    "Drying shrinkage happens regardless of load; creep is the slow strain "
                    "that grows while a load is held - both cause cracking and deflection.",
                ),
            ),
        ),
        # -- 7. Special concretes --------------------------------------
        _t(
            "Special concretes - self-compacting, high-performance, fiber-reinforced",
            "11 min",
            """# Special concretes - self-compacting, high-performance, fiber-reinforced

Ordinary concrete has limits; **special concretes** push specific properties far
beyond it, almost always enabled by admixtures and careful proportioning.

**Self-compacting concrete (SCC)** flows and consolidates under its own weight -
no vibration - filling congested reinforcement and complex forms while resisting
segregation. It needs high **fluidity** (high-range superplasticizer) balanced
with high **viscosity/cohesion** (more fines or a viscosity-modifying admixture).
Field acceptance uses the **slump-flow** test instead of a slump cone:

```text
Slump-flow test (SCC): lift the cone, measure the spread diameter.
    SF = average spread diameter (mm)
    SF1  550-650 mm   SF2  660-750 mm   SF3  760-850 mm
Also check T500 (time to reach 500 mm) for viscosity and the
J-ring for passing ability through rebar.
```

**High-performance / high-strength concrete (HPC)** targets very high strength
(often > 50 MPa, up to 100+ MPa) and/or very low permeability. The recipe: a
**very low w/c** (around 0.20-0.35), a strong superplasticizer, and **silica
fume** to fill the finest pores and strengthen the paste-aggregate interface.
Used in tall columns, long spans, and aggressive environments. **Ultra-high
performance concrete (UHPC)** goes further (> 120 MPa) with fine steel fibers.

**Fiber-reinforced concrete (FRC)** disperses short fibers (steel, glass,
polypropylene, natural) through the mix. Fibers do not make it much stronger;
they bridge cracks, so they add **post-crack toughness, ductility and crack
control** - key for slabs on grade, tunnel linings (shotcrete), and precast.

```mermaid
graph TD
    BASE["Beyond ordinary concrete"] --> SCC["Self compacting"]
    BASE --> HPC["High performance"]
    BASE --> FRC["Fiber reinforced"]
    SCC --> FLOW["Flows without vibration slump flow test"]
    HPC --> LOWWC["Very low w slash c plus silica fume"]
    HPC --> STR["Very high strength low permeability"]
    FRC --> FIB["Fibers bridge cracks"]
    FIB --> TOUGH["Post crack toughness and ductility"]
```

Remember: each special concrete solves one problem - SCC solves placing in
congested forms, HPC solves strength and durability with a very low w/c and
silica fume, and FRC solves brittleness by bridging cracks with fibers.
""",
        ),
        quiz_lesson(
            "Quiz: Special concretes - self-compacting, high-performance, fiber-reinforced",
            (
                q(
                    "What defines self-compacting concrete (SCC)?",
                    (
                        opt("It sets in under one minute"),
                        opt(
                            "It flows and consolidates under its own weight without "
                            "vibration, while resisting segregation",
                            correct=True,
                        ),
                        opt("It contains no cement"),
                        opt("It can only be used underwater"),
                    ),
                    "SCC balances high fluidity (superplasticizer) with cohesion; it is "
                    "accepted by the slump-flow test, not the slump cone.",
                ),
                q(
                    "What combination typically produces high-performance/high-strength concrete?",
                    (
                        opt("A high w/c ratio and coarse aggregate only"),
                        opt(
                            "A very low w/c ratio, a strong superplasticizer, and silica "
                            "fume to densify the paste and interface",
                            correct=True,
                        ),
                        opt("Extra mixing water and no admixtures"),
                        opt("Air entrainment as the main ingredient"),
                    ),
                    "Very low w/c (0.20-0.35) plus silica fume fills the finest pores and "
                    "strengthens the paste-aggregate transition zone.",
                ),
                q(
                    "What do fibers mainly contribute to fiber-reinforced concrete?",
                    (
                        opt("A large increase in compressive strength"),
                        opt("Faster hydration"),
                        opt(
                            "Post-crack toughness, ductility and crack control - they "
                            "bridge cracks rather than raising raw strength",
                            correct=True,
                        ),
                        opt("A lower cement cost only"),
                    ),
                    "Fibers do not add much strength; they hold cracks together, adding "
                    "toughness - valuable in slabs, shotcrete and precast.",
                ),
            ),
        ),
        # -- 8. Low-carbon and sustainable concrete --------------------
        _t(
            "Low-carbon and sustainable concrete",
            "11 min",
            """# Low-carbon and sustainable concrete

Cement is responsible for roughly **7-8% of global CO2 emissions**, almost all
of it from **clinker**: about 60% of the CO2 is *process* emissions from
calcining limestone (CaCO3 -> CaO + CO2) and the rest is fuel to reach ~1450 C.
Because concrete is used in enormous volumes, small improvements per tonne add
up to a huge climate lever - and lowering carbon usually improves durability too.

The main strategies, roughly in order of impact today:

- **Clinker substitution (SCMs)** - replace part of the clinker with fly ash,
  slag, calcined clay or limestone powder. **LC3** (limestone calcined clay
  cement) can cut clinker to ~50% with comparable performance. This is the
  single biggest near-term lever.
- **Optimize the mix** - use only the cement you need; use superplasticizers to
  lower w/c and cement content; specify strength at **56 or 91 days** where the
  schedule allows, so slower SCM-rich mixes qualify.
- **Better aggregates and recycled content** - recycled concrete aggregate,
  optimized grading to reduce paste demand.
- **CO2 curing / mineralization** - inject CO2 that reacts and is permanently
  stored as carbonate in the concrete.
- **Novel binders** - alkali-activated (geopolymer) and calcined-clay systems
  that avoid or reduce Portland clinker.

A **carbon footprint** is quantified per unit of concrete and, better, per unit
of delivered strength:

```text
Embodied carbon of a mix (cradle-to-gate):
    GWP = sum( mass_i * EF_i )       kg CO2e per m3
      EF = emission factor of each material

Example (per m3):
    CEM I 320 kg x 0.90 kgCO2e/kg = 288
    Fly ash 80 kg x 0.01          =   0.8
    Aggregates 1850 kg x 0.005    =   9.3
    Water + admixture             ~   3
    Total ~ 301 kgCO2e/m3
Replacing 30% of CEM I with fly ash cuts ~86 kgCO2e/m3 (~28%).
Report per MPa: GWP / f_ck, to reward strength-efficient mixes.
```

```mermaid
graph TD
    CLK["Clinker is the CO2 hotspot"] --> SUB["Substitute clinker with SCMs and LC3"]
    CLK --> OPT["Optimize mix lower cement"]
    SUB --> LOW["Lower embodied carbon"]
    OPT --> LOW
    ALT["Novel binders geopolymer"] --> LOW
    CO2C["CO2 curing mineralization"] --> LOW
    LOW --> METRIC["Report kg CO2e per m3 and per MPa"]
```

Remember: clinker is the carbon problem, so the biggest lever is replacing it
with SCMs (LC3, fly ash, slag) while optimizing the mix - and you judge progress
by embodied carbon per cubic meter and, better, per MPa of delivered strength.
""",
        ),
        quiz_lesson(
            "Quiz: Low-carbon and sustainable concrete",
            (
                q(
                    "Where does most of concrete's CO2 footprint come from?",
                    (
                        opt("The mixing water"),
                        opt("The aggregates"),
                        opt(
                            "The clinker in cement - largely process CO2 from calcining "
                            "limestone plus the fuel to fire the kiln",
                            correct=True,
                        ),
                        opt("The steel formwork"),
                    ),
                    "About 60% of cement CO2 is process emissions from CaCO3 -> CaO + CO2; "
                    "clinker is the hotspot, so reducing it is the main lever.",
                ),
                q(
                    "What is the single biggest near-term strategy to cut concrete's carbon?",
                    (
                        opt("Adding more mixing water"),
                        opt(
                            "Clinker substitution - replacing part of the clinker with "
                            "SCMs such as fly ash, slag or calcined clay (e.g. LC3)",
                            correct=True,
                        ),
                        opt("Using a darker cement color"),
                        opt("Increasing the w/c ratio to use less cement"),
                    ),
                    "SCMs and blended cements like LC3 replace clinker with lower-carbon, "
                    "often performance-improving materials - the biggest lever today.",
                ),
                q(
                    "Why report embodied carbon per MPa of strength, not just per cubic meter?",
                    (
                        opt("Because volume is impossible to measure"),
                        opt(
                            "It rewards strength-efficient mixes - a higher-strength "
                            "low-carbon concrete may deliver the same capacity with less "
                            "material",
                            correct=True,
                        ),
                        opt("Because codes forbid per-cubic-meter reporting"),
                        opt("It has no engineering meaning"),
                    ),
                    "Normalizing GWP by f_ck credits mixes that achieve the required "
                    "performance with less carbon - a fairer functional comparison.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Which hydration product gives concrete its strength?",
                    (
                        opt("Calcium hydroxide (CH)"),
                        opt("Calcium silicate hydrate (C-S-H)", correct=True),
                        opt("Gypsum"),
                        opt("Ettringite only"),
                    ),
                    "C-S-H is the binding gel; CH provides the alkaline reserve that "
                    "protects steel but little strength.",
                ),
                q(
                    "Abrams' law says that, for workable concrete, compressive strength "
                    "depends mainly on...",
                    (
                        opt("the cement brand"),
                        opt("the water-cement ratio", correct=True),
                        opt("the ambient temperature at delivery"),
                        opt("the shape of the formwork"),
                    ),
                    "Lower w/c -> fewer capillary pores -> higher strength and lower permeability.",
                ),
                q(
                    "You design for f_ck = 25 MPa with a standard deviation s = 4 MPa. "
                    "The target mean strength f_cm is about...",
                    (
                        opt("about 25 MPa"),
                        opt("about 31.6 MPa", correct=True),
                        opt("about 20 MPa"),
                        opt("about 50 MPa"),
                    ),
                    "f_cm = f_ck + 1.65 s = 25 + 1.65 x 4 = 31.6 MPa.",
                ),
                q(
                    "A truck of concrete is too stiff to place well. The correct action is to...",
                    (
                        opt("add water from the hose to loosen it"),
                        opt(
                            "re-dose with a superplasticizer, gaining flow without raising "
                            "the w/c ratio",
                            correct=True,
                        ),
                        opt("place it as is and skip vibration"),
                        opt("add dry cement on top"),
                    ),
                    "Adding water raises w/c and destroys strength and durability; a "
                    "water-reducer restores workability at the same w/c.",
                ),
                q(
                    "Concrete is typically combined with steel reinforcement because "
                    "concrete is...",
                    (
                        opt("weak in compression"),
                        opt(
                            "weak in tension, while steel carries the tensile forces", correct=True
                        ),
                        opt("unable to resist any load alone"),
                        opt("too light without steel"),
                    ),
                    "Concrete is strong in compression but about ten times weaker in "
                    "tension; rebar takes the tension.",
                ),
                q(
                    "How do pozzolanic SCMs (fly ash, silica fume) improve concrete?",
                    (
                        opt("They evaporate faster than water"),
                        opt(
                            "They react with calcium hydroxide to form extra C-S-H, giving "
                            "a denser, less permeable, more durable paste",
                            correct=True,
                        ),
                        opt("They raise the w/c ratio"),
                        opt("They add chlorides to accelerate setting"),
                    ),
                    "The pozzolanic reaction consumes weak CH and makes more strength gel - "
                    "and replacing clinker lowers CO2.",
                ),
                q(
                    "Which best explains why adequate cover over the rebar is a "
                    "durability requirement?",
                    (
                        opt("It makes the concrete cheaper"),
                        opt(
                            "The cover must be deep enough that the carbonation (and "
                            "chloride) front does not reach the steel within the design life",
                            correct=True,
                        ),
                        opt("Cover has no effect on corrosion"),
                        opt("It only affects the concrete color"),
                    ),
                    "Carbonation depth grows as x = k*sqrt(t); the cover is sized so the "
                    "front stays short of the rebar over the service life.",
                ),
                q(
                    "What is the key difference between shrinkage and creep?",
                    (
                        opt("They are identical"),
                        opt(
                            "Shrinkage is volume change mainly from water loss even when "
                            "unloaded; creep is strain that grows under sustained load",
                            correct=True,
                        ),
                        opt("Shrinkage needs load; creep needs no load"),
                        opt("Both finish within one hour of casting"),
                    ),
                    "Drying shrinkage happens regardless of load; creep is time-dependent "
                    "strain under a held load - both drive cracking and deflection.",
                ),
                q(
                    "Self-compacting concrete (SCC) is accepted in the field using which test?",
                    (
                        opt("The standard slump cone height"),
                        opt("The slump-flow (spread diameter) test", correct=True),
                        opt("The 28-day cylinder crush only"),
                        opt("The carbonation depth test"),
                    ),
                    "SCC flows under its own weight; its consistency is measured by the "
                    "spread diameter (slump-flow), often with T500 and the J-ring.",
                ),
                q(
                    "What is the single biggest near-term lever to reduce concrete's "
                    "carbon footprint?",
                    (
                        opt("Using more mixing water"),
                        opt(
                            "Substituting clinker with SCMs and blended cements such as "
                            "LC3 (limestone calcined clay), while optimizing the mix",
                            correct=True,
                        ),
                        opt("Increasing the w/c ratio"),
                        opt("Painting structures white"),
                    ),
                    "Clinker is the CO2 hotspot, so replacing it with lower-carbon SCMs is "
                    "the main lever - judged by embodied carbon per m3 and per MPa.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CONCRETE_TECHNOLOGY_COURSES: tuple[SeedCourse, ...] = (_CONCRETE_TECHNOLOGY,)
