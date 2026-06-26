"""Capstone: AI-Optimised Organic Part track: Basics -> Intermediate -> Advanced.

An end-to-end mechanical-engineering capstone that takes a bracket from a brief to
a printed part: framing requirements and load cases, topology optimization and
generative refinement, then FEA validation, design for additive manufacturing and
final print. Lessons are `text` with LaTeX, interactive ```plot blocks (stiffness,
compliance, convergence, S-N curves), ```mermaid workflow/decision diagrams and
runnable ```python/```matlab snippets for SIMP topology optimization, FEA checks
and DfAM computations.
"""

# ruff: noqa: RUF001
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Capstone: AI-Optimised Organic Part — Basics ─────────────────────────────

_BASICS = SeedCourse(
    slug="capstone-generative-mechanical-design-basics",
    title="Capstone: AI-Optimised Organic Part — Basics",
    description=(
        "The intuition behind AI-driven mechanical design. Frame a real part "
        "from a brief: write requirements, define load cases and a design "
        "space, and understand why topology optimization produces those "
        "skeletal, bone-like shapes. Covers stiffness vs strength, factor of "
        "safety, and where additive manufacturing fits. Interactive plots and "
        "workflow diagrams throughout, no heavy math required."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is generative mechanical design?",
            "10 min",
            r"""
# What is generative mechanical design?

**Generative design** lets the computer propose part geometry from goals and
constraints rather than from a designer sketching features. You specify *where
loads enter*, *where the part is bolted down*, *what space it may occupy*, and
*what to minimise* (usually mass). An optimizer then carves material away from
the regions that carry little load, leaving an efficient, often organic shape.

The umbrella covers two related ideas. **Topology optimization** decides the best
material layout inside a fixed design space. **Generative design** (as marketed by
Fusion 360, nTop, Ansys) wraps that with multiple load cases, manufacturing
constraints and an outcome explorer that returns several candidates.

```mermaid
flowchart LR
  BRIEF["Design brief"] --> REQ["Requirements + load cases"]
  REQ --> SPACE["Design space + keep-out zones"]
  SPACE --> OPT["Topology / generative optimizer"]
  OPT --> CAND["Candidate geometries"]
  CAND --> FEA["FEA validation"]
  FEA --> DFAM["Design for additive manufacturing"]
  DFAM --> PRINT["Printed part"]
```

The payoff is **specific stiffness** — stiffness per unit mass. An optimized
bracket can match the original's deflection at a fraction of the weight, because
material sits only where the load path needs it.

**Next:** turning a vague brief into precise requirements.
""",
        ),
        _t(
            "From brief to requirements and load cases",
            "11 min",
            r"""
# From brief to requirements and load cases

A brief such as *"a lighter engine-mount bracket"* is not yet solvable. You must
translate it into **measurable requirements** and a set of **load cases** the
optimizer and FEA can act on. Good requirements are verifiable: a number, a unit
and a direction (minimise / must-not-exceed).

| Requirement | Example value |
|---|---|
| Max mass | $\le 180$ g |
| Max deflection at load point | $\le 0.5$ mm |
| Factor of safety on yield | $\ge 2.0$ |
| Bolt pattern (keep-out) | 4 × M6, fixed |
| Build envelope | $120 \times 80 \times 60$ mm |

A **load case** is a specific combination of forces, moments and supports the
part must survive: e.g. *1.5 kN downward at the boss + clamped bolt holes*. Real
parts have several (static, braking, vibration), and the optimizer must satisfy
all of them at once.

```mermaid
flowchart TB
  B["Brief: lighter bracket"] --> F["Functional: carry 1.5 kN"]
  B --> P["Performance: < 0.5 mm deflection"]
  B --> C["Constraints: bolts, envelope, material"]
  F --> LC["Load cases"]
  P --> LC
  C --> LC
```

The load magnitude scales the required cross-section. For a simple tensile member
the stress is $\sigma = F/A$, so doubling the force doubles the area you need at
constant stress — a first sanity check on whether the brief is even feasible.

**Next:** stiffness versus strength — two requirements that pull differently.
""",
        ),
        _t(
            "Stiffness, strength and factor of safety",
            "11 min",
            r"""
# Stiffness, strength and factor of safety

Two properties dominate a structural brief and beginners often conflate them.
**Stiffness** resists *deformation*: a stiff part barely deflects under load.
**Strength** resists *failure*: a strong part does not yield or fracture. A part
can be strong but flexible (a fishing rod) or stiff but brittle (cast iron).

For a linear-elastic material, stress and strain are tied by **Hooke's law**
$\sigma = E\varepsilon$, where $E$ is Young's modulus. The material behaves
elastically up to the **yield stress** $\sigma_y$; beyond it, deformation is
permanent.

```plot
{"title": "Stress-strain: elastic region then yield", "xLabel": "strain (millistrain)", "yLabel": "stress (MPa)", "xRange": [0, 4], "yRange": [0, 320], "grid": true, "functions": [{"expr": "70*x", "label": "elastic: sigma = E*eps", "color": "#2563eb"}, {"expr": "250", "label": "yield stress sigma_y", "color": "#dc2626"}]}
```

The **factor of safety** (FoS) is the margin between what the material can take
and what the load demands:

$$\text{FoS} = \frac{\sigma_y}{\sigma_{\max}}$$

A FoS of 2 means the part sees half its yield stress at the worst load case.
Optimizers minimise mass *subject to* a stress (strength) constraint and often a
**compliance** (stiffness) objective — so both ideas appear in one problem.

**Next:** the design space, keep-out zones and boundary conditions.
""",
        ),
        _t(
            "Design space, keep-out zones and boundary conditions",
            "10 min",
            r"""
# Design space, keep-out zones and boundary conditions

The optimizer can only place material where you let it. You define three regions:

- **Design space** — the volume the optimizer may fill or empty.
- **Preserve / keep-in regions** — geometry that must stay (bolt bosses, bearing
  seats, mating faces). These are *frozen*.
- **Keep-out / obstacle regions** — volumes that must stay empty (clearance for a
  shaft, a neighbouring part, a tool path).

**Boundary conditions** anchor the physics: where the part is **fixed**
(supports) and where **loads** are applied. Get these wrong and the optimizer
solves the wrong problem perfectly.

```mermaid
flowchart LR
  DS["Design space (fillable)"] --> OPT["Optimizer"]
  KI["Keep-in: bosses, seats"] --> OPT
  KO["Keep-out: clearances"] --> OPT
  BC["Boundary conditions: fixed + loads"] --> OPT
  OPT --> SHAPE["Material only on load paths"]
```

A larger design space gives the optimizer more freedom and usually a lighter
result, but it must respect the build envelope and keep-outs. A common beginner
error is too small a design space, which forces material into inefficient layouts.

The fixed supports define the **load path** — the chain of material connecting
loads to ground. Topology optimization is, intuitively, the search for the
lightest load path that meets every requirement.

**Next:** why optimized parts look organic.
""",
        ),
        _t(
            "Why optimized parts look organic",
            "10 min",
            r"""
# Why optimized parts look organic

The skeletal, bone-like shapes optimizers produce are not a style choice — they
fall out of the physics. Material is expensive (it adds mass), so the optimizer
keeps it only along **principal stress paths**, the directions in which load
actually flows. The result resembles trabecular bone or a tree branch because
nature solves the same minimise-mass-at-required-stiffness problem.

A classic illustration is the **Michell truss**: the theoretically lightest
structure to carry a load to a support is a fan of curved members following
principal stress trajectories — almost exactly what topology optimization
rediscovers numerically.

```plot
{"title": "Specific stiffness rises as material moves to load paths", "xLabel": "optimization iteration", "yLabel": "stiffness per unit mass (norm.)", "xRange": [0, 30], "yRange": [0, 1.2], "grid": true, "functions": [{"expr": "1-exp(-0.4*x)", "label": "specific stiffness", "color": "#16a34a"}]}
```

Two practical consequences:

- **Hollow and branched** geometry is hard to machine but natural for **additive
  manufacturing**, which is why the two technologies pair so well.
- The shapes have **smooth, curved fillets** that lower stress concentrations,
  improving fatigue life compared with the sharp corners of a blocky bracket.

So "organic" is really "efficient": every strut earns its mass by carrying load.

**Next:** the full capstone arc you will execute.
""",
        ),
        _t(
            "The capstone arc: brief to printed part",
            "9 min",
            r"""
# The capstone arc: brief to printed part

This track follows one part — a lightweight bracket — through the complete
modern design loop. Each stage feeds the next, and you iterate when validation
fails.

```mermaid
flowchart TB
  S1["1. Frame: requirements + load cases"] --> S2["2. Topology optimization"]
  S2 --> S3["3. Generative refinement + smoothing"]
  S3 --> S4["4. FEA validation"]
  S4 -->|fail| S2
  S4 -->|pass| S5["5. Design for additive manufacturing"]
  S5 --> S6["6. Print + post-process"]
  S6 --> S7["7. Verify against requirements"]
```

The **Basics** course (this one) builds intuition. **Intermediate** adds the
quantitative core: the SIMP method, compliance minimisation, mesh convergence and
the FEA you use to check a candidate. **Advanced** reaches the state of the art:
multi-load-case and stress-constrained optimization, AI surrogate models and
generative neural methods, lattice infill and a printable, verified part.

A key mindset: optimization gives a **candidate**, not a finished part. FEA
validation and manufacturability constraints almost always send you back to
adjust the problem statement — tightening a keep-out, adding a load case, or
relaxing a mass target. That loop is the real engineering.

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Capstone: AI-Optimised Organic Part — Intermediate ───────────────────────

_INTERMEDIATE = SeedCourse(
    slug="capstone-generative-mechanical-design-intermediate",
    title="Capstone: AI-Optimised Organic Part — Intermediate",
    description=(
        "The quantitative core of topology optimization and FEA. Derive the "
        "compliance-minimisation problem, the SIMP material model and the "
        "optimality-criteria update; control checkerboarding with filters; and "
        "validate a candidate with linear static FEA, mesh convergence and the "
        "von Mises stress criterion. Includes runnable Python/MATLAB for a 2D "
        "SIMP solver and FEA checks."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The compliance minimisation problem",
            "12 min",
            r"""
# The compliance minimisation problem

Topology optimization for stiffness is posed as **minimum compliance**.
Compliance $c$ is the work done by the external loads — the inverse of global
stiffness — so minimising it maximises stiffness. With a finite-element
discretisation, the design variables are element densities
$x_e \in [0, 1]$ (0 = void, 1 = solid):

$$\min_{x}\; c(x) = U^\top K(x)\, U \quad \text{s.t.}\quad K(x)\,U = F,\;\; \frac{V(x)}{V_0} \le f,\;\; 0 < x_{\min} \le x_e \le 1$$

Here $K$ is the global stiffness matrix, $U$ the displacement vector, $F$ the
load, and $f$ the **volume fraction** (e.g. keep 30% of the box). The constraint
$KU = F$ is just static equilibrium solved by FEA at every iteration.

```mermaid
flowchart LR
  X["Densities x_e"] --> K["Assemble K(x)"]
  K --> SOLVE["Solve K*U = F (FEA)"]
  SOLVE --> C["Compliance c = U^T K U"]
  C --> SENS["Sensitivities dc/dx_e"]
  SENS --> UPD["Update densities"]
  UPD --> X
```

The compliance objective is **self-adjoint**, which makes the sensitivity cheap
to compute (next lesson). Lower compliance is plotted against iteration below — a
typical monotone-ish descent toward a converged layout.

```plot
{"title": "Compliance descent during optimization", "xLabel": "iteration", "yLabel": "compliance (norm.)", "xRange": [0, 40], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "0.1+0.9*exp(-0.25*x)", "label": "c(x) decreasing", "color": "#2563eb"}]}
```

**Next:** SIMP — how a 0/1 problem becomes differentiable.
""",
        ),
        _t(
            "SIMP: penalising intermediate densities",
            "12 min",
            r"""
# SIMP: penalising intermediate densities

A true topology problem is discrete (material or void), which is hard to
optimize. **SIMP** (Solid Isotropic Material with Penalisation) relaxes it: each
element's stiffness scales with its density raised to a power $p$:

$$E_e(x_e) = E_{\min} + x_e^{\,p}\,(E_0 - E_{\min}),\qquad p \ge 3$$

With $p = 1$ the stiffness is linear in density and grey (intermediate) material
is "cheap", so the optimizer happily fills with $x_e \approx 0.5$. Penalising with
$p \ge 3$ makes intermediate densities **stiffness-inefficient**: half-dense
material costs half the volume but yields only $0.5^3 = 0.125$ of the stiffness,
so the optimizer is pushed toward crisp 0/1 designs.

```plot
{"title": "SIMP stiffness vs density for several penalties", "xLabel": "density x_e", "yLabel": "relative stiffness E_e/E_0", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "p = 1 (no penalty)", "color": "#16a34a"}, {"expr": "x^3", "label": "p = 3", "color": "#2563eb"}, {"expr": "x^5", "label": "p = 5", "color": "#dc2626"}]}
```

The element sensitivity of compliance follows directly from the SIMP law and the
self-adjoint property:

$$\frac{\partial c}{\partial x_e} = -p\,x_e^{\,p-1}(E_0 - E_{\min})\,u_e^\top k_0\, u_e$$

where $u_e$ are the element displacements and $k_0$ the unit-stiffness element
matrix. It is always $\le 0$: adding material reduces compliance.

```python
import numpy as np

def simp_stiffness(x, E0=70e3, Emin=1e-3, p=3.0):
    # SIMP interpolation: relative modulus per element density.
    return Emin + x**p * (E0 - Emin)

x = np.array([0.0, 0.5, 1.0])
print(simp_stiffness(x))  # void ~0, grey heavily penalised, solid ~E0
```

**Next:** the optimality-criteria update that moves densities.
""",
        ),
        _t(
            "Optimality criteria and density filtering",
            "13 min",
            r"""
# Optimality criteria and density filtering

Given sensitivities, how do we update densities? The classic, robust choice is the
**optimality-criteria (OC)** method, a fixed-point update derived from the KKT
conditions. Each element scales by its sensitivity-to-Lagrange-multiplier ratio,
clamped to a move limit $m$:

$$x_e^{\text{new}} = \max\!\Big(x_{\min},\; \max\!\big(x_e - m,\; \min(1,\; \min(x_e + m,\; x_e\, B_e^{\eta}))\big)\Big),\quad B_e = \frac{-\partial c/\partial x_e}{\lambda\,\partial V/\partial x_e}$$

The multiplier $\lambda$ is found by bisection so the volume constraint is met.

Raw SIMP suffers two numerical pathologies: **checkerboarding** (artificial
stiff chequer patterns) and **mesh dependence** (finer meshes give finer, thinner
members). The cure is a **filter** with radius $r_{\min}$ that smooths
sensitivities (or densities) over a neighbourhood, imposing a minimum feature
size:

```mermaid
flowchart LR
  S["Element sensitivities"] --> FILT["Filter radius r_min"]
  FILT --> OC["OC update + bisection on lambda"]
  OC --> CHK{"converged?"}
  CHK -->|no| S
  CHK -->|yes| OUT["Final layout"]
```

```python
import numpy as np

def oc_update(x, dc, volfrac, move=0.2):
    # One optimality-criteria step; bisection enforces volume fraction.
    l1, l2 = 1e-9, 1e9
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        xnew = np.clip(x * np.sqrt(-dc / lmid), x - move, x + move)
        xnew = np.clip(xnew, 1e-3, 1.0)
        l1, l2 = (lmid, l2) if xnew.mean() > volfrac else (l1, lmid)
    return xnew
```

This OC + filter loop is the heart of Sigmund's famous 99-line MATLAB code.

**Next:** validating a candidate with linear static FEA.
""",
        ),
        _t(
            "Linear static FEA for validation",
            "12 min",
            r"""
# Linear static FEA for validation

An optimized layout is only a *candidate*; you confirm it with a proper
**finite-element analysis**. Linear static FEA assembles the global system

$$K\,U = F$$

from element stiffness matrices, applies displacement boundary conditions, solves
for nodal displacements $U$, then recovers element strains and stresses. The
assumptions — linear elasticity, small deflections, no contact — must actually
hold for the result to be trustworthy.

```mermaid
flowchart TB
  GEO["Geometry + mesh"] --> KE["Element matrices k_e"]
  KE --> ASM["Assemble global K"]
  ASM --> BC["Apply loads F + supports"]
  BC --> SOLVE["Solve K*U = F"]
  SOLVE --> POST["Recover stress, strain, deflection"]
  POST --> CHK["Check vs requirements"]
```

A minimal 1D bar example shows the assembly and solve pattern that scales to 3D
solids:

```python
import numpy as np

# Two axial bar elements, node 0 fixed, force P at the free end.
E, A, L = 70e3, 50.0, 100.0      # MPa, mm^2, mm
k = E * A / L
K = np.array([[ k, -k,  0],
              [-k, 2*k, -k],
              [ 0, -k,  k]])
F = np.array([0.0, 0.0, 1000.0]) # N at the tip
free = [1, 2]                    # node 0 is fixed
U = np.zeros(3)
U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
print("tip deflection (mm):", U[2])
```

Compare the FEA tip deflection against the hand check $\delta = PL/(AE)$ per bar:
agreement validates your model before you trust a complex part.

**Next:** mesh convergence — making the numbers reliable.
""",
        ),
        _t(
            "Mesh convergence and discretisation error",
            "11 min",
            r"""
# Mesh convergence and discretisation error

FEA approximates a continuum with a finite mesh, so every result carries
**discretisation error**. Coarse meshes are too stiff and *under*-predict stress,
especially at fillets and holes where gradients are steep. A **mesh convergence
study** refines element size $h$ and watches a quantity of interest (peak von
Mises stress, max deflection) until it stops changing:

$$\text{error} \approx C\, h^{\,k}\;\longrightarrow\; 0 \text{ as } h \to 0$$

where $k$ depends on element order. You accept the mesh once successive
refinements change the result by less than a tolerance (e.g. 2–5%).

```plot
{"title": "Peak stress converges as mesh is refined", "xLabel": "elements per fillet (1/h)", "yLabel": "peak von Mises (MPa)", "xRange": [1, 12], "yRange": [120, 260], "grid": true, "functions": [{"expr": "240-130*exp(-0.5*x)", "label": "converging peak stress", "color": "#dc2626"}]}
```

Practical guidance:

- Use **quadratic** elements; they converge faster than linear at the same node
  count and avoid shear locking.
- Refine **locally** at stress raisers (fillets, the boss/web junction) rather
  than globally — cheaper for the same accuracy.
- Watch for **singularities** at sharp re-entrant corners, where stress never
  converges; round them or interpret with care.

```python
import numpy as np

stress = np.array([170, 205, 224, 233, 238, 240])  # peak vs refinement level
rel_change = np.abs(np.diff(stress)) / stress[1:]
print("converged when below tol:", rel_change)      # ~0.008 at the end -> stop
```

**Next:** the failure criterion that turns stress into a pass/fail.
""",
        ),
        _t(
            "Stress criteria and factor of safety in FEA",
            "11 min",
            r"""
# Stress criteria and factor of safety in FEA

FEA returns a full 3D stress tensor at every point, but a single scalar decides
whether ductile metal yields: the **von Mises (distortion-energy) stress**.

$$\sigma_v = \sqrt{\tfrac{1}{2}\big[(\sigma_1-\sigma_2)^2 + (\sigma_2-\sigma_3)^2 + (\sigma_3-\sigma_1)^2\big]}$$

Yielding is predicted when $\sigma_v \ge \sigma_y$, so the local **factor of
safety** is $\text{FoS} = \sigma_y / \sigma_v$. You scan the part for the minimum
FoS and require it to clear the brief (e.g. $\ge 2.0$) across every load case.

```mermaid
flowchart LR
  TEN["Stress tensor at each node"] --> VM["Von Mises sigma_v"]
  VM --> FOS["FoS = sigma_y / sigma_v"]
  FOS --> MIN["Find min FoS over all load cases"]
  MIN --> PASS{"min FoS >= target?"}
  PASS -->|no| REDESIGN["Add material / change problem"]
  PASS -->|yes| ACCEPT["Validated"]
```

```python
import numpy as np

def von_mises(s):  # s = (sxx, syy, szz, sxy, syz, szx) in MPa
    sxx, syy, szz, sxy, syz, szx = s
    return np.sqrt(0.5*((sxx-syy)**2 + (syy-szz)**2 + (szz-sxx)**2)
                   + 3*(sxy**2 + syz**2 + szx**2))

sy = 250.0  # yield stress, MPa
peak = von_mises((180, 60, 0, 40, 0, 0))
print("von Mises:", round(peak, 1), " FoS:", round(sy/peak, 2))
```

Stress concentrations multiply nominal stress by a factor $K_t$ at holes and
fillets; topology optimization's smooth fillets help keep $\sigma_v$ — and thus
FoS — within bounds.

**Next:** check the quantitative methods.
""",
        ),
        _quiz(),
    ),
)


# ── Capstone: AI-Optimised Organic Part — Advanced ───────────────────────────

_ADVANCED = SeedCourse(
    slug="capstone-generative-mechanical-design-advanced",
    title="Capstone: AI-Optimised Organic Part — Advanced",
    description=(
        "State-of-the-art and applied generative design. Handle multiple load "
        "cases and stress-constrained topology optimization; accelerate the loop "
        "with machine-learning surrogates and generative neural geometry; design "
        "conformal lattice infill; enforce additive-manufacturing constraints "
        "(overhangs, supports, anisotropy) in the optimizer; and verify the "
        "final printed part. Runnable Python for surrogates, lattices and DfAM "
        "checks."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Multi-load-case and stress-constrained optimization",
            "13 min",
            r"""
# Multi-load-case and stress-constrained optimization

Real brackets see several load cases — static, braking, vibration — and the part
must survive all of them. The standard trick is a **weighted compliance**
objective summing each case's compliance:

$$\min_x\; \sum_{i} w_i\, U_i^\top K(x)\, U_i,\qquad \sum_i w_i = 1$$

Each case needs its own FEA solve per iteration, so cost scales with the number of
cases. Weighting trades stiffness across scenarios.

Stiffness design alone can leave hidden stress hot-spots, so the frontier is
**stress-constrained** topology optimization. It is hard for three reasons:

- **Local nature** — a stress limit applies at every element, so there are
  thousands of constraints.
- **Singularity** — vanishing-density elements have ill-defined stress; an
  *epsilon-relaxation* of the stress measure is required.
- **Non-linearity** — stress is far more sensitive to density changes than
  compliance.

Constraint **aggregation** (a $p$-norm or KS function) collapses the many local
constraints into a few global ones for tractable gradients:

$$\sigma_{PN} = \Big(\sum_e \sigma_e^{\,P}\Big)^{1/P} \;\xrightarrow{P\to\infty}\; \max_e \sigma_e$$

```python
import numpy as np

def p_norm_stress(sigma, P=8):
    # Aggregate element von Mises stresses into a smooth max surrogate.
    sigma = np.asarray(sigma, float)
    return (np.sum(sigma**P))**(1.0/P)

s = [120, 180, 240, 90]
print("p-norm:", round(p_norm_stress(s), 1), " true max:", max(s))
```

Larger $P$ approximates the true max but stiffens the optimization; practitioners
ramp $P$ during the run.

**Next:** replacing slow FEA with ML surrogates.
""",
        ),
        _t(
            "Machine-learning surrogates for the design loop",
            "13 min",
            r"""
# Machine-learning surrogates for the design loop

Every optimization iteration and every generative variant needs an FEA solve,
which dominates wall-clock time. A **surrogate model** learns the map
*design parameters -> performance* (compliance, peak stress, mass) from a sampled
dataset, then predicts in milliseconds, enabling rapid exploration and
gradient-free search.

```mermaid
flowchart LR
  DOE["Design of experiments (LHS samples)"] --> SIM["High-fidelity FEA"]
  SIM --> DATA["(params, responses) dataset"]
  DATA --> FIT["Train surrogate (GP / NN)"]
  FIT --> SUR["Fast predictor"]
  SUR --> SEARCH["Optimize / explore cheaply"]
  SEARCH --> CHECK["Validate best on real FEA"]
  CHECK -->|refine| DOE
```

Two workhorses:

- **Gaussian-process (Kriging)** surrogates give a prediction *and* an
  uncertainty, which **Bayesian optimization** exploits via an acquisition
  function (expected improvement) to choose the next expensive FEA wisely.
- **Neural-network** surrogates scale to high-dimensional inputs (full geometry,
  fields) where GPs struggle.

```python
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

# Toy: predict bracket mass-penalty from two design knobs.
X = np.array([[0.2,0.3],[0.5,0.4],[0.8,0.6],[0.3,0.7],[0.6,0.2]])
y = np.array([1.8, 1.1, 0.7, 1.4, 1.0])             # measured compliance
gp = GaussianProcessRegressor(C(1.0)*RBF(0.3), normalize_y=True).fit(X, y)
mu, sd = gp.predict([[0.55, 0.45]], return_std=True)
print("predicted:", round(mu[0], 2), " +/-", round(sd[0], 2))
```

Surrogates must be **validated** (hold-out R^2, then confirm the chosen design on
real FEA); a confident-but-wrong surrogate is a classic failure mode.

The convergence to a good design accelerates sharply versus brute-force search:

```plot
{"title": "Surrogate-guided search converges faster", "xLabel": "expensive FEA evaluations", "yLabel": "best compliance found (norm.)", "xRange": [0, 25], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "0.2+0.8*exp(-0.4*x)", "label": "Bayesian / surrogate", "color": "#16a34a"}, {"expr": "0.2+0.8*exp(-0.1*x)", "label": "random search", "color": "#dc2626"}]}
```

**Next:** generative neural methods that propose geometry directly.
""",
        ),
        _t(
            "Generative neural methods for geometry",
            "12 min",
            r"""
# Generative neural methods for geometry

Beyond surrogates, deep-generative models now propose geometry itself. Trained on
libraries of optimized structures, they output candidate designs conditioned on
loads and constraints — often near-feasible in a single forward pass, then
polished by a few classical optimization steps.

```mermaid
flowchart LR
  COND["Conditions: loads, BCs, volfrac"] --> GEN["Generative model (GAN / diffusion / VAE)"]
  GEN --> CAND["Candidate density field"]
  CAND --> REFINE["Few SIMP steps to enforce physics"]
  REFINE --> FEA["FEA verify"]
```

Families in use:

- **cGANs / diffusion models** learn the distribution of optimal topologies and
  sample new ones; diffusion gives diverse, high-resolution fields.
- **Variational autoencoders** give a smooth latent space you can optimize *in*,
  turning shape search into low-dimensional continuous search.
- **Neural reparameterisation / implicit fields (DeepSIMP, neural SDFs)**
  represent the density as a network and optimize its weights with the FEA
  gradient — resolution-independent, smooth geometry.

The decisive caveat: generative output is a **prior**, never a guarantee. It can
violate equilibrium or a stress limit, so every candidate is re-checked by FEA
before acceptance. The value is speed and diversity, not correctness.

```python
import numpy as np

def latent_search(decode, objective, dim=8, steps=40, lr=0.1):
    # Optimize a design inside a VAE latent space via finite-diff gradients.
    z = np.zeros(dim)
    for _ in range(steps):
        g = np.zeros(dim)
        f0 = objective(decode(z))
        for i in range(dim):
            dz = np.zeros(dim); dz[i] = 1e-3
            g[i] = (objective(decode(z + dz)) - f0) / 1e-3
        z -= lr * g
    return decode(z)
```

**Next:** lattice infill for lightweight stiffness.
""",
        ),
        _t(
            "Lattice infill and multiscale design",
            "12 min",
            r"""
# Lattice infill and multiscale design

Solid optimized members can be made lighter still by replacing bulk with
**lattices** — periodic or graded cellular structures only additive manufacturing
can build. The design becomes **multiscale**: a macro layout (topology) plus a
micro unit cell whose relative density sets local stiffness.

Cell stiffness scales with **relative density** $\bar\rho$ via a Gibson-Ashby
power law:

$$\frac{E^*}{E_s} = C\left(\frac{\rho^*}{\rho_s}\right)^{n}$$

with $n \approx 2$ for bending-dominated cells (kelvin, octet under bending) and
$n \approx 1$ for stretch-dominated cells (octet truss) — the latter far stiffer
per gram.

```plot
{"title": "Gibson-Ashby: relative modulus vs relative density", "xLabel": "relative density rho*/rho_s", "yLabel": "relative modulus E*/E_s", "xRange": [0, 0.6], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "x", "label": "stretch-dominated n=1", "color": "#16a34a"}, {"expr": "x^2", "label": "bending-dominated n=2", "color": "#dc2626"}]}
```

**Triply periodic minimal surfaces** (TPMS) such as gyroid and Schwarz-P are
popular: smooth, self-supporting, no stress-concentrating nodes, and easy to
grade by varying an offset. A gyroid is the implicit isosurface

$$\sin x\cos y + \sin y\cos z + \sin z\cos x = t$$

where the threshold $t$ tunes wall thickness and thus local density.

```python
import numpy as np

def gyroid(x, y, z, t=0.0):
    # Gyroid implicit field; solid where value <= t.
    return (np.sin(x)*np.cos(y) + np.sin(y)*np.cos(z) + np.sin(z)*np.cos(x)) - t

xs = np.linspace(0, 2*np.pi, 5)
print("on-surface sign change:", np.sign(gyroid(xs, xs, xs)))
```

You map the macro density field onto local lattice $\bar\rho$, giving stiffness
exactly where the load path demands it.

**Next:** baking additive-manufacturing constraints into the optimizer.
""",
        ),
        _t(
            "Design for additive manufacturing constraints",
            "12 min",
            r"""
# Design for additive manufacturing constraints

An optimized geometry is worthless if it cannot be printed. **DfAM** folds the
process physics into the optimization and the final CAD so the part comes off the
build plate sound.

Key constraints:

- **Overhang / self-support angle** — surfaces shallower than a critical angle
  (typically $\theta_c \approx 45^\circ$ from horizontal in metal PBF) need
  supports. Overhang constraints can be added directly to topology optimization
  (e.g. the AM filter) so members stay self-supporting.
- **Minimum feature size and gap** — set by beam/nozzle and powder removal; the
  filter radius $r_{\min}$ enforces it.
- **Trapped powder / resin** — closed internal voids must have drain holes;
  lattices help.
- **Anisotropy** — layer bonding makes the build (Z) direction weaker; FEA should
  use orthotropic properties oriented to the build.
- **Residual stress and distortion** — fast thermal gradients in metal PBF warp
  parts; orientation and supports manage it.

```mermaid
flowchart TB
  GEO["Optimized geometry"] --> ORI["Choose build orientation"]
  ORI --> OH{"overhang < theta_c?"}
  OH -->|yes| SUP["Add supports / redesign"]
  OH -->|no| FEAT
  SUP --> FEAT{"features > min size?"}
  FEAT -->|no| FIX["Thicken / merge"]
  FEAT -->|yes| DRAIN["Add powder drains"]
  DRAIN --> READY["Build-ready"]
```

```python
import numpy as np

def needs_support(normals_z, theta_c_deg=45.0):
    # Flag downward faces shallower than the self-support angle.
    nz = np.asarray(normals_z)                 # z-component of face normal
    angle = np.degrees(np.arcsin(np.clip(-nz, -1, 1)))  # overhang angle
    return (nz < 0) & (angle < theta_c_deg)

print(needs_support([-0.9, -0.2, 0.5]))  # steep ok, shallow needs support
```

Orientation also affects surface finish, support volume and cost — a small
optimization in itself.

**Next:** verifying the final printed part.
""",
        ),
        _t(
            "Verification of the final printed part",
            "12 min",
            r"""
# Verification of the final printed part

The capstone closes by proving the *physical* part meets the brief — simulation is
necessary but not sufficient. Verification spans dimensions, internal integrity
and mechanical performance.

```mermaid
flowchart TB
  PRINT["Printed part"] --> POST["Heat-treat / HIP / machine seats"]
  POST --> DIM["Dimensional: CMM / 3D scan vs CAD"]
  DIM --> NDT["NDT: CT scan for porosity / inclusions"]
  NDT --> TEST["Mechanical test: load to spec"]
  TEST --> COMP["Compare to FEA + requirements"]
  COMP -->|gap| ROOT["Root-cause: process, model, or design"]
  COMP -->|pass| SIGN["Sign off"]
```

What to check, and why:

- **Dimensional** — CT or structured-light scan overlaid on CAD catches shrinkage
  and distortion; bolt holes and bearing seats are usually post-machined to
  tolerance.
- **Internal quality** — **CT porosity** analysis matters because lack-of-fusion
  voids slash fatigue life; correlate with process parameters.
- **Mechanical** — a static proof load and, for cyclic duty, fatigue testing.
  Compare measured stiffness/strength to FEA to **validate the model**, not just
  the part.

Fatigue deserves attention: as-built surfaces are rough, so the S-N curve sits
below wrought data unless surfaces are finished or HIP'd.

```plot
{"title": "S-N: as-built vs finished additive metal", "xLabel": "log10 cycles to failure", "yLabel": "stress amplitude (MPa)", "xRange": [3, 7], "yRange": [80, 320], "grid": true, "functions": [{"expr": "400-45*x", "label": "machined / HIP", "color": "#16a34a"}, {"expr": "320-45*x", "label": "as-built (rough)", "color": "#dc2626"}]}
```

Discrepancies feed the loop: a stiffness gap may mean wrong material data, a
porosity finding may mean re-tuning the process. Only after a clean pass do you
sign the part off against the original requirements.

**Next:** check the advanced material.
""",
        ),
        _quiz(),
    ),
)


CAPSTONE_GENERATIVE_MECHANICAL_DESIGN_COURSES: tuple[SeedCourse, ...] = (
    _BASICS,
    _INTERMEDIATE,
    _ADVANCED,
)
__all__ = ["CAPSTONE_GENERATIVE_MECHANICAL_DESIGN_COURSES"]
