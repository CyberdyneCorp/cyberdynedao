"""Academy seed content - Environmental Process Engineering.

Making chemical processes clean: this course walks through how engineers
keep pollutants out of water, air, and land, and how they close material
loops. It covers environmental regulation and pollution prevention, water
and wastewater treatment, air pollution control, solid and hazardous waste
handling, life-cycle assessment, emissions and carbon accounting, green
chemistry and cleaner production, and resource recovery in the circular
economy. Every lesson is a direct explanation with a design equation or
worked calculation and a mermaid diagram, followed by a checkpoint quiz;
the course closes with a comprehensive final quiz.
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


_ENVIRONMENTAL_PROCESS_ENGINEERING = SeedCourse(
    slug="environmental-process-engineering",
    title="Environmental Process Engineering",
    description=(
        "Making chemical processes clean: water and wastewater treatment, air "
        "pollution control, solid and hazardous waste management, life-cycle "
        "assessment, emissions and carbon accounting, green chemistry and the "
        "circular economy - grounded in real design equations, mass balances "
        "and standards, with a worked calculation and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Process Engineering

Every chemical process takes in raw materials and energy and gives back
products - plus streams you would rather not release: contaminated water,
flue gas, and solid residues. **Environmental process engineering** is the
discipline of designing and operating processes so those unwanted streams
are prevented, minimized, treated, or turned back into resources. It is
regulation, chemistry, and unit operations working together to keep a
plant clean and compliant.

The approach here is **concrete**: every lesson explains one idea directly,
shows it with a real design equation or a worked mass balance, and draws
the process as a diagram. After each lesson there is a short quiz; at the
end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Regulation and pollution prevention** - the rules and the hierarchy
2. **Water and wastewater treatment** - removing pollutants from water
3. **Air pollution control** - cleaning gas streams
4. **Solid and hazardous waste** - treating and stabilizing residues
5. **Life-cycle assessment** - the cradle-to-grave view
6. **Emissions and carbon accounting** - measuring the footprint
7. **Green chemistry and cleaner production** - designing waste out
8. **Resource recovery and the circular economy** - closing the loops

Tools like **Aspen Plus**, **HYSYS**, and open-source **DWSIM** let you
model these operations; standards from the **EPA**, **ISO**, **API**, and
**IUPAC** anchor the practice. Keep the process picture in mind and each
piece slots into place.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is environmental process engineering about?",
                    (
                        opt("Only cleaning up spills after they happen"),
                        opt(
                            "Designing and operating processes so unwanted streams are "
                            "prevented, minimized, treated, or turned back into resources",
                            correct=True,
                        ),
                        opt("Writing environmental laws"),
                        opt("Selling carbon credits"),
                    ),
                    "It spans prevention, minimization, treatment and recovery across "
                    "water, air and solid streams - not just end-of-pipe cleanup.",
                ),
                q(
                    "How is each content lesson structured in this course?",
                    (
                        opt("Only a list of regulations to memorize"),
                        opt(
                            "A direct explanation, a real design equation or worked "
                            "calculation, and a process diagram, then a short quiz",
                            correct=True,
                        ),
                        opt("A video with no text"),
                        opt("Pure history with no engineering"),
                    ),
                    "Explanation + a concrete equation or balance + a mermaid diagram + "
                    "a checkpoint quiz, lesson after lesson.",
                ),
            ),
        ),
        # -- 1. Regulation & pollution prevention ----------------------
        _t(
            "Environmental regulations and pollution prevention",
            "10 min",
            """# Environmental regulations and pollution prevention

Environmental engineering does not start at the end of the pipe - it
starts with the **law** and with a **hierarchy** that says the best waste
is the waste you never make. In the United States the backbone statutes
are the **Clean Water Act** (surface water discharges, via NPDES permits),
the **Clean Air Act** (air emissions), and **RCRA** (solid and hazardous
waste). A discharge **permit** sets numeric **limits** on what a stream
may contain; exceeding them is a violation.

The organizing principle is the **pollution prevention hierarchy**, most
preferred first:

- **Source reduction (prevention)** - change the process, chemistry, or
  inputs so the pollutant is not created. Cheapest and most effective.
- **Reuse and recycling** - keep materials in use instead of discarding.
- **Treatment** - if you must generate it, transform it into something
  less harmful before release.
- **Disposal** - the last resort: landfill or controlled release.

A permit limit is usually a **mass load**, not just a concentration -
because dilution is not treatment. The load is concentration times flow:

```text
Mass load  L = Q * C

Q = 2000 m3/day (flow)
C = 30 mg/L      (pollutant concentration)

Unit-consistent:  30 mg/L = 30 g/m3
L = 2000 m3/day * 30 g/m3 = 60000 g/day = 60 kg/day

Doubling the flow with clean water halves C but leaves L unchanged -
which is why permits cap the load, not just the concentration.
```

```mermaid
graph TD
    P1["Source reduction prevent"] --> P2["Reuse and recycle"]
    P2 --> P3["Treat before release"]
    P3 --> P4["Dispose as last resort"]
    LAW["Permit limits the load"] --> P3
```

Remember: comply with the permit, but climb the hierarchy - preventing a
kilogram of pollutant beats treating it every time.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental regulations and pollution prevention",
            (
                q(
                    "What is the most preferred tier of the pollution prevention hierarchy?",
                    (
                        opt("Disposal to landfill"),
                        opt("End-of-pipe treatment"),
                        opt(
                            "Source reduction - changing the process so the pollutant is "
                            "never created",
                            correct=True,
                        ),
                        opt("Diluting the stream with clean water"),
                    ),
                    "Prevention at the source is cheapest and most effective; treatment "
                    "and disposal sit lower in the hierarchy.",
                ),
                q(
                    "Why do discharge permits cap the mass load, not just the concentration?",
                    (
                        opt("Concentration is impossible to measure"),
                        opt(
                            "Because dilution is not treatment - adding clean water lowers "
                            "concentration but the mass of pollutant released is unchanged",
                            correct=True,
                        ),
                        opt("Because flow is always constant"),
                        opt("To make permits easier to write"),
                    ),
                    "Load L = Q * C; diluting raises Q and lowers C so L stays the same. "
                    "Capping the load closes that loophole.",
                ),
                q(
                    "Which US statute governs hazardous and solid waste?",
                    (
                        opt("The Clean Water Act"),
                        opt("The Clean Air Act"),
                        opt("RCRA - the Resource Conservation and Recovery Act", correct=True),
                        opt("NPDES"),
                    ),
                    "RCRA covers solid and hazardous waste; the Clean Water Act (via "
                    "NPDES permits) covers water discharges and the Clean Air Act covers air.",
                ),
            ),
        ),
        # -- 2. Water & wastewater treatment ---------------------------
        _t(
            "Water and wastewater treatment",
            "11 min",
            """# Water and wastewater treatment

Wastewater treatment removes pollutants in stages, each targeting a
different class of contaminant. The classic municipal train has three:

- **Primary (physical)** - screening and **sedimentation** let heavy
  solids settle and grease float. Removes suspended solids, little else.
- **Secondary (biological)** - microorganisms eat the dissolved organic
  matter, measured as **BOD** (biochemical oxygen demand). The workhorse is
  **activated sludge**: an aerated tank of microbes followed by a clarifier
  that settles the biomass, most of which is recycled.
- **Tertiary (polishing)** - removes nutrients (**nitrogen**,
  **phosphorus**), remaining solids, and pathogens (via filtration and
  **disinfection** - chlorine, UV, or ozone).

The key idea in biological treatment is giving the microbes enough time.
The **hydraulic retention time (HRT)** is simply tank volume over flow:

```text
Hydraulic retention time:  HRT = V / Q

V = 5000 m3   (aeration tank volume)
Q = 20000 m3/day (influent flow)

HRT = 5000 / 20000 = 0.25 day = 6 hours

Removal efficiency for a pollutant:
eta = (C_in - C_out) / C_in

C_in = 250 mg/L BOD, C_out = 20 mg/L BOD
eta = (250 - 20) / 250 = 0.92  ->  92 percent BOD removal
```

Longer retention (or more biomass) generally means more removal, up to a
point; too little and organics pass through untreated.

```mermaid
graph LR
    RAW["Raw wastewater"] --> PRI["Primary settle solids"]
    PRI --> SEC["Secondary activated sludge"]
    SEC --> CLAR["Clarifier settle biomass"]
    CLAR --> TER["Tertiary nutrients and filter"]
    TER --> DIS["Disinfection"]
    DIS --> OUT["Clean effluent"]
    CLAR --> RAS["Return sludge to aeration"]
```

Remember: treat in stages - physical first, biological for the dissolved
organics, then polish. Retention time and biomass set how much BOD you
actually remove.
""",
        ),
        quiz_lesson(
            "Quiz: Water and wastewater treatment",
            (
                q(
                    "What does secondary (biological) treatment such as activated sludge remove?",
                    (
                        opt("Only large floating debris"),
                        opt(
                            "Dissolved organic matter, measured as BOD, using "
                            "microorganisms in an aerated tank",
                            correct=True,
                        ),
                        opt("Only dissolved salts"),
                        opt("Nothing - it is purely decorative"),
                    ),
                    "Microbes consume the dissolved organics (BOD); a clarifier then "
                    "settles the biomass, most of which is recycled.",
                ),
                q(
                    "A 4000 m3 aeration tank treats 16000 m3/day. What is the hydraulic "
                    "retention time?",
                    (
                        opt("4 days"),
                        opt("0.25 day, that is 6 hours", correct=True),
                        opt("16 hours"),
                        opt("1 day"),
                    ),
                    "HRT = V / Q = 4000 / 16000 = 0.25 day = 6 hours.",
                ),
                q(
                    "Influent BOD is 300 mg/L and effluent BOD is 30 mg/L. What is the "
                    "removal efficiency?",
                    (
                        opt("30 percent"),
                        opt("70 percent"),
                        opt("90 percent", correct=True),
                        opt("10 percent"),
                    ),
                    "eta = (300 - 30) / 300 = 270/300 = 0.90 = 90 percent.",
                ),
            ),
        ),
        # -- 3. Air pollution control ----------------------------------
        _t(
            "Air pollution control",
            "11 min",
            """# Air pollution control

Gas streams from combustion and processing carry **particulate matter**
(PM), acid gases like **SOx** and **NOx**, and **volatile organic
compounds** (VOCs). Each pollutant class has a matched control device, and
picking the right one starts with the particle or molecule you must
capture.

For **particulates**:

- **Cyclones** - spin the gas so inertia flings coarse particles to the
  wall. Cheap, but weak on fine PM. Good as a pre-cleaner.
- **Fabric filters (baghouses)** - pass gas through cloth; very high
  efficiency down to fine particles.
- **Electrostatic precipitators (ESPs)** - charge particles and collect
  them on plates; excellent on high volumes of fine PM.

For **gases**:

- **Absorbers (scrubbers)** - dissolve or react the gas into a liquid; a
  limestone scrubber removes SO2 as gypsum (**flue-gas desulfurization**).
- **Adsorbers** - trap VOCs on **activated carbon**.
- **Thermal or catalytic oxidizers** - burn VOCs to CO2 and water.
- **Selective catalytic reduction (SCR)** - converts NOx to N2 with ammonia.

Control devices are rated by **collection efficiency**, and when you put
them in series the penetrations multiply:

```text
Collection efficiency:  eta = 1 - (C_out / C_in)

Series devices - overall penetration is the product of penetrations:
P_total = P1 * P2 = (1 - eta1) * (1 - eta2)
eta_total = 1 - P_total

Cyclone eta1 = 0.70  ->  P1 = 0.30
Baghouse eta2 = 0.99 ->  P2 = 0.01

P_total   = 0.30 * 0.01 = 0.003
eta_total = 1 - 0.003 = 0.997  ->  99.7 percent overall
```

```mermaid
graph LR
    GAS["Dirty flue gas"] --> CYC["Cyclone coarse PM"]
    CYC --> BAG["Baghouse fine PM"]
    BAG --> SCR["Scrubber acid gas"]
    SCR --> OX["Oxidizer or SCR"]
    OX --> STACK["Clean stack gas"]
```

Remember: match the device to the pollutant, use a coarse pre-cleaner
ahead of a fine one, and multiply penetrations to get the overall
efficiency of a train.
""",
        ),
        quiz_lesson(
            "Quiz: Air pollution control",
            (
                q(
                    "Which device is best suited to capturing high volumes of fine "
                    "particulate matter?",
                    (
                        opt("A cyclone alone"),
                        opt(
                            "An electrostatic precipitator or a fabric-filter baghouse",
                            correct=True,
                        ),
                        opt("An SCR unit"),
                        opt("An activated-carbon adsorber"),
                    ),
                    "Cyclones only catch coarse PM; ESPs and baghouses handle fine "
                    "particulate at high efficiency. SCR and carbon target gases, not PM.",
                ),
                q(
                    "A cyclone (70 percent) feeds a baghouse (99 percent) in series. What "
                    "is the overall collection efficiency?",
                    (
                        opt("84.5 percent"),
                        opt("99.7 percent", correct=True),
                        opt("169 percent"),
                        opt("70 percent"),
                    ),
                    "Multiply penetrations: 0.30 * 0.01 = 0.003, so eta = 1 - 0.003 = "
                    "99.7 percent. Efficiencies do not simply add.",
                ),
                q(
                    "What does a limestone scrubber (flue-gas desulfurization) remove?",
                    (
                        opt("Fine particulate only"),
                        opt("NOx by reduction to nitrogen"),
                        opt("SO2, capturing it in a liquid and forming gypsum", correct=True),
                        opt("Carbon dioxide"),
                    ),
                    "FGD absorbers react SO2 with a limestone slurry to make gypsum. NOx "
                    "control is SCR; PM control is filters or ESPs.",
                ),
            ),
        ),
        # -- 4. Solid & hazardous waste --------------------------------
        _t(
            "Solid and hazardous waste treatment",
            "11 min",
            """# Solid and hazardous waste treatment

Not all waste is a stream you can pipe. Solids and sludges - and the
hazardous subset that is toxic, corrosive, ignitable, or reactive - need
their own handling. Under **RCRA**, a waste is either **non-hazardous**
(managed in engineered landfills) or **hazardous** (cradle-to-grave
tracking, licensed treatment).

The main treatment routes:

- **Physical/chemical** - neutralization of acids and bases, precipitation
  of dissolved metals as hydroxides, oxidation or reduction to detoxify.
- **Stabilization and solidification** - bind contaminants (often heavy
  metals) into a solid matrix, usually cement, so they cannot leach.
- **Thermal (incineration)** - high-temperature destruction of organic
  hazardous waste; recovers energy but needs air pollution control on the
  flue gas.
- **Secure landfill** - lined, capped, and monitored disposal for residues
  that cannot be further treated.

Whether a stabilized waste is safe to landfill is decided by a **leaching
test** - the EPA **TCLP** - which simulates rainwater percolating through
the waste. A worked check on a metal-precipitation step:

```text
Metal removal by hydroxide precipitation, then a leachate check.

Influent:  C_in  = 50 mg/L dissolved lead
Effluent:  C_out = 0.5 mg/L after precipitation and filtration

Removal:  eta = (50 - 0.5) / 50 = 0.99 -> 99 percent

Leachate check (TCLP-style) on the solidified sludge:
measured leachate = 2.5 mg/L lead
regulatory limit  = 5.0 mg/L lead
2.5 < 5.0  ->  PASS, may go to a non-hazardous landfill
```

```mermaid
graph TD
    W["Waste stream"] --> CLASS["Classify hazardous or not"]
    CLASS --> PC["Physical and chemical treat"]
    PC --> STAB["Stabilize and solidify"]
    STAB --> TCLP["Leaching test TCLP"]
    TCLP --> LAND["Secure landfill if pass"]
    CLASS --> INC["Incinerate organics"]
    INC --> ASH["Treat ash and flue gas"]
```

Remember: classify first, treat to reduce toxicity and mobility, then
prove with a leaching test that what you landfill will stay put.
""",
        ),
        quiz_lesson(
            "Quiz: Solid and hazardous waste treatment",
            (
                q(
                    "What is the purpose of stabilization and solidification?",
                    (
                        opt("To dilute the waste with water"),
                        opt(
                            "To bind contaminants such as heavy metals into a solid matrix "
                            "so they cannot leach out",
                            correct=True,
                        ),
                        opt("To make the waste burn more easily"),
                        opt("To relabel hazardous waste as non-hazardous without treating it"),
                    ),
                    "Solidification traps contaminants (often in cement) to stop leaching; "
                    "a leaching test then confirms it worked.",
                ),
                q(
                    "A TCLP test measures leachate lead at 2.5 mg/L against a 5.0 mg/L "
                    "limit. What does this mean?",
                    (
                        opt("The waste fails and must be re-treated"),
                        opt(
                            "The waste passes - leachate is below the limit, so it may go "
                            "to a suitable landfill",
                            correct=True,
                        ),
                        opt("The test is invalid"),
                        opt("The lead concentration doubled during the test"),
                    ),
                    "2.5 mg/L is below the 5.0 mg/L regulatory limit, so the stabilized "
                    "waste passes the leaching test.",
                ),
                q(
                    "Under RCRA, how is hazardous waste tracked?",
                    (
                        opt("It is not tracked once it leaves the plant"),
                        opt(
                            "Cradle to grave - from generation through treatment to final "
                            "disposal, with licensed handlers",
                            correct=True,
                        ),
                        opt("Only at the point of disposal"),
                        opt("Only while it is being generated"),
                    ),
                    "RCRA imposes cradle-to-grave tracking so hazardous waste is "
                    "accounted for from generation to final disposal.",
                ),
            ),
        ),
        # -- 5. Life-cycle assessment ----------------------------------
        _t(
            "Life-cycle assessment",
            "11 min",
            """# Life-cycle assessment

Cleaning one pipe can be an illusion if it just moves the burden
elsewhere - a scrubber that removes SO2 but consumes huge electricity may
raise total emissions. **Life-cycle assessment (LCA)** takes the
**cradle-to-grave** view: it tallies environmental impacts across a
product's whole life - raw materials, manufacturing, use, and end of life -
so you optimize the system, not one stage.

LCA is standardized in **ISO 14040/14044** and has four phases:

- **Goal and scope** - what you are studying and the **functional unit**
  (the basis for comparison, e.g. "1 liter of packaged beverage delivered").
- **Inventory analysis (LCI)** - list every input (energy, materials) and
  output (emissions, waste) across the life cycle.
- **Impact assessment (LCIA)** - translate the inventory into impact
  categories: global warming, acidification, eutrophication, water use.
- **Interpretation** - find the hotspots and check the conclusions.

Everything is normalized to the **functional unit** so alternatives are
compared on equal terms:

```text
Compare two cups per one use (the functional unit).

Paper cup:      18 g CO2e per use (made, used once, landfilled)
Ceramic mug:    packed 1050 g CO2e to make; 12 g CO2e per wash

Break-even number of uses N where the mug ties the paper cup:
1050 + 12 N = 18 N
1050 = 6 N
N = 175 uses

Below 175 uses the paper cup wins; above it, the mug wins.
Conclusion depends entirely on the functional unit and lifetime.
```

```mermaid
graph LR
    RAW["Raw material extraction"] --> MFG["Manufacturing"]
    MFG --> USE["Use phase"]
    USE --> EOL["End of life"]
    EOL --> REC["Recycle or dispose"]
    FU["Functional unit"] --> LCIA["Impact per functional unit"]
```

Remember: LCA stops you from shifting burdens between stages. Define the
functional unit, inventory the whole life, and compare on that basis.
""",
        ),
        quiz_lesson(
            "Quiz: Life-cycle assessment",
            (
                q(
                    "What does a cradle-to-grave life-cycle assessment prevent?",
                    (
                        opt("Any use of energy"),
                        opt(
                            "Burden shifting - improving one stage while unknowingly making "
                            "another stage worse overall",
                            correct=True,
                        ),
                        opt("The need for any measurement"),
                        opt("Products from ever being recycled"),
                    ),
                    "LCA tallies impacts across the whole life so you optimize the total, "
                    "not one stage at another stage's expense.",
                ),
                q(
                    "Why is the functional unit central to an LCA?",
                    (
                        opt("It sets the color of the report"),
                        opt(
                            "It is the common basis that lets alternatives be compared on "
                            "equal terms per unit of service delivered",
                            correct=True,
                        ),
                        opt("It is only used for pricing"),
                        opt("It replaces the inventory step"),
                    ),
                    "All inputs and impacts are normalized to the functional unit (e.g. "
                    "one use), so comparisons are fair.",
                ),
                q(
                    "A mug costs 1050 g CO2e to make plus 12 g per wash; a paper cup is 18 "
                    "g per use. After how many uses does the mug break even?",
                    (
                        opt("58 uses"),
                        opt("175 uses", correct=True),
                        opt("1050 uses"),
                        opt("12 uses"),
                    ),
                    "1050 + 12N = 18N gives 6N = 1050, so N = 175 uses to break even.",
                ),
            ),
        ),
        # -- 6. Emissions & carbon accounting --------------------------
        _t(
            "Emissions and carbon accounting",
            "11 min",
            """# Emissions and carbon accounting

You cannot manage what you do not measure. **Carbon accounting** quantifies
a facility's or product's **greenhouse gas** emissions in a common
currency: **CO2 equivalents (CO2e)**, which weights each gas by its
**global warming potential (GWP)**. Methane's 100-year GWP is about 28, so
1 tonne of methane counts as roughly 28 tonnes of CO2e.

The **GHG Protocol** sorts emissions into three **scopes**:

- **Scope 1** - direct emissions from sources you own or control (furnaces,
  process reactions, company vehicles).
- **Scope 2** - indirect emissions from the energy you purchase
  (electricity, steam).
- **Scope 3** - everything else in the value chain (purchased goods,
  transport, product use and disposal). Usually the largest and hardest.

Most emissions are estimated with an **emission factor** - activity data
times an emissions-per-unit figure:

```text
Emissions = Activity data * Emission factor

Scope 1 - natural gas combustion:
fuel burned      = 500000 m3 natural gas
emission factor  = 1.9 kg CO2 per m3
Scope 1 = 500000 * 1.9 = 950000 kg = 950 t CO2

Scope 2 - purchased electricity:
electricity      = 2000 MWh
grid factor      = 0.4 t CO2e per MWh
Scope 2 = 2000 * 0.4 = 800 t CO2e

Convert a methane leak to CO2e (GWP = 28):
10 t CH4 * 28 = 280 t CO2e
```

```mermaid
graph TD
    ACT["Activity data"] --> EF["Emission factor"]
    EF --> CO2E["Emissions in CO2e"]
    S1["Scope 1 direct"] --> CO2E
    S2["Scope 2 purchased energy"] --> CO2E
    S3["Scope 3 value chain"] --> CO2E
    CO2E --> REPORT["Inventory and reduction targets"]
```

Remember: convert everything to CO2e with GWPs, split emissions into the
three scopes, and estimate each with activity data times an emission
factor. That inventory is the baseline every reduction target measures against.
""",
        ),
        quiz_lesson(
            "Quiz: Emissions and carbon accounting",
            (
                q(
                    "What does CO2 equivalent (CO2e) let you do?",
                    (
                        opt("Ignore gases other than CO2"),
                        opt(
                            "Express different greenhouse gases in a common currency by "
                            "weighting each by its global warming potential",
                            correct=True,
                        ),
                        opt("Convert mass into money"),
                        opt("Measure only methane"),
                    ),
                    "CO2e = mass times GWP, so methane, CO2 and others add up on a common "
                    "climate-impact basis.",
                ),
                q(
                    "Purchased electricity emissions fall under which GHG Protocol scope?",
                    (
                        opt("Scope 1"),
                        opt("Scope 2", correct=True),
                        opt("Scope 3"),
                        opt("They are not counted"),
                    ),
                    "Scope 2 covers indirect emissions from purchased energy; Scope 1 is "
                    "direct on-site, Scope 3 is the rest of the value chain.",
                ),
                q(
                    "Burning 500000 m3 of gas at 1.9 kg CO2 per m3 emits how much?",
                    (
                        opt("95 t CO2"),
                        opt("950 t CO2", correct=True),
                        opt("9500 t CO2"),
                        opt("1.9 t CO2"),
                    ),
                    "500000 * 1.9 = 950000 kg = 950 t CO2 (activity data times emission factor).",
                ),
            ),
        ),
        # -- 7. Green chemistry & cleaner production -------------------
        _t(
            "Green chemistry and cleaner production",
            "11 min",
            """# Green chemistry and cleaner production

The cheapest pollutant to control is the one you design out. **Green
chemistry** rethinks the reaction itself, and **cleaner production** does
the same for the whole process, so waste and hazard are prevented at the
source rather than treated later. Anastas and Warner's **twelve principles
of green chemistry** put prevention first: safer solvents, catalysis over
stoichiometric reagents, renewable feedstocks, and designing products to
degrade.

Two quantitative yardsticks tell you how wasteful a synthesis is:

- **Atom economy** - of all the atoms in the reactants, what fraction ends
  up in the desired product. High atom economy means less inherent waste.
- **E-factor** - kilograms of waste produced per kilogram of product.
  Bulk chemicals sit near 1-5; pharmaceuticals can exceed 100.

```text
Atom economy = (mass of desired product atoms / total mass of reactant atoms) * 100

Example - a reaction with product molar mass 180 g/mol from reactants
totaling 250 g/mol of atoms:
atom economy = 180 / 250 * 100 = 72 percent
(28 percent of the reactant mass is destined to become byproduct)

E-factor = total waste mass / product mass
Produce 100 kg product, generate 3500 kg waste (solvents, salts, water):
E-factor = 3500 / 100 = 35 kg waste per kg product

Switching to a catalytic route that cuts solvent waste to 800 kg:
E-factor = 800 / 100 = 8  ->  a large reduction in waste at the source
```

```mermaid
graph LR
    FEED["Feedstock choice"] --> RXN["Reaction design"]
    RXN --> CAT["Catalysis not stoichiometric"]
    CAT --> SOLV["Safer or no solvent"]
    SOLV --> AE["High atom economy"]
    AE --> EF["Low E-factor"]
    EF --> LESS["Less waste to treat"]
```

Remember: measure a synthesis by atom economy and E-factor, then redesign -
catalysis, safer solvents, better feedstocks - so the waste is never made.
Prevention beats treatment on both cost and risk.
""",
        ),
        quiz_lesson(
            "Quiz: Green chemistry and cleaner production",
            (
                q(
                    "What does atom economy measure?",
                    (
                        opt("The monetary cost of atoms"),
                        opt(
                            "The fraction of reactant atoms that end up in the desired "
                            "product - higher means less inherent waste",
                            correct=True,
                        ),
                        opt("The number of reaction steps"),
                        opt("The energy used per reaction"),
                    ),
                    "Atom economy = product atoms over total reactant atoms; a high value "
                    "means little of the input is destined to be byproduct.",
                ),
                q(
                    "A process makes 100 kg of product and generates 3500 kg of waste. "
                    "What is its E-factor?",
                    (
                        opt("0.03"),
                        opt("35 kg waste per kg product", correct=True),
                        opt("3500"),
                        opt("100"),
                    ),
                    "E-factor = waste mass / product mass = 3500 / 100 = 35.",
                ),
                q(
                    "Which idea best captures the core of green chemistry and cleaner production?",
                    (
                        opt("Treat waste more efficiently after the reaction"),
                        opt(
                            "Prevent waste and hazard at the source by redesigning the "
                            "chemistry and process",
                            correct=True,
                        ),
                        opt("Dilute waste before discharge"),
                        opt("Move production to a less regulated country"),
                    ),
                    "Both prevent waste at the source - catalysis, safer solvents, better "
                    "feedstocks - rather than treating it end-of-pipe.",
                ),
            ),
        ),
        # -- 8. Resource recovery & circular economy -------------------
        _t(
            "Resource recovery and the circular economy",
            "11 min",
            """# Resource recovery and the circular economy

The final shift is from a **linear** economy - take, make, use, dispose -
to a **circular** one, where materials and energy loop back instead of
becoming waste. A treatment residue is often a resource in the wrong place:
biogas from a digester, nutrients from wastewater, metals from spent
catalyst, heat from a flue.

Common recovery routes:

- **Energy recovery** - **anaerobic digestion** turns organic waste into
  **biogas** (methane) for power; waste heat drives other processes.
- **Material recovery** - recycle metals, plastics, and glass; recover
  **phosphorus** from wastewater as struvite fertilizer.
- **Water reuse** - treat effluent to a quality fit for cooling, irrigation,
  or even potable reuse, cutting fresh-water draw.
- **Industrial symbiosis** - one plant's waste stream is another plant's
  feedstock (the Kalundborg model).

You judge how circular a system is with **recovery and circularity rates**:

```text
Material recovery rate = recovered mass / total waste mass

Total plastic waste = 1000 t/yr
Recovered and recycled = 650 t/yr
Recovery rate = 650 / 1000 = 0.65 -> 65 percent

Energy from anaerobic digestion:
organic waste       = 2000 t/yr
biogas yield        = 120 m3 biogas per tonne
methane content     = 60 percent -> 0.60 volume fraction
energy of methane   = 36 MJ per m3

Methane volume = 2000 * 120 * 0.60 = 144000 m3/yr
Energy         = 144000 * 36 = 5184000 MJ/yr = 5184 GJ/yr recovered
```

```mermaid
graph LR
    WASTE["Process and organic waste"] --> AD["Anaerobic digestion"]
    AD --> BIO["Biogas energy"]
    WASTE --> MAT["Material recovery"]
    MAT --> FEED["Feedstock for another plant"]
    EFF["Treated effluent"] --> REUSE["Water reuse"]
    BIO --> LOOP["Close the loop"]
    FEED --> LOOP
    REUSE --> LOOP
```

Remember: in a circular economy waste is a misplaced resource. Recover
energy, materials, and water, feed one plant's output into another's
input, and measure progress with recovery and circularity rates.
""",
        ),
        quiz_lesson(
            "Quiz: Resource recovery and the circular economy",
            (
                q(
                    "What is the core idea of a circular economy?",
                    (
                        opt("Take, make, use, dispose as fast as possible"),
                        opt(
                            "Loop materials and energy back into use so waste becomes a "
                            "resource instead of being disposed",
                            correct=True,
                        ),
                        opt("Ban all manufacturing"),
                        opt("Only recycle paper"),
                    ),
                    "Circular thinking closes loops - energy, material and water recovery, "
                    "and industrial symbiosis - versus the linear take-make-dispose model.",
                ),
                q(
                    "Anaerobic digestion of organic waste primarily produces what useful output?",
                    (
                        opt("Chlorine gas"),
                        opt("Biogas (methane) that can be burned for energy", correct=True),
                        opt("Pure hydrogen only"),
                        opt("Drinking water"),
                    ),
                    "Digestion converts organic waste to methane-rich biogas, an energy "
                    "recovery route.",
                ),
                q(
                    "650 t of 1000 t of plastic waste are recycled. What is the material "
                    "recovery rate?",
                    (
                        opt("35 percent"),
                        opt("65 percent", correct=True),
                        opt("6.5 percent"),
                        opt("100 percent"),
                    ),
                    "Recovery rate = recovered / total = 650 / 1000 = 0.65 = 65 percent.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the most preferred tier of the pollution prevention hierarchy?",
                    (
                        opt("Disposal"),
                        opt("End-of-pipe treatment"),
                        opt(
                            "Source reduction - not creating the pollutant in the first place",
                            correct=True,
                        ),
                        opt("Dilution"),
                    ),
                    "Prevention at the source beats reuse, treatment, and disposal on "
                    "both cost and effectiveness.",
                ),
                q(
                    "Why do discharge permits cap mass load rather than concentration alone?",
                    (
                        opt("Concentration cannot be measured"),
                        opt(
                            "Because dilution is not treatment - the load L = Q * C is "
                            "unchanged when you add clean water",
                            correct=True,
                        ),
                        opt("Because flow never varies"),
                        opt("To simplify the paperwork"),
                    ),
                    "Diluting lowers concentration but not the mass discharged; capping "
                    "the load closes that loophole.",
                ),
                q(
                    "Which stage of wastewater treatment uses microorganisms to remove "
                    "dissolved organics (BOD)?",
                    (
                        opt("Primary sedimentation"),
                        opt("Secondary biological treatment, e.g. activated sludge", correct=True),
                        opt("Screening"),
                        opt("Disinfection"),
                    ),
                    "Secondary treatment (activated sludge) is the biological step that "
                    "consumes dissolved organic matter.",
                ),
                q(
                    "Influent BOD is 250 mg/L, effluent is 20 mg/L. What is the removal "
                    "efficiency?",
                    (
                        opt("80 percent"),
                        opt("92 percent", correct=True),
                        opt("20 percent"),
                        opt("8 percent"),
                    ),
                    "eta = (250 - 20) / 250 = 230/250 = 0.92 = 92 percent.",
                ),
                q(
                    "A cyclone at 70 percent feeds a baghouse at 99 percent in series. "
                    "Overall efficiency is closest to:",
                    (
                        opt("85 percent"),
                        opt("99.7 percent", correct=True),
                        opt("169 percent"),
                        opt("70 percent"),
                    ),
                    "Multiply penetrations: 0.30 * 0.01 = 0.003; eta = 1 - 0.003 = 99.7 "
                    "percent. Efficiencies do not add.",
                ),
                q(
                    "A stabilized waste leaches lead at 2.5 mg/L against a 5.0 mg/L TCLP "
                    "limit. The result is:",
                    (
                        opt("A failure - re-treat the waste"),
                        opt("A pass - it may go to a suitable landfill", correct=True),
                        opt("Inconclusive"),
                        opt("A doubling of the lead content"),
                    ),
                    "2.5 mg/L is below the 5.0 mg/L limit, so the leaching test passes.",
                ),
                q(
                    "What does the functional unit provide in a life-cycle assessment?",
                    (
                        opt("The report's file format"),
                        opt(
                            "A common basis of service so alternatives are compared on "
                            "equal terms per unit delivered",
                            correct=True,
                        ),
                        opt("The price of the product"),
                        opt("The color coding of impacts"),
                    ),
                    "Every input and impact is normalized to the functional unit, making "
                    "comparisons fair.",
                ),
                q(
                    "Purchased electricity emissions belong to which GHG Protocol scope?",
                    (
                        opt("Scope 1"),
                        opt("Scope 2", correct=True),
                        opt("Scope 3"),
                        opt("None"),
                    ),
                    "Scope 2 is indirect emissions from purchased energy; Scope 1 is "
                    "direct, Scope 3 is the wider value chain.",
                ),
                q(
                    "A process makes 100 kg of product with 3500 kg of waste. Its E-factor is:",
                    (
                        opt("0.03"),
                        opt("35", correct=True),
                        opt("100"),
                        opt("3500"),
                    ),
                    "E-factor = waste mass / product mass = 3500 / 100 = 35 kg waste per "
                    "kg product.",
                ),
                q(
                    "In a circular economy, a treatment residue such as biogas or "
                    "recovered phosphorus is best seen as:",
                    (
                        opt("A cost to be disposed of as fast as possible"),
                        opt(
                            "A misplaced resource to recover and loop back into use",
                            correct=True,
                        ),
                        opt("Something to dilute and discharge"),
                        opt("Irrelevant to process design"),
                    ),
                    "Circular design recovers energy, materials and water - one plant's "
                    "waste becomes another's feedstock.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_PROCESS_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (
    _ENVIRONMENTAL_PROCESS_ENGINEERING,
)
