"""Academy seed content — the Software Quality track (Beginner → Advanced).

* ``software-quality-basics``        — what quality is, QA, attributes vs
  metrics, dependability, maintenance types, measuring quality
* ``software-quality-intermediate``  — ISO/IEC 25010, SQuaRE quality-in-use,
  reviews/inspections/audits, the defect lifecycle, reliability metrics
* ``software-quality-advanced``      — CMMI, MPS.BR, Sommerville's three levels,
  quality plans (GQM), continuous improvement (PDCA), maturity scoring

Runnable ``code`` lessons use plain builtins + ``assert`` (the sandbox blocks
imports), so each metric calculation is fully self-contained.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# ──────────────────────────────────────────────────────────────────────
# software-quality-basics
# ──────────────────────────────────────────────────────────────────────

_SQ_BASICS = SeedCourse(
    slug="software-quality-basics",
    title="Software Quality — Basics",
    description=(
        "What software quality really means and why it pays off: the business "
        "benefits, quality assurance (QA) vs quality control, the crucial "
        "difference between attributes and metrics, the dependability "
        "dimensions, the four kinds of software maintenance, and a hands-on "
        "lab measuring defect density and MTBF."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is software quality?",
            "9 min",
            r"""# What is software quality?

**Software quality** is the degree to which a system meets its users' needs,
its defined requirements, and the expected technical standards. In plain terms:
quality software **works well, fails less, is more reliable, and gives a better
experience**.

Why does it pay off? The benefits are concrete and business-facing:

- **It saves money** — fewer defects mean less rework, fewer emergency fixes,
  and less support cost.
- **It prevents catastrophic corporate emergencies** — serious failures are
  caught *before* they reach production and customers.
- **It earns customer trust** — shipping stable software signals commitment to
  the user's success.
- **It keeps the user experience high** — no slowness, errors, or frustration.

```mermaid
flowchart LR
  Q["Software quality"] --> A["Saves money (less rework)"]
  Q --> B["Prevents catastrophic emergencies"]
  Q --> C["Earns customer trust"]
  Q --> D["High user experience"]
```

**Exam tip.** When a question lists *saves money*, *prevents catastrophic
corporate emergencies*, *inspires customer confidence*, and *keeps the user
experience high* together, the answer it's pointing at is **software quality**.

Quality isn't a single attribute you bolt on at the end — it's the cumulative
result of good requirements, sound design, careful construction, and disciplined
verification. The rest of this course unpacks how we *assure*, *describe*, and
*measure* it.
""",
        ),
        _t(
            "Quality assurance (QA) vs quality control",
            "10 min",
            r"""# Quality assurance (QA) vs quality control

**Quality assurance (QA)** exists to make sure the software is delivered to the
final customer *with* quality — and that the **process** of verifying that
quality is run in an **organised** way. QA is *process-oriented*: it's about
building things right so defects are prevented, not just found.

What a QA function actually does:

- **Defines** quality standards, processes, and acceptance criteria.
- **Plans** how quality will be evaluated across the project.
- **Tracks** tests, technical reviews, and audits.
- **Records** errors and non-conformities so the team can fix them *and learn*.
- **Controls** the risks — and the suppliers — that could affect quality.

```mermaid
flowchart TB
  S["Define standards & criteria"] --> P["Plan how quality is evaluated"]
  P --> T["Track tests, reviews, audits"]
  T --> R["Record errors & non-conformities"]
  R --> I["Fix and learn (improve)"]
  I --> S
```

**QA vs QC.** People mix these up:

- **Quality assurance (QA)** is *preventive* and *process-focused* — "are we
  doing the right activities so defects don't happen?"
- **Quality control (QC)** is *detective* and *product-focused* — "does this
  built artifact meet the spec?" Testing and inspection are QC activities.

A simple way to remember it: **QA builds the process; QC checks the product.**
Both feed each other — QC findings flow back into QA so the process keeps
improving.
""",
        ),
        _t(
            "Quality attributes vs metrics",
            "9 min",
            r"""# Quality attributes vs metrics

This is one of the most common exam traps, so make it crisp:

- An **attribute** is a *desired characteristic* of the software (a quality
  you want it to have).
- A **metric** is a *way to measure or track* that characteristic.

Attributes answer "**what** quality do we want?"; metrics answer "**how much**
of it do we have, in numbers?"

| Attribute (characteristic) | Metric (how it's measured)               |
|----------------------------|------------------------------------------|
| Completeness               | Number of requirements satisfied         |
| Understandability          | Readability index                        |
| Ambiguity                  | Number of ambiguous terms                |
| Reliability                | Mean time between failures (MTBF)        |
| Maintainability            | Time to fix or change                    |

```mermaid
flowchart LR
  subgraph Attributes
    A1["Completeness"]
    A2["Understandability"]
    A3["Ambiguity"]
  end
  subgraph Metrics
    M1["Requirements satisfied"]
    M2["Readability index"]
    M3["Ambiguous-term count"]
  end
  A1 --> M1
  A2 --> M2
  A3 --> M3
```

**Exam tip.** *Completeness, understandability, and ambiguity* are **attributes**
(characteristics). *Time-to-change* and *counts of modifiers/terms* are closer to
**metrics** (measurements). If the question lists qualities you want, it's
attributes; if it lists numbers you collect, it's metrics.

The point of metrics is to make an abstract attribute **observable and
trackable over time** — you can't manage what you don't measure.
""",
        ),
        _t(
            "The dependability dimensions",
            "9 min",
            r"""# The dependability dimensions

**Dependability** (the *trust* dimension) is about being able to **believe the
software will behave properly, safely, and predictably**. It's an umbrella over
several related properties:

- **Availability** — the system is up and ready when you need it.
- **Reliability** — it behaves correctly over time, with few failures.
- **Safety** — it does not cause harm to people or the environment.
- **Security** — it protects against malicious access and attacks.

```mermaid
mindmap
  root(("Dependability (trust)"))
    Availability
    Reliability
    Safety
    Security
    Maintainability
```

**Maintainability** is a further property often discussed under dependability:
the ability of the software to be **corrected, updated, adapted, or improved
with ease**. A handy discursive answer:

> An additional property of the dependability dimension is **maintainability**,
> because it lets us fix defects and adapt the software *without* compromising
> its quality, reliability, or the customer's trust.

Why maintainability matters more than ever: in a world of "vibe-coding" and AI
generating code fast, it's not enough to produce code quickly — it must stay
**organised, understandable, and safe to change**. Code you can't modify
confidently is a liability no matter how fast it was written. Maintainability is
the property that keeps the *other* dependability properties affordable to
preserve over a system's life.
""",
        ),
        _t(
            "Software maintenance types",
            "10 min",
            r"""# Software maintenance types

Software keeps evolving after it ships. **Maintenance** is classified by the
*reason* for the change — four classic types:

- **Corrective** — fixes defects, failures, or non-conformities found after
  delivery or during use.
- **Adaptive** — adapts the software to changes in its environment: a new
  operating system, a law, a third-party API, infrastructure.
- **Perfective** — improves performance or usability, or adds desired
  functionality (the software still "works", but you make it better).
- **Preventive** — improves the internal structure to **avoid future problems**
  (refactoring, hardening) before they ever become failures.

```mermaid
mindmap
  root(("Maintenance"))
    Corrective
      "Fix defects / non-conformities"
    Adaptive
      "New OS, law, API, infra"
    Perfective
      "Improve performance / add features"
    Preventive
      "Improve structure to avoid future issues"
```

**Exam tip.** The keyword that pins each type:

- "corrects defects / faults" → **corrective**
- "adapts to environment changes (OS, law, API)" → **adaptive**
- "improves performance / adds wanted features" → **perfective**
- "improves internal structure to avoid future problems" → **preventive**

A common mistake is collapsing *perfective* and *preventive*: perfective is
about **outward improvement** (faster, nicer, more features) while preventive is
about **inward structural health** (so problems don't arise later). Mature teams
budget for *all four* — neglecting preventive maintenance is what slowly turns a
healthy codebase into legacy.
""",
        ),
        _code(
            "Lab: measuring quality (defect density & MTBF)",
            "12 min",
            r"""# Two foundational quality metrics, computed from scratch — no imports.
# A metric turns an abstract attribute into a trackable number.

# --- 1) DEFECT DENSITY = defects / size (per 1000 lines of code, KLOC) ---
# in a real program you'd read these from your tracker / repo stats
defects_found = 37
lines_of_code = 24500
kloc = lines_of_code / 1000.0
defect_density = defects_found / kloc          # defects per KLOC

print("Defect density")
print("  defects:", defects_found, " size:", lines_of_code, "LOC")
print("  =", round(defect_density, 3), "defects / KLOC")

# Lower is better. Compare two releases to see if quality is improving.
release_a = 37 / (24500 / 1000.0)
release_b = 22 / (26100 / 1000.0)
improved = release_b < release_a
print("  release A:", round(release_a, 3), " release B:", round(release_b, 3))
assert improved, "release B should have lower defect density"
print("  density dropped from A to B ✓")

# --- 2) MTBF = mean time between failures (a RELIABILITY metric) ---
# Total operating time divided by the number of failures observed.
# in a real program you'd compute total uptime from monitoring logs
total_operating_hours = 8760     # one year of running
failures = 12
mtbf = total_operating_hours / failures
print()
print("MTBF (mean time between failures)")
print("  operating hours:", total_operating_hours, " failures:", failures)
print("  MTBF =", round(mtbf, 1), "hours between failures")

# Higher MTBF = more reliable. Convert to days for a human-readable view.
mtbf_days = mtbf / 24.0
print("  ≈", round(mtbf_days, 1), "days between failures")
assert mtbf > total_operating_hours / 20, "with 12 failures/yr, MTBF must exceed 438h"
print("  reliability check passed ✓")

# Takeaway: defect density tracks how buggy the code is per unit of size;
# MTBF tracks how long it runs before it fails. Track both over releases.
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# software-quality-intermediate
# ──────────────────────────────────────────────────────────────────────

_SQ_INTERMEDIATE = SeedCourse(
    slug="software-quality-intermediate",
    title="Software Quality — Intermediate",
    description=(
        "Standards and practice: the ISO/IEC 25010 product quality model, the "
        "SQuaRE framework and quality-in-use (effectiveness, productivity, "
        "safety, satisfaction), reviews/inspections/audits, the defect "
        "lifecycle and defect-removal efficiency, the reliability metrics that "
        "matter (MTBF, MTTR, availability), and a quality-scorecard lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The ISO/IEC 25010 product quality model",
            "10 min",
            r"""# The ISO/IEC 25010 product quality model

Talking about quality vaguely doesn't scale — you need a shared vocabulary.
**ISO/IEC 25010** defines a **product quality model**: eight top-level
characteristics that any software can be evaluated against, each broken into
sub-characteristics.

The eight characteristics:

- **Functional suitability** — does it do what's needed, correctly and
  completely?
- **Performance efficiency** — time behaviour and resource use.
- **Compatibility** — coexists and interoperates with other systems.
- **Usability** — easy to learn, operate, and free of user error.
- **Reliability** — maturity, availability, fault tolerance, recoverability.
- **Security** — confidentiality, integrity, authenticity.
- **Maintainability** — modularity, reusability, analysability, modifiability,
  testability.
- **Portability** — adaptability, installability, replaceability.

```mermaid
mindmap
  root(("ISO/IEC 25010 product quality"))
    "Functional suitability"
    "Performance efficiency"
    Compatibility
    Usability
    Reliability
    Security
    Maintainability
    Portability
```

This model is the *product* view — qualities of the software artifact itself.
It pairs with a separate **quality-in-use** view (next lesson), which looks at
the *outcomes* real users get. Note how the attributes you met in the Basics
course (reliability, maintainability) reappear here as first-class
characteristics — 25010 organises them into one coherent, measurable map you can
use as a **checklist** when defining and assessing quality.
""",
        ),
        _t(
            "SQuaRE & quality in use",
            "9 min",
            r"""# SQuaRE & quality in use

**SQuaRE** (Systems and software Quality Requirements and Evaluation, the
ISO/IEC 25000 series) is the family of standards that *contains* the 25010 model.
Beyond the **product quality** view, SQuaRE defines **quality in use** — quality
seen from the **real context of the user**, i.e. the *outcomes* of using the
software, not the properties of the artifact.

The quality-in-use characteristics are:

- **Effectiveness** — the user **achieves their goals** (accurately and
  completely).
- **Productivity** — the user achieves those goals **with good use of time and
  resources**.
- **Safety** — using the system **reduces risks and harm** (to people, business,
  data, environment).
- **Satisfaction** — the user has a **positive experience**.

```mermaid
flowchart TB
  QU["Quality in use (SQuaRE)"] --> E["Effectiveness (goals achieved)"]
  QU --> P["Productivity (good use of time/resources)"]
  QU --> S["Safety (reduced risk/harm)"]
  QU --> T["Satisfaction (positive experience)"]
```

**Exam tip.** When asked what *quality in use* in SQuaRE includes, the answer is
**effectiveness, productivity, safety, and satisfaction**.

The distinction to keep straight: **product quality** describes the software
itself (is it reliable, maintainable, secure?); **quality in use** describes what
happens when a *specific user* pursues a *specific goal* in a *specific context*.
A product can score well on product quality yet score poorly in use if the
context is wrong — which is why SQuaRE measures both.
""",
        ),
        _t(
            "Reviews, inspections & audits",
            "9 min",
            r"""# Reviews, inspections & audits

Testing runs the code; **static** quality techniques examine the work *without*
running it — and they catch a different, often cheaper-to-fix, class of problems
(unclear requirements, design flaws, standards violations). These are core QA
activities:

- **Walkthrough** — the author informally guides peers through the artifact to
  gather feedback. Low ceremony.
- **Technical review** — peers evaluate the work against requirements and
  standards; more structured than a walkthrough.
- **Inspection** — the most formal: defined roles (author, moderator, reader,
  scribe), entry/exit criteria, checklists, and logged defects with metrics
  (Fagan inspections). Highly effective at finding defects early.
- **Audit** — an **independent** check that the *process and standards were
  actually followed* (a compliance/QA lens), not primarily a defect hunt.

```mermaid
flowchart LR
  W["Walkthrough (informal)"] --> R["Technical review (structured)"]
  R --> I["Inspection (formal, roles + checklist)"]
  I --> A["Audit (independent process check)"]
```

The key insight: these techniques **shift defect detection left**, to phases
*before* code even runs, where fixing is dramatically cheaper:

```plot
{"title": "Relative cost to fix a defect by phase", "xLabel": "phase (requirements → design → code → test → production)", "yLabel": "relative cost", "xRange": [0, 4], "yRange": [0, 90], "functions": [{"expr": "3^x", "label": "cost grows roughly exponentially", "color": "#dc2626"}]}
```

A defect caught in a requirements review costs a fraction of the same defect
escaping to production. Reviews and inspections are some of the highest-ROI
quality activities a team can adopt — and unlike dynamic testing, they work on
documents and designs, not just running code.
""",
        ),
        _t(
            "Defect management & the defect lifecycle",
            "9 min",
            r"""# Defect management & the defect lifecycle

A defect (bug) isn't just "found and fixed" — it moves through a **lifecycle**,
and tracking that lifecycle is how QA learns and improves. A typical flow:

- **New** — a defect is reported.
- **Assigned** — triaged and given to a developer (with a severity/priority).
- **Open / In progress** — being worked on.
- **Fixed** — the developer believes it's resolved.
- **Retest / Verified** — QA confirms the fix (or **reopens** it if not).
- **Closed** — verified resolved.
- **Rejected / Deferred / Duplicate** — not a valid defect, postponed, or
  already tracked.

```mermaid
stateDiagram-v2
  [*] --> New
  New --> Assigned
  Assigned --> InProgress
  InProgress --> Fixed
  Fixed --> Verified
  Verified --> Closed
  Fixed --> Reopened: retest fails
  Reopened --> InProgress
  New --> Rejected: not a defect
  Closed --> [*]
```

**Severity vs priority** — a frequently confused pair:

- **Severity** = technical impact ("it corrupts data" is high severity).
- **Priority** = business urgency ("fix before the launch demo" is high
  priority).

A typo on the landing page can be *low severity but high priority*; a rare crash
in an unused admin tool can be *high severity but low priority*.

Recording defects with consistent states, severity, and root cause turns
bug-fixing into **data**: it feeds metrics like defect density and
defect-removal efficiency (next lesson), and reveals *where* in the process
defects keep entering — which is what drives lasting improvement.
""",
        ),
        _t(
            "Quality metrics that matter (MTBF, MTTR, availability, DRE)",
            "10 min",
            r"""# Quality metrics that matter

Metrics make quality manageable — but only the *right* ones. Four that recur in
every serious quality program:

- **MTBF — mean time between failures.** Total operating time ÷ number of
  failures. Higher = more **reliable**.
- **MTTR — mean time to repair/recover.** Total downtime ÷ number of incidents.
  Lower = you **recover** faster.
- **Availability** — the fraction of time the system is up:

$$
A = \frac{MTBF}{MTBF + MTTR}
$$

- **Defect Removal Efficiency (DRE)** — of all the defects that existed, what
  fraction did you catch *before* release:

$$
DRE = \frac{defects\ found\ before\ release}{defects\ found\ before + after\ release}
$$

```mermaid
flowchart LR
  MTBF["MTBF (reliability)"] --> AV["Availability = MTBF / (MTBF + MTTR)"]
  MTTR["MTTR (recovery)"] --> AV
  DRE["DRE (pre-release catch rate)"] --> Q["Process quality signal"]
```

Availability is dominated by how fast you *recover*, not just how rarely you
fail — watch how availability climbs as MTTR shrinks (here for a fixed
MTBF of 200 hours):

```plot
{"title": "Availability vs MTTR (MTBF fixed at 200h)", "xLabel": "MTTR (hours)", "yLabel": "availability", "xRange": [0, 50], "yRange": [0, 1.05], "functions": [{"expr": "200 / (200 + x)", "label": "A = 200/(200+MTTR)", "color": "#16a34a"}]}
```

Use these together: MTBF/availability describe the *product's* runtime quality;
DRE describes how good your *process* is at catching defects early. A high DRE
means few bugs escape to users — the closest thing to a quality scoreboard.
You'll compute all four in the next lab.
""",
        ),
        _code(
            "Lab: a quality scorecard (availability & DRE)",
            "13 min",
            r"""# Build a small quality scorecard from raw numbers — builtins only.

# --- Reliability & recovery ---
# in a real program you'd pull these from monitoring/incident tooling
operating_hours = 4000
failures = 8
downtime_hours = 20
incidents = 8

mtbf = operating_hours / failures            # mean time between failures
mttr = downtime_hours / incidents            # mean time to repair
availability = mtbf / (mtbf + mttr)          # the availability formula

print("MTBF        :", round(mtbf, 2), "h")
print("MTTR        :", round(mttr, 2), "h")
print("Availability:", round(availability, 5),
      "(", round(availability * 100, 3), "% )")

# Availability is between 0 and 1; faster recovery (lower MTTR) raises it.
assert 0.0 < availability < 1.0
assert availability > 0.99, "with MTBF 500h and MTTR 2.5h, availability should exceed 99%"
print("availability sanity check ✓")

# --- Defect Removal Efficiency: how many defects we caught before release ---
defects_before_release = 142
defects_after_release = 18                    # escaped to users
total_defects = defects_before_release + defects_after_release
dre = defects_before_release / total_defects

print()
print("Defects caught before release:", defects_before_release)
print("Defects escaped to users     :", defects_after_release)
print("DRE =", round(dre, 4), "(", round(dre * 100, 2), "% )")

# Higher DRE = a better process at catching defects early. Industry-strong is >90%.
assert 0.0 < dre <= 1.0
strong_process = dre > 0.85
print("strong defect-removal process:", strong_process)
assert strong_process, "DRE should be above 0.85 for a healthy process"
print("DRE check passed ✓")

# --- Roll it into a simple letter grade (all logic inline, no helper calls) ---
score = 0
if availability > 0.99:
    score = score + 1
if availability > 0.999:
    score = score + 1
if dre > 0.85:
    score = score + 1
if dre > 0.92:
    score = score + 1
grades = ["D", "C", "B", "A", "A+"]
grade = grades[score]
print()
print("Scorecard points:", score, "/ 4  ->  grade:", grade)
""",
        ),
    ),
)


# ──────────────────────────────────────────────────────────────────────
# software-quality-advanced
# ──────────────────────────────────────────────────────────────────────

_SQ_ADVANCED = SeedCourse(
    slug="software-quality-advanced",
    title="Software Quality — Advanced",
    description=(
        "Process maturity and management: the five CMMI levels, the MPS.BR "
        "maturity model (levels 2 and 5 in depth), Sommerville's three levels "
        "of quality concern (organizational / project / product), building a "
        "quality plan with Goal-Question-Metric (GQM), continuous improvement "
        "via PDCA and root-cause analysis, and a maturity-assessment lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Process maturity: CMMI (5 levels)",
            "10 min",
            r"""# Process maturity: CMMI (5 levels)

**CMMI** (Capability Maturity Model Integration) is a model for assessing and
improving the **maturity of an organisation's processes**. For exam questions,
the single most important fact is that it has **5 levels** — and that each level
builds on the one below it.

| Level | Name                       | Central idea                          |
|-------|----------------------------|---------------------------------------|
| 1     | Initial                    | Unpredictable, poorly controlled      |
| 2     | Managed                    | Projects are planned and tracked      |
| 3     | Defined                    | Processes standardised org-wide       |
| 4     | Quantitatively Managed     | Measurement & statistical control     |
| 5     | Optimizing                 | Continuous process improvement        |

```mermaid
flowchart TB
  L1["1. Initial (unpredictable)"] --> L2["2. Managed (planned & tracked)"]
  L2 --> L3["3. Defined (standardised)"]
  L3 --> L4["4. Quantitatively Managed (measured)"]
  L4 --> L5["5. Optimizing (continuous improvement)"]
```

**Benefits of CMMI.** Adopting it improves the organisation's processes,
increases product quality, reduces rework, and improves **predictability** and
project management. A short discursive answer:

> CMMI improves a company's processes, making development more organised and
> predictable. It also raises product quality, reducing errors, rework, and
> failures.

The progression is the whole point: you can't run a meaningful *quantitative*
program (level 4) until processes are *defined* and *standardised* (level 3),
which itself depends on individual projects being *managed* (level 2). Skipping
levels doesn't work — maturity is cumulative.
""",
        ),
        _t(
            "The MPS.BR maturity model",
            "9 min",
            r"""# The MPS.BR maturity model

**MPS.BR** (Melhoria de Processo do Software Brasileiro) is also a **process
maturity model** — a Brazilian framework aligned with CMMI and ISO standards,
designed to be adoptable in graduated steps (it has seven levels, labelled A
through G, with G the entry point and A the highest). For exams, two levels
dominate: **level 2 (Managed)** and **level 5 (Optimizing)**.

- **Level 2 — Managed (Gerenciado).** Tied to **project planning**, **project
  monitoring/tracking**, **requirements management**, and **supplier
  agreements**. The theme is: get individual projects *under control*.
- **Level 5 — Optimizing (Otimizado).** Tied to **innovation and its rollout
  across the organisation**, plus **causal analysis and resolution** (finding
  and eliminating the root causes of problems). The theme is: **continuous
  improvement**.

```mermaid
flowchart LR
  N2["Level 2 - Managed"] --> N2a["Project planning & tracking"]
  N2 --> N2b["Requirements management"]
  N2 --> N2c["Supplier agreements"]
  N5["Level 5 - Optimizing"] --> N5a["Innovation rolled out org-wide"]
  N5 --> N5b["Causal analysis & resolution"]
```

**To memorise it:** *level 2 organises and manages; level 5 improves
continuously and eliminates the causes of problems.*

**Exam tips.**

- MPS.BR **level 5 — Optimizing** → *innovation and organisational rollout;
  analysis and resolution of causes.*
- MPS.BR **level 2 — Managed** → *project planning, requirements management,
  monitoring, and suppliers.*

Notice the parallel with CMMI: both are maturity ladders where the bottom rungs
bring projects under control and the top rung is about systematically improving
the process itself.
""",
        ),
        _t(
            "Quality management at three levels (Sommerville)",
            "9 min",
            r"""# Quality management at three levels (Sommerville)

Sommerville frames quality management as operating at three **levels of
concern**. Each level owns a different scope of decision:

- **Organizational level** — defines the company's **quality policies,
  standards, and culture**. This is the broad, cross-project layer.
- **Project level** — defines the **quality plan for a specific project**: its
  goals, the processes and standards used, and how delivery will be assured.
- **Product / process level** — observes whether the **software and the
  development process actually meet the criteria** that were defined.

```mermaid
flowchart TB
  ORG["Organizational level: policies, standards, culture"] --> PRJ["Project level: the project's quality plan, goals, standards"]
  PRJ --> PRD["Product/process level: does the software & process meet the criteria?"]
```

**Exam tips.**

- The **organizational level** is the one that defines company-wide policies,
  standards, and culture — it shows up as a *correct* option for "what is a level
  of quality concern".
- When a question describes a **quality plan for the project**, with **goals,
  processes, and standards** used in delivery, associate it with the **project
  level**.

The hierarchy matters: organisational standards constrain what each project's
quality plan may set, and the project plan in turn defines the criteria the
product/process level is checked against. Quality decisions flow **down** the
levels; evidence and findings flow **back up**.
""",
        ),
        _t(
            "Building a quality plan & strategy (GQM)",
            "10 min",
            r"""# Building a quality plan & strategy (GQM)

A **quality plan** is the project-level artifact (recall Sommerville's project
level) that states *which* qualities matter for *this* project, *how* they'll be
achieved, and *how* they'll be measured. The risk is choosing metrics because
they're easy, not because they're meaningful. **Goal-Question-Metric (GQM)**
prevents that by deriving metrics *top-down* from goals:

1. **Goal** — a business/quality objective ("improve reliability of checkout").
2. **Question** — what would tell us we're meeting it? ("How often does checkout
   fail? How fast do we recover?").
3. **Metric** — the number that answers each question (MTBF, MTTR, availability,
   escaped-defect count).

```mermaid
flowchart TB
  G["Goal: improve checkout reliability"] --> Q1["Q: how often does it fail?"]
  G --> Q2["Q: how fast do we recover?"]
  Q1 --> M1["Metric: MTBF / failure rate"]
  Q2 --> M2["Metric: MTTR / availability"]
```

Every metric you collect should trace back up to a question and a goal — if it
doesn't, drop it. This keeps the plan focused and avoids "vanity metrics".

A good quality plan typically pins down:

- the **target attributes** (from a model like ISO/IEC 25010) that matter most,
- **measurable goals** for each (e.g. "availability ≥ 99.9%", "DRE ≥ 90%"),
- the **activities** that will achieve them (reviews, inspections, test levels,
  audits),
- and the **roles and gates** (who signs off, what blocks a release).

GQM turns a vague aspiration ("ship quality software") into a small set of
**goal-linked, trackable numbers** — the bridge between strategy and the metrics
from the Intermediate course.
""",
        ),
        _t(
            "Continuous improvement: PDCA & root-cause analysis",
            "10 min",
            r"""# Continuous improvement: PDCA & root-cause analysis

The top of every maturity model (CMMI level 5, MPS.BR level 5) is **continuous
improvement** — and its engine is the **PDCA cycle** (Plan-Do-Check-Act, the
Deming cycle):

- **Plan** — identify a problem or opportunity and plan a change/experiment.
- **Do** — implement the change on a small scale.
- **Check** — measure the results against the expected outcome.
- **Act** — if it worked, **standardise** it; if not, adjust and loop again.

```mermaid
stateDiagram-v2
  [*] --> Plan
  Plan --> Do
  Do --> Check
  Check --> Act
  Act --> Plan: iterate / standardise
```

PDCA never "finishes" — it spins continuously, each turn raising the baseline.

**Root-cause analysis (RCA)** is what feeds the *Plan* step with real problems.
Instead of patching symptoms, you trace a defect or incident to its underlying
cause. Two common tools:

- **5 Whys** — ask "why?" repeatedly until you reach a process cause, not a
  surface one.
- **Fishbone / Ishikawa diagram** — categorise candidate causes (people, process,
  tools, environment, materials) to structure the hunt.

This is exactly the spirit of **MPS.BR level 5's "causal analysis and
resolution"** and CMMI level 5: don't just fix the bug — fix the *process* that
let the bug in, so the whole class of defects stops recurring. Over many PDCA
turns guided by RCA, the escaped-defect rate falls and the organisation's
maturity genuinely rises — improvement compounds:

```plot
{"title": "Escaped defects fall as PDCA cycles compound", "xLabel": "improvement cycles", "yLabel": "escaped defects per release", "xRange": [0, 12], "yRange": [0, 55], "functions": [{"expr": "50 * exp(-0.3 * x)", "label": "escaped defects", "color": "#2563eb"}]}
```
""",
        ),
        _code(
            "Lab: a maturity-assessment scorer",
            "13 min",
            r"""# Score an organisation's process maturity from yes/no practice answers,
# CMMI-style (1 Initial .. 5 Optimizing). Builtins only, fully self-contained.

# Each level is "achieved" only if its key practices are in place AND every
# lower level is also achieved (maturity is cumulative — you can't skip levels).
# in a real assessment these come from interviews/evidence, not literals.
practices = {
    2: True,   # Managed: projects planned, tracked; requirements managed
    3: True,   # Defined: processes standardised org-wide
    4: True,   # Quantitatively Managed: measurement & statistical control
    5: False,  # Optimizing: continuous improvement, causal analysis
}

# Walk levels 2..5; stop at the first gap. Level 1 (Initial) is the floor.
level = 1
for lvl in [2, 3, 4, 5]:
    if practices[lvl]:
        level = lvl
    else:
        break   # cumulative: a missing level caps maturity here

names = {
    1: "Initial",
    2: "Managed",
    3: "Defined",
    4: "Quantitatively Managed",
    5: "Optimizing",
}
print("Assessed CMMI maturity level:", level, "-", names[level])

# Even though level 4 practices are present, the level-5 gap caps us at 4.
assert level == 4, "a gap at level 5 must cap maturity at 4 (cumulative model)"
print("cumulative-model check ✓ (level-5 gap caps at 4)")

# --- Turn the per-level answers into a readiness percentage toward level 5 ---
achieved = 0
for lvl in [2, 3, 4, 5]:
    if practices[lvl]:
        achieved = achieved + 1
readiness = achieved / 4.0
print("Practice areas in place:", achieved, "/ 4  ->",
      round(readiness * 100, 1), "% toward Optimizing")

# --- Recommend the next focus area (the first unmet level) ---
focus_level = None
for lvl in [2, 3, 4, 5]:
    if not practices[lvl]:
        focus_level = lvl
        break
if focus_level is None:
    print("Next focus: sustain level 5 (continuous improvement)")
else:
    print("Next focus: reach level", focus_level, "-", names[focus_level])

assert focus_level == 5
print("recommendation check ✓")
# Takeaway: maturity scoring is cumulative — invest in the lowest unmet level.
""",
        ),
    ),
)


SOFTWARE_QUALITY_COURSES = (_SQ_BASICS, _SQ_INTERMEDIATE, _SQ_ADVANCED)
