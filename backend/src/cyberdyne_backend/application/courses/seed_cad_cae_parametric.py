"""Parametric & Simulation-Driven Design track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on building models that change with
their parameters and that close the loop with simulation. From sketch
constraints and feature trees, through design tables, configurations and
associativity, to CAD-CAE integration, design-of-experiments, surrogate models
and optimization-driven (generative) design. Lessons are `text` with LaTeX,
interactive ```plot blocks, ```mermaid workflow diagrams and runnable
```python / ```matlab code.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Parametric & Simulation-Driven Design — Basics ───────────────────────────

_BASICS = SeedCourse(
    slug="cad-cae-parametric-basics",
    title="Parametric & Simulation-Driven Design — Basics",
    description=(
        "The intuition behind parametric CAD. Learn what a parameter and a "
        "constraint are, how geometric and dimensional constraints fully define a "
        "sketch, how a feature tree captures design intent, and why a model that "
        "regenerates from a few driving dimensions beats redrawing geometry. "
        "Interactive plots and workflow diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is parametric design?",
            "10 min",
            r"""
# What is parametric design?

**Parametric design** means the geometry is not drawn once and frozen — it is
*defined by parameters* (named dimensions and relations) so that changing a
number regenerates the whole model. A bracket whose hole spacing is driven by a
variable `pitch` updates everywhere the instant you edit `pitch`. The model
captures *design intent*, not just a final shape.

Contrast this with **direct (explicit) modelling**, where you push and pull
geometry that has no history. Direct editing is fast for one-off tweaks;
parametric modelling pays off when a design must be revised many times or
re-used as a family of variants.

The value grows with the number of revisions: redrawing costs scale with each
change, while a parametric edit is nearly free once the model is built.

```plot
{"title": "Effort vs number of design revisions: redraw vs parametric edit", "xLabel": "number of revisions", "yLabel": "cumulative effort (relative)", "xRange": [0, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.2*x", "label": "redraw each time", "color": "#dc2626"}, {"expr": "2 + 0.1*x", "label": "build once + parametric edits", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  P["Parameters - pitch, dia, thickness"] -->|"drive"| M["Model definition"]
  M --> G["Generated geometry"]
  EDIT["Edit a parameter"] -->|"regenerate"| G
  G --> V["Variant / family"]
```

Modern tools — SOLIDWORKS, Creo, NX, CATIA, Fusion 360, Onshape — are all
parametric at heart, with optional direct-edit modes.

**Next:** the constraints that make a sketch behave predictably.
""",
        ),
        _t(
            "Sketch constraints and degrees of freedom",
            "11 min",
            r"""
# Sketch constraints and degrees of freedom

A 2D sketch is a set of points and curves with **degrees of freedom (DOF)**.
Each point has two DOF ($x, y$), so a sketch of $N$ points starts with $2N$ DOF.
**Constraints** remove DOF until the sketch is **fully defined** (zero DOF) — it
can no longer be dragged into a different shape.

Two families of constraint:

- **Geometric** — coincident, horizontal, vertical, parallel, perpendicular,
  tangent, concentric, equal, symmetric. They relate entities to each other.
- **Dimensional** — lengths, radii, angles. They pin numeric values and become
  the *parameters* you later edit.

A sketch reaches zero DOF when constraints balance the freedoms:

$$\text{DOF} = 2 N_{\text{points}} - N_{\text{constraints}} = 0.$$

```plot
{"title": "Sketch degrees of freedom as constraints are added", "xLabel": "constraints applied", "yLabel": "remaining DOF", "xRange": [0, 8], "yRange": [0, 8], "grid": true, "functions": [{"expr": "8 - x", "label": "DOF = 2N - constraints", "color": "#2563eb"}]}
```

```mermaid
flowchart TB
  S["Sketch entities - 2N DOF"] --> GC["Geometric constraints"]
  S --> DC["Dimensional constraints"]
  GC --> FD{"DOF = 0 ?"}
  DC --> FD
  FD -->|"yes"| FULL["Fully defined - stable"]
  FD -->|"no, > 0"| UNDER["Under-defined - drags freely"]
  FD -->|"no, conflict"| OVER["Over-defined - error"]
```

An **under-defined** sketch (DOF > 0) shifts unpredictably when neighbouring
geometry changes; an **over-defined** sketch throws a conflict. Aim for exactly
zero — fully defined, no redundant constraints.

**Next:** stacking features into a history tree that remembers your intent.
""",
        ),
        _t(
            "Features and the design tree",
            "11 min",
            r"""
# Features and the design tree

A solid is built from **features** applied in order: a base **extrude** or
**revolve**, then **cut**, **fillet**, **chamfer**, **shell**, **hole**,
**pattern** and **mirror**. Each feature references earlier geometry and is
recorded in the **feature (history) tree**. Editing a feature and pressing
*regenerate* replays the tree from that point downward.

The tree *is* the design intent. The order matters: a fillet placed before a
pattern is repeated by the pattern; placed after, it is not. References should
point at stable geometry (origin planes, named features) rather than fragile
edges that vanish when an upstream feature changes — the cause of the dreaded
**rebuild error**.

```mermaid
flowchart LR
  SK["Sketch + constraints"] --> EX["Extrude - base"]
  EX --> CUT["Cut - pocket"]
  CUT --> HOLE["Hole feature"]
  HOLE --> FIL["Fillet"]
  FIL --> PAT["Pattern"]
  PAT --> BODY["Solid body"]
  PARAM["Parameters"] -.->|"drive + regenerate"| BODY
```

A parameter edit propagates down the tree; the model recomputes a new solid. A
simple parametric volume regenerates from its driving dimensions:

```python
import numpy as np

def plate_volume(length, width, thickness, hole_dia, n_holes):
    gross = length * width * thickness
    holes = n_holes * np.pi * (hole_dia / 2) ** 2 * thickness
    return gross - holes          # mm^3

print(round(plate_volume(120, 60, 8, 10, 4), 1))   # 55089.4
print(round(plate_volume(150, 60, 8, 10, 4), 1))   # edit length -> regenerates
```

**Next:** why a fully defined, well-ordered model is robust to change.
""",
        ),
        _t(
            "Design intent and robust models",
            "10 min",
            r"""
# Design intent and robust models

**Design intent** is the set of rules you want the model to obey as it changes:
"these holes stay centred", "the wall is always 2 mm", "the boss tracks the
flange". You encode intent through constraints, smart references, symmetry and
relations — so the *right* things move and the *right* things stay put when a
parameter changes.

A robust model is fully defined, references stable geometry, uses meaningful
feature order, and avoids brittle dependencies. Robustness pays off as the
number of downstream edits grows: brittle models accumulate rebuild errors,
while robust ones absorb change with near-zero rework.

```plot
{"title": "Rework cost vs design-intent quality", "xLabel": "design-intent quality (0-10)", "yLabel": "rework per change (relative)", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "rework decay", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  INTENT["Design intent"] --> FD["Fully defined sketches"]
  INTENT --> REF["Stable references - planes, origins"]
  INTENT --> SYM["Symmetry + relations"]
  INTENT --> ORD["Sensible feature order"]
  FD --> ROBUST["Robust, editable model"]
  REF --> ROBUST
  SYM --> ROBUST
  ORD --> ROBUST
```

A quick test: change a key dimension and regenerate. If the model updates as you
expected with no errors, the intent is captured. If geometry collapses or
features fail, the dependencies were fragile.

**Next:** linking dimensions to each other with equations and relations.
""",
        ),
        _t(
            "Relations, equations and units",
            "11 min",
            r"""
# Relations, equations and units

Beyond pinning numbers, you can link dimensions with **equations** so one value
is computed from others. A global variable `wall = 2` and a relation
`pocket_depth = thickness - wall` mean the pocket floor tracks the wall as the
plate thickness changes. Equations turn a model into a small program.

Relations also enforce **engineering rules**: keep a fillet a fraction of a
thickness, hold a fastener clearance, or derive a bolt-circle radius from a
diameter. A driven dimension that is, say, 60% of a width changes whenever the
width does:

```plot
{"title": "Driven dimension from an equation (height = 0.6 * width)", "xLabel": "width (mm)", "yLabel": "driven height (mm)", "xRange": [0, 100], "yRange": [0, 70], "grid": true, "functions": [{"expr": "0.6*x", "label": "height = 0.6 * width", "color": "#2563eb"}]}
```

```python
# Global variables + relations evaluated in order (like a CAD equation set)
params = {"width": 80.0, "wall": 2.0, "thickness": 10.0}
params["height"]       = 0.6 * params["width"]          # relation
params["pocket_depth"] = params["thickness"] - params["wall"]
params["bolt_radius"]  = 0.5 * params["width"] - 8.0
print({k: round(v, 2) for k, v in params.items()})
```

Mind **units**: a model has a unit system (mm, inch) and equations must be
dimensionally consistent. Mixing units silently is a classic source of error —
keep a single system and treat angles in degrees or radians consistently.

```mermaid
flowchart LR
  GV["Global variables"] --> EQ["Equations / relations"]
  EQ --> DD["Driven dimensions"]
  DD --> MODEL["Model regenerates"]
  RULE["Engineering rule"] -.->|"encoded as"| EQ
```

**Next:** documenting and exchanging a parametric model.
""",
        ),
        _t(
            "Documenting and exchanging models",
            "10 min",
            r"""
# Documenting and exchanging models

A parametric model is only useful if others can read and re-use it. Two layers
matter: **internal documentation** (clear feature names, organized parameter
sets, comments on relations) and **external exchange** (the file formats that
move geometry between tools).

Native files (`.sldprt`, `.prt`, `.CATPart`) keep the full history and
parameters but are tool-specific. **Neutral formats** trade history for
portability:

- **STEP (ISO 10303, AP242)** — solid B-rep + optional semantic PMI; the
  workhorse for CAD-to-CAD and CAD-to-CAE exchange.
- **IGES** — older surface/curve exchange, largely superseded by STEP.
- **STL / 3MF** — tessellated mesh for 3D printing (loses exact geometry).
- **Parasolid (.x_t)** — kernel-level B-rep, common between kernel-sharing tools.

```mermaid
flowchart LR
  NAT["Native model - full history + params"] --> STEP["STEP AP242 - B-rep + PMI"]
  NAT --> STL["STL / 3MF - mesh for printing"]
  NAT --> XT["Parasolid .x_t - kernel B-rep"]
  STEP --> CAE["CAE / FEA tools"]
  STEP --> CAM["CAM / machining"]
  STL --> AM["Additive manufacturing"]
```

Exporting to a mesh discards parametrics and approximates curves with facets;
finer tessellation lowers the chordal deviation but inflates file size, so you
trade accuracy against weight:

```plot
{"title": "STL chordal (faceting) error vs facet count", "xLabel": "facet count (thousands)", "yLabel": "chordal deviation (mm)", "xRange": [1, 50], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/sqrt(x)", "label": "deviation ~ 1/sqrt(facets)", "color": "#dc2626"}]}
```

Prefer STEP for engineering hand-off; reserve mesh formats for fabrication.

**Next:** check your understanding of parametric fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Parametric & Simulation-Driven Design — Intermediate ─────────────────────

_INTERMEDIATE = SeedCourse(
    slug="cad-cae-parametric-intermediate",
    title="Parametric & Simulation-Driven Design — Intermediate",
    description=(
        "The quantitative core of model management. Covers design tables and "
        "configurations for part families, top-down assembly modelling with "
        "skeletons, associativity and external references, in-context and "
        "equation-driven curves, and the basics of meshing and a first CAD-CAE "
        "handoff. Worked examples with plots, diagrams and Python."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Design tables and part families",
            "12 min",
            r"""
# Design tables and part families

A **design table** drives a part's parameters from a spreadsheet: each row is a
**configuration** (a member of a part family), each column a dimension or
suppression state. One model then represents a whole catalogue — a family of
bolts, gears, or housings — generated by reading rows.

This is how standard-component libraries scale: instead of 40 hand-built bolt
models you keep one parametric model and a 40-row table. The number of
configurations a single model can serve grows combinatorially with the number of
independent parameters, which is exactly why tables are powerful.

```plot
{"title": "Configurations from independent 2-value parameters", "xLabel": "number of parameters", "yLabel": "possible configurations", "xRange": [0, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "2^x", "label": "configs = 2^params", "color": "#2563eb"}]}
```

```python
import itertools

# A tiny design table generator: family of flanges from a parameter grid
params = {
    "bore":      [20, 25, 30],     # mm
    "pcd":       [60, 70],         # pitch-circle diameter
    "thickness": [8, 10],          # mm
}
rows = list(itertools.product(*params.values()))
table = [dict(zip(params.keys(), r)) for r in rows]
print(len(table))      # 12 configurations
print(table[0])        # {'bore': 20, 'pcd': 60, 'thickness': 8}
```

```mermaid
flowchart LR
  MODEL["One parametric model"] --> DT["Design table (rows = configs)"]
  DT --> C1["Config A"]
  DT --> C2["Config B"]
  DT --> C3["Config ..."]
  C1 --> BOM["Family / catalogue"]
  C2 --> BOM
  C3 --> BOM
```

Tables can also **suppress** features per row, so a configuration can drop a hole
or a boss entirely — variation in topology, not just dimensions.

**Next:** configurations and how they manage variation within one document.
""",
        ),
        _t(
            "Configurations and variation management",
            "11 min",
            r"""
# Configurations and variation management

A **configuration** is a saved state of a model — a set of dimension values,
suppression states and properties — stored inside one document. Configurations
manage *intentional* variation: machined-vs-cast versions, simplified
representations for large assemblies, or stages of a process.

The engineering payoff is **reuse**: parts that share 90% of their definition
should share one model. But configurations add management cost — too many, and
the document becomes hard to maintain. There is a sweet spot between *too many
separate files* and *too many configurations crammed in one file*.

```plot
{"title": "Maintenance cost vs configurations per model", "xLabel": "configurations in one document", "yLabel": "relative maintenance cost", "xRange": [1, 30], "yRange": [0, 5], "grid": true, "functions": [{"expr": "3/x + 0.12*x", "label": "total cost (reuse vs bloat)", "color": "#dc2626"}]}
```

The cost curve has a minimum: few configs waste reuse, many configs bloat the
file. Differentiating $3/x + 0.12x$ and setting it to zero gives the optimum
near $x = \sqrt{3/0.12} \approx 5$ configurations.

```python
import numpy as np

def maintenance_cost(n, reuse=3.0, bloat=0.12):
    return reuse / n + bloat * n

n = np.arange(1, 16)
best = n[np.argmin(maintenance_cost(n))]
print(best)    # ~5 configurations minimizes the toy cost model
```

```mermaid
flowchart TB
  MODEL["Single document"] --> CFG["Configurations"]
  CFG --> MACH["Machined variant"]
  CFG --> CAST["Cast variant"]
  CFG --> SIMP["Simplified - large-assembly rep"]
  CFG --> PROC["In-process stage"]
```

**Next:** building assemblies from the top down with a controlling skeleton.
""",
        ),
        _t(
            "Top-down assembly and skeletons",
            "12 min",
            r"""
# Top-down assembly and skeletons

In **bottom-up** assembly you model parts independently and mate them together.
In **top-down** assembly you start from the assembly: a **skeleton** (layout
sketch, master model, or set of reference geometry) holds the controlling
dimensions, and individual parts reference it. Change the skeleton and every part
updates — a single source of truth for shared interfaces.

Skeletons shine when many parts share an interface: a mounting pattern, an
envelope, a kinematic layout. The cost of a global change drops sharply because
edits happen once in the skeleton instead of $n$ times across $n$ parts.

```plot
{"title": "Edits to change a shared interface: bottom-up vs skeleton-driven", "xLabel": "parts sharing the interface", "yLabel": "manual edits required", "xRange": [1, 12], "yRange": [0, 12], "grid": true, "functions": [{"expr": "x", "label": "bottom-up (edit each part)", "color": "#dc2626"}, {"expr": "1", "label": "skeleton (edit once)", "color": "#16a34a"}]}
```

```mermaid
flowchart TB
  SKEL["Skeleton / master model"] --> P1["Part A references skeleton"]
  SKEL --> P2["Part B references skeleton"]
  SKEL --> P3["Part C references skeleton"]
  EDIT["Edit skeleton layout"] -->|"propagates"| P1
  EDIT --> P2
  EDIT --> P3
```

```python
# Skeleton-driven layout: parts read shared interface dimensions
skeleton = {"mount_pitch": 100.0, "envelope_h": 250.0, "shaft_axis_z": 60.0}

def bracket(skel):                      # part derives geometry from skeleton
    return {"hole_spacing": skel["mount_pitch"],
            "height":       skel["envelope_h"] - 30.0}

print(bracket(skeleton))                # {'hole_spacing': 100.0, 'height': 220.0}
skeleton["mount_pitch"] = 120.0         # one edit...
print(bracket(skeleton))                # ...updates the part
```

**Next:** the associativity that keeps drawings, parts and assemblies in sync.
""",
        ),
        _t(
            "Associativity and external references",
            "11 min",
            r"""
# Associativity and external references

**Associativity** is the live link between related documents: a drawing updates
when its part changes; an assembly updates when a component changes; an
**in-context** feature updates when the geometry it references moves. This keeps
a project consistent without manual re-syncing.

The flip side is the **external reference** — a dependency from one document on
another. References form a directed graph; a change ripples through it. Useful,
but uncontrolled in-context references create fragile webs and **circular
dependencies** (A drives B drives A), which break regeneration.

```mermaid
flowchart LR
  PART["Part"] -->|"associative"| DRW["Drawing"]
  PART -->|"in assembly"| ASM["Assembly"]
  ASM -->|"in-context ref"| PART2["Mating part"]
  SKEL["Skeleton"] -->|"controls"| PART
  PART2 -.->|"avoid: circular ref"| SKEL
```

Reference depth governs rebuild cost: the more layers a change must propagate
through, the longer a full rebuild takes, roughly linearly with chain length:

```plot
{"title": "Rebuild time vs reference-chain depth", "xLabel": "reference chain depth", "yLabel": "rebuild time (relative)", "xRange": [1, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1 + 1.1*x", "label": "rebuild ~ linear in depth", "color": "#2563eb"}]}
```

```python
# Detect a circular external reference before it breaks the rebuild
graph = {"drawing": ["part"], "part": ["skeleton"], "skeleton": ["part"]}

def has_cycle(g):
    seen, stack = set(), set()
    def dfs(node):
        seen.add(node); stack.add(node)
        for nxt in g.get(node, []):
            if nxt in stack or (nxt not in seen and dfs(nxt)):
                return True
        stack.discard(node); return False
    return any(dfs(n) for n in g if n not in seen)

print(has_cycle(graph))   # True -> circular reference, fix it
```

Best practice: drive shared geometry from a skeleton, keep references shallow and
one-directional, and break in-context links once the design stabilizes.

**Next:** driving geometry with equations and mathematically defined curves.
""",
        ),
        _t(
            "Equation-driven and in-context geometry",
            "11 min",
            r"""
# Equation-driven and in-context geometry

Many CAD tools accept **equation-driven curves**: a profile defined by an
explicit $y=f(x)$ or a parametric pair $x(t), y(t)$. This is how you model a cam
profile, a turbine-blade camber line, an Archimedean spiral or an involute gear
tooth precisely rather than approximating with arcs.

For example, an **involute** — the standard gear-tooth flank — is the parametric
curve traced by unwinding a string from a base circle of radius $r_b$:

$$x(t) = r_b\,(\cos t + t\,\sin t), \qquad y(t) = r_b\,(\sin t - t\,\cos t).$$

A simple sinusoidal cam-displacement profile (rise as a smooth function of angle)
shows the idea of geometry from an equation:

```plot
{"title": "Equation-driven cam displacement vs cam angle", "xLabel": "cam angle (rad)", "yLabel": "follower lift (mm)", "xRange": [0, 6.28], "yRange": [0, 20], "grid": true, "functions": [{"expr": "10*(1 - cos(x))", "label": "lift = 10(1 - cos theta)", "color": "#2563eb"}]}
```

```python
import numpy as np

# Sample an involute tooth flank, then export points to drive a CAD spline
r_b = 20.0                              # base-circle radius (mm)
t = np.linspace(0, 1.2, 30)            # roll angle (rad)
x = r_b * (np.cos(t) + t * np.sin(t))
y = r_b * (np.sin(t) - t * np.cos(t))
pts = np.column_stack([x, y])
print(pts.shape, pts[0].round(2))      # (30, 2) [20. 0.]
```

**In-context** geometry is the assembly-level twin: a feature on one part is
sketched against the live geometry of a neighbour (a gasket that follows a flange
face). It guarantees fit but creates an external reference, so use it
deliberately and break the link once the interface is frozen.

```mermaid
flowchart LR
  EQ["Equation y=f(x) or x(t),y(t)"] --> CURVE["Exact curve - cam, involute, spiral"]
  CURVE --> FEAT["Feature - extrude / sweep"]
  CTX["Neighbour geometry"] -.->|"in-context ref"| FEAT
```

**Next:** turning a CAD model into a mesh a solver can use.
""",
        ),
        _t(
            "Meshing and the first CAD-CAE handoff",
            "12 min",
            r"""
# Meshing and the first CAD-CAE handoff

To simulate, the continuous CAD geometry is discretized into a **mesh** of finite
elements. The solver computes approximate fields (stress, temperature, flow) at
nodes and interpolates between them. **Mesh quality** and **density** control
accuracy: too coarse and the answer is wrong; too fine and the solve is slow.

The hallmark of a trustworthy simulation is a **mesh-convergence study**: refine
the mesh and watch the result approach a limit. Finer meshes reduce
discretization error, typically as a power of element size $h$, so the computed
peak stress converges toward the true value:

$$\text{error} \approx C\,h^{p}, \quad p \ge 1 \;\;\text{for well-formed elements.}$$

```plot
{"title": "Mesh convergence: computed peak stress vs element count", "xLabel": "elements (thousands)", "yLabel": "peak stress (MPa)", "xRange": [1, 40], "yRange": [80, 130], "grid": true, "functions": [{"expr": "120 - 40/sqrt(x)", "label": "converges to ~120 MPa", "color": "#16a34a"}]}
```

```python
import numpy as np

# Richardson-style convergence check on three mesh refinements
h     = np.array([4.0, 2.0, 1.0])         # element size (mm)
sigma = np.array([101.0, 114.0, 119.0])   # peak stress (MPa)

# observed order p from successive halvings
p = np.log((sigma[1]-sigma[0])/(sigma[2]-sigma[1])) / np.log(2)
extrap = sigma[2] + (sigma[2]-sigma[1])/(2**p - 1)   # Richardson extrapolation
print(round(p, 2), round(extrap, 1))      # ~1.38 ~120.6 MPa (mesh-independent)
```

```mermaid
flowchart LR
  CAD["CAD geometry"] --> CLEAN["Defeature - remove tiny fillets/holes"]
  CLEAN --> MESH["Mesh - element type + size"]
  MESH --> BC["Loads + boundary conditions"]
  BC --> SOLVE["Solve"]
  SOLVE --> CONV{"Converged?"}
  CONV -->|"no"| MESH
  CONV -->|"yes"| POST["Post-process results"]
```

**Defeaturing** (removing tiny fillets, logos, fasteners) before meshing avoids
sliver elements and slashes element count without changing the physics that
matters.

**Next:** check your understanding of tables, assemblies and meshing.
""",
        ),
        _quiz(),
    ),
)


# ── Parametric & Simulation-Driven Design — Advanced ─────────────────────────

_ADVANCED = SeedCourse(
    slug="cad-cae-parametric-advanced",
    title="Parametric & Simulation-Driven Design — Advanced",
    description=(
        "State-of-the-art simulation-driven design. Closes the CAD-CAE loop with "
        "parametric studies and design of experiments, builds surrogate (response "
        "surface and Gaussian-process) models, runs gradient and global "
        "optimization, applies topology and generative design, and assembles "
        "end-to-end automation pipelines and digital twins. Worked code in Python "
        "and MATLAB."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Closing the CAD-CAE loop",
            "12 min",
            r"""
# Closing the CAD-CAE loop

**Simulation-driven design** turns the CAD model into a variable in an automated
loop: a script sets parameters, regenerates geometry, meshes, solves, reads a
response, and decides the next set of parameters. The human states *what* to
optimize; the loop searches *how*.

The core abstraction is a **black-box function** $y = f(\mathbf{x})$ mapping
design variables $\mathbf{x}$ (dimensions, thicknesses, angles) to performance
metrics $y$ (mass, stress, frequency, drag). Each evaluation is one full
CAD-mesh-solve cycle, so evaluations are *expensive* — the central challenge of
the field.

```mermaid
flowchart LR
  X["Design variables x"] --> CAD["Regenerate CAD"]
  CAD --> MESH["Mesh"]
  MESH --> SOLVE["FEA / CFD solve"]
  SOLVE --> Y["Response y = f(x)"]
  Y --> OPT["Optimizer / sampler"]
  OPT -->|"next x"| X
```

A well-driven loop converges the objective toward an optimum over iterations:

```plot
{"title": "Objective vs optimization iteration (driven CAD-CAE loop)", "xLabel": "iteration", "yLabel": "objective (relative, lower better)", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "objective convergence", "color": "#dc2626"}]}
```

```python
# Skeleton of a closed-loop driver (CAD/CAE calls stubbed as a cheap proxy)
def evaluate(x):                          # x = [thickness, rib_height]
    mass   = 0.8*x[0] + 0.3*x[1]          # proxy for solver-reported mass
    stress = 200.0 / (x[0]*x[1] + 1e-6)   # proxy for peak stress
    return mass, stress

def feasible(x):
    _, stress = evaluate(x)
    return stress <= 120.0                # constraint from the solver

best = min((x for x in [[3,10],[4,8],[5,12]] if feasible(x)),
           key=lambda x: evaluate(x)[0])
print(best, [round(v,1) for v in evaluate(best)])
```

**Next:** sampling the design space efficiently with design of experiments.
""",
        ),
        _t(
            "Design of experiments and sensitivity",
            "12 min",
            r"""
# Design of experiments and sensitivity

Because each CAD-CAE evaluation is costly, you choose sample points
deliberately — **Design of Experiments (DOE)**. A full factorial grid explodes
as $L^{k}$ for $L$ levels and $k$ factors, so practitioners use **fractional
factorials**, **Latin Hypercube Sampling (LHS)** for space-filling coverage, or
**Sobol** sequences. LHS gives uniform marginal coverage with far fewer points
than a grid.

DOE feeds **sensitivity analysis**: which parameters actually move the response?
**Main-effect** and **Sobol** indices rank factors so you fix the irrelevant ones
and optimize only the influential few. Grid cost grows exponentially while
space-filling designs scale linearly with the budget you set:

```plot
{"title": "Samples needed: full-factorial grid vs space-filling DOE", "xLabel": "number of factors k", "yLabel": "samples (log-ish, relative)", "xRange": [1, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "3^x", "label": "full factorial 3^k", "color": "#dc2626"}, {"expr": "20*x", "label": "space-filling (linear budget)", "color": "#16a34a"}]}
```

```python
import numpy as np

rng = np.random.default_rng(0)

def latin_hypercube(n, k, bounds):
    # n space-filling samples over k factors within the given bounds
    cut = np.linspace(0, 1, n + 1)
    u = cut[:-1] + rng.random((n, k)) * (1.0 / n)
    for j in range(k):                       # shuffle each column independently
        u[:, j] = rng.permutation(u[:, j])
    lo, hi = bounds[:, 0], bounds[:, 1]
    return lo + u * (hi - lo)

bounds = np.array([[2.0, 6.0], [5.0, 15.0]])   # thickness, rib height
X = latin_hypercube(12, 2, bounds)
print(X.shape, X.min(axis=0).round(2), X.max(axis=0).round(2))
```

```mermaid
flowchart LR
  DV["Design variables + ranges"] --> DOE["DOE - LHS / Sobol / fractional"]
  DOE --> RUNS["Batch of CAD-CAE runs"]
  RUNS --> SENS["Sensitivity / Sobol indices"]
  SENS --> KEEP["Keep influential factors"]
  KEEP --> NEXT["Reduced design problem"]
```

**Next:** fitting a cheap surrogate so you stop calling the expensive solver.
""",
        ),
        _t(
            "Surrogate models and response surfaces",
            "13 min",
            r"""
# Surrogate models and response surfaces

A **surrogate** (metamodel) approximates the expensive function $f(\mathbf{x})$
from a handful of DOE evaluations, so further design exploration costs almost
nothing. The simplest is a **response surface** — a polynomial fit, e.g. a
quadratic

$$\hat{y}(\mathbf{x}) = \beta_0 + \sum_i \beta_i x_i + \sum_{i\le j} \beta_{ij} x_i x_j.$$

More powerful is **Kriging / Gaussian-process regression (GPR)**, which
interpolates the samples *and* returns a predictive variance — an uncertainty
estimate that drives smart sampling. Surrogate accuracy improves as training
points are added, with prediction error falling roughly as a power of the sample
count:

```plot
{"title": "Surrogate prediction error vs training samples", "xLabel": "training samples", "yLabel": "RMSE (relative)", "xRange": [4, 60], "yRange": [0, 1], "grid": true, "functions": [{"expr": "2/sqrt(x)", "label": "error ~ 1/sqrt(n)", "color": "#16a34a"}]}
```

```python
import numpy as np

# Least-squares quadratic response surface for one factor (extends to many)
x = np.array([2.0, 3.0, 4.0, 5.0, 6.0])             # design variable
y = np.array([41.0, 30.0, 25.0, 27.0, 36.0])        # solver response

A = np.column_stack([np.ones_like(x), x, x**2])     # [1, x, x^2]
beta, *_ = np.linalg.lstsq(A, y, rcond=None)
x_opt = -beta[1] / (2 * beta[2])                    # vertex of the parabola
print(beta.round(3), round(x_opt, 2))               # fitted RSM + its minimizer
```

The payoff: optimize on the surrogate (milliseconds per evaluation), then verify
the predicted optimum with one true solver run. **Adaptive sampling** — adding
points where the GP variance or the expected improvement is largest — refines the
surrogate only where it matters.

```mermaid
flowchart LR
  DOE["DOE samples"] --> FIT["Fit surrogate - RSM / Kriging"]
  FIT --> OPTM["Optimize on surrogate (cheap)"]
  OPTM --> VERIFY["Verify with true solver"]
  VERIFY -->|"add point where uncertain"| FIT
  VERIFY -->|"converged"| OUT["Optimal design"]
```

**Next:** the optimization algorithms that search the design space.
""",
        ),
        _t(
            "Optimization algorithms for design",
            "13 min",
            r"""
# Optimization algorithms for design

Design optimization minimizes an objective subject to constraints:

$$\min_{\mathbf{x}}\; f(\mathbf{x}) \quad \text{s.t.}\quad g_j(\mathbf{x}) \le 0,\;
\; \mathbf{x}_{\text{lo}} \le \mathbf{x} \le \mathbf{x}_{\text{hi}}.$$

**Gradient-based** methods (SQP, interior-point) converge fast on smooth,
unimodal problems and scale to many variables, using $\nabla f$ from adjoint or
finite differences. **Gradient-free / global** methods — genetic algorithms,
particle swarm, simulated annealing, Bayesian optimization — handle noisy,
multimodal, black-box responses but need more evaluations. Convergence speed is
the practical divide:

```plot
{"title": "Convergence: gradient-based vs global optimizer", "xLabel": "function evaluations", "yLabel": "objective gap to optimum", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.6*x)", "label": "gradient-based (fast, local)", "color": "#2563eb"}, {"expr": "exp(-0.2*x)", "label": "global (slower, robust)", "color": "#dc2626"}]}
```

```python
import numpy as np
from scipy.optimize import minimize

# Constrained design: minimize mass, keep peak stress <= 120 MPa
def mass(x):    return 0.8*x[0] + 0.3*x[1]          # thickness, rib height
def stress(x):  return 200.0 / (x[0]*x[1])          # solver proxy

cons = [{"type": "ineq", "fun": lambda x: 120.0 - stress(x)}]
bnds = [(2.0, 6.0), (5.0, 15.0)]
res = minimize(mass, x0=[4.0, 10.0], method="SLSQP", bounds=bnds, constraints=cons)
print(res.x.round(2), round(mass(res.x), 2), round(stress(res.x), 1))
```

```mermaid
flowchart LR
  PROB["min f(x) s.t. g(x)<=0"] --> SMOOTH{"Smooth + unimodal?"}
  SMOOTH -->|"yes"| GRAD["Gradient - SQP / interior-point"]
  SMOOTH -->|"no, multimodal/noisy"| GLOB["Global - GA / PSO / Bayesian"]
  GRAD --> X["Optimal x*"]
  GLOB --> X
```

In practice, couple a **global** search over a **surrogate** to find the basin,
then polish with a **gradient** step on the true model — the best of both.

**Next:** letting the algorithm invent the geometry with topology optimization.
""",
        ),
        _t(
            "Topology and generative design",
            "13 min",
            r"""
# Topology and generative design

**Topology optimization** computes the optimal material layout for a load path
rather than tuning a fixed shape. The classic **SIMP** (Solid Isotropic Material
with Penalization) method gives each element a density $\rho_e \in [0,1]$ and
minimizes compliance (maximizes stiffness) under a volume budget:

$$\min_{\rho}\; C(\rho)=\mathbf{U}^{\top}\mathbf{K}(\rho)\,\mathbf{U}
\quad \text{s.t.}\quad \frac{V(\rho)}{V_0}\le f,\;\; 0<\rho_{\min}\le\rho_e\le 1,$$

with stiffness penalized as $E_e = E_{\min} + \rho_e^{\,p}(E_0-E_{\min})$,
$p\approx 3$, pushing densities toward solid or void. **Generative design**
wraps this in a multi-objective, manufacturing-aware search that returns many
candidate geometries. Compliance falls over the optimization iterations:

```plot
{"title": "Topology optimization: compliance vs iteration", "xLabel": "iteration", "yLabel": "normalized compliance", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "compliance convergence", "color": "#16a34a"}]}
```

```matlab
% One SIMP optimality-criteria density update (core of 99-line topopt)
function xnew = oc_update(x, dc, volfrac, move)
    l1 = 0; l2 = 1e9;
    while (l2 - l1) / (l1 + l2 + 1e-9) > 1e-3
        lmid = 0.5 * (l1 + l2);
        xnew = max(1e-3, max(x - move, ...
               min(1.0, min(x + move, x .* sqrt(-dc / lmid)))));
        if mean(xnew(:)) > volfrac   % too much material -> raise multiplier
            l1 = lmid;
        else
            l2 = lmid;
        end
    end
end
```

```mermaid
flowchart LR
  SPEC["Loads + supports + volume target"] --> FE["FE solve -> compliance"]
  FE --> SENS["Sensitivity dC/drho"]
  SENS --> UPD["OC / MMA density update"]
  UPD --> FILT["Filter (mesh independence)"]
  FILT -->|"not converged"| FE
  FILT -->|"converged"| SMOOTH["Smooth -> manufacturable CAD"]
```

Outputs need **interpretation and smoothing** into manufacturable geometry, and
modern tools (Fusion 360 Generative Design, nTopology) add lattice infills and
AM/CNC constraints so candidates are buildable, not just optimal on paper.

**Next:** wiring everything into an automated pipeline and a digital twin.
""",
        ),
        _t(
            "Design automation pipelines and digital twins",
            "12 min",
            r"""
# Design automation pipelines and digital twins

The endgame is an **automation pipeline**: CAD APIs (SOLIDWORKS API, NX Open,
Onshape FeatureScript/REST, pythonOCC) chained with a mesher, a solver and an
optimizer, orchestrated by a script or a process-integration tool (Isight,
modeFRONTIER, optiSLang). A spec goes in; a verified, optimized, documented
design comes out — with traceability for every run.

A **digital twin** extends this past delivery: the parametric+simulation model is
kept in sync with a physical asset via sensor data, so it predicts behaviour,
flags drift and guides maintenance. The model's parameters are continuously
**calibrated** to measurements, so prediction error decays as data accumulates:

```plot
{"title": "Digital-twin prediction error vs calibration data", "xLabel": "calibration updates", "yLabel": "model error (relative)", "xRange": [0, 12], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.35*x)", "label": "error after calibration", "color": "#16a34a"}]}
```

```python
# A minimal automation pipeline: declarative stages run in order, results logged
def run_pipeline(spec):
    log = {}
    geom   = {"params": spec}                              # 1. regenerate CAD
    log["mesh"]   = max(2.0, 40.0 / spec["budget"])        # 2. choose mesh size
    log["stress"] = 200.0 / (spec["thk"] * spec["rib"])    # 3. solve (proxy)
    log["mass"]   = 0.8*spec["thk"] + 0.3*spec["rib"]
    log["ok"]     = log["stress"] <= 120.0                 # 4. check constraints
    log["geom"]   = geom
    return log                                             # 5. traceable record

print(run_pipeline({"thk": 4.0, "rib": 10.0, "budget": 20}))
```

```mermaid
flowchart LR
  SPEC["Requirements / spec"] --> CADAPI["CAD API - regenerate"]
  CADAPI --> MESH["Mesh"]
  MESH --> SOLVE["Solver"]
  SOLVE --> OPT["Optimizer (DOE + surrogate)"]
  OPT -->|"iterate"| CADAPI
  OPT --> OUT["Verified optimized design + report"]
  ASSET["Physical asset - sensors"] -->|"calibrate"| TWIN["Digital twin"]
  OUT --> TWIN
```

The result is a living, simulation-backed model: parametric in, optimized out,
and continuously validated against reality.

**Next:** check your understanding of the simulation-driven design loop.
""",
        ),
        _quiz(),
    ),
)


CAD_CAE_PARAMETRIC_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["CAD_CAE_PARAMETRIC_COURSES"]
