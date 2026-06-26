"""Robot Manipulators & Industrial Robotics track: Basics -> Intermediate -> Advanced.

From robot anatomy, joints and spatial transformations through forward/inverse
kinematics and the Jacobian to manipulator dynamics, trajectory generation and
control. Lessons are `text` with LaTeX, interactive ```plot blocks (joint
trajectories, manipulability, singularity behaviour, optimization convergence),
```mermaid diagrams (robot taxonomy, DH frames, kinematic/control pipelines) and
runnable ```python (NumPy/SciPy) / ```matlab code for transforms, IK solvers,
dynamics and trajectory optimization.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Robot Manipulators & Industrial Robotics — Basics ────────────────────────

_BASICS = SeedCourse(
    slug="robot-manipulators-basics",
    title="Robot Manipulators & Industrial Robotics — Basics",
    description=(
        "An intuition-first tour of robot manipulators: the anatomy of links and "
        "joints, common industrial robot morphologies (articulated, SCARA, "
        "Cartesian, delta), the workspace and degrees of freedom, rigid-body poses "
        "and homogeneous transformations, rotations, and a first look at how joint "
        "angles map to a tool position. Interactive transformation plots and robot "
        "taxonomy diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Anatomy of a robot manipulator",
            "10 min",
            r"""
# Anatomy of a robot manipulator

A **robot manipulator** is an open kinematic chain of rigid **links** connected
by **joints**, with a **base** at one end and an **end-effector** (gripper, weld
torch, tool) at the other. The controller commands the joints; the geometry of
the chain decides where the tool ends up.

Almost every industrial joint is one of two kinds:

- **Revolute (R)** — a hinge that rotates about an axis; its variable is an
  angle $\theta$.
- **Prismatic (P)** — a slider that translates along an axis; its variable is a
  displacement $d$.

A robot is named by its first joints: an **RRR** articulated arm, an **RRP**
SCARA, a **PPP** Cartesian gantry. Each independent joint adds one **degree of
freedom (DoF)**. To reach an arbitrary position *and* orientation in 3-D space
you need **six** DoF — three to place the wrist, three to orient the tool.

```mermaid
flowchart LR
    BASE[Base] --> J1[Joint 1] --> L1[Link 1] --> J2[Joint 2]
    J2 --> L2[Link 2] --> J3[Joint 3] --> WR[Wrist] --> EE[End-effector / tool]
```

The chain of joint variables $q = (q_1,\dots,q_n)$ is the **configuration**; the
tool's position and orientation is the **pose**. Everything in this course is
about the map between the two.

**Next:** the common industrial robot morphologies.
""",
        ),
        _t(
            "Industrial robot morphologies",
            "11 min",
            r"""
# Industrial robot morphologies

Industrial arms come in a handful of standard **morphologies**, each a different
arrangement of revolute and prismatic joints tuned to a class of tasks.

- **Articulated (6R)** — the classic anthropomorphic arm (KUKA, ABB, FANUC).
  Six revolute joints give a large, dexterous workspace; the default for welding,
  painting and general handling.
- **SCARA (RRP)** — two parallel revolute joints plus a vertical slider. Stiff
  vertically, compliant in the horizontal plane: ideal for fast pick-and-place
  and assembly (peg-in-hole).
- **Cartesian / gantry (PPP)** — three orthogonal linear axes. Simple kinematics
  and high accuracy over large flat areas (machining, 3-D printing, palletizing).
- **Delta (parallel)** — three arms driven from the base move a light platform;
  closed loops give very high speed and acceleration for packaging.

```mermaid
flowchart TB
    R[Industrial manipulators] --> A[Serial / open chain]
    R --> P[Parallel / closed chain]
    A --> AR[Articulated 6R]
    A --> SC[SCARA RRP]
    A --> CA[Cartesian PPP]
    P --> DE[Delta]
    P --> HX[Hexapod / Stewart]
```

Serial arms trade stiffness and speed for reach and dexterity; parallel robots
do the opposite. The reachable region — the **workspace** — and the payload set
the choice as much as the kinematics.

**Next:** workspace, degrees of freedom and reachability.
""",
        ),
        _t(
            "Workspace and degrees of freedom",
            "10 min",
            r"""
# Workspace and degrees of freedom

The **workspace** is the set of poses the end-effector can reach. We distinguish
the **reachable workspace** (positions the tool can touch in *some* orientation)
from the smaller **dexterous workspace** (positions reachable in *every*
orientation). Reach, joint limits and self-collision all shrink it.

For a planar 2-link arm with lengths $\ell_1,\ell_2$, the reachable set is an
annulus: the tool distance from the base ranges between $|\ell_1-\ell_2|$ and
$\ell_1+\ell_2$. Inside that ring most points are reachable in **two** ways —
"elbow up" and "elbow down".

```plot
{"title": "Planar 2-link reach: tool x vs elbow angle (l1=l2=1)", "xLabel": "shoulder angle (rad)", "yLabel": "tool x position", "xRange": [0,3.14], "yRange": [-2,2], "grid": true, "functions": [{"expr": "cos(x) + cos(2*x)", "label": "x = l1*cos(t) + l2*cos(2t)", "color": "#2563eb"}]}
```

**Degrees of freedom** count the independent ways the tool can move. Six DoF span
all of position and orientation in space; fewer means a *constrained* task space
(a 4-DoF SCARA cannot tilt its tool). Extra joints beyond six make a robot
**redundant** — many configurations reach the same pose, which is useful for
dodging obstacles and singularities.

```mermaid
flowchart LR
    DOF[Required task DoF] --> CHK{Robot DoF vs task}
    CHK -->|robot < task| UND[Under-actuated: cannot reach all poses]
    CHK -->|robot = task| EXA[Exactly determined]
    CHK -->|robot > task| RED[Redundant: extra freedom]
```

**Next:** describing pose with homogeneous transformations.
""",
        ),
        _t(
            "Rigid-body pose and homogeneous transforms",
            "11 min",
            r"""
# Rigid-body pose and homogeneous transforms

To say where a link is, we attach a **coordinate frame** to it and express its
**pose** relative to another frame. A pose has two parts: a **rotation** $R$ (a
$3\times3$ orthonormal matrix) and a **translation** $p$ (a 3-vector). Packed
together they form a $4\times4$ **homogeneous transformation**:

$$T = \begin{bmatrix} R & p \\ 0\;0\;0 & 1 \end{bmatrix}$$

The magic of this form is **composition by matrix multiplication**. If frame 1
is at $T_1$ in the base and frame 2 is at $T_2$ in frame 1, then frame 2 in the
base is simply $T_1 T_2$. Chaining transforms down the links is how we build the
whole arm's geometry.

```python
import numpy as np

def transform(R, p):
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = p
    return T

Rz = lambda a: np.array([[np.cos(a), -np.sin(a), 0],
                         [np.sin(a),  np.cos(a), 0],
                         [0, 0, 1]])

T1 = transform(Rz(np.pi/2), [1, 0, 0])   # rotate 90 deg, move along x
T2 = transform(np.eye(3),   [0.5, 0, 0]) # slide 0.5 along its own x
T_base = T1 @ T2                          # frame 2 expressed in the base
print(np.round(T_base[:3, 3], 3))        # tool tip position
```

```plot
{"title": "A point on link 2 traced as link 1 rotates", "xLabel": "joint-1 angle (rad)", "yLabel": "world x of tool", "xRange": [0,6.28], "yRange": [-1.6,1.6], "grid": true, "functions": [{"expr": "cos(x) - 0.5*sin(x)", "label": "world x(angle)", "color": "#2563eb"}]}
```

The inverse $T^{-1}$ has rotation $R^\top$ and translation $-R^\top p$ — cheap to
compute and used constantly to change reference frames.

**Next:** rotations - the three ways we represent orientation.
""",
        ),
        _t(
            "Rotations and orientation",
            "11 min",
            r"""
# Rotations and orientation

Orientation is harder than position because 3-D rotation is not a simple vector
space. Three representations dominate robotics, each with a trade-off:

- **Rotation matrix** $R$ — unambiguous and easy to compose ($R_a R_b$), but uses
  9 numbers for 3 DoF and must stay orthonormal.
- **Euler / roll-pitch-yaw angles** — three intuitive numbers, but they suffer
  **gimbal lock**: at certain angles two axes align and one DoF is lost.
- **Unit quaternion** $q=(w,x,y,z)$ — four numbers, no gimbal lock, numerically
  stable, and the standard for smooth orientation interpolation (**slerp**).

A rotation by angle $\theta$ about a unit axis $\hat{n}$ (the axis-angle form)
ties them together via Rodrigues' formula:

$$R = I + \sin\theta\,[\hat{n}]_\times + (1-\cos\theta)\,[\hat{n}]_\times^2$$

```mermaid
flowchart LR
    AX[Axis-angle] --> RM[Rotation matrix]
    AX --> QT[Quaternion]
    QT --> RM
    RM --> EU[Euler RPY]
    EU -. gimbal lock .-> RM
```

```python
import numpy as np

def rodrigues(axis, theta):
    n = np.asarray(axis) / np.linalg.norm(axis)
    K = np.array([[0, -n[2], n[1]],
                  [n[2], 0, -n[0]],
                  [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(theta)*K + (1-np.cos(theta))*(K @ K)

R = rodrigues([0, 0, 1], np.pi/2)   # 90 deg about z
print(np.round(R, 3))
```

```plot
{"title": "Trace of R (rotation about z) vs angle", "xLabel": "angle (rad)", "yLabel": "trace(R) = 1 + 2cos(theta)", "xRange": [0,6.28], "yRange": [-1.2,3.2], "grid": true, "functions": [{"expr": "1 + 2*cos(x)", "label": "trace(R)", "color": "#2563eb"}]}
```

Use matrices to compute, quaternions to store and interpolate, Euler angles only
to talk to humans.

**Next:** from joint angles to tool position - a first look.
""",
        ),
        _t(
            "From joint angles to tool position",
            "11 min",
            r"""
# From joint angles to tool position

We can now answer the central question of kinematics for a simple arm: given the
joint angles, **where is the tool?** This direction — configuration to pose — is
**forward kinematics**, and for a planar 2-link arm it is pure trigonometry.

With link lengths $\ell_1,\ell_2$ and joint angles $\theta_1,\theta_2$ (the
second measured relative to the first link):

$$x = \ell_1\cos\theta_1 + \ell_2\cos(\theta_1+\theta_2)$$
$$y = \ell_1\sin\theta_1 + \ell_2\sin(\theta_1+\theta_2)$$

```python
import numpy as np

def fk_planar(theta1, theta2, l1=1.0, l2=1.0):
    x = l1*np.cos(theta1) + l2*np.cos(theta1 + theta2)
    y = l1*np.sin(theta1) + l2*np.sin(theta1 + theta2)
    return np.array([x, y])

print(np.round(fk_planar(np.pi/4, np.pi/2), 3))  # tool (x, y)
```

The tool height $y$ as the shoulder sweeps (elbow fixed) traces a smooth curve —
the kind of relationship the controller must reason about every cycle:

```plot
{"title": "Tool height y as shoulder sweeps (elbow at 60 deg)", "xLabel": "shoulder angle (rad)", "yLabel": "tool y", "xRange": [0,3.14], "yRange": [-0.5,2], "grid": true, "functions": [{"expr": "sin(x) + sin(x + 1.047)", "label": "y(theta1)", "color": "#2563eb"}]}
```

Forward kinematics is always well-defined and unique: a configuration maps to
exactly one pose. The hard problem is the *reverse* — finding the joint angles
for a desired pose — which has multiple solutions or none. That is **inverse
kinematics**, the heart of the Intermediate course.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Robot Manipulators & Industrial Robotics — Intermediate ──────────────────

_INTERMEDIATE = SeedCourse(
    slug="robot-manipulators-intermediate",
    title="Robot Manipulators & Industrial Robotics — Intermediate",
    description=(
        "The core quantitative methods of manipulator kinematics: Denavit-"
        "Hartenberg parameters and the forward-kinematics product of transforms, "
        "analytic and numerical inverse kinematics, the manipulator Jacobian "
        "relating joint and Cartesian velocities, singularities and "
        "manipulability, joint-space trajectory generation, and resolved-rate "
        "velocity control. Worked NumPy/SciPy code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Denavit-Hartenberg parameters",
            "12 min",
            r"""
# Denavit-Hartenberg parameters

To handle a real arm systematically we need a convention for placing frames on
each link. The **Denavit-Hartenberg (DH)** convention describes the transform
between consecutive joint frames with just **four** parameters per joint:

- $a_i$ — link length (offset along the common normal),
- $\alpha_i$ — link twist (angle between joint axes),
- $d_i$ — link offset (along the previous $z$),
- $\theta_i$ — joint angle (about $z$).

For a revolute joint $\theta_i$ is the variable; for a prismatic joint $d_i$ is.
Each joint's transform is a fixed product:

$$^{i-1}T_i = R_z(\theta_i)\,T_z(d_i)\,T_x(a_i)\,R_x(\alpha_i)$$

```mermaid
flowchart LR
    F0[Frame i-1] --> RZ[Rz theta] --> TZ[Tz d] --> TX[Tx a] --> RX[Rx alpha] --> F1[Frame i]
```

```python
import numpy as np

def dh_transform(theta, d, a, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,      sa,     ca,    d],
        [0,       0,      0,    1],
    ])

# one row per joint: (theta, d, a, alpha)
print(np.round(dh_transform(np.pi/2, 0.1, 0.3, np.pi/2), 3))
```

A **DH table** — one row per joint — fully specifies the arm's geometry. It is
the standard interchange format between CAD, the controller and simulation tools
like the Robotics Toolbox or ROS URDF.

**Next:** forward kinematics as a product of transforms.
""",
        ),
        _t(
            "Forward kinematics by transform chains",
            "12 min",
            r"""
# Forward kinematics by transform chains

With a DH table, **forward kinematics** is the product of the per-joint
transforms from base to tool:

$$^0T_n(q) = {}^0T_1(q_1)\,{}^1T_2(q_2)\cdots{}^{n-1}T_n(q_n)$$

The result's top-left $3\times3$ block is the tool orientation $R$, and the last
column is the tool position $p$. This is exact, unique and fast — the routine the
controller calls thousands of times per second.

```python
import numpy as np

def dh_transform(theta, d, a, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([[ct, -st*ca, st*sa, a*ct],
                     [st,  ct*ca,-ct*sa, a*st],
                     [0,     sa,    ca,   d],
                     [0,      0,     0,   1]])

def forward_kinematics(dh_rows, q):
    T = np.eye(4)
    for (theta, d, a, alpha), qi in zip(dh_rows, q):
        T = T @ dh_transform(theta + qi, d, a, alpha)  # revolute: add qi to theta
    return T

# 2R planar arm (a1=a2=1), all twists zero
rows = [(0, 0, 1.0, 0), (0, 0, 1.0, 0)]
T = forward_kinematics(rows, [np.pi/4, np.pi/4])
print(np.round(T[:3, 3], 3))   # tool position
```

As the elbow sweeps with the shoulder fixed, the tool's reach (distance from
base) varies smoothly — a direct readout of the chained transform:

```plot
{"title": "Tool reach |p| vs elbow angle (2R arm, l1=l2=1)", "xLabel": "elbow angle (rad)", "yLabel": "distance from base", "xRange": [0,3.14], "yRange": [0,2.1], "grid": true, "functions": [{"expr": "sqrt(2 + 2*cos(x))", "label": "|p| = sqrt(2 + 2cos(theta2))", "color": "#2563eb"}]}
```

Because matrix multiplication composes cleanly, the same code handles 2-DoF toys
and 7-DoF collaborative arms — only the DH table changes.

**Next:** inverse kinematics - analytic and numerical.
""",
        ),
        _t(
            "Inverse kinematics",
            "13 min",
            r"""
# Inverse kinematics

**Inverse kinematics (IK)** is the reverse map: given a desired tool pose, find
the joint angles $q$. Unlike forward kinematics it can have **multiple**
solutions (elbow up/down, wrist flip), **infinitely many** (redundant arms), or
**none** (target outside the workspace).

For the planar 2R arm there is a clean **analytic** solution. The elbow angle
comes from the law of cosines:

$$\cos\theta_2 = \frac{x^2+y^2-\ell_1^2-\ell_2^2}{2\ell_1\ell_2}$$

then $\theta_1 = \operatorname{atan2}(y,x) - \operatorname{atan2}(\ell_2\sin\theta_2,\ \ell_1+\ell_2\cos\theta_2)$.

```python
import numpy as np

def ik_planar(x, y, l1=1.0, l2=1.0, elbow_up=True):
    c2 = (x*x + y*y - l1*l1 - l2*l2) / (2*l1*l2)
    c2 = np.clip(c2, -1, 1)                  # guard targets just past reach
    t2 = np.arccos(c2) * (1 if elbow_up else -1)
    t1 = np.arctan2(y, x) - np.arctan2(l2*np.sin(t2), l1 + l2*np.cos(t2))
    return np.array([t1, t2])

print(np.round(ik_planar(1.0, 1.0), 3))     # two angles, elbow-up branch
```

Most real 6-DoF arms with a **spherical wrist** admit a closed-form solution by
*kinematic decoupling*: solve the arm for the wrist centre, then the wrist for
orientation. Arms without that structure use **numerical IK** (next lessons via
the Jacobian).

```plot
{"title": "Elbow angle vs target distance r (2R arm, l1=l2=1)", "xLabel": "target distance r", "yLabel": "theta2 (rad)", "xRange": [0,2], "yRange": [0,3.2], "grid": true, "functions": [{"expr": "acos((x*x - 2)/2)", "label": "theta2 = acos((r^2-2)/2)", "color": "#dc2626"}]}
```

Choosing *which* solution to use — by joint limits, continuity from the current
pose, or distance to obstacles — is as important as finding one.

**Next:** the manipulator Jacobian.
""",
        ),
        _t(
            "The manipulator Jacobian",
            "12 min",
            r"""
# The manipulator Jacobian

The **Jacobian** $J(q)$ is the linear map from joint velocities to end-effector
velocity — the differential of forward kinematics:

$$\begin{bmatrix} v \\ \omega \end{bmatrix} = J(q)\,\dot q$$

It is a $6\times n$ matrix: the top three rows give linear velocity $v$, the
bottom three angular velocity $\omega$. For a revolute joint $i$ the column is
$\big[\,z_{i-1}\times(p_n-p_{i-1}),\ z_{i-1}\,\big]^\top$, built directly from the
forward-kinematics frames. The same $J$ also maps forces: $\tau = J^\top \mathcal{F}$
(the **force-torque duality**).

```python
import numpy as np

def jacobian_planar(q, l1=1.0, l2=1.0):
    t1, t12 = q[0], q[0] + q[1]
    # d(x,y)/d(theta1, theta2) for the 2R arm
    return np.array([
        [-l1*np.sin(t1) - l2*np.sin(t12), -l2*np.sin(t12)],
        [ l1*np.cos(t1) + l2*np.cos(t12),  l2*np.cos(t12)],
    ])

J = jacobian_planar([np.pi/4, np.pi/4])
print(np.round(J, 3))
print("det(J) =", round(float(np.linalg.det(J)), 3))   # -> l1*l2*sin(theta2)
```

For the 2R arm $\det J = \ell_1\ell_2\sin\theta_2$: it vanishes when the arm is
straight or folded ($\theta_2=0$ or $\pi$). That determinant collapsing is the
analytic signature of a **singularity**, the subject of the next lesson.

```plot
{"title": "Jacobian determinant vs elbow angle (2R, l1=l2=1)", "xLabel": "elbow angle theta2 (rad)", "yLabel": "det(J)", "xRange": [0,3.14], "yRange": [-0.2,1.1], "grid": true, "functions": [{"expr": "sin(x)", "label": "det(J) = sin(theta2)", "color": "#2563eb"}]}
```

**Next:** singularities and manipulability.
""",
        ),
        _t(
            "Singularities and manipulability",
            "12 min",
            r"""
# Singularities and manipulability

A **singularity** is a configuration where the Jacobian loses rank: the arm can
no longer move its tool in some direction, no matter how it spins its joints. Near
one, the **inverse** map blows up — small Cartesian motions demand huge joint
speeds, which is dangerous and a common cause of protective stops.

Types: **boundary** singularities (arm fully stretched, at the workspace edge)
and **interior** singularities (e.g. **wrist singularity**, two wrist axes
aligning). Detect them through the Jacobian's **singular values** from the SVD
$J = U\Sigma V^\top$: when the smallest singular value $\sigma_\min \to 0$, you
are at a singularity.

A scalar health metric is Yoshikawa's **manipulability**:

$$w(q) = \sqrt{\det\!\big(J J^\top\big)} = \sigma_1\sigma_2\cdots$$

which is the volume of the velocity ellipsoid — large means dexterous, zero means
singular.

```python
import numpy as np

def manipulability(J):
    return np.sqrt(np.linalg.det(J @ J.T))

# 2R arm: w = |l1*l2*sin(theta2)|, peaks at theta2 = 90 deg
def w_2r(theta2, l1=1.0, l2=1.0):
    return abs(l1*l2*np.sin(theta2))

print(round(w_2r(np.pi/2), 3), "(max)", round(w_2r(0.05), 3), "(near singular)")
```

```plot
{"title": "Manipulability w(theta2) for a 2R arm (l1=l2=1)", "xLabel": "elbow angle theta2 (rad)", "yLabel": "manipulability w", "xRange": [0,3.14], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "abs(sin(x))", "label": "w = |sin(theta2)|", "color": "#16a34a"}]}
```

Robust controllers stay away from low-$w$ regions or use a **damped least-squares**
inverse $J^\top(JJ^\top+\lambda^2 I)^{-1}$ that trades a little accuracy for
bounded joint speeds near singularities.

**Next:** trajectory generation in joint space.
""",
        ),
        _t(
            "Joint-space trajectory generation",
            "12 min",
            r"""
# Joint-space trajectory generation

Commanding a joint to jump to a target angle would demand infinite velocity. A
**trajectory** is a smooth time function $q(t)$ that moves between waypoints while
respecting velocity and acceleration limits. The simplest smooth point-to-point
move is a **cubic polynomial** with zero end velocities:

$$q(t) = q_0 + 3\Delta\frac{t^2}{T^2} - 2\Delta\frac{t^3}{T^3}, \quad \Delta=q_f-q_0$$

Its velocity is a parabola (peak at mid-move) and acceleration is linear. A
**quintic** (5th-order) polynomial additionally zeroes the end accelerations,
giving continuous, jerk-friendlier motion; **trapezoidal velocity** profiles are
used when a constant-speed cruise phase is wanted.

```python
import numpy as np

def cubic(q0, qf, T, t):
    d = qf - q0
    s = 3*(t/T)**2 - 2*(t/T)**3          # normalized 0 -> 1
    sd = (6*t/T**2 - 6*t**2/T**3)        # velocity scaling
    return q0 + d*s, d*sd

t = np.linspace(0, 1, 100)
q, qd = cubic(0.0, np.pi/2, 1.0, t)
print("peak joint speed (rad/s):", round(qd.max(), 3))  # at t = T/2
```

```plot
{"title": "Cubic joint trajectory: position s(t) and velocity", "xLabel": "time (normalized t/T)", "yLabel": "value (normalized)", "xRange": [0,1], "yRange": [0,1.6], "grid": true, "functions": [{"expr": "3*x^2 - 2*x^3", "label": "position s(t)", "color": "#2563eb"}, {"expr": "6*x - 6*x^2", "label": "velocity (norm)", "color": "#dc2626"}]}
```

For multi-segment paths the controller fits **splines** through the waypoints so
velocity and acceleration stay continuous at each knot, avoiding the torque
spikes a piecewise plan would cause.

**Next:** resolved-rate velocity control.
""",
        ),
        _t(
            "Resolved-rate velocity control",
            "12 min",
            r"""
# Resolved-rate velocity control

Many tasks specify a desired **tool velocity** — keep the torch moving along a
seam at 5 mm/s — rather than a sequence of joint angles. **Resolved-rate motion
control** converts a commanded Cartesian velocity into joint rates by inverting
the Jacobian:

$$\dot q = J(q)^{-1}\,\dot x_\text{des}$$

For non-square or near-singular $J$ we use the **pseudoinverse** $J^{+}$ or the
**damped least-squares** form. Integrating $\dot q$ also gives a general
**numerical IK**: drive the pose error to zero by stepping
$\dot q = J^{+}\,K\,e$, which converges from any reachable start.

```python
import numpy as np

def resolved_rate_ik(fk, jac, q, target, K=2.0, dt=0.02, steps=200, lam=0.05):
    for _ in range(steps):
        e = target - fk(q)                      # Cartesian error
        if np.linalg.norm(e) < 1e-4:
            break
        J = jac(q)
        Jdls = J.T @ np.linalg.inv(J @ J.T + lam**2*np.eye(len(e)))
        q = q + dt * (Jdls @ (K * e))           # damped least-squares step
    return q

# pair this with the 2R fk/jacobian from earlier lessons
```

The pose-error norm falls roughly geometrically each step — the familiar
exponential convergence of a well-tuned closed loop:

```plot
{"title": "Resolved-rate IK error vs iteration", "xLabel": "iteration", "yLabel": "||pose error|| (norm)", "xRange": [0,12], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "error decay", "color": "#16a34a"}]}
```

The damping factor $\lambda$ is the key tuning knob: zero gives exact tracking but
unbounded joint speeds at singularities; larger $\lambda$ keeps motion safe at the
cost of small steady tracking error.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


# ── Robot Manipulators & Industrial Robotics — Advanced ──────────────────────

_ADVANCED = SeedCourse(
    slug="robot-manipulators-advanced",
    title="Robot Manipulators & Industrial Robotics — Advanced",
    description=(
        "State-of-the-art manipulator dynamics and control: the recursive Newton-"
        "Euler and Lagrangian dynamic models, computed-torque and operational-space "
        "control, impedance and force control for contact tasks, optimization-based "
        "trajectory planning, and learning-based control. Includes Python/SciPy "
        "dynamics, optimization and reinforcement-learning code."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Manipulator dynamics: the equation of motion",
            "13 min",
            r"""
# Manipulator dynamics: the equation of motion

Kinematics says *where*; **dynamics** says what **torques** produce a motion. The
rigid-body equation of motion of an $n$-joint manipulator is:

$$M(q)\ddot q + C(q,\dot q)\dot q + g(q) = \tau$$

- $M(q)$ — the configuration-dependent **mass/inertia matrix** (symmetric,
  positive-definite),
- $C(q,\dot q)\dot q$ — **Coriolis and centrifugal** terms (velocity-coupled),
- $g(q)$ — **gravity** torques,
- $\tau$ — actuator joint torques.

This couples every joint to every other: accelerating the shoulder pushes the
elbow. Two computational routes exist — the **Lagrangian** (energy-based, good for
deriving symbolic $M,C,g$) and the **recursive Newton-Euler algorithm (RNEA)**,
an $O(n)$ outward-inward sweep that is the workhorse for real-time inverse
dynamics.

```mermaid
flowchart LR
    Q[q, qdot, qddot] --> OUT[Outward: velocities & accels base->tip]
    OUT --> FRC[Forces/moments at each link]
    FRC --> IN[Inward: sum forces tip->base]
    IN --> TAU[joint torques tau]
```

```python
import numpy as np

# Gravity torque of a 2R arm (point masses m at link ends, lengths l)
def gravity_2r(q, m1, m2, l1, l2, g=9.81):
    t1, t12 = q[0], q[0] + q[1]
    g1 = (m1+m2)*g*l1*np.cos(t1) + m2*g*l2*np.cos(t12)
    g2 = m2*g*l2*np.cos(t12)
    return np.array([g1, g2])

print(np.round(gravity_2r([0.0, 0.0], 1, 1, 1, 1), 2))  # max gravity, arm level
```

```plot
{"title": "Shoulder gravity torque vs arm angle (2R, level=worst)", "xLabel": "shoulder angle (rad)", "yLabel": "gravity torque (N*m)", "xRange": [0,3.14], "yRange": [-30,30], "grid": true, "functions": [{"expr": "29.4*cos(x)", "label": "g1(theta1)", "color": "#2563eb"}]}
```

The structure $M,C,g$ is what every model-based controller in this course exploits.

**Next:** computed-torque control.
""",
        ),
        _t(
            "Computed-torque control",
            "13 min",
            r"""
# Computed-torque control

**Computed-torque control** (a.k.a. inverse-dynamics or feedback-linearizing
control) uses the dynamic model to *cancel* the nonlinear coupling, leaving a
clean linear error system. The control law:

$$\tau = M(q)\big(\ddot q_d + K_d\dot e + K_p e\big) + C(q,\dot q)\dot q + g(q)$$

with error $e = q_d - q$. Substituting into the equation of motion makes the
closed loop exactly $\ddot e + K_d\dot e + K_p e = 0$ — a decoupled second-order
system whose poles you place directly. Choosing $K_p=\omega_n^2$, $K_d=2\zeta\omega_n$
sets every joint's natural frequency and damping.

```python
import numpy as np

def computed_torque(M, C_qd, g, q, qd, q_des, qd_des, qdd_des, wn=20.0, zeta=1.0):
    Kp, Kd = wn**2, 2*zeta*wn
    e, ed = q_des - q, qd_des - qd
    a = qdd_des + Kd*ed + Kp*e            # commanded acceleration
    return M @ a + C_qd + g              # full inverse-dynamics torque

# M, C_qd (=C@qd), g come from RNEA / the dynamic model each cycle
```

With perfect model knowledge the joint error decays as a critically damped
second-order response — fast and overshoot-free:

```plot
{"title": "Tracking error under computed torque (critically damped)", "xLabel": "time (s)", "yLabel": "joint error (rad)", "xRange": [0,1], "yRange": [-0.1,0.6], "grid": true, "functions": [{"expr": "0.5*exp(-20*x)*(1 + 20*x)", "label": "e(t), wn=20, zeta=1", "color": "#16a34a"}]}
```

The catch is **model dependence**: errors in $M,C,g$ (payload changes, friction)
degrade the cancellation. Robust and adaptive variants add terms that estimate or
bound the model error online.

**Next:** operational-space and impedance control.
""",
        ),
        _t(
            "Operational-space and impedance control",
            "13 min",
            r"""
# Operational-space and impedance control

When the *task* lives in Cartesian space — track a tool path, push with a set
force — Khatib's **operational-space formulation** writes the dynamics directly in
task coordinates using the Jacobian:

$$\Lambda(q)\ddot x + \mu(q,\dot q) + p(q) = \mathcal{F}, \quad \Lambda = (J M^{-1} J^\top)^{-1}$$

so a Cartesian wrench command maps to joint torques via $\tau = J^\top\mathcal{F}$.
This naturally handles redundancy: extra DoF are used in the **null space** of $J$
for secondary goals (posture, joint-limit avoidance) without disturbing the task.

For contact, **impedance control** regulates the *relationship* between motion and
force rather than either alone, making the end-effector behave like a virtual
mass-spring-damper:

$$\mathcal{F} = M_d\ddot{\tilde x} + D_d\dot{\tilde x} + K_d\tilde x$$

Stiff gains for free motion, compliant gains for contact — the safe way to do
assembly and human-robot interaction.

```mermaid
flowchart LR
    TASK[task wrench F] --> JT[tau = J^T F]
    JT --> NS[+ null-space torque: posture]
    NS --> ARM[manipulator]
    ARM --> FB[x, xdot, contact force] --> IMP[impedance law] --> TASK
```

```python
import numpy as np

def impedance_wrench(x, xd, x_des, xd_des, Kd, Dd):
    xt, xtd = x_des - x, xd_des - xd          # task-space error
    return Kd @ xt + Dd @ xtd                 # desired contact wrench

# tau = J.T @ impedance_wrench(...); add g(q) for gravity compensation
```

```plot
{"title": "Contact force vs penetration (selectable stiffness)", "xLabel": "penetration (mm)", "yLabel": "contact force (N)", "xRange": [0,5], "yRange": [0,50], "grid": true, "functions": [{"expr": "9*x", "label": "stiff Kd", "color": "#dc2626"}, {"expr": "3*x", "label": "compliant Kd", "color": "#16a34a"}]}
```

Choosing the right impedance for each axis (stiff normal to a surface, soft along
it) is the core skill of contact-rich manipulation.

**Next:** optimization-based trajectory planning.
""",
        ),
        _t(
            "Optimization-based trajectory planning",
            "13 min",
            r"""
# Optimization-based trajectory planning

Beyond fitting polynomials, modern planners **optimize** a whole trajectory
against an objective subject to the robot's dynamics and constraints — collision
avoidance, joint/torque limits, minimum time or minimum energy. This is a
**trajectory optimization** (optimal control) problem, usually solved by **direct
collocation** (discretize states/controls, hand to an NLP solver like IPOPT) or
sampling-based methods (RRT*, then smooth).

A minimum-effort point-to-point form:

$$\min_{q(\cdot),\tau(\cdot)} \int_0^T \|\tau\|^2\,dt \quad \text{s.t. } M\ddot q + C\dot q + g = \tau,\ q\in[q_-,q_+],\ |\tau|\le\tau_\max$$

```python
import numpy as np
from scipy.optimize import minimize

# Minimum-jerk 1-DoF move via free interior knots (toy collocation)
T, n = 1.0, 21
t = np.linspace(0, T, n)
q0, qf = 0.0, 1.0
def cost(qmid):
    q = np.concatenate(([q0], qmid, [qf]))
    jerk = np.diff(q, 3)                      # 3rd difference ~ jerk
    return np.sum(jerk**2)
x0 = np.linspace(q0, qf, n)[1:-1]
res = minimize(cost, x0, method="L-BFGS-B")
print("min-jerk cost:", round(res.fun, 4))
```

A solver started from a feasible guess drives the cost down fast, then refines —
the typical optimization convergence curve:

```plot
{"title": "Trajectory-optimizer cost vs iteration", "xLabel": "iteration", "yLabel": "cost (norm)", "xRange": [0,15], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "objective", "color": "#2563eb"}]}
```

For obstacle-rich scenes, planners like **CHOMP**, **STOMP** and **TrajOpt** fold
a collision-cost gradient into the same machinery, deforming an initial path out
of collision while keeping it smooth.

**Next:** learning-based manipulator control.
""",
        ),
        _t(
            "Learning-based manipulator control",
            "13 min",
            r"""
# Learning-based manipulator control

When the model is uncertain or the task is hard to specify analytically (contact,
deformable objects, vision-in-the-loop grasping), **learning-based** methods
complement model-based control. Three families dominate:

- **Reinforcement learning (RL)** — learn a policy $\pi_\theta(a\mid s)$ that
  maximizes expected reward, often trained in simulation and transferred to
  hardware (**sim-to-real**) with domain randomization.
- **Imitation / behaviour cloning** — learn from human demonstrations; recent
  **diffusion policies** and transformer policies handle multimodal, high-DoF
  manipulation.
- **Learned dynamics / residual control** — a network corrects a nominal
  model-based controller, capturing friction and unmodeled effects.

```mermaid
flowchart LR
    SIM[Sim + domain randomization] --> POL[Policy pi_theta]
    DEMO[Human demos] --> POL
    POL --> ROB[Real robot]
    ROB --> OBS[state, reward] --> UPD[policy update] --> POL
```

```python
import numpy as np

# Sketch: residual policy on top of a model-based controller
def control(state, model_torque, policy):
    s = np.asarray(state)
    residual = policy(s)                 # learned correction (NN forward pass)
    return model_torque + residual       # nominal + learned term

# train policy to minimize task loss; nominal term keeps it safe early on
```

Across training episodes the task reward rises and saturates — the signature
learning curve of a converging policy:

```plot
{"title": "RL return vs training episodes (manipulation policy)", "xLabel": "episodes (k)", "yLabel": "normalized return", "xRange": [0,10], "yRange": [0,1.1], "grid": true, "functions": [{"expr": "1 - exp(-0.5*x)", "label": "learning curve", "color": "#16a34a"}]}
```

The pragmatic state of the art is **hybrid**: a model-based controller guarantees
stability and safety while a learned component handles what the model cannot —
giving the data-efficiency of physics with the flexibility of learning.

**Next:** check your understanding with a short quiz.
""",
        ),
        _t(
            "Case study: a 6-DoF pick-and-place cell",
            "13 min",
            r"""
# Case study: a 6-DoF pick-and-place cell

Tie it together with an industrial **pick-and-place** cell: a 6R arm with a
spherical wrist, a 2D/3D camera, and a conveyor. The full pipeline chains every
idea from the track.

```mermaid
flowchart LR
    CAM[Camera: detect & pose] --> IK[Inverse kinematics]
    IK --> PLAN[Trajectory optimization]
    PLAN --> CTL[Computed-torque tracking]
    CTL --> GRASP[Impedance grasp + force check]
    GRASP --> PLACE[Place & retreat] --> CAM
```

Design decisions and the numbers behind them:

- **Vision -> pose**: hand-eye calibration gives the object pose in the base
  frame; closed-form IK (spherical wrist) returns up to 8 solutions, pruned by
  joint limits and continuity from the current pose.
- **Path**: a min-jerk / collision-aware trajectory keeps cycle time low while
  respecting torque limits — cycle time often dominated by accel/decel, not
  cruise.
- **Tracking**: computed-torque with gravity compensation holds sub-millimetre
  path error at high speed.
- **Grasp**: switch to impedance/force control on approach so a misaligned part
  is guided in rather than jammed.

Reducing the trajectory's peak acceleration lengthens the move only modestly while
sharply cutting peak motor torque — the classic throughput-vs-torque trade the
cell designer tunes:

```plot
{"title": "Cycle time and peak torque vs accel limit (normalized)", "xLabel": "acceleration limit (norm)", "yLabel": "value (norm)", "xRange": [0.5,3], "yRange": [0,3.5], "grid": true, "functions": [{"expr": "1/x + 0.5", "label": "cycle time", "color": "#2563eb"}, {"expr": "x", "label": "peak torque", "color": "#dc2626"}]}
```

```python
import numpy as np

# Pick the best of multiple IK solutions: closest to current joints, in limits
def select_solution(solutions, q_now, q_min, q_max):
    feasible = [q for q in solutions if np.all(q >= q_min) and np.all(q <= q_max)]
    if not feasible:
        return None
    return min(feasible, key=lambda q: np.linalg.norm(np.asarray(q) - q_now))
```

The lesson: a working cell is a *system* — perception, kinematics, planning and
control co-designed — and reliability comes from how the stages hand off, not from
any single clever algorithm.

**Next:** check your understanding with a short quiz.
""",
        ),
        _quiz(),
    ),
)


ROBOT_MANIPULATORS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["ROBOT_MANIPULATORS_COURSES"]
