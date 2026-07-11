"""Academy seed content - Mass Transfer and Separation Processes.

How species move through phases and how mixtures are pulled apart. The
course builds from molecular diffusion and Fick's law, through convective
transfer coefficients and two-film interphase theory, into the workhorse
separations of the chemical industry: gas absorption and stripping,
distillation by McCabe-Thiele, liquid-liquid extraction, and membranes.
It closes with the dimensionless groups (Sherwood, Schmidt) and the
transport analogies that let one measurement predict another. Every
lesson is a direct explanation with a worked equation or calculation and
a mermaid diagram, followed by a checkpoint quiz; a comprehensive final
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


_MASS_TRANSFER_SEPARATIONS = SeedCourse(
    slug="mass-transfer-separations",
    title="Mass Transfer & Separation Processes",
    description=(
        "How species move and how mixtures are separated - diffusion, "
        "interphase transfer, and the workhorse separations of absorption, "
        "distillation, extraction and membranes. Each lesson pairs a direct "
        "explanation and a mermaid diagram with a worked design equation or "
        "a Python calculation grounded in real practice (McCabe-Thiele, "
        "Antoine, HTU-NTU, Sherwood and Schmidt numbers)."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Mass Transfer and Separation Processes

Almost nothing useful comes out of a reactor pure. Crude oil, fermentation
broth, reformer gas, produced water - the value is in a mixture, and a
**separation** is what turns that mixture into products. Behind every
separation is one physical fact: **species move from where their chemical
potential is high to where it is low**. Learn how that movement works and
the whole toolbox of separations starts to make sense.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a worked equation or a short calculation, and draws
it as a diagram. After each lesson there is a short quiz; at the end, a
final quiz spans the whole course.

What you will build understanding for, in order:

1. **Molecular diffusion and Fick's law** - the microscopic driving force
2. **Convective mass transfer and coefficients** - transfer at a surface
3. **Interphase mass transfer and two-film theory** - crossing between phases
4. **Gas absorption and stripping** - scrubbing a gas with a liquid
5. **Distillation fundamentals** - McCabe-Thiele and vapor-liquid equilibrium
6. **Liquid-liquid extraction** - separating with a second solvent
7. **Membrane separations** - a barrier that plays favorites
8. **Dimensionless groups and analogies** - Sherwood, Schmidt, and shortcuts

The thread running through all of it: a **driving force** (a concentration
or activity difference) divided by a **resistance** gives a **flux**. Change
the phase, the geometry, or the barrier and the details change - but that
flux idea, and the equilibrium line it chases, never leaves.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What single physical idea underlies every separation in this course?",
                    (
                        opt("Species are created and destroyed to balance a mixture"),
                        opt(
                            "Species move from high to low chemical potential, driven by "
                            "a concentration or activity difference",
                            correct=True,
                        ),
                        opt("Heat always flows faster than mass"),
                        opt("Every mixture separates itself given enough time at rest"),
                    ),
                    "A driving force (difference in potential) over a resistance gives a "
                    "flux - the recurring theme of the course.",
                ),
                q(
                    "How is each lesson structured?",
                    (
                        opt("Pure theory with no examples"),
                        opt(
                            "A direct explanation, a worked equation or calculation, and "
                            "a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only a quiz, with no reading"),
                        opt("A video lecture with no text"),
                    ),
                    "Explain one idea, show it concretely, draw it, then check understanding.",
                ),
            ),
        ),
        # -- 1. Molecular diffusion and Fick's law ---------------------
        _t(
            "Molecular diffusion and Fick's law",
            "10 min",
            """# Molecular diffusion and Fick's law

**Molecular diffusion** is the net movement of a species caused by its own
random molecular motion, from a region of high concentration to low. No
stirring, no bulk flow - just the statistics of many molecules wandering.
Given a concentration gradient, more molecules step down the hill than up
it, and a **net flux** results.

**Fick's first law** puts a number on it. In one dimension, the molar flux
of species A relative to the mixture is proportional to its concentration
gradient:

```text
J_A = -D_AB * (dC_A / dz)

  J_A   = molar flux of A            [mol / (m^2 . s)]
  D_AB  = diffusion coefficient of A in B   [m^2 / s]
  dC_A/dz = concentration gradient of A     [mol / m^3 / m]

The minus sign: flux points DOWN the gradient (high to low).
```

The **diffusion coefficient** D_AB (or diffusivity) is the material
property that sets the pace. Order-of-magnitude values are worth
memorizing because they explain a lot:

- Gases:   D roughly 1e-5 m^2/s   (fast - molecules are far apart)
- Liquids: D roughly 1e-9 m^2/s   (about 10,000x slower)
- Solids:  D roughly 1e-12 m^2/s or less (glacial)

For gases the **Chapman-Enskog** theory predicts D_AB rising with
temperature (about T^1.5 to T^1.75) and falling with pressure. For liquids
the **Stokes-Einstein** relation ties D to temperature over viscosity.

A worked estimate - how far does a molecule diffuse in time t? The
characteristic distance scales as the square root of D times t:

```text
Liquid, D = 1e-9 m^2/s, over t = 100 s:
  x ~ sqrt(D . t) = sqrt(1e-9 * 100) = sqrt(1e-7) = 3.2e-4 m = 0.32 mm

Diffusion alone moves things a fraction of a millimeter in a minute or
two - which is exactly why real equipment relies on convection, not just
molecular diffusion, to move mass over useful distances.
```

```mermaid
graph LR
    HI["High concentration region"] --> GRAD["Concentration gradient"]
    GRAD --> RANDOM["Random molecular motion"]
    RANDOM --> NET["Net flux down the gradient"]
    NET --> LO["Low concentration region"]
    DAB["Diffusivity D sets the pace"] --> NET
```

Remember: Fick's law says flux equals diffusivity times the gradient,
pointing downhill - and molecular diffusion alone is slow, which motivates
everything that follows.
""",
        ),
        quiz_lesson(
            "Quiz: Molecular diffusion and Fick's law",
            (
                q(
                    "What does Fick's first law state?",
                    (
                        opt("Flux is proportional to temperature only"),
                        opt(
                            "Molar flux is proportional to the concentration gradient, "
                            "with diffusivity as the constant and a minus sign for the "
                            "downhill direction",
                            correct=True,
                        ),
                        opt("Flux is independent of concentration"),
                        opt("Flux points up the concentration gradient"),
                    ),
                    "J_A = -D_AB (dC_A/dz): diffusivity times gradient, directed from high to low.",
                ),
                q(
                    "Roughly how do gas, liquid and solid diffusivities compare?",
                    (
                        opt("They are all about the same"),
                        opt(
                            "Gases near 1e-5, liquids near 1e-9, solids near 1e-12 m^2/s "
                            "- each phase is orders of magnitude slower than the last",
                            correct=True,
                        ),
                        opt("Solids diffuse fastest"),
                        opt("Liquids diffuse faster than gases"),
                    ),
                    "About 1e-5 (gas), 1e-9 (liquid), 1e-12 (solid) m^2/s - a huge range "
                    "that shapes equipment design: liquid processes need far more "
                    "interfacial area than gas ones.",
                ),
                q(
                    "Why does real separation equipment rely on convection rather than "
                    "molecular diffusion alone?",
                    (
                        opt("Convection is cheaper to buy"),
                        opt(
                            "Molecular diffusion moves mass only a fraction of a "
                            "millimeter in a minute; convection is needed to move mass "
                            "over useful distances",
                            correct=True,
                        ),
                        opt("Diffusion violates the second law"),
                        opt("Convection needs no driving force"),
                    ),
                    "The sqrt(D.t) estimate shows diffusion is slow over macroscopic "
                    "distances, so bulk flow does the long-range transport.",
                ),
            ),
        ),
        # -- 2. Convective mass transfer and coefficients --------------
        _t(
            "Convective mass transfer and coefficients",
            "10 min",
            """# Convective mass transfer and coefficients

When a fluid flows past a surface, mass transfer between the surface and
the bulk fluid is **convective**: bulk motion sweeps species toward and
away from a thin **boundary layer** near the wall, and molecular diffusion
carries them across that last thin film. Rather than solve the full
gradient, engineers lump it into a **mass transfer coefficient**.

The rate law looks just like Newton's law of cooling, but for mass:

```text
N_A = k_c * (C_A,s - C_A,bulk)

  N_A     = molar flux of A            [mol / (m^2 . s)]
  k_c     = convective mass transfer coefficient  [m / s]
  C_A,s   = concentration at the surface   [mol / m^3]
  C_A,bulk = concentration in the bulk fluid [mol / m^3]
```

The coefficient **k_c** bundles the messy boundary-layer physics into one
number. It grows with velocity, with diffusivity, and with anything that
thins the boundary layer (turbulence, small tubes). We rarely derive k_c;
we **correlate** it through the Sherwood number (covered later), which is
the dimensionless form of k_c.

The total rate scales with area, so real contactors maximize interfacial
area A per unit volume:

```text
Total molar transfer rate:
  W_A = k_c * A * (C_A,s - C_A,bulk)     [mol / s]

For a packed or sprayed contactor the area is huge and hard to measure, so
designers use a VOLUMETRIC coefficient k_c . a, where 'a' is interfacial
area per unit volume [m^2 / m^3], and work with (k_c . a) as one lumped
group.
```

A quick calculation of the transfer rate at a wetted wall:

```python
# Wall dissolving into a flowing liquid
kc = 2.0e-5          # m/s, convective mass transfer coefficient
A = 0.50             # m^2, contact area
Cs = 30.0            # mol/m^3, saturation at the surface
Cb = 5.0             # mol/m^3, bulk concentration
W = kc * A * (Cs - Cb)
print(W)             # 2.5e-4 mol/s  -> raise kc (velocity) or A to speed it
```

```mermaid
graph LR
    BULK["Flowing bulk fluid"] --> BL["Thin boundary layer"]
    BL --> SURF["Surface concentration"]
    KC["Coefficient k_c lumps the physics"] --> RATE["N equals k_c times driving force"]
    SURF --> RATE
    RATE --> AREA["Total rate scales with area"]
```

Remember: convective transfer packages the boundary layer into a
coefficient k_c, the flux is k_c times a concentration difference, and the
total rate is k_c times area times that difference - so more area and more
velocity mean more separation.
""",
        ),
        quiz_lesson(
            "Quiz: Convective mass transfer and coefficients",
            (
                q(
                    "What does a convective mass transfer coefficient k_c represent?",
                    (
                        opt("The diffusivity of the species"),
                        opt(
                            "A lumped number capturing boundary-layer transfer, so flux "
                            "equals k_c times a concentration difference",
                            correct=True,
                        ),
                        opt("The equilibrium constant of the mixture"),
                        opt("The total pressure of the system"),
                    ),
                    "k_c bundles the boundary-layer physics; N_A = k_c (C_s - C_bulk), "
                    "analogous to Newton's law of cooling.",
                ),
                q(
                    "Why do packed and sprayed contactors use a volumetric coefficient k_c . a?",
                    (
                        opt("Because area does not matter in these devices"),
                        opt(
                            "The interfacial area is large and hard to measure, so k_c "
                            "and the area per volume 'a' are lumped into one group",
                            correct=True,
                        ),
                        opt("To avoid using diffusivity"),
                        opt("Because k_c is zero in packing"),
                    ),
                    "In real contactors 'a' (m^2/m^3) is uncertain, so designers "
                    "correlate the product k_c . a directly.",
                ),
                q(
                    "How can you increase the total convective transfer rate W_A?",
                    (
                        opt("Reduce the interfacial area"),
                        opt("Lower the fluid velocity"),
                        opt(
                            "Increase k_c (more velocity or turbulence), the interfacial "
                            "area, or the concentration driving force",
                            correct=True,
                        ),
                        opt("Bring the phases to equilibrium"),
                    ),
                    "W_A = k_c . A . (C_s - C_bulk); each factor is a lever, and "
                    "equilibrium would zero the driving force.",
                ),
            ),
        ),
        # -- 3. Interphase mass transfer and two-film theory -----------
        _t(
            "Interphase mass transfer and two-film theory",
            "11 min",
            """# Interphase mass transfer and two-film theory

Most separations move a species **across a phase boundary** - a solute out
of a gas into a liquid, out of one liquid into another. The **two-film
theory** (Whitman) is the classic, workable picture: on each side of the
interface sits a stagnant **film** in which all the resistance lives, and
**at the interface the two phases are in equilibrium**.

So the journey has two resistances in series: diffuse through the gas film,
then diffuse through the liquid film. At the interface, the gas- and
liquid-side compositions are linked by an equilibrium relation - often
**Henry's law**, p_A = H . x_A.

Because interface compositions are hard to measure, we combine both films
into an **overall coefficient** driven by an easily computed difference: the
bulk composition versus the composition that *would* be in equilibrium with
the other bulk phase (the star, `*`, state):

```text
Flux, gas-side overall form:
  N_A = K_y * (y_A - y_A*)      y_A* = value in equilibrium with x_A,bulk

Resistances add in series (like resistors). With m the slope of the
equilibrium line (y = m x):

  1 / K_y  =  1 / k_y  +  m / k_x
  \\_____/     \\____/     \\____/
   overall      gas       liquid
                film       film
```

Which film controls? Compare the terms:

- **Gas-film control** - when m is small (very soluble gas, e.g. ammonia in
  water); the 1/k_y term dominates. Speed it up by improving the gas side.
- **Liquid-film control** - when m is large (sparingly soluble gas, e.g.
  oxygen or CO2 in water); the m/k_x term dominates. Improve the liquid side.

A worked split of the resistance:

```text
Given: k_y = 0.010, k_x = 0.020 (mol/m^2.s), equilibrium slope m = 2.0
  1/K_y = 1/0.010 + 2.0/0.020 = 100 + 100 = 200
  Gas-film share  = 100/200 = 50 percent
  Liquid-film share = 100/200 = 50 percent
Raise m to 20 and the liquid film holds 91 percent of the resistance -
so a sparingly soluble gas is liquid-film controlled.
```

```mermaid
graph LR
    GB["Gas bulk y"] --> GF["Gas film resistance"]
    GF --> INT["Interface at equilibrium"]
    INT --> LF["Liquid film resistance"]
    LF --> LB["Liquid bulk x"]
    SLOPE["Equilibrium slope m sets the split"] --> INT
```

Remember: transfer between phases is two film resistances in series with
equilibrium at the interface; roll them into an overall K, and the slope of
the equilibrium line tells you which side to improve.
""",
        ),
        quiz_lesson(
            "Quiz: Interphase mass transfer and two-film theory",
            (
                q(
                    "What are the core assumptions of two-film theory?",
                    (
                        opt("There is no interface between the phases"),
                        opt(
                            "All resistance sits in a stagnant film on each side, and "
                            "the two phases are in equilibrium at the interface",
                            correct=True,
                        ),
                        opt("Only the gas phase has any resistance"),
                        opt("Equilibrium is reached in the bulk, not the interface"),
                    ),
                    "Two stagnant films carry all the resistance; the interface itself "
                    "is at equilibrium.",
                ),
                q(
                    "Why introduce an overall coefficient like K_y with a y_A* driving force?",
                    (
                        opt("Because k_y and k_x are always equal"),
                        opt(
                            "Interface compositions are hard to measure, so the two film "
                            "resistances are combined and driven by the bulk versus its "
                            "equilibrium value",
                            correct=True,
                        ),
                        opt("To ignore the liquid film entirely"),
                        opt("Because equilibrium does not apply"),
                    ),
                    "1/K_y = 1/k_y + m/k_x lets us use measurable bulk compositions and "
                    "the star state.",
                ),
                q(
                    "A sparingly soluble gas (large equilibrium slope m, like CO2 in "
                    "water) is usually controlled by which film?",
                    (
                        opt("The gas film"),
                        opt("The liquid film - the m/k_x term dominates", correct=True),
                        opt("Neither film - it is instantaneous"),
                        opt("Both films equally, always"),
                    ),
                    "Large m makes m/k_x dominate the resistance sum, so improving the "
                    "liquid side speeds transfer. Small m (very soluble, e.g. ammonia) "
                    "is gas-film controlled instead.",
                ),
            ),
        ),
        # -- 4. Gas absorption and stripping ---------------------------
        _t(
            "Gas absorption and stripping",
            "11 min",
            """# Gas absorption and stripping

**Absorption** contacts a gas with a liquid **solvent** that preferentially
dissolves one component - scrubbing CO2 or H2S from natural gas with an
amine, or SO2 from a flue gas with water. **Stripping** is the reverse:
contacting a loaded liquid with a gas (steam, air, inert) to pull the
solute back out and regenerate the solvent. They are the same equipment
and math run in opposite directions.

The workhorse device is a **packed column**: liquid flows down over packing
(random rings or structured sheets from vendors like Sulzer or Koch), gas
flows up, and they meet **countercurrently** across a large wetted area.
Countercurrent flow keeps a driving force at both ends, which is why it
beats co-current.

A **mass balance** on the column gives the **operating line** - the
relation between the liquid composition x and the gas composition y at any
height. On dilute x-y coordinates it is a straight line of slope L/G:

```text
Operating line (solute balance around the top of an absorber):
  G(y - y_top) = L(x - x_top)   ->   y = (L/G) x + constant

  G = gas molar flow (solute-free basis)
  L = liquid molar flow (solute-free basis)
  L/G = slope of the operating line

Absorption: operating line lies ABOVE the equilibrium line (gas gives up
solute to liquid). Stripping: it lies BELOW.
```

The **minimum solvent rate** and column height come from how far the
operating line sits from the equilibrium line - the gap is the driving
force. Height is sized with the **HTU-NTU** method:

```text
Packed height:
  Z = HTU * NTU

  HTU = height of a transfer unit = G / (K_y . a . S)   [m]   (efficiency)
  NTU = number of transfer units  = integral of dy/(y - y*)  (difficulty)

For a dilute system with a straight, dilute-limit equilibrium line:
  NTU ~ ln[(y_in - y*)/(y_out - y*)]     more separation -> larger NTU
```

A quick solvent-rate check:

```python
# Absorb solute from gas: pick liquid rate above the minimum
G = 100.0            # mol/s gas (solute-free)
y_in, y_out = 0.02, 0.001      # mole fractions in and out
m = 0.8              # equilibrium slope y = m x, lean solvent x_in ~ 0
Lmin = G * (y_in - y_out) / (y_in / m - 0.0)   # simplest dilute estimate
L = 1.5 * Lmin       # operate at ~1.5x minimum (rule of thumb)
print(round(Lmin, 1), round(L, 1))   # design above Lmin for a finite column
```

```mermaid
graph TD
    GIN["Gas in solute rich"] --> COL["Packed column countercurrent"]
    LIN["Lean solvent in at top"] --> COL
    COL --> GOUT["Clean gas out at top"]
    COL --> LOUT["Loaded solvent out at bottom"]
    LOUT --> STRIP["Stripper regenerates solvent"]
    STRIP --> LIN
```

Remember: absorption moves solute gas-to-liquid, stripping reverses it; a
countercurrent packed column with an operating line of slope L/G does the
work, and height equals HTU times NTU.
""",
        ),
        quiz_lesson(
            "Quiz: Gas absorption and stripping",
            (
                q(
                    "How do absorption and stripping relate?",
                    (
                        opt("They are unrelated processes"),
                        opt(
                            "Stripping is the reverse of absorption - the same "
                            "equipment and math run to move solute out of the liquid "
                            "instead of into it",
                            correct=True,
                        ),
                        opt("Both add solute to the gas phase"),
                        opt("Stripping only works for solids"),
                    ),
                    "Absorption: gas to liquid. Stripping: liquid to gas, to regenerate "
                    "the solvent.",
                ),
                q(
                    "What is the slope of the operating line in a dilute absorber or stripper?",
                    (
                        opt("The equilibrium constant m"),
                        opt("The ratio L/G of liquid to gas molar flows", correct=True),
                        opt("Always exactly 1.0"),
                        opt("The column height Z"),
                    ),
                    "A solute mass balance gives y = (L/G)x + constant; the slope is "
                    "the liquid-to-gas flow ratio.",
                ),
                q(
                    "In the HTU-NTU method, what do HTU and NTU represent?",
                    (
                        opt("Both are just the column diameter"),
                        opt(
                            "HTU is the height of one transfer unit (contactor "
                            "efficiency); NTU is the number of transfer units (how hard "
                            "the separation is); Z = HTU . NTU",
                            correct=True,
                        ),
                        opt("HTU is the number of trays, NTU the reflux ratio"),
                        opt("They are the same quantity with different units"),
                    ),
                    "Height = HTU (efficiency, from k_y.a) times NTU (difficulty, from "
                    "the integral of dy/(y - y*)).",
                ),
            ),
        ),
        # -- 5. Distillation fundamentals (McCabe-Thiele) --------------
        _t(
            "Distillation fundamentals (McCabe-Thiele)",
            "12 min",
            """# Distillation fundamentals (McCabe-Thiele)

**Distillation** separates liquids by their **volatility difference**: boil
the mixture, and the vapor is richer in the more-volatile component. Do
this over and over up a column of trays and you concentrate the light
component at the top (**distillate**) and the heavy at the bottom
(**bottoms**). It is by far the most common industrial separation.

The equilibrium behind it is **vapor-liquid equilibrium (VLE)**. For an
ideal binary, **relative volatility** alpha captures how easy the split is:

```text
Relative volatility:
  alpha = (y_A / x_A) / (y_B / x_B)

VLE curve (constant alpha, ideal case):
  y_A = alpha x_A / (1 + (alpha - 1) x_A)

alpha = 1 means no separation (an azeotrope-like pinch); larger alpha means
an easier separation and fewer stages. Antoine equation vapor pressures
feed the K-values that give alpha.
```

The **McCabe-Thiele method** is the classic graphical design for a binary
column. Plot y vs x, draw the equilibrium curve, then draw two **operating
lines** from mass balances - one for the section above the feed (rectifying)
and one below (stripping) - plus a **q-line** for the feed condition. Step
off stairs between the operating line and the equilibrium curve; each step
is one **theoretical stage**.

```text
Rectifying operating line (above the feed), with reflux ratio R = L/D:
  y = (R / (R + 1)) x + x_D / (R + 1)

  R      = reflux ratio (returned liquid / distillate)
  x_D    = distillate composition
  Higher R -> operating line nearer the 45 degree line -> fewer stages but
  more energy. There is a trade-off between stages (capital) and reflux
  (energy). Minimum reflux R_min gives infinite stages; total reflux gives
  the minimum stages.
```

A quick stage-count feel using the Fenske equation at total reflux:

```python
import math
alpha = 2.5          # relative volatility (light/heavy)
xD = 0.95            # distillate light-key mole fraction
xB = 0.05            # bottoms light-key mole fraction
# Fenske minimum number of stages at total reflux:
num = math.log((xD/(1-xD)) * ((1-xB)/xB))
Nmin = num / math.log(alpha)
print(round(Nmin, 1))   # ~6.4 -> real column needs more, at finite reflux
```

```mermaid
graph TD
    FEED["Feed enters mid column"] --> RECT["Rectifying section above feed"]
    FEED --> STRIP["Stripping section below feed"]
    RECT --> COND["Condenser and reflux R"]
    COND --> DIST["Distillate light rich"]
    STRIP --> REB["Reboiler adds heat"]
    REB --> BOTT["Bottoms heavy rich"]
```

Remember: distillation exploits relative volatility; McCabe-Thiele steps
stages between the equilibrium curve and the operating lines, and reflux
ratio trades stages (capital) against energy.
""",
        ),
        quiz_lesson(
            "Quiz: Distillation fundamentals (McCabe-Thiele)",
            (
                q(
                    "What property does distillation exploit to separate a mixture?",
                    (
                        opt("Differences in density only"),
                        opt(
                            "Differences in volatility - vapor is richer in the "
                            "more-volatile component",
                            correct=True,
                        ),
                        opt("Differences in electrical charge"),
                        opt("Differences in molecular color"),
                    ),
                    "Boil the mix; the more-volatile species concentrates in the vapor. "
                    "Relative volatility alpha measures how easy the split is.",
                ),
                q(
                    "In McCabe-Thiele, what does each step between the operating line "
                    "and the equilibrium curve represent?",
                    (
                        opt("One meter of column height"),
                        opt("One theoretical (equilibrium) stage", correct=True),
                        opt("One degree of temperature change"),
                        opt("One unit of reflux ratio"),
                    ),
                    "Each stair is a theoretical stage; count them to size the column "
                    "(real trays via a stage efficiency).",
                ),
                q(
                    "What is the trade-off set by the reflux ratio R?",
                    (
                        opt("More reflux always means both fewer stages and less energy"),
                        opt(
                            "Higher R needs fewer stages (less capital) but more reboiler "
                            "energy; lower R needs more stages but less energy",
                            correct=True,
                        ),
                        opt("Reflux ratio has no effect on stage count"),
                        opt("Minimum reflux gives the minimum number of stages"),
                    ),
                    "R_min gives infinite stages; total reflux gives minimum stages "
                    "(Fenske). Real columns sit between, balancing capital and energy - "
                    "the central economic decision in column design.",
                ),
            ),
        ),
        # -- 6. Liquid-liquid extraction -------------------------------
        _t(
            "Liquid-liquid extraction",
            "11 min",
            """# Liquid-liquid extraction

Some mixtures cannot be distilled cheaply - the components are heat-sensitive,
close-boiling, or form an azeotrope. **Liquid-liquid extraction (LLE)** offers
another route: add a second, **immiscible solvent** that preferentially
dissolves the target solute, let the two liquid phases separate by density,
and draw off the solute-rich solvent (the **extract**), leaving the depleted
feed (the **raffinate**). Penicillin recovery, aromatics from reformate, and
metal recovery all use it.

The key property is the **distribution (partition) coefficient** - how the
solute splits between the two phases at equilibrium:

```text
Distribution coefficient:
  K_D = (concentration of solute in extract) / (concentration in raffinate)
      = y / x   at equilibrium

A large K_D means the solvent grabs the solute strongly - a good, selective
solvent. Selectivity (relative to the carrier) must also be high, or you
extract the wrong thing too.
```

Doing it in **stages** multiplies the effect. A single mixer-settler gives
one equilibrium stage; a countercurrent cascade (or a rotating-disc or
packed extraction column) stacks many, so fresh solvent always meets the
most-depleted feed - the same countercurrent advantage as absorption.

A worked single-stage extraction:

```text
Single equilibrium stage, dilute solute:
  Feed: F = 100 kg/s carrier, solute fraction x_F = 0.10
  Solvent: S = 100 kg/s, solute-free
  Distribution: K_D = y/x = 4.0

  Extraction factor: E = K_D . (S/F) = 4.0 * (100/100) = 4.0
  Fraction remaining in raffinate = 1/(1 + E) = 1/5 = 0.20
  So one stage removes 80 percent of the solute; a countercurrent cascade
  of a few stages drives it far lower.
```

```python
# Countercurrent cascade: fraction of solute left after N ideal stages
E = 4.0              # extraction factor K_D * S/F
N = 3                # ideal stages
# Kremser-type result for a lean, straight-equilibrium system:
frac_left = (E - 1) / (E**(N + 1) - 1)
print(round(frac_left, 4))   # ~0.0118 -> ~99 percent removed in 3 stages
```

```mermaid
graph LR
    FEED["Feed solute in carrier"] --> MIX["Mix with solvent"]
    SOLV["Fresh solvent"] --> MIX
    MIX --> SETTLE["Settle two liquid phases"]
    SETTLE --> EXT["Extract solute rich solvent"]
    SETTLE --> RAF["Raffinate depleted feed"]
```

Remember: extraction uses a second immiscible solvent and the distribution
coefficient K_D to pull a solute out; a countercurrent cascade of stages
turns a modest per-stage split into a near-complete recovery.
""",
        ),
        quiz_lesson(
            "Quiz: Liquid-liquid extraction",
            (
                q(
                    "When is liquid-liquid extraction chosen over distillation?",
                    (
                        opt("Always - it is cheaper in every case"),
                        opt(
                            "When components are heat-sensitive, close-boiling, or "
                            "azeotropic - where distillation is costly or infeasible",
                            correct=True,
                        ),
                        opt("Only for gases"),
                        opt("Only when no solvent exists"),
                    ),
                    "Extraction sidesteps boiling, so it suits heat-sensitive or "
                    "hard-to-distill mixtures.",
                ),
                q(
                    "What does the distribution (partition) coefficient K_D describe?",
                    (
                        opt("The boiling point of the solvent"),
                        opt(
                            "The equilibrium ratio of solute concentration in the "
                            "extract to that in the raffinate",
                            correct=True,
                        ),
                        opt("The density difference between phases"),
                        opt("The number of stages required"),
                    ),
                    "K_D = y/x at equilibrium; a large, selective K_D means an effective solvent.",
                ),
                q(
                    "Why run extraction as a countercurrent cascade of stages?",
                    (
                        opt("To heat the mixture more evenly"),
                        opt(
                            "Fresh solvent meets the most-depleted feed at each stage, "
                            "multiplying a modest per-stage split into near-complete "
                            "recovery",
                            correct=True,
                        ),
                        opt("Because a single stage is impossible to build"),
                        opt("To eliminate the need for a solvent"),
                    ),
                    "Countercurrent staging keeps a driving force everywhere - the same "
                    "advantage as in absorption - so few stages remove most of the solute.",
                ),
            ),
        ),
        # -- 7. Membrane separations -----------------------------------
        _t(
            "Membrane separations",
            "11 min",
            """# Membrane separations

A **membrane** is a thin barrier that lets some species through more easily
than others. Instead of adding heat or a solvent, you apply a **driving
force** - usually a pressure difference - and let selectivity do the work.
The feed splits into the **permeate** (what passes) and the **retentate**
(what is held back). Because there is often no phase change, membranes can
be very energy-efficient.

Pressure-driven membranes form a spectrum by pore size and what they
reject:

- **Microfiltration (MF)** - particles, bacteria (~0.1 micron)
- **Ultrafiltration (UF)** - proteins, macromolecules
- **Nanofiltration (NF)** - multivalent ions, small organics
- **Reverse osmosis (RO)** - dissolved salts; the basis of **seawater
  desalination**

For RO, the applied pressure must first overcome the **osmotic pressure**
that pulls water the wrong way, then provide the net driving force:

```text
Osmotic pressure (van 't Hoff, dilute):
  pi = i . C . R . T
    i = number of ions per formula unit (NaCl -> ~2)
    C = molar concentration, R = gas constant, T = temperature

Water flux through an RO membrane:
  J_w = A_w . (dP - d_pi)
    A_w   = membrane water permeance
    dP    = applied pressure difference
    d_pi  = osmotic pressure difference across the membrane
Net driving force is (applied pressure MINUS osmotic pressure).
```

Performance is judged by **flux** (throughput per area) and **rejection**
(selectivity):

```python
# Salt rejection of an RO membrane
Cf = 35000.0         # mg/L feed salinity (~seawater)
Cp = 350.0           # mg/L permeate salinity
rejection = (1 - Cp/Cf) * 100
print(round(rejection, 1))   # 99.0 percent salt rejected
```

The practical enemy is **fouling** - particles, scale, and biofilm building
on the surface and cutting flux - and **concentration polarization**, where
rejected solute piles up at the membrane face and raises the local osmotic
pressure. Pretreatment, crossflow, and cleaning manage them.

```mermaid
graph LR
    FEED["Pressurized feed"] --> MEM["Selective membrane"]
    MEM --> PERM["Permeate passes through"]
    MEM --> RET["Retentate held back"]
    DP["Applied pressure driving force"] --> MEM
    FOUL["Fouling and polarization cut flux"] --> MEM
```

Remember: a membrane separates by selective permeability under a driving
force, splitting feed into permeate and retentate; for RO the net driving
force is applied pressure minus osmotic pressure, and fouling is the
practical limit.
""",
        ),
        quiz_lesson(
            "Quiz: Membrane separations",
            (
                q(
                    "How does a membrane separation work?",
                    (
                        opt("By boiling the feed into vapor"),
                        opt(
                            "A selective barrier lets some species permeate under a "
                            "driving force, splitting feed into permeate and retentate",
                            correct=True,
                        ),
                        opt("By freezing out the solute"),
                        opt("By adding an immiscible solvent"),
                    ),
                    "No phase change needed: selectivity plus a driving force (often "
                    "pressure) does the separation.",
                ),
                q(
                    "In reverse osmosis, what is the net driving force for water flux?",
                    (
                        opt("The applied pressure alone"),
                        opt(
                            "The applied pressure minus the osmotic pressure difference "
                            "across the membrane",
                            correct=True,
                        ),
                        opt("The osmotic pressure alone"),
                        opt("The temperature difference"),
                    ),
                    "J_w = A_w (dP - d_pi): you must beat osmotic pressure before any "
                    "net water crosses.",
                ),
                q(
                    "What are fouling and concentration polarization?",
                    (
                        opt("Ways to increase membrane flux"),
                        opt(
                            "Fouling is buildup on the surface that cuts flux; "
                            "concentration polarization is rejected solute piling up at "
                            "the membrane face, raising local osmotic pressure",
                            correct=True,
                        ),
                        opt("Types of membrane material"),
                        opt("Names for the permeate and retentate streams"),
                    ),
                    "Both degrade performance; crossflow, pretreatment and cleaning "
                    "manage them. Rejection and flux are the two performance metrics, "
                    "and fouling attacks flux over time.",
                ),
            ),
        ),
        # -- 8. Dimensionless groups and analogies ---------------------
        _t(
            "Dimensionless groups (Sherwood, Schmidt) and analogies",
            "11 min",
            """# Dimensionless groups (Sherwood, Schmidt) and analogies

We almost never solve the boundary layer from first principles. Instead we
**correlate** mass transfer coefficients using **dimensionless groups** -
the same trick that gives Nusselt and Prandtl numbers for heat. Three
groups run the show for mass transfer.

```text
Sherwood number (dimensionless mass transfer coefficient):
  Sh = k_c . L / D_AB       (convective transfer / diffusive transfer)

Schmidt number (momentum diffusivity / mass diffusivity):
  Sc = nu / D_AB = mu / (rho . D_AB)

Reynolds number (inertial / viscous forces):
  Re = rho . u . L / mu
```

Correlations then take the form **Sh = f(Re, Sc)**, mirroring heat
transfer's **Nu = f(Re, Pr)**. A classic for flow past a sphere or a pipe:

```text
Frossling / Ranz-Marshall (single sphere):
  Sh = 2 + 0.6 . Re^0.5 . Sc^(1/3)

Read it as: Sh gives k_c once you know the flow (Re) and the fluid
properties (Sc). More turbulence (higher Re) -> higher Sh -> higher k_c.
```

The deep idea is the **transport analogy**: momentum, heat, and mass are
carried by the same eddies, so their transfer coefficients move together.
The **Chilton-Colburn analogy** links them through the **j-factors**:

```text
Chilton-Colburn analogy:
  j_D = j_H          ->     Sh / (Re . Sc^(1/3))  =  Nu / (Re . Pr^(1/3))

Practical payoff: measure or correlate HEAT transfer (Nu), and predict
MASS transfer (Sh) for the same geometry - just swap Pr for Sc. One
experiment, two coefficients.
```

A worked coefficient from a correlation:

```python
Re, Sc = 10000.0, 0.9        # air-like flow past a surface
D_AB = 2.0e-5                # m^2/s, gas diffusivity
L = 0.10                     # m, characteristic length
Sh = 0.023 * Re**0.8 * Sc**(1.0/3.0)   # Dittus-Boelter-type analogy form
kc = Sh * D_AB / L
print(round(Sh, 1), round(kc, 5))   # Sh ~ 43.3, kc ~ 0.0087 m/s
```

```mermaid
graph TD
    RE["Reynolds number flow regime"] --> SH["Sherwood number"]
    SC["Schmidt number fluid properties"] --> SH
    SH --> KC["Extract k_c from Sh"]
    NU["Nusselt number heat transfer"] --> ANALOGY["Chilton Colburn analogy"]
    ANALOGY --> SH
```

Remember: Sherwood is the dimensionless k_c, Schmidt is the momentum-to-mass
diffusivity ratio, correlations give Sh = f(Re, Sc), and transport
analogies let a heat-transfer measurement predict mass transfer.
""",
        ),
        quiz_lesson(
            "Quiz: Dimensionless groups (Sherwood, Schmidt) and analogies",
            (
                q(
                    "What does the Sherwood number represent?",
                    (
                        opt("The ratio of heat to mass diffusivity"),
                        opt(
                            "The dimensionless convective mass transfer coefficient, "
                            "Sh = k_c L / D_AB - convective over diffusive transfer",
                            correct=True,
                        ),
                        opt("The pressure drop across a column"),
                        opt("The number of theoretical stages"),
                    ),
                    "Sh is to mass transfer what Nu is to heat transfer: the "
                    "dimensionless transfer coefficient.",
                ),
                q(
                    "What does the Schmidt number compare?",
                    (
                        opt("Inertial to viscous forces"),
                        opt(
                            "Momentum diffusivity (kinematic viscosity) to mass "
                            "diffusivity, Sc = nu / D_AB",
                            correct=True,
                        ),
                        opt("Heat capacity to thermal conductivity"),
                        opt("Reflux ratio to feed ratio"),
                    ),
                    "Sc = nu/D_AB is the mass-transfer analogue of the Prandtl number (nu/alpha).",
                ),
                q(
                    "What practical payoff does the Chilton-Colburn analogy give?",
                    (
                        opt("It removes the need for any driving force"),
                        opt(
                            "It links heat and mass transfer (j_H = j_D), so a "
                            "heat-transfer correlation predicts mass transfer by "
                            "swapping Pr for Sc",
                            correct=True,
                        ),
                        opt("It proves diffusion is instantaneous"),
                        opt("It sets the osmotic pressure of a membrane"),
                    ),
                    "Momentum, heat and mass share the same eddies; one measurement "
                    "(Nu) yields the other (Sh) for the same geometry. Correlations "
                    "take the form Sh = f(Re, Sc), paralleling Nu = f(Re, Pr).",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does Fick's first law relate?",
                    (
                        opt("Pressure to temperature"),
                        opt(
                            "Molar flux to the concentration gradient, through the "
                            "diffusivity, pointing down the gradient",
                            correct=True,
                        ),
                        opt("Reflux ratio to stage count"),
                        opt("Osmotic pressure to salinity"),
                    ),
                    "J_A = -D_AB (dC_A/dz): the microscopic driving force for diffusion.",
                ),
                q(
                    "A convective mass transfer coefficient k_c primarily does what?",
                    (
                        opt("Sets the equilibrium composition"),
                        opt(
                            "Lumps the boundary-layer physics so flux equals k_c times a "
                            "concentration difference",
                            correct=True,
                        ),
                        opt("Equals the diffusivity exactly"),
                        opt("Measures the column height"),
                    ),
                    "N_A = k_c (C_s - C_bulk); k_c grows with velocity and turbulence.",
                ),
                q(
                    "In two-film theory, where does the resistance to interphase "
                    "transfer reside, and what holds at the interface?",
                    (
                        opt("All in the bulk; the interface is at high concentration"),
                        opt(
                            "In stagnant films on each side of the interface, with the "
                            "two phases in equilibrium at the interface itself",
                            correct=True,
                        ),
                        opt("Only in the gas phase; the liquid has none"),
                        opt("Nowhere - transfer is instantaneous"),
                    ),
                    "Two film resistances in series, equilibrium at the interface; "
                    "combine into an overall K.",
                ),
                q(
                    "A sparingly soluble gas (large equilibrium slope m) is controlled "
                    "by which film?",
                    (
                        opt("The gas film"),
                        opt("The liquid film, since m/k_x dominates the resistance", correct=True),
                        opt("Neither"),
                        opt("The membrane film"),
                    ),
                    "Large m makes m/k_x the biggest term, so the liquid side controls "
                    "(e.g. CO2 or O2 in water).",
                ),
                q(
                    "What is the slope of the operating line in a dilute absorber?",
                    (
                        opt("The relative volatility alpha"),
                        opt("The liquid-to-gas molar flow ratio L/G", correct=True),
                        opt("The distribution coefficient K_D"),
                        opt("The Sherwood number"),
                    ),
                    "A solute balance gives y = (L/G)x + const; height then is HTU . NTU.",
                ),
                q(
                    "In distillation, what does relative volatility alpha tell you?",
                    (
                        opt("Nothing about separability"),
                        opt(
                            "How easy the split is - alpha near 1 means a very hard "
                            "separation, larger alpha means fewer stages",
                            correct=True,
                        ),
                        opt("The osmotic pressure of the feed"),
                        opt("The membrane rejection"),
                    ),
                    "alpha = 1 pinches (azeotrope-like); larger alpha eases the split. "
                    "Fenske sets minimum stages at total reflux.",
                ),
                q(
                    "What trade-off does the reflux ratio govern in a distillation column?",
                    (
                        opt("Feed temperature versus product purity"),
                        opt(
                            "Number of stages (capital) versus reboiler energy - higher "
                            "reflux needs fewer stages but more energy",
                            correct=True,
                        ),
                        opt("Membrane flux versus rejection"),
                        opt("Diffusivity versus viscosity"),
                    ),
                    "R_min gives infinite stages; total reflux gives minimum stages; "
                    "real designs balance capital against energy.",
                ),
                q(
                    "What does the distribution coefficient K_D govern in liquid-liquid "
                    "extraction?",
                    (
                        opt("The boiling point of the raffinate"),
                        opt(
                            "How the solute splits between extract and raffinate at "
                            "equilibrium - larger K_D means a stronger, better solvent",
                            correct=True,
                        ),
                        opt("The Reynolds number of the flow"),
                        opt("The number of trays in a column"),
                    ),
                    "K_D = y/x; a countercurrent cascade turns a modest per-stage split "
                    "into near-complete recovery.",
                ),
                q(
                    "For reverse osmosis, the net driving force for water flux is:",
                    (
                        opt("Applied pressure only"),
                        opt("Osmotic pressure only"),
                        opt(
                            "Applied pressure minus the osmotic pressure difference "
                            "across the membrane",
                            correct=True,
                        ),
                        opt("Temperature difference across the membrane"),
                    ),
                    "J_w = A_w (dP - d_pi): you must overcome osmotic pressure before "
                    "net water permeates. Fouling is the practical limit.",
                ),
                q(
                    "What do the Sherwood and Schmidt numbers do for mass transfer design?",
                    (
                        opt("They measure column height directly"),
                        opt(
                            "Sh is the dimensionless k_c and Sc is the momentum-to-mass "
                            "diffusivity ratio; correlations Sh = f(Re, Sc) and analogies "
                            "let heat data predict mass transfer",
                            correct=True,
                        ),
                        opt("They set the reflux ratio"),
                        opt("They define the distribution coefficient"),
                    ),
                    "Sh = k_c L / D_AB, Sc = nu / D_AB; the Chilton-Colburn analogy "
                    "(j_H = j_D) swaps Pr for Sc to turn one measurement into two.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

MASS_TRANSFER_SEPARATIONS_COURSES: tuple[SeedCourse, ...] = (_MASS_TRANSFER_SEPARATIONS,)
