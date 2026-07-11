"""Academy seed content - Material and Energy Balances.

The foundational accounting of chemical engineering: tracking mass and
energy through processes with and without reaction. It builds from the
general balance equation and process variables, through single-unit and
multi-unit balances (recycle, bypass, purge), reactive systems (limiting
reagent, conversion, yield), and the energy balance (enthalpy, heat
capacity, phase change), closing with a fully worked combined material
and energy balance. Every lesson is a direct explanation with a worked
balance and a mermaid diagram, followed by a checkpoint quiz; the course
closes with a comprehensive final quiz.
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


_MATERIAL_ENERGY_BALANCES = SeedCourse(
    slug="material-energy-balances",
    title="Material & Energy Balances",
    description=(
        "The foundational accounting of chemical engineering - tracking mass "
        "and energy through processes with and without reaction, including "
        "recycle, bypass and purge. Every lesson explains one idea directly, "
        "shows a worked balance, and draws the process as a diagram, closing "
        "with a fully worked combined material and energy balance."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Material and Energy Balances

Every chemical process - a reactor, a distillation column, an entire
plant - obeys two accounting laws: **mass is conserved** and **energy is
conserved**. Material and energy balances are how a chemical engineer
turns those laws into numbers: how much feed, how much product, how much
heat. Get the balances right and the rest of design follows; get them
wrong and nothing downstream is trustworthy.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short worked balance, and draws the process as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course. Process simulators (Aspen Plus, HYSYS,
DWSIM) automate these calculations, but they solve exactly the balances
you are about to learn by hand.

What you will build understanding for, in order:

1. **The conservation principle** - the general balance equation
2. **Process variables** - flow, composition, density
3. **Single-unit material balances** - no reaction
4. **Multiple units** - recycle, bypass and purge
5. **Reactive balances** - limiting reagent, conversion, yield
6. **Energy and the energy balance** - the first law for open systems
7. **Enthalpy** - heat capacity and phase changes
8. **Combined material and energy balances** - a worked process

This is the map. Each idea stacks on the previous one, so work through
them in order.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What two conservation laws underpin every material and energy balance?",
                    (
                        opt("Conservation of momentum and charge"),
                        opt(
                            "Conservation of mass and conservation of energy",
                            correct=True,
                        ),
                        opt("Conservation of pressure and temperature"),
                        opt("Conservation of volume and density"),
                    ),
                    "Mass is conserved and energy is conserved - balances turn those two "
                    "laws into numbers for a process.",
                ),
                q(
                    "How do process simulators like Aspen Plus relate to hand balances?",
                    (
                        opt("They replace the balances with guesses"),
                        opt(
                            "They automate the same mass and energy balances you learn to "
                            "do by hand",
                            correct=True,
                        ),
                        opt("They only compute costs, never balances"),
                        opt("They are unrelated to conservation laws"),
                    ),
                    "Simulators solve the identical conservation equations; understanding "
                    "the hand method is what lets you trust and debug them.",
                ),
            ),
        ),
        # -- 1. Conservation principle ---------------------------------
        _t(
            "The conservation principle and the general balance equation",
            "10 min",
            """# The conservation principle and the general balance equation

Everything in this course is one equation applied over and over. For any
**balanced quantity** (total mass, the mass of one species, energy) over
a chosen **system** and time period:

```text
Accumulation = Input - Output + Generation - Consumption
```

- **Input** and **Output** - what crosses the system boundary in feeds
  and product streams.
- **Generation** and **Consumption** - what a chemical reaction creates
  or destroys inside the boundary. **Total mass is never generated or
  consumed**, but an individual species can be. Energy has no chemical
  generation term, though reaction releases or absorbs it as heat.
- **Accumulation** - the change of the quantity held inside the system.

Two simplifications do most of the work:

- **Steady state** - nothing inside the system changes with time, so
  **Accumulation = 0**. Continuous plants run at steady state by design.
- **No reaction** - Generation = Consumption = 0. The balance collapses
  to the familiar **Input = Output**.

The first and most important step is always to **draw and label a
flowchart**, then **define the system boundary** (the dashed envelope you
balance across). A worked total mass balance on a steady-state mixer:

```text
System: mixer (steady state, no reaction) -> Accumulation = 0, Gen = Con = 0
Balance:  Input = Output
  Stream 1:  100 kg/h
  Stream 2:   50 kg/h
  Product m3: ?
  100 + 50 = m3   ->   m3 = 150 kg/h
```

```mermaid
graph LR
    S1["Feed 1 100 kg per h"] --> MIX["Mixer"]
    S2["Feed 2 50 kg per h"] --> MIX
    MIX --> P["Product 150 kg per h"]
```

Remember: pick the system, decide steady state and reaction, then write
`Input - Output + Generation - Consumption = Accumulation`. Every later
lesson is a special case of this.
""",
        ),
        quiz_lesson(
            "Quiz: The conservation principle and the general balance equation",
            (
                q(
                    "What is the general balance equation for any conserved quantity?",
                    (
                        opt("Input = Output, always"),
                        opt(
                            "Accumulation = Input - Output + Generation - Consumption",
                            correct=True,
                        ),
                        opt("Input + Output = Generation"),
                        opt("Accumulation = Input times Output"),
                    ),
                    "The full form has input, output, generation, consumption and "
                    "accumulation; the simpler forms are special cases.",
                ),
                q(
                    "At steady state with no chemical reaction, the balance reduces to what?",
                    (
                        opt("Accumulation = Generation"),
                        opt("Input = Output", correct=True),
                        opt("Output = Consumption"),
                        opt("Input = Accumulation"),
                    ),
                    "Steady state sets accumulation to zero; no reaction sets generation "
                    "and consumption to zero, leaving Input = Output.",
                ),
                q(
                    "Which quantity can never be generated or consumed by a reaction?",
                    (
                        opt("The mass of an individual species"),
                        opt("Total mass", correct=True),
                        opt("Moles of gas"),
                        opt("Energy"),
                    ),
                    "Total mass is always conserved; individual species and moles can "
                    "change, and reaction releases or absorbs energy.",
                ),
            ),
        ),
        # -- 2. Process variables --------------------------------------
        _t(
            "Process variables: flow, composition, density",
            "10 min",
            """# Process variables: flow, composition, density

Balances are written in terms of a handful of **process variables**. You
must be fluent in what each means and how they convert.

**Flow rate** - how much of a stream passes per unit time. Two flavours:

- **Mass flow** (kg/h) and **molar flow** (kmol/h). Convert with molar
  mass: `n = m / M`.
- **Volumetric flow** (m3/h) links to mass flow through **density**:
  `mass flow = density x volumetric flow`.

**Composition** - the makeup of a mixture. Two bases that must never be
confused:

- **Mass fraction** `w_i = mass of i / total mass`.
- **Mole fraction** `x_i = moles of i / total moles`.
- Each set sums to 1: `sum(w_i) = 1` and `sum(x_i) = 1`. That
  "fractions sum to one" is itself an equation you use to close balances.

**Density** `rho = mass / volume` ties the mass world to the volume
world. For gases, the ideal gas law `PV = nRT` plays the density role.

Convert a stream from mass to mole basis (basis: 100 kg):

```text
Stream: 60 percent methanol (M=32), 40 percent water (M=18) by mass
Basis: 100 kg
  methanol: 60 kg / 32 = 1.875 kmol
  water:    40 kg / 18 = 2.222 kmol
  total moles = 4.097 kmol
  x_methanol = 1.875 / 4.097 = 0.458
  x_water    = 2.222 / 4.097 = 0.542   (check: 0.458 + 0.542 = 1.000)
```

Notice mass fraction 0.60 became mole fraction 0.458 - the two bases are
not interchangeable.

```mermaid
graph LR
    V["Volumetric flow"] -->|"times density"| M["Mass flow"]
    M -->|"divide by molar mass"| N["Molar flow"]
    M --> W["Mass fractions sum to one"]
    N --> X["Mole fractions sum to one"]
```

Remember: state your **basis**, keep mass and mole bases separate, and
use `sum of fractions = 1` as a genuine equation.
""",
        ),
        quiz_lesson(
            "Quiz: Process variables: flow, composition, density",
            (
                q(
                    "How do you convert a mass flow to a molar flow?",
                    (
                        opt("Multiply by density"),
                        opt("Divide the mass flow by the molar mass", correct=True),
                        opt("Multiply by the mole fraction"),
                        opt("Divide by the volumetric flow"),
                    ),
                    "n = m / M: mass flow divided by molar mass gives molar flow.",
                ),
                q(
                    "Why can a 60 percent-by-mass stream have a different value as a mole fraction?",
                    (
                        opt("Because mass is not conserved"),
                        opt(
                            "Because species have different molar masses, so mass and "
                            "mole bases are not interchangeable",
                            correct=True,
                        ),
                        opt("Because density changes with temperature only"),
                        opt("Because fractions do not have to sum to one"),
                    ),
                    "Dividing each mass by its own molar mass reweights the composition, "
                    "so mass and mole fractions differ.",
                ),
                q(
                    "What useful equation do the fractions of a stream always satisfy?",
                    (
                        opt("They sum to the density"),
                        opt("They sum to 1", correct=True),
                        opt("They sum to the molar mass"),
                        opt("They sum to the flow rate"),
                    ),
                    "Mass fractions sum to 1 and mole fractions sum to 1 - a real "
                    "equation used to close balances.",
                ),
            ),
        ),
        # -- 3. Single unit, no reaction -------------------------------
        _t(
            "Material balances on a single unit (no reaction)",
            "11 min",
            """# Material balances on a single unit (no reaction)

With no reaction, a steady-state unit obeys **Input = Output** for total
mass **and for every species independently**. That gives you a set of
simultaneous equations you solve for the unknowns.

The method, every time:

1. **Draw and label** the flowchart - every stream with its flow and
   composition, unknowns as symbols.
2. **Choose a basis** - a convenient amount (100 kg of feed, 100 kmol/h)
   to anchor the arithmetic.
3. **Count** - unknowns versus independent balance equations. A unit
   with `S` species gives `S` independent balances (total mass is the sum
   of the species balances, so it is not extra).
4. **Solve** the equations.

Worked example - a **separator** splits a feed into two product streams:

```text
Feed F: 1000 kg/h, 50 percent benzene (B) / 50 percent toluene (T)
Top D:  overhead, 95 percent B / 5 percent T
Bottom W: bottoms,10 percent B / 90 percent T
Find D and W.

Total mass:  F = D + W          ->  1000 = D + W
Benzene:     0.50 F = 0.95 D + 0.10 W
             500 = 0.95 D + 0.10 W
Substitute W = 1000 - D:
  500 = 0.95 D + 0.10 (1000 - D)
  500 = 0.95 D + 100 - 0.10 D
  400 = 0.85 D    ->  D = 470.6 kg/h
  W = 1000 - 470.6 = 529.4 kg/h
Check toluene: 0.05(470.6) + 0.90(529.4) = 23.5 + 476.5 = 500 = 0.50 F  OK
```

The independent check (toluene) closing to the feed confirms the answer.

```mermaid
graph LR
    F["Feed 1000 kg per h"] --> SEP["Separator"]
    SEP --> D["Top 95 percent benzene"]
    SEP --> W["Bottom 90 percent toluene"]
```

Remember: label, pick a basis, write one balance per species, and verify
with the balance you did not use to solve.
""",
        ),
        quiz_lesson(
            "Quiz: Material balances on a single unit (no reaction)",
            (
                q(
                    "For a steady-state unit with no reaction, the balance Input = Output holds for what?",
                    (
                        opt("Total mass only"),
                        opt(
                            "Total mass and each chemical species independently",
                            correct=True,
                        ),
                        opt("Energy only"),
                        opt("Volume only"),
                    ),
                    "Every species is separately conserved, giving one balance equation "
                    "per species.",
                ),
                q(
                    "Why choose a basis of calculation before solving?",
                    (
                        opt("It changes the physics of the process"),
                        opt(
                            "It anchors the arithmetic to a convenient amount so the "
                            "numbers are easy to work with",
                            correct=True,
                        ),
                        opt("It is required to conserve energy"),
                        opt("It removes the need for species balances"),
                    ),
                    "A basis (say 1000 kg/h of feed) fixes the scale; results scale "
                    "linearly to the real flow.",
                ),
                q(
                    "For a unit handling a mixture of S species, how many independent "
                    "material balances can you write?",
                    (
                        opt("S plus 1, counting the total"),
                        opt(
                            "S - the total mass balance is the sum of the species "
                            "balances, not an extra one",
                            correct=True,
                        ),
                        opt("Always exactly 2"),
                        opt("As many as there are streams"),
                    ),
                    "The total balance is the sum of the species balances, so only S of "
                    "them are independent.",
                ),
            ),
        ),
        # -- 4. Recycle, bypass, purge ---------------------------------
        _t(
            "Multiple units: recycle, bypass and purge",
            "12 min",
            """# Multiple units: recycle, bypass and purge

Real plants are networks of units, and three stream patterns appear
everywhere. The trick is choosing the **right system boundary** - you can
balance the overall process, a single unit, or a mixing/splitting point,
and picking well makes the algebra simple.

- **Recycle** - a stream is sent back to be reprocessed. It raises overall
  conversion and recovers unreacted feed or catalyst. A **fresh feed**
  mixes with the recycle to form the **combined feed** to the unit.
- **Bypass** - part of the feed skips a unit and rejoins downstream, used
  to blend to a target (for example, trimming how much of a stream gets
  treated).
- **Purge** - a small stream continuously removed from a recycle loop to
  stop an **inert or impurity** from accumulating. Without a purge, an
  unreactive component entering with fresh feed has nowhere to leave and
  builds up without bound.

Key idea: choose boundaries so each balance has as few unknowns as
possible. The **overall balance** (around the whole plant, cutting only
fresh feed and net products) ignores the recycle entirely - recycle
streams are internal to it.

Worked recycle with purge - inert argon enters and must leave via purge:

```text
Fresh feed enters with 2 kg/h argon (inert). At steady state argon does
not react and does not leave in product, so ALL of it must leave in the
purge.
  Overall argon balance:  argon in fresh feed = argon in purge
  2 kg/h in  =  argon out in purge  ->  purge carries 2 kg/h argon
If the recycle loop argon mole fraction is 0.04, the purge (same
composition as the loop it is bled from) is:
  purge total = 2 / 0.04 = 50 kg/h
```

The purge rate is set by the inert balance - remove exactly what comes in.

```mermaid
graph LR
    FF["Fresh feed"] --> MIX["Mixer"]
    MIX --> RX["Reactor"]
    RX --> SEP["Separator"]
    SEP --> PROD["Product"]
    SEP --> SPLIT["Splitter"]
    SPLIT --> PURGE["Purge removes inert"]
    SPLIT --> REC["Recycle"]
    REC --> MIX
```

Remember: recycle improves conversion, bypass blends to spec, and purge
prevents inert build-up - and the overall balance is your friend because
it hides the internal recycle.
""",
        ),
        quiz_lesson(
            "Quiz: Multiple units: recycle, bypass and purge",
            (
                q(
                    "What is the purpose of a purge stream in a recycle loop?",
                    (
                        opt("To speed up the reaction"),
                        opt(
                            "To continuously remove an inert or impurity so it does not "
                            "accumulate in the loop",
                            correct=True,
                        ),
                        opt("To heat the recycle stream"),
                        opt("To increase the fresh feed rate"),
                    ),
                    "Without a purge, an inert entering with fresh feed has no other "
                    "exit and builds up without bound.",
                ),
                q(
                    "Why is the overall balance around the whole plant convenient with recycle?",
                    (
                        opt("It doubles the number of unknowns"),
                        opt(
                            "The recycle is internal to it, so it only involves fresh "
                            "feed and net product streams",
                            correct=True,
                        ),
                        opt("It ignores conservation of mass"),
                        opt("It only works when there is a reaction"),
                    ),
                    "Cutting only the fresh feed and net products, the recycle never "
                    "crosses the boundary, so it drops out.",
                ),
                q(
                    "What does a bypass stream do?",
                    (
                        opt("Sends product back to be reprocessed"),
                        opt("Removes inert from a loop"),
                        opt(
                            "Routes part of the feed around a unit to rejoin downstream, "
                            "often to blend to a target",
                            correct=True,
                        ),
                        opt("Adds heat to the reactor"),
                    ),
                    "Bypass skips the unit and recombines downstream - handy for trimming "
                    "to a spec. Recycle (reprocessing) and purge (inert removal) are "
                    "different patterns.",
                ),
            ),
        ),
        # -- 5. Balances with reaction ---------------------------------
        _t(
            "Material balances with chemical reaction (limiting reagent, conversion, yield)",
            "12 min",
            """# Material balances with chemical reaction

When a reaction runs, **total mass is still conserved**, but individual
species are generated and consumed, so `Input = Output` fails for each
species. You track the reaction with a few standard quantities.

- **Limiting reagent** - the reactant that would run out first given the
  feed ratio versus the **stoichiometric** ratio. Everything else is in
  **excess**. Percent excess is measured against what the limiting reagent
  needs.
- **Conversion** `X = (reactant consumed) / (reactant fed)`. It says how
  far the reaction proceeds toward completion.
- **Yield** and **selectivity** matter when side reactions exist:
  yield compares product actually made to the maximum possible; selectivity
  compares the desired product to an undesired one.

A clean bookkeeping tool is the **extent of reaction** `xi`: for a species
`i` with stoichiometric coefficient `nu_i` (negative for reactants,
positive for products), `n_i,out = n_i,in + nu_i * xi`. One `xi` closes
every species.

Worked example - ammonia synthesis `N2 + 3 H2 -> 2 NH3`:

```text
Feed: 100 kmol N2, 300 kmol H2 (stoichiometric ratio 1:3, so neither is
in excess). Nitrogen conversion X = 0.20.
  N2 consumed = 0.20 x 100 = 20 kmol  ->  extent xi = 20 kmol
  N2 out = 100 - 1(20) = 80 kmol
  H2 out = 300 - 3(20) = 240 kmol
  NH3 out = 0 + 2(20) = 40 kmol
  Total out = 80 + 240 + 40 = 360 kmol   (moles fell: gas count drops)
Mass check (M: N2=28, H2=2, NH3=17):
  in  = 100(28) + 300(2) = 2800 + 600 = 3400 kg
  out = 80(28) + 240(2) + 40(17) = 2240 + 480 + 680 = 3400 kg   OK
```

Note **moles are not conserved** (400 kmol in, 360 out) but **mass is** -
the classic reactive-balance signature.

```mermaid
graph LR
    N["Nitrogen feed"] --> RX["Reactor N2 plus 3 H2"]
    H["Hydrogen feed"] --> RX
    RX --> A["Ammonia product"]
    RX --> U["Unreacted N2 and H2"]
```

Remember: identify the limiting reagent, use conversion or extent to get
generation and consumption, and always confirm **mass** (not moles)
balances.
""",
        ),
        quiz_lesson(
            "Quiz: Material balances with chemical reaction (limiting reagent, conversion, yield)",
            (
                q(
                    "In a reactive process, which quantity is still conserved and which may not be?",
                    (
                        opt("Moles are conserved; mass may not be"),
                        opt(
                            "Mass is conserved; moles may not be",
                            correct=True,
                        ),
                        opt("Both mass and moles are always conserved"),
                        opt("Neither mass nor moles is conserved"),
                    ),
                    "Reactions change the number of moles but never the total mass - the "
                    "mass check is the reliable one.",
                ),
                q(
                    "What is the limiting reagent?",
                    (
                        opt("The reactant present in the largest amount"),
                        opt(
                            "The reactant that would be used up first relative to the "
                            "stoichiometric ratio",
                            correct=True,
                        ),
                        opt("The product formed in the smallest amount"),
                        opt("Any inert in the feed"),
                    ),
                    "It runs out first given the feed ratio versus stoichiometry; the "
                    "others are in excess.",
                ),
                q(
                    "How is fractional conversion of a reactant defined?",
                    (
                        opt("Product made divided by feed mass"),
                        opt(
                            "Reactant consumed divided by reactant fed",
                            correct=True,
                        ),
                        opt("Moles out divided by moles in"),
                        opt("Desired product divided by undesired product"),
                    ),
                    "X = consumed / fed measures how far the reaction proceeds; the last "
                    "option describes selectivity.",
                ),
            ),
        ),
        # -- 6. Energy balance -----------------------------------------
        _t(
            "Energy and the energy balance",
            "11 min",
            """# Energy and the energy balance

Mass is only half the accounting. The **first law of thermodynamics** for
an **open system** (streams flowing in and out) balances energy the same
way mass was balanced. At **steady state** the general open-system energy
balance is:

```text
Q - Ws = dH + dEk + dEp

Q   = heat added to the system      (positive = heat in)
Ws  = shaft work done BY the system (positive = work out)
dH  = change in enthalpy of the streams (out minus in)
dEk = change in kinetic energy
dEp = change in potential energy
```

For most chemical process units the kinetic and potential terms are
negligible next to the thermal terms, and there is no shaft work, so it
simplifies to the workhorse form:

```text
Q = dH = H_out - H_in
```

Heat in equals the enthalpy the streams gained. This is why **enthalpy**
(the next lesson) is the central property - it carries the thermal energy
of flowing streams.

Sign convention matters: `Q > 0` means heat flows **into** the system
(**endothermic** duty, a heater); `Q < 0` means heat flows **out** (an
**exothermic** duty, a cooler). Getting the sign wrong flips a heater into
a cooler.

Worked sensible-heat duty - heat a water stream:

```text
Heat 500 kg/h of liquid water from 25 C to 80 C.
  cp of liquid water = 4.18 kJ/(kg C)
  Q = m x cp x (T_out - T_in)
    = 500 x 4.18 x (80 - 25)
    = 500 x 4.18 x 55
    = 114,950 kJ/h  (about 31.9 kW)
Q is positive: heat is added, as expected for a heater.
```

```mermaid
graph LR
    IN["Feed stream H in"] --> UNIT["Process unit"]
    Q["Heat Q added"] --> UNIT
    UNIT --> OUT["Product stream H out"]
    UNIT --> WS["Shaft work Ws"]
```

Remember: at steady state, with kinetic, potential and work terms
dropped, `Q = H_out - H_in`. Keep the sign convention straight - positive
Q is heat in.
""",
        ),
        quiz_lesson(
            "Quiz: Energy and the energy balance",
            (
                q(
                    "For a steady-state process unit with negligible kinetic, potential "
                    "and shaft-work terms, the energy balance reduces to what?",
                    (
                        opt("Q = 0 always"),
                        opt("Q = H_out - H_in", correct=True),
                        opt("Q = mass in - mass out"),
                        opt("Q = Ws"),
                    ),
                    "The heat added equals the change in stream enthalpy from inlet to outlet.",
                ),
                q(
                    "Under the usual convention, what does a positive Q mean?",
                    (
                        opt("Heat flows out of the system"),
                        opt("Heat flows into the system", correct=True),
                        opt("Work is done by the system"),
                        opt("The reaction is exothermic"),
                    ),
                    "Positive Q is heat added - a heating duty; a cooler has Q negative.",
                ),
                q(
                    "In the sensible-heat example, why was Q computed as m x cp x delta T?",
                    (
                        opt("Because the stream changed phase"),
                        opt(
                            "Because a single-phase stream is being warmed, so its "
                            "enthalpy change is heat capacity times temperature change",
                            correct=True,
                        ),
                        opt("Because a reaction was occurring"),
                        opt("Because shaft work dominated"),
                    ),
                    "Sensible heat for a single phase is m x cp x delta T; no phase "
                    "change or reaction is involved.",
                ),
            ),
        ),
        # -- 7. Enthalpy, cp, phase changes ----------------------------
        _t(
            "Enthalpy, heat capacity and phase changes",
            "11 min",
            """# Enthalpy, heat capacity and phase changes

Enthalpy `H` is only meaningful as a **change** relative to a chosen
**reference state**, because there is no absolute zero of enthalpy. You
pick a reference (temperature, phase) and compute every stream's enthalpy
relative to it. Two kinds of enthalpy change appear:

- **Sensible heat** - warming or cooling within a single phase. The
  **heat capacity** `cp` (kJ/(mol C) or kJ/(kg C)) gives
  `dH = integral of cp dT`, or simply `dH = cp * (T2 - T1)` when `cp` is
  roughly constant.
- **Latent heat** - a **phase change** at constant temperature. Melting
  absorbs the **heat of fusion**; boiling absorbs the **heat of
  vaporization** `dHvap`. Crucially, **temperature does not change during
  a phase change** - all the heat goes into the transition.

To move a stream between two states you add the pieces along a path:
sensible heat to the transition temperature, then latent heat for the
phase change, then sensible heat onward. Because enthalpy is a **state
function**, the path you choose does not matter - only the endpoints do.

Worked example - fully vaporize and superheat water (path method):

```text
Take 1 kg water from liquid at 25 C to steam at 120 C, at 1 atm.
  Step 1  liquid 25 C -> liquid 100 C:
     m x cp,liq x dT = 1 x 4.18 x (100 - 25) = 313.5 kJ
  Step 2  boil at 100 C (latent, T constant):
     m x dHvap = 1 x 2257 = 2257 kJ
  Step 3  vapor 100 C -> vapor 120 C:
     m x cp,vap x dT = 1 x 1.90 x (120 - 100) = 38 kJ
  Total dH = 313.5 + 2257 + 38 = 2608.5 kJ
```

The latent step dwarfs the sensible steps - phase change carries most of
the energy, which is why boilers and condensers dominate plant heat duty.

```mermaid
graph LR
    L1["Liquid 25 C"] -->|"sensible heat"| L2["Liquid 100 C"]
    L2 -->|"latent heat of vaporization"| V1["Vapor 100 C"]
    V1 -->|"sensible heat"| V2["Vapor 120 C"]
```

Remember: choose a reference state, add sensible plus latent heat along a
convenient path (enthalpy is a state function), and remember temperature
stays constant through a phase change.
""",
        ),
        quiz_lesson(
            "Quiz: Enthalpy, heat capacity and phase changes",
            (
                q(
                    "Why is enthalpy always reported as a change relative to a reference state?",
                    (
                        opt("Because enthalpy is negative"),
                        opt(
                            "Because there is no absolute zero of enthalpy, so only "
                            "differences are meaningful",
                            correct=True,
                        ),
                        opt("Because heat capacity is unknown"),
                        opt("Because mass is conserved"),
                    ),
                    "You pick a reference state and compute every stream relative to it; "
                    "only enthalpy differences have physical meaning.",
                ),
                q(
                    "What happens to temperature while a pure substance changes phase at "
                    "constant pressure?",
                    (
                        opt("It rises steadily"),
                        opt(
                            "It stays constant - all the heat goes into the phase "
                            "transition (latent heat)",
                            correct=True,
                        ),
                        opt("It falls to the reference temperature"),
                        opt("It oscillates"),
                    ),
                    "During a phase change the added heat is latent heat and temperature "
                    "is unchanged until the transition completes.",
                ),
                q(
                    "Because enthalpy is a state function, what is true of the path used "
                    "to compute a change between two states?",
                    (
                        opt("Only the shortest path gives the right answer"),
                        opt(
                            "Any convenient path gives the same result - only the endpoints matter",
                            correct=True,
                        ),
                        opt("The path must avoid any phase change"),
                        opt("The path changes the total enthalpy difference"),
                    ),
                    "A state function depends only on the endpoints, so you build a "
                    "convenient path of sensible and latent steps.",
                ),
            ),
        ),
        # -- 8. Combined balance ---------------------------------------
        _t(
            "Combined material and energy balances (a worked process)",
            "12 min",
            """# Combined material and energy balances (a worked process)

Real design needs **both** balances at once: solve the material balance
first to get all stream flows and compositions, then use those flows in
the energy balance to size the heat duty. Mass gives you the amounts;
energy gives you the heating or cooling to buy.

The combined procedure:

1. **Flowchart and basis** - label every stream.
2. **Material balance** - solve for all unknown flows and compositions.
3. **Reference state** - choose it for the energy balance.
4. **Enthalpy of each stream** - sensible plus latent, relative to the
   reference, using the flows from step 2.
5. **Energy balance** - `Q = H_out - H_in` (plus reaction heat if a
   reaction runs) to get the duty.

Worked example - an **evaporator** concentrating a salt solution:

```text
MATERIAL BALANCE (steady state, no reaction)
Feed F: 1000 kg/h, 10 percent salt, enters at 25 C.
Product L: concentrated to 30 percent salt.
Vapor V: pure water boiled off.
  Salt balance:  0.10 x 1000 = 0.30 x L  ->  L = 333.3 kg/h
  Total balance: 1000 = L + V  ->  V = 1000 - 333.3 = 666.7 kg/h

ENERGY BALANCE (reference: liquid water and feed at 25 C; boiling 100 C)
Approx with cp,soln = 4.0 kJ/(kg C), dHvap = 2257 kJ/kg:
  1) heat feed 25 -> 100 C:  1000 x 4.0 x (100 - 25) = 300,000 kJ/h
  2) vaporize 666.7 kg/h water: 666.7 x 2257 = 1,504,700 kJ/h
  Q = 300,000 + 1,504,700 = 1,804,700 kJ/h  (about 501 kW of steam duty)
```

Material balance sized the streams (333 kg/h product, 667 kg/h vapor);
the energy balance then sized the reboiler duty (about 501 kW) - exactly
what you would specify a heat exchanger and steam supply against.

```mermaid
graph LR
    F["Feed 1000 kg per h 10 percent salt"] --> EV["Evaporator"]
    STEAM["Steam duty Q"] --> EV
    EV --> V["Vapor 667 kg per h water"]
    EV --> L["Product 333 kg per h 30 percent salt"]
```

Remember: material balance first for the flows, energy balance second for
the duty. Together they turn a process sketch into equipment you can
specify - the foundation everything else in chemical engineering builds
on.
""",
        ),
        quiz_lesson(
            "Quiz: Combined material and energy balances (a worked process)",
            (
                q(
                    "In a combined analysis, which balance do you normally solve first, and why?",
                    (
                        opt("The energy balance, because heat drives everything"),
                        opt(
                            "The material balance first, because its stream flows are "
                            "needed to compute the enthalpies in the energy balance",
                            correct=True,
                        ),
                        opt("They must be solved simultaneously, never in order"),
                        opt("The energy balance, because mass is irrelevant"),
                    ),
                    "You need the flows from the material balance before you can size the "
                    "enthalpy terms and heat duty.",
                ),
                q(
                    "In the evaporator, how was the vapor rate of 666.7 kg/h obtained?",
                    (
                        opt("From the heat duty"),
                        opt(
                            "From the material balances: a salt balance fixed the "
                            "product, then the total balance gave the vapor",
                            correct=True,
                        ),
                        opt("From the heat of vaporization alone"),
                        opt("By assuming half the feed evaporates"),
                    ),
                    "Salt balance gives L = 333.3 kg/h; total balance V = 1000 - L = "
                    "666.7 kg/h - pure material balance.",
                ),
                q(
                    "Why did vaporizing the water dominate the evaporator heat duty?",
                    (
                        opt("Because sensible heating is always larger"),
                        opt(
                            "Because latent heat of vaporization is large, so boiling off "
                            "667 kg/h of water needs far more energy than warming the feed",
                            correct=True,
                        ),
                        opt("Because the salt absorbs most of the heat"),
                        opt("Because the feed entered above its boiling point"),
                    ),
                    "Latent heat dwarfs sensible heat; the vaporization term (about "
                    "1.5 million kJ/h) far exceeds the sensible term (300,000 kJ/h).",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the general balance equation for a conserved quantity?",
                    (
                        opt("Input = Output in all cases"),
                        opt(
                            "Accumulation = Input - Output + Generation - Consumption",
                            correct=True,
                        ),
                        opt("Generation = Input + Output"),
                        opt("Accumulation = Input x Output"),
                    ),
                    "All balances are special cases of this; steady state drops "
                    "accumulation, no reaction drops generation and consumption.",
                ),
                q(
                    "A continuous unit at steady state with no reaction obeys which relation?",
                    (
                        opt("Accumulation = Generation"),
                        opt("Input = Output, for total mass and each species", correct=True),
                        opt("Output = Consumption"),
                        opt("Input = Accumulation"),
                    ),
                    "With accumulation and reaction terms zero, input equals output for "
                    "total mass and every species.",
                ),
                q(
                    "Converting a stream from mass basis to mole basis requires what?",
                    (
                        opt("Multiplying each component mass by its density"),
                        opt(
                            "Dividing each component mass by its molar mass, then "
                            "renormalizing to get mole fractions",
                            correct=True,
                        ),
                        opt("Nothing - mass and mole fractions are equal"),
                        opt("Multiplying by the volumetric flow"),
                    ),
                    "n_i = m_i / M_i, then x_i = n_i / total moles; mass and mole "
                    "fractions generally differ.",
                ),
                q(
                    "What is the role of a purge stream in a recycle loop?",
                    (
                        opt("To increase reaction temperature"),
                        opt(
                            "To bleed off an inert or impurity so it does not accumulate "
                            "in the loop",
                            correct=True,
                        ),
                        opt("To recover product from the vapor"),
                        opt("To bypass the reactor"),
                    ),
                    "At steady state the purge must remove exactly the inert that enters "
                    "with the fresh feed.",
                ),
                q(
                    "In a reactive process, which check reliably confirms the balance?",
                    (
                        opt("Total moles in equals total moles out"),
                        opt("Total mass in equals total mass out", correct=True),
                        opt("Volume in equals volume out"),
                        opt("Number of streams in equals streams out"),
                    ),
                    "Reactions change moles but never total mass, so the mass check is "
                    "the trustworthy one.",
                ),
                q(
                    "Fractional conversion of a reactant is defined as…",
                    (
                        opt("moles out divided by moles in"),
                        opt("reactant consumed divided by reactant fed", correct=True),
                        opt("desired product divided by side product"),
                        opt("product mass divided by feed volume"),
                    ),
                    "X = consumed / fed; the desired-versus-side-product ratio is selectivity.",
                ),
                q(
                    "For a steady-state unit with negligible kinetic, potential and shaft "
                    "work, the energy balance is…",
                    (
                        opt("Q = 0"),
                        opt("Q = H_out - H_in", correct=True),
                        opt("Q = mass out - mass in"),
                        opt("Q = Ws"),
                    ),
                    "Heat added equals the enthalpy change of the streams from inlet to outlet.",
                ),
                q(
                    "During a pure-component phase change at constant pressure, the temperature…",
                    (
                        opt("rises linearly with heat added"),
                        opt(
                            "stays constant while latent heat drives the transition",
                            correct=True,
                        ),
                        opt("drops to the reference temperature"),
                        opt("depends on the heat capacity"),
                    ),
                    "All added heat goes into the phase change, so temperature holds "
                    "until the transition is complete.",
                ),
                q(
                    "Why can you compute an enthalpy change along any convenient path of "
                    "sensible and latent steps?",
                    (
                        opt("Because mass is conserved"),
                        opt(
                            "Because enthalpy is a state function - the change depends "
                            "only on the endpoints",
                            correct=True,
                        ),
                        opt("Because heat capacity is always constant"),
                        opt("Because the reference state is arbitrary"),
                    ),
                    "State functions depend only on start and end states, so you build "
                    "the easiest path between them.",
                ),
                q(
                    "In a combined material and energy analysis, the correct order is…",
                    (
                        opt("energy balance first, then material balance"),
                        opt(
                            "material balance first for the flows, then energy balance "
                            "for the heat duty",
                            correct=True,
                        ),
                        opt("only the energy balance is needed"),
                        opt("only the material balance is needed"),
                    ),
                    "Solve the material balance to get stream flows, then use them in the "
                    "energy balance to size the duty.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

MATERIAL_ENERGY_BALANCES_COURSES: tuple[SeedCourse, ...] = (_MATERIAL_ENERGY_BALANCES,)
