"""Academy seed content - Ecological Engineering and Restoration.

An intermediate course on repairing damaged ecosystems using ecological
engineering. It moves from principles and degraded-land assessment
through revegetation, erosion control and soil bioengineering, constructed
wetlands, river and stream restoration, ecological corridors and offsets,
and finally monitoring restoration success. Every lesson is a direct
explanation with a mermaid diagram and a worked design, formula or
calculation, followed by a checkpoint quiz; the course closes with a
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


_ECOLOGICAL_RESTORATION = SeedCourse(
    slug="ecological-restoration",
    title="Ecological Engineering & Restoration",
    description=(
        "Repairing damaged ecosystems: degraded land assessment, revegetation "
        "and erosion control, constructed wetlands, river restoration and "
        "nature-based solutions. Each lesson grounds the practice in real "
        "standards (SER, CONAMA, ABNT NBR, EPA, IUCN) with a worked design "
        "equation or calculation and a diagram, then a checkpoint quiz."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Ecological Engineering and Restoration

Ecosystems get damaged - by mining, farming, deforestation, channelized
rivers, pollution and sprawl. **Ecological engineering** designs
interventions that work *with* natural processes to repair them, and
**ecological restoration** is the practice of assisting the recovery of an
ecosystem that has been degraded, damaged or destroyed (the SER
definition). This course teaches how to assess damage and design
restoration that actually recovers function, not just green cover.

The approach is **concrete and quantitative**: every lesson explains one
idea directly, draws it as a diagram, and works one real design equation
or calculation (a soil-loss estimate, a wetland sizing, a planting
density, a survival rate). After each lesson there is a short quiz; at the
end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **Principles of ecological engineering** - self-design, reference
   ecosystems, working with succession
2. **Degraded land assessment** - baselines, indicators, reference sites
3. **Revegetation and reforestation** - species, densities, nucleation
4. **Erosion control and soil bioengineering** - RUSLE, live structures
5. **Constructed wetlands** - treating water with designed ecosystems
6. **River and stream restoration** - reconnecting channel and floodplain
7. **Ecological corridors and offsets** - connectivity and no-net-loss
8. **Monitoring restoration success** - indicators, targets, adaptive
   management

Restoration is never a single planting event - it is a designed
trajectory checked against a reference and adjusted over years. Keep that
frame and every technique below fits together.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is ecological restoration, in the SER sense?",
                    (
                        opt("Planting any fast-growing trees to make land green"),
                        opt("Building concrete structures to replace an ecosystem"),
                        opt(
                            "Assisting the recovery of an ecosystem that has been "
                            "degraded, damaged or destroyed, toward a reference state",
                            correct=True,
                        ),
                        opt("Fencing land off and never touching it"),
                    ),
                    "Restoration assists recovery of ecosystem structure and function, "
                    "measured against a reference - not just adding green cover.",
                ),
                q(
                    "How is each lesson in this course structured?",
                    (
                        opt("Pure theory with no numbers"),
                        opt(
                            "A direct explanation, a diagram, and a worked design "
                            "equation or calculation, followed by a checkpoint quiz",
                            correct=True,
                        ),
                        opt("Only a video with no text"),
                        opt("A list of species names to memorize"),
                    ),
                    "Every lesson pairs a clear explanation with a mermaid diagram and "
                    "one concrete worked example, then a short quiz.",
                ),
            ),
        ),
        # -- 1. Principles ---------------------------------------------
        _t(
            "Principles of ecological engineering",
            "10 min",
            """# Principles of ecological engineering

**Ecological engineering** is the design of sustainable ecosystems that
integrate human society with the natural environment for the benefit of
both. The central idea, from H.T. Odum and W. Mitsch, is **self-design**:
rather than fully specifying every component, you set the right conditions
(hydrology, soil, a seed source) and let nature select and organize the
species that fit. You steer succession instead of fighting it.

Some guiding principles:

- **Work with succession, not against it.** Early "pioneer" species
  stabilize and enrich the site, creating conditions for later species.
  Design the starting point, not the endpoint.
- **Use a reference ecosystem.** A comparable healthy site (or historical
  data) defines the target composition, structure and function. Without a
  reference you cannot say what "restored" means.
- **Match energy signature and site.** Native species adapted to the local
  climate, soils and hydrology need less maintenance and subsidy.
- **Design for resilience and self-maintenance.** The goal is a system
  that persists without permanent human inputs.

The **SER restorative continuum** frames the options: from reducing
impacts, through **rehabilitation** (recovering function) and
**reclamation** (making degraded land usable again), up to full
**restoration** toward a reference ecosystem.

```mermaid
graph LR
    DIST["Disturbed site"] --> COND["Set starting conditions"]
    COND --> PIONEER["Pioneer species colonize"]
    PIONEER --> BUILD["Soil and habitat build"]
    BUILD --> LATE["Later successional species"]
    LATE --> REF["Approach reference ecosystem"]
    REF --> SELF["Self maintaining system"]
```

A simple way to place a project on the continuum by ecosystem condition:

```text
Restorative continuum (target ecosystem attributes recovered):

  Reduce impacts        : stop ongoing degradation, no recovery target
  Remediation           : remove contaminants
  Reclamation           : stabilize, restore basic use and cover
  Rehabilitation        : recover key functions and services
  Full restoration      : structure AND function approach reference

Rule of thumb:
  set condition, let self-design work, measure against a reference.
```

Remember: you design the *conditions and trajectory*, and let the
ecosystem self-organize toward a reference you defined in advance.
""",
        ),
        quiz_lesson(
            "Quiz: Principles of ecological engineering",
            (
                q(
                    "What does 'self-design' mean in ecological engineering?",
                    (
                        opt("The engineer specifies every species and its position"),
                        opt(
                            "You set the right conditions and let nature select and "
                            "organize the species that fit",
                            correct=True,
                        ),
                        opt("The ecosystem is left entirely alone with no intervention"),
                        opt("Software designs the ecosystem automatically"),
                    ),
                    "Self-design (Odum, Mitsch): create conditions and a seed source, "
                    "and let succession and selection do the organizing.",
                ),
                q(
                    "Why is a reference ecosystem important?",
                    (
                        opt("It is a legal requirement with no technical use"),
                        opt(
                            "It defines the target composition, structure and function - "
                            "without it you cannot say what 'restored' means",
                            correct=True,
                        ),
                        opt("It tells you which pesticides to apply"),
                        opt("It sets the market price of the land"),
                    ),
                    "A comparable healthy site or historical data provides the target "
                    "and the yardstick for success.",
                ),
                q(
                    "On the SER restorative continuum, how does rehabilitation differ "
                    "from full restoration?",
                    (
                        opt("They are identical terms"),
                        opt(
                            "Rehabilitation recovers key functions and services; full "
                            "restoration returns both structure and function toward a "
                            "reference ecosystem",
                            correct=True,
                        ),
                        opt("Rehabilitation always uses non-native species only"),
                        opt("Full restoration ignores the reference ecosystem"),
                    ),
                    "The continuum runs from reducing impacts through reclamation and "
                    "rehabilitation up to full restoration against a reference.",
                ),
            ),
        ),
        # -- 2. Degraded land assessment -------------------------------
        _t(
            "Degraded land assessment",
            "11 min",
            """# Degraded land assessment

Before you design anything, you diagnose the site. **Assessment**
establishes a **baseline** - the current physical, chemical and biological
condition - and compares it to a **reference** to define the restoration
gap and the limiting factors.

What to characterize:

- **Soil** - texture, pH, organic matter, bulk density (compaction),
  nutrients, salinity, and contaminants (heavy metals, hydrocarbons).
- **Hydrology** - water table, drainage, flooding regime; often the master
  variable, especially for wetlands.
- **Vegetation and seed bank** - remaining native cover, invasive species,
  whether a viable seed bank exists (natural regeneration is cheaper than
  planting when it works).
- **Landscape context** - nearby seed sources and habitat that will
  recolonize the site, and the surrounding land use.

The output is a set of **indicators** measured against reference values.
A useful, simple index compares each indicator to its reference and
averages:

```python
# Land Condition Index: 0 (degraded) .. 1 (equals reference)
def condition_index(site, reference):
    scores = []
    for key in reference:
        # cap each ratio at 1 so a site cannot "exceed" the reference
        ratio = min(site[key] / reference[key], 1.0)
        scores.append(ratio)
    return sum(scores) / len(scores)

reference = {"organic_matter_pct": 4.0, "cover_pct": 90, "species_n": 40}
site      = {"organic_matter_pct": 1.2, "cover_pct": 25, "species_n": 8}

print(round(condition_index(site, reference), 2))   # -> 0.28
```

An index near **0.28** flags a heavily degraded site: low organic matter,
sparse cover and few species - a large gap to close. Which indicator is
*worst* (here, cover and species) points to the limiting factors to
target first.

```mermaid
graph TD
    SITE["Degraded site"] --> SOIL["Soil texture pH organic matter"]
    SITE --> HYDRO["Hydrology and drainage"]
    SITE --> VEG["Vegetation and seed bank"]
    SOIL --> IND["Indicators vs reference"]
    HYDRO --> IND
    VEG --> IND
    IND --> GAP["Restoration gap and limiting factors"]
    GAP --> PLAN["Design targets the limiting factors"]
```

Remember: measure the baseline, compare to a reference, and let the
*worst-performing indicators* set your design priorities.
""",
        ),
        quiz_lesson(
            "Quiz: Degraded land assessment",
            (
                q(
                    "What is the purpose of a baseline assessment before restoration?",
                    (
                        opt("To decide the final selling price of the timber"),
                        opt(
                            "To establish current soil, hydrology and vegetation "
                            "condition and compare it to a reference, defining the gap "
                            "and limiting factors",
                            correct=True,
                        ),
                        opt("To skip the reference ecosystem entirely"),
                        opt("To plant trees as fast as possible"),
                    ),
                    "The baseline plus a reference defines the restoration gap and shows "
                    "which limiting factors to target.",
                ),
                q(
                    "Why is a site's existing seed bank worth assessing?",
                    (
                        opt("It has no effect on restoration cost"),
                        opt(
                            "A viable native seed bank can drive natural regeneration, "
                            "which is often cheaper than planting when it works",
                            correct=True,
                        ),
                        opt("Seed banks only matter for aquatic systems"),
                        opt("It tells you the soil pH directly"),
                    ),
                    "Passive regeneration from a seed bank and nearby seed sources can "
                    "restore a site at far lower cost than full planting.",
                ),
                q(
                    "In the condition index, why cap each indicator ratio at 1.0?",
                    (
                        opt("To make the code run faster"),
                        opt(
                            "So a site that exceeds the reference on one indicator cannot "
                            "mask deficits on others",
                            correct=True,
                        ),
                        opt("Because ratios above 1 are physically impossible"),
                        opt("To convert the result to a percentage"),
                    ),
                    "Capping prevents one over-performing indicator from inflating the "
                    "average and hiding the real limiting factors.",
                ),
            ),
        ),
        # -- 3. Revegetation and reforestation -------------------------
        _t(
            "Revegetation and reforestation",
            "11 min",
            """# Revegetation and reforestation

**Revegetation** re-establishes plant cover; **reforestation** re-creates
forest specifically. The design choices are *which species*, *how many per
hectare*, and *what arrangement* - all driven by the reference ecosystem
and the site's limiting factors.

Key decisions:

- **Native, locally sourced species.** Use provenances adapted to the
  site. In Brazil, restoration plantings mix successional groups -
  **pioneers** (fast, shade-intolerant) with **secondary and climax**
  species - so early cover shades out weeds while the slower canopy builds.
- **Passive vs active.** If regeneration potential is high (seed bank,
  nearby forest), assisted natural regeneration is cheapest. If the site is
  severely degraded or isolated, active planting is needed.
- **Nucleation.** Instead of planting uniformly, create dense "islands"
  (Anderson nuclei) that attract seed-dispersing birds and spread outward -
  cheaper and more self-organizing than blanket planting.

Planting density is a real design number. From a target density you get
spacing, and from area you get the number of seedlings:

```text
Spacing from density (square grid):
    spacing s = sqrt( 10000 / D )           [D = stems per hectare]

Seedlings needed:
    N = D * A                               [A = area in hectares]

Worked example - reforestation at D = 1667 stems/ha over A = 4 ha:
    s = sqrt(10000 / 1667) = sqrt(6.0) = 2.45 m   -> about 3.0 x 2.0 m grid
    N = 1667 * 4 = 6668 seedlings
    with 50 percent pioneers -> 3334 pioneer + 3334 non-pioneer seedlings
```

Brazilian restoration guidance (for example Sao Paulo state) often
requires a minimum of about **80 native species** and high initial
density (roughly 1600 to 3000 stems per hectare) to ensure diversity and
fast canopy closure.

```mermaid
graph TD
    REF["Reference forest"] --> SPEC["Choose native species"]
    SPEC --> PION["Pioneers fast cover"]
    SPEC --> SEC["Secondary and climax canopy"]
    PION --> DENS["Set density and spacing"]
    SEC --> DENS
    DENS --> ARR["Arrangement rows or nuclei"]
    ARR --> CLOSE["Canopy closure shades weeds"]
```

Remember: match species to the reference, mix successional groups for fast
cover plus long-term structure, and derive spacing and seedling counts
directly from your target density.
""",
        ),
        quiz_lesson(
            "Quiz: Revegetation and reforestation",
            (
                q(
                    "Why mix pioneer species with secondary and climax species in a "
                    "reforestation planting?",
                    (
                        opt("Pioneers are decorative only"),
                        opt(
                            "Fast pioneers give early cover that shades out weeds while "
                            "the slower secondary and climax species build long-term "
                            "canopy and structure",
                            correct=True,
                        ),
                        opt("Climax species grow fastest and need no companions"),
                        opt("Mixing groups is banned in restoration"),
                    ),
                    "Successional mixing gives quick canopy closure now and a diverse, "
                    "structured forest later.",
                ),
                q(
                    "At a target density of 1600 stems per hectare, roughly what square "
                    "spacing does s = sqrt(10000/D) give?",
                    (
                        opt("About 0.5 m"),
                        opt("About 2.5 m", correct=True),
                        opt("About 10 m"),
                        opt("About 25 m"),
                    ),
                    "sqrt(10000/1600) = sqrt(6.25) = 2.5 m, so about a 2.5 m grid.",
                ),
                q(
                    "What is nucleation in restoration planting?",
                    (
                        opt("Planting a single species across the whole site uniformly"),
                        opt(
                            "Creating dense planted islands that attract seed dispersers "
                            "and spread outward, instead of blanket planting",
                            correct=True,
                        ),
                        opt("Using nuclear energy to speed up growth"),
                        opt("Removing all vegetation before planting"),
                    ),
                    "Nuclei (Anderson islands) seed the landscape and let natural "
                    "dispersal do much of the work - cheaper and self-organizing.",
                ),
            ),
        ),
        # -- 4. Erosion control and soil bioengineering ----------------
        _t(
            "Erosion control and soil bioengineering",
            "12 min",
            """# Erosion control and soil bioengineering

Bare, disturbed soil erodes - losing the very medium plants need and
sending sediment into streams. **Erosion control** stabilizes soil while
vegetation establishes; **soil bioengineering** uses *living plant
material* (stakes, fascines, brush layers) as structural elements,
combining engineering function with ecological recovery.

To size the problem, engineers estimate soil loss with the **Revised
Universal Soil Loss Equation (RUSLE)**:

```text
RUSLE annual soil loss (tons per hectare per year):
    A = R * K * LS * C * P

    R  = rainfall erosivity        (climate)
    K  = soil erodibility          (soil type)
    LS = slope length and steepness (topography)
    C  = cover and management       (vegetation - the big lever)
    P  = support practice           (terraces, contour work)

Worked example - bare slope vs vegetated:
    R = 5000, K = 0.03, LS = 1.5, P = 1.0
    Bare soil    C = 1.0  -> A = 5000*0.03*1.5*1.0*1.0 = 225 t/ha/yr
    Grass cover  C = 0.02 -> A = 5000*0.03*1.5*0.02*1.0 = 4.5 t/ha/yr

    Cover alone cuts loss ~50x. C (vegetation) is the dominant control.
```

That result is the core lesson: **vegetation cover (the C factor) is the
strongest lever** in erosion control. Living techniques deliver it while
adding roots that reinforce the soil:

- **Live stakes and cuttings** - dormant woody cuttings driven into the
  slope; they root and bind soil.
- **Live fascines** - bundles of live branches laid in shallow trenches
  along the contour to slow runoff and trap sediment.
- **Brush layering** - live branches placed on benches across the slope,
  breaking slope length (reducing LS).
- **Erosion-control blankets and hydroseeding** - temporary cover that
  protects soil until roots take hold.

```mermaid
graph TD
    BARE["Bare disturbed slope"] --> RUSLE["Estimate loss with RUSLE"]
    RUSLE --> COVER["Add vegetation cover lowers C"]
    RUSLE --> STRUCT["Live structures reinforce soil"]
    COVER --> ROOT["Roots bind and reinforce"]
    STRUCT --> ROOT
    ROOT --> STABLE["Slope stabilized sediment trapped"]
```

Remember: quantify loss with RUSLE, then attack the biggest factors - drop
C with fast cover and cut LS with contour structures - using living
material so the fix becomes a functioning ecosystem.
""",
        ),
        quiz_lesson(
            "Quiz: Erosion control and soil bioengineering",
            (
                q(
                    "In the RUSLE equation A = R*K*LS*C*P, which factor does establishing "
                    "vegetation cover most directly reduce?",
                    (
                        opt("R, rainfall erosivity"),
                        opt("K, soil erodibility"),
                        opt("C, the cover and management factor", correct=True),
                        opt("R and K equally"),
                    ),
                    "Vegetation lowers C - the dominant, controllable lever, cutting soil "
                    "loss dramatically as the worked example showed.",
                ),
                q(
                    "What defines soil bioengineering specifically?",
                    (
                        opt("Using only concrete and steel structures"),
                        opt(
                            "Using living plant material such as live stakes, fascines "
                            "and brush layers as structural, soil-reinforcing elements",
                            correct=True,
                        ),
                        opt("Applying pesticides to bare soil"),
                        opt("Genetically modifying soil bacteria"),
                    ),
                    "Soil bioengineering combines engineering function with ecological "
                    "recovery by using live plant material as structure.",
                ),
                q(
                    "A bare slope has RUSLE loss of 225 t/ha/yr; adding grass drops C "
                    "from 1.0 to 0.02. Roughly what is the new loss?",
                    (
                        opt("About 225 t/ha/yr, unchanged"),
                        opt("About 45 t/ha/yr"),
                        opt("About 4.5 t/ha/yr", correct=True),
                        opt("Exactly zero"),
                    ),
                    "Loss scales linearly with C: 225 * (0.02/1.0) = 4.5 t/ha/yr, roughly "
                    "a 50-fold reduction.",
                ),
            ),
        ),
        # -- 5. Constructed wetlands -----------------------------------
        _t(
            "Constructed wetlands",
            "12 min",
            """# Constructed wetlands

A **constructed wetland** is an engineered ecosystem - a shallow, planted
basin - that treats water (municipal wastewater, stormwater, mine or
agricultural runoff) using the same processes as natural wetlands:
sedimentation, plant uptake, and above all **microbial transformation** in
the root zone. It is a flagship of ecological engineering: pollutants in,
clean water and habitat out, with little energy input.

Two main types:

- **Surface-flow (free water surface)** - water flows over the soil among
  emergent plants; looks like a marsh, good for polishing and habitat.
- **Subsurface-flow** - water moves through a gravel bed planted with
  reeds; more efficient per area for BOD and pathogens, less odor and
  mosquito exposure. Can be horizontal or vertical flow.

Design is driven by the **required removal**. A common first-order
areal model (the k-C* model) sizes the wetland:

```text
First-order areal (k-C*) sizing for a constructed wetland:

    A = (Q / k) * ln( (Ci - C*) / (Ce - C*) )

    A  = wetland surface area (m2)
    Q  = flow rate (m3/day)
    k  = areal rate constant (m/day)     [pollutant and type specific]
    Ci = inlet concentration  (mg/L)
    Ce = target outlet conc.  (mg/L)
    C* = background concentration (mg/L)

Worked example - BOD removal:
    Q = 500 m3/day, k = 0.10 m/day, Ci = 150, Ce = 30, C* = 5 mg/L
    A = (500 / 0.10) * ln((150 - 5)/(30 - 5))
      = 5000 * ln(145/25)
      = 5000 * ln(5.8)
      = 5000 * 1.758 = 8789 m2  (~0.88 ha)
```

So treating 500 m3/day of this wastewater to 30 mg/L BOD needs roughly
**0.9 hectare** of wetland. Halving the target outlet concentration
increases the required area (the log term grows), which is why land area
often limits how clean the effluent can get.

```mermaid
graph LR
    IN["Inflow polluted water"] --> SETTLE["Sedimentation settles solids"]
    SETTLE --> ROOT["Root zone microbial treatment"]
    ROOT --> UPTAKE["Plant nutrient uptake"]
    UPTAKE --> OUT["Cleaner outflow"]
    ROOT --> HAB["Wetland habitat co benefit"]
```

Remember: a constructed wetland is a designed ecosystem sized from the
required pollutant removal (k-C* model) - the microbes in the root zone do
most of the work, and habitat is a bonus.
""",
        ),
        quiz_lesson(
            "Quiz: Constructed wetlands",
            (
                q(
                    "In a constructed wetland, which process does most of the pollutant treatment?",
                    (
                        opt("Chlorination in a mixing tank"),
                        opt(
                            "Microbial transformation in the plant root zone, alongside "
                            "sedimentation and plant uptake",
                            correct=True,
                        ),
                        opt("High-pressure membrane filtration"),
                        opt("Ultraviolet lamps in the basin"),
                    ),
                    "Constructed wetlands rely on root-zone microbes plus settling and "
                    "plant uptake - low-energy, ecosystem-based treatment.",
                ),
                q(
                    "How does a subsurface-flow wetland differ from a surface-flow one?",
                    (
                        opt("It has no plants"),
                        opt(
                            "Water flows through a planted gravel bed rather than over "
                            "open soil, giving more efficient treatment per area and less "
                            "odor and mosquito exposure",
                            correct=True,
                        ),
                        opt("It only works with drinking water"),
                        opt("It requires no sizing calculation"),
                    ),
                    "Subsurface flow keeps water below the surface in gravel - efficient "
                    "and lower nuisance; surface flow mimics an open marsh.",
                ),
                q(
                    "In the k-C* sizing model A = (Q/k)*ln((Ci-C*)/(Ce-C*)), what happens "
                    "to required area as you demand a lower outlet concentration Ce?",
                    (
                        opt("Area decreases"),
                        opt("Area stays the same"),
                        opt(
                            "Area increases, because the logarithm term grows as Ce "
                            "approaches the background C*",
                            correct=True,
                        ),
                        opt("Area becomes negative"),
                    ),
                    "Cleaner effluent needs more area; near the background concentration "
                    "the log term rises steeply, so land often limits achievable quality.",
                ),
            ),
        ),
        # -- 6. River and stream restoration ---------------------------
        _t(
            "River and stream restoration",
            "12 min",
            """# River and stream restoration

Many rivers were straightened, dammed, dredged and cut off from their
floodplains for drainage and navigation. **River restoration** reverses
that - reconnecting the channel to its floodplain, restoring natural flow
and sediment, and rebuilding in-stream and riparian habitat. Modern
practice favors **process-based** restoration: fix the processes (flow,
sediment, connectivity) and let the river build its own form, rather than
imposing a fixed shape.

Common interventions:

- **Remeandering** - restoring sinuosity to a channelized reach, slowing
  water and recreating pools and riffles.
- **Floodplain reconnection and levee setback** - letting high flows spill
  onto the floodplain, storing water and trapping sediment.
- **Riparian buffers** - replanting the streambank corridor to shade the
  water, stabilize banks and filter runoff.
- **Barrier removal and fish passage** - removing or bypassing dams and
  culverts to restore migration and sediment transport.
- **Environmental flows** - releasing water to mimic the natural flow
  regime downstream of dams.

The **natural flow regime** - magnitude, frequency, duration, timing and
rate of change of flows - is the master variable. A widely used rule for
environmental flow is to protect a fraction of natural flow:

```python
# Simple environmental-flow (Tennant-style) check, monthly mean flows
def eflow_ok(natural_flow, released_flow, min_fraction=0.30):
    required = natural_flow * min_fraction
    return released_flow >= required, round(required, 1)

# Dam releases 8 m3/s in a month whose natural mean was 40 m3/s
ok, req = eflow_ok(40.0, 8.0)
print(ok, req)   # -> False 12.0  (needs >= 12 m3/s for good habitat)
```

Releasing only 8 m3/s where 12 m3/s (30 percent of natural) is the target
fails the environmental-flow check - habitat downstream is being starved.
The fix is to reshape the release schedule toward the natural regime, not
just raise a single number.

```mermaid
graph TD
    CHAN["Channelized degraded reach"] --> PROC["Restore processes"]
    PROC --> FLOW["Natural flow regime and eflows"]
    PROC --> SED["Sediment continuity barrier removal"]
    PROC --> CONN["Floodplain reconnection"]
    FLOW --> FORM["River rebuilds pools and riffles"]
    SED --> FORM
    CONN --> RIP["Riparian buffer shade and banks"]
    FORM --> HAB["Recovered aquatic habitat"]
    RIP --> HAB
```

Remember: restore the *processes* - flow, sediment and connectivity - and
the river builds and maintains its own healthy form, far more durably than
a fixed engineered channel shape.
""",
        ),
        quiz_lesson(
            "Quiz: River and stream restoration",
            (
                q(
                    "What is 'process-based' river restoration?",
                    (
                        opt("Pouring concrete to fix the channel in one shape forever"),
                        opt(
                            "Restoring the underlying processes - flow, sediment and "
                            "connectivity - so the river builds and maintains its own form",
                            correct=True,
                        ),
                        opt("Removing all water from the river"),
                        opt("Planting only non-native trees on the banks"),
                    ),
                    "Fix the processes and the form follows and self-maintains - far more "
                    "durable than imposing a fixed geometry.",
                ),
                q(
                    "Why are riparian buffers valuable in stream restoration?",
                    (
                        opt("They block all water from reaching the stream"),
                        opt(
                            "They shade and cool the water, stabilize banks and filter "
                            "runoff before it reaches the channel",
                            correct=True,
                        ),
                        opt("They only provide visual landscaping"),
                        opt("They increase erosion of the banks"),
                    ),
                    "The riparian corridor is a core restoration element: shade, bank "
                    "stability and pollutant filtering.",
                ),
                q(
                    "A dam releases 8 m3/s in a month whose natural mean flow was 40 "
                    "m3/s, against a 30 percent environmental-flow target. Is it enough?",
                    (
                        opt("Yes, 8 exceeds the requirement"),
                        opt(
                            "No - the target is 0.30 * 40 = 12 m3/s, and 8 falls short, "
                            "starving downstream habitat",
                            correct=True,
                        ),
                        opt("The natural flow is irrelevant to the check"),
                        opt("Environmental flow cannot be calculated"),
                    ),
                    "30 percent of 40 is 12 m3/s; releasing only 8 fails the check and "
                    "the release schedule must be reshaped toward the natural regime.",
                ),
            ),
        ),
        # -- 7. Ecological corridors and offsets -----------------------
        _t(
            "Ecological corridors and offsets",
            "11 min",
            """# Ecological corridors and offsets

Restoration rarely happens on one isolated patch. At the landscape scale,
**connectivity** decides whether populations survive: isolated fragments
lose species over time, while **ecological corridors** link them, letting
plants and animals move, breed and recolonize. Island-biogeography and
metapopulation theory both say the same thing - bigger and better-connected
habitat holds more species.

Design ideas:

- **Corridors and stepping stones** - continuous strips (riparian
  corridors are natural ones) or a chain of small patches that animals hop
  between. Width matters: a wider corridor serves more species and resists
  edge effects.
- **Buffer zones and core areas** - protect a core, surround it with a
  buffer of compatible land use.
- **Edge effects** - long, thin patches are almost all edge (drier,
  windier, more invaded); compact shapes protect more interior habitat.

When development is unavoidable, the **mitigation hierarchy** governs the
response: **avoid**, then **minimize**, then **restore/rehabilitate**, and
only as a last resort **offset** the residual impact elsewhere. A
biodiversity **offset** aims for **no net loss** (ideally a net gain) of
biodiversity, and because restored habitat is riskier and lower-quality
than intact habitat, offsets use **multipliers** - you restore several
hectares to compensate for one lost.

```text
No-net-loss offset with a multiplier:

    offset_area = impact_area * multiplier

    multiplier reflects: time lag to maturity, restoration risk,
    and the quality gap between lost and restored habitat.

Worked example:
    A road clears 5 ha of mature forest.
    Restored habitat matures slowly and may fail -> multiplier = 3.
    offset_area = 5 * 3 = 15 ha to restore for no net loss.
```

The multiplier is not padding - it prices in the years of lost function
and the chance the restoration underperforms. Offsets are a *last* resort:
avoiding the impact is always ecologically cheaper than trying to rebuild
mature habitat.

```mermaid
graph TD
    FRAG["Isolated habitat fragments"] --> CORR["Corridors and stepping stones"]
    CORR --> CONN["Populations move and recolonize"]
    DEV["Unavoidable development"] --> AVOID["Avoid"]
    AVOID --> MIN["Minimize"]
    MIN --> REST["Restore on site"]
    REST --> OFF["Offset residual with multiplier"]
    OFF --> NNL["Aim for no net loss"]
```

Remember: connect habitat so populations persist, and follow the
mitigation hierarchy - avoid first, offset last, and size offsets with a
multiplier that honestly reflects risk and time lag.
""",
        ),
        quiz_lesson(
            "Quiz: Ecological corridors and offsets",
            (
                q(
                    "Why do ecological corridors matter at the landscape scale?",
                    (
                        opt("They look attractive from the air"),
                        opt(
                            "They connect otherwise isolated habitat fragments, letting "
                            "species move, breed and recolonize, so populations persist",
                            correct=True,
                        ),
                        opt("They replace the need for any core habitat"),
                        opt("They increase edge effects on purpose"),
                    ),
                    "Connectivity counters the species loss that isolation causes - "
                    "bigger and better-connected habitat holds more species.",
                ),
                q(
                    "What is the correct order of the mitigation hierarchy?",
                    (
                        opt("Offset, restore, minimize, avoid"),
                        opt(
                            "Avoid, then minimize, then restore on site, and only "
                            "offset the residual impact as a last resort",
                            correct=True,
                        ),
                        opt("Restore first, then avoid"),
                        opt("Offset everything immediately"),
                    ),
                    "Avoid > minimize > restore > offset. Offsetting is the last resort "
                    "because rebuilding mature habitat is risky and slow.",
                ),
                q(
                    "A project clears 5 ha of mature forest and the offset multiplier is "
                    "3 for time lag and risk. How much must be restored for no net loss?",
                    (
                        opt("5 ha"),
                        opt("8 ha"),
                        opt("15 ha", correct=True),
                        opt("1.7 ha"),
                    ),
                    "offset_area = impact_area * multiplier = 5 * 3 = 15 ha; the "
                    "multiplier prices in years of lost function and restoration risk.",
                ),
            ),
        ),
        # -- 8. Monitoring restoration success -------------------------
        _t(
            "Monitoring restoration success",
            "11 min",
            """# Monitoring restoration success

Restoration is a multi-year trajectory, not an event, so you must
**monitor** to know whether the site is on track - and adjust if it is
not. Good monitoring compares measured **indicators** against
**quantitative targets** derived from the reference ecosystem, over time.

What to track (the SER five-star / ecosystem-attributes framework groups
these): **absence of threats**, **physical conditions** (soil, hydrology),
**species composition**, **structural diversity**, **ecosystem function**
(nutrient cycling, productivity), and **external exchanges** (connectivity,
gene flow).

Design principles for credible monitoring:

- **Set SMART targets tied to the reference** - for example "canopy cover
  >= 70 percent by year 5", "native species richness >= 60 percent of
  reference by year 10".
- **Use controls or reference sites** - measure a reference and, ideally,
  an untreated control so you can attribute change to your intervention
  (a BACI design: before-after, control-impact).
- **Monitor the right interval** - dense early (establishment years) then
  periodic; woody systems need a decade or more.
- **Close the loop with adaptive management** - if an indicator is off
  target, diagnose and intervene (replant gaps, control invasives, fix
  hydrology), then keep measuring.

A common quantitative check is **seedling survival**, which drives
replanting decisions:

```python
# Survival rate and replanting decision
def survival(planted, alive, threshold=0.80):
    rate = alive / planted
    replant = max(0, planted - alive) if rate < threshold else 0
    return round(rate, 2), replant

rate, replant = survival(planted=6000, alive=4200)
print(rate, replant)   # -> 0.7 1800  (70% < 80% target -> replant 1800)
```

A first-year survival of **70 percent** is below the 80 percent target, so
the plan triggers replanting of about **1800 seedlings** - a concrete
adaptive-management action, decided by data against a target.

```mermaid
graph TD
    TARGET["Targets from reference ecosystem"] --> MEAS["Measure indicators over time"]
    MEAS --> COMP["Compare to targets and reference"]
    COMP --> ONTRACK["On track continue monitoring"]
    COMP --> OFF["Off target"]
    OFF --> ACT["Adaptive action replant or control"]
    ACT --> MEAS
```

Remember: define quantitative targets from the reference, measure against
controls over years, and feed the results into adaptive management - the
restoration loop only closes when monitoring changes what you do.
""",
        ),
        quiz_lesson(
            "Quiz: Monitoring restoration success",
            (
                q(
                    "What makes a restoration monitoring target credible?",
                    (
                        opt("It is vague, like 'the site should look better'"),
                        opt(
                            "It is quantitative and tied to the reference ecosystem, such "
                            "as 'canopy cover >= 70 percent by year 5'",
                            correct=True,
                        ),
                        opt("It is set only after the project ends"),
                        opt("It ignores the reference ecosystem"),
                    ),
                    "SMART targets derived from the reference let you judge whether the "
                    "trajectory is on track.",
                ),
                q(
                    "Why use a reference site and, ideally, an untreated control (a BACI "
                    "design) when monitoring?",
                    (
                        opt("To make the report longer"),
                        opt(
                            "So observed change can be attributed to the intervention "
                            "rather than to background trends or weather",
                            correct=True,
                        ),
                        opt("Because controls are legally forbidden"),
                        opt("To avoid measuring anything"),
                    ),
                    "Before-after, control-impact comparison separates the restoration "
                    "effect from what would have happened anyway.",
                ),
                q(
                    "First-year survival is 4200 of 6000 seedlings against an 80 percent "
                    "target. What does adaptive management call for?",
                    (
                        opt("Nothing - 70 percent exceeds the target"),
                        opt(
                            "Survival is 70 percent, below the 80 percent target, so "
                            "replant about 1800 seedlings and keep monitoring",
                            correct=True,
                        ),
                        opt("Abandon the whole site immediately"),
                        opt("Remove the survivors and start over"),
                    ),
                    "4200/6000 = 0.70 < 0.80, so the data triggers replanting the gap "
                    "(about 1800) - monitoring feeding action closes the loop.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the core idea of 'self-design' in ecological engineering?",
                    (
                        opt("Specifying every plant and its exact position"),
                        opt(
                            "Setting the right conditions and a seed source, then letting "
                            "nature select and organize the species that fit",
                            correct=True,
                        ),
                        opt("Leaving the site completely untouched"),
                        opt("Replacing the ecosystem with engineered structures"),
                    ),
                    "You design conditions and trajectory; succession and selection do "
                    "the organizing toward a reference.",
                ),
                q(
                    "Why is a reference ecosystem central to restoration?",
                    (
                        opt("It sets the land's resale value"),
                        opt(
                            "It defines the target composition, structure and function "
                            "and provides the yardstick for measuring success",
                            correct=True,
                        ),
                        opt("It determines which pesticides to use"),
                        opt("It has no technical role"),
                    ),
                    "Without a reference you cannot define 'restored' or measure the gap.",
                ),
                q(
                    "In the RUSLE equation A = R*K*LS*C*P, which factor does vegetation "
                    "cover most reduce?",
                    (
                        opt("R"),
                        opt("K"),
                        opt("C, the cover and management factor", correct=True),
                        opt("P only"),
                    ),
                    "Cover drops C, the dominant controllable lever - fast vegetation can "
                    "cut soil loss dramatically.",
                ),
                q(
                    "What defines soil bioengineering?",
                    (
                        opt("Using only concrete and steel"),
                        opt(
                            "Using living plant material as structural, soil-reinforcing elements",
                            correct=True,
                        ),
                        opt("Spraying herbicide on slopes"),
                        opt("Removing all vegetation permanently"),
                    ),
                    "Live stakes, fascines and brush layers give engineering function "
                    "plus ecological recovery.",
                ),
                q(
                    "In a constructed wetland, most treatment comes from…",
                    (
                        opt("chlorine dosing"),
                        opt(
                            "microbial transformation in the root zone, with "
                            "sedimentation and plant uptake",
                            correct=True,
                        ),
                        opt("reverse osmosis membranes"),
                        opt("ultraviolet lamps"),
                    ),
                    "It is a designed ecosystem - root-zone microbes do most of the work "
                    "at low energy cost.",
                ),
                q(
                    "The k-C* wetland sizing model shows that demanding a lower outlet "
                    "concentration…",
                    (
                        opt("reduces the required area"),
                        opt(
                            "increases the required area, as the log term grows near the "
                            "background concentration",
                            correct=True,
                        ),
                        opt("has no effect on area"),
                        opt("makes the area negative"),
                    ),
                    "Cleaner effluent needs more land; near background C* the area rises steeply.",
                ),
                q(
                    "What is process-based river restoration?",
                    (
                        opt("Fixing the channel in one shape with concrete"),
                        opt(
                            "Restoring flow, sediment and connectivity so the river "
                            "builds and maintains its own form",
                            correct=True,
                        ),
                        opt("Draining the river completely"),
                        opt("Planting only exotic bank species"),
                    ),
                    "Restore the processes and the durable, self-maintaining form follows.",
                ),
                q(
                    "What is the correct order of the mitigation hierarchy?",
                    (
                        opt("Offset, restore, minimize, avoid"),
                        opt(
                            "Avoid, minimize, restore on site, then offset the residual "
                            "as a last resort",
                            correct=True,
                        ),
                        opt("Restore, then avoid"),
                        opt("Offset first, always"),
                    ),
                    "Avoiding an impact is ecologically cheaper than rebuilding mature "
                    "habitat, so offsets come last.",
                ),
                q(
                    "Why do biodiversity offsets use a multiplier greater than 1?",
                    (
                        opt("To make paperwork harder"),
                        opt(
                            "To account for the time lag to maturity, restoration risk "
                            "and the quality gap between lost and restored habitat, "
                            "aiming for no net loss",
                            correct=True,
                        ),
                        opt("Because restored habitat is always better than intact"),
                        opt("It is an arbitrary number with no basis"),
                    ),
                    "5 ha lost at a 3x multiplier means restoring 15 ha - pricing in "
                    "years of lost function and the chance restoration underperforms.",
                ),
                q(
                    "What closes the loop in restoration monitoring?",
                    (
                        opt("Filing the report and doing nothing"),
                        opt(
                            "Adaptive management - when an indicator is off target, "
                            "diagnose and intervene, then keep measuring",
                            correct=True,
                        ),
                        opt("Stopping all measurement after year one"),
                        opt("Ignoring the reference site"),
                    ),
                    "Monitoring only matters when it changes what you do - measure "
                    "against targets and controls, then act.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ECOLOGICAL_RESTORATION_COURSES: tuple[SeedCourse, ...] = (_ECOLOGICAL_RESTORATION,)
