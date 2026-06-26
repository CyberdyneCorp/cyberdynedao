"""AI-Driven Organic & Biomimetic Shapes track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on generating organic, biomimetic
geometry. Starts from natural form, lattices and biomimicry intuition; moves
through the quantitative tools of implicit/TPMS modelling, voxel fields and the
generative/diffusion models that synthesise 3D form; and ends with optimisation
for lightweight, manufacturable, print-ready parts. Lessons are `text` with
LaTeX, interactive ```plot blocks (scaling, growth, loss and convergence
curves), ```mermaid pipelines/classifications and runnable ```python/```matlab
snippets for SDFs, lattices, diffusion sampling and topology optimisation.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── AI-Driven Organic & Biomimetic Shapes — Basics ───────────────────────────

_BASICS = SeedCourse(
    slug="ai-organic-shapes-basics",
    title="AI-Driven Organic & Biomimetic Shapes — Basics",
    description=(
        "The intuition behind organic and biomimetic design: why nature's "
        "forms — bone, bamboo, leaf veins, shells — are so efficient, and how "
        "engineers borrow them. Covers what biomimicry is, scaling laws and "
        "allometry, cellular materials and lattices, curvature and minimal "
        "surfaces, and how computers represent organic shape. Interactive plots "
        "and classification diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Why nature builds organic shapes",
            "10 min",
            r"""
# Why nature builds organic shapes

Natural structures look **organic** — smooth, branching, porous, curved — because
they are shaped by **selection under constraints**: do the job with the least
material, energy and growth time. A femur is hollow with a spongy interior; a leaf
spreads a vein network to feed every cell; a nautilus grows a logarithmic spiral.
None of these are arbitrary; each is close to an **optimum** for its loads.

Engineering borrows this in two ways: **biomimicry** (copy a working principle,
e.g. the kingfisher beak that inspired the Shinkansen nose) and **bio-inspired
optimisation** (let an algorithm rediscover nature-like form for our loads).

```mermaid
flowchart LR
  NAT["Natural form (bone, leaf, shell)"] --> PRIN["Extract principle"]
  PRIN --> MODEL["Model geometry + loads"]
  MODEL --> OPT["Optimise / generate"]
  OPT --> PART["Engineered organic part"]
```

A recurring theme is **material efficiency**: nature puts material only where
stress flows. Removing under-stressed material from a solid beam barely lowers
its stiffness at first but sharply cuts mass — the basis of lightweighting:

```plot
{"title": "Stiffness retained vs material removed", "xLabel": "fraction of material removed", "yLabel": "relative stiffness", "xRange": [0, 0.8], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-0.5*x^2", "label": "stiffness falls slowly at first", "color": "#16a34a"}]}
```

**Next:** what biomimicry is, and its levels of abstraction.
""",
        ),
        _t(
            "Biomimicry: levels and examples",
            "11 min",
            r"""
# Biomimicry: levels and examples

**Biomimicry** is design inspired by biological strategies. It works at three
levels: copying **form** (shape), **process** (how it is made/works), or **system**
(how parts cooperate). Higher levels transfer more deeply but are harder to
abstract.

```mermaid
flowchart TB
  BIO["Biological model"] --> FORM["Form: shark-skin riblets, gecko adhesion"]
  BIO --> PROC["Process: self-healing, growth, folding"]
  BIO --> SYS["System: termite-mound ventilation, ecosystems"]
  FORM --> ENG["Engineered solution"]
  PROC --> ENG
  SYS --> ENG
```

Classic cases: **shark-skin riblets** reduce turbulent drag; **lotus-leaf**
micro-bumps make surfaces self-cleaning; **honeycomb** cores give panels high
bending stiffness per weight; **bone trabeculae** align with principal stresses
(Wolff's law). The honeycomb is a good number: hexagonal cells maximise enclosed
area per unit wall length, so bending stiffness per mass beats a solid plate as
the panel gets thicker (stiffness scales with thickness cubed, mass only linearly):

```plot
{"title": "Sandwich-panel bending stiffness vs core thickness", "xLabel": "core thickness t (mm)", "yLabel": "relative bending stiffness", "xRange": [1, 20], "yRange": [0, 90], "grid": true, "functions": [{"expr": "0.01*x^3", "label": "stiffness ~ t^3 (mass ~ t)", "color": "#2563eb"}]}
```

The discipline: **abstract** the principle (drag-reducing grooves), don't just
copy the animal. That abstraction is where engineering judgement lives.

**Next:** scaling laws — why size changes everything.
""",
        ),
        _t(
            "Scaling laws and allometry",
            "11 min",
            r"""
# Scaling laws and allometry

Organisms and structures cannot simply be scaled up: as a shape grows by a linear
factor $L$, **area** grows as $L^2$ and **volume (mass)** as $L^3$. Strength
follows cross-sectional area, but weight follows volume — so big things are
**relatively weaker**. This square-cube law explains why an ant lifts many times
its weight while an elephant has thick, pillar-like legs.

Biologists capture such relations with **allometry**, $Y = a\,M^{b}$, a power law
between a trait $Y$ and body mass $M$. Plotted on log axes it is a straight line
of slope $b$. Bone cross-section, metabolic rate ($b\approx 3/4$, Kleiber's law)
and limb thickness all follow allometric scaling.

```mermaid
flowchart LR
  L["Linear size L"] --> A["Area ~ L^2 (strength)"]
  L --> V["Volume ~ L^3 (weight)"]
  A --> R["Stress ~ weight/area ~ L"]
  V --> R
  R --> NEED["Bigger -> stockier to keep stress bounded"]
```

The consequence for design: a part that works at one scale may fail when enlarged,
because self-weight stress rises **linearly with size**:

```plot
{"title": "Self-weight stress vs linear scale (square-cube law)", "xLabel": "scale factor L", "yLabel": "relative self-weight stress", "xRange": [1, 10], "yRange": [0, 11], "grid": true, "functions": [{"expr": "x", "label": "stress ~ weight/area ~ L", "color": "#dc2626"}]}
```

So biomimetic shapes are **size-specific**: copy the principle, then re-tune
proportions for your actual scale and material.

**Next:** cellular materials, lattices and foams.
""",
        ),
        _t(
            "Cellular materials, lattices and foams",
            "12 min",
            r"""
# Cellular materials, lattices and foams

Nature rarely uses solid material; it uses **cellular** material — bone, wood,
cork, sponge — a network of struts or walls with voids. Engineered versions are
**foams** (random cells) and **lattices** (periodic unit cells: BCC, octet-truss,
honeycomb). They trade a little stiffness for a large drop in weight, plus energy
absorption and surface area.

```mermaid
flowchart TB
  SOLID["Solid material"] --> CELL["Introduce voids"]
  CELL --> FOAM["Random foam (stochastic)"]
  CELL --> LAT["Periodic lattice (unit cell)"]
  LAT --> STRUT["Strut: BCC, FCC, octet-truss"]
  LAT --> SURF["Surface: gyroid, Schwarz-P (TPMS)"]
```

The key descriptor is **relative density** $\bar{\rho} = \rho^*/\rho_s$ — the
fraction of space filled with solid. Gibson and Ashby's scaling law links the
foam's modulus to the solid's:

$$\frac{E^*}{E_s} = C\,\bar{\rho}^{\,n},$$

with $n\approx 2$ for bending-dominated cells (most foams) and $n\approx 1$ for
stretching-dominated ones (octet-truss). The exponent is everything: at 20 %
density a stretching lattice is far stiffer than a bending foam.

```plot
{"title": "Gibson-Ashby: relative modulus vs relative density", "xLabel": "relative density rho*/rhos", "yLabel": "relative modulus E*/Es", "xRange": [0.05, 0.6], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "x^2", "label": "bending-dominated (n=2)", "color": "#dc2626"}, {"expr": "0.9*x", "label": "stretching-dominated (n=1)", "color": "#16a34a"}]}
```

Because cellular geometry is hard to machine but easy to 3D print, lattices are
where organic design and additive manufacturing meet.

**Next:** curvature and minimal surfaces — the geometry of smooth form.
""",
        ),
        _t(
            "Curvature and minimal surfaces",
            "11 min",
            r"""
# Curvature and minimal surfaces

Organic shapes are **smooth and curved**, so we describe them with **curvature**.
At a point on a surface there are two **principal curvatures** $\kappa_1,
\kappa_2$. Two combinations matter: the **mean curvature** $H =
\tfrac{1}{2}(\kappa_1+\kappa_2)$ and the **Gaussian curvature** $K =
\kappa_1\kappa_2$. A sphere has $K>0$ (dome), a saddle has $K<0$ (like a Pringle),
a cylinder has $K=0$.

```mermaid
flowchart LR
  PT["Surface point"] --> K1["Principal kappa_1"]
  PT --> K2["Principal kappa_2"]
  K1 --> H["Mean H = (k1+k2)/2"]
  K2 --> H
  K1 --> G["Gaussian K = k1*k2"]
  K2 --> G
  H --> MIN["H = 0 -> minimal surface"]
```

A **minimal surface** has $H=0$ everywhere — it locally minimises area, like a
soap film on a wire loop. **Triply periodic minimal surfaces (TPMS)** such as the
**gyroid** tile space with $H\approx 0$, giving smooth, self-supporting,
double-curved walls that nature favours (butterfly-wing scales, beetle shells).
They have no sharp stress concentrations, which is mechanically excellent.

For a simple curved profile, curvature peaks where the shape bends hardest. For a
parabola $y=x^2$ the curvature is $\kappa = 2/(1+4x^2)^{3/2}$, largest at the
vertex:

```plot
{"title": "Curvature of a parabola y = x^2", "xLabel": "x", "yLabel": "curvature kappa", "xRange": [-2, 2], "yRange": [0, 2.2], "grid": true, "functions": [{"expr": "2/(1+4*x^2)^1.5", "label": "kappa peaks at the vertex", "color": "#2563eb"}]}
```

Curvature also bounds **stress concentration**: sharp corners (high $\kappa$)
concentrate stress, smooth fillets spread it — why organic forms rarely have sharp
internal angles.

**Next:** how computers represent organic shape.
""",
        ),
        _t(
            "How computers represent organic shape",
            "11 min",
            r"""
# How computers represent organic shape

To generate organic form a computer needs a representation. The main families:

```mermaid
flowchart TB
  REP["Shape representation"] --> MESH["Boundary mesh (triangles, STL)"]
  REP --> BREP["Parametric B-rep / NURBS (CAD)"]
  REP --> VOX["Voxels (3D grid of cells)"]
  REP --> SDF["Implicit field / signed distance (SDF)"]
  SDF --> ISO["Marching cubes -> mesh"]
  VOX --> ISO
```

- **Meshes** store the surface as triangles — universal for printing (STL) but
  awkward to edit organically.
- **NURBS/B-rep** are smooth and exact but struggle with very complex topology
  (thousands of holes).
- **Voxels** fill space with a grid — natural for lattices and field data, but
  memory grows as $n^3$.
- **Implicit / signed distance fields (SDF)** store, at each point, the signed
  distance to the surface ($f<0$ inside, $f=0$ on it). They make blending,
  offsetting and booleans trivial — ideal for organic, branching geometry.

A sphere SDF is just $f(\mathbf{p}) = \lVert\mathbf{p}\rVert - r$. Smoothly
**blending** two SDFs gives the rounded, fused junctions that look biological:

```python
import numpy as np

def sphere_sdf(p, center, r):
    return np.linalg.norm(p - center, axis=-1) - r

def smooth_union(d1, d2, k=0.5):
    # Polynomial smooth-min: blends two fields into one organic surface.
    h = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0)
    return d2 * (1 - h) + d1 * h - k * h * (1 - h)

# Two overlapping blobs fuse with a smooth, fillet-like neck:
grid = np.stack(np.meshgrid(*[np.linspace(-2, 2, 64)] * 3, indexing="ij"), -1)
a = sphere_sdf(grid, np.array([-0.6, 0, 0]), 1.0)
b = sphere_sdf(grid, np.array([0.6, 0, 0]), 1.0)
field = smooth_union(a, b, k=0.4)      # field <= 0 marks the solid
```

Memory cost is why naive voxel grids do not scale — doubling resolution multiplies
storage eightfold:

```plot
{"title": "Voxel-grid memory vs resolution", "xLabel": "grid resolution n (per axis, x10)", "yLabel": "relative memory", "xRange": [1, 10], "yRange": [0, 1100], "grid": true, "functions": [{"expr": "x^3", "label": "memory ~ n^3", "color": "#dc2626"}]}
```

**Next:** quick knowledge check on organic-shape fundamentals.
""",
        ),
        _quiz(),
    ),
)


# ── AI-Driven Organic & Biomimetic Shapes — Intermediate ─────────────────────

_INTERMEDIATE = SeedCourse(
    slug="ai-organic-shapes-intermediate",
    title="AI-Driven Organic & Biomimetic Shapes — Intermediate",
    description=(
        "The core quantitative methods for generating organic geometry. Covers "
        "signed distance fields and constructive modelling, TPMS and lattice "
        "mathematics, procedural growth (L-systems, reaction-diffusion, "
        "space colonisation), marching cubes and mesh extraction, and an "
        "introduction to learned shape representations. Plots, pipeline "
        "diagrams and Python/MATLAB code throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Signed distance fields and implicit modelling",
            "12 min",
            r"""
# Signed distance fields and implicit modelling

A **signed distance field (SDF)** assigns every point in space the signed distance
to a surface: $f(\mathbf{p}) < 0$ inside, $>0$ outside, $=0$ on the surface. This
implicit representation makes organic operations algebraic. **Booleans** are
min/max:

$$f_{\cup} = \min(f_1,f_2),\quad f_{\cap}=\max(f_1,f_2),\quad f_{-}=\max(f_1,-f_2),$$

and an **offset** (thickening a shell) is just $f \mapsto f - t$. The magic for
organic form is the **smooth minimum**, which replaces sharp boolean seams with
fillets.

```mermaid
flowchart LR
  PRIM["Primitive SDFs (sphere, box, torus)"] --> OPS["Ops: smooth union / subtract / offset"]
  OPS --> FIELD["Combined scalar field f(p)"]
  FIELD --> ISO["Isosurface f = 0"]
  ISO --> MESH["Marching cubes -> printable mesh"]
```

A property worth knowing: a **true** SDF satisfies the **eikonal equation**
$\lVert\nabla f\rVert = 1$, so the gradient gives the exact surface normal — handy
for shading, offsetting and ray-marching. Booleans via min/max can break this, so
fields are sometimes re-distanced.

```python
import numpy as np

def box_sdf(p, half):
    q = np.abs(p) - half
    return (np.linalg.norm(np.maximum(q, 0.0), axis=-1)
            + np.minimum(np.max(q, axis=-1), 0.0))

def smin(a, b, k=0.3):                 # smooth minimum (exponential form)
    return -np.log(np.exp(-k * a) + np.exp(-k * b)) / k

def normal(field_fn, p, eps=1e-3):     # gradient ~ surface normal
    g = np.array([
        field_fn(p + d) - field_fn(p - d)
        for d in (np.array([eps,0,0]), np.array([0,eps,0]), np.array([0,0,eps]))
    ])
    return g / (np.linalg.norm(g) + 1e-9)
```

The smooth-union **blend radius** $k$ controls how organic the junction looks:
small $k$ keeps a sharp seam, large $k$ swells a generous fillet (and adds
material), so it trades aesthetics against mass:

```plot
{"title": "Blend fillet radius vs smoothing parameter k", "xLabel": "smoothing k", "yLabel": "effective fillet radius (mm)", "xRange": [0.1, 4], "yRange": [0, 5], "grid": true, "functions": [{"expr": "1.2*sqrt(x)", "label": "larger k -> rounder, heavier junction", "color": "#2563eb"}]}
```

**Next:** the mathematics of TPMS and lattices.
""",
        ),
        _t(
            "TPMS and lattice mathematics",
            "13 min",
            r"""
# TPMS and lattice mathematics

**Triply periodic minimal surfaces (TPMS)** are defined by a single implicit
equation, making them ideal for parametric organic infill. The **gyroid**,
**Schwarz-P** and **diamond** approximations are:

$$\text{gyroid: } \sin x\cos y+\sin y\cos z+\sin z\cos x = c,$$
$$\text{Schwarz-P: } \cos x+\cos y+\cos z = c,$$

where the arguments are scaled by $2\pi/a$ for cell size $a$, and the level $c$
(or a thickness offset) sets the **relative density**. Thresholding the field at
$|f|<t$ produces a **sheet** TPMS (a double-walled shell); thresholding $f<c$
gives a **solid-network** TPMS.

```mermaid
flowchart TB
  EQ["Implicit TPMS equation f(x,y,z)"] --> SCALE["Scale by 2*pi/a (cell size)"]
  SCALE --> LVL["Choose level c / thickness t"]
  LVL --> DENS["Sets relative density"]
  DENS --> SAMPLE["Sample on voxel grid"]
  SAMPLE --> MC["Marching cubes -> mesh"]
```

TPMS are attractive because they are **smooth, self-supporting** (good for
printing) and have **near-zero mean curvature**, so no stress raisers. Their
stiffness follows Gibson-Ashby scaling; gyroids behave close to
bending-dominated, $E^*/E_s \propto \bar{\rho}^{\,2}$.

```python
import numpy as np

def gyroid_field(x, y, z, a=10.0):
    k = 2 * np.pi / a
    return (np.sin(k*x)*np.cos(k*y)
            + np.sin(k*y)*np.cos(k*z)
            + np.sin(k*z)*np.cos(k*x))

n = 80
g = np.linspace(0, 30, n)
X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
f = gyroid_field(X, Y, Z, a=10.0)
t = 0.6                                 # sheet thickness offset
sheet = np.abs(f) < t                   # double-walled gyroid sheet
print("relative density:", round(sheet.mean(), 3))
```

You can **grade** a lattice by making the cell size $a$ or thickness $t$ vary with
position — denser where stress is high — mimicking bone. Density scales roughly
linearly with the thickness offset over the useful range:

```plot
{"title": "Gyroid relative density vs thickness offset", "xLabel": "thickness offset t", "yLabel": "relative density", "xRange": [0.1, 1.6], "yRange": [0, 0.6], "grid": true, "functions": [{"expr": "0.33*x", "label": "thicker walls -> denser, stiffer", "color": "#16a34a"}]}
```

**Next:** procedural growth models for branching, natural form.
""",
        ),
        _t(
            "Procedural growth: L-systems and reaction-diffusion",
            "13 min",
            r"""
# Procedural growth: L-systems and reaction-diffusion

Some organic structure is best **grown** by rules rather than carved by fields.
Three classics:

- **L-systems**: grammar rewriting that grows plants, trees and vasculature. A
  string of symbols is rewritten each step, then interpreted as turtle graphics.
- **Space colonisation**: branches grow toward scattered attractor points —
  excellent for leaf venation and lung-like networks.
- **Reaction-diffusion (Turing patterns)**: two chemicals diffuse and react to
  form spots and stripes (animal coats, coral).

```mermaid
flowchart LR
  AX["Axiom / seed"] --> RULE["Apply production rules"]
  RULE --> ITER{"Iterate n times?"}
  ITER -- yes --> RULE
  ITER -- no --> INTERP["Interpret as geometry (turtle / branches)"]
  INTERP --> ORG["Organic branching structure"]
```

A Gray-Scott reaction-diffusion step produces Turing patterns from noise:

$$\frac{\partial u}{\partial t}=D_u\nabla^2u-uv^2+F(1-u),\quad
\frac{\partial v}{\partial t}=D_v\nabla^2v+uv^2-(F+k)v.$$

```python
import numpy as np
from scipy.ndimage import laplace

def gray_scott(u, v, Du=0.16, Dv=0.08, F=0.060, k=0.062, steps=2000):
    for _ in range(steps):
        uvv = u * v * v
        u += Du * laplace(u) - uvv + F * (1 - u)
        v += Dv * laplace(v) + uvv - (F + k) * v
    return u, v                          # threshold v -> organic spot/stripe mask
```

Branching networks obey **Murray's law**: at a bifurcation the parent radius
cubes equal the sum of daughter cubes, $r_0^3 = r_1^3 + r_2^3$, minimising
pumping cost. The daughter-to-parent radius ratio for a symmetric split is
$2^{-1/3}\approx 0.794$, and branch radius shrinks geometrically with generation:

```plot
{"title": "Murray's law: vessel radius vs branch generation", "xLabel": "branch generation", "yLabel": "relative radius", "xRange": [0, 8], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "0.794^x", "label": "r ~ 2^(-n/3) per symmetric split", "color": "#2563eb"}]}
```

**Next:** turning fields into printable meshes with marching cubes.
""",
        ),
        _t(
            "Marching cubes and mesh extraction",
            "12 min",
            r"""
# Marching cubes and mesh extraction

Implicit fields and voxel data must become a **boundary mesh** to be printed. The
standard algorithm is **marching cubes**: march a cube through the voxel grid,
classify its 8 corners as inside/outside the isolevel, look up the resulting
triangle pattern (256 cases reduced to 15 by symmetry), and place vertices on
edges by **linear interpolation** of the field.

```mermaid
flowchart LR
  FIELD["Scalar field on voxel grid"] --> CELL["For each cube of 8 corners"]
  CELL --> CLASS["Classify corners vs isolevel -> 8-bit index"]
  CLASS --> LUT["Edge table + triangle table lookup"]
  LUT --> INTERP["Interpolate vertex on each crossed edge"]
  INTERP --> TRI["Emit triangles -> watertight mesh"]
```

Edge interpolation places the vertex where the field equals the isolevel $c$
between corner values $f_a,f_b$:

$$t = \frac{c - f_a}{f_b - f_a},\qquad \mathbf{v} = \mathbf{p}_a + t(\mathbf{p}_b-\mathbf{p}_a).$$

```python
import numpy as np
from skimage.measure import marching_cubes

def field_to_mesh(field, isolevel=0.0, spacing=(0.5, 0.5, 0.5)):
    # Extract a watertight triangle mesh from a 3D scalar field.
    verts, faces, normals, _ = marching_cubes(field, level=isolevel, spacing=spacing)
    return verts, faces, normals

# Mesh complexity grows with resolution; triangle count tracks surface area / h^2
```

Mesh **resolution** trades fidelity for size: the triangle count scales with
surface area divided by the squared voxel spacing $h$, so halving $h$ roughly
quadruples triangles. **Dual contouring** is an alternative that preserves sharp
edges using the field gradient (Hermite data), useful when organic forms meet flat
machined faces.

```plot
{"title": "Marching-cubes triangle count vs voxel spacing", "xLabel": "voxel spacing h (mm)", "yLabel": "relative triangle count", "xRange": [0.2, 2], "yRange": [0, 30], "grid": true, "functions": [{"expr": "1/x^2", "label": "triangles ~ area / h^2", "color": "#dc2626"}]}
```

**Next:** learned shape representations — neural fields and latent spaces.
""",
        ),
        _t(
            "Learned shape representations",
            "13 min",
            r"""
# Learned shape representations

To let AI *generate* shape, we need representations a neural network can produce.
The modern answer is **neural implicit fields**: a small MLP $f_\theta(\mathbf{p})$
that outputs an occupancy or signed distance at any point $\mathbf{p}$, optionally
conditioned on a **latent code** $\mathbf{z}$ describing the shape.

```mermaid
flowchart LR
  Z["Latent code z"] --> NET["MLP f_theta(p, z)"]
  P["Query point p"] --> NET
  NET --> SDF["Predicted SDF / occupancy"]
  SDF --> MC["Marching cubes -> mesh"]
  SHAPES["Dataset of shapes"] --> TRAIN["Train: fit SDF + learn latent space"]
  TRAIN --> Z
```

**DeepSDF** trains one network over a whole class of shapes, giving each a latent
$\mathbf{z}$; interpolating between two codes **morphs** smoothly between shapes —
the start of generative design. **Occupancy networks** predict inside/outside
instead of distance. The training loss is a clamped L1 on SDF samples:

$$\mathcal{L} = \sum_i \big| \,\text{clamp}(f_\theta(\mathbf{p}_i,\mathbf{z}),\delta) - \text{clamp}(s_i,\delta)\,\big| .$$

```python
import torch, torch.nn as nn

class DeepSDF(nn.Module):
    def __init__(self, latent=64, width=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent + 3, width), nn.ReLU(),
            nn.Linear(width, width), nn.ReLU(),
            nn.Linear(width, 1), nn.Tanh(),         # signed distance (scaled)
        )

    def forward(self, z, p):                          # z:(B,latent) p:(B,3)
        return self.net(torch.cat([z, p], dim=-1)).squeeze(-1)
```

Such networks are **resolution-free** (query any point) and compact, and their
training loss falls steeply then plateaus as the latent space captures the shape
family:

```plot
{"title": "Neural-SDF reconstruction loss vs training epoch", "xLabel": "epoch (x10)", "yLabel": "reconstruction loss", "xRange": [0, 20], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.3*x)+0.05", "label": "loss decreases toward a floor", "color": "#16a34a"}]}
```

These latent shape spaces are exactly what generative and diffusion models sample
from — the subject of the Advanced course.

**Next:** quick knowledge check on quantitative organic-shape methods.
""",
        ),
        _quiz(),
    ),
)


# ── AI-Driven Organic & Biomimetic Shapes — Advanced ─────────────────────────

_ADVANCED = SeedCourse(
    slug="ai-organic-shapes-advanced",
    title="AI-Driven Organic & Biomimetic Shapes — Advanced",
    description=(
        "State-of-the-art and applied generative design for manufacturable "
        "organic parts. Covers generative models for 3D form (VAEs/GANs), "
        "diffusion models on shapes, topology optimisation and generative "
        "design, manufacturability and print-readiness constraints, and an "
        "end-to-end pipeline from prompt to printed lightweight part. Plots, "
        "workflow diagrams and Python/MATLAB optimisation code throughout."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Generative models for 3D form",
            "13 min",
            r"""
# Generative models for 3D form

A **generative model** learns a distribution over shapes so it can synthesise new
ones. The main families applied to 3D:

```mermaid
flowchart TB
  GEN["Generative models for 3D"] --> VAE["VAE: encode -> latent -> decode"]
  GEN --> GAN["GAN: generator vs discriminator"]
  GEN --> AR["Autoregressive (voxel/mesh tokens)"]
  GEN --> DIFF["Diffusion (denoise from noise)"]
  VAE --> LAT["Sample latent z -> decode to SDF/voxel"]
  GAN --> LAT
```

A **variational autoencoder (VAE)** encodes a shape to a latent $\mathbf{z}$,
regularised toward a Gaussian, then decodes back; you generate by sampling
$\mathbf{z}\sim\mathcal{N}(0,I)$. Its loss balances reconstruction against a **KL**
term:

$$\mathcal{L} = \underbrace{\mathbb{E}\,\lVert \hat{x}-x\rVert^2}_{\text{reconstruction}} + \beta\,\underbrace{D_{KL}\!\big(q(z\mid x)\,\Vert\,p(z)\big)}_{\text{regularisation}}.$$

A **GAN** instead trains a generator against a discriminator (3D-GAN over voxels);
it produces sharp shapes but can suffer **mode collapse**. Operating on a *latent*
SDF (rather than raw voxels) keeps memory tractable.

```python
import torch, torch.nn.functional as F

def vae_loss(x_hat, x, mu, logvar, beta=1.0):
    recon = F.mse_loss(x_hat, x, reduction="sum")
    kld = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + beta * kld

def sample_shape(decoder, latent_dim, n=1):
    z = torch.randn(n, latent_dim)        # sample prior -> new organic shape
    return decoder(z)                     # -> SDF / voxel grid
```

The **$\beta$** knob trades reconstruction fidelity against a smoother, more
disentangled latent space — too high and detail blurs, too low and sampling gives
artefacts:

```plot
{"title": "VAE trade-off: reconstruction error vs beta", "xLabel": "KL weight beta", "yLabel": "reconstruction error", "xRange": [0.1, 8], "yRange": [0, 6], "grid": true, "functions": [{"expr": "0.6*x+0.4", "label": "higher beta -> smoother latent, blurrier shapes", "color": "#dc2626"}]}
```

**Next:** diffusion models, today's strongest 3D generators.
""",
        ),
        _t(
            "Diffusion models for shape synthesis",
            "14 min",
            r"""
# Diffusion models for shape synthesis

**Diffusion models** are the state of the art for generative shape. They learn to
**reverse a noising process**: a forward chain gradually corrupts a shape (in
voxel, point-cloud or latent-SDF form) into Gaussian noise; a network learns to
**denoise** step by step, so sampling starts from pure noise and walks back to a
clean shape.

The forward step adds noise with a schedule $\beta_t$:

$$x_t = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon,\quad \bar{\alpha}_t=\prod_{s\le t}(1-\beta_s),$$

and the network $\epsilon_\theta(x_t,t)$ is trained to predict the noise, with loss
$\mathcal{L}=\mathbb{E}\,\lVert\epsilon-\epsilon_\theta(x_t,t)\rVert^2$. **Latent
diffusion** runs this inside a VAE's latent space (as in modern 3D systems and
Shap-E / point-cloud diffusion), and **conditioning** on a text or image embedding
gives prompt-driven generation.

```mermaid
flowchart LR
  X0["Clean shape x0"] --> FWD["Forward: add noise (beta_t schedule)"]
  FWD --> XT["Noisy x_T ~ N(0, I)"]
  XT --> REV["Reverse: denoise eps_theta(x_t, t)"]
  COND["Text / image condition"] --> REV
  REV --> GEN["Generated organic shape"]
```

```python
import torch

def ddpm_sample(model, shape, betas, cond=None):
    alphas = 1.0 - betas
    abar = torch.cumprod(alphas, dim=0)
    x = torch.randn(shape)                          # start from pure noise
    for t in reversed(range(len(betas))):
        eps = model(x, t, cond)                     # predicted noise
        a, ab = alphas[t], abar[t]
        mean = (x - betas[t] / torch.sqrt(1 - ab) * eps) / torch.sqrt(a)
        x = mean + (torch.sqrt(betas[t]) * torch.randn_like(x) if t > 0 else 0)
    return x                                        # -> latent / voxel shape
```

Sample quality (e.g. measured by a shape FID) **improves with the number of
denoising steps** but with diminishing returns, so practitioners trade steps for
speed:

```plot
{"title": "Generation quality vs denoising steps", "xLabel": "denoising steps (x100)", "yLabel": "sample quality (1 - normalized FID)", "xRange": [0, 10], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "1-exp(-0.5*x)", "label": "diminishing returns past ~few hundred steps", "color": "#16a34a"}]}
```

The output is rarely print-ready: it must be meshed, repaired and constrained —
the next lessons.

**Next:** topology optimisation and generative design.
""",
        ),
        _t(
            "Topology optimisation and generative design",
            "13 min",
            r"""
# Topology optimisation and generative design

Where diffusion models learn shape from data, **topology optimisation (TO)** and
**generative design** *derive* organic shape from physics: find the material
layout that minimises **compliance** (maximises stiffness) for a mass budget.
The result is the bone-like, branching geometry AM loves. The **SIMP** method
gives each element a density $x_e\in[0,1]$ with penalised stiffness:

$$E_e(x_e)=E_{min}+x_e^{\,p}(E_0-E_{min}),\quad p\approx 3,$$

minimising $c=\mathbf{U}^\top\mathbf{K}\mathbf{U}$ s.t. $\sum x_e v_e\le V^*$.
**Generative design** wraps many such solves (varied loads, seeds, even different
synthesis methods) and presents a Pareto set of candidates.

```mermaid
flowchart LR
  INIT["Initialise densities x_e"] --> FEA["FE solve K U = F"]
  FEA --> SENS["Compliance + sensitivities dc/dx"]
  SENS --> FILT["Density filter (avoid checkerboard)"]
  FILT --> UPD["Optimality-criteria update"]
  UPD --> CONV{"Converged?"}
  CONV -- no --> FEA
  CONV -- yes --> ORG["Organic, minimal-mass layout"]
```

```python
import numpy as np

def oc_update(x, dc, volfrac, move=0.2):
    # Optimality-criteria density update for SIMP topology optimisation.
    l1, l2 = 1e-9, 1e9
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l1 + l2)
        xnew = np.clip(x * np.sqrt(-dc / lmid), x - move, x + move)
        xnew = np.clip(xnew, 0.0, 1.0)
        l1, l2 = (lmid, l2) if xnew.mean() > volfrac else (l1, lmid)
    return xnew
```

Compliance falls steeply over iterations toward a stiff optimum:

```plot
{"title": "Topology-optimisation convergence", "xLabel": "iteration", "yLabel": "normalized compliance", "xRange": [0, 25], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "exp(-0.4*x)+0.15", "label": "compliance decreases to optimum", "color": "#16a34a"}]}
```

Modern practice blends both worlds: TO for the load-bearing skeleton, learned
generative priors or lattices for infill, all under **AM-aware** filters
(overhang, minimum member size) so the output prints.

**Next:** making generated organic shapes manufacturable.
""",
        ),
        _t(
            "Manufacturability and print-readiness",
            "12 min",
            r"""
# Manufacturability and print-readiness

A beautiful generated shape is worthless if it cannot be built. Turning organic
geometry **print-ready** means enforcing process constraints and repairing the
mesh:

```mermaid
flowchart TB
  GEN["Generated / optimised shape"] --> REPAIR["Repair: watertight, fix normals, remove non-manifold"]
  REPAIR --> CONSTR["Apply DfAM constraints"]
  CONSTR --> OVER["Overhang < critical angle?"]
  CONSTR --> WALL["Min wall / member size?"]
  CONSTR --> TRAP["Trapped powder / escape holes?"]
  OVER --> ORIENT["Optimise build orientation"]
  WALL --> ORIENT
  TRAP --> ORIENT
  ORIENT --> READY["Print-ready build"]
```

Key checks: **minimum wall** (~0.4-1.0 mm), the **overhang rule** (surfaces
steeper than the critical angle, often ~45 deg from horizontal, are
self-supporting), **escape holes** for trapped powder/resin in internal lattices,
and **build-orientation** choice, which trades support volume against strength
anisotropy and surface finish. A per-facet overhang test:

```python
import numpy as np

def needs_support(normals, build_dir=(0, 0, 1), crit_deg=45.0):
    # Flag down-facing facets steeper than the critical overhang angle.
    b = np.asarray(build_dir, float)
    n = normals / np.linalg.norm(normals, axis=1, keepdims=True)
    down = n @ (-b)
    angle_from_horiz = np.degrees(np.arcsin(np.clip(down, -1, 1)))
    return angle_from_horiz > (90.0 - crit_deg)

def support_fraction(normals, **kw):
    return float(needs_support(normals, **kw).mean())
```

The orientation choice is a real optimisation: supported area (hence post-processing
cost) varies strongly with tilt, with a clear minimum away from the worst angle:

```plot
{"title": "Support volume vs build-orientation tilt", "xLabel": "tilt angle (rad)", "yLabel": "relative support volume", "xRange": [0.05, 1.5], "yRange": [0, 8], "grid": true, "functions": [{"expr": "1/sin(x)", "label": "flat overhangs need the most support", "color": "#dc2626"}]}
```

TPMS infill helps here: it is **self-supporting** and self-draining, so organic
lattices often need no internal supports at all.

**Next:** an end-to-end prompt-to-part pipeline.
""",
        ),
        _t(
            "End-to-end pipeline: prompt to printed part",
            "13 min",
            r"""
# End-to-end pipeline: prompt to printed part

Putting it together: a modern organic-design workflow chains a **generative
model**, **physics-based optimisation**, **lattice infill**, **manufacturability
checks** and **slicing** into one loop — increasingly with a human or AI agent in
the loop selecting candidates.

```mermaid
flowchart LR
  PROMPT["Prompt / requirements + loads"] --> GEN["Generative model (diffusion) -> candidate forms"]
  GEN --> TO["Topology optimisation under loads"]
  TO --> LAT["Graded TPMS / lattice infill"]
  LAT --> CHK["Manufacturability + simulation check"]
  CHK -- fail --> GEN
  CHK -- pass --> SLICE["Orient + slice -> G-code"]
  SLICE --> PRINT["Print + post-process"]
```

The loop is a constrained optimisation: maximise stiffness-to-weight subject to
print constraints and a performance target. A simple driver that scores candidates
and keeps improving:

```python
import numpy as np

def evaluate(shape):
    # Toy objective: stiffness-to-mass, penalised by unsupported overhang area.
    stiffness = simulate_stiffness(shape)      # FE surrogate
    mass = shape.relative_density
    penalty = 5.0 * support_fraction(shape.normals)
    return stiffness / mass - penalty          # higher is better

def design_loop(generator, n_iter=30):
    best, best_score = None, -np.inf
    for i in range(n_iter):
        cand = generator.sample()              # diffusion / VAE proposal
        cand = topology_refine(cand)           # physics step
        cand = add_graded_lattice(cand)        # organic infill
        s = evaluate(cand)
        if s > best_score:
            best, best_score = cand, s
    return best, best_score
```

Across iterations the best score climbs and saturates as the design approaches a
manufacturable, lightweight optimum:

```plot
{"title": "Best design score vs pipeline iteration", "xLabel": "iteration", "yLabel": "stiffness-to-mass score (normalized)", "xRange": [0, 30], "yRange": [0, 1.1], "grid": true, "functions": [{"expr": "1-exp(-0.18*x)", "label": "convergence to a print-ready optimum", "color": "#16a34a"}]}
```

The frontier: **multi-physics** objectives (stiffness + thermal + flow),
**differentiable** pipelines that backprop manufacturing cost into the generator,
and **agentic** design exploration — but the human still owns requirements,
validation and sign-off.

**Next:** final knowledge check across generative, optimisation and DfAM topics.
""",
        ),
        _quiz(),
    ),
)


AI_ORGANIC_SHAPES_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["AI_ORGANIC_SHAPES_COURSES"]
