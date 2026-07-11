"""Academy seed content - Reinforced Concrete Design.

Designing reinforced-concrete elements to code: the limit-state
philosophy and partial safety factors, material behaviour with bond and
anchorage, flexural design of beams, shear and stirrups, one-way and
two-way slabs, columns with slenderness effects, reinforcement detailing,
and serviceability (cracking and deflection). Every lesson is a direct
explanation grounded in NBR 6118, ACI 318 and Eurocode 2 practice, with a
worked design calculation and a mermaid diagram, followed by a checkpoint
quiz; the course closes with a comprehensive final quiz.
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


_REINFORCED_CONCRETE_DESIGN = SeedCourse(
    slug="reinforced-concrete-design",
    title="Reinforced Concrete Design",
    description=(
        "Designing reinforced-concrete elements to code - limit states, "
        "flexure, shear, slabs, columns and reinforcement detailing, "
        "following NBR 6118, ACI 318 and Eurocode 2 principles. Every "
        "lesson gives a direct explanation, a worked design calculation, "
        "and a diagram, then a checkpoint quiz."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Reinforced Concrete Design

Concrete is strong in compression and weak in tension; steel is strong in
tension. **Reinforced concrete** combines them so that each material does
what it does best. Designing it well means proportioning members so they
are safe against collapse and still serviceable - not too cracked, not too
deflected - over their whole life. This course walks that path element by
element.

The approach is **code-based and concrete**: every lesson explains one
idea directly, works a short numerical example (a design formula or a mini
calculation), and draws the idea as a diagram. After each lesson there is
a short quiz; at the end, a final quiz covers the whole course.

Design here follows the **limit-state** framework common to **NBR 6118**
(Brazil), **ACI 318** (USA) and **Eurocode 2** (Europe). The symbols
differ slightly between codes, but the physics and the logic are the same.

What you will build understanding for, in order:

1. **Limit-state philosophy** - safety factors and design values
2. **Materials, bond and anchorage** - how steel and concrete act together
3. **Flexural design of beams** - singly and doubly reinforced sections
4. **Shear design** - diagonal cracking and stirrups
5. **Slabs** - one-way and two-way behaviour
6. **Columns** - axial load, moments and slenderness
7. **Detailing** - spacing, cover, laps and anchorage in practice
8. **Serviceability** - controlling cracking and deflection

This is the map. Keep a code nearby as you go; the goal is to understand
*why* each rule exists, so the numbers make sense.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "Why do we combine concrete and steel in reinforced concrete?",
                    (
                        opt("Steel is cheaper than concrete per unit volume"),
                        opt(
                            "Concrete is strong in compression but weak in tension, so "
                            "steel carries the tension where concrete would crack",
                            correct=True,
                        ),
                        opt("Concrete cannot resist any load on its own"),
                        opt("Steel protects concrete from rain"),
                    ),
                    "Each material does what it does best: concrete in compression, "
                    "steel in tension.",
                ),
                q(
                    "Which design framework does this course follow?",
                    (
                        opt("Allowable-stress design only"),
                        opt(
                            "Limit-state design, shared in principle by NBR 6118, ACI 318 "
                            "and Eurocode 2",
                            correct=True,
                        ),
                        opt("A single national code with no international basis"),
                        opt("Purely empirical rules of thumb"),
                    ),
                    "Modern codes use limit states; the symbols differ but the logic is common.",
                ),
            ),
        ),
        # -- 1. Limit-state philosophy ---------------------------------
        _t(
            "Limit-state design philosophy and safety factors",
            "10 min",
            """# Limit-state design philosophy and safety factors

A **limit state** is a condition beyond which a structure no longer meets
a design requirement. Two families matter:

- **Ultimate Limit States (ULS)** - collapse, rupture, loss of
  equilibrium, buckling. Getting these wrong risks lives.
- **Serviceability Limit States (SLS)** - excessive deflection, cracking,
  or vibration. These affect usability and durability, not immediate
  safety.

Rather than a single global factor of safety, limit-state design uses
**partial safety factors** applied separately to loads and to materials.
Loads are factored **up** and material strengths factored **down**, so the
design checks a deliberately pessimistic case.

On the **action** side, characteristic loads are increased:

- Permanent (dead) load factor: about **1.4** (NBR/EC2) or **1.2** (ACI).
- Variable (live) load factor: about **1.4** (NBR) or **1.6** (ACI/EC2).

On the **resistance** side, characteristic strengths are reduced by
material factors (gamma_m). Design values:

```text
Design concrete strength:  fcd = fck / gamma_c,  gamma_c = 1.4  (NBR/EC2)
Design steel strength:     fyd = fyk / gamma_s,  gamma_s = 1.15 (NBR/EC2)

Worked example (NBR 6118):
  fck = 30 MPa  ->  fcd = 30 / 1.4  = 21.4 MPa
  fyk = 500 MPa ->  fyd = 500 / 1.15 = 434.8 MPa

Design condition (ULS):   Sd <= Rd
  where Sd = effect of factored loads
        Rd = resistance from design material strengths
```

ACI 318 packages this differently: it multiplies the nominal resistance by
a **strength-reduction factor phi** (e.g. 0.90 for tension-controlled
flexure) instead of dividing each material strength, but the intent is the
same - keep demand comfortably below capacity.

```mermaid
graph LR
    LK["Characteristic loads"] --> LF["Multiply by load factors"]
    LF --> SD["Design load effect Sd"]
    MK["Characteristic strengths"] --> MF["Divide by material factors"]
    MF --> RD["Design resistance Rd"]
    SD --> CHK{"Is Sd less than Rd"}
    RD --> CHK
    CHK -->|"yes"| OK["Safe"]
    CHK -->|"no"| NG["Redesign"]
```

Remember: safety is distributed - factor the loads up, factor the
strengths down, then require demand to stay below capacity for every limit
state.
""",
        ),
        quiz_lesson(
            "Quiz: Limit-state design philosophy and safety factors",
            (
                q(
                    "What distinguishes an Ultimate Limit State from a Serviceability Limit State?",
                    (
                        opt("ULS is about appearance; SLS is about collapse"),
                        opt(
                            "ULS concerns collapse and safety (rupture, buckling); SLS "
                            "concerns usability and durability (deflection, cracking)",
                            correct=True,
                        ),
                        opt("They are the same check with different names"),
                        opt("SLS uses larger safety factors than ULS"),
                    ),
                    "ULS protects life; SLS keeps the structure usable and durable.",
                ),
                q(
                    "How are partial safety factors applied in limit-state design?",
                    (
                        opt("A single global factor multiplies the whole structure"),
                        opt(
                            "Loads are factored up and material strengths factored down, "
                            "separately",
                            correct=True,
                        ),
                        opt("Only the steel is factored; concrete is left unfactored"),
                        opt("Factors are applied only to serviceability checks"),
                    ),
                    "Separate partial factors on actions and on resistances create a "
                    "pessimistic design case.",
                ),
                q(
                    "Using NBR 6118 factors, what is fcd for fck = 40 MPa?",
                    (
                        opt("40 MPa"),
                        opt("28.6 MPa", correct=True),
                        opt("56 MPa"),
                        opt("34.8 MPa"),
                    ),
                    "fcd = fck / gamma_c = 40 / 1.4 = 28.6 MPa.",
                ),
            ),
        ),
        # -- 2. Materials, bond and anchorage --------------------------
        _t(
            "Materials, bond and anchorage",
            "10 min",
            """# Materials, bond and anchorage

Reinforced concrete only works if the two materials **act together**. That
cooperation depends on the properties of each material and on the **bond**
that transfers force between them.

**Concrete** is classed by its characteristic cylinder strength **fck**
(e.g. C25, C30 - 25 or 30 MPa). Its tensile strength is small (roughly
**fctm ~ 0.3 * fck^(2/3)** in Eurocode/NBR terms) and unreliable, so in
ULS design we usually **ignore concrete in tension** and let steel carry
it. The modulus of elasticity grows with strength (Eci scales with the
square root of fck).

**Reinforcing steel** is classed by its characteristic yield strength
**fyk** (e.g. CA-50 at 500 MPa in Brazil, Grade 60 at 420 MPa in the USA).
It is modelled as **elastic-perfectly-plastic**: linear up to yield, then a
flat plateau. Its modulus **Es ~ 200 GPa** is essentially constant.

**Bond** is the shear stress at the steel-concrete interface that lets a
bar develop its force gradually along its length. Ribbed (deformed) bars
bond far better than smooth bars because the ribs bear mechanically on the
concrete. A bar must be embedded a sufficient **anchorage (development)
length** for it to reach yield without slipping:

```text
Basic anchorage length (NBR 6118 / EC2 form):
  lb = (phi / 4) * (fyd / fbd)

  phi = bar diameter
  fyd = design yield strength of steel
  fbd = design bond strength (depends on concrete, bar surface, position)

Worked example:
  phi = 16 mm,  fyd = 435 MPa,  fbd = 2.9 MPa (good bond, C25)
  lb = (16 / 4) * (435 / 2.9) = 4 * 150 = 600 mm

  So a 16 mm bar needs about 600 mm of straight embedment - or a hook
  or bend to shorten it.
```

If anchorage is too short the bar pulls out before yielding - a brittle,
unsafe failure. Hooks, bends and mechanical anchors shorten the straight
length needed.

```mermaid
graph TD
    C["Concrete strong in compression"] --> ACT["Act together via bond"]
    S["Steel strong in tension"] --> ACT
    ACT --> BOND["Bond stress transfers force"]
    BOND --> ANCH["Anchorage length develops yield"]
    ANCH --> OKA["Bar yields safely"]
    ANCH --> SHORT["Too short means pull out"]
    SHORT --> BRIT["Brittle failure"]
```

Remember: design leans on steel for tension and on bond to hand the force
over - no adequate anchorage, no reinforced concrete.
""",
        ),
        quiz_lesson(
            "Quiz: Materials, bond and anchorage",
            (
                q(
                    "In ULS flexural design, how is concrete's tensile strength treated?",
                    (
                        opt("It is the main source of resistance"),
                        opt(
                            "It is usually ignored, because it is small and unreliable - "
                            "steel carries the tension",
                            correct=True,
                        ),
                        opt("It equals the compressive strength"),
                        opt("It is multiplied by the load factor"),
                    ),
                    "Concrete cracks in tension, so design assigns tension to the reinforcement.",
                ),
                q(
                    "What is 'bond' in reinforced concrete?",
                    (
                        opt("A chemical glue applied to bars before pouring"),
                        opt(
                            "The interface shear stress that transfers force between "
                            "steel and concrete along the bar",
                            correct=True,
                        ),
                        opt("The financial guarantee on a construction contract"),
                        opt("The weld between two bars"),
                    ),
                    "Bond lets a bar develop its force gradually; ribbed bars bond much "
                    "better than smooth ones - deformed bars bear mechanically on the "
                    "concrete through their ribs.",
                ),
                q(
                    "What happens if a bar's anchorage length is too short?",
                    (
                        opt("Nothing - length does not affect strength"),
                        opt(
                            "The bar can pull out before reaching yield, a brittle and "
                            "unsafe failure",
                            correct=True,
                        ),
                        opt("The concrete becomes stronger"),
                        opt("The bar yields at a lower stress but stays safe"),
                    ),
                    "Insufficient anchorage means slip before yield; hooks and bends "
                    "shorten the straight length needed.",
                ),
            ),
        ),
        # -- 3. Flexural design of beams -------------------------------
        _t(
            "Flexural design of beams (singly and doubly reinforced)",
            "12 min",
            """# Flexural design of beams (singly and doubly reinforced)

A loaded beam bends: the top fibres shorten (compression) and the bottom
fibres lengthen (tension). We place **tension steel** near the bottom to
carry that tension and let concrete carry the compression at the top.

At ULS we assume the **rectangular stress block**: the curved concrete
compression stress distribution is replaced by a uniform stress over a
depth **a = beta1 * x** (x is the neutral-axis depth). Design rests on
**force equilibrium** and **moment equilibrium** of the cross-section.

For a **singly reinforced** rectangular section (tension steel only), the
concrete compression C balances the steel tension T:

```text
Equilibrium (ACI-style rectangular block):
  T = C
  As * fy = 0.85 * fc * b * a      ->  a = (As * fy) / (0.85 * fc * b)

Nominal moment capacity (lever arm = d - a/2):
  Mn = As * fy * (d - a / 2)

Worked example:
  b = 300 mm, d = 550 mm, fc = 25 MPa, fy = 500 MPa, As = 1600 mm^2
  a  = (1600 * 500) / (0.85 * 25 * 300) = 800000 / 6375 = 125.5 mm
  Mn = 1600 * 500 * (550 - 125.5/2)
     = 800000 * 487.3 = 389.8e6 N.mm = 389.8 kN.m
  Design capacity: phi * Mn = 0.90 * 389.8 = 350.8 kN.m
```

We want a **ductile** failure: the steel should **yield before** the
concrete crushes, giving warning (large deflection and cracking) before
collapse. This is ensured by limiting the neutral-axis depth ratio x/d.
A **tension-controlled** section (ACI) or a section with x/d below the
code limit (NBR/EC2) yields first - never over-reinforce into a sudden
concrete-crushing failure.

When the section is too small to carry the moment with tension steel
alone (x/d would exceed the limit), add **compression steel** near the
top: this is a **doubly reinforced** beam. The compression bars help the
concrete resist compression, restoring ductility and adding capacity.

```mermaid
graph TD
    LOAD["Bending moment on beam"] --> COMP["Concrete compression at top"]
    LOAD --> TENS["Steel tension at bottom"]
    COMP --> EQ["Force and moment equilibrium"]
    TENS --> EQ
    EQ --> DUCT{"Does steel yield first"}
    DUCT -->|"yes"| SINGLE["Ductile singly reinforced"]
    DUCT -->|"no"| DOUBLE["Add compression steel"]
    DOUBLE --> DUCT2["Restored ductility"]
```

Remember: solve equilibrium for the stress block, keep the neutral axis
shallow enough that steel yields first, and add compression steel when a
single layer would force a brittle section.
""",
        ),
        quiz_lesson(
            "Quiz: Flexural design of beams (singly and doubly reinforced)",
            (
                q(
                    "What is the 'rectangular stress block' used for in flexural design?",
                    (
                        opt("It describes the shape of the beam cross-section"),
                        opt(
                            "It replaces the real curved concrete compression stress with "
                            "a uniform stress over a depth a, simplifying equilibrium",
                            correct=True,
                        ),
                        opt("It is the arrangement of stirrups"),
                        opt("It is the deflected shape of the beam"),
                    ),
                    "An equivalent uniform block makes the compression resultant easy to "
                    "compute for equilibrium.",
                ),
                q(
                    "Why do we limit the neutral-axis depth (keep x/d small) in flexural design?",
                    (
                        opt("To use less concrete"),
                        opt(
                            "To ensure the tension steel yields before the concrete "
                            "crushes, giving a ductile, warned failure",
                            correct=True,
                        ),
                        opt("To make the beam lighter"),
                        opt("To avoid needing any reinforcement"),
                    ),
                    "A shallow neutral axis means steel-controlled, ductile failure "
                    "rather than sudden concrete crushing. Over-reinforced sections crush "
                    "the concrete first with little warning, so codes cap x/d.",
                ),
                q(
                    "When is a doubly reinforced beam needed?",
                    (
                        opt("Whenever the beam is longer than 5 m"),
                        opt(
                            "When the section is too small to carry the moment ductilely "
                            "with tension steel alone, so compression steel is added",
                            correct=True,
                        ),
                        opt("Only when there is no bending"),
                        opt("When the concrete is stronger than the steel"),
                    ),
                    "Compression steel restores ductility and adds capacity when a "
                    "single tension layer would over-reinforce the section.",
                ),
            ),
        ),
        # -- 4. Shear design and stirrups ------------------------------
        _t(
            "Shear design and stirrups",
            "11 min",
            """# Shear design and stirrups

Bending is not the only action. Near supports, **shear force** is large,
and combined shear and flexure create **diagonal tension** in the web of a
beam. Because concrete is weak in tension, this can open **diagonal
cracks** at roughly 45 degrees - a potentially **brittle** failure if
unchecked.

Shear resistance is modelled as two contributions:

- **Vc** - the shear carried by the concrete itself (aggregate interlock,
  the compression zone, dowel action of the bars).
- **Vs** - the shear carried by **shear reinforcement**, usually vertical
  **stirrups** (also called links or ties) that cross the diagonal cracks
  and carry the tension across them, like the ties of a truss.

The classic **truss analogy** pictures the cracked beam as a truss:
concrete forms diagonal compression struts, the stirrups are vertical
tension ties, and the longitudinal bars are the chords.

```text
Design condition:
  Vu <= phi * (Vc + Vs)     (ACI form)

Concrete contribution (simplified ACI):
  Vc = 0.17 * lambda * sqrt(fc) * b * d      (SI units, MPa and mm)

Stirrup contribution (vertical stirrups spaced s):
  Vs = (Av * fy * d) / s

Worked example:
  b = 300 mm, d = 550 mm, fc = 25 MPa, fy = 500 MPa
  Vc = 0.17 * 1.0 * sqrt(25) * 300 * 550 = 0.17 * 5 * 165000
     = 140250 N = 140.3 kN
  Two-leg 10 mm stirrup: Av = 2 * 78.5 = 157 mm^2, spacing s = 150 mm
  Vs = (157 * 500 * 550) / 150 = 43175000 / 150 = 287.8 kN
  phi(Vc + Vs) = 0.75 * (140.3 + 287.8) = 0.75 * 428.1 = 321.1 kN
```

If the factored shear Vu exceeds phi*(Vc + Vs), reduce the **stirrup
spacing s** (closer stirrups add capacity) or increase the section. Codes
also cap the **maximum spacing** (e.g. d/2) so every potential diagonal
crack is crossed by at least one stirrup, and require a **minimum**
amount of shear steel even where Vu is small - because shear failure gives
little warning.

```mermaid
graph LR
    VU["Shear force near support"] --> DIAG["Diagonal tension in web"]
    DIAG --> CRACK["Diagonal cracks"]
    CRACK --> VC["Concrete carries Vc"]
    CRACK --> VS["Stirrups carry Vs"]
    VC --> SUM["Total capacity Vc plus Vs"]
    VS --> SUM
    SUM --> CHK{"Is Vu below capacity"}
    CHK -->|"no"| CLOSE["Reduce stirrup spacing"]
```

Remember: shear failure is brittle, so design generously - concrete plus
stirrups must beat the factored shear, keep spacing tight enough to catch
every diagonal crack, and always provide minimum stirrups.
""",
        ),
        quiz_lesson(
            "Quiz: Shear design and stirrups",
            (
                q(
                    "Why is shear failure treated so cautiously in beam design?",
                    (
                        opt("It only affects appearance"),
                        opt(
                            "It is brittle and gives little warning, unlike ductile "
                            "flexural yielding",
                            correct=True,
                        ),
                        opt("It cannot actually cause collapse"),
                        opt("It happens only in columns"),
                    ),
                    "Diagonal-tension failure can be sudden, so codes design shear with "
                    "extra conservatism and minimum stirrups.",
                ),
                q(
                    "What role do stirrups play in shear resistance?",
                    (
                        opt("They increase the bending capacity directly"),
                        opt(
                            "They cross the diagonal cracks and carry tension across them, "
                            "acting like the tension ties of a truss",
                            correct=True,
                        ),
                        opt("They replace the longitudinal reinforcement"),
                        opt("They only hold the bars in place during pouring"),
                    ),
                    "In the truss analogy the stirrups are vertical ties; they provide "
                    "the Vs contribution.",
                ),
                q(
                    "If the factored shear exceeds phi*(Vc + Vs), a direct fix is to...",
                    (
                        opt("remove some stirrups"),
                        opt("increase the stirrup spacing"),
                        opt(
                            "reduce the stirrup spacing s, adding shear capacity",
                            correct=True,
                        ),
                        opt("lengthen the beam"),
                    ),
                    "Vs = Av*fy*d/s, so smaller s means larger Vs; codes also cap the "
                    "maximum spacing.",
                ),
            ),
        ),
        # -- 5. Slabs --------------------------------------------------
        _t(
            "One-way and two-way slabs",
            "11 min",
            """# One-way and two-way slabs

A **slab** is a plate-like member that carries load in bending to its
supports. How it spans depends on its **aspect ratio** - the ratio of the
longer span to the shorter span.

- **One-way slab** - supported on two opposite sides, or with the long
  span at least about **twice** the short span. It bends essentially in
  **one direction** (the short span), like a wide, shallow beam. Main steel
  runs across the short span; lighter **distribution steel** runs the other
  way to spread load and control shrinkage cracking.
- **Two-way slab** - supported on all four sides with a length-to-width
  ratio **below about 2**. It bends in **both directions**, sharing load
  between them, and needs main reinforcement in each direction.

The practical rule of thumb:

```text
Aspect ratio  Ly / Lx   (Ly = longer span, Lx = shorter span)

  Ly / Lx  >= 2   ->  one-way   (spans mainly the short direction)
  Ly / Lx  <  2   ->  two-way   (spans both directions)

One-way slab design (per metre strip, like a beam of width b = 1000 mm):
  w  = 8 kN/m^2 factored load,  Lx = 4.0 m, simply supported
  M  = w * Lx^2 / 8 = 8 * 4.0^2 / 8 = 16 kN.m per metre width
  Then design As per metre exactly like a beam with b = 1000 mm.

Minimum slab steel (shrinkage and temperature, ACI): about 0.0018 * b * h.
```

Design of a one-way slab is just beam design applied to a **1 metre wide
strip**. Two-way slabs are richer: moments are found by coefficient
methods, the direct-design method, yield-line analysis, or finite
elements, and the corners tend to lift and need extra reinforcement.

**Flat slabs** (supported directly on columns, no beams) are a common
two-way form; their critical check is **punching shear** around each
column, where the column can push through the slab.

```mermaid
graph TD
    SLAB["Slab spanning to supports"] --> RATIO{"Long span over short span"}
    RATIO -->|"two or more"| ONE["One way slab"]
    RATIO -->|"less than two"| TWO["Two way slab"]
    ONE --> STRIP["Design a one metre strip as a beam"]
    TWO --> BOTH["Reinforce both directions"]
    TWO --> PUNCH["Check punching shear at columns"]
```

Remember: the aspect ratio decides whether load runs one way or two;
one-way slabs are strip-beams, two-way slabs share load in both directions
and demand a punching-shear check at columns.
""",
        ),
        quiz_lesson(
            "Quiz: One-way and two-way slabs",
            (
                q(
                    "What determines whether a slab acts one-way or two-way?",
                    (
                        opt("The concrete strength"),
                        opt(
                            "The aspect ratio of the spans - long span at least about "
                            "twice the short span acts one-way; otherwise two-way",
                            correct=True,
                        ),
                        opt("The colour of the reinforcement"),
                        opt("Whether it is on the ground floor"),
                    ),
                    "Ly/Lx >= 2 spans mainly the short way (one-way); below 2 it shares "
                    "load both ways.",
                ),
                q(
                    "How is a one-way slab conveniently designed?",
                    (
                        opt("As a column under axial load"),
                        opt(
                            "As a beam of a 1 metre wide strip spanning the short direction",
                            correct=True,
                        ),
                        opt("Only by finite-element analysis"),
                        opt("With no reinforcement at all"),
                    ),
                    "A 1 m strip behaves like a wide, shallow beam, so beam formulas "
                    "apply directly.",
                ),
                q(
                    "For a flat slab supported directly on columns, which check is critical?",
                    (
                        opt("Wind uplift on the roof"),
                        opt("Bond of the column bars only"),
                        opt(
                            "Punching shear around each column, where the column can push "
                            "through the slab",
                            correct=True,
                        ),
                        opt("Torsion of the foundation"),
                    ),
                    "Flat slabs concentrate shear around columns; punching shear governs there.",
                ),
            ),
        ),
        # -- 6. Columns and slenderness --------------------------------
        _t(
            "Columns and slenderness effects",
            "11 min",
            """# Columns and slenderness effects

A **column** is a compression member: it carries axial load down to the
foundation, usually together with **bending moments** from frame action,
eccentric loads or lateral forces. Its longitudinal bars share the
compression and, on one face, may be in tension when moment is large; the
**ties (or spirals)** hold those bars in position and stop them from
buckling outward.

For a **short column** (stocky, low slenderness), strength is governed by
the material capacity of the section. Pure axial capacity is roughly:

```text
Squash load (short column, pure axial, ACI-style):
  Pn = 0.85 * fc * (Ag - Ast) + fy * Ast

  Ag  = gross concrete area
  Ast = total area of longitudinal steel

Worked example:
  300 x 300 mm column, fc = 25 MPa, fy = 500 MPa
  Ast = 4 bars of 20 mm = 4 * 314 = 1256 mm^2
  Ag  = 300 * 300 = 90000 mm^2
  Pn = 0.85 * 25 * (90000 - 1256) + 500 * 1256
     = 21.25 * 88744 + 628000
     = 1885810 + 628000 = 2.51e6 N = 2514 kN
```

Real columns carry axial load **and** moment, so we design against an
**interaction diagram** (P-M curve): the combination of axial force and
moment must fall inside the section's capacity envelope.

**Slenderness** changes the picture. A slender column, when loaded, bows
sideways; that lateral deflection adds an extra **P-delta** moment
(axial force times the sideways displacement), which increases deflection
further - a second-order effect that can trigger **buckling** before the
material limit. Codes gauge it with the **slenderness ratio**:

```text
Slenderness ratio:  lambda = (k * l) / r

  k = effective-length factor (support conditions)
  l = unbraced length
  r = radius of gyration of the section

  Low lambda   ->  short column, second-order effects negligible
  High lambda  ->  slender column, magnify moments (P-delta) or buckling
```

When lambda exceeds the code limit, the design moment must be
**magnified** (or a full second-order analysis performed) to account for
P-delta. Slender columns are therefore weaker than their material capacity
suggests - slenderness, not crushing, may govern.

```mermaid
graph TD
    COL["Column axial load plus moment"] --> INT["Check on P M interaction diagram"]
    COL --> SLEN{"Slenderness ratio"}
    SLEN -->|"low"| SHORT["Short column material governs"]
    SLEN -->|"high"| LONG["Slender column"]
    LONG --> PD["P delta second order moment"]
    PD --> MAG["Magnify design moment"]
    MAG --> BUCK["Guard against buckling"]
```

Remember: columns resist combined axial load and moment on an interaction
diagram, ties restrain the bars, and slenderness adds P-delta moments that
can make buckling - not crushing - the governing failure.
""",
        ),
        quiz_lesson(
            "Quiz: Columns and slenderness effects",
            (
                q(
                    "Real columns are usually designed against what, rather than pure axial capacity?",
                    (
                        opt("A single allowable stress"),
                        opt(
                            "An axial-force and moment (P-M) interaction diagram, since "
                            "they carry combined load and moment",
                            correct=True,
                        ),
                        opt("The shear capacity alone"),
                        opt("Only the deflection limit"),
                    ),
                    "Columns almost always carry moment as well as axial force, so the "
                    "combination must lie inside the P-M envelope.",
                ),
                q(
                    "What is the P-delta (second-order) effect in a slender column?",
                    (
                        opt("The column heats up under load"),
                        opt(
                            "Lateral deflection under load creates an extra moment (axial "
                            "force times displacement) that grows the deflection further",
                            correct=True,
                        ),
                        opt("The concrete shrinks over time"),
                        opt("The bars corrode faster"),
                    ),
                    "The added P-delta moment can cause buckling before the material "
                    "limit is reached, so slender columns need their design moments "
                    "magnified or a full second-order analysis.",
                ),
                q(
                    "A high slenderness ratio lambda = kl/r means the column is...",
                    (
                        opt("short, so second-order effects are negligible"),
                        opt(
                            "slender, so P-delta moments must be magnified and buckling "
                            "guarded against",
                            correct=True,
                        ),
                        opt("stronger than its material capacity"),
                        opt("free of any axial load"),
                    ),
                    "High lambda makes slenderness, not crushing, potentially govern the design.",
                ),
            ),
        ),
        # -- 7. Detailing of reinforcement -----------------------------
        _t(
            "Detailing of reinforcement",
            "11 min",
            """# Detailing of reinforcement

A correct calculation still fails if the bars are badly arranged.
**Detailing** turns the required steel area into buildable, durable,
force-transferring reinforcement. It is where many real-world failures
originate.

Key detailing controls:

- **Concrete cover** - the clear concrete between the outermost bar and the
  surface. It protects steel from **corrosion** and provides fire
  resistance and bond. Cover grows with exposure aggressiveness (NBR 6118
  environmental classes I to IV); an interior slab may use ~20 mm, a marine
  structure much more.
- **Bar spacing** - minimum clear spacing lets the largest aggregate and
  the concrete flow around the bars (good compaction); maximum spacing
  limits crack widths and keeps steel effective.
- **Laps (splices)** - bars come in finite lengths, so they are spliced by
  overlapping (a **lap length**) or by mechanical/welded couplers. Lap
  length is driven by the same bond mechanics as anchorage; laps are
  staggered so not all bars splice at the same section.
- **Anchorage and hooks** - bars must be anchored past the point they are
  no longer needed; standard **90 or 180 degree hooks** develop force in a
  short length near supports.
- **Curtailment** - bars can be stopped where the moment no longer needs
  them, but only after extending a code-required distance past that point
  so bond and shear are respected.
- **Stirrup detailing** - closed ties with proper hooks (often 135 degrees
  into the core) confine the concrete and restrain longitudinal bars,
  which is essential in seismic regions.

```text
Minimum cover guidance (NBR 6118, characteristic examples):
  Class I  (rural, dry)          slabs ~20 mm   beams/columns ~25 mm
  Class II (urban)               slabs ~25 mm   beams/columns ~30 mm
  Class III(marine, industrial)  slabs ~35 mm   beams/columns ~40 mm
  Class IV (aggressive, tidal)   slabs ~45 mm   beams/columns ~50 mm

Clear bar spacing (typical minimum):
  s_min >= the largest of:  bar diameter,  20 mm,  1.2 * max aggregate size
```

The detailer's job is to satisfy all of these at once: enough cover for
durability, enough spacing for compaction, enough lap and anchorage for
force transfer, and stirrups that confine the core.

```mermaid
graph TD
    AS["Required steel from calculation"] --> COVER["Cover for durability and fire"]
    AS --> SPACE["Spacing for compaction and cracks"]
    AS --> LAP["Laps and couplers to splice bars"]
    AS --> ANCH["Anchorage and hooks at ends"]
    AS --> STIR["Stirrup hooks confine the core"]
    COVER --> BUILD["Buildable durable detail"]
    SPACE --> BUILD
    LAP --> BUILD
    ANCH --> BUILD
    STIR --> BUILD
```

Remember: detailing is not an afterthought - cover, spacing, laps,
anchorage and stirrup hooks are what let the calculated steel actually
work in the real structure.
""",
        ),
        quiz_lesson(
            "Quiz: Detailing of reinforcement",
            (
                q(
                    "What is the primary purpose of concrete cover over the reinforcement?",
                    (
                        opt("To make the member heavier"),
                        opt(
                            "To protect the steel from corrosion and provide fire "
                            "resistance and bond",
                            correct=True,
                        ),
                        opt("To reduce the amount of steel needed"),
                        opt("To colour the surface"),
                    ),
                    "Cover grows with exposure class precisely because durability "
                    "(corrosion protection) depends on it.",
                ),
                q(
                    "Why are lap splices staggered rather than all placed at one section?",
                    (
                        opt("To use more steel"),
                        opt(
                            "So the splice does not concentrate at a single weak section - "
                            "spreading them keeps force transfer reliable",
                            correct=True,
                        ),
                        opt("Because bars must always be welded"),
                        opt("Staggering has no engineering purpose"),
                    ),
                    "Lap length follows bond mechanics; staggering avoids a single "
                    "heavily-spliced cross-section.",
                ),
                q(
                    "Detailing is best described as...",
                    (
                        opt("an optional finishing step with no structural effect"),
                        opt(
                            "turning the required steel area into buildable, durable, "
                            "force-transferring reinforcement - cover, spacing, laps, "
                            "anchorage and stirrups",
                            correct=True,
                        ),
                        opt("choosing the concrete colour"),
                        opt("only relevant for columns"),
                    ),
                    "Good numbers still fail if the bars are badly arranged; detailing is "
                    "where many real failures originate.",
                ),
            ),
        ),
        # -- 8. Serviceability -----------------------------------------
        _t(
            "Serviceability: cracking and deflection",
            "11 min",
            """# Serviceability: cracking and deflection

A member can be perfectly safe against collapse yet unfit for use - if it
sags visibly or cracks badly. **Serviceability limit states** check
behaviour under **service (unfactored) loads**, focusing on **deflection**
and **crack width**.

**Cracking.** Because concrete is weak in tension, reinforced concrete is
**expected to crack** - that is how the steel picks up tension. The goal is
not zero cracks but **controlled** crack width, so cracks stay narrow
enough to protect the steel from corrosion and to look acceptable. Codes
limit crack width (for example around **0.3 mm** for typical interior
exposure in NBR 6118 and EC2, tighter for aggressive environments). Narrow
cracks are achieved by using **more, smaller-diameter bars at closer
spacing** rather than a few large bars, and by limiting steel stress under
service load.

**Deflection.** Excessive deflection cracks partitions, ponds water on
roofs, and alarms occupants. Two effects matter:

- **Immediate deflection** under load, computed with an **effective moment
  of inertia** that accounts for cracking (a cracked section is less stiff
  than the gross section).
- **Long-term deflection** from **creep and shrinkage**, which can multiply
  the immediate value by roughly **2 to 3** over years. Compression steel
  reduces long-term deflection by restraining creep.

The simplest control is the **span-to-depth ratio**: keep it below code
limits and detailed deflection calculation is often unnecessary.

```text
Deflection control - span/depth (L/d) guidance (order of magnitude):
  Simply supported beam   L/d  ~  16 to 20
  Continuous beam         L/d  ~  21 to 26
  Cantilever              L/d  ~  7  to 8

Crack-width intuition:
  Same As, smaller bars closer together  ->  narrower cracks
  Lower service steel stress             ->  narrower cracks

Long-term deflection (simple multiplier form):
  delta_total = delta_immediate * (1 + lambda_creep)
  lambda_creep often 2 to 3  ->  long-term sag is dominated by creep
```

Serviceability is checked at service load, not factored load, because the
question is how the structure behaves in everyday use - not whether it
finally collapses.

```mermaid
graph TD
    SERV["Service load behaviour"] --> CRACK["Crack width control"]
    SERV --> DEFL["Deflection control"]
    CRACK --> BARS["More smaller bars closer spaced"]
    CRACK --> STRESS["Limit service steel stress"]
    DEFL --> IMM["Immediate cracked stiffness"]
    DEFL --> LONG["Long term creep and shrinkage"]
    LONG --> COMP["Compression steel reduces creep sag"]
```

Remember: serviceability is checked under everyday loads - concrete is
meant to crack, so control the crack width, and keep deflection in check
with span-to-depth limits and awareness of long-term creep.
""",
        ),
        quiz_lesson(
            "Quiz: Serviceability: cracking and deflection",
            (
                q(
                    "Under what loads are serviceability limit states checked?",
                    (
                        opt("Factored (ultimate) loads"),
                        opt(
                            "Service (unfactored) loads, because the question is everyday "
                            "behaviour, not collapse",
                            correct=True,
                        ),
                        opt("Only wind loads"),
                        opt("No loads at all"),
                    ),
                    "SLS asks how the structure behaves in normal use; ULS is the "
                    "collapse check with factored loads.",
                ),
                q(
                    "What is the correct attitude toward cracking in reinforced concrete?",
                    (
                        opt("Cracks must never occur"),
                        opt(
                            "Cracking is expected - the aim is to control crack width so "
                            "cracks stay narrow and protect the steel",
                            correct=True,
                        ),
                        opt("Cracks improve strength"),
                        opt("Cracks are irrelevant to durability"),
                    ),
                    "Concrete cracks as steel takes up tension; codes limit crack width "
                    "(e.g. about 0.3 mm) rather than forbid cracks. More, smaller bars at "
                    "closer spacing and lower service stress keep cracks narrow.",
                ),
                q(
                    "Why can long-term deflection be much larger than the immediate deflection?",
                    (
                        opt("Because the load factors increase over time"),
                        opt(
                            "Creep and shrinkage of concrete grow deflection over years, "
                            "often by a factor of 2 to 3",
                            correct=True,
                        ),
                        opt("Because steel yields under service load"),
                        opt("Because the span shortens"),
                    ),
                    "Creep and shrinkage dominate long-term sag; compression steel helps "
                    "restrain it.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "In limit-state design, how is safety distributed?",
                    (
                        opt("A single global safety factor on the whole structure"),
                        opt(
                            "Loads are factored up and material strengths factored down, "
                            "then demand must stay below capacity for each limit state",
                            correct=True,
                        ),
                        opt("Only the steel strength is reduced"),
                        opt("Only serviceability is checked"),
                    ),
                    "Partial factors on actions and resistances create a pessimistic "
                    "design case; Sd <= Rd for every limit state.",
                ),
                q(
                    "Why is concrete's tensile strength normally ignored in ULS flexure?",
                    (
                        opt("It is larger than its compressive strength"),
                        opt(
                            "It is small and unreliable, so steel is assigned the tension",
                            correct=True,
                        ),
                        opt("Concrete never experiences tension"),
                        opt("Codes forbid using concrete at all"),
                    ),
                    "The cracked tension zone is carried by reinforcement, not the concrete.",
                ),
                q(
                    "What does an adequate anchorage (development) length ensure?",
                    (
                        opt("The bar rusts more slowly"),
                        opt(
                            "The bar can develop its yield force through bond without pulling out",
                            correct=True,
                        ),
                        opt("The concrete cures faster"),
                        opt("The beam deflects less"),
                    ),
                    "Too-short anchorage gives a brittle pull-out failure; hooks and "
                    "bends shorten the straight length needed.",
                ),
                q(
                    "Keeping the neutral-axis depth ratio x/d small in a beam ensures...",
                    (
                        opt("the concrete crushes first"),
                        opt(
                            "the tension steel yields before the concrete crushes - a "
                            "ductile, warned failure",
                            correct=True,
                        ),
                        opt("no reinforcement is needed"),
                        opt("the beam carries more shear"),
                    ),
                    "A shallow neutral axis gives steel-controlled ductile behaviour "
                    "instead of sudden concrete crushing.",
                ),
                q(
                    "In shear design, what carries the Vs contribution across diagonal cracks?",
                    (
                        opt("The concrete cover"),
                        opt("The longitudinal tension bars only"),
                        opt(
                            "The stirrups (shear reinforcement) crossing the cracks, like "
                            "truss tension ties",
                            correct=True,
                        ),
                        opt("The concrete compression zone alone"),
                    ),
                    "Vc is the concrete's share; Vs = Av*fy*d/s is the stirrups' share.",
                ),
                q(
                    "A slab with long span at least about twice the short span behaves...",
                    (
                        opt("as a two-way slab"),
                        opt(
                            "as a one-way slab, spanning mainly the short direction and "
                            "designed as a 1 metre strip",
                            correct=True,
                        ),
                        opt("as a column"),
                        opt("with no bending at all"),
                    ),
                    "Ly/Lx >= 2 gives one-way action; below 2 the slab shares load both ways.",
                ),
                q(
                    "For a flat slab on columns, which failure mode is the critical check?",
                    (
                        opt("Torsion of the beams"),
                        opt("Bond of the slab bars only"),
                        opt(
                            "Punching shear, where a column can push through the slab",
                            correct=True,
                        ),
                        opt("Wind uplift"),
                    ),
                    "Shear concentrates around columns in flat slabs, so punching shear "
                    "governs there.",
                ),
                q(
                    "How does slenderness affect a column's design?",
                    (
                        opt("It has no effect"),
                        opt(
                            "A slender column develops P-delta second-order moments, so "
                            "moments are magnified and buckling guarded against",
                            correct=True,
                        ),
                        opt("It increases the concrete strength"),
                        opt("It removes the need for ties"),
                    ),
                    "High slenderness makes buckling, not material crushing, potentially "
                    "govern - design moments must be magnified.",
                ),
                q(
                    "Which detailing measure most directly protects reinforcement from corrosion?",
                    (
                        opt("Larger stirrup spacing"),
                        opt(
                            "Adequate concrete cover, increased for aggressive exposure",
                            correct=True,
                        ),
                        opt("Shorter lap lengths"),
                        opt("Fewer, larger bars"),
                    ),
                    "Cover grows with NBR 6118 environmental class; it is the front-line "
                    "durability defence.",
                ),
                q(
                    "Serviceability crack control is best achieved by...",
                    (
                        opt("using a few very large bars"),
                        opt(
                            "using more, smaller-diameter bars at closer spacing and "
                            "limiting service steel stress",
                            correct=True,
                        ),
                        opt("removing the reinforcement"),
                        opt("increasing the load factor"),
                    ),
                    "Concrete is meant to crack; narrow, well-distributed cracks come "
                    "from smaller bars closer together at lower service stress.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

REINFORCED_CONCRETE_DESIGN_COURSES: tuple[SeedCourse, ...] = (_REINFORCED_CONCRETE_DESIGN,)
