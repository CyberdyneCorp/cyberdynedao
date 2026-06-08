"""Curated Mathematics track for engineers & programmers: Basics →
Intermediate → Advanced.

Covers sets & logic, algebra, linear algebra, derivatives, integrals, ODEs,
PDEs and graph theory — always tied to code and real systems. Lessons are
`text` with LaTeX math and interactive ```plot blocks (curves, sliders,
animations, vectors, 3D surfaces); the Advanced track ends with a runnable
Python numerical lab.
"""

# Lesson prose uses typographic characters (×, →, ≈, ∂, ∇, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Mathematics — Basics ─────────────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="math-basics",
    title="Mathematics — Basics",
    description=(
        "Math for engineers & programmers from the ground up: sets and logic, "
        "the algebra and functions you reuse daily, reading and transforming "
        "graphs, and a first look at the derivative as a rate of change. Every "
        "idea is tied to code and real systems."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Sets, logic & functions",
            "10 min",
            """\
# Sets, logic & functions

Almost everything in math and programming is built from three ideas: **sets**
(collections), **logic** (true/false), and **functions** (mappings).

## Sets

A **set** is an unordered collection of distinct items: $A = \\{1, 2, 3\\}$.

| Operation | Math | In code (Python) |
|-----------|------|------------------|
| union | $A \\cup B$ | `A | B` |
| intersection | $A \\cap B$ | `A & B` |
| difference | $A \\setminus B$ | `A - B` |
| membership | $x \\in A$ | `x in A` |

Databases are set machines: a SQL `JOIN` is an intersection, `UNION` is a
union, `WHERE` filters a set.

## Logic

Propositions are **true (1)** or **false (0)**, combined with **AND** ($\\wedge$),
**OR** ($\\vee$), **NOT** ($\\neg$) — exactly the `&&`, `||`, `!` of code and the
gates inside every CPU. A logical condition *is* a function returning 0 or 1:

```plot
{"title": "Logic as a function: the step (Heaviside)", "xLabel": "x", "yLabel": "x > 0 ?", "xRange": [-3, 3], "yRange": [-0.3, 1.3], "functions": [{"expr": "if(x > 0, 1, 0)", "label": "1 if x>0 else 0", "color": "#16a34a"}]}
```

That "1 if positive, else 0" is the indicator function — and softened, it's the
activation function of a neuron.

## Functions

A **function** $f$ maps each input to exactly one output, like a pure function
in code: same input → same output. Drag the input and watch the output it
produces on the curve $f(x) = x^2$:

```plot
{"title": "A function maps input → output", "xLabel": "input x", "yLabel": "output f(x)", "xRange": [-3, 3], "yRange": [0, 9], "controls": [{"name": "a", "range": [-3, 3], "value": 1.5, "label": "input x"}], "functions": [{"expr": "x^2", "label": "f(x) = x²", "color": "#2563eb"}], "points": [{"xExpr": "a", "yExpr": "a^2", "label": "(x, f(x))", "color": "#dc2626", "size": 7}]}
```

**Next:** the algebra of functions you'll use constantly.
""",
        ),
        _t(
            "Algebra: growth, exponentials & logs",
            "11 min",
            """\
# Algebra: growth, exponentials & logs

Algebra is the grammar of formulas. The shapes that matter most in engineering
and programming are **polynomials**, **exponentials**, and their inverse,
**logarithms**.

## Why growth rate is everything

A program that takes $n^2$ steps and one that takes $2^n$ steps feel the same
for tiny $n$ — then exponential growth explodes. This is the heart of **Big-O**:

```plot
{"title": "Why exponential growth dominates (Big-O)", "xLabel": "input size n", "yLabel": "operations", "xRange": [0, 8], "yRange": [0, 260], "functions": [{"expr": "x*log2(x+1)", "label": "n log n", "color": "#16a34a"}, {"expr": "x^2", "label": "n² (quadratic)", "color": "#2563eb"}, {"expr": "2^x", "label": "2ⁿ (exponential)", "color": "#dc2626"}]}
```

At $n=8$ the quadratic needs 64 steps; the exponential needs 256 — and at
$n=40$ it would outlast the universe. Choosing the green curve over the red one
is what algorithm design is about.

## Exponentials & logarithms

$\\log_b$ is the inverse of $b^x$: it answers "how many doublings?". Logarithms
turn multiplication into addition and tame huge ranges (decibels, pH, Richter
scale, log-scale plots). **Exponential decay** $e^{-kt}$ shows up everywhere —
radioactive half-life, a capacitor discharging, a learning-rate schedule:

```plot
{"title": "Exponential decay: half-life / RC discharge", "xLabel": "time t", "yLabel": "amount", "xRange": [0, 10], "yRange": [0, 1.05], "controls": [{"name": "k", "range": [0.1, 2], "value": 0.6, "label": "decay rate k"}], "functions": [{"expr": "exp(-k*x)", "label": "e^(−k t)", "color": "#dc2626"}]}
```

Raise $k$ and it decays faster — a larger rate means a shorter half-life
$t_{1/2} = \\ln 2 / k$.

**Next:** reading and reshaping graphs.
""",
        ),
        _t(
            "Graphs & transforming functions",
            "10 min",
            """\
# Graphs & transforming functions

A graph turns a formula into a picture. Four knobs reshape almost any curve:
**amplitude** (vertical stretch), **frequency** (horizontal squeeze),
**phase** (horizontal shift), and **offset** (vertical shift).

$$y = A\\,\\sin(\\omega x + \\varphi) + c.$$

Drag each one and watch the wave respond — this single family models AC voltage,
audio tones, vibrations and seasonal trends:

```plot
{"title": "Transform a wave: A·sin(ωx + φ) + c", "xLabel": "x", "yLabel": "y", "xRange": [-6.283, 6.283], "yRange": [-4, 4], "controls": [{"name": "A", "range": [0.2, 3], "value": 1.5, "label": "amplitude A"}, {"name": "w", "range": [0.3, 3], "value": 1, "label": "frequency ω"}, {"name": "p", "range": [-3.14, 3.14], "value": 0, "label": "phase φ"}, {"name": "c", "range": [-2, 2], "value": 0, "label": "offset c"}], "functions": [{"expr": "A*sin(w*x + p) + c", "label": "y", "color": "#2563eb"}]}
```

## Roots & intersections

Where a curve crosses $y=0$ are its **roots** (solutions); where two curves meet
is where their equations are equal — exactly what a solver, a break-even
analysis, or a physics collision check computes.

```plot
{"title": "Roots and an intersection", "xLabel": "x", "yLabel": "y", "xRange": [-3, 3], "yRange": [-4, 6], "functions": [{"expr": "x^2 - 2", "label": "f(x) = x² − 2", "color": "#2563eb"}, {"expr": "x", "label": "g(x) = x", "color": "#16a34a"}], "points": [{"x": 2, "y": 2, "label": "f = g", "color": "#dc2626", "size": 7}, {"x": -1, "y": -1, "color": "#dc2626", "size": 7}]}
```

**Next:** how fast a curve changes — the derivative.
""",
        ),
        _t(
            "Rates of change: the derivative",
            "11 min",
            """\
# Rates of change: the derivative

The **derivative** $f'(x)$ is the *instantaneous rate of change* — the slope of
the curve at a point. It's speed from position, marginal cost from cost, current
from charge, and the gradient a neural network follows while training.

$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}.$$

Geometrically it's the slope of the **tangent line**. Slide the point along
$f(x)=x^2$ and watch the tangent tilt — its slope is exactly $f'(x) = 2x$ (zero
at the bottom, steep at the sides):

```plot
{"title": "The derivative is the slope of the tangent", "xLabel": "x", "yLabel": "f(x)", "xRange": [-3, 3], "yRange": [-2, 9], "controls": [{"name": "a", "range": [-2.5, 2.5], "value": 1, "label": "point a"}], "functions": [{"expr": "x^2", "label": "f(x) = x²", "color": "#2563eb"}], "parametric": [{"x": "a + u", "y": "a^2 + 2*a*u", "param": "u", "range": [-2, 2], "color": "#dc2626", "label": "tangent (slope 2a)"}], "points": [{"xExpr": "a", "yExpr": "a^2", "color": "#dc2626", "size": 7, "label": "a"}]}
```

A few rules cover most cases:

| $f(x)$ | $f'(x)$ |
|--------|---------|
| $x^n$ | $n x^{n-1}$ |
| $e^{x}$ | $e^{x}$ |
| $\\sin x$ | $\\cos x$ |
| $\\ln x$ | $1/x$ |

Where $f'=0$ the curve is flat — a **maximum or minimum**. That's why
optimization (the next course) hunts for points where the derivative vanishes.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Mathematics — Intermediate ───────────────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="math-intermediate",
    title="Mathematics — Intermediate",
    description=(
        "The working toolkit: vectors and linear algebra, matrices as "
        "transformations and linear systems, derivatives in depth (chain rule, "
        "partials, gradients) and integrals as accumulated area — the math "
        "behind graphics, robotics, signals and machine learning."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Vectors & linear algebra",
            "12 min",
            """\
# Vectors & linear algebra

A **vector** is a list of numbers with direction and magnitude:
$\\vec{u} = (u_1, u_2, \\dots)$. It's a point in space, a force, an RGB colour, a
row of features fed to a model — all the same object.

## Adding vectors

Vectors add tip-to-tail: $\\vec{u} + \\vec{v}$ closes the triangle. Rotate
$\\vec{v}$ and watch the sum move — this is how displacements, velocities and
forces combine:

```plot
{"title": "Vector addition: u + v", "equal": true, "xRange": [-1, 5], "yRange": [-1, 4], "controls": [{"name": "ang", "range": [0, 180], "value": 60, "label": "direction of v (°)"}], "vectors": [{"x": 3, "y": 0, "from": [0, 0], "label": "u", "color": "#2563eb"}, {"xExpr": "2*cos(rad(ang))", "yExpr": "2*sin(rad(ang))", "from": [3, 0], "label": "v", "color": "#16a34a"}, {"xExpr": "3 + 2*cos(rad(ang))", "yExpr": "2*sin(rad(ang))", "from": [0, 0], "label": "u + v", "color": "#dc2626"}]}
```

## Dot product

$\\vec{u}\\cdot\\vec{v} = \\sum u_i v_i = |\\vec u|\\,|\\vec v|\\cos\\theta$ measures
**alignment**. It powers similarity search, projections, and the "how much of
this direction?" question — a single dot product is the core of a neural network
neuron and of cosine similarity in search engines.

**Next:** matrices — vectors transformed in bulk.
""",
        ),
        _t(
            "Matrices, systems & transformations",
            "13 min",
            """\
# Matrices, systems & transformations

A **matrix** is a grid of numbers that **transforms** vectors: $\\vec{y} = A\\vec{x}$.
Every rotation, scaling, projection and shear in graphics and robotics is a
matrix.

## A rotation matrix

$$R(\\theta) = \\begin{bmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{bmatrix}.$$

Its **columns are where the basis vectors land**. Spin $\\theta$ and watch
$\\hat{x}$ and $\\hat{y}$ rotate together — exactly what happens to every pixel
when you rotate an image or to a robot arm's frame:

```plot
{"title": "A rotation matrix turns the basis vectors", "equal": true, "xRange": [-1.5, 1.5], "yRange": [-1.5, 1.5], "controls": [{"name": "th", "range": [0, 360], "value": 30, "label": "angle θ (°)"}], "vectors": [{"xExpr": "cos(rad(th))", "yExpr": "sin(rad(th))", "from": [0, 0], "label": "R·x̂", "color": "#dc2626"}, {"xExpr": "-sin(rad(th))", "yExpr": "cos(rad(th))", "from": [0, 0], "label": "R·ŷ", "color": "#16a34a"}]}
```

## A linear map reshapes everything

Apply a diagonal scaling to *every* point on a circle and it becomes an ellipse.
The stretch factors are the matrix's **eigenvalues** — the idea behind PCA, data
whitening and stability analysis:

```plot
{"title": "A linear map sends a circle to an ellipse", "equal": true, "xRange": [-3, 3], "yRange": [-3, 3], "controls": [{"name": "sx", "range": [0.3, 2.5], "value": 2, "label": "scale x"}, {"name": "sy", "range": [0.3, 2.5], "value": 1, "label": "scale y"}], "parametric": [{"x": "cos(s)", "y": "sin(s)", "param": "s", "range": [0, 6.283], "color": "#cbd5e1", "label": "unit circle"}, {"x": "sx*cos(s)", "y": "sy*sin(s)", "param": "s", "range": [0, 6.283], "color": "#2563eb", "label": "image (ellipse)"}]}
```

## Solving systems

$A\\vec{x} = \\vec{b}$ asks "what input produces this output?" — circuit node
equations, structural loads, balancing chemical reactions, and the least-squares
fit behind linear regression are all this one equation, solved by elimination or
matrix inverse.

**Next:** derivatives in higher dimensions — gradients.
""",
        ),
        _t(
            "Derivatives, gradients & optimization",
            "13 min",
            """\
# Derivatives, gradients & optimization

With several inputs, each variable has its own **partial derivative**
$\\partial f / \\partial x_i$ (rate of change in that direction, holding the rest
fixed). Stack them into the **gradient**:

$$\\nabla f = \\Big(\\tfrac{\\partial f}{\\partial x}, \\tfrac{\\partial f}{\\partial y}, \\dots\\Big),$$

which points **uphill**, in the direction of steepest increase. The **chain
rule** — $\\dfrac{d}{dt} f(g(t)) = f'(g)\\,g'(t)$ — is what lets backpropagation
push gradients through a deep network.

## Gradient descent

To *minimise* (a loss, an error, an energy), step **downhill**:
$x \\leftarrow x - \\eta\\, f'(x)$. Press **Play** and watch the iterate roll into
the minimum of $f(x)=x^2$ — this is how essentially every machine-learning model
is trained:

```plot
{"title": "Gradient descent rolls downhill to the minimum", "xLabel": "x", "yLabel": "loss f(x)", "xRange": [-3, 3], "yRange": [0, 9], "animate": {"param": "t", "range": [0, 3], "label": "iteration (time)"}, "functions": [{"expr": "x^2", "label": "f(x) = x²", "color": "#2563eb"}], "points": [{"xExpr": "2.5*exp(-2*t)", "yExpr": "(2.5*exp(-2*t))^2", "label": "current x", "color": "#dc2626", "size": 7, "trail": true}]}
```

In higher dimensions the loss is a **surface**. Here is a saddle $f(x,y)=x^2-y^2$
— **rotate and tilt** it: a minimum along one axis, a maximum along the other.
Saddle points are exactly what makes high-dimensional optimization tricky:

```plot
{"mode": "3d", "title": "A loss surface with a saddle: f(x,y) = x² − y²", "xRange": [-3, 3], "yRange": [-3, 3], "zRange": [-9, 9], "azimuth": 40, "elevation": 25, "zLabel": "f", "surfaces": [{"expr": "x^2 - y^2", "color": "#9333ea"}]}
```

**Next:** the opposite of the derivative — the integral.
""",
        ),
        _t(
            "Integrals: accumulation & area",
            "12 min",
            """\
# Integrals: accumulation & area

If the derivative is a *rate*, the **integral** is the *total accumulated*. It is
the area under a curve:

$$\\int_a^b f(x)\\,dx = \\text{(area between } f \\text{ and the axis)}.$$

The **Fundamental Theorem of Calculus** ties them together: integrating a rate
recovers the quantity. Distance is the integral of speed; energy is the integral
of power; charge is the integral of current; probability is the area under a
density.

Press **Play** to sweep the upper limit $b$: the moving dot is the **running
area** under $\\sin x$, which traces out its integral $1 - \\cos x$:

```plot
{"title": "Integral = accumulated area", "xLabel": "x", "yLabel": "y", "xRange": [0, 6.283], "yRange": [-1.3, 2.3], "animate": {"param": "b", "range": [0, 6.283], "label": "upper limit b"}, "functions": [{"expr": "sin(x)", "label": "rate f(x) = sin x", "color": "#2563eb"}, {"expr": "1 - cos(x)", "label": "total ∫₀ˣ f = 1 − cos x", "color": "#16a34a"}], "points": [{"xExpr": "b", "yExpr": "1 - cos(b)", "label": "area so far", "color": "#dc2626", "size": 7, "trail": true}]}
```

When $\\sin x$ is positive the area grows; once it goes negative (after $\\pi$) the
running total falls again — area below the axis counts as negative.

In code you rarely integrate by hand: you sum many thin slices (a **Riemann
sum**), which is exactly what `numpy.trapz` or an ODE solver does numerically —
the topic of the Advanced course.

**Next:** test what you've learned.
""",
        ),
        _quiz(),
    ),
)

# ── Mathematics — Advanced ───────────────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="math-advanced",
    title="Mathematics — Advanced",
    description=(
        "Differential equations and beyond: first/second-order ODEs, the big "
        "three PDEs (heat, wave, Laplace), graph theory for networks and "
        "algorithms, and a runnable numerical lab — the continuous-math core of "
        "simulation, control and scientific computing."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Ordinary differential equations (ODEs)",
            "13 min",
            """\
# Ordinary differential equations (ODEs)

An **ODE** relates a function to its own derivatives. It's the language of
*change*: how a quantity evolves given the rule for its rate.

## First order: dy/dt = k·y

"The rate of change is proportional to the amount" — the most common law in
nature. Its solution is an exponential $y = y_0 e^{kt}$. Slide $k$ from positive
(growth) to negative (decay): bank interest and bacteria for $k>0$; radioactive
decay, a cooling coffee and an RC circuit for $k<0$:

```plot
{"title": "dy/dt = k·y → exponential", "xLabel": "t", "yLabel": "y(t)", "xRange": [0, 4], "yRange": [0, 8], "controls": [{"name": "k", "range": [-1, 1], "value": 0.5, "label": "rate k"}], "functions": [{"expr": "exp(k*x)", "label": "y = y₀ e^(k t)", "color": "#2563eb"}]}
```

## Bounded growth: the logistic equation

Real growth saturates. $\\dot y = r\\,y(1 - y/K)$ gives the famous **S-curve** —
epidemics, product adoption, and the sigmoid that squashes a neuron's output:

```plot
{"title": "Logistic growth (S-curve): saturation", "xLabel": "t", "yLabel": "population", "xRange": [-6, 6], "yRange": [0, 1.05], "controls": [{"name": "r", "range": [0.5, 3], "value": 1.2, "label": "growth rate r"}], "functions": [{"expr": "1/(1 + exp(-r*x))", "label": "logistic", "color": "#16a34a"}]}
```

## Second order: oscillation & damping

$m\\ddot x + c\\dot x + k x = 0$ describes a mass-spring, an RLC circuit, a
suspension. The damping $c$ decides whether it rings or settles smoothly — the
same model you met in the Physics track, here as a general ODE:

```plot
{"title": "Damped second-order ODE", "xLabel": "t", "yLabel": "x(t)", "xRange": [0, 10], "yRange": [-1.2, 1.2], "animate": {"param": "t", "range": [0, 10], "label": "time"}, "controls": [{"name": "z", "range": [0, 1.5], "value": 0.3, "label": "damping ζ"}], "functions": [{"expr": "exp(-z*x)*cos(3*x)", "label": "x(t)", "color": "#9ca3af"}], "points": [{"xExpr": "t", "yExpr": "exp(-z*t)*cos(3*t)", "label": "state", "color": "#2563eb", "size": 7}]}
```

**Next:** when the unknown depends on *several* variables — PDEs.
""",
        ),
        _t(
            "Partial differential equations (PDEs)",
            "14 min",
            """\
# Partial differential equations (PDEs)

A **PDE** involves partial derivatives in **several variables** — usually space
*and* time. Three linear PDEs cover an enormous range of engineering.

## The wave equation

$$\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\frac{\\partial^2 u}{\\partial x^2}.$$

Disturbances **travel** at speed $c$ without changing shape — sound, light,
water ripples, signals on a wire, a guitar string. Press **Play** and change the
speed:

```plot
{"title": "Wave equation: a travelling wave", "xLabel": "position x", "yLabel": "u(x, t)", "xRange": [0, 12.566], "yRange": [-1.5, 1.5], "animate": {"param": "t", "range": [0, 12.566], "label": "time t"}, "controls": [{"name": "c", "range": [0.2, 2], "value": 1, "label": "wave speed c"}], "functions": [{"expr": "sin(x - c*t)", "label": "u = sin(x − c t)", "color": "#2563eb"}]}
```

## The heat (diffusion) equation

$$\\frac{\\partial u}{\\partial t} = \\alpha \\frac{\\partial^2 u}{\\partial x^2}.$$

Sharp features **smooth out** over time. A hot spot spreads and flattens — the
same math as a Gaussian blur in image processing, smoke dispersing, and option
pricing in finance. Play it:

```plot
{"title": "Heat equation: a hot spot spreading out", "xLabel": "position x", "yLabel": "temperature", "xRange": [-6, 6], "yRange": [0, 1.1], "animate": {"param": "t", "range": [0, 5], "label": "time t"}, "functions": [{"expr": "exp(-x^2 / (1 + 4*t)) / sqrt(1 + 4*t)", "label": "u(x, t)", "color": "#dc2626"}]}
```

## The steady state: shapes & modes

When time settles (Laplace's equation $\\nabla^2 u = 0$) or a membrane vibrates,
the solution is a 2D **mode shape**. **Rotate** this drum/plate mode
$u(x,y)=\\sin x\\,\\sin y$ — the basis of FEM simulation, antenna design and the
harmonics of a musical instrument:

```plot
{"mode": "3d", "title": "A 2D mode shape u(x,y) = sin x · sin y", "xRange": [-3.14, 3.14], "yRange": [-3.14, 3.14], "zRange": [-1, 1], "azimuth": 40, "elevation": 30, "zLabel": "u", "surfaces": [{"expr": "sin(x)*sin(y)", "color": "#2563eb"}]}
```

**Next:** discrete math for networks — graphs.
""",
        ),
        _t(
            "Graphs & graph theory",
            "12 min",
            """\
# Graphs & graph theory

A **graph** is a set of **nodes** (vertices) joined by **edges**. It models any
network: roads, the internet, social connections, task dependencies, molecules,
and the computation graph of a neural network.

```mermaid
flowchart LR
  A((A)) --- B((B))
  A --- C((C))
  B --- C
  C --- D((D))
  B --- D
```

The same graph as a plot — nodes as points, edges as lines:

```plot
{"title": "A graph: nodes & edges", "equal": true, "grid": false, "xRange": [-0.5, 4.5], "yRange": [-0.5, 3.5], "series": [{"points": [[0, 0], [2, 3]], "color": "#9ca3af"}, {"points": [[0, 0], [3, 1]], "color": "#9ca3af"}, {"points": [[2, 3], [3, 1]], "color": "#9ca3af"}, {"points": [[3, 1], [4, 3]], "color": "#9ca3af"}, {"points": [[2, 3], [4, 3]], "color": "#9ca3af"}], "points": [{"x": 0, "y": 0, "label": "A", "color": "#2563eb", "size": 9}, {"x": 2, "y": 3, "label": "B", "color": "#2563eb", "size": 9}, {"x": 3, "y": 1, "label": "C", "color": "#2563eb", "size": 9}, {"x": 4, "y": 3, "label": "D", "color": "#2563eb", "size": 9}]}
```

## The adjacency matrix

A graph is stored as a matrix $A_{ij} = 1$ if $i$ and $j$ are connected — linking
graph theory straight back to linear algebra (powers $A^n$ count paths of length
$n$):

| | A | B | C | D |
|---|---|---|---|---|
| **A** | 0 | 1 | 1 | 0 |
| **B** | 1 | 0 | 1 | 1 |
| **C** | 1 | 1 | 0 | 1 |
| **D** | 0 | 1 | 1 | 0 |

## What you compute on graphs

- **Shortest path** (Dijkstra / A\\*) — GPS routing, network packets.
- **Traversal** (BFS / DFS) — crawling, dependency resolution, build order.
- **Connectivity & components** — clusters in social networks.
- **Spanning trees / flow** — laying cable cheaply, max throughput.

These algorithms run on the structure above; the math just guarantees they're
correct and efficient.

**Next:** put the continuous methods to work in code.
""",
        ),
        _code(
            "Numerical lab: solve it in code",
            "12 min",
            """\
# Two numerical workhorses of engineering math — from scratch, no libraries.

# 1) Solve an ODE with Euler's method:  dy/dt = r*y*(1 - y/K)  (logistic growth)
#    Step forward in tiny increments: y_next = y + (dy/dt)*dt
r = 1.0
K = 100.0
dt = 0.1
y = 1.0
t = 0.0
for step in range(60):              # integrate 6 seconds
    y = y + r * y * (1.0 - y / K) * dt
    t = t + dt
print("logistic population after", round(t, 1), "s:", round(y, 2), "(saturates at K =", K, ")")

# 2) Gradient descent: minimise f(x) = (x - 3)^2,  f'(x) = 2*(x - 3)
#    Step downhill: x_next = x - lr * f'(x)
x = 0.0
lr = 0.1
for step in range(50):
    grad = 2.0 * (x - 3.0)
    x = x - lr * grad
print("gradient descent found x =", round(x, 4), "(true minimum at 3)")

# 3) Numerical integral of sin(x) on [0, pi] via a Riemann sum  (exact answer = 2)
n = 200
a = 0.0
b = 3.141592653589793
total = 0.0
width = (b - a) / n
for i in range(n):
    xi = a + (i + 0.5) * width      # midpoint rule
    # sin without importing math: 7-term Taylor series is plenty on [0, pi]
    s = xi
    term = xi
    k = 1
    while k <= 6:
        term = -term * xi * xi / ((2 * k) * (2 * k + 1))
        s = s + term
        k = k + 1
    total = total + s * width
print("integral of sin on [0, pi] ~", round(total, 4), "(exact = 2)")

# Try it yourself:
#   - Raise lr toward 1.0: faster descent, but too high overshoots/diverges.
#   - Change K or r and watch the saturation level and speed move.
#   - Increase n for a more accurate integral; shrink dt for a better ODE.
""",
        ),
        _quiz(),
    ),
)


MATH_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)

__all__ = ["MATH_COURSES"]
