"""Academy seed content - Environmental Disaster Management and Resilience.

Preparing for and responding to environmental disasters - floods,
landslides, droughts, wildfires, industrial spills and dam or tailings
failures. The course covers hazard and risk fundamentals, the physics of
each hazard, early warning and emergency planning, and resilient
reconstruction. Every lesson is a direct explanation grounded in real
practice (CONAMA/ABNT NBR, WHO/EPA, Sendai Framework, IPCC) with a
mermaid diagram and a worked formula or calculation, followed by a
checkpoint quiz; the course closes with a comprehensive final quiz.
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


_DISASTER_RISK_RESILIENCE = SeedCourse(
    slug="disaster-risk-resilience",
    title="Environmental Disaster Management and Resilience",
    description=(
        "Preparing for and responding to environmental disasters - floods, "
        "landslides, droughts, wildfires, industrial spills and dam or "
        "tailings failures. You learn how each hazard works, how risk is "
        "quantified, how early warning and emergency plans limit harm, and "
        "how to rebuild resiliently - grounded in the Sendai Framework, "
        "CONAMA/ABNT NBR and WHO/EPA practice, with a worked calculation "
        "and a diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Disaster Management and Resilience

Environmental disasters are not purely acts of nature. A flood, a
landslide, or a tailings-dam failure becomes a *disaster* only when a
**hazard** meets **exposed, vulnerable** people and assets. That framing
is the good news: while we rarely stop the hazard, we can shrink the
exposure and vulnerability - and that is what disaster risk management
does.

This course is **practical and quantitative**. Every lesson explains one
family of hazards or one part of the management cycle directly, shows the
core idea in a diagram, and works through a real formula or calculation
you would actually use - a return period, a factor of safety, a dam-break
wave, a plume footprint.

What you will build understanding for, in order:

1. **Natural and technological hazards** - the risk equation and the DRM cycle
2. **Floods and flood risk** - return periods, mapping, and defence
3. **Landslides and mass movements** - slope stability and triggers
4. **Droughts and wildfires** - slow-onset stress and fire behaviour
5. **Industrial accidents and spills** - source terms and containment
6. **Dam and tailings failures** - breach, inundation, and Brazil's lessons
7. **Early warning and emergency planning** - the four-element chain
8. **Resilient reconstruction and continuity** - building back better

The guiding standards are the UN **Sendai Framework** for disaster risk
reduction, Brazil's **CONAMA/ABNT NBR** environmental rules, and
**WHO/EPA/IPCC** guidance. Knowing where each hazard and each control
fits makes the whole field far easier to reason about.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "When does a natural hazard become a 'disaster'?",
                    (
                        opt("Whenever the hazard is physically large"),
                        opt(
                            "When a hazard meets exposed and vulnerable people and "
                            "assets, overwhelming their capacity to cope",
                            correct=True,
                        ),
                        opt("Only when it is reported in the news"),
                        opt("Only when it happens at night"),
                    ),
                    "Disaster = hazard x exposure x vulnerability; a huge hazard in an "
                    "empty desert harms no one.",
                ),
                q(
                    "What is the practical hope in disaster risk management?",
                    (
                        opt("We can usually prevent the hazard itself"),
                        opt(
                            "We can reduce exposure and vulnerability even when we cannot "
                            "stop the hazard",
                            correct=True,
                        ),
                        opt("Disasters are random and nothing helps"),
                        opt("Only insurance matters"),
                    ),
                    "You rarely stop an earthquake or a storm, but you can move people "
                    "out of harm's way and strengthen what remains.",
                ),
            ),
        ),
        # -- 1. Natural and technological hazards ----------------------
        _t(
            "Natural and technological hazards",
            "10 min",
            """# Natural and technological hazards

A **hazard** is a process or event that can cause harm. Hazards split
into two broad families:

- **Natural hazards** - hydrometeorological (floods, droughts, storms),
  geophysical (landslides, earthquakes), and climatological (wildfires,
  heatwaves).
- **Technological (na-tech) hazards** - failures of human systems:
  chemical spills, industrial explosions, dam and tailings breaches.
  These often *cascade* from a natural trigger - a flood that ruptures a
  pipeline is a **na-tech** event.

Risk is the combination of three factors. A widely used relation:

```text
Risk = Hazard x Exposure x Vulnerability

Hazard        - probability and intensity of the damaging event
Exposure      - people and assets located where the hazard acts
Vulnerability - the degree to which they are harmed when it hits
                (mitigated by Capacity - preparedness and resources)

Worked example (annual expected loss):
  Hazard        P(flood in a year) = 0.02   (a 1-in-50-year flood)
  Exposure      value at risk      = R$ 20,000,000
  Vulnerability damage fraction    = 0.30
  Expected Annual Loss = 0.02 x 20,000,000 x 0.30 = R$ 120,000
```

Managing risk is a continuous **disaster risk management (DRM) cycle**,
not a one-off. The UN **Sendai Framework (2015-2030)** organises it
around four priorities: understand risk, strengthen governance, invest in
resilience, and enhance preparedness for "build back better".

```mermaid
graph LR
    PREV["Prevention and mitigation"] --> PREP["Preparedness"]
    PREP --> RESP["Response"]
    RESP --> REC["Recovery and reconstruction"]
    REC --> PREV
```

Remember: you cannot manage what you have not measured. Estimating hazard,
exposure and vulnerability separately is the first step, because each one
is reduced by different actions.
""",
        ),
        quiz_lesson(
            "Quiz: Natural and technological hazards",
            (
                q(
                    "What are the three factors in the standard risk relation?",
                    (
                        opt("Wind, water, and fire"),
                        opt(
                            "Hazard, exposure, and vulnerability",
                            correct=True,
                        ),
                        opt("Cost, schedule, and scope"),
                        opt("Prevention, response, and recovery"),
                    ),
                    "Risk = Hazard x Exposure x Vulnerability; capacity reduces vulnerability.",
                ),
                q(
                    "What is a 'na-tech' (technological) hazard?",
                    (
                        opt("A purely natural event with no human involvement"),
                        opt(
                            "A failure of a human-made system, often cascading from a "
                            "natural trigger - like a flood rupturing a chemical tank",
                            correct=True,
                        ),
                        opt("A software bug in a weather model"),
                        opt("A hazard that only affects technology companies"),
                    ),
                    "Na-tech = natural-hazard-triggered technological accidents; spills, "
                    "explosions and dam breaches belong here.",
                ),
                q(
                    "With P(event)=0.02/yr, R$20M at risk and a 0.30 damage fraction, "
                    "what is the expected annual loss?",
                    (
                        opt("R$ 600,000"),
                        opt("R$ 120,000", correct=True),
                        opt("R$ 20,000,000"),
                        opt("R$ 6,000"),
                    ),
                    "0.02 x 20,000,000 x 0.30 = R$ 120,000 - the annualised risk cost.",
                ),
            ),
        ),
        # -- 2. Floods and flood risk ----------------------------------
        _t(
            "Floods and flood risk",
            "11 min",
            """# Floods and flood risk

A **flood** is water covering land that is normally dry. The common types
are **riverine** (a river overtops its banks after heavy or prolonged
rain), **flash** (intense rain on steep or urban catchments, minutes to
hours), and **coastal** (storm surge and high tides). Urbanisation makes
all of them worse: paving replaces soil, so rain that once soaked in now
runs off fast.

Flood hazard is described statistically by the **return period** - the
average interval between floods of a given size. Its inverse is the
annual exceedance probability:

```text
Return period and exceedance probability
  T  = return period in years
  P  = annual exceedance probability = 1 / T
  A "100-year flood" has T=100, so P = 0.01 (1 percent chance each year)

Rational method for a design peak flow (small catchments):
  Q = C x i x A / 360      (Q in m3/s, i in mm/h, A in hectares)
  C = runoff coefficient (0.10 grass ... 0.95 asphalt)

  Example:  C = 0.80 (urban), i = 60 mm/h, A = 50 ha
  Q = 0.80 x 60 x 50 / 360 = 6.7 m3/s
```

The runoff coefficient C is why cities flood: raising C from 0.3 to 0.8
more than doubles the peak flow for the same rain.

Management combines **structural** measures (levees, detention basins,
restored floodplains that store water) and **non-structural** ones
(flood-hazard maps, zoning that keeps building out of the floodway, and
warning systems). Tools like **HEC-RAS** and **SWMM** simulate how a flood
wave spreads so engineers can size defences and draw hazard maps.

```mermaid
graph TD
    RAIN["Heavy or prolonged rain"] --> RUNOFF["Fast urban runoff"]
    RUNOFF --> RISE["River or drainage rises"]
    RISE --> MAP["Flood hazard mapping"]
    MAP --> STRUCT["Levees and detention basins"]
    MAP --> NONSTRUCT["Zoning and warnings"]
    STRUCT --> RISK["Reduced flood risk"]
    NONSTRUCT --> RISK
```

Remember: a "100-year flood" is a probability, not a schedule - two can
strike in consecutive years. Design to a return period, but plan for the
flood that exceeds it.
""",
        ),
        quiz_lesson(
            "Quiz: Floods and flood risk",
            (
                q(
                    "What is the annual exceedance probability of a 100-year flood?",
                    (
                        opt("100 percent - it happens every year"),
                        opt("1 percent in any given year (P = 1/T)", correct=True),
                        opt("It cannot happen twice in a century"),
                        opt("50 percent"),
                    ),
                    "P = 1/T = 1/100 = 0.01; the return period is a long-run average, "
                    "not a fixed calendar.",
                ),
                q(
                    "Why does urbanisation increase flood peaks?",
                    (
                        opt("Cities attract more rain"),
                        opt(
                            "Paving raises the runoff coefficient - rain runs off fast "
                            "instead of soaking in, increasing peak flow",
                            correct=True,
                        ),
                        opt("Rivers move faster in cities by law"),
                        opt("It does not - cities flood less"),
                    ),
                    "In Q = C x i x A / 360, a higher C directly scales up the peak "
                    "discharge for the same rainfall.",
                ),
                q(
                    "Which is a NON-structural flood measure?",
                    (
                        opt("A concrete levee"),
                        opt("A detention basin"),
                        opt(
                            "Flood-hazard mapping and zoning that keeps building out of "
                            "the floodway",
                            correct=True,
                        ),
                        opt("A floodwall"),
                    ),
                    "Non-structural measures manage exposure through planning and "
                    "warnings rather than concrete.",
                ),
            ),
        ),
        # -- 3. Landslides and mass movements --------------------------
        _t(
            "Landslides and mass movements",
            "11 min",
            """# Landslides and mass movements

A **landslide** is the downslope movement of soil or rock under gravity.
Types include slow **creep**, rotational **slumps**, fast **debris
flows**, and **rockfalls**. In Brazil, the deadly events are usually
rainfall-triggered debris flows on steep, deforested slopes - the 2011
Serrana region disaster in Rio de Janeiro killed over 900 people.

Stability is judged by the **factor of safety (FS)** - the ratio of the
forces resisting sliding to the forces driving it:

```text
Factor of Safety on a slope
  FS = resisting forces / driving forces
  FS > 1  stable      FS = 1  on the point of failure      FS < 1  fails

Infinite-slope model (shallow soil layer, slope angle beta):
  FS = (c' + (gamma - m x gamma_w) x z x cos^2(beta) x tan(phi'))
       / (gamma x z x sin(beta) x cos(beta))

  c'    = effective cohesion        phi' = effective friction angle
  gamma = soil unit weight          z    = depth to slip surface
  m     = fraction of z that is saturated   gamma_w = water unit weight
```

The key insight is in the term `m x gamma_w`: as rain saturates the soil,
**pore-water pressure** rises, which cuts the effective normal stress and
therefore the resisting friction. That is why slopes fail *during and
just after* intense rain - water does not add much weight, but it
strongly reduces strength.

Controls follow directly: **drainage** to keep pore pressure down,
**retaining walls** and soil nails to add resistance, **re-vegetation** to
bind shallow soil, and **hazard zoning** to keep housing off the most
unstable slopes. Rainfall-threshold **early warning** buys time to
evacuate.

```mermaid
graph TD
    RAIN["Intense rainfall"] --> PORE["Pore pressure rises"]
    PORE --> STR["Effective strength drops"]
    STR --> FS["Factor of safety below one"]
    FS --> SLIDE["Slope fails"]
    DRAIN["Drainage and re-vegetation"] --> PORE
    WALL["Retaining structures"] --> FS
```

Remember: on a slope, water is dangerous less for its weight than for the
**pore pressure** it creates - manage the water and you manage most of the
landslide risk.
""",
        ),
        quiz_lesson(
            "Quiz: Landslides and mass movements",
            (
                q(
                    "What does a factor of safety below 1 mean for a slope?",
                    (
                        opt("The slope is extra safe"),
                        opt(
                            "Driving forces exceed resisting forces - the slope fails",
                            correct=True,
                        ),
                        opt("The slope is exactly 1 metre high"),
                        opt("Nothing - FS is only about cost"),
                    ),
                    "FS = resisting/driving; FS < 1 means the driving forces win and the "
                    "slope moves.",
                ),
                q(
                    "Why do rainfall-triggered slides usually fail during or just after "
                    "heavy rain?",
                    (
                        opt("The added weight of the water pushes the slope down"),
                        opt(
                            "Rising pore-water pressure reduces effective stress and "
                            "frictional strength, dropping the factor of safety",
                            correct=True,
                        ),
                        opt("Rain makes the rock heavier than steel"),
                        opt("Lightning weakens the soil"),
                    ),
                    "Water's main effect is pore pressure, which cuts strength - not the "
                    "small extra weight it adds.",
                ),
                q(
                    "Which control most directly targets the pore-pressure cause of "
                    "shallow slides?",
                    (
                        opt("Painting the slope"),
                        opt("Adding heavy rock on top"),
                        opt("Sub-surface drainage to keep pore pressure low", correct=True),
                        opt("Building houses higher up the slope"),
                    ),
                    "Drainage removes the water driving pore pressure; walls and "
                    "vegetation help too but address it less directly.",
                ),
            ),
        ),
        # -- 4. Droughts and wildfires ---------------------------------
        _t(
            "Droughts and wildfires",
            "11 min",
            """# Droughts and wildfires

**Droughts** are slow-onset disasters: a prolonged deficit of water that
creeps in over months. They come in linked stages - **meteorological**
(rainfall below normal), **agricultural** (soil moisture too low for
crops), **hydrological** (rivers and reservoirs fall), and
**socioeconomic** (water supply and economy suffer). Because they arrive
slowly and end slowly, droughts are easy to underestimate and hard to
declare over.

A common index is the **Standardized Precipitation Index (SPI)**, which
expresses rainfall as standard deviations from the local long-term mean:

```python
# Standardized Precipitation Index (simplified, normal approximation)
def spi(precip_mm, mean_mm, std_mm):
    return (precip_mm - mean_mm) / std_mm

# Example: a station whose 3-month normal is 300 mm (std 80 mm)
print(spi(140, 300, 80))   # -> -2.0  (extreme drought)

# SPI interpretation:
#   0 to -0.99   mild        -1.0 to -1.49  moderate
#  -1.5 to -1.99 severe       <= -2.0       extreme drought
```

Drought and **wildfire** are tightly coupled: drought dries the fuel, and
fire behaviour is driven by the **fire triangle** - fuel, oxygen, and
heat - amplified by weather and terrain. Fire spreads faster **uphill**
(flames preheat the slope above) and with wind and low humidity. In
Brazil the concern is acute in the Cerrado, Amazon edges, and the
Pantanal, where most ignitions are human and drought years turn them into
megafires.

Management spans **prevention** (fuel breaks, controlled/prescribed
burns, restricting ignition on high-danger days), **monitoring** (INPE
satellite hotspot detection, fire-danger indices), and **response**
(brigades and coordinated suppression).

```mermaid
graph TD
    DEFICIT["Rainfall deficit"] --> METE["Meteorological drought"]
    METE --> AGRI["Agricultural drought"]
    AGRI --> HYDRO["Hydrological drought"]
    HYDRO --> DRYFUEL["Vegetation dries out"]
    DRYFUEL --> FIRE["Wildfire ignites and spreads"]
    FIRE --> RESP["Detection and suppression"]
```

Remember: drought sets the stage and dry fuel is the ammunition - manage
water stress and fuel load early, because once a megafire runs under
drought conditions, suppression alone rarely wins.
""",
        ),
        quiz_lesson(
            "Quiz: Droughts and wildfires",
            (
                q(
                    "Why are droughts described as 'slow-onset' disasters?",
                    (
                        opt("They only happen at night"),
                        opt(
                            "They build over months through meteorological, "
                            "agricultural and hydrological stages, and end slowly",
                            correct=True,
                        ),
                        opt("They are caused by slow rivers"),
                        opt("They are never actually harmful"),
                    ),
                    "The creeping, multi-stage nature makes droughts easy to "
                    "underestimate and hard to declare over.",
                ),
                q(
                    "An SPI value of -2.0 indicates what?",
                    (
                        opt("Extreme drought - rainfall 2 std below the mean", correct=True),
                        opt("A very wet period"),
                        opt("Exactly average rainfall"),
                        opt("A flood warning"),
                    ),
                    "SPI = (precip - mean)/std; -2.0 or below is classified as extreme drought.",
                ),
                q(
                    "According to fire behaviour, a wildfire generally spreads fastest…",
                    (
                        opt("downhill, away from the wind"),
                        opt("uphill, because flames preheat the fuel above", correct=True),
                        opt("only on flat ground"),
                        opt("in high humidity"),
                    ),
                    "Upslope spread plus wind and low humidity accelerate fire; the fire "
                    "triangle (fuel, oxygen, heat) sets the base conditions.",
                ),
            ),
        ),
        # -- 5. Industrial accidents and spills ------------------------
        _t(
            "Industrial accidents and spills",
            "11 min",
            """# Industrial accidents and spills

Industry stores and moves large quantities of hazardous material - fuels,
solvents, acids, pesticides. A **spill** or release turns that into an
environmental disaster: contaminated rivers and soil, toxic air, fish
kills. Releases reach the environment through three main pathways -
**water** (a river carries a slug of pollutant downstream), **soil and
groundwater** (infiltration to aquifers), and **air** (a toxic or
flammable gas cloud).

The first quantitative step is the **source term** - how much is released,
how fast. For a puncture in a tank, an orifice model estimates the leak:

```text
Liquid leak rate through a hole (Torricelli / Bernoulli)
  Q = Cd x A x sqrt(2 x g x h)

  Cd = discharge coefficient (~0.61 sharp orifice)
  A  = hole area (m2)     g = 9.81 m/s2     h = liquid head above hole (m)

  Example: A = 0.001 m2, h = 4 m
  Q = 0.61 x 0.001 x sqrt(2 x 9.81 x 4)
    = 0.61 x 0.001 x 8.86 = 0.0054 m3/s  (about 5.4 L/s)
```

For an airborne toxic release, the **Gaussian plume model** predicts
downwind concentration; for a river spill, an advection-dispersion model
predicts how the peak concentration attenuates as it travels. These tell
responders where the hazard is heading and how long until it arrives.

Prevention and response are layered: **secondary containment** (bunds or
dikes sized to hold the largest tank plus rainfall), **spill kits and
booms**, and formal emergency plans. In Brazil this is governed by
**CONAMA** resolutions and licensing; a facility's **PEI** (individual
emergency plan) is mandatory for oil-handling sites.

```mermaid
graph TD
    RELEASE["Hazardous release"] --> SOURCE["Estimate source term"]
    SOURCE --> WATER["Water pathway"]
    SOURCE --> SOIL["Soil and groundwater pathway"]
    SOURCE --> AIR["Air pathway plume"]
    WATER --> CONTAIN["Booms and containment"]
    AIR --> EVAC["Downwind evacuation"]
    SOIL --> REMED["Remediation"]
```

Remember: response starts with the **source term** - you cannot predict
where a spill goes or protect people downstream until you know how much is
escaping and how fast.
""",
        ),
        quiz_lesson(
            "Quiz: Industrial accidents and spills",
            (
                q(
                    "What is the 'source term' in a spill assessment?",
                    (
                        opt("The name of the responsible company"),
                        opt(
                            "How much hazardous material is released and how fast - the "
                            "starting point for predicting spread",
                            correct=True,
                        ),
                        opt("The cost of the cleanup"),
                        opt("The colour of the chemical"),
                    ),
                    "Without the release rate and quantity you cannot model where the "
                    "hazard goes or who is downstream/downwind.",
                ),
                q(
                    "In the orifice leak model Q = Cd x A x sqrt(2 x g x h), what raises "
                    "the leak rate?",
                    (
                        opt("A smaller hole"),
                        opt(
                            "A larger hole area or a greater liquid head above the hole",
                            correct=True,
                        ),
                        opt("Lower gravity"),
                        opt("A colder day only"),
                    ),
                    "Q scales with hole area A and with the square root of head h - a "
                    "fuller tank and a bigger hole both leak faster.",
                ),
                q(
                    "What is the purpose of secondary containment (a bund) around a tank?",
                    (
                        opt("Decoration"),
                        opt(
                            "To hold the largest tank's contents plus rainfall if the "
                            "tank fails, stopping the spill from spreading",
                            correct=True,
                        ),
                        opt("To increase storage capacity"),
                        opt("To keep the tank warm"),
                    ),
                    "A bund is a passive barrier sized for the worst single failure plus "
                    "rain - a core CONAMA/licensing requirement.",
                ),
            ),
        ),
        # -- 6. Dam and tailings failures ------------------------------
        _t(
            "Dam and tailings failures",
            "11 min",
            """# Dam and tailings failures

Dams store enormous potential energy. When one fails, that energy
releases almost instantly as a **flood wave**. **Tailings dams** - which
hold mining waste as a slurry - are especially dangerous: the released
material is a dense, fast mud that behaves like a debris flow. Brazil
learned this at catastrophic cost in **Mariana (Fundao, 2015)** and
**Brumadinho (2019)**, where a tailings-dam collapse killed 270 people in
minutes.

Failure modes include **overtopping** (flood exceeds spillway),
**internal erosion / piping** (seepage washes out fines), and, for
tailings, **static liquefaction** (loose saturated tailings suddenly lose
strength and flow). A first estimate of the outflow uses a peak-breach
relation:

```text
Peak breach discharge (regression on dam-break case history)
  Qp = 0.0039 x V ^ 0.8122     (Qp in m3/s, V = reservoir volume in m3)
                                (Froehlich-type empirical form)

  Example: V = 12,000,000 m3
  Qp = 0.0039 x 12,000,000 ^ 0.8122
     = 0.0039 x 5.0e5 (approx) = about 1,960 m3/s peak outflow

Arrival time of the wave (very rough):
  t = distance / wave celerity,  celerity c ~ sqrt(g x depth)
  10 km downstream, wave depth ~4 m:  c ~ sqrt(9.81 x 4) ~ 6.3 m/s
  t ~ 10,000 / 6.3 ~ 1,600 s ~ 27 minutes
```

Those numbers explain why **downstream warning time is measured in
minutes**, and why siting people below a tailings dam is so hazardous.

Management is now heavily regulated. Brazil's **ANM** and law after
Brumadinho ban the riskiest **upstream** construction method, require a
**dam-break study**, a mapped **self-rescue zone (ZAS)**, sirens, and an
emergency action plan (**PAEBM**). Engineering controls include proper
drainage, monitored pore pressure, and buttressing.

```mermaid
graph TD
    TRIGGER["Overtopping or liquefaction"] --> BREACH["Dam breach"]
    BREACH --> WAVE["Flood or mud wave"]
    WAVE --> ZAS["Self rescue zone downstream"]
    STUDY["Dam break study"] --> MAP["Inundation map"]
    MAP --> SIREN["Sirens and evacuation plan"]
    ZAS --> SIREN
```

Remember: for a dam, the study, the inundation map, and the siren chain
exist because the wave can arrive in **minutes** - preparedness downstream
matters as much as the structure itself.
""",
        ),
        quiz_lesson(
            "Quiz: Dam and tailings failures",
            (
                q(
                    "Why are tailings-dam failures often deadlier than water-dam floods?",
                    (
                        opt("Tailings dams are always taller"),
                        opt(
                            "The released material is a dense, fast mud that behaves like "
                            "a debris flow, and can liquefy suddenly",
                            correct=True,
                        ),
                        opt("Tailings are lighter than water"),
                        opt("They only fail in winter"),
                    ),
                    "Static liquefaction turns loose saturated tailings into a fast, "
                    "heavy flow - as at Mariana and Brumadinho.",
                ),
                q(
                    "The peak-breach and wave-arrival calculations mainly show that…",
                    (
                        opt("downstream warning time is often only minutes", correct=True),
                        opt("dams never really fail"),
                        opt("the wave takes days to arrive"),
                        opt("volume has no effect on outflow"),
                    ),
                    "A wave travelling ~6 m/s covers 10 km in under half an hour - hence "
                    "sirens and pre-mapped self-rescue zones.",
                ),
                q(
                    "What did Brazil require of tailings dams after Brumadinho?",
                    (
                        opt("Nothing changed"),
                        opt(
                            "Banning the riskiest upstream method and requiring dam-break "
                            "studies, mapped self-rescue zones, sirens and emergency plans",
                            correct=True,
                        ),
                        opt("Only a coat of paint"),
                        opt("Building homes closer to save land"),
                    ),
                    "ANM regulation now mandates the PAEBM, the ZAS self-rescue zone, and "
                    "phase-out of upstream dams.",
                ),
            ),
        ),
        # -- 7. Early warning and emergency planning -------------------
        _t(
            "Early warning and emergency planning",
            "11 min",
            """# Early warning and emergency planning

A hazard forecast only saves lives if it reaches the right people in time
to act. A **people-centred early warning system (EWS)** has **four
linked elements** - and it is only as strong as its weakest link:

1. **Risk knowledge** - who and what is exposed, and where.
2. **Monitoring and forecasting** - sensors, radar, and models that detect
   the hazard building (rain gauges, river levels, tailings pore-pressure,
   satellite hotspots).
3. **Warning dissemination** - getting an actionable message to people
   (sirens, SMS/cell broadcast, radio) with clear instructions.
4. **Response capability** - people who *know what to do* and can do it -
   rehearsed evacuation routes, shelters, drills.

A famous failure mode: a perfect forecast that never reaches households,
or reaches them with no rehearsed action, saves no one. In Brazil,
**CEMADEN** monitors and forecasts, while **Defesa Civil** issues alerts
and runs the local response.

Warnings need a **lead time** longer than the time people need to reach
safety:

```text
Effective warning condition
  Lead time  >=  Detection delay + Dissemination delay + Response time

  Example (debris flow):
    Forecast issued 40 min before impact           lead time = 40 min
    Detection + processing                          = 5 min
    Alert dissemination (siren + SMS)               = 5 min
    Households evacuate to high ground              = 25 min
    Slack = 40 - (5 + 5 + 25) = 5 min  ->  people reach safety in time
```

Planning turns this into documents and muscle memory: a **contingency
plan** per hazard, mapped **evacuation routes** and shelters, defined
**alert levels** (observation -> attention -> alert -> maximum), and
regular **community drills**. The **Sendai Framework's** Target G is
explicitly to expand multi-hazard early warning coverage.

```mermaid
graph LR
    KNOW["Risk knowledge"] --> MON["Monitoring and forecast"]
    MON --> DISS["Warning dissemination"]
    DISS --> RESP["Response capability"]
    RESP --> SAFE["People reach safety"]
    DRILL["Community drills"] --> RESP
```

Remember: an early warning system is a chain of four links - risk
knowledge, monitoring, dissemination, and rehearsed response - and it
fails at its weakest link, which is usually the last-mile human one.
""",
        ),
        quiz_lesson(
            "Quiz: Early warning and emergency planning",
            (
                q(
                    "What are the four elements of a people-centred early warning system?",
                    (
                        opt("Sirens, radios, phones, and TVs"),
                        opt(
                            "Risk knowledge, monitoring and forecasting, warning "
                            "dissemination, and response capability",
                            correct=True,
                        ),
                        opt("Prevention, response, recovery, and funding"),
                        opt("Rain, rivers, slopes, and dams"),
                    ),
                    "The four linked elements form a chain; the system is only as strong "
                    "as its weakest link.",
                ),
                q(
                    "A perfect forecast that never reaches households demonstrates that…",
                    (
                        opt("forecasting is the only thing that matters"),
                        opt(
                            "the system fails at its weakest link - here, dissemination "
                            "and response, not the science",
                            correct=True,
                        ),
                        opt("early warning systems are pointless"),
                        opt("sirens are never needed"),
                    ),
                    "The last-mile human links (getting the message out and rehearsed "
                    "action) are the common point of failure.",
                ),
                q(
                    "For a warning to be effective, the lead time must exceed…",
                    (
                        opt("the cost of the sirens"),
                        opt(
                            "the sum of detection delay, dissemination delay and the time "
                            "people need to reach safety",
                            correct=True,
                        ),
                        opt("one full day, always"),
                        opt("the height of the dam"),
                    ),
                    "Lead time >= detection + dissemination + response time, or people "
                    "cannot get clear in time.",
                ),
            ),
        ),
        # -- 8. Resilient reconstruction and continuity ----------------
        _t(
            "Resilient reconstruction and continuity",
            "11 min",
            """# Resilient reconstruction and continuity

After the emergency comes **recovery** - and the central principle,
enshrined in the **Sendai Framework**, is **Build Back Better (BBB)**.
Reconstruction is a rare window to reduce future risk: rebuild to a higher
standard, relocate the most exposed, and restore the natural buffers
(mangroves, floodplains, forested slopes) that blunt the next event.
Rebuilding identical, exposed structures simply resets the clock to the
next disaster.

**Resilience** is the system's ability to absorb a shock, keep essential
functions, and recover quickly. It is measured, roughly, as the area lost
under a performance-over-time curve:

```python
# Resilience as retained performance over the disruption period
# Q(t) = system functionality (1.0 = normal). Resilience R in [0,1].
def resilience(functionality, times):
    # trapezoidal area under Q(t) divided by the ideal (full) area
    total = 0.0
    for i in range(1, len(times)):
        dt = times[i] - times[i - 1]
        total += 0.5 * (functionality[i] + functionality[i - 1]) * dt
    span = times[-1] - times[0]
    return total / span                 # 1.0 = no loss; lower = deeper/longer dip

# Shallower drop and faster recovery -> higher R
print(resilience([1.0, 0.3, 0.6, 1.0], [0, 1, 3, 6]))   # ~0.66
```

Two levers raise R: **reduce the depth of the drop** (robustness -
stronger buildings, redundancy) and **shorten the recovery** (rapid
restoration - stockpiles, mutual-aid agreements, pre-arranged funding and
contracts).

Organisations formalise the recovery side as a **Business Continuity Plan
(BCP)**, built around two targets: the **RTO** (recovery time objective -
how fast a function must be back) and **RPO** (recovery point objective -
how much data/state loss is tolerable). **ISO 22301** is the continuity
standard; **ISO 14001** keeps environmental management improving after the
event.

```mermaid
graph LR
    EVENT["Disaster event"] --> DROP["Functionality drops"]
    DROP --> RECOVER["Recovery over time"]
    RECOVER --> BBB["Build back better"]
    BBB --> ROBUST["More robust and less exposed"]
    ROBUST --> NEXT["Lower loss next time"]
    NEXT --> DROP
```

Remember: resilience is set by two things - how far you fall and how fast
you get back up. Reconstruction that only restores the old, exposed
system wastes the one chance to lower both.
""",
        ),
        quiz_lesson(
            "Quiz: Resilient reconstruction and continuity",
            (
                q(
                    "What does 'Build Back Better' mean in recovery?",
                    (
                        opt("Rebuild exactly what existed, as fast as possible"),
                        opt(
                            "Use reconstruction to reduce future risk - higher standards, "
                            "relocating the most exposed, restoring natural buffers",
                            correct=True,
                        ),
                        opt("Never rebuild anything"),
                        opt("Build only bigger, more expensive structures"),
                    ),
                    "Rebuilding identical, exposed structures just resets the clock; BBB "
                    "lowers vulnerability and exposure while you rebuild.",
                ),
                q(
                    "Resilience is raised by which two levers?",
                    (
                        opt("Painting and landscaping"),
                        opt(
                            "Reducing the depth of the functionality drop (robustness) "
                            "and shortening the recovery time",
                            correct=True,
                        ),
                        opt("Ignoring the event and hoping"),
                        opt("Only buying more insurance"),
                    ),
                    "A shallower dip and a faster bounce-back both increase the area "
                    "under the performance curve.",
                ),
                q(
                    "In a Business Continuity Plan, what is the RTO?",
                    (
                        opt("The cost of the disaster"),
                        opt(
                            "The recovery time objective - how quickly a function must be "
                            "restored after disruption",
                            correct=True,
                        ),
                        opt("The number of employees"),
                        opt("The rainfall total"),
                    ),
                    "RTO = how fast a function must be back; RPO = how much data/state "
                    "loss is tolerable. ISO 22301 governs continuity.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the standard disaster risk relation?",
                    (
                        opt("Risk = Cost + Time"),
                        opt(
                            "Risk = Hazard x Exposure x Vulnerability",
                            correct=True,
                        ),
                        opt("Risk = Rain x Wind"),
                        opt("Risk = Prevention + Recovery"),
                    ),
                    "Reduce any factor - hazard, exposure or vulnerability - and you "
                    "reduce risk; capacity lowers vulnerability.",
                ),
                q(
                    "A '50-year flood' has what annual chance of being equalled or exceeded?",
                    (
                        opt("50 percent"),
                        opt("2 percent (P = 1/T = 1/50)", correct=True),
                        opt("It happens exactly once every 50 years"),
                        opt("0 percent until year 50"),
                    ),
                    "P = 1/T; the return period is a long-run average, so two can fall "
                    "in successive years.",
                ),
                q(
                    "During heavy rain, what most reduces a slope's factor of safety?",
                    (
                        opt("The weight of the rainwater added on top"),
                        opt(
                            "Rising pore-water pressure cutting effective stress and "
                            "frictional strength",
                            correct=True,
                        ),
                        opt("Cooler air temperature"),
                        opt("Sunlight on the slope"),
                    ),
                    "Water's dominant effect on stability is pore pressure, not its "
                    "modest added weight.",
                ),
                q(
                    "An SPI of -1.7 corresponds to which drought category?",
                    (
                        opt("Wet conditions"),
                        opt("Severe drought", correct=True),
                        opt("Extreme drought"),
                        opt("Normal"),
                    ),
                    "SPI -1.5 to -1.99 is severe; -2.0 and below is extreme.",
                ),
                q(
                    "In a chemical spill, why compute the source term first?",
                    (
                        opt("To assign blame"),
                        opt(
                            "The release rate and quantity drive every downstream or "
                            "downwind prediction of where the hazard goes",
                            correct=True,
                        ),
                        opt("It sets the cleanup invoice"),
                        opt("It is only paperwork"),
                    ),
                    "No source term means no plume, no travel time, no protective "
                    "action for people downstream.",
                ),
                q(
                    "Which failure mode is specific to loose, saturated tailings?",
                    (
                        opt("Overtopping only"),
                        opt("Static liquefaction - sudden loss of strength and flow", correct=True),
                        opt("Freezing solid"),
                        opt("Evaporation"),
                    ),
                    "Liquefaction turned Brumadinho's tailings into a fast mud wave that "
                    "arrived in minutes.",
                ),
                q(
                    "What are the four elements of a people-centred early warning system?",
                    (
                        opt("Radar, siren, radio, TV"),
                        opt(
                            "Risk knowledge, monitoring and forecasting, warning "
                            "dissemination, response capability",
                            correct=True,
                        ),
                        opt("Rain, river, road, roof"),
                        opt("Plan, build, test, deploy"),
                    ),
                    "The system fails at its weakest link, usually the last-mile "
                    "dissemination and rehearsed response.",
                ),
                q(
                    "For a warning to save lives, the lead time must be greater than…",
                    (
                        opt("the value of the property at risk"),
                        opt(
                            "detection delay + dissemination delay + the time people need "
                            "to reach safety",
                            correct=True,
                        ),
                        opt("the height of the nearest hill"),
                        opt("the rainfall depth in millimetres"),
                    ),
                    "If any of those delays eats the lead time, people cannot get clear "
                    "before impact.",
                ),
                q(
                    "What does 'Build Back Better' aim to achieve in reconstruction?",
                    (
                        opt("Restore the old, exposed system as-is"),
                        opt(
                            "Use the rebuild to lower future exposure and vulnerability - "
                            "higher standards, relocation, restored natural buffers",
                            correct=True,
                        ),
                        opt("Delay all rebuilding indefinitely"),
                        opt("Maximise construction cost"),
                    ),
                    "Reconstruction is the rare chance to reduce risk instead of "
                    "resetting the clock to the next disaster.",
                ),
                q(
                    "Which two levers most directly increase a system's resilience?",
                    (
                        opt("More meetings and more reports"),
                        opt(
                            "Reducing the depth of the functionality drop (robustness) "
                            "and shortening the recovery time",
                            correct=True,
                        ),
                        opt("Ignoring monitoring and drills"),
                        opt("Building only on floodplains"),
                    ),
                    "A shallower dip and a faster bounce-back both raise the retained "
                    "performance over the disruption.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

DISASTER_RISK_RESILIENCE_COURSES: tuple[SeedCourse, ...] = (_DISASTER_RISK_RESILIENCE,)
