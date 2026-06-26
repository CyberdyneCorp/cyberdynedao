"""Kinematics & Dynamics of Machinery track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on mechanisms and machines. Starts
from links, joints and mobility (Gruebler/Kutzbach) and the four-bar linkage;
moves through analytical position, velocity and acceleration analysis, cams and
gear trains; and ends with balancing, mechanism synthesis and computational
methods (multibody simulation and optimization-based synthesis). Lessons are
`text` with LaTeX, interactive ```plot blocks (displacement/velocity/cam/balance
curves), ```mermaid classification and workflow diagrams, and runnable
```python/```matlab snippets for loop-closure solving, cam design and synthesis.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Kinematics & Dynamics of Machinery — Basics ──────────────────────────────

_BASICS = SeedCourse(
    slug="kinematics-of-machinery-basics",
    title="Kinematics & Dynamics of Machinery — Basics",
    description=(
        "The foundations of mechanism analysis: links and kinematic pairs, the "
        "mobility (degrees-of-freedom) equation, Grashof's criterion for the "
        "four-bar linkage, and the difference between kinematics and kinetics. "
        "Builds the vocabulary and physical intuition you need before any "
        "quantitative analysis, with interactive plots and mechanism diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Machines, mechanisms, links and joints",
            "10 min",
            r"""
# Machines, mechanisms, links and joints

A **mechanism** is an assembly of rigid bodies connected by joints so that one
input motion produces a constrained, predictable output motion. A **machine** is
a mechanism (or set of mechanisms) that also transmits significant **force and
power** to do useful work. The bodies are called **links**; the connections are
**kinematic pairs** (joints).

Links are counted by how many joints they carry: a *binary* link has two, a
*ternary* link three, and so on. The fixed link is the **frame** or ground.
Joints are classified by the relative motion they permit and how many degrees of
freedom (DOF) they remove.

```mermaid
flowchart TB
  J["Kinematic pairs"] --> LOWER["Lower pairs (surface contact)"]
  J --> HIGHER["Higher pairs (line/point contact)"]
  LOWER --> R["Revolute R - 1 DOF"]
  LOWER --> P["Prismatic P - 1 DOF"]
  LOWER --> C["Cylindrical C - 2 DOF"]
  HIGHER --> CAM["Cam/follower"]
  HIGHER --> GEAR["Gear teeth"]
```

A **revolute** (pin) joint allows pure rotation; a **prismatic** (slider) allows
pure translation. Both are *lower pairs* with surface contact and one DOF.
Cam-follower and gear contacts are *higher pairs* with line or point contact.

The simplest useful closed chain is the **four-bar linkage**: ground, crank,
coupler and rocker joined by four revolutes. Almost every planar mechanism you
will study is built from these elements.

**Next:** counting degrees of freedom with the mobility equation.
""",
        ),
        _t(
            "Mobility and the Gruebler-Kutzbach equation",
            "11 min",
            r"""
# Mobility and the Gruebler-Kutzbach equation

**Mobility** $M$ is the number of independent inputs (degrees of freedom) a
mechanism needs to have a definite motion. For a **planar** mechanism the
Gruebler-Kutzbach criterion is

$$M = 3(n-1) - 2 j_1 - j_2$$

where $n$ is the number of links (including ground), $j_1$ the number of one-DOF
(lower) pairs, and $j_2$ the number of two-DOF (higher) pairs. Each free planar
body has 3 DOF; each lower pair removes 2, each higher pair removes 1.

For a four-bar: $n=4$, $j_1=4$, $j_2=0$, so $M = 3(3) - 8 = 1$. One input (turn
the crank) fully determines the motion — exactly what we want for a machine.

```plot
{"title": "Planar mobility vs number of revolute joints (n links)", "xLabel": "number of links n", "yLabel": "joints for M = 1", "xRange": [4, 12], "yRange": [4, 18], "grid": true, "functions": [{"expr": "(3*(x-1)-1)/2", "label": "j1 = (3(n-1)-1)/2", "color": "#2563eb"}]}
```

Interpreting $M$:

- $M = 1$: a constrained mechanism (one input -> definite motion).
- $M = 0$: a **structure** (no motion).
- $M < 0$: a statically indeterminate, **over-constrained** structure.
- $M \ge 2$: needs multiple inputs (e.g. a robot arm).

Beware **idle DOF** (a roller that spins freely) and special geometries
(parallelogram linkages) where Gruebler miscounts; spatial mechanisms use the
analogous formula $M = 6(n-1) - \sum (6-f_i)$.

**Next:** the four-bar linkage and Grashof's rotation criterion.
""",
        ),
        _t(
            "The four-bar linkage and Grashof's criterion",
            "12 min",
            r"""
# The four-bar linkage and Grashof's criterion

The four-bar is the workhorse of machine design. Whether any link can fully
**rotate** depends only on the link lengths through **Grashof's law**. Let $S$,
$L$ be the shortest and longest links and $P$, $Q$ the other two. The linkage is
**Grashof** (at least one link makes a full revolution) when

$$S + L \le P + Q$$

The position of the shortest link then sets the type:

```mermaid
flowchart LR
  G["S + L <= P + Q (Grashof)"] --> CR["Shortest is ground -> double-crank"]
  G --> CK["Shortest is a side -> crank-rocker"]
  G --> DR["Shortest is coupler -> double-rocker"]
  NG["S + L > P + Q (non-Grashof)"] --> TR["Triple-rocker (no full rotation)"]
```

A **crank-rocker** converts continuous rotation (motor crank) into oscillation
(rocker) — wipers, oil pumps, sewing machines. When $S+L = P+Q$ exactly the
linkage is at a **change point** (e.g. the parallelogram), where it can shift
between branches and may need an extra link to disambiguate.

The output rocker angle versus crank angle is nonlinear; a representative
oscillation looks like:

```plot
{"title": "Rocker output angle vs crank angle (crank-rocker)", "xLabel": "crank angle (rad)", "yLabel": "rocker angle (deg)", "xRange": [0, 6.28], "yRange": [-40, 40], "grid": true, "functions": [{"expr": "30*sin(x)", "label": "rocker oscillation", "color": "#16a34a"}]}
```

Two key performance numbers follow from geometry: the **transmission angle**
(coupler-to-rocker angle, best near 90 deg) and the **time ratio** of forward to
return stroke, which gives quick-return action.

**Next:** how the transmission angle governs force transmission.
""",
        ),
        _t(
            "Transmission angle and mechanical advantage",
            "10 min",
            r"""
# Transmission angle and mechanical advantage

The **transmission angle** $\mu$ is the acute angle between the coupler and the
output link (rocker). It measures how effectively force is passed to the output:
the useful (motion-driving) component of the coupler force is proportional to
$\sin\mu$, while the wasted (bearing-loading) component scales with $\cos\mu$.

Good design keeps $\mu$ in the range $40^\circ \le \mu \le 140^\circ$; values
near $0^\circ$ or $180^\circ$ cause large bearing forces, poor mechanical
advantage, and risk of locking.

```plot
{"title": "Force-transmission effectiveness vs transmission angle", "xLabel": "transmission angle (rad)", "yLabel": "effectiveness ~ sin(mu)", "xRange": [0, 3.1416], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "sin(x)", "label": "useful component ~ sin(mu)", "color": "#2563eb"}]}
```

**Mechanical advantage** (MA) of a linkage is the ratio of output torque to input
torque. By virtual work, with no friction, $T_{in}\,\omega_{in} =
T_{out}\,\omega_{out}$, so

$$\mathrm{MA} = \frac{T_{out}}{T_{in}} = \frac{\omega_{in}}{\omega_{out}}$$

MA becomes very large near a **toggle** (dead-center) position where the output
velocity ratio approaches zero — exploited in clamps, crushers and toggle
presses to multiply force, at the cost of motion.

**Next:** distinguishing kinematics from kinetics (dynamics).
""",
        ),
        _t(
            "Kinematics versus kinetics",
            "10 min",
            r"""
# Kinematics versus kinetics

Machine dynamics splits into two complementary problems:

- **Kinematics** studies motion *geometrically* — position, velocity and
  acceleration — without asking what causes it. Inputs are link geometry and the
  driving motion; outputs are displacements and their time derivatives.
- **Kinetics** (often loosely "dynamics") relates the **forces and torques** to
  the resulting motion through Newton-Euler or Lagrange equations, using link
  masses and inertias.

```mermaid
flowchart LR
  GEOM["Link geometry + input motion"] --> KIN["Kinematics: position, velocity, acceleration"]
  KIN --> KINETICS["Kinetics: forces, torques, inertia"]
  KINETICS --> DESIGN["Bearing loads, driving torque, sizing"]
```

A classic result is the **inertia force**: a link of mass $m$ whose center of
mass accelerates at $a$ experiences an effective d'Alembert force $F = -m\,a$ that
must be reacted by the joints. In a slider-crank running at speed, these inertia
forces grow with the *square* of crank speed, $\propto \omega^2$:

```plot
{"title": "Peak piston inertia force vs engine speed (~ omega^2)", "xLabel": "crank speed omega (normalized)", "yLabel": "inertia force (normalized)", "xRange": [0, 4], "yRange": [0, 16], "grid": true, "functions": [{"expr": "x^2", "label": "F ~ m r omega^2", "color": "#dc2626"}]}
```

This is why high-speed machinery must be **balanced**: the unbalanced inertia
forces, not the static loads, often dominate bearing wear and vibration.

**Next:** test your grasp of mechanisms, mobility and the four-bar.
""",
        ),
        _quiz(),
    ),
)


# ── Kinematics & Dynamics of Machinery — Intermediate ────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="kinematics-of-machinery-intermediate",
    title="Kinematics & Dynamics of Machinery — Intermediate",
    description=(
        "The core quantitative methods of machine kinematics: vector-loop "
        "position analysis and its numerical solution, velocity and "
        "acceleration analysis (including the Coriolis term), instantaneous "
        "centers, cam profile design with standard follower motions, and gear "
        "trains and ratios. Includes runnable Python/MATLAB for loop closure "
        "and cam generation."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Vector-loop position analysis",
            "13 min",
            r"""
# Vector-loop position analysis

Analytical kinematics replaces graphical construction with algebra. Model each
link as a **position vector** in complex (or 2D vector) form and write a closed
**loop-closure equation**. For the four-bar with link lengths $r_1$ (ground),
$r_2$ (crank), $r_3$ (coupler), $r_4$ (rocker) and angles $\theta_i$:

$$r_2 e^{i\theta_2} + r_3 e^{i\theta_3} - r_4 e^{i\theta_4} - r_1 = 0$$

Splitting into real and imaginary parts gives two scalar equations in the two
unknown angles $\theta_3,\theta_4$ for a given crank angle $\theta_2$. These are
nonlinear (sines and cosines) and are solved with the Freudenstein equation or
numerically by Newton-Raphson.

```python
import numpy as np
from scipy.optimize import fsolve

r1, r2, r3, r4 = 4.0, 2.0, 3.5, 3.0          # link lengths

def loop(x, th2):
    th3, th4 = x
    fx = r2*np.cos(th2) + r3*np.cos(th3) - r4*np.cos(th4) - r1
    fy = r2*np.sin(th2) + r3*np.sin(th3) - r4*np.sin(th4)
    return [fx, fy]

th3, th4 = fsolve(loop, [0.5, 1.5], args=(np.radians(60.0),))
print(np.degrees([th3, th4]))   # coupler and rocker angles
```

Sweeping $\theta_2$ through $0..2\pi$ traces the rocker's output curve:

```plot
{"title": "Coupler angle vs crank angle (four-bar)", "xLabel": "crank angle (rad)", "yLabel": "coupler angle (rad)", "xRange": [0, 6.28], "yRange": [0, 1.5], "grid": true, "functions": [{"expr": "0.6+0.4*cos(x)", "label": "theta3(theta2)", "color": "#2563eb"}]}
```

Newton-Raphson converges in a few iterations if the initial guess is on the
correct **assembly branch** (open vs crossed).

**Next:** differentiating the loop equation for velocities.
""",
        ),
        _t(
            "Velocity analysis and instant centers",
            "12 min",
            r"""
# Velocity analysis and instant centers

Differentiate the loop-closure equation once with respect to time to get the
**velocity equations**. For the four-bar, differentiating the complex loop gives

$$r_2\omega_2 e^{i\theta_2} + r_3\omega_3 e^{i\theta_3} - r_4\omega_4 e^{i\theta_4} = 0$$

a *linear* system in the unknown angular velocities $\omega_3,\omega_4$ once the
positions are known. Solve the 2x2 system at each crank angle.

```python
import numpy as np
def velocities(th2, th3, th4, w2, r2, r3, r4):
    A = np.array([[-r3*np.sin(th3),  r4*np.sin(th4)],
                  [ r3*np.cos(th3), -r4*np.cos(th4)]])
    b = np.array([ r2*np.sin(th2), -r2*np.cos(th2)]) * w2
    w3, w4 = np.linalg.solve(A, b)
    return w3, w4
```

The graphical counterpart is the **instantaneous center of velocity** (IC): the
point about which one body appears to rotate relative to another at an instant. A
planar mechanism with $n$ links has

$$N = \frac{n(n-1)}{2}$$

instant centers, located using the **Kennedy-Aronhold theorem** (any three bodies
share three collinear ICs). The rocker's angular velocity ratio peaks where the
mechanism nears a toggle:

```plot
{"title": "Rocker angular velocity vs crank angle", "xLabel": "crank angle (rad)", "yLabel": "omega4 (rad/s)", "xRange": [0, 6.28], "yRange": [-3, 3], "grid": true, "functions": [{"expr": "2*sin(x+0.4)", "label": "omega4(theta2)", "color": "#16a34a"}]}
```

**Next:** the acceleration equation and the Coriolis term.
""",
        ),
        _t(
            "Acceleration analysis and the Coriolis term",
            "12 min",
            r"""
# Acceleration analysis and the Coriolis term

Differentiating the velocity loop again gives the **acceleration equations**.
For a point fixed on a rotating link, total acceleration has a **normal**
(centripetal) part $\omega^2 r$ directed inward and a **tangential** part
$\alpha r$ perpendicular to the link:

$$\mathbf{a} = \underbrace{-\omega^2 \mathbf{r}}_{\text{normal}} + \underbrace{\boldsymbol{\alpha}\times\mathbf{r}}_{\text{tangential}}$$

When a point also **slides along** a rotating link (slider in a rotating slot,
Scotch yoke, Geneva mechanism), an extra **Coriolis acceleration** appears:

$$\mathbf{a}_{cor} = 2\,\boldsymbol{\omega}\times\mathbf{v}_{rel}, \qquad |\mathbf{a}_{cor}| = 2\,\omega\, v_{rel}$$

Forgetting this term is the classic beginner error. The four-bar acceleration
loop is again linear in $\alpha_3,\alpha_4$ once positions and velocities are
known:

```matlab
% Four-bar angular accelerations (positions/velocities already solved)
A = [-r3*sin(th3),  r4*sin(th4);
      r3*cos(th3), -r4*cos(th4)];
b = [ r2*a2*sin(th2) + r2*w2^2*cos(th2) + r3*w3^2*cos(th3) - r4*w4^2*cos(th4);
     -r2*a2*cos(th2) + r2*w2^2*sin(th2) + r3*w3^2*sin(th3) - r4*w4^2*sin(th4)];
alpha = A\b;          % [alpha3; alpha4]
```

The coupler-point acceleration magnitude over a cycle reveals where inertia loads
peak:

```plot
{"title": "Coupler-point acceleration over a cycle", "xLabel": "crank angle (rad)", "yLabel": "acceleration (m/s^2)", "xRange": [0, 6.28], "yRange": [0, 12], "grid": true, "functions": [{"expr": "6+5*cos(2*x)", "label": "|a| coupler point", "color": "#dc2626"}]}
```

**Next:** designing cam profiles for prescribed follower motion.
""",
        ),
        _t(
            "Cam profiles and follower motion",
            "13 min",
            r"""
# Cam profiles and follower motion

A **cam** is a higher-pair mechanism that converts rotation into a prescribed
follower **displacement program** $s(\theta)$. Design proceeds from the desired
follower motion (rise, dwell, return) rather than from the cam shape, which is
derived last. The key requirement is **continuity of acceleration** to avoid
shock and vibration.

Standard rise motions, in order of smoothness:

- **Constant velocity** — infinite acceleration at ends (avoid).
- **Simple harmonic (SHM)** — finite but discontinuous acceleration at boundaries.
- **Cycloidal** — $s(\theta) = h\left[\frac{\theta}{\beta} -
  \frac{1}{2\pi}\sin\frac{2\pi\theta}{\beta}\right]$, acceleration starts and ends
  at zero. Preferred for high speed.

The **fundamental law of cam design**: the follower displacement, velocity and
acceleration must all be **continuous** across the whole cycle (jerk should be
finite). Cycloidal motion satisfies this; SHM and constant-velocity do not.

```python
import numpy as np
h, beta = 20.0, np.radians(120.0)            # rise 20 mm over 120 deg
th = np.linspace(0, beta, 200)
s = h*(th/beta - np.sin(2*np.pi*th/beta)/(2*np.pi))      # cycloidal rise
v = (h/beta)*(1 - np.cos(2*np.pi*th/beta))              # velocity
a = (2*np.pi*h/beta**2)*np.sin(2*np.pi*th/beta)         # acceleration
```

The cycloidal acceleration is a smooth sine that returns to zero at both ends:

```plot
{"title": "Cycloidal cam acceleration during rise", "xLabel": "cam angle (fraction of rise)", "yLabel": "follower acceleration (norm.)", "xRange": [0, 6.28], "yRange": [-1.2, 1.2], "grid": true, "functions": [{"expr": "sin(x)", "label": "a ~ sin(2 pi theta/beta)", "color": "#2563eb"}]}
```

The **pressure angle** (between follower motion and the normal at contact) must
stay below about 30 deg for translating followers; raise the base circle radius if
it is exceeded.

**Next:** gear trains, ratios and the train value.
""",
        ),
        _t(
            "Gear trains and the train value",
            "12 min",
            r"""
# Gear trains and the train value

Gears transmit rotation at a fixed **speed ratio** set by tooth counts. For a
single mesh, conjugate (involute) teeth give a constant velocity ratio. The
**gear ratio** between driver (pinion, $N_2$ teeth) and driven gear ($N_3$ teeth)
is

$$\frac{\omega_3}{\omega_2} = -\frac{N_2}{N_3}$$

(the minus sign is the reversed sense for external gears). For a **simple train**
(one gear per shaft) the idlers cancel: the overall ratio depends only on the
first and last gears. For a **compound train** (two gears keyed to a shaft) the
**train value** multiplies the meshes:

$$e = \frac{\text{product of driver teeth}}{\text{product of driven teeth}}$$

```mermaid
flowchart LR
  IN["Input shaft"] --> G2["Pinion N2"]
  G2 --> G3["Gear N3 (+ N3' compound)"]
  G3 --> G4["Gear N4"]
  G4 --> OUT["Output shaft - overall e"]
```

For an **epicyclic (planetary)** train, gears move on a rotating carrier, so use
the **formula method** (relative to the carrier):

$$\frac{\omega_{last} - \omega_{carrier}}{\omega_{first} - \omega_{carrier}} = e$$

This single equation, plus the known input speeds, solves the planetary's output
— the basis of automatic transmissions and large reduction drives. Output speed
falls inversely with overall ratio:

```plot
{"title": "Output speed vs overall gear ratio (fixed input)", "xLabel": "overall ratio", "yLabel": "output speed (rpm)", "xRange": [1, 10], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "1000/x", "label": "n_out = n_in / ratio", "color": "#16a34a"}]}
```

**Next:** check your command of analytical kinematics, cams and gears.
""",
        ),
        _quiz(),
    ),
)


# ── Kinematics & Dynamics of Machinery — Advanced ────────────────────────────

_ADVANCED = SeedCourse(
    slug="kinematics-of-machinery-advanced",
    title="Kinematics & Dynamics of Machinery — Advanced",
    description=(
        "State-of-the-art and applied machine dynamics: static and dynamic "
        "balancing of rotating and reciprocating machinery, the inverse problem "
        "of mechanism synthesis (function, path and motion generation), "
        "optimization-based and computational synthesis, flexible-multibody "
        "simulation, and AI/surrogate methods for design. Includes runnable "
        "Python for balancing, precision-point synthesis and optimization loops."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Static and dynamic balancing of rotors",
            "13 min",
            r"""
# Static and dynamic balancing of rotors

Rotating machinery vibrates when the mass center is off the spin axis. A point
unbalance $m$ at radius $r$ produces a rotating centrifugal force

$$F = m\,r\,\omega^2$$

that grows with the **square of speed** — the dominant excitation in high-speed
machines. **Static balance** removes the net force ($\sum m_i r_i = 0$ as
vectors). **Dynamic balance** additionally removes the net moment couple ($\sum
m_i r_i a_i = 0$, where $a_i$ are axial positions) so the rotor is balanced at
*every* speed. A rigid rotor needs correction in **two planes**.

```python
import numpy as np
# Unbalances: (mass*radius vector, axial position). Solve two correction planes.
mr = np.array([1.5+0.0j, 0.0+2.0j, -1.0+0.5j])     # m*r as complex vectors
ax = np.array([0.10, 0.25, 0.40])                  # axial positions (m)
zA, zB = 0.0, 0.5                                   # correction plane positions
# Force and moment balance -> corrections in planes A and B
UB = -np.sum(mr*(zB-ax))/(zB-zA)
UA = -np.sum(mr) - UB
print("plane A:", UA, "  plane B:", UB)            # required m*r corrections
```

The residual unbalance force on the bearings scales as $\omega^2$ until
correction; field balancing uses **influence coefficients** measured from trial
weights.

```plot
{"title": "Bearing force vs speed: unbalanced vs balanced rotor", "xLabel": "speed omega (norm.)", "yLabel": "bearing force (norm.)", "xRange": [0, 5], "yRange": [0, 26], "grid": true, "functions": [{"expr": "x^2", "label": "unbalanced ~ omega^2", "color": "#dc2626"}, {"expr": "0.05*x^2", "label": "balanced (residual)", "color": "#16a34a"}]}
```

ISO 21940 defines balance-quality grades (e.g. G2.5 for machine tools, G6.3 for
general machinery).

**Next:** balancing reciprocating (slider-crank) inertia forces.
""",
        ),
        _t(
            "Reciprocating balancing and engine dynamics",
            "12 min",
            r"""
# Reciprocating balancing and engine dynamics

A slider-crank's piston acceleration is not a pure sinusoid. Expanding the exact
kinematics for crank radius $r$, rod length $l$ and ratio $n = l/r$ gives the
piston acceleration

$$a_p \approx r\omega^2\left(\cos\theta + \frac{\cos 2\theta}{n}\right)$$

The $\cos\theta$ term is the **primary** inertia force (frequency $\omega$); the
$\cos 2\theta$ term is the **secondary** (frequency $2\omega$). Primary forces can
be balanced by counterweights or balance shafts running at $\omega$; secondary
forces need shafts at $2\omega$ (e.g. Lanchester balancers in inline-four
engines).

```python
import numpy as np
r, l, w = 0.04, 0.14, 300.0        # m, m, rad/s
n = l/r
th = np.linspace(0, 2*np.pi, 400)
a = r*w**2*(np.cos(th) + np.cos(2*th)/n)        # piston acceleration
primary   = r*w**2*np.cos(th)
secondary = r*w**2*np.cos(2*th)/n
```

Engine **configuration** determines which orders cancel: an inline-six is
naturally balanced in primary and secondary forces and couples; a 90-deg V8 with
a cross-plane crank balances primaries with counterweights. The acceleration
shows the characteristic asymmetry from the secondary term:

```plot
{"title": "Piston acceleration: primary + secondary", "xLabel": "crank angle (rad)", "yLabel": "acceleration (norm.)", "xRange": [0, 6.28], "yRange": [-1.6, 1.6], "grid": true, "functions": [{"expr": "cos(x)+0.28*cos(2*x)", "label": "a_p (n = 3.5)", "color": "#2563eb"}, {"expr": "cos(x)", "label": "primary only", "color": "#dc2626"}]}
```

**Next:** the inverse problem - synthesizing a mechanism for a task.
""",
        ),
        _t(
            "Mechanism synthesis: function, path and motion",
            "13 min",
            r"""
# Mechanism synthesis: function, path and motion

**Synthesis** is the inverse of analysis: given a desired task, find the link
geometry. Three classic problem types:

- **Function generation** — make output angle track a function of input angle,
  $\psi = f(\phi)$ (e.g. a computing linkage).
- **Path generation** — make a coupler point trace a specified curve.
- **Motion (rigid-body) generation** — guide a body through prescribed
  positions and orientations.

```mermaid
flowchart LR
  TASK["Design task"] --> TYPE{"Type?"}
  TYPE --> FUN["Function generation"]
  TYPE --> PATH["Path generation"]
  TYPE --> MOT["Motion generation (Burmester)"]
  FUN --> FREU["Freudenstein equation"]
  MOT --> BURM["Burmester curves -> link pivots"]
```

**Precision-point** synthesis matches the task exactly at a few points; error
grows between them (structural error). For function generation the
**Freudenstein equation**

$$K_1\cos\psi - K_2\cos\phi + K_3 = \cos(\phi-\psi)$$

is *linear* in the unknowns $K_1,K_2,K_3$, so three precision points give a 3x3
linear solve for the link-length ratios:

```python
import numpy as np
phi = np.radians([20, 40, 60]);  psi = np.radians([30, 55, 75])
A = np.column_stack([np.cos(psi), -np.cos(phi), np.ones(3)])
b = np.cos(phi - psi)
K1, K2, K3 = np.linalg.solve(A, b)          # Freudenstein constants -> ratios
```

For motion generation, **Burmester theory** locates the circle/center points that
guide a body through up to five finitely separated positions. Spacing precision
points by **Chebyshev** rule minimizes the worst-case structural error.

**Next:** recasting synthesis as numerical optimization.
""",
        ),
        _t(
            "Optimization-based and computational synthesis",
            "13 min",
            r"""
# Optimization-based and computational synthesis

Precision-point methods give only a handful of exact points. **Optimization
synthesis** instead minimizes a continuous error over the whole task. Define
design variables $\mathbf{x}$ (link lengths, pivot locations, crank offset) and
minimize the deviation between the generated and target curves:

$$\min_{\mathbf{x}} \; \sum_{k=1}^{m} \big\| \mathbf{p}_{gen}(\mathbf{x},\theta_k) - \mathbf{p}_{target,k} \big\|^2$$

subject to Grashof, transmission-angle and assembly (non-defect) constraints. The
landscape is **nonconvex** with many local minima and infeasible "circuit defect"
regions, so global/stochastic methods (genetic algorithms, particle swarm,
differential evolution) plus a local polish work well.

```python
import numpy as np
from scipy.optimize import differential_evolution

target = np.array([[ ... ]])    # desired coupler-curve points

def cost(x):
    pts = coupler_curve(x)      # forward kinematics of candidate linkage
    err = np.sum((pts - target)**2)
    if not grashof_ok(x) or min_transmission_angle(x) < np.radians(40):
        err += 1e3              # penalty for defective/poor designs
    return err

bounds = [(0.5, 5)]*4 + [(-3, 3)]*4
res = differential_evolution(cost, bounds, tol=1e-6, seed=0)
```

Typical convergence of the objective decays roughly exponentially with
generations:

```plot
{"title": "Synthesis objective vs optimizer generation", "xLabel": "generation", "yLabel": "coupler-curve error", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "error ~ exp(-0.4 g)", "color": "#16a34a"}]}
```

Modern toolchains add **surrogate models** and **machine-learned** atlases of
coupler curves to seed the search, cutting forward-kinematic evaluations by orders
of magnitude.

**Next:** simulating the full machine with multibody dynamics and AI surrogates.
""",
        ),
        _t(
            "Multibody simulation and AI-assisted design",
            "13 min",
            r"""
# Multibody simulation and AI-assisted design

Closed-loop and spatial mechanisms are simulated as **constrained multibody
systems**. Assemble the constraint Jacobian $\Phi_q$ and solve the
**index-3 differential-algebraic equations** (DAEs):

$$\begin{bmatrix} M & \Phi_q^{\top} \\ \Phi_q & 0 \end{bmatrix}
\begin{bmatrix} \ddot{q} \\ \lambda \end{bmatrix} =
\begin{bmatrix} Q \\ \gamma \end{bmatrix}$$

where $M$ is the mass matrix, $\lambda$ the Lagrange multipliers (joint reaction
forces), $Q$ applied loads and $\gamma$ the acceleration-level constraint term.
Stabilization (Baumgarte) or projection keeps the position/velocity constraints
satisfied. Flexible links add modal or finite-element coordinates for elastodynamic
effects.

```python
import numpy as np
def mbd_accel(q, qd, M, Phi_q, Q, gamma):
    n = M.shape[0]
    K = np.block([[M, Phi_q.T],
                  [Phi_q, np.zeros((Phi_q.shape[0],)*2)]])
    rhs = np.concatenate([Q, gamma])
    sol = np.linalg.solve(K, rhs)
    return sol[:n], sol[n:]        # accelerations, Lagrange multipliers
```

Tools such as Adams, Simscape Multibody and open-source MBDyn integrate these DAEs.
The current frontier couples them with **AI**: neural-network **surrogates** that
predict peak joint forces in microseconds, **reinforcement-learning** controllers
for legged and parallel robots, and **physics-informed** models that respect the
constraint manifold. Surrogate error typically falls as more training samples are
added:

```plot
{"title": "Surrogate model error vs training samples", "xLabel": "training samples (x100)", "yLabel": "validation error", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "RMSE decay", "color": "#2563eb"}]}
```

These surrogates close the synthesis loop: optimize over thousands of candidate
linkages in seconds, then verify the winner with a full multibody solve.

**Next:** the final assessment on balancing, synthesis and simulation.
""",
        ),
        _quiz(),
    ),
)


KINEMATICS_OF_MACHINERY_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["KINEMATICS_OF_MACHINERY_COURSES"]
