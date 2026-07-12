"""Academy seed content - Air Pollution and Control.

An advanced course on understanding and controlling air pollution: the
structure of the atmosphere and the meteorology that governs pollutant
fate, the main pollutants and their emission sources, atmospheric
stability and Gaussian-plume dispersion, particulate control (cyclones,
baghouses, electrostatic precipitators) and gaseous control (scrubbers,
adsorption), mobile-source emissions, air-quality monitoring and
standards, and indoor air quality. Every lesson is a direct explanation
with a design equation or worked calculation and a mermaid diagram,
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


_AIR_POLLUTION_CONTROL = SeedCourse(
    slug="air-pollution-control",
    title="Air Pollution & Control",
    description=(
        "Understanding and controlling air pollution: sources and pollutants, "
        "atmospheric structure and meteorology, stability and Gaussian-plume "
        "dispersion, particulate control (cyclones, baghouses, electrostatic "
        "precipitators) and gaseous control (scrubbers, adsorption), mobile-source "
        "emissions, monitoring and air-quality standards, and indoor air quality - "
        "with design equations, worked calculations and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Air Pollution and Control

Air pollution is a mass-balance problem played out in a moving,
turbulent fluid. Pollutants are **emitted** from sources, **transported
and diluted** by the atmosphere, **transformed** by chemistry, and finally
**removed** - either by nature or by the control devices we design. This
course follows that chain from source to standard.

The approach is **direct and quantitative**: each lesson explains one
idea clearly, works a real design equation or calculation (a stack-gas
concentration, a Gaussian-plume estimate, a cyclone cut diameter, a
scrubber efficiency), and draws the process as a diagram. After each
lesson there is a short quiz; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Atmospheric structure and meteorology** - the layers and the drivers
2. **Pollutants and emission sources** - what we emit and from where
3. **Atmospheric stability and dispersion** - the Gaussian plume model
4. **Particulate control** - cyclones, baghouses, electrostatic precipitators
5. **Gaseous control** - scrubbers and adsorption
6. **Mobile source emissions** - engines, controls, and fuels
7. **Monitoring and standards** - measuring air quality against limits
8. **Indoor air quality** - the environment where people spend most time

Standards appear throughout - WHO air-quality guidelines, US EPA NAAQS,
and Brazil's CONAMA resolutions and ABNT NBR methods - grounded in real
practice but kept teachable.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "How does this course frame air pollution?",
                    (
                        opt("Purely as a chemistry problem with no physics"),
                        opt(
                            "As a chain from emission to transport and dilution to "
                            "transformation to removal - a mass balance in a moving fluid",
                            correct=True,
                        ),
                        opt("As something only indoor air causes"),
                        opt("As a topic with no measurable standards"),
                    ),
                    "Sources emit, the atmosphere transports and dilutes, chemistry "
                    "transforms, and removal (natural or engineered) closes the balance.",
                ),
                q(
                    "What does each content lesson include besides the explanation?",
                    (
                        opt("Only a list of references"),
                        opt(
                            "A worked design equation or calculation and a mermaid "
                            "diagram of the process",
                            correct=True,
                        ),
                        opt("A full software installation guide"),
                        opt("Nothing beyond prose"),
                    ),
                    "Every lesson pairs a concrete calculation with a diagram so the "
                    "concept is both quantitative and visual.",
                ),
            ),
        ),
        # -- 1. Atmosphere & meteorology -------------------------------
        _t(
            "Atmospheric structure and meteorology",
            "10 min",
            """# Atmospheric structure and meteorology

Pollution behaves according to *where* in the atmosphere it lives and
*how* the air moves. The atmosphere is layered by its **temperature
profile**:

- **Troposphere** (surface to about 10-15 km) - where weather and almost
  all air pollution occur; temperature normally falls with height.
- **Stratosphere** (up to about 50 km) - holds the ozone layer;
  temperature *rises* with height, which suppresses vertical mixing.
- **Mesosphere** and **thermosphere** - higher still, minor for pollution.

The layer that matters most for control is the **atmospheric boundary
layer (ABL)** - the lowest few hundred to a couple thousand metres, where
the surface directly stirs the air. Its depth, the **mixing height**,
sets the volume available to dilute emissions: a shallow mixing height
traps pollutants near the ground.

The key thermodynamic idea is the **dry adiabatic lapse rate** - how fast
a rising parcel of dry air cools as it expands. It is essentially
constant:

```text
Dry adiabatic lapse rate:
  Gamma_d = g / c_p
          = 9.81 (m/s^2) / 1005 (J/kg-K)
          = 0.00976 K/m  ~ 9.8 degC per 1000 m

Compare with the measured environmental lapse rate (ELR):
  ELR > Gamma_d  -> unstable  (parcel keeps rising, good mixing)
  ELR < Gamma_d  -> stable    (parcel sinks back, poor mixing)
  ELR = 0 or < 0 -> inversion (very stable, pollutants trapped)
```

Comparing the measured **environmental lapse rate** with the adiabatic
rate tells you whether the air resists or encourages vertical motion -
the single biggest control on how quickly emissions dilute. Wind speed,
solar heating, and terrain complete the picture.

```mermaid
graph TD
    SUN["Solar heating of surface"] --> ABL["Boundary layer mixing"]
    ABL --> MIX["Mixing height sets dilution volume"]
    LAPSE["Environmental lapse rate"] --> STAB["Stability of the air"]
    STAB --> MIX
    MIX --> CONC["Ground level concentration"]
```

Remember: the atmosphere is the reactor and the diluter. Its temperature
profile and mixing height decide whether a given emission becomes a
nuisance or disperses harmlessly.
""",
        ),
        quiz_lesson(
            "Quiz: Atmospheric structure and meteorology",
            (
                q(
                    "In which atmospheric layer does almost all air pollution occur?",
                    (
                        opt("The stratosphere"),
                        opt("The mesosphere"),
                        opt(
                            "The troposphere - the lowest layer, where weather happens",
                            correct=True,
                        ),
                        opt("The thermosphere"),
                    ),
                    "The troposphere (surface to about 10-15 km) contains weather and "
                    "nearly all emissions; temperature normally falls with height there.",
                ),
                q(
                    "What is the approximate dry adiabatic lapse rate?",
                    (
                        opt("About 0.65 degC per 1000 m"),
                        opt("About 9.8 degC per 1000 m (g divided by c_p)", correct=True),
                        opt("About 100 degC per 1000 m"),
                        opt("Zero - temperature never changes with height"),
                    ),
                    "Gamma_d = g / c_p = 9.81 / 1005 = 0.00976 K/m, about 9.8 degC per km.",
                ),
                q(
                    "Why does a shallow mixing height worsen ground-level pollution?",
                    (
                        opt("It increases the wind speed"),
                        opt(
                            "It shrinks the air volume available to dilute emissions, so "
                            "concentrations near the ground rise",
                            correct=True,
                        ),
                        opt("It removes all sources of emission"),
                        opt("It has no effect on concentration"),
                    ),
                    "The mixing height sets the dilution volume; a low ceiling traps "
                    "pollutants near the surface.",
                ),
            ),
        ),
        # -- 2. Pollutants & sources -----------------------------------
        _t(
            "Pollutants and emission sources",
            "10 min",
            """# Pollutants and emission sources

Air pollutants split into two families. **Primary pollutants** are
emitted directly; **secondary pollutants** form in the atmosphere from
reactions among primaries. The regulated **criteria pollutants** (the ones
with health-based ambient standards) are the core set:

- **Particulate matter (PM10, PM2.5)** - solid and liquid particles;
  PM2.5 penetrates deep into the lungs and is the largest health burden.
- **Sulfur dioxide (SO2)** - from burning sulfur-bearing fuels; drives
  acid deposition.
- **Nitrogen oxides (NOx = NO + NO2)** - from high-temperature combustion.
- **Carbon monoxide (CO)** - from incomplete combustion.
- **Ozone (O3)** - a *secondary* pollutant formed when NOx and volatile
  organic compounds react in sunlight (photochemical smog).
- **Lead (Pb)** - now largely controlled after leaded-fuel phaseouts.

Sources are categorized as **point** (a single stack), **area** (many
small diffuse sources, e.g. residential heating), **mobile** (vehicles),
and **natural** (dust, volcanoes, biogenic VOCs).

Engineers quantify emissions with **emission factors** - a mass of
pollutant per unit of activity (US EPA compiles these in AP-42):

```text
Emission rate estimate:
  E = A * EF * (1 - eta/100)

  E   = emission rate (kg/yr)
  A   = activity level (e.g. tonnes fuel burned per year)
  EF  = emission factor (kg pollutant per tonne activity)
  eta = overall control efficiency (percent)

Worked example - SO2 from fuel oil:
  A  = 5000 tonnes/yr,  EF = 18 kg SO2 per tonne (2 percent S oil)
  eta = 90 percent scrubber
  E = 5000 * 18 * (1 - 0.90) = 9000 kg SO2 per year
```

```mermaid
graph LR
    POINT["Point sources stacks"] --> AMB["Ambient air"]
    AREA["Area sources diffuse"] --> AMB
    MOBILE["Mobile sources vehicles"] --> AMB
    NAT["Natural sources"] --> AMB
    AMB --> PRIM["Primary pollutants"]
    PRIM --> SEC["Secondary ozone and smog"]
```

Remember: know the pollutant family, the source type, and the emission
factor. Together they turn "we burn fuel" into a defensible kilograms-per-
year inventory - the starting point for any control design.
""",
        ),
        quiz_lesson(
            "Quiz: Pollutants and emission sources",
            (
                q(
                    "Which of these is a secondary pollutant?",
                    (
                        opt("Sulfur dioxide emitted from a stack"),
                        opt(
                            "Ground-level ozone, formed when NOx and VOCs react in sunlight",
                            correct=True,
                        ),
                        opt("Carbon monoxide from incomplete combustion"),
                        opt("Primary particulate matter from a diesel exhaust"),
                    ),
                    "Ozone is not emitted directly; it forms in the atmosphere from "
                    "photochemical reactions of NOx and VOCs.",
                ),
                q(
                    "What is an emission factor?",
                    (
                        opt("The legal fine per tonne of pollutant"),
                        opt(
                            "A mass of pollutant emitted per unit of activity, used to "
                            "estimate emission rates",
                            correct=True,
                        ),
                        opt("The temperature of the stack gas"),
                        opt("The wind speed at the source"),
                    ),
                    "Emission factors (e.g. from EPA AP-42) give kg pollutant per unit "
                    "of fuel or product, enabling inventory estimates.",
                ),
                q(
                    "Using E = A * EF * (1 - eta/100), what is the emission if A = 5000 "
                    "t/yr, EF = 18 kg/t, and eta = 90 percent?",
                    (
                        opt("90000 kg/yr"),
                        opt("9000 kg/yr", correct=True),
                        opt("900 kg/yr"),
                        opt("18000 kg/yr"),
                    ),
                    "5000 * 18 * (1 - 0.90) = 90000 * 0.10 = 9000 kg/yr.",
                ),
            ),
        ),
        # -- 3. Stability & dispersion ---------------------------------
        _t(
            "Atmospheric stability and dispersion",
            "11 min",
            """# Atmospheric stability and dispersion

Once emitted from a stack, a plume is carried downwind and spread by
turbulence. **Atmospheric stability** governs how fast it spreads. The
classic **Pasquill-Gifford stability classes** run from A (very unstable,
strong daytime mixing) through D (neutral) to F (very stable, calm
night). Each class maps to dispersion coefficients.

The workhorse model is the **Gaussian plume equation**, which assumes the
downwind concentration spreads as a normal distribution in the crosswind
(y) and vertical (z) directions:

```text
Gaussian plume (continuous point source, with ground reflection):

  C(x,y,z) = ( Q / (2*pi*u*sigma_y*sigma_z) )
             * exp( -y^2 / (2*sigma_y^2) )
             * [ exp( -(z-H)^2 / (2*sigma_z^2) )
               + exp( -(z+H)^2 / (2*sigma_z^2) ) ]

  C       = concentration (g/m^3)
  Q       = source strength (g/s)
  u       = wind speed at stack height (m/s)
  sigma_y, sigma_z = dispersion coefficients (m), depend on x and stability
  H       = effective stack height (m) = physical height + plume rise
  y, z    = crosswind and vertical distance from plume centerline
```

For the **ground-level centerline** (y = 0, z = 0), it simplifies to:

```text
  C(x,0,0) = ( Q / (pi*u*sigma_y*sigma_z) ) * exp( -H^2 / (2*sigma_z^2) )
```

Two design levers fall straight out of this: a **taller effective stack H**
sharply lowers ground concentration, and **higher wind speed u** dilutes
the plume. Plume rise itself (from buoyancy and momentum) adds to the
physical height and is often estimated with **Briggs equations**.

Regulatory practice uses computer models built on this physics - **AERMOD**
is the US EPA preferred steady-state Gaussian model - to demonstrate
compliance with ambient standards.

```mermaid
graph LR
    STACK["Stack emission Q"] --> RISE["Plume rise adds to height"]
    RISE --> H["Effective height H"]
    STAB["Stability class A to F"] --> SIG["Dispersion coefficients"]
    WIND["Wind speed u"] --> DISP["Downwind dilution"]
    H --> DISP
    SIG --> DISP
    DISP --> GLC["Ground level concentration"]
```

Remember: the Gaussian plume ties source strength, wind, stability, and
stack height into one estimate of downwind concentration - the equation
behind most permit calculations.
""",
        ),
        quiz_lesson(
            "Quiz: Atmospheric stability and dispersion",
            (
                q(
                    "In the Pasquill-Gifford scheme, what does stability class A represent?",
                    (
                        opt("Very stable, calm night conditions"),
                        opt(
                            "Very unstable conditions with strong daytime mixing",
                            correct=True,
                        ),
                        opt("Neutral conditions"),
                        opt("An atmospheric inversion"),
                    ),
                    "Classes run A (very unstable, strong mixing) through D (neutral) to "
                    "F (very stable); A disperses plumes fastest.",
                ),
                q(
                    "In the Gaussian plume model, what does the effective stack height H "
                    "represent?",
                    (
                        opt("Only the physical height of the chimney"),
                        opt(
                            "The physical stack height plus the plume rise from buoyancy "
                            "and momentum",
                            correct=True,
                        ),
                        opt("The wind speed at the top of the stack"),
                        opt("The distance to the nearest receptor"),
                    ),
                    "H = physical height + plume rise; a larger H sharply reduces "
                    "ground-level concentration.",
                ),
                q(
                    "According to the ground-level centerline equation, how does raising "
                    "the effective stack height H affect ground concentration?",
                    (
                        opt("It increases ground-level concentration"),
                        opt(
                            "It decreases it - H appears in exp(-H^2 / (2 sigma_z^2)), so "
                            "a larger H lowers the ground value",
                            correct=True,
                        ),
                        opt("It has no effect at all"),
                        opt("It only changes the crosswind spread"),
                    ),
                    "The exponential term exp(-H^2 / (2 sigma_z^2)) shrinks as H grows, "
                    "so taller effective stacks cut ground-level concentration.",
                ),
            ),
        ),
        # -- 4. Particulate control ------------------------------------
        _t(
            "Particulate control - cyclones, baghouses, precipitators",
            "11 min",
            """# Particulate control - cyclones, baghouses, precipitators

To remove particles from a gas stream, engineers pick a device based on
the **particle size**, the **loading**, the **temperature**, and the
required **efficiency**. Three families dominate.

**Cyclones** spin the gas so inertia flings particles to the wall. They
are cheap and rugged but only good for coarse particles (roughly above
5-10 micrometres). Their key spec is the **cut diameter** - the size
collected at 50 percent efficiency:

```text
Cyclone cut diameter (Lapple):
  d_pc = sqrt( 9 * mu * W / (2 * pi * N_e * v_i * (rho_p - rho_g)) )

  mu    = gas viscosity (kg/m-s)
  W     = inlet width (m)
  N_e   = effective number of turns (typically about 5)
  v_i   = inlet gas velocity (m/s)
  rho_p, rho_g = particle and gas density (kg/m^3)

Smaller d_pc means finer particles are captured.
```

**Baghouses (fabric filters)** pass the gas through cloth bags; a **dust
cake** builds up and does most of the filtering, reaching over 99 percent
even on fine particles. The design metric is the **air-to-cloth ratio**
(filtration velocity):

```text
  Air-to-cloth ratio = Q / A_cloth   (m/min or m3/min per m2)
  Lower ratio -> lower pressure drop and longer bag life.
```

**Electrostatic precipitators (ESPs)** charge particles in a corona field
and collect them on grounded plates. Efficiency follows the
**Deutsch-Anderson equation**:

```text
  eta = 1 - exp( - w * A / Q )

  w = drift (migration) velocity of charged particles (m/s)
  A = total collecting plate area (m^2)
  Q = gas volumetric flow rate (m^3/s)

Doubling A does not double the penetration - efficiency approaches 100
percent only asymptotically.
```

```mermaid
graph LR
    GAS["Dusty gas stream"] --> CYC["Cyclone coarse particles"]
    CYC --> ESP["Precipitator or baghouse fine particles"]
    ESP --> CLEAN["Cleaned gas to stack"]
    ESP --> HOP["Collected dust to hopper"]
```

Remember: match the device to the particle size. Cyclones knock out the
coarse load cheaply; baghouses and ESPs polish the fine fraction to high
efficiency - often staged in series.
""",
        ),
        quiz_lesson(
            "Quiz: Particulate control - cyclones, baghouses, precipitators",
            (
                q(
                    "What is a cyclone's 'cut diameter'?",
                    (
                        opt("The diameter of the cyclone body"),
                        opt(
                            "The particle size collected at 50 percent efficiency",
                            correct=True,
                        ),
                        opt("The largest particle the cyclone can hold"),
                        opt("The diameter of the outlet pipe"),
                    ),
                    "The cut diameter d_pc is the size captured at 50 percent efficiency; "
                    "a smaller d_pc means finer particles are collected.",
                ),
                q(
                    "The Deutsch-Anderson equation eta = 1 - exp(-wA/Q) describes which device?",
                    (
                        opt("A cyclone"),
                        opt("A fabric filter baghouse"),
                        opt("An electrostatic precipitator", correct=True),
                        opt("A wet scrubber"),
                    ),
                    "Deutsch-Anderson relates ESP efficiency to drift velocity w, plate "
                    "area A, and gas flow Q.",
                ),
                q(
                    "Why are cyclones usually placed before a baghouse or ESP rather than "
                    "used alone?",
                    (
                        opt("They are the most efficient on fine particles"),
                        opt(
                            "They cheaply remove the coarse load, leaving the fine "
                            "fraction for the high-efficiency device downstream",
                            correct=True,
                        ),
                        opt("They cool the gas below the dew point"),
                        opt("They charge the particles electrically"),
                    ),
                    "Cyclones handle coarse particles cheaply; staging them ahead of a "
                    "baghouse or ESP protects and offloads the finishing device.",
                ),
            ),
        ),
        # -- 5. Gaseous control ----------------------------------------
        _t(
            "Gaseous control - scrubbers and adsorption",
            "11 min",
            """# Gaseous control - scrubbers and adsorption

Removing *gaseous* pollutants (SO2, HCl, H2S, VOCs) is a mass-transfer
problem: move the molecule from the gas phase into a liquid or onto a
solid. Two approaches dominate.

**Absorption (wet scrubbing)** contacts the gas with a liquid that
dissolves or reacts with the pollutant. In a **packed tower**, gas rises
counter-current to a falling scrubbing liquid over packing that maximizes
contact area. For SO2, a **limestone or lime slurry** neutralizes the acid
gas - the basis of **flue-gas desulfurization (FGD)**:

```text
Wet FGD reaction (limestone):
  SO2 + CaCO3 + 1/2 O2 + 2 H2O  ->  CaSO4 . 2H2O + CO2
                                     (gypsum, a saleable byproduct)

Absorber sizing uses the transfer-unit concept:
  Height of packing Z = HTU * NTU
  HTU = height of a transfer unit (m)
  NTU = number of transfer units ~ ln(C_in / C_out) for dilute gas
```

The equilibrium that limits absorption is described by **Henry's law** -
the gas concentration a liquid can hold is proportional to its partial
pressure:

```text
  p_A = H * x_A
  p_A = partial pressure of solute in gas (atm)
  H   = Henry's law constant (atm per mole fraction)
  x_A = mole fraction in liquid
Low H (very soluble gas) makes absorption easy.
```

**Adsorption** binds molecules onto the surface of a solid - most often
**activated carbon** for VOCs and odors, or zeolites. It excels at low
concentrations and can recover solvent. The bed saturates over time,
tracked by a **breakthrough curve**; the spent carbon is then regenerated
(steam or thermal) or replaced.

```mermaid
graph LR
    GAS["Gas with SO2 or VOC"] --> ABS["Absorber packed tower"]
    ABS --> CLEAN["Cleaned gas"]
    ABS --> LIQ["Spent scrubbing liquid"]
    GAS --> ADS["Adsorber carbon bed"]
    ADS --> REGEN["Regenerate or replace carbon"]
```

Remember: absorption suits soluble or reactive gases at higher loads and
often makes a byproduct (gypsum); adsorption suits dilute VOCs and odors
and can recover the captured compound. Choose by solubility, concentration,
and whether you want recovery.
""",
        ),
        quiz_lesson(
            "Quiz: Gaseous control - scrubbers and adsorption",
            (
                q(
                    "What does Henry's law (p_A = H * x_A) tell a scrubber designer?",
                    (
                        opt("The pressure drop across the packing"),
                        opt(
                            "How much of the gas a liquid can hold at equilibrium - a low "
                            "H means a very soluble gas, easy to absorb",
                            correct=True,
                        ),
                        opt("The number of bags in a baghouse"),
                        opt("The drift velocity of charged particles"),
                    ),
                    "Henry's law sets the gas-liquid equilibrium; soluble gases (low H) "
                    "are readily absorbed.",
                ),
                q(
                    "In wet flue-gas desulfurization with limestone, what useful "
                    "byproduct is produced?",
                    (
                        opt("Elemental sulfur"),
                        opt("Gypsum (calcium sulfate dihydrate)", correct=True),
                        opt("Activated carbon"),
                        opt("Nitric acid"),
                    ),
                    "SO2 + CaCO3 + O2 + water yields gypsum (CaSO4.2H2O), which can be "
                    "sold for wallboard.",
                ),
                q(
                    "Which technology is best suited to removing dilute VOCs and odors, "
                    "with possible solvent recovery?",
                    (
                        opt("A cyclone"),
                        opt("An electrostatic precipitator"),
                        opt(
                            "Adsorption onto activated carbon, tracked by a breakthrough curve",
                            correct=True,
                        ),
                        opt("A settling chamber"),
                    ),
                    "Activated-carbon adsorption excels at low concentrations, and the "
                    "captured compound can often be recovered on regeneration.",
                ),
            ),
        ),
        # -- 6. Mobile source emissions --------------------------------
        _t(
            "Mobile source emissions",
            "10 min",
            """# Mobile source emissions

Vehicles are the dominant source of urban NOx, CO, and much of the VOC
and fine-particle burden. The pollutants come from the combustion
chemistry itself: **CO** and **unburned hydrocarbons (HC)** from
incomplete combustion, **NOx** from nitrogen fixed at high flame
temperatures, and **PM** especially from diesel engines.

The central control on gasoline engines is the **three-way catalytic
converter**, which does three jobs at once - only if the air-fuel mixture
is held near the **stoichiometric** point by an oxygen sensor and
closed-loop fuel control:

```text
Three-way catalyst reactions:
  Oxidation:   2 CO  + O2    -> 2 CO2
               HC    + O2    -> CO2 + H2O
  Reduction:   2 NO  + 2 CO  -> N2 + 2 CO2

Stoichiometric air-fuel ratio for gasoline ~ 14.7 : 1 (by mass)
The lambda sensor keeps the mixture at lambda = 1 so the catalyst can
oxidize CO and HC while reducing NOx simultaneously.
```

Diesel engines run lean, so they need different aftertreatment: a
**diesel particulate filter (DPF)** to trap soot and **selective catalytic
reduction (SCR)** injecting urea (AdBlue) to convert NOx to nitrogen:

```text
SCR reaction (urea provides ammonia):
  4 NO + 4 NH3 + O2 -> 4 N2 + 6 H2O
```

Standards tighten over generations - **Euro 1 through Euro 6/7** in Europe
and **PROCONVE (L and P phases)** in Brazil - and are verified on
standardized **drive cycles** (WLTP, real-driving emissions). Fuel quality
(low sulfur, ethanol blends) and fleet electrification cut the burden
further.

```mermaid
graph LR
    ENG["Engine combustion"] --> RAW["Raw CO HC NOx PM"]
    RAW --> TWC["Three way catalyst gasoline"]
    RAW --> DPF["Particulate filter diesel"]
    DPF --> SCR["SCR urea reduces NOx"]
    TWC --> TAIL["Tailpipe within standard"]
    SCR --> TAIL
```

Remember: gasoline control hinges on holding stoichiometry so a three-way
catalyst works; diesel needs a filter for soot plus SCR for NOx. Standards
and drive cycles enforce it, and cleaner fuels plus electrification shrink
the source.
""",
        ),
        quiz_lesson(
            "Quiz: Mobile source emissions",
            (
                q(
                    "Why must a gasoline engine hold the air-fuel mixture near "
                    "stoichiometric (lambda = 1)?",
                    (
                        opt("To maximize fuel consumption"),
                        opt(
                            "So the three-way catalyst can oxidize CO and HC while "
                            "reducing NOx at the same time",
                            correct=True,
                        ),
                        opt("To keep the engine cold"),
                        opt("Because diesel engines require it"),
                    ),
                    "The three-way catalyst only performs all three reactions in a narrow "
                    "window around lambda = 1, held by the oxygen sensor.",
                ),
                q(
                    "How do diesel engines control NOx, since they run lean?",
                    (
                        opt("With a three-way catalyst alone"),
                        opt(
                            "Selective catalytic reduction (SCR), injecting urea so "
                            "ammonia converts NOx to nitrogen",
                            correct=True,
                        ),
                        opt("By adding lead to the fuel"),
                        opt("By running richer than stoichiometric"),
                    ),
                    "Lean diesel exhaust needs SCR: 4 NO + 4 NH3 + O2 -> 4 N2 + 6 H2O, "
                    "with a DPF for soot.",
                ),
                q(
                    "What are Euro 6 and Brazil's PROCONVE examples of?",
                    (
                        opt("Fuel brand names"),
                        opt(
                            "Progressively tightening vehicle emission standards, "
                            "verified on standardized drive cycles",
                            correct=True,
                        ),
                        opt("Types of catalytic converter metal"),
                        opt("Names of atmospheric stability classes"),
                    ),
                    "They are regulatory standards that tighten over generations and are "
                    "checked on drive cycles such as WLTP.",
                ),
            ),
        ),
        # -- 7. Monitoring & standards ---------------------------------
        _t(
            "Air quality monitoring and standards",
            "10 min",
            """# Air quality monitoring and standards

You cannot manage what you do not measure. **Ambient air-quality
monitoring** compares measured concentrations against **health-based
standards** to protect the public and to trigger action.

Measurement methods span a range of cost and accuracy:

- **Reference (regulatory) monitors** - gravimetric filters for PM,
  chemiluminescence for NOx, UV fluorescence for SO2, non-dispersive
  infrared for CO. Accurate but expensive and sparse.
- **Low-cost sensors** - optical PM sensors and electrochemical gas
  sensors give dense, real-time coverage but need calibration.
- **Remote sensing** - satellite instruments (e.g. Sentinel-5P TROPOMI)
  map pollutants like NO2 over whole regions.

Standards set the limits. The **US EPA NAAQS**, **WHO air-quality
guidelines** (tightened in 2021), and Brazil's **CONAMA Resolution 491/2018**
specify concentration limits over averaging periods. For example, WHO 2021
sets PM2.5 at 5 ug/m3 annual and 15 ug/m3 for 24 hours.

To communicate risk, agencies collapse several pollutants into one **Air
Quality Index (AQI)** using linear interpolation between breakpoints:

```text
AQI (piecewise linear interpolation for a pollutant):

  AQI = ( (I_hi - I_lo) / (C_hi - C_lo) ) * (C - C_lo) + I_lo

  C            = measured concentration
  C_lo, C_hi   = concentration breakpoints bracketing C
  I_lo, I_hi   = index values at those breakpoints

The reported AQI is the maximum across all measured pollutants.
```

Data quality hinges on siting, calibration, and completeness. Reference
methods are defined by standards bodies (US EPA reference methods, ABNT
NBR procedures) so results are comparable across networks.

```mermaid
graph LR
    AMB["Ambient air"] --> MON["Monitors reference and low cost"]
    SAT["Satellite remote sensing"] --> DATA["Air quality data"]
    MON --> DATA
    DATA --> COMP["Compare to standards"]
    COMP --> AQI["Air quality index"]
    AQI --> ACTION["Public alert and control action"]
```

Remember: match the method to the need, calibrate relentlessly, and judge
the numbers against a defined standard. The AQI turns raw concentrations
into a message the public can act on.
""",
        ),
        quiz_lesson(
            "Quiz: Air quality monitoring and standards",
            (
                q(
                    "How is the reported Air Quality Index chosen when several pollutants "
                    "are measured?",
                    (
                        opt("It is the average of all pollutant sub-indices"),
                        opt(
                            "It is the maximum sub-index across all measured pollutants",
                            correct=True,
                        ),
                        opt("It is the minimum sub-index"),
                        opt("It is always based only on ozone"),
                    ),
                    "The AQI takes the worst (maximum) pollutant sub-index so the message "
                    "reflects the dominant risk.",
                ),
                q(
                    "What is a trade-off of low-cost air-quality sensors versus reference "
                    "monitors?",
                    (
                        opt("They are more accurate but slower"),
                        opt(
                            "They give dense, real-time coverage but need careful "
                            "calibration to be reliable",
                            correct=True,
                        ),
                        opt("They cannot measure any pollutant"),
                        opt("They only work on satellites"),
                    ),
                    "Low-cost sensors trade some accuracy for spatial and temporal "
                    "density; calibration against reference methods is essential.",
                ),
                q(
                    "What do WHO guidelines, US EPA NAAQS, and Brazil's CONAMA Resolution "
                    "491/2018 have in common?",
                    (
                        opt("They are all vehicle drive cycles"),
                        opt(
                            "They set health-based ambient concentration limits over "
                            "defined averaging periods",
                            correct=True,
                        ),
                        opt("They define particle cut diameters for cyclones"),
                        opt("They are Henry's law constants"),
                    ),
                    "All three specify ambient air-quality standards (limit plus "
                    "averaging time) that monitoring is judged against.",
                ),
            ),
        ),
        # -- 8. Indoor air quality -------------------------------------
        _t(
            "Indoor air quality",
            "10 min",
            """# Indoor air quality

People spend roughly 90 percent of their time indoors, so indoor
concentrations often matter more to actual exposure than outdoor levels.
Indoor air has its own sources: **combustion** (gas stoves, unvented
heaters producing CO and NO2), **building materials and furnishings**
(formaldehyde and other VOCs off-gassing), **biological agents** (mold,
dust mites), **radon** seeping from soil, and **outdoor air brought in**.

The central engineering control is **ventilation** - diluting and removing
indoor pollutants with outdoor air. A simple **steady-state mass balance**
on a well-mixed room gives the indoor concentration:

```text
Well-mixed room mass balance at steady state:

  C_in = C_out + S / (Q_vent)

  C_in  = indoor concentration
  C_out = outdoor (supply) concentration
  S     = indoor emission rate (mass/time)
  Q_vent = ventilation rate (volume/time)

Ventilation is often expressed as air changes per hour:
  ACH = Q_vent / V_room   (room volumes exchanged per hour)
Higher ACH lowers C_in for a given indoor source S.
```

Standards guide the design: **ASHRAE Standard 62.1** sets minimum
ventilation rates, and WHO indoor guidelines cover CO, formaldehyde, and
radon. But ventilation trades off against **energy** - conditioning
outdoor air costs energy, so modern practice uses **demand-controlled
ventilation** (often driven by a CO2 sensor as a proxy for occupancy) and
**heat-recovery ventilators**.

Where ventilation is not enough, **filtration** cleans recirculated air -
**HEPA** filters for particles, activated carbon for gases. The COVID era
sharpened focus on **airborne transmission**, adding filtration and higher
ventilation as infection controls.

```mermaid
graph TD
    SRC["Indoor sources VOC CO radon mold"] --> ROOM["Room air concentration"]
    VENT["Ventilation outdoor air"] --> ROOM
    ROOM --> FILT["Filtration HEPA and carbon"]
    FILT --> ROOM
    ROOM --> EXP["Human exposure"]
    ENERGY["Energy cost of conditioning air"] --> VENT
```

Remember: indoor exposure dominates total exposure. Control it by cutting
sources, ventilating enough (balanced against energy), and filtering what
remains - the same source-transport-removal logic, applied to the room
you are sitting in.
""",
        ),
        quiz_lesson(
            "Quiz: Indoor air quality",
            (
                q(
                    "In the well-mixed room balance C_in = C_out + S / Q_vent, how does "
                    "raising the ventilation rate Q_vent affect indoor concentration?",
                    (
                        opt("It raises C_in"),
                        opt(
                            "It lowers C_in, because the indoor source term S / Q_vent "
                            "shrinks as Q_vent grows",
                            correct=True,
                        ),
                        opt("It has no effect on C_in"),
                        opt("It only changes the outdoor concentration"),
                    ),
                    "More ventilation dilutes the indoor source: the S / Q_vent term "
                    "falls, so C_in approaches C_out.",
                ),
                q(
                    "Why is indoor air quality so important to overall exposure?",
                    (
                        opt("Indoor air is always cleaner than outdoor air"),
                        opt(
                            "People spend roughly 90 percent of their time indoors, so "
                            "indoor concentrations dominate real exposure",
                            correct=True,
                        ),
                        opt("Indoor air has no pollution sources"),
                        opt("Standards ignore indoor air entirely"),
                    ),
                    "Because most time is spent indoors, indoor concentrations often "
                    "matter more to actual exposure than ambient outdoor levels.",
                ),
                q(
                    "What is the main trade-off when increasing ventilation for indoor "
                    "air quality?",
                    (
                        opt("It always makes the air dirtier"),
                        opt(
                            "Conditioning more outdoor air costs energy, which is why "
                            "demand-controlled ventilation and heat recovery are used",
                            correct=True,
                        ),
                        opt("It requires removing all windows"),
                        opt("It has no downside at all"),
                    ),
                    "Ventilation dilutes pollutants but costs energy to heat or cool the "
                    "incoming air; demand control and heat recovery manage that trade-off.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the approximate dry adiabatic lapse rate, and why does it matter?",
                    (
                        opt("About 100 degC per km; it sets the wind speed"),
                        opt(
                            "About 9.8 degC per km (g / c_p); comparing it to the "
                            "environmental lapse rate tells you the air's stability",
                            correct=True,
                        ),
                        opt("Zero; temperature never varies with height"),
                        opt("About 0.5 degC per km; it sets the ozone concentration"),
                    ),
                    "Gamma_d ~ 9.8 degC/km; if the environmental lapse rate exceeds it "
                    "the air is unstable (good mixing), if less it is stable.",
                ),
                q(
                    "Ground-level ozone is best described as:",
                    (
                        opt("A primary pollutant emitted directly from stacks"),
                        opt(
                            "A secondary pollutant formed from NOx and VOCs reacting in sunlight",
                            correct=True,
                        ),
                        opt("An inert gas with no health effect"),
                        opt("A particulate matter fraction"),
                    ),
                    "Ozone forms photochemically in the atmosphere - it is the classic "
                    "secondary pollutant of urban smog.",
                ),
                q(
                    "In the Gaussian plume model, raising the effective stack height H:",
                    (
                        opt("increases ground-level concentration"),
                        opt(
                            "decreases ground-level concentration, via the exp(-H^2 / "
                            "(2 sigma_z^2)) term",
                            correct=True,
                        ),
                        opt("has no effect on ground concentration"),
                        opt("changes only the source strength Q"),
                    ),
                    "A larger H shrinks the exponential term, lowering the ground-level "
                    "centerline concentration.",
                ),
                q(
                    "The Deutsch-Anderson equation eta = 1 - exp(-wA/Q) is used to size "
                    "which device?",
                    (
                        opt("A packed absorption tower"),
                        opt("An electrostatic precipitator", correct=True),
                        opt("A three-way catalytic converter"),
                        opt("A HEPA filter"),
                    ),
                    "Deutsch-Anderson gives ESP efficiency from drift velocity w, plate "
                    "area A, and gas flow Q.",
                ),
                q(
                    "Which device is the cheap, rugged first stage for removing coarse particles?",
                    (
                        opt("An electrostatic precipitator"),
                        opt("A cyclone", correct=True),
                        opt("An activated-carbon adsorber"),
                        opt("A packed scrubbing tower"),
                    ),
                    "Cyclones use inertia to fling coarse particles to the wall; they are "
                    "often staged ahead of a baghouse or ESP.",
                ),
                q(
                    "Henry's law (p_A = H * x_A) governs the design of:",
                    (
                        opt("A cyclone's cut diameter"),
                        opt(
                            "Gas absorption in a scrubber - how much pollutant the liquid "
                            "can hold at equilibrium",
                            correct=True,
                        ),
                        opt("The drive cycle of a vehicle"),
                        opt("The mixing height of the boundary layer"),
                    ),
                    "Henry's law sets the gas-liquid equilibrium; low H means a soluble "
                    "gas that absorbs readily.",
                ),
                q(
                    "A three-way catalytic converter needs the engine held near "
                    "stoichiometric because:",
                    (
                        opt(
                            "it lets the catalyst oxidize CO and HC while reducing NOx at once",
                            correct=True,
                        ),
                        opt("it maximizes soot production"),
                        opt("diesel engines demand a rich mixture"),
                        opt("it cools the exhaust gas"),
                    ),
                    "All three catalyst reactions only proceed together in a narrow "
                    "window around lambda = 1.",
                ),
                q(
                    "Which technology treats NOx in lean diesel exhaust?",
                    (
                        opt("A three-way catalyst alone"),
                        opt(
                            "Selective catalytic reduction (SCR) with urea-derived ammonia",
                            correct=True,
                        ),
                        opt("A cyclone"),
                        opt("A HEPA filter"),
                    ),
                    "SCR converts NOx to nitrogen (4 NO + 4 NH3 + O2 -> 4 N2 + 6 H2O), "
                    "paired with a diesel particulate filter for soot.",
                ),
                q(
                    "When several pollutants are measured, the reported Air Quality Index is:",
                    (
                        opt("the average of the sub-indices"),
                        opt("the maximum sub-index across all pollutants", correct=True),
                        opt("always the ozone value"),
                        opt("the minimum sub-index"),
                    ),
                    "The AQI reports the worst pollutant so the public message reflects "
                    "the dominant risk.",
                ),
                q(
                    "In a well-mixed room, C_in = C_out + S / Q_vent. Raising Q_vent "
                    "(more ventilation):",
                    (
                        opt("increases the indoor concentration"),
                        opt(
                            "lowers the indoor concentration, at the cost of energy to "
                            "condition the incoming air",
                            correct=True,
                        ),
                        opt("has no effect indoors"),
                        opt("only changes the outdoor concentration"),
                    ),
                    "More ventilation dilutes the indoor source (S / Q_vent falls) but "
                    "costs energy - hence demand-controlled ventilation and heat recovery.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

AIR_POLLUTION_CONTROL_COURSES: tuple[SeedCourse, ...] = (_AIR_POLLUTION_CONTROL,)
