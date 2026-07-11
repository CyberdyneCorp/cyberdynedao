"""Academy seed content - Foundations and Retaining Structures.

The geotechnical design course that connects the structure to the ground:
how to investigate a site, choose and size shallow or deep foundations,
check bearing capacity and settlement, and design the systems that hold
the earth back - lateral pressure theory, retaining walls, and slope and
reinforced-soil stabilization. Every lesson is a direct explanation with a
worked bearing-capacity or earth-pressure calculation and a mermaid
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


_FOUNDATIONS_RETAINING = SeedCourse(
    slug="foundations-retaining",
    title="Foundations & Retaining Structures",
    description=(
        "Designing what holds structures up and holds the ground back - "
        "shallow and deep foundations, bearing capacity and settlement, "
        "earth pressure and retaining systems. Every lesson pairs a direct "
        "explanation with a worked bearing-capacity or earth-pressure "
        "calculation and a diagram, grounded in ABNT NBR, Eurocode 7 and "
        "AASHTO practice."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Foundations and Retaining Structures

Every structure eventually rests on soil or rock, and much of civil
engineering is the quiet art of transferring loads into the ground safely
and holding unstable earth in place. This course is about that interface:
**foundations** that carry the building down into competent ground, and
**retaining structures** that resist the lateral push of soil and water.

The approach is **direct and quantitative**: each lesson explains one idea
clearly, works a short real calculation (a bearing-capacity check, an
earth-pressure resultant, a settlement estimate), and draws the mechanism
as a diagram. After each lesson there is a checkpoint quiz; a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **Geotechnical investigation and SPT** - reading the ground before you design
2. **Shallow foundations** - footings and rafts near the surface
3. **Deep foundations** - piles and caissons reaching competent strata
4. **Bearing capacity** - the load the soil can carry before it fails
5. **Settlement** - how much the foundation moves, and soil-structure interaction
6. **Lateral earth pressure** - Rankine and Coulomb theory
7. **Retaining walls** - gravity, cantilever, and anchored systems
8. **Earthworks and slope stabilization** - reinforced soil and stability

Two design questions recur throughout: **will it fail** (an ultimate limit
state - bearing, sliding, overturning) and **will it move too much** (a
serviceability limit state - settlement, tilt). Good geotechnical design
answers both, with the site investigation from lesson one grounding every
number that follows.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What two families of structures does this course cover?",
                    (
                        opt("Bridges and tunnels"),
                        opt(
                            "Foundations that carry loads into the ground, and "
                            "retaining structures that hold unstable earth back",
                            correct=True,
                        ),
                        opt("Roofs and facades"),
                        opt("Pipelines and pumps"),
                    ),
                    "Foundations transfer load down into competent ground; retaining "
                    "structures resist the lateral push of soil and water.",
                ),
                q(
                    "The course frames design around which two recurring questions?",
                    (
                        opt("What color and what shape"),
                        opt("Which contractor and what schedule"),
                        opt(
                            "Will it fail (ultimate limit state) and will it move too "
                            "much (serviceability limit state)",
                            correct=True,
                        ),
                        opt("How tall and how heavy"),
                    ),
                    "Ultimate limit states (bearing, sliding, overturning) and "
                    "serviceability limit states (settlement, tilt) must both be checked.",
                ),
            ),
        ),
        # -- 1. Site investigation / SPT -------------------------------
        _t(
            "Geotechnical investigation and SPT",
            "10 min",
            """# Geotechnical investigation and SPT

You cannot design a foundation for ground you have not characterized. A
**geotechnical investigation** determines the soil profile, groundwater
level, and strength and stiffness of each layer, so the designer knows
what is under the structure before choosing a foundation type.

The workhorse in most of the world is the **Standard Penetration Test
(SPT)**, standardized in Brazil as **ABNT NBR 6484** and internationally
as ASTM D1586. A sampler is driven into the borehole base by a 65 kg
hammer falling 75 cm; the number of blows to drive the final 30 cm is the
**N value** (in Brazil, N-SPT or `N60` after energy correction). High N
means dense sand or stiff clay; low N means loose or soft ground.

The N value feeds correlations for strength and stiffness. A common
first-pass estimate of an **allowable bearing pressure** for shallow
footings on sand uses N directly. One classic rule of thumb:

```text
Allowable bearing pressure (footing on sand), Terzaghi-Peck style:

    q_all ~= 10 * N60      [kPa], for settlement limited to ~25 mm

Worked example - medium-dense sand, N60 = 20:

    q_all ~= 10 * 20 = 200 kPa

So a 2.0 m x 2.0 m footing could carry about:

    Q_all = q_all * A = 200 kPa * (2.0 * 2.0) m^2 = 800 kN
```

The full investigation combines **borings** (SPT, sampling), sometimes
**CPT** (cone penetration) for a continuous profile, and lab tests on
recovered samples for classification (USCS / ABNT NBR 6502), Atterberg
limits, and consolidation. Groundwater is logged because it changes
effective stress and therefore strength.

```mermaid
graph TD
    SITE["Site and loads"] --> BORE["Borings and SPT"]
    BORE --> N["N values per layer"]
    BORE --> GW["Groundwater level"]
    BORE --> LAB["Lab tests classify and strength"]
    N --> PROFILE["Soil profile and parameters"]
    GW --> PROFILE
    LAB --> PROFILE
    PROFILE --> DESIGN["Foundation design decisions"]
```

Remember: the investigation is not paperwork - every strength, stiffness,
and water table used later comes from it. Under-investigating is the most
expensive economy in foundation engineering.
""",
        ),
        quiz_lesson(
            "Quiz: Geotechnical investigation and SPT",
            (
                q(
                    "What does the SPT N value measure?",
                    (
                        opt("The chemical composition of the soil"),
                        opt(
                            "The number of hammer blows to drive the sampler the final "
                            "30 cm - a proxy for soil density and strength",
                            correct=True,
                        ),
                        opt("The color of the soil sample"),
                        opt("The groundwater flow rate"),
                    ),
                    "High N means dense sand or stiff clay; low N means loose or soft "
                    "ground. It feeds strength and stiffness correlations.",
                ),
                q(
                    "Using q_all ~= 10 * N60 kPa, what is the allowable bearing pressure "
                    "for a sand layer with N60 = 15?",
                    (
                        opt("15 kPa"),
                        opt("150 kPa", correct=True),
                        opt("1500 kPa"),
                        opt("10 kPa"),
                    ),
                    "10 * 15 = 150 kPa. It is a first-pass, settlement-limited estimate, "
                    "not a substitute for a full bearing-capacity check.",
                ),
                q(
                    "Why is the groundwater level always logged during investigation?",
                    (
                        opt("To decide the paint color"),
                        opt(
                            "It changes effective stress and therefore soil strength and "
                            "the loads on the foundation",
                            correct=True,
                        ),
                        opt("It has no effect on design"),
                        opt("Only to estimate drinking water supply"),
                    ),
                    "Effective stress governs strength; a high water table reduces it "
                    "and adds uplift and hydrostatic pressure.",
                ),
            ),
        ),
        # -- 2. Shallow foundations ------------------------------------
        _t(
            "Shallow foundations (footings, rafts)",
            "10 min",
            """# Shallow foundations (footings, rafts)

A **shallow foundation** spreads a structural load onto competent soil
near the surface, at an embedment depth roughly comparable to its width.
When the ground close to the surface is strong enough, shallow foundations
are the cheapest and simplest choice.

The common types:

- **Isolated (spread) footing** - a single pad under one column. The most
  common element; sized so the soil pressure stays within allowable.
- **Strip footing** - a continuous footing under a wall or a line of
  columns.
- **Combined footing** - one footing under two or more columns, used when
  they are close or near a property line.
- **Raft (mat) foundation** - a single thick slab under the whole
  structure. Chosen when column loads are heavy, soil is weak, or footings
  would otherwise overlap. It averages pressure and bridges soft spots.

Sizing an isolated footing is fundamentally area from pressure: pick a
plan area so the applied pressure does not exceed the allowable bearing
pressure `q_all`.

```text
Isolated footing sizing - service load method:

    Required area  A_req = P / q_all
    Square footing side  B = sqrt(A_req)

Worked example - column load P = 1200 kN, q_all = 250 kPa:

    A_req = 1200 kN / 250 kPa = 4.8 m^2
    B = sqrt(4.8) = 2.19 m   ->  adopt B = 2.20 m (A = 4.84 m^2)

Check contact pressure:
    q = P / A = 1200 / 4.84 = 248 kPa  <=  250 kPa   OK
```

A **raft** is preferred once the summed footing area would exceed roughly
half the building footprint, or where differential settlement between
separate footings would be intolerable - the stiff slab ties the columns
together and shares load.

```mermaid
graph TD
    LOAD["Column and wall loads"] --> Q["Which soil is competent"]
    Q -->|"strong shallow soil"| SHALLOW["Shallow foundation"]
    SHALLOW --> FOOT["Isolated or strip footing"]
    SHALLOW --> COMB["Combined footing"]
    SHALLOW --> RAFT["Raft when loads heavy or soil weak"]
    Q -->|"weak shallow soil"| DEEP["Go to deep foundation"]
```

Remember: shallow foundations turn a concentrated column load into a soil
pressure. Size for area first (q_all), then verify bearing capacity and
settlement - the next two lessons.
""",
        ),
        quiz_lesson(
            "Quiz: Shallow foundations (footings, rafts)",
            (
                q(
                    "When is a raft (mat) foundation typically preferred over isolated footings?",
                    (
                        opt("Always, because it is cheapest"),
                        opt(
                            "When loads are heavy or soil is weak so footings would "
                            "overlap, or to control differential settlement",
                            correct=True,
                        ),
                        opt("Only for single-column sheds"),
                        opt("Only on solid rock"),
                    ),
                    "A raft averages pressure across the whole footprint and ties "
                    "columns together, bridging soft spots.",
                ),
                q(
                    "A column carries P = 900 kN and q_all = 300 kPa. What is the "
                    "required footing area?",
                    (
                        opt("3.0 m^2", correct=True),
                        opt("0.33 m^2"),
                        opt("30 m^2"),
                        opt("270 m^2"),
                    ),
                    "A_req = P / q_all = 900 / 300 = 3.0 m^2 (a square side of about 1.73 m).",
                ),
                q(
                    "What defines a foundation as 'shallow'?",
                    (
                        opt("It is made of shallow concrete"),
                        opt(
                            "It bears near the surface, at an embedment depth roughly "
                            "comparable to its width, spreading load onto competent soil",
                            correct=True,
                        ),
                        opt("It is less than 1 cm thick"),
                        opt("It only carries wind load"),
                    ),
                    "Shallow foundations rely on strong soil near the surface; when that "
                    "is absent, deep foundations reach lower strata.",
                ),
            ),
        ),
        # -- 3. Deep foundations ---------------------------------------
        _t(
            "Deep foundations (piles, caissons)",
            "10 min",
            """# Deep foundations (piles, caissons)

When competent soil is too deep for footings, a **deep foundation**
transfers load past the weak upper layers to strong strata below. Piles
and caissons carry load two ways: **end (tip) bearing** on the firm layer
they reach, and **skin (shaft) friction** along their sides.

```text
Pile axial capacity - static formula:

    Q_ult = Q_tip + Q_shaft
    Q_tip   = q_p * A_tip           (unit tip resistance x tip area)
    Q_shaft = sum( f_s,i * A_side,i ) (unit skin friction x side area)

    Q_all = Q_ult / FS              (FS ~ 2.0 to 3.0)

Worked example - bored pile, D = 0.5 m, L = 12 m:
    A_tip  = pi/4 * 0.5^2 = 0.196 m^2
    A_side = pi * 0.5 * 12 = 18.85 m^2
    q_p    = 3000 kPa,  f_s = 40 kPa (average)

    Q_tip   = 3000 * 0.196   = 589 kN
    Q_shaft = 40 * 18.85     = 754 kN
    Q_ult   = 589 + 754      = 1343 kN
    Q_all   = 1343 / 2.5     = 537 kN
```

The main families:

- **Driven piles** - precast concrete, steel, or timber hammered into
  place. They displace soil (densifying sand) and their driving resistance
  is itself a capacity check.
- **Bored piles / drilled shafts** - a hole is augered and filled with
  reinforced concrete. Low vibration; can reach large diameters and depths.
- **Continuous flight auger (CFA)** - concrete pumped through a hollow
  auger as it withdraws; fast and quiet.
- **Caissons** - large-diameter shafts (sometimes hand or machine dug)
  that carry very heavy loads, common under bridge piers.

Piles rarely act alone: a group shares a **pile cap**, and **group
efficiency** (piles interfering with each other's stress bulbs) means the
group capacity is usually less than the sum of individual piles.

```mermaid
graph TD
    LOAD["Heavy load and weak upper soil"] --> DEEP["Deep foundation"]
    DEEP --> DRIVEN["Driven pile"]
    DEEP --> BORED["Bored pile or drilled shaft"]
    DEEP --> CAIS["Caisson"]
    DRIVEN --> CAP["Load into pile"]
    BORED --> CAP
    CAIS --> CAP
    CAP --> TIP["End bearing on firm stratum"]
    CAP --> SKIN["Skin friction along shaft"]
```

Remember: a deep foundation reaches down to strength the surface lacks,
splitting its capacity between the tip and the shaft - and a group of
piles is not simply the sum of its parts.
""",
        ),
        quiz_lesson(
            "Quiz: Deep foundations (piles, caissons)",
            (
                q(
                    "How does a pile carry axial load?",
                    (
                        opt("Only by floating on groundwater"),
                        opt(
                            "By a combination of end (tip) bearing on a firm stratum and "
                            "skin friction along its shaft",
                            correct=True,
                        ),
                        opt("Only by adhesion to the pile cap"),
                        opt("Only by wind suction"),
                    ),
                    "Q_ult = Q_tip + Q_shaft; the split depends on soil profile and pile type.",
                ),
                q(
                    "A pile has Q_tip = 500 kN and Q_shaft = 700 kN. With a factor of "
                    "safety of 2.0, what is the allowable capacity?",
                    (
                        opt("2400 kN"),
                        opt("600 kN", correct=True),
                        opt("1200 kN"),
                        opt("100 kN"),
                    ),
                    "Q_ult = 500 + 700 = 1200 kN; Q_all = 1200 / 2.0 = 600 kN.",
                ),
                q(
                    "Why is a pile group's capacity usually less than the sum of the "
                    "individual piles?",
                    (
                        opt("The concrete gets weaker in groups"),
                        opt(
                            "Group efficiency - closely spaced piles overlap each "
                            "other's stress zones and interfere",
                            correct=True,
                        ),
                        opt("Groups are never used in practice"),
                        opt("The pile cap removes all capacity"),
                    ),
                    "Overlapping stress bulbs reduce group efficiency below 100 percent, "
                    "so the group is checked as a block as well.",
                ),
            ),
        ),
        # -- 4. Bearing capacity ---------------------------------------
        _t(
            "Bearing capacity of foundations",
            "11 min",
            """# Bearing capacity of foundations

**Bearing capacity** is the maximum pressure the soil can support before a
**shear failure** forms beneath the foundation - a wedge of soil punches
down and heaves up beside the footing. It is the ultimate limit state for
a foundation, distinct from settlement (the serviceability limit).

**Terzaghi's bearing-capacity equation** for a strip footing sums three
contributions - cohesion, surcharge (soil above founding level), and the
footing's own width:

```text
Terzaghi ultimate bearing capacity (strip footing):

    q_ult = c * Nc  +  q * Nq  +  0.5 * gamma * B * Ng

    c     = soil cohesion               [kPa]
    q     = gamma * Df  (surcharge)     [kPa]
    gamma = unit weight of soil         [kN/m^3]
    B     = footing width               [m]
    Nc, Nq, Ng = bearing-capacity factors (function of phi)

Worked example - strip footing, B = 2 m, Df = 1 m,
gamma = 18 kN/m^3, c = 10 kPa, phi = 30 deg
(Nc = 37.2, Nq = 22.5, Ng = 19.7):

    q     = 18 * 1 = 18 kPa
    q_ult = 10*37.2 + 18*22.5 + 0.5*18*2*19.7
          = 372 + 405 + 354.6
          = 1131.6 kPa

    Allowable (FS = 3):
    q_all = 1131.6 / 3 = 377 kPa
```

The **bearing-capacity factors** `Nc`, `Nq`, `Ng` grow rapidly with the
friction angle `phi`: dense sand (high phi) carries far more than soft
clay. For a purely cohesive clay under undrained loading `phi = 0`, the
formula collapses to the familiar `q_ult = 5.14 * cu + q`.

Real footings are rarely infinite strips, so **shape, depth, and
inclination factors** modify the base equation (Meyerhof, Vesic, and
Eurocode 7 / ABNT NBR 6122 give these). A **factor of safety of about 3**
on ultimate capacity gives the allowable pressure used to size footings.

```mermaid
graph TD
    Q["Applied pressure"] --> COMP["Compare to capacity"]
    C["Cohesion term c Nc"] --> QULT["Ultimate q_ult"]
    S["Surcharge term q Nq"] --> QULT
    W["Width term half gamma B Ng"] --> QULT
    QULT --> FS["Divide by factor of safety"]
    FS --> QALL["Allowable pressure"]
    QALL --> COMP
    COMP --> OK["Safe if applied is below allowable"]
```

Remember: bearing capacity is a shear-failure limit. Terzaghi sums
cohesion, surcharge, and width terms; the friction angle drives the
factors; and a factor of safety of roughly 3 separates ultimate from
allowable.
""",
        ),
        quiz_lesson(
            "Quiz: Bearing capacity of foundations",
            (
                q(
                    "What physical failure does bearing capacity guard against?",
                    (
                        opt("Corrosion of the rebar"),
                        opt(
                            "A shear failure in the soil - a wedge punching down and "
                            "heaving up beside the footing",
                            correct=True,
                        ),
                        opt("Cracking of the concrete from heat"),
                        opt("Wind uplift on the roof"),
                    ),
                    "It is the ultimate limit state: the soil shears before the "
                    "foundation can carry more load.",
                ),
                q(
                    "In Terzaghi's equation q_ult = c*Nc + q*Nq + 0.5*gamma*B*Ng, what "
                    "does the middle term represent?",
                    (
                        opt("The cohesion of the soil"),
                        opt(
                            "The surcharge from soil above the founding level (q = gamma * Df)",
                            correct=True,
                        ),
                        opt("The weight of the building"),
                        opt("The groundwater pressure only"),
                    ),
                    "c*Nc is cohesion, q*Nq is surcharge from embedment depth, and "
                    "0.5*gamma*B*Ng is the footing-width term.",
                ),
                q(
                    "If q_ult = 900 kPa and a factor of safety of 3 is applied, what is "
                    "the allowable bearing pressure?",
                    (
                        opt("2700 kPa"),
                        opt("300 kPa", correct=True),
                        opt("900 kPa"),
                        opt("3 kPa"),
                    ),
                    "q_all = q_ult / FS = 900 / 3 = 300 kPa.",
                ),
                q(
                    "Why does dense sand have a much higher bearing capacity than soft clay?",
                    (
                        opt("It is a different color"),
                        opt(
                            "The bearing-capacity factors Nc, Nq and Ng grow rapidly "
                            "with the friction angle phi",
                            correct=True,
                        ),
                        opt("Clay has no weight"),
                        opt("Sand is always saturated"),
                    ),
                    "High phi means large N factors; clay under undrained loading uses "
                    "phi = 0 and q_ult = 5.14 cu + q.",
                ),
            ),
        ),
        # -- 5. Settlement ---------------------------------------------
        _t(
            "Foundation settlement and soil-structure interaction",
            "11 min",
            """# Foundation settlement and soil-structure interaction

A foundation can be perfectly safe against bearing failure yet still fail
its purpose by **settling too much**. Settlement is the serviceability
limit state, and often the one that actually governs design, especially on
clays.

Total settlement has three parts:

- **Immediate (elastic) settlement** - happens as load is applied, from
  elastic distortion of the soil. Dominant in sands.
- **Primary consolidation** - slow squeezing of water out of saturated
  clay under load; can take months to years. Dominant in clays.
- **Secondary compression (creep)** - very slow rearrangement of the soil
  skeleton after consolidation ends.

For a normally consolidated clay layer, primary consolidation settlement
comes from the compression index `Cc`:

```text
Consolidation settlement (normally consolidated clay):

    S_c = (Cc / (1 + e0)) * H * log10( (sigma0 + d_sigma) / sigma0 )

    Cc      = compression index
    e0      = initial void ratio
    H       = clay layer thickness
    sigma0  = initial effective stress at layer mid-depth
    d_sigma = stress increase from the foundation

Worked example - H = 3 m, Cc = 0.30, e0 = 0.90,
sigma0 = 100 kPa, d_sigma = 60 kPa:

    ratio = (100 + 60) / 100 = 1.60
    S_c = (0.30 / 1.90) * 3.0 * log10(1.60)
        = 0.1579 * 3.0 * 0.204
        = 0.097 m  ~=  97 mm
```

What usually matters is not total settlement but **differential
settlement** - the difference between points - because that is what cracks
walls, jams doors, and tilts a structure. Codes limit **angular
distortion** (differential settlement divided by span); a common
serviceability limit is about 1/500 for framed buildings.

This is where **soil-structure interaction** enters: the foundation and
the superstructure are not independent. A stiff raft or a stiff frame
redistributes load away from soft spots, reducing differential settlement,
while a flexible structure follows the ground. Modern design increasingly
models the two together rather than assuming a rigid foundation on springs.

```mermaid
graph TD
    LOAD["Foundation load"] --> IMM["Immediate elastic settlement"]
    LOAD --> CONS["Primary consolidation in clay"]
    LOAD --> SEC["Secondary creep"]
    IMM --> TOTAL["Total settlement"]
    CONS --> TOTAL
    SEC --> TOTAL
    TOTAL --> DIFF["Differential settlement"]
    DIFF --> DIST["Angular distortion limit"]
    STIFF["Structure stiffness"] --> DIFF
```

Remember: bearing capacity asks if it will fail; settlement asks if it
will move too much - and differential movement, not total, is usually what
damages the structure. Design the soil and the structure as one system.
""",
        ),
        quiz_lesson(
            "Quiz: Foundation settlement and soil-structure interaction",
            (
                q(
                    "Which settlement component dominates in saturated clays and can "
                    "take months to years?",
                    (
                        opt("Immediate elastic settlement"),
                        opt("Primary consolidation settlement", correct=True),
                        opt("Wind-induced settlement"),
                        opt("Thermal settlement"),
                    ),
                    "Consolidation is the slow squeezing of water from clay; immediate "
                    "elastic settlement dominates in sands.",
                ),
                q(
                    "Why does differential settlement usually matter more than total settlement?",
                    (
                        opt("It is easier to measure"),
                        opt(
                            "Differential movement is what cracks walls, tilts the "
                            "structure and jams openings - angular distortion is limited "
                            "by codes",
                            correct=True,
                        ),
                        opt("Total settlement is never a concern"),
                        opt("It only affects the paint"),
                    ),
                    "A uniform settlement can be tolerated; a difference between points "
                    "causes distortion and damage.",
                ),
                q(
                    "In the consolidation formula, increasing the compression index Cc "
                    "does what to the predicted settlement?",
                    (
                        opt("Decreases it"),
                        opt("Increases it", correct=True),
                        opt("Has no effect"),
                        opt("Makes it negative"),
                    ),
                    "S_c is proportional to Cc / (1 + e0); a more compressible clay "
                    "(higher Cc) settles more.",
                ),
                q(
                    "What is the core idea of soil-structure interaction?",
                    (
                        opt("Soil and structure never affect each other"),
                        opt(
                            "The stiffness of the foundation and superstructure "
                            "redistributes load and controls differential settlement - "
                            "they behave as one system",
                            correct=True,
                        ),
                        opt("The structure floats freely above the soil"),
                        opt("Only the soil deforms, never the structure"),
                    ),
                    "A stiff raft or frame moves load away from soft spots; modern "
                    "design models the two together.",
                ),
            ),
        ),
        # -- 6. Lateral earth pressure ---------------------------------
        _t(
            "Lateral earth pressure (Rankine, Coulomb)",
            "11 min",
            """# Lateral earth pressure (Rankine, Coulomb)

Soil pushes sideways. Any wall that retains a soil mass must resist that
**lateral earth pressure**, and how much pressure depends on whether the
wall can move. Three states matter:

- **At-rest** `K0` - the wall does not move; the soil keeps its in-situ
  horizontal stress. `K0 ~= 1 - sin(phi)` for normally consolidated soil.
- **Active** `Ka` - the wall moves *away* from the soil; the soil relaxes
  and pushes with the minimum pressure. This is the usual design case for
  a free-standing retaining wall.
- **Passive** `Kp` - the wall pushes *into* the soil; the soil resists
  with the maximum pressure. This is the resistance in front of a wall toe
  or an embedded sheet pile.

**Rankine theory** gives the coefficients for a smooth vertical wall with
horizontal backfill:

```text
Rankine coefficients (cohesionless, horizontal backfill):

    Ka = (1 - sin phi) / (1 + sin phi) = tan^2(45 - phi/2)
    Kp = (1 + sin phi) / (1 - sin phi) = tan^2(45 + phi/2)

Active pressure at depth z:   p_a = Ka * gamma * z
Total active thrust on wall height H:
    Pa = 0.5 * Ka * gamma * H^2   (acts at H/3 above the base)

Worked example - dry sand wall, H = 5 m,
gamma = 18 kN/m^3, phi = 32 deg:

    Ka = tan^2(45 - 16) = tan^2(29) = 0.307
    Pa = 0.5 * 0.307 * 18 * 5^2
       = 0.5 * 0.307 * 18 * 25
       = 69.1 kN per metre of wall
    Line of action: 5 / 3 = 1.67 m above the base
```

**Coulomb theory** is more general: it accounts for **wall friction**
(the roughness between wall and soil), a **sloping backfill**, and a
**battered wall face**, by analyzing a sliding soil wedge. Rankine is the
simpler special case; Coulomb is what you use when the geometry or wall
friction cannot be ignored, and it is the basis of most retaining-wall
codes.

Two more effects: **water** behind a wall adds a full hydrostatic pressure
on top of the (reduced, effective-stress) soil pressure, which is why
drainage is critical; and a **surcharge** on the backfill adds a uniform
`Ka * q` to the soil pressure.

```mermaid
graph TD
    WALL["Retaining wall and backfill"] --> MOVE["Does the wall move"]
    MOVE -->|"no movement"| K0["At rest K0"]
    MOVE -->|"away from soil"| KA["Active Ka minimum"]
    MOVE -->|"into the soil"| KP["Passive Kp maximum"]
    KA --> THRUST["Active thrust Pa"]
    THRUST --> POINT["Acts at one third H above base"]
```

Remember: pressure depends on wall movement (active is the design push,
passive the resistance). Rankine handles the simple case; Coulomb adds
wall friction and slope. Always add water and surcharge - and drain the
backfill.
""",
        ),
        quiz_lesson(
            "Quiz: Lateral earth pressure (Rankine, Coulomb)",
            (
                q(
                    "Which earth-pressure state is the usual design case for a "
                    "free-standing retaining wall?",
                    (
                        opt("Passive - the maximum pressure"),
                        opt(
                            "Active - the wall moves slightly away from the soil, which "
                            "then pushes with the minimum pressure",
                            correct=True,
                        ),
                        opt("At-rest only, always"),
                        opt("Hydrostatic only"),
                    ),
                    "A yielding wall mobilizes the active state; passive is the "
                    "resistance in front of the toe.",
                ),
                q(
                    "For sand with phi = 30 deg, Ka = tan^2(45 - phi/2). What is Ka?",
                    (
                        opt("0.33", correct=True),
                        opt("3.0"),
                        opt("1.0"),
                        opt("0.03"),
                    ),
                    "tan^2(45 - 15) = tan^2(30) = 0.333. Kp would be its reciprocal, about 3.0.",
                ),
                q(
                    "What does Coulomb theory account for that simple Rankine theory does not?",
                    (
                        opt("Nothing - they are identical"),
                        opt(
                            "Wall friction, a sloping backfill, and a battered wall face, "
                            "by analyzing a sliding soil wedge",
                            correct=True,
                        ),
                        opt("Only the color of the soil"),
                        opt("The temperature of the wall"),
                    ),
                    "Rankine is the smooth-wall, horizontal-backfill special case; "
                    "Coulomb is the more general wedge analysis.",
                ),
                q(
                    "Why is drainage behind a retaining wall critical?",
                    (
                        opt("To keep the wall clean"),
                        opt(
                            "Water adds a full hydrostatic pressure on top of the soil "
                            "pressure, greatly increasing the total thrust",
                            correct=True,
                        ),
                        opt("Water has no effect on the wall"),
                        opt("It only matters for the paint"),
                    ),
                    "Undrained water can double the thrust; weep holes and granular "
                    "drains relieve it.",
                ),
            ),
        ),
        # -- 7. Retaining walls ----------------------------------------
        _t(
            "Retaining walls (gravity, cantilever, anchored)",
            "11 min",
            """# Retaining walls (gravity, cantilever, anchored)

A **retaining wall** holds a soil mass at a slope steeper than it could
stand on its own. The earth pressure from the previous lesson is the load;
the wall must be checked against several failure modes at once.

The main types, by how they resist the thrust:

- **Gravity wall** - a massive block of concrete or masonry whose sheer
  weight resists sliding and overturning. Simple, used for lower heights.
- **Cantilever wall** - a slender reinforced-concrete stem on a base slab.
  The weight of backfill sitting on the **heel** helps hold it down, so it
  uses far less material than a gravity wall - the workhorse up to ~8 m.
- **Counterfort wall** - a cantilever with triangular ribs tying stem to
  base, for greater heights.
- **Anchored / tied-back wall** - a sheet-pile or diaphragm wall held by
  **ground anchors** (tendons grouted into stable soil behind the failure
  wedge). Used for deep excavations where a free-standing wall is
  impractical.

Every retaining wall is checked against three **external** failures plus
internal structural strength:

```text
Retaining-wall stability checks (per metre of wall):

  1. Overturning about the toe:
       FS_ot = (sum resisting moments) / (overturning moment) >= 2.0
  2. Sliding along the base:
       FS_sl = (friction + passive) / (horizontal thrust) >= 1.5
  3. Bearing: base pressure <= allowable bearing capacity

Worked example - overturning of a wall, H = 5 m:
  Active thrust Pa = 69 kN at 1.67 m above base
  Overturning moment  M_ot = 69 * 1.67 = 115 kN.m
  Wall + backfill weight W = 260 kN acting 1.9 m from toe
  Resisting moment    M_r = 260 * 1.9 = 494 kN.m

  FS_ot = 494 / 115 = 4.3   >= 2.0   OK
```

The **sliding** check often governs and is the hardest to satisfy; a
**base key** (a downward projection) mobilizes extra passive resistance to
help. **Overturning** is checked about the toe. **Bearing** uses the
capacity theory from lesson four, watching for an eccentric, trapezoidal
pressure distribution under the base. A separate **global (slope) stability**
check makes sure the whole wall-and-soil block does not slide on a deep
surface - the subject of the next lesson.

```mermaid
graph TD
    THRUST["Active earth thrust"] --> WALL["Retaining wall"]
    WALL --> OT["Check overturning about toe"]
    WALL --> SL["Check sliding on base"]
    WALL --> BR["Check bearing under base"]
    WALL --> ST["Check structural strength"]
    OT --> SAFE["Wall is stable"]
    SL --> SAFE
    BR --> SAFE
    ST --> SAFE
```

Remember: choose the wall type by height and site (gravity, cantilever,
anchored), then prove it against overturning, sliding, and bearing - plus
its own structural strength and the global stability of the slope.
""",
        ),
        quiz_lesson(
            "Quiz: Retaining walls (gravity, cantilever, anchored)",
            (
                q(
                    "How does a cantilever retaining wall use less material than a gravity wall?",
                    (
                        opt("It is hollow and filled with air"),
                        opt(
                            "The weight of backfill resting on its heel slab helps hold "
                            "it down, so the stem can be slender reinforced concrete",
                            correct=True,
                        ),
                        opt("It relies only on rebar with no concrete"),
                        opt("It floats on water"),
                    ),
                    "A gravity wall resists by its own mass alone; a cantilever recruits "
                    "the backfill weight on the heel.",
                ),
                q(
                    "A wall has a resisting moment of 480 kN.m and an overturning moment "
                    "of 120 kN.m. What is the factor of safety against overturning?",
                    (
                        opt("4.0", correct=True),
                        opt("0.25"),
                        opt("600"),
                        opt("360"),
                    ),
                    "FS_ot = M_resisting / M_overturning = 480 / 120 = 4.0, comfortably "
                    "above the usual 2.0 minimum.",
                ),
                q(
                    "Which stability check often governs a retaining wall and can be "
                    "helped by a base key?",
                    (
                        opt("Overturning about the toe"),
                        opt("Sliding along the base", correct=True),
                        opt("Concrete shrinkage"),
                        opt("Wind on the exposed face"),
                    ),
                    "Sliding is frequently the hardest to satisfy; a base key mobilizes "
                    "extra passive resistance.",
                ),
                q(
                    "What holds an anchored (tied-back) wall in place?",
                    (
                        opt("Only its own weight"),
                        opt(
                            "Ground anchors - tendons grouted into stable soil behind "
                            "the failure wedge",
                            correct=True,
                        ),
                        opt("Nothing, it is temporary scaffolding"),
                        opt("Passive pressure alone at the top"),
                    ),
                    "Anchored walls suit deep excavations where a free-standing wall is "
                    "impractical; anchors reach past the active wedge.",
                ),
            ),
        ),
        # -- 8. Earthworks / slope stabilization -----------------------
        _t(
            "Earthworks, slope stabilization and reinforced soil",
            "11 min",
            """# Earthworks, slope stabilization and reinforced soil

Not every soil-retention problem is a wall. **Earthworks** shape the
ground itself - cuts and fills, embankments, and slopes - and where a
slope is too steep to stand alone, engineers either flatten it, drain it,
or reinforce it.

A slope fails when the **shear stress** driving a soil mass down a surface
exceeds the **shear strength** resisting it. The measure is the **factor
of safety**:

```text
Slope factor of safety (infinite-slope, drained cohesionless):

    FS = tan(phi) / tan(beta)

    phi  = soil friction angle
    beta = slope angle from horizontal

Worked example - dry sand slope, phi = 34 deg, beta = 25 deg:

    FS = tan(34) / tan(25) = 0.6745 / 0.4663 = 1.45   (stable, > 1)

With seepage parallel to the slope, effective stress drops and:
    FS ~= (gamma' / gamma_sat) * tan(phi) / tan(beta)
which can push FS below 1 - why drainage is the first line of defence.
```

For general slopes with cohesion, **method-of-slices** analyses (Bishop,
Fellenius, Morgenstern-Price) divide the mass and sum forces on a trial
circular or non-circular surface, searching for the critical (lowest-FS)
one - the same global-stability check that guards a retaining wall.

Ways to stabilize a slope:

- **Regrade** - flatten the slope or add a stabilizing berm at the toe.
- **Drainage** - surface channels and subsurface drains lower pore
  pressure; often the cheapest and most effective single measure.
- **Retaining structures** - walls, soldier piles, or soil nails pin the
  mass.
- **Reinforced soil** - layers of **geogrid** or steel strips built into a
  compacted fill create a **Mechanically Stabilized Earth (MSE)** mass
  that acts as a coherent gravity block. This is the basis of modern MSE
  walls and reinforced-soil embankments (AASHTO and ABNT NBR guidance),
  and of **geosynthetic-reinforced** steep slopes.

Good earthworks also depend on **compaction** control - placing fill in
lifts at the right moisture content to reach a target density (the Proctor
test), because a poorly compacted fill settles and weakens.

```mermaid
graph TD
    SLOPE["Slope or embankment"] --> FS["Factor of safety of shear"]
    FS -->|"too low"| STAB["Stabilize"]
    STAB --> GRADE["Regrade or add toe berm"]
    STAB --> DRAIN["Drainage lowers pore pressure"]
    STAB --> STRUCT["Walls or soil nails"]
    STAB --> MSE["Reinforced soil with geogrid MSE"]
    FS -->|"adequate"| OK["Slope is stable"]
```

Remember: a slope stands when strength beats the driving stress. Drain it
first, regrade or reinforce if needed - and reinforced soil turns a
compacted fill into its own gravity structure. Control compaction, or the
best design settles anyway.
""",
        ),
        quiz_lesson(
            "Quiz: Earthworks, slope stabilization and reinforced soil",
            (
                q(
                    "For a dry cohesionless slope, FS = tan(phi) / tan(beta). If "
                    "phi = 34 deg and beta = 25 deg, the slope is:",
                    (
                        opt("Failing, because FS is below 1"),
                        opt(
                            "Stable, because FS = 1.45 which is greater than 1",
                            correct=True,
                        ),
                        opt("Independent of the friction angle"),
                        opt("Only stable if it rains"),
                    ),
                    "tan(34)/tan(25) = 1.45 > 1. Seepage lowers effective stress and can "
                    "push FS below 1, which is why drainage matters.",
                ),
                q(
                    "What is Mechanically Stabilized Earth (MSE)?",
                    (
                        opt("A type of concrete gravity wall"),
                        opt(
                            "A compacted fill reinforced with layers of geogrid or steel "
                            "strips so the mass acts as a coherent gravity block",
                            correct=True,
                        ),
                        opt("Soil that needs no compaction"),
                        opt("A drainage pipe system"),
                    ),
                    "Reinforcement layers give the fill internal tensile capacity; the "
                    "reinforced mass then behaves like a gravity structure.",
                ),
                q(
                    "Which single measure is often the cheapest and most effective way "
                    "to stabilize a slope?",
                    (
                        opt("Painting the slope face"),
                        opt(
                            "Drainage - lowering pore pressure with surface and subsurface drains",
                            correct=True,
                        ),
                        opt("Adding load at the crest"),
                        opt("Removing all vegetation"),
                    ),
                    "Water is the enemy of slopes; lowering pore pressure raises "
                    "effective stress and the factor of safety.",
                ),
                q(
                    "Why is compaction control (e.g. the Proctor test) important in earthworks?",
                    (
                        opt("It makes the fill a nicer color"),
                        opt(
                            "Fill placed in lifts at the right moisture reaches a target "
                            "density; poorly compacted fill settles and weakens",
                            correct=True,
                        ),
                        opt("It has no effect on performance"),
                        opt("It only matters for concrete"),
                    ),
                    "Density controls strength and settlement; the Proctor test sets the "
                    "moisture-density target for field compaction.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does the SPT N value primarily indicate?",
                    (
                        opt("The soil color"),
                        opt(
                            "The blow count to drive the sampler - a proxy for soil "
                            "density and strength",
                            correct=True,
                        ),
                        opt("The exact groundwater flow rate"),
                        opt("The concrete grade"),
                    ),
                    "N feeds strength and stiffness correlations; it comes from the site "
                    "investigation that grounds every later number.",
                ),
                q(
                    "A column carries 1500 kN and the allowable bearing pressure is "
                    "250 kPa. What footing area is required?",
                    (
                        opt("6.0 m^2", correct=True),
                        opt("0.17 m^2"),
                        opt("60 m^2"),
                        opt("375 m^2"),
                    ),
                    "A = P / q_all = 1500 / 250 = 6.0 m^2 (a square side of about 2.45 m).",
                ),
                q(
                    "How does a pile transfer load to the ground?",
                    (
                        opt("Only through the pile cap"),
                        opt(
                            "Through end (tip) bearing plus skin friction along the shaft",
                            correct=True,
                        ),
                        opt("Only by buoyancy"),
                        opt("Only through the reinforcing steel"),
                    ),
                    "Q_ult = Q_tip + Q_shaft; deep foundations reach strength the surface lacks.",
                ),
                q(
                    "In Terzaghi's bearing-capacity equation, which factors grow "
                    "rapidly with the friction angle phi?",
                    (
                        opt("The unit weight only"),
                        opt(
                            "The bearing-capacity factors Nc, Nq and Ng",
                            correct=True,
                        ),
                        opt("The factor of safety"),
                        opt("The footing thickness"),
                    ),
                    "Higher phi means much larger N factors, so dense sand carries far "
                    "more than soft clay.",
                ),
                q(
                    "Which limit state is about the foundation moving too much rather "
                    "than shearing the soil?",
                    (
                        opt("Bearing capacity"),
                        opt("Settlement (serviceability)", correct=True),
                        opt("Sliding"),
                        opt("Overturning"),
                    ),
                    "Bearing capacity is the ultimate (failure) limit; settlement is the "
                    "serviceability limit and often governs on clay.",
                ),
                q(
                    "For a retaining wall that yields slightly, which earth-pressure "
                    "coefficient applies to the backfill push?",
                    (
                        opt("Passive Kp"),
                        opt("At-rest K0"),
                        opt("Active Ka", correct=True),
                        opt("Hydrostatic only"),
                    ),
                    "A wall moving away from the soil mobilizes the active (minimum) "
                    "state; passive is the resistance in front of the toe.",
                ),
                q(
                    "The active thrust on a wall is Pa = 0.5 * Ka * gamma * H^2. For "
                    "Ka = 0.30, gamma = 18 kN/m^3, H = 4 m, what is Pa per metre?",
                    (
                        opt("43.2 kN", correct=True),
                        opt("21.6 kN"),
                        opt("108 kN"),
                        opt("10.8 kN"),
                    ),
                    "0.5 * 0.30 * 18 * 16 = 43.2 kN/m, acting at H/3 = 1.33 m above the base.",
                ),
                q(
                    "Which three external checks must a retaining wall satisfy?",
                    (
                        opt("Color, texture, and finish"),
                        opt(
                            "Overturning about the toe, sliding on the base, and bearing "
                            "under the base",
                            correct=True,
                        ),
                        opt("Wind, snow, and seismic only"),
                        opt("Compression, tension, and torsion of the rebar only"),
                    ),
                    "Plus internal structural strength and global slope stability of the "
                    "whole wall-and-soil block.",
                ),
                q(
                    "For a dry cohesionless slope, when is FS = tan(phi)/tan(beta) "
                    "greater than 1 (stable)?",
                    (
                        opt("When the slope angle beta exceeds phi"),
                        opt(
                            "When the friction angle phi exceeds the slope angle beta",
                            correct=True,
                        ),
                        opt("Only when the soil is saturated"),
                        opt("Never for sand"),
                    ),
                    "A cohesionless slope stands as long as it is flatter than the "
                    "friction angle; seepage lowers effective stress and FS.",
                ),
                q(
                    "What is the working principle of reinforced soil (MSE)?",
                    (
                        opt("It removes the need to compact fill"),
                        opt(
                            "Geogrid or steel reinforcement layers give a compacted fill "
                            "internal tensile capacity so the mass acts as a gravity "
                            "block",
                            correct=True,
                        ),
                        opt("It replaces soil with concrete entirely"),
                        opt("It relies only on drainage"),
                    ),
                    "The reinforced mass behaves as a coherent gravity structure - the "
                    "basis of MSE walls and reinforced-soil slopes.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

FOUNDATIONS_RETAINING_COURSES: tuple[SeedCourse, ...] = (_FOUNDATIONS_RETAINING,)
