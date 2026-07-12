"""Academy seed content - Water Quality and Environmental Monitoring.

Measuring the state of the environment: the physical, chemical,
microbiological and nutrient parameters that describe a water body, the
indices and standards used to judge them, how to design a defensible
sampling campaign, the analytical methods and QA/QC that make numbers
trustworthy, and biomonitoring with living indicators. Every lesson is a
direct explanation with a worked formula or calculation and a mermaid
diagram, followed by a checkpoint quiz; the course closes with a
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


_WATER_QUALITY_MONITORING = SeedCourse(
    slug="water-quality-monitoring",
    title="Water Quality & Environmental Monitoring",
    description=(
        "Measuring the state of the environment: water quality parameters "
        "(physical, chemical, nutrient, microbiological), the indices and "
        "standards used to judge them, sampling design and sample "
        "preservation, analytical methods and QA/QC, and biomonitoring - with "
        "worked formulas, real standards (CONAMA, WHO, EPA, ISO) and a "
        "diagram in every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Water Quality and Environmental Monitoring

You cannot manage what you do not measure. Before you treat a river,
license a discharge, or protect a drinking-water source, you have to know
its **state**: what is in the water, how much, how it varies, and how
trustworthy the numbers are. This course is the measurement half of
environmental engineering - the parameters, the standards, and the
discipline that turns a water sample into a defensible decision.

The approach is **concrete**: every lesson explains one idea directly,
shows it in a worked formula or a short calculation, and draws the idea
as a diagram. After each lesson there is a short quiz; at the end, a final
quiz covers the whole course.

What you will build understanding for, in order:

1. **Physical parameters** - turbidity, temperature, solids
2. **Chemical parameters** - dissolved oxygen, BOD, COD
3. **Nutrients and eutrophication** - nitrogen, phosphorus, trophic state
4. **Microbiological indicators** - total and fecal coliforms, E. coli
5. **Water quality indices and standards** - WQI, CONAMA, WHO, EPA
6. **Sampling design and preservation** - where, when, and how to sample
7. **Analytical methods and QA/QC** - Standard Methods, blanks, spikes
8. **Biomonitoring and bioindicators** - macroinvertebrates and biotic indices

This is the map. Each parameter connects to a standard, a method, and a
decision - by the end you will read a monitoring report and know exactly
what each number means and whether to trust it.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the core idea of environmental monitoring?",
                    (
                        opt("Treating water before you measure it"),
                        opt(
                            "Measuring the state of a water body - what is in it, how "
                            "much, and how reliably - so decisions rest on data",
                            correct=True,
                        ),
                        opt("Guessing water quality from its appearance alone"),
                        opt("Replacing laboratories with opinion"),
                    ),
                    "You cannot manage what you do not measure; monitoring produces the "
                    "defensible numbers that decisions rely on.",
                ),
                q(
                    "How is each lesson structured in this course?",
                    (
                        opt("Only long theory, no examples"),
                        opt(
                            "A direct explanation, a worked formula or calculation, and "
                            "a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("Just a quiz with no teaching"),
                        opt("Video only, no text"),
                    ),
                    "Explanation + worked example + diagram + checkpoint quiz, closing "
                    "with a comprehensive final quiz.",
                ),
            ),
        ),
        # -- 1. Physical parameters ------------------------------------
        _t(
            "Physical parameters - turbidity, temperature, solids",
            "10 min",
            """# Physical parameters - turbidity, temperature, solids

The **physical parameters** describe water without chemistry - how clear,
how warm, and how much suspended and dissolved matter it carries. They are
fast, cheap, and often the first sign something has changed.

**Turbidity** is the cloudiness caused by suspended particles scattering
light, measured by a nephelometer in **NTU** (Nephelometric Turbidity
Units). High turbidity shelters pathogens from disinfection and signals
erosion or a discharge. WHO recommends drinking water below **1 NTU** for
effective disinfection; CONAMA 357 sets limits by water class.

**Temperature** controls almost everything else: it sets the maximum
**dissolved oxygen** the water can hold (warmer water holds less), speeds
up reactions and biological demand, and shifts species. A thermal
discharge that raises temperature can suffocate a healthy stream.

**Solids** are split by how you separate them. Filter a known volume,
dry, and weigh:

- **Total Suspended Solids (TSS)** - retained on the filter.
- **Total Dissolved Solids (TDS)** - pass through, left after evaporation.
- **Total Solids (TS)** = TSS + TDS.

The gravimetric formula for suspended solids:

```text
TSS (mg/L) = (A - B) * 1000 / V

  A = mass of filter + dried residue (mg)
  B = mass of clean filter (mg)
  V = sample volume filtered (mL)

Worked example:
  clean filter B      = 1500.0 mg
  filter + residue A  = 1512.5 mg
  volume V            = 250 mL
  TSS = (1512.5 - 1500.0) * 1000 / 250
      = 12.5 * 1000 / 250
      = 50 mg/L
```

```mermaid
graph TD
    SAMPLE["Water sample"] --> FILTER["Filter known volume"]
    FILTER --> RETAINED["Retained on filter is TSS"]
    FILTER --> THROUGH["Passes through"]
    THROUGH --> EVAP["Evaporate and dry"]
    EVAP --> TDS["Residue is TDS"]
    RETAINED --> TOTAL["TS equals TSS plus TDS"]
    TDS --> TOTAL
```

Remember: physical parameters are the quick screen - turbidity for
clarity, temperature because it governs oxygen and rates, solids for the
load the water carries.
""",
        ),
        quiz_lesson(
            "Quiz: Physical parameters - turbidity, temperature, solids",
            (
                q(
                    "What does turbidity measure and in what unit?",
                    (
                        opt("Dissolved oxygen, in mg/L"),
                        opt(
                            "Cloudiness from suspended particles scattering light, in NTU",
                            correct=True,
                        ),
                        opt("Temperature, in degrees Celsius"),
                        opt("Acidity, in pH units"),
                    ),
                    "Turbidity is nephelometric cloudiness in NTU; high turbidity "
                    "shelters pathogens from disinfection.",
                ),
                q(
                    "Why does temperature matter so much to water quality?",
                    (
                        opt("It changes the water color permanently"),
                        opt(
                            "Warmer water holds less dissolved oxygen and speeds up "
                            "reactions and biological demand",
                            correct=True,
                        ),
                        opt("It has no measurable effect"),
                        opt("It only matters for drinking taste"),
                    ),
                    "Temperature sets DO saturation (warmer = less oxygen) and drives "
                    "reaction and metabolic rates.",
                ),
                q(
                    "A 200 mL sample gives a clean filter of 1000.0 mg and a "
                    "dried filter-plus-residue of 1008.0 mg. What is the TSS?",
                    (
                        opt("8 mg/L"),
                        opt("40 mg/L", correct=True),
                        opt("400 mg/L"),
                        opt("80 mg/L"),
                    ),
                    "TSS = (1008.0 - 1000.0) * 1000 / 200 = 8 * 1000 / 200 = 40 mg/L.",
                ),
            ),
        ),
        # -- 2. Chemical parameters (DO, BOD, COD) ---------------------
        _t(
            "Chemical parameters - dissolved oxygen, BOD, COD",
            "11 min",
            """# Chemical parameters - dissolved oxygen, BOD, COD

The chemistry that decides whether aquatic life survives centers on
**oxygen** and the demand placed on it by organic pollution.

**Dissolved Oxygen (DO)** is the oxygen actually available to fish and
aerobic microbes, in mg/L. It falls as temperature rises and as microbes
consume oxygen to break down waste. Below roughly **4-5 mg/L** many
species suffer; near zero the water is **anoxic** and only foul anaerobic
processes remain.

**Biochemical Oxygen Demand (BOD)** measures how much oxygen microbes need
to break down the **biodegradable** organic matter in a sample. The
standard test, **BOD5**, incubates a sample in the dark at 20 C for 5 days
and measures the oxygen consumed:

```text
BOD5 (mg/L) = (DO_initial - DO_final) * dilution_factor

  dilution_factor = total bottle volume / sample volume

Worked example:
  DO_initial   = 8.2 mg/L
  DO_final     = 3.4 mg/L
  sample       = 30 mL in a 300 mL bottle -> DF = 300/30 = 10
  BOD5 = (8.2 - 3.4) * 10 = 4.8 * 10 = 48 mg/L
```

**Chemical Oxygen Demand (COD)** uses a strong oxidant (dichromate) to
burn **all** oxidizable matter - biodegradable or not - in a couple of
hours. COD is always >= BOD, and the **BOD/COD ratio** tells you how
treatable a wastewater is: a ratio above ~0.5 means readily biodegradable
(good for biological treatment); a low ratio points to persistent or toxic
matter needing chemical or physical treatment.

The link between oxygen demand and river health is captured by the
classic **Streeter-Phelps** oxygen-sag model: a discharge drives DO down
as BOD is exerted, then reaeration from the atmosphere pulls it back up,
tracing a sag curve downstream.

```mermaid
graph LR
    WASTE["Organic discharge"] --> BOD["BOD exerted by microbes"]
    BOD --> DROP["Dissolved oxygen drops"]
    DROP --> SAG["Oxygen sag minimum"]
    ATM["Atmospheric reaeration"] --> RECOVER["Oxygen recovers downstream"]
    SAG --> RECOVER
```

Remember: DO is the resource, BOD is the biodegradable demand on it, COD
is the total chemical demand, and the sag curve links a discharge to the
oxygen a river can offer life.
""",
        ),
        quiz_lesson(
            "Quiz: Chemical parameters - dissolved oxygen, BOD, COD",
            (
                q(
                    "What does BOD measure that COD does not?",
                    (
                        opt("All oxidizable matter, biodegradable or not"),
                        opt(
                            "Only the biodegradable organic matter, via microbial "
                            "oxygen consumption",
                            correct=True,
                        ),
                        opt("The dissolved oxygen at saturation"),
                        opt("The turbidity of the sample"),
                    ),
                    "BOD is the biodegradable demand (microbes over 5 days); COD burns "
                    "everything oxidizable chemically, so COD >= BOD.",
                ),
                q(
                    "A BOD5 test reads DO 9.0 mg/L initially and 4.0 mg/L after 5 "
                    "days, with a dilution factor of 20. What is the BOD5?",
                    (
                        opt("5 mg/L"),
                        opt("100 mg/L", correct=True),
                        opt("13 mg/L"),
                        opt("0.25 mg/L"),
                    ),
                    "BOD5 = (9.0 - 4.0) * 20 = 5 * 20 = 100 mg/L.",
                ),
                q(
                    "What does the Streeter-Phelps oxygen-sag curve describe?",
                    (
                        opt("The rise of turbidity after rain"),
                        opt(
                            "Dissolved oxygen dropping below a discharge as BOD is "
                            "exerted, then recovering as reaeration outpaces demand",
                            correct=True,
                        ),
                        opt("The daily temperature cycle of a lake"),
                        opt("The pH change during titration"),
                    ),
                    "Deoxygenation from BOD versus reaeration from the atmosphere "
                    "traces the classic downstream sag and recovery.",
                ),
            ),
        ),
        # -- 3. Nutrients and eutrophication ---------------------------
        _t(
            "Nutrients and eutrophication indicators",
            "10 min",
            """# Nutrients and eutrophication indicators

**Nutrients** - chiefly **nitrogen** and **phosphorus** - are essential
for life, but in excess they over-fertilize a water body. The result is
**eutrophication**: explosive algal growth, then die-off, whose decay
consumes oxygen and kills fish, plus toxin-producing cyanobacteria.

**Nitrogen** appears as several species along an oxidation ladder:

- **Organic N and ammonia (NH3/NH4+)** - fresh pollution; ammonia is toxic
  to fish and exerts oxygen demand as it nitrifies.
- **Nitrite (NO2-)** - a short-lived intermediate.
- **Nitrate (NO3-)** - the oxidized end product; the WHO drinking-water
  guideline is **50 mg/L as nitrate** (methemoglobinemia risk in infants).

**Phosphorus**, usually the **limiting nutrient** in fresh water, is
measured as **total phosphorus (TP)**. Because it limits growth, even
small increases trigger blooms - which is why phosphorus is the priority
target in lake management.

Managers judge enrichment with a **trophic state** classification, often
via **Carlson's Trophic State Index (TSI)**, computed from total
phosphorus, chlorophyll-a, or Secchi depth:

```python
import math

def tsi_total_phosphorus(tp_ug_per_L: float) -> float:
    # Carlson TSI from total phosphorus (micrograms per litre)
    return 14.42 * math.log(tp_ug_per_L) + 4.15

# Worked example: TP = 30 ug/L
tsi = tsi_total_phosphorus(30)      # ~ 53.2
# TSI < 40 oligotrophic, 40-50 mesotrophic,
# 50-70 eutrophic, > 70 hypereutrophic
# 53.2 -> eutrophic
```

```mermaid
graph TD
    LOAD["Excess nitrogen and phosphorus"] --> ALGAE["Algal and cyanobacteria bloom"]
    ALGAE --> DIEOFF["Bloom dies off"]
    DIEOFF --> DECOMP["Decomposition consumes oxygen"]
    DECOMP --> HYPOXIA["Hypoxia and fish kills"]
    ALGAE --> TOXIN["Cyanotoxin risk"]
```

Remember: nitrogen and phosphorus feed growth, phosphorus usually limits
it in fresh water, and a trophic index turns nutrient and algae readings
into a single enrichment class.
""",
        ),
        quiz_lesson(
            "Quiz: Nutrients and eutrophication indicators",
            (
                q(
                    "What is eutrophication?",
                    (
                        opt("The natural cooling of a deep lake"),
                        opt(
                            "Nutrient over-enrichment driving algal blooms whose decay "
                            "depletes oxygen and harms aquatic life",
                            correct=True,
                        ),
                        opt("The removal of all nitrogen from water"),
                        opt("An increase in water clarity"),
                    ),
                    "Excess nitrogen and phosphorus feed blooms; the die-off consumes "
                    "oxygen, causing hypoxia and fish kills.",
                ),
                q(
                    "Which nutrient is usually the limiting factor in fresh water?",
                    (
                        opt("Phosphorus", correct=True),
                        opt("Chloride"),
                        opt("Dissolved oxygen"),
                        opt("Silica"),
                    ),
                    "Phosphorus commonly limits fresh-water growth, so it is the "
                    "priority control target for blooms.",
                ),
                q(
                    "A lake has a Carlson TSI of 53. How is it classified?",
                    (
                        opt("Oligotrophic"),
                        opt("Mesotrophic"),
                        opt("Eutrophic", correct=True),
                        opt("Hypereutrophic"),
                    ),
                    "TSI 50-70 is eutrophic (nutrient-rich); below 40 oligotrophic, "
                    "above 70 hypereutrophic.",
                ),
            ),
        ),
        # -- 4. Microbiological indicators -----------------------------
        _t(
            "Microbiological indicators - coliforms",
            "10 min",
            """# Microbiological indicators - coliforms

Testing water for every possible pathogen is impractical, so we use
**indicator organisms** - bacteria whose presence signals fecal
contamination and thus the possible presence of pathogens.

The classic indicators are **coliforms**:

- **Total coliforms** - a broad group, some naturally in soil and plants;
  useful for treatment integrity but not specific to fecal pollution.
- **Fecal (thermotolerant) coliforms** - grow at 44.5 C; a tighter signal
  of warm-blooded fecal input.
- **Escherichia coli (E. coli)** - a specific member of the fecal group
  and the **preferred indicator** of recent fecal contamination.

Good indicators share traits: present when pathogens are, absent when
water is clean, more numerous and hardier than the pathogens, easy to
detect, and harmless themselves.

Standards are strict. The **WHO** guideline for drinking water is **zero
E. coli per 100 mL**. For recreational and raw waters, CONAMA 357 sets
class limits in **coliforms per 100 mL**. Counts are reported as **Most
Probable Number (MPN)** from multiple-tube fermentation, or as **Colony
Forming Units (CFU)** from membrane filtration:

```text
Membrane filtration count:

CFU / 100 mL = (colonies counted / volume filtered in mL) * 100

Worked example:
  colonies counted = 48
  volume filtered  = 50 mL
  CFU/100 mL = (48 / 50) * 100 = 96 CFU/100 mL

Count plates with 20-80 (ideally 20-60) colonies for reliability;
dilute high-load samples so counts fall in that window.
```

```mermaid
graph TD
    SAMPLE["Water sample"] --> FILTER["Membrane filtration"]
    FILTER --> INCUBATE["Incubate on selective medium"]
    INCUBATE --> COUNT["Count coliform colonies"]
    COUNT --> CFU["Report CFU per 100 mL"]
    CFU --> COMPARE["Compare to WHO and CONAMA limits"]
    COMPARE --> DECISION["Safe or contaminated"]
```

Remember: we test indicators, not every pathogen; E. coli is the gold
standard for fecal contamination, and results are compared as CFU or MPN
per 100 mL against strict health-based limits.
""",
        ),
        quiz_lesson(
            "Quiz: Microbiological indicators - coliforms",
            (
                q(
                    "Why do we test for indicator organisms instead of every pathogen?",
                    (
                        opt("Pathogens are harmless"),
                        opt(
                            "Testing every pathogen is impractical; indicators like "
                            "E. coli reliably signal fecal contamination and possible "
                            "pathogens",
                            correct=True,
                        ),
                        opt("Indicators are cheaper to grow than water is to collect"),
                        opt("Indicators cause the disease directly"),
                    ),
                    "A good indicator is present with pathogens, easy to detect, and "
                    "harmless - E. coli is the preferred fecal indicator.",
                ),
                q(
                    "What is the WHO drinking-water guideline for E. coli?",
                    (
                        opt("Below 50 per 100 mL"),
                        opt("Zero per 100 mL", correct=True),
                        opt("Below 1000 per 100 mL"),
                        opt("Any level is acceptable"),
                    ),
                    "WHO requires zero E. coli per 100 mL in drinking water; its "
                    "presence indicates recent fecal contamination.",
                ),
                q(
                    "Membrane filtration of a 25 mL sample yields 40 coliform "
                    "colonies. What is the count per 100 mL?",
                    (
                        opt("40 CFU/100 mL"),
                        opt("160 CFU/100 mL", correct=True),
                        opt("10 CFU/100 mL"),
                        opt("1000 CFU/100 mL"),
                    ),
                    "CFU/100 mL = (40 / 25) * 100 = 160 CFU/100 mL.",
                ),
            ),
        ),
        # -- 5. Indices and standards ----------------------------------
        _t(
            "Water quality indices and standards",
            "10 min",
            """# Water quality indices and standards

A monitoring campaign produces dozens of parameters. A **Water Quality
Index (WQI)** collapses them into a single 0-100 score so a river can be
labelled from *very bad* to *excellent* and compared across sites and
time. The widely used **NSF WQI** aggregates nine parameters - DO, fecal
coliforms, pH, BOD5, temperature change, total phosphate, nitrate,
turbidity, and total solids - each converted to a sub-index **qi** by a
rating curve, then combined with weights **wi**:

```text
Weighted-sum NSF WQI:

WQI = sum( wi * qi )    with sum(wi) = 1

  qi = sub-index (0-100) from each parameter rating curve
  wi = weight of that parameter (DO and coliforms weigh most)

Simplified worked example (3 parameters):
  DO         qi = 90, wi = 0.30 -> 27.0
  coliforms  qi = 60, wi = 0.30 -> 18.0
  turbidity  qi = 70, wi = 0.40 -> 28.0
  WQI = 27.0 + 18.0 + 28.0 = 73  -> good
```

An index summarizes; **standards** set the legal line. Standards are
**use-based** - the water is protected for its intended use:

| Framework            | Scope                    | Example limit                 |
| -------------------- | ------------------------ | ----------------------------- |
| WHO Guidelines       | Drinking water (global)  | E. coli 0 per 100 mL          |
| US EPA               | Drinking and ambient US  | Nitrate 10 mg/L as N          |
| CONAMA 357/2005      | Brazil surface classes   | DO not below 5 mg/L class 2   |
| CONAMA 430/2011      | Brazil effluent limits   | BOD removal or concentration  |
| ABNT NBR standards   | Sampling and methods     | Preservation and procedures   |

CONAMA 357 sorts fresh water into **classes** (special, 1, 2, 3, 4) by
intended use; the stricter the use (e.g. water supply with simple
treatment), the tighter the limits. A result is judged against the class
assigned to that stretch of river.

```mermaid
graph TD
    PARAMS["Many parameters measured"] --> SUB["Convert each to sub index qi"]
    SUB --> WEIGHT["Apply weights wi"]
    WEIGHT --> WQI["Single WQI score"]
    WQI --> CLASS["Compare to standard classes"]
    CLASS --> USE["Judge fitness for intended use"]
```

Remember: an index gives one comparable score for communication; the
standard - WHO, EPA, or CONAMA class - sets the pass/fail line for the
water's intended use.
""",
        ),
        quiz_lesson(
            "Quiz: Water quality indices and standards",
            (
                q(
                    "What does a Water Quality Index do?",
                    (
                        opt("Replaces the need to measure any parameters"),
                        opt(
                            "Collapses many parameters into a single 0-100 score for "
                            "easy comparison and communication",
                            correct=True,
                        ),
                        opt("Measures only temperature"),
                        opt("Sets the legal discharge limit"),
                    ),
                    "A WQI aggregates weighted sub-indices into one score; standards, "
                    "not the index, set the legal line.",
                ),
                q(
                    "On what basis are water quality standards typically set?",
                    (
                        opt("The color of the water"),
                        opt(
                            "The intended use - drinking, recreation, aquatic life - "
                            "with stricter uses getting tighter limits",
                            correct=True,
                        ),
                        opt("The size of the treatment plant"),
                        opt("Random thresholds with no basis"),
                    ),
                    "Standards are use-based; e.g. CONAMA 357 classes protect fresh "
                    "water by intended use, from special to class 4.",
                ),
                q(
                    "Using WQI = sum(wi * qi): DO qi 80 wi 0.5, turbidity qi 60 "
                    "wi 0.5. What is the WQI?",
                    (
                        opt("140"),
                        opt("70", correct=True),
                        opt("40"),
                        opt("100"),
                    ),
                    "WQI = 0.5*80 + 0.5*60 = 40 + 30 = 70.",
                ),
            ),
        ),
        # -- 6. Sampling design and preservation -----------------------
        _t(
            "Sampling design and sample preservation",
            "11 min",
            """# Sampling design and sample preservation

A perfect laboratory cannot rescue a bad sample. The number is only as
good as the water that reached the lab, so **sampling design** and
**preservation** are where quality is won or lost.

**Design** answers where, when, and how often:

- **Representativeness** - the sample must reflect the water body, not a
  puddle by the bank. Sample in the mixed flow, at the right depth.
- **Grab vs composite** - a **grab** sample captures one instant (good for
  DO, pH, coliforms that change fast); a **composite** blends many aliquots
  over time or space for an average load (good for effluent loading).
- **Sampling frequency** - enough points in time to capture variation
  (storm events, seasonal cycles, diurnal DO swings), not just fair-weather
  days.
- **Chain of custody** - documented handling from field to lab so results
  are legally defensible.

**Preservation** stops the sample changing between field and bench.
Different parameters need different treatment - **Standard Methods** and
**ABNT NBR** tabulate them:

| Parameter        | Container   | Preservation          | Max holding time |
| ---------------- | ----------- | --------------------- | ---------------- |
| Dissolved oxygen | glass BOD   | fix on site or probe  | analyze at once  |
| BOD5             | plastic     | cool to 4 C           | 48 hours         |
| Metals           | plastic     | HNO3 to pH below 2    | 6 months         |
| Nutrients        | plastic     | cool 4 C or H2SO4     | 28 days          |
| Coliforms        | sterile     | cool 4 C, dark        | 24 hours         |

Some parameters must be measured **in the field** because they change
almost instantly - DO, pH, temperature, free chlorine, and turbidity are
best read on site with a calibrated probe.

The load a sample represents combines concentration with flow:

```text
Pollutant load:

Load (kg/day) = Concentration (mg/L) * Flow (m3/day) / 1000

Worked example:
  BOD concentration = 40 mg/L
  effluent flow     = 2000 m3/day
  Load = 40 * 2000 / 1000 = 80 kg BOD/day
```

```mermaid
graph LR
    PLAN["Design where when how often"] --> COLLECT["Collect grab or composite"]
    COLLECT --> FIELD["Measure DO pH temperature on site"]
    COLLECT --> PRESERVE["Preserve cool acidify"]
    PRESERVE --> CUSTODY["Chain of custody"]
    CUSTODY --> LAB["Analyze within holding time"]
```

Remember: representative design, the right grab-or-composite choice,
field measurement of the volatile parameters, correct preservation, and
holding times - miss any and the lab result describes a sample that no
longer exists.
""",
        ),
        quiz_lesson(
            "Quiz: Sampling design and sample preservation",
            (
                q(
                    "When is a composite sample preferred over a grab sample?",
                    (
                        opt("For dissolved oxygen, which changes fast"),
                        opt(
                            "When you want an average load over time or space, such as "
                            "effluent loading",
                            correct=True,
                        ),
                        opt("Never - grabs are always better"),
                        opt("Only for coliform testing"),
                    ),
                    "Composites blend many aliquots for an average; grabs capture one "
                    "instant, needed for fast-changing parameters like DO.",
                ),
                q(
                    "Why are DO, pH and temperature usually measured in the field?",
                    (
                        opt("Field probes are cheaper than any lab"),
                        opt(
                            "They change almost instantly after collection, so bench "
                            "values would no longer represent the water",
                            correct=True,
                        ),
                        opt("The lab cannot measure them at all"),
                        opt("Regulations forbid lab measurement"),
                    ),
                    "Volatile parameters shift in transit; a calibrated on-site probe "
                    "captures the true in-situ value.",
                ),
                q(
                    "An effluent at 50 mg/L BOD flows at 4000 m3/day. What is the BOD load?",
                    (
                        opt("20 kg/day"),
                        opt("200 kg/day", correct=True),
                        opt("2000 kg/day"),
                        opt("2 kg/day"),
                    ),
                    "Load = 50 * 4000 / 1000 = 200 kg BOD/day.",
                ),
            ),
        ),
        # -- 7. Analytical methods and QA/QC ---------------------------
        _t(
            "Analytical methods and quality control (QA and QC)",
            "11 min",
            """# Analytical methods and quality control (QA and QC)

A number without quality control is just a rumor. **Analytical methods**
must be standardized and their results checked, or you cannot know whether
a reading reflects the water or a mistake. Two ideas underpin this:

- **QA (Quality Assurance)** - the whole management system: documented,
  validated methods, trained analysts, accredited labs (ISO/IEC 17025).
- **QC (Quality Control)** - the specific field and bench checks that catch
  error in each batch.

Use **recognized methods** - *Standard Methods for the Examination of
Water and Wastewater*, EPA methods, and **ABNT NBR** procedures - so
results are comparable and defensible. Common instruments: titration
(alkalinity, DO Winkler), spectrophotometry (nutrients, metals color
reactions), ion chromatography, and ICP for trace metals.

The core **QC samples** each catch a different error:

| QC sample        | What it catches                                  |
| ---------------- | ------------------------------------------------ |
| Method blank     | Contamination from reagents or glassware         |
| Duplicate        | Precision - random scatter of the method         |
| Matrix spike     | Recovery and matrix interference (accuracy)      |
| Calibration std  | Instrument drift against known concentrations    |
| Field blank      | Contamination during sampling and transport      |

Two numbers summarize batch quality. **Spike recovery** checks accuracy;
acceptance is often **80-120 percent**:

```text
Percent recovery = (spiked_result - sample_result) / spike_added * 100

Worked example:
  sample_result  = 5.0 mg/L
  spiked_result  = 14.0 mg/L
  spike_added    = 10.0 mg/L
  recovery = (14.0 - 5.0) / 10.0 * 100 = 90 percent  -> acceptable
```

**Relative Percent Difference (RPD)** on duplicates checks precision:

```text
RPD = |value1 - value2| / ((value1 + value2)/2) * 100

  duplicates 20 and 22 mg/L:
  RPD = |20 - 22| / 21 * 100 = 2/21 * 100 = 9.5 percent  -> good precision
```

Below the numbers lie the **detection limits**: the **MDL** (method
detection limit) is the lowest concentration reliably distinguished from
zero, and results below it are reported as *not detected*, not as zero.

```mermaid
graph TD
    METHOD["Standardized method"] --> CALIB["Calibrate instrument"]
    CALIB --> RUN["Analyze samples"]
    RUN --> QC["Run QC blanks duplicates spikes"]
    QC --> CHECK["Recovery and RPD within limits"]
    CHECK --> ACCEPT["Report results"]
    CHECK --> REJECT["Out of limits reanalyze batch"]
```

Remember: QA is the system and QC the checks - blanks for contamination,
duplicates for precision, spikes for accuracy - and results below the
detection limit are *not detected*, never a bare zero.
""",
        ),
        quiz_lesson(
            "Quiz: Analytical methods and quality control (QA and QC)",
            (
                q(
                    "What is the difference between QA and QC?",
                    (
                        opt("They are identical terms"),
                        opt(
                            "QA is the overall management system of validated methods "
                            "and accreditation; QC is the specific field and bench "
                            "checks in each batch",
                            correct=True,
                        ),
                        opt("QA is done only in the field, QC only in the office"),
                        opt("QC sets the standards, QA analyzes samples"),
                    ),
                    "QA assures the system (methods, training, ISO 17025); QC catches "
                    "error per batch with blanks, duplicates and spikes.",
                ),
                q(
                    "A matrix spike adds 10 mg/L; the sample reads 3.0 and the "
                    "spiked reads 12.0 mg/L. What is the percent recovery?",
                    (
                        opt("120 percent"),
                        opt("90 percent", correct=True),
                        opt("75 percent"),
                        opt("30 percent"),
                    ),
                    "Recovery = (12.0 - 3.0) / 10.0 * 100 = 90 percent, within the "
                    "usual 80-120 percent window.",
                ),
                q(
                    "How should a result below the method detection limit be reported?",
                    (
                        opt("As exactly zero"),
                        opt(
                            "As not detected, since below the MDL it cannot be reliably "
                            "distinguished from zero",
                            correct=True,
                        ),
                        opt("As the highest calibration standard"),
                        opt("As a negative number"),
                    ),
                    "Below the MDL the method cannot separate the value from zero, so "
                    "it is reported as not detected, not as a bare zero.",
                ),
            ),
        ),
        # -- 8. Biomonitoring ------------------------------------------
        _t(
            "Biomonitoring and bioindicators",
            "10 min",
            """# Biomonitoring and bioindicators

Chemical sampling is a snapshot - it captures the water only at the
instant you dipped the bottle. **Biomonitoring** uses living organisms as
integrators: because they live in the water continuously, their community
reflects conditions over **weeks and months**, including pollution pulses
a monthly grab sample would miss.

A **bioindicator** is a species or community whose presence, absence, or
condition reveals environmental quality. The workhorses in rivers are
**benthic macroinvertebrates** - insect larvae, worms, snails, crustaceans
living on the bed - because different groups have different **sensitivity
to pollution**:

- **Sensitive (intolerant)** - mayflies, stoneflies, caddisflies (the
  **EPT** taxa). Their presence signals clean, well-oxygenated water.
- **Tolerant** - worms (oligochaetes) and midge larvae (chironomids)
  thrive even in organically polluted, low-oxygen water. A community of
  only these signals degradation.

Turning the community into a score uses a **biotic index**. Each taxon
gets a tolerance value; the assemblage yields an index compared to
reference conditions. A simple, robust example is the **percent EPT**:

```python
def percent_ept(ept_count: int, total_count: int) -> float:
    # fraction of the sample that is sensitive EPT taxa
    return ept_count / total_count * 100

# Worked example: 45 EPT out of 150 individuals
pct = percent_ept(45, 150)     # 30.0 percent
# high percent EPT -> good quality; low -> degraded
```

Other tools include the **BMWP** (Biological Monitoring Working Party)
score, diatom indices, and **bioassays** - controlled toxicity tests where
organisms (Daphnia, algae, fish) are exposed to a sample to measure lethal
or effect concentrations. Bioindicators and chemistry are complementary:
chemistry tells you **what** pollutant and how much; biology tells you the
**integrated ecological effect** over time.

```mermaid
graph TD
    SAMPLE["Sample the river bed community"] --> IDENTIFY["Identify macroinvertebrate taxa"]
    IDENTIFY --> SENSITIVE["Sensitive EPT taxa present"]
    IDENTIFY --> TOLERANT["Tolerant worms and midges"]
    SENSITIVE --> SCORE["Compute biotic index"]
    TOLERANT --> SCORE
    SCORE --> QUALITY["Ecological quality class"]
```

Remember: chemistry is a snapshot, biology integrates over time; sensitive
EPT taxa mean clean water, a tolerant-only community means degradation,
and a biotic index turns the living community into a quality class.
""",
        ),
        quiz_lesson(
            "Quiz: Biomonitoring and bioindicators",
            (
                q(
                    "What advantage does biomonitoring have over a single chemical grab sample?",
                    (
                        opt("It is always cheaper and needs no expertise"),
                        opt(
                            "Living communities integrate conditions over weeks and "
                            "months, capturing pollution pulses a snapshot would miss",
                            correct=True,
                        ),
                        opt("It measures exact pollutant concentrations"),
                        opt("It replaces the need for any chemistry"),
                    ),
                    "Organisms live in the water continuously, so their community "
                    "reflects integrated conditions, not just one instant.",
                ),
                q(
                    "What does a community of only tolerant worms and midge larvae indicate?",
                    (
                        opt("Clean, well-oxygenated water"),
                        opt(
                            "Organic pollution and degraded, low-oxygen conditions",
                            correct=True,
                        ),
                        opt("No possible conclusion"),
                        opt("High turbidity only"),
                    ),
                    "Tolerant taxa persist in polluted, low-oxygen water; the absence "
                    "of sensitive EPT taxa signals degradation.",
                ),
                q(
                    "A sample has 30 EPT individuals out of 120 total. What is the percent EPT?",
                    (
                        opt("30 percent"),
                        opt("25 percent", correct=True),
                        opt("4 percent"),
                        opt("40 percent"),
                    ),
                    "Percent EPT = 30 / 120 * 100 = 25 percent; higher values indicate "
                    "better ecological quality.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is environmental water monitoring for?",
                    (
                        opt("Treating water without measuring it"),
                        opt(
                            "Measuring the state of a water body reliably so decisions "
                            "and standards rest on defensible data",
                            correct=True,
                        ),
                        opt("Judging water quality by appearance alone"),
                        opt("Eliminating the need for laboratories"),
                    ),
                    "You cannot manage what you do not measure; monitoring produces "
                    "the trustworthy numbers decisions rely on.",
                ),
                q(
                    "What does turbidity indicate and why does it matter for disinfection?",
                    (
                        opt("Oxygen level; it has no disinfection effect"),
                        opt(
                            "Cloudiness from suspended particles that can shelter "
                            "pathogens from disinfection",
                            correct=True,
                        ),
                        opt("Temperature; warmer water disinfects better"),
                        opt("Nitrate concentration"),
                    ),
                    "High turbidity shields microbes from disinfectant, so WHO advises "
                    "drinking water below 1 NTU.",
                ),
                q(
                    "Why is COD always greater than or equal to BOD?",
                    (
                        opt("COD ignores oxidizable matter"),
                        opt(
                            "COD chemically oxidizes all oxidizable matter, while BOD "
                            "only counts the biodegradable fraction",
                            correct=True,
                        ),
                        opt("BOD includes metals COD cannot"),
                        opt("They are unrelated measurements"),
                    ),
                    "COD burns everything oxidizable; BOD is the biodegradable subset, "
                    "so COD >= BOD and the ratio shows treatability.",
                ),
                q(
                    "Which nutrient usually limits growth in fresh water, making it "
                    "the priority target for blooms?",
                    (
                        opt("Chloride"),
                        opt("Phosphorus", correct=True),
                        opt("Sodium"),
                        opt("Dissolved oxygen"),
                    ),
                    "Phosphorus is commonly the limiting nutrient in fresh water; even "
                    "small increases can trigger eutrophication.",
                ),
                q(
                    "Which organism is the preferred indicator of recent fecal contamination?",
                    (
                        opt("Total coliforms"),
                        opt("Escherichia coli", correct=True),
                        opt("Blue-green algae"),
                        opt("Mayfly larvae"),
                    ),
                    "E. coli is a specific fecal indicator; WHO requires zero E. coli "
                    "per 100 mL in drinking water.",
                ),
                q(
                    "What is the role of a Water Quality Index versus a standard?",
                    (
                        opt("They are the same thing"),
                        opt(
                            "The index gives one comparable 0-100 score for "
                            "communication; the standard sets the legal pass/fail line "
                            "by intended use",
                            correct=True,
                        ),
                        opt("The index is legally binding, the standard is optional"),
                        opt("Both only measure temperature"),
                    ),
                    "A WQI summarizes many parameters; standards like WHO, EPA and "
                    "CONAMA classes set the enforceable limits.",
                ),
                q(
                    "Why must DO, pH and temperature be measured in the field?",
                    (
                        opt("Field probes are more accurate than any lab"),
                        opt(
                            "They change almost instantly after collection, so lab "
                            "values would not represent the water",
                            correct=True,
                        ),
                        opt("Labs are legally forbidden from measuring them"),
                        opt("They cannot be measured at all"),
                    ),
                    "Volatile parameters shift in transit; an on-site calibrated probe "
                    "captures the true in-situ value.",
                ),
                q(
                    "Which QC sample catches contamination from reagents or glassware?",
                    (
                        opt("Matrix spike"),
                        opt("Duplicate"),
                        opt("Method blank", correct=True),
                        opt("Calibration standard"),
                    ),
                    "A blank should read clean; a signal in it reveals contamination "
                    "from reagents, glassware or handling.",
                ),
                q(
                    "A spike adds 20 mg/L; sample reads 4.0 and spiked reads 22.0 "
                    "mg/L. What is the percent recovery?",
                    (
                        opt("110 percent"),
                        opt("90 percent", correct=True),
                        opt("18 percent"),
                        opt("80 percent"),
                    ),
                    "Recovery = (22.0 - 4.0) / 20.0 * 100 = 90 percent, inside the "
                    "80-120 percent acceptance window.",
                ),
                q(
                    "What does an abundance of sensitive EPT macroinvertebrates signal?",
                    (
                        opt("Severe organic pollution"),
                        opt(
                            "Clean, well-oxygenated water of good ecological quality",
                            correct=True,
                        ),
                        opt("High nitrate only"),
                        opt("Nothing measurable"),
                    ),
                    "Mayflies, stoneflies and caddisflies are intolerant of pollution; "
                    "their presence indicates healthy, well-oxygenated water.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

WATER_QUALITY_MONITORING_COURSES: tuple[SeedCourse, ...] = (_WATER_QUALITY_MONITORING,)
