"""Academy seed content - Structural Analysis.

How structures carry load, from statically determinate beams and trusses
to the classical and matrix methods for indeterminate structures. Each
lesson gives a direct explanation grounded in real practice (ABNT NBR,
ACI, Eurocode, AASHTO), a mermaid diagram of the idea, and a worked
equilibrium or deflection calculation, followed by a checkpoint quiz; the
course closes with a comprehensive final quiz.
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


_STRUCTURAL_ANALYSIS = SeedCourse(
    slug="structural-analysis",
    title="Structural Analysis",
    description=(
        "How structures carry load - from statically determinate beams and "
        "trusses to the force, displacement and matrix stiffness methods for "
        "indeterminate structures. Every lesson pairs a direct explanation "
        "with a mermaid diagram and a worked equilibrium or deflection "
        "calculation, grounded in real codes (ABNT NBR, ACI, Eurocode, AASHTO)."
    ),
    level="Intermediate",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Structural Analysis

Before a beam is sized or a bridge is detailed, someone has to answer one
question: **how does the structure carry its load down to the ground?**
Structural analysis is the discipline that answers it - turning loads,
geometry and supports into the internal forces (axial, shear, moment) and
the deflections an engineer then checks against a code.

This course builds that skill in order: first the **statically
determinate** structures you can solve with equilibrium alone (beams,
trusses, frames, arches), then the tools - energy methods, the force
method, and the matrix stiffness method - that unlock **statically
indeterminate** structures, which is almost everything real.

The approach is **concrete**: every lesson explains one idea directly,
draws it as a diagram, and works a short calculation you can follow with a
pencil. After each lesson there is a short quiz; at the end, a final quiz
covers the whole course.

What you will build understanding for, in order:

1. **Loads, supports and free-body diagrams** - the raw inputs
2. **Determinate beams** - shear and moment diagrams
3. **Trusses** - method of joints and sections
4. **Frames and arches** - bending plus axial systems
5. **Influence lines and moving loads** - bridges and cranes
6. **Energy methods and virtual work** - computing deflections
7. **The force method** - solving indeterminate structures by redundants
8. **The matrix stiffness method** - how software actually does it

The first half you can do by hand; the second half is the theory behind
every structural analysis program (SAP2000, STAAD, robot). Knowing both
means you can trust - and check - what the software tells you.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What is the central question structural analysis answers?",
                    (
                        opt("Which architect designed the building"),
                        opt("What color to paint the steel"),
                        opt(
                            "How a structure carries its loads down to the ground - the "
                            "internal forces and deflections that result",
                            correct=True,
                        ),
                        opt("How much the project will cost"),
                    ),
                    "Analysis turns loads, geometry and supports into internal forces "
                    "(axial, shear, moment) and deflections.",
                ),
                q(
                    "How is the course ordered?",
                    (
                        opt("Alphabetically by topic"),
                        opt(
                            "Statically determinate structures first (solvable by "
                            "equilibrium), then methods for indeterminate structures",
                            correct=True,
                        ),
                        opt("Only computational methods, no hand calculation"),
                        opt("Random - the order does not matter"),
                    ),
                    "Determinate beams, trusses, frames and arches come first; then "
                    "energy, force and stiffness methods unlock indeterminate systems.",
                ),
            ),
        ),
        # -- 1. Loads, supports, FBD -----------------------------------
        _t(
            "Loads, supports and free-body diagrams",
            "10 min",
            """# Loads, supports and free-body diagrams

Every analysis starts by replacing the real world with a **model**: the
**loads** acting, the **supports** holding the structure, and the reaction
forces those supports supply. The tool that makes this rigorous is the
**free-body diagram (FBD)** - an isolated sketch of the structure with
every external force and reaction drawn on it.

**Loads** come in families the codes define. ABNT NBR 6120 gives permanent
(dead) and variable (live) loads; NBR 6123 gives wind. Common idealizations:

- **Point (concentrated) load** P - a single force, in kN.
- **Distributed load** w - force per length, in kN per m; its resultant is
  the area under the diagram, acting through its centroid.
- **Moment (couple)** M - a pure twisting action, in kN times m.

**Supports** are classified by what they restrain, which sets how many
**reaction components** they contribute:

- **Roller** - resists one force (normal to the surface). 1 reaction.
- **Pin (hinge)** - resists force in two directions, but not moment. 2.
- **Fixed** - resists two forces and a moment. 3 reactions.

```mermaid
graph TD
    STRUCT["Real structure and loads"] --> MODEL["Idealize loads and supports"]
    MODEL --> FBD["Draw free body diagram"]
    FBD --> EQ["Apply equilibrium equations"]
    EQ --> RX["Sum Fx equals zero"]
    EQ --> RY["Sum Fy equals zero"]
    EQ --> RM["Sum M equals zero"]
    RM --> REACT["Support reactions solved"]
```

A planar (2D) structure has exactly **three equilibrium equations**: the
sum of horizontal forces, the sum of vertical forces, and the sum of
moments about any point are each zero. Solve them for the reactions.

**Worked example - simply supported beam.** A 6 m beam is pinned at A (left)
and on a roller at B (right). A 12 kN point load sits 2 m from A.

```text
Given:  span L = 6 m, load P = 12 kN at x = 2 m from A
        A = pin (Ax, Ay), B = roller (By, vertical)

Sum Fx = 0:   Ax = 0

Sum M about A = 0  (counterclockwise positive):
        By * 6  -  12 * 2  =  0
        By = 24 / 6 = 4 kN  (up)

Sum Fy = 0:   Ay + By - 12 = 0
        Ay = 12 - 4 = 8 kN  (up)

Check, Sum M about B:  12*(6-2) - Ay*6 = 48 - 48 = 0  OK
```

The load closer to A throws more reaction onto A - exactly what intuition
expects. Get the FBD and reactions right and the rest of the analysis
follows; get them wrong and everything downstream is wrong.
""",
        ),
        quiz_lesson(
            "Quiz: Loads, supports and free-body diagrams",
            (
                q(
                    "How many independent equilibrium equations does a planar (2D) "
                    "structure provide?",
                    (
                        opt("One"),
                        opt("Two"),
                        opt(
                            "Three - sum of horizontal forces, sum of vertical forces, "
                            "and sum of moments each equal zero",
                            correct=True,
                        ),
                        opt("Six"),
                    ),
                    "In 2D: Sum Fx = 0, Sum Fy = 0, Sum M = 0.",
                ),
                q(
                    "How many reaction components does a fixed support provide in 2D?",
                    (
                        opt("One (a single vertical force)"),
                        opt("Two (two forces, no moment)"),
                        opt(
                            "Three - two force components and a resisting moment",
                            correct=True,
                        ),
                        opt("Zero - a fixed support carries no reaction"),
                    ),
                    "Roller = 1, pin = 2, fixed = 3. A fixed support also resists "
                    "rotation, adding the moment reaction.",
                ),
                q(
                    "For the worked beam (12 kN load 2 m from the pin A on a 6 m span), "
                    "what is the roller reaction at B?",
                    (
                        opt("8 kN"),
                        opt("4 kN", correct=True),
                        opt("12 kN"),
                        opt("24 kN"),
                    ),
                    "Sum of moments about A: By*6 = 12*2, so By = 4 kN; then Ay = 8 kN.",
                ),
            ),
        ),
        # -- 2. Determinate beams --------------------------------------
        _t(
            "Statically determinate beams",
            "11 min",
            """# Statically determinate beams

A beam is **statically determinate** when equilibrium alone gives every
reaction and internal force - three unknown reactions, three equations.
Once the reactions are known, the job is to find the **internal shear V**
and **bending moment M** at every section, because those are what size the
beam (V governs shear and web design, M governs flexure).

**Sign convention** (the standard one): shear is positive when it tends to
rotate the segment clockwise; bending moment is positive when it **sags**
(concave up, tension on the bottom fibre). A key relationship ties loads,
shear and moment together:

```text
   dV/dx = -w(x)      (slope of shear = minus the distributed load)
   dM/dx =  V(x)      (slope of moment = the shear)
```

So between loads the shear is constant or linear, the moment is linear or
parabolic, and **the moment is a maximum or minimum where the shear crosses
zero** - the single most useful fact for finding peak moment.

```mermaid
graph TD
    REACT["Reactions from equilibrium"] --> CUT["Cut a section at x"]
    CUT --> FBD["Free body of one side"]
    FBD --> V["Sum Fy gives shear V"]
    FBD --> M["Sum M at cut gives moment M"]
    V --> ZERO["Find where V equals zero"]
    ZERO --> MMAX["Moment is maximum there"]
    M --> DIAG["Plot the V and M diagrams"]
```

**Worked example - central point load.** Simply supported span L with a
load P at midspan. By symmetry each reaction is P/2.

```text
Given:  span L, load P at midspan (x = L/2)
        Reactions:  Ay = By = P/2

Shear:  0 < x < L/2   ->  V = +P/2   (constant)
        L/2 < x < L   ->  V = -P/2

Shear crosses zero at midspan  ->  moment is maximum there.

Moment at midspan (cut just left of centre, take left side):
        M_max = (P/2) * (L/2) = P*L/4

Deflection at midspan (elastic, EI constant):
        delta_max = P*L^3 / (48*EI)
```

For a full **uniformly distributed load** w over the span the companions
are the ones every engineer memorizes: max moment `M = w*L^2/8` at midspan,
and max deflection `delta = 5*w*L^4 / (384*EI)`. These closed forms are the
sanity check you hold every computer result up against.

The V and M **diagrams** are the deliverable: plot V(x) and M(x) along the
beam, read off the peak values, and design for them.
""",
        ),
        quiz_lesson(
            "Quiz: Statically determinate beams",
            (
                q(
                    "Along a beam, the bending moment reaches a local maximum or minimum where...",
                    (
                        opt("the distributed load is largest"),
                        opt("the shear force crosses zero", correct=True),
                        opt("the beam is deepest"),
                        opt("a support is located, always"),
                    ),
                    "Because dM/dx = V, the moment is stationary exactly where V = 0.",
                ),
                q(
                    "For a simply supported span L with a central point load P, what is "
                    "the maximum bending moment?",
                    (
                        opt("P*L/8"),
                        opt("P*L/4", correct=True),
                        opt("w*L^2/8"),
                        opt("P*L^3 / (48*EI)"),
                    ),
                    "Reaction P/2 times half-span L/2 gives M_max = P*L/4 at midspan. "
                    "(P*L^3/48EI is the deflection, not the moment.)",
                ),
                q(
                    "For a simply supported span L under a uniform load w, the maximum "
                    "midspan moment is:",
                    (
                        opt("w*L^2/8", correct=True),
                        opt("w*L^2/2"),
                        opt("w*L/4"),
                        opt("5*w*L^4/384"),
                    ),
                    "M_max = w*L^2/8 is the classic UDL result; 5wL^4/384EI is its "
                    "midspan deflection.",
                ),
            ),
        ),
        # -- 3. Trusses ------------------------------------------------
        _t(
            "Trusses - method of joints and sections",
            "11 min",
            """# Trusses - method of joints and sections

A **truss** is an assembly of straight members connected at joints,
idealized as **frictionless pins** and loaded **only at the joints**. Under
those assumptions each member carries **only axial force** - pure tension or
pure compression, no bending. That is why trusses (roofs, bridges, towers)
are so material-efficient.

First check **determinacy**. For a plane truss with m members, r reactions
and j joints:

```text
   m + r = 2j    ->  statically determinate (and, if stable, solvable)
   m + r > 2j    ->  statically indeterminate (extra members / redundancy)
   m + r < 2j    ->  unstable mechanism (will collapse)
```

Each joint gives 2 equations (Sum Fx = 0, Sum Fy = 0), hence the 2j.

**Method of joints** - isolate one pin at a time and enforce Sum Fx = 0 and
Sum Fy = 0. Start at a joint with at most two unknown members. It is
systematic and finds *every* member force, but you march joint to joint.

**Method of sections** - cut an imaginary line through the (up to three)
members you care about, take a free body of one side, and use all three
equilibrium equations - crucially **Sum M = 0 about a smart point** to
isolate a single unknown. It is the fast route to one specific member deep
in the truss.

```mermaid
graph TD
    TRUSS["Truss and joint loads"] --> DET["Check m plus r equals 2j"]
    DET --> REACT["Solve support reactions"]
    REACT --> CHOICE{"Which members needed"}
    CHOICE -->|"all of them"| JOINTS["Method of joints"]
    CHOICE -->|"a few, deep in"| SECT["Method of sections"]
    JOINTS --> FORCES["Member tensions and compressions"]
    SECT --> FORCES
```

**Worked example - method of joints.** A joint carries a downward 10 kN
load. Two members meet there: a horizontal member BC and a diagonal AB at
30 degrees above the horizontal.

```text
At the loaded joint (unknowns F_AB along diagonal, F_BC horizontal):

Sum Fy = 0:   F_AB * sin(30) - 10 = 0
              F_AB = 10 / 0.5 = 20 kN
              (positive assuming tension; sign tells you compression here
               if the diagonal pushes toward the joint)

Sum Fx = 0:   F_BC + F_AB * cos(30) = 0
              F_BC = -20 * 0.866 = -17.3 kN
              (negative sign = the assumed direction was wrong)
```

A **tension** result (member pulls on the joint) is conventionally positive;
a **negative** answer means the member is in **compression** - which matters
enormously, because compression members can **buckle** and are checked
against slenderness (Euler load, NBR 8800 / Eurocode 3), not just yield.
""",
        ),
        quiz_lesson(
            "Quiz: Trusses - method of joints and sections",
            (
                q(
                    "In an idealized pin-jointed truss loaded only at joints, each "
                    "member carries...",
                    (
                        opt("bending moment and shear"),
                        opt("only axial force - pure tension or compression", correct=True),
                        opt("torsion"),
                        opt("no force at all"),
                    ),
                    "Frictionless pins and joint-only loads mean members are two-force "
                    "members: axial force only.",
                ),
                q(
                    "For a plane truss, which condition indicates static determinacy?",
                    (
                        opt("m + r < 2j"),
                        opt("m + r = 2j", correct=True),
                        opt("m + r > 2j"),
                        opt("m = j"),
                    ),
                    "m + r = 2j (and stable) = determinate; greater = indeterminate; "
                    "less = an unstable mechanism.",
                ),
                q(
                    "When is the method of sections the better choice over the method of joints?",
                    (
                        opt("When you need the force in every single member"),
                        opt(
                            "When you need the force in one or a few specific members "
                            "without marching through every joint",
                            correct=True,
                        ),
                        opt("When the truss is unstable"),
                        opt("Only for three-dimensional trusses"),
                    ),
                    "A single cut plus Sum M about a chosen point isolates a target "
                    "member directly - faster than joint-by-joint.",
                ),
            ),
        ),
        # -- 4. Frames and arches --------------------------------------
        _t(
            "Frames and arches",
            "11 min",
            """# Frames and arches

**Frames** are structures whose members are joined rigidly (moment
connections), so unlike trusses their members carry **axial force, shear
AND bending moment** together. A portal frame - two columns and a beam - is
the archetype of a building bay. Determinacy uses the same counting idea,
now with 3 conditions per rigid joint; **internal hinges** each release one
moment and add an equation of condition (Sum M = 0 at the hinge).

**Arches** turn the problem on its head. A curved arch carries load mainly
by **axial compression** pushed along its shape, developing outward
**horizontal thrust** at the supports. A **three-hinged arch** (hinges at
both supports and the crown) is statically determinate: three global
equilibrium equations plus the condition that moment is zero at the crown
hinge give the four unknowns (two components at each support).

If an arch is shaped so that bending moment is **zero everywhere** under a
given load, that shape is the **funicular** (a parabola for uniform load, a
catenary for self-weight). Real masonry and concrete arches are designed
close to the funicular so the material stays in compression - the reason
they span so far in stone.

```mermaid
graph TD
    LOAD["Applied loads"] --> TYPE{"Rigid frame or arch"}
    TYPE -->|"frame"| FRAME["Members carry N V and M"]
    TYPE -->|"arch"| ARCH["Curve carries axial compression"]
    ARCH --> THRUST["Horizontal thrust at supports"]
    FRAME --> HINGE["Internal hinges add conditions"]
    ARCH --> CROWN["Crown hinge, moment equals zero"]
    THRUST --> FUNIC["Funicular shape, minimal bending"]
    CROWN --> FUNIC
```

**Worked example - three-hinged arch thrust.** A three-hinged parabolic
arch spans L = 20 m with rise h = 5 m and carries a total uniform load
w = 10 kN per m. By symmetry each vertical reaction is w*L/2. The horizontal
thrust follows from moment = 0 at the crown hinge.

```text
Given:  L = 20 m, rise h = 5 m, w = 10 kN/m
        Vertical reactions:  Va = Vb = w*L/2 = 10*20/2 = 100 kN

Take the LEFT half, moment about the crown hinge C = 0:
        Va*(L/2) - w*(L/2)*(L/4) - H*h = 0
        100*10  -  10*10*5       - H*5 = 0
        1000    -  500           - H*5 = 0
        H = 500 / 5 = 100 kN  (horizontal thrust at each support)

General result for a parabolic arch under UDL:  H = w*L^2 / (8*h)
        Check:  10 * 400 / (8*5) = 4000/40 = 100 kN  OK
```

Note how a **flatter** arch (smaller rise h) needs a **larger** thrust H -
which is why shallow arches push their abutments hard and demand robust
foundations or ties. Frames and arches are where axial and bending action
combine; understanding both prepares the ground for indeterminate analysis.
""",
        ),
        quiz_lesson(
            "Quiz: Frames and arches",
            (
                q(
                    "How do rigid-frame members differ from truss members?",
                    (
                        opt("Frame members carry no force"),
                        opt(
                            "Frame members carry axial force, shear and bending moment "
                            "together, because the joints are rigid",
                            correct=True,
                        ),
                        opt("Frame members carry only tension"),
                        opt("They are identical"),
                    ),
                    "Rigid (moment) connections transmit bending, so frame members are "
                    "not two-force members.",
                ),
                q(
                    "Why is a three-hinged arch statically determinate?",
                    (
                        opt("It has no reactions"),
                        opt(
                            "The crown hinge adds a condition (moment = 0 there) that, "
                            "with the three global equilibrium equations, solves the four "
                            "support unknowns",
                            correct=True,
                        ),
                        opt("Arches are always indeterminate"),
                        opt("It carries no horizontal thrust"),
                    ),
                    "Two support hinges give four unknowns; three equilibrium equations "
                    "plus the crown-hinge condition make four equations.",
                ),
                q(
                    "For a parabolic three-hinged arch under a uniform load, the "
                    "horizontal thrust is H = w*L^2/(8*h). What happens as the rise h "
                    "decreases (a flatter arch)?",
                    (
                        opt("The thrust H decreases"),
                        opt(
                            "The thrust H increases, pushing harder on the abutments", correct=True
                        ),
                        opt("The thrust becomes zero"),
                        opt("The vertical reactions increase"),
                    ),
                    "H is inversely proportional to h, so a flatter arch develops larger "
                    "horizontal thrust and needs stronger abutments or a tie.",
                ),
            ),
        ),
        # -- 5. Influence lines ----------------------------------------
        _t(
            "Influence lines and moving loads",
            "11 min",
            """# Influence lines and moving loads

Dead load sits still, but a **truck on a bridge or a crane on a rail
moves**. The critical question becomes: *where must the moving load stand to
make a given response - a reaction, a shear, a moment at one section - as
large as possible?* The tool for this is the **influence line**.

An **influence line** is a graph of one specific response (say the moment at
midspan) as a **unit load moves** across the structure. Read it this way:
the ordinate under position x is the value of that response when the unit
load is at x. This is fundamentally different from a shear or moment diagram
(which fixes the load and varies the section); an influence line **fixes the
section and moves the load**.

For statically determinate structures the influence lines are made of
**straight segments**, a fact formalized by the **Muller-Breslau
principle**: the influence line for a reaction or internal force has the
same shape as the **deflected form** you get by releasing that restraint and
imposing a unit displacement. It turns drawing influence lines into a
kinematics sketch.

```mermaid
graph TD
    UNIT["Unit load moves across span"] --> IL["Influence line for one response"]
    IL --> MB["Muller Breslau, release the restraint"]
    MB --> SHAPE["Deflected shape gives the ordinates"]
    SHAPE --> PLACE["Place moving loads at the peaks"]
    PLACE --> POINT["Point load times peak ordinate"]
    PLACE --> UDL["Distributed load times area under line"]
    POINT --> DESIGN["Maximum design response"]
```

Using an influence line to find the maximum effect:

- A **concentrated load** P gives its largest effect when placed at the
  **peak ordinate**: response = P times (peak ordinate).
- A **uniform load** w gives response = w times (**area** under the
  influence line over the loaded length) - so load only the parts of the
  span where the ordinate has the sign you want.

```text
Example - midspan moment, simply supported span L.
The influence line for M at midspan is a triangle,
peak ordinate at midspan = L/4.

Single moving wheel P at midspan:
        M_max = P * (L/4)

Full moving uniform load w over the whole span:
        area of triangle = (1/2) * base * height
                         = (1/2) * L * (L/4) = L^2/8
        M_max = w * (L^2/8) = w*L^2/8   (matches the UDL result - good)
```

Bridge codes (AASHTO LRFD, ABNT NBR 7188 with its TB-450 vehicle, Eurocode
Load Model 1) specify exactly these moving load patterns; influence lines
are how you position them to envelope the worst case at each section.
""",
        ),
        quiz_lesson(
            "Quiz: Influence lines and moving loads",
            (
                q(
                    "What does an influence line show?",
                    (
                        opt("The bending moment at every section for a fixed load"),
                        opt(
                            "The value of one specific response as a unit load moves "
                            "across the structure",
                            correct=True,
                        ),
                        opt("The deflected shape under dead load"),
                        opt("The stress-strain curve of the material"),
                    ),
                    "Influence line = fix the response location, move the unit load. A "
                    "moment diagram does the opposite.",
                ),
                q(
                    "The Muller-Breslau principle says the influence line for a force or "
                    "reaction has the same shape as...",
                    (
                        opt("the bending moment diagram"),
                        opt(
                            "the deflected shape produced by releasing that restraint and "
                            "imposing a unit displacement",
                            correct=True,
                        ),
                        opt("the cross-section of the beam"),
                        opt("the load pattern itself"),
                    ),
                    "Release the restraint, impose a unit movement, and the deflected "
                    "form is the influence line - pure kinematics.",
                ),
                q(
                    "To maximize a response from a moving UNIFORM load using its "
                    "influence line, you compute the response as w times...",
                    (
                        opt("the peak ordinate only"),
                        opt(
                            "the area under the influence line over the loaded length, "
                            "loading only the regions of the desired sign",
                            correct=True,
                        ),
                        opt("the span length"),
                        opt("the number of supports"),
                    ),
                    "Point load uses the peak ordinate; distributed load uses the area, "
                    "loaded where the ordinate has the sign you want.",
                ),
            ),
        ),
        # -- 6. Energy methods -----------------------------------------
        _t(
            "Energy methods and virtual work",
            "12 min",
            """# Energy methods and virtual work

So far we have found forces. But structures must also satisfy
**serviceability** - deflections limited (NBR 6118 caps beam deflection
near L/250, Eurocode similarly) so floors do not sag and finishes do not
crack. **Energy methods** are the elegant, general way to compute a specific
deflection or rotation, and they are the conceptual bridge to indeterminate
analysis.

The workhorse is the **principle of virtual work** (unit-load method). To
find the displacement at a point in a chosen direction:

1. Solve the **real** structure for its internal forces under the actual
   loads (for beams and frames, the moment M along each member).
2. Apply a **virtual unit load** (1) at the point, in the direction of the
   wanted displacement, and solve for its internal forces (m).
3. The external virtual work equals the internal virtual work:

```text
   1 * delta  =  integral over the structure of ( m * M / EI ) dx      (bending)

   For trusses (axial only):
   1 * delta  =  sum over members of ( n * N * L ) / (A*E)

   where  N, M = real member forces      (from step 1)
          n, m = forces from the unit load (from step 2)
```

The virtual load is a mathematical probe: it does no real work, it simply
extracts the deflection you asked about. **Castigliano's second theorem** is
the sibling statement: the deflection at a load equals the partial
derivative of total strain energy with respect to that load,
`delta = dU/dP`.

```mermaid
graph TD
    REAL["Real loads, solve M or N"] --> COMBINE["Combine m times M over EI"]
    UNIT["Virtual unit load at the point"] --> LITTLE["Solve virtual m or n"]
    LITTLE --> COMBINE
    COMBINE --> INTEG["Integrate along members"]
    INTEG --> DELTA["Deflection or rotation delta"]
    DELTA --> CHECK["Check against code limit L over 250"]
```

**Worked example - tip deflection of a cantilever.** A cantilever of length
L carries a point load P at the free end. We want the vertical deflection at
the tip.

```text
Measure x from the free end.
Real moment from P:            M(x) = -P * x
Virtual unit load (1) at tip:  m(x) = -1 * x = -x

1 * delta = integral 0..L of ( m * M / EI ) dx
          = (1/EI) integral 0..L of ( (-x)(-P x) ) dx
          = (P/EI) integral 0..L of x^2 dx
          = (P/EI) * (L^3 / 3)

delta_tip = P*L^3 / (3*EI)     (the standard cantilever result - confirmed)
```

The power of virtual work is its **generality**: the same recipe handles
beams, frames and trusses, point loads, distributed loads, even temperature
and support settlement. And it is exactly the machinery the force method
uses next to solve indeterminate structures.
""",
        ),
        quiz_lesson(
            "Quiz: Energy methods and virtual work",
            (
                q(
                    "In the unit-load (virtual work) method for a beam deflection, what "
                    "are m and M?",
                    (
                        opt("Both are from the real loads"),
                        opt(
                            "M is the moment from the real loads; m is the moment from a "
                            "virtual unit load applied at the point of interest",
                            correct=True,
                        ),
                        opt("Both are from the virtual unit load"),
                        opt("m is the mass and M is the moment"),
                    ),
                    "You combine the real force system (M, N) with the virtual unit-load "
                    "system (m, n): delta = integral of m*M/EI.",
                ),
                q(
                    "Castigliano's second theorem states that the deflection at a load equals...",
                    (
                        opt("the load times the span"),
                        opt(
                            "the partial derivative of total strain energy with respect "
                            "to that load, delta = dU/dP",
                            correct=True,
                        ),
                        opt("the area of the moment diagram"),
                        opt("the reaction at the nearest support"),
                    ),
                    "delta = dU/dP - a compact energy statement equivalent to virtual "
                    "work for computing deflections.",
                ),
                q(
                    "The virtual-work tip deflection of a cantilever with end load P is "
                    "P*L^3/(3*EI). Why do we trust energy methods for such results?",
                    (
                        opt("They only work for cantilevers"),
                        opt(
                            "The method is general - one recipe (combine real and virtual "
                            "internal forces) handles beams, frames and trusses under many "
                            "load types",
                            correct=True,
                        ),
                        opt("They avoid needing the material stiffness EI"),
                        opt("They never require solving the real structure first"),
                    ),
                    "Generality is the point: the same integral of m*M/EI (or sum of "
                    "n*N*L/AE) covers a huge range of structures and loads.",
                ),
            ),
        ),
        # -- 7. Force method -------------------------------------------
        _t(
            "Statically indeterminate structures - the force method",
            "12 min",
            """# Statically indeterminate structures - the force method

Most real structures - continuous beams over many supports, rigid frames,
fixed arches - are **statically indeterminate**: they have **more unknown
reactions or member forces than equilibrium equations**. The extra unknowns
are called **redundants**, and their number is the **degree of static
indeterminacy**. Equilibrium alone is not enough; you also need
**compatibility** (deflections must fit together) and the **material law**
(EI relating force to deformation).

The **force method** (also called the flexibility or method of consistent
deformations) is the classical hand approach:

1. **Choose redundants** - remove enough restraints to leave a stable,
   *determinate* **primary structure** (e.g. remove the middle support of a
   two-span beam, or cut a redundant member).
2. **Solve the primary structure** under the real loads and find the
   displacement at each released point - the **compatibility gap** (delta_0).
3. **Apply each redundant as a unit force** on the primary structure and
   find the displacement it causes - the **flexibility coefficient**
   (delta_11, etc.), computed by virtual work from the previous lesson.
4. **Enforce compatibility** - the real structure has *no* gap at a support,
   so superpose until the total displacement there is zero, and solve for
   the redundant.

```mermaid
graph TD
    INDET["Indeterminate structure"] --> REDUN["Choose redundants"]
    REDUN --> PRIM["Release to a determinate primary structure"]
    PRIM --> D0["Displacement from real loads delta 0"]
    PRIM --> D1["Displacement from unit redundant delta 11"]
    D0 --> COMPAT["Compatibility, total displacement equals zero"]
    D1 --> COMPAT
    COMPAT --> SOLVE["Solve for the redundant force"]
    SOLVE --> FINAL["Superpose for final forces"]
```

The compatibility equation for a single redundant X is a one-liner:

```text
   delta_0  +  X * delta_11  =  0        ->      X = - delta_0 / delta_11

   delta_0   = deflection at the release under the real load
   delta_11  = deflection at the release due to a unit value of X
```

**Worked example - propped cantilever.** A beam of length L is fixed at A
and propped on a roller at B, carrying a uniform load w. It is indeterminate
to the **first degree**. Choose the prop reaction R at B as the redundant;
the primary structure is a cantilever fixed at A, free at B.

```text
Primary cantilever, tip deflection under the UDL (downward):
        delta_0  = w*L^4 / (8*EI)

Tip deflection from a unit upward force at B:
        delta_11 = L^3 / (3*EI)

Compatibility at B (real roller allows no deflection):
        delta_0 = R * delta_11
        w*L^4/(8*EI) = R * L^3/(3*EI)
        R = (w*L^4/8) * (3 / L^3) = 3*w*L/8

So the prop carries  R = 3wL/8  (up).
Equilibrium then gives the fixed-end reaction  = wL - 3wL/8 = 5wL/8,
and the fixed-end moment  M_A = w*L^2/8  - well-known results, recovered.
```

The force method is beautifully intuitive for one or two redundants, but it
grows awkward when there are many (you must pick releases and invert a
flexibility matrix by hand). That practical limit is exactly why the next
lesson's **displacement/stiffness** method won - it automates.
""",
        ),
        quiz_lesson(
            "Quiz: Statically indeterminate structures - the force method",
            (
                q(
                    "What makes a structure statically indeterminate?",
                    (
                        opt("It has fewer members than joints"),
                        opt(
                            "It has more unknown reactions or member forces than the "
                            "available equilibrium equations - the extras are redundants",
                            correct=True,
                        ),
                        opt("It carries no load"),
                        opt("It is made of steel rather than concrete"),
                    ),
                    "Degree of indeterminacy = unknowns minus equilibrium equations; "
                    "those extra unknowns are the redundants.",
                ),
                q(
                    "In the force method, what condition supplies the extra equations "
                    "beyond equilibrium?",
                    (
                        opt("Conservation of mass"),
                        opt(
                            "Compatibility - displacements at the released redundants must "
                            "match the real structure (e.g. zero at a support)",
                            correct=True,
                        ),
                        opt("The speed of the moving load"),
                        opt("Random choice"),
                    ),
                    "delta_0 + X*delta_11 = 0 enforces compatibility; the flexibility "
                    "coefficients come from virtual work.",
                ),
                q(
                    "For the propped cantilever under a uniform load w (span L), the "
                    "force method gives the prop reaction as:",
                    (
                        opt("w*L/2"),
                        opt("3*w*L/8", correct=True),
                        opt("5*w*L/8"),
                        opt("w*L^2/8"),
                    ),
                    "R = delta_0/delta_11 = (wL^4/8)/(L^3/3) = 3wL/8; the fixed end then "
                    "takes 5wL/8. (wL^2/8 is the fixed-end moment, not a reaction.)",
                ),
            ),
        ),
        # -- 8. Matrix stiffness method --------------------------------
        _t(
            "Displacement and matrix stiffness method",
            "12 min",
            """# Displacement and matrix stiffness method

The force method solves for forces; the **displacement method** flips the
unknowns to **displacements and rotations** of the joints. Its matrix form -
the **direct stiffness method** - is the algorithm inside every structural
analysis program, because it is completely systematic: no clever choice of
redundants, just assemble and solve.

The governing relationship for the whole structure is a single matrix
equation:

```text
   { F }  =  [ K ] { D }

   { F } = vector of joint loads (known)
   { D } = vector of joint displacements and rotations (unknown)
   [ K ] = global stiffness matrix (built from the geometry and EA, EI)
```

You **solve for the displacements** { D } = [K]^-1 { F }, then back out each
member's internal forces from its own displacements. The workflow:

1. **Member stiffness** - each element has a stiffness matrix [k] in its
   local axes (axial term EA/L, bending terms in EI/L). For a truss bar it
   is just the axial term; for a beam element it includes shear and moment.
2. **Transform** local [k] to global axes with a rotation matrix.
3. **Assemble** every member's contribution into the global [K] by adding
   terms at the shared **degrees of freedom** (this overlap-and-add step is
   why a shared joint stiffens for all members at once).
4. **Apply boundary conditions** - strike out the rows and columns of the
   restrained (supported) DOFs.
5. **Solve** the reduced system for the free displacements, then recover
   member forces and reactions.

```mermaid
graph TD
    DISC["Discretize into members and joints"] --> KLOC["Member stiffness k local"]
    KLOC --> TRANS["Transform to global axes"]
    TRANS --> ASSEM["Assemble global K"]
    ASSEM --> BC["Apply boundary conditions"]
    BC --> SOLVE["Solve F equals K times D for D"]
    SOLVE --> RECOVER["Recover member forces and reactions"]
    RECOVER --> POST["Post process, check code limits"]
```

**Worked example - axial stiffness of one bar.** A single bar of area A,
modulus E, length L, aligned with the x-axis, connects node 1 to node 2. In
local axial coordinates its stiffness matrix relates the two axial
displacements to the two axial forces:

```python
# Axial bar element stiffness (local axes), F = k @ d
# k has units of force/length; here k_axial = E*A/L
E = 200e6      # kPa  (steel, ~200 GPa)
A = 0.0020     # m^2  (cross-section area)
L = 4.0        # m    (member length)

k_axial = E * A / L                 # = 100000 kN/m

# Element stiffness matrix [ [ k, -k ], [ -k, k ] ]
# Force at node 2 for an applied displacement d2 (node 1 held):
d2 = 0.001                          # m  (1 mm stretch)
F2 = k_axial * d2                   # = 100 kN  tension
# Internal axial force N = k_axial * (d2 - d1) = 100 kN
```

That 2x2 block, transformed and tiled across every member, *is* a truss
solver. Add the bending and shear terms and the same procedure analyzes
continuous beams, frames and full buildings. Understanding it means you can
**read what SAP2000, STAAD or robot are doing** - and spot when a bad mesh,
a missing restraint, or a released DOF has produced a nonsense result. That
judgment, resting on the hand methods from the whole course, is the point of
learning structural analysis.
""",
        ),
        quiz_lesson(
            "Quiz: Displacement and matrix stiffness method",
            (
                q(
                    "In the displacement (stiffness) method, what are the primary unknowns?",
                    (
                        opt("The redundant forces"),
                        opt("The joint displacements and rotations", correct=True),
                        opt("The support reactions only"),
                        opt("The material densities"),
                    ),
                    "The stiffness method solves F = K*D for the joint displacements D "
                    "first, then recovers member forces - the opposite of the force "
                    "method.",
                ),
                q(
                    "What does the global stiffness matrix [K] represent, and how is it built?",
                    (
                        opt("The applied loads; it is measured on site"),
                        opt(
                            "The structure's resistance relating loads to displacements; "
                            "it is assembled by adding each member's stiffness at the "
                            "shared degrees of freedom",
                            correct=True,
                        ),
                        opt("The deflection limits from the code"),
                        opt("A random matrix chosen by the engineer"),
                    ),
                    "Each member's local [k] is transformed to global axes and summed "
                    "(overlap-and-add) at shared DOFs to form [K].",
                ),
                q(
                    "For a single axial bar, the stiffness term is k = E*A/L. With "
                    "E = 200e6 kPa, A = 0.002 m^2, L = 4 m, what force resists a 1 mm "
                    "(0.001 m) stretch?",
                    (
                        opt("10 kN"),
                        opt("100 kN", correct=True),
                        opt("1000 kN"),
                        opt("1 kN"),
                    ),
                    "k = 200e6*0.002/4 = 100000 kN/m; F = k*d = 100000*0.001 = 100 kN.",
                ),
                q(
                    "Why is understanding the stiffness method valuable even though "
                    "software does it for you?",
                    (
                        opt("It lets you avoid ever using software"),
                        opt(
                            "It lets you read and sanity-check what programs like SAP2000 "
                            "or STAAD do - catching bad meshes, missing restraints or wrong "
                            "releases",
                            correct=True,
                        ),
                        opt("It makes the matrices smaller"),
                        opt("It removes the need for boundary conditions"),
                    ),
                    "The method is the engine inside the software; knowing it turns you "
                    "from a button-pusher into someone who can trust and verify results.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "How many independent equilibrium equations are available for a "
                    "planar structure?",
                    (
                        opt("One"),
                        opt("Three - Sum Fx, Sum Fy and Sum M each equal zero", correct=True),
                        opt("Six"),
                        opt("As many as there are members"),
                    ),
                    "2D equilibrium gives exactly three equations; that count drives the "
                    "determinacy tests throughout the course.",
                ),
                q(
                    "Along a beam, the bending moment is a local maximum where the shear force...",
                    (
                        opt("is largest"),
                        opt("crosses zero", correct=True),
                        opt("equals the reaction"),
                        opt("is negative"),
                    ),
                    "Because dM/dx = V, the moment is stationary where V = 0 - the fast "
                    "way to locate peak moment.",
                ),
                q(
                    "In an ideal pin-jointed truss loaded only at joints, each member carries:",
                    (
                        opt("bending and shear"),
                        opt("only axial force (tension or compression)", correct=True),
                        opt("torsion"),
                        opt("no internal force"),
                    ),
                    "Two-force members: axial only. A negative result means compression, "
                    "which must then be checked for buckling.",
                ),
                q(
                    "The plane-truss determinacy condition m + r = 2j means the truss is:",
                    (
                        opt("unstable"),
                        opt("statically determinate (if stable)", correct=True),
                        opt("statically indeterminate"),
                        opt("over-loaded"),
                    ),
                    "Equality = determinate; m + r > 2j = indeterminate; m + r < 2j = a mechanism.",
                ),
                q(
                    "For a parabolic three-hinged arch under a uniform load, the "
                    "horizontal thrust is H = w*L^2/(8*h). A flatter arch (smaller rise "
                    "h) therefore has:",
                    (
                        opt("smaller thrust"),
                        opt("larger thrust, pushing harder on the abutments", correct=True),
                        opt("zero thrust"),
                        opt("no vertical reaction"),
                    ),
                    "H varies inversely with rise, so shallow arches demand robust "
                    "abutments or a tie.",
                ),
                q(
                    "An influence line is used to:",
                    (
                        opt("find stresses for a fixed load"),
                        opt(
                            "find how one response varies as a load moves, and where to "
                            "place moving loads for the worst effect",
                            correct=True,
                        ),
                        opt("size the foundations"),
                        opt("measure material strength"),
                    ),
                    "Fix the response location, move the unit load; then place real "
                    "moving loads at the peaks (point loads) or over the areas (UDL).",
                ),
                q(
                    "The unit-load (virtual work) method finds a deflection by combining:",
                    (
                        opt("two real load cases"),
                        opt(
                            "the real internal forces (M, N) with the internal forces "
                            "(m, n) from a virtual unit load at the point of interest",
                            correct=True,
                        ),
                        opt("the mass and acceleration"),
                        opt("only the support reactions"),
                    ),
                    "delta = integral of m*M/EI (bending) or sum of n*N*L/AE (trusses).",
                ),
                q(
                    "What is a 'redundant' in the analysis of an indeterminate structure?",
                    (
                        opt("A member that carries no load"),
                        opt(
                            "An unknown force beyond what equilibrium alone can determine, "
                            "released to form a determinate primary structure",
                            correct=True,
                        ),
                        opt("A duplicate support that is deleted"),
                        opt("A rounding error"),
                    ),
                    "The force method removes redundants to get a determinate primary "
                    "structure, then restores them via compatibility.",
                ),
                q(
                    "In the force method, the compatibility equation delta_0 + X*delta_11 "
                    "= 0 enforces that:",
                    (
                        opt("the total load is zero"),
                        opt(
                            "the displacement at the released redundant matches the real "
                            "structure (e.g. zero at a support)",
                            correct=True,
                        ),
                        opt("the moment diagram is symmetric"),
                        opt("the beam has constant EI"),
                    ),
                    "delta_0 is the primary-structure gap, delta_11 the flexibility per "
                    "unit redundant; compatibility solves X = -delta_0/delta_11.",
                ),
                q(
                    "In the matrix stiffness method, the equation F = K*D is solved for "
                    "D, where D is the vector of:",
                    (
                        opt("member cross-section areas"),
                        opt("joint displacements and rotations", correct=True),
                        opt("applied loads"),
                        opt("material moduli"),
                    ),
                    "Displacements are the unknowns; [K] is assembled from member "
                    "stiffnesses, boundary conditions are applied, then member forces are "
                    "recovered - the algorithm inside analysis software.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

STRUCTURAL_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_STRUCTURAL_ANALYSIS,)
