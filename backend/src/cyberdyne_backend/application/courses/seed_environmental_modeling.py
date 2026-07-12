"""Academy seed content - Environmental Modeling.

Predicting how environmental systems behave: mass balances and reactors,
surface-water quality (Streeter-Phelps, QUAL2K), groundwater (MODFLOW),
hydrologic and stormwater response (HEC-HMS, SWMM), and atmospheric
dispersion (AERMOD). It closes with the practice that turns any model
into a decision tool - calibration, validation, sensitivity and
uncertainty analysis, and scenario studies driven from Python. Every
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


_ENVIRONMENTAL_MODELING = SeedCourse(
    slug="environmental-modeling",
    title="Environmental Modeling",
    description=(
        "Predict environmental systems with the standard toolbox: mass "
        "balances and reactors, surface-water quality (Streeter-Phelps, "
        "QUAL2K), groundwater (MODFLOW), hydrologic and stormwater models "
        "(HEC-HMS, SWMM) and atmospheric dispersion (AERMOD) - then calibrate, "
        "validate and quantify uncertainty, with worked equations, Python "
        "snippets and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Modeling

An **environmental model** is a simplified mathematical description of a
real system - a river, an aquifer, a watershed, an air basin - that lets
you predict how it will respond to a change before that change happens.
Will a discharge push dissolved oxygen below the limit? How far will a
plume travel? What flood peak follows a design storm? Models turn those
questions into numbers you can defend.

This is an **Advanced** course. It assumes you are comfortable with mass
balances, basic differential equations, and reading a little Python. The
approach is **concrete**: each lesson explains one modeling idea directly,
works a real equation or calculation (a reactor balance, a Streeter-Phelps
sag, a Darcy flux, a Gaussian plume), and draws the idea as a diagram.
After each lesson there is a short quiz; a final quiz covers the whole
course.

What you will build understanding for, in order:

1. **Mass balances and reactors** - the conservation law behind every model
2. **Surface water quality** - Streeter-Phelps and QUAL2K
3. **Groundwater** - Darcy's law and MODFLOW
4. **Hydrology and stormwater** - HEC-HMS and SWMM
5. **Atmospheric dispersion** - the Gaussian plume and AERMOD
6. **Calibration and validation** - making a model match reality, then proving it
7. **Sensitivity and uncertainty analysis** - which inputs matter, and how sure are you
8. **Scenario analysis with Python** - turning a calibrated model into decisions

A model is only useful if it is calibrated, validated, and honest about its
uncertainty - so the second half of the course is as important as the first.
Standards and regulators (EPA, WHO, CONAMA, ABNT NBR) expect exactly that
discipline.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is an environmental model, fundamentally?",
                    (
                        opt("A physical scale replica of a river or aquifer"),
                        opt(
                            "A simplified mathematical description of a real system that "
                            "predicts how it responds to change",
                            correct=True,
                        ),
                        opt("A monitoring station that records field data"),
                        opt("A single regulatory limit value"),
                    ),
                    "A model abstracts a system into equations so you can predict "
                    "behavior before making a change.",
                ),
                q(
                    "Why does this course spend its second half on calibration, "
                    "validation and uncertainty?",
                    (
                        opt("Those topics are optional extras rarely used in practice"),
                        opt(
                            "A model is only a defensible decision tool once it is "
                            "calibrated, validated and honest about uncertainty",
                            correct=True,
                        ),
                        opt("Regulators never look at model performance"),
                        opt("They replace the need for a mass balance"),
                    ),
                    "An uncalibrated, unvalidated model with no uncertainty statement is "
                    "not trustworthy - regulators and good practice both require it.",
                ),
            ),
        ),
        # -- 1. Mass balances and reactors -----------------------------
        _t(
            "Mass balances and environmental reactors",
            "11 min",
            """# Mass balances and environmental reactors

Almost every environmental model is a **mass balance** on a defined
**control volume**: what accumulates inside equals what comes in, minus
what goes out, plus or minus what is generated or consumed by reaction.

```text
Accumulation = Inflow - Outflow +/- Reaction

  V dC/dt = Q*C_in - Q*C - k*C*V

  V     = control volume
  Q     = volumetric flow rate
  C_in  = inflow concentration
  C     = concentration in the volume
  k     = first-order reaction rate constant
```

Two idealized **reactor models** bracket real behavior:

- **CSTR (completely mixed)** - the contents are uniform, so the outflow
  concentration equals the concentration everywhere inside. A lake or a
  well-mixed basin.
- **PFR (plug flow)** - fluid moves like a plug with no mixing along the
  flow direction; concentration changes with distance. A long narrow river
  reach or pipe.

At **steady state** the accumulation term is zero. For a CSTR with
first-order decay, setting `dC/dt = 0`:

```text
0 = Q*C_in - Q*C - k*C*V
=>  C = C_in / (1 + k*tau),   tau = V/Q  (hydraulic residence time)

Example: C_in = 10 mg/L, k = 0.5 /h, tau = 4 h
  C = 10 / (1 + 0.5*4) = 10 / 3 = 3.33 mg/L
```

The same species in a **PFR** decays exponentially with residence time,
`C = C_in * exp(-k*tau)`, which for the same numbers gives
`10 * exp(-2) = 1.35 mg/L` - lower, because a plug is never diluted by
already-treated fluid. Choosing the right reactor idealization is the
first modeling decision you make.

```mermaid
graph LR
    IN["Inflow Q Cin"] --> CV["Control volume V"]
    CV --> RXN["Reaction k C V"]
    CV --> OUT["Outflow Q C"]
    ACC["Accumulation V dC dt"] --> CV
    CV --> SS["Steady state dC dt is zero"]
```

Remember: define the control volume, write in minus out plus or minus
reaction, then decide whether the system is better idealized as mixed or
plug flow.
""",
        ),
        quiz_lesson(
            "Quiz: Mass balances and environmental reactors",
            (
                q(
                    "What is the general form of a mass balance on a control volume?",
                    (
                        opt("Inflow equals outflow, always"),
                        opt(
                            "Accumulation equals inflow minus outflow plus or minus reaction",
                            correct=True,
                        ),
                        opt("Concentration equals flow times volume"),
                        opt("Reaction equals accumulation times residence time"),
                    ),
                    "Conservation of mass: what builds up is what enters, minus what "
                    "leaves, adjusted for what reacts.",
                ),
                q(
                    "How does a CSTR differ from a PFR?",
                    (
                        opt("A CSTR has no reaction; a PFR always does"),
                        opt(
                            "A CSTR is completely mixed so outflow equals interior "
                            "concentration; a PFR moves as a plug with concentration "
                            "changing along the flow path",
                            correct=True,
                        ),
                        opt("A PFR is always at steady state; a CSTR never is"),
                        opt("They give identical results for first-order decay"),
                    ),
                    "Mixed tank versus plug flow - for the same k and residence time the "
                    "PFR removes more of a decaying species.",
                ),
                q(
                    "For a steady-state CSTR with first-order decay, C_in = 20 mg/L, "
                    "k = 1 /h and tau = 1 h, what is the outflow concentration?",
                    (
                        opt("20 mg/L"),
                        opt("10 mg/L", correct=True),
                        opt("7.4 mg/L"),
                        opt("0 mg/L"),
                    ),
                    "C = C_in / (1 + k*tau) = 20 / (1 + 1*1) = 10 mg/L.",
                ),
            ),
        ),
        # -- 2. Surface water quality ----------------------------------
        _t(
            "Surface water quality modeling (Streeter-Phelps, QUAL2K)",
            "12 min",
            """# Surface water quality modeling (Streeter-Phelps, QUAL2K)

When organic waste enters a river, microbes consume it and draw down
**dissolved oxygen (DO)**. The classic model of this is **Streeter-Phelps
(1925)**: a plug-flow river with two competing processes - **deoxygenation**
from biochemical oxygen demand (**BOD**) and **rearomation** from the
atmosphere. Track the **oxygen deficit** D (saturation minus actual DO):

```text
dD/dt = kd*L - ka*D

  L  = BOD remaining (mg/L)      L = L0 * exp(-kd*t)
  kd = deoxygenation rate (/d)
  ka = reaeration rate (/d)
  D  = DO deficit = DO_sat - DO

Solution (the "oxygen sag" curve):
  D(t) = (kd*L0)/(ka - kd) * (exp(-kd*t) - exp(-ka*t)) + D0*exp(-ka*t)

Critical time (deepest sag, dD/dt = 0):
  t_c = 1/(ka - kd) * ln[ (ka/kd) * (1 - D0*(ka - kd)/(kd*L0)) ]
```

Travel time `t` is distance divided by stream velocity, so the deficit is
really a function of distance downstream. The **critical point** is where
DO is lowest - the design concern, because that is where DO may fall below
the standard (commonly around 5 mg/L to protect aquatic life; CONAMA 357
sets class limits in Brazil).

Streeter-Phelps is deliberately minimal. Modern practice uses **QUAL2K**
(the EPA river and stream water-quality model), which extends the same
mass-balance idea to many interacting constituents - BOD, DO, nitrogen and
phosphorus species, algae, pH, temperature - across a network of reaches
with sediment interactions. The physics is richer, but the backbone is
still deoxygenation, reaeration, and transport.

```mermaid
graph LR
    LOAD["Waste load BOD"] --> DEOX["Deoxygenation kd L"]
    DEOX --> DEF["Oxygen deficit D"]
    ATM["Atmosphere"] --> REAER["Reaeration ka D"]
    REAER --> DEF
    DEF --> SAG["Oxygen sag curve"]
    SAG --> CRIT["Critical point lowest DO"]
```

Remember: DO drops where deoxygenation outruns reaeration; the sag curve's
critical point is where you check the standard, and QUAL2K generalizes the
same balance to a full multi-constituent river network.
""",
        ),
        quiz_lesson(
            "Quiz: Surface water quality modeling (Streeter-Phelps, QUAL2K)",
            (
                q(
                    "In the Streeter-Phelps model, which two competing processes shape "
                    "the dissolved-oxygen profile?",
                    (
                        opt("Evaporation and precipitation"),
                        opt(
                            "Deoxygenation from BOD and reaeration from the atmosphere",
                            correct=True,
                        ),
                        opt("Sedimentation and resuspension only"),
                        opt("Photosynthesis and gravity"),
                    ),
                    "BOD decay removes oxygen (deoxygenation); the atmosphere resupplies "
                    "it (reaeration). Their balance is the oxygen sag.",
                ),
                q(
                    "What is the 'critical point' of the oxygen sag curve?",
                    (
                        opt("Where the river is deepest"),
                        opt("Where BOD is highest"),
                        opt(
                            "The location and time of minimum dissolved oxygen, where the "
                            "DO standard is most at risk",
                            correct=True,
                        ),
                        opt("Where reaeration equals zero"),
                    ),
                    "At t_c the deficit is largest (dD/dt = 0); that lowest-DO point is "
                    "the design concern.",
                ),
                q(
                    "How does QUAL2K extend Streeter-Phelps?",
                    (
                        opt("It ignores dissolved oxygen entirely"),
                        opt(
                            "It applies the same mass-balance approach to many "
                            "interacting constituents (nutrients, algae, pH, temperature) "
                            "across a network of reaches",
                            correct=True,
                        ),
                        opt("It only works for groundwater"),
                        opt("It removes the need for BOD data"),
                    ),
                    "Same backbone (transport plus reactions), but multi-constituent and "
                    "multi-reach - a fuller river water-quality model.",
                ),
            ),
        ),
        # -- 3. Groundwater --------------------------------------------
        _t(
            "Groundwater modeling (MODFLOW)",
            "12 min",
            """# Groundwater modeling (MODFLOW)

Groundwater flow is governed by **Darcy's law**: flow through porous media
is proportional to the **hydraulic conductivity** and the **hydraulic
gradient**. Combine Darcy's law with a mass balance on a control volume and
you get the **groundwater flow equation** that every aquifer model solves.

```text
Darcy's law:   q = -K * dh/dx        (specific discharge, or Darcy flux)
  K    = hydraulic conductivity (m/d)
  dh/dx= hydraulic gradient (head drop per distance)
Actual seepage velocity:  v = q / n_e   (n_e = effective porosity)

Governing flow equation (transient, confined):
  d/dx(Kx dh/dx) + d/dy(Ky dh/dy) + d/dz(Kz dh/dz) + W = Ss dh/dt
  W  = source/sink (recharge, wells)
  Ss = specific storage
```

Analytical solutions exist only for simple geometry, so real aquifers are
solved **numerically**. The industry standard is **MODFLOW** (US
Geological Survey), a **finite-difference** code: the aquifer is divided
into a grid of cells; MODFLOW writes the flow equation for each cell and
solves the linked system for the **head** in every cell. Wells, rivers,
recharge, and boundaries are added as **packages**.

A quick Darcy calculation shows the scale of movement:

```python
K = 10.0       # hydraulic conductivity, m/d
dh = 2.0       # head drop, m
L = 500.0      # flow path length, m
n_e = 0.25     # effective porosity

q = K * (dh / L)          # Darcy flux = 0.04 m/d
v = q / n_e               # seepage velocity = 0.16 m/d
travel_time = L / v       # ~3125 days ~= 8.6 years
print(round(q, 3), round(v, 3), round(travel_time))
```

Groundwater moves slowly - which is exactly why contamination is so
persistent and why predictive models matter for wellhead protection and
plume capture. Contaminant transport (advection plus dispersion plus
reaction) is then solved on the same grid by companions like **MT3D**.

```mermaid
graph TD
    HEAD["Hydraulic head field"] --> DARCY["Darcy flux q equals minus K grad h"]
    DARCY --> GRID["Finite difference grid of cells"]
    GRID --> SOLVE["Solve head in every cell"]
    RECH["Recharge and wells"] --> GRID
    BND["Boundary conditions"] --> GRID
    SOLVE --> TRANS["Transport of contaminants"]
```

Remember: Darcy's law plus a cell-by-cell mass balance is what MODFLOW
solves; heads give you fluxes, fluxes give you velocities, and velocities
tell you how fast a plume travels.
""",
        ),
        quiz_lesson(
            "Quiz: Groundwater modeling (MODFLOW)",
            (
                q(
                    "What does Darcy's law relate?",
                    (
                        opt("Rainfall to runoff"),
                        opt(
                            "Groundwater flux to hydraulic conductivity and the hydraulic gradient",
                            correct=True,
                        ),
                        opt("Oxygen deficit to BOD"),
                        opt("Wind speed to plume rise"),
                    ),
                    "q = -K dh/dx: flow through porous media is proportional to "
                    "conductivity times the head gradient.",
                ),
                q(
                    "What numerical method does MODFLOW use to solve the groundwater "
                    "flow equation?",
                    (
                        opt("Gaussian plume superposition"),
                        opt("The unit hydrograph"),
                        opt(
                            "Finite differences on a grid of cells, solving for head in each cell",
                            correct=True,
                        ),
                        opt("Streeter-Phelps integration"),
                    ),
                    "MODFLOW discretizes the aquifer into cells and solves the coupled "
                    "head equations - a finite-difference solver.",
                ),
                q(
                    "Why does the seepage velocity exceed the Darcy flux?",
                    (
                        opt("Because conductivity increases with depth"),
                        opt(
                            "The Darcy flux is divided by effective porosity, since water "
                            "actually moves only through the pore space",
                            correct=True,
                        ),
                        opt("Because dispersion adds velocity"),
                        opt("They are always equal"),
                    ),
                    "v = q / n_e: only the pores carry flow, so the actual water velocity "
                    "is faster than the bulk Darcy flux.",
                ),
            ),
        ),
        # -- 4. Hydrologic and stormwater ------------------------------
        _t(
            "Hydrologic and stormwater modeling (HEC-HMS, SWMM)",
            "12 min",
            """# Hydrologic and stormwater modeling (HEC-HMS, SWMM)

**Hydrologic models** convert rainfall into runoff and route it through a
watershed to predict streamflow - the basis for flood forecasting and
drainage design. The core problem is **rainfall-runoff transformation**:
not all rain becomes runoff; some infiltrates, some is intercepted or
evaporates. The remainder is **effective precipitation**.

A widely used method is the **SCS Curve Number**, which lumps land use and
soil type into a single **curve number (CN)**:

```text
SCS-CN runoff:
  S = (25400 / CN) - 254        (mm, potential retention)
  Q = (P - 0.2*S)^2 / (P + 0.8*S)   for P > 0.2*S, else Q = 0

  P  = rainfall depth (mm)
  Q  = runoff depth (mm)
  CN = 30 (permeable) to 98 (paved), from soil group and land cover

Example: P = 75 mm, CN = 85
  S = 25400/85 - 254 = 44.8 mm
  Q = (75 - 0.2*44.8)^2 / (75 + 0.8*44.8) = (66.0)^2 / 110.8 = 39.3 mm
```

**HEC-HMS** (US Army Corps of Engineers) assembles these pieces - loss
method, a **unit hydrograph** to shape the runoff into a flow-versus-time
curve, and channel **routing** - into a basin model that produces the
**design flood hydrograph**. It is the standard for watershed hydrology and
flood studies.

For the **urban** side, **SWMM** (EPA Storm Water Management Model) simulates
runoff over subcatchments and then routes it through a network of pipes,
channels, storage and pumps - solving the hydraulics of the drainage system,
including surcharge and flooding. SWMM also models green infrastructure
(bioretention, permeable pavement) as Low Impact Development controls.

```mermaid
graph LR
    RAIN["Rainfall hyetograph"] --> LOSS["Losses infiltration"]
    LOSS --> EFF["Effective rainfall"]
    EFF --> UH["Unit hydrograph transform"]
    UH --> HYD["Runoff hydrograph"]
    HYD --> ROUTE["Route through channels or pipes"]
    ROUTE --> PEAK["Design peak flow"]
```

Remember: hydrology is rainfall minus losses, transformed to a hydrograph
and routed to a peak. HEC-HMS does the watershed and flood side; SWMM does
the urban drainage network and green infrastructure.
""",
        ),
        quiz_lesson(
            "Quiz: Hydrologic and stormwater modeling (HEC-HMS, SWMM)",
            (
                q(
                    "What is 'effective precipitation' in a rainfall-runoff model?",
                    (
                        opt("The total rainfall depth measured at a gauge"),
                        opt(
                            "The portion of rainfall that becomes runoff after "
                            "infiltration and other losses are removed",
                            correct=True,
                        ),
                        opt("Rain that evaporates before reaching the ground"),
                        opt("The peak flow rate in the channel"),
                    ),
                    "Only the rain left after losses (infiltration, interception) runs "
                    "off - that effective rainfall drives the hydrograph.",
                ),
                q(
                    "What does the SCS Curve Number represent?",
                    (
                        opt("The number of storms per year"),
                        opt(
                            "A lumped index of land use and soil type that sets how much "
                            "rainfall becomes runoff",
                            correct=True,
                        ),
                        opt("The channel Manning roughness"),
                        opt("The reaeration rate of a stream"),
                    ),
                    "Higher CN (paved, poor soils) means more runoff; lower CN (permeable) "
                    "means more infiltration.",
                ),
                q(
                    "How do HEC-HMS and SWMM differ in typical use?",
                    (
                        opt("HEC-HMS models air quality; SWMM models groundwater"),
                        opt(
                            "HEC-HMS focuses on watershed hydrology and flood hydrographs; "
                            "SWMM focuses on urban drainage networks and stormwater "
                            "hydraulics",
                            correct=True,
                        ),
                        opt("They are identical tools with different names"),
                        opt("SWMM cannot handle rainfall input"),
                    ),
                    "Watershed and flood studies use HEC-HMS; urban pipe/channel drainage "
                    "and green infrastructure use SWMM.",
                ),
            ),
        ),
        # -- 5. Atmospheric dispersion ---------------------------------
        _t(
            "Atmospheric dispersion modeling (AERMOD)",
            "12 min",
            """# Atmospheric dispersion modeling (AERMOD)

To predict pollutant concentrations downwind of a stack, you model how the
**plume** is carried by the wind (**advection**) and spread by turbulence
(**dispersion**). The foundational model is the **Gaussian plume**: the
plume cross-section is bell-shaped in the horizontal and vertical, spreading
as it travels.

```text
Gaussian plume (ground-level, continuous point source):
  C(x,y,z) = Q / (2*pi*u*sy*sz)
             * exp(-y^2 / (2*sy^2))
             * [ exp(-(z-H)^2/(2*sz^2)) + exp(-(z+H)^2/(2*sz^2)) ]

  Q  = emission rate (g/s)
  u  = wind speed at stack height (m/s)
  H  = effective stack height = physical height + plume rise
  sy, sz = horizontal and vertical dispersion coefficients (grow with x)

Max ground-level concentration under the plume centerline (y=0, z=0):
  C = Q / (pi*u*sy*sz) * exp(-H^2 / (2*sz^2))
```

The dispersion coefficients `sy` and `sz` grow with downwind distance and
depend on **atmospheric stability** - unstable (sunny, turbulent) air
disperses a plume quickly; stable (calm, night) air keeps it tight and can
produce high ground concentrations far downwind. Older models used the
**Pasquill-Gifford stability classes** (A to F) to pick these coefficients.

**AERMOD** is the EPA's current regulatory air-dispersion model. It keeps
the steady-state Gaussian form but replaces the crude stability classes with
modern **boundary-layer physics** - it characterizes turbulence from actual
meteorology and handles terrain, building downwash, and deposition. AERMOD
is what permit applications in the US use to show a source will meet the
National Ambient Air Quality Standards.

```mermaid
graph LR
    STACK["Stack emission Q"] --> RISE["Plume rise effective height H"]
    RISE --> WIND["Advection by wind u"]
    WIND --> DISP["Dispersion sy and sz"]
    STAB["Atmospheric stability"] --> DISP
    DISP --> CONC["Ground level concentration"]
    CONC --> STD["Compare to air quality standard"]
```

Remember: a plume is advected by the wind and spread by turbulence; the
Gaussian equation captures that, stability sets how fast it spreads, and
AERMOD grounds the same form in real boundary-layer meteorology.
""",
        ),
        quiz_lesson(
            "Quiz: Atmospheric dispersion modeling (AERMOD)",
            (
                q(
                    "In the Gaussian plume model, what do the coefficients sy and sz represent?",
                    (
                        opt("The emission rate and stack height"),
                        opt(
                            "The horizontal and vertical spread of the plume, which grow "
                            "with downwind distance",
                            correct=True,
                        ),
                        opt("The wind speed and direction"),
                        opt("The deposition and washout rates"),
                    ),
                    "sy and sz are the dispersion (spread) coefficients; a wider plume "
                    "means lower peak concentration.",
                ),
                q(
                    "How does atmospheric stability affect a plume?",
                    (
                        opt("Stability has no effect on dispersion"),
                        opt(
                            "Unstable, turbulent air disperses a plume quickly; stable, "
                            "calm air keeps it tight and can give high concentrations far "
                            "downwind",
                            correct=True,
                        ),
                        opt("Stable air always disperses plumes fastest"),
                        opt("Stability only changes wind direction"),
                    ),
                    "Turbulence drives dispersion - unstable air spreads a plume, stable "
                    "air confines it.",
                ),
                q(
                    "What distinguishes AERMOD from the older Gaussian-class approach?",
                    (
                        opt("It abandons the Gaussian form entirely"),
                        opt(
                            "It replaces crude Pasquill-Gifford stability classes with "
                            "modern boundary-layer physics and handles terrain and "
                            "building downwash",
                            correct=True,
                        ),
                        opt("It only works for groundwater plumes"),
                        opt("It ignores meteorology"),
                    ),
                    "AERMOD keeps a steady-state Gaussian core but parameterizes "
                    "turbulence from real boundary-layer meteorology - the EPA regulatory "
                    "standard.",
                ),
            ),
        ),
        # -- 6. Calibration and validation -----------------------------
        _t(
            "Calibration and validation",
            "11 min",
            """# Calibration and validation

A model has **parameters** you cannot measure directly - a reaeration rate,
a hydraulic conductivity field, a curve number. **Calibration** is the
process of adjusting those parameters so the model **reproduces observed
data**. **Validation** is the separate step of testing the calibrated model
against **different** data it never saw, to show it generalizes rather than
merely memorizes.

Never calibrate and validate on the same data. **Split** the record: use
one period (or set of gauges) to calibrate, hold back another to validate.
This is the environmental-modeling version of train/test separation.

Calibration is an **optimization**: minimize an objective function that
measures the gap between modeled and observed values. Common goodness-of-fit
metrics:

```text
RMSE  = sqrt( mean( (obs - sim)^2 ) )         lower is better

Nash-Sutcliffe efficiency (NSE), standard in hydrology:
  NSE = 1 - sum((obs - sim)^2) / sum((obs - mean_obs)^2)
        NSE = 1 : perfect
        NSE = 0 : no better than predicting the mean
        NSE < 0 : worse than the mean

PBIAS = 100 * sum(obs - sim) / sum(obs)       percent bias, near 0 is best
```

You can tune by hand (change a parameter, re-run, compare) or use
**automated calibration** (PEST is the standard tool for MODFLOW and many
others), which runs the model hundreds of times and adjusts parameters to
minimize the objective. Guard against **overfitting** - a model that matches
one dataset perfectly but has physically absurd parameters will fail on new
conditions. Keep parameters within plausible physical ranges.

```mermaid
graph TD
    DATA["Observed data"] --> SPLIT["Split record"]
    SPLIT --> CAL["Calibration set"]
    SPLIT --> VAL["Validation set"]
    CAL --> TUNE["Adjust parameters minimize error"]
    TUNE --> MODEL["Calibrated model"]
    VAL --> CHECK["Validate on unseen data"]
    MODEL --> CHECK
    CHECK --> GOOD["Report NSE RMSE PBIAS"]
```

Remember: calibrate to fit, validate on held-out data to prove it
generalizes, and judge fit with metrics like NSE, RMSE and PBIAS - not by
eye alone.
""",
        ),
        quiz_lesson(
            "Quiz: Calibration and validation",
            (
                q(
                    "What is the difference between calibration and validation?",
                    (
                        opt("They are two names for the same step"),
                        opt(
                            "Calibration adjusts parameters to fit observed data; "
                            "validation tests the calibrated model against different data "
                            "it never saw",
                            correct=True,
                        ),
                        opt("Validation adjusts parameters; calibration only reports results"),
                        opt("Calibration uses the future; validation uses the past"),
                    ),
                    "Fit on the calibration set, then prove generalization on held-out "
                    "validation data - like train/test.",
                ),
                q(
                    "What does a Nash-Sutcliffe efficiency (NSE) of 0 mean?",
                    (
                        opt("The model is perfect"),
                        opt(
                            "The model is no better than simply predicting the mean of "
                            "the observations",
                            correct=True,
                        ),
                        opt("The model has zero bias"),
                        opt("The observations are all zero"),
                    ),
                    "NSE = 1 is perfect, NSE = 0 matches the mean, NSE < 0 is worse than the mean.",
                ),
                q(
                    "Why must you avoid overfitting during calibration?",
                    (
                        opt("Overfitting makes the model run too slowly"),
                        opt(
                            "A model tuned to match one dataset with physically absurd "
                            "parameters will fail under new conditions",
                            correct=True,
                        ),
                        opt("Overfitting only matters for air-quality models"),
                        opt("It has no effect on predictions"),
                    ),
                    "Keep parameters physically plausible; a perfect fit with nonsense "
                    "parameters does not generalize.",
                ),
            ),
        ),
        # -- 7. Sensitivity and uncertainty ----------------------------
        _t(
            "Sensitivity and uncertainty analysis",
            "12 min",
            """# Sensitivity and uncertainty analysis

Every model input carries uncertainty, and a prediction is only as
trustworthy as your understanding of how that uncertainty propagates.
Two related questions:

- **Sensitivity analysis** - *which* inputs matter? How much does the output
  change when an input changes? It tells you where to spend measurement
  effort and which parameters dominate the result.
- **Uncertainty analysis** - *how uncertain* is the output, given the
  uncertainty in the inputs? It produces a range or distribution around the
  prediction, not a single deceptively precise number.

A simple **local** sensitivity is a one-at-a-time finite difference - nudge
one parameter, hold the rest fixed, measure the response:

```text
Sensitivity of output y to parameter p:
  S = (dy/y) / (dp/p)      dimensionless relative sensitivity

  S near 0  : output barely responds to p (low priority)
  |S| large : output is dominated by p (measure it well)
```

Local methods miss interactions and nonlinearity, so **global** methods
sample the whole input space. The workhorse is **Monte Carlo**: draw each
uncertain input from its probability distribution, run the model, and repeat
thousands of times to build the output distribution.

```python
import numpy as np

rng = np.random.default_rng(42)
n = 10000
# uncertain inputs sampled from distributions
kd = rng.normal(0.30, 0.05, n)   # deoxygenation rate, /d
L0 = rng.normal(20.0, 3.0, n)    # initial BOD, mg/L
t = 2.0                          # travel time, days

L = L0 * np.exp(-kd * t)         # BOD remaining, run per sample
print("mean:", round(L.mean(), 2),
      "  95% interval:", np.round(np.percentile(L, [2.5, 97.5]), 2))
```

Variance-based methods like **Sobol indices** go further, attributing the
output variance to each input and their interactions. The deliverable is
always the same: a prediction reported **with** its uncertainty (a
confidence or credible interval), which is what a regulator or decision
maker actually needs.

```mermaid
graph TD
    INPUTS["Uncertain inputs with distributions"] --> SENS["Sensitivity which inputs matter"]
    INPUTS --> MC["Monte Carlo sampling"]
    MC --> RUNS["Thousands of model runs"]
    RUNS --> DIST["Output distribution"]
    DIST --> INTERVAL["Confidence interval"]
    SENS --> PRIORITY["Prioritize data collection"]
```

Remember: sensitivity ranks the inputs, uncertainty quantifies the output
spread, and Monte Carlo is the general engine - never report a single number
as if it had no uncertainty.
""",
        ),
        quiz_lesson(
            "Quiz: Sensitivity and uncertainty analysis",
            (
                q(
                    "What question does sensitivity analysis answer?",
                    (
                        opt("How uncertain is the final prediction?"),
                        opt(
                            "Which inputs most influence the output, and by how much",
                            correct=True,
                        ),
                        opt("What the true value of every parameter is"),
                        opt("Whether the model compiles"),
                    ),
                    "Sensitivity ranks inputs by influence; uncertainty analysis is the "
                    "separate question of output spread.",
                ),
                q(
                    "What is the Monte Carlo approach to uncertainty analysis?",
                    (
                        opt("Run the model once with best-guess inputs"),
                        opt(
                            "Draw each uncertain input from its distribution and run the "
                            "model many times to build the output distribution",
                            correct=True,
                        ),
                        opt("Adjust parameters until the fit is perfect"),
                        opt("Solve the governing equation analytically"),
                    ),
                    "Sample inputs, run repeatedly, and the spread of outputs gives the "
                    "prediction uncertainty.",
                ),
                q(
                    "Why report a prediction with a confidence interval rather than a "
                    "single number?",
                    (
                        opt("To make the report longer"),
                        opt(
                            "A single number hides the uncertainty; decision makers and "
                            "regulators need the plausible range",
                            correct=True,
                        ),
                        opt("Intervals are required by the mermaid syntax"),
                        opt("Because Monte Carlo cannot produce a mean"),
                    ),
                    "An interval communicates how sure you are - a single deceptively "
                    "precise value does not.",
                ),
            ),
        ),
        # -- 8. Scenario analysis with Python --------------------------
        _t(
            "Scenario analysis with Python",
            "12 min",
            """# Scenario analysis with Python

A calibrated, validated model with a handle on its uncertainty becomes a
**decision tool** through **scenario analysis**: run the model under
different assumptions - a new discharge, a climate projection, an added
treatment step, a land-use change - and compare the outcomes side by side.
Python is the glue that makes this fast and reproducible.

The pattern is to wrap the model in a function, define scenarios as data,
run them in a loop, and tabulate the results:

```python
import numpy as np
import pandas as pd

def critical_deficit(L0, kd, ka, D0=0.0):
    # Streeter-Phelps critical (max) oxygen deficit, mg/L
    tc = 1/(ka - kd) * np.log((ka/kd) * (1 - D0*(ka - kd)/(kd*L0)))
    return (kd * L0 / ka) * np.exp(-kd * tc)

scenarios = pd.DataFrame([
    {"name": "baseline",       "L0": 20.0, "kd": 0.30, "ka": 0.55},
    {"name": "upgraded plant",  "L0": 12.0, "kd": 0.30, "ka": 0.55},
    {"name": "low flow summer", "L0": 20.0, "kd": 0.35, "ka": 0.40},
])

scenarios["Dmax_mgL"] = scenarios.apply(
    lambda r: round(critical_deficit(r.L0, r.kd, r.ka), 2), axis=1)
scenarios["DO_min_mgL"] = (9.0 - scenarios["Dmax_mgL"]).round(2)  # DO_sat ~ 9
print(scenarios[["name", "Dmax_mgL", "DO_min_mgL"]])
```

This immediately shows which scenario risks breaching a DO standard (say
5 mg/L). Combine scenario analysis with the Monte Carlo uncertainty from the
previous lesson and you get, for each scenario, not just a number but a
**distribution** - the probability that the standard is met. That is exactly
what a **total maximum daily load** (TMDL) study or an environmental impact
assessment needs.

Good scenario workflows are **scripted end to end** - inputs, model run,
metrics, and plots in version-controlled code - so a reviewer can reproduce
every figure. Modern practice layers on **digital twins** of treatment
plants and **machine-learning surrogates** that emulate a slow physical
model for near-real-time forecasting, but the logic is the same: define
scenarios, run, compare, decide.

```mermaid
graph LR
    MODEL["Calibrated model"] --> WRAP["Wrap as a function"]
    WRAP --> SCEN["Define scenarios as data"]
    SCEN --> LOOP["Run each scenario"]
    LOOP --> MC["Add Monte Carlo uncertainty"]
    MC --> TABLE["Compare metrics and risk"]
    TABLE --> DECIDE["Inform the decision"]
```

Remember: scenario analysis is how a model earns its keep - script it, run
the alternatives, carry the uncertainty through, and present the comparison
that supports a decision.
""",
        ),
        quiz_lesson(
            "Quiz: Scenario analysis with Python",
            (
                q(
                    "What is scenario analysis?",
                    (
                        opt("Calibrating the model to a single dataset"),
                        opt(
                            "Running a validated model under different assumptions and "
                            "comparing the outcomes to support a decision",
                            correct=True,
                        ),
                        opt("Measuring field data at one location"),
                        opt("Deriving the governing equation by hand"),
                    ),
                    "Scenarios explore what-if conditions - a new discharge, climate "
                    "change, an upgrade - and compare results.",
                ),
                q(
                    "Why script a scenario workflow end to end in version-controlled code?",
                    (
                        opt("To make it impossible to reproduce"),
                        opt(
                            "So inputs, runs, metrics and plots are reproducible and a "
                            "reviewer can regenerate every figure",
                            correct=True,
                        ),
                        opt("Because regulators forbid spreadsheets only"),
                        opt("To hide the assumptions from reviewers"),
                    ),
                    "Reproducibility is the point - scripted runs let anyone verify the analysis.",
                ),
                q(
                    "What do you gain by combining scenario analysis with Monte Carlo uncertainty?",
                    (
                        opt("A faster single deterministic run"),
                        opt(
                            "For each scenario, a distribution of outcomes - for example "
                            "the probability that a standard is met",
                            correct=True,
                        ),
                        opt("The exact true parameter values"),
                        opt("A guarantee the model is perfectly calibrated"),
                    ),
                    "Each scenario yields a distribution, so you can state the risk of "
                    "breaching a limit - what a TMDL or impact study needs.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What conservation principle underlies almost every environmental model?",
                    (
                        opt("Conservation of momentum only"),
                        opt(
                            "A mass balance on a control volume: accumulation equals "
                            "inflow minus outflow plus or minus reaction",
                            correct=True,
                        ),
                        opt("Conservation of curve numbers"),
                        opt("The Gaussian distribution"),
                    ),
                    "Every model in this course is a mass balance at heart - reactors, "
                    "rivers, aquifers, watersheds and plumes alike.",
                ),
                q(
                    "In a steady-state CSTR with first-order decay, how does outflow "
                    "concentration relate to inflow?",
                    (
                        opt("C = C_in always"),
                        opt(
                            "C = C_in / (1 + k*tau), where tau is the hydraulic residence time",
                            correct=True,
                        ),
                        opt("C = C_in * exp(k*tau)"),
                        opt("C = C_in * k * tau"),
                    ),
                    "Setting accumulation to zero gives C = C_in / (1 + k*tau); the PFR "
                    "form is C_in*exp(-k*tau).",
                ),
                q(
                    "What does the Streeter-Phelps oxygen sag curve describe?",
                    (
                        opt("Groundwater head along a flow path"),
                        opt(
                            "The dissolved-oxygen deficit downstream of a waste load, set "
                            "by deoxygenation versus reaeration",
                            correct=True,
                        ),
                        opt("The plume rise above a stack"),
                        opt("The runoff hydrograph of a watershed"),
                    ),
                    "BOD decay draws DO down, reaeration brings it back; the deepest "
                    "point (critical) is where the DO standard is at risk.",
                ),
                q(
                    "MODFLOW solves the groundwater flow equation using which method?",
                    (
                        opt("Gaussian plume superposition"),
                        opt("The SCS curve number"),
                        opt(
                            "Finite differences on a grid of cells, solving for hydraulic "
                            "head in each cell",
                            correct=True,
                        ),
                        opt("Monte Carlo sampling of heads"),
                    ),
                    "MODFLOW discretizes the aquifer into cells and solves the coupled "
                    "head equations - Darcy's law plus a cell mass balance.",
                ),
                q(
                    "Which tool pair matches its domain correctly?",
                    (
                        opt("AERMOD for groundwater, MODFLOW for air"),
                        opt(
                            "HEC-HMS for watershed hydrology and floods, SWMM for urban "
                            "drainage networks",
                            correct=True,
                        ),
                        opt("QUAL2K for aquifers, MODFLOW for rivers"),
                        opt("SWMM for atmospheric dispersion"),
                    ),
                    "HEC-HMS does rainfall-runoff and flood hydrographs; SWMM does urban "
                    "stormwater pipe and channel hydraulics.",
                ),
                q(
                    "What does AERMOD improve over the older Gaussian stability-class approach?",
                    (
                        opt("It removes the wind entirely"),
                        opt(
                            "It parameterizes dispersion from modern boundary-layer "
                            "meteorology and handles terrain and building downwash",
                            correct=True,
                        ),
                        opt("It switches from air to water quality"),
                        opt("It eliminates the need for an emission rate"),
                    ),
                    "AERMOD keeps a steady-state Gaussian core but grounds turbulence in "
                    "real boundary-layer physics - the EPA regulatory model.",
                ),
                q(
                    "Why must calibration and validation use different data?",
                    (
                        opt("To double the amount of computation"),
                        opt(
                            "So validation genuinely tests generalization on data the "
                            "model never saw, rather than the data it was tuned to",
                            correct=True,
                        ),
                        opt("Because regulators forbid reusing data"),
                        opt("It makes the NSE automatically equal to 1"),
                    ),
                    "Split the record: fit on the calibration set, prove it on held-out "
                    "validation data - the environmental train/test split.",
                ),
                q(
                    "What does a Nash-Sutcliffe efficiency less than 0 indicate?",
                    (
                        opt("A perfect model"),
                        opt("Zero bias"),
                        opt(
                            "The model performs worse than simply predicting the mean of "
                            "the observations",
                            correct=True,
                        ),
                        opt("The data are missing"),
                    ),
                    "NSE = 1 perfect, 0 matches the mean, negative is worse than the mean.",
                ),
                q(
                    "What is the difference between sensitivity analysis and uncertainty analysis?",
                    (
                        opt("They are the same procedure"),
                        opt(
                            "Sensitivity identifies which inputs most affect the output; "
                            "uncertainty quantifies the spread of the output given "
                            "uncertain inputs",
                            correct=True,
                        ),
                        opt("Sensitivity produces a confidence interval; uncertainty ranks inputs"),
                        opt("Both require a groundwater model"),
                    ),
                    "Sensitivity ranks inputs by influence; uncertainty (often via Monte "
                    "Carlo) reports the output distribution.",
                ),
                q(
                    "Why combine scenario analysis with Monte Carlo uncertainty in a "
                    "study like a TMDL?",
                    (
                        opt("To make the model deterministic"),
                        opt(
                            "It yields, per scenario, a distribution of outcomes - for "
                            "example the probability a standard is met - not just a single "
                            "number",
                            correct=True,
                        ),
                        opt("It removes the need for calibration"),
                        opt("It converts the model into a Gaussian plume"),
                    ),
                    "Carrying uncertainty through each scenario gives the risk of "
                    "breaching a limit, which is what the decision needs.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_MODELING_COURSES: tuple[SeedCourse, ...] = (_ENVIRONMENTAL_MODELING,)
