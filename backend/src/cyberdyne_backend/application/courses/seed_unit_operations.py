"""Academy seed content - Unit Operations.

The workhorse physical operations that every chemical plant is assembled
from: moving fluids with pumps and compressors, separating mixtures by
distillation, concentrating and crystallizing with evaporators, removing
water by drying, separating solids by filtration and sedimentation,
purifying with adsorption, and transferring heat in exchangers. Each
lesson explains one operation directly, shows how to size or scale it with
a worked design calculation, and draws the flow as a diagram, followed by
a checkpoint quiz; the course closes with a comprehensive final quiz.
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


_UNIT_OPERATIONS = SeedCourse(
    slug="unit-operations",
    title="Unit Operations",
    description=(
        "The standard physical operations that make up every chemical plant - "
        "fluid transport, distillation, evaporation, drying, filtration, "
        "adsorption and heat exchange - and how to size and scale them. Every "
        "lesson gives a direct explanation, a worked sizing or design "
        "calculation, and a process diagram, so you can read a flowsheet and "
        "put real numbers on the equipment."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Unit Operations

A chemical plant looks complicated, but it is built from a small set of
repeating **physical operations** - moving a fluid, separating a mixture,
adding or removing heat, taking water out of a solid. These are the
**unit operations**, and once you can recognize and size each one you can
read any flowsheet and start putting numbers on the equipment.

The approach here is **concrete and quantitative**: every lesson explains
one operation directly, shows a short worked example of how engineers
**size or scale** it (a design equation, a mass or energy balance, a
Python calculation), and draws the operation as a diagram. After each
lesson there is a short quiz; at the end, a final quiz covers the whole
course.

What you will learn to size, in order:

1. **Fluid transport, pumps and compressors** - moving liquids and gases
2. **Distillation columns** - separating by relative volatility
3. **Evaporation and crystallization** - concentrating and forming solids
4. **Drying** - removing bound and free moisture from solids
5. **Filtration and sedimentation** - separating solids from fluids
6. **Adsorption** - capturing components on a solid surface
7. **Heat exchangers as a unit operation** - transferring heat
8. **Selecting and scaling unit operations** - choosing and sizing up

Ground rules you will see throughout: write a **mass and energy balance**
first, use **dimensionless groups** (Reynolds, Nusselt, Sherwood) to
carry lab data to plant scale, and always check that your equipment sits
in a sensible operating window. Simulators such as **Aspen Plus, HYSYS
and DWSIM** automate these calculations, but they only help once you know
what they are doing.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a 'unit operation'?",
                    (
                        opt("A single line of code in a process simulator"),
                        opt("A department in a chemical company"),
                        opt(
                            "A standard physical operation - such as pumping, "
                            "distillation or drying - that plants are assembled from",
                            correct=True,
                        ),
                        opt("A safety inspection performed once per shift"),
                    ),
                    "Plants are built from a small set of repeating physical operations; "
                    "learning to size each one lets you read any flowsheet.",
                ),
                q(
                    "What does each content lesson in this course give you?",
                    (
                        opt("Only a definition to memorize"),
                        opt(
                            "A direct explanation, a worked sizing or design "
                            "calculation, and a process diagram",
                            correct=True,
                        ),
                        opt("A full simulator licence"),
                        opt("Only a quiz, with no explanation"),
                    ),
                    "The course is deliberately quantitative: explain, size with a "
                    "worked calculation, and diagram the operation.",
                ),
            ),
        ),
        # -- 1. Fluid transport ----------------------------------------
        _t(
            "Fluid transport, pumps and compressors",
            "10 min",
            """# Fluid transport, pumps and compressors

Every plant has to **move fluids** through pipes against friction and
elevation. The tool for liquids is the **pump**; for gases it is the
**compressor** or **fan**. Sizing them starts from the **mechanical
energy balance** - how much head the machine must add.

Two ideas dominate. First, **friction loss** depends on flow regime,
captured by the **Reynolds number** Re = rho*v*D/mu: below about 2100 the
flow is **laminar**, above about 4000 it is **turbulent**, which sets the
friction factor. Second, a pump adds **head** (energy per unit weight,
in metres), and the operating point is where the **pump curve** crosses
the **system curve**.

For liquids, guard against **cavitation**: the available suction head
**NPSHA** must exceed the pump's required **NPSHR**, or vapour bubbles
form and collapse, damaging the impeller.

A worked pump sizing using the mechanical energy balance:

```text
Duty:   Q = 0.020 m3/s of water (rho = 1000 kg/m3)
Static lift:            dz = 15 m
Friction head loss:     hf = 6 m  (from friction factor and pipe length)
Velocity/pressure terms negligible between two open tanks.

Total dynamic head:
  H = dz + hf = 15 + 6 = 21 m

Hydraulic power:
  P_hyd = rho * g * Q * H
        = 1000 * 9.81 * 0.020 * 21 = 4120 W = 4.12 kW

Apply pump efficiency eta = 0.65:
  P_shaft = P_hyd / eta = 4.12 / 0.65 = 6.3 kW

So specify roughly a 7.5 kW motor and confirm NPSHA > NPSHR.
```

For a gas, the machine is a compressor and the energy input follows the
compression path (isothermal or adiabatic); the same idea of overcoming a
pressure difference applies, but density changes with pressure.

```mermaid
graph LR
    TANK["Source tank"] --> SUCT["Suction line and NPSHA check"]
    SUCT --> PUMP["Pump adds head H"]
    PUMP --> DISCH["Discharge line friction"]
    DISCH --> DEST["Destination at higher elevation"]
    PUMP --> CURVE["Operating point on pump curve"]
```

Remember: size a pump from total head equals static lift plus friction,
convert to shaft power through efficiency, and always verify the suction
side will not cavitate.
""",
        ),
        quiz_lesson(
            "Quiz: Fluid transport, pumps and compressors",
            (
                q(
                    "The total dynamic head a pump must supply is made up of what?",
                    (
                        opt("Only the pipe diameter"),
                        opt(
                            "The static lift (elevation change) plus the friction head "
                            "loss (plus any pressure and velocity terms)",
                            correct=True,
                        ),
                        opt("Only the motor efficiency"),
                        opt("The Reynolds number times the flow rate"),
                    ),
                    "H = static lift + friction loss; multiply rho*g*Q*H for hydraulic "
                    "power, then divide by efficiency for shaft power.",
                ),
                q(
                    "What does the Reynolds number tell you when sizing a pipe?",
                    (
                        opt("The pump's purchase cost"),
                        opt(
                            "Whether the flow is laminar or turbulent, which sets the "
                            "friction factor and hence the friction loss",
                            correct=True,
                        ),
                        opt("The exact motor voltage needed"),
                        opt("The crystal size in the product"),
                    ),
                    "Re = rho*v*D/mu: laminar below about 2100, turbulent above about "
                    "4000, controlling friction losses.",
                ),
                q(
                    "Why must NPSHA exceed NPSHR for a liquid pump?",
                    (
                        opt("To make the motor spin faster"),
                        opt("To reduce the purchase price"),
                        opt(
                            "Otherwise the liquid vaporizes at the suction and the "
                            "bubbles collapse, causing cavitation damage",
                            correct=True,
                        ),
                        opt("To increase the Reynolds number"),
                    ),
                    "Available suction head must beat the required value or cavitation "
                    "erodes the impeller and kills performance.",
                ),
            ),
        ),
        # -- 2. Distillation -------------------------------------------
        _t(
            "Distillation columns",
            "11 min",
            """# Distillation columns

**Distillation** separates a liquid mixture by exploiting differences in
**volatility**: heat the mixture and the more volatile component
concentrates in the vapour, the less volatile in the liquid. Repeat the
partial vaporization and condensation on many **stages** stacked in a
column and you get a sharp separation - the workhorse of the refining and
petrochemical industries.

The key property is the **relative volatility** alpha = (y_A/x_A) /
(y_B/x_B). The larger alpha is, the easier the separation and the fewer
stages you need. Vapour rises, liquid falls, and they contact on **trays**
or **packing**; a **reboiler** boils the bottoms and a **condenser**
returns **reflux** to the top.

For a binary mixture the classic hand method is **McCabe-Thiele**: plot
the equilibrium curve and the operating lines, and step off the stages
between them. The **reflux ratio** R = L/D trades off against stages -
more reflux means fewer stages but more reboiler and condenser duty (more
energy). The two limits bound the design:

```text
Minimum stages (total reflux) - Fenske equation:
  N_min = ln[ (x_D/(1-x_D)) * ((1-x_W)/x_W) ] / ln(alpha)

Example: light-key purity x_D = 0.98, bottoms x_W = 0.02, alpha = 2.5
  ratio term = (0.98/0.02) * (0.98/0.02) = 49 * 49 = 2401
  N_min = ln(2401) / ln(2.5) = 7.78 / 0.916 = 8.5 stages

Minimum reflux (infinite stages) sets the other bound; the real design
runs at R = 1.2 to 1.5 times R_min, giving a finite stage count between
these limits (Gilliland correlation ties N and R together).
```

```mermaid
graph TD
    FEED["Feed enters mid column"] --> COL["Column with stages"]
    COL --> TOP["Vapour up to condenser"]
    TOP --> REFLUX["Reflux liquid returned"]
    TOP --> DIST["Distillate light product"]
    COL --> BOT["Liquid down to reboiler"]
    BOT --> BOILUP["Vapour boilup back up"]
    BOT --> BOTTOMS["Bottoms heavy product"]
```

Remember: separation is driven by relative volatility, the number of
stages and the reflux ratio trade against each other, and Fenske gives
the minimum stages at total reflux as an anchor for the real design.
""",
        ),
        quiz_lesson(
            "Quiz: Distillation columns",
            (
                q(
                    "What physical property does distillation exploit to separate a mixture?",
                    (
                        opt("Differences in colour"),
                        opt("Differences in electrical charge"),
                        opt(
                            "Differences in volatility - the more volatile component "
                            "concentrates in the vapour",
                            correct=True,
                        ),
                        opt("Differences in radioactivity"),
                    ),
                    "Relative volatility alpha drives the split; larger alpha means an "
                    "easier separation with fewer stages.",
                ),
                q(
                    "What does the Fenske equation give you?",
                    (
                        opt("The pump power for the reflux"),
                        opt(
                            "The minimum number of stages at total reflux for a "
                            "specified separation",
                            correct=True,
                        ),
                        opt("The column diameter"),
                        opt("The condenser cooling water flow"),
                    ),
                    "N_min from Fenske anchors the design; real columns run at finite "
                    "reflux with more stages than N_min.",
                ),
                q(
                    "How do reflux ratio and number of stages trade off?",
                    (
                        opt("They are unrelated"),
                        opt(
                            "More reflux means fewer stages but higher reboiler and "
                            "condenser energy duty",
                            correct=True,
                        ),
                        opt("More reflux always needs more stages"),
                        opt("Reflux has no effect on energy use"),
                    ),
                    "Designs run at about 1.2 to 1.5 times minimum reflux, balancing "
                    "capital (stages) against energy (reflux duty).",
                ),
            ),
        ),
        # -- 3. Evaporation & crystallization --------------------------
        _t(
            "Evaporation and crystallization",
            "10 min",
            """# Evaporation and crystallization

**Evaporation** concentrates a solution by boiling off **solvent**
(usually water), leaving a more concentrated liquor - think of thickening
fruit juice or caustic soda. **Crystallization** goes further: keep
removing solvent (or cool the liquor) until the solute exceeds its
**solubility** and forms solid **crystals** you can filter off. Together
they turn a dilute solution into a concentrated product or a pure solid.

Evaporator sizing starts from a **mass and energy balance**. The solute
is conserved, so you know how much water to boil off; the heat to boil it
comes from steam through a heating surface, sized by Q = U*A*dT.

A worked single-effect evaporator balance:

```text
Feed:    F = 10000 kg/h at 10 wt% solids  -> solute = 1000 kg/h
Product: L at 40 wt% solids  -> solute still 1000 kg/h
  L = 1000 / 0.40 = 2500 kg/h
Vapour boiled off:
  V = F - L = 10000 - 2500 = 7500 kg/h of water

Heat duty (latent heat of water ~ 2260 kJ/kg, feed already near boiling):
  Q = V * lambda = 7500/3600 * 2260 = 4710 kW

Heating area with U = 2000 W/m2K and dT = 25 K:
  A = Q / (U * dT) = 4 710 000 / (2000 * 25) = 94 m2
```

To cut steam use, plants run **multiple-effect** evaporators: the vapour
from one effect heats the next at lower pressure, so one kilogram of steam
boils off several kilograms of water. Watch **boiling point elevation**
(concentrated liquor boils hotter) and fouling.

```mermaid
graph LR
    FEED["Dilute feed"] --> EVAP["Evaporator heated by steam"]
    EVAP --> VAP["Water vapour off"]
    EVAP --> CONC["Concentrated liquor"]
    CONC --> CRYST["Cool or concentrate past solubility"]
    CRYST --> XTAL["Crystals form"]
    CRYST --> MOTHER["Mother liquor recycled"]
```

Remember: size an evaporator from a solute balance to get the vapour rate,
then Q = U*A*dT for the area; push past solubility to crystallize, and use
multiple effects to save steam.
""",
        ),
        quiz_lesson(
            "Quiz: Evaporation and crystallization",
            (
                q(
                    "In an evaporator mass balance, what stays constant between feed and product?",
                    (
                        opt("The water content"),
                        opt("The non-volatile solute mass", correct=True),
                        opt("The total mass flow"),
                        opt("The temperature"),
                    ),
                    "Solute is conserved, so knowing feed and product concentrations "
                    "fixes the product flow and the vapour boiled off.",
                ),
                q(
                    "Why do plants use multiple-effect evaporators?",
                    (
                        opt("To make the crystals larger"),
                        opt(
                            "The vapour from one effect heats the next at lower "
                            "pressure, so one kilogram of steam boils off several "
                            "kilograms of water",
                            correct=True,
                        ),
                        opt("To avoid needing any steam at all"),
                        opt("To increase boiling point elevation"),
                    ),
                    "Reusing vapour as the heating medium across effects sharply cuts "
                    "the fresh steam per kilogram of water evaporated.",
                ),
                q(
                    "What triggers crystals to form during crystallization?",
                    (
                        opt("Heating the liquor above its boiling point"),
                        opt("Adding more solvent"),
                        opt(
                            "Driving the solute concentration past its solubility limit "
                            "by removing solvent or cooling",
                            correct=True,
                        ),
                        opt("Increasing the pump speed"),
                    ),
                    "Supersaturation - exceeding solubility - is the driving force for "
                    "nucleation and crystal growth.",
                ),
            ),
        ),
        # -- 4. Drying -------------------------------------------------
        _t(
            "Drying",
            "10 min",
            """# Drying

**Drying** removes a liquid (usually water) from a **solid** by
vaporizing it, typically with warm air. It is the last step for many
products - pharmaceuticals, food powders, polymers - and it controls final
moisture, particle properties and stability.

The heart of drying is the **drying-rate curve**, which has two regimes:

- **Constant-rate period** - the surface stays wet, water evaporates as if
  from a free liquid, and the rate is set by **heat and mass transfer**
  from the air (air temperature, humidity and velocity). Removing more air
  or hotter air speeds it up.
- **Falling-rate period** - once the surface dries, moisture must diffuse
  from inside the solid to the surface. The rate drops and is controlled
  by the **material**, not the air. This is where most of the time goes.

The target is the **equilibrium moisture content**: a solid in contact
with air of a given humidity can only be dried down to the moisture in
balance with that air - you cannot go below it without drier air.

A worked drying-time estimate for the constant-rate period:

```text
Wet solid: 100 kg dry basis, from X1 = 0.40 to Xc = 0.15 kg water/kg dry
Water to remove in constant-rate period:
  W = 100 * (0.40 - 0.15) = 25 kg

Exposed area A = 5 m2, constant drying rate Rc = 1.5 kg/(m2 h)
  Rate of removal = Rc * A = 1.5 * 5 = 7.5 kg/h

Constant-rate drying time:
  t = W / (Rc * A) = 25 / 7.5 = 3.3 h

The falling-rate period below Xc is slower and is integrated separately
from the falling-rate curve down to the target moisture.
```

Equipment matches the material: **tray** dryers for batches, **rotary**
and **fluidized-bed** dryers for free-flowing solids, **spray** dryers to
turn a liquid feed directly into a powder.

```mermaid
graph LR
    WET["Wet solid feed"] --> HEAT["Warm air supplies heat"]
    HEAT --> CONST["Constant rate surface wet"]
    CONST --> CRIT["Critical moisture content"]
    CRIT --> FALL["Falling rate internal diffusion"]
    FALL --> EQ["Equilibrium moisture reached"]
    EQ --> DRY["Dry product"]
```

Remember: drying has a fast constant-rate period set by the air and a slow
falling-rate period set by the solid, and you can only reach the
equilibrium moisture in balance with the drying air.
""",
        ),
        quiz_lesson(
            "Quiz: Drying",
            (
                q(
                    "What controls the drying rate during the constant-rate period?",
                    (
                        opt("Internal diffusion inside the solid"),
                        opt(
                            "Heat and mass transfer from the air - its temperature, "
                            "humidity and velocity",
                            correct=True,
                        ),
                        opt("The colour of the solid"),
                        opt("The pump curve"),
                    ),
                    "While the surface stays wet, water leaves as from a free liquid, so "
                    "the air conditions set the rate.",
                ),
                q(
                    "What happens in the falling-rate period?",
                    (
                        opt("Drying speeds up dramatically"),
                        opt(
                            "The surface has dried, so moisture must diffuse from inside "
                            "the solid and the rate falls, controlled by the material",
                            correct=True,
                        ),
                        opt("The air humidity no longer matters at all and drying stops"),
                        opt("The solid reabsorbs water from the air"),
                    ),
                    "Below the critical moisture content, internal diffusion limits the "
                    "rate - this is where most drying time is spent.",
                ),
                q(
                    "Why can you not dry a solid below its equilibrium moisture content?",
                    (
                        opt("The dryer runs out of electricity"),
                        opt(
                            "That moisture is in balance with the drying air's humidity; "
                            "reaching lower requires drier air",
                            correct=True,
                        ),
                        opt("The solid always stays fully wet"),
                        opt("Equilibrium moisture is always zero"),
                    ),
                    "Equilibrium moisture depends on the air humidity; only drier air "
                    "lowers the achievable end moisture.",
                ),
            ),
        ),
        # -- 5. Filtration & sedimentation -----------------------------
        _t(
            "Filtration and sedimentation",
            "10 min",
            """# Filtration and sedimentation

Once you have made a solid, you have to **separate it from the liquid**.
Two mechanical operations do this. **Filtration** forces the slurry
through a **medium** (cloth, screen, membrane) that holds back solids as a
**cake** and lets the **filtrate** pass. **Sedimentation** lets gravity
pull the denser solids down through the liquid so the clear liquid
overflows the top.

Filtration is governed by flow through the growing cake. As the cake
thickens, resistance rises and the flow slows. The **cake filtration
equation** relates filtrate volume, pressure drop and time:

```text
Constant-pressure cake filtration (per unit area):
  dt/dV = (mu / (A^2 * dP)) * (alpha * c * V + A * Rm)

  alpha = specific cake resistance   c = solids per volume filtrate
  Rm = medium resistance             dP = pressure drop

Integrating gives a straight line of t/V versus V:
  t/V = [ mu*alpha*c / (2*A^2*dP) ] * V + [ mu*Rm / (A*dP) ]

Plot t/V against V from a lab test; the slope gives alpha (cake
resistance) and the intercept gives Rm. Those two numbers scale the test
straight up to a full-size filter of area A.
```

For sedimentation, the key number is the **settling velocity** of a
particle. In the slow (Stokes) regime a sphere settles at:

```text
Stokes settling velocity:
  v = (rho_s - rho_l) * g * d^2 / (18 * mu)

Example: d = 50 um, rho_s = 2500, rho_l = 1000 kg/m3, mu = 0.001 Pa s
  v = (1500) * 9.81 * (50e-6)^2 / (18 * 0.001)
    = 1500 * 9.81 * 2.5e-9 / 0.018 = 0.0020 m/s

A thickener or clarifier must have enough surface area that the upflow of
liquid is slower than this settling velocity, or particles carry over.
```

```mermaid
graph TD
    SLURRY["Feed slurry"] --> SPLIT["Solid liquid separation"]
    SPLIT --> FILT["Filtration through medium"]
    FILT --> CAKE["Cake retained"]
    FILT --> FILTRATE["Clear filtrate"]
    SPLIT --> SETTLE["Sedimentation by gravity"]
    SETTLE --> UNDER["Thickened underflow"]
    SETTLE --> OVER["Clarified overflow"]
```

Remember: filtration retains a cake whose resistance grows with thickness
(get alpha and Rm from a lab t/V plot), while sedimentation separates by
settling velocity, so a clarifier is sized to keep liquid upflow below it.
""",
        ),
        quiz_lesson(
            "Quiz: Filtration and sedimentation",
            (
                q(
                    "Why does the flow rate fall during constant-pressure cake filtration?",
                    (
                        opt("The pump gets weaker over time"),
                        opt(
                            "The cake grows thicker, so its resistance to flow rises",
                            correct=True,
                        ),
                        opt("The filtrate becomes more viscous"),
                        opt("The medium dissolves"),
                    ),
                    "Resistance rises as solids build up; a t/V versus V plot gives the "
                    "cake resistance alpha and medium resistance Rm.",
                ),
                q(
                    "In Stokes' law, how does settling velocity depend on particle diameter?",
                    (
                        opt("It is independent of diameter"),
                        opt("It is proportional to the diameter"),
                        opt(
                            "It is proportional to the diameter squared - larger "
                            "particles settle much faster",
                            correct=True,
                        ),
                        opt("It is inversely proportional to the diameter"),
                    ),
                    "v scales with (rho_s - rho_l)*g*d^2/(18*mu); the d-squared term "
                    "means fine particles settle very slowly.",
                ),
                q(
                    "How is a gravity clarifier sized?",
                    (
                        opt("By making the tank as tall as possible"),
                        opt(
                            "So the upward liquid velocity is below the particle "
                            "settling velocity, or solids carry over the top",
                            correct=True,
                        ),
                        opt("By matching the pump curve to the system curve"),
                        opt("By the relative volatility of the solids"),
                    ),
                    "Clarifier area, not depth, controls the overflow: keep upflow "
                    "slower than the settling velocity so particles descend.",
                ),
            ),
        ),
        # -- 6. Adsorption ---------------------------------------------
        _t(
            "Adsorption",
            "10 min",
            """# Adsorption

**Adsorption** captures molecules from a fluid onto the surface of a
**solid adsorbent** - activated carbon, zeolite, silica gel, alumina. It
is how plants remove trace impurities, dry gases, recover solvents and
purify products down to parts per million, where distillation would be
uneconomic.

The capacity of an adsorbent at equilibrium is described by an
**isotherm** - the loading q on the solid versus the concentration or
pressure in the fluid. Two common forms:

- **Langmuir** - assumes a fixed number of sites, so loading saturates:
  q = q_max * K * C / (1 + K * C).
- **Freundlich** - an empirical power law: q = K * C^(1/n), good for
  heterogeneous surfaces at moderate concentration.

In practice adsorption runs in a **packed bed**. Feed enters and the front
of the bed loads up first; a **mass-transfer zone** moves down the bed
until the outlet concentration rises - **breakthrough**. You stop before
that and **regenerate** the bed (heat it, drop the pressure, or purge it),
so beds run in a swing cycle: one adsorbing while another regenerates.

A worked bed-capacity estimate:

```text
Adsorbent: 500 kg of carbon, equilibrium loading q = 0.18 kg VOC/kg carbon
Feed: air with 0.004 kg VOC per m3, flow 0.5 m3/s

Total capacity to breakthrough (assume full use of equilibrium loading):
  M = 500 * 0.18 = 90 kg VOC

VOC fed per second:
  m_dot = 0.5 * 0.004 = 0.002 kg/s

Ideal time to breakthrough:
  t = M / m_dot = 90 / 0.002 = 45000 s = 12.5 h

Real beds break through earlier because of the mass-transfer zone; a
usable-capacity factor of about 0.6 to 0.7 is applied, so plan to switch
beds near 8 to 9 hours.
```

```mermaid
graph LR
    FEED["Feed with impurity"] --> BED["Packed adsorbent bed"]
    BED --> ZONE["Mass transfer zone moves down"]
    ZONE --> CLEAN["Purified outlet"]
    ZONE --> BT["Breakthrough detected"]
    BT --> REGEN["Regenerate by heat or purge"]
    REGEN --> BED
```

Remember: adsorbent capacity follows an isotherm (Langmuir saturates,
Freundlich is a power law), packed beds run to breakthrough then
regenerate, and real usable capacity is a fraction of the equilibrium
loading because of the mass-transfer zone.
""",
        ),
        quiz_lesson(
            "Quiz: Adsorption",
            (
                q(
                    "What does an adsorption isotherm describe?",
                    (
                        opt("The temperature of the bed over time"),
                        opt(
                            "The equilibrium loading on the solid versus the "
                            "concentration or pressure in the fluid",
                            correct=True,
                        ),
                        opt("The pump head required"),
                        opt("The colour of the adsorbent"),
                    ),
                    "Isotherms like Langmuir and Freundlich give capacity q as a "
                    "function of fluid concentration.",
                ),
                q(
                    "What is 'breakthrough' in a packed adsorption bed?",
                    (
                        opt("The bed physically cracking open"),
                        opt(
                            "When the mass-transfer zone reaches the outlet and the "
                            "exit concentration begins to rise",
                            correct=True,
                        ),
                        opt("When the pump cavitates"),
                        opt("When the crystals form"),
                    ),
                    "You stop the run before breakthrough and regenerate; beds swing "
                    "between adsorbing and regenerating.",
                ),
                q(
                    "Why is the usable bed capacity less than the equilibrium loading times the mass of adsorbent?",
                    (
                        opt("The adsorbent dissolves in the feed"),
                        opt(
                            "The mass-transfer zone means part of the bed is only "
                            "partly loaded when the outlet breaks through",
                            correct=True,
                        ),
                        opt("Isotherms overpredict by exactly half every time"),
                        opt("Regeneration adds mass to the bed"),
                    ),
                    "A usable-capacity factor of about 0.6 to 0.7 accounts for the "
                    "unused loading in the transfer zone at breakthrough.",
                ),
            ),
        ),
        # -- 7. Heat exchangers ----------------------------------------
        _t(
            "Heat exchangers as a unit operation",
            "10 min",
            """# Heat exchangers as a unit operation

Almost every operation so far needs **heat added or removed** - reboilers,
condensers, evaporators, dryers, feed preheaters. The **heat exchanger**
is the unit operation that transfers heat between two streams without
mixing them, most often the **shell-and-tube** design built to the
**ASME BPVC** and TEMA standards.

Sizing rests on one equation: **Q = U*A*dTlm**.

- **Q** is the duty, from an energy balance on either stream
  (Q = m*cp*dT, or m*lambda for a phase change).
- **U** is the **overall heat transfer coefficient**, combining the two
  film coefficients and the wall - dominated by the worse side, and it
  degrades as **fouling** builds up.
- **dTlm** is the **log-mean temperature difference**, the correct average
  driving force along the exchanger. **Counter-current** flow gives a
  larger dTlm than co-current for the same terminal temperatures, so it
  needs less area.

A worked area calculation:

```text
Hot oil: 3 kg/s, cp = 2.1 kJ/kgK, cooled 120 -> 70 C
Duty:  Q = 3 * 2.1 * (120 - 70) = 315 kW

Cooling water enters 25 C, leaves 45 C (counter-current).
Terminal differences:
  dT1 = 120 - 45 = 75 C     dT2 = 70 - 25 = 45 C
Log-mean temperature difference:
  dTlm = (75 - 45) / ln(75/45) = 30 / 0.511 = 58.7 C

With U = 400 W/m2K:
  A = Q / (U * dTlm) = 315000 / (400 * 58.7) = 13.4 m2
```

A quick Python version of the same sizing:

```python
import math

Q = 315_000.0            # W, from the energy balance
dT1, dT2 = 75.0, 45.0    # terminal temperature differences, C
U = 400.0                # W/m2K, overall coefficient

dTlm = (dT1 - dT2) / math.log(dT1 / dT2)
area = Q / (U * dTlm)
print(round(dTlm, 1), "C ->", round(area, 1), "m2")   # 58.7 C -> 13.4 m2
```

```mermaid
graph LR
    HOTIN["Hot stream in"] --> HEX["Heat exchanger area A"]
    COLDIN["Cold stream in counter current"] --> HEX
    HEX --> HOTOUT["Hot stream cooled"]
    HEX --> COLDOUT["Cold stream heated"]
    HEX --> DRIVE["Driving force is log mean dT"]
```

Remember: size any exchanger from Q = U*A*dTlm - get Q from an energy
balance, U from the film coefficients plus fouling, and use the log-mean
driving force with counter-current flow to minimize area.
""",
        ),
        quiz_lesson(
            "Quiz: Heat exchangers as a unit operation",
            (
                q(
                    "What is the design equation for a heat exchanger?",
                    (
                        opt("Q = m * v^2 / 2"),
                        opt("Q = U * A * dTlm", correct=True),
                        opt("Q = rho * g * H"),
                        opt("Q = alpha * c * V"),
                    ),
                    "Duty equals overall coefficient times area times the log-mean "
                    "temperature difference.",
                ),
                q(
                    "Why is counter-current flow preferred over co-current?",
                    (
                        opt("It is cheaper to fabricate"),
                        opt(
                            "It gives a larger log-mean temperature difference for the "
                            "same terminal temperatures, so less area is needed",
                            correct=True,
                        ),
                        opt("It removes the need for a pump"),
                        opt("It prevents all fouling"),
                    ),
                    "A larger dTlm means a bigger driving force, so counter-current "
                    "exchangers are more compact for the same duty.",
                ),
                q(
                    "What happens to the overall coefficient U as fouling builds up?",
                    (
                        opt("It increases, improving heat transfer"),
                        opt(
                            "It decreases, adding resistance so the exchanger transfers "
                            "less heat for the same area",
                            correct=True,
                        ),
                        opt("It stays exactly constant"),
                        opt("It becomes negative"),
                    ),
                    "Fouling layers add thermal resistance; designers include a fouling "
                    "allowance so the exchanger still meets duty over time.",
                ),
            ),
        ),
        # -- 8. Selecting & scaling ------------------------------------
        _t(
            "Selecting and scaling unit operations",
            "10 min",
            """# Selecting and scaling unit operations

A flowsheet is a **sequence of unit operations** chosen to get from raw
feed to product. Two engineering skills tie the course together: picking
the **right operation** for a separation, and **scaling** a proven design
from the lab or pilot plant to full size.

**Selecting** starts from the property difference you can exploit:

- Different **volatility** -> distillation or evaporation.
- Different **solubility** -> crystallization, or extraction.
- A **solid** to recover from a fluid -> filtration or sedimentation.
- A trace component in a large stream -> adsorption or absorption.
- Heat to move -> a heat exchanger.

Cost and scale then narrow it: distillation is cheap at large throughput
but poor for trace removal; adsorption is ideal for trace removal but
expensive in bulk.

**Scaling** is where dimensionless groups earn their keep. You almost
never build the plant-size unit first; you match **dimensionless numbers**
between scales so the physics stays the same:

```text
Group            Ratio it captures            Keeps constant across scale
-----            ------------------            ---------------------------
Reynolds  Re     inertia / viscous            flow regime (laminar/turbulent)
Nusselt   Nu     convective / conductive      heat-transfer coefficient
Sherwood  Sh     convective / diffusive       mass-transfer coefficient
Prandtl   Pr     momentum / thermal diff.     fluid property group

Rule of thumb: hold the governing dimensionless group constant and the
correlation (e.g. Nu = 0.023*Re^0.8*Pr^0.4 for turbulent tube flow) carries
lab data straight to plant size. Geometric similarity plus matched groups
means the pilot result predicts the full-scale result.
```

Beware what does **not** scale linearly: surface-to-volume ratio falls as
equipment grows (so heat removal per unit volume drops - a real risk for
exothermic reactors), and mixing time changes with impeller scale-up rules
(constant power per unit volume or constant tip speed, not both).

```mermaid
graph TD
    PROP["Property difference to exploit"] --> PICK["Select the unit operation"]
    PICK --> COST["Weigh cost and throughput"]
    COST --> PILOT["Prove at lab or pilot scale"]
    PILOT --> DIM["Match dimensionless groups"]
    DIM --> FULL["Scale up to full plant"]
    FULL --> CHECK["Check surface to volume and mixing"]
```

Remember: choose the operation from the property difference and the scale,
then scale up by holding the governing dimensionless group constant - and
watch the ratios (like surface to volume) that shift as equipment grows.
""",
        ),
        quiz_lesson(
            "Quiz: Selecting and scaling unit operations",
            (
                q(
                    "You need to remove a trace impurity down to parts per million from a large stream. Which operation fits best?",
                    (
                        opt("Distillation, because it is cheap at large throughput"),
                        opt(
                            "Adsorption, which excels at removing trace components",
                            correct=True,
                        ),
                        opt("Sedimentation"),
                        opt("Compression"),
                    ),
                    "Distillation is uneconomic for trace removal; adsorption (or "
                    "absorption) is the standard choice at low concentration.",
                ),
                q(
                    "Why do engineers hold a dimensionless group constant when scaling up?",
                    (
                        opt("To keep the equipment the same colour"),
                        opt(
                            "So the governing physics (flow regime, heat or mass "
                            "transfer) stays the same and lab correlations still apply",
                            correct=True,
                        ),
                        opt("Because regulations require it"),
                        opt("To make the Reynolds number zero"),
                    ),
                    "Matching Reynolds, Nusselt or Sherwood between scales keeps the "
                    "correlation valid, so pilot data predicts full scale.",
                ),
                q(
                    "What is a classic pitfall that does NOT scale linearly with size?",
                    (
                        opt("The colour of the product"),
                        opt(
                            "The surface-to-volume ratio falls as equipment grows, so "
                            "heat removal per unit volume drops",
                            correct=True,
                        ),
                        opt("The atomic weight of the solvent"),
                        opt("The value of pi"),
                    ),
                    "Volume grows faster than surface; exothermic reactors can lose the "
                    "ability to shed heat at large scale.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is a unit operation?",
                    (
                        opt("A financial unit in a plant budget"),
                        opt(
                            "A standard physical operation - pumping, distillation, "
                            "drying and so on - that plants are built from",
                            correct=True,
                        ),
                        opt("A single reaction step only"),
                        opt("A control-room shift"),
                    ),
                    "Plants are assembled from a small set of repeating physical "
                    "operations; sizing each is the core skill.",
                ),
                q(
                    "A pump's total dynamic head is the static lift plus what?",
                    (
                        opt("The Reynolds number"),
                        opt(
                            "The friction head loss (plus pressure and velocity terms)",
                            correct=True,
                        ),
                        opt("The relative volatility"),
                        opt("The log-mean temperature difference"),
                    ),
                    "H = static lift + friction loss; then P_shaft = rho*g*Q*H / "
                    "efficiency, with an NPSHA check against cavitation.",
                ),
                q(
                    "Distillation separates components based on their…",
                    (
                        opt("electrical charge"),
                        opt("relative volatility", correct=True),
                        opt("magnetic moment"),
                        opt("particle diameter"),
                    ),
                    "Larger relative volatility alpha means an easier split; Fenske "
                    "gives the minimum stages at total reflux.",
                ),
                q(
                    "In an evaporator, what quantity is conserved that lets you find the vapour rate?",
                    (
                        opt("The total mass flow"),
                        opt("The non-volatile solute mass", correct=True),
                        opt("The heat duty"),
                        opt("The pressure"),
                    ),
                    "Solute in equals solute out; with the two concentrations you get "
                    "the product flow and the water boiled off.",
                ),
                q(
                    "Which drying regime is slow and controlled by diffusion inside the solid?",
                    (
                        opt("The constant-rate period"),
                        opt("The falling-rate period", correct=True),
                        opt("The equilibrium period"),
                        opt("The turbulent period"),
                    ),
                    "Below the critical moisture content, internal diffusion limits the "
                    "rate; most drying time is spent here.",
                ),
                q(
                    "In Stokes' law, the settling velocity of a particle scales with…",
                    (
                        opt("the diameter to the first power"),
                        opt("the square of the particle diameter", correct=True),
                        opt("the inverse of the diameter"),
                        opt("the diameter cubed"),
                    ),
                    "v = (rho_s - rho_l)*g*d^2/(18*mu); the d-squared term is why fines "
                    "settle so slowly and a clarifier is sized on area.",
                ),
                q(
                    "In a packed adsorption bed, what marks the point to stop and regenerate?",
                    (
                        opt("The pump cavitating"),
                        opt(
                            "Breakthrough - the mass-transfer zone reaches the outlet "
                            "and the exit concentration rises",
                            correct=True,
                        ),
                        opt("The reflux ratio hitting its minimum"),
                        opt("The log-mean temperature difference going to zero"),
                    ),
                    "Run to just before breakthrough, then swing to a regenerated bed; "
                    "usable capacity is about 0.6 to 0.7 of equilibrium loading.",
                ),
                q(
                    "What are the three factors in the heat exchanger design equation Q = U*A*dTlm?",
                    (
                        opt("Reynolds number, area, and pressure"),
                        opt(
                            "Overall heat transfer coefficient, heat transfer area, and "
                            "log-mean temperature difference",
                            correct=True,
                        ),
                        opt("Relative volatility, reflux, and stages"),
                        opt("Density, gravity, and head"),
                    ),
                    "Q from an energy balance, U from the film coefficients plus "
                    "fouling, dTlm as the correct average driving force.",
                ),
                q(
                    "Why is counter-current flow used in heat exchangers?",
                    (
                        opt("It eliminates fouling completely"),
                        opt(
                            "It gives a larger log-mean temperature difference, so less "
                            "area is needed for the same duty",
                            correct=True,
                        ),
                        opt("It removes the need for cooling water"),
                        opt("It lowers the Reynolds number to zero"),
                    ),
                    "A bigger driving force means a more compact exchanger for the same heat duty.",
                ),
                q(
                    "When scaling a unit operation from pilot to plant, what is held constant to keep the physics the same?",
                    (
                        opt("The absolute size of the equipment"),
                        opt(
                            "The governing dimensionless group (Reynolds, Nusselt or "
                            "Sherwood), so correlations still apply",
                            correct=True,
                        ),
                        opt("The colour of the vessel"),
                        opt("The number of operators"),
                    ),
                    "Match the dimensionless group and geometry and lab data carries to "
                    "full scale - but watch ratios like surface to volume that shift.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

UNIT_OPERATIONS_COURSES: tuple[SeedCourse, ...] = (_UNIT_OPERATIONS,)
