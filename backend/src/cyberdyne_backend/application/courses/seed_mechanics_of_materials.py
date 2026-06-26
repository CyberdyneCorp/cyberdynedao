"""Mechanics of Materials track: Basics -> Intermediate -> Advanced.

A three-level mechanical-engineering track on how solids carry load. Starts from
stress, strain and Hooke's law, builds through axial loading, torsion and the
bending of beams, then reaches deflection, combined loading, column buckling,
failure theories, fatigue and FEM/optimization. Lessons are `text` with LaTeX,
interactive ```plot blocks (stress-strain, deflection, buckling, S-N, FRF),
```mermaid design/classification diagrams and runnable ```python/```matlab code.
"""

# Lesson prose uses typographic characters (×, →, ≈, σ, ε, τ, μ, …) and LaTeX —
# exempt this content file from the ambiguous-character lints.
# ruff: noqa: RUF001, RUF003
from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _quiz() -> SeedLesson:
    return SeedLesson(title="Check your knowledge", lesson_type="quiz", duration="4 min")


# ── Mechanics of Materials — Basics ──────────────────────────────────────────

_BASICS = SeedCourse(
    slug="mechanics-of-materials-basics",
    title="Mechanics of Materials — Basics",
    description=(
        "The intuition and fundamentals of how solid bodies respond to load: "
        "normal and shear stress, normal and shear strain, the stress-strain "
        "curve and Hooke's law, Poisson's ratio and the elastic constants, and "
        "the design quantities of factor of safety and allowable stress. "
        "Interactive plots and diagrams throughout."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Normal and shear stress",
            "10 min",
            r"""
# Normal and shear stress

**Stress** measures how hard the internal material is pushed at a point: force
per unit area, in pascals ($1\,\text{Pa}=1\,\text{N/m}^2$; engineering usually
works in MPa). Cut a loaded member and look at the internal force on the exposed
face. The component **perpendicular** to the face is **normal stress**:

$$\sigma = \frac{N}{A},$$

tensile when it pulls the face outward, compressive when it pushes in. The
component **tangent** to the face is **shear stress**:

$$\tau = \frac{V}{A}.$$

For a bar of cross-section $A$ pulled by an axial force $N$, the average normal
stress is uniform across the section. Larger force or smaller area means more
stress — and stress, not force, is what the material actually "feels":

```plot
{"title": "Axial stress vs applied force (A = 100 mm^2)", "xLabel": "axial force N (kN)", "yLabel": "stress sigma (MPa)", "xRange": [0, 50], "yRange": [0, 500], "grid": true, "functions": [{"expr": "10*x", "label": "sigma = N/A", "color": "#2563eb"}]}
```

Stress is a *property of a point and a plane*: rotate the cut and the split
between normal and shear changes, even though the load is unchanged. That idea
matures later into the stress tensor and Mohr's circle.

```mermaid
flowchart LR
  L["External load"] --> C["Imaginary cut"]
  C --> N["Normal component -> sigma = N/A"]
  C --> S["Tangential component -> tau = V/A"]
```

**Next:** how the material deforms — normal and shear strain.
""",
        ),
        _t(
            "Normal and shear strain",
            "10 min",
            r"""
# Normal and shear strain

Stress has a partner: **strain**, the geometric measure of deformation.
**Normal strain** is the fractional change in length of a fibre,

$$\varepsilon = \frac{\delta}{L_0} = \frac{L - L_0}{L_0},$$

dimensionless (often quoted in microstrain, $1\,\mu\varepsilon = 10^{-6}$). A bar
that stretches $\delta$ over original length $L_0$ has uniform axial strain
$\varepsilon$. **Shear strain** $\gamma$ measures angular distortion: the change
(in radians) of an originally right angle between two fibres.

```plot
{"title": "Elongation vs strain for L0 = 2 m", "xLabel": "strain epsilon (-)", "yLabel": "elongation delta (mm)", "xRange": [0, 0.01], "yRange": [0, 20], "grid": true, "functions": [{"expr": "2000*x", "label": "delta = epsilon * L0", "color": "#16a34a"}]}
```

Two distinctions matter. **Engineering strain** uses the original length $L_0$;
**true strain** $\varepsilon_t=\ln(L/L_0)$ uses the current length and is used for
large plastic deformation. And strain is *local*: in a tapered or non-uniform bar
it varies along the length, so we integrate $\delta=\int \varepsilon\,dx$ rather
than multiply.

```mermaid
flowchart LR
  D["Deformation"] --> A["Length change -> normal strain epsilon"]
  D --> B["Angle change -> shear strain gamma"]
  A --> M["Material law links stress and strain"]
  B --> M
```

Stress and strain are linked by the material's constitutive law — next.

**Next:** the stress-strain curve that every material has.
""",
        ),
        _t(
            "The stress-strain curve",
            "12 min",
            r"""
# The stress-strain curve

Pull a standard specimen in a tension test and plot $\sigma$ against
$\varepsilon$ — the **stress-strain curve**, a fingerprint of the material. For a
ductile metal like mild steel it has clear regions: an initial **linear-elastic**
line, a **yield** point, a **strain-hardening** rise to the **ultimate tensile
strength** $\sigma_u$, then necking and **fracture**.

```plot
{"title": "Stress-strain curve (ductile metal)", "xLabel": "strain epsilon (-)", "yLabel": "stress sigma (MPa)", "xRange": [0, 0.06], "yRange": [0, 450], "grid": true, "functions": [{"expr": "200000*x", "label": "elastic: sigma = E*epsilon", "color": "#2563eb"}, {"expr": "250 + 3000*x", "label": "plastic / hardening", "color": "#dc2626"}]}
```

Key landmarks read off the curve:

- **Proportional / elastic limit** — end of recoverable, linear behaviour.
- **Yield strength $\sigma_y$** — onset of permanent (plastic) deformation; for
  metals without a sharp knee, the **0.2 % offset** method defines it.
- **Ultimate strength $\sigma_u$** — the peak stress.
- **Ductility** — total elongation or % reduction of area at fracture.

Brittle materials (cast iron, ceramics, concrete) have almost no plastic region
and fracture near the elastic limit. The **area under the curve** is the energy
absorbed per unit volume — small for brittle, large for tough materials. ASTM E8
standardises the metallic tension test.

**Next:** the elastic part written as a law — Hooke's law and stiffness $E$.
""",
        ),
        _t(
            "Hooke's law and Young's modulus",
            "11 min",
            r"""
# Hooke's law and Young's modulus

In the linear-elastic region stress is proportional to strain — **Hooke's law**:

$$\sigma = E\,\varepsilon.$$

The constant $E$ is **Young's modulus** (the elastic modulus), the *stiffness*
of the material: the slope of the elastic line on the stress-strain curve. It has
units of stress (GPa) because strain is dimensionless. Steel $E\approx 200$ GPa,
aluminium $\approx 70$ GPa, concrete $\approx 30$ GPa — steel is about three
times stiffer than aluminium for the same geometry.

```plot
{"title": "Hooke's law: stiffer materials have steeper lines", "xLabel": "strain epsilon (-)", "yLabel": "stress sigma (MPa)", "xRange": [0, 0.002], "yRange": [0, 400], "grid": true, "functions": [{"expr": "200000*x", "label": "steel E=200 GPa", "color": "#2563eb"}, {"expr": "70000*x", "label": "aluminium E=70 GPa", "color": "#16a34a"}]}
```

Combine Hooke's law with the definitions of stress and strain to get the
**axial deformation** of a uniform bar — the workhorse formula for stretch:

$$\delta = \frac{NL}{AE}.$$

Stiffness is geometry × material: the axial stiffness is $k = AE/L$, so a bar
behaves like a linear spring. Shear has its own version, $\tau = G\gamma$, with
**shear modulus** $G$. Hooke's law is the foundation of nearly everything that
follows — axial, torsion and bending all reduce to it locally.

**Next:** the sideways effect of stretching — Poisson's ratio.
""",
        ),
        _t(
            "Poisson's ratio and elastic constants",
            "10 min",
            r"""
# Poisson's ratio and elastic constants

Stretch a bar axially and it gets *thinner* sideways. **Poisson's ratio**
$\nu$ is the (positive) ratio of lateral contraction to axial extension:

$$\nu = -\frac{\varepsilon_{\text{lateral}}}{\varepsilon_{\text{axial}}}.$$

For most metals $\nu\approx 0.3$; rubber is near $0.5$ (almost
incompressible); cork is near $0$. Thermodynamics limits isotropic materials to
$-1 < \nu < 0.5$.

```plot
{"title": "Lateral strain vs axial strain (nu = 0.3)", "xLabel": "axial strain epsilon_axial (-)", "yLabel": "lateral strain epsilon_lat (-)", "xRange": [0, 0.01], "yRange": [-0.004, 0], "grid": true, "functions": [{"expr": "-0.3*x", "label": "eps_lat = -nu*eps_axial", "color": "#dc2626"}]}
```

For an **isotropic** material only two of the elastic constants are independent.
They are tied together by:

$$G = \frac{E}{2(1+\nu)}, \qquad K = \frac{E}{3(1-2\nu)},$$

where $G$ is the shear modulus and $K$ the bulk modulus. Knowing $E$ and $\nu$
fixes the complete linear-elastic response.

```mermaid
flowchart LR
  E["Young's modulus E"] --> R["Isotropic relations"]
  V["Poisson ratio nu"] --> R
  R --> G["Shear modulus G = E / (2(1+nu))"]
  R --> K["Bulk modulus K = E / (3(1-2nu))"]
```

**Next:** turning these properties into safe designs — factor of safety.
""",
        ),
        _t(
            "Factor of safety and allowable stress",
            "10 min",
            r"""
# Factor of safety and allowable stress

A real design never runs at the failure stress. The **factor of safety** (FoS)
is the ratio of a failure measure to the actual working value:

$$n = \frac{\sigma_{\text{fail}}}{\sigma_{\text{allow}}},$$

where $\sigma_{\text{fail}}$ is usually the yield strength $\sigma_y$ (or
ultimate $\sigma_u$ for brittle materials). Designers size members so the
**allowable (working) stress** stays below the limit:

$$\sigma_{\text{allow}} = \frac{\sigma_y}{n}.$$

Typical $n$ runs from ~1.5 for well-characterised aerospace structures to 3-5
for civil structures with uncertain loads. As $n$ rises, allowable stress falls,
so the part gets larger and heavier — safety trades against weight and cost:

```plot
{"title": "Allowable stress vs factor of safety (sigma_y = 250 MPa)", "xLabel": "factor of safety n", "yLabel": "allowable stress (MPa)", "xRange": [1, 6], "yRange": [0, 260], "grid": true, "functions": [{"expr": "250/x", "label": "sigma_allow = sigma_y / n", "color": "#2563eb"}]}
```

Modern codes (e.g. AISC LRFD, Eurocode) refine this into **load and resistance
factor design (LRFD)**, applying separate partial factors to loads and to
material resistance rather than a single lumped FoS.

```mermaid
flowchart LR
  M["Material strength sigma_y"] --> A["Divide by FoS n"]
  A --> W["Allowable stress"]
  W --> D["Size member: sigma_actual <= sigma_allow"]
```

**Next:** the Intermediate course — axial, torsion and bending, quantitatively.
""",
        ),
        _quiz(),
    ),
)


# ── Mechanics of Materials — Intermediate ────────────────────────────────────

_INTERMEDIATE = SeedCourse(
    slug="mechanics-of-materials-intermediate",
    title="Mechanics of Materials — Intermediate",
    description=(
        "The core quantitative methods of mechanics of materials: axial "
        "deformation of bars and statically indeterminate assemblies, torsion "
        "of circular shafts, shear-force and bending-moment diagrams, the "
        "flexure formula for bending stress and the transverse shear stress "
        "formula. Worked equations, plots and Python computations throughout."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Axial deformation and indeterminate bars",
            "13 min",
            r"""
# Axial deformation and indeterminate bars

For a prismatic bar with internal force $N$, the axial deformation is
$\delta = NL/(AE)$; for segments or varying load,

$$\delta = \sum_i \frac{N_i L_i}{A_i E_i} \quad\text{or}\quad
\delta = \int_0^L \frac{N(x)}{A(x)\,E}\,dx.$$

When the supports impose more reactions than statics can solve, the bar is
**statically indeterminate**: equilibrium alone is not enough. The recipe adds a
**compatibility** equation (a geometric constraint on deformation) plus the
**force-deformation** law. A bar fixed at both ends loaded at mid-span, for
example, splits the load between segments so the two ends do not move:
$\delta_{AB}+\delta_{BC}=0$.

```python
import numpy as np

# Bar fixed at both ends (A and C), axial load P applied at point B.
E = 200e9            # Pa (steel)
A = 1e-4             # m^2
L1, L2 = 0.6, 0.4    # m, segments AB and BC
P = 50e3             # N applied at B (toward C)

# Unknown: reaction R_A. Compatibility: total elongation = 0.
# delta = R_A*L1/(A E) + (R_A - P)*L2/(A E) = 0  ->  R_A*(L1+L2) = P*L2
R_A = P * L2 / (L1 + L2)
R_C = P - R_A
print(f"R_A = {R_A/1e3:.1f} kN, R_C = {R_C/1e3:.1f} kN")
sigma_AB = R_A / A / 1e6
print(f"stress AB = {sigma_AB:.1f} MPa")
```

The reactions split in inverse proportion to segment lengths (stiffness in
parallel). Thermal effects add a term $\delta_T=\alpha\,\Delta T\,L$, which in a
restrained bar generates large **thermal stress** $\sigma=E\alpha\,\Delta T$.

```plot
{"title": "Axial elongation vs load (delta = NL/AE)", "xLabel": "load N (kN)", "yLabel": "elongation delta (mm)", "xRange": [0, 100], "yRange": [0, 3], "grid": true, "functions": [{"expr": "0.03*x", "label": "delta = NL/AE", "color": "#2563eb"}]}
```

**Next:** twisting members — torsion of circular shafts.
""",
        ),
        _t(
            "Torsion of circular shafts",
            "12 min",
            r"""
# Torsion of circular shafts

A circular shaft carrying torque $T$ develops **shear stress** that grows
linearly from zero at the centre to a maximum at the surface. The **torsion
formula** is:

$$\tau = \frac{T\,\rho}{J}, \qquad \tau_{\max} = \frac{T\,r}{J},$$

where $\rho$ is radial position, $r$ the outer radius and $J$ the **polar moment
of inertia** ($J=\pi r^4/2$ for a solid circle, $\frac{\pi}{2}(r_o^4-r_i^4)$ for a
tube). The **angle of twist** over length $L$ is:

$$\phi = \frac{T L}{G J}.$$

```plot
{"title": "Torsional shear stress across the radius (linear)", "xLabel": "radial position rho (mm)", "yLabel": "shear stress tau (MPa)", "xRange": [0, 20], "yRange": [0, 80], "grid": true, "functions": [{"expr": "4*x", "label": "tau = T*rho/J", "color": "#dc2626"}]}
```

Power transmission ties torque to rotational speed: $P = T\omega$, so a shaft
turning at $\omega$ rad/s transmitting power $P$ carries $T = P/\omega$.

```python
import numpy as np

P = 50e3              # W
rpm = 1500
omega = rpm*2*np.pi/60
T = P/omega           # N*m
r = 0.02              # m (solid shaft)
J = np.pi*r**4/2
tau_max = T*r/J/1e6
G = 80e9
phi_per_m = T/(G*J)   # rad/m
print(f"T = {T:.1f} N*m, tau_max = {tau_max:.1f} MPa, twist = {np.degrees(phi_per_m):.3f} deg/m")
```

Hollow shafts are far more efficient: most material near the axis carries little
stress, so a tube gives nearly the same $J$ at much lower weight.

**Next:** how beams carry transverse load — shear and moment diagrams.
""",
        ),
        _t(
            "Shear force and bending moment diagrams",
            "13 min",
            r"""
# Shear force and bending moment diagrams

Beams resist transverse loads through internal **shear force** $V(x)$ and
**bending moment** $M(x)$. These vary along the beam, and the diagrams that plot
them are the central tool of beam design — the peak $M$ locates the most stressed
section. They obey the differential relations:

$$\frac{dV}{dx} = -w(x), \qquad \frac{dM}{dx} = V(x),$$

so distributed load is the slope of $V$, and shear is the slope of $M$. The
moment is extreme where $V=0$.

For a simply supported beam of span $L$ with a central point load $P$, the
reactions are $P/2$ each, shear jumps at midspan, and the moment peaks at
$M_{\max}=PL/4$.

```python
import numpy as np

P, L = 10e3, 4.0                 # N, m
x = np.linspace(0, L, 401)
R = P/2
V = np.where(x < L/2, R, R - P)  # shear
M = np.where(x < L/2, R*x, R*x - P*(x - L/2))
print(f"max |V| = {np.max(np.abs(V))/1e3:.1f} kN")
print(f"max M = {np.max(M)/1e3:.1f} kN*m  (expected PL/4 = {P*L/4/1e3:.1f})")
```

```plot
{"title": "Bending moment, simply supported beam, central load", "xLabel": "position x (m)", "yLabel": "moment M (kN*m)", "xRange": [0, 4], "yRange": [0, 12], "grid": true, "functions": [{"expr": "5*x", "label": "M(x), left half", "color": "#2563eb"}, {"expr": "5*(4-x)", "label": "M(x), right half", "color": "#16a34a"}]}
```

Sign convention: sagging (concave-up) moment is positive. Construct the diagrams
by integrating loads, or by sections — both give the inputs to the flexure
formula next.

**Next:** the stress those moments cause — the flexure formula.
""",
        ),
        _t(
            "Bending stress and the flexure formula",
            "12 min",
            r"""
# Bending stress and the flexure formula

A bending moment $M$ makes one face of a beam stretch and the other compress.
Plane sections stay plane, so normal strain varies linearly across the depth,
zero on the **neutral axis** (the centroid). With Hooke's law this gives the
**flexure formula**:

$$\sigma = -\frac{M\,y}{I}, \qquad \sigma_{\max} = \frac{M\,c}{I} = \frac{M}{S},$$

where $y$ is distance from the neutral axis, $I$ the **second moment of area**,
$c$ the distance to the extreme fibre and $S=I/c$ the **section modulus**.
Bending stress is largest at the top and bottom fibres and zero at the centroid:

```plot
{"title": "Bending stress varies linearly across the depth", "xLabel": "distance from neutral axis y (mm)", "yLabel": "stress sigma (MPa)", "xRange": [-50, 50], "yRange": [-120, 120], "grid": true, "functions": [{"expr": "2.4*x", "label": "sigma = -M*y/I (sign per convention)", "color": "#2563eb"}]}
```

For a rectangle $b\times h$, $I=bh^3/12$ and $S=bh^2/6$ — depth $h$ matters far
more than width $b$, which is why beams are tall and I-sections push area to the
flanges.

```python
b, h = 0.05, 0.10      # m
I = b*h**3/12          # m^4
c = h/2
S = I/c
M = 5e3                # N*m
sigma_max = M*c/I/1e6
print(f"I = {I:.3e} m^4, S = {S:.3e} m^3, sigma_max = {sigma_max:.1f} MPa")
```

To make a beam stiffer and stronger in bending, increase $I$ (deepen it) — the
single highest-leverage move in beam design.

**Next:** the shear stress that accompanies bending.
""",
        ),
        _t(
            "Transverse shear stress in beams",
            "11 min",
            r"""
# Transverse shear stress in beams

Bending moment produces normal stress; the accompanying **shear force** $V$
produces **transverse shear stress** through the cross-section, given by the
**shear formula**:

$$\tau = \frac{V\,Q}{I\,t},$$

where $Q$ is the **first moment of area** of the part of the section beyond the
point of interest, $I$ the second moment of area and $t$ the width there. Unlike
bending stress, shear stress is **zero at the top and bottom** fibres and
**maximum at the neutral axis**.

For a rectangular section the distribution is parabolic, peaking at
$\tau_{\max}=\tfrac{3}{2}\,V/A$ — 50 % higher than the average $V/A$:

```plot
{"title": "Parabolic shear stress across a rectangular section", "xLabel": "distance from neutral axis y (mm)", "yLabel": "shear stress tau (MPa)", "xRange": [-50, 50], "yRange": [0, 4], "grid": true, "functions": [{"expr": "3 - 0.0012*x^2", "label": "tau ~ (1 - (2y/h)^2)", "color": "#dc2626"}]}
```

```python
import numpy as np

V = 10e3
b, h = 0.05, 0.10
A = b*h
I = b*h**3/12
y = np.linspace(-h/2, h/2, 101)
Q = b*(h**2/8 - y**2/2)        # first moment above y
tau = V*Q/(I*b)
print(f"tau_max = {tau.max()/1e3:.2f} kPa, 1.5*V/A = {1.5*V/A/1e3:.2f} kPa")
```

In thin-walled sections (I-beams, channels) shear flows around the walls — the
**shear flow** $q=\tau t = VQ/I$ — and locating the **shear centre** prevents
unwanted twisting. Short, heavily loaded beams can be shear-critical rather than
bending-critical.

**Next:** the Advanced course — deflection, buckling, combined loading and FEM.
""",
        ),
        _quiz(),
    ),
)


# ── Mechanics of Materials — Advanced ────────────────────────────────────────

_ADVANCED = SeedCourse(
    slug="mechanics-of-materials-advanced",
    title="Mechanics of Materials — Advanced",
    description=(
        "State-of-the-art and applied mechanics of materials: beam deflection "
        "by integration and energy methods, plane stress transformation and "
        "Mohr's circle, combined loading, column buckling, the principal "
        "failure theories, fatigue and the S-N curve, and computational solid "
        "mechanics with the finite element method and structural optimization."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Beam deflection: integration and energy methods",
            "13 min",
            r"""
# Beam deflection: integration and energy methods

Strength limits stress; **serviceability** limits deflection. The elastic curve
$v(x)$ of a beam follows the **Euler-Bernoulli** equation:

$$EI\,\frac{d^2 v}{dx^2} = M(x).$$

Integrate twice and apply boundary conditions to get slope and deflection. A
cantilever of length $L$ with an end load $P$ deflects at the tip by:

$$\delta_{\text{tip}} = \frac{P L^3}{3 E I}.$$

The cubic dependence on $L$ dominates — doubling the span makes it eight times
softer.

```plot
{"title": "Cantilever tip deflection vs span (PL^3/3EI)", "xLabel": "span L (m)", "yLabel": "tip deflection delta (mm)", "xRange": [0, 3], "yRange": [0, 60], "grid": true, "functions": [{"expr": "2.2*x^3", "label": "delta = P L^3 / (3 E I)", "color": "#2563eb"}]}
```

**Energy methods** are often faster for complex loads. **Castigliano's second
theorem** gives a deflection as the partial derivative of strain energy with
respect to the corresponding load:

$$\delta_i = \frac{\partial U}{\partial P_i}, \qquad
U = \int \frac{M(x)^2}{2EI}\,dx.$$

```python
import numpy as np
from scipy.integrate import quad

P, L, E, I = 1000.0, 2.0, 200e9, 1e-6
# Castigliano: delta = (1/EI) * integral( M * dM/dP ) dx ; M = -P x for cantilever
integrand = lambda x: (-P*x)*(-x)/(E*I)
delta, _ = quad(integrand, 0, L)
print(f"delta_tip = {delta*1e3:.3f} mm  (closed form {P*L**3/(3*E*I)*1e3:.3f} mm)")
```

Superposition of tabulated cases handles most practical beams.

**Next:** how stress looks on rotated planes — transformation and Mohr's circle.
""",
        ),
        _t(
            "Stress transformation and Mohr's circle",
            "13 min",
            r"""
# Stress transformation and Mohr's circle

At a point under **plane stress** ($\sigma_x,\sigma_y,\tau_{xy}$), the stresses
on a plane rotated by $\theta$ follow the **transformation equations**:

$$\sigma_{x'} = \frac{\sigma_x+\sigma_y}{2} + \frac{\sigma_x-\sigma_y}{2}\cos 2\theta + \tau_{xy}\sin 2\theta.$$

The rotation angle that removes shear gives the **principal stresses**:

$$\sigma_{1,2} = \frac{\sigma_x+\sigma_y}{2} \pm \sqrt{\left(\frac{\sigma_x-\sigma_y}{2}\right)^2 + \tau_{xy}^2},$$

and the radius of that root is the **maximum in-plane shear stress**. Plotting
$(\sigma,\tau)$ as $\theta$ varies traces **Mohr's circle**, centred at the
average normal stress with that radius:

```plot
{"title": "Mohr's circle: shear vs normal stress as plane rotates", "xLabel": "normal stress sigma (MPa)", "yLabel": "shear stress tau (MPa)", "xRange": [-20, 120], "yRange": [-60, 60], "grid": true, "functions": [{"expr": "sqrt(abs(2500 - (x-50)^2))", "label": "upper half of Mohr circle", "color": "#2563eb"}, {"expr": "-sqrt(abs(2500 - (x-50)^2))", "label": "lower half", "color": "#16a34a"}]}
```

```python
import numpy as np

sx, sy, txy = 80.0, 20.0, 30.0          # MPa
avg = (sx+sy)/2
R = np.hypot((sx-sy)/2, txy)
s1, s2 = avg+R, avg-R
theta_p = 0.5*np.degrees(np.arctan2(2*txy, sx-sy))
print(f"sigma1 = {s1:.1f}, sigma2 = {s2:.1f} MPa, tau_max = {R:.1f} MPa, theta_p = {theta_p:.1f} deg")
```

Principal stresses feed directly into the failure theories.

**Next:** members under several loads at once — combined loading.
""",
        ),
        _t(
            "Combined loading and pressure vessels",
            "12 min",
            r"""
# Combined loading and pressure vessels

Real members rarely see a single action: a bracket may carry axial force,
bending and torsion together. Within linear elasticity, **superpose** the stress
contributions at a point, then transform to find principal stresses:

$$\sigma = \frac{N}{A} \pm \frac{M c}{I}, \qquad \tau = \frac{T r}{J} + \frac{V Q}{I t}.$$

A canonical case is the **thin-walled pressure vessel** (wall thickness
$t \ll r$). A cylinder under internal pressure $p$ develops a **hoop** (or
circumferential) stress twice the **longitudinal** stress:

$$\sigma_\theta = \frac{p r}{t}, \qquad \sigma_z = \frac{p r}{2 t}.$$

That 2:1 ratio is why cylindrical tanks split along their length, and why end
caps and welds are oriented accordingly.

```plot
{"title": "Hoop and longitudinal stress vs pressure (r/t = 50)", "xLabel": "internal pressure p (MPa)", "yLabel": "stress (MPa)", "xRange": [0, 5], "yRange": [0, 260], "grid": true, "functions": [{"expr": "50*x", "label": "hoop sigma_theta = p r / t", "color": "#dc2626"}, {"expr": "25*x", "label": "longitudinal sigma_z = p r / 2t", "color": "#2563eb"}]}
```

```python
p, r, t = 2e6, 0.5, 0.01     # Pa, m, m
hoop = p*r/t/1e6
longi = p*r/(2*t)/1e6
print(f"hoop = {hoop:.1f} MPa, longitudinal = {longi:.1f} MPa")
```

Spheres halve the stress again ($\sigma=pr/2t$ everywhere), which is why
high-pressure storage vessels are spherical.

**Next:** instability of slender members — column buckling.
""",
        ),
        _t(
            "Column buckling and stability",
            "12 min",
            r"""
# Column buckling and stability

A slender column can fail by **buckling** — a sudden sideways collapse — long
before its material yields. The **Euler critical load** for a pin-ended column is:

$$P_{cr} = \frac{\pi^2 E I}{(K L)^2},$$

where $KL$ is the **effective length** ($K=1$ pinned-pinned, $0.5$ fixed-fixed,
$2$ fixed-free). Buckling depends on stiffness $EI$ and geometry, *not* on
material strength. Dividing by area gives the critical stress in terms of the
**slenderness ratio** $KL/r$ (with $r=\sqrt{I/A}$ the radius of gyration):

$$\sigma_{cr} = \frac{\pi^2 E}{(KL/r)^2}.$$

```plot
{"title": "Critical buckling load vs column length (Euler)", "xLabel": "length L (m)", "yLabel": "P_cr (kN)", "xRange": [1, 5], "yRange": [0, 200], "grid": true, "functions": [{"expr": "200/x^2", "label": "P_cr = pi^2 E I / (KL)^2", "color": "#2563eb"}]}
```

The inverse-square dependence is dramatic — long columns are vastly weaker. Above
a transition slenderness, real columns yield before Euler buckling, so codes use
the **Johnson parabola** or column curves for intermediate columns.

```python
import numpy as np

E, I = 200e9, 4.9e-7      # Pa, m^4
K, L = 1.0, 3.0
P_cr = np.pi**2*E*I/(K*L)**2
A = 2.5e-3
r = np.sqrt(I/A)
print(f"P_cr = {P_cr/1e3:.1f} kN, slenderness KL/r = {K*L/r:.0f}")
```

**Next:** predicting failure under general stress — failure theories.
""",
        ),
        _t(
            "Failure theories and fatigue",
            "13 min",
            r"""
# Failure theories and fatigue

Under combined stress, when does a material fail? **Yield criteria** map a 3D
stress state to a single equivalent stress compared with $\sigma_y$:

- **von Mises (distortion-energy)** — best for ductile metals:
  $$\sigma_v = \sqrt{\sigma_1^2 - \sigma_1\sigma_2 + \sigma_2^2}\;\le\;\sigma_y.$$
- **Tresca (maximum shear)** — conservative:
  $\tau_{\max}=(\sigma_1-\sigma_3)/2 \le \sigma_y/2$.
- **Maximum normal stress (Rankine)** — for brittle materials.

Even below yield, repeated loading causes **fatigue**. The **S-N curve** plots
stress amplitude against cycles to failure $N_f$ (log scale); steels show an
**endurance limit** below which life is effectively infinite:

```plot
{"title": "S-N (Wohler) curve: stress amplitude vs log cycles", "xLabel": "log10(cycles to failure)", "yLabel": "stress amplitude (MPa)", "xRange": [3, 8], "yRange": [100, 400], "grid": true, "functions": [{"expr": "550 - 60*x", "label": "finite-life region", "color": "#dc2626"}, {"expr": "180", "label": "endurance limit", "color": "#16a34a"}]}
```

```python
import numpy as np

# Basquin finite-life: S = sigma_f' * (2 Nf)^b
sigma_f, b = 900.0, -0.085
Nf = np.array([1e4, 1e5, 1e6])
S = sigma_f*(2*Nf)**b
for n, s in zip(Nf, S):
    print(f"Nf = {n:.0e} cycles -> amplitude {s:.0f} MPa")
```

Mean stress (Goodman/Gerber), stress concentrations and surface finish strongly
reduce fatigue life — most service failures are fatigue, not static overload.

**Next:** solving real geometries numerically — FEM and optimization.
""",
        ),
        _t(
            "Finite element method and structural optimization",
            "14 min",
            r"""
# Finite element method and structural optimization

Closed-form formulas cover simple shapes; real parts need the **finite element
method (FEM)**. The continuum is discretised into elements; each contributes a
**stiffness matrix** $k$, assembled into a global system:

$$\mathbf{K}\,\mathbf{u} = \mathbf{F},$$

solved for nodal displacements $\mathbf{u}$, from which element strains and
stresses follow. For a 1D axial (bar) element the element stiffness is
$k=\frac{AE}{L}\begin{psmallmatrix}1&-1\\-1&1\end{psmallmatrix}$.

```python
import numpy as np

# Two axial bar elements in series, fixed-free, end load P.
E, A = 200e9, 1e-4
L = 0.5
k = A*E/L
K = np.zeros((3, 3))
ke = k*np.array([[1, -1], [-1, 1]])
for n in (0, 1):                       # assemble elements 0-1 and 1-2
    K[n:n+2, n:n+2] += ke
# Node 0 fixed -> solve reduced system for u1, u2 with F = [0, P] at nodes 1,2
P = 30e3
Kr = K[1:, 1:]
u = np.linalg.solve(Kr, np.array([0.0, P]))
print(f"u_node1 = {u[0]*1e3:.4f} mm, u_node2 (tip) = {u[1]*1e3:.4f} mm")
```

Beyond analysis, **structural optimization** automates design: minimise mass
subject to stress/displacement constraints, or run **topology optimization**
(SIMP method) to grow material only where it carries load. Gradient-based and
ML-surrogate optimizers converge the objective iteration by iteration:

```plot
{"title": "Optimization convergence (mass vs iteration)", "xLabel": "iteration", "yLabel": "normalized objective", "xRange": [0, 10], "yRange": [0, 1], "grid": true, "functions": [{"expr": "exp(-0.4*x)", "label": "objective ~ exp(-0.4 k)", "color": "#16a34a"}]}
```

```mermaid
flowchart LR
  CAD["Geometry / mesh"] --> FEA["FEM solve K u = F"]
  FEA --> S["Stress, displacement"]
  S --> O["Optimizer: update design"]
  O -->|"converged?"| FEA
  O --> R["Lightweight design"]
```

Commercial tools (Abaqus, ANSYS, COMSOL) and open-source (CalculiX, FEniCS)
implement this, increasingly coupled with ML surrogates for fast design search.

**Next:** you have completed the Mechanics of Materials track.
""",
        ),
        _quiz(),
    ),
)


MECHANICS_OF_MATERIALS_COURSES: tuple[SeedCourse, ...] = (_BASICS, _INTERMEDIATE, _ADVANCED)
__all__ = ["MECHANICS_OF_MATERIALS_COURSES"]
