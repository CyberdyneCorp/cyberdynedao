"""Academy seed content - Engineering Geology.

The geological basis of civil engineering: how rocks and soils form and
behave, how groundwater moves, how the ground fails, and how site
investigation turns all of that into safe foundations, tunnels and dams.
Every lesson is a direct explanation with a concrete example - a design
formula, a classification table, or a field measurement - and a mermaid
diagram, followed by a checkpoint quiz; the course closes with a
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


_ENGINEERING_GEOLOGY = SeedCourse(
    slug="engineering-geology",
    title="Engineering Geology",
    description=(
        "The geological basis of civil engineering: rocks and soils, "
        "groundwater, geological hazards, and how site investigation informs "
        "foundations, tunnels and dams. Every lesson pairs a direct "
        "explanation with a real classification, formula or field method and "
        "a diagram, grounded in standards such as USCS, RQD and Eurocode 7."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Engineering Geology

Every structure a civil engineer builds - a house, a bridge, a tunnel, a
dam - ultimately rests on the **ground**. Engineering geology is the
discipline that reads the ground: what it is made of, how it formed, how
water moves through it, how it can fail, and what that means for design.
Get the geology wrong and no amount of clever structure above will save
you; get it right and the ground becomes a reliable partner.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it with a real example (a classification table, a
design formula, a worked mini-calculation), and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Minerals and rocks** - the three rock families and how they behave
2. **Weathering and soil formation** - how rock becomes soil
3. **Geological structures** - faults, folds and discontinuities
4. **Groundwater and aquifers** - how water moves through the ground
5. **Geological hazards** - landslides and mass movements
6. **Site investigation** - boreholes and geophysics
7. **Geology for structures** - foundations, tunnels and dams
8. **Geospatial hazard mapping** - GIS, remote sensing and monitoring

This is the map. Real projects blend all of it, but understanding each
piece on its own is what lets you read a site and design for it with
confidence.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Why does engineering geology matter for civil engineering?",
                    (
                        opt("It only matters for mining, not construction"),
                        opt(
                            "Every structure ultimately rests on the ground, so its "
                            "geology governs whether foundations, tunnels and dams are "
                            "safe",
                            correct=True,
                        ),
                        opt("It is only about identifying pretty crystals"),
                        opt("It replaces the need for structural design"),
                    ),
                    "The ground carries every structure; reading it correctly is the "
                    "foundation of safe design.",
                ),
                q(
                    "How is each lesson in this course structured?",
                    (
                        opt("A long theory dump with no examples"),
                        opt(
                            "A direct explanation with a concrete example and a diagram, "
                            "followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("Video lectures with no text"),
                    ),
                    "Explain one idea, show a real example, draw it, then check "
                    "understanding with a quiz.",
                ),
            ),
        ),
        # -- 1. Minerals and rocks -------------------------------------
        _t(
            "Minerals and rocks",
            "10 min",
            """# Minerals and rocks

A **mineral** is a naturally occurring solid with a definite chemical
composition and an ordered crystal structure - quartz, feldspar, mica,
calcite. A **rock** is an aggregate of one or more minerals. What the
minerals are, and how they are bound together, controls how strong,
durable and watertight the rock is for engineering.

Rocks are grouped into **three families** by how they form:

- **Igneous** - crystallized from molten magma or lava. **Intrusive**
  rocks (granite) cool slowly underground into coarse, interlocking
  crystals and are typically strong and durable. **Extrusive** rocks
  (basalt) cool fast at the surface into fine grains.
- **Sedimentary** - formed by deposition and **cementation** of
  weathered fragments or chemical precipitates: sandstone, shale,
  limestone. They occur in **beds** (layers) and their strength varies
  widely with the cement and porosity.
- **Metamorphic** - existing rock transformed by heat and pressure
  without melting: shale becomes slate, limestone becomes marble,
  granite becomes gneiss. Many develop **foliation** - a planar fabric
  that is a plane of weakness.

For engineering, a key strength measure is the **Unconfined Compressive
Strength (UCS)**. A rough field-to-lab classification:

```text
Rock strength by UCS (approx., after ISRM):
  Very weak      1 - 5 MPa     crumbles, weak shale
  Weak           5 - 25 MPa    weathered sandstone
  Medium strong  25 - 50 MPa   many limestones
  Strong         50 - 100 MPa  sound sandstone, marble
  Very strong    100 - 250 MPa fresh granite, basalt
```

A fresh granite at 150 MPa makes an excellent foundation rock; a weak,
laminated shale at 3 MPa may soften in water and needs great care.

```mermaid
graph TD
    MAGMA["Molten magma"] --> IGN["Igneous rock"]
    IGN --> WEATH["Weathering and erosion"]
    WEATH --> SED["Sedimentary rock"]
    SED --> HEATP["Heat and pressure"]
    IGN --> HEATP
    HEATP --> MET["Metamorphic rock"]
    MET --> MELT["Melting"]
    MELT --> MAGMA
```

Remember: identify the rock family and its minerals first - it predicts
strength, durability, and where the weaknesses will be.
""",
        ),
        quiz_lesson(
            "Quiz: Minerals and rocks",
            (
                q(
                    "How do the three rock families form?",
                    (
                        opt("All three crystallize from magma"),
                        opt(
                            "Igneous from cooling magma, sedimentary from deposition and "
                            "cementation, metamorphic from heat and pressure on existing "
                            "rock",
                            correct=True,
                        ),
                        opt("They are defined only by their color"),
                        opt("Sedimentary rocks form by melting"),
                    ),
                    "The rock cycle: melt to igneous, weather and cement to sedimentary, "
                    "cook under pressure to metamorphic.",
                ),
                q(
                    "Why does a coarse-grained granite tend to be stronger than a "
                    "fine-grained volcanic ash?",
                    (
                        opt("It is a different color"),
                        opt(
                            "It cooled slowly underground, forming large interlocking "
                            "crystals that bind the rock tightly",
                            correct=True,
                        ),
                        opt("It contains more water"),
                        opt("It is always younger"),
                    ),
                    "Slow intrusive cooling gives coarse, interlocking crystals - a "
                    "durable, high-strength fabric.",
                ),
                q(
                    "What does the Unconfined Compressive Strength (UCS) describe?",
                    (
                        opt("How much water a rock can hold"),
                        opt("The color index of the rock"),
                        opt(
                            "The stress an intact rock sample can carry before failing "
                            "in compression, used to rank rock strength",
                            correct=True,
                        ),
                        opt("The age of the rock in millions of years"),
                    ),
                    "UCS in MPa is the standard intact-strength measure - fresh granite "
                    "is very strong, weak shale is very weak.",
                ),
            ),
        ),
        # -- 2. Weathering and soil formation --------------------------
        _t(
            "Weathering and soil formation",
            "10 min",
            """# Weathering and soil formation

**Weathering** is the breakdown of rock in place, at or near the surface.
It is what turns solid rock into the **soil** that most foundations
actually sit on, and it controls how deep you must go to reach sound
ground. There are two kinds, usually acting together:

- **Physical (mechanical) weathering** breaks rock into smaller pieces
  without changing its chemistry: freeze-thaw wedging in cracks, thermal
  expansion, unloading and root growth. It produces **coarse** debris.
- **Chemical weathering** alters the minerals themselves: feldspar
  reacts with water and carbon dioxide to form **clay minerals**;
  limestone dissolves in weak acid. It produces **fine** particles and
  is fastest in warm, wet climates - which is why deep tropical
  weathering profiles (common in Brazil) can be tens of metres thick.

The result grades from fresh rock up to residual soil. Engineers log
this with a **weathering grade** scale:

```text
Weathering grades (ISRM, W1 to W6):
  W1  Fresh          no visible weathering
  W2  Slightly       discoloration on surfaces
  W3  Moderately     less than half decomposed to soil
  W4  Highly         more than half decomposed to soil
  W5  Completely     all rock decomposed to soil, fabric intact
  W6  Residual soil  fabric destroyed, engineering soil
```

Soil formed on the spot from the rock below is **residual soil**; soil
carried and deposited elsewhere (by rivers, wind, gravity, ice) is
**transported soil** - alluvial, aeolian, colluvial, glacial. The two
behave very differently: residual soils keep a "relict" structure from
the parent rock, while transported soils are sorted by the process that
moved them.

```mermaid
graph TD
    ROCK["Fresh bedrock"] --> PHYS["Physical weathering"]
    ROCK --> CHEM["Chemical weathering"]
    PHYS --> GRADE["Weathering profile W1 to W6"]
    CHEM --> GRADE
    GRADE --> RES["Residual soil in place"]
    GRADE --> TRANS["Transported soil moved and deposited"]
```

Remember: weathering sets how far down "good ground" begins, and whether
the soil above it is residual (relict structure) or transported (sorted
by how it arrived).
""",
        ),
        quiz_lesson(
            "Quiz: Weathering and soil formation",
            (
                q(
                    "What is the difference between physical and chemical weathering?",
                    (
                        opt("Physical only happens underwater"),
                        opt(
                            "Physical breaks rock into smaller pieces without changing "
                            "chemistry; chemical alters the minerals themselves, forming "
                            "clays or dissolving rock",
                            correct=True,
                        ),
                        opt("They are two names for the same process"),
                        opt("Chemical weathering only affects metals"),
                    ),
                    "Physical = mechanical break-up (coarse debris); chemical = mineral "
                    "alteration (fine clays), fastest when warm and wet.",
                ),
                q(
                    "What does a weathering grade of W6 (residual soil) indicate?",
                    (
                        opt("Fresh, unweathered rock"),
                        opt("Rock discolored only on the surfaces"),
                        opt(
                            "The rock has fully decomposed to an engineering soil with "
                            "its original fabric destroyed",
                            correct=True,
                        ),
                        opt("A rock that cannot weather any further because it is metal"),
                    ),
                    "W1 is fresh rock, W6 is residual soil; the grade tells you how deep "
                    "sound ground lies.",
                ),
                q(
                    "How does residual soil differ from transported soil?",
                    (
                        opt("Residual soil is always stronger"),
                        opt(
                            "Residual soil forms in place from the rock below and keeps "
                            "a relict structure; transported soil is moved and deposited, "
                            "sorted by the process that carried it",
                            correct=True,
                        ),
                        opt("Transported soil never contains clay"),
                        opt("They behave identically in foundations"),
                    ),
                    "In-place vs moved: residual keeps parent-rock structure, "
                    "transported is sorted by river, wind, gravity or ice.",
                ),
            ),
        ),
        # -- 3. Geological structures ----------------------------------
        _t(
            "Geological structures",
            "10 min",
            """# Geological structures

Rock masses are rarely intact blocks. Over geological time, tectonic
forces bend and break them, leaving **structures** - and in most rock,
the strength of the *mass* is governed not by the intact rock but by
these **discontinuities**: the planes along which it is weak.

The main structures:

- **Folds** - layers bent by compression. An upfold is an **anticline**,
  a downfold a **syncline**. Folding tilts beds and can concentrate
  fracturing at the sharply curved hinges.
- **Faults** - fractures along which the two sides have **moved
  relative to each other**. Normal faults (extension), reverse/thrust
  faults (compression) and strike-slip faults (sideways). Faults are
  crushed, weak, water-bearing zones and may be seismically active.
- **Joints** - fractures with **no** relative movement, usually in
  regular sets. They are the most common discontinuity and control how
  a rock mass drains, weathers and fails.
- **Bedding** and **foliation** - the layering in sedimentary and
  metamorphic rock, themselves planes of weakness.

A discontinuity is described by its **orientation**, given as **dip and
dip direction**: the dip is the steepest angle the plane makes with
horizontal, the dip direction the compass bearing it slopes toward.

```text
Orientation example (dip / dip direction):
  Joint set 1:  75 / 090   steep, dipping east
  Joint set 2:  30 / 250   shallow, dipping WSW
  Bedding:      10 / 180    gently south

Rule of thumb for a rock slope:
  a plane that "daylights" (dips out of the face) at an
  angle steeper than its friction angle can slide.
```

If a joint dips out of a cut slope more steeply than the friction along
it, the block above can slide - the basis of **kinematic** slope
analysis. That is why mapping orientations, not just rock type, is
essential.

```mermaid
graph TD
    STRESS["Tectonic stress"] --> FOLD["Folds anticline and syncline"]
    STRESS --> FAULT["Faults with movement"]
    STRESS --> JOINT["Joints no movement"]
    FOLD --> DISC["Discontinuities in the rock mass"]
    FAULT --> DISC
    JOINT --> DISC
    DISC --> BEHAV["Mass strength and slope stability"]
```

Remember: the rock mass is only as strong as its discontinuities - map
their orientation, spacing and condition, because they, not the intact
rock, usually decide how it fails.
""",
        ),
        quiz_lesson(
            "Quiz: Geological structures",
            (
                q(
                    "What is the difference between a joint and a fault?",
                    (
                        opt("A joint is bigger than a fault"),
                        opt(
                            "A fault is a fracture along which the two sides have moved "
                            "relative to each other; a joint is a fracture with no "
                            "relative movement",
                            correct=True,
                        ),
                        opt("A joint only occurs in soil"),
                        opt("Faults never carry water"),
                    ),
                    "Movement is the distinction: faults slipped (weak, crushed zones), "
                    "joints did not.",
                ),
                q(
                    "Why is the strength of a rock mass often governed by its "
                    "discontinuities rather than the intact rock?",
                    (
                        opt("Because intact rock has no strength at all"),
                        opt(
                            "Discontinuities are planes of weakness along which the mass "
                            "can slide, drain and weather, so they usually control how "
                            "it fails",
                            correct=True,
                        ),
                        opt("Because discontinuities are always vertical"),
                        opt("Because intact rock is always weaker than joints"),
                    ),
                    "A strong rock cut by adversely oriented joints can still fail along "
                    "them - map the planes.",
                ),
                q(
                    "What does 'dip and dip direction' describe?",
                    (
                        opt("The rock's chemical composition"),
                        opt("The age of the fault"),
                        opt(
                            "The orientation of a discontinuity: the steepest angle it "
                            "makes with horizontal and the compass bearing it slopes "
                            "toward",
                            correct=True,
                        ),
                        opt("The temperature at which the rock formed"),
                    ),
                    "Orientation drives kinematic slope analysis - a plane daylighting "
                    "steeper than its friction angle can slide.",
                ),
            ),
        ),
        # -- 4. Groundwater and aquifers -------------------------------
        _t(
            "Groundwater and aquifers",
            "10 min",
            """# Groundwater and aquifers

Water in the ground is central to almost every geotechnical problem: it
reduces soil strength, drives landslides, floods excavations, and attacks
foundations. Below the **water table**, the pores and fractures of the
ground are fully saturated.

Two key properties describe how ground holds and moves water:

- **Porosity** - the fraction of the volume that is void space (how much
  water it can hold).
- **Permeability** (hydraulic conductivity, k) - how easily water flows
  through it. Clean gravel is highly permeable; clay has high porosity
  but very low permeability.

A rock or soil that both stores and transmits useful water is an
**aquifer** (sand, gravel, fractured limestone). A low-permeability layer
that holds water back is an **aquitard** (clay). An **unconfined**
aquifer has the water table as its upper surface; a **confined** aquifer
is trapped between aquitards under pressure, so water in a well rises
above the aquifer top (an artesian condition).

Groundwater flow through soil follows **Darcy's law** - flow is
proportional to permeability and to the hydraulic gradient:

```text
Darcy's law:
  Q = k * i * A

  Q = flow rate (m3/s)
  k = hydraulic conductivity (m/s)
  i = hydraulic gradient = head drop / flow length (dimensionless)
  A = cross-sectional area of flow (m2)

Worked example:
  k = 1e-4 m/s (sand), head drop 2 m over 40 m length, A = 10 m2
  i = 2 / 40 = 0.05
  Q = 1e-4 * 0.05 * 10 = 5e-5 m3/s = 0.05 L/s
```

The critical engineering point is **pore water pressure**. Water in the
pores carries part of the load, reducing the **effective stress** that
holds soil grains together (Terzaghi: effective stress = total stress
minus pore pressure). Raise the pore pressure - by rain, a rising water
table, or a blocked drain - and you lower effective stress and strength.
That is the trigger behind a great many failures.

```mermaid
graph TD
    RAIN["Rainfall recharge"] --> WT["Water table"]
    WT --> UNCON["Unconfined aquifer"]
    AQT["Aquitard low permeability"] --> CONF["Confined aquifer under pressure"]
    UNCON --> FLOW["Darcy flow Q equals k i A"]
    CONF --> FLOW
    FLOW --> PWP["Pore water pressure"]
    PWP --> EFF["Lower effective stress and strength"]
```

Remember: know where the water table is and how pore pressure changes -
it is usually the difference between stable ground and failure.
""",
        ),
        quiz_lesson(
            "Quiz: Groundwater and aquifers",
            (
                q(
                    "What is the difference between porosity and permeability?",
                    (
                        opt("They are the same property"),
                        opt(
                            "Porosity is how much void space (water) the ground can "
                            "hold; permeability is how easily water flows through it",
                            correct=True,
                        ),
                        opt("Porosity only applies to rock, permeability only to soil"),
                        opt("Permeability measures the color of the water"),
                    ),
                    "Clay shows the contrast: high porosity but very low permeability.",
                ),
                q(
                    "In Darcy's law Q = k i A, what is the hydraulic gradient i?",
                    (
                        opt("The permeability of the soil"),
                        opt("The total flow area"),
                        opt(
                            "The head drop divided by the flow length - a dimensionless "
                            "measure of the driving slope of the water",
                            correct=True,
                        ),
                        opt("The temperature of the groundwater"),
                    ),
                    "i = head loss / distance; multiply by k and A to get the flow rate.",
                ),
                q(
                    "How does rising pore water pressure make ground more likely to fail?",
                    (
                        opt("It has no effect on strength"),
                        opt(
                            "It reduces effective stress (total stress minus pore "
                            "pressure), lowering the strength holding the soil grains "
                            "together",
                            correct=True,
                        ),
                        opt("It freezes the soil solid"),
                        opt("It increases the rock's UCS"),
                    ),
                    "Terzaghi's effective stress principle: more pore pressure, less "
                    "effective stress, less strength - a classic failure trigger.",
                ),
            ),
        ),
        # -- 5. Geological hazards and mass movements ------------------
        _t(
            "Geological hazards and mass movements",
            "10 min",
            """# Geological hazards and mass movements

The ground itself can be the hazard. **Mass movement** (or mass wasting)
is the downslope movement of rock, soil or debris under gravity -
landslides in the broad sense. They are among the most damaging natural
hazards, and in most cases their causes are understandable and
predictable.

Movements are classified by **material** and by **type of movement**:

- **Falls** - blocks detaching from a steep face and free-falling
  (rockfall).
- **Slides** - a coherent mass moving on a defined surface. **Rotational
  slides** (slumps) move on a curved surface, common in clay; **planar
  slides** move on a flat plane such as a joint or bedding, common in
  rock.
- **Flows** - the material behaves like a fluid: **debris flows** and
  **mudflows**, often triggered by intense rain, which are deadly and
  fast. These cause many fatalities on steep tropical slopes.
- **Creep** - very slow, continuous downslope movement, revealed by bent
  trees and tilted poles.

A slope's stability is summarized by the **Factor of Safety (FoS)** - the
ratio of resisting forces to driving forces:

```text
Factor of Safety:
  FoS = resisting forces / driving forces
      = shear strength available / shear stress required

  FoS > 1   stable (design usually needs 1.3 to 1.5)
  FoS = 1   limiting equilibrium (on the verge)
  FoS < 1   failure

Triggers reduce FoS by either:
  - raising driving force  (steeper cut, added load, earthquake shaking)
  - lowering resistance    (rain raising pore pressure, weathering,
                            toe erosion, vegetation removal)
```

A slope can sit at FoS just above 1 for years, then fail when a heavy
rain raises pore water pressure - the effective-stress link from the last
lesson. Understanding the trigger is the key to prevention: drainage,
regrading, retaining structures, and early-warning monitoring.

```mermaid
graph TD
    GRAV["Gravity on the slope"] --> DRIVE["Driving forces"]
    STR["Shear strength"] --> RESIST["Resisting forces"]
    DRIVE --> FOS["Factor of safety ratio"]
    RESIST --> FOS
    RAIN["Rain raises pore pressure"] --> DRIVE
    TOE["Toe erosion or steep cut"] --> DRIVE
    FOS --> FAIL["Below one means failure"]
```

Remember: mass movement is gravity beating strength. Classify the
movement, quantify the Factor of Safety, and identify the trigger that
tips it below one.
""",
        ),
        quiz_lesson(
            "Quiz: Geological hazards and mass movements",
            (
                q(
                    "What does a slope's Factor of Safety represent?",
                    (
                        opt("The steepness of the slope in degrees"),
                        opt(
                            "The ratio of resisting forces to driving forces; below 1 "
                            "means failure",
                            correct=True,
                        ),
                        opt("The number of landslides that have occurred"),
                        opt("The permeability of the slope material"),
                    ),
                    "FoS = resisting / driving; design typically targets 1.3 to 1.5, and "
                    "FoS = 1 is limiting equilibrium.",
                ),
                q(
                    "How does a rotational slide differ from a planar slide?",
                    (
                        opt("A rotational slide only happens in rock"),
                        opt(
                            "A rotational slide moves on a curved surface (common in "
                            "clay); a planar slide moves on a flat plane such as a joint "
                            "or bedding (common in rock)",
                            correct=True,
                        ),
                        opt("They are identical"),
                        opt("A planar slide is always slower than creep"),
                    ),
                    "Curved failure surface = rotational (slump); flat discontinuity = "
                    "planar slide.",
                ),
                q(
                    "Why does heavy rainfall so often trigger landslides?",
                    (
                        opt("Rain increases the rock's UCS"),
                        opt("Rain has no effect on slopes"),
                        opt(
                            "It raises pore water pressure, which lowers effective "
                            "stress and shear strength, dropping the Factor of Safety "
                            "below 1",
                            correct=True,
                        ),
                        opt("Rain only causes rockfalls, never flows"),
                    ),
                    "The effective-stress link again: pore pressure up, resistance down, "
                    "a marginal slope fails.",
                ),
            ),
        ),
        # -- 6. Site investigation methods -----------------------------
        _t(
            "Site investigation methods",
            "10 min",
            """# Site investigation methods

You cannot design safely for ground you have not investigated. A **site
investigation (SI)** builds a picture of the subsurface - the ground
model - before design. It has direct and indirect methods, and good
practice combines them.

The staged approach:

- **Desk study and walkover** - existing geological maps, air photos,
  historical records, and a site visit. Cheap, and it targets everything
  that follows.
- **Boreholes** - the direct backbone of SI: drilling to bring up soil
  and rock **samples** and to install instruments. Samples let you
  classify and lab-test the ground; the borehole log records the
  sequence with depth.
- **In-situ tests** - measurements in the ground itself. The **Standard
  Penetration Test (SPT)** counts the blows N to drive a sampler 300 mm
  and indexes soil density; the **Cone Penetration Test (CPT)** pushes
  an instrumented cone for a continuous strength profile.
- **Geophysics** - indirect, non-intrusive imaging between boreholes:
  **seismic refraction** (wave speed rises with rock quality and depth
  to bedrock), **electrical resistivity** (maps clay, water and
  cavities). It is fast and areal but must be **calibrated** against
  boreholes - it infers, it does not sample.

For rock cores, the key quality index is the **Rock Quality Designation
(RQD)**:

```text
Rock Quality Designation (RQD):
  RQD = (sum of intact core pieces >= 100 mm) / (total core run) * 100

Example: a 2.0 m core run; sound pieces >= 100 mm total 1.5 m
  RQD = 1.5 / 2.0 * 100 = 75 %   ->  "Fair" rock

  RQD classes:  0-25 Very poor | 25-50 Poor | 50-75 Fair
                75-90 Good     | 90-100 Excellent
```

Boreholes give hard truth at points; geophysics interpolates cheaply
between them. Combine them so the ground model is both accurate and
continuous - and always investigate deep enough to cover the zone your
structure will stress.

```mermaid
graph TD
    DESK["Desk study and walkover"] --> PLAN["Investigation plan"]
    PLAN --> BH["Boreholes and sampling"]
    PLAN --> INSITU["In situ tests SPT and CPT"]
    PLAN --> GEO["Geophysics seismic and resistivity"]
    BH --> MODEL["Ground model"]
    INSITU --> MODEL
    GEO --> CAL["Calibrate against boreholes"]
    CAL --> MODEL
    MODEL --> DESIGN["Input to design"]
```

Remember: boreholes sample the truth at points, geophysics fills the gaps
between them - use both, calibrate one against the other, and build a
ground model before you design.
""",
        ),
        quiz_lesson(
            "Quiz: Site investigation methods",
            (
                q(
                    "Why combine boreholes with geophysics in a site investigation?",
                    (
                        opt("Geophysics is always more accurate than boreholes"),
                        opt(
                            "Boreholes give direct samples at points but are sparse; "
                            "geophysics images cheaply between them but must be "
                            "calibrated against the boreholes",
                            correct=True,
                        ),
                        opt("Boreholes are only for water wells"),
                        opt("Geophysics samples the soil directly"),
                    ),
                    "Direct-at-points plus indirect-continuous gives a ground model that "
                    "is both accurate and complete.",
                ),
                q(
                    "What does the Rock Quality Designation (RQD) measure?",
                    (
                        opt("The chemical composition of the rock"),
                        opt(
                            "The percentage of a core run made up of sound intact pieces "
                            "at least 100 mm long - an index of rock mass quality",
                            correct=True,
                        ),
                        opt("The depth of the water table"),
                        opt("The number of boreholes drilled"),
                    ),
                    "RQD = sum of pieces >= 100 mm / total run x 100; higher percent "
                    "means better, less fractured rock.",
                ),
                q(
                    "What does the Standard Penetration Test (SPT) N-value index?",
                    (
                        opt("The temperature of the ground"),
                        opt("The permeability in m/s"),
                        opt(
                            "The density or consistency of soil, from the blow count to "
                            "drive a sampler 300 mm",
                            correct=True,
                        ),
                        opt("The age of the rock"),
                    ),
                    "SPT counts blows N per 300 mm - a quick in-situ index of soil "
                    "density and strength.",
                ),
            ),
        ),
        # -- 7. Geology for foundations, tunnels and dams --------------
        _t(
            "Geology for foundations, tunnels and dams",
            "11 min",
            """# Geology for foundations, tunnels and dams

Everything so far - rock type, weathering, structures, groundwater,
hazards, investigation - feeds one purpose: designing structures that
work with the ground. Three classic problems show how.

**Foundations** transfer a structure's load into the ground. If competent
ground is shallow, a **shallow foundation** (a footing or raft) spreads
the load near the surface. If good ground is deep - beneath soft or
weathered material - **deep foundations** (piles) carry the load down to
it. The ground must resist without failing (**bearing capacity**) and
without settling too much (**settlement**).

```text
Shallow footing check (simplified):
  bearing pressure  q = P / A     (load / footing area)
  require:  q <= q_allow = q_ult / FoS   (FoS often 3 for bearing)

Example: column load P = 900 kN, allowable q_allow = 200 kPa
  required area A >= P / q_allow = 900 / 200 = 4.5 m2
  -> a footing about 2.2 m x 2.2 m
```

**Tunnels** are built entirely within the ground, so geology is
everything. The **rock mass quality** decides how it behaves and what
support it needs. Weak, blocky or squeezing ground needs heavy support; a
**fault or water-bearing zone** intersected underground can flood or
collapse the heading. Classification systems (**RMR**, the **Q-system**,
both fed by RQD, joint condition and groundwater) turn the ground model
into support recommendations.

**Dams** impound water, so two geological questions dominate: can the
foundation carry the load without failing, and will water **leak**
through or under it? A permeable or faulted foundation can lose the
reservoir or, worse, suffer **internal erosion (piping)** where seeping
water carries soil particles away - a leading cause of embankment dam
failure. The classic treatment is a **grout curtain** to cut off seepage
under the dam.

```mermaid
graph TD
    GM["Ground model"] --> FND["Foundations bearing and settlement"]
    GM --> TUN["Tunnels rock mass and support"]
    GM --> DAM["Dams stability and seepage"]
    FND --> SAFE["Safe structure"]
    TUN --> SAFE
    DAM --> SEEP["Control seepage with grout curtain"]
    SEEP --> SAFE
```

Remember: the same ground model answers different questions for each
structure - bearing and settlement for foundations, rock-mass support for
tunnels, stability and seepage control for dams.
""",
        ),
        quiz_lesson(
            "Quiz: Geology for foundations, tunnels and dams",
            (
                q(
                    "When are deep (pile) foundations used instead of shallow footings?",
                    (
                        opt("Whenever the building is tall, regardless of ground"),
                        opt(
                            "When competent ground is deep, beneath soft or weathered "
                            "material, so load must be carried down to it",
                            correct=True,
                        ),
                        opt("Only in dry climates"),
                        opt("Never - shallow footings always work"),
                    ),
                    "Shallow ground good = spread the load near surface; good ground "
                    "deep = pile down to it.",
                ),
                q(
                    "Why is geology 'everything' for a tunnel?",
                    (
                        opt("Because tunnels are always in soil, never rock"),
                        opt(
                            "The tunnel is built entirely within the ground, so rock "
                            "mass quality and features like faults or water-bearing "
                            "zones decide behavior and the support needed",
                            correct=True,
                        ),
                        opt("Because tunnels do not need any support"),
                        opt("Because tunnels carry no load"),
                    ),
                    "RMR and the Q-system turn the ground model into support "
                    "requirements; a fault or water zone can flood or collapse a "
                    "heading.",
                ),
                q(
                    "What is 'piping' (internal erosion) in a dam foundation, and why "
                    "does it matter?",
                    (
                        opt("Water flowing through the dam's drainage pipes as designed"),
                        opt(
                            "Seeping water progressively carrying soil particles away, "
                            "eroding a channel that can lead to dam failure",
                            correct=True,
                        ),
                        opt("A method of measuring reservoir depth"),
                        opt("The freezing of water in the reservoir"),
                    ),
                    "Piping is a leading cause of embankment dam failure; a grout "
                    "curtain cuts off the seepage that drives it.",
                ),
            ),
        ),
        # -- 8. Geospatial hazard mapping and monitoring ---------------
        _t(
            "Geospatial hazard mapping and monitoring",
            "10 min",
            """# Geospatial hazard mapping and monitoring

Modern engineering geology is increasingly **digital and geospatial**. A
single borehole tells you about one point; hazards act across whole
hillsides, valleys and cities. Geospatial tools let us map, predict and
watch the ground at that scale - and warn before it fails.

The digital toolkit:

- **GIS (Geographic Information System)** - the platform that layers
  geology, slope, rainfall, land use and past-failure data on a map, so
  they can be combined and analyzed together.
- **Remote sensing** - satellite and aerial imagery, and **LiDAR** that
  strips vegetation to reveal a bare-earth terrain model exposing old
  landslide scars invisible on the ground.
- **Drones and photogrammetry** - low-cost, high-resolution surveys of
  cuts, quarries and slopes, repeatable to detect change.
- **InSAR** - satellite radar interferometry that measures ground
  movement to **millimetre** precision over wide areas, catching slow
  creep before collapse.
- **IoT and ML** - in-ground sensors (piezometers for pore pressure,
  inclinometers for movement) streaming live data; machine learning
  turns rainfall and movement histories into failure predictions.

A **landslide susceptibility map** combines the controlling factors in
GIS to score each location:

```text
Susceptibility (weighted-overlay concept):
  S = w1*slope + w2*geology + w3*rainfall + w4*land_use ...
      (each factor rated, weights w sum to 1)

  Low | Moderate | High | Very high   susceptibility zones

Early-warning chain:
  sensors -> live data -> threshold (e.g. pore pressure or
  rainfall intensity) exceeded -> alert -> evacuate / restrict
```

The payoff is prediction and **early warning**: sensors feeding live data
against thresholds can trigger an alert - and an evacuation - hours
before a slope lets go, turning a disaster into a near miss. This is
where engineering geology meets the wider digital-twin and smart-monitoring
practice reshaping civil engineering.

```mermaid
graph TD
    DATA["Geology slope rainfall data"] --> GIS["GIS layers"]
    RS["Remote sensing LiDAR and InSAR"] --> GIS
    GIS --> SUSC["Susceptibility map"]
    SENS["IoT sensors piezometers"] --> LIVE["Live monitoring"]
    LIVE --> ML["Machine learning prediction"]
    SUSC --> WARN["Early warning and planning"]
    ML --> WARN
```

Remember: geospatial mapping and live monitoring extend geology from a
point to a landscape and from a snapshot to real time - the basis of
prediction and early warning.
""",
        ),
        quiz_lesson(
            "Quiz: Geospatial hazard mapping and monitoring",
            (
                q(
                    "What is the role of GIS in geological hazard mapping?",
                    (
                        opt("It drills the boreholes"),
                        opt(
                            "It layers and combines spatial data - geology, slope, "
                            "rainfall, land use, past failures - so they can be analyzed "
                            "together across an area",
                            correct=True,
                        ),
                        opt("It measures the UCS of rock samples"),
                        opt("It replaces the need for any field data"),
                    ),
                    "GIS is the platform that overlays the controlling factors to score "
                    "susceptibility across a landscape.",
                ),
                q(
                    "What does InSAR (satellite radar interferometry) provide for slope "
                    "monitoring?",
                    (
                        opt("The chemical composition of the soil"),
                        opt("The exact borehole depth"),
                        opt(
                            "Millimetre-precision measurement of ground movement over "
                            "wide areas, catching slow creep before collapse",
                            correct=True,
                        ),
                        opt("The rock's RQD value"),
                    ),
                    "InSAR detects tiny, wide-area displacement remotely - an early "
                    "signal of instability.",
                ),
                q(
                    "How does an early-warning system turn monitoring into safety?",
                    (
                        opt("By making the slope stronger automatically"),
                        opt(
                            "Live sensor data is compared against thresholds (e.g. pore "
                            "pressure or rainfall); exceeding them triggers an alert and "
                            "evacuation before failure",
                            correct=True,
                        ),
                        opt("By predicting the exact day a slope formed"),
                        opt("By replacing the site investigation"),
                    ),
                    "Sensors to data to threshold to alert: warning hours ahead turns a "
                    "disaster into a near miss.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "How are the three rock families distinguished?",
                    (
                        opt("By color alone"),
                        opt(
                            "By how they form: igneous from cooling magma, sedimentary "
                            "from deposition and cementation, metamorphic from heat and "
                            "pressure",
                            correct=True,
                        ),
                        opt("By their age only"),
                        opt("All three form by melting"),
                    ),
                    "Formation process defines the family and predicts engineering behavior.",
                ),
                q(
                    "What distinguishes residual soil from transported soil?",
                    (
                        opt("Residual soil is always coarser"),
                        opt(
                            "Residual soil forms in place from the rock below and keeps "
                            "a relict structure; transported soil was moved and "
                            "deposited, sorted by the carrying process",
                            correct=True,
                        ),
                        opt("Transported soil never holds water"),
                        opt("They behave identically"),
                    ),
                    "In-place weathering vs moved-and-deposited - a fundamental "
                    "distinction for behavior.",
                ),
                q(
                    "Why is a rock mass often only as strong as its discontinuities?",
                    (
                        opt("Because intact rock has no strength"),
                        opt(
                            "Joints, faults and bedding are planes of weakness along "
                            "which the mass can slide and fail, usually governing its "
                            "behavior",
                            correct=True,
                        ),
                        opt("Because discontinuities are always horizontal"),
                        opt("Because the intact rock always fails first"),
                    ),
                    "Map orientation, spacing and condition of discontinuities - they, "
                    "not the intact rock, tend to control failure.",
                ),
                q(
                    "In Darcy's law Q = k i A, what does k represent?",
                    (
                        opt("The porosity fraction"),
                        opt(
                            "The hydraulic conductivity (permeability) - how easily "
                            "water flows through the ground",
                            correct=True,
                        ),
                        opt("The hydraulic gradient"),
                        opt("The cross-sectional area"),
                    ),
                    "k is permeability; i is the gradient and A the area - together they "
                    "give the flow rate.",
                ),
                q(
                    "According to the effective-stress principle, how does rising pore "
                    "water pressure affect soil strength?",
                    (
                        opt("It increases strength"),
                        opt("It has no effect"),
                        opt(
                            "It reduces effective stress (total stress minus pore "
                            "pressure), lowering strength - a common failure trigger",
                            correct=True,
                        ),
                        opt("It only changes the soil color"),
                    ),
                    "More pore pressure means less effective stress and less strength - "
                    "the link behind many landslides.",
                ),
                q(
                    "A slope has a Factor of Safety of 0.9. What does this mean?",
                    (
                        opt("The slope is very stable"),
                        opt(
                            "Driving forces exceed resisting forces, so the slope is "
                            "failing (FoS below 1)",
                            correct=True,
                        ),
                        opt("The slope is exactly at limiting equilibrium"),
                        opt("The slope is 90 degrees steep"),
                    ),
                    "FoS = resisting / driving; below 1 means failure, 1 is limiting "
                    "equilibrium, design targets 1.3 to 1.5.",
                ),
                q(
                    "What does a Rock Quality Designation (RQD) of 90 percent indicate?",
                    (
                        opt("Very poor, highly fractured rock"),
                        opt(
                            "Excellent-quality rock - 90 percent of the core run is "
                            "sound intact pieces at least 100 mm long",
                            correct=True,
                        ),
                        opt("The rock is 90 million years old"),
                        opt("The water table is 90 m deep"),
                    ),
                    "RQD 90-100 percent is 'Excellent'; it indexes how intact and "
                    "unfractured the rock mass is.",
                ),
                q(
                    "Why should a site investigation combine boreholes and geophysics?",
                    (
                        opt("Geophysics samples the ground directly"),
                        opt(
                            "Boreholes give direct truth at sparse points while "
                            "geophysics images cheaply between them and is calibrated "
                            "against the boreholes",
                            correct=True,
                        ),
                        opt("Boreholes are only for measuring temperature"),
                        opt("They give the same information, so either alone is enough"),
                    ),
                    "Point-accurate plus area-continuous, one calibrating the other, "
                    "builds a reliable ground model.",
                ),
                q(
                    "For a dam foundation, which two geological questions dominate?",
                    (
                        opt("Rock color and mineral names"),
                        opt(
                            "Can the foundation carry the load without failing, and will "
                            "water leak through or under it (seepage and piping)",
                            correct=True,
                        ),
                        opt("How old the rock is and its RQD only"),
                        opt("The height of the dam and its paint"),
                    ),
                    "Stability and seepage - a grout curtain is the classic cutoff for "
                    "the seepage that drives piping.",
                ),
                q(
                    "How does modern geospatial monitoring improve on a single borehole "
                    "for hazards?",
                    (
                        opt("It does not - a borehole is always enough"),
                        opt(
                            "GIS, remote sensing (LiDAR, InSAR) and IoT sensors extend "
                            "geology from a point to a landscape and from a snapshot to "
                            "real time, enabling prediction and early warning",
                            correct=True,
                        ),
                        opt("It only measures rock color from space"),
                        opt("It replaces the need for any ground investigation"),
                    ),
                    "Hazards act across landscapes and over time; geospatial tools map "
                    "and watch them at that scale to warn before failure.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENGINEERING_GEOLOGY_COURSES: tuple[SeedCourse, ...] = (_ENGINEERING_GEOLOGY,)
