"""Academy seed content - Water Supply and Treatment.

Turning raw water into safe drinking water: estimating demand and choosing
sources, the conventional treatment train from coagulation through
disinfection, advanced processes for hard-to-remove contaminants, and how
treated water reaches the tap. Every lesson is a direct explanation with a
worked design calculation and a mermaid diagram, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.
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


_WATER_TREATMENT = SeedCourse(
    slug="water-treatment",
    title="Water Supply and Treatment",
    description=(
        "Turning raw water into safe drinking water: demand and source "
        "selection, the conventional treatment train from coagulation to "
        "disinfection, advanced processes like membranes and advanced "
        "oxidation, and distribution - with worked design calculations, "
        "WHO/EPA and ABNT NBR references, and a diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Water Supply and Treatment

Clean drinking water is one of the great public-health achievements, and
behind every tap sits a **treatment train**: a sequence of physical and
chemical processes that takes raw water from a river, lake or aquifer and
makes it safe to drink. This course walks that train end to end, then goes
beyond it into advanced processes and distribution.

The approach is **concrete**: every lesson explains one process directly,
grounds it in real practice and standards (WHO and EPA drinking-water
guidelines, ABNT NBR and CONAMA in Brazil), shows a **worked design
calculation**, and draws the process as a diagram. After each lesson there
is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Water demand and source selection** - how much, from where
2. **Coagulation and flocculation** - destabilizing fine particles
3. **Sedimentation and flotation** - separating the solids
4. **Filtration** - polishing the clarified water
5. **Disinfection** - chlorine, UV and ozone
6. **Iron, manganese and hardness removal** - the common nuisances
7. **Membranes and advanced oxidation** - the modern edge
8. **Sludge handling and distribution** - residuals and delivery

The train is roughly linear, but each stage prepares the water for the
next. Knowing what each unit does - and how to size it - is what turns a
list of tanks into a working plant.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is a water 'treatment train'?",
                    (
                        opt("A single tank that does everything at once"),
                        opt(
                            "A sequence of physical and chemical unit processes that "
                            "together turn raw water into safe drinking water",
                            correct=True,
                        ),
                        opt("The pipeline that carries water to the city"),
                        opt("A rail line used to deliver bottled water"),
                    ),
                    "Each unit process (coagulation, sedimentation, filtration, "
                    "disinfection...) does one job and prepares water for the next.",
                ),
                q(
                    "Which standards does this course ground its examples in?",
                    (
                        opt("Only local city bylaws"),
                        opt(
                            "Drinking-water guidelines such as WHO and EPA, plus ABNT NBR "
                            "and CONAMA in Brazil",
                            correct=True,
                        ),
                        opt("Aviation safety standards"),
                        opt("No standards - just theory"),
                    ),
                    "Real treatment is driven by health-based limits from bodies like "
                    "WHO, EPA, and national standards.",
                ),
            ),
        ),
        # -- 1. Demand and sources -------------------------------------
        _t(
            "Water demand and source selection",
            "10 min",
            """# Water demand and source selection

Before you design any treatment, you must answer two questions: **how much
water is needed**, and **where does it come from**. Both drive every tank
size and pipe diameter downstream.

**Demand** is estimated from population and a **per-capita consumption**
figure (litres per person per day, often written L/cap/day or qpc). You
project the served population to a design horizon, multiply by consumption,
and apply peaking factors - because peak-day and peak-hour flows are much
larger than the average.

```text
Average daily demand:
  Q_avg = P * q / 86400        [L/s]
    P = population served [inhabitants]
    q = per-capita consumption [L/cap/day]
    86400 = seconds per day

Worked example (design horizon):
  P = 50,000 inhabitants
  q = 200 L/cap/day
  Q_avg = 50,000 * 200 / 86400 = 115.7 L/s

Peak factors (ABNT NBR 12211 style):
  K1 (max day)  = 1.2
  K2 (max hour) = 1.5
  Q_peak_hour = Q_avg * K1 * K2 = 115.7 * 1.2 * 1.5 = 208.3 L/s
```

**Source selection** trades off quantity, quality, and reliability:

- **Surface water** (rivers, lakes, reservoirs) - abundant but variable and
  exposed: turbidity spikes after rain, seasonal algae, pollution risk.
  Usually needs the full treatment train.
- **Groundwater** (wells, springs) - naturally filtered and steadier, often
  low turbidity, but can carry hardness, iron, manganese, nitrate, or
  arsenic. Frequently needs less clarification but targeted removal.
- **Reuse and desalination** - increasingly used where fresh sources are
  scarce; membrane-heavy and energy-intensive.

The **multiple-barrier principle** underlies it all: protect the source
first (a clean catchment is the cheapest treatment), then rely on
successive treatment barriers, so no single failure reaches the consumer.

```mermaid
graph TD
    POP["Projected population"] --> DEM["Estimate demand qpc times P"]
    DEM --> PEAK["Apply peak factors K1 and K2"]
    PEAK --> NEED["Design flow"]
    SRC["Candidate sources"] --> QUAL["Assess quantity and quality"]
    QUAL --> NEED
    NEED --> TRAIN["Size the treatment train"]
```

Remember: demand sets the *size* of the plant; source quality sets the
*shape* of the treatment train.
""",
        ),
        quiz_lesson(
            "Quiz: Water demand and source selection",
            (
                q(
                    "Average daily demand is estimated primarily from what?",
                    (
                        opt("Pipe diameter alone"),
                        opt(
                            "Served population multiplied by per-capita consumption, "
                            "projected to a design horizon",
                            correct=True,
                        ),
                        opt("The number of treatment tanks"),
                        opt("Rainfall only"),
                    ),
                    "Q_avg = P * q / 86400; peak factors then scale it to max-day and "
                    "max-hour flows.",
                ),
                q(
                    "Why apply peaking factors (K1, K2) to average demand?",
                    (
                        opt("To make the numbers larger for billing"),
                        opt(
                            "Peak-day and peak-hour flows exceed the average, and the "
                            "plant and pipes must handle those peaks",
                            correct=True,
                        ),
                        opt("Because average demand cannot be measured"),
                        opt("To convert litres to cubic metres"),
                    ),
                    "Infrastructure is sized for peak flow, not just the daily average.",
                ),
                q(
                    "Compared with surface water, groundwater typically...",
                    (
                        opt("is always dirtier and needs more clarification"),
                        opt(
                            "is steadier and often lower in turbidity, but may carry "
                            "hardness, iron, manganese, nitrate or arsenic",
                            correct=True,
                        ),
                        opt("never requires any treatment"),
                        opt("has higher turbidity after every rainfall"),
                    ),
                    "Groundwater is naturally filtered and stable but can need targeted "
                    "removal of dissolved constituents.",
                ),
            ),
        ),
        # -- 2. Coagulation and flocculation ---------------------------
        _t(
            "Coagulation and flocculation",
            "11 min",
            """# Coagulation and flocculation

Raw surface water is cloudy because it carries **colloids** - very fine
clay, silt and organic particles. They stay suspended because they carry
like (usually negative) surface charges that make them repel each other, so
they never settle on their own. **Coagulation** and **flocculation** fix
this in two linked steps.

**Coagulation** adds a **coagulant** - commonly aluminium sulphate (alum),
ferric chloride, or polyaluminium chloride (PAC) - and mixes it in
**rapidly**. The metal ions neutralize the particle charges and form
gelatinous metal-hydroxide precipitates, letting the destabilized colloids
begin to stick together. This is fast, high-energy mixing over seconds.

**Flocculation** follows with **slow, gentle** mixing for 20-40 minutes.
Gentle stirring promotes particle collisions so the tiny destabilized
particles grow into large, settleable **flocs** - without shearing them
apart.

The intensity of mixing is captured by the **velocity gradient G**:

```text
Velocity gradient:
  G = sqrt( P / (mu * V) )      [1/s]
    P  = power input [W]
    mu = dynamic viscosity of water [Pa.s]  (about 1.0e-3 at 20 C)
    V  = tank volume [m3]

Typical targets:
  Rapid mix (coagulation): G = 700 to 1000 1/s  (seconds)
  Flocculation:            G = 20 to 70 1/s     (20-40 min)

Worked example (flocculator):
  V = 300 m3, target G = 40 1/s, mu = 1.0e-3 Pa.s
  P = G^2 * mu * V = 40^2 * 1.0e-3 * 300 = 480 W
```

The right **coagulant dose** is found empirically with a **jar test** -
bench beakers dosed at different rates to see which produces the best
settling floc at the water's pH. Too little coagulant and colloids stay
dispersed; too much (overdosing) can restabilize them.

```mermaid
graph LR
    RAW["Raw water with colloids"] --> DOSE["Add coagulant"]
    DOSE --> RAPID["Rapid mix high G neutralize charge"]
    RAPID --> SLOW["Slow mix low G grow flocs"]
    SLOW --> FLOC["Settleable flocs"]
    JAR["Jar test"] --> DOSE
```

Remember: coagulation destabilizes the particles with fast mixing;
flocculation grows them into flocs with slow mixing. Get the dose from a
jar test.
""",
        ),
        quiz_lesson(
            "Quiz: Coagulation and flocculation",
            (
                q(
                    "Why do colloidal particles in raw water not settle on their own?",
                    (
                        opt("They are heavier than water"),
                        opt(
                            "They carry like surface charges that make them repel each "
                            "other, keeping them suspended",
                            correct=True,
                        ),
                        opt("They dissolve completely"),
                        opt("They are always removed by gravity in seconds"),
                    ),
                    "Coagulation neutralizes those charges so particles can stick together.",
                ),
                q(
                    "What is the key difference in mixing between coagulation and flocculation?",
                    (
                        opt("Both use identical slow mixing"),
                        opt(
                            "Coagulation is rapid high-energy mixing over seconds; "
                            "flocculation is slow gentle mixing over 20-40 minutes",
                            correct=True,
                        ),
                        opt("Coagulation is slow, flocculation is rapid"),
                        opt("Neither involves any mixing"),
                    ),
                    "Fast mix disperses the coagulant and neutralizes charge; slow mix "
                    "grows flocs without shearing them.",
                ),
                q(
                    "What is a jar test used to determine?",
                    (
                        opt("The pipe diameter for distribution"),
                        opt("The chlorine residual at the tap"),
                        opt(
                            "The optimal coagulant dose and conditions for good floc "
                            "formation at the water's pH",
                            correct=True,
                        ),
                        opt("The population to be served"),
                    ),
                    "Bench-scale jars at varying doses reveal the dose that settles best; "
                    "overdosing can restabilize colloids.",
                ),
            ),
        ),
        # -- 3. Sedimentation and flotation ----------------------------
        _t(
            "Sedimentation and flotation",
            "11 min",
            """# Sedimentation and flotation

After flocculation you have big, heavy flocs suspended in the water. Now
you separate them. The two main approaches are **sedimentation** (let them
sink) and **dissolved air flotation** (float them up).

**Sedimentation** is gravity settling in a large, quiet basin. The
governing design parameter is the **surface overflow rate (SOR)**, also
called the **surface loading rate** - the flow divided by the basin's
horizontal surface area. A particle is captured if its settling velocity is
at least the overflow rate:

```text
Surface overflow rate:
  SOR = Q / A          [m3/(m2.day)]  = m/day
    Q = flow [m3/day]
    A = plan surface area [m2]
  A particle settles out if v_settle >= SOR.

Typical SOR for floc after coagulation: 20 to 40 m3/(m2.day)

Worked example (sizing a settling basin):
  Q = 208 L/s = 208 * 86.4 = 17,971 m3/day
  Choose SOR = 30 m3/(m2.day)
  A = Q / SOR = 17,971 / 30 = 599 m2
  (e.g. a basin about 12 m wide x 50 m long)

Detention time also matters:
  t = V / Q  ->  aim for roughly 2 to 4 hours
```

Notice the SOR depends on **area, not depth** - a classic result of ideal
settling theory. **High-rate settlers** exploit this by adding inclined
**plates or tubes** that multiply the effective settling area in the same
footprint.

**Dissolved air flotation (DAF)** is the alternative for water with *light*
flocs that settle poorly - algae-laden or low-turbidity, highly coloured
water. Air is dissolved into recycled water under pressure, then released;
the resulting **microbubbles** attach to flocs and carry them to the
surface as a float layer skimmed off the top. DAF is compact and fast.

```mermaid
graph TD
    IN["Flocculated water"] --> CHOICE{"Floc density"}
    CHOICE -->|"heavy floc"| SED["Sedimentation gravity settling"]
    CHOICE -->|"light floc or algae"| DAF["Dissolved air flotation"]
    SED --> CLAR["Clarified water to filters"]
    DAF --> CLAR
    SED --> SLUDGE["Settled sludge"]
    DAF --> FLOAT["Skimmed float"]
```

Remember: sedimentation is sized by surface overflow rate (area, not
depth); DAF floats light flocs that will not sink. Both hand clarified
water to the filters.
""",
        ),
        quiz_lesson(
            "Quiz: Sedimentation and flotation",
            (
                q(
                    "The surface overflow rate for a settling basin depends mainly on...",
                    (
                        opt("the depth of the basin"),
                        opt(
                            "the flow divided by the plan surface area (area, not depth)",
                            correct=True,
                        ),
                        opt("the chlorine dose"),
                        opt("the pipe material"),
                    ),
                    "Ideal settling theory: a particle is captured if its settling "
                    "velocity is at least Q/A.",
                ),
                q(
                    "When is dissolved air flotation (DAF) preferred over sedimentation?",
                    (
                        opt("When flocs are dense and settle quickly"),
                        opt(
                            "When flocs are light and settle poorly - algae-laden or "
                            "low-turbidity, highly coloured water",
                            correct=True,
                        ),
                        opt("When there is no coagulation step"),
                        opt("Only for groundwater with high hardness"),
                    ),
                    "DAF uses microbubbles to float light flocs that would not sink.",
                ),
                q(
                    "How do inclined plate or tube settlers improve a basin?",
                    (
                        opt("They add chemicals to the water"),
                        opt("They heat the water to settle faster"),
                        opt(
                            "They multiply the effective settling area within the same "
                            "footprint, raising capacity",
                            correct=True,
                        ),
                        opt("They remove the need for coagulation"),
                    ),
                    "Since capture depends on area, more inclined surface area means "
                    "higher throughput in the same tank.",
                ),
            ),
        ),
        # -- 4. Filtration ---------------------------------------------
        _t(
            "Filtration",
            "11 min",
            """# Filtration

Sedimentation removes most solids, but the clarified water still carries
fine particles and floc that escaped settling. **Granular media filtration**
polishes it by passing water down through a bed of **sand** (often over a
supporting gravel layer, or with an anthracite layer on top - a
**dual-media** filter). This is the last particle barrier before
disinfection, and it is critical for removing chlorine-resistant pathogens
like *Cryptosporidium* cysts.

Removal is not just straining. Particles are captured by **depth
filtration** - trapped throughout the bed by contact, adhesion and
sedimentation onto the grains, not merely on the surface. That is why the
media has depth.

The key design parameter is the **filtration rate** (loading rate):

```text
Filtration rate:
  v = Q / A           [m3/(m2.h)]  = m/h
    Q = flow [m3/h]
    A = filter plan area [m2]

Typical rates:
  Slow sand filter:   0.1 to 0.3 m/h
  Rapid sand filter:  5 to 12 m/h  (most common in cities)

Worked example (sizing rapid filters):
  Q = 208 L/s = 748.8 m3/h
  Design rate v = 8 m/h
  Total area A = Q / v = 748.8 / 8 = 93.6 m2
  Use 4 filters -> ~23.4 m2 each (allows one offline for backwash)
```

As a filter runs, captured solids clog the pores and **head loss** rises.
When head loss reaches a limit (or turbidity breaks through), the filter is
cleaned by **backwashing** - reversing flow to fluidize the bed and flush
out the trapped solids. Provide enough filters that the plant keeps meeting
demand while one is being backwashed.

Filtered-water **turbidity** is the headline quality target: WHO and EPA
push treated turbidity below **1 NTU**, and ideally below **0.3 NTU**,
because low turbidity both signals good particle removal and lets
disinfection work efficiently.

```mermaid
graph TD
    CLAR["Clarified water"] --> BED["Down through sand and anthracite"]
    BED --> DEPTH["Depth filtration captures fines"]
    DEPTH --> FILT["Low turbidity filtrate"]
    FILT --> HL{"Head loss high"}
    HL -->|"no"| FILT
    HL -->|"yes"| BW["Backwash reverse flow"]
    BW --> BED
```

Remember: filtration is depth capture, not just straining; size it by
filtration rate, plan for backwash, and aim for turbidity under 1 NTU
before disinfection.
""",
        ),
        quiz_lesson(
            "Quiz: Filtration",
            (
                q(
                    "How does granular media filtration mainly capture particles?",
                    (
                        opt("Only by straining at the surface"),
                        opt(
                            "By depth filtration - particles adhere onto grains "
                            "throughout the bed, not just on top",
                            correct=True,
                        ),
                        opt("By dissolving them"),
                        opt("By boiling the water"),
                    ),
                    "That is why filter media has depth; capture happens throughout.",
                ),
                q(
                    "What does backwashing a rapid sand filter do?",
                    (
                        opt("Adds coagulant to the bed"),
                        opt("Disinfects the water"),
                        opt(
                            "Reverses flow to fluidize the bed and flush out trapped "
                            "solids when head loss gets too high",
                            correct=True,
                        ),
                        opt("Permanently removes the filter from service"),
                    ),
                    "Provide enough filters that demand is met while one backwashes.",
                ),
                q(
                    "What treated-water turbidity target do WHO and EPA push toward?",
                    (
                        opt("Below 1 NTU, ideally under 0.3 NTU", correct=True),
                        opt("Around 50 NTU"),
                        opt("Turbidity does not matter after filtration"),
                        opt("Exactly 10 NTU"),
                    ),
                    "Low turbidity signals good particle removal and helps disinfection "
                    "reach chlorine-resistant pathogens.",
                ),
            ),
        ),
        # -- 5. Disinfection -------------------------------------------
        _t(
            "Disinfection - chlorine, UV, ozone",
            "12 min",
            """# Disinfection - chlorine, UV, ozone

Filtration clears particles, but pathogens can remain. **Disinfection** is
the final barrier that inactivates bacteria, viruses and protozoa. Three
methods dominate: **chlorine**, **ultraviolet (UV)**, and **ozone**.

**Chlorination** is the workhorse. Chlorine gas or hypochlorite is added and
reacts to form **free chlorine** (HOCl and OCl-), a strong oxidant. Its
great advantage is a lasting **residual**: chlorine stays in the water
through the distribution network, guarding against recontamination all the
way to the tap. WHO recommends a residual of roughly **0.2 to 0.5 mg/L** at
the point of use. Its downside is **disinfection by-products (DBPs)** -
trihalomethanes (THMs) and haloacetic acids form when chlorine reacts with
natural organic matter, so THMs are regulated (EPA limit 80 ug/L).

Disinfection dose is quantified by the **CT concept**:

```text
CT = C * t          [mg.min/L]
    C = disinfectant residual concentration [mg/L]
    t = contact time [min]

A required CT (from tables) delivers a target log-inactivation for a
given pathogen, temperature and pH.

Worked example (contact tank):
  Required CT for the target = 15 mg.min/L
  Available residual C = 1.0 mg/L
  Needed contact time t = CT / C = 15 / 1.0 = 15 min
  If flow Q = 748.8 m3/h, contact volume V = Q * t/60
     V = 748.8 * 15/60 = 187 m3
```

**Ultraviolet (UV)** light damages microbial DNA so organisms cannot
reproduce. It is highly effective against chlorine-resistant
*Cryptosporidium* and *Giardia*, adds no chemicals and forms no DBPs - but
it leaves **no residual**, so it is usually paired with a small chlorine
dose for distribution protection. Dose is measured in mJ/cm2.

**Ozone (O3)** is the strongest common oxidant. It inactivates a very broad
range of pathogens fast, and also oxidizes taste, odour and colour
compounds. It is generated on site (it cannot be stored), is energy
intensive, and leaves no lasting residual - and it can form **bromate** if
the water contains bromide, which is itself regulated.

```mermaid
graph TD
    FILT["Filtered water"] --> DIS{"Disinfection method"}
    DIS -->|"chlorine"| CL["Free chlorine lasting residual"]
    DIS -->|"UV"| UV["UV damages DNA no residual"]
    DIS -->|"ozone"| OZ["Ozone strong oxidant no residual"]
    CL --> NET["Protected in distribution"]
    UV --> BOOST["Add chlorine for residual"]
    OZ --> BOOST
    BOOST --> NET
```

Remember: chlorine gives a protective residual but forms DBPs; UV and ozone
are powerful and chemical-light but leave no residual, so they are paired
with chlorine for the network. Size the dose with CT.
""",
        ),
        quiz_lesson(
            "Quiz: Disinfection - chlorine, UV, ozone",
            (
                q(
                    "What is the main advantage of chlorine over UV and ozone?",
                    (
                        opt("It forms no by-products"),
                        opt(
                            "It leaves a lasting residual that protects water through the "
                            "distribution network to the tap",
                            correct=True,
                        ),
                        opt("It requires no contact time"),
                        opt("It is the weakest oxidant"),
                    ),
                    "UV and ozone leave no residual, so they are usually paired with a "
                    "chlorine dose for the network.",
                ),
                q(
                    "In the CT concept, what do C and t represent?",
                    (
                        opt("Cost and time"),
                        opt(
                            "Disinfectant residual concentration and contact time - their "
                            "product sets the log-inactivation achieved",
                            correct=True,
                        ),
                        opt("Chlorine and turbidity"),
                        opt("Capacity and temperature only"),
                    ),
                    "CT = C * t; a required CT from tables delivers a target inactivation "
                    "for a pathogen, temperature and pH.",
                ),
                q(
                    "Which statement about UV disinfection is correct?",
                    (
                        opt("It leaves a strong chlorine residual"),
                        opt("It is ineffective against Cryptosporidium"),
                        opt(
                            "It damages microbial DNA and adds no chemicals or DBPs, but "
                            "leaves no residual for distribution",
                            correct=True,
                        ),
                        opt("It generates trihalomethanes"),
                    ),
                    "UV is excellent against chlorine-resistant protozoa but must be "
                    "paired with chlorine for downstream protection.",
                ),
                q(
                    "A disinfection by-product concern with chlorine is...",
                    (
                        opt("bromate only"),
                        opt(
                            "trihalomethanes and haloacetic acids formed when chlorine "
                            "reacts with natural organic matter",
                            correct=True,
                        ),
                        opt("dissolved oxygen"),
                        opt("increased turbidity"),
                    ),
                    "THMs are regulated (EPA limit 80 ug/L); ozone with bromide instead "
                    "risks bromate.",
                ),
            ),
        ),
        # -- 6. Iron, manganese and hardness ---------------------------
        _t(
            "Iron, manganese and hardness removal",
            "11 min",
            """# Iron, manganese and hardness removal

Some of the most common water problems are not pathogens or turbidity but
**dissolved minerals**, especially in groundwater. Three classics: **iron**,
**manganese**, and **hardness**. They are aesthetic and operational
nuisances more than acute health risks, but customers notice them fast.

**Iron (Fe) and manganese (Mn)** dissolve in oxygen-poor groundwater as
Fe(II) and Mn(II). They are colourless underground, but once exposed to air
they **oxidize** to insoluble Fe(III) and Mn(IV), staining laundry and
fixtures rust-brown or black and causing taste complaints. The standard
treatment is **oxidation followed by filtration**: aerate (or dose an
oxidant like chlorine, potassium permanganate or ozone) to precipitate the
metals, then filter out the particles. Manganese is slower to oxidize and
needs a higher pH than iron.

```text
Iron oxidation (simplified):
  4 Fe(2+) + O2 + 10 H2O -> 4 Fe(OH)3 (solid) + 8 H(+)

Oxidant demand (stoichiometry, approximate):
  O2 needed   ~ 0.14 mg per mg Fe(2+)
  Cl2 needed  ~ 0.62 mg per mg Fe(2+),  ~1.27 mg per mg Mn(2+)

Worked example:
  Raw Fe = 2.0 mg/L, Mn = 0.5 mg/L
  Chlorine demand = 2.0*0.62 + 0.5*1.27 = 1.24 + 0.64 = 1.88 mg/L
  (add this on top of the disinfection residual you want to keep)
```

**Hardness** is dissolved **calcium and magnesium** (Ca2+, Mg2+), reported
as mg/L of CaCO3. Hard water scales pipes and boilers and wastes soap; it
is not a health hazard. Two removal routes:

- **Lime softening** - add lime (and sometimes soda ash) to raise pH and
  precipitate CaCO3 and Mg(OH)2, which settle out. Good for large plants.
- **Ion exchange** - pass water through a resin that swaps Ca2+ and Mg2+
  for Na+; the resin is regenerated with brine. This is how household
  softeners work.

```text
Hardness classes (as CaCO3):
  Soft:            < 60 mg/L
  Moderately hard: 60 to 120 mg/L
  Hard:            120 to 180 mg/L
  Very hard:       > 180 mg/L
```

```mermaid
graph TD
    GW["Groundwater"] --> FEMN{"Fe and Mn present"}
    FEMN -->|"yes"| OX["Aerate or oxidize"]
    OX --> FILT["Filter out precipitates"]
    GW --> HARD{"Hardness high"}
    HARD -->|"lime"| LIME["Lime softening precipitate"]
    HARD -->|"resin"| IEX["Ion exchange swap for sodium"]
    FILT --> OUT["Treated water"]
    LIME --> OUT
    IEX --> OUT
```

Remember: iron and manganese are removed by oxidize-then-filter; hardness
is removed by lime softening or ion exchange. These are mostly aesthetic
and operational fixes, not disinfection.
""",
        ),
        quiz_lesson(
            "Quiz: Iron, manganese and hardness removal",
            (
                q(
                    "What is the standard way to remove dissolved iron and manganese?",
                    (
                        opt("Boil the water"),
                        opt(
                            "Oxidize them (by aeration or an oxidant) to insoluble forms, "
                            "then filter out the precipitates",
                            correct=True,
                        ),
                        opt("Add more coagulant only"),
                        opt("Raise the turbidity"),
                    ),
                    "Fe(II)/Mn(II) are soluble until oxidized; manganese needs a higher "
                    "pH and oxidizes more slowly than iron.",
                ),
                q(
                    "Water hardness is caused by which dissolved ions?",
                    (
                        opt("Sodium and chloride"),
                        opt(
                            "Calcium and magnesium, usually reported as mg/L of CaCO3",
                            correct=True,
                        ),
                        opt("Iron and manganese"),
                        opt("Nitrate and arsenic"),
                    ),
                    "Hardness scales pipes and wastes soap but is not a health hazard.",
                ),
                q(
                    "How does a household ion-exchange softener remove hardness?",
                    (
                        opt("It oxidizes calcium into a gas"),
                        opt(
                            "A resin swaps Ca2+ and Mg2+ for Na+, and is regenerated with brine",
                            correct=True,
                        ),
                        opt("It filters out dissolved calcium by straining"),
                        opt("It chlorinates the hardness away"),
                    ),
                    "Lime softening is the large-plant alternative: precipitate CaCO3 and "
                    "Mg(OH)2 at raised pH.",
                ),
            ),
        ),
        # -- 7. Membranes and advanced oxidation -----------------------
        _t(
            "Membranes and advanced oxidation",
            "11 min",
            """# Membranes and advanced oxidation

Conventional treatment handles most surface and groundwater, but modern
challenges - desalination, water reuse, and trace contaminants like
pesticides, pharmaceuticals and PFAS - push beyond it. Two advanced
families answer: **membranes** and **advanced oxidation processes (AOPs)**.

**Membranes** are thin barriers that let water pass while rejecting
contaminants by size and, for the tightest ones, charge. They form a
spectrum by pore size:

```text
Membrane spectrum (loosest to tightest):
  Microfiltration (MF)   ~0.1 um     removes particles, most bacteria
  Ultrafiltration (UF)   ~0.01 um    removes viruses, colloids, macromolecules
  Nanofiltration (NF)    ~0.001 um   removes divalent ions, softening, organics
  Reverse osmosis (RO)   dense film  removes monovalent salts - desalination

Reverse osmosis basics:
  Applied pressure must exceed osmotic pressure of the feed.
  Seawater osmotic pressure ~ 27 bar; RO runs at 55 to 70 bar.

Recovery:
  r = Q_permeate / Q_feed   (fraction recovered as clean water)
  Worked example: feed 1000 m3/d, permeate 450 m3/d
    r = 450 / 1000 = 0.45 = 45 percent
    concentrate (brine) = 550 m3/d must be managed
```

MF and UF are increasingly used *instead of* sand filters (a strong,
absolute barrier to *Cryptosporidium*); NF and RO handle dissolved salts and
organics. The price is **energy** (especially RO) and a **concentrate/brine**
stream to dispose of.

**Advanced oxidation processes (AOPs)** generate highly reactive **hydroxyl
radicals (OH.)** - a far stronger and less selective oxidant than chlorine
or even ozone - to destroy trace organic pollutants that other steps miss.
Common combinations: **ozone + hydrogen peroxide**, **UV + hydrogen
peroxide**, and UV/ozone. AOPs *mineralize* micropollutants (break them down
toward CO2 and water) rather than just moving them to another phase, which
is why they are central to potable reuse.

```mermaid
graph TD
    FEED["Feed water"] --> MEM{"Contaminant type"}
    MEM -->|"particles and microbes"| MFUF["MF or UF barrier"]
    MEM -->|"dissolved salts"| RO["NF or RO"]
    RO --> BRINE["Concentrate to manage"]
    FEED --> TRACE{"Trace organics"}
    TRACE -->|"yes"| AOP["AOP hydroxyl radicals"]
    AOP --> MIN["Micropollutants mineralized"]
    MFUF --> CLEAN["High quality water"]
    RO --> CLEAN
    MIN --> CLEAN
```

Remember: membranes reject by size and charge (MF/UF for particles and
microbes, NF/RO for dissolved salts), at an energy and brine cost; AOPs use
hydroxyl radicals to destroy trace organics. Together they enable
desalination and safe water reuse.
""",
        ),
        quiz_lesson(
            "Quiz: Membranes and advanced oxidation",
            (
                q(
                    "Which membrane process is used for seawater desalination?",
                    (
                        opt("Microfiltration"),
                        opt("Ultrafiltration"),
                        opt(
                            "Reverse osmosis - a dense membrane that rejects monovalent "
                            "salts under high pressure",
                            correct=True,
                        ),
                        opt("Nanofiltration only"),
                    ),
                    "RO must apply pressure above the feed's osmotic pressure; seawater "
                    "RO runs at roughly 55 to 70 bar.",
                ),
                q(
                    "What do advanced oxidation processes (AOPs) rely on?",
                    (
                        opt("Straining by pore size"),
                        opt(
                            "Highly reactive hydroxyl radicals that destroy trace organic "
                            "pollutants, often from ozone or UV with hydrogen peroxide",
                            correct=True,
                        ),
                        opt("Adding calcium to the water"),
                        opt("Freezing the contaminants"),
                    ),
                    "Hydroxyl radicals are a stronger, less selective oxidant than "
                    "chlorine or ozone and can mineralize micropollutants.",
                ),
                q(
                    "A downside of reverse osmosis that must be managed is...",
                    (
                        opt("it produces no clean water"),
                        opt(
                            "high energy use and a concentrate (brine) stream that needs disposal",
                            correct=True,
                        ),
                        opt("it cannot remove any salts"),
                        opt("it increases turbidity"),
                    ),
                    "Recovery r = permeate/feed; the rejected fraction leaves as "
                    "concentrate that must be handled.",
                ),
            ),
        ),
        # -- 8. Sludge and distribution --------------------------------
        _t(
            "Sludge handling and distribution networks",
            "11 min",
            """# Sludge handling and distribution networks

A treatment plant makes clean water - and **residuals**. Every barrier that
removes something produces a waste stream, and the plant is not finished
until those are handled and the treated water actually reaches homes at
adequate pressure.

**Sludge and residuals** come mainly from the clarifiers (settled coagulant
sludge) and filter **backwash** water. This sludge is watery, so the job is
to **thicken and dewater** it - reduce volume so it can be disposed of or
reused (e.g. as landfill cover or, where permitted, land application):

```text
Sludge dewatering - volume shrinks sharply as solids concentrate:
  V2 / V1 = (100 - p1) / (100 - p2)     (approx, mass of solids constant)
    p = percent solids by mass

Worked example:
  Thicken sludge from 1 percent to 5 percent solids:
    V2 / V1 = (100 - 1) / (100 - 5) = 99 / 95 = 0.94  (thickening only)
  Then dewater 1 percent to 25 percent solids on a belt press:
    V2 / V1 = (100 - 1) / (100 - 25) = 99 / 75 = 1.32 ...
    inverted for solids basis: a 25x concentration cuts volume ~25-fold.
```

Backwash water is often **recovered** (settled and returned to the plant
head) to save water. Coagulant sludge and disposal must comply with
environmental rules (in Brazil, CONAMA resolutions and ABNT NBR guidance).

**Distribution** delivers treated water reliably. Key elements:

- **Storage reservoirs** - balance supply against fluctuating demand and
  provide reserve for fire flow and outages.
- **Pumps and pressure zones** - maintain adequate pressure everywhere (a
  common target is roughly 20 to 50 metres of head, about 200 to 500 kPa);
  pressure zones handle hilly terrain.
- **A looped network** - pipes connected in loops rather than dead-end
  branches, so water can reach any point by multiple paths (resilience and
  fewer stagnation zones).
- **Maintaining a disinfectant residual** and positive pressure everywhere
  to prevent contamination getting in.

Engineers model networks with tools like **EPANET** to check pressures,
flows, and how the chlorine residual decays across the system.

```mermaid
graph TD
    PLANT["Treatment plant"] --> RES["Clarifier and filter residuals"]
    RES --> THICK["Thicken and dewater"]
    THICK --> DISP["Dispose or reuse"]
    PLANT --> CLEAN["Treated water"]
    CLEAN --> STORE["Storage reservoirs"]
    STORE --> PUMP["Pumps and pressure zones"]
    PUMP --> LOOP["Looped network with residual"]
    LOOP --> TAP["Consumer taps"]
```

Remember: residuals must be thickened, dewatered and disposed of
responsibly; distribution needs storage, adequate pressure, a looped
resilient network, and a maintained residual - modelled with tools like
EPANET.
""",
        ),
        quiz_lesson(
            "Quiz: Sludge handling and distribution networks",
            (
                q(
                    "Where does most treatment-plant sludge come from?",
                    (
                        opt("The distribution reservoirs"),
                        opt(
                            "The clarifiers (settled coagulant sludge) and filter backwash water",
                            correct=True,
                        ),
                        opt("The disinfection contact tank only"),
                        opt("The consumer taps"),
                    ),
                    "Residuals are thickened and dewatered to cut volume before disposal or reuse.",
                ),
                q(
                    "Why are distribution networks usually built as loops rather than dead-end branches?",
                    (
                        opt("To use more pipe for no reason"),
                        opt(
                            "So water can reach any point by multiple paths - improving "
                            "resilience and reducing stagnation",
                            correct=True,
                        ),
                        opt("Because loops need no pumping"),
                        opt("To avoid maintaining any residual"),
                    ),
                    "Looped networks are more resilient and have fewer dead-end stagnation zones.",
                ),
                q(
                    "What tool is commonly used to model pressures, flows and residual decay in a distribution network?",
                    (
                        opt("AERMOD"),
                        opt("EPANET", correct=True),
                        opt("MODFLOW"),
                        opt("A jar test"),
                    ),
                    "EPANET simulates hydraulics and water quality (like chlorine decay) "
                    "across a network.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "Average daily water demand is estimated from...",
                    (
                        opt("the number of tanks in the plant"),
                        opt(
                            "served population times per-capita consumption, then scaled "
                            "by peak factors",
                            correct=True,
                        ),
                        opt("chlorine residual at the tap"),
                        opt("the pipe material only"),
                    ),
                    "Q_avg = P * q / 86400; peak factors give max-day and max-hour flows "
                    "for sizing.",
                ),
                q(
                    "What is the correct order of the conventional treatment train?",
                    (
                        opt("Disinfection, filtration, coagulation, sedimentation"),
                        opt(
                            "Coagulation and flocculation, sedimentation, filtration, disinfection",
                            correct=True,
                        ),
                        opt("Filtration, disinfection, coagulation, sedimentation"),
                        opt("Sedimentation, disinfection, coagulation, filtration"),
                    ),
                    "Destabilize particles, settle them, filter the fines, then disinfect.",
                ),
                q(
                    "What does the velocity gradient G describe in coagulation and flocculation?",
                    (
                        opt("The chlorine residual"),
                        opt(
                            "The intensity of mixing - high G for rapid mix, low G for "
                            "gentle floc growth",
                            correct=True,
                        ),
                        opt("The filter loading rate"),
                        opt("The osmotic pressure"),
                    ),
                    "G = sqrt(P/(mu*V)); rapid mix uses high G, flocculation low G to "
                    "grow flocs without shearing.",
                ),
                q(
                    "The surface overflow rate that sizes a settling basin depends mainly on...",
                    (
                        opt("basin depth"),
                        opt("flow divided by plan surface area (area, not depth)", correct=True),
                        opt("chlorine dose"),
                        opt("pipe diameter"),
                    ),
                    "Ideal settling: a particle is captured if its settling velocity is "
                    "at least Q/A; inclined plates add area in the same footprint.",
                ),
                q(
                    "Rapid sand filters mainly work by...",
                    (
                        opt("boiling the water"),
                        opt(
                            "depth filtration - capturing fine particles onto grains "
                            "throughout the bed, cleaned by backwashing",
                            correct=True,
                        ),
                        opt("adding coagulant"),
                        opt("reverse osmosis"),
                    ),
                    "The last particle barrier before disinfection; aim for turbidity under 1 NTU.",
                ),
                q(
                    "In disinfection, the CT concept multiplies...",
                    (
                        opt("cost times time"),
                        opt(
                            "disinfectant residual concentration times contact time to "
                            "reach a target inactivation",
                            correct=True,
                        ),
                        opt("chlorine times turbidity"),
                        opt("capacity times temperature"),
                    ),
                    "A required CT from tables delivers the target log-inactivation for a "
                    "pathogen at a given temperature and pH.",
                ),
                q(
                    "Which disinfectant leaves a lasting residual to protect the distribution network?",
                    (
                        opt("Ultraviolet light"),
                        opt("Ozone"),
                        opt("Chlorine (free chlorine)", correct=True),
                        opt("None of them leave any residual"),
                    ),
                    "UV and ozone leave no residual, so they are paired with a chlorine "
                    "dose for the network.",
                ),
                q(
                    "How are dissolved iron and manganese in groundwater removed?",
                    (
                        opt("Ion exchange for sodium only"),
                        opt(
                            "Oxidize them to insoluble forms (aeration or an oxidant), then filter",
                            correct=True,
                        ),
                        opt("Reverse osmosis is the only option"),
                        opt("They cannot be removed"),
                    ),
                    "Manganese oxidizes more slowly and needs a higher pH than iron.",
                ),
                q(
                    "Which membrane process removes monovalent salts for desalination?",
                    (
                        opt("Microfiltration"),
                        opt("Reverse osmosis", correct=True),
                        opt("Ultrafiltration"),
                        opt("A rapid sand filter"),
                    ),
                    "MF/UF remove particles and microbes; NF/RO handle dissolved salts, "
                    "at an energy and brine cost.",
                ),
                q(
                    "A well-designed distribution network typically features...",
                    (
                        opt("dead-end branches only, with no storage"),
                        opt(
                            "storage reservoirs, adequate pressure, a looped resilient "
                            "layout, and a maintained disinfectant residual",
                            correct=True,
                        ),
                        opt("no pumps and no residual"),
                        opt("a single pipe with no redundancy"),
                    ),
                    "Loops give multiple paths and less stagnation; EPANET models "
                    "pressures, flows and residual decay.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

WATER_TREATMENT_COURSES: tuple[SeedCourse, ...] = (_WATER_TREATMENT,)
