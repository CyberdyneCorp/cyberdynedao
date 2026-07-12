"""Academy seed content - Introduction to Environmental Engineering.

An orientation to environmental engineering: what environmental engineers
actually do across water, air, waste and climate; the major problems the
field exists to solve; the regulatory landscape (CONAMA, ABNT NBR, WHO,
EPA) and the ethics of the profession; and the modern data, GIS, modeling
and AI toolkit. It sits in front of the specialist courses (water
treatment, air quality, solid waste, hydrology) as the "what the field is
and how it fits together" introduction. Every lesson is a direct
explanation with a concrete example - a design equation, a mass balance,
a standards table or a Python snippet - and a mermaid diagram, followed by
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


_INTRO_ENVIRONMENTAL_ENGINEERING = SeedCourse(
    slug="intro-environmental-engineering",
    title="Introduction to Environmental Engineering",
    description=(
        "An orientation to environmental engineering before the specialist "
        "courses: what environmental engineers do across water, air, waste and "
        "climate, the major problems the field solves, the regulatory landscape "
        "and professional ethics, sustainability and the SDGs, and the modern "
        "data, GIS, modeling and AI toolkit - with real design equations, "
        "standards tables and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Introduction to Environmental Engineering

Environmental engineering applies science and engineering to **protect
human health and the environment**: making water safe to drink, treating
what we send back to rivers, keeping the air breathable, managing waste,
and cutting the emissions that drive climate change. It is where civil,
chemical and biological engineering meet public health and ecology.

This course is the **map** of the field. Every lesson explains one idea
directly, grounds it in a short real example (a design equation, a mass
balance, a standards table, or a Python snippet), and draws it as a
diagram. After each lesson there is a short quiz; at the end, a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **History and scope** - how the field grew from sanitation to climate
2. **The major problems** - water, air, waste, climate
3. **Roles and ethics** - what the engineer does and answers to
4. **Water and sanitation** - the supply and treatment picture
5. **Pollution and its control** - the general control strategy
6. **Legislation and licensing** - the rules and permits
7. **Sustainability and the SDGs** - the goals that frame the work
8. **The modern toolkit** - data, GIS, modeling and AI

This is the overview; the specialist courses in this track (water
treatment, air quality, solid waste, hydrology and modeling) are the deep
dives. Knowing where each fits makes them far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core purpose of environmental engineering?",
                    (
                        opt("Designing highways and bridges"),
                        opt(
                            "Applying science and engineering to protect human health "
                            "and the environment - water, air, waste and climate",
                            correct=True,
                        ),
                        opt("Writing environmental novels"),
                        opt("Selling carbon credits only"),
                    ),
                    "The field exists to safeguard public health and ecosystems using "
                    "engineering across water, air, waste and climate.",
                ),
                q(
                    "How does this course relate to the specialist courses in the track?",
                    (
                        opt("It replaces them"),
                        opt(
                            "It is the big-picture overview that shows where each topic "
                            "fits, before the specialist deep dives",
                            correct=True,
                        ),
                        opt("It only covers laboratory chemistry"),
                        opt("It is unrelated to the other courses"),
                    ),
                    "Learn the map first (this course), then the specialist courses "
                    "make sense in context.",
                ),
            ),
        ),
        # -- 1. History and scope --------------------------------------
        _t(
            "History and scope of environmental engineering",
            "9 min",
            """# History and scope of environmental engineering

Environmental engineering grew out of **sanitary engineering** - the 19th
century fight against waterborne disease. When John Snow traced an 1854
London cholera outbreak to a single contaminated water pump, he showed
that **infrastructure protects public health**. Cities responded with
sewers, filtered and later chlorinated water supplies, and epidemics of
cholera and typhoid collapsed. That link - clean water and sanitation
equals fewer deaths - is the foundation of the field.

The **scope widened** over time as new problems appeared:

- **1850s-1900s: Sanitation** - water supply, sewerage, disease control.
- **Mid 1900s: Pollution control** - industrial effluents, smog, rivers
  catching fire; the first air and water quality laws.
- **1970s: The environmental era** - the US EPA (1970), major clean air
  and water acts, and environmental impact assessment become standard.
- **1990s onward: Sustainability** - life-cycle thinking, ISO 14001
  environmental management, and the shift from "clean up" to "prevent."
- **2000s onward: Climate** - greenhouse gases, adaptation, and the
  energy-water-carbon links now sit alongside classic pollution work.

So a modern environmental engineer may design a drinking-water plant,
model a smokestack plume, plan a landfill, or estimate a project's carbon
footprint - the same discipline, a much broader mandate.

```mermaid
graph LR
    SAN["Sanitation 1850s"] --> POLL["Pollution control 1950s"]
    POLL --> ENV["Environmental era 1970s"]
    ENV --> SUS["Sustainability 1990s"]
    SUS --> CLI["Climate era 2000s"]
```

A quick sense of scale for why sanitation still dominates globally:

```text
WHO/UNICEF (illustrative global figures)
  People without safely managed drinking water : ~2.0 billion
  People without safely managed sanitation     : ~3.6 billion
  Leading cause of the disease burden addressed : diarrhoeal disease
```

Remember: the field began by proving that engineering saves lives through
clean water, and it has kept widening - from the water pump to the
climate - ever since.
""",
        ),
        quiz_lesson(
            "Quiz: History and scope of environmental engineering",
            (
                q(
                    "From which older discipline did environmental engineering grow?",
                    (
                        opt("Aerospace engineering"),
                        opt(
                            "Sanitary engineering - the 19th century fight against "
                            "waterborne disease with sewers and safe water supply",
                            correct=True,
                        ),
                        opt("Software engineering"),
                        opt("Mining engineering"),
                    ),
                    "Sanitary engineering (clean water, sewerage) proved infrastructure "
                    "protects public health and became the field's foundation.",
                ),
                q(
                    "What did John Snow's 1854 cholera investigation demonstrate?",
                    (
                        opt("That cholera spreads only through the air"),
                        opt(
                            "That contaminated water infrastructure drives disease - "
                            "linking a water source to an outbreak",
                            correct=True,
                        ),
                        opt("That antibiotics cure cholera"),
                        opt("That the field should focus on climate first"),
                    ),
                    "Tracing the outbreak to a single pump tied disease to water "
                    "infrastructure, the founding insight of sanitary engineering.",
                ),
                q(
                    "How has the scope of the field changed over time?",
                    (
                        opt("It has narrowed to only drinking water"),
                        opt(
                            "It widened from sanitation to pollution control, then "
                            "sustainability, then climate - a broader mandate",
                            correct=True,
                        ),
                        opt("It stopped changing after 1900"),
                        opt("It abandoned water once air laws appeared"),
                    ),
                    "Each era added a layer: sanitation, pollution control, "
                    "sustainability and now climate, all within one discipline.",
                ),
            ),
        ),
        # -- 2. The major problems -------------------------------------
        _t(
            "The major environmental problems",
            "10 min",
            """# The major environmental problems (water, air, waste, climate)

Almost everything an environmental engineer does maps to **four families
of problems**. Knowing the families - and the metrics used to measure each
- lets you place any specific task.

**Water.** Too little, too dirty, or in the wrong place. This covers
drinking-water scarcity and contamination, wastewater that pollutes rivers,
and flooding. The classic health metric for organic water pollution is
**BOD** (biochemical oxygen demand): how much dissolved oxygen microbes
consume breaking down the waste. High BOD starves fish of oxygen.

**Air.** Pollutants that harm health and ecosystems: **particulate matter
(PM2.5 and PM10)**, nitrogen oxides, sulphur dioxide, ozone and carbon
monoxide. PM2.5 - fine particles that reach deep into the lungs - is the
single largest environmental health risk worldwide.

**Waste.** The solids and hazardous materials society discards:
municipal solid waste, industrial and hazardous waste, and now electronic
waste. The strategy is the **waste hierarchy** (prevent, reuse, recycle,
recover, then dispose) rather than defaulting to landfill.

**Climate.** Greenhouse gases - mainly carbon dioxide, methane and nitrous
oxide - trapping heat and destabilising the climate. Measured in **carbon
dioxide equivalent** so gases of different potency can be summed.

These families interlock: a landfill leaks into water and emits methane
(climate); burning waste affects air. The engineer works across the web,
not one silo.

```mermaid
graph TD
    ENV["Environmental problems"] --> WATER["Water scarcity and pollution"]
    ENV --> AIR["Air pollution PM and gases"]
    ENV --> WASTE["Solid and hazardous waste"]
    ENV --> CLIMATE["Greenhouse gas emissions"]
    WASTE --> WATER
    WASTE --> CLIMATE
```

A few reference thresholds an engineer keeps in mind:

```text
Indicative health and quality guidelines
  WHO PM2.5 annual guideline        : 5 ug/m3
  WHO drinking water, E. coli       : 0 per 100 mL
  Well-treated sewage effluent BOD  : < 20 mg/L (varies by regulation)
  Global warming potential, methane : ~28 x CO2 over 100 years
```

Remember: water, air, waste and climate - four families, each with its own
yardstick, all connected. Most of the field is some combination of these.
""",
        ),
        quiz_lesson(
            "Quiz: The major environmental problems",
            (
                q(
                    "What are the four families of environmental problems in this course?",
                    (
                        opt("Noise, light, heat, vibration"),
                        opt(
                            "Water, air, waste, and climate",
                            correct=True,
                        ),
                        opt("Soil, rock, metal, glass"),
                        opt("Cost, schedule, scope, quality"),
                    ),
                    "Water, air, waste and climate organise almost all environmental "
                    "engineering work.",
                ),
                q(
                    "What does BOD (biochemical oxygen demand) measure?",
                    (
                        opt("The temperature of a river"),
                        opt(
                            "How much dissolved oxygen microbes consume breaking down "
                            "organic waste - high BOD starves water of oxygen",
                            correct=True,
                        ),
                        opt("The amount of plastic in the ocean"),
                        opt("The carbon footprint of a factory"),
                    ),
                    "BOD is the classic index of organic water pollution; it depletes "
                    "dissolved oxygen aquatic life needs.",
                ),
                q(
                    "Why are the four problem families described as interlocking?",
                    (
                        opt("They are actually the same problem"),
                        opt(
                            "Actions in one affect others - a landfill leaks to water "
                            "and emits methane to the climate, for example",
                            correct=True,
                        ),
                        opt("They never interact"),
                        opt("Only climate matters, the rest are ignorable"),
                    ),
                    "The families connect, so engineers work across the web rather than "
                    "treating each in isolation.",
                ),
            ),
        ),
        # -- 3. Roles and ethics ---------------------------------------
        _t(
            "The environmental engineer's roles and ethics",
            "9 min",
            """# The environmental engineer's roles and ethics

Environmental engineers work in many settings, but the roles cluster into
a few recognisable types:

- **Design** - sizing and specifying treatment plants, landfills, drainage
  and pollution controls (the classic engineering output).
- **Assessment** - environmental impact assessment (EIA), monitoring, and
  measuring what is actually in the water, air or soil.
- **Operations** - running and optimising plants and utilities day to day.
- **Regulation and consulting** - writing or enforcing standards, advising
  clients on permits and compliance.
- **Research** - developing new processes, sensors and models.

Across all of these, the profession is bound by a **code of ethics**. The
first canon in engineering codes (for example the ASCE and NSPE codes) is
blunt: **hold paramount the safety, health and welfare of the public**.
For environmental engineers that duty explicitly extends to the
**environment and future generations** - sustainable development is written
into modern codes.

That creates real tension. An engineer serves a client or employer but
must not do so at the public's expense. Practical duties that follow:

- **Competence** - work only within your area of expertise.
- **Honesty** - report data truthfully; do not hide an exceedance or bias a
  study toward the answer a client wants.
- **Disclosure** - reveal conflicts of interest; protect whistle-blowing on
  genuine dangers.
- **Sustainability** - weigh long-term and cumulative effects, not just the
  immediate permit.

```mermaid
graph TD
    ENG["Environmental engineer"] --> DUTY["Hold public safety paramount"]
    DUTY --> HEALTH["Protect health"]
    DUTY --> ENVI["Protect environment"]
    DUTY --> FUTURE["Protect future generations"]
    ENG --> CLIENT["Serve client honestly"]
    CLIENT --> DUTY
```

A worked ethical test many codes imply:

```text
Before signing off, ask:
  1. Is it safe for the public and workers   ? If no -> stop.
  2. Is the data honestly and fully reported ? If no -> fix it.
  3. Are long-term and cumulative effects weighed ?
  4. Are conflicts of interest disclosed     ?
  Only a clear yes to safety and honesty lets the rest proceed.
```

Remember: technical skill is necessary but not sufficient - the engineer's
first obligation is to the public and the environment, even above the
client who pays.
""",
        ),
        quiz_lesson(
            "Quiz: The environmental engineer's roles and ethics",
            (
                q(
                    "What is the first canon of engineering codes of ethics?",
                    (
                        opt("Maximise the client's profit"),
                        opt(
                            "Hold paramount the safety, health and welfare of the public "
                            "- extended to the environment and future generations",
                            correct=True,
                        ),
                        opt("Finish every project under budget"),
                        opt("Always use the newest technology"),
                    ),
                    "Public safety and welfare come first; modern environmental codes "
                    "add the environment and future generations explicitly.",
                ),
                q(
                    "A client pressures you to omit a pollutant exceedance from a "
                    "report. What does the ethics code require?",
                    (
                        opt("Omit it, since the client pays"),
                        opt(
                            "Report the data honestly and fully - hiding an exceedance "
                            "violates the duty of honesty and public protection",
                            correct=True,
                        ),
                        opt("Report it only if a colleague agrees"),
                        opt("Delete the underlying measurements"),
                    ),
                    "Honest, complete reporting is non-negotiable; the public interest "
                    "outranks the client's preference.",
                ),
                q(
                    "Which of these is a recognised role of environmental engineers?",
                    (
                        opt("Only writing novels about nature"),
                        opt(
                            "Design, assessment, operations, regulation and research "
                            "across water, air, waste and climate systems",
                            correct=True,
                        ),
                        opt("Exclusively trading stocks"),
                        opt("Only teaching, never practising"),
                    ),
                    "The roles cluster into design, assessment, operations, regulation "
                    "and research.",
                ),
            ),
        ),
        # -- 4. Water resources and sanitation -------------------------
        _t(
            "Water resources and sanitation overview",
            "10 min",
            """# Water resources and sanitation overview

Water is the field's oldest and largest domain. Two linked jobs: get
**safe water to people** (supply) and **safely return** what they use
(sanitation). Follow the water through the **urban water cycle**:

1. **Source** - a river, reservoir, or aquifer (groundwater).
2. **Drinking-water treatment** - typically coagulation, flocculation,
   sedimentation, filtration and disinfection, to meet a **potability
   standard** (for example WHO guidelines; in Brazil, the Ministry of
   Health potability rule).
3. **Distribution** - pumped through the network to homes and industry.
4. **Use** - domestic, industrial, agricultural.
5. **Wastewater collection** - sewers carry it away.
6. **Wastewater treatment** - usually preliminary, primary (settling),
   secondary (biological, removing BOD), and sometimes tertiary
   (nutrients, disinfection) before discharge.
7. **Return** - treated effluent goes back to a receiving water body,
   completing the cycle for the next user downstream.

```mermaid
graph LR
    SRC["Source river or aquifer"] --> DWT["Drinking water treatment"]
    DWT --> DIST["Distribution network"]
    DIST --> USE["Homes and industry"]
    USE --> SEW["Sewer collection"]
    SEW --> WWT["Wastewater treatment"]
    WWT --> REC["Receiving water body"]
    REC --> SRC
```

Engineers size these systems from **demand and flow**. A basic water
demand estimate:

```text
Average daily demand
  Q_avg = Population x per_capita_demand
  Example: 50000 people x 150 L/person/day
         = 7,500,000 L/day
         = 7,500 m3/day  (about 86.8 L/s)

Peak flows are a multiple of the average:
  Q_peak = peak_factor x Q_avg   (peak_factor often 1.5 to 2.5)
```

A key sanitation performance number is **treatment efficiency** - the
percent of a pollutant removed:

```text
Removal efficiency
  E = (C_in - C_out) / C_in x 100 percent
  Example (BOD): (200 - 20) / 200 x 100 = 90 percent
```

Remember: supply and sanitation are two halves of one urban water cycle,
sized from population and demand, and judged by whether the water meets a
potability standard going in and a discharge standard coming out.
""",
        ),
        quiz_lesson(
            "Quiz: Water resources and sanitation overview",
            (
                q(
                    "In the urban water cycle, what happens between 'use' and returning "
                    "water to a river?",
                    (
                        opt("Nothing - used water goes straight back"),
                        opt(
                            "Sewers collect it and wastewater treatment removes "
                            "pollutants before discharge to a receiving water body",
                            correct=True,
                        ),
                        opt("It is bottled and sold"),
                        opt("It evaporates completely"),
                    ),
                    "Collection then treatment (primary, secondary, sometimes tertiary) "
                    "protects the receiving water before return.",
                ),
                q(
                    "A plant reduces BOD from 200 mg/L to 20 mg/L. What is the removal efficiency?",
                    (
                        opt("20 percent"),
                        opt("50 percent"),
                        opt("90 percent", correct=True),
                        opt("110 percent"),
                    ),
                    "E = (200 - 20) / 200 x 100 = 90 percent.",
                ),
                q(
                    "Why must drinking-water treatment meet a potability standard?",
                    (
                        opt("To make the water taste sweet"),
                        opt(
                            "To ensure it is safe to drink - meeting health-based limits "
                            "such as WHO guidelines or a national potability rule",
                            correct=True,
                        ),
                        opt("Standards are optional decoration"),
                        opt("To increase the water pressure"),
                    ),
                    "Potability standards set health-based limits the treated water must "
                    "satisfy before distribution.",
                ),
            ),
        ),
        # -- 5. Pollution and its control ------------------------------
        _t(
            "Pollution and its control",
            "10 min",
            """# Pollution and its control (an overview)

**Pollution** is the introduction of substances or energy into the
environment at rates that cause harm. Two useful distinctions frame every
control decision.

**Point vs non-point sources.** A **point source** discharges from an
identifiable spot - a pipe, a stack, an outfall - and is relatively easy to
permit and treat. A **non-point (diffuse) source** - farm runoff, urban
stormwater, road dust - enters over a wide area and is far harder to
capture. Much modern effort targets diffuse pollution precisely because the
point sources were tackled first.

**The control hierarchy.** The cheapest and most effective control is not
to create the pollutant. In order of preference:

1. **Prevention / source reduction** - change the process so less waste
   forms (cleaner production).
2. **Minimisation and reuse** - recover and recycle within the process.
3. **Treatment** - remove or neutralise what remains (end-of-pipe).
4. **Safe disposal** - contain the unavoidable residual responsibly.

"End-of-pipe" treatment is the last resort, not the default. This mirrors
the waste hierarchy and the shift from "clean up" to "prevent."

```mermaid
graph TD
    POL["Pollution control"] --> PREV["Prevent at source"]
    PREV --> MIN["Minimise and reuse"]
    MIN --> TREAT["Treat end of pipe"]
    TREAT --> DISP["Safe disposal of residual"]
    POL --> SRC{"Point or non-point"}
    SRC -->|"point"| PIPE["Permit and treat outfall"]
    SRC -->|"non-point"| DIFF["Manage runoff over area"]
```

Treatment itself works by moving or destroying the pollutant, using
**physical** (screening, sedimentation, filtration), **chemical**
(coagulation, oxidation, neutralisation) and **biological** (microbes
digesting organics) processes - usually in combination.

A simple **mass balance** underlies most treatment sizing. For a substance
at steady state with no reaction:

```text
Mass in = Mass out
  Q_in x C_in = Q_out x C_out
  If a process removes 80 percent of a 500 mg/L stream:
    C_out = 500 x (1 - 0.80) = 100 mg/L
Loads (mass/time) matter more than concentration alone:
  Load = Q x C   ( e.g. m3/day x g/m3 = g/day )
```

Remember: prevent before you treat, treat before you dispose, and know
whether you are fighting a pipe you can point to or diffuse pollution
spread across the landscape.
""",
        ),
        quiz_lesson(
            "Quiz: Pollution and its control",
            (
                q(
                    "What is the difference between a point and a non-point source?",
                    (
                        opt("Point sources are always larger"),
                        opt(
                            "A point source discharges from an identifiable spot (a pipe "
                            "or stack); a non-point source enters diffusely over a wide "
                            "area, like farm runoff",
                            correct=True,
                        ),
                        opt("Non-point sources are always illegal"),
                        opt("There is no real difference"),
                    ),
                    "Point = one identifiable outfall, easy to permit; non-point = "
                    "diffuse and much harder to capture.",
                ),
                q(
                    "What is the preferred first step in the pollution control hierarchy?",
                    (
                        opt("End-of-pipe treatment"),
                        opt(
                            "Prevention or source reduction - changing the process so "
                            "less pollutant forms in the first place",
                            correct=True,
                        ),
                        opt("Safe disposal in a landfill"),
                        opt("Diluting it in a river"),
                    ),
                    "Prevent first, then minimise/reuse, then treat, then dispose; "
                    "end-of-pipe is the last resort.",
                ),
                q(
                    "A process removes 80 percent of a 500 mg/L stream. Using a mass "
                    "balance, what is the outlet concentration?",
                    (
                        opt("400 mg/L"),
                        opt("100 mg/L", correct=True),
                        opt("500 mg/L"),
                        opt("0 mg/L"),
                    ),
                    "C_out = 500 x (1 - 0.80) = 100 mg/L.",
                ),
            ),
        ),
        # -- 6. Legislation and licensing ------------------------------
        _t(
            "Environmental legislation and licensing",
            "10 min",
            """# Environmental legislation and licensing (an overview)

Engineering choices are bounded by **law**. Two things every environmental
engineer must read: the **standards** that set numeric limits, and the
**licensing process** that authorises a project to operate.

**Standards** come in layers - international guidance, national law, and
technical norms:

- **International** - WHO drinking-water and air-quality guidelines; ISO
  standards such as **ISO 14001** (environmental management systems).
- **National** - in Brazil, **CONAMA** resolutions set water-body
  classifications and effluent/air limits; the US relies on EPA rules under
  the Clean Water and Clean Air Acts and drinking-water regulations.
- **Technical norms** - **ABNT NBR** standards specify how to build and
  test (for example NBR 7229 for septic tanks); analogous to ASTM/EN
  elsewhere.

**Environmental licensing** is the permit pathway. In the Brazilian model
it runs in three stages, and most countries have an equivalent sequence:

1. **Preliminary license (LP)** - approves the project's location and
   concept, usually after an **environmental impact assessment (EIA/RIMA)**.
2. **Installation license (LI)** - authorises construction to the approved
   design and mitigation plan.
3. **Operation license (LO)** - authorises running the facility, with
   monitoring conditions attached; it is renewed periodically.

```mermaid
graph LR
    EIA["Impact assessment EIA"] --> LP["Preliminary license"]
    LP --> LI["Installation license"]
    LI --> LO["Operation license"]
    LO --> MON["Monitoring and renewal"]
    MON --> LO
```

A crosscutting principle behind the whole system is **the polluter pays**:
the party causing pollution bears the cost of preventing and remediating
it. Alongside it, the **precautionary principle** says a lack of full
scientific certainty is not a reason to postpone action against serious
harm.

A compliance check is a simple table lookup - measure, then compare to the
applicable limit:

```text
Parameter        Measured   Limit (illustrative)   Status
  BOD, effluent   45 mg/L    <= 60 mg/L or 80% rem   OK
  pH, effluent    9.4        5 to 9                   EXCEEDANCE
  PM10, air       120 ug/m3  <= 50 ug/m3 (WHO 24h)    EXCEEDANCE
```

Remember: know your numeric limits and your license stage. Design has to
satisfy the standard, and the project cannot legally operate without the
operating license and its monitoring conditions.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental legislation and licensing",
            (
                q(
                    "In the three-stage licensing model, which license authorises "
                    "actually running the facility?",
                    (
                        opt("The preliminary license (LP)"),
                        opt("The installation license (LI)"),
                        opt(
                            "The operation license (LO), which carries monitoring "
                            "conditions and is renewed periodically",
                            correct=True,
                        ),
                        opt("No license is needed to operate"),
                    ),
                    "LP approves location/concept, LI approves construction, LO "
                    "authorises operation with monitoring and renewal.",
                ),
                q(
                    "What does the 'polluter pays' principle mean?",
                    (
                        opt("The government pays for all cleanup"),
                        opt(
                            "The party causing pollution bears the cost of preventing "
                            "and remediating it",
                            correct=True,
                        ),
                        opt("Pollution is always free to emit"),
                        opt("Downstream users pay for upstream pollution"),
                    ),
                    "The cost of prevention and remediation falls on whoever causes the pollution.",
                ),
                q(
                    "Which of these is a set of Brazilian technical construction/testing "
                    "norms an environmental engineer follows?",
                    (
                        opt("ABNT NBR standards", correct=True),
                        opt("The periodic table"),
                        opt("The Kelvin scale"),
                        opt("The metric prefixes"),
                    ),
                    "ABNT NBR norms (e.g. NBR 7229 for septic tanks) specify how to "
                    "build and test, alongside CONAMA limits and WHO/ISO guidance.",
                ),
            ),
        ),
        # -- 7. Sustainability and the SDGs ----------------------------
        _t(
            "Sustainability and the Sustainable Development Goals",
            "9 min",
            """# Sustainability and the Sustainable Development Goals

**Sustainable development** is meeting present needs without compromising
the ability of future generations to meet theirs (the Brundtland
definition). It is usually drawn as **three pillars** that must all hold:
**environment, society and economy** - sometimes called people, planet and
prosperity. A project that is profitable but wrecks the environment, or
green but unaffordable, is not sustainable.

The world's shared agenda is the UN's **17 Sustainable Development Goals
(SDGs)**, adopted in 2015 for 2030. Several sit squarely in environmental
engineering:

- **SDG 6** - clean water and sanitation (the field's heartland).
- **SDG 7** - affordable and clean energy.
- **SDG 11** - sustainable cities (waste, drainage, air).
- **SDG 12** - responsible consumption and production (waste hierarchy,
  cleaner production).
- **SDG 13** - climate action.
- **SDG 14 and 15** - life below water and life on land.

A practical tool for putting sustainability into numbers is **life cycle
assessment (LCA)**, standardised by **ISO 14040/14044**. LCA tallies the
environmental impacts of a product or process across its whole life -
**cradle to grave** - so you compare options on total impact, not just the
part you see.

```mermaid
graph TD
    SD["Sustainable development"] --> ENV["Environment"]
    SD --> SOC["Society"]
    SD --> ECON["Economy"]
    ENV --> LCA["Life cycle assessment"]
    LCA --> RAW["Raw materials"]
    LCA --> MAKE["Manufacture and use"]
    LCA --> END["End of life"]
```

The four LCA stages in ISO 14040 give the workflow:

```text
LCA workflow (ISO 14040)
  1. Goal and scope   - what is compared, and boundaries (cradle to grave)
  2. Inventory (LCI)  - list all inputs and emissions
  3. Impact (LCIA)    - convert to impacts (e.g. kg CO2-eq, water use)
  4. Interpretation   - find hotspots, compare options, report honestly
```

Remember: sustainability balances environment, society and economy; the
SDGs are the shared targets; and LCA is how you measure whole-life impact
so a "green" choice is green across its entire life, not just on the label.
""",
        ),
        quiz_lesson(
            "Quiz: Sustainability and the Sustainable Development Goals",
            (
                q(
                    "What are the three pillars of sustainable development?",
                    (
                        opt("Water, air, and soil"),
                        opt(
                            "Environment, society, and economy - all three must hold",
                            correct=True,
                        ),
                        opt("Past, present, and future"),
                        opt("Design, build, operate"),
                    ),
                    "People, planet and prosperity: a choice must be environmentally, "
                    "socially and economically sound to be sustainable.",
                ),
                q(
                    "Which SDG is the heartland of environmental engineering?",
                    (
                        opt("SDG 4 - quality education"),
                        opt(
                            "SDG 6 - clean water and sanitation",
                            correct=True,
                        ),
                        opt("SDG 8 - decent work"),
                        opt("SDG 17 - partnerships"),
                    ),
                    "SDG 6 (clean water and sanitation) is the field's core, with SDG "
                    "11, 12 and 13 close behind.",
                ),
                q(
                    "What does a life cycle assessment (ISO 14040) evaluate?",
                    (
                        opt("Only the manufacturing cost"),
                        opt(
                            "Environmental impacts across a product's whole life, cradle "
                            "to grave, so options are compared on total impact",
                            correct=True,
                        ),
                        opt("Only the disposal step"),
                        opt("Only the marketing claims"),
                    ),
                    "LCA tallies impacts across the entire life cycle so a green choice "
                    "is green overall, not just at one stage.",
                ),
            ),
        ),
        # -- 8. The modern toolkit -------------------------------------
        _t(
            "The modern toolkit",
            "10 min",
            """# The modern toolkit (data, GIS, modeling, AI)

Modern environmental engineering runs on **data and computation**. Four
layers make up the digital toolkit, and they build on one another.

**1. Data and sensing.** Continuous measurement from **IoT sensors** (water
quality probes, low-cost air monitors), **remote sensing** (satellites like
Landsat and Sentinel for land use, floods, algal blooms, deforestation),
and public monitoring networks. The raw material of every decision.

**2. GIS - Geographic Information Systems.** Environmental data is
inherently **spatial**: watersheds, pollution plumes, service areas. GIS
(for example QGIS or ArcGIS) stores, maps and analyses data by location -
overlaying a river network, a population map and a discharge map to find
who is at risk.

**3. Modeling and simulation.** Physics-based models predict behaviour
before it happens. The standard workhorses:

- **EPANET** - drinking-water distribution networks.
- **SWMM** - urban stormwater and sewers.
- **QUAL2K** - river water quality.
- **AERMOD** - air-pollutant dispersion from sources.
- **MODFLOW** - groundwater flow.

Many rest on classic equations - for example **Darcy's law** for
groundwater and the **Streeter-Phelps** oxygen-sag model for rivers.

**4. AI and machine learning.** On top of the data, ML **forecasts and
detects**: predicting air-quality or flood peaks, spotting anomalies in
sensor streams, classifying satellite imagery for land-cover change, and
driving **digital twins** - live virtual replicas of a treatment plant used
to optimise and test operation. The discipline here is **responsible,
explainable AI**: models feeding public-health and permit decisions must be
validated, transparent and monitored, not black boxes.

```mermaid
graph LR
    SENSE["Sensors and satellites"] --> GIS["GIS spatial analysis"]
    GIS --> MODEL["Process models EPANET SWMM MODFLOW"]
    MODEL --> AI["Machine learning and forecasting"]
    AI --> TWIN["Digital twin and decisions"]
    TWIN --> SENSE
```

A tiny taste of the data layer - flag readings that breach a limit with
pandas:

```python
import pandas as pd

# hourly PM2.5 readings from a low-cost sensor (ug/m3)
df = pd.read_csv("pm25.csv", parse_dates=["timestamp"])
WHO_24H = 15.0  # WHO 24-hour PM2.5 guideline

daily = df.resample("D", on="timestamp")["pm25"].mean()
exceedances = daily[daily > WHO_24H]
print(f"Days over the WHO 24h guideline: {len(exceedances)}")
```

Remember: sense it, map it in GIS, simulate it with process models, then
learn from it with AI - and keep the AI transparent, because these outputs
protect public health.
""",
        ),
        quiz_lesson(
            "Quiz: The modern toolkit",
            (
                q(
                    "What is GIS used for in environmental engineering?",
                    (
                        opt("Compiling source code"),
                        opt(
                            "Storing, mapping and analysing environmental data by "
                            "location - overlaying spatial layers like watersheds and "
                            "populations",
                            correct=True,
                        ),
                        opt("Running the payroll"),
                        opt("Editing photographs for reports only"),
                    ),
                    "Environmental data is spatial; GIS analyses it by location to find, "
                    "for example, who is downstream of a discharge.",
                ),
                q(
                    "Which tool is the standard model for a drinking-water distribution network?",
                    (
                        opt("AERMOD"),
                        opt("EPANET", correct=True),
                        opt("MODFLOW"),
                        opt("A word processor"),
                    ),
                    "EPANET models water distribution; SWMM does stormwater, AERMOD air "
                    "dispersion, MODFLOW groundwater.",
                ),
                q(
                    "What is a 'digital twin' of a treatment plant?",
                    (
                        opt("A second physical plant built next door"),
                        opt(
                            "A live virtual replica fed by sensor data, used to optimise "
                            "and test operation",
                            correct=True,
                        ),
                        opt("A backup copy of the plant's paperwork"),
                        opt("A photograph of the plant"),
                    ),
                    "A digital twin mirrors the real plant in software so operators can "
                    "simulate and optimise before acting.",
                ),
                q(
                    "Why does the course stress responsible, explainable AI?",
                    (
                        opt("Because AI is banned in engineering"),
                        opt(
                            "Because these models feed public-health and permit "
                            "decisions, so they must be validated, transparent and "
                            "monitored, not black boxes",
                            correct=True,
                        ),
                        opt("Because explainable models are always more accurate"),
                        opt("Because regulators dislike all software"),
                    ),
                    "Outputs affecting public health and compliance must be trustworthy "
                    "and transparent, not opaque.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is environmental engineering?",
                    (
                        opt("Designing skyscrapers"),
                        opt(
                            "Applying science and engineering to protect human health "
                            "and the environment across water, air, waste and climate",
                            correct=True,
                        ),
                        opt("A branch of accounting"),
                        opt("Only the study of endangered species"),
                    ),
                    "The field safeguards public health and ecosystems through "
                    "engineering across the four problem families.",
                ),
                q(
                    "From which discipline did the field grow, and what did it prove?",
                    (
                        opt("Aerospace - that rockets fly"),
                        opt(
                            "Sanitary engineering - that clean water and sanitation "
                            "infrastructure protect public health",
                            correct=True,
                        ),
                        opt("Software - that code compiles"),
                        opt("Finance - that markets clear"),
                    ),
                    "Sanitary engineering (safe water, sewerage) is the foundation; it "
                    "showed infrastructure saves lives.",
                ),
                q(
                    "What does BOD indicate about water?",
                    (
                        opt("Its temperature"),
                        opt(
                            "Organic pollution - the dissolved oxygen microbes consume "
                            "degrading the waste, which can starve aquatic life",
                            correct=True,
                        ),
                        opt("Its electrical conductivity"),
                        opt("Its carbon footprint"),
                    ),
                    "High BOD means high organic load and low remaining oxygen for fish.",
                ),
                q(
                    "A treatment step cuts a pollutant from 300 mg/L to 60 mg/L. What is "
                    "the removal efficiency?",
                    (
                        opt("60 percent"),
                        opt("80 percent", correct=True),
                        opt("20 percent"),
                        opt("240 percent"),
                    ),
                    "E = (300 - 60) / 300 x 100 = 80 percent.",
                ),
                q(
                    "What is the preferred first action in the pollution control hierarchy?",
                    (
                        opt("End-of-pipe treatment"),
                        opt("Safe disposal"),
                        opt(
                            "Prevention at the source, so less pollutant forms in the first place",
                            correct=True,
                        ),
                        opt("Dilution in a river"),
                    ),
                    "Prevent, then minimise/reuse, then treat, then dispose.",
                ),
                q(
                    "Which license, in the three-stage model, authorises operating a "
                    "facility with monitoring conditions?",
                    (
                        opt("Preliminary license (LP)"),
                        opt("Installation license (LI)"),
                        opt("Operation license (LO)", correct=True),
                        opt("No license is required"),
                    ),
                    "LP approves concept, LI approves construction, LO authorises "
                    "operation and is renewed with monitoring.",
                ),
                q(
                    "What is the first canon of engineering ethics for the profession?",
                    (
                        opt("Maximise client profit above all"),
                        opt(
                            "Hold paramount the safety, health and welfare of the "
                            "public, extended to the environment and future generations",
                            correct=True,
                        ),
                        opt("Deliver every project early"),
                        opt("Use the newest technology available"),
                    ),
                    "Public safety and welfare - and the environment and future "
                    "generations - come before the client's interest.",
                ),
                q(
                    "What are the three pillars of sustainable development?",
                    (
                        opt("Air, water, soil"),
                        opt(
                            "Environment, society, and economy",
                            correct=True,
                        ),
                        opt("Plan, build, operate"),
                        opt("Local, national, global"),
                    ),
                    "A choice must be environmentally, socially and economically sound "
                    "to be sustainable; SDG 6 anchors the field.",
                ),
                q(
                    "Which set correctly pairs a model with its domain?",
                    (
                        opt("EPANET for payroll, SWMM for email"),
                        opt(
                            "EPANET for water distribution, SWMM for stormwater, MODFLOW "
                            "for groundwater, AERMOD for air dispersion",
                            correct=True,
                        ),
                        opt("AERMOD for accounting, MODFLOW for graphics"),
                        opt("All four model the same thing"),
                    ),
                    "EPANET water networks, SWMM stormwater, MODFLOW groundwater, "
                    "AERMOD air dispersion.",
                ),
                q(
                    "Why must AI used for environmental decisions be explainable and validated?",
                    (
                        opt("Because regulators forbid all software"),
                        opt("Because black-box models are always wrong"),
                        opt(
                            "Because the outputs feed public-health and permit "
                            "decisions, so they must be transparent, validated and "
                            "monitored - not opaque black boxes",
                            correct=True,
                        ),
                        opt("Because explainable models never need data"),
                    ),
                    "Responsible, explainable AI is required because these outputs "
                    "protect public health and inform compliance.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

INTRO_ENVIRONMENTAL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (
    _INTRO_ENVIRONMENTAL_ENGINEERING,
)
