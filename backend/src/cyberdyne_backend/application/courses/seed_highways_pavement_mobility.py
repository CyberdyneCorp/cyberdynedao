"""Academy seed content - Highways, Pavement and Mobility.

Designing roads and moving people: highway planning and traffic studies,
geometric design (horizontal and vertical curves, superelevation),
earthworks and mass-haul diagrams, pavement materials and asphalt binders,
flexible and rigid pavement design, pavement evaluation and maintenance,
and modern traffic engineering, capacity and smart mobility (ITS). Every
lesson is a direct explanation with a mermaid diagram and a worked design
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


_HIGHWAYS_PAVEMENT_MOBILITY = SeedCourse(
    slug="highways-pavement-mobility",
    title="Highways, Pavement & Mobility",
    description=(
        "Designing roads and moving people - geometric design, earthworks, "
        "flexible and rigid pavements, traffic engineering and sustainable "
        "smart mobility. Every lesson pairs a direct explanation with a "
        "mermaid diagram and a worked design calculation grounded in AASHTO, "
        "DNIT and modern ITS practice."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Highways, Pavement and Mobility

A highway is a system: a line drawn across the land, a body of earth
shaped to carry it, layers of material that spread the wheel loads, and a
stream of vehicles that must move safely and efficiently. This course
walks the full chain - from the first traffic study to the smart-mobility
sensors that keep the corridor flowing.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short worked example (a design formula, a mini-calculation),
and draws the idea as a diagram. After each lesson there is a short quiz;
at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Highway planning and traffic studies** - forecasting demand and design volumes
2. **Geometric design** - horizontal and vertical curves, superelevation
3. **Earthworks and mass-haul diagrams** - balancing cut and fill
4. **Pavement materials and asphalt binders** - what the layers are made of
5. **Flexible pavement design** - asphalt over granular layers
6. **Rigid pavement design** - concrete slabs on grade
7. **Pavement evaluation and maintenance** - measuring and preserving condition
8. **Traffic engineering, capacity and smart mobility** - flow, capacity and ITS

Standards appear throughout - **AASHTO**, **DNIT/ABNT NBR**, the **Highway
Capacity Manual (HCM)** - but the aim is to make each idea teachable, not
to reproduce a code. Learn the chain once and every road you drive will
read differently.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How is a highway best understood in this course?",
                    (
                        opt("Only as a ribbon of asphalt"),
                        opt(
                            "As a system - an alignment across the land, earthworks, "
                            "pavement layers and a traffic stream that must move safely "
                            "and efficiently",
                            correct=True,
                        ),
                        opt("As a single concrete slab"),
                        opt("As a purely aesthetic object"),
                    ),
                    "The course follows the whole chain from traffic study to smart "
                    "mobility, treating the road as an integrated system.",
                ),
                q(
                    "What does each content lesson contain?",
                    (
                        opt("Only a long list of standards to memorize"),
                        opt(
                            "A direct explanation, a mermaid diagram, and a worked design "
                            "example, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Just a video with no text"),
                        opt("A single multiple-choice question and nothing else"),
                    ),
                    "Explanation + diagram + worked example + checkpoint quiz is the "
                    "pattern in every lesson.",
                ),
            ),
        ),
        # -- 1. Planning and traffic studies ---------------------------
        _t(
            "Highway planning and traffic studies",
            "10 min",
            """# Highway planning and traffic studies

Before a single line is drawn, you must answer: **how many vehicles, of
what type, will use this road, now and in the design year?** Everything
downstream - number of lanes, pavement thickness, geometry - depends on
that forecast.

The core measured quantity is **AADT** (Annual Average Daily Traffic): the
total yearly traffic divided by 365. But design is not driven by an
average; it is driven by a busy-but-not-extreme hour. The standard is the
**Design Hourly Volume (DHV)**, taken as the **30th highest hourly volume**
of the year - high enough to matter, not so rare it is uneconomic to
serve.

Key relationships:

- **DHV = AADT x K** - the K factor (often 0.08 to 0.12 on rural roads)
  converts daily to the design hour.
- **DDHV = DHV x D** - the directional split D (often around 0.60) gives
  the peak-direction volume that sizes the lanes.
- Traffic is **grown** to the design year with a compound rate:
  future volume = present volume x (1 + i) ^ n.

A worked forecast:

```text
Given:  AADT = 12,000 veh/day
        annual growth i = 3%, design period n = 20 years
        K = 0.10   D = 0.60

Design-year AADT = 12,000 x (1 + 0.03)^20
                 = 12,000 x 1.806
                 = 21,673 veh/day

DHV  = 21,673 x 0.10          = 2,167 veh/h  (both directions)
DDHV = 2,167  x 0.60          = 1,300 veh/h  (peak direction)

-> the peak-direction design volume is ~1,300 veh/h,
   which then drives the lane count via capacity analysis.
```

Traffic studies also classify vehicles (cars vs trucks matter enormously
for pavement) and count turning movements at intersections. The truck
share feeds directly into the pavement load calculation you will meet in
the flexible-pavement lesson.

```mermaid
graph LR
    COUNT["Traffic counts and AADT"] --> GROW["Grow to design year"]
    GROW --> DHV["Design hourly volume"]
    DHV --> DDHV["Peak direction DDHV"]
    DDHV --> LANES["Lane count and geometry"]
    COUNT --> CLASS["Vehicle classification"]
    CLASS --> LOADS["Truck loads for pavement"]
```

Remember: the design volume is a chosen busy hour in a forecast year, not
today's average - plan for the road you will need, not the one you have.
""",
        ),
        quiz_lesson(
            "Quiz: Highway planning and traffic studies",
            (
                q(
                    "What is AADT?",
                    (
                        opt("The traffic in the single busiest hour of the year"),
                        opt(
                            "Annual Average Daily Traffic - total yearly traffic divided by 365",
                            correct=True,
                        ),
                        opt("The number of trucks per lane"),
                        opt("The average speed of vehicles"),
                    ),
                    "AADT is the yearly average daily volume; the design hour is derived "
                    "from it with the K factor.",
                ),
                q(
                    "The Design Hourly Volume is conventionally taken as which hour?",
                    (
                        opt("The single highest hour of the year"),
                        opt("The average hour"),
                        opt("The 30th highest hourly volume of the year", correct=True),
                        opt("The quietest hour at night"),
                    ),
                    "The 30th-highest hour is high enough to matter but not so extreme "
                    "that serving it is uneconomic.",
                ),
                q(
                    "How is present traffic grown to a design year n years ahead at rate i?",
                    (
                        opt("Add i vehicles each year"),
                        opt(
                            "Compound growth: future = present x (1 + i) ^ n",
                            correct=True,
                        ),
                        opt("Multiply by n only"),
                        opt("Divide by the growth rate"),
                    ),
                    "Traffic forecasting uses compound growth over the design period.",
                ),
            ),
        ),
        # -- 2. Geometric design ---------------------------------------
        _t(
            "Geometric design - curves and superelevation",
            "12 min",
            """# Geometric design - curves and superelevation

**Geometric design** shapes the road so a vehicle at the **design speed**
can travel it safely and comfortably. It has two profiles that combine
into a 3D alignment: the **horizontal** (the plan view - straights and
curves) and the **vertical** (the elevation - grades and crest/sag
curves).

## Horizontal curves and superelevation

On a curve, a vehicle needs sideways force to turn. That comes from two
sources: **side friction** (f) between tyre and road, and
**superelevation** (e) - banking the road toward the inside of the curve.
The minimum radius that a design speed can safely hold is:

```text
Minimum radius (metric, V in km/h):

        V^2
R_min = ---------------
        127 x (e + f)

Example:  V = 100 km/h,  e_max = 0.08,  f = 0.12

        100^2            10,000
R_min = ------------- = --------- = 393 m
        127 x (0.20)      25.4

-> a 100 km/h curve needs a radius of at least ~393 m.
```

Larger radius = flatter, safer, more comfortable curve. Between the
straight and the circular curve a **transition (spiral) curve** eases the
steering and introduces the superelevation gradually.

## Vertical curves

Where two grades meet, a **parabolic vertical curve** smooths the change.
Its length is governed by **sight distance**: on a **crest** curve the
driver must see far enough to stop for an object ahead; on a **sag** curve
the concern is comfort and headlight throw at night. Length is expressed
through the **K value** (length per 1% change of grade):

```text
Curve length L = K x A

  where A = algebraic difference of grades (in %)
        K = design constant from the design speed and sight distance

Example:  grades +3% then -2%  ->  A = |3 - (-2)| = 5%
          design speed gives K = 52 (crest, stopping sight distance)

          L = 52 x 5 = 260 m of vertical curve
```

```mermaid
graph TD
    SPEED["Design speed"] --> HORIZ["Horizontal alignment"]
    SPEED --> VERT["Vertical alignment"]
    HORIZ --> RAD["Minimum radius from e and f"]
    HORIZ --> SPIRAL["Transition spiral"]
    VERT --> SIGHT["Sight distance controls length"]
    SIGHT --> KVAL["K value gives curve length"]
    RAD --> SAFE["Safe comfortable 3D alignment"]
    KVAL --> SAFE
```

Remember: the design speed sets the numbers, superelevation plus friction
hold a vehicle on the horizontal curve, and sight distance sizes the
vertical curve.
""",
        ),
        quiz_lesson(
            "Quiz: Geometric design - curves and superelevation",
            (
                q(
                    "What two effects let a vehicle hold a horizontal curve?",
                    (
                        opt("Braking and acceleration"),
                        opt(
                            "Side friction between tyre and road plus superelevation "
                            "(banking) of the road",
                            correct=True,
                        ),
                        opt("Wind resistance and gravity alone"),
                        opt("Only the width of the lane"),
                    ),
                    "R_min = V^2 / (127 x (e + f)) combines superelevation e and side friction f.",
                ),
                q(
                    "If design speed increases, what happens to the minimum curve radius?",
                    (
                        opt("It decreases"),
                        opt("It stays the same"),
                        opt(
                            "It increases - radius grows with the square of the speed",
                            correct=True,
                        ),
                        opt("Radius does not depend on speed"),
                    ),
                    "Because V is squared in R_min = V^2 / (127 (e+f)), faster roads need "
                    "much larger radii.",
                ),
                q(
                    "What primarily controls the length of a crest vertical curve?",
                    (
                        opt("The colour of the pavement"),
                        opt(
                            "Stopping sight distance - the driver must see far enough to stop",
                            correct=True,
                        ),
                        opt("The number of lanes"),
                        opt("The asphalt binder grade"),
                    ),
                    "On crest curves, length L = K x A is set so the driver can see and "
                    "stop for an object ahead.",
                ),
            ),
        ),
        # -- 3. Earthworks and mass-haul -------------------------------
        _t(
            "Earthworks and mass-haul diagrams",
            "11 min",
            """# Earthworks and mass-haul diagrams

Once the alignment is fixed, the ground rarely matches it. **Earthworks**
reshape the terrain: **cut** where you remove material (the road is below
the natural ground) and **fill** where you add it (the road is above).
The economic goal is to **balance cut and fill** so excavated material is
reused nearby instead of being dumped or imported.

A subtlety: soil changes volume when handled. **Bulking (swell)** makes
loose excavated soil occupy more than in place; **shrinkage** makes
compacted fill occupy less than the borrow it came from. A **shrinkage
factor** converts bank (in-place cut) volume to compacted fill volume.

The planning tool is the **mass-haul diagram**: cumulative earthwork
volume plotted along the road station by station. Cut is positive, fill
is negative.

```text
Mass-haul (worked mini-example, after shrinkage):

 Station   Cut(+)/Fill(-)   Cumulative
   0+000        0               0
   0+100      +400            +400   (cut)
   0+200      +300            +700   (peak - end of cut)
   0+300      -350            +350
   0+400      -350               0   (balance point)
   0+500      -200            -200   (fill exceeds cut -> borrow)

Reading it:
  - rising curve = cut zone,  falling curve = fill zone
  - a peak/valley marks the switch between cut and fill
  - where the curve crosses back to a previous level = the
    earthwork balances (haul from cut feeds the fill for free)
  - the curve ending below zero (-200) = a shortfall to be
    imported from a borrow pit
```

The horizontal distance material is moved is the **haul**; keeping haul
short is what saves money. Where the curve stays above the balance line,
cut is hauled forward into fill; where it dips below, you need **borrow**;
where it rises above available cut, you must **waste** the surplus.

```mermaid
graph LR
    ALIGN["Fixed alignment"] --> XSEC["Cross sections cut and fill"]
    XSEC --> SHRINK["Apply shrinkage factor"]
    SHRINK --> CUM["Cumulative volume"]
    CUM --> MHD["Mass haul diagram"]
    MHD --> BALANCE["Balance cut against fill"]
    BALANCE --> BORROW["Borrow where fill exceeds cut"]
    BALANCE --> WASTE["Waste where cut exceeds fill"]
```

Remember: earthworks are about moving the least material the shortest
distance - balance cut and fill, correct for shrinkage, and let the
mass-haul diagram show where to borrow or waste.
""",
        ),
        quiz_lesson(
            "Quiz: Earthworks and mass-haul diagrams",
            (
                q(
                    "What is the economic goal of earthworks design?",
                    (
                        opt("Maximize the amount of imported material"),
                        opt(
                            "Balance cut and fill so excavated material is reused nearby, "
                            "minimizing haul, borrow and waste",
                            correct=True,
                        ),
                        opt("Always dump all excavated soil off site"),
                        opt("Keep the road exactly at natural ground everywhere"),
                    ),
                    "Balancing cut and fill and keeping haul short is what controls "
                    "earthwork cost.",
                ),
                q(
                    "Why is a shrinkage factor applied when moving cut into fill?",
                    (
                        opt("Because soil never changes volume"),
                        opt(
                            "Compacted fill occupies less volume than the in-place bank "
                            "material it came from, so bank volume must be adjusted",
                            correct=True,
                        ),
                        opt("To make the diagram look better"),
                        opt("Because water is always added"),
                    ),
                    "Shrinkage converts in-place (bank) cut volume to compacted fill "
                    "volume so the balance is realistic.",
                ),
                q(
                    "On a mass-haul diagram, what does the curve dipping below the "
                    "balance line indicate?",
                    (
                        opt("A surplus of cut to be wasted"),
                        opt("A perfectly balanced section"),
                        opt(
                            "A shortfall - fill exceeds available cut, so material must "
                            "be imported from a borrow pit",
                            correct=True,
                        ),
                        opt("The end of the project"),
                    ),
                    "Below the balance line means fill is not covered by cut, requiring "
                    "borrow; above it means surplus cut to waste.",
                ),
            ),
        ),
        # -- 4. Pavement materials and binders -------------------------
        _t(
            "Pavement materials and asphalt binders",
            "11 min",
            """# Pavement materials and asphalt binders

A pavement is a **layered structure** and each layer does a job. From the
top down in a flexible pavement: a **surface (wearing) course** of asphalt
concrete, a **base** and **sub-base** of graded granular material, all
resting on the compacted **subgrade** (the natural soil). Loads spread
downward through the layers so the weak subgrade only sees a small stress.

**Asphalt concrete** is a mix of **aggregate** (about 95% by mass -
crushed stone and sand, well graded so particles interlock) bound by
**asphalt binder (bitumen)** - the black, viscoelastic glue (about 5% by
mass). The binder is the key variable: it is a **viscoelastic** material,
behaving like a stiff solid when cold or under fast traffic and like a
viscous liquid when hot or under slow load.

Two failures drive binder selection at the two temperature extremes:

- **Rutting** (permanent deformation) in hot weather - the binder must be
  **stiff enough** not to flow.
- **Thermal / fatigue cracking** in cold weather - the binder must be
  **soft enough** not to become brittle.

The modern **Superpave PG (Performance Grade)** system names a binder by
the pavement temperatures it must survive:

```text
Reading a Superpave grade:  PG 64-22

   PG 64 - 22
      |     |
      |     +--  lowest pavement temperature it resists = -22 C
      |          (guards against thermal cracking)
      +--------  highest pavement temperature it resists = +64 C
                 (guards against rutting)

A hotter climate -> higher first number (e.g. PG 70-16)
A colder climate -> lower  second number (e.g. PG 58-34)
Polymer modification widens the useful range (e.g. PG 76-22).
```

In Brazil, DNIT specifies binders by penetration/viscosity grades (for
example CAP 50/70) with similar intent. Either way, the binder is chosen
to the site climate and traffic.

```mermaid
graph TD
    SURF["Asphalt surface course"] --> BASE["Granular base"]
    BASE --> SUBBASE["Sub base"]
    SUBBASE --> SUBGRADE["Compacted subgrade"]
    BINDER["Asphalt binder viscoelastic"] --> HOT["Stiff enough resists rutting"]
    BINDER --> COLD["Soft enough resists cracking"]
    HOT --> PG["Performance grade selection"]
    COLD --> PG
```

Remember: the pavement spreads load through graded layers, and the asphalt
binder is a viscoelastic material graded (PG or penetration) to be stiff
in heat and soft in cold for the site.
""",
        ),
        quiz_lesson(
            "Quiz: Pavement materials and asphalt binders",
            (
                q(
                    "Why is a pavement built as a layered structure?",
                    (
                        opt("To use more material"),
                        opt(
                            "So wheel loads spread downward through progressively cheaper "
                            "layers, leaving only a small stress on the weak subgrade",
                            correct=True,
                        ),
                        opt("Only for appearance"),
                        opt("Because a single thick layer is impossible to build"),
                    ),
                    "Each layer spreads the load so the natural subgrade sees a manageable stress.",
                ),
                q(
                    "What does 'viscoelastic' mean for asphalt binder?",
                    (
                        opt("It is always a rigid solid"),
                        opt("It is always a liquid"),
                        opt(
                            "It behaves like a stiff solid when cold or under fast load "
                            "and like a viscous liquid when hot or under slow load",
                            correct=True,
                        ),
                        opt("It never changes with temperature"),
                    ),
                    "This dual behaviour is why binder grade must be matched to the "
                    "climate and traffic speed.",
                ),
                q(
                    "In the Superpave grade PG 64-22, what does the -22 represent?",
                    (
                        opt("The percentage of binder in the mix"),
                        opt(
                            "The lowest pavement temperature (-22 C) the binder must "
                            "resist, guarding against thermal cracking",
                            correct=True,
                        ),
                        opt("The number of layers"),
                        opt("The design speed"),
                    ),
                    "The first number is the high-temperature limit (rutting), the second "
                    "is the low-temperature limit (cracking).",
                ),
            ),
        ),
        # -- 5. Flexible pavement design -------------------------------
        _t(
            "Flexible pavement design",
            "12 min",
            """# Flexible pavement design

A **flexible pavement** (asphalt over granular layers) carries load by
**spreading** it through the layers - it flexes slightly under each wheel
and relies on the strength of every layer, especially the subgrade. Design
means choosing layer thicknesses so the structure survives the traffic
loads over its design life.

## Traffic in load repetitions, not vehicles

Pavements do not care about vehicles equally - a loaded truck axle does
thousands of times the damage of a car. So traffic is converted to
**ESALs** (Equivalent Single Axle Loads) using the AASHTO **fourth-power
law**: the damage of an axle rises with roughly the *fourth power* of its
load relative to the standard 80 kN (18 kip) single axle.

```text
Load equivalency factor (approx):

        ( axle load  )^4
LEF  = ( ----------- )
        ( 80 kN std  )

Example:  one 100 kN axle vs the 80 kN standard

        (100/80)^4 = (1.25)^4 = 2.44

-> a single 100 kN axle = 2.44 standard ESALs.
   A 160 kN axle = (2.0)^4 = 16 ESALs - one heavy axle
   does the damage of sixteen standard ones.
```

Sum the ESALs from every axle over the design life to get the design
traffic **W18**.

## The AASHTO structural number

The AASHTO flexible method rolls the whole layered structure into one
**Structural Number (SN)**, a weighted sum of thickness x strength:

```text
SN = a1*D1 + a2*D2*m2 + a3*D3*m3

  ai = layer coefficient (material strength)
  Di = layer thickness
  mi = drainage coefficient

Example: surface a1 = 0.44, D1 = 100 mm (4 in)
         base    a2 = 0.14, D2 = 200 mm (8 in), m2 = 1.0
         subbase a3 = 0.11, D3 = 150 mm (6 in), m3 = 1.0
   (in inches)
   SN = 0.44*4 + 0.14*8*1.0 + 0.11*6*1.0
      = 1.76 + 1.12 + 0.66 = 3.54
```

The required SN comes from the design equation using W18, the subgrade
stiffness (**resilient modulus** MR, or CBR in simpler methods),
reliability and the allowable loss of serviceability. You then pick real
layer thicknesses whose SN meets or exceeds the requirement.

```mermaid
graph LR
    TRAFFIC["Mixed traffic"] --> ESAL["Convert to ESALs"]
    ESAL --> W18["Design traffic W18"]
    SUBG["Subgrade MR or CBR"] --> REQ["Required structural number"]
    W18 --> REQ
    REQ --> LAYERS["Choose layer thicknesses"]
    LAYERS --> SNCHECK["Provided SN meets required SN"]
```

Remember: convert traffic to ESALs with the fourth-power law, translate
subgrade strength and traffic into a required SN, then thicken the layers
until the provided SN clears it.
""",
        ),
        quiz_lesson(
            "Quiz: Flexible pavement design",
            (
                q(
                    "Why is traffic converted to ESALs for pavement design?",
                    (
                        opt("Because all vehicles damage the pavement equally"),
                        opt(
                            "Because damage rises steeply with axle load (about the "
                            "fourth power), so heavy axles must be weighted far more than "
                            "cars",
                            correct=True,
                        ),
                        opt("To count the number of lanes"),
                        opt("To measure the pavement colour"),
                    ),
                    "The fourth-power law means one heavy axle can equal thousands of "
                    "cars in damage; ESALs capture that.",
                ),
                q(
                    "By the fourth-power law, a 160 kN axle is worth about how many "
                    "80 kN standard ESALs?",
                    (
                        opt("2"),
                        opt("4"),
                        opt("16", correct=True),
                        opt("160"),
                    ),
                    "(160/80)^4 = 2^4 = 16 - one heavy axle equals sixteen standard ones.",
                ),
                q(
                    "What does the AASHTO Structural Number (SN) represent?",
                    (
                        opt("The number of vehicles per day"),
                        opt(
                            "The combined strength of the layered structure - a weighted "
                            "sum of each layer's coefficient times its thickness",
                            correct=True,
                        ),
                        opt("The pavement's colour grade"),
                        opt("The design speed of the road"),
                    ),
                    "SN = sum of ai*Di*mi; you thicken layers until the provided SN meets "
                    "the required SN.",
                ),
            ),
        ),
        # -- 6. Rigid pavement design ----------------------------------
        _t(
            "Rigid pavement design",
            "12 min",
            """# Rigid pavement design

A **rigid pavement** is a **Portland cement concrete (PCC)** slab resting
on a base and subgrade. Unlike flexible pavement, it carries load by
**bending as a stiff plate** - the slab's own flexural strength spreads
the wheel load over a wide area, so the subgrade sees very low stress. The
concrete does the structural work; the layers below mainly provide uniform
support.

The subgrade support is expressed as the **modulus of subgrade reaction k**
(pressure per unit deflection, in MPa/m or pci) - think of the soil as a
bed of springs under the slab.

## Where the slab is weakest

Concrete is strong in compression but weak in tension, and a load bends
the slab, putting the bottom (or top) in tension. Critical stress depends
on **where** the wheel sits:

- **Interior** loading - lowest stress.
- **Edge** loading - higher.
- **Corner** loading - most critical; the slab is least supported there.

Westergaard's classic edge-stress form shows what matters:

```text
Slab edge stress (schematic Westergaard form):

           P
   sigma = --- x f( l / b )         l = radius of relative stiffness
           h^2

   l = [ E h^3 / (12 (1 - v^2) k) ] ^ 0.25

  P = wheel load, h = slab thickness, E,v = concrete properties,
  k = subgrade reaction

Key lever: stress falls with the SQUARE of slab thickness h.
Doubling nothing else, going from 200 mm to 250 mm slab cuts the
critical stress by roughly (200/250)^2 = 0.64 -> a 36% reduction.
```

The slab is proportioned so this critical stress stays safely below the
concrete **flexural strength (modulus of rupture)** under the design number
of load repetitions (fatigue).

## Joints - the defining detail

Concrete shrinks and expands, so rigid pavements are divided into slabs by
**joints**: **contraction** joints (control where cracks form),
**expansion** joints, and **construction** joints. Load is carried across
joints by **dowel bars** (smooth, for load transfer) and slabs are tied
laterally with **tie bars**.

```mermaid
graph TD
    SLAB["Concrete slab as stiff plate"] --> BEND["Bends and spreads load"]
    BEND --> SUBG["Low stress on subgrade k"]
    LOAD["Wheel position"] --> INT["Interior lowest stress"]
    LOAD --> EDGE["Edge higher stress"]
    LOAD --> CORNER["Corner most critical"]
    SLAB --> JOINTS["Joints and dowels control cracking"]
```

Remember: the rigid slab spreads load by bending, corner and edge loading
govern, thickness cuts stress with its square, and joints with dowels
manage the inevitable movement.
""",
        ),
        quiz_lesson(
            "Quiz: Rigid pavement design",
            (
                q(
                    "How does a rigid concrete pavement carry wheel loads?",
                    (
                        opt("By spreading load flexibly through many granular layers"),
                        opt(
                            "By bending as a stiff plate whose flexural strength spreads "
                            "the load over a wide area, leaving low stress on the subgrade",
                            correct=True,
                        ),
                        opt("By transferring load only to the asphalt above it"),
                        opt("It cannot carry loads at all"),
                    ),
                    "The stiff slab does the structural work; the layers below mainly "
                    "give uniform support (modulus of subgrade reaction k).",
                ),
                q(
                    "Which loading position is most critical for a concrete slab?",
                    (
                        opt("Interior loading"),
                        opt("Edge loading"),
                        opt("Corner loading - the slab is least supported there", correct=True),
                        opt("All positions are identical"),
                    ),
                    "Corner is most critical, then edge, then interior - a key reason "
                    "dowels are placed at joints.",
                ),
                q(
                    "Why are contraction joints and dowel bars used in rigid pavements?",
                    (
                        opt("Purely for decoration"),
                        opt(
                            "Concrete shrinks and expands; joints control where cracks "
                            "form and dowels transfer load across the joint",
                            correct=True,
                        ),
                        opt("To make the slab thinner"),
                        opt("To increase the design speed"),
                    ),
                    "Joints manage the inevitable movement; dowels keep load transfer "
                    "smooth across them.",
                ),
            ),
        ),
        # -- 7. Pavement evaluation and maintenance --------------------
        _t(
            "Pavement evaluation and maintenance",
            "11 min",
            """# Pavement evaluation and maintenance

A pavement is an asset that **deteriorates** from the day it opens under
traffic and weather. **Pavement management** is the discipline of
measuring that decline and intervening at the right moment - because
repair gets dramatically more expensive the longer you wait.

## Measuring condition

Two families of measurement:

- **Functional** - how the road serves the user. **Roughness** is the key
  index, reported as **IRI** (International Roughness Index, m/km); rutting
  and skid resistance also count. A common summary is the **PSI/PCI**
  (present serviceability / pavement condition index).
- **Structural** - the load-carrying capacity. Measured
  **non-destructively** with a **Falling Weight Deflectometer (FWD)**,
  which drops a known load and reads the deflection bowl to back-calculate
  layer stiffnesses.

## The deterioration curve - why timing is everything

Condition follows a curve that falls slowly, then steeply. Acting while
the road is still fair is far cheaper than reconstructing after it fails:

```text
Condition (PCI)
 100 |*----____
     |          '*---__            <- preventive seal here is cheap
  70 |                 '*--_
     |                     '*_      <- rehabilitation
  40 |                        '*_
     |                           '*_
  10 |                              '*   <- reconstruction (most costly)
     +----------------------------------> time / traffic

Rule of thumb: money spent keeping a GOOD road good is a fraction
of the cost of rebuilding a FAILED one. Each 1 unit of preventive
maintenance can save several units of later rehabilitation.
```

## The maintenance ladder

Matched to where the road sits on the curve:

- **Preventive maintenance** - seals, thin overlays, crack sealing while
  the road is still good. Cheapest per year of life added.
- **Rehabilitation** - structural overlays, milling and resurfacing, when
  condition has dropped but the base is sound.
- **Reconstruction** - rebuild the structure once it has failed. Most
  costly; the outcome you plan to avoid.

```mermaid
graph LR
    OPEN["Road opens"] --> MEASURE["Measure IRI and FWD"]
    MEASURE --> INDEX["Condition index PCI"]
    INDEX --> GOOD["Good preventive seal"]
    INDEX --> FAIR["Fair rehabilitation"]
    INDEX --> POOR["Poor reconstruction"]
    GOOD --> LIFE["Extends life cheaply"]
```

Remember: measure both function (IRI) and structure (FWD), watch the
deterioration curve, and spend on preventive maintenance early - it is
far cheaper than waiting for reconstruction.
""",
        ),
        quiz_lesson(
            "Quiz: Pavement evaluation and maintenance",
            (
                q(
                    "What does the IRI measure?",
                    (
                        opt("The structural load capacity of the base"),
                        opt(
                            "Roughness - the functional ride quality of the pavement "
                            "surface, in m/km",
                            correct=True,
                        ),
                        opt("The asphalt binder grade"),
                        opt("The traffic volume"),
                    ),
                    "IRI is a functional (ride-quality) index; structural capacity is "
                    "measured separately (e.g. by FWD).",
                ),
                q(
                    "What does a Falling Weight Deflectometer evaluate?",
                    (
                        opt("The colour of the pavement"),
                        opt(
                            "Structural capacity - it drops a known load and reads the "
                            "deflection bowl to back-calculate layer stiffness, without "
                            "destroying the pavement",
                            correct=True,
                        ),
                        opt("The number of vehicles per hour"),
                        opt("The design speed"),
                    ),
                    "The FWD is a non-destructive structural test; the deflection bowl "
                    "reveals how stiff each layer is.",
                ),
                q(
                    "Why does the deterioration curve argue for early preventive maintenance?",
                    (
                        opt("Because condition improves over time on its own"),
                        opt(
                            "Because condition falls slowly then steeply; a small "
                            "preventive spend while the road is still good saves much "
                            "larger later rehabilitation or reconstruction cost",
                            correct=True,
                        ),
                        opt("Because reconstruction is always the cheapest option"),
                        opt("Because roads never need repair"),
                    ),
                    "Keeping a good road good costs a fraction of rebuilding a failed "
                    "one - timing on the curve is everything.",
                ),
            ),
        ),
        # -- 8. Traffic engineering, capacity and smart mobility -------
        _t(
            "Traffic engineering, capacity and smart mobility",
            "12 min",
            """# Traffic engineering, capacity and smart mobility

The road exists to move people. **Traffic engineering** studies the flow
itself, and **smart mobility** adds sensing and control to squeeze more
safe throughput from the same asphalt.

## The fundamental relationship

The three basic variables are **flow q** (vehicles per hour), **density k**
(vehicles per km) and **speed v** (km/h). They are tied by one identity:

```text
Fundamental relation of traffic flow:

        q = k x v      (flow = density x speed)

  - Empty road:   density low  -> free-flow speed, but little flow
  - Jammed road:  density high -> speed ~ 0, so flow ~ 0
  - Somewhere between lies the CAPACITY - the maximum flow

Example:  density k = 25 veh/km,  space-mean speed v = 80 km/h
          q = 25 x 80 = 2,000 veh/h per lane

Beyond a critical density, adding cars REDUCES flow -> congestion.
```

Plotting q against k gives the parabola-like **fundamental diagram**: flow
rises with density up to a **critical density**, peaks at **capacity**,
then falls into the congested regime.

## Capacity and level of service

The **Highway Capacity Manual (HCM)** rates a facility by **Level of
Service (LOS)** A to F - A is free flow, F is breakdown - based on a
measure of effectiveness (density on freeways, delay at signals). The
**volume-to-capacity (v/c) ratio** tells you how close you are to the edge.

## Smart mobility and ITS

**Intelligent Transportation Systems (ITS)** instrument the corridor:

- **Sensors** - inductive loops, radar, and **computer vision** cameras
  count and classify vehicles in real time.
- **Adaptive signal control** - signals retime themselves to actual demand
  instead of fixed plans.
- **Ramp metering and variable message signs** manage freeway inflow.
- **Connected and autonomous vehicles (V2X)**, and **ML models** predict
  congestion and feed it to travel-time and routing apps.
- **Digital twins** of the network let operators test control strategies
  before applying them, supporting sustainable, multimodal mobility.

```mermaid
graph TD
    SENSE["Sensors loops radar vision"] --> DATA["Real time flow data"]
    DATA --> DIAG["Fundamental diagram q equals k v"]
    DIAG --> LOS["Level of service and v over c"]
    DATA --> CONTROL["Adaptive signals and ramp metering"]
    CONTROL --> PREDICT["ML prediction and digital twin"]
    PREDICT --> FLOW["Safer smarter sustainable flow"]
```

Remember: flow equals density times speed with a capacity peak in between,
LOS grades how close you run to it, and ITS uses sensing, adaptive control
and prediction to move more people safely on the same road.
""",
        ),
        quiz_lesson(
            "Quiz: Traffic engineering, capacity and smart mobility",
            (
                q(
                    "What is the fundamental relationship of traffic flow?",
                    (
                        opt("Flow = speed / density"),
                        opt("Flow = density + speed"),
                        opt("Flow = density x speed (q = k x v)", correct=True),
                        opt("Flow is independent of density and speed"),
                    ),
                    "q = k v ties the three variables; capacity is the peak flow between "
                    "free-flow and jam conditions.",
                ),
                q(
                    "What happens to flow when density rises beyond the critical density?",
                    (
                        opt("Flow keeps rising without limit"),
                        opt(
                            "Flow decreases - the road enters the congested regime even "
                            "as more cars are added",
                            correct=True,
                        ),
                        opt("Flow stays exactly at capacity forever"),
                        opt("Speed increases"),
                    ),
                    "Past critical density, speed drops fast enough that q = k v falls - "
                    "that is congestion.",
                ),
                q(
                    "What is a defining capability of an ITS / smart-mobility system?",
                    (
                        opt("Repaving the road automatically"),
                        opt(
                            "Sensing traffic in real time (loops, radar, computer vision) "
                            "and adapting control - e.g. adaptive signals, ramp metering "
                            "and ML prediction",
                            correct=True,
                        ),
                        opt("Removing all traffic signals permanently"),
                        opt("Setting the asphalt binder grade"),
                    ),
                    "ITS instruments the corridor and closes the loop with adaptive "
                    "control and prediction, often supported by a digital twin.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "The Design Hourly Volume used to size a road is conventionally which hour?",
                    (
                        opt("The average hour of the year"),
                        opt("The single highest hour of the year"),
                        opt("The 30th highest hourly volume of the year", correct=True),
                        opt("A random midnight hour"),
                    ),
                    "The 30th-highest hour balances adequacy against economy; DHV = AADT x K.",
                ),
                q(
                    "For a horizontal curve, R_min = V^2 / (127 (e + f)). If design speed "
                    "doubles, the minimum radius roughly…",
                    (
                        opt("halves"),
                        opt("stays the same"),
                        opt(
                            "quadruples, because radius grows with the square of speed",
                            correct=True,
                        ),
                        opt("drops to zero"),
                    ),
                    "V is squared, so doubling speed multiplies the required radius by about four.",
                ),
                q(
                    "What controls the length of a crest vertical curve?",
                    (
                        opt("The asphalt colour"),
                        opt("Stopping sight distance, via L = K x A", correct=True),
                        opt("The number of joints"),
                        opt("The subgrade reaction k"),
                    ),
                    "Crest curves are sized so drivers can see and stop for an object "
                    "ahead; length = K times the grade change A.",
                ),
                q(
                    "On a mass-haul diagram, the curve ending below the balance line means…",
                    (
                        opt("surplus cut to be wasted"),
                        opt("a perfectly balanced project"),
                        opt("a fill shortfall requiring borrow material", correct=True),
                        opt("the road is complete"),
                    ),
                    "Below the balance line, fill exceeds available cut, so material must "
                    "be imported from a borrow pit.",
                ),
                q(
                    "In the Superpave grade PG 70-16, what does the 70 mean?",
                    (
                        opt("The percentage of aggregate"),
                        opt(
                            "The highest pavement temperature (70 C) the binder must "
                            "resist, guarding against rutting",
                            correct=True,
                        ),
                        opt("The number of load repetitions"),
                        opt("The slab thickness in mm"),
                    ),
                    "The first number is the high-temperature (rutting) limit; the second "
                    "is the low-temperature (cracking) limit.",
                ),
                q(
                    "Why is traffic converted to ESALs in flexible pavement design?",
                    (
                        opt("Because every vehicle causes equal damage"),
                        opt(
                            "Because damage rises with about the fourth power of axle "
                            "load, so heavy axles must be weighted far above cars",
                            correct=True,
                        ),
                        opt("To count the lanes"),
                        opt("To measure roughness"),
                    ),
                    "The AASHTO fourth-power law: a 160 kN axle = (2)^4 = 16 standard ESALs.",
                ),
                q(
                    "The AASHTO Structural Number (SN) is…",
                    (
                        opt("the daily vehicle count"),
                        opt(
                            "a weighted sum of each layer's coefficient, thickness and "
                            "drainage - the combined strength of the flexible structure",
                            correct=True,
                        ),
                        opt("the concrete flexural strength"),
                        opt("the design speed"),
                    ),
                    "SN = sum of ai*Di*mi; layers are thickened until provided SN meets "
                    "the required SN from traffic and subgrade.",
                ),
                q(
                    "For a rigid concrete pavement, which wheel position is most critical?",
                    (
                        opt("Interior loading"),
                        opt("Edge loading"),
                        opt("Corner loading, where the slab is least supported", correct=True),
                        opt("They are all equal"),
                    ),
                    "Corner is most critical, then edge, then interior - a reason dowels "
                    "transfer load across joints.",
                ),
                q(
                    "Doubling nothing else, increasing a rigid slab from 200 mm to 250 mm "
                    "cuts critical stress because stress varies with…",
                    (
                        opt("the cube of thickness"),
                        opt("the inverse square of slab thickness (1/h^2)", correct=True),
                        opt("thickness linearly"),
                        opt("the traffic volume only"),
                    ),
                    "Edge stress ~ P/h^2, so more thickness sharply reduces stress - "
                    "(200/250)^2 = 0.64, a 36% cut.",
                ),
                q(
                    "Which pair correctly matches the measurement to what it evaluates?",
                    (
                        opt("IRI measures structural capacity; FWD measures colour"),
                        opt(
                            "IRI measures functional roughness (ride quality); FWD "
                            "measures structural capacity via the deflection bowl",
                            correct=True,
                        ),
                        opt("Both measure traffic volume"),
                        opt("Both measure the binder grade"),
                    ),
                    "IRI is functional roughness; the non-destructive FWD gives structural "
                    "capacity.",
                ),
                q(
                    "Why favour early preventive maintenance over waiting?",
                    (
                        opt("Because roads improve on their own over time"),
                        opt(
                            "Because condition falls slowly then steeply; a small early "
                            "spend saves much larger later rehabilitation or "
                            "reconstruction cost",
                            correct=True,
                        ),
                        opt("Because reconstruction is the cheapest option"),
                        opt("Because maintenance is never needed"),
                    ),
                    "Keeping a good road good costs a fraction of rebuilding a failed one.",
                ),
                q(
                    "In the fundamental traffic relation q = k x v, what is 'capacity'?",
                    (
                        opt("The speed limit sign value"),
                        opt(
                            "The maximum flow, reached at the critical density between "
                            "free-flow and jammed conditions",
                            correct=True,
                        ),
                        opt("The total number of lanes"),
                        opt("The density when the road is empty"),
                    ),
                    "Flow peaks at capacity; beyond the critical density, adding vehicles "
                    "reduces flow (congestion). ITS helps hold flow near capacity.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

HIGHWAYS_PAVEMENT_MOBILITY_COURSES: tuple[SeedCourse, ...] = (_HIGHWAYS_PAVEMENT_MOBILITY,)
