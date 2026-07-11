"""Academy seed content - Introduction to Civil Engineering.

An orientation to the profession before the technical deep dives: what
civil engineers actually do, the full lifecycle of a built asset, the
main areas of practice, how the profession is regulated and held
accountable (the Confea/Crea system and the ART), how to read the
drawings and documents that carry a design, and how ethics, safety,
sustainability and digital tools (BIM, data, AI, digital twins) are
reshaping the field. Every lesson is a direct explanation with a concrete
example and a mermaid diagram, followed by a checkpoint quiz; the course
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


_INTRO_CIVIL_ENGINEERING = SeedCourse(
    slug="intro-civil-engineering",
    title="Introduction to Civil Engineering",
    description=(
        "An orientation to the profession: what civil engineers do, the "
        "lifecycle of a built asset from conception to demolition, the main "
        "areas of practice, professional regulation and ethics (the "
        "Confea/Crea system and the ART), how to read engineering drawings, "
        "and how BIM, data and AI are reshaping the field - with a worked "
        "example and a diagram in every lesson."
    ),
    level="Beginner",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Introduction to Civil Engineering

Civil engineering is the profession that plans, designs, builds and
maintains the physical world people rely on every day: buildings,
bridges, roads, dams, water and sewage systems, ports and railways. It is
one of the oldest engineering disciplines and, increasingly, one of the
most digital. This course is the **orientation**: the whole map of the
profession before you go deep on any single subject.

The approach is **small and concrete**: every lesson explains one idea
directly, shows it in a short real example (a design formula, a document,
a spec table), and draws the idea as a diagram. After each lesson there
is a short quiz; at the end, a final quiz covers the whole course.

What you will build understanding for, in order:

1. **History and scope** - what the profession is and what it covers
2. **The lifecycle of a built asset** - conception through demolition
3. **Areas of practice** - structures, geotechnics, hydraulics, transport, management
4. **Codes, standards and regulation** - the Confea/Crea system and the ART
5. **Reading drawings and projects** - the language of a design
6. **Ethics, responsibility and safety** - the duty an engineer carries
7. **Sustainability and resilience** - building for the long term
8. **Digital transformation** - BIM, data, AI and digital twins

This is the map. Later courses in the track (soil mechanics, structural
analysis, hydraulics, construction management) are the deep dives;
knowing where each fits makes them far easier to learn.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What does civil engineering fundamentally concern itself with?",
                    (
                        opt("Only the design of tall office buildings"),
                        opt("Writing software for construction companies"),
                        opt(
                            "Planning, designing, building and maintaining the physical "
                            "infrastructure society relies on - buildings, bridges, roads, "
                            "water systems and more",
                            correct=True,
                        ),
                        opt("Selling construction materials"),
                    ),
                    "Civil engineering spans the whole built environment, from "
                    "conception through maintenance, not a single building type.",
                ),
                q(
                    "How is this course meant to relate to the deeper technical courses "
                    "in the track?",
                    (
                        opt("It replaces them"),
                        opt(
                            "It is the big-picture orientation that shows where each "
                            "subject fits, before the topic-specific deep dives",
                            correct=True,
                        ),
                        opt("It only covers construction site safety"),
                        opt("It is unrelated to the other civil courses"),
                    ),
                    "Learn the map first (this course), then the specialised courses "
                    "make sense in context.",
                ),
            ),
        ),
        # -- 1. History and scope --------------------------------------
        _t(
            "History and scope of civil engineering",
            "9 min",
            """# History and scope of civil engineering

The word **civil** originally meant "not military": it named the
engineers who built for public and civilian life - aqueducts, roads,
harbours - as opposed to fortifications and war machines. That split, in
18th-century Europe, is where the modern profession got its name.

The practice is far older than the name. Roman **aqueducts** and roads,
Egyptian and Mesopotamian irrigation, medieval **cathedrals** and their
arches and flying buttresses - all are civil engineering solving the same
enduring problem: **carry loads safely, move water and people, and make
it last**. The 19th and 20th centuries added steel, reinforced concrete
and soil mechanics, turning craft rules of thumb into a quantitative
science.

Today the **scope** is broad. A useful way to see it is by the systems a
society needs:

- **Buildings** - housing, schools, hospitals, industry.
- **Transport** - roads, railways, bridges, airports, ports.
- **Water** - supply, drainage, sewage, dams, irrigation.
- **Energy and industry** - foundations for plants, offshore structures.
- **Environment** - flood defence, waste, land reclamation.

What unites them is a **method**: understand the demand (the loads and
flows), choose materials and a form, check it against the physics and the
codes, build it, and keep it serving. A quick sense of scale, comparing
the material strengths a civil engineer works with every day:

```text
Typical characteristic strengths (order of magnitude)
--------------------------------------------------------------
Material              Compression        Tension
--------------------------------------------------------------
Structural concrete   20 to 50 MPa       weak - reinforce it
Reinforcing steel     ~500 MPa           ~500 MPa (yield)
Structural timber      20 to 40 MPa      ~20 MPa
Soil (bearing)        0.1 to 0.6 MPa     essentially none
--------------------------------------------------------------
Lesson: concrete carries compression, steel carries tension,
and together (reinforced concrete) they do both.
```

```mermaid
graph TD
    NEED["Society needs infrastructure"] --> BUILD["Buildings"]
    NEED --> TRANS["Transport networks"]
    NEED --> WATER["Water and sanitation"]
    NEED --> ENERGY["Energy and industry"]
    NEED --> ENV["Environment and defence"]
    BUILD --> METHOD["Same method design to maintenance"]
    TRANS --> METHOD
    WATER --> METHOD
    ENERGY --> METHOD
    ENV --> METHOD
```

Remember: civil engineering is an ancient craft turned quantitative
science, and its scope is nothing less than the physical systems a
society runs on.
""",
        ),
        quiz_lesson(
            "Quiz: History and scope of civil engineering",
            (
                q(
                    "Why is the discipline called 'civil' engineering?",
                    (
                        opt("Because it is polite work"),
                        opt(
                            "To distinguish civilian and public works (roads, aqueducts, "
                            "harbours) from military engineering",
                            correct=True,
                        ),
                        opt("Because it was invented by a person named Civil"),
                        opt("Because it only applies to city halls"),
                    ),
                    "'Civil' originally meant non-military - engineering for public and "
                    "civilian life.",
                ),
                q(
                    "In reinforced concrete, why are steel and concrete combined?",
                    (
                        opt("Steel is cheaper than concrete"),
                        opt("To make the structure heavier"),
                        opt(
                            "Concrete is strong in compression but weak in tension, so "
                            "steel is added to carry the tension",
                            correct=True,
                        ),
                        opt("Concrete cannot resist any load on its own"),
                    ),
                    "Concrete handles compression, steel handles tension; together they "
                    "cover both - the core idea of reinforced concrete.",
                ),
                q(
                    "Which best describes the modern scope of civil engineering?",
                    (
                        opt("Only the design of skyscrapers"),
                        opt(
                            "The physical systems a society relies on - buildings, "
                            "transport, water, energy and environmental works",
                            correct=True,
                        ),
                        opt("Only road paving"),
                        opt("Purely theoretical study with no construction"),
                    ),
                    "The scope is the whole built environment, unified by a common "
                    "method rather than a single structure type.",
                ),
            ),
        ),
        # -- 2. Lifecycle of a built asset -----------------------------
        _t(
            "The lifecycle of a built asset",
            "10 min",
            """# The lifecycle of a built asset

No structure is a one-off event; it is an **asset with a life**, and
civil engineers are involved at every stage. Understanding the whole
lifecycle explains why early decisions matter so much: choices made in
the first weeks lock in most of the cost and impact of the decades that
follow.

The stages, in order:

1. **Conception (planning)** - Is it needed? Where? What does it have to
   do? This is feasibility, site selection, budget and the terms of
   reference. Cheap to change, enormous in consequence.
2. **Design (project)** - Engineers turn the brief into drawings,
   calculations and specifications: geometry, loads, materials,
   foundations. Design is itself phased - preliminary, then detailed
   ("executive") design ready to build from.
3. **Construction (execution)** - The design is built: earthworks,
   foundations, structure, systems, finishes - managed for cost, schedule
   and quality on a live site.
4. **Operation (use)** - The asset serves its purpose: a bridge carries
   traffic, a plant treats water. Most of the value - and most of the
   time - lives here.
5. **Maintenance** - Inspection and upkeep keep it safe and functional:
   preventive (planned) beats corrective (after failure). This runs
   throughout operation.
6. **Demolition or decommissioning** - At end of life, the asset is
   safely removed or repurposed, ideally recovering and recycling
   materials.

A key principle: **the cost of change rises steeply through the life**.
Fixing a problem on the drawing board is trivial; fixing it after
construction can cost orders of magnitude more.

```text
Relative cost to correct a defect, by stage (illustrative)
----------------------------------------------------------
Conception   1x       cheapest - just change the brief
Design       ~5x      redraw and recalculate
Construction ~20x     rework built elements
Operation    ~100x+   repair, downtime, possible litigation
----------------------------------------------------------
This is why review effort concentrates early.
```

```mermaid
graph LR
    CONC["Conception and feasibility"] --> DES["Design and calculation"]
    DES --> CONS["Construction and execution"]
    CONS --> OPER["Operation and use"]
    OPER --> MAINT["Maintenance and inspection"]
    MAINT --> OPER
    OPER --> END["Demolition or decommission"]
```

Remember: a built asset lives for decades; the engineer's leverage is
greatest at the start, when a stroke of a pen still costs almost nothing.
""",
        ),
        quiz_lesson(
            "Quiz: The lifecycle of a built asset",
            (
                q(
                    "What is the correct order of the built-asset lifecycle?",
                    (
                        opt("Construction, design, conception, operation"),
                        opt(
                            "Conception, design, construction, operation, maintenance, demolition",
                            correct=True,
                        ),
                        opt("Design, demolition, construction, operation"),
                        opt("Operation, conception, maintenance, design"),
                    ),
                    "It starts with the idea (conception) and ends with removal "
                    "(demolition), with operation and maintenance running longest.",
                ),
                q(
                    "Why do early-stage decisions matter so much?",
                    (
                        opt("Because early work is the most fun"),
                        opt(
                            "The cost of correcting a problem rises steeply through the "
                            "life, so a change on the drawing board is far cheaper than "
                            "one after construction",
                            correct=True,
                        ),
                        opt("Because later stages have no engineers"),
                        opt("Because codes only apply to conception"),
                    ),
                    "Conception and design lock in most cost and impact; fixing defects "
                    "later can cost orders of magnitude more.",
                ),
                q(
                    "How does preventive maintenance differ from corrective maintenance?",
                    (
                        opt("They are the same thing"),
                        opt("Preventive happens only after a failure"),
                        opt(
                            "Preventive is planned upkeep that avoids failures; corrective "
                            "reacts after something has already failed",
                            correct=True,
                        ),
                        opt("Corrective maintenance is always cheaper"),
                    ),
                    "Planned, preventive maintenance is generally safer and cheaper than "
                    "waiting for failure and reacting.",
                ),
            ),
        ),
        # -- 3. Areas of practice --------------------------------------
        _t(
            "Areas of practice in civil engineering",
            "10 min",
            """# Areas of practice in civil engineering

Civil engineering is too broad for one person to master entirely, so it
divides into **areas of practice** that specialise while sharing the same
foundations of mechanics, materials and mathematics. The main ones:

- **Structures** - the skeleton that carries loads: beams, columns,
  slabs, frames, bridges. The structural engineer proves the structure
  will not collapse (strength, the **ultimate limit state**) and will not
  deform or crack unacceptably in use (the **serviceability limit state**).
- **Geotechnics** - soil and rock: foundations, retaining walls,
  embankments, slope stability, tunnels. Everything rests on the ground,
  and the ground is the most variable material an engineer meets.
- **Hydraulics and sanitation** - water in motion and at rest: supply
  networks, drainage, sewage collection and treatment, dams, flood
  control. It protects public health and manages the water cycle.
- **Transportation** - moving people and goods: road and railway
  geometry, pavements, traffic, airports, ports and the logistics of
  networks.
- **Construction management** - turning a design into a finished work on
  budget and on time: planning, scheduling, cost control, procurement,
  quality and safety on site.

These areas interlock. A single **bridge** needs structures (the deck and
piers), geotechnics (the foundations), hydraulics (the river it crosses),
transportation (the road it carries) and construction management (to
build it) - all cooperating.

A worked micro-example from structures - the bending strength that sizes
a beam:

```text
Section modulus and bending stress
----------------------------------
Bending stress:   sigma = M / W
Section modulus (rectangle):  W = b * h^2 / 6

Example: a beam with b = 0.20 m, h = 0.50 m, moment M = 60 kN*m
  W = 0.20 * 0.50^2 / 6 = 0.00833 m^3
  sigma = 60 / 0.00833 = 7200 kPa = 7.2 MPa
Compare 7.2 MPa against the material's allowable stress to check it.
----------------------------------
```

```mermaid
graph TD
    CE["Civil engineering"] --> STR["Structures"]
    CE --> GEO["Geotechnics"]
    CE --> HYD["Hydraulics and sanitation"]
    CE --> TRA["Transportation"]
    CE --> MAN["Construction management"]
    STR --> BRIDGE["A bridge needs all of them"]
    GEO --> BRIDGE
    HYD --> BRIDGE
    TRA --> BRIDGE
    MAN --> BRIDGE
```

Remember: the areas specialise but never work alone - real projects
demand several of them at once, coordinated into one solution.
""",
        ),
        quiz_lesson(
            "Quiz: Areas of practice in civil engineering",
            (
                q(
                    "Which area is primarily responsible for foundations, retaining "
                    "walls and slope stability?",
                    (
                        opt("Hydraulics and sanitation"),
                        opt("Transportation"),
                        opt("Geotechnics", correct=True),
                        opt("Construction management"),
                    ),
                    "Geotechnics deals with soil and rock - the ground everything else rests on.",
                ),
                q(
                    "What is the difference between the ultimate and serviceability "
                    "limit states in structural design?",
                    (
                        opt("They are the same check"),
                        opt(
                            "The ultimate limit state guards against collapse (strength); "
                            "serviceability guards against excessive deflection or "
                            "cracking in normal use",
                            correct=True,
                        ),
                        opt("Serviceability is about collapse, ultimate about comfort"),
                        opt("Both only apply to bridges"),
                    ),
                    "ULS = will it stand up; SLS = is it usable and durable in service. "
                    "A design must satisfy both.",
                ),
                q(
                    "Why is a single bridge a good example of the areas working together?",
                    (
                        opt("Because bridges need only structural engineers"),
                        opt(
                            "It combines structures, geotechnics, hydraulics, "
                            "transportation and construction management in one project",
                            correct=True,
                        ),
                        opt("Because a bridge involves no soil"),
                        opt("Because bridges are never managed"),
                    ),
                    "The deck (structures), foundations (geotechnics), river "
                    "(hydraulics), road (transport) and build (management) all meet.",
                ),
            ),
        ),
        # -- 4. Codes, standards and regulation ------------------------
        _t(
            "Codes, standards and professional regulation",
            "10 min",
            """# Codes, standards and professional regulation

Engineering is trusted with public safety, so it is **regulated**. Two
layers matter: the **technical** rules a design must obey, and the
**professional** rules about who may sign for it.

**Technical codes and standards** set the minimum requirements a design
must meet. In Brazil these are the **ABNT NBR** standards - for example
NBR 6118 (concrete structures), NBR 6122 (foundations), NBR 8681
(actions and safety of structures). Internationally you will meet the
**Eurocodes**, the American **ACI** and **AISC** codes, and **AASHTO**
for highways and bridges. They encode hard-won experience so every
engineer starts from a safe, agreed baseline instead of reinventing it.

**Professional regulation** governs the person. In Brazil the system is:

- **Confea** - the Federal Council of Engineering and Agronomy, which
  sets national rules for the profession.
- **Crea** - the Regional Council in each state, where an engineer
  **registers** and is licensed to practise.
- **ART (Anotacao de Responsabilidade Tecnica)** - the "Technical
  Responsibility Note". For essentially every technical service, the
  responsible engineer files an ART that legally records **who is
  responsible** for that specific work. It ties a named, licensed person
  to the design or execution and is the backbone of accountability.

So a legal, safe project has two things: it **complies with the codes**,
and a **registered engineer takes formal responsibility** for it via an
ART.

```text
Anatomy of an ART (what it records)
-----------------------------------
- The responsible professional (name and Crea registration)
- The contracting client
- The specific service (e.g. "structural design" or "site management")
- The work location and contract value
- The relevant technical activity codes
=> Legally binds a named, licensed engineer to that work.
-----------------------------------
```

```mermaid
graph TD
    CONFEA["Confea federal council sets rules"] --> CREA["Crea regional council registers"]
    CREA --> ENG["Licensed engineer"]
    ENG --> ART["Files an ART per service"]
    ART --> RESP["Legal technical responsibility recorded"]
    CODES["ABNT NBR and international codes"] --> DESIGN["Compliant design"]
    ENG --> DESIGN
    DESIGN --> RESP
```

Remember: codes make the design safe by rule, and the ART filed through
the Confea/Crea system makes a named engineer answerable for it.
""",
        ),
        quiz_lesson(
            "Quiz: Codes, standards and professional regulation",
            (
                q(
                    "What does the ART (Anotacao de Responsabilidade Tecnica) do?",
                    (
                        opt("It is a tax on construction materials"),
                        opt(
                            "It legally records which registered engineer is responsible "
                            "for a specific technical service",
                            correct=True,
                        ),
                        opt("It is a type of concrete test"),
                        opt("It certifies that a design is patented"),
                    ),
                    "The ART ties a named, licensed professional to a specific work - "
                    "the backbone of accountability.",
                ),
                q(
                    "In the Brazilian system, what is the relationship between Confea and Crea?",
                    (
                        opt("They are competing private companies"),
                        opt(
                            "Confea is the federal council setting national rules; Crea is "
                            "the regional council where engineers register and are "
                            "licensed",
                            correct=True,
                        ),
                        opt("Crea sets the rules and Confea only issues fines"),
                        opt("They regulate only architects, not engineers"),
                    ),
                    "Confea = federal (rules), Crea = regional (registration and "
                    "licensing of the professional).",
                ),
                q(
                    "What is the role of a technical code such as ABNT NBR 6118?",
                    (
                        opt("It lists the prices of building materials"),
                        opt(
                            "It sets the minimum technical requirements a design must meet "
                            "- here, for concrete structures",
                            correct=True,
                        ),
                        opt("It registers the engineer with the council"),
                        opt("It is optional guidance with no bearing on safety"),
                    ),
                    "Codes encode agreed, safe minimums so every design starts from a "
                    "trusted baseline. NBR 6118 covers concrete structures.",
                ),
            ),
        ),
        # -- 5. Reading drawings and projects --------------------------
        _t(
            "Reading and interpreting engineering drawings",
            "10 min",
            """# Reading and interpreting engineering drawings

A design has to be **communicated** to the people who build it, and the
universal language for that is the **technical drawing** plus its
supporting documents. Learning to read them is a core literacy of the
profession.

A construction project is not one drawing but a coordinated **set**, each
discipline contributing its own:

- **Architectural** - spaces, layout, finishes, the overall form.
- **Structural** - foundations, beams, columns, slabs, reinforcement.
- **Installations** - electrical, hydraulic (water and sewage), HVAC.
- **Site and topographic** - the terrain, levels and location.

Drawings use standard **views** to describe three-dimensional reality on
paper:

- **Plan** - a horizontal cut seen from above (the layout of a floor).
- **Elevation** - a straight-on view of a face (a facade).
- **Section (cut)** - a vertical slice revealing what is inside.
- **Detail** - a zoomed-in view of a connection or component.

Two conventions make drawings readable everywhere:

- **Scale** - the ratio of drawing to reality. A **1:100** plan means
  1 cm on paper is 100 cm (1 m) in the world; a 1:50 detail is twice as
  large. Always read the scale before measuring anything.
- **Title block and legend** - every sheet carries a title block (project,
  discipline, author, date, revision) and a legend explaining its
  symbols, line types and hatching.

A quick scale worked example:

```text
Reading a scale
---------------
Real length = drawing length * scale factor

On a 1:100 plan, a wall drawn 4.5 cm long:
  real = 4.5 cm * 100 = 450 cm = 4.50 m

On a 1:25 detail, a bar drawn 3.2 cm:
  real = 3.2 cm * 25 = 80 cm = 0.80 m
---------------
Always confirm the sheet's scale before scaling any dimension.
```

```mermaid
graph TD
    SET["Project drawing set"] --> ARCH["Architectural"]
    SET --> STRU["Structural"]
    SET --> INST["Installations"]
    SET --> TOPO["Site and topographic"]
    ARCH --> VIEWS["Views plan elevation section detail"]
    STRU --> VIEWS
    VIEWS --> READ["Read with scale title block and legend"]
    READ --> BUILD["Builders execute the design"]
```

Remember: a drawing set is a coordinated language - know the views, always
check the scale, and read the title block and legend before you trust a
dimension.
""",
        ),
        quiz_lesson(
            "Quiz: Reading and interpreting engineering drawings",
            (
                q(
                    "On a drawing at scale 1:100, how long in reality is a wall drawn 6 cm long?",
                    (
                        opt("6 cm"),
                        opt("60 cm"),
                        opt("6 m", correct=True),
                        opt("600 m"),
                    ),
                    "6 cm * 100 = 600 cm = 6 m. Real length equals drawing length times "
                    "the scale factor.",
                ),
                q(
                    "What does a 'section' (cut) view show that a plan does not?",
                    (
                        opt("Only the exterior colour"),
                        opt(
                            "A vertical slice through the building, revealing what is "
                            "inside and the heights of elements",
                            correct=True,
                        ),
                        opt("The project's budget"),
                        opt("The name of the client"),
                    ),
                    "A section is a vertical cut; a plan is a horizontal cut seen from "
                    "above. Together they describe the 3D reality.",
                ),
                q(
                    "Why should you read the title block and legend before measuring on a sheet?",
                    (
                        opt("They are decorative only"),
                        opt(
                            "They give the scale, revision, discipline and the meaning of "
                            "symbols and line types - without them a dimension can be "
                            "misread",
                            correct=True,
                        ),
                        opt("Because measuring is never allowed"),
                        opt("Because they replace the drawing"),
                    ),
                    "Scale and legend are what make the marks on paper mean real, "
                    "unambiguous quantities.",
                ),
            ),
        ),
        # -- 6. Ethics, responsibility and safety ----------------------
        _t(
            "Professional ethics, responsibility and safety",
            "10 min",
            """# Professional ethics, responsibility and safety

Because civil works can injure or kill people when they fail, the
profession carries a **duty of care** that goes beyond any contract. The
engineer's first obligation is to the **safety, health and welfare of the
public** - above the client's convenience and above the engineer's own
interest. This principle sits at the top of every engineering code of
ethics.

What that means in practice:

- **Competence** - work only within your area of qualification; call in
  a specialist when a problem is outside it.
- **Honesty and integrity** - report findings truthfully; do not sign off
  on work you have not verified or do not believe is safe.
- **Responsibility** - own your decisions. In the Brazilian system the
  **ART** makes this legally concrete: your name is on the work.
- **Confidentiality and fair dealing** - protect client information;
  avoid conflicts of interest.

**Safety** is where ethics meets the daily reality of a construction
site - one of the more hazardous workplaces there is. Two ideas organise
it:

- **The hierarchy of controls** - the ranked ways to reduce a hazard,
  strongest first: **eliminate** the hazard, then **substitute** it, then
  **engineer** controls (guardrails, shoring), then **administrative**
  measures (procedures, training), and only last **PPE** (helmet, harness,
  boots). PPE is the last line, not the first.
- **Collective before individual protection** - in Brazil, the norms (for
  example the regulatory norm NR-18 for construction) prioritise
  collective protection (EPC) such as guardrails and nets over relying on
  each worker's PPE (EPI) alone.

```text
Hierarchy of controls (most to least effective)
-----------------------------------------------
1. Eliminate     remove the hazard entirely
2. Substitute    replace it with something safer
3. Engineering   guardrails, shoring, ventilation
4. Administrative procedures, signage, training, rotation
5. PPE           helmet, harness, gloves - last resort
-----------------------------------------------
Design out the danger first; PPE protects only one person.
```

```mermaid
graph TD
    DUTY["Duty of care to the public"] --> COMP["Competence"]
    DUTY --> HON["Honesty and integrity"]
    DUTY --> RESP["Responsibility named on the work"]
    DUTY --> SAFE["Safety on site"]
    SAFE --> ELIM["Eliminate or substitute hazard"]
    SAFE --> ENGC["Engineering and collective controls"]
    SAFE --> PPE["PPE as the last line"]
```

Remember: the engineer answers to the public first; safety is engineered
in by controlling hazards at the source, with PPE only ever the last line
of defence.
""",
        ),
        quiz_lesson(
            "Quiz: Professional ethics, responsibility and safety",
            (
                q(
                    "According to engineering codes of ethics, what is the engineer's "
                    "paramount obligation?",
                    (
                        opt("Maximising the client's profit"),
                        opt("Finishing as fast as possible"),
                        opt(
                            "The safety, health and welfare of the public, above client "
                            "convenience or personal interest",
                            correct=True,
                        ),
                        opt("Using the newest technology available"),
                    ),
                    "Public safety comes first - this is the top principle in essentially "
                    "every engineering code of ethics.",
                ),
                q(
                    "In the hierarchy of controls, where does personal protective "
                    "equipment (PPE) rank?",
                    (
                        opt("First - always the primary defence"),
                        opt(
                            "Last - used only after eliminating, substituting and "
                            "engineering out the hazard",
                            correct=True,
                        ),
                        opt("It is not part of the hierarchy"),
                        opt("Above engineering controls"),
                    ),
                    "PPE protects only the individual and is the last line; you design "
                    "out the hazard first.",
                ),
                q(
                    "What does it mean to work 'within your competence'?",
                    (
                        opt("Never asking anyone for help"),
                        opt("Only doing the easiest tasks"),
                        opt(
                            "Taking on work only in your area of qualification and "
                            "bringing in a specialist when a problem falls outside it",
                            correct=True,
                        ),
                        opt("Signing any document a client requests"),
                    ),
                    "Competence means honest limits: qualified work, and a specialist "
                    "when the problem exceeds your expertise.",
                ),
            ),
        ),
        # -- 7. Sustainability and resilience --------------------------
        _t(
            "Sustainability and resilience in civil works",
            "10 min",
            """# Sustainability and resilience in civil works

The built environment consumes a large share of the world's energy,
materials and water, and produces a large share of its waste and carbon.
So modern civil engineering is judged not only by "does it stand up and
work?" but by "**at what cost to the future?**" Two related ideas capture
this.

**Sustainability** - meeting present needs without compromising the
ability of future generations to meet theirs. In practice it is balanced
across three pillars: **environmental, social and economic**. For a civil
work this shows up as:

- **Whole-life thinking** - judge a design by its **lifecycle** cost and
  impact, not just the build. Cement and steel carry large **embodied
  carbon**; operation carries **operational** energy. A cheaper building
  that wastes energy for fifty years is not cheap.
- **Efficient materials and reuse** - use less, use lower-carbon
  alternatives, design for disassembly and recycling.
- **Water and land** - manage stormwater, protect soil, reduce the
  footprint.

**Resilience** - the ability of an asset or system to **withstand,
absorb and recover** from shocks: floods, earthquakes, extreme heat,
material ageing. A resilient design does not just resist the expected
load; it degrades gracefully and recovers quickly from the unexpected.
Climate change makes this urgent, because the "expected" loads
(rainfall, temperature, sea level) are shifting.

A simple lifecycle-comparison example:

```text
Whole-life view of two facade options (illustrative)
----------------------------------------------------
                     Option A        Option B
Build cost           lower           higher
Embodied carbon      high            lower
Operational energy   high (poor      low (well
                     insulation)     insulated)
50-year total cost   HIGHER          LOWER
----------------------------------------------------
The cheaper build can be the more expensive asset.
Decide on whole-life cost, not first cost.
```

```mermaid
graph TD
    SUS["Sustainability three pillars"] --> ENV["Environmental"]
    SUS --> SOC["Social"]
    SUS --> ECON["Economic"]
    ENV --> WLC["Whole life carbon and cost"]
    RES["Resilience"] --> WITH["Withstand shocks"]
    RES --> ABS["Absorb and adapt"]
    RES --> REC["Recover quickly"]
    WLC --> DESIGN["Design decision"]
    REC --> DESIGN
```

Remember: sustainability asks what a work costs the future across its
whole life, and resilience asks how well it survives and recovers from
shocks - both now shape the design, not just strength and cost.
""",
        ),
        quiz_lesson(
            "Quiz: Sustainability and resilience in civil works",
            (
                q(
                    "What are the three pillars usually used to balance sustainability?",
                    (
                        opt("Steel, concrete and timber"),
                        opt("Environmental, social and economic", correct=True),
                        opt("Design, construction and demolition"),
                        opt("Cost, schedule and scope"),
                    ),
                    "Sustainability balances environmental, social and economic "
                    "considerations together.",
                ),
                q(
                    "What is the difference between embodied and operational carbon?",
                    (
                        opt("They are the same"),
                        opt(
                            "Embodied carbon comes from producing the materials and "
                            "building; operational carbon comes from energy used while the "
                            "asset is in service",
                            correct=True,
                        ),
                        opt("Embodied carbon only occurs during demolition"),
                        opt("Operational carbon is emitted before construction"),
                    ),
                    "Whole-life carbon adds the up-front embodied carbon to the "
                    "operational carbon accrued over the asset's life.",
                ),
                q(
                    "What does 'resilience' mean for a civil asset?",
                    (
                        opt("That it is the cheapest option to build"),
                        opt(
                            "Its ability to withstand, absorb and recover from shocks such "
                            "as floods or earthquakes",
                            correct=True,
                        ),
                        opt("That it never needs maintenance"),
                        opt("That it uses only recycled materials"),
                    ),
                    "Resilience is graceful degradation and quick recovery from the "
                    "unexpected, increasingly important under a changing climate.",
                ),
            ),
        ),
        # -- 8. Digital transformation ---------------------------------
        _t(
            "The digital transformation of civil engineering",
            "10 min",
            """# The digital transformation of civil engineering

Civil engineering is being reshaped by digital tools as profoundly as the
arrival of reinforced concrete once reshaped it. The work is moving from
lines on paper to **data-rich models** that live across the whole
lifecycle. This is where the profession is going, and it is where the
Cyberdyne track will take you deep.

The keystone is **BIM (Building Information Modelling)**. BIM is not just
3D drawing - it is a **shared, structured model** where every element (a
beam, a pipe, a door) carries **data**: dimensions, material, cost,
supplier, maintenance schedule. Disciplines coordinate on one model, and
**clash detection** finds conflicts (a duct through a beam) in the model
instead of on site. The open exchange format is **IFC (Industry
Foundation Classes)**, so models move between tools.

Building on that foundation:

- **Data and analytics** - captured across design, construction and
  operation, feeding better estimates and decisions.
- **AI and machine learning** - **predictive** models for cost and
  schedule, **computer vision** for progress and safety monitoring from
  site photos, and **generative design** that explores thousands of
  layout or structural options against your constraints.
- **Digital twins** - a live digital replica of a physical asset, fed by
  **IoT sensors** (strain, vibration, temperature, flow). It mirrors the
  asset in real time to monitor health, predict maintenance and simulate
  "what if" before acting on the real thing.
- **Reality capture** - **drones and photogrammetry**, and laser scanning,
  turn a real site into precise 3D data; **GIS** ties infrastructure to
  geography.

The through-line: the **model becomes the single source of truth**, and
data flows from it into every stage and back.

```text
From drawing to living model
----------------------------
Old world:  2D drawings  -> build -> paper as-builts -> forget
New world:  BIM model (IFC)
              -> design coordinated, clashes caught early
              -> construction tracked (drones, computer vision)
              -> operation via a digital twin (IoT sensors)
              -> AI predicts maintenance and cost
Data flows both ways across the whole lifecycle.
----------------------------
```

```mermaid
graph TD
    BIM["BIM model shared and data rich"] --> IFC["IFC open exchange"]
    BIM --> CLASH["Clash detection in the model"]
    BIM --> DT["Digital twin of the asset"]
    SENS["IoT sensors"] --> DT
    DRONE["Drones and photogrammetry"] --> BIM
    DT --> AI["AI prediction and generative design"]
    AI --> DECIDE["Better decisions across the lifecycle"]
```

Remember: the future of civil engineering is a data-rich model at the
centre - BIM and IFC as the backbone, digital twins fed by sensors, and
AI turning that data into prediction and better design.
""",
        ),
        quiz_lesson(
            "Quiz: The digital transformation of civil engineering",
            (
                q(
                    "What makes BIM more than just 3D drawing?",
                    (
                        opt("It uses brighter colours"),
                        opt(
                            "Every element carries structured data (material, cost, "
                            "schedule) in a shared model coordinated across disciplines",
                            correct=True,
                        ),
                        opt("It only works for small houses"),
                        opt("It removes the need for any engineer"),
                    ),
                    "BIM is an information model - the 'I' is data attached to every "
                    "element, not just geometry.",
                ),
                q(
                    "What is a digital twin?",
                    (
                        opt("A backup copy of the drawings"),
                        opt("A second identical building nearby"),
                        opt(
                            "A live digital replica of a physical asset, fed by IoT "
                            "sensors, used to monitor, predict and simulate in real time",
                            correct=True,
                        ),
                        opt("A rendering used only for marketing"),
                    ),
                    "A digital twin mirrors the real asset with live sensor data, "
                    "enabling monitoring, prediction and 'what if' simulation.",
                ),
                q(
                    "What does IFC (Industry Foundation Classes) provide?",
                    (
                        opt("A brand of concrete"),
                        opt(
                            "An open exchange format so BIM models can move between "
                            "different software tools",
                            correct=True,
                        ),
                        opt("A type of drone"),
                        opt("A safety regulation"),
                    ),
                    "IFC is the open, vendor-neutral format that lets a BIM model be "
                    "shared across tools and disciplines.",
                ),
                q(
                    "Which is an example of AI applied to civil engineering?",
                    (
                        opt("Pouring concrete by hand"),
                        opt(
                            "Computer vision reading site photos to track progress and "
                            "flag safety issues",
                            correct=True,
                        ),
                        opt("Printing a paper drawing"),
                        opt("Storing files on a USB stick"),
                    ),
                    "Computer vision, predictive cost/schedule models and generative "
                    "design are all AI applications in the field.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In one sentence, what is civil engineering?",
                    (
                        opt("The design of software for builders"),
                        opt(
                            "The profession that plans, designs, builds and maintains the "
                            "physical infrastructure society relies on",
                            correct=True,
                        ),
                        opt("Only the construction of bridges"),
                        opt("A branch of the military"),
                    ),
                    "It spans the whole built environment across the full lifecycle, "
                    "unified by a common engineering method.",
                ),
                q(
                    "Why did the discipline come to be called 'civil' engineering?",
                    (
                        opt("Because it is done politely"),
                        opt(
                            "To distinguish civilian and public works from military engineering",
                            correct=True,
                        ),
                        opt("Because it only builds city halls"),
                        opt("Because it needs no mathematics"),
                    ),
                    "'Civil' originally meant non-military - engineering for public life.",
                ),
                q(
                    "At which stage of a built asset's lifecycle is the cost of changing "
                    "a decision lowest?",
                    (
                        opt("Operation"),
                        opt("Construction"),
                        opt("Conception and design", correct=True),
                        opt("Demolition"),
                    ),
                    "Early on, a change costs almost nothing; correcting the same "
                    "problem after construction can cost orders of magnitude more.",
                ),
                q(
                    "Which area of practice deals mainly with soil, foundations and "
                    "slope stability?",
                    (
                        opt("Transportation"),
                        opt("Geotechnics", correct=True),
                        opt("Hydraulics and sanitation"),
                        opt("Construction management"),
                    ),
                    "Geotechnics covers the ground - the most variable material an "
                    "engineer works with.",
                ),
                q(
                    "What is the purpose of an ART in the Brazilian Confea/Crea system?",
                    (
                        opt("To set the price of a project"),
                        opt(
                            "To legally record which registered engineer is responsible "
                            "for a specific technical service",
                            correct=True,
                        ),
                        opt("To certify a material as recyclable"),
                        opt("To replace the technical drawings"),
                    ),
                    "The ART binds a named, licensed professional to the work - the "
                    "backbone of technical accountability.",
                ),
                q(
                    "On a 1:50 drawing, a beam is drawn 8 cm long. How long is it in reality?",
                    (
                        opt("8 cm"),
                        opt("0.8 m"),
                        opt("4 m", correct=True),
                        opt("40 m"),
                    ),
                    "8 cm * 50 = 400 cm = 4 m. Real length equals drawing length times "
                    "the scale factor.",
                ),
                q(
                    "In the hierarchy of controls for site safety, what is the least "
                    "effective (last-resort) measure?",
                    (
                        opt("Eliminating the hazard"),
                        opt("Engineering controls such as guardrails"),
                        opt("Personal protective equipment (PPE)", correct=True),
                        opt("Substituting a safer method"),
                    ),
                    "PPE protects only the individual and comes last; you design out the "
                    "hazard at the source first.",
                ),
                q(
                    "Why should a design be judged on its whole-life cost rather than "
                    "its build cost alone?",
                    (
                        opt("Because build cost is impossible to estimate"),
                        opt(
                            "A cheaper build can waste energy and need repair for decades, "
                            "making it the more expensive asset over its life",
                            correct=True,
                        ),
                        opt("Because operation is always free"),
                        opt("Because codes forbid measuring build cost"),
                    ),
                    "Embodied plus operational impact over decades can dwarf the initial "
                    "build cost - decide on whole-life value.",
                ),
                q(
                    "What best describes BIM?",
                    (
                        opt("A single 2D floor plan"),
                        opt(
                            "A shared, data-rich model where every element carries "
                            "information and disciplines coordinate together",
                            correct=True,
                        ),
                        opt("A brand of surveying drone"),
                        opt("A type of reinforcing steel"),
                    ),
                    "BIM's value is the information attached to a coordinated model, with "
                    "IFC as the open exchange format.",
                ),
                q(
                    "Which pairing correctly matches a digital tool to its use in civil "
                    "engineering?",
                    (
                        opt("Digital twin - a marketing rendering only"),
                        opt(
                            "IoT sensors feeding a digital twin to monitor an asset's "
                            "health in real time",
                            correct=True,
                        ),
                        opt("Drones - used only to deliver concrete"),
                        opt("GIS - a brand of cement"),
                    ),
                    "A digital twin is fed by IoT sensors for real-time monitoring and "
                    "predictive maintenance; drones and GIS capture and locate data.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

INTRO_CIVIL_ENGINEERING_COURSES: tuple[SeedCourse, ...] = (_INTRO_CIVIL_ENGINEERING,)
