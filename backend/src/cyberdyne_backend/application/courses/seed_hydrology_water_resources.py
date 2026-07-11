"""Academy seed content - Hydrology and Water Resources.

Quantifying water in the environment so it can be engineered: the
hydrologic cycle, how rainfall is measured and analyzed, what happens to
water when it hits the ground (infiltration and evapotranspiration), how
watersheds turn rain into streamflow, the rational and SCS methods for
predicting runoff, IDF curves and peak flow, flood frequency and return
periods, and how a changing climate reshapes water resources management.
Every lesson is a direct explanation with a worked calculation and a
mermaid diagram, followed by a checkpoint quiz; the course closes with a
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


_HYDROLOGY_WATER_RESOURCES = SeedCourse(
    slug="hydrology-water-resources",
    title="Hydrology & Water Resources",
    description=(
        "Quantifying water in the environment - the hydrologic cycle, "
        "rainfall, watersheds, runoff and floods - to design resilient "
        "water infrastructure under a changing climate. Every lesson pairs "
        "a direct explanation with a worked hydrologic calculation and a "
        "diagram, grounded in standard practice (rational method, SCS "
        "curve number, IDF curves, flood frequency)."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Hydrology and Water Resources

Hydrology is the science of **water on and below the land surface** - how
much falls as rain, where it goes, and how fast it moves. Water resources
engineering turns that science into design: culverts sized for a storm,
reservoirs sized for a drought, levees sized for a flood. This course
connects the two, from a raindrop to a hydrograph to a design discharge.

The approach is **quantitative and concrete**: every lesson explains one
idea directly, works a short calculation you could run yourself (a water
balance, a runoff estimate, a return period), and draws the idea as a
diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **The hydrologic cycle** - the water balance that governs everything
2. **Precipitation and rainfall analysis** - measuring and averaging rain
3. **Infiltration and evapotranspiration** - the losses before runoff
4. **Watersheds and hydrographs** - how a basin responds to a storm
5. **Rainfall-runoff modeling** - the rational method and the SCS method
6. **Peak flow and IDF curves** - the design storm and its intensity
7. **Floods and extreme events** - return period and frequency analysis
8. **Climate change and water resources** - designing under nonstationarity

Numbers here follow common engineering practice (SI units, the rational
and SCS/NRCS methods, Gumbel frequency analysis). The point is not to
memorize a formula but to understand what each term means physically, so
you can size real infrastructure with judgment.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is hydrology, in one line?",
                    (
                        opt("The study of ocean currents only"),
                        opt(
                            "The science of water on and below the land surface - how "
                            "much falls, where it goes, and how fast it moves",
                            correct=True,
                        ),
                        opt("The chemistry of drinking water treatment"),
                        opt("A method for pouring concrete underwater"),
                    ),
                    "Hydrology quantifies the movement and storage of water; water "
                    "resources engineering turns that into design.",
                ),
                q(
                    "How is each content lesson structured in this course?",
                    (
                        opt("Pure theory with no numbers"),
                        opt(
                            "A direct explanation, a worked hydrologic calculation, and "
                            "a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Only multiple-choice questions"),
                        opt("A video with no text"),
                    ),
                    "Explanation plus a concrete calculation plus a diagram, then a "
                    "checkpoint quiz - and a final quiz at the end.",
                ),
            ),
        ),
        # -- 1. The hydrologic cycle -----------------------------------
        _t(
            "The hydrologic cycle",
            "9 min",
            """# The hydrologic cycle

The **hydrologic cycle** is the continuous circulation of water through
the atmosphere, land, and oceans, driven by solar energy and gravity.
Water **evaporates** from oceans and soil, **transpires** from plants,
condenses into clouds, falls as **precipitation**, and returns to the sea
as **surface runoff** and **groundwater flow**. No water is created or
destroyed - it is only stored and moved between reservoirs.

The engineering tool that captures this is the **water balance**. Over a
watershed and a time period, what comes in must equal what leaves plus
the change in storage:

- **P** = precipitation (in)
- **Q** = runoff / streamflow out (out)
- **ET** = evapotranspiration (out)
- **G** = net groundwater exchange (out or in)
- **dS** = change in storage (soil moisture, snowpack, reservoirs)

```mermaid
graph LR
    OCEAN["Ocean and soil"] --> EVAP["Evaporation"]
    PLANTS["Vegetation"] --> TRANS["Transpiration"]
    EVAP --> CLOUD["Condensation"]
    TRANS --> CLOUD
    CLOUD --> PRECIP["Precipitation"]
    PRECIP --> RUNOFF["Surface runoff"]
    PRECIP --> INFIL["Infiltration"]
    RUNOFF --> OCEAN
    INFIL --> GW["Groundwater to ocean"]
```

**Worked example - annual water balance of a basin.** A 50 km2 catchment
receives 1200 mm of rain in a year. Streamflow at the outlet totals
480 mm depth, and evapotranspiration is estimated at 650 mm. What is the
change in storage?

```text
Water balance:  dS = P - Q - ET
  dS = 1200 - 480 - 650  =  70 mm

Interpretation: +70 mm of water was ADDED to storage this year
(recharged soil moisture and aquifers). A negative dS would mean the
basin drew DOWN its stored water - a drought signal.

Runoff coefficient (fraction of rain that became streamflow):
  C = Q / P = 480 / 1200 = 0.40  (40 percent)
```

Remember: the water balance is bookkeeping for a watershed. Every
hydrologic design - reservoir yield, drought reserve, recharge estimate -
starts by deciding which term you are solving for.
""",
        ),
        quiz_lesson(
            "Quiz: The hydrologic cycle",
            (
                q(
                    "What drives the hydrologic cycle?",
                    (
                        opt("Only ocean tides"),
                        opt(
                            "Solar energy (evaporation) and gravity (precipitation and "
                            "flow), circulating a fixed amount of water",
                            correct=True,
                        ),
                        opt("Chemical reactions in the soil"),
                        opt("Human pumping alone"),
                    ),
                    "The sun lifts water into the atmosphere; gravity brings it back "
                    "down and moves it seaward. Water is conserved, not created.",
                ),
                q(
                    "In the water balance dS = P - Q - ET, what does a positive dS mean?",
                    (
                        opt("The basin lost stored water"),
                        opt(
                            "Water was added to storage - soil moisture and aquifers "
                            "recharged over the period",
                            correct=True,
                        ),
                        opt("Precipitation was zero"),
                        opt("Evapotranspiration exceeded precipitation"),
                    ),
                    "Inputs exceeded outputs, so storage grew. Negative dS is a "
                    "drawdown (drought) signal.",
                ),
                q(
                    "A basin gets 1000 mm of rain and produces 300 mm of runoff. What "
                    "is the runoff coefficient?",
                    (
                        opt("0.03"),
                        opt("3.3"),
                        opt("0.30 - about 30 percent of rain became streamflow", correct=True),
                        opt("It cannot be computed"),
                    ),
                    "C = Q / P = 300 / 1000 = 0.30. The rest was lost to ET, "
                    "infiltration, and storage.",
                ),
            ),
        ),
        # -- 2. Precipitation and rainfall analysis --------------------
        _t(
            "Precipitation and rainfall analysis",
            "10 min",
            """# Precipitation and rainfall analysis

**Precipitation** is the input that everything downstream depends on, so
measuring and summarizing it well is the first job in any study. Rain is
recorded at point **gauges** (tipping-bucket or weighing), and increasingly
estimated over areas by **weather radar** and **satellite**. A single
gauge measures one point; a watershed needs an **areal average**.

Three classic methods convert point gauges into a basin-average rainfall:

- **Arithmetic mean** - just average the gauges. Fine when gauges are
  evenly spread and terrain is flat.
- **Thiessen polygons** - weight each gauge by the area closest to it
  (its polygon). Handles uneven gauge spacing.
- **Isohyetal method** - draw contours of equal rainfall (isohyets) and
  weight by the area between them. Best where orography matters, but
  needs judgment.

```mermaid
graph TD
    GAUGES["Point rain gauges"] --> ARITH["Arithmetic mean"]
    GAUGES --> THIESSEN["Thiessen polygons"]
    GAUGES --> ISO["Isohyetal contours"]
    ARITH --> AREAL["Areal average rainfall"]
    THIESSEN --> AREAL
    ISO --> AREAL
    AREAL --> DESIGN["Input to runoff design"]
```

**Worked example - Thiessen areal average.** Three gauges cover a basin.
Each gauge has a rainfall depth and a Thiessen polygon area:

```text
Gauge   Rain P (mm)   Polygon area A (km2)   P * A
  A         62              18               1116
  B         48              25               1200
  C         75              12                900
-------------------------------------------------
 Sum                        55               3216

Thiessen average = sum(P*A) / sum(A)
                 = 3216 / 55  =  58.5 mm

A plain arithmetic mean would give (62 + 48 + 75) / 3 = 61.7 mm.
Thiessen is lower here because gauge B (the driest) covers the
largest area - area weighting matters.
```

A second everyday task is checking a gauge record for consistency. A
**double-mass curve** plots a station's cumulative rainfall against the
cumulative average of nearby stations; a change in slope flags when a
gauge was moved or its exposure changed, and the record is corrected by
the slope ratio.

Remember: garbage in, garbage out. Get the rainfall input right -
correctly averaged over the basin and checked for consistency - before
trusting any runoff or flood number that follows.
""",
        ),
        quiz_lesson(
            "Quiz: Precipitation and rainfall analysis",
            (
                q(
                    "Why do the Thiessen and isohyetal methods exist instead of just "
                    "averaging the gauges?",
                    (
                        opt("They are older and slower"),
                        opt(
                            "They weight point gauges by area, giving a better basin "
                            "average when gauges are unevenly spaced or terrain varies",
                            correct=True,
                        ),
                        opt("They ignore the rainfall data"),
                        opt("They only work for a single gauge"),
                    ),
                    "A plain mean assumes each gauge represents equal area; Thiessen "
                    "and isohyetal account for the area each gauge actually represents.",
                ),
                q(
                    "In the Thiessen method, each gauge is weighted by...",
                    (
                        opt("its elevation"),
                        opt("the area of the polygon closest to that gauge", correct=True),
                        opt("the number of tips of its bucket"),
                        opt("the distance to the basin outlet"),
                    ),
                    "Areal average = sum(P times area) divided by total area, where "
                    "each area is the Thiessen polygon nearest that gauge.",
                ),
                q(
                    "What does a change of slope in a double-mass curve indicate?",
                    (
                        opt("A leap year"),
                        opt(
                            "An inconsistency in the gauge record - the station was "
                            "likely moved or its exposure changed and needs correction",
                            correct=True,
                        ),
                        opt("That rainfall stopped forever"),
                        opt("That the basin doubled in area"),
                    ),
                    "The curve should be a straight line if the station is consistent "
                    "with its neighbors; a slope break flags a data problem.",
                ),
            ),
        ),
        # -- 3. Infiltration and evapotranspiration --------------------
        _t(
            "Infiltration and evapotranspiration",
            "10 min",
            """# Infiltration and evapotranspiration

Not all rain becomes runoff. Two **losses** intercept it first:
**infiltration** (water soaking into the soil) and **evapotranspiration**
(water returning to the atmosphere). Runoff is what is left over, so
estimating these losses is central to any runoff prediction.

**Infiltration** is highest when the soil is dry and decays toward a
steady rate as the soil saturates. The classic model is **Horton's
equation**, an exponential decay from an initial capacity to a final
capacity:

```text
Horton infiltration capacity:
  f(t) = fc + (f0 - fc) * e^(-k t)

  f0 = initial capacity (mm/hr, dry soil)
  fc = final steady capacity (mm/hr, saturated)
  k  = decay constant (1/hr)

Example: f0 = 30 mm/hr, fc = 6 mm/hr, k = 2 /hr, at t = 1 hr:
  f(1) = 6 + (30 - 6) * e^(-2*1)
       = 6 + 24 * 0.135
       = 6 + 3.25  =  9.25 mm/hr
So after one hour the soil accepts only about 9 mm/hr; rain above that
rate ponds and becomes runoff.
```

**Evapotranspiration (ET)** combines direct **evaporation** from soil and
water surfaces with **transpiration** from plants. **Potential ET (PET)**
is the demand if water were unlimited; **actual ET** is limited by how
much water is available. ET is estimated from climate data (temperature,
radiation, humidity, wind) using methods such as **Penman-Monteith**
(the standard) or the simpler temperature-based **Thornthwaite** and
**Blaney-Criddle**.

```mermaid
graph TD
    RAIN["Rainfall on the surface"] --> INTER["Interception by plants"]
    RAIN --> INFIL["Infiltration into soil"]
    RAIN --> PONDING["Rain above infiltration rate"]
    INFIL --> SOIL["Soil moisture storage"]
    SOIL --> ET["Evapotranspiration back to air"]
    SOIL --> RECHARGE["Deep percolation to aquifer"]
    PONDING --> RUNOFF["Surface runoff"]
```

Why it matters: a **crop water requirement** for irrigation is basically
actual ET minus effective rainfall. A **flood estimate** is total rain
minus infiltration and other losses. The same two loss processes drive
both water supply and flood design - just with opposite emphasis.

Remember: rainfall minus losses equals runoff. Infiltration governs the
fast, storm-scale loss; evapotranspiration governs the slow, seasonal
loss. Get the losses right and the runoff falls out.
""",
        ),
        quiz_lesson(
            "Quiz: Infiltration and evapotranspiration",
            (
                q(
                    "According to Horton's model, how does infiltration capacity change "
                    "during a storm?",
                    (
                        opt("It stays constant"),
                        opt(
                            "It starts high on dry soil and decays exponentially toward "
                            "a lower steady rate as the soil saturates",
                            correct=True,
                        ),
                        opt("It increases without limit"),
                        opt("It is always zero"),
                    ),
                    "f(t) = fc + (f0 - fc) e^(-kt): dry soil accepts water fast, then "
                    "the rate falls toward the saturated capacity fc.",
                ),
                q(
                    "What is the difference between potential ET and actual ET?",
                    (
                        opt("They are identical"),
                        opt(
                            "Potential ET is the atmospheric demand if water were "
                            "unlimited; actual ET is capped by the water actually "
                            "available",
                            correct=True,
                        ),
                        opt("Potential ET only happens at night"),
                        opt("Actual ET ignores plants"),
                    ),
                    "In a wet climate actual ET approaches PET; in a dry one, actual "
                    "ET falls short because there is not enough water to meet demand.",
                ),
                q(
                    "Why do infiltration and ET matter for flood design?",
                    (
                        opt("They do not - only rainfall matters"),
                        opt(
                            "Runoff equals rainfall minus losses; underestimating the "
                            "losses overestimates runoff, and vice versa",
                            correct=True,
                        ),
                        opt("They only matter for groundwater"),
                        opt("They replace the need to measure rainfall"),
                    ),
                    "The loss processes decide how much of the storm becomes the "
                    "runoff a culvert or channel must carry.",
                ),
            ),
        ),
        # -- 4. Watersheds and hydrographs -----------------------------
        _t(
            "Watersheds and hydrographs",
            "10 min",
            """# Watersheds and hydrographs

A **watershed** (catchment, drainage basin) is the area of land that
drains to a common outlet. Its boundary is the **drainage divide** - the
ridgeline separating flow that goes one way from flow that goes the
other. Everything in hydrologic design is defined *for a watershed at a
point*: the outlet where you want the flow.

A watershed's shape and character control how it responds to rain. Key
descriptors:

- **Area (A)** - the biggest single control on flow volume.
- **Time of concentration (tc)** - time for water to travel from the
  hydraulically most distant point to the outlet. Longer tc means a
  slower, flatter response.
- **Slope, land use, and drainage density** - steep, paved, well-drained
  basins respond fast and peaky; flat, vegetated, porous basins respond
  slow and muted.

The response is drawn as a **hydrograph**: discharge Q at the outlet
plotted against time. A storm produces a **rising limb**, a **peak**, and
a longer **falling (recession) limb** as storage drains:

```mermaid
graph LR
    RAIN["Storm rainfall"] --> BASIN["Watershed storage and travel"]
    BASIN --> RISE["Rising limb"]
    RISE --> PEAK["Peak discharge"]
    PEAK --> FALL["Falling recession limb"]
    FALL --> BASE["Baseflow from groundwater"]
```

A powerful idea is the **unit hydrograph**: the hydrograph produced by
**one unit of runoff** (say 1 cm) falling uniformly over the basin in a
set duration. Because the basin response is treated as **linear**, you
scale and add unit hydrographs to build the response to any storm.

**Worked example - runoff volume under a hydrograph.** A storm hydrograph
has a roughly triangular direct-runoff shape: peak 12 m3/s, total base
time 6 hours. Estimate the runoff volume and its depth over a 20 km2
basin.

```text
Triangle volume = 0.5 * base * height
  base = 6 hr = 6 * 3600 s = 21600 s
  Volume = 0.5 * 21600 s * 12 m3/s = 129600 m3

Runoff depth = Volume / Area
  Area = 20 km2 = 20e6 m2
  depth = 129600 / 20e6 = 0.00648 m = 6.5 mm

So this storm produced about 6.5 mm of direct runoff over the basin.
```

Remember: the watershed converts a rainfall input into a streamflow
output, and the hydrograph is that output over time. Area sets the
volume; time of concentration and basin character set the shape.
""",
        ),
        quiz_lesson(
            "Quiz: Watersheds and hydrographs",
            (
                q(
                    "What is a watershed?",
                    (
                        opt("A building that stores water"),
                        opt(
                            "The area of land that drains to a common outlet, bounded by "
                            "the drainage divide",
                            correct=True,
                        ),
                        opt("A single rain gauge"),
                        opt("The channel bed only"),
                    ),
                    "Hydrologic design is always for a watershed at a chosen outlet "
                    "point; the divide (ridgeline) sets its boundary.",
                ),
                q(
                    "What does a longer time of concentration imply about the hydrograph?",
                    (
                        opt("A faster, sharper peak"),
                        opt(
                            "A slower, flatter response - water takes longer to reach the outlet",
                            correct=True,
                        ),
                        opt("No runoff at all"),
                        opt("A doubling of rainfall"),
                    ),
                    "Steep, paved basins have short tc and peaky hydrographs; flat, "
                    "porous basins have long tc and muted ones.",
                ),
                q(
                    "What is a unit hydrograph?",
                    (
                        opt("The hydrograph of the largest flood on record"),
                        opt(
                            "The basin response to one unit of runoff over a set "
                            "duration, scaled and summed to model any storm",
                            correct=True,
                        ),
                        opt("A gauge reading in metric units"),
                        opt("The baseflow with no storm"),
                    ),
                    "It treats the basin as linear: scale by rainfall amount and add "
                    "shifted copies to build the response to a real storm. It is a "
                    "cornerstone of applied hydrology because it turns a complex basin "
                    "into a reusable, linear response function.",
                ),
            ),
        ),
        # -- 5. Rainfall-runoff modeling -------------------------------
        _t(
            "Rainfall-runoff modeling (rational method, SCS)",
            "11 min",
            """# Rainfall-runoff modeling (rational method, SCS)

To size a culvert or a storm sewer you need a **design discharge** from a
**design rainfall**. Two workhorse methods dominate practice: the
**rational method** (small, urban catchments) and the **SCS/NRCS curve
number method** (larger and rural catchments).

**The rational method** gives a peak flow directly:

```text
Rational method:  Q = C * i * A     (SI:  Q = C i A / 3.6)

  Q = peak discharge (m3/s)
  C = runoff coefficient (dimensionless, 0 to 1)
  i = rainfall intensity (mm/hr) for a duration = time of concentration
  A = catchment area (km2)
  3.6 = unit-conversion factor for these units

Example: a 0.4 km2 parking-lot catchment, C = 0.85 (mostly paved),
design intensity i = 90 mm/hr:
  Q = (0.85 * 90 * 0.4) / 3.6 = 8.5 m3/s
```

The key assumptions: rainfall is uniform, the storm lasts at least the
**time of concentration** (so the whole basin contributes at once), and C
is constant. That is why it is trusted only on **small** basins, commonly
under about 80 hectares.

**The SCS curve number method** estimates the **runoff depth** from total
rainfall using a single parameter, the **curve number (CN)**, which
encodes soil type and land use (CN near 100 is paved and impervious;
lower CN is porous and vegetated):

```text
SCS runoff:
  S = (25400 / CN) - 254       (potential retention, mm)
  Q = (P - 0.2 S)^2 / (P + 0.8 S)   for  P > 0.2 S,  else Q = 0

  0.2 S is the initial abstraction (interception plus early infiltration)

Example: P = 75 mm design rainfall, CN = 80:
  S = 25400/80 - 254 = 317.5 - 254 = 63.5 mm
  0.2 S = 12.7 mm, and P = 75 > 12.7, so runoff occurs
  Q = (75 - 12.7)^2 / (75 + 0.8*63.5)
    = (62.3)^2 / (75 + 50.8)
    = 3881 / 125.8  =  30.9 mm of runoff
```

```mermaid
graph TD
    START["Design storm rainfall"] --> SIZE{"Small urban catchment"}
    SIZE -->|"yes"| RAT["Rational method Q equals CiA"]
    SIZE -->|"no"| SCS["SCS curve number method"]
    RAT --> PEAK["Peak discharge"]
    SCS --> DEPTH["Runoff depth"]
    DEPTH --> HYDRO["Convert to hydrograph and peak"]
    PEAK --> DESIGN["Size the structure"]
    HYDRO --> DESIGN
```

Choosing between them: the rational method gives a **peak** fast for a
small paved area; the SCS method gives a **volume and hydrograph** and
scales to larger, mixed-land-use basins. Both turn a design rainfall into
the design flow that structures must carry.

Remember: pick the method to match the basin. Small and paved - rational.
Larger and mixed - curve number. Either way, the design rainfall in
drives the design discharge out.
""",
        ),
        quiz_lesson(
            "Quiz: Rainfall-runoff modeling (rational method, SCS)",
            (
                q(
                    "In the rational method Q = C i A, what is i?",
                    (
                        opt("The infiltration rate"),
                        opt(
                            "The design rainfall intensity, taken for a duration equal "
                            "to the time of concentration",
                            correct=True,
                        ),
                        opt("The basin slope"),
                        opt("The number of gauges"),
                    ),
                    "The storm must last at least tc so the whole basin contributes; i "
                    "is read from an IDF curve at that duration.",
                ),
                q(
                    "Why is the rational method restricted to small catchments?",
                    (
                        opt("Because the arithmetic is hard for big ones"),
                        opt(
                            "Its assumptions - uniform rainfall and a constant runoff "
                            "coefficient over the basin - only hold for small areas",
                            correct=True,
                        ),
                        opt("Large basins never flood"),
                        opt("It requires a curve number"),
                    ),
                    "Over a large, mixed basin rainfall and C vary too much; the SCS "
                    "method is used instead.",
                ),
                q(
                    "In the SCS method, what does a high curve number (CN near 100) represent?",
                    (
                        opt("A porous, forested basin with little runoff"),
                        opt(
                            "An impervious, paved surface that produces a large fraction "
                            "of the rainfall as runoff",
                            correct=True,
                        ),
                        opt("A basin with no rainfall"),
                        opt("A measurement error"),
                    ),
                    "CN encodes soil and land use; high CN means low retention S, so "
                    "more of the rain runs off.",
                ),
            ),
        ),
        # -- 6. Peak flow and IDF curves -------------------------------
        _t(
            "Peak flow and IDF curves",
            "10 min",
            """# Peak flow and IDF curves

Both design methods need a **design rainfall intensity**, and that comes
from an **Intensity-Duration-Frequency (IDF) curve**. An IDF curve
summarizes a location's rainfall statistics into one chart: for a chosen
**return period** (frequency) it gives the rainfall **intensity** as a
function of storm **duration**. Two facts drive its shape:

- **Shorter storms are more intense.** A 10-minute cloudburst delivers a
  higher mm/hr than a 6-hour soak, so intensity falls as duration rises.
- **Rarer storms are more intense.** The 100-year curve sits above the
  10-year curve for every duration.

A common analytic form fits the curves so software can read them:

```text
IDF equation (one common form):
  i = a / (t + b)^c

  i = intensity (mm/hr)
  t = duration (min)
  a, b, c = fitted constants for a site AND a return period

Example: for the 25-year event, a = 3200, b = 12, c = 0.78.
A catchment has time of concentration tc = 30 min, so use t = 30:
  i = 3200 / (30 + 12)^0.78
    = 3200 / (42)^0.78
    = 3200 / 19.6
    =  163 mm/hr

Feed this into the rational method for the 25-year peak flow.
```

The workflow ties the whole course together: pick a return period from
the risk you will accept, find the time of concentration of your basin,
read the intensity off the IDF curve at that duration, and compute the
peak flow.

```mermaid
graph LR
    RISK["Choose return period"] --> IDF["IDF curve for that frequency"]
    TC["Time of concentration"] --> IDF
    IDF --> INT["Design intensity i"]
    INT --> METHOD["Rational or SCS method"]
    METHOD --> QPEAK["Design peak discharge"]
    QPEAK --> STRUCT["Size culvert or channel"]
```

Why the duration equals tc: intensity is highest for short storms, but a
storm shorter than tc never wets the whole basin at once, so it cannot
produce the maximum peak. The storm that peaks the flow is the one whose
duration just equals the time of concentration - the standard rational
method assumption.

Remember: the IDF curve is the bridge from a location's rainfall record
to a design number. Return period sets which curve; time of concentration
sets where on it you read.
""",
        ),
        quiz_lesson(
            "Quiz: Peak flow and IDF curves",
            (
                q(
                    "What does an IDF curve relate?",
                    (
                        opt("Infiltration, drainage, and flow"),
                        opt(
                            "Rainfall intensity to storm duration for a given return "
                            "period (frequency)",
                            correct=True,
                        ),
                        opt("Irrigation demand to farm size"),
                        opt("Ice, dew, and frost"),
                    ),
                    "Intensity-Duration-Frequency: for a chosen frequency, intensity "
                    "versus duration.",
                ),
                q(
                    "How does rainfall intensity change as storm duration increases?",
                    (
                        opt("It increases"),
                        opt(
                            "It decreases - short bursts are more intense than long soaks",
                            correct=True,
                        ),
                        opt("It stays exactly constant"),
                        opt("It becomes negative"),
                    ),
                    "That is why the IDF curve slopes downward with duration; a "
                    "10-minute cloudburst has a higher mm/hr than a 6-hour rain.",
                ),
                q(
                    "In the rational method, why is the design storm duration set equal "
                    "to the time of concentration?",
                    (
                        opt("To make the arithmetic simpler"),
                        opt(
                            "A storm shorter than tc never has the whole basin "
                            "contributing at once, so tc gives the largest peak",
                            correct=True,
                        ),
                        opt("Because IDF curves only exist at tc"),
                        opt("To ignore the smallest basins"),
                    ),
                    "Shorter storms are more intense but do not engage the whole "
                    "basin; the peak comes from duration equal to tc. This trade-off - "
                    "higher intensity for short storms versus full basin contribution "
                    "at tc - is why tc is the critical duration.",
                ),
            ),
        ),
        # -- 7. Floods and extreme events ------------------------------
        _t(
            "Floods and extreme events (return period, frequency)",
            "11 min",
            """# Floods and extreme events (return period, frequency)

Design is about **rare** events, so hydrologists work in the language of
**probability**. The **return period (T)**, or recurrence interval, is
the average time between events of a given size. It is the inverse of the
annual **exceedance probability (p)**:

```text
Return period and probability:
  T = 1 / p            p = 1 / T

A "100-year flood" has p = 1/100 = 0.01: a 1 percent chance of being
equaled or exceeded IN ANY GIVEN YEAR. It is NOT "once every 100 years"
on a schedule - two can occur in consecutive years.

Risk over a design life of n years (probability of at least one exceedance):
  R = 1 - (1 - p)^n

Example: a culvert with a 50-year design life, sized for the T = 100-year
flood (p = 0.01):
  R = 1 - (1 - 0.01)^50 = 1 - (0.99)^50 = 1 - 0.605 = 0.395
So there is about a 40 percent chance the 100-year flood is exceeded at
least once during the culvert's life. Rarity is not safety.
```

To find the flood magnitude for a return period, we do **flood frequency
analysis**: fit a probability distribution to the annual maximum
discharges on record, then read off the value at the target probability.
Common distributions are **Gumbel (EV1)**, **Log-Pearson Type III** (the
US federal standard for floods), and the **GEV**.

```text
Gumbel (EV1) frequency factor method:
  x_T = xbar + K_T * s

  xbar = mean of annual peak flows
  s    = standard deviation of annual peak flows
  K_T  = frequency factor for return period T

Example: annual peaks have xbar = 120 m3/s, s = 35 m3/s.
For T = 100 yr, the Gumbel frequency factor is about K_T = 3.14:
  x_100 = 120 + 3.14 * 35 = 120 + 110 = 230 m3/s
That 230 m3/s is the 100-year design flood for this station.
```

```mermaid
graph TD
    RECORD["Annual peak flow record"] --> FIT["Fit a distribution"]
    FIT --> GUMBEL["Gumbel or Log Pearson III"]
    GUMBEL --> TARGET["Choose return period T"]
    TARGET --> QT["Design flood magnitude"]
    QT --> LIFE["Combine with design life"]
    LIFE --> RISK["Total risk over the life"]
```

A caution: frequency analysis assumes the record is **stationary** -
that the statistics do not change over time. Land-use change and climate
change violate that assumption, which is the bridge to the final lesson.

Remember: return period is an annual probability, not a calendar. Fit the
record, read the magnitude at your target T, and always convert to the
real question - the risk over the structure's whole life.
""",
        ),
        quiz_lesson(
            "Quiz: Floods and extreme events (return period, frequency)",
            (
                q(
                    "What does a '100-year flood' actually mean?",
                    (
                        opt("It happens exactly once every 100 years on a schedule"),
                        opt(
                            "It has a 1 percent chance (p = 1/100) of being equaled or "
                            "exceeded in any given year",
                            correct=True,
                        ),
                        opt("It is the largest flood physically possible"),
                        opt("It only happens in the 100th year"),
                    ),
                    "Return period is an average annual probability; two 100-year "
                    "floods can occur in back-to-back years.",
                ),
                q(
                    "A structure with a 30-year life is designed for the 100-year flood "
                    "(p = 0.01). Roughly what is the chance that flood is exceeded at "
                    "least once in its life?",
                    (
                        opt("About 1 percent"),
                        opt("Exactly 0 percent - it is safe"),
                        opt(
                            "About 26 percent - R = 1 - (0.99)^30",
                            correct=True,
                        ),
                        opt("Exactly 100 percent"),
                    ),
                    "R = 1 - (1 - 0.01)^30 = 1 - 0.74 = 0.26. Rarity per year still "
                    "adds up to real risk over a long life.",
                ),
                q(
                    "What key assumption does classical flood frequency analysis make?",
                    (
                        opt("That rainfall is always zero"),
                        opt(
                            "Stationarity - that the statistical properties of the flow "
                            "record do not change over time",
                            correct=True,
                        ),
                        opt("That the basin has no soil"),
                        opt("That every year has the same flood"),
                    ),
                    "Fitting a distribution to the record assumes the past represents "
                    "the future - an assumption climate change challenges.",
                ),
            ),
        ),
        # -- 8. Climate change and water resources ---------------------
        _t(
            "Climate change and water resources management",
            "11 min",
            """# Climate change and water resources management

Classical hydrology assumes **stationarity** - that the statistics of the
past predict the future. A warming climate breaks that assumption: warmer
air holds more moisture (about 7 percent more per degree C, the
**Clausius-Clapeyron** relation), which intensifies extreme rainfall,
shifts snowmelt earlier, and lengthens droughts. The famous phrase is
**"stationarity is dead"** - the historical record alone no longer sizes
infrastructure safely.

What changes for the water engineer:

- **More intense design storms.** IDF curves built on old records
  **underestimate** future extremes; agencies now publish climate-adjusted
  IDF curves and apply **change factors** to design intensities.
- **Shifted timing and supply.** Earlier snowmelt and longer dry spells
  stress reservoir operation, irrigation, and water supply reliability.
- **Deeper uncertainty.** Design now spans a **range** of climate
  scenarios rather than one stationary record.

The management response is **resilience and adaptation** across the whole
cycle:

- **Green infrastructure and low-impact development (LID)** - rain
  gardens, permeable pavement, bioswales, detention ponds. They restore
  infiltration, so a higher CN basin behaves more like a lower one.
- **Integrated water resources management (IWRM)** - manage supply,
  demand, flood, and ecology together at the basin scale, not structure
  by structure.
- **Digital tools** - real-time IoT gauges, remote sensing, and
  ML-based streamflow and flood forecasting turn static design into
  adaptive, data-driven operation; **digital twins** of a basin test
  scenarios before they happen.

```mermaid
graph TD
    WARM["Warming climate"] --> MOIST["More atmospheric moisture"]
    MOIST --> EXTREME["More intense storms"]
    WARM --> TIMING["Earlier snowmelt and droughts"]
    EXTREME --> NONSTAT["Stationarity no longer holds"]
    TIMING --> NONSTAT
    NONSTAT --> ADAPT["Adaptive design"]
    ADAPT --> GREEN["Green infrastructure and LID"]
    ADAPT --> IWRM["Integrated basin management"]
    ADAPT --> DIGITAL["Sensors and forecasting"]
```

**Worked example - a climate change factor on design intensity.** A
region projects a 15 percent increase in extreme rainfall intensity by
end of century. A culvert now sized for i = 90 mm/hr should be checked
against:

```text
Adjusted intensity:
  i_future = i * (1 + change factor)
           = 90 * (1 + 0.15)
           = 90 * 1.15  =  103.5 mm/hr

Using the rational method (Q proportional to i), the design peak flow
rises by the same 15 percent. A culvert sized only for today's 90 mm/hr
would be under-capacity for the projected storm - so engineers add
freeboard, upsize, or add green infrastructure to absorb the difference.
```

Remember: the historical record is necessary but no longer sufficient.
Design for a range of futures, restore natural infiltration and storage,
and manage the whole basin adaptively - resilience, not a single
stationary number, is the goal.
""",
        ),
        quiz_lesson(
            "Quiz: Climate change and water resources management",
            (
                q(
                    "What does 'stationarity is dead' mean for hydrologic design?",
                    (
                        opt("Rivers have stopped flowing"),
                        opt(
                            "The past statistical record no longer reliably predicts "
                            "future extremes, so design must account for change",
                            correct=True,
                        ),
                        opt("Rain gauges must stay in one place"),
                        opt("Floods no longer occur"),
                    ),
                    "A warming climate shifts the distribution of extremes; sizing "
                    "purely from historical records can underestimate future risk.",
                ),
                q(
                    "Why does a warmer atmosphere intensify extreme rainfall?",
                    (
                        opt("Warm air is heavier and falls faster"),
                        opt(
                            "Warmer air holds more moisture (about 7 percent per degree "
                            "C, Clausius-Clapeyron), fueling more intense storms",
                            correct=True,
                        ),
                        opt("It stops evaporation entirely"),
                        opt("It removes all clouds"),
                    ),
                    "More available moisture means heavier cloudbursts, which is why "
                    "old IDF curves can underestimate future intensities.",
                ),
                q(
                    "How does green infrastructure (LID) help a catchment adapt?",
                    (
                        opt("It paves over the soil to speed runoff"),
                        opt(
                            "It restores infiltration and storage - rain gardens, "
                            "permeable pavement, detention - so the basin behaves like "
                            "a lower curve number",
                            correct=True,
                        ),
                        opt("It removes all vegetation"),
                        opt("It only works in dry climates"),
                    ),
                    "By soaking up and slowing runoff, LID offsets the higher peaks "
                    "that intensified storms would otherwise produce.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In the water balance dS = P - Q - ET, what is Q?",
                    (
                        opt("The rainfall input"),
                        opt(
                            "The runoff or streamflow leaving the watershed",
                            correct=True,
                        ),
                        opt("The evapotranspiration"),
                        opt("The change in storage"),
                    ),
                    "P is input; Q, ET are outputs; dS is the change in stored water.",
                ),
                q(
                    "Which method weights each rain gauge by the area of its nearest "
                    "polygon to get a basin average?",
                    (
                        opt("Arithmetic mean"),
                        opt("Thiessen polygon method", correct=True),
                        opt("Horton's equation"),
                        opt("Gumbel analysis"),
                    ),
                    "Thiessen areal average = sum(P times polygon area) / total area.",
                ),
                q(
                    "Horton's infiltration equation describes capacity that...",
                    (
                        opt("stays constant through the storm"),
                        opt(
                            "starts high on dry soil and decays exponentially to a "
                            "steady saturated rate",
                            correct=True,
                        ),
                        opt("increases without bound"),
                        opt("is always equal to rainfall"),
                    ),
                    "f(t) = fc + (f0 - fc) e^(-kt); the soil accepts less as it wets up.",
                ),
                q(
                    "On a hydrograph, what is the recession (falling) limb?",
                    (
                        opt("The rise before the peak"),
                        opt(
                            "The declining discharge after the peak as basin storage drains",
                            correct=True,
                        ),
                        opt("The flat baseflow before the storm"),
                        opt("The rainfall hyetograph"),
                    ),
                    "Rising limb up to the peak, then the recession limb as the basin "
                    "empties toward baseflow.",
                ),
                q(
                    "In the rational method Q = C i A, what does the runoff coefficient "
                    "C represent?",
                    (
                        opt("The basin area in km2"),
                        opt(
                            "The fraction of rainfall that becomes runoff, from 0 to 1 "
                            "depending on land cover",
                            correct=True,
                        ),
                        opt("The rainfall intensity"),
                        opt("The time of concentration"),
                    ),
                    "Paved surfaces have C near 0.9; porous vegetated ones much lower.",
                ),
                q(
                    "In the SCS method, a higher curve number (CN) means...",
                    (
                        opt("more retention and less runoff"),
                        opt(
                            "less retention S and more runoff - toward impervious, "
                            "paved conditions",
                            correct=True,
                        ),
                        opt("no effect on runoff"),
                        opt("colder soil"),
                    ),
                    "S = 25400/CN - 254; high CN means small S, so more of the rain runs off.",
                ),
                q(
                    "In the rational method, what design storm duration gives the "
                    "largest peak flow?",
                    (
                        opt("The shortest possible storm"),
                        opt("A duration equal to the time of concentration", correct=True),
                        opt("A 24-hour storm always"),
                        opt("Duration does not matter"),
                    ),
                    "Shorter storms are more intense but do not engage the whole basin; "
                    "the peak occurs when duration equals tc.",
                ),
                q(
                    "A '50-year flood' has an annual exceedance probability of...",
                    (
                        opt("0.50"),
                        opt("0.02 - a 2 percent chance in any given year", correct=True),
                        opt("50 percent every year"),
                        opt("zero"),
                    ),
                    "p = 1/T = 1/50 = 0.02. Return period is the inverse of annual "
                    "exceedance probability.",
                ),
                q(
                    "Why is 'stationarity' a problem for flood frequency analysis under "
                    "climate change?",
                    (
                        opt("It makes the math impossible"),
                        opt(
                            "It assumes the statistics of the past predict the future, "
                            "which a warming climate violates",
                            correct=True,
                        ),
                        opt("It only applies to groundwater"),
                        opt("It requires more than one gauge"),
                    ),
                    "Warmer air intensifies extremes, so historical records can "
                    "underestimate future design floods.",
                ),
                q(
                    "A region expects a 20 percent increase in extreme rainfall "
                    "intensity. Using the rational method, how does the design peak flow "
                    "change (all else equal)?",
                    (
                        opt("It stays the same"),
                        opt(
                            "It rises by about 20 percent, since Q is proportional to intensity i",
                            correct=True,
                        ),
                        opt("It falls by 20 percent"),
                        opt("It doubles"),
                    ),
                    "In Q = C i A, Q scales directly with i; a 20 percent higher "
                    "intensity gives a 20 percent higher peak, so structures may need "
                    "upsizing. This is why agencies apply climate change factors to "
                    "design intensities and add freeboard or green infrastructure.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

HYDROLOGY_WATER_RESOURCES_COURSES: tuple[SeedCourse, ...] = (_HYDROLOGY_WATER_RESOURCES,)
