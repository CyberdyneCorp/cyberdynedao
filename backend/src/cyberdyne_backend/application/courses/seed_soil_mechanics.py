"""Academy seed content - Soil Mechanics.

The mechanical behavior of soils, the foundation of geotechnical
engineering: how soils form, the three-phase system and index properties,
grain-size and Atterberg limits, classification (USCS/SUCS and ABNT),
compaction, permeability and seepage, stresses and the effective stress
principle, shear strength (Mohr-Coulomb), and consolidation and
settlement. Every lesson is a direct explanation with a worked phase
diagram, formula or calculation and a mermaid diagram, followed by a
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


_SOIL_MECHANICS = SeedCourse(
    slug="soil-mechanics",
    title="Soil Mechanics",
    description=(
        "The mechanical behavior of soils - index properties, "
        "classification, compaction, seepage, stress, strength and "
        "consolidation - the foundation of geotechnical engineering. Every "
        "lesson is a direct explanation with a worked phase diagram or "
        "formula and a diagram, grounded in real practice (ABNT NBR, "
        "SUCS/USCS, Darcy, Terzaghi, Mohr-Coulomb)."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Soil Mechanics

Soil is the material we build on and build with, yet it is neither a solid
nor a fluid - it is a **three-phase** mixture of solid grains, water and
air whose behavior depends on how those phases are arranged. Soil
mechanics is the discipline that turns that messy reality into numbers an
engineer can design with: how much a foundation will settle, whether a
slope will slide, how fast water seeps through a dam.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in a worked phase diagram, formula or short
calculation, and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Origin, phases and index properties** - the three-phase model
2. **Grain size and Atterberg limits** - describing the grains and the fines
3. **Classification** - USCS/SUCS and ABNT systems
4. **Compaction** - the Proctor test and field control
5. **Permeability and seepage** - Darcy's law and flow through soil
6. **Stresses and effective stress** - Terzaghi's central principle
7. **Shear strength** - the Mohr-Coulomb failure criterion
8. **Consolidation and settlement** - how saturated clays deform over time

This is the backbone of geotechnical engineering. Foundations, retaining
walls, embankments, dams and slopes all rest on these eight ideas - master
the fundamentals here and the applied courses become far easier.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Why is soil described as a three-phase material?",
                    (
                        opt("Because it always has three layers"),
                        opt(
                            "Because it is a mixture of solid grains, water and air, "
                            "and its behavior depends on how those phases are arranged",
                            correct=True,
                        ),
                        opt("Because it is tested at three temperatures"),
                        opt("Because it has three chemical elements"),
                    ),
                    "Solids, water and air together make up soil; the proportions and "
                    "arrangement govern its mechanical behavior.",
                ),
                q(
                    "What does this course prepare you for?",
                    (
                        opt("Only laboratory chemistry"),
                        opt(
                            "The fundamentals behind foundations, slopes, embankments "
                            "and dams - the core of geotechnical engineering",
                            correct=True,
                        ),
                        opt("Structural steel design only"),
                        opt("Electrical grounding systems"),
                    ),
                    "Index properties, classification, compaction, seepage, stress, "
                    "strength and consolidation underpin all geotechnical design.",
                ),
            ),
        ),
        # -- 1. Origin, phases, index properties -----------------------
        _t(
            "Soil origin, three-phase system and index properties",
            "11 min",
            """# Soil origin, three-phase system and index properties

Soil is the product of **weathering** - the physical and chemical
breakdown of rock. **Residual** soils stay where the parent rock decayed;
**transported** soils are moved and deposited by water (alluvial),
wind (aeolian), ice (glacial) or gravity (colluvial). Origin controls
grain shape, mineralogy and structure, which is why geology matters to the
geotechnical engineer.

A soil element is a **three-phase system**. We split it into a **phase
diagram** by volume (V) on the left and mass (M) on the right:

```text
        VOLUME                        MASS
   +----------------+            +----------------+
   |     Air   Va   |            |    Air ~ 0     |
   +----------------+  Vv        +----------------+
   |    Water  Vw   |            |   Water   Mw   |
   +================+            +================+
   |               |            |               |
   |  Solids  Vs   |            |  Solids   Ms  |
   +----------------+            +----------------+

Vv = Va + Vw   (void volume)
V  = Vs + Vw + Va      M = Ms + Mw
```

From this diagram come the **index properties** - the ratios that
describe the state of the soil:

```text
Void ratio        e = Vv / Vs
Porosity          n = Vv / V           n = e / (1 + e)
Water content     w = Mw / Ms          (as a decimal or percent)
Degree of satur.  S = Vw / Vv          (S = 1 fully saturated)
Bulk unit weight  gamma   = M g / V
Specific gravity  Gs = rho_s / rho_water   (quartz ~ 2.65)

A key identity:   S * e = w * Gs
```

Worked example - a saturated clay sample: w = 0.40, Gs = 2.70, S = 1.

```text
S * e = w * Gs   ->   1 * e = 0.40 * 2.70   ->   e = 1.08
Porosity  n = e / (1 + e) = 1.08 / 2.08 = 0.519  (about 52 percent voids)
```

```mermaid
graph TD
    SOIL["Soil element"] --> SOLID["Solid grains"]
    SOIL --> VOID["Voids"]
    VOID --> WATER["Water"]
    VOID --> AIR["Air"]
    SOLID --> E["Void ratio e equals Vv over Vs"]
    WATER --> W["Water content w equals Mw over Ms"]
    WATER --> S["Saturation S equals Vw over Vv"]
```

Remember: nearly every soil-mechanics calculation starts by drawing the
phase diagram and reading off the index properties.
""",
        ),
        quiz_lesson(
            "Quiz: Soil origin, three-phase system and index properties",
            (
                q(
                    "What is the difference between residual and transported soils?",
                    (
                        opt("Residual soils are always sandy"),
                        opt(
                            "Residual soils remain over the parent rock that weathered; "
                            "transported soils were moved and deposited by water, wind, "
                            "ice or gravity",
                            correct=True,
                        ),
                        opt("Transported soils never contain clay"),
                        opt("There is no real difference"),
                    ),
                    "Origin controls grain shape, mineralogy and structure, so it "
                    "matters to geotechnical behavior.",
                ),
                q(
                    "Void ratio e is defined as which ratio?",
                    (
                        opt("Volume of voids to total volume"),
                        opt("Volume of voids to volume of solids", correct=True),
                        opt("Mass of water to mass of solids"),
                        opt("Volume of water to volume of voids"),
                    ),
                    "e = Vv / Vs. Porosity n = Vv / V is the voids-to-total ratio; the "
                    "two relate by n = e / (1 + e).",
                ),
                q(
                    "For a saturated soil (S = 1), the identity S*e = w*Gs reduces to?",
                    (
                        opt("e = w * Gs", correct=True),
                        opt("e = w / Gs"),
                        opt("w = e * Gs"),
                        opt("Gs = w * e"),
                    ),
                    "With S = 1, e = w * Gs - a fast way to get void ratio from water "
                    "content and specific gravity for saturated soils.",
                ),
            ),
        ),
        # -- 2. Grain size and Atterberg -------------------------------
        _t(
            "Grain-size distribution and Atterberg limits",
            "11 min",
            """# Grain-size distribution and Atterberg limits

Two families of tests describe a soil's grains: **grain-size
distribution** for the coarse fraction and the **Atterberg limits** for
the fine (clay and silt) fraction.

**Grain-size distribution** is found by **sieving** the coarse grains and,
for particles finer than the No. 200 sieve (0.075 mm), by
**sedimentation** (hydrometer). The result is a curve of percent passing
against grain diameter on a log scale. From it we read characteristic
diameters and two shape coefficients:

```text
D10 = diameter at 10 percent passing  (the "effective size")
D30 = diameter at 30 percent passing
D60 = diameter at 60 percent passing

Coefficient of uniformity   Cu = D60 / D10
Coefficient of curvature     Cc = (D30)^2 / (D10 * D60)

Well graded gravel: Cu > 4  and  1 <= Cc <= 3
Well graded sand:   Cu > 6  and  1 <= Cc <= 3
A high Cu means a wide range of sizes (well graded);
Cu near 1 means one size dominates (poorly graded, uniform).
```

The **Atterberg limits** capture how fine-grained soil changes state with
water content. As water is added, a clay passes solid -> semisolid ->
plastic -> liquid. The boundaries are:

- **Shrinkage limit (SL)** - below it, drying no longer shrinks the soil.
- **Plastic limit (PL)** - the water content where the soil starts to
  crumble when rolled into a 3 mm thread.
- **Liquid limit (LL)** - the water content at which it begins to flow
  (Casagrande cup or fall cone).

The single most useful derived number is the **plasticity index**:

```text
Plasticity Index   PI = LL - PL
Liquidity Index    LI = (w - PL) / PI

Worked example:  LL = 52,  PL = 24,  in-situ w = 31
PI = 52 - 24 = 28   (a highly plastic clay, CH)
LI = (31 - 24) / 28 = 0.25   (stiff, closer to the plastic limit)
```

```mermaid
graph LR
    SOIL["Soil sample"] --> COARSE["Coarse fraction"]
    SOIL --> FINE["Fine fraction"]
    COARSE --> SIEVE["Sieve analysis Cu and Cc"]
    FINE --> ATT["Atterberg limits"]
    ATT --> LL["Liquid limit"]
    ATT --> PL["Plastic limit"]
    LL --> PI["Plasticity index PI equals LL minus PL"]
    PL --> PI
```

Remember: sieve/hydrometer describe the *grains*; Atterberg limits describe
how the *fines* behave with water. Together they feed the classification.
""",
        ),
        quiz_lesson(
            "Quiz: Grain-size distribution and Atterberg limits",
            (
                q(
                    "The coefficient of uniformity Cu = D60 / D10 tells you what?",
                    (
                        opt("The soil's water content"),
                        opt(
                            "How wide the range of grain sizes is - a high Cu means "
                            "well graded, a value near 1 means uniform (poorly graded)",
                            correct=True,
                        ),
                        opt("The plasticity of the fines"),
                        opt("The soil's unit weight"),
                    ),
                    "Cu spreads the sizes; Cc = D30^2 / (D10*D60) checks the curve's "
                    "shape. Both come from the grain-size distribution.",
                ),
                q(
                    "How is the plasticity index defined?",
                    (
                        opt("PI = LL + PL"),
                        opt("PI = LL - PL", correct=True),
                        opt("PI = PL - SL"),
                        opt("PI = w - LL"),
                    ),
                    "PI = LL - PL is the range of water content over which the soil is "
                    "plastic; a large PI indicates a highly plastic clay.",
                ),
                q(
                    "Which test is used for particles finer than the No. 200 sieve (0.075 mm)?",
                    (
                        opt("Coarse sieving only"),
                        opt("Sedimentation / hydrometer analysis", correct=True),
                        opt("The Proctor compaction test"),
                        opt("The Casagrande liquid-limit cup"),
                    ),
                    "Sieves handle the coarse fraction; the hydrometer (sedimentation) "
                    "measures the silt and clay sizes below 0.075 mm.",
                ),
            ),
        ),
        # -- 3. Classification -----------------------------------------
        _t(
            "Soil classification (USCS/SUCS, ABNT)",
            "11 min",
            """# Soil classification (USCS/SUCS, ABNT)

Classification puts a soil in a named group so engineers share a common
language and can anticipate behavior. The dominant system is the **Unified
Soil Classification System (USCS)**, known in Brazil as **SUCS** and
standardized for laboratory identification in **ABNT NBR 6502 / NBR 7181**.

The first split uses the **No. 200 sieve (0.075 mm)**:

- If **less than 50 percent passes** No. 200, the soil is **coarse
  grained** (gravel G or sand S). Judge it by grain-size shape:
  well graded (W) or poorly graded (P) using Cu and Cc.
- If **50 percent or more passes** No. 200, the soil is **fine grained**
  (silt M or clay C), and you judge it on the **plasticity chart** using
  LL and PI.

The USCS uses a **two-letter symbol**: a prefix for the dominant type and
a suffix for the grading or plasticity.

```text
Prefix              Suffix
  G  gravel           W  well graded
  S  sand             P  poorly graded
  M  silt             M  silty fines
  C  clay             C  clayey fines
  O  organic          L  low plasticity  (LL < 50)
  Pt peat             H  high plasticity  (LL >= 50)

Examples:  SW  well graded sand
           GP  poorly graded gravel
           CL  low-plasticity clay      CH  high-plasticity clay
           ML  low-plasticity silt      MH  high-plasticity silt
```

The **plasticity chart** separates clays from silts with the **A-line**:

```text
A-line:   PI = 0.73 * (LL - 20)

Worked example:  LL = 52,  PI = 28
A-line PI at LL = 52:  0.73 * (52 - 20) = 0.73 * 32 = 23.4
Measured PI = 28 > 23.4  ->  plots ABOVE the A-line  ->  clay (C)
LL = 52 >= 50  ->  high plasticity (H)   =>   group symbol CH
```

```mermaid
graph TD
    SOIL["Soil sample"] --> SIEVE["Percent passing No 200"]
    SIEVE -->|"less than 50"| COARSE["Coarse grained G or S"]
    SIEVE -->|"50 or more"| FINE["Fine grained M or C"]
    COARSE --> GRAD["Grading Cu and Cc gives W or P"]
    FINE --> CHART["Plasticity chart A line"]
    CHART --> ABOVE["Above A line clay C"]
    CHART --> BELOW["Below A line silt M"]
```

Remember: coarse soils are classified by *grain size*, fine soils by
*plasticity*. The A-line and the LL = 50 boundary place the fines on the
chart, and NBR 6502 gives the Brazilian terminology.
""",
        ),
        quiz_lesson(
            "Quiz: Soil classification (USCS/SUCS, ABNT)",
            (
                q(
                    "What separates coarse-grained from fine-grained soils in USCS/SUCS?",
                    (
                        opt("Whether the soil is wet or dry"),
                        opt(
                            "Whether less than 50 percent, or 50 percent or more, passes "
                            "the No. 200 sieve (0.075 mm)",
                            correct=True,
                        ),
                        opt("Its color"),
                        opt("Its specific gravity"),
                    ),
                    "The No. 200 sieve is the coarse/fine boundary; coarse soils are "
                    "judged by grading, fine soils by plasticity.",
                ),
                q(
                    "The suffix H in a group symbol such as CH or MH means what?",
                    (
                        opt("Well graded"),
                        opt("High plasticity, with LL greater than or equal to 50", correct=True),
                        opt("High permeability"),
                        opt("Homogeneous"),
                    ),
                    "L = low plasticity (LL < 50), H = high plasticity (LL >= 50); the "
                    "prefix C or M tells clay from silt.",
                ),
                q(
                    "A fine soil plots above the A-line on the plasticity chart. It is?",
                    (
                        opt("A silt"),
                        opt("A clay", correct=True),
                        opt("A gravel"),
                        opt("Organic peat"),
                    ),
                    "Above the A-line (PI = 0.73*(LL - 20)) means clay (C); below it "
                    "means silt (M).",
                ),
            ),
        ),
        # -- 4. Compaction ---------------------------------------------
        _t(
            "Compaction (Proctor)",
            "10 min",
            """# Compaction (Proctor)

**Compaction** is the *mechanical* densification of soil by expelling
**air** from the voids - not water. Denser soil means higher strength,
lower permeability and less future settlement, so nearly every
embankment, road subgrade and earth dam is compacted and controlled.

The reference test is the **Proctor test** (ABNT NBR 7182; standard and
modified energies). Soil is compacted in a mould at several water contents,
and for each we compute the **dry unit weight**:

```text
Dry unit weight   gamma_d = gamma / (1 + w)

  gamma = bulk (moist) unit weight = W / V
  w     = water content (decimal)
```

Plot gamma_d against w and you get the **compaction curve**, a hump:

- Too dry: grains resist rearrangement, low density.
- Adding water lubricates the grains, density rises to a **peak**.
- Past the peak, water starts filling voids that soil should occupy,
  pushing grains apart, and density falls.

The peak defines two design targets:

```text
Maximum dry unit weight   gamma_d,max   (top of the curve)
Optimum moisture content  OMC = w at the peak

Above the curve is the "zero air voids" line (S = 1):
   gamma_d,zav = (Gs * gamma_w) / (1 + w * Gs)
No real compaction curve can cross it - you cannot remove all air.
```

Field control compares the site to the lab peak using **relative
compaction**:

```text
Relative compaction  RC = gamma_d,field / gamma_d,max  * 100 percent
Typical spec:  RC >= 95 percent  of the modified Proctor maximum,
               placed near OMC.

Worked example:  gamma_d,max = 18.5 kN/m3,  field gamma_d = 17.8 kN/m3
RC = 17.8 / 18.5 * 100 = 96.2 percent   ->  passes a 95 percent spec.
```

```mermaid
graph TD
    TEST["Proctor test"] --> POINTS["Compact at several water contents"]
    POINTS --> GD["Compute dry unit weight each point"]
    GD --> CURVE["Plot compaction curve"]
    CURVE --> PEAK["Peak gives gamma d max and OMC"]
    PEAK --> FIELD["Field control"]
    FIELD --> RC["Relative compaction versus spec"]
```

Remember: compaction removes air, not water; the Proctor peak sets the
target dry density and the optimum moisture, and the field is checked
against it with relative compaction.
""",
        ),
        quiz_lesson(
            "Quiz: Compaction (Proctor)",
            (
                q(
                    "What does compaction primarily remove from the soil?",
                    (
                        opt("Water"),
                        opt("Air from the voids", correct=True),
                        opt("Clay minerals"),
                        opt("Dissolved salts"),
                    ),
                    "Compaction expels air to densify the soil; it is distinct from "
                    "consolidation, which slowly drives out water.",
                ),
                q(
                    "What do the two design targets from the Proctor curve represent?",
                    (
                        opt("The minimum strength and maximum cost"),
                        opt(
                            "The maximum dry unit weight and the optimum moisture "
                            "content at the peak of the compaction curve",
                            correct=True,
                        ),
                        opt("The liquid and plastic limits"),
                        opt("Cu and Cc"),
                    ),
                    "gamma_d,max and OMC define the field target: compact near OMC to "
                    "reach the specified fraction of gamma_d,max.",
                ),
                q(
                    "If the lab maximum dry unit weight is 18.5 kN/m3 and the field "
                    "value is 17.8 kN/m3, the relative compaction is about?",
                    (
                        opt("104 percent"),
                        opt("96 percent", correct=True),
                        opt("88 percent"),
                        opt("70 percent"),
                    ),
                    "RC = 17.8 / 18.5 * 100 = 96.2 percent - it passes a typical 95 "
                    "percent specification.",
                ),
            ),
        ),
        # -- 5. Permeability and seepage -------------------------------
        _t(
            "Permeability and seepage (Darcy)",
            "11 min",
            """# Permeability and seepage (Darcy)

Water moves through the connected voids of soil, and how fast it moves
governs seepage under dams, drawdown of the water table, and the time
clays take to consolidate. The governing law is **Darcy's law**, valid for
the slow (laminar) flow typical of soils:

```text
Darcy's law     v = k * i          Q = k * i * A

  v = discharge velocity (flow per unit total area)
  k = coefficient of permeability (hydraulic conductivity), units m/s
  i = hydraulic gradient = head loss / flow length = dh / L
  A = total cross-sectional area
  Q = volumetric flow rate

Seepage velocity (through the voids only):  vs = v / n
```

The permeability **k** spans an enormous range with grain size - it is the
single most variable soil property:

```text
Clean gravel     k ~ 1e-1  to 1e-2  m/s
Clean sand       k ~ 1e-3  to 1e-5  m/s
Silt             k ~ 1e-6  to 1e-8  m/s
Clay             k ~ 1e-9  to 1e-11 m/s   (nearly impervious)
```

Worked example - flow under a sheet pile in sand:

```text
Given:  k = 2e-4 m/s,  head loss dh = 3 m across flow length L = 12 m,
        cross-section A = 8 m2
i = dh / L = 3 / 12 = 0.25
v = k * i = 2e-4 * 0.25 = 5e-5 m/s
Q = v * A = 5e-5 * 8 = 4e-4 m3/s = 0.4 litre/s
```

When a **rising** upward gradient in sand reduces effective stress to
zero, grains lose contact and the soil "boils" - the **critical hydraulic
gradient**:

```text
Critical gradient   i_cr = (Gs - 1) / (1 + e) = gamma_sub / gamma_w
For a typical sand (Gs = 2.65, e = 0.65):
i_cr = (2.65 - 1) / (1 + 0.65) = 1.65 / 1.65 = 1.0
```

If the actual upward gradient approaches i_cr, **quicksand / piping**
threatens - a key check for cofferdams and dam foundations.

```mermaid
graph LR
    HEAD["Head difference dh"] --> GRAD["Gradient i equals dh over L"]
    GRAD --> DARCY["Darcy law v equals k times i"]
    DARCY --> FLOW["Flow rate Q equals v times A"]
    GRAD --> UP["Upward gradient in sand"]
    UP --> CRIT["Compare with critical gradient"]
    CRIT --> BOIL["Piping or quicksand risk"]
```

Remember: Darcy's law (v = k*i) governs seepage; k varies by orders of
magnitude with grain size; and an upward gradient near i_cr can liquefy
sand.
""",
        ),
        quiz_lesson(
            "Quiz: Permeability and seepage (Darcy)",
            (
                q(
                    "Darcy's law states that the discharge velocity in soil is?",
                    (
                        opt("v = k / i"),
                        opt(
                            "v = k * i, with k the permeability and i the hydraulic gradient",
                            correct=True,
                        ),
                        opt("v = i / k"),
                        opt("v = k * A only"),
                    ),
                    "v = k*i (and Q = k*i*A). The gradient i = head loss / flow length "
                    "drives the flow.",
                ),
                q(
                    "How does the permeability k of clay compare with that of clean sand?",
                    (
                        opt("Clay is far more permeable than sand"),
                        opt(
                            "Clay is many orders of magnitude less permeable - it is "
                            "nearly impervious compared with sand",
                            correct=True,
                        ),
                        opt("They are essentially equal"),
                        opt("Permeability does not depend on grain size"),
                    ),
                    "k drops from ~1e-3 m/s in clean sand to ~1e-9 m/s or less in clay; "
                    "grain size is the dominant control.",
                ),
                q(
                    "What happens when an upward hydraulic gradient reaches the critical "
                    "gradient i_cr in sand?",
                    (
                        opt("The sand becomes stronger"),
                        opt(
                            "Effective stress falls to zero and the sand boils - "
                            "quicksand or piping",
                            correct=True,
                        ),
                        opt("Permeability drops to zero"),
                        opt("The water table rises permanently"),
                    ),
                    "i_cr = (Gs - 1)/(1 + e) ~ 1; at that gradient grain contact is "
                    "lost and the sand loses all strength.",
                ),
            ),
        ),
        # -- 6. Stresses and effective stress --------------------------
        _t(
            "Stresses in soil and effective stress principle",
            "11 min",
            """# Stresses in soil and effective stress principle

The single most important idea in soil mechanics is **Terzaghi's
principle of effective stress**. The total stress at a depth is carried by
two things: the **soil skeleton** (grain-to-grain contact) and the **pore
water**. Only the part carried by the skeleton controls strength and
deformation.

```text
Effective stress principle
   sigma' = sigma - u

   sigma  = total vertical stress  (weight of everything above)
   u      = pore water pressure    (u = gamma_w * hw below the water table)
   sigma' = effective vertical stress  (carried by the grain skeleton)
```

Total stress is the accumulated weight of the overlying soil columns:

```text
sigma = sum( gamma_i * h_i )     (sum layer unit weight times thickness)
Above the water table use moist gamma; below, use saturated gamma_sat.
Pore pressure     u = gamma_w * (depth below water table),  gamma_w = 9.81 kN/m3
```

Worked example - a point 6 m deep, water table at the surface, saturated
sand gamma_sat = 20 kN/m3:

```text
sigma  = gamma_sat * z          = 20 * 6      = 120 kPa
u      = gamma_w * z             = 9.81 * 6    = 58.9 kPa
sigma' = sigma - u              = 120 - 58.9  = 61.1 kPa
```

Why it matters: raise the water table (u up) and sigma' falls - the soil
effectively weakens even though nothing was excavated. Pump the water down
(u falls) and sigma' rises, which is why over-pumping an aquifer causes
ground **subsidence**. Every strength and settlement calculation that
follows uses sigma', not sigma.

```mermaid
graph TD
    TOTAL["Total stress sigma"] --> SKEL["Carried by soil skeleton"]
    TOTAL --> PORE["Carried by pore water u"]
    SKEL --> EFF["Effective stress sigma prime"]
    PORE --> EFF
    EFF --> STRENGTH["Controls shear strength"]
    EFF --> SETTLE["Controls settlement"]
```

Remember: sigma' = sigma - u. Strength and settlement respond only to
effective stress, so tracking the pore pressure is everything.
""",
        ),
        quiz_lesson(
            "Quiz: Stresses in soil and effective stress principle",
            (
                q(
                    "Terzaghi's effective stress principle is written as?",
                    (
                        opt("sigma' = sigma + u"),
                        opt("sigma' = sigma - u, where u is the pore water pressure", correct=True),
                        opt("sigma' = u - sigma"),
                        opt("sigma' = sigma * u"),
                    ),
                    "Effective stress = total stress minus pore pressure. Only sigma' "
                    "governs strength and deformation.",
                ),
                q(
                    "At 6 m depth in saturated sand (gamma_sat = 20 kN/m3) with the water "
                    "table at the surface, the effective vertical stress is about?",
                    (
                        opt("120 kPa"),
                        opt("61 kPa", correct=True),
                        opt("59 kPa"),
                        opt("0 kPa"),
                    ),
                    "sigma = 120 kPa, u = 9.81*6 = 58.9 kPa, so sigma' = 120 - 58.9 = 61.1 kPa.",
                ),
                q(
                    "Why does over-pumping groundwater cause ground subsidence?",
                    (
                        opt("It adds weight to the soil"),
                        opt(
                            "Lowering the water table reduces pore pressure u, which "
                            "raises effective stress sigma' and compresses the soil",
                            correct=True,
                        ),
                        opt("It dissolves the soil grains"),
                        opt("It increases permeability"),
                    ),
                    "Less u means more sigma' on the skeleton; the increased effective "
                    "stress compresses the soil and the ground settles.",
                ),
            ),
        ),
        # -- 7. Shear strength -----------------------------------------
        _t(
            "Shear strength (Mohr-Coulomb)",
            "11 min",
            """# Shear strength (Mohr-Coulomb)

A soil fails not by crushing but by **shearing** - grains slide over one
another along a surface. The **Mohr-Coulomb failure criterion** gives the
shear strength available on any plane as a straight line in terms of
**effective** stress:

```text
Mohr-Coulomb (effective stress)
   tau_f = c' + sigma_n' * tan(phi')

   tau_f    = shear strength on the failure plane
   c'       = effective cohesion (intercept)
   phi'     = effective friction angle (slope of the line)
   sigma_n' = effective normal stress on the plane
```

The two parameters have physical meaning:

- **Friction angle phi'** - the frictional, interlocking resistance
  between grains. It dominates in **sands** (clean sand: c' ~ 0, phi' ~ 30
  to 40 degrees). More normal stress means more strength.
- **Cohesion c'** - a strength that exists at zero normal stress, from
  bonding and cementation in **clays**. A saturated clay loaded fast
  behaves as **undrained** with phi = 0 and strength su (the undrained
  shear strength).

We measure c' and phi' with the **direct shear**, **triaxial** or **vane**
tests, plotting Mohr circles at failure; the line tangent to them is the
**failure envelope**.

Worked example - a sandy soil, c' = 5 kPa, phi' = 32 degrees, on a plane
where sigma_n' = 100 kPa:

```text
tau_f = c' + sigma_n' * tan(phi')
      = 5 + 100 * tan(32 deg)
      = 5 + 100 * 0.625
      = 67.5 kPa    (shear strength available on that plane)
```

A stress state whose Mohr circle stays **below** the envelope is stable;
one that just **touches** it is at failure. This criterion underlies slope
stability, bearing capacity and earth-pressure analysis.

```mermaid
graph TD
    SOIL["Soil under load"] --> SHEAR["Fails by shearing on a plane"]
    SHEAR --> MC["Mohr Coulomb envelope"]
    MC --> COH["Cohesion c prime intercept"]
    MC --> FRIC["Friction angle phi prime slope"]
    COH --> STR["Shear strength tau f"]
    FRIC --> STR
    STR --> USE["Slopes bearing capacity earth pressure"]
```

Remember: tau_f = c' + sigma_n' * tan(phi'). Sands rely on friction (phi'),
clays add cohesion (c'), and strength is always taken in effective-stress
terms.
""",
        ),
        quiz_lesson(
            "Quiz: Shear strength (Mohr-Coulomb)",
            (
                q(
                    "The Mohr-Coulomb failure criterion (effective stress) is?",
                    (
                        opt("tau_f = c' - sigma_n' * tan(phi')"),
                        opt("tau_f = c' + sigma_n' * tan(phi')", correct=True),
                        opt("tau_f = sigma_n' / tan(phi')"),
                        opt("tau_f = c' * sigma_n'"),
                    ),
                    "Shear strength is the cohesion intercept c' plus the frictional "
                    "term sigma_n' * tan(phi').",
                ),
                q(
                    "In a clean sand, which parameter dominates the shear strength?",
                    (
                        opt("Cohesion c', which is large"),
                        opt(
                            "The friction angle phi'; clean sand has c' close to zero "
                            "and relies on grain friction",
                            correct=True,
                        ),
                        opt("The permeability k"),
                        opt("The liquid limit"),
                    ),
                    "Sands are frictional (c' ~ 0, phi' ~ 30-40 deg); clays add "
                    "cohesion. Strength grows with effective normal stress.",
                ),
                q(
                    "With c' = 5 kPa, phi' = 32 degrees and sigma_n' = 100 kPa, the "
                    "shear strength on the plane is about?",
                    (
                        opt("32 kPa"),
                        opt("67.5 kPa", correct=True),
                        opt("105 kPa"),
                        opt("5 kPa"),
                    ),
                    "tau_f = 5 + 100*tan(32) = 5 + 62.5 = 67.5 kPa.",
                ),
            ),
        ),
        # -- 8. Consolidation and settlement ---------------------------
        _t(
            "Consolidation and settlement",
            "11 min",
            """# Consolidation and settlement

When you load a **saturated clay**, water cannot escape instantly because
clay's permeability is tiny. The load is first carried by **excess pore
pressure**; as water slowly drains, that pressure dissipates and the load
transfers to the skeleton (effective stress rises), so the soil compresses.
This time-dependent process is **consolidation**, and the resulting
volume change is **settlement** (Terzaghi's theory).

For a **normally consolidated** clay, the settlement of a layer of
thickness H under a stress increase is:

```text
Primary consolidation settlement
   Sc = (Cc / (1 + e0)) * H * log10( (sigma0' + d_sigma) / sigma0' )

   Cc        = compression index (slope of e - log sigma' curve)
   e0        = initial void ratio
   sigma0'   = initial effective stress at mid-layer
   d_sigma   = stress increase from the load
   H         = layer thickness
```

Worked example - a 4 m normally consolidated clay layer:

```text
Given:  Cc = 0.30,  e0 = 0.90,  H = 4 m,
        sigma0' = 80 kPa,  d_sigma = 120 kPa (final 200 kPa)
Sc = (0.30 / (1 + 0.90)) * 4 * log10(200 / 80)
   = (0.30 / 1.90) * 4 * log10(2.5)
   = 0.1579 * 4 * 0.3979
   = 0.251 m   (about 251 mm of settlement)
```

The **rate** of settlement follows the coefficient of consolidation cv and
the drainage path length Hdr:

```text
Time factor      Tv = cv * t / (Hdr)^2
Time to a given degree of consolidation U:
   t = Tv * (Hdr)^2 / cv
Hdr = H  for single drainage,  H/2 for double drainage (drains both faces).
Rule of thumb:  Tv = 0.197 at U = 50 percent,  Tv = 0.848 at U = 90 percent.
```

Overloading (a **surcharge**) or **vertical drains** shorten Hdr to make
clays settle faster before construction - a common ground-improvement
tactic.

```mermaid
graph TD
    LOAD["Load on saturated clay"] --> EXCESS["Excess pore pressure"]
    EXCESS --> DRAIN["Water slowly drains out"]
    DRAIN --> EFF["Effective stress rises"]
    EFF --> COMP["Skeleton compresses"]
    COMP --> MAG["Magnitude from Cc equation"]
    COMP --> RATE["Rate from cv and time factor"]
```

Remember: consolidation is the slow squeeze of water from saturated clay.
The Cc equation gives *how much* settlement; the time factor Tv and cv give
*how fast*.
""",
        ),
        quiz_lesson(
            "Quiz: Consolidation and settlement",
            (
                q(
                    "Why is consolidation of saturated clay time-dependent?",
                    (
                        opt("Because clay expands when loaded"),
                        opt(
                            "Because clay's very low permeability makes the excess pore "
                            "water drain slowly, so effective stress rises only over time",
                            correct=True,
                        ),
                        opt("Because the load is applied gradually"),
                        opt("Because clay chemically reacts with water"),
                    ),
                    "Load first goes into excess pore pressure; slow drainage transfers "
                    "it to the skeleton, and the soil compresses over time.",
                ),
                q(
                    "In the primary consolidation equation, what does Cc represent?",
                    (
                        opt("The coefficient of permeability"),
                        opt(
                            "The compression index - the slope of the void ratio versus "
                            "log effective stress curve",
                            correct=True,
                        ),
                        opt("The undrained shear strength"),
                        opt("The critical hydraulic gradient"),
                    ),
                    "Cc measures how much void ratio drops per log-cycle of effective "
                    "stress; a larger Cc means more settlement.",
                ),
                q(
                    "How do vertical drains or a surcharge speed up consolidation?",
                    (
                        opt("They increase the clay's permeability chemically"),
                        opt(
                            "They shorten the drainage path (or raise the gradient) so "
                            "water escapes faster and settlement completes sooner",
                            correct=True,
                        ),
                        opt("They reduce the total settlement to zero"),
                        opt("They lower the compression index Cc"),
                    ),
                    "Rate depends on Tv = cv*t/Hdr^2; shorter Hdr (drains) or extra load "
                    "(surcharge) drives settlement before construction.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Soil is best described as which kind of material?",
                    (
                        opt("A single-phase solid"),
                        opt(
                            "A three-phase system of solid grains, water and air whose "
                            "arrangement governs its behavior",
                            correct=True,
                        ),
                        opt("A pure liquid"),
                        opt("A homogeneous metal"),
                    ),
                    "The three-phase model and its index properties are the starting "
                    "point of nearly every calculation.",
                ),
                q(
                    "For a saturated soil, the identity relating index properties is?",
                    (
                        opt("e = n * Gs"),
                        opt("S * e = w * Gs, which for S = 1 gives e = w * Gs", correct=True),
                        opt("w = e * n"),
                        opt("Gs = e / w"),
                    ),
                    "S*e = w*Gs links saturation, void ratio, water content and specific "
                    "gravity; at full saturation e = w*Gs.",
                ),
                q(
                    "The plasticity index of a fine soil is?",
                    (
                        opt("LL + PL"),
                        opt("LL - PL", correct=True),
                        opt("PL - SL"),
                        opt("D60 - D10"),
                    ),
                    "PI = LL - PL is the range of water content over which the soil stays plastic.",
                ),
                q(
                    "In USCS/SUCS, coarse soils and fine soils are classified by, respectively?",
                    (
                        opt("Color and smell"),
                        opt(
                            "Grain-size grading (Cu, Cc) for coarse soils, and "
                            "plasticity (LL, PI on the A-line chart) for fine soils",
                            correct=True,
                        ),
                        opt("Unit weight and permeability only"),
                        opt("Both by plasticity alone"),
                    ),
                    "The No. 200 sieve splits coarse from fine; coarse judged by "
                    "grading, fine by the plasticity chart.",
                ),
                q(
                    "In the Proctor test, dry unit weight is computed as?",
                    (
                        opt("gamma_d = gamma * (1 + w)"),
                        opt("gamma_d = gamma / (1 + w)", correct=True),
                        opt("gamma_d = gamma + w"),
                        opt("gamma_d = gamma * w"),
                    ),
                    "gamma_d = gamma / (1 + w); the peak of the gamma_d vs w curve gives "
                    "gamma_d,max at the optimum moisture content.",
                ),
                q(
                    "Darcy's law for seepage through soil is?",
                    (
                        opt("Q = k / (i * A)"),
                        opt("Q = k * i * A, with i the hydraulic gradient", correct=True),
                        opt("Q = i * A / k"),
                        opt("Q = k * A only"),
                    ),
                    "v = k*i and Q = k*i*A; the gradient i = head loss / flow length "
                    "drives the flow.",
                ),
                q(
                    "Terzaghi's effective stress principle states that?",
                    (
                        opt("Total stress equals pore pressure"),
                        opt(
                            "sigma' = sigma - u; only effective stress (carried by the "
                            "grain skeleton) controls strength and settlement",
                            correct=True,
                        ),
                        opt("Pore pressure has no effect on strength"),
                        opt("Effective stress equals total plus pore pressure"),
                    ),
                    "Effective stress = total minus pore pressure; raise u and sigma' "
                    "falls, weakening the soil.",
                ),
                q(
                    "The Mohr-Coulomb shear strength of a soil is given by?",
                    (
                        opt("tau_f = c' * sigma_n'"),
                        opt("tau_f = c' + sigma_n' * tan(phi')", correct=True),
                        opt("tau_f = c' - sigma_n'"),
                        opt("tau_f = sigma_n' / c'"),
                    ),
                    "Cohesion intercept plus a frictional term; sands rely on phi', "
                    "clays add c', always in effective stress terms.",
                ),
                q(
                    "Consolidation settlement of a normally consolidated clay depends on "
                    "which factor?",
                    (
                        opt(
                            "The compression index Cc and the log of the stress ratio", correct=True
                        ),
                        opt("Only the friction angle phi'"),
                        opt("The coefficient of uniformity Cu"),
                        opt("The Atterberg liquid limit alone"),
                    ),
                    "Sc = (Cc/(1+e0)) * H * log10((sigma0'+d_sigma)/sigma0'); Cc sets "
                    "the magnitude, cv and Tv set the rate.",
                ),
                q(
                    "An upward hydraulic gradient in sand reaching the critical value "
                    "i_cr = (Gs - 1)/(1 + e) causes what?",
                    (
                        opt("The sand to gain strength"),
                        opt(
                            "Effective stress to drop to zero - quicksand / piping, a "
                            "key check for cofferdams and dam foundations",
                            correct=True,
                        ),
                        opt("Permeability to vanish"),
                        opt("Consolidation to stop"),
                    ),
                    "At i_cr the seepage force offsets the buoyant weight; grains lose "
                    "contact and the sand boils.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SOIL_MECHANICS_COURSES: tuple[SeedCourse, ...] = (_SOIL_MECHANICS,)
