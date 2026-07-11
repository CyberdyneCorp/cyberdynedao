"""Academy seed content - Chemical Reaction Engineering.

Designing the heart of a chemical plant: how fast reactions go (rate laws
and the Arrhenius temperature dependence), the three ideal reactors that
every real reactor is measured against (batch, CSTR, PFR), and the design
equations that size them. It then moves to the hard, practical parts -
multiple reactions and selectivity, the coupled energy balance of
non-isothermal operation, and catalysis with its transport limitations.
Every lesson is a direct explanation with a worked design calculation and
a mermaid diagram, followed by a checkpoint quiz; the course closes with a
comprehensive final quiz.
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


_CHEMICAL_REACTION_ENGINEERING = SeedCourse(
    slug="chemical-reaction-engineering",
    title="Chemical Reaction Engineering",
    description=(
        "Designing the heart of a chemical plant - rate laws, the ideal "
        "reactors (batch, CSTR, PFR), multiple reactions and selectivity, "
        "non-isothermal operation and catalysis. Every lesson pairs a direct "
        "explanation with a worked design equation or Python calculation and a "
        "diagram, grounded in real practice (Arrhenius, Aspen/HYSYS/DWSIM, "
        "Thiele modulus)."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Chemical Reaction Engineering

The reactor is where raw materials become products - it is the one unit
that defines what the rest of the plant must do. Get the reactor right and
separations, recycles, and utilities follow; get it wrong and no amount of
downstream cleverness recovers the loss. **Chemical reaction engineering**
is the discipline of turning reaction kinetics into a sized, operable
reactor.

The approach here is **small and concrete**: every lesson explains one
idea directly, shows it in a worked design calculation (a rate law, a mole
balance, a sizing equation, or a short Python snippet), and draws the idea
as a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Reaction rate and rate laws** - how fast, and what it depends on
2. **Batch reactor design** - the fundamental time-based mole balance
3. **CSTR design** - the well-mixed continuous tank
4. **Plug-flow reactor design** - the ideal tube
5. **Comparing and combining reactors** - which is smaller, and in series
6. **Multiple reactions, selectivity and yield** - making the *right* product
7. **Non-isothermal reactors** - coupling the mole and energy balances
8. **Catalysis and heterogeneous reactions** - surfaces and transport

This is the map. Modern practice does the arithmetic in a flowsheet
simulator (Aspen Plus, HYSYS, DWSIM), but the simulator only echoes the
design equations in this course - you must understand them to trust it.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Why is the reactor considered the heart of a chemical plant?",
                    (
                        opt("Because it is always the most expensive single vessel"),
                        opt(
                            "It is where raw materials become products, so its "
                            "conversion and selectivity define what every downstream "
                            "separation and recycle must handle",
                            correct=True,
                        ),
                        opt("Because it never needs a catalyst"),
                        opt("Because it operates at ambient temperature"),
                    ),
                    "The reactor sets the feed to the rest of the plant; its "
                    "performance dictates separations, recycles and utilities.",
                ),
                q(
                    "What is the role of a flowsheet simulator like Aspen Plus in this course?",
                    (
                        opt("It replaces the need to understand the design equations"),
                        opt(
                            "It does the arithmetic quickly, but only echoes the same "
                            "mole and energy balances you must understand to trust the result",
                            correct=True,
                        ),
                        opt("It invents new reactions automatically"),
                        opt("It is used only for billing"),
                    ),
                    "Simulators execute the design equations fast; the engineer still "
                    "owns the kinetics and the judgement.",
                ),
            ),
        ),
        # -- 1. Rate laws ----------------------------------------------
        _t(
            "Reaction rate and rate laws",
            "11 min",
            """# Reaction rate and rate laws

The **rate of reaction** is how fast moles of a species are consumed or
formed per unit volume per unit time. For a species A it is written
`-r_A` (the minus sign because A is consumed). It is an **intensive**
quantity: it describes the chemistry at a point, independent of reactor
size or type. Sizing any reactor starts with knowing `-r_A`.

For a reaction `A + B -> products`, the **rate law** usually takes a
power-law form:

```text
-r_A = k * C_A^a * C_B^b

  -r_A : rate of consumption of A   [mol / (L . s)]
  k    : rate constant (temperature dependent)
  C_A  : concentration of A         [mol / L]
  a, b : reaction orders (found by experiment, NOT the stoichiometry)
  overall order n = a + b
```

The **orders are empirical** - you measure them; you do not read them off
the balanced equation. A reaction can be first order in A, zero order in
B, or have fractional or negative orders.

The rate constant `k` carries the temperature dependence through the
**Arrhenius equation**:

```text
k = A * exp(-E_a / (R * T))

  A    : pre-exponential (frequency) factor
  E_a  : activation energy   [J / mol]
  R    : 8.314 J / (mol . K)
  T    : absolute temperature [K]
```

A useful rule of thumb near room temperature: a 10 K rise roughly doubles
`k` for a typical activation energy. Plotting `ln(k)` against `1/T` gives a
straight line of slope `-E_a / R` - the standard way to extract `E_a` from
data:

```python
import numpy as np

R = 8.314  # J/(mol K)
T = np.array([300.0, 320.0, 340.0, 360.0])       # K
k = np.array([0.011, 0.028, 0.065, 0.14])        # 1/s

slope, intercept = np.polyfit(1.0 / T, np.log(k), 1)
E_a = -slope * R          # J/mol
A = np.exp(intercept)     # 1/s
print(f"E_a = {E_a/1000:.1f} kJ/mol,  A = {A:.3e} 1/s")
```

```mermaid
graph LR
    T["Temperature"] --> K["Rate constant k via Arrhenius"]
    C["Concentrations"] --> RATE["Rate minus r A"]
    K --> RATE
    ORDER["Reaction orders from experiment"] --> RATE
    RATE --> DESIGN["Feeds every reactor design equation"]
```

Remember: the rate law `-r_A = k(T) . f(C)` is the input to all reactor
design. Concentration sets the composition dependence; Arrhenius sets the
temperature dependence; both are found from experiment.
""",
        ),
        quiz_lesson(
            "Quiz: Reaction rate and rate laws",
            (
                q(
                    "How are the reaction orders a and b in a power-law rate law determined?",
                    (
                        opt("Read directly from the balanced stoichiometric equation"),
                        opt(
                            "Measured experimentally - they are empirical and need not "
                            "match the stoichiometric coefficients",
                            correct=True,
                        ),
                        opt("Always equal to 1 for every reaction"),
                        opt("Calculated from the molecular weight"),
                    ),
                    "Orders are empirical. Only for a true elementary step do they "
                    "happen to equal the stoichiometry.",
                ),
                q(
                    "In the Arrhenius equation k = A exp(-E_a / R T), what does a higher "
                    "activation energy E_a mean?",
                    (
                        opt("The rate is independent of temperature"),
                        opt(
                            "The rate constant is more sensitive to temperature - k "
                            "rises more steeply as T increases",
                            correct=True,
                        ),
                        opt("The reaction is always faster"),
                        opt("The pre-exponential factor becomes zero"),
                    ),
                    "E_a governs temperature sensitivity; a plot of ln k vs 1/T has slope -E_a/R.",
                ),
                q(
                    "Why is the reaction rate -r_A called an intensive property?",
                    (
                        opt("Because it depends on the total reactor volume"),
                        opt(
                            "Because it describes the chemistry per unit volume at a "
                            "point, independent of reactor size or type",
                            correct=True,
                        ),
                        opt("Because it is measured only in batch reactors"),
                        opt("Because it has units of moles only"),
                    ),
                    "Rate is per unit volume per unit time; the reactor design equation "
                    "then integrates it over the reactor.",
                ),
            ),
        ),
        # -- 2. Batch reactor ------------------------------------------
        _t(
            "Batch reactor design",
            "11 min",
            """# Batch reactor design

A **batch reactor** is charged with reactants, sealed, allowed to react
for a time, then emptied. There is no flow in or out during reaction, so
composition changes with **time**, not position. It is the workhorse of
low-volume, high-value chemistry - specialty chemicals, pharmaceuticals
(GMP batch records), fermentations.

The **general mole balance** on species A (in = out = 0, only generation
and accumulation) reduces to:

```text
dN_A / dt = r_A * V

  N_A : moles of A in the reactor
  r_A : rate of formation of A (negative for a reactant)
  V   : reaction volume
```

For **constant volume** (most liquid-phase batches), divide by V and work
in concentration, or work in **conversion** X, where
`N_A = N_A0 * (1 - X)`. The design equation becomes an integral for the
**time** needed to reach a target conversion:

```text
t = N_A0 * integral_0^X [ dX / ( -r_A * V ) ]

constant volume, first order  -r_A = k C_A :
    t = (1 / k) * ln( 1 / (1 - X) )
```

Worked example - how long to reach 90 percent conversion, first order,
`k = 0.05 / min`:

```python
import numpy as np

k = 0.05    # 1/min
X = 0.90
t = (1.0 / k) * np.log(1.0 / (1.0 - X))
print(f"t = {t:.1f} min")   # t = 46.1 min
```

Batch reactors trade **flexibility** (one vessel makes many products) for
**downtime**: every cycle includes charging, heating, reacting, cooling,
discharging, and cleaning. The productive fraction depends on that
turnaround, so real capacity uses the **total cycle time**, not just
reaction time.

```mermaid
graph TD
    CHARGE["Charge reactants"] --> REACT["React with time"]
    REACT --> BAL["Balance d N A dt equals r A times V"]
    BAL --> CONV["Integrate to target conversion"]
    CONV --> DISCHARGE["Discharge product"]
    DISCHARGE --> CLEAN["Clean and turnaround"]
    CLEAN --> CHARGE
```

Remember: in a batch reactor time is the design variable. Integrate the
mole balance from zero to the target conversion to get reaction time, then
add turnaround for real throughput.
""",
        ),
        quiz_lesson(
            "Quiz: Batch reactor design",
            (
                q(
                    "In a batch reactor, composition changes with what?",
                    (
                        opt("Position along a tube"),
                        opt("Time - there is no flow in or out during reaction", correct=True),
                        opt("The feed flow rate"),
                        opt("Nothing; it is at steady state"),
                    ),
                    "Batch is unsteady in time and uniform in space; the design "
                    "variable is reaction time.",
                ),
                q(
                    "For a constant-volume first-order batch reaction, the time to reach "
                    "conversion X is t = (1/k) ln(1/(1-X)). What does this imply as X "
                    "approaches 1?",
                    (
                        opt("Time approaches zero"),
                        opt(
                            "Time grows without bound - the last few percent of "
                            "conversion take disproportionately long",
                            correct=True,
                        ),
                        opt("Time is exactly proportional to X"),
                        opt("Time becomes negative"),
                    ),
                    "The logarithm diverges as X -> 1; chasing full conversion is "
                    "expensive in reactor time.",
                ),
                q(
                    "Why does real batch capacity use total cycle time rather than "
                    "reaction time alone?",
                    (
                        opt("Because the rate law changes between batches"),
                        opt(
                            "Each cycle also includes charging, heating, cooling, "
                            "discharging and cleaning - turnaround that reduces "
                            "productive fraction",
                            correct=True,
                        ),
                        opt("Because conversion is always 100 percent"),
                        opt("Because batch reactors run continuously"),
                    ),
                    "Throughput depends on the whole cycle, not just the reacting portion.",
                ),
            ),
        ),
        # -- 3. CSTR ---------------------------------------------------
        _t(
            "CSTR design",
            "11 min",
            """# CSTR design

A **continuous stirred-tank reactor (CSTR)**, also called a mixed-flow
reactor, runs continuously: feed enters and product leaves at steady flow,
and the contents are assumed **perfectly mixed**. The critical consequence:
the composition everywhere in the tank equals the **exit** composition. The
reaction therefore proceeds at the *low* rate corresponding to the outlet
concentration - a fundamental drawback of a single CSTR.

At **steady state**, accumulation is zero, so the mole balance is purely
algebraic (in - out + generation = 0):

```text
F_A0 - F_A + r_A * V = 0
  =>  V = ( F_A0 - F_A ) / ( -r_A )
  =>  V = F_A0 * X / ( -r_A )_exit

  F_A0 : molar feed rate of A
  X    : conversion
  (-r_A)_exit : rate evaluated at OUTLET conditions
```

Because the balance is algebraic, CSTR sizing needs no integration - just
evaluate the rate at the exit state. Define the **space time**
`tau = V / v_0` (reactor volume over volumetric feed rate); it is the mean
residence time and the key sizing number.

Worked example - liquid-phase, first order `-r_A = k C_A`,
`k = 0.30 / min`, target `X = 0.80`:

```python
k = 0.30   # 1/min
X = 0.80
# for first order, constant density: tau = X / (k (1 - X))
tau = X / (k * (1.0 - X))
print(f"space time tau = {tau:.1f} min")   # tau = 13.3 min
V = tau * 100.0   # for v0 = 100 L/min  ->  V in litres
print(f"volume V = {V:.0f} L")             # V = 1333 L
```

CSTRs shine for **liquid-phase** reactions, easy **temperature control**
(the large mixed volume is a heat sink), handling **slurries or
suspended solids**, and steady round-the-clock operation. The price is
that operating at exit concentration makes a single CSTR the **largest**
of the ideal reactors for a given conversion - often solved by putting
several in series.

```mermaid
graph LR
    FEED["Feed F A0 at v0"] --> TANK["Perfectly mixed tank"]
    TANK --> EXIT["Exit at conversion X"]
    TANK --> RATE["Rate evaluated at exit concentration"]
    RATE --> SIZE["V equals F A0 X over minus r A"]
    EXIT --> SIZE
```

Remember: a CSTR is well mixed, so it works at the exit rate and its mole
balance is algebraic. Size it with `V = F_A0 X / (-r_A)_exit`; its weakness
is running everywhere at the lowest reaction rate.
""",
        ),
        quiz_lesson(
            "Quiz: CSTR design",
            (
                q(
                    "In an ideal CSTR, the reaction rate inside the tank corresponds to "
                    "which concentration?",
                    (
                        opt("The feed (inlet) concentration"),
                        opt(
                            "The exit concentration - because perfect mixing makes the "
                            "whole tank equal to the outlet composition",
                            correct=True,
                        ),
                        opt("The average of inlet and outlet"),
                        opt("A value that changes with position in the tank"),
                    ),
                    "Perfect mixing = uniform composition = exit composition, so the "
                    "reactor runs at the low exit rate.",
                ),
                q(
                    "Why does CSTR sizing require no integration, unlike a batch or PFR?",
                    (
                        opt("Because CSTRs have no reaction"),
                        opt(
                            "At steady state the mole balance is algebraic - the rate is "
                            "evaluated once at the constant exit condition",
                            correct=True,
                        ),
                        opt("Because conversion is always zero"),
                        opt("Because the volume is always fixed at 1000 L"),
                    ),
                    "Steady state removes accumulation and uniform composition removes "
                    "the spatial gradient, leaving V = F_A0 X / (-r_A).",
                ),
                q(
                    "What is the main disadvantage of a single CSTR compared with the "
                    "other ideal reactors?",
                    (
                        opt("It cannot handle liquids"),
                        opt("It cannot reach steady state"),
                        opt(
                            "Operating everywhere at the low exit concentration makes it "
                            "the largest reactor for a given conversion",
                            correct=True,
                        ),
                        opt("It has no temperature control"),
                    ),
                    "Running at the lowest rate is the cost of perfect mixing; CSTRs in "
                    "series recover much of the volume penalty.",
                ),
            ),
        ),
        # -- 4. PFR ----------------------------------------------------
        _t(
            "Plug-flow reactor (PFR) design",
            "11 min",
            """# Plug-flow reactor (PFR) design

A **plug-flow reactor (PFR)** is an ideal tube: fluid moves through as a
series of thin "plugs" that do not mix with the plugs ahead or behind, but
are perfectly mixed radially. Concentration changes **continuously along
the length** - high at the inlet, low at the outlet. Because most of the
reactor sits at higher concentration than the exit, a PFR runs at a
**higher average rate** than a CSTR for the same conversion.

Apply the mole balance to a differential slice of volume `dV`. At steady
state it gives a differential design equation you integrate along the
reactor:

```text
F_A0 * dX/dV = -r_A
  =>  V = F_A0 * integral_0^X [ dX / (-r_A) ]

first order, constant density  -r_A = k C_A0 (1 - X) :
    V = (v_0 / k) * ln( 1 / (1 - X) )
    equivalently  tau = (1/k) ln(1/(1-X))
```

Notice the PFR result matches the **batch** result with residence time
`tau` playing the role of batch time `t`. A PFR is, in effect, a batch
reactor carried along in the flow - distance replaces time.

Worked example - first order, `k = 0.30 / min`, `X = 0.80` (same numbers
as the CSTR lesson, for comparison):

```python
import numpy as np

k = 0.30   # 1/min
X = 0.80
tau_pfr = (1.0 / k) * np.log(1.0 / (1.0 - X))
print(f"PFR space time = {tau_pfr:.1f} min")   # 5.4 min

tau_cstr = X / (k * (1.0 - X))
print(f"CSTR space time = {tau_cstr:.1f} min") # 13.3 min
# same duty, the PFR is about 2.5x smaller here
```

PFRs (tubular and packed-bed reactors) are the standard for **gas-phase**
reactions, high throughput, and high conversion per pass. The trade-offs:
harder temperature control (hot spots can form) and pressure drop along
the tube, which the Ergun equation captures for packed beds.

```mermaid
graph LR
    IN["Inlet high concentration"] --> SLICE["Differential slice dV"]
    SLICE --> INTEG["Integrate F A0 dX equals minus r A dV"]
    INTEG --> OUT["Outlet low concentration"]
    OUT --> HIGHRATE["High average rate versus CSTR"]
```

Remember: a PFR changes composition along its length, so its design
equation is an integral - identical in form to the batch equation with
residence time replacing time. For a given conversion it is smaller than a
single CSTR.
""",
        ),
        quiz_lesson(
            "Quiz: Plug-flow reactor (PFR) design",
            (
                q(
                    "In a PFR, how does concentration behave?",
                    (
                        opt("It is uniform everywhere, equal to the exit"),
                        opt(
                            "It changes continuously along the length - high at the "
                            "inlet, low at the outlet",
                            correct=True,
                        ),
                        opt("It only changes with time, not position"),
                        opt("It stays equal to the inlet everywhere"),
                    ),
                    "Plug flow means no axial mixing; each plug reacts as it travels, so "
                    "composition varies with position.",
                ),
                q(
                    "Why does the PFR design equation take the same integral form as the "
                    "batch reactor equation?",
                    (
                        opt("They are both algebraic"),
                        opt(
                            "A plug of fluid in a PFR behaves like a batch carried along "
                            "in the flow - residence time replaces batch time",
                            correct=True,
                        ),
                        opt("Because both operate at the exit concentration"),
                        opt("Because neither one reacts"),
                    ),
                    "Distance-in-flow maps onto time-in-batch, so V = F_A0 integral "
                    "dX/(-r_A) mirrors the batch integral.",
                ),
                q(
                    "For the same first-order reaction and conversion, how does the PFR "
                    "volume compare with a single CSTR?",
                    (
                        opt("They are always identical"),
                        opt("The CSTR is always smaller"),
                        opt(
                            "The PFR is smaller, because it operates at a higher average "
                            "rate rather than only at the low exit concentration",
                            correct=True,
                        ),
                        opt("The PFR cannot reach that conversion"),
                    ),
                    "The PFR spends most of its length at higher concentration, so it "
                    "needs less volume for the same duty.",
                ),
            ),
        ),
        # -- 5. Comparing/combining reactors ---------------------------
        _t(
            "Comparing and combining reactors",
            "11 min",
            """# Comparing and combining reactors

There is a clean visual tool for comparing reactors: the
**Levenspiel plot**, `1 / (-r_A)` versus conversion `X`. The design
equations turn into **areas** on this plot:

```text
CSTR volume  =  F_A0 * [ 1/(-r_A) ]_exit * X     -> a RECTANGLE
PFR  volume  =  F_A0 * integral_0^X 1/(-r_A) dX  -> the AREA UNDER the curve
```

For **normal kinetics** (rate falls as conversion rises, so `1/(-r_A)`
rises with X), the rectangle is always larger than the area under the
curve: **a PFR is smaller than a single CSTR** for the same conversion.
The gap widens at high conversion, where `1/(-r_A)` shoots up.

But this reverses for **autocatalytic** or product-accelerated reactions,
where the rate first rises with conversion. There the curve dips, and a
CSTR operating at the minimum of `1/(-r_A)` can beat a PFR over that
region. The lesson: reactor choice depends on the **shape of the kinetics**,
not a fixed rule.

Combining reactors captures the best of both. Key patterns:

- **CSTRs in series** - each tank steps the conversion down; as you add
  tanks the staircase approaches the smooth PFR curve. Infinite CSTRs in
  series equals one PFR.
- **PFR then CSTR, or CSTR then PFR** - order matters, and the best
  arrangement depends on the Levenspiel curve shape.
- A **CSTR first** is often smart for autocatalytic or highly exothermic
  systems (the mixed volume is stable and gets you past the slow start),
  followed by a PFR to finish the conversion efficiently.

```python
import numpy as np

# CSTRs in series approaching a PFR (first order, k tau_total fixed)
k, X_target = 0.30, 0.80
for N in (1, 2, 4, 10):
    # equal-sized CSTRs in series, solve total tau for X_target
    # per-stage conversion factor: (1 - X) = (1 / (1 + k tau_i))^N
    tau_i = ((1.0 / (1.0 - X_target)) ** (1.0 / N) - 1.0) / k
    print(f"N={N:2d}  total tau = {N * tau_i:5.1f} min")
# total tau shrinks toward the PFR value (5.4 min) as N grows
```

```mermaid
graph LR
    C1["CSTR stage 1"] --> C2["CSTR stage 2"]
    C2 --> C3["CSTR stage 3"]
    C3 --> APPROX["Staircase approaches PFR curve"]
    APPROX --> PFR["Infinite stages equals one PFR"]
```

Remember: plot `1/(-r_A)` vs X. Normal kinetics favour the PFR (area under
the curve beats the rectangle); autocatalytic kinetics can favour a CSTR;
and reactors in series or in the right order beat either one alone.
""",
        ),
        quiz_lesson(
            "Quiz: Comparing and combining reactors",
            (
                q(
                    "On a Levenspiel plot of 1/(-r_A) versus X, what does the CSTR "
                    "volume correspond to?",
                    (
                        opt("The area under the curve"),
                        opt(
                            "A rectangle of height 1/(-r_A) at the exit conversion times "
                            "the conversion X",
                            correct=True,
                        ),
                        opt("The slope of the curve"),
                        opt("Zero, since a CSTR has no volume"),
                    ),
                    "CSTR = F_A0 times the exit value of 1/(-r_A) times X, a rectangle; "
                    "the PFR is the area under the curve.",
                ),
                q(
                    "For normal kinetics (rate decreasing with conversion), which single "
                    "reactor is smaller for the same conversion?",
                    (
                        opt("The CSTR"),
                        opt(
                            "The PFR - the area under the curve is less than the rectangle",
                            correct=True,
                        ),
                        opt("They are always equal"),
                        opt("Neither can reach the conversion"),
                    ),
                    "Because 1/(-r_A) rises with X, the rectangle exceeds the area, so "
                    "the PFR wins for normal kinetics.",
                ),
                q(
                    "What happens as you add more equal-sized CSTRs in series?",
                    (
                        opt("The total volume grows without limit"),
                        opt(
                            "The staircase approaches the smooth PFR curve; in the limit "
                            "of infinite stages the series equals one PFR",
                            correct=True,
                        ),
                        opt("Conversion becomes impossible"),
                        opt("Each stage must be larger than the last"),
                    ),
                    "Infinite CSTRs in series behave as a PFR, recovering the single-CSTR "
                    "volume penalty.",
                ),
            ),
        ),
        # -- 6. Multiple reactions / selectivity -----------------------
        _t(
            "Multiple reactions, selectivity and yield",
            "12 min",
            """# Multiple reactions, selectivity and yield

Real chemistry rarely runs one clean reaction. Usually a **desired**
product competes with **undesired** ones. Two classic structures:

```text
Parallel (competing):        Series (consecutive):
    A --> D  (desired)            A --> D --> U
    A --> U  (undesired)         (D is what you want,
                                  but it degrades to U)
```

For these systems, **conversion is not enough** - you can convert all of A
and still make mostly junk. Two better measures:

```text
Selectivity  S = (rate of desired D) / (rate of undesired U)
Yield        Y = (moles D formed) / (moles A reacted)
```

The whole game is maximizing selectivity/yield, and the key lever is the
**ratio of the two rate laws**. For parallel reactions
`r_D = k_D C_A^a1` and `r_U = k_U C_A^a2`:

```text
S = r_D / r_U = (k_D / k_U) * C_A^(a1 - a2)

  if a1 > a2  (desired order higher):  keep C_A HIGH  -> use a PFR/batch
  if a1 < a2  (desired order lower):   keep C_A LOW   -> use a CSTR
```

So the **reactor choice is dictated by selectivity**, not just size. A PFR
keeps concentrations high; a CSTR keeps them low (at the exit value). Also,
temperature tilts selectivity through the two activation energies:

```text
k_D / k_U = (A_D / A_U) * exp( -(E_D - E_U) / (R T) )

  E_D > E_U : raise T to favour the desired reaction
  E_D < E_U : lower T to favour the desired reaction
```

For **series** reactions `A -> D -> U`, D passes through a **maximum** in
time (or in PFR length): stop too early and little D has formed, run too
long and D degrades to U. There is an optimum residence time.

```python
import numpy as np
# series A -> D -> U, first order each; find residence time maximising C_D
k1, k2 = 0.4, 0.15   # 1/min
t_opt = np.log(k1 / k2) / (k1 - k2)   # classic result for max C_D
print(f"optimum residence time = {t_opt:.1f} min")
```

```mermaid
graph TD
    A["Reactant A"] --> D["Desired product D"]
    A --> U1["Undesired U parallel"]
    D --> U2["Degrades to U series"]
    D --> SEL["Selectivity D over U"]
    SEL --> CHOICE["Choose reactor and T and concentration"]
```

Remember: with multiple reactions, optimize **selectivity and yield**, not
just conversion. Concentration level (set by reactor type) and temperature
(set by the activation-energy difference) are your two main levers; series
reactions add an optimum residence time.
""",
        ),
        quiz_lesson(
            "Quiz: Multiple reactions, selectivity and yield",
            (
                q(
                    "Why is conversion alone an inadequate objective when multiple "
                    "reactions occur?",
                    (
                        opt("Because conversion cannot be measured"),
                        opt(
                            "You can fully convert the reactant and still make mostly "
                            "the undesired product - selectivity and yield matter",
                            correct=True,
                        ),
                        opt("Because conversion is always 100 percent"),
                        opt("Because multiple reactions have no rate law"),
                    ),
                    "Selectivity (desired vs undesired) and yield capture whether you "
                    "made the right product, not just how much A reacted.",
                ),
                q(
                    "For parallel reactions where the desired reaction has the higher "
                    "order in A, what favours selectivity to the desired product?",
                    (
                        opt("Keeping the concentration of A low, e.g. a CSTR"),
                        opt(
                            "Keeping the concentration of A high, e.g. a PFR or batch reactor",
                            correct=True,
                        ),
                        opt("Removing the reactant entirely"),
                        opt("Using an infinitely large CSTR"),
                    ),
                    "S scales with C_A^(a1-a2); when a1 > a2, high C_A boosts the "
                    "desired rate more, so a PFR/batch wins.",
                ),
                q(
                    "In a series reaction A -> D -> U, why is there an optimum residence "
                    "time for the intermediate D?",
                    (
                        opt("Because D never forms"),
                        opt(
                            "Too short and little D has formed; too long and D degrades "
                            "to U - so C_D passes through a maximum",
                            correct=True,
                        ),
                        opt("Because U forms before D"),
                        opt("Because the rate constants are equal"),
                    ),
                    "D is an intermediate; its concentration peaks at t = ln(k1/k2) / "
                    "(k1 - k2) for first-order steps.",
                ),
            ),
        ),
        # -- 7. Non-isothermal / energy balance ------------------------
        _t(
            "Non-isothermal reactors and the energy balance",
            "12 min",
            """# Non-isothermal reactors and the energy balance

Reactions release or absorb heat, and the rate depends exponentially on
temperature through Arrhenius. So temperature and conversion are
**coupled**: you cannot solve the mole balance alone - you must solve it
**simultaneously with an energy balance**. This is where reactor design
gets genuinely hard, and where safety lives.

The steady-state energy balance for a flow reactor balances heat generated
by reaction against heat removed and the sensible heat of the streams:

```text
Q_removed  -  ( -Delta_H_rxn ) * ( -r_A ) * V  =  sum( F_i * Cp_i ) * dT

  Delta_H_rxn : heat of reaction (negative = exothermic)
  Q_removed   : duty of the cooling jacket or coils
  Cp_i        : heat capacities of the streams

adiabatic case (Q = 0): a linear T-vs-X relation
    T = T_0 + ( (-Delta_H_rxn) * X ) / ( sum theta_i Cp_i )
```

The dangerous feedback: for an **exothermic** reaction, a rise in T raises
the rate (Arrhenius), which releases **more** heat, which raises T
further. If heat removal cannot keep up, the temperature runs away - a
**thermal runaway**. Managing this is the core of reactor safety (ASME
BPVC vessels, relief sizing, DIERS methodology).

**Multiple steady states** are the signature of this coupling. Plotting a
sigmoidal **heat-generated** curve `G(T)` against a straight
**heat-removed** line `R(T)` for a CSTR, they can cross at up to **three**
points. The outer two are stable; the middle one is unstable. Which one
the reactor settles at depends on start-up and cooling.

```python
import numpy as np
# adiabatic temperature rise for an exothermic reaction
dH = -80_000.0     # J/mol (exothermic)
X = 0.80
sum_theta_Cp = 250.0   # J/(mol K), per mole of A fed
T0 = 350.0             # K
T = T0 + (-dH) * X / sum_theta_Cp
print(f"adiabatic exit temperature = {T:.0f} K")  # ~606 K - very hot
```

```mermaid
graph TD
    RXN["Exothermic reaction"] --> HEAT["Releases heat"]
    HEAT --> TUP["Temperature rises"]
    TUP --> RATE["Arrhenius rate increases"]
    RATE --> HEAT
    COOL["Cooling duty Q removed"] --> BAL["Heat balance"]
    HEAT --> BAL
    BAL --> STABLE["Stable point or runaway"]
```

Remember: non-isothermal design solves the mole and energy balances
**together**. Exothermic reactions have a positive-feedback loop that can
run away, they can show multiple steady states, and adequate heat removal
is a safety requirement, not an optimization.
""",
        ),
        quiz_lesson(
            "Quiz: Non-isothermal reactors and the energy balance",
            (
                q(
                    "Why must a non-isothermal reactor be solved with the mole and "
                    "energy balances together?",
                    (
                        opt("Because the mole balance has no solution"),
                        opt(
                            "Rate depends exponentially on temperature (Arrhenius) while "
                            "reaction changes temperature - conversion and T are coupled",
                            correct=True,
                        ),
                        opt("Because temperature is always constant"),
                        opt("Because the energy balance replaces the rate law"),
                    ),
                    "T sets the rate and the reaction sets T; the two balances are "
                    "solved simultaneously.",
                ),
                q(
                    "What drives a thermal runaway in an exothermic reactor?",
                    (
                        opt("Cooling that is too aggressive"),
                        opt(
                            "A positive feedback loop: higher T raises the rate, which "
                            "releases more heat, which raises T further, if heat removal "
                            "cannot keep up",
                            correct=True,
                        ),
                        opt("The reaction becoming endothermic"),
                        opt("The reactant running out"),
                    ),
                    "Arrhenius feedback plus insufficient heat removal is the runaway "
                    "mechanism; relief sizing and DIERS address it.",
                ),
                q(
                    "The intersection of the heat-generation curve G(T) and the "
                    "heat-removal line R(T) for a CSTR can produce what?",
                    (
                        opt("Exactly one steady state always"),
                        opt(
                            "Up to three steady states - the outer two stable and the "
                            "middle one unstable",
                            correct=True,
                        ),
                        opt("No steady state ever"),
                        opt("Only endothermic operation"),
                    ),
                    "Multiple steady states arise from the S-shaped generation curve "
                    "crossing the removal line; ignition/extinction depends on start-up.",
                ),
            ),
        ),
        # -- 8. Catalysis / heterogeneous ------------------------------
        _t(
            "Catalysis and heterogeneous reactions",
            "12 min",
            """# Catalysis and heterogeneous reactions

Most industrial reactions use a **catalyst** - a substance that speeds a
reaction by offering a lower-energy pathway, without being consumed. It
lowers the **activation energy**, so a catalyzed reaction reaches useful
rates at much lower temperature. Crucially a catalyst changes the **rate**,
never the **equilibrium**: it speeds the forward and reverse reactions
equally, so `K_eq` is untouched.

Most industrial catalysts are **heterogeneous solids** (a different phase
from the fluid reactants) - packed beds of metal-on-support pellets:
platinum reforming, iron for ammonia (Haber-Bosch), zeolites for cracking.
The reaction happens on the **surface**, through a sequence of steps:

```text
1. External diffusion : reactant moves from the bulk fluid to the pellet
2. Internal diffusion : reactant diffuses into the porous pellet
3. Adsorption         : reactant binds to an active site
4. Surface reaction   : the bound species react
5. Desorption         : product leaves the site
6. Diffusion out      : product returns to the bulk fluid
```

The **slowest** step controls the overall rate. If a chemical step
governs, the reactor is **reaction-limited** (raising T helps a lot). If
diffusion governs, it is **mass-transfer-limited** (raising T barely helps;
you need smaller pellets or better mixing instead).

Adsorption-based kinetics are usually written as
**Langmuir-Hinshelwood** rate laws (rate rises then saturates as a site
becomes fully covered). Whether internal diffusion matters is captured by
the **Thiele modulus** `phi` and the **effectiveness factor** `eta`:

```text
Thiele modulus  phi  ~ (pellet size) * sqrt( rate constant / diffusivity )
effectiveness   eta  = (actual rate) / (rate with no diffusion limit)

  small phi  -> eta ~ 1  : kinetics control, whole pellet is used
  large phi  -> eta << 1 : diffusion controls, only the outer shell reacts
```

Catalysts **deactivate** over time - sintering, coking (carbon fouling),
and poisoning (e.g. sulfur on metal sites) - which is why refineries
regenerate or replace catalyst on a schedule.

```python
import numpy as np
# effectiveness factor for a first-order spherical pellet
phi = 2.0
eta = (3.0 / phi**2) * (phi / np.tanh(phi) - 1.0)
print(f"effectiveness factor eta = {eta:.2f}")  # ~0.81
# eta < 1 signals internal diffusion is stealing some of the rate
```

```mermaid
graph LR
    BULK["Reactant in bulk fluid"] --> EXT["External diffusion to pellet"]
    EXT --> INT["Internal diffusion in pores"]
    INT --> ADS["Adsorb on active site"]
    ADS --> SURF["Surface reaction"]
    SURF --> DES["Desorb product"]
    DES --> OUT["Diffuse back to bulk"]
```

Remember: a catalyst lowers activation energy and speeds rate without
shifting equilibrium. In heterogeneous catalysis the slowest of the
diffusion-adsorption-reaction steps controls; the Thiele modulus and
effectiveness factor tell you whether chemistry or mass transfer is in
charge, and catalysts deactivate over time.
""",
        ),
        quiz_lesson(
            "Quiz: Catalysis and heterogeneous reactions",
            (
                q(
                    "How does a catalyst speed up a reaction, and what does it NOT change?",
                    (
                        opt("It raises the activation energy and shifts equilibrium"),
                        opt(
                            "It lowers the activation energy (a faster pathway) but does "
                            "not change the equilibrium constant",
                            correct=True,
                        ),
                        opt("It is consumed to provide energy"),
                        opt("It changes the heat of reaction only"),
                    ),
                    "A catalyst speeds forward and reverse equally, so K_eq is "
                    "unchanged; it just gets you there faster.",
                ),
                q(
                    "In a heterogeneous catalytic reaction, what determines the overall "
                    "observed rate?",
                    (
                        opt("Always the adsorption step"),
                        opt("The fastest of the steps"),
                        opt(
                            "The slowest step among external/internal diffusion, "
                            "adsorption, surface reaction and desorption",
                            correct=True,
                        ),
                        opt("The colour of the catalyst"),
                    ),
                    "The rate-limiting (slowest) step controls; whether it is chemistry "
                    "or diffusion decides how temperature affects the rate.",
                ),
                q(
                    "A large Thiele modulus with an effectiveness factor well below 1 "
                    "indicates what?",
                    (
                        opt("The reaction is at equilibrium"),
                        opt(
                            "Internal diffusion controls - only the outer shell of the "
                            "pellet reacts, so smaller pellets help more than higher "
                            "temperature",
                            correct=True,
                        ),
                        opt("The catalyst has infinite activity"),
                        opt("Kinetics fully control and the whole pellet is used"),
                    ),
                    "eta << 1 means the reactant cannot penetrate the pellet; reduce "
                    "pellet size or improve diffusion rather than just raising T.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In the rate law -r_A = k C_A^a C_B^b, where do the orders a and b come from?",
                    (
                        opt("The stoichiometric coefficients of the balanced equation"),
                        opt(
                            "Experiment - they are empirical and need not match the stoichiometry",
                            correct=True,
                        ),
                        opt("The molecular weights"),
                        opt("They are always 1"),
                    ),
                    "Orders are measured; only true elementary steps match the stoichiometry.",
                ),
                q(
                    "What does the Arrhenius equation describe?",
                    (
                        opt("The pressure drop across a packed bed"),
                        opt(
                            "How the rate constant k depends on temperature, k = A exp(-E_a / R T)",
                            correct=True,
                        ),
                        opt("The equilibrium composition"),
                        opt("The heat capacity of the fluid"),
                    ),
                    "Arrhenius gives the temperature dependence of k; ln k vs 1/T is a "
                    "line of slope -E_a/R.",
                ),
                q(
                    "In a batch reactor, what is the design variable?",
                    (
                        opt("Position along a tube"),
                        opt(
                            "Reaction time - integrate the mole balance to a target conversion",
                            correct=True,
                        ),
                        opt("The feed flow rate"),
                        opt("The exit concentration only"),
                    ),
                    "Batch is unsteady in time; the integral of the mole balance gives "
                    "the reaction time.",
                ),
                q(
                    "Why is the CSTR mole balance algebraic rather than an integral?",
                    (
                        opt("Because a CSTR does not react"),
                        opt(
                            "At steady state with perfect mixing the rate is evaluated "
                            "once at the constant exit condition",
                            correct=True,
                        ),
                        opt("Because conversion is always zero"),
                        opt("Because it is a batch reactor"),
                    ),
                    "V = F_A0 X / (-r_A) evaluated at exit; no spatial or time integral needed.",
                ),
                q(
                    "For the same first-order reaction and conversion, which single "
                    "reactor needs the least volume?",
                    (
                        opt("The single CSTR"),
                        opt("The PFR, because it runs at a higher average rate", correct=True),
                        opt("They are always equal"),
                        opt("The batch reactor is always largest"),
                    ),
                    "The PFR spends most of its length at higher concentration; on a "
                    "Levenspiel plot the area beats the CSTR rectangle.",
                ),
                q(
                    "On a Levenspiel plot, the PFR volume is represented by what?",
                    (
                        opt("A rectangle at the exit conversion"),
                        opt("The area under the 1/(-r_A) versus X curve", correct=True),
                        opt("The slope of the curve"),
                        opt("A single point"),
                    ),
                    "PFR = area under the curve; CSTR = rectangle of exit height times X.",
                ),
                q(
                    "With multiple reactions, what should you optimize beyond conversion?",
                    (
                        opt("Only the reactor colour"),
                        opt("Selectivity and yield toward the desired product", correct=True),
                        opt("The pump horsepower"),
                        opt("Nothing else matters"),
                    ),
                    "You can convert all of A and still make junk; selectivity and yield "
                    "measure whether you made the right product.",
                ),
                q(
                    "For parallel reactions where the desired reaction is higher order "
                    "in A, which reactor helps selectivity?",
                    (
                        opt("A CSTR, which keeps C_A low"),
                        opt("A PFR or batch, which keeps C_A high", correct=True),
                        opt("Any reactor works identically"),
                        opt("Only an empty reactor"),
                    ),
                    "S scales with C_A^(a1-a2); when a1 > a2 keep C_A high, so a "
                    "PFR/batch is preferred.",
                ),
                q(
                    "What is the danger unique to exothermic non-isothermal reactors?",
                    (
                        opt("They cool down uncontrollably"),
                        opt(
                            "Thermal runaway - higher T raises the rate, releasing more "
                            "heat, raising T further if cooling cannot keep up",
                            correct=True,
                        ),
                        opt("They cannot reach conversion"),
                        opt("They have no rate law"),
                    ),
                    "The Arrhenius positive-feedback loop plus insufficient heat removal "
                    "causes runaway; relief sizing manages it.",
                ),
                q(
                    "In heterogeneous catalysis, a catalyst changes the rate but not the "
                    "equilibrium because it…",
                    (
                        opt("is consumed during the reaction"),
                        opt("only works on the products"),
                        opt(
                            "lowers the activation energy of the forward and reverse "
                            "reactions equally, leaving K_eq unchanged",
                            correct=True,
                        ),
                        opt("raises the heat of reaction"),
                    ),
                    "Equal speed-up both ways means faster approach to the same "
                    "equilibrium; the slowest surface/diffusion step still limits rate.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CHEMICAL_REACTION_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_CHEMICAL_REACTION_ENGINEERING,)
