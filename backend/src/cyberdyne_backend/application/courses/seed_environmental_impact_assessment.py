"""Academy seed content - Environmental Impact Assessment and Licensing.

Environmental Impact Assessment (EIA) is the process that decides whether
and how a project proceeds. This course walks the full licensing pathway:
screening and scoping, baseline environmental diagnosis, impact
identification with matrices, significance evaluation, mitigation and
compensation, monitoring programs, and public participation. Every lesson
is a direct explanation grounded in real practice (CONAMA, ABNT NBR, EPA
NEPA, ISO 14001) with a mermaid diagram and a worked matrix, checklist or
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


_ENVIRONMENTAL_IMPACT_ASSESSMENT = SeedCourse(
    slug="environmental-impact-assessment",
    title="Environmental Impact Assessment & Licensing",
    description=(
        "The process that decides whether and how projects proceed: screening "
        "and scoping, baseline diagnosis, impact matrices, significance, "
        "mitigation, and public participation. Each lesson pairs a direct "
        "explanation grounded in real practice (CONAMA, ABNT NBR, EPA NEPA, "
        "ISO 14001) with a mermaid diagram and a worked matrix, checklist or "
        "calculation."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Impact Assessment and Licensing

**Environmental Impact Assessment (EIA)** is not paperwork you file at the
end - it is the structured process that decides, before a shovel hits the
ground, whether a project should proceed and under what conditions. A new
highway, dam, port, mine or industrial plant can reshape ecosystems and
communities for decades. EIA makes those consequences visible and forces
them into the decision.

This course follows the process the way a licensing authority does, from
the first screening question to the public hearing where affected people
have their say.

The approach is **concrete**: every lesson explains one stage directly,
shows it with a real example (an impact matrix, a scoping checklist, or a
significance calculation), and draws the stage as a diagram. After each
lesson there is a short quiz; at the end, a final quiz covers the whole
course.

What you will build understanding for, in order:

1. **The EIA process and licensing stages** - the map from idea to permit
2. **Screening and scoping** - does it need EIA, and on what to focus
3. **Baseline environmental diagnosis** - the "before" picture
4. **Impact identification and matrices** - linking actions to effects
5. **Significance evaluation** - which impacts actually matter
6. **Mitigation and compensation measures** - the mitigation hierarchy
7. **Environmental programs and monitoring** - proving it during operation
8. **Public participation and hearings** - the community's role

Frameworks referenced throughout - Brazil's **CONAMA** resolutions
(01/1986, 237/1997), **ABNT NBR** standards, the US **NEPA**, and **ISO
14001** environmental management - are named to ground the ideas, but the
focus is on understanding the process well enough to run it.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is Environmental Impact Assessment, fundamentally?",
                    (
                        opt("A report filed after a project is finished"),
                        opt("A tax paid on industrial emissions"),
                        opt(
                            "A structured process that evaluates a project's likely "
                            "environmental consequences before it is approved, to inform "
                            "whether and how it proceeds",
                            correct=True,
                        ),
                        opt("A software package for drawing maps"),
                    ),
                    "EIA is a decision-support process carried out before approval, not "
                    "an after-the-fact formality.",
                ),
                q(
                    "How is this course structured?",
                    (
                        opt("Only theory, with no examples"),
                        opt(
                            "Each stage is explained directly, with a matrix, checklist "
                            "or calculation and a diagram, followed by a short quiz",
                            correct=True,
                        ),
                        opt("It only covers legal citations"),
                        opt("It is a single long lecture with no quizzes"),
                    ),
                    "Explanation plus a concrete example plus a diagram plus a checkpoint "
                    "quiz per lesson, then a final quiz.",
                ),
            ),
        ),
        # -- 1. EIA process and licensing stages -----------------------
        _t(
            "The EIA process and licensing stages",
            "10 min",
            """# The EIA process and licensing stages

EIA is a **sequence of stages**, and environmental **licensing** is the
administrative track that runs alongside it. In Brazil, CONAMA Resolution
**237/1997** defines three licenses issued in order, each answering a
different question:

- **Preliminary License (LP)** - is the project viable, in this location,
  in principle? Granted at the planning phase, based on the EIA. It
  approves the concept and sets the conditions to design against.
- **Installation License (LI)** - may construction begin? Granted once the
  detailed environmental programs are approved. It authorizes building.
- **Operation License (LO)** - may the project run? Granted after checking
  that the required measures and programs are in place. It permits
  operation, and is renewed periodically.

The technical study behind the LP is the **EIA/RIMA**: the **EIA** is the
full technical assessment; the **RIMA** (Environmental Impact Report) is
its plain-language public summary.

The overall flow - proposal, screening, scoping, baseline, impact
prediction, significance, mitigation, reporting, review, decision, then
monitoring - is universal. NEPA in the US and EU Directive 2011/92
describe the same logic under different names.

```mermaid
graph LR
    PROP["Project proposal"] --> SCR["Screening"]
    SCR --> SCOPE["Scoping"]
    SCOPE --> BASE["Baseline diagnosis"]
    BASE --> PRED["Impact prediction"]
    PRED --> SIG["Significance evaluation"]
    SIG --> MIT["Mitigation and programs"]
    MIT --> RIMA["EIA and RIMA report"]
    RIMA --> REV["Public review and decision"]
    REV --> MON["Monitoring during operation"]
```

The three licenses map onto that flow:

```text
Planning phase   --> EIA/RIMA study --> Preliminary License (LP)
Detailed design  --> Environmental programs --> Installation License (LI)
Ready to operate --> Compliance check --> Operation License (LO)
```

Remember: EIA is the study; licensing is the permit sequence. Each license
gates the next phase, so an impact missed early is far more expensive to
fix later.
""",
        ),
        quiz_lesson(
            "Quiz: The EIA process and licensing stages",
            (
                q(
                    "Under CONAMA 237/1997, what are the three environmental licenses, in order?",
                    (
                        opt("Draft, Final, Renewal"),
                        opt(
                            "Preliminary License (LP), Installation License (LI), "
                            "Operation License (LO)",
                            correct=True,
                        ),
                        opt("Federal, State, Municipal"),
                        opt("Screening, Scoping, Monitoring"),
                    ),
                    "LP approves viability, LI authorizes construction, LO permits "
                    "operation - each gates the next phase.",
                ),
                q(
                    "What is the difference between the EIA and the RIMA?",
                    (
                        opt("They are two names for the same document"),
                        opt(
                            "The EIA is the full technical assessment; the RIMA is its "
                            "plain-language public summary",
                            correct=True,
                        ),
                        opt("The RIMA is written before the EIA"),
                        opt("The EIA is only for federal projects"),
                    ),
                    "RIMA (Environmental Impact Report) exists so the public can "
                    "understand the technical EIA.",
                ),
                q(
                    "At which phase is the Preliminary License (LP) granted?",
                    (
                        opt("After the project is already operating"),
                        opt("Midway through construction"),
                        opt(
                            "At the planning phase, based on the EIA, to confirm the "
                            "project is viable in principle and set conditions",
                            correct=True,
                        ),
                        opt("Only after monitoring data is collected"),
                    ),
                    "The LP is the earliest license; it approves the concept and "
                    "location before detailed design.",
                ),
            ),
        ),
        # -- 2. Screening and scoping ----------------------------------
        _t(
            "Screening and scoping",
            "10 min",
            """# Screening and scoping

Not every project needs a full EIA, and no EIA can study *everything*. The
first two stages solve exactly those two problems.

**Screening** asks: *does this project require a full EIA at all?* CONAMA
Resolution **01/1986** lists activity types that always require EIA/RIMA -
highways, railways, ports, airports, dams, large industrial plants,
mining, landfills. Two common screening approaches:

- **List-based (positive list)** - if the activity type and size cross a
  legal threshold, EIA is mandatory. Simple and predictable.
- **Case-by-case** - a preliminary check of location sensitivity and
  likely impact magnitude decides. Flexible but needs judgment.

Projects below the thresholds may need only a **simplified study** (in
Brazil, a RAS or PCA) rather than a full EIA/RIMA.

**Scoping** then asks: *given that we need an EIA, what should it focus
on?* Its job is to identify the **significant issues** and the **spatial
and temporal boundaries** of study, and to exclude the trivial - so effort
goes where impacts matter. Scoping defines the **area of influence**:

- **Direct area of influence (ADA/AID)** - where impacts are felt directly.
- **Indirect area of influence (AII)** - the wider zone of secondary effects.

A scoping checklist keeps the study bounded:

```text
SCOPING CHECKLIST (highway segment)
[x] Valued components: surface water, native vegetation, fauna corridors,
    air quality, noise, affected communities
[x] Spatial boundary: 500 m each side (direct), sub-basin (indirect)
[x] Temporal boundary: 24-month construction + 20-year operation
[x] Key concerns flagged: river crossing, protected-area edge, resettlement
[ ] Excluded as non-significant: distant landscape views, minor traffic
    signage
[x] Baseline data needed: 12 months of water quality, one wet + one dry season
```

```mermaid
graph TD
    PROJ["Proposed project"] --> Q1{"On mandatory EIA list"}
    Q1 -->|"yes"| FULL["Full EIA required"]
    Q1 -->|"no"| Q2{"Sensitive location or large scale"}
    Q2 -->|"yes"| CASE["Case by case study"]
    Q2 -->|"no"| SIMPLE["Simplified study"]
    FULL --> SCOPE["Scoping sets focus and boundaries"]
```

Remember: screening decides *whether*, scoping decides *what* - together
they keep the EIA proportionate and focused.
""",
        ),
        quiz_lesson(
            "Quiz: Screening and scoping",
            (
                q(
                    "What question does screening answer?",
                    (
                        opt("Which mitigation measures to apply"),
                        opt(
                            "Whether the project requires a full EIA at all",
                            correct=True,
                        ),
                        opt("How large the public hearing should be"),
                        opt("What the baseline water quality is"),
                    ),
                    "Screening is the gate that decides if a full EIA is needed, often "
                    "via a mandatory-activity list or case-by-case check.",
                ),
                q(
                    "What is the purpose of scoping?",
                    (
                        opt("To grant the Operation License"),
                        opt(
                            "To identify the significant issues and the spatial and "
                            "temporal boundaries of study, so effort focuses where "
                            "impacts matter",
                            correct=True,
                        ),
                        opt("To collect ten years of monitoring data"),
                        opt("To write the plain-language public summary"),
                    ),
                    "Scoping bounds the study: it flags the valued components and study "
                    "area and excludes the trivial.",
                ),
                q(
                    "What is the 'area of influence' defined during scoping?",
                    (
                        opt("The office where the study is written"),
                        opt("The budget available for the assessment"),
                        opt(
                            "The direct and indirect geographic zones where the "
                            "project's impacts are expected to be felt",
                            correct=True,
                        ),
                        opt("The list of team members"),
                    ),
                    "Direct area (impacts felt directly) plus indirect area (wider "
                    "secondary effects) bound the assessment spatially.",
                ),
            ),
        ),
        # -- 3. Baseline environmental diagnosis -----------------------
        _t(
            "Baseline environmental diagnosis",
            "10 min",
            """# Baseline environmental diagnosis

The **baseline diagnosis** (in Brazil, the *diagnostico ambiental*) is the
"before" picture: a characterization of the environment as it is *without*
the project. Everything later depends on it - you cannot judge a change if
you never measured the starting point.

The diagnosis is organized into three interacting **environments**:

- **Physical environment** - climate, air quality, geology, soils, surface
  and groundwater, noise. Governed by standards like CONAMA 357/2005
  (water classes) and the WHO/EPA air-quality guidelines.
- **Biotic environment** - flora, fauna, ecosystems, protected areas,
  species of conservation concern, ecological corridors.
- **Socioeconomic environment** - population, land use, economy, culture,
  vulnerable groups, archaeological and heritage sites.

Two disciplines make a baseline credible:

- **Represent natural variability** - sample across at least one **wet and
  one dry season**, because a single measurement can badly mislead.
- **Distinguish trend from noise** - many indicators drift on their own;
  the baseline must capture that so later changes are attributed correctly.

A worked example - summarizing a water-quality parameter into a baseline
statistic and comparing it to the legal limit:

```python
import numpy as np

# Dissolved oxygen (mg/L), one sampling campaign, station R1
do_samples = np.array([7.8, 8.1, 6.9, 7.4, 8.0, 7.2, 6.7, 7.6])

baseline_mean = do_samples.mean()
p10 = np.percentile(do_samples, 10)      # a conservative low value
conama_class2_min = 5.0                   # CONAMA 357/2005, Class 2 river

print(round(baseline_mean, 2), round(p10, 2))   # 7.46  6.76
print("compliant" if p10 >= conama_class2_min else "breach")  # compliant
```

The baseline is not just numbers - it is also **maps and inventories**:
land-cover maps, species lists, a census of affected households. Remote
sensing and GIS increasingly supply the physical and land-use layers.

```mermaid
graph TD
    SITE["Study area"] --> PHYS["Physical environment"]
    SITE --> BIO["Biotic environment"]
    SITE --> SOCIO["Socioeconomic environment"]
    PHYS --> DATA["Sampling maps and inventories"]
    BIO --> DATA
    SOCIO --> DATA
    DATA --> REF["Reference condition without project"]
```

Remember: the baseline is the reference you measure every predicted impact
against - sample the natural variability, or your later comparisons are
meaningless.
""",
        ),
        quiz_lesson(
            "Quiz: Baseline environmental diagnosis",
            (
                q(
                    "What does the baseline environmental diagnosis characterize?",
                    (
                        opt("The environment after the project is complete"),
                        opt(
                            "The environment as it is without the project - the "
                            "reference condition against which impacts are judged",
                            correct=True,
                        ),
                        opt("Only the project's financial cost"),
                        opt("The list of required licenses"),
                    ),
                    "The baseline is the 'before' picture; every predicted impact is "
                    "measured relative to it.",
                ),
                q(
                    "The three environments of a baseline diagnosis are:",
                    (
                        opt("Federal, state, and municipal"),
                        opt("Air, land, and sea"),
                        opt(
                            "Physical, biotic, and socioeconomic",
                            correct=True,
                        ),
                        opt("Past, present, and future"),
                    ),
                    "Physical (climate, water, soil), biotic (flora, fauna, ecosystems), "
                    "socioeconomic (people, land use, heritage).",
                ),
                q(
                    "Why should baseline sampling cover both a wet and a dry season?",
                    (
                        opt("To make the report longer"),
                        opt(
                            "To represent natural variability, so a single measurement "
                            "at one time does not mislead the assessment",
                            correct=True,
                        ),
                        opt("Because licenses are issued only in the dry season"),
                        opt("To avoid taking any measurements at all"),
                    ),
                    "Many indicators vary strongly by season; capturing that variability "
                    "makes later change attribution reliable.",
                ),
            ),
        ),
        # -- 4. Impact identification and matrices ---------------------
        _t(
            "Impact identification and matrices",
            "11 min",
            """# Impact identification and matrices

With a baseline in hand, the core analytical step is **impact
identification**: linking each **project action** to the **environmental
components** it affects. An impact is a *change* in a component caused by an
action - and the classic tool for finding them systematically is the
**interaction matrix**.

The **Leopold matrix** (1971) is the archetype: project actions run down
one axis, environmental and social factors across the other. Each cell
where an action plausibly affects a factor is marked, so no interaction is
forgotten. A simplified example for a small dam:

```text
LEOPOLD-STYLE INTERACTION MATRIX  (X = interaction to assess)
                        | Water | Fish  | Native | Local  | Local
Action                  | qual. | fauna | veg.   | jobs   | noise
------------------------|-------|-------|--------|--------|-------
Vegetation clearing     |   X   |       |   X    |        |
Excavation and earthwork|   X   |       |   X    |   X    |   X
River impoundment       |   X   |   X   |   X    |        |
Workforce influx        |       |       |        |   X    |   X
Reservoir operation     |   X   |   X   |        |   X    |
```

Impacts are then **classified** by their attributes - this vocabulary
recurs everywhere:

- **Nature** - positive (beneficial) or negative (adverse).
- **Direct vs indirect** - caused by the action itself, or by a knock-on
  chain (clearing -> erosion -> siltation downstream).
- **Reversible vs irreversible** - can the system recover, or not (species
  extinction is irreversible).
- **Temporary vs permanent**, and **short-, medium- or long-term**.
- **Cumulative** - adding to impacts from other projects in the region.

Beyond the matrix, practitioners use **checklists** (comprehensive but not
causal), **networks** (which trace indirect chains explicitly), and
**overlay maps/GIS** (which show *where* impacts concentrate). The matrix
is favored because it is systematic and hard to leave a gap in.

```mermaid
graph LR
    ACT["Project actions"] --> MATRIX["Interaction matrix"]
    ENV["Environmental components"] --> MATRIX
    MATRIX --> IMP["Identified impacts"]
    IMP --> CLASS["Classify nature reversibility term"]
    CLASS --> DIRECT["Direct impacts"]
    CLASS --> INDIRECT["Indirect and cumulative impacts"]
```

Remember: the matrix guarantees you cross every action against every
component; classification then describes each impact so it can be ranked in
the next stage.
""",
        ),
        quiz_lesson(
            "Quiz: Impact identification and matrices",
            (
                q(
                    "What does an interaction matrix such as the Leopold matrix do?",
                    (
                        opt("Sets the project budget"),
                        opt(
                            "Systematically crosses each project action against each "
                            "environmental component to identify interactions, so none "
                            "are forgotten",
                            correct=True,
                        ),
                        opt("Grants the Operation License"),
                        opt("Measures air quality directly"),
                    ),
                    "Actions on one axis, factors on the other; a marked cell is an "
                    "interaction to assess.",
                ),
                q(
                    "An impact described as 'irreversible' means:",
                    (
                        opt("It only lasts during construction"),
                        opt("It is always positive"),
                        opt(
                            "The affected system cannot recover to its prior state, "
                            "such as the extinction of a species",
                            correct=True,
                        ),
                        opt("It affects only water quality"),
                    ),
                    "Reversibility asks whether the environment can recover; some "
                    "impacts, like extinction, cannot be undone.",
                ),
                q(
                    "What is a cumulative impact?",
                    (
                        opt("An impact that disappears immediately"),
                        opt(
                            "An impact that adds to the effects of other projects or "
                            "activities in the same region",
                            correct=True,
                        ),
                        opt("An impact caused only by noise"),
                        opt("A benefit that offsets a cost"),
                    ),
                    "Cumulative impacts accumulate across multiple projects or over "
                    "time and are easily missed if each project is viewed alone.",
                ),
            ),
        ),
        # -- 5. Significance evaluation --------------------------------
        _t(
            "Significance evaluation",
            "11 min",
            """# Significance evaluation

Identifying impacts is not enough - a study can list dozens. **Significance
evaluation** ranks them, so decision-makers and mitigation effort focus on
what genuinely matters. This is where EIA turns a list into a judgment.

Significance is usually a function of two things:

- **Magnitude** - how large the change is (intensity, extent, duration).
- **Sensitivity / importance** of the receptor - how much the affected
  component matters (a protected species and a common weed differ).

A widely used approach is a **weighted scoring matrix**. Each impact is
scored on several criteria; a weighted sum gives a comparable index:

```text
Significance = w1*Magnitude + w2*Extent + w3*Duration + w4*Reversibility
              (each criterion scored 1 = low, 3 = medium, 5 = high)

Weights:  w1=0.35  w2=0.20  w3=0.20  w4=0.25   (sum = 1.0)
```

A worked calculation for two impacts of a dam:

```python
weights = {"magnitude": 0.35, "extent": 0.20, "duration": 0.20, "reversibility": 0.25}

def significance(scores):
    return round(sum(weights[k] * scores[k] for k in weights), 2)

fish_loss   = {"magnitude": 5, "extent": 3, "duration": 5, "reversibility": 5}
dust_constr = {"magnitude": 3, "extent": 1, "duration": 1, "reversibility": 1}

print(significance(fish_loss))    # 4.65  -> HIGH significance
print(significance(dust_constr))  # 1.70  -> LOW significance
```

Interpreting the index against thresholds (for example: < 2.0 low, 2.0 to
3.5 moderate, > 3.5 high) turns numbers into priorities. The permanent,
irreversible loss of migratory fish scores **high** and demands strong
mitigation; temporary construction dust scores **low** and needs only
routine control.

Two cautions keep scoring honest:

- **Transparency** - state every criterion, weight and threshold. The
  numbers are an aid to judgment, not a substitute for it.
- **Uncertainty** - where prediction is uncertain, say so and apply the
  **precautionary principle**: treat plausible severe impacts seriously
  rather than assuming the best case.

```mermaid
graph TD
    IMP["Identified impact"] --> MAG["Score magnitude"]
    IMP --> EXT["Score extent"]
    IMP --> DUR["Score duration"]
    IMP --> REV["Score reversibility"]
    MAG --> WSUM["Weighted sum"]
    EXT --> WSUM
    DUR --> WSUM
    REV --> WSUM
    WSUM --> RANK["Significance rank low medium high"]
```

Remember: significance turns a long impact list into a priority order -
magnitude times receptor importance, scored transparently, with the
precautionary principle where uncertainty is high.
""",
        ),
        quiz_lesson(
            "Quiz: Significance evaluation",
            (
                q(
                    "Why is significance evaluation necessary after impacts are identified?",
                    (
                        opt("To make the report look scientific"),
                        opt(
                            "To rank the many identified impacts so that decisions and "
                            "mitigation focus on the ones that genuinely matter",
                            correct=True,
                        ),
                        opt("To collect the baseline data again"),
                        opt("To schedule the public hearing"),
                    ),
                    "A study can list dozens of impacts; significance turns the list "
                    "into a priority order.",
                ),
                q(
                    "Significance typically depends on which two factors?",
                    (
                        opt("Project cost and construction time"),
                        opt(
                            "The magnitude of the change and the sensitivity or "
                            "importance of the affected receptor",
                            correct=True,
                        ),
                        opt("The number of pages in the report"),
                        opt("The weather on the sampling day"),
                    ),
                    "A large change to a highly sensitive receptor is far more "
                    "significant than the same change to a robust one.",
                ),
                q(
                    "What does the precautionary principle imply for uncertain but severe impacts?",
                    (
                        opt("Assume the best case and proceed"),
                        opt("Ignore the impact until it happens"),
                        opt(
                            "Take plausible severe impacts seriously despite uncertainty, "
                            "rather than assuming they will not occur",
                            correct=True,
                        ),
                        opt("Cancel every project automatically"),
                    ),
                    "Under uncertainty, the precautionary principle errs on the side of "
                    "caution for plausible serious harm.",
                ),
            ),
        ),
        # -- 6. Mitigation and compensation measures -------------------
        _t(
            "Mitigation and compensation measures",
            "11 min",
            """# Mitigation and compensation measures

Once significant impacts are ranked, the EIA must show how they will be
**managed**. The organizing idea is the **mitigation hierarchy** - apply
the options in order, because it is always better to prevent harm than to
repair it:

1. **Avoid** - change the design, route or timing to prevent the impact
   entirely (reroute a road around a wetland). The strongest option.
2. **Minimize / reduce** - where impact cannot be avoided, shrink it
   (dust suppression, quieter equipment, fish ladders, timing works
   outside breeding season).
3. **Restore / rehabilitate** - repair the affected area after the fact
   (revegetate cleared slopes, recover degraded soil).
4. **Compensate / offset** - for the **residual** impact that remains,
   provide an equivalent gain elsewhere (protect or restore habitat of the
   same type, in Brazil via the *compensacao ambiental* of SNUC Law
   9985/2000).

Each measure is classified as **preventive**, **corrective**,
**mitigating** or **compensatory**, and each is tied to the specific
impact it addresses and to a responsible party.

A worked mapping from impact to measure to residual:

```text
IMPACT                    | HIERARCHY   | MEASURE                     | RESIDUAL
--------------------------|-------------|-----------------------------|----------
Wetland loss (routing)    | Avoid       | Reroute 800 m north          | none
Construction dust         | Minimize    | Water haul roads, cover loads| low
Cleared slope erosion     | Restore     | Revegetate, silt fences      | low
Permanent forest loss 12 ha| Compensate | Protect 24 ha same biome     | offset
```

Note the **offset ratio**: 12 ha lost is compensated with 24 ha protected
(a 2:1 ratio) because protected land is not identical in quality or
certainty to what was lost. Offsets are a last resort, never a licence to
skip avoidance.

Compensation for protected areas in Brazil is calculated as a percentage
of project cost:

```text
Environmental compensation (SNUC) = project_investment * degradation_factor
example: R$ 50,000,000 * 0.5 percent = R$ 250,000 to conservation units
```

```mermaid
graph TD
    IMP["Significant impact"] --> AVOID["Avoid redesign"]
    AVOID --> MIN["Minimize reduce"]
    MIN --> REST["Restore rehabilitate"]
    REST --> RESID["Residual impact"]
    RESID --> COMP["Compensate offset"]
    COMP --> NETGAIN["No net loss goal"]
```

Remember: work the hierarchy top-down - avoid first, compensate last. Only
the residual impact that survives avoidance, minimization and restoration
should ever be offset.
""",
        ),
        quiz_lesson(
            "Quiz: Mitigation and compensation measures",
            (
                q(
                    "What is the correct order of the mitigation hierarchy?",
                    (
                        opt("Compensate, restore, minimize, avoid"),
                        opt(
                            "Avoid, minimize, restore, then compensate for the residual",
                            correct=True,
                        ),
                        opt("Minimize, avoid, compensate, restore"),
                        opt("Restore, compensate, avoid, minimize"),
                    ),
                    "Prevent first (avoid), then shrink (minimize), then repair "
                    "(restore), and only offset what remains (compensate).",
                ),
                q(
                    "What is a 'residual impact'?",
                    (
                        opt("An impact that was never identified"),
                        opt(
                            "The impact that remains after avoidance, minimization and "
                            "restoration have been applied",
                            correct=True,
                        ),
                        opt("An impact that only affects noise"),
                        opt("A positive impact of the project"),
                    ),
                    "Compensation and offsets target the residual - what is left once "
                    "the higher tiers of the hierarchy have done their work.",
                ),
                q(
                    "Why might an offset use a ratio like 2:1 (protect 24 ha for 12 ha lost)?",
                    (
                        opt("To make the project cheaper"),
                        opt("Because ratios are legally forbidden"),
                        opt(
                            "Because protected replacement land is not identical in "
                            "quality or certainty to what was lost, so more is required "
                            "to achieve equivalent value",
                            correct=True,
                        ),
                        opt("To speed up the public hearing"),
                    ),
                    "Offset ratios above 1:1 account for differences in habitat quality "
                    "and the risk that restoration or protection under-delivers.",
                ),
            ),
        ),
        # -- 7. Environmental programs and monitoring ------------------
        _t(
            "Environmental programs and monitoring",
            "10 min",
            """# Environmental programs and monitoring

Predictions and promises are worthless without follow-through. The EIA's
commitments are turned into **environmental programs** collected in a
**Basic Environmental Project (PBA)**, and their delivery is verified by
**monitoring**. This is the bridge from the study to real operation, and it
underpins the Installation and Operation licenses.

Typical programs on a large project include:

- **Environmental monitoring** - water quality, air, noise, groundwater
  levels, tracked against the baseline over time.
- **Fauna and flora programs** - rescue and relocation of wildlife during
  clearing, seedling nurseries and reforestation, monitoring of indicator
  species.
- **Erosion and sediment control**, effluent and **waste management**.
- **Environmental education** and **community communication** programs.
- **Emergency and risk-management** plans.

Monitoring only works if it is designed to **detect change against
thresholds**. Each indicator gets a limit, a sampling frequency, and a
**trigger** for action:

```text
MONITORING PLAN (extract)
Indicator          | Limit (standard)      | Frequency | If exceeded
-------------------|-----------------------|-----------|-------------------
Turbidity downstream| 100 NTU (CONAMA 357) | Monthly   | Stop earthworks, inspect
Effluent BOD       | 60 mg/L or 80 pct rem | Weekly    | Adjust treatment
Ambient noise night| 55 dB(A) NBR 10151    | Quarterly | Restrict night works
Reforestation      | 80 percent survival   | Biannual  | Replant failures
```

A simple compliance check on a monitored series:

```python
turbidity = [42, 55, 61, 118, 47]     # monthly NTU downstream
limit = 100
breaches = [i for i, v in enumerate(turbidity, 1) if v > limit]
print(breaches)   # [4]  -> month 4 exceeded, triggers corrective action
```

Programs feed an **Environmental Management System (ISO 14001)**, whose
**Plan-Do-Check-Act** cycle mirrors monitoring: set objectives, operate,
measure against them, and correct. Monitoring reports are what the agency
reviews to grant and renew the Operation License.

```mermaid
graph LR
    EIA["EIA commitments"] --> PBA["Environmental programs PBA"]
    PBA --> DO["Operate and control"]
    DO --> MON["Monitor indicators"]
    MON --> Q1{"Within limits"}
    Q1 -->|"yes"| REPORT["Report and renew license"]
    Q1 -->|"no"| CORR["Corrective action"]
    CORR --> DO
```

Remember: programs turn EIA promises into obligations, and monitoring with
clear thresholds and triggers is what proves - during operation - that the
predictions and mitigation actually hold.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental programs and monitoring",
            (
                q(
                    "What is the role of environmental programs (the PBA)?",
                    (
                        opt("To replace the need for any licenses"),
                        opt(
                            "To turn the EIA's commitments and mitigation measures into "
                            "concrete, deliverable programs for the construction and "
                            "operation phases",
                            correct=True,
                        ),
                        opt("To calculate the project's profit"),
                        opt("To decide whether an EIA is needed"),
                    ),
                    "The PBA operationalizes the study's promises; delivering it "
                    "underpins the Installation and Operation licenses.",
                ),
                q(
                    "What makes a monitoring plan actually useful?",
                    (
                        opt("Collecting data with no limits or actions defined"),
                        opt(
                            "Each indicator has a threshold, a sampling frequency, and a "
                            "defined trigger for corrective action when it is exceeded",
                            correct=True,
                        ),
                        opt("Measuring only once at the end of the project"),
                        opt("Reporting only positive results"),
                    ),
                    "Monitoring must detect change against thresholds and trigger action, "
                    "not just accumulate numbers.",
                ),
                q(
                    "How does ISO 14001 relate to environmental monitoring?",
                    (
                        opt("It forbids monitoring"),
                        opt("It is a water-quality limit"),
                        opt(
                            "Its Plan-Do-Check-Act cycle mirrors monitoring: set "
                            "objectives, operate, measure against them, and correct",
                            correct=True,
                        ),
                        opt("It replaces the Operation License"),
                    ),
                    "ISO 14001 provides the environmental management system whose "
                    "PDCA loop the monitoring program feeds.",
                ),
            ),
        ),
        # -- 8. Public participation and hearings ----------------------
        _t(
            "Public participation and hearings",
            "10 min",
            """# Public participation and hearings

EIA is not only technical - it is **democratic**. The people who live with
a project's consequences have a right to information and a voice in the
decision. **Public participation** is what gives the process legitimacy,
and in many systems it is legally mandatory.

The main mechanisms:

- **Disclosure** - the **RIMA** (plain-language summary) is made publicly
  available so non-specialists can understand the project and its effects.
- **Public comment period** - a defined window in which anyone can submit
  written observations to the licensing agency.
- **Public hearing (*audiencia publica*)** - a formal, minuted meeting,
  governed in Brazil by CONAMA Resolution **09/1987**, where the study is
  presented and the community questions it. It can be **requested** by a
  civil entity, the public prosecutor, or 50 or more citizens, and the
  agency must hold one when validly requested.

Participation is meaningful only when it happens **early enough to
influence the decision** - after the LP is already granted, comment is
theatre. Good practice engages communities during scoping, so their
knowledge shapes what the study examines. Special care is owed to
**vulnerable and traditional groups**: Indigenous and quilombola
communities have distinct consultation rights (linked to ILO Convention
169 and free, prior and informed consent).

Comments do not bind the decision, but the agency must **consider and
respond** to them, and unresolved concerns can lead to conditions on the
license - or to legal challenge, often via the public prosecutor
(*Ministerio Publico*).

```text
PARTICIPATION CHECKLIST
[x] RIMA published in accessible language and format
[x] Copies lodged at agency, city hall, local library
[x] Comment period opened (>= legal minimum, e.g. 45 days)
[x] Public hearing scheduled in the affected area, evening, local venue
[x] Indigenous/traditional communities consulted per their protocols
[x] Comments logged, responded to, and reflected in license conditions
```

```mermaid
graph TD
    RIMA["Publish RIMA"] --> INFORM["Inform the public"]
    INFORM --> COMMENT["Comment period"]
    COMMENT --> HEAR["Public hearing"]
    HEAR --> AGENCY["Agency considers input"]
    AGENCY --> Q1{"Concerns resolved"}
    Q1 -->|"yes"| DECIDE["Decision with conditions"]
    Q1 -->|"no"| REVISE["Revise study or conditions"]
    REVISE --> AGENCY
```

Remember: participation converts an expert study into a legitimate public
decision - it must be early, accessible, inclusive of vulnerable groups,
and genuinely reflected in the outcome, not a box ticked at the end.
""",
        ),
        quiz_lesson(
            "Quiz: Public participation and hearings",
            (
                q(
                    "Which document is published so the public can understand a project's impacts?",
                    (
                        opt("The full technical EIA only"),
                        opt(
                            "The RIMA - the plain-language environmental impact report "
                            "summarizing the EIA",
                            correct=True,
                        ),
                        opt("The Operation License"),
                        opt("The monitoring database"),
                    ),
                    "The RIMA exists specifically to make the technical EIA accessible "
                    "to non-specialists.",
                ),
                q(
                    "When is public participation most meaningful?",
                    (
                        opt("After the Preliminary License is already granted"),
                        opt("Only during operation, years later"),
                        opt(
                            "Early enough to actually influence the decision, ideally "
                            "from scoping onward",
                            correct=True,
                        ),
                        opt("Never - it does not affect anything"),
                    ),
                    "Comment after the decision is theatre; early engagement lets the "
                    "community shape what is studied and decided.",
                ),
                q(
                    "What obligation does a licensing agency have toward public comments?",
                    (
                        opt("To ignore them, since they are not binding"),
                        opt(
                            "To consider and respond to them, and reflect unresolved "
                            "concerns in license conditions where warranted",
                            correct=True,
                        ),
                        opt("To automatically cancel the project"),
                        opt("To forward them only to the developer"),
                    ),
                    "Comments do not bind the decision, but the agency must consider "
                    "and respond; concerns can become license conditions or grounds "
                    "for challenge.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What is the purpose of Environmental Impact Assessment?",
                    (
                        opt("To generate paperwork after construction"),
                        opt(
                            "To evaluate a project's likely environmental consequences "
                            "before approval, informing whether and how it proceeds",
                            correct=True,
                        ),
                        opt("To market the project to investors"),
                        opt("To replace the need for engineering design"),
                    ),
                    "EIA is a pre-decision process that makes consequences visible and "
                    "shapes the approval.",
                ),
                q(
                    "Which is the correct order of the three CONAMA 237/1997 licenses?",
                    (
                        opt("Operation, Installation, Preliminary"),
                        opt(
                            "Preliminary License, Installation License, Operation License",
                            correct=True,
                        ),
                        opt("Installation, Preliminary, Operation"),
                        opt("Preliminary, Operation, Installation"),
                    ),
                    "LP (viability) then LI (construction) then LO (operation) - each "
                    "gates the next phase.",
                ),
                q(
                    "Screening decides ___, while scoping decides ___.",
                    (
                        opt("the budget; the schedule"),
                        opt(
                            "whether a full EIA is needed; what the EIA should focus on "
                            "and its boundaries",
                            correct=True,
                        ),
                        opt("the mitigation; the compensation"),
                        opt("the hearing date; the report length"),
                    ),
                    "Screening is the whether-gate; scoping is the what-and-where focusing step.",
                ),
                q(
                    "Why must a baseline diagnosis capture natural variability (e.g. wet and dry seasons)?",
                    (
                        opt("To lengthen the study"),
                        opt(
                            "So later changes can be reliably attributed to the project "
                            "rather than to normal seasonal fluctuation",
                            correct=True,
                        ),
                        opt("Because licenses expire in the dry season"),
                        opt("To avoid measuring water quality"),
                    ),
                    "Without the natural range, you cannot tell a project impact from "
                    "ordinary variation.",
                ),
                q(
                    "What is the main value of an interaction (Leopold) matrix?",
                    (
                        opt("It grants the license automatically"),
                        opt(
                            "It systematically crosses every action against every "
                            "component so no interaction is overlooked",
                            correct=True,
                        ),
                        opt("It measures noise in decibels"),
                        opt("It sets the offset ratio"),
                    ),
                    "The matrix is a completeness tool - actions by components, cell by cell.",
                ),
                q(
                    "Significance evaluation ranks impacts primarily by combining:",
                    (
                        opt("cost and schedule"),
                        opt(
                            "the magnitude of the change and the importance or "
                            "sensitivity of the affected receptor",
                            correct=True,
                        ),
                        opt("the number of comments received"),
                        opt("the color of the map"),
                    ),
                    "Magnitude times receptor importance, scored transparently, yields a "
                    "priority order.",
                ),
                q(
                    "In the mitigation hierarchy, which option is always preferred first?",
                    (
                        opt("Compensate with an offset"),
                        opt("Restore the area afterward"),
                        opt(
                            "Avoid the impact entirely through design, routing or timing",
                            correct=True,
                        ),
                        opt("Minimize it slightly"),
                    ),
                    "Avoid, then minimize, then restore, and only offset the residual - "
                    "prevention beats repair.",
                ),
                q(
                    "What should be offset by compensation measures?",
                    (
                        opt("Every impact, before trying to avoid it"),
                        opt("Only positive impacts"),
                        opt(
                            "The residual impact that remains after avoidance, "
                            "minimization and restoration",
                            correct=True,
                        ),
                        opt("Nothing - offsets are illegal"),
                    ),
                    "Offsets are the last resort, targeting only what survives the "
                    "higher tiers of the hierarchy.",
                ),
                q(
                    "What makes a monitoring program effective during operation?",
                    (
                        opt("Collecting data with no thresholds"),
                        opt(
                            "Indicators tied to limits, sampling frequencies and triggers "
                            "for corrective action when exceeded",
                            correct=True,
                        ),
                        opt("Reporting once at project close"),
                        opt("Measuring only profit"),
                    ),
                    "Thresholds plus triggers let monitoring detect and correct "
                    "deviations, and support license renewal.",
                ),
                q(
                    "Why is public participation essential to EIA?",
                    (
                        opt("It speeds up construction"),
                        opt("It lowers the project cost"),
                        opt(
                            "It gives affected communities information and a voice, "
                            "lending the decision legitimacy - and must happen early "
                            "enough to influence it",
                            correct=True,
                        ),
                        opt("It replaces the technical study"),
                    ),
                    "Participation converts an expert study into a legitimate public "
                    "decision; it must be early, accessible and genuinely considered.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_IMPACT_ASSESSMENT_COURSES: tuple[SeedCourse, ...] = (
    _ENVIRONMENTAL_IMPACT_ASSESSMENT,
)
