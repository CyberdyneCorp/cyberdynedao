"""Academy seed content - Solid Waste Management and Landfills.

Managing society's discards from generation to final disposal: classifying
and characterizing waste, collecting and transporting it, recovering value
through recycling and composting, engineering a sanitary landfill, controlling
its leachate and biogas, handling hazardous and healthcare streams, and closing
material loops through the circular economy and reverse logistics. Every lesson
is a direct explanation grounded in ABNT NBR, CONAMA and PNRS practice with a
worked calculation and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz.
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


_SOLID_WASTE_MANAGEMENT = SeedCourse(
    slug="solid-waste-management",
    title="Solid Waste Management & Landfills",
    description=(
        "Managing society's discards, end to end: classification and "
        "gravimetric characterization, collection and transport, recycling and "
        "composting, sanitary landfill design, leachate and biogas control, "
        "hazardous and healthcare waste, and the circular economy - grounded in "
        "ABNT NBR, CONAMA and PNRS practice with a worked calculation and a "
        "diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Solid Waste Management and Landfills

Every city produces a river of discarded material every day, and where it
goes - a dump, a recycling line, a compost windrow, or an engineered
landfill - decides whether it becomes pollution or resource. **Solid waste
management** is the engineering and planning discipline that moves those
discards from the point of generation to a safe final destination while
recovering as much value as possible along the way.

This course follows waste from bin to final disposal. The approach is
**concrete**: every lesson explains one stage directly, works a real
calculation (a mass balance, a fleet sizing, a landfill volume, a biogas
estimate), and draws the idea as a diagram. After each lesson there is a
short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Waste classification and gravimetric characterization** - what is in
   the waste and how we measure it
2. **Collection and transport** - moving waste efficiently
3. **Recycling and material recovery** - pulling value back out
4. **Composting and anaerobic digestion** - treating the organic fraction
5. **Sanitary landfill design** - engineering safe final disposal
6. **Leachate and biogas management** - controlling what a landfill emits
7. **Hazardous and healthcare waste** - the streams that need special care
8. **The circular economy and reverse logistics** - closing material loops

Throughout we lean on real standards - Brazil's **PNRS** (Lei 12.305/2010),
**ABNT NBR** 10004 and 13896, **CONAMA** resolutions, and international
references like the **EPA** and the **waste hierarchy** - kept teachable.
By the end you will see municipal solid waste not as garbage but as a
managed system with measurable flows.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the scope of solid waste management as this course frames it?",
                    (
                        opt("Only the design of landfills"),
                        opt("Only household recycling programs"),
                        opt(
                            "Moving discards from the point of generation to a safe final "
                            "destination while recovering as much value as possible",
                            correct=True,
                        ),
                        opt("Only the collection trucks"),
                    ),
                    "It is a whole system - generation, collection, recovery, treatment "
                    "and disposal - not any single stage.",
                ),
                q(
                    "Which framework of national law grounds much of this course in Brazil?",
                    (
                        opt(
                            "The PNRS - National Solid Waste Policy (Lei 12.305/2010)", correct=True
                        ),
                        opt("The Kyoto Protocol"),
                        opt("The Basel Convention alone"),
                        opt("The building code"),
                    ),
                    "The Politica Nacional de Residuos Solidos sets the shared-"
                    "responsibility and waste-hierarchy framework used throughout.",
                ),
            ),
        ),
        # -- 1. Classification and characterization --------------------
        _t(
            "Waste classification and gravimetric characterization",
            "10 min",
            """# Waste classification and gravimetric characterization

Before you can manage waste you must know **what it is** and **how much of
each kind** there is. Two complementary ideas do this: **classification**
(what hazard class and origin a waste belongs to) and **gravimetric
characterization** (the measured composition by weight).

**Classification** in Brazil follows **ABNT NBR 10004**, which sorts solid
waste by the risk it poses:

- **Class I - hazardous** - flammable, corrosive, reactive, toxic or
  pathogenic (solvents, batteries, some healthcare waste).
- **Class II A - non-inert** - can biodegrade, burn or dissolve in water
  (most organic and mixed municipal waste).
- **Class II B - inert** - does not leach significant contaminants (clean
  construction rubble, some glass).

Waste is also grouped by **origin**: municipal solid waste (MSW),
construction and demolition, industrial, healthcare, and special streams.

**Gravimetric characterization** samples the actual waste and sorts it into
categories - organics, paper, plastic, glass, metal, rejects - then weighs
each. A typical Brazilian MSW profile is dominated by the **organic
fraction** (about half by weight), which is why composting matters so much.

```text
Gravimetric composition (worked example, 200 kg sample)
  Organic (food, yard):   102 kg  ->  51 percent
  Paper and cardboard:     26 kg  ->  13 percent
  Plastic:                 34 kg  ->  17 percent
  Glass:                   06 kg  ->   3 percent
  Metal:                   06 kg  ->   3 percent
  Rejects and other:       26 kg  ->  13 percent
  Total:                  200 kg  -> 100 percent

Percent of a fraction = (mass of fraction / total mass) x 100
Organic: (102 / 200) x 100 = 51 percent
```

Two more numbers drive every downstream design decision:

- **Per-capita generation** - kg per person per day (often 0.8 to 1.2 in
  Brazilian cities). Total daily mass = per-capita x population.
- **Apparent density** - loose MSW is roughly 200 to 250 kg per cubic
  metre; this sets truck and landfill volumes.

```mermaid
graph TD
    SAMPLE["Representative waste sample"] --> SORT["Sort into categories"]
    SORT --> WEIGH["Weigh each category"]
    WEIGH --> PERCENT["Percent by mass"]
    PERCENT --> DESIGN["Feeds design decisions"]
    CLASS["NBR 10004 class"] --> DESIGN
```

Remember: classification tells you the **hazard and handling**;
characterization tells you the **quantities**. Together they turn "garbage"
into numbers you can engineer around.
""",
        ),
        quiz_lesson(
            "Quiz: Waste classification and gravimetric characterization",
            (
                q(
                    "Under ABNT NBR 10004, what is a Class I waste?",
                    (
                        opt("Inert waste that does not leach contaminants"),
                        opt(
                            "Hazardous waste - flammable, corrosive, reactive, toxic or pathogenic",
                            correct=True,
                        ),
                        opt("Any household organic waste"),
                        opt("Clean construction rubble"),
                    ),
                    "Class I is hazardous; Class II A is non-inert, Class II B is inert.",
                ),
                q(
                    "What does gravimetric characterization measure?",
                    (
                        opt("The hazard class only"),
                        opt("The chemical formula of each item"),
                        opt(
                            "The composition of the waste by weight, sorting a sample into "
                            "categories and weighing each",
                            correct=True,
                        ),
                        opt("The truck routing schedule"),
                    ),
                    "It is a percent-by-mass profile of a representative sample.",
                ),
                q(
                    "A city of 300000 people generates 0.9 kg per person per day. What is "
                    "the daily MSW mass?",
                    (
                        opt("270 tonnes per day", correct=True),
                        opt("27 tonnes per day"),
                        opt("2700 tonnes per day"),
                        opt("90 tonnes per day"),
                    ),
                    "300000 x 0.9 = 270000 kg per day = 270 tonnes per day.",
                ),
            ),
        ),
        # -- 2. Collection and transport -------------------------------
        _t(
            "Collection and transport",
            "10 min",
            """# Collection and transport

**Collection** is the most visible - and usually the most expensive - part
of the system, often 50 to 70 percent of total cost. The engineering task
is to move a known daily mass of waste from thousands of generation points
to a treatment or disposal site with the fewest trucks, kilometres and
hours.

The core decisions:

- **Collection frequency** - how often each route is served (daily for
  dense organic-rich areas, less for recyclables).
- **Vehicle type** - **compactor trucks** (a compaction ratio of about 3:1
  raises payload density from ~200 to ~600 kg per cubic metre), skip
  loaders, or side-loaders.
- **Route design** - minimise deadheading (driving without collecting);
  heuristics turn streets into an efficient path, an "arc routing" problem.
- **Transfer stations** - when the disposal site is far, small collection
  trucks tip into large transfer trailers so the long haul moves more mass
  per trip, cutting cost and emissions.

Sizing a fleet is a mass-and-time balance. You need the daily mass, the
effective truck payload, and how many trips a truck can make in a shift:

```text
Fleet sizing (worked example)
  Daily waste to collect:        270 t/day
  Compactor effective payload:   10 t per trip
  Trips per truck per shift:     3
  Truck capacity per day = 10 t x 3 = 30 t/day

  Trucks needed = daily waste / capacity per truck
                = 270 / 30 = 9 trucks
  Add ~15 percent spare for maintenance -> round up to 11 trucks
```

```mermaid
graph LR
    GEN["Generation points"] --> COLLECT["Compactor collection route"]
    COLLECT --> TS["Transfer station"]
    TS --> HAUL["Long haul trailer"]
    HAUL --> DEST["Treatment or landfill"]
    COLLECT -->|"short haul"| DEST
```

Remember: collection is where most of the money goes, so small gains in
route efficiency, compaction and transfer logistics dominate the economics
of the whole system.
""",
        ),
        quiz_lesson(
            "Quiz: Collection and transport",
            (
                q(
                    "Why is a transfer station used?",
                    (
                        opt("To burn the waste"),
                        opt(
                            "To consolidate small collection loads into large trailers so "
                            "the long haul to a distant site moves more mass per trip",
                            correct=True,
                        ),
                        opt("To classify waste by hazard"),
                        opt("To generate biogas"),
                    ),
                    "Transfer stations cut long-haul cost and emissions when disposal is "
                    "far from collection.",
                ),
                q(
                    "What does a compactor truck's roughly 3:1 compaction ratio achieve?",
                    (
                        opt("It shreds the waste into powder"),
                        opt(
                            "It raises the payload density, so each trip carries far more mass",
                            correct=True,
                        ),
                        opt("It removes hazardous waste automatically"),
                        opt("It composts the organic fraction en route"),
                    ),
                    "Higher density means more tonnes per trip and fewer trips.",
                ),
                q(
                    "A city collects 270 t/day; each truck manages 30 t/day. Ignoring "
                    "spares, how many trucks are needed?",
                    (
                        opt("3"),
                        opt("9", correct=True),
                        opt("27"),
                        opt("90"),
                    ),
                    "270 / 30 = 9 trucks; a spare margin then rounds the fleet up.",
                ),
            ),
        ),
        # -- 3. Recycling and material recovery ------------------------
        _t(
            "Recycling and material recovery",
            "10 min",
            """# Recycling and material recovery

**Recycling** returns discarded materials to production as feedstock,
saving raw resources and landfill space. It sits high in the **waste
hierarchy** (reduce, reuse, recycle, recover energy, dispose), and in
Brazil it is a legal duty under the PNRS and organised largely through
**selective collection** (coleta seletiva) and cooperatives of waste
pickers (catadores).

Two collection models feed recovery:

- **Source separation** - generators split recyclables (dry) from organics
  and rejects (wet). Cleaner streams, higher-value output.
- **Mixed collection with a MRF** - a **Materials Recovery Facility** sorts
  a commingled stream mechanically and manually.

Inside a MRF the stream is separated by physical property:

- **Trommel screen** - separates by size.
- **Magnetic separator** - pulls out ferrous metals.
- **Eddy-current separator** - repels non-ferrous metals (aluminium).
- **Optical sorters** - identify plastics by resin type (PET, HDPE...).
- **Manual picking** - final quality control.

The key performance number is the **recovery rate** - how much of the
material actually entering recovery comes out as usable product, versus
lost to residue and contamination:

```python
# Recovery efficiency through a MRF line
recyclables_in = 34_000      # kg of plastic delivered to the MRF
recovered = 27_200           # kg baled as clean product
residue = recyclables_in - recovered

recovery_rate = recovered / recyclables_in * 100
print(f"Recovery rate: {recovery_rate:.1f} percent")   # 80.0 percent
print(f"Residue to landfill: {residue} kg")            # 6800 kg

# Diversion rate for the whole city
msw_total = 270_000          # kg/day
diverted = 95_000            # kg/day recycled + composted
print(f"Diversion: {diverted / msw_total * 100:.1f} percent")  # 35.2 percent
```

```mermaid
graph LR
    IN["Commingled recyclables"] --> TROMMEL["Trommel size screen"]
    TROMMEL --> MAGNET["Magnet ferrous metal"]
    MAGNET --> EDDY["Eddy current aluminium"]
    EDDY --> OPTICAL["Optical plastic sorting"]
    OPTICAL --> PICK["Manual quality picking"]
    PICK --> BALE["Baled product to market"]
```

Remember: recycling only counts what is **recovered clean and sold**.
Contamination is the enemy - a load of recyclables spoiled by food waste
can end up in the landfill anyway, which is why source separation matters.
""",
        ),
        quiz_lesson(
            "Quiz: Recycling and material recovery",
            (
                q(
                    "What does a MRF (Materials Recovery Facility) do?",
                    (
                        opt("Buries waste in engineered cells"),
                        opt(
                            "Sorts a mixed recyclable stream by physical property - size, "
                            "magnetism, resin type - into marketable materials",
                            correct=True,
                        ),
                        opt("Produces compost from organics"),
                        opt("Incinerates hazardous waste"),
                    ),
                    "A MRF uses trommels, magnets, eddy-current and optical sorters plus "
                    "manual picking.",
                ),
                q(
                    "Which device separates aluminium (a non-ferrous metal) in a MRF?",
                    (
                        opt("A magnetic separator"),
                        opt("An eddy-current separator", correct=True),
                        opt("A trommel screen"),
                        opt("An anaerobic digester"),
                    ),
                    "Magnets grab ferrous metal; eddy-current separators repel non-ferrous "
                    "metals like aluminium.",
                ),
                q(
                    "A MRF receives 34000 kg of plastic and bales 27200 kg. What is the "
                    "recovery rate?",
                    (
                        opt("80 percent", correct=True),
                        opt("20 percent"),
                        opt("68 percent"),
                        opt("120 percent"),
                    ),
                    "27200 / 34000 x 100 = 80 percent; the rest is residue and contamination.",
                ),
            ),
        ),
        # -- 4. Composting and anaerobic digestion ---------------------
        _t(
            "Composting and anaerobic digestion",
            "10 min",
            """# Composting and anaerobic digestion

Since roughly half of Brazilian MSW is **organic**, treating that fraction
biologically is the single biggest lever for diverting waste from landfill.
Two processes do it, distinguished by whether oxygen is present.

**Composting** is **aerobic** (with oxygen): microbes oxidise organic
matter into a stable, humus-like soil amendment, releasing CO2, water and
heat. Good compost depends on four controls:

- **C/N ratio** - carbon to nitrogen, ideally about **25:1 to 30:1**. Too
  much nitrogen (green material) smells of ammonia; too much carbon (brown
  material) composts slowly.
- **Moisture** - about 50 to 60 percent.
- **Oxygen** - turning windrows or forced aeration keeps it aerobic.
- **Temperature** - the thermophilic phase reaches 55 to 65 C, which
  sanitises the material (kills pathogens and weed seeds).

**Anaerobic digestion** is **without oxygen**: microbes break organics down
into **biogas** (about 50 to 65 percent methane) plus a nutrient-rich
**digestate**. It captures energy the compost pile would lose as heat, and
suits wet, high-nitrogen feedstocks (food waste, manure).

Blending feedstocks to hit the target C/N ratio is a classic mass balance:

```text
Blending to a target C/N ratio
  Food waste:   C/N = 15,  60 kg,  N-content basis
  Dry leaves:   C/N = 50,  40 kg

  Weighted C/N of the mix (mass-weighted approximation):
    (15 x 60 + 50 x 40) / (60 + 40)
  = (900 + 2000) / 100
  = 2900 / 100
  = 29  ->  within the ideal 25 to 30 band

Add more leaves to raise C/N, more food waste to lower it.
```

```mermaid
graph TD
    ORG["Organic fraction"] --> ROUTE{"Oxygen present"}
    ROUTE -->|"yes aerobic"| COMPOST["Composting windrow"]
    ROUTE -->|"no anaerobic"| DIGEST["Anaerobic digester"]
    COMPOST --> HUMUS["Stable compost soil amendment"]
    DIGEST --> BIOGAS["Biogas for energy"]
    DIGEST --> DIGESTATE["Nutrient rich digestate"]
```

Remember: **compost with air** to make a soil product; **digest without
air** to also capture energy as biogas. Either way, keeping organics out of
the landfill cuts both volume and the methane a landfill would emit.
""",
        ),
        quiz_lesson(
            "Quiz: Composting and anaerobic digestion",
            (
                q(
                    "What is the key difference between composting and anaerobic digestion?",
                    (
                        opt("Composting uses machines, digestion uses hands"),
                        opt(
                            "Composting is aerobic (with oxygen) and yields a soil "
                            "amendment; anaerobic digestion is without oxygen and yields "
                            "biogas plus digestate",
                            correct=True,
                        ),
                        opt("Composting produces methane, digestion produces CO2 only"),
                        opt("They are the same process"),
                    ),
                    "Oxygen present -> compost; oxygen absent -> biogas and digestate.",
                ),
                q(
                    "Why is the C/N ratio (about 25:1 to 30:1) important in composting?",
                    (
                        opt("It sets the truck routing"),
                        opt(
                            "It balances the microbial diet - too much nitrogen smells of "
                            "ammonia, too much carbon composts slowly",
                            correct=True,
                        ),
                        opt("It determines the hazard class"),
                        opt("It has no effect on compost quality"),
                    ),
                    "Carbon-to-nitrogen balance drives microbial activity and odour.",
                ),
                q(
                    "Blending 60 kg of food waste (C/N 15) with 40 kg of leaves (C/N 50) "
                    "gives an approximate mix C/N of:",
                    (
                        opt("15"),
                        opt("29", correct=True),
                        opt("50"),
                        opt("65"),
                    ),
                    "(15 x 60 + 50 x 40) / 100 = 2900 / 100 = 29, inside the ideal band.",
                ),
            ),
        ),
        # -- 5. Sanitary landfill design -------------------------------
        _t(
            "Sanitary landfill design",
            "11 min",
            """# Sanitary landfill design

Whatever cannot be recovered or treated needs safe **final disposal**. A
**sanitary landfill** (aterro sanitario) is an engineered facility - not a
dump (lixao) - designed to isolate waste from the environment. In Brazil
the PNRS made open dumps illegal, and **ABNT NBR 13896** and **NBR 15849**
set siting and design criteria.

The engineered barrier is built bottom-up in layers:

- **Liner system** - a low-permeability barrier (compacted clay with
  permeability below 10^-9 m/s, usually plus a **geomembrane** such as
  HDPE) that stops **leachate** from reaching groundwater.
- **Leachate collection** - a drainage layer and perforated pipes above the
  liner gather leachate to a sump for treatment.
- **Waste cells** - waste is placed in daily **cells**, compacted, and
  covered with soil (**daily cover**) to control odour, vectors and litter.
- **Gas collection** - vertical and horizontal wells draw off landfill gas
  (biogas) as the buried organics decompose.
- **Final cap** - when a cell is full, a capping system (clay/geomembrane
  plus drainage and topsoil) sheds rainwater and supports revegetation.

Siting avoids aquifer recharge zones, floodplains, and proximity to homes,
and keeps a buffer above the water table.

The number that decides a landfill's economics is its **airspace lifespan** -
how many years of waste the permitted volume will hold:

```text
Landfill lifespan (worked example)
  Available airspace volume:      2_000_000 m3
  Compacted waste density:              800 kg/m3
  Cover soil overhead:            ~20 percent of volume

  Usable volume for waste = 2_000_000 x 0.80 = 1_600_000 m3
  Waste mass capacity     = 1_600_000 x 800  = 1_280_000_000 kg
                          = 1_280_000 tonnes

  Annual waste received   = 270 t/day x 365   ~ 98_550 t/year

  Lifespan = 1_280_000 / 98_550 ~ 13 years
```

```mermaid
graph TD
    WASTE["Compacted waste cell"] --> COVER["Daily soil cover"]
    RAIN["Rainfall"] --> LEACHATE["Leachate percolates down"]
    LEACHATE --> DRAIN["Leachate collection layer"]
    DRAIN --> LINER["Clay and geomembrane liner"]
    LINER --> PROTECT["Groundwater protected"]
    WASTE --> GAS["Gas collection wells"]
```

Remember: a sanitary landfill is a **containment system** - liner and
leachate collection below, gas collection and a cap above - engineered so
that decomposing waste never contaminates soil, water or air. Airspace is
finite, which is why every tonne diverted upstream extends its life.
""",
        ),
        quiz_lesson(
            "Quiz: Sanitary landfill design",
            (
                q(
                    "What distinguishes a sanitary landfill from an open dump (lixao)?",
                    (
                        opt("Nothing, they are the same"),
                        opt(
                            "A sanitary landfill is engineered with a liner, leachate and "
                            "gas collection and daily cover to isolate waste from the "
                            "environment",
                            correct=True,
                        ),
                        opt("A dump is more expensive to build"),
                        opt("A sanitary landfill has no cover soil"),
                    ),
                    "Containment engineering - liner, leachate collection, gas wells, "
                    "cover - is the whole difference; the PNRS banned open dumps.",
                ),
                q(
                    "What is the purpose of the liner system at the base of a landfill?",
                    (
                        opt("To generate electricity"),
                        opt("To speed up decomposition"),
                        opt(
                            "A low-permeability barrier (compacted clay plus geomembrane) "
                            "that stops leachate from reaching groundwater",
                            correct=True,
                        ),
                        opt("To compact the waste"),
                    ),
                    "Clay below ~10^-9 m/s permeability plus an HDPE geomembrane isolates "
                    "leachate from the aquifer.",
                ),
                q(
                    "A landfill has 1280000 tonnes of usable capacity and receives about "
                    "98550 tonnes per year. Its lifespan is roughly:",
                    (
                        opt("1 year"),
                        opt("13 years", correct=True),
                        opt("50 years"),
                        opt("130 years"),
                    ),
                    "1280000 / 98550 is about 13 years; diverting waste upstream extends it.",
                ),
            ),
        ),
        # -- 6. Leachate and biogas management -------------------------
        _t(
            "Leachate and biogas management",
            "11 min",
            """# Leachate and biogas management

A landfill is a slow biological reactor, and it produces two things that
must be captured and treated: **leachate** (contaminated liquid) and
**landfill gas** (biogas).

**Leachate** (chorume) forms when rainwater percolates through the waste,
dissolving and carrying contaminants. It is a difficult effluent: very high
**BOD** and **COD**, ammonia nitrogen, salts and heavy metals. Its
character changes with age - young landfills give acidic, high-BOD leachate;
old ones give lower-BOD, high-ammonia leachate. Treatment therefore
combines steps: **biological** (aerated lagoons, activated sludge, or
recirculation back through the waste), **physico-chemical** (coagulation,
air stripping for ammonia), and often **membranes** (reverse osmosis) for
polishing before discharge, which must meet **CONAMA 430** limits.

A water balance predicts how much leachate to expect - the rain that
infiltrates minus what runs off or evaporates:

```text
Leachate generation (rational / water-balance estimate)
  Percolation P = C x I x A
    C = infiltration coefficient (fraction reaching waste), 0.30
    I = rainfall intensity, 1200 mm/year = 1.2 m/year
    A = open landfill area, 50_000 m2

  P = 0.30 x 1.2 x 50_000 = 18_000 m3/year
    ~ 49 m3/day of leachate to collect and treat

Reducing exposed area (capping, good drainage) shrinks C x A and so P.
```

**Landfill gas** is produced as the buried organic fraction decomposes
anaerobically. It is roughly **half methane (CH4) and half CO2**. Methane
is a potent greenhouse gas - about **28 times** the warming potential of
CO2 over 100 years (IPCC) - so it must not simply escape. Options, best
first:

- **Energy recovery** - collect the gas and burn it in engines or turbines
  for electricity (a landfill-gas-to-energy project, often a carbon-credit
  earner).
- **Flaring** - if energy use is not viable, flare it: burning CH4 to CO2
  cuts the climate impact roughly 28-fold.
- **Never vent raw** - releasing methane directly is the worst option.

```mermaid
graph TD
    WASTE["Decomposing waste"] --> LEACH["Leachate liquid"]
    WASTE --> GAS["Landfill gas methane and CO2"]
    LEACH --> BIO["Biological treatment"]
    BIO --> MEMB["Membrane polishing"]
    MEMB --> DISCHARGE["Discharge within CONAMA limits"]
    GAS --> ENERGY["Energy recovery engines"]
    GAS --> FLARE["Flare if no energy use"]
```

Remember: a landfill keeps working for decades after it closes. Capturing
and treating its **leachate** protects water; capturing its **methane** for
energy or flaring protects the climate - both are required, not optional.
""",
        ),
        quiz_lesson(
            "Quiz: Leachate and biogas management",
            (
                q(
                    "What is leachate (chorume) and why is it hard to treat?",
                    (
                        opt("Clean rainwater runoff, easily discharged"),
                        opt(
                            "Contaminated liquid from rain percolating through waste, with "
                            "very high BOD/COD, ammonia and heavy metals",
                            correct=True,
                        ),
                        opt("The gas produced by decomposition"),
                        opt("Compost tea sold as fertiliser"),
                    ),
                    "High organic load plus ammonia and metals - and its character shifts "
                    "as the landfill ages - so treatment combines several steps.",
                ),
                q(
                    "Landfill gas is about half methane. Why must it be captured and "
                    "burned rather than vented?",
                    (
                        opt("Methane smells bad but is otherwise harmless"),
                        opt(
                            "Methane is a potent greenhouse gas (about 28x CO2 over 100 "
                            "years); flaring or energy recovery cuts its climate impact",
                            correct=True,
                        ),
                        opt("Venting is illegal only for CO2"),
                        opt("It has no environmental effect either way"),
                    ),
                    "Burning CH4 to CO2 reduces warming potential dramatically; energy "
                    "recovery is best, flaring second, venting worst.",
                ),
                q(
                    "With C = 0.30, I = 1.2 m/year and A = 50000 m2, the estimated "
                    "leachate generation P = C x I x A is:",
                    (
                        opt("1800 m3/year"),
                        opt("18000 m3/year", correct=True),
                        opt("180000 m3/year"),
                        opt("50000 m3/year"),
                    ),
                    "0.30 x 1.2 x 50000 = 18000 m3/year, about 49 m3/day.",
                ),
            ),
        ),
        # -- 7. Hazardous and healthcare waste -------------------------
        _t(
            "Hazardous and healthcare waste",
            "10 min",
            """# Hazardous and healthcare waste

Some streams are too dangerous for the ordinary MSW system and need
dedicated handling. Two families dominate: **industrial hazardous waste**
and **healthcare (medical) waste**.

**Hazardous waste** is the **Class I** of ABNT NBR 10004 - waste that is
flammable, corrosive, reactive, toxic or pathogenic. It must be segregated
at source, labelled, and tracked with a **manifest** (documentation
following the waste from generator to final destination) so it can never be
"lost" into the environment. International movement is governed by the
**Basel Convention**. Treatment routes include:

- **Incineration** at high temperature for organic toxics (destroys the
  hazard; requires strict air-pollution control).
- **Physico-chemical treatment** (neutralisation, precipitation) for
  corrosives and metal-bearing liquids.
- **Stabilisation and solidification**, then disposal in a dedicated
  **Class I secure landfill** with a double liner.

**Healthcare waste** (residuos de servicos de saude, RSS) is regulated in
Brazil by **CONAMA 358** and **ANVISA RDC 222**, which sort it into groups:

- **Group A - infectious/biological** (cultures, contaminated materials) -
  treated to sterilise, typically by **autoclaving** (steam) before
  disposal.
- **Group B - chemical** (drugs, reagents) - treated like hazardous waste.
- **Group C - radioactive** - held for decay under nuclear rules.
- **Group D - common** (non-contaminated) - ordinary MSW route.
- **Group E - sharps** (needles, blades) - rigid puncture-proof containers.

Segregation at the point of generation is the golden rule: mixing a small
infectious fraction into general waste contaminates the whole load.

```python
# Why segregation matters: a little contamination spoils a lot
general_waste = 950        # kg of common (Group D) waste
infectious = 50            # kg of Group A mixed in by mistake

# Once mixed, the ENTIRE load must be treated as infectious
contaminated_total = general_waste + infectious
print(f"Load needing infectious treatment: {contaminated_total} kg")  # 1000 kg
# 50 kg of hazard forced 1000 kg through costly treatment - a 20x penalty
penalty = contaminated_total / infectious
print(f"Mass penalty from poor segregation: {penalty:.0f}x")          # 20x
```

```mermaid
graph TD
    SOURCE["Generation point"] --> SEG{"Segregate by group"}
    SEG -->|"Group A infectious"| AUTO["Autoclave sterilise"]
    SEG -->|"Group B chemical"| HAZ["Hazardous treatment"]
    SEG -->|"Group E sharps"| RIGID["Rigid sealed container"]
    SEG -->|"Group D common"| MSW["Ordinary MSW route"]
    AUTO --> DISPOSE["Safe final disposal"]
    HAZ --> DISPOSE
    RIGID --> DISPOSE
```

Remember: hazardous and healthcare waste are managed by **segregate,
track, treat, secure**. The cheapest and safest control is separating the
dangerous fraction at the source, before it can contaminate everything it
touches.
""",
        ),
        quiz_lesson(
            "Quiz: Hazardous and healthcare waste",
            (
                q(
                    "What is a waste manifest used for?",
                    (
                        opt("Advertising recycling services"),
                        opt(
                            "Tracking hazardous waste with documentation from generator to "
                            "final destination so it cannot be lost into the environment",
                            correct=True,
                        ),
                        opt("Measuring the C/N ratio of compost"),
                        opt("Routing collection trucks"),
                    ),
                    "Cradle-to-grave tracking is core to hazardous-waste control (and to "
                    "the Basel Convention for transboundary movement).",
                ),
                q(
                    "How is Group A (infectious) healthcare waste typically treated before "
                    "disposal?",
                    (
                        opt("Composted with food waste"),
                        opt("Recycled into new plastic"),
                        opt(
                            "Sterilised, typically by autoclaving with steam, to destroy pathogens",
                            correct=True,
                        ),
                        opt("Sent straight to an ordinary landfill untreated"),
                    ),
                    "Autoclaving sterilises infectious waste; sharps go in rigid "
                    "containers, chemicals follow the hazardous route.",
                ),
                q(
                    "If 50 kg of infectious waste is mistakenly mixed into 950 kg of "
                    "common waste, how much must now be treated as infectious?",
                    (
                        opt("50 kg"),
                        opt("500 kg"),
                        opt("1000 kg - the entire mixed load", correct=True),
                        opt("950 kg"),
                    ),
                    "Contamination spreads to the whole load; this is why source "
                    "segregation is the golden rule.",
                ),
            ),
        ),
        # -- 8. Circular economy and reverse logistics -----------------
        _t(
            "The circular economy and reverse logistics",
            "10 min",
            """# The circular economy and reverse logistics

The stages so far still assume a mostly **linear** economy: take, make,
use, dispose. The **circular economy** redesigns the system so materials
keep cycling - the goal is to reduce the waste that reaches the bottom of
the hierarchy at all. It rests on the **waste hierarchy**, most-preferred
first:

1. **Prevent / reduce** - do not create the waste (best of all).
2. **Reuse** - use the item again as-is.
3. **Recycle** - reprocess the material.
4. **Recover** - extract energy (composting, digestion, waste-to-energy).
5. **Dispose** - landfill, only as a last resort (worst).

The policy engine that pushes responsibility upstream is **Extended
Producer Responsibility (EPR)**: producers are made responsible for their
products after use, which incentivises durable, recyclable design. In
Brazil the PNRS implements EPR through **reverse logistics** (logistica
reversa) - obligatory take-back systems that return specific products to
the productive chain. Priority streams include:

- Pesticide packaging, batteries, tyres, lubricating oils, fluorescent
  lamps, and electronics (WEEE) - plus **sectoral agreements** (acordos
  setoriais) that share responsibility among government, producers and
  consumers.

Circularity is measured by **diversion** and **circularity rate** - how
much material is kept out of disposal and cycled back:

```text
Circularity indicators (city-scale, per day)
  Total MSW generated:        270 t
  Recycled (materials back):   55 t
  Composted / digested:        40 t
  Landfilled (disposed):      175 t

  Diversion rate = (recycled + composted) / total
                 = (55 + 40) / 270 = 95 / 270 = 35.2 percent

  Landfill dependence = 175 / 270 = 64.8 percent
  Goal: shift tonnes up the hierarchy -> diversion up, disposal down
```

```mermaid
graph TD
    DESIGN["Design for durability and recyclability"] --> USE["Use and reuse"]
    USE --> RETURN["Reverse logistics take back"]
    RETURN --> REPROCESS["Recycle or remanufacture"]
    REPROCESS --> DESIGN
    USE --> RESIDUAL["Residual only"]
    RESIDUAL --> DISPOSE["Landfill last resort"]
```

Remember: the circular economy inverts the whole course - instead of
managing waste at the end of pipe, it designs waste out at the start.
Reverse logistics and EPR are the mechanisms that make producers share the
job, turning the linear line into a loop.
""",
        ),
        quiz_lesson(
            "Quiz: The circular economy and reverse logistics",
            (
                q(
                    "What is the correct order of the waste hierarchy, most preferred first?",
                    (
                        opt("Dispose, recover, recycle, reuse, prevent"),
                        opt(
                            "Prevent/reduce, reuse, recycle, recover, dispose",
                            correct=True,
                        ),
                        opt("Recycle, prevent, dispose, reuse, recover"),
                        opt("Reuse, dispose, recycle, prevent, recover"),
                    ),
                    "Preventing waste is best; landfill disposal is the last resort.",
                ),
                q(
                    "What does reverse logistics (logistica reversa) implement under the PNRS?",
                    (
                        opt("Faster collection routes for MSW"),
                        opt(
                            "Extended Producer Responsibility - obligatory take-back of "
                            "products like batteries, tyres and electronics back into the "
                            "productive chain",
                            correct=True,
                        ),
                        opt("A new landfill liner standard"),
                        opt("A method for composting"),
                    ),
                    "Reverse logistics puts post-use responsibility on producers, sharing "
                    "the burden via sectoral agreements.",
                ),
                q(
                    "A city landfills 175 t of its 270 t daily MSW and diverts the rest. "
                    "Its diversion rate is about:",
                    (
                        opt("64.8 percent"),
                        opt("35.2 percent", correct=True),
                        opt("100 percent"),
                        opt("17.5 percent"),
                    ),
                    "(270 - 175) / 270 = 95 / 270 = 35.2 percent diverted; the rest is "
                    "landfill dependence.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Under ABNT NBR 10004, which class is hazardous waste?",
                    (
                        opt("Class II B - inert"),
                        opt("Class II A - non-inert"),
                        opt("Class I - hazardous", correct=True),
                        opt("Class III"),
                    ),
                    "Class I is hazardous; II A is non-inert, II B is inert.",
                ),
                q(
                    "Gravimetric characterization of MSW mainly tells you what?",
                    (
                        opt("The hazard class of each item"),
                        opt(
                            "The composition of the waste by weight, which fractions "
                            "dominate and feed design decisions",
                            correct=True,
                        ),
                        opt("The truck routing schedule"),
                        opt("The landfill liner permeability"),
                    ),
                    "It is a percent-by-mass profile; Brazilian MSW is organic-dominated.",
                ),
                q(
                    "Why is collection often 50 to 70 percent of total system cost?",
                    (
                        opt("Because landfills are free to build"),
                        opt(
                            "Moving waste from many generation points needs many trucks, "
                            "kilometres and labour hours",
                            correct=True,
                        ),
                        opt("Because recycling is banned"),
                        opt("Because leachate treatment dominates"),
                    ),
                    "It is labour- and fuel-intensive, so route and transfer efficiency "
                    "drive the economics.",
                ),
                q(
                    "Which MRF device separates non-ferrous metals such as aluminium?",
                    (
                        opt("Magnetic separator"),
                        opt("Eddy-current separator", correct=True),
                        opt("Trommel screen"),
                        opt("Optical sorter"),
                    ),
                    "Magnets grab ferrous metal; eddy-current repels aluminium.",
                ),
                q(
                    "Composting is aerobic; anaerobic digestion differs because it…",
                    (
                        opt("uses oxygen and makes only compost"),
                        opt(
                            "runs without oxygen and produces biogas (mostly methane) plus "
                            "digestate",
                            correct=True,
                        ),
                        opt("is only for hazardous waste"),
                        opt("requires no organic feedstock"),
                    ),
                    "No oxygen -> biogas and digestate; the energy a compost pile loses as "
                    "heat is captured.",
                ),
                q(
                    "What makes a sanitary landfill different from an open dump?",
                    (
                        opt("It has no cover soil"),
                        opt(
                            "Engineered containment - liner, leachate collection, gas "
                            "wells and daily cover isolate the waste",
                            correct=True,
                        ),
                        opt("It accepts only recyclables"),
                        opt("It is cheaper to operate"),
                    ),
                    "The PNRS banned open dumps; engineered containment is the whole difference.",
                ),
                q(
                    "What is the primary job of a landfill's clay-plus-geomembrane liner?",
                    (
                        opt("To generate biogas"),
                        opt(
                            "To stop leachate from percolating into groundwater",
                            correct=True,
                        ),
                        opt("To compact the waste"),
                        opt("To collect rainwater for reuse"),
                    ),
                    "A low-permeability barrier below the leachate collection layer "
                    "protects the aquifer.",
                ),
                q(
                    "Landfill gas is about half methane. The preferred way to handle it is:",
                    (
                        opt("Vent it directly to the atmosphere"),
                        opt(
                            "Capture it for energy recovery, or flare it if energy use is "
                            "not viable",
                            correct=True,
                        ),
                        opt("Dissolve it in the leachate"),
                        opt("Bury it deeper"),
                    ),
                    "Methane is ~28x CO2 over 100 years; energy recovery is best, flaring "
                    "second, venting worst.",
                ),
                q(
                    "Why is source segregation the golden rule for healthcare waste?",
                    (
                        opt("It makes trucks faster"),
                        opt(
                            "Mixing a small infectious fraction into general waste forces "
                            "the whole load through costly infectious treatment",
                            correct=True,
                        ),
                        opt("It increases the recycling rate of glass"),
                        opt("It is required only for radioactive waste"),
                    ),
                    "A little contamination spoils a lot; segregate, track, treat, secure.",
                ),
                q(
                    "In the waste hierarchy and circular economy, which option is most preferred?",
                    (
                        opt("Landfill disposal"),
                        opt("Energy recovery"),
                        opt(
                            "Preventing or reducing the waste in the first place",
                            correct=True,
                        ),
                        opt("Recycling"),
                    ),
                    "Prevent is best, dispose is last; the circular economy designs waste "
                    "out and uses reverse logistics and EPR to close the loop.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SOLID_WASTE_MANAGEMENT_COURSES: tuple[SeedCourse, ...] = (_SOLID_WASTE_MANAGEMENT,)
