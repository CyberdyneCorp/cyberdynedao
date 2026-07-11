"""Academy seed content - Construction Materials.

A working tour of the materials civil engineers build with: aggregates,
binders (cement, lime, gypsum), mortars, structural steel and rebar,
ceramics, and timber. Each lesson explains the material's properties and
behaviour, shows a real characterization test, spec table or design
formula, and draws the idea as a diagram, followed by a checkpoint quiz;
the course closes with a comprehensive final quiz. Grounded in everyday
practice and standards (ABNT/NBR, ASTM, ACI, Eurocode).
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


_CONSTRUCTION_MATERIALS = SeedCourse(
    slug="construction-materials",
    title="Construction Materials",
    description=(
        "The materials civil engineers build with - aggregates, binders, "
        "mortars, steel, ceramics and timber - their properties, "
        "characterization tests and quality control. Every lesson pairs a "
        "direct explanation with a real test procedure, spec table or design "
        "formula and a diagram, grounded in ABNT/NBR, ASTM, ACI and Eurocode "
        "practice."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Construction Materials

Structures are only as good as what they are made of. Before you can
design a beam or a pavement, you need to understand the **materials**:
what they are, how they behave under load and weather, how we **test**
them, and how quality is controlled on site and in the lab.

The approach is **small and concrete**: every lesson explains one family
of materials directly, shows it in a real example - a test procedure, a
specification table, or a design formula - and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Aggregates** - properties, grading, and the tests that qualify them
2. **Cements, lime and gypsum** - the binders that hold everything together
3. **Mortars** - proportioning and where each mix is used
4. **Structural steel and rebar** - strength, ductility, and bar identification
5. **Ceramic materials** - bricks, blocks and tiles
6. **Timber** - a natural, anisotropic structural material
7. **Material characterization tests** - the shared lab toolkit
8. **Standardization and quality control** - ABNT/NBR, ASTM and acceptance

This is the map. Concrete, steel design and geotechnics build directly on
these fundamentals - knowing the materials makes those courses far easier.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the focus of this course?",
                    (
                        opt("Only the structural analysis of finished buildings"),
                        opt(
                            "The materials civil engineers build with - their "
                            "properties, characterization tests and quality control",
                            correct=True,
                        ),
                        opt("Construction site safety regulations only"),
                        opt("Architectural drawing conventions"),
                    ),
                    "The course covers aggregates, binders, mortars, steel, ceramics "
                    "and timber - properties, testing and quality control.",
                ),
                q(
                    "What does each content lesson pair its explanation with?",
                    (
                        opt("A full building design project"),
                        opt(
                            "A real example - a test procedure, spec table or design "
                            "formula - plus a diagram",
                            correct=True,
                        ),
                        opt("Nothing - it is explanation only"),
                        opt("A video lecture"),
                    ),
                    "Direct explanation + one concrete example + a diagram, then a "
                    "checkpoint quiz.",
                ),
            ),
        ),
        # -- 1. Aggregates ---------------------------------------------
        _t(
            "Aggregates - properties, grading, tests",
            "10 min",
            """# Aggregates - properties, grading, tests

**Aggregates** are the granular materials - sand, gravel, crushed stone -
that make up roughly **70 percent of the volume** of concrete and mortar.
They are far cheaper than cement and, being inert and strong, they carry
much of the load. Good aggregate is not filler; it is structure.

We classify them by size:

- **Fine aggregate** (sand) - passes the 4.75 mm sieve (NBR NM 248 / ASTM
  C33). It fills the gaps between the coarse grains.
- **Coarse aggregate** (gravel, crushed stone) - retained on 4.75 mm. Its
  **maximum size** must suit the member and rebar spacing.

The key properties an engineer checks:

- **Grading (particle-size distribution)** - a well-graded mix has a
  smooth spread of sizes so small grains fill the voids between large
  ones. Less void means less paste needed, so a stronger, cheaper mix.
- **Fineness modulus (FM)** - a single number summarizing sand coarseness,
  from a standard sieve stack. Higher FM = coarser sand.
- **Specific gravity and water absorption** - needed to convert between
  mass and volume and to correct mix water for moisture the grains hold.
- **Cleanliness** - clay, silt and organic matter weaken the paste-to-
  aggregate bond; limits are set by standard.
- **Abrasion resistance** - the Los Angeles abrasion test (ASTM C131)
  measures wear, critical for road surface aggregate.

The **fineness modulus** is the sum of the cumulative percentages
retained on the standard sieves, divided by 100:

```text
Fineness Modulus (FM)
---------------------
FM = (sum of cumulative % retained on standard sieves) / 100

Standard sieves: 4.75, 2.36, 1.18, 0.60, 0.30, 0.15 mm

Worked example (cumulative % retained):
  4.75 mm .....  0
  2.36 mm ..... 12
  1.18 mm ..... 33
  0.60 mm ..... 57
  0.30 mm ..... 78
  0.15 mm ..... 95
  sum = 275   ->   FM = 275 / 100 = 2.75

FM about 2.3-3.1 is a typical medium sand for concrete.
```

```mermaid
graph TD
    SAMPLE["Aggregate sample"] --> SIEVE["Sieve analysis"]
    SIEVE --> FINE["Fine aggregate sand"]
    SIEVE --> COARSE["Coarse aggregate gravel"]
    FINE --> FM["Fineness modulus"]
    SIEVE --> GRADE["Grading curve"]
    GRADE --> WELL["Well graded low voids"]
    GRADE --> POOR["Poorly graded high voids"]
```

Remember: aggregate quality is decided by **grading, cleanliness and
strength** - measured with the sieve stack, absorption and abrasion tests
before a single batch of concrete is mixed.
""",
        ),
        quiz_lesson(
            "Quiz: Aggregates - properties, grading, tests",
            (
                q(
                    "What roughly separates fine from coarse aggregate?",
                    (
                        opt("The 0.075 mm sieve"),
                        opt("The 4.75 mm sieve - fine passes it, coarse is retained", correct=True),
                        opt("The 19 mm sieve"),
                        opt("Colour of the grains"),
                    ),
                    "By NBR NM 248 / ASTM C33, 4.75 mm is the fine-coarse boundary.",
                ),
                q(
                    "Why is a well-graded aggregate desirable?",
                    (
                        opt("It looks more uniform"),
                        opt(
                            "A smooth spread of sizes fills voids, so less paste is "
                            "needed and the mix is stronger and cheaper",
                            correct=True,
                        ),
                        opt("It weighs less"),
                        opt("It absorbs more water"),
                    ),
                    "Small grains fill gaps between large ones - lower void content, "
                    "less cement paste required.",
                ),
                q(
                    "The fineness modulus is computed how?",
                    (
                        opt("Maximum grain size divided by minimum grain size"),
                        opt(
                            "Sum of the cumulative percentages retained on the standard "
                            "sieves, divided by 100",
                            correct=True,
                        ),
                        opt("Mass of the sample divided by its volume"),
                        opt("Percentage of clay in the sample"),
                    ),
                    "Higher FM means a coarser sand; medium sand is about 2.3-3.1.",
                ),
            ),
        ),
        # -- 2. Cements, lime and gypsum -------------------------------
        _t(
            "Cements, lime and gypsum",
            "11 min",
            """# Cements, lime and gypsum

**Binders** are the materials that set and harden to glue aggregates into
a solid mass. The three classic mineral binders differ in *how* they
harden and *where* they belong.

**Portland cement** is the dominant binder. It is a **hydraulic** binder:
it reacts with water (**hydration**) and hardens even under water. Ground
clinker plus a little gypsum, its main compounds are C3S and C2S (which
give strength) and C3A and C4AF. Key facts:

- Sold by **strength class** - e.g. NBR 16697 CP II-32 or EN 197 CEM I
  42.5, where the number is the 28-day compressive strength in MPa.
- The **gypsum** added to clinker is a **set retarder** - without it the
  C3A would flash-set in minutes.
- Hydration is **exothermic**; mass concrete must manage this heat to
  avoid thermal cracking.

**Lime** comes from burning limestone to **quicklime** (CaO), then
**slaking** with water to **hydrated lime** (Ca(OH)2). Building lime is
mostly **air lime**: it hardens slowly by **carbonation** - reabsorbing
CO2 from the air - so it needs air, not submersion. It gives mortars
plasticity and the ability to "heal" fine cracks.

**Gypsum plaster** is calcined gypsum (CaSO4 hemihydrate). It sets fast by
rehydrating back to the dihydrate, gives a smooth finish, but is
water-soluble - so it is an **interior**, dry-environment material.

```mermaid
graph TD
    BIND["Mineral binders"] --> CEM["Portland cement"]
    BIND --> LIME["Lime"]
    BIND --> GYP["Gypsum plaster"]
    CEM --> HYD["Hydraulic sets with water"]
    LIME --> CARB["Air lime sets by carbonation"]
    GYP --> INT["Interior fast set water soluble"]
    HYD --> STR["Structural strength"]
    CARB --> PLAST["Plasticity and workability"]
```

A quick reference for where each binder belongs:

```text
Binder            Hardening        Water resistant?   Typical use
----------------  ---------------  -----------------  -------------------------
Portland cement   Hydration        Yes                Concrete, structural mortar
Air lime          Carbonation      No (needs air)     Renders, plasticizer
Gypsum plaster    Rehydration      No (interior)      Interior plaster, boards

Strength class reading: CP II-32  ->  ~32 MPa at 28 days
                        CEM I 42.5 ->  ~42.5 MPa at 28 days
```

Remember: **cement is hydraulic and structural, lime hardens in air and
adds workability, gypsum is a fast interior finish** - match the binder to
the exposure.
""",
        ),
        quiz_lesson(
            "Quiz: Cements, lime and gypsum",
            (
                q(
                    "What does 'hydraulic binder' mean, and which of these is one?",
                    (
                        opt("A binder that needs no water; gypsum"),
                        opt(
                            "A binder that hardens by reacting with water, even under "
                            "water; Portland cement",
                            correct=True,
                        ),
                        opt("A binder made from water; air lime"),
                        opt("A binder that only sets in a vacuum; clinker"),
                    ),
                    "Portland cement hydrates and hardens even submerged; air lime and "
                    "gypsum do not.",
                ),
                q(
                    "Why is gypsum added when grinding Portland clinker?",
                    (
                        opt("To colour the cement"),
                        opt("To make it cheaper"),
                        opt("As a set retarder, stopping the C3A from flash-setting", correct=True),
                        opt("To increase the maximum aggregate size"),
                    ),
                    "Without gypsum the C3A phase would flash-set within minutes.",
                ),
                q(
                    "In the class 'CP II-32' or 'CEM I 42.5', what does the number mean?",
                    (
                        opt("The bag mass in kilograms"),
                        opt("The 28-day compressive strength in MPa", correct=True),
                        opt("The maximum aggregate size in mm"),
                        opt("The setting time in minutes"),
                    ),
                    "The number is the characteristic 28-day compressive strength.",
                ),
            ),
        ),
        # -- 3. Mortars ------------------------------------------------
        _t(
            "Mortars and their applications",
            "10 min",
            """# Mortars and their applications

A **mortar** is a workable paste of **binder + fine aggregate + water**
(and often additives) that bonds units together or coats a surface. It is
the same idea as concrete but with **no coarse aggregate** - which is what
lets it be spread in thin, worked layers.

Mortars are named by their **binder**:

- **Cement mortar** - strong, water-resistant, but stiff and prone to
  shrinkage cracking if too rich.
- **Lime mortar** - very workable and flexible, breathable, self-healing
  of hairline cracks, but low strength and slow to gain it.
- **Cement-lime (mixed) mortar** - the everyday workhorse: cement for
  strength, lime for workability and crack tolerance.

And by their **job**:

- **Laying (bedding) mortar** - beds masonry units and transfers load.
- **Rendering / plastering mortar** - coats walls; the coarse render coat
  levels, the fine skim finishes.
- **Grout** - a fluid mortar that fills joints and cavities.

The recipe is a **volumetric proportion** binder : lime : sand, for
example **1 : 1 : 6** (cement : lime : sand). More sand = leaner, weaker,
more permeable; more cement = stronger but stiffer and more crack-prone.

```text
Mixing a 1 : 1 : 6 cement:lime:sand bedding mortar (by volume)
--------------------------------------------------------------
For 1 part cement (say 1 x 35 L bucket):
  cement .... 1 bucket   (~50 kg bag ~ 35 L loose)
  lime ...... 1 bucket
  sand ...... 6 buckets
  water ..... add to a plastic, workable consistency

Rule of thumb (masonry cement mortar classes, ASTM C270):
  Type M (1 : 0.25 : 3.5)  strongest, below-grade, retaining
  Type S (1 : 0.5  : 4.5)  structural, high bond
  Type N (1 : 1    : 6  )  general above-grade masonry
  Type O (1 : 2    : 9  )  interior, non-load-bearing
```

```mermaid
graph TD
    MIX["Mortar binder plus sand plus water"] --> CEMENT["Cement mortar strong"]
    MIX --> LIMEM["Lime mortar workable"]
    MIX --> MIXED["Cement lime mortar balanced"]
    MIXED --> BED["Bedding masonry units"]
    MIXED --> REND["Rendering and plastering"]
    MIXED --> GROUT["Grouting joints"]
```

Remember: choose the mortar so it is **no stronger than it needs to be** -
a mortar softer than the units cracks in the joints (easy to repair)
rather than through the bricks (hard to repair).
""",
        ),
        quiz_lesson(
            "Quiz: Mortars and their applications",
            (
                q(
                    "What distinguishes a mortar from concrete?",
                    (
                        opt("Mortar uses no water"),
                        opt(
                            "Mortar has no coarse aggregate, so it spreads in thin layers",
                            correct=True,
                        ),
                        opt("Mortar contains no binder"),
                        opt("Mortar is always stronger than concrete"),
                    ),
                    "Binder + fine aggregate + water, no gravel - which is why it can be "
                    "worked in thin coats.",
                ),
                q(
                    "Why add lime to a cement mortar?",
                    (
                        opt("To make it set faster"),
                        opt(
                            "For workability and crack tolerance, while the cement "
                            "provides strength",
                            correct=True,
                        ),
                        opt("To make it waterproof"),
                        opt("To replace the sand"),
                    ),
                    "Cement-lime mortar balances strength with plasticity and hairline-"
                    "crack tolerance.",
                ),
                q(
                    "Why should a bedding mortar be no stronger than it needs to be?",
                    (
                        opt("To save money only"),
                        opt(
                            "So cracking occurs in the repairable joints rather than "
                            "through the masonry units",
                            correct=True,
                        ),
                        opt("Because strong mortar is illegal"),
                        opt("So it sets more slowly"),
                    ),
                    "A mortar softer than the units sacrifices the joint, protecting the "
                    "harder-to-repair bricks.",
                ),
            ),
        ),
        # -- 4. Structural steel and rebar -----------------------------
        _t(
            "Structural steel and reinforcement bars",
            "11 min",
            """# Structural steel and reinforcement bars

Concrete is strong in compression but weak in tension; **steel** supplies
the tension capacity, and it is also the material of frames, beams and
connections. Steel is an **iron-carbon alloy** whose behaviour is defined
by its **stress-strain curve**.

Key mechanical properties, read from a tensile test:

- **Yield strength (fy)** - the stress at which the steel begins to deform
  permanently. The main design value for reinforcement.
- **Ultimate tensile strength (fu)** - the peak stress before necking.
- **Ductility** - the elongation before rupture. Steel's ability to yield
  and stretch (rather than shatter) gives structures **warning before
  failure** and is essential for seismic design.
- **Modulus of elasticity (E)** - about **200 GPa** for steel, nearly
  constant across grades; it sets stiffness, not strength.

**Reinforcement bars (rebar)** are graded by yield strength and surface:

- Brazilian NBR 7480 grades: **CA-25** (smooth, fy = 250 MPa), **CA-50**
  (ribbed, fy = 500 MPa - the standard), **CA-60** (ribbed wire, higher
  strength, often for stirrups).
- **Ribs (deformations)** create mechanical **bond** so the bar and
  concrete act together; smooth bars rely on friction only.
- ASTM A615 uses Grade 60 (fy about 420 MPa) as its common equivalent.

The elastic part of the curve follows **Hooke's law**:

```text
Elastic behaviour of steel (Hooke's law)
----------------------------------------
stress = E x strain        (below the yield point)
  sigma = E * epsilon

Worst-case check example - a CA-50 bar, 12.5 mm diameter:
  area A = pi/4 * (12.5 mm)^2 = 122.7 mm^2
  yield force = fy * A = 500 MPa * 122.7 mm^2
              = 61,350 N  ~  61.4 kN

Design (NBR 6118): fyd = fy / 1.15 = 500 / 1.15 = 435 MPa
```

```mermaid
graph TD
    LOAD["Apply tension"] --> ELASTIC["Elastic region Hooke law"]
    ELASTIC --> YIELD["Yield strength fy"]
    YIELD --> PLASTIC["Plastic deformation"]
    PLASTIC --> ULT["Ultimate strength fu"]
    ULT --> RUPT["Rupture after elongation"]
    YIELD --> DUCT["Ductility gives warning"]
```

Remember: for reinforcement the governing number is **yield strength
(fy)**, ductility gives the structure **warning before failure**, and the
**ribs bond** the bar to the concrete so the two work as one.
""",
        ),
        quiz_lesson(
            "Quiz: Structural steel and reinforcement bars",
            (
                q(
                    "Why is steel used to reinforce concrete?",
                    (
                        opt("Concrete is weak in compression, steel is strong in compression"),
                        opt(
                            "Concrete is weak in tension, and steel supplies the tension capacity",
                            correct=True,
                        ),
                        opt("Steel makes the concrete lighter"),
                        opt("Steel stops the concrete from setting"),
                    ),
                    "Concrete carries compression well; steel is added for the tension "
                    "it cannot take.",
                ),
                q(
                    "What does the CA-50 designation tell you (NBR 7480)?",
                    (
                        opt("A smooth bar with 250 MPa strength"),
                        opt("A ribbed bar with a yield strength of 500 MPa", correct=True),
                        opt("A bar 50 mm in diameter"),
                        opt("A bar with 50 percent carbon"),
                    ),
                    "CA-50 is the standard ribbed bar, fy = 500 MPa; CA-25 is smooth at 250 MPa.",
                ),
                q(
                    "Why does ductility matter in structural steel?",
                    (
                        opt("It makes the steel cheaper"),
                        opt(
                            "It lets the steel yield and stretch, giving warning before "
                            "failure - vital for seismic design",
                            correct=True,
                        ),
                        opt("It increases the modulus of elasticity"),
                        opt("It prevents the steel from rusting"),
                    ),
                    "Ductile steel deforms visibly before rupture instead of shattering "
                    "without warning.",
                ),
                q(
                    "Roughly what is the modulus of elasticity of structural steel?",
                    (
                        opt("About 20 GPa"),
                        opt("About 200 GPa, nearly constant across grades", correct=True),
                        opt("About 2000 GPa"),
                        opt("It varies with yield strength from 100 to 900 GPa"),
                    ),
                    "E is about 200 GPa for all common steel grades; it sets stiffness, "
                    "not strength.",
                ),
            ),
        ),
        # -- 5. Ceramic materials --------------------------------------
        _t(
            "Ceramic materials - bricks, blocks, tiles",
            "10 min",
            """# Ceramic materials - bricks, blocks, tiles

**Ceramics** are made by shaping clay and **firing** it at high
temperature. Firing drives off water and **sinters** the clay grains into
a hard, durable, fire-resistant body. The family covers structural units
(bricks and hollow blocks) and finishes (floor and wall tiles).

The main products:

- **Solid and perforated bricks** - the classic small unit, laid in
  mortar. Perforations lighten them and improve insulation.
- **Hollow ceramic blocks (tijolo/bloco)** - large voided units for fast
  masonry; the sealing block (bloco de vedacao) is non-structural, the
  structural block (bloco estrutural) carries load.
- **Tiles (ceramic and porcelain)** - fired finishes; porcelain tile is
  fired hotter and denser, so it absorbs far less water.

The properties that decide fitness for use:

- **Compressive strength** - governs structural masonry; a sealing block
  needs less than a load-bearing one (NBR 15270 sets minimums).
- **Water absorption** - a **durability and frost indicator**; a body that
  drinks too much water is weaker and spalls in freeze-thaw. It is the
  headline property for classifying **tiles**.
- **Dimensional accuracy and warping** - matters for laying and joint
  width.
- **Abrasion (PEI) rating** - for floor tiles, resistance to foot traffic
  wear.

**Water absorption** classifies tiles into groups (ISO 13006 / NBR 13818):

```text
Water absorption test (boiling method)
--------------------------------------
Absorption (%) = ((wet mass - dry mass) / dry mass) x 100

  dry mass  (oven dried) ..... 2000 g
  wet mass  (after boil) ..... 2060 g
  absorption = (2060 - 2000) / 2000 x 100 = 3.0 %

Tile groups by absorption:
  BIa   <= 0.5 %   porcelain - very dense, exterior, wet areas
  BIb   0.5 - 3 %  low absorption
  BIIa  3 - 6 %    medium
  BIII  > 10 %     high - interior wall tile only
```

```mermaid
graph TD
    CLAY["Clay shaped and dried"] --> FIRE["Fired and sintered"]
    FIRE --> BRICK["Bricks and blocks"]
    FIRE --> TILE["Tiles"]
    BRICK --> STRENGTH["Compressive strength governs"]
    TILE --> ABS["Water absorption governs"]
    ABS --> PORC["Low absorption porcelain durable"]
    ABS --> WALL["High absorption interior only"]
```

Remember: for **structural ceramics** the governing property is
**compressive strength**; for **tiles** it is **water absorption** - the
denser the fired body, the more durable and weather-resistant it is.
""",
        ),
        quiz_lesson(
            "Quiz: Ceramic materials - bricks, blocks, tiles",
            (
                q(
                    "What does firing do to shaped clay?",
                    (
                        opt("Dissolves it in water"),
                        opt(
                            "Sinters the clay grains into a hard, durable, fire-resistant body",
                            correct=True,
                        ),
                        opt("Turns it back into soft mud"),
                        opt("Adds steel reinforcement"),
                    ),
                    "High-temperature firing drives off water and sinters the grains together.",
                ),
                q(
                    "Which property is the headline indicator for classifying tiles?",
                    (
                        opt("Colour"),
                        opt("Water absorption - it indicates density and durability", correct=True),
                        opt("Mass per unit"),
                        opt("Number of perforations"),
                    ),
                    "Lower absorption (e.g. BIa porcelain <= 0.5 percent) means a denser, "
                    "more weather-resistant tile.",
                ),
                q(
                    "What is the difference between a sealing block and a structural block?",
                    (
                        opt("The sealing block is fired, the structural block is not"),
                        opt(
                            "The sealing block is non-load-bearing; the structural block "
                            "carries load and needs higher strength",
                            correct=True,
                        ),
                        opt("They are identical"),
                        opt("The structural block is only for tiles"),
                    ),
                    "NBR 15270 sets higher minimum compressive strength for structural "
                    "(load-bearing) blocks.",
                ),
            ),
        ),
        # -- 6. Timber -------------------------------------------------
        _t(
            "Timber as a construction material",
            "10 min",
            """# Timber as a construction material

**Timber** is a natural, renewable structural material with an excellent
**strength-to-weight ratio**. Unlike steel or concrete it is
**anisotropic** - its properties depend on direction, because wood is a
bundle of fibres (cellulose tubes) aligned along the trunk.

That grain direction dominates everything:

- **Along the grain (parallel to fibres)** - strong in tension and
  compression; this is how you load a column or a beam's span.
- **Across the grain (perpendicular)** - much weaker; the fibres split
  and crush easily.

Timber is graded as **softwood** (conifers, e.g. pine - fast growing,
lighter) or **hardwood** (broadleaf, e.g. eucalyptus - denser, stronger).
Brazilian **NBR 7190** classifies structural species into strength classes
(the C classes for conifers, D classes for hardwoods).

The properties that control design and durability:

- **Moisture content** - the single most important variable. Green timber
  shrinks and warps as it dries; strength rises as moisture falls to the
  reference **12 percent**. Standards report strengths at 12 percent.
- **Density** - correlates strongly with strength and hardness.
- **Natural defects** - **knots**, splits and sloping grain reduce
  strength and must be limited by the grading rules.
- **Biological durability** - wood rots and is attacked by insects
  (termites, borers) and fungi; it needs **preservative treatment** (e.g.
  CCA) or naturally durable species for exterior use.

**Moisture content** is measured by oven-drying:

```text
Moisture content (oven-dry method, NBR 7190 / ASTM D4442)
---------------------------------------------------------
MC (%) = ((wet mass - oven dry mass) / oven dry mass) x 100

  wet mass (as received) .... 55.0 g
  oven-dry mass ............. 47.0 g
  MC = (55.0 - 47.0) / 47.0 x 100 = 17.0 %

Reference conditions:
  Fibre saturation point ~ 28 %  (above this, strength is minimum)
  Reference moisture     = 12 %  (strengths tabulated here)
  Green timber           > 30 %  (must be seasoned before use)
```

```mermaid
graph TD
    TREE["Timber natural fibres"] --> GRAIN["Anisotropic grain direction"]
    GRAIN --> PARA["Along grain strong"]
    GRAIN --> PERP["Across grain weak"]
    TREE --> MC["Moisture content key variable"]
    MC --> SEASON["Season to 12 percent"]
    TREE --> DUR["Durability"]
    DUR --> TREAT["Preservative treatment"]
```

Remember: timber is **anisotropic** - design along the grain - and its
strength and stability hinge on **moisture content**, so season it to the
reference 12 percent and protect it from decay.
""",
        ),
        quiz_lesson(
            "Quiz: Timber as a construction material",
            (
                q(
                    "What does 'anisotropic' mean for timber?",
                    (
                        opt("It has the same strength in every direction"),
                        opt(
                            "Its properties depend on direction - much stronger along "
                            "the grain than across it",
                            correct=True,
                        ),
                        opt("It cannot carry any load"),
                        opt("It contains no moisture"),
                    ),
                    "Wood is a bundle of aligned fibres, so it is strong along the grain "
                    "and weak across it.",
                ),
                q(
                    "Why is moisture content the most important variable for timber?",
                    (
                        opt("It changes the colour"),
                        opt(
                            "It drives shrinkage, warping and strength; standards report "
                            "strength at a reference 12 percent",
                            correct=True,
                        ),
                        opt("It has no effect on strength"),
                        opt("It only matters for hardwoods"),
                    ),
                    "Green timber shrinks and warps as it dries; strength rises as "
                    "moisture falls toward 12 percent.",
                ),
                q(
                    "How is timber protected for exterior use against rot and insects?",
                    (
                        opt("By painting it any colour"),
                        opt(
                            "With preservative treatment (e.g. CCA) or by using naturally "
                            "durable species",
                            correct=True,
                        ),
                        opt("By raising its moisture content"),
                        opt("By cutting it across the grain"),
                    ),
                    "Wood is biodegradable; treatment or a durable species is needed for "
                    "outdoor exposure.",
                ),
            ),
        ),
        # -- 7. Characterization tests ---------------------------------
        _t(
            "Material characterization tests",
            "11 min",
            """# Material characterization tests

Specifications are only meaningful if you can **measure** whether a
material meets them. Characterization tests are the shared laboratory
toolkit that turns "this looks strong" into a number with a standard
behind it. They fall into a few families.

**Mechanical tests** - how the material responds to load:

- **Compressive strength** - the defining test for concrete, mortar and
  masonry. Concrete is cast into standard **cylinders** (150 x 300 mm,
  NBR 5739 / ASTM C39) or cubes, cured, and crushed at **28 days**.
- **Tensile test** - pull a specimen to rupture; gives yield, ultimate
  strength and elongation for steel.
- **Flexural (bending) test** - a beam under load; used for concrete
  modulus of rupture and for timber.
- **Hardness / abrasion** - resistance to surface wear.

**Physical tests** - describe the material without breaking it by load:

- **Density and specific gravity**, **water absorption and voids**,
  **moisture content**, and **granulometry (sieve analysis)**.

**Non-destructive tests (NDT)** - assess a material in place without
damaging it: the **rebound hammer (esclerometro)** estimates surface
concrete strength, **ultrasonic pulse velocity** finds voids and cracks,
and **rebar locators** map reinforcement.

The headline example - **concrete compressive strength**:

```text
Concrete cylinder compressive strength (NBR 5739 / ASTM C39)
------------------------------------------------------------
fc = P / A          P = failure load, A = cross-section area

Standard cylinder: 150 mm diameter, 300 mm high, tested at 28 days
  area A = pi/4 * (150 mm)^2 = 17,671 mm^2
  failure load P = 530,000 N
  fc = 530,000 / 17,671 = 30.0 MPa   ->  a C30 concrete

Acceptance uses the characteristic strength fck (the 5% fractile),
estimated from the test batch:  fck ~ fcm - 1.65 * s   (s = std dev)
```

```mermaid
graph TD
    SPEC["Material specimen"] --> MECH["Mechanical tests"]
    SPEC --> PHYS["Physical tests"]
    SPEC --> NDT["Non destructive tests"]
    MECH --> COMP["Compression cylinders"]
    MECH --> TENS["Tension steel bars"]
    PHYS --> ABS["Absorption and density"]
    NDT --> HAMMER["Rebound hammer in place"]
    COMP --> FC["Characteristic strength fck"]
```

Remember: every spec value points to a **standard test**. Concrete is
judged by **28-day compressive strength on standard cylinders**, and
acceptance is based on the **characteristic strength (fck)**, not a single
lucky specimen.
""",
        ),
        quiz_lesson(
            "Quiz: Material characterization tests",
            (
                q(
                    "How is concrete compressive strength normally determined?",
                    (
                        opt("By eye, from the colour of the surface"),
                        opt(
                            "By crushing standard cured cylinders (or cubes) at 28 days "
                            "and dividing failure load by area",
                            correct=True,
                        ),
                        opt("By weighing the fresh concrete"),
                        opt("By measuring the slump only"),
                    ),
                    "NBR 5739 / ASTM C39: fc = P / A on standard specimens at 28 days.",
                ),
                q(
                    "What is a non-destructive test (NDT), and give an example.",
                    (
                        opt("A test that always breaks the specimen; the tensile test"),
                        opt(
                            "A test that assesses the material in place without damaging "
                            "it; the rebound hammer or ultrasonic pulse velocity",
                            correct=True,
                        ),
                        opt("A test done only in a furnace; firing bricks"),
                        opt("A test of moisture content only; oven drying"),
                    ),
                    "NDT (rebound hammer, ultrasonic pulse, rebar locator) evaluates the "
                    "material without destroying it.",
                ),
                q(
                    "Why is acceptance based on the characteristic strength (fck) rather "
                    "than one specimen?",
                    (
                        opt("Because fck is always the highest single result"),
                        opt(
                            "Because it accounts for scatter - it is a low fractile "
                            "estimated from the batch mean and standard deviation",
                            correct=True,
                        ),
                        opt("Because a single specimen is illegal"),
                        opt("Because fck ignores the test results"),
                    ),
                    "fck is roughly fcm - 1.65 s, the 5 percent fractile, so it reflects "
                    "the real variability of the material.",
                ),
            ),
        ),
        # -- 8. Standardization and quality control --------------------
        _t(
            "Standardization and quality control",
            "10 min",
            """# Standardization and quality control

A test result means nothing without a **standard** to compare it to.
**Standardization** defines *how* to test, *what* the limits are, and *how*
to decide acceptance - so that "C30 concrete" or "CA-50 steel" means the
same thing to the supplier, the engineer and the inspector.

The main standards bodies you will meet:

- **ABNT / NBR** - the Brazilian standards (Associacao Brasileira de
  Normas Tecnicas). NBR 6118 (concrete structures), NBR 7480 (rebar), NBR
  15270 (ceramic blocks), NBR 7190 (timber).
- **ASTM** - the widely used US standards (e.g. C39 concrete, A615 rebar,
  C270 mortar).
- **ISO** and **EN (Eurocode)** - international and European standards.

**Quality control (QC)** is the on-the-ground activity of keeping the real
material within those limits. It runs across three phases:

- **Reception (incoming)** - inspect and test materials as they arrive;
  reject non-conforming lots (a cement past its shelf life, out-of-grade
  sand).
- **Process** - control the work as it happens: mix proportions, the
  concrete **slump test** for workability, curing, molding test specimens.
- **Acceptance** - test hardened specimens against the spec and apply a
  **statistical acceptance criterion**, because materials naturally vary.

Acceptance is **statistical**, not pass-on-one-sample:

```text
Statistical acceptance of concrete (NBR 12655)
----------------------------------------------
Sample the batch, cast n cylinders, test at 28 days, then:

  mean strength     fcm = average of the n results
  standard dev      s   = scatter of the results
  characteristic    fck,est = fcm - 1.65 * s   (5% fractile)

Accept the lot only if:   fck,est  >=  fck,specified

Example: specified fck = 25 MPa
  results give fcm = 31 MPa, s = 3 MPa
  fck,est = 31 - 1.65 * 3 = 26.05 MPa  >=  25 MPa   ->  ACCEPT
```

```mermaid
graph TD
    STD["Standards ABNT NBR ASTM ISO"] --> LIMITS["Define tests and limits"]
    LIMITS --> QC["Quality control on site"]
    QC --> RECV["Reception inspect incoming"]
    QC --> PROC["Process slump and curing"]
    QC --> ACC["Acceptance test specimens"]
    ACC --> STAT["Statistical criterion fck"]
    STAT --> DECIDE["Accept or reject the lot"]
```

Remember: standards make a spec **objective and shared**, and quality
control - reception, process, and **statistical acceptance** - keeps the
delivered material inside those limits despite natural variation.
""",
        ),
        quiz_lesson(
            "Quiz: Standardization and quality control",
            (
                q(
                    "What is the role of a standards body like ABNT or ASTM?",
                    (
                        opt("To sell the construction materials"),
                        opt(
                            "To define how to test, what the limits are, and how to "
                            "decide acceptance, so a spec means the same to everyone",
                            correct=True,
                        ),
                        opt("To build the structures directly"),
                        opt("To replace the need for testing"),
                    ),
                    "Standards make 'C30 concrete' or 'CA-50 steel' objective and shared "
                    "across supplier, engineer and inspector.",
                ),
                q(
                    "Which are the three phases of quality control described here?",
                    (
                        opt("Design, drawing, billing"),
                        opt("Reception, process, and acceptance", correct=True),
                        opt("Excavation, foundation, roofing"),
                        opt("Tension, compression, bending"),
                    ),
                    "Inspect incoming materials, control the process (slump, curing), and "
                    "test specimens for acceptance.",
                ),
                q(
                    "Why is concrete acceptance based on a statistical criterion?",
                    (
                        opt("To make the paperwork longer"),
                        opt(
                            "Because materials naturally vary, so acceptance uses the "
                            "mean and scatter to estimate the characteristic strength",
                            correct=True,
                        ),
                        opt("Because only one cylinder is ever cast"),
                        opt("Because standards forbid testing"),
                    ),
                    "fck,est = fcm - 1.65 s accounts for real batch variability rather "
                    "than one lucky or unlucky specimen.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "About what fraction of concrete's volume is aggregate?",
                    (
                        opt("About 10 percent"),
                        opt("About 70 percent", correct=True),
                        opt("About 95 percent"),
                        opt("Aggregate is not used in concrete"),
                    ),
                    "Aggregates make up roughly 70 percent of the volume and carry much "
                    "of the load.",
                ),
                q(
                    "A higher fineness modulus means the sand is...",
                    (
                        opt("finer"),
                        opt("coarser", correct=True),
                        opt("cleaner"),
                        opt("more absorbent"),
                    ),
                    "FM is the summed cumulative percentages retained over 100; higher = coarser.",
                ),
                q(
                    "Which binder is hydraulic (hardens under water)?",
                    (
                        opt("Air lime"),
                        opt("Gypsum plaster"),
                        opt("Portland cement", correct=True),
                        opt("None of them harden with water"),
                    ),
                    "Portland cement hydrates and hardens even submerged; air lime "
                    "carbonates and gypsum is an interior material.",
                ),
                q(
                    "Air lime hardens by which mechanism?",
                    (
                        opt("Hydration with water"),
                        opt("Carbonation - reabsorbing CO2 from the air", correct=True),
                        opt("Melting"),
                        opt("Electrolysis"),
                    ),
                    "Air lime needs air to carbonate; it does not set under water.",
                ),
                q(
                    "What mainly distinguishes a mortar from concrete?",
                    (
                        opt("Mortar has no binder"),
                        opt("Mortar has no coarse aggregate", correct=True),
                        opt("Mortar has no water"),
                        opt("Mortar is always cement-only"),
                    ),
                    "No gravel is what lets mortar be spread in thin, worked layers.",
                ),
                q(
                    "For a CA-50 reinforcing bar, what is the yield strength fy?",
                    (
                        opt("250 MPa"),
                        opt("500 MPa", correct=True),
                        opt("50 MPa"),
                        opt("600 MPa"),
                    ),
                    "CA-50 (NBR 7480) is the standard ribbed bar at fy = 500 MPa.",
                ),
                q(
                    "Why do reinforcing bars have ribs (deformations)?",
                    (
                        opt("For decoration"),
                        opt("To create mechanical bond with the concrete", correct=True),
                        opt("To make them lighter"),
                        opt("To increase the modulus of elasticity"),
                    ),
                    "Ribs let bar and concrete act together; smooth bars rely on friction only.",
                ),
                q(
                    "For ceramic tiles, which property is the headline classifier?",
                    (
                        opt("Compressive strength"),
                        opt("Water absorption", correct=True),
                        opt("Colour"),
                        opt("Firing time"),
                    ),
                    "Lower absorption (e.g. BIa porcelain) means a denser, more durable "
                    "tile; for structural blocks strength governs instead.",
                ),
                q(
                    "Timber is described as anisotropic because...",
                    (
                        opt("it has no moisture"),
                        opt(
                            "its strength depends on direction - much stronger along the "
                            "grain than across it",
                            correct=True,
                        ),
                        opt("it is equally strong in all directions"),
                        opt("it cannot carry load"),
                    ),
                    "Wood is aligned fibres; design along the grain, season to 12 percent "
                    "moisture.",
                ),
                q(
                    "How is concrete finally accepted on site?",
                    (
                        opt("If a single cylinder passes"),
                        opt(
                            "By a statistical criterion - the characteristic strength "
                            "fck,est from the batch must meet the specified fck",
                            correct=True,
                        ),
                        opt("By the colour of the hardened surface"),
                        opt("By weighing the truck"),
                    ),
                    "fck,est = fcm - 1.65 s must be at least the specified fck, "
                    "accounting for natural variation (NBR 12655).",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CONSTRUCTION_MATERIALS_COURSES: tuple[SeedCourse, ...] = (_CONSTRUCTION_MATERIALS,)
