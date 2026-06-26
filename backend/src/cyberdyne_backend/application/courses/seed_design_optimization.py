"""Engineering Design Optimization track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on optimizing engineering designs.
Starts from formulating objectives, design variables and constraints; builds
through gradient-based (KKT, line search, SQP) and gradient-free (GA, PSO)
methods; and reaches multi-objective, surrogate-based and robust optimization.
Lessons are `text` with LaTeX, interactive ```plot blocks (feasible regions,
convergence, Pareto fronts), ```mermaid workflows and runnable ```python/
```matlab code (SciPy/NumPy optimization loops).
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, ∇, λ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Engineering Design Optimization — Basics ─────────────────────────────────

_BASICS = SeedCourse(
    slug="design-optimization-basics",
    title="Engineering Design Optimization — Basics",
    description=(
        "The intuition and fundamentals of design optimization: turning a design "
        "problem into a standard mathematical program with an objective, design "
        "variables and constraints; understanding the feasible region, local vs "
        "global optima and convexity; reading optimality graphically; and the "
        "broad map of solution methods. Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is design optimization",
            "10 min",
            r"""
# What is design optimization

**Design optimization** is the systematic search for the design that is *best*
according to a measurable criterion, while respecting every requirement. Instead
of accepting the first feasible design, we let mathematics push the design toward
the boundary of what is achievable: lightest bracket that does not yield, cheapest
gearbox that meets the life target, most efficient wing that fits the envelope.

Every optimization problem has three ingredients: an **objective** (what we
minimize or maximize), **design variables** (what we are free to change) and
**constraints** (what must hold). Choosing them well is most of the work — a
sloppy formulation optimizes the wrong thing perfectly.

```mermaid
flowchart LR
  N["Design need"] --> V["Choose design variables x"]
  V --> O["Define objective f(x)"]
  O --> C["List constraints g, h"]
  C --> S["Solve the program"]
  S --> E["Interpret & verify"]
  E -->|"refine"| V
```

A toy example: minimize the mass of a solid round rod that must carry a tensile
load without yielding. The mass grows with cross-section area, while the stress
constraint sets a *minimum* area — the optimum sits exactly where the constraint
becomes active. Most engineering optima live on a constraint, not in the interior.

```plot
{"title": "Rod mass vs diameter (objective to minimize)", "xLabel": "diameter d (mm)", "yLabel": "mass m (kg)", "xRange": [0, 40], "yRange": [0, 12], "grid": true, "functions": [{"expr": "0.0061*x^2", "label": "m ~ d^2", "color": "#2563eb"}]}
```

**Next:** writing this down as a standard optimization problem.
""",
        ),
        _t(
            "The standard optimization problem",
            "11 min",
            r"""
# The standard optimization problem

Almost every method expects the problem in one canonical form. We **minimize** an
objective $f(\mathbf{x})$ over the design vector $\mathbf{x}\in\mathbb{R}^n$
subject to inequality and equality constraints:

$$\min_{\mathbf{x}} f(\mathbf{x}) \quad \text{s.t.}\quad
g_i(\mathbf{x}) \le 0,\; i=1\dots m, \quad
h_j(\mathbf{x}) = 0,\; j=1\dots p, \quad
\mathbf{x}^L \le \mathbf{x} \le \mathbf{x}^U.$$

Conventions matter: maximizing $f$ is just minimizing $-f$, and a constraint
"$\sigma \le \sigma_{\text{allow}}$" becomes $g=\sigma-\sigma_{\text{allow}}\le 0$.
The **bounds** $\mathbf{x}^L,\mathbf{x}^U$ are side constraints that keep variables
physical (a thickness cannot be negative). **Scaling** variables and constraints to
similar magnitudes is essential — solvers struggle when a length in metres sits
next to a stress in pascals.

```python
import numpy as np
from scipy.optimize import minimize

# Minimize a weighted sum, subject to g(x) <= 0 and bounds.
def f(x):      return x[0]**2 + 2.0 * x[1]**2
def g(x):      return 1.0 - x[0] - x[1]          # x0 + x1 >= 1  ->  g <= 0

cons = ({"type": "ineq", "fun": lambda x: -g(x)},)   # SciPy wants fun >= 0
res = minimize(f, x0=np.array([0.5, 0.5]), bounds=[(0, None), (0, None)],
               constraints=cons, method="SLSQP")
print(res.x, res.fun)   # active constraint: x0 + x1 == 1
```

Get the formulation right and the solver choice becomes a detail; get it wrong and
no solver will save you.

**Next:** the feasible region those constraints carve out.
""",
        ),
        _t(
            "Feasible region and constraints",
            "10 min",
            r"""
# Feasible region and constraints

The **feasible region** is the set of all design vectors that satisfy every
constraint and bound at once. Geometrically each inequality $g_i\le 0$ cuts the
space into an allowed half and a forbidden half; their intersection (further
sliced by equalities and bounds) is where the optimizer is permitted to roam.

A constraint is **active** at a point if it holds as an equality there ($g_i=0$) —
the design is pressed right against that limit. It is **inactive** if there is slack
($g_i<0$). Identifying which constraints will be active at the optimum is a core
engineering skill: a lightweight part is usually limited by stress *or* deflection,
rarely both at the exact same point.

```mermaid
flowchart TB
  S["Design space R^n"] --> B["Apply bounds xL <= x <= xU"]
  B --> I["Apply g(x) <= 0"]
  I --> E["Apply h(x) = 0"]
  E --> F["Feasible region (intersection)"]
  F --> A["Optimum often on active constraints"]
```

If the feasible region is **empty**, the problem is *infeasible* — the
requirements contradict each other and something must be relaxed. The plot shows a
constraint boundary $x_2 = 1 - x_1$; feasible designs sit on one side of it.

```plot
{"title": "A linear constraint boundary x1 + x2 = 1", "xLabel": "x1", "yLabel": "x2", "xRange": [0, 1.5], "yRange": [0, 1.5], "grid": true, "functions": [{"expr": "1 - x", "label": "g = 0 boundary", "color": "#dc2626"}]}
```

**Next:** what makes a point a minimum at all.
""",
        ),
        _t(
            "Local and global optima",
            "10 min",
            r"""
# Local and global optima

A point $\mathbf{x}^\*$ is a **local minimum** if no nearby feasible point has a
smaller objective; it is the **global minimum** if no feasible point anywhere is
smaller. The trouble is that most numerical methods are local: they walk downhill
and stop at the first valley they reach, which may not be the deepest.

Whether this matters depends on the landscape. A function with one bowl-shaped
valley has a single optimum, so local equals global. A **multimodal** function has
many valleys, and the starting point decides which one you land in.

```plot
{"title": "Multimodal objective: many local minima", "xLabel": "x", "yLabel": "f(x)", "xRange": [0, 10], "yRange": [-1.5, 1.5], "grid": true, "functions": [{"expr": "sin(x) + 0.2*x - 1", "label": "f(x)", "color": "#2563eb"}]}
```

Practical defenses against bad local optima: try **multiple random starts**, use
**global** (gradient-free) methods such as genetic algorithms or particle swarm,
or exploit problem structure when the function is **convex** (next lesson), where a
local optimum is guaranteed global.

```mermaid
flowchart LR
  M["Multimodal f"] --> R["Multistart local solvers"]
  M --> G["Global methods (GA, PSO)"]
  M --> C["Exploit convex structure"]
  R --> O["Best candidate optimum"]
  G --> O
  C --> O
```

**Next:** the property that makes optimization easy — convexity.
""",
        ),
        _t(
            "Convexity and why it matters",
            "10 min",
            r"""
# Convexity and why it matters

**Convexity** is the single most important property in optimization. A set is
convex if the straight segment between any two of its points stays inside the set; a
function is convex if its graph never bows above the chord joining two points:

$$f\big(\theta \mathbf{x} + (1-\theta)\mathbf{y}\big) \le
\theta f(\mathbf{x}) + (1-\theta) f(\mathbf{y}), \quad 0\le\theta\le 1.$$

A twice-differentiable $f$ is convex when its Hessian $\nabla^2 f$ is positive
semidefinite everywhere. The payoff is huge: for a **convex program** (convex
objective over a convex feasible set) every local minimum is the global minimum, so
a fast local method finds the true answer and you can *trust* it.

```plot
{"title": "Convex (one global min) vs nonconvex", "xLabel": "x", "yLabel": "f(x)", "xRange": [-3, 3], "yRange": [0, 9], "grid": true, "functions": [{"expr": "x^2", "label": "convex x^2", "color": "#16a34a"}, {"expr": "x^2 + 2*cos(3*x)", "label": "nonconvex", "color": "#dc2626"}]}
```

Linear and quadratic programs, and many norm-minimization problems, are convex.
Real mechanical designs (with stress, contact, buckling) are usually **nonconvex**,
but recognising convex *sub*problems lets you solve pieces reliably and reserve the
expensive global search for where it is truly needed.

```mermaid
flowchart LR
  P["Problem"] --> Q{"Convex?"}
  Q -->|"yes"| L["Local solver = global optimum"]
  Q -->|"no"| H["Global / multistart needed"]
```

**Next:** the menu of solution methods you can choose from.
""",
        ),
        _t(
            "A map of optimization methods",
            "10 min",
            r"""
# A map of optimization methods

There is no single best optimizer — the right tool depends on cost, smoothness and
dimensionality of the problem. The first big split is whether you can get
**derivatives** of the objective and constraints.

**Gradient-based** methods (steepest descent, Newton, SQP, interior-point) use
$\nabla f$ to march efficiently downhill; they are fast and scale to thousands of
variables, but need smooth functions and find only local optima. **Gradient-free**
methods (genetic algorithms, particle swarm, Nelder-Mead, simulated annealing) need
only function values, tolerate noise, discreteness and black boxes, and can escape
local optima — at the cost of many more evaluations.

```mermaid
flowchart TB
  O["Optimization methods"] --> D{"Derivatives available & cheap?"}
  D -->|"yes, smooth"| GB["Gradient-based: SQP, interior-point, Newton"]
  D -->|"no / noisy / black-box"| GF["Gradient-free: GA, PSO, Nelder-Mead, SA"]
  GB --> M{"Multiple objectives?"}
  GF --> M
  M -->|"yes"| MO["Multi-objective (Pareto, NSGA-II)"]
  M -->|"expensive sims"| SB["Surrogate-based optimization"]
```

A typical convergence history shows the objective dropping quickly then flattening
as the optimizer nears a stationary point — a useful sanity check that the run is
behaving.

```plot
{"title": "Typical convergence of an iterative optimizer", "xLabel": "iteration", "yLabel": "objective gap", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "f - f* ~ exp(-0.4 k)", "color": "#2563eb"}]}
```

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Design Optimization — Intermediate ───────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="design-optimization-intermediate",
    title="Engineering Design Optimization — Intermediate",
    description=(
        "The core quantitative machinery of optimization: gradients and the "
        "necessary conditions for an unconstrained minimum; line-search and "
        "Newton-type descent; the KKT conditions and Lagrange multipliers for "
        "constraints; penalty and SQP approaches; and the two workhorse "
        "gradient-free methods, genetic algorithms and particle swarm. "
        "Runnable Python optimization loops throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Gradients and optimality conditions",
            "12 min",
            r"""
# Gradients and optimality conditions

For a smooth unconstrained objective, calculus pins down where minima can live. The
**gradient** $\nabla f$ collects the partial derivatives and points in the
direction of steepest increase. A **necessary** first-order condition for a local
minimum is a *stationary point*, where the gradient vanishes:

$$\nabla f(\mathbf{x}^\*) = \mathbf{0}.$$

This is necessary but not sufficient — maxima and saddle points are stationary too.
The **second-order** test uses the Hessian $\nabla^2 f$: if it is positive definite
at a stationary point, that point is a strict local minimum; indefinite means a
saddle. Together these are the foundation every gradient method is built on.

```python
import numpy as np

def f(x):  return (x[0] - 1)**2 + 3*(x[1] + 2)**2
def grad(x): return np.array([2*(x[0]-1), 6*(x[1]+2)])

x = np.array([5.0, 5.0])
for _ in range(50):                       # steepest descent
    g = grad(x)
    if np.linalg.norm(g) < 1e-8:
        break
    x = x - 0.1 * g                       # step along -gradient
print(x)                                  # -> approx [1, -2], where grad = 0
```

The plot shows a 1-D slice: the minimum sits exactly where the slope (gradient) is
zero and the curve is locally bowl-shaped.

```plot
{"title": "Stationary point: gradient zero at the minimum", "xLabel": "x", "yLabel": "f(x)", "xRange": [-2, 4], "yRange": [0, 9], "grid": true, "functions": [{"expr": "(x-1)^2", "label": "f(x)", "color": "#2563eb"}]}
```

**Next:** how to actually descend — line search and Newton.
""",
        ),
        _t(
            "Line search and Newton methods",
            "12 min",
            r"""
# Line search and Newton methods

A descent method repeats two choices: a **direction** $\mathbf{p}_k$ and a **step
length** $\alpha_k$, updating $\mathbf{x}_{k+1}=\mathbf{x}_k+\alpha_k\mathbf{p}_k$.
**Steepest descent** uses $\mathbf{p}_k=-\nabla f$ — simple but slow and zig-zags in
ill-conditioned valleys. **Newton's method** uses curvature, solving
$\nabla^2 f\,\mathbf{p}_k=-\nabla f$, which gives quadratic convergence near the
optimum but needs the Hessian. **Quasi-Newton** methods (BFGS) build an approximate
Hessian from gradients — the practical default.

The step length is set by a **line search** that decreases $f$ "enough", typically
the Armijo (sufficient-decrease) condition with backtracking:

$$f(\mathbf{x}_k + \alpha \mathbf{p}_k) \le f(\mathbf{x}_k) +
c_1 \alpha\, \nabla f(\mathbf{x}_k)^\top \mathbf{p}_k.$$

```python
import numpy as np
def backtracking(f, grad, x, p, a=1.0, c1=1e-4, rho=0.5):
    fx, gx = f(x), grad(x)
    while f(x + a*p) > fx + c1*a*np.dot(gx, p):   # Armijo test
        a *= rho                                  # shrink the step
    return a
```

Newton converges in far fewer iterations than steepest descent on the same problem.

```plot
{"title": "Convergence: Newton vs steepest descent", "xLabel": "iteration", "yLabel": "objective gap", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-1.2*x)", "label": "Newton (fast)", "color": "#16a34a"}, {"expr": "exp(-0.25*x)", "label": "steepest descent", "color": "#dc2626"}]}
```

**Next:** adding constraints with KKT and Lagrange multipliers.
""",
        ),
        _t(
            "KKT conditions and Lagrange multipliers",
            "12 min",
            r"""
# KKT conditions and Lagrange multipliers

Constraints change the rules: the gradient need not vanish at the optimum, because
the constraints can hold the design back. The **Karush-Kuhn-Tucker (KKT)**
conditions generalise stationarity. At a constrained optimum $\mathbf{x}^\*$ there
exist multipliers $\lambda_i\ge 0$ (inequalities) and $\mu_j$ (equalities) with:

$$\nabla f + \sum_i \lambda_i \nabla g_i + \sum_j \mu_j \nabla h_j = \mathbf{0},
\quad \lambda_i g_i = 0, \quad g_i \le 0, \quad \lambda_i \ge 0.$$

The middle equation is **complementary slackness**: either a constraint is active
($g_i=0$) or its multiplier is zero. A multiplier is also the **shadow price** —
the rate at which the optimal objective improves if that constraint is loosened,
which tells the engineer exactly which requirement is "costing" the most.

```mermaid
flowchart LR
  K["KKT at x*"] --> S["Stationarity: grad L = 0"]
  K --> P["Primal feasibility: g<=0, h=0"]
  K --> D["Dual feasibility: lambda >= 0"]
  K --> C["Complementarity: lambda * g = 0"]
```

Geometrically, at the optimum the objective gradient is a non-negative combination
of the active constraint gradients: you cannot move downhill without violating a
binding constraint. The plot illustrates a contour value tangent to a constraint —
the hallmark of a KKT point.

```plot
{"title": "Objective contour tangent to a constraint at the optimum", "xLabel": "x1", "yLabel": "x2", "xRange": [0, 2], "yRange": [0, 2], "grid": true, "functions": [{"expr": "sqrt(abs(1 - (x-1)^2)) + 1", "label": "objective contour", "color": "#2563eb"}, {"expr": "2 - x", "label": "active constraint", "color": "#dc2626"}]}
```

**Next:** turning constraints into something a solver handles — penalty and SQP.
""",
        ),
        _t(
            "Penalty and SQP methods",
            "12 min",
            r"""
# Penalty and SQP methods

How do solvers actually enforce constraints? **Penalty methods** add a cost for
violations, turning a constrained problem into a sequence of unconstrained ones:

$$\phi(\mathbf{x}, r) = f(\mathbf{x}) + r \sum_i \max(0, g_i)^2 +
r \sum_j h_j^2.$$

As the penalty weight $r$ grows, the minimizer of $\phi$ approaches the true
constrained optimum, but large $r$ makes the problem ill-conditioned.
**Interior-point** (barrier) methods instead add a term that blows up *inside* the
feasible region near the boundary, keeping iterates feasible.

**Sequential Quadratic Programming (SQP)** is the gold standard for smooth
nonlinear problems: at each step it models the objective as a quadratic and the
constraints as linear, solves that QP for a search direction, then line-searches.
It honours the KKT conditions directly and converges fast.

```python
import numpy as np
from scipy.optimize import minimize

# Min f = (x-2)^2 + (y-1)^2  s.t.  x^2 + y^2 <= 1  (unit disk)
f    = lambda v: (v[0]-2)**2 + (v[1]-1)**2
con  = {"type": "ineq", "fun": lambda v: 1 - v[0]**2 - v[1]**2}   # g <= 0
res  = minimize(f, [0.0, 0.0], method="SLSQP", constraints=[con])
print(res.x, res.fun)   # optimum on the circle boundary (active constraint)
```

A penalized objective shows the violation cost rising steeply outside the feasible
range.

```plot
{"title": "Quadratic penalty for constraint x <= 1", "xLabel": "x", "yLabel": "penalty term", "xRange": [0, 3], "yRange": [0, 4], "grid": true, "functions": [{"expr": "(x>1)*(x-1)^2", "label": "r * max(0, x-1)^2", "color": "#dc2626"}]}
```

**Next:** when there are no gradients — genetic algorithms.
""",
        ),
        _t(
            "Genetic algorithms",
            "12 min",
            r"""
# Genetic algorithms

A **genetic algorithm (GA)** is a population-based, gradient-free search inspired by
natural selection. It needs only objective values, so it handles black-box
simulations, discrete or mixed variables, and rugged multimodal landscapes where
gradient methods get stuck.

A GA evolves a **population** of candidate designs through repeated cycles:
**evaluate** fitness, **select** the fitter parents (e.g. tournament selection),
**crossover** to recombine their variables into children, and **mutate** to inject
random variation that preserves diversity. Over generations the population drifts
toward good regions of the space.

```mermaid
flowchart LR
  I["Random population"] --> EV["Evaluate fitness f(x)"]
  EV --> SE["Selection"]
  SE --> CX["Crossover"]
  CX --> MU["Mutation"]
  MU --> EV2{"Converged?"}
  EV2 -->|"no"| EV
  EV2 -->|"yes"| B["Best design"]
```

```python
import numpy as np
from scipy.optimize import differential_evolution   # a GA-style global solver

# Rastrigin: highly multimodal, hard for local methods
def rastrigin(x):
    return 10*len(x) + np.sum(x**2 - 10*np.cos(2*np.pi*x))

bounds = [(-5.12, 5.12)] * 2
res = differential_evolution(rastrigin, bounds, seed=0, tol=1e-8)
print(res.x, res.fun)   # finds the global minimum near (0, 0)
```

The best-so-far fitness improves in steps as generations discover better basins —
slower than a gradient march, but robust to multimodality.

```plot
{"title": "GA best-so-far fitness over generations", "xLabel": "generation", "yLabel": "best objective", "xRange": [0, 30], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.15*x)", "label": "best-so-far", "color": "#16a34a"}]}
```

**Next:** a swarm-based alternative — particle swarm optimization.
""",
        ),
        _t(
            "Particle swarm optimization",
            "12 min",
            r"""
# Particle swarm optimization

**Particle swarm optimization (PSO)** is another population method, modelled on
flocking. Each **particle** is a candidate design with a position $\mathbf{x}_i$ and
a velocity $\mathbf{v}_i$. Particles remember their own best position
$\mathbf{p}_i$ (personal best) and share the swarm's best $\mathbf{g}$ (global
best), and each step nudges every particle toward both:

$$\mathbf{v}_i \leftarrow w\,\mathbf{v}_i + c_1 r_1 (\mathbf{p}_i - \mathbf{x}_i)
+ c_2 r_2 (\mathbf{g} - \mathbf{x}_i), \qquad
\mathbf{x}_i \leftarrow \mathbf{x}_i + \mathbf{v}_i.$$

The inertia weight $w$ balances exploration against exploitation; the cognitive
($c_1$) and social ($c_2$) coefficients weight personal vs collective memory.
PSO has few parameters, is trivial to implement, and like a GA needs no gradients.

```python
import numpy as np
def pso(f, lb, ub, n=30, iters=100, w=0.7, c1=1.5, c2=1.5, rng=np.random):
    X = rng.uniform(lb, ub, (n, len(lb)))         # positions
    V = np.zeros_like(X)                           # velocities
    P, Pv = X.copy(), np.array([f(x) for x in X])  # personal bests
    g = P[Pv.argmin()].copy()                      # global best
    for _ in range(iters):
        r1, r2 = rng.random(X.shape), rng.random(X.shape)
        V = w*V + c1*r1*(P - X) + c2*r2*(g - X)
        X = np.clip(X + V, lb, ub)
        fx = np.array([f(x) for x in X])
        better = fx < Pv
        P[better], Pv[better] = X[better], fx[better]
        g = P[Pv.argmin()].copy()
    return g, f(g)
```

The swarm's global-best objective falls quickly then refines as particles cluster
around the optimum.

```plot
{"title": "PSO global-best objective over iterations", "xLabel": "iteration", "yLabel": "global-best objective", "xRange": [0, 30], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.2*x)", "label": "global best", "color": "#2563eb"}]}
```

**Next:** check your understanding of the core methods.
""",
        ),
        _quiz(),
    ),
)


# ── Engineering Design Optimization — Advanced ───────────────────────────────

_ADVANCED = SeedCourse(
    slug="design-optimization-advanced",
    title="Engineering Design Optimization — Advanced",
    description=(
        "State-of-the-art and applied optimization: trading off competing goals "
        "with Pareto fronts and NSGA-II; replacing costly simulations with "
        "surrogate models and Bayesian optimization; designing for uncertainty "
        "via robust and reliability-based optimization; structural topology "
        "optimization; and gradient computation by adjoint and automatic "
        "differentiation. Runnable Python throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multi-objective optimization and Pareto fronts",
            "13 min",
            r"""
# Multi-objective optimization and Pareto fronts

Real designs balance **competing objectives** — lighter *and* stiffer, faster *and*
cheaper. With several objectives there is rarely one best design; instead there is a
set of **non-dominated** trade-offs. Design A **dominates** B if A is at least as
good on every objective and strictly better on one. The non-dominated set is the
**Pareto front**: moving along it, you can only improve one objective by sacrificing
another.

```plot
{"title": "Pareto front: mass vs deflection trade-off", "xLabel": "mass", "yLabel": "deflection", "xRange": [1, 5], "yRange": [0, 5], "grid": true, "functions": [{"expr": "1/(x-0.8)", "label": "Pareto front (non-dominated)", "color": "#2563eb"}]}
```

Two broad strategies: **scalarization** collapses objectives into one (e.g. a
weighted sum $\sum w_k f_k$, sweeping the weights to trace the front), or
**population methods** like **NSGA-II** that evolve a whole spread of solutions in a
single run using non-dominated sorting plus a crowding-distance measure to keep the
front diverse.

```mermaid
flowchart LR
  P["Population"] --> R["Non-dominated sorting (ranks)"]
  R --> CD["Crowding distance (diversity)"]
  CD --> SEL["Select by rank then spread"]
  SEL --> GA["Crossover + mutation"]
  GA --> P2{"Converged?"}
  P2 -->|"no"| R
  P2 -->|"yes"| F["Approximate Pareto front"]
```

The decision-maker then picks a single design from the front using preferences the
optimizer was never told — keeping engineering judgement in the loop. A weighted sum
cannot reach points on a non-convex part of a front, which is why dominance-based
methods are preferred for general problems.

**Next:** optimizing when each evaluation is a costly simulation.
""",
        ),
        _t(
            "Surrogate-based optimization",
            "13 min",
            r"""
# Surrogate-based optimization

When one objective evaluation is a multi-hour CFD or FEA run, you cannot afford the
thousands of calls a GA wants. **Surrogate-based optimization** builds a cheap
mathematical *model* of the expensive response from a handful of carefully chosen
samples, then optimizes the model — refining it where it matters.

The workflow: choose an initial **design of experiments** (Latin hypercube),
evaluate the true (expensive) function there, fit a **surrogate** (polynomial
response surface, radial basis function, or Kriging/Gaussian process), then use an
**infill criterion** to pick the next true evaluation, and repeat.

```mermaid
flowchart LR
  DOE["Latin-hypercube DOE"] --> EV["Run expensive sims"]
  EV --> FIT["Fit surrogate model"]
  FIT --> INF["Infill: where to sample next?"]
  INF --> EV2["Evaluate one new point"]
  EV2 --> FIT
  FIT --> OPT["Optimum on surrogate"]
```

```python
import numpy as np
from scipy.interpolate import Rbf            # radial-basis surrogate

# Expensive truth, sampled at a few points; fit a cheap surrogate.
truth   = lambda x: (x-2.0)**2 + 0.3*np.sin(6*x)
xs      = np.linspace(0, 4, 6)               # design of experiments
model   = Rbf(xs, truth(xs), function="multiquadric")
grid    = np.linspace(0, 4, 400)
x_star  = grid[np.argmin(model(grid))]       # optimize the surrogate
print(x_star, model(x_star))
```

```plot
{"title": "Surrogate model approximating an expensive response", "xLabel": "x", "yLabel": "response", "xRange": [0, 4], "yRange": [-1, 5], "grid": true, "functions": [{"expr": "(x-2)^2 + 0.3*sin(6*x)", "label": "true response", "color": "#dc2626"}, {"expr": "(x-2)^2", "label": "smooth surrogate", "color": "#2563eb"}]}
```

**Next:** spending samples intelligently with Bayesian optimization.
""",
        ),
        _t(
            "Bayesian optimization and acquisition functions",
            "13 min",
            r"""
# Bayesian optimization and acquisition functions

**Bayesian optimization (BO)** is the principled way to optimize an expensive,
black-box, possibly noisy function. It models the response with a **Gaussian
process (GP)** surrogate that predicts both a mean and an *uncertainty* at every
point, then uses an **acquisition function** to decide where to sample next —
balancing **exploitation** (sample where the mean is good) against **exploration**
(sample where uncertainty is high).

The most popular acquisition is **Expected Improvement (EI)**, which rewards points
likely to beat the best value seen so far. **Upper/Lower Confidence Bound** (mean
$\pm\,\kappa\sigma$) and **Probability of Improvement** are common alternatives.

```mermaid
flowchart LR
  D["Observed data"] --> GP["Fit Gaussian process (mean + variance)"]
  GP --> AQ["Maximize acquisition (e.g. EI)"]
  AQ --> X["Evaluate true f at chosen x"]
  X --> D
  GP --> R["Recommend best design"]
```

```python
import numpy as np
from scipy.stats import norm

def expected_improvement(mu, sigma, f_best, xi=0.01):
    # EI for minimization: improvement over current best f_best
    sigma = np.maximum(sigma, 1e-12)
    imp = f_best - mu - xi
    z = imp / sigma
    return imp * norm.cdf(z) + sigma * norm.pdf(z)
```

BO routinely finds good designs in tens of evaluations rather than thousands, which
is why it underpins modern automated design and machine-learning hyperparameter
tuning. The acquisition peaks where improvement is most likely — that is the next
point to simulate.

```plot
{"title": "Expected-improvement acquisition (peak = next sample)", "xLabel": "x", "yLabel": "acquisition", "xRange": [0, 6], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "exp(-(x-4)^2)", "label": "EI(x)", "color": "#16a34a"}]}
```

**Next:** designing for uncertainty — robust optimization.
""",
        ),
        _t(
            "Robust and reliability-based design optimization",
            "13 min",
            r"""
# Robust and reliability-based design optimization

A deterministic optimum often sits right on a constraint — perfect on paper, fragile
in reality, because manufacturing tolerances and loads vary. Two complementary
philosophies handle this. **Robust Design Optimization (RDO)** seeks designs whose
performance is *insensitive* to variation, typically minimizing a blend of the mean
and standard deviation of the response:

$$\min_{\mathbf{x}}\; \mu_f(\mathbf{x}) + k\,\sigma_f(\mathbf{x}).$$

**Reliability-Based Design Optimization (RBDO)** instead enforces that the
probability of constraint violation stays below a target — a chance constraint
$P[g(\mathbf{x},\mathbf{u}) > 0] \le P_f$, often evaluated with FORM/SORM or Monte
Carlo. The result is a design pulled *back* from the deterministic boundary by a
safety margin sized to the actual scatter, not a blanket factor of safety.

```mermaid
flowchart LR
  U["Uncertain inputs (tolerances, loads)"] --> P["Propagate uncertainty"]
  P --> M["Mean & variance of response"]
  M --> RDO["RDO: minimize mu + k*sigma"]
  P --> RB["Reliability: P[g>0] <= Pf"]
  RDO --> S["Robust / reliable optimum"]
  RB --> S
```

```python
import numpy as np
rng = np.random.default_rng(0)
def robust_objective(x, k=2.0, n=10000):
    # x is the nominal design; manufacturing adds Gaussian noise.
    samples = x + rng.normal(0, 0.1, n)
    f = (samples - 1.0)**2
    return f.mean() + k * f.std()          # penalize variability
```

A flat-bottomed (robust) optimum tolerates input scatter far better than a sharp
deterministic one, even if its nominal value is slightly worse.

```plot
{"title": "Sharp vs robust optimum under input scatter", "xLabel": "design x", "yLabel": "objective", "xRange": [-2, 4], "yRange": [0, 5], "grid": true, "functions": [{"expr": "4*(x-1)^2", "label": "sharp optimum", "color": "#dc2626"}, {"expr": "0.6*(x-1)^2 + 0.5", "label": "robust (flat) optimum", "color": "#16a34a"}]}
```

**Next:** letting the structure itself be the variable — topology optimization.
""",
        ),
        _t(
            "Topology optimization",
            "13 min",
            r"""
# Topology optimization

**Topology optimization** is the most general structural design problem: instead of
sizing a fixed shape, it decides *where material should exist at all* inside a design
domain. The domain is discretised into finite elements, each given a density
variable $\rho_e \in [0,1]$; the optimizer drives densities toward solid (1) or void
(0) to minimize **compliance** (maximize stiffness) under a material-volume budget:

$$\min_{\boldsymbol{\rho}}\; \mathbf{f}^\top\mathbf{u}(\boldsymbol{\rho})
\quad \text{s.t.}\quad \mathbf{K}(\boldsymbol{\rho})\mathbf{u}=\mathbf{f},\;
\sum_e \rho_e v_e \le V^\*.$$

The **SIMP** scheme (Solid Isotropic Material with Penalization) makes intermediate
densities inefficient via $E_e = \rho_e^{p} E_0$ with $p\approx 3$, pushing the
result to crisp solid/void. A **sensitivity filter** prevents checkerboarding and
mesh dependence. The output is the organic, load-path-following geometry now
ubiquitous in additive-manufactured brackets and aerospace parts.

```mermaid
flowchart LR
  D["Design domain + loads/BCs"] --> FE["FE analysis: K u = f"]
  FE --> SE["Sensitivity dC/drho (adjoint)"]
  SE --> FI["Density filter"]
  FI --> UP["Update densities (OC / MMA)"]
  UP --> FE
  UP --> R["Solid/void layout"]
```

```python
import numpy as np
# Optimality-criteria density update (core of the classic 99-line code)
def oc_update(rho, dC, vol_frac, move=0.2, eta=0.5):
    l1, l2 = 1e-9, 1e9
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        rho_new = np.clip(rho * (-dC / lmid)**eta,
                          np.maximum(0.0, rho - move),
                          np.minimum(1.0, rho + move))
        if rho_new.mean() > vol_frac:    # bisection on the volume constraint
            l1 = lmid
        else:
            l2 = lmid
    return rho_new
```

```plot
{"title": "SIMP penalization pushes densities to 0 or 1", "xLabel": "density rho", "yLabel": "stiffness fraction E/E0", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x^3", "label": "E/E0 = rho^3 (p=3)", "color": "#2563eb"}, {"expr": "x", "label": "linear (no penalty)", "color": "#dc2626"}]}
```

**Next:** computing the gradients that drive all of this — adjoints and autodiff.
""",
        ),
        _t(
            "Adjoint methods and automatic differentiation",
            "13 min",
            r"""
# Adjoint methods and automatic differentiation

Gradient-based optimization of large simulations lives or dies on how cheaply you
can get gradients. With $n$ design variables, **finite differences** need $n+1$
solver runs and are noisy — hopeless when $n$ is in the thousands (as in topology or
aerodynamic shape design). The **adjoint method** computes the full gradient of a
scalar objective at a cost *independent of $n$* — essentially one extra linear
solve.

For a response $J(\mathbf{u},\mathbf{x})$ with state $\mathbf{u}$ constrained by
$\mathbf{R}(\mathbf{u},\mathbf{x})=\mathbf{0}$, introduce the adjoint
$\boldsymbol{\psi}$ solving $(\partial\mathbf{R}/\partial\mathbf{u})^\top
\boldsymbol{\psi}=(\partial J/\partial\mathbf{u})^\top$; then the total derivative is

$$\frac{dJ}{d\mathbf{x}} = \frac{\partial J}{\partial \mathbf{x}}
- \boldsymbol{\psi}^\top \frac{\partial \mathbf{R}}{\partial \mathbf{x}}.$$

**Automatic differentiation (AD)** delivers the same exactness without hand-deriving
adjoints: it applies the chain rule to the actual code. **Reverse-mode** AD is the
discrete analogue of the adjoint — one backward sweep yields gradients for *all*
inputs, which is exactly why it powers modern ML and differentiable simulators.

```mermaid
flowchart LR
  X["Design x"] --> F["Forward solve R(u,x)=0"]
  F --> J["Objective J(u,x)"]
  J --> A["Adjoint solve for psi"]
  A --> G["Gradient dJ/dx (cost ~ 1 solve)"]
  G --> OPT["Gradient-based optimizer"]
```

```python
import numpy as np
# Reverse-mode AD with JAX: one call returns the full gradient vector.
import jax, jax.numpy as jnp
def J(x):                                   # scalar objective of many variables
    return jnp.sum((x - 2.0)**2) + jnp.sum(jnp.sin(x))
grad_J = jax.grad(J)                        # exact gradient, any dimension
print(grad_J(jnp.ones(1000)))              # 1000-D gradient in one sweep
```

The cost gap is dramatic: finite-difference effort scales with the number of design
variables, while adjoint/reverse-AD effort stays essentially flat.

```plot
{"title": "Gradient cost vs number of variables", "xLabel": "design variables n", "yLabel": "relative cost", "xRange": [1, 100], "yRange": [0, 100], "grid": true, "functions": [{"expr": "x", "label": "finite differences ~ n", "color": "#dc2626"}, {"expr": "2 + 0*x", "label": "adjoint / reverse-AD ~ const", "color": "#16a34a"}]}
```

**Next:** check your mastery of advanced optimization.
""",
        ),
        _quiz(),
    ),
)


DESIGN_OPTIMIZATION_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["DESIGN_OPTIMIZATION_COURSES"]
