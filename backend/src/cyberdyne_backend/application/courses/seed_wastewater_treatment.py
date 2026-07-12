"""Academy seed content - Wastewater and Effluent Treatment.

An advanced tour of how domestic sewage and industrial effluents are
cleaned before returning to the environment: characterizing the load,
the preliminary/primary/secondary/tertiary treatment sequence, the main
biological reactors (activated sludge, biofilm, UASB, ponds), nutrient
removal, and what to do with the sludge that every process produces.
Every lesson is a direct explanation grounded in real practice and
standards (CONAMA, ABNT NBR, WHO/EPA), with a design calculation and a
mermaid diagram, followed by a checkpoint quiz; a comprehensive final
quiz closes the course.
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


_WASTEWATER_TREATMENT = SeedCourse(
    slug="wastewater-treatment",
    title="Wastewater & Effluent Treatment",
    description=(
        "Cleaning up sewage and industrial effluents from characterization "
        "through primary, secondary and tertiary treatment: activated sludge "
        "and biofilm reactors, anaerobic UASB reactors, stabilization ponds, "
        "nitrogen and phosphorus removal, and sludge management and reuse - "
        "with a worked design calculation and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Wastewater and Effluent Treatment

Every city and factory produces a dirty water stream that must be cleaned
before it can return to a river, the sea, or the soil. **Wastewater
treatment** is the engineered sequence that removes solids, organic
matter, nutrients and pathogens from that stream so the receiving
environment stays healthy and legal discharge standards (in Brazil,
**CONAMA 357 and 430**; ABNT NBR design norms) are met.

This is an **advanced** course: it assumes you are comfortable with mass
balances and basic reactor ideas, and it goes straight to the process
engineering. Every lesson explains one idea directly, shows a **worked
design calculation** (a loading rate, an efficiency, a reactor volume, a
sludge mass), and draws the process as a diagram. A short quiz follows
each lesson; a final quiz covers the whole course.

The path, in order:

1. **Wastewater characterization** - the numbers that describe the load
2. **Preliminary and primary treatment** - screens, grit, settling
3. **Activated sludge** - the workhorse suspended-growth reactor
4. **Biological filters and biofilm reactors** - attached growth
5. **Anaerobic reactors (UASB)** - treatment that produces biogas
6. **Stabilization ponds** - low-cost natural treatment
7. **Nutrient removal** - nitrogen and phosphorus
8. **Sludge treatment, reuse and industrial effluents** - closing the loop

By the end you will be able to read a wastewater analysis, pick a treatment
train for a given context, and size its main units at a preliminary level.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the fundamental purpose of wastewater treatment?",
                    (
                        opt("To make water taste better for drinking"),
                        opt(
                            "To remove solids, organic matter, nutrients and pathogens "
                            "so the effluent can be discharged safely and legally",
                            correct=True,
                        ),
                        opt("To generate electricity from rivers"),
                        opt("To desalinate seawater"),
                    ),
                    "Treatment protects the receiving water and meets discharge "
                    "standards such as CONAMA 430; drinking-water treatment is a "
                    "separate discipline.",
                ),
                q(
                    "Which regulatory framework sets effluent discharge standards in Brazil?",
                    (
                        opt("The US Clean Air Act"),
                        opt("CONAMA resolutions 357 and 430", correct=True),
                        opt("The IPCC guidelines"),
                        opt("ISO 9001"),
                    ),
                    "CONAMA 357 classifies water bodies and 430 sets discharge "
                    "conditions and standards for effluents in Brazil.",
                ),
            ),
        ),
        # -- 1. Characterization ---------------------------------------
        _t(
            "Wastewater characterization",
            "10 min",
            """# Wastewater characterization

Before you can treat wastewater you must **quantify** it. Two things
matter: the **flow** (how much, and how it varies over the day) and the
**concentration** of each contaminant. Multiply them and you get the
**load** - the mass of pollutant arriving per day, which is what governs
reactor sizing.

The key quality parameters:

- **BOD (Biochemical Oxygen Demand)** - the oxygen microbes consume to
  degrade the **biodegradable** organic matter. Typical raw domestic
  sewage is around 250 to 400 mg/L.
- **COD (Chemical Oxygen Demand)** - oxygen to chemically oxidize
  **all** organic matter. Always higher than BOD; the **COD/BOD ratio**
  tells you how biodegradable the effluent is (near 2 for domestic,
  much higher for many industrial wastes).
- **TSS (Total Suspended Solids)** - the particulate fraction removed by
  settling and filtration.
- **Nitrogen and phosphorus** - nutrients that cause **eutrophication**.
- **Coliforms** - indicator organisms for pathogen risk.

**Per capita contributions** let you estimate loads from population: in
Brazil a common value is about **54 g BOD per person per day** and roughly
**150 to 200 L of water per person per day**.

```text
Design example - load from a town of 20,000 people

Flow:  Q = 20,000 people x 160 L/person/day
         = 3,200,000 L/day = 3,200 m3/day

BOD load: L = 20,000 people x 54 g BOD/person/day
            = 1,080,000 g/day = 1,080 kg BOD/day

Check concentration:
  C = load / flow = 1,080 kg/day / 3,200 m3/day
    = 0.3375 kg/m3 = 337.5 mg/L   (typical domestic sewage)
```

```mermaid
graph LR
    FLOW["Flow in cubic meters per day"] --> LOAD["Pollutant load in kg per day"]
    CONC["Concentration in mg per L"] --> LOAD
    LOAD --> SIZE["Reactor and unit sizing"]
    POP["Population and per capita rates"] --> FLOW
    POP --> CONC
```

Remember: **load equals flow times concentration**. Get the
characterization right and every downstream design follows; get it wrong
and the plant is under or over built.
""",
        ),
        quiz_lesson(
            "Quiz: Wastewater characterization",
            (
                q(
                    "What is the difference between BOD and COD?",
                    (
                        opt("They are two names for the same test"),
                        opt(
                            "BOD is the oxygen to degrade only biodegradable organic "
                            "matter; COD is the oxygen to chemically oxidize all organic "
                            "matter, so COD is always higher",
                            correct=True,
                        ),
                        opt("BOD measures solids and COD measures nitrogen"),
                        opt("COD is always lower than BOD"),
                    ),
                    "COD >= BOD; the COD/BOD ratio indicates how biodegradable an effluent is.",
                ),
                q(
                    "A pollutant load in kg/day is calculated how?",
                    (
                        opt("Concentration divided by flow"),
                        opt("Flow times concentration, with consistent units", correct=True),
                        opt("Flow plus concentration"),
                        opt("Population divided by flow"),
                    ),
                    "Load = flow x concentration; it is the mass per day that drives "
                    "reactor sizing.",
                ),
                q(
                    "Why does a high COD/BOD ratio matter for treatment choice?",
                    (
                        opt("It means the effluent is highly biodegradable"),
                        opt(
                            "It signals a large non-biodegradable fraction, so purely "
                            "biological treatment may not be enough",
                            correct=True,
                        ),
                        opt("It has no effect on treatment"),
                        opt("It means there are no suspended solids"),
                    ),
                    "Domestic sewage has COD/BOD near 2; many industrial effluents are "
                    "far higher and may need physical-chemical steps.",
                ),
            ),
        ),
        # -- 2. Preliminary and primary --------------------------------
        _t(
            "Preliminary and primary treatment",
            "10 min",
            """# Preliminary and primary treatment

The first units protect the plant and remove the easy solids **before**
any biology. Two stages:

**Preliminary treatment** removes coarse and inorganic material that would
clog or wear equipment:

- **Bar screens (gradeamento)** - metal bars catch rags, plastics and
  debris. Spacing sets what passes: coarse (40 to 100 mm) down to fine
  (< 10 mm).
- **Grit chambers (desarenador)** - slow the flow so dense sand and grit
  settle out but lighter organics stay suspended. The classic design
  targets a horizontal velocity around **0.3 m/s**.

**Primary treatment** is **plain sedimentation** in a primary settling
tank: gravity pulls settleable solids down to form **primary sludge**,
while floating grease is skimmed off the top. No biology yet - just
physics.

A primary settler is sized by its **surface overloading rate** (surface
hydraulic loading), the flow divided by the tank surface area:

```text
Design example - primary settling tank

Given:  Q = 3,200 m3/day
Target surface loading (domestic): q_A = 40 m3 per m2 per day

Required surface area:
  A = Q / q_A = 3,200 / 40 = 80 m2

If circular:  A = pi/4 x D^2
  D = sqrt(4A / pi) = sqrt(4 x 80 / 3.1416)
    = sqrt(101.9) = about 10.1 m diameter

Expected removals in primary treatment:
  BOD:  25 to 40 percent
  TSS:  50 to 65 percent
```

```mermaid
graph LR
    RAW["Raw sewage"] --> SCR["Bar screen removes debris"]
    SCR --> GRIT["Grit chamber removes sand"]
    GRIT --> PST["Primary settler"]
    PST --> PSL["Primary sludge to handling"]
    PST --> EFF["Settled sewage to biology"]
```

Remember: preliminary and primary steps are cheap physical processes that
strip out grit and settleable solids, cutting the load and protecting the
biological stage that follows.
""",
        ),
        quiz_lesson(
            "Quiz: Preliminary and primary treatment",
            (
                q(
                    "What is the job of a grit chamber (desarenador)?",
                    (
                        opt("To remove dissolved organic matter"),
                        opt(
                            "To slow the flow so dense sand and grit settle while lighter "
                            "organics stay suspended",
                            correct=True,
                        ),
                        opt("To disinfect the effluent"),
                        opt("To add oxygen to the water"),
                    ),
                    "Grit removal protects pumps and later units from abrasion; it "
                    "targets inorganic sand, not organics.",
                ),
                q(
                    "Primary treatment removes pollutants by what mechanism?",
                    (
                        opt("Biological oxidation by bacteria"),
                        opt("Plain gravity sedimentation of settleable solids", correct=True),
                        opt("Chemical precipitation of phosphorus"),
                        opt("Membrane filtration"),
                    ),
                    "Primary settling is pure physics - no biology - producing primary "
                    "sludge and typically removing 25 to 40 percent of BOD.",
                ),
                q(
                    "A primary settling tank is sized principally from which parameter?",
                    (
                        opt("Its surface overloading (hydraulic loading) rate", correct=True),
                        opt("The influent nitrogen concentration"),
                        opt("The biogas production rate"),
                        opt("The chlorine dose"),
                    ),
                    "Area = flow / surface loading rate; for domestic sewage a value "
                    "near 40 m3 per m2 per day is common.",
                ),
            ),
        ),
        # -- 3. Activated sludge ---------------------------------------
        _t(
            "Activated sludge",
            "11 min",
            """# Activated sludge

**Activated sludge** is the most widely used secondary (biological)
process. It is a **suspended-growth** system: a dense mixed culture of
bacteria (the **biomass** or **MLSS - mixed liquor suspended solids**)
floats in an **aeration tank**, eating the dissolved organic matter while
air is blown in to supply oxygen. The mixture then flows to a **secondary
clarifier** where the biomass settles; most is **recycled** back to keep
the population high, and the surplus is wasted as **secondary sludge**.

Two control parameters define an activated-sludge design:

- **F/M ratio (food to microorganism)** - the BOD load divided by the
  mass of biomass. It sets how hard the bugs work.
- **Sludge age (theta_c, solids retention time)** - the average time
  biomass stays in the system. Longer sludge age gives more complete,
  more stable treatment and enables nitrification.

```text
Design example - aeration tank volume from sludge age

Given:
  Q = 3,200 m3/day            (flow)
  S0 = 300 mg/L BOD           (after primary removal)
  Se = 20 mg/L BOD            (target effluent)
  X  = 3,000 mg/L MLSS        (biomass in tank)
  Y  = 0.6 kg VSS per kg BOD  (yield)
  kd = 0.06 per day           (decay)
  theta_c = 10 days           (sludge age)

Volume (complete-mix, simplified):
  V = [theta_c x Q x Y x (S0 - Se)] / [X x (1 + kd x theta_c)]
    = [10 x 3,200 x 0.6 x (300 - 20) x 1e-3] / [3,000 x (1 + 0.06 x 10) x 1e-3]
    = [10 x 3,200 x 0.6 x 280 x 1e-3] / [3,000 x 1.6 x 1e-3]
    = 5,376 / 4.8 = 1,120 m3

Hydraulic retention time:
  HRT = V / Q = 1,120 / 3,200 = 0.35 day = about 8.4 hours
```

```mermaid
graph LR
    IN["Settled sewage"] --> AER["Aeration tank with biomass"]
    AIR["Blown air supplies oxygen"] --> AER
    AER --> CLAR["Secondary clarifier"]
    CLAR --> OUT["Clarified effluent"]
    CLAR --> RAS["Return sludge keeps biomass high"]
    RAS --> AER
    CLAR --> WAS["Waste surplus sludge"]
```

Remember: activated sludge keeps a hungry biomass in suspension, feeds it
oxygen and sewage, then settles and recycles it. F/M and sludge age are
the two knobs that tune everything.
""",
        ),
        quiz_lesson(
            "Quiz: Activated sludge",
            (
                q(
                    "Activated sludge is what kind of biological process?",
                    (
                        opt("Attached-growth on fixed media"),
                        opt(
                            "Suspended-growth: biomass floats in an aerated mixed liquor "
                            "and is settled and recycled",
                            correct=True,
                        ),
                        opt("Purely anaerobic with no oxygen"),
                        opt("A physical membrane process"),
                    ),
                    "The biomass (MLSS) is suspended in the aeration tank; the clarifier "
                    "settles it and returns most as RAS.",
                ),
                q(
                    "Why is sludge age (solids retention time) increased to achieve nitrification?",
                    (
                        opt(
                            "Nitrifiers grow slowly and are washed out at short sludge age",
                            correct=True,
                        ),
                        opt("Longer sludge age removes suspended solids only"),
                        opt("It reduces the aeration requirement"),
                        opt("Nitrifiers are unaffected by sludge age"),
                    ),
                    "Slow-growing nitrifying bacteria need a long enough solids "
                    "retention time to establish and stay in the system.",
                ),
                q(
                    "What is the role of return activated sludge (RAS)?",
                    (
                        opt("To dilute the influent"),
                        opt(
                            "To recycle settled biomass from the clarifier back to the "
                            "aeration tank, keeping the population high",
                            correct=True,
                        ),
                        opt("To add chemicals for phosphorus removal"),
                        opt("To disinfect the final effluent"),
                    ),
                    "Recycling biomass maintains a high MLSS; only the surplus is wasted "
                    "as secondary sludge.",
                ),
            ),
        ),
        # -- 4. Biofilm reactors ---------------------------------------
        _t(
            "Biological filters and biofilm reactors",
            "10 min",
            """# Biological filters and biofilm reactors

Instead of keeping biomass in suspension, **attached-growth** systems let
bacteria grow as a **biofilm** on a fixed or moving surface; the
wastewater flows past and the film does the work. Because the biomass
clings to media, it is not washed out, so these systems are robust to flow
swings and simple to operate.

The main types:

- **Trickling filter (filtro biologico percolador)** - wastewater is
  sprinkled over a bed of stone or plastic media; a biofilm grows on the
  media and air moves through the voids. Sized by **hydraulic** and
  **organic loading** rates.
- **RBC (rotating biological contactor)** - discs on a slow-turning shaft
  dip in and out of the wastewater, alternately absorbing substrate and
  oxygen.
- **MBBR (moving bed biofilm reactor)** - small plastic carriers float in
  an aerated tank, giving huge biofilm surface area in a compact volume.

The design driver is the **specific surface area** of the media: more
area means more biofilm means more treatment per cubic metre. That is why
plastic media (100 to 200 m2/m3, or far more for MBBR carriers) replaced
stone (about 40 to 70 m2/m3).

```text
Design example - trickling filter organic loading

Given:
  BOD load to filter = 700 kg BOD/day
  Filter media volume required at a loading of
    Lv = 0.5 kg BOD per m3 per day (low-rate stone filter)

Media volume:
  V = load / Lv = 700 / 0.5 = 1,400 m3

If depth H = 2.0 m, plan area:
  A = V / H = 1,400 / 2.0 = 700 m2
  Diameter D = sqrt(4A/pi) = sqrt(4 x 700 / 3.1416) = about 29.9 m
```

```mermaid
graph TD
    IN["Settled sewage sprinkled on top"] --> MEDIA["Media with biofilm"]
    AIR["Air flows through the voids"] --> MEDIA
    MEDIA --> BIO["Biofilm degrades organics"]
    BIO --> SLOUGH["Excess biofilm sloughs off"]
    SLOUGH --> CLAR["Secondary clarifier"]
    CLAR --> OUT["Treated effluent"]
```

Remember: biofilm reactors trade the aeration control of activated sludge
for the ruggedness of biomass that cannot wash away. Media surface area is
the parameter that governs their capacity.
""",
        ),
        quiz_lesson(
            "Quiz: Biological filters and biofilm reactors",
            (
                q(
                    "What distinguishes attached-growth (biofilm) systems from activated sludge?",
                    (
                        opt("They use no bacteria at all"),
                        opt(
                            "Bacteria grow as a biofilm on fixed or moving media rather "
                            "than suspended in the liquid, so they are not washed out",
                            correct=True,
                        ),
                        opt("They require no oxygen"),
                        opt("They only remove suspended solids"),
                    ),
                    "The biofilm clings to media, making the process robust to flow "
                    "variation and simpler to operate.",
                ),
                q(
                    "Why did plastic media largely replace stone in trickling filters?",
                    (
                        opt("Plastic is cheaper to mine"),
                        opt(
                            "Plastic offers a much higher specific surface area, so more "
                            "biofilm and more treatment fit in the same volume",
                            correct=True,
                        ),
                        opt("Stone dissolves in sewage"),
                        opt("Plastic removes the need for a clarifier"),
                    ),
                    "More surface area per cubic metre means more biofilm and higher "
                    "treatment capacity.",
                ),
                q(
                    "In an MBBR, where does the biomass live?",
                    (
                        opt("Dissolved uniformly in the water"),
                        opt(
                            "On small free-floating plastic carriers kept moving in the "
                            "aerated tank",
                            correct=True,
                        ),
                        opt("On slowly rotating discs on a shaft"),
                        opt("At the bottom as settled sludge only"),
                    ),
                    "MBBR carriers provide large biofilm area in a compact tank; "
                    "rotating discs describe an RBC instead.",
                ),
            ),
        ),
        # -- 5. UASB ---------------------------------------------------
        _t(
            "Anaerobic reactors (UASB)",
            "11 min",
            """# Anaerobic reactors (UASB)

**Anaerobic** treatment degrades organic matter **without oxygen**, and
its end product is **biogas** (mostly methane) - energy rather than a cost.
It also produces far **less sludge** than aerobic processes and needs no
aeration, which is why the **UASB (Upflow Anaerobic Sludge Blanket)**
reactor became a standard first stage for warm-climate sewage, especially
in Brazil.

How a UASB works: raw sewage enters at the **bottom** and flows **upward**
through a dense **blanket** of anaerobic sludge granules. The bugs convert
organics to biogas as the water rises. At the top a clever **three-phase
separator (GLS - gas, liquid, solid)** splits the biogas off, lets sludge
settle back down, and releases the clarified liquid.

Trade-offs versus aerobic: anaerobic treatment reaches lower BOD removal
(about 60 to 75 percent), so it is usually **followed by a polishing
step** (a trickling filter, pond, or activated sludge) to meet discharge
limits. But it slashes energy use and sludge output.

The design driver is the **volumetric organic loading rate** and the
**upflow velocity**:

```text
Design example - UASB volume and upflow velocity

Given:
  Q = 3,200 m3/day
  COD load = 1,600 kg COD/day
  Volumetric loading Lv = 3.0 kg COD per m3 per day (typical for sewage)

Reactor volume:
  V = load / Lv = 1,600 / 3.0 = about 533 m3

Hydraulic retention time:
  HRT = V / Q = 533 / 3,200 = 0.167 day = about 4 hours

Check upflow velocity (need <= ~1.0 m/h for sewage).
  If depth H = 4.5 m, plan area A = V / H = 533 / 4.5 = 118 m2
  v_up = Q / A = (3,200 / 24) / 118 = 133.3 / 118 = about 1.13 m/h
  -> slightly high, so increase area (reduce depth or add a reactor).
```

```mermaid
graph TD
    IN["Raw sewage enters at bottom"] --> BLANKET["Upflow through sludge blanket"]
    BLANKET --> GLS["Three phase separator at top"]
    GLS --> GAS["Biogas mostly methane"]
    GLS --> OUT["Clarified effluent to polishing"]
    GLS --> SETTLE["Sludge settles back down"]
    SETTLE --> BLANKET
```

Remember: UASB treats sewage anaerobically with little energy and little
sludge, recovering biogas - but its partial removal usually needs an
aerobic polishing stage to hit final standards.
""",
        ),
        quiz_lesson(
            "Quiz: Anaerobic reactors (UASB)",
            (
                q(
                    "What is a defining advantage of anaerobic (UASB) treatment over aerobic processes?",
                    (
                        opt("It achieves near 100 percent BOD removal alone"),
                        opt(
                            "It needs no aeration, produces far less sludge, and recovers "
                            "energy as biogas",
                            correct=True,
                        ),
                        opt("It requires no reactor at all"),
                        opt("It removes phosphorus completely"),
                    ),
                    "Anaerobic treatment saves energy and produces methane and little "
                    "sludge, but its removal is partial.",
                ),
                q(
                    "Why is a UASB usually followed by a polishing (post-treatment) step?",
                    (
                        opt("Because it produces too much oxygen"),
                        opt(
                            "Because its BOD removal of roughly 60 to 75 percent is often "
                            "not enough to meet discharge standards on its own",
                            correct=True,
                        ),
                        opt("Because the biogas must be re-treated"),
                        opt("Because it removes all nutrients but no organics"),
                    ),
                    "A trickling filter, pond or activated-sludge polishing stage brings "
                    "the effluent to standard.",
                ),
                q(
                    "What does the three-phase separator at the top of a UASB do?",
                    (
                        opt("It adds oxygen to the reactor"),
                        opt(
                            "It separates biogas, lets sludge settle back, and releases "
                            "the clarified liquid",
                            correct=True,
                        ),
                        opt("It pumps sewage into the reactor"),
                        opt("It disinfects the effluent with chlorine"),
                    ),
                    "The GLS separator is what keeps the sludge blanket in the reactor "
                    "while venting gas and passing treated water.",
                ),
            ),
        ),
        # -- 6. Stabilization ponds ------------------------------------
        _t(
            "Stabilization ponds",
            "10 min",
            """# Stabilization ponds

**Stabilization ponds (lagoas de estabilizacao)** are large, shallow
earthen basins that treat sewage using **natural processes** - sunlight,
algae, bacteria and long retention times - with almost no mechanical
equipment. They are cheap to build and run, tolerant of shock loads, and
excellent at removing pathogens, which makes them a great fit where land
is available and a warm climate drives the biology.

The common configurations, often in series:

- **Anaerobic pond** - deep (3 to 5 m), heavily loaded; settles solids
  and digests them anaerobically. Handles most of the BOD.
- **Facultative pond** - shallower (1.5 to 2 m); aerobic near the surface
  (algae release oxygen in sunlight) and anaerobic at the bottom. This
  **algae-bacteria symbiosis** is the heart of pond treatment.
- **Maturation pond** - shallow polishing pond whose job is **pathogen
  die-off** (sunlight, high pH, long retention) to meet coliform limits
  for reuse or discharge.

The design driver for a facultative pond is the **surface BOD loading
rate**, which depends on temperature:

```text
Design example - facultative pond area

Given:
  BOD load = 1,080 kg BOD/day = 1,080,000 g/day
  Surface loading (warm climate) Ls = 250 kg BOD per hectare per day
    = 25 g BOD per m2 per day

Required surface area:
  A = load / Ls = 1,080,000 g/day / 25 g per m2 per day
    = 43,200 m2 = 4.32 hectares

Check retention time at depth H = 1.8 m:
  V = A x H = 43,200 x 1.8 = 77,760 m3
  HRT = V / Q = 77,760 / 3,200 = about 24 days
```

```mermaid
graph LR
    IN["Raw sewage"] --> ANA["Anaerobic pond removes most BOD"]
    ANA --> FAC["Facultative pond algae and bacteria"]
    SUN["Sunlight drives algae oxygen"] --> FAC
    FAC --> MAT["Maturation pond kills pathogens"]
    MAT --> OUT["Effluent for reuse or discharge"]
```

Remember: ponds swap concrete and machines for land and time. The
algae-bacteria symbiosis in the facultative pond does the aerobic work,
and maturation ponds are the pathogen-removal champions.
""",
        ),
        quiz_lesson(
            "Quiz: Stabilization ponds",
            (
                q(
                    "What drives the aerobic treatment inside a facultative pond?",
                    (
                        opt("Mechanical surface aerators only"),
                        opt(
                            "An algae-bacteria symbiosis - algae release oxygen in "
                            "sunlight which bacteria use to degrade organics",
                            correct=True,
                        ),
                        opt("Injected pure oxygen"),
                        opt("Chemical oxidants dosed at the inlet"),
                    ),
                    "Photosynthetic algae supply the oxygen; the symbiosis is the heart "
                    "of pond treatment.",
                ),
                q(
                    "What is the primary purpose of a maturation pond?",
                    (
                        opt("To remove grit"),
                        opt("To generate biogas"),
                        opt(
                            "Pathogen die-off through sunlight, high pH and long "
                            "retention, meeting coliform limits",
                            correct=True,
                        ),
                        opt("To settle primary sludge"),
                    ),
                    "Maturation (polishing) ponds are the pathogen-removal stage for "
                    "safe reuse or discharge.",
                ),
                q(
                    "A facultative pond's area is sized principally from what?",
                    (
                        opt(
                            "Its surface BOD loading rate, which depends on temperature",
                            correct=True,
                        ),
                        opt("The biogas yield"),
                        opt("The chlorine dose"),
                        opt("The influent phosphorus concentration"),
                    ),
                    "Area = BOD load / surface loading rate; warmer climates allow "
                    "higher loading and smaller ponds.",
                ),
            ),
        ),
        # -- 7. Nutrient removal ---------------------------------------
        _t(
            "Nutrient removal (nitrogen and phosphorus)",
            "11 min",
            """# Nutrient removal (nitrogen and phosphorus)

Removing BOD is not enough when the receiving water is sensitive:
**nitrogen (N)** and **phosphorus (P)** are nutrients that cause
**eutrophication** - algal blooms that strip oxygen and kill aquatic life.
Advanced (tertiary) treatment targets them specifically.

**Nitrogen** is removed biologically in two linked steps:

- **Nitrification** - under **aerobic** conditions, slow-growing
  autotrophic bacteria oxidize ammonia to nitrate:
  ammonia -> nitrite -> nitrate. It needs oxygen and a long sludge age.
- **Denitrification** - under **anoxic** conditions (no free oxygen but
  nitrate present), heterotrophs use nitrate as their oxygen source and
  release it as **nitrogen gas** to the atmosphere. It needs a carbon
  source.

Plants combine these in configurations like the **MLE (Modified
Ludzack-Ettinger)** process: an **anoxic** zone first, then an **aerobic**
zone, with nitrate-rich mixed liquor recycled back to the anoxic zone.

**Phosphorus** is removed two ways, often together:

- **Chemical precipitation** - dose a metal salt (alum or ferric
  chloride); phosphate precipitates as an insoluble solid removed with the
  sludge.
- **Enhanced Biological Phosphorus Removal (EBPR)** - alternate anaerobic
  and aerobic zones select for **PAOs (phosphorus-accumulating
  organisms)** that take up P far beyond their normal need and carry it
  out in the wasted sludge.

```text
Design example - alum dose for phosphorus removal

Given:
  Q = 3,200 m3/day
  P to remove = 6 mg/L (from 8 down to 2 mg/L)
  Molar dose ratio (practical) = 1.5 mol Al per mol P

Molar masses:  P = 31 g/mol,  Al = 27 g/mol
Mass ratio Al:P needed = 1.5 x (27 / 31) = 1.31 g Al per g P

Aluminium required:
  = 1.31 x 6 mg/L x 3,200 m3/day
  = 1.31 x 6 x 3,200 g/day = 25,152 g/day = about 25 kg Al/day
```

```mermaid
graph LR
    IN["Influent with N and P"] --> ANOX["Anoxic zone denitrification"]
    ANOX --> AER["Aerobic zone nitrification"]
    AER --> REC["Nitrate recycle to anoxic zone"]
    REC --> ANOX
    AER --> CHEM["Dose metal salt for phosphorus"]
    CHEM --> OUT["Low nutrient effluent"]
```

Remember: nitrogen leaves as gas via nitrification then denitrification;
phosphorus leaves in the sludge via chemical precipitation or biological
uptake. Both protect the receiving water from eutrophication.
""",
        ),
        quiz_lesson(
            "Quiz: Nutrient removal (nitrogen and phosphorus)",
            (
                q(
                    "How is nitrogen ultimately removed from wastewater biologically?",
                    (
                        opt("It is precipitated as a solid with alum"),
                        opt(
                            "Nitrification oxidizes ammonia to nitrate aerobically, then "
                            "denitrification converts nitrate to nitrogen gas under anoxic "
                            "conditions",
                            correct=True,
                        ),
                        opt("It is filtered out by a membrane"),
                        opt("It settles as primary sludge"),
                    ),
                    "The two-step aerobic-then-anoxic sequence sends nitrogen off as "
                    "gas to the atmosphere.",
                ),
                q(
                    "What conditions does denitrification require?",
                    (
                        opt("Plenty of dissolved oxygen"),
                        opt(
                            "Anoxic conditions - no free oxygen but nitrate present - "
                            "plus a carbon source",
                            correct=True,
                        ),
                        opt("Strong sunlight"),
                        opt("A high chlorine residual"),
                    ),
                    "Denitrifiers use nitrate as their oxygen source only when free "
                    "oxygen is absent.",
                ),
                q(
                    "How does Enhanced Biological Phosphorus Removal (EBPR) work?",
                    (
                        opt("By dosing ferric chloride at the inlet"),
                        opt(
                            "Alternating anaerobic and aerobic zones select for PAOs that "
                            "take up excess phosphorus and carry it out in the wasted sludge",
                            correct=True,
                        ),
                        opt("By boiling off the phosphorus"),
                        opt("By nitrifying the phosphate"),
                    ),
                    "PAOs accumulate P beyond their metabolic need; wasting that biomass "
                    "removes the phosphorus. Chemical precipitation is the alternative.",
                ),
            ),
        ),
        # -- 8. Sludge and industrial effluents ------------------------
        _t(
            "Sludge treatment, reuse and industrial effluents",
            "11 min",
            """# Sludge treatment, reuse and industrial effluents

Every treatment process concentrates pollutants into a **sludge (lodo)**,
and managing it can be **half the cost** of running a plant. Raw sludge is
mostly water, unstable and pathogenic, so it is processed through a
standard chain:

- **Thickening (adensamento)** - concentrate the solids, removing free
  water to shrink downstream volumes.
- **Stabilization** - reduce the organic (volatile) content and pathogens,
  usually by **anaerobic digestion** (which also yields biogas) or aerobic
  digestion.
- **Conditioning and dewatering (desaguamento)** - drying beds,
  centrifuges or belt/filter presses turn liquid sludge into a spadeable
  cake.
- **Final disposal or reuse** - landfill, or beneficial reuse as
  agricultural **biosolids** where regulations allow. In Brazil, **CONAMA
  375** governs agricultural use of sewage sludge.

The mass of dry solids sets the size of every unit:

```text
Design example - sludge dry mass and cake volume

Given:
  Excess biosolids production = 0.8 kg TSS per kg BOD removed
  BOD removed = 1,000 kg/day

Dry solids mass:
  M = 0.8 x 1,000 = 800 kg dry solids/day

Cake volume after dewatering to 25 percent dry solids
  (cake density about 1,050 kg/m3):
  Wet cake mass = 800 / 0.25 = 3,200 kg/day
  Cake volume   = 3,200 / 1,050 = about 3.05 m3/day
```

**Industrial effluents** differ from domestic sewage: they can be very
concentrated, toxic (heavy metals, solvents), extreme in pH, or poorly
biodegradable (high COD/BOD). They often need tailored steps **before**
any biology - **equalization** to smooth flow and load, **neutralization**
of pH, **physical-chemical** coagulation/flocculation, and sometimes
**advanced oxidation** - and are frequently discharged to a public sewer
only after meeting pretreatment limits.

```mermaid
graph LR
    RAW["Raw sludge mostly water"] --> THICK["Thickening"]
    THICK --> DIG["Anaerobic digestion stabilizes"]
    DIG --> GAS["Biogas recovered"]
    DIG --> DEW["Dewatering to cake"]
    DEW --> REUSE["Biosolids reuse or disposal"]
```

Remember: treatment does not destroy pollutants, it concentrates them into
sludge that must be stabilized, dewatered and safely disposed of or
reused. Industrial effluents add pretreatment steps tuned to their
specific hazards.
""",
        ),
        quiz_lesson(
            "Quiz: Sludge treatment, reuse and industrial effluents",
            (
                q(
                    "Why is sludge management so important in a treatment plant?",
                    (
                        opt("Sludge is harmless and can be ignored"),
                        opt(
                            "Treatment concentrates pollutants into sludge that is bulky, "
                            "unstable and pathogenic, and handling it can be about half "
                            "the plant cost",
                            correct=True,
                        ),
                        opt("Sludge is the final clean effluent"),
                        opt("Sludge removes the need for disinfection"),
                    ),
                    "Pollutants are not destroyed but concentrated; the sludge must be "
                    "stabilized, dewatered and safely disposed of or reused.",
                ),
                q(
                    "What does anaerobic digestion do for sludge?",
                    (
                        opt("It adds water to the sludge"),
                        opt(
                            "It stabilizes the sludge by reducing volatile solids and "
                            "pathogens while producing biogas",
                            correct=True,
                        ),
                        opt("It disinfects the final effluent with chlorine"),
                        opt("It thickens the sludge only"),
                    ),
                    "Digestion is the stabilization step; anaerobic digestion also "
                    "yields energy as biogas.",
                ),
                q(
                    "Why do many industrial effluents need pretreatment before biological treatment?",
                    (
                        opt("Because they are always cleaner than sewage"),
                        opt(
                            "They can be toxic, extreme in pH, or poorly biodegradable, so "
                            "steps like equalization, neutralization and physical-chemical "
                            "treatment are needed first",
                            correct=True,
                        ),
                        opt("Because biology works better on toxic waste"),
                        opt("Because they contain no organic matter"),
                    ),
                    "Tailored pretreatment protects the biological stage and meets "
                    "pretreatment limits before discharge to a sewer or river.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "A pollutant load in kg/day equals what?",
                    (
                        opt("Concentration divided by flow"),
                        opt("Flow times concentration in consistent units", correct=True),
                        opt("Population times BOD concentration"),
                        opt("Flow minus concentration"),
                    ),
                    "Load = flow x concentration; it drives all downstream sizing.",
                ),
                q(
                    "Which statement about BOD and COD is correct?",
                    (
                        opt("BOD is always higher than COD"),
                        opt(
                            "COD is always greater than or equal to BOD, and the COD/BOD "
                            "ratio indicates biodegradability",
                            correct=True,
                        ),
                        opt("They measure suspended solids"),
                        opt("They are unrelated to organic matter"),
                    ),
                    "COD oxidizes all organics chemically; BOD only the biodegradable fraction.",
                ),
                q(
                    "Preliminary and primary treatment remove pollutants by what means?",
                    (
                        opt("Biological oxidation"),
                        opt(
                            "Physical processes - screening, grit removal and gravity "
                            "sedimentation - with no biology",
                            correct=True,
                        ),
                        opt("Chemical nitrification"),
                        opt("Membrane osmosis"),
                    ),
                    "These first stages are physical; biology begins at secondary treatment.",
                ),
                q(
                    "In activated sludge, what are the two key control parameters?",
                    (
                        opt("Chlorine dose and pH"),
                        opt("F/M ratio and sludge age (solids retention time)", correct=True),
                        opt("Biogas yield and cake dryness"),
                        opt("Pond depth and retention time"),
                    ),
                    "F/M sets how hard the biomass works; sludge age governs stability "
                    "and enables nitrification.",
                ),
                q(
                    "What is the main advantage of biofilm (attached-growth) reactors?",
                    (
                        opt("They need no bacteria"),
                        opt(
                            "Biomass grows on media and cannot wash out, so they are "
                            "robust to flow swings and simple to operate",
                            correct=True,
                        ),
                        opt("They remove all phosphorus automatically"),
                        opt("They require no clarifier or media"),
                    ),
                    "Media surface area governs their capacity; the biofilm stays put.",
                ),
                q(
                    "Why is a UASB reactor often followed by a polishing step?",
                    (
                        opt("It over-treats the sewage"),
                        opt(
                            "Its anaerobic BOD removal is partial (about 60 to 75 percent), "
                            "so a post-treatment is needed to meet standards",
                            correct=True,
                        ),
                        opt("It produces too much oxygen"),
                        opt("It removes only phosphorus"),
                    ),
                    "UASB saves energy and sludge but usually needs an aerobic polishing "
                    "stage to hit discharge limits.",
                ),
                q(
                    "What does the algae-bacteria symbiosis provide in a facultative pond?",
                    (
                        opt("Chemical coagulation"),
                        opt(
                            "Algae release oxygen by photosynthesis that bacteria use to "
                            "degrade organic matter",
                            correct=True,
                        ),
                        opt("Anaerobic digestion of solids"),
                        opt("Mechanical mixing"),
                    ),
                    "This natural oxygen supply is the heart of facultative pond "
                    "treatment; maturation ponds then remove pathogens.",
                ),
                q(
                    "How is nitrogen ultimately removed from wastewater?",
                    (
                        opt("Precipitated with alum as a solid"),
                        opt(
                            "Nitrified to nitrate aerobically, then denitrified to "
                            "nitrogen gas under anoxic conditions",
                            correct=True,
                        ),
                        opt("Settled as primary sludge"),
                        opt("Filtered by membranes"),
                    ),
                    "Aerobic nitrification then anoxic denitrification sends nitrogen off as gas.",
                ),
                q(
                    "Which pair correctly describes phosphorus removal routes?",
                    (
                        opt("Nitrification and denitrification"),
                        opt(
                            "Chemical precipitation with a metal salt, and Enhanced "
                            "Biological Phosphorus Removal via PAOs",
                            correct=True,
                        ),
                        opt("Screening and grit removal"),
                        opt("Aeration and clarification only"),
                    ),
                    "Phosphorus leaves in the sludge, either precipitated chemically or "
                    "taken up biologically by PAOs.",
                ),
                q(
                    "What is the correct sequence of a typical sludge handling chain?",
                    (
                        opt("Disinfection, then aeration, then screening"),
                        opt(
                            "Thickening, stabilization (digestion), dewatering, then final "
                            "disposal or reuse as biosolids",
                            correct=True,
                        ),
                        opt("Chlorination, then settling, then flotation"),
                        opt("Denitrification, then grit removal"),
                    ),
                    "Concentrate, stabilize, dewater, dispose or reuse - treatment "
                    "concentrates pollutants into sludge that must be managed.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

WASTEWATER_TREATMENT_COURSES: tuple[SeedCourse, ...] = (_WASTEWATER_TREATMENT,)
