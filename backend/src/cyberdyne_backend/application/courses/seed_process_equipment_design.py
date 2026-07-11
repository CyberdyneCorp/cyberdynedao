"""Academy seed content - Process Equipment Design.

Sizing and specifying the hardware of a chemical plant: pressure vessels,
shell-and-tube heat exchangers, distillation column internals, storage
tanks, piping and pumps, and reactors - to the codes that govern them
(ASME BPVC, TEMA, API) and with materials and corrosion in mind. Every
lesson is a direct explanation with a mechanical/process diagram and a
worked design calculation, followed by a checkpoint quiz; the course
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


_PROCESS_EQUIPMENT_DESIGN = SeedCourse(
    slug="process-equipment-design",
    title="Process Equipment Design",
    description=(
        "Sizing and specifying the hardware of a chemical plant - pressure "
        "vessels, heat exchangers, columns, tanks, pumps and reactors - to "
        "code, with materials and corrosion in mind. Every lesson pairs a "
        "direct explanation and a mechanical diagram with a worked design "
        "calculation grounded in ASME BPVC, TEMA and API practice."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Process Equipment Design

A process flowsheet tells you *what* has to happen - separate, heat,
react, store, move. **Equipment design** turns each of those duties into
real hardware: a vessel with a wall thick enough to hold the pressure, a
heat exchanger with enough tubes to move the heat, a column with the right
trays, a pump that beats the system curve. This course is about that
translation, done **to code and with materials in mind**.

The approach is **calculation-first**: every lesson explains one class of
equipment directly, draws its mechanical or process structure as a
diagram, and works one real sizing calculation - the kind you would later
confirm in **Aspen**, **HYSYS** or a vendor datasheet. After each lesson
there is a short quiz; at the end, a final quiz covers the whole course.

What you will learn to size and specify, in order:

1. **Pressure vessels** - wall thickness to the ASME Boiler and Pressure
   Vessel Code
2. **Shell-and-tube heat exchangers** - area, LMTD and TEMA layout
3. **Distillation column internals** - trays, packing and diameter
4. **Storage tanks and vessels** - atmospheric and low-pressure storage
5. **Piping and pumps** - line sizing and the pump you need
6. **Reactor vessels** - volume, residence time and heat removal
7. **Materials and corrosion** - choosing metals that survive the service
8. **Mechanical integrity and codes** - the standards that govern it all

Throughout, remember the two questions every design answers: *is it big
enough to do the duty?* and *is it strong enough and durable enough to do
it safely for the plant's life?*
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does 'equipment design' add on top of a process flowsheet?",
                    (
                        opt("Nothing - the flowsheet already specifies the hardware"),
                        opt(
                            "It turns each process duty into real, code-compliant "
                            "hardware - sized to do the duty and strong and durable "
                            "enough to do it safely",
                            correct=True,
                        ),
                        opt("It only decides the paint colour of the vessels"),
                        opt("It replaces the need for process simulation"),
                    ),
                    "The flowsheet says what must happen; equipment design specifies the "
                    "physical vessel, exchanger, column or pump that does it.",
                ),
                q(
                    "What two questions does every equipment design answer?",
                    (
                        opt("Who built it and how much it cost"),
                        opt(
                            "Is it big enough for the duty, and is it strong and durable "
                            "enough to run safely for the plant's life",
                            correct=True,
                        ),
                        opt("What colour it is and where it ships from"),
                        opt("Which vendor is cheapest and which is fastest"),
                    ),
                    "Sizing (big enough) and mechanical/materials integrity (strong and "
                    "durable enough) are the two sides of every design.",
                ),
            ),
        ),
        # -- 1. Pressure vessel design (ASME BPVC) ---------------------
        _t(
            "Pressure vessel design (ASME BPVC)",
            "11 min",
            """# Pressure vessel design (ASME BPVC)

Most chemical plant hardware is, mechanically, a **pressure vessel**: a
container holding fluid at a pressure different from ambient. In North
America these are designed and stamped to the **ASME Boiler and Pressure
Vessel Code**, and Section **VIII Division 1** is the workhorse for
unfired vessels. The Code sets the allowable stress, the design formulas,
and the inspection and stamping rules.

The core sizing job is the **shell wall thickness**. For a thin-walled
cylinder under internal pressure, circumferential (hoop) stress governs.
The Section VIII-1 formula for the required thickness of a cylindrical
shell is:

```text
Cylindrical shell, internal pressure (ASME VIII-1, UG-27):

    t = P * R / (S * E - 0.6 * P)

  t = required wall thickness (before corrosion allowance)
  P = internal design pressure
  R = inside radius
  S = maximum allowable stress for the material at design temperature
  E = joint efficiency (weld quality: 1.0 full radiography ... 0.70 none)

Worked example:
  P = 1.72 MPa (250 psi) design pressure
  R = 0.75 m (inside radius, 1.5 m diameter vessel)
  S = 138 MPa (carbon steel SA-516-70 at temperature)
  E = 0.85 (spot radiography)

    t = (1.72 * 0.75) / (138 * 0.85 - 0.6 * 1.72)
      = 1.29 / (117.3 - 1.03)
      = 1.29 / 116.27
      = 0.0111 m  = 11.1 mm

  Add corrosion allowance (say 3 mm): t_design = 14.1 mm
  Round UP to the next standard plate: 16 mm.
```

Three ideas make this real practice, not just a formula:

- **Design pressure and temperature** are set *above* the worst operating
  case (commonly operating pressure plus a margin, and a corresponding
  temperature), because the vessel must survive upsets, not just normal
  running.
- **Corrosion allowance** is extra metal you add and expect to lose over
  the vessel's life - the pressure formula gives the metal that must
  *remain*, so you add the allowance on top.
- **Joint efficiency E** rewards weld inspection: fully radiographed welds
  let you use thinner walls than un-inspected ones.

The heads (ends) and any openings (nozzles) have their own Code rules -
an ellipsoidal or torispherical head, and **nozzle reinforcement** to
replace the metal a hole removes.

```mermaid
graph TD
    DUTY["Process duty pressure and temperature"] --> DESIGN["Set design pressure and temperature with margin"]
    DESIGN --> MAT["Pick material and allowable stress S"]
    MAT --> SHELL["Shell thickness by UG-27 formula"]
    SHELL --> CA["Add corrosion allowance"]
    CA --> HEADS["Size heads and nozzle reinforcement"]
    HEADS --> STAMP["Inspect and stamp to ASME VIII-1"]
```

Remember: the wall must hold the *design* pressure hot, keep enough metal
after a life of corrosion, and be joined by welds good enough for the
efficiency you assumed.
""",
        ),
        quiz_lesson(
            "Quiz: Pressure vessel design (ASME BPVC)",
            (
                q(
                    "Which code section is the workhorse for unfired pressure vessels?",
                    (
                        opt("ASME B31.3 Process Piping"),
                        opt("ASME BPVC Section VIII Division 1", correct=True),
                        opt("API 650 Welded Tanks"),
                        opt("TEMA Class R"),
                    ),
                    "Section VIII Division 1 of the ASME Boiler and Pressure Vessel Code "
                    "governs unfired vessel design and stamping.",
                ),
                q(
                    "In t = P R / (S E - 0.6 P), what does the joint efficiency E represent?",
                    (
                        opt("The pump efficiency feeding the vessel"),
                        opt(
                            "A factor rewarding weld quality and inspection - full "
                            "radiography allows a higher E and thus a thinner wall",
                            correct=True,
                        ),
                        opt("The thermal efficiency of the process"),
                        opt("The corrosion rate of the steel"),
                    ),
                    "E ranges roughly 0.70 (no radiography) to 1.0 (full radiography); "
                    "better-inspected welds permit thinner walls.",
                ),
                q(
                    "How is corrosion allowance handled in the thickness calculation?",
                    (
                        opt("It is subtracted from the design pressure"),
                        opt("It is ignored because stainless never corrodes"),
                        opt(
                            "It is added on top of the pressure-required thickness, since "
                            "the formula gives the metal that must remain after corrosion",
                            correct=True,
                        ),
                        opt("It replaces the joint efficiency term"),
                    ),
                    "The pressure formula sizes the surviving metal; corrosion allowance "
                    "is extra thickness you expect to lose over the vessel life.",
                ),
            ),
        ),
        # -- 2. Shell-and-tube heat exchanger design -------------------
        _t(
            "Shell-and-tube heat exchanger design",
            "11 min",
            """# Shell-and-tube heat exchanger design

When you must move heat between two fluids without mixing them, the
default is a **shell-and-tube heat exchanger**: a bundle of tubes inside a
cylindrical shell. One fluid flows through the tubes, the other around
them in the shell, and heat crosses the tube wall. Their mechanical
standard is **TEMA** (the Tubular Exchanger Manufacturers Association),
which classifies front head, shell and rear head types (the familiar
codes like **BEM**, **AES**, **BEU**).

The sizing job is the **heat transfer area**. Three quantities set it:

```text
Duty:      Q = m_hot * cp_hot * (T_in - T_out)      [energy balance]

Driving    LMTD = (dT1 - dT2) / ln(dT1 / dT2)
force:       dT1, dT2 = terminal temperature differences (hot end, cold end)

Area:      Q = U * A * LMTD * F   ->   A = Q / (U * LMTD * F)
             U = overall heat transfer coefficient
             F = LMTD correction factor for multi-pass geometry (<= 1)

Worked example (counter-current, F = 1):
  Q     = 500 kW = 500000 W
  Hot:   150 C -> 90 C     Cold: 30 C -> 80 C
  dT1 = 150 - 80 = 70 C    dT2 = 90 - 30 = 60 C
  LMTD = (70 - 60) / ln(70 / 60) = 10 / 0.1542 = 64.9 C
  U     = 500 W/(m2 K)   (typical water-to-organic, fouled)

  A = 500000 / (500 * 64.9) = 15.4 m2

  With 19 mm OD tubes, 5 m long:
    area per tube = pi * 0.019 * 5 = 0.298 m2
    tubes needed  = 15.4 / 0.298 = 52 tubes
```

Real design refines this:

- **Overall coefficient U** is built from the two film coefficients, the
  tube-wall resistance and **fouling factors** on each side. Fouling is
  often the largest resistance and the reason exchangers are oversized.
- **The F factor** corrects the LMTD when the flow is not pure
  counter-current (e.g. one shell pass and two tube passes). If F falls
  below about 0.8, add shell passes or use more shells in series.
- **Which fluid goes where** matters: the dirtier, more corrosive, or
  higher-pressure fluid usually goes in the **tubes** (easier to clean,
  cheaper to build thick), the other in the shell.

```mermaid
graph LR
    Q["Duty Q from energy balance"] --> LMTD["Compute LMTD from terminals"]
    LMTD --> F["Apply F correction for passes"]
    U["Overall U with fouling"] --> AREA["Area equals Q over U LMTD F"]
    F --> AREA
    AREA --> TUBES["Choose tube size length and count"]
    TUBES --> TEMA["Select TEMA head and shell type"]
```

Remember: duty sets *how much* heat, LMTD sets the *driving force*, U and
fouling set *how hard* it is - and their ratio is the area you must build.
""",
        ),
        quiz_lesson(
            "Quiz: Shell-and-tube heat exchanger design",
            (
                q(
                    "In A = Q / (U * LMTD * F), what does the LMTD represent?",
                    (
                        opt("The pressure drop across the tubes"),
                        opt(
                            "The log-mean temperature difference - the effective "
                            "temperature driving force between the two fluids",
                            correct=True,
                        ),
                        opt("The mechanical design temperature of the shell"),
                        opt("The fouling factor on the shell side"),
                    ),
                    "LMTD averages the terminal temperature differences logarithmically; "
                    "it is the driving force for heat transfer.",
                ),
                q(
                    "Why is the fouling factor important in the overall coefficient U?",
                    (
                        opt("It has no effect on modern exchangers"),
                        opt(
                            "Fouling adds thermal resistance - often the largest term - "
                            "so exchangers are sized larger to stay effective as they foul",
                            correct=True,
                        ),
                        opt("It only affects the pressure rating"),
                        opt("It increases the LMTD"),
                    ),
                    "Fouling resistance lowers U; ignoring it leaves an exchanger that "
                    "underperforms once deposits build up.",
                ),
                q(
                    "Which fluid is usually placed on the tube side, and why?",
                    (
                        opt("Always the hot fluid, to keep the shell cool"),
                        opt(
                            "The dirtier, more corrosive or higher-pressure fluid - tubes "
                            "are easier to clean and cheaper to build for tough service",
                            correct=True,
                        ),
                        opt("Always the fluid with the larger flow rate"),
                        opt("It never matters which side a fluid takes"),
                    ),
                    "Tube-side assignment favours the fluid that is dirty, corrosive or "
                    "high pressure because tubes are cleanable and cheaper to harden.",
                ),
            ),
        ),
        # -- 3. Distillation column internals --------------------------
        _t(
            "Distillation column internals",
            "11 min",
            """# Distillation column internals

A distillation column separates by repeatedly contacting rising vapour
with falling liquid so the light component enriches upward. The process
design (from a **McCabe-Thiele** diagram or a rigorous simulation) gives
you the number of theoretical stages and the internal vapour and liquid
loads. **Equipment design** turns that into the physical column: the
**internals** that make the contact happen and the **diameter** that
carries the traffic.

Two families of internals:

- **Trays** (sieve, valve, bubble-cap) - horizontal plates the liquid
  crosses while vapour bubbles up through it. Good for high liquid loads,
  fouling service and where you need to draw off side streams.
- **Packing** (random rings or structured sheets) - a bed the liquid
  trickles down and vapour rises through. Lower pressure drop per stage;
  favoured for vacuum service and for revamps that need more capacity in
  the same shell. Packing efficiency is quoted as **HETP** (height
  equivalent to a theoretical plate).

Real stages fall short of theoretical ones, so:

```text
Actual trays  = theoretical stages / overall tray efficiency
  e.g. 20 theoretical stages, efficiency 0.65 -> 31 actual trays

Packed height = theoretical stages * HETP
  e.g. 20 stages * 0.45 m HETP = 9.0 m of packing
```

The **diameter** is set by vapour capacity - too high a vapour velocity
entrains liquid upward (**flooding**), too low and trays weep. A common
capacity method uses the **Souders-Brown** equation:

```text
Flooding-limited vapour velocity (Souders-Brown):

    u_max = C_sb * sqrt((rho_L - rho_V) / rho_V)

Then size the diameter for a fraction of flooding (say 80 percent):

    Volumetric vapour flow  Qv = m_V / rho_V
    Required area  A = Qv / (0.80 * u_max)
    Diameter       D = sqrt(4 * A / pi)

Worked example:
  m_V = 3.0 kg/s,  rho_V = 2.0 kg/m3,  rho_L = 640 kg/m3
  C_sb = 0.09 m/s
  u_max = 0.09 * sqrt((640 - 2) / 2) = 0.09 * 17.86 = 1.61 m/s
  Qv    = 3.0 / 2.0 = 1.5 m3/s
  A     = 1.5 / (0.80 * 1.61) = 1.16 m2
  D     = sqrt(4 * 1.16 / pi) = 1.22 m
```

```mermaid
graph TD
    STAGES["Theoretical stages from process design"] --> CHOICE["Choose trays or packing"]
    CHOICE --> HEIGHT["Height from tray efficiency or HETP"]
    LOADS["Vapour and liquid loads"] --> VMAX["Flooding velocity Souders-Brown"]
    VMAX --> DIA["Diameter at a fraction of flooding"]
    HEIGHT --> COLUMN["Column shell height and diameter"]
    DIA --> COLUMN
```

Remember: process design gives stages and loads; equipment design chooses
trays or packing for the height and sizes the diameter to stay safely
below flooding.
""",
        ),
        quiz_lesson(
            "Quiz: Distillation column internals",
            (
                q(
                    "What sets the diameter of a distillation column?",
                    (
                        opt("The number of theoretical stages"),
                        opt(
                            "Vapour capacity - the diameter must keep the vapour velocity "
                            "safely below the flooding limit",
                            correct=True,
                        ),
                        opt("The colour of the trays"),
                        opt("The corrosion allowance alone"),
                    ),
                    "Too high a vapour velocity floods the column; the diameter is sized "
                    "for a fraction (say 80 percent) of the flooding velocity.",
                ),
                q(
                    "How do you get the actual number of trays from theoretical stages?",
                    (
                        opt("They are always equal"),
                        opt(
                            "Divide theoretical stages by the overall tray efficiency, "
                            "since real trays are less than a theoretical stage",
                            correct=True,
                        ),
                        opt("Multiply theoretical stages by the pressure drop"),
                        opt("Add the reflux ratio to the stage count"),
                    ),
                    "Actual trays = theoretical stages / tray efficiency; efficiency "
                    "below 1 means more physical trays than ideal stages.",
                ),
                q(
                    "What does HETP describe for packed columns?",
                    (
                        opt("The pressure rating of the shell"),
                        opt(
                            "Height equivalent to a theoretical plate - the packed depth "
                            "that achieves one theoretical stage",
                            correct=True,
                        ),
                        opt("The heat duty of the reboiler"),
                        opt("The maximum operating temperature"),
                    ),
                    "Packed height = theoretical stages * HETP; a smaller HETP means a "
                    "more efficient packing.",
                ),
            ),
        ),
        # -- 4. Storage tanks and vessels ------------------------------
        _t(
            "Storage tanks and vessels",
            "10 min",
            """# Storage tanks and vessels

Not everything is under high pressure. Plants hold feedstocks, products
and intermediates in **storage tanks and vessels**, and the right design
depends mostly on the **vapour pressure** of what is stored and the
pressure it must hold.

The main categories:

- **Atmospheric storage tanks** - large, flat-bottomed, essentially at
  ambient pressure. Designed to **API 650** (welded steel tanks). For
  volatile liquids a **floating roof** (external or internal) rides on the
  liquid surface to cut evaporation and breathing losses; for less
  volatile liquids a **fixed cone roof** is enough.
- **Low-pressure tanks** - hold a few tens of kPa of gauge pressure,
  designed to **API 620**.
- **Pressure storage** - for liquefied gases (LPG, ammonia) held under
  their own vapour pressure, you use **pressure vessels**: horizontal
  **bullets** or spherical tanks, designed to ASME VIII (the previous
  vessel lesson).

Two things dominate storage design beyond just holding the liquid:

- **Venting and breathing.** A fixed-roof tank breathes as it fills,
  empties, and as day and night change the temperature. It must be vented
  so it neither bursts on overpressure nor collapses under vacuum - sized
  to **API 2000**. Under-sizing vents is a classic cause of tank failure.
- **Containment.** Tanks sit inside a **dike or bund** sized to hold the
  contents of the largest tank (often 110 percent) so a leak does not
  spread.

Sizing the tank itself is mostly geometry, plus a shell that carries the
hydrostatic head of the stored liquid:

```text
Tank volume and shell thickness (API 650 one-foot method idea):

  Volume:  V = pi/4 * D^2 * H         (cylindrical tank)

  Shell (hoop stress from liquid head at the bottom course):
     t = rho * g * H * D / (2 * S * E)  + corrosion allowance

Worked example:
  Store 2000 m3 of a liquid, choose D = 15 m
     H = V / (pi/4 * D^2) = 2000 / (0.785 * 225) = 11.3 m
  Bottom-course thickness (rho = 900 kg/m3, S = 160 MPa, E = 0.85):
     t = 900 * 9.81 * 11.3 * 15 / (2 * 160e6 * 0.85)
       = 1.497e6 / 2.72e8 = 0.0055 m = 5.5 mm  + corrosion allowance
```

```mermaid
graph TD
    FLUID["What is stored and its vapour pressure"] --> TYPE{"Pressure needed"}
    TYPE -->|"atmospheric"| API650["API 650 flat bottom tank"]
    TYPE -->|"low pressure"| API620["API 620 tank"]
    TYPE -->|"liquefied gas"| VESSEL["ASME pressure vessel bullet or sphere"]
    API650 --> ROOF["Fixed or floating roof for losses"]
    API650 --> VENT["Vent sizing API 2000 and bund"]
```

Remember: match the tank type to the vapour pressure, protect it with
correctly sized venting, and contain a spill with a bund.
""",
        ),
        quiz_lesson(
            "Quiz: Storage tanks and vessels",
            (
                q(
                    "Which code governs large atmospheric welded steel storage tanks?",
                    (
                        opt("ASME VIII Division 1"),
                        opt("API 650", correct=True),
                        opt("TEMA Class C"),
                        opt("ASME B16.5"),
                    ),
                    "API 650 covers welded flat-bottomed atmospheric tanks; API 620 "
                    "covers low-pressure tanks, and ASME VIII covers pressure storage.",
                ),
                q(
                    "Why does a fixed-roof storage tank need correctly sized venting?",
                    (
                        opt("To let operators see inside"),
                        opt(
                            "It breathes as it fills, empties and changes temperature - "
                            "under-sized vents can burst it on overpressure or collapse "
                            "it under vacuum",
                            correct=True,
                        ),
                        opt("Only to reduce noise"),
                        opt("Venting is never required on storage tanks"),
                    ),
                    "Breathing from filling, emptying and thermal cycles must be relieved "
                    "per API 2000; poor vent sizing is a classic tank failure cause.",
                ),
                q(
                    "What is a floating roof for, on a volatile-liquid tank?",
                    (
                        opt("To raise the tank pressure rating"),
                        opt(
                            "It rides on the liquid surface to cut evaporation and "
                            "breathing losses of volatile product",
                            correct=True,
                        ),
                        opt("To act as the containment bund"),
                        opt("To hold liquefied gas under pressure"),
                    ),
                    "A floating roof removes the vapour space above the liquid, reducing "
                    "evaporative and breathing losses.",
                ),
            ),
        ),
        # -- 5. Piping and pump sizing ---------------------------------
        _t(
            "Piping and pump sizing",
            "11 min",
            """# Piping and pump sizing

Equipment is connected by **pipe**, and fluid is moved through it by
**pumps**. Two coupled sizing jobs: choose a pipe diameter, then choose a
pump that overcomes the resulting resistance at the required flow.

**Line sizing** trades capital against operating cost. A small pipe is
cheap to buy but has high velocity, high pressure drop and high pumping
power; a large pipe is the reverse. In practice engineers size to
**economic velocity** ranges (roughly 1-3 m/s for pumped liquids) and
check the pressure drop with the **Darcy-Weisbach** equation:

```text
Pressure drop in a pipe (Darcy-Weisbach):

    dP = f * (L / D) * (rho * v^2 / 2)

  f = Darcy friction factor (from Reynolds number Re and roughness,
      via the Moody chart or the Colebrook equation)
  L = length, D = inside diameter, v = velocity, rho = density

  Re = rho * v * D / mu   decides laminar (Re < 2300) vs turbulent
```

Piping itself is designed to **ASME B31.3** (process piping): wall
thickness from internal pressure, plus flanges, fittings and stress from
thermal expansion.

**Pump sizing** needs the flow rate and the **total head** the pump must
add. Head, not pressure, is the natural unit because it is
fluid-independent:

```text
Pump head from the energy balance (per unit weight):

    H = (P2 - P1)/(rho*g) + (z2 - z1) + (v2^2 - v1^2)/(2g) + h_f

      static pressure + static lift + velocity + friction (h_f from dP above)

Hydraulic power:   P_hyd = rho * g * Q * H
Shaft power:       P_shaft = P_hyd / eta_pump

Worked example:
  Q = 0.02 m3/s (72 m3/h) water, total head H = 45 m, eta = 0.70
  P_hyd  = 1000 * 9.81 * 0.02 * 45 = 8829 W = 8.8 kW
  P_shaft = 8.8 / 0.70 = 12.6 kW  -> select a 15 kW motor
```

Two more checks decide a workable pump:

- **Operating point** - a centrifugal pump follows a **head-vs-flow
  curve**; it runs where that curve crosses the **system curve** (static
  head plus friction that rises with flow squared). Size for that crossing.
- **NPSH** - the pump needs enough **Net Positive Suction Head available**
  over what it **requires**, or the liquid flashes at the impeller eye and
  the pump **cavitates**. Keep NPSHa > NPSHr with margin.

```mermaid
graph LR
    FLOW["Required flow rate"] --> DIA["Size pipe to economic velocity"]
    DIA --> DP["Friction from Darcy-Weisbach"]
    DP --> HEAD["Total head static plus friction"]
    HEAD --> OP["Operating point pump curve meets system curve"]
    OP --> POWER["Shaft power and motor selection"]
    OP --> NPSH["Check NPSHa greater than NPSHr"]
```

Remember: size the pipe for economic velocity, add up the head the pump
must deliver, place the operating point where the curves cross, and guard
against cavitation with NPSH margin.
""",
        ),
        quiz_lesson(
            "Quiz: Piping and pump sizing",
            (
                q(
                    "What does the Darcy-Weisbach equation give you?",
                    (
                        opt("The pump motor efficiency"),
                        opt(
                            "The frictional pressure drop of fluid flowing through a pipe",
                            correct=True,
                        ),
                        opt("The tank vent size"),
                        opt("The heat exchanger area"),
                    ),
                    "dP = f (L/D)(rho v^2 / 2) gives pipe friction loss; the friction "
                    "factor f depends on Reynolds number and roughness.",
                ),
                q(
                    "Why must NPSH available exceed NPSH required for a pump?",
                    (
                        opt("To increase the motor efficiency"),
                        opt(
                            "Otherwise the liquid flashes to vapour at the impeller eye "
                            "and the pump cavitates, damaging it and losing head",
                            correct=True,
                        ),
                        opt("To reduce the pipe diameter"),
                        opt("NPSH only matters for gases"),
                    ),
                    "If NPSHa falls below NPSHr the liquid boils at the suction, causing "
                    "cavitation; keep a margin between them.",
                ),
                q(
                    "Where does a centrifugal pump actually operate?",
                    (
                        opt("At its maximum possible head, always"),
                        opt(
                            "Where its head-vs-flow curve crosses the system curve "
                            "(static head plus friction rising with flow squared)",
                            correct=True,
                        ),
                        opt("At zero flow"),
                        opt("Wherever the motor nameplate says"),
                    ),
                    "The operating point is the intersection of the pump curve and the "
                    "system curve; you size for that crossing.",
                ),
            ),
        ),
        # -- 6. Reactor vessel design ----------------------------------
        _t(
            "Reactor vessel design",
            "11 min",
            """# Reactor vessel design

The **reactor** is where the chemistry happens, and its design couples
three things at once: **reaction kinetics** (how fast), **volume and
residence time** (how long the fluid stays), and **heat management** (most
reactions release or absorb heat that must be moved). Get any one wrong
and conversion, safety or selectivity suffer.

Two idealized flow patterns bracket real reactors:

- **CSTR** (continuous stirred-tank reactor) - well mixed, uniform
  composition; simple, good for liquids and for slow reactions.
- **PFR** (plug-flow reactor) - fluid moves as plugs with no back-mixing,
  usually a tube; gives higher conversion per volume for most kinetics.

Sizing starts from the **design equation** for the chosen type, using the
**rate law** (often **Arrhenius** for the temperature dependence):

```text
Rate law (first order):     -r_A = k * C_A,      k = A * exp(-Ea / (R*T))

CSTR volume (from mole balance):
    V = F_A0 * X / (-r_A at outlet conditions)

Worked example (liquid, first-order, CSTR):
  Feed F_A0 = 2.0 mol/s,  inlet C_A0 = 1.0 mol/L,  target conversion X = 0.80
  k = 0.05 1/s at the operating temperature
  Outlet C_A = C_A0 (1 - X) = 1.0 * 0.20 = 0.20 mol/L
  -r_A = k * C_A = 0.05 * 0.20 = 0.010 mol/(L s)
  V = F_A0 * X / (-r_A) = (2.0 * 0.80) / 0.010 = 160 L  = 0.16 m3

  Residence time tau = V / Q, with Q = F_A0 / C_A0 = 2.0 / 1.0 = 2.0 L/s
     tau = 160 / 2.0 = 80 s
```

The **heat** side is what makes a reactor a demanding vessel:

- **Exothermic** reactions must have heat removed or the temperature runs
  away - the rate rises with temperature (Arrhenius), which raises the
  heat release, which raises the temperature: a **thermal runaway**. You
  provide a **jacket or internal coils** and check the cooling can beat the
  worst-case heat generation.
- Mechanically the vessel is still an **ASME pressure vessel**, now with an
  **agitator** (power and shaft design), jacket, and nozzles for feed,
  product, relief and instruments - plus a **relief system** sized for the
  runaway or external-fire case.

```mermaid
graph TD
    KIN["Kinetics rate law and Arrhenius"] --> TYPE["Choose CSTR or PFR"]
    TYPE --> VOL["Volume from the design equation"]
    VOL --> TAU["Residence time volume over flow"]
    HEAT["Heat of reaction"] --> COOL["Jacket or coils sized to remove heat"]
    COOL --> RELIEF["Relief system for runaway or fire"]
    VOL --> MECH["ASME vessel with agitator and nozzles"]
```

Remember: kinetics and the design equation set the volume, flow sets the
residence time, and heat removal plus relief keep an exothermic reactor
from running away.
""",
        ),
        quiz_lesson(
            "Quiz: Reactor vessel design",
            (
                q(
                    "What does the Arrhenius equation describe in reactor design?",
                    (
                        opt("The pressure drop through the reactor"),
                        opt(
                            "How the reaction rate constant k rises with temperature, "
                            "k = A exp(-Ea / R T)",
                            correct=True,
                        ),
                        opt("The corrosion rate of the vessel wall"),
                        opt("The pump head needed to feed the reactor"),
                    ),
                    "Arrhenius gives the temperature dependence of the rate constant; it "
                    "drives both conversion and the heat-generation feedback.",
                ),
                q(
                    "Why is heat removal critical for an exothermic reactor?",
                    (
                        opt("It has no effect on safety"),
                        opt(
                            "Rate rises with temperature, which raises heat release and "
                            "temperature further - inadequate cooling causes thermal runaway",
                            correct=True,
                        ),
                        opt("Because cold reactors always react faster"),
                        opt("Only to save on pump power"),
                    ),
                    "The Arrhenius feedback (hotter -> faster -> hotter) can run away; a "
                    "jacket or coils plus a sized relief system prevent it.",
                ),
                q(
                    "In a CSTR, how is the required volume related to the reaction rate?",
                    (
                        opt("V = F_A0 * X / (-r_A) - volume rises as the rate falls", correct=True),
                        opt("Volume is independent of the reaction rate"),
                        opt("V equals the pump flow rate"),
                        opt("Volume equals the heat of reaction"),
                    ),
                    "The CSTR mole balance gives V = F_A0 X / (-r_A); a slower rate at "
                    "outlet conditions demands a larger reactor.",
                ),
            ),
        ),
        # -- 7. Materials selection and corrosion ----------------------
        _t(
            "Materials selection and corrosion",
            "11 min",
            """# Materials selection and corrosion

A vessel sized perfectly to code still fails early if it is built from the
wrong metal for the fluid it holds. **Materials selection** picks a
material of construction that is strong enough, resists the specific
**corrosion** of the service, and is affordable - and it drives the
**corrosion allowance** the mechanical design carries.

The common workhorses, cheapest first:

- **Carbon steel** (e.g. SA-516-70) - cheap, strong, the default for
  non-corrosive service; corrodes in wet or acidic conditions, so it
  carries a corrosion allowance.
- **Stainless steels** - **304/304L** and **316/316L** resist many
  corrosive services by forming a passive chromium-oxide film; 316 adds
  molybdenum for chloride and acid resistance.
- **Nickel alloys** (Hastelloy, Inconel), **titanium**, and non-metals
  (**lined** vessels, glass-lined, FRP) - for aggressive acids, chlorides
  or high temperature, at rising cost.

Corrosion is not one thing - the **mechanism** decides the right material:

- **Uniform corrosion** - even thinning; handled with a corrosion
  allowance and a known **corrosion rate** (often quoted in mm/year or
  mils/year).
- **Pitting and crevice corrosion** - localized attack, often by
  **chlorides**, that perforates while most of the wall looks fine.
- **Stress-corrosion cracking (SCC)** - cracking under the combination of
  tensile stress and a specific environment (e.g. chloride SCC of
  austenitic stainless, caustic or sulfide SCC).
- **Galvanic corrosion** - two dissimilar metals in contact in an
  electrolyte; the less noble one corrodes faster.

Selecting a material and sizing its allowance:

```text
Corrosion allowance from rate and life:

    CA = corrosion_rate * design_life

Worked example:
  Carbon steel, measured rate = 0.15 mm/year, design life = 20 years
    CA = 0.15 * 20 = 3.0 mm   -> add 3 mm to the pressure thickness

  If the rate were 0.5 mm/year, CA = 10 mm - at that point a more
  corrosion-resistant alloy or a lining is usually cheaper over the life
  than carrying 10 mm of sacrificial carbon steel.
```

Tools like a **corrosion (materials selection) chart** and standards such
as **NACE/AMPP** guidance (for example for sour, sulfide-containing
service) turn service conditions into an allowable material list.

```mermaid
graph TD
    SERVICE["Fluid temperature and contaminants"] --> MECH{"Corrosion mechanism"}
    MECH -->|"uniform"| CA["Carbon steel plus corrosion allowance"]
    MECH -->|"chlorides pitting or SCC"| ALLOY["316L or higher alloy"]
    MECH -->|"aggressive acid"| EXOTIC["Nickel alloy titanium or lining"]
    CA --> LIFE["Allowance equals rate times life"]
    ALLOY --> COST["Balance material cost against life"]
    EXOTIC --> COST
```

Remember: identify the corrosion *mechanism* first, pick a material that
resists it, and let the corrosion rate and design life set the allowance -
switching to a better alloy is often cheaper than carrying thick
sacrificial metal.
""",
        ),
        quiz_lesson(
            "Quiz: Materials selection and corrosion",
            (
                q(
                    "How is a corrosion allowance related to corrosion rate and design life?",
                    (
                        opt("It is unrelated to either"),
                        opt(
                            "Allowance = corrosion rate * design life - the sacrificial "
                            "metal expected to be lost over the vessel's service life",
                            correct=True,
                        ),
                        opt("It equals the design pressure times the radius"),
                        opt("It is always exactly 1 mm"),
                    ),
                    "CA = rate * life; a high rate over a long life demands thick "
                    "sacrificial metal, often making a better alloy cheaper.",
                ),
                q(
                    "Which corrosion mechanism is a particular threat to austenitic "
                    "stainless steel in chloride service?",
                    (
                        opt("Uniform corrosion only"),
                        opt(
                            "Chloride stress-corrosion cracking (and pitting) - localized "
                            "attack under tensile stress in a chloride environment",
                            correct=True,
                        ),
                        opt("Galvanic corrosion with itself"),
                        opt("Erosion by clean water"),
                    ),
                    "Chlorides drive pitting and stress-corrosion cracking of austenitic "
                    "stainless; 316 with molybdenum resists better than 304.",
                ),
                q(
                    "Why does identifying the corrosion mechanism come before picking a material?",
                    (
                        opt("It does not - any stainless works everywhere"),
                        opt(
                            "Different mechanisms (uniform, pitting, SCC, galvanic) need "
                            "different resistances, so the mechanism decides which "
                            "material actually survives the service",
                            correct=True,
                        ),
                        opt("Because the mechanism sets the pump head"),
                        opt("Only to choose the paint colour"),
                    ),
                    "A material resistant to uniform thinning may still fail by pitting "
                    "or SCC; the mechanism drives the correct selection.",
                ),
            ),
        ),
        # -- 8. Mechanical integrity and codes -------------------------
        _t(
            "Mechanical integrity and codes",
            "10 min",
            """# Mechanical integrity and codes

Individual equipment is designed to individual codes, but they sit inside
one framework: a plant must demonstrate **mechanical integrity** - that
its pressure-containing equipment is designed, built, inspected and
maintained so it does not fail. This lesson ties the codes together and
adds the parts that protect equipment beyond its own walls.

The **map of codes** you have met and their neighbours:

```text
Equipment                Governing standard(s)
-----------------------  ------------------------------------------
Pressure vessels         ASME BPVC Section VIII (Div 1/2)
Reactors (as vessels)    ASME BPVC Section VIII + relief sizing
Heat exchangers          ASME VIII (pressure parts) + TEMA (mechanical)
Distillation columns     ASME VIII (the shell is a pressure vessel)
Atmospheric tanks        API 650   (low pressure: API 620)
Tank venting             API 2000
Process piping           ASME B31.3
Flanges and fittings     ASME B16.5 / B16.47
Relief devices           ASME VIII UG-125+; sizing API 520/521
Materials and welding    ASME II (materials) and IX (welding qualification)
In-service inspection    API 510 (vessels), 570 (piping), 653 (tanks)
```

Three integrity ideas cut across all of them:

- **Overpressure protection.** Every pressure system needs a **relief
  device** - a relief valve or rupture disc - sized (API 520/521) for the
  worst credible case: blocked outlet, fire exposure, thermal expansion,
  or reaction runaway. The relief is the last line of defence when
  controls fail.
- **Inspection and testing.** New equipment is proof-tested, usually by a
  **hydrotest** to about **1.3 times** the design pressure (ASME VIII), and
  welds are examined. In service, equipment is re-inspected on a schedule
  (the API 5xx codes) - often **risk-based inspection (RBI)** that
  concentrates effort where failure is most likely and most consequential.
- **Management of change.** Any change to equipment, materials or operating
  conditions must be re-evaluated against the codes before it is made -
  quietly running a vessel hotter or at higher pressure than its stamp
  allows is how integrity is lost.

```mermaid
graph TD
    DESIGN["Design to the governing code"] --> BUILD["Fabricate and weld to ASME IX"]
    BUILD --> TEST["Hydrotest about 1.3 times design pressure"]
    TEST --> RELIEF["Relief device sized for worst case"]
    RELIEF --> OPERATE["Operate within the stamped limits"]
    OPERATE --> INSPECT["In service inspection API 510 570 653"]
    INSPECT --> MOC["Management of change re-evaluates"]
    MOC --> OPERATE
```

Remember: sizing gets you the right equipment; mechanical integrity -
relief protection, proof and in-service inspection, and disciplined change
control - keeps it safe for the whole life of the plant.
""",
        ),
        quiz_lesson(
            "Quiz: Mechanical integrity and codes",
            (
                q(
                    "What is the purpose of a relief device on a pressure system?",
                    (
                        opt("To increase the design pressure"),
                        opt(
                            "To protect against overpressure - sized for the worst "
                            "credible case such as blocked outlet, fire or reaction runaway",
                            correct=True,
                        ),
                        opt("To improve heat transfer"),
                        opt("To reduce the pump NPSH required"),
                    ),
                    "Relief valves and rupture discs (sized to API 520/521) are the last "
                    "line of defence when controls fail to hold pressure.",
                ),
                q(
                    "A new pressure vessel is typically proof-tested by a hydrotest to about…",
                    (
                        opt("0.5 times the design pressure"),
                        opt("exactly the operating pressure"),
                        opt("about 1.3 times the design pressure", correct=True),
                        opt("ten times the design pressure"),
                    ),
                    "ASME VIII specifies a hydrostatic test around 1.3 times design "
                    "pressure to prove the vessel before service.",
                ),
                q(
                    "Which standard governs in-service inspection of pressure vessels?",
                    (
                        opt("API 510", correct=True),
                        opt("ASME B31.3"),
                        opt("TEMA Class B"),
                        opt("API 2000"),
                    ),
                    "API 510 covers in-service vessel inspection; API 570 covers piping "
                    "and API 653 covers tanks.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In the ASME shell formula t = P R / (S E - 0.6 P), increasing the "
                    "joint efficiency E does what to the required wall thickness?",
                    (
                        opt("Increases it"),
                        opt(
                            "Decreases it - better-inspected welds allow a thinner wall",
                            correct=True,
                        ),
                        opt("Has no effect"),
                        opt("Sets it to zero"),
                    ),
                    "A higher E (from radiography) raises the denominator, reducing the "
                    "required thickness.",
                ),
                q(
                    "For a shell-and-tube exchanger, what does A = Q / (U * LMTD * F) size?",
                    (
                        opt("The pump power"),
                        opt(
                            "The heat transfer area needed to move duty Q against the "
                            "driving force LMTD at coefficient U",
                            correct=True,
                        ),
                        opt("The corrosion allowance"),
                        opt("The relief valve set pressure"),
                    ),
                    "Duty over (U times LMTD times the pass-correction F) gives the "
                    "required area, then tube count and TEMA layout.",
                ),
                q(
                    "What sets a distillation column's diameter?",
                    (
                        opt(
                            "Keeping vapour velocity safely below the flooding limit", correct=True
                        ),
                        opt("The number of theoretical stages"),
                        opt("The reboiler material"),
                        opt("The corrosion rate of the trays"),
                    ),
                    "Vapour capacity (via a flooding-velocity method like Souders-Brown) "
                    "sets diameter; stages and efficiency set height.",
                ),
                q(
                    "A liquefied gas such as LPG is best stored in what kind of equipment?",
                    (
                        opt("An open pond"),
                        opt("An API 650 atmospheric tank"),
                        opt(
                            "An ASME pressure vessel (bullet or sphere) holding it under "
                            "its own vapour pressure",
                            correct=True,
                        ),
                        opt("A fixed cone-roof tank with no venting"),
                    ),
                    "Liquefied gases held under vapour pressure need ASME pressure "
                    "vessels; atmospheric tanks suit low-vapour-pressure liquids.",
                ),
                q(
                    "Why must a pump keep NPSH available above NPSH required?",
                    (
                        opt("To raise the discharge pressure rating"),
                        opt(
                            "To stop the liquid flashing at the impeller eye, which causes "
                            "cavitation and lost head",
                            correct=True,
                        ),
                        opt("To reduce the pipe wall thickness"),
                        opt("NPSH matters only for gases"),
                    ),
                    "If NPSHa drops below NPSHr the liquid boils at the suction and the "
                    "pump cavitates; keep a margin.",
                ),
                q(
                    "In a CSTR sized by V = F_A0 X / (-r_A), a slower reaction rate means…",
                    (
                        opt("a smaller reactor"),
                        opt("a larger required reactor volume", correct=True),
                        opt("no change in volume"),
                        opt("a higher pump head"),
                    ),
                    "The rate is in the denominator, so a slower rate at outlet "
                    "conditions demands more volume for the same conversion.",
                ),
                q(
                    "Why is heat removal a defining concern for an exothermic reactor?",
                    (
                        opt("Cooling has no safety role"),
                        opt(
                            "The Arrhenius feedback (hotter means faster means more heat) "
                            "can cause thermal runaway without adequate cooling and relief",
                            correct=True,
                        ),
                        opt("Because cold reactors react faster"),
                        opt("Only to save pump power"),
                    ),
                    "A jacket or coils plus a sized relief system prevent the "
                    "temperature-rate-temperature runaway loop.",
                ),
                q(
                    "A corrosion allowance is calculated as…",
                    (
                        opt("design pressure times radius"),
                        opt("corrosion rate times design life", correct=True),
                        opt("the joint efficiency times the thickness"),
                        opt("the LMTD times the area"),
                    ),
                    "CA = rate * life gives the sacrificial metal; a high value often "
                    "justifies a more corrosion-resistant alloy.",
                ),
                q(
                    "Which corrosion mechanism especially threatens austenitic stainless "
                    "steel in chloride service?",
                    (
                        opt("Uniform thinning only"),
                        opt("Chloride stress-corrosion cracking and pitting", correct=True),
                        opt("Erosion by clean water"),
                        opt("Galvanic corrosion with an identical metal"),
                    ),
                    "Chlorides drive pitting and SCC of austenitic stainless; the "
                    "mechanism, not just the rate, must drive material choice.",
                ),
                q(
                    "Which pairing of equipment and governing code is correct?",
                    (
                        opt("Atmospheric storage tank - ASME B31.3"),
                        opt("Process piping - API 650"),
                        opt(
                            "Unfired pressure vessel - ASME BPVC Section VIII",
                            correct=True,
                        ),
                        opt("Heat exchanger tubes - API 2000"),
                    ),
                    "Vessels follow ASME VIII; piping follows B31.3; atmospheric tanks "
                    "follow API 650; tank venting follows API 2000.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

PROCESS_EQUIPMENT_DESIGN_COURSES: tuple[SeedCourse, ...] = (_PROCESS_EQUIPMENT_DESIGN,)
