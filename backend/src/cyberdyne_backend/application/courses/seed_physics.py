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

```plot
{"title": "Dropped ball: distance fallen vs time", "xLabel": "t (s)", "yLabel": "fallen (m)", "xRange": [0, 2], "functions": [{"expr": "0.5*9.81*x^2", "label": "½ g t²"}]}
```

The curve steepens — that upward bend *is* the (constant) acceleration.

Press **Play** below and watch two balls leave the same start. The blue one
moves at *constant velocity* (equal steps), the red one *accelerates* (steps
grow). Drag the slider to scrub time by hand; the dashed lines are the trails.

```plot
{"title": "Constant velocity vs constant acceleration", "xLabel": "x (m)", "yLabel": "lane", "xRange": [0, 10], "yRange": [0, 3], "grid": true, "animate": {"param": "t", "range": [0, 5], "label": "time t (s)"}, "points": [{"xExpr": "1.6*t", "y": 2, "label": "constant v", "color": "#2563eb", "size": 7, "trail": true}, {"xExpr": "0.32*t^2", "y": 1, "label": "constant a", "color": "#dc2626", "size": 7, "trail": true}]}
```

Both reach $x = 8\\,\\text{m}$ at $t = 5\\,\\text{s}$, but the accelerating ball
starts behind and overtakes — the area under *its* velocity line is the same,
just shaped differently.

## A real throw: projectile motion

Now combine the two at once: a thrown ball moves at **constant velocity**
sideways *and* **constant acceleration** ($-g$) downward. Drag the launch speed
$v_0$ and the angle, then press **Play** — the dashed trail is the parabola of a
basketball shot, a soccer free-kick, or a water fountain.

```plot
{"title": "Throwing a ball (projectile)", "xLabel": "x (m)", "yLabel": "height (m)", "xRange": [0, 40], "yRange": [0, 16], "animate": {"param": "t", "range": [0, 3], "label": "time (s)"}, "controls": [{"name": "v0", "range": [5, 25], "value": 18, "label": "launch speed v₀ (m/s)"}, {"name": "ang", "range": [10, 80], "value": 45, "label": "angle α (°)"}], "points": [{"xExpr": "v0*cos(rad(ang))*t", "yExpr": "max(0, v0*sin(rad(ang))*t - 0.5*9.81*t^2)", "label": "ball", "color": "#dc2626", "size": 7, "trail": true}]}
```

An angle near **45°** gives the longest range (ignoring air) — which is why
long-jumpers and shot-putters launch at roughly that angle.

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

```vectors
{"title": "Free-body diagram: hovering drone", "equal": true, "xRange": [-2, 2], "yRange": [-1.6, 1.6], "vectors": [{"x": 0, "y": 1.2, "from": [0, 0], "label": "T (thrust)", "color": "#16a34a"}, {"x": 0, "y": -1.2, "from": [0, 0], "label": "mg (weight)", "color": "#dc2626"}]}
```

At hover the two arrows are equal and opposite, so the net force is zero.

## On a slope: when does it slide?

Park on a hill or drop a box on a ramp: gravity splits into a part **along** the
slope (which tries to slide it) and a part **into** the slope (held by the
normal force). Friction resists up to $\\mu N$, so it slides only when

$$mg\\sin\\alpha > \\mu\\,mg\\cos\\alpha \\;\\Leftrightarrow\\; \\tan\\alpha > \\mu.$$

Tilt the ramp and change the grip $\\mu$ — when the red *pull* arrow beats the
blue *friction* arrow, it lets go. (Drawn in the slope's own frame: across = down
the ramp, up = perpendicular.)

```vectors
{"title": "Will it slide? Block on a ramp (slope frame)", "equal": true, "xRange": [-1.4, 1.4], "yRange": [-1.4, 1.2], "controls": [{"name": "a", "range": [0, 60], "value": 25, "label": "ramp angle α (°)"}, {"name": "mu", "range": [0, 1], "value": 0.5, "label": "friction μ"}], "vectors": [{"xExpr": "-sin(rad(a))", "y": 0, "from": [0, 0], "label": "gravity ∥ (pull)", "color": "#dc2626"}, {"xExpr": "mu*cos(rad(a))", "y": 0, "from": [0, 0], "label": "max friction", "color": "#2563eb"}, {"x": 0, "yExpr": "cos(rad(a))", "from": [0, 0], "label": "normal N", "color": "#16a34a"}, {"xExpr": "-sin(rad(a))", "yExpr": "-cos(rad(a))", "from": [0, 0], "label": "weight mg", "color": "#6b7280"}]}
```

This is exactly why an icy road (small $\\mu$) is dangerous on even a gentle hill,
and why tyres and climbing shoes chase high friction.

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

A **pendulum** shows the trade live. At the ends of the swing the bob is all
potential; at the bottom it is all kinetic — the total stays fixed. Press
**Play** and watch the arc:

```plot
{"title": "Pendulum: a swing trading energy", "equal": true, "xRange": [-2, 2], "yRange": [-2, 0.3], "animate": {"param": "t", "range": [0, 6.283], "label": "time"}, "vectors": [{"xExpr": "1.6*sin(0.6*cos(t))", "yExpr": "-1.6*cos(0.6*cos(t))", "from": [0, 0], "color": "#6b7280", "label": "rod"}], "points": [{"xExpr": "1.6*sin(0.6*cos(t))", "yExpr": "-1.6*cos(0.6*cos(t))", "label": "bob", "color": "#dc2626", "size": 8, "trail": true}]}
```

The same energies, plotted against time, cross like a seesaw — when one peaks
the other vanishes, and they always sum to 1:

```plot
{"title": "Energy trade: KE ↔ PE (sums to a constant)", "xLabel": "time", "yLabel": "fraction of total E", "xRange": [0, 6.283], "yRange": [0, 1.05], "functions": [{"expr": "(1 - cos(0.6*cos(x))) / (1 - cos(0.6))", "label": "potential PE", "color": "#2563eb"}, {"expr": "1 - (1 - cos(0.6*cos(x))) / (1 - cos(0.6))", "label": "kinetic KE", "color": "#dc2626"}]}
```

A playground swing, a wrecking ball and a roller coaster all run on this trade:
height becomes speed and back again.

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

Its size is $\\tau = r\\,F\\sin\\varphi$: it grows with the **lever arm** and with
how **perpendicular** the push is. Lengthen the wrench or push at $90°$ and the
same hand force turns a much tighter bolt — try it:

```plot
{"title": "Torque = r × F: why a longer wrench helps", "equal": true, "xRange": [-0.5, 3], "yRange": [-1.8, 1.8], "controls": [{"name": "L", "range": [0.5, 2.5], "value": 1.5, "label": "lever arm L (m)"}, {"name": "ang", "range": [0, 180], "value": 90, "label": "force angle φ (°)"}], "vectors": [{"xExpr": "L", "y": 0, "from": [0, 0], "label": "lever r", "color": "#6b7280"}, {"fromExpr": ["L", "0"], "xExpr": "L + 0.9*cos(rad(ang))", "yExpr": "0.9*sin(rad(ang))", "label": "force F", "color": "#dc2626"}]}
```

A door handle sits far from the hinge for the same reason — push near the hinge
($r$ small) and it barely opens.

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

```plot
{"title": "Simple harmonic motion", "xLabel": "ω t (rad)", "yLabel": "x(t)", "xRange": [0, 12.566], "functions": [{"expr": "cos(x)", "label": "x = A cos(ω t)"}]}
```

Now make it move. The dot below is the mass on the spring; the curve is its
trace. Use the sliders to change the amplitude $A$ and angular frequency
$\\omega$ and press **Play** — bigger $\\omega$ means faster oscillation,
bigger $A$ a wider swing.

```plot
{"title": "Mass on a spring", "xLabel": "t (s)", "yLabel": "x", "xRange": [0, 10], "yRange": [-3, 3], "animate": {"param": "t", "range": [0, 10], "label": "time t (s)"}, "controls": [{"name": "A", "range": [0.5, 3], "value": 2, "label": "amplitude A"}, {"name": "w", "range": [0.3, 3], "value": 1.2, "label": "ω (rad/s)"}], "functions": [{"expr": "A*cos(w*x)", "label": "x(t) = A cos(ω t)", "color": "#9ca3af"}], "points": [{"xExpr": "t", "yExpr": "A*cos(w*t)", "label": "mass", "color": "#dc2626", "size": 7}]}
```

## Damping: real oscillators lose energy

A perfect spring would swing forever, but friction and dampers bleed energy, so
the amplitude **decays**: $x(t) = e^{-\\zeta t}\\cos(\\omega t)$. Raise the damping
$\\zeta$ and watch it settle faster. This is your **car's suspension**: too little
damping and you bounce for ages after a bump; engineers tune it near *critical*
so one pothole gives a single smooth dip and done.

```plot
{"title": "Damped oscillation: a car's suspension", "xLabel": "time (s)", "yLabel": "displacement", "xRange": [0, 10], "yRange": [-1.2, 1.2], "animate": {"param": "t", "range": [0, 10], "label": "time (s)"}, "controls": [{"name": "z", "range": [0, 1.5], "value": 0.3, "label": "damping ζ"}], "functions": [{"expr": "exp(-z*x)*cos(3*x)", "label": "x(t) = e^(−ζt) cos(ωt)", "color": "#9ca3af"}, {"expr": "exp(-z*x)", "label": "decay envelope", "color": "#cbd5e1"}], "points": [{"xExpr": "t", "yExpr": "exp(-z*t)*cos(3*t)", "label": "mass", "color": "#2563eb", "size": 7}]}
```

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

Here are the three body axes and an angular-velocity vector $\\vec\\omega=(p,q,r)$.
**Rotate and tilt** the view to see the triad in 3D — this is exactly what a
drone's gyroscope (or your phone's, when it flips the screen) measures: the spin
rates $p, q, r$ about *its own* axes.

```plot
{"mode": "3d", "title": "Body axes & angular velocity ω", "xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "zRange": [-1.5, 1.5], "azimuth": 40, "elevation": 25, "vectors": [{"x": 1.2, "y": 0, "z": 0, "label": "x_B (fwd)", "color": "#dc2626"}, {"x": 0, "y": 1.2, "z": 0, "label": "y_B (right)", "color": "#16a34a"}, {"x": 0, "y": 0, "z": 1.2, "label": "z_B (down)", "color": "#2563eb"}, {"x": 0.5, "y": 0.5, "z": 0.9, "label": "ω", "color": "#9333ea"}]}
```

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

Here is the kind of motion we are after — a quadrotor climbing on a circular
path. **Drag *rotate* and *tilt* to orbit the view**, and press **Play** to fly
it along the grey reference path. The whole point of the next lessons is to find
the equations that produce trajectories like this.

```plot
{"mode": "3d", "title": "A 3D trajectory: climbing spiral", "xRange": [-3, 3], "yRange": [-3, 3], "zRange": [0, 6], "azimuth": 40, "elevation": 22, "animate": {"param": "t", "range": [0, 12.566], "label": "time"}, "parametric": [{"x": "2*cos(s)", "y": "2*sin(s)", "z": "0.4*s", "param": "s", "range": [0, 12.566], "color": "#9ca3af", "label": "flight path"}], "points": [{"xExpr": "2*cos(t)", "yExpr": "2*sin(t)", "zExpr": "0.4*t", "label": "drone", "color": "#dc2626", "size": 7}]}
```

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

```vectors
{"title": "Body-frame forces (pitched θ ≈ 35°)", "equal": true, "xRange": [-2, 2], "yRange": [-1.8, 1.8], "vectors": [{"x": 0, "y": 1.5, "label": "thrust T", "color": "#16a34a"}, {"x": 0.86, "y": -1.0, "label": "gravity (Rᵀg)", "color": "#dc2626"}]}
```

The net of these two arrows is what accelerates the body — tilt the thrust and
the horizontal component is exactly what moves the quadrotor sideways.

See it for yourself (world frame): pitching by $\\theta$ tilts the thrust, and the
leftover **net force** (purple) gains a horizontal part $T\\sin\\theta$. That
sideways push is *how a quadrotor accelerates forward* — there is no separate
"forward motor", it simply leans:

```plot
{"title": "Pitch to move: tilting thrust gives a sideways force", "equal": true, "xRange": [-0.6, 2], "yRange": [-1.3, 1.8], "controls": [{"name": "th", "range": [0, 40], "value": 20, "label": "pitch θ (°)"}], "vectors": [{"xExpr": "1.5*sin(rad(th))", "yExpr": "1.5*cos(rad(th))", "from": [0, 0], "label": "thrust T", "color": "#16a34a"}, {"x": 0, "y": -1, "from": [0, 0], "label": "gravity mg", "color": "#dc2626"}, {"xExpr": "1.5*sin(rad(th))", "yExpr": "1.5*cos(rad(th)) - 1", "from": [0, 0], "label": "net force", "color": "#9333ea"}]}
```

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

It helps to *see* a potential. Below is a 2D potential well
$V(x,y) = x^2 + y^2$ as a 3D surface — **rotate and tilt it** with the sliders.
A ball released anywhere rolls *downhill* (along $-\\nabla V$) toward the
minimum at the bottom; that gradient is exactly the conservative force the
Lagrangian bookkeeps for you.

```plot
{"mode": "3d", "title": "A potential well V(x,y) = x² + y²", "xRange": [-3, 3], "yRange": [-3, 3], "zRange": [0, 18], "azimuth": 35, "elevation": 28, "zLabel": "V", "surfaces": [{"expr": "x^2 + y^2", "color": "#2563eb"}]}
```

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

## The phase-space picture

The Hamiltonian's natural view is **phase space** — position against momentum. A
conservative system holds $\\mathcal{H}$ constant, so its state endlessly circles
a **closed orbit** (add damping and the orbit spirals inward). Press **Play** to
watch the state $(q, p)$ ride one constant-energy loop:

```plot
{"title": "Phase space: motion as a closed orbit", "xLabel": "position q", "yLabel": "momentum p", "xRange": [-2.3, 2.3], "yRange": [-2.3, 2.3], "equal": true, "animate": {"param": "t", "range": [0, 6.283], "label": "time"}, "parametric": [{"x": "2*cos(s)", "y": "2*sin(s)", "param": "s", "range": [0, 6.283], "color": "#cbd5e1", "label": "constant-energy orbit"}, {"x": "1.1*cos(s)", "y": "1.1*sin(s)", "param": "s", "range": [0, 6.283], "color": "#e2e8f0", "label": "lower energy"}], "points": [{"xExpr": "2*cos(t)", "yExpr": "-2*sin(t)", "label": "state (q,p)", "color": "#2563eb", "size": 7, "trail": true}]}
```

LC circuits, pendulums and mass–springs all trace these loops — with energy
methods you read the motion straight off the geometry.

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
