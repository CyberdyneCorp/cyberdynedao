"""Curated Electromagnetics track: Basics, Intermediate, Advanced.

A complete electromagnetics curriculum: static fields (charge, Coulomb, Gauss,
potential, capacitance, magnetism, induction, materials), Maxwell's equations and
electromagnetic waves (wave equation, polarization, the spectrum, Poynting,
reflection/refraction), and high-frequency engineering (transmission lines, the
Smith chart, antennas, waveguides, numerical EM and EMC). Dual MATLAB + Python
focus throughout, with runnable Python labs (numpy + matplotlib), interactive
```plot blocks, Mermaid diagrams, LaTeX formulas, and real use cases.

Quizzes (per-lesson checkpoints + a final) are attached from the central
QUIZ_REGISTRY at assembly time.
"""

from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import SeedCourse, SeedLesson


def _t(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="text", duration=duration, text_body=body)


def _code(title: str, duration: str, body: str) -> SeedLesson:
    return SeedLesson(title=title, lesson_type="code", duration=duration, text_body=body)


# -- Electromagnetics -- Basics: Fields ----------------------------------------

_EM_BASICS = SeedCourse(
    slug="electromagnetics-basics",
    title="Electromagnetics — Basics: Fields",
    description=(
        "Static electric and magnetic fields from the ground up: charge and "
        "Coulomb's law, field lines and Gauss's law, potential and capacitance, "
        "magnetism (Biot-Savart, Ampere, forces), electromagnetic induction "
        "(Faraday, Lenz, inductance, transformers), and how materials respond - "
        "with side-by-side MATLAB and Python, interactive plots, and a runnable "
        "field/potential lab."
    ),
    level="Beginner",
    lessons=(
        _t(
            "Electric charge & fields",
            "12 min",
            """\
# Electric charge & fields

Electromagnetics is the physics of **electric charge** and the fields it makes.
Charge comes in two signs (positive, negative), is **conserved**, and is
**quantized** in units of the electron charge $e \\approx 1.602 \\times 10^{-19}$ C.

## Coulomb's law

Two point charges push or pull along the line joining them, with a force that
falls off as the inverse square of distance:

$$\\vec{F} = \\frac{1}{4\\pi\\varepsilon_0}\\,\\frac{q_1 q_2}{r^2}\\,\\hat{r}, \\qquad \\frac{1}{4\\pi\\varepsilon_0} \\approx 8.99 \\times 10^9\\ \\text{N m}^2/\\text{C}^2.$$

Like charges repel, opposites attract. The inverse-square fall-off is steep -
slide the test charge and watch the force collapse with distance:

```plot
{"title": "Coulomb force vs separation (slide the charge q)", "xLabel": "separation r (m)", "yLabel": "force (N)", "xRange": [0.1, 3], "yRange": [0, 10], "grid": true, "controls": [{"name": "q", "range": [0.2, 2], "value": 1, "label": "charge q (uC)"}], "functions": [{"expr": "8.99*q/(x^2)", "label": "F = k q^2 / r^2"}]}
```

## The electric field

Rather than track every pairwise force, we say a charge fills space with an
**electric field** $\\vec{E}$ - the force per unit positive test charge:

$$\\vec{E} = \\frac{\\vec{F}}{q_{test}}, \\qquad E = \\frac{1}{4\\pi\\varepsilon_0}\\,\\frac{Q}{r^2}\\ \\text{(point charge)}.$$

**Field lines** point the way a positive charge would be pushed: out of positive
charges, into negative ones. Their density encodes field strength.

```mermaid
flowchart LR
  POS["+Q (source)"] -->|field lines out| SPACE["surrounding space"]
  SPACE -->|field lines in| NEG["-Q (sink)"]
```

## Gauss's law

A beautiful shortcut: the **electric flux** through any closed surface depends
only on the charge **inside** it:

$$\\oint \\vec{E}\\cdot d\\vec{A} = \\frac{Q_{enc}}{\\varepsilon_0}.$$

For symmetric problems (spheres, infinite lines, infinite planes) Gauss's law
gives the field in one line. A line of charge gives $E \\propto 1/r$; a sheet
gives a field that is **constant** with distance:

```plot
{"title": "Gauss's law: how E falls off by geometry", "xLabel": "distance r (m)", "yLabel": "E (relative)", "xRange": [0.2, 4], "yRange": [0, 6], "grid": true, "functions": [{"expr": "1/(x^2)", "label": "point charge ~ 1/r^2", "color": "#2563eb"}, {"expr": "1/x", "label": "line charge ~ 1/r", "color": "#16a34a"}, {"expr": "1 + 0*x", "label": "infinite sheet ~ const", "color": "#dc2626"}]}
```

## Where this shows up

Coulomb forces hold every **atom and molecule** together, drive **xerography**
and laser printers (charged toner), separate particles in **electrostatic
precipitators** (smokestack scrubbers), and explain why you get a **static
shock** after walking on carpet.

```matlab
k = 8.99e9; q1 = 1e-6; q2 = 2e-6; r = 0.1;
F = k*q1*q2/r^2;          % Coulomb force (N)
E = k*q1/r^2;             % field from q1 at r
```

```python
k, q1, q2, r = 8.99e9, 1e-6, 2e-6, 0.1
F = k*q1*q2/r**2          # Coulomb force (N)
E = k*q1/r**2             # field from q1 at r
```

**Next:** the energy view - potential and capacitance.
""",
        ),
        _t(
            "Electric potential & capacitance",
            "12 min",
            """\
# Electric potential & capacitance

The field tells you the force; **electric potential** tells you the energy. The
potential $V$ is the potential energy per unit charge, and it is what your
voltmeter actually measures.

## Potential of a point charge

$$V = \\frac{1}{4\\pi\\varepsilon_0}\\,\\frac{Q}{r}, \\qquad \\vec{E} = -\\nabla V.$$

The field is the **downhill slope** of potential. Surfaces of constant $V$ are
**equipotentials**, and field lines always cross them at right angles - like
contour lines and steepest-descent paths on a topographic map. The potential of
a point charge falls off as $1/r$ (gentler than the $1/r^2$ field):

```plot
{"title": "Potential and field of a point charge vs distance", "xLabel": "distance r (m)", "yLabel": "value (relative)", "xRange": [0.2, 4], "yRange": [0, 8], "grid": true, "functions": [{"expr": "1/x", "label": "potential V ~ 1/r", "color": "#2563eb"}, {"expr": "1/(x^2)", "label": "field E ~ 1/r^2", "color": "#dc2626"}]}
```

## Capacitance: storing charge

Two conductors separated by an insulator form a **capacitor**. Apply a voltage
and they store equal and opposite charge; the ratio is the **capacitance**:

$$C = \\frac{Q}{V}, \\qquad C_{\\text{parallel plate}} = \\frac{\\varepsilon_0\\,A}{d}.$$

More plate area or a thinner gap means more capacitance. Slide the gap $d$ and
watch capacitance climb as the plates get closer:

```plot
{"title": "Parallel-plate capacitance vs gap (slide area A)", "xLabel": "plate gap d (mm)", "yLabel": "capacitance (pF)", "xRange": [0.1, 5], "yRange": [0, 200], "grid": true, "controls": [{"name": "A", "range": [50, 400], "value": 100, "label": "plate area A (cm^2)"}], "functions": [{"expr": "8.854*A/x", "label": "C = eps0 A / d"}]}
```

## Energy stored

$$U = \\tfrac{1}{2} C V^2 = \\tfrac{1}{2} Q V = \\frac{Q^2}{2C}.$$

This energy lives in the **electric field** between the plates, at a density
$u = \\tfrac{1}{2}\\varepsilon_0 E^2$.

## Where this shows up

Capacitors are everywhere: **smoothing** power supplies, **timing** circuits,
**touchscreens** (your finger changes a capacitance), **DRAM** cells (one bit =
one tiny charged capacitor), and the **defibrillator** that dumps a stored joule
burst into a heart.

```matlab
eps0 = 8.854e-12; A = 0.01; d = 1e-3;
C = eps0*A/d;             % parallel-plate capacitance (F)
U = 0.5*C*12^2;           % energy stored at 12 V (J)
```

```python
eps0, A, d = 8.854e-12, 0.01, 1e-3
C = eps0*A/d              # capacitance (F)
U = 0.5*C*12**2           # energy at 12 V (J)
```

**Next:** moving charge makes magnetism.
""",
        ),
        _t(
            "Magnetic fields: Biot-Savart, Ampere & forces",
            "13 min",
            """\
# Magnetic fields: Biot-Savart, Ampere & forces

**Moving** charge - a current - creates a **magnetic field** $\\vec{B}$. Unlike
electric field lines, magnetic field lines form **closed loops** (there are no
magnetic monopoles).

## Two ways to find B

**Biot-Savart law** - sum the contribution of every current element (the
magnetic analogue of Coulomb's law):

$$d\\vec{B} = \\frac{\\mu_0}{4\\pi}\\,\\frac{I\\,d\\vec{l} \\times \\hat{r}}{r^2}, \\qquad \\mu_0 = 4\\pi \\times 10^{-7}\\ \\text{T m/A}.$$

**Ampere's law** - for symmetric geometries, the line integral of $\\vec{B}$
around a loop equals the enclosed current (the magnetic Gauss):

$$\\oint \\vec{B}\\cdot d\\vec{l} = \\mu_0 I_{enc}.$$

A long straight wire gives $B = \\mu_0 I / (2\\pi r)$ - falling off as $1/r$.
Slide the current and watch the field grow:

```plot
{"title": "Field around a long straight wire: B = mu0 I/(2 pi r)", "xLabel": "distance from wire r (mm)", "yLabel": "B (uT)", "xRange": [1, 50], "yRange": [0, 60], "grid": true, "controls": [{"name": "I", "range": [1, 20], "value": 5, "label": "current I (A)"}], "functions": [{"expr": "200*I/x", "label": "B(r)"}]}
```

## Forces: the Lorentz law

A magnetic field pushes on moving charge and on current-carrying wires:

$$\\vec{F} = q\\,\\vec{v} \\times \\vec{B}, \\qquad \\vec{F} = I\\,\\vec{L} \\times \\vec{B}.$$

The force is **perpendicular** to both velocity and field (right-hand rule), so a
charge in a uniform field travels in a **circle** at the cyclotron frequency
$\\omega_c = qB/m$. The magnetic force does **no work** (it only steers).

```mermaid
flowchart LR
  I["current I in wire"] --> B["external field B"]
  B --> F["force F = I L x B (sideways)"]
```

## Where this shows up

This is the heart of every **electric motor** (force on a current loop),
**loudspeaker** (force on a voice coil), **MRI scanner** (huge superconducting
$B$), **mass spectrometer** and **cyclotron** (circular charge paths), and the
**maglev** train.

```matlab
mu0 = 4*pi*1e-7; I = 10; r = 0.05;
B = mu0*I/(2*pi*r);       % field of a long wire (T)
F = I*0.2*B;              % force on a 0.2 m wire (N)
```

```python
import numpy as np
mu0, I, r = 4*np.pi*1e-7, 10, 0.05
B = mu0*I/(2*np.pi*r)     # field of a long wire (T)
F = I*0.2*B               # force on a 0.2 m wire (N)
```

**Next:** changing fields make voltage - induction.
""",
        ),
        _t(
            "Electromagnetic induction: Faraday, Lenz & inductance",
            "13 min",
            """\
# Electromagnetic induction: Faraday, Lenz & inductance

A static field stores energy; a **changing** magnetic field *generates*
electricity. This is the principle behind every generator and transformer.

## Faraday's law

A changing magnetic **flux** $\\Phi_B = \\int \\vec{B}\\cdot d\\vec{A}$ through a
loop induces a voltage (electromotive force):

$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt}.$$

The flux changes if the field changes, the loop area changes, or the loop
rotates. A coil spun in a field gives a **sinusoidal** voltage - the AC
generator. Slide the rotation speed and see the induced EMF amplitude grow:

```plot
{"title": "Induced EMF from a coil spinning in a field (slide speed)", "xLabel": "time (s)", "yLabel": "EMF (V)", "xRange": [0, 6.2832], "yRange": [-12, 12], "grid": true, "controls": [{"name": "w", "range": [1, 4], "value": 2, "label": "angular speed w (rad/s)"}], "functions": [{"expr": "3*w*sin(w*x)", "label": "EMF = -d(phi)/dt"}]}
```

## Lenz's law: the minus sign

The minus sign in Faraday's law is **Lenz's law**: the induced current flows to
**oppose** the change that made it. Push a magnet into a coil and the coil pushes
back - that opposition is where the mechanical work goes (and why a generator is
hard to turn under load). It is conservation of energy enforced.

## Inductance

A coil resists changes in its own current by inducing a back-EMF; the
proportionality is the **inductance** $L$:

$$v = L\\,\\frac{di}{dt}, \\qquad U = \\tfrac{1}{2} L i^2, \\qquad L_{solenoid} = \\frac{\\mu_0 N^2 A}{\\ell}.$$

## Transformers

Two coils sharing a magnetic core: a changing current in the primary induces a
voltage in the secondary, scaled by the **turns ratio**:

$$\\frac{V_s}{V_p} = \\frac{N_s}{N_p}, \\qquad \\frac{I_s}{I_p} = \\frac{N_p}{N_s}.$$

```mermaid
flowchart LR
  VP["primary Vp, Np turns"] --> CORE["shared iron core (flux)"]
  CORE --> VS["secondary Vs, Ns turns"]
```

## Where this shows up

Induction runs the **power grid** (generators and transformers step voltage up
for transmission, down for homes), **induction cooktops** and **wireless
chargers** (changing field heats/powers a coil), **electric guitar pickups**,
**metal detectors**, and **regenerative braking** in EVs.

```matlab
Np = 1000; Ns = 100; Vp = 230;
Vs = Vp*Ns/Np;            % step-down transformer -> 23 V
L = 1e-3; didt = 500;
vL = L*didt;              % back-EMF across an inductor
```

```python
Np, Ns, Vp = 1000, 100, 230
Vs = Vp*Ns/Np             # step-down -> 23 V
L, didt = 1e-3, 500
vL = L*didt               # back-EMF (V)
```

**Next:** how matter responds to fields.
""",
        ),
        _t(
            "Materials: dielectrics, conductors & boundaries",
            "11 min",
            """\
# Materials: dielectrics, conductors & boundaries

Fields behave differently inside matter. Two material constants capture the
response: the **permittivity** $\\varepsilon$ (electric) and the **permeability**
$\\mu$ (magnetic), usually written relative to vacuum:

$$\\varepsilon = \\varepsilon_r\\,\\varepsilon_0, \\qquad \\mu = \\mu_r\\,\\mu_0.$$

## Dielectrics: insulators that polarize

A **dielectric** has no free charge, but its molecules **polarize** in a field,
partly cancelling it. This lets a capacitor store more charge at the same
voltage: filling the gap with a dielectric of constant $\\varepsilon_r$ multiplies
capacitance by $\\varepsilon_r$:

$$C = \\varepsilon_r\\,\\frac{\\varepsilon_0 A}{d}.$$

```plot
{"title": "A dielectric multiplies capacitance (slide eps_r)", "xLabel": "plate gap d (mm)", "yLabel": "capacitance (pF)", "xRange": [0.2, 5], "yRange": [0, 400], "grid": true, "controls": [{"name": "epsr", "range": [1, 10], "value": 4, "label": "relative permittivity eps_r"}], "functions": [{"expr": "8.854*epsr*100/x", "label": "C = eps_r eps0 A / d"}]}
```

Common values: vacuum 1, air ~1, paper ~3, glass ~5, water ~80. Every dielectric
also has a **breakdown field** above which it arcs (air ~3 MV/m).

## Conductors: free charge moves

Inside a conductor in **electrostatic** equilibrium, charges rearrange until the
internal field is **zero** and all the excess charge sits on the **surface**.
That is why a metal box (a **Faraday cage**) shields its interior from external
fields - the basis of EMI shielding and why you are safe in a car during
lightning.

## Magnetic materials

| Class | $\\mu_r$ | Example |
|-------|---------|---------|
| Diamagnetic | slightly < 1 | copper, water |
| Paramagnetic | slightly > 1 | aluminum |
| **Ferromagnetic** | huge (100s-1000s) | iron, steel, ferrite |

Ferromagnets concentrate flux (transformer and motor cores) and show
**hysteresis** - they remember their magnetization (permanent magnets, data
storage).

## Boundary behaviour

At an interface between two media, the fields jump in a fixed way: the
**tangential E** and **tangential H** are continuous, while the **normal D** and
**normal B** are continuous. These boundary conditions are what bend light and
radio waves at surfaces - the subject of the Intermediate course.

```mermaid
flowchart LR
  M1["medium 1 (eps1, mu1)"] --> BC["boundary: tangential E, normal D continuous"]
  BC --> M2["medium 2 (eps2, mu2)"]
```

```matlab
eps0 = 8.854e-12; epsr = 4; A = 0.01; d = 1e-3;
C = epsr*eps0*A/d;        % capacitance with dielectric (F)
```

```python
eps0, epsr, A, d = 8.854e-12, 4, 0.01, 1e-3
C = epsr*eps0*A/d         # capacitance with dielectric (F)
```

**Next:** map the field of point charges yourself.
""",
        ),
        _code(
            "Lab: field & potential of point charges",
            "13 min",
            """\
# Map the electric field and potential of a pair of point charges (a dipole).
# Plot equipotential contours and the field-line direction (quiver) on a grid.
import numpy as np
import matplotlib.pyplot as plt

k = 8.99e9                      # Coulomb constant

# Two charges: +Q on the left, -Q on the right (a dipole).
charges = [(+1e-9, -1.0, 0.0), (-1e-9, +1.0, 0.0)]   # (q, x, y)

# Grid over the region of interest.
gx = np.linspace(-3, 3, 60)
gy = np.linspace(-3, 3, 60)
X, Y = np.meshgrid(gx, gy)

V = np.zeros_like(X)
Ex = np.zeros_like(X)
Ey = np.zeros_like(X)

for q, cx, cy in charges:
    dx = X - cx
    dy = Y - cy
    r = np.sqrt(dx**2 + dy**2) + 1e-9      # avoid divide-by-zero
    V += k*q/r
    Ex += k*q*dx/r**3
    Ey += k*q*dy/r**3

# Normalize field arrows so direction is visible everywhere.
mag = np.sqrt(Ex**2 + Ey**2) + 1e-12
Ux = Ex/mag
Uy = Ey/mag

plt.figure(figsize=(7, 6))
levels = np.linspace(-15, 15, 31)
cs = plt.contour(X, Y, np.clip(V, -15, 15), levels=levels, cmap="coolwarm")
plt.quiver(X[::3, ::3], Y[::3, ::3], Ux[::3, ::3], Uy[::3, ::3],
           color="#334155", scale=30, width=0.003)
plt.plot(-1, 0, "o", color="#dc2626", markersize=12, label="+Q")
plt.plot(+1, 0, "o", color="#2563eb", markersize=12, label="-Q")
plt.gca().set_aspect("equal")
plt.title("Dipole: equipotential contours + field direction")
plt.xlabel("x"); plt.ylabel("y"); plt.legend(); plt.show()

# Field magnitude at the origin (midpoint) - should point from + to -.
print(f"|E| at origin ~ {mag[30, 30]:.2e} (relative units)")
print("Field lines run from the + charge to the - charge.")

# Try it yourself:
#   1. Make both charges +1e-9 (like charges): the field pushes outward, no dipole.
#   2. The MATLAB way: use meshgrid, then contour() and quiver() the same arrays.
""",
        ),
    ),
)


# -- Electromagnetics -- Intermediate: Maxwell & Waves -------------------------

_EM_INTERMEDIATE = SeedCourse(
    slug="electromagnetics-intermediate",
    title="Electromagnetics — Intermediate: Maxwell & Waves",
    description=(
        "Maxwell's four equations and the electromagnetic wave: displacement "
        "current, the wave equation and c = 1/sqrt(mu eps), plane waves and the "
        "spectrum, polarization, the Poynting vector and power flow, and "
        "reflection/refraction at boundaries (Snell, Fresnel) - with dual "
        "MATLAB/Python, interactive plots, and a runnable wave-propagation lab."
    ),
    level="Intermediate",
    lessons=(
        _t(
            "Maxwell's equations",
            "13 min",
            """\
# Maxwell's equations

Four equations, written together by James Clerk Maxwell in the 1860s, contain
**all** of classical electromagnetism. In differential form:

| # | Equation | What it says |
|---|----------|--------------|
| 1 | $\\nabla\\cdot\\vec{E} = \\dfrac{\\rho}{\\varepsilon_0}$ | Gauss: charge makes diverging E |
| 2 | $\\nabla\\cdot\\vec{B} = 0$ | no magnetic monopoles (B loops close) |
| 3 | $\\nabla\\times\\vec{E} = -\\dfrac{\\partial \\vec{B}}{\\partial t}$ | Faraday: changing B makes E |
| 4 | $\\nabla\\times\\vec{B} = \\mu_0\\vec{J} + \\mu_0\\varepsilon_0\\dfrac{\\partial \\vec{E}}{\\partial t}$ | Ampere-Maxwell: current **and** changing E make B |

## The crucial addition: displacement current

Ampere's original law ($\\nabla\\times\\vec{B} = \\mu_0\\vec{J}$) fails for a
charging capacitor - no current flows through the gap, yet there is clearly a
magnetic field around it. Maxwell's fix was the **displacement current** term
$\\mu_0\\varepsilon_0\\,\\partial\\vec{E}/\\partial t$: a **changing electric
field** acts like a current and makes a magnetic field.

This is the linchpin. Equations 3 and 4 now feed each other: a changing $E$ makes
$B$, a changing $B$ makes $E$ - a self-sustaining **wave** that needs no wires
and no charges to keep going. Light was suddenly an electromagnetic phenomenon.

```mermaid
flowchart LR
  E["changing E field"] -->|Ampere-Maxwell| B["makes B field"]
  B -->|Faraday| E2["changing B makes E field"]
  E2 --> E
```

## The same physics, two scales

The differential form (above) is local; the **integral form** is what you use by
hand:

$$\\oint \\vec{E}\\cdot d\\vec{A} = \\frac{Q_{enc}}{\\varepsilon_0}, \\qquad \\oint \\vec{B}\\cdot d\\vec{l} = \\mu_0 I_{enc} + \\mu_0\\varepsilon_0\\frac{d\\Phi_E}{dt}.$$

The displacement current scales with frequency, so it is negligible at DC and
**dominant** at radio and optical frequencies. Slide the frequency to see the
displacement current density grow:

```plot
{"title": "Displacement current density vs frequency (slide field amplitude)", "xLabel": "frequency f (MHz)", "yLabel": "Jd (relative)", "xRange": [0, 100], "yRange": [0, 100], "grid": true, "controls": [{"name": "E0", "range": [0.2, 2], "value": 1, "label": "E amplitude (relative)"}], "functions": [{"expr": "E0*x", "label": "Jd = eps0 dE/dt ~ f"}]}
```

## Where this shows up

Maxwell's equations underpin **all** of radio, optics, microwaves, and antennas.
Every simulation tool (Ansys HFSS, CST, COMSOL) numerically solves exactly these
equations - which is the Advanced course's numerical-EM topic.

```matlab
eps0 = 8.854e-12; mu0 = 4*pi*1e-7;
c = 1/sqrt(mu0*eps0);     % speed of light from Maxwell (~3e8 m/s)
```

```python
import numpy as np
eps0, mu0 = 8.854e-12, 4*np.pi*1e-7
c = 1/np.sqrt(mu0*eps0)   # speed of light (~3e8 m/s)
```

**Next:** the wave that falls out of these equations.
""",
        ),
        _t(
            "The wave equation & electromagnetic waves",
            "13 min",
            """\
# The wave equation & electromagnetic waves

Combine Maxwell's curl equations (take the curl of Faraday, substitute
Ampere-Maxwell) in empty space and out pops the **wave equation**:

$$\\nabla^2 \\vec{E} = \\mu_0\\varepsilon_0\\,\\frac{\\partial^2 \\vec{E}}{\\partial t^2}.$$

This is the equation of any wave travelling at speed

$$c = \\frac{1}{\\sqrt{\\mu_0\\varepsilon_0}} \\approx 3.00 \\times 10^8\\ \\text{m/s}.$$

Maxwell computed this number from electrical measurements, found it matched the
measured speed of **light**, and concluded light *is* an electromagnetic wave.

## The plane wave

The simplest solution: $\\vec{E}$ and $\\vec{B}$ are perpendicular to each other
and to the direction of travel (a **transverse** wave), oscillating in step:

$$E(z,t) = E_0\\cos(kz - \\omega t), \\qquad \\frac{E_0}{B_0} = c, \\qquad k = \\frac{2\\pi}{\\lambda}, \\quad \\omega = 2\\pi f.$$

Wavelength, frequency, and speed are locked together: $c = \\lambda f$. Press Play
to watch the wave march to the right:

```plot
{"title": "A travelling plane wave E(z,t) = cos(kz - wt) - press Play", "xLabel": "position z", "yLabel": "E field", "xRange": [0, 12.566], "yRange": [-1.4, 1.4], "grid": true, "animate": {"param": "t", "range": [0, 6.2832], "label": "time"}, "functions": [{"expr": "cos(x - t)", "label": "E(z, t)"}], "points": [{"xExpr": "t", "yExpr": "cos(t - t)", "label": "crest", "color": "#dc2626", "size": 6, "trail": true}]}
```

## In a medium

Inside a material the wave slows to $v = 1/\\sqrt{\\mu\\varepsilon} = c/n$, where the
**refractive index** is $n = \\sqrt{\\varepsilon_r \\mu_r}$. The frequency stays the
same but the wavelength shrinks. Slide $n$ to compress the wave:

```plot
{"title": "Wavelength shrinks in a medium of index n (slide n)", "xLabel": "position z", "yLabel": "E field", "xRange": [0, 12.566], "yRange": [-1.4, 1.4], "grid": true, "controls": [{"name": "n", "range": [1, 3], "value": 1.5, "label": "refractive index n"}], "functions": [{"expr": "cos(n*x)", "label": "shorter wavelength in medium"}]}
```

## Where this shows up

Every wireless link, every fiber-optic cable, every radar, every camera - all are
EM waves at different frequencies. The locked $c = \\lambda f$ is why a 2.4 GHz
Wi-Fi wave is ~12.5 cm long (setting antenna sizes), and why GPS timing must
account for the finite speed of light.

```matlab
c = 3e8; f = 2.4e9;
lambda = c/f;             % Wi-Fi wavelength ~ 0.125 m
n = 1.5; v = c/n;         % speed in glass
```

```python
c, f = 3e8, 2.4e9
lam = c/f                 # wavelength ~ 0.125 m
n = 1.5; v = c/n          # speed in glass
```

**Next:** the orientation of the wave - polarization and the spectrum.
""",
        ),
        _t(
            "Polarization & the electromagnetic spectrum",
            "12 min",
            """\
# Polarization & the electromagnetic spectrum

A plane wave's $\\vec{E}$ points in a definite direction perpendicular to travel.
That direction - and how it evolves in time - is the **polarization**.

## Three polarization states

- **Linear** - $\\vec{E}$ oscillates along one fixed line.
- **Circular** - $\\vec{E}$ rotates at constant magnitude (two equal linear
  components 90 degrees out of phase).
- **Elliptical** - the general case.

Trace the tip of the $\\vec{E}$ vector over one cycle. Slide the phase between the
two components and watch a line become a circle become an ellipse:

```plot
{"title": "Polarization: tip of E vector over one cycle (slide phase)", "xLabel": "Ex", "yLabel": "Ey", "xRange": [-1.4, 1.4], "yRange": [-1.4, 1.4], "grid": true, "controls": [{"name": "p", "range": [0, 3.1416], "value": 1.5708, "label": "phase delta (rad)"}], "parametric": [{"x": "cos(t)", "y": "cos(t - p)", "range": [0, 6.2832], "label": "E tip (line -> circle -> ellipse)"}]}
```

A **polarizer** transmits only one linear direction; Malus's law gives the
throughput as $I = I_0\\cos^2\\theta$:

```plot
{"title": "Malus's law: a polarizer passes I0 cos^2(angle)", "xLabel": "angle between polarizer axes (deg)", "yLabel": "transmitted fraction", "xRange": [0, 180], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "cos(rad(x))^2", "label": "I / I0"}]}
```

## The electromagnetic spectrum

All EM waves are the same physics; only the frequency (and wavelength) differ:

```mermaid
flowchart LR
  RADIO["radio kHz-GHz"] --> MICRO["microwave"] --> IR["infrared"] --> VIS["visible"] --> UV["UV"] --> XRAY["X-ray"] --> GAMMA["gamma"]
```

| Band | Frequency | Use |
|------|-----------|-----|
| Radio | kHz - GHz | broadcast, Wi-Fi, cell |
| Microwave | 1 - 100 GHz | radar, ovens, satellite |
| Infrared | THz | heat, night vision, remotes |
| Visible | ~400-790 THz | sight, displays |
| X-ray / gamma | PHz+ | imaging, sterilization |

## Where this shows up

Polarized **sunglasses** block horizontally polarized glare; **LCD** screens
switch polarization to make pixels; **3D cinema** uses circular polarization per
eye; **radar** and **satellite** links reuse frequencies on orthogonal
polarizations to double capacity.

```matlab
theta = 30;               % degrees between polarizers
I = cosd(theta)^2;        % Malus's law -> 0.75
```

```python
import numpy as np
theta = np.deg2rad(30)
I = np.cos(theta)**2      # Malus's law -> 0.75
```

**Next:** how much power a wave carries - the Poynting vector.
""",
        ),
        _t(
            "The Poynting vector & energy flow",
            "11 min",
            """\
# The Poynting vector & energy flow

An EM wave carries **energy**, and the **Poynting vector** $\\vec{S}$ says how
much and which way it flows - power per unit area (W/m^2):

$$\\vec{S} = \\frac{1}{\\mu_0}\\,\\vec{E} \\times \\vec{B}.$$

It points in the direction the wave travels. For a plane wave, the
**time-averaged** magnitude (the intensity) is

$$\\langle S \\rangle = \\frac{1}{2}\\,c\\,\\varepsilon_0\\,E_0^2 = \\frac{E_0^2}{2\\eta_0}, \\qquad \\eta_0 = \\sqrt{\\frac{\\mu_0}{\\varepsilon_0}} \\approx 377\\ \\Omega.$$

The quantity $\\eta_0$ is the **impedance of free space** - the ratio $E_0/B_0c$ -
which reappears constantly in antennas and shielding. Intensity grows with the
**square** of the field amplitude:

```plot
{"title": "Wave intensity grows as E0^2 (slide free-space impedance scale)", "xLabel": "field amplitude E0 (V/m)", "yLabel": "intensity S (W/m^2)", "xRange": [0, 20], "yRange": [0, 0.6], "grid": true, "controls": [{"name": "eta", "range": [200, 500], "value": 377, "label": "wave impedance (ohm)"}], "functions": [{"expr": "x^2/(2*eta)", "label": "S = E0^2 / (2 eta)"}]}
```

## Inverse-square spreading

A point source radiates equally in all directions, so its intensity drops as
$1/r^2$ - the power spreads over a sphere of area $4\\pi r^2$:

$$S = \\frac{P}{4\\pi r^2}.$$

```plot
{"title": "Radiated intensity falls as 1/r^2 (slide source power)", "xLabel": "distance r (m)", "yLabel": "intensity (W/m^2)", "xRange": [0.5, 10], "yRange": [0, 4], "grid": true, "controls": [{"name": "P", "range": [10, 100], "value": 50, "label": "source power (W)"}], "functions": [{"expr": "P/(12.566*x^2)", "label": "S = P / (4 pi r^2)"}]}
```

## Radiation pressure

Because the wave carries momentum too, it pushes on whatever absorbs it -
**radiation pressure** $p = S/c$. Tiny, but real: the basis of **solar sails**
and a factor in comet tails pointing away from the Sun.

## Where this shows up

The Poynting vector is how engineers compute **antenna power density** (and
safety exposure limits), **solar panel** irradiance (~1 kW/m^2 at Earth),
**laser** intensity, and **microwave oven** heating. Even a DC circuit's energy,
strictly, flows through the *fields* around the wires, not inside the copper.

```matlab
eps0 = 8.854e-12; c = 3e8; E0 = 10;
S = 0.5*c*eps0*E0^2;      % time-averaged intensity (W/m^2)
p = S/c;                  % radiation pressure (Pa)
```

```python
eps0, c, E0 = 8.854e-12, 3e8, 10
S = 0.5*c*eps0*E0**2      # intensity (W/m^2)
p = S/c                   # radiation pressure (Pa)
```

**Next:** what happens when a wave hits a boundary.
""",
        ),
        _t(
            "Reflection & refraction at boundaries",
            "12 min",
            """\
# Reflection & refraction at boundaries

When a wave meets a boundary between two media, part **reflects** and part
**transmits** (refracts). The boundary conditions on $\\vec{E}$ and $\\vec{B}$ set
exactly how much of each.

## Snell's law: the bending

The transmitted wave changes direction because its speed changes:

$$n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2.$$

Going into a denser medium (higher $n$) bends the ray **toward** the normal.
Slide the second index and watch the refracted angle bend:

```plot
{"title": "Snell's law: refracted angle vs incidence (slide n2, n1=1)", "xLabel": "incidence angle (deg)", "yLabel": "refraction angle (deg)", "xRange": [0, 89], "yRange": [0, 90], "grid": true, "controls": [{"name": "n2", "range": [1, 2.5], "value": 1.5, "label": "second index n2"}], "functions": [{"expr": "deg(asin(clamp(sin(rad(x))/n2, -1, 1)))", "label": "refraction angle"}]}
```

## Total internal reflection

Going from dense to rare ($n_1 > n_2$), beyond the **critical angle**
$\\theta_c = \\arcsin(n_2/n_1)$ the wave cannot escape and reflects **completely**.
This traps light inside **optical fibers** and makes diamonds sparkle.

## Fresnel & normal incidence

The **Fresnel equations** give the reflected and transmitted fractions. At
**normal incidence** they simplify to a reflection coefficient

$$\\Gamma = \\frac{n_1 - n_2}{n_1 + n_2}, \\qquad R = \\Gamma^2, \\qquad T = 1 - R.$$

Reflectance climbs as the index mismatch grows. Slide $n_2$:

```plot
{"title": "Normal-incidence reflectance vs index mismatch (slide n2, n1=1)", "xLabel": "second index n2", "yLabel": "reflectance R", "xRange": [1, 4], "yRange": [0, 0.4], "grid": true, "controls": [{"name": "n1", "range": [1, 2], "value": 1, "label": "first index n1"}], "functions": [{"expr": "((n1 - x)/(n1 + x))^2", "label": "R = ((n1-n2)/(n1+n2))^2"}]}
```

Glass ($n=1.5$) in air reflects ~4% per surface - which is why camera lenses get
**anti-reflection coatings** (a quarter-wave layer that cancels the reflection by
interference).

## Where this shows up

Snell and Fresnel run **fiber optics**, **lenses and coatings**, **radar cross
section** (stealth shaping), **fingerprint sensors** (frustrated total internal
reflection), and **impedance matching** of antennas (the same math as the
Advanced reflection-coefficient lesson).

```matlab
n1 = 1; n2 = 1.5;
theta2 = asind(n1*sind(30)/n2);   % refracted angle for 30 deg
R = ((n1-n2)/(n1+n2))^2;          % normal-incidence reflectance ~ 0.04
```

```python
import numpy as np
n1, n2 = 1, 1.5
theta2 = np.degrees(np.arcsin(n1*np.sin(np.radians(30))/n2))
R = ((n1-n2)/(n1+n2))**2          # ~ 0.04
```

**Next:** animate a wave yourself.
""",
        ),
        _code(
            "Lab: a propagating & standing EM wave",
            "13 min",
            """\
# Animate a travelling wave, then superpose a reflected copy to form a
# STANDING wave. Plot snapshots in time and the standing-wave envelope.
import numpy as np
import matplotlib.pyplot as plt

c = 3e8
f = 1e9                          # 1 GHz
lam = c/f                        # wavelength (~0.3 m)
k = 2*np.pi/lam                  # wavenumber
w = 2*np.pi*f                    # angular frequency

z = np.linspace(0, 2*lam, 600)   # two wavelengths of space

plt.figure(figsize=(9, 6))

# -- Top: a travelling wave at several instants (it marches to the right) --
plt.subplot(2, 1, 1)
for frac, color in [(0.0, "#2563eb"), (0.2, "#16a34a"), (0.4, "#dc2626")]:
    t = frac/f                   # a fraction of one period
    E = np.cos(k*z - w*t)
    plt.plot(z*100, E, color=color, label=f"t = {frac:.1f} T")
plt.title("Travelling wave: E(z,t) = cos(kz - wt) moves right")
plt.xlabel("position z (cm)"); plt.ylabel("E"); plt.legend(); plt.grid(True)

# -- Bottom: forward + reflected = STANDING wave (fixed nodes) --
plt.subplot(2, 1, 2)
for frac, color in [(0.0, "#2563eb"), (0.125, "#16a34a"), (0.25, "#dc2626")]:
    t = frac/f
    forward = np.cos(k*z - w*t)
    reflected = np.cos(k*z + w*t)     # equal wave going the other way
    standing = forward + reflected    # = 2 cos(kz) cos(wt)
    plt.plot(z*100, standing, color=color, label=f"t = {frac:.3f} T")
plt.plot(z*100, 2*np.cos(k*z), "--", color="#94a3b8", label="envelope")
plt.plot(z*100, -2*np.cos(k*z), "--", color="#94a3b8")
plt.title("Standing wave: forward + reflected (nodes stay put)")
plt.xlabel("position z (cm)"); plt.ylabel("E"); plt.legend(); plt.grid(True)

plt.tight_layout(); plt.show()

print(f"frequency = {f/1e9:.1f} GHz, wavelength = {lam*100:.1f} cm")
print(f"standing-wave nodes are spaced half a wavelength = {lam*50:.1f} cm apart")

# Try it yourself:
#   1. Make the reflected wave smaller (0.5*np.cos(...)): a partial standing wave.
#   2. The MATLAB way: build z with linspace, loop over t, plot/hold on.
""",
        ),
    ),
)


# -- Electromagnetics -- Advanced: Transmission Lines & Antennas ---------------

_EM_ADVANCED = SeedCourse(
    slug="electromagnetics-advanced",
    title="Electromagnetics — Advanced: Transmission Lines & Antennas",
    description=(
        "High-frequency engineering: transmission lines (telegrapher equations, "
        "Z0, reflection coefficient, VSWR, standing waves), the Smith chart and "
        "impedance matching, antennas (the dipole, gain, radiation patterns, "
        "Friis), waveguides and microwave components, numerical EM and EMC - plus "
        "real RF/radar/wireless/MRI/fiber applications. Dual MATLAB/Python, "
        "interactive plots, and a runnable transmission-line/VSWR lab."
    ),
    level="Advanced",
    lessons=(
        _t(
            "Transmission lines: impedance, reflection & VSWR",
            "14 min",
            """\
# Transmission lines: impedance, reflection & VSWR

Once a cable is a significant fraction of a wavelength long, you can no longer
treat it as a simple wire - voltage and current become **waves** that travel,
reflect, and interfere. This is the world of RF.

## The telegrapher equations

Model the line as a ladder of tiny series inductance $L$ and shunt capacitance
$C$ per unit length. The voltage and current obey coupled wave equations - the
**telegrapher equations** - and propagate at $v = 1/\\sqrt{LC}$.

```mermaid
flowchart LR
  IN["source"] --> S1["L dz"] --> N1(("node"))
  N1 --> C1["C dz to ground"]
  N1 --> S2["L dz"] --> N2(("node")) --> LOAD["load ZL"]
```

## Characteristic impedance Z0

A wave travelling down the line sees a fixed ratio of voltage to current, the
**characteristic impedance**:

$$Z_0 = \\sqrt{\\frac{L}{C}}.$$

For coax this is set by the conductor geometry and dielectric - hence the
familiar **50 ohm** (RF/test) and **75 ohm** (video/antenna) cables.

## Reflection coefficient

If the load $Z_L$ does not equal $Z_0$, part of the wave **bounces back**:

$$\\Gamma = \\frac{Z_L - Z_0}{Z_L + Z_0}.$$

A matched load ($Z_L = Z_0$) gives $\\Gamma = 0$ - no reflection. An open or short
gives $|\\Gamma| = 1$ - total reflection. Slide the load and watch $\\Gamma$ swing
from -1 (short) through 0 (matched) to +1 (open):

```plot
{"title": "Reflection coefficient vs load (slide Z0)", "xLabel": "load impedance ZL (ohm)", "yLabel": "reflection coefficient", "xRange": [0, 200], "yRange": [-1.1, 1.1], "grid": true, "controls": [{"name": "Z0", "range": [25, 100], "value": 50, "label": "line impedance Z0 (ohm)"}], "functions": [{"expr": "(x - Z0)/(x + Z0)", "label": "gamma = (ZL - Z0)/(ZL + Z0)"}]}
```

## VSWR and standing waves

Forward and reflected waves interfere to make a **standing wave**; the ratio of
its max to min voltage is the **Voltage Standing Wave Ratio**:

$$\\text{VSWR} = \\frac{1 + |\\Gamma|}{1 - |\\Gamma|}.$$

VSWR = 1 is perfect; antenna installers aim for under ~1.5 (about 4% reflected
power). Slide the mismatch and watch VSWR blow up as $|\\Gamma| \\to 1$:

```plot
{"title": "VSWR explodes as reflection approaches 1", "xLabel": "|reflection coefficient|", "yLabel": "VSWR", "xRange": [0, 0.95], "yRange": [1, 40], "grid": true, "functions": [{"expr": "(1 + x)/(1 - x)", "label": "VSWR"}]}
```

## Where this shows up

This is the daily bread of **RF/microwave** design: matching antennas to
transmitters (a high VSWR can damage a transmitter), high-speed **PCB traces**
(controlled-impedance routing of USB/HDMI/Ethernet), and **cable TV/internet**
distribution.

```matlab
Z0 = 50; ZL = 75;
gamma = (ZL - Z0)/(ZL + Z0);      % 0.2
vswr = (1 + abs(gamma))/(1 - abs(gamma));  % 1.5
```

```python
Z0, ZL = 50, 75
gamma = (ZL - Z0)/(ZL + Z0)       # 0.2
vswr = (1 + abs(gamma))/(1 - abs(gamma))   # 1.5
```

**Next:** the graphical tool that tames all this - the Smith chart.
""",
        ),
        _t(
            "The Smith chart & impedance matching",
            "13 min",
            """\
# The Smith chart & impedance matching

Before computers, RF engineers solved transmission-line problems graphically on
the **Smith chart** - and it is still the universal language of RF, drawn live by
every network analyzer.

## What the chart is

The Smith chart maps the entire right-half impedance plane onto the **unit disk**
of the reflection coefficient $\\Gamma$. Constant-resistance and
constant-reactance lines become circles and arcs. The center is a perfect match
($\\Gamma = 0$, $Z = Z_0$); the rim is total reflection ($|\\Gamma| = 1$).

The reflection coefficient's magnitude is a **circle** of constant radius;
moving along a lossless line just rotates you around it. Here is the
$|\\Gamma| = $ const locus you would trace (slide the magnitude):

```plot
{"title": "Smith chart: constant-|gamma| circle in the reflection plane", "xLabel": "Re(gamma)", "yLabel": "Im(gamma)", "xRange": [-1.1, 1.1], "yRange": [-1.1, 1.1], "grid": true, "controls": [{"name": "g", "range": [0.1, 1], "value": 0.5, "label": "|gamma|"}], "parametric": [{"x": "g*cos(t)", "y": "g*sin(t)", "range": [0, 6.2832], "label": "constant |gamma|"}]}
```

## Why match?

A mismatch wastes power (reflected), distorts signals (standing waves), and can
damage transmitters. **Matching** inserts a lossless network that transforms
$Z_L$ to $Z_0$ at the design frequency.

## Matching techniques

| Technique | Idea | Best for |
|-----------|------|----------|
| **L-network** | two reactances (a series + a shunt) | narrowband, lumped |
| **Stub** | a shorted/open line length in shunt | distributed, microwave |
| **Quarter-wave** | a $\\lambda/4$ line of $Z = \\sqrt{Z_0 Z_L}$ | matching two real impedances |

The **quarter-wave transformer** is elegant: a line one quarter-wavelength long
inverts impedance, so a section of $Z = \\sqrt{Z_0 Z_L}$ matches a real load to
the line. Its match is perfect only at the design frequency and degrades as you
move away - slide the load to see the needed transformer impedance:

```plot
{"title": "Quarter-wave transformer impedance Z = sqrt(Z0 ZL) (slide Z0)", "xLabel": "load ZL (ohm)", "yLabel": "transformer Z (ohm)", "xRange": [10, 200], "yRange": [0, 150], "grid": true, "controls": [{"name": "Z0", "range": [25, 100], "value": 50, "label": "line Z0 (ohm)"}], "functions": [{"expr": "sqrt(Z0*x)", "label": "Z_quarter-wave"}]}
```

```mermaid
flowchart LR
  SRC["source Z0"] --> QW["quarter-wave line sqrt(Z0 ZL)"] --> LOAD["load ZL"]
```

## Where this shows up

Every **antenna tuner**, **amplifier** input/output network, **filter** design,
and **RFID** tag is a matching problem. Modern software (Keysight ADS, scikit-rf
in Python) does it numerically, but the Smith chart is still how engineers
*think* about it.

```matlab
Z0 = 50; ZL = 100;
Zqw = sqrt(Z0*ZL);        % quarter-wave transformer -> ~70.7 ohm
```

```python
import numpy as np
Z0, ZL = 50, 100
Zqw = np.sqrt(Z0*ZL)      # ~70.7 ohm
```

**Next:** launching the wave into free space - antennas.
""",
        ),
        _t(
            "Antennas: the dipole, gain & radiation patterns",
            "14 min",
            """\
# Antennas: the dipole, gain & radiation patterns

An **antenna** is a matched transition between a guided wave (on a line) and a
free-space wave. When current oscillates in a conductor comparable to a
wavelength, it **radiates**.

## The half-wave dipole

The classic antenna is a conductor a **half wavelength** long, fed in the middle.
At resonance it presents ~73 ohms (close to 50 ohm cable) and radiates a
doughnut-shaped pattern - strongest broadside, nothing off the ends. Its
normalized pattern:

```plot
{"title": "Half-wave dipole radiation pattern (relative field vs angle)", "xLabel": "angle from antenna axis (deg)", "yLabel": "relative field", "xRange": [0, 180], "yRange": [0, 1.05], "grid": true, "functions": [{"expr": "abs(cos(1.5708*cos(rad(x)))/sin(rad(x) + 0.0001))", "label": "dipole pattern"}]}
```

Note the deep nulls at 0 and 180 degrees (off the ends) and the broad maximum at
90 degrees (broadside).

## Gain, directivity & beamwidth

- **Directivity** $D$ - how much a pattern concentrates power versus an
  isotropic radiator.
- **Gain** $G = e\\,D$ - directivity times efficiency $e$, usually in **dBi**.
- **Beamwidth** - the angular width of the main lobe.

A bigger antenna (in wavelengths) makes a **narrower, higher-gain** beam. Slide
an aperture size and watch the beam sharpen and the peak rise:

```plot
{"title": "Bigger aperture = narrower, higher-gain beam (slide size)", "xLabel": "angle (deg)", "yLabel": "relative field", "xRange": [-60, 60], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "D", "range": [1, 8], "value": 3, "label": "aperture size (wavelengths)"}], "functions": [{"expr": "abs(sin(D*rad(x)*3.1416 + 0.0001)/(D*rad(x)*3.1416 + 0.0001))", "label": "array-factor beam"}]}
```

## Near field vs far field

Close to the antenna (the **near field**, within ~$2D^2/\\lambda$) the fields are
complicated and store reactive energy. Far away (the **far field**) the wave is
a clean spherical wave and the pattern is fixed - this is where you measure and
use an antenna.

## The Friis transmission equation

How much power reaches a receiver in free space:

$$\\frac{P_r}{P_t} = G_t\\,G_r\\left(\\frac{\\lambda}{4\\pi R}\\right)^2.$$

The $1/R^2$ free-space spreading (and the $\\lambda^2$) is why links get weaker
with distance and higher frequency. Slide the gain product:

```plot
{"title": "Friis: received power vs range (slide combined antenna gain)", "xLabel": "range R (km)", "yLabel": "relative received power", "xRange": [1, 20], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "G", "range": [1, 10], "value": 4, "label": "Gt*Gr (linear)"}], "functions": [{"expr": "G/(x^2)", "label": "Pr ~ G / R^2"}]}
```

```mermaid
flowchart LR
  TX["transmitter Pt, gain Gt"] --> PATH["free space, range R, loss ~ R^2"]
  PATH --> RX["receiver Pr, gain Gr"]
```

## Where this shows up

Antenna types match the job: **dipole/monopole** (broadcast, FM), **Yagi** (TV,
ham), **patch** (GPS, phones), **parabolic dish** (satellite, radio astronomy),
and **phased arrays** (radar, 5G beamforming - steering the beam electronically).

```matlab
lambda = 0.125; R = 1000; Gt = 2; Gr = 2;
Pr_over_Pt = Gt*Gr*(lambda/(4*pi*R))^2;   % Friis free-space ratio
```

```python
import numpy as np
lam, R, Gt, Gr = 0.125, 1000, 2, 2
ratio = Gt*Gr*(lam/(4*np.pi*R))**2        # Friis ratio
```

**Next:** guiding microwaves without radiating - waveguides.
""",
        ),
        _t(
            "Waveguides & microwave components",
            "12 min",
            """\
# Waveguides & microwave components

At high microwave frequencies, ordinary cables get **lossy** (the dielectric and
skin effect eat the signal). The fix: guide the wave inside a hollow metal pipe -
a **waveguide** - where the wave bounces along with very low loss.

## Modes and the cutoff frequency

A waveguide does not support every frequency. Below a **cutoff frequency**
(set by the guide's cross-section, roughly when the width is half a wavelength)
the wave **cannot propagate** - it decays. Above cutoff it travels in distinct
field patterns called **modes** (TE, TM). The dominant rectangular mode has

$$f_c = \\frac{c}{2a},$$

where $a$ is the broad-wall width. The guide is a built-in **high-pass filter**.
Slide the width and watch the cutoff move:

```plot
{"title": "Waveguide cutoff frequency vs broad-wall width", "xLabel": "broad-wall width a (mm)", "yLabel": "cutoff frequency (GHz)", "xRange": [5, 50], "yRange": [0, 35], "grid": true, "controls": [{"name": "k", "range": [1, 2], "value": 1, "label": "mode factor"}], "functions": [{"expr": "150*k/x", "label": "fc = c/(2a)"}]}
```

The phase velocity inside a guide actually **exceeds** $c$ (no information moves
faster than light - the group velocity stays below $c$), and it depends on
frequency, so waveguides are **dispersive**.

## The microwave component kit

Lumped resistors and capacitors do not behave at these frequencies, so microwave
engineering uses **distributed** structures:

| Component | Does |
|-----------|------|
| Directional coupler | sample a fraction of the forward/reverse wave |
| Circulator / isolator | route power one way (protects transmitters) |
| Cavity resonator | a high-Q "LC" made of a metal box (filters, oscillators) |
| Magic tee / hybrid | split and combine signals with set phases |
| Attenuator / phase shifter | control amplitude and phase |

```mermaid
flowchart LR
  SRC["microwave source"] --> ISO["isolator (one-way)"] --> WG["waveguide"] --> ANT["antenna / load"]
```

## Where this shows up

Waveguides feed **radar** dishes and **satellite** ground stations, carry the
output of a **microwave oven's** magnetron to the cooking cavity, route signals
inside **5G base stations** and **radio telescopes**, and form the **cavities**
in particle accelerators.

```matlab
c = 3e8; a = 22.86e-3;            % WR-90 X-band guide width
fc = c/(2*a);                     % cutoff ~ 6.56 GHz
```

```python
c, a = 3e8, 22.86e-3
fc = c/(2*a)                      # cutoff ~ 6.56 GHz
```

**Next:** when geometry gets complex - numerical EM and EMC.
""",
        ),
        _t(
            "Numerical EM, EMC & shielding",
            "12 min",
            """\
# Numerical EM, EMC & shielding

Real structures - a phone, a car, an aircraft - are far too complex to solve
Maxwell's equations by hand. Engineers turn to **computational
electromagnetics** and to the discipline of keeping systems from interfering -
**EMC**.

## Solving Maxwell numerically

| Method | Idea | Best for |
|--------|------|----------|
| **FDTD** | step the fields forward in time on a grid (finite-difference time-domain) | broadband, transients, antennas |
| **FEM** | mesh the volume into elements, solve in frequency | complex geometry, resonators |
| **MoM** | solve for surface currents (method of moments) | wire/surface antennas, scattering |

**FDTD** is the most intuitive: discretize space and time, then leapfrog $E$ and
$B$ from one equation to the next, exactly as Maxwell's curl equations dictate -
which is what the lab almost does for a transmission line. Stability requires the
**Courant condition** $c\\,\\Delta t \\le \\Delta x / \\sqrt{d}$, so finer grids need
smaller time steps:

```plot
{"title": "FDTD stability: max time step shrinks with cell size (slide dim)", "xLabel": "grid cell size dx (mm)", "yLabel": "max stable dt (ps)", "xRange": [0.5, 10], "yRange": [0, 35], "grid": true, "controls": [{"name": "d", "range": [1, 3], "value": 2, "label": "dimensions"}], "functions": [{"expr": "x/(0.3*sqrt(d))", "label": "Courant limit"}]}
```

## EMC: coexisting without interference

Every fast-switching circuit both **emits** noise and is **susceptible** to it.
**EMC** (electromagnetic compatibility) is engineering so devices neither jam
others nor get jammed - and pass mandatory FCC/CE limits.

```mermaid
flowchart LR
  SRC["noise source (switching, clock)"] --> PATH["coupling path (radiated / conducted)"]
  PATH --> VICTIM["victim circuit"]
  PATH --> FIX["break the path: shield, filter, ground"]
```

The three levers: reduce the **source**, break the **coupling path**, or harden
the **victim**.

## Shielding

A conductive enclosure (a **Faraday cage**) reflects and absorbs incident fields.
Shielding effectiveness, in dB, grows with conductivity, thickness, and
frequency - but every **slot, seam, and cable penetration leaks**. A gap acts
like a slot antenna; the leakage rises sharply as a slot approaches a half
wavelength. Slide frequency to see shielding degrade as wavelength nears the slot
size:

```plot
{"title": "Shielding leakage rises as wavelength nears the slot size", "xLabel": "frequency (GHz)", "yLabel": "leakage (relative)", "xRange": [0.1, 10], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "L", "range": [1, 6], "value": 3, "label": "slot length (cm)"}], "functions": [{"expr": "clamp(L*x/15, 0, 1)", "label": "leakage ~ slot / wavelength"}]}
```

## Where this shows up

CEM tools (Ansys HFSS, CST, Sonnet, open-source meep/openEMS) design every
**antenna, chip package, and connector**. EMC and shielding decide whether a
product **passes certification**: medical devices, automotive (a car is a rolling
EMC nightmare), avionics, and consumer electronics all live or die by it.

```matlab
c = 3e8; dx = 1e-3; dim = 3;
dt_max = dx/(c*sqrt(dim));         % FDTD Courant stability limit (s)
```

```python
import numpy as np
c, dx, dim = 3e8, 1e-3, 3
dt_max = dx/(c*np.sqrt(dim))       # Courant limit (s)
```

**Next:** put a line and its reflections in code.
""",
        ),
        _code(
            "Lab: transmission-line reflection & VSWR",
            "14 min",
            """\
# Compute the reflection coefficient, VSWR, and the voltage standing-wave
# pattern along a mismatched transmission line. Sweep the load to see the match.
import numpy as np
import matplotlib.pyplot as plt

Z0 = 50.0                       # 50 ohm line
freq = 1e9                      # 1 GHz
c = 3e8
lam = c/freq                    # wavelength
beta = 2*np.pi/lam              # phase constant

# Position along the line, from the load (z=0) back toward the source.
z = np.linspace(0, 2*lam, 600)

plt.figure(figsize=(9, 6))

# -- Top: standing-wave voltage pattern for three different loads --
plt.subplot(2, 1, 1)
loads = [(50.0, "#16a34a", "ZL=50 (matched)"),
         (100.0, "#2563eb", "ZL=100"),
         (1e9, "#dc2626", "ZL=open")]
for ZL, color, label in loads:
    gamma = (ZL - Z0)/(ZL + Z0)
    # |V(z)| = |1 + gamma * exp(-2 j beta z)|  (incident normalized to 1)
    Vz = np.abs(1 + gamma*np.exp(-2j*beta*z))
    vswr = (1 + abs(gamma))/(1 - abs(gamma)) if abs(gamma) < 1 else np.inf
    plt.plot(z*100, Vz, color=color, label=f"{label}, VSWR={vswr:.1f}")
plt.title("Voltage standing-wave pattern along the line")
plt.xlabel("distance from load (cm)"); plt.ylabel("|V| (normalized)")
plt.legend(); plt.grid(True)

# -- Bottom: VSWR as the load resistance is swept --
plt.subplot(2, 1, 2)
ZL_sweep = np.linspace(5, 500, 400)
gamma_sweep = (ZL_sweep - Z0)/(ZL_sweep + Z0)
vswr_sweep = (1 + np.abs(gamma_sweep))/(1 - np.abs(gamma_sweep))
plt.plot(ZL_sweep, vswr_sweep, color="#7c3aed")
plt.axvline(Z0, ls="--", color="#94a3b8", label="ZL = Z0 (VSWR=1)")
plt.title("VSWR vs load resistance (best at ZL = Z0)")
plt.xlabel("load resistance ZL (ohm)"); plt.ylabel("VSWR")
plt.ylim(1, 12); plt.legend(); plt.grid(True)

plt.tight_layout(); plt.show()

# Report one mismatch numerically.
ZL = 100.0
gamma = (ZL - Z0)/(ZL + Z0)
vswr = (1 + abs(gamma))/(1 - abs(gamma))
print(f"ZL = {ZL:.0f} ohm: gamma = {gamma:.3f}, VSWR = {vswr:.2f}")
print(f"reflected power fraction = |gamma|^2 = {gamma**2:.3f}")

# Try it yourself:
#   1. Set ZL = 0 (a short): VSWR -> infinity, deep nulls in |V(z)|.
#   2. The MATLAB way: same formulas, plot with hold on; abs() and angle() of gamma.
""",
        ),
        _t(
            "Applications: RF, radar, wireless, MRI & fiber",
            "12 min",
            """\
# Applications: RF, radar, wireless, MRI & fiber

Everything in this track - static fields, Maxwell's equations, waves,
transmission lines, antennas - comes together in the systems that define modern
life. Here is the throughline, application by application.

## Wireless communication (Wi-Fi, cellular, 5G)

A transmitter matches its power amplifier to an **antenna** (transmission-line
and Smith-chart matching), which launches a **wave** (Maxwell) that spreads by
the **Friis** law and is captured by a receive antenna. **5G** uses **phased
arrays** to steer narrow beams (antenna directivity) at millimeter waves, where
**waveguide**-like structures and careful **EMC** are essential.

## Radar

Send a pulse, listen for the echo. Range comes from the round-trip time
($R = c\\,\\Delta t/2$), and speed from the **Doppler** frequency shift. The
returned power follows the radar equation, which falls off as $1/R^4$ (out **and**
back) - far steeper than a one-way link. Slide the target size:

```plot
{"title": "Radar return power falls as 1/R^4 (slide target cross-section)", "xLabel": "range R (km)", "yLabel": "relative echo power", "xRange": [1, 20], "yRange": [0, 1.05], "grid": true, "controls": [{"name": "sigma", "range": [0.2, 2], "value": 1, "label": "radar cross-section (relative)"}], "functions": [{"expr": "sigma/(x^4)", "label": "Pr ~ sigma / R^4"}]}
```

This is why **stealth** aircraft shape and coat their surfaces to shrink $\\sigma$,
and why long-range radars need huge antennas and power.

## MRI

A **magnetic resonance imaging** scanner is applied electromagnetics end to end:
a huge static $B_0$ (1.5-7 T superconducting magnet) aligns proton spins;
**gradient coils** add position-dependent fields; an **RF coil** (an antenna at
the Larmor frequency $f = \\gamma B_0$, ~64 MHz at 1.5 T) tips the spins and then
receives the faint re-radiated signal. The Larmor frequency scales linearly with
field:

```plot
{"title": "MRI Larmor frequency vs magnet field (slide gyromagnetic ratio)", "xLabel": "magnet field B0 (tesla)", "yLabel": "Larmor frequency (MHz)", "xRange": [0.5, 7], "yRange": [0, 320], "grid": true, "controls": [{"name": "g", "range": [30, 50], "value": 42.58, "label": "gamma (MHz/T)"}], "functions": [{"expr": "g*x", "label": "f = gamma * B0"}]}
```

## Fiber optics

Light (an EM wave at ~200 THz) is trapped by **total internal reflection**
(the Intermediate reflection lesson) in a glass core of slightly higher index
than its cladding. Modern fiber loses only ~0.2 dB/km, carrying terabits across
oceans - the backbone of the internet.

```mermaid
flowchart LR
  STATIC["static fields"] --> MAXWELL["Maxwell's equations"]
  MAXWELL --> WAVES["EM waves"]
  WAVES --> LINES["transmission lines + antennas"]
  LINES --> APPS["RF, radar, 5G, MRI, fiber, radio astronomy"]
```

## More fields where this lives

- **Radio astronomy** - giant dishes and arrays (VLA, ALMA) detect faint cosmic
  EM waves.
- **Microwave heating** - ovens, industrial drying, medical ablation.
- **Wireless power** - resonant inductive coupling (the Basics induction lesson).
- **Particle accelerators** - RF cavities and waveguides push charged beams.

## The throughline

Charge makes fields (Coulomb, Gauss); moving charge makes magnetism
(Biot-Savart, Ampere); changing fields make each other and propagate as waves
(Maxwell); we guide, match, radiate, and receive those waves (lines, Smith chart,
antennas); and we simulate and shield the whole thing (numerical EM, EMC). Four
equations - and an entire technological civilization.

```matlab
gamma = 42.58e6; B0 = 1.5;
f_larmor = gamma*B0;              % MRI RF frequency ~ 63.9 MHz
c = 3e8; dt = 100e-6;
R = c*dt/2;                       % radar range from echo delay (m)
```

```python
gamma, B0 = 42.58e6, 1.5
f_larmor = gamma*B0               # ~63.9 MHz
c, dt = 3e8, 100e-6
R = c*dt/2                        # radar range (m)
```

That is the whole arc, from a single electron's field to a transcontinental
fiber link. The components and frequencies change; Maxwell's four equations
never do.
""",
        ),
    ),
)


ELECTROMAGNETICS_COURSES: tuple[SeedCourse, ...] = (
    _EM_BASICS,
    _EM_INTERMEDIATE,
    _EM_ADVANCED,
)

__all__ = ["ELECTROMAGNETICS_COURSES"]
