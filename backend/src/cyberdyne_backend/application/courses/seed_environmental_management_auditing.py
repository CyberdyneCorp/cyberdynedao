"""Academy seed content - Environmental Management, Auditing and ISO 14001.

Running environmental performance as a system rather than a checklist: the
ISO 14001 Environmental Management System (EMS) and the Plan-Do-Check-Act
cycle, environmental policy with aspects and impacts, measurable objectives
and indicators, environmental auditing, legal compliance and due diligence,
environmental liabilities, emergency preparedness, and continual improvement
closing into ESG reporting. Every lesson is a direct explanation with a
concrete example (a standards table, an indicator formula, or a process
snippet) and a mermaid diagram, followed by a checkpoint quiz; the course
closes with a comprehensive final quiz.
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


_ENVIRONMENTAL_MANAGEMENT_AUDITING = SeedCourse(
    slug="environmental-management-auditing",
    title="Environmental Management, Auditing & ISO 14001",
    description=(
        "Running environmental performance as a system - ISO 14001, aspects "
        "and impacts, objectives and indicators, auditing, compliance and due "
        "diligence, and ESG reporting. Every lesson explains one idea "
        "directly, shows it in a real example (a standards table, an indicator "
        "formula, or a process snippet), and draws it as a diagram, with a "
        "checkpoint quiz after each and a comprehensive final quiz."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Environmental Management, Auditing and ISO 14001

Environmental performance is not a one-off report or a permit on the wall
- it is something you **run as a system**. This course teaches you to
manage the environmental side of an organization the way a good operator
manages quality or safety: with a policy, measurable objectives, evidence,
audits, and continual improvement.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a standards table, an
indicator formula, or a process snippet), and draws the idea as a diagram.
After each lesson there is a short quiz; at the end, a final quiz covers
the whole course.

What you will build understanding for, in order:

1. **Environmental Management Systems and ISO 14001** - the PDCA backbone
2. **Environmental policy, aspects and impacts** - what you affect and how
3. **Objectives, targets and indicators** - turning intent into numbers
4. **Environmental auditing** - checking the system against evidence
5. **Legal compliance and due diligence** - obligations and liability
6. **Environmental liabilities** - contaminated land and provisions
7. **Emergency preparedness and response** - planning for the bad day
8. **Continual improvement and ESG reporting** - closing and disclosing the loop

Throughout we ground ideas in real practice and standards - **ISO 14001**,
**ISO 14031** (environmental performance evaluation), **ISO 19011**
(auditing), **ISO 14040** (life-cycle assessment), and Brazilian
references such as **ABNT NBR** and **CONAMA** resolutions, alongside
**GHG Protocol** and **GRI** for reporting. Keep it teachable: the point
is the system, not the acronyms.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the central idea of this course?",
                    (
                        opt("Filing a single annual environmental report"),
                        opt(
                            "Managing environmental performance as a system - policy, "
                            "objectives, evidence, audits and continual improvement",
                            correct=True,
                        ),
                        opt("Passing a one-time government inspection"),
                        opt("Installing a piece of monitoring software"),
                    ),
                    "Environmental performance is run as a management system, not "
                    "produced as a one-off document.",
                ),
                q(
                    "Which standard is the backbone reference for the course?",
                    (
                        opt("ISO 9001 for quality management"),
                        opt("ISO 27001 for information security"),
                        opt("ISO 14001 for environmental management systems", correct=True),
                        opt("ISO 45001 for occupational health and safety"),
                    ),
                    "ISO 14001 defines the environmental management system (EMS) this "
                    "course is built around.",
                ),
            ),
        ),
        # -- 1. EMS and ISO 14001 --------------------------------------
        _t(
            "Environmental management systems and ISO 14001",
            "10 min",
            """# Environmental management systems and ISO 14001

An **Environmental Management System (EMS)** is the set of processes an
organization uses to manage its environmental responsibilities in a
structured, repeatable way. **ISO 14001** is the international standard
that specifies the requirements for one. It does not set pollution limits
- it requires you to build the *machinery* that identifies your impacts,
sets objectives, controls operations, and improves over time.

At its heart is the **Plan-Do-Check-Act (PDCA)** cycle - the same
continual-improvement loop used across management standards:

- **Plan** - understand context, identify environmental aspects and legal
  obligations, set objectives.
- **Do** - implement operational controls, training, and documented
  procedures.
- **Check** - monitor, measure, audit, and evaluate compliance.
- **Act** - review at management level and drive corrective action and
  improvement.

The 2015 revision of ISO 14001 added the **High-Level Structure** shared
with ISO 9001, plus **risk-based thinking**, **leadership** commitment, and
a **life-cycle perspective** on aspects. Conformance can be independently
**certified** by an accredited body, but certification is a consequence of
a working system, not the goal.

```text
ISO 14001 clause map (2015), aligned to PDCA
------------------------------------------------------------
Clause 4  Context of the organization        (foundation)
Clause 5  Leadership and policy              PLAN
Clause 6  Planning: aspects, obligations,    PLAN
          risks, objectives
Clause 7  Support: resources, competence,    DO
          communication, documented info
Clause 8  Operation: controls, emergency     DO
Clause 9  Performance evaluation: monitor,   CHECK
          audit, management review
Clause 10 Improvement: nonconformity, CAPA,  ACT
          continual improvement
```

```mermaid
graph LR
    PLAN["Plan aspects and objectives"] --> DO["Do controls and training"]
    DO --> CHECK["Check monitor and audit"]
    CHECK --> ACT["Act review and improve"]
    ACT --> PLAN
```

Remember: ISO 14001 gives you a **system for managing environment**, and
PDCA is the engine that keeps it turning.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental management systems and ISO 14001",
            (
                q(
                    "What does ISO 14001 actually specify?",
                    (
                        opt("Numeric emission limits for each pollutant"),
                        opt(
                            "The requirements for an environmental management system - "
                            "the machinery to identify impacts, set objectives and improve",
                            correct=True,
                        ),
                        opt("A list of approved treatment technologies"),
                        opt("Fines for non-compliance"),
                    ),
                    "ISO 14001 sets EMS requirements, not pollution limits; the limits "
                    "come from law and permits.",
                ),
                q(
                    "What cycle is at the heart of ISO 14001?",
                    (
                        opt("Design-Build-Operate-Transfer"),
                        opt("Plan-Do-Check-Act (PDCA)", correct=True),
                        opt("Reduce-Reuse-Recycle"),
                        opt("Observe-Orient-Decide-Act"),
                    ),
                    "PDCA is the continual-improvement engine shared across ISO "
                    "management-system standards.",
                ),
                q(
                    "What did the 2015 revision of ISO 14001 emphasize?",
                    (
                        opt("Removing the need for any documentation"),
                        opt(
                            "Leadership, risk-based thinking and a life-cycle perspective, "
                            "on the shared High-Level Structure",
                            correct=True,
                        ),
                        opt("Mandatory carbon offsetting"),
                        opt("A ban on third-party certification"),
                    ),
                    "ISO 14001:2015 aligned to the High-Level Structure and added "
                    "leadership, risk-based thinking and life-cycle perspective.",
                ),
            ),
        ),
        # -- 2. Policy, aspects and impacts ----------------------------
        _t(
            "Environmental policy, aspects and impacts",
            "11 min",
            """# Environmental policy, aspects and impacts

The **environmental policy** is top management's public statement of
intent and direction. ISO 14001 requires it to commit to at least three
things: **protection of the environment** (including prevention of
pollution), **fulfilment of compliance obligations**, and **continual
improvement** of the EMS. It must fit the organization's context and
provide the frame for setting objectives.

The technical core of planning is the distinction between an **aspect** and
an **impact**:

- An **environmental aspect** is an *element of your activities, products
  or services that can interact with the environment* - a discharge, an
  emission, a resource use.
- An **environmental impact** is the *change* to the environment that
  results from that aspect - the actual effect, good or bad.

Aspect is the cause you control; impact is the consequence you care about.

```text
Aspect  --->  Impact  (worked examples)
------------------------------------------------------------
Boiler flue-gas emission (aspect) --> reduced air quality (impact)
Wastewater discharge (aspect)     --> river oxygen depletion (impact)
Diesel storage on site (aspect)   --> soil and groundwater contamination
Electricity consumption (aspect)  --> GHG emissions and climate change
Solvent use (aspect)              --> hazardous waste generation
```

You then rate each aspect for **significance** - typically severity of
impact times likelihood times a legal/stakeholder weighting - and manage
the **significant aspects** first. A life-cycle perspective means looking
beyond the gate: upstream (raw materials) and downstream (use and
end-of-life), not just what happens on site.

```mermaid
graph LR
    ACT["Activity or product"] --> ASP["Environmental aspect"]
    ASP --> IMP["Environmental impact"]
    IMP --> SIG["Rate significance"]
    SIG --> CTRL["Control significant aspects"]
    SIG --> OBJ["Feed objectives"]
```

Remember: policy sets the intent; the **aspects and impacts register** is
where that intent meets reality - it is the input to everything downstream.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental policy, aspects and impacts",
            (
                q(
                    "What three commitments must an ISO 14001 environmental policy include?",
                    (
                        opt("Profit, growth and market share"),
                        opt(
                            "Protection of the environment, fulfilment of compliance "
                            "obligations, and continual improvement",
                            correct=True,
                        ),
                        opt("Zero emissions, zero waste and zero water use"),
                        opt("Certification, marketing and reporting"),
                    ),
                    "Those three commitments are mandatory content of the policy under ISO 14001.",
                ),
                q(
                    "What is the difference between an aspect and an impact?",
                    (
                        opt("They are two words for the same thing"),
                        opt(
                            "An aspect is the element of your activity that interacts "
                            "with the environment; the impact is the resulting change",
                            correct=True,
                        ),
                        opt("An aspect is legal, an impact is illegal"),
                        opt("An aspect is measured, an impact is not"),
                    ),
                    "Aspect = cause you control (e.g. a discharge); impact = consequence. "
                    "A wastewater discharge is the aspect; the oxygen depletion in the "
                    "receiving river is the impact.",
                ),
                q(
                    "Why rate aspects for 'significance'?",
                    (
                        opt("To publish a longer register"),
                        opt(
                            "To prioritise - so control effort and objectives focus on "
                            "the significant aspects first",
                            correct=True,
                        ),
                        opt("Because ISO forbids managing minor aspects"),
                        opt("To calculate fines automatically"),
                    ),
                    "Significance (severity x likelihood x legal/stakeholder weight) "
                    "drives prioritisation of the significant aspects.",
                ),
            ),
        ),
        # -- 3. Objectives, targets and indicators ---------------------
        _t(
            "Objectives, targets and indicators",
            "11 min",
            """# Objectives, targets and indicators

A policy commitment is worthless until it becomes a **number you track**.
ISO 14001 requires **environmental objectives** at relevant functions and
levels, consistent with the policy and, crucially, **measurable** where
practicable. **ISO 14031** (environmental performance evaluation) gives the
vocabulary of **indicators**.

Three families of indicator:

- **Management Performance Indicators (MPIs)** - how well the system runs:
  percent of audits closed on time, training hours, number of open
  nonconformities.
- **Operational Performance Indicators (OPIs)** - the physical performance:
  energy per unit, water per unit, waste per unit, emissions per unit.
- **Environmental Condition Indicators (ECIs)** - the state of the
  environment itself: ambient river BOD, local air PM concentration.

Good objectives are **SMART** and usually expressed as **intensity**
(normalized) figures so they stay comparable as output changes. A typical
operational indicator is a simple intensity ratio:

```text
Energy intensity  =  Total energy used (kWh)  /  Units of production
Water intensity   =  Total water used (m3)    /  Units of production
Carbon intensity  =  Total CO2e (t)           /  Units of production

Worked example
  Energy used this year        =  1,250,000 kWh
  Units produced               =    500,000 units
  Energy intensity             =  2.5 kWh per unit
  Prior year intensity         =  2.9 kWh per unit
  Improvement                  =  (2.9 - 2.5) / 2.9  =  13.8 percent
```

```python
def energy_intensity(total_kwh: float, units: float) -> float:
    # kWh consumed per unit of production
    return total_kwh / units


def pct_reduction(prior: float, current: float) -> float:
    # percent improvement of an intensity indicator, positive is better
    return (prior - current) / prior * 100.0


intensity = energy_intensity(1_250_000, 500_000)   # 2.5 kWh/unit
saving = pct_reduction(2.9, intensity)             # 13.8 percent
```

```mermaid
graph TD
    POL["Policy commitment"] --> OBJ["Set measurable objective"]
    OBJ --> IND["Choose indicator MPI OPI ECI"]
    IND --> BASE["Set baseline and target"]
    BASE --> TRACK["Track and normalize"]
    TRACK --> REVIEW["Review against target"]
    REVIEW --> OBJ
```

Remember: turn each policy commitment into a **measurable objective** with
a **baseline, a target, and an indicator** - preferably an intensity ratio
that survives changes in production volume.
""",
        ),
        quiz_lesson(
            "Quiz: Objectives, targets and indicators",
            (
                q(
                    "Which standard provides the vocabulary of environmental performance indicators?",
                    (
                        opt("ISO 9001"),
                        opt("ISO 14031", correct=True),
                        opt("ISO 27001"),
                        opt("ISO 50001"),
                    ),
                    "ISO 14031 covers environmental performance evaluation and its "
                    "indicator families (MPI, OPI, ECI).",
                ),
                q(
                    "Why express an objective as an intensity (per-unit) figure?",
                    (
                        opt("Because absolute totals are illegal"),
                        opt(
                            "So the indicator stays comparable as production volume "
                            "changes - improvement is not masked by output swings",
                            correct=True,
                        ),
                        opt("To make the number larger"),
                        opt("Because ISO forbids absolute values"),
                    ),
                    "Intensity normalizes for output so genuine efficiency gains are "
                    "visible even when volume changes.",
                ),
                q(
                    "A plant used 1,250,000 kWh to make 500,000 units. What is its energy intensity?",
                    (
                        opt("0.4 kWh per unit"),
                        opt("2.5 kWh per unit", correct=True),
                        opt("25 kWh per unit"),
                        opt("1.25 kWh per unit"),
                    ),
                    "1,250,000 / 500,000 = 2.5 kWh per unit.",
                ),
            ),
        ),
        # -- 4. Environmental auditing ---------------------------------
        _t(
            "Environmental auditing",
            "11 min",
            """# Environmental auditing

An **environmental audit** is a *systematic, documented, independent and
objective* examination of evidence to determine whether the EMS conforms to
planned arrangements and is effectively implemented. **ISO 19011** gives the
guidelines for auditing management systems - the same discipline applies
whether the audit is **internal** (first party), **supplier** (second
party), or **certification** (third party).

The key principle is **conformity assessed against a criterion, using
objective evidence**:

- **Audit criteria** - the yardstick: ISO 14001 clauses, legal
  requirements, the organization's own procedures.
- **Objective evidence** - records, interviews, observation, measurements.
- **Audit finding** - the result of comparing evidence to criteria; a
  finding is a **conformity** or a **nonconformity** (major or minor), or
  an **opportunity for improvement**.

Auditors must be **independent of the activity audited** and **competent**;
they gather a **representative sample** because you cannot check everything.
A finding is only valid if it is **traceable to evidence** - "you said X;
the procedure requires Y; record Z shows neither" - never opinion.

```text
Audit trail for one finding
------------------------------------------------------------
Criterion : ISO 14001 cl. 9.1 - monitoring of significant aspects
Evidence  : Effluent pH log has no entries for 12-18 March
Finding   : Minor nonconformity - monitoring not performed as
            required by procedure PR-07
Action    : Root-cause + corrective action, verified at next audit
```

```mermaid
graph LR
    PLAN["Plan audit scope and criteria"] --> COLLECT["Collect objective evidence"]
    COLLECT --> COMPARE["Compare evidence to criteria"]
    COMPARE --> FIND["Record findings"]
    FIND --> REPORT["Report and rate nonconformities"]
    REPORT --> CAPA["Corrective action and follow up"]
```

Remember: an audit is not fault-finding for its own sake - it is a
**structured comparison of evidence against criteria** that feeds the
corrective-action and improvement machinery.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental auditing",
            (
                q(
                    "Which standard gives guidelines for auditing management systems?",
                    (
                        opt("ISO 14001"),
                        opt("ISO 19011", correct=True),
                        opt("ISO 14040"),
                        opt("ISO 31000"),
                    ),
                    "ISO 19011 provides guidelines for auditing management systems, "
                    "including environmental ones.",
                ),
                q(
                    "What makes an audit finding valid?",
                    (
                        opt("The seniority of the auditor"),
                        opt(
                            "It is traceable to objective evidence compared against a "
                            "defined criterion, not opinion",
                            correct=True,
                        ),
                        opt("It is agreed by a vote"),
                        opt("It appears in every audit"),
                    ),
                    "Findings must be evidence-based: criterion + objective evidence, "
                    "never personal opinion.",
                ),
                q(
                    "What is the difference between a first-party and a third-party audit?",
                    (
                        opt("First party is illegal, third party is legal"),
                        opt(
                            "First party is an internal audit by the organization itself; "
                            "third party is by an independent certification body",
                            correct=True,
                        ),
                        opt("First party checks finances, third party checks safety"),
                        opt("There is no difference"),
                    ),
                    "First party = internal; second party = supplier/customer; third "
                    "party = independent certification.",
                ),
            ),
        ),
        # -- 5. Legal compliance and due diligence ---------------------
        _t(
            "Legal compliance and due diligence",
            "11 min",
            """# Legal compliance and due diligence

ISO 14001 calls legal and other requirements **compliance obligations**,
and it requires you to **identify them, have access to them, evaluate
compliance, and keep evidence** of that evaluation. Certification does not
grant a licence to operate - the **environmental permit / licence** does,
and the two run in parallel.

In Brazil the licensing chain (Politica Nacional do Meio Ambiente, Lei
6.938/1981, and CONAMA resolutions) is a good concrete model:

- **Licenca Previa (LP)** - prior/location licence: approves the concept and
  siting, based on the environmental impact study.
- **Licenca de Instalacao (LI)** - installation licence: authorizes
  construction against approved plans.
- **Licenca de Operacao (LO)** - operating licence: authorizes operation
  and sets the conditions and monitoring you must maintain.

A **compliance register** lists each obligation, its source, what it
requires, how you meet it, and the evidence - reviewed on a schedule
because law changes:

```text
Compliance obligations register (extract)
------------------------------------------------------------
Obligation      | Source            | Requirement       | Evidence
----------------|-------------------|-------------------|-----------
Effluent limits | LO condition 4.2  | pH 6-9, BOD < 60  | Lab reports
Air monitoring  | CONAMA resolution | Annual stack test | Test cert.
Waste manifests | State agency rule | Track hazardous   | MTR records
Water abstraction| Outorga (permit) | Max 50 m3 per day | Meter logs
```

**Due diligence** is the forward-looking cousin: before an acquisition,
loan, or land purchase, you investigate environmental risk and liability -
a **Phase I** desktop and site review, escalating to **Phase II** sampling
if red flags appear - so you do not inherit someone else's contamination or
fines. The **polluter-pays principle** means liability can follow the site
and the operator, sometimes retroactively.

```mermaid
graph TD
    IDENT["Identify obligations"] --> ACCESS["Maintain access to text"]
    ACCESS --> EVAL["Evaluate compliance periodically"]
    EVAL --> EVID["Keep evidence of evaluation"]
    EVID --> GAP["Gap to corrective action"]
    IDENT --> DD["Due diligence for deals and land"]
```

Remember: compliance is an **evaluated, evidenced obligation** - not an
assumption - and due diligence stops you buying a liability you cannot see.
""",
        ),
        quiz_lesson(
            "Quiz: Legal compliance and due diligence",
            (
                q(
                    "What does ISO 14001 require regarding compliance obligations?",
                    (
                        opt("Only that you keep a copy of the law somewhere"),
                        opt(
                            "That you identify them, evaluate compliance periodically, "
                            "and keep evidence of the evaluation",
                            correct=True,
                        ),
                        opt("That you achieve 100 percent compliance instantly"),
                        opt("Nothing - it is voluntary"),
                    ),
                    "Identify, access, evaluate, and evidence - compliance must be "
                    "actively evaluated, not assumed.",
                ),
                q(
                    "In the Brazilian model, which licence authorizes operation and sets ongoing conditions?",
                    (
                        opt("Licenca Previa (LP)"),
                        opt("Licenca de Instalacao (LI)"),
                        opt("Licenca de Operacao (LO)", correct=True),
                        opt("There is only one licence for everything"),
                    ),
                    "LP approves siting, LI authorizes construction, LO authorizes "
                    "operation and sets monitoring conditions.",
                ),
                q(
                    "What is the purpose of environmental due diligence before an acquisition?",
                    (
                        opt("To increase the purchase price"),
                        opt(
                            "To investigate environmental risk and liability so you do "
                            "not inherit hidden contamination or fines",
                            correct=True,
                        ),
                        opt("To obtain an ISO certificate"),
                        opt("To replace the operating licence"),
                    ),
                    "Phase I/II due diligence surfaces liabilities before you buy them; "
                    "polluter-pays can make liability follow the site.",
                ),
            ),
        ),
        # -- 6. Environmental liabilities ------------------------------
        _t(
            "Environmental liabilities",
            "11 min",
            """# Environmental liabilities

An **environmental liability** (passivo ambiental) is an obligation - often
future and uncertain - to remediate damage or restore the environment: a
contaminated site, an abandoned tailings dam, soil and groundwater
pollution, or the closure and rehabilitation of a facility. It is both an
environmental problem and, increasingly, a **line on the balance sheet**.

The core management flow for a contaminated site follows a **conceptual
site model** and the **source-pathway-receptor** logic - a risk exists only
when all three are linked:

- **Source** - the contamination (a leaking tank, a landfill).
- **Pathway** - how it travels (groundwater flow, dust, direct contact).
- **Receptor** - who or what is exposed (a well, a river, residents).

Break any link and you break the risk. Investigation (Phase I desktop ->
Phase II intrusive sampling -> detailed risk assessment) tells you whether
remediation is needed and how much.

```text
Provision for a contaminated-site liability (simplified)
------------------------------------------------------------
Estimated remediation cost (undiscounted) : R$ 4,000,000
Expected timing                           : over 5 years
Discount rate                             : 6 percent per year
Present value provision  = 4,000,000 / (1.06 ^ 5)
                         = 4,000,000 / 1.3382
                         = R$ 2,988,000  (approx.)
```

A **provision** is recognized when a past event creates a present
obligation that is probable and can be estimated - the estimate is
**discounted to present value** for long-dated cleanups. Under the
polluter-pays principle, liability can attach to the operator, the
landowner, and successors, so liabilities discovered in due diligence
directly affect deal value.

```mermaid
graph LR
    SRC["Source contamination"] --> PATH["Pathway of migration"]
    PATH --> REC["Receptor exposed"]
    REC --> RISK["Unacceptable risk"]
    RISK --> REMED["Remediate or break pathway"]
    RISK --> PROV["Provision on balance sheet"]
```

Remember: manage liabilities with the **source-pathway-receptor** model -
remediate or interrupt a link - and recognize the cost as a **discounted
provision**, because ignored liabilities compound financially and legally.
""",
        ),
        quiz_lesson(
            "Quiz: Environmental liabilities",
            (
                q(
                    "For an environmental risk to exist under the conceptual site model, what must be present?",
                    (
                        opt("Only a source of contamination"),
                        opt(
                            "A source, a pathway, and a receptor - all three linked",
                            correct=True,
                        ),
                        opt("A permit and a fine"),
                        opt("An ISO 14001 certificate"),
                    ),
                    "Source-pathway-receptor must all connect; break any link and the "
                    "risk is broken.",
                ),
                q(
                    "Why is a long-dated remediation liability discounted to present value?",
                    (
                        opt("To make it look smaller for marketing"),
                        opt(
                            "Because money spent years from now is worth less today - the "
                            "provision reflects the present value of future cost",
                            correct=True,
                        ),
                        opt("Because ISO 14001 requires a 6 percent rate"),
                        opt("Discounting is not allowed for liabilities"),
                    ),
                    "Provisions for cleanups occurring over years are discounted to "
                    "present value, e.g. cost / (1 + r) ^ n.",
                ),
                q(
                    "Under the polluter-pays principle, who can carry environmental liability?",
                    (
                        opt("Only the current government"),
                        opt(
                            "The operator, the landowner and successors - liability can "
                            "follow the site",
                            correct=True,
                        ),
                        opt("Nobody once the site is sold"),
                        opt("Only the original construction contractor"),
                    ),
                    "Liability can attach to operator, landowner and successors, which is "
                    "why due diligence matters before a deal.",
                ),
            ),
        ),
        # -- 7. Emergency preparedness and response --------------------
        _t(
            "Emergency preparedness and response",
            "10 min",
            """# Emergency preparedness and response

ISO 14001 clause **8.2** requires you to **establish, maintain and test**
processes for responding to potential emergency situations that can have an
environmental impact - a spill, a fire, a tank rupture, a treatment-plant
failure. Preparedness is planned *before* the bad day, because in the middle
of an incident there is no time to invent a procedure.

The management structure follows the classic loop **prevent -> prepare ->
respond -> recover -> learn**:

- **Prevent** - reduce the likelihood at source: bunding, secondary
  containment, interlocks, maintenance.
- **Prepare** - plans, roles, trained responders, spill kits, drills, and
  agreed notification chains to authorities.
- **Respond** - contain, control, and notify per the plan; protect
  receptors first.
- **Recover** - clean up, restore, and manage waste generated.
- **Learn** - investigate, and feed corrective action back into the EMS.

Preparedness is only real if it is **tested**. Drills and tabletop
exercises validate the plan and are themselves auditable records.

```text
Spill response - first-hour checklist (illustrative)
------------------------------------------------------------
1. Ensure personal safety and raise the alarm
2. Identify the substance and consult the safety data sheet
3. Stop the source if safe (close valve, upright the drum)
4. Contain - deploy booms, block drains, build a dyke
5. Notify - incident commander, then regulator per LO condition
6. Recover spilled material and contaminated absorbents as waste
7. Record everything - times, actions, quantities, photos
```

```mermaid
graph LR
    PREVENT["Prevent at source"] --> PREPARE["Prepare plans and drills"]
    PREPARE --> RESPOND["Respond and notify"]
    RESPOND --> RECOVER["Recover and clean up"]
    RECOVER --> LEARN["Learn and corrective action"]
    LEARN --> PREVENT
```

Remember: emergency preparedness is a **tested** process, not a binder on a
shelf - protect receptors first, notify per your obligations, and feed
every incident back into the system.
""",
        ),
        quiz_lesson(
            "Quiz: Emergency preparedness and response",
            (
                q(
                    "What does ISO 14001 clause 8.2 require for emergencies?",
                    (
                        opt("Nothing - emergencies are outside its scope"),
                        opt(
                            "To establish, maintain and periodically test processes for "
                            "responding to potential emergency situations",
                            correct=True,
                        ),
                        opt("Only to buy insurance"),
                        opt("To report every emergency to ISO"),
                    ),
                    "Clause 8.2 requires emergency preparedness and response processes "
                    "that are maintained and tested.",
                ),
                q(
                    "Why must emergency plans be tested with drills?",
                    (
                        opt("To use up the training budget"),
                        opt(
                            "A plan is only real if it works under pressure - drills "
                            "validate it and produce auditable evidence",
                            correct=True,
                        ),
                        opt("Because ISO forbids written plans"),
                        opt("To slow down production deliberately"),
                    ),
                    "Preparedness is validated by testing; untested plans fail on the real day.",
                ),
                q(
                    "In a spill response, what is an early priority once people are safe?",
                    (
                        opt("Publish a press release first"),
                        opt(
                            "Stop the source if safe and contain the spill to protect "
                            "receptors, then notify per obligations",
                            correct=True,
                        ),
                        opt("Wait until the next audit"),
                        opt("Dilute it into the nearest river"),
                    ),
                    "Protect people, stop the source, contain to protect receptors, then "
                    "notify - diluting into a river is itself an offence.",
                ),
            ),
        ),
        # -- 8. Continual improvement and ESG reporting ----------------
        _t(
            "Continuous improvement and ESG reporting",
            "11 min",
            """# Continual improvement and ESG reporting

The last clauses of ISO 14001 close the loop. **Nonconformity and
corrective action** (clause 10.2) require you to react to problems, contain
them, find **root cause**, and act to stop recurrence - not just fix the
symptom. **Management review** (clause 9.3) puts performance in front of top
leadership on a schedule, and **continual improvement** (clause 10.3) is the
obligation to keep raising the bar over time. This is the **Act** of PDCA.

The disciplined tool is **CAPA** - Corrective And Preventive Action - driven
by root-cause analysis (5 Whys, fishbone):

```text
Corrective action record (CAPA)
------------------------------------------------------------
Nonconformity : Effluent pH exceeded LO limit on 14 March
Containment   : Diverted to holding tank, re-tested before release
Root cause    : Dosing pump failed; no low-flow alarm configured
Corrective    : Install and test low-flow alarm; add to PM schedule
Preventive    : Review alarms on all dosing systems
Verification  : Confirmed effective at next internal audit
```

Externally, the same performance data feeds **ESG reporting** - the
Environmental, Social and Governance disclosure investors and regulators now
expect. Frameworks give it structure and comparability:

- **GRI** - the widely used sustainability reporting standards.
- **GHG Protocol** - greenhouse-gas accounting in **Scope 1** (direct),
  **Scope 2** (purchased energy), and **Scope 3** (value chain).
- **TCFD / ISSB (IFRS S2)** - climate-related financial disclosure.

The EMS is the **engine room** of credible ESG: the aspects register,
indicators, audits and CAPA are exactly the auditable evidence that stops a
report being greenwashing.

```mermaid
graph LR
    NC["Nonconformity"] --> RCA["Root cause analysis"]
    RCA --> CAPA["Corrective and preventive action"]
    CAPA --> MR["Management review"]
    MR --> CI["Continual improvement"]
    CI --> ESG["ESG reporting GRI and GHG Protocol"]
    ESG --> NC
```

Remember: improvement is **root-cause driven**, reviewed by leadership, and
never finished - and a working EMS is what turns ESG reporting from a
brochure into **evidence**.
""",
        ),
        quiz_lesson(
            "Quiz: Continuous improvement and ESG reporting",
            (
                q(
                    "What does effective corrective action require beyond fixing the immediate problem?",
                    (
                        opt("Blaming the operator on shift"),
                        opt(
                            "Finding and addressing the root cause so the nonconformity "
                            "does not recur",
                            correct=True,
                        ),
                        opt("Hiding the nonconformity from auditors"),
                        opt("Waiting for the next management review"),
                    ),
                    "CAPA is root-cause driven: contain, find root cause, act to prevent "
                    "recurrence, then verify effectiveness.",
                ),
                q(
                    "In the GHG Protocol, what are Scope 1, 2 and 3 emissions?",
                    (
                        opt("Small, medium and large emissions"),
                        opt(
                            "Direct emissions, purchased-energy emissions, and value-chain "
                            "emissions respectively",
                            correct=True,
                        ),
                        opt("Past, present and future emissions"),
                        opt("Air, water and soil emissions"),
                    ),
                    "Scope 1 = direct; Scope 2 = purchased energy; Scope 3 = upstream and "
                    "downstream value chain.",
                ),
                q(
                    "How does a working EMS support credible ESG reporting?",
                    (
                        opt("It replaces the need to report at all"),
                        opt(
                            "Its aspects register, indicators, audits and CAPA provide "
                            "auditable evidence that guards against greenwashing",
                            correct=True,
                        ),
                        opt("It guarantees a perfect score automatically"),
                        opt("It hides poor performance from investors"),
                    ),
                    "The EMS is the engine room: it produces the auditable evidence that "
                    "makes ESG disclosure credible rather than marketing.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "What does ISO 14001 specify?",
                    (
                        opt("Numeric pollution limits for every industry"),
                        opt(
                            "The requirements for an environmental management system built "
                            "on the Plan-Do-Check-Act cycle",
                            correct=True,
                        ),
                        opt("A carbon tax schedule"),
                        opt("Approved remediation contractors"),
                    ),
                    "ISO 14001 sets EMS requirements around PDCA; limits come from law "
                    "and permits.",
                ),
                q(
                    "Which three commitments are mandatory in an ISO 14001 environmental policy?",
                    (
                        opt("Growth, profit and dividends"),
                        opt(
                            "Protection of the environment, fulfilment of compliance "
                            "obligations, and continual improvement",
                            correct=True,
                        ),
                        opt("Certification, audit and reporting"),
                        opt("Zero water, zero waste and zero energy"),
                    ),
                    "Those three commitments are required policy content.",
                ),
                q(
                    "A boiler flue-gas emission is the aspect. What is the impact?",
                    (
                        opt("The boiler itself"),
                        opt(
                            "Reduced local air quality - the resulting change to the environment",
                            correct=True,
                        ),
                        opt("The maintenance schedule"),
                        opt("The fuel invoice"),
                    ),
                    "Aspect = the emission you control; impact = the change it causes "
                    "(reduced air quality).",
                ),
                q(
                    "Why express environmental objectives as intensity (per-unit) indicators?",
                    (
                        opt("To make totals disappear"),
                        opt(
                            "So performance stays comparable as production volume changes",
                            correct=True,
                        ),
                        opt("Because absolute values are banned"),
                        opt("To avoid setting a baseline"),
                    ),
                    "Intensity normalizes for output, so efficiency gains are not masked "
                    "by volume swings.",
                ),
                q(
                    "What makes an audit finding valid under ISO 19011?",
                    (
                        opt("The auditor's rank"),
                        opt(
                            "It compares objective evidence against a defined criterion - "
                            "it is traceable, not opinion",
                            correct=True,
                        ),
                        opt("A majority vote of the audited team"),
                        opt("It appears in the previous report"),
                    ),
                    "Findings are evidence-based: criterion plus objective evidence.",
                ),
                q(
                    "What must an organization do about its compliance obligations under ISO 14001?",
                    (
                        opt("Assume compliance and move on"),
                        opt(
                            "Identify them, evaluate compliance periodically, and keep "
                            "evidence of the evaluation",
                            correct=True,
                        ),
                        opt("Report them only if fined"),
                        opt("Delegate them entirely to auditors"),
                    ),
                    "Compliance must be actively evaluated and evidenced, not assumed.",
                ),
                q(
                    "In the source-pathway-receptor model, how do you remove a contamination risk?",
                    (
                        opt("By buying insurance only"),
                        opt(
                            "By breaking any one of the three links - remove the source, "
                            "interrupt the pathway, or protect the receptor",
                            correct=True,
                        ),
                        opt("By renaming the site"),
                        opt("By ignoring the receptor"),
                    ),
                    "Risk needs all three linked; breaking one link breaks the risk.",
                ),
                q(
                    "Why is a long-dated remediation liability discounted?",
                    (
                        opt("To hide it from regulators"),
                        opt(
                            "Because future cost is worth less today - the provision "
                            "reflects present value",
                            correct=True,
                        ),
                        opt("Because ISO requires a fixed rate"),
                        opt("Discounting liabilities is prohibited"),
                    ),
                    "Provisions for multi-year cleanups are discounted to present value.",
                ),
                q(
                    "What does ISO 14001 require for emergency preparedness?",
                    (
                        opt("Only an insurance policy"),
                        opt(
                            "Processes to respond to potential emergencies that are "
                            "maintained and periodically tested",
                            correct=True,
                        ),
                        opt("Nothing at all"),
                        opt("Reporting every drill to ISO"),
                    ),
                    "Clause 8.2 requires tested, maintained emergency response processes.",
                ),
                q(
                    "In the GHG Protocol, Scope 2 emissions are…",
                    (
                        opt("direct emissions from owned sources"),
                        opt("emissions from purchased energy such as electricity", correct=True),
                        opt("value-chain emissions from suppliers and product use"),
                        opt("emissions to water only"),
                    ),
                    "Scope 1 direct, Scope 2 purchased energy, Scope 3 value chain.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

ENVIRONMENTAL_MANAGEMENT_AUDITING_COURSES: tuple[SeedCourse, ...] = (
    _ENVIRONMENTAL_MANAGEMENT_AUDITING,
)
