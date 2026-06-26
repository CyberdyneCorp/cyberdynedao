"""Engineering Graphics, GD&T & CAD track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on communicating designs. Starts from
orthographic/isometric projection and sketching, moves through dimensioning,
tolerance stacks and GD&T per ASME Y14.5, and ends with parametric solid
modelling, assemblies, model-based definition and CAD automation/optimization.
Lessons are `text` with LaTeX, interactive ```plot blocks, ```mermaid workflow
diagrams and runnable ```python / ```matlab code.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Engineering Graphics, GD&T & CAD — Basics ────────────────────────────────

_BASICS = SeedCourse(
    slug="engineering-graphics-cad-basics",
    title="Engineering Graphics, GD&T & CAD — Basics",
    description=(
        "The visual language of mechanical engineering. Learn orthographic and "
        "isometric projection, the alphabet of lines, multiview layout, sectional "
        "and auxiliary views, and basic dimensioning so a drawing communicates a "
        "part unambiguously. Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "The graphic language: views and projection",
            "11 min",
            r"""
# The graphic language: views and projection

An engineering drawing is a precise, standardized **language**. A 3D object is
flattened onto a 2D sheet by **projection**: rays from the object strike a
projection plane. In **orthographic projection** the rays are parallel and
perpendicular to the plane, so each view shows true shape and size with no
perspective distortion.

The two world standards differ only in *arrangement*. In **third-angle**
projection (ASME, North America) each view sits on the side it is seen from — the
top view is above the front. In **first-angle** projection (ISO, most of the
world) the object is imagined between observer and plane, so the top view falls
below the front. A symbol in the title block declares which is used.

A point projects at distance equal to its coordinate along the viewing axis. For
an observer looking along $z$, a 3D point $(x,y,z)$ maps to the planar point
$(x,y)$ — depth $z$ is simply discarded:

```plot
{"title": "Orthographic projection: image height vs object height (1:1, no distortion)", "xLabel": "object height (mm)", "yLabel": "projected height (mm)", "xRange": [0, 50], "yRange": [0, 50], "grid": true, "functions": [{"expr": "x", "label": "orthographic (parallel rays)", "color": "#2563eb"}, {"expr": "x*0.7", "label": "perspective (foreshortened)", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  OBJ["3D object"] --> PROJ["Projection onto plane"]
  PROJ --> O["Orthographic - parallel rays, true size"]
  PROJ --> P["Perspective - converging rays, foreshortened"]
  O --> ANG{"View arrangement"}
  ANG --> FA["First-angle - ISO"]
  ANG --> TA["Third-angle - ASME"]
```

**Next:** the standardized line types that carry meaning on every drawing.
""",
        ),
        _t(
            "The alphabet of lines",
            "10 min",
            r"""
# The alphabet of lines

Every line on a drawing has a defined meaning and weight, codified in ASME Y14.2
and ISO 128. Reading a drawing is largely reading its lines. The two governing
weights are a **thick** line (visible/cutting, roughly 0.5–0.7 mm) and a **thin**
line (hidden, center, dimension, extension, roughly 0.25–0.35 mm), giving a
contrast ratio near 2:1 so the part outline pops.

The core set:

- **Visible (object) line** — thick, continuous: edges you can see.
- **Hidden line** — thin, dashed: edges behind material.
- **Center line** — thin, long-short-long: axes of symmetry and holes.
- **Dimension & extension lines** — thin, continuous, with arrowheads.
- **Cutting-plane line** — thick, where a section is taken.
- **Phantom line** — thin, long-dash-dash: alternate positions, adjacent parts.

```mermaid
flowchart TB
  L["Line on drawing"] --> VIS["Thick continuous -> visible edge"]
  L --> HID["Thin dashed -> hidden edge"]
  L --> CEN["Thin long-short -> center / axis"]
  L --> DIM["Thin with arrows -> dimension"]
  L --> CUT["Thick -> cutting plane"]
```

A precedence rule resolves overlaps: a **visible** line wins over a hidden line,
which wins over a center line. Get the lineweights and precedence right and the
drawing is legible at a glance; get them wrong and a machinist reads the wrong
geometry.

**Next:** arranging the six principal views into a coherent multiview drawing.
""",
        ),
        _t(
            "Multiview drawings and view selection",
            "11 min",
            r"""
# Multiview drawings and view selection

A glass box surrounds the object; project each face onto the nearest pane, then
unfold the box into the plane of the paper. This yields the **six principal
views** (front, top, bottom, left, right, rear). In practice three views —
front, top, right — fully describe most prismatic parts.

Choose the **front view** as the one showing the most characteristic shape and
the fewest hidden lines, usually the natural functioning or machining
orientation. Width carries across between front and top; depth transfers from top
to side via a 45° miter line, keeping all views in alignment.

```mermaid
flowchart TB
  TOP["TOP view"]
  FRONT["FRONT view"]
  RIGHT["RIGHT-side view"]
  TOP -->|"width aligns"| FRONT
  FRONT -->|"height aligns"| RIGHT
  TOP -.->|"depth via 45 miter"| RIGHT
```

The number of views is an economy: include only as many as remove all ambiguity.
A cylinder needs two; a sphere needs one plus a note. Over-drawing wastes effort,
under-drawing leaves the part undefined. The relationship between necessary views
and feature complexity is roughly monotonic:

```plot
{"title": "Views required vs feature complexity", "xLabel": "feature complexity (count)", "yLabel": "views needed", "xRange": [0, 10], "yRange": [0, 6], "grid": true, "functions": [{"expr": "1 + log(1+x)", "label": "views = 1 + ln(1+complexity)", "color": "#16a34a"}]}
```

**Next:** revealing interior features with sectional and auxiliary views.
""",
        ),
        _t(
            "Sectional and auxiliary views",
            "11 min",
            r"""
# Sectional and auxiliary views

Hidden lines clutter complex interiors. A **section view** imagines a cutting
plane slicing the part; the near half is removed and exposed solid faces are
filled with **hatching** (section lining) at 45°, spaced for the material. The
cutting-plane line and arrows in an adjacent view show where the cut is taken and
the viewing direction.

Common types: **full section** (plane passes entirely through), **half section**
(one quarter removed, showing inside and outside), **offset section** (stepped
plane catching several features), **broken-out** (local), and **revolved/removed**
sections for ribs and spokes. Webs and ribs are **not** hatched when the plane
passes along them, to avoid implying a solid disk.

An **auxiliary view** projects onto a plane *parallel to an inclined surface* so
that surface appears in true size and shape — impossible in any principal view.
You project perpendicular to the slanted face and transfer the depth dimension.

```mermaid
flowchart LR
  PART["Part with inclined / interior feature"] --> Q{"What to show?"}
  Q -->|"interior"| SEC["Section view - cut + hatch"]
  Q -->|"true shape of slanted face"| AUX["Auxiliary view - project normal to face"]
  SEC --> FULL["full / half / offset / broken-out"]
```

```plot
{"title": "Hatch line spacing vs section area (keep ~constant density)", "xLabel": "section area (cm^2)", "yLabel": "recommended spacing (mm)", "xRange": [0, 50], "yRange": [0, 6], "grid": true, "functions": [{"expr": "1.5 + 0.07*x", "label": "spacing guide", "color": "#2563eb"}]}
```

**Next:** placing dimensions so the part can actually be made.
""",
        ),
        _t(
            "Dimensioning fundamentals",
            "11 min",
            r"""
# Dimensioning fundamentals

A view shows shape; **dimensions** give size and location. Good dimensioning is a
discipline: every feature gets exactly one **size** dimension and the **location**
dimensions needed to place it — no more (over-dimensioning creates conflicting
requirements), no less.

Rules from ASME Y14.5: dimension to **visible** outlines, not hidden lines; place
dimensions between views and off the part; keep extension lines from crossing
where avoidable; group related dimensions; never duplicate a dimension. Use a
clear scheme:

- **Chain (incremental)** — each feature located from the previous one. Simple,
  but tolerances *accumulate*.
- **Baseline (datum)** — every feature located from one reference. Tolerances do
  not stack.

Tolerance accumulation is the key trade-off. For $n$ chained dimensions each with
tolerance $\pm t$, the worst-case spread at the last feature grows linearly:

$$T_{\text{chain}} = n\,(2t), \qquad T_{\text{baseline}} = 2t.$$

```plot
{"title": "Worst-case tolerance buildup: chain vs baseline", "xLabel": "number of dimensions n", "yLabel": "accumulated tolerance (mm)", "xRange": [1, 8], "yRange": [0, 4], "grid": true, "functions": [{"expr": "0.5*x", "label": "chain (accumulates)", "color": "#dc2626"}, {"expr": "0.5", "label": "baseline (constant)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  F["Feature"] --> S["Size dimension (exactly one)"]
  F --> L["Location dimension(s)"]
  L --> CH["Chain - errors add"]
  L --> BL["Baseline - from one datum"]
```

**Next:** scales, title blocks and the conventions that finish a drawing.
""",
        ),
        _t(
            "Scale, title blocks and drawing standards",
            "10 min",
            r"""
# Scale, title blocks and drawing standards

A finished sheet carries more than geometry. The **scale** states the ratio of
drawing size to real size — $1{:}1$ full, $1{:}2$ half, $2{:}1$ enlarged. The
golden rule: **always dimension the true size**, never the scaled measurement, so
a print can be enlarged or reduced without lying about the part.

$$\text{drawn length} = \text{true length} \times \text{scale factor}.$$

```plot
{"title": "Drawn length vs true length for common scales", "xLabel": "true length (mm)", "yLabel": "drawn length (mm)", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x", "label": "1:1 full", "color": "#2563eb"}, {"expr": "0.5*x", "label": "1:2 half", "color": "#16a34a"}, {"expr": "2*x", "label": "2:1 double", "color": "#dc2626"}]}
```

The **title block** (lower-right) records part name and number, material, scale,
sheet size (A4–A0 or ANSI A–E), revision, units, tolerance defaults, and
approvals — it is the metadata index of the drawing. A **revision table** logs
every change so released prints stay traceable, and zone grid references locate
features on large sheets.

```mermaid
flowchart TB
  SHEET["Drawing sheet"] --> GEO["Views + dimensions"]
  SHEET --> TB["Title block: part no, material, scale, units"]
  SHEET --> REV["Revision table: rev, date, description"]
  SHEET --> NOTES["General notes + default tolerances"]
```

These conventions make a drawing a contract — anyone, anywhere, reads the same
intent.

**Next:** check your understanding of orthographic graphics fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Graphics, GD&T & CAD — Intermediate ──────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="engineering-graphics-cad-intermediate",
    title="Engineering Graphics, GD&T & CAD — Intermediate",
    description=(
        "The quantitative core of tolerancing and GD&T. Covers limits, fits and "
        "the ISO IT-grade system, the 14 geometric characteristics of ASME "
        "Y14.5, datum reference frames, material condition modifiers and bonus "
        "tolerance, and statistical tolerance stack-up analysis. Worked examples "
        "with plots, diagrams and Python."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Limits, fits and tolerances",
            "12 min",
            r"""
# Limits, fits and tolerances

No part is perfect, so every dimension has a **tolerance** — a permissible range.
The **limits** are the maximum and minimum acceptable sizes; their difference is
the tolerance $T = D_{\max} - D_{\min}$. The ISO 286 system standardizes this
with **IT grades** (IT01–IT18): the tolerance magnitude scales with the
standard tolerance unit $i$ (in micrometres) as

$$i = 0.45\,\sqrt[3]{D} + 0.001\,D \quad (D \text{ in mm}),$$

with each grade a fixed multiple of $i$. Coarser grades give larger tolerances
for larger parts, which is why $T$ grows with nominal size:

```plot
{"title": "ISO standard tolerance unit i vs nominal size", "xLabel": "nominal diameter D (mm)", "yLabel": "tolerance unit i (micrometres)", "xRange": [1, 100], "yRange": [0, 3], "grid": true, "functions": [{"expr": "0.45*(x)^(1/3) + 0.001*x", "label": "i = 0.45 D^(1/3) + 0.001 D", "color": "#2563eb"}]}
```

A **fit** is the relationship between a hole and a shaft. **Clearance** fits
always leave a gap, **interference** fits always overlap (press fits), and
**transition** fits may do either. The **hole-basis** system fixes the hole's
lower limit at nominal and varies the shaft (e.g. H7/g6 clearance, H7/p6
interference).

```python
import numpy as np

# Hole 25 H7 (+0/+0.021), shaft 25 g6 (-0.007/-0.020) -> clearance fit
hole = (25.000, 25.021)   # (min, max)
shaft = (25.000 - 0.020, 25.000 - 0.007)
max_clearance = hole[1] - shaft[0]   # 0.041 mm
min_clearance = hole[0] - shaft[1]   # 0.007 mm
print(round(min_clearance, 3), round(max_clearance, 3))  # 0.007 0.041
```

**Next:** why coordinate tolerancing alone is not enough — the case for GD&T.
""",
        ),
        _t(
            "Why GD&T: from coordinate tolerancing to function",
            "11 min",
            r"""
# Why GD&T: from coordinate tolerancing to function

Plus/minus coordinate tolerancing on a hole's $x$ and $y$ position produces a
**square** tolerance zone. But function — will the bolt pass? — depends on radial
distance from true position, which is circular. The corners of the square allow
positions farther than the sides, so a square zone *rejects good parts at the
sides and accepts marginal ones at the corners*. The diagonal is $\sqrt 2 \approx
1.41\times$ the side, so GD&T's round zone legitimately gains ~57% more usable
area:

$$A_{\square} = (2t)^2, \qquad A_{\bigcirc} = \pi\left(t\sqrt2\right)^2 = 2\pi t^2,
\qquad \frac{A_{\bigcirc}}{A_{\square}} = \frac{\pi}{2} \approx 1.57.$$

```plot
{"title": "Position error allowed vs direction: square (+/-) vs round (true position) zone", "xLabel": "angle (rad)", "yLabel": "max radial error (relative)", "xRange": [0, 1.57], "yRange": [0, 1.6], "grid": true, "functions": [{"expr": "1/cos(x)", "label": "square zone boundary", "color": "#dc2626"}, {"expr": "1.41", "label": "round zone (uniform)", "color": "#16a34a"}]}
```

**GD&T** (Geometric Dimensioning & Tolerancing, ASME Y14.5 / ISO 1101) controls
*geometry* — form, orientation, location, runout — relative to functional
**datums**, not just point-to-point distances. It captures design intent, enables
functional gaging, and unlocks **bonus tolerance**.

```mermaid
flowchart LR
  CT["Coordinate +/- tolerancing"] --> P1["Square zone - rejects good parts"]
  CT --> P2["No datum reference - ambiguous setup"]
  GDT["GD&T per ASME Y14.5"] --> B1["Round/functional zones"]
  GDT --> B2["Datum reference frame"]
  GDT --> B3["Bonus tolerance at MMC"]
```

**Next:** the fourteen geometric characteristic symbols and how to read a feature control frame.
""",
        ),
        _t(
            "Geometric characteristics and feature control frames",
            "12 min",
            r"""
# Geometric characteristics and feature control frames

ASME Y14.5 defines **14 geometric characteristics** in five families:

- **Form** (no datum): straightness, flatness, circularity, cylindricity.
- **Orientation**: parallelism, perpendicularity, angularity.
- **Location**: position, concentricity, symmetry.
- **Profile**: profile of a line, profile of a surface.
- **Runout**: circular runout, total runout.

Each control is written in a **feature control frame (FCF)**: a rectangle reading
left to right as *characteristic symbol | tolerance zone (with modifiers) |
datum references*. For example, position $\varnothing 0.2\,\text{(M)}$ to datums
A B C means "the axis must lie within a 0.2 mm cylindrical zone at MMC, oriented
and located by the A-B-C datum reference frame".

```mermaid
flowchart LR
  FCF["Feature Control Frame"] --> SYM["Symbol - e.g. position"]
  FCF --> TOL["Tolerance + modifier - 0.2 (M)"]
  FCF --> D["Datums - A | B | C (primary->tertiary)"]
  SYM --> FAM{"Family"}
  FAM --> FORM["Form"]
  FAM --> ORI["Orientation"]
  FAM --> LOC["Location"]
  FAM --> RUN["Runout / Profile"]
```

The tolerance value is the **diameter or width of the zone** within which the
controlled feature (axis, surface, center plane) must lie. Form controls take no
datum; orientation, location and runout require one or more.

```python
characteristics = {
    "form":        ["straightness", "flatness", "circularity", "cylindricity"],
    "orientation": ["parallelism", "perpendicularity", "angularity"],
    "location":    ["position", "concentricity", "symmetry"],
    "profile":     ["profile_of_line", "profile_of_surface"],
    "runout":      ["circular_runout", "total_runout"],
}
print(sum(len(v) for v in characteristics.values()))  # 14
```

**Next:** how datums build the reference frame that everything is measured against.
""",
        ),
        _t(
            "Datums and the datum reference frame",
            "11 min",
            r"""
# Datums and the datum reference frame

A **datum** is a theoretically exact reference — a point, axis or plane —
established from a real, imperfect **datum feature** on the part. To measure
orientation and location repeatably you need to fully constrain the part's six
**degrees of freedom** (three translations, three rotations). This is done with a
**datum reference frame (DRF)**: three mutually perpendicular planes.

The classic 3-2-1 rule sets up the frame for a prismatic part:

- **Primary datum (A)** — first contact, three high points, removes 3 DOF (one
  translation, two rotations).
- **Secondary datum (B)** — two points, removes 2 DOF.
- **Tertiary datum (C)** — one point, removes the last 1 DOF.

$$3 + 2 + 1 = 6 \text{ degrees of freedom fully constrained.}$$

```mermaid
flowchart LR
  PART["Part with 6 DOF"] --> A["Datum A - 3 points -> -3 DOF"]
  A --> B["Datum B - 2 points -> -2 DOF"]
  B --> C["Datum C - 1 point -> -1 DOF"]
  C --> DRF["Fully constrained DRF (0 DOF)"]
```

Order matters: the **primary** datum is most functionally important and contacts
first; reversing the order changes how the part seats and therefore the measured
results. Datums are how a measurement made anywhere reproduces the design intent.

```plot
{"title": "Degrees of freedom remaining as datums are applied (3-2-1)", "xLabel": "datums applied", "yLabel": "DOF remaining", "xRange": [0, 3], "yRange": [0, 6], "grid": true, "functions": [{"expr": "6 - (3*x - (x>1)*0)", "label": "constrained progression", "color": "#2563eb"}]}
```

**Next:** material condition modifiers and the bonus tolerance they unlock.
""",
        ),
        _t(
            "Material condition modifiers and bonus tolerance",
            "12 min",
            r"""
# Material condition modifiers and bonus tolerance

GD&T lets a tolerance depend on a feature's actual size through **material
condition modifiers**. **MMC** (maximum material condition, the M-in-circle) is
the size with the most material — the largest shaft, the smallest hole. **LMC**
is the opposite. **RFS** (regardless of feature size) applies the stated
tolerance at every size.

When position is specified **at MMC**, departing from MMC frees up **bonus
tolerance**: as a hole grows beyond its smallest size, the extra clearance is
added to the geometric tolerance.

$$t_{\text{total}} = t_{\text{geom}} + |D_{\text{actual}} - D_{\text{MMC}}|.$$

For a hole, MMC is the smallest hole, so a larger actual hole earns bonus:

```plot
{"title": "Bonus tolerance: total position tolerance vs hole size (MMC basis)", "xLabel": "actual hole diameter (mm)", "yLabel": "total position tolerance (mm)", "xRange": [10, 10.5], "yRange": [0, 0.8], "grid": true, "functions": [{"expr": "0.2 + (x - 10.0)", "label": "0.2 geom + bonus", "color": "#16a34a"}]}
```

```python
def total_position_tolerance(actual, mmc_size, geom_tol):
    bonus = abs(actual - mmc_size)      # departure from MMC
    return geom_tol + bonus

# Hole MMC = 10.00, geometric position tol 0.20 at MMC
print(round(total_position_tolerance(10.00, 10.00, 0.20), 3))  # 0.200 (no bonus)
print(round(total_position_tolerance(10.30, 10.00, 0.20), 3))  # 0.500 (0.30 bonus)
```

Bonus tolerance is "free" yield: it accepts more parts without compromising
function, because a bigger hole inherently has more clearance for the fastener.

```mermaid
flowchart LR
  MMC["Feature at MMC"] -->|"no departure"| T0["tolerance = geometric"]
  GROW["Hole grows toward LMC"] -->|"departure d"| TB["tolerance = geometric + d (bonus)"]
```

**Next:** combining all dimensions into a tolerance stack-up analysis.
""",
        ),
        _t(
            "Tolerance stack-up analysis",
            "12 min",
            r"""
# Tolerance stack-up analysis

A **stack-up** predicts whether an assembly's accumulated variation keeps a
critical gap or fit within spec. Two methods bracket reality.

**Worst-case (WC):** assume every part simultaneously at its worst limit. For a
chain of dimensions the gap tolerance is the *sum* of part tolerances:

$$T_{\text{WC}} = \sum_{i=1}^{n} t_i.$$

Safe but pessimistic — it guarantees 100% interchangeability at the cost of tight,
expensive tolerances.

**Statistical (RSS):** since independent variations rarely peak together, combine
them as a **root-sum-square**:

$$T_{\text{RSS}} = \sqrt{\sum_{i=1}^{n} t_i^{2}}.$$

For $n$ equal tolerances $t$, $T_{\text{WC}} = n\,t$ but $T_{\text{RSS}} =
t\sqrt n$ — the statistical stack grows only with $\sqrt n$, allowing looser,
cheaper part tolerances at a small, quantified reject risk.

```plot
{"title": "Stack-up tolerance vs number of parts (equal tolerances)", "xLabel": "number of parts n", "yLabel": "assembly tolerance (relative)", "xRange": [1, 10], "yRange": [0, 10], "grid": true, "functions": [{"expr": "x", "label": "worst-case (sum)", "color": "#dc2626"}, {"expr": "sqrt(x)", "label": "RSS (statistical)", "color": "#16a34a"}]}
```

```python
import numpy as np

tols = np.array([0.1, 0.1, 0.05, 0.05, 0.1])   # +/- tolerances (mm)
worst_case = tols.sum()                          # 0.40
rss        = np.sqrt((tols**2).sum())            # 0.187
print(round(worst_case, 3), round(rss, 3))       # 0.4 0.187
```

Use WC for safety-critical, low-volume assemblies; use RSS (or Monte Carlo
sampling) for high-volume production where a defined ppm reject rate is
acceptable.

**Next:** check your understanding of fits, GD&T and stack-ups.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Graphics, GD&T & CAD — Advanced ──────────────────────────────

_ADVANCED = SeedCourse(
    slug="engineering-graphics-cad-advanced",
    title="Engineering Graphics, GD&T & CAD — Advanced",
    description=(
        "State-of-the-art CAD practice. Parametric feature-based solid modelling "
        "and design intent, assembly mates and degrees of freedom, the boundary "
        "representation and NURBS math behind the kernel, model-based definition, "
        "and CAD automation with generative/topology optimization. Worked code in "
        "Python and MATLAB."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Parametric feature-based solid modelling",
            "12 min",
            r"""
# Parametric feature-based solid modelling

Modern CAD (SOLIDWORKS, Creo, NX, CATIA, Fusion 360, Onshape) is **parametric**
and **feature-based**. A model is a *history tree* of features — extrude, revolve,
fillet, pattern — each driven by **dimensions and constraints (parameters)**.
Change a parameter and the model **regenerates**: design intent is captured, not
just final geometry.

The base is a **2D sketch** governed by geometric constraints (coincident,
parallel, tangent) and dimensional ones. A sketch is **fully defined** when its
degrees of freedom reach zero:

$$\text{DOF} = 2 N_{\text{points}} - N_{\text{constraints}} = 0.$$

Under-constrained sketches drag unpredictably; over-constrained ones throw
conflicts.

```mermaid
flowchart LR
  S["2D Sketch + constraints"] --> F1["Extrude (base feature)"]
  F1 --> F2["Cut / Revolve"]
  F2 --> F3["Fillet / Chamfer"]
  F3 --> F4["Pattern / Mirror"]
  F4 --> SOLID["Solid body"]
  P["Parameters d1, d2, ..."] -.->|"drive"| F1
  P -.->|"edit -> regenerate"| SOLID
```

```python
# A toy parametric model: volume of a flanged boss regenerates from parameters
import numpy as np

def boss_volume(d_outer, d_bore, height):
    r_o, r_i = d_outer / 2, d_bore / 2
    return np.pi * (r_o**2 - r_i**2) * height   # mm^3

print(round(boss_volume(40, 20, 30), 1))   # 28274.3
print(round(boss_volume(50, 20, 30), 1))   # edit d_outer -> regenerates: 49480.1
```

Good design intent means edits propagate sensibly — fully defined sketches,
meaningful feature order, references to stable geometry rather than fragile edges.

**Next:** assembling parts with mates and tracking assembly degrees of freedom.
""",
        ),
        _t(
            "Assemblies, mates and degrees of freedom",
            "12 min",
            r"""
# Assemblies, mates and degrees of freedom

An **assembly** positions component instances with **mates** (SOLIDWORKS) or
**constraints** (Creo/NX): coincident, concentric, parallel, distance, angle.
Each rigid body starts with **6 DOF**; every mate removes some. A fully
constrained component has 0 DOF; a mechanism deliberately leaves DOF to allow
motion.

The **Gruebler / Kutzbach** mobility equation predicts a planar mechanism's
degrees of freedom from links and joints:

$$M = 3(n - 1) - 2 j_1 - j_2,$$

where $n$ is links (including ground), $j_1$ lower (1-DOF) pairs, $j_2$ higher
(2-DOF) pairs. A four-bar linkage: $n=4$, $j_1=4$, $j_2=0 \Rightarrow M = 3(3) -
8 = 1$ — one input drives it.

```plot
{"title": "Planar mechanism mobility M vs number of 1-DOF joints (n=4 links)", "xLabel": "number of lower pairs j1", "yLabel": "mobility M", "xRange": [2, 6], "yRange": [-3, 4], "grid": true, "functions": [{"expr": "9 - 2*x", "label": "M = 3(n-1) - 2 j1", "color": "#2563eb"}]}
```

```python
def kutzbach(n_links, j1_lower, j2_higher=0):
    return 3 * (n_links - 1) - 2 * j1_lower - j2_higher

print(kutzbach(4, 4))   # 1  -> four-bar linkage (1 DOF)
print(kutzbach(6, 7))   # 1  -> six-bar linkage
print(kutzbach(3, 3))   # 0  -> rigid structure (a triangle)
```

```mermaid
flowchart LR
  C["Component - 6 DOF"] --> M1["Concentric -> remove 4"]
  M1 --> M2["Coincident face -> remove 1"]
  M2 --> M3["Parallel/angle -> remove last"]
  M3 --> FIX["Fully constrained - 0 DOF"]
```

Over-defining mates creates conflicts; under-defining leaves parts free to drift.

**Next:** the geometric kernel — B-rep and the NURBS math beneath the surfaces.
""",
        ),
        _t(
            "The geometric kernel: B-rep and NURBS",
            "13 min",
            r"""
# The geometric kernel: B-rep and NURBS

Beneath the UI, a **geometric kernel** (Parasolid, ACIS, Open CASCADE) stores
solids as a **boundary representation (B-rep)**: a graph of *topology* (vertices,
edges, faces, shells) bound to *geometry* (points, curves, surfaces). A valid
solid satisfies **Euler's formula** for a simple polyhedron:

$$V - E + F = 2,$$

generalized for handles/holes as $V - E + F = 2(1 - g)$ with genus $g$. Kernels
check this and orientation to keep a body "watertight".

Free-form curves and surfaces are **NURBS** (Non-Uniform Rational B-Splines). A
NURBS curve is a weighted blend of control points $P_i$ via basis functions
$N_{i,p}$:

$$C(u) = \frac{\sum_{i=0}^{n} N_{i,p}(u)\, w_i\, P_i}{\sum_{i=0}^{n} N_{i,p}(u)\, w_i}.$$

Weights $w_i$ let NURBS represent conics (circles, ellipses) exactly — impossible
with plain polynomials — which is why they are the CAD standard.

```python
import numpy as np
from scipy.interpolate import BSpline

# Cubic B-spline curve from a control polygon
ctrl = np.array([[0, 0], [1, 2], [3, 3], [4, 0], [6, 1]])
p = 3
n = len(ctrl)
knots = np.concatenate(([0]*(p+1), np.arange(1, n-p), [n-p]*(p+1)))
u = np.linspace(0, n - p, 50)
curve = np.array([BSpline(knots, ctrl[:, d], p)(u) for d in range(2)]).T
print(curve.shape)   # (50, 2) -> sampled smooth curve
```

```plot
{"title": "B-spline basis weighting -> smooth blend (Gaussian-like influence)", "xLabel": "parameter u", "yLabel": "basis function value", "xRange": [0, 6], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-(x-3)^2)", "label": "control-point influence", "color": "#2563eb"}]}
```

```mermaid
flowchart TB
  K["Geometric kernel"] --> TOPO["Topology: V, E, F, shells (B-rep graph)"]
  K --> GEOM["Geometry: points, NURBS curves & surfaces"]
  TOPO --> VALID["Euler check V - E + F = 2(1-g)"]
  GEOM --> EXACT["NURBS weights -> exact conics"]
```

**Next:** putting the definition on the model itself with MBD and PMI.
""",
        ),
        _t(
            "Model-based definition and PMI",
            "11 min",
            r"""
# Model-based definition and PMI

**Model-Based Definition (MBD)** makes the **3D model the authoritative source**
of design data — dimensions, GD&T, notes and materials live *on the model* as
**Product and Manufacturing Information (PMI)**, governed by ASME Y14.41 and
ISO 16792. The 2D drawing becomes optional; downstream CAM, CMM and inspection
consume the model directly.

Benefits compound through the digital thread: a single source of truth removes
drawing/model mismatches, machine-readable **semantic PMI** drives automated
inspection and toolpaths, and exchange happens via neutral formats — **STEP
AP242** (which carries semantic PMI), **3D PDF**, **JT** and **QIF** for quality
data.

```mermaid
flowchart LR
  MBD["3D model + semantic PMI"] --> CAM["CAM toolpaths"]
  MBD --> CMM["CMM / inspection"]
  MBD --> SUP["Supplier (STEP AP242 / 3D PDF)"]
  MBD --> QIF["QIF quality data exchange"]
  MBD --> PLM["PLM digital thread"]
```

Maturity matters: **presentation** PMI is human-readable annotation only;
**representation (semantic)** PMI is machine-interpretable, linked to the faces it
controls, and is what unlocks automation. Adoption reduces interpretation errors
and cycle time, with returns rising as more downstream consumers read the model
directly:

```plot
{"title": "Rework cost vs MBD/semantic-PMI adoption maturity", "xLabel": "MBD adoption maturity", "yLabel": "relative rework cost", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "rework cost decay", "color": "#16a34a"}]}
```

**Next:** automating CAD and letting algorithms generate optimal geometry.
""",
        ),
        _t(
            "CAD automation and generative design",
            "13 min",
            r"""
# CAD automation and generative design

CAD systems expose **APIs** (SOLIDWORKS API, NX Open, Onshape REST/FeatureScript,
pythonOCC) to script repetitive work — configuration tables, drawing generation,
**design automation**. A parametric model plus a script becomes a *design
generator* that produces a family of parts from a spec.

**Generative design** and **topology optimization** invert the workflow: instead
of drawing geometry then checking it, you state loads, supports and a target, and
the algorithm *computes* the optimal material layout. The classic **SIMP**
(Solid Isotropic Material with Penalization) method assigns each element a density
$\rho_e \in [0,1]$ and minimizes compliance (maximizes stiffness) subject to a
volume fraction:

$$\min_{\rho}\; C(\rho)=\mathbf{U}^{\top}\mathbf{K}(\rho)\,\mathbf{U}
\quad \text{s.t.}\quad \frac{V(\rho)}{V_0}\le f,\;\; 0<\rho_{\min}\le\rho_e\le 1,$$

with element stiffness penalized as $E_e = E_{\min} + \rho_e^{\,p}(E_0-E_{\min})$,
$p \approx 3$, to push densities toward solid/void. Solved by iterative FE +
sensitivity analysis, compliance converges over the iterations:

```plot
{"title": "Topology optimization: compliance vs iteration (convergence)", "xLabel": "iteration", "yLabel": "normalized compliance", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "compliance convergence", "color": "#dc2626"}]}
```

```python
import numpy as np

# One SIMP optimality-criteria density update step (bisection on Lagrange mult.)
def oc_update(x, dc, volfrac, move=0.2):
    l1, l2 = 0.0, 1e9
    while (l2 - l1) / (l1 + l2 + 1e-9) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        xnew = np.clip(x * np.sqrt(-dc / lmid), x - move, x + move)
        xnew = np.clip(xnew, 1e-3, 1.0)
        if xnew.mean() > volfrac:   # too much material -> raise multiplier
            l1 = lmid
        else:
            l2 = lmid
    return xnew

x = np.full(20, 0.4)            # initial densities
dc = -np.linspace(1, 2, 20)    # (toy) compliance sensitivities
print(round(oc_update(x, dc, 0.4).mean(), 3))  # ~0.4 volume fraction held
```

```mermaid
flowchart LR
  SPEC["Loads + supports + volume target"] --> FE["FE solve -> compliance"]
  FE --> SENS["Sensitivity dC/drho"]
  SENS --> UPD["OC / MMA density update"]
  UPD --> FILT["Filter (mesh independence)"]
  FILT -->|"not converged"| FE
  FILT -->|"converged"| GEN["Optimized geometry -> smooth -> CAD"]
```

ML-driven generative tools (Fusion 360 Generative Design, nTop) and surrogate
models now explore thousands of manufacturable candidates against cost, weight
and process constraints.

**Next:** check your understanding of parametric modelling, kernels and generative design.
""",
        ),
        _quiz(),
    ),
)


ENGINEERING_GRAPHICS_CAD_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ENGINEERING_GRAPHICS_CAD_COURSES"]
