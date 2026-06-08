"""Curated Physics track: Basics → Intermediate → Advanced, building from
scratch up to the equations of motion of a quadrotor derived three ways
(Newton–Euler, Lagrangian, Hamiltonian).

Grounded in the user's Obsidian Physics + Quadcopters vault (notation matches
`Physics/Applications/Quadcopter Dynamics`). Lessons are `text` with LaTeX math
($$ … $$ / $ … $, rendered by the lesson Markdown view); the Advanced capstone
is a runnable Python lesson that integrates the EOM.
"""

# Lesson prose intentionally uses typographic characters (en dashes, ×, →, ≈)
# and physics/LaTeX notation — exempt this content file from the
# ambiguous-character lints.
# ruff: noqa: RUF001, RUF002, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Physics — Basics ─────────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="physics-basics",
    title="Physics — Basics",
    description=(
        "Mechanics from scratch: how things move (kinematics), why they move "
        "(Newton's laws and forces), and the bookkeeping of energy and momentum. "
        "No prior physics assumed — this is the foundation the whole track builds on."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Motion: position, velocity, acceleration",
            "10 min",
            """\
# Motion: position, velocity, acceleration

Physics starts by describing **how things move**, before asking *why*. Three
quantities do almost all the work.

- **Position** $x(t)$ — where something is, as a function of time.
- **Velocity** $v = \\dfrac{dx}{dt}$ — how fast position changes (the slope of $x$ vs $t$).
- **Acceleration** $a = \\dfrac{dv}{dt} = \\dfrac{d^2x}{dt^2}$ — how fast velocity changes.

The dot is shorthand for a time derivative: $\\dot{x} = v$, $\\ddot{x} = a$.
You'll see dots everywhere once we hit dynamics.

## Constant acceleration

If $a$ is constant (e.g. gravity near the ground, $a = -g$), integrating gives
the equations everyone memorises:

$$v(t) = v_0 + a\\,t, \\qquad x(t) = x_0 + v_0 t + \\tfrac{1}{2} a\\,t^2.$$

**Example.** Drop a ball ($v_0 = 0$, $a = -g = -9.81\\,\\text{m/s}^2$). After
$t = 1\\,\\text{s}$ it has fallen $\\tfrac{1}{2}g t^2 \\approx 4.9\\,\\text{m}$.

## Vectors

In 2D/3D, position/velocity/acceleration are **vectors** — they have direction.
$\\vec{r} = (x, y, z)$, and each component obeys the rules above independently.
A car turning at constant speed is still *accelerating*, because the direction
of $\\vec{v}$ changes.

**Next:** what makes velocity change — forces.
""",
        ),
        _t(
            "Forces & Newton's laws",
            "11 min",
            """\
# Forces & Newton's laws

A **force** is a push or pull (a vector, in newtons, N). Newton's three laws
tie forces to motion.

1. **Inertia.** With no net force, velocity stays constant (rest stays at rest).
2. **$\\vec{F} = m\\vec{a}$.** Net force = mass × acceleration. This is *the*
   equation of dynamics.
3. **Action–reaction.** Every force has an equal and opposite partner.

## Free-body diagrams

The key skill: draw the object, draw every force on it, add them as vectors,
then apply $\\sum \\vec{F} = m\\vec{a}$ per axis.

Common forces:
- **Weight** $\\vec{W} = m\\vec{g}$ (down, $g \\approx 9.81\\,\\text{m/s}^2$).
- **Normal** $N$ — a surface pushing back, perpendicular to it.
- **Friction** $f \\le \\mu N$ — opposes sliding.
- **Tension / thrust** — a rope pulls, a rotor pushes.

**Example (hover).** A drone of mass $m$ hovers when rotor thrust balances
weight: $T - mg = m\\,a$. Hovering means $a = 0$, so $T = mg$. Thrust above $mg$
makes it climb — that's the whole idea behind the quadrotor course later.

```text
        T (thrust, up)
        ↑
      [ drone ]
        ↓
        mg (weight, down)
```

**Next:** energy and momentum — two powerful shortcuts.
""",
        ),
        _t(
            "Energy & momentum",
            "10 min",
            """\
# Energy & momentum

Forces tell you *instantaneous* acceleration; **energy** and **momentum** are
conserved quantities that often let you skip the play-by-play.

## Work and kinetic energy

**Work** is force applied over a distance: $W = \\vec{F}\\cdot\\vec{d}$. It changes
**kinetic energy** $K = \\tfrac{1}{2} m v^2$:

$$W_{\\text{net}} = \\Delta K = \\tfrac{1}{2} m v_f^2 - \\tfrac{1}{2} m v_i^2.$$

## Potential energy & conservation

Near Earth, gravitational **potential energy** is $U = m g h$. With no friction,
the total $E = K + U$ is **conserved**:

$$\\tfrac{1}{2} m v^2 + m g h = \\text{constant}.$$

**Example.** Drop from height $h$: all $U$ becomes $K$, so
$v = \\sqrt{2gh}$ — no need to track time.

> This energy view (kinetic minus potential) is exactly what the **Lagrangian**
> method generalises later — so this idea reappears at the top of the track.

## Momentum

**Momentum** $\\vec{p} = m\\vec{v}$. Newton's 2nd law is really
$\\vec{F} = \\dfrac{d\\vec{p}}{dt}$, and with no external force, total momentum is
conserved (collisions, rocket/propeller thrust). The rotational cousin —
**angular momentum** — drives the next course.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Physics — Intermediate ───────────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="physics-intermediate",
    title="Physics — Intermediate",
    description=(
        "Rotation and the math of dynamics: angular motion and torque, simple "
        "harmonic motion, the calculus you actually need (derivatives, partials, "
        "gradients), and rigid bodies in 3D with rotating frames — the Newton–Euler "
        "toolkit for the quadrotor."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Rotational motion & torque",
            "11 min",
            """\
# Rotational motion & torque

Every linear idea has a rotational twin — just swap the symbols.

| Linear | Rotational |
|--------|------------|
| position $x$ | angle $\\theta$ |
| velocity $v = \\dot{x}$ | angular velocity $\\omega = \\dot{\\theta}$ |
| acceleration $a$ | angular accel $\\alpha = \\dot{\\omega}$ |
| mass $m$ | moment of inertia $I$ |
| force $F$ | torque $\\tau$ |
| $F = ma$ | $\\tau = I\\alpha$ |

## Torque

**Torque** is the rotational push: $\\vec{\\tau} = \\vec{r} \\times \\vec{F}$ —
force times lever arm. A rotor at distance $l$ from the centre producing thrust
$T$ creates a torque $\\tau = l\\,T$ that rolls/pitches the craft.

## Moment of inertia

$I$ is rotational "mass" — how hard it is to spin something. It depends on how
mass is distributed: $I = \\sum m_i r_i^2$. Mass far from the axis (long arms)
means large $I$, sluggish rotation.

## Angular momentum

$\\vec{L} = I\\vec{\\omega}$, and $\\vec{\\tau} = \\dfrac{d\\vec{L}}{dt}$. With no
torque, $\\vec{L}$ is conserved — why a spinning rotor resists tilting
(gyroscopic stiffness), a real effect in drones.

**Next:** oscillations and the calculus tools dynamics needs.
""",
        ),
        _t(
            "Oscillations & the calculus you need",
            "11 min",
            """\
# Oscillations & the calculus you need

## Simple harmonic motion

A mass on a spring feels a restoring force $F = -k x$. Newton's law gives a
**differential equation** — an equation relating a function to its derivatives:

$$m\\ddot{x} = -k x \\;\\;\\Rightarrow\\;\\; \\ddot{x} + \\omega^2 x = 0, \\quad \\omega = \\sqrt{k/m}.$$

Its solution oscillates: $x(t) = A\\cos(\\omega t + \\varphi)$. Dynamics is mostly
the art of writing down such equations (the *equations of motion*) and solving
or simulating them.

## The calculus toolkit

You need three ideas for the rest of the track:

- **Derivative** $\\dfrac{df}{dt}$ — rate of change (you've used $\\dot{x}$, $\\ddot{x}$).
- **Partial derivative** $\\dfrac{\\partial f}{\\partial x}$ — rate of change in
  *one* variable, holding the others fixed. The Lagrangian method is built from
  these.
- **Gradient** $\\nabla f = \\big(\\tfrac{\\partial f}{\\partial x}, \\tfrac{\\partial f}{\\partial y}, \\tfrac{\\partial f}{\\partial z}\\big)$
  — the direction of steepest increase; a force is often $\\vec{F} = -\\nabla U$.

**Example.** For $U = mgz$, $\\;\\vec{F} = -\\nabla U = (0,0,-mg)$ — gravity, recovered.

**Next:** rotation in 3D, frames, and the Newton–Euler equations.
""",
        ),
        _t(
            "Rigid bodies in 3D: frames & rotations",
            "13 min",
            """\
# Rigid bodies in 3D: frames & rotations

A drone isn't a point — it's a **rigid body** that translates *and* rotates. To
describe it we use two reference frames.

```mermaid
flowchart LR
  W["World / Earth frame\\n(fixed, e.g. NED)"] -- "rotation R(φ,θ,ψ)" --> B["Body frame\\n(rides with the craft)"]
```

- **World frame** (inertial) — fixed to the ground. Position lives here.
- **Body frame** — attached to the craft; its axes are forward/right/down.
  Thrust, inertia, and the gyros/accelerometers live here.

## Rotation matrices & Euler angles

The orientation is captured by **roll, pitch, yaw** $(\\phi, \\theta, \\psi)$ and a
**rotation matrix** $\\mathbf{R}$ that maps body vectors to world vectors:
$\\vec{v}_{\\text{world}} = \\mathbf{R}\\,\\vec{v}_{\\text{body}}$. $\\mathbf{R}$ is
orthogonal ($\\mathbf{R}^{-1} = \\mathbf{R}^{T}$).

## Angular velocity and the cross product

Body angular velocity is $\\vec{\\omega} = (p, q, r)$. A subtlety that defines 3D
dynamics: in a **rotating** frame, the rate of change of any vector picks up a
$\\vec{\\omega} \\times (\\cdot)$ term.

## Newton–Euler equations

Putting it together, a rigid body obeys two vector equations — translation
(Newton) and rotation (Euler):

$$m\\,\\dot{\\vec{v}} + \\vec{\\omega}\\times m\\vec{v} = \\vec{F}, \\qquad
\\mathbf{I}\\,\\dot{\\vec{\\omega}} + \\vec{\\omega}\\times \\mathbf{I}\\vec{\\omega} = \\vec{\\tau}.$$

Those two lines, written in the body frame, are the entire skeleton of the
quadrotor model. **Next course:** fill them in for a quadrotor — three ways.
""",
        ),
        _quiz(),
    ),
)

# ── Physics — Advanced: quadrotor EOM ────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="physics-quadrotor-dynamics",
    title="Physics — Equations of Motion of a Quadrotor",
    description=(
        "The capstone: model a quadrotor and derive its full equations of motion "
        "THREE ways — Newton–Euler, Lagrangian, and Hamiltonian — then integrate "
        "them in code. Assumes the Basics + Intermediate Physics courses."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The quadrotor model: frames, state & inputs",
            "12 min",
            """\
# The quadrotor model: frames, state & inputs

Before any derivation, pin down the model — frames, what the craft *is*, and
what we can control.

## Frames

- **Earth frame** (inertial), NED: $x$ north, $y$ east, $z$ **down**.
- **Body frame**, riding the craft: $x_B$ forward, $y_B$ right, $z_B$ down.

## State (12 numbers)

$$\\mathbf{x} = (\\underbrace{x,y,z}_{\\text{position (Earth)}},\\;
\\underbrace{\\phi,\\theta,\\psi}_{\\text{roll,pitch,yaw}},\\;
\\underbrace{u,v,w}_{\\text{velocity (body)}},\\;
\\underbrace{p,q,r}_{\\text{angular vel.\\ (body)}}).$$

## Inputs: from 4 motors to thrust + 3 moments

Each rotor spins at $\\Omega_i$ and makes thrust $T_i = k_T\\,\\Omega_i^2$ and a
reaction torque $\\propto k_Q\\,\\Omega_i^2$. The four combine into **one thrust**
(along $-z_B$, "up") and **three moments**:

$$\\begin{bmatrix} T \\\\ \\tau_\\phi \\\\ \\tau_\\theta \\\\ \\tau_\\psi \\end{bmatrix}
= \\underbrace{\\begin{bmatrix} k_T & k_T & k_T & k_T \\\\ -lk_T & lk_T & lk_T & -lk_T \\\\ lk_T & lk_T & -lk_T & -lk_T \\\\ k_Q & -k_Q & k_Q & -k_Q \\end{bmatrix}}_{\\text{mixer}}
\\begin{bmatrix} \\Omega_1^2 \\\\ \\Omega_2^2 \\\\ \\Omega_3^2 \\\\ \\Omega_4^2 \\end{bmatrix}.$$

The flight controller inverts this mixer to turn a desired $(T, \\tau_\\phi, \\tau_\\theta, \\tau_\\psi)$
into motor commands. From here on we treat $T$ and $\\vec{\\tau} = (\\tau_\\phi, \\tau_\\theta, \\tau_\\psi)$
as our inputs.

**Next:** the Newton–Euler equations of motion.
""",
        ),
        _t(
            "Newton–Euler equations of motion",
            "14 min",
            """\
# Newton–Euler equations of motion

We apply the two rigid-body equations from the last course, in the **body
frame**.

## Forces

- **Thrust** acts up along the body: $\\vec{F}_T = (0,0,-T)$.
- **Gravity** is simple in the Earth frame but must be rotated into the body
  frame: $\\vec{F}_g = m\\mathbf{R}^{T}(0,0,g)^{T} = m(-g\\sin\\theta,\\; g\\cos\\theta\\sin\\phi,\\; g\\cos\\theta\\cos\\phi)$.

## Translational dynamics (Newton, body frame)

$$m\\,\\dot{\\vec{v}} + \\vec{\\omega}\\times m\\vec{v} = \\vec{F}_T + \\vec{F}_g$$

Component-by-component, with $\\vec{v}=(u,v,w)$, $\\vec{\\omega}=(p,q,r)$:

$$m\\dot{u} = -mg\\sin\\theta + m(rv - qw)$$
$$m\\dot{v} = \\;\\;mg\\cos\\theta\\sin\\phi + m(pw - ru)$$
$$m\\dot{w} = -T + mg\\cos\\theta\\cos\\phi + m(qu - pv)$$

The $\\vec{\\omega}\\times m\\vec{v}$ terms are the "fictitious" Coriolis/centripetal
forces you get for writing Newton's law in a rotating frame.

## Rotational dynamics (Euler, body frame)

$$\\mathbf{I}\\,\\dot{\\vec{\\omega}} + \\vec{\\omega}\\times\\mathbf{I}\\vec{\\omega} = \\vec{\\tau}.$$

With a diagonal inertia $\\mathbf{I}=\\mathrm{diag}(I_{xx},I_{yy},I_{zz})$:

$$I_{xx}\\dot{p} = \\tau_\\phi + (I_{yy}-I_{zz})\\,qr$$
$$I_{yy}\\dot{q} = \\tau_\\theta + (I_{zz}-I_{xx})\\,pr$$
$$I_{zz}\\dot{r} = \\tau_\\psi + (I_{xx}-I_{yy})\\,pq$$

## Kinematics (tie body rates back to the world)

$$\\begin{bmatrix}\\dot x\\\\\\dot y\\\\\\dot z\\end{bmatrix} = \\mathbf{R}\\begin{bmatrix}u\\\\v\\\\w\\end{bmatrix}, \\qquad
\\begin{bmatrix}\\dot\\phi\\\\\\dot\\theta\\\\\\dot\\psi\\end{bmatrix} =
\\begin{bmatrix}1 & \\sin\\phi\\tan\\theta & \\cos\\phi\\tan\\theta\\\\0 & \\cos\\phi & -\\sin\\phi\\\\0 & \\sin\\phi\\sec\\theta & \\cos\\phi\\sec\\theta\\end{bmatrix}\\begin{bmatrix}p\\\\q\\\\r\\end{bmatrix}.$$

## Small-angle (hover) model

Near hover ($\\phi,\\theta\\approx 0$) it decouples into the form used for control:

$$m\\ddot z = mg - T,\\qquad I_{xx}\\ddot\\phi = \\tau_\\phi,\\quad I_{yy}\\ddot\\theta = \\tau_\\theta,\\quad I_{zz}\\ddot\\psi = \\tau_\\psi.$$

**Next:** the same equations from energy — the Lagrangian.
""",
        ),
        _t(
            "The Lagrangian derivation",
            "14 min",
            """\
# The Lagrangian derivation

Newton–Euler tracks forces and that pesky $\\vec\\omega\\times$ term. The
**Lagrangian** method instead uses **energy** and generalised coordinates — and
the constraint terms appear automatically.

## The recipe

1. Pick **generalised coordinates** $\\mathbf{q}$. For a quadrotor:
   $\\mathbf{q} = (x, y, z, \\phi, \\theta, \\psi)$.
2. Write the **kinetic energy** $T_{\\text{kin}}$ and **potential energy** $V$.
3. Form the **Lagrangian** $\\mathcal{L} = T_{\\text{kin}} - V$.
4. Apply the **Euler–Lagrange equation** for each coordinate $q_i$:

$$\\frac{d}{dt}\\!\\left(\\frac{\\partial \\mathcal{L}}{\\partial \\dot q_i}\\right) - \\frac{\\partial \\mathcal{L}}{\\partial q_i} = Q_i,$$

where $Q_i$ is the generalised (non-conservative) force/torque on $q_i$ —
here, thrust and rotor moments.

## Energies for the quadrotor

Translational + rotational kinetic energy, gravitational potential ($z$ down):

$$T_{\\text{kin}} = \\tfrac{1}{2} m\\,(\\dot x^2 + \\dot y^2 + \\dot z^2) + \\tfrac{1}{2}\\,\\vec\\omega^{T}\\mathbf{I}\\,\\vec\\omega, \\qquad V = -m g z.$$

## Translation

$\\mathcal{L}$ depends on $\\dot x,\\dot y,\\dot z$ and (through $V$) on $z$:

$$\\frac{d}{dt}(m\\dot x) = F_x,\\quad \\frac{d}{dt}(m\\dot y) = F_y,\\quad \\frac{d}{dt}(m\\dot z) + mg = F_z,$$

i.e. $m\\ddot{\\vec r} = \\mathbf{R}(0,0,-T)^T + (0,0,mg)^T$ — **the same translational
EOM**, now in world coordinates.

## Rotation

Carrying the attitude kinetic energy through Euler–Lagrange reproduces, after
simplification, Euler's equations:

$$\\mathbf{I}\\dot{\\vec\\omega} + \\vec\\omega\\times\\mathbf{I}\\vec\\omega = \\vec\\tau.$$

The gyroscopic $\\vec\\omega\\times\\mathbf{I}\\vec\\omega$ term — added "by hand" in
Newton–Euler — here **falls out of the derivatives**. That's the Lagrangian
payoff: no free-body diagrams, no fictitious forces, just energy.

**Next:** the Hamiltonian view.
""",
        ),
        _t(
            "The Hamiltonian derivation",
            "13 min",
            """\
# The Hamiltonian derivation

The **Hamiltonian** reformulates the same physics in terms of **momenta**
instead of velocities — turning $n$ second-order equations into $2n$
first-order ones, which is exactly the state-space form a simulator or
controller wants.

## From Lagrangian to Hamiltonian

1. Define the **generalised momentum** conjugate to each coordinate:

$$p_i = \\frac{\\partial \\mathcal{L}}{\\partial \\dot q_i}.$$

For translation this is ordinary momentum $p_x = m\\dot x$; for rotation it's
angular momentum.

2. **Legendre transform** to get the Hamiltonian (for our system, the total
energy):

$$\\mathcal{H}(\\mathbf{q}, \\mathbf{p}) = \\sum_i p_i \\dot q_i - \\mathcal{L} = T_{\\text{kin}} + V.$$

3. The dynamics are **Hamilton's equations**:

$$\\dot q_i = \\frac{\\partial \\mathcal{H}}{\\partial p_i}, \\qquad
\\dot p_i = -\\frac{\\partial \\mathcal{H}}{\\partial q_i} + Q_i.$$

## For the quadrotor's vertical axis (illustration)

With $\\mathcal{H} = \\dfrac{p_z^2}{2m} - mgz$ and thrust as the applied force:

$$\\dot z = \\frac{\\partial \\mathcal{H}}{\\partial p_z} = \\frac{p_z}{m}, \\qquad
\\dot p_z = -\\frac{\\partial \\mathcal{H}}{\\partial z} + F_z = mg - T.$$

Together: $m\\ddot z = mg - T$ — **identical** to Newton and Lagrange.

## Why three methods?

| Method | Works with | Best when |
|--------|-----------|-----------|
| **Newton–Euler** | forces & torques | building physical intuition, sensors in body frame |
| **Lagrangian** | energies $T-V$ | complex/constrained systems; constraint terms auto-appear |
| **Hamiltonian** | energies & momenta | state-space form, controls, energy methods, numerics |

All three describe the **same quadrotor** and yield the **same equations of
motion** — they're different languages for one truth.

**Next:** integrate the equations in code.
""",
        ),
        _code(
            "Simulate it: integrate the EOM",
            "12 min",
            """\
# Run the quadrotor equations of motion yourself.
# We integrate the (decoupled hover) Newton-Euler model with simple Euler steps:
#   vertical:  m * w_dot = T - m*g       (w = climb rate, up positive)
#   pitch:     Ixx * q_dot = tau         (q = pitch rate)
# Identical EOM whether you derived it via Newton, Lagrange, or Hamilton.

m = 1.0       # mass (kg)
g = 9.81      # gravity (m/s^2)
Ixx = 0.01    # roll/pitch inertia (kg m^2)

T = m * g + 0.5   # thrust just above weight -> gentle climb
tau = 0.002       # small constant pitch moment (N m)
dt = 0.01         # timestep (s)

z = 0.0; w = 0.0          # altitude, vertical velocity
theta = 0.0; q = 0.0      # pitch angle (rad), pitch rate
for step in range(300):   # simulate 3 seconds
    w += ((T - m * g) / m) * dt   # Newton:  m*w_dot = T - m*g
    z += w * dt
    q += (tau / Ixx) * dt         # Euler:   Ixx*q_dot = tau
    theta += q * dt

print("after 3 s of flight:")
print("  altitude   =", round(z, 2), "m")
print("  climb rate =", round(w, 2), "m/s")
print("  pitch      =", round(theta * 57.2958, 1), "deg")

# Try it yourself:
#   1. Set T = m*g exactly -> it hovers (altitude stays ~0).
#   2. Set tau = 0 -> pitch stays level. Raise Ixx -> it pitches slower.
#   3. Lower dt to 0.001 for a more accurate integration.
""",
        ),
        _quiz(),
    ),
)


PHYSICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["PHYSICS_COURSES"]
