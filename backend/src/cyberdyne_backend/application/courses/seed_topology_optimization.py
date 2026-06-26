"""Topology Optimization track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on structural topology optimization.
Starts from compliance minimisation and the density (SIMP) approach, builds
through sensitivity analysis, mesh-dependence filtering and the optimality-criteria
and MMA updates, then reaches level-set methods, manufacturing constraints,
3D parts and machine-learning surrogates. Lessons are `text` with LaTeX,
interactive ```plot blocks (SIMP penalisation, convergence, filter kernels),
```mermaid workflow/classification diagrams and runnable ```python/```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, ρ, σ, ∇, Ω, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Topology Optimization — Basics ────────────────────────────────────────────

_BASICS = SeedCourse(
    slug="topology-optimization-basics",
    title="Topology Optimization — Basics",
    description=(
        "The intuition and fundamentals of structural topology optimization: "
        "what it means to find the best material layout in a design domain, the "
        "difference between sizing, shape and topology optimization, the density "
        "(SIMP) idea, the compliance-minimisation problem with a volume "
        "constraint, and why filtering is needed. Interactive plots and diagrams "
        "throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What is topology optimization?",
            "10 min",
            r"""
# What is topology optimization?

**Topology optimization** asks a deceptively simple question: given a design
domain, a set of loads and supports, and a limited amount of material, *where
should the material go* to make the structure perform best? Unlike sizing
optimization (tune a thickness) or shape optimization (move a boundary), topology
optimization is free to create holes, branches and entirely new connectivity. The
result often looks organic — like bone or a tree — because nature solves the same
problem.

Formally we cover the domain with a fine mesh and let an indicator field decide,
element by element, whether material is present. The classic objective is to
minimise **compliance** $c = \mathbf{u}^\top \mathbf{K}\,\mathbf{u}$ (equivalently
maximise stiffness) subject to using no more than a fraction $V_f$ of the domain
volume.

```mermaid
flowchart LR
  D["Design domain + loads + supports"] --> V["Choose volume fraction Vf"]
  V --> O["Optimize material layout"]
  O --> R["Stiff, lightweight structure"]
```

A coarse mental model: stiffness rises steeply as you add the first material along
the load path, then with diminishing returns.

```plot
{"title": "Stiffness gain vs material added", "xLabel": "volume fraction", "yLabel": "relative stiffness", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-4*x)", "label": "diminishing returns", "color": "#2563eb"}]}
```

**Next:** sizing vs shape vs topology optimization.
""",
        ),
        _t(
            "Sizing, shape and topology optimization",
            "11 min",
            r"""
# Sizing, shape and topology optimization

Structural optimization comes in three flavours of increasing design freedom:

- **Sizing** keeps the geometry fixed and tunes parameters — bar cross-sections,
  plate thicknesses. The simplest, but it cannot change *where* material is.
- **Shape** moves the boundaries of an existing layout (fillet radii, hole
  positions) but cannot change the number of holes — the **topology** is fixed.
- **Topology** decides connectivity itself: how many holes, how the load paths
  branch. It is the most general and the hardest.

```mermaid
flowchart LR
  S["Sizing: tune dimensions"] --> H["Shape: move boundaries"]
  H --> T["Topology: change connectivity"]
  T --> N["Final design"]
```

A useful contrast is the design space. Sizing explores a low-dimensional vector;
topology explores a value per element, so the dimension equals the number of
elements (often $10^5$–$10^7$). That richness is why topology optimization needs
gradient information and clever updates rather than brute-force search.

```plot
{"title": "Design freedom vs problem dimension", "xLabel": "method (sizing -> topology)", "yLabel": "log10 design variables", "xRange": [0, 3], "yRange": [0, 7], "grid": true, "functions": [{"expr": "2*x + 1", "label": "growth of design space", "color": "#16a34a"}]}
```

In practice a workflow runs topology optimization first for concept layout, then
shape and sizing to clean it up for manufacture.

**Next:** the density approach and the SIMP model.
""",
        ),
        _t(
            "The density approach and SIMP",
            "12 min",
            r"""
# The density approach and SIMP

A true 0/1 material-or-void choice per element makes the problem combinatorial and
intractable. The **density approach** relaxes it: each element $e$ gets a
continuous **design density** $\rho_e \in [0,1]$, and we interpolate its stiffness
between void and solid.

The dominant interpolation is **SIMP** (Solid Isotropic Material with
Penalisation). The element Young's modulus is

$$E_e(\rho_e) = E_{\min} + \rho_e^{\,p}\,(E_0 - E_{\min}),$$

with penalisation exponent $p \ge 3$ and a tiny $E_{\min}$ to keep the stiffness
matrix non-singular. The exponent makes intermediate (grey) densities *inefficient*
— a half-dense element costs half the volume but delivers only $0.5^3 = 0.125$ of
the stiffness — so the optimiser is pushed toward crisp 0/1 designs.

```plot
{"title": "SIMP penalisation: stiffness vs density", "xLabel": "density rho", "yLabel": "E/E0", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "linear (p=1)", "color": "#2563eb"}, {"expr": "x^3", "label": "SIMP p=3", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  R["Density field rho_e in [0,1]"] --> I["SIMP: E = Emin + rho^p (E0 - Emin)"]
  I --> K["Element stiffness ke"]
  K --> G["Global K, solve K u = F"]
```

**Next:** compliance minimisation with a volume constraint.
""",
        ),
        _t(
            "Compliance minimisation with a volume constraint",
            "12 min",
            r"""
# Compliance minimisation with a volume constraint

The canonical topology problem is **minimum compliance** (maximum stiffness) at a
fixed material budget. With densities $\boldsymbol{\rho}$ as variables:

$$\min_{\boldsymbol{\rho}}\; c(\boldsymbol{\rho}) = \mathbf{u}^\top \mathbf{K}(\boldsymbol{\rho})\,\mathbf{u}$$

subject to the equilibrium $\mathbf{K}(\boldsymbol{\rho})\,\mathbf{u}=\mathbf{F}$,
the volume constraint $\sum_e \rho_e v_e \le V_f\,V_0$, and bounds
$0 \le \rho_e \le 1$.

Compliance is the work done by the external load; minimising it makes the
structure stiff. The volume constraint is what forces *choices* — without it the
optimum is trivially the full domain.

```plot
{"title": "Typical compliance convergence", "xLabel": "iteration", "yLabel": "compliance (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.15 + 0.85*exp(-0.4*x)", "label": "c decreases then plateaus", "color": "#2563eb"}]}
```

A minimal NumPy sketch of one objective evaluation:

```python
import numpy as np

def compliance(rho, K_of, F, p=3.0, Emin=1e-9, E0=1.0):
    K = K_of(Emin + rho**p * (E0 - Emin))  # assemble global stiffness
    u = np.linalg.solve(K, F)              # equilibrium K u = F
    c = float(F @ u)                       # = u^T K u
    return c, u
```

```mermaid
flowchart LR
  A["Assemble K(rho)"] --> B["Solve K u = F"]
  B --> C["Compute compliance c = uT K u"]
  C --> D["Check volume <= Vf"]
```

**Next:** why raw results checkerboard, and what filtering does.
""",
        ),
        _t(
            "Checkerboards, mesh dependence and filtering",
            "11 min",
            r"""
# Checkerboards, mesh dependence and filtering

Solve the bare problem and two artefacts appear. **Checkerboarding** is an
alternating solid/void pattern that the low-order finite elements *over-estimate*
in stiffness — a numerical artefact, not a real structure. **Mesh dependence**
means a finer mesh produces more, thinner members rather than a converged design.

The standard cure is a **filter** with radius $r_{\min}$ that couples each element
to its neighbours, imposing a minimum length scale. A **density filter** replaces
the design density with a weighted average over a neighbourhood $N_e$:

$$\tilde{\rho}_e = \frac{\sum_{i \in N_e} w(r_{ei})\,\rho_i}{\sum_{i \in N_e} w(r_{ei})}, \qquad w(r) = \max(0,\; r_{\min} - r).$$

The hat (cone) weight falls linearly to zero at the filter radius:

```plot
{"title": "Linear (cone) filter weight", "xLabel": "distance r / rmin", "yLabel": "weight", "xRange": [0, 1.5], "yRange": [0, 1], "grid": true, "functions": [{"expr": "abs(1 - x) * 0.5 + (1 - x)*0.5", "label": "w = max(0, 1 - r/rmin)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  P["Raw density rho"] --> F["Filter radius rmin"]
  F --> T["Smoothed density rho-tilde"]
  T --> X["No checkerboards, set length scale"]
```

Filtering removes the artefacts and makes the result mesh-independent — at the
cost of a slightly blurred (grey) boundary, which projection later sharpens.

**Next:** check your understanding of the fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── Topology Optimization — Intermediate ──────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="topology-optimization-intermediate",
    title="Topology Optimization — Intermediate",
    description=(
        "The core quantitative machinery of density-based topology optimization: "
        "the finite-element compliance problem, adjoint sensitivity analysis, "
        "sensitivity vs density filtering, the optimality-criteria and MMA update "
        "schemes, Heaviside projection for crisp boundaries, and the classic "
        "88-line MATLAB/Python implementation. Includes runnable code and plots."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "The discrete compliance problem in FE",
            "12 min",
            r"""
# The discrete compliance problem in FE

In a finite-element setting the compliance objective has a clean per-element form.
Because each element shares the same reference stiffness $\mathbf{k}_0$ scaled by
its SIMP modulus, compliance separates as a sum:

$$c(\boldsymbol{\rho}) = \mathbf{u}^\top \mathbf{K}\,\mathbf{u}
= \sum_e \big(E_{\min} + \rho_e^{\,p}(E_0 - E_{\min})\big)\,\mathbf{u}_e^\top \mathbf{k}_0\,\mathbf{u}_e,$$

where $\mathbf{u}_e$ is the element displacement vector. The global stiffness is
assembled from these element contributions and then $\mathbf{K}\mathbf{u}=\mathbf{F}$
is solved (Cholesky for the symmetric positive-definite system).

```python
import numpy as np

def assemble_K(rho, edofMat, KE, p, Emin, E0, ndof):
    # SIMP element moduli
    E = Emin + rho**p * (E0 - Emin)
    K = np.zeros((ndof, ndof))
    for e, dofs in enumerate(edofMat):
        K[np.ix_(dofs, dofs)] += E[e] * KE   # KE = reference k0
    return K
```

```plot
{"title": "Element compliance contribution vs density", "xLabel": "density rho_e", "yLabel": "stiffness weight rho^p", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x^3", "label": "rho^3", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  RE["rho_e"] --> EE["E_e = Emin + rho^p (E0-Emin)"]
  EE --> KE["k_e = E_e k0"]
  KE --> AS["Assemble global K"]
  AS --> SO["Solve K u = F"]
```

**Next:** the adjoint method for sensitivities.
""",
        ),
        _t(
            "Adjoint sensitivity analysis",
            "13 min",
            r"""
# Adjoint sensitivity analysis

Gradient-based topology optimization needs $\partial c / \partial \rho_e$ for every
element — potentially millions of derivatives. Computing them by finite differences
is hopeless. The **adjoint method** delivers all of them at the cost of essentially
one extra solve. For self-adjoint compliance the result is remarkably simple:

$$\frac{\partial c}{\partial \rho_e}
= -\,p\,\rho_e^{\,p-1}(E_0 - E_{\min})\,\mathbf{u}_e^\top \mathbf{k}_0\,\mathbf{u}_e.$$

The sensitivity is **always negative** (adding material lowers compliance) and is
largest where the element stores the most strain energy — exactly where material
matters most. Because compliance is self-adjoint, the adjoint vector equals
$-\mathbf{u}$ and no second linear solve is needed at all.

```python
import numpy as np

def dc_drho(rho, ue_all, KE, p, Emin, E0):
    # ue_all[e] is the element displacement vector for element e
    dc = np.empty(len(rho))
    for e, ue in enumerate(ue_all):
        dc[e] = -p * rho[e]**(p-1) * (E0 - Emin) * (ue @ KE @ ue)
    return dc
```

```plot
{"title": "Sensitivity magnitude vs density (p=3)", "xLabel": "density rho_e", "yLabel": "|dc/drho| (per unit strain energy)", "xRange": [0, 1], "yRange": [0, 3], "grid": true, "functions": [{"expr": "3*x^2", "label": "p rho^(p-1)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  U["Solve K u = F"] --> SE["Element strain energy ue^T k0 ue"]
  SE --> DC["dc/drho = -p rho^(p-1) (E0-Emin) * SE"]
  DC --> UP["Feed to update scheme"]
```

**Next:** filtering the sensitivities and densities.
""",
        ),
        _t(
            "Sensitivity and density filtering",
            "12 min",
            r"""
# Sensitivity and density filtering

Two filter variants regularise the problem. The **sensitivity filter** (Sigmund's
original) smooths the *gradients* before the update:

$$\widehat{\frac{\partial c}{\partial \rho_e}}
= \frac{1}{\rho_e \sum_{i} H_{ei}} \sum_{i \in N_e} H_{ei}\,\rho_i\,\frac{\partial c}{\partial \rho_i},$$

with cone weights $H_{ei} = \max(0, r_{\min} - \mathrm{dist}(e,i))$. The **density
filter** instead smooths the *densities* and then differentiates through the filter
by the chain rule — more consistent and easier to extend with projection.

```python
import numpy as np

def build_filter(coords, rmin):
    n = len(coords); H = np.zeros((n, n))
    for e in range(n):
        d = np.linalg.norm(coords - coords[e], axis=1)
        H[e] = np.maximum(0.0, rmin - d)   # cone weights
    Hs = H.sum(axis=1)
    return H, Hs

def density_filter(rho, H, Hs):
    return (H @ rho) / Hs                   # rho-tilde
```

The filter radius $r_{\min}$ sets the minimum feature size; larger $r_{\min}$ gives
thicker, fewer members.

```plot
{"title": "Number of members vs filter radius", "xLabel": "rmin (elements)", "yLabel": "relative member count", "xRange": [1, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/x", "label": "fewer, thicker members", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  S["Sensitivity filter: smooth dc/drho"] --> A["Less robust, heuristic"]
  D["Density filter: smooth rho"] --> B["Chain-rule consistent, extensible"]
```

**Next:** the optimality criteria and MMA update schemes.
""",
        ),
        _t(
            "Optimality criteria and MMA updates",
            "13 min",
            r"""
# Optimality criteria and MMA updates

Given sensitivities and the volume constraint, we need an **update rule**. The
**Optimality Criteria (OC)** method is a fixed-point scheme tailored to single
volume-constrained compliance. Each density is scaled by a factor
$B_e^{\eta}$ where $B_e = -(\partial c/\partial \rho_e)/(\lambda\,\partial V/\partial \rho_e)$,
clipped by a move limit $m$ and the $[0,1]$ bounds:

$$\rho_e^{\text{new}} = \max\!\big(0,\ \rho_e - m,\ \min(1,\ \rho_e + m,\ \rho_e B_e^{\eta})\big).$$

A bisection on the Lagrange multiplier $\lambda$ enforces the volume constraint
each iteration. OC is fast but limited to one constraint; the **Method of Moving
Asymptotes (MMA)** by Svanberg handles many constraints by building a convex
separable subproblem with moving asymptotes around the current point — the workhorse
for industrial topology optimization.

```python
import numpy as np

def oc_update(rho, dc, dv, volfrac, n_el, move=0.2):
    l1, l2 = 0.0, 1e9
    while (l2 - l1) / (l1 + l2 + 1e-12) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        be = np.sqrt(np.maximum(0, -dc / (dv * lmid)))
        rho_new = np.clip(rho * be, np.maximum(0, rho - move),
                          np.minimum(1, rho + move))
        if rho_new.sum() > volfrac * n_el:
            l1 = lmid          # too much material -> raise lambda
        else:
            l2 = lmid
    return rho_new
```

```plot
{"title": "OC volume bisection convergence", "xLabel": "bisection step", "yLabel": "lambda interval width", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.6*x)", "label": "halving each step", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  DC["Sensitivities dc, dv"] --> OC["OC: rho * Be^eta"]
  OC --> BI["Bisect lambda for volume"]
  BI --> MV["Apply move limit + bounds"]
```

**Next:** Heaviside projection for crisp 0/1 boundaries.
""",
        ),
        _t(
            "Heaviside projection for crisp designs",
            "11 min",
            r"""
# Heaviside projection for crisp designs

Density filtering blurs boundaries into a grey band. **Heaviside projection** pushes
the filtered density $\tilde{\rho}$ toward 0 or 1 around a threshold $\eta$ using a
smoothed step with sharpness $\beta$:

$$\bar{\rho}_e = \frac{\tanh(\beta\eta) + \tanh\!\big(\beta(\tilde{\rho}_e - \eta)\big)}{\tanh(\beta\eta) + \tanh\!\big(\beta(1 - \eta)\big)}.$$

As $\beta \to \infty$ the projection approaches a true step, so the final design is
nearly black-and-white. In practice $\beta$ is **continued** (doubled every few
dozen iterations) so the problem stays smooth early and crisp late. Combining
filter + projection also enables **robust** formulations (eroded / intermediate /
dilated designs) that guarantee a minimum length scale.

```plot
{"title": "Heaviside projection (eta=0.5)", "xLabel": "filtered density rho-tilde", "yLabel": "projected rho-bar", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "beta=0 (no projection)", "color": "#2563eb"}, {"expr": "(1 + tan(2*(x - 0.5)) * 0) + 0*x", "label": "ref", "color": "#16a34a"}]}
```

```python
import numpy as np

def heaviside(rho_tilde, beta, eta=0.5):
    num = np.tanh(beta*eta) + np.tanh(beta*(rho_tilde - eta))
    den = np.tanh(beta*eta) + np.tanh(beta*(1 - eta))
    return num / den
```

```mermaid
flowchart LR
  RT["Filtered rho-tilde"] --> H["Heaviside beta, eta"]
  H --> RB["Projected rho-bar ~ 0/1"]
  RB --> CT["Continuation: increase beta"]
```

**Next:** check your understanding of the core methods.
""",
        ),
        _quiz(),
    ),
)


# ── Topology Optimization — Advanced ──────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="topology-optimization-advanced",
    title="Topology Optimization — Advanced",
    description=(
        "State-of-the-art and applied topology optimization: level-set and "
        "phase-field methods, stress-constrained design, manufacturing constraints "
        "(overhang for additive manufacturing, casting, minimum length scale), "
        "large-scale 3D optimization, multiphysics and multi-material problems, and "
        "machine-learning surrogates and generative design. Includes runnable code "
        "and plots."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Level-set and phase-field methods",
            "13 min",
            r"""
# Level-set and phase-field methods

Density (SIMP) methods optimise a field per element; **level-set methods** instead
represent the structure as the zero contour of a higher-dimensional function
$\phi(\mathbf{x})$: material where $\phi \ge 0$, void where $\phi < 0$. The boundary
moves by solving a **Hamilton–Jacobi** advection equation driven by the shape
derivative $V_n$:

$$\frac{\partial \phi}{\partial t} + V_n\,|\nabla \phi| = 0.$$

The payoff is a **crisp, smooth boundary** at every step — no grey elements — which
makes stress evaluation and CAD export cleaner. The cost is that, in its classic
form, the level set cannot easily nucleate new holes; topological derivatives or a
reaction-diffusion (phase-field) formulation are added to restore that freedom.

```python
import numpy as np

def level_set_update(phi, Vn, dt, dx):
    # first-order upwind |grad phi|, advect the boundary
    gx = np.gradient(phi, dx, axis=0)
    gy = np.gradient(phi, dx, axis=1)
    grad = np.sqrt(gx**2 + gy**2)
    return phi - dt * Vn * grad
```

```plot
{"title": "Boundary velocity decays as design converges", "xLabel": "iteration", "yLabel": "max |Vn|", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "shape converging", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  P["Level set phi(x)"] --> SD["Shape derivative -> Vn"]
  SD --> HJ["Advect: Hamilton-Jacobi"]
  HJ --> RI["Reinitialise phi (signed distance)"]
  RI --> P
```

**Next:** stress-constrained topology optimization.
""",
        ),
        _t(
            "Stress-constrained topology optimization",
            "13 min",
            r"""
# Stress-constrained topology optimization

Minimum compliance gives stiff structures but says nothing about *strength*. Real
parts must keep the von Mises stress below the yield limit everywhere. Adding a
stress constraint per element is brutal for three reasons: the **singularity**
phenomenon (stress constraints vanish in void but block convergence to 0/1), the
**local** nature (millions of constraints), and **highly nonlinear** sensitivities.

The standard remedies: relax stress in low-density elements (the $\varepsilon$- or
qp-relaxation), then **aggregate** the many local constraints into a few global ones
with a **p-norm** or **KS** function that smoothly approximates the maximum:

$$\sigma_{\text{PN}} = \left(\sum_e \big(\sigma_e^{\text{vm}}\big)^{P}\right)^{1/P}
\;\xrightarrow[P\to\infty]{}\; \max_e \sigma_e^{\text{vm}}.$$

```python
import numpy as np

def p_norm_stress(sigma_vm, P=8.0):
    s = np.asarray(sigma_vm)
    return (np.sum(s**P))**(1.0/P)        # smooth max approximation
```

Larger $P$ tracks the true maximum more tightly but stiffens the optimisation:

```plot
{"title": "p-norm approaches the true max stress", "xLabel": "aggregation exponent P", "yLabel": "p-norm / true max", "xRange": [2, 20], "yRange": [1, 1.6], "grid": true, "functions": [{"expr": "1 + 0.8/x", "label": "tightens with P", "color": "#dc2626"}]}
```

```mermaid
flowchart LR
  VM["Local von Mises sigma_e"] --> RX["qp-relaxation in voids"]
  RX --> AG["Aggregate: p-norm / KS"]
  AG --> CN["Few global stress constraints"]
```

**Next:** manufacturing constraints and additive manufacturing.
""",
        ),
        _t(
            "Manufacturing constraints and additive overhang",
            "12 min",
            r"""
# Manufacturing constraints and additive overhang

An optimal layout is useless if it cannot be made. Topology optimization now bakes
**manufacturing constraints** directly into the formulation:

- **Minimum / maximum length scale** via filter + robust (eroded/dilated)
  projection — controls thin members and channel widths.
- **Casting / moulding**: no enclosed voids, plus a draw-direction constraint so
  the part can be extracted from the mould.
- **Additive manufacturing (AM) overhang**: self-supporting designs whose
  down-facing surfaces stay above a critical angle (typically $45^\circ$) so they
  print without sacrificial supports.

The AM overhang filter checks each element against the ones below it: material is
only allowed if it is sufficiently supported.

```plot
{"title": "Need for support vs overhang angle", "xLabel": "overhang angle (deg from horizontal)", "yLabel": "support requirement", "xRange": [0, 90], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1 + exp(0.3*(x - 45)))", "label": "drops past 45 deg", "color": "#16a34a"}]}
```

```python
import numpy as np

def overhang_ok(rho, min_support=0.3):
    # bottom-up: an element may be solid only if supported below
    ok = np.zeros_like(rho)
    ok[0] = rho[0]
    for j in range(1, rho.shape[0]):
        support = np.maximum.reduce([rho[j-1]])  # simplified support region
        ok[j] = np.where(support >= min_support, rho[j], 0.0)
    return ok
```

```mermaid
flowchart LR
  L["Layout"] --> LS["Length-scale (filter+robust)"]
  LS --> DR["Casting: draw direction, no voids"]
  DR --> OV["AM: 45-deg self-support"]
  OV --> M["Manufacturable part"]
```

**Next:** large-scale 3D and multiphysics problems.
""",
        ),
        _t(
            "Large-scale 3D and multiphysics design",
            "12 min",
            r"""
# Large-scale 3D and multiphysics design

Industrial parts live in 3D with $10^7$–$10^8$ elements, so the bottleneck is the
**linear solve** $\mathbf{K}\mathbf{u}=\mathbf{F}$ each iteration. Direct factorisation
becomes infeasible; the field standard is **matrix-free PCG** (preconditioned
conjugate gradient) with **geometric multigrid** preconditioning, run on distributed
MPI clusters or GPUs. This is what enables the famous billion-element aircraft-wing
designs.

The objective also broadens beyond stiffness: **multiphysics** problems couple
elasticity with heat conduction, fluid flow (Stokes/Navier–Stokes channels),
electromagnetics or compliant-mechanism kinematics. Each adds its own state
equation and adjoint, but the SIMP/density + adjoint + filter + MMA scaffold stays
the same.

```python
import numpy as np
from scipy.sparse.linalg import cg

def solve_pcg(K, F, M_inv, tol=1e-8):
    # matrix-free conjugate gradient with a (multigrid) preconditioner M_inv
    u, info = cg(K, F, rtol=tol, M=M_inv)
    return u, info
```

```plot
{"title": "Multigrid PCG: residual vs iteration", "xLabel": "CG iteration", "yLabel": "log10 relative residual", "xRange": [0, 12], "yRange": [-8, 0], "grid": true, "functions": [{"expr": "-0.7*x", "label": "linear convergence", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  D3["3D mesh, 10^7 elements"] --> MF["Matrix-free PCG"]
  MF --> MG["Geometric multigrid precond."]
  MG --> MP["Couple physics: thermal / fluid / EM"]
```

**Next:** machine learning surrogates and generative design.
""",
        ),
        _t(
            "Machine learning and generative design",
            "13 min",
            r"""
# Machine learning and generative design

The iterative cost of full topology optimization (dozens of FE solves) has driven a
wave of **machine-learning acceleration**. Three patterns dominate:

- **Surrogate / direct prediction**: a CNN or U-Net learns the map from boundary
  conditions and loads to the final density field, producing a near-optimal layout
  in one forward pass — then refined by a few real iterations.
- **Generative models** (GANs, VAEs, diffusion) explore *diverse* optimal-quality
  designs for the same problem, supporting human-in-the-loop "generative design"
  in CAD tools (Fusion 360, nTop, Ansys).
- **Online ML** inside the loop: predicting good initial densities or accelerating
  the linear solve.

A typical training target is the converged SIMP density; the loss combines pixel
error with a physics (compliance) penalty so predictions are not just visually but
*mechanically* plausible.

```python
import torch, torch.nn as nn

class TopoUNet(nn.Module):
    def __init__(self, in_ch=3):  # loads, BCs, volume-fraction channel
        super().__init__()
        self.enc = nn.Conv2d(in_ch, 32, 3, padding=1)
        self.dec = nn.Conv2d(32, 1, 3, padding=1)
    def forward(self, x):
        return torch.sigmoid(self.dec(torch.relu(self.enc(x))))  # density in [0,1]
```

```plot
{"title": "ML surrogate cuts iterations to convergence", "xLabel": "iteration", "yLabel": "compliance (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "0.15 + 0.85*exp(-0.4*x)", "label": "classic SIMP", "color": "#2563eb"}, {"expr": "0.15 + 0.4*exp(-0.9*x)", "label": "ML-initialised", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  BC["Loads + BCs + Vf"] --> NN["CNN / U-Net surrogate"]
  NN --> D0["Predicted density"]
  D0 --> FT["Few SIMP iterations (fine-tune)"]
  FT --> OUT["Optimal manufacturable design"]
```

**Next:** check your understanding of the state of the art.
""",
        ),
        _quiz(),
    ),
)


TOPOLOGY_OPTIMIZATION_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["TOPOLOGY_OPTIMIZATION_COURSES"]
