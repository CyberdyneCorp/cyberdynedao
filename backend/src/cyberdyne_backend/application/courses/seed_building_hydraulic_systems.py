"""Academy seed content - Building Hydraulic and Fire Systems.

The plumbing and fire-protection systems that keep a building safe and
livable: cold and hot water supply, sanitary sewage and venting, rainwater
drainage, reservoirs and pumps, water reuse and rainwater harvesting, and
fire-fighting systems (hydrants and sprinklers). It closes with how these
flows are sized and pressurized, and how the whole MEP set is coordinated
in BIM. Every lesson is a direct explanation grounded in Brazilian NBR and
international practice, with a worked sizing or pressure calculation and a
mermaid diagram, followed by a checkpoint quiz; the course ends with a
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


_BUILDING_HYDRAULIC_SYSTEMS = SeedCourse(
    slug="building-hydraulic-systems",
    title="Building Hydraulic & Fire Systems",
    description=(
        "The water, sewage, stormwater and fire-protection systems inside "
        "buildings - sizing, pressure, reuse, and coordinating MEP in BIM. "
        "Every lesson explains one system directly, works a real sizing or "
        "pressure calculation, and draws the flow as a diagram, grounded in "
        "NBR/ABNT and international practice."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Building Hydraulic and Fire Systems

Every building is a small water utility. Clean water arrives, is stored,
pressurized and distributed hot and cold; wastewater and sewage leave
safely; rain is caught and drained; and a separate, always-ready system
stands by to fight fire. Get any of these wrong and you get low pressure,
noise, backflow of sewer gas, flooding, or - at worst - a fire with no
water.

This course walks the water through a building, system by system. The
approach is **concrete**: each lesson explains one system directly, works
a real **sizing or pressure calculation** (pipe diameters, head loss,
reservoir volume, pump head), and draws the flow as a diagram. After each
lesson there is a short quiz; a final quiz covers everything.

What you will learn, in order:

1. **Cold and hot water supply** - how potable water is distributed
2. **Sanitary sewage and venting** - carrying waste away with sealed traps
3. **Rainwater collection and gutters** - draining roofs and paved areas
4. **Reservoirs and pumps** - storing and pressurizing the supply
5. **Water reuse and rainwater harvesting** - greywater and captured rain
6. **Fire-fighting systems** - hydrants and sprinklers
7. **Sizing and pressure requirements** - the calculations behind it all
8. **BIM coordination of MEP** - clash-free mechanical, electrical, plumbing

Standards are named where they help - the Brazilian **NBR/ABNT** suite
(NBR 5626 cold water, NBR 7198 hot water, NBR 8160 sewage, NBR 10844
rainwater, NBR 13714 hydrants), plus international references - but the
goal is understanding you can apply anywhere.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How does this course teach each building system?",
                    (
                        opt("Only with legal code text, no examples"),
                        opt(
                            "A direct explanation plus a worked sizing or pressure "
                            "calculation and a diagram of the flow",
                            correct=True,
                        ),
                        opt("Purely with photographs of pipes"),
                        opt("By memorizing product catalog part numbers"),
                    ),
                    "Each lesson pairs a clear explanation with a real calculation and "
                    "a mermaid diagram of the system.",
                ),
                q(
                    "Why is a building compared to 'a small water utility'?",
                    (
                        opt("Because it sells water to neighbors"),
                        opt(
                            "It must supply, store, pressurize and distribute clean "
                            "water and safely remove waste and rain",
                            correct=True,
                        ),
                        opt("Because plumbing is optional in modern buildings"),
                        opt("Because fire systems replace the city water main"),
                    ),
                    "Supply, storage, distribution and drainage all happen inside the "
                    "building, like a miniature utility.",
                ),
            ),
        ),
        # -- 1. Cold and hot water supply ------------------------------
        _t(
            "Cold and hot water supply",
            "10 min",
            """# Cold and hot water supply

The **cold water** system delivers potable water from the street main (or
a reservoir) to every fixture - taps, showers, toilets, appliances. In
Brazil it is governed by **NBR 5626**. Two common architectures:

- **Direct (upfeed)** - the street pressure feeds fixtures directly. Simple,
  but only works in low buildings where street pressure is enough.
- **Indirect (downfeed)** - water fills a **lower reservoir**, a pump lifts
  it to an **upper reservoir**, and gravity feeds the building down through
  distribution columns. This is the standard for multi-storey buildings
  because it decouples supply from unreliable street pressure.

Distribution branches from the upper tank down **columns** (risers), then
horizontal **branches**, then short **connections** to each fixture.

**Hot water** (NBR 7198) adds a heat source - individual (per apartment
electric or gas heater), central per building, or solar with a backup.
Longer hot runs may need a **recirculation loop** so a user does not waste
water waiting for it to warm.

```mermaid
graph TD
    MAIN["Street main"] --> LOW["Lower reservoir"]
    LOW --> PUMP["Booster pump"]
    PUMP --> UP["Upper reservoir"]
    UP --> COLD["Cold columns"]
    UP --> HEAT["Water heater"]
    HEAT --> HOT["Hot columns"]
    COLD --> FIX["Fixtures"]
    HOT --> FIX
```

**Worked example - available pressure at a fixture.** In a downfeed
system, static pressure comes from the height difference between the upper
tank water level and the fixture. Water gives about 9.81 kPa per metre
(roughly 1 mH2O = 9.81 kPa).

```text
Upper tank level:            30.0 m above ground
Shower on 3rd floor:          9.0 m above ground
Height difference h:         30.0 - 9.0 = 21.0 m

Static pressure = 9.81 kPa/m x 21.0 m = 206 kPa (about 2.1 bar)

NBR 5626 wants at least 10 kPa (1.0 mH2O) at the fixture in use, and
caps static pressure at 400 kPa. 206 kPa static is comfortably in range;
after head loss along the pipe the dynamic pressure stays adequate.
```

Remember: cold water is about getting **enough pressure everywhere** -
too little and fixtures dribble, too much and you get noise, wear and
leaks.
""",
        ),
        quiz_lesson(
            "Quiz: Cold and hot water supply",
            (
                q(
                    "Why do multi-storey buildings usually use an indirect (downfeed) supply?",
                    (
                        opt("It uses less pipe than any other method"),
                        opt(
                            "Storing water in an upper reservoir and feeding by gravity "
                            "decouples the building from unreliable street pressure",
                            correct=True,
                        ),
                        opt("It removes the need for any pump"),
                        opt("Street pressure is always too high for tall buildings"),
                    ),
                    "The upper tank buffers supply and provides steady gravity pressure "
                    "regardless of the street main.",
                ),
                q(
                    "Roughly what static pressure does a 21 m height difference give?",
                    (
                        opt("About 21 kPa"),
                        opt("About 2.1 kPa"),
                        opt("About 206 kPa (roughly 2.1 bar)", correct=True),
                        opt("About 2100 kPa"),
                    ),
                    "1 metre of water is about 9.81 kPa, so 21 m gives about 206 kPa.",
                ),
                q(
                    "What is the purpose of a hot water recirculation loop?",
                    (
                        opt("To heat the cold water columns"),
                        opt(
                            "To keep hot water near the fixtures so users do not run "
                            "the tap waiting for it to warm up",
                            correct=True,
                        ),
                        opt("To increase the street pressure"),
                        opt("To drain the reservoir automatically"),
                    ),
                    "Recirculation avoids wasting water and time on long hot runs.",
                ),
            ),
        ),
        # -- 2. Sanitary sewage and venting ----------------------------
        _t(
            "Sanitary sewage and venting",
            "10 min",
            """# Sanitary sewage and venting

The **sanitary sewage** system carries wastewater and human waste away by
**gravity**, kept separate from rainwater. In Brazil it follows
**NBR 8160**. The chain runs: fixture -> **trap** -> branch drain ->
**stack** (vertical) -> building drain -> the public sewer or a septic
system.

Two ideas make it safe:

- **Water-sealed traps** - the U-bend under every fixture holds a plug of
  water that blocks **sewer gases** (and odors, insects) from entering the
  room. Protecting that seal is the whole game.
- **Venting** - a parallel network of vent pipes open to the atmosphere.
  When a slug of water rushes down a stack it can push or pull air,
  creating pressure swings that would **siphon the trap seals dry**. Vents
  admit air so pressure stays near atmospheric and seals survive.

Drains flow **partly full** by design so air can move above the water,
which is why slope and diameter, not pressure, drive the sizing.

```mermaid
graph TD
    FIX["Fixture"] --> TRAP["Water sealed trap"]
    TRAP --> BR["Branch drain"]
    BR --> STACK["Soil stack"]
    VENT["Vent to atmosphere"] --> STACK
    STACK --> DRAIN["Building drain"]
    DRAIN --> SEWER["Public sewer or septic"]
```

**Worked example - sizing a horizontal branch by fixture units.** Drainage
is sized in **fixture units (FU)**, a dimensionless discharge weight per
fixture. Sum the FU on a branch and read the minimum diameter from the
code table.

```text
Fixtures on one bathroom branch (typical NBR 8160 weights):
  Lavatory (washbasin)   1 FU
  Shower                 2 FU
  Toilet (WC)            6 FU  (WC discharges to the soil stack directly)
  Bidet                  1 FU
Total on the wastewater branch (excluding WC): 1 + 2 + 1 = 4 FU

Table lookup: up to 6 FU -> minimum 50 mm horizontal branch.
The toilet needs its own 100 mm connection to the stack.
Minimum slope for a 100 mm drain: about 1 percent (1 cm per metre).
```

Remember: sewage flows downhill on slope, traps keep the gases out, and
**vents keep the traps from being siphoned dry**.
""",
        ),
        quiz_lesson(
            "Quiz: Sanitary sewage and venting",
            (
                q(
                    "What is the job of the water-sealed trap under a fixture?",
                    (
                        opt("To increase the drain flow rate"),
                        opt(
                            "To hold a plug of water that blocks sewer gases and odors "
                            "from entering the room",
                            correct=True,
                        ),
                        opt("To filter solids out of the wastewater"),
                        opt("To pressurize the stack"),
                    ),
                    "The U-bend water seal is the barrier against sewer gas.",
                ),
                q(
                    "Why does a drainage system need vent pipes?",
                    (
                        opt("To carry extra wastewater"),
                        opt(
                            "To admit air so pressure swings from draining water do not "
                            "siphon the trap seals dry",
                            correct=True,
                        ),
                        opt("To supply fresh water to the fixtures"),
                        opt("To heat the drain pipes"),
                    ),
                    "Vents keep the system near atmospheric pressure, protecting the trap seals.",
                ),
                q(
                    "How is a sanitary drainage branch sized?",
                    (
                        opt("By the water supply pressure in bar"),
                        opt(
                            "By summing the fixture units (FU) on the branch and reading "
                            "the minimum diameter from a table",
                            correct=True,
                        ),
                        opt("By the color of the pipe"),
                        opt("By the number of floors only"),
                    ),
                    "Fixture units weight each fixture's discharge; their sum sets the "
                    "diameter and slope.",
                ),
            ),
        ),
        # -- 3. Rainwater collection and gutters -----------------------
        _t(
            "Rainwater collection and gutters",
            "10 min",
            """# Rainwater collection and gutters

**Rainwater (stormwater)** drainage carries rain off roofs and paved areas
quickly, kept separate from sewage. In Brazil it follows **NBR 10844**.
The chain: roof surface -> **gutter (calha)** -> **downpipe
(condutor vertical)** -> horizontal drain -> soakaway, detention tank, or
storm sewer.

Sizing starts from a **design rainfall intensity** - a rare, intense storm
the system must handle without overflowing, expressed in mm/h and chosen
from **IDF (intensity-duration-frequency)** curves for the city and a
return period (often 5 min duration, 5 to 25 year return).

The core relation is the **Rational Method**:

```text
Q = C x i x A / 3600   (SI, with Q in L/s)

  Q = design flow (L/s)
  C = runoff coefficient (roofs ~ 1.0; asphalt ~ 0.9; lawn ~ 0.2)
  i = rainfall intensity (mm/h)
  A = catchment area (m2)
```

```mermaid
graph TD
    ROOF["Roof surface"] --> GUT["Gutter"]
    GUT --> DOWN["Downpipe"]
    DOWN --> HORIZ["Horizontal drain"]
    HORIZ --> DET["Detention tank"]
    DET --> STORM["Storm sewer or soakaway"]
```

**Worked example - flow from a roof and downpipe count.**

```text
Roof area A = 200 m2
Design intensity i = 150 mm/h  (from the local IDF curve)
Runoff coefficient C = 1.0  (impervious roof)

Q = C x i x A / 3600
Q = 1.0 x 150 x 200 / 3600
Q = 30000 / 3600 = 8.33 L/s

A 75 mm downpipe carries roughly 4 to 5 L/s (NBR 10844 tables, depending
on gutter head). 8.33 / 4.5 = 1.85, so use 2 downpipes of 75 mm (or one
100 mm pipe). Gutters get a slope of about 0.5 percent toward the outlets.
```

Remember: stormwater is a **peak-flow** problem - size for the rare
intense storm, keep it separate from sewage, and give every roof enough
downpipe capacity so it never backs up and floods.
""",
        ),
        quiz_lesson(
            "Quiz: Rainwater collection and gutters",
            (
                q(
                    "In the Rational Method Q = C x i x A / 3600, what does C represent?",
                    (
                        opt("The pipe diameter in mm"),
                        opt(
                            "The runoff coefficient - the fraction of rain that runs "
                            "off rather than soaking in",
                            correct=True,
                        ),
                        opt("The number of floors"),
                        opt("The cost per metre of gutter"),
                    ),
                    "C is near 1.0 for impervious roofs and much lower for permeable "
                    "surfaces like lawn.",
                ),
                q(
                    "A 200 m2 roof with i = 150 mm/h and C = 1.0 produces about what design flow?",
                    (
                        opt("About 0.83 L/s"),
                        opt("About 8.33 L/s", correct=True),
                        opt("About 83 L/s"),
                        opt("About 30 L/s"),
                    ),
                    "Q = 1.0 x 150 x 200 / 3600 = 8.33 L/s.",
                ),
                q(
                    "Why is rainwater kept in a separate system from sanitary sewage?",
                    (
                        opt("Rainwater is warmer than sewage"),
                        opt(
                            "It is a large peak flow that would overload the sewer and "
                            "mixing them wastes treatment capacity",
                            correct=True,
                        ),
                        opt("They use the same pipes anyway"),
                        opt("Rainwater cannot flow by gravity"),
                    ),
                    "Separating storm and sanitary flows avoids overloading and keeps "
                    "clean rain out of sewage treatment.",
                ),
            ),
        ),
        # -- 4. Reservoirs and pumps -----------------------------------
        _t(
            "Reservoirs and pumps",
            "10 min",
            """# Reservoirs and pumps

Because street supply is intermittent and pressure varies, buildings
**store** water and **pump** it. Two reservoirs are typical:

- **Lower reservoir (cistern)** - fed from the street, sized to ride out
  supply interruptions.
- **Upper reservoir (roof tank)** - fed by pumps, provides gravity
  pressure to the whole building.

**Reservoir volume** is usually the building's **daily consumption**,
split between lower and upper tanks (a common rule: lower 60 percent,
upper 40 percent), with a **fire reserve** added where required.

**Pumps** lift water from lower to upper tank against the **total dynamic
head** - the static lift plus friction losses. They are chosen from a
**pump curve** (head vs flow) to meet the design point. Booster/pressure
sets with variable-speed drives are used where gravity head is not enough.

```mermaid
graph TD
    STREET["Street supply"] --> CIST["Lower cistern"]
    CIST --> PUMP["Duty and standby pumps"]
    PUMP --> ROOF["Upper roof tank"]
    ROOF --> GRAV["Gravity distribution"]
    ROOF --> FIRE["Fire reserve volume"]
```

**Worked example - reservoir sizing and pump head.**

```text
Population: 40 apartments x 3 people = 120 people
Per capita demand: 200 L per person per day (NBR 5626 guidance)
Daily consumption = 120 x 200 = 24000 L = 24 m3

Store one day: 24 m3 total
  Lower cistern (60%): 14.4 m3
  Upper tank   (40%):  9.6 m3

Pump total dynamic head:
  Static lift (cistern level to roof tank):   32 m
  Friction and fitting losses (~15% of static): 5 m
  Total dynamic head Hman = 32 + 5 = 37 m

Pump hydraulic power for Q = 2.0 L/s = 0.002 m3/s:
  P = rho x g x Q x H = 1000 x 9.81 x 0.002 x 37 = 726 W
  At ~60% pump efficiency: 726 / 0.60 = 1210 W, about 1.6 hp.
```

Remember: **store a day's water**, add a fire reserve, and size the pump
for the **total dynamic head** - static lift plus friction - not just the
height.
""",
        ),
        quiz_lesson(
            "Quiz: Reservoirs and pumps",
            (
                q(
                    "What is 'total dynamic head' for a pump?",
                    (
                        opt("Only the vertical height it must lift water"),
                        opt(
                            "The static lift plus the friction and fitting losses the "
                            "pump must overcome",
                            correct=True,
                        ),
                        opt("The diameter of the pump outlet"),
                        opt("The volume of the upper tank"),
                    ),
                    "Static lift alone underestimates the head; friction losses must be added.",
                ),
                q(
                    "For 120 people at 200 L/person/day, what is the daily consumption?",
                    (
                        opt("2.4 m3"),
                        opt("24 m3", correct=True),
                        opt("240 m3"),
                        opt("120 m3"),
                    ),
                    "120 x 200 = 24000 L = 24 m3.",
                ),
                q(
                    "Why store water in both a lower cistern and an upper roof tank?",
                    (
                        opt("To double the water bill"),
                        opt(
                            "The lower tank rides out supply interruptions while the "
                            "upper tank provides gravity pressure to the building",
                            correct=True,
                        ),
                        opt("Because pumps cannot lift more than one floor"),
                        opt("To avoid needing any pump at all"),
                    ),
                    "Lower stores from the street; upper feeds the building by gravity.",
                ),
            ),
        ),
        # -- 5. Water reuse and rainwater harvesting -------------------
        _t(
            "Water reuse and rainwater harvesting",
            "10 min",
            """# Water reuse and rainwater harvesting

Buildings can cut potable demand by reusing water for **non-potable** uses
- toilet flushing, irrigation, washing, cooling. Two main sources:

- **Rainwater harvesting** - captured roof rain, screened and stored, used
  for flushing and irrigation. In Brazil, **NBR 15527** governs rainwater
  for non-potable uses.
- **Greywater reuse** - lightly used water from showers and basins (not
  toilet/kitchen 'blackwater'), treated and reused for flushing and
  irrigation.

A key design element is **first-flush diversion**: the first few
millimetres of rain wash dust and debris off the roof and are diverted
away before clean water reaches the storage tank. Reuse plumbing is a
**separate, clearly marked (purple) network** that must never cross-connect
to potable water.

```mermaid
graph TD
    RAIN["Roof rainfall"] --> FF["First flush diverter"]
    FF --> FILT["Screen and filter"]
    FILT --> TANK["Reuse storage tank"]
    GREY["Greywater from showers"] --> TREAT["Greywater treatment"]
    TREAT --> TANK
    TANK --> NONPOT["Toilets and irrigation"]
    TANK --> TOPUP["Potable top up if empty"]
```

**Worked example - harvested rainwater and payback in demand.**

```text
Catchment (roof) area A = 200 m2
Annual rainfall P = 1400 mm/year = 1.4 m/year
Runoff/collection efficiency e = 0.80 (losses, first flush, filter)

Harvestable volume V = A x P x e
V = 200 x 1.4 x 0.80 = 224 m3/year

Toilet flushing demand (40 apts, non-potable):
  120 people x 6 flushes/day x 6 L = 4320 L/day
  Annual = 4320 x 365 = 1.58 million L = 1577 m3/year

Rainwater covers 224 / 1577 = 14% of flushing demand; combined with
greywater it can cover a large share, sharply cutting potable use.
Storage tank sized for a dry-spell buffer (e.g. 20 days x daily use).
```

Remember: reuse water for **non-potable** duties only, keep it on a
**separate marked network** with a potable top-up, and divert the dirty
**first flush** before storage.
""",
        ),
        quiz_lesson(
            "Quiz: Water reuse and rainwater harvesting",
            (
                q(
                    "What is 'first-flush diversion' in a rainwater system?",
                    (
                        opt("Flushing all toilets at once each morning"),
                        opt(
                            "Diverting the first few millimetres of rain, which washes "
                            "dust and debris off the roof, away from the storage tank",
                            correct=True,
                        ),
                        opt("Draining the tank completely before each storm"),
                        opt("Adding chlorine to the first rain"),
                    ),
                    "The dirtiest initial runoff is sent to waste so cleaner water is stored.",
                ),
                q(
                    "For a 200 m2 roof, 1400 mm/year rainfall and 0.80 efficiency, the "
                    "harvestable volume is about:",
                    (
                        opt("About 22 m3/year"),
                        opt("About 224 m3/year", correct=True),
                        opt("About 2240 m3/year"),
                        opt("About 56 m3/year"),
                    ),
                    "V = 200 x 1.4 x 0.80 = 224 m3/year.",
                ),
                q(
                    "Why must reuse water stay on a separate, marked network?",
                    (
                        opt("To make it flow faster"),
                        opt(
                            "It is non-potable, so it must never cross-connect with the "
                            "potable supply and risk contamination",
                            correct=True,
                        ),
                        opt("Because purple pipe is cheaper"),
                        opt("So it can be billed at a higher rate"),
                    ),
                    "Non-potable water is only safe for flushing and irrigation and "
                    "must be isolated from drinking water.",
                ),
            ),
        ),
        # -- 6. Fire-fighting systems ----------------------------------
        _t(
            "Fire-fighting systems (hydrants, sprinklers)",
            "11 min",
            """# Fire-fighting systems (hydrants, sprinklers)

Fire protection is a **dedicated, always-ready** water system, independent
of the domestic supply, with a **reserved volume** in the reservoir that
domestic use can never draw down. Two main active systems:

- **Hydrant/hose systems** (Brazil: **NBR 13714**) - a fire main feeds
  **hydrant boxes** with hose and nozzle on each floor, for firefighters
  or trained occupants. A **fire pump** guarantees pressure and flow.
- **Automatic sprinklers** (Brazil: **NBR 10897**, internationally NFPA 13)
  - pipes under the ceiling with heat-sensitive **sprinkler heads**. Each
  head opens **individually** when its glass bulb bursts at a set
  temperature, spraying only over the fire. Sprinklers control most fires
  with just a few heads - they do not all open at once.

Design centers on a **hydraulically most-demanding area** (the remote,
worst-case zone), a **design density** (L/min per m2), and a minimum
**residual pressure** at the farthest head or hydrant while flowing.

```mermaid
graph TD
    RES["Fire reserve volume"] --> FPUMP["Fire pump and jockey"]
    FPUMP --> RISER["Fire riser main"]
    RISER --> HYD["Hydrant hose boxes"]
    RISER --> SPR["Sprinkler branch lines"]
    SPR --> HEAD["Heat activated heads"]
    HEAD --> FIRE["Water only over the fire"]
```

**Worked example - fire reserve and sprinkler demand.**

```text
Sprinkler design (light hazard, NBR 10897 / NFPA 13):
  Design density d = 4.1 L/min per m2
  Design (remote) area A = 140 m2
  Sprinkler demand = d x A = 4.1 x 140 = 574 L/min

Add an inside hose allowance: +100 L/min
Total design flow Q = 574 + 100 = 674 L/min = 40.4 m3/h

Required duration (light hazard): 30 min minimum
Fire reserve = Q x t = 674 L/min x 30 min = 20220 L, about 20.2 m3

This 20.2 m3 is RESERVED at the bottom of the tank - the domestic outlet
sits above it so everyday use can never consume the fire reserve.
Minimum residual pressure at the hydraulically remote head: about 100 kPa
(1.0 bar) while flowing.
```

Remember: fire water is **reserved and independent**, sprinkler heads open
**one at a time** over the fire, and you size for the **remote worst-case
area** at a minimum flowing pressure.
""",
        ),
        quiz_lesson(
            "Quiz: Fire-fighting systems (hydrants, sprinklers)",
            (
                q(
                    "How do automatic sprinkler heads operate in a fire?",
                    (
                        opt("They all open together across the whole building"),
                        opt(
                            "Each head opens individually when its heat-sensitive "
                            "element bursts, spraying only over the fire",
                            correct=True,
                        ),
                        opt("A firefighter opens each one by hand"),
                        opt("They spray continuously all the time"),
                    ),
                    "Heads activate one at a time by heat; only those over the fire "
                    "open, controlling most fires with a few heads.",
                ),
                q(
                    "For a 140 m2 design area at 4.1 L/min per m2, the sprinkler demand "
                    "(before hose allowance) is:",
                    (
                        opt("About 57 L/min"),
                        opt("About 574 L/min", correct=True),
                        opt("About 5740 L/min"),
                        opt("About 34 L/min"),
                    ),
                    "4.1 x 140 = 574 L/min.",
                ),
                q(
                    "Why is the fire reserve kept at the bottom of the reservoir with "
                    "the domestic outlet above it?",
                    (
                        opt("To make the tank easier to clean"),
                        opt(
                            "So everyday domestic use can never draw down the volume "
                            "reserved for firefighting",
                            correct=True,
                        ),
                        opt("Because fire water is heavier"),
                        opt("To reduce pump wear"),
                    ),
                    "The reserved fire volume must always be available regardless of "
                    "domestic consumption.",
                ),
            ),
        ),
        # -- 7. Sizing and pressure requirements -----------------------
        _t(
            "Sizing and pressure requirements",
            "11 min",
            """# Sizing and pressure requirements

Every system above rests on the same two questions: **what pipe diameter**
carries the flow, and **is the pressure enough** at the worst fixture? This
lesson ties the calculations together.

**Estimating peak flow.** Not every fixture runs at once. The **weighted
fixture unit** method assigns each fixture a weight, sums them for the
section, and converts to a probable **peak flow** with an empirical
relation (NBR 5626):

```text
Q = 0.3 x sqrt(sum of weights)   (Q in L/s)
```

**Choosing a diameter.** Pick the pipe so the **velocity** stays in a sane
band - about **0.6 to 3.0 m/s** (too slow silts, too fast erodes and makes
noise/water hammer). From continuity:

```text
Q = A x v = (pi/4) x D^2 x v   ->   D = sqrt( 4 Q / (pi x v) )
```

**Checking pressure.** Available pressure at a fixture is the static head
minus **head loss** (friction + fittings). Friction is estimated with
**Hazen-Williams** or **Darcy-Weisbach**; fittings via equivalent lengths.

```text
Available = static pressure - friction loss - fitting loss
Must remain >= the fixture's minimum flowing pressure (e.g. 10 kPa).
```

```mermaid
graph TD
    W["Sum fixture weights"] --> Q["Peak flow Q"]
    Q --> V["Pick velocity 0.6 to 3.0 m per s"]
    V --> D["Diameter D from continuity"]
    D --> HL["Head loss along pipe"]
    HL --> P["Check residual pressure"]
    P --> OK["Adequate or resize"]
```

**Worked example - diameter for a supply branch.**

```text
Fixtures on a branch, weights: shower 0.4 + basin 0.3 + WC valve 0.3 = 1.0
Peak flow Q = 0.3 x sqrt(1.0) = 0.30 L/s = 0.0003 m3/s

Target velocity v = 1.5 m/s
D = sqrt( 4 x 0.0003 / (pi x 1.5) )
D = sqrt( 0.0012 / 4.712 )
D = sqrt( 0.0002546 ) = 0.0160 m = 16 mm

Choose the next commercial size up: 20 mm (DN20) pipe.
Recheck velocity at 20 mm: v = Q / A = 0.0003 / 0.000314 = 0.95 m/s,
still inside the 0.6 to 3.0 m/s band. Good.
```

Remember: **flow from weights, diameter from a sane velocity, then verify
pressure survives the head loss** - the same loop for supply, drainage,
storm and fire.
""",
        ),
        quiz_lesson(
            "Quiz: Sizing and pressure requirements",
            (
                q(
                    "Why size pipes to keep velocity roughly between 0.6 and 3.0 m/s?",
                    (
                        opt("It is the only speed water can flow"),
                        opt(
                            "Too slow lets sediment settle; too fast causes erosion, "
                            "noise and water hammer",
                            correct=True,
                        ),
                        opt("To make the pipe cheaper regardless of flow"),
                        opt("Because pressure does not matter at those speeds"),
                    ),
                    "The velocity band balances self-cleaning flow against wear, noise and hammer.",
                ),
                q(
                    "Using Q = 0.3 x sqrt(sum of weights), a branch with total weight "
                    "1.0 has a peak flow of about:",
                    (
                        opt("0.30 L/s", correct=True),
                        opt("3.0 L/s"),
                        opt("1.0 L/s"),
                        opt("0.03 L/s"),
                    ),
                    "0.3 x sqrt(1.0) = 0.3 L/s.",
                ),
                q(
                    "After sizing a pipe by velocity, what final check confirms it works?",
                    (
                        opt("That the pipe is the cheapest available"),
                        opt(
                            "That residual pressure at the worst fixture stays at or "
                            "above its minimum after head loss",
                            correct=True,
                        ),
                        opt("That the pipe color matches the system"),
                        opt("That every fixture runs simultaneously"),
                    ),
                    "Static head minus friction and fitting losses must still exceed "
                    "the fixture's minimum flowing pressure.",
                ),
            ),
        ),
        # -- 8. BIM coordination of MEP --------------------------------
        _t(
            "BIM coordination of MEP systems",
            "11 min",
            """# BIM coordination of MEP systems

A modern building routes **MEP** - Mechanical (HVAC), Electrical, and
Plumbing (which includes all the water, sewage, storm and fire systems in
this course) - through the same tight ceiling and shaft space. **BIM
(Building Information Modeling)** coordinates them in a shared 3D model so
conflicts are found on screen, not on site.

Core practices:

- **Federated model** - each discipline authors its own model; they are
  combined ('federated') for coordination.
- **Clash detection** - software (e.g. Navisworks, Solibri) automatically
  finds where a **duct**, a **cable tray**, a **water pipe** and a
  **sprinkler line** occupy the same space (**hard clash**) or violate
  clearance/access rules (**soft clash**).
- **IFC** - the open **Industry Foundation Classes** exchange format lets
  models from different tools interoperate (openBIM).
- **LOD (Level of Development)** - how detailed/reliable an element is,
  from LOD 100 (concept) to LOD 400 (fabrication).

Coordinating early turns expensive on-site rework into a cheap model edit,
and the same model feeds quantities, fabrication and the **digital twin**
used to operate the building.

```mermaid
graph TD
    ARCH["Architecture model"] --> FED["Federated BIM model"]
    HVAC["Mechanical HVAC"] --> FED
    ELEC["Electrical"] --> FED
    PLUMB["Plumbing water sewage fire"] --> FED
    FED --> CLASH["Automated clash detection"]
    CLASH --> FIX["Resolve before construction"]
    FIX --> TWIN["Digital twin for operations"]
```

**Worked example - clash count and rework saving.**

```python
# Rough coordination benefit: cost avoided by fixing clashes in the model
clashes_found = 320          # hard + soft clashes in the federated model
avg_onsite_rework = 1500     # currency per clash if caught during build
model_fix_cost = 80          # currency per clash resolved in BIM

onsite_cost = clashes_found * avg_onsite_rework   # 480000
bim_cost = clashes_found * model_fix_cost         # 25600
savings = onsite_cost - bim_cost                  # 454400

print(f"Resolving {clashes_found} clashes in BIM saves {savings} vs site rework")
# Resolving 320 clashes in BIM saves 454400 vs site rework
```

Remember: MEP shares the same crowded space, so **federate the models,
clash-detect, and resolve on screen** - each conflict fixed in BIM is a
much cheaper problem than one discovered by a plumber on site.
""",
        ),
        quiz_lesson(
            "Quiz: BIM coordination of MEP systems",
            (
                q(
                    "What does MEP stand for in building coordination?",
                    (
                        opt("Money, Equipment, Planning"),
                        opt(
                            "Mechanical (HVAC), Electrical, and Plumbing - including the "
                            "water, sewage, storm and fire systems",
                            correct=True,
                        ),
                        opt("Masonry, Excavation, Paving"),
                        opt("Modeling, Estimating, Procurement"),
                    ),
                    "MEP groups the building services that share the ceiling and shaft "
                    "space and must be coordinated.",
                ),
                q(
                    "What is 'clash detection' in a federated BIM model?",
                    (
                        opt("Checking that colors match across drawings"),
                        opt(
                            "Automatically finding where elements occupy the same space "
                            "(hard clash) or violate clearances (soft clash)",
                            correct=True,
                        ),
                        opt("Counting the number of floors"),
                        opt("Testing the water pressure on site"),
                    ),
                    "Clash detection surfaces spatial conflicts on screen before they "
                    "become on-site rework.",
                ),
                q(
                    "Why does coordinating MEP in BIM save money?",
                    (
                        opt("It removes the need for any plumbing"),
                        opt(
                            "Fixing a conflict as a model edit is far cheaper than "
                            "discovering and reworking it during construction",
                            correct=True,
                        ),
                        opt("It makes pipes flow faster"),
                        opt("It eliminates the need for pumps"),
                    ),
                    "Each clash resolved in the model avoids costly demolition and rework on site.",
                ),
                q(
                    "What is IFC in the BIM context?",
                    (
                        opt("A brand of water pump"),
                        opt(
                            "The open Industry Foundation Classes exchange format that "
                            "lets models from different tools interoperate",
                            correct=True,
                        ),
                        opt("A fire-resistance rating"),
                        opt("A type of sprinkler head"),
                    ),
                    "IFC is the openBIM interchange standard for sharing models across software.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why do tall buildings favor an indirect downfeed water supply?",
                    (
                        opt("It needs no reservoir"),
                        opt(
                            "An upper reservoir fed by pumps gives steady gravity "
                            "pressure independent of unreliable street pressure",
                            correct=True,
                        ),
                        opt("Street pressure is always sufficient"),
                        opt("Downfeed removes the need for columns"),
                    ),
                    "The roof tank buffers supply and delivers consistent gravity "
                    "pressure through the building.",
                ),
                q(
                    "What two features keep a sanitary drainage system safe?",
                    (
                        opt("High pressure and small diameters"),
                        opt(
                            "Water-sealed traps that block sewer gas, and vents that "
                            "keep pressure near atmospheric so seals are not siphoned",
                            correct=True,
                        ),
                        opt("Chlorination and heating"),
                        opt("Pumps and pressure tanks"),
                    ),
                    "Traps seal out gas; vents protect those seals from siphoning.",
                ),
                q(
                    "In Q = C x i x A / 3600, a 200 m2 roof at i = 150 mm/h and C = 1.0 "
                    "gives about:",
                    (
                        opt("0.83 L/s"),
                        opt("8.33 L/s", correct=True),
                        opt("83 L/s"),
                        opt("833 L/s"),
                    ),
                    "1.0 x 150 x 200 / 3600 = 8.33 L/s - a peak-flow storm sizing.",
                ),
                q(
                    "A pump's 'total dynamic head' is:",
                    (
                        opt("Just the vertical lift"),
                        opt(
                            "The static lift plus friction and fitting losses along the pipe",
                            correct=True,
                        ),
                        opt("The reservoir volume"),
                        opt("The outlet diameter"),
                    ),
                    "You must add friction to the static lift or the pump is undersized.",
                ),
                q(
                    "Reused (non-potable) water must be:",
                    (
                        opt("Mixed into the drinking water to save pipe"),
                        opt(
                            "Kept on a separate, clearly marked network that never "
                            "cross-connects with the potable supply",
                            correct=True,
                        ),
                        opt("Used only for drinking"),
                        opt("Stored in the fire reserve"),
                    ),
                    "Non-potable water is safe only for flushing and irrigation and "
                    "must stay isolated from potable water.",
                ),
                q(
                    "How do automatic sprinkler heads activate?",
                    (
                        opt("All at once across the building"),
                        opt(
                            "Individually, when each head's heat-sensitive element "
                            "bursts over the fire",
                            correct=True,
                        ),
                        opt("Only when a firefighter opens a valve"),
                        opt("Continuously, day and night"),
                    ),
                    "Only heads over the fire open; a few control most fires.",
                ),
                q(
                    "Why is the fire reserve stored below the domestic outlet in the reservoir?",
                    (
                        opt("Fire water is denser"),
                        opt(
                            "So everyday domestic consumption can never draw down the "
                            "reserved firefighting volume",
                            correct=True,
                        ),
                        opt("To make cleaning easier"),
                        opt("To reduce pump wear"),
                    ),
                    "The reserved volume must always be available for firefighting.",
                ),
                q(
                    "Using D = sqrt(4Q / (pi v)), what drives the velocity you choose?",
                    (
                        opt("Making velocity as high as possible"),
                        opt(
                            "Staying in about 0.6 to 3.0 m/s to avoid sedimentation at "
                            "low speed and erosion, noise and hammer at high speed",
                            correct=True,
                        ),
                        opt("Matching the pipe color"),
                        opt("Keeping velocity exactly at 10 m/s"),
                    ),
                    "A sane velocity band self-cleans without wear or water hammer.",
                ),
                q(
                    "What is the final check after sizing a supply pipe?",
                    (
                        opt("That the pipe is the cheapest"),
                        opt(
                            "That residual pressure at the worst fixture stays above its "
                            "minimum after friction and fitting losses",
                            correct=True,
                        ),
                        opt("That every fixture runs at once"),
                        opt("That the velocity is zero"),
                    ),
                    "Static head minus head loss must still exceed the fixture's "
                    "minimum flowing pressure.",
                ),
                q(
                    "What is the main benefit of coordinating MEP systems in BIM with "
                    "clash detection?",
                    (
                        opt("It removes the need for plumbing entirely"),
                        opt(
                            "Spatial conflicts between ducts, pipes, trays and sprinklers "
                            "are found and fixed in the model instead of as costly "
                            "on-site rework",
                            correct=True,
                        ),
                        opt("It increases water pressure automatically"),
                        opt("It replaces the fire pump"),
                    ),
                    "Federate, clash-detect and resolve on screen - far cheaper than "
                    "discovering clashes during construction.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

BUILDING_HYDRAULIC_SYSTEMS_COURSES: tuple[SeedCourse, ...] = (_BUILDING_HYDRAULIC_SYSTEMS,)
