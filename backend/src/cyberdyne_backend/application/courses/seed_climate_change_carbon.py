"""Academy seed content - Climate Change, GHG Inventories and LCA.

The engineering of decarbonization, end to end: the physical climate
system and the greenhouse effect, the carbon cycle and radiative forcing,
emission scenarios and climate models, greenhouse-gas inventories across
scopes 1, 2 and 3, decarbonization pathways, life-cycle assessment,
carbon and water footprints, and adaptation, resilience and climate
justice. Every lesson is a direct explanation with a worked formula or
calculation and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz. Grounded in IPCC, the GHG
Protocol, and ISO 14040/14064.
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


_CLIMATE_CHANGE_CARBON = SeedCourse(
    slug="climate-change-carbon",
    title="Climate Change, GHG Inventories & LCA",
    description=(
        "The engineering of decarbonization: the climate system and carbon "
        "cycle, greenhouse-gas inventories across scopes 1, 2 and 3, "
        "life-cycle assessment, carbon and water footprints, and adaptation "
        "and resilience - with worked energy balances, emission-factor "
        "calculations and a diagram in every lesson, grounded in IPCC, the "
        "GHG Protocol and ISO 14040/14064."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Climate Change, GHG Inventories and LCA

Climate change is, at bottom, an **energy-balance problem** with an
engineering answer. Extra greenhouse gases trap heat; to stop the warming
you have to measure emissions honestly and then remove them from the
system. This course takes you from the physics of the greenhouse effect
to the accounting standards and life-cycle methods engineers use to
decarbonize real organizations and products.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a short worked calculation (an energy balance, an emission
factor, a footprint), and draws it as a diagram. After each lesson there
is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **The climate system** - the greenhouse effect as an energy balance
2. **The carbon cycle** - reservoirs, fluxes and radiative forcing
3. **Emission scenarios and climate models** - RCPs, SSPs and GCMs
4. **GHG inventories** - scopes 1, 2 and 3 under the GHG Protocol
5. **Decarbonization pathways** - the levers that cut emissions
6. **Life-cycle assessment** - cradle-to-grave impact under ISO 14040
7. **Carbon and water footprints** - product-level accounting
8. **Adaptation and resilience** - living with the warming we cannot avoid

This is the map. Standards referenced throughout - IPCC assessment
reports, the GHG Protocol, ISO 14064 and ISO 14040/14044 - are the tools
practicing climate engineers actually use.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "At its core, how does this course frame climate change?",
                    (
                        opt("As a purely political problem with no measurement"),
                        opt(
                            "As an energy-balance problem with an engineering answer - "
                            "measure emissions honestly, then remove them",
                            correct=True,
                        ),
                        opt("As a software bug in climate models"),
                        opt("As a problem only for future generations"),
                    ),
                    "The greenhouse effect is an energy balance; decarbonization is the "
                    "engineering response.",
                ),
                q(
                    "Which standards does the course lean on throughout?",
                    (
                        opt("Only local building codes"),
                        opt(
                            "IPCC assessment reports, the GHG Protocol, and ISO "
                            "14064 and 14040/14044",
                            correct=True,
                        ),
                        opt("Only corporate marketing guidelines"),
                        opt("None - it avoids all standards"),
                    ),
                    "These are the real reference frameworks for climate science and "
                    "GHG accounting.",
                ),
            ),
        ),
        # -- 1. Climate system and greenhouse effect -------------------
        _t(
            "The climate system and the greenhouse effect",
            "10 min",
            """# The climate system and the greenhouse effect

Earth's temperature is set by a simple balance: energy arriving from the
Sun must, on average, equal energy radiated back to space. The **incoming
solar flux** at the top of the atmosphere averages about 1361 W/m2 (the
**solar constant**), spread over the planet's disk and reflected in part
by clouds, ice and aerosols - the **albedo**.

Start with the **effective temperature** the Earth would have with *no*
atmosphere, from the Stefan-Boltzmann law balancing absorbed sunlight
against emitted infrared:

```text
Absorbed solar = Emitted infrared
(S/4)(1 - a)   = sigma * Te^4

  S     = 1361 W/m2   (solar constant)
  a     = 0.30        (planetary albedo, dimensionless)
  sigma = 5.67e-8 W/m2/K4  (Stefan-Boltzmann constant)

Te = [ S (1 - a) / (4 sigma) ]^(1/4)
   = [ 1361 * 0.70 / (4 * 5.67e-8) ]^(1/4)
   = 255 K  =  about -18 C
```

That -18 C is far colder than the observed **+15 C** surface average. The
**33 C gap** is the **natural greenhouse effect**: gases such as water
vapour, carbon dioxide and methane are transparent to incoming sunlight
but **absorb and re-emit outgoing infrared**, warming the surface below.

Adding more greenhouse gas thickens this blanket - the **enhanced
greenhouse effect** that drives modern warming. The climate is a coupled
system of atmosphere, ocean, ice (cryosphere), land and biosphere, all
exchanging energy and carbon:

```mermaid
graph TD
    SUN["Incoming solar shortwave"] --> ATM["Atmosphere"]
    ATM --> SURF["Surface absorbs energy"]
    SURF --> IR["Outgoing infrared longwave"]
    IR --> GHG["Greenhouse gases absorb infrared"]
    GHG --> BACK["Re-emitted back to surface"]
    BACK --> WARM["Surface warms above 255 K"]
```

Remember: the greenhouse effect is not a pollutant leak but a physical
energy balance - the natural version keeps Earth habitable, and adding
gas shifts the balance toward warming.
""",
        ),
        quiz_lesson(
            "Quiz: The climate system and the greenhouse effect",
            (
                q(
                    "Why is Earth's effective temperature (about 255 K) colder than "
                    "the observed surface average?",
                    (
                        opt("Because the solar constant is measured wrong"),
                        opt(
                            "The natural greenhouse effect adds about 33 C - gases absorb "
                            "and re-emit outgoing infrared, warming the surface",
                            correct=True,
                        ),
                        opt("Because the Earth is cooling overall"),
                        opt("Because albedo is exactly zero"),
                    ),
                    "255 K is the no-atmosphere balance; greenhouse gases lift the real "
                    "surface to about 288 K.",
                ),
                q(
                    "In the energy-balance equation, what does the albedo a represent?",
                    (
                        opt("The fraction of sunlight reflected back to space", correct=True),
                        opt("The total infrared emitted by the surface"),
                        opt("The Stefan-Boltzmann constant"),
                        opt("The mass of the atmosphere"),
                    ),
                    "Albedo (about 0.30) is the reflected fraction; only (1 - a) of the "
                    "incoming flux is absorbed.",
                ),
                q(
                    "Greenhouse gases affect which part of the radiation balance?",
                    (
                        opt("They reflect incoming sunlight"),
                        opt(
                            "They are largely transparent to incoming sunlight but absorb "
                            "outgoing infrared",
                            correct=True,
                        ),
                        opt("They increase the solar constant"),
                        opt("They have no effect on radiation"),
                    ),
                    "Transparent in, opaque out - that asymmetry is what warms the surface.",
                ),
            ),
        ),
        # -- 2. Carbon cycle and radiative forcing ---------------------
        _t(
            "The carbon cycle and radiative forcing",
            "10 min",
            """# The carbon cycle and radiative forcing

Carbon moves continuously between four great **reservoirs**: the
atmosphere (about 875 Gt C today), the oceans (about 38000 Gt C), land
and vegetation and soils (about 2000 Gt C), and geological stores
(fossil fuels, rocks). The **fluxes** between them - photosynthesis,
respiration, ocean gas exchange - are naturally near-balanced. Human
**fossil-fuel combustion and land-use change** inject roughly 11 Gt C per
year, a small flux against the stocks but enough to raise atmospheric
concentration steadily because the sinks only absorb about half of it.

The atmosphere has climbed from a pre-industrial **280 ppm** of CO2 to
over **420 ppm** today. The climate consequence is measured as
**radiative forcing** - the change in net energy flux at the tropopause,
in W/m2. For CO2 the forcing grows with the **logarithm** of
concentration:

```text
Radiative forcing of CO2 (simplified IPCC expression):

  dF = 5.35 * ln(C / C0)     [W/m2]

  C0 = 280 ppm  (pre-industrial reference)
  C  = 420 ppm  (present-day)

  dF = 5.35 * ln(420 / 280)
     = 5.35 * ln(1.50)
     = 5.35 * 0.405
     = about 2.17 W/m2
```

A positive forcing means the system is gaining energy and must warm to
restore balance. Different gases are compared with **Global Warming
Potential (GWP)** - the integrated forcing of 1 kg of gas over 100 years
relative to 1 kg of CO2. Methane has a GWP-100 of about 28-30; nitrous
oxide about 265. Emissions are summed in **CO2-equivalent (CO2e)** using
these factors.

```mermaid
graph LR
    ATM["Atmosphere carbon store"] --> PS["Photosynthesis uptake"]
    PS --> LAND["Land and biosphere store"]
    LAND --> RESP["Respiration returns carbon"]
    RESP --> ATM
    OCEAN["Ocean store"] --> ATM
    ATM --> OCEAN
    FOSSIL["Fossil fuel burning"] --> ATM
    ATM --> RF["Radiative forcing rises"]
```

Remember: it is the **cumulative** carbon added to the atmosphere, not
any single year, that sets the forcing - and forcing scales with the log
of concentration, so each further doubling adds a similar push.
""",
        ),
        quiz_lesson(
            "Quiz: The carbon cycle and radiative forcing",
            (
                q(
                    "Radiative forcing from CO2 scales with concentration how?",
                    (
                        opt("Linearly - double CO2, double the forcing"),
                        opt(
                            "Logarithmically - dF = 5.35 * ln(C / C0), so each doubling "
                            "adds a similar push",
                            correct=True,
                        ),
                        opt("As the square of concentration"),
                        opt("It does not depend on concentration"),
                    ),
                    "The log relationship means the first ppm matter more than the last; "
                    "each doubling gives roughly equal forcing.",
                ),
                q(
                    "What does Global Warming Potential (GWP) let you do?",
                    (
                        opt("Measure the mass of the atmosphere"),
                        opt(
                            "Compare gases on a common CO2-equivalent basis by their "
                            "integrated forcing over a time horizon",
                            correct=True,
                        ),
                        opt("Convert energy into temperature directly"),
                        opt("Calculate the solar constant"),
                    ),
                    "GWP-100 lets methane, N2O and CO2 be summed as CO2e; methane is "
                    "about 28-30, N2O about 265.",
                ),
                q(
                    "Why does atmospheric CO2 keep rising even though the human flux is "
                    "small against the reservoirs?",
                    (
                        opt("The reservoirs are actually empty"),
                        opt(
                            "Natural sinks absorb only about half the added carbon, so "
                            "the rest accumulates year after year",
                            correct=True,
                        ),
                        opt("The oceans emit all of it back instantly"),
                        opt("Because the solar constant is increasing"),
                    ),
                    "Roughly half the emitted carbon is taken up by ocean and land; the "
                    "remainder is cumulative in the atmosphere.",
                ),
            ),
        ),
        # -- 3. Emission scenarios and climate models ------------------
        _t(
            "Emission scenarios and climate models",
            "10 min",
            """# Emission scenarios and climate models

We cannot run experiments on a second Earth, so projections come from
**climate models** driven by **emission scenarios**. A scenario is a
plausible story of future emissions; a model translates that story into
temperature, rainfall and sea-level outcomes.

The IPCC uses two linked scenario families:

- **RCPs (Representative Concentration Pathways)** - labelled by the
  radiative forcing they reach in 2100: RCP2.6, RCP4.5, RCP6.0, RCP8.5
  (so RCP8.5 means about +8.5 W/m2, a high-emissions world).
- **SSPs (Shared Socioeconomic Pathways)** - narratives of population,
  economy and policy (SSP1 sustainability, SSP5 fossil-fuelled growth)
  that are paired with forcing levels, e.g. **SSP1-2.6** or **SSP5-8.5**.

**General Circulation Models (GCMs)** divide the atmosphere and ocean
into a 3D grid and step the physics forward in time, conserving energy,
mass and momentum in each cell. Because clouds and other processes are
smaller than a grid cell, they are **parameterized** - a key source of
spread between models.

A first-order estimate of eventual warming uses **climate sensitivity**,
the temperature rise per unit forcing:

```python
import math

# Equilibrium warming from a radiative forcing
lambda_sens = 0.8   # climate sensitivity parameter, K per (W/m2)
dF = 2.17           # present-day CO2 forcing, W/m2

delta_T = lambda_sens * dF
print(round(delta_T, 2))   # -> 1.74  (deg C of eventual warming)

# Equilibrium Climate Sensitivity: warming for a CO2 doubling
dF_2x = 5.35 * math.log(2)          # about 3.71 W/m2
ecs = lambda_sens * dF_2x
print(round(ecs, 2))                # -> 2.97  (deg C per doubling)
```

The IPCC "likely" range for equilibrium climate sensitivity is about
**2.5 to 4 C** per doubling. Models are compared as an **ensemble** - no
single run is trusted alone; the spread expresses genuine uncertainty.

```mermaid
graph TD
    SSP["Socioeconomic pathway SSP"] --> EMIT["Emission scenario"]
    RCP["Forcing level RCP"] --> EMIT
    EMIT --> GCM["General circulation model grid"]
    GCM --> PARAM["Parameterized clouds and aerosols"]
    PARAM --> ENS["Multi model ensemble"]
    ENS --> PROJ["Temperature and sea level projection"]
```

Remember: a projection is a scenario plus a model, and honest projections
report a **range** from many models, not a single deterministic number.
""",
        ),
        quiz_lesson(
            "Quiz: Emission scenarios and climate models",
            (
                q(
                    "What does the number in a scenario like RCP8.5 refer to?",
                    (
                        opt("The year the world reaches net zero"),
                        opt(
                            "The approximate radiative forcing in W/m2 reached by 2100",
                            correct=True,
                        ),
                        opt("The global average temperature in Celsius"),
                        opt("The number of models used"),
                    ),
                    "RCP8.5 means about +8.5 W/m2 - a high-emissions pathway; RCP2.6 is "
                    "a strong-mitigation one.",
                ),
                q(
                    "Why are clouds 'parameterized' in a GCM?",
                    (
                        opt("Because clouds do not affect climate"),
                        opt(
                            "They are smaller than a model grid cell, so their effect is "
                            "approximated rather than resolved directly",
                            correct=True,
                        ),
                        opt("Because they are impossible to observe"),
                        opt("To make the model run slower on purpose"),
                    ),
                    "Sub-grid processes must be parameterized, and this is a leading "
                    "source of model-to-model spread.",
                ),
                q(
                    "What is equilibrium climate sensitivity?",
                    (
                        opt("The solar constant divided by four"),
                        opt(
                            "The eventual global warming for a doubling of CO2 - IPCC "
                            "likely range about 2.5 to 4 C",
                            correct=True,
                        ),
                        opt("The albedo of the ocean"),
                        opt("The number of ppm added per year"),
                    ),
                    "ECS captures how strongly temperature responds to a CO2 doubling; "
                    "it is reported as a range.",
                ),
            ),
        ),
        # -- 4. GHG inventories (scopes 1, 2 and 3) --------------------
        _t(
            "GHG inventories (scopes 1, 2 and 3)",
            "11 min",
            """# GHG inventories (scopes 1, 2 and 3)

Before you can cut emissions you must **measure** them. A **greenhouse-gas
inventory** is an organization's accounting of the emissions it causes,
compiled under the **GHG Protocol** (and formalized in **ISO 14064-1**).
Emissions are sorted into three **scopes** to avoid double-counting and to
show where an organization has direct versus indirect influence:

- **Scope 1 - direct** emissions from sources the company owns or
  controls: fuel burned in boilers, furnaces and company vehicles,
  process emissions, refrigerant leaks.
- **Scope 2 - indirect from purchased energy**: the emissions from
  generating the electricity, steam, heat or cooling the company buys.
- **Scope 3 - all other indirect** emissions across the value chain:
  purchased goods and services, business travel, employee commuting,
  transport and distribution, use of sold products, end-of-life. Usually
  the **largest** and hardest to measure - often 70 percent or more of
  the total.

The core calculation everywhere is **activity data multiplied by an
emission factor**:

```text
Emissions (kg CO2e) = Activity data x Emission factor

Example - Scope 1, natural gas in a boiler:
  Activity data     = 100000 kWh of natural gas burned
  Emission factor   = 0.184 kg CO2e per kWh   (national fuel factor)
  Emissions         = 100000 x 0.184 = 18400 kg CO2e = 18.4 t CO2e

Example - Scope 2, purchased electricity (location-based):
  Activity data     = 250000 kWh from the grid
  Grid factor       = 0.075 kg CO2e per kWh   (low-carbon grid)
  Emissions         = 250000 x 0.075 = 18750 kg CO2e = 18.75 t CO2e
```

Scope 2 has two accounting methods: **location-based** (the average grid
factor where you operate) and **market-based** (reflecting the specific
electricity contracts or renewable certificates you purchase). Best
practice reports **both**.

```mermaid
graph TD
    SRC["Company activities"] --> S1["Scope 1 direct fuel and process"]
    SRC --> S2["Scope 2 purchased electricity and heat"]
    SRC --> S3["Scope 3 value chain up and downstream"]
    S1 --> INV["GHG inventory in CO2e"]
    S2 --> INV
    S3 --> INV
    INV --> REPORT["Report and set targets"]
```

Remember: activity data times emission factor, sorted into three scopes.
Scope 3 is usually the biggest and the reason a credible target must look
beyond a company's own fences.
""",
        ),
        quiz_lesson(
            "Quiz: GHG inventories (scopes 1, 2 and 3)",
            (
                q(
                    "Which scope covers emissions from purchased electricity?",
                    (
                        opt("Scope 1"),
                        opt("Scope 2", correct=True),
                        opt("Scope 3"),
                        opt("None - electricity is emission-free"),
                    ),
                    "Scope 2 is indirect emissions from generating the energy you buy; "
                    "Scope 1 is your own combustion.",
                ),
                q(
                    "What is the core emissions calculation in an inventory?",
                    (
                        opt("Temperature times albedo"),
                        opt(
                            "Activity data multiplied by an emission factor, expressed in CO2e",
                            correct=True,
                        ),
                        opt("Revenue divided by headcount"),
                        opt("Solar constant times area"),
                    ),
                    "For example 100000 kWh of gas x 0.184 kg CO2e/kWh = 18.4 t CO2e.",
                ),
                q(
                    "Why is Scope 3 usually the hardest and most important to address?",
                    (
                        opt("It is always zero"),
                        opt(
                            "It covers the whole value chain and is often the majority of "
                            "total emissions, yet is indirect and hard to measure",
                            correct=True,
                        ),
                        opt("It only counts refrigerant leaks"),
                        opt("It is banned from inventories"),
                    ),
                    "Value-chain emissions (purchased goods, use of products, etc.) "
                    "often exceed 70 percent of the total.",
                ),
            ),
        ),
        # -- 5. Decarbonization pathways -------------------------------
        _t(
            "Decarbonization pathways",
            "11 min",
            """# Decarbonization pathways

An inventory tells you where the emissions are; a **decarbonization
pathway** is the ordered set of actions that drives them to **net zero** -
the point where any residual emissions are balanced by permanent removals.
The scientific anchor is the **carbon budget**: the cumulative CO2 we can
still emit for a given temperature limit. Roughly, for a two-in-three
chance of staying under 1.5 C the world had about **500 Gt CO2** left from
the early 2020s, and at about 40 Gt CO2/year that is little more than a
decade.

The engineering levers, in the order teams usually apply them:

- **Efficiency and demand reduction** - use less energy for the same
  service (insulation, process heat recovery, right-sizing). The cheapest
  tonne is the one you never emit.
- **Electrify and switch fuels** - replace combustion with electric heat
  pumps, electric vehicles and electric process heat.
- **Clean the electricity** - decarbonize the grid with wind, solar,
  hydro and nuclear so that electrification actually cuts emissions.
- **Green fuels and feedstocks** - hydrogen, biomass and synthetic fuels
  for what cannot be electrified (aviation, steel, cement).
- **Carbon removal** - for the residual few percent that cannot be
  eliminated: afforestation, soil carbon, and engineered capture (BECCS,
  direct air capture).

A simple decomposition, the **Kaya identity**, shows the four dials that
set energy CO2:

```text
CO2 = Population x (GDP / Population) x (Energy / GDP) x (CO2 / Energy)
       people      affluence           energy intensity   carbon intensity

To cut CO2 while population and GDP per person keep rising, the last two
terms must fall fast:
  - Energy intensity  (Energy / GDP)  -> efficiency
  - Carbon intensity  (CO2 / Energy)  -> clean energy

Required annual improvement to halve emissions in 10 years:
  0.5^(1/10) - 1 = about -6.7 percent per year
```

A **marginal abatement cost curve (MACC)** ranks measures from cheapest
(often negative-cost efficiency) to most expensive, guiding where to
spend first.

```mermaid
graph LR
    MEASURE["Efficiency and demand cut"] --> ELEC["Electrify and switch fuels"]
    ELEC --> CLEAN["Decarbonize the grid"]
    CLEAN --> GREEN["Green fuels for hard sectors"]
    GREEN --> RESID["Residual emissions"]
    RESID --> REMOVE["Carbon removal to net zero"]
```

Remember: efficiency first, then electrify onto a clean grid, then green
fuels for what is left, and only then removals for the unavoidable
residual - all governed by a shrinking carbon budget.
""",
        ),
        quiz_lesson(
            "Quiz: Decarbonization pathways",
            (
                q(
                    "What does 'net zero' mean?",
                    (
                        opt("No organization emits anything at all"),
                        opt(
                            "Residual emissions are balanced by an equal amount of "
                            "permanent carbon removal",
                            correct=True,
                        ),
                        opt("Emissions are simply not measured"),
                        opt("The grid runs at zero voltage"),
                    ),
                    "Net zero allows unavoidable residual emissions only if matched by "
                    "genuine removals.",
                ),
                q(
                    "In the Kaya identity, which two terms must fall to cut CO2 while "
                    "population and GDP rise?",
                    (
                        opt("Population and affluence"),
                        opt(
                            "Energy intensity (Energy/GDP) and carbon intensity (CO2/Energy)",
                            correct=True,
                        ),
                        opt("The solar constant and albedo"),
                        opt("Scope 1 and Scope 2 only"),
                    ),
                    "Efficiency lowers energy intensity; clean energy lowers carbon "
                    "intensity - those are the controllable dials.",
                ),
                q(
                    "What is the usual first lever in a decarbonization pathway?",
                    (
                        opt("Direct air capture at any cost"),
                        opt(
                            "Efficiency and demand reduction - the cheapest tonne is the "
                            "one you never emit",
                            correct=True,
                        ),
                        opt("Buying unlimited offsets"),
                        opt("Ignoring the carbon budget"),
                    ),
                    "Efficiency first, then electrification and a clean grid, with "
                    "removals reserved for the residual.",
                ),
            ),
        ),
        # -- 6. Life-cycle assessment ----------------------------------
        _t(
            "Life-cycle assessment",
            "11 min",
            """# Life-cycle assessment

An organizational inventory counts a company's emissions; a **life-cycle
assessment (LCA)** counts the impacts of a **product or service across its
whole life** - raw materials, manufacture, distribution, use and
end-of-life. It exists to avoid **burden shifting**: an electric car that
looks clean in use may carry heavy emissions in battery manufacture, and
only a life-cycle view catches that.

LCA is standardized by **ISO 14040 and 14044** in four phases:

1. **Goal and scope** - define the question, the **functional unit** (the
   quantified service, e.g. "1000 km driven" or "1 litre of packaged
   drink delivered"), and the **system boundary** (cradle-to-gate,
   cradle-to-grave, or cradle-to-cradle).
2. **Inventory analysis (LCI)** - tally every input (energy, water,
   materials) and output (emissions, waste) across the boundary.
3. **Impact assessment (LCIA)** - translate that inventory into impact
   categories: global warming, acidification, eutrophication, water use,
   toxicity.
4. **Interpretation** - identify hotspots, test assumptions, and conclude.

Everything is normalized to the **functional unit**:

```text
Carbon footprint per functional unit:

  Impact per FU = Total life-cycle emissions / number of functional units

Example - two coffee cups, functional unit = "1 serving of coffee":
  Single-use paper cup: 0.11 kg CO2e per serving (made and discarded each time)
  Reusable ceramic mug: 0.31 kg CO2e to make + 0.012 kg CO2e per wash

  Break-even number of uses N where reusable beats single-use:
    0.31 + 0.012 N  =  0.11 N
    0.31            =  0.098 N
    N               =  about 3.2 uses

  So after ~4 uses the reusable mug wins - a result only LCA reveals.
```

The **choice of functional unit and boundary decides the answer**, so
they must be stated up front. A cradle-to-gate study (factory gate) and a
cradle-to-grave study (including use and disposal) can rank the same two
products differently.

```mermaid
graph LR
    GOAL["Goal and functional unit"] --> BOUND["System boundary"]
    BOUND --> LCI["Inventory of inputs and outputs"]
    LCI --> LCIA["Impact assessment categories"]
    LCIA --> INTERP["Interpretation and hotspots"]
    INTERP --> GOAL
```

Remember: LCA compares products on a **functional unit** across the whole
life cycle, so improvements in one stage are not just shifting burden to
another.
""",
        ),
        quiz_lesson(
            "Quiz: Life-cycle assessment",
            (
                q(
                    "What is a 'functional unit' in LCA?",
                    (
                        opt("The heaviest component of the product"),
                        opt(
                            "The quantified service the study compares against, e.g. "
                            "'1000 km driven' or '1 serving of coffee'",
                            correct=True,
                        ),
                        opt("The factory where the product is made"),
                        opt("The Stefan-Boltzmann constant"),
                    ),
                    "All impacts are normalized to the functional unit so products are "
                    "compared on equal service.",
                ),
                q(
                    "Why does LCA look across the whole life cycle rather than one stage?",
                    (
                        opt("To make the report longer"),
                        opt(
                            "To avoid burden shifting - an improvement in one stage may "
                            "just move impact to another",
                            correct=True,
                        ),
                        opt("Because only manufacturing matters"),
                        opt("Because ISO forbids single-stage analysis of energy"),
                    ),
                    "Cradle-to-grave thinking catches trade-offs a use-phase-only view would miss.",
                ),
                q(
                    "In the coffee-cup example, what determines whether the reusable mug wins?",
                    (
                        opt("Its colour"),
                        opt(
                            "The number of uses - it beats single-use only after enough "
                            "servings pass its break-even point",
                            correct=True,
                        ),
                        opt("The price of coffee"),
                        opt("The grid emission factor only"),
                    ),
                    "Reuse amortizes the higher manufacturing footprint; below the "
                    "break-even count the single-use cup is lower impact.",
                ),
            ),
        ),
        # -- 7. Carbon and water footprints ----------------------------
        _t(
            "Carbon and water footprints",
            "10 min",
            """# Carbon and water footprints

A **footprint** applies life-cycle thinking to a single impact category to
give one comparable number. Two matter most in practice.

The **carbon footprint** is the total greenhouse-gas emissions of a
product, activity or person, expressed in **CO2e** over the life cycle. It
is a single-issue LCA (the global-warming category) and is standardized
for products by **ISO 14067** and **PAS 2050**. Aggregate gases with GWP:

```text
Carbon footprint = sum over gases of ( mass_gas x GWP_gas )

Example - a meal with mixed emissions:
  CO2 : 2.0 kg   x  1    =  2.0 kg CO2e
  CH4 : 0.05 kg  x  28   =  1.4 kg CO2e
  N2O : 0.004 kg x  265  =  1.06 kg CO2e
  -------------------------------------
  Total footprint        =  4.46 kg CO2e
```

The **water footprint** (Hoekstra, standardized in **ISO 14046**) is the
volume of freshwater consumed and polluted across the life cycle, split
into three colours:

- **Blue water** - surface and groundwater consumed (irrigation, process).
- **Green water** - rainwater stored in soil and used by crops.
- **Grey water** - the freshwater needed to **dilute pollution** back to
  standards.

```text
Grey water footprint (dilution volume):

  Grey = L / (c_max - c_nat)

  L      = pollutant load released        (kg/year)
  c_max  = ambient water-quality limit    (kg/m3)
  c_nat  = natural background concentration (kg/m3)

Example - 1000 kg/yr of nitrate, limit 0.010 kg/m3, background 0.001:
  Grey = 1000 / (0.010 - 0.001) = 1000 / 0.009 = about 111000 m3/yr
```

Footprints turn diffuse impacts into a decision number - "this shirt is
2.1 kg CO2e and 2700 litres of water" - but a number is only as honest as
its **boundary and functional unit**, so those must travel with it.

```mermaid
graph TD
    LC["Product life cycle"] --> GAS["Greenhouse gas emissions"]
    LC --> H2O["Freshwater use and pollution"]
    GAS --> CF["Carbon footprint in CO2e"]
    H2O --> BLUE["Blue water consumed"]
    H2O --> GREEN["Green rainwater used"]
    H2O --> GREY["Grey dilution water"]
    BLUE --> WF["Water footprint total"]
    GREEN --> WF
    GREY --> WF
```

Remember: a footprint is a single-issue life-cycle number - carbon in
CO2e via GWP, water as blue plus green plus grey - and it only means
something with its boundary stated.
""",
        ),
        quiz_lesson(
            "Quiz: Carbon and water footprints",
            (
                q(
                    "How is a carbon footprint aggregated across different gases?",
                    (
                        opt("By adding raw masses regardless of gas"),
                        opt(
                            "By multiplying each gas mass by its GWP and summing to CO2e",
                            correct=True,
                        ),
                        opt("By taking the largest single gas only"),
                        opt("By dividing by the water footprint"),
                    ),
                    "Each gas is weighted by its GWP; for example 0.05 kg CH4 x 28 = 1.4 kg CO2e.",
                ),
                q(
                    "What is the 'grey' water footprint?",
                    (
                        opt("Rainwater stored in soil and used by crops"),
                        opt("Surface water consumed by irrigation"),
                        opt(
                            "The volume of freshwater needed to dilute pollution back to "
                            "quality standards",
                            correct=True,
                        ),
                        opt("Seawater used for cooling"),
                    ),
                    "Grey = load / (c_max - c_nat); green is soil rainwater and blue is "
                    "consumed surface or groundwater.",
                ),
                q(
                    "A footprint number is only meaningful if what travels with it?",
                    (
                        opt("The company logo"),
                        opt(
                            "Its system boundary and functional unit",
                            correct=True,
                        ),
                        opt("The price of the product"),
                        opt("The current air temperature"),
                    ),
                    "Without a stated boundary and functional unit, footprints cannot be "
                    "compared honestly.",
                ),
            ),
        ),
        # -- 8. Adaptation, resilience and climate justice -------------
        _t(
            "Adaptation, resilience and climate justice",
            "10 min",
            """# Adaptation, resilience and climate justice

Mitigation cuts future warming, but some change is already **locked in**
by past emissions, so we must also **adapt**. Where **mitigation** reduces
the cause (emissions), **adaptation** reduces the harm from impacts that
arrive anyway - heatwaves, floods, drought, sea-level rise. The two are
complements, not alternatives.

**Adaptation** measures span grey, green and soft options:

- **Grey (engineered)** - sea walls, raised flood defences, larger storm
  drains, cooling centres.
- **Green (nature-based)** - restored mangroves and wetlands that absorb
  storm surge, urban trees that cut heat, permeable surfaces.
- **Soft (institutional)** - early-warning systems, building codes, land-
  use zoning, insurance and emergency planning.

**Resilience** is the capacity of a community or system to absorb a shock
and recover function quickly. Engineers quantify exposure with **risk**:

```text
Climate risk = Hazard x Exposure x Vulnerability

  Hazard        - probability and intensity of the climate event
  Exposure      - people and assets in harm's way
  Vulnerability - susceptibility to damage (and lack of coping capacity)

Reducing ANY factor cuts risk:
  - move assets out of the floodplain  -> lower Exposure
  - stronger buildings and warning     -> lower Vulnerability
  - (hazard is set by the climate; mitigation lowers it globally)

Design standard example - a levee sized for a "100-year flood":
  Annual exceedance probability = 1 / 100 = 0.01
  Probability of at least one exceedance in 30 years:
    1 - (1 - 0.01)^30 = 1 - 0.74 = about 0.26  (26 percent)
```

That last number is the key lesson of resilience design: a "100-year"
defence still has a **26 percent chance** of being overtopped within a
30-year mortgage, and climate change is **raising** these probabilities.

**Climate justice** recognizes a deep asymmetry: the people who emitted
**least** - lower-income countries and communities - are often the **most
exposed and least resourced** to adapt. Fair policy therefore weighs who
caused the problem, who suffers, and who pays for adaptation and loss.

```mermaid
graph TD
    PAST["Locked in warming"] --> IMPACT["Unavoidable impacts"]
    IMPACT --> ADAPT["Adaptation grey green and soft"]
    ADAPT --> RES["Resilience recover quickly"]
    RISK["Hazard times exposure times vulnerability"] --> ADAPT
    RES --> JUST["Climate justice fair burden sharing"]
```

Remember: mitigation and adaptation work together, resilience is designed
by lowering exposure and vulnerability against a shifting hazard, and
climate justice asks that the burden fall fairly on those able to bear it.
""",
        ),
        quiz_lesson(
            "Quiz: Adaptation, resilience and climate justice",
            (
                q(
                    "How do mitigation and adaptation differ?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "Mitigation reduces the cause (emissions); adaptation reduces "
                            "the harm from impacts that arrive anyway",
                            correct=True,
                        ),
                        opt("Adaptation increases emissions on purpose"),
                        opt("Mitigation only applies to water footprints"),
                    ),
                    "They are complements: cut the cause and manage the unavoidable consequences.",
                ),
                q(
                    "In the climate-risk relationship, which factors can engineers reduce locally?",
                    (
                        opt("Only the hazard"),
                        opt(
                            "Exposure and vulnerability - e.g. move assets out of the "
                            "floodplain, strengthen buildings and add warning systems",
                            correct=True,
                        ),
                        opt("Only the solar constant"),
                        opt("None of them"),
                    ),
                    "Risk = Hazard x Exposure x Vulnerability; local action lowers "
                    "exposure and vulnerability, while mitigation lowers the hazard "
                    "globally.",
                ),
                q(
                    "What does climate justice highlight?",
                    (
                        opt("That all countries emit equally"),
                        opt(
                            "That those who emitted least are often the most exposed and "
                            "least able to adapt, so burdens should be shared fairly",
                            correct=True,
                        ),
                        opt("That adaptation is unnecessary"),
                        opt("That risk cannot be measured"),
                    ),
                    "The asymmetry between who caused warming and who suffers it is "
                    "central to fair policy.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why is Earth's surface warmer than its 255 K effective temperature?",
                    (
                        opt("The Sun is getting hotter"),
                        opt(
                            "The natural greenhouse effect - gases absorb and re-emit "
                            "outgoing infrared, adding about 33 C",
                            correct=True,
                        ),
                        opt("The albedo is greater than one"),
                        opt("The oceans generate their own heat"),
                    ),
                    "Greenhouse gases lift the surface from about 255 K to about 288 K.",
                ),
                q(
                    "Radiative forcing from CO2 grows with concentration how?",
                    (
                        opt("Linearly"),
                        opt("Logarithmically, dF = 5.35 * ln(C / C0)", correct=True),
                        opt("Exponentially"),
                        opt("Not at all"),
                    ),
                    "Each doubling of CO2 adds roughly equal forcing because of the log "
                    "relationship.",
                ),
                q(
                    "What does a scenario label like SSP5-8.5 combine?",
                    (
                        opt("Two unrelated temperatures"),
                        opt(
                            "A socioeconomic narrative (SSP5) paired with a 2100 forcing "
                            "level (8.5 W/m2)",
                            correct=True,
                        ),
                        opt("A model grid size and a year"),
                        opt("Two emission factors"),
                    ),
                    "SSPs give the storyline; the forcing number gives the radiative endpoint.",
                ),
                q(
                    "Which scope covers value-chain emissions such as purchased goods "
                    "and use of sold products?",
                    (
                        opt("Scope 1"),
                        opt("Scope 2"),
                        opt("Scope 3", correct=True),
                        opt("They are excluded from inventories"),
                    ),
                    "Scope 3 is all other indirect emissions and is usually the largest share.",
                ),
                q(
                    "What is the core emissions calculation in a GHG inventory?",
                    (
                        opt("Hazard times exposure"),
                        opt(
                            "Activity data multiplied by an emission factor, in CO2e",
                            correct=True,
                        ),
                        opt("GDP divided by population"),
                        opt("Solar constant times albedo"),
                    ),
                    "For instance 250000 kWh x 0.075 kg CO2e/kWh = 18.75 t CO2e.",
                ),
                q(
                    "In the Kaya identity, clean energy directly lowers which term?",
                    (
                        opt("Population"),
                        opt("Affluence (GDP per person)"),
                        opt("Carbon intensity (CO2 / Energy)", correct=True),
                        opt("The functional unit"),
                    ),
                    "Efficiency lowers energy intensity; clean energy lowers carbon intensity.",
                ),
                q(
                    "What must be defined first in an ISO 14040 life-cycle assessment?",
                    (
                        opt("The colour of the packaging"),
                        opt(
                            "The goal, functional unit and system boundary",
                            correct=True,
                        ),
                        opt("The stock price of the company"),
                        opt("The grid frequency"),
                    ),
                    "Functional unit and boundary decide the answer, so they are set in "
                    "the goal-and-scope phase.",
                ),
                q(
                    "How is a product carbon footprint aggregated across gases?",
                    (
                        opt("Sum of raw masses"),
                        opt(
                            "Each gas mass times its GWP, summed to CO2e",
                            correct=True,
                        ),
                        opt("Largest single gas only"),
                        opt("Divide by the water footprint"),
                    ),
                    "GWP weights each gas; CH4 and N2O count far more per kilogram than CO2.",
                ),
                q(
                    "The grey water footprint measures what?",
                    (
                        opt("Rainwater used by crops"),
                        opt(
                            "The freshwater needed to dilute pollution back to standards",
                            correct=True,
                        ),
                        opt("Seawater used for cooling"),
                        opt("The mass of the atmosphere"),
                    ),
                    "Grey = pollutant load / (limit - background); blue and green are "
                    "consumptive uses.",
                ),
                q(
                    "A '100-year' flood defence has what chance of being overtopped in 30 years?",
                    (
                        opt("Zero - it is designed to never fail"),
                        opt("Exactly 100 percent"),
                        opt(
                            "About 26 percent, from 1 - (1 - 0.01)^30",
                            correct=True,
                        ),
                        opt("Exactly 1 percent"),
                    ),
                    "Annual 1-in-100 risk compounds to roughly a quarter chance over 30 "
                    "years - and climate change is raising it.",
                ),
                q(
                    "What does climate justice emphasize?",
                    (
                        opt("That adaptation is unnecessary"),
                        opt(
                            "That those who emitted least are often most exposed and "
                            "least able to adapt, so burdens should fall fairly",
                            correct=True,
                        ),
                        opt("That all footprints are equal"),
                        opt("That mitigation and adaptation are the same"),
                    ),
                    "The gap between who caused warming and who suffers it is central to "
                    "fair climate policy.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CLIMATE_CHANGE_CARBON_COURSES: tuple[SeedCourse, ...] = (_CLIMATE_CHANGE_CARBON,)
