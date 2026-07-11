"""Academy seed content - Chemical Engineering Thermodynamics.

The thermodynamics that drives process design: PVT behavior and equations
of state, the first and second laws applied to flow processes, entropy and
exergy, thermodynamic properties and departure functions, the phase rule
and phase equilibrium, vapor-liquid equilibrium for separations, flash
calculations, and chemical reaction equilibrium. Every lesson is a direct
explanation with a worked equation or calculation and a mermaid diagram,
followed by a checkpoint quiz; the course closes with a comprehensive
final quiz.
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


_CHEMICAL_ENGINEERING_THERMODYNAMICS = SeedCourse(
    slug="chemical-engineering-thermodynamics",
    title="Chemical Engineering Thermodynamics",
    description=(
        "The thermodynamics that drives process design - equations of state, "
        "the laws applied to flow processes, phase and reaction equilibria, "
        "and vapor-liquid equilibrium for separations. Every lesson pairs a "
        "direct explanation with a worked design equation or calculation and a "
        "process diagram, grounded in real practice (Antoine, Peng-Robinson, "
        "Aspen/DWSIM, McCabe-Thiele)."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Chemical Engineering Thermodynamics

Thermodynamics is the quantitative backbone of process design. It tells
you how much energy a compressor needs, how a mixture splits between vapor
and liquid in a distillation column, and how far a reaction can go before
it stalls at equilibrium. Every flowsheet in Aspen Plus, HYSYS, or DWSIM
rests on the ideas in this course.

The approach is **direct and worked**: every lesson explains one idea
clearly, applies it in a short calculation (an equation of state, an
energy balance, an equilibrium relation), and draws it as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **PVT behavior and equations of state** - how real fluids deviate from ideal
2. **The first law for flow processes** - energy balances on open systems
3. **The second law, entropy and exergy** - direction, efficiency, lost work
4. **Thermodynamic properties and departure functions** - H, S, G of real fluids
5. **Phase equilibrium and the phase rule** - degrees of freedom and criteria
6. **Vapor-liquid equilibrium** - Raoult's law and activity coefficients
7. **Flash calculations** - splitting a feed into vapor and liquid
8. **Chemical reaction equilibrium** - how far a reaction proceeds

This is the map from molecular behavior to the unit operations that
separate and react. Master it once and the rest of process design becomes
a series of applications.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What role does thermodynamics play in process design?",
                    (
                        opt("It only matters for academic exams, not real plants"),
                        opt(
                            "It quantifies energy requirements and phase and reaction "
                            "equilibria - the foundation every flowsheet simulator rests on",
                            correct=True,
                        ),
                        opt("It is only about measuring temperatures"),
                        opt("It replaces the need for mass balances"),
                    ),
                    "Thermodynamics sets energy needs, how mixtures split between phases, "
                    "and how far reactions go - the core of design.",
                ),
                q(
                    "How is each lesson structured in this course?",
                    (
                        opt("Only historical background, no math"),
                        opt(
                            "A direct explanation, a worked equation or calculation, and "
                            "a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Just a list of definitions to memorize"),
                        opt("A single long video with no examples"),
                    ),
                    "Explain the idea, apply it in a calculation, draw it, then check "
                    "understanding with a quiz.",
                ),
            ),
        ),
        # -- 1. PVT and equations of state -----------------------------
        _t(
            "PVT behavior and equations of state",
            "11 min",
            """# PVT behavior and equations of state

A fluid's **pressure, molar volume, and temperature** (PVT) are linked by
an **equation of state (EOS)**. The simplest is the **ideal gas law**,
`PV = RT`, valid only at low pressure and high temperature where molecules
are far apart and do not interact. Real fluids deviate, and the deviation
is captured by the **compressibility factor** Z:

```text
Z = PV / (RT)

Z = 1      ideal gas
Z < 1      attractive forces dominate (near condensation)
Z > 1      repulsive forces dominate (high pressure)
```

For real fluids, **cubic equations of state** add a repulsive (volume) and
an attractive term. The **van der Waals** equation was first; modern
process simulators default to **Soave-Redlich-Kwong (SRK)** and
**Peng-Robinson (PR)**, which predict vapor and liquid densities and
vapor pressures well for hydrocarbons and light gases:

```text
Peng-Robinson:

P = RT / (V - b)  -  a(T) / (V*(V + b) + b*(V - b))

a(T) captures attraction (depends on Tc, Pc, acentric factor omega)
b    captures molecular volume (depends on Tc, Pc)
```

The **critical point** (Tc, Pc) is where the vapor and liquid become
indistinguishable; the **acentric factor** omega measures how non-spherical
a molecule is. These constants let one EOS describe many species.

The **principle of corresponding states** says fluids at the same
**reduced** conditions `Tr = T/Tc` and `Pr = P/Pc` have roughly the same
Z. This underlies generalized charts and the parameters in cubic EOS.

```mermaid
graph TD
    PVT["Measured P V and T"] --> IDEAL["Ideal gas PV equals RT"]
    IDEAL --> DEV["Real fluid deviates"]
    DEV --> Z["Compressibility factor Z"]
    DEV --> CUBIC["Cubic EOS SRK or PR"]
    CUBIC --> CONST["Uses Tc Pc and omega"]
    CONST --> CORR["Corresponding states"]
```

Remember: the ideal gas law is the starting point, and a cubic EOS such as
Peng-Robinson is what a simulator actually uses to get real densities,
enthalpies, and phase behavior.
""",
        ),
        quiz_lesson(
            "Quiz: PVT behavior and equations of state",
            (
                q(
                    "What does the compressibility factor Z measure?",
                    (
                        opt("The temperature of a fluid in kelvin"),
                        opt(
                            "How far a real fluid deviates from ideal-gas behavior; "
                            "Z = PV/(RT), equal to 1 for an ideal gas",
                            correct=True,
                        ),
                        opt("The mass of one mole of gas"),
                        opt("The speed of sound in the fluid"),
                    ),
                    "Z = PV/(RT); Z below 1 means attraction dominates, above 1 means "
                    "repulsion dominates.",
                ),
                q(
                    "Which equations of state do modern process simulators default to "
                    "for hydrocarbons?",
                    (
                        opt("Only the ideal gas law"),
                        opt(
                            "Cubic equations such as Soave-Redlich-Kwong and Peng-Robinson",
                            correct=True,
                        ),
                        opt("Newton's law of cooling"),
                        opt("The Nernst equation"),
                    ),
                    "SRK and Peng-Robinson add attractive and repulsive terms and predict "
                    "real densities and vapor pressures well.",
                ),
                q(
                    "What does the principle of corresponding states assert?",
                    (
                        opt("All fluids boil at the same temperature"),
                        opt(
                            "Fluids at the same reduced temperature and pressure "
                            "(T/Tc and P/Pc) have approximately the same Z",
                            correct=True,
                        ),
                        opt("Pressure and volume are always independent"),
                        opt("Critical points do not exist"),
                    ),
                    "Reduced conditions collapse many fluids onto one generalized "
                    "behavior - the basis for generalized charts and EOS parameters.",
                ),
            ),
        ),
        # -- 2. First law for flow processes ---------------------------
        _t(
            "The first law for flow processes",
            "11 min",
            """# The first law for flow processes

The **first law** is conservation of energy. For a **closed system** it is
`dU = dQ - dW`. But chemical plants run **open systems** - fluid flows
continuously through pumps, turbines, heat exchangers, and reactors - so we
need the **control-volume** form.

At **steady state**, the energy balance on an open system with one inlet
and one outlet is the **steady-flow energy equation**:

```text
Q - Ws = dH + d(u^2 / 2) + g*dz      (per unit mass)

Q   = heat added to the fluid
Ws  = shaft work done BY the fluid
dH  = enthalpy change (outlet minus inlet)
d(u^2/2) = kinetic energy change
g*dz = potential energy change
```

The key insight: fluid crossing a boundary carries **enthalpy** H = U + PV,
not just internal energy, because the flowing stream also does **flow work**
(PV) pushing itself across the boundary. That is why open-system balances
are written in H, not U.

For most process units, kinetic and potential terms are negligible, so the
balance simplifies to `Q - Ws = dH`. This gives fast results:

```text
Adiabatic turbine (Q = 0):   Ws = -dH = H_in - H_out
Pump/compressor (Q = 0):     Ws = -dH  (work input, dH > 0)
Heat exchanger (Ws = 0):     Q = dH
Throttle valve (Q = 0, Ws = 0):  dH = 0  (isenthalpic)
```

A **throttling valve** is isenthalpic: enthalpy is conserved, and for a
real gas the temperature usually drops (the **Joule-Thomson effect**),
which is how refrigeration and gas liquefaction cycles work.

```mermaid
graph LR
    IN["Inlet stream H in"] --> CV["Control volume unit"]
    Q["Heat Q added"] --> CV
    CV --> OUT["Outlet stream H out"]
    CV --> WS["Shaft work Ws out"]
    CV --> BAL["Q minus Ws equals delta H"]
```

Remember: for flowing systems the energy currency is **enthalpy**, and at
steady state `Q - Ws = dH` sizes almost every heater, cooler, pump, and
turbine on the flowsheet.
""",
        ),
        quiz_lesson(
            "Quiz: The first law for flow processes",
            (
                q(
                    "Why do open-system (flow) energy balances use enthalpy rather than "
                    "internal energy?",
                    (
                        opt("Enthalpy is easier to spell"),
                        opt(
                            "A flowing stream also does flow work (PV) to cross the "
                            "boundary, and H = U + PV bundles that in",
                            correct=True,
                        ),
                        opt("Internal energy cannot be measured"),
                        opt("Enthalpy is always zero for gases"),
                    ),
                    "Flow work PV plus internal energy U equals enthalpy H, the natural "
                    "currency for streams crossing a control-volume boundary.",
                ),
                q(
                    "For an adiabatic steady-flow turbine with negligible kinetic and "
                    "potential terms, the shaft work equals what?",
                    (
                        opt("The heat added, Q"),
                        opt(
                            "The enthalpy drop of the fluid: Ws = H_in - H_out",
                            correct=True,
                        ),
                        opt("Zero, always"),
                        opt("The pressure times the volume of the vessel"),
                    ),
                    "With Q = 0 and negligible KE/PE, Q - Ws = dH gives Ws = -dH = H_in - H_out.",
                ),
                q(
                    "A throttling (expansion) valve is best described as which kind of process?",
                    (
                        opt("Isothermal - constant temperature"),
                        opt("Isobaric - constant pressure"),
                        opt(
                            "Isenthalpic - constant enthalpy, with no shaft work and "
                            "no heat, often producing a Joule-Thomson temperature drop",
                            correct=True,
                        ),
                        opt("Isochoric - constant volume"),
                    ),
                    "With Q = 0 and Ws = 0, dH = 0; the Joule-Thomson effect cools most "
                    "real gases on expansion, enabling liquefaction cycles.",
                ),
            ),
        ),
        # -- 3. Second law, entropy, exergy ----------------------------
        _t(
            "The second law, entropy and exergy",
            "11 min",
            """# The second law, entropy and exergy

The first law says energy is conserved, but it does not say which way a
process will go. The **second law** supplies direction: for any real
process the **entropy** of the universe increases. Entropy S measures the
dispersal of energy; a **reversible** (idealized, infinitely slow) process
generates none, while every real process generates some.

For an **open system** at steady state, the entropy balance is:

```text
dS_dot = sum(m_dot_out * s_out) - sum(m_dot_in * s_in) - sum(Q_dot / T)

S_gen (entropy generation) >= 0    always
S_gen = 0   reversible (ideal) process
S_gen > 0   real, irreversible process
```

Entropy generation is never negative, and it is the fingerprint of
**irreversibility**: friction, unrestrained expansion, heat flow across a
finite temperature difference, mixing.

The practical payoff is **lost work** and **exergy**. Exergy (available
work) is the *maximum* useful work a stream can deliver as it comes to
equilibrium with the surroundings at T0. The **Gouy-Stodola** theorem ties
wasted potential directly to entropy generation:

```text
Lost work:   W_lost = T0 * S_gen

T0     = surroundings (dead-state) temperature
S_gen  = entropy generated by the process
```

Every bit of entropy you generate destroys `T0 * S_gen` of work you could
have had. This is why an **exergy analysis** - not just an energy balance -
tells you *where* a plant wastes its capacity to do work (often the
biggest losses are in combustion and heat transfer across large delta-T).

Real machines are rated against the reversible ideal by an **isentropic
efficiency**: for a turbine, actual work divided by the work of a
reversible (constant-entropy) expansion between the same pressures.

```mermaid
graph TD
    PROC["Real process"] --> SGEN["Entropy generation S gen"]
    SGEN --> DIR["Sets allowed direction"]
    SGEN --> LOST["Lost work equals T0 times S gen"]
    LOST --> EX["Exergy destroyed"]
    EX --> ANALYSIS["Exergy analysis finds waste"]
    ANALYSIS --> IMPROVE["Target the biggest losses"]
```

Remember: the first law counts energy, the second law counts its
**quality**. Minimizing entropy generation - and the lost work it causes -
is how you make a process efficient.
""",
        ),
        quiz_lesson(
            "Quiz: The second law, entropy and exergy",
            (
                q(
                    "What does the second law add that the first law does not provide?",
                    (
                        opt("A way to weigh the fluid"),
                        opt(
                            "The direction of a process: entropy of the universe "
                            "increases, so real processes generate entropy",
                            correct=True,
                        ),
                        opt("The color of the fluid"),
                        opt("The exact molecular weight"),
                    ),
                    "Energy is conserved either way; entropy generation (never negative) "
                    "picks the feasible direction.",
                ),
                q(
                    "The Gouy-Stodola relation W_lost = T0 * S_gen says what?",
                    (
                        opt("Lost work is independent of entropy generation"),
                        opt(
                            "The work destroyed by irreversibility equals the "
                            "surroundings temperature times the entropy generated",
                            correct=True,
                        ),
                        opt("Entropy generation can be negative"),
                        opt("Work is created out of nothing"),
                    ),
                    "Every unit of S_gen destroys T0 * S_gen of available work - the "
                    "reason exergy analysis targets irreversibility.",
                ),
                q(
                    "What is exergy (availability) of a stream?",
                    (
                        opt("Its total mass"),
                        opt("Its temperature only"),
                        opt(
                            "The maximum useful work it can deliver as it comes to "
                            "equilibrium with the surroundings",
                            correct=True,
                        ),
                        opt("The number of moles it contains"),
                    ),
                    "Exergy is the quality of energy - the work potential relative to the "
                    "dead state at T0; irreversibility destroys it.",
                ),
            ),
        ),
        # -- 4. Properties and departure functions ---------------------
        _t(
            "Thermodynamic properties and departure functions",
            "11 min",
            """# Thermodynamic properties and departure functions

Energy and entropy balances need **enthalpy H, entropy S, and Gibbs energy
G** for real fluids at real conditions. We build them from measurable data
using two tools: the **residual (departure) function** and the **fugacity**.

An ideal gas is easy: its H depends only on temperature, computed from the
**heat capacity** Cp. The trick is to correct that ideal value for real
behavior with a **departure function**, which an equation of state
supplies:

```text
Real property = ideal-gas property + departure

H(T,P)  = H_ideal(T)  + H_departure(T,P)
S(T,P)  = S_ideal(T,P) + S_departure(T,P)

Departure = (real value) - (ideal-gas value at the same T and P)
```

So to get the enthalpy change across a compressor, a simulator: (1)
computes the ideal-gas enthalpy change from Cp integrated over T, then (2)
adds the departure terms from the EOS at the inlet and outlet states. No
real gas is ever assumed ideal in the final numbers.

The **Maxwell relations** (from the exactness of the property differentials)
let us express hard-to-measure quantities in terms of PVT data. For
example, the temperature dependence of entropy at constant T uses only an
equation of state:

```text
(dS/dP)_T = -(dV/dT)_P        one Maxwell relation

Given an EOS V(T,P), this integrates to the entropy departure.
```

For phase and reaction equilibrium the central property is the **fugacity**
f - an "effective pressure" that makes the real-gas chemical potential look
like the ideal-gas one. The **fugacity coefficient** phi = f/P is 1 for an
ideal gas and is computed from an EOS:

```text
mu_real - mu_ideal = RT * ln(f / P) = RT * ln(phi)

phi = 1     ideal gas
phi != 1    real fluid, from the EOS
```

Fugacity is the quantity that must be **equal in every phase** at
equilibrium - the bridge to the next lessons.

```mermaid
graph TD
    CP["Heat capacity Cp data"] --> IDEAL["Ideal gas H and S"]
    EOS["Equation of state"] --> DEP["Departure functions"]
    IDEAL --> REAL["Real H S and G"]
    DEP --> REAL
    REAL --> FUG["Fugacity and phi"]
    FUG --> EQUIL["Used in phase and reaction equilibrium"]
```

Remember: real properties are the ideal-gas value plus an EOS-based
departure, and **fugacity** is the property that governs equilibrium
between phases and in reactions.
""",
        ),
        quiz_lesson(
            "Quiz: Thermodynamic properties and departure functions",
            (
                q(
                    "How does a simulator compute the real enthalpy of a fluid at a given T and P?",
                    (
                        opt("It always assumes the ideal-gas value"),
                        opt(
                            "Ideal-gas enthalpy from Cp plus a departure function from "
                            "the equation of state",
                            correct=True,
                        ),
                        opt("It measures it directly with a thermometer"),
                        opt("It sets enthalpy to zero for all fluids"),
                    ),
                    "Real property = ideal-gas property + departure; the EOS supplies the "
                    "departure correction.",
                ),
                q(
                    "What is the fugacity coefficient phi?",
                    (
                        opt("The mass of the fluid divided by its volume"),
                        opt(
                            "The ratio f/P; it equals 1 for an ideal gas and is computed "
                            "from an EOS for a real fluid",
                            correct=True,
                        ),
                        opt("The reaction rate constant"),
                        opt("The heat capacity at constant pressure"),
                    ),
                    "phi = f/P measures departure from ideal-gas chemical potential; "
                    "phi = 1 means ideal.",
                ),
                q(
                    "What quantity must be equal in every phase at equilibrium?",
                    (
                        opt("Density"),
                        opt("Viscosity"),
                        opt("Fugacity of each component", correct=True),
                        opt("Thermal conductivity"),
                    ),
                    "Equal fugacity of a species across phases is the equilibrium "
                    "criterion the next lessons build on.",
                ),
            ),
        ),
        # -- 5. Phase equilibrium and the phase rule -------------------
        _t(
            "Phase equilibrium and the phase rule",
            "11 min",
            """# Phase equilibrium and the phase rule

Separations - distillation, absorption, extraction - all rely on how a
mixture distributes itself between **phases** at equilibrium. Two questions
frame the topic: *what is the condition for equilibrium*, and *how many
variables am I free to set*.

The **condition for phase equilibrium** is that temperature, pressure, and
the **fugacity of every component** are equal in all phases:

```text
At equilibrium between vapor (V) and liquid (L):

T_V = T_L,   P_V = P_L,   and for every species i:
f_i(V) = f_i(L)

Equal fugacity is what drives mass transfer to a halt.
```

The bookkeeping of freedom is the **Gibbs phase rule**. It counts the
**degrees of freedom** F - the number of intensive variables (T, P,
compositions) you can independently fix:

```text
F = C - P + 2

C = number of components
P = number of phases present
2 = temperature and pressure

Example - pure water (C = 1):
  1 phase (liquid):        F = 1 - 1 + 2 = 2  (set T and P freely)
  2 phases (liq + vapor):  F = 1 - 2 + 2 = 1  (boiling line: fix T, P follows)
  3 phases (triple point): F = 1 - 3 + 2 = 0  (fixed, invariant point)
```

For a **binary** mixture (C = 2) with vapor and liquid present, F = 2: fix
temperature and pressure and the compositions of both phases are
determined - the basis of a Txy or Pxy diagram. This is why a
two-component vapor-liquid system has a well-defined bubble and dew line.

```mermaid
graph TD
    MIX["Multicomponent mixture"] --> COND["Equilibrium condition"]
    COND --> TEQ["T equal in all phases"]
    COND --> PEQ["P equal in all phases"]
    COND --> FEQ["Fugacity equal per component"]
    MIX --> RULE["Phase rule F equals C minus P plus 2"]
    RULE --> DOF["Degrees of freedom to fix"]
```

Remember: equilibrium means **equal fugacity** for every species across
phases, and the **phase rule** F = C - P + 2 tells you how many conditions
you get to choose before the rest are locked in.
""",
        ),
        quiz_lesson(
            "Quiz: Phase equilibrium and the phase rule",
            (
                q(
                    "What is the Gibbs phase rule?",
                    (
                        opt("F = P - C - 2"),
                        opt(
                            "F = C - P + 2, where C is components, P is phases, and F is "
                            "degrees of freedom",
                            correct=True,
                        ),
                        opt("F = C times P"),
                        opt("F = 2C + P"),
                    ),
                    "Degrees of freedom = components minus phases plus 2 (for T and P).",
                ),
                q(
                    "At the triple point of pure water, how many degrees of freedom are there?",
                    (
                        opt("Two - set T and P freely"),
                        opt("One - fix T and P follows"),
                        opt(
                            "Zero - it is an invariant point, fully fixed",
                            correct=True,
                        ),
                        opt("Three"),
                    ),
                    "C = 1, P = 3, so F = 1 - 3 + 2 = 0; the triple point occurs at a "
                    "single fixed T and P.",
                ),
                q(
                    "What is the thermodynamic condition for vapor-liquid equilibrium of "
                    "a component?",
                    (
                        opt("Its mass is equal in both phases"),
                        opt("Its density is equal in both phases"),
                        opt(
                            "Its fugacity is equal in the vapor and the liquid (with T "
                            "and P also equal)",
                            correct=True,
                        ),
                        opt("Its viscosity is equal in both phases"),
                    ),
                    "Equal fugacity per species, plus equal T and P, defines phase "
                    "equilibrium and stops net mass transfer.",
                ),
            ),
        ),
        # -- 6. Vapor-liquid equilibrium -------------------------------
        _t(
            "Vapor-liquid equilibrium (Raoult's law, activity coefficients)",
            "12 min",
            """# Vapor-liquid equilibrium (Raoult's law, activity coefficients)

**Vapor-liquid equilibrium (VLE)** is the workhorse of separations. It
relates the vapor composition y to the liquid composition x for each
species. The simplest model is **Raoult's law**, valid for **ideal**
mixtures of similar molecules:

```text
Raoult's law (ideal liquid):

y_i * P = x_i * P_i_sat(T)

y_i        vapor mole fraction
x_i        liquid mole fraction
P          total pressure
P_i_sat(T) pure-component vapor pressure at T
```

The **vapor pressure** P_sat comes from the **Antoine equation**, a
correlation fit to data:

```text
Antoine equation:

log10(P_sat) = A - B / (T + C)

A, B, C are tabulated constants per compound (watch the units and the
log base - they vary by source).
```

The ratio that separation columns care about is the **K-value** and the
**relative volatility** alpha, which measures how much easier one component
is to boil off than another:

```text
K_i = y_i / x_i                        (distribution ratio)
alpha_12 = K_1 / K_2                    (relative volatility)

alpha near 1  -> hard to separate (needs many stages)
alpha large   -> easy separation
```

Real mixtures of dissimilar molecules (alcohol + water, for instance)
**deviate** from Raoult's law. We correct the liquid side with an
**activity coefficient** gamma from a model such as **Wilson, NRTL, or
UNIQUAC**:

```text
Modified Raoult's law (non-ideal liquid):

y_i * P = x_i * gamma_i * P_i_sat(T)

gamma_i = 1      ideal (Raoult recovered)
gamma_i > 1      positive deviation (can form a minimum-boiling azeotrope)
```

Strong deviations create **azeotropes** - compositions where vapor and
liquid are identical, so ordinary distillation cannot cross them (e.g.
ethanol-water at about 95.6 percent ethanol). Choosing the right gamma
model (NRTL, UNIQUAC) is the single most important thermodynamic decision
when you build a distillation model in Aspen or DWSIM.

```mermaid
graph LR
    T["Temperature"] --> PSAT["Antoine gives P sat"]
    PSAT --> RAOULT["Raoult y P equals x P sat"]
    RAOULT --> IDEALVLE["Ideal VLE and K values"]
    NONIDEAL["Dissimilar molecules"] --> GAMMA["Activity coefficient gamma"]
    GAMMA --> MODVLE["Modified Raoult and azeotropes"]
```

Remember: VLE links y to x; Raoult's law handles ideal mixtures, and an
**activity coefficient** from NRTL or UNIQUAC handles the real, non-ideal
ones - including the azeotropes that limit what distillation can do.
""",
        ),
        quiz_lesson(
            "Quiz: Vapor-liquid equilibrium (Raoult's law, activity coefficients)",
            (
                q(
                    "What does Raoult's law state for an ideal liquid mixture?",
                    (
                        opt("y_i * P = x_i * P_i_sat(T)", correct=True),
                        opt("The vapor and liquid always have identical composition"),
                        opt("Pressure is independent of composition"),
                        opt("Temperature has no effect on vapor pressure"),
                    ),
                    "Partial pressure of a species equals its liquid mole fraction times "
                    "its pure-component vapor pressure.",
                ),
                q(
                    "Why introduce an activity coefficient gamma?",
                    (
                        opt("To convert temperature to pressure"),
                        opt(
                            "To correct the liquid phase for non-ideal behavior when "
                            "molecules are dissimilar; gamma = 1 recovers Raoult's law",
                            correct=True,
                        ),
                        opt("To count the number of phases"),
                        opt("To measure viscosity"),
                    ),
                    "Modified Raoult's law y*P = x*gamma*P_sat; gamma from Wilson/NRTL/"
                    "UNIQUAC captures real-mixture deviations.",
                ),
                q(
                    "What is an azeotrope?",
                    (
                        opt("A pump used in distillation"),
                        opt(
                            "A composition where vapor and liquid have identical "
                            "composition, so ordinary distillation cannot separate past it",
                            correct=True,
                        ),
                        opt("A type of heat exchanger"),
                        opt("A reaction that never reaches equilibrium"),
                    ),
                    "Strong deviations create azeotropes (e.g. ethanol-water near 95.6 "
                    "percent) that simple distillation cannot cross.",
                ),
            ),
        ),
        # -- 7. Flash calculations -------------------------------------
        _t(
            "Flash calculations",
            "11 min",
            """# Flash calculations

A **flash** is the fundamental separation calculation: a feed at some T and
P is brought to a drum where it splits into equilibrium **vapor** and
**liquid** streams. Every distillation stage, separator, and flowsheet
convergence loop is built on it. The classic case is the **isothermal
flash** - given feed composition z, and the drum T and P, find the vapor
fraction and the two product compositions.

Three relations define it, using the **K-value** `K_i = y_i / x_i`:

```text
Component balance:   z_i = V * y_i + (1 - V) * x_i     (per mole of feed)
Equilibrium:         y_i = K_i * x_i
Summation:           sum(y_i) = 1,  sum(x_i) = 1

V = vapor fraction (moles vapor per mole feed), between 0 and 1
```

Combining them gives the compositions in terms of V and the K-values:

```text
x_i = z_i / (1 + V * (K_i - 1))
y_i = K_i * x_i
```

Substituting into sum(y_i) - sum(x_i) = 0 yields the **Rachford-Rice
equation**, solved for V (it has one physical root and behaves well
numerically):

```text
Rachford-Rice:

f(V) = sum_i  [ z_i * (K_i - 1) / (1 + V * (K_i - 1)) ] = 0

Solve for V in [0, 1] by Newton's method or bisection.
```

Before solving, **bracket** the state: compute the **bubble point**
(sum(K_i * z_i) = 1 means V just above 0, all liquid) and the **dew point**
(sum(z_i / K_i) = 1 means V just below 1, all vapor). If the feed is
between them, a two-phase flash exists.

```python
import numpy as np
from scipy.optimize import brentq

z = np.array([0.5, 0.3, 0.2])     # feed mole fractions
K = np.array([3.0, 1.0, 0.35])    # K-values at drum T and P

def rachford_rice(V):
    return np.sum(z * (K - 1.0) / (1.0 + V * (K - 1.0)))

V = brentq(rachford_rice, 0.0, 1.0)     # vapor fraction
x = z / (1.0 + V * (K - 1.0))           # liquid composition
y = K * x                                # vapor composition
```

```mermaid
graph LR
    FEED["Feed z at T and P"] --> DRUM["Flash drum"]
    DRUM --> RR["Solve Rachford Rice for V"]
    RR --> XL["Liquid composition x"]
    RR --> YV["Vapor composition y"]
    XL --> LIQ["Liquid product"]
    YV --> VAP["Vapor product"]
```

Remember: a flash splits a feed into equilibrium vapor and liquid; the
**Rachford-Rice** equation solves for the vapor fraction, and every column
stage is essentially a flash repeated.
""",
        ),
        quiz_lesson(
            "Quiz: Flash calculations",
            (
                q(
                    "What does an isothermal flash calculation determine?",
                    (
                        opt("The reaction rate of a mixture"),
                        opt(
                            "How a feed splits into equilibrium vapor and liquid at a "
                            "given T and P - the vapor fraction and both compositions",
                            correct=True,
                        ),
                        opt("The viscosity of a liquid"),
                        opt("The heat capacity of a gas"),
                    ),
                    "Given feed z and drum T and P, find V and the equilibrium x and y.",
                ),
                q(
                    "The Rachford-Rice equation is solved for what variable?",
                    (
                        opt("The temperature of the feed"),
                        opt("The number of components"),
                        opt(
                            "The vapor fraction V (moles vapor per mole feed), between 0 and 1",
                            correct=True,
                        ),
                        opt("The molecular weight"),
                    ),
                    "Rachford-Rice packages the component balances, equilibrium, and "
                    "summation into one well-behaved equation in V.",
                ),
                q(
                    "How do you know a two-phase flash actually exists for a feed?",
                    (
                        opt("It always exists for any T and P"),
                        opt(
                            "The feed lies between its bubble point (V near 0) and its "
                            "dew point (V near 1)",
                            correct=True,
                        ),
                        opt("Only if the feed is a pure component"),
                        opt("Only above the critical pressure"),
                    ),
                    "Check bubble point sum(K*z)=1 and dew point sum(z/K)=1; between them "
                    "a two-phase solution with 0 < V < 1 exists.",
                ),
            ),
        ),
        # -- 8. Chemical reaction equilibrium --------------------------
        _t(
            "Chemical reaction equilibrium",
            "12 min",
            """# Chemical reaction equilibrium

Kinetics tells you how *fast* a reaction goes; **thermodynamics** tells you
how *far* it can go before it stops at **equilibrium**. A reactor design
starts with the equilibrium limit, then kinetics decides whether you can
reach it in a reasonable size.

Equilibrium is set by the **standard Gibbs energy change of reaction**,
`delta G0`, through the **equilibrium constant** K:

```text
delta G0(T) = -RT * ln(K)

K = exp( -delta G0 / (RT) )

delta G0 < 0  ->  K > 1   equilibrium favors products
delta G0 > 0  ->  K < 1   equilibrium favors reactants
```

K links to **activities** (for gases, fugacities; near-ideal, partial
pressures). For a general reaction with stoichiometric coefficients nu_i
(positive for products, negative for reactants):

```text
K = product_i ( a_i ^ nu_i )

For ideal gases:   K = product_i ( (P_i / P_ref) ^ nu_i )
```

Temperature dependence follows the **van 't Hoff equation** - and this is
where Le Chatelier's principle becomes quantitative:

```text
van 't Hoff:

d(ln K) / dT = delta H0 / (R * T^2)

delta H0 < 0 (exothermic):  K falls as T rises  -> heat up hurts conversion
delta H0 > 0 (endothermic): K rises as T rises  -> heat helps conversion
```

That is why **ammonia synthesis** (exothermic) runs at only moderate
temperature but very high pressure: raising T lowers K, but raising P shifts
the mole-reducing reaction toward product. To find the actual composition,
introduce the **extent of reaction** xi, write every mole number as
`n_i = n_i0 + nu_i * xi`, and solve the K expression for xi.

```mermaid
graph TD
    DG["Standard Gibbs energy delta G0"] --> K["Equilibrium constant K"]
    K --> POS["K greater than 1 favors products"]
    K --> NEG["K less than 1 favors reactants"]
    TEMP["Temperature change"] --> VH["van t Hoff shifts K"]
    PRES["Pressure and moles"] --> LC["Le Chatelier shift"]
    K --> XI["Solve extent of reaction xi"]
    XI --> COMP["Equilibrium composition"]
```

Remember: `delta G0 = -RT ln K` fixes the equilibrium constant, **van 't
Hoff** tells you how K moves with temperature, and solving for the **extent
of reaction** gives the equilibrium composition your reactor design targets.
""",
        ),
        quiz_lesson(
            "Quiz: Chemical reaction equilibrium",
            (
                q(
                    "How is the equilibrium constant K related to the standard Gibbs "
                    "energy change of reaction?",
                    (
                        opt("K = delta G0 * RT"),
                        opt(
                            "delta G0 = -RT * ln(K), so K = exp(-delta G0 / (RT))",
                            correct=True,
                        ),
                        opt("K is independent of delta G0"),
                        opt("K = delta G0 / R"),
                    ),
                    "A negative delta G0 gives K > 1 and product-favored equilibrium; "
                    "positive gives K < 1.",
                ),
                q(
                    "For an exothermic reaction (delta H0 < 0), what does the van 't Hoff "
                    "equation predict as temperature rises?",
                    (
                        opt("K increases, favoring more product"),
                        opt(
                            "K decreases, so higher temperature reduces equilibrium conversion",
                            correct=True,
                        ),
                        opt("K is unchanged by temperature"),
                        opt("The reaction reverses direction permanently"),
                    ),
                    "d(ln K)/dT = delta H0/(R T^2); with delta H0 negative, K falls as T "
                    "rises - the quantitative Le Chatelier result.",
                ),
                q(
                    "What does thermodynamic reaction equilibrium tell a reactor "
                    "designer, versus kinetics?",
                    (
                        opt(
                            "Thermodynamics gives the reaction speed; kinetics gives the "
                            "maximum conversion"
                        ),
                        opt(
                            "Thermodynamics sets how far the reaction can go (the "
                            "equilibrium limit); kinetics sets how fast it gets there",
                            correct=True,
                        ),
                        opt("They give identical information"),
                        opt("Neither is relevant to reactor design"),
                    ),
                    "Equilibrium is the ceiling on conversion; kinetics decides whether a "
                    "practical reactor size can approach it.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does the compressibility factor Z equal for an ideal gas, and "
                    "what does it capture for a real fluid?",
                    (
                        opt("Z = 0 for an ideal gas; it captures mass"),
                        opt(
                            "Z = 1 for an ideal gas; Z = PV/(RT) measures deviation from "
                            "ideal behavior for a real fluid",
                            correct=True,
                        ),
                        opt("Z = 100; it measures temperature"),
                        opt("Z has no physical meaning"),
                    ),
                    "Z = PV/(RT) = 1 ideal; below 1 attraction dominates, above 1 "
                    "repulsion dominates - a cubic EOS predicts it.",
                ),
                q(
                    "Which equations of state are the workhorses in modern process "
                    "simulators for hydrocarbons?",
                    (
                        opt("Ideal gas and Newton's law only"),
                        opt(
                            "Cubic equations of state such as Soave-Redlich-Kwong and "
                            "Peng-Robinson",
                            correct=True,
                        ),
                        opt("The Antoine equation only"),
                        opt("The Arrhenius equation"),
                    ),
                    "SRK and PR add attractive and repulsive terms using Tc, Pc, and the "
                    "acentric factor.",
                ),
                q(
                    "Why is the steady-flow energy balance written in enthalpy?",
                    (
                        opt("Enthalpy is easier to type"),
                        opt(
                            "A flowing stream does flow work PV crossing the boundary, "
                            "and H = U + PV includes it; at steady state Q - Ws = dH",
                            correct=True,
                        ),
                        opt("Internal energy does not exist for gases"),
                        opt("Because enthalpy is always constant"),
                    ),
                    "Flow work plus internal energy is enthalpy, the natural currency for "
                    "open-system balances.",
                ),
                q(
                    "The Gouy-Stodola relation W_lost = T0 * S_gen expresses what idea?",
                    (
                        opt("Energy is destroyed in real processes"),
                        opt(
                            "Entropy generation from irreversibility destroys available "
                            "work equal to T0 times S_gen",
                            correct=True,
                        ),
                        opt("Entropy generation can be negative"),
                        opt("Work equals heat always"),
                    ),
                    "Energy is conserved, but its quality (exergy) is destroyed; lost "
                    "work is T0 * S_gen.",
                ),
                q(
                    "How does a simulator obtain the real enthalpy or entropy of a fluid?",
                    (
                        opt("It assumes the ideal-gas value everywhere"),
                        opt(
                            "Ideal-gas value from Cp plus a departure function computed "
                            "from the equation of state",
                            correct=True,
                        ),
                        opt("It ignores temperature effects"),
                        opt("It uses only the molecular weight"),
                    ),
                    "Real property = ideal-gas property + EOS departure; fugacity plays "
                    "the same role for equilibrium.",
                ),
                q(
                    "What is the Gibbs phase rule, and what does F count?",
                    (
                        opt("F = C + P + 2; it counts atoms"),
                        opt(
                            "F = C - P + 2; F is the number of intensive variables you "
                            "can independently fix",
                            correct=True,
                        ),
                        opt("F = P - C; it counts phases only"),
                        opt("F = 2 always"),
                    ),
                    "Degrees of freedom = components minus phases plus 2; e.g. a pure "
                    "substance triple point has F = 0.",
                ),
                q(
                    "In modified Raoult's law y*P = x*gamma*P_sat, what is gamma?",
                    (
                        opt("The total pressure"),
                        opt(
                            "The activity coefficient correcting the liquid for "
                            "non-ideality; gamma = 1 recovers ideal Raoult's law",
                            correct=True,
                        ),
                        opt("The vapor fraction"),
                        opt("The equilibrium constant"),
                    ),
                    "gamma from Wilson, NRTL, or UNIQUAC handles dissimilar molecules and "
                    "predicts azeotropes.",
                ),
                q(
                    "The Rachford-Rice equation in a flash calculation solves for what?",
                    (
                        opt("The reactor volume"),
                        opt("The reaction rate"),
                        opt(
                            "The vapor fraction V, from which the equilibrium liquid and "
                            "vapor compositions follow",
                            correct=True,
                        ),
                        opt("The Antoine constants"),
                    ),
                    "It combines component balances, K-value equilibrium, and summation "
                    "into one equation in V.",
                ),
                q(
                    "What relates the equilibrium constant K to the standard Gibbs energy "
                    "change of reaction?",
                    (
                        opt("K = delta H0 / T"),
                        opt(
                            "delta G0 = -RT * ln(K), so a negative delta G0 gives K > 1 "
                            "and product-favored equilibrium",
                            correct=True,
                        ),
                        opt("K equals the reaction rate constant"),
                        opt("K is fixed at 1 for all reactions"),
                    ),
                    "delta G0 = -RT ln K sets the equilibrium; van 't Hoff gives its "
                    "temperature dependence.",
                ),
                q(
                    "For an exothermic reaction, what does raising the temperature do to "
                    "the equilibrium conversion, per van 't Hoff?",
                    (
                        opt("It increases conversion"),
                        opt(
                            "It decreases the equilibrium constant K and therefore the "
                            "maximum conversion",
                            correct=True,
                        ),
                        opt("It has no effect"),
                        opt("It changes the stoichiometry"),
                    ),
                    "d(ln K)/dT = delta H0/(R T^2); with delta H0 < 0, K falls as T rises "
                    "- why ammonia synthesis leans on pressure, not high temperature.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

CHEMICAL_ENGINEERING_THERMODYNAMICS_COURSES: tuple[SeedCourse, ...] = (
    _CHEMICAL_ENGINEERING_THERMODYNAMICS,
)
