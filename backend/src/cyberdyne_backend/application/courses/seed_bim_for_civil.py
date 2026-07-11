"""Academy seed content - BIM for Civil Engineering.

Building Information Modeling as a digital delivery method for civil and
infrastructure projects: BIM concepts and maturity levels, parametric
modeling with families and levels of development, discipline models and
quantity extraction, IFC and openBIM interoperability, the common data
environment, multidisciplinary coordination and clash detection, 4D
scheduling and 5D cost, and BIM for infrastructure (CIM) with digital
handover. Every lesson is a direct explanation with a real IFC, schedule
or process example and a mermaid diagram, followed by a checkpoint quiz;
the course closes with a comprehensive final quiz.
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


_BIM_FOR_CIVIL = SeedCourse(
    slug="bim-for-civil",
    title="BIM for Civil Engineering",
    description=(
        "Building Information Modeling for civil and infrastructure projects: "
        "parametric models, IFC and openBIM interoperability, the common data "
        "environment, multidisciplinary coordination and clash detection, and "
        "4D/5D delivery - with real IFC snippets, schedules and diagrams in "
        "every lesson."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# BIM for Civil Engineering

**Building Information Modeling (BIM)** is not just 3D drawing - it is a
way of delivering a project as a coordinated, data-rich digital model that
carries geometry *and* information from design through construction into
operation. For civil and infrastructure work - roads, bridges, drainage,
earthworks, utilities - this modern digital delivery replaces stacks of
disconnected 2D drawings with a single shared source of truth.

The approach here is **concrete and standards-based**: every lesson
explains one idea directly, shows it in a real example (an IFC snippet, a
quantity schedule, a process), and draws it as a diagram. After each
lesson there is a short quiz; a final quiz covers the whole course.

What you will build understanding for, in order:

1. **BIM concepts and maturity levels** - what BIM is and how it grew up
2. **Parametric modeling, families and LOD** - smart objects and detail
3. **Discipline models and quantity extraction** - takeoff from the model
4. **Interoperability and IFC / openBIM** - the open exchange standard
5. **The Common Data Environment (CDE)** - one place for the information
6. **Coordination and clash detection** - finding conflicts before site
7. **4D scheduling and 5D cost** - time and money linked to the model
8. **BIM for infrastructure (CIM) and digital handover** - linear assets
   and the operational deliverable

Modern practice leans on **open standards** - **ISO 19650** for
information management, **IFC** for exchange - so the workflow is
vendor-neutral. Know the map, and each authoring tool becomes just an
editor over the same shared model.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is BIM, fundamentally?",
                    (
                        opt("A single 3D drawing program"),
                        opt("A file format for images"),
                        opt(
                            "A way of delivering a project as a coordinated, data-rich "
                            "digital model carrying geometry and information across the "
                            "whole lifecycle",
                            correct=True,
                        ),
                        opt("A type of concrete admixture"),
                    ),
                    "BIM is a process and a model that carries information from design "
                    "to operation - not merely 3D geometry.",
                ),
                q(
                    "Which two open standards underpin the modern, vendor-neutral BIM "
                    "workflow taught here?",
                    (
                        opt("PDF and DWG"),
                        opt(
                            "ISO 19650 for information management and IFC for open exchange",
                            correct=True,
                        ),
                        opt("JPEG and MP4"),
                        opt("HTML and CSS"),
                    ),
                    "ISO 19650 governs how information is managed; IFC is the open "
                    "buildingSMART exchange schema.",
                ),
            ),
        ),
        # -- 1. Concepts and maturity ----------------------------------
        _t(
            "BIM concepts and maturity levels",
            "9 min",
            """# BIM concepts and maturity levels

At its core, BIM replaces the drawing with the **model**: instead of lines
on a sheet, you place **objects** - a wall, a pile, a manhole - that know
what they are and carry **attributes** (material, dimensions, load rating,
cost code). Drawings, schedules and reports are then *views* generated
from that single model, so they stay consistent.

Maturity is commonly described as **levels 0 to 3**, popularized by the UK
BIM programme:

- **Level 0** - unmanaged 2D CAD, paper-based exchange. No collaboration.
- **Level 1** - managed CAD in 2D or 3D, a shared standard and file naming,
  but models are not yet combined across disciplines.
- **Level 2** - each discipline authors its own 3D model; they are exchanged
  in a common format (IFC) and federated for coordination. Information is
  managed to a standard. This is the current baseline for most tenders.
- **Level 3** - a single shared model in an open, cloud environment, worked
  on collaboratively in real time. The direction of travel.

The word "dimensions" also grows: **3D** geometry, **4D** time, **5D**
cost, and often **6D** operation/facility management.

```mermaid
graph LR
    L0["Level 0 paper 2D CAD"] --> L1["Level 1 managed CAD"]
    L1 --> L2["Level 2 federated IFC models"]
    L2 --> L3["Level 3 shared open model"]
    L2 --> DIMS["3D 4D 5D 6D data"]
```

A simple attribute record shows why the model beats the drawing - the same
object can answer geometry, cost and scheduling questions at once:

```text
Object: Bored pile P-14
  Type            : Reinforced concrete bored pile
  Diameter        : 800 mm
  Length          : 18.0 m
  Concrete class  : C30/37
  Cost code       : 03-31-00
  Planned pour    : 2026-03-14 (linked to schedule task E-210)
```

Remember: BIM is model-first. Get the objects and their data right and the
drawings, quantities and schedules follow automatically.
""",
        ),
        quiz_lesson(
            "Quiz: BIM concepts and maturity levels",
            (
                q(
                    "In BIM, what is the relationship between the model and the drawings?",
                    (
                        opt("Drawings are authored first, then traced into a model"),
                        opt(
                            "Drawings, schedules and reports are views generated from a "
                            "single data-rich model, so they stay consistent",
                            correct=True,
                        ),
                        opt("They are unrelated files kept in separate folders"),
                        opt("The model is only a render with no data"),
                    ),
                    "Model-first: views (drawings, schedules) are derived from the model, "
                    "which keeps them coordinated.",
                ),
                q(
                    "What best describes BIM maturity Level 2?",
                    (
                        opt("Unmanaged paper-based 2D CAD"),
                        opt("A single shared cloud model edited in real time by all"),
                        opt(
                            "Each discipline authors its own 3D model, exchanged in a "
                            "common format (IFC) and federated for coordination",
                            correct=True,
                        ),
                        opt("No models at all, only spreadsheets"),
                    ),
                    "Level 2 = separate managed discipline models, exchanged and "
                    "federated - the common tender baseline. Level 3 is the single "
                    "shared model.",
                ),
                q(
                    "What does the '4D' dimension of BIM add?",
                    (
                        opt("Cost"),
                        opt("Time - linking the model to the construction schedule", correct=True),
                        opt("A fourth spatial axis"),
                        opt("Facility management"),
                    ),
                    "3D geometry, 4D time, 5D cost, 6D operation.",
                ),
            ),
        ),
        # -- 2. Parametric, families, LOD ------------------------------
        _t(
            "Parametric modeling, families and levels of development (LOD)",
            "10 min",
            """# Parametric modeling, families and levels of development (LOD)

BIM objects are **parametric**: their geometry is driven by **parameters**
and **rules**, not fixed lines. Change a girder's span and its length,
weight and connection geometry update; change a wall type and every
instance follows. This is what makes a model editable and reliable rather
than a brittle drawing.

Reusable object definitions are called **families** (Revit) or **types**;
each has parameters you set per instance. A civil library might hold
families for piles, culverts, guardrails, drainage pits and pavement
build-ups.

A tiny parametric definition, expressed as code, shows the idea - the
object computes properties from its parameters:

```python
# Parametric rectangular RC beam - geometry and quantities from parameters
def rc_beam(span_m, width_mm, depth_mm, rebar_ratio=0.015):
    volume_m3 = span_m * (width_mm / 1000) * (depth_mm / 1000)
    concrete_kg = volume_m3 * 2400          # C30/37 density
    steel_kg = volume_m3 * rebar_ratio * 7850
    return {"volume_m3": round(volume_m3, 3),
            "concrete_kg": round(concrete_kg),
            "steel_kg": round(steel_kg)}

rc_beam(8.0, 300, 600)   # -> volume 1.44 m3, ~3456 kg concrete, ~169 kg steel
```

How much *detail* an object carries is its **Level of Development (LOD)** -
an AIA scale that separates geometry richness from information:

- **LOD 100** - conceptual; a symbol or massing, no real dimensions.
- **LOD 200** - approximate size, shape and location; generic.
- **LOD 300** - precise geometry, specific dimensions and orientation.
- **LOD 350** - LOD 300 plus interfaces/connections to other elements.
- **LOD 400** - fabrication and assembly detail, ready for shop drawings.
- **LOD 500** - as-built, verified for operation.

A related idea, **Level of Information Need** (ISO 19650), reminds you to
model only to the detail the *purpose* requires - over-modeling wastes
effort.

```mermaid
graph LR
    PARAM["Parameters and rules"] --> FAM["Family or type"]
    FAM --> INST["Instances in the model"]
    INST --> LOD["Level of development"]
    LOD --> USE["Fit the modeling to the purpose"]
```

Remember: parameters make objects smart and editable; LOD tells everyone
how much to trust the geometry and data at each stage.
""",
        ),
        quiz_lesson(
            "Quiz: Parametric modeling, families and levels of development (LOD)",
            (
                q(
                    "What makes a BIM object 'parametric'?",
                    (
                        opt("It is drawn with fixed, unchangeable lines"),
                        opt(
                            "Its geometry and properties are driven by parameters and "
                            "rules, so changing a value updates the object",
                            correct=True,
                        ),
                        opt("It has a photorealistic material"),
                        opt("It is stored as a raster image"),
                    ),
                    "Parameters and rules drive the geometry - editable and consistent, "
                    "unlike static drawn lines.",
                ),
                q(
                    "What does Level of Development (LOD) describe?",
                    (
                        opt("The file size of the model"),
                        opt("The number of disciplines involved"),
                        opt(
                            "How much geometric and information detail an element carries "
                            "at a given stage, e.g. LOD 300 precise, LOD 400 fabrication",
                            correct=True,
                        ),
                        opt("The software version used"),
                    ),
                    "LOD is a maturity scale for an element from conceptual (100) to "
                    "as-built (500).",
                ),
                q(
                    "Why does 'Level of Information Need' (ISO 19650) matter?",
                    (
                        opt("It requires maximum detail everywhere"),
                        opt(
                            "It reminds you to model only to the detail the purpose "
                            "requires, avoiding wasteful over-modeling",
                            correct=True,
                        ),
                        opt("It sets the render resolution"),
                        opt("It defines the file naming only"),
                    ),
                    "Model fit-for-purpose: too much detail too early wastes effort.",
                ),
            ),
        ),
        # -- 3. Discipline models & quantities -------------------------
        _t(
            "Discipline models and quantity extraction",
            "10 min",
            """# Discipline models and quantity extraction

On a real project each discipline authors its **own model** - structures,
architecture, MEP, drainage, earthworks, roads - to a shared coordinate
system and standard. These are combined into a **federated model** for
coordination, but stay separately owned so each team controls its own
data. The **BIM Execution Plan (BEP)** records who owns what, the modeling
standards, LOD and exchange formats.

Because every object carries quantities, **takeoff** (quantity extraction)
becomes a query over the model rather than manual counting from drawings -
faster and far less error-prone. This is the heart of **5D** costing.

A quantity schedule pulled from a structural model looks like this - each
row is computed from the objects, not typed by hand:

```text
Bill item      Element type          Count   Qty       Unit
---------------------------------------------------------------
03-31-00       Bored pile D800        42      756.0    m
03-30-00       Pile cap C30/37        14       98.5    m3
03-30-00       Ground beam            26      141.2    m3
05-12-00       Steel girder S355      12       88.4    t
03-30-00       Deck slab C35/45        1      312.0    m3
```

Two cautions keep takeoff trustworthy:

- **Model to a consistent method of measurement** - agree units and rules
  (for example NBR 12721 or a standard method of measurement) so quantities
  map cleanly to bill items.
- **Classify every object** - attach a classification code (Uniclass,
  OmniClass or a project cost code) so quantities aggregate correctly.

```mermaid
graph TD
    STRUCT["Structures model"] --> FED["Federated model"]
    ARCH["Architecture model"] --> FED
    DRAIN["Drainage model"] --> FED
    EARTH["Earthworks model"] --> FED
    FED --> QTO["Quantity takeoff query"]
    QTO --> BOQ["Bill of quantities"]
```

Remember: separate ownership, federated view. Because objects carry
quantities and classification, the bill of quantities is generated from
the model - keep the classification clean and it stays reliable.
""",
        ),
        quiz_lesson(
            "Quiz: Discipline models and quantity extraction",
            (
                q(
                    "How are discipline models typically organized on a BIM project?",
                    (
                        opt("One giant file everyone edits at once"),
                        opt(
                            "Each discipline authors its own model to a shared "
                            "coordinate system; they are federated for coordination but "
                            "stay separately owned",
                            correct=True,
                        ),
                        opt("Only the architect models; others use paper"),
                        opt("Every discipline keeps its model in a private format nobody shares"),
                    ),
                    "Separate ownership, federated view - each team controls its own "
                    "data while models are combined for coordination.",
                ),
                q(
                    "Why is quantity takeoff from a BIM model more reliable than manual takeoff?",
                    (
                        opt("Because the model is prettier"),
                        opt(
                            "Quantities are computed from the objects themselves rather "
                            "than counted by hand from drawings, reducing error",
                            correct=True,
                        ),
                        opt("Because it ignores the geometry"),
                        opt("Because it needs no classification"),
                    ),
                    "Takeoff becomes a query over object data - the basis of 5D costing.",
                ),
                q(
                    "What must you attach to objects so quantities aggregate into the "
                    "right bill items?",
                    (
                        opt("A render material"),
                        opt("A photograph"),
                        opt(
                            "A classification code such as Uniclass, OmniClass or a "
                            "project cost code",
                            correct=True,
                        ),
                        opt("A file path"),
                    ),
                    "Classification lets quantities roll up correctly against the "
                    "method of measurement.",
                ),
            ),
        ),
        # -- 4. Interoperability / IFC / openBIM -----------------------
        _t(
            "Interoperability and IFC / openBIM",
            "11 min",
            """# Interoperability and IFC / openBIM

Different teams use different authoring tools, and a project outlives any
one of them. **openBIM** is the principle of exchanging models through
**open, vendor-neutral standards** so no one is locked in and the data
survives. The central standard is **IFC (Industry Foundation Classes)**,
an open schema from **buildingSMART**, standardized as **ISO 16739**.

An IFC file describes objects as typed entities (**IfcPile**, **IfcBeam**,
**IfcWall**) with properties, relationships and geometry - so a model
authored in one tool can be read faithfully in another. A simplified STEP
(.ifc) snippet:

```text
#41 = IFCPROJECT('0aB...',#5,'Ring Road Bridge',$,$,$,$,(#12),#9);
#88 = IFCPILE('2xY...',#5,'Bored pile P-14',$,'D800',
              #90,#95,'P-14',.BORED.,.FRICTION.,$);
#95 = IFCPROPERTYSET('3kL...',#5,'Pset_PileCommon',$,(#96,#97));
#96 = IFCPROPERTYSINGLEVALUE('Diameter',$,IFCLENGTHMEASURE(800.),$);
#97 = IFCPROPERTYSINGLEVALUE('LoadBearing',$,IFCBOOLEAN(.T.),$);
```

Two more openBIM standards complete the exchange:

- **BCF (BIM Collaboration Format)** - carries *issues* (a clash, a query)
  as small files with a viewpoint and comments, separate from the heavy
  model. It is how coordination comments travel between tools.
- **IDS (Information Delivery Specification)** - a machine-readable way to
  state and *check* what information must be present (for example "every
  pile must have a Diameter and a LoadBearing property"), so you can
  validate a delivered IFC automatically.

Exchange needs are pinned by an **MVD (Model View Definition)** - a subset
of IFC for a purpose (for example coordination view) - so tools agree on
what to export.

```mermaid
graph LR
    A["Authoring tool A"] --> IFC["IFC open model"]
    B["Authoring tool B"] --> IFC
    IFC --> IDS["Validate against IDS"]
    IFC --> COORD["Coordination tool"]
    COORD --> BCF["BCF issues back to authors"]
```

Remember: openBIM keeps the data vendor-neutral and durable. IFC carries
the model, IDS says what must be in it, and BCF carries the conversation
about it.
""",
        ),
        quiz_lesson(
            "Quiz: Interoperability and IFC / openBIM",
            (
                q(
                    "What is IFC?",
                    (
                        opt("A proprietary format owned by one software vendor"),
                        opt(
                            "An open, vendor-neutral schema from buildingSMART (ISO "
                            "16739) for exchanging BIM models between tools",
                            correct=True,
                        ),
                        opt("A rendering engine"),
                        opt("A type of steel connection"),
                    ),
                    "IFC is the open exchange standard at the heart of openBIM - it "
                    "keeps model data portable and durable.",
                ),
                q(
                    "What is BCF used for?",
                    (
                        opt("Storing the full heavy geometry"),
                        opt(
                            "Carrying coordination issues - a viewpoint plus comments - "
                            "between tools, separately from the model",
                            correct=True,
                        ),
                        opt("Rendering photorealistic images"),
                        opt("Compressing the IFC file"),
                    ),
                    "BCF = BIM Collaboration Format: it moves the conversation (clashes, "
                    "queries) without moving the whole model.",
                ),
                q(
                    "What does an IDS (Information Delivery Specification) let you do?",
                    (
                        opt("Draw the geometry automatically"),
                        opt("Replace the IFC file"),
                        opt(
                            "State and automatically check what information must be "
                            "present in a delivered model, e.g. required properties",
                            correct=True,
                        ),
                        opt("Schedule the construction"),
                    ),
                    "IDS makes the information requirement machine-checkable, so you can "
                    "validate an IFC delivery.",
                ),
            ),
        ),
        # -- 5. CDE ----------------------------------------------------
        _t(
            "The Common Data Environment (CDE)",
            "10 min",
            """# The Common Data Environment (CDE)

If Level 2 BIM means many models and many parties, where does all the
information live? In the **Common Data Environment (CDE)** - the single
agreed source of information for the project, defined by **ISO 19650**.
Every model, drawing, document and issue passes through it, with managed
access, versioning and an audit trail.

The CDE is organized around an information **workflow with four states**,
and information moves between them through controlled **gates**:

- **Work in Progress (WIP)** - a team's own draft, not yet shared. Private.
- **Shared** - checked and released for other disciplines to use and
  coordinate against, but not yet a contractual deliverable.
- **Published** - reviewed and authorized information, issued for use
  (for construction, for approval).
- **Archived** - a retained record of every previous state - the audit
  trail. Nothing is truly deleted.

Moving from WIP to Shared, and Shared to Published, is a **check/approve
gate**, not a copy - a person authorizes the transition.

A file naming and status convention makes the state explicit, for example:

```text
PRJ-CYB-BR-XX-M3-ST-0001-S3-P02.ifc
  PRJ-CYB   project and originator
  BR-XX     volume/system and level
  M3-ST     3D model, structures
  0001      number
  S3        status code S3 = shared for coordination
  P02       revision P02 (P = preliminary)
```

```mermaid
graph LR
    WIP["Work in progress private"] --> GATE1["Check and share"]
    GATE1 --> SHARED["Shared for coordination"]
    SHARED --> GATE2["Review and authorize"]
    GATE2 --> PUB["Published for use"]
    PUB --> ARCH["Archived record"]
```

Remember: the CDE is the one place the project's information lives, and the
WIP -> Shared -> Published -> Archived states, with gates between them,
keep everyone working from trusted, versioned data.
""",
        ),
        quiz_lesson(
            "Quiz: The Common Data Environment (CDE)",
            (
                q(
                    "What is the Common Data Environment (CDE)?",
                    (
                        opt("A rendering plugin"),
                        opt(
                            "The single agreed source of information for a project "
                            "(per ISO 19650) with managed access, versioning and audit",
                            correct=True,
                        ),
                        opt("A private folder on one engineer's laptop"),
                        opt("A type of concrete mix"),
                    ),
                    "The CDE is where all project information lives and is managed - "
                    "defined by ISO 19650.",
                ),
                q(
                    "What are the four information states in an ISO 19650 CDE workflow?",
                    (
                        opt("Draft, final, deleted, printed"),
                        opt(
                            "Work in Progress, Shared, Published, Archived",
                            correct=True,
                        ),
                        opt("Design, build, operate, demolish"),
                        opt("Red, amber, green, blue"),
                    ),
                    "WIP (private) -> Shared (for coordination) -> Published (authorized) "
                    "-> Archived (record).",
                ),
                q(
                    "What happens at the gate between Shared and Published?",
                    (
                        opt("Files are automatically deleted"),
                        opt("The model is rendered"),
                        opt(
                            "A person reviews and authorizes the information before it "
                            "becomes a published deliverable",
                            correct=True,
                        ),
                        opt("The project is archived and closed"),
                    ),
                    "Transitions are check/approve gates authorized by a person, not "
                    "silent copies.",
                ),
            ),
        ),
        # -- 6. Coordination & clash detection -------------------------
        _t(
            "Multidisciplinary coordination and clash detection",
            "10 min",
            """# Multidisciplinary coordination and clash detection

The biggest early payoff of BIM is catching conflicts **in the model
instead of on site**, where a rework can cost orders of magnitude more.
Disciplines are combined into a **federated model** and checked for
interferences - **clash detection**.

Clashes come in three kinds:

- **Hard clash** - two elements occupy the same space (a drainage pipe runs
  through a pile cap). A physical impossibility.
- **Soft clash (clearance)** - elements are too close, violating a required
  gap or maintenance/cover zone (a duct with no access clearance).
- **Workflow/4D clash** - a scheduling conflict in time or space (two
  trades needing the same area in the same week) - seen when the schedule
  is linked (next lesson).

A clash test is a rule between two element sets with a tolerance:

```text
Clash test:  Drainage pipes  vs  Structural pile caps
  Type       : Hard
  Tolerance  : 10 mm
  Results    : 3 clashes
    C-001  Pipe DN300 @ ch.1+240  intersects  Pile cap PC-07  (approve->assign)
    C-002  Pipe DN300 @ ch.1+318  intersects  Ground beam GB-3
    C-003  Manhole MH-12          intersects  Pile P-31
  Action     : raise BCF issue -> assign to drainage -> re-check next round
```

Coordination is a **cycle**, run on a regular (often weekly) rhythm: run
the tests, triage real clashes from noise, raise each as a **BCF issue**
assigned to the responsible discipline, resolve in the authoring tool,
then re-federate and re-check until clean. Small tolerances and good object
classification keep the noise down.

```mermaid
graph TD
    FED["Federated model"] --> RUN["Run clash tests"]
    RUN --> TRIAGE["Triage real clashes"]
    TRIAGE --> BCF["Raise BCF issues"]
    BCF --> FIX["Fix in authoring tools"]
    FIX --> RECHK["Re-federate and re-check"]
    RECHK --> FED
```

Remember: federate, clash-test, triage, assign via BCF, fix, re-check.
Resolving conflicts digitally on a regular cycle is what turns coordinated
models into a buildable design.
""",
        ),
        quiz_lesson(
            "Quiz: Multidisciplinary coordination and clash detection",
            (
                q(
                    "What is a 'hard clash'?",
                    (
                        opt("Two elements that are too close but not touching"),
                        opt(
                            "Two elements occupying the same physical space, e.g. a pipe "
                            "running through a pile cap",
                            correct=True,
                        ),
                        opt("A disagreement between two engineers"),
                        opt("A scheduling conflict in time"),
                    ),
                    "Hard = geometric overlap. Soft = clearance violation. "
                    "Workflow/4D = a time-space conflict.",
                ),
                q(
                    "What is the main value of clash detection?",
                    (
                        opt("Making the model render faster"),
                        opt(
                            "Catching conflicts in the model before construction, when "
                            "fixing them is far cheaper than reworking on site",
                            correct=True,
                        ),
                        opt("Reducing the number of disciplines"),
                        opt("Replacing the need for a schedule"),
                    ),
                    "Finding clashes digitally avoids expensive on-site rework - BIM's "
                    "biggest early payoff.",
                ),
                q(
                    "How does a resolved clash typically travel back to the responsible "
                    "discipline?",
                    (
                        opt("As a printed drawing mailed to them"),
                        opt("It cannot be tracked"),
                        opt(
                            "As a BCF issue with a viewpoint, assigned to the discipline, "
                            "then fixed and re-checked on the next coordination round",
                            correct=True,
                        ),
                        opt("By deleting the clashing element automatically"),
                    ),
                    "Coordination is a cycle: run, triage, assign via BCF, fix, "
                    "re-federate, re-check.",
                ),
            ),
        ),
        # -- 7. 4D / 5D ------------------------------------------------
        _t(
            "4D scheduling and 5D cost",
            "10 min",
            """# 4D scheduling and 5D cost

Once the geometry is coordinated, you connect it to **time** and **money**.
**4D** links model elements to **schedule tasks**; **5D** links them to
**cost**. Because the link is by object, both stay consistent with the
design as it changes.

**4D scheduling** ties each element to an activity so you can play the
build as an animation - see the sequence, spot when two trades need the
same space, and communicate the plan clearly. The link is a simple
mapping between the schedule and model objects:

```text
Task ID  Activity                Start        Finish       Linked objects
-------------------------------------------------------------------------
E-210    Bored piling axis A-D   2026-03-02   2026-03-27   Piles P-01..P-20
E-220    Pile caps axis A-D      2026-03-23   2026-04-10   Caps PC-01..PC-07
E-230    Ground beams            2026-04-06   2026-04-24   Beams GB-1..GB-9
E-240    Deck slab pour          2026-04-27   2026-05-08   Slab S-1
```

Playing this sequence exposes a **workflow clash**: piling (E-210) and pile
caps (E-220) overlap on the same axis for several days - resolve by
sequencing or splitting the work zone.

**5D cost** attaches rates to classified quantities, so the estimate is
generated from the model and updates when quantities change. A worked line:

```text
5D cost line - deck slab
  Quantity from model : 312.0 m3   (IfcSlab, C35/45)
  Unit rate           : 185.00 /m3 (concrete supply + place + finish)
  Reinforcement       : 46.8 t  x  1250.00 /t
  Slab cost           : 312.0 x 185.00  +  46.8 x 1250.00  =  116,220.00
```

Change the slab thickness and both the 3D volume and this 5D line move
together - no manual re-pricing.

```mermaid
graph LR
    MODEL["Coordinated 3D model"] --> D4["Link to schedule 4D"]
    MODEL --> D5["Link to cost 5D"]
    D4["Link to schedule 4D"] --> SEQ["Sequence and workflow clashes"]
    D5["Link to cost 5D"] --> EST["Model driven estimate"]
    SEQ --> PLAN["Reliable construction plan"]
    EST --> PLAN
```

Remember: 4D makes the plan visible in time and 5D makes cost follow the
model. Because both link by object, time and money stay consistent with
the design.
""",
        ),
        quiz_lesson(
            "Quiz: 4D scheduling and 5D cost",
            (
                q(
                    "What does 4D BIM add to the 3D model?",
                    (
                        opt("Cost rates"),
                        opt(
                            "A link between model elements and schedule tasks, so the "
                            "build sequence can be visualized in time",
                            correct=True,
                        ),
                        opt("Photorealistic materials"),
                        opt("A second spatial coordinate system"),
                    ),
                    "4D = model linked to the construction schedule; 5D = model linked to cost.",
                ),
                q(
                    "Why do 5D cost estimates stay consistent as the design changes?",
                    (
                        opt("They are locked and never change"),
                        opt(
                            "Cost is attached to classified model quantities, so when "
                            "quantities change the estimate updates with them",
                            correct=True,
                        ),
                        opt("An estimator re-types every price nightly"),
                        opt("They ignore the model entirely"),
                    ),
                    "Because the link is by object quantity, changing geometry moves the "
                    "cost line automatically.",
                ),
                q(
                    "Playing a 4D sequence reveals two trades needing the same zone in "
                    "the same week. What kind of clash is that?",
                    (
                        opt("A hard clash"),
                        opt("A soft clash / clearance clash"),
                        opt("A workflow / 4D clash - a conflict in time and space", correct=True),
                        opt("A rendering error"),
                    ),
                    "Time-space conflicts are workflow (4D) clashes, distinct from "
                    "geometric hard/soft clashes.",
                ),
            ),
        ),
        # -- 8. CIM & digital handover ---------------------------------
        _t(
            "BIM for infrastructure (CIM) and digital handover",
            "10 min",
            """# BIM for infrastructure (CIM) and digital handover

Civil infrastructure is mostly **linear** - roads, rail, tunnels, pipelines
- and modeled along an **alignment** (a horizontal and vertical route with
chainage/stationing) rather than around floors. This infrastructure-focused
practice is often called **CIM (Civil Information Modeling)**. It ties the
model to **terrain and geospatial context** (surveys, GIS, a coordinate
reference system), so a bridge sits correctly on real ground.

Key CIM ideas:

- **Alignment and corridor** - the road/rail is a template swept along the
  alignment; earthworks and pavement layers are generated from it.
- **Georeferencing** - the model is placed in a real coordinate system
  (for example UTM/SIRGAS 2000), essential when it meets survey and GIS.
- **IFC 4.3** - the IFC schema was extended for infrastructure with entities
  like **IfcAlignment**, **IfcRoad**, **IfcBridge**, **IfcRail** - so
  openBIM now covers civil assets, not just buildings.

Modern civil delivery increasingly feeds a **digital twin**: the as-built
model connected to live IoT sensor data (strain, settlement, traffic) for
operation - the 6D end of the lifecycle.

The final deliverable is a **digital handover**: not a stack of paper, but
the **as-built model plus structured asset data** for the operator. A
common format is **COBie**, which delivers asset information (equipment,
spaces, warranties, maintenance) as a structured dataset:

```text
COBie handover extract - drainage asset
  Component   : Pump-Station-PS1
  Space       : Chamber-CH-04
  Type        : Submersible pump 15 kW
  Serial      : SN-88213
  WarrantyEnd : 2031-05-08
  Maintenance : Inspect impeller every 6 months
```

```mermaid
graph LR
    ALIGN["Alignment and terrain"] --> CORR["Corridor model CIM"]
    CORR --> IFC43["IFC 4.3 infrastructure"]
    IFC43 --> ASBUILT["As built model"]
    ASBUILT --> COBIE["COBie asset data"]
    ASBUILT --> TWIN["Digital twin with IoT"]
    COBIE --> OPS["Operate and maintain"]
    TWIN --> OPS
```

Remember: infrastructure BIM models along an alignment on real terrain,
IFC 4.3 makes it openBIM, and the project ends not with drawings but with a
digital handover - an as-built model and structured asset data that feed
operation and a digital twin.
""",
        ),
        quiz_lesson(
            "Quiz: BIM for infrastructure (CIM) and digital handover",
            (
                q(
                    "How are linear infrastructure assets (roads, rail) modeled in CIM?",
                    (
                        opt("Around building floors and storeys"),
                        opt(
                            "Along an alignment (a route with chainage) on real terrain, "
                            "with a corridor swept along it",
                            correct=True,
                        ),
                        opt("Only as 2D plans"),
                        opt("As a single point with no geometry"),
                    ),
                    "Infrastructure is linear: modeled along a georeferenced alignment, "
                    "not around floors.",
                ),
                q(
                    "What did IFC 4.3 add?",
                    (
                        opt("Nothing new"),
                        opt("Only better rendering"),
                        opt(
                            "Infrastructure entities such as IfcAlignment, IfcRoad, "
                            "IfcBridge and IfcRail, extending openBIM to civil assets",
                            correct=True,
                        ),
                        opt("A proprietary lock-in format"),
                    ),
                    "IFC 4.3 brought infrastructure into the open schema, so CIM assets "
                    "exchange as openBIM.",
                ),
                q(
                    "What is a 'digital handover' at the end of a BIM project?",
                    (
                        opt("A box of printed drawings"),
                        opt(
                            "The as-built model plus structured asset data (e.g. COBie) "
                            "for the operator, feeding operation and a digital twin",
                            correct=True,
                        ),
                        opt("Deleting the model to save space"),
                        opt("A single photograph of the finished asset"),
                    ),
                    "Handover delivers the as-built model and structured asset "
                    "information - the operational, 6D deliverable.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is BIM?",
                    (
                        opt("A 3D rendering plugin"),
                        opt(
                            "A way of delivering a project as a coordinated, data-rich "
                            "digital model that carries information across the whole "
                            "lifecycle",
                            correct=True,
                        ),
                        opt("A file format for photographs"),
                        opt("A brand of surveying equipment"),
                    ),
                    "BIM is model-first delivery: geometry plus information from design "
                    "to operation.",
                ),
                q(
                    "What characterizes BIM maturity Level 2?",
                    (
                        opt("Unmanaged paper 2D CAD"),
                        opt(
                            "Separate discipline 3D models exchanged in a common format "
                            "and federated for coordination",
                            correct=True,
                        ),
                        opt("A single shared cloud model edited by all in real time"),
                        opt("No modeling at all"),
                    ),
                    "Level 2 = federated discipline models (the tender baseline); "
                    "Level 3 = one shared open model.",
                ),
                q(
                    "What does Level of Development (LOD) 300 mean for an element?",
                    (
                        opt("A conceptual symbol with no dimensions"),
                        opt(
                            "Precise geometry with specific dimensions, orientation and location",
                            correct=True,
                        ),
                        opt("Fabrication-ready shop detail"),
                        opt("A verified as-built record"),
                    ),
                    "LOD 300 is precise design geometry; 400 is fabrication, 500 is as-built.",
                ),
                q(
                    "Why is quantity takeoff generated from the model reliable?",
                    (
                        opt("It ignores the geometry"),
                        opt(
                            "Quantities are computed from classified objects rather than "
                            "counted by hand, and update as the design changes",
                            correct=True,
                        ),
                        opt("It is typed manually each night"),
                        opt("It uses no classification codes"),
                    ),
                    "Takeoff is a query over object data plus classification - the basis "
                    "of 5D costing.",
                ),
                q(
                    "What is IFC and who maintains it?",
                    (
                        opt("A proprietary format from one vendor"),
                        opt(
                            "An open, vendor-neutral exchange schema from buildingSMART "
                            "(ISO 16739)",
                            correct=True,
                        ),
                        opt("A rendering engine from a game studio"),
                        opt("A national building code"),
                    ),
                    "IFC is the open buildingSMART schema at the core of openBIM.",
                ),
                q(
                    "Which openBIM format carries coordination issues between tools?",
                    (
                        opt("COBie"),
                        opt("BCF - the BIM Collaboration Format", correct=True),
                        opt("DWG"),
                        opt("JPEG"),
                    ),
                    "BCF moves a viewpoint plus comments (clashes, queries) separately "
                    "from the heavy model.",
                ),
                q(
                    "What are the four information states of an ISO 19650 CDE?",
                    (
                        opt("Draft, final, deleted, printed"),
                        opt(
                            "Work in Progress, Shared, Published, Archived",
                            correct=True,
                        ),
                        opt("Plan, build, operate, demolish"),
                        opt("Alpha, beta, release, hotfix"),
                    ),
                    "WIP -> Shared -> Published -> Archived, with check/approve gates "
                    "between them.",
                ),
                q(
                    "A drainage pipe passes through a structural pile cap. What is this?",
                    (
                        opt("A soft clash"),
                        opt("A hard clash - two elements in the same physical space", correct=True),
                        opt("A workflow clash"),
                        opt("A georeferencing error"),
                    ),
                    "Hard clash = geometric overlap; soft = clearance; workflow/4D = "
                    "time-space conflict.",
                ),
                q(
                    "How do 4D and 5D BIM keep time and cost consistent with the design?",
                    (
                        opt("They are frozen at the start and never updated"),
                        opt(
                            "They link schedule tasks and cost to model objects, so both "
                            "update when the objects change",
                            correct=True,
                        ),
                        opt("They are maintained on paper by hand"),
                        opt("They ignore the model"),
                    ),
                    "Linking by object means changing geometry moves the schedule link "
                    "and the cost line automatically.",
                ),
                q(
                    "What does a BIM digital handover deliver to the operator?",
                    (
                        opt("Only a set of printed drawings"),
                        opt(
                            "The as-built model plus structured asset data (e.g. COBie), "
                            "which can feed a digital twin",
                            correct=True,
                        ),
                        opt("Nothing - the model is deleted"),
                        opt("A single rendered image"),
                    ),
                    "Handover is the operational deliverable: as-built model and asset "
                    "information for operation and maintenance.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

BIM_FOR_CIVIL_COURSES: tuple[SeedCourse, ...] = (_BIM_FOR_CIVIL,)
