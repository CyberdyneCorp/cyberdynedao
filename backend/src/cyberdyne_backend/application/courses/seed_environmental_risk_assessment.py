"""Academy seed content - Environmental and Health Risk Assessment.

Quantifying environmental and health risk end to end: the difference
between hazard and risk, environmental toxicology, dose-response
assessment, exposure assessment, carcinogenic and non-carcinogenic risk
characterization, ecological risk, uncertainty, and the risk
communication and management that turns numbers into decisions. Each
lesson is a direct explanation grounded in EPA, WHO and CONAMA/ABNT
practice, with one mermaid diagram and a worked formula or calculation;
every lesson is followed by a checkpoint quiz and the course closes with
a comprehensive final quiz.
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


_ENVIRONMENTAL_RISK_ASSESSMENT = SeedCourse(
    slug="environmental-risk-assessment",
    title="Environmental & Health Risk Assessment",
    description=(
        "Quantifying environmental and health risk: hazard versus risk, "
        "environmental toxicology, dose-response and exposure assessment, "
        "carcinogenic and non-carcinogenic risk, ecological risk, and risk "
        "characterization, communication and management - grounded in EPA, "
        "WHO and CONAMA/ABNT practice with a worked calculation and a "
        "diagram in every lesson."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental and Health Risk Assessment

Risk assessment is how we turn "this chemical is present" into "this is
how much harm it could cause, to whom, and how sure we are." It is the
bridge between environmental science and decisions about cleanup limits,
discharge permits, and public-health protection. This course teaches the
standard four-step framework used by the US EPA, the WHO, and Brazilian
regulators (CONAMA, ABNT NBR) and shows the math behind each step.

The approach is **quantitative and concrete**: every lesson explains one
idea directly, works one real calculation (an intake equation, a hazard
quotient, a cancer-risk estimate), and draws the idea as a diagram. After
each lesson there is a short quiz; at the end, a final quiz covers the
whole course.

What you will build understanding for, in order:

1. **Hazard versus risk** - why the two are not the same
2. **Environmental toxicology** - how substances cause harm
3. **Dose-response assessment** - the toxicity side of the equation
4. **Exposure assessment** - the contact side of the equation
5. **Carcinogenic and non-carcinogenic risk** - the two risk pathways
6. **Ecological risk assessment** - harm to populations and ecosystems
7. **Risk characterization and uncertainty** - combining and qualifying
8. **Risk communication and management** - from numbers to decisions

The four steps - hazard identification, dose-response, exposure, and
risk characterization - are the spine of the whole field. Learn where
each fits and the calculations become straightforward.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the purpose of risk assessment?",
                    (
                        opt("To prove a chemical is completely safe"),
                        opt(
                            "To turn the presence of a hazard into an estimate of how "
                            "much harm it could cause, to whom, and with what "
                            "uncertainty - to support decisions",
                            correct=True,
                        ),
                        opt("To measure only the concentration of a pollutant"),
                        opt("To replace environmental monitoring entirely"),
                    ),
                    "Risk assessment quantifies potential harm to inform decisions; it "
                    "is not a pass/fail safety certificate.",
                ),
                q(
                    "Which framework does this course follow?",
                    (
                        opt("A single-step pass/fail checklist"),
                        opt(
                            "The four-step framework: hazard identification, "
                            "dose-response, exposure assessment, risk characterization",
                            correct=True,
                        ),
                        opt("Only laboratory toxicity testing"),
                        opt("Only economic cost-benefit analysis"),
                    ),
                    "The four steps used by EPA, WHO and CONAMA/ABNT are the spine of "
                    "the whole field.",
                ),
            ),
        ),
        # -- 1. Hazard versus risk -------------------------------------
        _t(
            "Hazard versus risk",
            "9 min",
            """# Hazard versus risk

The single most misunderstood idea in the field is the difference between
hazard and risk. A **hazard** is the intrinsic ability of an agent to
cause harm - a property of the substance itself (mercury is toxic to the
nervous system; benzene is a carcinogen). A **risk** is the probability
that harm actually occurs given real-world **exposure** to that hazard.

The core relationship is simple to state:

**Risk = Hazard x Exposure**

A very hazardous substance locked in a sealed drum poses little risk,
because exposure is near zero. A mildly hazardous substance that everyone
drinks daily can pose a large risk. You cannot judge risk from hazard
alone - you must ask *how much*, *how often*, and *to whom*.

This distinction drives the whole four-step process. The first step,
**hazard identification**, asks *can this agent cause harm and what kind?*
The remaining steps quantify *how much*, under real exposure.

```mermaid
graph LR
    HAZID["Hazard identification"] --> DR["Dose response assessment"]
    HAZID --> EXP["Exposure assessment"]
    DR --> RC["Risk characterization"]
    EXP --> RC
    RC --> DEC["Risk management decision"]
```

A worked illustration of why exposure matters - two agents, same setting:

```text
Risk index = Hazard potency x Exposure (arbitrary units)

Agent A: highly toxic, potency = 100
         sealed, exposure  = 0.01
         risk index        = 100 x 0.01 = 1.0

Agent B: mildly toxic,  potency = 5
         daily contact, exposure = 2.0
         risk index        = 5 x 2.0   = 10.0

Conclusion: Agent B, though far less hazardous, poses ten times the
risk here because exposure dominates the product.
```

Regulators phrase this deliberately: a **hazard** classification (for
example a GHS pictogram, or a CONAMA list of priority pollutants) flags
what a substance *can* do; a **risk** assessment estimates what it *will*
do in a specific scenario. Managing risk means reducing the hazard, the
exposure, or both.

Remember: hazard is a property; risk is a probability that depends on
exposure. No exposure, no risk - however toxic the agent.
""",
        ),
        quiz_lesson(
            "Quiz: Hazard versus risk",
            (
                q(
                    "What is the difference between a hazard and a risk?",
                    (
                        opt("They mean exactly the same thing"),
                        opt(
                            "A hazard is the intrinsic ability of an agent to cause "
                            "harm; a risk is the probability harm actually occurs given "
                            "real exposure",
                            correct=True,
                        ),
                        opt("A hazard applies to people, a risk only to ecosystems"),
                        opt("A risk is measured in the lab, a hazard in the field"),
                    ),
                    "Hazard is a property of the substance; risk depends on exposure to "
                    "that hazard.",
                ),
                q(
                    "Which relationship best captures how risk arises?",
                    (
                        opt("Risk = Hazard only"),
                        opt("Risk = Exposure only"),
                        opt("Risk = Hazard x Exposure", correct=True),
                        opt("Risk = Hazard minus Exposure"),
                    ),
                    "A hazardous agent with near-zero exposure poses little risk; both "
                    "factors must be present.",
                ),
                q(
                    "A highly toxic substance sealed in an inaccessible container poses "
                    "what level of risk?",
                    (
                        opt("Very high, because it is toxic"),
                        opt(
                            "Low, because exposure is near zero even though the hazard is high",
                            correct=True,
                        ),
                        opt("Exactly the same as its hazard rating"),
                        opt("Impossible to estimate under any framework"),
                    ),
                    "No exposure, no risk - regardless of how hazardous the agent is.",
                ),
            ),
        ),
        # -- 2. Environmental toxicology -------------------------------
        _t(
            "Environmental toxicology",
            "10 min",
            """# Environmental toxicology

**Environmental toxicology** studies how chemical, physical and
biological agents cause adverse effects in living organisms and how those
agents behave once released. It provides the biological knowledge that
hazard identification and dose-response assessment depend on.

A few organizing concepts:

- **Toxicokinetics (ADME)** - what the body does to the substance:
  **A**bsorption, **D**istribution, **M**etabolism, **E**xcretion. This
  determines the **internal dose** that actually reaches target tissue.
- **Toxicodynamics** - what the substance does to the body: the mechanism
  of the adverse effect at the target site.
- **Bioaccumulation and biomagnification** - lipophilic, persistent
  substances (methylmercury, PCBs, many organochlorines) build up in
  tissue and concentrate up the food chain, so top predators and humans
  eating them carry the highest burden.
- **Acute versus chronic** - a single high dose versus long-term low-level
  exposure can produce entirely different effects.

The classic principle, from Paracelsus, is *"the dose makes the poison"* -
almost anything is toxic above some level, and many essential elements
(copper, selenium, zinc) are harmful both when deficient and when in
excess.

```mermaid
graph LR
    SRC["Source release"] --> ENV["Environmental fate"]
    ENV --> UPTAKE["Uptake and absorption"]
    UPTAKE --> ADME["Distribution metabolism excretion"]
    ADME --> TARGET["Target tissue internal dose"]
    TARGET --> EFFECT["Adverse effect"]
```

A quantitative anchor: **bioaccumulation** is often summarized by a
**Bioconcentration Factor (BCF)**, the ratio of concentration in an
organism to that in water at steady state.

```text
BCF = C_organism / C_water

Example (a persistent organic pollutant in fish):
  C_organism = 2.5 mg per kg tissue
  C_water    = 0.0005 mg per L
  BCF        = 2.5 / 0.0005 = 5000 L per kg

A BCF of 5000 signals strong bioaccumulation - the fish concentrates the
substance 5000-fold over the surrounding water, so a diet-based exposure
pathway may dominate the human risk even at low water concentrations.
```

Remember: toxicology tells us *how* an agent harms and *how much* reaches
the target. ADME sets the internal dose, bioaccumulation can amplify
exposure, and the dose always makes the poison.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental toxicology",
            (
                q(
                    "What do the letters ADME stand for in toxicokinetics?",
                    (
                        opt("Analysis, Detection, Measurement, Evaluation"),
                        opt(
                            "Absorption, Distribution, Metabolism, Excretion - what the "
                            "body does to a substance",
                            correct=True,
                        ),
                        opt("Acute, Delayed, Mutagenic, Ecological"),
                        opt("Air, Dust, Moisture, Effluent"),
                    ),
                    "ADME determines the internal dose that actually reaches target tissue.",
                ),
                q(
                    "What does a high Bioconcentration Factor (BCF) indicate?",
                    (
                        opt("The substance breaks down quickly in water"),
                        opt(
                            "The organism concentrates the substance far above the water "
                            "concentration, signalling strong bioaccumulation",
                            correct=True,
                        ),
                        opt("The substance is not toxic"),
                        opt("Exposure through water is the only pathway"),
                    ),
                    "BCF = C_organism / C_water; a large value means diet-based exposure "
                    "pathways may dominate risk.",
                ),
                q(
                    "What does 'the dose makes the poison' mean?",
                    (
                        opt("Only synthetic chemicals are toxic"),
                        opt(
                            "Toxicity depends on the amount - almost anything can be "
                            "harmful above some level, and some essentials harm in "
                            "excess or deficiency",
                            correct=True,
                        ),
                        opt("Poisons have no safe level ever"),
                        opt("Dose is irrelevant to toxicity"),
                    ),
                    "Paracelsus' principle: magnitude of exposure, not mere presence, "
                    "determines effect.",
                ),
            ),
        ),
        # -- 3. Dose-response assessment -------------------------------
        _t(
            "Dose-response assessment",
            "11 min",
            """# Dose-response assessment

**Dose-response assessment** is the toxicity half of risk: it quantifies
how the probability or severity of an effect changes with dose. It turns
"this is toxic" into a number you can multiply against exposure.

A central distinction shapes the whole calculation:

- **Threshold (non-carcinogenic) effects** - the body tolerates low doses
  with no observable adverse effect; harm appears only above a threshold.
  The key experimental points are the **NOAEL** (No Observed Adverse
  Effect Level) and **LOAEL** (Lowest Observed Adverse Effect Level).
- **Non-threshold (carcinogenic) effects** - assumed to have *no* safe
  dose; any exposure carries some incremental probability. The dose-
  response is treated as linear at low dose through the origin.

For threshold effects, regulators derive a **Reference Dose (RfD)** (or
Acceptable Daily Intake) - a daily dose believed safe over a lifetime -
by dividing a point of departure by **uncertainty factors (UF)**:

```text
RfD = POD / (UF1 x UF2 x ...)

POD = NOAEL or a benchmark dose, in mg per kg per day
UFs (each typically 10): interspecies, intraspecies (sensitive humans),
     subchronic-to-chronic, LOAEL-to-NOAEL, database gaps

Example:
  NOAEL = 5 mg per kg per day (chronic rat study)
  UF    = 10 (animal to human) x 10 (human variability) = 100
  RfD   = 5 / 100 = 0.05 mg per kg per day
```

For non-threshold (cancer) effects, the toxicity value is the **Slope
Factor (SF)** - the risk per unit dose - taken from the linear low-dose
slope of the dose-response curve.

```mermaid
graph TD
    STUDY["Toxicity study data"] --> POD["Point of departure NOAEL or BMD"]
    POD --> TYPE{"Threshold effect"}
    TYPE -->|"yes"| RFD["Divide by UF to get RfD"]
    TYPE -->|"no"| SF["Fit linear low dose slope factor"]
    RFD --> NONCANCER["Non cancer toxicity value"]
    SF --> CANCER["Cancer toxicity value"]
```

The **benchmark dose (BMD)** approach increasingly replaces the raw
NOAEL: it fits a model to all the data and takes the dose for a defined
response level (say a 10 percent increase), using its lower confidence
bound (BMDL) as the point of departure - more statistically robust than
picking one tested dose.

Remember: dose-response produces the toxicity number - an RfD for
threshold effects, a slope factor for carcinogens - that the exposure
estimate is later compared against or multiplied by.
""",
        ),
        quiz_lesson(
            "Quiz: Dose-response assessment",
            (
                q(
                    "How is a Reference Dose (RfD) derived from a NOAEL?",
                    (
                        opt("By multiplying the NOAEL by uncertainty factors"),
                        opt(
                            "By dividing the point of departure (NOAEL or BMD) by the "
                            "product of uncertainty factors",
                            correct=True,
                        ),
                        opt("By taking the highest tested dose directly"),
                        opt("By fitting a linear slope through the origin"),
                    ),
                    "RfD = POD / (UF1 x UF2 x ...); uncertainty factors account for "
                    "interspecies and human variability.",
                ),
                q(
                    "How do threshold and non-threshold (carcinogenic) effects differ "
                    "in dose-response?",
                    (
                        opt("Threshold effects have no safe dose"),
                        opt(
                            "Threshold effects have a dose below which no harm is "
                            "observed; non-threshold effects are assumed to carry risk "
                            "at any dose",
                            correct=True,
                        ),
                        opt("Non-threshold effects only occur in animals"),
                        opt("There is no practical difference"),
                    ),
                    "Non-carcinogens get an RfD below a threshold; carcinogens get a "
                    "slope factor with no assumed safe dose.",
                ),
                q(
                    "What advantage does the benchmark dose (BMD) approach have over "
                    "using a raw NOAEL?",
                    (
                        opt("It ignores the experimental data"),
                        opt(
                            "It fits a model to all the data and uses a lower confidence "
                            "bound, making it more statistically robust than one tested "
                            "dose",
                            correct=True,
                        ),
                        opt("It always gives a higher, less protective value"),
                        opt("It removes the need for any toxicity study"),
                    ),
                    "The BMDL uses the whole curve rather than depending on which doses "
                    "happened to be tested.",
                ),
            ),
        ),
        # -- 4. Exposure assessment ------------------------------------
        _t(
            "Exposure assessment",
            "11 min",
            """# Exposure assessment

**Exposure assessment** is the contact half of risk: it estimates the
magnitude, frequency, duration and route by which people (or organisms)
come into contact with a hazard, and converts that into a **dose** you
can compare against a toxicity value.

The key routes are **ingestion** (water, food, soil), **inhalation**
(air, vapor, dust) and **dermal** contact. For each, you build an
**exposure pathway**: a source, a release, an environmental medium, a
point of contact, and an exposed population. If any link is missing, the
pathway is incomplete and contributes no exposure.

The workhorse equation is the **Chronic Daily Intake (CDI)**, in mg per
kg of body weight per day. For drinking-water ingestion:

```text
CDI = (C x IR x EF x ED) / (BW x AT)

C  = contaminant concentration      (mg per L)
IR = intake rate                    (L per day)
EF = exposure frequency             (days per year)
ED = exposure duration              (years)
BW = body weight                    (kg)
AT = averaging time                 (days)

Example (adult, non-carcinogen):
  C  = 0.05 mg per L      IR = 2 L per day
  EF = 350 days per year  ED = 30 years
  BW = 70 kg              AT = 30 x 365 = 10950 days
  CDI = (0.05 x 2 x 350 x 30) / (70 x 10950)
      = 1050 / 766500
      = 0.00137 mg per kg per day
```

Two modeling choices matter. First, **averaging time**: for
non-carcinogens AT equals the exposure duration (effects track the
exposure period); for carcinogens AT equals a full lifetime (about 70
years, or 25550 days), spreading dose over the whole life. Second, the
**exposure scenario**: a central-tendency (average) estimate versus a
**Reasonable Maximum Exposure (RME)** for the more-exposed individual -
regulators typically protect the RME.

```mermaid
graph LR
    SRC["Contaminant source"] --> MEDIA["Environmental medium"]
    MEDIA --> ROUTE["Ingestion inhalation dermal"]
    ROUTE --> PARAM["Intake parameters IR EF ED BW"]
    PARAM --> CDI["Chronic daily intake"]
    CDI --> RISK["Feeds risk characterization"]
```

Exposure parameters come from standardized references (the EPA Exposure
Factors Handbook, and national equivalents) so assessments are
comparable. Concentrations may come from monitoring or from fate-and-
transport models (air dispersion, groundwater transport).

Remember: exposure assessment produces the dose (CDI) - concentration
times contact, normalized to body weight and time - which is exactly what
the toxicity value from dose-response is compared against.
""",
        ),
        quiz_lesson(
            "Quiz: Exposure assessment",
            (
                q(
                    "In the Chronic Daily Intake equation, what does the numerator "
                    "(C x IR x EF x ED) represent?",
                    (
                        opt("The toxicity of the substance"),
                        opt(
                            "The total amount contacted - concentration times intake "
                            "rate, frequency and duration",
                            correct=True,
                        ),
                        opt("The uncertainty factor"),
                        opt("The slope factor"),
                    ),
                    "The numerator is total contact; dividing by body weight and "
                    "averaging time normalizes it to a daily dose.",
                ),
                q(
                    "How does the averaging time (AT) differ between carcinogens and "
                    "non-carcinogens?",
                    (
                        opt("It is always the same"),
                        opt(
                            "For non-carcinogens AT equals the exposure duration; for "
                            "carcinogens AT equals a full lifetime",
                            correct=True,
                        ),
                        opt("For carcinogens AT is one year"),
                        opt("AT is never used for carcinogens"),
                    ),
                    "Cancer dose is averaged over a lifetime; non-cancer dose over the "
                    "actual exposure period.",
                ),
                q(
                    "What is a completed exposure pathway?",
                    (
                        opt("Any place a chemical is detected"),
                        opt(
                            "A pathway with all links present: source, release, medium, "
                            "point of contact and an exposed population",
                            correct=True,
                        ),
                        opt("A pathway that has been remediated"),
                        opt("Only an inhalation route"),
                    ),
                    "If any link is missing the pathway is incomplete and contributes no exposure.",
                ),
            ),
        ),
        # -- 5. Carcinogenic and non-carcinogenic risk -----------------
        _t(
            "Carcinogenic and non-carcinogenic risk",
            "11 min",
            """# Carcinogenic and non-carcinogenic risk

Risk characterization for human health splits along the same line as
dose-response: **non-carcinogenic** (threshold) effects use a ratio, and
**carcinogenic** (non-threshold) effects use a probability.

**Non-carcinogenic risk** uses the **Hazard Quotient (HQ)** - the
estimated dose divided by the safe dose:

```text
HQ = CDI / RfD

HQ <= 1  : exposure is at or below the reference dose - unlikely harm
HQ >  1  : exposure exceeds the safe dose - potential concern

Example:
  CDI = 0.00137 mg per kg per day
  RfD = 0.05   mg per kg per day
  HQ  = 0.00137 / 0.05 = 0.027   (well below 1 - acceptable)
```

When several substances act on the same target, their HQs are summed into
a **Hazard Index (HI)**; an HI above 1 flags concern even if no single HQ
does.

**Carcinogenic risk** estimates the *incremental lifetime probability* of
cancer from the exposure, using the slope factor:

```text
Risk = LADD x SF        (low-dose linear form)

LADD = lifetime average daily dose (mg per kg per day)
SF   = slope factor (per mg per kg per day)

Example:
  LADD = 0.0002 mg per kg per day
  SF   = 0.5   per mg per kg per day
  Risk = 0.0002 x 0.5 = 1 x 10^-4

Interpretation: 1 extra cancer case per 10000 people so exposed.
```

Regulators judge cancer risk against an **acceptable range**, commonly
**1 x 10^-6 to 1 x 10^-4** (one extra case per million to per ten
thousand). CONAMA and state agencies in Brazil use similar targets for
contaminated-land intervention values.

```mermaid
graph TD
    CDI["Estimated dose CDI or LADD"] --> TYPE{"Carcinogen"}
    TYPE -->|"no"| HQ["HQ equals CDI over RfD"]
    TYPE -->|"yes"| RISK["Risk equals LADD times SF"]
    HQ --> HI["Sum to hazard index"]
    RISK --> RANGE["Compare to 1e-6 to 1e-4"]
    HI --> DECIDE["Management decision"]
    RANGE --> DECIDE
```

A small Python snippet combining both for one contaminant:

```python
def health_risk(cdi, rfd, ladd, slope_factor):
    hazard_quotient = cdi / rfd
    cancer_risk = ladd * slope_factor
    return {
        "HQ": hazard_quotient,
        "non_cancer_concern": hazard_quotient > 1,
        "cancer_risk": cancer_risk,
        "cancer_concern": cancer_risk > 1e-4,
    }

# health_risk(0.00137, 0.05, 0.0002, 0.5)
# -> HQ 0.027 (ok), cancer_risk 1e-4 (upper edge of range)
```

Remember: HQ (dose over safe dose) for threshold effects, sum to HI;
probability (dose times slope factor) for carcinogens, judged against 1
in a million to 1 in ten thousand.
""",
        ),
        quiz_lesson(
            "Quiz: Carcinogenic and non-carcinogenic risk",
            (
                q(
                    "How is the non-carcinogenic Hazard Quotient calculated and interpreted?",
                    (
                        opt("CDI times RfD; any value is acceptable"),
                        opt(
                            "HQ = CDI / RfD; an HQ at or below 1 suggests unlikely harm, "
                            "above 1 flags potential concern",
                            correct=True,
                        ),
                        opt("RfD divided by CDI; higher is safer"),
                        opt("CDI times the slope factor"),
                    ),
                    "The hazard quotient compares the estimated dose to the safe reference dose.",
                ),
                q(
                    "How is incremental carcinogenic risk estimated?",
                    (
                        opt("By dividing the dose by the RfD"),
                        opt(
                            "Risk = lifetime average daily dose x slope factor, giving "
                            "an incremental lifetime probability of cancer",
                            correct=True,
                        ),
                        opt("By counting detected molecules"),
                        opt("By summing hazard quotients"),
                    ),
                    "The slope factor converts lifetime dose into an added cancer probability.",
                ),
                q(
                    "What cancer-risk range do regulators commonly treat as acceptable?",
                    (
                        opt("1 x 10^-1 to 1 x 10^0"),
                        opt("Exactly zero, always"),
                        opt(
                            "About 1 x 10^-6 to 1 x 10^-4 - one extra case per million "
                            "to per ten thousand exposed",
                            correct=True,
                        ),
                        opt("Any value below 1.0"),
                    ),
                    "This target range underlies EPA and CONAMA intervention values.",
                ),
            ),
        ),
        # -- 6. Ecological risk assessment -----------------------------
        _t(
            "Ecological risk assessment",
            "10 min",
            """# Ecological risk assessment

**Ecological risk assessment (ERA)** asks the same questions as human
health assessment but for non-human receptors - populations, communities
and ecosystems. The valued attributes to protect (fish populations,
pollinators, water quality) are called **assessment endpoints**, and the
measurable proxies for them are **measurement endpoints**.

ERA follows a parallel structure: **problem formulation** (what to
protect and the conceptual model), **analysis** (characterizing exposure
and effects), and **risk characterization**. Effects data come from
ecotoxicology tests reported as an **LC50** (concentration lethal to 50
percent of test organisms), **EC50** (effect concentration), or **NOEC**
(no observed effect concentration).

The screening-level metric mirrors the hazard quotient - the **Risk
Quotient (RQ)**:

```text
RQ = PEC / PNEC

PEC  = predicted (or measured) environmental concentration
PNEC = predicted no-effect concentration
     = toxicity endpoint / assessment factor

RQ <= 1 : acceptable at screening level
RQ >  1 : potential ecological risk - refine or manage

Example (a pesticide in a stream):
  LC50 (fish) = 1.2 mg per L
  assessment factor = 1000 (lab-to-field extrapolation)
  PNEC = 1.2 / 1000 = 0.0012 mg per L
  PEC  = 0.003 mg per L (modeled runoff)
  RQ   = 0.003 / 0.0012 = 2.5   (> 1 - risk indicated)
```

Because a single number hides variability, higher-tier ERA uses the
**Species Sensitivity Distribution (SSD)**: fit a distribution to many
species' toxicity values and read off the **HC5**, the concentration
protective of 95 percent of species. It is more realistic than protecting
only the average or a single test species.

```mermaid
graph TD
    PF["Problem formulation endpoints"] --> EXP["Exposure PEC"]
    PF --> EFF["Effects PNEC from tests"]
    EXP --> RQ["Risk quotient PEC over PNEC"]
    EFF --> RQ
    RQ --> CHAR["Ecological risk characterization"]
    CHAR --> MANAGE["Manage or refine with SSD"]
```

ERA also weighs **bioaccumulation and biomagnification** (from the
toxicology lesson) because top predators integrate exposure across the
food web, and it considers **community-level** effects (diversity,
function) that no single-species test captures. In Brazil, CONAMA
resolutions on water quality set class-based limits that function as
protective concentrations for aquatic life.

Remember: ERA protects populations and ecosystems, not individuals. The
screening metric is RQ = PEC / PNEC, and the SSD-derived HC5 gives a more
realistic, community-protective benchmark.
""",
        ),
        quiz_lesson(
            "Quiz: Ecological risk assessment",
            (
                q(
                    "What is the screening-level Risk Quotient in ecological risk assessment?",
                    (
                        opt("The lethal dose to a single organism"),
                        opt(
                            "RQ = PEC / PNEC - predicted environmental concentration "
                            "over predicted no-effect concentration; above 1 indicates "
                            "potential risk",
                            correct=True,
                        ),
                        opt("The number of species in the ecosystem"),
                        opt("The slope factor for wildlife"),
                    ),
                    "The RQ mirrors the human-health hazard quotient at the ecosystem level.",
                ),
                q(
                    "What is an assessment endpoint?",
                    (
                        opt("The last chemical measured in a survey"),
                        opt(
                            "The valued ecological attribute to be protected, such as a "
                            "fish population or water quality",
                            correct=True,
                        ),
                        opt("The concentration lethal to half the organisms"),
                        opt("The end of the exposure pathway"),
                    ),
                    "Measurement endpoints are the measurable proxies for the "
                    "assessment endpoints we want to protect.",
                ),
                q(
                    "What does the HC5 from a Species Sensitivity Distribution represent?",
                    (
                        opt("The concentration lethal to all species"),
                        opt(
                            "The concentration protective of 95 percent of species - a "
                            "more realistic, community-level benchmark",
                            correct=True,
                        ),
                        opt("The average body weight of test organisms"),
                        opt("The highest measured concentration in the field"),
                    ),
                    "The SSD fits many species' toxicity data and reads off a hazardous "
                    "concentration for a small, protected fraction.",
                ),
            ),
        ),
        # -- 7. Risk characterization and uncertainty ------------------
        _t(
            "Risk characterization and uncertainty",
            "11 min",
            """# Risk characterization and uncertainty

**Risk characterization** is the fourth step: it integrates the toxicity
(dose-response) and exposure results into a statement of risk, and - just
as importantly - describes the **confidence and limitations** behind that
number. A risk estimate without its uncertainty is a false precision.

A crucial distinction:

- **Variability** - real, irreducible differences across the population
  (people drink different amounts of water, weigh different amounts). More
  data describes it better but cannot remove it.
- **Uncertainty** - our lack of knowledge (an imperfect model, a small
  toxicity study, an estimated concentration). More or better data *can*
  reduce it.

Deterministic assessments handle this with **conservative point
estimates** - RME intake, upper-bound slope factors - so the answer errs
toward protection. Because multiplying several upper bounds can
**compound conservatism**, higher-tier assessments use **probabilistic
(Monte Carlo)** methods: represent each input as a distribution, sample
repeatedly, and produce a distribution of risk rather than one number.

```python
import numpy as np

rng = np.random.default_rng(42)
n = 100_000

# each input as a distribution (variability + uncertainty)
conc = rng.lognormal(mean=np.log(0.05), sigma=0.5, size=n)   # mg per L
intake = rng.triangular(1.0, 2.0, 3.0, size=n)               # L per day
body_wt = rng.normal(70, 12, size=n).clip(40, 120)           # kg
slope = 0.5                                                   # per mg per kg per day

ladd = (conc * intake * 350 * 30) / (body_wt * 25550)
risk = ladd * slope

p50, p95 = np.percentile(risk, [50, 95])
print(f"median risk {p50:.2e}, 95th percentile {p95:.2e}")
# e.g. median ~4e-5, 95th percentile ~1e-4: shows the spread, not one value
```

Reporting the **50th and 95th percentiles** tells a decision-maker both a
typical and a reasonably protective figure, and a **sensitivity
analysis** shows which inputs drive the result - so you know where better
data would matter most.

```mermaid
graph TD
    TOX["Dose response toxicity value"] --> RC["Risk characterization"]
    EXP["Exposure estimate"] --> RC
    RC --> POINT["Point estimate risk"]
    RC --> DIST["Probabilistic distribution"]
    DIST --> PCTL["Report percentiles"]
    RC --> UNC["State variability and uncertainty"]
    UNC --> SENS["Sensitivity analysis"]
```

Good risk characterization is **transparent, clear, consistent and
reasonable** (the EPA "TCCR" principle): state the assumptions, the
conservatism, and what would change the answer.

Remember: characterization combines toxicity and exposure into a risk
number and qualifies it - separating irreducible variability from
reducible uncertainty, and reporting a range rather than false precision.
""",
        ),
        quiz_lesson(
            "Quiz: Risk characterization and uncertainty",
            (
                q(
                    "What is the difference between variability and uncertainty?",
                    (
                        opt("They are synonyms"),
                        opt(
                            "Variability is real, irreducible population difference; "
                            "uncertainty is lack of knowledge that better data can "
                            "reduce",
                            correct=True,
                        ),
                        opt("Variability applies only to carcinogens"),
                        opt("Uncertainty can never be reduced"),
                    ),
                    "More data describes variability better but only reduces uncertainty.",
                ),
                q(
                    "Why use probabilistic (Monte Carlo) methods instead of stacking "
                    "conservative point estimates?",
                    (
                        opt("They are faster to compute by hand"),
                        opt(
                            "Multiplying several upper-bound values compounds "
                            "conservatism; sampling input distributions yields a "
                            "realistic distribution of risk",
                            correct=True,
                        ),
                        opt("They remove the need for toxicity data"),
                        opt("They always give a lower, less protective answer"),
                    ),
                    "Monte Carlo shows the spread and lets you report percentiles "
                    "rather than one compounded worst case.",
                ),
                q(
                    "What does a sensitivity analysis tell the assessor?",
                    (
                        opt("The exact true risk with no error"),
                        opt(
                            "Which input variables drive the result most, so you know "
                            "where better data would matter most",
                            correct=True,
                        ),
                        opt("The legal acceptable risk level"),
                        opt("The body weight of the population"),
                    ),
                    "It ranks inputs by influence, guiding where to invest in reducing "
                    "uncertainty.",
                ),
            ),
        ),
        # -- 8. Risk communication and management ----------------------
        _t(
            "Risk communication and management",
            "10 min",
            """# Risk communication and management

Assessment produces numbers; **risk management** decides what to do about
them, and **risk communication** makes both understandable to the people
affected. These are deliberately kept separate from assessment: the
science should describe risk objectively, while management weighs that
science against costs, benefits, feasibility, law and values.

**Risk management** integrates the risk estimate with other factors -
technical feasibility, economics, equity, and statute - to choose an
action: set a cleanup or discharge limit, require treatment, restrict
land use, or accept the risk with monitoring. The classic hierarchy of
controls is to **eliminate**, then **substitute**, then apply
**engineering controls**, then **administrative controls**, and only last
rely on personal protection - reduce the hazard or the exposure at the
most effective point.

**Risk communication** is the two-way exchange of information about risk.
Its guiding ideas (from Sandman and the US EPA):

- **Perceived risk is not just the numbers.** People react to *outrage*
  factors - is the risk voluntary, familiar, controllable, fair, dreaded?
  A small involuntary risk can alarm more than a large voluntary one.
- **Communicate early, honestly and clearly.** Acknowledge uncertainty
  rather than hide it; trust, once lost, is very hard to regain.
- **Listen.** Treat the public as a partner, address their actual
  concerns, and be transparent about who bears the risk and who benefits.

A useful framing is *perceived risk = hazard + outrage*: managing a
controversy often means addressing outrage (fairness, control, dread), not
only the hazard number.

```mermaid
graph LR
    ASSESS["Risk assessment science"] --> MGMT["Risk management"]
    CONTEXT["Cost feasibility law equity"] --> MGMT
    MGMT --> ACTION["Limits controls remediation"]
    MGMT --> COMM["Risk communication"]
    COMM --> PUBLIC["Affected public dialogue"]
    PUBLIC --> MGMT
```

A worked management trade-off - **cost-effectiveness** of a cleanup:

```text
Cost per case avoided = remediation cost / cancer cases avoided

Cases avoided = risk reduction x exposed population
  risk reduction = 1e-4 - 1e-5 = 9e-5
  population     = 50000
  cases avoided  = 9e-5 x 50000 = 4.5 cases

  remediation cost = 9,000,000 (currency units)
  cost per case    = 9,000,000 / 4.5 = 2,000,000 per case avoided

This figure informs - but does not by itself decide - the action;
equity, dread, legal limits and public input all weigh in.
```

Standards frameworks tie it together: **ISO 14001** environmental
management systems and **ISO 31000** risk management give organizations a
repeatable plan-do-check-act cycle for identifying, treating and
communicating environmental risk over time.

Remember: assessment says how big the risk is; management decides what to
do given costs, law and values; communication is an honest two-way
dialogue that respects outrage as well as numbers.
""",
        ),
        quiz_lesson(
            "Quiz: Risk communication and management",
            (
                q(
                    "Why are risk assessment and risk management kept separate?",
                    (
                        opt("Because they use different software"),
                        opt(
                            "Assessment describes risk objectively; management weighs "
                            "that science against costs, feasibility, law and values to "
                            "decide action",
                            correct=True,
                        ),
                        opt("Because management ignores the science"),
                        opt("They are not separate; they are the same step"),
                    ),
                    "Keeping the science objective and the decision explicit about "
                    "values improves both.",
                ),
                q(
                    "In risk communication, what does 'perceived risk = hazard + outrage' capture?",
                    (
                        opt("That perception depends only on the hazard number"),
                        opt(
                            "That people also react to outrage factors - voluntariness, "
                            "control, fairness, dread - not only the calculated hazard",
                            correct=True,
                        ),
                        opt("That outrage can be ignored"),
                        opt("That hazard is irrelevant to the public"),
                    ),
                    "A small involuntary, dreaded risk can alarm more than a larger "
                    "voluntary one; address outrage, not only numbers.",
                ),
                q(
                    "In the hierarchy of controls, which approach is most effective?",
                    (
                        opt("Personal protective equipment first"),
                        opt("Administrative controls first"),
                        opt(
                            "Eliminate or substitute the hazard first, before relying on "
                            "engineering, administrative controls or personal protection",
                            correct=True,
                        ),
                        opt("Accept the risk and monitor only"),
                    ),
                    "Reducing hazard or exposure at the source is more effective than "
                    "controls that depend on human behavior.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the essential difference between hazard and risk?",
                    (
                        opt("They are identical concepts"),
                        opt(
                            "Hazard is the intrinsic ability to cause harm; risk is the "
                            "probability of harm given real exposure (Risk = Hazard x "
                            "Exposure)",
                            correct=True,
                        ),
                        opt("Hazard is a probability, risk is a property"),
                        opt("Risk applies only to carcinogens"),
                    ),
                    "No exposure, no risk - however hazardous the agent.",
                ),
                q(
                    "What are the four steps of the risk assessment framework?",
                    (
                        opt("Sampling, testing, reporting, archiving"),
                        opt(
                            "Hazard identification, dose-response assessment, exposure "
                            "assessment, risk characterization",
                            correct=True,
                        ),
                        opt("Plan, do, check, act"),
                        opt("Detect, measure, model, publish"),
                    ),
                    "These four steps are used by EPA, WHO and CONAMA/ABNT alike.",
                ),
                q(
                    "How is a Reference Dose (RfD) obtained for a threshold effect?",
                    (
                        opt("NOAEL multiplied by the slope factor"),
                        opt(
                            "Point of departure (NOAEL or BMD) divided by the product of "
                            "uncertainty factors",
                            correct=True,
                        ),
                        opt("The highest tested dose, unadjusted"),
                        opt("The lifetime average daily dose"),
                    ),
                    "Uncertainty factors cover interspecies and human variability and data gaps.",
                ),
                q(
                    "Which equation gives the chronic daily intake from drinking water?",
                    (
                        opt("CDI = RfD / SF"),
                        opt(
                            "CDI = (C x IR x EF x ED) / (BW x AT)",
                            correct=True,
                        ),
                        opt("CDI = PEC / PNEC"),
                        opt("CDI = NOAEL x uncertainty factor"),
                    ),
                    "Concentration times contact, normalized by body weight and averaging time.",
                ),
                q(
                    "How is non-carcinogenic risk expressed and interpreted?",
                    (
                        opt("As a slope factor; higher is safer"),
                        opt(
                            "As a hazard quotient HQ = CDI / RfD; at or below 1 is "
                            "unlikely to harm, above 1 flags concern",
                            correct=True,
                        ),
                        opt("As a lifetime cancer probability"),
                        opt("As a bioconcentration factor"),
                    ),
                    "Multiple HQs on the same target sum into a hazard index.",
                ),
                q(
                    "How is incremental lifetime carcinogenic risk estimated?",
                    (
                        opt("CDI divided by the RfD"),
                        opt(
                            "Lifetime average daily dose multiplied by the slope factor, "
                            "judged against about 1e-6 to 1e-4",
                            correct=True,
                        ),
                        opt("The LC50 of the most sensitive species"),
                        opt("The hazard index summed across chemicals"),
                    ),
                    "The slope factor turns lifetime dose into an added cancer probability.",
                ),
                q(
                    "In ecological risk assessment, what is the screening Risk Quotient?",
                    (
                        opt("The number of exposed people"),
                        opt(
                            "RQ = PEC / PNEC; above 1 indicates potential ecological risk",
                            correct=True,
                        ),
                        opt("The RfD divided by the CDI"),
                        opt("The cost per cancer case avoided"),
                    ),
                    "PNEC comes from a toxicity endpoint (LC50, NOEC) divided by an "
                    "assessment factor.",
                ),
                q(
                    "What does a Species Sensitivity Distribution HC5 protect?",
                    (
                        opt("The single most sensitive individual organism"),
                        opt(
                            "95 percent of species - a community-level protective concentration",
                            correct=True,
                        ),
                        opt("Only the test species used in the lab"),
                        opt("The top predator alone"),
                    ),
                    "The SSD uses many species' data rather than a single test species.",
                ),
                q(
                    "In risk characterization, how do variability and uncertainty differ?",
                    (
                        opt("They are the same and both irreducible"),
                        opt(
                            "Variability is real population difference (irreducible); "
                            "uncertainty is lack of knowledge that better data can "
                            "reduce",
                            correct=True,
                        ),
                        opt("Uncertainty is real difference; variability is ignorance"),
                        opt("Neither affects the risk estimate"),
                    ),
                    "Monte Carlo methods represent both and report a distribution of "
                    "risk rather than false precision.",
                ),
                q(
                    "What does the framing 'perceived risk = hazard + outrage' mean for "
                    "risk communication?",
                    (
                        opt("Only the hazard number matters to the public"),
                        opt(
                            "People also react to outrage factors like fairness, "
                            "control and dread, so communication must address these, not "
                            "only the calculated hazard",
                            correct=True,
                        ),
                        opt("Outrage should be dismissed as irrational"),
                        opt("Communication should hide uncertainty"),
                    ),
                    "Managing a controversy often means addressing outrage as well as "
                    "the hazard, with honest two-way dialogue.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_RISK_ASSESSMENT_COURSES: tuple[SeedCourse, ...] = (_ENVIRONMENTAL_RISK_ASSESSMENT,)
