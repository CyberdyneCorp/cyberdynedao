"""Academy seed content - Petroleum Refining and Petrochemicals.

An advanced tour of how crude oil and natural gas become fuels and the
chemical building blocks of modern industry. It follows the barrel from
characterization through atmospheric and vacuum distillation, the
conversion units (catalytic cracking, reforming, hydroprocessing,
alkylation, isomerization), into the olefin and aromatic petrochemical
chains, natural gas processing, and finally refinery integration and
economics. Every lesson explains one idea directly, draws it as a mermaid
diagram, and grounds it in a worked balance, yield table or calculation;
each closes with a checkpoint quiz, and a comprehensive final quiz ends
the course.
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


_PETROCHEMICAL_REFINING = SeedCourse(
    slug="petrochemical-refining",
    title="Petroleum Refining & Petrochemicals",
    description=(
        "Converting crude oil and gas into fuels and chemical building blocks "
        "- distillation, catalytic cracking and reforming, hydroprocessing, "
        "and the olefin and aromatic petrochemical chains. Each lesson pairs "
        "a direct explanation with a process diagram and a worked balance, "
        "yield table or calculation grounded in real refinery practice."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Petroleum Refining and Petrochemicals

A **refinery** is a chemical plant that takes one messy feedstock - crude
oil - and separates and rearranges its molecules into a slate of valuable
products: gasoline, jet, diesel, fuel oil, and the light gases that feed
the **petrochemical** industry. Nothing about the crude is wasted if the
configuration is right; the art is matching what the barrel contains to
what the market wants.

This course follows the barrel from the tank farm to the product rack.
The approach is **direct and quantitative**: every lesson explains one
unit or concept, draws it as a diagram, and works a real example - a
mass balance, a yield table, an octane blend, or a short calculation you
could reproduce in a simulator such as **Aspen HYSYS**, **Aspen Plus**,
or the open-source **DWSIM**.

What you will build understanding for, in order:

1. **Crude oil composition and characterization** - what is in the barrel
2. **Atmospheric and vacuum distillation** - the first cut
3. **Catalytic cracking and reforming** - making gasoline and octane
4. **Hydrotreating and hydrocracking** - cleaning and converting with hydrogen
5. **Alkylation and isomerization** - building premium blendstocks
6. **Petrochemical building blocks** - olefins and aromatics
7. **Natural gas processing** - the other feedstock
8. **Refinery integration and economics** - making the whole thing pay

After each lesson there is a short quiz; at the end, a final quiz covers
the whole course. Standards and correlations from **API**, **ASTM**, and
**ISA** appear throughout so the numbers connect to real practice.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a refinery, fundamentally?",
                    (
                        opt("A tank farm that only stores crude oil"),
                        opt(
                            "A chemical plant that separates and rearranges crude oil "
                            "molecules into fuels and petrochemical feedstocks",
                            correct=True,
                        ),
                        opt("A pipeline that transports crude to market"),
                        opt("A drilling rig that extracts oil from the ground"),
                    ),
                    "Refining is separation plus conversion: turn one crude into a slate "
                    "of products matched to demand.",
                ),
                q(
                    "How does this course present each unit?",
                    (
                        opt("Pure theory with no numbers"),
                        opt(
                            "A direct explanation, a process diagram, and a worked "
                            "example such as a mass balance, yield table or calculation",
                            correct=True,
                        ),
                        opt("Only vendor brochures"),
                        opt("Only the history of the oil industry"),
                    ),
                    "Every lesson pairs concept, diagram and a reproducible quantitative example.",
                ),
            ),
        ),
        # -- 1. Crude oil composition ----------------------------------
        _t(
            "Crude oil composition and characterization",
            "11 min",
            """# Crude oil composition and characterization

Crude oil is a complex mixture of **hydrocarbons** plus small amounts of
sulfur, nitrogen, oxygen and metals. The hydrocarbons fall into families:
**paraffins** (straight and branched alkanes), **naphthenes**
(cycloalkanes), **aromatics** (benzene rings) and **asphaltenes** (heavy
polar molecules). The **PONA** analysis reports paraffins, olefins,
naphthenes and aromatics; crude has essentially no olefins, so it is
mostly a PNA mix.

Two numbers dominate how a crude is valued:

- **API gravity** - a density scale. Higher API means lighter (more
  valuable light ends). Light crude is above 31.1 API, heavy below 22.3.
- **Sulfur content** - crude below about 0.5 weight percent sulfur is
  **sweet**; above is **sour**. Sour crude needs more hydroprocessing, so
  it trades at a discount.

API gravity is defined from specific gravity at 60 degrees Fahrenheit:

```text
API gravity = (141.5 / SG_60/60) - 131.5

Example: a crude with specific gravity 0.85
  API = 141.5 / 0.85 - 131.5
      = 166.47 - 131.5
      = 34.97 API   -> a light, desirable crude
```

The single most important characterization tool is the **True Boiling
Point (TBP) curve** (ASTM D2892): a batch distillation that shows the
cumulative volume that boils below each temperature. It tells the refiner
how much of each product cut the crude can yield before any conversion.

```mermaid
graph TD
    CRUDE["Crude oil sample"] --> ASSAY["Crude assay"]
    ASSAY --> API["API gravity and density"]
    ASSAY --> SULF["Sulfur sweet or sour"]
    ASSAY --> TBP["True boiling point curve"]
    ASSAY --> PONA["PONA hydrocarbon families"]
    TBP --> CUTS["Predicted product cut yields"]
```

Remember: the assay - API gravity, sulfur, TBP curve and PONA - is the
refiner's spec sheet for the feedstock. It decides which crudes to buy
and how to run them.
""",
        ),
        quiz_lesson(
            "Quiz: Crude oil composition and characterization",
            (
                q(
                    "What does a higher API gravity indicate about a crude?",
                    (
                        opt("It is heavier and worth less"),
                        opt(
                            "It is lighter and generally more valuable, yielding more "
                            "light products",
                            correct=True,
                        ),
                        opt("It contains more sulfur"),
                        opt("It has more metals and asphaltenes"),
                    ),
                    "API = 141.5/SG - 131.5; higher API means lower density, so lighter "
                    "and usually more valuable.",
                ),
                q(
                    "A crude with 1.8 weight percent sulfur is described as what?",
                    (
                        opt("Sweet"),
                        opt(
                            "Sour - it needs more hydroprocessing and trades at a discount",
                            correct=True,
                        ),
                        opt("Synthetic"),
                        opt("Light by definition"),
                    ),
                    "Below about 0.5 percent sulfur is sweet; higher is sour and costs "
                    "more to clean up. Sulfur level, not gravity, sets the label.",
                ),
                q(
                    "What does the True Boiling Point (TBP) curve tell a refiner?",
                    (
                        opt("The color of the crude"),
                        opt("The price of the crude on the exchange"),
                        opt(
                            "The cumulative volume that boils below each temperature - the "
                            "potential yield of each product cut",
                            correct=True,
                        ),
                        opt("The number of wells needed"),
                    ),
                    "The TBP curve maps how much naphtha, kerosene, diesel and residue "
                    "the crude can give before conversion.",
                ),
            ),
        ),
        # -- 2. Distillation -------------------------------------------
        _t(
            "Atmospheric and vacuum distillation",
            "11 min",
            """# Atmospheric and vacuum distillation

Distillation is the refinery's first and largest separation. It exploits
one fact: different hydrocarbons **boil at different temperatures**.
Heated crude is separated into fractions by boiling range in a tall
**fractionating column** with dozens of trays.

The **Crude Distillation Unit (CDU)** runs near atmospheric pressure.
Crude is preheated against hot products, then fired to about 350-380
degrees Celsius in a furnace and flashed into the column. Light molecules
rise and condense high on cooler trays; heavy molecules stay low. Typical
cuts, lightest to heaviest:

```text
Product cut          Boiling range        Approx yield (light crude)
-------------------  -------------------  --------------------------
Fuel gas + LPG       below 30 C            2-4 vol percent
Light naphtha        30-90 C               6-10 vol percent
Heavy naphtha        90-180 C              12-18 vol percent
Kerosene / jet       180-260 C            10-15 vol percent
Atmospheric gas oil  260-350 C            15-22 vol percent
Atmospheric residue  above 350 C          35-50 vol percent
```

The **atmospheric residue** still holds valuable gas oil, but heating it
hotter at atmospheric pressure would **thermally crack** (coke) the
molecules. The solution is the **Vacuum Distillation Unit (VDU)**: lower
the pressure to roughly 10-40 mmHg absolute, which lowers boiling points,
so heavy gas oils vaporize at furnace temperatures that avoid cracking.

Vacuum splits the residue into **Vacuum Gas Oil (VGO)** - feed for the
cracker - and **Vacuum Residue**, the heaviest bottoms for coking,
asphalt or heavy fuel oil.

```mermaid
graph TD
    CRUDE["Desalted crude"] --> FURN["Furnace heat"]
    FURN --> CDU["Atmospheric column"]
    CDU --> NAP["Naphtha"]
    CDU --> KERO["Kerosene and jet"]
    CDU --> AGO["Atmospheric gas oil"]
    CDU --> ATR["Atmospheric residue"]
    ATR --> VDU["Vacuum column low pressure"]
    VDU --> VGO["Vacuum gas oil to cracker"]
    VDU --> VR["Vacuum residue"]
```

Remember: the CDU makes the first cut at atmospheric pressure; the VDU
recovers more distillate from the residue by lowering the pressure so
heavy molecules boil below their cracking temperature.
""",
        ),
        quiz_lesson(
            "Quiz: Atmospheric and vacuum distillation",
            (
                q(
                    "What physical property does distillation exploit to separate crude?",
                    (
                        opt("Different colors of the fractions"),
                        opt("Different boiling points of the hydrocarbons", correct=True),
                        opt("Different electrical charges"),
                        opt("Different magnetic susceptibilities"),
                    ),
                    "Light molecules boil low and rise; heavy molecules boil high and "
                    "stay down the column.",
                ),
                q(
                    "Why is a vacuum column used for the atmospheric residue instead of "
                    "just heating it hotter at atmospheric pressure?",
                    (
                        opt("Vacuum makes the column cheaper to build"),
                        opt(
                            "Lower pressure lowers boiling points, so heavy gas oils "
                            "vaporize below the temperature at which they would thermally "
                            "crack (coke)",
                            correct=True,
                        ),
                        opt("Vacuum adds hydrogen to the residue"),
                        opt("Atmospheric residue cannot be heated at all"),
                    ),
                    "At about 10-40 mmHg the heavy molecules boil at furnace-safe "
                    "temperatures, avoiding cracking and coking.",
                ),
                q(
                    "What is the main product of the vacuum unit that feeds the catalytic cracker?",
                    (
                        opt("Light naphtha"),
                        opt("Vacuum Gas Oil (VGO)", correct=True),
                        opt("Fuel gas"),
                        opt("Kerosene"),
                    ),
                    "VGO is the classic FCC feed; vacuum residue goes to coking, asphalt "
                    "or heavy fuel oil.",
                ),
            ),
        ),
        # -- 3. Catalytic cracking and reforming -----------------------
        _t(
            "Catalytic cracking and reforming",
            "12 min",
            """# Catalytic cracking and reforming

Distillation only separates what the crude already contains, and most
crudes yield more heavy gas oil than the market wants. **Conversion**
units break big molecules into smaller, more valuable ones, or rearrange
them for quality. Two workhorses do complementary jobs.

**Fluid Catalytic Cracking (FCC)** takes heavy vacuum gas oil and cracks
it into **gasoline** and light olefins over a hot **zeolite catalyst**
(faujasite / Y-zeolite). The catalyst circulates as a fine powder
(fluidized) between a **riser reactor**, where cracking happens in a few
seconds at about 500-540 degrees Celsius, and a **regenerator**, where
coke deposited on the catalyst is burned off - the burn also supplies the
heat the endothermic cracking needs. This coupling makes the FCC nearly
heat-balanced.

**Catalytic Reforming** does not crack for volume - it upgrades **heavy
naphtha into high-octane reformate** and, as a bonus, produces most of a
refinery's **hydrogen**. Over a platinum catalyst (Pt on alumina, often
Pt-Re, hence "Platforming"), low-octane paraffins and naphthenes are
converted to aromatics by **dehydrogenation** and **isomerization**:

```text
Reforming: methylcyclohexane -> toluene + 3 H2   (dehydrogenation)

  C7H14        ->    C7H8    +   3 H2
  RON ~ 71           RON 111       (byproduct hydrogen for hydrotreaters)
```

Aromatics have very high octane, so reformate is a key gasoline
blendstock - and the same aromatics are prized petrochemical feedstocks
(see the BTX lesson).

```mermaid
graph TD
    VGO["Vacuum gas oil"] --> RISER["FCC riser reactor"]
    RISER --> GASO["FCC gasoline and olefins"]
    RISER --> SPENT["Coked catalyst"]
    SPENT --> REGEN["Regenerator burns coke"]
    REGEN --> RISER
    NAP["Heavy naphtha"] --> REF["Catalytic reformer"]
    REF --> REFORMATE["High octane reformate"]
    REF --> H2["Hydrogen byproduct"]
```

Remember: FCC cracks heavy gas oil into gasoline and olefins with a
circulating zeolite catalyst that self-heats by burning its own coke;
reforming upgrades naphtha octane by making aromatics and hands the
refinery its hydrogen.
""",
        ),
        quiz_lesson(
            "Quiz: Catalytic cracking and reforming",
            (
                q(
                    "What does Fluid Catalytic Cracking (FCC) primarily do?",
                    (
                        opt("Separates crude by boiling point"),
                        opt(
                            "Cracks heavy vacuum gas oil into gasoline and light olefins "
                            "over a circulating zeolite catalyst",
                            correct=True,
                        ),
                        opt("Removes sulfur using hydrogen"),
                        opt("Compresses natural gas for transport"),
                    ),
                    "FCC is a volume conversion unit: big heavy molecules become gasoline "
                    "and valuable C3/C4 olefins.",
                ),
                q(
                    "In the FCC, what is the role of the regenerator?",
                    (
                        opt("It adds hydrogen to the feed"),
                        opt(
                            "It burns coke off the spent catalyst, restoring activity and "
                            "supplying heat for the endothermic cracking",
                            correct=True,
                        ),
                        opt("It distills the products"),
                        opt("It cools the catalyst to room temperature"),
                    ),
                    "Coke burn both cleans the catalyst and heat-balances the unit; the "
                    "catalyst circulates back to the riser.",
                ),
                q(
                    "What are the two most valuable outputs of catalytic reforming?",
                    (
                        opt("Asphalt and coke"),
                        opt("Sulfur and nitrogen"),
                        opt(
                            "High-octane reformate (rich in aromatics) and hydrogen",
                            correct=True,
                        ),
                        opt("Water and carbon dioxide"),
                    ),
                    "Reforming converts naphtha to aromatics for octane and generates the "
                    "hydrogen that hydrotreaters need.",
                ),
            ),
        ),
        # -- 4. Hydrotreating and hydrocracking ------------------------
        _t(
            "Hydrotreating and hydrocracking",
            "11 min",
            """# Hydrotreating and hydrocracking

Two conversion processes use **hydrogen** under pressure over a catalyst.
They share equipment ideas but aim at different things: one **cleans**,
the other **cleans and cracks**.

**Hydrotreating** (also hydroprocessing or HDS/HDN) removes contaminants
so a stream meets product specs and does not poison downstream catalysts.
Over a **cobalt-molybdenum** or **nickel-molybdenum** catalyst at roughly
300-400 degrees Celsius and 30-130 bar of hydrogen, sulfur leaves as
hydrogen sulfide, nitrogen as ammonia, and olefins are saturated:

```text
Hydrodesulfurization (HDS) of a thiol:

  R-SH  +  H2   ->   R-H  +  H2S

The H2S is stripped and sent to a Claus sulfur plant, which recovers
elemental sulfur and keeps SO2 emissions within regulation.
```

Deep hydrotreating is what makes today's **ultra-low-sulfur diesel**
(under 10-15 ppm sulfur) and clean gasoline possible.

**Hydrocracking** goes further: at higher pressure (100-200 bar) over a
**dual-function catalyst** (a metal for hydrogenation plus an acidic
zeolite for cracking), heavy vacuum gas oil is both cleaned and cracked
into lighter products. Because hydrogen is added as bonds break, the
products are saturated and clean - excellent jet and diesel. Hydrocracking
is flexible: shift severity to swing the product slate toward more diesel
or more naphtha.

The contrast with FCC: FCC **rejects carbon** (makes coke, produces
olefins, needs little hydrogen); hydrocracking **adds hydrogen** (no coke,
saturated products, hungry for hydrogen).

```mermaid
graph TD
    FEED["Sour distillate or VGO"] --> H2IN["Add hydrogen under pressure"]
    H2IN --> RX["Catalytic reactor"]
    RX --> CLEAN["Cleaned product"]
    RX --> H2S["Hydrogen sulfide to sulfur plant"]
    RX --> NH3["Ammonia"]
    RX --> CRACK["Hydrocracking splits heavy to light"]
    CRACK --> DIESEL["Clean diesel and jet"]
```

Remember: hydrotreating uses hydrogen to strip sulfur and nitrogen to
meet clean-fuel specs; hydrocracking uses more hydrogen and an acidic
catalyst to also crack heavy feed into clean light products - the
hydrogen-adding counterpart to the carbon-rejecting FCC.
""",
        ),
        quiz_lesson(
            "Quiz: Hydrotreating and hydrocracking",
            (
                q(
                    "What is the main purpose of hydrotreating?",
                    (
                        opt("To crack heavy feed into gasoline for volume"),
                        opt(
                            "To remove contaminants such as sulfur and nitrogen with "
                            "hydrogen so streams meet specs and protect downstream catalysts",
                            correct=True,
                        ),
                        opt("To compress natural gas"),
                        opt("To separate crude by boiling point"),
                    ),
                    "HDS/HDN clean the stream; sulfur leaves as H2S, nitrogen as ammonia, "
                    "olefins are saturated.",
                ),
                q(
                    "How does hydrocracking differ from FCC in its use of hydrogen?",
                    (
                        opt("Both reject carbon and make coke"),
                        opt(
                            "Hydrocracking adds hydrogen as bonds break (no coke, "
                            "saturated clean products) while FCC rejects carbon as coke "
                            "and uses little hydrogen",
                            correct=True,
                        ),
                        opt("Hydrocracking uses no catalyst"),
                        opt("FCC operates at higher hydrogen pressure than hydrocracking"),
                    ),
                    "Carbon-rejection (FCC, makes coke and olefins) vs hydrogen-addition "
                    "(hydrocracking, clean saturated products).",
                ),
                q(
                    "Where does the hydrogen sulfide removed during hydrotreating go?",
                    (
                        opt("Straight to the atmosphere"),
                        opt("Blended into the diesel product"),
                        opt(
                            "To a Claus sulfur plant that recovers elemental sulfur and "
                            "limits SO2 emissions",
                            correct=True,
                        ),
                        opt("Back into the crude tank"),
                    ),
                    "The Claus process turns H2S into saleable sulfur and keeps emissions "
                    "within regulation.",
                ),
            ),
        ),
        # -- 5. Alkylation and isomerization ---------------------------
        _t(
            "Alkylation and isomerization",
            "11 min",
            """# Alkylation and isomerization

The FCC and reformer make good gasoline, but a modern gasoline pool also
needs high-octane, **low-vapor-pressure, low-aromatic** blendstock -
especially as regulations cap benzene and volatility. Two acid-catalyzed
units build premium blendstock from light molecules.

**Alkylation** combines a light **olefin** (propylene, butylene from the
FCC) with **isobutane** over a strong acid catalyst - **hydrofluoric
(HF)** or **sulfuric acid**, or newer solid-acid catalysts - to make
**alkylate**, a mixture of branched, highly isomerized paraffins.
Alkylate is a refiner's ideal blendstock: high octane, low vapor
pressure, no olefins, no aromatics, no sulfur.

```text
Alkylation: isobutane + butylene -> isooctane (2,2,4-trimethylpentane)

  i-C4H10  +  C4H8   ->   C8H18
  (RON of isooctane = 100, by definition the octane reference)
```

**Isomerization** rearranges straight-chain **light naphtha** (normal
pentane and hexane) into their **branched isomers**, which have much
higher octane, over a platinum or chlorided-alumina / zeolite catalyst:

```text
Isomerization: n-pentane -> isopentane

  n-C5H12  ->  i-C5H12
  RON  62         92        (a large octane gain from a simple rearrangement)
```

Both units exploit the same chemistry lesson: **branching raises octane**.
The octane number of a blend is estimated by volume-weighted blending:

```python
# Estimate pool RON by volume-weighted blending
components = [
    ("alkylate",   0.25, 96),   # (name, volume fraction, RON)
    ("reformate",  0.35, 98),
    ("isomerate",  0.15, 88),
    ("fcc_gaso",   0.25, 91),
]
pool_ron = sum(frac * ron for _name, frac, ron in components)
print(round(pool_ron, 1))   # -> 94.3 RON pool
```

```mermaid
graph TD
    OLE["Light olefins from FCC"] --> ALK["Alkylation acid catalyst"]
    IC4["Isobutane"] --> ALK
    ALK --> ALKY["Alkylate high octane"]
    LN["Light naphtha n-paraffins"] --> ISOM["Isomerization"]
    ISOM --> ISO["Isomerate high octane"]
    ALKY --> POOL["Gasoline blending pool"]
    ISO --> POOL
```

Remember: alkylation joins light olefins to isobutane for premium
alkylate; isomerization branches light paraffins for octane. Both turn
low-value light ends into clean, high-octane, low-volatility blendstock -
because branching raises octane.
""",
        ),
        quiz_lesson(
            "Quiz: Alkylation and isomerization",
            (
                q(
                    "What does alkylation combine to make alkylate?",
                    (
                        opt("Two aromatic rings"),
                        opt(
                            "A light olefin (such as butylene) with isobutane over a "
                            "strong acid catalyst",
                            correct=True,
                        ),
                        opt("Hydrogen and sulfur"),
                        opt("Methane and steam"),
                    ),
                    "Olefin plus isobutane over HF or sulfuric acid gives branched "
                    "paraffins - high octane, low volatility, no aromatics.",
                ),
                q(
                    "Why does isomerization of n-pentane raise the octane number?",
                    (
                        opt("It adds sulfur"),
                        opt("It removes all the carbon"),
                        opt(
                            "It rearranges the straight chain into a branched isomer, and "
                            "branching raises octane",
                            correct=True,
                        ),
                        opt("It turns the paraffin into an aromatic ring"),
                    ),
                    "n-pentane RON ~62 becomes isopentane RON ~92 by branching alone.",
                ),
                q(
                    "Using volume-weighted blending, what is the pool RON of 50 percent "
                    "reformate at RON 98 and 50 percent alkylate at RON 96?",
                    (
                        opt("94"),
                        opt("97", correct=True),
                        opt("100"),
                        opt("92"),
                    ),
                    "0.5*98 + 0.5*96 = 49 + 48 = 97 RON. Linear volume blending is the "
                    "standard first estimate for octane pooling.",
                ),
            ),
        ),
        # -- 6. Petrochemical building blocks --------------------------
        _t(
            "Petrochemical building blocks (olefins and aromatics)",
            "12 min",
            """# Petrochemical building blocks (olefins and aromatics)

Fuels are most of the barrel by volume, but the highest-value molecules
often leave the refinery as **petrochemical feedstocks**. Almost the
entire chemical industry is built from a handful of building blocks in
two families.

**Olefins** are unsaturated molecules with a reactive carbon-carbon
double bond - **ethylene**, **propylene** and the **C4** olefins
(butadiene, butylenes). Their reactivity makes them the starting point
for polymers. The dominant source is the **steam cracker**: a hydrocarbon
feed (ethane, propane, or naphtha) is mixed with steam and heated to
about 800-850 degrees Celsius for a fraction of a second, then quenched.
Lighter feed favors ethylene; naphtha gives a broader olefin slate.

```text
Steam cracking of ethane to ethylene:

  C2H6   ->   C2H4  +  H2     (highly endothermic, very short residence time)

Ethylene chain:  ethylene -> polyethylene, ethylene oxide, ethylene glycol,
                              vinyl chloride -> PVC, styrene
```

**Aromatics** are the **BTX** group - **benzene, toluene, xylenes** -
recovered mainly from reformate and from steam-cracker pyrolysis
gasoline. They lead to another huge slice of the chemical world:

```text
Aromatic chains:
  benzene   -> styrene, phenol, cyclohexane -> nylon
  para-xylene -> terephthalic acid -> PET polyester (bottles, fiber)
  toluene   -> solvents, or disproportionation back to benzene + xylenes
```

The link back to refining is direct: the reformer that makes octane also
makes BTX, and the FCC and steam cracker make the olefins. A refinery
integrated with a petrochemical complex can shift molecules to whichever
market pays more.

```mermaid
graph TD
    FEED["Ethane propane or naphtha"] --> SC["Steam cracker"]
    SC --> ETH["Ethylene"]
    SC --> PROP["Propylene"]
    SC --> C4["C4 olefins and butadiene"]
    ETH --> PE["Polyethylene and derivatives"]
    PROP --> PP["Polypropylene and derivatives"]
    REF["Reformate and pygas"] --> BTX["Benzene toluene xylenes"]
    BTX --> POLY["Styrene nylon and PET polyester"]
```

Remember: olefins (ethylene, propylene, C4s) from steam cracking and
aromatics (BTX) from reforming are the two building-block families that
feed nearly all plastics, fibers and solvents. The same units that make
fuel quality also make these feedstocks.
""",
        ),
        quiz_lesson(
            "Quiz: Petrochemical building blocks (olefins and aromatics)",
            (
                q(
                    "Which molecules make up the aromatic BTX group?",
                    (
                        opt("Butane, toluene, xenon"),
                        opt("Benzene, toluene, xylenes", correct=True),
                        opt("Butadiene, thiophene, xylose"),
                        opt("Butanol, toluene, xylitol"),
                    ),
                    "BTX = benzene, toluene, xylenes - recovered mainly from reformate "
                    "and pyrolysis gasoline.",
                ),
                q(
                    "What process is the dominant source of ethylene and propylene?",
                    (
                        opt("Vacuum distillation"),
                        opt(
                            "Steam cracking - heating a hydrocarbon feed with steam to "
                            "about 800-850 C for a fraction of a second",
                            correct=True,
                        ),
                        opt("Alkylation"),
                        opt("Claus sulfur recovery"),
                    ),
                    "The steam cracker is the heart of the olefins industry; lighter feed "
                    "favors ethylene.",
                ),
                q(
                    "Para-xylene is the key precursor to which polymer?",
                    (
                        opt("Polyethylene"),
                        opt("PVC"),
                        opt(
                            "PET polyester (bottles and fiber), via terephthalic acid", correct=True
                        ),
                        opt("Nylon"),
                    ),
                    "p-xylene -> terephthalic acid -> PET; benzene leads to styrene and "
                    "nylon precursors instead.",
                ),
            ),
        ),
        # -- 7. Natural gas processing ---------------------------------
        _t(
            "Natural gas processing",
            "11 min",
            """# Natural gas processing

Crude is not the only feedstock. **Natural gas** - mostly **methane**
with heavier hydrocarbons and impurities - is both a fuel and a rich
source of petrochemical feed. Raw gas from the well must be processed
before it can enter a pipeline or a plant.

Raw gas contains **acid gases** (hydrogen sulfide, carbon dioxide),
**water**, and **natural gas liquids (NGLs)** - ethane, propane, butanes
and heavier. Processing removes what must go and recovers what is
valuable, in a standard order:

- **Acid gas removal** (sweetening) - amine units (MEA, MDEA) absorb H2S
  and CO2; the H2S feeds a Claus sulfur plant. Untreated H2S is toxic and
  corrosive and CO2 has no heating value.
- **Dehydration** - glycol (TEG) contactors remove water so it cannot
  form solid **hydrates** or corrode the pipeline.
- **NGL recovery** - a **cryogenic turboexpander** chills the gas to
  around minus 90 degrees Celsius so ethane and heavier condense and are
  separated. The remaining lean gas (mostly methane) meets pipeline spec.
- **Fractionation** - the recovered NGL is split into ethane (steam-cracker
  feed), propane and butane (LPG), and natural gasoline.

A first-pass gas balance shows why recovery matters:

```text
Raw gas basis: 100 mol
  Methane (C1)   88 mol   -> lean pipeline gas / fuel
  Ethane (C2)     6 mol   -> ethylene feedstock (steam cracker)
  Propane (C3)    3 mol   -> LPG
  Butanes (C4)    2 mol   -> LPG / alkylation feed
  CO2 + H2S       1 mol   -> removed (sulfur to Claus)

NGL recovered = C2 + C3 + C4 = 11 mol per 100 mol raw gas
```

Where gas is stranded far from market, it is chilled to about minus 162
degrees Celsius into **Liquefied Natural Gas (LNG)** for shipping, or
converted chemically via **gas-to-liquids** or to methanol and ammonia.

```mermaid
graph TD
    RAW["Raw natural gas"] --> AMINE["Amine acid gas removal"]
    AMINE --> H2S["Hydrogen sulfide to Claus"]
    AMINE --> DEHY["Glycol dehydration"]
    DEHY --> CRYO["Cryogenic NGL recovery"]
    CRYO --> LEAN["Lean pipeline gas methane"]
    CRYO --> NGL["Natural gas liquids"]
    NGL --> FRAC["Fractionation to ethane propane butane"]
```

Remember: gas processing sweetens (amine), dries (glycol), then recovers
NGLs cryogenically. Methane becomes pipeline gas or LNG; the ethane and
LPG it carries are prime petrochemical and fuel feedstocks.
""",
        ),
        quiz_lesson(
            "Quiz: Natural gas processing",
            (
                q(
                    "What is the main component of natural gas?",
                    (
                        opt("Ethane"),
                        opt("Methane", correct=True),
                        opt("Propane"),
                        opt("Carbon dioxide"),
                    ),
                    "Natural gas is mostly methane, with heavier NGLs and impurities mixed in.",
                ),
                q(
                    "Why are amine units used early in gas processing?",
                    (
                        opt("To add sulfur to the gas"),
                        opt(
                            "To remove acid gases (H2S and CO2); H2S is toxic and "
                            "corrosive and feeds the Claus plant, and CO2 has no heating "
                            "value",
                            correct=True,
                        ),
                        opt("To liquefy the methane"),
                        opt("To crack ethane into ethylene"),
                    ),
                    "Sweetening with MEA/MDEA protects equipment and recovers sulfur; "
                    "then the gas is dried and NGLs are recovered.",
                ),
                q(
                    "In the raw-gas balance (100 mol) with 6 mol ethane, 3 mol propane "
                    "and 2 mol butane, how much NGL is recovered per 100 mol?",
                    (
                        opt("6 mol"),
                        opt("9 mol"),
                        opt("11 mol", correct=True),
                        opt("88 mol"),
                    ),
                    "NGL = C2 + C3 + C4 = 6 + 3 + 2 = 11 mol; the rest is lean methane-rich "
                    "pipeline gas.",
                ),
            ),
        ),
        # -- 8. Refinery integration and economics ---------------------
        _t(
            "Refinery integration and economics",
            "12 min",
            """# Refinery integration and economics

A refinery is not a set of independent units - it is an **integrated
system** where one unit's product is the next unit's feed, and the whole
thing has to make money. Two ideas govern how a refinery is designed and
run: **configuration** and **margin**.

**Configuration** describes how much conversion a refinery has:

- **Topping** - distillation only; makes cuts, upgrades nothing.
- **Hydroskimming** - distillation plus reforming and hydrotreating;
  cleans and adds octane but cannot convert heavy residue.
- **Conversion (cracking)** - adds an FCC or hydrocracker to turn heavy
  gas oil into light products.
- **Deep conversion (coking)** - adds a coker to destroy vacuum residue,
  pushing overall light-product yield toward the whole barrel.

More conversion costs more capital but captures the spread between cheap
heavy feed and valuable light products.

The single most watched economic number is the **crack spread**: the
value of the products minus the cost of the crude. A common proxy is the
**3-2-1 crack spread** - three barrels of crude yielding two of gasoline
and one of distillate:

```python
# 3-2-1 crack spread per barrel of crude ($/bbl)
crude       = 80.0    # $/bbl WTI
gasoline    = 105.0   # $/bbl (2 of 3 barrels)
distillate  = 120.0   # $/bbl (1 of 3 barrels)

gross = (2 * gasoline + 1 * distillate) - 3 * crude
crack_spread = gross / 3
print(round(crack_spread, 2))   # -> 30.0 $/bbl gross margin
```

The **net cash margin** subtracts operating costs - the biggest of which
is **energy**, since a refinery burns a few percent of its own throughput
for process heat. Refiners also arbitrage between fuels and
**petrochemicals**: when olefin and aromatic margins beat fuel margins,
an integrated site routes propylene, benzene or naphtha to the chemical
plant instead of the gasoline pool. **Linear programming (LP)** models
optimize this blend of crude selection, unit severity and product routing
across the whole site every day.

```mermaid
graph TD
    CRUDE["Crude selection"] --> CONFIG["Refinery configuration"]
    CONFIG --> UNITS["Integrated units feed each other"]
    UNITS --> FUELS["Fuel products"]
    UNITS --> PETRO["Petrochemical feedstocks"]
    FUELS --> MARGIN["Crack spread margin"]
    PETRO --> MARGIN
    MARGIN --> LP["LP optimization every day"]
    LP --> CRUDE
```

Remember: refinery economics is configuration plus margin. Deeper
conversion captures the light-heavy spread; the crack spread and net cash
margin measure the money; and LP optimization continuously routes each
molecule to fuels or petrochemicals to maximize the value of the barrel.
""",
        ),
        quiz_lesson(
            "Quiz: Refinery integration and economics",
            (
                q(
                    "Which refinery configuration can convert heavy residue into light products?",
                    (
                        opt("Topping - distillation only"),
                        opt("Hydroskimming - distillation plus reforming and hydrotreating"),
                        opt(
                            "Deep conversion - adds a coker (and cracking) to destroy "
                            "vacuum residue and maximize light-product yield",
                            correct=True,
                        ),
                        opt("A tank farm"),
                    ),
                    "Topping and hydroskimming cannot convert residue; cracking and "
                    "coking configurations do.",
                ),
                q(
                    "What does the 3-2-1 crack spread represent?",
                    (
                        opt("Three refineries sharing two crudes and one pipeline"),
                        opt(
                            "A margin proxy: three barrels of crude yielding two of "
                            "gasoline and one of distillate, products minus crude cost",
                            correct=True,
                        ),
                        opt("The ratio of sulfur to nitrogen in the feed"),
                        opt("The number of trays in the crude column"),
                    ),
                    "It approximates gross refining margin per barrel from a typical "
                    "product yield.",
                ),
                q(
                    "With crude at 80, gasoline at 110 and distillate at 130 dollars per "
                    "barrel, what is the 3-2-1 crack spread per barrel of crude?",
                    (
                        opt("Zero"),
                        opt(
                            "About 36.67 dollars per barrel",
                            correct=True,
                        ),
                        opt("Exactly 80 dollars per barrel"),
                        opt("A negative number"),
                    ),
                    "(2*110 + 130 - 3*80)/3 = (220 + 130 - 240)/3 = 110/3 = 36.67. Gross "
                    "margin only; net cash margin subtracts energy and operating costs.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does API gravity measure and what does a high value mean?",
                    (
                        opt("Sulfur content; high means sour"),
                        opt(
                            "A density scale; high API means lighter crude, generally "
                            "more valuable",
                            correct=True,
                        ),
                        opt("Viscosity; high means thicker"),
                        opt("The number of aromatic rings"),
                    ),
                    "API = 141.5/SG - 131.5; higher API is lower density, so lighter and "
                    "usually worth more.",
                ),
                q(
                    "Why does a refinery use a vacuum column after atmospheric distillation?",
                    (
                        opt("To add hydrogen to the residue"),
                        opt(
                            "Lower pressure lowers boiling points so heavy gas oils "
                            "vaporize below their cracking temperature",
                            correct=True,
                        ),
                        opt("To sweeten the crude"),
                        opt("To compress the light gases"),
                    ),
                    "Vacuum recovers VGO from the atmospheric residue without thermally "
                    "cracking (coking) it.",
                ),
                q(
                    "Which unit cracks heavy vacuum gas oil into gasoline and light "
                    "olefins over a circulating zeolite catalyst?",
                    (
                        opt("Catalytic reformer"),
                        opt("Fluid Catalytic Cracker (FCC)", correct=True),
                        opt("Amine sweetening unit"),
                        opt("Vacuum column"),
                    ),
                    "FCC circulates catalyst between riser and regenerator, self-heating "
                    "by burning its own coke.",
                ),
                q(
                    "What two high-value products does catalytic reforming make?",
                    (
                        opt("Asphalt and sulfur"),
                        opt("High-octane reformate (aromatics) and hydrogen", correct=True),
                        opt("Coke and fuel gas"),
                        opt("Water and ammonia"),
                    ),
                    "Reforming upgrades naphtha octane by making aromatics and supplies "
                    "the refinery's hydrogen.",
                ),
                q(
                    "How does hydrocracking differ from FCC?",
                    (
                        opt("Hydrocracking rejects carbon as coke; FCC adds hydrogen"),
                        opt(
                            "Hydrocracking adds hydrogen to make clean saturated products; "
                            "FCC rejects carbon as coke and makes olefins",
                            correct=True,
                        ),
                        opt("They are identical processes"),
                        opt("Neither uses a catalyst"),
                    ),
                    "Hydrogen-addition (clean, no coke) vs carbon-rejection (coke, "
                    "olefins) - complementary conversion routes.",
                ),
                q(
                    "Why does isomerization or alkylation raise gasoline octane?",
                    (
                        opt("They add sulfur to the blend"),
                        opt(
                            "They produce branched paraffins, and branching raises octane",
                            correct=True,
                        ),
                        opt("They remove all hydrogen"),
                        opt("They increase vapor pressure"),
                    ),
                    "Both build branched, clean, low-volatility blendstock; branching is "
                    "the octane driver.",
                ),
                q(
                    "Which two families are the main petrochemical building blocks?",
                    (
                        opt("Paraffins and asphaltenes"),
                        opt("Olefins (ethylene, propylene) and aromatics (BTX)", correct=True),
                        opt("Sulfur and nitrogen compounds"),
                        opt("Water and carbon dioxide"),
                    ),
                    "Olefins from steam cracking and aromatics from reforming feed nearly "
                    "all plastics, fibers and solvents.",
                ),
                q(
                    "What is the correct order of the main natural gas processing steps?",
                    (
                        opt("NGL recovery, then sweetening, then dehydration"),
                        opt(
                            "Acid gas removal (amine), then dehydration (glycol), then "
                            "cryogenic NGL recovery",
                            correct=True,
                        ),
                        opt("Dehydration first, then cracking, then distillation"),
                        opt("Coking, then reforming, then blending"),
                    ),
                    "Sweeten, dry, then chill to recover NGLs; the lean methane meets "
                    "pipeline spec.",
                ),
                q(
                    "Para-xylene from the aromatics chain leads primarily to which product?",
                    (
                        opt("Polyethylene"),
                        opt("PET polyester, via terephthalic acid", correct=True),
                        opt("PVC"),
                        opt("Ammonia"),
                    ),
                    "p-xylene -> terephthalic acid -> PET for bottles and fiber.",
                ),
                q(
                    "What does the 3-2-1 crack spread estimate?",
                    (
                        opt("The sulfur recovery efficiency"),
                        opt(
                            "A gross refining margin proxy: value of two gasoline and one "
                            "distillate barrels minus three barrels of crude",
                            correct=True,
                        ),
                        opt("The number of distillation trays"),
                        opt("The API gravity of the crude"),
                    ),
                    "It approximates margin per barrel; net cash margin then subtracts "
                    "energy and operating costs.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PETROCHEMICAL_REFINING_COURSES: tuple[SeedCourse, ...] = (_PETROCHEMICAL_REFINING,)
