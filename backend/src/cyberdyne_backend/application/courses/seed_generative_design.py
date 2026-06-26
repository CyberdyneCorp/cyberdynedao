"""Generative Design & AI for CAD track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on goal-driven design automation: from
the intuition of letting requirements (loads, materials, constraints) generate
geometry, through quantitative design-space exploration with topology optimization
and metamodels, to state-of-the-art AI-assisted CAD (generative models, surrogate
neural nets, multi-objective candidate selection). Lessons are `text` with LaTeX,
interactive ```plot blocks, ```mermaid workflow diagrams and runnable
```python / ```matlab code.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Generative Design & AI for CAD — Basics ──────────────────────────────────

_BASICS = SeedCourse(
    slug="generative-design-basics",
    title="Generative Design & AI for CAD — Basics",
    description=(
        "The intuition behind generative design. Learn how a problem stated as "
        "goals, loads, materials and keep-out regions can drive a computer to "
        "propose geometry, how generative design differs from topology optimization "
        "and from traditional CAD, why one run yields many candidates, and how to "
        "read the trade-offs between them. Interactive plots and workflow diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is generative design?",
            "10 min",
            r"""
# What is generative design?

**Generative design** flips the usual CAD workflow. Instead of drawing a shape
and then checking whether it survives the loads, you state the *problem* — where
forces are applied, where the part bolts down, what material it is made of, how
heavy it may be — and let an algorithm *generate* geometry that satisfies the
goals. The engineer specifies **what** must be true; the computer searches for a
**how**.

The defining feature is that a single run returns **many** candidate designs, not
one. Each candidate trades objectives differently — lighter but more compliant,
stiffer but heavier — so the human curates rather than draws.

```mermaid
flowchart LR
  REQ["Requirements - loads, supports, material, mass limit"] --> ENG["Generative engine"]
  ENG --> C1["Candidate 1"]
  ENG --> C2["Candidate 2"]
  ENG --> C3["Candidate ..."]
  C1 --> SEL["Engineer selects + refines"]
  C2 --> SEL
  C3 --> SEL
```

The value over hand-drawn CAD grows with how hard the problem is to intuit. For a
simple bracket the engineer can guess a near-optimal shape; for a complex
multi-load casting, the design space is too large to explore by hand, and the
algorithm's reach over many evaluations pays off.

```plot
{"title": "Design quality vs candidates explored: by hand vs generative", "xLabel": "candidates explored", "yLabel": "best objective found (relative, higher better)", "xRange": [0, 50], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1 - exp(-0.12*x)", "label": "generative search", "color": "#16a34a"}, {"expr": "0.45 + 0.002*x", "label": "manual exploration", "color": "#dc2626"}]}
```

Tools such as Autodesk Fusion Generative Design, nTopology and Siemens NX
Topology Optimization put this within reach of a desktop.

**Next:** stating a generative problem as goals and constraints.
""",
        ),
        _t(
            "Goals, constraints and the design space",
            "11 min",
            r"""
# Goals, constraints and the design space

A generative problem is an **optimization problem** in disguise. Three
ingredients define it: **design variables** (what the algorithm may change),
**objectives** (what to minimize or maximize) and **constraints** (what must hold
no matter what). Formally,

$$\min_{\mathbf{x}\in\mathcal{D}}\; f(\mathbf{x})
\quad \text{s.t.}\quad g_j(\mathbf{x}) \le 0, \;\; h_k(\mathbf{x}) = 0.$$

Here $\mathbf{x}$ might be the material distribution in a volume; $f$ the mass or
compliance; $g_j$ the stress limit, displacement limit or manufacturing rule. The
set of all feasible $\mathbf{x}$ is the **design space** $\mathcal{D}$ — usually
enormous, which is why a search is needed.

The two regions that matter are the **preserve / keep regions** (bolt bosses,
bearing seats, mating faces you must not touch) and the **obstacle / keep-out
regions** (where material is forbidden — clearance for a cable, a moving arm).
Everything between is the design region the algorithm fills.

```mermaid
flowchart TB
  PROB["Generative problem"] --> DV["Design variables - material in design region"]
  PROB --> OBJ["Objectives - min mass / max stiffness"]
  PROB --> CON["Constraints - stress, displacement, keep-out"]
  DV --> SEARCH["Search the design space D"]
  OBJ --> SEARCH
  CON --> SEARCH
  SEARCH --> FEAS["Feasible candidate designs"]
```

Adding a constraint shrinks the feasible region: the more you demand, the smaller
the fraction of the design space that qualifies, so a well-posed problem balances
ambition against feasibility.

```plot
{"title": "Fraction of design space remaining feasible vs constraints", "xLabel": "number of active constraints", "yLabel": "feasible fraction", "xRange": [0, 8], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "feasible fraction shrinks", "color": "#2563eb"}]}
```

**Next:** how generative design relates to topology optimization.
""",
        ),
        _t(
            "Generative design vs topology optimization",
            "11 min",
            r"""
# Generative design vs topology optimization

The two terms are often confused. **Topology optimization** answers a precise
mathematical question: given one load case, one objective and a volume budget,
where should material go? It returns *one* optimized material layout for the
problem as posed.

**Generative design** is broader. It wraps optimization (often topology
optimization as its engine) in an automated loop that sweeps *multiple* objectives,
*multiple* materials and *multiple* manufacturing methods, and returns a whole
**portfolio** of candidates the engineer compares. Topology optimization is a
solver; generative design is a workflow around it.

```mermaid
flowchart LR
  SPEC["Problem spec"] --> GD["Generative design workflow"]
  GD --> M1["Material A, 3-axis CNC"]
  GD --> M2["Material B, additive"]
  GD --> M3["Material C, casting"]
  M1 --> TO1["Topology optimization run"]
  M2 --> TO2["Topology optimization run"]
  M3 --> TO3["Topology optimization run"]
  TO1 --> PORT["Portfolio of candidates"]
  TO2 --> PORT
  TO3 --> PORT
```

Both rely on the same underlying physics: minimize **compliance** $C =
\mathbf{U}^{\top}\mathbf{K}\mathbf{U}$ (equivalently maximize stiffness) for a
given amount of material. As the allowed volume fraction rises, the achievable
compliance falls — stiffer, but heavier:

```plot
{"title": "Achievable compliance vs allowed material volume fraction", "xLabel": "volume fraction", "yLabel": "minimum compliance (relative)", "xRange": [0.1, 1.0], "yRange": [0, 4], "grid": true, "functions": [{"expr": "0.3/x", "label": "compliance ~ 1/volume", "color": "#16a34a"}]}
```

A practical rule: reach for **topology optimization** when the problem is single,
well defined and you want the optimum; reach for **generative design** when you
want to explore many what-ifs and let manufacturing constraints shape the field.

**Next:** how the iterative engine actually proposes geometry.
""",
        ),
        _t(
            "How the generative engine iterates",
            "10 min",
            r"""
# How the generative engine iterates

Under the hood, the engine runs a loop. It proposes a material distribution,
simulates it with **finite element analysis (FEA)** to get stress and
displacement, scores it against the objectives and constraints, then nudges the
distribution toward better designs — and repeats until the result stops improving
(**convergence**).

```mermaid
flowchart LR
  INIT["Initial material field"] --> FEA["FEA solve - stress, displacement"]
  FEA --> SCORE["Score objectives + constraints"]
  SCORE --> UPD["Update material field"]
  UPD --> CONV{"Converged?"}
  CONV -->|"no"| FEA
  CONV -->|"yes"| OUT["Candidate geometry"]
```

Each loop is one full simulate-and-update step, and most engines report the
objective every iteration. A healthy run shows the objective falling quickly at
first and then flattening as it approaches the optimum:

```plot
{"title": "Objective vs iteration in a generative run", "xLabel": "iteration", "yLabel": "objective (relative, lower better)", "xRange": [0, 30], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.18*x)", "label": "objective convergence", "color": "#dc2626"}]}
```

You can watch convergence numerically with a simple stopping rule: stop when the
relative change in the objective drops below a tolerance.

```python
def converged(history, tol=1e-3):
    # True once the objective stops improving by more than tol (relative)
    if len(history) < 2:
        return False
    prev, curr = history[-2], history[-1]
    return abs(prev - curr) / (abs(prev) + 1e-12) < tol

obj = [1.0, 0.62, 0.41, 0.33, 0.305, 0.3041]
for k in range(2, len(obj) + 1):
    if converged(obj[:k]):
        print("converged at iteration", k - 1)   # converged at iteration 5
        break
```

More iterations and a finer mesh give a better answer but cost compute, so the
engineer sets a budget and a tolerance up front.

**Next:** the manufacturing constraints that keep candidates buildable.
""",
        ),
        _t(
            "Manufacturing constraints shape the result",
            "11 min",
            r"""
# Manufacturing constraints shape the result

An optimal shape on paper is useless if no machine can make it. Modern generative
engines fold the **manufacturing method** into the search so every candidate is
buildable. The same problem produces very different geometry depending on the
process you choose.

- **Additive (3D printing)** — organic, lattice-rich shapes; needs overhang/
  self-support rules and a minimum feature size.
- **Milling (3-axis / 5-axis)** — tool-accessible faces only; constrained by tool
  reach and draft.
- **Die casting** — needs **draft angles** and uniform wall thickness for ejection
  and cooling.
- **2.5D / sheet** — extrusion-like shapes with constant cross-section.

```mermaid
flowchart TB
  SPEC["Same problem spec"] --> ADD["Additive rules"]
  SPEC --> MILL["Milling rules"]
  SPEC --> CAST["Casting rules - draft, uniform wall"]
  ADD --> GA["Organic, lattice geometry"]
  MILL --> GM["Tool-accessible geometry"]
  CAST --> GC["Draughted, castable geometry"]
```

Constraints cost performance: a freely optimized (additive-style) part is usually
the lightest, while casting or milling rules force extra material, so mass rises
as you restrict the process. The trade-off is real and worth quantifying:

```plot
{"title": "Part mass vs manufacturing restriction (same stiffness target)", "xLabel": "process restriction level (0 = free, 5 = highly constrained)", "yLabel": "resulting mass (relative)", "xRange": [0, 5], "yRange": [0.8, 2], "grid": true, "functions": [{"expr": "1 + 0.18*x", "label": "mass grows with restriction", "color": "#dc2626"}]}
```

A minimum-feature-size rule, for instance, is what stops a lattice strut from
becoming thinner than the printer can resolve — so the chosen process directly
bounds the geometry.

**Next:** reading and comparing the candidate designs an engine produces.
""",
        ),
        _t(
            "Reading and comparing candidates",
            "10 min",
            r"""
# Reading and comparing candidates

A generative run hands you a gallery of candidates, each with metrics: mass,
maximum stress, displacement, **safety factor**, cost, manufacturing method. The
engineer's job is to *choose*. The key idea is that you cannot rank designs on one
number alone — you weigh competing objectives.

The honest way to compare is a **trade-off (Pareto) view**: plot one objective
against another. A design is **Pareto-optimal** (non-dominated) if no other
candidate is better in one objective without being worse in another. The frontier
of non-dominated designs is where good choices live.

```plot
{"title": "Trade-off frontier: mass vs compliance across candidates", "xLabel": "mass (kg)", "yLabel": "compliance (lower = stiffer)", "xRange": [1, 6], "yRange": [0, 3], "grid": true, "functions": [{"expr": "2.5/x", "label": "Pareto frontier - best trade-offs", "color": "#16a34a"}]}
```

A safety factor sanity-checks each candidate against its stress limit:

```python
def safety_factor(yield_stress, peak_stress):
    return yield_stress / peak_stress     # > 1 means it survives

candidates = [
    {"name": "A", "mass": 2.1, "peak_stress": 180.0},
    {"name": "B", "mass": 3.4, "peak_stress": 110.0},
    {"name": "C", "mass": 2.7, "peak_stress": 140.0},
]
yield_al = 250.0   # MPa (e.g. 6061-T6 aluminium)
for c in candidates:
    sf = safety_factor(yield_al, c["peak_stress"])
    print(c["name"], "mass", c["mass"], "SF", round(sf, 2), "ok" if sf >= 1.5 else "REJECT")
```

```mermaid
flowchart LR
  GALLERY["Candidate gallery + metrics"] --> FILTER["Filter by constraints - SF >= 1.5"]
  FILTER --> PARETO["Plot trade-offs - Pareto view"]
  PARETO --> CHOICE["Pick a non-dominated design"]
  CHOICE --> REFINE["Refine + validate in CAD/FEA"]
```

Filter out the infeasible (safety factor too low), then choose from the frontier
according to what the project values — lightness, cost or stiffness.

**Next:** check your understanding of generative-design fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Generative Design & AI for CAD — Intermediate ────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="generative-design-intermediate",
    title="Generative Design & AI for CAD — Intermediate",
    description=(
        "The quantitative core of design-space exploration. Covers the SIMP "
        "density method and compliance minimization, sensitivity analysis and "
        "filtering, design of experiments for sampling, surrogate models that "
        "replace the expensive solver, multi-objective optimization and the Pareto "
        "front, and constraint handling. Worked examples with plots, diagrams and "
        "Python."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Topology optimization with SIMP",
            "12 min",
            r"""
# Topology optimization with SIMP

The workhorse of generative geometry is **SIMP** — Solid Isotropic Material with
Penalization. The design region is meshed; each element $e$ gets a continuous
**density** $\rho_e \in [0,1]$ (the design variable). The optimizer minimizes
**compliance** (maximizes stiffness) under a volume budget $f$:

$$\min_{\boldsymbol{\rho}}\; C(\boldsymbol{\rho}) = \mathbf{U}^{\top}\mathbf{K}(\boldsymbol{\rho})\mathbf{U}
\quad \text{s.t.}\quad \frac{V(\boldsymbol{\rho})}{V_0} \le f,\;\; 0 < \rho_{\min} \le \rho_e \le 1.$$

To force densities toward solid (1) or void (0) rather than grey mush, each
element's stiffness is **penalized**:

$$E_e(\rho_e) = E_{\min} + \rho_e^{\,p}\,(E_0 - E_{\min}), \qquad p \approx 3.$$

The exponent $p$ makes intermediate densities mechanically inefficient, so the
optimizer avoids them. Higher $p$ sharpens the black-and-white result:

```plot
{"title": "SIMP stiffness interpolation E(rho) for penalty p = 3", "xLabel": "element density rho", "yLabel": "normalized stiffness E/E0", "xRange": [0, 1], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "x^3", "label": "E ~ rho^3 (penalized)", "color": "#2563eb"}, {"expr": "x", "label": "E ~ rho (no penalty)", "color": "#dc2626"}]}
```

```python
import numpy as np

def simp_stiffness(rho, E0=70e3, Emin=1e-3, p=3):
    # SIMP-interpolated Young modulus per element (MPa)
    return Emin + rho**p * (E0 - Emin)

rho = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
print((simp_stiffness(rho) / 70e3).round(3))   # [0. 0.016 0.125 0.422 1.]
```

```mermaid
flowchart LR
  MESH["Mesh design region"] --> RHO["Assign density rho_e to each element"]
  RHO --> KE["E_e = Emin + rho^p (E0 - Emin)"]
  KE --> FE["Assemble K, solve K U = F"]
  FE --> C["Compliance C = U^T K U"]
  C --> MIN["Minimize C s.t. volume <= f"]
```

The output is a near-binary density field — the optimized load path — that is
later smoothed into manufacturable geometry.

**Next:** the sensitivities that tell the optimizer which way to move.
""",
        ),
        _t(
            "Sensitivity analysis and filtering",
            "12 min",
            r"""
# Sensitivity analysis and filtering

To update densities efficiently, the optimizer needs **sensitivities** — how the
compliance changes if an element gets a little denser, $\partial C / \partial
\rho_e$. For compliance minimization with the **adjoint method** this is cheap and
analytic:

$$\frac{\partial C}{\partial \rho_e} = -p\,\rho_e^{\,p-1}\,(E_0 - E_{\min})\,
\mathbf{u}_e^{\top}\mathbf{k}_0\,\mathbf{u}_e \le 0,$$

where $\mathbf{u}_e$ is the element displacement and $\mathbf{k}_0$ the unit
element stiffness. The sensitivity is always non-positive: adding material never
increases compliance. Adding it where $\mathbf{u}_e^{\top}\mathbf{k}_0\mathbf{u}_e$
(the strain energy) is large helps most.

Raw SIMP suffers from **checkerboarding** and **mesh dependence**. The cure is a
**filter** that smooths densities (or sensitivities) over a radius $r_{\min}$,
weighting neighbours by distance:

$$\hat{s}_e = \frac{\sum_{i\in N_e} w(r_{ei})\,\rho_i\,s_i}{\rho_e\sum_{i\in N_e} w(r_{ei})},
\qquad w(r) = r_{\min} - r.$$

The filter enforces a minimum length scale, so results stop changing once the mesh
is fine enough relative to $r_{\min}$:

```plot
{"title": "Result variation vs mesh refinement (with and without filter)", "xLabel": "mesh refinement level", "yLabel": "design variation between meshes", "xRange": [1, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "with density filter (mesh-independent)", "color": "#16a34a"}, {"expr": "0.6 + 0.04*x", "label": "no filter (mesh-dependent)", "color": "#dc2626"}]}
```

```python
import numpy as np

def sensitivity_filter(rho, dc, coords, rmin):
    # Distance-weighted smoothing of compliance sensitivities (Sigmund filter)
    n = len(rho)
    dcn = np.zeros(n)
    for e in range(n):
        d = np.linalg.norm(coords - coords[e], axis=1)
        w = np.maximum(rmin - d, 0.0)             # linear hat weight
        dcn[e] = (w * rho * dc).sum() / (rho[e] * w.sum() + 1e-12)
    return dcn

coords = np.array([[0,0],[1,0],[2,0],[0,1],[1,1],[2,1]], float)
rho = np.full(6, 0.5); dc = np.array([-3,-1,-2,-2,-4,-1.0])
print(sensitivity_filter(rho, dc, coords, rmin=1.5).round(2))
```

```mermaid
flowchart LR
  FE["FE displacements u_e"] --> SENS["Adjoint sensitivity dC/drho"]
  SENS --> FILT["Density / sensitivity filter (rmin)"]
  FILT --> UPD["Density update step"]
  UPD --> CHECK{"Mesh-independent + no checkerboard?"}
  CHECK -->|"yes"| GOOD["Clean load path"]
```

**Next:** sampling the design space when the engine itself is a black box.
""",
        ),
        _t(
            "Design of experiments for exploration",
            "12 min",
            r"""
# Design of experiments for exploration

Beyond a single topology run, you often have a handful of high-level parameters
(rib count, wall thickness, fillet radius, material) and want to know how each
affects performance. Because each evaluation is a full simulation, you sample the
parameter space deliberately — **Design of Experiments (DOE)**.

A full-factorial grid needs $L^k$ runs for $L$ levels and $k$ factors and explodes
fast. **Latin Hypercube Sampling (LHS)** and **Sobol sequences** are
*space-filling*: they cover the space far better per sample, scaling with your
budget rather than exponentially with $k$.

```plot
{"title": "Runs required: full-factorial grid vs space-filling DOE", "xLabel": "number of factors k", "yLabel": "samples (relative)", "xRange": [1, 8], "yRange": [0, 260], "grid": true, "functions": [{"expr": "3^x", "label": "full factorial 3^k", "color": "#dc2626"}, {"expr": "25*x", "label": "space-filling (linear budget)", "color": "#16a34a"}]}
```

```python
import numpy as np

rng = np.random.default_rng(0)

def latin_hypercube(n, bounds):
    # n space-filling samples; bounds is (k, 2) of [lo, hi]
    k = len(bounds)
    cut = np.linspace(0, 1, n + 1)
    u = cut[:-1] + rng.random((n, k)) * (1.0 / n)
    for j in range(k):                          # de-correlate columns
        u[:, j] = rng.permutation(u[:, j])
    lo, hi = bounds[:, 0], bounds[:, 1]
    return lo + u * (hi - lo)

bounds = np.array([[2.0, 6.0],     # wall thickness (mm)
                   [2.0, 8.0],     # rib count
                   [1.0, 5.0]])    # fillet radius (mm)
X = latin_hypercube(15, bounds)
print(X.shape, X.min(axis=0).round(1), X.max(axis=0).round(1))
```

DOE feeds **sensitivity ranking**: fit a quick linear model and read which factor
moves the response most, so you drop the irrelevant ones and shrink the problem.

```mermaid
flowchart LR
  PARAMS["High-level parameters + ranges"] --> DOE["DOE - LHS / Sobol"]
  DOE --> RUNS["Batch of generative / FEA runs"]
  RUNS --> RANK["Rank factor influence"]
  RANK --> REDUCE["Fix weak factors, keep strong ones"]
  REDUCE --> NEXT["Smaller, focused search"]
```

**Next:** replacing the expensive solver with a cheap surrogate.
""",
        ),
        _t(
            "Surrogate models for fast evaluation",
            "13 min",
            r"""
# Surrogate models for fast evaluation

Each generative or FEA evaluation is expensive — seconds to hours. A
**surrogate** (metamodel) learns the mapping $\mathbf{x}\mapsto y$ from a modest
DOE sample, then predicts new points in microseconds, so you can explore and
optimize almost for free.

The simplest is a **polynomial response surface**, e.g. a quadratic

$$\hat{y}(\mathbf{x}) = \beta_0 + \sum_i \beta_i x_i + \sum_{i\le j}\beta_{ij} x_i x_j.$$

More capable is **Kriging / Gaussian-process regression**, which interpolates the
data *and* returns a predictive variance — an uncertainty that tells you where the
model is least trustworthy. Surrogate error falls as you add training points,
roughly as $1/\sqrt{n}$:

```plot
{"title": "Surrogate prediction error vs training samples", "xLabel": "training samples n", "yLabel": "RMSE (relative)", "xRange": [4, 60], "yRange": [0, 1], "grid": true, "functions": [{"expr": "2/sqrt(x)", "label": "RMSE ~ 1/sqrt(n)", "color": "#16a34a"}]}
```

```python
import numpy as np

# Quadratic response surface fit by least squares, then its minimizer
x = np.array([2.0, 3.0, 4.0, 5.0, 6.0])          # wall thickness (mm)
y = np.array([8.2, 5.1, 4.0, 4.4, 6.1])          # mass*compliance proxy

A = np.column_stack([np.ones_like(x), x, x**2])  # [1, x, x^2]
beta, *_ = np.linalg.lstsq(A, y, rcond=None)
x_opt = -beta[1] / (2 * beta[2])                 # vertex of the parabola
print(beta.round(3), "optimum at x =", round(x_opt, 2))
```

The workflow: sample with DOE, fit the surrogate, optimize on it (instant), then
**verify** the predicted optimum with one true solver run. **Adaptive sampling**
adds new points where the Gaussian-process variance — or the *expected
improvement* — is largest, refining the model only where it matters.

```mermaid
flowchart LR
  DOE["DOE samples"] --> FIT["Fit surrogate - RSM / Kriging"]
  FIT --> OPT["Optimize on surrogate (instant)"]
  OPT --> VERIFY["Verify with true solver"]
  VERIFY -->|"add point where uncertain"| FIT
  VERIFY -->|"converged"| OUT["Best design"]
```

**Next:** optimizing several conflicting objectives at once.
""",
        ),
        _t(
            "Multi-objective optimization and the Pareto front",
            "13 min",
            r"""
# Multi-objective optimization and the Pareto front

Real designs juggle conflicting goals — light *and* stiff *and* cheap. With more
than one objective there is rarely a single best design; instead there is a set of
**non-dominated** designs. A design $\mathbf{a}$ **dominates** $\mathbf{b}$ if it
is at least as good on every objective and strictly better on one. The
non-dominated set is the **Pareto front**.

$$\mathbf{a} \prec \mathbf{b} \iff f_i(\mathbf{a}) \le f_i(\mathbf{b})\;\forall i
\;\;\text{and}\;\; \exists j: f_j(\mathbf{a}) < f_j(\mathbf{b}).$$

Plotting two objectives reveals the trade-off: along the front, improving one
objective necessarily worsens another.

```plot
{"title": "Pareto front: mass vs compliance", "xLabel": "mass (kg)", "yLabel": "compliance (lower = stiffer)", "xRange": [1, 6], "yRange": [0, 3], "grid": true, "functions": [{"expr": "2.4/x", "label": "Pareto front", "color": "#16a34a"}]}
```

Algorithms such as **NSGA-II** evolve a population toward the whole front in one
run. The core operation is identifying the non-dominated set:

```python
import numpy as np

def pareto_front(F):
    # Indices of non-dominated rows (minimize every column of F)
    n = len(F)
    keep = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i != j and np.all(F[j] <= F[i]) and np.any(F[j] < F[i]):
                keep[i] = False                  # i is dominated by j
                break
    return np.where(keep)[0]

# columns: [mass, compliance]
F = np.array([[2.0, 2.4],[3.0, 1.5],[2.5, 2.0],[4.0, 1.2],[3.5, 1.8]])
print(pareto_front(F))      # non-dominated candidate indices
```

```mermaid
flowchart LR
  POP["Population of designs"] --> EVAL["Evaluate all objectives"]
  EVAL --> RANK["Non-dominated sorting (NSGA-II)"]
  RANK --> DIV["Crowding distance - keep spread"]
  DIV --> GEN["Selection + crossover + mutation"]
  GEN -->|"next generation"| EVAL
  RANK --> FRONT["Pareto front of trade-offs"]
```

The engineer then picks a point on the front using preferences (weights, a
budget cap) — the algorithm provides options, not a verdict.

**Next:** keeping every candidate inside its constraints.
""",
        ),
        _t(
            "Constraint handling in design search",
            "12 min",
            r"""
# Constraint handling in design search

Optimizers minimize objectives; constraints (stress limits, displacement caps,
volume budgets, manufacturing rules) must be *enforced*. Three common strategies:

- **Penalty method** — add a cost for violation, turning a constrained problem
  into an unconstrained one:
  $$\tilde{f}(\mathbf{x}) = f(\mathbf{x}) + \mu\sum_j \max(0, g_j(\mathbf{x}))^2.$$
  Simple, but the penalty weight $\mu$ must be tuned: too small ignores the
  constraint, too large distorts the search.
- **Lagrangian / KKT** — introduce multipliers and solve the stationarity
  conditions; the basis of gradient methods like SQP.
- **Feasibility rules** — in population methods (NSGA-II), prefer feasible over
  infeasible designs and rank infeasible ones by total violation.

As the penalty weight rises, constraint violation in the optimum shrinks toward
zero, at the cost of a stiffer, harder optimization landscape:

```plot
{"title": "Constraint violation at the optimum vs penalty weight", "xLabel": "penalty weight mu (relative)", "yLabel": "remaining violation", "xRange": [0, 10], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "violation -> 0 as mu grows", "color": "#2563eb"}]}
```

```python
import numpy as np
from scipy.optimize import minimize

# Minimize mass with a stress constraint via a quadratic penalty
def mass(x):    return 0.8*x[0] + 0.3*x[1]          # thickness, rib height
def stress(x):  return 200.0 / (x[0]*x[1])          # solver proxy (MPa)

def penalized(x, mu=50.0):
    g = max(0.0, stress(x) - 120.0)                 # violation of stress <= 120
    return mass(x) + mu * g**2

res = minimize(penalized, x0=[4.0, 10.0], method="Nelder-Mead")
print(res.x.round(2), "mass", round(mass(res.x), 2), "stress", round(stress(res.x), 1))
```

```mermaid
flowchart LR
  PROB["min f(x) s.t. g(x) <= 0"] --> METH{"Method"}
  METH -->|"penalty"| PEN["f + mu * violation^2"]
  METH -->|"Lagrangian"| LAG["multipliers + KKT"]
  METH -->|"population"| FEAS["feasibility-first ranking"]
  PEN --> SOLVE["Optimize"]
  LAG --> SOLVE
  FEAS --> SOLVE
  SOLVE --> XSTAR["Feasible optimum x*"]
```

**Next:** check your understanding of design-space exploration methods.
""",
        ),
        _quiz(),
    ),
)


# ── Generative Design & AI for CAD — Advanced ────────────────────────────────

_ADVANCED = SeedCourse(
    slug="generative-design-advanced",
    title="Generative Design & AI for CAD — Advanced",
    description=(
        "State-of-the-art AI for CAD. Covers deep generative models (VAEs, GANs, "
        "diffusion) over geometry, neural surrogates and physics-informed networks, "
        "Bayesian optimization for expensive design loops, deep reinforcement "
        "learning for sequential CAD construction, large-language/multimodal models "
        "as CAD copilots, and automated evaluation and selection of candidates. "
        "Worked code in Python and MATLAB."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Deep generative models of geometry",
            "13 min",
            r"""
# Deep generative models of geometry

Classical generative design *optimizes* geometry; **deep generative models**
*learn a distribution* over geometry and sample new shapes from it. Trained on a
corpus of designs, a model maps a low-dimensional **latent vector** $\mathbf{z}$
to a full shape, so navigating $\mathbf{z}$ explores a smooth space of plausible
parts.

Three families dominate:

- **Variational autoencoders (VAEs)** — encode a shape to a latent $\mathbf{z}$
  and decode it back, maximizing the evidence lower bound
  $$\mathcal{L} = \mathbb{E}_{q(z|x)}[\log p(x|z)] - D_{\mathrm{KL}}(q(z|x)\,\|\,p(z)).$$
- **Generative adversarial networks (GANs)** — a generator vs a discriminator,
  producing sharp shapes but trickier to train.
- **Diffusion models** — learn to denoise; current state of the art for fidelity
  and diversity, the basis of text-to-3D.

Representations vary: voxels, point clouds, signed distance fields (SDF), meshes,
or B-rep command sequences. As the latent dimension grows, reconstruction error
falls but the space gets harder to search — a capacity/usability trade-off:

```plot
{"title": "Reconstruction error vs latent dimension", "xLabel": "latent dimension", "yLabel": "reconstruction error (relative)", "xRange": [2, 64], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1.5/sqrt(x)", "label": "error decreases with capacity", "color": "#16a34a"}]}
```

```python
import numpy as np

# Interpolate in latent space between two designs (linear walk)
rng = np.random.default_rng(0)
z_a = rng.standard_normal(8)        # latent code of design A
z_b = rng.standard_normal(8)        # latent code of design B

def lerp(a, b, t):
    return (1 - t) * a + t * b       # decode(lerp) yields a smooth morph A->B

for t in [0.0, 0.5, 1.0]:
    z = lerp(z_a, z_b, t)
    print("t =", t, "||z|| =", round(np.linalg.norm(z), 3))
```

```mermaid
flowchart LR
  DATA["Corpus of designs"] --> ENC["Encoder"]
  ENC --> Z["Latent space z"]
  Z --> DEC["Decoder / generator"]
  DEC --> SHAPE["New geometry"]
  COND["Condition - text, constraints"] -.->|"steer"| DEC
```

**Next:** neural networks that replace the physics solver.
""",
        ),
        _t(
            "Neural surrogates and physics-informed networks",
            "13 min",
            r"""
# Neural surrogates and physics-informed networks

A **neural surrogate** is a network $\hat{f}_\theta(\mathbf{x})$ trained to
predict simulation outputs (stress field, drag, frequency) directly from a design,
replacing the FEA/CFD solver inside the loop. Once trained, inference is
milliseconds, turning a day-long sweep into seconds. **Convolutional** and
**graph** networks predict full fields on grids/meshes; **operator learning**
(Fourier Neural Operators, DeepONet) learns the solution *operator* itself and
generalizes across resolutions.

The catch: a purely data-driven net can violate physics off-distribution.
**Physics-informed neural networks (PINNs)** add the governing PDE residual to the
loss, so predictions obey the physics even with little data:

$$\mathcal{L} = \underbrace{\frac{1}{N}\sum \lVert \hat{u} - u\rVert^2}_{\text{data}}
+ \lambda \underbrace{\frac{1}{M}\sum \lVert \mathcal{N}[\hat{u}]\rVert^2}_{\text{PDE residual}}.$$

The physics term cuts the data needed to reach a target accuracy:

```plot
{"title": "Training data needed vs accuracy: data-only vs physics-informed", "xLabel": "target accuracy (0-10)", "yLabel": "training samples needed (relative)", "xRange": [1, 10], "yRange": [0, 12], "grid": true, "functions": [{"expr": "1.1*x", "label": "data-only", "color": "#dc2626"}, {"expr": "0.4*x", "label": "physics-informed (PINN)", "color": "#16a34a"}]}
```

```python
import numpy as np

# Toy PINN-style loss: data term + PDE-residual term for u'' = f
def pde_residual(u_pred, x, h=1e-3):
    upp = (u_pred(x + h) - 2*u_pred(x) + u_pred(x - h)) / h**2   # finite-diff u''
    return upp - f_source(x)

def f_source(x):   return -np.pi**2 * np.sin(np.pi * x)         # so u = sin(pi x)
u_pred = lambda x: np.sin(np.pi * x)                            # a candidate field

xs = np.linspace(0.1, 0.9, 9)
data_loss = np.mean((u_pred(xs) - np.sin(np.pi*xs))**2)
phys_loss = np.mean(pde_residual(u_pred, xs)**2)
lam = 1.0
print("total loss =", round(data_loss + lam*phys_loss, 6))
```

```mermaid
flowchart LR
  DESIGN["Design x"] --> NET["Neural surrogate f_theta"]
  NET --> FIELD["Predicted stress / flow field"]
  PDE["Governing PDE residual"] -.->|"adds to loss"| NET
  FIELD --> LOOP["Fast inner loop of optimizer"]
```

**Next:** spending a tiny evaluation budget wisely with Bayesian optimization.
""",
        ),
        _t(
            "Bayesian optimization for expensive designs",
            "13 min",
            r"""
# Bayesian optimization for expensive designs

When each design evaluation is very expensive (a coupled CFD-FEA solve, a
prototype test), you cannot afford hundreds of trials. **Bayesian optimization
(BO)** is built for this: it maintains a probabilistic surrogate — usually a
**Gaussian process** — over the objective and chooses each next point to balance
*exploiting* good regions against *exploring* uncertain ones.

The chooser is an **acquisition function**. **Expected Improvement (EI)** over the
current best $f^*$ is

$$\mathrm{EI}(\mathbf{x}) = (f^* - \mu(\mathbf{x}))\,\Phi(z) + \sigma(\mathbf{x})\,\phi(z),
\qquad z = \frac{f^* - \mu(\mathbf{x})}{\sigma(\mathbf{x})},$$

with $\mu,\sigma$ the GP mean and standard deviation. BO typically reaches a good
optimum in far fewer evaluations than random or grid search:

```plot
{"title": "Best objective found vs evaluations: Bayesian vs random search", "xLabel": "evaluations", "yLabel": "objective gap to optimum", "xRange": [0, 20], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.35*x)", "label": "Bayesian optimization", "color": "#16a34a"}, {"expr": "exp(-0.1*x)", "label": "random search", "color": "#dc2626"}]}
```

```python
import numpy as np
from scipy.stats import norm

def expected_improvement(mu, sigma, f_best, xi=0.01):
    # EI acquisition; pick the candidate that maximizes it
    sigma = np.maximum(sigma, 1e-9)
    z = (f_best - mu - xi) / sigma
    return (f_best - mu - xi) * norm.cdf(z) + sigma * norm.pdf(z)

# GP posterior at three candidate designs (mean, std); we minimize, best so far = 4.0
mu    = np.array([4.5, 3.8, 4.1])
sigma = np.array([0.2, 0.9, 0.5])
ei = expected_improvement(mu, sigma, f_best=4.0)
print("EI:", ei.round(4), "-> evaluate candidate", int(np.argmax(ei)))
```

```mermaid
flowchart LR
  DATA["Evaluated designs"] --> GP["Fit Gaussian process"]
  GP --> ACQ["Acquisition - Expected Improvement"]
  ACQ --> NEXT["Pick next design (explore vs exploit)"]
  NEXT --> EVAL["Expensive evaluation - CFD/FEA/test"]
  EVAL -->|"add to data"| GP
  GP --> BEST["Optimum within budget"]
```

**Next:** treating CAD construction as a sequential decision problem.
""",
        ),
        _t(
            "Reinforcement learning for sequential CAD",
            "13 min",
            r"""
# Reinforcement learning for sequential CAD

A CAD model is built as a *sequence* of operations — sketch, extrude, fillet,
pattern. This makes design a **sequential decision problem**, and **reinforcement
learning (RL)** a natural fit. An **agent** observes the current geometry (state
$s_t$), picks an operation (action $a_t$), and receives a **reward** $r_t$ tied to
performance (stiffness gained per gram added, constraint satisfaction).

The agent learns a **policy** $\pi_\theta(a\mid s)$ maximizing expected discounted
return

$$J(\theta) = \mathbb{E}_{\pi_\theta}\!\left[\sum_{t=0}^{T}\gamma^{t} r_t\right],
\qquad 0 < \gamma < 1.$$

RL has driven generative CAD command sequences, layout and packing, and process
planning. With training (episodes), average return climbs toward the achievable
optimum:

```plot
{"title": "Average episode return vs training episodes", "xLabel": "training episodes (thousands)", "yLabel": "return (relative, higher better)", "xRange": [0, 30], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1 - exp(-0.15*x)", "label": "learning curve", "color": "#16a34a"}]}
```

```python
import numpy as np

# One REINFORCE policy-gradient step over a CAD-operation episode
def discounted_returns(rewards, gamma=0.95):
    g, out = 0.0, []
    for r in reversed(rewards):              # accumulate backward
        g = r + gamma * g
        out.append(g)
    return np.array(out[::-1])

rewards = [0.0, 0.2, 0.0, 0.5, 1.0]         # reward per CAD action in the episode
G = discounted_returns(rewards)
G = (G - G.mean()) / (G.std() + 1e-8)        # baseline-subtracted advantage
print("normalized returns:", G.round(3))     # weights the log-prob gradient
```

```mermaid
flowchart LR
  STATE["State - current geometry"] --> POLICY["Policy pi_theta(a|s)"]
  POLICY --> ACT["CAD action - extrude / fillet / ..."]
  ACT --> ENV["Apply + simulate"]
  ENV --> REW["Reward - performance gain"]
  REW -->|"policy gradient update"| POLICY
  ENV --> STATE
```

**Next:** language and multimodal models as CAD copilots.
""",
        ),
        _t(
            "LLM and multimodal copilots for CAD",
            "12 min",
            r"""
# LLM and multimodal copilots for CAD

The newest layer turns natural language into design. **Large language models
(LLMs)** and **multimodal models** translate a prompt — "a lightweight bracket
that bolts to this plate and carries 500 N downward" — into a parametric script,
a feature recipe, or constraints fed to a generative engine. The model acts as a
**copilot**: the engineer states intent in words and sketches; the model emits
CAD operations.

Practical patterns:

- **Code generation** — the LLM writes CAD-API / scripting code (Onshape
  FeatureScript, CadQuery, pythonOCC) that builds the model deterministically.
- **Tool use / function calling** — the model calls solver and CAD functions and
  reasons over returned metrics.
- **Multimodal input** — sketches, reference images and drawings condition the
  output (text-and-image to geometry).
- **Retrieval-augmented** — ground generation in a company's standards and parts
  library to keep designs valid.

Code-generation from intent is the most reliable today because the geometry is
produced by deterministic CAD kernels, not the model's pixels:

```python
# An LLM emits CadQuery-style code from "bracket: 80x40, two M6 holes, 8 mm thick"
import cadquery as cq   # illustrative; runs in a CAD-scripting environment

def bracket(length=80, width=40, thick=8, hole_d=6.6, pitch=50):
    return (cq.Workplane("XY")
            .box(length, width, thick)
            .faces(">Z").workplane()
            .pushPoints([(-pitch/2, 0), (pitch/2, 0)])
            .hole(hole_d))                       # parametric, regenerates on edit

model = bracket()                                # deterministic geometry from intent
```

Capability is rising fast, but so is the need for verification — generated designs
must still pass FEA and the manufacturing rules.

```mermaid
flowchart LR
  NL["Natural-language intent + sketch"] --> LLM["LLM / multimodal copilot"]
  LLM --> CODE["CAD-API code / constraints"]
  RAG["Standards + parts library"] -.->|"retrieval-augmented"| LLM
  CODE --> KERNEL["Deterministic CAD kernel"]
  KERNEL --> GEOM["Parametric geometry"]
  GEOM --> CHECK["FEA + manufacturing verification"]
```

**Next:** automatically evaluating and selecting the best candidates.
""",
        ),
        _t(
            "Automated evaluation and candidate selection",
            "13 min",
            r"""
# Automated evaluation and candidate selection

A modern pipeline can emit dozens of candidates per hour; the bottleneck moves to
**evaluation and selection**. The goal is to score every candidate consistently,
discard the infeasible, and rank the rest by the project's true priorities — with
the human deciding from a short, defensible list rather than a flood.

A robust selection scheme: (1) **screen** on hard constraints (safety factor,
keep-out, manufacturability); (2) compute the **Pareto front** of the survivors;
(3) score front members with a **weighted/normalized** preference or a
**TOPSIS**-style distance to the ideal point. Normalizing each metric to $[0,1]$
keeps incomparable units (kg, MPa, $) on equal footing:

$$\tilde{m}_i = \frac{m_i - m_{\min}}{m_{\max} - m_{\min}}, \qquad
\text{score} = \sum_i w_i\,\tilde{m}_i,\;\; \sum_i w_i = 1.$$

As the candidate pool grows, the *quality* of the best feasible design keeps
improving but with diminishing returns — so a sensible pipeline caps generation
when the front stops advancing:

```plot
{"title": "Best feasible design quality vs candidates evaluated", "xLabel": "candidates evaluated", "yLabel": "best feasible quality (relative)", "xRange": [0, 60], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1 - exp(-0.08*x)", "label": "diminishing returns", "color": "#16a34a"}]}
```

```python
import numpy as np

def select(candidates, weights, sf_min=1.5):
    # Screen on safety factor, then rank survivors by normalized weighted score
    feasible = [c for c in candidates if c["sf"] >= sf_min]
    if not feasible:
        return None
    M = np.array([[c["mass"], c["compliance"], c["cost"]] for c in feasible], float)
    # minimize each metric -> normalize then invert so higher score = better
    norm = (M - M.min(0)) / (M.ptp(0) + 1e-12)
    score = 1.0 - norm @ np.array(weights)
    best = feasible[int(np.argmax(score))]
    return best["name"], round(float(score.max()), 3)

cands = [
    {"name": "A", "mass": 2.1, "compliance": 2.0, "cost": 30, "sf": 1.8},
    {"name": "B", "mass": 3.4, "compliance": 1.2, "cost": 22, "sf": 2.1},
    {"name": "C", "mass": 2.7, "compliance": 1.6, "cost": 41, "sf": 1.3},
]
print(select(cands, weights=[0.5, 0.3, 0.2]))   # screens C out, ranks A vs B
```

```mermaid
flowchart LR
  POOL["Candidate pool + metrics"] --> SCREEN["Screen - hard constraints"]
  SCREEN --> PF["Pareto front of survivors"]
  PF --> SCORE["Normalize + weighted score / TOPSIS"]
  SCORE --> SHORT["Short list for the engineer"]
  SHORT --> DECIDE["Human decision + final validation"]
```

The pipeline automates the grind — simulate, screen, rank — and reserves judgment
for the human, who chooses among a few well-characterized, validated designs.

**Next:** check your understanding of AI-driven generative design.
""",
        ),
        _quiz(),
    ),
)


GENERATIVE_DESIGN_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["GENERATIVE_DESIGN_COURSES"]
