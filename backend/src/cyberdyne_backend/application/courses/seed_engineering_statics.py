"""Engineering Statics track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on the statics of rigid bodies in
equilibrium: from forces, moments and free-body diagrams, through equilibrium of
particles and rigid bodies, trusses and frames, to friction, centroids,
distributed loads and second moments of area. Lessons are `text` with LaTeX,
interactive ```plot blocks (load curves, friction, distributions), ```mermaid
workflow/classification diagrams and runnable ```python (NumPy/SciPy) code that
solves equilibrium systems, truss method-of-joints and section properties.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Engineering Statics — Basics ─────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="engineering-statics-basics",
    title="Engineering Statics — Basics",
    description=(
        "The intuition and fundamentals of statics: scalars and vectors, forces "
        "and how to resolve and add them, the moment of a force and couples, the "
        "all-important free-body diagram, and the equilibrium of a particle. "
        "Built on SI units, Newton's laws and consistent sign conventions, with "
        "interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What statics is: forces, units & Newton's laws",
            "10 min",
            r"""
# What statics is: forces, units & Newton's laws

**Statics** is the branch of mechanics that studies bodies in **equilibrium** —
at rest or moving with constant velocity, so the net force and net moment on them
are zero. It is the foundation of structural and machine design: before a beam,
truss or bracket can be sized, the internal forces it carries must be found.

A **force** is a vector with magnitude, direction and point of application,
measured in **newtons** ($1\ \text{N} = 1\ \text{kg}\cdot\text{m/s}^2$).
Newton's three laws govern statics: (1) a body stays at rest unless acted on by a
net force; (2) $\mathbf{F} = m\,\mathbf{a}$; and (3) every action has an equal,
opposite reaction. In statics $\mathbf{a} = 0$, so Newton's second law collapses
to the equilibrium condition $\sum \mathbf{F} = 0$.

Weight is the gravitational force $W = m g$, with $g \approx 9.81\ \text{m/s}^2$.
Doubling a mass doubles its weight — a strictly linear relation:

```plot
{"title": "Weight vs mass (W = m g)", "xLabel": "mass m (kg)", "yLabel": "weight W (N)", "xRange": [0, 100], "yRange": [0, 1000], "grid": true, "functions": [{"expr": "9.81*x", "label": "W = 9.81 m", "color": "#2563eb"}]}
```

The statics workflow is the same on every problem:

```mermaid
flowchart LR
  A["Identify body"] --> B["Draw free-body diagram"]
  B --> C["Apply equilibrium: sum F = 0, sum M = 0"]
  C --> D["Solve for unknown forces"]
```

**Next:** representing forces as vectors and resolving them into components.
""",
        ),
        _t(
            "Vectors & resolving forces into components",
            "11 min",
            r"""
# Vectors & resolving forces into components

A force in a plane is most useful when split into **rectangular components**
along the $x$ and $y$ axes. For a force of magnitude $F$ at angle $\theta$ from
the $x$-axis:

$$F_x = F\cos\theta, \qquad F_y = F\sin\theta, \qquad F = \sqrt{F_x^2 + F_y^2}.$$

The angle is recovered with $\theta = \operatorname{atan2}(F_y, F_x)$. Working in
components turns vector addition into ordinary arithmetic: add the $x$-components
and the $y$-components of every force separately, then recombine.

The horizontal component of a fixed-magnitude force falls off as the cosine of
its angle — important when deciding how much of a pull actually acts along a
member:

```plot
{"title": "Horizontal component of a 100 N force vs angle", "xLabel": "angle theta (rad)", "yLabel": "Fx (N)", "xRange": [0, 1.57], "yRange": [0, 100], "grid": true, "functions": [{"expr": "100*cos(x)", "label": "Fx = 100 cos(theta)", "color": "#2563eb"}]}
```

In Python the resultant of several forces is a single vector sum:

```python
import numpy as np

# forces given as (magnitude N, angle deg)
forces = [(100, 30), (60, 120), (80, -45)]
vecs = np.array([[F*np.cos(np.radians(a)), F*np.sin(np.radians(a))]
                 for F, a in forces])
R = vecs.sum(axis=0)
mag = np.hypot(*R)
ang = np.degrees(np.arctan2(R[1], R[0]))
print(f"Resultant: {mag:.1f} N at {ang:.1f} deg")
```

**Next:** the moment of a force — how a force tends to rotate a body.
""",
        ),
        _t(
            "Moment of a force & couples",
            "11 min",
            r"""
# Moment of a force & couples

A force not only pushes a body, it tends to **rotate** it about a point. The
**moment** (or torque) of a force about point $O$ is

$$M_O = F\,d,$$

where $d$ is the **perpendicular distance** (the moment arm) from $O$ to the
line of action of the force. In 2-D the moment is a scalar with a sign — counter-
clockwise positive by the usual convention. Equivalently, $M_O = \mathbf{r}
\times \mathbf{F}$, giving $M_O = x F_y - y F_x$ from the components of the
position vector $\mathbf{r}$ and the force.

For a fixed force, the moment grows linearly with the moment arm — moving a
wrench's grip out from the bolt multiplies the turning effect:

```plot
{"title": "Moment vs moment arm for a 50 N force", "xLabel": "moment arm d (m)", "yLabel": "moment M (N*m)", "xRange": [0, 0.6], "yRange": [0, 30], "grid": true, "functions": [{"expr": "50*x", "label": "M = 50 d", "color": "#2563eb"}]}
```

A **couple** is two equal, opposite, non-collinear forces. Their net force is
zero, but they produce a pure moment $M = F\,d$ that is the **same about every
point** — a free vector. Couples are how we model applied torques.

```mermaid
flowchart LR
  F1["F (up)"] -.->|"separation d"| F2["F (down)"]
  F1 --> C["Pure couple M = F d, same about any point"]
  F2 --> C
```

**Next:** isolating a body and drawing its free-body diagram.
""",
        ),
        _t(
            "Free-body diagrams & support reactions",
            "12 min",
            r"""
# Free-body diagrams & support reactions

The **free-body diagram (FBD)** is the single most important skill in statics.
You isolate one body, "cut" it free from its surroundings, and replace every
contact and support with the **force(s)** it exerts. Then equilibrium equations
can be written about that body alone.

Each support type constrains motion and so supplies specific reactions:

| Support | Reactions |
|---|---|
| Roller / smooth surface | 1 force, normal to surface |
| Pin / hinge | 2 force components ($R_x$, $R_y$) |
| Fixed (built-in) support | 2 forces + 1 moment |
| Cable | tension along the cable only |

The count of unknown reactions versus available equations decides whether a
problem is **statically determinate** (solvable with statics alone) or
indeterminate.

```mermaid
flowchart TB
  A["Choose the body to isolate"] --> B["Remove supports & contacts"]
  B --> C["Add applied loads + weight"]
  C --> D["Add reaction force per support type"]
  D --> E["Label geometry, angles, distances"]
  E --> F["Ready: write equilibrium equations"]
```

A common error is forgetting that a pin gives **two** unknowns while a roller
gives only one. Count carefully: a simply supported beam (one pin, one roller)
has three reaction unknowns, matching the three planar equilibrium equations —
determinate.

**Next:** the equilibrium of a particle, the simplest equilibrium problem.
""",
        ),
        _t(
            "Equilibrium of a particle",
            "11 min",
            r"""
# Equilibrium of a particle

A **particle** is a body whose size is irrelevant, so all forces act through one
point and produce no moment. Equilibrium then requires only that the forces
balance:

$$\sum F_x = 0, \qquad \sum F_y = 0.$$

These two scalar equations solve for at most **two** unknowns. The classic case
is a weight hung from two cables: resolve each cable tension into components,
sum, and solve the resulting linear system.

For a symmetric two-cable support, each cable's tension rises sharply as the
cables flatten (small angle to the horizontal) — why a tightrope must carry huge
tension:

```plot
{"title": "Cable tension vs half-angle (1000 N load, two cables)", "xLabel": "angle from horizontal (rad)", "yLabel": "tension per cable (N)", "xRange": [0.1, 1.5], "yRange": [0, 5000], "grid": true, "functions": [{"expr": "500/sin(x)", "label": "T = W/(2 sin theta)", "color": "#dc2626"}]}
```

The same problem solved as a linear system in Python:

```python
import numpy as np

# Cables at 30 deg and 45 deg above horizontal hold a 1000 N weight.
a1, a2 = np.radians(30), np.radians(45)
A = np.array([[-np.cos(a1),  np.cos(a2)],   # sum Fx = 0
              [ np.sin(a1),  np.sin(a2)]])   # sum Fy = 0
b = np.array([0.0, 1000.0])
T1, T2 = np.linalg.solve(A, b)
print(f"T1 = {T1:.1f} N, T2 = {T2:.1f} N")
```

**Next:** test your grasp of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Statics — Intermediate ───────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="engineering-statics-intermediate",
    title="Engineering Statics — Intermediate",
    description=(
        "The core quantitative methods of statics: equilibrium of a rigid body in "
        "2-D and 3-D, analysis of trusses by the method of joints and the method "
        "of sections, frames and machines with multi-force members, and the "
        "internal shear-force and bending-moment diagrams that follow. Worked with "
        "linear systems in Python."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Rigid-body equilibrium in 2-D",
            "12 min",
            r"""
# Rigid-body equilibrium in 2-D

A rigid body, unlike a particle, has size, so forces produce moments and a third
equation appears:

$$\sum F_x = 0, \qquad \sum F_y = 0, \qquad \sum M_O = 0.$$

Three equations solve for **three** unknown reactions — exactly the count for a
determinate, properly constrained planar body. Choosing the moment point $O$
wisely (at the intersection of two unknowns) eliminates them from the moment
equation, often giving one reaction directly.

For a simply supported beam of span $L$ with a point load $P$ at distance $a$
from the left pin, summing moments about each support gives the reactions

$$R_A = P\frac{L-a}{L}, \qquad R_B = P\frac{a}{L}.$$

As the load slides toward $B$, reaction $R_B$ rises linearly while $R_A$ falls:

```plot
{"title": "Support reactions vs load position (P = 1000 N, L = 4 m)", "xLabel": "load position a (m)", "yLabel": "reaction (N)", "xRange": [0, 4], "yRange": [0, 1000], "grid": true, "functions": [{"expr": "1000*(4-x)/4", "label": "R_A", "color": "#2563eb"}, {"expr": "1000*x/4", "label": "R_B", "color": "#dc2626"}]}
```

The reactions are the solution of a 3x3 linear system:

```python
import numpy as np

P, a, L = 1000.0, 1.5, 4.0   # N, m, m
# unknowns: Ax, Ay, By  (pin at A, roller at B -> vertical only)
A = np.array([[1, 0, 0],            # sum Fx
              [0, 1, 1],            # sum Fy
              [0, 0, L]])           # sum M about A
b = np.array([0.0, P, P*a])
Ax, Ay, By = np.linalg.solve(A, b)
print(f"Ax={Ax:.0f}  Ay={Ay:.0f}  By={By:.0f} N")
```

**Next:** extending equilibrium to three dimensions.
""",
        ),
        _t(
            "Equilibrium in 3-D",
            "12 min",
            r"""
# Equilibrium in 3-D

In space a rigid body has **six** equilibrium equations — three force and three
moment:

$$\sum F_x = \sum F_y = \sum F_z = 0, \qquad \sum M_x = \sum M_y = \sum M_z = 0.$$

Moments are now genuine vectors computed with the cross product
$\mathbf{M}_O = \mathbf{r} \times \mathbf{F}$. Forces are written as
magnitude times a **unit vector** along the line of action, $\mathbf{F} =
F\,\hat{\mathbf{u}}$, where $\hat{\mathbf{u}} = \mathbf{d}/|\mathbf{d}|$ from the
position difference $\mathbf{d}$ between the two endpoints.

```mermaid
flowchart LR
  A["Endpoints of member"] --> B["d = end - start"]
  B --> C["unit vector u = d / |d|"]
  C --> D["F vector = F * u"]
  D --> E["M = r cross F"]
```

A 3-D problem, e.g. a mast held by three guy cables, is assembled as a 6x6 (or
smaller, exploiting symmetry) linear system. NumPy handles the cross products and
the solve:

```python
import numpy as np

# Pole top at P; three cables to ground anchors A, B, C; vertical load at top.
P = np.array([0, 0, 6.0])
anchors = {"A": [4, 0, 0], "B": [-2, 3, 0], "C": [-2, -3, 0]}
dirs = {k: (np.array(a) - P) / np.linalg.norm(np.array(a) - P)
        for k, a in anchors.items()}
M = np.column_stack([dirs["A"], dirs["B"], dirs["C"]])  # 3 unknown tensions
load = np.array([0, 0, 5000.0])                          # 5 kN upward reaction needed
T = np.linalg.solve(M, load)
print("Cable tensions (N):", np.round(T, 1))
```

The tension a single inclined cable must carry to resist a fixed vertical load
blows up as it nears horizontal:

```plot
{"title": "Cable tension vs elevation angle (5 kN vertical)", "xLabel": "elevation angle (rad)", "yLabel": "tension (N)", "xRange": [0.1, 1.5], "yRange": [0, 20000], "grid": true, "functions": [{"expr": "5000/sin(x)", "label": "T = F/sin(theta)", "color": "#dc2626"}]}
```

**Next:** trusses solved by the method of joints.
""",
        ),
        _t(
            "Trusses: the method of joints",
            "12 min",
            r"""
# Trusses: the method of joints

A **truss** is a structure of straight two-force members joined at pins. Each
member carries only **axial** force — pure tension or compression — so its line of
action lies along the member. The **method of joints** applies particle
equilibrium ($\sum F_x = 0$, $\sum F_y = 0$) at each pin, working outward from a
joint with at most two unknown members.

By convention member forces are assumed in **tension** (arrows pulling away from
the joint); a negative result means the member is actually in compression.

```mermaid
flowchart LR
  A["Find support reactions"] --> B["Pick joint with <= 2 unknowns"]
  B --> C["Sum Fx = 0, Sum Fy = 0"]
  C --> D["Solve member forces"]
  D --> E["Move to next joint"]
  E --> B
```

For a whole truss the joint equations form one large linear system $\mathbf{A}\,
\mathbf{f} = \mathbf{b}$, solved at once:

```python
import numpy as np

# Tiny 3-member truss: joints A(0,0) pin, B(4,0) roller, C(2,3).
# Members AC, BC, AB; 10 kN downward load at C.
import numpy as np
L_ac = np.hypot(2, 3); L_bc = np.hypot(2, 3)
# unit components toward C from each end
uac = np.array([2, 3]) / L_ac
ubc = np.array([-2, 3]) / L_bc
# Joint C equilibrium: F_AC*(-uac) + F_BC*(-ubc) + (0,-10000) = 0
A = np.column_stack([-uac, -ubc])
b = np.array([0.0, 10000.0])
F_ac, F_bc = np.linalg.solve(A, b)
print(f"AC = {F_ac/1e3:.2f} kN, BC = {F_bc/1e3:.2f} kN  (neg = compression)")
```

A member's required force grows as its angle to the load flattens:

```plot
{"title": "Diagonal member force vs angle (10 kN load)", "xLabel": "member angle (rad)", "yLabel": "member force (N)", "xRange": [0.2, 1.5], "yRange": [0, 30000], "grid": true, "functions": [{"expr": "10000/sin(x)", "label": "F = P/sin(theta)", "color": "#16a34a"}]}
```

**Next:** cutting through a truss with the method of sections.
""",
        ),
        _t(
            "Trusses: the method of sections",
            "11 min",
            r"""
# Trusses: the method of sections

When only a few specific member forces are wanted, the **method of sections** is
faster than joints. You make an imaginary cut through the truss (slicing at most
three unknown members), treat one side as a rigid body, and apply the **three**
rigid-body equations — including $\sum M = 0$ about a clever point.

The trick: take moments about the intersection of two of the three cut members,
so the moment equation contains **only the third unknown** and solves it
directly.

```mermaid
flowchart TB
  A["Find reactions"] --> B["Cut <= 3 unknown members"]
  B --> C["Keep one free-body side"]
  C --> D["Sum M about intersection of two cut members"]
  D --> E["One member force directly"]
  E --> F["Sum Fx, Sum Fy for the rest"]
```

For a Pratt or Warren bridge truss of depth $h$ under a panel load $P$ at a lever
arm $x$, a top chord found by moments is $F = P x / h$. The force scales inversely
with truss depth — deeper trusses carry the same moment with less chord force:

```plot
{"title": "Chord force vs truss depth (P*x = 40 kN*m)", "xLabel": "truss depth h (m)", "yLabel": "chord force (N)", "xRange": [0.5, 5], "yRange": [0, 80000], "grid": true, "functions": [{"expr": "40000/x", "label": "F = M / h", "color": "#2563eb"}]}
```

Method of sections and method of joints are complementary: sections for a quick
look at a few critical members, joints for a full enumeration.

**Next:** frames and machines, where members carry more than axial force.
""",
        ),
        _t(
            "Frames, machines & internal forces",
            "13 min",
            r"""
# Frames, machines & internal forces

**Frames** (stationary, e.g. a stepladder) and **machines** (moving, e.g.
pliers) contain **multi-force members** — members loaded at more than two points,
so they carry shear and bending as well as axial force. They are dismembered:
each member gets its own FBD, and Newton's third law links shared pins ($\mathbf{F}$
on one is $-\mathbf{F}$ on the other).

Inside a beam, the internal loads are the **shear force** $V$ and **bending
moment** $M$. They are tied by

$$\frac{dV}{dx} = -w(x), \qquad \frac{dM}{dx} = V(x),$$

so for a simply supported beam with a central point load the bending moment rises
linearly to a peak under the load and falls back to zero — the basis of the
shear-force and bending-moment diagrams (SFD/BMD):

```plot
{"title": "Bending moment along a beam, central point load (P=1000 N, L=4 m)", "xLabel": "position x (m)", "yLabel": "bending moment M (N*m)", "xRange": [0, 4], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "500*x - 1000*abs(x-2)*0.5 - 250*abs(x-2)", "label": "M(x)", "color": "#dc2626"}]}
```

A compact way to build the SFD/BMD numerically:

```python
import numpy as np

L, P = 4.0, 1000.0          # span (m), central load (N)
RA = RB = P/2               # symmetric reactions
x = np.linspace(0, L, 401)
V = np.where(x < L/2, RA, RA - P)              # shear force
M = np.where(x < L/2, RA*x, RA*x - P*(x-L/2))  # bending moment
print(f"Max |V| = {np.abs(V).max():.0f} N, Max M = {M.max():.0f} N*m")
```

**Next:** check your command of the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Statics — Advanced ───────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="engineering-statics-advanced",
    title="Engineering Statics — Advanced",
    description=(
        "Applied and state-of-the-art statics: dry friction and its engineering "
        "applications, centroids and centers of mass, distributed loads and "
        "hydrostatic pressure, the second moment of area with the parallel-axis "
        "theorem and Mohr's circle, and a computational closing chapter on "
        "matrix structural analysis and design optimization of trusses."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Dry friction & its applications",
            "12 min",
            r"""
# Dry friction & its applications

**Coulomb (dry) friction** resists sliding between contacting surfaces. While
static, the friction force adjusts to whatever value equilibrium needs, up to a
maximum

$$F_{\max} = \mu_s N,$$

where $\mu_s$ is the coefficient of static friction and $N$ the normal force.
Once motion begins, kinetic friction $F_k = \mu_k N$ (with $\mu_k < \mu_s$) acts.
A block on an incline stays put until the angle reaches $\theta = \arctan\mu_s$,
the **angle of repose**.

The maximum friction available rises linearly with the normal force — the basis
of clutches, brakes and bolted joints:

```plot
{"title": "Maximum static friction vs normal force (mu_s = 0.4)", "xLabel": "normal force N (N)", "yLabel": "max friction (N)", "xRange": [0, 1000], "yRange": [0, 400], "grid": true, "functions": [{"expr": "0.4*x", "label": "F_max = mu_s N", "color": "#2563eb"}]}
```

A spectacular nonlinear case is the **capstan (belt-friction) equation**: a rope
wrapped over a fixed drum amplifies a holding force exponentially with wrap angle,
$T_2 = T_1 e^{\mu\beta}$. A couple of turns lets a small force hold an enormous
load:

```plot
{"title": "Capstan tension ratio vs wrap angle (mu = 0.3)", "xLabel": "wrap angle beta (rad)", "yLabel": "T2 / T1", "xRange": [0, 6.28], "yRange": [0, 7], "grid": true, "functions": [{"expr": "exp(0.3*x)", "label": "T2/T1 = exp(mu*beta)", "color": "#dc2626"}]}
```

```python
import numpy as np
T1, mu, turns = 100.0, 0.3, 2          # held force (N), coeff, wraps
beta = turns * 2 * np.pi
print(f"Can hold {T1*np.exp(mu*beta):.0f} N with a {T1:.0f} N grip")
```

**Next:** locating centroids and centers of mass.
""",
        ),
        _t(
            "Centroids & centers of mass",
            "11 min",
            r"""
# Centroids & centers of mass

The **centroid** is the geometric center of an area; the **center of mass** is
where the weight of a body effectively acts. For a composite area built from
simple shapes,

$$\bar{x} = \frac{\sum A_i\,\bar{x}_i}{\sum A_i}, \qquad
\bar{y} = \frac{\sum A_i\,\bar{y}_i}{\sum A_i}.$$

Holes are treated as **negative areas**. For a continuous region the sums become
integrals, $\bar{x} = \frac{1}{A}\int x\,dA$. The centroid is essential because
distributed loads and bending stresses are referenced to it.

```mermaid
flowchart LR
  A["Split into simple shapes"] --> B["Area A_i + local centroid"]
  B --> C["First moments A_i * x_i, A_i * y_i"]
  C --> D["Sum and divide by total area"]
  D --> E["Composite centroid (xbar, ybar)"]
```

A composite-area centroid in a few lines:

```python
import numpy as np

# (area, x_centroid, y_centroid); a hole has negative area
parts = [(200.0, 5.0, 10.0),     # main rectangle
         (50.0, 15.0, 5.0),      # added flange
         (-30.0, 6.0, 8.0)]      # bolt hole
A = np.array([p[0] for p in parts])
x = np.array([p[1] for p in parts])
y = np.array([p[2] for p in parts])
xbar, ybar = (A*x).sum()/A.sum(), (A*y).sum()/A.sum()
print(f"Centroid = ({xbar:.2f}, {ybar:.2f})")
```

For a right triangle of base $b$, the centroid sits at $b/3$ from the vertical
edge — useful as a sanity check on numerical results:

```plot
{"title": "Triangle centroid x vs base length (x = b/3)", "xLabel": "base b (m)", "yLabel": "centroid x (m)", "xRange": [0, 6], "yRange": [0, 2], "grid": true, "functions": [{"expr": "x/3", "label": "xbar = b/3", "color": "#16a34a"}]}
```

**Next:** distributed loads and hydrostatic pressure.
""",
        ),
        _t(
            "Distributed loads & hydrostatic pressure",
            "12 min",
            r"""
# Distributed loads & hydrostatic pressure

Real loads are rarely points. A **distributed load** $w(x)$ (N/m) is replaced for
equilibrium by a single **resultant** equal to the area under the load curve,
acting through the **centroid** of that area:

$$R = \int_0^L w(x)\,dx, \qquad \bar{x} = \frac{1}{R}\int_0^L x\,w(x)\,dx.$$

A uniform load $w_0$ over length $L$ gives $R = w_0 L$ at midspan; a triangular
load gives $R = \tfrac{1}{2} w_0 L$ at $\tfrac{2}{3} L$ from the zero end.

**Hydrostatic pressure** is the classic linearly varying load: pressure grows
with depth as $p = \rho g h$, so a submerged wall feels a triangular pressure
distribution:

```plot
{"title": "Hydrostatic pressure vs depth (water)", "xLabel": "depth h (m)", "yLabel": "pressure p (kPa)", "xRange": [0, 10], "yRange": [0, 100], "grid": true, "functions": [{"expr": "9.81*x", "label": "p = rho g h (kPa)", "color": "#2563eb"}]}
```

The resultant force on the wall and its line of action by numerical integration:

```python
import numpy as np

rho, g, H, b = 1000.0, 9.81, 5.0, 2.0     # water, depth (m), wall width (m)
h = np.linspace(0, H, 501)
p = rho * g * h                            # Pa, increasing with depth
w = p * b                                  # N/m along the wall
R = np.trapz(w, h) if hasattr(np, "trapz") else np.trapezoid(w, h)
hbar = (np.trapezoid(h*w, h)) / R          # depth of resultant
print(f"Resultant = {R/1e3:.1f} kN at depth {hbar:.2f} m")
```

The resultant acts at $\tfrac{2}{3}H$ — the centroid of the triangular pressure
prism — a result every dam and tank wall design relies on.

**Next:** the second moment of area and Mohr's circle.
""",
        ),
        _t(
            "Second moment of area & the parallel-axis theorem",
            "13 min",
            r"""
# Second moment of area & the parallel-axis theorem

The **second moment of area** (area moment of inertia) measures how an area is
distributed about an axis — it governs a beam's bending stiffness and a column's
buckling resistance:

$$I_x = \int y^2\,dA, \qquad I_y = \int x^2\,dA.$$

For a rectangle of width $b$, height $h$ about its centroid, $I = bh^3/12$. The
**cube** dependence on height is why beams are oriented tall: doubling depth
multiplies stiffness eightfold.

```plot
{"title": "Rectangular I vs height (b = 0.1 m)", "xLabel": "height h (m)", "yLabel": "I (m^4)", "xRange": [0, 0.4], "yRange": [0, 0.0005], "grid": true, "functions": [{"expr": "0.1*x^3/12", "label": "I = b h^3 / 12", "color": "#dc2626"}]}
```

The **parallel-axis theorem** shifts a moment of inertia from the centroid to a
parallel axis a distance $d$ away:

$$I = \bar{I} + A\,d^2.$$

This is what lets composite sections (I-beams, channels) be built up from
rectangles. The **product of inertia** $I_{xy}$ and the rotation of axes lead to
**principal axes** and a **Mohr's circle** identical in form to the stress circle.

```python
import numpy as np

# I-beam: two flanges + web, parallel-axis to the section centroid (here y=0).
def rect_I(b, h, d):           # I about an axis distance d from the rect centroid
    return b*h**3/12 + (b*h)*d**2
flange = rect_I(0.10, 0.02, 0.11)      # one flange, d to neutral axis
web    = rect_I(0.01, 0.20, 0.0)       # web straddles the axis
I_total = 2*flange + web
print(f"I about neutral axis = {I_total:.3e} m^4")
```

**Next:** computational statics — matrix methods and optimization.
""",
        ),
        _t(
            "Computational statics: matrix methods & optimization",
            "14 min",
            r"""
# Computational statics: matrix methods & optimization

Modern statics is done at scale by the **direct stiffness method**, the backbone
of finite-element analysis. Each truss bar contributes a $4\times4$ element
stiffness $\mathbf{k} = \frac{EA}{L}\,\mathbf{T}$ in global coordinates; these
assemble into a global $\mathbf{K}$, and the structure is solved from
$\mathbf{K}\,\mathbf{u} = \mathbf{f}$ after applying boundary conditions.

```mermaid
flowchart LR
  A["Element stiffness k_e"] --> B["Assemble global K"]
  B --> C["Apply boundary conditions"]
  C --> D["Solve K u = f for displacements"]
  D --> E["Recover member forces & stresses"]
```

A single bar's contribution and a reduced solve:

```python
import numpy as np

def bar_k(E, A, L, c, s):
    k = E*A/L
    T = np.array([[c*c, c*s, -c*c, -c*s],
                  [c*s, s*s, -c*s, -s*s],
                  [-c*c, -c*s, c*c, c*s],
                  [-c*s, -s*s, c*s, s*s]])
    return k*T

K = bar_k(2.1e11, 1e-4, 2.0, 1.0, 0.0)     # horizontal steel bar
free = [2, 3]                               # free DOFs at the loaded node
Kff = K[np.ix_(free, free)]
f = np.array([0.0, -1000.0])                # 1 kN downward
u = np.linalg.solve(Kff, f)
print("Free displacements (m):", u)
```

**Design optimization** closes the loop: minimize structural mass subject to
stress and displacement limits, e.g. with `scipy.optimize` or topology
optimization (SIMP). Gradient-based optimizers converge geometrically — objective
decay looks like an exponential:

```plot
{"title": "Truss-mass optimization convergence", "xLabel": "iteration", "yLabel": "normalized mass above optimum", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "convergence", "color": "#16a34a"}]}
```

```python
from scipy.optimize import minimize
import numpy as np
# Minimize bar volume sum(A*L) s.t. stress |P/A| <= sigma_allow.
L = np.array([2.0, 2.5, 3.0]); P = np.array([8e3, 5e3, 6e3]); sa = 150e6
obj = lambda A: float(A @ L)
cons = [{"type": "ineq", "fun": lambda A, i=i: sa - P[i]/A[i]} for i in range(3)]
res = minimize(obj, x0=np.full(3, 1e-3), constraints=cons,
               bounds=[(1e-5, 1e-2)]*3)
print("Optimal areas (mm^2):", np.round(res.x*1e6, 1))
```

**Next:** prove your mastery of applied and computational statics.
""",
        ),
        _quiz(),
    ),
)


ENGINEERING_STATICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ENGINEERING_STATICS_COURSES"]
