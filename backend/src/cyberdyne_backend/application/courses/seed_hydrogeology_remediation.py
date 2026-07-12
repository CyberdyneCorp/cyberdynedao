"""Academy seed content - Hydrogeology, Contaminant Transport and Remediation.

Groundwater and how to clean it up, end to end: aquifers, porosity and
Darcy's law; regional flow and wells; how dissolved contaminants move by
advection, dispersion and sorption; site investigation and sampling;
conceptual site models and human-health risk; and the full remediation
toolbox from pump-and-treat and soil vapor extraction through
bioremediation, phytoremediation, monitored natural attenuation and
permeable reactive barriers. Every lesson is a direct explanation with a
worked equation or calculation and a mermaid diagram, followed by a
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


_HYDROGEOLOGY_REMEDIATION = SeedCourse(
    slug="hydrogeology-remediation",
    title="Hydrogeology, Contaminant Transport & Remediation",
    description=(
        "Groundwater and how to clean it - aquifers and Darcy flow, "
        "contaminant transport by advection, dispersion and sorption, site "
        "investigation and human-health risk, and the full toolbox of "
        "remediation techniques from pump-and-treat and soil vapor "
        "extraction to bioremediation, monitored natural attenuation and "
        "reactive barriers - with a worked calculation and a diagram in "
        "every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Hydrogeology, Contaminant Transport and Remediation

Groundwater supplies a large share of the world's drinking water, and once
it is polluted it can stay polluted for decades. This course follows the
water: how it is stored and moves underground, how a contaminant spreads
once it gets in, how we investigate and assess the risk of a contaminated
site, and the full toolbox of techniques we use to clean it up.

The approach is **quantitative and concrete**: every lesson explains one
idea directly, works a real equation or calculation (Darcy's law, a plume
retardation factor, a risk quotient, a pumping design), and draws the idea
as a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Aquifers, porosity and Darcy's law** - how water is stored and flows
2. **Groundwater flow and wells** - hydraulic head, gradients and pumping
3. **Contaminant transport** - advection, dispersion and sorption
4. **Contaminated site investigation** - drilling, sampling, delineation
5. **Conceptual site models and risk** - sources, pathways, receptors
6. **Pump-and-treat and soil vapor extraction** - hydraulic and vapor control
7. **Bioremediation and phytoremediation** - biology does the work
8. **Monitored natural attenuation and reactive barriers** - passive cleanup

Grounded in real practice - Darcy's law, MODFLOW and MT3D modeling, US EPA
and CETESB risk frameworks, CONAMA and ABNT NBR guidance, WHO drinking-water
standards - but kept teachable. This is the map from a drop of rain to a
remediated aquifer.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the overall arc of this course?",
                    (
                        opt("Only how to drill a water well"),
                        opt(
                            "From how groundwater is stored and moves, through how "
                            "contaminants spread and are assessed, to the full toolbox "
                            "for cleaning an aquifer up",
                            correct=True,
                        ),
                        opt("Only the chemistry of pollutants"),
                        opt("How to build a surface water dam"),
                    ),
                    "The course follows the water: storage and flow, transport, "
                    "investigation and risk, then remediation.",
                ),
                q(
                    "Why does groundwater contamination matter so much?",
                    (
                        opt("Groundwater is never used for drinking"),
                        opt(
                            "Groundwater supplies much of the world's drinking water "
                            "and, once polluted, can stay contaminated for decades",
                            correct=True,
                        ),
                        opt("Aquifers clean themselves within hours"),
                        opt("Contaminants cannot dissolve in water"),
                    ),
                    "Slow flow and long residence times mean contamination persists, "
                    "making prevention and cleanup both critical.",
                ),
            ),
        ),
        # -- 1. Aquifers, porosity and Darcy's law ---------------------
        _t(
            "Aquifers, porosity and Darcy's law",
            "11 min",
            """# Aquifers, porosity and Darcy's law

An **aquifer** is a body of saturated rock or sediment that stores and
transmits usable quantities of water. A layer that holds water but barely
transmits it (clay) is an **aquitard**. Aquifers come in two main types:

- **Unconfined (water-table)** - the top of the saturated zone is the water
  table, open to the atmosphere through the soil above it.
- **Confined (artesian)** - sandwiched between aquitards, under pressure, so
  water in a well rises above the top of the aquifer.

Two properties describe the storage and flow capacity of the material:

- **Porosity (n)** - the fraction of the total volume that is void space.
  Sand is roughly 0.25 to 0.40. But not all pore water can move; the part
  that drains freely is the **effective porosity**.
- **Hydraulic conductivity (K)** - how easily the material transmits water,
  in units of length per time (m/day). Gravel is high, clay is very low -
  conductivity spans over ten orders of magnitude across earth materials.

**Darcy's law** (Henry Darcy, 1856) is the foundation of the whole field.
It says the volumetric flow rate through a porous medium is proportional to
the cross-sectional area and the hydraulic gradient:

```text
Darcy's law:
    Q = -K * A * (dh / dL)

    Q  = volumetric flow rate   (m^3/day)
    K  = hydraulic conductivity (m/day)
    A  = cross-sectional area   (m^2)
    dh/dL = hydraulic gradient  (dimensionless, head drop per length)

Darcy (specific) velocity:  q = Q / A = -K * (dh/dL)
Average linear (seepage) velocity of water:
    v = q / n_e         where n_e = effective porosity

Worked example:
    K = 15 m/day,  gradient dh/dL = 0.004,  n_e = 0.25
    q = 15 * 0.004            = 0.06 m/day
    v = 0.06 / 0.25           = 0.24 m/day
So the actual water (and a conservative contaminant) moves ~0.24 m/day,
about 88 m per year - slow, which is why plumes persist.
```

The minus sign means water flows from **high head to low head** (downhill in
energy). The distinction between the Darcy velocity q and the real seepage
velocity v matters: contaminants travel at the faster seepage velocity,
because the water squeezes through only the pore space, not the whole area.

```mermaid
graph LR
    RECHARGE["Rain and recharge"] --> WT["Water table unconfined"]
    WT --> UNCONF["Unconfined aquifer"]
    UNCONF --> AQUITARD["Aquitard clay layer"]
    AQUITARD --> CONF["Confined aquifer under pressure"]
    CONF --> HEAD["High head to low head flow"]
    HEAD --> DARCY["Darcy law sets the rate"]
```

Remember: porosity is how much water is stored, conductivity is how fast it
moves, and Darcy's law ties gradient, conductivity and flow together.
""",
        ),
        quiz_lesson(
            "Quiz: Aquifers, porosity and Darcy's law",
            (
                q(
                    "What is the difference between an aquifer and an aquitard?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "An aquifer stores and readily transmits usable water; an "
                            "aquitard holds water but barely transmits it (e.g. clay)",
                            correct=True,
                        ),
                        opt("An aquitard is always deeper than an aquifer"),
                        opt("An aquifer contains no water"),
                    ),
                    "Transmission is the key: aquifers yield water, aquitards restrict "
                    "its movement.",
                ),
                q(
                    "In Darcy's law Q = -K*A*(dh/dL), what does the hydraulic "
                    "conductivity K represent?",
                    (
                        opt("The porosity of the rock"),
                        opt("The chemical reactivity of the water"),
                        opt(
                            "How easily the material transmits water, in length per "
                            "time - high for gravel, very low for clay",
                            correct=True,
                        ),
                        opt("The depth to the water table"),
                    ),
                    "K spans many orders of magnitude across earth materials and sets "
                    "how fast water moves under a given gradient.",
                ),
                q(
                    "Why is the average linear (seepage) velocity v faster than the "
                    "Darcy velocity q?",
                    (
                        opt("Because v ignores the hydraulic gradient"),
                        opt(
                            "Because water only flows through the pore space, so "
                            "v = q / n_e divides by the effective porosity (a fraction < 1)",
                            correct=True,
                        ),
                        opt("Because K is negative"),
                        opt("They are actually equal"),
                    ),
                    "Dividing the Darcy velocity by effective porosity gives the real "
                    "speed a water molecule (or conservative tracer) travels.",
                ),
            ),
        ),
        # -- 2. Groundwater flow and wells -----------------------------
        _t(
            "Groundwater flow and wells",
            "11 min",
            """# Groundwater flow and wells

Groundwater flow is driven by differences in **hydraulic head (h)** - the
mechanical energy of water per unit weight, essentially the elevation to
which water rises in a well. Head has two parts: **elevation head**
(position) plus **pressure head** (depth of water in the well). Water always
flows from **higher head to lower head**.

Measure head in three or more wells and you can build a **potentiometric
(water-table) map** of head contours. Flow lines run perpendicular to the
contours, pointing downgradient - this tells you which way a contaminant
plume will move, which is the first thing you need to know at any site.

The **hydraulic gradient** is the head drop divided by the distance:

```text
Hydraulic gradient:
    i = (h1 - h2) / L

Transmissivity (aquifer-integrated conductivity):
    T = K * b        where b = saturated thickness (m)

Steady radial flow to a well (Thiem equation, confined aquifer):
    Q = 2 * pi * T * (h2 - h1) / ln(r2 / r1)

Worked example - three-well gradient:
    Well A head = 30.0 m,  Well B head = 29.4 m,  spacing L = 150 m
    i = (30.0 - 29.4) / 150 = 0.6 / 150 = 0.004
This 0.004 gradient feeds straight into Darcy's law for flow direction
and rate; flow is from A (high head) toward B (low head).
```

When you **pump a well**, you lower head at the well and create a **cone of
depression** - a downward funnel in the water table that radiates outward.
The drawdown (head decline) is largest at the well and decreases with
distance. The **radius of influence** is how far out the pumping is felt.

Two ideas are central to remediation:

- **Capture zone** - the region of the aquifer that eventually flows into a
  pumping well. Designing pump-and-treat is really designing a capture zone
  wide enough to contain the whole plume.
- **Aquifer tests (pumping tests)** - pump at a known rate, measure drawdown
  in observation wells over time, and back out T and storativity. Those
  parameters feed flow models like **MODFLOW**.

```mermaid
graph TD
    HEAD["Measure head in wells"] --> MAP["Potentiometric contour map"]
    MAP --> FLOW["Flow lines downgradient"]
    PUMP["Pump a well"] --> CONE["Cone of depression"]
    CONE --> CAPTURE["Capture zone forms"]
    CAPTURE --> CONTAIN["Contain the plume"]
    FLOW --> CONTAIN
```

Remember: head differences drive flow, contour maps reveal direction, and a
pumping well's capture zone is the tool that lets us intercept a plume.
""",
        ),
        quiz_lesson(
            "Quiz: Groundwater flow and wells",
            (
                q(
                    "What does a potentiometric (water-table) contour map tell you?",
                    (
                        opt("The chemical composition of the water"),
                        opt(
                            "The distribution of hydraulic head, from which flow "
                            "direction (perpendicular to contours, downgradient) is read",
                            correct=True,
                        ),
                        opt("The porosity of every layer"),
                        opt("The age of the aquifer rock"),
                    ),
                    "Head contours reveal flow direction - the first thing you need to "
                    "predict where a plume will travel.",
                ),
                q(
                    "What is a 'cone of depression'?",
                    (
                        opt("A geological rock formation"),
                        opt(
                            "The downward funnel in the water table created around a "
                            "pumping well, with drawdown greatest at the well",
                            correct=True,
                        ),
                        opt("A type of drilling rig"),
                        opt("A confined aquifer under pressure"),
                    ),
                    "Pumping lowers head at the well; the cone radiates outward to the "
                    "radius of influence.",
                ),
                q(
                    "Why is the 'capture zone' the key concept for pump-and-treat design?",
                    (
                        opt("It measures the water's temperature"),
                        opt(
                            "It is the region that eventually flows into the pumping "
                            "well, so it must be made wide enough to contain the entire plume",
                            correct=True,
                        ),
                        opt("It sets the color of the water"),
                        opt("It has no role in remediation"),
                    ),
                    "Designing hydraulic containment means shaping a capture zone that "
                    "swallows the whole contaminant plume.",
                ),
            ),
        ),
        # -- 3. Contaminant transport ----------------------------------
        _t(
            "Contaminant transport (advection, dispersion, sorption)",
            "12 min",
            """# Contaminant transport (advection, dispersion, sorption)

Once a dissolved contaminant enters groundwater, three processes govern how
it moves and spreads:

- **Advection** - the contaminant is carried along with the flowing water at
  the average seepage velocity v. This is the bulk motion of the plume.
- **Dispersion** - the plume spreads out longitudinally and transversely as
  water threads through pores at different speeds and paths (mechanical
  dispersion) plus molecular diffusion. Dispersion smears sharp fronts into
  gradual ones and dilutes peak concentrations.
- **Sorption (retardation)** - the contaminant partitions between water and
  the solid aquifer grains. Time spent stuck to solids means the contaminant
  front lags behind the water. This is quantified by the **retardation
  factor R**.

The one-dimensional **advection-dispersion equation (ADE)** ties these
together:

```text
Advection-dispersion-reaction equation (1-D):
    R * dC/dt = D * d2C/dx2  -  v * dC/dx  -  R * lambda * C

    C  = concentration            v = seepage velocity
    D  = dispersion coefficient   lambda = decay rate (1/time)
    R  = retardation factor

Linear sorption and retardation:
    Kd = Koc * foc              (partition coefficient, L/kg)
    R  = 1 + (rho_b / n_e) * Kd

Worked retardation example (benzene-like solute):
    Koc = 60 L/kg,  foc = 0.002  ->  Kd = 60 * 0.002 = 0.12 L/kg
    bulk density rho_b = 1.8 kg/L,  effective porosity n_e = 0.30
    R = 1 + (1.8 / 0.30) * 0.12 = 1 + 6.0 * 0.12 = 1.72
The contaminant front moves at v / R = 1 / 1.72 = 0.58 times the water
velocity - about 42 percent slower than the groundwater itself.
```

Sorption depends strongly on the fraction of organic carbon (**foc**) in the
soil: more organic matter means more retardation for hydrophobic organics.
A retardation factor of 1 means the solute is conservative (moves with the
water, like chloride); values above 1 mean it is delayed.

A special complication is **NAPL** (non-aqueous phase liquid): fuels and
solvents that do not dissolve readily. **LNAPLs** (gasoline) are lighter than
water and float on the water table; **DNAPLs** (chlorinated solvents like
TCE/PCE) are denser and sink, pooling on aquitards - a long-term source that
slowly dissolves and feeds the plume for years.

```mermaid
graph LR
    SOURCE["Contaminant source"] --> ADV["Advection carries plume"]
    ADV --> DISP["Dispersion spreads and dilutes"]
    DISP --> SORB["Sorption retards the front"]
    SORB --> PLUME["Dissolved plume downgradient"]
    NAPL["DNAPL sinks to aquitard"] --> SOURCE
```

Remember: advection sets the speed and direction, dispersion spreads and
dilutes, and sorption slows the front - together they shape every plume.
""",
        ),
        quiz_lesson(
            "Quiz: Contaminant transport (advection, dispersion, sorption)",
            (
                q(
                    "What does advection describe in contaminant transport?",
                    (
                        opt("The spreading and dilution of the plume"),
                        opt(
                            "The bulk carrying of the contaminant along with the "
                            "flowing water at the seepage velocity",
                            correct=True,
                        ),
                        opt("The chemical decay of the contaminant"),
                        opt("The sticking of contaminant to soil grains"),
                    ),
                    "Advection is transport by the moving water itself - the plume's "
                    "main motion; dispersion and sorption modify it.",
                ),
                q(
                    "A retardation factor R = 1.72 means the contaminant front...",
                    (
                        opt("moves faster than the groundwater"),
                        opt(
                            "moves at v/R, i.e. about 0.58 times the water velocity - "
                            "delayed because it partitions onto the solids",
                            correct=True,
                        ),
                        opt("does not move at all"),
                        opt("has no sorption"),
                    ),
                    "R = 1 + (rho_b/n_e)*Kd; the front travels at v/R, so higher "
                    "sorption means more delay.",
                ),
                q(
                    "Why are DNAPLs (e.g. TCE, PCE) such a persistent problem?",
                    (
                        opt("They evaporate instantly"),
                        opt(
                            "Being denser than water they sink and pool on aquitards, "
                            "slowly dissolving and feeding the plume for years",
                            correct=True,
                        ),
                        opt("They float and blow away"),
                        opt("They are completely harmless"),
                    ),
                    "Dense non-aqueous phase liquids form long-term source zones that "
                    "are very hard to locate and remove.",
                ),
            ),
        ),
        # -- 4. Contaminated site investigation ------------------------
        _t(
            "Contaminated site investigation",
            "11 min",
            """# Contaminated site investigation

You cannot clean up what you have not characterized. **Site investigation**
is the phased process of finding out what contaminants are present, where,
in what concentrations, and how they are moving - the data that every later
decision rests on. It is typically staged so effort follows evidence:

- **Phase I - preliminary (historical)** - desk study of the site history,
  past land uses, records and a walkover. No sampling; identifies *areas of
  concern* and whether contamination is plausible.
- **Phase II - confirmatory / investigative** - actual drilling, soil and
  groundwater sampling, and lab analysis to confirm presence and identity.
- **Phase III - detailed / delineation** - map the full extent of the plume
  in three dimensions and define the source zone, enough to design cleanup.

Fieldwork tools include **soil borings** and **monitoring wells** (screened
at the target depth), **direct-push** rigs (Geoprobe) for fast profiling,
and increasingly **Membrane Interface Probe (MIP)** and **LIF** sensors that
log contamination continuously with depth. Samples go to the lab for the
target analytes (BTEX, chlorinated solvents, metals, etc.).

Getting representative samples matters as much as the analysis. Good
practice: purge wells before sampling, minimize aeration for volatiles, use
field QA/QC (blanks, duplicates), and preserve samples correctly.

```text
Delineation math - estimating dissolved contaminant mass:
    M = C * V_water = C * (n_e * V_bulk)

    C        = average dissolved concentration (mg/L = g/m^3)
    n_e      = effective porosity
    V_bulk   = contaminated aquifer volume (m^3)

Worked example:
    plume 100 m long x 40 m wide x 5 m thick = 20000 m^3 bulk
    n_e = 0.30  ->  water volume = 0.30 * 20000 = 6000 m^3
    average C = 2 mg/L = 2 g/m^3
    dissolved mass M = 2 * 6000 = 12000 g = 12 kg
This dissolved mass guides how big a treatment system must be - and it is
often small next to the mass still held in the source zone and sorbed to soil.
```

Sampling density is a trade-off: too few points and you miss the plume; too
many and cost explodes. Grids, judgmental placement near sources, and
statistical designs all get used. The deliverable is the input to the next
lesson: a defensible picture of source, extent and concentrations.

```mermaid
graph TD
    P1["Phase I historical desk study"] --> P2["Phase II drilling and sampling"]
    P2 --> LAB["Lab analysis of analytes"]
    LAB --> P3["Phase III delineate the plume"]
    P3 --> MAP["Extent and source defined"]
    MAP --> DESIGN["Feeds remediation design"]
```

Remember: investigate in phases, sample representatively, delineate in three
dimensions, and quantify the mass - characterization is the foundation of
every cleanup decision.
""",
        ),
        quiz_lesson(
            "Quiz: Contaminated site investigation",
            (
                q(
                    "What is the purpose of a Phase I (preliminary) investigation?",
                    (
                        opt("To fully delineate the plume in 3-D"),
                        opt(
                            "A desk study of site history and a walkover to identify "
                            "areas of concern and whether contamination is plausible - "
                            "no sampling yet",
                            correct=True,
                        ),
                        opt("To install the pump-and-treat system"),
                        opt("To issue the final closure certificate"),
                    ),
                    "Phase I is historical/qualitative; sampling and confirmation come "
                    "in Phase II, delineation in Phase III.",
                ),
                q(
                    "Why does representative sampling matter as much as lab analysis?",
                    (
                        opt("It does not; only the lab number counts"),
                        opt(
                            "A poorly collected sample (aerated, unpurged, wrong depth) "
                            "gives a wrong picture no matter how good the lab is",
                            correct=True,
                        ),
                        opt("Because labs never make errors"),
                        opt("Because sampling replaces the need for wells"),
                    ),
                    "Garbage in, garbage out: purge wells, minimize aeration for "
                    "volatiles, and run field QA/QC.",
                ),
                q(
                    "Using M = C * n_e * V_bulk, a 20000 m^3 plume with n_e = 0.30 and "
                    "C = 2 mg/L holds roughly how much dissolved mass?",
                    (
                        opt("12 kg", correct=True),
                        opt("120 kg"),
                        opt("2 kg"),
                        opt("1200 kg"),
                    ),
                    "Water volume = 0.30 * 20000 = 6000 m^3; mass = 2 g/m^3 * 6000 = "
                    "12000 g = 12 kg dissolved.",
                ),
            ),
        ),
        # -- 5. Conceptual site models and risk ------------------------
        _t(
            "Conceptual site models and risk",
            "11 min",
            """# Conceptual site models and risk

A **conceptual site model (CSM)** is the organizing story of a contaminated
site: it links **sources** of contamination, the **pathways** by which
contaminants travel, and the **receptors** (people, ecosystems) that could
be exposed. If any one of source, pathway or receptor is missing, there is
no complete exposure and therefore no risk by that route - this
**source-pathway-receptor** linkage is the heart of risk-based cleanup.

Typical elements:

- **Sources** - a leaking tank, a spill, a DNAPL pool, contaminated soil.
- **Pathways** - groundwater flow to a drinking well, vapor intrusion into a
  building, dermal contact, dust inhalation, uptake into crops.
- **Receptors** - residents, workers, aquatic life; each with different
  exposure and sensitivity.

**Human-health risk assessment** turns the CSM into numbers. Exposure is the
intake of a chemical; toxicity is how harmful a given intake is. The two are
combined differently for the two kinds of health effect:

```text
Chronic daily intake (drinking water, simplified):
    CDI = (C * IR * EF * ED) / (BW * AT)
    C=conc, IR=intake rate, EF=exposure freq, ED=duration,
    BW=body weight, AT=averaging time

Non-carcinogens - Hazard Quotient:
    HQ = CDI / RfD          (RfD = reference dose)
    HQ <= 1  ->  acceptable;  HQ > 1  ->  concern

Carcinogens - Excess Lifetime Cancer Risk:
    Risk = CDI * SF         (SF = slope factor)
    Acceptable range usually 1e-6 to 1e-4

Worked HQ example:
    CDI = 0.003 mg/kg/day,  RfD = 0.004 mg/kg/day
    HQ = 0.003 / 0.004 = 0.75  ->  below 1, acceptable by this route
```

Regulators compare measured concentrations against **screening levels** -
US EPA Regional Screening Levels, CETESB intervention values in Brazil,
CONAMA Resolution 420 for soil and groundwater quality, and WHO
drinking-water guideline values. Exceeding a screening level does not by
itself prove harm; it triggers a closer, site-specific risk assessment using
the CSM.

The CSM is a **living document**: as investigation data arrive it is refined,
and it directly drives remedy selection - you remediate to break the
critical source-pathway-receptor linkages.

```mermaid
graph LR
    SRC["Source leaking tank or DNAPL"] --> PATH["Pathway groundwater or vapor"]
    PATH --> REC["Receptor residents or wells"]
    REC --> EXP["Exposure and intake"]
    EXP --> RISK["Hazard quotient and cancer risk"]
    RISK --> DECISION["Remedy breaks the linkage"]
```

Remember: no source-pathway-receptor linkage means no risk; the CSM maps
those linkages and risk assessment quantifies them, driving the cleanup goal.
""",
        ),
        quiz_lesson(
            "Quiz: Conceptual site models and risk",
            (
                q(
                    "What three elements must all be present for an exposure to occur "
                    "in a conceptual site model?",
                    (
                        opt("Soil, water and air"),
                        opt(
                            "A source, a pathway, and a receptor - break any one and "
                            "that exposure route is incomplete",
                            correct=True,
                        ),
                        opt("A pump, a well and a filter"),
                        opt("Phase I, II and III reports"),
                    ),
                    "Source-pathway-receptor is the core linkage; remediation aims to "
                    "break at least one link.",
                ),
                q(
                    "For a non-carcinogen, what does a Hazard Quotient (HQ) greater "
                    "than 1 indicate?",
                    (
                        opt("The site is definitely safe"),
                        opt(
                            "The estimated intake exceeds the reference dose, so there "
                            "is potential concern warranting action or closer assessment",
                            correct=True,
                        ),
                        opt("A cancer risk of exactly one in a million"),
                        opt("The well has run dry"),
                    ),
                    "HQ = CDI/RfD; at or below 1 is acceptable, above 1 flags a "
                    "possible non-cancer health concern.",
                ),
                q(
                    "What is the role of screening levels such as US EPA RSLs, CETESB "
                    "values or CONAMA 420?",
                    (
                        opt("They are the exact cleanup completion date"),
                        opt(
                            "Benchmark concentrations that, when exceeded, trigger a "
                            "closer site-specific risk assessment - not automatic proof of harm",
                            correct=True,
                        ),
                        opt("They set the price of remediation"),
                        opt("They measure hydraulic conductivity"),
                    ),
                    "Exceeding a conservative screening level prompts further "
                    "evaluation via the CSM and site-specific risk assessment.",
                ),
            ),
        ),
        # -- 6. Pump-and-treat and soil vapor extraction ---------------
        _t(
            "Pump-and-treat and soil vapor extraction",
            "12 min",
            """# Pump-and-treat and soil vapor extraction

The first two workhorse **active** remediation methods pull contaminants out
of the ground - one from the saturated zone, one from the unsaturated zone.

**Pump-and-treat (P&T)** extracts contaminated groundwater through wells,
treats it aboveground (air stripping, granular activated carbon, advanced
oxidation), and discharges or reinjects the clean water. Its two goals are
**hydraulic containment** (the capture zone stops the plume spreading) and
**mass removal** (pulling contaminated water out). The extraction wells must
create a capture zone that fully encloses the plume:

```text
Capture-zone half-width for a single well (uniform flow, confined):
    y_max = Q / (2 * B * K * i)

    Q = pumping rate (m^3/day)   B = aquifer thickness (m)
    K = conductivity (m/day)     i = regional gradient

Worked example:
    Q = 200 m^3/day,  B = 10 m,  K = 15 m/day,  i = 0.004
    y_max = 200 / (2 * 10 * 15 * 0.004)
          = 200 / 1.2 = 167 m total capture width (2 * y_max)
If the plume is wider than this, add wells or increase Q.
```

P&T is reliable for containment but famously slow at *finishing* cleanup:
sorbed contaminant and DNAPL keep bleeding back into the water, producing a
**concentration tailing and rebound** curve. Concentrations fall fast at
first, then flatten out far above the target - often for decades.

**Soil vapor extraction (SVE)** treats the **unsaturated (vadose) zone**
above the water table. A blower applies a vacuum to wells screened in the
soil, pulling air through the pores; **volatile** contaminants (gasoline,
solvents) partition into that moving air and are drawn out for treatment.
SVE is very effective for volatile compounds in permeable soil. Adding **air
sparging** (injecting air below the water table so volatiles bubble up into
the SVE capture) extends it to the saturated zone.

```python
# Estimate SVE mass-removal rate from extracted vapor
Q_air = 500.0        # m^3/day of extracted vapor
C_vapor = 1200.0     # mg/m^3 contaminant in the vapor stream

daily_removal_g = Q_air * C_vapor / 1000.0   # mg -> g
print(f"SVE removes ~{daily_removal_g:.0f} g/day")   # ~600 g/day
# Removal declines over time as easy mass is depleted (asymptotic tailing)
```

```mermaid
graph TD
    PLUME["Groundwater plume"] --> EXW["Extraction wells pump out water"]
    EXW --> TREAT["Treatment carbon or air stripper"]
    TREAT --> DISCH["Clean water discharged or reinjected"]
    VADOSE["Vadose zone vapor"] --> SVE["SVE vacuum blower"]
    SVE --> VTREAT["Vapor treatment"]
```

Remember: P&T contains and slowly removes from the saturated zone but tails
for years; SVE strips volatiles from the vadose zone; together they are the
classic active pump-based toolkit.
""",
        ),
        quiz_lesson(
            "Quiz: Pump-and-treat and soil vapor extraction",
            (
                q(
                    "What are the two main goals of a pump-and-treat system?",
                    (
                        opt("Aeration and disinfection"),
                        opt(
                            "Hydraulic containment (a capture zone that stops the "
                            "plume) and mass removal (extracting contaminated water)",
                            correct=True,
                        ),
                        opt("Drilling and logging"),
                        opt("Vapor extraction and sparging"),
                    ),
                    "P&T both contains the plume and pulls mass out; the extraction "
                    "wells must capture the whole plume width.",
                ),
                q(
                    "Why does pump-and-treat often fail to reach the cleanup target quickly?",
                    (
                        opt("The pumps are too powerful"),
                        opt(
                            "Sorbed contaminant and DNAPL keep bleeding back into the "
                            "water, causing concentration tailing and rebound for years",
                            correct=True,
                        ),
                        opt("Groundwater is always already clean"),
                        opt("Carbon filters add contamination"),
                    ),
                    "Concentrations drop fast then flatten far above target - the "
                    "classic tailing and rebound problem.",
                ),
                q(
                    "What zone and contaminant type is soil vapor extraction (SVE) "
                    "best suited for?",
                    (
                        opt("Non-volatile metals in the saturated zone"),
                        opt(
                            "Volatile organic compounds in the unsaturated (vadose) "
                            "zone, in permeable soil, pulled out as vapor by a vacuum",
                            correct=True,
                        ),
                        opt("Radioactive waste in bedrock"),
                        opt("Dissolved salts in a confined aquifer"),
                    ),
                    "SVE draws air through vadose-zone pores; volatiles partition into "
                    "it. Air sparging extends the reach below the water table.",
                ),
            ),
        ),
        # -- 7. Bioremediation and phytoremediation --------------------
        _t(
            "Bioremediation and phytoremediation",
            "12 min",
            """# Bioremediation and phytoremediation

Instead of pumping contaminants out, **bioremediation** and
**phytoremediation** let biology destroy or immobilize them, often **in
situ** (in place) and at lower cost.

**Bioremediation** harnesses microorganisms that use contaminants as food or
electron acceptors, degrading them - ideally to harmless end products like
CO2, water and chloride. Two strategies:

- **Biostimulation** - the right microbes are already present; you add what
  is limiting (oxygen, nutrients, an electron donor) to speed them up.
- **Bioaugmentation** - the needed microbes are absent, so you inject a
  cultured strain (e.g. *Dehalococcoides* for chlorinated-solvent
  dechlorination).

The redox condition decides the pathway. **Aerobic** bacteria readily
oxidize petroleum hydrocarbons (BTEX) when oxygen is supplied. Chlorinated
solvents like PCE and TCE instead need **anaerobic reductive dechlorination**,
where an added electron donor (lactate, emulsified vegetable oil) drives
stepwise removal of chlorine atoms: PCE to TCE to DCE to vinyl chloride to
ethene. Watch for **vinyl chloride** - a more toxic intermediate that means
the process must be allowed to run to completion.

```text
Aerobic biodegradation of benzene (stoichiometry):
    C6H6 + 7.5 O2  ->  6 CO2 + 3 H2O

    Oxygen demand:  7.5 mol O2 per mol benzene
    = 7.5 * 32 g/mol O2  per  78 g/mol benzene
    = 240 / 78 = 3.08 g O2 per g benzene degraded

First-order in-situ decay (attenuation):
    C(t) = C0 * exp(-k * t)
    half-life  t_half = ln(2) / k
    e.g. k = 0.002 /day  ->  t_half = 0.693 / 0.002 = 347 days
This oxygen demand tells you how much air or oxygen release compound to add.
```

**Phytoremediation** uses **plants** to clean soil and shallow groundwater
through several mechanisms:

- **Phytoextraction** - plants (hyperaccumulators) take up metals into
  harvestable tissue.
- **Rhizodegradation** - root-zone microbes break down organics, stimulated
  by root exudates.
- **Phytostabilization** - roots immobilize contaminants, limiting spread.
- **Phytovolatilization / hydraulic control** - deep-rooted trees (poplars,
  willows) transpire large volumes, drawing down and containing plumes.

It is low-cost and green but slow, limited to the root depth, and the
harvested biomass may itself need disposal.

```mermaid
graph TD
    ORG["Organic contaminant"] --> AER["Aerobic add oxygen and nutrients"]
    AER --> CO2["CO2 water and chloride"]
    CHL["Chlorinated solvent"] --> ANA["Anaerobic reductive dechlorination"]
    ANA --> ETH["Stepwise to ethene"]
    METAL["Metals in soil"] --> PHYTO["Phytoextraction by plants"]
    PHYTO --> HARV["Harvest biomass"]
```

Remember: bioremediation lets microbes destroy organics (aerobic for
petroleum, anaerobic for chlorinated), and phytoremediation uses plants to
extract, degrade, stabilize or hydraulically contain - biology as the cleanup engine.
""",
        ),
        quiz_lesson(
            "Quiz: Bioremediation and phytoremediation",
            (
                q(
                    "What is the difference between biostimulation and bioaugmentation?",
                    (
                        opt("They are identical"),
                        opt(
                            "Biostimulation adds what limits microbes already present "
                            "(oxygen, nutrients); bioaugmentation injects microbes that "
                            "are missing",
                            correct=True,
                        ),
                        opt("Biostimulation uses plants; bioaugmentation uses pumps"),
                        opt("Both mean removing all the soil"),
                    ),
                    "Stimulate existing microbes, or augment with cultured strains "
                    "like Dehalococcoides when the right degraders are absent.",
                ),
                q(
                    "Petroleum hydrocarbons (BTEX) versus chlorinated solvents (PCE/TCE) "
                    "typically need which redox conditions?",
                    (
                        opt("Both need aerobic conditions only"),
                        opt(
                            "BTEX degrade well aerobically (add oxygen); PCE/TCE need "
                            "anaerobic reductive dechlorination with an electron donor",
                            correct=True,
                        ),
                        opt("Both need anaerobic conditions only"),
                        opt("Neither can be biodegraded"),
                    ),
                    "Redox controls the pathway; watch for vinyl chloride, a toxic "
                    "intermediate that must be driven fully to ethene.",
                ),
                q(
                    "Which phytoremediation mechanism uses deep-rooted trees to "
                    "transpire water and contain a plume?",
                    (
                        opt("Phytoextraction of metals into leaves"),
                        opt(
                            "Hydraulic control - trees like poplars and willows draw "
                            "down and contain shallow plumes by transpiration",
                            correct=True,
                        ),
                        opt("Excavation and landfilling"),
                        opt("Air sparging"),
                    ),
                    "High-transpiration trees act as living pumps, providing hydraulic "
                    "containment as well as rhizosphere degradation.",
                ),
            ),
        ),
        # -- 8. Monitored natural attenuation and reactive barriers ----
        _t(
            "Monitored natural attenuation and reactive barriers",
            "12 min",
            """# Monitored natural attenuation and reactive barriers

Not every cleanup needs pumps and blowers. Two **passive** approaches let
natural processes or a stationary treatment zone do the work with minimal
energy - but only where they genuinely protect receptors.

**Monitored natural attenuation (MNA)** relies on the physical, chemical and
biological processes that already shrink a plume: biodegradation (usually the
dominant, destructive one), dispersion, dilution, sorption, and abiotic
reactions. It is not "do nothing" - it demands **evidence** that attenuation
is real and sustained, plus a long-term monitoring network to confirm the
plume is stable or shrinking and not reaching receptors. Regulators expect
**three lines of evidence**:

1. Historical concentration trends showing the plume is stable or declining.
2. Geochemical indicators of active degradation (falling electron acceptors,
   rising byproducts - e.g. depleted oxygen and nitrate, elevated CO2,
   for chlorinated solvents the daughter products ethene and chloride).
3. Optional microbial or laboratory data confirming the degraders are present
   and active.

```text
Is MNA fast enough? Compare plume travel to degradation.
    plume front advances at  v/R  (retarded seepage velocity)
    concentration decays as   C(x) = C0 * exp(-k * x / (v/R))

Worked screen:
    v/R = 0.15 m/day,  first-order k = 0.0015 /day
    distance to receptor well = 120 m
    exponent = -k * x / (v/R) = -0.0015 * 120 / 0.15 = -1.2
    C/C0 = exp(-1.2) = 0.30
So 70 percent is removed before the plume reaches the well - MNA may
suffice only if the arriving 30 percent is below the cleanup standard.
```

**Permeable reactive barriers (PRBs)** are the passive counterpart to
pump-and-treat. Instead of pumping water to a treatment plant, you install a
stationary, permeable wall of reactive media **across the flow path**;
groundwater flows through it under its own natural gradient and is treated in
place. The media are chosen for the contaminant:

- **Zero-valent iron (ZVI)** - reductively dechlorinates TCE/PCE and reduces
  chromium and some other metals; the classic PRB fill.
- **Granular activated carbon** - adsorbs organics.
- **Limestone or apatite** - raises pH and precipitates or immobilizes metals.
- **Organic mulch / compost** - stimulates biological reduction.

Because there are no pumps, energy and operating costs are low; the main
risks are the barrier **clogging** or losing reactivity over time, and it
only treats water that actually flows through it, so placement and keying
into an aquitard matter.

```mermaid
graph LR
    PLUME["Plume moves under natural gradient"] --> WALL["Permeable reactive barrier"]
    WALL --> ZVI["Zero valent iron treats water"]
    ZVI --> CLEAN["Clean water downgradient"]
    SEP["Separate approach"] --> MNA["Monitored natural attenuation"]
    MNA --> MON["Long term monitoring network"]
    MON --> STABLE["Confirm plume stable or shrinking"]
```

Remember: MNA lets proven natural degradation finish the job under
monitoring and lines of evidence; a PRB is a passive in-place wall the water
cleans itself in - low energy, but both must be verified to protect receptors.
""",
        ),
        quiz_lesson(
            "Quiz: Monitored natural attenuation and reactive barriers",
            (
                q(
                    "Why is monitored natural attenuation (MNA) not the same as 'doing nothing'?",
                    (
                        opt("Because it uses large pumps"),
                        opt(
                            "It requires evidence that attenuation is real and "
                            "sustained plus long-term monitoring to confirm the plume "
                            "is stable and not reaching receptors",
                            correct=True,
                        ),
                        opt("Because it excavates all the soil"),
                        opt("Because it is always the fastest option"),
                    ),
                    "MNA relies on natural (mainly biodegradation) processes but must "
                    "prove them with multiple lines of evidence and monitoring.",
                ),
                q(
                    "How does a permeable reactive barrier (PRB) differ from pump-and-treat?",
                    (
                        opt("A PRB pumps water to a distant plant"),
                        opt(
                            "A PRB is a stationary permeable wall the plume flows "
                            "through under its own natural gradient, treating water in "
                            "place with no pumps",
                            correct=True,
                        ),
                        opt("A PRB only works on surface water"),
                        opt("They are exactly the same technology"),
                    ),
                    "PRBs are passive: the aquifer's own gradient carries water "
                    "through reactive media - low energy and operating cost.",
                ),
                q(
                    "Zero-valent iron (ZVI) is a common PRB medium mainly because it...",
                    (
                        opt("adds oxygen to the water"),
                        opt(
                            "reductively dechlorinates solvents like TCE/PCE and "
                            "reduces metals such as chromium as water passes through",
                            correct=True,
                        ),
                        opt("raises the water temperature"),
                        opt("increases the hydraulic gradient"),
                    ),
                    "ZVI is a reductant: it degrades chlorinated solvents and "
                    "immobilizes redox-sensitive metals in place.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In Darcy's law, the average linear (seepage) velocity a "
                    "contaminant travels at is...",
                    (
                        opt("v = K * i only"),
                        opt(
                            "v = q / n_e - the Darcy velocity divided by effective "
                            "porosity, faster than the Darcy velocity",
                            correct=True,
                        ),
                        opt("always equal to the Darcy velocity"),
                        opt("independent of porosity"),
                    ),
                    "Water squeezes through pores only, so dividing by effective "
                    "porosity gives the real (faster) transport speed.",
                ),
                q(
                    "A potentiometric contour map is used to determine...",
                    (
                        opt("the porosity of the soil"),
                        opt(
                            "groundwater flow direction - flow lines run perpendicular "
                            "to head contours, downgradient",
                            correct=True,
                        ),
                        opt("the chemical analytes present"),
                        opt("the age of the aquifer"),
                    ),
                    "Head contours reveal which way water - and any plume - will move.",
                ),
                q(
                    "Which set correctly names the three transport processes for a "
                    "dissolved plume?",
                    (
                        opt("Filtration, distillation, evaporation"),
                        opt(
                            "Advection (bulk carrying), dispersion (spreading and "
                            "dilution), and sorption (retardation of the front)",
                            correct=True,
                        ),
                        opt("Recharge, discharge, storage"),
                        opt("Aerobic, anaerobic, abiotic"),
                    ),
                    "Advection sets speed and direction, dispersion spreads, sorption "
                    "delays the front - the ADE combines them.",
                ),
                q(
                    "A retardation factor R = 1 + (rho_b/n_e)*Kd greater than 1 means...",
                    (
                        opt("the contaminant outruns the water"),
                        opt(
                            "the contaminant front is delayed, moving at v/R because it "
                            "partitions onto the solids",
                            correct=True,
                        ),
                        opt("there is no sorption"),
                        opt("the porosity is zero"),
                    ),
                    "Higher Kd or organic carbon means more sorption and a slower, "
                    "retarded front (v/R).",
                ),
                q(
                    "Why are DNAPLs especially problematic?",
                    (
                        opt("They float and evaporate away"),
                        opt(
                            "Being denser than water they sink and pool on aquitards, "
                            "acting as a long-term dissolving source",
                            correct=True,
                        ),
                        opt("They dissolve completely in minutes"),
                        opt("They cannot exist in groundwater"),
                    ),
                    "Dense non-aqueous phase liquids form persistent source zones that "
                    "feed plumes for years and are hard to remove.",
                ),
                q(
                    "For an exposure to be complete in a conceptual site model, you need...",
                    (
                        opt("only a source"),
                        opt(
                            "a source, a pathway, and a receptor all linked; break any "
                            "one and that route poses no risk",
                            correct=True,
                        ),
                        opt("only a receptor"),
                        opt("only a pathway"),
                    ),
                    "Source-pathway-receptor is the linkage risk-based remediation aims to break.",
                ),
                q(
                    "A Hazard Quotient HQ = CDI/RfD above 1 indicates...",
                    (
                        opt("no possible health effect"),
                        opt(
                            "the estimated intake exceeds the reference dose - a "
                            "potential non-cancer concern warranting action",
                            correct=True,
                        ),
                        opt("a one-in-a-million cancer risk"),
                        opt("the aquifer is confined"),
                    ),
                    "At or below 1 acceptable; above 1 flags a possible non-carcinogenic "
                    "concern (cancer risk uses CDI * slope factor instead).",
                ),
                q(
                    "The two goals of pump-and-treat are...",
                    (
                        opt("aeration and filtration"),
                        opt(
                            "hydraulic containment via a capture zone and mass removal "
                            "of contaminated water, though cleanup tails for years",
                            correct=True,
                        ),
                        opt("phytoextraction and harvesting"),
                        opt("sparging and venting"),
                    ),
                    "P&T contains and slowly removes but suffers tailing and rebound "
                    "from sorbed and NAPL mass.",
                ),
                q(
                    "Chlorinated solvents such as PCE and TCE are typically biodegraded by...",
                    (
                        opt("aerobic oxidation with added oxygen"),
                        opt(
                            "anaerobic reductive dechlorination driven by an electron "
                            "donor, stepping down to ethene",
                            correct=True,
                        ),
                        opt("photolysis in sunlight underground"),
                        opt("simple physical filtration"),
                    ),
                    "Petroleum (BTEX) degrades aerobically; chlorinated solvents need "
                    "anaerobic dechlorination - watch the vinyl chloride intermediate.",
                ),
                q(
                    "A permeable reactive barrier filled with zero-valent iron works by...",
                    (
                        opt("pumping water to an aboveground plant"),
                        opt(
                            "letting the plume flow through a stationary reactive wall "
                            "under its natural gradient, where ZVI dechlorinates "
                            "solvents and reduces metals in place",
                            correct=True,
                        ),
                        opt("heating the aquifer to boil contaminants off"),
                        opt("injecting plants into the aquifer"),
                    ),
                    "PRBs are passive in-situ treatment: no pumps, low energy, but they "
                    "must intercept the flow and can clog over time.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

HYDROGEOLOGY_REMEDIATION_COURSES: tuple[SeedCourse, ...] = (_HYDROGEOLOGY_REMEDIATION,)
