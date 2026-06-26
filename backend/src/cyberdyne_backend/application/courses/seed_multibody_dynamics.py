"""Multibody Dynamics & Simulation track: Basics -> Intermediate -> Advanced.

Bodies, joints and constraints; equations of motion (Newton-Euler, Lagrange,
DAEs) and their numerical integration; through to simulating mechanisms, vehicles
and robots. Lessons are `text` with single-backslash LaTeX, interactive ```plot
blocks for response and convergence curves, ```mermaid diagrams for modelling and
solver workflows, and runnable ```python (NumPy/SciPy) and ```matlab code for
assembling and integrating the equations of motion.
"""

# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson

# Lesson bodies use engineering notation (e.g. mass blocks like 6×6, units like
# −9.81 m/s²) inside the markdown, hence the ambiguous-unicode allowances above.


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


_BASICS = SeedCourse(
    slug="multibody-dynamics-basics",
    title="Multibody Dynamics & Simulation — Basics",
    description=(
        "Build intuition for systems of connected bodies: rigid bodies and their "
        "degrees of freedom, the joints that connect them, the constraints joints "
        "impose, and how to count mobility. A first reading of forces, torques and "
        "what a multibody simulation actually computes."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is a multibody system?",
            "10 min",
            r"""
# What is a multibody system?

A **multibody system (MBS)** is a collection of rigid (or flexible) bodies linked by **joints** and acted on by **forces**. A car suspension, a robot arm, an engine crank-slider, a wind-turbine drivetrain — all are multibody systems. Multibody dynamics is the discipline that predicts how such an assembly *moves* over time given its geometry, masses, joints and applied loads.

It sits between two simpler worlds. A single particle (Engineering Dynamics) has no orientation; a single rigid body has six degrees of freedom (DOF) in 3D — three translations, three rotations. Connect many bodies with joints and you get a constrained system whose motion is the heart of this track.

The deliverable of a simulation is a time history: positions, velocities, accelerations of every body, plus the **reaction forces** in each joint. Engineers use it to size bearings, check clearances, tune ride comfort and verify a robot reaches its target without collision.

```mermaid
flowchart LR
  A[Bodies: mass, inertia, geometry] --> D[Multibody model]
  B[Joints: constraints] --> D
  C[Forces: gravity, springs, motors] --> D
  D --> E[Equations of motion]
  E --> F[Simulation: positions, velocities, reactions over time]
```

```plot
{"title": "DOF of a chain of free bodies (3D, before joints)", "xLabel": "number of bodies", "yLabel": "degrees of freedom", "xRange": [1,8], "yRange": [0,48], "grid": true, "functions": [{"expr": "6*x", "label": "6 per free rigid body", "color": "#2563eb"}]}
```

**Next:** the rigid body and how we describe its pose.
""",
        ),
        _t(
            "Rigid bodies, pose and degrees of freedom",
            "12 min",
            r"""
# Rigid bodies, pose and degrees of freedom

A **rigid body** keeps every internal distance fixed, so its state is fully given by its **pose**: the position of a reference point (its mass center G) plus its orientation. In the plane that is 3 numbers $(x,y,\theta)$ — hence **3 DOF**. In space it is 6: position $(x,y,z)$ and three orientation parameters (Euler angles, or a unit quaternion to avoid singularities).

Mass distribution matters as much as mass. The **inertia tensor** $\mathbf I$ generalizes the scalar moment of inertia; for planar motion only $I_G=\int r^2\,dm$ about the out-of-plane axis is needed. Translation obeys $\sum\mathbf F=m\mathbf a_G$ and rotation obeys $\sum\mathbf M_G=I_G\,\alpha$ in 2D.

Orientation parameters are not just bookkeeping: Euler angles suffer **gimbal lock**, and quaternions $q=(q_0,q_1,q_2,q_3)$ with $|q|=1$ are the standard remedy in simulation codes.

```mermaid
flowchart TB
  A[Rigid body pose] --> B[Position of G]
  A --> C[Orientation]
  C --> D[Euler angles: 3 numbers, gimbal lock]
  C --> E[Quaternion: 4 numbers, |q|=1, no singularity]
```

```plot
{"title": "DOF of one rigid body: planar vs spatial", "xLabel": "dimension (2 = plane, 3 = space)", "yLabel": "DOF", "xRange": [2,3], "yRange": [0,7], "grid": true, "functions": [{"expr": "3*x - 3", "label": "DOF = 3*(d-1): 3 then 6", "color": "#16a34a"}]}
```

**Next:** how joints connect bodies and remove DOF.
""",
        ),
        _t(
            "Joints and the constraints they impose",
            "12 min",
            r"""
# Joints and the constraints they impose

A **joint** is an idealized connection that *allows* some relative motion and *forbids* the rest. Each forbidden motion is a **constraint** that removes degrees of freedom. The forbidden directions are exactly where the joint can carry a **reaction** force or torque.

Common lower-pair joints and the DOF they *permit* between two spatial bodies:

- **Revolute (pin/hinge):** 1 DOF (rotation about one axis). Removes 5.
- **Prismatic (slider):** 1 DOF (translation along one axis). Removes 5.
- **Cylindrical:** 2 DOF (rotate and slide on one axis).
- **Spherical (ball):** 3 DOF (pure rotation).
- **Planar:** 3 DOF; **fixed (weld):** 0 DOF.

In 2D a revolute joint removes 2 DOF (it ties the two contact points together), while a prismatic joint removes 2 as well (fixing one translation and the relative angle).

```mermaid
flowchart LR
  A[Two bodies] --> B[Revolute: 1 DOF]
  A --> C[Prismatic: 1 DOF]
  A --> D[Spherical: 3 DOF]
  A --> E[Fixed/weld: 0 DOF]
  B --> F[Joint carries the constrained reactions]
  C --> F
  D --> F
  E --> F
```

```plot
{"title": "DOF removed per joint vs DOF it permits (spatial)", "xLabel": "DOF permitted f", "yLabel": "DOF removed = 6 - f", "xRange": [0,6], "yRange": [0,6], "grid": true, "functions": [{"expr": "6 - x", "label": "removed = 6 - f", "color": "#dc2626"}]}
```

**Next:** counting the net mobility of an assembly.
""",
        ),
        _t(
            "Mobility and the Gruebler-Kutzbach criterion",
            "12 min",
            r"""
# Mobility and the Gruebler-Kutzbach criterion

How many independent motions does an assembled mechanism have? Count them with the **Gruebler-Kutzbach** mobility formula. For planar mechanisms with $n$ links (including the fixed ground), $j$ joints and $f_i$ DOF allowed by joint $i$:
$$M = 3(n-1) - \sum_{i=1}^{j}(3 - f_i).$$
For lower pairs that permit 1 DOF (pins, sliders), this reduces to the familiar $M = 3(n-1) - 2j$. The spatial version uses 6 instead of 3.

A planar **four-bar linkage** has $n=4$, $j=4$ revolute joints, giving $M = 3(3) - 2(4) = 1$ — a single input crank fully determines the motion. A slider-crank likewise gives $M=1$. $M=0$ means a structure (no motion); $M<0$ signals a statically indeterminate, over-constrained frame.

Beware **redundant constraints**: two parallel hinges on one axis count twice in the formula but remove fewer independent DOF, so the naive count can mislead — a hint of the constraint-rank issues you meet later.

```mermaid
flowchart LR
  A[Count links n incl. ground] --> B[Count joints and their DOF f_i]
  B --> C[M = 3(n-1) - sum(3 - f_i)]
  C --> D{M value}
  D -->|M=1| E[Mechanism: 1 input]
  D -->|M=0| F[Structure]
  D -->|M<0| G[Over-constrained]
```

```plot
{"title": "Planar mobility vs joint count (n=4 links, 1-DOF joints)", "xLabel": "number of joints j", "yLabel": "mobility M", "xRange": [3,6], "yRange": [-3,3], "grid": true, "functions": [{"expr": "9 - 2*x", "label": "M = 3(n-1) - 2j", "color": "#2563eb"}]}
```

**Next:** the forces and torques that drive the motion.
""",
        ),
        _t(
            "Forces, torques and free-body thinking",
            "11 min",
            r"""
# Forces, torques and free-body thinking

Motion comes from **applied loads**: gravity, springs and dampers, motor/actuator torques, contact and friction. In a multibody model these are added on top of the joint reactions, which are *unknowns* the simulation solves for. The bookkeeping tool is still the **free-body diagram (FBD)** — but now one per body, with joint reactions appearing as equal-and-opposite pairs (Newton's third law) between connected bodies.

A spring of stiffness $k$ between two attachment points contributes a force $F=-k(\ell-\ell_0)$ along its line of action; a linear damper adds $-c\dot\ell$. These translate into forces and moments on each connected body and are the easiest way to add compliance to an otherwise rigid model.

Cutting a joint and exposing its reaction is exactly how we will later assemble the equations of motion: each body gets $\sum\mathbf F=m\mathbf a_G$ and $\sum M_G=I_G\alpha$, and the joint reactions couple them.

```mermaid
flowchart LR
  A[Isolate each body] --> B[Draw applied loads: gravity, springs, motors]
  B --> C[Expose joint reactions as 3rd-law pairs]
  C --> D[Write F = m a and M = I alpha per body]
  D --> E[Couple via shared reactions]
```

```plot
{"title": "Spring force vs stretch (k = 800 N/m)", "xLabel": "stretch l - l0 (m)", "yLabel": "spring force (N)", "xRange": [-0.1,0.1], "yRange": [-80,80], "grid": true, "functions": [{"expr": "-800*x", "label": "F = -k (l - l0)", "color": "#16a34a"}]}
```

**Next:** what a solver does with all of this.
""",
        ),
        _t(
            "What a multibody simulation computes",
            "10 min",
            r"""
# What a multibody simulation computes

Given bodies, joints and forces, a simulator builds the **equations of motion** and marches them forward in time. Conceptually it repeats three steps each time step: (1) evaluate all forces at the current state, (2) solve for accelerations consistent with the joint constraints, (3) integrate accelerations to update velocities and positions. The output is a trajectory plus joint reactions.

Tools you will meet: general-purpose multibody packages (MSC Adams, Simscape Multibody, MBDyn), robotics dynamics libraries (Pinocchio, RBDL, MuJoCo, Drake), and DIY code in Python/MATLAB for learning. They differ mainly in how they *formulate* the constraints — a topic we open in the Intermediate course.

A first taste in code: integrate a simple pendulum (one body, one revolute joint to ground) with SciPy. The angle $\theta$ obeys $\ddot\theta=-(g/L)\sin\theta$.

```python
import numpy as np
from scipy.integrate import solve_ivp
g, L = 9.81, 1.0
rhs = lambda t, y: [y[1], -(g/L)*np.sin(y[0])]
sol = solve_ivp(rhs, [0, 10], [np.deg2rad(60), 0.0], max_step=0.01)
print(f"final angle {np.rad2deg(sol.y[0,-1]):.1f} deg, steps {sol.t.size}")
```

```plot
{"title": "Simple pendulum small-angle response (wn=sqrt(g/L))", "xLabel": "t (s)", "yLabel": "theta (rad)", "xRange": [0,8], "yRange": [-1,1], "grid": true, "functions": [{"expr": "1.047*cos(3.13*x)", "label": "theta(t) small-angle", "color": "#dc2626"}]}
```

**Next:** formalize joints as algebraic constraints in the Intermediate course.
""",
        ),
        _quiz(),
    ),
)


_INTERMEDIATE = SeedCourse(
    slug="multibody-dynamics-intermediate",
    title="Multibody Dynamics & Simulation — Intermediate",
    description=(
        "The core quantitative methods: constraint equations and the Jacobian, "
        "Newton-Euler and Lagrangian formulations, the descriptor (DAE) form with "
        "Lagrange multipliers, constraint stabilization, and explicit/implicit "
        "numerical integration. Worked code in SciPy and MATLAB."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Generalized coordinates and constraint equations",
            "13 min",
            r"""
# Generalized coordinates and constraint equations

We describe a system by a vector of **generalized coordinates** $\mathbf q$. Joints impose **holonomic constraints** — algebraic relations among positions — written as
$$\boldsymbol\Phi(\mathbf q,t)=\mathbf 0,$$
with $m$ scalar equations for $m$ constrained DOF. A revolute joint between bodies $i$ and $j$, for example, forces two reference points to coincide: $\mathbf r_i + \mathbf A_i\,\mathbf s_i' - \mathbf r_j - \mathbf A_j\,\mathbf s_j' = \mathbf 0$, where $\mathbf A$ are rotation matrices.

Differentiating gives the **velocity** and **acceleration** constraint forms:
$$\boldsymbol\Phi_{\mathbf q}\,\dot{\mathbf q} = -\boldsymbol\Phi_t,\qquad \boldsymbol\Phi_{\mathbf q}\,\ddot{\mathbf q} = -(\boldsymbol\Phi_{\mathbf q}\dot{\mathbf q})_{\mathbf q}\dot{\mathbf q} - 2\boldsymbol\Phi_{\mathbf q t}\dot{\mathbf q} - \boldsymbol\Phi_{tt} \equiv \boldsymbol\gamma.$$
The matrix $\boldsymbol\Phi_{\mathbf q}$ is the **constraint Jacobian** — the single most important object in the rest of this course.

Constraints that cannot be integrated to position level (e.g. rolling without slipping, $\dot x = R\dot\theta$) are **nonholonomic** and constrain only velocities.

```mermaid
flowchart TB
  A[Phi(q,t) = 0 : position] --> B[d/dt: Phi_q qdot = -Phi_t : velocity]
  B --> C[d/dt: Phi_q qddot = gamma : acceleration]
  C --> D[Constraint Jacobian Phi_q drives the dynamics]
```

```python
import numpy as np
# Planar revolute: point P on body fixed to ground at origin.
# q = [x, y, theta]; local offset s' = [sx, sy]
def Phi(q, s):
    x, y, th = q
    A = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return np.array([x, y]) + A @ s          # must equal 0
q, s = np.array([0.3, -0.2, 0.5]), np.array([-0.34, 0.16])
print("constraint residual:", np.round(Phi(q, s), 3))
```

**Next:** turning constraints and forces into equations of motion.
""",
        ),
        _t(
            "Newton-Euler equations of motion",
            "13 min",
            r"""
# Newton-Euler equations of motion

The **Newton-Euler** approach writes the unconstrained dynamics body-by-body and appends the joint reactions as forces $\boldsymbol\Phi_{\mathbf q}^{\mathsf T}\boldsymbol\lambda$, where $\boldsymbol\lambda$ are **Lagrange multipliers** (the constraint forces). For the full system,
$$\mathbf M\,\ddot{\mathbf q} + \boldsymbol\Phi_{\mathbf q}^{\mathsf T}\boldsymbol\lambda = \mathbf Q,$$
where $\mathbf M$ is the (often block-diagonal) **mass matrix**, $\mathbf Q$ the applied/generalized forces, and $\boldsymbol\Phi_{\mathbf q}^{\mathsf T}\boldsymbol\lambda$ the reaction. For a planar body the mass block is $\mathrm{diag}(m,m,I_G)$.

Pairing this with the acceleration-level constraint $\boldsymbol\Phi_{\mathbf q}\ddot{\mathbf q}=\boldsymbol\gamma$ gives the **augmented (KKT) system** solved at every instant:
$$\begin{bmatrix}\mathbf M & \boldsymbol\Phi_{\mathbf q}^{\mathsf T}\\ \boldsymbol\Phi_{\mathbf q} & \mathbf 0\end{bmatrix}\begin{bmatrix}\ddot{\mathbf q}\\ \boldsymbol\lambda\end{bmatrix}=\begin{bmatrix}\mathbf Q\\ \boldsymbol\gamma\end{bmatrix}.$$
Solve it for $\ddot{\mathbf q}$ and $\boldsymbol\lambda$, then integrate. The reactions come out *for free*, which is why this form dominates general-purpose codes.

```python
import numpy as np
def accel_and_lambda(M, Phiq, Q, gamma):
    n, m = M.shape[0], Phiq.shape[0]
    K = np.block([[M, Phiq.T], [Phiq, np.zeros((m, m))]])
    rhs = np.concatenate([Q, gamma])
    sol = np.linalg.solve(K, rhs)
    return sol[:n], sol[n:]      # qddot, lambda
M = np.diag([2.0, 2.0, 0.5])
Phiq = np.array([[1.0, 0, 0], [0, 1.0, 0]])   # pin at origin
qdd, lam = accel_and_lambda(M, Phiq, np.array([0, -19.62, 0.0]), np.zeros(2))
print("qddot:", np.round(qdd, 3), " lambda (reaction):", np.round(lam, 2))
```

**Next:** the energy-based alternative — Lagrange's equations.
""",
        ),
        _t(
            "Lagrangian formulation",
            "13 min",
            r"""
# Lagrangian formulation

The **Lagrangian** route trades vector force-balancing for scalar energy. Define $\mathcal L = T - V$ (kinetic minus potential energy) in terms of generalized coordinates. For unconstrained DOF,
$$\frac{d}{dt}\!\left(\frac{\partial \mathcal L}{\partial \dot q_k}\right) - \frac{\partial \mathcal L}{\partial q_k} = Q_k^{nc},$$
with $Q_k^{nc}$ the non-conservative generalized forces (motors, dampers). With constraints, add $\boldsymbol\Phi_{\mathbf q}^{\mathsf T}\boldsymbol\lambda$ exactly as before — the two formulations meet at the same descriptor equations.

The payoff is that reactions doing no work (ideal joints) never appear if you choose **minimal coordinates**. For a double pendulum with angles $\theta_1,\theta_2$, writing $T$ and $V$ and turning the crank yields the equations directly, with no joint forces to chase. The mass matrix $\mathbf M(\mathbf q)$ is now configuration-dependent and couples the coordinates.

```matlab
syms t1 t2 t1d t2d m1 m2 L1 L2 g real
% positions of the two bobs (planar double pendulum)
x1 =  L1*sin(t1);            y1 = -L1*cos(t1);
x2 = x1 + L2*sin(t2);        y2 = y1 - L2*cos(t2);
v1sq = (L1*t1d)^2;
v2sq = (L1*t1d)^2 + (L2*t2d)^2 + 2*L1*L2*t1d*t2d*cos(t1-t2);
T = 0.5*m1*v1sq + 0.5*m2*v2sq;          % kinetic energy
V = m1*g*y1 + m2*g*y2;                   % potential energy
Lag = T - V;                             % Lagrangian L = T - V
% EoM: d/dt(dL/dqdot) - dL/dq = 0  ->  use diff(...) symbolically
```

```plot
{"title": "Double-pendulum kinetic energy vs lead angle (schematic)", "xLabel": "theta1 (rad)", "yLabel": "T (J), unit params", "xRange": [-3,3], "yRange": [0,5], "grid": true, "functions": [{"expr": "0.5 + 2*sin(x)^2", "label": "T includes coupling cos(t1-t2)", "color": "#2563eb"}]}
```

**Next:** the differential-algebraic structure these equations share.
""",
        ),
        _t(
            "The descriptor form: differential-algebraic equations",
            "12 min",
            r"""
# The descriptor form: differential-algebraic equations

Stack the equations of motion with the position-level constraints and you get a **differential-algebraic equation (DAE)** system, not an ODE:
$$\mathbf M\ddot{\mathbf q}+\boldsymbol\Phi_{\mathbf q}^{\mathsf T}\boldsymbol\lambda=\mathbf Q,\qquad \boldsymbol\Phi(\mathbf q,t)=\mathbf 0.$$
The algebraic constraint $\boldsymbol\Phi=\mathbf 0$ has no derivative of $\boldsymbol\lambda$ in it — that is what makes it a DAE. Its **differentiation index** is 3 (you must differentiate $\boldsymbol\Phi$ three times to recover an ODE for $\boldsymbol\lambda$), and high index makes naive integration unstable.

Two coping strategies: solve at the **acceleration level** (index reduced to 1) using the KKT system from the Newton-Euler lesson, or move to **minimal coordinates** where constraints are eliminated and an ODE remains. Index reduction silently lets the position and velocity constraints **drift**, motivating the stabilization in the next lesson.

```mermaid
flowchart TB
  A[Index-3 DAE: M qdd + Phiq^T lam = Q, Phi=0] --> B[Differentiate Phi twice]
  B --> C[Index-1: solve KKT for qdd and lambda]
  C --> D[Integrate qdd -> drift in Phi and Phidot]
  A --> E[Or: minimal coordinates -> pure ODE]
```

```python
import numpy as np
# Index-3 -> index-1: append acceleration constraint Phiq qdd = gamma.
def kkt(M, Phiq, Q, gamma):
    z = np.zeros((Phiq.shape[0],)*2)
    K = np.block([[M, Phiq.T], [Phiq, z]])
    return np.linalg.solve(K, np.concatenate([Q, gamma]))
# condition number warns when constraints are near-redundant (rank loss)
M = np.diag([1.0, 1.0, 0.2]); Phiq = np.array([[1, 0, 0], [0, 1, 0.0]])
print("KKT cond:", np.linalg.cond(np.block([[M, Phiq.T],
      [Phiq, np.zeros((2, 2))]])))
```

**Next:** keeping the constraints satisfied during integration.
""",
        ),
        _t(
            "Constraint stabilization and drift",
            "12 min",
            r"""
# Constraint stabilization and drift

Integrating at the acceleration level only guarantees $\ddot{\boldsymbol\Phi}\to 0$; rounding and truncation let $\boldsymbol\Phi$ and $\dot{\boldsymbol\Phi}$ **drift** away from zero — a pendulum slowly grows its arm length on screen. Three standard fixes:

- **Baumgarte stabilization:** replace the acceleration target with $\ddot{\boldsymbol\Phi}+2\alpha\dot{\boldsymbol\Phi}+\beta^2\boldsymbol\Phi=\mathbf 0$, feeding position/velocity error back like a PD controller. Cheap, but $\alpha,\beta$ need tuning ($\beta=\alpha$ is a common, well-damped choice).
- **Coordinate projection:** after each step, project $\mathbf q$ back onto $\boldsymbol\Phi=\mathbf 0$ (and $\dot{\mathbf q}$ onto the velocity constraint) with a few Newton iterations. Robust and the modern default.
- **Index-2/GGL formulation:** add the velocity constraint with its own multiplier so the integrator sees a stabilized index-2 system.

```python
import numpy as np
def baumgarte_gamma(gamma0, Phi, Phidot, alpha=10.0, beta=10.0):
    # acceleration RHS becomes gamma0 - 2*alpha*Phidot - beta**2*Phi
    return gamma0 - 2*alpha*Phidot - beta**2*Phi
# projection step (positions): one Newton correction onto Phi(q)=0
def project(q, Phi_fn, Jac_fn):
    r = Phi_fn(q)
    J = Jac_fn(q)
    return q - J.T @ np.linalg.solve(J @ J.T, r)
print("Baumgarte and projection ready")
```

```plot
{"title": "Constraint error vs time: raw vs stabilized", "xLabel": "t (s)", "yLabel": "|Phi| (normalized)", "xRange": [0,10], "yRange": [0,1], "grid": true, "functions": [{"expr": "0.08*x", "label": "raw index-1 drift", "color": "#dc2626"}, {"expr": "exp(-1.5*x)", "label": "Baumgarte/projection", "color": "#16a34a"}]}
```

**Next:** the numerical integrators that march the system.
""",
        ),
        _t(
            "Numerical integration of multibody systems",
            "13 min",
            r"""
# Numerical integration of multibody systems

With accelerations available from the KKT solve, you integrate the state $[\mathbf q,\dot{\mathbf q}]$ forward. The choice of integrator matters:

- **Explicit Runge-Kutta** (e.g. RK45, SciPy's default): simple and accurate for non-stiff systems, but the step shrinks badly when stiff springs/contacts impose fast time constants.
- **Implicit methods** (BDF, Radau, generalized-$\alpha$, HHT-$\alpha$): handle stiffness and add controllable **numerical damping** to suppress spurious high-frequency joint chatter — the workhorses of commercial MBS codes.
- **Symplectic/variational integrators** conserve energy over long horizons — valuable for orbital and conservative mechanisms.

A practical rule: if your fastest physical period is $\tau$, an explicit method needs steps well below $\tau$; an implicit method does not. Below, the same constrained pendulum integrated with `Radau` stays on the constraint far longer than `RK45` at the same tolerance.

```python
import numpy as np
from scipy.integrate import solve_ivp
g, L = 9.81, 1.0                       # pendulum as 1-DOF ODE for clarity
def rhs(t, y): return [y[1], -(g/L)*np.sin(y[0])]
y0 = [np.deg2rad(80), 0.0]
for method in ("RK45", "Radau"):
    s = solve_ivp(rhs, [0, 20], y0, method=method, rtol=1e-8, atol=1e-9)
    print(f"{method:6s}: steps={s.t.size}, theta_end={np.rad2deg(s.y[0,-1]):.2f} deg")
```

```plot
{"title": "Explicit step size shrinks with stiffness", "xLabel": "stiffness ratio (fast/slow)", "yLabel": "stable explicit steps (rel.)", "xRange": [1,20], "yRange": [0,20], "grid": true, "functions": [{"expr": "x", "label": "explicit cost ~ stiffness", "color": "#dc2626"}, {"expr": "1 + 0*x", "label": "implicit (stiff) ~ flat", "color": "#16a34a"}]}
```

**Next:** simulate real mechanisms, vehicles and robots in the Advanced course.
""",
        ),
        _quiz(),
    ),
)


_ADVANCED = SeedCourse(
    slug="multibody-dynamics-advanced",
    title="Multibody Dynamics & Simulation — Advanced",
    description=(
        "State-of-the-art and applied multibody simulation: recursive O(n) robot "
        "dynamics, flexible bodies, contact and friction, vehicle dynamics, and the "
        "modern frontier — differentiable simulation, trajectory optimization and "
        "machine learning for fast, learnable multibody models."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Recursive O(n) algorithms for robot dynamics",
            "14 min",
            r"""
# Recursive O(n) algorithms for robot dynamics

For open kinematic chains (most robots), forming and inverting the dense KKT system is wasteful. **Recursive** algorithms exploit the tree structure to compute dynamics in $O(n)$ time. The **Recursive Newton-Euler Algorithm (RNEA)** solves *inverse* dynamics — given $\mathbf q,\dot{\mathbf q},\ddot{\mathbf q}$, find joint torques $\boldsymbol\tau$ — by a forward sweep propagating velocities/accelerations from base to tip and a backward sweep propagating forces from tip to base.

The companion **Articulated-Body Algorithm (ABA)** solves *forward* dynamics — given torques, find $\ddot{\mathbf q}$ — also in $O(n)$. Together they underpin the manipulator equation
$$\mathbf M(\mathbf q)\ddot{\mathbf q} + \mathbf C(\mathbf q,\dot{\mathbf q})\dot{\mathbf q} + \mathbf g(\mathbf q) = \boldsymbol\tau,$$
with $\mathbf C$ the Coriolis/centrifugal term and $\mathbf g$ gravity. Libraries Pinocchio, RBDL and MuJoCo implement these with spatial (6D) vector algebra (Featherstone).

```python
import numpy as np
# 2R planar arm: compute torques via the manipulator equation (RNEA result).
def manip_eq(q, qd, qdd, m=(1.0, 1.0), l=(1.0, 1.0), g=9.81):
    (t1, t2), (m1, m2), (l1, l2) = q, m, l
    a = m2*l1*l2
    M = np.array([[m1*l1**2 + m2*(l1**2 + l2**2 + 2*l1*l2*np.cos(t2)),
                   m2*(l2**2 + l1*l2*np.cos(t2))],
                  [m2*(l2**2 + l1*l2*np.cos(t2)), m2*l2**2]])
    C = np.array([-a*np.sin(t2)*(2*qd[0]*qd[1] + qd[1]**2),
                   a*np.sin(t2)*qd[0]**2])
    G = np.array([(m1+m2)*g*l1*np.cos(t1) + m2*g*l2*np.cos(t1+t2),
                  m2*g*l2*np.cos(t1+t2)])
    return M @ qdd + C + G
print("tau:", np.round(manip_eq([0.3, 0.5], [0.1, -0.2], [0.0, 0.0]), 3))
```

```plot
{"title": "Cost of dynamics: dense KKT vs recursive", "xLabel": "number of bodies n", "yLabel": "relative work", "xRange": [1,12], "yRange": [0,120], "grid": true, "functions": [{"expr": "x^3/12", "label": "dense ~ O(n^3)", "color": "#dc2626"}, {"expr": "x", "label": "recursive ~ O(n)", "color": "#16a34a"}]}
```

**Next:** bodies that bend — flexible multibody dynamics.
""",
        ),
        _t(
            "Flexible multibody dynamics",
            "13 min",
            r"""
# Flexible multibody dynamics

Real links bend; lightweight robots, wind-turbine blades and spacecraft booms must model **flexibility**. The dominant method is the **floating frame of reference (FFR)** formulation: a body's motion splits into large rigid-body motion of a moving frame plus small elastic deformation expressed in that frame, usually via a reduced set of **modal coordinates** (a Craig-Bampton component-mode synthesis from an FE model).

For large deformation (cables, very slender beams), the **Absolute Nodal Coordinate Formulation (ANCF)** uses global position and slope coordinates and yields a *constant* mass matrix at the cost of nonlinear elastic forces. The trade-off: FFR is efficient for small strain and high frequency content; ANCF excels at geometric nonlinearity.

Flexibility adds many stiff, lightly damped modes — exactly the case demanding the implicit, numerically-damped integrators (generalized-$\alpha$, HHT) from the Intermediate course.

```mermaid
flowchart LR
  A[Flexible body] --> B[FFR: rigid frame + modal coords]
  A --> C[ANCF: absolute nodal pos + slopes]
  B --> D[Reduced modes from FE - Craig-Bampton]
  C --> E[Constant mass matrix, nonlinear elastic forces]
  D --> F[Needs implicit damped integrator]
  E --> F
```

```plot
{"title": "Tip response: rigid vs first elastic mode added", "xLabel": "t (s)", "yLabel": "tip deflection (norm.)", "xRange": [0,10], "yRange": [-1,1], "grid": true, "functions": [{"expr": "0.6*cos(0.8*x)", "label": "rigid-body sway", "color": "#2563eb"}, {"expr": "0.6*cos(0.8*x) + 0.3*exp(-0.2*x)*cos(4*x)", "label": "with elastic mode", "color": "#dc2626"}]}
```

**Next:** what happens when bodies touch — contact and friction.
""",
        ),
        _t(
            "Contact, impact and friction",
            "13 min",
            r"""
# Contact, impact and friction

Contact turns smooth dynamics into a **non-smooth** problem. Two families dominate. **Penalty (compliant) contact** treats interpenetration $\delta$ as a stiff spring-damper, e.g. the Hunt-Crossley law $F_n = k\delta^{p} + b\,\delta^{p}\dot\delta$ that, unlike Kelvin-Voigt, keeps contact force non-negative and models hysteretic energy loss. Easy to integrate but stiff, so it forces small steps.

**Complementarity / rigid contact** enforces the **Signorini condition** $0\le F_n \perp \delta \ge 0$ (force *or* gap is zero, never both) together with the **Coulomb friction cone** $\|\mathbf F_t\|\le\mu F_n$. Solved per step as a **Linear Complementarity Problem (LCP)** or its convex relaxation — the basis of MuJoCo, Bullet and Drake's contact solvers. Impacts use a restitution law $\dot\delta^+ = -e\,\dot\delta^-$.

Friction is the hard part: the cone is non-smooth and the LCP can lack solutions (Painleve paradox), which is why production engines use regularized or convex-relaxed friction. The friction coefficient μ (mu) is the single most influential parameter — small changes flip a body between sticking and sliding, and the resulting tangential force scales as μ × F_n.

```python
import numpy as np
def hunt_crossley(delta, ddelta, k=1e5, b=50.0, p=1.5):
    if delta <= 0:                      # separated: no contact force
        return 0.0
    return max(0.0, k*delta**p + b*delta**p*ddelta)   # non-negative normal force
print("Fn:", round(hunt_crossley(1e-3, -0.2), 3), "N")
# Coulomb cone check
mu, Fn, Ft = 0.6, 120.0, np.array([40.0, 30.0])
print("sliding?" , np.linalg.norm(Ft) > mu*Fn)
```

```plot
{"title": "Normal contact force vs penetration (Hunt-Crossley)", "xLabel": "penetration delta (mm)", "yLabel": "F_n (N)", "xRange": [0,2], "yRange": [0,300], "grid": true, "functions": [{"expr": "100*x^1.5", "label": "F_n = k delta^p", "color": "#2563eb"}]}
```

**Next:** a flagship application — vehicle dynamics.
""",
        ),
        _t(
            "Application: vehicle dynamics simulation",
            "13 min",
            r"""
# Application: vehicle dynamics simulation

A full vehicle model is a multibody system: sprung mass (chassis), four unsprung masses (wheels), suspension links, springs/dampers and tires. For handling studies engineers often start with the **bicycle model**, lumping each axle into one wheel. Its linear single-track equations in lateral velocity $v$ and yaw rate $r$ are
$$m(\dot v + Ur) = F_{yf}+F_{yr},\qquad I_z\dot r = a F_{yf} - b F_{yr},$$
with tire lateral forces $F_y = -C_\alpha\,\alpha$ from slip angle $\alpha$ and cornering stiffness $C_\alpha$. This predicts **understeer/oversteer** and the critical speed.

Full multibody vehicle models (Adams/Car, Simscape, CarMaker) add 3D suspension kinematics, anti-roll bars, compliant bushings and the nonlinear **Pacejka "Magic Formula"** tire, then run ride, handling and durability events.

```python
import numpy as np
from scipy.integrate import solve_ivp
m, Iz, a, b, Caf, Car, U = 1500., 2250., 1.2, 1.6, 80e3, 80e3, 25.
def bicycle(t, x, delta):
    v, r = x
    af = (v + a*r)/U - delta            # front slip angle
    ar = (v - b*r)/U                    # rear slip angle
    Fyf, Fyr = -Caf*af, -Car*ar
    return [(Fyf + Fyr)/m - U*r, (a*Fyf - b*Fyr)/Iz]
sol = solve_ivp(bicycle, [0, 4], [0, 0], args=(np.deg2rad(2),), max_step=0.01)
print(f"steady yaw rate {sol.y[1,-1]:.3f} rad/s")
```

```plot
{"title": "Yaw-rate step response to a steer input", "xLabel": "t (s)", "yLabel": "yaw rate (norm.)", "xRange": [0,4], "yRange": [0,1.2], "grid": true, "functions": [{"expr": "1 - exp(-2.5*x)", "label": "first-order rise", "color": "#16a34a"}]}
```

**Next:** make the simulator differentiable and optimize through it.
""",
        ),
        _t(
            "Differentiable simulation and trajectory optimization",
            "14 min",
            r"""
# Differentiable simulation and trajectory optimization

If you can compute gradients *through* a multibody simulation, you can use gradient-based optimization for design and control. **Differentiable simulators** (Drake's AutoDiff, Brax, MuJoCo MJX, Tiny Differentiable Simulator) propagate analytic or automatic derivatives of the dynamics, giving $\partial \ddot{\mathbf q}/\partial(\mathbf q,\dot{\mathbf q},\boldsymbol\tau)$ cheaply.

**Trajectory optimization** then finds an input history minimizing a cost subject to the dynamics as constraints. **Direct collocation** discretizes states and controls at knot points and enforces the equations of motion as defect constraints, handing the large sparse NLP to an SQP/interior-point solver (IPOPT, SNOPT). The result is energy-optimal robot motions, gait trajectories and minimum-time maneuvers. Contact makes it a hybrid/contact-implicit problem — an active research frontier.

```python
import numpy as np
from scipy.optimize import minimize
# Minimum-effort move of a unit mass from 0 to 1 in N steps (direct transcription).
N, dt = 20, 0.1
def unpack(z): return z[:N], z[N:2*N+1]          # controls u, positions x (vel implicit)
def cost(z): u, _ = unpack(z); return dt*np.sum(u**2)
def dyn(z):                                       # x_{k+1} = x_k + dt*v, v from double integ.
    u, x = unpack(z); v = np.cumsum(u)*dt
    return np.diff(x) - dt*v[:-1]                 # defect = 0
z0 = np.zeros(3*N+1)
res = minimize(cost, z0, constraints=[{"type": "eq", "fun": dyn},
              {"type": "eq", "fun": lambda z: [unpack(z)[1][0], unpack(z)[1][-1]-1]}])
print("optimal effort:", round(res.fun, 4), "converged:", res.success)
```

```plot
{"title": "Optimizer cost convergence", "xLabel": "iteration", "yLabel": "objective (norm.)", "xRange": [0,12], "yRange": [0,1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "SQP convergence", "color": "#dc2626"}]}
```

**Next:** learning surrogate and hybrid dynamics models.
""",
        ),
        _t(
            "Machine learning for multibody dynamics",
            "13 min",
            r"""
# Machine learning for multibody dynamics

High-fidelity multibody runs are expensive, so ML increasingly augments or replaces parts of the pipeline. Three productive patterns:

- **Surrogate / reduced-order models:** train a neural net or Gaussian process to map design parameters to responses (peak loads, ride metrics), then optimize on the cheap surrogate with Bayesian optimization — only validating the best candidates in the full simulator.
- **Physics-informed and structured nets:** **Lagrangian/Hamiltonian Neural Networks** and **Deep Lagrangian Networks** learn the mass matrix and potential so the predicted dynamics *conserve energy* and respect structure, generalizing far better than a black box. **Graph Network Simulators** treat bodies as nodes and joints as edges, learning to roll the system forward.
- **Sim-to-real and residual learning:** learn the *residual* between a fast analytic model and measured data to capture unmodeled friction/compliance — then deploy in model-based control or reinforcement learning, where a fast differentiable simulator is the training environment.

The throughline of the whole track: a good physical model (constraints, EoM, integrators) plus modern computation (recursive algorithms, differentiable simulation, ML) lets you simulate, design and control mechanisms, vehicles and robots end to end.

```python
import numpy as np
# Sketch of a structured (Lagrangian-style) prediction: M(q) from a learned net,
# then accel = M^{-1} (tau - C qd - g). Here a tiny stand-in for the learned M.
def learned_M(q, w):                              # SPD by construction: L L^T
    L = np.array([[w[0], 0.0], [w[1], w[2]]]) * (1 + 0.1*np.cos(q[0]))
    return L @ L.T
def forward(q, qd, tau, w, C=np.zeros(2), g=np.array([0.0, 9.81])):
    return np.linalg.solve(learned_M(q, w), tau - C - g)
print("qddot:", np.round(forward(np.array([0.2, 0.0]), np.zeros(2),
      np.array([1.0, 0.0]), w=np.array([1.0, 0.2, 0.9])), 3))
```

```plot
{"title": "Surrogate speedup: full sim vs learned model", "xLabel": "design evaluations", "yLabel": "cumulative wall time (norm.)", "xRange": [0,50], "yRange": [0,50], "grid": true, "functions": [{"expr": "x", "label": "full multibody sim", "color": "#dc2626"}, {"expr": "0.05*x + 1", "label": "learned surrogate", "color": "#16a34a"}]}
```

**Next:** pair this with the Robotics, Control and Engineering Dynamics tracks.
""",
        ),
        _quiz(),
    ),
)


MULTIBODY_DYNAMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MULTIBODY_DYNAMICS_COURSES"]
