"""Computational Fluid Dynamics track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on simulating fluid flow numerically.
Starts from the governing equations and the finite-volume idea, builds through
meshing, boundary conditions, discretisation schemes, turbulence modelling and
the SIMPLE pressure-velocity coupling, and ends with convergence, verification
and validation, HPC, and ML/optimisation-accelerated CFD. Lessons are `text`
with LaTeX, interactive ```plot blocks (residuals, profiles, y+ , GCI),
```mermaid workflow/classification diagrams and runnable ```python/```matlab
snippets.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Computational Fluid Dynamics — Basics ────────────────────────────────────

_BASICS = SeedCourse(
    slug="computational-fluid-dynamics-basics",
    title="Computational Fluid Dynamics — Basics",
    description=(
        "Build intuition for what a CFD solver actually does: the governing "
        "conservation laws, why the equations are discretised, the finite-volume "
        "idea of fluxes through cell faces, the role of the mesh, what boundary "
        "conditions mean, and how an iterative solve marches to a converged "
        "answer. Interactive plots, workflow diagrams and short code throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "What CFD is and the governing equations",
            "11 min",
            r"""
# What CFD is and the governing equations

**Computational Fluid Dynamics (CFD)** solves the equations of fluid motion
numerically on a computer, giving fields of velocity, pressure and temperature
where analytical solutions do not exist. The foundation is three conservation
laws on a fluid: **mass**, **momentum** and **energy**.

For an incompressible Newtonian fluid the core pair is continuity and the
**Navier-Stokes** momentum equation,

$$\nabla\cdot\mathbf{u}=0,\qquad \rho\!\left(\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u}\right) = -\nabla p + \mu\nabla^2\mathbf{u} + \rho\mathbf{g}.$$

The terms are inertia (local + convective), pressure gradient, viscous diffusion
and body force. The **convective** term $(\mathbf{u}\cdot\nabla)\mathbf{u}$ is
nonlinear — the reason CFD is hard and turbulence exists. No general closed-form
solution is known, so we approximate.

```mermaid
flowchart LR
  PHY["Conservation laws: mass, momentum, energy"] --> PDE["Navier-Stokes PDEs"]
  PDE --> DISC["Discretise on a mesh"]
  DISC --> ALG["Algebraic system A x = b"]
  ALG --> SOL["Iterative solver -> flow fields"]
```

```plot
{"title": "Relative magnitude of inertia vs viscous forces (Re)", "xLabel": "characteristic speed V (m/s)", "yLabel": "Reynolds number Re", "xRange": [0, 10], "yRange": [0, 500000], "grid": true, "functions": [{"expr": "x*0.05/1.0e-6", "label": "Re = V L / nu (L=0.05 m, water)", "color": "#2563eb"}]}
```

**Next:** why we cannot solve the PDEs directly — discretisation.
""",
        ),
        _t(
            "From PDEs to a grid: discretisation",
            "12 min",
            r"""
# From PDEs to a grid: discretisation

A computer cannot store a continuous field, so CFD replaces derivatives with
**algebraic approximations** evaluated at a finite set of points or cells. Three
families dominate:

- **Finite Difference (FDM)** — approximate derivatives via Taylor series on a
  structured grid. Simple but awkward on complex geometry.
- **Finite Element (FEM)** — weighted-residual weak form; strong for structural
  and some flow problems.
- **Finite Volume (FVM)** — integrate the conservation law over each cell.
  **Conservative by construction**, so it dominates commercial CFD
  (OpenFOAM, Fluent, Star-CCM+).

A central-difference second derivative on spacing $\Delta x$ is

$$\left.\frac{\partial^2 \phi}{\partial x^2}\right|_i \approx \frac{\phi_{i+1}-2\phi_i+\phi_{i-1}}{\Delta x^2},$$

with **truncation error** $O(\Delta x^2)$: halving the spacing cuts the error by
about four for a second-order scheme.

```plot
{"title": "Discretisation error vs mesh spacing (orders 1 and 2)", "xLabel": "mesh spacing dx (normalised)", "yLabel": "error (normalised)", "xRange": [0.05, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "x", "label": "first order O(dx)", "color": "#dc2626"}, {"expr": "x^2", "label": "second order O(dx^2)", "color": "#2563eb"}]}
```

```python
import numpy as np

phi = lambda x: np.sin(x)          # exact field
x0 = 1.0
for dx in (0.1, 0.05, 0.025):
    approx = (phi(x0+dx) - 2*phi(x0) + phi(x0-dx)) / dx**2
    print(f"dx={dx:.3f}: d2phi={approx:.5f}, exact={-np.sin(x0):.5f}")
```

**Next:** the finite-volume idea of fluxes through cell faces.
""",
        ),
        _t(
            "The finite-volume method and fluxes",
            "13 min",
            r"""
# The finite-volume method and fluxes

The **finite-volume method (FVM)** divides the domain into non-overlapping
**control volumes** (cells) and integrates each conservation law over a cell.
Using the divergence theorem, a volume integral of a flux becomes a **sum of
fluxes through the cell faces**. For a steady scalar $\phi$ transported by
convection and diffusion,

$$\sum_{f}\big(\rho \mathbf{u}\,\phi - \Gamma\nabla\phi\big)_f\!\cdot\mathbf{A}_f = \int_{V} S\,dV,$$

where the sum is over faces $f$, $\Gamma$ is the diffusion coefficient and $S$ a
source. Because what leaves one cell through a face **exactly enters** its
neighbour, FVM is **locally and globally conservative** — mass, momentum and
energy are conserved to machine precision regardless of mesh quality.

```mermaid
flowchart LR
  P["Cell P (centroid value)"] -->|face flux| E["Cell E"]
  W["Cell W"] -->|face flux| P
  P --> BAL["Balance: sum of face fluxes = source"]
```

The face value of $\phi$ is interpolated from neighbouring centroids — the choice
of **interpolation (scheme)** controls accuracy and stability (covered later).

```plot
{"title": "1-D cell balance: flux in - flux out vs source", "xLabel": "cell index", "yLabel": "phi (cell value)", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-0.6*x)", "label": "transported scalar phi(x)", "color": "#16a34a"}]}
```

```python
import numpy as np

# 1-D steady diffusion with FVM: -Gamma d2phi/dx2 = 0, phi(0)=0, phi(1)=1
n = 5
A = np.diag([2.0]*n) - np.diag([1.0]*(n-1), 1) - np.diag([1.0]*(n-1), -1)
b = np.zeros(n); b[-1] = 1.0          # Dirichlet on the right face
phi = np.linalg.solve(A, b)
print("phi:", np.round(phi, 3))       # linear profile, as expected
```

**Next:** the mesh — the discrete skeleton of the domain.
""",
        ),
        _t(
            "Meshes: structured, unstructured and quality",
            "12 min",
            r"""
# Meshes: structured, unstructured and quality

The **mesh** (grid) is the set of cells that tile the domain. Its type and
quality strongly affect accuracy, convergence and cost.

- **Structured** — ordered (i, j, k) hexahedra; efficient and accurate but hard
  on complex shapes.
- **Unstructured** — arbitrary connectivity of tetrahedra/polyhedra; flexible for
  industrial geometry, the workhorse of modern solvers.
- **Hybrid** — structured prism layers near walls (to resolve boundary layers)
  plus unstructured cells in the bulk.

Quality metrics gate a usable mesh: **skewness** (cell distortion, keep low),
**aspect ratio**, **orthogonality** (face-normal alignment) and **smooth growth
ratio** ($<1.2$ typical). Poor cells cause numerical diffusion, slow convergence
or divergence.

```mermaid
flowchart TB
  M["Mesh"] --> S["Structured (hex)"]
  M --> U["Unstructured (tet/poly)"]
  M --> H["Hybrid (prism BL + bulk)"]
  M --> Q["Quality: skewness, aspect ratio, orthogonality"]
```

```plot
{"title": "Solution error vs cell count (more cells, less error)", "xLabel": "log10(cell count)", "yLabel": "discretisation error (normalised)", "xRange": [3, 7], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-(x-3))", "label": "error falls with refinement", "color": "#2563eb"}]}
```

```python
import numpy as np

# Estimate cells in a structured box mesh from target spacing
Lx, Ly, Lz = 2.0, 1.0, 0.5         # domain, m
dx = 0.01                          # target cell size, m
cells = (Lx/dx)*(Ly/dx)*(Lz/dx)
print(f"~{cells:.2e} cells for dx={dx*1000:.0f} mm")
```

**Next:** how we tell the solver about the physical edges — boundary conditions.
""",
        ),
        _t(
            "Boundary and initial conditions",
            "12 min",
            r"""
# Boundary and initial conditions

A PDE on a finite domain needs **boundary conditions (BCs)** on every patch and,
for transient runs, **initial conditions**. The common types:

- **Dirichlet** — fix the value (e.g. inlet velocity, wall temperature).
- **Neumann** — fix the normal gradient (e.g. zero-gradient outflow, adiabatic
  wall $\partial T/\partial n=0$).
- **Robin / mixed** — a combination (e.g. convective heat transfer).

Typical CFD patches: **velocity inlet** (Dirichlet $\mathbf{u}$), **pressure
outlet** (fix $p$, zero-gradient $\mathbf{u}$), **no-slip wall**
($\mathbf{u}=\mathbf{0}$), **symmetry** (zero normal flux) and **periodic**.
Choosing BCs that are physically consistent and well-posed is essential —
over-constraining (e.g. fixing both velocity and pressure at one patch) makes the
problem ill-posed.

```mermaid
flowchart LR
  IN["Velocity inlet (Dirichlet u)"] --> DOM["Domain"]
  WALL["No-slip wall (u = 0)"] --> DOM
  SYM["Symmetry (zero normal flux)"] --> DOM
  DOM --> OUT["Pressure outlet (fix p)"]
```

```plot
{"title": "No-slip wall: velocity rises from 0 across the layer", "xLabel": "distance from wall y (mm)", "yLabel": "u/U_inf", "xRange": [0, 5], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - exp(-1.2*x)", "label": "u(y): 0 at wall -> U_inf", "color": "#2563eb"}]}
```

```python
# A minimal BC dictionary as a solver might store it
bcs = {
    "inlet":   {"type": "velocity", "value": [10.0, 0.0, 0.0]},  # Dirichlet
    "outlet":  {"type": "pressure", "value": 0.0},               # gauge Pa
    "walls":   {"type": "noSlip"},                               # u = 0
    "top":     {"type": "symmetry"},
}
for name, bc in bcs.items():
    print(name, "->", bc["type"])
```

**Next:** how the solver iterates to a converged solution.
""",
        ),
        _t(
            "Convergence and residuals",
            "11 min",
            r"""
# Convergence and residuals

CFD solves a large coupled nonlinear system, so it **iterates**: start from a
guess, sweep the equations, update the fields, repeat. A **residual** measures how
far the current fields are from satisfying the discretised equations — the
imbalance $r = b - A\mathbf{x}$ for each cell, summed (often normalised) per
variable.

**Convergence** means the residuals have fallen by several orders of magnitude
(commonly $10^{-3}$ to $10^{-6}$) **and** monitored quantities of interest (drag,
mass flow, a probe value) have flattened. Watching only residuals is a classic
trap — a steady drag value matters more than a tiny residual.

```plot
{"title": "Residual history (log) over solver iterations", "xLabel": "iteration", "yLabel": "log10(residual)", "xRange": [0, 12], "yRange": [-6, 0], "grid": true, "functions": [{"expr": "-0.5*x", "label": "residual drops ~ exp decay", "color": "#dc2626"}]}
```

**Under-relaxation** factors $\alpha$ damp updates ($\phi^{new}=\phi^{old}+\alpha\,\Delta\phi$)
to keep the nonlinear iteration stable; too small slows convergence, too large
diverges.

```mermaid
flowchart LR
  G["Initial guess"] --> S["Sweep equations"]
  S --> R["Compute residuals"]
  R -->|not converged| S
  R -->|residuals low + monitors flat| D["Converged"]
```

```python
import numpy as np

# Toy fixed-point iteration with under-relaxation toward a root
f = lambda x: 0.5*(x + 2.0/x)     # Newton-like map -> sqrt(2)
x, alpha = 1.0, 0.8
for k in range(6):
    x_new = f(x)
    x = x + alpha*(x_new - x)
    print(f"iter {k}: x={x:.6f}, residual={abs(x*x-2):.2e}")
```

**Next:** check your understanding of the CFD basics.
""",
        ),
        _quiz(),
    ),
)


# ── Computational Fluid Dynamics — Intermediate ──────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="computational-fluid-dynamics-intermediate",
    title="Computational Fluid Dynamics — Intermediate",
    description=(
        "The quantitative core of CFD methods: convection-diffusion "
        "discretisation and scheme accuracy, stability and the CFL condition, "
        "the pressure-velocity coupling problem and SIMPLE, turbulence modelling "
        "with RANS (k-epsilon, k-omega SST) and wall treatment via y+, and "
        "transient time integration. Worked equations, plots and code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Convection-diffusion discretisation schemes",
            "13 min",
            r"""
# Convection-diffusion discretisation schemes

The transported scalar's **face value** must be interpolated from cell centroids.
The choice trades accuracy against stability. For the steady 1-D
convection-diffusion equation $\rho u\,d\phi/dx = \Gamma\,d^2\phi/dx^2$, the
local **Peclet number** $Pe = \rho u \Delta x/\Gamma$ measures convection vs
diffusion.

- **Central Differencing (CDS)** — second order, but oscillates (unbounded) for
  $|Pe|>2$.
- **First-order Upwind (UDS)** — takes the face value from the upstream cell;
  unconditionally bounded but adds **numerical (false) diffusion** that smears
  gradients.
- **Higher-order/bounded** — QUICK, linear-upwind, and TVD limiter schemes (e.g.
  van Leer, MUSCL) recover near-second-order accuracy while staying bounded.

```plot
{"title": "Numerical diffusion: upwind smears a step vs exact", "xLabel": "x", "yLabel": "phi", "xRange": [0, 6], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1/(1+exp(-(x-3)))", "label": "upwind-smeared step", "color": "#dc2626"}]}
```

```python
import numpy as np

# 1-D convection-diffusion with first-order upwind (Pe-stable)
n, u, Gamma, dx = 20, 1.0, 0.02, 1.0/20
Pe = u*dx/Gamma
A = np.zeros((n, n)); b = np.zeros(n)
for i in range(1, n-1):
    A[i, i-1] = -(Gamma/dx + max(u, 0))      # upwind west
    A[i, i+1] = -(Gamma/dx + max(-u, 0))     # upwind east
    A[i, i]   = -(A[i, i-1] + A[i, i+1])
A[0, 0] = A[-1, -1] = 1.0; b[-1] = 1.0       # phi(0)=0, phi(L)=1
phi = np.linalg.solve(A, b)
print(f"cell Pe={Pe:.1f}, phi[5]={phi[5]:.3f}")
```

**Next:** when does the scheme blow up — stability and the CFL number.
""",
        ),
        _t(
            "Stability and the CFL condition",
            "12 min",
            r"""
# Stability and the CFL condition

An explicit time-marching scheme is only **stable** if information does not travel
more than one cell per time step. The **Courant-Friedrichs-Lewy (CFL)** number
captures this:

$$\mathrm{CFL} = \frac{u\,\Delta t}{\Delta x}.$$

For an explicit advection solver stability requires $\mathrm{CFL}\le 1$ (often a
stricter limit in multiple dimensions). Exceed it and the solution oscillates and
diverges — the classic signature of an unstable run. **Implicit** schemes are
unconditionally stable in the linear sense (can use large $\Delta t$) but each
step solves a linear system and large steps still hurt accuracy.

```plot
{"title": "Max stable time step vs cell size (CFL = 1)", "xLabel": "cell size dx (mm)", "yLabel": "max dt (ms) at u = 10 m/s", "xRange": [1, 20], "yRange": [0, 2], "grid": true, "functions": [{"expr": "x/10", "label": "dt = CFL dx / u", "color": "#2563eb"}]}
```

Diffusion has its own explicit limit, the **von Neumann** condition
$\alpha\,\Delta t/\Delta x^2 \le 1/2$. The smaller of the two limits governs.

```python
import numpy as np

u, dx, CFL = 10.0, 0.005, 0.7      # m/s, m, target Courant
dt = CFL*dx/u
print(f"Stable explicit dt = {dt*1000:.3f} ms (CFL={CFL})")

# 1-D explicit upwind advection demo
n = 50; phi = np.zeros(n); phi[:10] = 1.0
for _ in range(20):
    phi[1:] = phi[1:] - CFL*(phi[1:] - phi[:-1])
print("front position cell:", int(np.argmax(phi < 0.5)))
```

**Next:** the central difficulty of incompressible CFD — pressure-velocity coupling.
""",
        ),
        _t(
            "Pressure-velocity coupling and SIMPLE",
            "14 min",
            r"""
# Pressure-velocity coupling and SIMPLE

In incompressible flow there is **no explicit equation for pressure** — continuity
$\nabla\cdot\mathbf{u}=0$ is a constraint, not an evolution equation. Pressure
acts as the field that enforces it. The momentum and continuity equations are
therefore **coupled** and must be solved together.

The **SIMPLE** algorithm (Semi-Implicit Method for Pressure-Linked Equations,
Patankar & Spalding 1972) breaks the deadlock iteratively:

1. Solve momentum with a guessed pressure $p^*$ -> intermediate velocity
   $\mathbf{u}^*$ (does not satisfy continuity).
2. Derive a **pressure-correction** equation from the continuity defect and solve
   it for $p'$.
3. **Correct** velocity and pressure: $p=p^*+\alpha_p p'$, update $\mathbf{u}$.
4. Repeat until the mass imbalance vanishes.

Variants: **SIMPLEC**, **PISO** (extra correctors, good for transient) and
**coupled** solvers that solve momentum and continuity in one matrix.

```mermaid
flowchart LR
  G["Guess p*"] --> MOM["Solve momentum -> u*"]
  MOM --> PC["Pressure-correction p'"]
  PC --> COR["Correct u and p"]
  COR -->|mass imbalance high| MOM
  COR -->|continuity satisfied| DONE["Converged"]
```

```plot
{"title": "Mass imbalance falling over SIMPLE outer iterations", "xLabel": "outer iteration", "yLabel": "log10(continuity residual)", "xRange": [0, 12], "yRange": [-6, 0], "grid": true, "functions": [{"expr": "-0.45*x", "label": "continuity residual", "color": "#dc2626"}]}
```

```python
# Sketch of one SIMPLE outer loop (schematic, not a full solver)
def simple_iteration(u_star, p_star, alpha_p=0.3):
    p_corr = solve_pressure_correction(u_star)   # from continuity defect
    p_new  = p_star + alpha_p * p_corr
    u_new  = correct_velocity(u_star, p_corr)    # makes div(u) -> 0
    return u_new, p_new

def solve_pressure_correction(u):  return 0.0    # placeholder
def correct_velocity(u, p):        return u      # placeholder
print("SIMPLE: momentum -> p' -> correct -> repeat")
```

**Next:** modelling the chaos — turbulence and RANS.
""",
        ),
        _t(
            "Turbulence modelling: RANS and two-equation models",
            "14 min",
            r"""
# Turbulence modelling: RANS and two-equation models

Resolving every turbulent eddy is infeasible for most engineering, so we
**Reynolds-average** the equations. Splitting $\mathbf{u}=\bar{\mathbf{u}}+\mathbf{u}'$
and averaging yields the **RANS** equations with an extra unknown, the **Reynolds
stress** tensor $-\rho\overline{u_i'u_j'}$. Closing it is the *turbulence closure
problem*.

The **Boussinesq hypothesis** models the Reynolds stress with an **eddy
viscosity** $\mu_t$, leaving us to compute $\mu_t$. Two-equation models do this by
transporting two turbulence quantities:

- **k-epsilon** — turbulent kinetic energy $k$ and dissipation $\varepsilon$;
  robust for free-shear flows, weaker near walls/adverse gradients.
- **k-omega SST** — blends k-omega near walls with k-epsilon in the free stream;
  the de-facto default for aerodynamics and separation.

The eddy viscosity scales as $\mu_t = \rho C_\mu k^2/\varepsilon$.

```mermaid
flowchart TB
  NS["Navier-Stokes"] --> RA["Reynolds-average"]
  RA --> RS["Reynolds stress (unknown)"]
  RS --> BO["Boussinesq: eddy viscosity mu_t"]
  BO --> KE["k-epsilon"]
  BO --> KW["k-omega SST"]
```

```plot
{"title": "Turbulent vs laminar mean velocity profile (pipe)", "xLabel": "r/R", "yLabel": "u/u_max", "xRange": [0, 1], "yRange": [0, 1], "grid": true, "functions": [{"expr": "1 - x^2", "label": "laminar (parabolic)", "color": "#2563eb"}, {"expr": "(1-x)^(1/7)", "label": "turbulent (1/7 power law)", "color": "#dc2626"}]}
```

```python
# Eddy viscosity from a k-epsilon state
rho, C_mu = 1.2, 0.09
k, eps = 0.5, 10.0                  # m^2/s^2, m^2/s^3
mu_t = rho*C_mu*k**2/eps
print(f"mu_t = {mu_t:.5f} Pa.s (vs molecular ~1.8e-5)")
```

**Next:** resolving the near-wall region with y+ and wall functions.
""",
        ),
        _t(
            "Near-wall treatment and the y-plus criterion",
            "12 min",
            r"""
# Near-wall treatment and the y-plus criterion

Steep gradients in the boundary layer make near-wall meshing decisive. The
dimensionless wall distance is

$$y^+ = \frac{u_\tau\,y}{\nu},\qquad u_\tau=\sqrt{\tau_w/\rho},$$

where $u_\tau$ is the friction velocity, $y$ the first-cell centroid distance and
$\tau_w$ the wall shear stress. The boundary layer has three zones: the **viscous
sublayer** ($y^+\lesssim5$, $u^+=y^+$), the **buffer layer** ($5<y^+<30$) and the
**log-law region** ($30\lesssim y^+\lesssim 300$, $u^+=\tfrac1\kappa\ln y^+ + B$).

Two strategies:

- **Wall-resolved** — put the first cell in the viscous sublayer, $y^+\approx1$.
  Needed for accurate heat transfer and separation; many prism layers.
- **Wall functions** — bridge the near-wall zone analytically with the first cell
  in the log layer, $30<y^+<300$. Cheaper, fine for attached high-Re flows.

Landing in the buffer layer ($5<y^+<30$) is the worst case — neither model
applies well.

```plot
{"title": "Law of the wall: u+ vs log10(y+)", "xLabel": "log10(y+)", "yLabel": "u+", "xRange": [0, 3], "yRange": [0, 20], "grid": true, "functions": [{"expr": "2.5*log(exp(log(10)*x)) + 5.0", "label": "log law u+ = (1/k) ln y+ + B", "color": "#2563eb"}]}
```

```python
import numpy as np

# First-cell height for a target y+ on a flat plate
rho, mu, U, L = 1.2, 1.8e-5, 30.0, 1.0
Re_L = rho*U*L/mu
Cf = 0.058*Re_L**-0.2              # turbulent flat-plate estimate
tau_w = 0.5*Cf*rho*U**2
u_tau = np.sqrt(tau_w/rho)
y_target = 1.0                    # y+ = 1
y1 = y_target*mu/(rho*u_tau)
print(f"u_tau={u_tau:.3f} m/s, first cell y={y1*1e6:.1f} um for y+=1")
```

**Next:** marching in time for unsteady CFD.
""",
        ),
        _t(
            "Transient simulation and time integration",
            "12 min",
            r"""
# Transient simulation and time integration

Unsteady flows (vortex shedding, pulsatile flow, combustion) need **time
integration**. The time derivative is discretised by schemes of differing order
and stability:

- **Explicit Euler** — first order, cheap per step, CFL-limited.
- **Implicit (backward) Euler** — first order, unconditionally stable, damps
  oscillations (sometimes too much).
- **Crank-Nicolson** — second order, energy-conserving but can ring.
- **Second-order backward (BDF2)** — the common production default: stable and
  second-order accurate.

For an explicit advective scheme the time step is bounded by the **Courant
number**; even with implicit schemes you keep $\mathrm{CFL}\sim 1$ to resolve the
physics. Vortex shedding sets a natural scale via the **Strouhal number**
$St=fD/U\approx0.2$, fixing how many steps per shedding cycle you need
(typically 20-40).

```mermaid
flowchart LR
  T0["State at t"] --> TI["Time scheme (Euler / CN / BDF2)"]
  TI --> IN["Inner SIMPLE/PISO solve"]
  IN --> T1["State at t + dt"]
  T1 -->|advance| TI
```

```plot
{"title": "Damped oscillation of a monitored signal (transient)", "xLabel": "time (s)", "yLabel": "lift coefficient C_L", "xRange": [0, 10], "yRange": [-1, 1], "grid": true, "functions": [{"expr": "exp(-0.2*x)*cos(3*x)", "label": "C_L(t) settling", "color": "#16a34a"}]}
```

```python
import numpy as np

# Time step from Strouhal target: ~30 steps per shedding cycle
U, D, St = 20.0, 0.05, 0.2
f = St*U/D                         # shedding frequency, Hz
dt = 1.0/(f*30)
print(f"f_shed={f:.1f} Hz, dt={dt*1000:.3f} ms for 30 steps/cycle")
```

**Next:** prove your grasp of the methods.
""",
        ),
        _quiz(),
    ),
)


# ── Computational Fluid Dynamics — Advanced ──────────────────────────────────

_ADVANCED = SeedCourse(
    slug="computational-fluid-dynamics-advanced",
    title="Computational Fluid Dynamics — Advanced",
    description=(
        "State-of-the-art and applied CFD: scale-resolving simulation (LES, DES, "
        "DNS), rigorous verification and validation with grid-convergence index "
        "and uncertainty, the practical end-to-end CFD workflow, high-performance "
        "parallel computing and solver scaling, adjoint-based shape optimisation, "
        "and machine-learning-accelerated CFD. Plots, workflows and runnable code "
        "throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Scale-resolving simulation: LES, DES and DNS",
            "15 min",
            r"""
# Scale-resolving simulation: LES, DES and DNS

RANS models the entire turbulence spectrum; **scale-resolving** methods resolve
part or all of it for higher fidelity. The **Kolmogorov cascade** carries energy
from large eddies to the dissipative microscale $\eta=(\nu^3/\varepsilon)^{1/4}$.

- **DNS** — resolve every scale down to $\eta$. Grid count scales as
  $\sim\mathrm{Re}^{9/4}$ and steps as $\mathrm{Re}^{3/4}$ — research-only.
- **LES** — resolve the large, energy-bearing eddies; model the subgrid scales
  with an **SGS** model (Smagorinsky, WALE, dynamic). Cost dominated by the wall
  layer, so wall-modelled LES (WMLES) is an active field.
- **DES / hybrid RANS-LES** — RANS in attached boundary layers, LES in separated
  regions. Pragmatic for high-Re external aerodynamics.

LES needs a **filter width** $\Delta$ tied to cell size and typically resolves
$\ge 80\%$ of turbulent kinetic energy to be credible.

```mermaid
flowchart TB
  SP["Turbulent energy spectrum"] --> R["RANS: model all scales"]
  SP --> L["LES: resolve large, model subgrid"]
  SP --> D["DNS: resolve all to eta"]
  L --> H["DES/hybrid: RANS wall + LES bulk"]
```

```plot
{"title": "Energy spectrum E(k): inertial -5/3 cascade", "xLabel": "log10(wavenumber k)", "yLabel": "log10 E(k)", "xRange": [0, 4], "yRange": [-8, 0], "grid": true, "functions": [{"expr": "-1.667*x", "label": "E(k) ~ k^(-5/3)", "color": "#2563eb"}]}
```

```python
import numpy as np

# DNS vs LES grid scaling (order of magnitude)
for Re in (1e4, 1e5, 1e6):
    N_dns = Re**2.25
    N_les = Re**1.8              # roughly, wall-resolved LES
    print(f"Re={Re:.0e}: DNS~{N_dns:.1e}, LES~{N_les:.1e} cells")
```

**Next:** trusting the result — verification and validation.
""",
        ),
        _t(
            "Verification, validation and the grid-convergence index",
            "14 min",
            r"""
# Verification, validation and the grid-convergence index

A CFD result is only useful if its **uncertainty** is quantified. Two distinct
activities (ASME V&V 20, AIAA G-077):

- **Verification** — "solving the equations right": code verification (method of
  manufactured solutions) and **solution verification** (discretisation error via
  mesh refinement).
- **Validation** — "solving the right equations": comparing against trusted
  **experimental data** with its own uncertainty.

The **Grid Convergence Index (GCI)** by Roache estimates discretisation
uncertainty from three systematically refined meshes. With refinement ratio
$r=h_{coarse}/h_{fine}$ and observed order $p$, the fine-grid GCI is

$$\mathrm{GCI}_{fine} = \frac{F_s\,|\,\varepsilon\,|}{r^{p}-1},\qquad \varepsilon=\frac{\phi_{fine}-\phi_{med}}{\phi_{fine}},$$

with safety factor $F_s\approx1.25$ for three grids. A small GCI and an observed
order near the scheme's formal order signal a mesh-converged solution.

```plot
{"title": "Quantity of interest converging with mesh refinement", "xLabel": "h^p (representative cell size)", "yLabel": "drag coefficient C_D", "xRange": [0, 1], "yRange": [0.3, 0.45], "grid": true, "functions": [{"expr": "0.32 + 0.1*x", "label": "Richardson extrapolation to h->0", "color": "#2563eb"}]}
```

```python
import numpy as np

# GCI from three grids (fine, medium, coarse)
phi1, phi2, phi3 = 0.322, 0.335, 0.360   # fine, medium, coarse C_D
r = 2.0                                   # refinement ratio
p = np.log((phi3 - phi2)/(phi2 - phi1)) / np.log(r)   # observed order
eps = (phi2 - phi1)/phi1
GCI = 1.25*abs(eps)/(r**p - 1)
print(f"observed order p={p:.2f}, GCI_fine={GCI*100:.2f}%")
```

**Next:** the full end-to-end CFD workflow in practice.
""",
        ),
        _t(
            "The practical CFD workflow end to end",
            "13 min",
            r"""
# The practical CFD workflow end to end

Production CFD is a disciplined pipeline, not a single solve. The standard stages:

1. **Define** the question and the quantity of interest (drag, $\Delta p$, heat
   load) and target accuracy.
2. **Geometry prep / CAD cleanup** — defeature, close gaps, extract the fluid
   volume.
3. **Mesh** — sizing, prism layers for target $y^+$, quality checks.
4. **Physics setup** — fluid properties, turbulence model, BCs, schemes.
5. **Solve** — initialise, ramp, monitor residuals and quantities of interest.
6. **Verify & validate** — mesh independence (GCI), compare to data.
7. **Post-process** — fields, integrals, reports.

A common failure is skipping mesh independence and trusting the first run. Good
practice: monitor a quantity of interest live, not just residuals.

```mermaid
flowchart LR
  Q["Define question + QoI"] --> G["CAD cleanup / fluid volume"]
  G --> M["Mesh + y+ check"]
  M --> P["Physics: model, BCs, schemes"]
  P --> S["Solve + monitor"]
  S --> V["Verify (GCI) + validate"]
  V --> PP["Post-process + report"]
  V -->|not converged| M
```

```plot
{"title": "Live monitor: drag converging while residuals drop", "xLabel": "iteration", "yLabel": "drag coefficient C_D", "xRange": [0, 12], "yRange": [0.2, 0.6], "grid": true, "functions": [{"expr": "0.32 + 0.25*exp(-0.4*x)", "label": "C_D settling to ~0.32", "color": "#16a34a"}]}
```

```python
# A workflow as an ordered checklist a script might enforce
stages = ["define", "cad_cleanup", "mesh", "yplus_check",
          "physics_setup", "solve", "mesh_independence", "validate", "report"]
done = {s: False for s in stages}
def can_run(stage):
    i = stages.index(stage)
    return all(done[s] for s in stages[:i])
print("can run 'solve' before mesh?", can_run("solve"))   # False
```

**Next:** running big cases fast — HPC and parallel scaling.
""",
        ),
        _t(
            "High-performance computing and parallel scaling",
            "13 min",
            r"""
# High-performance computing and parallel scaling

Industrial CFD runs on clusters via **domain decomposition**: the mesh is split
into partitions (one per MPI rank), each solving its subdomain and exchanging
**halo/ghost cell** data at partition boundaries every iteration. Partitioners
(METIS, Scotch) minimise the cut to reduce communication.

Scaling is bounded by **Amdahl's law** for a fixed problem (strong scaling): with
parallel fraction $P$ on $N$ cores the speedup is

$$S(N)=\frac{1}{(1-P)+P/N},$$

so even 95% parallel work caps speedup at 20x. **Weak scaling** (grow the problem
with $N$, Gustafson's law) is the realistic target for CFD: keep cells-per-core
roughly constant (often 50k-200k) and communication overhead stays bounded.

```plot
{"title": "Amdahl's law: speedup vs cores (P = 0.95)", "xLabel": "number of cores N", "yLabel": "speedup S(N)", "xRange": [1, 64], "yRange": [0, 20], "grid": true, "functions": [{"expr": "1/((1-0.95)+0.95/x)", "label": "S = 1/((1-P)+P/N)", "color": "#2563eb"}]}
```

```mermaid
flowchart LR
  MESH["Global mesh"] --> DD["Decompose (METIS/Scotch)"]
  DD --> R0["Rank 0 subdomain"]
  DD --> R1["Rank 1 subdomain"]
  R0 <-->|halo exchange (MPI)| R1
  R0 --> ASM["Solve + reduce"]
  R1 --> ASM
```

```python
import numpy as np

# Pick core count to keep ~100k cells/core, report Amdahl speedup
cells, target_per_core, P = 8_000_000, 100_000, 0.92
N = max(1, cells // target_per_core)
S = 1/((1-P) + P/N)
print(f"{N} cores, ~{cells//N:,} cells/core, Amdahl speedup ~{S:.1f}x")
```

**Next:** automatically improving the design — adjoint optimisation.
""",
        ),
        _t(
            "Adjoint-based shape optimisation",
            "14 min",
            r"""
# Adjoint-based shape optimisation

Beyond evaluating a fixed geometry, CFD can **optimise** it. Minimise an objective
$J$ (drag, pressure loss, flow uniformity) over design variables
$\boldsymbol{\alpha}$ subject to the discrete flow equations
$R(\mathbf{u},\boldsymbol{\alpha})=0$.

A finite-difference gradient costs **one CFD solve per design variable** —
hopeless for thousands of variables. The **adjoint method** instead solves a
single extra **adjoint system**,

$$\left(\frac{\partial R}{\partial \mathbf{u}}\right)^{\!T}\!\psi = \left(\frac{\partial J}{\partial \mathbf{u}}\right)^{\!T},\qquad \frac{dJ}{d\boldsymbol{\alpha}} = \frac{\partial J}{\partial \boldsymbol{\alpha}} - \psi^T\frac{\partial R}{\partial \boldsymbol{\alpha}},$$

giving the **full gradient at a cost almost independent of the number of design
variables**. This makes thousand-parameter aerodynamic and turbomachinery shape
optimisation tractable. **Discrete** vs **continuous** adjoints trade
consistency against derivation effort; gradients drive descent, often with mesh
morphing.

```plot
{"title": "Adjoint optimisation: drag objective convergence", "xLabel": "design iteration", "yLabel": "objective J (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "J ~ exp(-0.4 k)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  PAR["Parametrise shape (alpha)"] --> CFD["Primal CFD solve"]
  CFD --> ADJ["Adjoint solve -> dJ/dalpha"]
  ADJ --> UPD["Update alpha (descent)"]
  UPD --> MORPH["Morph mesh"]
  MORPH --> CFD
```

```python
import numpy as np

# Adjoint-style gradient descent on a quadratic drag surrogate
J  = lambda a: (a - 0.2)**2 + 0.05
dJ = lambda a: 2*(a - 0.2)            # gradient from one adjoint solve
a, lr = 1.0, 0.3
for k in range(8):
    a -= lr*dJ(a)
    print(f"iter {k}: alpha={a:.4f}, J={J(a):.5f}")
```

**Next:** the frontier — machine-learning-accelerated CFD.
""",
        ),
        _t(
            "Machine-learning-accelerated CFD",
            "14 min",
            r"""
# Machine-learning-accelerated CFD

ML is reshaping CFD across the pipeline rather than replacing the solver outright:

- **Surrogate / reduced-order models** — train a model (Gaussian process, POD,
  neural net) on a few CFD runs to predict outputs in milliseconds, enabling
  many-query design and **Bayesian optimisation**.
- **Learned turbulence closures** — data-driven corrections to RANS Reynolds
  stresses (e.g. field-inversion + ML) that improve separated-flow prediction.
- **Physics-Informed Neural Networks (PINNs)** — embed the Navier-Stokes
  **residual** in the loss so the network respects the PDE with few or no labels,

$$\mathcal{L} = \mathcal{L}_{data} + \lambda\,\big\|\,\partial_t\mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} + \nabla p/\rho - \nu\nabla^2\mathbf{u}\,\big\|^2.$$

- **ML super-resolution / corrections** — reconstruct fine fields from coarse
  solves, and **differentiable solvers** enable end-to-end gradient learning.

These cut cost dramatically but demand the same V&V rigour — generalisation
outside the training envelope is the central risk.

```mermaid
flowchart LR
  CFD["High-fidelity CFD data"] --> TR["Train surrogate / PINN / closure"]
  TR --> PR["Fast prediction"]
  PR --> BO["Bayesian optimisation / design sweep"]
  BO --> VV["Verify against CFD (V&V)"]
  VV -->|out of envelope| CFD
```

```plot
{"title": "Surrogate-driven Bayesian optimisation convergence", "xLabel": "evaluation", "yLabel": "best objective found (normalised)", "xRange": [0, 12], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.5*x)", "label": "best-so-far drag", "color": "#16a34a"}]}
```

```python
import numpy as np

# Gaussian-process-style surrogate: fit a few CFD points, predict cheaply
X = np.array([0.0, 0.3, 0.6, 1.0])        # design values sampled by CFD
y = (X - 0.2)**2 + 0.05                    # expensive CFD "drag"
coef = np.polyfit(X, y, 2)                 # cheap quadratic surrogate
a_grid = np.linspace(0, 1, 101)
a_best = a_grid[np.argmin(np.polyval(coef, a_grid))]
print(f"surrogate predicts optimum alpha ~ {a_best:.3f}")
```

**Next:** finish the track — test your mastery.
""",
        ),
        _quiz(),
    ),
)


COMPUTATIONAL_FLUID_DYNAMICS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["COMPUTATIONAL_FLUID_DYNAMICS_COURSES"]
