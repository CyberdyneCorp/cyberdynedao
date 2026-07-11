"""Academy seed content - Sustainable & Advanced Processes.

The chemical industry's energy transition, taught as one connected story:
why the sector must decarbonize, then the modern levers that do it - green
hydrogen from electrolysis, carbon capture utilization and storage,
electrification and electrochemistry, process intensification, biorefineries
and renewable feedstocks, circular-economy chemical recycling, and the
techno-economic and life-cycle analysis that decides which of these actually
pay off. Every lesson is a direct explanation with a worked design equation
or Python snippet and a mermaid diagram, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz. It leans on modern digital
practice - ML for process optimization, digital twins, and Aspen/DWSIM-style
flowsheet modelling - throughout.
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


_SUSTAINABLE_PROCESSES = SeedCourse(
    slug="sustainable-processes",
    title="Sustainable & Advanced Processes",
    description=(
        "The chemical industry's energy transition, end to end: green "
        "hydrogen from electrolysis, carbon capture utilization and storage, "
        "electrification and electrochemistry, process intensification, "
        "biorefineries and renewable feedstocks, circular-economy chemical "
        "recycling, and the techno-economic and life-cycle analysis that "
        "picks the winners - with worked equations, Python snippets, digital "
        "twins and ML optimization, and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Sustainable & Advanced Processes

The chemical industry turns fossil molecules into the materials modern life
runs on - and in doing so emits roughly **8 percent** of global CO2, split
between the **energy** it burns and the **feedstock carbon** locked into its
products. Decarbonizing it is not one switch; it is a portfolio of new
process technologies, each strong in a different place. This course is the
map of that portfolio.

The approach is **concrete**: every lesson explains one technology directly,
grounds it in a worked design equation or a short Python calculation, and
draws the process as a diagram. After each lesson there is a short quiz; at
the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **The energy transition** - where the emissions are and the levers to cut them
2. **Green hydrogen** - splitting water with renewable electricity
3. **Carbon capture (CCUS)** - separating, using, and storing CO2
4. **Electrification and electrochemistry** - heat and reactions from electrons
5. **Process intensification** - smaller, sharper, more efficient plants
6. **Biorefineries** - carbon from biomass instead of crude oil
7. **Circular economy and chemical recycling** - plastics back to feedstock
8. **Techno-economic and life-cycle analysis** - which options actually pay off

Throughout, we connect to modern digital practice - **Aspen Plus / HYSYS /
DWSIM** flowsheet models, **digital twins**, and **machine learning** for
process optimization - because the new plants are designed and run digitally.
This is the big picture; treat each lesson as the doorway to a field.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Roughly what share of global CO2 emissions does the chemical "
                    "industry account for, and why is it hard to abate?",
                    (
                        opt("About 50 percent, all from electricity use"),
                        opt(
                            "About 8 percent, split between energy burned for heat and "
                            "carbon locked into products as feedstock",
                            correct=True,
                        ),
                        opt("Under 1 percent, so it is not a priority"),
                        opt("About 30 percent, entirely from transport fuels"),
                    ),
                    "The sector's emissions come from both process energy and the "
                    "feedstock carbon in its products - so no single fix covers it.",
                ),
                q(
                    "How is this course structured?",
                    (
                        opt("A single long reference with no exercises"),
                        opt(
                            "One technology per lesson, each with a worked equation or "
                            "Python snippet and a diagram, followed by a checkpoint quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions, no explanations"),
                        opt("It only covers hydrogen"),
                    ),
                    "Each lesson pairs a direct explanation with a concrete calculation "
                    "and a mermaid diagram, then a short quiz.",
                ),
            ),
        ),
        # -- 1. Energy transition --------------------------------------
        _t(
            "The energy transition and the chemical industry",
            "10 min",
            """# The energy transition and the chemical industry

The chemical industry is uniquely hard to decarbonize because it needs
carbon **twice**: as an **energy** source (high-temperature process heat,
often above 500 C for steam cracking and reforming) and as a **feedstock**
(the carbon atoms in plastics, fertilizers, and solvents come from oil, gas,
or coal). You cannot electrify away the atoms in the product.

Emissions come in three **scopes** (GHG Protocol):

- **Scope 1** - direct, from combustion and reactions on site.
- **Scope 2** - indirect, from purchased electricity and steam.
- **Scope 3** - up and down the value chain (feedstock production, product
  end-of-life).

The **abatement levers** map onto the rest of this course:

- **Electrify the heat** - replace fired heaters with electric ones (Lesson 4).
- **Switch the hydrogen** - grey to green H2 (Lesson 2).
- **Capture what remains** - CCUS on concentrated stacks (Lesson 3).
- **Do more with less** - process intensification (Lesson 5).
- **Change the carbon source** - biomass and recycled carbon (Lessons 6-7).

A first quantitative screen is **marginal abatement cost (MAC)** - the cost
to avoid one tonne of CO2. You rank levers cheapest first:

```text
Marginal abatement cost:
  MAC = (annualized cost of option - annualized cost of baseline)
        / (baseline emissions - option emissions)     [USD per tonne CO2]

Worked screen (per year, one furnace):
  Baseline (gas-fired): cost 1.0 M USD, emits 20,000 t CO2
  Electric option:      cost 1.6 M USD, emits  4,000 t CO2 (clean grid)

  MAC = (1.6 - 1.0) M USD / (20,000 - 4,000) t
      = 600,000 USD / 16,000 t
      = 37.5 USD per tonne CO2 avoided

  If the carbon price > 37.5 USD/t, the switch pays for itself.
```

```mermaid
graph TD
    CHEM["Chemical plant emissions"] --> S1["Scope 1 combustion and reactions"]
    CHEM --> S2["Scope 2 purchased power and steam"]
    CHEM --> S3["Scope 3 feedstock and end of life"]
    S1 --> LEVER["Abatement levers"]
    S2 --> LEVER
    S3 --> LEVER
    LEVER --> RANK["Rank by marginal abatement cost"]
```

Remember: the industry needs carbon as both fuel and feedstock, so
decarbonization is a **portfolio** ranked by cost per tonne avoided - not one
silver bullet.
""",
        ),
        quiz_lesson(
            "Quiz: The energy transition and the chemical industry",
            (
                q(
                    "Why is the chemical industry harder to decarbonize than, say, "
                    "electricity generation?",
                    (
                        opt("Its plants are simply older"),
                        opt(
                            "It needs carbon both as an energy source and as the feedstock "
                            "atoms in its products, so electrifying does not remove the "
                            "product carbon",
                            correct=True,
                        ),
                        opt("It uses no electricity at all"),
                        opt("Its emissions are already zero"),
                    ),
                    "Carbon serves double duty - fuel and feedstock - which is why a "
                    "single lever is never enough.",
                ),
                q(
                    "Purchased-electricity emissions fall under which GHG Protocol scope?",
                    (
                        opt("Scope 1"),
                        opt("Scope 2", correct=True),
                        opt("Scope 3"),
                        opt("They are not counted"),
                    ),
                    "Scope 1 is direct on-site, Scope 2 is purchased energy, Scope 3 is "
                    "the wider value chain.",
                ),
                q(
                    "What does the marginal abatement cost (MAC) of an option tell you?",
                    (
                        opt("The total capital cost of the plant"),
                        opt(
                            "The cost to avoid one tonne of CO2, used to rank levers "
                            "cheapest-first against a carbon price",
                            correct=True,
                        ),
                        opt("The market price of the product"),
                        opt("The number of employees needed"),
                    ),
                    "MAC = extra cost divided by tonnes avoided; if the carbon price "
                    "exceeds it, the switch pays.",
                ),
            ),
        ),
        # -- 2. Green hydrogen -----------------------------------------
        _t(
            "Green hydrogen production (electrolysis)",
            "11 min",
            """# Green hydrogen production (electrolysis)

Hydrogen is already a huge industrial commodity (ammonia, methanol,
refining), but today about 95 percent is **grey** - made by **steam methane
reforming (SMR)**, which emits roughly 9-10 kg CO2 per kg H2. Colour codes:

- **Grey** - SMR, CO2 vented.
- **Blue** - SMR with carbon capture (Lesson 3).
- **Green** - **water electrolysis** powered by renewable electricity: no
  direct CO2 at all.

Electrolysis splits water with electricity:

```text
Overall:   2 H2O --> 2 H2 + O2

Thermodynamics (25 C, per mole H2):
  Reversible cell voltage from Gibbs energy:
    E_rev = dG / (n * F)
          = 237,000 J/mol / (2 * 96,485 C/mol)
          = 1.23 V

  Thermoneutral voltage (includes the heat term dH):
    E_tn = dH / (n * F) = 285,800 / (2 * 96,485) = 1.48 V
```

Real cells run above 1.48 V because of **overpotentials** (kinetics,
resistance), so efficiency is what you get for that extra voltage. The main
technologies: **alkaline** (mature, cheap), **PEM** (proton exchange
membrane - responsive, pairs well with variable renewables), and
**solid-oxide (SOEC)** (high temperature, highest efficiency).

Sizing is direct from Faraday's law:

```python
# H2 output and energy for a PEM stack
F = 96485          # C/mol
n = 2              # electrons per H2
LHV_H2 = 33.3      # kWh per kg (lower heating value)

current = 20000    # A (stack)
V_cell = 1.9       # V per cell, real operating point
cells = 100

# mol H2 per second = I / (n*F); *1000 A same idea per stack
mol_per_s = current / (n * F)          # ~0.104 mol/s
kg_per_h = mol_per_s * 2.016 / 1000 * 3600   # ~0.75 kg/h per cell path

power_kW = current * V_cell * cells / 1000    # 380 kW
# Specific energy ~ V_cell / 1.23 * (39.4 kWh/kg HHV basis)
eff = 1.23 / V_cell                     # ~0.65 voltage efficiency
print(round(power_kW, 1), round(eff, 2))
```

```mermaid
graph LR
    REN["Renewable electricity"] --> STACK["Electrolyzer stack"]
    WATER["Purified water"] --> STACK
    STACK --> H2["Green hydrogen"]
    STACK --> O2["Oxygen byproduct"]
    H2 --> USE["Ammonia methanol or fuel"]
    STACK --> LOSS["Losses as heat from overpotential"]
```

Remember: green H2 needs about **50-55 kWh of clean electricity per kg**, so
its cost is dominated by electricity price and how many hours a year the
stack runs - which is why PEM's fast response to cheap renewable power
matters.
""",
        ),
        quiz_lesson(
            "Quiz: Green hydrogen production (electrolysis)",
            (
                q(
                    "What distinguishes 'green' hydrogen from 'grey' and 'blue'?",
                    (
                        opt("Green is just a marketing label with no technical meaning"),
                        opt(
                            "Green is water electrolysis run on renewable electricity "
                            "(no direct CO2); grey is SMR venting CO2; blue is SMR with "
                            "carbon capture",
                            correct=True,
                        ),
                        opt("Green means the hydrogen is coloured with a dye"),
                        opt("Green uses coal, blue uses gas"),
                    ),
                    "The colour tracks the CO2 footprint of the production route, not the "
                    "gas itself.",
                ),
                q(
                    "Why do real electrolyzers operate above the 1.48 V thermoneutral voltage?",
                    (
                        opt("To produce oxygen faster than hydrogen"),
                        opt(
                            "Overpotentials from reaction kinetics and cell resistance "
                            "require extra voltage; that excess sets the efficiency",
                            correct=True,
                        ),
                        opt("Because water boils at that voltage"),
                        opt("It is a safety regulation unrelated to physics"),
                    ),
                    "Voltage efficiency is roughly 1.23 V divided by the actual cell "
                    "voltage; the excess becomes heat.",
                ),
                q(
                    "Which electrolyzer type is especially suited to pairing with "
                    "variable renewable power?",
                    (
                        opt("PEM, because it responds quickly to changing load", correct=True),
                        opt("None - electrolyzers cannot follow variable power"),
                        opt("Only high-temperature units can ever be used"),
                        opt("Grey SMR reactors"),
                    ),
                    "PEM electrolyzers ramp fast, matching intermittent renewable output; "
                    "alkaline is cheaper but slower, SOEC is most efficient but hot. PEM's "
                    "fast dynamic response is the key operational fit for wind and solar.",
                ),
            ),
        ),
        # -- 3. CCUS ---------------------------------------------------
        _t(
            "Carbon capture, utilization and storage (CCUS)",
            "11 min",
            """# Carbon capture, utilization and storage (CCUS)

For emissions you cannot avoid - concentrated process stacks, cement, blue
hydrogen - you **capture** the CO2 and either **use** it or **store** it
underground. Three capture architectures:

- **Post-combustion** - scrub CO2 from flue gas after burning. Most
  retrofittable; the workhorse solvent is **aqueous amine (MEA)**.
- **Pre-combustion** - convert fuel to H2 and CO2 first, capture the CO2
  before combustion (as in blue H2).
- **Oxy-fuel** - burn in pure oxygen so the flue gas is mostly CO2 and water,
  easy to separate.

The dominant post-combustion method is **chemical absorption**: flue gas
contacts an amine solution in an absorber; the rich solvent is heated in a
**stripper** to release pure CO2 and regenerate the amine. The catch is the
**regeneration energy** - boiling the solvent back is the main cost.

```text
Reversible amine reaction (absorb cold, release hot):
    CO2 + 2 R-NH2  <-->  R-NH-COO(-) + R-NH3(+)

Capture rate and energy penalty:
    captured = flue_CO2 * capture_efficiency
    reboiler_duty = captured * q_regen        [GJ]
      MEA q_regen ~ 3.6 GJ per tonne CO2

Worked example (per hour):
    flue_CO2 = 100 t/h, efficiency = 0.90
    captured = 90 t/h
    reboiler_duty = 90 * 3.6 = 324 GJ/h of low-pressure steam
```

That steam is energy diverted from the plant - the **energy penalty**, why
capture is expensive. **Utilization** turns CO2 into products (methanol via
green H2, building aggregates, urea, e-fuels); **storage** injects it into
deep saline aquifers or depleted reservoirs under a caprock, monitored to ISO
27914 geological-storage practice.

```mermaid
graph LR
    FLUE["Flue gas with CO2"] --> ABS["Amine absorber"]
    ABS --> CLEAN["Cleaned gas to stack"]
    ABS --> RICH["Rich solvent"]
    RICH --> STRIP["Stripper with reboiler heat"]
    STRIP --> CO2["Pure CO2 stream"]
    STRIP --> LEAN["Lean solvent recycled"]
    CO2 --> USE["Utilization e-fuels or urea"]
    CO2 --> STORE["Geological storage"]
```

Remember: capture is a **separation** problem dominated by regeneration
energy; the CO2 then goes to **use** (a product) or **storage** (deep
geology) - and the economics hinge on that energy penalty versus the carbon
price.
""",
        ),
        quiz_lesson(
            "Quiz: Carbon capture, utilization and storage (CCUS)",
            (
                q(
                    "In post-combustion amine capture, what is the main cost driver?",
                    (
                        opt("The price of the flue gas"),
                        opt(
                            "The regeneration (reboiler) energy needed to heat the rich "
                            "solvent and release the CO2 - the energy penalty",
                            correct=True,
                        ),
                        opt("The cost of the absorber column steel only"),
                        opt("There is no significant cost"),
                    ),
                    "Boiling the amine back to release CO2 diverts steam from the plant; "
                    "MEA needs roughly 3.6 GJ per tonne captured.",
                ),
                q(
                    "How does oxy-fuel capture differ from post-combustion?",
                    (
                        opt("It captures no CO2 at all"),
                        opt(
                            "It burns fuel in pure oxygen so the flue gas is mostly CO2 "
                            "and water, making separation easy",
                            correct=True,
                        ),
                        opt("It runs the reaction backwards to make fuel"),
                        opt("It only works on hydrogen"),
                    ),
                    "Oxy-fuel changes the combustion so the CO2 is already concentrated; "
                    "post-combustion scrubs dilute flue gas after normal burning.",
                ),
                q(
                    "What is the difference between the U and the S in CCUS?",
                    (
                        opt("They are the same step"),
                        opt(
                            "Utilization turns captured CO2 into products such as "
                            "e-fuels or urea; Storage injects it into deep geology",
                            correct=True,
                        ),
                        opt("Utilization stores it, storage sells it"),
                        opt("Both mean venting it to the atmosphere"),
                    ),
                    "Use makes a product from the CO2; storage locks it underground under "
                    "a caprock with monitoring.",
                ),
            ),
        ),
        # -- 4. Electrification ----------------------------------------
        _t(
            "Electrification and electrochemical processes",
            "10 min",
            """# Electrification and electrochemical processes

Much of a chemical plant's Scope 1 emissions come from **burning fuel to make
heat**. If the grid is clean, replacing that combustion with **electricity**
removes those emissions directly. Two families:

**Electrified heat** - do the same job with electrons:

- **Electric resistance and induction** heaters for furnaces.
- **Industrial heat pumps** - the standout for low-to-medium temperatures.
  A heat pump moves heat rather than making it, so its **coefficient of
  performance (COP)** is well above 1.

```text
Heat pump performance:
    COP = useful heat delivered / electrical work in
    Carnot ceiling: COP_max = T_hot / (T_hot - T_cold)   [kelvin]

Worked example (waste heat 40 C -> process 90 C):
    T_hot = 363 K, T_cold = 313 K
    COP_max = 363 / (363 - 313) = 7.3
    Real COP ~ 0.5 * Carnot ~ 3.6
    => 1 kWh electricity delivers ~3.6 kWh of process heat
```

**Electrochemistry** - drive the *reaction* with electrons instead of a
thermal/catalytic route. The electron becomes the reagent: chlor-alkali
(chlorine and caustic soda) is the classic large-scale example, and emerging
routes do **CO2 electroreduction** to CO or formate and **electrochemical
ammonia**. Selectivity is measured by **Faradaic efficiency** - the fraction
of charge that made the product you wanted rather than a side reaction like
hydrogen evolution.

```python
# Faradaic efficiency for CO2 -> CO
F = 96485
n = 2                 # electrons per CO
charge = 96485 * 3    # C passed (3 mol electrons)
mol_CO_made = 1.2     # measured product
ideal_mol = charge / (n * F)     # 1.5 mol if 100% selective
faradaic_eff = mol_CO_made / ideal_mol
print(round(faradaic_eff, 2))    # 0.80 -> 80% of charge made CO
```

```mermaid
graph TD
    POWER["Clean electricity"] --> HEAT["Electrified heat"]
    POWER --> ECHEM["Electrochemical reactor"]
    HEAT --> HP["Heat pump high COP"]
    HEAT --> RES["Resistance or induction"]
    ECHEM --> PROD["Product from electrons"]
    ECHEM --> FE["Faradaic efficiency selectivity"]
```

Remember: electrify **heat** where a heat pump's COP multiplies each kWh, and
use **electrochemistry** to make electrons the reagent - both only cut
emissions if the electricity is clean.
""",
        ),
        quiz_lesson(
            "Quiz: Electrification and electrochemical processes",
            (
                q(
                    "Why can an industrial heat pump deliver more heat energy than the "
                    "electricity it consumes?",
                    (
                        opt("It creates energy from nothing"),
                        opt(
                            "It moves existing low-grade heat to a higher temperature "
                            "rather than generating heat, so its COP is well above 1",
                            correct=True,
                        ),
                        opt("It secretly burns gas as well"),
                        opt("Its COP is always below 1"),
                    ),
                    "A COP of 3.6 means 1 kWh of electricity delivers about 3.6 kWh of "
                    "process heat by pumping heat uphill.",
                ),
                q(
                    "What does Faradaic efficiency measure in an electrochemical reactor?",
                    (
                        opt("The temperature of the electrolyte"),
                        opt(
                            "The fraction of the electrical charge that produced the "
                            "desired product rather than a side reaction",
                            correct=True,
                        ),
                        opt("The pressure inside the cell"),
                        opt("The cost of the electricity"),
                    ),
                    "It is a selectivity metric: 80 percent Faradaic efficiency means 80 "
                    "percent of the electrons made the target product.",
                ),
                q(
                    "Electrifying process heat only reduces emissions when...",
                    (
                        opt("the equipment is painted green"),
                        opt(
                            "the electricity supplying it is low-carbon; on a dirty grid "
                            "you can simply move the emissions upstream",
                            correct=True,
                        ),
                        opt("the plant runs at night only"),
                        opt("it is never actually beneficial"),
                    ),
                    "Electrification shifts emissions to Scope 2, so a clean grid is the "
                    "precondition for a real cut.",
                ),
            ),
        ),
        # -- 5. Process intensification --------------------------------
        _t(
            "Process intensification",
            "10 min",
            """# Process intensification

**Process intensification (PI)** means redesigning a process to be
dramatically smaller, more efficient, safer, and less energy-hungry - often
by combining steps or using far higher rates of heat and mass transfer.
Instead of a football-field of unit operations, you aim for equipment that is
orders of magnitude more compact.

Key ideas and equipment:

- **Combine operations** - **reactive distillation** does reaction and
  separation in one column (classic for methyl acetate), pushing equilibrium
  by continuously removing product and slashing capital.
- **Intensify transfer** - **microreactors** and **plate reactors** have huge
  surface-to-volume ratios, so heat and mass transfer are fast, reactions are
  safer, and you can run **continuous flow** instead of batch.
- **Novel fields** - **spinning disc** and **rotating packed beds** use
  centrifugal force to intensify contacting.

Why microchannels transfer heat so well - the key is characteristic size:

```text
Heat transfer coefficient scales inversely with channel size:
    Nu = h * d / k       (Nusselt number, ~constant in laminar flow)
    => h = Nu * k / d

Shrink the channel diameter d by 100x  =>  h rises by 100x.

Surface-area-to-volume for a channel:
    a/V = 4 / d
    d = 10 mm  -> a/V = 400  m2/m3
    d = 0.1 mm -> a/V = 40,000 m2/m3   (100x more transfer area)
```

That is why a microreactor can control a violently exothermic reaction that
would be dangerous in a batch vessel: heat is removed as fast as it is made.
Continuous flow also pairs naturally with **digital control** and **process
analytical technology (PAT)** for real-time quality.

```mermaid
graph LR
    BATCH["Large batch train"] --> PI["Process intensification"]
    PI --> RD["Reactive distillation combined steps"]
    PI --> MICRO["Microreactor high transfer"]
    PI --> FLOW["Continuous flow"]
    MICRO --> SAFE["Safer smaller inventory"]
    FLOW --> PAT["Real time quality control"]
```

Remember: PI trades bigger-is-safer for **smaller-is-sharper** - combine
steps, shrink the length scale to multiply transfer, and run continuously,
cutting energy, footprint, and hazardous inventory at once.
""",
        ),
        quiz_lesson(
            "Quiz: Process intensification",
            (
                q(
                    "What is the core idea of process intensification?",
                    (
                        opt("Building the largest possible reactors for economies of scale"),
                        opt(
                            "Redesigning processes to be far smaller, more efficient and "
                            "safer - often by combining steps or intensifying heat and "
                            "mass transfer",
                            correct=True,
                        ),
                        opt("Running everything at higher pressure only"),
                        opt("Adding more manual sampling steps"),
                    ),
                    "PI is about compact, sharper equipment and combined operations, not "
                    "just making units bigger.",
                ),
                q(
                    "Why does shrinking a reactor to microchannel scale improve heat "
                    "transfer so dramatically?",
                    (
                        opt("Smaller channels hold more catalyst"),
                        opt(
                            "The heat transfer coefficient scales inversely with channel "
                            "size and the surface-area-to-volume ratio rises, so transfer "
                            "per unit volume soars",
                            correct=True,
                        ),
                        opt("Small channels change the chemistry of the reaction"),
                        opt("It has no real effect on transfer"),
                    ),
                    "With Nu roughly constant, h scales as k/d and area/volume as 4/d - "
                    "shrinking d multiplies both.",
                ),
                q(
                    "What does reactive distillation combine into one unit?",
                    (
                        opt("Two separate distillation columns"),
                        opt(
                            "Chemical reaction and separation in a single column, driving "
                            "equilibrium by removing product continuously",
                            correct=True,
                        ),
                        opt("Heating and cooling of a batch tank"),
                        opt("Grinding and mixing of solids"),
                    ),
                    "Doing reaction and separation together cuts capital and pushes "
                    "conversion past the equilibrium limit.",
                ),
            ),
        ),
        # -- 6. Biorefineries ------------------------------------------
        _t(
            "Biorefineries and renewable feedstocks",
            "11 min",
            """# Biorefineries and renewable feedstocks

A **biorefinery** is to biomass what an oil refinery is to crude: it takes a
renewable carbon source - crops, wood, agricultural residues, algae, waste -
and fractionates it into fuels, chemicals, and materials. The point is to
change the **feedstock carbon** from fossil to biogenic, addressing the atoms
in the product, not just the process energy.

Feedstock generations:

- **First generation** - sugars, starch, vegetable oils (competes with food).
- **Second generation** - **lignocellulosic** residues (straw, bagasse, wood):
  cellulose, hemicellulose, and lignin. No food competition, but the
  recalcitrant structure is harder to break down.
- **Third generation** - algae and waste streams.

Conversion platforms:

- **Biochemical** - **pretreatment** to open the structure, **enzymatic
  hydrolysis** to sugars, then **fermentation** to ethanol, lactic acid, or
  building blocks. The route to bio-based **succinic acid** and PLA plastics.
- **Thermochemical** - **gasification** to syngas (CO + H2) for catalytic
  synthesis, or **pyrolysis** to bio-oil.

A biorefinery is only sustainable if it is **carbon-efficient**. The key
screen is **atom economy** and carbon yield:

```text
Atom economy (Trost):
    AE = (mass of atoms in desired product / mass of all reactant atoms) * 100%

Fermentation of glucose to ethanol:
    C6H12O6 -> 2 C2H5OH + 2 CO2
    glucose MW = 180.16
    2 ethanol = 2 * 46.07 = 92.14
    AE = 92.14 / 180.16 * 100 = 51.1%
    => ~49% of the carbon mass leaves as CO2 - a hard ceiling for this route
```

That CO2 is biogenic (recently from the air), and it is a **concentrated,
capturable** stream - so fermentation plus CCUS can be net carbon-negative.

```mermaid
graph LR
    BIO["Biomass feedstock"] --> PRE["Pretreatment"]
    PRE --> SUGAR["Sugars from hydrolysis"]
    SUGAR --> FERM["Fermentation"]
    FERM --> PROD["Bio fuels and chemicals"]
    FERM --> CO2["Biogenic CO2 capturable"]
    BIO --> GAS["Gasification to syngas"]
    GAS --> SYN["Catalytic synthesis"]
```

Remember: biorefineries swap **fossil carbon for biogenic carbon**;
lignocellulosic and waste feedstocks avoid the food-versus-fuel trap, and the
carbon yield (atom economy) decides whether a given route is worth building.
""",
        ),
        quiz_lesson(
            "Quiz: Biorefineries and renewable feedstocks",
            (
                q(
                    "What is the defining purpose of a biorefinery in decarbonization?",
                    (
                        opt("To burn biomass for electricity only"),
                        opt(
                            "To change the feedstock carbon in products from fossil to "
                            "biogenic, fractionating biomass into fuels, chemicals and "
                            "materials",
                            correct=True,
                        ),
                        opt("To replace all electrolysis"),
                        opt("To store CO2 underground"),
                    ),
                    "It addresses the carbon atoms in the product, not just process "
                    "energy - biomass in place of crude oil.",
                ),
                q(
                    "Why are second-generation (lignocellulosic) feedstocks preferred "
                    "over first-generation ones?",
                    (
                        opt("They are easier to break down chemically"),
                        opt(
                            "They use residues like straw and wood that do not compete "
                            "with food, though their recalcitrant structure is harder to "
                            "convert",
                            correct=True,
                        ),
                        opt("They contain no carbon"),
                        opt("They require no pretreatment at all"),
                    ),
                    "Lignocellulose avoids the food-versus-fuel problem; the trade-off is "
                    "tougher pretreatment and hydrolysis.",
                ),
                q(
                    "Glucose fermentation to ethanol has an atom economy near 51 percent. "
                    "What does that imply?",
                    (
                        opt("Half the reactor is empty"),
                        opt(
                            "About half the carbon mass leaves as CO2 - a hard yield "
                            "ceiling - but that CO2 is a concentrated biogenic stream "
                            "suited to capture",
                            correct=True,
                        ),
                        opt("The reaction is 51 percent complete"),
                        opt("Only 51 percent of the enzyme is active"),
                    ),
                    "Atom economy caps carbon yield; pairing the capturable CO2 with CCUS "
                    "can make the route net carbon-negative. It is a design-stage screen "
                    "of how much reactant mass ends up in the product.",
                ),
            ),
        ),
        # -- 7. Circular economy & recycling ---------------------------
        _t(
            "Circular economy and chemical recycling",
            "11 min",
            """# Circular economy and chemical recycling

The linear model - **take, make, dispose** - dumps the carbon and value in
products into landfill or incineration. The **circular economy** keeps
materials in use: reduce, reuse, and recycle carbon back into feedstock. For
plastics, the frontier is **chemical recycling**, which complements
mechanical recycling.

- **Mechanical recycling** - grind, melt, and re-mould. Cheap and low-energy,
  but each cycle **degrades** the polymer chains, and mixed or contaminated
  streams are hard to handle. Quality declines - "downcycling."
- **Chemical (advanced) recycling** - break the polymer back down to
  **monomers or feedstock molecules**, then re-polymerize to **virgin-grade**
  material. It handles mixed and dirty streams and closes the loop truly.

Chemical recycling routes:

- **Depolymerization (solvolysis)** - reverse the polymerization chemistry.
  **Glycolysis of PET** cleaves the ester bonds back to the BHET monomer -
  works because PET is a condensation polymer with cleavable linkages.
- **Pyrolysis** - heat mixed plastics without oxygen to a **pyrolysis oil**
  that a steam cracker can use as naphtha substitute. Handles polyolefins
  (PE, PP) that resist solvolysis.
- **Gasification** - to syngas for methanol or synthesis.

A simple **mass-balance** shows why yield and energy matter:

```text
Pyrolysis plant carbon balance (per 100 kg mixed plastic waste):
    Feed carbon:      ~85 kg C
    Pyrolysis oil:    60 kg  (the valuable naphtha substitute)
    Gas (fuel, burned on site): 25 kg
    Char and losses:  15 kg

    Circular carbon efficiency = oil to cracker / feed
                               = 60 / 100 = 60%
    Energy check: the 25 kg of gas often fuels the process,
    so the net electricity or heat import sets the CO2 footprint.
```

The strategy hierarchy is the **waste hierarchy**: prevention and reuse beat
recycling, and all beat energy recovery (incineration) or disposal. Chemical
recycling is not a licence to make more single-use plastic; it is the last
loop-closing step for what cannot be reduced or reused.

```mermaid
graph TD
    WASTE["Mixed plastic waste"] --> SORT["Sort and clean"]
    SORT --> MECH["Mechanical recycling"]
    SORT --> CHEM["Chemical recycling"]
    CHEM --> DEPOLY["Depolymerization to monomer"]
    CHEM --> PYRO["Pyrolysis to feedstock oil"]
    DEPOLY --> VIRGIN["Virgin grade polymer"]
    PYRO --> CRACK["Back to steam cracker"]
```

Remember: mechanical recycling is cheap but downcycles; **chemical recycling
returns plastic to monomers or feedstock** for virgin-grade loops - but it
sits *below* reduce and reuse in the waste hierarchy.
""",
        ),
        quiz_lesson(
            "Quiz: Circular economy and chemical recycling",
            (
                q(
                    "How does chemical recycling differ from mechanical recycling?",
                    (
                        opt("Chemical recycling just melts and re-moulds the plastic"),
                        opt(
                            "Chemical recycling breaks the polymer back to monomers or "
                            "feedstock molecules for virgin-grade material, handling mixed "
                            "and contaminated streams",
                            correct=True,
                        ),
                        opt("They are identical processes"),
                        opt("Chemical recycling always uses less energy"),
                    ),
                    "Mechanical recycling degrades chains each cycle (downcycling); "
                    "chemical recycling rebuilds virgin-grade polymer.",
                ),
                q(
                    "Why is glycolysis effective for recycling PET but not for polyethylene?",
                    (
                        opt("PET is more colourful"),
                        opt(
                            "PET is a condensation polymer with cleavable ester bonds that "
                            "solvolysis can reverse; polyolefins lack such linkages and "
                            "are better suited to pyrolysis",
                            correct=True,
                        ),
                        opt("Polyethylene dissolves instantly in water"),
                        opt("PET cannot be recycled at all"),
                    ),
                    "Route choice follows the polymer chemistry: cleavable bonds favour "
                    "solvolysis, inert C-C chains favour thermal pyrolysis.",
                ),
                q(
                    "Where does chemical recycling sit in the waste hierarchy?",
                    (
                        opt("Above prevention and reuse - it should be the first choice"),
                        opt(
                            "Below reduce and reuse; it closes the loop for what cannot be "
                            "prevented or reused, above incineration and disposal",
                            correct=True,
                        ),
                        opt("It is the same as landfill"),
                        opt("It replaces the need to reduce plastic use"),
                    ),
                    "Prevention and reuse come first; chemical recycling is a loop-closing "
                    "step, not a licence for more single-use plastic.",
                ),
            ),
        ),
        # -- 8. TEA / LCA ----------------------------------------------
        _t(
            "Techno-economic and life-cycle analysis of new processes",
            "11 min",
            """# Techno-economic and life-cycle analysis of new processes

Every technology in this course competes for capital, and "green" is not
enough - a new process must be **economically viable** and deliver a **real**
environmental benefit across its whole life. Two complementary analyses
decide:

- **Techno-economic analysis (TEA)** - is it profitable? Combines capital
  cost (CAPEX), operating cost (OPEX), and revenue over the project life.
- **Life-cycle assessment (LCA)** - is it actually greener? Counts
  environmental impacts from raw material to disposal (**cradle to grave**),
  per ISO 14040/14044, to avoid **burden-shifting** (fixing CO2 while
  worsening water or land use).

The headline TEA metric for an energy product is the **levelized cost** - the
break-even price over the plant's life:

```python
# Levelized cost of hydrogen (LCOH)
capex = 800e6          # USD
opex_yr = 40e6         # USD/year (incl. electricity)
h2_yr = 60000e3        # kg/year
life = 20              # years
rate = 0.08            # discount rate

# capital recovery factor annualizes CAPEX
crf = rate * (1 + rate)**life / ((1 + rate)**life - 1)   # ~0.1019
annual_cost = capex * crf + opex_yr
LCOH = annual_cost / h2_yr
print(round(LCOH, 2))    # ~1.36 USD/kg  (excl. detail; illustrative)
```

For LCA, the analogous metric is the **carbon footprint per unit of product**
(kg CO2-equivalent per kg), summed over every life stage. A green H2 plant on
a *coal* grid can have a worse footprint than grey H2 - LCA catches that;
looking only at the plant gate would miss it.

Modern practice does both digitally: an **Aspen / HYSYS / DWSIM** flowsheet
supplies the mass and energy balances, feeding a TEA spreadsheet and an LCA
model, and increasingly a **digital twin** plus **machine-learning
surrogate** explores thousands of design and operating cases (a Bayesian or
genetic optimizer minimizing cost and CO2 together on a **Pareto frontier**).

```mermaid
graph TD
    FLOW["Flowsheet model Aspen or DWSIM"] --> MB["Mass and energy balance"]
    MB --> TEA["Techno economic analysis"]
    MB --> LCA["Life cycle assessment"]
    TEA --> LCOX["Levelized cost per unit"]
    LCA --> CO2["CO2 equivalent per unit"]
    LCOX --> OPT["ML optimizer Pareto frontier"]
    CO2 --> OPT
```

Remember: **TEA asks 'does it pay?' and LCA asks 'is it truly greener?'** - a
new process must pass both, evaluated cradle-to-grave, and digital
flowsheets, twins, and ML optimizers are how that trade-off is explored today.
""",
        ),
        quiz_lesson(
            "Quiz: Techno-economic and life-cycle analysis of new processes",
            (
                q(
                    "What distinct questions do TEA and LCA answer?",
                    (
                        opt("Both answer whether the process is profitable"),
                        opt(
                            "TEA asks whether it is economically viable (CAPEX, OPEX, "
                            "revenue); LCA asks whether it is genuinely greener across its "
                            "whole life cycle",
                            correct=True,
                        ),
                        opt("Both only measure CO2"),
                        opt("TEA measures water use, LCA measures profit"),
                    ),
                    "A new process must pass both screens - money and true environmental benefit.",
                ),
                q(
                    "Why must LCA be done cradle-to-grave rather than at the plant gate?",
                    (
                        opt("Regulators enjoy long reports"),
                        opt(
                            "To capture upstream and downstream impacts and avoid "
                            "burden-shifting - e.g. green hydrogen made on a coal grid can "
                            "be worse than grey",
                            correct=True,
                        ),
                        opt("Gate-only analysis is always identical to full LCA"),
                        opt("It is only about the plant's own steel"),
                    ),
                    "Full-life accounting exposes hidden upstream emissions and stops one "
                    "impact being fixed while another worsens.",
                ),
                q(
                    "In the levelized-cost calculation, what does the capital recovery factor do?",
                    (
                        opt("It converts CO2 into dollars"),
                        opt(
                            "It annualizes the up-front CAPEX over the project life at the "
                            "discount rate, so it can be added to yearly OPEX",
                            correct=True,
                        ),
                        opt("It measures the plant's efficiency"),
                        opt("It sets the product's market price directly"),
                    ),
                    "CRF spreads the one-time capital cost into an equivalent annual "
                    "charge for the levelized-cost comparison.",
                ),
                q(
                    "How is machine learning used in modern process design here?",
                    (
                        opt("To replace the laws of thermodynamics"),
                        opt(
                            "As a surrogate/optimizer exploring thousands of design and "
                            "operating cases, finding the Pareto frontier that trades cost "
                            "against CO2",
                            correct=True,
                        ),
                        opt("Only to write the final report"),
                        opt("It is never used in this field"),
                    ),
                    "ML surrogates and Bayesian/genetic optimizers search the design space "
                    "far faster than manual case-by-case flowsheeting.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Why does the chemical industry need a portfolio of decarbonization "
                    "levers rather than one fix?",
                    (
                        opt("Because chemists like variety"),
                        opt(
                            "It needs carbon as both energy and feedstock, so different "
                            "levers address heat, hydrogen, capture, and the carbon source "
                            "separately",
                            correct=True,
                        ),
                        opt("Because one plant can only use one machine"),
                        opt("Because emissions are already zero"),
                    ),
                    "Fuel and feedstock carbon are different problems; levers are ranked "
                    "by marginal abatement cost.",
                ),
                q(
                    "What makes hydrogen 'green' rather than 'grey'?",
                    (
                        opt("It is stored at higher pressure"),
                        opt(
                            "It is produced by water electrolysis on renewable "
                            "electricity, with no direct CO2, versus SMR that vents CO2",
                            correct=True,
                        ),
                        opt("It is a different element"),
                        opt("It is cheaper to transport"),
                    ),
                    "Green = renewable-powered electrolysis; grey = steam methane "
                    "reforming venting roughly 9-10 kg CO2 per kg H2.",
                ),
                q(
                    "In amine-based carbon capture, the dominant cost comes from...",
                    (
                        opt("buying the flue gas"),
                        opt(
                            "the reboiler/regeneration energy that heats the solvent to "
                            "release the CO2 - the energy penalty",
                            correct=True,
                        ),
                        opt("painting the columns"),
                        opt("the oxygen produced"),
                    ),
                    "Regenerating the amine (about 3.6 GJ per tonne for MEA) is the "
                    "capture energy penalty.",
                ),
                q(
                    "An industrial heat pump with a COP of 4 means that...",
                    (
                        opt("it wastes three-quarters of its energy"),
                        opt(
                            "each kWh of electricity delivers about 4 kWh of process heat "
                            "by moving heat rather than generating it",
                            correct=True,
                        ),
                        opt("it runs at 4 times the pressure"),
                        opt("it needs four times more electricity than a resistor"),
                    ),
                    "COP above 1 is possible because the pump relocates existing heat "
                    "uphill in temperature.",
                ),
                q(
                    "Faradaic efficiency in an electrochemical reactor describes...",
                    (
                        opt("the reactor temperature"),
                        opt(
                            "the fraction of electrical charge that produced the desired "
                            "product rather than a side reaction",
                            correct=True,
                        ),
                        opt("the electricity price"),
                        opt("the size of the electrodes"),
                    ),
                    "It is the electrochemical selectivity metric.",
                ),
                q(
                    "Shrinking a reactor to microchannel scale improves heat transfer because...",
                    (
                        opt("smaller reactors are always colder"),
                        opt(
                            "the heat transfer coefficient scales as k/d and the "
                            "surface-area-to-volume ratio as 4/d, so smaller channels "
                            "multiply transfer per unit volume",
                            correct=True,
                        ),
                        opt("microchannels change the reaction chemistry"),
                        opt("it has no measurable effect"),
                    ),
                    "This is why process intensification can safely run violently "
                    "exothermic reactions in continuous flow.",
                ),
                q(
                    "The ~51 percent atom economy of glucose-to-ethanol fermentation means...",
                    (
                        opt("the reactor is half full"),
                        opt(
                            "about half the carbon mass leaves as CO2, a yield ceiling - "
                            "but that CO2 is a concentrated biogenic stream that can be "
                            "captured",
                            correct=True,
                        ),
                        opt("the enzyme is half active"),
                        opt("the process is half finished"),
                    ),
                    "Atom economy caps carbon yield; fermentation-plus-CCUS can be net "
                    "carbon-negative.",
                ),
                q(
                    "The main advantage of chemical recycling over mechanical recycling "
                    "is that it...",
                    (
                        opt("always uses less energy"),
                        opt(
                            "breaks plastics back to monomers or feedstock for "
                            "virgin-grade material and can handle mixed, contaminated "
                            "streams",
                            correct=True,
                        ),
                        opt("requires no sorting at all"),
                        opt("is free of any CO2 footprint"),
                    ),
                    "Mechanical recycling downcycles; chemical recycling truly closes the "
                    "loop, though it sits below reduce and reuse.",
                ),
                q(
                    "Why can a full cradle-to-grave LCA reverse the verdict on a 'green' process?",
                    (
                        opt("LCA ignores upstream stages"),
                        opt(
                            "It counts impacts across the whole life cycle, so upstream "
                            "emissions - like a coal grid powering electrolysis - can make "
                            "it worse than the incumbent",
                            correct=True,
                        ),
                        opt("It only looks at the product colour"),
                        opt("It never considers electricity"),
                    ),
                    "Plant-gate thinking misses burden-shifting; LCA per ISO 14040/44 catches it.",
                ),
                q(
                    "How are digital tools used to choose between these new processes?",
                    (
                        opt("They are not used; decisions are made by intuition"),
                        opt(
                            "Flowsheet models (Aspen/DWSIM) feed TEA and LCA, and ML "
                            "surrogates or optimizers explore many cases to trade cost "
                            "against CO2 on a Pareto frontier",
                            correct=True,
                        ),
                        opt("Only to render marketing brochures"),
                        opt("They replace thermodynamics entirely"),
                    ),
                    "Digital twins and ML optimizers search the cost-versus-emissions "
                    "trade-off far faster than manual case work.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SUSTAINABLE_PROCESSES_COURSES: tuple[SeedCourse, ...] = (_SUSTAINABLE_PROCESSES,)
