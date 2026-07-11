"""Academy seed content - Steel and Timber Structures.

An advanced structural-engineering course on designing with the two
"framed" materials: steel and timber. It covers steel grades and rolled
sections, the design of tension and compression members (with buckling),
beams in bending, and bolted and welded connections; then it turns to
timber - properties and strength grading, sawn members and modern
engineered wood (glulam and CLT) - and closes with fire and corrosion
protection. Every lesson gives a direct explanation, a worked member-
design calculation grounded in Eurocode / AISC / NBR practice, and a
mermaid diagram, each followed by a checkpoint quiz; a comprehensive
final quiz closes the course.
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


_STEEL_TIMBER_STRUCTURES = SeedCourse(
    slug="steel-timber-structures",
    title="Steel & Timber Structures",
    description=(
        "Designing structures in steel and timber - member behavior, "
        "buckling, and connections, plus modern engineered wood (glulam and "
        "CLT), with fire and corrosion protection. Every lesson pairs a "
        "direct explanation with a worked member-design calculation and a "
        "diagram, grounded in Eurocode, AISC and NBR/ABNT practice."
    ),
    level="Advanced",
    lessons=(
        # -- Welcome ---------------------------------------------------
        _t(
            "Welcome - how this course works",
            "5 min",
            """# Steel & Timber Structures

Steel and timber are the two great **framed** materials: instead of
pouring a monolithic mass like concrete, you assemble discrete members -
columns, beams, braces, ties - and join them at connections. That shifts
the design questions. A member is limited not only by the **strength** of
its material but by **stability**: a slender steel column can buckle at a
load far below its yield capacity, and the joints between members often
govern the whole design.

This course walks the design of both materials the way a structural
engineer meets them: what the material is, how each kind of member
behaves (tension, compression, bending), how you connect members, and
how you protect the finished structure from fire and corrosion. Timber
adds its own twist - it is **anisotropic** (strong along the grain, weak
across it) and its strength depends on moisture, load duration, and
grade.

The approach is **concrete**: every lesson explains one idea directly,
works a short real design check with numbers, and draws the idea as a
diagram. After each lesson there is a quiz; a final quiz covers the whole
course. Load and resistance factors follow limit-state design (Eurocode,
AISC LRFD, and NBR 8800 / NBR 7190 in Brazil).

What you will learn, in order:

1. **Steel properties and rolled sections** - grades, the stress-strain
   curve, and the shapes you build with
2. **Tension members** - the simplest member, and why net area governs
3. **Compression members and buckling** - the Euler load and slenderness
4. **Steel beams and bending** - plastic vs elastic capacity, and
   lateral-torsional buckling
5. **Bolted and welded connections** - how members actually join
6. **Timber properties and grading** - anisotropy, moisture, strength
   classes
7. **Timber members and engineered wood** - glulam and CLT
8. **Fire and corrosion protection** - keeping the structure durable

This is a design course: expect formulas, factors, and worked checks. By
the end you should be able to read a member, pick the failure mode that
governs, and size it.
""",
        ),
        quiz_lesson(
            "Quiz: Welcome - how this course works",
            (
                q(
                    "What makes steel and timber 'framed' materials, and why does "
                    "that change the design questions?",
                    (
                        opt("They are poured as one monolithic mass, so only strength matters"),
                        opt(
                            "You assemble discrete members joined at connections, so "
                            "stability (buckling) and the joints often govern, not just "
                            "material strength",
                            correct=True,
                        ),
                        opt("They cannot carry any tension"),
                        opt("They are always stronger than concrete"),
                    ),
                    "Discrete members and joints mean stability and connection design "
                    "matter as much as raw material strength.",
                ),
                q(
                    "Timber is described as anisotropic. What does that mean here?",
                    (
                        opt("It has the same strength in every direction"),
                        opt(
                            "Its strength depends on direction - strong along the grain, "
                            "much weaker across it",
                            correct=True,
                        ),
                        opt("It cannot carry bending"),
                        opt("It is immune to moisture"),
                    ),
                    "Anisotropy is central to timber design: parallel-to-grain and "
                    "perpendicular-to-grain strengths differ greatly.",
                ),
            ),
        ),
        # -- 1. Steel properties and rolled sections -------------------
        _t(
            "Structural steel properties and rolled sections",
            "10 min",
            """# Structural steel properties and rolled sections

Structural steel is prized for a **high strength-to-weight ratio**,
**ductility** (it deforms visibly before it fails, giving warning), and
the fact that it is **manufactured to a specification** - you know its
properties before you build. Its behavior is captured by the
**stress-strain curve** from a tension test.

Key properties, in the order the curve reveals them:

- **Modulus of elasticity** E - the slope of the initial straight
  (elastic) portion. For all structural steels E is about **200 GPa** -
  stiffness does not change with grade, only strength does.
- **Yield strength** f_y - the stress at which steel starts to deform
  permanently (plastically). This is the number most design checks use.
- **Ultimate (tensile) strength** f_u - the peak stress before necking
  and fracture.
- **Ductility** - the strain at fracture; structural steels stretch many
  percent before breaking.

Common grades name the yield strength: European **S235 / S275 / S355**
(f_y in MPa), American **A992** (f_y = 345 MPa, the standard for wide
flanges), Brazilian **ASTM A572 grade 50** and **MR250 / AR350** to NBR.

You do not machine members from blocks - you buy **rolled sections**,
standard shapes rolled hot at the mill:

- **I-sections / wide-flange (W, IPE, HE, UB, UC)** - the workhorse for
  beams and columns; material concentrated in the flanges where bending
  stress is highest.
- **Channels (C, UPN)**, **angles (L)** - bracing, ties, secondary members.
- **Hollow sections (RHS, SHS, CHS)** - closed tubes, excellent in
  compression and torsion.

Each section comes with tabulated properties: area A, second moment of
area I, elastic modulus W_el = I / c, and plastic modulus W_pl.

```mermaid
graph TD
    TEST["Tension test"] --> CURVE["Stress strain curve"]
    CURVE --> E["Modulus E about 200 GPa"]
    CURVE --> FY["Yield strength f_y"]
    CURVE --> FU["Ultimate strength f_u"]
    CURVE --> DUCT["Ductility warning before failure"]
    FY --> GRADE["Grade names f_y S235 S355 A992"]
    GRADE --> SHAPE["Rolled section I channel angle hollow"]
```

Worked example - reading a section and its yield capacity:

```text
Grade S355 steel:  f_y = 355 MPa,  E = 200 GPa
Section IPE 300 (from tables):
    A     = 5380 mm^2   (cross-sectional area)
    W_el  = 557 000 mm^3 (elastic section modulus, major axis)

Axial yield (squash) load of the gross section:
    N_pl = A * f_y = 5380 * 355 = 1 909 900 N approx 1910 kN

Elastic moment at first yield:
    M_el = W_el * f_y = 557 000 * 355 = 197.7e6 N.mm = 197.7 kN.m

Note: E is 200 GPa whether this is S235 or S355 - only f_y (and thus
the capacities above) changes with grade, not the stiffness.
```

Remember: stiffness is a constant (E about 200 GPa); grade sets the
strength; and you design with catalogue sections whose A, I and moduli
are already tabulated.
""",
        ),
        quiz_lesson(
            "Quiz: Structural steel properties and rolled sections",
            (
                q(
                    "How does the modulus of elasticity E differ between grades S235 and S355?",
                    (
                        opt("S355 has a much higher E"),
                        opt(
                            "E is essentially the same (about 200 GPa) for all "
                            "structural steels - only the yield strength f_y differs",
                            correct=True,
                        ),
                        opt("S235 is stiffer than S355"),
                        opt("E depends on the section shape, not the grade"),
                    ),
                    "Stiffness (E about 200 GPa) is constant across structural steel "
                    "grades; the grade number is the yield strength in MPa.",
                ),
                q(
                    "Why are I-sections so common for beams?",
                    (
                        opt("They are the cheapest possible shape"),
                        opt(
                            "Material is concentrated in the flanges, far from the "
                            "neutral axis, where bending stress is highest - efficient "
                            "in bending",
                            correct=True,
                        ),
                        opt("They cannot buckle"),
                        opt("They have no second moment of area"),
                    ),
                    "Placing area in the flanges maximizes I and the section modulus "
                    "for a given weight.",
                ),
                q(
                    "What does the yield strength f_y represent on the stress-strain curve?",
                    (
                        opt("The slope of the elastic portion"),
                        opt("The strain at fracture"),
                        opt(
                            "The stress at which steel begins to deform permanently "
                            "(plastically) - the value most design checks use",
                            correct=True,
                        ),
                        opt("The peak stress before fracture"),
                    ),
                    "f_y is the onset of plastic (permanent) deformation; f_u is the "
                    "ultimate peak, and the initial slope is E.",
                ),
            ),
        ),
        # -- 2. Tension members ----------------------------------------
        _t(
            "Tension members",
            "10 min",
            """# Tension members

A **tension member** is pulled along its axis - a truss bottom chord, a
bracing tie, a hanger. It is the simplest member to understand because it
has no stability problem: you cannot buckle something you are stretching.
Its capacity is pure material strength - but with a catch at the
connections.

Two limit states govern, and you take the **smaller**:

1. **Yielding of the gross section** - the whole member stretching
   plastically. Capacity uses the **gross area** A_g and yield strength:

   `N_pl,Rd = A_g * f_y / gamma_M0`   (Eurocode, with gamma_M0 = 1.0)

2. **Rupture of the net section** - fracture through the line of bolt
   holes, where the cross-section is reduced. Capacity uses the **net
   area** A_net and the ultimate strength f_u (with a larger safety
   factor because fracture is brittle and gives no warning):

   `N_u,Rd = 0.9 * A_net * f_u / gamma_M2`   (gamma_M2 = 1.25)

The **net area** is the gross area minus the material removed by holes on
the critical failure line:  `A_net = A_g - (n_holes * d_hole * t)`.

A subtlety at connections is **shear lag**: if only part of the section
is connected (e.g. an angle bolted through one leg only), the force
cannot spread uniformly, so an **effective net area** `A_eff = U * A_net`
is used, with a reduction factor U < 1. Connect more of the section to
raise U.

```mermaid
graph TD
    N["Axial tension force"] --> GROSS["Gross section yielding"]
    N --> NET["Net section rupture at holes"]
    GROSS --> AG["Uses A_g and f_y"]
    NET --> AN["Uses A_net and f_u"]
    NET --> LAG["Shear lag reduces to A_eff"]
    AG --> MIN["Design capacity is the smaller"]
    AN --> MIN
```

Worked example - a bolted flat tie, grade S275:

```text
Flat bar 200 mm wide x 12 mm thick, grade S275:
    f_y = 275 MPa,  f_u = 430 MPa
Connection: two M20 bolts across the width in one line.
    Standard hole diameter d_hole = 22 mm (20 mm bolt + 2 mm clearance)

Gross area:
    A_g   = 200 * 12 = 2400 mm^2
Net area (subtract two holes on the failure line):
    A_net = 2400 - 2 * 22 * 12 = 2400 - 528 = 1872 mm^2

1) Gross yielding:
    N_pl,Rd = A_g * f_y / gamma_M0 = 2400 * 275 / 1.0
            = 660 000 N = 660 kN
2) Net rupture:
    N_u,Rd  = 0.9 * A_net * f_u / gamma_M2
            = 0.9 * 1872 * 430 / 1.25 = 579 700 N approx 580 kN

Design tension resistance = min(660, 580) = 580 kN  -> net section governs.
```

Remember: a tension member cannot buckle, so it is governed by the
smaller of gross-section yield and net-section rupture - and the holes
you drill to connect it are usually what decides.
""",
        ),
        quiz_lesson(
            "Quiz: Tension members",
            (
                q(
                    "Which two limit states govern a bolted tension member, and which do you take?",
                    (
                        opt("Buckling and bending; take the larger"),
                        opt(
                            "Gross-section yielding and net-section rupture; take the "
                            "smaller capacity",
                            correct=True,
                        ),
                        opt("Only shear at the bolts"),
                        opt("Torsion and fatigue; take the average"),
                    ),
                    "Design resistance is the lesser of gross yielding (A_g, f_y) and "
                    "net rupture (A_net, f_u).",
                ),
                q(
                    "Why does the net-rupture check use f_u with a larger safety "
                    "factor than gross yielding?",
                    (
                        opt("Because f_u is smaller than f_y"),
                        opt(
                            "Fracture through the net section is a brittle failure with "
                            "no warning, so it needs a larger margin",
                            correct=True,
                        ),
                        opt("Because the net area is larger than the gross area"),
                        opt("Because bolts never fail"),
                    ),
                    "Gross yielding is ductile (visible stretching); net rupture is "
                    "brittle fracture, hence the larger partial factor.",
                ),
                q(
                    "What is 'shear lag' in a tension member?",
                    (
                        opt("The delay before a bolt tightens"),
                        opt(
                            "When only part of the section is connected, force cannot "
                            "spread uniformly, so an effective net area A_eff = U*A_net "
                            "(U < 1) is used",
                            correct=True,
                        ),
                        opt("The member yielding before it ruptures"),
                        opt("A property only of welded joints"),
                    ),
                    "Connecting more of the cross-section (e.g. both angle legs) raises "
                    "U toward 1 and reduces the shear-lag penalty.",
                ),
            ),
        ),
        # -- 3. Compression members and buckling -----------------------
        _t(
            "Compression members and buckling",
            "11 min",
            """# Compression members and buckling

Turn the force around and everything changes. A **compression member** (a
column, a strut) can fail long before its material yields, by **buckling**
- suddenly bowing sideways. Buckling is a **stability** failure, and it is
what makes compression design fundamentally different from tension.

The theoretical elastic buckling load of a pin-ended column is the
**Euler load**:

`N_cr = pi^2 * E * I / L^2`

Read what it tells you: capacity depends on **stiffness** (E*I) and the
**square** of the length. Double the length, quarter the capacity. And it
uses I - so a column buckles about its **weakest axis** (smallest I).

End conditions change the effective length through a factor K, giving an
**effective length** `L_cr = K * L`:

- Pinned-pinned: K = 1.0
- Fixed-fixed: K = 0.5
- Fixed-pinned: K = 0.7
- Fixed-free (cantilever column): K = 2.0

The governing parameter is **slenderness** `lambda = L_cr / r`, where
`r = sqrt(I / A)` is the radius of gyration. High slenderness means
buckling governs (elastic, Euler); low slenderness means the material
yields first (squashing). Real columns lie in between, so codes use
**buckling curves** that blend the two and account for imperfections and
residual stresses - the design strength is the squash load N_pl reduced
by a factor **chi** (chi <= 1) that depends on slenderness:

`N_b,Rd = chi * A * f_y / gamma_M1`

```mermaid
graph TD
    N["Axial compression"] --> SLEN["Slenderness lambda equals Lcr over r"]
    SLEN --> LOW["Low slenderness"]
    SLEN --> HIGH["High slenderness"]
    LOW --> YIELD["Squashing material yields"]
    HIGH --> EULER["Euler buckling stability"]
    YIELD --> CHI["Buckling curve reduction chi"]
    EULER --> CHI
    CHI --> NB["Design resistance N_b,Rd"]
```

Worked example - Euler load and slenderness of a column:

```text
Column: IPE 200, pinned both ends, length L = 4.0 m, grade S275.
Section properties (weak axis governs buckling):
    A     = 2850 mm^2
    I_z   = 1.42e6 mm^4   (minor axis - the weak one)
    f_y   = 275 MPa,  E = 200 000 MPa

Effective length (pinned-pinned, K = 1.0):
    L_cr = 1.0 * 4000 = 4000 mm

Euler (elastic critical) buckling load:
    N_cr = pi^2 * E * I_z / L_cr^2
         = 9.87 * 200000 * 1.42e6 / 4000^2
         = 175 200 N approx 175 kN

Compare with the squash (yield) load:
    N_pl = A * f_y = 2850 * 275 = 783 750 N approx 784 kN

N_cr (175 kN) << N_pl (784 kN): this slender column is buckling-governed.
Its usable design load N_b,Rd = chi * N_pl is far below 784 kN, driven by
the low Euler load - increase I (a stockier section) or reduce L_cr.
```

Remember: compression capacity is a contest between yielding and
buckling. Slenderness (L_cr / r about the weak axis) decides which wins,
and the buckling reduction chi turns the squash load into the real
design strength.
""",
        ),
        quiz_lesson(
            "Quiz: Compression members and buckling",
            (
                q(
                    "In the Euler buckling load N_cr = pi^2 E I / L^2, doubling the "
                    "length does what to the buckling capacity?",
                    (
                        opt("Doubles it"),
                        opt("Halves it"),
                        opt("Quarters it - capacity varies with 1 over L squared", correct=True),
                        opt("Leaves it unchanged"),
                    ),
                    "N_cr depends on the square of the (effective) length, so twice the "
                    "length gives one quarter of the buckling load.",
                ),
                q(
                    "About which axis does a doubly-symmetric column tend to buckle?",
                    (
                        opt("The axis with the largest second moment of area"),
                        opt(
                            "The weakest axis - the one with the smallest I (smallest "
                            "radius of gyration)",
                            correct=True,
                        ),
                        opt("Always the major axis"),
                        opt("Buckling does not depend on the axis"),
                    ),
                    "Buckling follows the path of least resistance: the minor axis with "
                    "the smallest I and smallest r.",
                ),
                q(
                    "A very slender steel column fails by which mechanism?",
                    (
                        opt("Material yielding (squashing) at f_y"),
                        opt(
                            "Elastic (Euler) buckling well below the yield load - a "
                            "stability failure",
                            correct=True,
                        ),
                        opt("Net-section rupture"),
                        opt("Shear lag"),
                    ),
                    "High slenderness means the Euler load is reached first; stocky "
                    "columns instead squash at the yield load.",
                ),
            ),
        ),
        # -- 4. Steel beams and bending --------------------------------
        _t(
            "Steel beams and bending",
            "11 min",
            """# Steel beams and bending

A **beam** carries load transverse to its axis, resisting it in
**bending** (and shear). The bending stress across the depth is
`sigma = M * y / I` - zero at the neutral axis, maximum at the extreme
fibres. First yield happens when the outer fibre reaches f_y, at the
**elastic moment**:

`M_el = W_el * f_y`   where `W_el = I / c` (elastic section modulus)

But steel is ductile: after the outer fibre yields, yielding spreads
inward until the **whole section** is plastic - a **plastic hinge**. The
full capacity is the **plastic moment**:

`M_pl = W_pl * f_y`   where W_pl is the plastic section modulus

The ratio `W_pl / W_el` is the **shape factor** - about **1.15** for an
I-section, **1.5** for a solid rectangle. It is the reserve strength
between first yield and full plastification, and it is why steel beam
design uses M_pl (for **compact** sections that can reach it).

The catch: a slender I-beam bent about its strong axis can fail early by
**lateral-torsional buckling (LTB)** - the compression flange, unbraced,
buckles sideways and twists the beam, just as a column flange would. The
resistance drops with the **unbraced length** L_b. You prevent LTB by
**bracing the compression flange** (a floor slab, purlins, or discrete
restraints) so the beam can develop its full M_pl.

So a beam must be checked for: **bending** (M_pl if compact and braced,
reduced if not), **shear** (carried mostly by the web), **deflection**
(a serviceability limit, e.g. span/360), and **LTB** if the compression
flange is unrestrained.

```mermaid
graph TD
    LOAD["Transverse load"] --> BEND["Bending moment M"]
    BEND --> EL["Elastic moment M_el equals W_el f_y"]
    EL --> PL["Plastic moment M_pl equals W_pl f_y"]
    PL --> COMPACT["If compact and braced"]
    COMPACT --> LTB["Else lateral torsional buckling"]
    LOAD --> SHEAR["Shear carried by web"]
    LOAD --> DEFL["Deflection serviceability limit"]
```

Worked example - elastic vs plastic moment of an IPE 300, S355:

```text
IPE 300, grade S355 (f_y = 355 MPa), fully braced compression flange.
Section moduli from tables (major axis):
    W_el = 557 000 mm^3
    W_pl = 628 000 mm^3

Elastic moment (first yield at extreme fibre):
    M_el = W_el * f_y = 557 000 * 355 = 197.7e6 N.mm = 197.7 kN.m

Plastic moment (full section plastified, the design capacity if compact):
    M_pl = W_pl * f_y = 628 000 * 355 = 222.9e6 N.mm = 222.9 kN.m

Shape factor:
    W_pl / W_el = 628 000 / 557 000 = 1.13   (typical for an I-section)

The plastic reserve gives about 13% more moment capacity than first
yield - available only because the compression flange is braced against
lateral-torsional buckling. If it were unbraced over a long span, LTB
would cap the resistance below M_pl.
```

Remember: a compact, laterally-braced steel beam reaches its plastic
moment M_pl = W_pl * f_y; leave the compression flange unbraced and
lateral-torsional buckling steals that capacity.
""",
        ),
        quiz_lesson(
            "Quiz: Steel beams and bending",
            (
                q(
                    "What is the difference between the elastic moment M_el and the "
                    "plastic moment M_pl of a steel beam?",
                    (
                        opt("They are always equal"),
                        opt(
                            "M_el is at first yield of the extreme fibre (W_el * f_y); "
                            "M_pl is full plastification of the whole section "
                            "(W_pl * f_y), which is larger",
                            correct=True,
                        ),
                        opt("M_pl is smaller than M_el"),
                        opt("M_el uses the plastic modulus"),
                    ),
                    "Yielding spreads from the extreme fibre inward until the whole "
                    "section is plastic; the ratio W_pl/W_el is the shape factor.",
                ),
                q(
                    "What is lateral-torsional buckling, and how do you prevent it?",
                    (
                        opt("Web crushing under load; add a thicker web"),
                        opt(
                            "The unbraced compression flange buckling sideways and "
                            "twisting the beam; prevent it by bracing the compression "
                            "flange",
                            correct=True,
                        ),
                        opt("Net-section rupture; add more bolts"),
                        opt("Deflection; make the span shorter"),
                    ),
                    "Restraining the compression flange (slab, purlins, discrete "
                    "braces) reduces the unbraced length so the beam can reach M_pl.",
                ),
                q(
                    "Roughly what is the shape factor (W_pl / W_el) of a typical I-section?",
                    (
                        opt("About 1.15", correct=True),
                        opt("About 0.5"),
                        opt("About 3.0"),
                        opt("Exactly 1.0"),
                    ),
                    "An I-section is about 1.15; a solid rectangle is 1.5. It measures "
                    "the reserve between first yield and full plastification.",
                ),
            ),
        ),
        # -- 5. Bolted and welded connections --------------------------
        _t(
            "Bolted and welded connections",
            "11 min",
            """# Bolted and welded connections

Members only work if they are **joined**, and connections are where many
failures - and most of the detailing effort - live. The two families are
**bolting** and **welding**.

**Bolts** are the site-friendly choice. Structural bolts come in grades
(e.g. **8.8**, **10.9** - the first number is f_u/100 in MPa, the product
of the two is roughly f_y/10). A bolt in a joint can fail by:

- **Shear** of the bolt shank - the bolt sliced across. Capacity per
  shear plane: `F_v,Rd = a_v * f_ub * A / gamma_M2`.
- **Bearing** - the bolt tearing/crushing the plate around the hole.
- **Tension** - pulling the bolt apart along its axis.

Bolted joints work in two ways: **bearing-type** (the plates slip until
the bolt bears on the hole and carries load in shear) or
**slip-critical** (high-strength bolts pretensioned so **friction**
between the faying surfaces carries the load with no slip - used where
movement or fatigue is a concern).

**Welds** fuse members with molten filler metal - stiff, continuous, and
efficient, but needing quality control (a bad weld is hard to see). The
two types:

- **Fillet welds** - a triangular bead in the corner between two parts;
  the workhorse. Sized by **throat thickness** a (about 0.7 * leg). Fails
  in shear on the throat: `F_w,Rd = f_vw,d * a * L_w`.
- **Butt (groove) welds** - fill the gap between aligned parts to make a
  full-strength joint; a full-penetration butt weld is as strong as the
  parent metal.

The design rule that ties it together: check **every** failure path -
bolt shear, plate bearing, weld throat, block tearing, and the members
themselves - and the connection capacity is the **smallest**.

```mermaid
graph TD
    JOINT["Connection"] --> BOLT["Bolted"]
    JOINT --> WELD["Welded"]
    BOLT --> SHEAR["Bolt shear"]
    BOLT --> BEAR["Plate bearing"]
    BOLT --> SLIP["Slip critical friction"]
    WELD --> FILLET["Fillet weld throat in shear"]
    WELD --> BUTT["Full penetration butt weld"]
    SHEAR --> MIN["Capacity is the smallest path"]
    BEAR --> MIN
    FILLET --> MIN
```

Worked example - shear capacity of a bolt group, grade 8.8 M20:

```text
Joint: 4 x M20 grade 8.8 bolts, single shear plane, threads in the plane.
    f_ub = 800 MPa (grade 8.8)
    Tensile stress area A_s = 245 mm^2 (M20)
    a_v = 0.6 (shear factor, threads in shear plane)
    gamma_M2 = 1.25

Shear resistance of ONE bolt (one shear plane):
    F_v,Rd = a_v * f_ub * A_s / gamma_M2
           = 0.6 * 800 * 245 / 1.25
           = 94 080 N approx 94.1 kN

Group of 4 bolts (bearing and block shear assumed not to govern):
    F_group = 4 * 94.1 = 376 kN

This is only the bolt-shear path. The real design capacity is the
minimum of bolt shear, plate bearing on each hole, block tearing of the
plate, and the member itself - always check them all.
```

Remember: a connection is a chain of failure paths - bolt shear, bearing,
weld throat, block tearing - and it is only as strong as the weakest one.
""",
        ),
        quiz_lesson(
            "Quiz: Bolted and welded connections",
            (
                q(
                    "In a slip-critical bolted connection, what actually carries the load?",
                    (
                        opt("The bolt shank in bearing after the plates slip"),
                        opt(
                            "Friction between the pretensioned faying surfaces, so the "
                            "joint does not slip",
                            correct=True,
                        ),
                        opt("The weld throat"),
                        opt("The net section of the plate"),
                    ),
                    "Pretensioned high-strength bolts clamp the plates; friction "
                    "transfers the load without slip - good for fatigue and movement.",
                ),
                q(
                    "How is a fillet weld's strength determined, and how does it fail?",
                    (
                        opt("By its length only; it fails in tension"),
                        opt(
                            "By its throat thickness (about 0.7 x leg) and length; it "
                            "fails in shear on the throat",
                            correct=True,
                        ),
                        opt("It is always as strong as the parent metal"),
                        opt("By the bolt grade"),
                    ),
                    "Fillet-weld capacity is shear on the throat area a * L_w; a full-"
                    "penetration butt weld is the one as strong as the parent metal.",
                ),
                q(
                    "How do you determine the design capacity of a bolted connection?",
                    (
                        opt("Take the largest of all the failure paths"),
                        opt("Only check bolt shear"),
                        opt(
                            "Check every failure path - bolt shear, plate bearing, block "
                            "tearing, the member - and take the smallest",
                            correct=True,
                        ),
                        opt("Add all the failure-path capacities together"),
                    ),
                    "A connection is a chain; its capacity is that of the weakest path, "
                    "so all must be checked.",
                ),
            ),
        ),
        # -- 6. Timber properties and grading --------------------------
        _t(
            "Timber properties and grading",
            "11 min",
            """# Timber properties and grading

Timber is a **natural, anisotropic** material, and that shapes every
design rule. Wood is made of fibres (cells) aligned along the grain, so
it is strong when loaded **parallel to the grain** and much weaker
**perpendicular** to it - compression perpendicular to grain can crush at
a fraction of the parallel strength. It is also **hygroscopic**: it
absorbs and releases moisture, swelling and shrinking, and its strength
and stiffness fall as moisture rises.

Because it grows rather than being manufactured, each piece varies -
**knots, slope of grain, density, and defects** all affect strength. So
timber is sorted by **strength grading**, either **visual** (a grader
inspects knots and grain) or **machine** (each piece is flexed to measure
stiffness, which correlates with strength). Grading assigns a **strength
class** with characteristic values:

- Softwoods: European classes **C14 ... C24 ... C30** (the number is the
  characteristic bending strength f_m,k in MPa).
- Hardwoods: classes **D30 ... D70**.
- Brazil, NBR 7190: classes such as **C20, C30, C40 / C60** for
  coniferous and dicotyledonous species.

Two factors are unique to timber design and multiply the strength:

- **Load duration (k_mod)** - wood is weaker under **long-term** load
  (creep and time-dependent failure). k_mod ranges roughly 0.5
  (permanent) to 1.1 (very short / instantaneous).
- **Moisture / service class** - k_mod also drops in wetter service
  classes (1 dry indoor, 2 covered, 3 exposed).

Design strength (Eurocode 5 form):

`f_d = k_mod * f_k / gamma_M`

```mermaid
graph TD
    TREE["Natural timber"] --> ANISO["Anisotropic grain direction"]
    ANISO --> PARA["Strong parallel to grain"]
    ANISO --> PERP["Weak perpendicular to grain"]
    TREE --> VARY["Knots density defects vary"]
    VARY --> GRADE["Strength grading visual or machine"]
    GRADE --> CLASS["Strength class C24 C30 D40"]
    CLASS --> FD["Design strength f_d"]
    FD --> KMOD["kmod load duration and moisture"]
```

Worked example - design bending strength of a C24 beam:

```text
Grade C24 softwood:  characteristic bending strength f_m,k = 24 MPa
Service class 1 (dry, indoors), medium-term load (e.g. imposed floor load).
From Eurocode 5 tables:
    k_mod   = 0.80   (medium-term, service class 1)
    gamma_M = 1.30   (solid timber)

Design bending strength:
    f_m,d = k_mod * f_m,k / gamma_M
          = 0.80 * 24 / 1.30
          = 14.8 MPa

Same timber under a PERMANENT load (k_mod = 0.60) instead:
    f_m,d = 0.60 * 24 / 1.30 = 11.1 MPa

The identical piece of wood is about 25% weaker in design just because
the load acts permanently - load duration is a first-class design
variable in timber, unlike steel.
```

Remember: timber is anisotropic and moisture-sensitive, sorted into
strength classes by grading; its design strength is the characteristic
value scaled by k_mod (load duration and moisture) - a factor steel has
no equivalent of.
""",
        ),
        quiz_lesson(
            "Quiz: Timber properties and grading",
            (
                q(
                    "Why is timber much weaker in compression perpendicular to the "
                    "grain than parallel to it?",
                    (
                        opt("Perpendicular loading heats the wood"),
                        opt(
                            "Wood fibres run along the grain, so across the grain the "
                            "cell walls crush easily - it is anisotropic",
                            correct=True,
                        ),
                        opt("It is actually stronger perpendicular"),
                        opt("Grading only measures perpendicular strength"),
                    ),
                    "Anisotropy from the aligned cell structure makes parallel-to-grain "
                    "far stronger than perpendicular.",
                ),
                q(
                    "What does the modification factor k_mod account for in timber design?",
                    (
                        opt("The bolt grade"),
                        opt("The colour of the wood"),
                        opt(
                            "Load duration and moisture (service class) - wood is weaker "
                            "under long-term load and in wet conditions",
                            correct=True,
                        ),
                        opt("The span of the beam"),
                    ),
                    "f_d = k_mod * f_k / gamma_M; k_mod falls for longer-duration loads "
                    "and wetter service classes.",
                ),
                q(
                    "What does the '24' in strength class C24 represent?",
                    (
                        opt("The moisture content in percent"),
                        opt("The number of knots allowed"),
                        opt(
                            "The characteristic bending strength f_m,k in MPa",
                            correct=True,
                        ),
                        opt("The density in kg per m3"),
                    ),
                    "In C/D classes the number is the characteristic bending strength "
                    "in MPa; C is softwood, D is hardwood.",
                ),
            ),
        ),
        # -- 7. Timber members and engineered wood ---------------------
        _t(
            "Timber members and engineered wood (glulam, CLT)",
            "11 min",
            """# Timber members and engineered wood (glulam, CLT)

Sawn timber members follow the same member logic as steel - just with
timber's rules. A timber **beam** is checked for bending
(`sigma_m,d <= f_m,d`), shear, bearing (compression perpendicular to
grain at supports), and deflection (creep matters, so a final deflection
uses a creep factor k_def). A timber **column** buckles like a steel one,
governed by slenderness, with a buckling factor k_c reducing the
compressive strength.

But sawn timber is limited by the tree: sizes are modest, long spans warp
and check, and defects cap the strength. **Engineered wood** overcomes
this by breaking wood down and re-gluing it, so defects are dispersed and
you can build large, dimensionally-stable members:

- **Glulam (glued laminated timber)** - many thin **laminations** glued
  face-to-face with the grain all running **lengthwise**. You can curve
  it, taper it, and span far - the material of choice for large timber
  roofs and arches. Strength classes like **GL24h / GL28h / GL32h**
  (homogeneous) or **GL...c** (combined, stronger laminations on the
  outside where bending stress peaks).
- **CLT (cross-laminated timber)** - layers glued in **alternating
  perpendicular directions** (like plywood at a large scale). The
  crossing makes it a **two-way panel** - strong and stiff in both
  directions and dimensionally stable - so it works as walls and floor
  **slabs**, the basis of modern **mass-timber** mid-rise buildings.
- **LVL, I-joists** - veneer- and web-based products for joists and beams.

The trade-off: engineered wood is stronger, larger, more predictable, and
more sustainable (it stores carbon), but costs more and depends on the
glue lines and factory quality control.

```mermaid
graph TD
    SAWN["Sawn timber limited by tree"] --> ENG["Engineered wood re glued"]
    ENG --> GLULAM["Glulam laminations all lengthwise"]
    ENG --> CLT["CLT layers alternating perpendicular"]
    ENG --> LVL["LVL and I joists"]
    GLULAM --> SPAN["Long spans beams and arches"]
    CLT --> PANEL["Two way panels walls and floors"]
    PANEL --> MASS["Mass timber mid rise buildings"]
```

Worked example - bending check of a glulam beam, GL28h:

```text
Glulam beam GL28h:  f_m,k = 28 MPa
Rectangular section b x h = 140 x 450 mm, simply supported span 6.0 m.
Service class 1, medium-term load: k_mod = 0.80, gamma_M = 1.25 (glulam).
Design moment from loads:  M_d = 42 kN.m (given).

Section modulus:
    W = b * h^2 / 6 = 140 * 450^2 / 6 = 4.725e6 mm^3

Design bending stress:
    sigma_m,d = M_d / W = 42e6 / 4.725e6 = 8.9 MPa

Design bending strength:
    f_m,d = k_mod * f_m,k / gamma_M = 0.80 * 28 / 1.25 = 17.9 MPa

Utilization:
    sigma_m,d / f_m,d = 8.9 / 17.9 = 0.50  -> OK (50% utilised)

A 140 x 450 glulam beam spans 6 m at half its bending capacity - a span
and depth that sawn timber of the same grade could not reliably reach.
```

Remember: sawn timber follows normal member checks but is capped by the
tree; glulam re-glues laminations lengthwise for long-span beams, and CLT
cross-laminates into two-way panels for walls and floors - the backbone
of mass-timber construction.
""",
        ),
        quiz_lesson(
            "Quiz: Timber members and engineered wood (glulam, CLT)",
            (
                q(
                    "What is the key difference between glulam and CLT?",
                    (
                        opt("Glulam is steel-reinforced; CLT is not"),
                        opt(
                            "Glulam glues laminations with the grain all lengthwise "
                            "(for beams/arches); CLT alternates layers perpendicular "
                            "(a two-way panel for walls/floors)",
                            correct=True,
                        ),
                        opt("They are the same product with different names"),
                        opt("CLT can only be used for beams"),
                    ),
                    "Glulam is a one-direction laminated beam material; CLT's crossed "
                    "layers make a two-way panel - the basis of mass timber.",
                ),
                q(
                    "Why can engineered wood span farther and more reliably than sawn "
                    "timber of the same species?",
                    (
                        opt("It is denser than steel"),
                        opt(
                            "Breaking wood into laminations and re-gluing disperses "
                            "defects and removes the size limits of the tree, giving "
                            "large, predictable, stable members",
                            correct=True,
                        ),
                        opt("Glue is stronger than wood in every direction"),
                        opt("It contains no moisture"),
                    ),
                    "Dispersing knots and defects and stacking laminations yields "
                    "bigger, more uniform, more dimensionally-stable members.",
                ),
                q(
                    "In a timber column, what does the buckling factor k_c do?",
                    (
                        opt("It increases strength for long columns"),
                        opt(
                            "It reduces the compressive strength based on slenderness, "
                            "just as chi does for steel columns",
                            correct=True,
                        ),
                        opt("It accounts for bolt shear"),
                        opt("It has no effect on capacity"),
                    ),
                    "Timber columns buckle by the same stability logic; k_c (<= 1) cuts "
                    "the compressive strength as slenderness rises.",
                ),
            ),
        ),
        # -- 8. Fire and corrosion protection --------------------------
        _t(
            "Fire and corrosion protection",
            "10 min",
            """# Fire and corrosion protection

A structure must survive its environment over decades, and the two big
durability threats are **fire** and **corrosion**. Steel and timber
behave oppositely under fire, which is one of the most interesting
contrasts in the two materials.

**Steel in fire** - steel does not burn, but it **loses strength and
stiffness sharply as it heats**: by about 550 C it retains roughly half
its yield strength, and unprotected steel in a fire reaches that in
minutes. Because it is thin and conductive, it heats fast. Protection
buys time (a **fire resistance rating** - R30, R60, R90 - minutes to
failure):

- **Intumescent paint** - swells into an insulating char when heated.
- **Boards / sprayed cementitious coatings** - encase the steel.
- **Concrete encasement** or filling hollow sections.
- Design measure: the **section factor** A/V (heated perimeter over
  volume) - chunkier sections heat slower.

**Timber in fire** - counterintuitively, heavy timber performs **well**.
It burns at a slow, **predictable charring rate** (about **0.65 mm/min**
for softwood glulam). The char layer **insulates** the core, which stays
cool and keeps its strength. So you design by **sacrificial charring**:
add extra thickness that is allowed to char away, and check the residual
cross-section. This is why mass-timber (glulam, CLT) can meet fire
ratings - a big section keeps a strong core.

**Corrosion of steel** - steel rusts when exposed to oxygen and moisture,
losing section. Protection:

- **Galvanizing** - a sacrificial zinc coating (the zinc corrodes first).
- **Paint systems / duplex coatings** for aggressive environments.
- **Weathering steel (Cor-Ten)** - forms a stable protective patina.
- **Corrosivity categories** (ISO 12944, C1 to C5/CX) set the system.

Timber's durability enemies are **decay (rot) and insects**, controlled
by keeping it dry, using naturally durable or **preservative-treated**
timber, and detailing to shed water.

```mermaid
graph TD
    DUR["Durability threats"] --> FIRE["Fire"]
    DUR --> CORR["Corrosion and decay"]
    FIRE --> STEELF["Steel loses strength when hot"]
    FIRE --> TIMBERF["Timber chars slowly and insulates"]
    STEELF --> PROT["Intumescent boards encasement"]
    TIMBERF --> SACR["Sacrificial charring residual section"]
    CORR --> GALV["Steel galvanize or coat"]
    CORR --> DECAY["Timber keep dry preservative treatment"]
```

Worked example - residual section of a timber column after 30 min fire:

```text
Glulam column 200 x 200 mm, softwood, fire exposed on all 4 sides.
Design charring rate (notional): beta_n = 0.70 mm/min.
Required fire resistance: R30 (30 minutes).

Char depth on each exposed face:
    d_char = beta_n * t = 0.70 * 30 = 21 mm

Residual ("still-strong") cross-section (both sides of each dimension):
    b_res = 200 - 2 * 21 = 158 mm
    h_res = 200 - 2 * 21 = 158 mm
    A_res = 158 * 158 = 24 964 mm^2  (vs 40 000 mm^2 original)

The inner 158 x 158 mm core is essentially unheated and keeps its full
strength - you check the column on this residual section for the fire
load case. A steel column of similar capacity would need applied fire
protection to survive the same 30 minutes.
```

Remember: heat weakens steel fast (protect it to buy R-minutes) but only
slowly chars timber (design the sacrifice and check the residual core);
against corrosion, galvanize or coat steel and keep timber dry and
treated.
""",
        ),
        quiz_lesson(
            "Quiz: Fire and corrosion protection",
            (
                q(
                    "Why can a large timber (glulam/CLT) member perform well in fire "
                    "without applied protection?",
                    (
                        opt("Timber does not burn at all"),
                        opt(
                            "It chars at a slow, predictable rate; the char layer "
                            "insulates a cool, strong residual core you can design for",
                            correct=True,
                        ),
                        opt("It conducts heat away instantly"),
                        opt("It gains strength when heated"),
                    ),
                    "Sacrificial charring: the outer char protects the inner core, so "
                    "the residual section keeps its strength - unlike steel.",
                ),
                q(
                    "What happens to structural steel as it heats in a fire?",
                    (
                        opt("It gets stronger"),
                        opt(
                            "It loses strength and stiffness sharply - about half its "
                            "yield strength by roughly 550 C - so it needs protection to "
                            "buy time",
                            correct=True,
                        ),
                        opt("It chars like timber"),
                        opt("It is unaffected below 900 C"),
                    ),
                    "Thin, conductive steel heats fast and softens; intumescent paint, "
                    "boards or encasement provide the fire-resistance rating.",
                ),
                q(
                    "How does galvanizing protect steel from corrosion?",
                    (
                        opt("It makes the steel non-conductive"),
                        opt(
                            "A zinc coating corrodes sacrificially in place of the "
                            "steel beneath it",
                            correct=True,
                        ),
                        opt("It seals the steel from all oxygen permanently and never wears"),
                        opt("It converts the steel to stainless steel"),
                    ),
                    "Zinc is anodic to steel and corrodes first (sacrificial "
                    "protection); weathering steel instead forms a stable patina.",
                ),
            ),
        ),
        # -- Final quiz ------------------------------------------------
        quiz_lesson(
            "Check your knowledge",
            (
                q(
                    "How does the modulus of elasticity E vary between structural steel grades?",
                    (
                        opt("It rises with the grade number"),
                        opt(
                            "It is essentially constant (about 200 GPa); only the yield "
                            "strength f_y changes with grade",
                            correct=True,
                        ),
                        opt("It depends on the section shape"),
                        opt("It doubles from S235 to S355"),
                    ),
                    "Stiffness is a material constant across grades; the grade sets "
                    "strength, not stiffness.",
                ),
                q(
                    "A bolted steel tension member is governed by which limit state?",
                    (
                        opt("Only buckling"),
                        opt(
                            "The smaller of gross-section yielding (A_g, f_y) and net-"
                            "section rupture through the holes (A_net, f_u)",
                            correct=True,
                        ),
                        opt("Lateral-torsional buckling"),
                        opt("Charring rate"),
                    ),
                    "Tension members cannot buckle; net-section rupture at the holes "
                    "often governs.",
                ),
                q(
                    "In the Euler load N_cr = pi^2 E I / L^2, a column buckles about which axis?",
                    (
                        opt("The strong axis (largest I)"),
                        opt(
                            "The weak axis (smallest I / smallest radius of gyration)", correct=True
                        ),
                        opt("Any axis equally"),
                        opt("The axis of the applied moment"),
                    ),
                    "Buckling takes the weakest path - the minor axis with the smallest "
                    "second moment of area.",
                ),
                q(
                    "What raises a steel beam's bending capacity from M_el to M_pl?",
                    (
                        opt("Adding bolt holes"),
                        opt(
                            "Ductile yielding spreading through the whole section (full "
                            "plastification) - available if the section is compact and "
                            "the compression flange is braced",
                            correct=True,
                        ),
                        opt("Increasing the moisture content"),
                        opt("Reducing the yield strength"),
                    ),
                    "M_pl = W_pl * f_y > M_el = W_el * f_y; the shape factor W_pl/W_el "
                    "is about 1.15 for an I-section.",
                ),
                q(
                    "What prevents a slender I-beam from reaching its plastic moment?",
                    (
                        opt("Net-section rupture"),
                        opt(
                            "Lateral-torsional buckling of the unbraced compression flange",
                            correct=True,
                        ),
                        opt("Corrosion"),
                        opt("Shear lag"),
                    ),
                    "Brace the compression flange to shorten the unbraced length and "
                    "let the beam develop M_pl.",
                ),
                q(
                    "How do you find the design capacity of a bolted or welded connection?",
                    (
                        opt("Take the largest failure path"),
                        opt(
                            "Check every path (bolt shear, plate bearing, weld throat, "
                            "block tearing, the members) and take the smallest",
                            correct=True,
                        ),
                        opt("Sum all failure paths"),
                        opt("Use only the weld length"),
                    ),
                    "A connection is a chain; its capacity equals that of its weakest link.",
                ),
                q(
                    "Which factor unique to timber scales its strength for load "
                    "duration and moisture?",
                    (
                        opt("The bolt shear factor a_v"),
                        opt("The buckling factor chi"),
                        opt("The modification factor k_mod", correct=True),
                        opt("The shape factor"),
                    ),
                    "f_d = k_mod * f_k / gamma_M; k_mod falls for long-term loads and "
                    "wet service classes - steel has no equivalent.",
                ),
                q(
                    "Why is timber weaker perpendicular to the grain than parallel to it?",
                    (
                        opt("Because grading only tests one direction"),
                        opt(
                            "It is anisotropic - the aligned cell fibres resist load "
                            "along the grain but crush easily across it",
                            correct=True,
                        ),
                        opt("Because moisture only affects one direction"),
                        opt("It is actually stronger perpendicular"),
                    ),
                    "Wood's directional cell structure is the root of every timber design rule.",
                ),
                q(
                    "What distinguishes CLT from glulam?",
                    (
                        opt("CLT is made of steel laminations"),
                        opt(
                            "CLT glues layers in alternating perpendicular directions "
                            "(a two-way panel for walls/floors); glulam runs all "
                            "laminations lengthwise (for beams/arches)",
                            correct=True,
                        ),
                        opt("Glulam is a panel, CLT is a beam"),
                        opt("They are identical"),
                    ),
                    "Cross-lamination gives two-way panel action - the basis of mass-"
                    "timber floors and walls.",
                ),
                q(
                    "In a fire, how do steel and heavy timber behave differently?",
                    (
                        opt("Both lose all strength instantly"),
                        opt(
                            "Steel heats fast and loses strength (needing protection); "
                            "heavy timber chars slowly and its char insulates a strong "
                            "residual core",
                            correct=True,
                        ),
                        opt("Timber melts while steel chars"),
                        opt("Neither is affected by fire"),
                    ),
                    "Design steel with applied protection for R-minutes; design timber "
                    "by sacrificial charring and check the residual section.",
                ),
            ),
            duration="10 min",
        ),
    ),
)

STEEL_TIMBER_STRUCTURES_COURSES: tuple[SeedCourse, ...] = (_STEEL_TIMBER_STRUCTURES,)
