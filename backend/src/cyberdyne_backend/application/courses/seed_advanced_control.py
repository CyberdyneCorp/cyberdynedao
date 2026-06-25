"""Advanced Control Systems track: Basics -> Intermediate -> Advanced.

Beyond classical (PID / root-locus / Bode) control into the modern toolkit:
state-space modelling and analysis, pole placement and observers, the linear
quadratic regulator (LQR), nonlinear systems and Lyapunov stability, then
feedback linearization, sliding-mode, model predictive control (MPC), robust
H-infinity, adaptive control and optimal estimation (the Kalman filter / LQG),
closing with a full design case study.

Lessons are `text` with LaTeX state-space math, interactive ```plot blocks
(step / impulse responses, phase portraits, LQR vs uncontrolled trade-offs) and
Mermaid block diagrams (feedback loops, observer + controller, MPC receding
horizon). Quizzes (per-lesson checkpoints + a final) are attached from the
central QUIZ_REGISTRY (seed_quizzes/advanced_control_*.py) at assembly time.
"""

# Lesson prose uses typographic characters (×, →, ≈, λ, ẋ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Advanced Control Systems — Basics ────────────────────────────────────────

_ADV_BASICS = SeedCourse(
    slug="advanced-control-basics",
    title="Advanced Control Systems — Basics",
    description=(
        "Step beyond classical transfer-function control into the modern, "
        "state-space view: why state space, the (A, B, C, D) model, solving the "
        "state equation with the state-transition matrix, stability from "
        "eigenvalues, and the twin structural properties of controllability and "
        "observability — with interactive response plots and block diagrams."
    ),
    level="Beginner",
    lessons=(
        _t(
            "From classical to modern control",
            "10 min",
            """\
# From classical to modern control

**Classical control** (PID, root locus, Bode) lives in the frequency domain and
works with a single transfer function $G(s) = \\dfrac{Y(s)}{U(s)}$ relating one
input to one output. It is brilliant for single-input single-output (SISO)
problems, but it hides the machinery inside the plant and strains badly when a
system has **many inputs and many outputs** (MIMO) that interact.

**Modern (state-space) control** instead tracks the system's internal **state** —
the minimal set of variables (positions, velocities, currents, temperatures) that,
together with future inputs, fully determine the future. The model is a set of
first-order differential equations in time, not a ratio of polynomials in $s$.

```mermaid
flowchart LR
  subgraph Classical
    U1[U s] --> G[G of s] --> Y1[Y s]
  end
  subgraph Modern
    U2[input u] --> ST[state x: A, B, C, D] --> Y2[output y]
  end
```

Why switch?

- **MIMO is natural.** One compact matrix equation handles any number of inputs
  and outputs and their cross-coupling.
- **Internal visibility.** We can reason about, and place sensors/actuators for,
  states we never directly measure.
- **Time domain & nonlinearity.** The same framework extends to time-varying,
  nonlinear and optimal control — where transfer functions cannot go.
- **It is what computers run.** Observers, LQR, Kalman filters and MPC are all
  state-space algorithms.

This track builds that toolkit from the ground up.

**Next:** writing a system in state-space form.
""",
        ),
        _t(
            "State-space representation (A, B, C, D)",
            "11 min",
            """\
# State-space representation (A, B, C, D)

A linear time-invariant (LTI) system in **state-space form** is

$$\\dot{\\mathbf{x}} = A\\,\\mathbf{x} + B\\,\\mathbf{u}, \\qquad
  \\mathbf{y} = C\\,\\mathbf{x} + D\\,\\mathbf{u}.$$

- $\\mathbf{x} \\in \\mathbb{R}^n$ — the **state** vector (what the system
  remembers).
- $\\mathbf{u} \\in \\mathbb{R}^m$ — the **input** (control) vector.
- $\\mathbf{y} \\in \\mathbb{R}^p$ — the measured **output** vector.
- $A$ ($n\\times n$) is the **system matrix** (internal dynamics), $B$ the
  **input matrix**, $C$ the **output matrix**, $D$ the **feedthrough** (often
  $0$).

## Worked example: mass–spring–damper

For $m\\ddot{q} + c\\dot{q} + k q = u$, choose states position and velocity,
$\\mathbf{x} = \\begin{bmatrix} q \\\\ \\dot q \\end{bmatrix}$:

$$A = \\begin{bmatrix} 0 & 1 \\\\ -\\tfrac{k}{m} & -\\tfrac{c}{m} \\end{bmatrix},\\;
  B = \\begin{bmatrix} 0 \\\\ \\tfrac{1}{m} \\end{bmatrix},\\;
  C = \\begin{bmatrix} 1 & 0 \\end{bmatrix},\\; D = 0.$$

```mermaid
flowchart LR
  U[input u] --> B((B))
  B --> SUM(("+"))
  SUM --> INT["integrator 1/s -> x"]
  INT --> C((C))
  C --> Y[output y]
  INT --> A((A))
  A --> SUM
```

The same plant has **many** valid state representations (any invertible change of
coordinates $\\mathbf{z} = T\\mathbf{x}$ gives another), but the input/output
behaviour is identical. The choice of states is yours; pick ones that are
physically meaningful or numerically convenient.

**Next:** solving the state equation in time.
""",
        ),
        _t(
            "Solving the state equation & the transition matrix",
            "11 min",
            """\
# Solving the state equation & the transition matrix

Given the state equation $\\dot{\\mathbf{x}} = A\\mathbf{x} + B\\mathbf{u}$ with
initial state $\\mathbf{x}(0)$, its solution mirrors the scalar case
$\\dot x = ax \\Rightarrow x(t) = e^{at}x(0)$, but with a **matrix exponential**:

$$\\mathbf{x}(t) = \\underbrace{e^{At}}_{\\Phi(t)}\\mathbf{x}(0)
  + \\int_0^t e^{A(t-\\tau)} B\\,\\mathbf{u}(\\tau)\\,d\\tau.$$

The matrix $\\Phi(t) = e^{At}$ is the **state-transition matrix**: it propagates
the free (unforced) state forward in time. It is defined by the series

$$e^{At} = I + At + \\frac{(At)^2}{2!} + \\frac{(At)^3}{3!} + \\cdots,$$

and satisfies $\\dot\\Phi = A\\Phi$, $\\Phi(0) = I$, and $\\Phi(t_2-t_1) =
\\Phi(t_2)\\Phi(-t_1)$.

If $A$ is diagonalisable as $A = V\\Lambda V^{-1}$ with eigenvalues $\\lambda_i$,
then $e^{At} = V e^{\\Lambda t} V^{-1}$, so each **mode** evolves as
$e^{\\lambda_i t}$. The free response is a blend of these modes. For a stable
real eigenvalue $\\lambda < 0$ the mode decays; here is $e^{\\lambda t}$ for a
couple of decay rates:

```plot
{"title": "Modes of the free response x(t) = e^(λt) x(0)", "xLabel": "time t", "yLabel": "mode amplitude", "xRange": [0, 6], "yRange": [0, 1.05], "functions": [{"expr": "exp(-0.5*x)", "label": "λ = -0.5 (slow decay)", "color": "#2563eb"}, {"expr": "exp(-1.5*x)", "label": "λ = -1.5 (fast decay)", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "x(0)", "color": "#16a34a", "size": 6}]}
```

The eigenvalues of $A$ therefore set *how fast* and *in what shape* the system
moves — which is exactly the stability story next.

**Next:** stability from the eigenvalues of A.
""",
        ),
        _t(
            "Stability via eigenvalues",
            "11 min",
            """\
# Stability via eigenvalues

Because the free response is built from modes $e^{\\lambda_i t}$, the stability
of an LTI system is read **directly off the eigenvalues of $A$** (the roots of
$\\det(sI - A) = 0$, which are also the poles):

- **Asymptotically stable** — every eigenvalue has **negative real part**
  ($\\operatorname{Re}\\lambda_i < 0$). All modes decay; the state returns to the
  origin.
- **Marginally stable** — simple eigenvalues on the imaginary axis
  ($\\operatorname{Re}\\lambda_i = 0$), none in the right half-plane: bounded,
  non-decaying oscillation.
- **Unstable** — any eigenvalue with **positive real part**: that mode grows
  without bound.

Complex pairs $\\lambda = -\\sigma \\pm j\\omega$ give a decaying oscillation
$e^{-\\sigma t}\\cos(\\omega t)$: $\\sigma$ sets the decay envelope, $\\omega$ the
ringing frequency. Below, the same oscillation frequency with a stable envelope
($\\sigma > 0$) versus an unstable one ($\\sigma < 0$):

```plot
{"title": "Eigenvalue real part decides stability of a mode", "xLabel": "time t", "yLabel": "state x(t)", "xRange": [0, 8], "yRange": [-2.5, 2.5], "functions": [{"expr": "exp(-0.4*x)*cos(3*x)", "label": "stable: Re λ = -0.4", "color": "#2563eb"}, {"expr": "exp(0.25*x)*cos(3*x)", "label": "unstable: Re λ = +0.25", "color": "#dc2626"}]}
```

This is the central payoff of the state-space view: design becomes "move the
eigenvalues into the left half-plane and place them where you want" — the
**pole-placement** problem of the Intermediate course. But moving them requires
two structural properties first.

**Next:** can we even reach every state? Controllability.
""",
        ),
        _t(
            "Controllability",
            "11 min",
            """\
# Controllability

Before we can *move* a system's eigenvalues with feedback, the input must
actually be able to influence every state. A system is **controllable** if, for
any initial state $\\mathbf{x}(0)$ and any target state, some finite input
$\\mathbf{u}(t)$ drives the state from one to the other in finite time.

**The test (Kalman rank condition).** Build the **controllability matrix**

$$\\mathcal{C} = \\big[\\, B \\;\\; AB \\;\\; A^2B \\;\\; \\cdots \\;\\; A^{n-1}B \\,\\big].$$

The system is controllable **iff** $\\operatorname{rank}(\\mathcal{C}) = n$ (full
row rank).

```mermaid
flowchart LR
  AB["B, AB, A^2 B, ... A^(n-1) B"] --> RK{"rank = n ?"}
  RK -- yes --> OK["controllable: poles freely placeable"]
  RK -- no --> NO["uncontrollable mode: cannot be moved by u"]
```

**Intuition.** Stacking $B, AB, A^2B, \\dots$ explores the directions the input
can push the state into directly and through the dynamics. If those directions
fail to span all of $\\mathbb{R}^n$, some combination of states is an
**uncontrollable mode** — the input cannot affect it at all. If that mode is also
unstable, the system is unstabilisable and no state feedback can save it.

Controllability is **structural**: it depends only on the pair $(A, B)$, not on
the specific input you choose. It is the precondition that makes arbitrary
**pole placement** possible.

**Next:** the dual question — can we see the state? Observability.
""",
        ),
        _t(
            "Observability",
            "10 min",
            """\
# Observability

Controllability asks whether the input can *reach* every state; **observability**
asks the dual question — whether watching the output long enough lets us
*reconstruct* the full internal state. A system is **observable** if the initial
state $\\mathbf{x}(0)$ can be determined from the output $\\mathbf{y}(t)$ over a
finite interval (with the known input).

**The test.** Build the **observability matrix**

$$\\mathcal{O} = \\begin{bmatrix} C \\\\ CA \\\\ CA^2 \\\\ \\vdots \\\\ CA^{n-1} \\end{bmatrix}.$$

The system is observable **iff** $\\operatorname{rank}(\\mathcal{O}) = n$.

This is the mathematical **dual** of controllability: $(A, C)$ is observable
exactly when $(A^\\top, C^\\top)$ is controllable. So every controllability result
has an observability twin — including the design tools to come.

```mermaid
flowchart LR
  Y[measured output y t] --> OBS["observer / estimator"]
  U[known input u t] --> OBS
  OBS --> XH["state estimate x-hat"]
```

If a system is **unobservable**, some internal mode never shows up in the output;
we are blind to it. The fix in practice is either to add a sensor (change $C$) or,
when that mode is stable and we only need its decay, to accept the loss.

Together, controllability and observability are the structural conditions behind
the two pillars of state-space design:

- **Controllable** ⟹ we can place poles with **state feedback**.
- **Observable** ⟹ we can build a **state observer** to estimate the states we
  cannot measure.

The Intermediate course combines both into the controller + observer design.

**Next:** check what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Advanced Control Systems — Intermediate ──────────────────────────────────

_ADV_INTERMEDIATE = SeedCourse(
    slug="advanced-control-intermediate",
    title="Advanced Control Systems — Intermediate",
    description=(
        "The core of state-space design: place closed-loop poles with state "
        "feedback, estimate unmeasured states with an observer (and the "
        "separation principle), trade effort against performance with the LQR, "
        "add integral action for tracking, then step into nonlinear systems — "
        "equilibria, linearization, phase portraits and Lyapunov stability."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Pole placement & state feedback",
            "12 min",
            """\
# Pole placement & state feedback

If the pair $(A, B)$ is controllable, we can place the closed-loop eigenvalues
*anywhere we like*. The tool is **full-state feedback**: feed every state back
through a gain row/matrix $K$,

$$\\mathbf{u} = -K\\,\\mathbf{x},$$

which turns the open-loop dynamics $\\dot{\\mathbf{x}} = A\\mathbf{x} +
B\\mathbf{u}$ into

$$\\dot{\\mathbf{x}} = (A - BK)\\,\\mathbf{x}.$$

```mermaid
flowchart LR
  R[reference r = 0] --> SUM(("+"))
  SUM -- u --> P["plant: x-dot = A x + B u"]
  P -- x --> Y[output]
  P -- x --> K["-K"]
  K --> SUM
```

Now we choose $K$ so that the eigenvalues of $A - BK$ sit at desired locations
$\\{p_1, \\dots, p_n\\}$ (chosen for a target settling time and damping). For a
controllable single-input system, **Ackermann's formula** gives $K$ in closed
form; numerically we use `place`. Controllability is exactly the condition that
makes *arbitrary* placement possible.

Pushing the poles further left makes the response faster — but at the cost of
larger control effort $u$ and a real chance of actuator saturation. Below, a
second-order response for a "slow" pole choice versus a "fast" one:

```plot
{"title": "Closed-loop step response: pole placement sets speed", "xLabel": "time t", "yLabel": "output y(t)", "xRange": [0, 10], "yRange": [0, 1.4], "functions": [{"expr": "1 - exp(-0.6*x)*(cos(1.0*x) + 0.6*sin(1.0*x))", "label": "slow poles (Re ≈ -0.6)", "color": "#2563eb"}, {"expr": "1 - exp(-1.5*x)*(cos(1.5*x) + sin(1.5*x))", "label": "fast poles (Re ≈ -1.5)", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "target = 1", "color": "#16a34a", "size": 5}]}
```

The trouble: $\\mathbf{u} = -K\\mathbf{x}$ assumes we **measure every state**. We
rarely do — which motivates the observer next.

**Next:** estimating the states we cannot measure.
""",
        ),
        _t(
            "State observers & the separation principle",
            "12 min",
            """\
# State observers & the separation principle

When we cannot measure all of $\\mathbf{x}$, we **estimate** it. A
**Luenberger observer** runs a copy of the model and corrects it using the
mismatch between the real and predicted outputs:

$$\\dot{\\hat{\\mathbf{x}}} = A\\hat{\\mathbf{x}} + B\\mathbf{u}
  + L\\,(\\mathbf{y} - C\\hat{\\mathbf{x}}).$$

The estimation error $\\mathbf{e} = \\mathbf{x} - \\hat{\\mathbf{x}}$ then obeys

$$\\dot{\\mathbf{e}} = (A - LC)\\,\\mathbf{e}.$$

So if $(A, C)$ is **observable**, we choose $L$ to place the eigenvalues of
$A - LC$ in the left half-plane and the estimate converges to the truth — exactly
the **dual** of pole placement (place poles of $A - LC$ instead of $A - BK$).

```mermaid
flowchart LR
  R[r] --> SUM(("+"))
  SUM -- u --> P["plant: x"]
  P -- "y" --> OBS["observer: A,B,L -> x-hat"]
  OBS -- "x-hat" --> K["-K"]
  K --> SUM
  P -- "u (also to observer)" --> OBS
```

We now control using the **estimate**: $\\mathbf{u} = -K\\hat{\\mathbf{x}}$. The
remarkable **separation principle** says the closed-loop eigenvalues of this
combined system are simply the union of the controller poles
(eigenvalues of $A - BK$) and the observer poles (eigenvalues of $A - LC$). They
**do not interact**, so you can design the feedback gain $K$ and the observer gain
$L$ completely independently. Rule of thumb: make the observer **2–5× faster**
than the controller so estimation settles before control acts on it.

**Next:** choosing K optimally instead of by hand — the LQR.
""",
        ),
        _t(
            "The linear quadratic regulator (LQR)",
            "12 min",
            """\
# The linear quadratic regulator (LQR)

Pole placement asks *where* to put the poles — but for a high-order or MIMO system
that choice is unobvious. The **linear quadratic regulator** instead asks you to
state *what you care about* as a cost, and computes the optimal gain $K$ for you.

Minimise the quadratic cost over an infinite horizon:

$$J = \\int_0^\\infty \\big(\\mathbf{x}^\\top Q\\,\\mathbf{x}
  + \\mathbf{u}^\\top R\\,\\mathbf{u}\\big)\\,dt,$$

where $Q \\succeq 0$ penalises **state error** (how badly you allow the states to
deviate) and $R \\succ 0$ penalises **control effort** (how expensive actuation
is). The optimal feedback is $\\mathbf{u} = -K\\mathbf{x}$ with

$$K = R^{-1}B^\\top P,$$

where $P$ solves the **algebraic Riccati equation**
$A^\\top P + PA - PBR^{-1}B^\\top P + Q = 0$.

The result is always a **stabilising** feedback (for a controllable system) with
excellent robustness margins. Tuning is intuitive: **large $Q$ / small $R$** =
aggressive, fast, expensive control; **small $Q$ / large $R$** = gentle, cheap,
slow control. Below, the regulated state for a cheap-control choice versus an
expensive-control one, against the uncontrolled (open-loop, slowly decaying)
response:

```plot
{"title": "LQR: cost trade-off between speed and control effort", "xLabel": "time t", "yLabel": "state x(t)", "xRange": [0, 10], "yRange": [-0.1, 1.05], "functions": [{"expr": "exp(-0.2*x)", "label": "uncontrolled (open loop)", "color": "#94a3b8"}, {"expr": "exp(-0.7*x)", "label": "large R: gentle, slow", "color": "#2563eb"}, {"expr": "exp(-1.8*x)", "label": "small R: aggressive, fast", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "x(0)", "color": "#16a34a", "size": 5}]}
```

LQR pairs with the Kalman filter (the optimal observer) to form **LQG** — the
Advanced course closes that loop.

**Next:** making the output track a non-zero reference.
""",
        ),
        _t(
            "Integral action & reference tracking",
            "11 min",
            """\
# Integral action & reference tracking

Plain state feedback $\\mathbf{u} = -K\\mathbf{x}$ is a **regulator**: it drives
the state to **zero**. Real systems must follow a non-zero **reference** $r$ — a
target speed, altitude, temperature — and do so with **no steady-state error**
even when the model is imperfect or a constant disturbance is present.

**Naive fix (feedforward).** Pick a reference gain $N$ so $\\mathbf{u} = -K\\mathbf{x}
+ Nr$ makes the output equal $r$ at steady state. It works *only* if the model is
exact — any plant-gain error or constant disturbance leaves a residual offset.

**Robust fix (integral action).** Augment the state with the **integral of the
tracking error**, $x_i = \\int (r - y)\\,dt$, and feed it back too:

$$\\dot{x}_i = r - y, \\qquad \\mathbf{u} = -K\\mathbf{x} - k_i\\,x_i.$$

As long as anything is left uncorrected, $x_i$ keeps accumulating and nudging $u$,
so at equilibrium $\\dot x_i = 0$ forces $y = r$ — **exactly**, model errors and
constant disturbances and all. This is the state-space sibling of the integral
term in PID.

```mermaid
flowchart LR
  R[reference r] --> SUM(("+"))
  Y[output y] -- "-" --> SUM
  SUM -- "error e" --> INT["integral: x_i = ∫e dt"]
  INT -- "-k_i x_i" --> U(("+"))
  X["state x"] -- "-K x" --> U
  U -- u --> P["plant"]
  P --> Y
```

You design the augmented gain $[K \\;\\; k_i]$ by pole placement or LQR on the
**augmented system**. The price is one extra (integrator) pole to place and a
watch for **integrator windup** when the actuator saturates.

**Next:** leaving the linear world.
""",
        ),
        _t(
            "Introduction to nonlinear systems",
            "12 min",
            """\
# Introduction to nonlinear systems

Real plants are **nonlinear**: $\\dot{\\mathbf{x}} = \\mathbf{f}(\\mathbf{x},
\\mathbf{u})$. They break the comfortable linear rules — superposition fails,
there can be **multiple equilibria**, limit cycles, and behaviour that depends on
the size of the input, not just its shape.

**Equilibria.** A point $\\mathbf{x}^*$ where motion stops:
$\\mathbf{f}(\\mathbf{x}^*, \\mathbf{u}^*) = \\mathbf{0}$. The pendulum has two —
hanging down (stable) and balanced up (unstable).

**Linearization.** Near an equilibrium we approximate the dynamics by the
**Jacobian**, recovering a local linear model to which all our tools apply:

$$\\delta\\dot{\\mathbf{x}} \\approx A\\,\\delta\\mathbf{x} + B\\,\\delta\\mathbf{u},
  \\quad A = \\left.\\frac{\\partial \\mathbf{f}}{\\partial \\mathbf{x}}\\right|_{*},
  \\; B = \\left.\\frac{\\partial \\mathbf{f}}{\\partial \\mathbf{u}}\\right|_{*}.$$

The eigenvalues of this local $A$ classify the equilibrium (stable node, saddle,
focus, …) — valid **only nearby**.

**Phase portrait.** For a 2-state system we plot trajectories in the
$(x_1, x_2)$ plane. For an undamped pendulum, energy is conserved, so trajectories
near the bottom equilibrium are **closed orbits** — concentric ovals around the
centre. Here is a family of such orbits $x_2 = \\pm c\\sqrt{1 - x_1^2}$ (upper
halves shown), each a constant-energy contour:

```plot
{"title": "Phase portrait: closed orbits around a stable equilibrium", "xLabel": "x₁ (angle)", "yLabel": "x₂ (angular velocity)", "xRange": [-1.2, 1.2], "yRange": [-1.2, 1.2], "functions": [{"expr": "0.4*sqrt(1 - x^2)", "label": "small-energy orbit", "color": "#2563eb"}, {"expr": "0.8*sqrt(1 - x^2)", "label": "larger-energy orbit", "color": "#dc2626"}], "points": [{"x": 0, "y": 0, "label": "stable equilibrium (centre)", "color": "#16a34a", "size": 6}]}
```

Linearization is the bridge that lets the whole earlier course govern a nonlinear
plant *near its operating point* — gain scheduling stitches several such points
together.

**Next:** stability without linearizing — Lyapunov.
""",
        ),
        _t(
            "Lyapunov stability",
            "11 min",
            """\
# Lyapunov stability

Linearization only tells us about behaviour *very near* an equilibrium, and says
nothing when the Jacobian has eigenvalues on the imaginary axis. **Lyapunov's
direct method** judges stability of the full nonlinear system **without solving
it** — by generalising the idea of energy.

Find a scalar **Lyapunov function** $V(\\mathbf{x})$ that is like an energy:

- $V(\\mathbf{0}) = 0$ and $V(\\mathbf{x}) > 0$ for $\\mathbf{x} \\neq \\mathbf{0}$
  (**positive definite** — a bowl with its bottom at the equilibrium).
- Its rate along trajectories,
  $\\dot V = \\nabla V \\cdot \\mathbf{f}(\\mathbf{x})$, is $\\le 0$.

Then the equilibrium is **stable**; if $\\dot V < 0$ (strictly, away from the
origin) it is **asymptotically stable** — energy is continuously dissipated, so
the state must slide to the bottom of the bowl.

```plot
{"title": "Lyapunov function V(x): a bowl that the state slides down", "xLabel": "state x", "yLabel": "V(x) (energy-like)", "xRange": [-3, 3], "yRange": [0, 5], "functions": [{"expr": "0.5*x^2", "label": "V(x) = ½x²", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "equilibrium: V = 0", "color": "#16a34a", "size": 6}, {"x": 2, "y": 2, "label": "state with V > 0", "color": "#dc2626", "size": 6}]}
```

**Why it matters.** For a linear system, $V = \\mathbf{x}^\\top P \\mathbf{x}$ with
$P$ solving the **Lyapunov equation** $A^\\top P + PA = -Q$ proves stability and is
the seed of the LQR's Riccati equation. For nonlinear systems it is *the* tool —
and finding a good $V$ is also the basis of **control Lyapunov functions**, where
we choose $\\mathbf{u}$ to *force* $\\dot V < 0$. That idea launches the Advanced
course.

**Next:** check what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Advanced Control Systems — Advanced ──────────────────────────────────────

_ADV_ADVANCED = SeedCourse(
    slug="advanced-control-advanced",
    title="Advanced Control Systems — Advanced",
    description=(
        "The research-grade toolkit: nonlinear control by feedback linearization "
        "and sliding modes, model predictive control (MPC) with constraints and a "
        "receding horizon, robust control and H-infinity for uncertainty, "
        "adaptive control, optimal estimation with the Kalman filter (LQG), and a "
        "full design case study that ties the whole track together."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Nonlinear control: feedback linearization & sliding mode",
            "13 min",
            """\
# Nonlinear control: feedback linearization & sliding mode

Linearizing about one operating point is fragile far from it. Two powerful
techniques control nonlinear plants **globally**.

## Feedback linearization

If the dynamics are $\\dot{\\mathbf{x}} = \\mathbf{f}(\\mathbf{x}) +
g(\\mathbf{x})\\,u$, choose a control that **cancels the nonlinearity** exactly:

$$u = \\frac{1}{g(\\mathbf{x})}\\big(-\\mathbf{f}(\\mathbf{x}) + v\\big),$$

leaving simple linear dynamics in the new input $v$ (e.g. $\\dot{\\mathbf{x}} = v$),
which we then close with ordinary linear control. This is exactly how robot-arm
**computed-torque** control works. The catch: it demands an **accurate model** —
cancellation is only as good as our knowledge of $\\mathbf{f}$ and $g$.

## Sliding-mode control

When the model is uncertain, **sliding-mode control (SMC)** is deliberately
robust. Define a **sliding surface** $s(\\mathbf{x}) = 0$ on which the error
dynamics are nice, then switch the control hard to force $s \\to 0$ and keep it
there:

$$u = -k\\,\\operatorname{sign}\\big(s(\\mathbf{x})\\big).$$

Once on the surface the motion is governed by the surface design and is
**insensitive to matched disturbances and model error** — its headline strength.
The cost is **chattering**: high-frequency switching that the ideal $\\operatorname{sign}$
produces, usually softened with a saturation/boundary-layer approximation:

```plot
{"title": "Sliding-mode law: ideal sign vs a smoothed boundary layer", "xLabel": "sliding variable s", "yLabel": "control u (normalized)", "xRange": [-2, 2], "yRange": [-1.4, 1.4], "functions": [{"expr": "x/sqrt(x^2 + 0.01)", "label": "near-ideal sign(s) (chatters)", "color": "#dc2626"}, {"expr": "x/sqrt(x^2 + 0.25)", "label": "smoothed (boundary layer)", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "sliding surface s = 0", "color": "#16a34a", "size": 6}]}
```

Feedback linearization trusts the model; sliding mode distrusts it. Real designs
often blend them.

**Next:** optimisation-based control — MPC.
""",
        ),
        _t(
            "Model predictive control (MPC)",
            "13 min",
            """\
# Model predictive control (MPC)

**Model predictive control** is the dominant advanced method in industry because
it does one thing the others cannot: it handles **constraints** — actuator
limits, state bounds, safety envelopes — directly and optimally.

At every sampling instant MPC:

1. uses the model to **predict** the output over a horizon of $N$ steps for a
   candidate sequence of future inputs;
2. solves a constrained **optimisation** for the input sequence that minimises a
   cost (tracking error + effort) subject to $u_{\\min} \\le u \\le u_{\\max}$ and
   state limits;
3. applies **only the first** input of that optimal sequence;
4. shifts the window forward and **repeats** at the next step.

That step-4 re-solving is the **receding horizon** — it turns an open-loop optimal
plan into closed-loop feedback and absorbs disturbances and model error.

```mermaid
flowchart LR
  R[reference trajectory] --> OPT["optimizer: min cost over N steps s.t. constraints"]
  X["current state x_k (or estimate)"] --> OPT
  MOD["prediction model"] --> OPT
  OPT -- "u*_k ... u*_(k+N-1)" --> APPLY["apply first input u*_k only"]
  APPLY -- u_k --> P["plant"]
  P -- "x_(k+1)" --> X
  APPLY -. "shift window, re-solve" .-> OPT
```

The cost over the prediction window typically looks like

$$J = \\sum_{i=0}^{N-1}\\Big( \\|\\,y_{k+i} - r_{k+i}\\,\\|_Q^2
  + \\|\\,u_{k+i}\\,\\|_R^2 \\Big),$$

so unconstrained MPC reduces to LQR — MPC is "LQR that can say *no* to limits".
Below, a predicted output ramping to a setpoint while respecting a hard ceiling
the controller must not cross:

```plot
{"title": "MPC prediction: track the reference but honour a hard limit", "xLabel": "prediction step (time)", "yLabel": "output y", "xRange": [0, 10], "yRange": [0, 1.3], "functions": [{"expr": "1 - exp(-0.8*x)", "label": "predicted output y", "color": "#2563eb"}, {"expr": "1.1 + 0*x", "label": "hard upper limit", "color": "#dc2626"}], "points": [{"x": 0, "y": 1, "label": "setpoint r = 1", "color": "#16a34a", "size": 5}]}
```

The price is **online computation** — each step solves an optimisation — which is
why MPC rose with cheap fast processors.

**Next:** designing for what we *don't* know — robust control.
""",
        ),
        _t(
            "Robust control & uncertainty (H-infinity)",
            "12 min",
            """\
# Robust control & uncertainty (H-infinity)

Every model is wrong: parameters drift, dynamics go unmodelled, sensors are
noisy. **Robust control** designs a *single fixed* controller that is guaranteed
to remain **stable and performant** across a whole set of plausible plants, not
just the nominal one.

We model uncertainty explicitly — e.g. a multiplicative perturbation
$G(s) = G_0(s)\\,(1 + \\Delta(s))$ with $\\|\\Delta\\|_\\infty \\le 1$ — and ask the
controller to tolerate **any** such $\\Delta$.

## The H-infinity idea

The **$\\mathcal{H}_\\infty$ norm** of a transfer function is its largest gain over
all frequencies — the worst case:

$$\\|T\\|_\\infty = \\sup_{\\omega} |T(j\\omega)|.$$

$\\mathcal{H}_\\infty$ design **minimises this worst-case gain** from disturbances
to errors, so it optimises for the nastiest input the system could see (unlike
LQR/$\\mathcal{H}_2$, which optimises an *average*). The famous **small-gain
theorem** then certifies stability: a feedback loop of stable blocks stays stable
if the loop gain stays below 1 at every frequency. Below, a sensitivity-style
worst-case gain curve kept under a robustness bound across the band:

```plot
{"title": "H-infinity: keep the worst-case gain under a bound at all ω", "xLabel": "frequency ω", "yLabel": "closed-loop gain |T(jω)|", "xRange": [0, 10], "yRange": [0, 2.2], "functions": [{"expr": "1.6*x/sqrt(x^2 + 4)", "label": "achieved gain |T(jω)|", "color": "#2563eb"}, {"expr": "1.8 + 0*x", "label": "robustness bound (γ)", "color": "#dc2626"}]}
```

The trade-off is the **robustness–performance** tension: a controller hardened
against the worst case is necessarily more conservative (slower, lower bandwidth)
than one tuned for the nominal plant. $\\mu$-synthesis extends this to structured
uncertainty.

**Next:** what if the plant changes while we run? Adaptive control.
""",
        ),
        _t(
            "Adaptive control",
            "11 min",
            """\
# Adaptive control

Robust control fixes one controller for a known *range* of plants. **Adaptive
control** goes further: it **adjusts the controller online** as it learns the
plant, ideal when parameters are unknown *and slowly changing* — a fuel-burning
aircraft losing mass, a robot picking up an unknown load.

Two classic architectures:

- **Model-Reference Adaptive Control (MRAC).** Specify a **reference model** that
  encodes the desired closed-loop behaviour. An adaptation law (e.g. the **MIT
  rule** or a Lyapunov-based law) tunes the controller gains in real time to drive
  the error between plant and reference model to zero.
- **Self-Tuning Regulator (STR).** Continuously **estimate** the plant parameters
  (recursive least squares) and **redesign** the controller from the fresh
  estimates each step — "estimate, then control", repeatedly.

```mermaid
flowchart LR
  R[reference r] --> RM["reference model"]
  R --> C["controller (tunable gains θ)"]
  C -- u --> P["unknown / changing plant"]
  P -- "y" --> CMP(("compare"))
  RM -- "y_m" --> CMP
  CMP -- "error e" --> ADAPT["adaptation law"]
  ADAPT -- "update θ" --> C
```

Adaptation makes the closed loop **nonlinear and time-varying** even when the
plant is linear, so the hard part is proving the gains converge and the loop stays
stable — almost always done with a **Lyapunov function** (back to the
Intermediate course). The danger is **bursting / parameter drift** when excitation
is poor; robustifying fixes (dead-zones, $\\sigma$-modification, projection) tame it.
Modern learning-based and reinforcement-learning controllers are intellectual
descendants of this idea.

**Next:** estimating state optimally under noise — the Kalman filter.
""",
        ),
        _t(
            "Optimal estimation & LQG (the Kalman filter)",
            "12 min",
            """\
# Optimal estimation & LQG (the Kalman filter)

The Luenberger observer assumed clean measurements. Reality has **process noise**
(unmodelled disturbances) and **measurement noise** (sensor error). The
**Kalman filter** is the *optimal* observer for a linear system with Gaussian
noise — it is a Luenberger observer whose gain is chosen to **minimise the
estimation-error variance**.

For the model
$\\dot{\\mathbf{x}} = A\\mathbf{x} + B\\mathbf{u} + \\mathbf{w}$,
$\\mathbf{y} = C\\mathbf{x} + \\mathbf{v}$ with covariances $W$ (process) and $V$
(measurement), it runs two repeating steps:

- **Predict** — push the estimate and its covariance forward through the model.
- **Update** — correct with the new measurement, weighted by the **Kalman gain**
  $L = PC^\\top V^{-1}$, which balances trust in the model against trust in the
  sensor ($P$ solves a Riccati equation — the **dual** of the LQR's).

Heavy sensor noise ⟹ small gain (lean on the model); precise sensor ⟹ large gain
(lean on the measurement). The filter blends a noisy measurement and a model
prediction into an estimate **better than either** alone:

```plot
{"title": "Kalman filter: estimate tracks truth, smoothing noisy data", "xLabel": "time t", "yLabel": "state / measurement", "xRange": [0, 12], "yRange": [-1.5, 1.5], "functions": [{"expr": "sin(x)", "label": "true state (unknown)", "color": "#16a34a"}, {"expr": "sin(x) + 0.35*sin(11*x)", "label": "noisy measurement y", "color": "#94a3b8"}, {"expr": "sin(x) + 0.05*sin(11*x)", "label": "Kalman estimate x-hat", "color": "#2563eb"}]}
```

## LQG: putting it together

The **Linear Quadratic Gaussian** controller is the headline result of optimal
control: **LQR feedback + Kalman filter**. By the **separation principle**, design
the optimal regulator $K$ and the optimal estimator $L$ **independently**, then
feed the controller the filter's estimate, $\\mathbf{u} = -K\\hat{\\mathbf{x}}$ —
provably optimal for the noisy linear-Gaussian problem.

```mermaid
flowchart LR
  R[reference] --> SUM(("+"))
  SUM -- u --> P["plant (+ process noise w)"]
  P -- "y + noise v" --> KF["Kalman filter -> x-hat"]
  KF -- "x-hat" --> K["-K (LQR gain)"]
  K --> SUM
```

**Next:** put the whole track to work — a design case study.
""",
        ),
        _t(
            "A design case study",
            "12 min",
            """\
# A design case study

Let's design a stabilising controller for the classic **inverted pendulum on a
cart** — a nonlinear, unstable, under-actuated benchmark — using the whole track
end to end. Goal: keep the pole upright while parking the cart, despite sensor
noise and a shove.

**1. Model & states.** States $\\mathbf{x} = [\\,p,\\ \\dot p,\\ \\theta,\\
\\dot\\theta\\,]^\\top$ (cart position/velocity, pole angle/rate), input $u$ =
motor force. The dynamics $\\mathbf{f}(\\mathbf{x}, u)$ are nonlinear (they contain
$\\sin\\theta$, $\\cos\\theta$).

**2. Linearize.** About the upright equilibrium ($\\theta = 0$), take the Jacobian
to get $(A, B)$. An eigenvalue of $A$ sits in the **right half-plane** — confirming
open-loop instability.

**3. Check structure.** Form $\\mathcal{C} = [B\\ AB\\ A^2B\\ A^3B]$: full rank,
so **controllable** — we can place the poles. Form $\\mathcal{O}$ from the measured
outputs (cart position + pole angle): full rank, so **observable** — we can
estimate the velocities we don't measure.

**4. Design feedback.** Choose **LQR** with $Q$ weighting pole angle heavily
(keep it upright) and cart position lightly, and $R$ moderate (limited motor).
Solve the Riccati equation for $K$.

**5. Design the estimator.** Build a **Kalman filter** for the noisy
position/angle sensors to reconstruct $[\\dot p,\\ \\dot\\theta]$ and reject noise.

**6. Combine (separation principle).** The compensator is LQR-on-the-estimate —
an **LQG** controller. Closed-loop poles = LQR poles ∪ filter poles, all in the
left half-plane.

```mermaid
flowchart LR
  R["reference (upright, cart=0)"] --> SUM(("+"))
  SUM -- "force u" --> CP["cart-pendulum plant (nonlinear)"]
  CP -- "noisy p, θ" --> KF["Kalman filter -> x-hat"]
  KF -- "x-hat (p, ṗ, θ, θ̇)" --> K["-K (LQR)"]
  K --> SUM
  D["disturbance / shove"] -.-> CP
```

**7. Verify.** Simulate against the **nonlinear** model: the controlled state
returns to upright after a shove, while the uncontrolled pole falls away. The
controlled angle decays; the uncontrolled one diverges:

```plot
{"title": "Case study: controlled pole recovers, uncontrolled diverges", "xLabel": "time t", "yLabel": "pole angle θ (rad)", "xRange": [0, 8], "yRange": [-0.5, 1.6], "functions": [{"expr": "0.2*exp(0.6*x)", "label": "uncontrolled (falls over)", "color": "#dc2626"}, {"expr": "0.2*exp(-0.9*x)*cos(1.6*x)", "label": "LQG-controlled (recovers)", "color": "#2563eb"}], "points": [{"x": 0, "y": 0, "label": "upright target θ = 0", "color": "#16a34a", "size": 5}]}
```

**Beyond.** If the pole carries an unknown load, add **adaptation**; if there are
hard force/track limits, swap the LQR for **MPC**; if the parameters are uncertain,
harden with **H-infinity**. Every tool in this track plugs into the same
state-space frame.

**Next:** check what you've learned.
""",
        ),
        _quiz(),
    ),
)


ADVANCED_CONTROL_COURSES: tuple[SeedCourse, ...] = (
    _ADV_BASICS,
    _ADV_INTERMEDIATE,
    _ADV_ADVANCED,
)

__all__ = ["ADVANCED_CONTROL_COURSES"]
