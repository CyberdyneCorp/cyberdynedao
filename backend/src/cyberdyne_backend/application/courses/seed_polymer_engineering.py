"""Academy seed content - Polymer Science and Engineering.

The science and manufacture of plastics, from the molecule to the machine.
It covers polymer structure and classification, the chain- and step-growth
polymerization mechanisms and the reactors that run them, how molecular
weight and its distribution govern behaviour, thermal and mechanical
properties, industrial processing (extrusion, injection molding),
additives, blends and composites, and the shift to sustainable and
biodegradable polymers. Every lesson is a direct explanation with a
mermaid diagram and a worked equation or calculation, followed by a
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


_POLYMER_ENGINEERING = SeedCourse(
    slug="polymer-engineering",
    title="Polymer Science & Engineering",
    description=(
        "The science and manufacture of plastics - polymer structure, "
        "polymerization mechanisms and reactors, molecular weight, thermal "
        "and mechanical properties, processing by extrusion and injection "
        "molding, additives, blends and composites, and the shift to "
        "sustainable and biodegradable polymers - with worked equations and "
        "a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Polymer Science and Engineering

Plastics are everywhere because polymers are extraordinarily tunable: the
same carbon-and-hydrogen backbone can be a soft food wrap, a rigid pipe,
a stretchy fibre, or a load-bearing composite - depending on the
molecule's architecture and how it was made and shaped. This course takes
you from the **molecule** through the **reactor** to the **machine**, and
finishes on the industry's biggest current challenge: making polymers
**sustainable**.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a worked equation or calculation (a rate law, a mass balance,
a property estimate), and draws the idea as a diagram. After each lesson a
short quiz checks understanding; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Polymer structure and classification** - the vocabulary of chains
2. **Polymerization mechanisms** - chain growth versus step growth
3. **Reactor engineering** - batch, CSTR, and specialized reactors
4. **Molecular weight and its distribution** - Mn, Mw, and dispersity
5. **Thermal and mechanical properties** - Tg, Tm, modulus and strength
6. **Processing** - extrusion and injection molding
7. **Additives, blends and composites** - engineering the final material
8. **Sustainable and biodegradable polymers** - recycling and bioplastics

Grounded throughout in real practice - **IUPAC** naming, the **Arrhenius**
and **Mark-Houwink** relations, **ASTM** test standards, and process
simulators such as **Aspen** and **DWSIM** - but kept teachable.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the overall path this course follows?",
                    (
                        opt("Only the chemistry of a single monomer"),
                        opt(
                            "From the molecule, through the reactor, to the machine, "
                            "and on to sustainability",
                            correct=True,
                        ),
                        opt("Only the recycling of waste plastic"),
                        opt("Only the mechanical testing of finished parts"),
                    ),
                    "The course spans structure, synthesis, reactors, properties, "
                    "processing, and sustainability - molecule to machine.",
                ),
                q(
                    "Why are polymers described as extraordinarily tunable?",
                    (
                        opt("They are all made from the same monomer"),
                        opt(
                            "Architecture and processing let one chemistry become "
                            "materials as different as film, pipe, and fibre",
                            correct=True,
                        ),
                        opt("They never change properties once made"),
                        opt("They can only ever be soft"),
                    ),
                    "Chain architecture plus how a polymer is made and shaped give an "
                    "enormous range of properties.",
                ),
            ),
        ),
        # -- 1. Structure and classification ---------------------------
        _t(
            "Polymer structure and classification",
            "10 min",
            """# Polymer structure and classification

A **polymer** is a large molecule (a macromolecule) built from many
repeating units called **mers**, joined by covalent bonds. The small
molecule that supplies each repeat unit is a **monomer**; the number of
repeat units in a chain is the **degree of polymerization**, n. Ethylene
(the monomer) polymerizes into **polyethylene**, -(CH2-CH2)n-.

Polymers are classified along several independent axes:

- **Backbone chemistry** - **homopolymer** (one repeat unit) versus
  **copolymer** (two or more). Copolymers can be random, alternating,
  block, or graft depending on how the units are sequenced.
- **Chain architecture** - **linear**, **branched**, or **crosslinked**
  (a network). More branching and crosslinking restrict chain motion.
- **Thermal behaviour** - a **thermoplastic** softens and flows on
  heating and can be reshaped repeatedly; a **thermoset** forms a
  permanent crosslinked network that chars rather than melts; an
  **elastomer** is a lightly crosslinked rubber that recovers its shape.
- **Order** - regions can be **amorphous** (tangled, random coil) or
  **semicrystalline** (chains folded into ordered lamellae). Most
  crystallizable polymers are only partly crystalline.

**Tacticity** - the stereochemistry of side groups along the chain -
strongly affects crystallinity: **isotactic** and **syndiotactic**
polypropylene crystallize and are useful; **atactic** polypropylene is a
soft tacky material.

```mermaid
graph TD
    P["Polymers"] --> ARCH["Architecture"]
    P --> THERM["Thermal behaviour"]
    ARCH --> LIN["Linear"]
    ARCH --> BR["Branched"]
    ARCH --> NET["Crosslinked network"]
    THERM --> TP["Thermoplastic reshapeable"]
    THERM --> TS["Thermoset permanent"]
    THERM --> EL["Elastomer rubbery"]
```

A worked example - degree of polymerization from molar masses:

```text
Degree of polymerization
    n = M_polymer / M_repeat_unit

Polyethylene chain of M = 140,000 g/mol
Repeat unit CH2-CH2  ->  M_repeat = 28 g/mol

    n = 140,000 / 28 = 5,000 repeat units per chain
```

Remember: the same atoms give wildly different materials - what changes is
the architecture, the thermal class, and the degree of order.
""",
        ),
        quiz_lesson(
            "Quiz: Polymer structure and classification",
            (
                q(
                    "What distinguishes a thermoplastic from a thermoset?",
                    (
                        opt("Thermoplastics are always stronger"),
                        opt(
                            "A thermoplastic softens and can be reshaped on heating; a "
                            "thermoset is a permanent crosslinked network that will not "
                            "re-melt",
                            correct=True,
                        ),
                        opt("Thermosets contain no carbon"),
                        opt("They are the same thing"),
                    ),
                    "Thermoplastics flow reversibly on heating; thermosets are "
                    "irreversibly crosslinked and char rather than melt.",
                ),
                q(
                    "The degree of polymerization n of a chain is best defined as:",
                    (
                        opt("The mass of one monomer molecule"),
                        opt(
                            "The number of repeat units in the chain - polymer mass "
                            "divided by the repeat-unit mass",
                            correct=True,
                        ),
                        opt("The melting temperature in kelvin"),
                        opt("The number of different monomers used"),
                    ),
                    "n = M_polymer / M_repeat_unit; e.g. 140000 / 28 = 5000 for that "
                    "polyethylene chain.",
                ),
                q(
                    "Why does tacticity matter for polypropylene?",
                    (
                        opt("It changes the colour only"),
                        opt(
                            "Isotactic and syndiotactic chains pack and crystallize into "
                            "a useful solid, while atactic chains stay soft and tacky",
                            correct=True,
                        ),
                        opt("It has no effect on any property"),
                        opt("It only affects the smell"),
                    ),
                    "Stereoregularity controls crystallinity; regular (iso or syndio) "
                    "tacticity enables crystallization.",
                ),
            ),
        ),
        # -- 2. Polymerization mechanisms ------------------------------
        _t(
            "Polymerization mechanisms (chain and step growth)",
            "11 min",
            """# Polymerization mechanisms (chain and step growth)

Two fundamentally different mechanisms build polymer chains, and they
behave in almost opposite ways.

**Chain-growth (addition) polymerization** adds monomers one at a time to
a small number of active chain ends. A typical **free-radical** route has
three stages:

- **Initiation** - an initiator (e.g. a peroxide) decomposes into radicals
  that add to a monomer's double bond, creating an active chain end.
- **Propagation** - the active end rapidly adds monomer after monomer;
  **high-molecular-weight chains form almost instantly**.
- **Termination** - two radicals combine or disproportionate, ending
  growth. Monomer that has not yet reacted is still full-length monomer.

At any moment you have full-size chains plus unreacted monomer; conversion
climbs over time but chain length is high from the start. Polyethylene,
polystyrene, PVC, and PMMA are made this way.

**Step-growth (condensation) polymerization** lets **any** two molecules
with reactive ends react with each other - monomer with monomer, dimer
with trimer, and so on. Chains grow slowly and steadily, and **high
molecular weight appears only at very high conversion**. Nylon and PET
(polyester) are classic examples; many step reactions release a small
molecule such as water.

```mermaid
graph LR
    subgraph CHAIN["Chain growth"]
    I["Initiation"] --> PR["Propagation fast"]
    PR --> TE["Termination"]
    end
    subgraph STEP["Step growth"]
    M["Monomers react in any pair"] --> OL["Oligomers combine"]
    OL --> HI["High MW only near full conversion"]
    end
```

The **Carothers equation** captures the step-growth contrast - average
chain length is set by the fractional conversion p of functional groups:

```text
Carothers equation (step growth, stoichiometric)
    Xn = 1 / (1 - p)          Xn = number-average degree of polymerization

p = 0.90  ->  Xn = 1 / 0.10 = 10       (still short chains)
p = 0.99  ->  Xn = 1 / 0.01 = 100      (useful polymer)
p = 0.999 ->  Xn = 1 / 0.001 = 1000    (needs near-perfect conversion)
```

Remember: chain growth makes long chains early and consumes monomer
gradually; step growth needs near-complete reaction before chains get long.
""",
        ),
        quiz_lesson(
            "Quiz: Polymerization mechanisms (chain and step growth)",
            (
                q(
                    "In free-radical chain-growth polymerization, when do "
                    "high-molecular-weight chains first appear?",
                    (
                        opt("Only at the very end, near full conversion"),
                        opt(
                            "Almost immediately - propagation builds long chains fast "
                            "while unreacted monomer remains",
                            correct=True,
                        ),
                        opt("Never - the chains stay short"),
                        opt("Only if water is removed"),
                    ),
                    "Chain growth gives full-length chains early; conversion rises over "
                    "time but chain length is high from the start.",
                ),
                q(
                    "According to the Carothers equation Xn = 1/(1-p), what conversion "
                    "p is needed for a number-average degree of polymerization of 100?",
                    (
                        opt("p = 0.50"),
                        opt("p = 0.90"),
                        opt("p = 0.99", correct=True),
                        opt("p = 0.10"),
                    ),
                    "Xn = 1/(1-p); for Xn = 100, 1-p = 0.01, so p = 0.99. Step growth "
                    "demands very high conversion.",
                ),
                q(
                    "What is a defining feature of step-growth polymerization?",
                    (
                        opt("Only chain ends react, one monomer at a time"),
                        opt(
                            "Any two molecules with reactive ends can combine, so chains "
                            "grow slowly and reach high MW only near full conversion",
                            correct=True,
                        ),
                        opt("It cannot make nylon or polyester"),
                        opt("It requires a radical initiator"),
                    ),
                    "Monomers, dimers and oligomers all react with each other; molecular "
                    "weight climbs steeply only at high p.",
                ),
            ),
        ),
        # -- 3. Reactor engineering ------------------------------------
        _t(
            "Polymerization reactor engineering",
            "11 min",
            """# Polymerization reactor engineering

Choosing and running the reactor is where chemistry meets chemical
engineering. Polymerizations are strongly **exothermic** and the reacting
mass becomes very **viscous**, so heat removal and mixing dominate the
design.

Four common **process types** decide where the polymer lives:

- **Bulk (mass)** - monomer plus initiator, no solvent. High purity but
  hard to cool as viscosity soars; risk of runaway (the **gel effect**).
- **Solution** - reaction in a solvent that carries away heat and lowers
  viscosity, at the cost of a separation step later.
- **Suspension** - monomer droplets dispersed in water; each droplet is a
  tiny bulk reactor and the water removes heat. Gives beads.
- **Emulsion** - monomer, water, and surfactant micelles; gives high
  molecular weight and a latex, used for paints and adhesives.

Two idealized reactor models bracket real behaviour:

- **Batch / plug-flow** - all molecules see the same reaction history, so
  the molecular-weight distribution is narrower.
- **Continuous stirred tank (CSTR)** - a broad **residence-time
  distribution** means molecules spend very different times reacting,
  broadening the distribution.

```mermaid
graph TD
    FEED["Monomer and initiator"] --> RX["Reactor"]
    RX --> HEAT["Remove exothermic heat"]
    RX --> MIX["Mix rising viscosity"]
    HEAT --> CTRL["Temperature control"]
    MIX --> CTRL
    CTRL --> PROD["Polymer product"]
    CTRL --> RUN["Avoid thermal runaway"]
```

A worked **heat-removal balance** shows why cooling is the constraint:

```text
Heat released by reaction must be removed by the jacket
    Q_rxn = (-dNm/dt) * (-dH_rxn)
    Q_removed = U * A * (T_reactor - T_coolant)

Example (per m3 basis):
    rate of monomer consumed = 2.0 mol/(L.s) = 2000 mol/(m3.s)
    heat of polymerization    = 90,000 J/mol
    Q_rxn = 2000 * 90,000 = 1.8e8 W/m3

With U = 500 W/(m2.K), driving force dT = 30 K:
    area needed per m3 = Q_rxn / (U*dT)
                       = 1.8e8 / (500 * 30) = 12,000 m2/m3
```

That impossibly large area per unit volume is exactly why bulk reactors
are diluted, staged, or run as thin films - heat transfer, not chemistry,
sets the limit.

Remember: polymer reactor design is governed by removing reaction heat and
mixing a thickening mass; the process type and reactor model together set
the product's molecular-weight distribution.
""",
        ),
        quiz_lesson(
            "Quiz: Polymerization reactor engineering",
            (
                q(
                    "Why is heat removal the central challenge in polymerization reactors?",
                    (
                        opt("The reactions absorb large amounts of heat"),
                        opt(
                            "The reactions are strongly exothermic while the mass grows "
                            "very viscous, so cooling and mixing get harder as it "
                            "proceeds",
                            correct=True,
                        ),
                        opt("Polymers only form below room temperature"),
                        opt("Heat has no effect on the product"),
                    ),
                    "Exothermic reaction plus rising viscosity make heat transfer the "
                    "limiting factor and risk thermal runaway.",
                ),
                q(
                    "Compared with a batch/plug-flow reactor, a CSTR tends to produce:",
                    (
                        opt("A narrower molecular-weight distribution"),
                        opt(
                            "A broader distribution, because its wide residence-time "
                            "distribution gives molecules very different reaction times",
                            correct=True,
                        ),
                        opt("No polymer at all"),
                        opt("Only crosslinked networks"),
                    ),
                    "A CSTR's spread of residence times broadens the distribution; batch "
                    "or plug-flow gives every chain a similar history.",
                ),
                q(
                    "In suspension polymerization, what role does the water play?",
                    (
                        opt("It is a monomer"),
                        opt(
                            "It disperses the monomer into droplets and carries away the "
                            "reaction heat, with each droplet acting as a tiny bulk "
                            "reactor",
                            correct=True,
                        ),
                        opt("It stops any reaction from happening"),
                        opt("It replaces the initiator"),
                    ),
                    "Suspension = monomer droplets in water; the water is the heat sink "
                    "and the product comes out as beads.",
                ),
            ),
        ),
        # -- 4. Molecular weight and distribution ----------------------
        _t(
            "Molecular weight and its distribution",
            "11 min",
            """# Molecular weight and its distribution

A synthetic polymer is never one chain length - it is a **distribution**
of lengths. Two averages summarize it, and their ratio measures its width.

- **Number-average molecular weight, Mn** - the total mass divided by the
  number of chains. It weights every chain equally, so short chains count
  as much as long ones. It governs properties that depend on the number of
  molecules (e.g. colligative effects, chain-end concentration).
- **Weight-average molecular weight, Mw** - each chain is weighted by its
  own mass, so long chains dominate. It governs melt viscosity and
  mechanical strength. Always **Mw >= Mn**.

Their ratio is the **dispersity** (formerly polydispersity index):

```text
Dispersity  D = Mw / Mn        (D >= 1)

D = 1.0   perfectly uniform (only living/anionic or nature achieve this)
D ~ 1.1   controlled/living radical polymerization
D ~ 2     ideal step-growth (Flory most-probable distribution)
D = 2-30  typical free-radical / commodity polymers
```

Worked averages for a tiny 3-population sample:

```text
Sample: 10 chains of 1,000 g/mol,  10 of 10,000,  10 of 100,000

Mn = sum(Ni*Mi) / sum(Ni)
   = (10*1000 + 10*10000 + 10*100000) / 30
   = 1,110,000 / 30 = 37,000 g/mol

Mw = sum(Ni*Mi^2) / sum(Ni*Mi)
   = (10*1000^2 + 10*10000^2 + 10*100000^2) / 1,110,000
   = 1.0101e11 / 1.11e6 = 91,000 g/mol

D = Mw/Mn = 91,000 / 37,000 = 2.46
```

Molecular weight is measured by **size-exclusion (gel-permeation)
chromatography (SEC/GPC)**, or estimated from **dilute-solution
viscosity** via the **Mark-Houwink** equation, which links intrinsic
viscosity to a viscosity-average molecular weight:

```text
Mark-Houwink:  [eta] = K * M_v^a
    K, a are constants for a given polymer/solvent/temperature
    a is typically 0.5 (theta solvent) to 0.8 (good solvent)
```

```mermaid
graph LR
    DIST["Chain-length distribution"] --> MN["Mn counts chains"]
    DIST --> MW["Mw weights by mass"]
    MN --> D["Dispersity Mw over Mn"]
    MW --> D
    DIST --> GPC["Measured by GPC or SEC"]
    GPC --> PROP["Predicts viscosity and strength"]
```

Remember: Mn counts molecules, Mw is dominated by the big ones, and their
ratio D tells you how broad the distribution is - which is what controls
processing and strength.
""",
        ),
        quiz_lesson(
            "Quiz: Molecular weight and its distribution",
            (
                q(
                    "How do Mn and Mw differ?",
                    (
                        opt("They are always equal for real polymers"),
                        opt(
                            "Mn weights every chain equally (total mass over number of "
                            "chains); Mw weights each chain by its own mass, so long "
                            "chains dominate",
                            correct=True,
                        ),
                        opt("Mn is always larger than Mw"),
                        opt("Mw ignores the heavy chains"),
                    ),
                    "Mn counts molecules; Mw is mass-weighted, so Mw >= Mn always.",
                ),
                q(
                    "What does a dispersity D = Mw/Mn of 1.0 indicate?",
                    (
                        opt("A very broad range of chain lengths"),
                        opt(
                            "A perfectly uniform sample where all chains are the same length",
                            correct=True,
                        ),
                        opt("That the polymer is crosslinked"),
                        opt("An impossible, invalid value"),
                    ),
                    "D = 1 means monodisperse; commodity free-radical polymers are far "
                    "broader (D of 2 to 30).",
                ),
                q(
                    "Which technique is the standard way to measure a full "
                    "molecular-weight distribution?",
                    (
                        opt("Differential scanning calorimetry"),
                        opt(
                            "Size-exclusion (gel-permeation) chromatography, SEC/GPC",
                            correct=True,
                        ),
                        opt("Tensile testing"),
                        opt("X-ray of the mould"),
                    ),
                    "GPC/SEC separates chains by size to give the distribution; "
                    "Mark-Houwink gives a viscosity-average from solution viscosity.",
                ),
            ),
        ),
        # -- 5. Thermal and mechanical properties ----------------------
        _t(
            "Thermal and mechanical properties",
            "11 min",
            """# Thermal and mechanical properties

How a plastic behaves in use is set by two transition temperatures and by
how its chains resist deformation.

- **Glass transition temperature, Tg** - the temperature below which the
  amorphous regions are a rigid, brittle **glass** and above which they
  become soft and rubbery. It is not melting; it is the onset of
  large-scale chain motion. Polystyrene has Tg near 100 C (rigid at room
  temperature); natural rubber has Tg near -70 C (rubbery at room
  temperature).
- **Melting temperature, Tm** - only **semicrystalline** polymers have a
  Tm, where the ordered crystalline regions melt. Amorphous polymers have
  only a Tg. Service temperature must respect both.

A useful rule of thumb links the two for many polymers:

```text
Tg/Tm rule of thumb (temperatures in KELVIN)
    Tg / Tm  ~  0.5 to 0.66  (symmetric ~ 0.5, asymmetric ~ 0.66)

Polypropylene: Tm = 170 C = 443 K
    estimate Tg ~ 0.6 * 443 = 266 K = -7 C   (measured ~ -10 C, good)
```

Mechanically, a polymer is **viscoelastic** - part solid-elastic, part
viscous-liquid - so response depends on temperature, time, and rate.
Basic stiffness comes from **Young's modulus** (Hooke's law) in the small,
elastic region:

```text
Young's modulus (elastic region)
    E = stress / strain = sigma / epsilon

A tensile bar: force 500 N over area 25 mm2, gauge length 50 mm,
extends 0.20 mm:
    sigma   = 500 / 25e-6  = 2.0e7 Pa = 20 MPa
    epsilon = 0.20 / 50    = 0.004
    E = 20 MPa / 0.004     = 5,000 MPa = 5.0 GPa
```

Because chains relax over time, a constant load gives increasing strain
(**creep**) and a constant strain gives falling stress (**stress
relaxation**) - both measured by **DMA** (dynamic mechanical analysis).
Standard tests include **ASTM D638** (tensile) and **ASTM D256** (Izod
impact). Adding crystallinity or crosslinks raises stiffness and heat
resistance but usually lowers toughness.

```mermaid
graph TD
    T["Temperature"] --> BEL["Below Tg glassy and brittle"]
    T --> BET["Between Tg and Tm rubbery"]
    T --> ABV["Above Tm melt flows"]
    BEL --> USE["Choose service window"]
    BET --> USE
    ABV --> USE
    USE --> VE["Viscoelastic creep and relaxation"]
```

Remember: Tg and Tm bound the service window, modulus sets stiffness, and
viscoelasticity means time and temperature always matter.
""",
        ),
        quiz_lesson(
            "Quiz: Thermal and mechanical properties",
            (
                q(
                    "What happens at the glass transition temperature Tg?",
                    (
                        opt("Crystalline regions melt into a liquid"),
                        opt(
                            "The amorphous regions change from a rigid glass to a soft, "
                            "rubbery state as large-scale chain motion begins",
                            correct=True,
                        ),
                        opt("The polymer decomposes chemically"),
                        opt("The molecular weight doubles"),
                    ),
                    "Tg is the onset of segmental motion in amorphous regions; it is not "
                    "melting (that is Tm, only for semicrystalline polymers).",
                ),
                q(
                    "A bar under 20 MPa stress strains 0.004 elastically. Its Young's modulus is:",
                    (
                        opt("0.08 MPa"),
                        opt("5,000 MPa (5.0 GPa)", correct=True),
                        opt("80 MPa"),
                        opt("0.2 GPa"),
                    ),
                    "E = stress/strain = 20 MPa / 0.004 = 5000 MPa = 5.0 GPa.",
                ),
                q(
                    "Why does a plastic under constant load slowly keep deforming (creep)?",
                    (
                        opt("Because it is perfectly elastic"),
                        opt(
                            "Because it is viscoelastic - the viscous component lets "
                            "chains rearrange over time under load",
                            correct=True,
                        ),
                        opt("Because its molecular weight is falling"),
                        opt("Creep never happens in polymers"),
                    ),
                    "Viscoelasticity means time and temperature matter: constant stress "
                    "gives creep, constant strain gives stress relaxation.",
                ),
            ),
        ),
        # -- 6. Processing ---------------------------------------------
        _t(
            "Polymer processing (extrusion, injection molding)",
            "11 min",
            """# Polymer processing (extrusion, injection molding)

Turning pellets into products means **melting**, **shaping**, and
**solidifying** a polymer - and doing it fast, repeatably, and without
degrading the material. Two processes dominate.

**Extrusion** makes **continuous** profiles - pipe, sheet, film, fibre,
and wire coating. A rotating **screw** inside a heated barrel conveys,
melts (mostly by **shear heating**, not just the barrel heaters), mixes,
and pumps the melt through a shaped **die**. The screw has three zones -
**feed**, **compression** (melting), and **metering** (pressurizing). It
also feeds the pellet stream for injection molding and compounding.

**Injection molding** makes **discrete** parts (bottle caps, housings,
connectors) in a fast repeating cycle: plasticize melt in a
reciprocating-screw barrel, **inject** it under high pressure into a cooled
**mould**, **hold** pressure while it solidifies, **cool**, then **eject**.
Cooling usually dominates the cycle time.

```mermaid
graph LR
    PEL["Pellets in hopper"] --> FEED["Feed zone"]
    FEED --> COMP["Compression zone melts"]
    COMP --> MET["Metering zone pressurizes"]
    MET --> DIE["Extrusion through a die"]
    MET --> INJ["Injection into a mould"]
    DIE --> COOL["Cool and solidify"]
    INJ --> COOL
```

Polymer melts are **shear-thinning** (pseudoplastic): viscosity **falls**
as shear rate rises, which is what lets thick melts fill thin moulds. The
**power-law** model captures it:

```text
Power-law (Ostwald-de Waele) viscosity
    eta = K * (gamma_dot)^(n-1)      n < 1 for shear thinning

K = 10,000 Pa.s^n,  n = 0.4
    at gamma_dot = 10 /s:
        eta = 10000 * 10^(0.4-1) = 10000 * 10^(-0.6) = 2,512 Pa.s
    at gamma_dot = 1000 /s (in the die):
        eta = 10000 * 1000^(-0.6) = 10000 * 0.0158 = 158 Pa.s
```

A 16-fold jump in shear rate drops the viscosity to a fraction - the melt
flows easily where it is sheared hard. **Cooling time** often controls
throughput; for a plate of thickness L it scales as L squared:

```text
Injection cooling time (slab approximation)
    t_cool ~ (L^2 / (pi^2 * alpha)) * ln( (4/pi) * (T_melt - T_mould)/(T_eject - T_mould) )
    -> halving wall thickness cuts cooling time roughly fourfold
```

Common defects tie back to this physics: **warpage** from uneven cooling
and shrinkage, **short shots** from too little pressure or too-high
viscosity, and **degradation** from too much heat or residence time.
Simulators such as **Autodesk Moldflow** predict fill, pack, and warpage.

Remember: extrusion is continuous through a die, injection molding is a
discrete cyclic shot into a mould, and shear-thinning plus cooling govern
how well and how fast a part forms.
""",
        ),
        quiz_lesson(
            "Quiz: Polymer processing (extrusion, injection molding)",
            (
                q(
                    "What is the main difference between extrusion and injection molding?",
                    (
                        opt("Extrusion cannot melt the polymer"),
                        opt(
                            "Extrusion makes continuous profiles through a die; injection "
                            "molding makes discrete parts in a repeating shot into a "
                            "mould",
                            correct=True,
                        ),
                        opt("Injection molding needs no cooling"),
                        opt("They produce identical products"),
                    ),
                    "Extrusion is continuous (pipe, sheet, film); injection molding is a "
                    "cyclic process for discrete parts.",
                ),
                q(
                    "Polymer melts are shear-thinning. What does that mean?",
                    (
                        opt("Viscosity rises as shear rate rises"),
                        opt(
                            "Viscosity falls as shear rate rises, so a thick melt can "
                            "still fill a thin mould where it is sheared hard",
                            correct=True,
                        ),
                        opt("Viscosity is independent of shear rate"),
                        opt("The melt turns solid under shear"),
                    ),
                    "Pseudoplastic behaviour (power-law n < 1): high shear rate lowers "
                    "viscosity, which enables mould filling.",
                ),
                q(
                    "Cooling time in injection molding scales roughly with the square "
                    "of wall thickness. What follows?",
                    (
                        opt("Thicker walls always cool faster"),
                        opt(
                            "Halving the wall thickness cuts cooling time about "
                            "fourfold, so thin, uniform walls speed the cycle",
                            correct=True,
                        ),
                        opt("Wall thickness has no effect on cycle time"),
                        opt("Cooling time depends only on colour"),
                    ),
                    "t_cool scales with L squared, so thin uniform walls dominate "
                    "throughput; uneven cooling also causes warpage.",
                ),
            ),
        ),
        # -- 7. Additives, blends and composites -----------------------
        _t(
            "Additives, blends and composites",
            "10 min",
            """# Additives, blends and composites

Almost no plastic is used as the neat polymer. **Compounding** mixes in
**additives**, other polymers (**blends**), or reinforcements
(**composites**) to hit a cost and performance target.

**Additives** - small amounts that change behaviour:

- **Plasticizers** - small molecules (e.g. phthalates in PVC) that space
  chains apart, lowering Tg and making a rigid polymer flexible.
- **Stabilizers** - **antioxidants** and **UV/light stabilizers** that
  interrupt the free-radical degradation that heat and sunlight cause.
- **Fillers** - cheap particulates (calcium carbonate, talc) that cut cost
  and can stiffen the part.
- **Flame retardants**, **colorants**, **lubricants**, and **antistatics**
  for specific needs.

**Blends** mix two polymers. Most polymer pairs are **immiscible** (they
phase-separate), so a **compatibilizer** - often a block copolymer that
sits at the interface - is added to bond the phases and stop the blend
being brittle. HIPS (rubber-toughened polystyrene) and PC/ABS are famous
blends.

**Composites** disperse a stiff, strong **reinforcement** (glass or carbon
fibre, or particulate) in a polymer **matrix**. The matrix transfers load
into the fibres, which carry most of it. A first estimate of stiffness
along aligned continuous fibres is the **rule of mixtures**:

```text
Rule of mixtures - longitudinal modulus (Voigt, iso-strain)
    E_c = Vf * E_f + (1 - Vf) * E_m

Glass fibre E_f = 73 GPa,  epoxy matrix E_m = 3 GPa,  fibre fraction Vf = 0.5
    E_c = 0.5 * 73 + 0.5 * 3 = 38 GPa

Transverse (iso-stress) is much lower:
    1/E_t = Vf/E_f + (1-Vf)/E_m
    1/E_t = 0.5/73 + 0.5/3 = 0.0068 + 0.1667 = 0.1735
    E_t = 5.8 GPa
```

The huge gap between 38 GPa along the fibres and 5.8 GPa across them is
why composites are **anisotropic** and why fibre orientation is a design
variable.

```mermaid
graph TD
    NEAT["Neat polymer"] --> ADD["Add additives"]
    NEAT --> BL["Blend with another polymer"]
    NEAT --> CO["Reinforce as composite"]
    ADD --> PLAS["Plasticizers and stabilizers"]
    BL --> COMPAT["Needs a compatibilizer"]
    CO --> ROM["Rule of mixtures stiffness"]
    ROM --> ANI["Anisotropic by fibre direction"]
```

Remember: additives tune one polymer, blends marry two (usually needing a
compatibilizer), and composites add a reinforcement whose orientation
makes the part directionally strong.
""",
        ),
        quiz_lesson(
            "Quiz: Additives, blends and composites",
            (
                q(
                    "What does a plasticizer do to a polymer such as PVC?",
                    (
                        opt("Raises its molecular weight"),
                        opt(
                            "Spaces the chains apart, lowering Tg and making a rigid "
                            "polymer flexible",
                            correct=True,
                        ),
                        opt("Makes it crystallize completely"),
                        opt("Acts as a flame retardant only"),
                    ),
                    "Plasticizers lower Tg and increase flexibility; that is how rigid "
                    "PVC becomes flexible vinyl.",
                ),
                q(
                    "For aligned continuous fibres at Vf = 0.5, E_f = 73 GPa and "
                    "E_m = 3 GPa, the rule-of-mixtures longitudinal modulus is:",
                    (
                        opt("3 GPa"),
                        opt("38 GPa", correct=True),
                        opt("73 GPa"),
                        opt("5.8 GPa"),
                    ),
                    "E_c = Vf*E_f + (1-Vf)*E_m = 0.5*73 + 0.5*3 = 38 GPa (the 5.8 GPa is "
                    "the much lower transverse value).",
                ),
                q(
                    "Why is a compatibilizer often needed in a polymer blend?",
                    (
                        opt("To colour the blend"),
                        opt(
                            "Most polymer pairs are immiscible and phase-separate; a "
                            "compatibilizer bonds the phases so the blend is not brittle",
                            correct=True,
                        ),
                        opt("To make the blend conduct electricity"),
                        opt("Blends never need any help"),
                    ),
                    "Immiscible phases give weak, brittle interfaces; a block-copolymer "
                    "compatibilizer sits at the interface and couples the phases.",
                ),
            ),
        ),
        # -- 8. Sustainable and biodegradable polymers -----------------
        _t(
            "Sustainable and biodegradable polymers",
            "11 min",
            """# Sustainable and biodegradable polymers

Most plastic is made from fossil feedstock, used briefly, and discarded -
so the field is shifting toward polymers that are **renewably sourced**,
**recyclable**, or **biodegradable**. These are three different ideas and
are easy to confuse.

- **Bio-based** - made from renewable feedstock (corn, sugarcane, cellulose)
  rather than oil. **Bio-polyethylene** is bio-based but chemically
  identical to fossil PE, so it is **not** biodegradable.
- **Biodegradable** - microbes can break the polymer down into water,
  CO2/CH4, and biomass under defined conditions. **PLA** (polylactic acid),
  **PHA**, and **PBAT** are biodegradable, but often only in **industrial
  composting** (about 58 C), not a home bin or the ocean.
- **Recyclable** - can be reprocessed. **Mechanical recycling** re-melts
  sorted plastic (PET, HDPE) but each cycle shortens chains and lowers
  quality (**downcycling**). **Chemical recycling** depolymerizes the
  polymer back to monomer for true circularity, at higher energy cost.

The **recycling codes** 1 to 7 identify resin; PET (1) and HDPE (2) are the
most widely recycled. A **life-cycle assessment (LCA)** is the honest way
to compare options, because a bioplastic can still lose if its farming and
composting footprint is high.

```mermaid
graph TD
    FEED["Feedstock choice"] --> FOSSIL["Fossil"]
    FEED --> BIO["Bio-based renewable"]
    USE["After use"] --> MECH["Mechanical recycle re-melt"]
    USE --> CHEM["Chemical recycle to monomer"]
    USE --> COMPOST["Industrial compost if biodegradable"]
    MECH --> DOWN["Quality drops downcycling"]
    CHEM --> CIRC["Closes the loop"]
```

A simple **mass-balance** on a recycling stream shows why yield and
contamination matter:

```text
Recycling mass balance
    Collected PET bottles      = 1000 kg
    Sorting loss (labels, caps, wrong resin) = 12 percent
    Washing/processing loss    = 8 percent of what remains

    after sorting  = 1000 * (1 - 0.12) = 880 kg
    after washing  = 880  * (1 - 0.08) = 810 kg
    recycled pellet yield = 810 / 1000 = 81 percent
```

The lost 19 percent, plus chain shortening on each melt cycle, is why
mechanical recycling alone cannot fully close the loop - and why chemical
recycling and better design-for-recycling matter.

Remember: bio-based, biodegradable, and recyclable are distinct; judge the
real benefit with a life-cycle assessment, not the label alone.
""",
        ),
        quiz_lesson(
            "Quiz: Sustainable and biodegradable polymers",
            (
                q(
                    "Bio-polyethylene is made from sugarcane. Is it biodegradable?",
                    (
                        opt("Yes, because it is bio-based it must biodegrade"),
                        opt(
                            "No - it is bio-based but chemically identical to fossil PE, "
                            "so it does not biodegrade; bio-based and biodegradable are "
                            "different",
                            correct=True,
                        ),
                        opt("Only in the ocean"),
                        opt("It is not a real polymer"),
                    ),
                    "Feedstock (bio-based) and end-of-life (biodegradable) are separate "
                    "properties; bio-PE degrades no faster than fossil PE.",
                ),
                q(
                    "Why does mechanical recycling of PET usually 'downcycle' the material?",
                    (
                        opt("It adds new monomer each time"),
                        opt(
                            "Each melt cycle shortens the chains and lowers molecular "
                            "weight and quality, so the recycled resin is worth less",
                            correct=True,
                        ),
                        opt("It increases molecular weight too much"),
                        opt("It never changes the polymer at all"),
                    ),
                    "Re-melting degrades chain length; chemical recycling back to monomer "
                    "avoids this but costs more energy.",
                ),
                q(
                    "In the recycling mass balance, 1000 kg of bottles lose 12 percent "
                    "in sorting then 8 percent in washing. What is the pellet yield?",
                    (
                        opt("80 percent"),
                        opt("81 percent", correct=True),
                        opt("88 percent"),
                        opt("100 percent"),
                    ),
                    "1000*0.88 = 880, then 880*0.92 = 810 kg, so yield = 810/1000 = 81 percent.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "A thermoset differs from a thermoplastic because it:",
                    (
                        opt("Can be re-melted and reshaped many times"),
                        opt(
                            "Forms a permanent crosslinked network that will not re-melt",
                            correct=True,
                        ),
                        opt("Contains no polymer chains"),
                        opt("Is always a liquid at room temperature"),
                    ),
                    "Thermosets are irreversibly crosslinked; thermoplastics soften and "
                    "reshape reversibly on heating.",
                ),
                q(
                    "Which mechanism reaches high molecular weight only near complete "
                    "conversion, following Xn = 1/(1-p)?",
                    (
                        opt("Free-radical chain growth"),
                        opt("Step-growth (condensation) polymerization", correct=True),
                        opt("Emulsion initiation"),
                        opt("Physical blending"),
                    ),
                    "Step growth: chains lengthen slowly and Xn climbs steeply only as p "
                    "approaches 1 (the Carothers relation).",
                ),
                q(
                    "The central engineering challenge in most polymerization reactors is:",
                    (
                        opt("Supplying heat to an endothermic reaction"),
                        opt(
                            "Removing exothermic reaction heat from an increasingly "
                            "viscous mass while keeping it mixed",
                            correct=True,
                        ),
                        opt("Preventing the monomer from ever reacting"),
                        opt("Keeping the reactor perfectly cold"),
                    ),
                    "Exothermic reaction plus rising viscosity make heat transfer and "
                    "mixing the limiting concerns, risking runaway.",
                ),
                q(
                    "For the same sample, which is always true of the averages?",
                    (
                        opt("Mn > Mw"),
                        opt("Mw >= Mn, and their ratio is the dispersity", correct=True),
                        opt("Mn = Mw for every real polymer"),
                        opt("Dispersity is always below 1"),
                    ),
                    "Mw is mass-weighted so Mw >= Mn; D = Mw/Mn >= 1 measures the width "
                    "of the distribution.",
                ),
                q(
                    "What does the glass transition temperature Tg mark?",
                    (
                        opt("The melting of crystalline regions"),
                        opt(
                            "The change of the amorphous regions between a rigid glass "
                            "and a soft rubbery state",
                            correct=True,
                        ),
                        opt("The temperature where the polymer forms"),
                        opt("The boiling point of the monomer"),
                    ),
                    "Tg is the onset of segmental motion in amorphous material; Tm "
                    "(semicrystalline only) is the melting of crystallites.",
                ),
                q(
                    "Why can a viscous polymer melt still fill a thin mould cavity?",
                    (
                        opt("Because its viscosity rises with shear rate"),
                        opt(
                            "Because it is shear-thinning - high shear rate lowers the "
                            "viscosity where the melt is forced through",
                            correct=True,
                        ),
                        opt("Because cooling makes it more fluid"),
                        opt("Because the mould heats it to boiling"),
                    ),
                    "Pseudoplastic (power-law n < 1) behaviour drops viscosity at high "
                    "shear rate, enabling mould filling.",
                ),
                q(
                    "In injection molding, cooling time scales roughly with wall "
                    "thickness squared. So thin, uniform walls:",
                    (
                        opt("Slow the cycle down"),
                        opt(
                            "Shorten cooling time sharply and reduce warpage from uneven shrinkage",
                            correct=True,
                        ),
                        opt("Have no effect on cycle time"),
                        opt("Always cause short shots"),
                    ),
                    "t_cool scales with L squared, so halving thickness cuts cooling "
                    "about fourfold; uneven thickness causes warpage.",
                ),
                q(
                    "For an aligned continuous-fibre composite, the rule of mixtures "
                    "E_c = Vf*E_f + (1-Vf)*E_m gives:",
                    (
                        opt("The transverse (across-fibre) modulus"),
                        opt(
                            "The longitudinal (along-fibre) modulus - highest when the "
                            "load runs along the fibres",
                            correct=True,
                        ),
                        opt("The melting temperature"),
                        opt("The dispersity"),
                    ),
                    "The Voigt iso-strain rule gives the stiff longitudinal modulus; the "
                    "transverse value is much lower, so composites are anisotropic.",
                ),
                q(
                    "Bio-based and biodegradable mean the same thing.",
                    (
                        opt("True - any renewable plastic breaks down"),
                        opt(
                            "False - bio-based describes the feedstock, biodegradable "
                            "describes end-of-life, and bio-PE is bio-based but not "
                            "biodegradable",
                            correct=True,
                        ),
                        opt("True - both refer to recycling codes"),
                        opt("False - both describe only fossil plastics"),
                    ),
                    "They are independent: bio-PE is bio-based yet non-biodegradable; PLA "
                    "is biodegradable (industrially) and bio-based.",
                ),
                q(
                    "Why is a life-cycle assessment (LCA) important when choosing a "
                    "greener plastic?",
                    (
                        opt("It measures only the colour of the plastic"),
                        opt(
                            "It compares the full footprint from feedstock to end-of-life, "
                            "so a bioplastic with high farming or composting impact does "
                            "not win by label alone",
                            correct=True,
                        ),
                        opt("It guarantees zero environmental impact"),
                        opt("It only counts the recycling code number"),
                    ),
                    "An LCA judges real benefit across the whole life cycle rather than "
                    "trusting a single 'bio' or 'recyclable' label.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

POLYMER_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_POLYMER_ENGINEERING,)
