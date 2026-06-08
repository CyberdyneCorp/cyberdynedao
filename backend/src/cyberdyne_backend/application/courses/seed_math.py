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


# ── Mathematics — Optimization & Backpropagation ─────────────────────────────

_OPTIMIZATION = SeedCourse(
    slug="math-optimization",
    title="Mathematics — Optimization & Backpropagation",
    description=(
        "The math that trains models and optimises systems: the multivariable "
        "chain rule and computational graphs, backpropagation (reverse-mode "
        "autodiff), linear programming, and convex quadratic optimization with "
        "Lagrange multipliers and the KKT conditions. Builds on the gradients "
        "and linear algebra from the Intermediate course."
    ),
    level="Advanced",
    lessons=(
        _t(
            "The chain rule & computational graphs",
            "12 min",
            """\
# The chain rule & computational graphs

Every model is a **composition** of simple steps. To differentiate it you only
need one rule applied repeatedly: the **chain rule**.

$$\\frac{d}{dx}\\,f\\big(g(x)\\big) = f'\\big(g(x)\\big)\\cdot g'(x).$$

"Multiply the local slopes along the path." For $h(x) = \\sin(x^2)$ the path is
$x \\to x^2 \\to \\sin(\\cdot)$, so $h'(x) = \\cos(x^2)\\cdot 2x$. Drag the point and
check the tangent matches that product:

```plot
{"title": "Chain rule: slope of a composite h(x) = sin(x²)", "xLabel": "x", "yLabel": "h(x)", "xRange": [-2.5, 2.5], "yRange": [-1.6, 1.6], "controls": [{"name": "a", "range": [-2.4, 2.4], "value": 1, "label": "point a"}], "functions": [{"expr": "sin(x^2)", "label": "h(x) = sin(x²)", "color": "#2563eb"}], "parametric": [{"x": "a + u", "y": "sin(a^2) + cos(a^2)*2*a*u", "param": "u", "range": [-1, 1], "color": "#dc2626", "label": "tangent, slope cos(a²)·2a"}], "points": [{"xExpr": "a", "yExpr": "sin(a^2)", "color": "#dc2626", "size": 7}]}
```

## Computational graphs

We draw a calculation as a **graph**: inputs and parameters flow forward through
operations to an output (a loss). This is literally how PyTorch, TensorFlow and
JAX represent a model.

```mermaid
flowchart LR
  x((x)) --> M1["× w"]
  w((w)) --> M1
  M1 --> A1["+ b"]
  b((b)) --> A1
  A1 --> R["ReLU"]
  R --> L["loss (y − ŷ)²"]
  y((y)) --> L
```

Each node has a simple **local derivative** with respect to its inputs. The
**multivariable chain rule** combines them: if a quantity feeds several paths,
you *add* the contributions from each path.

$$\\frac{\\partial L}{\\partial x} = \\sum_{\\text{paths}} \\;\\prod_{\\text{edges on path}} (\\text{local derivative}).$$

**Next:** doing this efficiently, backwards — backpropagation.
""",
        ),
        _t(
            "Backpropagation: gradients through a graph",
            "14 min",
            """\
# Backpropagation: gradients through a graph

**Backpropagation** is just the chain rule, organised to be cheap. Instead of
recomputing every path, it sweeps the graph **once forward** then **once
backward**.

1. **Forward pass.** Evaluate each node left → right, caching its output.
2. **Backward pass.** Start with $\\dfrac{\\partial L}{\\partial L}=1$ and push
   gradients right → left, multiplying by each node's local derivative
   (*reverse-mode automatic differentiation*).

Because every parameter's gradient comes out of a **single** backward sweep,
training a network with millions of weights costs about the same as one forward
pass — the reason deep learning is feasible at all.

## A tiny worked example

For one linear neuron $\\hat y = wx + b$ with squared-error loss
$L = (\\hat y - y)^2$:

$$\\frac{\\partial L}{\\partial \\hat y} = 2(\\hat y - y), \\quad
\\frac{\\partial L}{\\partial w} = 2(\\hat y - y)\\,x, \\quad
\\frac{\\partial L}{\\partial b} = 2(\\hat y - y).$$

Those gradients are exactly what the code lab computes. Gradient descent then
steps each weight downhill: $w \\leftarrow w - \\eta\\,\\partial L/\\partial w$.

## What training looks like

Over a loss surface in weight space, descent slides toward the minimum; the loss
falls epoch by epoch. **Rotate** the surface, then **Play** the training curve:

```plot
{"mode": "3d", "title": "Loss surface over two weights", "xRange": [-2, 3], "yRange": [-3, 2], "zRange": [0, 12], "azimuth": 40, "elevation": 28, "zLabel": "loss", "surfaces": [{"expr": "(x-1)^2 + (y+0.5)^2", "color": "#2563eb"}]}
```

```plot
{"title": "Training: loss drops as gradients update the weights", "xLabel": "epoch", "yLabel": "loss", "xRange": [0, 30], "yRange": [0, 1.05], "animate": {"param": "t", "range": [0, 30], "label": "epoch"}, "functions": [{"expr": "exp(-x/6)", "label": "loss(epoch)", "color": "#dc2626"}], "points": [{"xExpr": "t", "yExpr": "exp(-t/6)", "label": "now", "color": "#2563eb", "size": 7, "trail": true}]}
```

**Next:** optimization with hard constraints — linear programming.
""",
        ),
        _t(
            "Linear optimization (Linear Programming)",
            "13 min",
            """\
# Linear optimization (Linear Programming)

A **linear program** optimises a linear objective subject to linear
inequalities:

$$\\max_{\\vec x}\\; \\vec c^{\\,T}\\vec x \\quad \\text{s.t.}\\quad A\\vec x \\le \\vec b,\\;\\; \\vec x \\ge 0.$$

The constraints carve out a **feasible region** — a convex polygon (a *polytope*
in higher dimensions). The objective's contour lines are parallel straight
lines; pushing them as far as possible in the $\\vec c$ direction, the **optimum
sits at a corner (vertex)** of that region. That single fact is why the
**simplex** algorithm just walks from vertex to vertex.

Maximise $3x + 2y$ subject to $x + y \\le 4$, $x + 3y \\le 6$, $x,y \\ge 0$. Slide
the green iso-cost line — the last vertex it touches before leaving the region is
the optimum, $(3, 1)$ with value $11$:

```plot
{"title": "LP: maximise 3x + 2y over a feasible region", "xLabel": "x", "yLabel": "y", "xRange": [0, 5], "yRange": [0, 5], "controls": [{"name": "k", "range": [0, 16], "value": 6, "label": "iso-cost level 3x+2y = k"}], "functions": [{"expr": "4 - x", "label": "x + y ≤ 4", "color": "#94a3b8"}, {"expr": "(6 - x)/3", "label": "x + 3y ≤ 6", "color": "#cbd5e1"}, {"expr": "(k - 3*x)/2", "label": "iso-cost 3x+2y = k", "color": "#16a34a"}], "series": [{"points": [[0, 0], [4, 0], [3, 1], [0, 2], [0, 0]], "label": "feasible region", "color": "#2563eb"}], "points": [{"x": 3, "y": 1, "label": "optimum (3,1), k = 11", "color": "#dc2626", "size": 8}]}
```

## Where it shows up

- **Resource allocation / production planning** — maximise profit within
  material, labour and time limits.
- **Diet & blending problems** — cheapest mix meeting nutritional bounds.
- **Logistics & transportation** — minimise shipping cost across a network.
- **Scheduling and network flow** — assign jobs, route traffic.

Every LP has a **dual** LP whose optimum equals the primal's (strong duality);
the dual variables are the *shadow prices* — how much the optimum improves per
unit of relaxed constraint.

**Next:** curved objectives — quadratic optimization.
""",
        ),
        _t(
            "Quadratic optimization & Lagrange multipliers",
            "14 min",
            """\
# Quadratic optimization & Lagrange multipliers

A **quadratic program (QP)** has a quadratic objective and linear constraints:

$$\\min_{\\vec x}\\; \\tfrac{1}{2}\\,\\vec x^{\\,T} Q\\,\\vec x + \\vec c^{\\,T}\\vec x
\\quad \\text{s.t.}\\quad A\\vec x \\le \\vec b,\\; \\;E\\vec x = \\vec d.$$

When $Q$ is positive (semi)definite the objective is a **convex bowl**, so any
local minimum is the global one — the property that makes QPs reliable to solve.

## Least squares is a QP

Fitting a line $y = mx + b$ to data by minimising the sum of squared residuals
$\\sum (mx_i + b - y_i)^2$ is an **unconstrained convex QP**. Slide $m$ and $b$ to
shrink the gaps; the minimum has a closed form (the *normal equations*) and is
the backbone of regression:

```plot
{"title": "Least squares = unconstrained QP: fit a line", "xLabel": "x", "yLabel": "y", "xRange": [-0.5, 4.5], "yRange": [0, 6], "controls": [{"name": "m", "range": [0, 2], "value": 1, "label": "slope m"}, {"name": "b", "range": [-1, 2], "value": 0.5, "label": "intercept b"}], "functions": [{"expr": "m*x + b", "label": "fit y = m x + b", "color": "#dc2626"}], "series": [{"points": [[0, 1], [1, 2.1], [2, 2.9], [3, 4.2], [4, 5.1]], "label": "data", "color": "#2563eb"}], "points": [{"x": 0, "y": 1, "color": "#2563eb", "size": 6}, {"x": 1, "y": 2.1, "color": "#2563eb", "size": 6}, {"x": 2, "y": 2.9, "color": "#2563eb", "size": 6}, {"x": 3, "y": 4.2, "color": "#2563eb", "size": 6}, {"x": 4, "y": 5.1, "color": "#2563eb", "size": 6}]}
```

## Constraints: Lagrange multipliers

To minimise $f$ subject to an equality $g(\\vec x) = 0$, the optimum is where the
objective's contour is **tangent** to the constraint — i.e. their gradients are
parallel:

$$\\nabla f = \\lambda\\,\\nabla g.$$

Minimise $x^2 + y^2$ subject to $x + y = 2$. Grow the cost contour (radius $r$)
until it just **touches** the line — tangency happens at $(1,1)$, the
constrained minimum:

```plot
{"title": "Lagrange: min x²+y² s.t. x+y = 2 (tangency)", "equal": true, "xRange": [-0.5, 2.5], "yRange": [-0.5, 2.5], "controls": [{"name": "r", "range": [0.3, 2.2], "value": 1, "label": "cost contour radius r"}], "parametric": [{"x": "r*cos(s)", "y": "r*sin(s)", "param": "s", "range": [0, 6.283], "color": "#2563eb", "label": "cost contour x²+y² = r²"}], "functions": [{"expr": "2 - x", "label": "constraint x + y = 2", "color": "#16a34a"}], "points": [{"x": 1, "y": 1, "label": "optimum (1,1)", "color": "#dc2626", "size": 8}]}
```

For **inequality** constraints the generalisation is the **KKT conditions**
(stationarity, primal/dual feasibility, complementary slackness) — a constraint
either binds (active, $\\lambda > 0$) or is slack ($\\lambda = 0$).

## Where it shows up

- **Machine learning** — ridge regression, and the **SVM** margin is a QP.
- **Finance** — Markowitz portfolio: minimise variance ($\\vec x^T \\Sigma \\vec x$)
  at a target return.
- **Control** — **MPC** solves a QP every timestep to plan optimal actions.

**Next:** implement backprop and solve a QP in code.
""",
        ),
        _code(
            "Lab: backprop & a constrained QP in code",
            "12 min",
            """\
# Backprop on the simplest model + a constrained QP — from scratch, no libraries.

# Data roughly following  y = 1.0*x + 0.8
xs = [0.0, 1.0, 2.0, 3.0, 4.0]
ys = [0.9, 1.7, 2.9, 3.8, 4.7]
n = 5

# 1) LINEAR REGRESSION by gradient descent (this IS backprop for a 1-neuron net).
#    Model: yhat = w*x + b.  Loss: mean squared error.
#    Backprop gradients:  dL/dw = mean(2*(yhat-y)*x),  dL/db = mean(2*(yhat-y))
w = 0.0
b = 0.0
lr = 0.05
for epoch in range(3000):
    gw = 0.0
    gb = 0.0
    for i in range(n):
        yhat = w * xs[i] + b          # forward pass
        err = yhat - ys[i]
        gw = gw + 2.0 * err * xs[i]   # backward pass (chain rule)
        gb = gb + 2.0 * err
    w = w - lr * (gw / n)             # gradient-descent step
    b = b - lr * (gb / n)
print("fitted line:  y =", round(w, 3), "* x +", round(b, 3))

# 2) EQUALITY-CONSTRAINED QP:  min x^2 + y^2  s.t.  x + y = c
#    Lagrange:  2x = lambda, 2y = lambda  ->  x = y ;  with x + y = c  ->  x = y = c/2.
c = 2.0
x = c / 2.0
y = c / 2.0
print("constrained QP optimum:  x =", x, " y =", y, " cost =", x * x + y * y)

# 3) Sanity-check the QP numerically with projected gradient descent.
#    Step downhill on x^2+y^2, then project back onto the line x+y=c each step.
px = 0.0
py = 0.0
step = 0.1
for it in range(500):
    px = px - step * 2.0 * px
    py = py - step * 2.0 * py
    drift = (px + py - c) / 2.0       # project onto x + y = c
    px = px - drift
    py = py - drift
print("projected-GD optimum:    x =", round(px, 4), " y =", round(py, 4))

# Try it:
#   - Raise lr toward 0.2: faster fit, but too high diverges.
#   - Change c: the QP optimum is always x = y = c/2.
#   - Replace the data and watch the fitted slope/intercept track it.
""",
        ),
        _quiz(),
    ),
)


# ── Mathematics — Probability & Statistics ───────────────────────────────────

_PROBABILITY = SeedCourse(
    slug="math-probability",
    title="Mathematics — Probability & Statistics",
    description=(
        "Reasoning under uncertainty for engineers & data people: probability "
        "and events, random variables with expectation and variance, the "
        "distributions you actually meet (Bernoulli, Binomial, Poisson, Normal, "
        "Exponential), Bayes' theorem, and the Central Limit Theorem — with a "
        "Monte-Carlo code lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Probability, events & the long run",
            "11 min",
            """\
# Probability, events & the long run

**Probability** measures how likely an event is, on a scale from 0 (impossible)
to 1 (certain). Formally we have a **sample space** of outcomes; an **event** is
a subset of it, and $P(\\text{event}) = \\dfrac{\\text{favourable}}{\\text{total}}$
when outcomes are equally likely.

Three rules cover most of it:

- **Complement:** $P(\\text{not } A) = 1 - P(A)$.
- **Addition:** $P(A \\text{ or } B) = P(A) + P(B) - P(A \\text{ and } B)$.
- **Multiplication:** $P(A \\text{ and } B) = P(A)\\,P(B \\mid A)$; if $A,B$ are
  **independent**, $P(A \\text{ and } B) = P(A)\\,P(B)$.

## Conditional probability

$P(B \\mid A)$ is the probability of $B$ *given* $A$ happened. A probability tree
tracks it:

```mermaid
flowchart LR
  S(("start")) -->|"P(rain)=0.3"| R(("rain"))
  S -->|"P(dry)=0.7"| D(("dry"))
  R -->|"P(late|rain)=0.6"| RL["late"]
  D -->|"P(late|dry)=0.1"| DL["late"]
```

## Probability is the long-run frequency

Flip a fair coin many times and the fraction of heads settles toward $0.5$ — the
**Law of Large Numbers**. Press **Play** and watch the running estimate converge
(the wobble shrinks like $1/\\sqrt{n}$):

```plot
{"title": "Law of large numbers: estimate → true probability", "xLabel": "number of trials", "yLabel": "estimated P(heads)", "xRange": [1, 200], "yRange": [0, 1], "animate": {"param": "t", "range": [1, 200], "label": "trials"}, "functions": [{"expr": "0.5 + 0.45*sin(0.7*x)/sqrt(x)", "label": "running estimate", "color": "#2563eb"}, {"expr": "0.5", "label": "true p = 0.5", "color": "#16a34a"}], "points": [{"xExpr": "t", "yExpr": "0.5 + 0.45*sin(0.7*t)/sqrt(t)", "color": "#dc2626", "size": 6, "trail": true}]}
```

That convergence is exactly why **Monte-Carlo simulation**, casinos and A/B
tests work: enough samples and the average is reliable.

**Next:** summarising a random quantity — expectation & variance.
""",
        ),
        _t(
            "Random variables: expectation & variance",
            "12 min",
            """\
# Random variables: expectation & variance

A **random variable** $X$ assigns a number to each outcome (a die roll, a sensor
reading, tomorrow's demand). Its distribution is described by a **PMF** (discrete)
or **PDF** (continuous).

## Expectation — the mean

$$\\mathbb{E}[X] = \\sum_x x\\,P(x) \\quad\\text{or}\\quad \\int x\\,f(x)\\,dx.$$

It's the long-run **average** — the balance point of the distribution. A fair die
has $\\mathbb{E}[X] = 3.5$.

## Variance — the spread

$$\\operatorname{Var}(X) = \\mathbb{E}\\big[(X-\\mu)^2\\big] = \\mathbb{E}[X^2] - \\mu^2, \\qquad
\\sigma = \\sqrt{\\operatorname{Var}(X)}.$$

The **standard deviation** $\\sigma$ has the same units as $X$ and measures
typical distance from the mean. Drag the mean $\\mu$ (where the bell sits) and the
spread $\\sigma$ (how wide) — the markers show $\\mu$ and the $\\mu\\pm\\sigma$ band
that holds about 68% of the probability:

```plot
{"title": "Mean μ (centre) and spread σ of a distribution", "xLabel": "x", "yLabel": "density f(x)", "xRange": [-6, 8], "yRange": [0, 0.85], "controls": [{"name": "mu", "range": [-2, 4], "value": 1, "label": "mean μ"}, {"name": "sg", "range": [0.5, 3], "value": 1.5, "label": "std dev σ"}], "functions": [{"expr": "exp(-(x-mu)^2/(2*sg^2))/(sg*sqrt(2*pi))", "label": "f(x)", "color": "#2563eb"}], "points": [{"xExpr": "mu", "y": 0, "label": "μ = E[X]", "color": "#dc2626", "size": 7}, {"xExpr": "mu-sg", "y": 0, "label": "μ−σ", "color": "#16a34a", "size": 5}, {"xExpr": "mu+sg", "y": 0, "label": "μ+σ", "color": "#16a34a", "size": 5}]}
```

**Linearity** makes these easy to combine: $\\mathbb{E}[aX+b]=a\\mathbb{E}[X]+b$,
and for *independent* variables variances add. This is the backbone of error
propagation, risk and signal-to-noise ratios.

**Next:** the named distributions you'll keep meeting.
""",
        ),
        _t(
            "Distributions you'll actually use",
            "12 min",
            """\
# Distributions you'll actually use

A handful of distributions model most real situations.

- **Bernoulli / Binomial** — yes/no trials. Number of successes in $n$ tries
  (coin flips, click-through, defective parts).
- **Poisson** — counts of rare events in an interval (arrivals per minute, server
  requests, typos per page). One parameter, the rate $\\lambda$.
- **Uniform** — every value equally likely (an ideal random generator).
- **Exponential** — waiting time *until* the next event (time between arrivals,
  component lifetime). Memoryless.
- **Normal (Gaussian)** — the bell curve; sums of many small effects (measurement
  noise, heights), and the limit in the CLT lesson.

## The Gaussian

$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}\\,e^{-(x-\\mu)^2/(2\\sigma^2)}.$$

It's everywhere because of the Central Limit Theorem. Reshape it:

```plot
{"title": "The Normal (Gaussian) distribution", "xLabel": "x", "yLabel": "density", "xRange": [-8, 8], "yRange": [0, 0.85], "controls": [{"name": "mu", "range": [-3, 3], "value": 0, "label": "mean μ"}, {"name": "sg", "range": [0.5, 3], "value": 1, "label": "std dev σ"}], "functions": [{"expr": "exp(-(x-mu)^2/(2*sg^2))/(sg*sqrt(2*pi))", "label": "Normal(μ, σ)", "color": "#2563eb"}]}
```

## The Exponential (waiting times)

$$f(x) = \\lambda e^{-\\lambda x}, \\quad x \\ge 0, \\qquad \\mathbb{E}[X] = 1/\\lambda.$$

Higher rate $\\lambda$ → shorter waits. This models queue inter-arrival times and
time-to-failure in reliability engineering:

```plot
{"title": "Exponential: time until the next event", "xLabel": "wait time", "yLabel": "density", "xRange": [0, 6], "yRange": [0, 3], "controls": [{"name": "lam", "range": [0.3, 3], "value": 1, "label": "rate λ"}], "functions": [{"expr": "lam*exp(-lam*x)", "label": "λ e^(−λx)", "color": "#dc2626"}]}
```

## A discrete one: Poisson(λ = 3)

Counts come in spikes (a **PMF**), here the probability of seeing $k$ events when
the average is 3:

```plot
{"title": "Poisson(λ = 3) PMF", "xLabel": "count k", "yLabel": "P(k)", "xRange": [0, 11], "yRange": [0, 0.27], "grid": true, "series": [{"points": [[0, 0.0498], [1, 0.1494], [2, 0.224], [3, 0.224], [4, 0.168], [5, 0.1008], [6, 0.0504], [7, 0.0216], [8, 0.0081], [9, 0.0027], [10, 0.0008]], "label": "P(k)", "color": "#16a34a"}], "points": [{"x": 3, "y": 0.224, "label": "mode ≈ λ", "color": "#dc2626", "size": 6}]}
```

**Next:** updating beliefs with evidence — Bayes.
""",
        ),
        _t(
            "Bayes' theorem & inference",
            "13 min",
            """\
# Bayes' theorem & inference

**Bayes' theorem** flips a conditional probability — it tells you how to update a
belief when evidence arrives:

$$P(H \\mid E) = \\frac{P(E \\mid H)\\,P(H)}{P(E)} \\;\\;\\propto\\;\\; \\underbrace{P(E \\mid H)}_{\\text{likelihood}}\\cdot\\underbrace{P(H)}_{\\text{prior}}.$$

**posterior ∝ likelihood × prior.** It's the engine behind spam filters, medical
diagnosis, fault detection and all of Bayesian machine learning.

## The base-rate trap (a medical test)

A test is 99% accurate; a disease affects 1% of people. You test positive — odds
you're sick? Not 99%. Of 10,000 people, 100 are sick (≈99 test positive) and
9,900 are healthy (≈99 *false* positives). So

$$P(\\text{sick}\\mid +) = \\frac{99}{99 + 99} \\approx 50\\%.$$

Rare conditions make even good tests misleading — the **prior** dominates.

## Updating beliefs with data

Estimating a coin's bias (or a conversion rate): start from a flat prior and let
each observation reshape the **posterior**. Add heads and tails and watch the
belief sharpen and shift — exactly Bayesian A/B testing:

```plot
{"title": "Bayesian updating: posterior over a probability p", "xLabel": "p (probability of heads)", "yLabel": "belief density", "xRange": [0, 1], "yRange": [0, 4], "controls": [{"name": "h", "range": [0, 20], "value": 3, "step": 1, "label": "heads observed"}, {"name": "t", "range": [0, 20], "value": 1, "step": 1, "label": "tails observed"}], "functions": [{"expr": "x^h*(1-x)^t", "label": "posterior ∝ p^H (1−p)^T", "color": "#2563eb"}]}
```

With 0 observations it's flat (we know nothing); each head pushes the peak right,
each tail pushes it left, and more data makes it narrower (more certain).

**Next:** why the Normal keeps appearing — the CLT.
""",
        ),
        _t(
            "Sampling & the Central Limit Theorem",
            "11 min",
            """\
# Sampling & the Central Limit Theorem

We rarely measure a whole population — we take a **sample** and **estimate**.
Two results make that trustworthy.

- **Law of Large Numbers:** the sample mean converges to the true mean as $n$
  grows.
- **Central Limit Theorem (CLT):** for large $n$, the **sample mean** is
  approximately **Normal**, *whatever* the original distribution — with the same
  mean $\\mu$ but a standard deviation of $\\sigma/\\sqrt{n}$.

That $\\sqrt{n}$ is everything in statistics: to halve your error you need **four
times** the data. Increase the sample size $n$ and watch the distribution of the
sample mean tighten around the truth:

```plot
{"title": "CLT: the sample mean concentrates as n grows", "xLabel": "sample mean", "yLabel": "density", "xRange": [0, 6], "yRange": [0, 3], "controls": [{"name": "n", "range": [1, 50], "value": 1, "step": 1, "label": "sample size n"}], "functions": [{"expr": "exp(-(x-3)^2/(2/n))/sqrt(2*pi/n)", "label": "distribution of x̄", "color": "#2563eb"}], "points": [{"x": 3, "y": 0, "label": "true mean μ = 3", "color": "#dc2626", "size": 7}]}
```

## Confidence intervals

A 95% confidence interval is roughly $\\bar x \\pm 1.96\\,\\sigma/\\sqrt{n}$ — the
margin of error in every poll. Narrower bars need more samples, by that same
$\\sqrt{n}$ law.

Real uses: **A/B testing**, polling, quality control, Monte-Carlo error bars, and
estimating model accuracy from a test set.

**Next:** simulate it all in code.
""",
        ),
        _code(
            "Monte-Carlo lab: estimate π, mean/variance & Bayes",
            "12 min",
            """\
# Monte Carlo & statistics from scratch — no libraries.

# A tiny linear-congruential generator for repeatable 'random' numbers in [0, 1).
seed = 12345
rnd = []
for i in range(40000):
    seed = (1103515245 * seed + 12345) % 2147483648
    rnd.append(seed / 2147483648.0)

# 1) ESTIMATE pi: throw darts in a unit square; fraction inside the quarter circle * 4.
inside = 0
trials = 20000
for i in range(trials):
    xr = rnd[2 * i]
    yr = rnd[2 * i + 1]
    if xr * xr + yr * yr <= 1.0:
        inside = inside + 1
print("Monte-Carlo pi ~", round(4.0 * inside / trials, 4), "(true 3.1416)")

# 2) MEAN and VARIANCE of the uniform draws (expect mean 0.5, variance 1/12 = 0.0833).
total = 0.0
for i in range(trials):
    total = total + rnd[i]
mean = total / trials
sqsum = 0.0
for i in range(trials):
    d = rnd[i] - mean
    sqsum = sqsum + d * d
var = sqsum / trials
print("sample mean ~", round(mean, 4), " variance ~", round(var, 4), "(uniform: 0.5, 0.0833)")

# 3) BAYES update: prior Beta(1,1); after H heads and T tails the posterior mean is
#    (1 + H) / (2 + H + T).
heads = 7
tails = 3
postmean = (1.0 + heads) / (2.0 + heads + tails)
print("after", heads, "heads,", tails, "tails -> P(heads) estimate =", round(postmean, 3))

# Try it:
#   - Raise trials: the pi error shrinks like 1/sqrt(trials) (the CLT in action).
#   - Change heads/tails and watch the estimate move away from the 0.5 prior.
""",
        ),
        _quiz(),
    ),
)

# ── Mathematics — Fourier & Signals ──────────────────────────────────────────

_FOURIER = SeedCourse(
    slug="math-fourier",
    title="Mathematics — Fourier & Signals",
    description=(
        "How signals are built, transformed and filtered: sinusoids and complex "
        "exponentials, Fourier series, the Fourier transform and the frequency "
        "domain, sampling and aliasing (Nyquist/DFT), and filtering by "
        "convolution — the math behind audio, communications, control and image "
        "processing, with a pure-Python signals lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Signals, sinusoids & complex exponentials",
            "12 min",
            """\
# Signals, sinusoids & complex exponentials

A **signal** is a value that varies over time (or space). The building block is
the **sinusoid**:

$$x(t) = A\\,\\cos(\\omega t + \\varphi),$$

with **amplitude** $A$, **angular frequency** $\\omega = 2\\pi f$, and **phase**
$\\varphi$. The deep idea — **Euler's formula** — packs cosine and sine into one
rotating complex exponential:

$$e^{i\\theta} = \\cos\\theta + i\\sin\\theta.$$

So a sinusoid is the shadow (real part) of a vector — a **phasor** — spinning at
rate $\\omega$. Press **Play**: the phasor rotates…

```plot
{"title": "A phasor e^{iωt} rotating", "equal": true, "xRange": [-1.3, 1.3], "yRange": [-1.3, 1.3], "animate": {"param": "t", "range": [0, 6.283], "label": "ωt"}, "controls": [{"name": "w", "range": [1, 4], "value": 1, "step": 1, "label": "cycles"}], "parametric": [{"x": "cos(s)", "y": "sin(s)", "param": "s", "range": [0, 6.283], "color": "#cbd5e1", "label": "unit circle"}], "vectors": [{"xExpr": "cos(w*t)", "yExpr": "sin(w*t)", "from": [0, 0], "label": "e^{iωt}", "color": "#dc2626"}]}
```

…and its horizontal shadow traces a cosine:

```plot
{"title": "Its real part is a cosine", "xLabel": "t", "yLabel": "cos(ωt)", "xRange": [0, 6.283], "yRange": [-1.2, 1.2], "animate": {"param": "t", "range": [0, 6.283], "label": "ωt"}, "controls": [{"name": "w", "range": [1, 4], "value": 1, "step": 1, "label": "cycles"}], "functions": [{"expr": "cos(w*x)", "label": "cos(ωt)", "color": "#2563eb"}], "points": [{"xExpr": "t", "yExpr": "cos(w*t)", "color": "#dc2626", "size": 6, "trail": true}]}
```

Phasors turn calculus on sinusoids into simple algebra — the reason all of AC
circuits, audio and communications is written in complex exponentials.

**Next:** building *any* periodic signal from sinusoids.
""",
        ),
        _t(
            "Fourier series: building waves from sinusoids",
            "13 min",
            """\
# Fourier series: building waves from sinusoids

**Fourier's idea:** *any* periodic signal is a sum of sinusoids — a fundamental
plus its **harmonics** (integer multiples of the base frequency):

$$x(t) = a_0 + \\sum_{k=1}^{\\infty} \\big(a_k\\cos k\\omega t + b_k\\sin k\\omega t\\big).$$

A square wave, for instance, is built from the **odd** harmonics:

$$\\text{square}(t) = \\frac{4}{\\pi}\\left(\\sin t + \\tfrac{1}{3}\\sin 3t + \\tfrac{1}{5}\\sin 5t + \\cdots\\right).$$

Add harmonics one at a time and watch the corners sharpen into a square (the
little overshoot at the edges that never quite goes away is the **Gibbs
phenomenon**):

```plot
{"title": "A square wave from sine harmonics", "xLabel": "x", "yLabel": "sum", "xRange": [-3.14, 9.42], "yRange": [-1.5, 1.5], "controls": [{"name": "N", "range": [1, 6], "value": 1, "step": 1, "label": "number of harmonics"}], "functions": [{"expr": "1.273*(sin(x) + if(N>=2,1,0)*sin(3*x)/3 + if(N>=3,1,0)*sin(5*x)/5 + if(N>=4,1,0)*sin(7*x)/7 + if(N>=5,1,0)*sin(9*x)/9 + if(N>=6,1,0)*sin(11*x)/11)", "label": "partial sum", "color": "#2563eb"}]}
```

The coefficients $a_k, b_k$ say *how much* of each harmonic is present — that list
of amounts is the signal's **spectrum**. This is exactly how a synthesizer builds
timbres and how an instrument's tone is its mix of harmonics.

**Next:** the spectrum as a transform — time ↔ frequency.
""",
        ),
        _t(
            "The Fourier transform & the frequency domain",
            "13 min",
            """\
# The Fourier transform & the frequency domain

The **Fourier transform** generalises the series to *any* signal: it rewrites a
function of **time** as a function of **frequency**, revealing which frequencies
it contains.

$$X(f) = \\int_{-\\infty}^{\\infty} x(t)\\,e^{-i 2\\pi f t}\\,dt.$$

A messy-looking signal in time can be a couple of clean spikes in frequency. Here
a signal is the sum of two tones — change their frequencies in the time view…

```plot
{"title": "A signal = sum of two tones (time domain)", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 6.283], "yRange": [-2.2, 2.2], "controls": [{"name": "f1", "range": [1, 6], "value": 2, "step": 1, "label": "tone 1 frequency"}, {"name": "f2", "range": [1, 6], "value": 5, "step": 1, "label": "tone 2 frequency"}], "functions": [{"expr": "sin(f1*x) + 0.6*sin(f2*x)", "label": "signal", "color": "#2563eb"}]}
```

…and the **spectrum** shows exactly two spikes at those frequencies, with heights
equal to the amplitudes:

```plot
{"title": "Its spectrum (frequency domain)", "xLabel": "frequency", "yLabel": "magnitude", "xRange": [0, 7], "yRange": [0, 1.3], "controls": [{"name": "f1", "range": [1, 6], "value": 2, "step": 1, "label": "tone 1 frequency"}, {"name": "f2", "range": [1, 6], "value": 5, "step": 1, "label": "tone 2 frequency"}], "vectors": [{"xExpr": "f1", "y": 1, "fromExpr": ["f1", "0"], "label": "tone 1", "color": "#dc2626"}, {"xExpr": "f2", "yExpr": "0.6", "fromExpr": ["f2", "0"], "label": "tone 2", "color": "#16a34a"}]}
```

The frequency domain is where you *see* what a signal is made of — which is why
it powers audio EQ and spectrum analysers, MRI reconstruction, JPEG/MP3
compression (drop the inaudible/invisible frequencies), and vibration analysis.

**Next:** doing this on a computer — sampling, the DFT and aliasing.
""",
        ),
        _t(
            "Sampling, the DFT & aliasing",
            "13 min",
            """\
# Sampling, the DFT & aliasing

Computers store signals as **samples** taken every $T_s$ seconds (sample rate
$f_s = 1/T_s$). The **Discrete Fourier Transform (DFT)** — computed fast by the
**FFT** — gives the spectrum of those samples and is one of the most-used
algorithms in all of engineering.

## The Nyquist limit

You can only faithfully capture frequencies **below half the sample rate**
($f_s/2$, the **Nyquist frequency**). Sample too slowly and a high frequency
masquerades as a low one — **aliasing**. Below, a fast wave (grey) and a slow
wave (red) pass through the *exact same samples* (dots): once sampled, you can't
tell them apart.

```plot
{"title": "Aliasing: too-slow sampling fakes a low frequency", "xLabel": "time (samples at integers)", "yLabel": "amplitude", "xRange": [0, 10], "yRange": [-1.3, 1.3], "functions": [{"expr": "cos(2*pi*0.9*x)", "label": "true: 0.9 cycles/sample", "color": "#94a3b8"}, {"expr": "cos(2*pi*0.1*x)", "label": "alias: 0.1 cycles/sample", "color": "#dc2626"}], "series": [{"points": [[0, 1], [1, 0.809], [2, 0.309], [3, -0.309], [4, -0.809], [5, -1], [6, -0.809], [7, -0.309], [8, 0.309], [9, 0.809], [10, 1]], "label": "samples", "color": "#2563eb"}]}
```

It's the wagon-wheels-spinning-backwards effect in film, and why every ADC has an
**anti-aliasing low-pass filter** before it, and why CD audio samples at 44.1 kHz
(just above twice the ~20 kHz of hearing).

## The DFT

For $N$ samples $x_n$, the DFT gives $N$ frequency bins:

$$X_k = \\sum_{n=0}^{N-1} x_n\\,e^{-i 2\\pi k n / N}.$$

The FFT computes this in $O(N\\log N)$ instead of $O(N^2)$ — the difference
between real-time audio and not.

**Next:** shaping signals — filtering & convolution.
""",
        ),
        _t(
            "Filtering & convolution",
            "12 min",
            """\
# Filtering & convolution

A **filter** keeps some frequencies and removes others. A **low-pass** filter
smooths (removes high-frequency noise); a **high-pass** sharpens (removes slow
drift); a **band-pass** isolates a range.

In the time domain a (linear, time-invariant) filter is **convolution** with the
filter's **impulse response** $h$:

$$y(t) = (x * h)(t) = \\int x(\\tau)\\,h(t-\\tau)\\,d\\tau.$$

A moving average is the simplest example. Here a clean signal carries
high-frequency noise; turn the noise gain down to watch the low-pass filter
recover the underlying wave:

```plot
{"title": "Low-pass filtering removes high-frequency noise", "xLabel": "time", "yLabel": "amplitude", "xRange": [0, 6.283], "yRange": [-1.8, 1.8], "controls": [{"name": "g", "range": [0, 1], "value": 1, "label": "noise let through"}], "functions": [{"expr": "sin(x) + g*0.5*sin(13*x)", "label": "signal + noise", "color": "#94a3b8"}, {"expr": "sin(x)", "label": "after low-pass", "color": "#2563eb"}]}
```

## The frequency response

The clean way to describe a filter is its **gain at each frequency**,
$|H(f)|$. A first-order low-pass passes low frequencies and rolls off past its
**cutoff** $f_c$. Slide the cutoff — everything left of it passes, everything
right is attenuated (this curve is a **Bode plot**):

```plot
{"title": "Low-pass frequency response |H(f)|", "xLabel": "frequency f", "yLabel": "gain", "xRange": [0, 10], "yRange": [0, 1.1], "controls": [{"name": "fc", "range": [0.5, 5], "value": 2, "label": "cutoff fc"}], "functions": [{"expr": "1/sqrt(1 + (x/fc)^2)", "label": "|H(f)|", "color": "#2563eb"}]}
```

**Convolution in time = multiplication in frequency** — the central theorem that
ties this whole course together. Filtering is used everywhere: audio EQ and noise
reduction, image blur/sharpen and edge detection, smoothing sensor data, and the
convolutional layers of a CNN.

**Next:** build a signal pipeline in code.
""",
        ),
        _code(
            "Signals lab: filter a signal & find its period",
            "12 min",
            """\
# Signals in pure Python: build a noisy periodic signal, filter it, find its period.

P = 8                 # true period (samples)
N = 64
sig = []
for i in range(N):
    phase = i % P
    tri = phase if phase <= P / 2 else P - phase     # a triangle wave of period P
    noise = ((i * 37 + 11) % 7 - 3) * 0.2            # small, repeatable wiggle
    sig.append(tri + noise)

# Center the signal (subtract its mean) for the period analysis below.
total = 0.0
for i in range(N):
    total = total + sig[i]
mean = total / N
cen = []
for i in range(N):
    cen.append(sig[i] - mean)

# 1) MOVING-AVERAGE low-pass filter (window 3): convolution with [1/3, 1/3, 1/3].
smooth = []
for i in range(N):
    lo = i - 1 if i - 1 >= 0 else 0
    hi = i + 1 if i + 1 < N else N - 1
    smooth.append((sig[lo] + sig[i] + sig[hi]) / 3.0)

roughraw = 0.0
roughsmooth = 0.0
for i in range(1, N):
    roughraw = roughraw + abs(sig[i] - sig[i - 1])
    roughsmooth = roughsmooth + abs(smooth[i] - smooth[i - 1])
print("roughness   raw:", round(roughraw, 2), "  smoothed:", round(roughsmooth, 2))

# 2) FIND THE PERIOD (a tiny pitch detector) via the average squared difference.
#    The lag that best matches the signal to a shifted copy of itself IS the period.
bestlag = 2
bestd = 1.0e18
for lag in range(2, 24):
    d = 0.0
    cnt = 0
    for i in range(N - lag):
        diff = cen[i] - cen[i + lag]
        d = d + diff * diff
        cnt = cnt + 1
    d = d / cnt
    if d < bestd:
        bestd = d
        bestlag = lag
print("detected period (samples):", bestlag, " (true period =", P, ")")

# Try it:
#   - Change P and watch the detected period follow it.
#   - Raise the noise scale; the moving average still recovers the trend.
#   - Widen the filter window (i-2 .. i+2) for stronger smoothing.
""",
        ),
        _quiz(),
    ),
)


MATH_COURSES: tuple[SeedCourse, ...] = (
    _BASICS,
    _INTERMEDIATE,
    _ADVANCED,
    _OPTIMIZATION,
    _PROBABILITY,
    _FOURIER,
)

__all__ = ["MATH_COURSES"]
