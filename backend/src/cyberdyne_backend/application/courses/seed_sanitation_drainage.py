"""Academy seed content - Sanitation and Urban Drainage.

The infrastructure of public health: how cities supply potable water,
collect and treat the sewage they produce, and manage the rain that falls
on them. The course walks the full water cycle of a city - captation,
treatment and distribution of drinking water; collection and multi-stage
treatment of wastewater; sludge and effluent handling; and micro and macro
urban drainage including sustainable techniques for stormwater and floods.
Every lesson is a direct explanation grounded in real engineering practice
(NBR/ABNT, EPANET, USCS) with a mermaid diagram and a worked sizing example,
followed by a checkpoint quiz; a comprehensive final quiz closes the course.
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


_SANITATION_DRAINAGE = SeedCourse(
    slug="sanitation-drainage",
    title="Sanitation & Urban Drainage",
    description=(
        "The infrastructure of public health - water supply, sewage collection "
        "and treatment, and sustainable urban drainage to manage stormwater and "
        "floods. You walk a city's whole water cycle: captation, treatment and "
        "distribution of drinking water; collection and multi-stage treatment of "
        "wastewater; sludge and effluent handling; and micro and macro drainage "
        "with modern sustainable techniques - with a diagram and a sizing "
        "example in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Sanitation & Urban Drainage

**Basic sanitation** is arguably the most cost-effective public-health
intervention ever engineered: clean water in, dirty water safely out, and
rain kept from flooding the streets. This course covers the three services
that make a city habitable - **water supply**, **sewage** collection and
treatment, and **urban drainage** - as one connected system.

The approach is **concrete and quantitative**: every lesson explains one
idea directly, draws it as a diagram, and works a short real sizing example
(a demand estimate, a pipe diameter, a tank volume, a runoff flow). After
each lesson there is a short quiz; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Water supply systems** - demand, captation, treatment, distribution
2. **Water distribution network modeling** - the EPANET hydraulic model
3. **Sewage collection systems** - gravity sewers that carry it away
4. **Wastewater treatment** - preliminary, primary, secondary, tertiary
5. **Sludge and effluent management** - the solids and the discharge
6. **Urban micro and macro drainage** - streets to rivers
7. **Sustainable urban drainage** - SUDS, LID, permeable pavements
8. **Flood modeling and stormwater plans** - designing for the storm

Throughout we reference real practice and standards - Brazilian **NBR/ABNT**
norms, the **EPANET** hydraulic engine, the **USCS** soil classification -
but keep everything teachable. The goal is that you can read a sanitation
project, follow the numbers, and understand why each structure exists.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What three services does 'basic sanitation' cover in this course?",
                    (
                        opt("Roads, bridges, and tunnels"),
                        opt(
                            "Water supply, sewage collection and treatment, and urban drainage",
                            correct=True,
                        ),
                        opt("Electricity, gas, and telecommunications"),
                        opt("Only drinking water treatment"),
                    ),
                    "The course treats supply, sewage, and drainage as one connected "
                    "urban water system.",
                ),
                q(
                    "What does each content lesson include?",
                    (
                        opt("Only a long historical narrative"),
                        opt(
                            "A direct explanation, a mermaid diagram, and a worked sizing "
                            "example, followed by a quiz",
                            correct=True,
                        ),
                        opt("A quiz only, with no explanation"),
                        opt("A video with no text"),
                    ),
                    "Explanation + diagram + a quantitative example + checkpoint quiz is "
                    "the pattern in every lesson.",
                ),
            ),
        ),
        # -- 1. Water supply systems -----------------------------------
        _t(
            "Water supply systems",
            "10 min",
            """# Water supply systems

A public **water supply system** takes water from a source and delivers it,
potable and pressurized, to every tap in a city. It is a chain of unit
operations, each sized for the population it serves.

The standard stages, in order:

- **Captation** - abstract raw water from a surface source (river, reservoir)
  or a groundwater well, screening out debris.
- **Adduction** - transmission mains carry raw water to the treatment plant,
  and treated water from the plant toward the city.
- **Treatment** - the **ETA** (Estacao de Tratamento de Agua) makes the raw
  water safe: coagulation, flocculation, sedimentation, filtration, and
  disinfection.
- **Reservation** - reservoirs store treated water to buffer demand peaks
  and provide fire and emergency reserve.
- **Distribution** - a pressurized pipe network delivers water to each
  connection.

Everything is sized from **demand**. The design flow starts from a per-capita
consumption **q** (liters per person per day), the population **P**, and peak
coefficients: **k1** for the maximum daily demand and **k2** for the maximum
hourly demand. Typical Brazilian values are q around 150 to 200 L/hab/day,
k1 = 1.2, k2 = 1.5.

```mermaid
graph LR
    SRC["Source river or well"] --> CAP["Captation and screening"]
    CAP --> ADD["Adduction main"]
    ADD --> ETA["Treatment plant"]
    ETA --> RES["Reservoir storage"]
    RES --> NET["Distribution network"]
    NET --> TAP["Consumer taps"]
```

**Worked example - design flows for a town.** Population P = 50000, per-capita
q = 160 L/hab/day, k1 = 1.2, k2 = 1.5.

```text
Average daily demand:
  Qavg = P * q / 86400
       = 50000 * 160 / 86400
       = 8,000,000 / 86400
       = 92.6 L/s

Maximum daily flow (sizes treatment and adduction):
  Qmax.day = k1 * Qavg = 1.2 * 92.6 = 111.1 L/s

Maximum hourly flow (sizes the distribution network):
  Qmax.hour = k1 * k2 * Qavg = 1.2 * 1.5 * 92.6 = 166.7 L/s
```

The rule: **treatment and mains are sized for the max-day flow; the
distribution network for the max-hour flow.** Get the demand right and every
downstream structure follows.
""",
        ),
        quiz_lesson(
            "Quiz: Water supply systems",
            (
                q(
                    "What is the correct order of the main water supply stages?",
                    (
                        opt("Distribution, treatment, captation, source"),
                        opt(
                            "Captation, adduction, treatment, reservation, distribution",
                            correct=True,
                        ),
                        opt("Treatment, captation, distribution, adduction"),
                        opt("Reservation, source, distribution, treatment"),
                    ),
                    "Raw water is captured, transmitted, treated, stored, then "
                    "distributed to taps.",
                ),
                q(
                    "The coefficient k1 in water-demand design represents what?",
                    (
                        opt("The pipe roughness"),
                        opt(
                            "The maximum daily demand factor over the yearly average", correct=True
                        ),
                        opt("The population growth rate"),
                        opt("The chlorine dose"),
                    ),
                    "k1 (typically 1.2) scales the average day to the peak day; k2 (1.5) "
                    "scales to the peak hour.",
                ),
                q(
                    "Which flow is used to size the distribution network?",
                    (
                        opt("The average daily flow"),
                        opt("The maximum hourly flow, Qavg times k1 times k2", correct=True),
                        opt("The minimum night flow"),
                        opt("The fire flow only"),
                    ),
                    "The network must meet the peak-hour demand; treatment and mains use "
                    "the max-day flow.",
                ),
            ),
        ),
        # -- 2. Water distribution network modeling --------------------
        _t(
            "Water distribution network modeling",
            "11 min",
            """# Water distribution network modeling

A distribution network is a graph of **nodes** (junctions where demand is
withdrawn) connected by **links** (pipes, pumps, valves). Sizing it by hand
is impractical beyond a few pipes, so engineers build a **hydraulic model** -
the industry-standard engine is **EPANET** (EPA), and most commercial tools
wrap it.

The model solves two conservation laws simultaneously across the whole
network:

- **Continuity at each node** - flow in equals flow out plus the demand
  withdrawn there.
- **Energy (head loss) along each pipe** - the drop in hydraulic head from
  one node to the next follows a friction equation, usually **Hazen-Williams**
  or **Darcy-Weisbach**.

The Hazen-Williams head loss for a pipe (SI form) is:

```text
Head loss along a pipe (Hazen-Williams, SI):
  hf = 10.67 * L * Q^1.852 / ( C^1.852 * D^4.87 )

where
  hf = head loss (m)
  L  = pipe length (m)
  Q  = flow (m3/s)
  C  = Hazen-Williams roughness coefficient (dimensionless)
  D  = internal diameter (m)

Typical C: new PVC/plastic ~ 150, cement-lined iron ~ 130, old iron ~ 100.
```

EPANET assembles one such equation per pipe plus one continuity equation per
node and iterates (gradient method) until heads and flows are consistent. The
outputs an engineer checks: **pressure at every node** (design target often
10 to 50 m of water column - too low fails service, too high bursts pipes)
and **velocity in every pipe** (target roughly 0.6 to 3.0 m/s - too slow lets
sediment settle, too fast erodes and hammers).

```mermaid
graph TD
    RES["Source reservoir fixed head"] --> N1["Junction node"]
    N1 --> N2["Junction node"]
    N1 --> N3["Junction node"]
    N2 --> N4["Junction node"]
    N3 --> N4
    N4 --> TANK["Storage tank"]
    N2 --> DEM["Demand withdrawn here"]
```

**Worked example - head loss in one main.** A PVC main carries Q = 0.05 m3/s
over L = 800 m, diameter D = 0.30 m, C = 150.

```text
hf = 10.67 * 800 * 0.05^1.852 / ( 150^1.852 * 0.30^4.87 )

  0.05^1.852  = 0.00453
  150^1.852   = 10930
  0.30^4.87   = 0.00293

hf = 10.67 * 800 * 0.00453 / ( 10930 * 0.00293 )
   = 38.66 / 32.02
   = 1.21 m

Velocity check: v = Q / A = 0.05 / (pi/4 * 0.30^2)
   = 0.05 / 0.0707 = 0.71 m/s  -> within 0.6 to 3.0 m/s, OK.
```

Remember: a network model is just continuity plus friction, solved
everywhere at once - you calibrate C against field pressures, then trust the
model to size pipes and site tanks.
""",
        ),
        quiz_lesson(
            "Quiz: Water distribution network modeling",
            (
                q(
                    "In a hydraulic network model, what are the two conservation laws "
                    "solved together?",
                    (
                        opt("Mass of chlorine and mass of fluoride"),
                        opt(
                            "Continuity at each node and energy (head loss) along each pipe",
                            correct=True,
                        ),
                        opt("Ohm's law and Kirchhoff's law"),
                        opt("Momentum and temperature"),
                    ),
                    "Flow balances at each node; head loss follows a friction law along "
                    "each pipe - EPANET iterates both to consistency.",
                ),
                q(
                    "In the Hazen-Williams equation, a higher coefficient C means what?",
                    (
                        opt("A rougher pipe with more head loss"),
                        opt("A smoother pipe with less head loss for the same flow", correct=True),
                        opt("A larger diameter"),
                        opt("A longer pipe"),
                    ),
                    "C rises with smoothness (new PVC ~150, old iron ~100); higher C "
                    "gives lower hf.",
                ),
                q(
                    "Why keep pipe velocity within roughly 0.6 to 3.0 m/s?",
                    (
                        opt("It has no engineering effect"),
                        opt(
                            "Too slow lets sediment settle; too fast causes erosion and "
                            "water hammer",
                            correct=True,
                        ),
                        opt("To make the water colder"),
                        opt("Only to reduce cost"),
                    ),
                    "The velocity window balances self-cleansing against pipe wear and "
                    "surge - a standard design check.",
                ),
            ),
        ),
        # -- 3. Sewage collection systems ------------------------------
        _t(
            "Sewage collection systems",
            "10 min",
            """# Sewage collection systems

Where the supply network is **pressurized and branching outward**, a
**sanitary sewer** system is the mirror image: it runs by **gravity**,
converging inward, collecting used water from every building and carrying it
to the treatment plant.

Key components:

- **House connections** feed into **collector sewers** running under the
  streets.
- Collectors join **trunk sewers** (interceptors) that gather large areas.
- **Manholes** (pocos de visita) sit at every junction, change of direction,
  slope, or diameter, for inspection and cleaning.
- Where gravity cannot continue (a low point), a **lift/pumping station**
  raises the flow to resume gravity flow downstream.

Two design principles dominate. First, the **separate system**: Brazilian
practice (and most modern codes) keeps **sanitary sewage** and **stormwater**
in entirely different pipe networks, so the treatment plant is not flooded by
rain. Second, **partially full gravity flow**: sewers are sized to run
part-full (commonly a maximum depth y/D around 0.75) so a ventilated air space
remains above the flow and carries off gases.

Two hydraulic limits govern the slope:

- A **minimum self-cleansing velocity** (about 0.6 m/s at least once a day, or
  a minimum tractive force near 1.0 Pa) to keep solids moving and avoid
  deposits.
- A **maximum velocity** (about 5 m/s) to limit erosion of the pipe.

```mermaid
graph TD
    H1["House connection"] --> COL["Collector sewer"]
    H2["House connection"] --> COL
    COL --> MH["Manhole junction"]
    MH --> TRUNK["Trunk interceptor"]
    TRUNK --> LIFT["Lift station if needed"]
    LIFT --> ETE["Treatment plant"]
```

**Worked example - self-cleansing slope.** A collector must carry a peak
Q = 20 L/s = 0.020 m3/s in a D = 0.20 m pipe flowing at y/D = 0.75. Manning's
equation gives the required slope:

```text
Manning:  Q = (1/n) * A * R^(2/3) * S^(1/2)   ->   S = ( Q*n / (A * R^(2/3)) )^2

At y/D = 0.75 for D = 0.20 m (circular pipe geometry):
  A (flow area)          = 0.0247 m2
  R (hydraulic radius)   = 0.0608 m
  n (PVC roughness)      = 0.013

  A * R^(2/3) = 0.0247 * 0.0608^(2/3) = 0.0247 * 0.1543 = 0.003811

  S = ( 0.020 * 0.013 / 0.003811 )^2
    = ( 0.0682 )^2
    = 0.00465  ->  about 0.47%, i.e. ~4.7 m drop per km.

Velocity check: v = Q / A = 0.020 / 0.0247 = 0.81 m/s  (> 0.6 m/s, self-cleansing OK)
```

Remember: sanitary sewers are gravity systems designed part-full, on a slope
tuned to stay above the self-cleansing velocity but below the erosion limit -
kept strictly separate from stormwater.
""",
        ),
        quiz_lesson(
            "Quiz: Sewage collection systems",
            (
                q(
                    "How does a sanitary sewer network differ hydraulically from a water "
                    "distribution network?",
                    (
                        opt("Both are pressurized and branch outward"),
                        opt(
                            "Sewers run by gravity, part-full, converging inward; the "
                            "supply network is pressurized and branches outward",
                            correct=True,
                        ),
                        opt("Sewers are always pumped along their whole length"),
                        opt("There is no difference"),
                    ),
                    "Gravity, part-full flow, converging to the plant is the sewer "
                    "pattern; supply is pressurized and diverging.",
                ),
                q(
                    "What is the 'separate system' principle?",
                    (
                        opt("Each house has its own treatment plant"),
                        opt(
                            "Sanitary sewage and stormwater are carried in entirely "
                            "different pipe networks",
                            correct=True,
                        ),
                        opt("Men's and women's sewage are separated"),
                        opt("Treated and raw water share a pipe"),
                    ),
                    "Keeping rain out of the sanitary network prevents the treatment "
                    "plant from being overwhelmed by storms.",
                ),
                q(
                    "Why is a minimum self-cleansing velocity (about 0.6 m/s) required?",
                    (
                        opt("To cool the sewage"),
                        opt(
                            "To keep solids in suspension so they do not deposit and clog",
                            correct=True,
                        ),
                        opt("To increase the pipe diameter"),
                        opt("To raise the water table"),
                    ),
                    "Below the self-cleansing velocity, solids settle and the sewer "
                    "silts up; a matching tractive force criterion is also used.",
                ),
            ),
        ),
        # -- 4. Wastewater treatment processes -------------------------
        _t(
            "Wastewater treatment processes",
            "11 min",
            """# Wastewater treatment processes

The **ETE** (Estacao de Tratamento de Esgoto) removes pollutants from sewage
before returning the water to a river or the sea. Treatment is organized in
**levels**, each targeting a coarser-to-finer class of pollutant:

- **Preliminary** - physical removal of coarse solids and grit. **Bar
  screens** catch rags and debris; **grit chambers** let sand settle. Protects
  downstream pumps and pipes.
- **Primary** - **sedimentation** in quiescent tanks lets settleable organic
  solids fall out as raw sludge and floatables be skimmed. Removes roughly
  25 to 40% of the **BOD**.
- **Secondary** - **biological** treatment: microorganisms consume the
  dissolved and colloidal organic matter. Common processes are **activated
  sludge** (aerated tank plus a secondary clarifier) and **anaerobic reactors**
  such as the **UASB**, widely used in Brazil for warm climates. Removes 85 to
  95% of BOD overall.
- **Tertiary/advanced** - polishing for specific targets: **nutrient removal**
  (nitrogen and phosphorus, to prevent eutrophication), filtration, and
  **disinfection** (chlorine, UV, or ozone) to kill pathogens before
  discharge.

The master pollutant indicator is **BOD** (Biochemical Oxygen Demand): the
oxygen microbes need to break down the organic load. Raw domestic sewage is
around 300 mg/L BOD; Brazilian discharge standards (CONAMA 430) require either
a maximum of 120 mg/L or at least 60% removal, and states often demand more.

```mermaid
graph LR
    RAW["Raw sewage"] --> PRE["Preliminary screens and grit"]
    PRE --> PRIM["Primary sedimentation"]
    PRIM --> SEC["Secondary biological"]
    SEC --> TERT["Tertiary nutrients and disinfection"]
    TERT --> OUT["Treated effluent to river"]
    PRIM --> SL["Sludge stream"]
    SEC --> SL
```

**Worked example - required removal efficiency.** Influent BOD = 320 mg/L. The
river-discharge limit is 30 mg/L (a stricter state standard).

```text
Overall efficiency needed:
  E = (BOD.in - BOD.out) / BOD.in
    = (320 - 30) / 320
    = 290 / 320
    = 0.906  ->  90.6% removal.

Primary alone (~35%) leaves 320 * (1 - 0.35) = 208 mg/L  -> not enough.
Add secondary activated sludge (~90% of what enters it):
  208 * (1 - 0.90) = 20.8 mg/L  -> below 30 mg/L, target met.
```

Remember: treatment is staged by pollutant size and type - physical, then
settling, then biological, then polishing - and you size each stage to hit
the required **BOD** (and nutrient) removal for the receiving water.
""",
        ),
        quiz_lesson(
            "Quiz: Wastewater treatment processes",
            (
                q(
                    "Which sequence lists the treatment levels in the correct order?",
                    (
                        opt("Secondary, primary, preliminary, tertiary"),
                        opt("Preliminary, primary, secondary, tertiary", correct=True),
                        opt("Tertiary, secondary, primary, preliminary"),
                        opt("Primary, preliminary, tertiary, secondary"),
                    ),
                    "Coarse physical (preliminary), settling (primary), biological "
                    "(secondary), polishing (tertiary).",
                ),
                q(
                    "What does secondary (biological) treatment mainly remove?",
                    (
                        opt("Coarse rags and grit"),
                        opt(
                            "Dissolved and colloidal organic matter, via microorganisms",
                            correct=True,
                        ),
                        opt("Only heavy metals"),
                        opt("Nothing - it is decorative"),
                    ),
                    "Activated sludge or a UASB reactor uses microbes to consume the "
                    "organic load, cutting BOD by 85 to 95%.",
                ),
                q(
                    "What does BOD measure?",
                    (
                        opt("The pipe diameter"),
                        opt(
                            "The oxygen microorganisms need to break down the organic "
                            "matter - the organic pollution load",
                            correct=True,
                        ),
                        opt("The chlorine residual"),
                        opt("The water temperature"),
                    ),
                    "Biochemical Oxygen Demand is the master indicator of organic "
                    "load; discharge standards are written around it.",
                ),
            ),
        ),
        # -- 5. Sludge and effluent management -------------------------
        _t(
            "Sludge and effluent management",
            "10 min",
            """# Sludge and effluent management

Treating sewage does not make pollutants vanish - it **concentrates** them
into two output streams that must themselves be managed: the **treated
effluent** (the clarified liquid returned to the environment) and the
**sludge** (the solids removed along the way, called lodo in Brazil).

**Sludge** is the harder problem: it leaves the process as a thin slurry
(often 1 to 3% solids) that is bulky, odorous, and biologically active. The
standard processing train reduces its volume and stabilizes it:

- **Thickening** - concentrate the solids (gravity thickener or flotation),
  cutting volume before anything else.
- **Digestion/stabilization** - **anaerobic** or **aerobic** digestion (or
  lime/alkaline stabilization) reduces volatile solids, destroys pathogens,
  and cuts odor. Anaerobic digestion also yields **biogas** (methane) that can
  power the plant.
- **Dewatering** - centrifuges, belt/plate filter presses, or drying beds
  remove water to produce a spadable **cake** (15 to 30% solids).
- **Final disposal** - sanitary landfill, or beneficial reuse as agricultural
  **biosolids** where stabilization meets standards (in Brazil, CONAMA 375).

The **effluent** side is about meeting the discharge permit for the receiving
water: residual BOD, suspended solids, nutrients, coliforms, pH. Where the
receiving body is sensitive, an extra **disinfection** or **polishing** step
is added, or the effluent is reused (irrigation, industrial cooling).

```mermaid
graph TD
    ETE["Treatment process"] --> EFF["Effluent stream"]
    ETE --> RAW["Raw sludge stream"]
    EFF --> DISC["Discharge or reuse"]
    RAW --> THK["Thickening"]
    THK --> DIG["Digestion and stabilization"]
    DIG --> DEW["Dewatering to cake"]
    DEW --> DISP["Landfill or biosolids reuse"]
```

**Worked example - dewatering shrinks the volume.** A plant produces sludge at
1.5% solids and dewaters it to a 25% cake. How much does the volume shrink,
for the same mass of dry solids?

```text
Volume is inversely proportional to solids concentration (same dry mass, water ~ constant density):

  V.cake / V.slurry = Cs.slurry / Cs.cake = 1.5% / 25% = 0.06

So the cake is about 6% of the original slurry volume - a ~94% reduction.

If the slurry stream is 50 m3/day:
  Cake volume = 0.06 * 50 = 3 m3/day to haul away.
```

Remember: sanitation moves and concentrates pollution - the plant is only
finished when both streams are dealt with. Thicken, stabilize, and dewater the
sludge; meet the permit (or reuse it) for the effluent.
""",
        ),
        quiz_lesson(
            "Quiz: Sludge and effluent management",
            (
                q(
                    "Why does treating sewage still leave a disposal problem?",
                    (
                        opt("Treatment destroys all matter completely"),
                        opt(
                            "It concentrates pollutants into two streams - treated "
                            "effluent and sludge - that must themselves be managed",
                            correct=True,
                        ),
                        opt("Effluent needs no permit"),
                        opt("Sludge evaporates on its own"),
                    ),
                    "Pollutants are moved and concentrated, not made to vanish; both the "
                    "liquid and solid outputs need handling.",
                ),
                q(
                    "What is the correct order of the sludge processing train?",
                    (
                        opt("Dewatering, thickening, digestion, disposal"),
                        opt(
                            "Thickening, digestion/stabilization, dewatering, disposal",
                            correct=True,
                        ),
                        opt("Disposal, digestion, thickening, dewatering"),
                        opt("Digestion, disposal, thickening, dewatering"),
                    ),
                    "Concentrate (thicken), stabilize (digest), remove water (dewater), "
                    "then dispose or reuse.",
                ),
                q(
                    "A useful by-product of anaerobic sludge digestion is:",
                    (
                        opt("Chlorine gas"),
                        opt("Biogas (methane) that can power the plant", correct=True),
                        opt("Drinking water"),
                        opt("Grit"),
                    ),
                    "Anaerobic digestion reduces volatile solids and yields methane-rich "
                    "biogas usable for energy.",
                ),
            ),
        ),
        # -- 6. Urban micro- and macro-drainage ------------------------
        _t(
            "Urban micro- and macro-drainage",
            "11 min",
            """# Urban micro- and macro-drainage

**Urban drainage** is the third sanitation service: managing the **rain** that
falls on a city. Unlike sewage, stormwater is clean-ish but arrives in huge,
sudden volumes, and urbanization makes it worse - roofs and pavement are
**impervious**, so water that once soaked in now runs off fast.

Drainage is split by scale:

- **Microdrainage** - the local, in-street system: roof and lot drainage,
  street gutters, **inlets** (bocas de lobo), the buried storm sewer pipes,
  and manholes. Sized for frequent storms (return period **T** around 2 to 10
  years).
- **Macrodrainage** - the receiving system for whole catchments: main
  channels, natural and canalized **streams and rivers**, detention/retention
  basins, and large culverts. Sized for rarer, larger storms (T of 25, 50, or
  100 years).

The workhorse for small urban catchments is the **Rational Method**, which
turns a design rainfall intensity into a peak runoff flow:

```text
Rational Method:   Q = C * i * A / 3.6    (SI, Q in m3/s)

where
  Q = peak runoff flow (m3/s)
  C = runoff coefficient (0 to 1): fraction of rain that runs off
      (asphalt ~0.90, roofs ~0.85, lawns ~0.15)
  i = rainfall intensity (mm/h) for the design return period and a
      duration equal to the catchment's time of concentration tc
  A = drainage area (km2)
  3.6 = unit-conversion constant
```

The **time of concentration tc** is how long water takes to travel from the
farthest point of the catchment to the outlet; you read **i** off an **IDF**
(intensity-duration-frequency) curve for that tc and the chosen return period.

```mermaid
graph TD
    RAIN["Design rainfall on catchment"] --> ROOF["Roofs and lots"]
    RAIN --> STREET["Streets and gutters"]
    ROOF --> INLET["Inlets bocas de lobo"]
    STREET --> INLET
    INLET --> MICRO["Microdrainage storm sewers"]
    MICRO --> MACRO["Macrodrainage channels and rivers"]
    MACRO --> DET["Detention basin then outfall"]
```

**Worked example - peak runoff by the Rational Method.** A 0.25 km2 catchment
is 70% paved (C = 0.90) and 30% green (C = 0.20). For the design storm,
i = 90 mm/h.

```text
Weighted runoff coefficient:
  C = 0.70 * 0.90 + 0.30 * 0.20
    = 0.63 + 0.06
    = 0.69

Peak flow:
  Q = C * i * A / 3.6
    = 0.69 * 90 * 0.25 / 3.6
    = 15.525 / 3.6
    = 4.31 m3/s
```

Remember: microdrainage handles the frequent street-level storm, macrodrainage
the rare catchment-scale flood, and the Rational Method (Q = C i A / 3.6) links
a design rainfall to the peak flow you must convey.
""",
        ),
        quiz_lesson(
            "Quiz: Urban micro- and macro-drainage",
            (
                q(
                    "What distinguishes microdrainage from macrodrainage?",
                    (
                        opt("Micro is for sewage, macro is for water supply"),
                        opt(
                            "Micro is the local in-street system for frequent storms; "
                            "macro is the catchment-scale channel and river system for "
                            "rarer, larger storms",
                            correct=True,
                        ),
                        opt("They are the same thing at different times of day"),
                        opt("Micro uses pumps, macro never does"),
                    ),
                    "Scale and return period set them apart: streets/inlets/pipes (T~2 "
                    "to 10 yr) versus channels/rivers/basins (T~25 to 100 yr).",
                ),
                q(
                    "In the Rational Method Q = C i A / 3.6, what is the coefficient C?",
                    (
                        opt("The pipe roughness"),
                        opt("The fraction of rainfall that becomes runoff (0 to 1)", correct=True),
                        opt("The rainfall duration"),
                        opt("The channel slope"),
                    ),
                    "C is the runoff coefficient; paved surfaces (~0.9) run off far more "
                    "than lawns (~0.15), so urbanization raises it.",
                ),
                q(
                    "Why does urbanization increase peak stormwater runoff?",
                    (
                        opt("Rain falls harder over cities"),
                        opt(
                            "Impervious roofs and pavement stop water soaking in, so more "
                            "runs off, faster",
                            correct=True,
                        ),
                        opt("Cities have fewer people"),
                        opt("Pipes create extra rain"),
                    ),
                    "Sealing the ground raises both the runoff coefficient and the speed "
                    "of concentration, enlarging the flood peak.",
                ),
            ),
        ),
        # -- 7. Sustainable urban drainage -----------------------------
        _t(
            "Sustainable urban drainage",
            "10 min",
            """# Sustainable urban drainage

Traditional drainage tries to move stormwater **away as fast as possible** -
which just pushes the flood downstream and makes it worse for everyone below.
The modern paradigm inverts that goal: **hold the water where it falls, slow
it down, and let it soak in.** The same idea has several names:

- **SUDS** - Sustainable Urban Drainage Systems (UK).
- **LID** - Low Impact Development (USA).
- **BMPs** - Best Management Practices; **Sponge City** (China).

The unifying principle is to **mimic the pre-development hydrology**: restore
infiltration, evapotranspiration, and storage that paving removed, so the
catchment behaves more like it did before it was built on. Common measures:

- **Permeable pavements** - porous asphalt, pervious concrete, or block pavers
  that let rain infiltrate through the surface into a stone reservoir below,
  instead of running off.
- **Bioretention and rain gardens** - shallow planted depressions that pond,
  filter, and infiltrate runoff.
- **Green roofs** - soil and vegetation that store and evapotranspire rain.
- **Infiltration trenches and soakaways**, **swales** (grassed channels), and
  **detention/retention basins** that store the peak and release it slowly.

Besides cutting the peak flow, these measures **treat** the water (removing
sediment and pollutants), recharge groundwater, and cool and green the city.

```mermaid
graph TD
    RAIN["Rainfall on the lot"] --> GREEN["Green roof stores and evaporates"]
    RAIN --> PERM["Permeable pavement infiltrates"]
    GREEN --> RG["Rain garden bioretention"]
    PERM --> RES["Stone reservoir stores"]
    RG --> INF["Infiltration to groundwater"]
    RES --> INF
    RG --> SLOW["Slow release to drainage"]
```

**Worked example - sizing a permeable-pavement reservoir.** A 500 m2 permeable
lot must capture a design rainfall depth of 40 mm without overflowing. The
sub-base stone has a void ratio (porosity) of 30%.

```text
Volume of rain to store:
  V.rain = area * depth = 500 m2 * 0.040 m = 20 m3

Storage available per metre of stone depth:
  usable = porosity = 0.30, so 1 m of stone over 500 m2 holds
  500 * 1 * 0.30 = 150 m3 per metre of depth.

Required stone-reservoir depth:
  d = V.rain / (area * porosity)
    = 20 / (500 * 0.30)
    = 20 / 150
    = 0.133 m  ->  about 0.15 m of stone sub-base (rounded up).
```

Remember: sustainable drainage manages the storm **at source** - infiltrate,
detain, and slowly release - so the city sheds less water, and cleaner water,
than a pipe-everything-away approach.
""",
        ),
        quiz_lesson(
            "Quiz: Sustainable urban drainage",
            (
                q(
                    "What is the core principle behind SUDS / LID?",
                    (
                        opt("Move stormwater away as fast as possible"),
                        opt(
                            "Hold water where it falls, slow it down, and let it soak in, "
                            "mimicking pre-development hydrology",
                            correct=True,
                        ),
                        opt("Pipe all rain directly into rivers"),
                        opt("Treat stormwater like sewage"),
                    ),
                    "Source control that restores infiltration and storage, rather than "
                    "rapid conveyance that shifts the flood downstream.",
                ),
                q(
                    "How does a permeable pavement reduce runoff?",
                    (
                        opt("It heats the water so it evaporates instantly"),
                        opt(
                            "It lets rain infiltrate through the surface into a stone "
                            "reservoir below instead of running off",
                            correct=True,
                        ),
                        opt("It pumps water uphill"),
                        opt("It seals the ground more tightly"),
                    ),
                    "Porous surface plus a stone sub-base stores and infiltrates the "
                    "rain at source.",
                ),
                q(
                    "Besides cutting peak flow, what extra benefit do SUDS measures give?",
                    (
                        opt("They increase impervious area"),
                        opt(
                            "They treat the water (removing pollutants), recharge "
                            "groundwater, and cool and green the city",
                            correct=True,
                        ),
                        opt("They eliminate the need for any drainage"),
                        opt("They raise the runoff coefficient"),
                    ),
                    "Water quality, groundwater recharge, and urban cooling are "
                    "co-benefits of source control.",
                ),
            ),
        ),
        # -- 8. Flood modeling and stormwater management plans ---------
        _t(
            "Flood modeling and stormwater management plans",
            "11 min",
            """# Flood modeling and stormwater management plans

Sizing single pipes with the Rational Method is fine for small catchments, but
a whole city needs a **model** and a **plan**. Flood modeling links rainfall to
water levels so engineers can see *where* and *how deep* flooding will be, and
test fixes before building them.

A flood model has two coupled parts:

- **Hydrology** - turn a design storm into flow over time (a **hydrograph**),
  accounting for infiltration losses and catchment response.
- **Hydraulics** - route those flows through pipes, channels, and floodplains
  (1D in the network, often **2D** across the terrain surface) to get water
  depth and extent. Tools such as **SWMM** (EPA Storm Water Management Model),
  HEC-RAS, and MIKE do this.

A key idea a model captures that a simple pipe calc misses: **detention**. A
storage basin cannot reduce the total volume of rain, but by holding the peak
and releasing it slowly it **cuts the peak flow** downstream - flattening the
hydrograph so the receiving channel is not overwhelmed.

The engineering wraps into a **Stormwater / Drainage Master Plan** (in Brazil
a Plano Diretor de Drenagem), which sets design return periods, maps flood
risk, protects floodplains and drainage easements, and often mandates
**on-site detention** so new development does not increase the peak leaving
its lot.

```mermaid
graph TD
    STORM["Design storm IDF"] --> HYDRO["Hydrology model hydrograph"]
    HYDRO --> ROUTE["Hydraulic routing 1D and 2D"]
    ROUTE --> MAP["Flood depth and extent map"]
    MAP --> PLAN["Drainage master plan"]
    PLAN --> DET["Detention basins and on-site storage"]
    DET --> HYDRO
```

**Worked example - detention basin volume (simple mass balance).** A
development's design storm produces an inflow peak of Q.in = 4.0 m3/s over an
effective duration of 30 min. The downstream channel can safely accept only
Q.out = 1.5 m3/s. Estimate the storage a detention basin must provide.

```text
Approximate required storage = (excess inflow) * duration:

  Q.excess = Q.in - Q.out = 4.0 - 1.5 = 2.5 m3/s
  duration = 30 min = 1800 s

  V.storage ~= Q.excess * duration
            = 2.5 * 1800
            = 4500 m3

So a basin of roughly 4500 m3 (e.g. 1.5 m deep over ~3000 m2) holds the peak
and releases it at the safe 1.5 m3/s rate. (A full design routes the inflow
hydrograph through the basin's stage-storage-discharge curve; this mass
balance is the first-cut estimate.)
```

Remember: model the storm as a hydrograph, route it to get flood depth, and
use **detention** plus a master plan to cap the peak - so the city grows
without pushing its floods onto everyone downstream.
""",
        ),
        quiz_lesson(
            "Quiz: Flood modeling and stormwater management plans",
            (
                q(
                    "What are the two coupled parts of a flood model?",
                    (
                        opt("Water supply and sewage"),
                        opt(
                            "Hydrology (rainfall to a flow hydrograph) and hydraulics "
                            "(routing flows to get water depth and extent)",
                            correct=True,
                        ),
                        opt("Coagulation and disinfection"),
                        opt("Thickening and dewatering"),
                    ),
                    "Hydrology produces the hydrograph; hydraulics routes it through "
                    "pipes, channels, and floodplains (tools like SWMM, HEC-RAS).",
                ),
                q(
                    "How does a detention basin reduce downstream flooding?",
                    (
                        opt("It makes the total rainfall volume disappear"),
                        opt(
                            "It stores the peak and releases it slowly, cutting the peak "
                            "flow while total volume is unchanged",
                            correct=True,
                        ),
                        opt("It speeds the water downstream faster"),
                        opt("It treats the water chemically"),
                    ),
                    "Detention flattens the hydrograph: same volume, lower peak, so the "
                    "receiving channel is not overwhelmed.",
                ),
                q(
                    "What does a Stormwater / Drainage Master Plan typically require of "
                    "new development?",
                    (
                        opt("That it pave over all green space"),
                        opt(
                            "On-site detention so the development does not increase the "
                            "peak flow leaving its lot",
                            correct=True,
                        ),
                        opt("That it discharge sewage into the storm drain"),
                        opt("That it ignore return periods"),
                    ),
                    "Master plans set return periods, map flood risk, protect "
                    "floodplains, and mandate on-site storage to hold the peak constant.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Which flow governs the sizing of a water distribution network?",
                    (
                        opt("The average daily flow"),
                        opt("The maximum hourly flow (Qavg times k1 times k2)", correct=True),
                        opt("The minimum night flow"),
                        opt("The sludge flow"),
                    ),
                    "The network must satisfy the peak hour; treatment and mains use the "
                    "max-day flow (k1 only).",
                ),
                q(
                    "In a hydraulic network model, head loss along a pipe is computed with:",
                    (
                        opt("Ohm's law"),
                        opt(
                            "A friction equation such as Hazen-Williams or Darcy-Weisbach",
                            correct=True,
                        ),
                        opt("The Rational Method"),
                        opt("Manning's equation for BOD"),
                    ),
                    "Continuity at nodes plus a friction head-loss law per pipe - what "
                    "EPANET solves iteratively.",
                ),
                q(
                    "Why are sanitary sewers designed to flow only part-full by gravity?",
                    (
                        opt("To save on pipe cost only"),
                        opt(
                            "To keep a ventilated air space above the flow and stay above "
                            "the self-cleansing velocity",
                            correct=True,
                        ),
                        opt("Because they are pressurized"),
                        opt("To mix in stormwater"),
                    ),
                    "Part-full gravity flow ventilates gases and, on the right slope, "
                    "keeps velocity self-cleansing but below the erosion limit.",
                ),
                q(
                    "What does secondary wastewater treatment remove, and how?",
                    (
                        opt("Grit, using bar screens"),
                        opt(
                            "Dissolved and colloidal organic matter, using "
                            "microorganisms (activated sludge or a UASB reactor)",
                            correct=True,
                        ),
                        opt("Heavy metals, using magnets"),
                        opt("Nothing measurable"),
                    ),
                    "Biological secondary treatment cuts BOD by 85 to 95% after "
                    "preliminary and primary stages.",
                ),
                q(
                    "Raw domestic sewage has a BOD around 300 mg/L. If the discharge "
                    "limit is 30 mg/L, roughly what overall removal is needed?",
                    (
                        opt("About 10%"),
                        opt("About 50%"),
                        opt("About 90%", correct=True),
                        opt("About 99.9%"),
                    ),
                    "(300 - 30)/300 = 0.90, so about 90% removal - primary plus "
                    "secondary treatment.",
                ),
                q(
                    "What is the correct order of the sludge processing train?",
                    (
                        opt("Disposal, dewatering, digestion, thickening"),
                        opt(
                            "Thickening, digestion/stabilization, dewatering, disposal",
                            correct=True,
                        ),
                        opt("Digestion, disposal, thickening, dewatering"),
                        opt("Dewatering, disposal, thickening, digestion"),
                    ),
                    "Concentrate, stabilize, remove water, then landfill or reuse as biosolids.",
                ),
                q(
                    "In the Rational Method Q = C i A / 3.6, a fully paved catchment "
                    "versus a grassed one has:",
                    (
                        opt("A lower runoff coefficient C"),
                        opt(
                            "A higher runoff coefficient C and thus a larger peak flow",
                            correct=True,
                        ),
                        opt("The same C"),
                        opt("No runoff at all"),
                    ),
                    "Impervious paving has C ~0.9 versus lawn ~0.15, so it produces a "
                    "much larger peak - the core reason urbanization worsens floods.",
                ),
                q(
                    "What is the unifying goal of SUDS / LID / sponge-city drainage?",
                    (
                        opt("Convey stormwater away as fast as possible"),
                        opt(
                            "Manage stormwater at source - infiltrate, detain, and slowly "
                            "release - mimicking pre-development hydrology",
                            correct=True,
                        ),
                        opt("Combine sewage and stormwater in one pipe"),
                        opt("Increase impervious cover"),
                    ),
                    "Source control restores infiltration and storage, cutting the peak "
                    "and treating the water instead of shifting the flood downstream.",
                ),
                q(
                    "A detention basin reduces downstream flooding by:",
                    (
                        opt("Removing the rainfall volume entirely"),
                        opt(
                            "Storing the peak and releasing it slowly, so peak flow drops "
                            "while total volume stays the same",
                            correct=True,
                        ),
                        opt("Speeding water to the river"),
                        opt("Disinfecting the runoff"),
                    ),
                    "It flattens the hydrograph - same volume, lower peak - protecting "
                    "the receiving channel.",
                ),
                q(
                    "Why does modern practice keep sanitary sewage and stormwater in "
                    "separate networks?",
                    (
                        opt("To use more pipe for its own sake"),
                        opt(
                            "So rain does not flood and overwhelm the sewage treatment plant",
                            correct=True,
                        ),
                        opt("Because stormwater is more polluted than sewage"),
                        opt("To mix the two before the river"),
                    ),
                    "The separate system keeps the treatment plant sized for sewage, not "
                    "for every storm - a foundational sanitation principle.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

SANITATION_DRAINAGE_COURSES: tuple[SeedCourse, ...] = (_SANITATION_DRAINAGE,)
