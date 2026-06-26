"""Finite Element Analysis track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on the finite element method for
solids and thermal problems. Starts from discretisation and the weak (variational)
form, builds through element types, shape functions, meshing and assembly, then
reaches structural and thermal solves, convergence, error estimation, nonlinear
and dynamic analysis, and contemporary methods (adaptive refinement, reduced-order
models, ML surrogates, topology optimization). Lessons are `text` with LaTeX,
interactive ```plot blocks (shape functions, convergence, frequency response),
```mermaid workflow/classification diagrams and runnable ```python/```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, ε, ∇, Ω, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Finite Element Analysis — Basics ──────────────────────────────────────────

_BASICS = SeedCourse(
    slug="finite-element-analysis-basics",
    title="Finite Element Analysis — Basics",
    description=(
        "The intuition and fundamentals of the finite element method: why we "
        "discretise a continuous body, the idea of interpolation over elements, "
        "the strong versus weak (variational) form of a boundary value problem, "
        "the simplest 1D bar element, and how local element equations assemble "
        "into a global system. Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why discretise: from continuum to elements",
            "10 min",
            r"""
# Why discretise: from continuum to elements

Most engineering fields — displacement in a loaded bracket, temperature in a fin,
pressure in a flow — are governed by **partial differential equations** that have
no closed-form solution on a real, complicated geometry. The **finite element
method (FEM)** sidesteps this by replacing the continuous body $\Omega$ with a
mesh of small, simple **elements** (lines, triangles, quads, tetrahedra) joined
at **nodes**. The unknown field is approximated by a few values *at the nodes* and
interpolated in between.

The core trade-off: more, smaller elements track the true field better but cost
more to solve. Discretisation error shrinks as the mesh is refined:

```plot
{"title": "Discretisation error vs number of elements", "xLabel": "number of elements", "yLabel": "approx. error (%)", "xRange": [1, 20], "yRange": [0, 60], "grid": true, "functions": [{"expr": "60/x^1.5", "label": "error ~ 1/n^1.5", "color": "#dc2626"}]}
```

The method is general: pick elements, choose how the field varies inside each
(the **shape functions**), enforce the governing physics in an averaged sense,
assemble, and solve a linear system $\mathbf{K}\mathbf{u}=\mathbf{F}$.

```mermaid
flowchart LR
  C["Continuous body, PDE"] --> M["Mesh: nodes + elements"]
  M --> E["Element equations"]
  E --> A["Assemble global system K u = F"]
  A --> S["Solve for nodal values"]
  S --> P["Recover stress / flux"]
```

**Next:** how the field is interpolated inside an element.
""",
        ),
        _t(
            "Nodes, elements and interpolation",
            "11 min",
            r"""
# Nodes, elements and interpolation

Inside an element the unknown field is written as a weighted sum of the **nodal
values** $u_i$ using **shape functions** $N_i(x)$:

$$u(x) \approx \sum_{i=1}^{n} N_i(x)\,u_i.$$

The shape functions are the heart of FEM. Each $N_i$ equals $1$ at its own node
and $0$ at every other node (the **Kronecker-delta** property), and they sum to
$1$ everywhere (**partition of unity**), so a constant field is reproduced
exactly. For a 2-node linear bar element on $0 \le x \le L$:

$$N_1(x) = 1 - \frac{x}{L}, \qquad N_2(x) = \frac{x}{L}.$$

```plot
{"title": "Linear shape functions on a 2-node element (L = 1)", "xLabel": "position x", "yLabel": "N(x)", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - x", "label": "N1 = 1 - x/L", "color": "#2563eb"}, {"expr": "x", "label": "N2 = x/L", "color": "#16a34a"}]}
```

Because $u(x)$ is linear inside this element, its derivative (strain) is
**constant** — a real limitation that drives us to higher-order elements later.
A node shared by two elements forces the field to be **continuous** across the
boundary, which is exactly the inter-element compatibility we want.

```mermaid
flowchart LR
  N["Nodal values u_i"] --> SF["Shape functions N_i(x)"]
  SF --> F["Field u(x) = sum N_i u_i"]
  F --> D["Derivative -> strain / gradient"]
```

**Next:** the strong form and the weak (variational) form.
""",
        ),
        _t(
            "Strong form vs weak form",
            "12 min",
            r"""
# Strong form vs weak form

A boundary value problem is naturally stated in **strong form** — a differential
equation that must hold at *every* point. For 1D axial elasticity with stiffness
$EA$ and distributed load $f(x)$:

$$\frac{d}{dx}\!\left(EA\,\frac{du}{dx}\right) + f(x) = 0, \qquad 0 < x < L.$$

This demands a twice-differentiable $u$ — too strict for piecewise-linear FEM
fields. The fix is the **weak form**: multiply by an arbitrary **test (weight)
function** $w$, integrate over the domain, and integrate by parts. The
second derivative moves onto $w$, lowering the smoothness required of $u$:

$$\int_0^L EA\,\frac{dw}{dx}\frac{du}{dx}\,dx = \int_0^L w f\,dx + \big[w\,EA\,u'\big]_0^L.$$

The boundary term carries the **natural (Neumann)** condition (applied force /
flux); **essential (Dirichlet)** conditions (prescribed displacement) are imposed
directly and make $w$ vanish there. This is the **Galerkin** method when $w$ is
built from the same shape functions as $u$.

```mermaid
flowchart LR
  S["Strong form: PDE at every point"] --> W["Multiply by test function w"]
  W --> I["Integrate over domain"]
  I --> P["Integrate by parts"]
  P --> WF["Weak form: integral statement"]
  WF --> G["Galerkin: w from same N_i"]
```

The weak form is the launch point for the element equations: the integral splits
naturally into element-by-element contributions.

**Next:** building the simplest element — the 1D bar.
""",
        ),
        _t(
            "The 1D bar element",
            "12 min",
            r"""
# The 1D bar element

Apply the weak form to one 2-node bar of length $L$, area $A$, modulus $E$. With
$u(x) = N_1 u_1 + N_2 u_2$, the strain is $\varepsilon = du/dx = (u_2-u_1)/L$, a
constant. Substituting the shape-function derivatives into the weak form gives the
**element stiffness matrix**:

$$\mathbf{k}^e = \frac{EA}{L}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix},
\qquad \mathbf{k}^e \mathbf{u}^e = \mathbf{f}^e.$$

It is symmetric, singular (an unconstrained bar can translate freely), and looks
exactly like a linear spring of stiffness $k = EA/L$ — FEM recovers the physics we
already know.

```plot
{"title": "Bar element acts like a spring: force vs elongation", "xLabel": "elongation (mm)", "yLabel": "axial force (kN)", "xRange": [0, 2], "yRange": [0, 80], "grid": true, "functions": [{"expr": "40*x", "label": "F = (EA/L) * delta", "color": "#2563eb"}]}
```

```python
import numpy as np

E, A, L = 200e9, 1e-4, 0.5     # Pa, m^2, m
k = E * A / L
ke = k * np.array([[1.0, -1.0], [-1.0, 1.0]])
# Fix node 0, pull node 1 with P = 30 kN: solve k * u1 = P
P = 30e3
u1 = P / k
print(f"k = {k:.3e} N/m, tip displacement = {u1 * 1e3:.4f} mm")
print("element stiffness:\n", ke)
```

The same derivation, with more nodes or in 2D/3D, produces every other element —
only the shape functions and the integral change.

**Next:** putting elements together by assembly.
""",
        ),
        _t(
            "Assembly into a global system",
            "11 min",
            r"""
# Assembly into a global system

A structure is a collection of elements that share nodes. **Assembly** adds each
element's stiffness contribution into the right slots of a large **global
stiffness matrix** $\mathbf{K}$, indexed by the global node (and DOF) numbers.
Where two elements meet at a node, their entries **superpose**:

$$\mathbf{K}\,\mathbf{u} = \mathbf{F}.$$

For two bars in series (nodes 0-1-2) the assembled $3\times3$ matrix adds the
$1$-$1$ corner of element A to the $1$-$1$ corner of element B at the shared node.
Raw $\mathbf{K}$ is singular until **boundary conditions** remove rigid-body
motion; we then solve the reduced system.

```python
import numpy as np

E, A, L = 200e9, 1e-4, 0.5
k = E * A / L
ke = k * np.array([[1.0, -1.0], [-1.0, 1.0]])

K = np.zeros((3, 3))
for n in (0, 1):                 # elements 0-1 and 1-2
    K[n:n + 2, n:n + 2] += ke    # scatter-add (assembly)

# Node 0 fixed; force P at the free end (node 2)
P = 30e3
Kr = K[1:, 1:]                   # apply Dirichlet BC by deleting row/col 0
u = np.linalg.solve(Kr, np.array([0.0, P]))
print(f"u1 = {u[0] * 1e3:.4f} mm, u2 (tip) = {u[1] * 1e3:.4f} mm")
```

The pattern — *form element matrix -> scatter into global -> apply BCs -> solve*
— is identical for thousands of elements; only the bookkeeping grows.

```mermaid
flowchart LR
  E1["Element A matrix"] --> G["Global K (scatter-add)"]
  E2["Element B matrix"] --> G
  G --> BC["Apply boundary conditions"]
  BC --> SOL["Solve K u = F"]
```

**Next:** what FEM is used for in practice.
""",
        ),
        _t(
            "Where FEM is used: a first workflow",
            "10 min",
            r"""
# Where FEM is used: a first workflow

FEM is the workhorse of computational engineering: structural stress and
deflection, heat conduction, vibration and modal analysis, fluid and
electromagnetic fields, crash and forming simulation. Every analysis follows the
same three-phase workflow, and most analyst time is spent *outside* the solver.

**Pre-processing** — build/clean geometry (CAD), define material and section
properties, mesh, apply loads and boundary conditions. **Solution** — assemble and
solve $\mathbf{K}\mathbf{u}=\mathbf{F}$ (or a nonlinear / transient variant).
**Post-processing** — recover and visualise stress, strain, temperature; check
results against hand calculations and convergence.

```mermaid
flowchart LR
  CAD["CAD geometry"] --> PRE["Pre-process: mesh, materials, BCs, loads"]
  PRE --> SOLVE["Solver: K u = F"]
  SOLVE --> POST["Post-process: stress, deflection, plots"]
  POST --> V["Validate vs theory / tests"]
  V -->|"refine"| PRE
```

The cardinal rule: **a result is meaningless without validation**. Always sanity
check magnitudes (does the tip deflection match $PL^3/3EI$?), watch units, and
confirm the answer stops changing as the mesh is refined.

```plot
{"title": "Solution converges as the mesh is refined", "xLabel": "mesh refinement level", "yLabel": "computed tip deflection (mm)", "xRange": [1, 8], "yRange": [0, 12], "grid": true, "functions": [{"expr": "10 - 9*exp(-0.7*x)", "label": "approaches exact value", "color": "#16a34a"}]}
```

Popular tools: ANSYS, Abaqus, COMSOL, Nastran (commercial); CalculiX, FEniCS,
Code_Aster (open source). They differ in interface, not in the underlying method.

**Next:** the Intermediate course — element types, mapping, integration and solves.
""",
        ),
        _quiz(),
    ),
)


# ── Finite Element Analysis — Intermediate ────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="finite-element-analysis-intermediate",
    title="Finite Element Analysis — Intermediate",
    description=(
        "The core quantitative machinery of FEM: families of element types and "
        "their shape functions, isoparametric mapping and the Jacobian, numerical "
        "(Gauss) integration of element matrices, building the 2D structural "
        "element with the B-matrix, solving steady-state heat conduction, and "
        "meshing strategy with element quality. Worked equations, plots and Python "
        "computations throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Element types and shape functions",
            "13 min",
            r"""
# Element types and shape functions

Elements are classified by **dimension** (1D bar/beam, 2D triangle/quad, 3D
tet/hex) and by **order** (linear vs quadratic). Order sets the polynomial degree
of the interpolation and therefore the accuracy. A **linear** (2-node) element has
constant strain; a **quadratic** (3-node) element adds a mid-side node and lets
strain vary linearly — far more accurate for bending.

For a 3-node quadratic line on the reference coordinate $\xi \in [-1, 1]$:

$$N_1 = \tfrac{1}{2}\xi(\xi-1), \quad N_2 = 1-\xi^2, \quad N_3 = \tfrac{1}{2}\xi(\xi+1).$$

```plot
{"title": "Quadratic shape functions on the reference element", "xLabel": "xi", "yLabel": "N(xi)", "xRange": [-1, 1], "yRange": [-0.3, 1.1], "grid": true, "functions": [{"expr": "0.5*x*(x-1)", "label": "N1 (left node)", "color": "#2563eb"}, {"expr": "1 - x^2", "label": "N2 (mid node)", "color": "#16a34a"}, {"expr": "0.5*x*(x+1)", "label": "N3 (right node)", "color": "#dc2626"}]}
```

```python
import numpy as np

xi = np.array([-1.0, 0.0, 1.0])            # the three node locations
N = np.vstack([0.5 * xi * (xi - 1),        # N1
               1 - xi ** 2,                # N2
               0.5 * xi * (xi + 1)]).T     # N3
print("Kronecker-delta property (should be identity):\n", np.round(N, 6))
print("partition of unity (rows sum to 1):", np.round(N.sum(axis=1), 6))
```

Triangles use **area (barycentric) coordinates**; quads and bricks use tensor
products of 1D functions. Higher order buys accuracy per element but costs more
integration points and a denser system — the classic **h- vs p-refinement** choice.

**Next:** mapping real elements to a reference element.
""",
        ),
        _t(
            "Isoparametric mapping and the Jacobian",
            "13 min",
            r"""
# Isoparametric mapping and the Jacobian

Real meshes have distorted, curved-sided elements. Rather than integrate over each
oddly shaped element, we map every element to a single **reference (parent)
element** in natural coordinates $\xi$ and integrate there. In an **isoparametric**
element the *same* shape functions interpolate both the field and the geometry:

$$x(\xi) = \sum_i N_i(\xi)\,x_i, \qquad u(\xi) = \sum_i N_i(\xi)\,u_i.$$

Derivatives in physical space need the **Jacobian** $J = dx/d\xi = \sum_i
(dN_i/d\xi)\,x_i$, which relates the two coordinate systems:

$$\frac{dN_i}{dx} = \frac{1}{J}\frac{dN_i}{d\xi}, \qquad dx = J\,d\xi.$$

The determinant $\det J$ is the local stretch/area scale; it **must be positive
everywhere** — a zero or negative Jacobian means a folded or inverted element,
which corrupts the solve.

```python
import numpy as np

# 4-node quad, slightly distorted; evaluate Jacobian at the centre (xi=eta=0)
nodes = np.array([[0.0, 0.0], [2.2, 0.1], [2.0, 1.0], [0.1, 1.1]])
# dN/dxi, dN/deta for bilinear quad at (0,0):
dN_dxi = 0.25 * np.array([-1, 1, 1, -1])
dN_deta = 0.25 * np.array([-1, -1, 1, 1])
J = np.array([dN_dxi @ nodes, dN_deta @ nodes])
print("Jacobian:\n", J)
print(f"det(J) = {np.linalg.det(J):.4f}  (must be > 0)")
```

```mermaid
flowchart LR
  R["Reference element (xi, eta)"] --> MAP["x = sum N_i x_i"]
  MAP --> P["Physical distorted element"]
  P --> J["Jacobian J = dx/d xi"]
  J --> INT["Integrate in reference space"]
```

**Next:** evaluating those integrals numerically — Gauss quadrature.
""",
        ),
        _t(
            "Numerical integration with Gauss quadrature",
            "12 min",
            r"""
# Numerical integration with Gauss quadrature

Element matrices are integrals of shape-function products over the reference
element. Closed forms exist only for simple cases, so FEM uses **Gauss-Legendre
quadrature**: approximate the integral by a weighted sum at clever sample points.

$$\int_{-1}^{1} g(\xi)\,d\xi \approx \sum_{p=1}^{m} w_p\, g(\xi_p).$$

An $m$-point Gauss rule integrates polynomials up to degree $2m-1$ **exactly**.
The 2-point rule ($\xi = \pm 1/\sqrt{3}$, weights $1$) handles linear-element
stiffness; quadratic elements need 3 points (in each direction). In 2D/3D the
rules are tensor products, and the determinant of the Jacobian enters the weight:
$\int_\Omega \dots\, d\Omega = \sum_p w_p (\det J)_p (\dots)_p$.

```python
import numpy as np

# Verify 2-point Gauss integrates a cubic exactly on [-1, 1]
pts = np.array([-1 / np.sqrt(3), 1 / np.sqrt(3)])
wts = np.array([1.0, 1.0])
g = lambda x: 3 * x ** 3 + 2 * x ** 2 - x + 5
gauss = np.sum(wts * g(pts))
exact = 4.0 / 3 + 10          # integral of g on [-1,1]
print(f"Gauss = {gauss:.6f}, exact = {exact:.6f}")
```

```plot
{"title": "Quadrature error vs number of Gauss points", "xLabel": "number of points m", "yLabel": "log10 integration error", "xRange": [1, 6], "yRange": [-12, 0], "grid": true, "functions": [{"expr": "1 - 3*x", "label": "error falls sharply with m", "color": "#dc2626"}]}
```

**Reduced integration** (fewer points) speeds the solve and can soften
over-stiff elements, but too few points causes spurious **hourglass** zero-energy
modes — a real pitfall in practice.

**Next:** assembling a 2D structural element with the B-matrix.
""",
        ),
        _t(
            "The 2D structural element and the B-matrix",
            "13 min",
            r"""
# The 2D structural element and the B-matrix

For 2D solids each node has two displacement DOFs $(u, v)$. The **strain-
displacement matrix** $\mathbf{B}$ holds the shape-function derivatives and maps
nodal displacements to the strain vector $\{\varepsilon_x, \varepsilon_y,
\gamma_{xy}\}$:

$$\boldsymbol{\varepsilon} = \mathbf{B}\,\mathbf{u}^e.$$

With the elastic **constitutive matrix** $\mathbf{D}$ (plane stress or plane
strain), the element stiffness is the integral

$$\mathbf{k}^e = \int_{\Omega^e} \mathbf{B}^{\mathsf T}\,\mathbf{D}\,\mathbf{B}\;t\,d\Omega
= \sum_p w_p\,(\det J)_p\,\mathbf{B}_p^{\mathsf T}\mathbf{D}\,\mathbf{B}_p\,t.$$

The **constant-strain triangle (CST)** has constant $\mathbf{B}$, so its stiffness
needs no quadrature:

```python
import numpy as np

# CST element; plane stress
xy = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0]])  # node coords (m)
E, nu, t = 200e9, 0.3, 0.01
x, y = xy[:, 0], xy[:, 1]
b = np.array([y[1] - y[2], y[2] - y[0], y[0] - y[1]])
c = np.array([x[2] - x[1], x[0] - x[2], x[1] - x[0]])
Area = 0.5 * abs((x[1] - x[0]) * (y[2] - y[0]) - (x[2] - x[0]) * (y[1] - y[0]))
B = np.zeros((3, 6))
B[0, 0::2] = b; B[1, 1::2] = c
B[2, 0::2] = c; B[2, 1::2] = b
B /= (2 * Area)
D = E / (1 - nu ** 2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
ke = t * Area * B.T @ D @ B
print(f"ke shape {ke.shape}, symmetric: {np.allclose(ke, ke.T)}")
```

Quads use Gauss integration of the same $\mathbf{B}^{\mathsf T}\mathbf{D}\mathbf{B}$
form. This single expression underlies all 2D/3D stress analysis.

**Next:** the same machinery applied to heat conduction.
""",
        ),
        _t(
            "Steady-state heat conduction by FEM",
            "12 min",
            r"""
# Steady-state heat conduction by FEM

FEM is not limited to structures. Steady **heat conduction** obeys the Poisson
equation $\nabla\!\cdot(k\nabla T) + Q = 0$, whose weak form yields a **conductivity
matrix** that is the thermal analogue of stiffness:

$$\mathbf{K}_T\,\mathbf{T} = \mathbf{Q}, \qquad
\mathbf{K}_T^e = \int_{\Omega^e} k\,\mathbf{B}_T^{\mathsf T}\mathbf{B}_T\,d\Omega.$$

Here $\mathbf{T}$ holds nodal temperatures and $\mathbf{B}_T$ contains the
shape-function gradients. **Dirichlet** BCs fix temperatures; **Neumann** BCs apply
heat flux; **convection** (Robin) BCs add a boundary term $hA$ to $\mathbf{K}_T$
and $h A T_\infty$ to the load. The structure of the solve is identical to the
structural case — only the physics in the element integral changes.

```python
import numpy as np

# 1D wall, 4 linear elements; left face fixed at 100 C, right convects to 20 C
n_el = 4
k, A, L = 30.0, 1.0, 0.2       # W/mK, m^2, m
h, Tinf = 25.0, 20.0           # convection coefficient, ambient
le = L / n_el
ke = k * A / le * np.array([[1.0, -1.0], [-1.0, 1.0]])
K = np.zeros((n_el + 1, n_el + 1))
F = np.zeros(n_el + 1)
for e in range(n_el):
    K[e:e + 2, e:e + 2] += ke
K[-1, -1] += h * A             # convection at right node
F[-1] += h * A * Tinf
# Dirichlet at node 0: T0 = 100
T0 = 100.0
F -= K[:, 0] * T0
T = np.zeros(n_el + 1); T[0] = T0
T[1:] = np.linalg.solve(K[1:, 1:], F[1:])
print("nodal temperatures (C):", np.round(T, 2))
```

```plot
{"title": "Temperature profile across a conducting wall", "xLabel": "position through wall (mm)", "yLabel": "temperature (C)", "xRange": [0, 200], "yRange": [20, 100], "grid": true, "functions": [{"expr": "100 - 0.35*x", "label": "near-linear conduction profile", "color": "#dc2626"}]}
```

**Next:** building a good mesh and judging element quality.
""",
        ),
        _t(
            "Meshing strategy and element quality",
            "11 min",
            r"""
# Meshing strategy and element quality

The mesh is the single biggest lever on accuracy and cost. **Structured** meshes
(regular quads/hexes) are efficient and accurate; **unstructured** meshes (tris/tets)
fill arbitrary geometry automatically. The art is putting elements where the field
changes fast — at fillets, holes and load points — and coarsening elsewhere.

Element **quality** metrics flag elements that degrade the solve:

- **Aspect ratio** — long thin elements lose accuracy; keep it low.
- **Skewness** — deviation from the ideal shape; high skew distorts the Jacobian.
- **Jacobian ratio** — must stay positive; near-zero signals near-inverted elements.

```python
import numpy as np

# Aspect ratio of a quad element from its node coordinates
quad = np.array([[0, 0], [4.0, 0], [4.0, 0.5], [0, 0.5]])
edges = np.linalg.norm(np.diff(np.vstack([quad, quad[0]]), axis=0), axis=1)
aspect = edges.max() / edges.min()
print(f"edge lengths = {np.round(edges, 2)}, aspect ratio = {aspect:.1f}")
print("warn: aspect ratio > 5" if aspect > 5 else "ok")
```

Always perform **mesh refinement (convergence) studies**: solve on progressively
finer meshes and watch a key result (peak stress) stabilise. Use **mesh grading /
local refinement** near stress concentrations rather than refining everywhere.

```mermaid
flowchart LR
  G["Geometry"] --> SEED["Seed sizes (fine at features)"]
  SEED --> MESH["Generate mesh"]
  MESH --> Q["Check quality: aspect, skew, Jacobian"]
  Q -->|"bad"| SEED
  Q -->|"good"| SOLVE["Solve and converge"]
```

```plot
{"title": "Peak stress vs element size (mesh convergence)", "xLabel": "element size (mm)", "yLabel": "peak stress (MPa)", "xRange": [1, 10], "yRange": [100, 200], "grid": true, "functions": [{"expr": "180 - 60*exp(-0.6*x)", "label": "converged value as size -> 0", "color": "#2563eb"}]}
```

**Next:** the Advanced course — convergence theory, dynamics, nonlinearity and modern methods.
""",
        ),
        _quiz(),
    ),
)


# ── Finite Element Analysis — Advanced ────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="finite-element-analysis-advanced",
    title="Finite Element Analysis — Advanced",
    description=(
        "State-of-the-art and applied FEM: convergence theory and a-posteriori "
        "error estimation with adaptive refinement, geometric and material "
        "nonlinearity with Newton-Raphson, dynamic and modal analysis, validation "
        "and verification against theory and tests, and contemporary acceleration "
        "via reduced-order models, machine-learning surrogates and topology "
        "optimization. Worked equations, plots and Python/MATLAB code throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Convergence, consistency and error estimation",
            "13 min",
            r"""
# Convergence, consistency and error estimation

FEM converges to the exact solution as elements shrink, *provided* the elements
are **consistent** (can reproduce constant strain) and **complete** (pass the
**patch test**). The energy-norm error of an order-$p$ element on size-$h$ mesh
obeys an **a-priori** estimate:

$$\|e\|_{E} \le C\,h^{p}\,|u|_{p+1},$$

so halving $h$ for linear elements ($p{=}1$) roughly halves the error; quadratic
elements converge faster. On a log-log plot the slope of error vs $h$ is the
**convergence rate** $p$.

```plot
{"title": "Energy-norm error vs element size (log-log)", "xLabel": "log10(element size h)", "yLabel": "log10(error)", "xRange": [-2, 0], "yRange": [-4, 0], "grid": true, "functions": [{"expr": "2*x", "label": "linear elements, slope ~ 1-2", "color": "#2563eb"}, {"expr": "3*x - 0.5", "label": "quadratic, steeper slope", "color": "#16a34a"}]}
```

In practice the exact solution is unknown, so we use **a-posteriori** error
estimators (e.g. **Zienkiewicz-Zhu** stress recovery, or residual-based
estimators) to flag where error is large and drive **adaptive (h-/p-) refinement**.

```python
import numpy as np

# Estimate convergence rate from two meshes (Richardson extrapolation)
h = np.array([0.1, 0.05])         # element sizes
err = np.array([8.0e-3, 2.1e-3])  # measured energy-norm errors
rate = np.log(err[0] / err[1]) / np.log(h[0] / h[1])
print(f"observed convergence rate p ~ {rate:.2f}")
```

```mermaid
flowchart LR
  SOLVE["Solve on mesh"] --> EST["A-posteriori error estimate"]
  EST --> MARK["Mark high-error elements"]
  MARK --> REF["Refine (h or p)"]
  REF --> SOLVE
  EST -->|"tolerance met"| DONE["Accept solution"]
```

**Next:** problems where stiffness itself changes — nonlinear FEM.
""",
        ),
        _t(
            "Nonlinear FEM and Newton-Raphson",
            "13 min",
            r"""
# Nonlinear FEM and Newton-Raphson

Many real problems are **nonlinear**: large deflections (**geometric**),
plasticity or hyperelasticity (**material**), and contact (**boundary**). The
stiffness now depends on the displacement, so $\mathbf{K}(\mathbf{u})\mathbf{u} =
\mathbf{F}$ cannot be solved in one shot. We define a **residual** and drive it to
zero with **Newton-Raphson** iteration:

$$\mathbf{r}(\mathbf{u}) = \mathbf{F}_\text{int}(\mathbf{u}) - \mathbf{F}_\text{ext},
\qquad \mathbf{K}_T\,\Delta\mathbf{u} = -\mathbf{r},\quad
\mathbf{u} \leftarrow \mathbf{u} + \Delta\mathbf{u},$$

where $\mathbf{K}_T = \partial\mathbf{F}_\text{int}/\partial\mathbf{u}$ is the
**tangent stiffness**. With a good tangent, convergence is **quadratic** — the
residual norm squares each iteration.

```python
import numpy as np

# Nonlinear spring: f_int = k*u + alpha*u^3 = F_ext, solve by Newton
k, alpha, F = 1000.0, 5e6, 200.0
u = 0.0
for it in range(10):
    r = k * u + alpha * u ** 3 - F      # residual
    Kt = k + 3 * alpha * u ** 2         # tangent
    du = -r / Kt
    u += du
    print(f"iter {it}: u = {u:.6e}, |r| = {abs(r):.3e}")
    if abs(r) < 1e-9:
        break
```

```plot
{"title": "Newton-Raphson residual norm vs iteration (quadratic)", "xLabel": "iteration", "yLabel": "log10(residual norm)", "xRange": [0, 6], "yRange": [-12, 1], "grid": true, "functions": [{"expr": "1 - 2.2*x", "label": "quadratic convergence", "color": "#dc2626"}]}
```

**Load stepping** (incrementing $\mathbf{F}_\text{ext}$) and **arc-length** methods
handle snap-through and softening where plain Newton diverges.

**Next:** motion and vibration — dynamic and modal analysis.
""",
        ),
        _t(
            "Dynamic and modal analysis",
            "13 min",
            r"""
# Dynamic and modal analysis

Time-dependent problems add a **mass matrix** $\mathbf{M}$ and **damping**
$\mathbf{C}$ to the equilibrium, giving the semi-discrete equation of motion:

$$\mathbf{M}\ddot{\mathbf{u}} + \mathbf{C}\dot{\mathbf{u}} + \mathbf{K}\mathbf{u}
= \mathbf{F}(t).$$

The undamped, unforced problem is the **generalised eigenvalue problem**
$\mathbf{K}\boldsymbol{\phi} = \omega^2 \mathbf{M}\boldsymbol{\phi}$, whose roots
are the **natural frequencies** $\omega_n$ and **mode shapes** $\boldsymbol{\phi}$.
Near a natural frequency a structure resonates — the dynamic amplification peaks:

```plot
{"title": "Frequency response: amplification vs frequency ratio", "xLabel": "frequency ratio r = omega/omega_n", "yLabel": "amplification factor", "xRange": [0, 3], "yRange": [0, 6], "grid": true, "functions": [{"expr": "1/sqrt((1-x^2)^2 + (0.2*x)^2)", "label": "FRF (damping = 0.1)", "color": "#2563eb"}]}
```

```python
import numpy as np
from scipy.linalg import eigh

# 3-DOF lumped-mass chain; natural frequencies via generalized eigenproblem
m, k = 1.0, 1000.0
M = m * np.eye(3)
K = k * np.array([[2.0, -1, 0], [-1, 2, -1], [0, -1, 1]])
w2, phi = eigh(K, M)            # K phi = w^2 M phi
wn = np.sqrt(w2)
print("natural frequencies (rad/s):", np.round(wn, 2))
print("frequencies (Hz):", np.round(wn / (2 * np.pi), 2))
```

For transient response we integrate in time with **Newmark-beta** or **HHT-alpha**
(implicit, unconditionally stable) or **central difference** (explicit, used for
crash/impact). Damping is often modelled as **Rayleigh** $\mathbf{C} = a\mathbf{M}
+ b\mathbf{K}$.

**Next:** trusting the answer — verification and validation.
""",
        ),
        _t(
            "Verification, validation and result interpretation",
            "12 min",
            r"""
# Verification, validation and result interpretation

A pretty contour plot is not a correct one. **Verification** asks *did we solve the
equations right?* (mesh convergence, code/patch tests, comparison to analytical
benchmarks). **Validation** asks *did we solve the right equations?* (comparison to
physical experiments). Both are mandatory before trusting an FEM result.

Common pitfalls to interpret carefully:

- **Stress singularities** at sharp re-entrant corners and point loads — stress
  grows without bound as the mesh refines; never report the singular peak, use a
  realistic fillet or a structural stress method.
- **Averaged vs unaveraged stress** — large jumps between adjacent elements
  signal an under-resolved mesh.
- **Units and boundary conditions** — the most frequent source of order-of-
  magnitude errors.

```python
import numpy as np

# Verify a cantilever FEM result against the closed-form tip deflection
P, L, E, I = 1000.0, 2.0, 200e9, 1e-6
delta_theory = P * L ** 3 / (3 * E * I)
delta_fem = 0.01293                       # from the solver (m)
err = abs(delta_fem - delta_theory) / delta_theory * 100
print(f"theory = {delta_theory*1e3:.3f} mm, FEM = {delta_fem*1e3:.3f} mm")
print(f"relative error = {err:.2f} %  -> {'PASS' if err < 5 else 'INVESTIGATE'}")
```

```plot
{"title": "Apparent peak stress diverges at a singularity", "xLabel": "1 / element size", "yLabel": "reported peak stress (MPa)", "xRange": [1, 10], "yRange": [100, 400], "grid": true, "functions": [{"expr": "100 + 30*x", "label": "no convergence (singular corner)", "color": "#dc2626"}]}
```

ASME V&V 10/20 codify this discipline for solid mechanics and CFD.

**Next:** going faster — reduced-order models and ML surrogates.
""",
        ),
        _t(
            "Reduced-order models and ML surrogates",
            "13 min",
            r"""
# Reduced-order models and ML surrogates

Full FEM is expensive for many-query tasks — design sweeps, optimization, real-time
digital twins. **Reduced-order models (ROMs)** project the huge system onto a small
basis. **Proper orthogonal decomposition (POD)** extracts dominant modes from
**snapshots** (full solutions at sampled parameters) via the SVD, then solves a
tiny reduced system $\boldsymbol{\Phi}^{\mathsf T}\mathbf{K}\boldsymbol{\Phi}\,
\mathbf{a} = \boldsymbol{\Phi}^{\mathsf T}\mathbf{F}$.

```python
import numpy as np

# POD basis from FEM snapshots; energy captured by leading modes
rng = np.random.default_rng(0)
snapshots = rng.standard_normal((500, 40))      # 500 DOFs x 40 parameter samples
U, S, _ = np.linalg.svd(snapshots, full_matrices=False)
energy = np.cumsum(S ** 2) / np.sum(S ** 2)
r = int(np.searchsorted(energy, 0.99) + 1)
print(f"modes for 99% energy: {r} (vs 500 DOFs) -> {500 // r}x reduction")
Phi = U[:, :r]                                  # reduced basis
```

```plot
{"title": "POD: captured energy vs number of retained modes", "xLabel": "number of modes", "yLabel": "cumulative energy fraction", "xRange": [0, 20], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-0.4*x)", "label": "energy saturates quickly", "color": "#16a34a"}]}
```

Beyond projection, **ML surrogates** (Gaussian processes, neural networks) learn
the map from design parameters to responses directly; **physics-informed neural
networks (PINNs)** and **graph neural networks** on meshes are active research for
fast, differentiable solvers. These complement, not replace, FEM — trained on it
and validated against it.

```mermaid
flowchart LR
  FEM["Full FEM (snapshots)"] --> POD["POD / SVD basis"]
  POD --> ROM["Reduced-order model"]
  FEM --> ML["Train ML surrogate"]
  ROM --> Q["Fast many-query: optimization, digital twin"]
  ML --> Q
```

**Next:** letting the solver design the part — topology optimization.
""",
        ),
        _t(
            "Topology optimization and design-driven FEM",
            "14 min",
            r"""
# Topology optimization and design-driven FEM

The frontier of applied FEM is **inverse design**: let the analysis decide the
shape. **Topology optimization** distributes material in a domain to minimise
**compliance** (maximise stiffness) for a fixed mass. The **SIMP** (Solid
Isotropic Material with Penalisation) method gives each element a density
$\rho_e \in [0,1]$ and penalises intermediate values so the result is nearly
black-and-white:

$$E_e(\rho_e) = \rho_e^{p}\,E_0, \qquad
\min_{\boldsymbol\rho}\; c = \mathbf{u}^{\mathsf T}\mathbf{K}\mathbf{u}
\;\; \text{s.t.}\;\; \textstyle\sum_e \rho_e v_e \le V^{*}.$$

Each iteration: FEM solve, **sensitivity analysis** $\partial c/\partial\rho_e =
-p\,\rho_e^{p-1}\mathbf{u}_e^{\mathsf T}\mathbf{k}_0\mathbf{u}_e$, a density-filter
to avoid checkerboarding, then an **optimality-criteria** update. The objective
falls monotonically and converges:

```plot
{"title": "Topology optimization: compliance vs iteration", "xLabel": "iteration", "yLabel": "normalized compliance", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "compliance ~ exp(-0.4 k)", "color": "#16a34a"}]}
```

```python
import numpy as np

# One SIMP sensitivity + optimality-criteria density update (schematic)
p, vol_frac = 3.0, 0.4
rho = np.full(8, vol_frac)
Ue2 = np.array([2.1, 0.4, 1.8, 0.2, 1.5, 0.3, 0.9, 0.1])   # u_e^T k0 u_e per element
dc = -p * rho ** (p - 1) * Ue2                              # compliance sensitivity
lam = 0.5                                                   # Lagrange multiplier (bisected in practice)
rho_new = np.clip(rho * np.sqrt(-dc / lam), 0.001, 1.0)
rho_new *= vol_frac * len(rho) / rho_new.sum()             # enforce volume
print("updated densities:", np.round(rho_new, 3))
```

```mermaid
flowchart LR
  DOM["Design domain + loads"] --> FEA["FEM solve K u = F"]
  FEA --> SENS["Sensitivity dc/d rho"]
  SENS --> FILT["Density filter"]
  FILT --> UPD["OC / MMA density update"]
  UPD -->|"not converged"| FEA
  UPD --> OUT["Optimized, lightweight design"]
```

Coupled with **additive manufacturing**, topology-optimized parts are now
flight- and production-ready; commercial tools (Altair OptiStruct, ANSYS, nTop)
and open-source (`topopt`, `ToOptiX`) implement these algorithms.

**Next:** you have completed the Finite Element Analysis track.
""",
        ),
        _quiz(),
    ),
)


FINITE_ELEMENT_ANALYSIS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["FINITE_ELEMENT_ANALYSIS_COURSES"]
